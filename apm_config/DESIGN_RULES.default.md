# Design Rules — Default Configuration
<!-- cs: Výchozí konfigurace projektových pravidel návrhu -->

No project-specific design invariants are defined by default. A consuming project
overrides this file **in full** by creating `doc/apm_config/DESIGN_RULES.user.md` — see
the Config Resolution mechanism in `rules/200-project-design-rules.mdc`.
<!-- cs: Ve výchozím stavu nejsou definována žádná projektově specifická pravidla návrhu.
     Spotřebitelský projekt tento soubor ZCELA přepíše vytvořením
     doc/apm_config/DESIGN_RULES.user.md — viz Config Resolution mechanismus v
     rules/200-project-design-rules.mdc. -->

## How to read this file (keep this section when you fill in `.user.md`)
<!-- cs: Jak číst tenhle soubor (ponech tuto sekci při vyplňování .user.md) -->

- **[general]** — a rule that holds regardless of this project. Once proven in practice,
  promote it into `rules/` (this template) and remove it from here.
- **[project]** — genuinely specific to this project; stays here.
- This file **adds to** the general rules in `rules/`, it does not restate them. If you
  find yourself copying something that `rules/070-project-management.mdc` or
  `rules/090-apm-orchestration.mdc` already say, delete it — link instead.
<!-- cs: [general] — pravidlo platné bez ohledu na projekt; jakmile se osvědčí, povyš ho do
     rules/ v šabloně a odsud smaž. [project] — opravdu specifické pro tento projekt, zůstává.
     Tenhle soubor obecná pravidla doplňuje, nepřepisuje je. Pokud kopíruješ něco, co už
     říká 070-project-management.mdc nebo 090-apm-orchestration.mdc, smaž to a odkaž. -->

## Suggested sections (fill in `DESIGN_RULES.user.md`)
<!-- cs: Doporučené sekce (vyplň v DESIGN_RULES.user.md) -->

- **Source of Truth** — which document is the active SoT for this project (the *rule*
  for handling SoT conflicts lives in `rules/070-project-management.mdc`; only the pointer
  is project data).
- **Forbidden technologies** — with justification.
- **Product invariants enforced in code** — the handful of promises that must be checked
  by a test/gate, not just claimed in a report (e.g. verified citations, budget caps,
  license flags) — this is normally the bulk of this file.
- **Documentation language outside APM** — `<communication-language>` (`LANGUAGE.user.md`)
  already covers chat and APM reports; state here only if free-form docs (`doc/`,
  `private_doc/`) use a different language.
<!-- cs: Zdroj pravdy — jen ukazatel na aktivní SoT (pravidlo pro řešení konfliktů je v
     070-project-management.mdc). Zakázané technologie — s odůvodněním. Produktové invarianty
     vynucené v kódu — hrstka slibů ověřovaných testem/branou, ne jen tvrzením v reportu; to
     bývá hlavní obsah tohoto souboru. Jazyk dokumentace mimo APM — LANGUAGE.user.md už
     pokrývá chat a APM reporty, uveď jen pokud se volná dokumentace liší. -->
