---
description: >-
  Show the current APM role → model assignments from the Active Role Assignments table
  in rules/00-model-policy.mdc. Use when: user says "/role-show", "jaké role/modely",
  "which model for which role", or similar.
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

Read the *Active Role Assignments* table in `rules/00-model-policy.mdc`.
<!-- cs: Přečti tabulku Active Role Assignments v rules/00-model-policy.mdc. -->

### Step 2 — Present
<!-- cs: Krok 2 — Zobraz -->

Show each role with its assigned model. For any role marked `unassigned`, note that the
agent will **ask** the Human before acting in that role (and that `/role-assign` can set it).
<!-- cs: Zobraz každou roli s přiřazeným modelem. U role `unassigned` upozorni, že se agent
     před prací v té roli ZEPTÁ Humana (a že /role-assign ji nastaví). -->

### Step 3 — Reminder
<!-- cs: Krok 3 — Připomínka -->

Note the Cursor limitation: models are not auto-switched per role; the Human selects the
model in the model selector.
<!-- cs: Připomeň omezení Cursoru: modely se per role nepřepínají automaticky; Human vybírá
     model v selektoru. -->
