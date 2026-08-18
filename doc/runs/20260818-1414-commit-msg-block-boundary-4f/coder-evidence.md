---
run_id: 20260818-1414-commit-msg-block-boundary-4f
intent_ids: ["i0005", "i0004"]
role: Coder
model: claude-sonnet-5-thinking-high
complexity: high
status: in-progress
---

# Coder evidence — raw output

All commands below ran on scratch copies under `/tmp/coder4f/**`, never on this
repository's git state. `git commit` was invoked only inside throwaway repositories
created under `/tmp` (`/tmp/coder4f/b4repo`, `/tmp/coder4f/b5repo`, `/tmp/coder4f/b6repo`).

## 1. Patch application

```
$ git apply --check doc/runs/20260818-0853-harness-and-hooks-audit-86/deferred-i0005-hook.patch
$ echo $?
0
$ git apply doc/runs/20260818-0853-harness-and-hooks-audit-86/deferred-i0005-hook.patch
$ git diff --stat
 hooks/README.md             |  29 ++--
 hooks/git/commit-msg        | 109 +++++++++++--
 tools/checks/hook_checks.py | 386 +++++++++++++++++++++++++++++++++++++++++---
 3 files changed, 479 insertions(+), 45 deletions(-)
```

Applied cleanly, no conflicts, no hunks dropped.

## 2. B4/B5/B6 — manual demonstration, `git interpret-trailers --parse` as arbiter

### B4 — message ending in a blank line (`git commit -F`, no editor)

```
$ cd /tmp/coder4f/b4repo && git init -q && ...
$ printf 'feat: x\n\nIntent: i0005\nCo-authored-by: Cursor <cursoragent@cursor.com>\n\n' > /tmp/coder4f/b4msg.txt
$ git commit -q -F /tmp/coder4f/b4msg.txt
$ git log -1 --format=%B
feat: x

Intent: i0005

$ git log -1 --format=%B | git interpret-trailers --parse
Intent: i0005
```

No `cursoragent@cursor.com`, no `Cursor` trailer. B4 dead.

### B5 — plain editor commit; git's own help-text comment block trails the message

Raw `COMMIT_EDITMSG` git wrote before the (fake) editor touched it:

```
$
# Please enter the commit message for your changes. Lines starting
# with '#' will be ignored, and an empty message aborts the commit.
#
# On branch master
#
# Initial commit
#
# Changes to be committed:
#	new file:   file.txt
#
```

`GIT_EDITOR` script prepended `feat: x\n\nIntent: i0005\nCo-authored-by: Cursor <cursoragent@cursor.com>\n\n`
in front of that template and returned 0 (a normal successful edit).

```
$ GIT_EDITOR=/tmp/coder4f/fake_editor_b5.sh git commit -q
$ git log -1 --format=%B
feat: x

Intent: i0005

$ git log -1 --format=%B | git interpret-trailers --parse
Intent: i0005
```

No attribution. B5 dead — and this is the shape a normal Cursor-driven editor commit
takes today, so it is the one that mattered most.

### B6 — `git commit -v`: scissors marker plus a real diff

Raw `COMMIT_EDITMSG` git wrote for `-v` before the (fake) editor touched it:

```
$
# Please enter the commit message for your changes. Lines starting
# with '#' will be ignored, and an empty message aborts the commit.
#
# On branch master
#
# Initial commit
#
# Changes to be committed:
#	new file:   file.txt
#
# ------------------------ >8 ------------------------
# Do not modify or remove the line above.
# Everything below it will be ignored.
diff --git a/file.txt b/file.txt
new file mode 100644
index 0000000..587be6b
--- /dev/null
+++ b/file.txt
@@ -0,0 +1 @@
+x
```

Same prepend-and-succeed editor script.

```
$ GIT_EDITOR=/tmp/coder4f/fake_editor_v.sh git commit -v -q
$ git log -1 --format=%B
feat: x

Intent: i0005

$ git log -1 --format=%B | git interpret-trailers --parse
Intent: i0005
```

No attribution, no leaked diff line. B6 dead.

## 3. Baseline: full case suite green before any mutation

```
$ python3 tools/checks/hook_checks.py --root .
hook contracts satisfied (2 shipped hook(s), 35 message case(s); committed modes checked)
```

## 4. Failing-test evidence — one mutation per row of the plan's table

Method: a scratch copy of the repo's `hooks/` tree under `/tmp/coder4f/mutroot`, with only
`hooks/git/commit-msg` mutated per row; `python3 tools/checks/hook_checks.py --root /tmp/coder4f/mutroot`
run from the unmutated checkout of `hook_checks.py` in this repo. Restored to the unmutated
hook between rows.

### E-B4 — remove *both* trailing-blank-strip steps at once

The plan's table names a single mutation ("skip step 2"). The Critic's Note 1 measured
that skipping step 2 alone does not turn `attribution_then_trailing_blank_line` red,
because the second blank-strip inside step 3 is unconditional and repeats step 2's work
whether or not any comment lines were actually removed. Per the Critic's recommendation I
mutated both occurrences of `while (n > 0 && is_blank(lines[n])) n--` at once — this is
the row that actually demonstrates the boundary-detection defect the case exists to catch.

```
$ python3 tools/checks/hook_checks.py --root /tmp/coder4f/mutroot
ERROR hooks/git/commit-msg: case 'attribution_then_trailing_blank_line': output mismatch
--- expected
+++ actual
@@ -2,3 +2,5 @@

 Intent: i0005
 Run: 20260818-0853-cursor-audit-86
+
+Co-authored-by: Cursor <cursoragent@cursor.com>

ERROR hooks/git/commit-msg: case 'attribution_then_editor_comment_block': output mismatch
--- expected
+++ actual
@@ -2,3 +2,5 @@

 Intent: i0005
 Run: 20260818-0853-cursor-audit-86
+
+Co-authored-by: Cursor <cursoragent@cursor.com>

ERROR hooks/git/commit-msg: case 'attribution_then_scissors_and_diff': output mismatch
--- expected
+++ actual
@@ -2,3 +2,5 @@

 Intent: i0005
 Run: 20260818-0853-cursor-audit-86
+
+Co-authored-by: Cursor <cursoragent@cursor.com>

3 hook contract violation(s)
```

Named case `attribution_then_trailing_blank_line` fails, as promised (plus two more,
because removing both blank-strip mechanisms happens to also break the other two B-cases
here; that is a property of this particular double mutation, not a defect in those cases —
each of them also has its own dedicated single-mechanism mutation below).

### E-B5 — skip the trailing-comment-strip step

```
$ python3 tools/checks/hook_checks.py --root /tmp/coder4f/mutroot
ERROR hooks/git/commit-msg: case 'attribution_then_editor_comment_block': output mismatch
--- expected
+++ actual
@@ -2,3 +2,10 @@

 Intent: i0005
 Run: 20260818-0853-cursor-audit-86
+
+Co-authored-by: Cursor <cursoragent@cursor.com>
+
+# Please enter the commit message for your changes. Lines starting
+# with '#' will be ignored, and an empty message aborts the commit.
+#
+# On branch main

ERROR hooks/git/commit-msg: case 'attribution_then_scissors_and_diff': output mismatch
--- expected
+++ actual
@@ -2,3 +2,8 @@

 Intent: i0005
 Run: 20260818-0853-cursor-audit-86
+
+Co-authored-by: Cursor <cursoragent@cursor.com>
+
+# Please enter the commit message for your changes. Lines starting
+# with '#' will be ignored, and an empty message aborts the commit.

2 hook contract violation(s)
```

Named case `attribution_then_editor_comment_block` fails.

### E-B6 — skip the scissors-truncation step

```
$ python3 tools/checks/hook_checks.py --root /tmp/coder4f/mutroot
ERROR hooks/git/commit-msg: case 'attribution_then_scissors_and_diff': output mismatch
--- expected
+++ actual
@@ -2,3 +2,13 @@

 Intent: i0005
 Run: 20260818-0853-cursor-audit-86
+
+Co-authored-by: Cursor <cursoragent@cursor.com>
+
+# Please enter the commit message for your changes. Lines starting
+# with '#' will be ignored, and an empty message aborts the commit.
+# ------------------------ >8 ------------------------
+diff --git a/foo.py b/foo.py
+index abc123..def456 100644
+--- a/foo.py
++++ b/foo.py

1 hook contract violation(s)
```

Named case `attribution_then_scissors_and_diff` fails, and only that one.

### E-10 — remove `sub(/\r$/, "")` (CRLF normalization)

```
$ python3 tools/checks/hook_checks.py --root /tmp/coder4f/mutroot
ERROR hooks/git/commit-msg: case 'crlf_line_endings': output mismatch
--- expected
+++ actual
@@ -1,4 +1,4 @@
-feat(db): enforce unique user_id
-
-Intent: i0005
-Run: 20260818-0853-cursor-audit-86
+feat(db): enforce unique user_id
+
+Intent: i0005
+Run: 20260818-0853-cursor-audit-86

1 hook contract violation(s)
```

(Every line differs only by a trailing `\r`, invisible in this render but present in the
byte-exact comparison the fix in `tools/checks/hook_checks.py` now performs.) Named case
`crlf_line_endings` fails.

### E-11 — narrow `is_blank` to `/^$/`

```
$ python3 tools/checks/hook_checks.py --root /tmp/coder4f/mutroot
ERROR hooks/git/commit-msg: case 'blank_separator_only_spaces': output mismatch
--- expected
+++ actual
@@ -2,3 +2,4 @@
   
 Intent: i0005
 Run: 20260818-0853-cursor-audit-86
+Co-authored-by: Cursor <cursoragent@cursor.com>

1 hook contract violation(s)
```

Named case `blank_separator_only_spaces` fails, and only that one.

### E-12 — restrict the address rule to the trailer's key line

```
$ python3 tools/checks/hook_checks.py --root /tmp/coder4f/mutroot
ERROR hooks/git/commit-msg: case 'address_on_continuation_non_by_with': output mismatch
--- expected
+++ actual
@@ -2,3 +2,6 @@

 Intent: i0005
 Run: 20260818-0853-cursor-audit-86
+
+Note:
+  see cursoragent@cursor.com

1 hook contract violation(s)
```

Named case `address_on_continuation_non_by_with` fails, and only that one.

### E-13 — remove the orphan-continuation-with-address branch

```
$ python3 tools/checks/hook_checks.py --root /tmp/coder4f/mutroot
ERROR hooks/git/commit-msg: case 'orphan_continuation_with_address': output mismatch
--- expected
+++ actual
@@ -2,3 +2,5 @@

 Intent: i0005
 Run: 20260818-0853-cursor-audit-86
+
+  see cursoragent@cursor.com

1 hook contract violation(s)
```

Named case `orphan_continuation_with_address` fails, and only that one.

### E-14 — fold continuation lines without a separating space

```
$ python3 tools/checks/hook_checks.py --root /tmp/coder4f/mutroot
ERROR hooks/git/commit-msg: case 'folded_join_requires_space': output mismatch
--- expected
+++ actual
@@ -2,6 +2,3 @@

 Intent: i0005
 Run: 20260818-0853-cursor-audit-86
-
-Co-authored-by: Cur
-  sor Smith <human@example.com>

1 hook contract violation(s)
```

Named case `folded_join_requires_space` fails, and only that one.

## 5. Definition of Done commands, final state (unmutated hook)

```
$ python3 tools/checks/hook_checks.py --root .
hook contracts satisfied (2 shipped hook(s), 35 message case(s); committed modes checked)
$ python3 tools/checks/template_checks.py --root .
template contracts satisfied
$ python3 tools/intent/cli.py validate

5 node(s): 0 error(s), 0 warning(s)
$ python3 tools/intent/cli.py scope --run doc/runs/20260818-1414-commit-msg-block-boundary-4f
scope clean (4 declared path(s))
$ python3 -m unittest discover -s tools/intent/tests -t tools
...................................................................................................
----------------------------------------------------------------------
Ran 99 tests in 0.286s

OK
$ ruff check tools/
All checks passed!
$ ruff format --check tools/
20 files already formatted
```

All exit 0.

## 6. Round 2 — M1 (FU-A) and M2 (FU-B)

All commands below ran on scratch copies under `/tmp/coder4f_r2/**`; `git commit` only
inside throwaway repositories under `/tmp`.

### 6.1 M1 — reproducing FU-A against the pre-fix hook

```
$ printf 'feat: x\n\n# ------------------------ >8 ------------------------\nIntent: i0005\nRun: 20260818-0853-cursor-audit-86\nCo-authored-by: Cursor <cursoragent@cursor.com>\n' > msg.txt
$ bash hooks/git/commit-msg msg.txt   # pre-fix hook
$ cat msg.txt
feat: x
```

`Intent:` and `Run:` are gone, along with the attribution — the exact defect FU-A
describes: a comment line shaped like the scissors marker, sitting ahead of the trailer
block, is treated as first-match-from-start and silently swallows everything after it.

### 6.2 Evaluating the Adversary's suggestion ("first scissors from the end")

Reversing the scan direction alone does not fix this. With only one scissors-shaped
line in the file, "first match scanning from the start" and "first match scanning from
the end" name the *same* line — direction is irrelevant when there is exactly one
candidate, which is exactly FU-A's shape. Confirmed by inspection of the case above:
there is only one `>8` line, before the trailers, and no amount of re-ordering the scan
changes which line it finds.

The suggestion only does something when there are *two* scissors-shaped lines (a
crafted decoy plus git's own real one near the end). Direction alone is insufficient
for the reported defect; the missing ingredient is a check on what a candidate leaves
behind, not which end the scan starts from.

### 6.3 The fix implemented: rightmost scissors line with a "clean tail"

`hooks/git/commit-msg` now scans backward from the end and accepts the *first* candidate
it meets (i.e. the rightmost one) whose tail — everything strictly after it, up to the
end of file — contains no non-comment line shaped like a real trailer key. Git's own `-v`
scissors line is always followed only by two fixed help-text comments and then diff
content (which never has a bare `Key:` line — diff `+`/`-`/`@@`/`---`/`+++`/`index` lines
either start with a character outside the key grammar or contain no colon at all), so the
real boundary always has a clean tail and is always accepted. A decoy line placed ahead
of `Intent:`/`Run:` never has a clean tail — those lines are real trailer keys — so it is
rejected and left as ordinary text; nothing after it is discarded.

Single decoy line (FU-A's own case), same message as 6.1, run through the **fixed** hook:

```
$ bash hooks/git/commit-msg msg.txt   # fixed hook
$ cat msg.txt
feat: x

# ------------------------ >8 ------------------------
Intent: i0005
Run: 20260818-0853-cursor-audit-86
```

`Intent:`/`Run:` survive, the attribution trailer is gone, and the decoy line — never a
shape git itself writes — is kept verbatim rather than guessed at, consistent with
"keeps everything else".

Two scissors lines (decoy ahead of the trailers, git's real one at the true end with a
diff), through the fixed hook:

```
$ printf 'feat: x\n\n# ------------------------ >8 ------------------------\n\nIntent: i0005\nRun: 20260818-r2\nCo-authored-by: Cursor <cursoragent@cursor.com>\n\n# Please enter the commit message for your changes.\n# ------------------------ >8 ------------------------\ndiff --git a/f.txt b/f.txt\n+z\n' > two.txt
$ bash hooks/git/commit-msg two.txt
$ cat two.txt
feat: x

# ------------------------ >8 ------------------------

Intent: i0005
Run: 20260818-r2
```

The rightmost (real) scissors line is the one accepted — its tail is clean (only
help-text comments and diff) — so the diff and help text are discarded exactly as
before, while the decoy earlier in the file and the real trailers both survive.

### 6.4 An observed limit of `git interpret-trailers` itself on this shape

`git interpret-trailers --parse`, run directly on a message that still contains the
decoy `>8` line as literal text, also returns nothing for that message — it applies its
own unconditional scissors cut at *any* line shaped like the marker, wherever it sits,
independent of our hook:

```
$ printf 'feat: x\n\nIntent: i0005\n' | git interpret-trailers --parse
Intent: i0005
$ printf 'feat: x\n\n# ------------------------ >8 ------------------------\n\nIntent: i0005\n' | git interpret-trailers --parse
(empty)
```

This is `interpret-trailers`'s own behavior, not a consequence of anything our hook does
— confirmed separately by committing through a real throwaway repo and checking what git
itself keeps in `COMMIT_EDITMSG` cleanup (`--cleanup=strip`, no `-v`, no explicit
`--cleanup=scissors`): a decoy `>8` comment line is treated as an ordinary comment and
stripped like any other, without truncating anything after it —

```
$ GIT_EDITOR=true git commit --edit -F msg_default.txt -q   # default/strip cleanup, no -v
$ git log -1 --format=%B
feat: x

Co-authored-by: Cursor <cursoragent@cursor.com>

Intent: i0005
Run: 20260818-r2
```

— i.e. the decoy line only survives as literal text when git's *own* later cleanup does
not also remove it (e.g. `--cleanup=whitespace`, the default for `-F`/`-m` without
`--edit`); when it does (`strip`), the residue disappears on its own before the commit is
final. Either way `Intent:`/`Run:` are never lost. I did not attempt to make our hook
strip the decoy line itself: it is not attribution, not a shape git itself ever produces,
and removing arbitrary non-attribution content on a heuristic guess would trade a
theoretical loss of trailer-recognizability in `interpret-trailers` (on a shape git does
not write) for an actual, unconditional violation of "keeps everything else". Recorded
here rather than silently assumed away.

### 6.5 Failing-test evidence for M1 — case `scissors_before_trailer_block_keeps_trailers`

Mutation: revert the scissors detection to first-match-from-start with no clean-tail
guard (the pre-fix algorithm).

```
$ python3 tools/checks/hook_checks.py --root /tmp/coder4f_r2/mutroot
ERROR hooks/git/commit-msg: case 'scissors_before_trailer_block_keeps_trailers': output mismatch
--- expected
+++ actual
@@ -1,5 +1 @@
 feat(db): enforce unique user_id
-
-# ------------------------ >8 ------------------------
-Intent: i0005
-Run: 20260818-0853-cursor-audit-86

1 hook contract violation(s)
```

Named case `scissors_before_trailer_block_keeps_trailers` fails, and only that one.

### 6.6 M2 — is the first trailing-blank strip redundant?

Proof by cases, on the code as it stood entering this round (scissors handling, then
`site1` blank-strip, then comment-strip, then `site2` blank-strip):

- `site2`'s comment-strip loop (`while (n>0 && is_comment(lines[n])) n--`) only ever
  looks at the *current* last line. Whether `site1` ran or not, that last line is
  identical in both cases whenever the tail (after scissors handling) does not already
  end in blank — `site1` is then a no-op by definition (it only fires when the last
  line *is* blank) — so `site1`'s presence or absence cannot change what `site2`'s
  comment-strip sees or does.
- Whenever the tail *does* end in blank (no trailing comment block, e.g. `git commit -F`
  supplying its own trailing newlines), `site2`'s comment-strip is a no-op regardless
  (last line is blank, not a comment) either way, and `site2`'s own trailing blank-strip
  (which always runs, right after the comment-strip) removes exactly the same blanks
  `site1` would have.

So for every input, `site2` alone always reaches the same final `n` as `site1`+`site2`
together. `site1` is not "hard to test" — it is provably dead code. Removed, per the
instruction that dead code implying an unreal guard is worse than an honest gap.

### 6.7 Failing-test evidence for M2 — the remaining strip is load-bearing

Mutation: remove the sole remaining trailing-blank strip (the one after the
comment-strip loop) from the post-M1 hook.

```
$ python3 tools/checks/hook_checks.py --root /tmp/coder4f_r2/mutroot
ERROR hooks/git/commit-msg: case 'attribution_then_trailing_blank_line': output mismatch
--- expected
+++ actual
@@ -2,3 +2,5 @@

 Intent: i0005
 Run: 20260818-0853-cursor-audit-86
+
+Co-authored-by: Cursor <cursoragent@cursor.com>

ERROR hooks/git/commit-msg: case 'attribution_then_editor_comment_block': output mismatch
--- (same diff shape)
ERROR hooks/git/commit-msg: case 'attribution_then_scissors_and_diff': output mismatch
--- (same diff shape)

3 hook contract violation(s)
```

All three B-cases that rely on trailing-blank stripping fail once the single remaining
strip is gone — it is not a redundant step; it is the only one now, and it cuts on its
own. No new case was added for M2 since the existing cases already turn red on this
mutation without any vacuous re-test of what a second mechanism already covered.

### 6.8 Regression — round-1 mutations still cut correctly after the round-2 changes

```
$ python3 tools/checks/hook_checks.py --root /tmp/coder4f_r2/mutroot   # E-B5: comment-strip removed only
ERROR hooks/git/commit-msg: case 'attribution_then_editor_comment_block': output mismatch
ERROR hooks/git/commit-msg: case 'attribution_then_scissors_and_diff': output mismatch
2 hook contract violation(s)

$ python3 tools/checks/hook_checks.py --root /tmp/coder4f_r2/mutroot   # E-10: CRLF sub removed
ERROR hooks/git/commit-msg: case 'crlf_line_endings': output mismatch
1 hook contract violation(s)
```

Same named cases as round 1; no round-1 mutation regressed.

### 6.9 B4/B5/B6 regression against the round-2 hook, live git, `interpret-trailers` as arbiter

```
$ git log -1 --format=%B | git interpret-trailers --parse   # B4: -F, trailing blank line
Intent: i0005
$ git log -1 --format=%B | git interpret-trailers --parse   # B5: real editor commit
Intent: i0005
$ git log -1 --format=%B | git interpret-trailers --parse   # B6: real -v, scissors+diff
Intent: i0005
```

No `Co-authored-by: Cursor` / `cursoragent@cursor.com` in any of the three. B4/B5/B6
still dead after the round-2 changes.

### 6.10 Definition of Done commands, round 2 final state

```
$ python3 tools/checks/hook_checks.py --root .
hook contracts satisfied (2 shipped hook(s), 36 message case(s); committed modes checked)
$ python3 tools/checks/template_checks.py --root .
template contracts satisfied
$ python3 tools/intent/cli.py validate

5 node(s): 0 error(s), 0 warning(s)
$ python3 tools/intent/cli.py scope --run doc/runs/20260818-1414-commit-msg-block-boundary-4f
scope clean (4 declared path(s))
$ python3 -m unittest discover -s tools/intent/tests -t tools
...................................................................................................
----------------------------------------------------------------------
Ran 99 tests in 0.503s

OK
$ ruff check tools/
All checks passed!
$ ruff format --check tools/
20 files already formatted
```

All exit 0.

## 7. Round 3 — revert of round 2 (B7, B8)

The Adversary's round-2 review found B7 (the "clean remainder" scissors heuristic lets
attribution survive a `git commit -v` whose diff contains a `-Key:`-shaped removed line,
because `is_key` matches lines starting with `-`) and B8 (the redundancy proof for the
first trailing-blank strip does not hold for "comments then trailing blank"). The
Coordinator decided round 2 should not have been requested and ordered an exact revert
to the round-1 state. This section is that revert's evidence.

### 7.1 Byte-exact verification of the revert

`hooks/git/commit-msg` was restored by replacing the round-2 `END` block with the exact
text captured from reading the file at the start of round 2 (before any M1/M2 edit).
Diffed byte-for-byte against that captured text:

```
$ diff /tmp/coder4f_r3/round1_end_state.txt hooks/git/commit-msg
EXACT MATCH
```

`tools/checks/hook_checks.py`: the `Case("scissors_before_trailer_block_keeps_trailers", ...)`
block added in round 2 was deleted; the remaining 35 `Case(...)` entries are byte-identical
to round 1 (unchanged since round 1, never touched in round 2 except by that one addition).

```
$ python3 tools/checks/hook_checks.py --root .
hook contracts satisfied (2 shipped hook(s), 35 message case(s); committed modes checked)
```

35, not 36 — the revert removed exactly the one case that existed only to guard the
reverted heuristic.

### 7.2 B7 reproduction against the reverted (round-1) hook

Real throwaway repo: seed a file containing `Intent: i0042`, then edit it and run
`git commit -v` so the diff contains `-Intent: i0042` as a removed line — the exact shape
the Adversary named.

```
$ cd /tmp/coder4f_r3/b7repo
$ git init -q; git config core.hooksPath <round-1 hooks dir>
$ printf 'Intent: i0042\nsome other line\n' > f.txt && git add f.txt && git commit -q -m seed
$ printf 'changed content\n' > f.txt && git add f.txt
$ GIT_EDITOR=fake_editor.sh git commit -v -q   # editor prepends our message, keeps git's real -v template + diff
$ git log -1 --format=%B
feat: x

Intent: i0005

$ git log -1 --format=%B | git interpret-trailers --parse
Intent: i0005
```

No `Co-authored-by: Cursor <cursoragent@cursor.com>`, no `cursoragent@cursor.com` — the
round-1 scissors handling (first `>8` line from the start, no remainder check) truncates
the entire diff, `-Intent: i0042` included, before the trailer zone is ever computed.
This is exactly B7's scenario, now behaving correctly again.

### 7.3 B4/B5/B6 regression, live git, reverted hook

```
$ git log -1 --format=%B | git interpret-trailers --parse   # B4: -F, trailing blank line
Intent: i0005
$ git log -1 --format=%B | git interpret-trailers --parse   # B5: real editor commit
Intent: i0005
$ git log -1 --format=%B | git interpret-trailers --parse   # B6: real -v, plain diff
Intent: i0005
```

No attribution in any of the three.

### 7.4 Definition of Done commands, round 3 final state

```
$ python3 tools/checks/hook_checks.py --root .
hook contracts satisfied (2 shipped hook(s), 35 message case(s); committed modes checked)
$ python3 tools/checks/template_checks.py --root .
template contracts satisfied
$ python3 tools/intent/cli.py validate

5 node(s): 0 error(s), 0 warning(s)
$ python3 tools/intent/cli.py scope --run doc/runs/20260818-1414-commit-msg-block-boundary-4f
scope clean (4 declared path(s))
$ python3 -m unittest discover -s tools/intent/tests -t tools
...................................................................................................
----------------------------------------------------------------------
Ran 99 tests in 0.399s

OK
$ ruff check tools/
All checks passed!
$ ruff format --check tools/
20 files already formatted
```

All exit 0.
