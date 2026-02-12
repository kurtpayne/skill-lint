from __future__ import annotations

from pathlib import Path

from skilllint.analyzers.security._patterns import build_patterns, run_line_patterns
from skilllint.core.result import Finding


def analyze(path: Path, text: str, intel_patterns: list[dict] | None = None) -> list[Finding]:
    base = [
        {
            "id": "url",
            "regex": r"\b(http[s]?://|webhook|pastebin|ngrok|requestbin)\b",
            "severity": "medium",
            "confidence": 0.76,
            "title": "Potential outbound exfiltration channel",
            "remediation": "Review outbound URLs and require allowlisted destinations.",
        },
        {
            "id": "secret_material",
            "regex": r"(AWS_SECRET_ACCESS_KEY|OPENAI_API_KEY|BEGIN\s+PRIVATE\s+KEY)",
            "severity": "critical",
            "confidence": 0.94,
            "title": "Possible secret material exposure",
            "remediation": "Remove exposed secret material and rotate credentials.",
        },
    ]
    patterns = build_patterns(base + (intel_patterns or []))
    return run_line_patterns(path, text, "exfiltration", "SEC-EXFIL", patterns)
