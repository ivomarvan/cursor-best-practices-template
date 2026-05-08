# Cursor-best-practices-template

A shared Cursor IDE configuration library — curated `.mdc` rules and agent skills
enforcing consistent coding standards across all your projects.

Rules cover: general programming, Git, Docker, Python, Vue.js/Vite/Tailwind,
C/C++ ESP-IDF, and PostgreSQL. Skills cover: Docker setup, Python dev workflow,
PostgreSQL access, and Vue.js dev workflow.

---

## Repository structure

```
cursor-best-practices-template/
├── rules/          # .mdc rule files — Cursor reads these as .cursor/rules/
├── skills/         # Agent skill directories — Cursor reads as .cursor/skills/
├── .cursor/
│   ├── rules  →  ../rules     # symlink — enables rules while editing this repo
│   └── skills →  ../skills    # symlink — enables skills while editing this repo
└── README.md
```

---

## Using this repo in your projects

### Option A — Git submodule (recommended)

The repo root maps directly to `.cursor/`, so Cursor discovers `rules/` and `skills/`
without any extra configuration.

```bash
# In your project root:
git submodule add git@github.com:ivomarvan/cursor-best-practices-template.git .cursor

# Clone a project that already has this submodule:
git clone --recurse-submodules <your-project-url>

# Update the submodule to the latest version of this template:
git submodule update --remote .cursor
git add .cursor
git commit -m "chore(cursor): update shared rules to latest"
```

After adding the submodule, `.cursor/rules/` and `.cursor/skills/` are immediately
available to Cursor.

### Option B — Symbolic links (single machine, no team sharing)

```bash
git clone git@github.com:ivomarvan/cursor-best-practices-template.git ~/dev/cursor-template

# In each project:
ln -s ~/dev/cursor-template/rules  .cursor/rules
ln -s ~/dev/cursor-template/skills .cursor/skills
```

---

## Adding project-specific rules (wrapper pattern)

When a project needs its own rules **in addition to** the shared ones, do not mount
this repo directly at `.cursor/`. Use a wrapper instead:

```bash
# 1. Add the template as a submodule at a named path (not .cursor)
git submodule add git@github.com:ivomarvan/cursor-best-practices-template.git .cursor-shared

# 2. Create your project's .cursor/ with symlinks to shared rules
mkdir -p .cursor/rules .cursor/skills

# Symlink all shared rules
for f in .cursor-shared/rules/*.mdc; do
  ln -s "../../${f}" ".cursor/rules/$(basename $f)"
done

# Symlink all shared skills
for d in .cursor-shared/skills/*/; do
  name=$(basename "$d")
  ln -s "../../.cursor-shared/skills/${name}" ".cursor/skills/${name}"
done

# 3. Add project-specific rules directly into .cursor/rules/
cat > .cursor/rules/20-project-specific.mdc << 'EOF'
---
description: Project-specific conventions for <your-project>.
alwaysApply: true
---
# Project-specific Rules
...
EOF
```

Resulting layout:

```
your-project/
├── .cursor/
│   ├── rules/
│   │   ├── 00-communication-language.mdc  →  ../../.cursor-shared/rules/...  (symlink)
│   │   ├── 10-python.mdc                  →  ../../.cursor-shared/rules/...  (symlink)
│   │   └── 20-project-specific.mdc        ← your own rule, tracked in your repo
│   └── skills/
│       ├── python-dev/                    →  ../../.cursor-shared/skills/...  (symlink)
│       └── my-custom-skill/               ← your own skill, tracked in your repo
├── .cursor-shared/                        ← this template repo as submodule
└── ...
```

To update the shared rules later:

```bash
git submodule update --remote .cursor-shared
# Re-run the symlinking loop if new rule files were added upstream
```

---

## Creating a clone for a different communication language

This repo defaults to **Czech** (`cs`) as the communication language
(see `rules/00-communication-language.mdc`).

To create your own version for a different language (e.g. German):

```bash
# 1. Fork this repo on GitHub, then clone your fork
git clone git@github.com:<you>/cursor-best-practices-template-de.git
cd cursor-best-practices-template-de

# 2. Change the communication language setting
#    Edit rules/00-communication-language.mdc:
#    Replace: | `<communication-language>` | Czech (čeština) |
#    With:    | `<communication-language>` | German (Deutsch) |
#    Replace: | `<lang-code>`              | `cs`             |
#    With:    | `<lang-code>`              | `de`             |

# 3. Update all existing <!-- cs: ... --> comments in every rule and skill
#    to <!-- de: ... --> with translated text.
#    Tip: ask Cursor agent to do this — it understands the bilingual principle
#    from 00-meta-rules-and-skills.mdc and will translate all comments in one pass.

# 4. If lang-code = en: omit translation comments entirely —
#    English text is already the communication language.
```

For an **English-only** version (no translation comments):

```bash
# In rules/00-communication-language.mdc set:
#   <communication-language>  →  English
#   <lang-code>               →  en
#
# Then remove all <!-- cs: ... --> comments from rules/ and skills/.
# Ask the Cursor agent: "Remove all cs comments from all rules and skills."
```

---

## Keeping your fork up to date

```bash
# Add the upstream remote (once):
git remote add upstream git@github.com:ivomarvan/cursor-best-practices-template.git

# Pull upstream improvements into your fork:
git fetch upstream
git merge upstream/main
# Resolve any conflicts (typically in 00-communication-language.mdc
# and translated comments).
```