---
run_id: 20260817-1703-views-hygiene-dc
intent_ids: ["i0004"]
role: Adversary
model: claude-opus-5-thinking-high
complexity: high
status: done
rounds: 2
---

# Nezávislá recenze

## Verdikt

**APPROVE** (kolo 2).

Kolo 1 skončilo **REQUEST CHANGES** kvůli jednomu blokujícímu nálezu. Ten je opravený a
opravu jsem si ověřil vlastní mutací, ne z `grader.md`: mutace, kterou jsem blokující nález
v kole 1 doložil, dnes test shodí, a shodí ho **na dokumentové aserci**, zatímco řádková
polovina zůstává zelená. Řádková aserce přitom pořád řeže — stará mutace na tabulku padá
dál. Nic jiného se v pracovním stromě nepohnulo.

Záznam kola 1 níž zůstává nezměněný, včetně znění blokujícího nálezu; je označený jako
uzavřený, ne smazaný.

## Blokující

- **[KOLO 1 — UZAVŘENO v kole 2]** **`c20` stále tvrdí víc, než jeho vynucovač prokazuje:
  `render_map` píše tři věci, test kontroluje jednu** —
  `tools/intent/tests/test_tools.py:156-164` (aserce na řádku 163-164) — doplnit dokumentovou
  aserci, tj. vedle stávající kontroly na řádku ještě `self.assertNotIn("nonsense/place", text)`.

  `render_map` vypisuje řádek tabulky, mermaid diagram a souhrn kontraktů. Test najde řádek
  uzlu a `nonsense/place` vylučuje **jen z něj** (`assertNotIn(..., row)`). Doložil jsem
  mutací, ne úvahou: nechal jsem zapsanou cestu prosáknout do labelu mermaid diagramu
  (`tools/intent/generate.py:45`, plus pole `path` na `Node` jako v mutaci 2). Výsledek:

  ```
      i0002["i0002<br/>engine<br/>nonsense/place"]
  ```

  `nonsense/place` je v `MAP.md`, `c20` je porušené — a `Ran 82 tests ... OK`, exit 0.

  Není to můj přísnější výklad kontraktu; **plán tu aserci jmenovitě žádal**. Testovací
  specifikace v `plan.md` má na mapové polovině spojku: „týž uzel má v `render_map` cestu z
  řetězce předků **a** `nonsense/place` se v `MAP.md` nevyskytuje". Následující odstavec
  zakazuje hledat hodnotu *jen* jako podřetězec celého dokumentu a přikazuje se opřít o
  řádek — tedy „řádek **navíc**", ne „řádek **místo** dokumentu". Coder druhý konjunkt
  zúžil na řádek a v `report.md` to uvádí jako vlastní rozhodnutí („U mapy se nehledá
  `nonsense/place` v celém dokumentu"). Zužovat testovací specifikaci přijatého plánu není
  role Codera; a položka Definition of Done „`c20` má vynucovač, jehož tělo prokazuje obě
  poloviny na obou pohledech" je tím pravdivá jen o tabulce.

  Blokuji proto, že je to **týž vzorec potřetí, jen posunutý o jednu úroveň**: nejdřív
  „soubor uzlu → generovaný pohled", pak „index → druhý pohled", teď „řádek tabulky →
  zbytek téhož pohledu". Oprava je jeden řádek a stávající řádkovou aserci neruší.

  **Uzavření (kolo 2).** `tools/intent/tests/test_tools.py:169` nese
  `self.assertNotIn("nonsense/place", text)` a řádková aserce (`:167-168`) zůstala vedle ní.
  Přeověřeno mutacemi v tabulce „Co jsem ověřil sám (kolo 2)". `report.md` už zúžení
  neprezentuje jako rozhodnutí, ale jako porušení testovací specifikace plánu, které našla
  nezávislá recenze — to je správný záznam, protože příště se podle reportu pozná, že tady
  brána zabrala, ne že Coder volil.

## Závažné

Žádný z těchto nálezů nevznikl v tomto běhu a žádný neblokuje. Disposici, kterou navrhuje
Coordinator (zapsat je Humanovi, zúžení `c6` jako rozhodnutí Humana), **potvrzuji** — se
třemi upřesněními, která jsou v odrážkách níž. Podmínku mám jednu: patří do `status.md`
i s reprodukcí, ne jako holá řádka v tabulce navazující práce. Předchozí běh ukázal, že
nález přežije jen tak, jak je zapsaný.

- **`c6` je nepravdivé a vyvrací ho vlastní testovací sada** — `c6` říká „A slice carries
  ancestors and semantic dependencies but **never siblings**", ale `build_slice`
  (`tools/intent/slicing.py:70` a `:80-84`) dává do `result.files` i uzly z `talks_to`,
  včetně **příchozích** hran. Sourozenec s hranou `talks_to` na cílový uzel se do slice
  dostane. Ověřeno spuštěním, ne čtením:

  ```
  files: ['…/i0001-system.md', '…/i0003-target.md', '…/i0002-sibling.md']
  SIBLING FILE IN SLICE: True
  ```

  `test_slice_includes_incoming_talks_to` (`tools/intent/tests/test_tools.py:34-42`) přesně
  tuhle situaci staví — `caller` i `callee` jsou obě děti `root` — takže sada sama dokazuje
  opak toho, co `c6` tvrdí. Vynucovač `c6` (`:20-32`) testuje jen sourozence **bez** hrany
  `talks_to`, tedy jedinou větev, ve které věta platí.

  Není to nález proti tomuto běhu: `c6` je v HEAD, běh se ho nedotkl a jeho cíl je omezený
  na kontrakty o generovaných pohledech. Zároveň to Coder ani Coordinator opravit nesmí —
  zúžení `c6` je oslabení kontraktu, tedy věc Humana, stejně jako bylo u `c7`. Patří to do
  `status.md` jako otevřený nález a do navazujícího běhu.

  **Upřesnění ke kolu 2.** Označení „rozhodnutí Humana" je správné a je jediná možnost, i
  když se to na první pohled nezdá: druhá cesta — nechat text a **dotáhnout kód**, aby slice
  sourozence opravdu nenesla — by rozbila to, co metodika chce (`07-intent-tree.mdc`:
  „`talks_to` enters as **context**"). Oprava tedy nutně míří do textu `c6`, a text se bude
  zužovat. Human má na výběr mezi „přeformulovat `c6` tak, aby `talks_to` jmenoval" a
  „rozdělit ho na dva kontrakty"; obojí je oslabení dnešní univerzální věty.

- **`build_index` počítá odvozený `depth` na dvou místech; test sahá na jedno** —
  `tools/intent/generate.py:73` (`nodes[*].depth`) a `:92` (`reverse_code_map[*].depth`).
  Mutace, která nechá zapsaný `depth` vyhrát **jen** v reverzní mapě, projde: `Ran 82 tests
  ... OK`. Kdybych mutoval `nodes[*].depth`, test padne (`AssertionError: 99 != 1`), takže
  tuhle polovinu nový test drží — a drží ji nad rámec `c20`, které mluví jen o cestě.

  Zúžené `c7` („The generated index carries a path and a depth derived from the parent
  chain") tím nepadá: kvantifikátor v něm není, a `nodes[*]` odvozený path i depth nese.
  Je to ale doslova ta konfigurace, ze které vyrostly předchozí dva nálezy — jedna odvozená
  hodnota, dvě nezávislá místa výpočtu, test na jednom — a tentokrát **vevnitř funkce,
  kterou běh přezkoumával**. Buď rozšířit tělo o aserci na `reverse_code_map`, nebo to
  vědomě zapsat jako nekryté; nechat to nevyslovené je třetí opakování téže slepé skvrny.

  **Upřesnění ke kolu 2.** Tenhle bod pro Humana **není** — rozšíření vynucovače je
  posílení, tedy práce běžného běhu. Do `status.md` patří jako navazující práce, ne jako
  rozhodnutí, na které se čeká.

- **Odvozenou cestu vypisují i dva pohledy, o kterých nemluví žádný kontrakt** —
  `render_slice` (`tools/intent/slicing.py:100` a `:105`, řádky `- path:` a `- depth:`) a
  příkaz `owner` (`tools/intent/main.py:213`). Generované pohledy to nejsou, takže `c20` o
  nich neříká nic a běh tím nic neporušuje. Praktický dopad je ale větší než u `INDEX.json`:
  slice je dokument, který čte Coder jako pravdu. Pro navazující běh, ne pro tento.

- **`c19` není pravdivé o node files v `_retired/`** — `_check_identity`
  (`tools/intent/validate.py:53`) iteruje jen `tree.nodes`, takže hlášení o neznámých polích
  (`:70-71`) retired uzly nikdy nepotká, přestože `parse_node` je do `unknown_fields`
  poslušně dá. Ověřeno: retired node file s `path: nonsense/place` a `depth: 99` má
  `unknown_fields: ['depth', 'path']`, a `validate` na něj vrátí jediný nález, `V7` o
  registru. Věta „A path or depth written into **a node file** is reported as an unknown
  field" je tedy univerzální tvrzení s nepokrytým výřezem. Přebraný kontrakt, mimo cíl
  tohoto běhu; hlásím, aby se to neztratilo.

  **Upřesnění ke kolu 2.** Ani tenhle bod není nutně pro Humana. Levnější a poctivější
  směr je **posílit vynucovač** — nechat `_check_identity` projít i `tree.retired` — a text
  `c19` nechat, jak je. To je změna nástroje v běžném běhu. Rozhodnutí Humana by z toho
  bylo teprve tehdy, kdyby navazující běh chtěl místo toho zúžit větu.

## Drobné / neblokující

- **Komentář `# Index half first — order matters for mutation evidence (index then map).`
  (`tools/intent/tests/test_tools.py:151`) — v tomhle znění má jít pryč.** Ne celý:
  omezení, které popisuje, je skutečné a stojí za zápis (index se asertuje před mapou, aby
  jednostranná regrese pojmenovala pohled, který se rozbil). Pryč má jít **slovník běhu**.
  „Mutation evidence" je pojem z `grader.md`; čtenář za rok otevře test, žádný běh k němu
  mít nebude a bude hádat, o jaké důkazy šlo. Komentář má říkat omezení, ne jak si ho
  jednou někdo naměřil — třeba „`index` before `map`: a one-sided regression must name the
  view that broke". Druhý komentář (`:156`, „Map half: row carries the derived path; the
  written path is absent from MAP.md") je v pořádku: „half" je čitelné z `c20` a věta říká,
  co dvě aserce dohromady drží. Neblokuje a APPROVE na tom nezávisí.
- `next(...)` bez výchozí hodnoty (`tools/intent/tests/test_tools.py:158-162`): kdyby řádek
  uzlu nešlo najít, unittest to ohlásí jako `StopIteration` ERROR, ne FAIL. **Tiše projít to
  nemůže**, což je to podstatné, a chybu je vidět; `next(..., "")` by dal čitelnější hlášku
  ve tvaru neúspěšné aserce. Logika hledání řádku sama je v pořádku: bere buňku Id
  (`line.split("|")[1]`), takže na oddělovač hlavičky ani na jiný řádek nesedne a v tomto
  stromu neexistuje druhý řádek se `` `i0002` `` v prvním sloupci.
  **Vyřízeno v kole 2** — `next(..., None)` + `assertIsNotNone(row, f"no table row for node
  {child}")`. Ověřeno mutací: když řádek přestane být dohledatelný, hláška je
  `AssertionError: unexpectedly None : no table row for node i0002`, tedy FAIL se jménem
  uzlu, ne `StopIteration`.
- Komentáře v těle testu jsou jinak přesně to, co má komentář dělat: říkají důvod, ne co
  řádek dělá.
- `assertTrue({sibling_a, sibling_b} & flagged)` (`tools/intent/tests/test_validate.py:164-165`,
  přebraný kód) při pádu vypíše jen „False is not true"; aserce s hláškou by se ladila lépe.

## Co jsem ověřil sám (kolo 1)

| # | Úkon | Výsledek |
|---|---|---|
| 1 | `python3 tools/intent/cli.py scope --run doc/runs/20260817-1703-views-hygiene-dc` | `scope clean (6 declared path(s))`, exit 0; `git status --short` hlásí jen 5 deklarovaných souborů + adresář běhu |
| 2 | Podmínka Kritika u `test_validate.py` | Splněna. mtime `2026-08-17 06:45`, tedy před začátkem běhu (17:03), zbytek výstupů 17:12; řádky, na které ukazuje `grader.md` předchozího běhu (143, 179), v souboru přesně sedí — obsah je bajt za bajtem to, co zastavený běh nechal |
| 3 | `c7` doslovně z `change.md` a pravdivé | Ano. `build_index` (`generate.py:65,72-73`) ukládá `path` z `tree.path_of` i `depth` jako `len(path)-1`; `test_index_holds_derived_path_and_depth` obojí asertuje na vnukovi (`path`, `depth == 2`) |
| 4 | Reprodukce mutace 1 (`path` na `Node` + přednost v `build_index`) | Padá indexová polovina, `test_tools.py:153`, `'nonsense/place' != 'i0001/i0002'`; 82 testů, 1 pád |
| 4 | Reprodukce mutace 2 (totéž + přednost v `render_map`) | Padá **mapová** polovina, `test_tools.py:163`, `'`i0001/i0002`' not found in '\| `i0002` \| `nonsense/place` \| engine \| — \| — \|'`; indexová polovina prošla — řez je opravdu na mapě |
| 4 | Mutace navíc: zapsaný `depth` v `nodes[*]` | Padá `test_tools.py:154`, `99 != 1` |
| 4 | Mutace navíc: zapsaný `depth` jen v `reverse_code_map` | `Ran 82 tests … OK` — nepokryto (viz Závažné) |
| 4 | Mutace navíc: zapsaná cesta do labelu mermaid diagramu | `nonsense/place` v `MAP.md`, `Ran 82 tests … OK` — **blokující nález** |
| 5 | Hledání řádku uzlu | Nemůže tiše projít (`next()` bez default vyhodí), nemůže sednout na jiný řádek (buňka Id, backticky); čitelnost hlášky viz Drobné |
| 6 | `git diff tools/intent/generate.py tools/intent/model.py tools/intent/validate.py` | Prázdný — chování nástroje se nezměnilo, jak plán slíbil |
| 7 | Vzorec „vada se přestěhovala" pro `c6`, `c7`, `c18`, `c19`, `c20` | `c20`: `render_map` (řádek pokryt, diagram a souhrn kontraktů ne → bloker), `build_index` `nodes[*]` pokryto; `c7`: dva výpočty `depth`, jeden pokrytý; `c18`: `_check_code_paths` + `_is_ancestor` přes `tree.ancestors`, tříúrovňový řetězec pokrývá i prarodiče, `assertNotIn("V6", …)` platí pro celý strom — v pořádku; `c19`: `parse_node` + `_check_identity`, retired soubory nepokryté; `c6`: `build_slice` — věta nepravdivá (viz Závažné) |
| 8 | Poctivost vrstvy realizace | `doc/intent/_realization.yaml` v `git status` **není**, `realization status --node i0004` → `stale [own contracts changed; own meaning changed]`, `realization check` → `consistent (1 entry/entries)`. Coder si svou práci nenárokoval |
| 9 | Generované pohledy proti uzlu | `validate` → `5 node(s): 0 error(s), 0 warning(s)` (tedy i V9), `INDEX.json` nese nové znění `c7` i vynucovač `c20` s novým jménem, řádek `i0004` v `MAP.md` obsahuje `c18`–`c20`; staré jméno `test_a_path_in_a_node_file_does_not_reach_the_index` už se v repozitáři mimo `doc/runs/` nikde nevyskytuje |
| — | Celá sada v repozitáři | `python3 -m unittest discover -s tools/intent/tests -t tools` → `Ran 82 tests … OK`, exit 0 |

## Co jsem ověřil sám (kolo 2)

| # | Úkon | Výsledek |
|---|---|---|
| 1 | Znovu moje mutace z kola 1 (`path` na `Node` + únik do mermaid labelu) | **Padá**, `test_tools.py:169`, `AssertionError: 'nonsense/place' unexpectedly found in …` — tedy na **dokumentové** aserci. V doprovodné hlášce je vidět, že řádek tabulky nesl `` `i0001/i0002` ``, takže řádkové aserce (`:167-168`) prošly. Přesně ten řez, který jsem si vyžádal |
| 2 | Mutace 2 z kola 1 (přednost zapsané cesty v řádku `render_map`) | **Pořád padá**, `test_tools.py:167`, `'`i0001/i0002`' not found in '\| `i0002` \| `nonsense/place` \| engine \| — \| — \|'` — řádková aserce nezakrněla, dokumentová ji nepřebila |
| 3 | Mutace navíc: buňka Id ztratí backticky, takže řádek nejde dohledat | `test_tools.py:166`, `AssertionError: unexpectedly None : no table row for node i0002` — FAIL se jménem uzlu, žádné `StopIteration`. Bod z Drobných je opravdu vyřízený |
| 4 | Nehybnost okolí | `git diff` je prázdný pro `tools/intent/generate.py`, `model.py`, `validate.py`. `tools/intent/tests/test_validate.py` má pořád mtime `2026-08-17 06:45` (tedy nedotčený ani v kole 2) a jeho diff je beze změny těch 40/6 řádků převzatých ze zastaveného běhu. `git status --short` hlásí tytéž 5 souborů + adresář běhu |
| 5 | Vrstva realizace | `doc/intent/_realization.yaml` není v `git status`, mtime `2026-08-16 13:42`; `realization status --node i0004` → `stale [own contracts changed; own meaning changed]`; `realization check` → `consistent (1 entry/entries)`. Coder si ani v kole 2 nic nenárokoval |
| 6 | `grader.md` append-only | Ano. Řádky 1–204 jsou znak za znak to, co jsem čítal v kole 1 (mutace 1 a 2, zelená po revertu, brány, ruff); kolo 2 začíná až za oddělovačem na řádku 206. Mutace 3 je zaznamenaná s oběma diffy a se stejným pádem, jaký jsem naměřil sám |
| 7 | Brány v repozitáři | `validate` → `0 error(s), 0 warning(s)`; sada → `Ran 82 tests … OK` (počet testů se nezměnil, přidala se aserce, ne test); `scope --run …` → `scope clean (6 declared path(s))`; `ruff check tools/` → `All checks passed!`; `ruff format --check tools/` → `19 files already formatted`. Vše exit 0 |
| 8 | `report.md` proti skutečnosti | Sedí. Zúžení je zapsané jako porušení testovací specifikace plánu chycené nezávislou recenzí, ne jako rozhodnutí; tabulka důkazů uvádí tři mutace; `Nedotčeno` odpovídá prázdným diffům |

Mutace jsem dělal na kopiích v `/tmp` (`/tmp/adv-dc` v kole 1, `/tmp/adv-dc2` v kole 2), ne
v repozitáři, a obě jsem po sobě smazal. V repozitáři jsem za obě kola nezměnil nic kromě
tohoto `review.md`.
