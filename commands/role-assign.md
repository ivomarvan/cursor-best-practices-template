---
description: >-
  Assign an AI model to an APM role (Planner, Coder, Reviewer) by updating the
  Active Role Assignments table in rules/00-model-policy.mdc. Ask if role/model is missing.
  Use when: user says "/role-assign", "přiřaď roli/model", "set Planner model", or similar.
---

# Command: role-assign

## What this command does

Records which model a given APM role should use, by updating the **Active Role Assignments**
table in `rules/00-model-policy.mdc`. Roles are not bound to fixed models — this command is
how the Human assigns them.

## Steps for the agent

### Step 1 — Determine role(s) and model

Parse the Human's message for:
- **Role**: one or more of `Planner` | `Coder` | `Reviewer`.
- **Model**: the model id/name to assign (verbatim, as the Human writes it).

If the role or the model is missing or ambiguous, **ASK** the Human — list the three roles
and their current assignments, and let the Human name the model. Do **not** guess a model.

### Step 2 — Update the assignments table

In `rules/00-model-policy.mdc`, *Active Role Assignments* table, set the row for each chosen
role: put the model in `Assigned model` and today's date in `Updated`. Change only those rows.
To clear an assignment, set the model back to `unassigned` and `Updated` to `—`.

### Step 3 — Confirm

- Echo the new assignment(s).
- Remind: Cursor does **not** auto-switch models — the Human must pick the model in the
  model selector when acting in that role.

## Notes

- This edits a tracked rule file; it is **not** a git commit. No git operations here.
- See `/role-show` to display current assignments.
