from __future__ import annotations

import re
from pathlib import Path

from skilllint.core.result import Finding


RX = re.compile(r"\b(latest|\*)\b")


def analyze(path: Path, text: str) -> list[Finding]:
    if path.name not in {"requirements.txt", "package.json", "pyproject.toml"}:
        return []
    findings: list[Finding] = []
    for i, line in enumerate(text.splitlines(), start=1):
        if RX.search(line) and any(x in line for x in ["==", ">=", "^", "~", ":"]):
            findings.append(
                Finding(
                    id="SEC-SUPPLY-UNPINNED",
                    source="security",
                    severity="medium",
                    confidence=0.7,
                    category="supply_chain",
                    file=str(path),
                    line_start=i,
                    line_end=i,
                    evidence=line.strip()[:300],
                    title="Dependency may be weakly pinned",
                    remediation="Prefer pinned versions for reproducible and safer builds.",
                )
            )
    return findings
