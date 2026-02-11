# SkillLint v2.0 Implementation Plan

## Project Goal
Transform SkillScan (security-focused scanner) into SkillLint (offline quality + security linter for AI skills).

## Strategic Decisions (Locked)

1. **Evolve existing codebase (not rewrite)**
   - Reuse ~60-70% from SkillScan (CLI, file handling, policy system, CI/CD patterns)
   - New package name: `skilllint`
   - New CLI command: `skilllint`

2. **Dual purpose model**
   - Primary (80%): quality linting during development
   - Secondary (20%): offline security scanning for third-party skills

3. **Keep security scanner core**
   - Keep: malware patterns, injection patterns, exfil patterns, supply chain checks, binary artifact checks, YAML policy controls
   - Remove/de-prioritize: AI-assisted scanning + enterprise intel feed management

4. **8 quality metrics (NLP-powered)**
   - Readability
   - Complexity
   - Structure
   - Consistency
   - Completeness
   - Maintainability
   - Precision
   - Security Integration

5. **Three-tier fix strategy**
   - Level 1: Safe auto-fixes
   - Level 2: Suggested/interactive fixes
   - Level 3: Guidance-only recommendations

---

## Proposed Architecture

```text
src/skilllint/
├── core/
│   ├── analyzer.py
│   ├── file_handler.py
│   └── result.py
├── analyzers/
│   ├── quality/
│   │   ├── readability.py
│   │   ├── complexity.py
│   │   ├── structure.py
│   │   ├── consistency.py
│   │   ├── completeness.py
│   │   ├── maintainability.py
│   │   ├── precision.py
│   │   └── security_integration.py
│   └── security/
│       ├── malware.py
│       ├── injection.py
│       ├── exfiltration.py
│       ├── supply_chain.py
│       └── binary_artifacts.py
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

---

## 3-Week Milestones

### Week 1 — Foundation + Parity
- [ ] Rename/import migration SkillScan -> SkillLint
- [ ] Stand up CLI entrypoint (`skilllint`)
- [ ] Port security analyzers
- [ ] Define unified result schema for quality + security findings
- [ ] Implement basic scan pipeline (single file + directory)

### Week 2 — Quality Metrics Engine
- [ ] Implement 8 quality metric analyzers (v1 scoring)
- [ ] Add aggregate quality score + per-metric scorecards
- [ ] Add policy thresholds and severity mapping
- [ ] Add markdown + JSON report output

### Week 3 — Fixes + DevEx + Launch Prep
- [ ] Implement Level 1 safe auto-fixes
- [ ] Implement interactive suggestions for Level 2
- [ ] Add guidance templates for Level 3
- [ ] Add tests + sample fixtures
- [ ] Prepare packaging (PyPI), docs, and launch checklist

---

## Initial Backlog (First Build Tasks)

1. Create `pyproject.toml` with console script:
   - `skilllint = skilllint.cli.main:app`
2. Create result schema dataclasses:
   - Finding, MetricScore, ScanSummary, ScanResult
3. Add scanner orchestrator:
   - load files -> run analyzers -> merge findings -> apply policy -> output
4. Add one quality analyzer end-to-end first (`readability.py`) + one security analyzer (`injection.py`)
5. Add `skilllint scan <path> --format json|markdown`

---

## Guardrails

- Offline-first by default
- Deterministic output where possible
- Explain findings with evidence and remediation
- Never auto-apply risky fixes silently

