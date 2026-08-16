---
run_id: 20260816-1302-realization-layer-91
intent_ids: ["i0004"]
role: Critic
model: claude-sonnet-5-thinking-high
complexity: high
status: done
---

# Kritika změny záměru (kolo 3 — poslední)

## Verdikt
ACCEPT

Všech deset kontraktů, které tento běh přidává (`c8`–`c17`), teď splňuje vlastní pravidlo,
které si běh zapsal do `## Contracts`: jeden kontrakt = jedno tvrzení = jeden test, který
přesně to tvrzení prověřuje. `c9`, `c10` (kolo 1) a `c15`/`c16` (kolo 2, dřív `c15`) jsou
opravené správně a žádný nový výskyt stejné vady jsem v `c8`–`c17` nenašel. `c1`–`c7`
jsem podle stejného kritéria prošel navíc, mimo mandát tohoto běhu — dva z nich (`c4`,
`c7`) mají tutéž vadu, ale jde o **informaci pro Human, ne o důvod tenhle běh blokovat**,
protože předcházejí tomuto běhu a nikdo je v tomto běhu nepsal ani nesliboval opravit.

## Co se opravilo správně (kolo 2 → kolo 3)

- **`c15`/`c16` rozdělené.** Bývalý `c15` ("carries a change of contracts... but never a
  change of meaning") je teď dva kontrakty s jedním tvrzením každý:
  - `c15` "A change of contracts on a uses target opens its consumer" →
    `test_uses_target_contract_change_opens_the_consumer` — test mění `target`'s kontrakt
    a ověřuje `consumer.state == "stale"` s důvodem `"used {target} changed contracts"`.
    Přesný zásah, žádný zbytek tvrzení navíc.
  - `c16` "A change of meaning on a uses target never reaches its consumer" →
    `test_uses_target_meaning_change_leaves_the_consumer_alone` — test mění `target`'s
    `## Meaning` a ověřuje `target.state == "stale"` ale `consumer.state == "realized"`.
    Přesný zásah.
  - Žádný test v souboru už není osiřelý: `test_uses_target_contract_change_opens_the_consumer`
    (dřív bez vazby na kontrakt) je teď formálně `enforced_by` pro `c15`.
- **`c17`** (přejmenovaný z kola-2 `c16`) beze změny textu ani testu — pořád přesný zásah,
  ověřil jsem znovu i implementaci `tools/intent/validate.py::enforcer_problem` (regex s
  hranicí slova místo substring matche), beze změny od kola 2.
- **Próza `c8`–`c14` → `c8`–`c17`** opravena v `## Contracts`, teď odpovídá skutečnému
  rozsahu.
- **Nové pravidlo zapsané do uzlu** ("Each contract states exactly one thing... A sentence
  joined by a semicolon or by 'but never' carries a second claim...") je samo o sobě nová,
  konkrétní, ověřitelná informace o uzlu `i0004` — splňuje A3 (nerestatuje rodiče, `i0001`
  o tomhle nic neříká) a je to zpřísnění postupu psaní kontraktů v tomto uzlu, ne prázdná
  próza: dá se jím mechanicky projít každý budoucí kontrakt (přesně jak to dělám teď).
- **A6 argument** v `change.md` beze změny od kola 2 — pořád stojí na nezměněných
  `code_paths`/`test_paths` a chybějícím rozhraní pro jiný produkt. Platí i teď (viz níže).

## Aplikace vlastního kritéria na c1–c17

Kritérium z nového odstavce: **kontrakt smí tvrdit jen to, co jeho `enforced_by` skutečně
dokazuje; věta spojená středníkem nebo "but never" je podezřelá, pokud ty dvě poloviny
nedokazuje jeden a týž test.** (Výjimka: pokud je druhá polovina přímý logický důsledek
první — jako u `c14` — nejde o druhé nezávislé tvrzení a není co dělit.)

| Id | V rozsahu běhu? | Tvrzení = 1 test dokazuje celé? | Nález |
|----|------------------|-----------------------------------|-------|
| `c1` | mimo | Ano — jednoduché tvrzení, `test_dump_then_parse`. | Bez nálezu. |
| `c2` | mimo | Ano — "rejected, never ignored" je jeden jev (vyvolání výjimky), ne dvě nezávislá tvrzení; `test_anchor_is_rejected` ho dokazuje celý. | Bez nálezu. |
| `c3` | mimo | Ano — `test_minimal_valid_tree_has_no_errors`. | Bez nálezu. |
| `c4` | **mimo, ale nalezeno** | **Ne.** "may overlap only along the ancestor chain, **never** between siblings" je dvě nezávislá tvrzení. `enforced_by` je `test_siblings_may_not_overlap`, který dokazuje jen zápornou polovinu (sourozenci nesmí). Kladnou polovinu ("along the ancestor chain" smí) dokazuje `test_validate.py::test_parent_and_child_may_overlap` — existující test, ale **není** `enforced_by` žádného kontraktu. | **Informace pro Human** — stejná vada jako `c9`/`c10`/`c15` v tomto běhu, ale v uzlu odjakživa, žádný soubor tohoto běhu se `c4` nedotýká. Nedoporučuji blokovat tento běh kvůli ní. |
| `c5` | mimo | Ano — "is an error, not a warning" je jedna binární klasifikace (nález má jediné pole `level`); `test_contract_pointing_at_missing_test_is_rejected` ji ověřuje tím, že `V5` najde v `codes(tree)` (defaultně `level="error"`). Není to nezávisle rozbitelné druhé tvrzení jako u `c4`. | Bez nálezu. |
| `c6` | mimo | Ano — "ancestors **and** semantic dependencies **but never** siblings" zní jako tři tvrzení, ale `test_slice_contains_ancestors_and_uses_but_not_siblings` je **všechny tři** ověřuje v jednom těle (`assertIn(root, ancestors)`, `assertIn(shared, uses)`, `assertNotIn(sibling, joined)`). Na rozdíl od `c4`/`c9`/`c10`/`c15` tu nejde o rozdělení mezi dva testy. | Bez nálezu. |
| `c7` | **mimo, ale nalezeno** | **Ne.** "exist only in generated views, **never** in a node file" — `test_index_holds_derived_path_and_depth` dokazuje jen kladnou polovinu (index nese `path`/`depth`). Zápornou polovinu (uzel front matter je nikdy nenese) nedokazuje **žádný** test v souboru — je to slabší případ než `c4`, kde aspoň existoval osiřelý test. Obecný mechanismus `unknown fields` (`model.py`/`validate.py:70-71`, `V1` varování) by pravděpodobně pole `path`/`depth` ve front matteru odchytil, ale žádný test to s těmito konkrétními jmény polí neověřuje. | **Informace pro Human** — totéž zjištění jako u `c4`, opět mimo tento běh. |
| `c8` | ano | Ano, beze změny od kola 1/2. | Bez nálezu. |
| `c9` | ano | Ano, opraveno v kole 1. | Bez nálezu. |
| `c10` | ano | Ano, opraveno v kole 1. | Bez nálezu. |
| `c11` | ano | Ano, beze změny. | Bez nálezu. |
| `c12` | ano | Ano, beze změny. | Bez nálezu. |
| `c13` | ano | Ano, beze změny. | Bez nálezu. |
| `c14` | ano | Ano — druhá půlka je přímý důsledek první, ne nezávislé tvrzení. | Bez nálezu. |
| `c15` | ano | **Ano, opraveno v kole 3.** | Nález z kola 2 uzavřen. |
| `c16` | ano | **Ano, opraveno v kole 3** (nový kontrakt, dřívější osiřelý test teď má domov). | Nález z kola 2 uzavřen. |
| `c17` | ano | Ano, beze změny od kola 2. | Bez nálezu. |

Shrnutí: **v rozsahu tohoto běhu (`c8`–`c17`) nezůstává žádný blocker.** Mimo rozsah
(`c1`–`c7`) jsem našel dva výskyty téže vady (`c4`, `c7`) — zaznamenávám je jako dluh vůči
Human, ne jako důvod k REVISE tohoto běhu, přesně podle zadání kola 3.

## Axiomy A1–A6 po přidané próze — potvrzeno

- **A1 Refinement** — beze změny oproti kolu 2, nová próza je jen upřesnění uvnitř `i0004`,
  nemění vztah k `i0001`.
- **A2 Preservation** — `i0001` se v tomto běhu vůbec nemění (potvrzeno `git status` —
  soubor není v diffu).
- **A3 New information** — nová věta "Each contract states exactly one thing..." je
  konkrétní metodologické pravidlo pro psaní kontraktů v tomto uzlu; `i0001` nic
  podobného netvrdí, není to restatement rodiče.
- **A4 Contract strengthening** — `git diff` potvrzuje, že blok `c1`–`c7` je beze změny
  (diff se ho nedotýká); `c8`–`c17` jsou čistě přidané/zúžené, nic není oslabeno.
- **A5 Path sufficiency** — žádný nový cizí pojem zavlečen mimo `uses`.
- **A6 Frugality** — argument v `change.md` (nezměněné `code_paths`/`test_paths`, žádné
  rozhraní pro jiný produkt) obstojí; `code_paths: ["tools/"]` a
  `test_paths: ["tools/intent/tests/"]` u `i0004` jsou v diffu nedotčené, což ověřuje
  tvrzení doslovně.

## Co jsem ověřil sám

| Příkaz | Výsledek | Exit code |
|---|---|---|
| `python3 tools/intent/cli.py validate` | `5 node(s): 0 error(s), 0 warning(s)` | 0 |
| `git diff doc/intent/nodes/i0004-intent-tooling.md` | potvrzuje: `c1`–`c7` nezměněny; `c15`/`c16` nově rozdělené; `c17` (dřív `c16` v kole 2) beze změny; próza `c8`–`c17` opravena; nový odstavec o pravidlu "jeden kontrakt = jedno tvrzení" přidán; `code_paths`/`test_paths` nedotčené | 0 |
| `python3 -m unittest discover -s intent/tests -p "test_*.py" -v` (v `tools/`) | 80 testů v celé sadě `tools/intent/tests/`, všechny `ok` | 0 |
| Ruční přečtení `test_uses_target_contract_change_opens_the_consumer` a `test_uses_target_meaning_change_leaves_the_consumer_alone` proti `c15`/`c16` | oba testy teď mají přesně jeden kontrakt, žádný osiřelý test nezůstal | — |
| Ruční přečtení `tools/intent/tests/test_validate.py` (celý soubor) proti `c1`–`c7` | odhalilo `test_parent_and_child_may_overlap` jako osiřelý test vůči `c4` (stejný vzorec jako `c9`/`c10`/`c15` v tomto běhu) | — |
| `grep -rn '"path"\|"depth"'` v `tools/intent/` + přečtení `model.py` (`KNOWN_FIELDS`, `unknown_fields`) a `validate.py:70-71` | potvrdilo, že žádný test neověřuje zápornou polovinu `c7` jmenovitě; obecný `V1` "unknown fields" mechanismus by ji pravděpodobně zachytil, ale bez specifického testu na `path`/`depth` | — |
| Ruční přečtení celého `doc/runs/20260816-1302-realization-layer-91/change.md` | potvrzuje poctivý zápis obou kol zúžení včetně přiznání, že druhá verze vadu recyklovala, a nezměněný A6 argument z kola 2 | — |
