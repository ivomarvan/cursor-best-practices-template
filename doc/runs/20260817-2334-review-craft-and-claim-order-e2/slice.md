# Slice for i0002 — Rules

- path: `i0001/i0002`
- depth: 1
- realization: realized

## Intent nodes (read as truth)

- `doc/intent/nodes/i0001-harness.md`
- `doc/intent/nodes/i0002-rules.md`

## Contracts in force

- `i0001` c1: Relative links inside rules and skills resolve to existing files — `cmd: python3 tools/checks/template_checks.py --root .`
- `i0001` c2: Cursor discovers rules and skills through the .cursor symlinks — `cmd: python3 tools/checks/template_checks.py --root .`
- `i0002` c1: Every rule declares its activation: description, globs, or alwaysApply true — `cmd: python3 tools/checks/template_checks.py --root .`
- `i0002` c2: An always-applied rule stays within 150 lines, a scoped rule within 250 — `cmd: python3 tools/checks/template_checks.py --root .`

Anything outside this list is not part of the task context.

---

# Slice for i0003 — Skills

- path: `i0001/i0003`
- depth: 1
- realization: not_claimed

## Intent nodes (read as truth)

- `doc/intent/nodes/i0001-harness.md`
- `doc/intent/nodes/i0003-skills.md`
- `doc/intent/nodes/i0002-rules.md`

## Contracts in force

- `i0001` c1: Relative links inside rules and skills resolve to existing files — `cmd: python3 tools/checks/template_checks.py --root .`
- `i0001` c2: Cursor discovers rules and skills through the .cursor symlinks — `cmd: python3 tools/checks/template_checks.py --root .`
- `i0003` c1: Every skill directory holds a SKILL.md declaring name and description — `cmd: python3 tools/checks/template_checks.py --root .`
- `i0003` c2: A skill stays within 500 lines — `cmd: python3 tools/checks/template_checks.py --root .`

Anything outside this list is not part of the task context.

---

# Slice for i0004 — Intent tooling

- path: `i0001/i0004`
- depth: 1
- realization: realized

## Intent nodes (read as truth)

- `doc/intent/nodes/i0001-harness.md`
- `doc/intent/nodes/i0004-intent-tooling.md`

## Contracts in force

- `i0001` c1: Relative links inside rules and skills resolve to existing files — `cmd: python3 tools/checks/template_checks.py --root .`
- `i0001` c2: Cursor discovers rules and skills through the .cursor symlinks — `cmd: python3 tools/checks/template_checks.py --root .`
- `i0004` c1: Node front matter survives a dump and parse round trip unchanged — `tools/intent/tests/test_miniyaml.py::test_dump_then_parse`
- `i0004` c2: Constructs outside the supported YAML subset are rejected, never ignored — `tools/intent/tests/test_miniyaml.py::test_anchor_is_rejected`
- `i0004` c3: A structurally correct tree produces no validator errors — `tools/intent/tests/test_validate.py::test_minimal_valid_tree_has_no_errors`
- `i0004` c4: code_paths of two different nodes may not overlap unless one is an ancestor of the other — `tools/intent/tests/test_validate.py::test_overlap_outside_the_ancestor_chain_is_rejected`
- `i0004` c5: A contract pointing at a missing test is an error, not a warning — `tools/intent/tests/test_validate.py::test_contract_pointing_at_missing_test_is_rejected`
- `i0004` c6: A slice carries exactly these intent nodes: the node, its ancestors, its `uses` targets and the far end of every `talks_to` edge — kinship alone adds none — `tools/intent/tests/test_tools.py::test_slice_carries_exactly_ancestors_uses_and_talks_to_ends`
- `i0004` c7: The generated index carries a path and a depth derived from the parent chain — `tools/intent/tests/test_tools.py::test_index_holds_derived_path_and_depth`
- `i0004` c8: A change of a node's meaning invalidates the claim that it was realized — `tools/intent/tests/test_realization.py::test_changing_the_meaning_makes_a_claim_stale`
- `i0004` c9: An unproven ancestor never blocks a proven child — `tools/intent/tests/test_realization.py::test_unproven_ancestor_does_not_block_a_child`
- `i0004` c10: Invalidation across a uses edge stops after one hop — `tools/intent/tests/test_realization.py::test_uses_propagation_stops_after_one_hop`
- `i0004` c11: A contract whose enforcer disappeared reaches the worklist instead of staying realized — `tools/intent/tests/test_realization.py::test_a_broken_node_appears_in_the_worklist`
- `i0004` c12: A realization claim signed by the Coder is refused — `tools/intent/tests/test_realization.py::test_coder_may_not_claim_its_own_work`
- `i0004` c13: A human acceptance signed with an agent role is refused — `tools/intent/tests/test_realization.py::test_an_agent_may_not_accept`
- `i0004` c14: The scope guard always allows the realization layer, so a run cannot trip its own gate — `tools/intent/tests/test_realization.py::test_scope_guard_always_allows_the_realization_layer`
- `i0004` c15: A change of contracts on a uses target opens its consumer — `tools/intent/tests/test_realization.py::test_uses_target_contract_change_opens_the_consumer`
- `i0004` c16: A change of meaning on a uses target never reaches its consumer — `tools/intent/tests/test_realization.py::test_uses_target_meaning_change_leaves_the_consumer_alone`
- `i0004` c17: An enforcer renamed to a longer symbol counts as missing, not as still present — `tools/intent/tests/test_realization.py::test_a_renamed_enforcer_symbol_makes_a_node_broken`
- `i0004` c18: code_paths of a node and any of its ancestors may overlap — `tools/intent/tests/test_validate.py::test_the_ancestor_chain_may_overlap`
- `i0004` c19: A path or depth written into a node file is reported as an unknown field — `tools/intent/tests/test_validate.py::test_derived_fields_in_a_node_file_are_reported`
- `i0004` c20: A path written into a node file never becomes the node's path in a generated view — `tools/intent/tests/test_tools.py::test_a_path_in_a_node_file_does_not_reach_a_generated_view`

Anything outside this list is not part of the task context.
