"""Context slice: the adressed list of files one agent action is allowed to read."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from intent import realization
from intent.model import Tree

ADR_DIRNAME = "doc/architecture/decisions"


@dataclass
class Slice:
    node: str
    ancestors: list[str] = field(default_factory=list)
    uses: list[str] = field(default_factory=list)
    talks_to: list[str] = field(default_factory=list)
    files: list[str] = field(default_factory=list)
    adrs: list[str] = field(default_factory=list)
    code: list[str] = field(default_factory=list)
    tests: list[str] = field(default_factory=list)
    realization: str = ""


def _node_file(tree: Tree, node_id: str) -> str | None:
    node = tree.nodes.get(node_id)
    if node is None or node.source is None:
        return None
    return str(node.source.relative_to(tree.root_dir))


def _find_adrs(tree: Tree, ids: list[str]) -> list[str]:
    adr_dir = tree.root_dir / ADR_DIRNAME
    if not adr_dir.is_dir():
        return []
    hits: list[str] = []
    for path in sorted(adr_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        if any(node_id in text for node_id in ids):
            hits.append(str(path.relative_to(tree.root_dir)))
    return hits


def _expand(root: Path, patterns: list[str]) -> list[str]:
    found: list[str] = []
    for pattern in patterns:
        target = root / pattern
        if target.is_dir():
            for path in sorted(target.rglob("*")):
                if path.is_file() and "__pycache__" not in path.parts:
                    found.append(str(path.relative_to(root)))
        elif target.exists():
            found.append(str(target.relative_to(root)))
        else:
            found.extend(
                str(path.relative_to(root)) for path in sorted(root.glob(pattern)) if path.is_file()
            )
    return found


def build_slice(tree: Tree, node_id: str, for_implementation: bool) -> Slice:
    """Assemble the slice for ``node_id`` following the rules of the methodology."""
    if node_id not in tree.nodes:
        raise KeyError(node_id)
    node = tree.nodes[node_id]

    ancestors = [item.id for item in tree.ancestors(node_id)]
    incoming = sorted(other.id for other in tree.nodes.values() if node_id in other.talks_to)
    talks = sorted(set(node.talks_to) | set(incoming))

    result = Slice(
        node=node_id,
        ancestors=ancestors,
        uses=sorted(node.uses),
        talks_to=talks,
    )

    node_ids = [*ancestors, node_id, *result.uses, *result.talks_to]
    for candidate in node_ids:
        file_path = _node_file(tree, candidate)
        if file_path and file_path not in result.files:
            result.files.append(file_path)

    result.adrs = _find_adrs(tree, [*ancestors, node_id])
    if for_implementation:
        result.code = _expand(tree.root_dir, node.code_paths)
        result.tests = _expand(tree.root_dir, node.test_paths)

    # The Coder needs to know what moved since the node was last proven, not just what
    # the node means; without it the reason for the run has to be retold in prose.
    state = realization.compute_states(tree).get(node_id)
    result.realization = state.summary() if state else "not applicable (node is not current)"
    return result


def render_slice(tree: Tree, result: Slice) -> str:
    node = tree.nodes[result.node]
    path = "/".join(tree.path_of(result.node))
    lines = [
        f"# Slice for {result.node} — {node.title}",
        "",
        f"- path: `{path}`",
        f"- depth: {tree.depth_of(result.node)}",
        f"- realization: {result.realization}",
        "",
        "## Intent nodes (read as truth)",
        "",
    ]
    for file_path in result.files:
        lines.append(f"- `{file_path}`")
    if result.adrs:
        lines += ["", "## Decision records", ""]
        lines += [f"- `{item}`" for item in result.adrs]
    if result.code:
        lines += ["", "## Code owned by this node", ""]
        lines += [f"- `{item}`" for item in result.code]
    if result.tests:
        lines += ["", "## Tests owned by this node", ""]
        lines += [f"- `{item}`" for item in result.tests]
    if node.open_questions:
        lines += ["", "## Open questions (blocking)", ""]
        lines += [f"- {item}" for item in node.open_questions]
    lines += [
        "",
        "## Contracts in force",
        "",
    ]
    for ancestor in [*result.ancestors, result.node]:
        for contract in tree.nodes[ancestor].contracts:
            lines.append(
                f"- `{ancestor}` {contract.id}: {contract.text} — `{contract.enforced_by}`"
            )
    lines.append("")
    lines.append("Anything outside this list is not part of the task context.")
    lines.append("")
    return "\n".join(lines)
