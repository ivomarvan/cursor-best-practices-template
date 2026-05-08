---
apm_category: task-spec
apm_ref: E010.T010
apm_level: task
created_by: Planner
model: <model-name>
intended_for: Coder
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
---

# Task Specification: E010.T010 — <Task Name>

## Goal
<!-- What must be built. 1–3 sentences. Coder implements exactly this — no more, no less. -->

## Inputs
- `<path/to/file>` — description of what to use from it
- <!-- list all files/data the Coder needs to read -->

## Outputs
- `<path/to/new/file>` — what it should contain
- `<path/to/modified/file>` — what to change and why

## Context Bundle

**Files to read:**
- `<path>` — reason

**Files NOT to modify:**
- `<path>` — reason (e.g. owned by another Task, infrastructure config)

**Interfaces from prior Tasks:**
- none  <!-- or: T010 exposes `<function/class>` in `<module>` -->

## Dependencies
- none  <!-- or: T010 must be completed first -->

## Test Specification

Write tests in `tests/<corresponding-path>/test_<name>.py` (or equivalent for the language).

- **Happy path:** <describe>
- **Edge case 1:** <describe>
- **Error/failure case:** <describe>

## Definition of Done

See `dod.md` for the checklist. Summary:
- [ ] <criterion 1>
- [ ] <criterion 2>
- [ ] All new tests pass
- [ ] Full test suite passes (no regressions)

## Recommended Coder Model
Composer-2  <!-- or: claude-opus-4-7 for complex reasoning tasks -->
