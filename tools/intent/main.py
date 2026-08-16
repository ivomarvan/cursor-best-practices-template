"""Command line entry point for the intent tree tooling."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from intent import coverage as coverage_module
from intent import generate, realization, scope, slicing, validate
from intent.miniyaml import dump, parse
from intent.model import (
    INTENT_DIRNAME,
    NODES_DIRNAME,
    REGISTRY_FILENAME,
    Tree,
    TreeError,
    find_root,
    load_tree,
)

NODE_TEMPLATE = """# {title}

## Refines
One sentence: which part of the parent this node develops further.

## Meaning
Two to eight sentences. What this is and what it is for, without repeating the parent.

## Contracts
Explain the contracts from the front matter when one line is not enough.

## Non-goals
What explicitly does not belong here.

## Open questions
"""

ROOT_TEMPLATE = """# {title}

## Meaning
Two to eight sentences describing the product as a whole.

## Contracts
Explain the contracts from the front matter when one line is not enough.

## Non-goals
What this product explicitly does not do.

## Open questions
"""


def _resolve_root(args: argparse.Namespace) -> Path:
    if args.root:
        root = Path(args.root).resolve()
        if not (root / INTENT_DIRNAME).is_dir():
            raise TreeError(f"{root} does not contain {INTENT_DIRNAME}")
        return root
    return find_root()


def cmd_validate(args: argparse.Namespace) -> int:
    tree = load_tree(_resolve_root(args))
    findings = validate.validate(tree)
    errors = [item for item in findings if item.level == "error"]
    warnings = [item for item in findings if item.level == "warning"]

    if args.json:
        payload = {
            "errors": [vars(item) for item in errors],
            "warnings": [vars(item) for item in warnings],
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        for finding in findings:
            print(finding.format())
        print(f"\n{len(tree.nodes)} node(s): {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


def cmd_map(args: argparse.Namespace) -> int:
    tree = load_tree(_resolve_root(args))
    changed = generate.write_generated(tree)
    if changed:
        for item in changed:
            print(f"updated {item}")
    else:
        print("generated files already up to date")
    return 0


def cmd_new(args: argparse.Namespace) -> int:
    root = _resolve_root(args)
    tree = load_tree(root)
    registry = tree.registry

    if args.parent and args.parent not in tree.nodes:
        raise TreeError(f"parent {args.parent} does not exist")
    if not args.parent and tree.roots():
        raise TreeError("the tree already has a root; pass --parent")
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", args.slug):
        raise TreeError("slug must be lowercase letters, digits and dashes")

    node_id = f"{registry.prefix}{registry.next_serial:04d}"
    title = args.title or args.slug.replace("-", " ").capitalize()

    front = {
        "id": node_id,
        "parent": args.parent,
        "slug": args.slug,
        "title": title,
        "status": "proposed",
        "uses": [],
        "talks_to": [],
        "superseded_by": None,
        "contracts": [],
        "code_paths": [],
        "test_paths": [],
        "open_questions": [],
    }
    template = ROOT_TEMPLATE if args.parent is None else NODE_TEMPLATE
    body = template.format(title=title)
    target = root / INTENT_DIRNAME / NODES_DIRNAME / f"{node_id}-{args.slug}.md"
    target.write_text(f"---\n{dump(front)}---\n\n{body}", encoding="utf-8")

    registry_path = root / INTENT_DIRNAME / REGISTRY_FILENAME
    data = parse(registry_path.read_text(encoding="utf-8"))
    issued = data.get("issued") or {}
    issued[node_id] = {"slug": args.slug}
    data["issued"] = issued
    data["next_serial"] = registry.next_serial + 1
    registry_path.write_text(dump(data), encoding="utf-8")

    print(f"created {target.relative_to(root)}")
    print(f"registry next_serial -> {registry.next_serial + 1}")
    print("status is 'proposed'; promote it to 'current' only after review")
    return 0


def cmd_move(args: argparse.Namespace) -> int:
    root = _resolve_root(args)
    tree = load_tree(root)
    node = tree.nodes.get(args.node)
    if node is None or node.source is None:
        raise TreeError(f"node {args.node} does not exist")
    if args.parent not in tree.nodes:
        raise TreeError(f"parent {args.parent} does not exist")
    if args.parent == args.node:
        raise TreeError("a node cannot be its own parent")

    text = node.source.read_text(encoding="utf-8")
    replaced, count = re.subn(
        r"^parent:.*$", f"parent: {args.parent}", text, count=1, flags=re.MULTILINE
    )
    if count == 0:
        raise TreeError(f"{node.source}: no 'parent:' line found")
    node.source.write_text(replaced, encoding="utf-8")
    generate.write_generated(load_tree(root))
    print(f"{args.node} now refines {args.parent}; regenerated map and index")
    print("run the abstraction critic on both nodes before promoting them")
    return 0


def cmd_slice(args: argparse.Namespace) -> int:
    tree = load_tree(_resolve_root(args))
    try:
        result = slicing.build_slice(tree, args.node, for_implementation=args.for_ != "plan")
    except KeyError:
        raise TreeError(f"node {args.node} does not exist") from None
    if args.json:
        print(json.dumps(vars(result), indent=2, ensure_ascii=False))
    else:
        print(slicing.render_slice(tree, result), end="")
    return 0


def cmd_scope(args: argparse.Namespace) -> int:
    tree = load_tree(_resolve_root(args))
    run_dir = Path(args.run).resolve()
    violations, declaration = scope.check_scope(tree, run_dir, args.base, args.node)
    if violations:
        print(f"scope violation against {declaration.source}:")
        for item in violations:
            print(f"  undeclared change: {item}")
        print("\nRaise the complexity of this run and wake the independent review.")
        return 1
    print(f"scope clean ({len(declaration.allowed())} declared path(s))")
    return 0


def cmd_coverage(args: argparse.Namespace) -> int:
    tree = load_tree(_resolve_root(args))
    report = coverage_module.build_report(tree)
    if args.json:
        print(json.dumps(vars(report), indent=2, ensure_ascii=False))
    else:
        print(coverage_module.render_report(report), end="")
    if args.strict and (report.review_exceptions or report.uncovered_code):
        return 1
    return 0


def cmd_owner(args: argparse.Namespace) -> int:
    tree = load_tree(_resolve_root(args))
    node_id = coverage_module.find_node_for_path(tree, args.path)
    if node_id is None:
        print(f"no node owns {args.path}")
        return 1
    node = tree.nodes[node_id]
    print(f"{node_id} — {node.title} ({'/'.join(tree.path_of(node_id))})")
    return 0


def _realization_context(
    args: argparse.Namespace,
) -> tuple[Tree, realization.Layer, realization.Policy]:
    tree = load_tree(_resolve_root(args))
    return tree, realization.load_layer(tree.intent_dir), realization.load_policy(tree.intent_dir)


def cmd_realization_status(args: argparse.Namespace) -> int:
    tree, layer, policy = _realization_context(args)
    states = realization.compute_states(tree, layer, policy)
    if args.node:
        if args.node not in states:
            raise TreeError(f"{args.node} is not a current node")
        states = {args.node: states[args.node]}
    if args.json:
        payload = {node_id: vars(state) for node_id, state in states.items()}
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(realization.render_states(tree, states), end="")
    return 0


def cmd_realization_worklist(args: argparse.Namespace) -> int:
    tree, layer, policy = _realization_context(args)
    states = realization.compute_states(tree, layer, policy)
    if args.json:
        items = [vars(state) for state in realization.build_worklist(tree, states)]
        print(json.dumps(items, indent=2, ensure_ascii=False))
    else:
        print(realization.render_worklist(tree, states), end="")
    return 0


def cmd_realization_summary(args: argparse.Namespace) -> int:
    tree, layer, policy = _realization_context(args)
    states = realization.compute_states(tree, layer, policy)
    if args.json:
        print(json.dumps(realization.summarise(states), indent=2))
    else:
        print(realization.render_summary(states), end="")
    return 0


def cmd_realization_claim(args: argparse.Namespace) -> int:
    tree, layer, policy = _realization_context(args)
    state = realization.claim(tree, layer, policy, args.node, args.evidence, args.by)
    realization.save_layer(layer)
    print(f"{args.node} claimed against {args.evidence} — now {state.summary()}")
    return 0


def cmd_realization_affirm(args: argparse.Namespace) -> int:
    tree, layer, policy = _realization_context(args)
    touched = realization.affirm(tree, layer, policy, args.node, args.by, args.reason, args.subtree)
    realization.save_layer(layer)
    print(f"affirmed {len(touched)} claim(s): {', '.join(touched)}")
    print("The evidence was not re-run; only its wording baseline moved.")
    return 0


def cmd_realization_accept(args: argparse.Namespace) -> int:
    tree, layer, _ = _realization_context(args)
    decision = "rejected" if args.reject else "approved"
    state = realization.decide(tree, layer, args.node, decision, args.by, args.note)
    realization.save_layer(layer)
    print(f"{args.node} {decision} by {args.by} — now {state.summary()}")
    return 0


def cmd_realization_check(args: argparse.Namespace) -> int:
    tree, layer, policy = _realization_context(args)
    problems = realization.check_layer(tree, layer, policy)
    for problem in problems:
        print(f"ERROR {problem}")
    if problems:
        print(f"\n{len(problems)} realization layer violation(s)")
        return 1
    print(f"realization layer consistent ({len(layer.entries)} entry/entries)")
    return 0


def cmd_realization_prune(args: argparse.Namespace) -> int:
    tree, layer, _ = _realization_context(args)
    removed = realization.prune(tree, layer)
    if not removed:
        print("nothing to prune")
        return 0
    realization.save_layer(layer)
    print(f"removed {len(removed)} entry/entries: {', '.join(removed)}")
    return 0


def _add_realization_commands(sub: argparse._SubParsersAction) -> None:
    parser = sub.add_parser("realization", help="claims about fulfilling the intent")
    inner = parser.add_subparsers(dest="realization_command", required=True)

    status = inner.add_parser("status", help="derived state of every current node")
    status.add_argument("--node")
    status.add_argument("--json", action="store_true")
    status.set_defaults(func=cmd_realization_status)

    worklist = inner.add_parser("worklist", help="what still needs work, ancestors first")
    worklist.add_argument("--json", action="store_true")
    worklist.set_defaults(func=cmd_realization_worklist)

    summary = inner.add_parser("summary", help="how much of the intent is realized")
    summary.add_argument("--json", action="store_true")
    summary.set_defaults(func=cmd_realization_summary)

    claim = inner.add_parser("claim", help="record that a node's contracts hold")
    claim.add_argument("node")
    claim.add_argument("--evidence", required=True, help="run directory or VERIFY.md")
    claim.add_argument("--by", required=True, help="who claims it; never the Coder")
    claim.set_defaults(func=cmd_realization_claim)

    affirm = inner.add_parser("affirm", help="keep a claim after a harmless text change")
    affirm.add_argument("node")
    affirm.add_argument("--by", required=True, help="a human; agent roles are refused")
    affirm.add_argument("--reason", required=True)
    affirm.add_argument("--subtree", action="store_true", help="affirm descendants as well")
    affirm.set_defaults(func=cmd_realization_affirm)

    accept = inner.add_parser("accept", help="human verdict on a claim")
    accept.add_argument("node")
    accept.add_argument("--by", required=True)
    accept.add_argument("--note")
    accept.add_argument("--reject", action="store_true", help="reject instead of approve")
    accept.set_defaults(func=cmd_realization_accept)

    check = inner.add_parser("check", help="internal consistency of the layer (R1-R7)")
    check.set_defaults(func=cmd_realization_check)

    prune = inner.add_parser("prune", help="drop entries for nodes that are no longer current")
    prune.set_defaults(func=cmd_realization_prune)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="intent",
        description="Tooling for the intent tree (ICE methodology).",
    )
    parser.add_argument("--root", help="project root; defaults to the nearest doc/intent parent")
    sub = parser.add_subparsers(dest="command", required=True)

    validate_parser = sub.add_parser("validate", help="run machine rules V1-V10")
    validate_parser.add_argument("--json", action="store_true")
    validate_parser.set_defaults(func=cmd_validate)

    map_parser = sub.add_parser("map", help="regenerate MAP.md and INDEX.json")
    map_parser.set_defaults(func=cmd_map)

    new_parser = sub.add_parser("new", help="allocate an id and create a node")
    new_parser.add_argument("--parent", help="parent node id; omit only for the root")
    new_parser.add_argument("--slug", required=True)
    new_parser.add_argument("--title")
    new_parser.set_defaults(func=cmd_new)

    move_parser = sub.add_parser("move", help="re-parent a node")
    move_parser.add_argument("node")
    move_parser.add_argument("--parent", required=True)
    move_parser.set_defaults(func=cmd_move)

    slice_parser = sub.add_parser("slice", help="print the context slice for a node")
    slice_parser.add_argument("node")
    slice_parser.add_argument(
        "--for", dest="for_", choices=("plan", "implement"), default="implement"
    )
    slice_parser.add_argument("--json", action="store_true")
    slice_parser.set_defaults(func=cmd_slice)

    scope_parser = sub.add_parser("scope", help="check the diff against declared outputs")
    scope_parser.add_argument("--run", required=True, help="run directory with plan.md or run.md")
    scope_parser.add_argument("--base", help="git ref to diff against (default: working tree)")
    scope_parser.add_argument("--node", action="append", help="node whose paths are allowed")
    scope_parser.set_defaults(func=cmd_scope)

    coverage_parser = sub.add_parser("coverage", help="contracts without tests, code without nodes")
    coverage_parser.add_argument("--json", action="store_true")
    coverage_parser.add_argument("--strict", action="store_true", help="exit 1 on any gap")
    coverage_parser.set_defaults(func=cmd_coverage)

    owner_parser = sub.add_parser("owner", help="which node governs a path")
    owner_parser.add_argument("path")
    owner_parser.set_defaults(func=cmd_owner)

    _add_realization_commands(sub)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except TreeError as exc:
        print(f"intent: {exc}", file=sys.stderr)
        return 2
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print(f"intent: {exc}", file=sys.stderr)
        return 2
