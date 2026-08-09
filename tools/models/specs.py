"""Defines the upper level YAML model used by all specifications"""
import datetime
from enum import Enum

import semver
from pydantic import Field
from pydantic_core import core_schema

from finopspp.models.core import Config


# modified from:
# https://python-semver.readthedocs.io/en/latest/advanced/combine-pydantic-and-semver.html
class _Version: # pylint: disable=too-few-public-methods
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        def validate_from_str(value: str):
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
    def __get_pydantic_json_schema__(cls, _core_schema, handler):
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


# pylint: disable=invalid-name
class StatusEnum(str, Enum):
    """Enumeration of options for valid statuses of a specification"""
    proposed = 'Proposed'
    accepted = 'Accepted'
    deprecated = 'Deprecated'
# pylint: enable=invalid-name


class MetadataSpec(Config):
    """Metadata specification model"""
    Proposed: datetime.date = Field(
        description='ISO 8601 date a specification was proposal'
    )
    Adopted: datetime.date | None = Field(
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
    """Specification ID model"""
    ID: int | None = Field(
        description='Unique, with respect to a specification type, ID for a specification',
        gt=0,
        lt=1000
    )


class SpecBase(Config):
    """Base, common model for specifications"""
    Title: str | None = Field(
        description='Short title of a specification',
        max_length=100
    )
    Description: str | None = Field(
        description='Longer form description of a specification is attempting to address',
        max_length=1000
    )
