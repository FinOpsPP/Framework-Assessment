"""Defines YAML model for overrides of other model fields"""
from typing import Optional

from pydantic import Field, field_validator

from finopspp.models.core import Config
from finopspp.models.specs import SpecID


class BaseOverride(Config):
    """Basic overrides model allowed for all specifications"""
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
    """Override model only allowed for action specification"""
    SlugUpdate: Optional[str] = Field(
        default=None, description='Update the slug for an action'
    )


class StdOverride(BaseOverride, Config):
    """Common (or standard) overrides model allowed for most specifications"""
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
    # DropIDs.
    # Method can be defined with any name
    @field_validator('AddIDs', 'DropIDs', mode='after')
    def setup_default(cls, value, values, **kwargs): # pylint: disable=no-self-argument,unused-argument
        if value:
            return value

        return []

OverrideMap = {
    'std': StdOverride,
    'action': ActionOverride
}
