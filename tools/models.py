"""Defines the YAML specifications"""
import datetime
from enum import Enum
from typing import Any, Optional, Callable

import semver
from pydantic.dataclasses import dataclass
from pydantic import ConfigDict, Field, GetJsonSchemaHandler
from pydantic_core import core_schema
from pydantic.json_schema import JsonSchemaValue

CONFIG = ConfigDict(
    json_schema_serialization_defaults_required=True,
    frozen=True,
    validate_by_alias=True,
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

@dataclass(config=CONFIG)
class Approver():
    Name: str | None = Field(
        example='Reviewer One'
    )
    Email: str | None = Field(
        example='reviewer1@example.com'
    )
    Date: datetime.date | None = Field(
        description='ISO 8601 date of approval from approver'
    )

class StatusEnum(str, Enum):
    proposed = 'Proposed'
    accepted = 'Accepted'
    deprecated = 'Deprecated'

@dataclass(config=CONFIG)
class MetadataSpec():
    Proposed: datetime.date = Field(
        example=datetime.date.today(), description='ISO 8601 date a specification was proposal'
    )
    Adoption: datetime.date | None = Field(
        description='ISO 8601 date a specification was adapted'
    )
    Modified: datetime.date | None = Field(
        description='ISO 8601 date a specification was last modified'
    )
    Version: _Version = Field(
        example='0.0.1', description='Semantic version for a specification'
    )
    Status: StatusEnum = Field(
        example=StatusEnum.proposed, description='Lifecycle status for a specification'
    )
    Approvers: list[Approver] = Field(
        example=[Approver(Name=None, Email=None, Date=None)],
        description='List of approvers for a specification'
    )

@dataclass(config=CONFIG)
class SpecID():
    ID: int = Field(description='Unique, with respect to a specification type, ID for a specification')

@dataclass(config=CONFIG)
class SpecBase():
    Title: str | None = Field(
        description='Short title a specification'
    )
    Description: str | None = Field(
        description='Longer form description of a specification is attempting to address'
    )

@dataclass(config=CONFIG)
class BaseOverride():
    Profile: str = Field(
        description='Profile override is tied to.'
    )
    TitleUpdate: Optional[str] = Field(
        default=None, description='Update the title of a specification'
    )
    DescriptionUpdate: Optional[str] = Field(
        default=None, description='Update the description of a specification'
    )

@dataclass(config=CONFIG)
class ActionOverride(BaseOverride):
    WeightUpdate: Optional[int] = Field(
        default=None, description='Update the weight for an action'
    )

@dataclass(config=CONFIG)
class StdOverride(BaseOverride):
    AddIDs: Optional[list[int]] = Field(
        default=None, description='List of sub-specification IDs to add to a specification'
    )
    DropIDs: Optional[list[int]] = Field(
        default=None, description='List of sub-specification IDs to drop from a specification'
    )

@dataclass(config=CONFIG)
class Reference():
    Name: str | None = Field(
        description='Name or short title of a reference'
    )
    Link: str | None = Field(
        description='URL link for a reference'
    )
    Comment: str | None = Field(
        description='Comments or longer form description of how a reference related to a specification'
    )

@dataclass(config=CONFIG)
class ActionSpec(SpecBase, SpecID):
    ImplementationTypes: list[str | None] = Field(
        example=[None],
        description='List of how the specification is implemented',
        alias='Implementation Types'
    )
    References: list[Reference] = Field(
        example=[Reference(Name=None, Link=None, Comment=None)],
        description='List reference objects'
    )
    Notes: list[str | None] = Field(
        example=[None], description='List of notes related to a specific action'
    )

@dataclass(config=CONFIG)
class ActionItem(SpecID):
    Overrides: Optional[list[ActionOverride] | None] = Field(
        default=None, description='List of action overrides by profile'
    )

@dataclass(config=CONFIG)
class Action():
    Metadata: MetadataSpec = Field(description='Metadata for an Action specification')
    Specification: ActionSpec = Field(description='An action specification')

@dataclass(config=CONFIG)
class CapabilityItem(SpecBase):
    Actions: list[SpecID | ActionItem] | None = Field(description='List of action IDs')

@dataclass(config=CONFIG)
class CapabilitySpec(CapabilityItem, SpecBase, SpecID):
    Overrides: list[StdOverride] | None = Field(description='List of overrides by profile')

@dataclass(config=CONFIG)
class Capability():
    Metadata: MetadataSpec = Field(description='Metadata for a capability specification')
    Specification: CapabilitySpec = Field(description='Capability specification')

@dataclass(config=CONFIG)
class DomainItem(SpecBase):
    Capabilities: list[SpecID | CapabilityItem] = Field(
        description='List of capability IDs or capability items'
    )

@dataclass(config=CONFIG)
class DomainSpec(DomainItem, SpecBase, SpecID):
    Overrides: list[StdOverride] | None = Field(description='List of overrides by profile')

@dataclass(config=CONFIG)
class Domain():
    Metadata: MetadataSpec = Field(description='Metadata for a domain specification')
    Specification: DomainSpec = Field(description='A domain specification')

@dataclass(config=CONFIG)
class ProfileSpec(SpecBase, SpecID):
    Domains: list[SpecID | DomainItem] = Field(description='List of domain IDs or domain items')

@dataclass(config=CONFIG)
class Profile():
    Metadata: MetadataSpec = Field(description='Metadata for a profile specification')
    Specification: ProfileSpec = Field(description='A profile specification')