#!/usr/bin/env python3
"""Machine enforcement of the contracts declared about the git hooks.

The commit-msg hook is the only thing standing between an agent-authored commit and a
history polluted with tool attribution, so its behaviour is checked rather than trusted.

Usage:
    python3 tools/checks/hook_checks.py [--root .]
"""

from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

REQUIRED_HOOKS = ("hooks/git/commit-msg", "hooks/session-start.sh")

# Shared subject + Intent/Run trailers used by most cases; measured expected outputs
# come from the repaired commit-msg hook (byte-exact).
_BASE = "feat(db): enforce unique user_id\n\nIntent: i0005\nRun: 20260818-0853-cursor-audit-86\n"
_CLEAN = "feat(db): enforce unique user_id\n\nIntent: i0005\nRun: 20260818-0853-cursor-audit-86\n"


@dataclass(frozen=True)
class Case:
    name: str
    message: str
    expected: str


CASES: tuple[Case, ...] = (
    Case(
        "cursor_trailer",
        _BASE + "\nCo-authored-by: Cursor <cursoragent@cursor.com>\n",
        _CLEAN,
    ),
    Case(
        "cursor_agent_prefix",
        _BASE + "\nCo-authored-by: CursorAgent <bot@example.com>\n",
        _CLEAN,
    ),
    Case(
        "cursor_hyphen_bot",
        _BASE + "\nCo-authored-by: Cursor-bot <bot@example.com>\n",
        _CLEAN,
    ),
    Case(
        "cursor_xyz",
        _BASE + "\nCo-authored-by: CursorXYZ\n",
        _CLEAN,
    ),
    Case(
        "capitalised_key",
        _BASE + "\nCo-Authored-By: Cursor <bot@example.com>\n",
        _CLEAN,
    ),
    Case(
        "made_with",
        _BASE + "\nMade-with: Cursor\n",
        _CLEAN,
    ),
    Case(
        "generated_with",
        _BASE + "\nGenerated-with: Cursor 1.2\n",
        _CLEAN,
    ),
    Case(
        "signed_off_by_agent",
        _BASE + "\nSigned-off-by: Cursor Agent <cursoragent@cursor.com>\n",
        _CLEAN,
    ),
    Case(
        "human_co_author",
        _BASE + "\nCo-authored-by: Ivo Example <ivo@example.com>\n",
        _CLEAN + "\nCo-authored-by: Ivo Example <ivo@example.com>\n",
    ),
    Case(
        "body_quotes_the_address",
        (
            "feat(db): enforce unique user_id\n"
            "\n"
            "Never write Co-authored-by: Cursor <cursoragent@cursor.com> by hand.\n"
            "\n"
            "Intent: i0005\n"
            "Run: 20260818-0853-cursor-audit-86\n"
        ),
        (
            "feat(db): enforce unique user_id\n"
            "\n"
            "Never write Co-authored-by: Cursor <cursoragent@cursor.com> by hand.\n"
            "\n"
            "Intent: i0005\n"
            "Run: 20260818-0853-cursor-audit-86\n"
        ),
    ),
    Case(
        "subject_names_cursor",
        ("docs: Cursor attribution note\n\nIntent: i0005\nRun: 20260818-0853-cursor-audit-86\n"),
        ("docs: Cursor attribution note\n\nIntent: i0005\nRun: 20260818-0853-cursor-audit-86\n"),
    ),
    Case(
        "run_slug_contains_cursor",
        _BASE,
        _CLEAN,
    ),
    Case(
        "trailing_blank_lines",
        _BASE + "\n\n\n",
        _CLEAN,
    ),
    Case(
        "attribution_only",
        "Co-authored-by: Cursor <cursoragent@cursor.com>\n",
        "",
    ),
    # Address branch only: value does not start with Cursor, so the name branch misses it.
    Case(
        "address_only_trailer",
        _BASE + "\nReported-by: someone <cursoragent@cursor.com>\n",
        _CLEAN,
    ),
    # B2 — key forms git interpret-trailers accepts (or that the old unanchored address
    # grep removed); name/address grammar must be wide enough for all of them.
    Case(
        "space_before_colon",
        _BASE + "\nCo-authored-by : Cursor <cursoragent@cursor.com>\n",
        _CLEAN,
    ),
    Case(
        "digit_key_address",
        _BASE + "\n2fa-note: cursoragent@cursor.com\n",
        _CLEAN,
    ),
    Case(
        "underscore_key_address",
        _BASE + "\nCo_authored_by: Cursor <cursoragent@cursor.com>\n",
        _CLEAN,
    ),
    Case(
        "dot_key_address",
        _BASE + "\nco.authored.by: cursoragent@cursor.com\n",
        _CLEAN,
    ),
    # B3 — folded trailers (continuation lines belong to the preceding key).
    Case(
        "folded_space_continuation",
        (
            "feat(x): subject\n\nReason: body.\n\nIntent: i0005\n"
            "Co-authored-by:\n  Cursor <cursoragent@cursor.com>\n"
        ),
        "feat(x): subject\n\nReason: body.\n\nIntent: i0005\n",
    ),
    Case(
        "folded_tab_continuation",
        (
            "feat(x): subject\n\nReason: body.\n\nIntent: i0005\n"
            "Co-authored-by:\n\tCursor <cursoragent@cursor.com>\n"
        ),
        "feat(x): subject\n\nReason: body.\n\nIntent: i0005\n",
    ),
    Case(
        "folded_name_then_address",
        (
            "feat(x): subject\n\nReason: body.\n\nIntent: i0005\n"
            "Co-authored-by: Cursor\n  <cursoragent@cursor.com>\n"
        ),
        "feat(x): subject\n\nReason: body.\n\nIntent: i0005\n",
    ),
    Case(
        "folded_space_before_colon",
        (
            "feat(x): subject\n\nReason: body.\n\nIntent: i0005\n"
            "Co-authored-by :\n  Cursor <cursoragent@cursor.com>\n"
        ),
        "feat(x): subject\n\nReason: body.\n\nIntent: i0005\n",
    ),
    # Structural edges: subject only; mixed trailers; indented prose quote; CRLF.
    Case(
        "subject_only_no_trailer_block",
        "feat(db): enforce unique user_id\n",
        "feat(db): enforce unique user_id\n",
    ),
    Case(
        "mixed_attribution_and_legitimate_trailers",
        (
            "feat(db): enforce unique user_id\n\n"
            "Intent: i0005\n"
            "Run: 20260818-0853-cursor-audit-86\n"
            "Co-authored-by: Ivo Example <ivo@example.com>\n"
            "Co-authored-by: Cursor <cursoragent@cursor.com>\n"
        ),
        (
            "feat(db): enforce unique user_id\n\n"
            "Intent: i0005\n"
            "Run: 20260818-0853-cursor-audit-86\n"
            "Co-authored-by: Ivo Example <ivo@example.com>\n"
        ),
    ),
    Case(
        "indented_prose_quotes_attribution",
        (
            "feat(db): enforce unique user_id\n\n"
            "Note the form:\n"
            "  Co-authored-by: Cursor <cursoragent@cursor.com>\n"
            "in docs only.\n\n"
            "Intent: i0005\n"
            "Run: 20260818-0853-cursor-audit-86\n"
        ),
        (
            "feat(db): enforce unique user_id\n\n"
            "Note the form:\n"
            "  Co-authored-by: Cursor <cursoragent@cursor.com>\n"
            "in docs only.\n\n"
            "Intent: i0005\n"
            "Run: 20260818-0853-cursor-audit-86\n"
        ),
    ),
    Case(
        "crlf_line_endings",
        (
            "feat(db): enforce unique user_id\r\n\r\n"
            "Intent: i0005\r\n"
            "Run: 20260818-0853-cursor-audit-86\r\n"
            "Co-authored-by: Cursor <cursoragent@cursor.com>\r\n"
        ),
        _CLEAN,
    ),
    Case(
        "made_with_space_before_colon",
        _BASE + "\nMade-with : Cursor\n",
        _CLEAN,
    ),
    # Block boundary: the last raw paragraph is not the trailer block once git's own
    # cleanup (strip / whitespace / scissors) is anticipated. Each of these is only
    # reachable through a shape git itself produces or accepts, never through the hook.
    Case(
        "attribution_then_trailing_blank_line",
        _BASE + "\nCo-authored-by: Cursor <cursoragent@cursor.com>\n\n",
        _CLEAN,
    ),
    Case(
        "attribution_then_editor_comment_block",
        (
            _BASE
            + "\nCo-authored-by: Cursor <cursoragent@cursor.com>\n"
            + "\n"
            + "# Please enter the commit message for your changes. Lines starting\n"
            + "# with '#' will be ignored, and an empty message aborts the commit.\n"
            + "#\n"
            + "# On branch main\n"
        ),
        _CLEAN,
    ),
    Case(
        "attribution_then_scissors_and_diff",
        (
            _BASE
            + "\nCo-authored-by: Cursor <cursoragent@cursor.com>\n"
            + "\n"
            + "# Please enter the commit message for your changes. Lines starting\n"
            + "# with '#' will be ignored, and an empty message aborts the commit.\n"
            + "# ------------------------ >8 ------------------------\n"
            + "diff --git a/foo.py b/foo.py\n"
            + "index abc123..def456 100644\n"
            + "--- a/foo.py\n"
            + "+++ b/foo.py\n"
        ),
        _CLEAN,
    ),
    # Enforcer gaps found by mutation testing (see hooks/git/commit-msg for the code
    # each of these guards): the hook was already correct, only the check was mute.
    Case(
        "blank_separator_only_spaces",
        (
            "feat(db): enforce unique user_id\n"
            "   \n"
            "Intent: i0005\n"
            "Run: 20260818-0853-cursor-audit-86\n"
            "Co-authored-by: Cursor <cursoragent@cursor.com>\n"
        ),
        (
            "feat(db): enforce unique user_id\n"
            "   \n"
            "Intent: i0005\n"
            "Run: 20260818-0853-cursor-audit-86\n"
        ),
    ),
    Case(
        "address_on_continuation_non_by_with",
        _BASE + "\nNote:\n  see cursoragent@cursor.com\n",
        _CLEAN,
    ),
    Case(
        "orphan_continuation_with_address",
        _BASE + "\n  see cursoragent@cursor.com\n",
        _CLEAN,
    ),
    Case(
        "folded_join_requires_space",
        _BASE + "\nCo-authored-by: Cur\n  sor Smith <human@example.com>\n",
        _CLEAN + "\nCo-authored-by: Cur\n  sor Smith <human@example.com>\n",
    ),
)


def declared_hooks(root: Path) -> list[Path]:
    """Hooks named in hooks.json, paths relative to root after stripping ``.cursor/``."""
    config = root / "hooks.json"
    if not config.is_file():
        return []
    data = json.loads(config.read_text(encoding="utf-8"))
    found: list[Path] = []
    for entries in (data.get("hooks") or {}).values():
        for entry in entries:
            command = entry.get("command", "")
            if not command:
                continue
            relative = re.sub(r"^\.cursor/", "", command)
            found.append(root / relative)
    return found


def shipped_hooks(root: Path) -> list[Path]:
    """Every non-documentation file under hooks/, plus anything declared in hooks.json."""
    hooks_dir = root / "hooks"
    discovered: list[Path] = []
    if hooks_dir.is_dir():
        discovered = [
            path for path in hooks_dir.rglob("*") if path.is_file() and path.suffix != ".md"
        ]
    by_key = {path.resolve(): path for path in discovered}
    for path in declared_hooks(root):
        by_key.setdefault(path.resolve(), path)
    return sorted(by_key.values(), key=lambda path: str(path))


def check_executable(root: Path) -> list[str]:
    errors: list[str] = []
    if not (root / "hooks").is_dir():
        return ["hooks/: missing"]

    hooks = shipped_hooks(root)
    by_relative: dict[str, Path] = {}
    for path in hooks:
        try:
            relative = str(path.relative_to(root))
        except ValueError:
            relative = str(path)
        by_relative[relative] = path

    for required in REQUIRED_HOOKS:
        if required not in by_relative:
            errors.append(f"{required}: missing (required shipped hook)")

    for relative, path in sorted(by_relative.items()):
        if not path.exists():
            errors.append(f"{relative}: missing")
            continue
        if not path.stat().st_mode & stat.S_IXUSR:
            errors.append(f"{relative}: not executable")
    return errors


def _diff_message(expected: str, actual: str) -> str:
    diff = "".join(
        difflib.unified_diff(
            expected.splitlines(keepends=True),
            actual.splitlines(keepends=True),
            fromfile="expected",
            tofile="actual",
        )
    )
    if diff:
        return diff
    return f"expected={expected!r} actual={actual!r}"


def check_commit_msg_strips_attribution(root: Path) -> list[str]:
    hook = root / "hooks/git/commit-msg"
    if not hook.exists():
        return ["hooks/git/commit-msg: missing"]

    errors: list[str] = []
    for case in CASES:
        with tempfile.TemporaryDirectory() as tmp:
            message_file = Path(tmp) / "COMMIT_EDITMSG"
            # Bytes, not text: a text-mode write/read round-trip on some platforms
            # would translate "\r\n", hiding exactly the difference crlf_line_endings
            # exists to catch.
            message_file.write_bytes(case.message.encode("utf-8"))
            result = subprocess.run(
                ["bash", str(hook), str(message_file)],
                capture_output=True,
                text=True,
                check=False,
                env={**os.environ, "LC_ALL": "C"},
            )
            if result.returncode != 0:
                errors.append(
                    f"hooks/git/commit-msg: case '{case.name}': "
                    f"exited {result.returncode}: {result.stderr.strip()}"
                )
                continue
            cleaned = message_file.read_bytes()
            expected = case.expected.encode("utf-8")
            if cleaned != expected:
                errors.append(
                    f"hooks/git/commit-msg: case '{case.name}': output mismatch\n"
                    f"{_diff_message(case.expected, cleaned.decode('utf-8', errors='replace'))}"
                )
    return errors


def check_committed_mode(root: Path) -> tuple[list[str], str]:
    """Compare tracked shipped-hook modes in the git index against 100755."""
    try:
        toplevel = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return [], f"committed modes not verified: {root} is not the top of a git work tree"

    if toplevel.returncode != 0:
        return [], f"committed modes not verified: {root} is not the top of a git work tree"

    resolved_top = Path(toplevel.stdout.strip()).resolve()
    if resolved_top != root.resolve():
        return [], f"committed modes not verified: {root} is not the top of a git work tree"

    listed = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-s", "--", "hooks"],
        capture_output=True,
        text=True,
        check=False,
    )
    if listed.returncode != 0:
        return [f"git ls-files failed: {listed.stderr.strip()}"], "committed modes checked"

    index: dict[str, str] = {}
    for line in listed.stdout.splitlines():
        # format: <mode> <object> <stage>\t<path>
        if "\t" not in line:
            continue
        meta, path = line.split("\t", 1)
        mode = meta.split()[0]
        index[path] = mode

    errors: list[str] = []
    notes: list[str] = []
    for path in shipped_hooks(root):
        if not path.exists():
            continue
        relative = str(path.relative_to(root))
        if relative not in index:
            notes.append(f"{relative} untracked")
            continue
        if index[relative] != "100755":
            errors.append(f"{relative}: committed mode is {index[relative]}, expected 100755")

    note = "committed modes checked"
    if notes:
        note = f"committed modes checked ({', '.join(notes)} untracked)"
    return errors, note


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()

    mode_errors, mode_note = check_committed_mode(root)
    errors = check_executable(root) + check_commit_msg_strips_attribution(root) + mode_errors
    for error in errors:
        print(f"ERROR {error}")
    if errors:
        print(f"\n{len(errors)} hook contract violation(s)")
        return 1

    n = len([path for path in shipped_hooks(root) if path.exists()])
    m = len(CASES)
    print(f"hook contracts satisfied ({n} shipped hook(s), {m} message case(s); {mode_note})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
