# Design Rules — Default Configuration
<!-- cs: Výchozí konfigurace projektových pravidel návrhu -->

No project-specific design invariants are defined by default. A consuming project
overrides this file **in full** by creating `doc/apm_config/DESIGN_RULES.user.md` — see
the Config Resolution mechanism in `rules/20-project-design-rules.mdc`.
<!-- cs: Ve výchozím stavu nejsou definována žádná projektově specifická pravidla návrhu.
     Spotřebitelský projekt tento soubor ZCELA přepíše vytvořením
     doc/apm_config/DESIGN_RULES.user.md — viz Config Resolution mechanismus v
     rules/20-project-design-rules.mdc. -->

## Suggested sections (fill in `DESIGN_RULES.user.md`)
<!-- cs: Doporučené sekce (vyplň v DESIGN_RULES.user.md) -->

- Source of Truth (which documents are binding, in which order)
- Planner / Coder / Reviewer responsibilities specific to this project
- Forbidden technologies (with justification)
- Human gate policy per Task complexity tier
<!-- cs: Zdroj pravdy (které dokumenty jsou závazné, v jakém pořadí).
     Odpovědnosti Plannera/Codera/Reviewera specifické pro tento projekt.
     Zakázané technologie (s odůvodněním).
     Politika lidské brány podle pásma složitosti tasku. -->
