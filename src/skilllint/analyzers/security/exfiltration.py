from __future__ import annotations

import re
from pathlib import Path

from skilllint.core.result import Finding


RX = re.compile(r"\b(http[s]?://|webhook|pastebin|ngrok|requestbin)\b", re.I)


def analyze(path: Path, text: str) -> list[Finding]:
    findings: list[Finding] = []
    for i, line in enumerate(text.splitlines(), start=1):
        if RX.search(line):
            findings.append(
                Finding(
                    id="SEC-EXFIL-URL",
                    source="security",
                    severity="medium",
                    confidence=0.75,
                    category="exfiltration",
                    file=str(path),
                    line_start=i,
                    line_end=i,
                    evidence=line.strip()[:300],
                    title="Potential outbound exfiltration channel",
                    remediation="Review outbound URLs and require allowlisted destinations.",
                )
            )
    return findings
