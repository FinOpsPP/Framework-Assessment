"""Includes smart defaults for the different specification models"""
import datetime

from finopspp.models import definitions


Action = definitions.Action(
    Metadata=definitions.MetadataSpec(
        Proposed=datetime.date.today(),
        Adopted=None,
        Modified=None,
        Version='0.0.1',
        Status=definitions.StatusEnum.proposed.value,
        Approvers=[
            definitions.Approver(
                Name=None,
                Email=None,
                Date=None
            )
        ]
    ),
    Specification=definitions.ActionSpec(
        ID=None,
        Title=None,
        Description=None,
        Slug=None,
        ImplementationTypes=[
            None
        ],
        Weight=0,
        Formula=None,
        Scoring=[
            definitions.ScoringDetail(
                Score=0,
                Condition=None
            )
        ],
        References=[
            definitions.Reference(
                Name=None,
                Link=None,
                Comment=None
            )
        ],
        Notes=[
            None
        ]
    )
)


Capability = definitions.Capability(
    Metadata=definitions.MetadataSpec(
        Proposed=datetime.date.today(),
        Adopted=None,
        Modified=None,
        Version='0.0.1',
        Status=definitions.StatusEnum.proposed.value,
        Approvers=[
            definitions.Approver(
                Name=None,
                Email=None,
                Date=None
            )
        ]
    ),
    Specification=definitions.CapabilitySpec(
        ID=None,
        Title=None,
        Description=None,
        Actions=[
            definitions.SpecID(
                ID=None
            )
        ],
        Overrides=None
    )
)


Domain = definitions.Domain(
    Metadata=definitions.MetadataSpec(
        Proposed=datetime.date.today(),
        Adopted=None,
        Modified=None,
        Version='0.0.1',
        Status=definitions.StatusEnum.proposed.value,
        Approvers=[
            definitions.Approver(
                Name=None,
                Email=None,
                Date=None
            )
        ]
    ),
    Specification=definitions.DomainSpec(
        ID=None,
        Title=None,
        Description=None,
        Capabilities=[
            definitions.SpecID(
                ID=None
            )
        ],
        Overrides=None
    )
)


Profile = definitions.Profile(
    Metadata=definitions.MetadataSpec(
        Proposed=datetime.date.today(),
        Adopted=None,
        Modified=None,
        Version='0.0.1',
        Status=definitions.StatusEnum.proposed.value,
        Approvers=[
            definitions.Approver(
                Name=None,
                Email=None,
                Date=None
            )
        ]
    ),
    Specification=definitions.ProfileSpec(
        ID=None,
        Title=None,
        Description=None,
        Domains=[
            definitions.SpecID(
                ID=None
            ),
            definitions.DomainItem(
                Title=None,
                Description=None,
                Capabilities=[
                    definitions.SpecID(
                        ID=None
                    ),
                    definitions.CapabilityItem(
                        Title=None,
                        Description=None,
                        Actions=[
                            definitions.ActionItem(
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
