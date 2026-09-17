# Known Limitations — Not Simply Resolvable Yet

<!-- cs: Známá omezení — nejde je jednoduše vyřešit -->

> Written during a v1.1.0 methodology review. Each item below was considered and
> rejected as a template-level fix — not because it is unimportant, but because the fix
> requires either a decision outside the template's authority, live introspection this
> agent does not have, or real piloting time rather than more rule text. Revisit this
> file when circumstances change (noted per item).
<!-- cs: Zapsáno během revize metodiky v1.1.0. Každý bod byl zvážen a odmítnut jako
     oprava na úrovni šablony — ne proto, že by nebyl důležitý, ale protože oprava
     vyžaduje buď rozhodnutí mimo pravomoc šablony, živou introspekci, kterou tento agent
     nemá, nebo reálný čas pilotování místo dalšího textu pravidla. Vrať se k tomuto
     souboru, až se okolnosti změní (u každého bodu uvedeno). -->

## A. Checkpoint-per-Task as the default commit workflow

<!-- cs: A. Checkpoint-per-task jako výchozí commit workflow -->

**Idea**: make "one Task = one commit" the standard, so the Reviewer always works
against a clean `git diff`.

**Why it doesn't fit here**: this project's own Git rule (`rules/020-git.mdc`) forbids
`git commit`/`git push` without an explicit trigger phrase from the Human, by explicit
Human instruction ("I never want automatic commits — I want absolute control over the
repository"). Making per-Task commits a *default* behavior would override that
instruction from inside the template, which is not this template's call to make.

**What is possible instead** (implemented in v1.2.0): after every APPROVE the Planner
*offers* a commit in one line and the Human answers with a trigger phrase
(`rules/090-apm-orchestration.mdc` § A, `skills/review-task/SKILL.md` R6). If the Human
declines, the Reviewer path-scopes its diff to the Task's `spec.md` Outputs and says so in
`review.md`. It cannot be made automatic without the Human either invoking that trigger
every time or changing the underlying Git policy.

**Revisit when**: the Human decides to relax the git-control rule for a specific project
via that project's own `DESIGN_RULES.user.md`.

<!-- cs: Nápad: "jeden task = jeden commit" jako standard pro čistý git diff Revieweru.
     Proč to nejde: 020-git.mdc zakazuje commit/push bez trigger phrase, na explicitní
     přání Humana ("absolutní kontrola nad repozitářem"). Šablona to nesmí obejít.
     Co lze: doporučit "s commitem do feature" po každém tasku, ne vynutit. Vrátit se:
     až Human uvolní git-pravidlo pro konkrétní projekt v DESIGN_RULES.user.md. -->

## B. Empirical proof of double-loading via the self-referential symlink

<!-- cs: B. Empirické ověření dvojího načítání přes symlink -->

**Idea**: prove or disprove that mounting this template as a `.cursor` git submodule,
combined with an internal `rules/ -> ../rules`-style symlink, causes Cursor to load the
same `alwaysApply` rule twice (double token cost).

**Why it doesn't fit here**: verifying this needs a live Cursor session with a real
submodule mount and visibility into Cursor's internal "relevant rules" resolution — an
introspection channel this agent does not have from a text-only chat window.

**What was done instead**: the template's own internal `.cursor/rules` /
`.cursor/skills` symlinks were removed (v1.1.0) — they existed only for this repo's own
now-abandoned dogfooding setup and were not needed by any documented consumption path
(Option A submodule mounts the repo root directly; Option C copies files). Removing them
does not resolve the underlying question, but it does eliminate the one place in this
repo where the failure mode could have originated.

**Revisit when**: someone can reproduce a live submodule mount inside a running Cursor
session and inspect which rule files it actually attached to a query.

<!-- cs: Nápad: dokázat/vyvrátit dvojí načtení stejného alwaysApply pravidla při
     submodulu + symlinku. Proč to nejde: potřeba živá Cursor session s reálným
     submodulem a pohledem do interního resolveru pravidel — nemám introspekci.
     Co bylo uděláno: template's vlastní symlinky odstraněny (v1.1.0) — sloužily jen
     opuštěnému self-dogfoodingu a nebyly potřeba pro Option A ani C. Nevyřeší otázku,
     ale odstraní jedno místo, kde k tomu mohlo docházet. Vrátit se: až někdo bude moct
     živě reprodukovat submodul mount v běžící Cursor session. -->

## C. Deterministic-gate templates for every language stack

<!-- cs: C. Gate-vzor pro všechny jazykové stacky šablony -->

**Idea**: ship a `make check`-equivalent pattern (Makefile + CI workflow) for every
stack this template has a rule for: Python, C++/ESP32, Vue/Vite.

**Why it doesn't fit here (yet)**: the Python pattern (v1.1.0) is a single, well-defined
target because `ruff`/`mypy`/`pytest` are already the template's canonical Python tools.
C++/ESP32 (`idf.py build` + on-target or Unity/CMock test flows) and Vue/Vite (`npm test`
+ `eslint` + `vue-tsc`) each need their own idiomatic equivalent — that is real,
per-stack design work, not a mechanical copy of the Python pattern.

**What was done instead**: `README.md` and `skills/python-dev/SKILL.md` explicitly flag
this as Python-only coverage, so nobody assumes the other stacks have an equivalent gate
that does not exist yet.

**Revisit when**: a project actually using the C++/ESP32 or Vue/Vite rules needs a
deterministic gate — build the pattern against that project's real toolchain, not
speculatively.

<!-- cs: Nápad: make check vzor pro všechny jazyky šablony. Proč to nejde (ještě):
     Python vzor je dobře definovaný cíl, protože ruff/mypy/pytest jsou už kanonické
     nástroje. C++/ESP32 a Vue/Vite potřebují vlastní idiomatický ekvivalent — reálná
     práce na návrhu, ne mechanická kopie. Co bylo uděláno: README.md a python-dev
     SKILL.md explicitně říkají, že je to jen pro Python. Vrátit se: až reálný projekt
     s C++/ESP32 nebo Vue/Vite gate potřebuje. -->

## D. Real piloting of the new mechanisms

<!-- cs: D. Skutečné pilotování nových mechanismů -->

**Idea**: confirm that `spike` Epics, `DECISIONS.md`, band-based gates, etc. do not fall
into the same trap as a previous, abandoned methodology iteration ("too formalistic,
slows work down").

**Why it doesn't fit here**: writing a rule is not the same as proving it works. That
can only be shown by running real Tasks in a real project (`lab.witwhip`) and observing
where it drags — this is explicitly a staged rollout, not a one-shot template change.

**What was done instead**: the mechanisms are written and internally consistent
(v1.1.0). Piloting is the Human's and Planner's job in the consuming project, not
something this template repo can do to itself.

**Revisit when**: after the first few Epics in `lab.witwhip` (or another consuming
project) have gone through `spike`/`DECISIONS.md`/band gates in practice — collect what
drags and bring concrete friction points back here.

<!-- cs: Nápad: ověřit, že nové mechanismy nespadnou do stejné pasti jako opuštěná verze
     metodiky ("příliš formalistické"). Proč to nejde: psaní pravidla ≠ důkaz, že
     funguje; ověří to jen reálné tasky v reálném projektu. Co bylo uděláno: mechanismy
     jsou napsané a vnitřně konzistentní. Vrátit se: po prvních epikách v lab.witwhip,
     které mechanismy reálně použily. -->

## E. Accuracy of agent self-reported token usage

<!-- cs: E. Přesnost self-reportu tokenů agentem -->

**Idea**: have the Coder fill in a "tokens used" field in the Epic Report automatically.

**Why it doesn't fit here**: an agent has no reliable introspective access to how many
tokens a session actually consumed — only Cursor's own UI shows real counts. An agent
"guessing" a number would be worse than no number at all (false precision).

**What was done instead**: `skills/review-epic/SKILL.md` defines the field but marks it
Human-filled (copied from the UI); the Coder leaves it as `—` rather than estimate.

**Revisit when**: Cursor (or the SDK) exposes a token-usage API an agent can read
directly instead of guessing.

<!-- cs: Nápad: Coder automaticky vyplní "tokeny" v Epic Reportu. Proč to nejde: agent
     nemá spolehlivou introspekci vlastní spotřeby tokenů, jen Cursor UI ukazuje reálná
     čísla; hádané číslo by bylo horší než žádné. Co bylo uděláno: pole existuje, ale
     vyplňuje ho Human; Coder nechává "—". Vrátit se: až Cursor/SDK nabídne API na
     spotřebu tokenů, které agent může přečíst přímo. -->
