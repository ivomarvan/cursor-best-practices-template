---
run_id: 20260817-1743-methodology-debt-ea
intent_ids: ["i0002"]
role: Grader
model: none — the Grader is not a language model
complexity: high
status: in-progress
---

# Grader log

No new tests and no failing-test evidence: the enforcer of `i0002` is
`template_checks.py`, and the change is textual decisions only.

## Gates

### `python3 tools/intent/cli.py validate`

```
5 node(s): 0 error(s), 0 warning(s)
```

exit code: 0

### `python3 tools/intent/cli.py realization check`

```
realization layer consistent (1 entry/entries)
```

exit code: 0

### `python3 -m unittest discover -s tools/intent/tests -t tools`

```
..................................................................................
----------------------------------------------------------------------
Ran 82 tests in 0.480s

OK
```

exit code: 0

### `python3 tools/checks/template_checks.py --root .`

```
template contracts satisfied
```

exit code: 0

### `python3 tools/checks/hook_checks.py --root .`

```
hook contracts satisfied
```

exit code: 0

### `python3 tools/intent/cli.py scope --run doc/runs/20260817-1743-methodology-debt-ea`

```
scope clean (3 declared path(s))
```

exit code: 0

## Definition of Done evidence (not gates)

### `wc -l rules/07-ice-workflow.mdc rules/00-model-policy.mdc`

```
 118 rules/07-ice-workflow.mdc
  96 rules/00-model-policy.mdc
 214 total
```

exit code: 0

### `grep -c 'cursor-grok-4.6-high' AGENT_MODELS.md`

```
0
```

exit code: 1 (no matches — expected)

## Re-grade after Adversary fix (R2 older sentence)

Reconciled the pre-R2 lead-in in `rules/00-model-policy.mdc` so the parent-window
reminder is a courtesy for a role the catalog does not govern. The three R2 paragraphs
are unchanged.

### `python3 tools/intent/cli.py validate`

```
5 node(s): 0 error(s), 0 warning(s)
```

exit code: 0

### `python3 tools/intent/cli.py realization check`

```
realization layer consistent (1 entry/entries)
```

exit code: 0

### `python3 -m unittest discover -s tools/intent/tests -t tools`

```
..................................................................................
----------------------------------------------------------------------
Ran 82 tests in 0.309s

OK
```

exit code: 0

### `python3 tools/checks/template_checks.py --root .`

```
template contracts satisfied
```

exit code: 0

### `python3 tools/checks/hook_checks.py --root .`

```
hook contracts satisfied
```

exit code: 0

### `python3 tools/intent/cli.py scope --run doc/runs/20260817-1743-methodology-debt-ea`

```
scope clean (3 declared path(s))
```

exit code: 0

### `wc -l rules/07-ice-workflow.mdc rules/00-model-policy.mdc`

```
 118 rules/07-ice-workflow.mdc
  97 rules/00-model-policy.mdc
 215 total
```

exit code: 0

### `grep -c 'cursor-grok-4.6-high' AGENT_MODELS.md`

```
0
```

exit code: 1 (no matches — expected)

## Re-grade after Human scope extension (`AGENT_MODELS.explanation.md`)

Dated Czech note (2026-08-17) added after `## Podklady`: available Grok
subagent slugs, catalog band mapping, supersession of four table rows and the
"Grok 4.5 does not belong" sentence. Tables and original argument untouched.

### `python3 tools/intent/cli.py validate`

```
5 node(s): 0 error(s), 0 warning(s)
```

exit code: 0

### `python3 tools/intent/cli.py realization check`

```
realization layer consistent (1 entry/entries)
```

exit code: 0

### `python3 -m unittest discover -s tools/intent/tests -t tools`

```
..................................................................................
----------------------------------------------------------------------
Ran 82 tests in 0.316s

OK
```

exit code: 0

### `python3 tools/checks/template_checks.py --root .`

```
template contracts satisfied
```

exit code: 0

### `python3 tools/checks/hook_checks.py --root .`

```
hook contracts satisfied
```

exit code: 0

### `python3 tools/intent/cli.py scope --run doc/runs/20260817-1743-methodology-debt-ea`

```
scope clean (4 declared path(s))
```

exit code: 0

### `wc -l AGENT_MODELS.explanation.md rules/07-ice-workflow.mdc rules/00-model-policy.mdc`

```
  163 AGENT_MODELS.explanation.md
  118 rules/07-ice-workflow.mdc
   97 rules/00-model-policy.mdc
```

exit code: 0

### `grep -c 'cursor-grok-4.6-high' AGENT_MODELS.md`

```
0
```

exit code: 1 (no matches — expected)

## Re-grade after Adversary non-blocking polish

(1) Dropped the unverifiable claim that Grok 4.6 high effort is available in
the Cursor UI; parent-window clause now follows only `00-model-policy.mdc`.
(2) One Czech sentence above the Role × pásmo table points at the note and
names the four superseded rows. Tables untouched.

### `python3 tools/intent/cli.py validate`

```
5 node(s): 0 error(s), 0 warning(s)
```

exit code: 0

### `python3 tools/intent/cli.py realization check`

```
realization layer consistent (1 entry/entries)
```

exit code: 0

### `python3 -m unittest discover -s tools/intent/tests -t tools`

```
..................................................................................
----------------------------------------------------------------------
Ran 82 tests in 0.305s

OK
```

exit code: 0

### `python3 tools/checks/template_checks.py --root .`

```
template contracts satisfied
```

exit code: 0

### `python3 tools/checks/hook_checks.py --root .`

```
hook contracts satisfied
```

exit code: 0

### `python3 tools/intent/cli.py scope --run doc/runs/20260817-1743-methodology-debt-ea`

```
scope clean (4 declared path(s))
```

exit code: 0

### `wc -l AGENT_MODELS.explanation.md`

```
166 AGENT_MODELS.explanation.md
```

exit code: 0
