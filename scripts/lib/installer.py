"""Core template-installation logic shared by the install and migrate CLI scripts.

See `rules/20-project-design-rules.mdc` for the Config Resolution mechanism this module
implements: template defaults live in `apm_config/<NAME>.default.md`, project overrides
live in `doc/apm_config/<NAME>.user.md`.
"""

from __future__ import annotations

import datetime
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from lib.strip_comments import strip_comments

#: Top-level entries copied verbatim (after comment stripping) into <target>/.cursor/.
COPY_ENTRIES: tuple[str, ...] = ("commands", "hooks", "hooks.json", "rules", "skills")

#: File suffixes eligible for bilingual "cs:" comment stripping.
FILTER_SUFFIXES: tuple[str, ...] = (".mdc", ".md", ".sh")

#: Config settings resolved via the default-vs-user-override mechanism (LANGUAGE is
#: handled separately by `_seed_language`, since it is generated, not copied verbatim).
CONFIG_NAMES: tuple[str, ...] = ("AGENT_MODELS", "DESIGN_RULES")

#: Version string that selects the legacy (pre-v1.1.0) config-file layout.
LEGACY_VERSION = "v1.0.0"

#: Fallback version when `git describe` is unavailable (e.g. not a git checkout).
DEFAULT_TEMPLATE_VERSION = "v1.1.0"

#: Known language presets for --lang; any other code is used verbatim as its own name.
LANGUAGE_NAMES: dict[str, str] = {
    "en": "English",
    "cs": "Czech (čeština)",
    "de": "German (Deutsch)",
}


class TemplateInstallError(RuntimeError):
    """Raised when the template cannot be installed into a target project."""


@dataclass
class InstallReport:
    """Summary of the files an install run created vs. left untouched, for CLI output."""

    created: list[Path] = field(default_factory=list)
    kept: list[Path] = field(default_factory=list)

    def record_created(self, path: Path) -> None:
        """Note that `path` was newly written by this run."""
        self.created.append(path)

    def record_kept(self, path: Path) -> None:
        """Note that `path` already existed and was intentionally left untouched."""
        self.kept.append(path)


class TemplateInstaller:
    """Installs (or re-installs) this template into a consuming project.

    Copies `commands/`, `hooks/`, `hooks.json`, `rules/`, `skills/` into
    `<target>/.cursor/`, stripping bilingual `cs:` comments, and seeds
    `doc/apm_config/*.user.md` from `apm_config/*.default.md` — but only if a user file
    does not exist yet, so a Human's existing project configuration is never
    overwritten. `<target>/.cursor/` itself is always wiped and rewritten in full: it is
    treated as 100% generated content, never hand-edited (see
    `rules/20-project-design-rules.mdc`).
    """

    def __init__(self, template_root: Path) -> None:
        """Args:
            template_root: Root of the cursor-best-practices-template checkout (the
                directory containing `rules/`, `skills/`, `apm_config/`, ...).
        """
        self._template_root = template_root

    def detect_version(self) -> str:
        """Return the template's current version tag/SHA, or a hardcoded fallback.

        Returns:
            The output of `git describe --tags --always` in the template checkout, or
            `DEFAULT_TEMPLATE_VERSION` if this is not a git checkout.
        """
        try:
            result = subprocess.run(
                ["git", "-C", str(self._template_root), "describe", "--tags", "--always"],
                capture_output=True,
                text=True,
                check=True,
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            return DEFAULT_TEMPLATE_VERSION
        return result.stdout.strip() or DEFAULT_TEMPLATE_VERSION

    def install(
        self,
        target: Path,
        lang_code: str = "en",
        config_layout: str | None = None,
    ) -> InstallReport:
        """Install the template into `target`, seeding config on first run.

        Args:
            target: Root of the consuming project (must already exist).
            lang_code: Language to seed `LANGUAGE.user.md` with on first install;
                ignored on re-install if that file already exists.
            config_layout: Version string selecting the config-file layout. Defaults to
                `self.detect_version()`. `LEGACY_VERSION` additionally writes config at
                the pre-v1.1.0 fixed paths (root `DESIGN_RULES.md`,
                `doc/AGENT_MODELS.md`), for external tooling that still expects them.

        Returns:
            An `InstallReport` listing every file created vs. kept.

        Raises:
            TemplateInstallError: If `target` does not exist or is not a directory.
        """
        if not target.is_dir():
            raise TemplateInstallError(
                f"target path does not exist or is not a directory: {target}"
            )

        resolved_layout = config_layout or self.detect_version()
        report = InstallReport()

        target_cursor = target / ".cursor"
        self._rewrite_cursor_dir(target_cursor)
        self._write_version_marker(target_cursor, resolved_layout)

        apm_config_dir = target / "doc" / "apm_config"
        apm_config_dir.mkdir(parents=True, exist_ok=True)

        for name in CONFIG_NAMES:
            default_file = self._template_root / "apm_config" / f"{name}.default.md"
            user_file = apm_config_dir / f"{name}.user.md"
            self._seed_from_default(default_file, user_file, report)

        self._seed_language(apm_config_dir / "LANGUAGE.user.md", lang_code, report)

        if resolved_layout == LEGACY_VERSION:
            self._write_legacy_paths(target, apm_config_dir, report)

        return report

    def _rewrite_cursor_dir(self, target_cursor: Path) -> None:
        """Wipe `target_cursor` and repopulate it from the template, comments stripped."""
        if target_cursor.exists():
            shutil.rmtree(target_cursor)
        target_cursor.mkdir(parents=True)

        for entry in COPY_ENTRIES:
            src = self._template_root / entry
            if not src.exists():
                continue
            dst = target_cursor / entry
            if src.is_dir():
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)

        for path in target_cursor.rglob("*"):
            if path.is_file() and path.suffix in FILTER_SUFFIXES:
                filtered = strip_comments(path.read_text(encoding="utf-8"), lang_code="cs")
                path.write_text(filtered, encoding="utf-8")

    def _write_version_marker(self, target_cursor: Path, version: str) -> None:
        """Write `.cursor/TEMPLATE_VERSION` recording the installed template version."""
        marker = target_cursor / "TEMPLATE_VERSION"
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        marker.write_text(
            "source:     git@github.com:ivomarvan/cursor-best-practices-template.git\n"
            f"version:    {version}\n"
            f"generated:  {timestamp}\n"
            "generator:  scripts/install_into_project.py\n",
            encoding="utf-8",
        )

    def _seed_from_default(
        self, default_file: Path, user_file: Path, report: InstallReport
    ) -> None:
        """Create `user_file` from `default_file` unless it already exists."""
        if user_file.exists():
            report.record_kept(user_file)
            return
        user_file.parent.mkdir(parents=True, exist_ok=True)
        filtered = strip_comments(default_file.read_text(encoding="utf-8"), lang_code="cs")
        user_file.write_text(filtered, encoding="utf-8")
        report.record_created(user_file)

    def _seed_language(self, user_file: Path, lang_code: str, report: InstallReport) -> None:
        """Create `LANGUAGE.user.md` for `lang_code`, unless it already exists."""
        if user_file.exists():
            report.record_kept(user_file)
            return
        language_name = LANGUAGE_NAMES.get(lang_code, lang_code)
        user_file.parent.mkdir(parents=True, exist_ok=True)
        user_file.write_text(
            "# Communication Language — Project Override\n\n"
            f"Seeded by `scripts/install_into_project.py --lang {lang_code}`. Edit this "
            "file by hand to change the language later — see "
            "`rules/00-communication-language.mdc`.\n\n"
            "## Active Setting\n\n"
            "| Parameter | Value |\n"
            "|-----|----|\n"
            f"| `<communication-language>` | {language_name} |\n"
            f"| `<lang-code>` | `{lang_code}` |\n",
            encoding="utf-8",
        )
        report.record_created(user_file)

    def _write_legacy_paths(
        self, target: Path, apm_config_dir: Path, report: InstallReport
    ) -> None:
        """Additionally seed the pre-v1.1.0 fixed config paths, for legacy tooling."""
        legacy_design_rules = target / "DESIGN_RULES.md"
        if not legacy_design_rules.exists():
            shutil.copy2(apm_config_dir / "DESIGN_RULES.user.md", legacy_design_rules)
            report.record_created(legacy_design_rules)

        legacy_agent_models = target / "doc" / "AGENT_MODELS.md"
        if not legacy_agent_models.exists():
            legacy_agent_models.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(apm_config_dir / "AGENT_MODELS.user.md", legacy_agent_models)
            report.record_created(legacy_agent_models)
