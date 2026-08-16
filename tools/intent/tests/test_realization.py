"""Tests for the realization layer: fingerprints, derived states and the worklist."""

import unittest

from intent.model import TreeError
from intent.realization import (
    Policy,
    affirm,
    build_worklist,
    check_layer,
    claim,
    compute_states,
    contracts_fingerprint,
    decide,
    load_layer,
    meaning_fingerprint,
    prune,
    save_layer,
)
from intent.scope import Declaration, allowed_paths
from intent.tests.helpers import TreeBuilder

CONTRACT = [{"id": "c1", "text": "x holds", "enforced_by": "cmd: true"}]

BODY = """# {title}

## Refines
Refines the parent.

## Meaning
{meaning}

## Non-goals
Nothing else.
"""


class RealizationTestCase(unittest.TestCase):
    def setUp(self):
        self.builder = TreeBuilder()
        self.addCleanup(self.builder.cleanup)
        self.policy = Policy()

    def evidence(self, name="20260816-1200-demo"):
        """A run directory with a Grader log — what the standard profile demands."""
        self.builder.write_file(f"doc/runs/{name}/grader.md", "all green\n")
        return f"doc/runs/{name}"

    def layer_of(self, tree):
        return load_layer(tree.intent_dir)

    def state_of(self, tree, layer, node_id):
        return compute_states(tree, layer, self.policy)[node_id]

    def retitle(self, tree, node_id, meaning):
        """Rewrite the Meaning section of a node in memory."""
        node = tree.nodes[node_id]
        node.body = BODY.format(title=node.title, meaning=meaning)


class FingerprintTest(RealizationTestCase):
    def test_reordering_contracts_does_not_change_the_fingerprint(self):
        root = self.builder.add("system")
        node = self.builder.add(
            "app",
            parent=root,
            contracts=[
                {"id": "c1", "text": "a", "enforced_by": "cmd: true"},
                {"id": "c2", "text": "b", "enforced_by": "cmd: true"},
            ],
        )
        tree = self.builder.finish()
        before = contracts_fingerprint(tree.nodes[node])
        tree.nodes[node].contracts.reverse()
        self.assertEqual(before, contracts_fingerprint(tree.nodes[node]))

    def test_renaming_a_node_does_not_change_the_meaning_fingerprint(self):
        root = self.builder.add("system")
        node = self.builder.add("app", parent=root)
        tree = self.builder.finish()
        before = meaning_fingerprint(tree.nodes[node])
        tree.nodes[node].title = "Something else entirely"
        tree.nodes[node].code_paths = ["src/moved/"]
        self.assertEqual(before, meaning_fingerprint(tree.nodes[node]))

    def test_changing_the_meaning_section_changes_the_fingerprint(self):
        root = self.builder.add("system")
        node = self.builder.add("app", parent=root)
        tree = self.builder.finish()
        before = meaning_fingerprint(tree.nodes[node])
        self.retitle(tree, node, "A different promise entirely.")
        self.assertNotEqual(before, meaning_fingerprint(tree.nodes[node]))


class ClaimTest(RealizationTestCase):
    def test_claim_makes_a_node_realized(self):
        root = self.builder.add("system")
        node = self.builder.add("app", parent=root, contracts=CONTRACT)
        tree = self.builder.finish()
        layer = self.layer_of(tree)

        state = claim(tree, layer, self.policy, node, self.evidence(), "Coordinator")
        self.assertEqual(state.state, "realized")
        self.assertEqual(self.state_of(tree, layer, node).state, "realized")

    def test_coder_may_not_claim_its_own_work(self):
        root = self.builder.add("system")
        node = self.builder.add("app", parent=root, contracts=CONTRACT)
        tree = self.builder.finish()
        layer = self.layer_of(tree)

        with self.assertRaises(TreeError):
            claim(tree, layer, self.policy, node, self.evidence(), "Coder")

    def test_claim_refuses_a_node_with_an_open_question(self):
        root = self.builder.add("system")
        node = self.builder.add(
            "app", parent=root, contracts=CONTRACT, open_questions=["is the format stable?"]
        )
        tree = self.builder.finish()
        layer = self.layer_of(tree)

        with self.assertRaises(TreeError):
            claim(tree, layer, self.policy, node, self.evidence(), "Coordinator")

    def test_claim_refuses_evidence_without_a_grader_log(self):
        root = self.builder.add("system")
        node = self.builder.add("app", parent=root, contracts=CONTRACT)
        tree = self.builder.finish()
        self.builder.write_file("doc/runs/empty/plan.md", "no grader here\n")
        layer = self.layer_of(tree)

        with self.assertRaises(TreeError):
            claim(tree, layer, self.policy, node, "doc/runs/empty", "Coordinator")

    def test_relaxed_profile_accepts_verify_as_evidence(self):
        root = self.builder.add("system")
        node = self.builder.add("app", parent=root, contracts=CONTRACT)
        tree = self.builder.finish()
        self.builder.write_file("VERIFY.md", "# VERIFY\n")
        policy = Policy(evidence_profile="relaxed")
        layer = self.layer_of(tree)

        state = claim(tree, layer, policy, node, "VERIFY.md", "ivo")
        self.assertEqual(state.state, "realized")


class StalenessTest(RealizationTestCase):
    def test_changing_the_meaning_makes_a_claim_stale(self):
        root = self.builder.add("system")
        node = self.builder.add("app", parent=root, contracts=CONTRACT)
        tree = self.builder.finish()
        layer = self.layer_of(tree)
        claim(tree, layer, self.policy, node, self.evidence(), "Coordinator")

        self.retitle(tree, node, "Now it promises something else.")
        state = self.state_of(tree, layer, node)
        self.assertEqual(state.state, "stale")
        self.assertIn("own meaning changed", state.reasons)

    def test_ancestor_text_change_opens_the_subtree(self):
        root = self.builder.add("system")
        middle = self.builder.add("engine", parent=root, contracts=CONTRACT)
        leaf = self.builder.add("schema", parent=middle, contracts=CONTRACT)
        tree = self.builder.finish()
        layer = self.layer_of(tree)
        for node_id in (middle, leaf):
            claim(tree, layer, self.policy, node_id, self.evidence(), "Coordinator")

        self.retitle(tree, middle, "The engine now means something else.")
        state = self.state_of(tree, layer, leaf)
        self.assertEqual(state.state, "stale")
        self.assertEqual(state.blocked_by, middle)

    def test_unproven_ancestor_does_not_block_a_child(self):
        """Decision Q4: only a change of wording invalidates, never a state.

        Otherwise adoption would have to start at the root — the least provable node in
        any tree — because after bootstrap nothing is claimed anywhere.
        """
        root = self.builder.add("system")
        leaf = self.builder.add("app", parent=root, contracts=CONTRACT)
        tree = self.builder.finish()
        layer = self.layer_of(tree)
        claim(tree, layer, self.policy, leaf, self.evidence(), "Coordinator")

        states = compute_states(tree, layer, self.policy)
        self.assertEqual(states[root].state, "not_claimed")
        self.assertEqual(states[leaf].state, "realized")

    def test_uses_target_contract_change_opens_the_consumer(self):
        root = self.builder.add("system")
        target = self.builder.add("shared", parent=root, contracts=CONTRACT)
        consumer = self.builder.add("app", parent=root, uses=[target], contracts=CONTRACT)
        tree = self.builder.finish()
        layer = self.layer_of(tree)
        for node_id in (target, consumer):
            claim(tree, layer, self.policy, node_id, self.evidence(), "Coordinator")

        tree.nodes[target].contracts[0].text = "x holds, but differently"
        state = self.state_of(tree, layer, consumer)
        self.assertEqual(state.state, "stale")
        self.assertIn(f"used {target} changed contracts", state.reasons)

    def test_uses_target_meaning_change_leaves_the_consumer_alone(self):
        root = self.builder.add("system")
        target = self.builder.add("shared", parent=root, contracts=CONTRACT)
        consumer = self.builder.add("app", parent=root, uses=[target], contracts=CONTRACT)
        tree = self.builder.finish()
        layer = self.layer_of(tree)
        for node_id in (target, consumer):
            claim(tree, layer, self.policy, node_id, self.evidence(), "Coordinator")

        self.retitle(tree, target, "Same commitment, better prose.")
        states = compute_states(tree, layer, self.policy)
        self.assertEqual(states[target].state, "stale")
        self.assertEqual(states[consumer].state, "realized")

    def test_uses_propagation_stops_after_one_hop(self):
        root = self.builder.add("system")
        deep = self.builder.add("deep", parent=root, contracts=CONTRACT)
        middle = self.builder.add("middle", parent=root, uses=[deep], contracts=CONTRACT)
        outer = self.builder.add("outer", parent=root, uses=[middle], contracts=CONTRACT)
        tree = self.builder.finish()
        layer = self.layer_of(tree)
        for node_id in (deep, middle, outer):
            claim(tree, layer, self.policy, node_id, self.evidence(), "Coordinator")

        tree.nodes[deep].contracts[0].text = "a stricter promise"
        states = compute_states(tree, layer, self.policy)
        self.assertEqual(states[middle].state, "stale")
        self.assertEqual(states[outer].state, "realized")


class BrokenEnforcerTest(RealizationTestCase):
    def test_a_missing_enforcer_makes_a_realized_node_broken(self):
        root = self.builder.add("system")
        self.builder.write_file("tests/test_app.py", "def test_x():\n    assert True\n")
        node = self.builder.add(
            "app",
            parent=root,
            contracts=[{"id": "c1", "text": "x", "enforced_by": "tests/test_app.py::test_x"}],
        )
        tree = self.builder.finish()
        layer = self.layer_of(tree)
        claim(tree, layer, self.policy, node, self.evidence(), "Coordinator")

        (tree.root_dir / "tests/test_app.py").unlink()
        state = self.state_of(tree, layer, node)
        self.assertEqual(state.state, "broken")
        self.assertTrue(any("enforcer missing" in reason for reason in state.reasons))

    def test_a_renamed_enforcer_symbol_makes_a_node_broken(self):
        """A substring match would accept 'test_x' inside 'test_x_v2' and miss the rename."""
        root = self.builder.add("system")
        self.builder.write_file("tests/test_app.py", "def test_x():\n    assert True\n")
        node = self.builder.add(
            "app",
            parent=root,
            contracts=[{"id": "c1", "text": "x", "enforced_by": "tests/test_app.py::test_x"}],
        )
        tree = self.builder.finish()
        layer = self.layer_of(tree)
        claim(tree, layer, self.policy, node, self.evidence(), "Coordinator")

        renamed = "def test_x_v2():\n    assert True\n"
        (tree.root_dir / "tests/test_app.py").write_text(renamed, encoding="utf-8")
        self.assertEqual(self.state_of(tree, layer, node).state, "broken")

    def test_a_broken_node_appears_in_the_worklist(self):
        root = self.builder.add("system")
        self.builder.write_file("tests/test_app.py", "def test_x():\n    assert True\n")
        node = self.builder.add(
            "app",
            parent=root,
            contracts=[{"id": "c1", "text": "x", "enforced_by": "tests/test_app.py::test_x"}],
        )
        tree = self.builder.finish()
        layer = self.layer_of(tree)
        claim(tree, layer, self.policy, node, self.evidence(), "Coordinator")
        (tree.root_dir / "tests/test_app.py").unlink()

        states = compute_states(tree, layer, self.policy)
        self.assertIn(node, [item.node for item in build_worklist(tree, states)])


class AffirmTest(RealizationTestCase):
    def test_affirm_keeps_the_claim_after_a_harmless_edit(self):
        root = self.builder.add("system")
        node = self.builder.add("app", parent=root, contracts=CONTRACT)
        tree = self.builder.finish()
        layer = self.layer_of(tree)
        claim(tree, layer, self.policy, node, self.evidence(), "Coordinator")

        self.retitle(tree, node, "A node used by the test suite (typo fixed).")
        self.assertEqual(self.state_of(tree, layer, node).state, "stale")

        affirm(tree, layer, self.policy, node, "ivo", "typo only", subtree=False)
        self.assertEqual(self.state_of(tree, layer, node).state, "realized")

    def test_affirm_refuses_an_agent_role(self):
        root = self.builder.add("system")
        node = self.builder.add("app", parent=root, contracts=CONTRACT)
        tree = self.builder.finish()
        layer = self.layer_of(tree)
        claim(tree, layer, self.policy, node, self.evidence(), "Coordinator")

        with self.assertRaises(TreeError):
            affirm(tree, layer, self.policy, node, "Coordinator", "looks fine", subtree=False)

    def test_affirm_subtree_touches_descendants_with_a_claim(self):
        root = self.builder.add("system")
        middle = self.builder.add("engine", parent=root, contracts=CONTRACT)
        leaf = self.builder.add("schema", parent=middle, contracts=CONTRACT)
        tree = self.builder.finish()
        layer = self.layer_of(tree)
        for node_id in (middle, leaf):
            claim(tree, layer, self.policy, node_id, self.evidence(), "Coordinator")

        self.retitle(tree, middle, "Rewritten prose, same commitment.")
        touched = affirm(tree, layer, self.policy, middle, "ivo", "prose only", subtree=True)
        self.assertEqual(sorted(touched), sorted([middle, leaf]))
        states = compute_states(tree, layer, self.policy)
        self.assertEqual(states[leaf].state, "realized")


class AcceptanceTest(RealizationTestCase):
    def test_review_contract_makes_acceptance_required(self):
        root = self.builder.add("system")
        node = self.builder.add(
            "app",
            parent=root,
            contracts=[{"id": "c1", "text": "x", "enforced_by": "review", "reason": "no snapshot"}],
        )
        tree = self.builder.finish()
        layer = self.layer_of(tree)
        claim(tree, layer, self.policy, node, self.evidence(), "Coordinator")

        self.assertEqual(self.state_of(tree, layer, node).acceptance, "pending")
        decide(tree, layer, node, "approved", "ivo", "read it by hand")
        self.assertEqual(self.state_of(tree, layer, node).acceptance, "approved")

    def test_acceptance_decays_when_the_wording_moves(self):
        root = self.builder.add("system")
        node = self.builder.add(
            "app",
            parent=root,
            contracts=[{"id": "c1", "text": "x", "enforced_by": "review", "reason": "no snapshot"}],
        )
        tree = self.builder.finish()
        layer = self.layer_of(tree)
        claim(tree, layer, self.policy, node, self.evidence(), "Coordinator")
        decide(tree, layer, node, "approved", "ivo", None)

        self.retitle(tree, node, "The promise moved.")
        self.assertEqual(self.state_of(tree, layer, node).acceptance, "pending")

    def test_rejection_marks_an_otherwise_realized_node(self):
        root = self.builder.add("system")
        node = self.builder.add("app", parent=root, contracts=CONTRACT)
        tree = self.builder.finish()
        layer = self.layer_of(tree)
        claim(tree, layer, self.policy, node, self.evidence(), "Coordinator")
        decide(tree, layer, node, "rejected", "ivo", "the test misses the point")

        state = self.state_of(tree, layer, node)
        self.assertEqual(state.state, "rejected")

    def test_an_agent_may_not_accept(self):
        root = self.builder.add("system")
        node = self.builder.add("app", parent=root, contracts=CONTRACT)
        tree = self.builder.finish()
        layer = self.layer_of(tree)
        claim(tree, layer, self.policy, node, self.evidence(), "Coordinator")

        with self.assertRaises(TreeError):
            decide(tree, layer, node, "approved", "Adversary", None)

    def test_leaf_profile_requires_acceptance_for_nodes_owning_code(self):
        root = self.builder.add("system")
        self.builder.write_file("src/app.py", "x = 1\n")
        node = self.builder.add("app", parent=root, code_paths=["src/"], contracts=CONTRACT)
        tree = self.builder.finish()
        policy = Policy(acceptance_profile="leaf")
        layer = self.layer_of(tree)
        claim(tree, layer, policy, node, self.evidence(), "Coordinator")

        self.assertEqual(compute_states(tree, layer, policy)[node].acceptance, "pending")


class WorklistTest(RealizationTestCase):
    def test_worklist_puts_ancestors_first(self):
        root = self.builder.add("system")
        middle = self.builder.add("engine", parent=root, contracts=CONTRACT)
        leaf = self.builder.add("schema", parent=middle, contracts=CONTRACT)
        tree = self.builder.finish()
        layer = self.layer_of(tree)

        order = [item.node for item in build_worklist(tree, compute_states(tree, layer))]
        self.assertEqual(order, [root, middle, leaf])

    def test_realized_and_accepted_nodes_leave_the_worklist(self):
        root = self.builder.add("system")
        tree = self.builder.finish()
        layer = self.layer_of(tree)
        claim(tree, layer, self.policy, root, self.evidence(), "Coordinator")

        states = compute_states(tree, layer, self.policy)
        self.assertEqual(build_worklist(tree, states), [])


class PersistenceTest(RealizationTestCase):
    def test_layer_survives_a_save_and_load_round_trip(self):
        root = self.builder.add("system")
        node = self.builder.add("app", parent=root, contracts=CONTRACT)
        tree = self.builder.finish()
        layer = self.layer_of(tree)
        claim(tree, layer, self.policy, node, self.evidence(), "Coordinator")
        decide(tree, layer, node, "approved", "ivo", "looks right")
        save_layer(layer)

        reloaded = load_layer(tree.intent_dir)
        self.assertEqual(reloaded.claim_of(node).by, "Coordinator")
        self.assertEqual(reloaded.acceptance_of(node).decision, "approved")
        self.assertEqual(compute_states(tree, reloaded, self.policy)[node].state, "realized")

    def test_an_empty_layer_is_written_and_read_back(self):
        self.builder.add("system")
        tree = self.builder.finish()
        layer = self.layer_of(tree)
        save_layer(layer)
        self.assertEqual(load_layer(tree.intent_dir).entries, {})

    def test_prune_drops_entries_for_nodes_that_left(self):
        root = self.builder.add("system")
        node = self.builder.add("app", parent=root, contracts=CONTRACT)
        tree = self.builder.finish()
        layer = self.layer_of(tree)
        claim(tree, layer, self.policy, node, self.evidence(), "Coordinator")

        tree.nodes[node].status = "superseded"
        self.assertEqual(prune(tree, layer), [node])


class ConsistencyTest(RealizationTestCase):
    def test_a_consistent_layer_reports_nothing(self):
        root = self.builder.add("system")
        tree = self.builder.finish()
        layer = self.layer_of(tree)
        claim(tree, layer, self.policy, root, self.evidence(), "Coordinator")
        self.assertEqual(check_layer(tree, layer, self.policy), [])

    def test_acceptance_signed_by_an_agent_is_reported(self):
        root = self.builder.add("system")
        tree = self.builder.finish()
        layer = self.layer_of(tree)
        claim(tree, layer, self.policy, root, self.evidence(), "Coordinator")
        decide(tree, layer, root, "approved", "ivo", None)
        layer.acceptance_of(root).by = "Grader"

        problems = check_layer(tree, layer, self.policy)
        self.assertTrue(any(problem.startswith("R5") for problem in problems))

    def test_an_entry_for_an_unknown_node_is_reported(self):
        root = self.builder.add("system")
        tree = self.builder.finish()
        layer = self.layer_of(tree)
        claim(tree, layer, self.policy, root, self.evidence(), "Coordinator")
        layer.entries["i9999"] = layer.entries.pop(root)

        problems = check_layer(tree, layer, self.policy)
        self.assertTrue(any(problem.startswith("R1") for problem in problems))

    def test_vanished_evidence_is_reported(self):
        root = self.builder.add("system")
        tree = self.builder.finish()
        layer = self.layer_of(tree)
        claim(tree, layer, self.policy, root, self.evidence(), "Coordinator")
        (tree.root_dir / "doc/runs/20260816-1200-demo/grader.md").unlink()

        problems = check_layer(tree, layer, self.policy)
        self.assertTrue(any(problem.startswith("R3") for problem in problems))


class ScopeInteractionTest(RealizationTestCase):
    def test_scope_guard_always_allows_the_realization_layer(self):
        self.builder.add("system")
        tree = self.builder.finish()
        run_dir = tree.root_dir / "doc/runs/20260816-1200-demo"
        run_dir.mkdir(parents=True, exist_ok=True)

        allowed = allowed_paths(tree, run_dir, Declaration(outputs=["src/app.py"]))
        self.assertIn("doc/intent/_realization.yaml", allowed)


if __name__ == "__main__":
    unittest.main()
