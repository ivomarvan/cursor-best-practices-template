---
run_id: 20260816-1302-realization-layer-91
intent_ids: ["i0004"]
role: Grader
model: none — the Grader is not a language model
complexity: high
status: in-progress
---

# Grader

Raw output of every command in `VERIFY.md`, in order, plus the scope guard.
Nothing here was retyped by hand.

Machine: Linux 6.8.0-137-generic x86_64, Python 3.14.5, git 2.43.0
Branch: v2, HEAD fc71878
Date: 2026-08-16T13:04:35+02:00

## $ python3 tools/intent/cli.py validate

```

5 node(s): 0 error(s), 0 warning(s)
```

exit code: 0

## $ python3 tools/intent/cli.py realization check

```
realization layer consistent (0 entry/entries)
```

exit code: 0

## $ python3 -m unittest discover -s tools/intent/tests -t tools

```
...............................................................................
----------------------------------------------------------------------
Ran 79 tests in 0.271s

OK
```

exit code: 0

## $ python3 tools/checks/template_checks.py --root .

```
template contracts satisfied
```

exit code: 0

## $ python3 tools/checks/hook_checks.py --root .

```
hook contracts satisfied
```

exit code: 0

## $ ruff check tools/

```
[1;32mAll checks passed![0m
```

exit code: 0

## $ ruff format --check tools/

```
19 files already formatted
```

exit code: 0

## $ python3 tools/intent/cli.py scope --run doc/runs/20260816-1302-realization-layer-91 --node i0004

```
scope clean (30 declared path(s))
```

exit code: 0

## Failing-test evidence

The design decision under test is Q4: **only a change of wording invalidates a claim,
never a state.** To show the new tests are load-bearing rather than decorative, the
rejected alternative was patched in — an unclaimed ancestor also opens its subtree —
and the suite re-run against otherwise unchanged code.

```diff
                 changed = _changed_part(ancestor.id, moved_contracts, moved_meaning)
+                    or ("state" if layer.claim_of(ancestor.id) is None else None)
```

```
.................F.F.F.FF...F........F..F.FF.F.................................
======================================================================
FAIL: test_rejection_marks_an_otherwise_realized_node (intent.tests.test_realization.AcceptanceTest.test_rejection_marks_an_otherwise_realized_node)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_realization.py", line 350, in test_rejection_marks_an_otherwise_realized_node
    self.assertEqual(state.state, "rejected")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'stale' != 'rejected'
- stale
+ rejected


======================================================================
FAIL: test_affirm_keeps_the_claim_after_a_harmless_edit (intent.tests.test_realization.AffirmTest.test_affirm_keeps_the_claim_after_a_harmless_edit)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_realization.py", line 282, in test_affirm_keeps_the_claim_after_a_harmless_edit
    self.assertEqual(self.state_of(tree, layer, node).state, "realized")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'stale' != 'realized'
- stale
+ realized


======================================================================
FAIL: test_affirm_subtree_touches_descendants_with_a_claim (intent.tests.test_realization.AffirmTest.test_affirm_subtree_touches_descendants_with_a_claim)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_realization.py", line 307, in test_affirm_subtree_touches_descendants_with_a_claim
    self.assertEqual(states[leaf].state, "realized")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'stale' != 'realized'
- stale
+ realized


======================================================================
FAIL: test_a_missing_enforcer_makes_a_realized_node_broken (intent.tests.test_realization.BrokenEnforcerTest.test_a_missing_enforcer_makes_a_realized_node_broken)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_realization.py", line 250, in test_a_missing_enforcer_makes_a_realized_node_broken
    self.assertEqual(state.state, "broken")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'stale' != 'broken'
- stale
+ broken


======================================================================
FAIL: test_claim_makes_a_node_realized (intent.tests.test_realization.ClaimTest.test_claim_makes_a_node_realized)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_realization.py", line 103, in test_claim_makes_a_node_realized
    self.assertEqual(state.state, "realized")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'stale' != 'realized'
- stale
+ realized


======================================================================
FAIL: test_relaxed_profile_accepts_verify_as_evidence (intent.tests.test_realization.ClaimTest.test_relaxed_profile_accepts_verify_as_evidence)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_realization.py", line 145, in test_relaxed_profile_accepts_verify_as_evidence
    self.assertEqual(state.state, "realized")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'stale' != 'realized'
- stale
+ realized


======================================================================
FAIL: test_layer_survives_a_save_and_load_round_trip (intent.tests.test_realization.PersistenceTest.test_layer_survives_a_save_and_load_round_trip)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_realization.py", line 408, in test_layer_survives_a_save_and_load_round_trip
    self.assertEqual(compute_states(tree, reloaded, self.policy)[node].state, "realized")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'stale' != 'realized'
- stale
+ realized


======================================================================
FAIL: test_ancestor_text_change_opens_the_subtree (intent.tests.test_realization.StalenessTest.test_ancestor_text_change_opens_the_subtree)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_realization.py", line 173, in test_ancestor_text_change_opens_the_subtree
    self.assertEqual(state.blocked_by, middle)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'i0001' != 'i0002'
- i0001
?     ^
+ i0002
?     ^


======================================================================
FAIL: test_unproven_ancestor_does_not_block_a_child (intent.tests.test_realization.StalenessTest.test_unproven_ancestor_does_not_block_a_child)
Decision Q4: only a change of wording invalidates, never a state.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_realization.py", line 189, in test_unproven_ancestor_does_not_block_a_child
    self.assertEqual(states[leaf].state, "realized")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'stale' != 'realized'
- stale
+ realized


======================================================================
FAIL: test_uses_propagation_stops_after_one_hop (intent.tests.test_realization.StalenessTest.test_uses_propagation_stops_after_one_hop)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_realization.py", line 232, in test_uses_propagation_stops_after_one_hop
    self.assertEqual(states[outer].state, "realized")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'stale' != 'realized'
- stale
+ realized


======================================================================
FAIL: test_uses_target_meaning_change_leaves_the_consumer_alone (intent.tests.test_realization.StalenessTest.test_uses_target_meaning_change_leaves_the_consumer_alone)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_realization.py", line 217, in test_uses_target_meaning_change_leaves_the_consumer_alone
    self.assertEqual(states[consumer].state, "realized")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'stale' != 'realized'
- stale
+ realized


----------------------------------------------------------------------
Ran 79 tests in 0.431s

FAILED (failures=11)
```

exit code: 1

### After reverting the patch

```
...............................................................................
----------------------------------------------------------------------
Ran 79 tests in 0.229s

OK
```

exit code: 0

## Verdict

All nine machine gates exit 0 on the delivered code. Eleven tests fail under the
rejected propagation rule, which is the evidence that contracts c8-c14 constrain
behaviour rather than restate it.

---

# Round 2 — after the Critic and the Adversary

Round 1 was green, but both review gates returned findings. Contracts `c9` and `c10`
were narrowed to what their enforcer proves, `c15` and `c16` were added, and
`enforcer_problem` in `tools/intent/validate.py` was tightened from a substring match
to a whole-symbol match. The gates therefore re-run in full.

Round 1 also logged `ruff` under the VERIFY heading, which contradicts the sentence in
`VERIFY.md` that the Grader runs "exactly these... and nothing else". Ruff is a Coder
self-check, and below it is labelled as one.

Date: 2026-08-16T13:20:43+02:00, HEAD fc71878

## VERIFY.md — the Grader mandate

### $ python3 tools/intent/cli.py validate

```

5 node(s): 0 error(s), 0 warning(s)
```

exit code: 0

### $ python3 tools/intent/cli.py realization check

```
realization layer consistent (0 entry/entries)
```

exit code: 0

### $ python3 -m unittest discover -s tools/intent/tests -t tools

```
................................................................................
----------------------------------------------------------------------
Ran 80 tests in 0.243s

OK
```

exit code: 0

### $ python3 tools/checks/template_checks.py --root .

```
template contracts satisfied
```

exit code: 0

### $ python3 tools/checks/hook_checks.py --root .

```
hook contracts satisfied
```

exit code: 0

### $ python3 tools/intent/cli.py scope --run doc/runs/20260816-1302-realization-layer-91 --node i0004

```
scope clean (30 declared path(s))
```

exit code: 0

## Failing-test evidence for c16

The Adversary found that `enforcer_problem` matched the enforcer symbol as a plain
substring, so renaming `test_x` to `test_x_v2` left the contract looking enforced.
Reverting the fix to the old substring match, against otherwise unchanged code:

```diff
-        if not re.search(rf"(?<![\w.]){re.escape(symbol)}\b", content):
+        if symbol not in content:
```

```
........................F.......................................................
======================================================================
FAIL: test_a_renamed_enforcer_symbol_makes_a_node_broken (intent.tests.test_realization.BrokenEnforcerTest.test_a_renamed_enforcer_symbol_makes_a_node_broken)
A substring match would accept 'test_x' inside 'test_x_v2' and miss the rename.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_realization.py", line 268, in test_a_renamed_enforcer_symbol_makes_a_node_broken
    self.assertEqual(self.state_of(tree, layer, node).state, "broken")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'realized' != 'broken'
- realized
+ broken


----------------------------------------------------------------------
Ran 80 tests in 0.255s

FAILED (failures=1)
```

exit code: 1

### After reverting the patch

```
................................................................................
----------------------------------------------------------------------
Ran 80 tests in 0.246s

OK
```

exit code: 0

## Coder self-checks — beyond the Grader mandate

Required by `01-general-programming.mdc` (verification before completion), not listed
in `VERIFY.md`, therefore not part of what the Grader is allowed to demand.

### $ ruff check tools/

```
[1;32mAll checks passed![0m
```

exit code: 0

### $ ruff format --check tools/

```
19 files already formatted
```

exit code: 0

## Verdict — round 2

Six gates of the Grader mandate exit 0. Both failing-test evidences behave as claimed:
the suite fails under the rejected propagation rule (11 tests, round 1) and under the
old substring enforcer match (round 2), and passes once each patch is reverted.

---

# Round 3 — after the second review round

Both gates found the same defect independently: the fix to `c10` had recreated the
compound-statement problem in the new `c15`. The `uses` edge now has one contract per
direction (`c15`, `c16`), each with its own test and no orphaned test left in the file,
and the rule behind it is written into the node so it is not rediscovered a third time.
`c16` from round 2 became `c17`.

Date: 2026-08-16T13:33:31+02:00

## VERIFY.md — the Grader mandate

### $ python3 tools/intent/cli.py validate

```

5 node(s): 0 error(s), 0 warning(s)
```

exit code: 0

### $ python3 tools/intent/cli.py realization check

```
realization layer consistent (0 entry/entries)
```

exit code: 0

### $ python3 -m unittest discover -s tools/intent/tests -t tools

```
................................................................................
----------------------------------------------------------------------
Ran 80 tests in 0.142s

OK
```

exit code: 0

### $ python3 tools/checks/template_checks.py --root .

```
template contracts satisfied
```

exit code: 0

### $ python3 tools/checks/hook_checks.py --root .

```
hook contracts satisfied
```

exit code: 0

### $ python3 tools/intent/cli.py scope --run doc/runs/20260816-1302-realization-layer-91 --node i0004

```
scope clean (30 declared path(s))
```

exit code: 0

### $ ruff check tools/  (Coder self-check, not in VERIFY.md)

```
[1;32mAll checks passed![0m
```

exit code: 0

### $ ruff format --check tools/  (Coder self-check, not in VERIFY.md)

```
19 files already formatted
```

exit code: 0

