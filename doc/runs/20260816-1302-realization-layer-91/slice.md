# Slice for i0004 — Intent tooling

- path: `i0001/i0004`
- depth: 1
- realization: not_claimed

## Intent nodes (read as truth)

- `doc/intent/nodes/i0001-harness.md`
- `doc/intent/nodes/i0004-intent-tooling.md`

## Code owned by this node

- `tools/README.md`
- `tools/checks/hook_checks.py`
- `tools/checks/template_checks.py`
- `tools/intent/__init__.py`
- `tools/intent/cli.py`
- `tools/intent/coverage.py`
- `tools/intent/generate.py`
- `tools/intent/main.py`
- `tools/intent/miniyaml.py`
- `tools/intent/model.py`
- `tools/intent/realization.py`
- `tools/intent/scope.py`
- `tools/intent/slicing.py`
- `tools/intent/tests/__init__.py`
- `tools/intent/tests/helpers.py`
- `tools/intent/tests/test_miniyaml.py`
- `tools/intent/tests/test_realization.py`
- `tools/intent/tests/test_tools.py`
- `tools/intent/tests/test_validate.py`
- `tools/intent/validate.py`

## Tests owned by this node

- `tools/intent/tests/__init__.py`
- `tools/intent/tests/helpers.py`
- `tools/intent/tests/test_miniyaml.py`
- `tools/intent/tests/test_realization.py`
- `tools/intent/tests/test_tools.py`
- `tools/intent/tests/test_validate.py`

## Contracts in force

- `i0001` c1: Relative links inside rules and skills resolve to existing files — `cmd: python3 tools/checks/template_checks.py --root .`
- `i0001` c2: Cursor discovers rules and skills through the .cursor symlinks — `cmd: python3 tools/checks/template_checks.py --root .`
- `i0004` c1: Node front matter survives a dump and parse round trip unchanged — `tools/intent/tests/test_miniyaml.py::test_dump_then_parse`
- `i0004` c2: Constructs outside the supported YAML subset are rejected, never ignored — `tools/intent/tests/test_miniyaml.py::test_anchor_is_rejected`
- `i0004` c3: A structurally correct tree produces no validator errors — `tools/intent/tests/test_validate.py::test_minimal_valid_tree_has_no_errors`
- `i0004` c4: code_paths may overlap only along the ancestor chain, never between siblings — `tools/intent/tests/test_validate.py::test_siblings_may_not_overlap`
- `i0004` c5: A contract pointing at a missing test is an error, not a warning — `tools/intent/tests/test_validate.py::test_contract_pointing_at_missing_test_is_rejected`
- `i0004` c6: A slice carries ancestors and semantic dependencies but never siblings — `tools/intent/tests/test_tools.py::test_slice_contains_ancestors_and_uses_but_not_siblings`
- `i0004` c7: Path and depth exist only in generated views, never in a node file — `tools/intent/tests/test_tools.py::test_index_holds_derived_path_and_depth`
- `i0004` c8: A change of a node's meaning invalidates the claim that it was realized — `tools/intent/tests/test_realization.py::test_changing_the_meaning_makes_a_claim_stale`
- `i0004` c9: An unproven ancestor never blocks a proven child; only changed wording propagates — `tools/intent/tests/test_realization.py::test_unproven_ancestor_does_not_block_a_child`
- `i0004` c10: Invalidation across a uses edge stops after one hop and only on a contract change — `tools/intent/tests/test_realization.py::test_uses_propagation_stops_after_one_hop`
- `i0004` c11: A contract whose enforcer disappeared reaches the worklist instead of staying realized — `tools/intent/tests/test_realization.py::test_a_broken_node_appears_in_the_worklist`
- `i0004` c12: A realization claim signed by the Coder is refused — `tools/intent/tests/test_realization.py::test_coder_may_not_claim_its_own_work`
- `i0004` c13: A human acceptance signed with an agent role is refused — `tools/intent/tests/test_realization.py::test_an_agent_may_not_accept`
- `i0004` c14: The scope guard always allows the realization layer, so a run cannot trip its own gate — `tools/intent/tests/test_realization.py::test_scope_guard_always_allows_the_realization_layer`

Anything outside this list is not part of the task context.
