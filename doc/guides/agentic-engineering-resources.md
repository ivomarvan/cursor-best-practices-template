# Agentic Engineering — studijní materiály

> Kurátorovaný seznam zdrojů k vylepšení vedení projektů, na kterých pracují AI agenti.
> Každá položka je napojená na konkrétní doporučení nebo prvek tohoto APM systému.
> Odkazy ověřeny: 2026-06-13.

---

## Jádro: vzory agentních systémů

### Building Effective Agents — Anthropic
<https://www.anthropic.com/engineering/building-effective-agents>

Referenční přehled vzorů: rozdíl mezi *workflow* (předdefinované kroky) a *agentem*
(model řídí vlastní postup) a katalog vzorů — prompt chaining, routing, orchestrator–workers
a **evaluator–optimizer**.

- **Souvislost s naším APM:** evaluator–optimizer = naše nová role **Reviewer**
  (`skills/review-task/`). Orchestrator–workers = vztah Planner → Coder.
- Hlavní zásada: *„Najdi nejjednodušší řešení a složitost přidávej, jen když je potřeba."*

### Effective context engineering for AI agents — Anthropic
<https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>

Jak spravovat *attention budget* modelu: hledat nejmenší množinu vysoce signálních tokenů.
Strategie: compaction, tool-result clearing, externí paměť (note-taking), izolace přes subagenty.

- **Souvislost s naším APM:** přímá teorie za naším **Context Bundle** a dokumentovou pamětí
  (spec/report). Nápad na zlepšení: cross-task „memory" a handover mezi instancemi.

### Effective harnesses for long-running agents / Harness design — Anthropic
<https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents>
<https://www.anthropic.com/engineering/harness-design-long-running-apps>

Jak stavět „harness" pro agenty běžící přes mnoho kontextových oken. Klíčové pro dlouhé tasky
a paralelní běh (doporučení #5 — worktrees / Cloud Agents).

---

## Produkční principy

### 12-Factor Agents — Dex Horthy / HumanLayer
<https://github.com/humanlayer/12-factor-agents>

Dvanáct principů pro spolehlivé LLM aplikace (analogie 12-Factor App). Mj.: vlastni si svoje
prompty, kontext i control flow; malé fokusované agenty; human-in-the-loop; stateless reducer.

- **Souvislost s naším APM:** potvrzuje náš design (Human gate, malé role, dokumentový stav)
  a dává slovník pro další vylepšení.

### Agentic Project Management (APM) — sdi2200262
<https://github.com/sdi2200262/agentic-project-management>

Upstream framework, kterým je náš systém inspirovaný. Stojí za prostudování zejména:
- **Memory Bank** a **Handover Protocol** (dva artefakty: Handover File + Handover Prompt)
  pro přenos „pracovní paměti" do čerstvé instance, když se zaplní kontext.
- Návrh: <https://agentic-project-management.dev/docs/context-and-memory-management>

- **Souvislost s naším APM:** chybějící dílek u nás — co dělat, když Coder/Planner narazí na
  strop kontextu uprostřed dlouhého tasku (kandidát na budoucí skill `handover`).

---

## Bezpečnost agentů

### The lethal trifecta for AI agents — Simon Willison
<https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/>

Krádež dat je možná, když agent má současně: (1) přístup k privátním datům,
(2) příjem nedůvěryhodného obsahu, (3) možnost odchozí komunikace. Odstranění libovolné nohy
útok zablokuje.

- **Souvislost s naším APM:** přímý základ pravidla `rules/08-agent-security.mdc`.
- Navazující: *Design Patterns for Securing LLM Agents against Prompt Injections* (odkazováno
  v článku) — šest vzorů obrany.

---

## Klasické inženýrské základy (stále platné)

### Documenting Architecture Decisions (ADR) — Michael Nygard
<https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions>
Komentář M. Fowlera: <https://martinfowler.com/bliki/ArchitectureDecisionRecord.html>

Lehký formát záznamu rozhodnutí (Title, Status, Context, Decision, Consequences) verzovaný
vedle kódu.

- **Souvislost s naším APM:** základ pro **ADR most** (doporučení #2) — povyšování rozhodnutí
  z Task/Epic reportů do `doc/architecture/decisions/`.

### The Practical Test Pyramid — Ham Vocke (na webu M. Fowlera)
<https://martinfowler.com/articles/practical-test-pyramid.html>

Vyvážené portfolio testů: hodně rychlých unit testů, méně integračních, minimum e2e.

- **Souvislost s naším APM:** podklad pro budoucí samostatné pravidlo `19-testing.mdc`
  (doporučení #6) — coverage brána a test pyramida nad rámec „happy + edge + error".

---

## Cursor — platforma

- **Rules:** <https://cursor.com/docs/rules> — `.mdc`, `globs`, `alwaysApply`, precedence,
  `AGENTS.md` jako alternativa.
- **Cloud / Background Agents:** <https://cursor.com/docs/cloud-agent> — izolované VM,
  paralelní běh, `.cursor/environment.json`. Relevantní pro paralelní tasky (doporučení #5).
  - Pozor: komunitní zkušenost — `globs`/auto-attached pravidla v background agentech historicky
    nefungovala spolehlivě; ověř u svého workflow.
- **Cursor SDK:** pro skutečnou per-role automatizaci modelů (Planner/Coder/Reviewer) mimo IDE
  (souvisí s omezením popsaným v `rules/00-model-policy.mdc`).

---

## Průběžné čtení

- **Exploring Gen AI** — Martin Fowler / Birgitta Böckeler:
  <https://martinfowler.com/articles/exploring-gen-ai.html>
  Kritický, nehypovaný pohled na AI ve vývoji software.

---

## Mapa: doporučení → zdroj → stav v repu

| # | Doporučení | Hlavní zdroj | Stav |
|---|------------|--------------|------|
| 1 | Nezávislý Reviewer | Building Effective Agents (evaluator–optimizer) | hotovo — `skills/review-task/` |
| 2 | ADR most | Nygard — ADR | hotovo — rule 07 + skills |
| 3 | Definition of Ready | (vlastní; protějšek DoD) | hotovo — rule 07 + plan-epic |
| 7 | Prompt-injection obrana | Willison — lethal trifecta | hotovo — `rules/08-agent-security.mdc` |
| 8 | Model-policy single source | 12-Factor Agents (own your config) | hotovo — `rules/00-model-policy.mdc` |
| 4 | Spec reconciliation | APM memory/handover | částečně — v `review-epic` |
| 5 | Paralelní tasky | Anthropic harness / Cursor Cloud Agents | navrženo |
| 6 | Testovací strategie | Practical Test Pyramid | navrženo |
| 9 | Měření procesu | building evals (Anthropic/OpenAI) | navrženo |
