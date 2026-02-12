from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Optional


@dataclass
class Finding:
    id: str
    source: str  # finding source category (reserved)
    severity: str  # low | medium | high | critical
    confidence: float
    category: str
    file: str
    line_start: Optional[int] = None
    line_end: Optional[int] = None
    evidence: str = ""
    title: str = ""
    remediation: str = ""


@dataclass
class MetricScore:
    name: str
    score: float
    target: Optional[str] = None
    notes: str = ""


@dataclass
class ScanSummary:
    files_scanned: int = 0
    findings_total: int = 0
    by_severity: dict[str, int] = field(default_factory=dict)
    quality_overall: float = 0.0


@dataclass
class ScanResult:
    target: str
    findings: list[Finding] = field(default_factory=list)
    metrics: list[MetricScore] = field(default_factory=list)
    summary: ScanSummary = field(default_factory=ScanSummary)

    def to_dict(self) -> dict[str, Any]:
        return {
            "tool": "skilllint",
            "target": self.target,
            "summary": asdict(self.summary),
            "metrics": [asdict(m) for m in self.metrics],
            "findings": [asdict(f) for f in self.findings],
        }
