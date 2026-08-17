---
run_id: 20260816-2145-contract-hygiene-cd
intent_ids: ["i0004"]
role: Coder
model: claude-sonnet-5-thinking-high
complexity: high
status: done
---

# Report

## Co bylo implementováno

Podle přijatého `plan.md` a `change.md` (kolo 3, `ACCEPT`) jsem upravil kontrakty uzlu
`i0004` a rozšířil testy, které je dokazují — beze změny produkčního kódu
(`tools/intent/validate.py`, `model.py`, `generate.py` zůstávají v konečném stavu
nezměněné; byly dotčeny jen dočasně, během mutací).

Ve front matteru `i0004-intent-tooling.md` jsem přeformuloval `c4` (z „may overlap only
along the ancestor chain, never between siblings" na „of two different nodes may not
overlap unless one is an ancestor of the other") a `c7` (z „exist only in generated
views, never in a node file" na „are derived into the generated views"), a přidal tři
nové kontrakty `c18`, `c19`, `c20` přesně ve znění z `change.md`. V sekci `## Contracts`
jsem nahradil dva odstavce prózy: shrnující odstavec na začátku (obecné pravidlo „and
nowhere else" místo sourozeneckého, a „five contracts" místo „Two of them") a odstavec s
kritériem, který nyní obsahuje vsuvku u `c14` („cannot trip its own gate" follows from
„always allows"), aby derivace nebyla nutná k odhadu.

V `test_validate.py` jsem přejmenoval a rozšířil `test_siblings_may_not_overlap` na
`test_overlap_outside_the_ancestor_chain_is_rejected` (dokazuje `V6` u sourozenců **i** u
bratranců) a `test_parent_and_child_may_overlap` na `test_the_ancestor_chain_may_overlap`
(dokazuje absenci `V6` u rodič–dítě **i** u prarodič–vnuk pomocí tříúrovňového řetězce).
Přidal jsem nový test `test_derived_fields_in_a_node_file_are_reported` pro `c19`. V
`test_tools.py` jsem přidal `test_a_path_in_a_node_file_does_not_reach_the_index` pro
`c20`.

Pro každý ze čtyř testů (dva rozšířené, dva nové) jsem aplikoval mutaci z `plan.md`,
spustil sadu, zachytil výstup, mutaci vrátil a ověřil zelenou sadu — zaznamenáno v
`grader.md`. Všechny čtyři mutace se chovaly přesně podle predikce plánu: každá shodila
právě jeden cílený test a nic jiného.

Nakonec jsem spustil `intent map`, aby `MAP.md` a `INDEX.json` odpovídaly novým
kontraktům, a všechny gate příkazy z `VERIFY.md` mandátu.

## Vstupy a výstupy

### Přečteno

- `doc/runs/20260816-2145-contract-hygiene-cd/slice.md`
- `doc/runs/20260816-2145-contract-hygiene-cd/plan.md`
- `doc/runs/20260816-2145-contract-hygiene-cd/change.md`
- `doc/runs/20260816-2145-contract-hygiene-cd/critique.md`
- `doc/intent/nodes/i0004-intent-tooling.md`
- `doc/intent/nodes/i0001-harness.md`
- `tools/intent/validate.py`
- `tools/intent/model.py`
- `tools/intent/generate.py`
- `tools/intent/tests/test_validate.py`
- `tools/intent/tests/test_tools.py`
- `tools/intent/tests/helpers.py`

### Vytvořeno

- `doc/runs/20260816-2145-contract-hygiene-cd/grader.md`
- `doc/runs/20260816-2145-contract-hygiene-cd/report.md`

### Změněno

- `doc/intent/nodes/i0004-intent-tooling.md`
- `tools/intent/tests/test_validate.py`
- `tools/intent/tests/test_tools.py`
- `doc/intent/MAP.md`
- `doc/intent/INDEX.json`

### Nedotčeno

- `tools/intent/validate.py`
- `tools/intent/model.py`
- `tools/intent/generate.py`
- `doc/intent/_realization.yaml`

## Použité metody a rozhodnutí

Text kontraktů a prózy jsem převzal z `change.md` doslovně — beze změny jediného slova —
protože prošel třemi koly kritiky a run instrukce to výslovně žádají. Nekontroloval jsem
tedy, zda by se dalo znění vylepšit; kontroloval jsem jen, že citace do uzlu sedí přesně.

U `test_overlap_outside_the_ancestor_chain_is_rejected` jsem postavil čtyři uzly navíc
(`aunt`, `uncle` a jejich děti `cousin-a`, `cousin-b`) tak, aby měly společného prarodiče,
ale různé rodiče — to je definice bratranců, kterou `change.md` používá k odlišení od
sourozenců. Test kontroluje přes `validate(tree)` přímo (ne přes `self.codes()`, který by
jen řekl „V6 je někde v sadě"), že `V6` padne na dvojici sourozenců **a** na dvojici
bratranců zvlášť — jinak by test mohl procházet i s mutací, která hlásí `V6` jen u jedné z
dvou skupin.

U `test_the_ancestor_chain_may_overlap` jsem zvolil tříúrovňový řetězec (`db` → `models`
→ `user`) s překrývajícími se `code_paths` na všech třech úrovních. To v jednom stromu
dokazuje jak rodič–dítě (`db`–`models`, `models`–`user`), tak prarodič–vnuk (`db`–`user`)
bez nutnosti dvou samostatných stromů.

Pro `c19` jsem zvolil jedno tělo testu se dvěma uzly: `engine` s `path`/`depth` ve front
matteru a `clean` bez nich. Test tvrdí existenci nálezu `V1`, jehož `message` obsahuje
obě slova `path` a `depth`, u `engine`, a nepřítomnost takového nálezu u `clean` —
přesně podle testovací specifikace, včetně toho, že úroveň nálezu (`error`/`warning`)
se nikde neasertuje.

Pro `c20` jsem využil nápovědu z úkolu: `TreeBuilder.add` propíše libovolné klíčové
argumenty do front matteru přes `front.update(fields)`, takže `path="nonsense/place",
depth=99` je legální bez úpravy pomocníka. Test ověřuje, že `build_index` vrátí cestu
spočtenou z řetězce předků (`f"{root}/{child}"`), ne zapsanou hodnotu.

Mutace jsem aplikoval přesně podle `plan.md` tabulky (žádnou jsem neupravoval) a po
každé okamžitě ověřil, že diff proti HEAD je po revertu prázdný (`git diff --stat`), než
jsem přešel k další — aby se mutace nekumulovaly a měření zůstalo čisté jedna proti
jedné.

## Reference do kódu

| Soubor | Řádky | Shrnutí |
|---|---|---|
| `doc/intent/nodes/i0004-intent-tooling.md` | 20-22 | Přeformulované `c4` |
| `doc/intent/nodes/i0004-intent-tooling.md` | 29-31 | Přeformulované `c7` |
| `doc/intent/nodes/i0004-intent-tooling.md` | 62-70 | Nové `c18`, `c19`, `c20` |
| `doc/intent/nodes/i0004-intent-tooling.md` | 94-112 | Nahrazené odstavce prózy v `## Contracts` |
| `tools/intent/tests/test_validate.py` | 131-143 | `test_the_ancestor_chain_may_overlap` (`c18`) |
| `tools/intent/tests/test_validate.py` | 145-165 | `test_overlap_outside_the_ancestor_chain_is_rejected` (`c4`) |
| `tools/intent/tests/test_validate.py` | 168-180 | `test_derived_fields_in_a_node_file_are_reported` (`c19`) |
| `tools/intent/tests/test_tools.py` | 145-152 | `test_a_path_in_a_node_file_does_not_reach_the_index` (`c20`) |

## Důkazy

| Příkaz | Výsledek | Exit code |
|---|---|---|
| `python3 tools/intent/cli.py map` | `doc/intent/MAP.md`, `doc/intent/INDEX.json` aktualizovány | 0 |
| `python3 -m unittest discover -s tools/intent/tests -t tools` | `Ran 82 tests … OK` | 0 |
| Mutace 1 (`c4`, společný rodič namísto předka) | padá právě `test_overlap_outside_the_ancestor_chain_is_rejected` | 1 |
| Mutace 2 (`c18`, `_is_ancestor` jen přímý rodič) | padá právě `test_the_ancestor_chain_may_overlap` | 1 |
| Mutace 3 (`c19`, `path`/`depth` do `KNOWN_FIELDS`) | padá právě `test_derived_fields_in_a_node_file_are_reported` | 1 |
| Mutace 4 (`c20`, zapsaná cesta přednost v `build_index`) | padá právě `test_a_path_in_a_node_file_does_not_reach_the_index` | 1 |
| Sada po každém revertu | `Ran 82 tests … OK` | 0 |
| `python3 tools/intent/cli.py validate` | `5 node(s): 0 error(s), 0 warning(s)` | 0 |
| `python3 tools/intent/cli.py realization check` | `realization layer consistent (1 entry/entries)` | 0 |
| `python3 tools/intent/cli.py realization status --node i0004` | `stale [own contracts changed; own meaning changed]` — očekávané | 0 |
| `python3 tools/checks/template_checks.py --root .` | `template contracts satisfied` | 0 |
| `python3 tools/checks/hook_checks.py --root .` | `hook contracts satisfied` | 0 |
| `python3 tools/intent/cli.py scope --run doc/runs/20260816-2145-contract-hygiene-cd` | `scope clean (6 declared path(s))` — bez `--node` | 0 |
| `ruff check tools/` (Coder self-check) | `All checks passed!` | 0 |
| `ruff format --check tools/` (Coder self-check) | `19 files already formatted` | 0 |

Podrobný, strojově čitelný log se všemi diffy a syrovými výstupy je v `grader.md`.

## Definition of Done

Všechny body z `plan.md` jsou splněné: `c4`+`c18` dohromady pokrývají celé pravidlo, které
`_check_code_paths` vynucuje (sourozenci i bratranci na chybové straně, rodič–dítě i
prarodič–vnuk na kladné straně), `c7`+`c19`+`c20` dohromady pokrývají původní výrok `c7`
o path/depth. Každý z pěti kontraktů má `enforced_by` na existující symbol, jehož tělo
prokazuje celou jeho větu — ověřeno jednotlivě při psaní testů i souhrnně přes
`intent validate`. Shrnující odstavec i odstavec s kritériem v `## Contracts` jsou
nahrazené zněním z `change.md` (včetně vsuvky u `c14`). Všechny čtyři mutace jsou
zaznamenané v `grader.md`, každá s pádem přesně jednoho cíleného testu a s návratem do
zelené. `intent validate` končí 0, generované soubory jsou aktuální, celá sada
`tools/intent/tests` je zelená (82 testů), `template_checks` a `hook_checks` končí 0,
`ruff check`/`ruff format --check` nad `tools/` jsou čisté a kontrola rozsahu bez
`--node` končí 0. Stav `stale` uzlu `i0004` ve vrstvě realizace je očekávaný důsledek
změny kontraktů a nebyl opravován — nový důkaz a claim je práce Coordinatora po zeleném
Graderu.
