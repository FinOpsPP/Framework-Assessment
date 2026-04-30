# YAML Specification Schemas & Override System

> Source: `tools/models/definitions.py`, `specifications/`

All spec files have two top-level sections: `Metadata` and `Specification`.

---

## Metadata Block (all spec types)

```yaml
Metadata:
  Proposed: 'YYYY-MM-DD'       # ISO 8601, required
  Adopted: null                 # null until accepted
  Modified: null                # null or ISO 8601
  Version: 0.0.1               # semver string
  Status: Proposed              # Proposed | Accepted | Deprecated
  Approvers:
  - Name: null
    Email: null
    Date: null
```

---

## Action Spec

```yaml
Specification:
  ID: <int 1-999>
  Title: <string max 100>
  Description: <string max 1000>
  Slug: <string max 25>              # e.g. "1-inventory-sources"
  Implementation Types:               # YAML alias — field name is ImplementationTypes
  - <string or null>
  Weight: <float >= 0>               # priority/risk weight
  Formula: null                       # or multiline string using |-
  Score Type: <ScoreTypeEnum>         # YAML alias — field name is ScoreType
                                      # Values: binary | bucket | multi_bucket | percent |
                                      #         sequential | threshold | calculation (default)
  Scoring:                            # min 1, max 11 entries
  - Score: <int 0-10>
    Condition: <string or null>
  References:
  - Name: <string or null>
    Link: <URL or null>
    Comment: <string or null>
  Supplemental Guidance:              # YAML alias — field name is SupplementalGuidance
  - <string or null>
  Overrides: null                     # or list of ActionOverride (see below)
```

---

## Capability Spec

```yaml
Specification:
  ID: <int 1-999>
  Title: <string max 100>
  Description: <string max 1000 or null>
  Actions:
  - ID: <int>                         # references action spec by ID
  Overrides: null                     # or list of StdOverride
```

---

## Domain Spec

```yaml
Specification:
  ID: <int 1-999>
  Title: <string max 100>
  Description: <string max 1000 or null>
  Capabilities:
  - ID: <int>                         # references capability spec by ID
  Overrides: null                     # or list of StdOverride
```

Capabilities can also be defined inline with `Title`, `Description`, and `Actions` fields.

---

## Profile Spec

```yaml
Specification:
  ID: <int 1-999>
  Title: <string max 100>
  Description: <string max 1000 or null>
  Domains:
  - ID: <int>                         # reference existing domain by ID
```

Domains can be defined inline with `Title`, `Description`, and `Capabilities` (which themselves can inline `Actions`). See `specifications/profiles/002.yaml` for an example.

---

## Override System

Overrides live on the **base spec** (not on the profile). They are keyed by profile title or ID.

### ActionOverride (actions only)

```yaml
Overrides:
- Profile: "FinOps++"               # or {ID: 2}
  TitleUpdate: null
  DescriptionUpdate: null
  WeightUpdate: null                 # Optional[int] — change weight for this profile
```

### StdOverride (capabilities and domains)

```yaml
Overrides:
- Profile: "FinOps++"
  TitleUpdate: null
  DescriptionUpdate: null
  AddIDs: []                         # add sub-spec IDs for this profile
  DropIDs:                           # drop sub-spec IDs for this profile
  - ID: <int>
```

### How Overrides Work

- `DropIDs` removes a sub-item for that profile only (e.g., drop a capability from a domain)
- `AddIDs` adds a sub-item for that profile only
- A domain can drop a capability for FinOps++ while keeping it for FinOps Foundation
- Overrides are applied during assessment generation via `overrides_helper()`

---

## Validation Rules

| Rule | Constraint |
|---|---|
| Extra fields | Forbidden during `validate` (`extra='forbid'`), ignored during normal loading |
| ID | Integer > 0 and < 1000 |
| Score | Integer 0–10 inclusive |
| Scoring list | 1–11 entries |
| Title | Max 100 characters |
| Description | Max 1000 characters |
| Version | Valid semver (e.g., `1.0.0`) |
| Status | One of: `Proposed`, `Accepted`, `Deprecated` |
| Score Type | One of: `binary`, `bucket`, `multi_bucket`, `percent`, `sequential`, `threshold`, `calculation` |

---

## YAML Style

- **2-space indentation** (not 4) per YAML v1.2.2
- Multiline strings use `|` block scalar
- Dates quoted: `'YYYY-MM-DD'`
- Use `null` for empty values (not empty string)
- Overrides block always appears last in the Specification section
