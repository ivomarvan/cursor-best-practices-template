---
description: >-
  Run full CI suite, then commit all changes with a smart message and push to master.
  Use when: user says "push".
  Explicit exception to 02-git.mdc: direct push to master is allowed here.
---

# Command: push
<!-- cs: Příkaz: push -->

## What this command does
<!-- cs: Co příkaz dělá -->

1. Runs `scripts/run_all_tests.sh` (project-specific CI mirror).
2. If any check fails → prints the failure and **stops**. No git operations.
3. If all checks pass → stages all changes, builds a commit message, commits, pushes.

<!-- cs:
1. Spustí scripts/run_all_tests.sh (projektový CI mirror).
2. Pokud některá kontrola selže → vypíše chybu a ZASTAVÍ se. Žádné git operace.
3. Pokud vše projde → přidá změny, sestaví commit message, commitne, pushne.
-->

## Steps for the agent
<!-- cs: Kroky pro agenta -->

### Step 1 — Run CI checks
<!-- cs: Krok 1 — Spusť CI kontroly -->

```bash
bash scripts/run_all_tests.sh
```

- If exit code ≠ 0: report which check failed, **stop here**. Do not proceed.
- If exit code = 0: continue.

<!-- cs:
- Pokud exit code ≠ 0: vypište která kontrola selhala, ZASTAVTE SE zde. Nepokračujte.
- Pokud exit code = 0: pokračujte.
-->

### Step 2 — Stage all changes
<!-- cs: Krok 2 — Přidej všechny změny -->

```bash
git add -A
```

- Stages modified, new, and deleted files.
- Files listed in `.gitignore` are automatically excluded.
- Do **not** stage `.env` or any file containing real secrets.

<!-- cs:
- Přidá změněné, nové i smazané soubory.
- Soubory v .gitignore jsou automaticky vynechány.
- NEPŘIDÁVEJTE .env ani soubory se skutečnými secrets.
-->

### Step 3 — Inspect what will be committed
<!-- cs: Krok 3 — Prozkoumej co se bude commitovat -->

Run these read-only commands and use the output to build the commit message:

```bash
git status
git diff --staged
git log --oneline -5
```

<!-- cs: Spusť tyto readonly příkazy a použij výstup pro sestavení commit message: -->

### Step 4 — Build commit message
<!-- cs: Krok 4 — Sestav commit message -->

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

<!-- cs:
Pravidla:
- Odvoďte type a scope z diff a kontextu nedávné konverzace.
- Použijte jeden typ, který nejlépe vystihuje dominantní změnu.
- Pokud změny zahrnují více témat, vypište je v těle.
- Nikdy nepoužívejte vágní popis (fix stuff, update, wip).
-->

### Step 5 — Commit and push
<!-- cs: Krok 5 — Commitni a pushni -->

```bash
git commit -m "$(cat <<'EOF'
<commit message from step 4>
EOF
)"

git push origin master
```

**Security note:** This is an explicit exception to the `02-git.mdc` prohibition on
direct master pushes. It is safe here because CI checks passed in step 1.

<!-- cs:
Bezpečnostní poznámka: Toto je explicitní výjimka ze zákazu přímého push na master
v 02-git.mdc. Je to bezpečné, protože CI kontroly prošly v kroku 1.
-->

## Abort conditions
<!-- cs: Podmínky zastavení -->

Stop immediately and report if any of the following is true:
<!-- cs: Okamžitě zastavte a nahlaste pokud platí cokoliv z následujícího: -->

- `scripts/run_all_tests.sh` exits with non-zero.
- `git status` shows nothing to commit (nothing staged after `git add -A`).
- Staged files include `.env`, credentials, or private keys.
