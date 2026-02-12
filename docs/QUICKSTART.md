# SkillLint Quick Start

SkillLint is an **offline-first quality linter** for AI skill content.

## 1) Install (editable/dev)

```bash
cd skill-lint
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## 2) Run your first scan

```bash
skilllint scan examples/clean-skill.md --format text
```

Expected behavior:
- reports quality summary
- exits with code `2` only when quality policy gates fail

## 3) Scan a directory with policy

```bash
skilllint scan . --policy src/skilllint/policies/default.yaml --format json
```

Exit code behavior:
- `0`: quality gates passed
- `2`: quality policy gates failed

## 4) Apply safe fixes (Level 1)

```bash
skilllint fix examples/insecure-skill.md --verbose
```

Safe fixes include:
- line ending normalization
- trailing whitespace cleanup
- terminal newline enforcement
- markdown heading spacing normalization
- `bash-tool` -> `bash_tool` normalization

## 5) CI usage

```bash
skilllint scan . --policy src/skilllint/policies/strict.yaml --format text
```

Recommended pipeline sequence:
1. run tests
2. run `ruff check`
3. run `skilllint scan` (quality policy enforced)
