# finopspp CLI Commands

> Source: `tools/__main__.py` | Install: `pip install -e ".[dev]"`

Invocation: `finopspp <command> <subcommand> [options]` or `python -m tools <command> ...`

---

## specifications validate

Validate YAML specs against Pydantic models with `extra='forbid'`.

```bash
finopspp specifications validate --specification-type=actions all
finopspp specifications validate --specification-type=actions 001
finopspp specifications validate --specification-type=capabilities all
finopspp specifications validate --specification-type=domains all
finopspp specifications validate --specification-type=profiles all
```

- `--specification-type`: `actions` | `capabilities` | `domains` | `profiles`
- `<id>`: 3-digit zero-padded ID or `all`
- Exits with code 1 if any spec fails

---

## specifications new

Create a new spec file from defaults (`tools/models/defaults.py`).

```bash
finopspp specifications new --specification-type=actions 137
finopspp specifications new --specification-type=capabilities 024
```

Creates `specifications/<type>/NNN.yaml` with template values. Edit afterward.

---

## specifications update

Update spec files to match current Pydantic model schema. Adds new fields, removes old ones, bumps version.

```bash
finopspp specifications update --specification-type=actions all
finopspp specifications update --specification-type=actions all --major
```

- `--major`: Bump major version instead of minor

---

## specifications show

Display a spec in the terminal with syntax highlighting (via Rich).

```bash
finopspp specifications show --specification-type=actions 001
finopspp specifications show --specification-type=actions 001 --metadata
```

---

## specifications list

List all specs by fully qualified ID per profile (`Domain.Capability.Action`).

```bash
finopspp specifications list --profile="FinOps Foundation"
finopspp specifications list --profile="FinOps++" --show-action-status
finopspp specifications list --profile="FinOps++" --status-by=Accepted
```

---

## specifications schema

Display the JSON/OpenAPI schema for a spec type.

```bash
finopspp specifications schema --specification-type=actions
```

---

## generate components

Generate markdown component files from YAML specs.

```bash
finopspp generate components --specification-type=actions
finopspp generate components --specification-type=capabilities
finopspp generate components --specification-type=domains
finopspp generate components --specification-type=profiles
```

Output: `components/<type>/NNN.md`

---

## generate assessment

Generate framework markdown and Excel assessment worksheet for a profile.

```bash
finopspp generate assessment --profile="FinOps Foundation"
finopspp generate assessment --profile="FinOps++"
```

Output: `assessments/<profile-title>/framework.md` + `assessment.xlsx`

---

## generate documents

Generate JSON Schema documentation for all spec types.

```bash
finopspp generate documents
```

Output: `specifications/README.md`

---

## version

Show tool version, Python version, and system info.

```bash
finopspp version
```

---

## Common Workflows

### Add a new action

```bash
finopspp specifications new --specification-type=actions 137
# Edit specifications/actions/137.yaml (Title, Description, Scoring, etc.)
finopspp specifications validate --specification-type=actions 137
# Add action ID to relevant capability: specifications/capabilities/NNN.yaml
finopspp specifications validate --specification-type=capabilities NNN
finopspp generate components --specification-type=actions
finopspp generate assessment --profile="FinOps Foundation"
```

### Fix a typo in generated markdown

1. Find the source spec in `specifications/` (not the `.md` file)
2. Edit the YAML
3. Validate: `finopspp specifications validate --specification-type=<type> NNN`
4. Regenerate: `finopspp generate components --specification-type=<type>`

### Validate everything

```bash
finopspp specifications validate --specification-type=actions all
finopspp specifications validate --specification-type=capabilities all
finopspp specifications validate --specification-type=domains all
finopspp specifications validate --specification-type=profiles all
```

### Full regeneration

```bash
finopspp generate components --specification-type=actions
finopspp generate components --specification-type=capabilities
finopspp generate components --specification-type=domains
finopspp generate components --specification-type=profiles
finopspp generate assessment --profile="FinOps Foundation"
finopspp generate assessment --profile="FinOps++"
```
