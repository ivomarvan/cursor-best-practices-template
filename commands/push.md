---
description: >-
  Run full CI suite, then commit all changes with a smart message and push to master.
  Use when: user says "push".
  Explicit exception to 02-git.mdc: direct push to master is allowed here.
---

# Command: push

## What this command does

1. Runs `scripts/run_all_tests.sh` (project-specific CI mirror).
2. If any check fails → prints the failure and **stops**. No git operations.
3. If all checks pass → stages all changes, builds a commit message, commits, pushes.

## Steps for the agent

### Step 1 — Run CI checks

```bash
bash scripts/run_all_tests.sh
```

- If exit code ≠ 0: report which check failed, **stop here**. Do not proceed.
- If exit code = 0: continue.

### Step 2 — Stage all changes

```bash
git add -A
```

- Stages modified, new, and deleted files.
- Files listed in `.gitignore` are automatically excluded.
- Do **not** stage `.env` or any file containing real secrets.

### Step 3 — Inspect what will be committed

Run these read-only commands and use the output to build the commit message:

```bash
git status
git diff --staged
git log --oneline -5
```

### Step 4 — Build commit message

Follow Conventional Commits format (see `02-git.mdc`):

```
<type>(<scope>): <imperative description, max 72 chars>

<optional body: why, not what — wrap at 72 chars>
```

Rules:
- Infer `type` and `scope` from the staged diff and the recent conversation context.
- Use one type that best describes the dominant change.
- If changes span multiple concerns, list them in the body.
- Never use vague descriptions (`fix stuff`, `update`, `wip`).

**No Cursor attribution in commit messages** (Human policy):
- Do **not** append `Co-authored-by: Cursor <cursoragent@cursor.com>`, `Made-with: Cursor`,
  or any similar AI/Cursor trailer to the subject or body.
- Do **not** use `git commit --trailer=…` or any flag that injects attribution.
- The commit message must contain **only** what you write in step 4 — nothing else.

### Step 5 — Commit and push

```bash
git commit -m "$(cat <<'EOF'
<commit message from step 4>
EOF
)"

git push origin master
```

**Verify commit message (no attribution):** Cursor may inject attribution at runtime even
when the agent omits it. After `git commit`, run:

```bash
git log -1 --format=%B
```

If the output contains `Co-authored-by: Cursor`, `Made-with: Cursor`, or
`cursoragent@cursor.com`, **amend** the commit to remove those lines, then push:

```bash
git commit --amend -m "$(cat <<'EOF'
<same message from step 4 — no attribution lines>
EOF
)"
```

Re-check with `git log -1 --format=%B` before `git push`. Do not push until the message
is clean.

**Security note:** This is an explicit exception to the `02-git.mdc` prohibition on
direct master pushes. It is safe here because CI checks passed in step 1.

## Abort conditions

Stop immediately and report if any of the following is true:

- `scripts/run_all_tests.sh` exits with non-zero.
- `git status` shows nothing to commit (nothing staged after `git add -A`).
- Staged files include `.env`, credentials, or private keys.
