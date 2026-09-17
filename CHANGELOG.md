# Changelog

All notable changes to `cursor-best-practices-template` are documented in this file.

## v1.2.0

### Added

- **Manifest-based ownership inside `.cursor/`** (`.cursor/TEMPLATE_MANIFEST`): the
  installer records every file it writes and on re-install removes/rewrites exactly
  those. Project-owned rules (`rules/9xx-<slug>.mdc` — reserved namespace), own skills
  and commands, and Cursor's `mcp.json` survive. Pre-manifest installs fall back to
  removing only the current template's paths. `check_installation.py` verifies the
  manifest, reports project-owned files as kept, and flags a rule outside `9xx-` that is
  not in the manifest as a probable orphan. `200-project-design-rules.mdc` § Ownership,
  `000-meta` file naming, and README § *Adding project-specific rules and skills*
  (replaces the submodule-only wrapper pattern as the primary guidance) document it.
- **`rules/005-decision-protocol.mdc`** (`alwaysApply`): how any role asks the Human for a
  decision — one decision per message, plain-language problem, 2–4 options with
  consequences, one recommendation marked *(Recommended)*, then wait. Referenced from the
  Human Gate Briefing (`090` § C) and from `project-init` Step 2.
- **Template's own deterministic gate**: `Makefile` (`make check` = ruff + ruff format
  --check + mypy --strict + pytest), `pyproject.toml`, `tests/` (strip_comments unit tests;
  install into a temp project and run `check_installation.py` on it), and
  `.github/workflows/ci.yml`. A rule over its line limit or a leaked `cs:` comment now
  fails CI here, not in a consuming project.
- **`doc/DECISIONS.md`**: append-only register of settled template design questions.
- **Installer copies `apm_config/*.default.md` to `.cursor/apm_config/`**, so the
  resolution rule in `200-project-design-rules.mdc` is literally true inside the project.
  `check_installation.py` verifies the three default files.
- **`090` § E — Scope of the ceremony**: 6–8 Task cap moved here from § D; explicit
  statement that changes outside an Epic (typos, docs, config) need no APM ceremony.
- **Epic Report**: `Kola revize` (REQUEST CHANGES count) and `BLOCKED` columns as the
  cheap DoR-quality signal (`review-epic`, example `report.md`).
- **`project-init`**: Step 2 is skipped when the brief already has a decisions register
  and no open questions; Step 3 gains § 7 *Source of Truth* and the rule to move detailed
  brief sections verbatim to `doc/architecture/` instead of compressing them.
- **`README.cs.md`**: plain-language Czech guide — what the template is, vocabulary,
  installation, APM day-to-day, git trigger phrases, project rules, FAQ, file map.
- **README.md and README.project_management.md rewritten** against the current state:
  vocabulary sections, quick start, manifest-based ownership, bands/gates/subagent
  protocol, decision protocol, SoT + `DECISIONS.md`, spike Epics, upgrade routine,
  *Developing the template*; submodule/symlink guides collapsed into details blocks.

### Changed

- **Reviewer `low` = `—`** in `AGENT_MODELS.default.md` (was `unassigned`, which made
  every `low` Task stop to ask the Human). `000-model-policy.mdc` defines `—` (step 4)
  and splits step 2 into parent-window (remind Human) vs. subagent (pass `model`
  parameter) delivery.
- **`090` § A / `review-task`**: the Reviewer reads `report.md` last (integrity check),
  the Planner's prompt never paraphrases it; dirty working tree → path-scoped diff over
  `spec.md` Outputs, stated in `review.md`; after APPROVE the Planner *offers* a commit
  (Human answers with a trigger phrase) — never commits on its own.
- **`commit-task`**: new *Before Every Commit* block — Reviewer APPROVE (or gate for
  `low`), `make check` locally, secret guard after `git add -A`.
- **`/push`** runs `make check` (fallback `scripts/run_all_tests.sh`); documented as the
  slash-command form of the consent `020-git.mdc` requires.
- **`030-docker-policy.mdc`**: Docker exemptions are recorded in the project's
  `DESIGN_RULES.user.md`, never by editing the rule inside `.cursor/`; `profiles` YAML
  example moved to `040-docker-standards.mdc`.
- **Context slimming of `alwaysApply` rules**: generic `.gitignore` block moved from
  `020-git.mdc` to `060-project-structure.mdc`; read-only git command list removed;
  bilingual-comment convention referenced from `000-communication-language.mdc` instead
  of duplicated (canonical copy in `000-meta-rules-and-skills.mdc`). `120-cpp-esp32.mdc`
  trimmed under the 250-line `globs` limit (installed form).
- **`000-meta-rules-and-skills.mdc`**: line limits are measured on the installed
  (comment-stripped) form.
- **`hooks/session-start.sh`** sets `core.hooksPath` only when unset; an existing
  different value is respected and a chaining hint printed. `hooks/README.md` updated for
  Option C.
- **`skills/python-dev/templates/Makefile`**: `RUNNER` and `MYPY_PATHS` variables —
  `make check RUNNER=` runs the gate natively for Docker-exempt projects and spikes.
- Report tier row says 7 sections (matches `070`); example APM docs carry
  `template_version`; `README.md` fork guide merges `upstream/master`.

### Fixed

- `check_installation.py`: `apm_config/` is expected under `.cursor/` (was listed as a
  violation); `tests/` added to the never-copied set; mypy `--strict` clean.
- Stale reference to `communication-language.mdc` in `000-meta-rules-and-skills.mdc`.

## v1.1.0

### Added

- **Config Resolution mechanism** (`rules/200-project-design-rules.mdc`): a single,
  generic default-vs-override pattern now backs three settings — `AGENT_MODELS`,
  `DESIGN_RULES`, `LANGUAGE`. Template defaults ship in `apm_config/<NAME>.default.md`;
  a consuming project overrides a setting **in full** by creating
  `doc/apm_config/<NAME>.user.md`. This replaces the previous single-purpose mechanism
  that only covered `DESIGN_RULES.md` at the project root.
- **`apm_config/` directory**: `AGENT_MODELS.default.md` (the former *Active Role
  Assignments* table, moved out of `rules/000-model-policy.mdc`), `DESIGN_RULES.default.md`
  (empty skeleton), `LANGUAGE.default.md` (English — the former active-settings table,
  moved out of `rules/000-communication-language.mdc`).
- **`scripts/install_into_project.py`**: Python 3, `argparse`-based CLI (standard
  `-h`/`--help`, error messages) that installs this template into a consuming project
  as a plain, filtered copy — a non-submodule alternative ("Option C" in `README.md`).
  Strips bilingual `cs:` comments on copy, writes a `.cursor/TEMPLATE_VERSION` marker,
  seeds `doc/apm_config/*.user.md` (create-if-missing — never overwrites existing project
  configuration on re-install), and supports a `--lang <code>` parameter and a
  `--config-layout <version>` parameter for legacy path compatibility.
- **`scripts/migrate_submodule_to_copy.py`**: Python 3, `argparse`-based CLI that
  migrates a submodule-based project to the copy-based method, preserving existing
  `DESIGN_RULES.md` / `doc/AGENT_MODELS.md` / locally-modified language settings by
  copying them into `doc/apm_config/*.user.md` before regenerating `.cursor/`. Prints
  (does not run) a `git rm` recommendation for the now-redundant legacy files and the
  git commands needed to deregister the submodule.
- **`scripts/lib/`**: shared Python library backing both CLIs — `installer.py`
  (`TemplateInstaller` — copy/filter/seed logic), `migration.py` (submodule-to-copy
  helpers), and `strip_comments.py`, which removes `<!-- cs: ... -->` and `# cs: ...`
  bilingual annotation comments from copied files without touching example text that
  merely documents the comment syntax (e.g. in `rules/000-meta-rules-and-skills.mdc`).
- **`CHANGELOG.md`** (this file).
- **`rules/090-apm-orchestration.mdc`**: Planner ↔ subagent protocol, a band-based Human
  gate policy (`high` gates every Task, `medium`/`low` surface only in the Epic Report),
  matching report tiers (full / short / micro), the **Human Gate Briefing** format
  (where we are · what changed · decision needed · consequence of inaction), a 6–8 Task
  cap per Epic, and a parent-window implementation exception for `low`-band Tasks. This
  replaces the "Human gate after every Task" ceremony with a gate cost proportional to
  the Task's band.
- **Bands** (`rules/000-model-policy.mdc`): the `low`/`medium`/`high` Task-difficulty
  concept — generic hard triggers for `high`, per-role granularity (Planner/Epic,
  Coder+Reviewer/Task), and the deterministic escalation table (second `REQUEST CHANGES`
  raises the band; `high` + second `REQUEST CHANGES` escalates to Human; only Human may
  lower a band) — is now a template mechanism, not something each project reinvents.
  `AGENT_MODELS.default.md` ships a role × band assignment table (replacing the old flat
  role-only table) plus a place for a project's own additional `high` triggers.
  `AGENT_MODELS.user.md` may leave `Reviewer`/`low` unassigned if the deterministic gate
  already covers it — the template now says so explicitly.
- **`doc/project-progress/DECISIONS.md`** (`skills/project-init/templates/DECISIONS.md`):
  a short, append-only decisions register — one row per already-settled question — that
  is the fast target the **Source of Truth** conflict check
  (`rules/070-project-management.mdc`) diffs a new chat instruction against, instead of
  re-reading the full `spec.md`/`roadmap.md`/`DESIGN_RULES.user.md` tree on every Phase.
  Seeded by `project-init` alongside `GLOSSARY.md`.
- **Epic type: spike** (`rules/070-project-management.mdc`): a formalized shell for
  exploratory/experiment work — `spike/<desc>` branch (`rules/020-git.mdc`), a DoR naming
  metrics/dataset/candidates instead of a feature Goal, a results-table + ADR as DoD, and
  a Reviewer who checks reproducibility, not code quality. Stopping a spike is explicitly
  a **Human decision made with the Planner**, never an automatic threshold. A matching
  Docker-policy exception (`rules/030-docker-policy.mdc`) lets spike code skip the
  mandatory `README.docker.md`/pinned-version ceremony until promoted to production.
- **Deterministic gate — Python** (`skills/python-dev/templates/Makefile`, `ci.yml`): a
  `make check` target (`ruff` + `mypy --strict` + `pytest`) that the Coder, the Reviewer,
  and CI all run identically, wired into `skills/execute-task/SKILL.md` and
  `skills/review-task/SKILL.md`. Python-only for now — `README.md` and
  `skills/python-dev/SKILL.md` flag that C++/ESP32 and Vue/Vite need their own equivalent
  target as future template work (see `doc/KNOWN_LIMITATIONS.md` §C).
- **Subagent completion protocol** (`rules/090-apm-orchestration.mdc` §A): a Coder/
  Reviewer subagent's final message to the Planner is exactly `DONE: <path>` or
  `BLOCKED: <one question>` — no code, no prose summary — plus a standard handoff
  sentence for resuming Planner work in a fresh chat window after the previous one fills up.
- **`template_version` front-matter field** (`rules/070-project-management.mdc` and every
  skill's document template): records the `.cursor/TEMPLATE_VERSION` value active when an
  APM document was first created, for later audits of which template revision a Task's
  conventions came from. Omitted only for `brief.md` (Human input).
- **`check_installation.py`**: two new checks — every `rules/*.mdc` must declare
  `alwaysApply` in its frontmatter, and `alwaysApply: true` combined with a non-empty
  `globs` is now a reported `VIOLATION` (dead configuration — `globs` has no effect once
  `alwaysApply` is true). A heuristic dead-link checker was considered and deliberately
  **not** added — see the module docstring for why.
- **`doc/KNOWN_LIMITATIONS.md`**: five review findings that were considered and
  deliberately **not** fixed at the template level (checkpoint-per-Task commits
  conflicting with the Human's own git-control rule; symlink double-loading needs live
  Cursor introspection this agent lacks; per-stack deterministic gates beyond Python;
  real piloting of the new mechanisms; agent self-reported token accounting) — each with
  why, what was done instead, and the condition to revisit it.

### Changed

- `rules/000-model-policy.mdc`: the *Active Role Assignments* table is no longer stored
  in this rule file — it is resolved from **AGENT_MODELS config** (see Config Resolution
  above). The `unassigned` → ask-the-Human behavior is unchanged, only its storage
  location moved.
- `rules/000-communication-language.mdc`: the active-language table is no longer stored
  in this rule file — it is resolved from **LANGUAGE config**. The template's own default
  communication language changed from Czech to **English**; individual projects choose
  their language via the install script's `--lang` parameter or by editing
  `doc/apm_config/LANGUAGE.user.md`.
- `rules/200-project-design-rules.mdc`: generalized from a `DESIGN_RULES.md`-only rule
  into the shared Config Resolution mechanism used by all three settings.
- `commands/role-assign.md`, `commands/role-show.md`: now read/write
  `doc/apm_config/AGENT_MODELS.user.md` instead of the table inside
  `rules/000-model-policy.mdc`.
- `skills/review-task/SKILL.md`: updated its reference to the Reviewer model assignment
  to point at the resolved AGENT_MODELS config.
- `rules/070-project-management.mdc`: added a **Source of Truth (SoT)** section (conflict
  handling rule — the active SoT pointer itself stays project data in
  `DESIGN_RULES.user.md`) and a one-line "state lives in files" principle, both promoted
  from project-level `DESIGN_RULES.md` content that turned out to be general, not
  project-specific. The Coder Task Report section now notes it documents the `high`-band
  tier only; `description` fixed from "two-actor model" to "Planner/Coder/Reviewer".
- `skills/plan-epic/SKILL.md`, `skills/execute-task/SKILL.md`,
  `skills/review-task/SKILL.md`, `skills/review-epic/SKILL.md`: wired up to the new band
  gate policy — conditional FT.7, report tier by band, band escalation bumps the report
  tier, Epic Report task table gained a Band / Human-gate column, and Human-facing
  presentation steps now use the Human Gate Briefing format.
- `apm_config/DESIGN_RULES.default.md`: reworked from a bare placeholder into a template
  that explains the `[general]`/`[project]` promotion convention and lists the sections
  that should remain genuinely project-specific (SoT pointer, forbidden tech, product
  invariants enforced in code, non-APM documentation language) now that orchestration,
  gate policy, and Reviewer duties live in `rules/`.
- `README.md`: added the "Configuration: defaults vs. project overrides" section, a new
  "Option C — Copy via install script" installation method, and rewrote "Choosing the
  communication language for a project" (previously "Creating a clone for a different
  communication language", which required forking the whole template). The
  **recommended** installation method moved from Option A (submodule) to Option C
  (copy) — only the copy method gets the comment-stripping token savings from Problem
  #1 (Context Tax).
- **Vocabulary unified: `Complexity: high` flag → `Band` (`low`/`medium`/`high`).**
  `rules/070-project-management.mdc` and `skills/plan-epic/SKILL.md` (Task List column,
  DoR checklist, output checklists) now name a Task's **band** everywhere a Coder model
  is recommended, instead of an optional binary flag — every Task has exactly one band,
  it is never "unflagged".
- `commands/role-assign.md`, `commands/role-show.md`: assignments are now read/written
  per **role × band** cell (`AGENT_MODELS.default.md`'s new table shape), not per role
  alone; a `—` cell (e.g. Planner `low`) means "not applicable", distinct from
  `unassigned`.
- **Rules renumbered to a steps-of-ten scheme**, mirroring the Epic/Task numbering
  already used in `rules/070-project-management.mdc` (`epic-010`, `epic-020`, ...): `00-*`
  → `000-*`, `01-*` → `010-*`, ..., `09-*` → `090-*`, `10-*` → `100-*`, ...,
  `20-project-design-rules.mdc` → `200-project-design-rules.mdc`. Every cross-reference in
  `rules/`, `skills/`, `commands/`, `scripts/`, and both `README*.md` was updated
  mechanically (descriptive part of each filename, e.g. `project-management.mdc`, is
  unchanged). This leaves 9 free numbers inside each decade for future insertions without
  another renumbering — see the "File Naming" example in
  `rules/000-meta-rules-and-skills.mdc`. `scripts/migrate_submodule_to_copy.py`
  deliberately keeps the **old** `rules/00-communication-language.mdc` path where it
  inspects a pre-migration git submodule checkout, which predates this rename.
- **`rules/000-meta-rules-and-skills.mdc`, `rules/060-project-structure.mdc`**: demoted
  from `alwaysApply: true` to agent-requested (`description`-only) activation — both
  already had a description written like an agent-requested trigger, and `060` was over
  its `alwaysApply` line limit anyway. Saves ~200+ lines of context on every agent call
  in a consuming project when neither topic is actually in play. `README.md`'s Rules
  table Activation column updated to "on request" for both.
- **This repo's own `.cursor/rules` / `.cursor/skills` symlinks removed.** They existed
  only so this repo's own past self-development could dogfood its rules via Cursor —
  irrelevant now that development here does not depend on it, and not needed by any
  documented consumption path (Option A submodule mounts the repo root directly, which
  already contains `rules/`/`skills/` at top level; Option C copies files). Verified this
  does not affect existing Option A submodule consumers.
- **`skills/project-init/templates/GLOSSARY.md`**: moved out of
  `doc/project-progress/GLOSSARY.md` — `doc/` is never copied by
  `scripts/install_into_project.py`, so a file only reachable there could never actually
  be seeded into a consuming project (see Fixed, below). `scripts/lib/installer.py` and
  `check_installation.py` both gained a `*/templates/*` exclusion from bilingual-comment
  stripping / leaked-comment checks — GLOSSARY.md and DECISIONS.md are bilingual content
  for the consuming project's Human, not agent rule text, so English is not their sole
  source of truth the way it is for `rules/`/`skills/`.
- **`rules/200-project-design-rules.mdc`**: a `DESIGN_RULES.user.md` "Forbidden
  technologies" entry now explicitly takes precedence over the corresponding
  `1xx-*.mdc` technology rule.
- **`rules/050-new-technology.mdc`**: added a "Bulk registration" variant for
  introducing several technologies at once (typically Phase 0) — same per-technology
  checklist, but one consolidated `README.md` table instead of repeated prose.
- **`rules/080-agent-security.mdc`**: added a rule that scripts consuming live untrusted
  network input run as a CLI process outside the agent chat session; the agent works
  from their recorded output/fixtures, not a live mid-session fetch.
- **`rules/140-fastapi.mdc`**: `globs` narrowed from `**/*.py` (every Python file in any
  project) to the `backend/`/`api/` tree plus the file names this rule's own "Project
  Structure" section already prescribes (`main.py`, `router.py`, `dependencies.py`,
  `service.py`, `schemas.py`) — a non-FastAPI Python project no longer pays this rule's
  context cost on every `.py` edit. `description` updated so the agent still pulls the
  rule in for FastAPI code that lands outside this layout (`060-project-structure.mdc`
  gained a matching one-line pointer to keep the two rules in sync).

### Fixed

- **`skills/project-init/SKILL.md` step 6**: referenced
  `.cursor/skills/project-init/templates/GLOSSARY.md`, which did not exist yet (the only
  glossary content lived at `doc/project-progress/GLOSSARY.md`, a path `doc/` never
  copies into a consuming project). The file now actually exists at that path; step 6
  also seeds the new `DECISIONS.md` template.
- **`rules/020-git.mdc`**: removed a `globs:` line that had no effect next to
  `alwaysApply: true` (now also caught by `check_installation.py`).
- **`rules/070-project-management.mdc`** Coder Task Report "Required content" table was
  missing the **Deviations from spec.md** section that `skills/execute-task/SKILL.md`'s
  template and `skills/review-task/SKILL.md`'s Step R4 already both required and checked
  for — the table now lists all 7 sections in the order every other document agrees on.
- **`README.md`** Rules table "Activation" column was stale for four rows: `150-qdrant.mdc`,
  `170-redis.mdc`, and `180-celery.mdc` were shown as `**/*.py` (implying no narrowing at
  all, though the actual `globs` in each file already were narrow) and
  `140-fastapi.mdc` still showed its pre-this-session pattern. All four now show a
  representative excerpt of their actual `globs`.

### Hard rule introduced

- `.cursor/` in a consuming project is now explicitly documented as **100% generated**
  by `scripts/install_into_project.py` and must **never be hand-edited**. Every
  project-specific override belongs in `doc/apm_config/*.user.md`.

## v1.0.0

- Initial tagged version: Reviewer role, Definition of Ready (DoR) gate, model policy,
  and agent security rules.
