# Agent Models — Default Configuration
<!-- cs: Výchozí konfigurace modelů pro role -->

Default role → model assignments shipped with the template. A consuming project
overrides this file **in full** by creating `doc/apm_config/AGENT_MODELS.user.md` — see
the Config Resolution mechanism in `rules/200-project-design-rules.mdc`.
<!-- cs: Výchozí přiřazení rolí a modelů dodávané se šablonou. Spotřebitelský projekt
     tento soubor ZCELA přepíše vytvořením doc/apm_config/AGENT_MODELS.user.md — viz
     Config Resolution mechanismus v rules/200-project-design-rules.mdc. -->

## Bands — project-specific hard triggers for `high`
<!-- cs: Pásma — projektově specifické tvrdé spouštěče pro high -->

Band definition, granularity, and escalation are a fixed mechanism in
`rules/000-model-policy.mdc`. List here only triggers **specific to this project** (the
generic ones in that rule always apply, in addition to these):
<!-- cs: Definice pásem, granularita a eskalace jsou pevný mechanismus v
     rules/000-model-policy.mdc. Sem patří jen spouštěče specifické pro tento projekt
     (obecné z pravidla platí navíc k nim): -->

- *(none by default — add project risk areas here, e.g. "billing/payment code paths",
  "data-retention deletion logic")*

## Active Role Assignments
<!-- cs: Aktivní přiřazení rolí -->

| Role | `low` | `medium` | `high` |
|---|---|---|---|
| Planner | — | `unassigned` | `unassigned` |
| Coder | `unassigned` | `unassigned` | `unassigned` |
| Reviewer | `unassigned` | `unassigned` | `unassigned` |

`unassigned` means the agent **must ask** the Human before acting in that role. `—` for
Planner `low` is expected: Planner is banded per Epic (`rules/000-model-policy.mdc`), and
an Epic made only of `low` Tasks does not occur — use `medium` if it ever does.
Edit via `/role-assign`, or by hand — see `rules/000-model-policy.mdc` for the resolution
rule.
<!-- cs: `unassigned` znamená, že se agent MUSÍ zeptat Humana, než začne v té roli
     pracovat. `—` u Planner low je záměrné: Planner má pásmo za epiku, epika jen z low
     tasků nenastává — použij medium. Uprav přes /role-assign, nebo ručně — viz
     rules/000-model-policy.mdc pro pravidlo rozlišení. -->
