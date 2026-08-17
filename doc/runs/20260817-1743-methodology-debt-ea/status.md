---
run_id: 20260817-1743-methodology-debt-ea
intent_ids: ["i0002"]
role: Coordinator
model: claude-opus-5-thinking-high
complexity: high
status: done
---

# Stav běhu

## Výsledek

Běh **dokončen**. Kritik `ACCEPT` ve druhém kole, Adversář `APPROVE` ve druhém kole.
Tři rozhodnutí, která Human vyslovil v předchozích bězích, jsou konečně v textu metodiky, a
katalog neobsahuje slug, který nejde spustit.

Dluh, který tento běh splácel, vznikl tím, že rozhodnutí žilo jen v `status.md` jednoho
běhu. Pravidlo zapsané v záznamu není pravidlo — příští běh ho nenajde.

## Co vzniklo

| Id | Kam | Co říká |
|----|-----|---------|
| R1 | `rules/07-ice-workflow.mdc` | brána znovuotevřená pozdější bránou pokračuje ve svém počítání kol; to kolo nepovoluje Coordinator, ale Human |
| R3 | `rules/07-ice-workflow.mdc` | jeden běh smí měnit záměr i implementovat jen tehdy, když Kritik přijal deltu dřív, než začal Coder |
| R2 | `rules/00-model-policy.mdc` | volba Humana v UI je autoritativní pro roli rodičovského okna; není to odchylka; při kolizi ustupuje druhá role uvnitř katalogu; katalog vládne Coderovi jen když je Coder subagent |
| R4 | `AGENT_MODELS.md` | šest buněk s nespustitelným slugem opraveno |

R1 a R3 přidaly do always-applied pravidla přesně 8 řádků z osmi povolených; soubor má 118
ze 150. `00-model-policy.mdc` má 97 z 250.

## R1 se použilo hned na tento běh

Adversář našel bloker, jehož oprava vyžadovala přidat výstup do plánu, který už Kritik
přijal. Podle R1 — pravidla, které tenhle běh právě psal — si Coordinator takové kolo
nesmí odsouhlasit sám. Eskalováno Humanovi, který rozšíření udělil a rozhodl i věcné otázky.

Stojí za zaznamenání, že pravidlo se osvědčilo dřív, než bylo zacommitované.

## Rozhodnutí Humana

### 1. Katalog na pásmu `high` — zůstává `cursor-grok-4.5-high`

Otázka zněla: když `cursor-grok-4.6-high` nejde předat subagentovi, je lepší novější model
s nižším úsilím (`cursor-grok-4.6-medium`), nebo starší s vyšším (`cursor-grok-4.5-high`)?

**Rozhodnuto: starší s vyšším úsilím.** Pásmo pojmenovává požadované úsilí. Model si to
navíc odpracoval přímo v tomto běhu: jako Kritik našel dva blokery, které Planner přehlédl
— že nespustitelný slug je v katalogu šestkrát, ne dvakrát, a že první znění R2 vypustilo
tři nosné věty z Humanova vlastního rozhodnutí.

### 2. `AGENT_MODELS.explanation.md` — krátká datovaná poznámka, ne přepis

Soubor doporučoval nespustitelný slug a psal, že Grok 4.5 do katalogu nepatří, zatímco
katalog říká opak a na ten soubor se odkazuje jako na svůj podklad.

**Rozhodnuto: poznámka.** Úvaha Humana zůstává, jak byla; mění se jen fakt, který v době
psaní neplatil. Adversář to ve druhém kole označil za lepší volbu, než sám v prvním kole
připouštěl: neplatný je jediný fakt a přepis by smazal stopu, proč se rozhodovalo tak, jak
se rozhodovalo.

### 3. `grader.md` pořizuje Coordinator, ne Coder — **vlastní běh**

Adversář upozornil, že v tomto běhu psal strojový záznam Coder, což je v běhu o „bráně,
kterou si nesmíš odsouhlasit sám" nepříjemné. Čísla byla pravdivá — přeměřil je Adversář i
Coordinator — ale metodika dnes neříká, kdo záznam pořizuje.

**Rozhodnuto: doplnit do metodiky, samostatným během.** Do tohoto běhu se to nepropašuje;
byla by to změna pravidla, kterou Kritik neviděl.

### 4. Sdílený slug Kritika a Codera na `high` — zůstává

Po opravě mají obě role `cursor-grok-4.5-high`. Tvrdé omezení to neporušuje: hlídané je
`adversary_differs_from_coder` a `critic_differs_from_planner`, a Kritik posuzuje práci
Plannera, ne Coderovu.

## Použité modely

| Role | Model | Poznámka |
|---|---|---|
| Coordinator, Planner | `claude-opus-5-thinking-high` | rodičovské okno, volba Humana |
| Critic | `cursor-grok-4.5-high` | katalogový slug pro `high` po opravě |
| Coder | `cursor-grok-4.5-high` | tamtéž |
| Grader | žádný — stroj | |
| Adversary | `claude-opus-5-thinking-high` | jiný model než Coder |

Poprvé bez substituce: katalog po R4 obsahuje jen slugy, které jdou skutečně předat.

## Otevřené nálezy

| # | Co | Druh |
|---|---|---|
| Z4 | Kontrolní tabulka v katalogu jmenuje rodiny bez úsilí („Grok 4.6"), zatímco YAML nad ní rozlišuje `4.6-medium` a `4.5-high` | drobné, nerozhodnuto |
| — | `grader.md` pořizuje Coordinator (rozhodnutí 3) | běh o metodice |

## Navazující práce

| # | Co | Druh |
|---|---|---|
| 1 | `c6` — přeformulovat, nebo rozdělit | rozhodnutí Humana padlo: přeformulovat tak, aby `talks_to` jmenoval |
| 2 | `grader.md` pořizuje Coordinator | běh o metodice |
| 3 | Vynucovač `c7` i na `reverse_code_map` | běžný běh |
| 4 | `_check_identity` i nad `tree.retired` | běžný běh |
| 5 | Rozhodnout, zda `render_slice` a `owner` mají kontrakt | běžný běh |
| 6 | `scope --base <commit>` | běžný běh |
| 7 | Zbylé uzly `i0001`, `i0002`, `i0003`, `i0005` do stavu `realized` | postupně |
| 8 | README, přepínání verzí, merge do `master`, tag v2 | uzavření verze |
