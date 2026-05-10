---
name: commit-task
description: >-
  Git commit workflow activated by explicit trigger phrases in Human messages.
  Handles 4 variants: direct master commit, master+CI iterative check,
  new feature branch commit, feature branch+CI with squash merge to master.
  For groups of tasks: chained feature branches, each task one commit,
  only the last branch merges to master.
  Use when: Human uses "s commitem", "s commitem s CI",
  "s commitem do feature", or "s commitem do feature s CI" (CS),
  or "with commit", "with commit and CI", "with feature commit",
  "with feature commit and CI" (EN) in their message.
---

# Skill: Git Commit Workflow
<!-- cs: Skill: Git commit workflow -->

## Trigger Detection
<!-- cs: Detekce triggeru -->

Parse the Human's message to identify:
1. **Task list**: one or more tasks (e.g. T010, T020, T030) — execute in order.
2. **Variant** from phrase at end of message:

| Phrase CS | Phrase EN | Variant |
|---|---|---|
| `... s commitem` | `... with commit` | A — master, no CI |
| `... s commitem s CI` | `... with commit and CI` | B — master + CI |
| `... s commitem do feature` | `... with feature commit` | C — feature branch, no CI |
| `... s commitem do feature s CI` | `... with feature commit and CI` | D — feature branch + CI + squash merge |

<!-- cs: Parsuj seznam tasků a variantu z trigger phrase. -->

## Branch Naming Convention
<!-- cs: Pojmenování větví -->

Feature branch name is derived automatically from the epic and task directory:
```
feature/e{epic_NNN}-t{task_NNN}-{task-slug}
```
`task-slug` = part of the task directory name after `task-NNN-`.

Examples:
- epic `epic-020-data-model` / task `task-010-domain-models` → `feature/e020-t010-domain-models`
- task `task-030-seed-data` → `feature/e020-t030-seed-data`

<!-- cs: Slug = část adresáře tasku za task-NNN-. Název se odvozuje automaticky. -->

## Variant A — Commit to master (no CI)
<!-- cs: Varianta A — Commit do master (bez CI) -->

For each task in order (one commit per task, directly on `master`):
```bash
git add -A
git commit -m "$(cat <<'EOF'
<conventional-commit-message>

Epic: <epic-name>
Task: <task-name>
EOF
)"
git push origin master
```

<!-- cs: Každý task = jeden commit přímo na master, sekvenčně. -->

## Variant B — Commit to master with CI (iterative, max 3 attempts)
<!-- cs: Varianta B — Commit do master s CI (iterativní, max 3 pokusy) -->

For each task:
```bash
git add -A && git commit -m "<message>" && git push origin master
gh run watch --exit-status   # blocks; exit 0 = green, non-zero = failed
```

If CI fails → see [CI Fix Loop](#ci-fix-loop).
After green CI: proceed to next task (if group).

<!-- cs: Po zelené CI pokračuj k dalšímu tasku. Při selhání: CI Fix Loop. -->

## Variant C — Commit to feature branch (no CI)
<!-- cs: Varianta C — Commit do feature větve (bez CI) -->

**First task** (or single task) — branch from `master`:
```bash
git checkout master
git checkout -b feature/e{NNN}-t{NNN}-{slug}
git add -A && git commit -m "<message>"
git push -u origin feature/e{NNN}-t{NNN}-{slug}
```

**Each subsequent task in group** — branch from the previous feature branch:
```bash
# while on previous feature branch:
git checkout -b feature/e{NNN}-t{NNN}-{slug}
git add -A && git commit -m "<message>"
git push -u origin feature/e{NNN}-t{NNN}-{slug}
```

No merge to master — Human decides when to merge.
<!-- cs: Žádný merge do master — rozhoduje Human. Každá větev navazuje na předchozí. -->

## Variant D — Feature branch + CI + squash merge to master
<!-- cs: Varianta D — Feature větev + CI + squash merge do master -->

Same branching as Variant C. After each task's push, check CI:
```bash
gh run watch --exit-status
```

If CI fails → see [CI Fix Loop](#ci-fix-loop).
After **last task** CI is green, squash-merge the last feature branch to master:
```bash
gh pr create \
  --title "<conventional-commit-title>" \
  --body "$(cat <<'EOF'
Tasks: <list>
Epic: <epic-name>
EOF
)" \
  --base master
gh pr merge --squash --delete-branch
```

<!-- cs: Squash merge přes gh CLI jen po zelené CI posledního tasku. -->

## CI Fix Loop
<!-- cs: CI Fix Loop -->

Max **3 total push attempts** (original + 2 fix commits).

```
attempt = 1
PUSH → gh run watch --exit-status
if green → continue
if red AND attempt < 3:
  attempt += 1
  gh run view --log-failed   # read CI logs to identify the failure
  → fix code / tests / lint
  git add -A
  git commit -m "fix(<scope>): address CI failure attempt {attempt}"
  git push
  → repeat from gh run watch
if red AND attempt == 3:
  → STOP — see Max Attempts Exceeded below
```

<!-- cs: Max 3 pokusy. Po každém selhání: přečti logy, oprav, commit, push, opakuj. -->

### Max Attempts Exceeded
<!-- cs: Překročení max počtu pokusů -->

1. Stay on current branch — do NOT merge to master.
2. Add failure section to current task's `report.md`:
   ```markdown
   ## CI Failure — Manual Intervention Required
   - CI step that failed: <step name>
   - Errors encountered: <summary>
   - Attempts made: 3
   - Remaining issue: <description of what still fails and why>
   ```
3. Report to Human: summarize what failed, what was tried, what is needed.

<!-- cs: Zůstaň na větvi, zapiš do report.md, předej Humanovi. -->

## Group Tasks — Sequential Execution with Chained Branches
<!-- cs: Skupinové tasky — sekvenční provedení s řetězenými větvemi -->

Example: `Proveď T010, T020, T030 s commitem do feature s CI`

```
master
  └─ feature/e020-t010-domain-models    ← execute T010, commit, CI green
       └─ feature/e020-t020-repository  ← execute T020, commit, CI green
            └─ feature/e020-t030-seed   ← execute T030, commit, CI green
                 └─ squash merge → master
```

Rules:
- Execute the task before committing (if not yet done).
- Each new branch is created from the previous feature branch (not from `master`).
- Squash merge to master only after the **last task's** CI is green.
- If any task fails CI after max attempts: STOP, report, do NOT proceed to next task.

<!-- cs: Každá větev navazuje na předchozí. Merge jen po zelené CI posledního. Při selhání: zastav. -->
