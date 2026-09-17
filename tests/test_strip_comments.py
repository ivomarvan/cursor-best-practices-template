"""Tests for `scripts/lib/strip_comments.py`."""

from __future__ import annotations

from lib.strip_comments import strip_comments


def test_strip_single_line_html_comment_removes_line() -> None:
    text = "# Title\n<!-- cs: Nadpis -->\n\nBody.\n"
    assert strip_comments(text) == "# Title\n\nBody.\n"


def test_strip_indented_html_comment_keeps_bullet() -> None:
    text = "- Bullet in English.\n  <!-- cs: Odrážka česky. -->\n- Next.\n"
    assert strip_comments(text) == "- Bullet in English.\n- Next.\n"


def test_strip_multiline_html_comment_removes_whole_block() -> None:
    text = "Para.\n<!-- cs: první řádek\n     druhý řádek\n     třetí -->\nAfter.\n"
    assert strip_comments(text) == "Para.\nAfter.\n"


def test_strip_yaml_hash_comment() -> None:
    text = "---\nalwaysApply: true\n# cs: platí vždy\n---\n"
    assert strip_comments(text) == "---\nalwaysApply: true\n---\n"


def test_strip_leaves_other_lang_codes_untouched() -> None:
    text = "Text.\n<!-- de: Deutsch -->\n<!-- cs: česky -->\n"
    assert strip_comments(text, lang_code="cs") == "Text.\n<!-- de: Deutsch -->\n"


def test_strip_leaves_placeholder_syntax_examples_untouched() -> None:
    # Documentation of the convention itself (000-meta-rules-and-skills.mdc) uses the
    # placeholder `<lang-code>` — that must survive, only the concrete marker is stripped.
    text = "Prefix `<!-- <lang-code>: ... -->` (or `# <lang-code>: ...`).\n"
    assert strip_comments(text) == text


def test_strip_leaves_mid_line_arrow_example_untouched() -> None:
    # A "-->" that is not at end of line belongs to illustrative text, not a comment.
    text = "Comments look like `<!-- cs: ... -->` in Markdown.\n"
    assert strip_comments(text) == text


def test_strip_is_idempotent() -> None:
    text = "A\n<!-- cs: a -->\nB\n# cs: b\n"
    once = strip_comments(text)
    assert strip_comments(once) == once
