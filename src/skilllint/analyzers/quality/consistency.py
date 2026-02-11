from __future__ import annotations

import re
from collections import Counter

from skilllint.core.result import MetricScore


def score_consistency(text: str) -> MetricScore:
    words = re.findall(r"\b[a-zA-Z][a-zA-Z0-9_-]{2,}\b", text.lower())
    if not words:
        return MetricScore("consistency", 0.0, target=">85", notes="No content")
    common = Counter(words).most_common(20)
    dominant = sum(c for _, c in common) / max(1, len(words))
    # reward stable repeated terminology up to a point
    score = min(100.0, 60.0 + dominant * 120.0)
    return MetricScore("consistency", round(score, 2), target=">85", notes=f"top20_ratio={dominant:.2f}")
