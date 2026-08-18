---
run_id: 20260818-0853-harness-and-hooks-audit-86
intent_ids: ["i0001", "i0005", "i0003", "i0004", "i0002"]
role: Coder
model: cursor-grok-4.5-high
complexity: high
status: in-progress
---

# Coder evidence — raw mutation and measurement output

Mutations restored from `/tmp/ice-audit-backups/`. No git commit.

## E1 — link_targets: skills rglob -> glob(*/SKILL.md)

```
FF
======================================================================
FAIL: test_a_broken_link_in_a_second_tier_skill_file_is_reported (intent.tests.test_checks.TemplateLinkTest.test_a_broken_link_in_a_second_tier_skill_file_is_reported)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_checks.py", line 151, in test_a_broken_link_in_a_second_tier_skill_file_is_reported
    self.assertEqual(code, 1)
    ~~~~~~~~~~~~~~~~^^^^^^^^^
AssertionError: 0 != 1

======================================================================
FAIL: test_a_broken_link_in_a_nested_skill_file_is_reported (intent.tests.test_checks.TemplateLinkTest.test_a_broken_link_in_a_nested_skill_file_is_reported)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_checks.py", line 160, in test_a_broken_link_in_a_nested_skill_file_is_reported
    self.assertEqual(code, 1)
    ~~~~~~~~~~~~~~~~^^^^^^^^^
AssertionError: 0 != 1

----------------------------------------------------------------------
Ran 2 tests in 0.009s

FAILED (failures=2)
exit: 1
```

## E2 — link_targets: drop rules

```
F
======================================================================
FAIL: test_a_broken_link_in_a_rule_is_reported (intent.tests.test_checks.TemplateLinkTest.test_a_broken_link_in_a_rule_is_reported)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_checks.py", line 132, in test_a_broken_link_in_a_rule_is_reported
    self.assertEqual(code, 1)
    ~~~~~~~~~~~~~~~~^^^^^^^^^
AssertionError: 0 != 1

----------------------------------------------------------------------
Ran 1 test in 0.007s

FAILED (failures=1)
exit: 1
```

## E3 — delete unterminated fence report

```
F
======================================================================
FAIL: test_an_unterminated_fenced_block_is_reported (intent.tests.test_checks.TemplateLinkTest.test_an_unterminated_fenced_block_is_reported)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_checks.py", line 178, in test_an_unterminated_fenced_block_is_reported
    self.assertEqual(code, 1)
    ~~~~~~~~~~~~~~~~^^^^^^^^^
AssertionError: 0 != 1

----------------------------------------------------------------------
Ran 1 test in 0.006s

FAILED (failures=1)
exit: 1
```

## E4 — delete symlink identity branch

```
FF
======================================================================
FAIL: test_a_symlink_pointing_outside_the_harness_is_reported (intent.tests.test_checks.TemplateSymlinkTest.test_a_symlink_pointing_outside_the_harness_is_reported) (name='rules')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_checks.py", line 261, in test_a_symlink_pointing_outside_the_harness_is_reported
    self.assertEqual(code, 1)
    ~~~~~~~~~~~~~~~~^^^^^^^^^
AssertionError: 0 != 1

======================================================================
FAIL: test_a_symlink_pointing_outside_the_harness_is_reported (intent.tests.test_checks.TemplateSymlinkTest.test_a_symlink_pointing_outside_the_harness_is_reported) (name='skills')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_checks.py", line 261, in test_a_symlink_pointing_outside_the_harness_is_reported
    self.assertEqual(code, 1)
    ~~~~~~~~~~~~~~~~^^^^^^^^^
AssertionError: 0 != 1

----------------------------------------------------------------------
Ran 1 test in 0.014s

FAILED (failures=2)
exit: 1
```

## E5 — drop made_with from CASES

```
F
======================================================================
FAIL: test_the_check_reports_attribution_that_survived (intent.tests.test_checks.HookAttributionCheckTest.test_the_check_reports_attribution_that_survived) (stub='made_with')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_checks.py", line 332, in test_the_check_reports_attribution_that_survived
    self.assertEqual(code, 1, out)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^
AssertionError: 0 != 1 : hook contracts satisfied (2 shipped hook(s), 13 message case(s); committed modes not verified: /tmp/harness-gl62r0gr/project/.cursor is not the top of a git work tree)


----------------------------------------------------------------------
Ran 1 test in 1.295s

FAILED (failures=1)
exit: 1
```

## E6 — replace byte equality with substring conditions

```
FFFF
======================================================================
FAIL: test_the_check_reports_a_trailer_that_was_deleted (intent.tests.test_checks.HookAttributionCheckTest.test_the_check_reports_a_trailer_that_was_deleted) (extra='intent')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_checks.py", line 385, in test_the_check_reports_a_trailer_that_was_deleted
    self.assertEqual(code, 1, out)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^
AssertionError: 0 != 1 : hook contracts satisfied (2 shipped hook(s), 14 message case(s); committed modes not verified: /tmp/harness-sp30f6bo/project/.cursor is not the top of a git work tree)


======================================================================
FAIL: test_the_check_reports_a_trailer_that_was_deleted (intent.tests.test_checks.HookAttributionCheckTest.test_the_check_reports_a_trailer_that_was_deleted) (extra='run')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_checks.py", line 385, in test_the_check_reports_a_trailer_that_was_deleted
    self.assertEqual(code, 1, out)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^
AssertionError: 0 != 1 : hook contracts satisfied (2 shipped hook(s), 14 message case(s); committed modes not verified: /tmp/harness-4r5a_v47/project/.cursor is not the top of a git work tree)


======================================================================
FAIL: test_the_check_reports_a_trailer_that_was_deleted (intent.tests.test_checks.HookAttributionCheckTest.test_the_check_reports_a_trailer_that_was_deleted) (extra='subject')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_checks.py", line 385, in test_the_check_reports_a_trailer_that_was_deleted
    self.assertEqual(code, 1, out)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^
AssertionError: 0 != 1 : hook contracts satisfied (2 shipped hook(s), 14 message case(s); committed modes not verified: /tmp/harness-ujx5s7dv/project/.cursor is not the top of a git work tree)


======================================================================
FAIL: test_the_check_reports_a_body_that_was_reflowed (intent.tests.test_checks.HookAttributionCheckTest.test_the_check_reports_a_body_that_was_reflowed)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_checks.py", line 395, in test_the_check_reports_a_body_that_was_reflowed
    self.assertEqual(code, 1, out)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^
AssertionError: 0 != 1 : hook contracts satisfied (2 shipped hook(s), 14 message case(s); committed modes not verified: /tmp/harness-ha916lk2/project/.cursor is not the top of a git work tree)


----------------------------------------------------------------------
Ran 2 tests in 1.959s

FAILED (failures=4)
exit: 1
```

## E7 — hard-coded hook pair instead of shipped_hooks

```
FF
======================================================================
FAIL: test_the_check_reports_a_hook_that_is_not_executable (intent.tests.test_checks.HookExecutableCheckTest.test_the_check_reports_a_hook_that_is_not_executable) (hook='hooks/git/pre-push')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_checks.py", line 455, in test_the_check_reports_a_hook_that_is_not_executable
    self.assertEqual(code, 1, out)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^
AssertionError: 0 != 1 : hook contracts satisfied (3 shipped hook(s), 14 message case(s); committed modes not verified: /tmp/harness-fs4ywatv/project/.cursor is not the top of a git work tree)


======================================================================
FAIL: test_the_check_reports_a_hook_that_is_not_executable (intent.tests.test_checks.HookExecutableCheckTest.test_the_check_reports_a_hook_that_is_not_executable) (hook='hooks/after-edit.sh')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_checks.py", line 455, in test_the_check_reports_a_hook_that_is_not_executable
    self.assertEqual(code, 1, out)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^
AssertionError: 0 != 1 : hook contracts satisfied (3 shipped hook(s), 14 message case(s); committed modes not verified: /tmp/harness-k0ij910j/project/.cursor is not the top of a git work tree)


----------------------------------------------------------------------
Ran 1 test in 1.601s

FAILED (failures=2)
exit: 1
```

## E8 — delete 100755 comparison

```
F
======================================================================
FAIL: test_the_check_reports_a_committed_mode_without_the_exec_bit (intent.tests.test_checks.HookExecutableCheckTest.test_the_check_reports_a_committed_mode_without_the_exec_bit)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_checks.py", line 517, in test_the_check_reports_a_committed_mode_without_the_exec_bit
    self.assertEqual(code, 1, out)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^
AssertionError: 0 != 1 : hook contracts satisfied (2 shipped hook(s), 14 message case(s); committed modes checked)


----------------------------------------------------------------------
Ran 1 test in 0.589s

FAILED (failures=1)
exit: 1
```

## E9 — delete REQUIRED_HOOKS assertion

```
F
======================================================================
FAIL: test_the_check_reports_a_required_hook_that_is_missing (intent.tests.test_checks.HookExecutableCheckTest.test_the_check_reports_a_required_hook_that_is_missing)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_checks.py", line 466, in test_the_check_reports_a_required_hook_that_is_missing
    self.assertEqual(code, 1, out)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^
AssertionError: 0 != 1 : hook contracts satisfied (1 shipped hook(s), 14 message case(s); committed modes not verified: /tmp/harness-alfsun5r/project/.cursor is not the top of a git work tree)


----------------------------------------------------------------------
Ran 1 test in 0.516s

FAILED (failures=1)
exit: 1
```

## E10 — restore today's two unanchored grep stages

```
ERROR hooks/git/commit-msg: case 'capitalised_key': output mismatch
--- expected
+++ actual
@@ -2,3 +2,5 @@
 
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86
+
+Co-Authored-By: Cursor <bot@example.com>

ERROR hooks/git/commit-msg: case 'made_with': output mismatch
--- expected
+++ actual
@@ -2,3 +2,5 @@
 
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86
+
+Made-with: Cursor

ERROR hooks/git/commit-msg: case 'generated_with': output mismatch
--- expected
+++ actual
@@ -2,3 +2,5 @@
 
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86
+
+Generated-with: Cursor 1.2

ERROR hooks/git/commit-msg: case 'body_quotes_the_address': output mismatch
--- expected
+++ actual
@@ -1,6 +1,5 @@
 feat(db): enforce unique user_id
 
-Never write Co-authored-by: Cursor <cursoragent@cursor.com> by hand.
 
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86

ERROR hooks/git/commit-msg: case 'attribution_only': output mismatch
--- expected
+++ actual
@@ -0,0 +1 @@
+Co-authored-by: Cursor <cursoragent@cursor.com>


5 hook contract violation(s)
exit: 1
```

## E11 — realization.py: coder -> coderx

```
F
======================================================================
FAIL: test_a_hand_written_coder_claim_is_reported (intent.tests.test_realization.ConsistencyTest.test_a_hand_written_coder_claim_is_reported)
R6 must fire when the YAML was edited by hand, not only via claim().
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/tools/intent/tests/test_realization.py", line 500, in test_a_hand_written_coder_claim_is_reported
    self.assertTrue(problems)
    ~~~~~~~~~~~~~~~^^^^^^^^^^
AssertionError: [] is not true

----------------------------------------------------------------------
Ran 1 test in 0.015s

FAILED (failures=1)
exit: 1
```

## E12 — round-1 token anchor instead of prefix

```
ERROR hooks/git/commit-msg: case 'cursor_agent_prefix': output mismatch
--- expected
+++ actual
@@ -2,3 +2,5 @@
 
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86
+
+Co-authored-by: CursorAgent <bot@example.com>

ERROR hooks/git/commit-msg: case 'cursor_hyphen_bot': output mismatch
--- expected
+++ actual
@@ -2,3 +2,5 @@
 
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86
+
+Co-authored-by: Cursor-bot <bot@example.com>

ERROR hooks/git/commit-msg: case 'cursor_xyz': output mismatch
--- expected
+++ actual
@@ -2,3 +2,5 @@
 
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86
+
+Co-authored-by: CursorXYZ


3 hook contract violation(s)
exit: 1
```

## Post-mutation green confirmation

```
...................................................................................................................
----------------------------------------------------------------------
Ran 115 tests in 10.532s

OK
exit: 0
template contracts satisfied
exit: 0
hook contracts satisfied (2 shipped hook(s), 14 message case(s); committed modes checked)
exit: 0
```

## A3c — supersets remasured (old HEAD hook vs repaired working tree)

```
class  old        new        line
T1     maže       maže       Co-authored-by: Cursor <cursoragent@cursor.com>
T2a    maže       maže       Co-authored-by: CursorAgent <bot@example.com>
T2b    maže       maže       Co-authored-by: Cursor-bot <bot@example.com>
T2c    maže       maže       Co-authored-by: CursorXYZ
T2d    maže       maže       Co-authored-by: Cursorina Smith <c@x.com>
T3     maže       maže       Co-authored-by: Cursor
T4     maže       maže         Co-authored-by: Cursor <x@y.com>
T5     nechává    maže       Co-Authored-By: Cursor <bot@example.com>
T6a    nechává    maže       Made-with: Cursor
T6b    nechává    maže       Generated-with: Cursor 1.2
T7     maže       maže       Signed-off-by: Cursor Agent <cursoragent@cursor.com>
T8     maže       maže       Reported-by: someone <cursoragent@cursor.com>
T9a    nechává    nechává    Intent: i0005
T9b    nechává    nechává    Run: 20260818-0853-cursor-audit-86
T9c    nechává    nechává    Co-authored-by: Ivo Example <ivo@example.com>
T10a   nechává    nechává    Tool: Cursor
T10b   nechává    nechává    X-Cursor-Agent: yes
T11    maže       maže       Note: mail cursoragent@cursor.com for access
T12a   maže       nechává    Never write Co-authored-by: Cursor by hand.
T12b   maže       nechává    The hook removes Co-authored-by: Cursor <cursoragent@cursor.com> from 
T13a   nechává    nechává    docs: Cursor attribution note
T13b   nechává    nechává    docs: cursor rules cleanup
T13c   maže       nechává    fix: strip Co-authored-by: Cursor properly
```

rows where old deletes / new keeps outside T12/T13: none

## Mutation exit summary

- E1: exit 1
- E2: exit 1
- E3: exit 1
- E4: exit 1
- E5: exit 1
- E6: exit 1
- E7: exit 1
- E8: exit 1
- E9: exit 1
- E10: exit 1
- E11: exit 1
- E12: exit 1
- suite after restore: exit 0
- template_checks: exit 0
- hook_checks: exit 0

## Mount test (DoD 10)

```
$ mkdir -p /tmp/ice-mount-project && cp -a . /tmp/ice-mount-project/.cursor && rm -rf /tmp/ice-mount-project/.cursor/.git
$ python3 /tmp/ice-mount-project/.cursor/tools/checks/template_checks.py --root /tmp/ice-mount-project/.cursor
template contracts satisfied
exit: 0
$ python3 /tmp/ice-mount-project/.cursor/tools/checks/hook_checks.py --root /tmp/ice-mount-project/.cursor
hook contracts satisfied (2 shipped hook(s), 14 message case(s); committed modes not verified: /tmp/ice-mount-project/.cursor is not the top of a git work tree)
exit: 0
```

## Unittest count

```
Ran 115 tests in ~11s
OK
(previous baseline was 82)
```

---
# Round 2 — B1/B2 fixes (E13+)

Appended after Adversary REQUEST CHANGES. Mutations restored from
`/tmp/ice-audit-backups-r2/`. No git commit.

## E13 — delete address alternative from commit-msg (B1)

```
ERROR hooks/git/commit-msg: case 'address_only_trailer': output mismatch
--- expected
+++ actual
@@ -2,3 +2,5 @@
 
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86
+
+Reported-by: someone <cursoragent@cursor.com>

ERROR hooks/git/commit-msg: case 'digit_key_address': output mismatch
--- expected
+++ actual
@@ -2,3 +2,5 @@
 
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86
+
+2fa-note: cursoragent@cursor.com

ERROR hooks/git/commit-msg: case 'underscore_key_address': output mismatch
--- expected
+++ actual
@@ -2,3 +2,5 @@
 
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86
+
+Co_authored_by: Cursor <cursoragent@cursor.com>

ERROR hooks/git/commit-msg: case 'dot_key_address': output mismatch
--- expected
+++ actual
@@ -2,3 +2,5 @@
 
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86
+
+co.authored.by: cursoragent@cursor.com


4 hook contract violation(s)
exit: 1
```

## E14 — revert to narrow key grammar (B2)

```
ERROR hooks/git/commit-msg: case 'space_before_colon': output mismatch
--- expected
+++ actual
@@ -2,3 +2,5 @@
 
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86
+
+Co-authored-by : Cursor <cursoragent@cursor.com>

ERROR hooks/git/commit-msg: case 'digit_key_address': output mismatch
--- expected
+++ actual
@@ -2,3 +2,5 @@
 
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86
+
+2fa-note: cursoragent@cursor.com

ERROR hooks/git/commit-msg: case 'underscore_key_address': output mismatch
--- expected
+++ actual
@@ -2,3 +2,5 @@
 
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86
+
+Co_authored_by: Cursor <cursoragent@cursor.com>

ERROR hooks/git/commit-msg: case 'dot_key_address': output mismatch
--- expected
+++ actual
@@ -2,3 +2,5 @@
 
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86
+
+co.authored.by: cursoragent@cursor.com


4 hook contract violation(s)
exit: 1
```

## Git-arbitrated superset enumeration (old HEAD vs repaired)

For each candidate: `git interpret-trailers --parse` (is it a trailer?),
then both hooks. Claim: wherever `old` deletes, `new` deletes too — except
authorised T12/T13 prose/subject tightenings.

```
id     git  old      new      line
B2a    yes  maže     maže     Co-authored-by : Cursor <cursoragent@cursor.com>
B2b    yes  maže     maže     2fa-note: cursoragent@cursor.com
B2c    no   maže     maže     Co_authored_by: Cursor <cursoragent@cursor.com>
B2d    no   maže     maže     co.authored.by: cursoragent@cursor.com
B1     yes  maže     maže     Reported-by: someone <cursoragent@cursor.com>
T1     yes  maže     maže     Co-authored-by: Cursor <cursoragent@cursor.com>
T2a    yes  maže     maže     Co-authored-by: CursorAgent <bot@example.com>
T2b    yes  maže     maže     Co-authored-by: Cursor-bot <bot@example.com>
T2c    yes  maže     maže     Co-authored-by: CursorXYZ
T5     yes  nechává  maže     Co-Authored-By: Cursor <bot@example.com>
T6a    yes  nechává  maže     Made-with: Cursor
T6b    yes  nechává  maže     Generated-with: Cursor 1.2
T6s    yes  nechává  maže     Made-with : Cursor
T7     yes  maže     maže     Signed-off-by: Cursor Agent <cursoragent@cursor.com>
T8     yes  maže     maže     Reported-by: someone <cursoragent@cursor.com>
T9a    yes  nechává  nechává  Intent: i0005
T9b    yes  nechává  nechává  Run: 20260818-0853-cursor-audit-86
T9c    yes  nechává  nechává  Co-authored-by: Ivo Example <ivo@example.com>
T10a   yes  nechává  nechává  Tool: Cursor
T11    yes  maže     maže     Note: mail cursoragent@cursor.com for access
T12a   no   maže     nechává  Never write Co-authored-by: Cursor by hand.
T12b   no   maže     nechává  The hook removes Co-authored-by: Cursor <cursoragent@cursor.com>
T13a   n/a  nechává  nechává  docs: Cursor attribution note
T13c   n/a  maže     nechává  fix: strip Co-authored-by: Cursor properly
M1a    yes  nechává  maže     Reviewed-by: Cursory glance at the diff
M1b    yes  nechává  maže     Fixed-by: Cursory reading of the spec
M1c    yes  nechává  maže     Made-with: cursory care
M1d    yes  nechává  maže     Tested-with: Cursor-free toolchain
M1e    yes  nechává  maže     Reported-by: Cursor Smith <smith@example.com>
T4     no   maže     maže       Co-authored-by: Cursor <x@y.com>
```

old-maže/new-nechává outside T12/T13: none

## M1 — prefix-match cost (intentional, not narrowed)

Name branch matches value prefix `cursor`, so these trailers today's hook keeps
are removed by the repaired hook: `Reviewed-by: Cursory glance…`,
`Made-with: cursory care`, `Reported-by: Cursor Smith <…>`, etc. Same cost the
Critic already accepted for `Cursorina Smith`. Documented in hook comment and
`hooks/README.md`; regex not narrowed.

## Post-E13/E14 green confirmation

```
...................................................................................................................
----------------------------------------------------------------------
Ran 115 tests in 14.636s

OK
exit: 0
hook contracts satisfied (2 shipped hook(s), 19 message case(s); committed modes checked)
exit: 0
template contracts satisfied
exit: 0
```


---
# Round 3 — B3 trailer-block structure (E15+)

## B3 reproduction then fix confirmation

```
folded_space_continuation:
  old keeps agent/address: False
  new keeps agent/address: False
  new out: 'feat(x): subject\n\nReason: body.\n\nIntent: i0005\n'
folded_tab_continuation:
  old keeps agent/address: False
  new keeps agent/address: False
  new out: 'feat(x): subject\n\nReason: body.\n\nIntent: i0005\n'
folded_name_then_address:
  old keeps agent/address: False
  new keeps agent/address: False
  new out: 'feat(x): subject\n\nReason: body.\n\nIntent: i0005\n'
folded_space_before_colon:
  old keeps agent/address: False
  new keeps agent/address: False
  new out: 'feat(x): subject\n\nReason: body.\n\nIntent: i0005\n'
```

## E15 — remove trailer-block detection (always trailer_start=1)

```
ERROR hooks/git/commit-msg: case 'cursor_trailer': output mismatch
--- expected
+++ actual
@@ -1,4 +1,3 @@
 feat(db): enforce unique user_id
-
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86

ERROR hooks/git/commit-msg: case 'cursor_agent_prefix': output mismatch
--- expected
+++ actual
@@ -1,4 +1,3 @@
 feat(db): enforce unique user_id
-
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86

ERROR hooks/git/commit-msg: case 'cursor_hyphen_bot': output mismatch
--- expected
+++ actual
@@ -1,4 +1,3 @@
 feat(db): enforce unique user_id
-
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86

ERROR hooks/git/commit-msg: case 'cursor_xyz': output mismatch
--- expected
+++ actual
@@ -1,4 +1,3 @@
 feat(db): enforce unique user_id
-
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86

ERROR hooks/git/commit-msg: case 'capitalised_key': output mismatch
--- expected
+++ actual
@@ -1,4 +1,3 @@
 feat(db): enforce unique user_id
-
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86

ERROR hooks/git/commit-msg: case 'made_with': output mismatch
--- expected
+++ actual
@@ -1,4 +1,3 @@
 feat(db): enforce unique user_id
-
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86

ERROR hooks/git/commit-msg: case 'generated_with': output mismatch
--- expected
+++ actual
@@ -1,4 +1,3 @@
 feat(db): enforce unique user_id
-
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86

ERROR hooks/git/commit-msg: case 'signed_off_by_agent': output mismatch
--- expected
+++ actual
@@ -1,4 +1,3 @@
 feat(db): enforce unique user_id
-
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86

ERROR hooks/git/commit-msg: case 'human_co_author': output mismatch
--- expected
+++ actual
@@ -1,6 +1,4 @@
 feat(db): enforce unique user_id
-
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86
-
 Co-authored-by: Ivo Example <ivo@example.com>

ERROR hooks/git/commit-msg: case 'body_quotes_the_address': output mismatch
--- expected
+++ actual
@@ -1,6 +1,4 @@
 feat(db): enforce unique user_id
-
 Never write Co-authored-by: Cursor <cursoragent@cursor.com> by hand.
-
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86

ERROR hooks/git/commit-msg: case 'subject_names_cursor': output mismatch
--- expected
+++ actual
@@ -1,4 +1,3 @@
 docs: Cursor attribution note
-
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86

ERROR hooks/git/commit-msg: case 'run_slug_contains_cursor': output mismatch
--- expected
+++ actual
@@ -1,4 +1,3 @@
 feat(db): enforce unique user_id
-
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86

ERROR hooks/git/commit-msg: case 'trailing_blank_lines': output mismatch
--- expected
+++ actual
@@ -1,4 +1,3 @@
 feat(db): enforce unique user_id
-
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86

ERROR hooks/git/commit-msg: case 'address_only_trailer': output mismatch
--- expected
+++ actual
@@ -1,4 +1,3 @@
 feat(db): enforce unique user_id
-
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86

ERROR hooks/git/commit-msg: case 'space_before_colon': output mismatch
--- expected
+++ actual
@@ -1,4 +1,3 @@
 feat(db): enforce unique user_id
-
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86

ERROR hooks/git/commit-msg: case 'digit_key_address': output mismatch
--- expected
+++ actual
@@ -1,4 +1,3 @@
 feat(db): enforce unique user_id
-
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86

ERROR hooks/git/commit-msg: case 'underscore_key_address': output mismatch
--- expected
+++ actual
@@ -1,4 +1,3 @@
 feat(db): enforce unique user_id
-
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86

ERROR hooks/git/commit-msg: case 'dot_key_address': output mismatch
--- expected
+++ actual
@@ -1,4 +1,3 @@
 feat(db): enforce unique user_id
-
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86

ERROR hooks/git/commit-msg: case 'folded_space_continuation': output mismatch
--- expected
+++ actual
@@ -1,5 +1,3 @@
 feat(x): subject
-
 Reason: body.
-
 Intent: i0005

ERROR hooks/git/commit-msg: case 'folded_tab_continuation': output mismatch
--- expected
+++ actual
@@ -1,5 +1,3 @@
 feat(x): subject
-
 Reason: body.
-
 Intent: i0005

ERROR hooks/git/commit-msg: case 'folded_name_then_address': output mismatch
--- expected
+++ actual
@@ -1,5 +1,3 @@
 feat(x): subject
-
 Reason: body.
-
 Intent: i0005

ERROR hooks/git/commit-msg: case 'folded_space_before_colon': output mismatch
--- expected
+++ actual
@@ -1,5 +1,3 @@
 feat(x): subject
-
 Reason: body.
-
 Intent: i0005

ERROR hooks/git/commit-msg: case 'mixed_attribution_and_legitimate_trailers': output mismatch
--- expected
+++ actual
@@ -1,5 +1,4 @@
 feat(db): enforce unique user_id
-
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86
 Co-authored-by: Ivo Example <ivo@example.com>

ERROR hooks/git/commit-msg: case 'indented_prose_quotes_attribution': output mismatch
--- expected
+++ actual
@@ -1,8 +1,5 @@
 feat(db): enforce unique user_id
-
 Note the form:
-  Co-authored-by: Cursor <cursoragent@cursor.com>
 in docs only.
-
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86

ERROR hooks/git/commit-msg: case 'crlf_line_endings': output mismatch
--- expected
+++ actual
@@ -1,4 +1,3 @@
 feat(db): enforce unique user_id
-
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86

ERROR hooks/git/commit-msg: case 'made_with_space_before_colon': output mismatch
--- expected
+++ actual
@@ -1,4 +1,3 @@
 feat(db): enforce unique user_id
-
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86


26 hook contract violation(s)
exit: 1
```

## E16 — remove continuation handling

```
ERROR hooks/git/commit-msg: case 'folded_space_continuation': output mismatch
--- expected
+++ actual
@@ -3,3 +3,4 @@
 Reason: body.
 
 Intent: i0005
+Co-authored-by:

ERROR hooks/git/commit-msg: case 'folded_tab_continuation': output mismatch
--- expected
+++ actual
@@ -3,3 +3,4 @@
 Reason: body.
 
 Intent: i0005
+Co-authored-by:

ERROR hooks/git/commit-msg: case 'folded_space_before_colon': output mismatch
--- expected
+++ actual
@@ -3,3 +3,4 @@
 Reason: body.
 
 Intent: i0005
+Co-authored-by :


3 hook contract violation(s)
exit: 1
```

## Git-arbitrated superset (round 3, structural hook)

```
id               old      new     
B3a              clears   clears   o_del_new_keep=False
B3b              clears   clears   o_del_new_keep=False
B3c              clears   clears   o_del_new_keep=False
B3d              clears   clears   o_del_new_keep=False
B2a              clears   clears   o_del_new_keep=False
B2b              clears   clears   o_del_new_keep=False
T1               clears   clears   o_del_new_keep=False
T6a              clears   clears   o_del_new_keep=False
T9c              keeps_human keeps_human o_del_new_keep=False
T12a             may_strip_prose keeps_prose o_del_new_keep=False
T13a             clears   clears   o_del_new_keep=False
M1a              clears   clears   o_del_new_keep=False
prose_indented   may_strip_prose keeps_prose o_del_new_keep=False
```

violations (old removes line / new keeps, outside authorised prose): none

## Post-E15/E16 green

```
...................................................................................................................
----------------------------------------------------------------------
Ran 115 tests in 14.574s

OK
exit: 0
hook contracts satisfied (2 shipped hook(s), 28 message case(s); committed modes checked)
exit: 0
template contracts satisfied
exit: 0
CASES: 
message cases: 28
```
