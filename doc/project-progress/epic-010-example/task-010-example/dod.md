---
apm_category: dod
apm_ref: E010.T010
apm_level: task
created_by: Planner
model: <model-name>
intended_for: Coder
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
---

# Definition of Done: E010.T010 — <Task Name>

> Instructions for Coder: mark each item ✅ (met) or ❌ <note> (not met, with explanation).
> Every item must be addressed — no blanks. Blank = not reviewed = not done.

---

## Functional Criteria

- [ ] <criterion — e.g. "Database migration runs without error">
- [ ] <criterion — e.g. "API endpoint returns correct response for valid input">

## Test Criteria

- [ ] All new tests pass (`pytest tests/ -v`)
- [ ] Full test suite passes — no regressions (`pytest tests/ -v --tb=short`)

## Code Quality Criteria

- [ ] No `TODO`/`FIXME` left in committed code
- [ ] Linter passes without errors
- [ ] All public functions have docstrings

## Documentation Criteria

- [ ] `report.md` written with all required sections
- [ ] Code references in report point to correct files and line numbers

---

**Filled by Coder:** <model-name>, <YYYY-MM-DD>
