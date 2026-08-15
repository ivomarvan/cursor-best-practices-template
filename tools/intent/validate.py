"""Machine rules V1–V10 of the intent tree.

Semantic axioms (A1–A6) are not checked here — they need a reader. Everything in
this module is deterministic and dependency-free.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from intent.generate import generated_is_current
from intent.model import (
    NODE_ID_PATTERN,
    RETIRED_DIRNAME,
    STATUS_VALUES,
    Node,
    Tree,
)

BODY_WARN_LINES = 120
BODY_ERROR_LINES = 200
REQUIRED_SECTIONS_ROOT = ("Meaning",)
REQUIRED_SECTIONS_CHILD = ("Refines", "Meaning")


@dataclass
class Finding:
    level: str  # "error" | "warning"
    code: str
    node: str
    message: str

    def format(self) -> str:
        mark = "ERROR  " if self.level == "error" else "warning"
        return f"{mark} {self.code} {self.node}: {self.message}"


class _Collector:
    def __init__(self) -> None:
        self.findings: list[Finding] = []

    def error(self, code: str, node: str, message: str) -> None:
        self.findings.append(Finding("error", code, node, message))

    def warn(self, code: str, node: str, message: str) -> None:
        self.findings.append(Finding("warning", code, node, message))


def _check_identity(tree: Tree, out: _Collector) -> None:
    for node in tree.nodes.values():
        if not NODE_ID_PATTERN.match(node.id):
            out.error("V1", node.id, "id must match 'i' followed by at least four digits")
        if node.id not in tree.registry.issued:
            out.error("V1", node.id, f"id is not issued in {tree.registry.source.name}")
        elif tree.registry.is_retired(node.id):
            out.error("V1", node.id, "id is marked retired in the registry but the node is active")
        if not node.slug:
            out.error("V1", node.id, "missing slug")
        if not node.title:
            out.error("V1", node.id, "missing title")
        if node.status not in STATUS_VALUES:
            out.error("V1", node.id, f"status must be one of {', '.join(STATUS_VALUES)}")
        if node.source is not None:
            expected = f"{node.id}-{node.slug}.md"
            if node.source.name != expected:
                out.error("V1", node.id, f"file should be named {expected}")
        if node.unknown_fields:
            out.warn("V1", node.id, f"unknown fields: {', '.join(node.unknown_fields)}")
        serial = int(node.id[1:]) if node.id[1:].isdigit() else -1
        if serial >= tree.registry.next_serial:
            out.error("V1", node.id, "id is at or beyond registry next_serial")


def _check_structure(tree: Tree, out: _Collector) -> None:
    roots = tree.roots()
    if not roots:
        out.error("V2", "-", "the tree has no root (no node with 'parent: null')")
    elif len(roots) > 1:
        joined = ", ".join(node.id for node in roots)
        out.error("V2", "-", f"the tree must have exactly one root, found: {joined}")

    for node in tree.nodes.values():
        if node.parent is None:
            continue
        parent = tree.nodes.get(node.parent)
        if parent is None:
            out.error("V2", node.id, f"parent {node.parent} does not exist")
            continue
        if parent.status != "current" and node.status == "current":
            out.error("V2", node.id, f"parent {parent.id} is '{parent.status}', not 'current'")
        if tree.has_cycle(node.id):
            out.error("V2", node.id, "refinement edges form a cycle")


def _check_edges(tree: Tree, out: _Collector) -> None:
    for node in tree.nodes.values():
        for target in node.uses:
            if target not in tree.nodes:
                out.error("V3", node.id, f"uses unknown node {target}")
            elif target == node.id:
                out.error("V3", node.id, "uses itself")
        for target in node.talks_to:
            if target not in tree.nodes:
                out.error("V3", node.id, f"talks_to unknown node {target}")

    colour: dict[str, int] = {}

    def visit(node_id: str, trail: list[str]) -> None:
        colour[node_id] = 1
        for target in tree.nodes[node_id].uses if node_id in tree.nodes else []:
            if target not in tree.nodes:
                continue
            state = colour.get(target, 0)
            if state == 1:
                cycle = " -> ".join([*trail, node_id, target])
                out.error("V3", node_id, f"'uses' edges form a cycle: {cycle}")
            elif state == 0:
                visit(target, [*trail, node_id])
        colour[node_id] = 2

    for node_id in sorted(tree.nodes):
        if colour.get(node_id, 0) == 0:
            visit(node_id, [])


def _check_contracts(tree: Tree, out: _Collector) -> None:
    for node in tree.nodes.values():
        if node.code_paths and not node.contracts:
            out.error("V4", node.id, "node owns code_paths but declares no contract")
        seen: set[str] = set()
        for contract in node.contracts:
            if not contract.id:
                out.error("V5", node.id, "contract without id")
            elif contract.id in seen:
                out.error("V5", node.id, f"duplicate contract id {contract.id}")
            else:
                seen.add(contract.id)
            if not contract.text:
                out.error("V5", node.id, f"contract {contract.id} has no text")
            enforcer = contract.enforced_by
            if not enforcer:
                out.error("V5", node.id, f"contract {contract.id} has no enforced_by")
                continue
            if enforcer == "review":
                if not contract.reason:
                    out.error(
                        "V5",
                        node.id,
                        f"contract {contract.id} uses 'review' without a reason",
                    )
                else:
                    out.warn(
                        "V5",
                        node.id,
                        f"contract {contract.id} is not machine-enforced (review exception)",
                    )
                continue
            if enforcer.startswith("cmd:"):
                if not enforcer[4:].strip():
                    out.error("V5", node.id, f"contract {contract.id} has an empty command")
                continue
            _check_test_reference(tree, node, contract.id, enforcer, out)


def _check_test_reference(
    tree: Tree, node: Node, contract_id: str, enforcer: str, out: _Collector
) -> None:
    file_part, _, symbol = enforcer.partition("::")
    target = tree.root_dir / file_part
    if not target.exists():
        out.error("V5", node.id, f"contract {contract_id} points at missing file {file_part}")
        return
    if symbol:
        content = target.read_text(encoding="utf-8", errors="replace")
        if symbol not in content:
            out.error(
                "V5",
                node.id,
                f"contract {contract_id} points at '{symbol}' which is absent from {file_part}",
            )


def _check_code_paths(tree: Tree, out: _Collector) -> None:
    owners: list[tuple[str, str]] = []
    for node in tree.nodes.values():
        for code_path in node.code_paths:
            owners.append((code_path.rstrip("/"), node.id))

    for index, (path_a, node_a) in enumerate(owners):
        for path_b, node_b in owners[index + 1 :]:
            if node_a == node_b:
                continue
            if not _overlaps(path_a, path_b):
                continue
            if _is_ancestor(tree, node_a, node_b) or _is_ancestor(tree, node_b, node_a):
                continue
            out.error(
                "V6",
                node_a,
                f"code_path '{path_a}' overlaps '{path_b}' owned by {node_b}, "
                "which is neither an ancestor nor a descendant",
            )


def _overlaps(path_a: str, path_b: str) -> bool:
    if path_a == path_b:
        return True
    return path_a.startswith(path_b + "/") or path_b.startswith(path_a + "/")


def _is_ancestor(tree: Tree, ancestor_id: str, node_id: str) -> bool:
    return ancestor_id in [node.id for node in tree.ancestors(node_id)]


def _check_lifecycle(tree: Tree, out: _Collector) -> None:
    for node in tree.nodes.values():
        if node.status == "superseded":
            if not node.superseded_by:
                out.error("V7", node.id, "status 'superseded' requires superseded_by")
            elif node.superseded_by not in tree.nodes:
                out.error(
                    "V7", node.id, f"superseded_by points at unknown node {node.superseded_by}"
                )
        if node.status == "retired":
            out.error("V7", node.id, f"retired nodes belong in {RETIRED_DIRNAME}/")

    for node in tree.retired.values():
        if node.status != "retired":
            out.error("V7", node.id, f"node in {RETIRED_DIRNAME}/ must have status 'retired'")
        if not tree.registry.is_retired(node.id):
            out.error("V7", node.id, "retired node is not marked retired in the registry")

    for node_id, entry in tree.registry.issued.items():
        if entry.get("retired") and node_id in tree.nodes:
            continue  # already reported by V1
        if not entry.get("retired") and node_id not in tree.nodes and node_id not in tree.retired:
            out.warn("V7", node_id, "issued in the registry but no node file exists")


def _check_body(tree: Tree, out: _Collector) -> None:
    for node in tree.nodes.values():
        sections = node.sections()
        required = REQUIRED_SECTIONS_ROOT if node.parent is None else REQUIRED_SECTIONS_CHILD
        for name in required:
            if name not in sections:
                out.error("V8", node.id, f"body is missing the '## {name}' section")
        count = node.body_line_count
        if count > BODY_ERROR_LINES:
            out.error("V8", node.id, f"body has {count} lines, the limit is {BODY_ERROR_LINES}")
        elif count > BODY_WARN_LINES:
            out.warn(
                "V8", node.id, f"body has {count} lines, consider splitting (>{BODY_WARN_LINES})"
            )
        if node.open_questions:
            out.warn(
                "V8",
                node.id,
                f"{len(node.open_questions)} open question(s) — work touching this node escalates",
            )


def _check_generated(tree: Tree, out: _Collector) -> None:
    for filename in generated_is_current(tree):
        out.error("V9", "-", f"{filename} is stale — run 'intent map'")


def _current_branch(root: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def _check_proposed(tree: Tree, out: _Collector, default_branches: tuple[str, ...]) -> None:
    proposed = [node.id for node in tree.nodes.values() if node.status == "proposed"]
    if not proposed:
        return
    branch = _current_branch(tree.root_dir)
    if branch is None or branch in default_branches:
        where = branch or "an unknown branch"
        out.error(
            "V10",
            ", ".join(sorted(proposed)),
            f"proposed nodes must live on a working branch, not on {where}",
        )
    else:
        out.warn("V10", ", ".join(sorted(proposed)), f"proposed nodes present on branch '{branch}'")


def validate(tree: Tree, default_branches: tuple[str, ...] = ("main", "master")) -> list[Finding]:
    """Run every machine rule and return the findings in rule order."""
    out = _Collector()
    _check_identity(tree, out)
    _check_structure(tree, out)
    _check_edges(tree, out)
    _check_contracts(tree, out)
    _check_code_paths(tree, out)
    _check_lifecycle(tree, out)
    _check_body(tree, out)
    _check_generated(tree, out)
    _check_proposed(tree, out, default_branches)
    return sorted(out.findings, key=lambda finding: (finding.code, finding.node))
