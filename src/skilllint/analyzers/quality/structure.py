from __future__ import annotations

import re

from skilllint.core.result import MetricScore


def score_structure(text: str) -> MetricScore:
    headings = re.findall(r"^#{1,6}\s+.+$", text, flags=re.M)
    bullet = re.findall(r"^\s*[-*]\s+.+$", text, flags=re.M)
    paragraphs = [p for p in text.split("\n\n") if p.strip()]

    score = 40.0
    score += min(25.0, len(headings) * 5)
    score += min(20.0, len(bullet) * 1.5)
    score += min(15.0, len(paragraphs) * 1.2)
    score = max(0.0, min(100.0, score))
    return MetricScore("structure", round(score, 2), target=">80", notes=f"headings={len(headings)}")
