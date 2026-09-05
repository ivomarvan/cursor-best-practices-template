# Changelog

All notable changes to `cursor-best-practices-template` are documented in this file.

## v1.1.0

### Added

- **Config Resolution mechanism** (`rules/20-project-design-rules.mdc`): a single,
  generic default-vs-override pattern now backs three settings — `AGENT_MODELS`,
  `DESIGN_RULES`, `LANGUAGE`. Template defaults ship in `apm_config/<NAME>.default.md`;
  a consuming project overrides a setting **in full** by creating
  `doc/apm_config/<NAME>.user.md`. This replaces the previous single-purpose mechanism
  that only covered `DESIGN_RULES.md` at the project root.
- **`apm_config/` directory**: `AGENT_MODELS.default.md` (the former *Active Role
  Assignments* table, moved out of `rules/00-model-policy.mdc`), `DESIGN_RULES.default.md`
  (empty skeleton), `LANGUAGE.default.md` (English — the former active-settings table,
  moved out of `rules/00-communication-language.mdc`).
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
  moving them into `doc/apm_config/*.user.md` before regenerating `.cursor/`. Prints
  (does not run) the git commands needed to deregister the submodule.
- **`scripts/lib/`**: shared Python library backing both CLIs — `installer.py`
  (`TemplateInstaller` — copy/filter/seed logic), `migration.py` (submodule-to-copy
  helpers), and `strip_comments.py`, which removes `<!-- cs: ... -->` and `# cs: ...`
  bilingual annotation comments from copied files without touching example text that
  merely documents the comment syntax (e.g. in `rules/00-meta-rules-and-skills.mdc`).
- **`CHANGELOG.md`** (this file).

### Changed

- `rules/00-model-policy.mdc`: the *Active Role Assignments* table is no longer stored
  in this rule file — it is resolved from **AGENT_MODELS config** (see Config Resolution
  above). The `unassigned` → ask-the-Human behavior is unchanged, only its storage
  location moved.
- `rules/00-communication-language.mdc`: the active-language table is no longer stored
  in this rule file — it is resolved from **LANGUAGE config**. The template's own default
  communication language changed from Czech to **English**; individual projects choose
  their language via the install script's `--lang` parameter or by editing
  `doc/apm_config/LANGUAGE.user.md`.
- `rules/20-project-design-rules.mdc`: generalized from a `DESIGN_RULES.md`-only rule
  into the shared Config Resolution mechanism used by all three settings.
- `commands/role-assign.md`, `commands/role-show.md`: now read/write
  `doc/apm_config/AGENT_MODELS.user.md` instead of the table inside
  `rules/00-model-policy.mdc`.
- `skills/review-task/SKILL.md`: updated its reference to the Reviewer model assignment
  to point at the resolved AGENT_MODELS config.
- `README.md`: added the "Configuration: defaults vs. project overrides" section, a new
  "Option C — Copy via install script" installation method, and rewrote "Choosing the
  communication language for a project" (previously "Creating a clone for a different
  communication language", which required forking the whole template).

### Hard rule introduced

- `.cursor/` in a consuming project is now explicitly documented as **100% generated**
  by `scripts/install_into_project.py` and must **never be hand-edited**. Every
  project-specific override belongs in `doc/apm_config/*.user.md`.

## v1.0.0

- Initial tagged version: Reviewer role, Definition of Ready (DoR) gate, model policy,
  and agent security rules.
