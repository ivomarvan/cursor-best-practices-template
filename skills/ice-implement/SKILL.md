---
name: ice-implement
description: >-
  Implement one ICE run as the Coder: read only the slice, write code and tests, produce
  failing-test evidence, fill the Definition of Done and write report.md. Use when a plan
  has been accepted and it is time to write code, or when the Human says "implementuj",
  "naprogramuj to", "implement this task".
---

# Skill: Implement a run (Coder)

You are the **Coder**. You write code and tests inside the boundaries of the plan. You do
not change `current` intent nodes and you never start your own review.

Tool prefix (`TOOL`): `python3 .cursor/tools/intent/cli.py` in a project,
`python3 tools/intent/cli.py` inside the template repo.

## Prerequisites

- `plan.md` in the run directory, with `outputs` and `incidental` declared.
- `slice.md` in the run directory — that is your whole context.
- `VERIFY.md` in the project root.

## Step 1 — Read the slice, nothing else

The slice holds the ancestor chain, semantic dependencies, the code and tests this node
owns, and the contracts in force. Anything outside it is not your context. If you need a
file to compile, you may open it — but you may not use it to reinterpret the intent.

Record in `report.md` which files you actually read.

## Step 2 — Stop conditions (check before writing code)

Stop and report instead of improvising when:

- the plan contradicts a contract in the slice;
- a node in the slice has an open question touching your task;
- you would have to change a file outside `outputs` and `incidental`;
- you would have to weaken a contract or edit a `current` node.

A stopped run is a much smaller problem than a silent scope expansion.

## Step 3 — Failing-test evidence first

For every bug fix and every new behaviour, show the new test failing on unchanged code:

```bash
# write the test, then run it before the implementation exists
<test command from VERIFY.md>   # must fail — save this output
```

Paste that output into `report.md` under Evidence. A test that passes on unchanged code
proves nothing. This is not full test-driven development — it is its cheap, load-bearing
part.

## Step 4 — Implement

Follow `01-general-programming.mdc` and the language rules. Keep the diff inside the
declared outputs. If a contract in the slice says `enforced_by: <test>`, that test must
exist and actually exercise the contract.

## Step 5 — Self-check before handing over

```bash
$TOOL validate
$TOOL scope --run doc/runs/<run> --node <iNNNN>
# every command from VERIFY.md
```

These same commands will be re-run by the Grader. Numbers you write in the report are
claims; the Grader's log is the record.

## Step 6 — Report and Definition of Done

Write `report.md` following the structure in `07-run-artifacts.mdc`: what was
implemented, inputs and outputs (one path per bullet), methods and decisions, code
references, evidence, Definition of Done.

Tick a Definition of Done item only when the artifact or command behind it exists. An
unticked box is information; a falsely ticked box is the failure this whole process
exists to prevent.

## Output checklist

- [ ] Diff stays inside `outputs` + `incidental`
- [ ] No `current` intent node modified
- [ ] Failing-test evidence captured for every new test
- [ ] All `VERIFY.md` commands pass locally
- [ ] `report.md` written; every ticked Definition of Done item has an artifact

## Additional resources

- [../../rules/07-run-artifacts.mdc](../../rules/07-run-artifacts.mdc)
- [../../rules/09-testing.mdc](../../rules/09-testing.mdc)
- [../../rules/01-general-programming.mdc](../../rules/01-general-programming.mdc)
