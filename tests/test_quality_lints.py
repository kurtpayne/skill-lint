from pathlib import Path

from skilllint.analyzers.quality.lints import analyze_quality_lints


def test_missing_usage_and_troubleshooting_findings():
    text = """
---
name: sample-skill
description: brief description
---

# Overview
Some content.
"""
    findings = analyze_quality_lints(Path("SKILL.md"), text)
    ids = {f.id for f in findings}
    assert "QLINT-ONBOARDING-MISSING" in ids
    assert "QLINT-TROUBLESHOOTING-MISSING" in ids


def test_strong_skill_has_fewer_findings():
    text = """
---
name: deployment-debug
description: This skill should be used when users need deployment debugging help with logs and remediation steps.
---

# Overview

## Usage

```bash
run tool --arg
```

## Examples
For example: do x.
For example: do y.

## Troubleshooting
If command fails, retry with verbose and inspect logs.
"""
    findings = analyze_quality_lints(Path("SKILL.md"), text)
    ids = {f.id for f in findings}
    assert "QLINT-ONBOARDING-MISSING" not in ids
    assert "QLINT-TROUBLESHOOTING-MISSING" not in ids
