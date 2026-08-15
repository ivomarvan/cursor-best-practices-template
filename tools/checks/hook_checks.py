#!/usr/bin/env python3
"""Machine enforcement of the contracts declared about the git hooks.

The commit-msg hook is the only thing standing between an agent-authored commit and a
history polluted with tool attribution, so its behaviour is checked rather than trusted.

Usage:
    python3 tools/checks/hook_checks.py [--root .]
"""

from __future__ import annotations

import argparse
import os
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

SAMPLE_MESSAGE = """feat(db): enforce unique user_id

Intent: i0042
Run: 20260815-1328-demo-a7

Co-authored-by: Cursor <cursoragent@cursor.com>


"""


def check_executable(root: Path) -> list[str]:
    errors: list[str] = []
    for relative in ("hooks/git/commit-msg", "hooks/session-start.sh"):
        path = root / relative
        if not path.exists():
            errors.append(f"{relative}: missing")
            continue
        if not path.stat().st_mode & stat.S_IXUSR:
            errors.append(f"{relative}: not executable")
    return errors


def check_commit_msg_strips_attribution(root: Path) -> list[str]:
    hook = root / "hooks/git/commit-msg"
    if not hook.exists():
        return ["hooks/git/commit-msg: missing"]
    with tempfile.TemporaryDirectory() as tmp:
        message_file = Path(tmp) / "COMMIT_EDITMSG"
        message_file.write_text(SAMPLE_MESSAGE, encoding="utf-8")
        result = subprocess.run(
            ["bash", str(hook), str(message_file)],
            capture_output=True,
            text=True,
            check=False,
            env={**os.environ, "LC_ALL": "C"},
        )
        if result.returncode != 0:
            return [f"hooks/git/commit-msg: exited {result.returncode}: {result.stderr.strip()}"]
        cleaned = message_file.read_text(encoding="utf-8")

    errors: list[str] = []
    if "Co-authored-by: Cursor" in cleaned or "cursoragent@cursor.com" in cleaned:
        errors.append("hooks/git/commit-msg: attribution survived the hook")
    if "Intent: i0042" not in cleaned or "feat(db): enforce unique user_id" not in cleaned:
        errors.append("hooks/git/commit-msg: the hook removed content it should keep")
    if cleaned.endswith("\n\n"):
        errors.append("hooks/git/commit-msg: trailing blank lines were not trimmed")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()

    errors = check_executable(root) + check_commit_msg_strips_attribution(root)
    for error in errors:
        print(f"ERROR {error}")
    if errors:
        print(f"\n{len(errors)} hook contract violation(s)")
        return 1
    print("hook contracts satisfied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
