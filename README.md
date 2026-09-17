# cursor-best-practices-template

A reusable **Cursor IDE configuration** for people who build software with AI agents and
want the result to look like it was written by one disciplined team — not by whichever
model happened to be in the chat window.

It ships three things:

1. **Rules** — coding standards the agent follows automatically (Git conventions, Docker
   policy, Python/Vue/C++ style, security against prompt injection, …).
2. **Skills and commands** — step-by-step procedures the agent executes on request
   (set up Docker, run the Python quality gate, plan an epic, review a task, commit).
3. **APM — Agentic Project Management** — a lightweight workflow in which a *Planner*
   agent plans, a *Coder* agent implements, an independent *Reviewer* agent checks the
   work, and **you** decide only where it matters.

Everything is installed into a project with one command and upgraded with the same
command. Your own configuration and project-specific rules survive every upgrade.

![](img/cursor-best-practices-template.jpg)

> 🇨🇿 Czech readers: [`README.cs.md`](README.cs.md) is a plain-language guide to the
> whole methodology. The APM workflow in detail is in
> [`README.project_management.md`](README.project_management.md).

---

## Table of contents

- [Vocabulary](#vocabulary)
- [Quick start](#quick-start)
- [What gets installed](#what-gets-installed)
- [Rules](#rules) · [Skills](#skills) · [Commands](#commands) · [Hooks](#hooks)
- [Configuration: template defaults vs. project overrides](#configuration-template-defaults-vs-project-overrides)
- [Adding project-specific rules and skills](#adding-project-specific-rules-and-skills)
- [APM in five minutes](#apm-in-five-minutes)
- [Git: what the agent never does on its own](#git-what-the-agent-never-does-on-its-own)
- [Keeping a project up to date](#keeping-a-project-up-to-date)
- [Other installation methods](#other-installation-methods)
- [Repository structure](#repository-structure)
- [Developing the template](#developing-the-template)

---

## Vocabulary

The rest of this document uses these terms. Cursor-specific ones first, then ours.

| Term | Meaning |
|---|---|
| **Rule** (`.cursor/rules/*.mdc`) | A Markdown file with YAML front matter that Cursor injects into the agent's context. Three activation modes: `alwaysApply: true` (every call — expensive, keep short), `globs:` (only when a matching file is in context, e.g. `**/*.py`), or *description-only* (the agent pulls it in when the description fits the task). |
| **Skill** (`.cursor/skills/<name>/SKILL.md`) | A procedure with numbered steps and exact commands. The agent picks it by matching your request against the skill's `description`; you can also name it explicitly ("follow the `execute-task` skill"). |
| **Command** (`.cursor/commands/<name>.md`) | A slash command typed in chat: `/push`, `/role-show`. Same file format as a skill, triggered by name. |
| **Hook** (`.cursor/hooks.json`) | A script Cursor runs on an event. We use `sessionStart` to activate a git `commit-msg` hook that strips Cursor's `Co-authored-by` trailer. |
| **Subagent** | A separate agent the main chat spawns for one bounded job, with its own fresh context and — importantly — its own **model**. APM runs the Coder and the Reviewer this way. |
| **APM** | *Agentic Project Management* — our workflow: Planner → Coder → Reviewer → Human, organised into Epics and Tasks. Details in [`README.project_management.md`](README.project_management.md). |
| **Planner / Coder / Reviewer / Human** | The four APM roles. Planner (strong model) plans and decomposes; Coder (cheaper model) implements; Reviewer (strong model, *different from the Coder*) checks the diff against the spec; Human decides. |
| **Epic, Task** | An Epic is a deliverable-sized chunk of the roadmap (6–8 Tasks). A Task is half a day to two days of Coder work, independently implementable and testable. |
| **Band** | A Task's risk class — `low`, `medium`, `high` — decided upfront from deterministic triggers (schema change, deletion, untrusted input, …), never by feel. The band chooses the model tier *and* how much human review the Task gets. |
| **Human gate** | A point where the agent stops and waits for your decision. Opened for every `high`-band Task, for each Epic plan, and for each Roadmap review — not after every Task. |
| **Deterministic gate** | The mechanical quality check that does not involve an LLM: `make check` = linter + formatter + strict types + tests. The Coder, the Reviewer and CI all run the same command, so "passes" means the same thing everywhere. Shipped for Python. |
| **DoR / DoD** | *Definition of Ready* — checklist a Task spec must pass before a Coder may start. *Definition of Done* — checklist the Coder fills and the Reviewer verifies against real artifacts. |
| **SoT, `DECISIONS.md`** | *Source of Truth* — the document(s) that bind the project (`spec.md` by default). `DECISIONS.md` is a short append-only register of settled questions that every phase checks first, so the agent never silently contradicts an earlier decision. |
| **Config Resolution** | How three settings (`AGENT_MODELS`, `DESIGN_RULES`, `LANGUAGE`) work: a template default in `.cursor/apm_config/<NAME>.default.md`, optionally replaced *in full* by your `doc/apm_config/<NAME>.user.md`. |
| **`TEMPLATE_MANIFEST`, `TEMPLATE_VERSION`** | Two files the installer writes into `.cursor/`. The manifest lists every file the template owns (only those are rewritten on upgrade); the version marker records which template revision is installed. |

---

## Quick start

Requirements: Python 3.10+ (standard library only), git, Cursor.

```bash
# 1. Clone the template once, anywhere on disk — it stays separate from your projects
git clone git@github.com:ivomarvan/cursor-best-practices-template.git ~/dev/cursor-best-practices-template

# 2. Install into a project (English chat) …
python3 ~/dev/cursor-best-practices-template/scripts/install_into_project.py ~/dev/my-project

#    … or with Czech as the language the agent talks to you in
python3 ~/dev/cursor-best-practices-template/scripts/install_into_project.py ~/dev/my-project --lang cs

# 3. Verify (read-only; exit code 1 if anything is off)
python3 ~/dev/cursor-best-practices-template/scripts/check_installation.py ~/dev/my-project
```

Then open the project in Cursor. The `sessionStart` hook activates the git hook; the
rules are live immediately. Two things to do in the first chat:

```text
/role-show                       # see which model each APM role uses — all "unassigned" at first
/role-assign Planner high <model>  # …assign them (or answer when the agent asks)
```

Commit `.cursor/` and `doc/apm_config/` to your project's repository — they are part of
the project, and teammates get the same agent behaviour after `git pull`.

---

## What gets installed

```
my-project/
├── .cursor/                         ← template-owned files + your own additions
│   ├── rules/        *.mdc          ← coding standards (template) + 9xx-*.mdc (yours)
│   ├── skills/       <name>/SKILL.md
│   ├── commands/     push.md, role-assign.md, role-show.md
│   ├── hooks/        session-start.sh, git/commit-msg
│   ├── hooks.json
│   ├── apm_config/   AGENT_MODELS.default.md, DESIGN_RULES.default.md, LANGUAGE.default.md
│   ├── TEMPLATE_MANIFEST            ← list of template-owned files (generated, never edit)
│   └── TEMPLATE_VERSION             ← installed template revision + timestamp
└── doc/apm_config/                  ← YOUR configuration — created once, never overwritten
    ├── AGENT_MODELS.user.md         ← which model runs which role × band
    ├── DESIGN_RULES.user.md         ← binding project invariants, forbidden tech, Docker exemptions
    └── LANGUAGE.user.md             ← chat language (seeded from --lang)
```

The installer strips the template's bilingual maintainer comments (`<!-- cs: … -->`) on
the way, so the copy is roughly half the token size of the source. The template's own
`scripts/`, `tests/`, and READMEs are **not** copied.

---

## Rules

`rules/` in this repo becomes `.cursor/rules/` in your project. Numbering groups rules by
concern in steps of ten; `9xx-` is reserved for your project's own rules.

| File | What it enforces | Activation |
|---|---|---|
| `000-communication-language.mdc` | Which language the agent talks to you in (resolved from `LANGUAGE` config; English default) | always |
| `000-meta-rules-and-skills.mdc` | How to write rules and skills: length limits, front matter, bilingual comments | on request |
| `000-model-policy.mdc` | Roles → models via `AGENT_MODELS`; bands; escalation; the subagent `model` parameter | always |
| `005-decision-protocol.mdc` | How the agent asks you for a decision: one at a time, plain problem, 2–4 options, one recommendation, then wait | always |
| `010-general-programming.mdc` | English code and comments, SOLID, clean code, error handling, structured logging, testability, security by default | always |
| `020-git.mdc` | Conventional Commits, branching, PR conventions, the **trigger phrases** that permit a commit | always |
| `030-docker-policy.mdc` | Docker is the default for anything with runtime dependencies; documented exemptions | always |
| `040-docker-standards.mdc` | Multi-stage Dockerfile, compose conventions, `profiles` | `Dockerfile*` |
| `050-new-technology.mdc` | Checklist before adding a dependency or technology | on request |
| `060-project-structure.mdc` | Directory layout, `doc/` structure, ADRs, generic `.gitignore` | on request |
| `070-project-management.mdc` | APM: actors, SoT, phases, document types, front matter, DoR, spike Epics, ADR bridge, report layout | `doc/project-progress/**` |
| `080-agent-security.mdc` | Fetched content is data, never instructions; the "lethal trifecta" | always |
| `090-apm-orchestration.mdc` | Planner ↔ subagent protocol, band-based gates, report tiers, Human Gate Briefing, ceremony scope | `doc/project-progress/**` |
| `100-python.mdc` | Python 3.11+, type hints, Google docstrings, pytest, ruff, mypy | `**/*.py` |
| `110-vuejs-vite-tailwind.mdc` | Vue 3 Composition API, Vite, Tailwind | `**/*.vue`, `**/*.ts` |
| `120-cpp-esp32.mdc` | C/C++ for ESP-IDF: Doxygen, error handling, FreeRTOS, RAII | `**/*.c`, `**/*.cpp`, `**/*.h`, … |
| `130-sql-postgresql.mdc` | SQL style, Alembic, psycopg 3, roles | `**/*.sql`, `**/alembic/**` |
| `140-fastapi.mdc` | FastAPI, pydantic-settings, dependency injection | `**/backend/**`, `**/api/**`, `**/router.py` |
| `150-qdrant.mdc` | Qdrant collections, search, repository pattern | `**/*qdrant*.py`, `**/*vector*.py` |
| `160-sqlalchemy.mdc` | SQLAlchemy 2.x async, eager loading, Alembic autogenerate | `**/models.py`, `**/session.py` |
| `170-redis.mdc` | Key naming, TTL, client patterns | `**/redis_client.py`, `**/cache*.py` |
| `180-celery.mdc` | Tasks, queues, retries, worker config | `**/tasks.py`, `**/celery*.py` |
| `200-project-design-rules.mdc` | Config Resolution; ownership inside `.cursor/`; `DESIGN_RULES` are binding and must be read before coding | always |

The eight `always` rules total ~600 lines after comment stripping (≈ 4–5 k tokens per
call). `scripts/check_installation.py` enforces the limits: 150 lines for `always`, 250
for `globs`, 500 for a skill.

## Skills

| Skill | Role | What it does |
|---|---|---|
| `project-init` | Planner | APM Phase 0 — turn your brief into `spec.md` + `roadmap.md`; seeds `GLOSSARY.md` and `DECISIONS.md` |
| `plan-epic` | Planner | APM Phase E — decompose an Epic into 6–8 Tasks with Context Bundles; DoR gate |
| `execute-task` | Coder | APM Phase T — implement, test, run `make check`, fill DoD, write the report |
| `review-task` | Reviewer | APM Phase R — independent review of the diff vs. spec/DoD → `review.md` verdict |
| `review-epic` | Coder + Planner | APM Phase ER — Epic Report; Roadmap validity review with you |
| `commit-task` | any | Phrase-triggered commit workflow: direct, with CI, feature branch, feature + CI + squash |
| `python-dev` | any | Run scripts/tests/ruff/mypy in Docker; set up the `make check` gate and CI |
| `docker-new-project`, `docker-debug` | any | Scaffold Dockerfile/compose/`README.docker.md`; diagnose container problems |
| `postgresql-dev`, `sqlalchemy-dev`, `qdrant-dev`, `vuejs-dev` | any | Day-to-day workflows for those stacks |

> **Deterministic gate coverage.** `skills/python-dev/templates/` ships a `Makefile`
> (`make check` = `ruff check` + `ruff format --check` + `mypy --strict` + `pytest`) and a
> GitHub Actions `ci.yml`. `make check RUNNER=` runs it natively for Docker-exempt
> projects and spikes. C++/ESP32 and Vue/Vite do not have an equivalent target yet.

## Commands

| Command | What happens |
|---|---|
| `/push` | Runs the deterministic gate (`make check`; fallback `scripts/run_all_tests.sh`). Green → stage, commit (Conventional Commits), push to `master`. Red → stops, no git operations. This *is* your explicit consent under `020-git.mdc`. |
| `/role-assign [role] [band] [model]` | Writes a model into the role × band table in `doc/apm_config/AGENT_MODELS.user.md`; asks for whatever is missing. |
| `/role-show` | Prints the current role × band → model table and reminds you how models are delivered (chat selector vs. subagent parameter). |

## Hooks

`hooks.json` registers `hooks/session-start.sh` for `sessionStart`. It sets
`core.hooksPath = .cursor/hooks/git` **only if unset**, so the versioned `commit-msg` hook
runs on every commit and removes Cursor's `Co-authored-by: Cursor` trailer. If you already
use another hooks directory (husky, pre-commit), the script prints how to chain the two
instead of overriding yours. Details: [`hooks/README.md`](hooks/README.md).

---

## Configuration: template defaults vs. project overrides

Three settings follow one mechanism (`rules/200-project-design-rules.mdc`):

| Setting | Controls | Default (`.cursor/apm_config/`) | Your override (`doc/apm_config/`) |
|---|---|---|---|
| `LANGUAGE` | The language the agent uses in chat and in APM reports | English | `LANGUAGE.user.md` — seeded by `--lang`, edit by hand any time |
| `AGENT_MODELS` | Which model runs each role × band; project-specific `high` triggers | all `unassigned` (agent asks) | `AGENT_MODELS.user.md` — via `/role-assign` or by hand |
| `DESIGN_RULES` | Binding project invariants: forbidden technologies, Docker exemptions, SoT list, anything that must beat a general rule | empty skeleton | `DESIGN_RULES.user.md` — by hand |

If `<NAME>.user.md` exists it **replaces the default in full** (whole file, no per-field
merge). The installer creates the `.user.md` files once and never touches them again.

**Models.** Roles are not bound to model names — models and prices change. The default
table has Reviewer `low` = `—` (the deterministic gate is the review for mechanical
changes) and Planner `low` = `—` (Planner is banded per Epic). Any cell left `unassigned`
makes the agent ask before acting in that role/band. Cursor does not switch the main chat
window's model for you — the agent reminds you to; subagents (Coder, Reviewer) receive the
model as a call parameter automatically.

---

## Adding project-specific rules and skills

Project-owned content lives *next to* the template files inside `.cursor/` and survives
every upgrade, because the installer removes only what `.cursor/TEMPLATE_MANIFEST` lists.

| What | Where | Convention |
|---|---|---|
| Project rule | `.cursor/rules/9xx-<slug>.mdc` | `9xx-` is reserved for projects; template numbering stops at `2xx` |
| Project skill | `.cursor/skills/<name>/SKILL.md` | any name the template does not use |
| Project command | `.cursor/commands/<name>.md` | any name the template does not use |
| Configuration | `doc/apm_config/<NAME>.user.md` | full-file replacement of the default |
| Binding invariants, forbidden tech, Docker exemptions | `doc/apm_config/DESIGN_RULES.user.md` | takes precedence over template rules |

```markdown
<!-- .cursor/rules/900-domain-conventions.mdc -->
---
description: Domain conventions for <your-project> — apply when touching src/domain/.
globs: "src/domain/**"
alwaysApply: false
---
# Domain conventions
...
```

A project rule may **narrow or extend** a template rule. To **override** one, state it in
`DESIGN_RULES.user.md` — that file has precedence; a competing `.mdc` alone would leave
the agent with two contradicting instructions. Never edit a file listed in
`TEMPLATE_MANIFEST`; the next upgrade silently reverts it. `check_installation.py` reports
your files as *project-owned (kept)* and warns about a rule outside `9xx-` that the
manifest does not know (a likely orphan from an older version).

---

## APM in five minutes

```
You write a brief (informal, any length)
   ↓  Phase 0 — project-init (Planner)
spec.md + roadmap.md                                        [you approve]
   ↓  Phase E — plan-epic (Planner)          per Epic
epic-NNN/plan.md + task-NNN/spec.md + dod.md  [DoR gate]    [you approve the plan]
   ↓  Phase T — execute-task (Coder, subagent)       per Task
code + tests + make check + report.md
   ↓  Phase R — review-task (Reviewer, subagent, different model)
review.md: APPROVE / REQUEST CHANGES  (≤ 3 rounds; 2nd REQUEST CHANGES raises the band)
   ↓                                                        [you see only high-band Tasks]
   ↓  Phase ER — review-epic (Coder + Planner)
epic report (every Task incl. band, review rounds, BLOCKED count) + roadmap check  [you decide]
```

What makes it cheap enough for a solo developer:

- **Bands scale the ceremony.** `low` Tasks get a five-line report and the deterministic
  gate as their review; `medium` a short report and an LLM review; `high` a full report,
  an LLM review, *and* your gate. You see `medium`/`low` Tasks in the Epic Report table.
- **Subagents keep the audit trail honest.** The Planner runs in your chat; it spawns the
  Coder and the Reviewer as subagents with the model from `AGENT_MODELS`. A subagent
  returns exactly `DONE: <path>` or `BLOCKED: <one question>` — the Planner reads the
  file, never the subagent's own summary.
- **Every gate opens with a briefing**, not a raw report: where we are, what changed,
  *one* decision needed with a recommendation, what happens if you do nothing.
- **Decisions are asked one at a time** (`005-decision-protocol.mdc`) and recorded in
  `DECISIONS.md` so they are never silently contradicted later.
- **Outside an Epic is fine.** Typos, docs, config tweaks you ask for directly are not
  Tasks — no spec, no report, no Reviewer.

Full walkthrough, document formats, checklists: [`README.project_management.md`](README.project_management.md).

---

## Git: what the agent never does on its own

`020-git.mdc` forbids `commit`, `push`, `pull`, `merge`, `rebase`, `reset`, and force
pushes without your explicit consent. Consent is one of these — nothing else counts:

| You write (CS / EN) | Result |
|---|---|
| `… s commitem` / `… with commit` | commit on `master` |
| `… s commitem s CI` / `… with commit and CI` | commit on `master`, watch CI, fix up to 3× |
| `… s commitem do feature` / `… with feature commit` | new `feature/eNNN-tNNN-slug` branch |
| `… s commitem do feature s CI` / `… with feature commit and CI` | feature branch + CI + squash merge |
| `/push` | gate → commit → push to `master` |

Before any commit the `commit-task` skill requires the Reviewer's APPROVE (or the gate for
`low`), runs `make check` locally, and refuses to stage `.env`, keys, or `nogit_data/`.
After each APPROVE the Planner *offers* a commit in one line; if you decline, the Reviewer
of the next Task scopes its diff to that Task's declared outputs and says so.

---

## Keeping a project up to date

```bash
cd ~/dev/cursor-best-practices-template && git pull
python3 scripts/install_into_project.py ~/dev/my-project     # rewrites template-owned files only
python3 scripts/check_installation.py  ~/dev/my-project      # read-only audit
cat ~/dev/my-project/.cursor/TEMPLATE_VERSION                 # what is installed now
```

`check_installation.py` verifies placement, the manifest, the three default configs,
absence of leaked `cs:` comments, rule length limits, and front matter sanity. A project
whose `TEMPLATE_VERSION` lags behind runs with rules that no longer match the skills they
were written against — upgrade first, then start work. What changed between versions:
[`CHANGELOG.md`](CHANGELOG.md).

---

## Other installation methods

**Option C (the copy installer above) is recommended.** Two older methods remain
supported for cases where `.cursor/` must be a live git dependency:

<details>
<summary><b>Option A — git submodule at <code>.cursor/</code></b></summary>

```bash
git submodule add git@github.com:ivomarvan/cursor-best-practices-template.git .cursor
git clone --recurse-submodules <your-project-url>          # cloning such a project
git submodule update --remote .cursor && git add .cursor    # upgrading the pin
```

Trade-offs: no comment stripping (≈ twice the tokens per call), no `TEMPLATE_MANIFEST`
(so no safe place for project rules inside `.cursor/`), submodule mechanics
(`.gitmodules`, detached HEAD). For project-specific rules mount the submodule at
`.cursor-shared/` and symlink its `rules/*.mdc` and `skills/*/` into `.cursor/`, then add
your `9xx-*.mdc` next to the links.

Removing a submodule: `git submodule deinit -f .cursor && git rm -f .cursor && rm -rf .git/modules/.cursor`.

</details>

<details>
<summary><b>Option B — symbolic links (single machine)</b></summary>

```bash
git clone git@github.com:ivomarvan/cursor-best-practices-template.git ~/dev/cursor-template
ln -s ~/dev/cursor-template/rules  .cursor/rules
ln -s ~/dev/cursor-template/skills .cursor/skills
```

Not shareable with a team; same token cost as Option A.

</details>

<details>
<summary><b>Migrating from A/B to C</b></summary>

```bash
python3 scripts/migrate_submodule_to_copy.py ~/dev/my-project --lang cs
```

Copies legacy `DESIGN_RULES.md` / `doc/AGENT_MODELS.md` content into
`doc/apm_config/*.user.md`, then regenerates `.cursor/`. It **prints** (does not run) the
`git rm` for the legacy files and the submodule deregistration commands, and ends with a
final `install_into_project.py` re-run — `git submodule deinit` empties `.cursor/` again,
so that last command is not optional.

</details>

---

## Repository structure

```
cursor-best-practices-template/
├── rules/                  # .mdc rules → installed as .cursor/rules/
├── skills/                 # skills → .cursor/skills/ (python-dev/templates/ has Makefile + ci.yml)
├── commands/               # /push, /role-assign, /role-show → .cursor/commands/
├── hooks/, hooks.json      # sessionStart hook + git commit-msg hook
├── apm_config/             # *.default.md for AGENT_MODELS, DESIGN_RULES, LANGUAGE
├── scripts/                # install_into_project.py, check_installation.py,
│                           # migrate_submodule_to_copy.py, lib/  (never copied)
├── tests/                  # pytest suite for scripts/ (never copied)
├── doc/
│   ├── DECISIONS.md        # settled design questions about the template itself
│   ├── KNOWN_LIMITATIONS.md# reviewed, deliberately not fixed — with reasons
│   ├── guides/             # e.g. agentic-engineering-resources.md
│   └── project-progress/   # example APM documents (brief, spec, roadmap, epic, task)
├── Makefile, pyproject.toml, .github/workflows/ci.yml   # the template's own gate
├── README.md · README.cs.md · README.project_management.md · CHANGELOG.md
```

Source files carry bilingual maintainer comments (`<!-- cs: … -->`); English is the
sole source of truth and the comments are stripped on install.

---

## Developing the template

```bash
pip install ruff mypy pytest      # once
make check                        # ruff + ruff format --check + mypy --strict + pytest
make audit P=~/dev/my-project     # check_installation.py on an installed project
```

`pytest` installs the real `rules/` and `skills/` into a temporary project and runs
`check_installation.py` on the result, so a rule over its line limit, a leaked `cs:`
comment, or broken front matter fails here — not in someone's chat session.
`.github/workflows/ci.yml` runs the same target on every push and pull request.

- Settled design questions: [`doc/DECISIONS.md`](doc/DECISIONS.md)
- Deliberately unfixed findings, with reasons: [`doc/KNOWN_LIMITATIONS.md`](doc/KNOWN_LIMITATIONS.md)
- Writing rules and skills: `rules/000-meta-rules-and-skills.mdc`
- Keeping a fork current: `git remote add upstream <this repo>; git fetch upstream; git merge upstream/master`
