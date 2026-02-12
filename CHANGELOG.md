# Changelog

All notable changes to SkillLint will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-02-11

### Added
- Configurable security intel subsystem with strong offline defaults
- Bundled offline security signature pack (`signatures/security_signatures.yaml`)
- Support for policy-driven custom signature files (`security.intel.mode: file`)
- Expanded offline security coverage (secret exposure, floating VCS refs, encoded payload indicators)
- PRD traceability matrix documentation (`docs/PRD_TRACEABILITY.md`)
- Release workflow (`.github/workflows/release.yml`) with build + `twine check`
- Additional tests for intel config and analyzer integration

### Changed
- Security analyzers now support layered signatures (built-ins + optional intel signatures)
- CI workflow hardened with concurrency controls, timeouts, and dependency caching
- Quickstart and examples expanded with intel configuration and custom signature examples
- Package version alignment to `1.1.0`

### Security
- AI-assisted scanning remains disabled by design
- Remote intel fetching remains disabled by design

## [1.0.0] - 2026-02-11

### Added
- Initial release of SkillLint v1.0
- 8 core quality metrics (readability, complexity, structure, consistency, completeness, maintainability, precision, security_integration)
- 5 security analyzers (injection, malware, exfiltration, supply_chain, binary_artifacts)
- Policy enforcement engine with YAML support
- Safe auto-fix engine (Level 1: whitespace, markdown, tool names)
- CLI with `scan` and `fix` commands
- JSON, markdown, and text output formats
- CI/CD via GitHub Actions
- Ripgrep-based fast file discovery with fallback
- Exit code enforcement for CI integration
- Comprehensive test suite (>80% coverage)
- Quick start documentation and examples
- PyPI-ready packaging

### Security
- All security analyzers operate offline (no external API calls)
- Policy-based severity gates prevent risky patterns from passing CI
