---
run_id: 20260816-1302-realization-layer-91
intent_ids: ["i0004"]
role: Adversary
model: claude-sonnet-5-thinking-high
complexity: high
status: done
---

# Nezávislá recenze — kolo 3 (finální)

## Verdikt
APPROVE, s jednou položkou k rozhodnutí Human a dvěma drobnostmi do `status.md`

Tohle je poslední kolo, které metodika Adversáři dovoluje, a poprvé nenacházím žádnou
věcnou vadu v kódu ani v pokrytí kontraktů testy. `c15` je rozdělený přesně tak, jak
kritika z kola 2 navrhla, a ověřil jsem oba testy tělo po těle: `c15` („A change of
contracts on a uses target opens its consumer") dokazuje jen a přesně
`test_uses_target_contract_change_opens_the_consumer`, `c16` („…never reaches its
consumer") jen a přesně `test_uses_target_meaning_change_leaves_the_consumer_alone`,
`c17` (přejmenovaný vynucovač) beze změny od kola 2. Žádný kontrakt v souboru už nemá
text širší než svůj vynucovač. Pravidlo je navíc zapsané do prózy uzlu (`## Contracts`),
takže se příště nebude znovu objevovat jako překvapení. Všech šest povinných příkazů z
`VERIFY.md` plus scope guard plus oba `ruff` self-checky jsem spustil sám, nezávisle na
`grader.md`, a vyšly identicky — 0 na všem. Nedávám tedy REQUEST CHANGES: nenašel jsem nic,
co by musel opravit Coder. Verdikt ale není bezpodmínečný APPROVE, protože jedna procesní
mezera z kola 2 (Kritik neviděl finální text) přetrvává a je na Human, aby řekl, zda ji
akceptuje tak, jak je zdokumentovaná níže, nebo si vyžádá ještě jeden — mimo tuto
Adversářskou smyčku — průchod Kritika.

## K rozhodnutí Human (mimo Adversářskou smyčku)

- **Finální text `c15`/`c16`/`c17` dosud neviděl žádný Kritik.** Ověřil jsem obsah
  `critique.md` znovu, k tomuto kolu: framatter pořád tvrdí `status: done`, nadpis je
  „Kritika změny záměru (kolo 2)", verdikt je `REVISE` a soubor se od mého kola 2 nezměnil
  ani bajt (`mtime` 13:25, zatímco `change.md`, `report.md`, `grader.md` mají 13:30–13:33 —
  vznikly *po* posledním zápisu do `critique.md`). Ta kritika popisuje přesně vadu, kterou
  jsem sám nezávisle našel v kole 2 (`c15` jako složené tvrzení se dvěma testy, z nichž
  `enforced_by` ukazuje jen na jeden) a doporučuje přesně to rozdělení na dva kontrakty,
  které teď v `i0004` skutečně je. Jinými slovy: **oprava odpovídá Kritikovu vlastnímu
  doporučení do písmene**, ale žádný Kritik verdikt nad *touto* verzí (`c15`+`c16`+`c17`,
  „kolo 3") na disku neexistuje — `rules/07-ice-workflow.mdc` přitom řadí „Critic on an
  intent change" mezi povinné brány pro `high`. Sám jsem provedl srovnání textu kontraktu s
  tělem jeho vynucovače se stejnou důsledností, jakou by použil Kritik (viz „Co jsem ověřil
  sám" níže), a nenašel jsem žádnou zbývající neshodu. Nepovažuji to za důvod žádat čtvrté
  kolo s Coderem — žádný kód se měnit nemá. Je to ale procesní díra, kterou nemůže zavřít
  Adversary sám za sebe: buď si Human vyžádá krátký, samostatný průchod Kritika nad
  aktuálním `i0004` (nemusí to být další plné kolo s Coderem a Adversářem), nebo vědomě
  převezme tuhle roli sám a zaznamená to v `status.md` jako rozhodnutí, ne jako přehlédnutí.
  Doporučuji druhou možnost, protože substanci jsem ověřil já, ale je to na Human, ne na mně.

- **`_acceptance_state` hlásí `acceptance: pending` i pro uzel, který ještě nikdo
  neclaimnul** (`tools/intent/realization.py:326-336`) — ověřil jsem to na vlastním stromu s
  `acceptance_profile: leaf`: `realization status` na nezaclaimnutém uzlu s `code_paths`
  vypíše `i0001 not_claimed, acceptance pending` a `realization summary` započítá tenhle
  uzel do `acceptance: … pending`, přestože `decide()` na nezaclaimnutý uzel odmítne
  pracovat (`TreeError`) — není tedy co „pending" akceptovat, dokud uzel nemá claim. Argument
  pro zachování (skutečně bude potřeba souhlas, jen ještě nemůže nastat) je vnitřně
  konzistentní a nepřidává žádnou nekonzistentní kombinaci stavu. Můj názor: je to platné
  rozhodnutí, ale zavádějící pro člověka, který čte jen `summary` — číslo „N pending" pak
  míchá „čeká se na mě" s „ještě to nikdo neclaimnul, čekat se nedá na nic". Kdybych trval na
  změně, navrhl bych ne nový čtvrtý stav (souhlasím, že by to zbytečně nafouklo slovník), ale
  aby `summary`/`worklist` počítaly do „pending" jen uzly, které mají claim — čistě otázka
  vykreslení, ne modelu dat. Je to ale styl, ne vada: neblokuje a klidně může jít do
  `status.md` jako zaznamenaný nesouhlas, přesně jak bod 5 zadání navrhuje.

## Závažné

- **`enforcer_problem` je teď zdokumentovaný jako vědomý kompromis — souhlasím, že
  dokumentace je správná odpověď, ne over-engineering.** `tools/intent/validate.py:145-150`
  má nový komentář: „a text search cannot tell a definition from a mention… this tool has no
  dependencies." Ověřil jsem, že nález samotný (doslovné slovo v komentáři/docstringu se
  pořád počítá jako „přítomné") skutečně přetrvává — mutační test s
  `"obj.test_x()\n# def test_x is inherited from elsewhere\n"` a `enforced_by: "…::test_x"`
  pořád vrátí „přítomný" — ale plně robustní oprava by vyžadovala parser na jazyk, což
  odporuje `## Meaning` uzlu `i0004` („no third-party dependencies, deliberately… must run
  before that project has an environment"). Trvat na víc než na komentáři by tady bylo
  neúměrné vlastnímu záměru uzlu. Snižuji na neblokující.

## Drobné / neblokující

- `report.md:143` teď správně říká „35 testů v 11 třídách" (opraveno z kola 2 „devíti
  skupinách") — ověřeno, `grep -c "^class "` dává 11. Ale objevil jsem novou drobnost na
  stejné stránce: `report.md:24` pořád píše „devět podpříkazů" a „devět nových kontraktů".
  Spočítal jsem oboje přímo z kódu: `tools/intent/main.py` definuje osm podpříkazů
  `realization` (`status`, `worklist`, `summary`, `claim`, `affirm`, `accept`, `check`,
  `prune`), ne devět, a `i0004` má deset nových kontraktů (`c8`–`c17`), ne devět — číslo
  „devět" bylo správné pro stav po kole 2 (`c8`–`c16`), ale kolo 3 přidalo `c17` a větu
  nikdo nepřepsal. Kosmetická nepřesnost, ne věcná; nemění žádný důkaz ani verdikt.
- `cli-evidence.md` teď pokrývá i `prune` (druhý throwaway strom: claim, smazání souboru
  uzlu, `check` pojmenuje osiřelý záznam jako `R1`, `prune` ho odstraní, `check` znovu
  čistý) — ověřil jsem přečtením, odpovídá to skutečnému chování `cmd_realization_prune`.
  Všiml jsem si jen kopírovací chyby: poslední odrážka v „What this shows" je v souboru
  duplicovaná (řádky 239-240 a 242-243 jsou identické) — kosmetika, nic sémantické.
- `README.md:216-217` teď zní `broken --> realized: enforcer restored` a
  `rejected --> realized: the Human accepted after a fix` — nález z kola 1 („claimed again"
  naznačovalo nutnost nového `claim`) je opravený; ověřil jsem proti `compute_states`, že
  automatické zotavení bez nového `claim` je přesně to, co diagram teď tvrdí.

## Co jsem ověřil sám

### Kolo 3 (nově tento průchod)

| Příkaz / akce | Výsledek | Exit code |
|---|---|---|
| `python3 tools/intent/cli.py validate` | `5 node(s): 0 error(s), 0 warning(s)` | 0 |
| `python3 tools/intent/cli.py realization check` | `realization layer consistent (0 entry/entries)` | 0 |
| `python3 -m unittest discover -s tools/intent/tests -t tools` | `Ran 80 tests … OK` | 0 |
| `python3 tools/checks/template_checks.py --root .` / `hook_checks.py --root .` | vyhovuje | 0 / 0 |
| `python3 tools/intent/cli.py scope --run doc/runs/20260816-1302-realization-layer-91 --node i0004` | `scope clean (30 declared path(s))` | 0 |
| `ruff check tools/` / `ruff format --check tools/` | čisté | 0 / 0 |
| Ruční čtení těl `test_uses_target_contract_change_opens_the_consumer`, `test_uses_target_meaning_change_leaves_the_consumer_alone`, `test_a_renamed_enforcer_symbol_makes_a_node_broken` vedle textů `c15`/`c16`/`c17` | každý test dokazuje přesně a jen text svého kontraktu, žádný přesah | — |
| Vlastní throwaway strom (`/tmp/rtest2`) s `acceptance_profile: leaf` a nezaclaimnutým uzlem s `code_paths` | `realization status` → `not_claimed, acceptance pending`; `summary` → `acceptance: 1 required, 0 approved, 1 pending` — potvrzuje nález o `_acceptance_state` | 0 |
| `grep -n "inner.add_parser" tools/intent/main.py` | 8 podpříkazů `realization`, ne 9 — `report.md:24` je nepřesný | — |
| `grep -c '  - id: c' doc/intent/nodes/i0004-intent-tooling.md` | 17 kontraktů celkem = 10 nových (`c8`–`c17`), ne 9 — `report.md:24` je nepřesný | — |
| `ls -la` + čtení `critique.md` | `mtime` 13:25, framatter `status: done`, verdikt `REVISE`, nadpis „kolo 2"; `change.md`/`report.md`/`grader.md` mají `mtime` 13:30–13:33, tedy vznikly až po posledním zápisu do `critique.md` — kritika nad finálním `c15`/`c16`/`c17` neexistuje | — |
| `test -f status.md` | neexistuje (očekáváno, píše se poslední) | — |
| Čtení `cli-evidence.md` sekce o `prune` | odpovídá skutečnému chování `cmd_realization_prune`; drobná duplicitní odrážka na konci souboru | — |
| Čtení `README.md:209-218` proti `compute_states`/`_acceptance_state` v `tools/intent/realization.py` | diagram teď odpovídá kódu | — |

### Kolo 2 (beze změny, pro úplnost)

| Příkaz / akce | Výsledek | Exit code |
|---|---|---|
| Ruční obnova staré podřetězcové shody v `enforcer_problem` (přesně diff z `grader.md` round 2) + testy | přesně 1 pád (`test_a_renamed_enforcer_symbol_makes_a_node_broken`), shoda s `grader.md` | 1 (očekáváno) |
| Vrácení patche, `diff` proti záloze | identické | — |
| Ruční obnova patche z kola 1 (nezaclaimnutý předek propaguje jako „state") nad **aktuálním** kódem + testy | 12 pádů (11 z kola 1 plus nově `test_a_renamed_enforcer_symbol_makes_a_node_broken`, který má stejnou strukturu jako `test_a_missing_enforcer_makes_a_realized_node_broken` — očekávaný nárůst, ne rozpor s `grader.md`, protože ten log je historický záznam kola 1 s 79 testy) | 1 (očekáváno) |
| Vrácení patche, `diff` proti záloze, opětovné `unittest discover` | identické, `Ran 80 tests … OK` | 0 |
| Python skript ověřující chování `(?<![\w.]){symbol}\b` na devíti scénářích (přesný rename, prefix, tečkovaný odkaz, metaznaky…) | výsledky odpovídají zjištěním výše | — |
