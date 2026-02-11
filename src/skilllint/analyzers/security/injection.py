from __future__ import annotations

import re
from pathlib import Path

from skilllint.core.result import Finding


PATTERNS = [
    ("prompt_injection_ignore", re.compile(r"ignore\s+previous\s+instructions", re.I), "high"),
    ("prompt_injection_system", re.compile(r"you\s+are\s+now\s+in\s+developer\s+mode", re.I), "medium"),
    ("template_raw_input", re.compile(r"\{\{\s*user_input\s*\}\}|\{user_input\}", re.I), "medium"),
]


def analyze(path: Path, text: str) -> list[Finding]:
    findings: list[Finding] = []
    lines = text.splitlines()
    for i, line in enumerate(lines, start=1):
        for pid, rx, sev in PATTERNS:
            if rx.search(line):
                findings.append(
                    Finding(
                        id=f"SEC-INJ-{pid}",
                        source="security",
                        severity=sev,
                        confidence=0.85,
                        category="injection",
                        file=str(path),
                        line_start=i,
                        line_end=i,
                        evidence=line.strip()[:300],
                        title=f"Possible injection pattern: {pid}",
                        remediation="Sanitize/segment untrusted input and avoid direct prompt interpolation.",
                    )
                )
    return findings
