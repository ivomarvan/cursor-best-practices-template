---
description: >-
  Assign an AI model to an APM role (Planner, Coder, Reviewer) by updating the
  Active Role Assignments table in rules/00-model-policy.mdc. Ask if role/model is missing.
  Use when: user says "/role-assign", "přiřaď roli/model", "set Planner model", or similar.
---

# Command: role-assign
<!-- cs: Příkaz: přiřazení modelu roli -->

## What this command does
<!-- cs: Co příkaz dělá -->

Records which model a given APM role should use, by updating the **Active Role Assignments**
table in `rules/00-model-policy.mdc`. Roles are not bound to fixed models — this command is
how the Human assigns them.
<!-- cs: Zaznamená, který model má daná APM role používat, úpravou tabulky Active Role
     Assignments v rules/00-model-policy.mdc. Role nejsou vázané na modely — takto je Human přiřazuje. -->

## Steps for the agent
<!-- cs: Kroky pro agenta -->

### Step 1 — Determine role(s) and model
<!-- cs: Krok 1 — Urči roli/role a model -->

Parse the Human's message for:
- **Role**: one or more of `Planner` | `Coder` | `Reviewer`.
- **Model**: the model id/name to assign (verbatim, as the Human writes it).

If the role or the model is missing or ambiguous, **ASK** the Human — list the three roles
and their current assignments, and let the Human name the model. Do **not** guess a model.
<!-- cs: Pokud role nebo model chybí či jsou nejasné, ZEPTEJ SE Humana — vypiš tři role
     a jejich aktuální přiřazení a nech Humana model pojmenovat. Model nehádej. -->

### Step 2 — Update the assignments table
<!-- cs: Krok 2 — Aktualizuj tabulku přiřazení -->

In `rules/00-model-policy.mdc`, *Active Role Assignments* table, set the row for each chosen
role: put the model in `Assigned model` and today's date in `Updated`. Change only those rows.
To clear an assignment, set the model back to `unassigned` and `Updated` to `—`.
<!-- cs: V rules/00-model-policy.mdc, tabulka Active Role Assignments, nastav řádek pro každou
     zvolenou roli: model do Assigned model, dnešní datum do Updated. Měň jen tyto řádky.
     Pro zrušení vrať model na `unassigned` a Updated na `—`. -->

### Step 3 — Confirm
<!-- cs: Krok 3 — Potvrď -->

- Echo the new assignment(s).
- Remind: Cursor does **not** auto-switch models — the Human must pick the model in the
  model selector when acting in that role.
<!-- cs: Zopakuj nová přiřazení. Připomeň: Cursor sám model nepřepíná — Human ho musí
     vybrat v selektoru modelu, když v té roli pracuje. -->

## Notes
<!-- cs: Poznámky -->

- This edits a tracked rule file; it is **not** a git commit. No git operations here.
  <!-- cs: Upravuje verzovaný soubor pravidla; není to git commit. Žádné git operace. -->
- See `/role-show` to display current assignments.
  <!-- cs: Viz /role-show pro zobrazení aktuálních přiřazení. -->
