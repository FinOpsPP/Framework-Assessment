"""Base model definition used for all FinOps++ models"""
from pydantic import BaseModel, ConfigDict


# For the configuration used here we ignore extra values that
# are passed to our models. That is to help the update CLI
# command remove fields that are no longer needed.
# But note that the validation CLI command will be validating
# with extra='forbid'. Causing extra fields to fail validation.
class Config(BaseModel):
    model_config = ConfigDict(
        json_schema_serialization_defaults_required=True,
        validate_assignment=True,
        validate_by_alias=True,
        validate_by_name=True,
        serialize_by_alias=True,
        extra='ignore'
    )
