from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Iterable


SUPPORTED_EXTENSIONS = {".yaml", ".yml", ".md", ".txt", ".json", ".py"}


def _iter_with_ripgrep(target: Path) -> Iterable[Path]:
    """Fast file discovery using ripgrep if available.

    Falls back by raising RuntimeError if rg is unavailable or fails.
    """
    if shutil.which("rg") is None:
        raise RuntimeError("ripgrep not installed")

    # rg --files lists tracked/visible files quickly; we filter extensions in Python
    proc = subprocess.run(
        ["rg", "--files", str(target)],
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode not in (0, 1):
        raise RuntimeError(f"ripgrep failed: exit={proc.returncode}")

    for line in proc.stdout.splitlines():
        p = Path(line)
        if not p.is_absolute():
            p = target / p
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS:
            yield p


def _iter_with_rglob(target: Path) -> Iterable[Path]:
    for p in target.rglob("*"):
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS:
            yield p


def iter_candidate_files(target: Path) -> Iterable[Path]:
    if target.is_file():
        if target.suffix.lower() in SUPPORTED_EXTENSIONS:
            yield target
        return

    try:
        yielded = False
        for p in _iter_with_ripgrep(target):
            yielded = True
            yield p
        if yielded:
            return
    except Exception:
        # deterministic fallback path
        pass

    yield from _iter_with_rglob(target)
