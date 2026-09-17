# APM Glossary — Agentic Project Management

<!-- cs: Slovník pojmů pro APM — Agentem Řízený Vývoj -->

> This file is for **human readers**. For machine-readable conventions, see
> `rules/070-project-management.mdc` and, for the Human gate / band policy,
> `rules/090-apm-orchestration.mdc`.
<!-- cs: Tento soubor je pro lidské čtenáře. Strojové konvence viz rules/070-project-management.mdc
     a pro politiku lidských bran/pásem rules/090-apm-orchestration.mdc. -->

---

## Actors
<!-- cs: Aktéři -->

### Planner
**Czech:** Plánovač

The expensive, complex AI model responsible for understanding the project, asking clarifying
questions, writing the Project Specification and Roadmap, decomposing Epics into Tasks,
and reviewing whether the Roadmap remains valid after each Epic closes.

The Planner never writes production code. It writes documents that guide the Coder.

<!-- cs: Dražší, komplexní AI model zodpovědný za porozumění projektu, kladení upřesňujících otázek,
     psaní specifikace a roadmapy, dekomposici epik na tasky a review roadmapy po uzavření každé epiky.
     Planner nikdy nepíše produkční kód — píše dokumenty, které vedou Codera. -->

### Coder
**Czech:** Kodér

The cheaper AI model responsible for implementing code, writing tests, running the regression
check, filling the Definition of Done checklist, and writing Task and Epic Reports.

The Coder always reads `spec.md` and `dod.md` before starting work. It never plans or changes
the Roadmap — if the spec is ambiguous, it stops and reports to the **Planner** (its
orchestrator), not to Human directly: a Coder subagent has no channel of its own to Human.

<!-- cs: Levnější AI model zodpovědný za implementaci kódu, psaní testů, regresní kontrolu,
     vyplnění DoD checklistu a psaní reportů.
     Coder vždy čte spec.md a dod.md před zahájením práce. Nikdy neplánuje ani nemění roadmapu.
     Při nejasnosti reportuje Plannerovi, ne přímo Humanovi. -->

### Reviewer
**Czech:** Recenzent

A strong-reasoning AI model (assigned per `rules/000-model-policy.mdc`) that is a **different
agent than the Coder**. It performs an
independent, adversarial review of a completed Task before the Human: it checks the real
`git diff` against `spec.md` and `dod.md`, re-runs the tests itself, verifies every `✅`
against an actual artifact, hunts scope creep and weak tests, and writes `review.md` with an
APPROVE / REQUEST CHANGES verdict. The Reviewer never edits production code — the Coder fixes
findings in a bounded loop (max 3 rounds).

An author should never grade their own work; the Reviewer closes that blind spot
(evaluator–optimizer pattern).

<!-- cs: Silný AI model (úroveň Planner), jiný agent než Coder. Provádí nezávislou adversariální
     revizi dokončeného tasku před Humanem: kontroluje skutečný git diff proti spec.md a dod.md,
     sám spustí testy, ověří každou ✅ proti reálnému artefaktu, hledá scope creep a slabé testy,
     píše review.md s verdiktem APPROVE / REQUEST CHANGES. Reviewer needituje produkční kód —
     nálezy opravuje Coder ve smyčce (max 3 kola). Autor nemá hodnotit vlastní práci. -->

### Human
**Czech:** Člověk

You — the project owner. You provide the initial brief, approve all Planner-produced documents
before work begins, review Coder output, and make final decisions on Roadmap changes.
You are the only actor who can authorize `git commit/push` or destructive operations.

<!-- cs: Ty — vlastník projektu. Poskytuješ vstupní brief, schvaluješ všechny dokumenty Planneru,
     revidujete výstup Codera a rozhoduješ o změnách roadmapy.
     Jsi jediný aktér, který může autorizovat git commit/push nebo destruktivní operace. -->

### Band
**Czech:** Pásmo

A deterministic difficulty rating (`low` / `medium` / `high`) assigned to every Task
(and, at the max over its Tasks, to its Epic for the Planner) from fixed triggers — never
judged by feel. The band decides which model tier runs the Task
(`rules/000-model-policy.mdc`) and how much process ceremony it costs: gate at FT.7 and
report tier (`rules/090-apm-orchestration.mdc`). A second `REQUEST CHANGES` from the
Reviewer raises the band automatically; only Human may lower one.

<!-- cs: Deterministické hodnocení obtížnosti (low/medium/high) přiřazené každému tasku
     (a epice Planneru, jako maximum přes její tasky) podle pevných spouštěčů — nikdy od oka.
     Pásmo určuje jak úroveň modelu, tak cenu procesu: bránu na FT.7 a úroveň reportu.
     Druhé REQUEST CHANGES od Reviewera pásmo automaticky zvedá; snížit ho smí jen Human. -->

---

## Document Types
<!-- cs: Typy dokumentů -->

### Project Brief (`brief.md`)
**Czech:** Neformální zadání projektu

The raw, unstructured input from Human at the start of a project. Captured verbatim —
never interpreted or reformulated. Serves as the permanent record of original intent.

<!-- cs: Surový, nestrukturovaný vstup od člověka na začátku projektu. Zaznamenaný doslova.
     Slouží jako trvalý záznam původního záměru. -->

### Decisions Register (`DECISIONS.md`)
**Czech:** Registr rozhodnutí

A short, append-only table — one row per already-settled question (question, decision,
date, reference) — that every Phase checks a new chat instruction against before
starting. It exists because re-reading the full `spec.md`/`roadmap.md`/`DESIGN_RULES.user.md`
tree on every Phase does not scale; `DECISIONS.md` is the fast, always-scannable target
for the Source of Truth conflict check (`rules/070-project-management.mdc`). The full SoT
documents remain authoritative for completeness.

<!-- cs: Krátká, append-only tabulka — jeden řádek na už vyřešenou otázku (otázka,
     rozhodnutí, datum, odkaz) — proti které se ověřuje nový pokyn z chatu před zahájením
     každé fáze. Existuje, protože číst celý strom spec.md/roadmap.md/DESIGN_RULES.user.md
     při každé fázi neškáluje; DECISIONS.md je rychlý, vždy celý čitelný cíl kontroly
     rozporu SoT. Plné SoT dokumenty zůstávají autoritativní pro úplnost. -->

### Project Specification (`spec.md`)
**Czech:** Specifikace projektu

The Planner's formalized document derived from the Project Brief after iterative discussion.
Contains: project goal, scope, non-goals, key technical decisions, assumptions,
and the project-level Definition of Done.

This is the **single source of truth** for what the project must achieve.

<!-- cs: Formalizovaný dokument Planneru odvozený z brifu po iterativní diskuzi.
     Obsahuje: cíl, scope, non-goals, klíčová technická rozhodnutí, předpoklady a DoD projektu.
     Je to jediný zdroj pravdy pro to, čeho musí projekt dosáhnout. -->

### Roadmap (`roadmap.md`)
**Czech:** Hlavní plán projektu

An ordered list of Epics that collectively deliver the Project Specification.
Numbered in steps of 10 (E010, E020...) to allow insertion.
Reviewed and potentially updated after each Epic closes.

<!-- cs: Seřazený seznam epik, které společně naplňují specifikaci projektu.
     Číslováno po 10 (E010, E020...) pro možnost vkládání.
     Reviduje se a případně aktualizuje po uzavření každé epiky. -->

### Epic (`epic-NNN-name/`)
**Czech:** Velký úkol (Epika)

A significant, self-contained deliverable within the project — typically 3–8 Tasks.
An Epic should be completable within a few days of focused work.
Named with a step-of-10 number and a short mnemonic: `epic-010-setup-infrastructure`.

<!-- cs: Významný, ucelený deliverable v projektu — typicky 3–8 tasků.
     Epika by měla být dokončitelná během několika dní soustředěné práce.
     Pojmenována číslem po 10 a krátkým mnemotechnickým popisem. -->

### Epic Plan (`epic-NNN/plan.md`)
**Czech:** Plán epiky

Written by Planner before any coding starts. Contains the list of Tasks with dependencies,
the Context Bundle for each Task, test specification, and Definition of Done checklist.
Must be approved by Human before Coder begins work.

<!-- cs: Napsán Plannerem před zahájením kódování. Obsahuje seznam tasků se závislostmi,
     Context Bundle pro každý task, specifikaci testů a DoD checklist.
     Musí být schválen člověkem před zahájením práce Codera. -->

### Task (`task-NNN-name/`)
**Czech:** Úkol (Task)

The smallest independently implementable and testable unit of work.
A Task produces a concrete artifact (a module, a migration, a configured service, etc.)
that can be tested in isolation.

Numbered relative to the Epic (T010, T020...) with step-of-10.

<!-- cs: Nejmenší samostatně implementovatelná a testovatelná jednotka práce.
     Task produkuje konkrétní artefakt, který lze testovat izolovaně.
     Číslováno relativně k epice (T010, T020...) po 10. -->

### Task Specification (`task-NNN/spec.md`)
**Czech:** Zadání tasku

Written by Planner. The complete instruction set for Coder — contains goal, inputs,
outputs, Context Bundle, dependencies, test specification, and Definition of Done checklist.
The Coder must be able to implement the entire Task from this document alone.

<!-- cs: Napsáno Plannerem. Kompletní instrukce pro Codera — obsahuje cíl, vstupy, výstupy,
     Context Bundle, závislosti, specifikaci testů a DoD checklist.
     Coder musí být schopen implementovat celý task pouze z tohoto dokumentu. -->

### Context Bundle
**Czech:** Kontextový balík

A section within Task Specification that tells Coder exactly which files to read,
which files NOT to modify, and which interfaces prior Tasks have made available.
Compensates for the Coder's limited project-wide context.

<!-- cs: Sekce v Task Specification, která Coderovi říká přesně které soubory číst,
     které soubory NESMÍ měnit, a jaká rozhraní poskytují předchozí tasky.
     Kompenzuje omezený projektový kontext Codera. -->

### Definition of Ready (DoR)
**Czech:** Kritéria připravenosti

A quality gate on the **input** side, the counterpart of the Definition of Done. Before a Task
is handed to a Coder, its `spec.md` must pass the DoR checklist: measurable goal, concrete
outputs, complete Context Bundle, verifiable DoD, named test cases, and the Coder role
resolved (model assigned per `rules/000-model-policy.mdc`). Checked
at the FE.2 Human review of the Epic Plan. A vague spec guarantees a failed Task.

<!-- cs: Brána kvality na vstupní straně, protějšek Definition of Done. Než task dostane Coder,
     jeho spec.md musí projít DoR checklistem: měřitelný cíl, konkrétní výstupy, úplný Context
     Bundle, ověřitelné DoD, pojmenované testovací případy a úroveň modelu. Kontroluje se při
     FE.2. Vágní spec = selhaný task. -->

### Definition of Done (`task-NNN/dod.md`)
**Czech:** Kritéria splnění

A checklist created by Planner and filled by Coder. Each criterion is marked ✅ or ❌.
All items must be addressed (no blanks) before a Task is considered complete.
Always includes: all new tests pass, full test suite passes (no regressions).

<!-- cs: Checklist vytvořený Plannerem a vyplněný Coderem. Každé kritérium je označeno ✅ nebo ❌.
     Všechny položky musí být vyplněny před považováním tasku za dokončený.
     Vždy zahrnuje: všechny nové testy projdou, celá testovací sada projde (žádné regrese). -->

### Task Report (`task-NNN/report.md`)
**Czech:** Report tasku

Written by Coder after completing a Task, in `<communication-language>`. Tier depends on
the Task's **Band**: full (7 sections — what/inputs-outputs/decisions/deviations/code refs/
regression/DoD) for `high`, short (4 sections) for `medium`, micro (5 lines) for `low` —
see `rules/090-apm-orchestration.mdc`.

The primary mechanism by which Human stays informed of what happened.

<!-- cs: Napsáno Coderem po dokončení tasku, v <communication-language>. Úroveň závisí na
     pásmu tasku: plná (7 sekcí) pro high, krátká (4 sekce) pro medium, mikro (5 řádků)
     pro low.
     Primární mechanismus, kterým zůstává člověk informován o tom, co se dělo. -->

### Task Review (`task-NNN/review.md`)
**Czech:** Revize tasku

Written by the Reviewer (≠ Coder) after the Task Report, before any Human review. Contains
the verdict (APPROVE / REQUEST CHANGES), severity-tagged findings (blocker / major /
minor), per-item verification of the DoD, and an independent test-run result. An APPROVE
verdict completes the Task in every Band; whether it also advances to Human review (FT.7)
depends on the Task's **Band** — only `high` (or an escalated Task) reaches FT.7,
`medium`/`low` surface later in the Epic Report instead.

<!-- cs: Napsáno Reviewerem (≠ Coder) po Task Reportu, před případnou revizí Humanem. Obsahuje
     verdikt (APPROVE / REQUEST CHANGES), nálezy podle závažnosti (blocker / major / minor), ověření
     DoD po položkách a nezávislý výsledek testů. APPROVE task dokončí v každém pásmu; jestli
     jde i k Humanovi na FT.7, závisí na pásmu — jen high (nebo eskalovaný) tam jde, medium/low
     se objeví až v Epic Reportu. -->

### Epic Report (`epic-NNN/report.md`)
**Czech:** Report epiky

Written by Coder after all Tasks in an Epic are complete.
Aggregates Task Reports into a single summary covering: completed Tasks, key decisions,
deviations from plan, and recommendations for the Planner.

<!-- cs: Napsáno Coderem po dokončení všech tasků v epice.
     Agreguje reporty tasků do jednoho souhrnu pokrývajícího: dokončené tasky, klíčová rozhodnutí,
     odchylky od plánu a doporučení pro Plannera. -->

---

## Reference Scheme
<!-- cs: Schéma referencí -->

| Level | Format | Example |
|-------|--------|---------|
| Project | `PROJECT` | `apm_ref: PROJECT` |
| Epic | `ENNN` | `apm_ref: E010` |
| Task | `ENNN.TNNN` | `apm_ref: E010.T020` |

Numbering in steps of 10: insert `E015` between `E010` and `E020`.

<!-- cs: Číslování po 10: vložení E015 mezi E010 a E020. -->

---

## APM Phase Reference
<!-- cs: Přehled fází APM -->

| Phase | Code | Actor | Output |
|-------|------|-------|--------|
| Project Init | F0.1–F0.5 | Human→Planner | `brief.md`, `spec.md`, `roadmap.md` |
| Epic Planning | FE.1–FE.2 | Planner | `epic-NNN/plan.md`, task dirs (+ DoR gate) |
| Task Execution | FT.1–FT.7 | Coder | implementation, tests, `dod.md`, `report.md` (FT.7 Human gate is Band-conditional — see `rules/090-apm-orchestration.mdc`) |
| Task Review | FR.1–FR.3 | Reviewer | `task-NNN/review.md` (APPROVE / REQUEST CHANGES) |
| Epic Closure | FER.1–FER.2 | Coder→Planner | `epic-NNN/report.md`, roadmap + ADR review |
