---
name: execute-task
description: >-
  APM Phase T — Execute a single Task as the Coder: implement code, write tests,
  run regression check, fill Definition of Done, and write Task Report.
  Use when: Human or Planner assigns a Task to Coder, or when starting work on
  task-NNN-name/ directory that contains spec.md and dod.md.
---

# Skill: APM Task Execution (Phase T)
<!-- cs: Skill: APM Provedení Tasku (Fáze T) -->

## Prerequisites
<!-- cs: Předpoklady -->

- You are acting as **Coder**.
- `task-NNN-name/spec.md` exists (Task Specification + Context Bundle).
- `task-NNN-name/dod.md` exists (Definition of Done checklist to fill).
- All Tasks listed as dependencies in spec.md are completed.

<!-- cs: Jsi Coder. spec.md a dod.md existují. Závislé tasky jsou dokončeny. -->

## Steps
<!-- cs: Kroky -->

### Step 1 — Read Task Specification [FT.1]
<!-- cs: Krok 1 — Přečíst Task Specification [FT.1] -->

Read `spec.md` completely. Pay special attention to:
- **Context Bundle**: read every file listed; understand what must NOT be modified.
- **Interfaces from prior Tasks**: understand what you can call/import.
- **Test Specification**: plan tests before writing implementation code.
- **Definition of Done**: know the success criteria before you start.

### Step 2 — Implement [FT.2]
<!-- cs: Krok 2 — Implementovat [FT.2] -->

Follow all applicable project rules (language rules, docker policy, git conventions).
- Write code per spec — no scope creep beyond what `spec.md` describes.
- If you discover the spec is ambiguous or impossible: STOP and report to Human before continuing.
- Do not modify files listed in Context Bundle as "Do not modify".

### Step 3 — Write and Run Tests [FT.3]
<!-- cs: Krok 3 — Napsat a spustit testy [FT.3] -->

Write tests per the Test Specification in `spec.md`. Minimum:
- Happy path
- At least 1 edge case
- At least 1 error/failure case

Run tests:
```bash
# Python example
pytest tests/ -v

# Check all new tests pass
```

All new tests must pass. If any fail: fix implementation, not the test.

### Step 4 — Regression Check [FT.4]
<!-- cs: Krok 4 — Regresní check [FT.4] -->

Run the **full** test suite (not just Task tests):
```bash
pytest tests/ -v --tb=short
```

All previously passing tests must still pass. If regressions appear:
- Fix them before proceeding — do not suppress or skip.
- If fixing requires changing `spec.md` scope: STOP and notify Human.

### Step 5 — Fill Definition of Done [FT.5]
<!-- cs: Krok 5 — Vyplnit Definition of Done [FT.5] -->

Open `dod.md` and mark each criterion:
- `✅` — fully met
- `❌ <note>` — not met; explain why

Every criterion must be addressed. No silent skips.

**DoD integrity rule — mark `✅` only after verifying the artifact exists:**
<!-- cs: Pravidlo integrity DoD — označ ✅ pouze poté, co ověříš, že artefakt existuje. -->
- File referenced → file is on disk
- Test referenced → test actually passes
- Endpoint referenced → endpoint actually responds
- Report referenced → `report.md` is written

❌ Pre-emptively marking `✅` for unfinished work is a DoD integrity violation.
<!-- cs: Předčasné označení ✅ pro nedokončenou práci je porušení integrity DoD. -->

### Step 6 — Write Task Report [FT.6]
<!-- cs: Krok 6 — Napsat Task Report [FT.6] -->

Create `task-NNN-name/report.md`:

```yaml
---
apm_category: task-report
apm_ref: E010.T020
apm_level: task
created_by: Coder
model: <model-name>
intended_for: Human
created_at: <YYYY-MM-DD>
updated_at: <YYYY-MM-DD>
---
```

Report language: **`<communication-language>`** (from `00-communication-language.mdc`).

Required sections (write in `<communication-language>`):
```markdown
# Task Report: E010.T020 — <Task Name>

## Co bylo implementováno
Stručný popis implementace (2–5 vět).

## Vstupy a výstupy
- **Přečteno:** `src/db/models.py`, `doc/project-progress/spec.md`
- **Vytvořeno:** `src/db/migrations/0001_initial.py`, `tests/db/test_models.py`
- **Změněno:** `src/db/__init__.py`

## Použité metody a rozhodnutí
- Popis klíčových architektonických rozhodnutí a důvod.

## Odchylky od spec.md
Pokud žádné: `—`. Jinak pro každou odchylku: co, proč, dopad.

## Reference do kódu
- `src/db/models.py:15-42` — definice datových modelů
- `tests/db/test_models.py:1-60` — testy modelů

## Výsledek regresního testu
✅ Všechny testy projdou (47/47).
# or:
❌ Regrese: test_xyz selhalo — popis a fix.

## Definition of Done
Viz [dod.md](dod.md) — všechna kritéria ✅.
```

### Step 7 — Self-review before submitting [FT.7 prep]
<!-- cs: Krok 7 — Vlastní revize před odevzdáním [FT.7 prep] -->

Before signalling completion, verify:
- [ ] Code diff only touches files allowed by Context Bundle
- [ ] All new tests pass
- [ ] Full test suite passes (no regressions)
- [ ] `dod.md` fully filled (no blank checkboxes)
- [ ] Every `✅` in `dod.md` that references a file/test/endpoint → artifact actually exists
- [ ] Every deviation from `spec.md` → documented in `report.md § Odchylky`
- [ ] `report.md` written with **all** required sections (including `Odchylky od spec.md`)
- [ ] No `TODO`/`FIXME` left in committed code

## Output Checklist
<!-- cs: Výstupní checklist -->

- [ ] Implementation complete per `spec.md`
- [ ] New tests: all pass [FT.3]
- [ ] Full test suite: no regressions [FT.4]
- [ ] `dod.md` — all checkboxes filled ✅/❌ [FT.5]
- [ ] `report.md` — all required sections present in `<communication-language>` [FT.6]

## Git Commit (optional — only when triggered)
<!-- cs: Git commit (volitelný — jen pokud je trigger v příkazu) -->

If the Human's message contains a commit trigger phrase (`s commitem`, `s commitem s CI`,
`s commitem do feature`, `s commitem do feature s CI`), invoke skill `commit-task`
**after** completing Steps 1–7 above.
<!-- cs: Pokud příkaz obsahuje commit trigger phrase, aktivuj skill commit-task po dokončení kroků 1–7. -->

## Additional resources
- [../../../rules/07-project-management.mdc](../../../rules/07-project-management.mdc)
- [README.project_management.md](../../../README.project_management.md)
- [../commit-task/SKILL.md](../commit-task/SKILL.md)
