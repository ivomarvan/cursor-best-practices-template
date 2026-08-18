# .cursor/hooks

Cursor IDE hooks and shared git hooks for projects using this submodule.

## Structure

```
<repo>/
├── hooks.json             → Cursor project hooks (lives at the repository root)
└── hooks/
    ├── session-start.sh   → sessionStart: activates the git commit-msg hook
    ├── git/
    │   └── commit-msg     → strips Cursor agent attribution trailers
    └── README.md          → this file
```

## What it solves

Cursor IDE automatically appends attribution trailers such as
`Co-authored-by: Cursor <cursoragent@cursor.com>` and `Made-with: Cursor` to commit
messages at the git level — bypassing agent instructions.

The `commit-msg` git hook removes those trailers from the **trailer block** (the last
blank-line-separated paragraph): any `-by` / `-with` key whose unfolded value names the
Cursor agent as a prefix — including folded continuation lines and forms git accepts with
spaces around `:` — and any trailer-shaped key carrying `cursoragent@cursor.com`. Prose
before the trailer block is left untouched, so an indented quote of an attribution string
in the body stays. Human co-authors, `Intent:` / `Run:`, and Conventional Commit subjects
are kept. The Cursor prefix is intentional: `CursorAgent` is stripped, and so is a
human-looking `Reported-by: Cursor Smith` or `Reviewed-by: Cursory …`.

The block itself is located in the message **git will actually keep**, not in the raw
file an editor session hands back: a scissors marker and everything after it
(`git commit -v` / `--cleanup=scissors`), a trailing block of `core.commentChar` comment
lines, and the blank runs bordering either are anticipated before the trailer block is
searched for. Without that, a message ending in a blank line, a plain editor commit, or
`-v`'s scissors-and-diff would each hide the real trailer block behind template noise and
let the attribution through.

### Two prices, paid on purpose, not improvements

- Attribution written in the subject line or in body prose, ahead of the trailer block,
  **survives**. Prose before the block is a deliberate, untouched construction — and git
  itself never parses that text as a trailer either, so the history git keeps is not
  misrepresented.
- A legitimate trailer whose *continuation* line alone carries the agent's address is
  **discarded whole**, key included (for example `Intent: i0005` folded with an indented
  `see cursoragent@cursor.com` line disappears entirely). This is the necessary
  consequence of dropping an attribution trailer as one unit: there is no way to keep the
  key while removing only the offending continuation line.

### Known limits, not addressed here

- A comment line shaped like the scissors marker (`core.commentChar` plus `>8`), placed
  *ahead* of the trailer block instead of at the true end of the message, truncates
  everything after it, including legitimate trailers such as `Intent:` / `Run:`. Git
  itself never produces this shape — it only ever writes the marker immediately before a
  diff — so this is a limit on crafted input, not on ordinary use.
- Of the two trailing-blank-run strips in the preflight, the first has no test that
  isolates it: no mutation of it alone turns the suite red.
- If `core.commentChar` in the config that runs this hook does not match the character
  actually used in the file (a hand-written `!` header while the config still says the
  default `#`, or the reverse), the trailing comment block is not recognised as one and
  attribution inside it can survive.
- Prose that follows a trailing comment block, rather than being part of it, is read as
  the message's last paragraph and kept — including any attribution string quoted there.

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
