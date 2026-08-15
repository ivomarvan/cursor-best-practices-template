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
    text: "code_paths may overlap only along the ancestor chain, never between siblings"
    enforced_by: "tools/intent/tests/test_validate.py::test_siblings_may_not_overlap"
  - id: c5
    text: "A contract pointing at a missing test is an error, not a warning"
    enforced_by: "tools/intent/tests/test_validate.py::test_contract_pointing_at_missing_test_is_rejected"
  - id: c6
    text: "A slice carries ancestors and semantic dependencies but never siblings"
    enforced_by: "tools/intent/tests/test_tools.py::test_slice_contains_ancestors_and_uses_but_not_siblings"
  - id: c7
    text: "Path and depth exist only in generated views, never in a node file"
    enforced_by: "tools/intent/tests/test_tools.py::test_index_holds_derived_path_and_depth"
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
validation, id allocation, generated views, context slices, the scope guard and coverage.
`tools/checks/` implements the contracts this repository declares about itself.

The tooling has no third-party dependencies, deliberately. It is the thing that checks
whether a project is in a valid state, so it must run before that project has an
environment, and in a consuming repository it lives inside a submodule where installing
packages would be someone else's decision. The restricted YAML subset for node front
matter exists for the same reason.

## Contracts
The contracts describe behaviour a future change could plausibly break, not the shape of
the code. Two of them encode decisions that cost real thought: overlapping `code_paths`
are legal along the ancestor chain but not between siblings, and derived data such as
path and depth is generated rather than stored, so inserting a level of abstraction does
not rewrite an entire subtree.

## Non-goals
- Not a test runner: which commands prove a project correct is listed in its `VERIFY.md`.
- Not a linter for product code.
- The tooling never reads `.cursor/`: a submodule may carry its own tree, and two
  registries in one project would make every id ambiguous.

## Open questions
