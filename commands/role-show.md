---
description: >-
  Show the current APM role → model assignments from the Active Role Assignments table
  in rules/00-model-policy.mdc. Use when: user says "/role-show", "jaké role/modely",
  "which model for which role", or similar.
---

# Command: role-show

## What this command does

Displays which model each APM role (Planner, Coder, Reviewer) is currently assigned to.

## Steps for the agent

### Step 1 — Read assignments

Read the *Active Role Assignments* table in `rules/00-model-policy.mdc`.

### Step 2 — Present

Show each role with its assigned model. For any role marked `unassigned`, note that the
agent will **ask** the Human before acting in that role (and that `/role-assign` can set it).

### Step 3 — Reminder

Note the Cursor limitation: models are not auto-switched per role; the Human selects the
model in the model selector.
