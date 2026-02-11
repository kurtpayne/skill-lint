# SkillLint

SkillLint is an offline quality + security linter for AI skills.

## Vision

- **Quality linting** for day-to-day development (primary)
- **Security scanning** for external/marketplace skills (secondary)
- **100% offline**: no API keys, no cloud dependency

## Core Value

The only offline tool targeting both:
1. Skill quality metrics (readability, complexity, structure, etc.)
2. Security pattern scanning (injection, malware patterns, exfil indicators)

## Planned CLI

```bash
skilllint scan path/to/skills/
skilllint lint path/to/skill.yaml
skilllint fix path/to/skill.yaml --safe
skilllint report results.json --format markdown
```

## Status

Scaffolded v2.0 pivot from SkillScan. See `IMPLEMENTATION_PLAN.md`.
