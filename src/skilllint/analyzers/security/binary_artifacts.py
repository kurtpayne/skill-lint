from __future__ import annotations

from pathlib import Path

from skilllint.core.result import Finding


BINARY_EXTS = {".exe", ".dll", ".so", ".dylib", ".bin", ".jar"}


def analyze(path: Path, _text: str) -> list[Finding]:
    if path.suffix.lower() not in BINARY_EXTS:
        return []
    return [
        Finding(
            id="SEC-BIN-ARTIFACT",
            source="security",
            severity="high",
            confidence=0.9,
            category="binary_artifact",
            file=str(path),
            title="Binary artifact detected",
            evidence=path.name,
            remediation="Track provenance and verify checksums/signatures for binaries.",
        )
    ]
