# Agent Models — default catalog

Default model assignment for the ICE roles. When this rule set is mounted as a submodule,
this file is `.cursor/AGENT_MODELS.md` and is **read-only** for the project: editing it
changes every project that uses the template.

To change models for one project, create `AGENT_MODELS.md` in that **project root** and
restate only the roles you want to override. Resolution and constraints are defined in
`rules/00-model-policy.mdc`.

Cursor does not auto-switch the parent chat's model. For a subagent, the Coordinator
passes the chosen slug; for the parent window, it reminds the Human to select it.

```yaml
schema_version: 1
updated: 2026-08-15
authority: Human
coordinator_may_select: true
# A role with lock: true uses `pinned` and does not vary by complexity.

roles:
  Coordinator:
    intent: orchestration, strong reasoning, no production code
    lock: false
    pinned: null
    low: composer-2.5
    medium: claude-sonnet-5-thinking-high
    high: claude-opus-5-thinking-high

  Planner:
    intent: decomposition, intent deltas, slices
    lock: false
    pinned: null
    low: claude-sonnet-5-thinking-high
    medium: claude-sonnet-5-thinking-high
    high: claude-opus-5-thinking-high

  Critic:
    intent: adversarial reading of plans and intent nodes
    lock: false
    pinned: null
    low: claude-sonnet-5-thinking-high
    medium: claude-opus-5-thinking-high
    high: claude-opus-5-thinking-high

  Coder:
    intent: implementation and tests; cheaper model unless complexity is high
    lock: false
    pinned: null
    low: composer-2.5
    medium: composer-2.5
    high: claude-sonnet-5-thinking-high

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

Note on the defaults above: at `low` the Critic and the Planner share a model, which the
`critic_differs_from_planner` constraint asks you to avoid. `low` runs do not run a
Critic at all (see `rules/07-ice-workflow.mdc`), so the row is only a fallback — but if
you start using a Critic at `low`, change one of the two.

The slugs are a snapshot for August 2026. Replace them when the model list in Cursor
changes; the methodology never hardcodes them.
