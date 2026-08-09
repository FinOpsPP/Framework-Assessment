"""Defines the YAML models used by the capability component"""
from pydantic import Field

from finopspp.models.core import Config
from finopspp.models.specs import MetadataSpec, SpecBase, SpecID
from finopspp.models.overrides import StdOverride
from finopspp.models.actions import ActionItem


class CapabilityItem(SpecBase, Config):
    """Special capability item model used for listing capabilities in other specifications"""
    Actions: list[SpecID | ActionItem] | None = Field(description='List of action IDs')


class CapabilitySpec(CapabilityItem, SpecBase, SpecID, Config):
    """Capability specification core model"""
    Overrides: list[StdOverride] | None = Field(description='List of overrides by profile')


class Capability(Config):
    """Top-level Capability Component model"""
    Metadata: MetadataSpec = Field(description='Metadata for a capability specification')
    Specification: CapabilitySpec = Field(description='A capability specification')
