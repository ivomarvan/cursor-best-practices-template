# Agent Models — Default Configuration
<!-- cs: Výchozí konfigurace modelů pro role -->

Default role → model assignments shipped with the template. A consuming project
overrides this file **in full** by creating `doc/apm_config/AGENT_MODELS.user.md` — see
the Config Resolution mechanism in `rules/20-project-design-rules.mdc`.
<!-- cs: Výchozí přiřazení rolí a modelů dodávané se šablonou. Spotřebitelský projekt
     tento soubor ZCELA přepíše vytvořením doc/apm_config/AGENT_MODELS.user.md — viz
     Config Resolution mechanismus v rules/20-project-design-rules.mdc. -->

## Active Role Assignments
<!-- cs: Aktivní přiřazení rolí -->

| Role | Assigned model | Updated |
|---|----|---|
| Planner | `unassigned` | — |
| Coder | `unassigned` | — |
| Reviewer | `unassigned` | — |

`unassigned` means the agent **must ask** the Human before acting in that role. Edit via
`/role-assign`, or by hand — see `rules/00-model-policy.mdc` for the resolution rule.
<!-- cs: `unassigned` znamená, že se agent MUSÍ zeptat Humana, než začne v té roli
     pracovat. Uprav přes /role-assign, nebo ručně — viz rules/00-model-policy.mdc pro
     pravidlo rozlišení. -->
