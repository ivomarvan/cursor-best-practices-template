"""Tests for the machine rules V1-V10."""

import unittest

from intent.tests.helpers import TreeBuilder
from intent.validate import validate


class ValidateTestCase(unittest.TestCase):
    def setUp(self):
        self.builder = TreeBuilder()
        self.addCleanup(self.builder.cleanup)

    def codes(self, tree, level="error"):
        return sorted(finding.code for finding in validate(tree) if finding.level == level)


class HappyPathTest(ValidateTestCase):
    def test_minimal_valid_tree_has_no_errors(self):
        root = self.builder.add("system")
        self.builder.add("engine", parent=root)
        tree = self.builder.finish()
        self.assertEqual(self.codes(tree), [])


class IdentityTest(ValidateTestCase):
    def test_unissued_id_is_an_error(self):
        root = self.builder.add("system")
        tree = self.builder.finish()
        del tree.registry.issued[root]
        self.assertIn("V1", self.codes(tree))

    def test_filename_must_match_id_and_slug(self):
        root = self.builder.add("system")
        tree = self.builder.finish()
        node = tree.nodes[root]
        node.source.rename(node.source.with_name("wrong-name.md"))
        tree = self.builder.finish()
        self.assertIn("V1", self.codes(tree))


class StructureTest(ValidateTestCase):
    def test_two_roots_are_rejected(self):
        self.builder.add("system")
        self.builder.add("second")
        tree = self.builder.finish()
        self.assertIn("V2", self.codes(tree))

    def test_missing_parent_is_rejected(self):
        self.builder.add("system")
        self.builder.add("orphan", parent="i9999")
        tree = self.builder.finish()
        self.assertIn("V2", self.codes(tree))


class EdgeTest(ValidateTestCase):
    def test_uses_cycle_is_rejected(self):
        root = self.builder.add("system")
        first = self.builder.add("a", parent=root)
        second = self.builder.add("b", parent=root)
        tree = self.builder.finish()
        tree.nodes[first].uses = [second]
        tree.nodes[second].uses = [first]
        self.assertIn("V3", self.codes(tree))

    def test_talks_to_cycle_is_allowed(self):
        root = self.builder.add("system")
        first = self.builder.add("a", parent=root)
        second = self.builder.add("b", parent=root)
        tree = self.builder.finish()
        tree.nodes[first].talks_to = [second]
        tree.nodes[second].talks_to = [first]
        self.assertNotIn("V3", self.codes(tree))


class ContractTest(ValidateTestCase):
    def test_code_paths_without_contract_is_rejected(self):
        root = self.builder.add("system")
        self.builder.write_file("src/app.py", "print('x')\n")
        self.builder.add("app", parent=root, code_paths=["src/"])
        tree = self.builder.finish()
        self.assertIn("V4", self.codes(tree))

    def test_contract_pointing_at_missing_test_is_rejected(self):
        root = self.builder.add("system")
        self.builder.add(
            "app",
            parent=root,
            code_paths=["src/"],
            contracts=[{"id": "c1", "text": "x", "enforced_by": "tests/nope.py::test_x"}],
        )
        tree = self.builder.finish()
        self.assertIn("V5", self.codes(tree))

    def test_contract_pointing_at_existing_symbol_passes(self):
        root = self.builder.add("system")
        self.builder.write_file("tests/test_app.py", "def test_x():\n    assert True\n")
        self.builder.add(
            "app",
            parent=root,
            code_paths=["src/"],
            contracts=[{"id": "c1", "text": "x", "enforced_by": "tests/test_app.py::test_x"}],
        )
        tree = self.builder.finish()
        self.assertNotIn("V5", self.codes(tree))

    def test_review_exception_requires_reason(self):
        root = self.builder.add("system")
        self.builder.add(
            "app",
            parent=root,
            code_paths=["src/"],
            contracts=[{"id": "c1", "text": "x", "enforced_by": "review"}],
        )
        tree = self.builder.finish()
        self.assertIn("V5", self.codes(tree))

    def test_review_exception_with_reason_is_a_warning_only(self):
        root = self.builder.add("system")
        self.builder.add(
            "app",
            parent=root,
            code_paths=["src/"],
            contracts=[{"id": "c1", "text": "x", "enforced_by": "review", "reason": "no snapshot"}],
        )
        tree = self.builder.finish()
        self.assertNotIn("V5", self.codes(tree))
        self.assertIn("V5", self.codes(tree, level="warning"))


class CodePathTest(ValidateTestCase):
    def test_the_ancestor_chain_may_overlap(self):
        root = self.builder.add("system")
        contract = [{"id": "c1", "text": "x", "enforced_by": "cmd: true"}]
        parent = self.builder.add("db", parent=root, code_paths=["src/db/"], contracts=contract)
        child = self.builder.add(
            "models", parent=parent, code_paths=["src/db/models/"], contracts=contract
        )
        self.builder.add(
            "user", parent=child, code_paths=["src/db/models/user/"], contracts=contract
        )
        tree = self.builder.finish()
        self.assertNotIn("V6", self.codes(tree))

    def test_overlap_outside_the_ancestor_chain_is_rejected(self):
        root = self.builder.add("system")
        contract = [{"id": "c1", "text": "x", "enforced_by": "cmd: true"}]
        # Siblings: two different nodes, same parent — neither is the other's ancestor.
        sibling_a = self.builder.add("a", parent=root, code_paths=["src/db/"], contracts=contract)
        sibling_b = self.builder.add(
            "b", parent=root, code_paths=["src/db/models/"], contracts=contract
        )
        # Cousins: two different nodes, children of two different parents.
        aunt = self.builder.add("aunt", parent=root, contracts=contract)
        uncle = self.builder.add("uncle", parent=root, contracts=contract)
        cousin_a = self.builder.add(
            "cousin-a", parent=aunt, code_paths=["src/api/"], contracts=contract
        )
        cousin_b = self.builder.add(
            "cousin-b", parent=uncle, code_paths=["src/api/v1/"], contracts=contract
        )
        tree = self.builder.finish()
        flagged = {finding.node for finding in validate(tree) if finding.code == "V6"}
        self.assertTrue({sibling_a, sibling_b} & flagged)
        self.assertTrue({cousin_a, cousin_b} & flagged)


class DerivedFieldTest(ValidateTestCase):
    def test_derived_fields_in_a_node_file_are_reported(self):
        root = self.builder.add("system")
        engine = self.builder.add("engine", parent=root, path="nonsense/place", depth=99)
        # The contract says path or depth — each alone is already the mistake.
        path_only = self.builder.add("path-only", parent=root, path="nonsense/place")
        depth_only = self.builder.add("depth-only", parent=root, depth=99)
        clean = self.builder.add("clean", parent=root)
        # A retired file is a node file too, and its derived fields are the same mistake.
        gone = self.builder.add("gone", parent=root, retired=True, path="nonsense/place", depth=99)
        tree = self.builder.finish()

        findings = list(validate(tree))
        flagged_path = {
            finding.node
            for finding in findings
            if finding.code == "V1" and "path" in finding.message
        }
        flagged_depth = {
            finding.node
            for finding in findings
            if finding.code == "V1" and "depth" in finding.message
        }
        self.assertIn(engine, flagged_path)
        self.assertIn(engine, flagged_depth)
        self.assertIn(path_only, flagged_path)
        self.assertNotIn(path_only, flagged_depth)
        self.assertIn(depth_only, flagged_depth)
        self.assertNotIn(depth_only, flagged_path)
        self.assertNotIn(clean, flagged_path)
        self.assertNotIn(clean, flagged_depth)
        self.assertIn(gone, flagged_path)
        self.assertIn(gone, flagged_depth)


class LifecycleTest(ValidateTestCase):
    def test_superseded_requires_target(self):
        root = self.builder.add("system")
        self.builder.add("old", parent=root, status="superseded")
        tree = self.builder.finish()
        self.assertIn("V7", self.codes(tree))

    def test_retired_status_may_not_live_in_nodes(self):
        root = self.builder.add("system")
        self.builder.add("gone", parent=root, status="retired")
        tree = self.builder.finish()
        self.assertIn("V7", self.codes(tree))


class BodyTest(ValidateTestCase):
    def test_missing_section_is_rejected(self):
        root = self.builder.add("system")
        self.builder.add("child", parent=root, body="# Child\n\n## Meaning\nNo refines section.\n")
        tree = self.builder.finish()
        self.assertIn("V8", self.codes(tree))

    def test_oversized_body_is_rejected(self):
        root = self.builder.add("system")
        filler = "\n".join(f"line {index}" for index in range(220))
        self.builder.add(
            "big",
            parent=root,
            body=f"# Big\n\n## Refines\nx\n\n## Meaning\n{filler}\n",
        )
        tree = self.builder.finish()
        self.assertIn("V8", self.codes(tree))


class GeneratedTest(ValidateTestCase):
    def test_stale_map_is_rejected(self):
        root = self.builder.add("system")
        tree = self.builder.finish()
        (tree.intent_dir / "MAP.md").write_text("stale\n", encoding="utf-8")
        self.assertIn("V9", self.codes(tree))
        self.assertTrue(root)


if __name__ == "__main__":
    unittest.main()
