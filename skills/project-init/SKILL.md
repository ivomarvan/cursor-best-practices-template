---
name: project-init
description: >-
  APM Phase 0 — Initialize a new project using the Agentic Project Management workflow.
  Guides the Planner through formalizing a Project Brief into spec.md and roadmap.md.
  Use when: starting a new project, receiving an informal brief from Human, or
  setting up the doc/project-progress/ directory structure for the first time.
---

# Skill: APM Project Initialization (Phase 0)
<!-- cs: Skill: APM Inicializace projektu (Fáze 0) -->

## Prerequisites
<!-- cs: Předpoklady -->

- You are acting as **Planner**.
- Human has provided a **Project Brief** (informal input — text, bullet list, or verbal).
- Rule `070-project-management.mdc` is in context (provides APM conventions).

<!-- cs: Jsi v roli Planner. Člověk poskytl Project Brief. Pravidlo 070-project-management.mdc je v kontextu. -->

## Steps
<!-- cs: Kroky -->

### Step 1 — Save the Project Brief [F0.1]
<!-- cs: Krok 1 — Uložit Project Brief [F0.1] -->

Create `doc/project-progress/brief.md` with front matter:

```yaml
---
apm_category: project-brief
apm_ref: PROJECT
apm_level: project
created_by: Human
intended_for: Planner
created_at: <YYYY-MM-DD>
updated_at: <YYYY-MM-DD>
---
```

Paste or transcribe the Human's informal input verbatim. Do not interpret yet.

### Step 2 — Iterative Clarification [F0.2]
<!-- cs: Krok 2 — Iterativní upřesnění [F0.2] -->

**Skip this step** if the brief already contains a decisions register (or the project has
a filled `DECISIONS.md`) **and** no open blocking questions — a complete brief is not
re-interrogated (see `070-project-management.mdc` SoT rule: what the SoT answers, do not
ask). Go straight to Step 3.
<!-- cs: Krok přeskoč, když brief už má registr rozhodnutí (nebo projekt vyplněný
     DECISIONS.md) a žádné otevřené blokující otázky — hotový brief se znovu nevyslýchá.
     Rovnou na krok 3. -->

Otherwise ask Human targeted questions to resolve ambiguities — **one decision per
question**, each with the options and your recommendation (`005-decision-protocol.mdc`).
Cover:
<!-- cs: Jinak polož cílené otázky — jedno rozhodnutí na otázku, s možnostmi a doporučením
     (005-decision-protocol.mdc). Pokryj: -->
- **Scope**: what is explicitly IN and OUT of scope?
- **Users**: who uses the system? what are their key workflows?
- **Constraints**: technology stack, deployment target, performance requirements?
- **Success criteria**: how do we know the project is done?
- **Non-goals**: what must we NOT build (to prevent scope creep)?

REPEAT until Human confirms the brief is complete.

### Step 3 — Write Project Specification [F0.3]
<!-- cs: Krok 3 — Napsat specifikaci projektu [F0.3] -->

Create `doc/project-progress/spec.md`:

```yaml
---
apm_category: project-spec
apm_ref: PROJECT
apm_level: project
created_by: Planner
model: <model-name>
template_version: <from .cursor/TEMPLATE_VERSION>
intended_for: All
created_at: <YYYY-MM-DD>
updated_at: <YYYY-MM-DD>
---
```

Required sections:
1. **Goal** — 1–3 sentence project goal
2. **Scope** — what is in scope
3. **Non-Goals** — what is explicitly out of scope
4. **Key Technical Decisions** — stack, architecture style, major constraints
5. **Assumptions** — what we assume to be true
6. **Project-Level Definition of Done** — criteria for project completion
7. **Source of Truth** — the ordered list of SoT documents (`070-project-management.mdc`);
   `spec.md` alone is the default, a detailed brief may stay in the list.

**Detailed brief.** If the brief already contains architecture, data model, or domain
detail (tables, schemas, flows), do **not** compress it into `spec.md`. Move each such
section to its own file under `doc/architecture/<topic>.md` (verbatim, Human's input is
never rewritten), link it from `spec.md` § 4, and list the moved files in the SoT
section. `spec.md` stays the short entry point; the detail stays authoritative.
<!-- cs: 7. Source of Truth — seřazený seznam SoT dokumentů; default je jen spec.md.
     Podrobný brief: architekturu, datový model a doménový detail nekomprimuj do spec.md,
     přesuň každou sekci beze změny do doc/architecture/<téma>.md, odkaž ze spec.md § 4 a
     soubory uveď v sekci SoT. spec.md zůstane krátkým vstupem, detail zůstane závazný. -->

### Step 4 — Write Roadmap [F0.4]
<!-- cs: Krok 4 — Napsat Roadmapu [F0.4] -->

Create `doc/project-progress/roadmap.md`:

```yaml
---
apm_category: roadmap
apm_ref: PROJECT
apm_level: project
created_by: Planner
model: <model-name>
template_version: <from .cursor/TEMPLATE_VERSION>
intended_for: All
created_at: <YYYY-MM-DD>
updated_at: <YYYY-MM-DD>
---
```

List Epics in order. Use step-of-10 numbering:

```markdown
## Epic E010 — Setup & Infrastructure
Brief description. Estimated complexity: low/medium/high.

## Epic E020 — Core Domain Logic
...
```

Rationale for step-of-10: allows inserting `E015` between `E010` and `E020`.

### Step 5 — Human Review [F0.5]
<!-- cs: Krok 5 — Revize člověkem [F0.5] -->

Present `spec.md` and `roadmap.md` to Human for approval.
If rejected: revise and resubmit. Do not proceed to Epic planning until approved.

### Step 6 — Create Directory Structure
<!-- cs: Krok 6 — Vytvořit adresářovou strukturu -->

```bash
mkdir -p doc/project-progress
# Copy the GLOSSARY.md and DECISIONS.md templates shipped with this skill
cp .cursor/skills/project-init/templates/GLOSSARY.md doc/project-progress/GLOSSARY.md
cp .cursor/skills/project-init/templates/DECISIONS.md doc/project-progress/DECISIONS.md
```

## Output Checklist
<!-- cs: Výstupní checklist -->

- [ ] `doc/project-progress/brief.md` — Human's input preserved verbatim
- [ ] `doc/project-progress/spec.md` — all 7 required sections present
- [ ] Detailed brief sections moved verbatim to `doc/architecture/` and linked (if any)
- [ ] `doc/project-progress/roadmap.md` — Epics numbered E010, E020...
- [ ] `doc/project-progress/GLOSSARY.md` — copied from template
- [ ] `doc/project-progress/DECISIONS.md` — copied from template (empty register)
- [ ] Human has approved spec.md + roadmap.md [F0.5]

## Additional resources
- [../../../rules/070-project-management.mdc](../../../rules/070-project-management.mdc)
- [README.project_management.md](../../../README.project_management.md)
