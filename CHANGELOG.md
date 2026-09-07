# Changelog

All notable changes to `cursor-best-practices-template` are documented in this file.

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

### Hard rule introduced

- `.cursor/` in a consuming project is now explicitly documented as **100% generated**
  by `scripts/install_into_project.py` and must **never be hand-edited**. Every
  project-specific override belongs in `doc/apm_config/*.user.md`.

## v1.0.0

- Initial tagged version: Reviewer role, Definition of Ready (DoR) gate, model policy,
  and agent security rules.
