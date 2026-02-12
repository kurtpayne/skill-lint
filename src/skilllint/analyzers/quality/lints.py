from __future__ import annotations

import re
from pathlib import Path

from skilllint.core.result import Finding


HEADING_RE = re.compile(r"^#{1,6}\s+(.+)$", flags=re.M)
CODE_FENCE_RE = re.compile(r"```", flags=re.M)


def _line_number(text: str, pattern: re.Pattern[str]) -> int | None:
    m = pattern.search(text)
    if not m:
        return None
    return text[: m.start()].count("\n") + 1


def analyze_quality_lints(path: Path, text: str) -> list[Finding]:
    findings: list[Finding] = []
    lower = text.lower()
    headings = [h.strip().lower() for h in HEADING_RE.findall(text)]

    # 1) Frontmatter trigger quality (when frontmatter exists)
    if text.lstrip().startswith("---"):
        fm_end = text.find("\n---", 3)
        frontmatter = text[: fm_end + 4] if fm_end != -1 else ""
        if frontmatter:
            has_name = bool(re.search(r"^name:\s*\S+", frontmatter, flags=re.M))
            has_desc = bool(re.search(r"^description:\s*.+", frontmatter, flags=re.M))
            if not has_name or not has_desc:
                findings.append(
                    Finding(
                        id="QLINT-FRONTMATTER-REQUIRED",
                        source="quality",
                        severity="medium",
                        confidence=0.95,
                        category="authoring",
                        file=str(path),
                        title="Missing required frontmatter fields",
                        evidence="frontmatter should include name and description",
                        remediation="Add YAML frontmatter with `name` and trigger-focused `description`.",
                    )
                )
            desc_match = re.search(r"^description:\s*(.+)$", frontmatter, flags=re.M)
            if desc_match:
                desc = desc_match.group(1).strip().lower()
                if len(desc.split()) < 10 or ("use when" not in desc and "should be used when" not in desc):
                    findings.append(
                        Finding(
                            id="QLINT-TRIGGER-CLARITY",
                            source="quality",
                            severity="low",
                            confidence=0.8,
                            category="activation",
                            file=str(path),
                            title="Description may be too vague for reliable activation",
                            evidence=desc_match.group(1).strip()[:300],
                            remediation="Describe concrete trigger conditions (e.g., 'Use when ...').",
                        )
                    )

    # 2) Onboarding/usage
    has_usage = any(k in h for h in headings for k in ["usage", "quickstart", "getting started"])
    if not has_usage:
        findings.append(
            Finding(
                id="QLINT-ONBOARDING-MISSING",
                source="quality",
                severity="medium",
                confidence=0.85,
                category="onboarding",
                file=str(path),
                title="Missing onboarding section",
                evidence="No Usage/Quickstart/Getting Started heading detected",
                remediation="Add a short quickstart section with first 1-3 steps.",
            )
        )

    # 3) Troubleshooting / failure modes
    has_troubleshooting = any(k in h for h in headings for k in ["troubleshooting", "failure", "errors", "pitfalls"])
    if not has_troubleshooting:
        findings.append(
            Finding(
                id="QLINT-TROUBLESHOOTING-MISSING",
                source="quality",
                severity="low",
                confidence=0.82,
                category="operability",
                file=str(path),
                title="Missing troubleshooting or failure mode guidance",
                evidence="No Troubleshooting/Errors heading detected",
                remediation="Document common failures and recovery steps.",
            )
        )

    # 4) Example density
    code_fences = len(CODE_FENCE_RE.findall(text)) // 2
    explicit_examples = len(re.findall(r"\bfor example\b|\bexample:\b", lower))
    if code_fences == 0 and explicit_examples < 2:
        findings.append(
            Finding(
                id="QLINT-EXAMPLES-THIN",
                source="quality",
                severity="medium",
                confidence=0.75,
                category="examples",
                file=str(path),
                title="Few concrete examples detected",
                evidence=f"code_fences={code_fences}, example_mentions={explicit_examples}",
                remediation="Add at least 1-2 realistic examples including expected output.",
            )
        )

    # 5) Dense paragraphs
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    too_dense = [p for p in paragraphs if len(re.findall(r"\b\w+\b", p)) > 180]
    if too_dense:
        findings.append(
            Finding(
                id="QLINT-DENSITY-HIGH",
                source="quality",
                severity="low",
                confidence=0.78,
                category="readability",
                file=str(path),
                line_start=_line_number(text, re.compile(re.escape(too_dense[0][:40]))),
                title="Large dense paragraph may hurt readability",
                evidence=too_dense[0][:300],
                remediation="Split dense blocks into shorter sections or bullets.",
            )
        )

    return findings
