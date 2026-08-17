"""Tests for slice, scope, coverage and the generated views."""

import json
import unittest

from intent.coverage import build_report, find_node_for_path
from intent.generate import build_index, render_map
from intent.scope import Declaration, _matches, load_declaration
from intent.slicing import build_slice
from intent.tests.helpers import TreeBuilder


class ToolTestCase(unittest.TestCase):
    def setUp(self):
        self.builder = TreeBuilder()
        self.addCleanup(self.builder.cleanup)


class SliceTest(ToolTestCase):
    def test_slice_carries_exactly_ancestors_uses_and_talks_to_ends(self):
        # Three-level ancestor chain and one-hop edges only: a uses-of-uses node and
        # two-hop talks_to partners (outgoing and incoming) stay outside.
        root = self.builder.add("system")
        mid = self.builder.add("mid", parent=root)
        deeper_shared = self.builder.add("deeper-shared", parent=root)
        shared = self.builder.add("shared", parent=root, uses=[deeper_shared])
        further_listener = self.builder.add("further-listener", parent=root)
        listener = self.builder.add("listener", parent=root, talks_to=[further_listener])
        target = self.builder.add("target", parent=mid, uses=[shared], talks_to=[listener])
        caller = self.builder.add("caller", parent=root, talks_to=[target])
        far_caller = self.builder.add("far-caller", parent=root, talks_to=[caller])
        sibling = self.builder.add("sibling", parent=mid)
        consumer = self.builder.add("consumer", parent=root, uses=[target])
        child = self.builder.add("child", parent=target)
        tree = self.builder.finish()

        expected = {root, mid, target, shared, listener, caller}
        outside = {
            deeper_shared,
            further_listener,
            far_caller,
            sibling,
            consumer,
            child,
        }

        for for_implementation in (False, True):
            with self.subTest(for_implementation=for_implementation):
                result = build_slice(tree, target, for_implementation=for_implementation)
                carried = {path.split("/")[-1].split("-")[0] for path in result.files}
                self.assertEqual(carried, expected)
                # Implied by the equality above; kept so a leak names the relation that leaked.
                self.assertEqual(carried & outside, set())

    def test_slice_includes_incoming_talks_to(self):
        root = self.builder.add("system")
        caller = self.builder.add("caller", parent=root)
        tree_ids = self.builder.add("callee", parent=root)
        tree = self.builder.finish()
        tree.nodes[caller].talks_to = [tree_ids]

        result = build_slice(tree, tree_ids, for_implementation=False)
        self.assertIn(caller, result.talks_to)

    def test_slice_lists_owned_code_when_implementing(self):
        root = self.builder.add("system")
        self.builder.write_file("src/app/main.py", "x = 1\n")
        node = self.builder.add(
            "app",
            parent=root,
            code_paths=["src/app/"],
            contracts=[{"id": "c1", "text": "x", "enforced_by": "cmd: true"}],
        )
        tree = self.builder.finish()

        result = build_slice(tree, node, for_implementation=True)
        self.assertIn("src/app/main.py", result.code)


class ScopeTest(ToolTestCase):
    def test_pattern_matching_covers_directories(self):
        self.assertTrue(_matches("src/db/models.py", ["src/db/"]))
        self.assertTrue(_matches("src/db/models.py", ["src/db/models.py"]))
        self.assertTrue(_matches("uv.lock", ["*.lock"]))
        self.assertFalse(_matches("src/api/routes.py", ["src/db/"]))

    def test_declaration_is_read_from_plan_front_matter(self):
        self.builder.add("system")
        tree = self.builder.finish()
        run_dir = tree.root_dir / "doc/runs/20260815-1200-demo"
        run_dir.mkdir(parents=True)
        (run_dir / "plan.md").write_text(
            "---\noutputs: [src/app.py]\nincidental: [uv.lock]\n---\n\n# Plan\n",
            encoding="utf-8",
        )
        declaration = load_declaration(run_dir)
        self.assertEqual(declaration.outputs, ["src/app.py"])
        self.assertEqual(declaration.incidental, ["uv.lock"])
        self.assertEqual(len(declaration.allowed()), 2)

    def test_missing_plan_raises(self):
        self.builder.add("system")
        tree = self.builder.finish()
        run_dir = tree.root_dir / "doc/runs/empty"
        run_dir.mkdir(parents=True)
        with self.assertRaises(FileNotFoundError):
            load_declaration(run_dir)

    def test_empty_declaration_allows_nothing(self):
        self.assertEqual(Declaration().allowed(), [])


class CoverageTest(ToolTestCase):
    def test_report_counts_review_exceptions(self):
        root = self.builder.add("system")
        self.builder.write_file("src/app.py", "x = 1\n")
        self.builder.add(
            "app",
            parent=root,
            code_paths=["src/"],
            contracts=[
                {"id": "c1", "text": "a", "enforced_by": "cmd: true"},
                {"id": "c2", "text": "b", "enforced_by": "review", "reason": "manual"},
            ],
        )
        tree = self.builder.finish()
        report = build_report(tree, code_roots=("src",))
        self.assertEqual(report.total_contracts, 2)
        self.assertEqual(report.machine_enforced, 1)
        self.assertEqual(len(report.review_exceptions), 1)
        self.assertEqual(report.uncovered_code, [])

    def test_report_lists_code_outside_any_node(self):
        self.builder.add("system")
        self.builder.write_file("src/orphan.py", "x = 1\n")
        tree = self.builder.finish()
        report = build_report(tree, code_roots=("src",))
        self.assertEqual(report.uncovered_code, ["src/orphan.py"])

    def test_reverse_lookup_prefers_the_deepest_node(self):
        root = self.builder.add("system")
        contract = [{"id": "c1", "text": "x", "enforced_by": "cmd: true"}]
        parent = self.builder.add("db", parent=root, code_paths=["src/db/"], contracts=contract)
        child = self.builder.add(
            "models", parent=parent, code_paths=["src/db/models/"], contracts=contract
        )
        tree = self.builder.finish()
        self.assertEqual(find_node_for_path(tree, "src/db/models/user.py"), child)
        self.assertEqual(find_node_for_path(tree, "src/db/session.py"), parent)
        self.assertIsNone(find_node_for_path(tree, "src/api/routes.py"))


class GeneratedViewTest(ToolTestCase):
    def test_index_holds_derived_path_and_depth(self):
        root = self.builder.add("system")
        child = self.builder.add("engine", parent=root)
        grandchild = self.builder.add(
            "schema",
            parent=child,
            code_paths=["src/schema/"],
            contracts=[{"id": "c1", "text": "x", "enforced_by": "cmd: true"}],
        )
        tree = self.builder.finish()

        index = build_index(tree)
        self.assertEqual(index["nodes"][grandchild]["path"], f"{root}/{child}/{grandchild}")
        self.assertEqual(index["nodes"][grandchild]["depth"], 2)
        self.assertEqual(index["nodes"][root]["children"], [child])
        self.assertEqual(json.loads(json.dumps(index))["schema_version"], 1)
        # The index derives depth twice: once per node entry, once per reverse row.
        row = next((item for item in index["reverse_code_map"] if item["node"] == grandchild), None)
        self.assertIsNotNone(row, f"no reverse row for node {grandchild}")
        self.assertEqual(str(row["depth"]), "2")

    def test_a_path_in_a_node_file_does_not_reach_a_generated_view(self):
        root = self.builder.add("system")
        child = self.builder.add("engine", parent=root, path="nonsense/place", depth=99)
        tree = self.builder.finish()
        expected_path = f"{root}/{child}"

        # Index before map: a one-sided regression must name which view broke.
        index = build_index(tree)
        self.assertEqual(index["nodes"][child]["path"], expected_path)
        self.assertEqual(index["nodes"][child]["depth"], 1)

        # Map: the node's row carries the derived path; the written path is absent from MAP.md.
        text = render_map(tree)
        row = next(
            (
                line
                for line in text.splitlines()
                if line.startswith("|") and f"`{child}`" in line.split("|")[1]
            ),
            None,
        )
        self.assertIsNotNone(row, f"no table row for node {child}")
        self.assertIn(f"`{expected_path}`", row)
        self.assertNotIn("nonsense/place", row)
        self.assertNotIn("nonsense/place", text)

    def test_map_contains_every_node_and_a_diagram(self):
        root = self.builder.add("system")
        child = self.builder.add("engine", parent=root)
        tree = self.builder.finish()

        text = render_map(tree)
        self.assertIn(root, text)
        self.assertIn(child, text)
        self.assertIn("```mermaid", text)
        self.assertIn(f"{root} --> {child}", text)


if __name__ == "__main__":
    unittest.main()
