"""Includes smart defaults for the different specifications"""
import datetime

from finopspp import models


Action = models.Action(
    Metadata=models.MetadataSpec(
        Proposed=datetime.date.today(),
        Adopted=None,
        Modified=None,
        Version='0.0.1',
        Status=models.StatusEnum.proposed.value,
        Approvers=[
            models.Approver(
                Name=None,
                Email=None,
                Date=None
            )
        ]
    ),
    Specification=models.ActionSpec(
        ID=None,
        Title=None,
        Description=None,
        ImplementationTypes=[
            None
        ],
        Weight=0,
        Formula=None,
        Scoring=[
            models.ScoringDetail(
                Score=0,
                Condition=None
            )
        ],
        References=[
            models.Reference(
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


Capability = models.Capability(
    Metadata=models.MetadataSpec(
        Proposed=datetime.date.today(),
        Adopted=None,
        Modified=None,
        Version='0.0.1',
        Status=models.StatusEnum.proposed.value,
        Approvers=[
            models.Approver(
                Name=None,
                Email=None,
                Date=None
            )
        ]
    ),
    Specification=models.CapabilitySpec(
        ID=None,
        Title=None,
        Description=None,
        Actions=[
            models.SpecID(
                ID=None
            )
        ],
        Overrides=None
    )
)


Domain = models.Domain(
    Metadata=models.MetadataSpec(
        Proposed=datetime.date.today(),
        Adopted=None,
        Modified=None,
        Version='0.0.1',
        Status=models.StatusEnum.proposed.value,
        Approvers=[
            models.Approver(
                Name=None,
                Email=None,
                Date=None
            )
        ]
    ),
    Specification=models.DomainSpec(
        ID=None,
        Title=None,
        Description=None,
        Capabilities=[
            models.SpecID(
                ID=None
            )
        ],
        Overrides=None
    )
)


Profile = models.Profile(
    Metadata=models.MetadataSpec(
        Proposed=datetime.date.today(),
        Adopted=None,
        Modified=None,
        Version='0.0.1',
        Status=models.StatusEnum.proposed.value,
        Approvers=[
            models.Approver(
                Name=None,
                Email=None,
                Date=None
            )
        ]
    ),
    Specification=models.ProfileSpec(
        ID=None,
        Title=None,
        Description=None,
        Domains=[
            models.SpecID(
                ID=None
            ),
            models.DomainItem(
                Title=None,
                Description=None,
                Capabilities=[
                    models.SpecID(
                        ID=None
                    ),
                    models.CapabilityItem(
                        Title=None,
                        Description=None,
                        Actions=[
                            models.ActionItem(
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
