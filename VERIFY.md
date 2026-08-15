# VERIFY

The complete list of commands that prove this repository is in a valid state. The Grader
runs exactly these, in this order, and nothing else. It may not invent a command, and it
may not skip one because it "obviously passes".

Every project using this harness keeps its own `VERIFY.md` in its root, listing its own
commands. Changing this file forces complexity `high` — it is the definition of proof.

Run from the repository root, with any Python 3.11+ interpreter. No dependencies.

| # | Command | Expected | Proves |
|---|---------|----------|--------|
| 1 | `python3 tools/intent/cli.py validate` | exit 0 | the intent tree satisfies V1–V10 |
| 2 | `python3 -m unittest discover -s tools/intent/tests -t tools` | exit 0 | the tooling behaves as the contracts of `i0004` claim |
| 3 | `python3 tools/checks/template_checks.py --root .` | exit 0 | contracts of `i0001`, `i0002`, `i0003` |
| 4 | `python3 tools/checks/hook_checks.py --root .` | exit 0 | contracts of `i0005` |

All four in one line:

```bash
python3 tools/intent/cli.py validate \
  && python3 -m unittest discover -s tools/intent/tests -t tools \
  && python3 tools/checks/template_checks.py --root . \
  && python3 tools/checks/hook_checks.py --root .
```

When this repository is mounted in a project as `.cursor/`, prefix the paths:
`python3 .cursor/tools/intent/cli.py validate`. A consuming project verifies its own
code; it is not expected to run the harness's self-checks on every commit.

## Scope guard

`python3 tools/intent/cli.py scope --run doc/runs/<run>` is part of every run, but it is
not listed above because it takes an argument. The Coordinator runs it as part of
step 7 and records the output in `grader.md`.
