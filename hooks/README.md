# .cursor/hooks

Cursor IDE hooks and shared git hooks for projects using this template.

## Structure

```
.cursor/
├── hooks.json           → Cursor project hooks registration (installer copies it here)
└── hooks/
    ├── session-start.sh → sessionStart: activates the git commit-msg hook
    ├── git/
    │   └── commit-msg   → strips Cursor auto-attribution from every commit message
    └── README.md        → this file
```

## What it solves

Cursor IDE automatically appends `Co-authored-by: Cursor <cursoragent@cursor.com>`
to every commit message at the git level — bypassing agent instructions.

The `commit-msg` git hook removes this trailer before git finalises the commit.

## How it activates

`session-start.sh` runs at every Cursor session start (registered in `hooks.json`).
If `core.hooksPath` is **unset**, it runs:

```bash
git config --local core.hooksPath .cursor/hooks/git
```

The setting persists in `.git/config` after the first session.

If `core.hooksPath` is already set to something else (husky, pre-commit, your own
hooks), the script **does not override it** — it prints a note to stderr instead. Keep
both by calling `.cursor/hooks/git/commit-msg "$1"` from your own `commit-msg` hook.

## Manual activation (after cloning without Cursor)

```bash
git config --local core.hooksPath .cursor/hooks/git
```

Run once per clone. No further steps needed.

## Installing into a project

Recommended (Option C in the root `README.md`):

```bash
python3 <template>/scripts/install_into_project.py --project <project-root> --lang cs
```

The installer copies `hooks.json` and `hooks/` into `<project-root>/.cursor/`. Open the
project in Cursor — the `sessionStart` hook activates automatically. Options A/B
(submodule at `.cursor/`) work the same way because the path `.cursor/hooks/git` is
constant in every variant.
