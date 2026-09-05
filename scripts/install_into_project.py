#!/usr/bin/env python3
"""Install (or re-install) this template into a consuming project as a plain, filtered
copy — the non-submodule alternative described in README.md ("Option C").

What it does:
    1. Wipes <target>/.cursor/ entirely and rewrites it from commands/, hooks/,
       hooks.json, rules/, skills/ — with bilingual "cs:" comments stripped.
    2. Writes <target>/.cursor/TEMPLATE_VERSION with the source version + timestamp.
    3. Seeds <target>/doc/apm_config/{AGENT_MODELS,DESIGN_RULES,LANGUAGE}.user.md from
       this template's apm_config/*.default.md — but ONLY if a user file does not exist
       yet (never overwrites a Human's existing configuration).

Hard rule this script enforces: .cursor/ in the target project is 100% generated.
Any override belongs in doc/apm_config/*.user.md — see rules/20-project-design-rules.mdc.

Examples:
    install_into_project.py ~/dev/my-project
    install_into_project.py ~/dev/my-project --lang cs
    install_into_project.py ~/dev/my-project --config-layout v1.0.0
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.installer import LEGACY_VERSION, TemplateInstallError, TemplateInstaller  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for this CLI.

    Returns:
        A configured `argparse.ArgumentParser` (provides `-h`/`--help` automatically).
    """
    parser = argparse.ArgumentParser(
        prog="install_into_project.py",
        description=(
            "Install this template into a consuming project's .cursor/ directory, "
            "stripping bilingual comments and seeding doc/apm_config/*.user.md."
        ),
        epilog=(
            "Examples:\n"
            "  install_into_project.py ~/dev/my-project\n"
            "  install_into_project.py ~/dev/my-project --lang cs\n"
        ),
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
            "Language to seed LANGUAGE.user.md with on first install (default: "
            "%(default)s). Known: en, cs, de — any other code is accepted verbatim. "
            "Ignored on re-install if the file already exists."
        ),
    )
    parser.add_argument(
        "--config-layout",
        default=None,
        metavar="VERSION",
        help=(
            "Config-file layout version (default: auto-detected template version). "
            f"'{LEGACY_VERSION}' additionally writes the pre-v1.1.0 fixed config paths "
            "(root DESIGN_RULES.md, doc/AGENT_MODELS.md), for external tooling that "
            "still expects them."
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
    template_root = Path(__file__).resolve().parent.parent
    installer = TemplateInstaller(template_root)

    try:
        target = args.target.resolve()
        report = installer.install(target, lang_code=args.lang, config_layout=args.config_layout)
    except TemplateInstallError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"Template root : {template_root}")
    print(f"Target project: {target}")
    print()
    for path in report.created:
        print(f"create {path}")
    for path in report.kept:
        print(f"keep   {path} (already exists, not overwritten)")
    print()
    print("Done. Remember:")
    print(f"  - Everything under {target / '.cursor'} is generated — never hand-edit it.")
    print(f"  - Configure this project only via {target / 'doc' / 'apm_config'}/*.user.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
