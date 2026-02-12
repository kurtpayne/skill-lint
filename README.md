# SkillLint

[![CI](https://github.com/kurtpayne/skill-lint/actions/workflows/ci.yml/badge.svg)](https://github.com/kurtpayne/skill-lint/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

**Offline quality + security linter for AI skills**

SkillLint is the only offline tool that checks **both quality AND security** for AI skills. No API keys, no cloud dependencies—just fast, local analysis.

## Features

### 🔍 Quality Metrics (8 Core)
- **Readability** - Flesch-Kincaid + documentation coverage
- **Complexity** - Decision paths & cognitive load
- **Structure** - Organization & logical flow
- **Consistency** - Uniform terminology & style
- **Completeness** - Required sections present
- **Maintainability** - Ease of modification
- **Precision** - Clarity of instructions
- **Security Integration** - Security best practices

### 🛡️ Security Scanning
- Prompt injection patterns
- Malware-like execution patterns
- Data exfiltration indicators
- Secret exposure indicators
- Supply chain issues (unpinned/floating dependencies)
- Binary artifact detection
- Configurable offline intel signatures (bundled or local file)

### ✨ Auto-Fix
- **Level 1 (Safe)**: Auto-applied fixes
  - Whitespace normalization
  - Markdown syntax fixes
  - Tool name standardization
- **Level 2 (Interactive)**: Suggested refactors
- **Level 3 (Guidance)**: Manual recommendations

### 📊 Policy Enforcement
- YAML-based policies (`default`, `strict`, custom)
- Quality thresholds per metric
- Security severity gates
- CI-friendly exit codes

## Quick Start

### Install

```bash
pip install skilllint
```

Or for development:

```bash
git clone https://github.com/kurtpayne/skill-lint
cd skill-lint
pip install -e .
```

### Basic Usage

Scan a file:
```bash
skilllint scan my-skill.md
```

Scan with policy enforcement:
```bash
skilllint scan . --policy src/skilllint/policies/strict.yaml
```

Apply safe auto-fixes:
```bash
skilllint fix my-skill.md --verbose
```

Generate detailed report:
```bash
skilllint scan . --format markdown -o report.md
```

### Exit Codes
- `0`: All checks passed
- `2`: Quality or security policy gates failed

## Example Output

```bash
$ skilllint scan examples/insecure-skill.md --format text
SkillLint: scanned 1 files, findings=3, quality=45.2 | quality_failures=2
```

JSON output:
```bash
$ skilllint scan examples/ --format json
{
  "tool": "skilllint",
  "target": "examples/",
  "summary": {
    "files_scanned": 2,
    "findings_total": 3,
    "by_severity": {
      "critical": 1,
      "high": 1,
      "medium": 1
    },
    "quality_overall": 62.5
  },
  "metrics": [...],
  "findings": [...]
}
```

## Use Cases

### Development (Primary)
Run on every save/commit to catch quality issues early:
```bash
skilllint scan . --format text
```

### Security Review (Secondary)
Scan external/marketplace skills before use:
```bash
skilllint scan third-party-skill/ --policy strict.yaml
```

### CI/CD Integration
```yaml
- name: Lint AI skills
  run: skilllint scan skills/ --policy .skilllint-policy.yaml
```

## Documentation

- [Quick Start Guide](docs/QUICKSTART.md)
- [Examples](docs/EXAMPLES.md)
- [PRD Traceability Matrix](docs/PRD_TRACEABILITY.md)
- [Implementation Plan](IMPLEMENTATION_PLAN.md)

## Architecture

```
src/skilllint/
├── analyzers/
│   ├── quality/      # 8 quality metric analyzers
│   └── security/     # 5 security pattern scanners
├── core/
│   ├── analyzer.py   # Orchestration engine
│   ├── policy.py     # Policy enforcement
│   └── result.py     # Unified result schema
├── fixes/            # Auto-fix engine (3 levels)
└── cli/              # Command-line interface
```

## Development

Run tests:
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ --cov=src/skilllint --cov-report=html
```

Dogfood (scan self):
```bash
skilllint scan . --policy src/skilllint/policies/default.yaml
```

## Roadmap

- [x] Core quality + security analyzers
- [x] Policy enforcement engine
- [x] Safe auto-fix (Level 1)
- [x] CI/CD workflows
- [x] Test coverage >80%
- [ ] VSCode extension
- [ ] Interactive fix mode (Level 2)
- [ ] AI-assisted scoring (optional)
- [ ] Plugin API

## Contributing

PRs welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Unique Value Proposition

**SkillLint is the only offline tool that targets both quality AND security for AI skills.**

Unlike cloud-based tools (requires API keys, usage fees, privacy concerns) or pure security scanners (miss quality issues), SkillLint runs 100% locally and checks everything that matters.

Perfect for:
- Daily development workflows
- CI/CD pipelines
- Security audits of third-party skills
- Open source skill repositories

---

Built by [Kurt Payne](https://github.com/kurtpayne) | [Report Issues](https://github.com/kurtpayne/skill-lint/issues)
