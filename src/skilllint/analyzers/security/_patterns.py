from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from skilllint.core.result import Finding


def build_patterns(entries: list[dict[str, Any]]) -> list[tuple[str, re.Pattern[str], str, float, str, str]]:
    compiled: list[tuple[str, re.Pattern[str], str, float, str, str]] = []
    for entry in entries:
        try:
            pid = str(entry["id"])
            rx = re.compile(str(entry["regex"]), re.I)
            sev = str(entry.get("severity", "medium"))
            conf = float(entry.get("confidence", 0.75))
            title = str(entry.get("title", f"Security pattern detected: {pid}"))
            remediation = str(entry.get("remediation", "Review and remediate suspicious pattern."))
            compiled.append((pid, rx, sev, conf, title, remediation))
        except Exception:
            continue
    return compiled


def run_line_patterns(
    path: Path,
    text: str,
    category: str,
    findings_prefix: str,
    patterns: list[tuple[str, re.Pattern[str], str, float, str, str]],
) -> list[Finding]:
    out: list[Finding] = []
    for i, line in enumerate(text.splitlines(), start=1):
        for pid, rx, sev, conf, title, remediation in patterns:
            if rx.search(line):
                out.append(
                    Finding(
                        id=f"{findings_prefix}-{pid}",
                        source="security",
                        severity=sev,
                        confidence=conf,
                        category=category,
                        file=str(path),
                        line_start=i,
                        line_end=i,
                        evidence=line.strip()[:300],
                        title=title,
                        remediation=remediation,
                    )
                )
    return out
