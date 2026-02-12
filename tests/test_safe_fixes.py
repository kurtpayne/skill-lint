from skilllint.fixes.safe_fixes import apply_safe_fixes_to_text


def test_trailing_whitespace():
    text, changes = apply_safe_fixes_to_text("line 1  \nline 2\t\n")
    assert "trimmed_trailing_whitespace" in changes
    assert text == "line 1\nline 2\n"


def test_terminal_newline():
    text, changes = apply_safe_fixes_to_text("content")
    assert "added_terminal_newline" in changes
    assert text.endswith("\n")


def test_markdown_heading_spacing():
    text, changes = apply_safe_fixes_to_text("#Heading\n##Another")
    assert "normalized_markdown_headings" in changes
    assert "# Heading" in text
    assert "## Another" in text


def test_tool_name_standardization():
    text, changes = apply_safe_fixes_to_text("Use bash-tool for scripts")
    assert "standardized_tool_name_bash_tool" in changes
    assert "bash_tool" in text


def test_no_changes_needed():
    text, changes = apply_safe_fixes_to_text("# Clean heading\n\nContent.\n")
    assert len(changes) == 0
