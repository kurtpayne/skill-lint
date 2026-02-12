from skilllint.analyzers.quality.readability import score_readability
from skilllint.analyzers.quality.complexity import score_complexity
from skilllint.analyzers.quality.structure import score_structure
from skilllint.analyzers.quality.completeness import score_completeness


def test_readability_simple():
    text = "This is a simple test. It has short words. Easy to read."
    result = score_readability(text)
    assert result.name == "readability"
    assert result.score > 0
    assert result.score <= 100


def test_complexity_low():
    text = "Simple linear text with no branching."
    result = score_complexity(text)
    assert result.name == "complexity"
    assert result.score >= 90  # should be very high (low complexity)


def test_structure_with_headings():
    text = "# Heading\n\n- bullet 1\n- bullet 2\n\nParagraph text."
    result = score_structure(text)
    assert result.score >= 50


def test_completeness_all_sections():
    text = "# Overview\n\n# Inputs\n\n# Outputs\n\n# Examples"
    result = score_completeness(text)
    assert result.score == 80.0
