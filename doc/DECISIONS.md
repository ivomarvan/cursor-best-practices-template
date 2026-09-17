# Decisions Register — template

<!-- Append-only. One row per settled question about the template itself that could
     otherwise resurface in a later review or be silently contradicted by an edit. This
     is the same instrument the template asks consuming projects to keep
     (skills/project-init/templates/DECISIONS.md), applied to its own development.
     Keep entries short; link to the file/section that has the detail. -->

| # | Question | Decision | Date | Reference |
|---|----------|----------|------|-----------|
| 1 | Is `.cursor/` in a consuming project hand-editable? | Template-owned files (listed in `TEMPLATE_MANIFEST`): no — generated; overrides live in `doc/apm_config/*.user.md`. Project-owned files: yes (see #11). | 2026-09, revised 2026-09-17 | `rules/200-project-design-rules.mdc` |
| 2 | Recommended installation method? | Option C (filtered copy via `scripts/install_into_project.py`); submodule (A) and symlinks (B) stay documented but are not recommended. | 2026-09 | `README.md` § Using this repo |
| 3 | Where do project-specific Docker exemptions go? | `DESIGN_RULES.user.md`, never into `030-docker-policy.mdc` inside the project. General exemptions are proposed upstream. | 2026-09-17 | `rules/030-docker-policy.mdc` |
| 4 | Reviewer for `low` band? | Default `—`: deterministic gate is the review. A project may assign a model; never `unassigned`. | 2026-09-17 | `apm_config/AGENT_MODELS.default.md`, `rules/000-model-policy.mdc` |
| 5 | Automatic commit after APPROVE? | No — the Planner *offers* a commit; the Human answers with a trigger phrase. Reviewer path-scopes its diff otherwise. | 2026-09-17 | `rules/090-apm-orchestration.mdc` § A, `doc/KNOWN_LIMITATIONS.md` § A |
| 6 | Where are rule line limits measured? | On the installed (comment-stripped) form; enforced by `check_installation.py` and the template's `make check`. | 2026-09-17 | `rules/000-meta-rules-and-skills.mdc` |
| 7 | Do template defaults ship into the project? | Yes — `apm_config/*.default.md` is copied to `.cursor/apm_config/`, so the resolution rule is literally true in the project. | 2026-09-17 | `scripts/lib/installer.py` `COPY_ENTRIES` |
| 8 | How does the agent ask the Human for decisions? | One decision per message, plain problem, 2–4 options, one recommendation, then wait — `alwaysApply`. | 2026-09-17 | `rules/005-decision-protocol.mdc` |
| 9 | Should `session-start.sh` override an existing `core.hooksPath`? | No — set only if unset; otherwise print how to chain the commit-msg hook. | 2026-09-17 | `hooks/session-start.sh`, `hooks/README.md` |
| 10 | Minimum Python for `scripts/`? | 3.10 (`X | Y` unions OK, no `datetime.UTC`); CI runs 3.12. | 2026-09-17 | `pyproject.toml`, `.github/workflows/ci.yml` |
| 11 | Where do project-specific rules/skills live under Option C? | Next to template files in `.cursor/`: `rules/9xx-<slug>.mdc`, own `skills/<name>/`, `commands/<name>.md`. Installer removes only manifest-listed files on re-install (manifest chosen over `doc/apm_config/rules/` source-copy and over DESIGN_RULES-text-only). | 2026-09-17 | `scripts/lib/installer.py`, `README.md` § Adding project-specific rules |
