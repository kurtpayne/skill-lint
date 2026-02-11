from __future__ import annotations

import re

from skilllint.core.result import MetricScore


def score_complexity(text: str) -> MetricScore:
    # Lower is better in concept; we return 0..100 where higher is better for consistency.
    # Penalize branching words and nesting markers.
    branch_tokens = re.findall(r"\b(if|elif|else|for|while|and|or|case|when)\b", text, flags=re.I)
    nesting_tokens = re.findall(r"(\{|\}|\(|\)|\[|\])", text)
    lines = max(1, len(text.splitlines()))

    raw = (len(branch_tokens) * 2.5 + len(nesting_tokens) * 0.4) / lines
    penalty = min(100.0, raw * 20)
    score = max(0.0, 100.0 - penalty)
    return MetricScore(
        name="complexity",
        score=round(score, 2),
        target=">=70 (maps from <30 raw complexity)",
        notes=f"branches={len(branch_tokens)} nesting={len(nesting_tokens)} lines={lines}",
    )
