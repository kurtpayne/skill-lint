from __future__ import annotations

import re

from skilllint.core.result import MetricScore


REQUIRED_SECTIONS = ["overview", "inputs", "outputs", "examples"]


def score_completeness(text: str) -> MetricScore:
    lower = text.lower()
    found = 0
    for sec in REQUIRED_SECTIONS:
        if re.search(rf"\b{re.escape(sec)}\b", lower):
            found += 1
    score = (found / len(REQUIRED_SECTIONS)) * 100.0
    return MetricScore("completeness", round(score, 2), target=">90", notes=f"required_sections_found={found}/{len(REQUIRED_SECTIONS)}")
