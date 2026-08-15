---
id: i0005
parent: i0001
slug: git-hooks
title: Git hooks
status: current
uses: []
talks_to: []
superseded_by: null
contracts:
  - id: c1
    text: "The commit-msg hook removes agent attribution and keeps everything else"
    enforced_by: "cmd: python3 tools/checks/hook_checks.py --root ."
  - id: c2
    text: "Every shipped hook is executable"
    enforced_by: "cmd: python3 tools/checks/hook_checks.py --root ."
code_paths: ["hooks/"]
test_paths: []
open_questions: []
---

# Git hooks

## Refines
The part of the harness that acts at git boundaries, where a rule alone cannot reach.

## Meaning
Hooks enforce what an agent cannot be trusted to remember. The commit-msg hook strips the
tool attribution that Cursor injects automatically, so the history records the author who
is accountable for the change rather than the editor that typed it. The session hook
surfaces project state at the start of a conversation.

They are activated per clone with `git config --local core.hooksPath .cursor/hooks/git`;
git deliberately does not let a repository install hooks by itself.

## Contracts
The first contract is written as behaviour, not as a file property: the hook must remove
the attribution **and** leave the intent trailers intact. Half of that is easy to satisfy
by deleting too much, which is why the check asserts both directions.

## Non-goals
- Not a substitute for CI: hooks run locally and can be bypassed with `--no-verify`.
- Not a policy engine — commit conventions live in the git rule.

## Open questions
