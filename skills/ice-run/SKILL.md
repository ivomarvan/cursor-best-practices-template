---
name: ice-run
description: >-
  Drive one ICE run end to end as the Coordinator: route the request to an intent node,
  classify complexity, run the intent change when needed, plan, implement, grade,
  review and close. Use when the Human asks for any change to a project that has an
  intent tree, or says "spusť běh", "start a run", "udělej změnu podle ICE".
---

# Skill: Run one ICE change (Coordinator)

You are the **Coordinator**. You start other roles as subagents, read their files, and
never write production code yourself.

## Prerequisites

- The project has `doc/intent/` with at least a root node. If not, run `intent-change`
  first to create the root — no production code before an approved root.
- `VERIFY.md` exists in the project root and lists the verification commands.
- Model per role resolved from `AGENT_MODELS.md` (see `00-model-policy.mdc`).

Tool prefix used below (`TOOL`): `python3 .cursor/tools/intent/cli.py` in a project,
`python3 tools/intent/cli.py` inside the template repo.

## Step 1 — Create the run directory

```bash
mkdir -p doc/runs/$(date +%Y%m%d-%H%M)-<slug>-$(openssl rand -hex 1)
```

Write `request.md` in your own words. Never hand the raw chat message to a Coder as a
specification.

## Step 2 — Route

```bash
cat doc/intent/MAP.md
$TOOL owner <path/you/expect/to/change>
$TOOL realization status --node <iNNNN>
```

Name the affected node ids. If no node fits, that is a finding: either a node is missing
(go to Step 4) or the work is outside the project's intent — ask the Human.

When the Human asks "what should we do next?" rather than for a specific change, start
from `$TOOL realization worklist` instead. It lists every node that is unproven, stale,
broken or waiting for acceptance, ancestors first. Take a node marked `ready`; a node
marked `blocked_by iNNNN` waits, because fixing the ancestor may change what it needs.

## Step 3 — Classify complexity

Apply the deterministic triggers in `07-ice-workflow.mdc`. Write the level into the run
front matter. You may raise it later; only the Human may lower it.

## Step 4 — Intent change, if the meaning changed

Find the **highest** node whose contract or meaning the request violates. If there is
one, invoke the `intent-change` skill and do not continue until the tree is `current`
again. Never adjust code so the tree does not have to move.

## Step 5 — Plan

Start the **Planner** with the slice:

```bash
$TOOL slice <iNNNN> --for plan > doc/runs/<run>/slice.md
```

The Planner writes `plan.md`: goal, `outputs`, `incidental`, test spec, Definition of
Done. Check it against the Definition of Ready in `07-run-artifacts.mdc`.

At `medium` and `high`, start the **Critic** on the plan; it writes `critique.md` with
`ACCEPT` or `REVISE`. After the third `REVISE`, escalate to the Human.

## Step 6 — Implement

Start the **Coder** (see the `ice-implement` skill) with `plan.md` and the implementation
slice. The Coder writes code, tests, failing-test evidence and `report.md`.

## Step 7 — Evidence (Grader)

Run the machine gates yourself; do not trust numbers from the report.

```bash
$TOOL validate
$TOOL scope --run doc/runs/<run> --node <iNNNN>
# then every command listed in VERIFY.md
```

Write the raw output to `grader.md`. Failures go back to the Coder — at most three
rounds, then escalate. A scope violation raises the run to `medium` and wakes the
Adversary regardless of the original level.

Once `grader.md` is green, record the realization claim — you, never the Coder:

```bash
$TOOL realization claim <iNNNN> --evidence doc/runs/<run> --by Coordinator
```

The tool refuses a node with an open question or with an unreachable enforcer. Such a
refusal is a finding about the run, not an obstacle to route around.

## Step 8 — Independent review

At `medium` and `high`, start the **Adversary** (skill `ice-review`) with a model that
differs from the Coder's. Give it the plan, the Definition of Done and the diff. It
writes `review.md`. At most three rounds, then escalate.

## Step 9 — Close

Write `status.md`: final state, models used, loop counts, Human gate. Promote any
cross-node decision into an ADR under `doc/architecture/decisions/`. Record a skipped
Human review with its reason. Commit only if the Human asks.

Check whether the node still owes anything:

```bash
$TOOL realization status --node <iNNNN>
```

If acceptance is `pending`, the run closes as `awaiting-acceptance` and you tell the Human
what to look at. **Never** run `realization accept` or `realization affirm` yourself —
both are human judgements and the tool refuses an agent role in `--by`.

If an intent change in Step 4 turned other nodes `stale`, say so: either they belong in
follow-up runs, or the Human affirms them with a reason.

## Output checklist

- [ ] Run directory with `request.md` and either `run.md` (low) or the full set
- [ ] Affected node ids recorded in the front matter (`intent_ids`)
- [ ] `intent validate` and `intent scope` green, logged in `grader.md`
- [ ] Every gate required by the complexity level actually ran
- [ ] Realization claimed for the affected node, or the reason it could not be
- [ ] `status.md` written; skipped Human review has a recorded reason

## Additional resources

- [../../rules/07-ice-workflow.mdc](../../rules/07-ice-workflow.mdc)
- [../../rules/07-run-artifacts.mdc](../../rules/07-run-artifacts.mdc)
- [../../rules/07-realization.mdc](../../rules/07-realization.mdc)
- [../../rules/00-model-policy.mdc](../../rules/00-model-policy.mdc)
