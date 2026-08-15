---
id: i0002
parent: i0001
slug: rules
title: Rules
status: current
uses: []
talks_to: []
superseded_by: null
contracts:
  - id: c1
    text: "Every rule declares its activation: description, globs, or alwaysApply true"
    enforced_by: "cmd: python3 tools/checks/template_checks.py --root ."
  - id: c2
    text: "An always-applied rule stays within 150 lines, a scoped rule within 250"
    enforced_by: "cmd: python3 tools/checks/template_checks.py --root ."
code_paths: ["rules/"]
test_paths: []
open_questions: []
---

# Rules

## Refines
The part of the harness that is loaded into an agent's context automatically, without
being asked for.

## Meaning
Rules are standing constraints: what always holds, regardless of the task at hand. They
are numbered by topic so that the ordering communicates precedence to a reader, and each
one declares how it is activated — always, by file pattern, or on request.

Activation is the scarce resource. Everything marked always-applied is paid for in every
single request, so the size limit is not cosmetics: it is the budget that keeps the
permanently loaded context small enough to still be read rather than skimmed.

## Contracts
The limits are asymmetric on purpose. An always-applied rule competes with the user's
actual question for attention, so it gets 150 lines; a rule loaded only for matching
files can afford 250.

## Non-goals
- Not step-by-step procedures — those are skills, loaded when relevant.
- Not project-specific conventions — those belong in the consuming project's own rules
  or in its `DESIGN_RULES.md`.

## Open questions
