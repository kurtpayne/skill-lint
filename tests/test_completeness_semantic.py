from skilllint.analyzers.quality.completeness import score_completeness


def test_completeness_semantic_aliases_core_present():
    text = """
# Purpose

## Prerequisites

## Results

## Getting Started
"""
    result = score_completeness(text)
    assert result.score >= 80.0


def test_completeness_bonus_for_operational_sections():
    text = """
# Overview
## Inputs
## Outputs
## Examples
## Troubleshooting
## Constraints
"""
    result = score_completeness(text)
    assert result.score == 100.0
