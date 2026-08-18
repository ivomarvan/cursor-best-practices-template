"""Reach tests for template_checks (the cmd: enforcer behind i0001 c1 and c2)."""

from __future__ import annotations

import contextlib
import io
import shutil
import tempfile
import unittest
from pathlib import Path

from checks import template_checks


class HarnessBuilder:
    """Minimal template under ``<tmp>/project/.cursor/`` for check reach tests."""

    def __init__(self) -> None:
        self._tmp = tempfile.mkdtemp(prefix="harness-")
        self.project = Path(self._tmp) / "project"
        self.root = self.project / ".cursor"
        self.root.mkdir(parents=True)
        (self.root / "rules").mkdir()
        (self.root / "skills" / "demo").mkdir(parents=True)
        (self.root / ".cursor").mkdir()
        self.write(
            "rules/00-demo.mdc",
            "---\nalwaysApply: true\n---\n\n# Demo rule\n",
        )
        self.write(
            "skills/demo/SKILL.md",
            "---\nname: demo\ndescription: A demo skill for harness tests.\n---\n\n# Demo\n",
        )
        self.symlink(".cursor/rules", "../rules")
        self.symlink(".cursor/skills", "../skills")

    def cleanup(self) -> None:
        shutil.rmtree(self._tmp, ignore_errors=True)

    def write(self, relative: str, content: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def symlink(self, relative: str, target: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() or path.is_symlink():
            path.unlink()
        path.symlink_to(target)

    def run_template(self) -> tuple[int, str]:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = template_checks.main(["--root", str(self.root)])
        return code, buf.getvalue()


class TemplateLinkTest(unittest.TestCase):
    def setUp(self) -> None:
        self.harness = HarnessBuilder()
        self.addCleanup(self.harness.cleanup)

    def test_a_broken_link_in_a_rule_is_reported(self) -> None:
        self.harness.write(
            "rules/00-demo.mdc",
            "---\nalwaysApply: true\n---\n\nSee [x](../rules/does-not-exist.mdc).\n",
        )
        code, out = self.harness.run_template()
        self.assertEqual(code, 1)
        self.assertIn("broken link", out)

    def test_a_broken_link_in_a_skill_is_reported(self) -> None:
        self.harness.write(
            "skills/demo/SKILL.md",
            "---\nname: demo\ndescription: Demo.\n---\n\n"
            "See [x](../../rules/does-not-exist.mdc).\n",
        )
        code, out = self.harness.run_template()
        self.assertEqual(code, 1)
        self.assertIn("broken link", out)

    def test_a_broken_link_in_a_second_tier_skill_file_is_reported(self) -> None:
        self.harness.write(
            "skills/demo/reference.md",
            "See [missing](../../rules/nope.mdc).\n",
        )
        code, out = self.harness.run_template()
        self.assertEqual(code, 1)
        self.assertIn("broken link", out)

    def test_a_broken_link_in_a_nested_skill_file_is_reported(self) -> None:
        self.harness.write(
            "skills/demo/sub/examples.md",
            "See [missing](../../../rules/nope.mdc).\n",
        )
        code, out = self.harness.run_template()
        self.assertEqual(code, 1)
        self.assertIn("broken link", out)

    def test_a_link_inside_a_fenced_block_is_not_a_reference(self) -> None:
        self.harness.write(
            "skills/demo/SKILL.md",
            "---\nname: demo\ndescription: Demo.\n---\n\n```\n[x](../../rules/nope.mdc)\n```\n",
        )
        code, out = self.harness.run_template()
        self.assertEqual(code, 0, out)
        self.assertIn("template contracts satisfied", out)

    def test_an_unterminated_fenced_block_is_reported(self) -> None:
        self.harness.write(
            "skills/demo/SKILL.md",
            "---\nname: demo\ndescription: Demo.\n---\n\n```\n\nSee [x](../../rules/nope.mdc).\n",
        )
        code, out = self.harness.run_template()
        self.assertEqual(code, 1)
        self.assertIn("unterminated code block", out)
        self.assertIn("SKILL.md", out)

    def test_an_anchor_only_link_is_not_resolved(self) -> None:
        self.harness.write(
            "skills/demo/SKILL.md",
            "---\nname: demo\ndescription: Demo.\n---\n\nSee [x](#section).\n",
        )
        code, out = self.harness.run_template()
        self.assertEqual(code, 0, out)

    def test_an_external_link_is_not_resolved(self) -> None:
        self.harness.write(
            "skills/demo/SKILL.md",
            "---\nname: demo\ndescription: Demo.\n---\n\n"
            "See [a](https://example.com) and [b](mailto:a@b.c).\n",
        )
        code, out = self.harness.run_template()
        self.assertEqual(code, 0, out)

    def test_a_bracketed_target_is_not_resolved(self) -> None:
        self.harness.write(
            "skills/demo/SKILL.md",
            "---\nname: demo\ndescription: Demo.\n---\n\nSee [x](<a b.md>).\n",
        )
        code, out = self.harness.run_template()
        self.assertEqual(code, 0, out)

    def test_a_link_to_an_existing_directory_is_accepted(self) -> None:
        self.harness.write(
            "skills/demo/SKILL.md",
            "---\nname: demo\ndescription: Demo.\n---\n\nSee [rules](../../rules/).\n",
        )
        code, out = self.harness.run_template()
        self.assertEqual(code, 0, out)


class TemplateSymlinkTest(unittest.TestCase):
    def setUp(self) -> None:
        self.harness = HarnessBuilder()
        self.addCleanup(self.harness.cleanup)

    def test_a_missing_cursor_symlink_is_reported(self) -> None:
        for name in ("rules", "skills"):
            with self.subTest(name=name):
                harness = HarnessBuilder()
                self.addCleanup(harness.cleanup)
                (harness.root / ".cursor" / name).unlink()
                code, out = harness.run_template()
                self.assertEqual(code, 1)
                self.assertIn("expected a symlink", out)

    def test_a_real_directory_in_place_of_the_symlink_is_reported(self) -> None:
        for name in ("rules", "skills"):
            with self.subTest(name=name):
                harness = HarnessBuilder()
                self.addCleanup(harness.cleanup)
                link = harness.root / ".cursor" / name
                link.unlink()
                link.mkdir()
                code, out = harness.run_template()
                self.assertEqual(code, 1)
                self.assertIn("expected a symlink", out)

    def test_a_dangling_symlink_is_reported(self) -> None:
        for name in ("rules", "skills"):
            with self.subTest(name=name):
                harness = HarnessBuilder()
                self.addCleanup(harness.cleanup)
                harness.symlink(f".cursor/{name}", f"../{name}-gone")
                code, out = harness.run_template()
                self.assertEqual(code, 1)
                self.assertIn("does not resolve to a directory", out)

    def test_a_symlink_pointing_outside_the_harness_is_reported(self) -> None:
        for name in ("rules", "skills"):
            with self.subTest(name=name):
                harness = HarnessBuilder()
                self.addCleanup(harness.cleanup)
                (harness.root / "doc").mkdir(exist_ok=True)
                harness.symlink(f".cursor/{name}", "../doc")
                code, out = harness.run_template()
                self.assertEqual(code, 1)
                self.assertIn("symlink resolves to", out)

    def test_the_checks_pass_with_the_harness_mounted_as_cursor(self) -> None:
        code, out = self.harness.run_template()
        self.assertEqual(code, 0, out)

    def test_a_mounted_harness_still_reports_a_broken_symlink(self) -> None:
        (self.harness.root / ".cursor" / "skills").unlink()
        code, out = self.harness.run_template()
        self.assertEqual(code, 1)
        self.assertIn("expected a symlink", out)


if __name__ == "__main__":
    unittest.main()
