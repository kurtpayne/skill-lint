# Changelog

All notable changes to SkillLint will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-02-11

### Changed
- Re-scoped SkillLint to a **pure quality assessment + linting** tool.
- Removed all security scanning analyzers, signatures, and intel subsystem.
- Removed security policy gates; only quality gates remain.
- Simplified scan reporting to quality-centric output.
- Updated README/docs/examples/implementation plan for quality-only positioning.
- Updated tests and CI expectations to quality-only behavior.

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

## [1.0.0] - 2026-02-11

### Added
- Initial release of SkillLint v1.0
