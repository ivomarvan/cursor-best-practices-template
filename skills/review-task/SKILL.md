---
name: review-task
description: >-
  APM Phase R — Independent adversarial review of a completed Task before Human review.
  The Reviewer (a different agent/model than the Coder) checks the git diff against
  spec.md and dod.md, verifies every DoD ✅ against real artifacts, hunts scope creep,
  false claims, missing tests, and writes review.md with an APPROVE / REQUEST CHANGES
  verdict. Use when: a Coder has finished a Task (report.md exists) and before the Human
  reviews it, or when Human asks to review/QA a task.
---

# Skill: APM Independent Task Review (Phase R)
<!-- cs: Skill: APM Nezávislá revize tasku (Fáze R) -->

## Why this role exists
<!-- cs: Proč tato role existuje -->

The Coder self-reports its own Definition of Done. LLMs systematically over-rate their
own work and mark `✅` for things that are not actually true. A **separate** agent — the
Reviewer — closes that gap before the Human spends attention. This is the
**evaluator–optimizer** pattern: a critic independent of the author.
<!-- cs: Coder si sám vyplňuje DoD. LLM systematicky přeceňuje vlastní práci a označí ✅
     i to, co neplatí. Samostatný agent Reviewer tuto mezeru uzavře dřív, než Human
     vynaloží pozornost. Jde o vzor evaluator–optimizer: kritik nezávislý na autorovi. -->

## Prerequisites
<!-- cs: Předpoklady -->

- You act as **Reviewer**, NOT the Coder. Use a strong-reasoning model assigned to the
  **Reviewer role** in `rules/00-model-policy.mdc` (not the cheap Coder model). If the
  Reviewer role is `unassigned`, ask the Human which model to use before reviewing.
- `task-NNN-name/spec.md`, `dod.md`, and `report.md` exist.
- The Coder's implementation is committed or present as a working-tree diff.

<!-- cs: Jsi Reviewer, ne Coder. Použij silný model — úroveň Planner z 00-model-policy.mdc.
     spec.md, dod.md a report.md existují. Implementace je v diffu. -->

## Trust boundary
<!-- cs: Hranice důvěry -->

Review against the **ground truth**, not the Coder's narrative:
<!-- cs: Reviewuj proti realitě, ne proti vyprávění Codera: -->
- Trusted: `spec.md`, `dod.md`, the actual `git diff`, the actual test run output.
- Treated skeptically: claims in `report.md` and `✅` marks in `dod.md` — **verify them**.
<!-- cs: Důvěřuj: spec.md, dod.md, skutečný git diff, skutečný výstup testů.
     Skepticky ber: tvrzení v report.md a ✅ v dod.md — ověř je. -->

## Steps
<!-- cs: Kroky -->

### Step R1 — Gather ground truth
<!-- cs: Krok R1 — Získej realitu -->

```bash
# What actually changed
git status
git diff                      # working tree, or:
git diff <base>..HEAD         # if the Coder committed
```

Read `spec.md` (Goal, Outputs, Context Bundle, Test Specification, DoD) and `dod.md`.
Read `report.md` last — as a claim to verify, not as truth.
<!-- cs: Přečti spec.md a dod.md. report.md čti až nakonec — jako tvrzení k ověření. -->

### Step R2 — Verify each Definition of Done item
<!-- cs: Krok R2 — Ověř každou položku DoD -->

For every `✅` in `dod.md`, confirm the artifact really exists:
<!-- cs: U každé ✅ v dod.md ověř, že artefakt skutečně existuje: -->
- File referenced → it is on disk and in the diff.
- Test referenced → run it; it actually passes.
- Endpoint referenced → it actually responds.
- Behavior referenced → there is a test or evidence proving it.

Any `✅` you cannot verify is a **finding** (severity: blocker).
<!-- cs: Každá ✅, kterou nelze ověřit, je nález (severity: blocker). -->

### Step R3 — Re-run the test suite independently
<!-- cs: Krok R3 — Spusť testy nezávisle -->

Do not trust the report's test numbers. Run them yourself:
```bash
# language-appropriate; e.g.
pytest tests/ -v --tb=short
```
Record real counts and exit code. Mismatch vs. `report.md` is a finding.
<!-- cs: Nevěř číslům v reportu. Spusť testy sám, zapiš skutečné počty a exit code.
     Nesoulad s report.md je nález. -->

### Step R4 — Adversarial checklist
<!-- cs: Krok R4 — Adversariální checklist -->

- **Spec conformance:** does the diff implement exactly the Goal/Outputs? Nothing missing?
  <!-- cs: Soulad se specem: dělá diff přesně Goal/Outputs? Nic nechybí? -->
- **Scope creep:** any change NOT required by the spec? Any file edited that the
  Context Bundle marked "Do not modify"?
  <!-- cs: Scope creep: změna mimo spec? Editace souboru označeného "Do not modify"? -->
- **Test adequacy:** happy path + edge case + error case present and meaningful (not
  assert-true placeholders)? Are the spec's named cases covered?
  <!-- cs: Dostatečnost testů: happy/edge/error případy reálné (ne assert True)? -->
- **Quality gates:** project rules honored (lint, types, docstrings, no `TODO`/`FIXME`,
  no hardcoded secrets/paths, structured logging not `print`)?
  <!-- cs: Kvalitativní brány: lint, typy, docstringy, žádné TODO/FIXME, žádné secrets/cesty,
       strukturované logování místo print? -->
- **Security:** untrusted input handled; no secret leakage (see `08-agent-security.mdc`).
  <!-- cs: Bezpečnost: ošetřený nedůvěryhodný vstup; žádný únik secrets. -->
- **Report integrity:** does `report.md § Odchylky od spec.md` disclose every deviation
  you found in the diff?
  <!-- cs: Integrita reportu: přiznává report všechny odchylky, které jsi našel v diffu? -->

### Step R5 — Write the Review
<!-- cs: Krok R5 — Napiš revizi -->

Create `task-NNN-name/review.md`:

```yaml
---
apm_category: task-review
apm_ref: E010.T020
apm_level: task
created_by: Reviewer
model: <model-name>
intended_for: Coder, Human
created_at: <YYYY-MM-DD>
updated_at: <YYYY-MM-DD>
---
```

Report language: **`<communication-language>`**. Required structure (cs headings shown;
use the English phrase as the `##` heading when `<lang-code>` = `en`):

```markdown
# Task Review: E010.T020 — <Task Name>

## Verdikt
APPROVE  — nebo —  REQUEST CHANGES (round N)

## Nálezy
| # | Severity | Místo | Popis | Doporučená oprava |
|---|----------|-------|-------|-------------------|
| 1 | blocker  | `src/x.py:42` | ✅ v dod.md, ale funkce neexistuje | implementovat / opravit dod.md |
| 2 | major    | tests | chybí error-case test ze spec | doplnit test |
| 3 | minor    | `src/x.py:10` | docstring chybí | doplnit |

## Ověření Definition of Done
Per-položkový výsledek: ✅ ověřeno / ❌ neplatí (s důvodem).

## Nezávislý výsledek testů
Příkaz, skutečné počty, exit code. Porovnání s report.md.

## Shrnutí
1–3 věty. Pokud APPROVE: připraveno pro Human review.
```

Severity: **blocker** (must fix), **major** (should fix), **minor** (nice to fix).
Verdict is **REQUEST CHANGES** if any blocker (or unresolved major) exists.
<!-- cs: Severity: blocker (nutno opravit), major (mělo by se), minor (drobnost).
     Verdikt REQUEST CHANGES, pokud existuje blocker (nebo nevyřešený major). -->

### Step R6 — Review loop (bounded)
<!-- cs: Krok R6 — Revizní smyčka (omezená) -->

```
round = 1
REVIEW → verdict
if APPROVE → hand to Human [FT.7]
if REQUEST CHANGES and round < 3:
    Coder fixes findings → updates report.md → round += 1 → REVIEW again
if REQUEST CHANGES and round == 3:
    STOP. Escalate to Human with the open findings — do not loop forever.
```

The Reviewer reports findings; the **Coder** fixes them (re-invoke `execute-task`
addressing `review.md`). The Reviewer never edits production code itself.
<!-- cs: Reviewer hlásí nálezy; opravuje je Coder (znovu execute-task podle review.md).
     Reviewer sám needituje produkční kód. Max 3 kola, pak eskalace na Humana. -->

## Output Checklist
<!-- cs: Výstupní checklist -->

- [ ] Ground truth gathered from real `git diff` (not from report.md) [R1]
- [ ] Every `dod.md` ✅ independently verified [R2]
- [ ] Test suite re-run by Reviewer; real counts recorded [R3]
- [ ] Adversarial checklist completed (scope creep, security, quality) [R4]
- [ ] `review.md` written with verdict + severity-tagged findings [R5]
- [ ] Loop bounded to 3 rounds; escalate if exceeded [R6]

## Additional resources
- [../../../rules/07-project-management.mdc](../../../rules/07-project-management.mdc)
- [../../../rules/00-model-policy.mdc](../../../rules/00-model-policy.mdc)
- [../execute-task/SKILL.md](../execute-task/SKILL.md)
- [../../../README.project_management.md](../../../README.project_management.md)
