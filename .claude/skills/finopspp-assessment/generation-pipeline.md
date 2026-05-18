# Generation Pipeline

> Source: `tools/models/`, `tools/composers/`, `tools/templates/`

## Data Flow

```
YAML specs (specifications/)
       │
       ▼
Pydantic validation (tools/models/definitions.py)
       │
       ├──► Jinja2 templates (tools/templates/*.j2)
       │         │
       │         ▼
       │    Markdown components (components/)
       │    Framework docs (assessments/<profile>/framework.md)
       │
       └──► Excel composer (tools/composers/excel.py)
                  │
                  ▼
             Assessment worksheets (assessments/<profile>/assessment.xlsx)
```

---

## Key Source Files

| File | Purpose |
|---|---|
| `tools/__main__.py` | CLI entry point — all Click commands (~26KB) |
| `tools/models/definitions.py` | Pydantic models for all spec types (~10KB) |
| `tools/models/defaults.py` | Default values for `specifications new` (~3KB) |
| `tools/composers/markdown.py` | Markdown file writing via Jinja2 |
| `tools/composers/excel.py` | Excel workbook generation via xlsxwriter |
| `tools/composers/helpers.py` | `normalize()` — converts hierarchy to pandas DataFrame |

---

## Pydantic Model Hierarchy

```
Config (BaseModel with extra='ignore')
  ├─ Approver (Name, Email, Date)
  ├─ MetadataSpec (Proposed, Adopted, Modified, Version, Status, Approvers)
  ├─ SpecID (ID: int, gt=0, lt=1000)
  ├─ SpecBase (Title: max 100, Description: max 1000)
  ├─ ScoringDetail (Score: 0-10, Condition)
  ├─ Reference (Name, Link, Comment)
  ├─ ScoreTypeEnum (calculation|bucket|multi_bucket|percent|sequential|binary|threshold)
  ├─ BaseOverride (Profile, TitleUpdate, DescriptionUpdate)
  │   ├─ ActionOverride (+WeightUpdate: Optional[int])
  │   └─ StdOverride (+AddIDs, +DropIDs)
  ├─ ActionItem (SpecID + Overrides)
  ├─ ActionSpec (ActionItem + SpecBase + Slug, ImplementationTypes, Weight, Formula, ScoreType, Scoring, References, SupplementalGuidance)
  ├─ CapabilityItem (SpecBase + Actions list)
  ├─ CapabilitySpec (CapabilityItem + SpecBase + SpecID + Overrides)
  ├─ DomainItem (SpecBase + Capabilities list)
  ├─ DomainSpec (DomainItem + SpecBase + SpecID + Overrides)
  └─ ProfileSpec (SpecBase + SpecID + Domains list)
```

Top-level wrappers (what YAML files map to):
- `Action = { Metadata: MetadataSpec, Specification: ActionSpec }`
- `Capability = { Metadata: MetadataSpec, Specification: CapabilitySpec }`
- `Domain = { Metadata: MetadataSpec, Specification: DomainSpec }`
- `Profile = { Metadata: MetadataSpec, Specification: ProfileSpec }`

**Important**: Config uses `extra='ignore'` normally, but `validate` CLI command uses `extra='forbid'`.

---

## Jinja2 Templates

| Template | Generates | Output Location |
|---|---|---|
| `actions.md.j2` | Action component pages | `components/actions/NNN.md` |
| `capabilities.md.j2` | Capability component pages | `components/capabilities/NNN.md` |
| `domains.md.j2` | Domain component pages | `components/domains/NNN.md` |
| `profiles.md.j2` | Profile component pages | `components/profiles/NNN.md` |
| `framework.md.j2` | Assessment framework overview (nested HTML tables) | `assessments/<profile>/framework.md` |
| `schemas.md.j2` | JSON Schema documentation | `specifications/README.md` |

---

## Excel Composer

Generates `.xlsx` assessment workbooks with:
- **Overview sheet** — summary scores, domain/capability counts, pie chart
- **Maturity - Domains** — radar chart by domain
- **Maturity - Capabilities** — radar chart by capability
- **Scoring sheet** — main assessment data with dropdowns, formulas for weighted scores, hyperlinks

The `normalize()` helper in `composers/helpers.py` flattens the hierarchy into a pandas DataFrame for Excel generation.

---

## Key Internal Functions (in `__main__.py`)

- **`sub_specification_helper(spec, file_location)`** — resolves ID references to full specs by loading from YAML files
- **`overrides_helper(spec, profile, override_type)`** — applies profile-specific overrides (AddIDs/DropIDs/WeightUpdate)
- **`SpecSubspecMap`** — defines parent-child relationships: `profiles → domains → capabilities → actions`

---

## How to Add a New Field to a Spec Type

1. Add the field to the Pydantic model in `tools/models/definitions.py`
2. Add a default value in `tools/models/defaults.py`
3. Update the relevant Jinja2 template in `tools/templates/` if it should appear in output
4. Run `finopspp specifications update --specification-type=<type> all` to add the field to existing specs
5. Validate: `finopspp specifications validate --specification-type=<type> all`
6. Regenerate affected outputs

## How to Modify Generated Output Format

- **Markdown layout**: Edit the `.j2` template in `tools/templates/`
- **Excel layout**: Edit `tools/composers/excel.py`
- Then regenerate all affected outputs

---

## Development Setup

```bash
python -m venv .venv
source .venv/bin/activate          # or .venv\Scripts\activate on Windows
pip install -e ".[dev]"            # includes validation and linting deps
```

Python 3.13+ required. Dependencies: Click, Pydantic, PyYAML, Jinja2, xlsxwriter, pandas, semver, Rich.
