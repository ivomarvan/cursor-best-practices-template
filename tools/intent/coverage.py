"""Coverage of intent by executable enforcement, and of code by intent."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from intent.model import Tree

DEFAULT_CODE_ROOTS = ("src", "backend/src", "frontend/src", "rules", "skills", "tools")
IGNORED_PARTS = {"__pycache__", ".git", "node_modules", ".venv", "dist", "build"}


@dataclass
class CoverageReport:
    total_contracts: int = 0
    machine_enforced: int = 0
    review_exceptions: list[str] = field(default_factory=list)
    uncovered_code: list[str] = field(default_factory=list)
    scanned_code: int = 0

    @property
    def enforcement_ratio(self) -> float:
        if self.total_contracts == 0:
            return 1.0
        return self.machine_enforced / self.total_contracts


def _owned_paths(tree: Tree) -> list[str]:
    owned: list[str] = []
    for node in tree.nodes.values():
        owned.extend(item.rstrip("/") for item in node.code_paths)
        owned.extend(item.rstrip("/") for item in node.test_paths)
    return owned


def _is_owned(relative: str, owned: list[str]) -> bool:
    return any(relative == item or relative.startswith(item + "/") for item in owned)


def build_report(tree: Tree, code_roots: tuple[str, ...] = DEFAULT_CODE_ROOTS) -> CoverageReport:
    report = CoverageReport()
    for node in tree.nodes.values():
        for contract in node.contracts:
            report.total_contracts += 1
            if contract.enforced_by == "review":
                report.review_exceptions.append(f"{node.id}/{contract.id}: {contract.text}")
            else:
                report.machine_enforced += 1

    owned = _owned_paths(tree)
    for root_name in code_roots:
        root = tree.root_dir / root_name
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file() or set(path.parts) & IGNORED_PARTS:
                continue
            relative = str(path.relative_to(tree.root_dir))
            report.scanned_code += 1
            if not _is_owned(relative, owned):
                report.uncovered_code.append(relative)
    return report


def render_report(report: CoverageReport) -> str:
    lines = [
        "# Intent coverage",
        "",
        f"- contracts: {report.total_contracts}",
        f"- machine-enforced: {report.machine_enforced} ({report.enforcement_ratio * 100:.0f}%)",
        f"- review exceptions: {len(report.review_exceptions)}",
        f"- files scanned: {report.scanned_code}",
        f"- files outside any node: {len(report.uncovered_code)}",
    ]
    if report.review_exceptions:
        lines += ["", "## Contracts without a machine enforcer", ""]
        lines += [f"- {item}" for item in report.review_exceptions]
    if report.uncovered_code:
        lines += ["", "## Files not owned by any node", ""]
        lines += [f"- `{item}`" for item in report.uncovered_code]
    lines.append("")
    return "\n".join(lines)


def find_node_for_path(tree: Tree, target: str) -> str | None:
    """Reverse lookup: which node governs ``target``? Deepest node wins."""
    best: tuple[int, str] | None = None
    normalised = str(Path(target)).rstrip("/")
    for node in tree.nodes.values():
        for code_path in node.code_paths:
            trimmed = code_path.rstrip("/")
            if normalised == trimmed or normalised.startswith(trimmed + "/"):
                depth = tree.depth_of(node.id)
                if best is None or depth > best[0]:
                    best = (depth, node.id)
    return None if best is None else best[1]
