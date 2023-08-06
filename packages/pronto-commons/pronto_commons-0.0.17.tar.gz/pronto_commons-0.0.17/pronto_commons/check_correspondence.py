from dataclasses import fields, dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Tuple, Type, Mapping, Dict, Any

from bson import ObjectId
import marshmallow.fields as f

from .marshmallow import ObjectIdField


@dataclass
class OverrideExpectedType:
    ref_suffix_to_match: str
    entity_type_to_match: Type
    new_expected_swagger_type: str


@dataclass
class CorrespondenceChecker:

    # decoded swagger from the yaml
    swagger: Dict[str, Any]

    # these are some types that we have wrapped in Optional
    # because there is no way to recognize an Optional for an arbitrary
    # type, we have to brute force away. but it is fine, because we can
    # just add to this list when there is a new case.
    types_wrapped_in_optional: List[Type]

    entity_to_schema_and_swagger: Mapping[Type, Tuple[Type[f.Field], str]]
    override_expected_types: List[OverrideExpectedType]

    def check(
        self, schema, entity, non_serialized_fields: List[str], swagger_name: str
    ) -> None:
        """
        Asserts that properties in the schema and the entity correspond to each other.
        It doesn't check everything, since Marshmallow doesn't work well with typing.

        :param: schema: A Marshmallow schema, inheriting from "Schema". The class itself, not the instance!
        :param: entity: A Dataclass entity. The class itself, not the instance!
        :param: non_serialized_fields: Fields that are not supposed to be in the Marshmallow or the Swagger
        :param: swagger_name: The name of the key in /components/schemas that represents this entity and schema
        """
        swagger_data_type = self.swagger["components"]["schemas"][swagger_name]
        properties = swagger_data_type["properties"]

        schema = schema._declared_fields
        for field in fields(entity):
            if field.name in non_serialized_fields:
                assert (
                    field.name not in schema
                ), f"entity {entity}: {field.name} is in marshmallow schema, even though it is marked as nonserialized in correspondence checker source code"
                assert (
                    field.name not in properties
                ), f"entity {entity}: {field.name} is in swagger, even though it is not in schema:\n{properties[field.name]}"
                continue
            else:
                assert (
                    field.name in schema
                ), f"entity {entity}: field {field.name} is not marked as nonserialized, but is missing in schema"

            field_type: Type = field.type

            for t in self.types_wrapped_in_optional:
                if field_type == Optional[t]:
                    field_type = t
                    assert not schema[field.name].required
                    assert field.name not in swagger_data_type.get(
                        "required", []
                    ) or properties[field.name].get(
                        "nullable"
                    ), f"entity {entity}, field name {field.name}, is marked as required in swagger, but it is optional in entity"
                    break

            expect: Tuple[Type[f.Field], str]

            # this block determines the expected marshmallow
            # type based on the entity type
            if field_type is str:
                if field.name == "profile_picture":
                    expect = f.Url, "string"
                else:
                    expect = f.Str, "string"
            elif field_type is int:
                expect = f.Int, "integer"
            elif field_type is float:
                expect = f.Float, "number"
            elif field_type is bool:
                expect = f.Boolean, "boolean"
            elif field_type is Decimal:
                expect = f.Decimal, "Price"
            elif field_type is datetime:
                expect = f.DateTime, "DateTime"
            elif field_type is ObjectId:
                expect = ObjectIdField, "ObjectId"
            else:
                try:
                    expect = self.entity_to_schema_and_swagger[field_type]
                except KeyError:
                    assert (
                        False
                    ), f"entity {entity}: unknown type {field_type} encountered for field {field.name}. types that can be wrapped in Optional[...] should be specified above"

            assert expect[0] is type(
                schema[field.name]
            ), f"\nentity {entity}\nfield name {field.name}:\n-------------------\nexpected type: {expect[0]}\nactual type {schema[field.name]}"

            swagger_type = properties[field.name].get("type")
            if swagger_type:
                assert (
                    swagger_type == expect[1]
                ), f"entity {entity}, field name {field.name}: expected swagger type {expect[1]} but got {swagger_type}"
            else:
                # handle the idiom where something is made nullable by wrapping it
                # in an anyOf with one item
                anyOf = properties[field.name].get("anyOf", [])
                if len(anyOf) == 1:
                    properties[field.name] = anyOf[0]

                for o in self.override_expected_types:
                    if (
                        properties[field.name]["$ref"].endswith(o.ref_suffix_to_match)
                        and field_type is o.entity_type_to_match
                    ):
                        assert expect[1] == o.new_expected_swagger_type
                        break
                else:
                    # if it is not a special case
                    # the actual swagger reference
                    # must match the expected one
                    actual_ref = properties[field.name]["$ref"]
                    expected_ref = "#/components/schemas/" + expect[1]
                    assert (
                        actual_ref == expected_ref
                    ), f"entity {entity} field {field.name} has ref in swagger {properties[field.name]['$ref']} but it should be {expect[1]} according to {field_type}"
