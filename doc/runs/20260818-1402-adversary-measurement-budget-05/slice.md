# Slice for i0003 — Skills

- path: `i0001/i0003`
- depth: 1
- realization: realized

## Intent nodes (read as truth)

- `doc/intent/nodes/i0001-harness.md`
- `doc/intent/nodes/i0003-skills.md`
- `doc/intent/nodes/i0002-rules.md`

## Code owned by this node

- `skills/commit-task/SKILL.md`
- `skills/docker-debug/SKILL.md`
- `skills/docker-new-project/SKILL.md`
- `skills/ice-implement/SKILL.md`
- `skills/ice-review/SKILL.md`
- `skills/ice-run/SKILL.md`
- `skills/intent-change/SKILL.md`
- `skills/postgresql-dev/SKILL.md`
- `skills/python-dev/SKILL.md`
- `skills/qdrant-dev/SKILL.md`
- `skills/sqlalchemy-dev/SKILL.md`
- `skills/vuejs-dev/SKILL.md`

## Contracts in force

- `i0001` c1: Relative links inside rules and skills resolve to existing files — `cmd: python3 tools/checks/template_checks.py --root .`
- `i0001` c2: Cursor discovers rules and skills through the .cursor symlinks — `cmd: python3 tools/checks/template_checks.py --root .`
- `i0003` c1: Every skill directory holds a SKILL.md declaring name and description — `cmd: python3 tools/checks/template_checks.py --root .`
- `i0003` c2: A skill stays within 500 lines — `cmd: python3 tools/checks/template_checks.py --root .`

Anything outside this list is not part of the task context.
