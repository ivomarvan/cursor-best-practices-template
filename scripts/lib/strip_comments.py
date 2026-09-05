#!/usr/bin/env python3
"""Strip bilingual annotation comments from template source files.

The template's rules and skills carry bilingual comments (see
`rules/00-meta-rules-and-skills.mdc`) of the form `<!-- cs: ... -->` (Markdown/HTML,
possibly spanning multiple lines) and `# cs: ...` (YAML front matter / code blocks).
These comments exist purely to help a human maintainer read the template in their own
language; the English text next to them is the sole source of truth for the agent. This
script removes them so that a copy installed into a consuming project carries fewer
tokens, without touching illustrative example text that merely documents the comment
syntax itself (e.g. inside `00-meta-rules-and-skills.mdc`).

Usage:
    strip_comments.py [--lang-code cs] < input > output
    strip_comments.py [--lang-code cs] FILE1 [FILE2 ...]   # rewrite files in place
"""

import argparse
import re
import sys
from pathlib import Path


def _build_patterns(lang_code: str) -> tuple[re.Pattern[str], re.Pattern[str]]:
    """Build the HTML-comment and code-comment strip patterns for one lang code.

    Args:
        lang_code: The comment marker to strip, e.g. "cs" (matches `<!-- cs: ... -->`
            and `# cs: ...`). Only this exact marker is targeted — placeholder text such
            as `<lang-code>` used in documentation examples is never matched.

    Returns:
        A tuple (html_pattern, code_pattern) of compiled regexes.
    """
    escaped = re.escape(lang_code)

    # HTML/Markdown block comments: <!-- cs: ... --> may span multiple lines.
    # The lazy body (.*?) only stops at a "-->" that is immediately followed by an
    # actual newline or end-of-string. This deliberately skips a "-->" that appears
    # mid-line (e.g. inside example text illustrating the comment syntax itself), and
    # keeps scanning for the real closing delimiter instead of truncating early.
    html_pattern = re.compile(
        r"[ \t]*<!--[ \t]*" + escaped + r":.*?-->[ \t]*(?:\n|\Z)",
        re.DOTALL,
    )

    # YAML / code-style single-line comments: # cs: ...
    code_pattern = re.compile(
        r"^[ \t]*#[ \t]*" + escaped + r":.*(?:\n|\Z)",
        re.MULTILINE,
    )

    return html_pattern, code_pattern


def strip_comments(text: str, lang_code: str = "cs") -> str:
    """Remove `<!-- {lang_code}: ... -->` and `# {lang_code}: ...` comments from text.

    Args:
        text: Source file content.
        lang_code: The bilingual comment marker to strip (default: "cs").

    Returns:
        The text with matching comment lines/blocks removed (including their trailing
        newline, so no blank gap is left behind).
    """
    html_pattern, code_pattern = _build_patterns(lang_code)
    text = html_pattern.sub("", text)
    text = code_pattern.sub("", text)
    return text


def main() -> int:
    """CLI entry point: filter stdin→stdout, or rewrite files in place.

    Returns:
        Process exit code (0 on success).
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--lang-code",
        default="cs",
        help="Bilingual comment marker to strip, e.g. 'cs' (default: %(default)s).",
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Files to rewrite in place. If omitted, filters stdin to stdout.",
    )
    args = parser.parse_args()

    if not args.files:
        sys.stdout.write(strip_comments(sys.stdin.read(), args.lang_code))
        return 0

    for file_path in args.files:
        path = Path(file_path)
        original = path.read_text(encoding="utf-8")
        filtered = strip_comments(original, args.lang_code)
        if filtered != original:
            path.write_text(filtered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
