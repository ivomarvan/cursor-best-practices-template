---
run_id: 20260818-1651-verdict-reopening-0d
intent_ids: ["i0002"]
role: Coder
model: cursor-grok-4.6-medium
complexity: low
status: done
outputs: ["rules/07-ice-workflow.mdc"]
incidental: []
---

# Plán

Doplnit do `rules/07-ice-workflow.mdc` jednu až dvě věty: verdikt `APPROVE` nebo
`ACCEPT` je uzavřený i s neblokujícími follow-upy v něm; znovu ho otevřít smí jen
Human; Coordinator nález zapíše jako známý limit a běh uzavře, nebo se zeptá;
blokátor znamená, že verdikt nikdy uzavřený nebyl.

Umístění: hned za odstavec o bráně znovu otevřené *pozdější* bránou. Ten text není
v `## Gates`, ale v `## Roles`, kde se počítají kola. Tam vedle sebe stojí dva
odlišné případy: znovuotevření po *selhání* jinde versus znovuotevření verdiktu, který
*prošel*. `## Always the Human` už pokrývá „any escalation“ a snižování složitosti;
opakovat totéž tam by bylo skládání. `## Gates` zůstává tabulkou, které brány
platí na které úrovni.

Test spec (próza, žádný jednotkový test): enforcer `template_checks.py` soubor
dosáhne — dočasně rozbitý relativní odkaz, exit 1 a jméno souboru, návrat, exit 0.

# Report

## Co bylo implementováno

Dvě věty v `## Roles` souboru `rules/07-ice-workflow.mdc`, hned po pravidle o bráně
znovu otevřené pozdější bránou:

> An `APPROVE` or `ACCEPT` is closed, including any follow-up the reviewer marked as
> non-blocking in it; a blocker means that verdict was never closed. Reopening a closed
> verdict for such a finding is the Human's call; the Coordinator records the finding as
> a known limit and closes, or asks.

## Vstupy a výstupy

### Přečteno

- `doc/runs/20260818-1651-verdict-reopening-0d/request.md`
- `doc/runs/20260818-1651-verdict-reopening-0d/slice.md`
- `doc/intent/nodes/i0001-harness.md`
- `doc/intent/nodes/i0002-rules.md`
- `rules/07-ice-workflow.mdc`
- `rules/07-run-artifacts.mdc`
- `VERIFY.md`
- `tools/checks/template_checks.py`

### Vytvořeno

- `doc/runs/20260818-1651-verdict-reopening-0d/run.md`

### Změněno

- `rules/07-ice-workflow.mdc`

### Nedotčeno

- `doc/intent/nodes/i0002-rules.md`
- `skills/ice-run/SKILL.md`
- `hooks/`

## Použité metody a rozhodnutí

Související pravidlo („gate reopened by a later gate“) žije v `## Roles`, ne v
`## Gates`. Nová věta tam patří, protože rozlišuje úspěšný verdikt od selhání a
Coordinator kola počítá právě v této sekci. `## Always the Human` by rozhodnutí
přiřadilo správné osobě, ale zdvojilo by „any escalation“ a oddělilo by je od
počítání kol. `## Gates` by větu strčilo do tabulky, která říká *které* brány
běží, ne *kdy se smí znovu otevřít uzavřená*.

## Reference do kódu

| File | Lines | Summary |
|------|-------|---------|
| `rules/07-ice-workflow.mdc` | 59–62 | Closed `APPROVE`/`ACCEPT`; Human reopens; blocker ≠ closed |

Před: 118 řádků. Po: 123. Limit `alwaysApply`: 150.

## Důkazy

Dočasná mutace: odkaz `[missing](does-not-exist.md)` na konci existujícího odstavce
o znovuotevřené bráně. Po zachycení výstupu vráceno; ve working tree zůstala jen
zamýšlená změna.

```
ERROR /home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/rules/07-ice-workflow.mdc: broken link: does-not-exist.md

1 template contract violation(s)
EXIT:1
```

Po návratu a po doplnění vět:

```
template contracts satisfied
EXIT:0
```

| Command | Result | Exit code |
|---------|--------|-----------|
| `python3 tools/checks/template_checks.py --root .` (broken link) | names `rules/07-ice-workflow.mdc` | 1 |
| `python3 tools/checks/template_checks.py --root .` | `template contracts satisfied` | 0 |
| `python3 tools/intent/cli.py validate` | `5 node(s): 0 error(s), 0 warning(s)` | 0 |
| `python3 -m unittest discover -s tools/intent/tests -t tools` | `Ran 99 tests` / `OK` | 0 |
| `python3 tools/intent/cli.py realization check` | `realization layer consistent` | 0 |
| `python3 tools/checks/hook_checks.py --root .` | `hook contracts satisfied` | 0 |
| `wc -l rules/07-ice-workflow.mdc` | `123` (limit 150) | 0 |

## Definition of Done

Věta je v `rules/07-ice-workflow.mdc` v `## Roles` vedle pravidla o znovuotevření
brány selháním. Enforcer soubor pojmenoval při rozbitém odkazu a po opravě prošel.
`intent validate`, unittest sada a `template_checks.py` končí 0. Soubor má 123
řádků, pod limitem 150. Tento `run.md` nese plán, report a surový výstup mutace.
