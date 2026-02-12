# Contributing to SkillLint

Thanks for your interest in contributing! SkillLint is 100% open source and welcomes improvements.

## Development Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/kurtpayne/skill-lint
   cd skill-lint
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install in editable mode with dev dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Run tests:
   ```bash
   pytest tests/ -v
   ```

## Making Changes

1. Create a feature branch:
   ```bash
   git checkout -b feature/my-improvement
   ```

2. Make your changes and add tests.

3. Verify tests pass:
   ```bash
   pytest tests/ -v --cov=src/skilllint
   ```

4. Run the linter on itself (dogfooding):
   ```bash
   skilllint scan . --policy src/skilllint/policies/default.yaml
   ```

5. Commit with a clear message:
   ```bash
   git commit -m "feat: add new quality metric for X"
   ```

6. Push and open a PR:
   ```bash
   git push origin feature/my-improvement
   ```

## Contribution Guidelines

### Code Style
- Follow PEP 8 (enforced via `ruff`)
- Type hints encouraged for public APIs
- Keep functions focused and testable

### Testing
- Add tests for new features
- Maintain >80% code coverage
- Test both happy path and edge cases

### Commits
Use conventional commit format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation only
- `test:` - Test changes
- `refactor:` - Code refactoring

### Pull Requests
- Reference related issues
- Describe what changed and why
- Keep PRs focused (one feature/fix per PR)
- Ensure CI passes before requesting review

## Adding Analyzers

### New Quality Metric
1. Create `src/skilllint/analyzers/quality/my_metric.py`
2. Implement `score_my_metric(text: str) -> MetricScore`
3. Add to orchestrator in `src/skilllint/core/analyzer.py`
4. Add tests in `tests/test_quality_analyzers.py`
5. Update policy files with threshold

### New Security Pattern
1. Create `src/skilllint/analyzers/security/my_check.py`
2. Implement `analyze(path: Path, text: str) -> list[Finding]`
3. Add to orchestrator
4. Add tests
5. Document in README

## Questions?

Open an issue or discussion on GitHub!
