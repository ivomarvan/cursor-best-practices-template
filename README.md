# Cursor-best-practices-template

A shared Cursor IDE configuration library — curated `.mdc` rules and agent skills
enforcing consistent coding standards across all your projects.

## Agentic Project Management (APM)

This template is built around the idea of managing AI models like a real development team. By organizing AI development into a clearly structured process, the results go beyond mindless code generation.

The workflow is divided into distinct roles:

- 🧠 **Planner (Analyst/Architect)**: Handled by high-context reasoning models (e.g., Sonnet 4.6). The Planner analyzes requirements, breaks them down into Epics and Tasks, prepares precise specifications, sets boundaries (Context Bundles), and defines the Definition of Done.
- 💻 **Coder (Developer)**: Handled by faster, cost-effective models (e.g., Composer 2). The Coder takes the Planner's specifications, implements the code, writes tests, and checks off the DoD requirements.
- 👤 **Human (Tech Lead)**: Has the final say. Conducts code reviews, makes strategic decisions, and ensures no destructive operations happen without explicit approval.

Output quality is enforced by strict repository rules:
- **Strict Boundaries**: Clean Code, SOLID principles, and intent-focused comments.
- **Automated Quality**: Mandatory linting and formatting (Ruff, ESLint) and strict type checking (Mypy, vue-tsc).
- **Test-Driven**: Local testing backed by a CI pipeline.
- **Versioned Reports**: For every completed task, the agent writes a detailed Markdown report detailing files read, changes made, and regression test results, ensuring absolute transparency.

For the full APM workflow documentation, see
[README.project_management.md](README.project_management.md).

---

## Repository structure

```
cursor-best-practices-template/
├── rules/          # .mdc rule files — Cursor reads these as .cursor/rules/
├── skills/         # Agent skill directories — Cursor reads as .cursor/skills/
├── doc/            # Template-level documentation and APM document templates
│   └── project-progress/   # APM templates (brief, spec, roadmap, epics, tasks)
├── .cursor/
│   ├── rules  →  ../rules     # symlink — enables rules while editing this repo
│   └── skills →  ../skills    # symlink — enables skills while editing this repo
├── README.md
└── README.project_management.md   # APM workflow documentation
```

---

## Rules and Skills overview

### Rules (`rules/`)

| File | Topic | Activation |
|------|-------|-----------|
| `00-communication-language.mdc` | Communication language setting (CS/DE/EN) | always |
| `00-meta-rules-and-skills.mdc` | How to write rules and skills | always |
| `01-general-programming.mdc` | OOP, SOLID, clean code, error handling, logging | always |
| `02-git.mdc` | Conventional commits, branching, `.gitignore` | always |
| `03-docker-policy.mdc` | When Docker is mandatory; exemptions | always |
| `04-docker-standards.mdc` | Dockerfile standards, multi-stage builds | `Dockerfile*` |
| `05-new-technology.mdc` | Process for adding new technologies | on request |
| `06-project-structure.mdc` | Universal directory layout, `doc/` structure | always |
| `07-project-management.mdc` | APM workflow, terminology, file headers | `doc/project-progress/**` |
| `10-python.mdc` | Python 3.11+, type hints, docstrings, pytest, ruff | `**/*.py` |
| `11-vuejs-vite-tailwind.mdc` | Vue 3 + Vite + Tailwind CSS, Composition API | `**/*.vue`, `**/*.ts` |
| `12-cpp-esp32.mdc` | C/C++ ESP-IDF, FreeRTOS, RAII, Doxygen | `**/*.c`, `**/*.cpp`, `**/*.h` |
| `13-sql-postgresql.mdc` | SQL conventions, Alembic, psycopg 3, roles | `**/*.sql` |
| `14-fastapi.mdc` | FastAPI, pydantic-settings, dependency injection | `**/router*.py`, `**/main.py` |
| `15-qdrant.mdc` | Qdrant client, collections, search, repository pattern | `**/*.py` |
| `16-sqlalchemy.mdc` | SQLAlchemy 2.x ORM, async sessions, eager loading, Alembic autogenerate | `**/models.py`, `**/session.py` |

### Skills (`skills/`)

| Directory | Skill | Purpose |
|-----------|-------|---------|
| `docker-new-project/` | Docker setup | Scaffold Dockerfile + compose + README.docker.md |
| `docker-debug/` | Docker debug | Diagnose container/compose failures |
| `python-dev/` | Python dev | Docker-based Python development workflow |
| `postgresql-dev/` | PostgreSQL dev | Docker-based PostgreSQL access and migrations |
| `vuejs-dev/` | Vue.js dev | Docker-based Vue.js development workflow |
| `qdrant-dev/` | Qdrant dev | Docker-based Qdrant collection management and testing |
| `sqlalchemy-dev/` | SQLAlchemy dev | Scaffold SQLAlchemy + Alembic, migration workflow, troubleshooting |
| `project-init/` | APM Phase 0 | Formalize brief → `spec.md` + `roadmap.md` |
| `plan-epic/` | APM Phase E | Decompose Epic into Tasks with Context Bundles |
| `execute-task/` | APM Phase T | Implement Task: code + tests + DoD + report |
| `review-epic/` | APM Phase ER | Write Epic Report + review Roadmap validity |

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

## Git Submodule Guide

This section covers everything you need to know about using this template (or any Git submodule) day-to-day.

### Adding the submodule to a project

```bash
# Option A — mount directly as .cursor/ (no project-specific rules needed)
git submodule add git@github.com:ivomarvan/cursor-best-practices-template.git .cursor

# Option B — mount at .cursor-shared/ (use wrapper pattern for project-specific rules)
git submodule add git@github.com:ivomarvan/cursor-best-practices-template.git .cursor-shared
```

After running this command, Git creates a `.gitmodules` file and a committed reference (not the full content) to the submodule. Commit both:

```bash
git add .gitmodules .cursor    # (or .cursor-shared)
git commit -m "chore(cursor): add shared cursor rules as submodule"
```

---

### Cloning a project that has a submodule

```bash
# ✅ Recommended — clone and initialize all submodules in one step
git clone --recurse-submodules git@github.com:<you>/<your-project>.git

# If you already cloned without --recurse-submodules, initialize afterwards:
git submodule update --init --recursive
```

Without `--recurse-submodules`, the `.cursor/` (or `.cursor-shared/`) directory exists but is **empty**.

---

### Updating the submodule to the latest version

The submodule is pinned to a specific commit. To update it to the latest template commit:

```bash
# Pull latest from the submodule's remote and pin the new commit
git submodule update --remote .cursor

# Commit the updated pin in your project
git add .cursor
git commit -m "chore(cursor): update shared rules to latest"
```

To update all submodules at once: `git submodule update --remote --merge`

---

### Making changes inside the submodule

The submodule is a full Git repository inside your project. To contribute a fix or addition to the template:

```bash
# 1. Enter the submodule directory
cd .cursor       # (or .cursor-shared)

# 2. Check out the branch you want to work on
git checkout main
git pull

# 3. Make your changes, then commit inside the submodule
git add rules/15-qdrant.mdc
git commit -m "feat(qdrant): add vector database rule"

# 4. Push the submodule changes to the template repo
git push

# 5. Return to the parent project and update the pinned commit
cd ..
git add .cursor
git commit -m "chore(cursor): update shared rules (added qdrant rule)"
git push
```

> The parent project stores only a **commit SHA** pointing into the submodule repo.
> After you push inside the submodule, you must also update + commit + push the parent.

---

### Checking submodule status

```bash
# Show which commit each submodule is pinned to + whether it has local changes
git submodule status

# Show submodule details in git status
git status   # submodule shows as "modified" when its pinned SHA changed

# Show the full diff of which commit the submodule moved to
git diff --submodule
```

---

### Pulling a project when the submodule was updated upstream

When a teammate updated the pinned submodule commit and pushed, your local clone will show the submodule as "modified". Sync it:

```bash
git pull
git submodule update --init --recursive
```

Add this to CI pipelines and onboarding scripts to ensure submodules are always initialized.

---

### Removing a submodule

```bash
# 1. Remove the entry from .gitmodules
git submodule deinit -f .cursor

# 2. Remove from Git's index
git rm -f .cursor

# 3. Clean up the internal Git state
rm -rf .git/modules/.cursor

# 4. Commit the removal
git commit -m "chore: remove cursor submodule"
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