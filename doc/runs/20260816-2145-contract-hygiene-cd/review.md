---
run_id: 20260816-2145-contract-hygiene-cd
intent_ids: ["i0004"]
role: Adversary
model: claude-opus-5-thinking-high
complexity: high
status: done
---

# Nezávislá recenze

## Verdikt

**REQUEST CHANGES**

Řemeslo je nadprůměrné: diff sedí na plán do posledního souboru, próza je doslovná,
všechny čtyři mutace jsem přeměřil sám a reprodukují se přesně, produkční kód nástroje
zůstal nedotčený a Coder nenapsal claim. Podmínky P1, P2 i P3 jsou splněné.

Blokuji na jediné věci, a je to právě ta, kvůli které běh existuje. Uzel má **dva**
generované pohledy — `render_map` a `build_index` (`tools/intent/generate.py`) — a každý
si cestu počítá zvlášť. `c7` mluví o „the generated view**s**" a `c20` o „in **a**
generated view", ale oba jejich vynucovače sahají jen na `build_index`. Vada, kterou běh
uklízel u `c4` („never between siblings" proti testu na sourozence) a u `c7` („never in a
node file" proti testu na kladnou půlku), se tím neodstranila — jen se přestěhovala z
„souboru uzlu" do „toho druhého generovaného pohledu". Doložil jsem to spuštěním, ne
čtením.

## Blokující

### B1 — `c20` tvrdí o obou generovaných pohledech, dokazuje jeden

`doc/intent/nodes/i0004-intent-tooling.md:69` — „A path written into a node file **never**
becomes the node's path in **a generated view**". Vynucovač
`tools/intent/tests/test_tools.py:145-152` sahá jen na `build_index`; jméno testu to samo
přiznává — `..._does_not_reach_the_index`.

`render_map` počítá cestu vlastním voláním `tree.path_of` (`tools/intent/generate.py:34`),
nezávisle na `build_index` (`tools/intent/generate.py:72`). Nad kopií v `/tmp/adv_cd` jsem
aplikoval dvoubodovou obdobu mutace 4, ale mířenou na `render_map` místo `build_index`
(pole `Node.written_path` plněné z front matteru + přednost v `render_map`). Výsledek:

```
| `i0001` | `i0001`          | system | — | — |
| `i0002` | `nonsense/place` | engine | — | — |
```

Zapsaná cesta se stala cestou uzlu v `MAP.md`, tedy `c20` je porušené — a přitom
`Ran 82 tests … OK` (exit 0) a `python3 tools/intent/cli.py validate` →
`5 node(s): 0 error(s), 0 warning(s)` (exit 0). Kontrakt zakazuje něco, co jeho vynucovač
nechá projít.

Tím padá i položka Definition of Done „Každý z pěti kontraktů má `enforced_by` na
existující symbol, **jehož tělo prokazuje celou jeho větu**" (`plan.md:102-103`), kterou
`report.md:157-158` označuje za splněnou.

Co se musí změnit — jedna ze dvou cest, obě legitimní:

- zúžit text na to, co test dokazuje: „…never becomes the node's path in **the generated
  index**" (pak text a jméno testu sedí na sebe), **nebo**
- rozšířit tělo testu i na `render_map` — asertovat, že vykreslená `MAP.md` obsahuje
  odvozenou cestu a neobsahuje `nonsense/place`. Mutace na to existuje, naměřil jsem ji
  výše.

### B2 — `c7` má tutéž vadu v množném čísle

`doc/intent/nodes/i0004-intent-tooling.md:30` — „Path and depth are derived into the
generated **views**". Vynucovač `tools/intent/tests/test_tools.py:133-143` se dotýká zase
jen `build_index`.

Naměřeno: nahradil jsem v `render_map` hodnotu sloupce `Path` konstantou (`path = "—"`),
takže `MAP.md` žádnou odvozenou cestu nenese. Sada zůstala zelená —
`Ran 82 tests … OK`, exit 0. `test_map_contains_every_node_and_a_diagram`
(`test_tools.py:154-163`) to nechytá, protože id uzlu je v řádku tabulky i ve sloupci `Id`.

Druhá polovina téhož: `MAP.md` žádný sloupec `depth` nemá. Věta čtená distributivně —
„path a depth se odvozují do generovaných pohledů" — je tedy o jednom z těch dvou pohledů
rovnou nepravdivá, ne jen nedokázaná.

Připouštím vstřícné čtení („derived rather than stored, a bydlí to v generovaných
pohledech"), pod kterým je `c7` v pořádku. Právě proto to zapisuji: běh, jehož předmětem
je, že se kontrakt nemá dát číst šířeji než jeho test, si dvojznačnost tohoto druhu
nemůže nechat. Oprava je stejná a v jednom tahu s B1 — buď „the generated index"
(souhlasně se jménem `test_index_holds_derived_path_and_depth`), nebo test na `MAP.md`.

`change.md:65` říká u tohoto bodu „dnešní test stačí". To je jediné místo delty, kde se
dosah testu odhadl a nezměřil, a je to přesně to místo, kde vada zůstala.

## Závažné

### Z1 — `report.md` opírá klíčovou položku DoD o příkaz, který ji ověřit nemůže

`report.md:157-159`: „Každý z pěti kontraktů má `enforced_by` na existující symbol, jehož
tělo prokazuje celou jeho větu — ověřeno jednotlivě při psaní testů i **souhrnně přes
`intent validate`**."

`intent validate` tohle neumí a netvrdí to. `enforcer_problem`
(`tools/intent/validate.py:129-156`) ověřuje existenci souboru a výskyt symbolu textovým
hledáním; komentář na řádcích 149-153 sám upozorňuje, že přijme i symbol zmíněný v
komentáři. O tom, co tělo testu dokazuje, neříká nic. Souhrnný důkaz tedy neexistuje;
zbývá čtení Codera, které nikdo negradoval — a je to právě to místo, kudy B1 a B2 prošly.

Formulaci je třeba opravit na to, co se skutečně stalo („ověřeno čtením při psaní testů;
`intent validate` ověřuje jen existenci symbolu"). Není to kosmetika: příští čtenář DoD
jinak uvěří, že tu položku hlídá stroj.

## Drobné / neblokující

- **D1** — `test_derived_fields_in_a_node_file_are_reported` (`test_validate.py:169-180`)
  nikde neasertuje, že nález je *o neznámém poli*; požaduje jen `V1`, jehož `message`
  obsahuje slova `path` a `depth`. `c19` říká „is reported as an **unknown field**". Kdyby
  se zpráva `_check_identity` přeformulovala mimo pojem unknown fields, test projde.
  Test **není** vatový — ověřil jsem, že shodí i jednostrannou mutaci (jen `path` do
  `KNOWN_FIELDS` → sada padá) — jde čistě o znění asercí.
- **D2** — `assertNotIn(clean, flagged)` v témže testu nese málo: `clean` nemá žádné
  neznámé pole, takže nález toho tvaru u něj nemůže vzniknout jinak než rozbitím celého
  mechanismu. Plán ho vyžadoval, není to odchylka; jen to není hrana, kterou by se dalo
  argumentovat.
- **D3** — `assertTrue({sibling_a, sibling_b} & flagged)` (`test_validate.py:164-165`) je
  věcně správná volba, protože `_check_code_paths` hlásí jen na `node_a` z dvojice, ale
  chybová hláška je pak `AssertionError: set() is not true` — vidět v `grader.md:45`.
  `assertTrue(..., msg=...)` nebo porovnání množin by příštímu čtenáři logu ušetřilo
  vyšetřování.
- **D4** — Stará jména `test_siblings_may_not_overlap` a `test_parent_and_child_may_overlap`
  žijí už jen v artefaktech běhů (audit), v žádném `enforced_by` ani ve stromu ne. Nic
  neosiřelo. `slice.md` nese předchozí znění `c4`/`c7` a `realization: realized` — správně,
  je to snímek pořízený před změnou.

## Co jsem ověřil sám

Sondy běžely nad kopií v `/tmp/adv_cd`; v repozitáři jsem nezměnil nic než tento
`review.md`.

| Příkaz / úkon | Výsledek | Exit code |
|---|---|---|
| `python3 tools/intent/cli.py scope --run doc/runs/20260816-2145-contract-hygiene-cd` (bez `--node`) | `scope clean (6 declared path(s))`; všech 5 změněných souborů je v `outputs` nebo `incidental` | 0 |
| `python3 tools/intent/cli.py validate` | `5 node(s): 0 error(s), 0 warning(s)` | 0 |
| `python3 -m unittest discover -s tools/intent/tests -t tools` | `Ran 82 tests … OK` | 0 |
| `git diff tools/intent/validate.py tools/intent/model.py tools/intent/generate.py` | prázdný — chování nástroje se nezměnilo, jak běh sliboval | 0 |
| **Mutace 1** (`_check_code_paths` jen společný rodič) přeaplikována | padá **právě** `test_overlap_outside_the_ancestor_chain_is_rejected`, `AssertionError: set() is not true` — identické s `grader.md` | 1 |
| **Mutace 2** (`_is_ancestor` jen přímý rodič) přeaplikována | padá **právě** `test_the_ancestor_chain_may_overlap`, `'V6' unexpectedly found in ['V6']` — identické | 1 |
| **Mutace 3** (`path`+`depth` do `KNOWN_FIELDS`) přeaplikována | padá **právě** `test_derived_fields_in_a_node_file_are_reported` — identické | 1 |
| **Mutace 4** (`Node.written_path` + přednost v `build_index`) přeaplikována | padá **právě** `test_a_path_in_a_node_file_does_not_reach_the_index`, `'nonsense/place' != 'i0001/i0002'` — identické | 1 |
| Sada po každém revertu | `Ran 82 tests … OK` | 0 |
| **Vlastní sonda k B1**: `written_path` s předností v `render_map` (ne v `build_index`) | `MAP.md` vypíše `nonsense/place` jako cestu uzlu, sada **zelená**, `validate` **0 chyb** | 0 |
| **Vlastní sonda k B2**: sloupec `Path` v `render_map` nahrazen konstantou | sada **zelená** — odvozenou cestu v `MAP.md` nehlídá žádný test | 0 |
| **Vlastní sonda k D1**: jen `path` do `KNOWN_FIELDS` | sada padá — obě půlky `c19` test řeže jednotlivě | 1 |
| **P1** — čtení `## Contracts` uzlu | `Two of them` ani `but not between siblings` v uzlu nezůstalo; nové znění je „take five contracts between them" a „and nowhere else" | — |
| **P2** — čtení odstavce s kritériem | u `c14` v uzlu stojí `"cannot trip its own gate" follows from "always allows"` i referent „the run's own write" | — |
| **P3** — čtení Definition of Done v `plan.md` | odrážky pro **oba** odstavce (`plan.md:104-107`) | — |
| **Doslovnost prózy** — strojové porovnání obou citovaných bloků z `change.md` s tělem uzlu | oba bloky jsou v uzlu znak po znaku; žádné tiché vylepšení | — |
| `python3 tools/intent/cli.py realization status` | `i0004 stale [own contracts changed; own meaning changed]`, ostatní `not_claimed` | 0 |
| `python3 tools/intent/cli.py realization check` | `realization layer consistent (1 entry/entries)` | 0 |
| `git status --short` nad `doc/intent/_realization.yaml` | soubor **není** změněn; jediný zápis je claim předchozího běhu podepsaný Coordinatorem — Coder claim nenapsal | — |
| Dohledání starých symbolů v celém repozitáři | `test_siblings_may_not_overlap` a `test_parent_and_child_may_overlap` už jen v artefaktech běhů, v žádném `enforced_by` | — |
| `ruff check tools/` a `ruff format --check tools/` | `All checks passed!`, `19 files already formatted` | 0 |

Kontrakty `c4`, `c18` a `c19` jsem četl proti celému tělu jejich testů a nemám k nim
nález. `c4` má obě půlky (sourozenci i bratranci) v jednom těle a každou shazuje vlastní
mutace; `c18` prokazuje vzdálenost 1 i 2 jedním tříúrovňovým řetězcem; `c19` úroveň nálezu
netvrdí, jak `change.md:78-81` slibuje, a test ji skutečně nikde neasertuje.
