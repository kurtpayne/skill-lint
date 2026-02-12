# SkillLint Implementation Plan (Quality-Only Scope)

## Project Goal
Position SkillLint as a focused, offline quality assessment + linting tool for AI skills.

## Strategic Decisions (Locked)

1. **Quality-first product**
   - Focus exclusively on quality metrics and linting workflows
   - No security scanning subsystem in core scope

2. **Offline and deterministic**
   - No cloud/API dependency required for scoring
   - Deterministic scoring and policy results where possible

3. **Practical developer workflow**
   - Fast local scans during authoring
   - CI policy enforcement
   - Safe autofix for low-risk formatting and hygiene issues

## Core Metrics
- Readability
- Complexity
- Structure
- Consistency
- Completeness
- Maintainability
- Precision

## Architecture

```text
src/skilllint/
├── core/
│   ├── analyzer.py
│   ├── file_handler.py
│   ├── policy.py
│   └── result.py
├── analyzers/
│   └── quality/
│       ├── readability.py
│       ├── complexity.py
│       ├── structure.py
│       ├── consistency.py
│       ├── completeness.py
│       ├── maintainability.py
│       └── precision.py
├── fixes/
│   ├── safe_fixes.py
│   ├── suggested_fixes.py
│   └── guidance.py
├── policies/
│   ├── default.yaml
│   └── strict.yaml
└── cli/
    └── main.py
```

## Milestones

### Milestone 1 — Quality Foundation
- [x] Quality analyzers and aggregate scoring
- [x] Policy loader and quality thresholds
- [x] CLI scan output formats

### Milestone 2 — Lint/Fix Workflow
- [x] Safe autofix implementation
- [ ] Suggested/interactive fix flow improvements
- [ ] Guidance template expansion

### Milestone 3 — Developer Experience
- [x] Tests + CI
- [x] Quickstart + examples
- [ ] Editor integration roadmap

## Guardrails
- Offline-first by default
- Explain metric outcomes clearly
- Never auto-apply risky fixes silently
