# SkillLint

[![CI](https://github.com/kurtpayne/skill-lint/actions/workflows/ci.yml/badge.svg)](https://github.com/kurtpayne/skill-lint/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

**Offline quality linter for AI skills**

SkillLint is an offline quality assessment and linting tool for AI skills. No API keys, no cloud dependencies—just fast, local analysis focused on writing quality.

## Features

### 🔍 Quality Metrics
- **Readability** - sentence/word complexity heuristics
- **Complexity** - decision-path and branching pressure
- **Structure** - organization and document flow
- **Consistency** - terminology/style consistency
- **Completeness** - required sections present
- **Maintainability** - ease of long-term updates
- **Precision** - clarity and specificity of instructions

### ✨ Auto-Fix
- **Level 1 (Safe)**: Auto-applied fixes
  - Whitespace normalization
  - Markdown syntax fixes
  - Tool name standardization
- **Level 2/3**: Suggested and guidance improvements (roadmap)

### 📊 Policy Enforcement
- YAML-based policies (`default`, `strict`, custom)
- Quality thresholds per metric
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
pip install -e .[dev]
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
- `0`: Quality gates passed
- `2`: Quality policy gates failed

## Documentation

- [Quick Start Guide](docs/QUICKSTART.md)
- [Examples](docs/EXAMPLES.md)
- [Implementation Plan](IMPLEMENTATION_PLAN.md)

## Architecture

```
src/skilllint/
├── analyzers/
│   └── quality/      # quality metric analyzers
├── core/
│   ├── analyzer.py   # orchestration engine
│   ├── policy.py     # quality policy enforcement
│   └── result.py     # unified result schema
├── fixes/            # auto-fix engine
└── cli/              # command-line interface
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

## License

MIT License - see [LICENSE](LICENSE) for details.
