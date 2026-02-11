from __future__ import annotations

import re

from skilllint.core.result import MetricScore


def score_security_integration(text: str) -> MetricScore:
    checks = {
        "input_validation": bool(re.search(r"\b(validate|sanitize)\b", text, flags=re.I)),
        "error_handling": bool(re.search(r"\b(error|exception|fallback|retry)\b", text, flags=re.I)),
        "secure_defaults": bool(re.search(r"\b(least privilege|deny by default|secure)\b", text, flags=re.I)),
        "secret_hygiene": bool(re.search(r"\b(secret|token|apikey|api key|credential)\b", text, flags=re.I)),
    }
    score = (sum(1 for v in checks.values() if v) / len(checks)) * 100.0
    return MetricScore("security_integration", round(score, 2), target=">75", notes=str(checks))
