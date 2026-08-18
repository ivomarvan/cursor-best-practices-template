# coder-evidence.md — raw mutation and VERIFY transcripts

Run: 20260817-2334-review-craft-and-claim-order-e2
Role: Coder

Note: mutations use a byte-exact file backup and restore (not `git checkout`),
so the R5/R6/R7 edits in the working tree stay intact.

---

## Mutation 1 — alwaysApply line limit (i0002 c2)

### Setup
Append 40 blank lines to `rules/07-ice-workflow.mdc` (after R6-h is already applied).

### Command
```
python3 tools/checks/template_checks.py --root .
```
### Output
```
ERROR /home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/rules/07-ice-workflow.mdc: 158 lines exceeds the alwaysApply limit of 150

1 template contract violation(s)
```
### Exit code: 1
### Lines after mutation: 158
### Revert: cp /tmp/ice-workflow.bak → rules/07-ice-workflow.mdc
### git diff --stat -- rules/07-ice-workflow.mdc after revert:
```
 rules/07-ice-workflow.mdc | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
(empty above = working-tree R6-h retained; mutation blank lines gone)
```
### Post-revert: 118 lines

---

## Mutation 2 — broken relative link (i0001 c1)

### Setup
In `skills/ice-review/SKILL.md` Additional resources, replace
`[../../rules/07-realization.mdc](../../rules/07-realization.mdc)` with
`[../../rules/07-realization-x.mdc](../../rules/07-realization-x.mdc)`.
(The path string appears twice on one line — display text and href.)

### Command
```
python3 tools/checks/template_checks.py --root .
```
### Output
```
ERROR /home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/skills/ice-review/SKILL.md: broken link: ../../rules/07-realization-x.mdc

1 template contract violation(s)
```
### Exit code: 1
### Revert: cp /tmp/ice-review.bak → skills/ice-review/SKILL.md
### git diff --stat -- skills/ice-review/SKILL.md after revert:
```
 skills/ice-review/SKILL.md | 50 +++++++++++++++++++++++++++++++++++++++-------
 1 file changed, 43 insertions(+), 7 deletions(-)
(empty above = R7 edits retained; broken link gone)
```

---

## Mutation 3 — bypass Coder claim refusal (i0004 c12)

### Setup
Inside `def claim` only (~line 546), change `by.strip().lower() == "coder"`
to `== "coderx"`. Leave `claim.by.strip().lower() == "coder"` near line 480 untouched.

### Guards before mutation
```
480:            if claim.by.strip().lower() == "coder":
546:    if by.strip().lower() == "coder":
```

### Command
```
python3 -m unittest discover -s tools/intent/tests -t tools
```
### Output
```
............................F.....................................................
======================================================================
FAIL: test_coder_may_not_claim_its_own_work (intent.tests.test_realization.ClaimTest.test_coder_may_not_claim_its_own_work)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_realization.py", line 112, in test_coder_may_not_claim_its_own_work
    with self.assertRaises(TreeError):
         ~~~~~~~~~~~~~~~~~^^^^^^^^^^^
AssertionError: TreeError not raised

----------------------------------------------------------------------
Ran 82 tests in 0.327s

FAILED (failures=1)
```
### Exit code: 1
### Revert: cp /tmp/realization.bak → tools/intent/realization.py
### git diff --stat -- tools/intent/realization.py after revert:
```
 tools/intent/realization.py | 3 ++-
 1 file changed, 2 insertions(+), 1 deletion(-)
(empty above relative to pre-mutation R6-m text = mutation gone)
```
### Guards after revert:
```
480:            if claim.by.strip().lower() == "coder":
546:    if by.strip().lower() == "coder":
```

---

## Green after all three mutations reverted

### unittest
```
..................................................................................
----------------------------------------------------------------------
Ran 82 tests in 0.341s

OK
```
Exit code: 0

### template_checks
```
template contracts satisfied
```
Exit code: 0

---

## VERIFY / DoD commands (post-edit, green tree)

### 1. intent validate
```
python3 tools/intent/cli.py validate
```
#### Output
```

5 node(s): 0 error(s), 0 warning(s)
```
Exit code: 0

### 2. realization check
```
python3 tools/intent/cli.py realization check
```
#### Output
```
realization layer consistent (2 entry/entries)
```
Exit code: 0

### 3. unittest
```
python3 -m unittest discover -s tools/intent/tests -t tools
```
#### Output
```
..................................................................................
----------------------------------------------------------------------
Ran 82 tests in 0.354s

OK
```
Exit code: 0

### 4. template_checks
```
python3 tools/checks/template_checks.py --root .
```
#### Output
```
template contracts satisfied
```
Exit code: 0

### 5. hook_checks
```
python3 tools/checks/hook_checks.py --root .
```
#### Output
```
hook contracts satisfied
```
Exit code: 0

### 6. scope
```
python3 tools/intent/cli.py scope --run doc/runs/20260817-2334-review-craft-and-claim-order-e2
```
#### Output
```
scope clean (8 declared path(s))
```
Exit code: 0

### 7. wc -l outputs
```
wc -l rules/07-ice-workflow.mdc rules/07-realization.mdc rules/07-run-artifacts.mdc skills/ice-run/SKILL.md skills/ice-review/SKILL.md skills/ice-implement/SKILL.md README.md tools/intent/realization.py
```
#### Output
```
  118 rules/07-ice-workflow.mdc
  155 rules/07-realization.mdc
  139 rules/07-run-artifacts.mdc
  156 skills/ice-run/SKILL.md
  126 skills/ice-review/SKILL.md
  108 skills/ice-implement/SKILL.md
  652 README.md
  697 tools/intent/realization.py
 2151 total
```
Exit code: 0

### 9a. canonical full
```
grep -rn once every gate the level requires has passed rules/ skills/ README.md tools/
```
#### Output
```
rules/07-run-artifacts.mdc:87:the run, once every gate the level requires has passed: at `low` the gates themselves, at
rules/07-ice-workflow.mdc:45:| **Coordinator** (parent chat) | start other roles, pick models, count loops, allocate ids, claim realization once every gate the level requires has passed | write production code; grade its own output |
rules/07-realization.mdc:80:| `claim` | Coordinator, once every gate the level requires has passed — at `low` the Grader, above it the Adversary too | the **Coder** — nobody grades their own work |
skills/ice-implement/SKILL.md:98:- [ ] No realization claim written — the Coordinator's, once every gate the level requires has passed
skills/ice-run/SKILL.md:116:Claim once every gate the level requires has passed: at `low` that is the green Grader, at
skills/ice-run/SKILL.md:148:- [ ] Realization claimed in Step 9, once every gate the level requires has passed — or why not
README.md:257:| `claim` | Coordinator, once every gate the level requires has passed — at `low` the Grader, above it the Adversary too | the **Coder** — nobody grades their own work |
tools/intent/realization.py:549:            "the Coordinator claims once every gate the level requires has passed"
grep: tools/intent/__pycache__/realization.cpython-314.pyc: binary file matches
```
Exit code: 0

FULL_COUNT=8
### 9b. canonical sub
```
grep -rn every gate the level requires rules/ skills/ README.md tools/
```
#### Output
```
rules/07-run-artifacts.mdc:87:the run, once every gate the level requires has passed: at `low` the gates themselves, at
rules/07-ice-workflow.mdc:45:| **Coordinator** (parent chat) | start other roles, pick models, count loops, allocate ids, claim realization once every gate the level requires has passed | write production code; grade its own output |
rules/07-realization.mdc:80:| `claim` | Coordinator, once every gate the level requires has passed — at `low` the Grader, above it the Adversary too | the **Coder** — nobody grades their own work |
skills/ice-implement/SKILL.md:98:- [ ] No realization claim written — the Coordinator's, once every gate the level requires has passed
skills/ice-run/SKILL.md:116:Claim once every gate the level requires has passed: at `low` that is the green Grader, at
skills/ice-run/SKILL.md:148:- [ ] Realization claimed in Step 9, once every gate the level requires has passed — or why not
README.md:257:| `claim` | Coordinator, once every gate the level requires has passed — at `low` the Grader, above it the Adversary too | the **Coder** — nobody grades their own work |
tools/intent/realization.py:549:            "the Coordinator claims once every gate the level requires has passed"
grep: tools/intent/__pycache__/realization.cpython-314.pyc: binary file matches
```
Exit code: 0

SUB_COUNT=8

### 10. Grader is green / green Grader
```
Grader is green exit=1
rules/07-run-artifacts.mdc:84:Realization is not ticked by the Coder, and above `low` not by a green Grader alone either.
skills/ice-run/SKILL.md:116:Claim once every gate the level requires has passed: at `low` that is the green Grader, at
```

### 12. claims after the Grader / ruff
```
claims after exit=1
### 12b. ruff check
```
ruff check tools/
```
#### Output
```
[1;32mAll checks passed![0m
```
Exit code: 0

### 12c. ruff format --check
```
ruff format --check tools/
```
#### Output
```
19 files already formatted
```
Exit code: 0

### git diff -- tools/intent/realization.py
```
diff --git a/tools/intent/realization.py b/tools/intent/realization.py
index e017dcf..b680547 100644
--- a/tools/intent/realization.py
+++ b/tools/intent/realization.py
@@ -545,7 +545,8 @@ def claim(
         raise TreeError("claim requires --by")
     if by.strip().lower() == "coder":
         raise TreeError(
-            "the Coder may not claim its own work; the Coordinator claims after the Grader"
+            "the Coder may not claim its own work; "
+            "the Coordinator claims once every gate the level requires has passed"
         )
     if node.open_questions:
         raise TreeError(
```

### 13. claim command location
```
113:$TOOL realization claim <iNNNN> --evidence doc/runs/<run> --by Coordinator
108:## Step 9 — Claim, then close
97:Record no realization claim here. A green gate proves that the commands passed, not that
```

### 15. ice-review steps / no live names
```
22:## Step 1 — Read in the right order
29:## Step 2 — The eight checks
42:## Step 3 — Read each contract sentence against the code
74:## Step 4 — Attack the tests specifically
87:## Step 5 — Verdict
(no slicing.py/talks_to)
```

### 16. unclaim
```
(tools: empty)
rules/07-realization.mdc:90:`unclaim` command. Where a review runs, the claim waits for its verdict — `REQUEST CHANGES`
skills/ice-run/SKILL.md:119:`unclaim`: the fingerprints cover only the node's text, so a claim written against a diff
```

### 17. doc/runs scope
```
?? doc/runs/20260817-2334-review-craft-and-claim-order-e2/
--- name-only for outputs ---
README.md
rules/07-ice-workflow.mdc
rules/07-realization.mdc
rules/07-run-artifacts.mdc
skills/ice-implement/SKILL.md
skills/ice-review/SKILL.md
skills/ice-run/SKILL.md
tools/intent/realization.py
```

### git status --short (full)
```
 M README.md
 M rules/07-ice-workflow.mdc
 M rules/07-realization.mdc
 M rules/07-run-artifacts.mdc
 M skills/ice-implement/SKILL.md
 M skills/ice-review/SKILL.md
 M skills/ice-run/SKILL.md
 M tools/intent/realization.py
?? doc/runs/20260817-2334-review-craft-and-claim-order-e2/
```

---

## Round 2 — fixes B1–B6 (after REQUEST CHANGES)

Touched: `skills/ice-review/SKILL.md`, `rules/07-run-artifacts.mdc`,
`skills/ice-run/SKILL.md`.

### validate
```
python3 tools/intent/cli.py validate
```
#### Output
```

5 node(s): 0 error(s), 0 warning(s)
```
Exit code: 0

### realization check
```
python3 tools/intent/cli.py realization check
```
#### Output
```
realization layer consistent (2 entry/entries)
```
Exit code: 0

### unittest
```
python3 -m unittest discover -s tools/intent/tests -t tools
```
#### Output
```
..................................................................................
----------------------------------------------------------------------
Ran 82 tests in 0.398s

OK
```
Exit code: 0

### template_checks
```
python3 tools/checks/template_checks.py --root .
```
#### Output
```
template contracts satisfied
```
Exit code: 0

### hook_checks
```
python3 tools/checks/hook_checks.py --root .
```
#### Output
```
hook contracts satisfied
```
Exit code: 0

### scope
```
python3 tools/intent/cli.py scope --run doc/runs/20260817-2334-review-craft-and-claim-order-e2
```
#### Output
```
scope clean (8 declared path(s))
```
Exit code: 0

### wc -l touched + all outputs
```
wc -l rules/07-ice-workflow.mdc rules/07-realization.mdc rules/07-run-artifacts.mdc skills/ice-run/SKILL.md skills/ice-review/SKILL.md skills/ice-implement/SKILL.md README.md tools/intent/realization.py
```
#### Output
```
  118 rules/07-ice-workflow.mdc
  155 rules/07-realization.mdc
  141 rules/07-run-artifacts.mdc
  156 skills/ice-run/SKILL.md
  132 skills/ice-review/SKILL.md
  108 skills/ice-implement/SKILL.md
  652 README.md
  697 tools/intent/realization.py
 2159 total
```
Exit code: 0

### DoD 9 greps
```
rules/07-run-artifacts.mdc:89:the run, once every gate the level requires has passed: at `low` the gates themselves, at
rules/07-ice-workflow.mdc:45:| **Coordinator** (parent chat) | start other roles, pick models, count loops, allocate ids, claim realization once every gate the level requires has passed | write production code; grade its own output |
rules/07-realization.mdc:80:| `claim` | Coordinator, once every gate the level requires has passed — at `low` the Grader, above it the Adversary too | the **Coder** — nobody grades their own work |
skills/ice-implement/SKILL.md:98:- [ ] No realization claim written — the Coordinator's, once every gate the level requires has passed
skills/ice-run/SKILL.md:116:Claim once every gate the level requires has passed: at `low` that is the green Grader, at
skills/ice-run/SKILL.md:148:- [ ] Realization claimed in Step 9, once every gate the level requires has passed — or why not
README.md:257:| `claim` | Coordinator, once every gate the level requires has passed — at `low` the Grader, above it the Adversary too | the **Coder** — nobody grades their own work |
tools/intent/realization.py:549:            "the Coordinator claims once every gate the level requires has passed"
FULL=8
rules/07-run-artifacts.mdc:89:the run, once every gate the level requires has passed: at `low` the gates themselves, at
rules/07-ice-workflow.mdc:45:| **Coordinator** (parent chat) | start other roles, pick models, count loops, allocate ids, claim realization once every gate the level requires has passed | write production code; grade its own output |
rules/07-realization.mdc:80:| `claim` | Coordinator, once every gate the level requires has passed — at `low` the Grader, above it the Adversary too | the **Coder** — nobody grades their own work |
skills/ice-implement/SKILL.md:98:- [ ] No realization claim written — the Coordinator's, once every gate the level requires has passed
skills/ice-run/SKILL.md:116:Claim once every gate the level requires has passed: at `low` that is the green Grader, at
skills/ice-run/SKILL.md:148:- [ ] Realization claimed in Step 9, once every gate the level requires has passed — or why not
README.md:257:| `claim` | Coordinator, once every gate the level requires has passed — at `low` the Grader, above it the Adversary too | the **Coder** — nobody grades their own work |
tools/intent/realization.py:549:            "the Coordinator claims once every gate the level requires has passed"
SUB=8
```

### _policy.yaml evidence_profile (read, not changed)
```
# Realization policy: when a human must sign off, and what counts as evidence.
# Changing this file is a hard trigger for complexity 'high' — it is the definition of
# sufficient proof, in the same class as VERIFY.md. Only the Human may change it.
#
# acceptance_profile:
#   none      acceptance is possible but never required
#   standard  required where a contract has enforced_by: review
#   leaf      standard, plus every node that owns code_paths
#   strict    required for every node
#
# evidence_profile:
#   standard  a claim must point at a run directory containing grader.md
#   relaxed   enforcers must exist; evidence may be VERIFY.md (adopting an old project)
schema_version: 1
acceptance_profile: standard
evidence_profile: standard
```

### low-tier text after B6
```
## How many files

**`low`** — `run.md` (sections: request, plan, report, status) **and** a separate
`grader.md` beside it. The gate log cannot live inside `run.md`: `grader.md` belongs to
the Coordinator, which writes it from commands it ran itself; `run.md` is the Coder's.

**`medium` and `high`** — separate files:
144:- [ ] Run directory with `run.md` and `grader.md` (low), or the full separate set (medium/high)
```

### ruff
```
[1;32mAll checks passed![0m
19 files already formatted
```

### git status --short
```
 M README.md
 M rules/07-ice-workflow.mdc
 M rules/07-realization.mdc
 M rules/07-run-artifacts.mdc
 M skills/ice-implement/SKILL.md
 M skills/ice-review/SKILL.md
 M skills/ice-run/SKILL.md
 M tools/intent/realization.py
?? doc/runs/20260817-2334-review-craft-and-claim-order-e2/
```

### Coder did not write grader.md this round
```
coder-evidence.md
critique.md
grader.md
plan.md
report.md
request.md
review.md
slice-implement.md
slice.md
```

---

## Round 3 — M1 + FU-A minors (after APPROVE)

Touched: `skills/ice-review/SKILL.md`, `skills/ice-run/SKILL.md`.
Untouched on purpose: canonical sentence sites, TreeError, low tier, check 8,
`realization.py:480` (FU-B).

### validate
```
python3 tools/intent/cli.py validate
```
#### Output
```

5 node(s): 0 error(s), 0 warning(s)
```
Exit code: 0

### realization check
```
python3 tools/intent/cli.py realization check
```
#### Output
```
realization layer consistent (2 entry/entries)
```
Exit code: 0

### unittest
```
python3 -m unittest discover -s tools/intent/tests -t tools
```
#### Output
```
..................................................................................
----------------------------------------------------------------------
Ran 82 tests in 0.446s

OK
```
Exit code: 0

### template_checks
```
python3 tools/checks/template_checks.py --root .
```
#### Output
```
template contracts satisfied
```
Exit code: 0

### hook_checks
```
python3 tools/checks/hook_checks.py --root .
```
#### Output
```
hook contracts satisfied
```
Exit code: 0

### scope
```
python3 tools/intent/cli.py scope --run doc/runs/20260817-2334-review-craft-and-claim-order-e2
```
#### Output
```
scope clean (8 declared path(s))
```
Exit code: 0

### wc -l
```
wc -l rules/07-ice-workflow.mdc rules/07-realization.mdc rules/07-run-artifacts.mdc skills/ice-run/SKILL.md skills/ice-review/SKILL.md skills/ice-implement/SKILL.md README.md tools/intent/realization.py
```
#### Output
```
  118 rules/07-ice-workflow.mdc
  155 rules/07-realization.mdc
  141 rules/07-run-artifacts.mdc
  156 skills/ice-run/SKILL.md
  133 skills/ice-review/SKILL.md
  108 skills/ice-implement/SKILL.md
  652 README.md
  697 tools/intent/realization.py
 2160 total
```
Exit code: 0

### ruff check
```
ruff check tools/
```
#### Output
```
[1;32mAll checks passed![0m
```
Exit code: 0

### ruff format --check
```
ruff format --check tools/
```
#### Output
```
19 files already formatted
```
Exit code: 0

### DoD 9
```
rules/07-run-artifacts.mdc:89:the run, once every gate the level requires has passed: at `low` the gates themselves, at
rules/07-ice-workflow.mdc:45:| **Coordinator** (parent chat) | start other roles, pick models, count loops, allocate ids, claim realization once every gate the level requires has passed | write production code; grade its own output |
rules/07-realization.mdc:80:| `claim` | Coordinator, once every gate the level requires has passed — at `low` the Grader, above it the Adversary too | the **Coder** — nobody grades their own work |
skills/ice-implement/SKILL.md:98:- [ ] No realization claim written — the Coordinator's, once every gate the level requires has passed
skills/ice-run/SKILL.md:116:Claim once every gate the level requires has passed: at `low` that is the green Grader, at
skills/ice-run/SKILL.md:148:- [ ] Realization claimed in Step 9, once every gate the level requires has passed — or why not
README.md:257:| `claim` | Coordinator, once every gate the level requires has passed — at `low` the Grader, above it the Adversary too | the **Coder** — nobody grades their own work |
tools/intent/realization.py:549:            "the Coordinator claims once every gate the level requires has passed"
FULL=8
rules/07-run-artifacts.mdc:89:the run, once every gate the level requires has passed: at `low` the gates themselves, at
rules/07-ice-workflow.mdc:45:| **Coordinator** (parent chat) | start other roles, pick models, count loops, allocate ids, claim realization once every gate the level requires has passed | write production code; grade its own output |
rules/07-realization.mdc:80:| `claim` | Coordinator, once every gate the level requires has passed — at `low` the Grader, above it the Adversary too | the **Coder** — nobody grades their own work |
skills/ice-implement/SKILL.md:98:- [ ] No realization claim written — the Coordinator's, once every gate the level requires has passed
skills/ice-run/SKILL.md:116:Claim once every gate the level requires has passed: at `low` that is the green Grader, at
skills/ice-run/SKILL.md:148:- [ ] Realization claimed in Step 9, once every gate the level requires has passed — or why not
README.md:257:| `claim` | Coordinator, once every gate the level requires has passed — at `low` the Grader, above it the Adversary too | the **Coder** — nobody grades their own work |
tools/intent/realization.py:549:            "the Coordinator claims once every gate the level requires has passed"
SUB=8
```

### Final M1 / Minor wording
```
3. A place where the sentence turns false and the suite stays green is a **blocker** when
   the sentence is false now, or when this run asserted that place closed — in the plan,
   the Definition of Done, or a realization claim. Otherwise it is a **follow-up**: write
   it so the Human can drop it into a later run; do not block this one for it.

Contracts with `enforced_by: review` have no suite to mutate. They are Human judgements,
not automatic blockers from this step.

Mutate a scratch copy, never the working tree. Restore the copy after each mutation; when
finished, confirm the working tree was never touched.

The defect is rarely where the run looked: it is the same claim repaired in one view while
it leaks in a neighbouring one, a second derivation site, or an unexercised branch.

### When the review ends, enumerate

In the verdict you are about to ship, whichever round that is, list the complete set of
places reached by the sentences this diff can make false, plus any the run asserts closed,
and mark each one closed or open:
---
144:- [ ] Run directory with `request.md`, plus `run.md` and `grader.md` (low) or the full separate set
```

### Unchanged verified surfaces (spot checks)
```
40:| 8 | Did a claim jump ahead of you? | `git diff -- doc/intent/_realization.yaml` must add no claim citing this run; `$TOOL realization check` exits 0 — the claim comes after your verdict |
**`low`** — `run.md` (sections: request, plan, report, status) **and** a separate
`grader.md` beside it. The gate log cannot live inside `run.md`: `grader.md` belongs to
the Coordinator, which writes it from commands it ran itself; `run.md` is the Coder's.
549:            "the Coordinator claims once every gate the level requires has passed"
480:            if claim.by.strip().lower() == "coder":
546:    if by.strip().lower() == "coder":
22:## Step 1 — Read in the right order
29:## Step 2 — The eight checks
42:## Step 3 — Read each contract sentence against the code
81:## Step 4 — Attack the tests specifically
94:## Step 5 — Verdict
```

### git status --short
```
 M README.md
 M rules/07-ice-workflow.mdc
 M rules/07-realization.mdc
 M rules/07-run-artifacts.mdc
 M skills/ice-implement/SKILL.md
 M skills/ice-review/SKILL.md
 M skills/ice-run/SKILL.md
 M tools/intent/realization.py
?? doc/runs/20260817-2334-review-craft-and-claim-order-e2/
```
