# Slice for i0005 — Git hooks

- path: `i0001/i0005`
- depth: 1
- realization: not_claimed

## Intent nodes (read as truth)

- `doc/intent/nodes/i0001-harness.md`
- `doc/intent/nodes/i0005-git-hooks.md`

## Code owned by this node

- `hooks/README.md`
- `hooks/git/commit-msg`
- `hooks/session-start.sh`

## Contracts in force

- `i0001` c1: Relative links inside rules and skills resolve to existing files — `cmd: python3 tools/checks/template_checks.py --root .`
- `i0001` c2: Cursor discovers rules and skills through the .cursor symlinks — `cmd: python3 tools/checks/template_checks.py --root .`
- `i0005` c1: The commit-msg hook removes agent attribution and keeps everything else — `cmd: python3 tools/checks/hook_checks.py --root .`
- `i0005` c2: Every shipped hook is executable — `cmd: python3 tools/checks/hook_checks.py --root .`

Anything outside this list is not part of the task context.
