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
        "security_integration_min": 75,
    },
    "security": {
        "fail_on": ["critical", "high"],
        "intel": {"mode": "bundled", "ai_assisted": False, "allow_remote": False},
    },
}


def _tiny_yaml_load(text: str) -> dict[str, Any]:
    """Very small YAML-ish loader for project policy files.

    Supports simple nested maps/lists used by our default policies.
    """
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

        if line.startswith("- "):
            item = line[2:].strip()
            if isinstance(parent, list):
                parent.append(item)
            continue

        if ":" not in line:
            continue
        k, v = [x.strip() for x in line.split(":", 1)]

        if v == "":
            # create nested map by default; switch to list if next lines are '- '
            node: Any = {}
            if isinstance(parent, dict):
                parent[k] = node
            stack.append((indent + 2, node))
            continue

        # scalar parse
        if v.isdigit():
            sv: Any = int(v)
        elif v.lower() in {"true", "false"}:
            sv = v.lower() == "true"
        else:
            sv = v.strip('"')

        if isinstance(parent, dict):
            parent[k] = sv

    # post-pass for known list under security.fail_on in minimal policies
    if "security" in data and isinstance(data["security"], dict):
        sec = data["security"]
        if "fail_on" in sec and isinstance(sec["fail_on"], dict) and not sec["fail_on"]:
            # couldn't infer list; try regex extraction
            values = []
            in_block = False
            for raw in text.splitlines():
                if raw.strip().startswith("fail_on:"):
                    in_block = True
                    continue
                if in_block:
                    s = raw.strip()
                    if s.startswith("- "):
                        values.append(s[2:].strip())
                    elif s and not s.startswith("#") and not raw.startswith(" " * 4):
                        break
            sec["fail_on"] = values

    return data


def load_policy(path: Path | None) -> dict[str, Any]:
    if path is None:
        return DEFAULT_POLICY

    text = path.read_text(encoding="utf-8")

    # Try JSON first
    try:
        obj = json.loads(text)
        if isinstance(obj, dict):
            return obj
    except Exception:
        pass

    # Try PyYAML if available
    try:
        import yaml  # type: ignore

        obj = yaml.safe_load(text)
        if isinstance(obj, dict):
            return obj
    except Exception:
        pass

    # tiny fallback parser
    return _tiny_yaml_load(text)


def should_fail(findings_by_severity: dict[str, int], fail_on: list[str]) -> bool:
    return any(findings_by_severity.get(level, 0) > 0 for level in fail_on)
