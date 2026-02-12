from __future__ import annotations

import re

from skilllint.core.result import MetricScore


SECTION_FAMILIES: dict[str, tuple[str, ...]] = {
    "overview": ("overview", "summary", "introduction", "purpose", "context"),
    "inputs": ("inputs", "input", "prerequisites", "requirements"),
    "outputs": ("outputs", "output", "results", "deliverables", "response"),
    "examples": ("examples", "usage", "quickstart", "getting started"),
    "constraints": ("constraints", "limitations", "guardrails", "boundaries"),
    "failure_modes": ("troubleshooting", "errors", "failure", "common issues", "pitfalls"),
}

CORE_FAMILIES = ("overview", "inputs", "outputs", "examples")
OPTIONAL_FAMILIES = ("constraints", "failure_modes")


def _has_family(text_lower: str, aliases: tuple[str, ...]) -> bool:
    return any(re.search(rf"\b{re.escape(alias)}\b", text_lower) for alias in aliases)


def score_completeness(text: str) -> MetricScore:
    lower = text.lower()
    found_core = sum(1 for fam in CORE_FAMILIES if _has_family(lower, SECTION_FAMILIES[fam]))
    found_optional = sum(1 for fam in OPTIONAL_FAMILIES if _has_family(lower, SECTION_FAMILIES[fam]))

    # Core sections account for 80 points, optional operational sections 20 points.
    core_score = (found_core / len(CORE_FAMILIES)) * 80.0
    optional_score = (found_optional / len(OPTIONAL_FAMILIES)) * 20.0
    score = core_score + optional_score

    return MetricScore(
        "completeness",
        round(score, 2),
        target=">80",
        notes=f"core={found_core}/{len(CORE_FAMILIES)} optional={found_optional}/{len(OPTIONAL_FAMILIES)}",
    )
