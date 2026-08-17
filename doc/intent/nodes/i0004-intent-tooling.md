---
id: i0004
parent: i0001
slug: intent-tooling
title: Intent tooling
status: current
uses: []
talks_to: []
superseded_by: null
contracts:
  - id: c1
    text: "Node front matter survives a dump and parse round trip unchanged"
    enforced_by: "tools/intent/tests/test_miniyaml.py::test_dump_then_parse"
  - id: c2
    text: "Constructs outside the supported YAML subset are rejected, never ignored"
    enforced_by: "tools/intent/tests/test_miniyaml.py::test_anchor_is_rejected"
  - id: c3
    text: "A structurally correct tree produces no validator errors"
    enforced_by: "tools/intent/tests/test_validate.py::test_minimal_valid_tree_has_no_errors"
  - id: c4
    text: "code_paths of two different nodes may not overlap unless one is an ancestor of the other"
    enforced_by: "tools/intent/tests/test_validate.py::test_overlap_outside_the_ancestor_chain_is_rejected"
  - id: c5
    text: "A contract pointing at a missing test is an error, not a warning"
    enforced_by: "tools/intent/tests/test_validate.py::test_contract_pointing_at_missing_test_is_rejected"
  - id: c6
    text: "A slice carries ancestors and semantic dependencies but never siblings"
    enforced_by: "tools/intent/tests/test_tools.py::test_slice_contains_ancestors_and_uses_but_not_siblings"
  - id: c7
    text: "The generated index carries a path and a depth derived from the parent chain"
    enforced_by: "tools/intent/tests/test_tools.py::test_index_holds_derived_path_and_depth"
  - id: c8
    text: "A change of a node's meaning invalidates the claim that it was realized"
    enforced_by: "tools/intent/tests/test_realization.py::test_changing_the_meaning_makes_a_claim_stale"
  - id: c9
    text: "An unproven ancestor never blocks a proven child"
    enforced_by: "tools/intent/tests/test_realization.py::test_unproven_ancestor_does_not_block_a_child"
  - id: c10
    text: "Invalidation across a uses edge stops after one hop"
    enforced_by: "tools/intent/tests/test_realization.py::test_uses_propagation_stops_after_one_hop"
  - id: c11
    text: "A contract whose enforcer disappeared reaches the worklist instead of staying realized"
    enforced_by: "tools/intent/tests/test_realization.py::test_a_broken_node_appears_in_the_worklist"
  - id: c12
    text: "A realization claim signed by the Coder is refused"
    enforced_by: "tools/intent/tests/test_realization.py::test_coder_may_not_claim_its_own_work"
  - id: c13
    text: "A human acceptance signed with an agent role is refused"
    enforced_by: "tools/intent/tests/test_realization.py::test_an_agent_may_not_accept"
  - id: c14
    text: "The scope guard always allows the realization layer, so a run cannot trip its own gate"
    enforced_by: "tools/intent/tests/test_realization.py::test_scope_guard_always_allows_the_realization_layer"
  - id: c15
    text: "A change of contracts on a uses target opens its consumer"
    enforced_by: "tools/intent/tests/test_realization.py::test_uses_target_contract_change_opens_the_consumer"
  - id: c16
    text: "A change of meaning on a uses target never reaches its consumer"
    enforced_by: "tools/intent/tests/test_realization.py::test_uses_target_meaning_change_leaves_the_consumer_alone"
  - id: c17
    text: "An enforcer renamed to a longer symbol counts as missing, not as still present"
    enforced_by: "tools/intent/tests/test_realization.py::test_a_renamed_enforcer_symbol_makes_a_node_broken"
  - id: c18
    text: "code_paths of a node and any of its ancestors may overlap"
    enforced_by: "tools/intent/tests/test_validate.py::test_the_ancestor_chain_may_overlap"
  - id: c19
    text: "A path or depth written into a node file is reported as an unknown field"
    enforced_by: "tools/intent/tests/test_validate.py::test_derived_fields_in_a_node_file_are_reported"
  - id: c20
    text: "A path written into a node file never becomes the node's path in a generated view"
    enforced_by: "tools/intent/tests/test_tools.py::test_a_path_in_a_node_file_does_not_reach_a_generated_view"
code_paths: ["tools/"]
test_paths: ["tools/intent/tests/"]
open_questions: []
---

# Intent tooling

## Refines
The executable part of the harness: the commands that turn the methodology from advice
into something that can fail a build.

## Meaning
Two families of scripts live here. `tools/intent/` implements the intent tree itself —
validation, id allocation, generated views, context slices, the scope guard, coverage and
the realization layer that records what the project already fulfils. `tools/checks/`
implements the contracts this repository declares about itself.

The tooling has no third-party dependencies, deliberately. It is the thing that checks
whether a project is in a valid state, so it must run before that project has an
environment, and in a consuming repository it lives inside a submodule where installing
packages would be someone else's decision. The restricted YAML subset for node front
matter exists for the same reason.

## Contracts
The contracts describe behaviour a future change could plausibly break, not the shape of
the code. Two decisions in there cost real thought and take five contracts between them:
overlapping `code_paths` are legal along the ancestor chain and nowhere else, and derived
data such as path and depth is generated rather than stored, so inserting a level of
abstraction does not rewrite an entire subtree.

The realization contracts (`c8`–`c17`) guard the same principle one layer up. Only
assertions are stored; staleness is computed from fingerprints, so an inconsistent state
cannot be written down. Invalidation follows a change of **wording**, never a state —
otherwise an unproven root would forbid proving anything beneath it, and one edit to a
widely used node would redden the whole tree.

A contract may claim only what its `enforced_by` proves. What decides is not the shape of
the sentence but the reach of the test: where a sentence has two halves, one and the same
test must prove both, or the halves belong to two contracts. A half that follows directly
from the other, using only the terms the contract itself names, is not a second claim and
is not split. `c14` is that case and the tightest one here: "cannot trip its own gate"
follows from "always allows", because the gate in question is the run's own write.

## Non-goals
- Not a test runner: which commands prove a project correct is listed in its `VERIFY.md`.
- Not a linter for product code.
- Not a build dashboard: the realization layer records that an enforcer exists, never
  whether it passed a minute ago. That changes with every commit and belongs to the
  Grader.
- The tooling never reads `.cursor/`: a submodule may carry its own tree, and two
  registries in one project would make every id ambiguous.

## Open questions
