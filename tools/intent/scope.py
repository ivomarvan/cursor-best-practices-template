"""Scope guard: compare the working diff against the outputs declared in a plan.

This is the cheapest gate in the methodology and the only one that protects the
light-weight path, where no independent reviewer runs.
"""

from __future__ import annotations

import fnmatch
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from intent.miniyaml import YamlError, parse, split_front_matter
from intent.model import Tree

PLAN_FILENAMES = ("plan.md", "run.md")


@dataclass
class Declaration:
    outputs: list[str] = field(default_factory=list)
    incidental: list[str] = field(default_factory=list)
    source: str = ""

    def allowed(self) -> list[str]:
        return [*self.outputs, *self.incidental]


def load_declaration(run_dir: Path) -> Declaration:
    """Read declared outputs from the run's plan front matter."""
    for name in PLAN_FILENAMES:
        candidate = run_dir / name
        if not candidate.exists():
            continue
        try:
            front, _ = split_front_matter(candidate.read_text(encoding="utf-8"))
            data = parse(front)
        except YamlError as exc:
            raise ValueError(f"{candidate}: {exc}") from exc
        outputs = data.get("outputs") or []
        incidental = data.get("incidental") or []
        if not isinstance(outputs, list) or not isinstance(incidental, list):
            raise ValueError(f"{candidate}: 'outputs' and 'incidental' must be lists")
        return Declaration(
            outputs=[str(item) for item in outputs],
            incidental=[str(item) for item in incidental],
            source=candidate.name,
        )
    joined = " or ".join(PLAN_FILENAMES)
    raise FileNotFoundError(f"no {joined} with declared outputs in {run_dir}")


def changed_files(root: Path, base: str | None) -> list[str]:
    """List files changed in the working tree, optionally against a base ref."""
    command = ["git", "diff", "--name-only"]
    if base:
        command.append(base)
    tracked = subprocess.run(command, cwd=root, capture_output=True, text=True, check=False)
    if tracked.returncode != 0:
        raise RuntimeError(tracked.stderr.strip() or "git diff failed")
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    names = tracked.stdout.split() + untracked.stdout.split()
    return sorted(set(names))


def _matches(path: str, patterns: list[str]) -> bool:
    for pattern in patterns:
        normalised = pattern.rstrip("/")
        if path == normalised or fnmatch.fnmatch(path, pattern):
            return True
        if path.startswith(normalised + "/"):
            return True
    return False


def check_scope(
    tree: Tree, run_dir: Path, base: str | None = None, node_ids: list[str] | None = None
) -> tuple[list[str], Declaration]:
    """Return the files that were changed without being declared."""
    declaration = load_declaration(run_dir)
    allowed = declaration.allowed()
    run_relative = str(run_dir.relative_to(tree.root_dir))
    allowed.append(run_relative)
    for node_id in node_ids or []:
        node = tree.nodes.get(node_id)
        if node:
            allowed.extend(node.code_paths)
            allowed.extend(node.test_paths)
    violations = [
        path for path in changed_files(tree.root_dir, base) if not _matches(path, allowed)
    ]
    return violations, declaration
