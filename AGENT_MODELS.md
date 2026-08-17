# Agent Models — default catalog

Default model assignment for the ICE roles. When this rule set is mounted as a submodule,
this file is `.cursor/AGENT_MODELS.md` and is **read-only** for the project: editing it
changes every project that uses the template.

To change models for one project, create `AGENT_MODELS.md` in that **project root** and
restate only the roles you want to override. Resolution and constraints are defined in
`rules/00-model-policy.mdc`.

Why these slugs were chosen: see `AGENT_MODELS.explanation.md` in this directory
(snapshot 2026-08-17). Evidence: `doc/cursor_models/`.

Cursor does not auto-switch the parent chat's model. For a subagent, the Coordinator
passes the chosen slug; for the parent window, it reminds the Human to select it.
The Human's UI selection is authoritative for the role the parent window is playing;
catalog slugs apply to delegated subagents.

```yaml
schema_version: 1
updated: 2026-08-17
authority: Human
coordinator_may_select: true
# A role with lock: true uses `pinned` and does not vary by complexity.

roles:
  Coordinator:
    intent: orchestration, strong reasoning, no production code
    lock: false
    pinned: null
    low: composer-2.5
    medium: cursor-grok-4.6-medium
    high: claude-opus-5-thinking-high

  Planner:
    intent: decomposition, intent deltas, slices
    lock: false
    pinned: null
    low: cursor-grok-4.6-medium
    medium: cursor-grok-4.6-medium
    high: claude-opus-5-thinking-high

  Critic:
    intent: adversarial reading of plans and intent nodes
    lock: false
    pinned: null
    low: claude-sonnet-5-thinking-high
    medium: claude-sonnet-5-thinking-high
    high: cursor-grok-4.5-high

  Coder:
    intent: implementation and tests; cheaper model unless complexity is high
    lock: false
    pinned: null
    low: composer-2.5
    medium: cursor-grok-4.6-medium
    high: cursor-grok-4.5-high

  Adversary:
    intent: independent review of the diff and the Definition of Done
    lock: false
    pinned: null
    low: claude-sonnet-5-thinking-high
    medium: claude-sonnet-5-thinking-high
    high: claude-opus-5-thinking-high

constraints:
  adversary_differs_from_coder: true
  critic_differs_from_planner: true
  grader_is_not_an_llm: true
```

Constraint check (Planner ≠ Critic, Coder ≠ Adversary in every band):

| Band | Planner | Critic | Coder | Adversary |
|------|---------|--------|-------|-----------|
| `low` | Grok 4.6 | Sonnet 5 (gate unused) | Composer 2.5 | Sonnet 5 (gate unused) |
| `medium` | Grok 4.6 | Sonnet 5 | Grok 4.6 | Sonnet 5 |
| `high` | Opus 5 | Grok 4.5 | Grok 4.5 | Opus 5 |

`low` Critic and Adversary rows are fallbacks: `low` runs do not run those gates
(see `rules/07-ice-workflow.mdc`). A scope-guard failure raises the run to `medium`
and those roles then take the medium slugs.

The slugs are a snapshot for 17 August 2026. Replace them when the model list in
Cursor changes; the methodology never hardcodes them.
