"""Defines the YAML specifications"""
import datetime
from enum import Enum
from typing import Any, Callable

import semver
from pydantic.dataclasses import dataclass
from pydantic import ConfigDict, Field, GetJsonSchemaHandler
from pydantic_core import core_schema
from pydantic.json_schema import JsonSchemaValue

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

@dataclass(config=ConfigDict(json_schema_serialization_defaults_required=True))
class Approver():
    Name: str = Field(
        default=None, example='Reviewer One'
    )
    Email: str = Field(
        default=None, example='reviewer1@example.com'
    )
    Date: datetime.date = Field(
        default=None, description='ISO 8601 date of approval from approver'
    )

class StatusEnum(str, Enum):
    proposed = 'Proposed'
    approved = 'Approved'
    deprecated = 'Deprecated'

@dataclass(config=ConfigDict(json_schema_serialization_defaults_required=True))
class MetadataSpec():
    Proposed: datetime.date = Field(
        default=datetime.date.today(), description='ISO 8601 date a specification was proposal'
    )
    Adoption: datetime.date = Field(
        default=None, description='ISO 8601 date a specification was adapted'
    )
    Modified: datetime.date = Field(
        default=None, description='ISO 8601 date a specification was last modified'
    )
    Version: _Version = Field(
        default='0.0.1', description='Semantic version for a specification'
    )
    Status: StatusEnum = Field(
        default=StatusEnum.proposed, description='Lifecycle status for a specification'
    )
    Approvers: list[Approver] = Field(
        default=[Approver()], description='List of approvers for a specification'
    )

@dataclass
class SpecID():
    ID: int = Field(description='Unique, with respect to a specification type, ID for a specification')

@dataclass(config=ConfigDict(json_schema_serialization_defaults_required=True))
class SpecBase():
    Title: str = Field(
        default=None, description='Short title a specification'
    )
    Description: str = Field(
        default=None, description='Longer form description of a specification is attempting to address'
    )

@dataclass(config=ConfigDict(json_schema_serialization_defaults_required=True))
class Reference():
    Name: str = Field(
        default=None, description='Name or short title of a reference'
    )
    Link: str = Field(
        default=None, description='URL link for a reference'
    )
    Comment: str = Field(
        default=None,
        description='Comments or longer form description of how a reference related to a specification'
    )

@dataclass(config=ConfigDict(json_schema_serialization_defaults_required=True))
class ActionSpec(SpecBase, SpecID):
    ImplementationTypes: list[str] = Field(
        default=[None], description='List of how the specification is implemented'
    )
    References: list[Reference] = Field(
        default=[Reference()], description='List reference objects'
    )
    Notes: list[str] = Field(
        default=[None], description='List of notes related to a specific action'
    )

@dataclass
class Action():
    Metadata: MetadataSpec = Field(description='Metadata for an Action specification')
    Specification: ActionSpec = Field(description='An action specification')

@dataclass(config=ConfigDict(json_schema_serialization_defaults_required=True))
class CapabilityItem(SpecBase):
    Actions: list[SpecID] = Field(default=None, description='List of action IDs')

@dataclass
class CapabilitySpec(CapabilityItem, SpecBase, SpecID):
    pass

@dataclass
class Capability():
    Metadata: MetadataSpec = Field(description='Metadata for a capability specification')
    Specification: CapabilitySpec = Field(description='Capability specification')

@dataclass
class DomainItem(SpecBase):
    Capabilities: list[SpecID | CapabilityItem] = Field(
        description='List of capability IDs or capability items'
    )

@dataclass
class DomainSpec(DomainItem, SpecBase, SpecID):
    pass

@dataclass
class Domain():
    Metadata: MetadataSpec = Field(description='Metadata for a domain specification')
    Specification: DomainSpec = Field(description='A domain specification')

@dataclass
class ProfileSpec(SpecBase, SpecID):
    Domains: list[SpecID | DomainItem] = Field(description='List of domain IDs or domain items')

@dataclass
class Profile():
    Metadata: MetadataSpec = Field(description='Metadata for a profile specification')
    Specification: ProfileSpec = Field(description='A profile specification')