---
run_id: 20260817-1703-views-hygiene-dc
intent_ids: ["i0004"]
role: Coder
model: cursor-grok-4.5-high
complexity: high
status: done
---

# Report

## Co bylo implementováno

Text kontraktu `c7` v `i0004` je zúžený na generovaný index (path + depth z řetězce
předků). Vynucovač `c20` ukazuje na přejmenovaný test
`test_a_path_in_a_node_file_does_not_reach_a_generated_view`, jehož jedno tělo dokazuje
obě poloviny: v `build_index` i na řádku uzlu v `render_map` zůstává odvozená cesta, a
`nonsense/place` se v celém `MAP.md` nevyskytuje. Round 2 doplnil chybějící dokumentovou
aserci po REQUEST CHANGES. `test_validate.py`, `generate.py` ani `model.py` se neměnily.

## Vstupy a výstupy

### Přečteno

- `doc/runs/20260817-1703-views-hygiene-dc/slice.md`
- `doc/runs/20260817-1703-views-hygiene-dc/plan.md`
- `doc/runs/20260817-1703-views-hygiene-dc/change.md`
- `doc/runs/20260817-1703-views-hygiene-dc/critique.md`
- `doc/intent/nodes/i0004-intent-tooling.md`
- `tools/intent/tests/test_tools.py`
- `tools/intent/generate.py`
- `tools/intent/model.py`
- `tools/intent/tests/helpers.py`

### Vytvořeno

- `doc/runs/20260817-1703-views-hygiene-dc/grader.md`
- `doc/runs/20260817-1703-views-hygiene-dc/report.md`

### Změněno

- `doc/intent/nodes/i0004-intent-tooling.md`
- `tools/intent/tests/test_tools.py`
- `doc/intent/MAP.md`
- `doc/intent/INDEX.json`

### Nedotčeno

- `tools/intent/tests/test_validate.py`
- `tools/intent/generate.py`
- `tools/intent/model.py`
- `doc/intent/_realization.yaml`

## Použité metody a rozhodnutí

Pořadí asercí je index a pak mapa, aby mutace mířená na jednu stranu `path_of` padla
viditelně na správné polovině. Plán vyžadoval obě kontroly u mapy: odvozenou cestu na
řádku uzlu **a** absenci `nonsense/place` v celém `MAP.md`. V round 1 chyběla
dokumentová aserce — Coder ji zúžil jen na řádek a zapsal to jako vlastní rozhodnutí.
To bylo porušení testovací specifikace plánu; nezávislá recenze (Adversary) to chytila
únikem do mermaid štítku při zelené sadě. Round 2 doplňuje `assertNotIn` nad celým
`text` a nechává řádkovou kontrolu. Hledání řádku má default `None` a srozumitelnou
asercí místo `StopIteration`. Realization claim jsem nezapisoval — to je práce
Coordinátora.

## Reference do kódu

| Soubor | Řádky | Shrnutí |
|--------|-------|---------|
| `doc/intent/nodes/i0004-intent-tooling.md` | 29–31 | nový text `c7` (jen index) |
| `doc/intent/nodes/i0004-intent-tooling.md` | 68–70 | `c20` → přejmenovaný test |
| `tools/intent/tests/test_tools.py` | 145–170 | index, řádek mapy i absence v celém `MAP.md` |

## Důkazy

| Příkaz | Výsledek | Exit code |
|--------|----------|-----------|
| mutace 1 (`path` + `build_index`) | padla indexová polovina | 1 |
| mutace 2 (`path` + `render_map` tabulka) | padla mapová polovina (řádek) | 1 |
| mutace 3 (`path` + mermaid label) | padla dokumentová `assertNotIn` | 1 |
| suite po revertu mutací | 82 OK | 0 |
| `python3 tools/intent/cli.py validate` | 0 error(s), 0 warning(s) | 0 |
| `python3 tools/intent/cli.py realization check` | layer consistent; `i0004` stale | 0 |
| `python3 -m unittest discover -s tools/intent/tests -t tools` | 82 OK | 0 |
| `python3 tools/checks/template_checks.py --root .` | satisfied | 0 |
| `python3 tools/checks/hook_checks.py --root .` | satisfied | 0 |
| `python3 tools/intent/cli.py scope --run doc/runs/20260817-1703-views-hygiene-dc` | scope clean | 0 |
| `ruff check tools/` | All checks passed | 0 |
| `ruff format --check tools/` | 19 files already formatted | 0 |

Surový záznam je v `grader.md` (round 2 append-only).

## Definition of Done

`c7` už netvrdí depth o `MAP.md`; `c20` má jeden test, který drží oba pohledy včetně
absence zapsané cesty v celém `MAP.md`. Žádný kontrakt neukazuje na neexistující
symbol. Tři mutace jsou v `grader.md` s pádem a návratem do zelené. Brány validate /
realization / unittest / template / hook / scope i ruff končí 0. Realization claim na
`i0004` záměrně chybí — zapíše ho Coordinator.
