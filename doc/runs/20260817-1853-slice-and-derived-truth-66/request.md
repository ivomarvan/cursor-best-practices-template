---
run: 20260817-1853-slice-and-derived-truth-66
intent_ids: [i0004]
complexity: high
opened: 2026-08-17
---

# Request

Close the last three places where node `i0004` states something the code does not do, or
proves less than the sentence promises. All three were found by earlier Adversary reviews
and carried in run status files instead of in the tree. This run empties that queue; after
it, every contract on `i0004` is true and reached by its enforcer.

## F1 — `c6` is false and the node's own test suite disproves it

`c6` reads *"A slice carries ancestors and semantic dependencies but never siblings"*.
`build_slice` in `tools/intent/slicing.py` also collects **incoming** `talks_to` edges, so
a sibling that talks to the node is in the slice. `test_slice_includes_incoming_talks_to`
proves exactly that. The enforcer named by `c6` only passes because its fixture gives the
sibling no edge at all — it tests a sibling with no reason to be there, not the rule the
sentence states.

The Human has approved reformulating `c6`. The new sentence has to say what the slice
actually does: membership follows declared edges and the ancestor chain, and kinship alone
is not a reason to be included. Whether that is one contract or two is the Planner's call
under the rule already written in `i0004` — a sentence with two halves needs one test that
proves both, or it is two contracts.

## F2 — the index derives `depth` in two places and the enforcer reaches one

`build_index` in `tools/intent/generate.py` computes a derived depth for the node entry
and, separately, for every row of `reverse_code_map`, where it decides the sort order that
makes the deepest owner win. `c7` says the generated index carries a derived path and
depth; `test_index_holds_derived_path_and_depth` only looks at the node entry. A change to
the reverse row's depth passes the suite today.

## F3 — `c19` does not apply to node files under `_retired/`

`c19` says a path or depth written into a node file is reported as an unknown field.
`_check_identity` in `tools/intent/validate.py` iterates `tree.nodes` only, so a retired
node file is never read for unknown fields. Note the trap: retired nodes deliberately fail
other identity rules (the registry marks them retired), so the fix is not to run the whole
identity check over `tree.retired`. Only the unknown-field report should reach them, or
`c19` must say it applies to current nodes.

## Constraint

Every fix is a tightening except the `c6` reformulation, which the Human approved because
the present wording is untrue. Nothing else in the tree may promise less after this run
than it does now. Each contract that changes needs failing-test evidence: a mutation that
makes its enforcer fail, re-runnable by the Adversary.

## Out of scope

Ideas the Human moved to `doc/new_ideas/` and does not want in this run: a `--base` option
for the scope guard, contracts covering the derived path printed by `render_slice` and the
`owner` command, and the wording of the constraint table in `AGENT_MODELS.md`.
