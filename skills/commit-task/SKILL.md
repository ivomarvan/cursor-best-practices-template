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

## Prerequisites

- `git` configured: `user.name` and `user.email` set.
- `gh` CLI installed and authenticated:
  ```bash
  gh --version          # must be present
  gh auth status        # must show: Logged in to github.com
  ```
  Install: <https://cli.github.com/> · Auth: `gh auth login`
- Push access to the repository (for Variants A–D).
- **CI/CD note**: on GitHub Actions runners `gh` is pre-installed and auto-authenticated
  via `GITHUB_TOKEN` — no manual setup needed.

## Trigger Detection

Parse the Human's message to identify:
1. **Task list**: one or more tasks (e.g. T010, T020, T030) — execute in order.
2. **Variant** from phrase at end of message:

| Phrase CS | Phrase EN | Variant |
|---|---|---|
| `... s commitem` | `... with commit` | A — master, no CI |
| `... s commitem s CI` | `... with commit and CI` | B — master + CI |
| `... s commitem do feature` | `... with feature commit` | C — feature branch, no CI |
| `... s commitem do feature s CI` | `... with feature commit and CI` | D — feature branch + CI + squash merge |

## Branch Naming Convention

Feature branch name is derived automatically from the epic and task directory:
```
feature/e{epic_NNN}-t{task_NNN}-{task-slug}
```
`task-slug` = part of the task directory name after `task-NNN-`.

Examples:
- epic `epic-020-data-model` / task `task-010-domain-models` → `feature/e020-t010-domain-models`
- task `task-030-seed-data` → `feature/e020-t030-seed-data`

## Variant A — Commit to master (no CI)

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

## Variant B — Commit to master with CI (iterative, max 3 attempts)

For each task:
```bash
git add -A && git commit -m "<message>" && git push origin master
gh run watch --exit-status   # blocks; exit 0 = green, non-zero = failed
```

If CI fails → see [CI Fix Loop](#ci-fix-loop).
After green CI: proceed to next task (if group).

## Variant C — Commit to feature branch (no CI)

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

## Variant D — Feature branch + CI + squash merge to master

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

## CI Fix Loop

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

### Max Attempts Exceeded

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

## Group Tasks — Sequential Execution with Chained Branches

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
