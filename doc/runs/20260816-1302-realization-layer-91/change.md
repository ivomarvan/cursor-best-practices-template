---
run_id: 20260816-1302-realization-layer-91
intent_ids: ["i0004"]
role: Planner
model: claude-opus-5-thinking-high
complexity: high
status: in-progress
---

# Změna záměru

## Nejvyšší uzel, kterého se změna dotýká

`i0004 — Intent tooling`. Vrstva realizace je další příkaz nástroje nad stromem záměru,
takže nezakládá nový uzel; rozšiřuje význam a závazky uzlu, který už nástroj vlastní.

Uzel `i0001` (harness) se nemění: nic v novém mechanismu neodporuje jeho významu ani
jeho kontraktům. `i0002` (rules) se nemění co do významu — přibývá pravidlo, ale význam
„pravidla jsou krátká, aktivovaná deklarativně" platí dál a nové pravidlo se do rozpočtu
vejde.

## Změněné uzly

| Uzel | Změna | Typ |
|------|-------|-----|
| `i0004` | `## Meaning`: mezi rodiny skriptů přibyla vrstva realizace | rozšíření výkladu |
| `i0004` | `## Contracts`: odstavec o tom, co hlídají nové kontrakty | výklad |
| `i0004` | `## Non-goals`: nástroj není nástěnka CI | **zpřísnění** |
| `i0004` | kontrakty `c8`–`c17` | **přidání** |

Žádný kontrakt nebyl oslaben ani odstraněn. `c1`–`c7` mají nezměněný text i vynucovač.
Podle axiomu A4 je přidání a zúžení legální bez lidského povolení; oslabení by nebylo.

## Nové kontrakty a jejich vynucovače

| Id | Tvrzení | Vynucovač |
|----|---------|-----------|
| `c8` | změna významu uzlu zneplatní tvrzení, že je realizovaný | `test_changing_the_meaning_makes_a_claim_stale` |
| `c9` | nedokázaný předek neblokuje dokázaného potomka | `test_unproven_ancestor_does_not_block_a_child` |
| `c10` | šíření po hraně `uses` končí po jednom kroku | `test_uses_propagation_stops_after_one_hop` |
| `c11` | kontrakt se zmizelým vynucovačem se dostane do worklistu | `test_a_broken_node_appears_in_the_worklist` |
| `c12` | tvrzení podepsané Coderem je odmítnuto | `test_coder_may_not_claim_its_own_work` |
| `c13` | lidský souhlas podepsaný agentní rolí je odmítnut | `test_an_agent_may_not_accept` |
| `c14` | kontrola rozsahu vrstvu vždy povolí, takže běh neshodí vlastní bránu | `test_scope_guard_always_allows_the_realization_layer` |
| `c15` | změna kontraktů cíle hrany `uses` otevře spotřebitele | `test_uses_target_contract_change_opens_the_consumer` |
| `c16` | změna významu cíle hrany `uses` se ke spotřebiteli nedostane | `test_uses_target_meaning_change_leaves_the_consumer_alone` |
| `c17` | vynucovač přejmenovaný na delší symbol platí za chybějící, ne za přítomný | `test_a_renamed_enforcer_symbol_makes_a_node_broken` |

Všech deset jsou strojové testy v `tools/intent/tests/test_realization.py`. Žádný nový
kontrakt není `enforced_by: review`, takže `intent coverage` nepřibývá výjimka a profil
souhlasu `standard` u `i0004` souhlas nevyžaduje.

**Zúženo po kritice, dvakrát.** První verze měla `c8`–`c14`, přičemž `c9` a `c10`
spojovaly středníkem dvě nezávisle rozbitelná tvrzení, ale jejich `enforced_by` prokazoval
jen první polovinu. Kontrakt, jehož text sahá dál než jeho vynucovač, je přesně ten druh
přání, který má `enforced_by` vylučovat.

Druhá verze tu vadu recyklovala: `c15` zněl „přenese změnu kontraktů, **ale nikdy** změnu
významu" — zase dvě tvrzení pod jedním testem, který dokazoval jen to druhé. Obě recenzní
brány to našly nezávisle na sobě. Teprve třetí verze má pravidlo bez výjimky: **jeden
kontrakt = jedno tvrzení = jeden test, který přesně to tvrzení prověřuje.** Kladná i
záporná polovina šíření po hraně `uses` má vlastní kontrakt (`c15`, `c16`) a vlastní test;
žádný test v souboru už není osiřelý. Pravidlo je zapsané v `## Contracts` uzlu, aby
příští změna nemusela objevovat totéž potřetí. `c17` vzešel z nálezu Adversáře.

## Dotčené hrany

Žádná. Nepřibyla ani neubyla hrana `uses` ani `talks_to`; `parent` uzlu `i0004` zůstává
`i0001`. Otisk významu proto nemá důvod se hnout z titulu hran, jen z titulu textu.

## Proč to nezakládá nový uzel

Podle axiomu A6 (frugalita) uzel vzniká tam, kde nese kontrakt nebo význam, který rodič
nedrží. Vrstva realizace žádný samostatný význam nemá — je to odpověď nástroje na otázku
nad stromem, stejně jako `slice` nebo `coverage`.

První verze tohoto odstavce tvrdila, že vlastní uzel by dával smysl, až kdyby vrstva měla
vlastní úložiště. Kritik ukázal, že si tím dokument protiřečí: `_realization.yaml`
vlastní úložiště **je**. Argument tedy nestojí na úložišti, ale na dvou jiných faktech:
`code_paths` a `test_paths` uzlu `i0004` se nezměnily (nový modul leží uvnitř `tools/`,
které uzel už vlastní), a vrstva nemá rozhraní pro nikoho zvenčí. Uzel by si zasloužila
teprve tehdy, kdyby ji začal konzumovat samostatný produkt — nejpravděpodobněji editor
stromu záměru — protože pak by měla závazky vůči někomu jinému než vůči nástroji samotnému.

## Rozsah zastarání, který změna způsobila

Žádný. Vrstva byla před tímto během prázdná, takže neexistovalo tvrzení, které by se dalo
zneplatnit — `i0004` byl `not_claimed` před změnou i po ní. Ověřeno:
`intent realization worklist` hlásí všech pět uzlů jako `not_claimed`, žádný `stale`.

Tohle je vědomě nejlevnější možný okamžik na takhle širokou změnu záměru a je to jediný
důvod, proč se v jednom běhu smí sejít změna stromu i implementace: nemá to koho ranit.
