"""Defines the YAML models for the domain component"""
from pydantic import Field

from finopspp.models.core import Config
from finopspp.models.specs import MetadataSpec, SpecBase, SpecID
from finopspp.models.overrides import StdOverride
from finopspp.models.capabilities import CapabilityItem


class DomainItem(SpecBase, Config):
    """Special domain item model used for listing domains in other specifications"""
    Capabilities: list[SpecID | CapabilityItem] = Field(
        description='List of capability IDs or capability items'
    )


class DomainSpec(DomainItem, SpecBase, SpecID, Config):
    """Domain specification core model"""
    Overrides: list[StdOverride] | None = Field(description='List of overrides by profile')


class Domain(Config):
    """Top-level Domain Component model"""
    Metadata: MetadataSpec = Field(description='Metadata for a domain specification')
    Specification: DomainSpec = Field(description='A domain specification')
