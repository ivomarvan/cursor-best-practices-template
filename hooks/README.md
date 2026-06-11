# .cursor/hooks

Cursor IDE hooks and shared git hooks for projects using this submodule.

## Structure

```
hooks/
├── hooks.json           → Cursor project hooks (place at project root or .cursor/)
├── session-start.sh     → sessionStart: activates the git commit-msg hook
├── git/
│   └── commit-msg       → strips Cursor auto-attribution from every commit message
└── README.md            → this file
```

## What it solves

Cursor IDE automatically appends `Co-authored-by: Cursor <cursoragent@cursor.com>`
to every commit message at the git level — bypassing agent instructions.

The `commit-msg` git hook removes this trailer before git finalises the commit.

## How it activates

`session-start.sh` runs at every Cursor session start (registered in `hooks.json`).
It runs:

```bash
git config --local core.hooksPath .cursor/hooks/git
```

This tells git to use the versioned hooks directory instead of `.git/hooks/`.
The setting persists in `.git/config` after the first session.

## Manual activation (after cloning without Cursor)

```bash
git config --local core.hooksPath .cursor/hooks/git
```

Run once per clone. No further steps needed.

## Using this submodule in other projects

1. Add as submodule at `.cursor/`:
   ```bash
   git submodule add git@github.com:ivomarvan/cursor-best-practices-template.git .cursor
   ```
2. Open the project in Cursor — `sessionStart` hook activates automatically.
3. Done. All future commits in that project will have the Cursor trailer stripped.
