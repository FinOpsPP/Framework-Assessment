"""Defines the YAML models used to construct profiles"""
from pydantic import Field

from finopspp.models.core import Config
from finopspp.models.specs import MetadataSpec, SpecBase, SpecID
from finopspp.models.domains import DomainItem


class ProfileSpec(SpecBase, SpecID, Config):
    """Profile specification core model"""
    Domains: list[SpecID | DomainItem] = Field(description='List of domain IDs or domain items')


class Profile(Config):
    """Top-level Profile model"""
    Metadata: MetadataSpec = Field(description='Metadata for a profile specification')
    Specification: ProfileSpec = Field(description='A profile specification')
