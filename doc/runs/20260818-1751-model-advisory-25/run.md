---
run_id: 20260818-1751-model-advisory-25
intent_ids: ["i0002"]
role: Coder
model: cursor-grok-4.6-medium
complexity: low
status: done
outputs: ["rules/00-model-policy.mdc"]
incidental: []
---

# Plán

## Cíl

Sekce `## Cursor limitation` v `rules/00-model-policy.mdc` pojmenuje povinnost Coordinátora
ohlásit model rodičovského okna ve chvíli klasifikace složitosti: úroveň, slug z katalogu
pro tu roli a úroveň, a slug, na kterém okno skutečně běží. Stávající významy sekce
(Cursor nepřepíná model rodiče, volba Humana je autoritativní, není to odchylka, srážka
s tvrdým omezením, Coder mimo katalog když píše v rodiči) zůstanou beze změny.

## Výstupy

- `rules/00-model-policy.mdc` — jediný soubor.

## Testovací specifikace

Prozaické pravidlo nemá unit test. Důkaz, že enforcer `i0001` c1 sahá na tento soubor:
dočasně vložit relativní odkaz na neexistující soubor, `template_checks.py` musí skončit
kódem 1 a jmenovat `rules/00-model-policy.mdc`; po vrácení kód 0. Hranice řádků:
`alwaysApply: false` → scoped limit 250 (`i0002` c2).

## Definition of Done

Povinnost s momentem a obsahem v pravidle; `template_checks.py`, `intent validate` a
`unittest` zelené; počet řádků pod limitem; tento `run.md`.

# Report

## Co bylo implementováno

V `rules/00-model-policy.mdc`, sekce `## Cursor limitation`, je z laskavosti bez okamžiku
povinnost s okamžikem a obsahem. Mechanismus Cursoru, autoritativnost volby Humana,
srážka s tvrdým omezením a věta o Coderovi v rodičovském okně zůstaly.

## Vstupy a výstupy

### Přečteno

- `doc/runs/20260818-1751-model-advisory-25/request.md`
- `doc/runs/20260818-1751-model-advisory-25/slice.md`
- `doc/intent/nodes/i0001-harness.md`
- `doc/intent/nodes/i0002-rules.md`
- `rules/00-model-policy.mdc`
- `tools/checks/template_checks.py`
- `VERIFY.md`

### Vytvořeno

- `doc/runs/20260818-1751-model-advisory-25/run.md`

### Změněno

- `rules/00-model-policy.mdc`

### Nedotčeno

- `skills/ice-run/SKILL.md`
- `doc/intent/nodes/i0002-rules.md`
- `AGENT_MODELS.md`

## Použité metody a rozhodnutí

Nová věta má vlastní odstavec mezi mechanismem (co Cursor neumí) a autoritou (co platí,
když se volba Humana střetne s katalogem). Do prvního odstavce by zapadla jako další
souvětí bez okamžiku — přesně ten stav, který se měnil. Před srážku s tvrdým omezením
nepatří: to je jiný rozhodovací uzel.

Žádné stávající odstavce se nepřesouvaly. Z prvního odstavce zmizela věta o courtesy;
SDK věta přišla o „without that reminder“, protože připomínka už není volitelná, a
říká totéž: plná automatizace rodičovského okna potřebuje SDK nebo Cloud Agents.
Do odstavce o autoritě přibyly dvě věty, které by jinak dublovaly „katalog na tu roli
neplatí“: „An authoritative choice is an informed one.“ (proč hlásit) a „The Human may
continue unchanged.“ (pokračovat beze změny nic neporušuje). Collision a Coder odstavce
jsou beze změny.

## Reference do kódu

| File | Lines | Summary |
|------|-------|---------|
| `rules/00-model-policy.mdc` | 79–101 | `## Cursor limitation`: mechanismus, povinnost při klasifikaci, autorita, srážka, Coder |

Přesné znění nového odstavce a doplnění:

```
When the Coordinator classifies the run's complexity — before any role starts — it tells
the Human the classified level, the slug the catalog asks for that role at that level, and
the slug the parent window is actually running on. After that moment the model choice is
already spent.
```

Do odstavce o autoritě: `An authoritative choice is an informed one.` a `The Human may continue unchanged.`

## Důkazy

Řádky: před 97, po 101. `alwaysApply: false`, bez `globs` → scoped limit **250**
(`ALWAYS_APPLY_LIMIT` 150 se neuplatní).

Failing-test evidence (dočasný odkaz `[missing](does-not-exist.md)` v prvním odstavci
sekce, pak revert):

```
ERROR /home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/rules/00-model-policy.mdc: broken link: does-not-exist.md

1 template contract violation(s)
EXIT:1
```

Po revertu: `template contracts satisfied`, `EXIT:0`.

| Command | Result | Exit code |
|---------|--------|-----------|
| `python3 tools/checks/template_checks.py --root .` (broken link) | names `rules/00-model-policy.mdc` | 1 |
| `python3 tools/checks/template_checks.py --root .` | template contracts satisfied | 0 |
| `python3 tools/intent/cli.py validate` | 5 node(s): 0 error(s), 0 warning(s) | 0 |
| `python3 tools/intent/cli.py realization check` | realization layer consistent | 0 |
| `python3 -m unittest discover -s tools/intent/tests -t tools` | Ran 99 tests, OK | 0 |
| `python3 tools/checks/hook_checks.py --root .` | hook contracts satisfied | 0 |
| `python3 tools/intent/cli.py scope --run doc/runs/20260818-1751-model-advisory-25 --node i0002` | `undeclared change: doc/new_ideas/user_ideas_after_first_version_v2.0.md` | 1 |

Cílená změna je jen `rules/00-model-policy.mdc`. Scope hlásí untracked
`doc/new_ideas/user_ideas_after_first_version_v2.0.md`, který tento běh nevytvořil ani
needitoval a který proto není v `outputs` ani `incidental`.

## Definition of Done

Povinnost je v pravidle s momentem (klasifikace složitosti, před startem rolí) a obsahem
(úroveň, katalogový slug, skutečný slug okna). Enforcer na soubor sahá (exit 1 se jménem
souboru, pak exit 0). VALIDATE, unittest i template_checks po revertu končí 0. 101 řádků
je pod scoped limitem 250. Tento `run.md` je zapsaný. Realization claim nepatří Coderovi.
