# SkillLint Quick Start

SkillLint is an **offline-first** quality and security linter for AI skill content.

## 1) Install (editable/dev)

```bash
cd skill-lint
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## 2) Run your first scan

```bash
skilllint scan examples/insecure-skill.md --format text
```

Expected behavior:
- reports quality summary + security findings
- exits with code `2` if policy gates fail

## 3) Scan a directory with policy

```bash
skilllint scan . --policy src/skilllint/policies/default.yaml --format json
```

Exit code behavior:
- `0`: all gates passed
- `2`: quality/security gates failed

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

## 5) Intel subsystem (configurable, offline-safe defaults)

Security intel is configurable via policy, with strong defaults:
- `mode: bundled`
- `ai_assisted: false`
- `allow_remote: false`

Example:

```yaml
security:
  fail_on: [critical, high]
  intel:
    mode: bundled   # disabled | bundled | file
    file: examples/custom-signatures.yaml
    ai_assisted: false
    allow_remote: false
```

> Note: AI-assisted scanning and remote intel fetch are disabled by design in current releases.

## 6) CI usage

```bash
skilllint scan . --policy src/skilllint/policies/strict.yaml --format text
```

Recommended pipeline sequence:
1. run tests
2. run `ruff check`
3. run `skilllint scan` (policy-enforced)
