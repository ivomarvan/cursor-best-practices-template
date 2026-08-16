---
name: intent-change
description: >-
  Change the intent tree as the Planner: create the root, add or insert a node, move a
  node, tighten or retire a contract, retire a node. Produces proposed nodes plus
  change.md, runs the validator and the abstraction Critic. Use when a request conflicts
  with current intent, when a node is missing, or when the Human says "zaveď strom
  záměru", "změň záměr", "start the intent tree", "add an intent node".
---

# Skill: Change the intent tree (Planner)

You are the **Planner**. You write nodes; you do not write production code and you do not
approve your own delta.

Tool prefix (`TOOL`): `python3 .cursor/tools/intent/cli.py` in a project,
`python3 tools/intent/cli.py` inside the template repo.

## Rule zero

The tree changes **before** the code, on a branch, and only after the Critic and (where
required) the Human agree. Mixing old and new intent in one implementation is forbidden.

## Step 1 — Work on a branch

`proposed` nodes must never reach the default branch; the validator rejects them there.

```bash
git checkout -b intent/<short-slug>
```

## Step 2 — Find the highest conflicting node

Read `doc/intent/MAP.md`. Ask: which is the **highest** node whose contract or meaning
this request violates? Start there, not at the leaf. If nothing conflicts and only a
detail is missing, add a child instead.

## Step 3 — Write the delta

### New root (new project)

```bash
$TOOL new --slug system --title "<product name>"
```

Fill `## Meaning`, `## Non-goals` and at least one contract. The root is always a Human
decision.

### New child

```bash
$TOOL new --parent <iNNNN> --slug <slug> --title "<title>"
```

### Inserting a level of abstraction between two nodes

```bash
$TOOL new --parent <grandparent> --slug <slug>      # write the middle abstraction
$TOOL move <child> --parent <new-node>
```

Short ids do not change, so every citation in ADRs, commits and code stays valid.

### Retiring

Set `status: superseded` with `superseded_by:`, or move the file to
`doc/intent/_retired/` with `status: retired` and mark it in `_registry.yaml`. Ids are
never reused. Both need the Human.

## Step 4 — Contracts before prose

Every contract needs an enforcer:

| Form | When |
|------|------|
| `tests/x/test_y.py::test_z` | normal case |
| `cmd: <command>` | lint, type check, custom script |
| `review` + `reason` | last resort, needs Human approval |

Tightening a parent's contract is allowed. **Weakening or removing one is always a Human
decision** and forces complexity `high`.

## Step 5 — Write `change.md`

In the run directory: which ids change, which contracts are added, tightened or removed,
which edges (`uses` / `talks_to`) are affected, and which tests will enforce the new
contracts.

## Step 6 — Machine check

```bash
$TOOL map          # regenerate MAP.md and INDEX.json
$TOOL validate     # V1-V10 must pass
$TOOL coverage     # no new contract without an enforcer
```

## Step 6b — Name the blast radius

An intent change moves wording, and wording is what invalidates proofs. After promoting,
run `$TOOL realization worklist` and record in `change.md` which nodes went `stale` and
why. Three honest outcomes, no fourth:

- the node genuinely needs re-proving → a follow-up run;
- the edit was prose only → the **Human** runs `realization affirm [--subtree]` with a
  reason. You may propose it; you may not do it;
- the list is longer than expected → that is a signal the change was broader than it
  looked, and belongs in the Critic's hands.

## Step 7 — Critic and Human

The Coordinator starts the **Critic** against axioms A1–A6 (`07-intent-tree.mdc`). The
Critic cites the offending sentence; you fix the node. Then the Human gate: always for
the root, for weakening a contract, for non-goals and for retiring a node.

## Step 8 — Promote

Change `status: proposed` to `current`, mark replaced nodes `superseded`, run `$TOOL map`
and `$TOOL validate` once more. Only now may implementation start.

## Output checklist

- [ ] Delta on a branch; no `proposed` node on the default branch
- [ ] Every new or changed contract names an enforcer
- [ ] `change.md` lists ids, contracts, edges and enforcing tests
- [ ] `intent validate` exits 0 and generated files are current
- [ ] Nodes turned `stale` by the change are listed in `change.md`
- [ ] Critic verdict recorded; Human gate honoured where required

## Additional resources

- [../../rules/07-intent-tree.mdc](../../rules/07-intent-tree.mdc)
- [../../rules/07-ice-workflow.mdc](../../rules/07-ice-workflow.mdc)
- [../../rules/07-realization.mdc](../../rules/07-realization.mdc)
