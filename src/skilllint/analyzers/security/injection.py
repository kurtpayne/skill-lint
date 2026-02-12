from __future__ import annotations

from pathlib import Path

from skilllint.analyzers.security._patterns import build_patterns, run_line_patterns


def analyze(path: Path, text: str, intel_patterns: list[dict] | None = None) -> list:
    base = [
        {
            "id": "prompt_injection_ignore",
            "regex": r"ignore\s+previous\s+instructions",
            "severity": "high",
            "confidence": 0.9,
            "title": "Prompt-injection override phrase",
            "remediation": "Sanitize/segment untrusted input and keep instruction hierarchy intact.",
        },
        {
            "id": "prompt_injection_system",
            "regex": r"you\s+are\s+now\s+in\s+developer\s+mode",
            "severity": "medium",
            "confidence": 0.85,
            "title": "Prompt jailbreak phrase",
            "remediation": "Block jailbreak trigger phrases and enforce policy boundaries.",
        },
        {
            "id": "template_raw_input",
            "regex": r"\{\{\s*user_input\s*\}\}|\{user_input\}",
            "severity": "medium",
            "confidence": 0.8,
            "title": "Raw user input interpolation",
            "remediation": "Sanitize/segment untrusted input and avoid direct prompt interpolation.",
        },
    ]
    patterns = build_patterns(base + (intel_patterns or []))
    return run_line_patterns(path, text, "injection", "SEC-INJ", patterns)
