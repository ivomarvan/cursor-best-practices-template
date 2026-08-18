---
run: 20260817-2334-review-craft-and-claim-order-e2
intent_ids: [i0002, i0003]
complexity: high
opened: 2026-08-17
---

# Request

Write three things into the methodology that it currently relies on someone remembering.
All three were decided by the Human; none of them is a new idea invented by this run. This
is the last methodology debt before the version closes, so after this run the harness owes
nothing that lives only in a chat transcript or a run status file.

## R5 — `grader.md` is the Coordinator's artifact, never the Coder's

The Grader is a machine gate, and its whole value is that nobody who wants the result to be
green produces it. Today `skills/ice-run/SKILL.md` step 7 tells the Coordinator to run the
gates and write the raw output, but nothing says the Coder may **not** write that file, and
in a recent run the Coder produced its evidence under a name one letter away from
`grader.md`. Say it explicitly, in the place a Coder reads: the Coder's own measurements
belong in its own file and in `report.md`; `grader.md` is written by the Coordinator from
commands it ran itself.

## R6 — the realization claim belongs after independent review, not before it

`skills/ice-run/SKILL.md` step 7 orders the Coordinator to record `realization claim` as
soon as `grader.md` is green, and the Adversary starts only in step 8. In run
`20260817-1853-slice-and-derived-truth-66` node `i0004` therefore reported `realized`
continuously across two `REQUEST CHANGES` verdicts and four blockers.

The hole is not cosmetic and the Adversary of that run argued it in four parts, all
verified: a claim's fingerprint covers only the node's **text**, so fixing the blockers in
tests never moves it and a false claim can never redden by itself; there is no `unclaim`
command, so a reviewer has no mechanical way to withdraw one; the only machine precondition
of `claim` is that enforcers are reachable, not that an enforcer proves its sentence — and
that judgement is exactly what the review produces; and meanwhile `realization worklist`
answers "nothing left on this node" to a Human asking what to do next.

Move the claim to step 9, after `review.md` exists with a verdict. Make sure the ordering
is stated wherever it can be read in isolation — the skill's step list, its output
checklist, and `rules/07-realization.mdc` if that file describes when a claim is recorded.
The Human chose the smallest fix: reorder, do not add an `unclaim` command.

## R7 — write down the review technique that has found every real defect here

The Adversary in this repository has only ever found defects when its briefing told it, in
so many words, to **read each contract sentence against the code and find every place in
the codebase where that sentence could be true or false** — and that the defect is usually
the same claim repaired in one view while it leaks in a neighbouring one, a second
derivation site, or an unexercised branch. With that instruction: four blockers in the last
run, four in the one before. It currently lives in the Coordinator's prompt, which means it
works only when the Coordinator remembers to type it. It belongs in
`skills/ice-review/SKILL.md`.

Two further practices from the same run earned their place next to it, and both are about
making a review terminate honestly rather than about finding more:

- The check is not "does the test pass" but "would this test fail if the sentence became
  false" — demonstrated by a mutation, in every place the sentence reaches. A review that
  re-runs the suite has verified nothing the Grader had not already verified.
- When a review reaches its last permitted round, it should name the complete set of places
  the contract reaches and mark each one closed or open. That table is what let the last
  run end in agreement instead of in a fourth round; without it, "one more corner" has no
  stopping rule.

Keep this proportionate. `skills/ice-review/SKILL.md` is a skill under `i0003`, which
contracts a 500-line limit, and a skill nobody finishes reading has no effect.

## Constraint

This run changes methodology text only. It writes no production code and adds no tooling —
in particular it does **not** add `realization unclaim`, which the Human considered and
declined. Node `i0002` is currently `realized` and its contracts constrain rule length;
`i0003` contracts skill length. Both limits must still hold when this run ends, and the
Grader proves it.

## Out of scope

The two follow-ups recorded in the previous run's `review.md` (the empty
`for_implementation=True` branch, and the `c19` predicate matching free message text), and
everything the Human moved to `doc/new_ideas/`.
