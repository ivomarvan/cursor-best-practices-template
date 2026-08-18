---
run: 20260818-0853-harness-and-hooks-audit-86
intent_ids: [i0001, i0002, i0003, i0004, i0005]
complexity: high
opened: 2026-08-18
---

# Request

The last run of this phase. Afterwards the intent tree owes nothing: every node is claimed
with evidence, every contract's enforcer has been audited for reach, and no methodology
text carries a known ambiguity.

## A — audit the four contracts nobody has ever checked, then claim `i0001` and `i0005`

Three of five nodes are `realized`. The two that remain — `i0001` (the root) and `i0005`
(git hooks) — carry four contracts between them, and all four are enforced by `cmd:`:

- `i0001` `c1`: relative links inside rules and skills resolve to existing files
- `i0001` `c2`: Cursor discovers rules and skills through the `.cursor` symlinks
- `i0005` `c1`: the commit-msg hook removes agent attribution and keeps everything else
- `i0005` `c2`: every shipped hook is executable

A `cmd:` enforcer is the weakest thing in this tree, and the tooling says so out loud:
`enforcer_problem` returns `None` for anything starting with `cmd:` without looking at what
the command does, because whether it holds "cannot be decided by looking at the file
system". `cmd: true` would satisfy the validator. These four are therefore the only
contracts here whose reach has never been examined by anything.

Examine it. For each of the four, find every place the sentence speaks about and prove by
mutation that the named command fails there. Concretely and non-exhaustively: does the link
check cover skills as well as rules, relative links in every syntax the files actually use,
and links inside the run-artifact tiers? Does the symlink check notice a symlink replaced by
a real directory, and a symlink pointing at the wrong place, not merely a missing one? Does
the commit-msg check prove **both** halves — attribution removed *and* everything else kept,
including the `Intent:` and `Run:` trailers? Does "every shipped hook" mean every file under
`hooks/`, including `session-start.sh` and anything added later, or only the ones the check
happens to name?

Where a check is short, lengthen the check — do not narrow the sentence. Where a sentence
genuinely claims more than it should, say so and stop; narrowing a contract is the Human's
decision, and this run has no authorisation for one.

Then, and only then, claim both nodes. A claim recorded because the gates were green would
be exactly the rubber stamp this whole phase has been spent removing: `coverage 28/28` means
every contract has an enforcer, not that every enforcer reaches every place its sentence
speaks about.

## B — close the three follow-ups from the previous two runs

Written up in `doc/runs/20260817-2334-review-craft-and-claim-order-e2/review.md`; read them
there rather than re-deriving them.

- **FU-B** — `i0004` `c12` ("A realization claim signed by the Coder is refused") has two
  derivation sites: `claim()` in `tools/intent/realization.py`, which the suite reaches, and
  the `R6` report in `check()`, which it does not. A mutation at the second site leaves the
  suite green. The Adversary demonstrated by hand-writing `by: Coder` into the layer that the
  sentence is **true** in both directions, so this is a missing test, not a missing
  behaviour. Add the test.
- **FU-C** — the new Step 3 of `skills/ice-review/SKILL.md` asks whether a sentence is false
  **now**, but a mutation only shows what *would* happen. The step gives no way to measure
  the predicate it uses. The Adversary proposes a sentence; it is one line at the end of
  point 1.
- **FU-D** — the `skills/ice-run/SKILL.md` checklist asks for `request.md` as a file, while
  `rules/07-run-artifacts.mdc` gives a `low` run `request` as a *section* of `run.md`. The
  ambiguity predates both runs. Resolve it in whichever direction is right and make both
  files agree.

## Constraint

Every change is a tightening or a clarification. No contract text may promise less after
this run than it does now. Every enforcer that changes needs failing-test evidence: a
mutation that makes it fail, re-runnable by the Adversary.

## Out of scope

Everything the Human moved to `doc/new_ideas/`: a `--base` option for the scope guard,
contracts covering the derived path printed by `render_slice` and the `owner` command, and
the wording of the constraint table in `AGENT_MODELS.md`. Also out of scope: the previous
runs' committed artifacts, which are audit records and are not rewritten.
