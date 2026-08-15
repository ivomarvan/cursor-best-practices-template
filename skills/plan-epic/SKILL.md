---
name: plan-epic
description: >-
  APM Phase E — Decompose an Epic into Tasks as the Planner.
  Creates epic-NNN/plan.md with Task Specifications and Context Bundles for the Coder.
  Use when: Human approves the Roadmap and asks Planner to plan the next Epic,
  or when an Epic needs to be broken down into implementable Tasks.
---

# Skill: APM Epic Planning (Phase E)

## Prerequisites

- You are acting as **Planner**.
- `doc/project-progress/spec.md` and `doc/project-progress/roadmap.md` exist and are approved.
- You know which Epic to plan (e.g. `E010`).
- Read the entire `spec.md` before starting — every Task must align with project goals.

## Steps

### Step 1 — Create Epic Directory [FE.1]

```bash
mkdir -p doc/project-progress/epic-NNN-short-name
```

Naming: `epic-010-setup-infrastructure`, `epic-020-core-api`, etc.

### Step 2 — Analyze and Decompose [FE.1]

Before writing, think through:
- What is the minimal deliverable of this Epic?
- What are the natural boundaries between Tasks (independent, testable units)?
- What order do Tasks depend on each other?
- Which Tasks are risky / complex enough to warrant a stronger Coder model?

Tasks should be **independently implementable** and **testable in isolation**.

### Step 3 — Write Epic Plan [FE.1]

Create `doc/project-progress/epic-NNN-name/plan.md`:

```yaml
---
apm_category: epic-plan
apm_ref: E010
apm_level: epic
created_by: Planner
model: <model-name>
intended_for: Coder, Human
created_at: <YYYY-MM-DD>
updated_at: <YYYY-MM-DD>
---
```

Epic Plan structure:
```markdown
# Epic Plan: E010 — Setup Infrastructure

## Epic Goal
One paragraph — what this Epic delivers when complete.

## Task List
| Task | Name | Depends on | Coder model | Complexity |
|------|------|-----------|-------------|------------|
| T010 | Create database schema | — | Coder role | low |
| T020 | Configure Docker services | T010 | Coder role | low |
| T030 | Write integration tests | T010, T020 | Coder role | medium |

## Task Specifications

### T010 — Create database schema
**Goal:** ...
**Inputs:** ...
**Outputs:** ...
**Context Bundle:**
- Read: `doc/project-progress/spec.md` (data model section)
- Do not modify: `docker-compose.yml`
- Interfaces from prior tasks: none
**Test Specification:** ...
**Definition of Done:**
- [ ] Migration file created in `src/db/migrations/`
- [ ] Migration runs without error: `alembic upgrade head`
- [ ] All tests pass
- [ ] No regressions in full test suite
**Recommended Coder model:** Coder role (Complexity: low) — model assigned per `00-model-policy.mdc`

### T020 — Configure Docker services
...
```

### Step 4 — Create Task Directories and Files [FE.1]

For each Task, create:
```
epic-NNN-name/
└── task-NNN-name/
    ├── spec.md    ← Task Specification + Context Bundle (extracted from plan.md)
    └── dod.md     ← Definition of Done checklist (blank checkboxes for Coder to fill)
```

`spec.md` front matter:
```yaml
---
apm_category: task-spec
apm_ref: E010.T020
apm_level: task
created_by: Planner
model: <model-name>
intended_for: Coder
created_at: <YYYY-MM-DD>
updated_at: <YYYY-MM-DD>
---
```

`dod.md` front matter:
```yaml
---
apm_category: dod
apm_ref: E010.T020
apm_level: task
created_by: Planner
model: <model-name>
intended_for: Coder
created_at: <YYYY-MM-DD>
updated_at: <YYYY-MM-DD>
---
```

`dod.md` content — blank checklist for Coder to fill:
```markdown
# Definition of Done: E010.T020

- [ ] <criterion 1>
- [ ] <criterion 2>
- [ ] All new tests pass
- [ ] Full test suite passes (no regressions)
```

### Step 5 — Human Review + Definition of Ready gate [FE.2]

Before presenting, self-check **every** Task against the **Definition of Ready (DoR)**
checklist in `07-project-management.mdc`. A vague spec guarantees a failed Task — the spec
is the quality gate. Fix any Task that fails DoR before handing it to a Coder.

Present `plan.md` to Human for approval.
Key review points Human should check:
- Each Task passes DoR (goal measurable, Context Bundle complete, DoD verifiable)?
- Task granularity reasonable (not too large, not trivial)?
- Dependencies correct?
- Recommended Coder model names the Coder role, with `Complexity: high` flagged where a
  stronger model is warranted (models assigned per `00-model-policy.mdc`)?

Do **not** start any Task until Human approves the Epic Plan.

## Output Checklist

- [ ] `epic-NNN-name/plan.md` — Epic goal + task table + all task specs
- [ ] `epic-NNN-name/task-NNN-name/spec.md` for each Task
- [ ] `epic-NNN-name/task-NNN-name/dod.md` for each Task (blank checkboxes)
- [ ] Dependencies between Tasks explicitly stated
- [ ] Recommended Coder model per Task names the Coder role + Complexity (models assigned per `00-model-policy.mdc`)
- [ ] Every Task passes the Definition of Ready checklist
- [ ] Human approved the Epic Plan [FE.2]

## Additional resources
- [../../../rules/07-project-management.mdc](../../../rules/07-project-management.mdc)
- [../../../rules/00-model-policy.mdc](../../../rules/00-model-policy.mdc)
- [README.project_management.md](../../../README.project_management.md)
