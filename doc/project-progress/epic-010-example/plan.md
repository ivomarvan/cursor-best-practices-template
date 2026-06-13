---
apm_category: epic-plan
apm_ref: E010
apm_level: epic
created_by: Planner
model: <model-name>
intended_for: Coder, Human
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
---

# Epic Plan: E010 — <Epic Name>

## Epic Goal
<!-- One paragraph — what this Epic delivers when all Tasks are complete. -->

## Task List

| Task | Name | Depends on | Coder model | Complexity |
|------|------|-----------|-------------|------------|
| T010 | <name> | — | Coder role | low |
| T020 | <name> | T010 | Coder role | low |

## Task Specifications

---

### T010 — <Task Name>

**Goal:**
<!-- What must be built. 1–3 sentences. -->

**Inputs:**
- <!-- Files to read, APIs, data provided -->

**Outputs:**
- <!-- Files to create/modify, interfaces to expose -->

**Context Bundle:**
- **Read:** `<path>` — reason
- **Do not modify:** `<path>`
- **Interfaces from prior Tasks:** none | `<Task>` provides `<interface>`

**Dependencies:** none | T010

**Test Specification:**
- Happy path: ...
- Edge case: ...
- Error case: ...

**Definition of Done:**
- [ ] <criterion 1>
- [ ] <criterion 2>
- [ ] All new tests pass
- [ ] Full test suite passes (no regressions)

**Recommended Coder model:** Coder role (Complexity: low) — model assigned per `rules/00-model-policy.mdc`

---

### T020 — <Task Name>

<!-- Repeat structure above -->
