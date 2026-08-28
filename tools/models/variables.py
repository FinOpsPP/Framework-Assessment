"""Defines the TOML variables config file"""
from pydantic import BaseModel, ConfigDict, model_validator
from pydantic import Field

from finopspp.models.core import Config
from finopspp.models.specs import StatusEnum, SemanticVersion
from finopspp.models.actions import WeightValidator


class Basic(Config):
    """Model for the basic section of the variables config"""
    name: str | None = Field(
        description='Name or short title of a reference'
    )
    version: SemanticVersion | None = Field(
        description='Name or short title of a reference'
    )


class Profile(Config):
    """Model for the profile section of the variables config"""
    title: str | None = Field(
        description='Name or short title of a reference'
    )
    version: SemanticVersion | None = Field(
        description='Name or short title of a reference'
    )
    status: StatusEnum = Field(
        description='Lifecycle status for a specification'
    )


class Weights(BaseModel):
    """Model for the weights section of the variables config"""
    model_config = ConfigDict(extra='allow')

    @model_validator(mode='after')
    def validate_weights(self):
        """Validate the weight values"""
        new_extras = {}
        for domain, subextras_1 in self.model_extra.items():
            for capability, subextras_2 in subextras_1.items():
                for action, weight in subextras_2.items():
                    weight = WeightValidator.validate_python(weight, strict=True)
                    new_extras[f'{domain}.{capability}.{action}'] = weight

        self.__pydantic_extra__ = new_extras
        return self


class Variables(Config):
    """Model specification for the variables config"""
    basic: Basic
    profile: Profile
    weights: Weights
