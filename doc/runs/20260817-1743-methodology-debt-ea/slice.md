# Slice for i0002 — Rules

- path: `i0001/i0002`
- depth: 1
- realization: not_claimed

## Intent nodes (read as truth)

- `doc/intent/nodes/i0001-harness.md`
- `doc/intent/nodes/i0002-rules.md`

## Code owned by this node

- `rules/00-communication-language.mdc`
- `rules/00-meta-rules-and-skills.mdc`
- `rules/00-model-policy.mdc`
- `rules/01-general-programming.mdc`
- `rules/02-git.mdc`
- `rules/03-docker-policy.mdc`
- `rules/04-docker-standards.mdc`
- `rules/05-new-technology.mdc`
- `rules/06-project-structure.mdc`
- `rules/07-ice-workflow.mdc`
- `rules/07-intent-tree.mdc`
- `rules/07-realization.mdc`
- `rules/07-run-artifacts.mdc`
- `rules/08-agent-security.mdc`
- `rules/09-testing.mdc`
- `rules/10-python.mdc`
- `rules/11-vuejs-vite-tailwind.mdc`
- `rules/12-cpp-esp32.mdc`
- `rules/13-sql-postgresql.mdc`
- `rules/14-fastapi.mdc`
- `rules/15-qdrant.mdc`
- `rules/16-sqlalchemy.mdc`
- `rules/17-redis.mdc`
- `rules/18-task-queue.mdc`
- `rules/20-project-design-rules.mdc`

## Contracts in force

- `i0001` c1: Relative links inside rules and skills resolve to existing files — `cmd: python3 tools/checks/template_checks.py --root .`
- `i0001` c2: Cursor discovers rules and skills through the .cursor symlinks — `cmd: python3 tools/checks/template_checks.py --root .`
- `i0002` c1: Every rule declares its activation: description, globs, or alwaysApply true — `cmd: python3 tools/checks/template_checks.py --root .`
- `i0002` c2: An always-applied rule stays within 150 lines, a scoped rule within 250 — `cmd: python3 tools/checks/template_checks.py --root .`

Anything outside this list is not part of the task context.
