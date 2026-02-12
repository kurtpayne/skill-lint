from __future__ import annotations

import re
from pathlib import Path


_HEADING_RX = re.compile(r"^(#+)([^#\s].*)$", flags=re.M)
_TRAILING_WS_BEFORE_NL = re.compile(r"[ \t]+(?=\n)")
_TRAILING_WS_END = re.compile(r"[ \t]+\Z")


def apply_safe_fixes_to_text(text: str) -> tuple[str, list[str]]:
    changes: list[str] = []
    out = text

    # Normalize line endings
    if "\r\n" in out:
        out = out.replace("\r\n", "\n")
        changes.append("normalized_line_endings")

    # Trim trailing spaces while preserving existing line structure
    trimmed = _TRAILING_WS_BEFORE_NL.sub("", out)
    trimmed = _TRAILING_WS_END.sub("", trimmed)
    if trimmed != out:
        out = trimmed
        changes.append("trimmed_trailing_whitespace")

    # Ensure single terminal newline
    if not out.endswith("\n"):
        out += "\n"
        changes.append("added_terminal_newline")

    # Normalize malformed markdown headings: '#Heading' -> '# Heading'
    fixed = _HEADING_RX.sub(lambda m: f"{m.group(1)} {m.group(2).lstrip()}", out)
    if fixed != out:
        out = fixed
        changes.append("normalized_markdown_headings")

    # Standardize old tool naming typo
    replaced = out.replace("bash-tool", "bash_tool")
    if replaced != out:
        out = replaced
        changes.append("standardized_tool_name_bash_tool")

    return out, changes


def apply_safe_fixes(path: Path) -> list[str]:
    try:
        original = path.read_text(encoding="utf-8")
    except Exception:
        return []

    fixed, changes = apply_safe_fixes_to_text(original)
    if changes and fixed != original:
        path.write_text(fixed, encoding="utf-8")
    return changes
