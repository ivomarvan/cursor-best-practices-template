---
name: review-epic
description: >-
  APM Phase ER — Close an Epic: Coder aggregates Task Reports into Epic Report,
  then Planner consults Human on Roadmap validity. Use when: all Tasks of an Epic
  are completed and approved, and it's time to write the Epic Report and review
  whether the Roadmap needs updating before proceeding to the next Epic.
---

# Skill: APM Epic Review and Closure (Phase ER)

## Prerequisites

- All Tasks of the current Epic are completed, **Reviewer-approved** (`review.md` =
  APPROVE), and Human-approved [Phase R, FT.7].
- All `task-NNN/report.md` and `task-NNN/review.md` files exist.
- You switch roles: **Coder** writes Epic Report → **Planner** leads Roadmap review.

## Part A — Epic Report (Coder) [FER.1]

### Step A1 — Read all Task Reports

Read every `task-NNN-name/report.md` in the Epic directory.
Identify: key decisions, patterns, problems encountered, notable outcomes.

### Step A2 — Write Epic Report

Create `epic-NNN-name/report.md`:

```yaml
---
apm_category: epic-report
apm_ref: E010
apm_level: epic
created_by: Coder
model: <model-name>
intended_for: Human, Planner
created_at: <YYYY-MM-DD>
updated_at: <YYYY-MM-DD>
---
```

Report language: **`<communication-language>`** (from `00-communication-language.mdc`).

Required sections:
```markdown
# Epic Report: E010 — <Epic Name>

## Shrnutí epiky
Co bylo v rámci epiky implementováno — 1 odstavec.

## Dokončené tasky
| Task | Název | Výsledek |
|------|-------|---------|
| T010 | Create database schema | ✅ |
| T020 | Configure Docker services | ✅ |

## Klíčová rozhodnutí a poznatky
- Rozhodnutí učiněná v průběhu epiky, která ovlivňují další vývoj.
- Problémy, na které jsme narazili, a jak jsme je vyřešili.

## Odchylky od Epic Planu
Co bylo jinak než plánováno? Proč? Jaký mělo dopad?

## Doporučení pro Planner
Poznatky z implementace relevantní pro plánování dalších Epik.
(Rizika, technický dluh, přidané závislosti, potřebné refaktory.)

## Reference
- Epic Plan: [plan.md](plan.md)
- Task Reports: [T010](task-010-name/report.md), [T020](task-020-name/report.md)
```

## Part B — Roadmap Review (Planner + Human) [FER.2]

### Step B1 — Planner reads Epic Report and current Roadmap

Read:
- `epic-NNN/report.md` (just written)
- `doc/project-progress/roadmap.md`
- `doc/project-progress/spec.md` (project goals — unchanged reference)

### Step B2 — Planner assesses Roadmap validity

Ask: given what we learned in this Epic, are the upcoming Epics still correct?
- Were assumptions in the spec invalidated?
- Did new dependencies or risks emerge?
- Is any planned Epic now unnecessary? Is a new Epic needed?

**ADR + spec reconciliation:** verify that any architectural decision made during the Epic
is captured as an ADR in `doc/architecture/decisions/` and is consistent with `spec.md`.
If implementation invalidated part of the spec, propose a spec update to the Human (the
spec is the single source of truth and must not silently rot).

### Step B3 — Present assessment to Human

Present one of three conclusions:

**A) Roadmap unchanged** — "Epics E020–E050 remain valid. Proceed to E020."

**B) Update needed** — Propose specific changes to `roadmap.md`:
```markdown
Proposed change: Insert E015 — Refactor auth layer
Reason: T030 revealed that the current auth interface won't scale to E020 requirements.
```

**C) Major revision** — Significant scope or architecture change; discuss with Human before writing.

### Step B4 — Update roadmap.md if approved

If Human approves changes: update `roadmap.md` front matter `updated_at` and content.
Inserting between E010 and E020: use `E015-name`.

## Human Review Checklist [FT.7 for Epic]

Human should verify before approving Epic closure:
- [ ] All Task `dod.md` files are fully ✅?
- [ ] All Task `review.md` verdicts are APPROVE?
- [ ] Epic Report accurately reflects what was built?
- [ ] Architectural decisions captured as ADRs and consistent with `spec.md`?
- [ ] Roadmap is still valid or updated with justified changes?
- [ ] No regressions in full test suite?

## Output Checklist

- [ ] `epic-NNN/report.md` — all required sections, in `<communication-language>` [FER.1]
- [ ] Roadmap reviewed with Human [FER.2]
- [ ] `roadmap.md` updated if needed (with updated_at)
- [ ] Human has confirmed readiness to proceed to next Epic

## Additional resources
- [../../../rules/07-project-management.mdc](../../../rules/07-project-management.mdc)
- [README.project_management.md](../../../README.project_management.md)
