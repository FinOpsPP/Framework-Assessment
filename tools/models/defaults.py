"""Includes smart defaults for the different specification models"""
import datetime

from finopspp.models.specs import MetadataSpec, StatusEnum, Approver, SpecID
from finopspp.models import actions, capabilities, domains, profiles


Action = actions.Action(
    Metadata=MetadataSpec(
        Proposed=datetime.date.today(),
        Adopted=None,
        Modified=None,
        Version='0.0.1',
        Status=StatusEnum.proposed.value,
        Approvers=[
            Approver(
                Name=None,
                Email=None,
                Date=None
            )
        ]
    ),
    Specification=actions.ActionSpec(
        ID=None,
        Title=None,
        Description=None,
        Slug=None,
        ImplementationTypes=[
            None
        ],
        Weight=0,
        Formula=None,
        ScoreType=actions.ScoreTypeEnum.calculation.value,
        Scoring=[
            actions.ScoringDetail(
                Score=0,
                Condition=None
            )
        ],
        References=[
            actions.ScoreTypeRefMap[actions.ScoreTypeEnum.calculation.value]
        ],
        SupplementalGuidance=[
            None
        ]
    )
)


Capability = capabilities.Capability(
    Metadata=MetadataSpec(
        Proposed=datetime.date.today(),
        Adopted=None,
        Modified=None,
        Version='0.0.1',
        Status=StatusEnum.proposed.value,
        Approvers=[
            Approver(
                Name=None,
                Email=None,
                Date=None
            )
        ]
    ),
    Specification=capabilities.CapabilitySpec(
        ID=None,
        Title=None,
        Description=None,
        Actions=[
            SpecID(
                ID=None
            )
        ],
        Overrides=None
    )
)


Domain = domains.Domain(
    Metadata=MetadataSpec(
        Proposed=datetime.date.today(),
        Adopted=None,
        Modified=None,
        Version='0.0.1',
        Status=StatusEnum.proposed.value,
        Approvers=[
            Approver(
                Name=None,
                Email=None,
                Date=None
            )
        ]
    ),
    Specification=domains.DomainSpec(
        ID=None,
        Title=None,
        Description=None,
        Capabilities=[
            SpecID(
                ID=None
            )
        ],
        Overrides=None
    )
)


Profile = profiles.Profile(
    Metadata=MetadataSpec(
        Proposed=datetime.date.today(),
        Adopted=None,
        Modified=None,
        Version='0.0.1',
        Status=StatusEnum.proposed.value,
        Approvers=[
            Approver(
                Name=None,
                Email=None,
                Date=None
            )
        ]
    ),
    Specification=profiles.ProfileSpec(
        ID=None,
        Title=None,
        Description=None,
        Domains=[
            SpecID(
                ID=None
            ),
            domains.DomainItem(
                Title=None,
                Description=None,
                Capabilities=[
                    SpecID(
                        ID=None
                    ),
                    capabilities.CapabilityItem(
                        Title=None,
                        Description=None,
                        Actions=[
                            actions.ActionItem(
                                ID=None,
                                Overrides=None
                            )
                        ]
                    )
                ]
            )
        ]
    )
)
