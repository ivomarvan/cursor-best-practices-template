---
run_id: 20260816-1302-realization-layer-91
intent_ids: ["i0004"]
role: Coder
model: claude-opus-5-thinking-high
complexity: high
status: done
---

# CLI evidence for the write commands

The unit suite calls the module functions directly, so it does not prove the argparse
layer is wired correctly. The Adversary was right that the Definition of Done item
"write commands verified through the CLI" had no artifact behind it. This is it.

A throwaway two-node tree in `/tmp/ice-cli-evidence`, driven only through
`python3 tools/intent/cli.py --root <dir>`. Every block below is unedited output.

## $ intent realization worklist

```
i0001  not_claimed                                                ready
        Demo system
i0002  not_claimed                                                ready
        Engine

Work top down: a node blocked by an ancestor waits for that ancestor.
```

exit code: 0

## $ intent realization claim i0002 --evidence doc/runs/20260816-1200-demo --by Coder

```
intent: the Coder may not claim its own work; the Coordinator claims after the Grader
```

exit code: 2

## $ intent realization claim i0002 --evidence doc/runs/20260816-1200-demo --by Coordinator

```
i0002 claimed against doc/runs/20260816-1200-demo — now realized
```

exit code: 0

## The ancestor meaning is now rewritten, twice, by hand

## $ intent realization worklist

```
i0001  stale [own meaning changed]                                ready
        Demo system
i0002  stale [ancestor i0001 changed meaning]                     blocked_by i0001
        Engine

Work top down: a node blocked by an ancestor waits for that ancestor.
```

exit code: 0

## $ intent realization affirm i0001 --subtree --by Coordinator --reason 'prose only'

```
intent: affirm is a human decision; 'Coordinator' is an agent role
```

exit code: 2

## $ intent realization affirm i0001 --subtree --by ivo --reason 'prose only, contracts untouched'

```
affirmed 2 claim(s): i0001, i0002
The evidence was not re-run; only its wording baseline moved.
```

exit code: 0

## $ intent realization summary

```
2 current node(s), 2 realized (100%)
  stale        0
  broken       0
  rejected     0
  not claimed  0
acceptance: 0 required, 0 approved, 0 pending
```

exit code: 0

## $ intent realization accept i0002 --reject --by ivo --note 'the test proves nothing'

```
i0002 rejected by ivo — now rejected, acceptance rejected
```

exit code: 0

## $ intent realization status --node i0002

```
i0002  rejected, acceptance rejected
        Engine
```

exit code: 0

## $ intent realization accept i0002 --by ivo --note 'fixed'

```
i0002 approved by ivo — now realized, acceptance approved
```

exit code: 0

## $ intent realization status --node i0002

```
i0002  realized, acceptance approved
        Engine
```

exit code: 0

## The enforcer of i0002 is now pointed at a test that does not exist

## $ intent realization status --node i0002

```
i0002  stale [own contracts changed; enforcer missing: c1]
        Engine
```

exit code: 0

## $ intent realization check

```
realization layer consistent (2 entry/entries)
```

exit code: 0

## The stored layer, in full

```yaml
schema_version: 1
nodes:
  i0001:
    claim:
      evidence: doc/runs/20260816-1200-demo
      by: Coordinator
      contracts: sha256:e3b0c44298fc1c14
      meaning: sha256:78063e92e650288c
      affirmed_by: ivo
      affirm_reason: prose only, contracts untouched
  i0002:
    claim:
      evidence: doc/runs/20260816-1200-demo
      by: Coordinator
      contracts: sha256:4b283c98259f5e7d
      meaning: sha256:615a9d696f52f9f4
      affirmed_by: ivo
      affirm_reason: prose only, contracts untouched
    acceptance:
      decision: approved
      by: ivo
      note: fixed
      contracts: sha256:4b283c98259f5e7d
      meaning: sha256:615a9d696f52f9f4
```

## A second tree: what happens to a claim when its node leaves

`i0002` is claimed, then its node file is deleted from the tree.

### $ intent realization summary

```
2 current node(s), 1 realized (50%)
  stale        0
  broken       0
  rejected     0
  not claimed  1
acceptance: 0 required, 0 approved, 0 pending
```

exit code: 0

The file `i0002-engine.md` is now deleted.

### $ intent map

```
updated doc/intent/MAP.md
updated doc/intent/INDEX.json
```

exit code: 0

### $ intent realization check

```
ERROR R1 i0002: no such node in the tree

1 realization layer violation(s)
```

exit code: 1

### $ intent realization prune

```
removed 1 entry/entries: i0002
```

exit code: 0

### $ intent realization check

```
realization layer consistent (0 entry/entries)
```

exit code: 0

## What this shows

- The Coder is refused and the Coordinator is not (`c12`).
- An agent is refused as the signer of a human judgement (`c13`).
- An edited ancestor turns its subtree `stale` and marks the child `blocked_by`.
- `affirm --subtree` re-points both claims at the new wording without new evidence.
- A rejection survives as a state; a later acceptance clears it.
- A vanished enforcer shows as `enforcer missing`, and the reasons stack.
- Only fingerprints, evidence and signatures are ever stored — no derived state.

- `prune` drops the entry only after the node itself is gone, and `check` names the
  orphan before that (`R1`) instead of silently tidying it away.

- `prune` drops the entry only after the node itself is gone, and `check` names the
  orphan before that (`R1`) instead of silently tidying it away.
