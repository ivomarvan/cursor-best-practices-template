---
run_id: 20260818-1651-verdict-reopening-0d
intent_ids: ["i0002"]
role: Coordinator
model: claude-opus-5-thinking-high
complexity: low
status: done
human_review: skipped
skipped_by: Coordinator
skip_reason: "complexity=low; grader passed; scope clean; no intent change; the Human approved the substance before the run started"
---

# Stav běhu — kdo smí znovu otevřít uzavřený verdikt

## Výsledek

Hotovo. Do `rules/07-ice-workflow.mdc` přibyly dvě věty:

> An `APPROVE` or `ACCEPT` is closed, including any follow-up the reviewer marked as
> non-blocking in it; a blocker means that verdict was never closed. Reopening a closed
> verdict for such a finding is the Human's call; the Coordinator records the finding as
> a known limit and closes, or asks.

## Umístění

Coder je dal do `## Roles`, hned za pravidlo o bráně znovu otevřené pozdější bránou,
a zdůvodnil to lépe, než zněl požadavek. Ta dvě pravidla teď stojí vedle sebe jako dvojice
a rozdíl mezi nimi je vidět: první řeší bránu znovu otevřenou **selháním** jinde, druhé
verdikt, který **prošel**. `## Gates` zůstává tabulkou, které brány běží, ne kdy se smí
znovu otevřít uzavřená. Do `## Always the Human` by to bylo duplicitní vůči „any
escalation".

## Role a modely

| Role | Model | Kol |
|---|---|---|
| Coordinator + Grader | `claude-opus-5-thinking-high` (volba Humana v UI) | 1 |
| Coder | `cursor-grok-4.6-medium` | 1 |
| Critic, Adversary | neběželi — `low` je nežádá | — |

## Brány

Zelené v prvním kole. `validate` 5 uzlů bez chyby, `scope clean (1 declared)`, oba `checks`
skripty, 99 testů, `realization check consistent`. Soubor 123 řádek proti limitu 150.

Doklad dosahu enforceru: dočasný odkaz na neexistující soubor, `template_checks.py`
skončil 1 a soubor jmenoval; po revertu 0.

## Human gate

Přeskočený, ale ne mlčky. Human schválil **podstatu** pravidla dřív, než běh začal —
rozhodl o ní, když mu Coordinator přiznal chybu v kole 2 běhu `…-1414-…` a nabídl mu
varianty. Tenhle běh je zápis jeho rozhodnutí, ne návrh; `low` navíc Human review nežádá.

## Původ

Pravidlo vzniklo z konkrétní chyby: Coordinator si v běhu `…-1414-…` vyžádal kolo navíc,
aby z Adversářova `APPROVE` zmizela pojmenovaná výhrada k tvaru, který git nikdy nevyrobí.
Oprava rozbila tvar, který git vyrábí běžně, a celé kolo se muselo vrátit. Text pravidla
o tom mlčí, jak má — pravidlo říká, co platí, ne odkud přišlo. Historie je v `doc/runs/`.
