from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class IntelConfig:
    mode: str = "bundled"  # disabled | bundled | file
    file: str | None = None
    allow_remote: bool = False
    ai_assisted: bool = False


@dataclass
class IntelBundle:
    patterns: dict[str, list[dict[str, Any]]] = field(default_factory=dict)


def _load_yaml(path: Path) -> dict[str, Any]:
    import yaml  # type: ignore

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def resolve_intel_config(policy: dict[str, Any]) -> IntelConfig:
    security = policy.get("security", {}) if isinstance(policy, dict) else {}
    intel = security.get("intel", {}) if isinstance(security, dict) else {}
    cfg = IntelConfig()
    if isinstance(intel, dict):
        cfg.mode = str(intel.get("mode", cfg.mode)).lower()
        cfg.file = intel.get("file")
        cfg.allow_remote = bool(intel.get("allow_remote", False))
        cfg.ai_assisted = bool(intel.get("ai_assisted", False))

    # Strong offline defaults: always disable AI-assisted and remote fetch.
    cfg.ai_assisted = False
    cfg.allow_remote = False

    if cfg.mode not in {"disabled", "bundled", "file"}:
        cfg.mode = "bundled"
    if cfg.mode == "file" and not cfg.file:
        cfg.mode = "bundled"
    return cfg


def load_intel_bundle(config: IntelConfig, project_root: Path | None = None) -> IntelBundle:
    if config.mode == "disabled":
        return IntelBundle()

    if config.mode == "file" and config.file:
        path = Path(config.file)
        if not path.is_absolute() and project_root:
            path = (project_root / path).resolve()
        if path.exists():
            data = _load_yaml(path)
            return IntelBundle(patterns=_extract_patterns(data))

    bundled = Path(__file__).resolve().parent.parent / "signatures" / "security_signatures.yaml"
    if bundled.exists():
        data = _load_yaml(bundled)
        return IntelBundle(patterns=_extract_patterns(data))
    return IntelBundle()


def _extract_patterns(raw: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = {}
    patterns = raw.get("patterns", {}) if isinstance(raw, dict) else {}
    if not isinstance(patterns, dict):
        return out

    for category, items in patterns.items():
        if not isinstance(items, list):
            continue
        valid: list[dict[str, Any]] = []
        for item in items:
            if isinstance(item, dict) and "id" in item and "regex" in item:
                valid.append(item)
        if valid:
            out[str(category)] = valid
    return out
