# FinOpsPP Assessment Repository

> Source: [github.com/FinOpsPP/Framework-Assessment](https://github.com/FinOpsPP/Framework-Assessment)

## Trigger Conditions

Activate this skill when the user asks about:
- Repository structure, architecture, or how the codebase works
- Writing, editing, or validating YAML specifications
- Using the `finopspp` CLI tool (commands, flags, errors)
- Scoring methods, weights, or formulas for actions
- Generating markdown components, framework docs, or Excel assessments
- The override system (profile-specific customizations)
- Profiles (000 Template, 001 FinOps Foundation, 002 FinOps++)
- Data models (Pydantic), Jinja2 templates, or composers
- Code quality (linting, validation)
- Contributing workflow or development setup

## Architecture Overview

NIST CSF-inspired assessment using an As-Code approach. YAML specifications are the single source of truth.

| Directory | Purpose | Editable? |
|---|---|---|
| `specifications/` | YAML specs (actions, capabilities, domains, profiles) | **YES** — source of truth |
| `components/` | Auto-generated markdown per spec (via Jinja2) | NO — regenerated |
| `assessments/` | Generated framework.md + assessment.xlsx per profile | NO — regenerated |
| `tools/` | `finopspp` Python CLI (Click + Pydantic + Jinja2 + xlsxwriter) | YES — for tool changes |
| `guidelines/` | Development, style, scoring, design guidance | YES — documentation |

## Hierarchy (mirrors NIST CSF)

```
Profile  →  Domain  →  Capability  →  Action
(NIST:  Function  →  Category  →  Sub-category)
```

## Specification Counts

| Type | Count | ID Range | File Location |
|---|---|---|---|
| Actions | 136 | 001–136 | `specifications/actions/NNN.yaml` |
| Capabilities | 23 | 000–022 | `specifications/capabilities/NNN.yaml` |
| Domains | 5 | 000–004 | `specifications/domains/NNN.yaml` |
| Profiles | 3 | 000–002 | `specifications/profiles/NNN.yaml` |

IDs are zero-padded to 3 digits in filenames. ID 0 files are templates.

## What to Edit for Common Tasks

| Task | Edit | Then Run |
|---|---|---|
| Add a new action | `finopspp specifications new --specification-type=actions <id>`, then edit the YAML | `finopspp specifications validate` |
| Fix text in component markdown | The YAML spec in `specifications/`, not the `.md` | `finopspp generate components --specification-type=<type>` |
| Change scoring for an action | `specifications/actions/NNN.yaml` Scoring section | `finopspp specifications validate --specification-type=actions NNN` |
| Add action to a capability | `specifications/capabilities/NNN.yaml` Actions list | Validate, then generate |
| Customize for a profile | Add Override block in the domain/capability/action YAML | Validate |
| Change Excel layout | `tools/composers/excel.py` | `finopspp generate assessment --profile="<name>"` |
| Change markdown format | `tools/templates/*.j2` | `finopspp generate components --specification-type=<type>` |
| Add a field to a spec type | `tools/models/definitions.py` + `defaults.py` + template | `finopspp specifications update`, then regenerate |

## Code Quality

| Tool | Target | Command |
|---|---|---|
| pylint | Python (PEP 8, 120-char lines) | `pylint tools/` |
| yamllint | YAML (v1.2.2, 2-space indent) | `yamllint specifications/` |
| pymarkdownlnt | Markdown (CommonMark, 120-char) | `pymarkdownlnt scan components/` |
| cspell | Spelling (optional locally) | `cspell` |

Python 3.13+ required. Install: `pip install -e ".[dev]"`

## Progressive Disclosure

Read additional files for deeper detail:

- **YAML spec schemas and overrides** → Read `yaml-specifications.md`
- **CLI commands and workflows** → Read `cli-commands.md`
- **Scoring system and profiles** → Read `scoring-and-profiles.md`
- **Generation pipeline (models, templates, composers)** → Read `generation-pipeline.md`
