#!/usr/bin/env python3
"""Migrate a project from the git-submodule installation method to the plain-copy
method (install_into_project.py), preserving any existing project configuration.

What it does automatically:
    1. Detects a `.cursor` git submodule entry in the target project.
    2. Copies legacy config content (root DESIGN_RULES.md, doc/AGENT_MODELS.md) into
       doc/apm_config/{DESIGN_RULES,AGENT_MODELS}.user.md, if not already migrated.
       The legacy files themselves are left in place — see the note below.
    3. Detects a locally-modified (dirty) rules/00-communication-language.mdc inside
       the (pre-rename) submodule and, if found, extracts its active language into
       doc/apm_config/LANGUAGE.user.md.
    4. Runs the same logic as install_into_project.py to (re)generate .cursor/ and
       seed any remaining missing *.user.md files (idempotent — never overwrites
       what step 2/3 already wrote).

What it does NOT do (prints the commands instead, for the Human to run explicitly):
    - Removing the now-redundant legacy config files (root DESIGN_RULES.md,
      doc/AGENT_MODELS.md) once their content has been copied into
      doc/apm_config/*.user.md.
    - Deregistering the git submodule (`git submodule deinit`, `.gitmodules` edit,
      `git rm --cached .cursor`, `rm -rf .git/modules/.cursor`).
    - Staging/committing the new plain .cursor/ content.
These are all destructive or structural git operations and are intentionally left to
an explicit Human decision — see rules/020-git.mdc and
rules/000-meta-rules-and-skills.mdc ("no deletion of config files without confirmation").

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

    legacy_files_to_remove: list[Path] = []

    legacy_design_rules = target / "DESIGN_RULES.md"
    if migrate_legacy_config_file(legacy_design_rules, apm_config_dir / "DESIGN_RULES.user.md"):
        print(f"migrated {legacy_design_rules} -> {apm_config_dir / 'DESIGN_RULES.user.md'}")
        legacy_files_to_remove.append(legacy_design_rules)

    legacy_agent_models = target / "doc" / "AGENT_MODELS.md"
    if migrate_legacy_config_file(legacy_agent_models, apm_config_dir / "AGENT_MODELS.user.md"):
        print(f"migrated {legacy_agent_models} -> {apm_config_dir / 'AGENT_MODELS.user.md'}")
        legacy_files_to_remove.append(legacy_agent_models)

    # Old, pre-rename filename: a submodule checkout predates the 000-*/010-*/... rename
    # done alongside this script, so it still has the old flat 00-*/01-*/... names.
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

    if legacy_files_to_remove:
        print()
        print(
            "The following legacy config files were copied into doc/apm_config/*.user.md "
            "above and are no longer read by the config resolution mechanism (see "
            "rules/200-project-design-rules.mdc). They are now redundant — remove them "
            "once you've confirmed the migrated content is correct:\n"
        )
        quoted_paths = " ".join(f'"{path}"' for path in legacy_files_to_remove)
        print(f"  git rm {quoted_paths}\n")

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
