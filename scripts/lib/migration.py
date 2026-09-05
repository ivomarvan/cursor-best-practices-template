"""Helpers for migrating a submodule-based project to the copy-based installation
(see `scripts/migrate_submodule_to_copy.py`).
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

_LANGUAGE_NAME_ROW = re.compile(r"\|\s*`<communication-language>`\s*\|\s*(.+?)\s*\|\s*$", re.MULTILINE)
_LANGUAGE_CODE_ROW = re.compile(r"\|\s*`<lang-code>`\s*\|\s*`?([a-z]{2})`?\s*\|\s*$", re.MULTILINE)


def has_cursor_submodule_entry(target: Path) -> bool:
    """Return True if `target/.gitmodules` references a `.cursor` submodule."""
    gitmodules = target / ".gitmodules"
    if not gitmodules.is_file():
        return False
    return ".cursor" in gitmodules.read_text(encoding="utf-8")


def migrate_legacy_config_file(legacy_file: Path, new_file: Path) -> bool:
    """Move `legacy_file` content into `new_file`, unless `new_file` already exists.

    Returns:
        True if `new_file` was written, False if there was nothing to do (either the
        legacy file is missing, or the new file already exists and must not be
        overwritten).
    """
    if not legacy_file.is_file() or new_file.exists():
        return False
    new_file.parent.mkdir(parents=True, exist_ok=True)
    new_file.write_text(legacy_file.read_text(encoding="utf-8"), encoding="utf-8")
    return True


def is_dirty(git_dir: Path, relative_path: str) -> bool:
    """Return True if `relative_path` differs from HEAD inside the `git_dir` repo.

    Returns False (treated as "unmodified") if `git_dir` is not a git repository or
    `git` is unavailable — the caller falls back to seeding the default in that case.
    """
    try:
        result = subprocess.run(
            ["git", "-C", str(git_dir), "diff", "--quiet", "--", relative_path],
            capture_output=True,
        )
    except FileNotFoundError:
        return False
    return result.returncode != 0


def extract_language_setting(language_file: Path) -> tuple[str, str]:
    """Parse the (pre-v1.1.0) Active Settings table for language name + code.

    Args:
        language_file: A `rules/00-communication-language.mdc` file that was locally
            hand-edited to change the active language (dirty relative to the pinned
            submodule commit).

    Returns:
        A `(language_name, lang_code)` tuple. Falls back to `("English", "en")` for
        whichever field could not be parsed.
    """
    text = language_file.read_text(encoding="utf-8")
    name_match = _LANGUAGE_NAME_ROW.search(text)
    code_match = _LANGUAGE_CODE_ROW.search(text)
    language_name = name_match.group(1) if name_match else "English"
    lang_code = code_match.group(1) if code_match else "en"
    return language_name, lang_code


def write_language_override(target_file: Path, language_name: str, lang_code: str) -> None:
    """Write a `LANGUAGE.user.md` override migrated from a submodule hand-edit."""
    target_file.parent.mkdir(parents=True, exist_ok=True)
    target_file.write_text(
        "# Communication Language — Project Override\n\n"
        "Migrated from a locally-modified `.cursor/rules/00-communication-language.mdc` "
        "(submodule installation).\n\n"
        "## Active Setting\n\n"
        "| Parameter | Value |\n"
        "|-----|----|\n"
        f"| `<communication-language>` | {language_name} |\n"
        f"| `<lang-code>` | `{lang_code}` |\n",
        encoding="utf-8",
    )


def deregister_submodule_commands(target: Path) -> str:
    """Return the (unexecuted) shell commands needed to deregister the .cursor submodule.

    These are structural git operations left for the Human to run explicitly — see
    `rules/02-git.mdc`.

    IMPORTANT: `git submodule deinit -f .cursor` empties `<target>/.cursor/` regardless
    of what is currently in it — including the plain-copy content this script just
    wrote. `.cursor/` must therefore be regenerated one more time, *after* deinit, via
    `install_into_project.py` — this is included as the final command below.
    """
    return (
        f'  cd "{target}"\n'
        "  git submodule deinit -f .cursor        # empties .cursor/ — this is expected\n"
        "  git rm -f .cursor\n"
        "  rm -rf .git/modules/.cursor\n"
        "  python3 <template-root>/scripts/install_into_project.py .   # regenerate .cursor/\n"
        "  git add .gitmodules .cursor doc/apm_config\n"
        "  # review with: git status / git diff --staged\n"
        "  # commit only when you are ready (no automatic commit is performed here)\n"
    )
