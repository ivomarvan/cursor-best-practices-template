---
run_id: 20260818-1751-model-advisory-25
intent_ids: ["i0002"]
role: Coordinator
model: claude-opus-5-thinking-high
complexity: low
status: done
human_review: performed
scope_guard: failed-and-waived-by-Human
---

# Stav běhu — ohlásit model dřív, než se běh rozjede

## Výsledek

Hotovo. `rules/00-model-policy.mdc` už neříká, že připomenout Humanovi model rodičovského
okna je *courtesy*. Je to povinnost s daným okamžikem a daným obsahem:

> When the Coordinator classifies the run's complexity — before any role starts — it tells
> the Human the classified level, the slug the catalog asks for that role at that level, and
> the slug the parent window is actually running on. After that moment the model choice is
> already spent.

Do odstavce o autoritě Humanovy volby přibyla věta, která říká proč: *An authoritative
choice is an informed one.* Coder zároveň vyhodil slovo `courtesy` a dodatek
„without that reminder", protože po téhle změně by obojí lhalo. To je správný instinkt —
nová věta nemá stát vedle staré, která ji popírá.

Soubor má 101 řádek proti limitu 250 pro pravidlo s `alwaysApply: false`.

## Spadlý scope guard — falešný poplach, prominutý Humanem

`intent scope` skončil s exit 1 a nahlásil nedeklarovanou změnu
`doc/new_ideas/user_ideas_after_first_version_v2.0.md`. Surový výstup je v `grader.md`;
nečistil jsem ho.

Je to falešný poplach z konstrukce nástroje. Ten soubor jsou poznámky Humana, které psal
v chatu, zatímco běh běžel; žádná role ho nečetla ani nezapsala a vlastní diff běhu je
uzavřený v jediné deklarované cestě. Strážce to rozlišit neumí, protože porovnává pracovní
strom proti `HEAD`, ne proti základně pořízené na startu běhu.

Metodika na spadlý scope guard reaguje deterministicky: zvýšit na `medium` a probudit
nezávislou recenzi. Coordinator si tenhle krok neprominul sám — předložil ho Humanovi
i s odůvodněním a **Human bránu prominul**. Zapsáno tady, ne zamlčeno; kdo bude tenhle běh
číst jako precedens, ať čte i to, že prominutí bylo lidské rozhodnutí, ne úleva agenta.

Stalo se to dnes potřetí. Příčina je zapsaná jako námět: strážce rozsahu kouká i do
`doc/new_ideas/`, což je prostor, který nepatří žádnému uzlu stromu a je výslovně Humanův.

## Role a modely

| Role | Model | Kol |
|---|---|---|
| Coordinator + Grader | `claude-opus-5-thinking-high` (volba Humana v UI) | 1 |
| Coder | `cursor-grok-4.6-medium` | 1 |
| Critic, Adversary | neběželi — `low` je nežádá; scope guard je probudil, Human je prominul | — |

## Původ

Human zvažoval novou roli, která by z chatu volala Coordinatora jako subagenta se správným
modelem z katalogu, protože agent si v Cursoru vlastní model nezvolí. Návrh se zamítl:
subagent nemá dokumentovaný kanál pro průběžné hlášení Humanovi, takže by chat po celou
dobu běhu mlčel — a to je právě ta bolest, kterou měl řešit. Zdůvodnění celé je
v `request.md`, ať se k té myšlence dá vrátit se znalostí toho, proč tudy ne.
