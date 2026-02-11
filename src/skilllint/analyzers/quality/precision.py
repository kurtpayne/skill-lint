from __future__ import annotations

import re

from skilllint.core.result import MetricScore


VAGUE = re.compile(r"\b(maybe|somehow|various|etc\.?|probably|could be)\b", re.I)


def score_precision(text: str) -> MetricScore:
    words = max(1, len(re.findall(r"\b\w+\b", text)))
    vague = len(VAGUE.findall(text))
    ratio = vague / words
    score = max(0.0, min(100.0, 100.0 - ratio * 1200.0))
    return MetricScore("precision", round(score, 2), target=">80", notes=f"vague_terms={vague}")
