#!/usr/bin/env python3
"""Machine enforcement of the contracts this rule set declares about itself.

Every check here is referenced from a contract in ``doc/intent/nodes``. Cursor rule
files use folded YAML scalars, which the intent parser deliberately rejects, so the
front matter is inspected line by line instead.

Usage:
    python3 tools/checks/template_checks.py [--root .]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ALWAYS_APPLY_LIMIT = 150
SCOPED_RULE_LIMIT = 250
SKILL_LIMIT = 500

LINK_PATTERN = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SKIP_LINK_PREFIXES = ("http://", "https://", "mailto:", "#")


class Findings:
    def __init__(self) -> None:
        self.errors: list[str] = []

    def fail(self, where: Path, message: str) -> None:
        self.errors.append(f"{where}: {message}")


def read_front_matter(path: Path) -> list[str] | None:
    """Return the raw front matter lines, or ``None`` when the block is absent."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return lines[1:index]
    return None


def has_key(front: list[str], key: str) -> bool:
    return any(re.match(rf"^{key}\s*:", line) for line in front)


def value_of(front: list[str], key: str) -> str:
    for line in front:
        match = re.match(rf"^{key}\s*:\s*(.*)$", line)
        if match:
            return match.group(1).strip()
    return ""


def check_rules(root: Path, findings: Findings) -> None:
    """Rule files declare their activation and stay within their size budget."""
    rules_dir = root / "rules"
    if not rules_dir.is_dir():
        findings.fail(rules_dir, "rules directory is missing")
        return
    for path in sorted(rules_dir.glob("*.mdc")):
        front = read_front_matter(path)
        if front is None:
            findings.fail(path, "missing '---' front matter block")
            continue
        always = value_of(front, "alwaysApply") == "true"
        if not always and not has_key(front, "description") and not has_key(front, "globs"):
            findings.fail(path, "needs a description, globs, or alwaysApply: true")
        total = len(path.read_text(encoding="utf-8").splitlines())
        limit = ALWAYS_APPLY_LIMIT if always else SCOPED_RULE_LIMIT
        if total > limit:
            kind = "alwaysApply" if always else "scoped"
            findings.fail(path, f"{total} lines exceeds the {kind} limit of {limit}")


def check_skills(root: Path, findings: Findings) -> None:
    """Every skill is discoverable: it declares a name and a description."""
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        findings.fail(skills_dir, "skills directory is missing")
        return
    for directory in sorted(item for item in skills_dir.iterdir() if item.is_dir()):
        path = directory / "SKILL.md"
        if not path.exists():
            findings.fail(directory, "skill directory without SKILL.md")
            continue
        front = read_front_matter(path)
        if front is None:
            findings.fail(path, "missing '---' front matter block")
            continue
        if not has_key(front, "name"):
            findings.fail(path, "front matter is missing 'name'")
        if not has_key(front, "description"):
            findings.fail(path, "front matter is missing 'description'")
        total = len(path.read_text(encoding="utf-8").splitlines())
        if total > SKILL_LIMIT:
            findings.fail(path, f"{total} lines exceeds the skill limit of {SKILL_LIMIT}")


def strip_code_blocks(text: str) -> str:
    """Drop fenced code blocks: links inside them are illustrations, not references."""
    kept: list[str] = []
    inside = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            inside = not inside
            continue
        if not inside:
            kept.append(line)
    return "\n".join(kept)


def check_links(root: Path, findings: Findings) -> None:
    """Relative links inside rules and skills point at files that exist."""
    targets = [*(root / "rules").glob("*.mdc"), *(root / "skills").glob("*/SKILL.md")]
    for path in sorted(targets):
        prose = strip_code_blocks(path.read_text(encoding="utf-8"))
        for link in LINK_PATTERN.findall(prose):
            target = link.split("#", 1)[0].strip()
            if not target or target.startswith(SKIP_LINK_PREFIXES):
                continue
            if target.startswith("<") and target.endswith(">"):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                findings.fail(path, f"broken link: {target}")


def check_symlinks(root: Path, findings: Findings) -> None:
    """Cursor discovers rules and skills through the .cursor symlinks."""
    for name in ("rules", "skills"):
        link = root / ".cursor" / name
        if not link.is_symlink():
            findings.fail(link, "expected a symlink so Cursor discovers this directory")
        elif not link.resolve().is_dir():
            findings.fail(link, "symlink does not resolve to a directory")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()

    findings = Findings()
    check_rules(root, findings)
    check_skills(root, findings)
    check_links(root, findings)
    check_symlinks(root, findings)

    for error in findings.errors:
        print(f"ERROR {error}")
    if findings.errors:
        print(f"\n{len(findings.errors)} template contract violation(s)")
        return 1
    print("template contracts satisfied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
