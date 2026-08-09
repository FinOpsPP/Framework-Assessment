"""Defines the YAML models used by the action component"""
from enum import Enum
from typing import Optional

from pydantic import Field, model_serializer

from finopspp.models.core import Config
from finopspp.models.specs import MetadataSpec, SpecBase, SpecID
from finopspp.models.overrides import ActionOverride


class ActionItem(SpecID, Config):
    """Special action item model used for listing actions in other specifications"""
    Overrides: Optional[list[ActionOverride]] = Field(
        default=[],
        description='List of action overrides by profile'
    )


# pylint: disable=invalid-name
class ScoreTypeEnum(str, Enum):
    """Enumeration of options for valid score types for an Action"""
    calculation = 'calculation'
    bucket = 'bucket'
    multiBucket = 'multi_bucket'
    percent = 'percent'
    sequential = 'sequential'
    binary = 'binary'
    threshold = 'threshold'
# pylint: enable=invalid-name


class Reference(Config):
    """Common model for references used in Action models"""
    Name: str | None = Field(
        description='Name or short title of a reference'
    )
    Link: str | None = Field(
        description='URL link for a reference'
    )
    Comment: str | None = Field(
        description='Comments or longer form description of how a reference related to a specification'
    )

ScoreTypeRefMap = {
    ScoreTypeEnum.binary.value: Reference(
        Name='FinOps++ Score Type - Binary',
        Link='https://github.com/FinOpsPP/Framework-Assessment/blob/main/guidelines/scoring.md#binary',
        Comment='binary is a useful scoring to start of with, as it simple requires an action to be taken or not.'
    ),
    ScoreTypeEnum.bucket.value: Reference(
        Name='FinOps++ Score Type - Bucket',
        Link='https://github.com/FinOpsPP/Framework-Assessment/blob/main/guidelines/scoring.md#bucket-of-accomplishments', # pylint: disable=line-too-long
        Comment='an evolution of binary, with more steps to take toward maturity.'
    ),
    ScoreTypeEnum.calculation.value: Reference(
        Name='FinOps++ Score Type - Calculation',
        Link='https://github.com/FinOpsPP/Framework-Assessment/blob/main/guidelines/scoring.md#other-mathematical-formulae', # pylint: disable=line-too-long
        Comment='a generic "calculation" type used as the default score type when creating a new score.'
    ),
    ScoreTypeEnum.multiBucket.value: Reference(
        Name='FinOps++ Score Type - Multiple Weighted Bucket',
        Link='https://github.com/FinOpsPP/Framework-Assessment/blob/main/guidelines/scoring.md##multiple-weighted-buckets', # pylint: disable=line-too-long
        Comment='an even more granular version of bucket, where steps are weight by importance to an action.'
    ),
    ScoreTypeEnum.percent.value: Reference(
        Name='FinOps++ Score Type - Percentage Calculation',
        Link='https://github.com/FinOpsPP/Framework-Assessment/blob/main/guidelines/scoring.md#percentage-calculation',
        Comment='a kind of threshold type where the steps are specifically precentages leading to 100%.'
    ),
    ScoreTypeEnum.sequential.value: Reference(
        Name='FinOps++ Score Type - Sequential Process',
        Link='https://github.com/FinOpsPP/Framework-Assessment/blob/main/guidelines/scoring.md#sequential-process',
        Comment='can be used whenever the steps in an action need to be completed in a certain order.'
    ),
    ScoreTypeEnum.threshold.value: Reference(
        Name='FinOps++ Score Type - Threshold Process',
        Link='https://github.com/FinOpsPP/Framework-Assessment/blob/main/guidelines/scoring.md#threshold-process',
        Comment='an evolution of sequential, where steps below a given level are complete when that level is reached.'
    )
}


class ScoringDetail(Config):
    """Scoring model using in Action models"""
    Score: int = Field(
        default=0,
        description='Score value associated with a condition',
        ge=0,
        le=10
    )
    Condition: str | None = Field(
        description='Conditional required to meet score value'
    )


class ActionSpec(ActionItem, SpecBase, SpecID, Config):
    """Action specification core model"""
    Slug: str | None = Field(
        description='Machine parsable and human readable(ish) super short key label for action',
        max_length=25
    )
    ImplementationTypes: list[str | None] = Field(
        description='List of how the specification is implemented',
        alias='Implementation Types'
    )
    Weight: float = Field(
        description='Priority or risk related weight for a score',
        ge=0
    )
    Formula: Optional[str] = Field(
        default=None,
        description='Formula used to compute the score condition'
    )
    ScoreType: ScoreTypeEnum = Field(
        default=ScoreTypeEnum.calculation,
        description='Type of scoring used for action',
        alias='Score Type'
    )
    Scoring: list[ScoringDetail] = Field(
        description='Scoring details used to determine the maturity of an action',
        min_length=1, # must include at least one detail objects
        max_length=11 # max of 11 (i.e ints 0-10) detail objects
    )
    References: list[Reference] = Field(
        description='List of reference objects'
    )
    SupplementalGuidance: list[str | None] = Field(
        description='List of notes that provide additional insights for a specific action',
        alias='Supplemental Guidance'
    )

    # Custom function to help make sure the overrides
    # are always correctly ordered when serialized.
    # Method can be defined with any name
    @model_serializer(when_used='json')
    def serialize_json_model(self):
        """Serialization helper in a format that works with pydantic"""
        # NOTE: lookups on the model need to be the Alias and not
        # the Field name.
        model = self.model_dump()

        # ensure overrides are always at the end of the serialized output
        # if they exist, by removing it and then adding it back.
        if 'Overrides' in model:
            overrides = model['Overrides']
            del model['Overrides']
            model['Overrides'] = overrides

        # ensure that the model always includes a reference for the score
        # type. We add the reference if one doesn't exist. But we do not
        # remove other score type references that already exists. This
        # is because we figure that there are some situations where
        # and individual would want multiple score type references.
        # we leave this to the action author and PR reviews to determine.
        score_type = model.get('Score Type')
        references = model.get('References', [])
        score_reference = ScoreTypeRefMap[score_type].model_dump()
        if score_reference not in references:
            references.append(score_reference)

        # remove all references if they do not have a Name or URL
        for index, reference in enumerate(references):
            if reference['Name']:
                continue

            del references[index]

        # else just return the original model
        return model


class Action(Config):
    """Top-level Action Component model"""
    Metadata: MetadataSpec = Field(description='Metadata for an Action specification')
    Specification: ActionSpec = Field(description='An action specification')
