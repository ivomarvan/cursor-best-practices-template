---
run_id: 20260818-1414-commit-msg-block-boundary-4f
intent_ids: ["i0005", "i0004"]
role: Grader
model: n/a
complexity: high
status: done
---

# Grader for run doc/runs/20260818-1414-commit-msg-block-boundary-4f

Round 1, run by the Coordinator, 2026-08-18T14:33:00+02:00. Raw output, nothing edited.

```
$ git status --short
 M hooks/README.md
 M hooks/git/commit-msg
 M tools/checks/hook_checks.py
?? doc/runs/20260818-1414-commit-msg-block-boundary-4f/
```

```
$ python3 tools/intent/cli.py validate

5 node(s): 0 error(s), 0 warning(s)
exit_code=0
```

```
$ python3 tools/intent/cli.py scope --run doc/runs/20260818-1414-commit-msg-block-boundary-4f
scope clean (4 declared path(s))
exit_code=0
```

```
$ python3 tools/intent/cli.py realization check
realization layer consistent (4 entry/entries)
exit_code=0
```

```
$ python3 tools/checks/hook_checks.py --root .
hook contracts satisfied (2 shipped hook(s), 35 message case(s); committed modes checked)
exit_code=0
```

```
$ python3 tools/checks/template_checks.py --root .
template contracts satisfied
exit_code=0
```

```
$ python3 -m unittest discover -s tools/intent/tests -t tools
----------------------------------------------------------------------
Ran 99 tests in 0.237s

OK
exit_code=0
```

```
$ ruff check tools/
All checks passed!
exit_code=0
```

```
$ ruff format --check tools/
20 files already formatted
exit_code=0
```

```
$ python3 tools/intent/cli.py coverage
# Intent coverage

- contracts: 28
- machine-enforced: 28 (100%)
- review exceptions: 0
- files scanned: 58
- files outside any node: 0
exit_code=0
```

## Coordinator spot check — B5, the shape that mattered

Not a substitute for the Adversary; one probe on the blocker the escalation called the
serious one. Run in a scratch directory, on a temporary file, no repository state touched.

```
$ printf 'feat: x\n\nIntent: i0005\nCo-authored-by: Cursor <cursoragent@cursor.com>\n\n# Please enter the commit message for your changes. Lines starting\n# with '#' will be ignored, and an empty message aborts the commit.\n' > msg.txt
$ bash ./hook msg.txt
$ cat msg.txt
feat: x

Intent: i0005
$ git interpret-trailers --parse < msg.txt
Intent: i0005
```

The editor comment block is gone, the attribution with it, the intent trailer survives.

---

# Grader — round 2

Run by the Coordinator, 2026-08-18T14:52:00+02:00, after the Coder addressed FU-A and
FU-B. Raw output, nothing edited.

```
$ git status --short
 M hooks/README.md
 M hooks/git/commit-msg
 M tools/checks/hook_checks.py
?? doc/runs/20260818-1414-commit-msg-block-boundary-4f/
```

```
$ python3 tools/intent/cli.py validate

5 node(s): 0 error(s), 0 warning(s)
exit_code=0
```

```
$ python3 tools/intent/cli.py scope --run doc/runs/20260818-1414-commit-msg-block-boundary-4f
scope clean (4 declared path(s))
exit_code=0
```

```
$ python3 tools/checks/hook_checks.py --root .
hook contracts satisfied (2 shipped hook(s), 36 message case(s); committed modes checked)
exit_code=0
```

```
$ python3 tools/checks/template_checks.py --root .
template contracts satisfied
exit_code=0
```

```
$ python3 -m unittest discover -s tools/intent/tests -t tools
----------------------------------------------------------------------
Ran 99 tests in 0.413s

OK
exit_code=0
```

```
$ ruff check tools/
All checks passed!
exit_code=0
```

```
$ ruff format --check tools/
20 files already formatted
exit_code=0
```

```
$ git diff --stat doc/intent/_realization.yaml
(empty — no claim was recorded before the verdict)
```

---

# Grader — round 3 (revert of round 2)

Run by the Coordinator, 2026-08-18T15:20:00+02:00. Round 2 was reverted by Human decision
after the Adversary found B7 and B8. Raw output, nothing edited.

```
$ python3 tools/intent/cli.py validate
validate ok (5 node(s): 0 error(s), 0 warning(s))
exit_code=0
```

```
$ python3 tools/intent/cli.py scope --run doc/runs/20260818-1414-commit-msg-block-boundary-4f
scope clean (4 declared path(s))
exit_code=0
```

```
$ python3 tools/checks/hook_checks.py --root .
hook contracts satisfied (2 shipped hook(s), 35 message case(s); committed modes checked)
exit_code=0
```

The case count is back to 35, matching the state the Adversary approved in round 1.

```
$ python3 tools/checks/template_checks.py --root .
template contracts satisfied
exit_code=0
```

```
$ python3 -m unittest discover -s tools/intent/tests -t tools
Ran 99 tests in 0.350s

OK
exit_code=0
```

```
$ ruff check tools/ && ruff format --check tools/
ruff ok
exit_code=0
```

```
$ git diff --stat doc/intent/_realization.yaml
(realization untouched — no claim was recorded before the verdict)
```

## Coordinator spot checks on the reverted hook

Three shapes, scratch directory, temporary files, no repository state touched.

```
$ # B7 shape: commit -v buffer whose diff contains "-Intent: i0042"
$ bash ./hook msg.txt && git interpret-trailers --parse < msg.txt
Intent: i0005
```

```
$ # B4 shape: message ending in a blank line
$ bash ./hook m2.txt && git interpret-trailers --parse < m2.txt
Intent: i0005
```

```
$ # the "keeps everything else" half: a human co-author must survive
$ bash ./hook m3.txt && cat m3.txt
feat: z

Intent: i0005
Co-authored-by: Ivo Example <ivo@example.com>
```

B7 is gone with the heuristic that caused it, B4 stays dead, and legitimate content survives.
