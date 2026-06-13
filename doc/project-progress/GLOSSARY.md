# APM Glossary — Agentic Project Management

<!-- cs: Slovník pojmů pro APM — Agentem Řízený Vývoj -->

> This file is for **human readers**. For machine-readable conventions, see `rules/07-project-management.mdc`.
<!-- cs: Tento soubor je pro lidské čtenáře. Strojové konvence viz rules/07-project-management.mdc. -->

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
the Roadmap — if the spec is ambiguous, it stops and asks Human.

<!-- cs: Levnější AI model zodpovědný za implementaci kódu, psaní testů, regresní kontrolu,
     vyplnění DoD checklistu a psaní reportů.
     Coder vždy čte spec.md a dod.md před zahájením práce. Nikdy neplánuje ani nemění roadmapu. -->

### Reviewer
**Czech:** Recenzent

A strong-reasoning AI model (assigned per `rules/00-model-policy.mdc`) that is a **different
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

---

## Document Types
<!-- cs: Typy dokumentů -->

### Project Brief (`brief.md`)
**Czech:** Neformální zadání projektu

The raw, unstructured input from Human at the start of a project. Captured verbatim —
never interpreted or reformulated. Serves as the permanent record of original intent.

<!-- cs: Surový, nestrukturovaný vstup od člověka na začátku projektu. Zaznamenaný doslova.
     Slouží jako trvalý záznam původního záměru. -->

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
resolved (model assigned per `rules/00-model-policy.mdc`). Checked
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

Written by Coder after completing a Task. Language: `<communication-language>`.
Contains: what was implemented, inputs/outputs, key decisions, code references,
regression check result, and DoD summary.

The primary mechanism by which Human stays informed of what happened.

<!-- cs: Napsáno Coderem po dokončení tasku. Jazyk: <communication-language>.
     Obsahuje: co bylo implementováno, vstupy/výstupy, klíčová rozhodnutí, reference do kódu,
     výsledek regresního testu a shrnutí DoD.
     Primární mechanismus, kterým zůstává člověk informován o tom, co se dělo. -->

### Task Review (`task-NNN/review.md`)
**Czech:** Revize tasku

Written by the Reviewer (≠ Coder) after the Task Report, before Human review. Contains the
verdict (APPROVE / REQUEST CHANGES), severity-tagged findings (blocker / major / minor),
per-item verification of the DoD, and an independent test-run result. Only an APPROVE verdict
advances the Task to Human review.

<!-- cs: Napsáno Reviewerem (≠ Coder) po Task Reportu, před revizí Humanem. Obsahuje verdikt
     (APPROVE / REQUEST CHANGES), nálezy podle závažnosti (blocker / major / minor), ověření
     DoD po položkách a nezávislý výsledek testů. Jen verdikt APPROVE posune task k Humanovi. -->

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
| Task Execution | FT.1–FT.7 | Coder | implementation, tests, `dod.md`, `report.md` |
| Task Review | FR.1–FR.3 | Reviewer | `task-NNN/review.md` (APPROVE / REQUEST CHANGES) |
| Epic Closure | FER.1–FER.2 | Coder→Planner | `epic-NNN/report.md`, roadmap + ADR review |
