from __future__ import annotations

import re

from skilllint.core.result import MetricScore


_SENTENCE_SPLIT = re.compile(r"[.!?]+")
_WORD = re.compile(r"[A-Za-z0-9_'-]+")


def _syllables(word: str) -> int:
    word = word.lower()
    groups = re.findall(r"[aeiouy]+", word)
    count = len(groups) if groups else 1
    if word.endswith("e") and count > 1:
        count -= 1
    return max(1, count)


def score_readability(text: str) -> MetricScore:
    words = _WORD.findall(text)
    sentences = [s for s in _SENTENCE_SPLIT.split(text) if s.strip()]
    if not words:
        return MetricScore(name="readability", score=0.0, target="70-80", notes="No words found")

    w = len(words)
    s = max(1, len(sentences))
    syll = sum(_syllables(x) for x in words)

    # Flesch Reading Ease, clamped 0..100
    flesch = 206.835 - 1.015 * (w / s) - 84.6 * (syll / w)
    score = max(0.0, min(100.0, flesch))
    return MetricScore(
        name="readability",
        score=round(score, 2),
        target="70-80",
        notes=f"sentences={s} words={w}",
    )
