# Agentic Engineering — studijní materiály

> Kurátorovaný seznam zdrojů k vylepšení vedení projektů, na kterých pracují AI agenti.
> Každá položka je napojená na konkrétní doporučení nebo prvek metodiky ICE
> (Intent – Contract – Evidence) v tomto repozitáři.
> Odkazy ověřeny: 2026-06-13.

---

## Jádro: vzory agentních systémů

### Building Effective Agents — Anthropic
<https://www.anthropic.com/engineering/building-effective-agents>

Referenční přehled vzorů: rozdíl mezi *workflow* (předdefinované kroky) a *agentem*
(model řídí vlastní postup) a katalog vzorů — prompt chaining, routing, orchestrator–workers
a **evaluator–optimizer**.

- **Souvislost s ICE:** evaluator–optimizer = role **Adversary** (`skills/ice-review/`)
  a strojový **Grader**. Orchestrator–workers = vztah Coordinator → Planner/Coder.
- Hlavní zásada: *„Najdi nejjednodušší řešení a složitost přidávej, jen když je potřeba."*

### Effective context engineering for AI agents — Anthropic
<https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>

Jak spravovat *attention budget* modelu: hledat nejmenší množinu vysoce signálních tokenů.
Strategie: compaction, tool-result clearing, externí paměť (note-taking), izolace přes subagenty.

- **Souvislost s ICE:** přímá teorie za **řezem kontextu** (`intent slice`) a stromem záměru
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

- **Souvislost s ICE:** potvrzuje design (Human gate, malé role, stav v souborech)
  a dává slovník pro další vylepšení.

### Agentic Project Management (APM) — sdi2200262
<https://github.com/sdi2200262/agentic-project-management>

Upstream framework, kterým je náš systém inspirovaný. Stojí za prostudování zejména:
- **Memory Bank** a **Handover Protocol** (dva artefakty: Handover File + Handover Prompt)
  pro přenos „pracovní paměti" do čerstvé instance, když se zaplní kontext.
- Návrh: <https://agentic-project-management.dev/docs/context-and-memory-management>

- **Souvislost s ICE:** eskalační pravidla — co dělat, když Coder nebo Planner narazí na
  strop kontextu uprostřed dlouhého tasku (kandidát na budoucí skill `handover`).

---

## Bezpečnost agentů

### The lethal trifecta for AI agents — Simon Willison
<https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/>

Krádež dat je možná, když agent má současně: (1) přístup k privátním datům,
(2) příjem nedůvěryhodného obsahu, (3) možnost odchozí komunikace. Odstranění libovolné nohy
útok zablokuje.

- **Souvislost s ICE:** přímý základ pravidla `rules/08-agent-security.mdc`.
- Navazující: *Design Patterns for Securing LLM Agents against Prompt Injections* (odkazováno
  v článku) — šest vzorů obrany.

---

## Klasické inženýrské základy (stále platné)

### Documenting Architecture Decisions (ADR) — Michael Nygard
<https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions>
Komentář M. Fowlera: <https://martinfowler.com/bliki/ArchitectureDecisionRecord.html>

Lehký formát záznamu rozhodnutí (Title, Status, Context, Decision, Consequences) verzovaný
vedle kódu.

- **Souvislost s ICE:** základ pro **ADR most** — povyšování rozhodnutí z reportů běhu
  do `doc/architecture/decisions/` s citací krátkých identifikátorů uzlů.

### The Practical Test Pyramid — Ham Vocke (na webu M. Fowlera)
<https://martinfowler.com/articles/practical-test-pyramid.html>

Vyvážené portfolio testů: hodně rychlých unit testů, méně integračních, minimum e2e.

- **Souvislost s ICE:** podklad pro pravidlo `09-testing.mdc`
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
| 1 | Nezávislá recenze | Building Effective Agents (evaluator–optimizer) | hotovo — `skills/ice-review/` |
| 2 | ADR most | Nygard — ADR | hotovo — `rules/07-run-artifacts.mdc` |
| 3 | Definition of Ready | (vlastní; protějšek DoD) | hotovo — `rules/07-run-artifacts.mdc` |
| 7 | Prompt-injection obrana | Willison — lethal trifecta | hotovo — `rules/08-agent-security.mdc` |
| 8 | Katalog modelů | 12-Factor Agents (own your config) | hotovo — `AGENT_MODELS.md` |
| 4 | Udržovaný zdroj pravdy | APM memory/handover | hotovo — strom záměru `doc/intent/` |
| 5 | Paralelní běhy | Anthropic harness / Cursor Cloud Agents | navrženo |
| 6 | Testovací strategie | Practical Test Pyramid | navrženo |
| 9 | Měření procesu | building evals (Anthropic/OpenAI) | navrženo — metriky nad `doc/runs/` |
