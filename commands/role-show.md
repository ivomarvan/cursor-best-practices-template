---
description: >-
  Show the current APM role → model assignments from the resolved AGENT_MODELS config
  (doc/apm_config/AGENT_MODELS.user.md or .cursor/apm_config/AGENT_MODELS.default.md).
  Use when: user says "/role-show", "jaké role/modely", "which model for which role", or
  similar.
---

# Command: role-show
<!-- cs: Příkaz: zobrazení přiřazení rolí -->

## What this command does
<!-- cs: Co příkaz dělá -->

Displays which model each APM role (Planner, Coder, Reviewer) is currently assigned to.
<!-- cs: Zobrazí, jaký model má aktuálně přiřazena každá APM role (Planner, Coder, Reviewer). -->

## Steps for the agent
<!-- cs: Kroky pro agenta -->

### Step 1 — Read assignments
<!-- cs: Krok 1 — Přečti přiřazení -->

Read the resolved *Active Role Assignments* table: `doc/apm_config/AGENT_MODELS.user.md`
if it exists, otherwise `.cursor/apm_config/AGENT_MODELS.default.md` (see the Config
Resolution mechanism in `rules/200-project-design-rules.mdc`).
<!-- cs: Přečti vyřešenou tabulku Active Role Assignments: doc/apm_config/
     AGENT_MODELS.user.md, pokud existuje, jinak .cursor/apm_config/
     AGENT_MODELS.default.md (viz Config Resolution mechanismus v rules/20-project-
     design-rules.mdc). -->

### Step 2 — Present
<!-- cs: Krok 2 — Zobraz -->

Show the role × band table (`low`/`medium`/`high`, see `rules/000-model-policy.mdc`). For
any cell marked `unassigned`, note that the agent will **ask** the Human before acting in
that role/band (and that `/role-assign` can set it). A `—` cell (Planner `low`, Reviewer
`low`) means "not applicable" — never occurs / gate only — not "unassigned".
<!-- cs: Zobraz tabulku role × pásmo. U buňky `unassigned` upozorni, že se agent před prací
     v té roli/pásmu ZEPTÁ Humana (a že /role-assign ji nastaví). Buňka `—` (Planner low,
     Reviewer low) znamená "neaplikuje se" — nenastává / jen gate — ne "nepřiřazeno". -->

### Step 3 — Reminder
<!-- cs: Krok 3 — Připomínka -->

Note the Cursor limitation: the parent window's model is not auto-switched per role — the
Human selects it in the model selector; subagents get the model via the call's `model`
parameter (`rules/000-model-policy.mdc`, Resolution rule step 2).
<!-- cs: Připomeň omezení Cursoru: model rodičovského okna se per role nepřepíná — Human ho
     vybírá v selektoru; subagenti dostanou model parametrem model při volání
     (000-model-policy.mdc, krok 2). -->
