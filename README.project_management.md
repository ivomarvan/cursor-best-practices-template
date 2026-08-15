# APM — Agentic Project Management

A structured workflow for building software projects using two specialized AI agents:
a **Planner** for analysis and decomposition, and a **Coder** for implementation.

APM gives you human oversight at every checkpoint while letting AI handle the cognitive
work of planning and the mechanical work of coding.

---

## Quick Overview

```
Human provides brief
    ↓
Planner formalizes → spec.md + roadmap.md  [Human approves]
    ↓
For each Epic:
    Planner decomposes → epic plan + task specs  [Definition of Ready gate] [Human approves]
    ↓
    For each Task:
        Coder implements → tests → DoD checklist → report
        Reviewer (independent) → review.md (APPROVE / REQUEST CHANGES)
            ↳ loop with Coder, max 3 rounds
        [Human reviews]
    ↓
    Coder writes Epic Report
    Planner + Human review Roadmap validity (+ ADR / spec reconciliation)
    ↓
Project complete
```

**Key principle:** Nothing moves forward without Human approval at each phase boundary.

---

## The Actors

Model per role is defined centrally in `rules/00-model-policy.mdc` (change it in one place).

### Planner

Act in the **Planner role** — a strong-reasoning model assigned per `rules/00-model-policy.mdc`
(the Human assigns it, or the agent asks before planning).

The Planner never writes production code. Its job is:
- Understanding the project through discussion with Human
- Writing `spec.md` (what to build) and `roadmap.md` (in what order)
- Decomposing each Epic into concrete, independently testable Tasks
- Preparing a **Context Bundle** for each Task — the exact files Coder must read,
  the files it must not touch, and the interfaces prior Tasks expose
- Reviewing whether the Roadmap is still valid after each Epic closes

The Planner's output is the quality gate for everything the Coder does.
If the Task Specification is vague or incomplete, the Coder will fail.

### Coder

Act in the **Coder role** — a fast / cost-effective model assigned per
`rules/00-model-policy.mdc`. The Planner flags Tasks that warrant a stronger model
(`Complexity: high`); the Human decides what to assign.

The Coder:
- Reads `spec.md` and `dod.md` before writing a single line of code
- Implements exactly what the spec says — no more, no less
- Writes tests (happy path + edge cases + error cases)
- Runs the **full test suite** to catch regressions
- Fills the Definition of Done checklist
- Writes a Task Report in `<communication-language>` with code references

If the spec is ambiguous or contradictory, the Coder stops and reports to Human.
The Coder never modifies files listed as "Do not modify" in the Context Bundle.

### Reviewer

Act in the **Reviewer role** — a strong-reasoning model assigned per
`rules/00-model-policy.mdc`. The Reviewer is a **different agent/model than the Coder**: an
author should never grade their own work.

The Reviewer:
- Reviews against ground truth — the real `git diff`, `spec.md`, `dod.md`, and a test run
  it executes itself — not the Coder's narrative in `report.md`
- Verifies **every** `✅` in `dod.md` against an actual artifact (file/test/endpoint)
- Hunts scope creep, files touched against the Context Bundle, weak/placeholder tests,
  missing edge/error cases, quality-gate violations, and undisclosed deviations
- Writes `review.md` with a verdict (**APPROVE** / **REQUEST CHANGES**) and
  severity-tagged findings (blocker / major / minor)
- Never edits production code — the Coder fixes findings in a bounded loop (max 3 rounds);
  if it exceeds the limit, the Reviewer escalates to the Human

This is the **evaluator–optimizer** pattern: an independent critic between the author and
the Human. It directly addresses the LLM tendency to over-rate its own output.

---

## Workflow in Detail

### Phase 0 — Project Initialization

**Steps F0.1–F0.5** | Actor: Human → Planner

| Step | Action | Output |
|------|--------|--------|
| F0.1 | Human delivers informal Project Brief | `brief.md` saved verbatim |
| F0.2 | Planner asks clarifying questions; iterates with Human | (discussion) |
| F0.3 | Planner writes Project Specification | `spec.md` |
| F0.4 | Planner writes Roadmap (ordered list of Epics) | `roadmap.md` |
| F0.5 | Human reviews and approves both documents | ✅ Gate |

The iterative discussion in F0.2 is the most important step. The Planner should surface:
- Scope boundaries ("Is X in or out?")
- User personas and their workflows
- Technology constraints and preferences
- Success criteria — how do we know the project is done?
- Explicit non-goals — what must we not build?

`spec.md` is the **single source of truth** for the entire project. It does not change
unless Human explicitly approves a revision. When assumptions prove wrong during
implementation, the spec is updated with a record of what changed and why.

### Phase E — Epic Planning

**Steps FE.1–FE.2** | Actor: Planner

Before writing any code, the Planner decomposes the Epic into Tasks.

Each Task must be:
- **Independently implementable** — Coder can complete it without simultaneous work on other Tasks
- **Independently testable** — passing tests prove the Task is correct
- **Appropriately sized** — typically half a day to two days of Coder work

The Planner writes:
1. `epic-NNN/plan.md` — the full Epic Plan with all Task Specifications
2. `epic-NNN/task-NNN/spec.md` — the Task Specification extracted for easy Coder reference
3. `epic-NNN/task-NNN/dod.md` — blank Definition of Done checklist

The Context Bundle in each Task Specification is critical. It tells the Coder:
- Which files to read to understand the context
- Which files are off-limits (owned by infrastructure, another Task, etc.)
- What interfaces prior Tasks have already implemented

**Definition of Ready (DoR) gate:** before any Task is handed to a Coder, its `spec.md`
must pass the DoR checklist (goal measurable, Outputs concrete, Context Bundle complete,
DoD verifiable, tests named, Coder role resolved per `rules/00-model-policy.mdc`). The DoR is
the counterpart of the DoD and is checked at the FE.2 Human review. A vague spec guarantees a
failed Task — fix it first.

**FE.2 gate:** Human reviews the Epic Plan before Coder begins any Task.

### Phase T — Task Execution

**Steps FT.1–FT.7** | Actor: Coder

| Step | Action |
|------|--------|
| FT.1 | Read `spec.md` completely, including Context Bundle |
| FT.2 | Implement code per specification |
| FT.3 | Write and run tests — all new tests must pass |
| FT.4 | Run full test suite — no regressions allowed |
| FT.5 | Fill `dod.md` — mark each criterion ✅ or ❌ with note |
| FT.6 | Write `report.md` with all required sections |
| FT.7 | Human reviews — approve or reject with feedback |

**On ambiguity:** If the Coder encounters something the spec doesn't cover, it stops
and reports to Human. It does not make architectural decisions on its own.

**On regressions (FT.4):** Regressions must be fixed before submitting — never suppressed
or skipped. If fixing a regression requires changing scope, Human decides.

**Task Report structure** (written in `<communication-language>`):
1. What was implemented
2. Inputs and outputs (files read / created / modified)
3. Methods and key decisions (with justification)
4. Code references (file paths and line ranges)
5. Regression check result
6. Definition of Done summary

**ADR bridge:** if a Task makes a decision that affects structure, dependencies, interfaces,
or other tasks, the Coder records it as an ADR in `doc/architecture/decisions/` and links it
from `report.md`. This keeps architectural knowledge out of buried task reports.

### Phase R — Independent Review

**Steps FR.1–FR.3** | Actor: Reviewer (≠ Coder)

After the Coder writes `report.md`, the Task goes to an **independent Reviewer** before the
Human, not straight to Human review.

| Step | Action |
|------|--------|
| FR.1 | Reviewer gathers ground truth: real `git diff`, `spec.md`, `dod.md`; re-runs tests |
| FR.2 | Reviewer verifies every `✅`, hunts scope creep / weak tests / undisclosed deviations |
| FR.3 | Reviewer writes `review.md`: verdict (APPROVE / REQUEST CHANGES) + findings |

**On REQUEST CHANGES:** the Coder fixes each finding, updates `report.md`, and resubmits.
The loop is bounded to **3 rounds**; if still failing, the Reviewer escalates to the Human.
Only an **APPROVE** verdict advances the Task to Human review (FT.7).

### Phase ER — Epic Closure

**Steps FER.1–FER.2** | Actor: Coder → Planner

Once all Tasks are approved:

1. **Coder** writes `epic-NNN/report.md` aggregating all Task Reports.
   Sections: completed Tasks, key decisions, deviations from plan, recommendations for Planner.

2. **Planner** reads the Epic Report, re-reads `roadmap.md` and `spec.md`, then assesses:
   - Are the upcoming Epics still correct given what we learned?
   - Did implementation reveal risks, new dependencies, or invalid assumptions?

3. **Planner presents one of three conclusions to Human:**
   - **Roadmap unchanged** → proceed to next Epic
   - **Update needed** → propose specific changes to `roadmap.md` with justification
   - **Major revision** → discuss with Human before writing anything

4. If Human approves changes, update `roadmap.md` (`updated_at` + content).

---

## Directory Structure

```
doc/project-progress/
├── GLOSSARY.md                      # Bilingual glossary of APM terms
├── brief.md                         # Project Brief (Human, verbatim)
├── spec.md                          # Project Specification (Planner)
├── roadmap.md                       # Roadmap — ordered Epic list (Planner)
├── epic-010-setup-infrastructure/
│   ├── plan.md                      # Epic Plan + all Task Specs (Planner)
│   ├── report.md                    # Epic Report (Coder)
│   ├── task-010-create-database/
│   │   ├── spec.md                  # Task Specification + Context Bundle (Planner)
│   │   ├── dod.md                   # Definition of Done checklist (Planner → Coder fills)
│   │   ├── report.md                # Task Report (Coder)
│   │   └── review.md                # Task Review (Reviewer) — APPROVE / REQUEST CHANGES
│   └── task-020-configure-docker/
│       ├── spec.md
│       ├── dod.md
│       ├── report.md
│       └── review.md
└── epic-020-core-api/
    └── ...
```

**Numbering convention:** Steps of 10 (`E010`, `E020`, `T010`, `T020`).
Insert between existing items: `epic-015-auth-refactor` fits between `epic-010` and `epic-020`.
This maintains shell sort order while allowing flexible insertion.

### Integration with project `doc/`

`doc/project-progress/` sits alongside the standard doc subdirectories:

```
doc/
├── architecture/          # System design, ADRs
├── guides/                # How-to guides, runbooks
├── api/                   # API specifications
├── external/              # Read-only external references
└── project-progress/      # APM artifacts (this workflow)
```

---

## File Header Convention

Every APM document begins with YAML front matter:

```yaml
---
apm_category: task-spec         # document type (see table below)
apm_ref: E010.T020              # reference: PROJECT | E010 | E010.T020
apm_level: task                 # project | epic | task
created_by: Planner             # Planner | Coder | Human
model: <model-id>               # actual model used (assigned per rules/00-model-policy.mdc); omit if Human
intended_for: Coder             # Planner | Coder | Human | All
created_at: 2026-05-08
updated_at: 2026-05-08
---
```

| `apm_category` value | Document |
|---------------------|----------|
| `project-brief` | `brief.md` |
| `project-spec` | `spec.md` (project level) |
| `roadmap` | `roadmap.md` |
| `epic-plan` | `epic-NNN/plan.md` |
| `task-spec` | `task-NNN/spec.md` |
| `dod` | `task-NNN/dod.md` |
| `task-report` | `task-NNN/report.md` |
| `task-review` | `task-NNN/review.md` |
| `epic-report` | `epic-NNN/report.md` |

---

## Cursor Skills

Five Skills guide AI agents through each APM phase:

| Skill | Used by | Phase |
|-------|---------|-------|
| `project-init` | Planner | Phase 0 — brief → spec + roadmap |
| `plan-epic` | Planner | Phase E — roadmap → epic plan + task specs (+ DoR gate) |
| `execute-task` | Coder | Phase T — spec → implementation + report |
| `review-task` | Reviewer | Phase R — diff vs spec/dod → `review.md` verdict |
| `review-epic` | Coder + Planner | Phase ER — epic report + roadmap review |

To invoke a skill, use `@skill-name` in Cursor chat, or reference it directly:
`Read .cursor/skills/execute-task/SKILL.md and follow it.`

---

## Cursor Rule

`rules/07-project-management.mdc` activates automatically when working on files in
`doc/project-progress/**/*.md`. It provides:
- Condensed APM terminology (machine-readable)
- Document type reference table
- File header schema
- Required sections for Task Specification and Task Report
- Security guards (no git push without Human approval)

---

## Terminology Reference

For full definitions of all APM terms, see
[`doc/project-progress/GLOSSARY.md`](doc/project-progress/GLOSSARY.md).

Quick reference:

| English | Czech | File/Location |
|---------|-------|---------------|
| Project Brief | Neformální zadání | `brief.md` |
| Project Specification | Specifikace projektu | `spec.md` |
| Roadmap | Hlavní plán | `roadmap.md` |
| Epic | Velký úkol (Epika) | `epic-NNN-name/` |
| Epic Plan | Plán epiky | `epic-NNN/plan.md` |
| Task | Úkol | `task-NNN-name/` |
| Task Specification | Zadání tasku | `task-NNN/spec.md` |
| Context Bundle | Kontextový balík | section in `spec.md` |
| Definition of Done | Kritéria splnění | `task-NNN/dod.md` |
| Task Report | Report tasku | `task-NNN/report.md` |
| Task Review | Revize tasku (Reviewer) | `task-NNN/review.md` |
| Definition of Ready | Kritéria připravenosti | DoR gate at FE.2 |
| Epic Report | Report epiky | `epic-NNN/report.md` |
| Human Review | Revize člověkem | steps FT.7, FE.2 |

---

## Checklist — Starting a New Project

```
[ ] Read README.project_management.md (this file)
[ ] Open Cursor and load the project
[ ] Invoke skill: @project-init
[ ] Deliver Project Brief to Planner
[ ] Iterate with Planner until spec.md and roadmap.md are approved [F0.5]
[ ] For each Epic: invoke @plan-epic, check DoR per Task, review plan.md, approve [FE.2]
[ ] For each Task: invoke @execute-task (Coder), then @review-task (Reviewer, different model)
[ ] Review the Reviewer's review.md, then approve the Task as Human [FT.7]
[ ] After each Epic: invoke @review-epic, review roadmap + ADR/spec validity [FER.2]
```

---

## Security and Human Control

APM is designed to keep Human in control at all times:

- **No git commit or push** without explicit Human instruction.
- **No database migrations** without Human approval.
- **No destructive file operations** without confirmation.
- Every phase boundary requires Human approval before the next phase begins.
- The Coder stops and escalates to Human when the spec is ambiguous.
- The Planner proposes Roadmap changes; Human decides whether to apply them.
