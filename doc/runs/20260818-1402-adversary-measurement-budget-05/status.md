---
run_id: 20260818-1402-adversary-measurement-budget-05
intent_ids: ["i0003"]
role: Coordinator
model: claude-opus-5-thinking-high
complexity: low
status: done
human_review: skipped
skipped_by: Coordinator
skip_reason: "complexity=low; grader passed; scope clean; no intent change; two sentences of procedure"
---

# Stav běhu — rozpočet měření pro Adversáře

## Výsledek

Hotovo. Do `skills/ice-review/SKILL.md` přibyl strop měření v jednotkách práce a povinná
sekce `What I did not measure`; do Kroku 8 v `skills/ice-run/SKILL.md` přibyla povinnost
Coordinátora ten strop a pořadí priorit **zadat**. Věta „Adversář nemůže dodržet rozpočet,
který jsi nevyslovil" nese celou pointu.

## Role a modely

| Role | Model | Kol |
|---|---|---|
| Coordinator + Grader | `claude-opus-5-thinking-high` (volba Humana v UI) | — |
| Coder | `cursor-grok-4.6-medium` | 1 |
| Critic | neběžel — `low` ho nežádá | — |
| Adversary | neběžel — `low` ho nežádá | — |

## Brány

Všechny zelené v prvním kole: `validate` 5 uzlů bez chyby, `scope clean (2 declared)`,
`realization check consistent`, oba `checks` skripty, 99 testů, `coverage` 28 z 28.
Surový výstup v `grader.md`.

Doklad dosahu enforceru: Coder dočasně vložil do `skills/ice-review/SKILL.md` odkaz na
neexistující soubor, `template_checks.py` skončil 1 a soubor jmenoval; po revertu 0.
Je to jediná forma „failing-test evidence", která u prózy dává smysl.

## Nárok

`i0003` byl nárokovaný už v běhu `…-1743-methodology-debt-ea`. Nárokoval jsem ho znovu
proti tomuto běhu, aby doklad ukazoval na běh, jehož brány běžely nad **současným** kódem.
Není to opravná akce — obě věty `i0003` platily i předtím. Otisky pokrývají jen text uzlu,
takže změna kódu pod uzlem nárok sama nezčervená; to je vědomé rozhodnutí z návrhu vrstvy,
ne mezera, kterou by tenhle nárok zakrýval.

## Proč běh sám o sobě

Rozdělil jsem původně zamýšlený běh D na dva. Human chtěl obojí najednou, ale routing
ukázal, že by běh sáhl na tři uzly — `i0005` (hook), `i0004` (`hook_checks.py`) a `i0003`
(skills). To je přesně ta šíře, kterou předchozí běh doplatil. Navíc má tohle pravidlo
platit **pro** hookový běh, takže musí vzniknout dřív než on.

## Co zůstává

Nic z tohoto běhu. Oprava hooku (B4, B5, B6 a FU-10 … FU-16) je předmětem samostatného
běhu, který začíná z `deferred-i0005-hook.patch` v adresáři běhu `…-0853-…`.
