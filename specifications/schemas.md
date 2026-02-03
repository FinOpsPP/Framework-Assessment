# Component Specifications

This document includes the schemas for all the main specifications used by FinOps++. The schemas
are all produced via the [Pydantic JSON Schema](https://docs.pydantic.dev/latest/concepts/json_schema/) and follow both the [OpenAPI Specification](https://spec.openapis.org/oas/latest.html). Importantly,
the outputs are in [YAML format](https://yaml.org/). This choice was made in order to follow the use of YAML in the specifications used by FinOps++. It also
matches the format that is exported by the `finopspp specifications schemas` command.

## Action

Base component used by FinOps++. Can be composed into groups of Capabilities. Example: [Action - 000.yaml](./actions/000.yaml)

```yaml
$defs:
  ActionOverride:
    description: Override model only allowed for action specification
    properties:
      Profile:
        anyOf:
        - type: string
        - $ref: '#/$defs/SpecID'
        description: Title or ID of profile that override is tied to.
        title: Profile
      TitleUpdate:
        anyOf:
        - type: string
        - type: 'null'
        default: null
        description: Update the title of a specification
        title: Titleupdate
      DescriptionUpdate:
        anyOf:
        - type: string
        - type: 'null'
        default: null
        description: Update the description of a specification
        title: Descriptionupdate
      WeightUpdate:
        anyOf:
        - type: integer
        - type: 'null'
        default: null
        description: Update the weight for an action
        title: Weightupdate
    required:
    - Profile
    - TitleUpdate
    - DescriptionUpdate
    - WeightUpdate
    title: ActionOverride
    type: object
  ActionSpec:
    description: Action specification core model
    properties:
      ID:
        anyOf:
        - exclusiveMaximum: 1000
          exclusiveMinimum: 0
          type: integer
        - type: 'null'
        description: Unique, with respect to a specification type, ID for a specification
        title: Id
      Title:
        anyOf:
        - maxLength: 100
          type: string
        - type: 'null'
        description: Short title of a specification
        title: Title
      Description:
        anyOf:
        - maxLength: 1000
          type: string
        - type: 'null'
        description: Longer form description of a specification is attempting to address
        title: Description
      Overrides:
        anyOf:
        - items:
            $ref: '#/$defs/ActionOverride'
          type: array
        - type: 'null'
        default: []
        description: List of action overrides by profile
        title: Overrides
      Slug:
        anyOf:
        - maxLength: 20
          type: string
        - type: 'null'
        description: Machine parsable and human readable(ish) super short key label
          for action
        title: Slug
      Implementation Types:
        description: List of how the specification is implemented
        items:
          anyOf:
          - type: string
          - type: 'null'
        title: Implementation Types
        type: array
      Weight:
        description: Priority or risk related weight for a score
        minimum: 0
        title: Weight
        type: number
      Formula:
        anyOf:
        - type: string
        - type: 'null'
        default: null
        description: Formula used to compute the score condition
        title: Formula
      Scoring:
        description: Scoring details used to determine the maturity of an action
        items:
          $ref: '#/$defs/ScoringDetail'
        maxItems: 11
        minItems: 1
        title: Scoring
        type: array
      References:
        description: List of reference objects
        items:
          $ref: '#/$defs/Reference'
        title: References
        type: array
      Notes:
        description: List of notes related to a specific action
        items:
          anyOf:
          - type: string
          - type: 'null'
        title: Notes
        type: array
    required:
    - ID
    - Title
    - Description
    - Overrides
    - Slug
    - Implementation Types
    - Weight
    - Formula
    - Scoring
    - References
    - Notes
    title: ActionSpec
    type: object
  Approver:
    properties:
      Name:
        anyOf:
        - type: string
        - type: 'null'
        description: Name of of the approver
        title: Name
      Email:
        anyOf:
        - type: string
        - type: 'null'
        description: Email address of the approver
        title: Email
      Date:
        anyOf:
        - format: date
          type: string
        - type: 'null'
        description: ISO 8601 date of approval from the approver
        title: Date
    required:
    - Name
    - Email
    - Date
    title: Approver
    type: object
  MetadataSpec:
    description: Metadata specification model
    properties:
      Proposed:
        description: ISO 8601 date a specification was proposal
        format: date
        title: Proposed
        type: string
      Adopted:
        anyOf:
        - format: date
          type: string
        - type: 'null'
        description: ISO 8601 date a specification was adapted
        title: Adopted
      Modified:
        anyOf:
        - format: date
          type: string
        - type: 'null'
        description: ISO 8601 date a specification was last modified
        title: Modified
      Version:
        description: Semantic version for a specification
        title: Version
        type: string
      Status:
        $ref: '#/$defs/StatusEnum'
        description: Lifecycle status for a specification
      Approvers:
        description: List of approvers for a specification
        items:
          $ref: '#/$defs/Approver'
        title: Approvers
        type: array
    required:
    - Proposed
    - Adopted
    - Modified
    - Version
    - Status
    - Approvers
    title: MetadataSpec
    type: object
  Reference:
    description: Common model for references used in Action models
    properties:
      Name:
        anyOf:
        - type: string
        - type: 'null'
        description: Name or short title of a reference
        title: Name
      Link:
        anyOf:
        - type: string
        - type: 'null'
        description: URL link for a reference
        title: Link
      Comment:
        anyOf:
        - type: string
        - type: 'null'
        description: Comments or longer form description of how a reference related
          to a specification
        title: Comment
    required:
    - Name
    - Link
    - Comment
    title: Reference
    type: object
  ScoringDetail:
    description: Scoring model using in Action models
    properties:
      Score:
        default: 0
        description: Score value associated with a condition
        maximum: 10
        minimum: 0
        title: Score
        type: integer
      Condition:
        anyOf:
        - type: string
        - type: 'null'
        description: Conditional required to meet score value
        title: Condition
    required:
    - Score
    - Condition
    title: ScoringDetail
    type: object
  SpecID:
    description: Specification ID model
    properties:
      ID:
        anyOf:
        - exclusiveMaximum: 1000
          exclusiveMinimum: 0
          type: integer
        - type: 'null'
        description: Unique, with respect to a specification type, ID for a specification
        title: Id
    required:
    - ID
    title: SpecID
    type: object
  StatusEnum:
    description: Enumeration of options for valid statuses of a specification
    enum:
    - Proposed
    - Accepted
    - Deprecated
    title: StatusEnum
    type: string
description: Top-level Action Component model
properties:
  Metadata:
    $ref: '#/$defs/MetadataSpec'
    description: Metadata for an Action specification
  Specification:
    $ref: '#/$defs/ActionSpec'
    description: An action specification
required:
- Metadata
- Specification
title: Action
type: object

```

## Capability

Component attempts to create a first-order logical grouping of Actions. Can be composed into groups of Domains.
Example: [Capability - 000.yaml](./capabilities/000.yaml)

```yaml
$defs:
  ActionItem:
    description: Special action item model used for listing actions in other specifications
    properties:
      ID:
        anyOf:
        - exclusiveMaximum: 1000
          exclusiveMinimum: 0
          type: integer
        - type: 'null'
        description: Unique, with respect to a specification type, ID for a specification
        title: Id
      Overrides:
        anyOf:
        - items:
            $ref: '#/$defs/ActionOverride'
          type: array
        - type: 'null'
        default: []
        description: List of action overrides by profile
        title: Overrides
    required:
    - ID
    - Overrides
    title: ActionItem
    type: object
  ActionOverride:
    description: Override model only allowed for action specification
    properties:
      Profile:
        anyOf:
        - type: string
        - $ref: '#/$defs/SpecID'
        description: Title or ID of profile that override is tied to.
        title: Profile
      TitleUpdate:
        anyOf:
        - type: string
        - type: 'null'
        default: null
        description: Update the title of a specification
        title: Titleupdate
      DescriptionUpdate:
        anyOf:
        - type: string
        - type: 'null'
        default: null
        description: Update the description of a specification
        title: Descriptionupdate
      WeightUpdate:
        anyOf:
        - type: integer
        - type: 'null'
        default: null
        description: Update the weight for an action
        title: Weightupdate
    required:
    - Profile
    - TitleUpdate
    - DescriptionUpdate
    - WeightUpdate
    title: ActionOverride
    type: object
  Approver:
    properties:
      Name:
        anyOf:
        - type: string
        - type: 'null'
        description: Name of of the approver
        title: Name
      Email:
        anyOf:
        - type: string
        - type: 'null'
        description: Email address of the approver
        title: Email
      Date:
        anyOf:
        - format: date
          type: string
        - type: 'null'
        description: ISO 8601 date of approval from the approver
        title: Date
    required:
    - Name
    - Email
    - Date
    title: Approver
    type: object
  CapabilitySpec:
    description: Capability specification core model
    properties:
      ID:
        anyOf:
        - exclusiveMaximum: 1000
          exclusiveMinimum: 0
          type: integer
        - type: 'null'
        description: Unique, with respect to a specification type, ID for a specification
        title: Id
      Title:
        anyOf:
        - maxLength: 100
          type: string
        - type: 'null'
        description: Short title of a specification
        title: Title
      Description:
        anyOf:
        - maxLength: 1000
          type: string
        - type: 'null'
        description: Longer form description of a specification is attempting to address
        title: Description
      Actions:
        anyOf:
        - items:
            anyOf:
            - $ref: '#/$defs/SpecID'
            - $ref: '#/$defs/ActionItem'
          type: array
        - type: 'null'
        description: List of action IDs
        title: Actions
      Overrides:
        anyOf:
        - items:
            $ref: '#/$defs/StdOverride'
          type: array
        - type: 'null'
        description: List of overrides by profile
        title: Overrides
    required:
    - ID
    - Title
    - Description
    - Actions
    - Overrides
    title: CapabilitySpec
    type: object
  MetadataSpec:
    description: Metadata specification model
    properties:
      Proposed:
        description: ISO 8601 date a specification was proposal
        format: date
        title: Proposed
        type: string
      Adopted:
        anyOf:
        - format: date
          type: string
        - type: 'null'
        description: ISO 8601 date a specification was adapted
        title: Adopted
      Modified:
        anyOf:
        - format: date
          type: string
        - type: 'null'
        description: ISO 8601 date a specification was last modified
        title: Modified
      Version:
        description: Semantic version for a specification
        title: Version
        type: string
      Status:
        $ref: '#/$defs/StatusEnum'
        description: Lifecycle status for a specification
      Approvers:
        description: List of approvers for a specification
        items:
          $ref: '#/$defs/Approver'
        title: Approvers
        type: array
    required:
    - Proposed
    - Adopted
    - Modified
    - Version
    - Status
    - Approvers
    title: MetadataSpec
    type: object
  SpecID:
    description: Specification ID model
    properties:
      ID:
        anyOf:
        - exclusiveMaximum: 1000
          exclusiveMinimum: 0
          type: integer
        - type: 'null'
        description: Unique, with respect to a specification type, ID for a specification
        title: Id
    required:
    - ID
    title: SpecID
    type: object
  StatusEnum:
    description: Enumeration of options for valid statuses of a specification
    enum:
    - Proposed
    - Accepted
    - Deprecated
    title: StatusEnum
    type: string
  StdOverride:
    description: Common (or standard) overrides model allowed for most specifications
    properties:
      Profile:
        anyOf:
        - type: string
        - $ref: '#/$defs/SpecID'
        description: Title or ID of profile that override is tied to.
        title: Profile
      TitleUpdate:
        anyOf:
        - type: string
        - type: 'null'
        default: null
        description: Update the title of a specification
        title: Titleupdate
      DescriptionUpdate:
        anyOf:
        - type: string
        - type: 'null'
        default: null
        description: Update the description of a specification
        title: Descriptionupdate
      AddIDs:
        anyOf:
        - items:
            $ref: '#/$defs/SpecID'
          type: array
        - type: 'null'
        default: []
        description: List of sub-specification IDs to add to a specification
        title: Addids
      DropIDs:
        anyOf:
        - items:
            $ref: '#/$defs/SpecID'
          type: array
        - type: 'null'
        default: []
        description: List of sub-specification IDs to drop from a specification
        title: Dropids
    required:
    - Profile
    - TitleUpdate
    - DescriptionUpdate
    - AddIDs
    - DropIDs
    title: StdOverride
    type: object
description: Top-level Capability Component model
properties:
  Metadata:
    $ref: '#/$defs/MetadataSpec'
    description: Metadata for a capability specification
  Specification:
    $ref: '#/$defs/CapabilitySpec'
    description: A capability specification
required:
- Metadata
- Specification
title: Capability
type: object

```

## Domain

Components attempts to create a second-order logical grouping of Actions, by categorizing Capabilities.
Can be composed into Profiles. Example: [Domain - 000.yaml](./domains/000.yaml)

```yaml
$defs:
  ActionItem:
    description: Special action item model used for listing actions in other specifications
    properties:
      ID:
        anyOf:
        - exclusiveMaximum: 1000
          exclusiveMinimum: 0
          type: integer
        - type: 'null'
        description: Unique, with respect to a specification type, ID for a specification
        title: Id
      Overrides:
        anyOf:
        - items:
            $ref: '#/$defs/ActionOverride'
          type: array
        - type: 'null'
        default: []
        description: List of action overrides by profile
        title: Overrides
    required:
    - ID
    - Overrides
    title: ActionItem
    type: object
  ActionOverride:
    description: Override model only allowed for action specification
    properties:
      Profile:
        anyOf:
        - type: string
        - $ref: '#/$defs/SpecID'
        description: Title or ID of profile that override is tied to.
        title: Profile
      TitleUpdate:
        anyOf:
        - type: string
        - type: 'null'
        default: null
        description: Update the title of a specification
        title: Titleupdate
      DescriptionUpdate:
        anyOf:
        - type: string
        - type: 'null'
        default: null
        description: Update the description of a specification
        title: Descriptionupdate
      WeightUpdate:
        anyOf:
        - type: integer
        - type: 'null'
        default: null
        description: Update the weight for an action
        title: Weightupdate
    required:
    - Profile
    - TitleUpdate
    - DescriptionUpdate
    - WeightUpdate
    title: ActionOverride
    type: object
  Approver:
    properties:
      Name:
        anyOf:
        - type: string
        - type: 'null'
        description: Name of of the approver
        title: Name
      Email:
        anyOf:
        - type: string
        - type: 'null'
        description: Email address of the approver
        title: Email
      Date:
        anyOf:
        - format: date
          type: string
        - type: 'null'
        description: ISO 8601 date of approval from the approver
        title: Date
    required:
    - Name
    - Email
    - Date
    title: Approver
    type: object
  CapabilityItem:
    description: Special capability item model used for listing capabilities in other
      specifications
    properties:
      Title:
        anyOf:
        - maxLength: 100
          type: string
        - type: 'null'
        description: Short title of a specification
        title: Title
      Description:
        anyOf:
        - maxLength: 1000
          type: string
        - type: 'null'
        description: Longer form description of a specification is attempting to address
        title: Description
      Actions:
        anyOf:
        - items:
            anyOf:
            - $ref: '#/$defs/SpecID'
            - $ref: '#/$defs/ActionItem'
          type: array
        - type: 'null'
        description: List of action IDs
        title: Actions
    required:
    - Title
    - Description
    - Actions
    title: CapabilityItem
    type: object
  DomainSpec:
    description: Domain specification core model
    properties:
      ID:
        anyOf:
        - exclusiveMaximum: 1000
          exclusiveMinimum: 0
          type: integer
        - type: 'null'
        description: Unique, with respect to a specification type, ID for a specification
        title: Id
      Title:
        anyOf:
        - maxLength: 100
          type: string
        - type: 'null'
        description: Short title of a specification
        title: Title
      Description:
        anyOf:
        - maxLength: 1000
          type: string
        - type: 'null'
        description: Longer form description of a specification is attempting to address
        title: Description
      Capabilities:
        description: List of capability IDs or capability items
        items:
          anyOf:
          - $ref: '#/$defs/SpecID'
          - $ref: '#/$defs/CapabilityItem'
        title: Capabilities
        type: array
      Overrides:
        anyOf:
        - items:
            $ref: '#/$defs/StdOverride'
          type: array
        - type: 'null'
        description: List of overrides by profile
        title: Overrides
    required:
    - ID
    - Title
    - Description
    - Capabilities
    - Overrides
    title: DomainSpec
    type: object
  MetadataSpec:
    description: Metadata specification model
    properties:
      Proposed:
        description: ISO 8601 date a specification was proposal
        format: date
        title: Proposed
        type: string
      Adopted:
        anyOf:
        - format: date
          type: string
        - type: 'null'
        description: ISO 8601 date a specification was adapted
        title: Adopted
      Modified:
        anyOf:
        - format: date
          type: string
        - type: 'null'
        description: ISO 8601 date a specification was last modified
        title: Modified
      Version:
        description: Semantic version for a specification
        title: Version
        type: string
      Status:
        $ref: '#/$defs/StatusEnum'
        description: Lifecycle status for a specification
      Approvers:
        description: List of approvers for a specification
        items:
          $ref: '#/$defs/Approver'
        title: Approvers
        type: array
    required:
    - Proposed
    - Adopted
    - Modified
    - Version
    - Status
    - Approvers
    title: MetadataSpec
    type: object
  SpecID:
    description: Specification ID model
    properties:
      ID:
        anyOf:
        - exclusiveMaximum: 1000
          exclusiveMinimum: 0
          type: integer
        - type: 'null'
        description: Unique, with respect to a specification type, ID for a specification
        title: Id
    required:
    - ID
    title: SpecID
    type: object
  StatusEnum:
    description: Enumeration of options for valid statuses of a specification
    enum:
    - Proposed
    - Accepted
    - Deprecated
    title: StatusEnum
    type: string
  StdOverride:
    description: Common (or standard) overrides model allowed for most specifications
    properties:
      Profile:
        anyOf:
        - type: string
        - $ref: '#/$defs/SpecID'
        description: Title or ID of profile that override is tied to.
        title: Profile
      TitleUpdate:
        anyOf:
        - type: string
        - type: 'null'
        default: null
        description: Update the title of a specification
        title: Titleupdate
      DescriptionUpdate:
        anyOf:
        - type: string
        - type: 'null'
        default: null
        description: Update the description of a specification
        title: Descriptionupdate
      AddIDs:
        anyOf:
        - items:
            $ref: '#/$defs/SpecID'
          type: array
        - type: 'null'
        default: []
        description: List of sub-specification IDs to add to a specification
        title: Addids
      DropIDs:
        anyOf:
        - items:
            $ref: '#/$defs/SpecID'
          type: array
        - type: 'null'
        default: []
        description: List of sub-specification IDs to drop from a specification
        title: Dropids
    required:
    - Profile
    - TitleUpdate
    - DescriptionUpdate
    - AddIDs
    - DropIDs
    title: StdOverride
    type: object
description: Top-level Domain Component model
properties:
  Metadata:
    $ref: '#/$defs/MetadataSpec'
    description: Metadata for a domain specification
  Specification:
    $ref: '#/$defs/DomainSpec'
    description: A domain specification
required:
- Metadata
- Specification
title: Domain
type: object

```

## Profile

The top-level logical grouping of Actions. While not really a component itself, a Profile defines a
complete "menu" of Actions grouped by Domains, and then Capabilities. These menus can then be scoped
down for specific use cases. Example: [Profile - 000.yaml](./profiles/000.yaml)

```yaml
$defs:
  ActionItem:
    description: Special action item model used for listing actions in other specifications
    properties:
      ID:
        anyOf:
        - exclusiveMaximum: 1000
          exclusiveMinimum: 0
          type: integer
        - type: 'null'
        description: Unique, with respect to a specification type, ID for a specification
        title: Id
      Overrides:
        anyOf:
        - items:
            $ref: '#/$defs/ActionOverride'
          type: array
        - type: 'null'
        default: []
        description: List of action overrides by profile
        title: Overrides
    required:
    - ID
    - Overrides
    title: ActionItem
    type: object
  ActionOverride:
    description: Override model only allowed for action specification
    properties:
      Profile:
        anyOf:
        - type: string
        - $ref: '#/$defs/SpecID'
        description: Title or ID of profile that override is tied to.
        title: Profile
      TitleUpdate:
        anyOf:
        - type: string
        - type: 'null'
        default: null
        description: Update the title of a specification
        title: Titleupdate
      DescriptionUpdate:
        anyOf:
        - type: string
        - type: 'null'
        default: null
        description: Update the description of a specification
        title: Descriptionupdate
      WeightUpdate:
        anyOf:
        - type: integer
        - type: 'null'
        default: null
        description: Update the weight for an action
        title: Weightupdate
    required:
    - Profile
    - TitleUpdate
    - DescriptionUpdate
    - WeightUpdate
    title: ActionOverride
    type: object
  Approver:
    properties:
      Name:
        anyOf:
        - type: string
        - type: 'null'
        description: Name of of the approver
        title: Name
      Email:
        anyOf:
        - type: string
        - type: 'null'
        description: Email address of the approver
        title: Email
      Date:
        anyOf:
        - format: date
          type: string
        - type: 'null'
        description: ISO 8601 date of approval from the approver
        title: Date
    required:
    - Name
    - Email
    - Date
    title: Approver
    type: object
  CapabilityItem:
    description: Special capability item model used for listing capabilities in other
      specifications
    properties:
      Title:
        anyOf:
        - maxLength: 100
          type: string
        - type: 'null'
        description: Short title of a specification
        title: Title
      Description:
        anyOf:
        - maxLength: 1000
          type: string
        - type: 'null'
        description: Longer form description of a specification is attempting to address
        title: Description
      Actions:
        anyOf:
        - items:
            anyOf:
            - $ref: '#/$defs/SpecID'
            - $ref: '#/$defs/ActionItem'
          type: array
        - type: 'null'
        description: List of action IDs
        title: Actions
    required:
    - Title
    - Description
    - Actions
    title: CapabilityItem
    type: object
  DomainItem:
    description: Special domain item model used for listing domains in other specifications
    properties:
      Title:
        anyOf:
        - maxLength: 100
          type: string
        - type: 'null'
        description: Short title of a specification
        title: Title
      Description:
        anyOf:
        - maxLength: 1000
          type: string
        - type: 'null'
        description: Longer form description of a specification is attempting to address
        title: Description
      Capabilities:
        description: List of capability IDs or capability items
        items:
          anyOf:
          - $ref: '#/$defs/SpecID'
          - $ref: '#/$defs/CapabilityItem'
        title: Capabilities
        type: array
    required:
    - Title
    - Description
    - Capabilities
    title: DomainItem
    type: object
  MetadataSpec:
    description: Metadata specification model
    properties:
      Proposed:
        description: ISO 8601 date a specification was proposal
        format: date
        title: Proposed
        type: string
      Adopted:
        anyOf:
        - format: date
          type: string
        - type: 'null'
        description: ISO 8601 date a specification was adapted
        title: Adopted
      Modified:
        anyOf:
        - format: date
          type: string
        - type: 'null'
        description: ISO 8601 date a specification was last modified
        title: Modified
      Version:
        description: Semantic version for a specification
        title: Version
        type: string
      Status:
        $ref: '#/$defs/StatusEnum'
        description: Lifecycle status for a specification
      Approvers:
        description: List of approvers for a specification
        items:
          $ref: '#/$defs/Approver'
        title: Approvers
        type: array
    required:
    - Proposed
    - Adopted
    - Modified
    - Version
    - Status
    - Approvers
    title: MetadataSpec
    type: object
  ProfileSpec:
    description: Profile specification core model
    properties:
      ID:
        anyOf:
        - exclusiveMaximum: 1000
          exclusiveMinimum: 0
          type: integer
        - type: 'null'
        description: Unique, with respect to a specification type, ID for a specification
        title: Id
      Title:
        anyOf:
        - maxLength: 100
          type: string
        - type: 'null'
        description: Short title of a specification
        title: Title
      Description:
        anyOf:
        - maxLength: 1000
          type: string
        - type: 'null'
        description: Longer form description of a specification is attempting to address
        title: Description
      Domains:
        description: List of domain IDs or domain items
        items:
          anyOf:
          - $ref: '#/$defs/SpecID'
          - $ref: '#/$defs/DomainItem'
        title: Domains
        type: array
    required:
    - ID
    - Title
    - Description
    - Domains
    title: ProfileSpec
    type: object
  SpecID:
    description: Specification ID model
    properties:
      ID:
        anyOf:
        - exclusiveMaximum: 1000
          exclusiveMinimum: 0
          type: integer
        - type: 'null'
        description: Unique, with respect to a specification type, ID for a specification
        title: Id
    required:
    - ID
    title: SpecID
    type: object
  StatusEnum:
    description: Enumeration of options for valid statuses of a specification
    enum:
    - Proposed
    - Accepted
    - Deprecated
    title: StatusEnum
    type: string
description: Top-level Profile model
properties:
  Metadata:
    $ref: '#/$defs/MetadataSpec'
    description: Metadata for a profile specification
  Specification:
    $ref: '#/$defs/ProfileSpec'
    description: A profile specification
required:
- Metadata
- Specification
title: Profile
type: object

```