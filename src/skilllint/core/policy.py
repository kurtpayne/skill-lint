from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DEFAULT_POLICY = {
    "version": 1,
    "name": "default",
    "quality": {
        "readability_min": 70,
        "complexity_max": 30,
        "structure_min": 80,
        "consistency_min": 85,
        "completeness_min": 90,
        "maintainability_min": 70,
        "precision_min": 80,
    },
}


def _tiny_yaml_load(text: str) -> dict[str, Any]:
    """Very small YAML-ish loader for simple policy maps."""
    data: dict[str, Any] = {}
    stack: list[tuple[int, Any]] = [(0, data)]

    for raw in text.splitlines():
        if not raw.strip() or raw.strip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()

        while stack and indent < stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]

        if ":" not in line:
            continue
        k, v = [x.strip() for x in line.split(":", 1)]

        if v == "":
            node: Any = {}
            if isinstance(parent, dict):
                parent[k] = node
            stack.append((indent + 2, node))
            continue

        if v.isdigit():
            sv: Any = int(v)
        elif v.lower() in {"true", "false"}:
            sv = v.lower() == "true"
        else:
            sv = v.strip('"')

        if isinstance(parent, dict):
            parent[k] = sv

    return data


def load_policy(path: Path | None) -> dict[str, Any]:
    if path is None:
        return DEFAULT_POLICY

    text = path.read_text(encoding="utf-8")

    try:
        obj = json.loads(text)
        if isinstance(obj, dict):
            return obj
    except Exception:
        pass

    try:
        import yaml  # type: ignore

        obj = yaml.safe_load(text)
        if isinstance(obj, dict):
            return obj
    except Exception:
        pass

    return _tiny_yaml_load(text)
