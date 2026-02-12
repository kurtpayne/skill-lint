# SkillLint Quick Start

## Install (local editable)

```bash
cd skill-lint
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Scan a file

```bash
skilllint scan examples/insecure-skill.md --format markdown
```

## Scan a repo/directory with policy

```bash
skilllint scan . --policy src/skilllint/policies/default.yaml --format json
```

Exit code behavior:
- `0`: pass
- `2`: failed quality/security policy gates

## Apply safe auto-fixes

```bash
skilllint fix examples/insecure-skill.md --verbose
```

Safe fixes include:
- line ending normalization
- trailing whitespace cleanup
- terminal newline enforcement
- markdown heading spacing normalization
- `bash-tool` -> `bash_tool` normalization

## Recommended CI usage

```bash
skilllint scan . --policy src/skilllint/policies/strict.yaml --format text
```
