from __future__ import annotations

import re

from skilllint.core.result import MetricScore


def score_maintainability(text: str) -> MetricScore:
    lines = max(1, len(text.splitlines()))
    duplicates = len(re.findall(r"\b(TODO|FIXME|HACK)\b", text, flags=re.I))
    long_lines = sum(1 for line in text.splitlines() if len(line) > 140)
    penalty = min(100.0, duplicates * 8 + long_lines * 1.5 + (lines / 500) * 10)
    score = max(0.0, 100.0 - penalty)
    return MetricScore("maintainability", round(score, 2), target=">70", notes=f"todo_like={duplicates} long_lines={long_lines}")
