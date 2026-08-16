---
run_id: 20260816-1302-realization-layer-91
intent_ids: ["i0004"]
role: Planner
model: claude-opus-5-thinking-high
complexity: high
status: in-progress
outputs:
  - tools/intent/realization.py
  - tools/intent/tests/test_realization.py
  - tools/intent/main.py
  - tools/intent/model.py
  - tools/intent/scope.py
  - tools/intent/slicing.py
  - tools/intent/validate.py
  - doc/intent/nodes/i0004-intent-tooling.md
  - doc/intent/_policy.yaml
  - rules/07-realization.mdc
  - rules/07-ice-workflow.mdc
  - rules/07-intent-tree.mdc
  - rules/07-run-artifacts.mdc
  - skills/ice-run/SKILL.md
  - skills/ice-implement/SKILL.md
  - skills/ice-review/SKILL.md
  - skills/intent-change/SKILL.md
  - VERIFY.md
  - README.md
  - doc/new_ideas/intent-realization.Opus5.md
  - doc/new_ideas/intent-realization-status.critique-Opus5.md
incidental:
  - doc/intent/_realization.yaml
  - doc/intent/MAP.md
  - doc/intent/INDEX.json
  - doc/new_ideas/ice-agentic-sdlc.Opus5.md
  - doc/new_ideas/ice-agentic-sdlc.Opus5.current_version.md
  - doc/new_ideas/living-intent-sdlc.md
  - doc/new_ideas/living-intent-sdlc.CursorGrog4.4.work_version.md
  - doc/new_ideas/intent-realization-status.concept.md
  - doc/new_ideas/intent_tree_editor.first_notices.md
---

# Plán

## Cíl

Otázka „co ještě zbývá udělat" má po tomto běhu strojovou odpověď: příkaz, který ze
stromu záměru a z uložených tvrzení spočítá seznam uzlů vyžadujících práci, u každého
uvede důvod a označí ty, které čekají na předka.

Měřitelně: `intent realization worklist` na projektu s prázdnou vrstvou vypíše všechny
`current` uzly jako `not_claimed`; po zapsání tvrzení uzel ze seznamu zmizí; po změně
textu uzlu se do něj vrátí s důvodem.

## Výstupy

Deklarované výše. Tři skupiny:

1. **Nástroj** — nový modul `realization.py`, osm podpříkazů v `main.py`, řádek stavu
   v řezu (`slicing.py`), výjimka pro vrstvu v kontrole rozsahu (`scope.py`), konstanty
   cest (`model.py`) a vytažení kontroly dosažitelnosti vynucovače z `validate.py` tak,
   aby ji obě vrstvy sdílely.
2. **Záměr a jeho důkazy** — kontrakty `c8`–`c14` na `i0004`, testy, `_policy.yaml`,
   řádek `realization check` ve `VERIFY.md`.
3. **Metodika a výklad** — nové pravidlo, čtyři skills, oddíl v `README.md`.

Dva soubory v `doc/new_ideas/` jsou ve výstupech, ne mezi průvodními: koncepční dokumenty
se během implementace ukázaly být na dvou místech v rozporu se skutečností (viz report),
a nechat je rozejít se s kódem by z nich udělalo past.

## Průvodní soubory

`MAP.md` a `INDEX.json` se přegenerují změnou kontraktů `i0004`. `_realization.yaml`
vznikne prvním tvrzením. Šest souborů v `doc/new_ideas/` je v pracovním stromě **z doby
před tímto během** (rozpracované koncepty a poznámky Humana) — tento běh se jich nedotkl,
ale kontrola rozsahu je vidí, takže jsou přiznané tady, ne omluvené až dodatečně.

## Testovací specifikace

Pro každou skupinu chování šťastná cesta, hrana a chybový stav:

| Skupina | Šťastná cesta | Hrana | Chyba |
|---------|---------------|-------|-------|
| Otisky | změna `## Meaning` změní otisk | přeuspořádání kontraktů a přejmenování uzlu otisk nezmění | — |
| Tvrzení | `claim` udělá z uzlu `realized` | důkaz v profilu `relaxed` smí být `VERIFY.md` | `claim` odmítne Codera, otevřenou otázku i důkaz bez `grader.md` |
| Zastarání | změna vlastního významu → `stale` | změna předka otevře podstrom a nastaví `blocked_by` | nedokázaný předek potomka **ne**blokuje |
| Hrana `uses` | změna kontraktů cíle otevře spotřebitele | změna významu cíle spotřebitele nechá být | šíření končí po jednom kroku |
| Rozbitý vynucovač | smazaný test → `broken` | `broken` uzel je ve worklistu | — |
| Potvrzení a souhlas | `affirm` vrátí tvrzení do `realized` | `--subtree` potvrdí i potomky s tvrzením | agentní role je u `affirm` i `accept` odmítnuta |
| Uložení | tvrzení přežije zápis a načtení | prázdná vrstva se uloží a načte | záznam pro neexistující uzel hlásí `R1` |

Navíc **negativní ověření návrhového rozhodnutí**: dočasně přepnout šíření na zamítnutou
variantu (stav se šíří stejně jako text) a doložit, které testy spadnou. Bez toho je
tvrzení „tyhle testy hlídají rozhodnutí Q4" nepodložené.

## Definition of Done

- [ ] `intent validate` končí 0 a generované soubory jsou aktuální
- [ ] `intent realization check` končí 0
- [ ] Celá sada `tools/intent/tests` je zelená
- [ ] `template_checks` a `hook_checks` končí 0 (rozpočty řádků pravidel a skills)
- [ ] `ruff check` a `ruff format --check` nad `tools/` jsou čisté
- [ ] Sedm nových kontraktů `i0004` ukazuje na existující testovací symboly
- [ ] Doloženo, že nové testy padají pod zamítnutou variantou šíření
- [ ] Zápisové příkazy ověřeny přes CLI, ne jen voláním funkcí
- [ ] `README.md` popisuje vrstvu včetně toho, co se ukládá a co se počítá
- [ ] Kontrola rozsahu končí 0 proti tomuto plánu

## Co plán vědomě nedělá

- Nezakládá tvrzení za uzly `i0001`–`i0003` a `i0005`. Tento běh dokazuje `i0004`;
  ostatní zůstávají `not_claimed`, což je pravda, ne dluh přehlédnutím.
- Nezavádí stav do `MAP.md` ani `INDEX.json`. Ty jsou hlídané na aktuálnost pravidlem V9
  a rychle se měnící sloupec by tu bránu shazoval po každém tvrzení.
- Neřeší uživatelské rozhraní. Vrstva jen musí umět `--json`.
