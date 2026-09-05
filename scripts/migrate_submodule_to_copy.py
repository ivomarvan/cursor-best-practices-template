#!/usr/bin/env python3
"""Migrate a project from the git-submodule installation method to the plain-copy
method (install_into_project.py), preserving any existing project configuration.

What it does automatically:
    1. Detects a `.cursor` git submodule entry in the target project.
    2. Moves legacy config content (root DESIGN_RULES.md, doc/AGENT_MODELS.md) into
       doc/apm_config/{DESIGN_RULES,AGENT_MODELS}.user.md, if not already migrated.
    3. Detects a locally-modified (dirty) rules/00-communication-language.mdc inside
       the submodule and, if found, extracts its active language into
       doc/apm_config/LANGUAGE.user.md.
    4. Runs the same logic as install_into_project.py to (re)generate .cursor/ and
       seed any remaining missing *.user.md files (idempotent — never overwrites
       what step 2/3 already wrote).

What it does NOT do (prints the commands instead, for the Human to run explicitly):
    - Deregistering the git submodule (`git submodule deinit`, `.gitmodules` edit,
      `git rm --cached .cursor`, `rm -rf .git/modules/.cursor`).
    - Staging/committing the new plain .cursor/ content.
These are structural git operations and are intentionally left to an explicit Human
decision — see rules/02-git.mdc.

Note: `git submodule deinit -f .cursor` empties .cursor/ regardless of what this script
just wrote there. The printed command block therefore ends with a final
install_into_project.py re-run, which regenerates .cursor/ one last time, now safely
outside of any submodule registration.

Example:
    migrate_submodule_to_copy.py ~/dev/my-project --lang cs
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.installer import TemplateInstallError, TemplateInstaller  # noqa: E402
from lib.migration import (  # noqa: E402
    deregister_submodule_commands,
    extract_language_setting,
    has_cursor_submodule_entry,
    is_dirty,
    migrate_legacy_config_file,
    write_language_override,
)


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for this CLI.

    Returns:
        A configured `argparse.ArgumentParser` (provides `-h`/`--help` automatically).
    """
    parser = argparse.ArgumentParser(
        prog="migrate_submodule_to_copy.py",
        description=(
            "Migrate a submodule-based project to the plain-copy installation method, "
            "preserving existing DESIGN_RULES.md / AGENT_MODELS.md / language overrides."
        ),
        epilog="Example:\n  migrate_submodule_to_copy.py ~/dev/my-project --lang cs\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "target",
        type=Path,
        help="Path to the consuming project's root directory (must already exist).",
    )
    parser.add_argument(
        "--lang",
        default="en",
        metavar="CODE",
        help=(
            "Fallback language for LANGUAGE.user.md if no locally-modified setting is "
            "detected in the submodule (default: %(default)s)."
        ),
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entry point.

    Args:
        argv: Command-line arguments (excluding the program name); defaults to
            `sys.argv[1:]` when None.

    Returns:
        Process exit code (0 on success, 1 on error).
    """
    args = build_parser().parse_args(argv)
    target = args.target.resolve()
    if not target.is_dir():
        print(f"error: target path does not exist or is not a directory: {target}", file=sys.stderr)
        return 1

    if not has_cursor_submodule_entry(target):
        print(
            f"warning: no '.cursor' submodule entry found in {target}/.gitmodules — "
            "continuing anyway.",
            file=sys.stderr,
        )

    apm_config_dir = target / "doc" / "apm_config"
    apm_config_dir.mkdir(parents=True, exist_ok=True)

    if migrate_legacy_config_file(target / "DESIGN_RULES.md", apm_config_dir / "DESIGN_RULES.user.md"):
        print(f"migrated {target / 'DESIGN_RULES.md'} -> {apm_config_dir / 'DESIGN_RULES.user.md'}")

    if migrate_legacy_config_file(
        target / "doc" / "AGENT_MODELS.md", apm_config_dir / "AGENT_MODELS.user.md"
    ):
        print(f"migrated {target / 'doc' / 'AGENT_MODELS.md'} -> {apm_config_dir / 'AGENT_MODELS.user.md'}")

    submodule_lang_file = target / ".cursor" / "rules" / "00-communication-language.mdc"
    new_language_file = apm_config_dir / "LANGUAGE.user.md"
    if submodule_lang_file.is_file() and not new_language_file.exists():
        if is_dirty(target / ".cursor", "rules/00-communication-language.mdc"):
            print("detected locally-modified 00-communication-language.mdc — extracting active setting")
            language_name, lang_code = extract_language_setting(submodule_lang_file)
            write_language_override(new_language_file, language_name, lang_code)
            print(f"migrated language setting -> {new_language_file}")

    template_root = Path(__file__).resolve().parent.parent
    installer = TemplateInstaller(template_root)
    try:
        report = installer.install(target, lang_code=args.lang)
    except TemplateInstallError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    for path in report.created:
        print(f"create {path}")
    for path in report.kept:
        print(f"keep   {path} (already exists, not overwritten)")

    print()
    print(
        "Migration content is ready. The submodule itself is still registered — "
        "deregister and stage it manually (structural git operation, requires your "
        "explicit confirmation).\n"
    )
    print(
        "WARNING: 'git submodule deinit -f .cursor' below empties .cursor/ again, "
        "including the plain-copy content just written above. That is expected — the "
        "command block ends with a final install_into_project.py re-run to regenerate "
        "it, now safely outside of any submodule registration:\n"
    )
    commands = deregister_submodule_commands(target).replace(
        "<template-root>", str(template_root)
    )
    print(commands)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
