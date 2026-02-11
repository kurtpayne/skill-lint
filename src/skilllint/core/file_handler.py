from pathlib import Path
from typing import Iterable


SUPPORTED_EXTENSIONS = {".yaml", ".yml", ".md", ".txt", ".json", ".py"}


def iter_candidate_files(target: Path) -> Iterable[Path]:
    if target.is_file():
        if target.suffix.lower() in SUPPORTED_EXTENSIONS:
            yield target
        return
    for p in target.rglob("*"):
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS:
            yield p
