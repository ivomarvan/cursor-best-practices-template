"""Shared pytest fixtures for the template's own test suite.

The suite tests the tooling under `scripts/` (installer, comment stripper, installation
checker) against the real template checkout, so a broken rule file or a length-limit
regression fails here — before it reaches a consuming project.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

TEMPLATE_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = TEMPLATE_ROOT / "scripts"

# Make `lib.*` and the CLI modules importable the same way the scripts do it.
sys.path.insert(0, str(SCRIPTS_DIR))


@pytest.fixture(scope="session")
def template_root() -> Path:
    """Root of this template checkout (the directory containing `rules/`, `skills/`)."""
    return TEMPLATE_ROOT


@pytest.fixture
def installed_project(tmp_path: Path, template_root: Path) -> Path:
    """A fresh consuming project with the template installed (`--lang cs`).

    Returns:
        Root of the temporary project directory.
    """
    from lib.installer import TemplateInstaller

    project = tmp_path / "project"
    project.mkdir()
    TemplateInstaller(template_root).install(project, lang_code="cs")
    return project
