"""Defines the YAML specifications"""
import datetime
from enum import Enum
from typing import Any, Optional, Callable

import semver
from pydantic import BaseModel, ConfigDict, Field, GetJsonSchemaHandler, field_validator, model_serializer
from pydantic_core import core_schema
from pydantic.json_schema import JsonSchemaValue

class Config(BaseModel):
    model_config = ConfigDict(
        json_schema_serialization_defaults_required=True,
        validate_assignment=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
        extra='forbid'
    )

# from https://python-semver.readthedocs.io/en/latest/advanced/combine-pydantic-and-semver.html
class _Version:
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        def validate_from_str(value: str) -> semver.Version:
            return semver.Version.parse(value)

        from_str_schema = core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(validate_from_str),
            ]
        )

        return core_schema.json_or_python_schema(
            json_schema=from_str_schema,
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(semver.Version),
                    from_str_schema,
                ]
            ),
            serialization = core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return handler(core_schema.str_schema())


class Approver(Config):
    Name: str | None = Field(
        description='Name of of the approver'
    )
    Email: str | None = Field(
        description='Email address of the approver'
    )
    Date: datetime.date | None = Field(
        description='ISO 8601 date of approval from the approver'
    )


class StatusEnum(str, Enum):
    proposed = 'Proposed'
    accepted = 'Accepted'
    deprecated = 'Deprecated'

class MetadataSpec(Config):
    Proposed: datetime.date = Field(
        description='ISO 8601 date a specification was proposal'
    )
    Adoption: datetime.date | None = Field(
        description='ISO 8601 date a specification was adapted'
    )
    Modified: datetime.date | None = Field(
        description='ISO 8601 date a specification was last modified'
    )
    Version: _Version = Field(
        description='Semantic version for a specification'
    )
    Status: StatusEnum = Field(
        description='Lifecycle status for a specification'
    )
    Approvers: list[Approver] = Field(
        description='List of approvers for a specification'
    )


class SpecID(Config):
    ID: int | None = Field(
        description='Unique, with respect to a specification type, ID for a specification',
        gt=0,
        lt=1000
    )

class SpecBase(Config):
    Title: str | None = Field(
        description='Short title of a specification',
        max_length=100
    )
    Description: str | None = Field(
        description='Longer form description of a specification is attempting to address'
    )


class BaseOverride(Config):
    Profile: str | SpecID = Field(
        description='Title or ID of profile that override is tied to.'
    )
    TitleUpdate: Optional[str] = Field(
        default=None, description='Update the title of a specification'
    )
    DescriptionUpdate: Optional[str] = Field(
        default=None, description='Update the description of a specification'
    )

class ActionOverride(BaseOverride, Config):
    WeightUpdate: Optional[int] = Field(
        default=None, description='Update the weight for an action'
    )

class StdOverride(BaseOverride, Config):
    AddIDs: Optional[list[SpecID]] = Field(
        default=[],
        validate_default=True,
        description='List of sub-specification IDs to add to a specification'
    )
    DropIDs: Optional[list[SpecID]] = Field(
        default=[],
        validate_default=True,
        description='List of sub-specification IDs to drop from a specification'
    )

    # Custom function to ensure that the validator is setup
    # to always include the default lists for AddIDs and
    # DropIDs. Can be defined with any name
    @field_validator('AddIDs', 'DropIDs', mode='after')
    def setup_default(cls, value, values, **kwargs):
        if value:
            return value

        return []

OVERRIDE_MAP = {
    'std': StdOverride,
    'action': ActionOverride
}


class ActionItem(SpecID, Config):
    Overrides: Optional[list[ActionOverride]] = Field(
        default=[],
        description='List of action overrides by profile'
    )

class Reference(Config):
    Name: str | None = Field(
        description='Name or short title of a reference'
    )
    Link: str | None = Field(
        description='URL link for a reference'
    )
    Comment: str | None = Field(
        description='Comments or longer form description of how a reference related to a specification'
    )

class ActionSpec(ActionItem, SpecBase, SpecID, Config):
    ImplementationTypes: list[str | None] = Field(
        description='List of how the specification is implemented',
        alias='Implementation Types'
    )
    References: list[Reference] = Field(
        description='List reference objects'
    )
    Notes: list[str | None] = Field(
        description='List of notes related to a specific action'
    )

    # Custom function to help make sure the overrides
    # are always correctly ordered when serialized.
    # Can be defined with any name
    @model_serializer(when_used='json')
    def serialize_json_model(self):
        model = self.model_dump()
        
        # ensure overrides are always at the end of the serialized output
        # if they exist, by removing it and then adding it back.
        if 'Overrides' in list(model.keys()):
            overrides = model.get('Overrides')
            del model['Overrides']
            model['Overrides'] = overrides
            return model

        # else just return the original model
        return model

class Action(Config):
    Metadata: MetadataSpec = Field(description='Metadata for an Action specification')
    Specification: ActionSpec = Field(description='An action specification')


class CapabilityItem(SpecBase, Config):
    Actions: list[SpecID | ActionItem] | None = Field(description='List of action IDs')

class CapabilitySpec(CapabilityItem, SpecBase, SpecID, Config):
    Overrides: list[StdOverride] | None = Field(description='List of overrides by profile')

class Capability(Config):
    Metadata: MetadataSpec = Field(description='Metadata for a capability specification')
    Specification: CapabilitySpec = Field(description='Capability specification')


class DomainItem(SpecBase, Config):
    Capabilities: list[SpecID | CapabilityItem] = Field(
        description='List of capability IDs or capability items'
    )

class DomainSpec(DomainItem, SpecBase, SpecID, Config):
    Overrides: list[StdOverride] | None = Field(description='List of overrides by profile')

class Domain(Config):
    Metadata: MetadataSpec = Field(description='Metadata for a domain specification')
    Specification: DomainSpec = Field(description='A domain specification')


class ProfileSpec(SpecBase, SpecID, Config):
    Domains: list[SpecID | DomainItem] = Field(description='List of domain IDs or domain items')

class Profile(Config):
    Metadata: MetadataSpec = Field(description='Metadata for a profile specification')
    Specification: ProfileSpec = Field(description='A profile specification')