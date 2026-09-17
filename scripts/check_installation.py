#!/usr/bin/env python3
"""Audit a consuming project's `.cursor/` + `doc/apm_config/` layout after running
`install_into_project.py` or `migrate_submodule_to_copy.py`.

This is a **read-only** checker — it never modifies or deletes anything, it only
reports discrepancies for the Human to act on.

Checks performed:
    1. Placement — every expected entry under `<target>/.cursor/` exists
       (`commands/`, `hooks/`, `hooks.json`, `rules/`, `skills/`, `TEMPLATE_VERSION`);
       `doc/apm_config/*.user.md` exist; no entry outside the expected copy set leaked
       into `.cursor/` (e.g. `apm_config/`, `scripts/`, `README.md`); `.cursor` is not
       (still) a git submodule; the legacy `DESIGN_RULES.md` / `doc/AGENT_MODELS.md`
       files are absent (expected only if `--config-layout v1.0.0` was used
       deliberately); no leftover bilingual `cs:` comments (stripping should have
       removed them).
    2. Length limits — `alwaysApply: true` rules <= 150 lines, `globs` rules <= 250
       lines, `skills/*/SKILL.md` <= 500 lines (see `rules/000-meta-rules-and-skills.mdc`
       for the source of these limits).
    3. Frontmatter sanity — every `rules/*.mdc` has a YAML frontmatter block with an
       `alwaysApply` key; and `alwaysApply: true` never appears together with a
       non-empty `globs` (the `globs` key has no effect once `alwaysApply` is true —
       it is dead configuration and a sign the wrong activation type was intended).

Not checked: dead links between documents (references to renamed/removed rules or
skills) — this would require a heuristic (regex over prose) with a real false-positive
rate on code blocks that merely illustrate a path, so it is deliberately left out rather
than shipped half-reliable.

Exit code: 1 if any discrepancy was found, 0 if the layout is clean.

Example:
    check_installation.py ~/dev/my-project
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

#: Line limits per rule/skill category — see rules/000-meta-rules-and-skills.mdc.
ALWAYS_APPLY_LIMIT = 150
GLOBS_LIMIT = 250
SKILL_LIMIT = 500

#: Top-level entries install_into_project.py copies into <target>/.cursor/.
EXPECTED_CURSOR_ENTRIES: tuple[str, ...] = ("commands", "hooks", "hooks.json", "rules", "skills")

#: Entries that must NEVER appear under <target>/.cursor/ — they are template-only
#: (development/meta files, never part of the copy set).
UNEXPECTED_CURSOR_ENTRIES: tuple[str, ...] = (
    "apm_config",
    "scripts",
    "doc",
    "README.md",
    "README.project_management.md",
    "LICENSE",
    "img",
    "CHANGELOG.md",
)

#: Config overrides install_into_project.py seeds under <target>/doc/apm_config/.
EXPECTED_APM_CONFIG_FILES: tuple[str, ...] = (
    "AGENT_MODELS.user.md",
    "DESIGN_RULES.user.md",
    "LANGUAGE.user.md",
)

#: Legacy (pre-v1.1.0) config paths that should be removed once migrated.
LEGACY_PATHS: tuple[str, ...] = ("DESIGN_RULES.md", "doc/AGENT_MODELS.md")

#: File suffixes checked for leaked bilingual "cs:" comments (should have been
#: stripped on copy — see scripts/lib/strip_comments.py).
_CHECKED_SUFFIXES: tuple[str, ...] = (".mdc", ".md", ".sh", ".py")
_LEAKED_COMMENT_PATTERN = re.compile(r"<!--\s*cs\s*:|^\s*#\s*cs\s*:", re.MULTILINE)


class Status:
    """Severity levels used in a `CheckResult` — plain constants, not an Enum, so they
    format directly as fixed-width strings in the CLI report.
    """

    OK = "OK"
    WARNING = "WARNING"
    VIOLATION = "VIOLATION"
    MISSING = "MISSING"


@dataclass(frozen=True)
class CheckResult:
    """One reported finding: a label identifying what was checked, its status, and an
    optional human-readable detail explaining a non-OK status.
    """

    status: str
    label: str
    detail: str = ""

    def is_problem(self) -> bool:
        """Return True if this result represents a discrepancy (any non-OK status)."""
        return self.status != Status.OK


class InstallationChecker:
    """Read-only auditor for a consuming project's `.cursor/` + `doc/apm_config/`
    layout. Every method only reads the filesystem — nothing is ever written or
    deleted; see the module docstring for the full list of checks performed.
    """

    def __init__(self, target: Path) -> None:
        """Args:
            target: Root of the consuming project to audit (must already exist).
        """
        self._target = target
        self._cursor_dir = target / ".cursor"
        self._apm_config_dir = target / "doc" / "apm_config"

    def run(self) -> list[CheckResult]:
        """Run every check and return all findings (OK and non-OK) in report order."""
        results: list[CheckResult] = []
        results.extend(self._check_placement())
        results.extend(self._check_lengths())
        results.extend(self._check_rule_frontmatter())
        return results

    def _check_placement(self) -> list[CheckResult]:
        results = [self._check_entry_exists(entry) for entry in EXPECTED_CURSOR_ENTRIES]
        results.append(self._check_entry_exists("TEMPLATE_VERSION"))
        results.extend(self._check_no_unexpected_entries())
        results.extend(
            self._check_apm_config_file(name) for name in EXPECTED_APM_CONFIG_FILES
        )
        results.append(self._check_not_a_submodule())
        results.extend(self._check_legacy_files_removed())
        results.extend(self._check_no_leaked_comments())
        return results

    def _check_entry_exists(self, name: str) -> CheckResult:
        path = self._cursor_dir / name
        if path.exists():
            return CheckResult(Status.OK, f".cursor/{name}")
        return CheckResult(Status.MISSING, f".cursor/{name}", "expected entry not found")

    def _check_no_unexpected_entries(self) -> list[CheckResult]:
        if not self._cursor_dir.is_dir():
            return []
        allowed = set(EXPECTED_CURSOR_ENTRIES) | {"TEMPLATE_VERSION"}
        results = []
        for entry in sorted(self._cursor_dir.iterdir()):
            if entry.name in allowed:
                continue
            severity = Status.VIOLATION if entry.name in UNEXPECTED_CURSOR_ENTRIES else Status.WARNING
            results.append(
                CheckResult(
                    severity,
                    f".cursor/{entry.name} not expected",
                    "not part of the standard copy set — should not be under .cursor/",
                )
            )
        return results

    def _check_apm_config_file(self, name: str) -> CheckResult:
        path = self._apm_config_dir / name
        if path.is_file():
            return CheckResult(Status.OK, f"doc/apm_config/{name}")
        return CheckResult(Status.MISSING, f"doc/apm_config/{name}", "config override not seeded")

    def _check_not_a_submodule(self) -> CheckResult:
        git_marker = self._cursor_dir / ".git"
        if git_marker.exists():
            return CheckResult(
                Status.VIOLATION,
                ".cursor is not a git submodule",
                f"found {git_marker} — .cursor is still (or again) a submodule checkout",
            )
        gitmodules = self._target / ".gitmodules"
        if gitmodules.is_file() and ".cursor" in gitmodules.read_text(encoding="utf-8"):
            return CheckResult(
                Status.WARNING,
                ".cursor is not a git submodule",
                f"{gitmodules} still references a '.cursor' submodule entry",
            )
        return CheckResult(Status.OK, ".cursor is not a git submodule")

    def _check_legacy_files_removed(self) -> list[CheckResult]:
        results = []
        for relative in LEGACY_PATHS:
            path = self._target / relative
            if path.exists():
                results.append(
                    CheckResult(
                        Status.WARNING,
                        f"legacy {relative} absent",
                        f"{path} still exists — redundant once its content is migrated "
                        "into doc/apm_config/*.user.md; expected only if "
                        "--config-layout v1.0.0 is used deliberately for legacy tooling",
                    )
                )
            else:
                results.append(CheckResult(Status.OK, f"legacy {relative} absent"))
        return results

    def _check_no_leaked_comments(self) -> list[CheckResult]:
        if not self._cursor_dir.is_dir():
            return []
        results = []
        for path in sorted(self._cursor_dir.rglob("*")):
            if not path.is_file() or path.suffix not in _CHECKED_SUFFIXES:
                continue
            if "templates" in path.relative_to(self._target).parts:
                # Skill-shipped project deliverables (e.g. project-init's GLOSSARY.md /
                # DECISIONS.md) are intentionally left bilingual — see
                # scripts/lib/installer.py's matching exclusion.
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            match = _LEAKED_COMMENT_PATTERN.search(text)
            if match:
                line_no = text.count("\n", 0, match.start()) + 1
                results.append(
                    CheckResult(
                        Status.VIOLATION,
                        f"no leaked 'cs:' comment in {path.relative_to(self._target)}",
                        f"line {line_no} — comment stripping may have failed",
                    )
                )
        if not results:
            results.append(CheckResult(Status.OK, "no leaked 'cs:' comments under .cursor/"))
        return results

    def _check_lengths(self) -> list[CheckResult]:
        results = []
        rules_dir = self._cursor_dir / "rules"
        if rules_dir.is_dir():
            results.extend(self._check_rule_length(path) for path in sorted(rules_dir.glob("*.mdc")))
        skills_dir = self._cursor_dir / "skills"
        if skills_dir.is_dir():
            results.extend(
                self._check_line_limit(path, SKILL_LIMIT, "skill")
                for path in sorted(skills_dir.glob("*/SKILL.md"))
            )
        return results

    def _check_rule_frontmatter(self) -> list[CheckResult]:
        """Every rule must declare `alwaysApply`, and never combine it (`true`) with a
        non-empty `globs` — that combination is dead configuration (see module docstring).
        """
        rules_dir = self._cursor_dir / "rules"
        if not rules_dir.is_dir():
            return []
        results = []
        for path in sorted(rules_dir.glob("*.mdc")):
            text = path.read_text(encoding="utf-8", errors="replace")
            frontmatter = _parse_frontmatter(text)
            label = str(path.relative_to(self._target))
            if "alwaysApply" not in frontmatter:
                results.append(
                    CheckResult(Status.VIOLATION, label, "missing 'alwaysApply' key in frontmatter")
                )
                continue
            always_apply = frontmatter.get("alwaysApply", "").strip().lower() == "true"
            has_globs = bool(frontmatter.get("globs", "").strip())
            if always_apply and has_globs:
                results.append(
                    CheckResult(
                        Status.VIOLATION,
                        f"{label} alwaysApply+globs conflict",
                        "globs has no effect once alwaysApply is true — remove one",
                    )
                )
            else:
                results.append(CheckResult(Status.OK, f"{label} frontmatter"))
        return results

    def _check_rule_length(self, path: Path) -> CheckResult:
        text = path.read_text(encoding="utf-8", errors="replace")
        frontmatter = _parse_frontmatter(text)
        always_apply = frontmatter.get("alwaysApply", "").strip().lower() == "true"
        has_globs = bool(frontmatter.get("globs", "").strip())
        if always_apply:
            return self._check_line_limit(path, ALWAYS_APPLY_LIMIT, "alwaysApply", text)
        if has_globs:
            return self._check_line_limit(path, GLOBS_LIMIT, "globs", text)
        line_count = len(text.splitlines())
        label = f"{path.relative_to(self._target)} (description-only, {line_count} lines, no limit)"
        return CheckResult(Status.OK, label)

    def _check_line_limit(
        self, path: Path, limit: int, category: str, text: str | None = None
    ) -> CheckResult:
        text = text if text is not None else path.read_text(encoding="utf-8", errors="replace")
        line_count = len(text.splitlines())
        label = f"{path.relative_to(self._target)} ({category}, {line_count}/{limit} lines)"
        if line_count > limit:
            return CheckResult(Status.VIOLATION, label, f"exceeds {category} limit of {limit} lines")
        return CheckResult(Status.OK, label)


def _parse_frontmatter(text: str) -> dict[str, str]:
    """Parse a minimal YAML frontmatter block delimited by leading `---` markers.

    Args:
        text: Full file content.

    Returns:
        A flat mapping of top-level frontmatter keys to their raw string values
        (quotes not stripped). Empty if the file has no frontmatter block.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    frontmatter: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            key, _, value = line.partition(":")
            frontmatter[key.strip()] = value.strip()
    return frontmatter


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for this CLI.

    Returns:
        A configured `argparse.ArgumentParser` (provides `-h`/`--help` automatically).
    """
    parser = argparse.ArgumentParser(
        prog="check_installation.py",
        description=(
            "Read-only audit of a consuming project's .cursor/ and doc/apm_config/ "
            "layout after install_into_project.py or migrate_submodule_to_copy.py. "
            "Reports discrepancies; fixes nothing."
        ),
        epilog="Example:\n  check_installation.py ~/dev/my-project\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "target",
        type=Path,
        help="Path to the consuming project's root directory (must already exist).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entry point.

    Args:
        argv: Command-line arguments (excluding the program name); defaults to
            `sys.argv[1:]` when None.

    Returns:
        Process exit code: 1 if any discrepancy was found, 0 if the layout is clean.
    """
    args = build_parser().parse_args(argv)
    target = args.target.resolve()
    if not target.is_dir():
        print(f"error: target path does not exist or is not a directory: {target}", file=sys.stderr)
        return 1

    results = InstallationChecker(target).run()

    for result in results:
        line = f"{result.status:9s} {result.label}"
        if result.detail:
            line += f"  \u2014 {result.detail}"
        print(line)

    problems = [result for result in results if result.is_problem()]
    print()
    if problems:
        suffix = "y" if len(problems) == 1 else "ies"
        print(f"{len(problems)} discrepanc{suffix} found in {target}.")
        return 1
    print(f"No discrepancies found in {target}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
