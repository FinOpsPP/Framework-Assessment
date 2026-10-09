# Component Specification Schemas

This document includes the schemas for all the main specifications used by FinOps++. The schemas
are all produced via the [Pydantic JSON Schema](https://docs.pydantic.dev/latest/concepts/json_schema/) and follow both the [OpenAPI Specification](https://spec.openapis.org/oas/latest.html). Importantly,
the outputs are in [YAML format](https://yaml.org/). This choice was made in order to follow the usage of yaml in the specifications used by FinOps++. It also
matches exactly the output that comes from running the `finopspp specifications schema` command. These schemas are created As-Code under
[definitions](../tools/models/definitions.py). All component specifications are validated against these definitions, and new component specifications
can be created from them. Commands for these can be found in [CLI Tool](../tools/README.md#cli-tool) of the README.

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
      SlugUpdate:
        anyOf:
        - type: string
        - type: 'null'
        default: null
        description: Update the slug for an action
        title: Slugupdate
    required:
    - Profile
    - TitleUpdate
    - DescriptionUpdate
    - SlugUpdate
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
        - maxLength: 25
          type: string
        - type: 'null'
        description: Machine parsable and human readable(ish) super short key label for action
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
      Score Type:
        $ref: '#/$defs/ScoreTypeEnum'
        default: calculation
        description: Type of scoring used for action
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
      Supplemental Guidance:
        description: List of notes that provide additional insights for a specific action
        items:
          anyOf:
          - type: string
          - type: 'null'
        title: Supplemental Guidance
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
    - Score Type
    - Scoring
    - References
    - Supplemental Guidance
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
        description: Comments or longer form description of how a reference related to a specification
        title: Comment
    required:
    - Name
    - Link
    - Comment
    title: Reference
    type: object
  ScoreTypeEnum:
    description: Enumeration of options for valid score types for an Action
    enum:
    - calculation
    - bucket
    - multi_bucket
    - percent
    - sequential
    - binary
    - threshold
    title: ScoreTypeEnum
    type: string
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
      SlugUpdate:
        anyOf:
        - type: string
        - type: 'null'
        default: null
        description: Update the slug for an action
        title: Slugupdate
    required:
    - Profile
    - TitleUpdate
    - DescriptionUpdate
    - SlugUpdate
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
      SlugUpdate:
        anyOf:
        - type: string
        - type: 'null'
        default: null
        description: Update the slug for an action
        title: Slugupdate
    required:
    - Profile
    - TitleUpdate
    - DescriptionUpdate
    - SlugUpdate
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
    description: Special capability item model used for listing capabilities in other specifications
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
      SlugUpdate:
        anyOf:
        - type: string
        - type: 'null'
        default: null
        description: Update the slug for an action
        title: Slugupdate
    required:
    - Profile
    - TitleUpdate
    - DescriptionUpdate
    - SlugUpdate
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
    description: Special capability item model used for listing capabilities in other specifications
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
# Specifications

- [actions/000.yaml](/specifications/actions/000.yaml)
- [actions/001.yaml](/specifications/actions/001.yaml)
- [actions/002.yaml](/specifications/actions/002.yaml)
- [actions/003.yaml](/specifications/actions/003.yaml)
- [actions/004.yaml](/specifications/actions/004.yaml)
- [actions/005.yaml](/specifications/actions/005.yaml)
- [actions/006.yaml](/specifications/actions/006.yaml)
- [actions/007.yaml](/specifications/actions/007.yaml)
- [actions/008.yaml](/specifications/actions/008.yaml)
- [actions/009.yaml](/specifications/actions/009.yaml)
- [actions/010.yaml](/specifications/actions/010.yaml)
- [actions/011.yaml](/specifications/actions/011.yaml)
- [actions/012.yaml](/specifications/actions/012.yaml)
- [actions/013.yaml](/specifications/actions/013.yaml)
- [actions/014.yaml](/specifications/actions/014.yaml)
- [actions/015.yaml](/specifications/actions/015.yaml)
- [actions/016.yaml](/specifications/actions/016.yaml)
- [actions/017.yaml](/specifications/actions/017.yaml)
- [actions/018.yaml](/specifications/actions/018.yaml)
- [actions/019.yaml](/specifications/actions/019.yaml)
- [actions/020.yaml](/specifications/actions/020.yaml)
- [actions/021.yaml](/specifications/actions/021.yaml)
- [actions/022.yaml](/specifications/actions/022.yaml)
- [actions/023.yaml](/specifications/actions/023.yaml)
- [actions/024.yaml](/specifications/actions/024.yaml)
- [actions/025.yaml](/specifications/actions/025.yaml)
- [actions/026.yaml](/specifications/actions/026.yaml)
- [actions/027.yaml](/specifications/actions/027.yaml)
- [actions/028.yaml](/specifications/actions/028.yaml)
- [actions/029.yaml](/specifications/actions/029.yaml)
- [actions/030.yaml](/specifications/actions/030.yaml)
- [actions/031.yaml](/specifications/actions/031.yaml)
- [actions/032.yaml](/specifications/actions/032.yaml)
- [actions/033.yaml](/specifications/actions/033.yaml)
- [actions/034.yaml](/specifications/actions/034.yaml)
- [actions/035.yaml](/specifications/actions/035.yaml)
- [actions/036.yaml](/specifications/actions/036.yaml)
- [actions/037.yaml](/specifications/actions/037.yaml)
- [actions/038.yaml](/specifications/actions/038.yaml)
- [actions/039.yaml](/specifications/actions/039.yaml)
- [actions/040.yaml](/specifications/actions/040.yaml)
- [actions/041.yaml](/specifications/actions/041.yaml)
- [actions/042.yaml](/specifications/actions/042.yaml)
- [actions/043.yaml](/specifications/actions/043.yaml)
- [actions/044.yaml](/specifications/actions/044.yaml)
- [actions/045.yaml](/specifications/actions/045.yaml)
- [actions/046.yaml](/specifications/actions/046.yaml)
- [actions/047.yaml](/specifications/actions/047.yaml)
- [actions/048.yaml](/specifications/actions/048.yaml)
- [actions/049.yaml](/specifications/actions/049.yaml)
- [actions/050.yaml](/specifications/actions/050.yaml)
- [actions/051.yaml](/specifications/actions/051.yaml)
- [actions/052.yaml](/specifications/actions/052.yaml)
- [actions/053.yaml](/specifications/actions/053.yaml)
- [actions/054.yaml](/specifications/actions/054.yaml)
- [actions/055.yaml](/specifications/actions/055.yaml)
- [actions/056.yaml](/specifications/actions/056.yaml)
- [actions/057.yaml](/specifications/actions/057.yaml)
- [actions/058.yaml](/specifications/actions/058.yaml)
- [actions/059.yaml](/specifications/actions/059.yaml)
- [actions/060.yaml](/specifications/actions/060.yaml)
- [actions/061.yaml](/specifications/actions/061.yaml)
- [actions/062.yaml](/specifications/actions/062.yaml)
- [actions/063.yaml](/specifications/actions/063.yaml)
- [actions/064.yaml](/specifications/actions/064.yaml)
- [actions/065.yaml](/specifications/actions/065.yaml)
- [actions/066.yaml](/specifications/actions/066.yaml)
- [actions/067.yaml](/specifications/actions/067.yaml)
- [actions/068.yaml](/specifications/actions/068.yaml)
- [actions/069.yaml](/specifications/actions/069.yaml)
- [actions/070.yaml](/specifications/actions/070.yaml)
- [actions/071.yaml](/specifications/actions/071.yaml)
- [actions/072.yaml](/specifications/actions/072.yaml)
- [actions/073.yaml](/specifications/actions/073.yaml)
- [actions/074.yaml](/specifications/actions/074.yaml)
- [actions/075.yaml](/specifications/actions/075.yaml)
- [actions/076.yaml](/specifications/actions/076.yaml)
- [actions/077.yaml](/specifications/actions/077.yaml)
- [actions/078.yaml](/specifications/actions/078.yaml)
- [actions/079.yaml](/specifications/actions/079.yaml)
- [actions/080.yaml](/specifications/actions/080.yaml)
- [actions/081.yaml](/specifications/actions/081.yaml)
- [actions/082.yaml](/specifications/actions/082.yaml)
- [actions/083.yaml](/specifications/actions/083.yaml)
- [actions/084.yaml](/specifications/actions/084.yaml)
- [actions/085.yaml](/specifications/actions/085.yaml)
- [actions/086.yaml](/specifications/actions/086.yaml)
- [actions/087.yaml](/specifications/actions/087.yaml)
- [actions/088.yaml](/specifications/actions/088.yaml)
- [actions/089.yaml](/specifications/actions/089.yaml)
- [actions/090.yaml](/specifications/actions/090.yaml)
- [actions/091.yaml](/specifications/actions/091.yaml)
- [actions/092.yaml](/specifications/actions/092.yaml)
- [actions/093.yaml](/specifications/actions/093.yaml)
- [actions/094.yaml](/specifications/actions/094.yaml)
- [actions/095.yaml](/specifications/actions/095.yaml)
- [actions/096.yaml](/specifications/actions/096.yaml)
- [actions/097.yaml](/specifications/actions/097.yaml)
- [actions/098.yaml](/specifications/actions/098.yaml)
- [actions/099.yaml](/specifications/actions/099.yaml)
- [actions/100.yaml](/specifications/actions/100.yaml)
- [actions/101.yaml](/specifications/actions/101.yaml)
- [actions/102.yaml](/specifications/actions/102.yaml)
- [actions/103.yaml](/specifications/actions/103.yaml)
- [actions/104.yaml](/specifications/actions/104.yaml)
- [actions/105.yaml](/specifications/actions/105.yaml)
- [actions/106.yaml](/specifications/actions/106.yaml)
- [actions/107.yaml](/specifications/actions/107.yaml)
- [actions/108.yaml](/specifications/actions/108.yaml)
- [actions/109.yaml](/specifications/actions/109.yaml)
- [actions/110.yaml](/specifications/actions/110.yaml)
- [actions/111.yaml](/specifications/actions/111.yaml)
- [actions/112.yaml](/specifications/actions/112.yaml)
- [actions/113.yaml](/specifications/actions/113.yaml)
- [actions/114.yaml](/specifications/actions/114.yaml)
- [actions/115.yaml](/specifications/actions/115.yaml)
- [actions/116.yaml](/specifications/actions/116.yaml)
- [actions/117.yaml](/specifications/actions/117.yaml)
- [actions/118.yaml](/specifications/actions/118.yaml)
- [actions/119.yaml](/specifications/actions/119.yaml)
- [actions/120.yaml](/specifications/actions/120.yaml)
- [actions/121.yaml](/specifications/actions/121.yaml)
- [actions/122.yaml](/specifications/actions/122.yaml)
- [actions/123.yaml](/specifications/actions/123.yaml)
- [actions/124.yaml](/specifications/actions/124.yaml)
- [actions/125.yaml](/specifications/actions/125.yaml)
- [actions/126.yaml](/specifications/actions/126.yaml)
- [actions/127.yaml](/specifications/actions/127.yaml)
- [actions/128.yaml](/specifications/actions/128.yaml)
- [actions/129.yaml](/specifications/actions/129.yaml)
- [actions/130.yaml](/specifications/actions/130.yaml)
- [actions/131.yaml](/specifications/actions/131.yaml)
- [actions/132.yaml](/specifications/actions/132.yaml)
- [actions/133.yaml](/specifications/actions/133.yaml)
- [actions/134.yaml](/specifications/actions/134.yaml)
- [actions/135.yaml](/specifications/actions/135.yaml)
- [actions/136.yaml](/specifications/actions/136.yaml)
- [actions/137.yaml](/specifications/actions/137.yaml)
- [actions/138.yaml](/specifications/actions/138.yaml)
- [actions/139.yaml](/specifications/actions/139.yaml)
- [capabilities/000.yaml](/specifications/capabilities/000.yaml)
- [capabilities/001.yaml](/specifications/capabilities/001.yaml)
- [capabilities/002.yaml](/specifications/capabilities/002.yaml)
- [capabilities/003.yaml](/specifications/capabilities/003.yaml)
- [capabilities/004.yaml](/specifications/capabilities/004.yaml)
- [capabilities/005.yaml](/specifications/capabilities/005.yaml)
- [capabilities/006.yaml](/specifications/capabilities/006.yaml)
- [capabilities/007.yaml](/specifications/capabilities/007.yaml)
- [capabilities/008.yaml](/specifications/capabilities/008.yaml)
- [capabilities/009.yaml](/specifications/capabilities/009.yaml)
- [capabilities/010.yaml](/specifications/capabilities/010.yaml)
- [capabilities/011.yaml](/specifications/capabilities/011.yaml)
- [capabilities/012.yaml](/specifications/capabilities/012.yaml)
- [capabilities/013.yaml](/specifications/capabilities/013.yaml)
- [capabilities/014.yaml](/specifications/capabilities/014.yaml)
- [capabilities/015.yaml](/specifications/capabilities/015.yaml)
- [capabilities/016.yaml](/specifications/capabilities/016.yaml)
- [capabilities/017.yaml](/specifications/capabilities/017.yaml)
- [capabilities/018.yaml](/specifications/capabilities/018.yaml)
- [capabilities/019.yaml](/specifications/capabilities/019.yaml)
- [capabilities/020.yaml](/specifications/capabilities/020.yaml)
- [capabilities/021.yaml](/specifications/capabilities/021.yaml)
- [capabilities/022.yaml](/specifications/capabilities/022.yaml)
- [capabilities/023.yaml](/specifications/capabilities/023.yaml)
- [domains/000.yaml](/specifications/domains/000.yaml)
- [domains/001.yaml](/specifications/domains/001.yaml)
- [domains/002.yaml](/specifications/domains/002.yaml)
- [domains/003.yaml](/specifications/domains/003.yaml)
- [domains/004.yaml](/specifications/domains/004.yaml)
- [profiles/000.yaml](/specifications/profiles/000.yaml)
- [profiles/001.yaml](/specifications/profiles/001.yaml)
- [profiles/002.yaml](/specifications/profiles/002.yaml)
- [variables/example.fppvars.toml](/specifications/variables/example.fppvars.toml)
