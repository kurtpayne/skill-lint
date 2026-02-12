from __future__ import annotations

from pathlib import Path

from skilllint.analyzers.quality.completeness import score_completeness
from skilllint.analyzers.quality.complexity import score_complexity
from skilllint.analyzers.quality.consistency import score_consistency
from skilllint.analyzers.quality.maintainability import score_maintainability
from skilllint.analyzers.quality.precision import score_precision
from skilllint.analyzers.quality.readability import score_readability
from skilllint.analyzers.quality.structure import score_structure
from skilllint.analyzers.quality.lints import analyze_quality_lints
from skilllint.core.file_handler import iter_candidate_files
from skilllint.core.result import ScanResult


def _read_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""


def analyze(target: Path, policy: dict | None = None) -> ScanResult:
    _ = policy  # reserved for future quality-only extensions
    result = ScanResult(target=str(target))

    for file_path in iter_candidate_files(target):
        text = _read_file(file_path)
        if text:
            result.metrics.extend(
                [
                    score_readability(text),
                    score_complexity(text),
                    score_structure(text),
                    score_consistency(text),
                    score_completeness(text),
                    score_maintainability(text),
                    score_precision(text),
                ]
            )
            result.findings.extend(analyze_quality_lints(file_path, text))

        result.summary.files_scanned += 1

    sev = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for f in result.findings:
        sev[f.severity] = sev.get(f.severity, 0) + 1
    result.summary.findings_total = len(result.findings)
    result.summary.by_severity = sev
    if result.metrics:
        result.summary.quality_overall = round(sum(m.score for m in result.metrics) / len(result.metrics), 2)

    return result
