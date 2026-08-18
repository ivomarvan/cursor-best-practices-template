# Grader for run doc/runs/20260818-0853-harness-and-hooks-audit-86

Round 4, run by the Coordinator, 2026-08-18T13:58:00+02:00, over the narrowed close:
the `i0005` hook work was withdrawn to `deferred-i0005-hook.patch` after the Adversary
escalated, so these numbers describe the `i0001` half plus FU-B, FU-C and FU-D.
Raw output, nothing edited. Rounds 1 to 3 are preserved above in `review.md`.

```
$ python3 tools/intent/cli.py validate

5 node(s): 0 error(s), 0 warning(s)
exit_code=0
```

```
$ python3 tools/intent/cli.py realization check
realization layer consistent (3 entry/entries)
exit_code=0
```

```
$ python3 tools/intent/cli.py scope --run doc/runs/20260818-0853-harness-and-hooks-audit-86
scope clean (10 declared path(s))
exit_code=0
```

```
$ python3 -m unittest discover -s tools/intent/tests -t tools
...................................................................................................
----------------------------------------------------------------------
Ran 99 tests in 0.419s

OK
exit_code=0
```

```
$ python3 tools/checks/template_checks.py --root .
template contracts satisfied
exit_code=0
```

```
$ python3 tools/checks/hook_checks.py --root .
hook contracts satisfied
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
