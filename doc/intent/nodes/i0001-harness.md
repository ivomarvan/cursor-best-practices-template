---
id: i0001
parent: null
slug: harness
title: Cursor agent harness
status: current
uses: []
talks_to: []
superseded_by: null
contracts:
  - id: c1
    text: "Relative links inside rules and skills resolve to existing files"
    enforced_by: "cmd: python3 tools/checks/template_checks.py --root ."
  - id: c2
    text: "Cursor discovers rules and skills through the .cursor symlinks"
    enforced_by: "cmd: python3 tools/checks/template_checks.py --root ."
code_paths: []
test_paths: []
open_questions: []
---

# Cursor agent harness

## Meaning
A shared, versioned harness that shapes how AI agents work on software: what they must
know before touching code, how work is decomposed, and what counts as proof that the
work is done. It is consumed by other repositories, normally as a git submodule mounted
at `.cursor/`, so its own correctness is a prerequisite for every project that uses it.

The harness is deliberately not a framework the product code depends on. Nothing here is
imported at runtime; everything here is read by an agent or executed as a check.

## Contracts
Both contracts protect discoverability rather than content. A rule nobody loads and a
link that leads nowhere are worse than a missing rule, because they create the
appearance of guidance.

## Non-goals
- Not a project template: it ships no application scaffolding, no dependency manifest
  and no CI definition for the consuming project.
- Not a runtime library: no product imports anything from here.
- Not a model catalogue authority: which model plays which role is a Human decision
  recorded in `AGENT_MODELS.md`, not an invariant of this tree.

## Open questions
