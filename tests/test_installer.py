"""Tests for `scripts/lib/installer.py` — install into a temp project and audit it.

These are the template's own deterministic gate: the real `rules/` and `skills/` are
installed with comments stripped, then `check_installation.py` must report zero
discrepancies. A rule over its line limit, a leaked `cs:` comment, or a frontmatter
mistake therefore fails the template's CI, not the consuming project's session.
"""

from __future__ import annotations

from pathlib import Path

import pytest

import check_installation
from lib.installer import (
    COPY_ENTRIES,
    MANIFEST_NAME,
    TemplateInstaller,
    TemplateInstallError,
    read_manifest,
)


def test_install_creates_expected_layout(installed_project: Path) -> None:
    cursor = installed_project / ".cursor"
    for entry in COPY_ENTRIES:
        assert (cursor / entry).exists(), entry
    assert (cursor / "TEMPLATE_VERSION").is_file()
    for name in ("AGENT_MODELS", "DESIGN_RULES", "LANGUAGE"):
        assert (installed_project / "doc" / "apm_config" / f"{name}.user.md").is_file()
        assert (cursor / "apm_config" / f"{name}.default.md").is_file()


def test_install_passes_installation_checker(installed_project: Path) -> None:
    results = check_installation.InstallationChecker(installed_project).run()
    problems = [r for r in results if r.is_problem()]
    assert not problems, "\n".join(f"{r.status} {r.label} — {r.detail}" for r in problems)


def test_installer_and_checker_agree_on_copy_set() -> None:
    # The checker duplicates the copy set on purpose (it must stay importable standalone);
    # this test is the contract that keeps the two constants in sync.
    assert set(COPY_ENTRIES) == set(check_installation.EXPECTED_CURSOR_ENTRIES)


def test_reinstall_keeps_user_config(installed_project: Path, template_root: Path) -> None:
    user_file = installed_project / "doc" / "apm_config" / "DESIGN_RULES.user.md"
    user_file.write_text("# my project rules\n", encoding="utf-8")

    report = TemplateInstaller(template_root).install(installed_project, lang_code="cs")

    assert user_file.read_text(encoding="utf-8") == "# my project rules\n"
    assert user_file in report.kept


def test_reinstall_keeps_project_owned_files(installed_project: Path, template_root: Path) -> None:
    # Project-owned content lives next to template files and must survive a re-install
    # — see rules/200-project-design-rules.mdc (manifest-based ownership).
    cursor = installed_project / ".cursor"
    project_rule = cursor / "rules" / "900-domain.mdc"
    project_rule.write_text("---\nalwaysApply: false\n---\n# Domain\n", encoding="utf-8")
    project_skill = cursor / "skills" / "my-skill" / "SKILL.md"
    project_skill.parent.mkdir()
    project_skill.write_text("---\nname: my-skill\n---\n", encoding="utf-8")
    mcp = cursor / "mcp.json"
    mcp.write_text("{}\n", encoding="utf-8")

    TemplateInstaller(template_root).install(installed_project, lang_code="cs")

    assert project_rule.is_file()
    assert project_skill.is_file()
    assert mcp.is_file()
    manifest = read_manifest(cursor)
    assert manifest is not None
    assert "rules/900-domain.mdc" not in manifest
    assert "rules/020-git.mdc" in manifest


def test_reinstall_removes_files_dropped_by_template(
    installed_project: Path, template_root: Path
) -> None:
    # Simulate a file the previous template version installed but the current one no
    # longer ships: listed in the manifest -> must be removed, not left as an orphan.
    cursor = installed_project / ".cursor"
    dropped = cursor / "rules" / "099-old-rule.mdc"
    dropped.write_text("---\nalwaysApply: false\n---\n", encoding="utf-8")
    manifest = cursor / MANIFEST_NAME
    manifest.write_text(manifest.read_text(encoding="utf-8") + "rules/099-old-rule.mdc\n")

    TemplateInstaller(template_root).install(installed_project, lang_code="cs")

    assert not dropped.exists()


def test_template_file_edits_are_overwritten(installed_project: Path, template_root: Path) -> None:
    git_rule = installed_project / ".cursor" / "rules" / "020-git.mdc"
    git_rule.write_text("hand edit\n", encoding="utf-8")

    TemplateInstaller(template_root).install(installed_project, lang_code="cs")

    assert git_rule.read_text(encoding="utf-8") != "hand edit\n"


def test_install_without_manifest_keeps_unknown_files(
    installed_project: Path, template_root: Path
) -> None:
    # Pre-manifest installs (v1.1.x) have no TEMPLATE_MANIFEST; the fallback removes only
    # the current template's own paths and leaves everything else alone.
    cursor = installed_project / ".cursor"
    (cursor / MANIFEST_NAME).unlink()
    project_rule = cursor / "rules" / "910-legacy-project.mdc"
    project_rule.write_text("---\nalwaysApply: false\n---\n", encoding="utf-8")

    TemplateInstaller(template_root).install(installed_project, lang_code="cs")

    assert project_rule.is_file()
    assert (cursor / MANIFEST_NAME).is_file()


def test_checker_warns_on_rule_outside_project_namespace(installed_project: Path) -> None:
    orphan = installed_project / ".cursor" / "rules" / "300-not-ours.mdc"
    orphan.write_text("---\nalwaysApply: false\n---\n", encoding="utf-8")
    ok_rule = installed_project / ".cursor" / "rules" / "900-ours.mdc"
    ok_rule.write_text("---\nalwaysApply: false\n---\n", encoding="utf-8")

    results = check_installation.InstallationChecker(installed_project).run()

    warnings = [r for r in results if r.status == check_installation.Status.WARNING]
    assert [r.label for r in warnings] == [".cursor/rules/300-not-ours.mdc not in manifest"]


def test_language_seed_uses_requested_code(tmp_path: Path, template_root: Path) -> None:
    project = tmp_path / "p"
    project.mkdir()
    TemplateInstaller(template_root).install(project, lang_code="de")
    text = (project / "doc" / "apm_config" / "LANGUAGE.user.md").read_text(encoding="utf-8")
    assert "German (Deutsch)" in text
    assert "| `<lang-code>` | `de` |" in text


def test_install_into_missing_target_raises(tmp_path: Path, template_root: Path) -> None:
    with pytest.raises(TemplateInstallError):
        TemplateInstaller(template_root).install(tmp_path / "does-not-exist")


def test_installed_rules_contain_no_cs_comments(installed_project: Path) -> None:
    rules = list((installed_project / ".cursor" / "rules").glob("*.mdc"))
    assert rules
    for path in rules:
        assert "<!-- cs:" not in path.read_text(encoding="utf-8"), path.name
