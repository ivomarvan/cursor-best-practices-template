"""Realization layer: what the project claims about fulfilling its intent.

Only assertions are stored — that someone claimed a node realized, against which wording
of the intent, and whether a human accepted it. Staleness, blocking, the reason a claim
stopped holding and the worklist are all **computed** from the difference between the
stored fingerprints and the current tree.

That split is the whole design. Because staleness is never written down, an inconsistent
combination (a realized child under an ancestor whose meaning moved) cannot be stored in
the first place, and a node file stays pure meaning instead of carrying machine state.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path

from intent.miniyaml import YamlError, dump, parse
from intent.model import (
    POLICY_FILENAME,
    REALIZATION_FILENAME,
    Node,
    Tree,
    TreeError,
)
from intent.validate import enforcer_problem

SCHEMA_VERSION = 1
FINGERPRINT_PREFIX = "sha256:"
FINGERPRINT_DIGITS = 16

#: Sections whose wording is part of the meaning a claim was made against.
MEANING_SECTIONS = ("Refines", "Meaning", "Contracts", "Non-goals")

ACCEPTANCE_PROFILES = ("none", "standard", "leaf", "strict")
EVIDENCE_PROFILES = ("standard", "relaxed")
ACCEPTANCE_DECISIONS = ("approved", "rejected")

#: Names an agent may carry. A human decision signed with one of these is a forgery.
AGENT_ROLES = ("coordinator", "planner", "critic", "coder", "grader", "adversary")

GRADER_FILENAME = "grader.md"


# --------------------------------------------------------------------------- fingerprints


def _normalise(text: str) -> str:
    """Strip trailing whitespace and surrounding blank lines, keeping inner structure."""
    lines = [line.rstrip() for line in text.splitlines()]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines)


def body_sections(node: Node) -> dict[str, str]:
    """Split a node body into its ``## `` sections, keyed by heading."""
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in node.body.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            sections.setdefault(current, [])
            continue
        if current is not None:
            sections[current].append(line)
    return {name: "\n".join(lines) for name, lines in sections.items()}


def _digest(text: str) -> str:
    full = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return FINGERPRINT_PREFIX + full[:FINGERPRINT_DIGITS]


def contracts_fingerprint(node: Node) -> str:
    """Hash the enforceable commitments: contract id, text, enforcer and reason.

    Sorted by contract id, so reordering the front matter does not invalidate a claim.
    """
    rows = sorted(node.contracts, key=lambda contract: contract.id)
    canonical = "\n".join(
        f"{item.id}|{item.text}|{item.enforced_by}|{item.reason or ''}" for item in rows
    )
    return _digest(canonical)


def meaning_fingerprint(node: Node) -> str:
    """Hash the wording of the meaning, plus the two edges that define the node's place.

    Deliberately excludes ``slug``, ``title``, ``status``, ``code_paths``, ``test_paths``,
    ``talks_to`` and open questions: renaming a node or moving its files is not a change
    of what it commits to.
    """
    sections = body_sections(node)
    parts = [f"## {name}\n{_normalise(sections.get(name, ''))}" for name in MEANING_SECTIONS]
    parts.append(f"parent:{node.parent or ''}")
    parts.append("uses:" + ",".join(sorted(node.uses)))
    return _digest("\n".join(parts))


def is_fingerprint(value: str) -> bool:
    if not value.startswith(FINGERPRINT_PREFIX):
        return False
    digits = value[len(FINGERPRINT_PREFIX) :]
    return len(digits) == FINGERPRINT_DIGITS and all(char in "0123456789abcdef" for char in digits)


# --------------------------------------------------------------------------- stored layer


@dataclass
class Claim:
    """Someone's assertion that a node's contracts hold, and against which wording."""

    evidence: str
    by: str
    contracts: str
    meaning: str
    affirmed_by: str | None = None
    affirm_reason: str | None = None

    def to_mapping(self) -> dict[str, object]:
        data: dict[str, object] = {
            "evidence": self.evidence,
            "by": self.by,
            "contracts": self.contracts,
            "meaning": self.meaning,
        }
        if self.affirmed_by:
            data["affirmed_by"] = self.affirmed_by
        if self.affirm_reason:
            data["affirm_reason"] = self.affirm_reason
        return data


@dataclass
class Acceptance:
    """A human decision about a claim, tied to the wording it was made against."""

    decision: str
    by: str
    contracts: str
    meaning: str
    note: str | None = None

    def to_mapping(self) -> dict[str, object]:
        data: dict[str, object] = {"decision": self.decision, "by": self.by}
        if self.note:
            data["note"] = self.note
        data["contracts"] = self.contracts
        data["meaning"] = self.meaning
        return data


@dataclass
class Entry:
    claim: Claim | None = None
    acceptance: Acceptance | None = None


@dataclass
class Layer:
    entries: dict[str, Entry]
    source: Path

    def entry(self, node_id: str) -> Entry:
        return self.entries.setdefault(node_id, Entry())

    def claim_of(self, node_id: str) -> Claim | None:
        found = self.entries.get(node_id)
        return found.claim if found else None

    def acceptance_of(self, node_id: str) -> Acceptance | None:
        found = self.entries.get(node_id)
        return found.acceptance if found else None


def _as_mapping(value: object, where: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise TreeError(f"{where} must be a mapping")
    return value


def _text(mapping: dict[str, object], key: str) -> str:
    value = mapping.get(key)
    return "" if value is None else str(value)


def _optional(mapping: dict[str, object], key: str) -> str | None:
    value = mapping.get(key)
    return None if value is None else str(value)


def load_layer(intent_dir: Path) -> Layer:
    """Read the stored layer; a missing file means nothing has ever been claimed."""
    path = intent_dir / REALIZATION_FILENAME
    if not path.exists():
        return Layer({}, path)
    try:
        data = parse(path.read_text(encoding="utf-8"))
    except YamlError as exc:
        raise TreeError(f"{path}: {exc}") from exc

    version = data.get("schema_version")
    if version != SCHEMA_VERSION:
        raise TreeError(
            f"{path}: unsupported schema_version {version!r}, expected {SCHEMA_VERSION}"
        )

    entries: dict[str, Entry] = {}
    for node_id, raw in _as_mapping(data.get("nodes") or {}, f"{path}: 'nodes'").items():
        body = _as_mapping(raw, f"{path}: entry {node_id}")
        entry = Entry()
        if body.get("claim") is not None:
            claim = _as_mapping(body["claim"], f"{path}: {node_id} claim")
            entry.claim = Claim(
                evidence=_text(claim, "evidence"),
                by=_text(claim, "by"),
                contracts=_text(claim, "contracts"),
                meaning=_text(claim, "meaning"),
                affirmed_by=_optional(claim, "affirmed_by"),
                affirm_reason=_optional(claim, "affirm_reason"),
            )
        if body.get("acceptance") is not None:
            acceptance = _as_mapping(body["acceptance"], f"{path}: {node_id} acceptance")
            entry.acceptance = Acceptance(
                decision=_text(acceptance, "decision"),
                by=_text(acceptance, "by"),
                contracts=_text(acceptance, "contracts"),
                meaning=_text(acceptance, "meaning"),
                note=_optional(acceptance, "note"),
            )
        entries[str(node_id)] = entry
    return Layer(entries, path)


def save_layer(layer: Layer) -> None:
    """Write the layer back, node ids sorted so diffs stay readable."""
    nodes: dict[str, object] = {}
    for node_id in sorted(layer.entries):
        entry = layer.entries[node_id]
        mapping: dict[str, object] = {}
        if entry.claim is not None:
            mapping["claim"] = entry.claim.to_mapping()
        if entry.acceptance is not None:
            mapping["acceptance"] = entry.acceptance.to_mapping()
        if mapping:
            nodes[node_id] = mapping
    payload: dict[str, object] = {"schema_version": SCHEMA_VERSION, "nodes": nodes}
    layer.source.parent.mkdir(parents=True, exist_ok=True)
    layer.source.write_text(dump(payload), encoding="utf-8")


# --------------------------------------------------------------------------- policy


@dataclass
class Policy:
    """When a human must sign off and what counts as evidence."""

    acceptance_profile: str = "standard"
    evidence_profile: str = "standard"

    def requires_acceptance(self, node: Node) -> bool:
        if self.acceptance_profile == "none":
            return False
        if self.acceptance_profile == "strict":
            return True
        if any(contract.enforced_by == "review" for contract in node.contracts):
            return True
        return self.acceptance_profile == "leaf" and bool(node.code_paths)


def load_policy(intent_dir: Path) -> Policy:
    path = intent_dir / POLICY_FILENAME
    if not path.exists():
        return Policy()
    try:
        data = parse(path.read_text(encoding="utf-8"))
    except YamlError as exc:
        raise TreeError(f"{path}: {exc}") from exc
    policy = Policy(
        acceptance_profile=str(data.get("acceptance_profile") or "standard"),
        evidence_profile=str(data.get("evidence_profile") or "standard"),
    )
    if policy.acceptance_profile not in ACCEPTANCE_PROFILES:
        raise TreeError(f"{path}: acceptance_profile must be one of {ACCEPTANCE_PROFILES}")
    if policy.evidence_profile not in EVIDENCE_PROFILES:
        raise TreeError(f"{path}: evidence_profile must be one of {EVIDENCE_PROFILES}")
    return policy


# --------------------------------------------------------------------------- derived state


@dataclass
class NodeState:
    """The computed answer for one node. Nothing here is ever written to disk."""

    node: str
    state: str  # realized | stale | broken | rejected | not_claimed
    acceptance: str  # not_required | pending | approved | rejected
    reasons: list[str] = field(default_factory=list)
    blocked_by: str | None = None

    def needs_work(self) -> bool:
        return self.state != "realized" or self.acceptance in ("pending", "rejected")

    def summary(self) -> str:
        text = self.state
        if self.reasons:
            text += " [" + "; ".join(self.reasons) + "]"
        if self.acceptance != "not_required":
            text += f", acceptance {self.acceptance}"
        return text


def missing_enforcers(tree: Tree, node: Node) -> list[str]:
    """Contract ids whose enforcer cannot be found — the static half of 'broken'."""
    return [item.id for item in node.contracts if enforcer_problem(tree, item)]


def _acceptance_state(
    acceptance: Acceptance | None, contracts: str, meaning: str, required: bool
) -> str:
    unchanged = (
        acceptance is not None
        and acceptance.contracts == contracts
        and acceptance.meaning == meaning
    )
    if unchanged and acceptance is not None:
        return acceptance.decision
    return "pending" if required else "not_required"


def compute_states(
    tree: Tree, layer: Layer | None = None, policy: Policy | None = None
) -> dict[str, NodeState]:
    """Derive the state of every ``current`` node from the tree and the stored claims.

    Invalidation follows a change of **wording**, never a state: a node whose text moved
    opens its subtree (and, for contracts, its direct ``uses`` consumers). A node that is
    merely unproven blocks nothing — otherwise an unproven root would forbid proving
    anything below it, and adoption would have to start at the least provable node.
    """
    layer = load_layer(tree.intent_dir) if layer is None else layer
    policy = load_policy(tree.intent_dir) if policy is None else policy

    current = {node_id: node for node_id, node in tree.nodes.items() if node.status == "current"}
    contracts_now = {node_id: contracts_fingerprint(node) for node_id, node in current.items()}
    meaning_now = {node_id: meaning_fingerprint(node) for node_id, node in current.items()}

    moved_contracts: set[str] = set()
    moved_meaning: set[str] = set()
    for node_id in current:
        claim = layer.claim_of(node_id)
        if claim is None:
            continue
        if claim.contracts != contracts_now[node_id]:
            moved_contracts.add(node_id)
        if claim.meaning != meaning_now[node_id]:
            moved_meaning.add(node_id)

    states: dict[str, NodeState] = {}
    for node_id, node in current.items():
        claim = layer.claim_of(node_id)
        acceptance = _acceptance_state(
            layer.acceptance_of(node_id),
            contracts_now[node_id],
            meaning_now[node_id],
            policy.requires_acceptance(node),
        )
        broken = missing_enforcers(tree, node)
        reasons: list[str] = []
        blocked_by: str | None = None

        if claim is None:
            state = "not_claimed"
            if broken:
                reasons.append("enforcer missing: " + ", ".join(broken))
        else:
            if node_id in moved_contracts:
                reasons.append("own contracts changed")
            if node_id in moved_meaning:
                reasons.append("own meaning changed")
            for ancestor in tree.ancestors(node_id):
                changed = _changed_part(ancestor.id, moved_contracts, moved_meaning)
                if changed:
                    reasons.append(f"ancestor {ancestor.id} changed {changed}")
                    blocked_by = blocked_by or ancestor.id
            for target in sorted(node.uses):
                if target in moved_contracts:
                    reasons.append(f"used {target} changed contracts")
            stale = bool(reasons)
            if broken:
                reasons.append("enforcer missing: " + ", ".join(broken))
            if stale:
                state = "stale"
            elif broken:
                state = "broken"
            elif acceptance == "rejected":
                state = "rejected"
            else:
                state = "realized"

        states[node_id] = NodeState(node_id, state, acceptance, reasons, blocked_by)
    return states


def _changed_part(node_id: str, moved_contracts: set[str], moved_meaning: set[str]) -> str | None:
    parts = []
    if node_id in moved_contracts:
        parts.append("contracts")
    if node_id in moved_meaning:
        parts.append("meaning")
    return " and ".join(parts) if parts else None


def build_worklist(tree: Tree, states: dict[str, NodeState]) -> list[NodeState]:
    """Everything that still needs work, ancestors first so the order is workable."""
    pending = [state for state in states.values() if state.needs_work()]
    return sorted(pending, key=lambda item: (tree.depth_of(item.node), item.node))


def summarise(states: dict[str, NodeState]) -> dict[str, int]:
    counts = {
        "nodes": len(states),
        "realized": 0,
        "stale": 0,
        "broken": 0,
        "rejected": 0,
        "not_claimed": 0,
        "acceptance_required": 0,
        "acceptance_approved": 0,
        "acceptance_pending": 0,
    }
    for state in states.values():
        counts[state.state] += 1
        if state.acceptance != "not_required":
            counts["acceptance_required"] += 1
        if state.acceptance == "approved":
            counts["acceptance_approved"] += 1
        elif state.acceptance == "pending":
            counts["acceptance_pending"] += 1
    return counts


# --------------------------------------------------------------------------- consistency


def check_layer(tree: Tree, layer: Layer, policy: Policy) -> list[str]:
    """Rules R1-R7 over the stored layer.

    This checks that the layer is internally consistent, **not** that the project is
    realized. An unfinished project is the normal state; an inconsistent layer is a bug.
    """
    problems: list[str] = []
    for node_id in sorted(layer.entries):
        entry = layer.entries[node_id]
        node = tree.nodes.get(node_id)
        if node is None:
            problems.append(f"R1 {node_id}: no such node in the tree")
            continue
        if node.status != "current":
            problems.append(f"R1 {node_id}: status is '{node.status}', not 'current'")

        claim = entry.claim
        if claim is not None:
            if not claim.evidence:
                problems.append(f"R2 {node_id}: claim without evidence")
            if not claim.by:
                problems.append(f"R2 {node_id}: claim without 'by'")
            for label, value in (("contracts", claim.contracts), ("meaning", claim.meaning)):
                if not is_fingerprint(value):
                    problems.append(f"R7 {node_id}: claim has a malformed {label} fingerprint")
            problems.extend(_evidence_problems(tree, node_id, claim.evidence, policy))
            if claim.by.strip().lower() == "coder":
                problems.append(f"R6 {node_id}: a claim may not be written by the Coder")
            if claim.affirmed_by and claim.affirmed_by.strip().lower() in AGENT_ROLES:
                problems.append(f"R5 {node_id}: affirmation signed by an agent role")

        acceptance = entry.acceptance
        if acceptance is not None:
            if acceptance.decision not in ACCEPTANCE_DECISIONS:
                problems.append(f"R4 {node_id}: decision must be approved or rejected")
            if not acceptance.by:
                problems.append(f"R4 {node_id}: acceptance without 'by'")
            elif acceptance.by.strip().lower() in AGENT_ROLES:
                problems.append(f"R5 {node_id}: acceptance signed by an agent role")
            if claim is None:
                problems.append(f"R4 {node_id}: acceptance without a claim to accept")
            for label, value in (
                ("contracts", acceptance.contracts),
                ("meaning", acceptance.meaning),
            ):
                if not is_fingerprint(value):
                    problems.append(f"R7 {node_id}: acceptance has a malformed {label} fingerprint")
    return problems


def _evidence_problems(tree: Tree, node_id: str, evidence: str, policy: Policy) -> list[str]:
    if not evidence:
        return []
    target = tree.root_dir / evidence
    if not target.exists():
        return [f"R3 {node_id}: evidence {evidence} does not exist"]
    if policy.evidence_profile != "standard":
        return []
    if not target.is_dir() or not (target / GRADER_FILENAME).exists():
        return [
            f"R3 {node_id}: evidence {evidence} is not a run directory with {GRADER_FILENAME} "
            "(evidence_profile: standard)"
        ]
    return []


# --------------------------------------------------------------------------- mutations


def _require_current(tree: Tree, node_id: str) -> Node:
    node = tree.nodes.get(node_id)
    if node is None:
        raise TreeError(f"node {node_id} does not exist")
    if node.status != "current":
        raise TreeError(f"node {node_id} is '{node.status}'; only current nodes carry a claim")
    return node


def _require_human(who: str, action: str) -> None:
    if not who.strip():
        raise TreeError(f"{action} requires --by")
    if who.strip().lower() in AGENT_ROLES:
        raise TreeError(f"{action} is a human decision; '{who}' is an agent role")


def claim(
    tree: Tree, layer: Layer, policy: Policy, node_id: str, evidence: str, by: str
) -> NodeState:
    """Record that the node's contracts hold, against the wording they hold for now."""
    node = _require_current(tree, node_id)
    if not by.strip():
        raise TreeError("claim requires --by")
    if by.strip().lower() == "coder":
        raise TreeError(
            "the Coder may not claim its own work; "
            "the Coordinator claims once every gate the level requires has passed"
        )
    if node.open_questions:
        raise TreeError(
            f"{node_id} has {len(node.open_questions)} open question(s); "
            "an open question blocks implementation, so it also blocks a claim"
        )
    broken = missing_enforcers(tree, node)
    if broken:
        raise TreeError(f"{node_id}: contract(s) {', '.join(broken)} have no reachable enforcer")
    problems = _evidence_problems(tree, node_id, evidence, policy)
    if not evidence.strip():
        problems.append(f"R2 {node_id}: claim without evidence")
    if problems:
        raise TreeError("; ".join(problems))

    entry = layer.entry(node_id)
    entry.claim = Claim(
        evidence=evidence,
        by=by,
        contracts=contracts_fingerprint(node),
        meaning=meaning_fingerprint(node),
    )
    return compute_states(tree, layer, policy)[node_id]


def affirm(
    tree: Tree, layer: Layer, policy: Policy, node_id: str, by: str, reason: str, subtree: bool
) -> list[str]:
    """Re-point existing claims at the current wording, without new evidence.

    Only a human may do this: deciding that a text change did not invalidate a proof is a
    judgement, not a computation. ``subtree`` exists so one harmless edit high in the tree
    does not cost dozens of separate decisions.
    """
    _require_human(by, "affirm")
    if not reason.strip():
        raise TreeError("affirm requires --reason: it is the only record of the judgement")
    _require_current(tree, node_id)

    targets = [node_id]
    if subtree:
        targets.extend(_descendants(tree, node_id))

    touched: list[str] = []
    for target in targets:
        node = tree.nodes.get(target)
        claim_record = layer.claim_of(target)
        if node is None or node.status != "current" or claim_record is None:
            continue
        claim_record.contracts = contracts_fingerprint(node)
        claim_record.meaning = meaning_fingerprint(node)
        claim_record.affirmed_by = by
        claim_record.affirm_reason = reason
        touched.append(target)
    if not touched:
        raise TreeError(f"{node_id}: nothing to affirm — no claim exists yet")
    return touched


def _descendants(tree: Tree, node_id: str) -> list[str]:
    found: list[str] = []
    queue = [node_id]
    while queue:
        current = queue.pop()
        for child in tree.children_of(current):
            found.append(child.id)
            queue.append(child.id)
    return sorted(found)


def decide(
    tree: Tree, layer: Layer, node_id: str, decision: str, by: str, note: str | None
) -> NodeState:
    """Record the human verdict on a claim."""
    if decision not in ACCEPTANCE_DECISIONS:
        raise TreeError(f"decision must be one of {ACCEPTANCE_DECISIONS}")
    _require_human(by, decision)
    node = _require_current(tree, node_id)
    if layer.claim_of(node_id) is None:
        raise TreeError(f"{node_id}: nothing to {decision} — no claim exists yet")
    if decision == "rejected" and not (note or "").strip():
        raise TreeError("a rejection requires --note saying what is wrong")

    entry = layer.entry(node_id)
    entry.acceptance = Acceptance(
        decision=decision,
        by=by,
        contracts=contracts_fingerprint(node),
        meaning=meaning_fingerprint(node),
        note=note,
    )
    return compute_states(tree, layer)[node_id]


def prune(tree: Tree, layer: Layer) -> list[str]:
    """Drop entries for nodes that are no longer current; git keeps the history."""
    removed = [
        node_id
        for node_id in sorted(layer.entries)
        if node_id not in tree.nodes or tree.nodes[node_id].status != "current"
    ]
    for node_id in removed:
        del layer.entries[node_id]
    return removed


# --------------------------------------------------------------------------- rendering


def render_states(tree: Tree, states: dict[str, NodeState]) -> str:
    lines = []
    for node_id in sorted(states, key=lambda item: (tree.depth_of(item), item)):
        state = states[node_id]
        node = tree.nodes[node_id]
        lines.append(f"{node_id}  {state.summary()}")
        lines.append(f"        {node.title}")
    return "\n".join(lines) + "\n" if lines else "no current nodes\n"


def render_worklist(tree: Tree, states: dict[str, NodeState]) -> str:
    items = build_worklist(tree, states)
    if not items:
        every = len(states)
        return f"worklist empty — all {every} current node(s) realized and accepted\n"
    lines = []
    for state in items:
        marker = f"blocked_by {state.blocked_by}" if state.blocked_by else "ready"
        lines.append(f"{state.node}  {state.summary():<58} {marker}")
        lines.append(f"        {tree.nodes[state.node].title}")
    lines.append("")
    lines.append("Work top down: a node blocked by an ancestor waits for that ancestor.")
    return "\n".join(lines) + "\n"


def render_summary(states: dict[str, NodeState]) -> str:
    counts = summarise(states)
    total = counts["nodes"] or 1
    share = 100 * counts["realized"] // total
    lines = [
        f"{counts['nodes']} current node(s), {counts['realized']} realized ({share}%)",
        f"  stale        {counts['stale']}",
        f"  broken       {counts['broken']}",
        f"  rejected     {counts['rejected']}",
        f"  not claimed  {counts['not_claimed']}",
        f"acceptance: {counts['acceptance_required']} required, "
        f"{counts['acceptance_approved']} approved, {counts['acceptance_pending']} pending",
    ]
    return "\n".join(lines) + "\n"
