---
id: i0003
parent: i0001
slug: skills
title: Skills
status: current
uses: [i0002]
talks_to: []
superseded_by: null
contracts:
  - id: c1
    text: "Every skill directory holds a SKILL.md declaring name and description"
    enforced_by: "cmd: python3 tools/checks/template_checks.py --root ."
  - id: c2
    text: "A skill stays within 500 lines"
    enforced_by: "cmd: python3 tools/checks/template_checks.py --root ."
code_paths: ["skills/"]
test_paths: []
open_questions: []
---

# Skills

## Refines
The part of the harness that is loaded on demand: procedures an agent reads when it
recognises the situation they describe.

## Meaning
A skill is a procedure with a trigger. Its `description` is not documentation — it is the
matching surface an agent uses to decide whether to read the rest, so a skill with a
vague description is functionally invisible even though the file exists.

Skills carry the ICE roles: driving a run, changing the intent tree, implementing, and
reviewing. Each names the role it plays and the boundaries of that role, because the
separation between who writes and who judges is what makes the process worth more than
a single long prompt.

## Contracts
Both contracts are about discoverability and size, mirroring the rules node: a skill that
cannot be found does nothing, and a skill too long to read gets skimmed.

## Non-goals
- Not standing constraints — a skill that must always hold is a rule in the wrong place.
- Not a place to restate a rule: skills cite rules, they do not copy them.

## Open questions
