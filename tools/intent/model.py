"""In-memory model of the intent tree: nodes, registry and derived structure.

Derived data (path, depth, children, reverse code map) is computed here and never
stored in node files, so that inserting a level of abstraction does not rewrite a
whole subtree.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from intent.miniyaml import YamlError, parse, split_front_matter

NODE_ID_PATTERN = re.compile(r"^i\d{4,}$")
INTENT_DIRNAME = "doc/intent"
NODES_DIRNAME = "nodes"
RETIRED_DIRNAME = "_retired"
REGISTRY_FILENAME = "_registry.yaml"
MAP_FILENAME = "MAP.md"
INDEX_FILENAME = "INDEX.json"

STATUS_VALUES = ("proposed", "current", "superseded", "retired")

LIST_FIELDS = ("uses", "talks_to", "code_paths", "test_paths", "open_questions")
KNOWN_FIELDS = {
    "id",
    "parent",
    "slug",
    "title",
    "status",
    "superseded_by",
    "contracts",
    *LIST_FIELDS,
}


class TreeError(Exception):
    """Raised when the tree cannot be loaded at all (as opposed to being invalid)."""


@dataclass
class Contract:
    id: str
    text: str
    enforced_by: str
    reason: str | None = None


@dataclass
class Node:
    id: str
    slug: str
    title: str
    status: str
    parent: str | None
    uses: list[str] = field(default_factory=list)
    talks_to: list[str] = field(default_factory=list)
    code_paths: list[str] = field(default_factory=list)
    test_paths: list[str] = field(default_factory=list)
    open_questions: list[str] = field(default_factory=list)
    contracts: list[Contract] = field(default_factory=list)
    superseded_by: str | None = None
    body: str = ""
    source: Path | None = None
    unknown_fields: list[str] = field(default_factory=list)
    retired_file: bool = False

    @property
    def body_line_count(self) -> int:
        return len([line for line in self.body.splitlines() if line.strip()])

    def sections(self) -> list[str]:
        return [line[3:].strip() for line in self.body.splitlines() if line.startswith("## ")]


@dataclass
class Registry:
    prefix: str
    next_serial: int
    issued: dict[str, dict[str, object]]
    source: Path

    def is_retired(self, node_id: str) -> bool:
        entry = self.issued.get(node_id) or {}
        return bool(entry.get("retired"))


def _as_str_list(value: object, field_name: str, node_id: str) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    raise TreeError(f"{node_id}: field '{field_name}' must be a list")


def parse_node(path: Path) -> Node:
    """Read a single node file into a :class:`Node`."""
    text = path.read_text(encoding="utf-8")
    try:
        front, body = split_front_matter(text)
        data = parse(front)
    except YamlError as exc:
        raise TreeError(f"{path}: {exc}") from exc

    node_id = str(data.get("id") or "")
    if not node_id:
        raise TreeError(f"{path}: missing 'id'")

    raw_contracts = data.get("contracts") or []
    if not isinstance(raw_contracts, list):
        raise TreeError(f"{node_id}: 'contracts' must be a list")
    contracts: list[Contract] = []
    for item in raw_contracts:
        if not isinstance(item, dict):
            raise TreeError(f"{node_id}: every contract must be a mapping")
        contracts.append(
            Contract(
                id=str(item.get("id") or ""),
                text=str(item.get("text") or ""),
                enforced_by=str(item.get("enforced_by") or ""),
                reason=None if item.get("reason") is None else str(item.get("reason")),
            )
        )

    parent = data.get("parent")
    superseded_by = data.get("superseded_by")
    return Node(
        id=node_id,
        slug=str(data.get("slug") or ""),
        title=str(data.get("title") or ""),
        status=str(data.get("status") or ""),
        parent=None if parent is None else str(parent),
        uses=_as_str_list(data.get("uses"), "uses", node_id),
        talks_to=_as_str_list(data.get("talks_to"), "talks_to", node_id),
        code_paths=_as_str_list(data.get("code_paths"), "code_paths", node_id),
        test_paths=_as_str_list(data.get("test_paths"), "test_paths", node_id),
        open_questions=_as_str_list(data.get("open_questions"), "open_questions", node_id),
        contracts=contracts,
        superseded_by=None if superseded_by is None else str(superseded_by),
        body=body,
        source=path,
        unknown_fields=sorted(set(data) - KNOWN_FIELDS),
        retired_file=path.parent.name == RETIRED_DIRNAME,
    )


def load_registry(intent_dir: Path) -> Registry:
    path = intent_dir / REGISTRY_FILENAME
    if not path.exists():
        raise TreeError(f"registry not found: {path}")
    try:
        data = parse(path.read_text(encoding="utf-8"))
    except YamlError as exc:
        raise TreeError(f"{path}: {exc}") from exc
    issued_raw = data.get("issued") or {}
    if not isinstance(issued_raw, dict):
        raise TreeError(f"{path}: 'issued' must be a mapping")
    issued: dict[str, dict[str, object]] = {}
    for key, value in issued_raw.items():
        issued[str(key)] = value if isinstance(value, dict) else {}
    next_serial = data.get("next_serial")
    if not isinstance(next_serial, int):
        raise TreeError(f"{path}: 'next_serial' must be an integer")
    return Registry(
        prefix=str(data.get("prefix") or "i"),
        next_serial=next_serial,
        issued=issued,
        source=path,
    )


@dataclass
class Tree:
    root_dir: Path
    intent_dir: Path
    registry: Registry
    nodes: dict[str, Node]
    retired: dict[str, Node]

    def children_of(self, node_id: str) -> list[Node]:
        return sorted(
            (node for node in self.nodes.values() if node.parent == node_id),
            key=lambda node: node.id,
        )

    def roots(self) -> list[Node]:
        return sorted(
            (node for node in self.nodes.values() if node.parent is None),
            key=lambda node: node.id,
        )

    def ancestors(self, node_id: str) -> list[Node]:
        """Return nodes from the root down to (and excluding) ``node_id``."""
        chain: list[Node] = []
        seen: set[str] = set()
        current = self.nodes.get(node_id)
        while current is not None and current.parent is not None:
            if current.parent in seen:
                break
            seen.add(current.parent)
            parent = self.nodes.get(current.parent)
            if parent is None:
                break
            chain.append(parent)
            current = parent
        return list(reversed(chain))

    def path_of(self, node_id: str) -> list[str]:
        return [node.id for node in self.ancestors(node_id)] + [node_id]

    def depth_of(self, node_id: str) -> int:
        return len(self.path_of(node_id)) - 1

    def has_cycle(self, node_id: str) -> bool:
        seen: set[str] = set()
        current = self.nodes.get(node_id)
        while current is not None and current.parent is not None:
            if current.id in seen:
                return True
            seen.add(current.id)
            current = self.nodes.get(current.parent)
        return False

    def sorted_nodes(self) -> list[Node]:
        return sorted(self.nodes.values(), key=lambda node: (self.depth_of(node.id), node.id))


def find_root(start: Path | None = None) -> Path:
    """Locate the project root: the nearest ancestor containing ``doc/intent``.

    The search deliberately never descends into ``.cursor``: a template mounted as a
    submodule may carry its own intent tree, which must not mix with the project's.
    """
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / INTENT_DIRNAME).is_dir():
            return candidate
    raise TreeError(f"no '{INTENT_DIRNAME}' directory found in {current} or any parent directory")


def load_tree(root: Path) -> Tree:
    intent_dir = root / INTENT_DIRNAME
    nodes_dir = intent_dir / NODES_DIRNAME
    if not nodes_dir.is_dir():
        raise TreeError(f"nodes directory not found: {nodes_dir}")

    nodes: dict[str, Node] = {}
    for path in sorted(nodes_dir.glob("*.md")):
        node = parse_node(path)
        if node.id in nodes:
            raise TreeError(f"duplicate node id {node.id} in {path}")
        nodes[node.id] = node

    retired: dict[str, Node] = {}
    retired_dir = intent_dir / RETIRED_DIRNAME
    if retired_dir.is_dir():
        for path in sorted(retired_dir.glob("*.md")):
            node = parse_node(path)
            retired[node.id] = node

    return Tree(
        root_dir=root,
        intent_dir=intent_dir,
        registry=load_registry(intent_dir),
        nodes=nodes,
        retired=retired,
    )
