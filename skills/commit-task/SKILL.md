---
name: commit-task
description: >-
  Git commit workflow activated by explicit trigger phrases in Human messages.
  Handles 4 variants: direct master commit, master+CI iterative check,
  new feature branch commit, feature branch+CI with squash merge to master.
  For groups of runs: chained feature branches, each run one commit,
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
1. **Run list**: one or more ICE runs (directories under `doc/runs/`) — execute in order.
2. **Variant** from phrase at end of message:

| Phrase CS | Phrase EN | Variant |
|---|---|---|
| `... s commitem` | `... with commit` | A — master, no CI |
| `... s commitem s CI` | `... with commit and CI` | B — master + CI |
| `... s commitem do feature` | `... with feature commit` | C — feature branch, no CI |
| `... s commitem do feature s CI` | `... with feature commit and CI` | D — feature branch + CI + squash merge |

## Branch Naming Convention

Feature branch name is derived from the affected intent node and the run slug:
```
feature/{iNNNN}-{run-slug}
```
`run-slug` = the descriptive part of the run directory name, without date and suffix.

Examples:
- run `20260815-1328-user-email-a7` on node `i0042` → `feature/i0042-user-email`
- run `20260816-0900-rate-limit-3c` on node `i0031` → `feature/i0031-rate-limit`

## Commit Message Trailers

Every commit produced by this skill ends with machine-checkable trailers, so the history
links back to the intent:

```
Intent: i0042
Run: 20260815-1328-user-email-a7
```

## Variant A — Commit to master (no CI)

For each run in order (one commit per run, directly on `master`):
```bash
git add -A
git commit -m "$(cat <<'EOF'
<conventional-commit-message>

Intent: <iNNNN>
Run: <run_id>
EOF
)"
git push origin master
```

## Variant B — Commit to master with CI (iterative, max 3 attempts)

For each run:
```bash
git add -A && git commit -m "<message>" && git push origin master
gh run watch --exit-status   # blocks; exit 0 = green, non-zero = failed
```

If CI fails → see [CI Fix Loop](#ci-fix-loop).
After green CI: proceed to the next run (if a group).

## Variant C — Commit to feature branch (no CI)

**First run** (or single run) — branch from `master`:
```bash
git checkout master
git checkout -b feature/{iNNNN}-{slug}
git add -A && git commit -m "<message>"
git push -u origin feature/{iNNNN}-{slug}
```

**Each subsequent run in the group** — branch from the previous feature branch:
```bash
# while on previous feature branch:
git checkout -b feature/{iNNNN}-{slug}
git add -A && git commit -m "<message>"
git push -u origin feature/{iNNNN}-{slug}
```

No merge to master — Human decides when to merge.

## Variant D — Feature branch + CI + squash merge to master

Same branching as Variant C. After each run's push, check CI:
```bash
gh run watch --exit-status
```

If CI fails → see [CI Fix Loop](#ci-fix-loop).
After the **last run's** CI is green, squash-merge the last feature branch to master:
```bash
gh pr create \
  --title "<conventional-commit-title>" \
  --body "$(cat <<'EOF'
Runs: <list>
Intent: <iNNNN>
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
2. Add a failure section to the current run's `report.md`:
   ```markdown
   ## CI Failure — Manual Intervention Required
   - CI step that failed: <step name>
   - Errors encountered: <summary>
   - Attempts made: 3
   - Remaining issue: <description of what still fails and why>
   ```
3. Report to Human: summarize what failed, what was tried, what is needed.

## Groups of Runs — Sequential Execution with Chained Branches

Example: `Proveď běhy A, B, C s commitem do feature s CI`

```
master
  └─ feature/i0042-domain-models    ← run A, commit, CI green
       └─ feature/i0043-repository  ← run B, commit, CI green
            └─ feature/i0044-seed   ← run C, commit, CI green
                 └─ squash merge → master
```

Rules:
- Finish the run (Grader green, review closed) before committing.
- Each new branch is created from the previous feature branch (not from `master`).
- Squash merge to master only after the **last run's** CI is green.
- If any run fails CI after max attempts: STOP, report, do NOT proceed to the next run.
