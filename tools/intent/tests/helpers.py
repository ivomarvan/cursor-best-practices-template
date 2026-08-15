"""Builders for throw-away intent trees used by the tests."""

from __future__ import annotations

import tempfile
from pathlib import Path

from intent.miniyaml import dump
from intent.model import INTENT_DIRNAME, Tree, load_tree

DEFAULT_BODY = """# {title}

## Refines
Refines the parent.

## Meaning
A node used by the test suite.
"""

ROOT_BODY = """# {title}

## Meaning
The system as a whole, for test purposes.
"""


class TreeBuilder:
    """Create a temporary project containing an intent tree."""

    def __init__(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.intent_dir = self.root / INTENT_DIRNAME
        (self.intent_dir / "nodes").mkdir(parents=True)
        self._issued: dict[str, dict[str, object]] = {}
        self._serial = 1

    def cleanup(self) -> None:
        self._tmp.cleanup()

    def add(self, slug: str, *, parent: str | None = None, body: str | None = None, **fields):
        node_id = f"i{self._serial:04d}"
        self._serial += 1
        front: dict[str, object] = {
            "id": node_id,
            "parent": parent,
            "slug": slug,
            "title": fields.pop("title", slug.replace("-", " ")),
            "status": fields.pop("status", "current"),
            "uses": fields.pop("uses", []),
            "talks_to": fields.pop("talks_to", []),
            "superseded_by": fields.pop("superseded_by", None),
            "contracts": fields.pop("contracts", []),
            "code_paths": fields.pop("code_paths", []),
            "test_paths": fields.pop("test_paths", []),
            "open_questions": fields.pop("open_questions", []),
        }
        front.update(fields)
        template = ROOT_BODY if parent is None else DEFAULT_BODY
        text = body if body is not None else template.format(title=front["title"])
        target = self.intent_dir / "nodes" / f"{node_id}-{slug}.md"
        target.write_text(f"---\n{dump(front)}---\n\n{text}", encoding="utf-8")
        self._issued[node_id] = {"slug": slug}
        return node_id

    def write_file(self, relative: str, content: str) -> Path:
        target = self.root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

    def finish(self) -> Tree:
        registry = {
            "prefix": "i",
            "next_serial": self._serial,
            "issued": self._issued,
        }
        (self.intent_dir / "_registry.yaml").write_text(dump(registry), encoding="utf-8")
        tree = load_tree(self.root)
        from intent.generate import write_generated

        write_generated(tree)
        return load_tree(self.root)
