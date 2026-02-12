from __future__ import annotations

from pathlib import Path

from skilllint.analyzers.security._patterns import build_patterns, run_line_patterns
from skilllint.core.result import Finding


TARGET_FILES = {"requirements.txt", "package.json", "pyproject.toml", "poetry.lock", "Pipfile"}


def analyze(path: Path, text: str, intel_patterns: list[dict] | None = None) -> list[Finding]:
    if path.name not in TARGET_FILES:
        return []

    base = [
        {
            "id": "unpinned",
            "regex": r"\b(latest|\*)\b",
            "severity": "medium",
            "confidence": 0.72,
            "title": "Dependency may be weakly pinned",
            "remediation": "Prefer pinned versions for reproducible and safer builds.",
        },
        {
            "id": "git_head",
            "regex": r"(git\+https?://|github\.com/.+@(main|master|HEAD))",
            "severity": "high",
            "confidence": 0.84,
            "title": "Floating VCS dependency reference",
            "remediation": "Pin immutable commit SHAs for VCS dependencies.",
        },
    ]
    patterns = build_patterns(base + (intel_patterns or []))
    return run_line_patterns(path, text, "supply_chain", "SEC-SUPPLY", patterns)
