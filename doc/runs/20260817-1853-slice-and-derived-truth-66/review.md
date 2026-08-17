---
run_id: 20260817-1853-slice-and-derived-truth-66
intent_ids: ["i0004"]
role: Adversary
model: claude-opus-5-thinking-high
complexity: high
status: done
rounds: 3
---

# Nezávislá recenze

Model Codera byl `cursor-grok-4.5-high`, můj je `claude-opus-5-thinking-high` — podmínka
`adversary_differs_from_coder` splněna.

> **Aktuální verdikt je verdikt round 3 na konci tohoto dokumentu: APPROVE.**
> Záznamy round 1 a round 2 jsou ponechané nezměněné jako audit. Blokátory B1, B2, B3
> (round 1) a B4 (round 2) jsou všechny opravené a ověřené mutací, ne přečtením.
> Round 3 nese jednu položku k opravě **před commitem** (nejde o blokátor), dva
> follow-upy pro pozdější běh a eskalaci o pořadí `realization claim`.

## Verdikt — round 1

**REQUEST CHANGES** — tři blokátory. Všechny tři jsou **tentýž druh vady, kvůli kterému
tento běh vznikl**: věta kontraktu sahá dál než její vynucovač. Běh ji uzavřel v místech,
která pojmenoval požadavek, a nechal ji otevřenou o úroveň vedle — u `c6` ve dvou místech,
u `c19` v jednom.

Produkční změna (`validate.py`) je správná, minimální a past z plánu je dodržená. `c7` je
po tomto běhu doopravdy uzavřené. Rozsah neuteče, brány jsou zelené, žádné tvrzení
z `report.md` jsem nevyvrátil.

## Blokátory

### B1 — `c6` slovo „exactly“ je prokázané jen do vzdálenosti jedné hrany

`tools/intent/tests/test_tools.py:21-28` — fixtura je hvězda: kořen je **přímý rodič**
cílového uzlu, `shared` nemá vlastní `uses`, `listener` ani `caller` nemají další
`talks_to`. Žádný ze tří vztahů, o kterých věta mluví, není ve fixtuře delší než jeden
skok. Rovnost množin na řádku 33 proto **neumí odlišit** jednoskokové pravidlo, které kód
implementuje, od jakékoli tranzitivní varianty — a věta „exactly these intent nodes: the
node, **its ancestors**, its `uses` targets and the far end of every `talks_to` edge“ je
o tranzitivitě.

Tři reprodukce, každá nechá sadu celou zelenou (`Ran 82 tests … OK`), a každá dělá větu
`c6` nepravdivou:

```diff
# (a) tools/intent/slicing.py:69 — slice nese jen rodiče, ne řetězec předků
-    ancestors = [item.id for item in tree.ancestors(node_id)]
+    ancestors = [item.id for item in tree.ancestors(node_id)][-1:]
```

```diff
# (b) tools/intent/slicing.py:76 — 'uses' se rozšíří na tranzitivní uzávěr
-        uses=sorted(node.uses),
+        uses=sorted(set(node.uses) | {u for t in node.uses if t in tree.nodes for u in tree.nodes[t].uses}),
```

```diff
# (c) tools/intent/slicing.py:71 — 'talks_to' se rozšíří na dva skoky
-    talks = sorted(set(node.talks_to) | set(incoming))
+    talks = set(node.talks_to) | set(incoming)
+    talks = sorted(talks | {t for m in list(talks) if m in tree.nodes for t in tree.nodes[m].talks_to})
```

Reprodukce (a) je z těch tří nejtěžší, protože `result.ancestors` napájí i sekci
„Contracts in force“ (`tools/intent/slicing.py:130`). Pod ní tedy každý slice hlubší než
jedna úroveň tiše přestane nést kontrakty prarodičů — a sada to nezaznamená.

**Tenhle standard už v tomto repozitáři platí a byl vysloven o `c18`.** Adversář běhu
`20260817-1703-views-hygiene-dc` u `c18` výslovně ověřoval, že „tříúrovňový řetězec
pokrývá i prarodiče“ (`review.md:179`). `c6` dostalo v tomto běhu podstatně silnější větu
a slabší fixturu.

**Co musí změnit:** fixtura potřebuje v každém ze tří vztahů řetěz délky dvě —
řetězec předků `root → mid → target` s `mid` v očekávané množině, `uses` cíl, který sám
něco `uses` (a ten druhý uzel **mimo** očekávanou množinu), a far end `talks_to`, který
sám s někým dalším mluví (také mimo). Teprve pak rovnost množin odliší jeden skok od
uzávěru. Text `c6` se měnit nemusí — je pravdivý, jen nedokázaný.

### B2 — `c6` není prokázané ve větvi `for_implementation=True`

`tools/intent/tests/test_tools.py:31` volá `build_slice(..., for_implementation=False)`.
`build_slice` má druhou větev (`tools/intent/slicing.py:87-89`), do které vynucovač `c6`
nikdy nevstoupí. Věta přitom neříká „a plan slice“, říká „**a slice**“, a nově vložený
odstavec v uzlu (`doc/intent/nodes/i0004-intent-tooling.md:112-113`) k tomu přidává
výslovný závazek: *„Descendants are outside the set as well — carrying them would be a
change of intent, not a refactor.“*

Reprodukce — věrohodná změna („Coder ať při implementaci vidí i svůj podstrom“), po které
je věta i ten odstavec nepravdivý a sada zelená (`Ran 82 tests … OK`):

```diff
# tools/intent/slicing.py:80
     node_ids = [*ancestors, node_id, *result.uses, *result.talks_to]
+    if for_implementation:
+        node_ids += [child.id for child in tree.children_of(node_id)]
```

To **není** ten follow-up o `render_slice`, který Human odložil do `doc/new_ideas/`.
Jde o `build_slice` a o `result.files` — přesně o to, na co `c6` ukazuje. Odložený nápad
se týká odvozené cesty, kterou `render_slice` **tiskne**; tady jde o obsah množiny uzlů.

**Co musí změnit:** vynucovač musí nad **touž** fixturou spustit i
`for_implementation=True` a udělat tutéž rovnost množin nad `result.files`. Pravidlo, na
které se plán sám odvolává („jedna a táž věta = jeden test, který prokáže obě půlky“),
tohle vyžaduje: dnes je prokázaná jedna ze dvou větví.

### B3 — `c19` říká „path **or** depth“, test zná jen případ, kdy jsou tam obě

`tools/intent/tests/test_validate.py:171` a `:174` zapisují **oba** klíče
(`path=…, depth=99`), a predikát na `:177-178` vyžaduje, aby ve zprávě byla obě slova.
Případ, kdy je v souboru uzlu jen `path` (nebo jen `depth`), tedy v testu neexistuje
a nelze ho tím predikátem ani vyjádřit. Reprodukce, po které je věta `c19` nepravdivá
o polovině svého vlastního „or“ a sada je zelená (`Ran 82 tests … OK`):

```diff
# tools/intent/validate.py:54
-    if node.unknown_fields:
+    if len(node.unknown_fields) > 1:
```

**Poznámka k závažnosti:** tato mezera je **starší než tento běh** — F3 mířila na dosah
na `_retired/`, ne na disjunkci. Uvádím ji jako blokátor proto, že cíl v `plan.md:24-30`
slibuje, že po běhu je *„každý kontrakt `i0004` pravdivý a dosažený svým vynucovačem“*,
a `c19` je jeden ze tří kontraktů, které běh otevřel. Oprava je dvouřádková: jeden uzel
jen s `path`, druhý jen s `depth`, a predikát rozdělit na dvě podmínky. Kdyby to Human
chtěl odložit, B1 a B2 tím nejsou dotčené — ty jsou vady, které tento běh vyrobil.

## Major

### M1 — „verbatim“ výstupy v `grader-evidence.md` neodpovídají odeslanému souboru

`grader-evidence.md:38`, `:75` a `:114` citují `test_tools.py", line 35` resp. `line 157`.
V odeslaném souboru jsou ty aserce na řádcích **33** a **155**. Důvod je v `report.md:82-83`:
`ruff format` po zaznamenání důkazů složil řádek `target = self.builder.add(…)` na jeden,
čímž se soubor zkrátil o dva řádky. Důkaz tedy nebyl pořízen nad kódem, který se odesílá.

Věcně to drží — mutace 1, 2, 3 i 4 jsem sám znovu spustil nad **finálním** kódem a každá
shodila právě jmenovaný test se stejnou zprávou (tabulka níž). `test_validate.py` sedí
na řádek přesně. Není to blokátor, protože položka Definition of Done („čtyři mutace,
každá s pádem právě jednoho jmenovaného testu“) je splněná; je to ale záznam označený
jako „verbatim“, který se doslova reprodukovat nedá. Přeměřit po formátování, nebo to
slovo z nadpisu vypustit.

### M2 — `grader.md` má rozbité kódování v titulku

`grader.md:1`: `# Grader â€” doc/runs/…`. UTF-8 pomlčka zapsaná jako latin-1. Kosmetika,
ale `grader.md` je audit, který čte Human.

## Minor / neblokující

1. `report.md:113` a `:116` uvádějí `realization status --node i0004` → `stale`
   a prázdný `git status --short doc/intent/_realization.yaml`. Dnes je stav `realized`
   a soubor je změněný. Není to nepravda Codera — je to důsledek toho, že Coordinator
   nárokoval po něm (viz níž).
2. Katalog `AGENT_MODELS.md` přiděluje v pásmu `high` Kritikovi i Coderovi tentýž slug
   (`cursor-grok-4.5-high`). `constraints` to nezakazuje, takže to není porušení pravidla.
   Stojí to ale za zaznamenání jako **eskalace na Humana**, ne jako blokátor: `critique.md:19-20`
   uvádí, že Kritik navržené testy sám postavil na scratch kopii a proměřil — tedy tentýž
   model, který fixturu schválil, ji pak napsal. B1 a B2 jsou přesně to, co nezávislý
   Kritik mohl zachytit. Formulace omezující tabulky je mimo rozsah tohoto běhu.
3. Kde jsem vědomě netlačil: u `c7` a `c19` jsem **nepovažoval** implicitní univerzální
   kvantifikaci („pro každý uzel, pro každý tvar stromu“) za případ, který musí vynucovač
   vyjmenovat. Trvám jen na případech, které **text kontraktu sám pojmenuje** — proto je
   „path or depth“ blokátor a „nese to index i pro kořen?“ není.

## Co jsem prověřoval nejtvrději a nenašel nic

**`c7`.** Prošel jsem každé odvození cesty a hloubky v `tools/` (`grep` na `path_of`,
`depth_of`, `len(path)`, `"depth"`). V `build_index` jsou přesně tři nesené odvozené
hodnoty — `nodes[*].path` (`generate.py:72`), `nodes[*].depth` (`:73`) a
`reverse_code_map[*].depth` (`:92`) — a test sahá na všechny tři
(`test_tools.py:148`, `:149`, `:155`). Čtvrté odvození v indexu není: `reverse.sort`
(`:94`) hloubku jen čte, `nodes[*].file` je `node.source`, `code_path` je deklarovaný.
`render_map:34` odvozuje cestu, ale do **MAP.md**, o kterém `c7` nemluví — a je pokrytá
testem `c20`. `slicing.py:100,105` a `main.py:213` jsou `render_slice` a příkaz `owner`,
tedy položky, které Human odložil. A na rozdíl od `c6` je `c7` prokázané **tranzitivně**:
fixtura má řetěz `root/child/grandchild` a asertuje hloubku 2, ne 1. Tady je vzorec
„vada o úroveň vedle“ opravdu uzavřený.

**Past u `c19`.** Ověřil jsem spuštěním, ne čtením, že do `tree.retired` jde jen jedno
hlášení: strom z fixtury dá **2 varování `V1` a 0 chyb**, current uzel není ohlášený
dvakrát (`set(tree.nodes) & set(tree.retired)` je prázdná), čistý retired soubor nedá
**žádný** nález, a žádné jiné pravidlo `V1` na retired uzly nespadne. Třetí druh souboru
uzlu neexistuje: `load_tree` čte jen `nodes/*.md` a `_retired/*.md`, `proposed`
i `superseded` uzly leží v `nodes/`, a `_proposed/` v tomto nástroji ani v pravidlech není
(`grep` přes `rules/`, `skills/`, `tools/`). `c19` je po tomto běhu uzavřené ve všem kromě
disjunkce z B3.

**Odvození id z cesty v testu `c6`.** `path.split("/")[-1].split("-")[0]` slepit dva různé
uzly do jednoho klíče nemůže: klíčem je `iNNNN` z názvu `{id}-{slug}.md`, a ta část je
unikátní z definice registru. Test tedy neprochází „za špatný důvod“ kvůli klíči. Prochází
za špatný důvod kvůli tvaru fixtury (B1), což je jiná vada.

## Ověřené mutace (znovu, nad finálním kódem)

Vše na kopii `/tmp/adv-probe` (`tools/` + `ruff.toml`); pracovní strom repozitáře jsem
nezměnil. Po každé mutaci reverze a `diff -r` proti repozitáři.

| # | Mutace z `grader-evidence.md` | Padlo právě | Zpráva | Shoda |
|---|---|---|---|---|
| 1 | `*result.talks_to` → `*node.talks_to` | `test_slice_carries_exactly_…` | `Items in the second set but not the first: 'i0005'` | ano |
| 2 | přidat sourozence do `node_ids` | totéž | `Items in the first set but not the second: 'i0007' 'i0006'` | ano |
| 3 | `reverse … "depth": "0"` | `test_index_holds_derived_path_and_depth` | `'0' != '2'` | ano |
| 4 | `tree.retired` → `tree.nodes` | `test_derived_fields_in_a_node_file_are_reported` | `'i0004' not found in {'i0002'}` | ano |

Reprodukoval jsem tedy **všechny čtyři**, ne jen dvě. Každá shodila právě jeden test,
jmenovitě ten svůj; u mutace 1 zůstal `test_slice_includes_incoming_talks_to` zelený,
u mutace 3 `test_reverse_lookup_prefers_the_deepest_node` zelený. Odchylka je jen
v číslech řádků (M1).

## Mutace, které jsem přidal sám — všechny nechaly sadu zelenou

| # | Zásah | Která věta se stala nepravdivou | Sada |
|---|---|---|---|
| A | `slicing.py:69` → `[-1:]` | `c6` „its ancestors“ | 82 OK |
| B | `slicing.py:76` → tranzitivní `uses` | `c6` „its `uses` targets“ | 82 OK |
| C | `slicing.py:71` → dva skoky `talks_to` | `c6` „the far end of every `talks_to` edge“ | 82 OK |
| D | `slicing.py:80` → potomci při `for_implementation` | `c6` „kinship alone adds none“ + odstavec v uzlu | 82 OK |
| E | `validate.py:54` → `len(...) > 1` | `c19` „A path **or** depth“ | 82 OK |
| F | `slicing.py:89` → `result.files.extend(result.code)` | nic (kód není intent-uzel) | 82 OK |

Mutace F je jediná, kterou **nepovažuji** za nález: kvalifikátor „these intent nodes“ ji
pokrývá tak, jak `change.md:76-79` tvrdí. Referent je opravdu seznam uzlů, ne dokument.
Tenhle bod jsem se snažil zlomit a nezlomil jsem ho.

## Co jsem sám ověřil (příkaz → exit code)

| Příkaz | Výstup | Exit |
|---|---|---|
| `python3 tools/intent/cli.py validate` | `5 node(s): 0 error(s), 0 warning(s)` | 0 |
| `python3 tools/intent/cli.py realization check` | `realization layer consistent (2 entry/entries)` | 0 |
| `python3 tools/intent/cli.py realization status --node i0004` | `i0004  realized` | 0 |
| `python3 tools/intent/cli.py coverage` | `contracts: 28`, `machine-enforced: 28 (100%)`, `files outside any node: 0` | 0 |
| `python3 tools/intent/cli.py scope --run doc/runs/20260817-1853-slice-and-derived-truth-66` | `scope clean (8 declared path(s))` | 0 |
| `python3 -m unittest discover -s tools/intent/tests -t tools` | `Ran 82 tests … OK` | 0 |
| `python3 tools/checks/template_checks.py --root .` | `template contracts satisfied` | 0 |
| `python3 tools/checks/hook_checks.py --root .` | `hook contracts satisfied` | 0 |
| `ruff check tools/` | `All checks passed!` | 0 |
| `ruff format --check tools/` | `19 files already formatted` | 0 |
| `grep -rn "never siblings" . --exclude-dir=.git --exclude-dir=runs` | prázdný | 1 |
| `grep -rn "test_slice_contains_ancestors_and_uses_but_not_siblings" . --exclude-dir=.git --exclude-dir=runs` | prázdný | 1 |

Osm kontrol z osmi bran je zelených. `map` jsem nespouštěl, protože zapisuje; `validate`
bez `V9` je rovnocenný důkaz, že `MAP.md` i `INDEX.json` jsou aktuální.

Rozsah: `git status --short` obsahuje právě osm změněných souborů a všech osm je
v `outputs` nebo `incidental` z `plan.md`. `git diff --stat` je prázdný pro `slicing.py`,
`generate.py`, `model.py`, `coverage.py` a `scope.py`, jak plán slibuje. Do `## Contracts`
je vložený jen nový odstavec, ostatní tři jsou znak za znak stejné. Produkční změna ve
`validate.py` je opravdu jen `_report_unknown_fields`, cyklus přes `tree.retired`
a import `Node`. Scope creep jsem nenašel, oslabený test taky ne — nový test `c6` je
**silnější** než ten, který nahradil, jen ne tak silný, jak jeho věta tvrdí.

Ověřeno také, že fixtura si nález nevyrábí sama: `TreeBuilder.add(retired=True)` je
explicitní keyword, `path`/`depth` jdou do `**fields`, tedy do front matteru, a odtud do
`unknown_fields` — což je právě ta chyba, kterou `c19` popisuje. Kdyby `retired` šlo přes
`**fields`, bylo by samo tím neznámým polem; plán to předvídal a Coder to dodržel.

Ani jedna aserce v diffu není sebepotvrzující: očekávaná množina v `c6` je vypsaná
z rolí fixtury, `"2"` v `c7` je konstanta, `assertIn(gone, flagged)` je jméno uzlu.
Nikde se neasertuje hodnota spočítaná stejně jako v produkčním kódu.

## Nález o metodice, ne o tomto diffu — nárok před recenzí

Coordinator zapsal nárok na realizaci `i0004` **před** mým spuštěním, protože
`skills/ice-run/SKILL.md:94-98` (krok 7) to tak nařizuje a `rules/07-realization.mdc` to
potvrzuje („`claim` | Coordinator, after the Grader is green“). Adversář je až krok 8.
Je to vada v harnessu a stojí za opravu. Důvody, v tomto pořadí:

1. **Vrstva dnes tvrdí `realized`, zatímco recenze je otevřená.**
   `realization status --node i0004` vrací `realized` bez jakékoli zmínky o tom, že
   nezávislý přezkum běží. `worklist` uzel neuvede. Human, který se ptá „co zbývá“,
   dostane odpověď „na `i0004` nic“ — přesně v okamžiku, kdy na něm zbývají tři věci.
2. **Otisk pokrývá jen text uzlu, takže nepravdivý nárok se sám neopraví.**
   Fingerprints jsou `contracts` a `meaning` (`rules/07-realization.mdc`). Moje tři
   blokátory se opravují **v testech**, ne v uzlu. Oprava tedy nepohne ani jedním
   otiskem — nárok zůstane `realized` a nikdy nezčervená, přestože byl v momentě zápisu
   nepravdivý. To není teoretická možnost: přesně to se stalo v tomto běhu.
3. **Neexistuje `unclaim`.** Podpříkazy jsou `status`, `worklist`, `summary`, `claim`,
   `affirm`, `accept`, `check`, `prune` (`tools/intent/main.py:310-350`). Nárok jde
   odklidit jen `accept --reject` (jen Human), nebo změnou textu, která ho udělá `stale`.
   Adversář s verdiktem REQUEST CHANGES tedy nemá **žádný** mechanický způsob, jak
   nepravdivý `realized` stáhnout — a nemá ho mít, protože nárok psát nesmí.
4. **Jediná mechanická podmínka `claim`u je „vynucovače jsou dosažitelné“.** Že vynucovač
   svou větu opravdu dokazuje, se nekontroluje. To je legitimní — je to soud, ne
   aritmetika — ale právě proto ten soud musí být zapsaný **před** nárokem, ne po něm.

Nejmenší oprava, kterou bych navrhoval: přesunout `realization claim` z kroku 7 do
kroku 9 („Close“), za `review.md`, a v kroku 7 nechat jen brány a `grader.md`. Zachovává
to všechno ostatní — Coder dál nesmí nárokovat, Coordinator dál nárokuje po zelené bráně,
jen zelená brána nově znamená „brána i recenze“. U `low` běhů, kde Adversář neběží, se nic
nemění.

Změna metodiky je věc Humana (`rules/07-ice-workflow.mdc`, sekce „Always the Human“),
takže tohle je **eskalace, ne blokátor** — proti diffu tohoto běhu nemám v této věci nic.
Pro tento konkrétní běh z toho ale plyne úkol: až B1–B3 doběhnou, nárok na `i0004` je
potřeba přepsat proti novému stavu, protože ten dnešní byl zapsán proti kódu, o kterém
teď píšu, že jeho vynucovače nesahají tam, kam jejich věty tvrdí.

## Rozsah, který jsem nerozšiřoval

Nepožaduji `--base` pro scope guard, ani kontrakt nad odvozenou cestou v `render_slice`
a v příkazu `owner`, ani formulaci omezující tabulky v `AGENT_MODELS.md`. Pro správnost
tohoto běhu nosné nejsou. Jediné, co z odložených věcí do B1–B3 zasahuje, je vztah
`render_slice` ↔ `result.ancestors` (B1), a i tam žádám jen o silnější fixturu už
existujícího testu `c6`, ne o nový kontrakt.

---

# Round 2

## Verdikt — round 2

**REQUEST CHANGES** — jeden blokátor, **B4**. Není to nový nález: je to **nedokončená
polovina B1**. Hrana `talks_to` má v `build_slice` dvě odvozovací místa a fixtura po
round 2 fixuje hranici jen u jednoho z nich.

Všechno ostatní je hotové a ověřil jsem to sám, ne z tabulky Codera. B1 (a), (b), (c),
B2 i B3 jsou opravené a všech pět mých reprodukcí, které v round 1 nechávaly sadu zelenou,
teď padá na jmenovaném testu. `M1` (nereprodukovatelné „verbatim" výstupy) je opravená
poctivě — Coder evidenci nepřipsal, ale **přeměřil celou**, včetně mutací 1–4, a čísla
řádků 43, 165, 193 a 199 v `grader-evidence.md` v odeslaných souborech skutečně sedí
(ověřeno `sed -n`). Produkční kód se nezměnil vůbec: `git diff --stat` je pro
`slicing.py`, `generate.py`, `model.py`, `coverage.py` a `scope.py` prázdný.

Kdyby Human chtěl B4 přeskočit, řeknu to na rovinu: je to jediná zbývající hranice věty
`c6` a její oprava je **jeden uzel ve fixtuře a jedna položka v `outside`**. Není důvod ji
odkládat, a po ní už u `c6` žádné nefixované místo není — enumeraci uvádím níž, aby round 3
měl viditelný konec.

## Blokátor

### B4 — příchozí polovina `talks_to` nemá ve fixtuře hranici

`build_slice` skládá `talks_to` ze **dvou** odvození (`tools/intent/slicing.py:70-71`):

```python
    incoming = sorted(other.id for other in tree.nodes.values() if node_id in other.talks_to)
    talks = sorted(set(node.talks_to) | set(incoming))
```

Fixtura po B1 fixuje hranici jen u **vlastní** hrany: `listener` mluví s
`further_listener` a ten je v `outside`, takže mutace „dva skoky po vlastních hranách"
padá (moje reprodukce C, mutace 7). U **příchozí** hrany hranice chybí — ve fixtuře není
uzel, který by mluvil s `caller`. Rozšíření příchozí strany na dva skoky proto projde
celou sadou:

```diff
# tools/intent/slicing.py:70
-    incoming = sorted(other.id for other in tree.nodes.values() if node_id in other.talks_to)
+    first = {other.id for other in tree.nodes.values() if node_id in other.talks_to}
+    second = {o.id for o in tree.nodes.values() if any(f in o.talks_to for f in first)}
+    incoming = sorted(first | second)
```

```
Ran 82 tests in 0.185s
OK
exit_code=0
```

**Není to no-op, který nic nemění.** Aby nešlo namítnout, že mutace na dnešním kódu nic
nedělá, doložil jsem, že mění chování — na stromu, který se od fixtury liší jediným uzlem
`far_caller` s `talks_to: [caller]`:

```
### UNMUTATED
  far_caller id      : i0009
  carried            : ['i0001', 'i0002', 'i0004', 'i0006', 'i0007', 'i0008']
  far_caller carried : False
### MUTATED (two-hop incoming)
  far_caller id      : i0009
  carried            : ['i0001', 'i0002', 'i0004', 'i0006', 'i0007', 'i0008', 'i0009']
  far_caller carried : True
```

`far_caller` **není** far end žádné hrany `talks_to` incidentní s `target` — hrana vede
`far_caller → caller`. Věta „A slice carries exactly these intent nodes: … the far end of
every `talks_to` edge" je tedy pod mutací nepravdivá a sada je zelená. To je přesně
kritérium, které jsem použil v round 1.

Čtení věty tady nezpochybňuji: přivlastnění se z „**its** `uses` targets" přenáší i na
další člen výčtu, a odstavec v uzlu to potvrzuje („`talks_to` counts in both
directions"). Takže „edges incident on the node, both directions" — a fixována je jedna
z těch dvou directions.

**Co musí změnit:** jeden uzel ve fixtuře `test_slice_carries_exactly_ancestors_uses_and_talks_to_ends`
a jeden záznam v `outside`, ve tvaru symetrickém k `further_listener`:

```python
far_caller = self.builder.add("far-caller", parent=root, talks_to=[caller])
...
outside = {deeper_shared, further_listener, far_caller, sibling, consumer, child}
```

Text `c6` se nemění, produkční kód se nemění. Mutace výše je pak devátá reprodukce, která
padá — patří do `grader-evidence.md` jako mutace 10.

## Kde končí požadavek — aby round 3 měl viditelný konec

Round 1 i round 2 skončily „vada o úroveň vedle", takže napíšu závazně **pravidlo, které
používám**, ne jen další nález. Vynucovač `c6` musí fixovat hranici u každého odvození,
které kód **skutečně implementuje** — což je totéž kritérium, jakým tenhle běh uzavřel
`c7` (dvě odvození `depth` → dvě aserce). Odvození jsou v `build_slice` právě tato:

| # | Odvození | Hranici drží | Stav |
|---|---|---|---|
| 1 | `tree.ancestors(node_id)` | `root` na hloubce 2 (mutace 5) | uzavřeno |
| 2 | sám `node_id` | členství v `expected` | uzavřeno |
| 3 | `node.uses` | `deeper_shared` (mutace 6) | uzavřeno |
| 4 | `node.talks_to` — vlastní hrana | `further_listener` (mutace 7) | uzavřeno |
| 5 | `incoming` — příchozí hrana | **nic** | **B4** |
| 6 | větev `for_implementation` | `child` v obou větvích (mutace 8) | uzavřeno |

Po B4 je tabulka celá zelená a od `c6` už nic dalšího nechci. Zejména **nebudu** žádat:

- **řetězec předků délky tři.** Hloubka 2 odlišuje „jde k rodiči" od „prochází řetězec",
  což je celá hranice toho odvození; hloubka 3 nepřidává nový režim selhání. Je to táž
  míra, jakou Adversář běhu 1703 přijal u `c18` a jakou má dnes `c7`
  (`root/child/grandchild`). Kdybych chtěl 3, chtěl bych zítra 4 — to je regres bez konce.
- **bratrance ani pravnuky.** Kód neobsahuje **žádné** odvození z příbuznosti. Věta říká
  „kinship alone adds none" a fixtura má reprezentanta tří tříd příbuznosti: sourozence
  pod `mid`, strýce (děti `root` bez hrany) a potomka. Kdo do slice přidá pravidlo nad
  příbuzností, přidává nový kód, a hranici má dokázat ten, kdo ho přidává.
- **cokoli z `doc/new_ideas/`** — `scope --base`, kontrakt nad `render_slice` a `owner`,
  tabulka v `AGENT_MODELS.md`. Ani v round 2 nejsou pro správnost tohoto běhu nosné.

## Mých pět reprodukcí z round 1, znovu spuštěných proti opraveným testům

Vše na scratch kopii `/tmp/adv2` (`tools/` + `ruff.toml`); po každé mutaci reverze
s kontrolou, že soubor je **bajt za bajtem** shodný s repozitářem, a znovu zelená sada.
Pracovní strom repozitáře jsem nezměnil.

| Repro (round 1) | Zásah | Padá | Zpráva | `failures=` |
|---|---|---|---|---|
| A = B1 (a) | `slicing.py:69` → `[-1:]` | `test_slice_carries_exactly_…`, obě větve | `Items in the second set but not the first: 'i0001'` | 2 |
| B = B1 (b) | `slicing.py:76` → tranzitivní `uses` | totéž, obě větve | `Items in the first set but not the second: 'i0003'` | 2 |
| C = B1 (c) | `slicing.py:71` → dva skoky `talks_to` | totéž, obě větve | `Items in the first set but not the second: 'i0005'` | 2 |
| D = B2 | `slicing.py:80` → potomci při implement | totéž, **jen** `for_implementation=True` | `Items in the first set but not the second: 'i0011'` | 1 |
| E = B3 | `validate.py:54` → `len(...) > 1` | `test_derived_fields_in_a_node_file_are_reported` | `'i0003' not found in {'i0006', 'i0002'}` | 1 |

`Ran 82 tests` u všech pěti, `exit_code=1`, po reverzi `OK` / `exit_code=0`. Žádný jiný
test u nich nepadl, takže signál nic nezakrývá. Doslovné výstupy A–C mám v protokolu
včetně tracebacků; sedí na `test_tools.py:43` a `test_validate.py:193`, tedy na řádky,
které `grader-evidence.md` cituje.

## `subTest` — nedá se spolknout a větve se navzájem nekryjí

Tři nezávislé důkazy, ne úvaha:

1. **Pád jen v druhé větvi je nahlášený.** Reprodukce D shodí výhradně
   `(for_implementation=True)`, `FAILED (failures=1)`, `exit_code=1`. Kdyby `subTest`
   pád v druhé větvi spolkl, běh by skončil `OK`.
2. **Pád v první větvi nezastaví druhou.** Mutace, která přidá `child` vždy a `sibling`
   navíc jen při `for_implementation`, vypíše **různé** zprávy pro obě větve:

```
FAIL: … (for_implementation=False)   AssertionError: Items in the first set but not the second: 'i0011'
FAIL: … (for_implementation=True)    AssertionError: Items in the first set but not the second: 'i0011' 'i0009'
FAILED (failures=2)
```

   Druhá větev tedy proběhla a nahlásila se **samostatně**, přestože první už padla.
3. **Sdílený stav mezi větvemi neexistuje.** `tree` se staví jednou před cyklem, ale
   `build_slice` ho nemění — porovnal jsem snapshot `(parent, uses, talks_to, source)`
   všech jedenácti uzlů před oběma voláními a po nich: `tree mutated by build_slice: False`.
   `result` je v každé iteraci nový `Slice`. Fixtura jedné větve tedy do druhé neteče.

Počet testů zůstává 82 — `subTest` testy nepřidává, jen dělí hlášení, takže položka
Definition of Done „počet testů 82" je splněná a není obejitá.

## Negativní členové jsou vyloučení ze správného důvodu

Neověřoval jsem to čtením tabulky, ale mutací pro každou třídu zvlášť:

| Třída | Mutace | Kdo unikl | Padá |
|---|---|---|---|
| sourozenec | `siblings = [n for n in nodes if n.parent == node.parent]` | **jen** `i0009` (`sibling` pod `mid`) | ano, obě větve |
| příchozí `uses` (opačný směr) | `node_ids += [n.id for n in nodes if node_id in n.uses]` | `i0010` (`consumer`) | ano, obě větve |
| potomek | potomci při `for_implementation` | `i0011` (`child`) | ano, větev `True` |
| `uses` druhého řádu | tranzitivní `uses` | `i0003` (`deeper_shared`) | ano, obě větve |
| vlastní `talks_to` druhého řádu | dva skoky | `i0005` (`further_listener`) | ano, obě větve |
| **příchozí `talks_to` druhého řádu** | dva skoky příchozí | nikdo — chybí uzel | **ne → B4** |

Tvrzení Codera, že mutace sourozenců po B1 sáhne jen na `sibling` pod `mid` a `consumer`
drží rovnost množin, je **pravdivé** — potvrdil jsem obojí samostatnou mutací, ne
odvozením. Přeřazení `target` pod `mid` tím zároveň udělalo z dětí `root` bez hrany
(`deeper_shared`, `further_listener`, `consumer`) třídu „strýc", takže mutace nad
příbuzností rodiče má ve fixtuře na co narazit.

## Klíč z cesty a řazení nic nemaskují

Slugy nově obsahují pomlčky (`deeper-shared`, `further-listener`), takže jsem klíč
`path.split("/")[-1].split("-")[0]` přeměřil, ne odhadl. Vypsané hodnoty:

```
files : ['doc/intent/nodes/i0001-system.md', 'doc/intent/nodes/i0002-mid.md',
         'doc/intent/nodes/i0007-target.md', 'doc/intent/nodes/i0004-shared.md',
         'doc/intent/nodes/i0006-listener.md', 'doc/intent/nodes/i0008-caller.md']
keys  : ['i0001', 'i0002', 'i0007', 'i0004', 'i0006', 'i0008']
len(files) = 6   len(set(keys)) = 6   -> collapse: False
ancestors = ['i0001', 'i0002']    uses = ['i0004']    talks_to = ['i0006', 'i0008']
```

Pomlčka ve slugu klíč neposune — dělí se na **první** pomlčce, tedy hned za id. Dva různé
uzly se do jednoho klíče slít nemohou (`len(files) == len(set(keys))`, doloženo pro obě
větve), takže rovnost množin neprojde tím, že by dva uniklé uzly splynuly v jeden.
Řazení je bez vlivu: `carried` i `expected` jsou množiny, a `ancestors = ['i0001','i0002']`
ukazuje, že řetězec je opravdu dvouprvkový, ne že by se rodič opakoval.

## `c19` po B3 — „or" je prokázané a přísnost se dál netvrdí

Fixturu jsem si vypsal, protože jednopolní případ je celé jádro B3 a znečištěný uzel by
nedokazoval nic:

```
i0002 engine      unknown_fields=['depth', 'path']  retired_file=False
i0003 path-only   unknown_fields=['path']           retired_file=False
i0004 depth-only  unknown_fields=['depth']          retired_file=False
i0005 clean       unknown_fields=[]                 retired_file=False
i0006 gone        unknown_fields=['depth', 'path']  retired_file=True
errors: 0   warnings: 4
flagged_path : ['i0002', 'i0003', 'i0006']
flagged_depth: ['i0002', 'i0004', 'i0006']
```

`path_only` nese **právě** `['path']`, `depth_only` **právě** `['depth']` — žádné další
neznámé pole, které by nález vyrobilo za ně. Disjunkce je tedy prokázaná v obou
polovinách, a `assertNotIn(path_only, flagged_depth)` / `assertNotIn(depth_only, flagged_path)`
navíc drží, že hlášení nepřestřeluje.

**Přísnost se dál netvrdí**, jak plán slíbil. Predikát filtruje na `finding.code == "V1"`,
nikoli na `finding.level`. Ověřil jsem to pozitivně: po záměně `out.warn` → `out.error`
v `_report_unknown_fields` zůstává sada zelená (`Ran 82 tests … OK`, `exit_code=0`).
Budoucí zpřísnění varování na chybu tedy `c19` neporuší — přesně jak `plan.md` chtěl.

## Co jsem prověřoval a nenašel nic (round 2)

**`c7` — tři odvozovací místa po round 2 dál řežou.** Zmutoval jsem každé zvlášť:
`nodes[*].path` → `'wrong'` (padá `test_index_holds_derived_path_and_depth`
i `test_a_path_in_a_node_file_does_not_reach_a_generated_view`, obě se správnou ascercí),
`nodes[*].depth` → `0` (totéž), `reverse_code_map[*].depth` → `"0"` (padá jen
`test_index_holds_derived_path_and_depth`). Že u prvních dvou padnou dva testy, signál
nekryje — jsou to `c7` a `c20`, oba ta místa legitimně čtou, a každý pád jmenuje svou
vlastní aserci.

**Past u `c19` je pořád dodržená.** Mutace `tree.retired` → `tree.nodes` v prvním cyklu
`_check_identity` shodí `test_derived_fields_…` na `assertIn(gone, flagged_path)`
(`'i0006' not found in {'i0003', 'i0002'}`). Fixtura po B3 má **0 chyb a 4 varování**, tedy
žádný šum, který by nález přebil, a jediné nálezy, které padnou do `flagged_path` /
`flagged_depth`, jsou hlášení o neznámých polích — nic jiného v tom stromu ta dvě slova
ve zprávě nemá (vypsáno, ne odhadnuto).

**Vazba predikátu na slugy fixtury.** Napadlo mě, že slugy `path-only` a `depth-only`
obsahují přesně ta slova, na která predikát matchuje, a že zpráva V1 „file should be named
`i0003-path-only.md`" by uzel označila za nesprávný důvod. Ověřil jsem, že to dnes nehrozí
a že to není jednou mutací zneužitelné: zpráva o názvu souboru v téhle fixtuře nikdy
nevznikne (`TreeBuilder` píše `{id}-{slug}.md`), a když nechám hlášení přestat jmenovat
pole (`"unknown front matter fields present"`), test **padne**
(`'i0002' not found in set()`), takže se o slugy neopírá. Zůstává to jako Minor níž.

## Major

Žádný. `M1` z round 1 je uzavřená — evidence je přeměřená celá, ne dopsaná, a její
citace řádků jsem si ověřil proti odeslaným souborům.

## Minor / neblokující

1. **`M2` z round 1 trvá.** `grader.md:1` má pořád `# Grader â€” doc/runs/…` — UTF-8
   pomlčka zapsaná jako latin-1. Kosmetika v souboru, který čte Human.
2. **Predikát `c19` matchuje celý text nálezu.** `"path" in finding.message` je dnes
   nezneužitelný (viz výš), ale opírá se o to, že žádná jiná zpráva V1 na ty uzly
   nedosáhne. Robustnější by bylo kotvit na prefix `unknown fields:`. Neblokující:
   jednou mutací se to zlomit nedá.
3. **Větev `for_implementation=True` běží s prázdným `code` / `tests`.** `target` nemá
   `code_paths`, takže obě větve dnes vracejí identický `result.files`. Pro B2 to stačí
   (mutace 8 tu větev prokazatelně navštíví), ale interakci mezi výstupem `_expand`
   a `result.files` fixtura nepozoruje — viz „nejsilnější zbývající argument" níž.
4. **Poznámka o `AGENT_MODELS.md` z round 1 zůstává eskalací**, ne blokátorem: v pásmu
   `high` má Kritik i Coder tentýž slug. Formulace omezující tabulky je mimo rozsah běhu.

## Eskalace — nárok před recenzí (nezměněno z round 1)

Nález o tom, že `skills/ice-run/SKILL.md:94-98` nechává `realization claim` proběhnout
před krokem 8, platí beze změny a nepřepisuji ho. Round 2 mu naopak dal druhý empirický
doklad: `realization status --node i0004` hlásí `realized` i teď, po round 1 s verdiktem
REQUEST CHANGES a před tímto verdiktem. Blokátory se opravovaly **v testech**, takže se
nepohnul ani otisk `contracts`, ani `meaning`, a nárok zůstal celou dobu zelený, přesně
jak jsem v round 1 předpověděl. Návrh se nemění: přesunout `claim` do kroku 9, za
`review.md`. Rozhodnutí patří Humanovi.

Pro tento běh z toho dál plyne, že po uzavření B4 je potřeba nárok na `i0004` přepsat
proti finálnímu stavu.

## Co jsem sám ověřil (round 2)

| Příkaz | Výstup | Exit |
|---|---|---|
| `python3 tools/intent/cli.py validate` | `5 node(s): 0 error(s), 0 warning(s)` | 0 |
| `python3 tools/intent/cli.py realization check` | `realization layer consistent (2 entry/entries)` | 0 |
| `python3 tools/intent/cli.py realization status --node i0004` | `i0004  realized` | 0 |
| `python3 tools/intent/cli.py coverage` | `contracts: 28`, `machine-enforced: 28 (100%)`, `files outside any node: 0` | 0 |
| `python3 tools/intent/cli.py scope --run doc/runs/20260817-1853-slice-and-derived-truth-66` | `scope clean (8 declared path(s))` | 0 |
| `python3 -m unittest discover -s tools/intent/tests -t tools` | `Ran 82 tests … OK` | 0 |
| `python3 tools/checks/template_checks.py --root .` | `template contracts satisfied` | 0 |
| `python3 tools/checks/hook_checks.py --root .` | `hook contracts satisfied` | 0 |
| `ruff check tools/` | `All checks passed!` | 0 |
| `ruff format --check tools/` | `19 files already formatted` | 0 |
| `sed -n '43p;165p' tools/intent/tests/test_tools.py` | `assertEqual(carried, expected)` / `assertEqual(str(row["depth"]), "2")` | 0 |
| `sed -n '193p;199p' tools/intent/tests/test_validate.py` | `assertIn(path_only, flagged_path)` / `assertIn(gone, flagged_path)` | 0 |

Rozsah: `git status --short` má pořád právě osm změněných souborů, všechny v `outputs`
nebo `incidental`; nový soubor v běhu nevznikl. `git diff --stat` je prázdný pro
`slicing.py`, `generate.py`, `model.py`, `coverage.py` a `scope.py` — produkční kód se
v round 2 opravdu nehnul, opravily se jen důkazy, což je u nálezů typu „věta sahá dál než
test" ta správná oprava. Scratch kopie `/tmp/adv2` je smazaná.

## Nejsilnější argument, který by proti tomuto diffu šel vznést

Kdyby B4 nebylo, obhajoval bych diff s jednou výhradou, a je fér ji pojmenovat teď, aby ji
nemusel hledat někdo jiný: **větev `for_implementation=True` je navštívená, ale prázdná.**
`target` nemá `code_paths` ani `test_paths`, takže `result.code` a `result.tests` jsou
v obou větvích `[]` a `result.files` je bit za bitem stejný. Mutace, která do
`result.files` přilije `result.code` (`result.files.extend(result.code)`), proto zůstává
zelená — přeměřeno, `Ran 82 tests … OK`.

Netvrdím, že je to porušení `c6`: kvalifikátor „these **intent nodes**" tu drží, protože
kód není intent-uzel, a to jsem se v round 1 snažil zlomit a nezlomil. Argument, který
by šel vznést, je jemnější a mířil by na `render_slice`: `result.files` se tiskne pod
hlavičkou „## Intent nodes (read as truth)". Kdyby některý uzel vlastnil `code_paths`
zahrnující `doc/intent/nodes/`, `_expand` by vrátil soubory uzlů a takový únik by se
v té sekci projevil jako intent-uzel, který tam nepatří. Potřebuje to ale **dvě** shody
zároveň (mutaci **a** strom, kde uzel vlastní vlastní strom záměru), takže vůči jedné
mutaci je test odolný a jako blokátor to neuvádím.

Poctivé řešení je levné a nepatří do tohoto běhu: dát `target` ve fixtuře `code_paths`
plus kontrakt, ať obě větve nejsou identické. Zapisuji to jako **kandidáta na follow-up**,
protože sousedí s tím, co Human odložil (kontrakt nad `render_slice`), a nechci pod
hlavičkou blokátoru propašovat rozsah, který vyřadil.

---

# Round 3 — poslední kolo

## Verdikt — round 3

**APPROVE.**

Tento diff bych obhajoval proti někomu, kdo se ho snaží vyvrátit — protože jsem se o to
sám pokusil třikrát a tentokrát se mi to nepodařilo. B4 je zavřené. Šestimístná tabulka
odvození, kterou jsem v round 2 vyhlásil jako **podmínku ukončení** tohoto běhu, je celá
zelená a podepisuji ji níž po jednom místě, každé samostatnou mutací. Kontrakty, které jsem
uzavřel dřív (`c7`, `c19`), jsem přeměřil znovu, protože fixtura `c6` narostla a chtěl jsem
vědět, jestli se něco nerozvázalo — nerozvázalo.

**Blokátor nemám žádný.** Do stromu záměru nevstupuje žádná nepravdivá věta: `c6`, `c7`
i `c19` jsou pravdivé o kódu a každý z nich je svým vynucovačem dosažený v každé hranici,
kterou jeho věta vyslovuje. Produkční kód se za tři kola nezměnil ani o bajt
(`git diff --stat` pro `slicing.py`, `generate.py`, `model.py`, `coverage.py`, `scope.py`
je prázdný) — celý běh opravil tvrzení a důkazy, ne chování, což je u nálezu „věta sahá dál
než test" ta správná oprava.

Jedna položka se musí opravit **před commitem** a vědomě ji nedávám do žádné ze dvou hromad
(`## Před commitem` níž): dvě z devíti starších mutací v `grader-evidence.md` po round 3
jmenují **nesprávný uzel**. Nezakládá to blokátor podle definice, kterou mám — nic
nepravdivého tím nevstupuje do stromu a věcně každá mutace řeže tak, jak tvrdí (ověřeno
mnou). Je to vada auditního záznamu, ne kontraktu, a její oprava je přepsání textu, ne
čtvrté kolo recenze. Kdyby Human chtěl přísnější čtení („artefakt Definition of Done
obsahující nesprávná id je nepravdivé DoD tvrzení → blokátor"), eskalaci mu neberu
a nebudu proti ní argumentovat.

## Mutace B4 proti finálním testům — doslova

```diff
# tools/intent/slicing.py:70
-    incoming = sorted(other.id for other in tree.nodes.values() if node_id in other.talks_to)
+    first = {other.id for other in tree.nodes.values() if node_id in other.talks_to}
+    second = {o.id for o in tree.nodes.values() if any(f in o.talks_to for f in first)}
+    incoming = sorted(first | second)
```

```
...........................................................FF......................
======================================================================
FAIL: test_slice_carries_exactly_ancestors_uses_and_talks_to_ends (intent.tests.test_tools.SliceTest.test_slice_carries_exactly_ancestors_uses_and_talks_to_ends) (for_implementation=False)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/adv3/tools/intent/tests/test_tools.py", line 51, in test_slice_carries_exactly_ancestors_uses_and_talks_to_ends
    self.assertEqual(carried, expected)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
AssertionError: Items in the first set but not the second:
'i0009'

======================================================================
FAIL: test_slice_carries_exactly_ancestors_uses_and_talks_to_ends (intent.tests.test_tools.SliceTest.test_slice_carries_exactly_ancestors_uses_and_talks_to_ends) (for_implementation=True)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/adv3/tools/intent/tests/test_tools.py", line 51, in test_slice_carries_exactly_ancestors_uses_and_talks_to_ends
    self.assertEqual(carried, expected)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
AssertionError: Items in the first set but not the second:
'i0009'

----------------------------------------------------------------------
Ran 82 tests in 0.172s

FAILED (failures=2)

exit_code=1
reverted byte-exact
```

Padla **jen** metoda `test_slice_carries_exactly_…`, obě její větve, `Ran 82 tests`,
`FAILED (failures=2)`. Žádný jiný test, takže signál nic nezakrývá. `i0009` je
`far_caller`, tedy uzel, který mluví s `caller` a není far end žádné hrany incidentní
s `target` — přesně ta hranice, která v round 2 chyběla. Po reverzi je soubor bajt za
bajtem shodný s repozitářem a sada `OK`.

## Podepisovaná tabulka — šest odvození `c6`, každé samostatnou mutací

Zásah, který jsem provedl v každém místě, a co sada řekla. Vše na `/tmp/adv3`, po každé
mutaci reverze s kontrolou bajtové shody a znovu zelená sada.

| # | Odvození (`build_slice`) | Zásah | Padá | Zpráva | Stav |
|---|---|---|---|---|---|
| 1 | `tree.ancestors(node_id)` | `[-1:]` | `test_slice_carries_exactly_…`, obě větve | `second set but not the first: 'i0001'` | **uzavřeno** |
| 2 | sám `node_id` | vypustit `node_id` z `node_ids` | totéž, obě větve | `second set but not the first: 'i0007'` | **uzavřeno** |
| 3 | `node.uses` | tranzitivní uzávěr | totéž, obě větve | `first set but not the second: 'i0003'` | **uzavřeno** |
| 4 | `node.talks_to` (vlastní hrana) | dva skoky | totéž, obě větve | `first set but not the second: 'i0005'` | **uzavřeno** |
| 5 | `incoming` (příchozí hrana) | dva skoky | totéž, obě větve | `first set but not the second: 'i0009'` | **uzavřeno (B4)** |
| 6 | větev `for_implementation` | potomci při implement | totéž, **jen** větev `True` | `first set but not the second: 'i0012'` | **uzavřeno** |

Místo 2 (`node_id` sám) jsem v round 2 označil za „uzavřené členstvím v `expected`" bez
mutace. V posledním kole jsem si ho nechtěl nechat na slovo, tak jsem ho zmutoval: uzel se
z `node_ids` vypustí a test padne na `'i0007'`. Tabulka je tedy podepsaná celá, ne pět
šestin.

K tomu tři třídy příbuznosti, které věta vylučuje slovy „kinship alone adds none" — každá
má ve fixtuře reprezentanta a každá padá:

| Třída | Zásah | Kdo unikl | Padá |
|---|---|---|---|
| sourozenec (dítě `mid`) | `n.parent == node.parent` | `i0010` (`sibling`) | ano, obě větve |
| strýc (dítě `root` mimo `mid`) | `n.parent == parent.parent` | `i0003`, `i0005`, `i0009`, `i0011` | ano, obě větve |
| opačný směr `uses` | `node_id in n.uses` | `i0011` (`consumer`) | ano, obě větve |
| potomek | potomci při implement | `i0012` (`child`) | ano, větev `True` |

Fixtura má dnes dvanáct uzlů a id se posunula: `far_caller = i0009`, takže `sibling`
je `i0010`, `consumer` `i0011` a `child` `i0012`. Ověřeno výpisem, ne odhadem.

Klíč z cesty jsem přeměřil znovu, protože slugů s pomlčkou je teď víc a uzlů je dvanáct:

```
files : ['i0001-system.md', 'i0002-mid.md', 'i0007-target.md',
         'i0004-shared.md', 'i0006-listener.md', 'i0008-caller.md']
keys  : ['i0001', 'i0002', 'i0007', 'i0004', 'i0006', 'i0008']
len(files) = 6   len(set(keys)) = 6   collapse: False
ancestors = ['i0001', 'i0002']   uses = ['i0004']   talks_to = ['i0006', 'i0008']
tree mutated by build_slice: False        total nodes in fixture: 12
```

Dva různé uzly se do jednoho klíče slít nemohou (`len(files) == len(set(keys))` v obou
větvích), řetězec předků je opravdu dvouprvkový, a `build_slice` strom nemění — snapshot
`(parent, uses, talks_to, source)` všech dvanácti uzlů je před oběma voláními a po nich
identický, takže větve `subTest` si do sebe neteče fixtura.

## Nerozvázalo se to, co jsem uzavřel dřív

Fixtura `c6` narostla o uzel a čísla řádků se posunula, takže jsem `c7` a `c19` neproklamoval
za nedotčené — přeměřil jsem je.

| Kontrakt | Zásah | Výsledek |
|---|---|---|
| `c7` odvození 1 | `nodes[*].path` → `'wrong'` | padá `test_index_holds_derived_path_and_depth` **a** `test_a_path_in_a_node_file_does_not_reach_a_generated_view`, každý na své asercii |
| `c7` odvození 2 | `nodes[*].depth` → `0` | totéž, `0 != 2` a `0 != 1` |
| `c7` odvození 3 | `reverse_code_map[*].depth` → `"0"` | padá **jen** `test_index_holds_derived_path_and_depth`, `'0' != '2'` |
| `c19` dosah | `tree.retired` → `tree.nodes` | padá `test_derived_fields_…` na `assertIn(gone, flagged_path)` |
| `c19` „or" | `if len(node.unknown_fields) > 1` | padá `test_derived_fields_…` na `assertIn(path_only, flagged_path)` |
| `c19` přísnost | `out.warn` → `out.error` | sada **zelená** — úroveň nálezu se dál netvrdí, jak plán slíbil |

Že u prvních dvou padnou dva testy, signál nekryje: jsou to `c7` a `c20`, obě ta místa
legitimně čtou, a každý pád jmenuje svou vlastní aserci.

## Před commitem — jedna položka, není to blokátor ani follow-up

**Mutace 1–9 v `grader-evidence.md` nebyly po round 3 přeměřené.** Přidala se jen mutace 10.
Fixtura `c6` mezitím narostla o `far_caller`, čímž se posunula id i řádky, takže starší
záznamy popisují stav, který už neexistuje:

| Kde | Záznam říká | Ve finálním kódu je |
|---|---|---|
| mutace 2 (příbuznost) | uniklý uzel `'i0009'` | `'i0010'` — `i0009` je dnes `far_caller`, ne `sibling` |
| mutace 8 (větev implement) | uniklý uzel `'i0011'` | `'i0012'` — `i0011` je dnes `consumer`, ne `child` |
| mutace 1, 2, 5, 6, 7, 8 | `test_tools.py, line 43` | řádek 43 je `consumer,` uvnitř množiny `outside`; aserce je na **51** |
| mutace 3 (`c7`) | `test_tools.py, line 165` | řádek 165 je `index = build_index(tree)`; aserce je na **173** |

Řádky `test_validate.py` 193 a 199 sedí — ten soubor se v round 3 nezměnil.

**Proč to není blokátor.** Definice, kterou mám, je „diff tvrdí nepravdu a merge by dostal
nepravdivou větu do stromu záměru". Do stromu nevstupuje nic nepravdivého a věcně je každý
záznam pravdivý v tom, na čem záleží: která mutace, který test, kolik pádů, po reverzi
zelená. Přeměřil jsem si všech deset sám a všechny řežou. Zastaralá jsou id a čísla řádků,
tedy dekorace záznamu. Položka Definition of Done „mutace, každá s pádem právě jednoho
jmenovaného testu" je splněná.

**Proč to přesto není ani follow-up.** Follow-up je něco, co jde odložit do dalšího běhu.
Tohle ne: až se běh uzavře a zapíše, ten záznam už nikdo neopraví, a dvě jeho položky
jmenují nesprávný uzel — čtenář za rok z mutace 2 usoudí, že příbuznostní mutace chytá
`far_caller`, což je nepravda. Je to oprava textu v artefaktu **tohoto** běhu, ne recenze
kódu, a proto ji píšu sem a ne do hromady.

**Co udělat:** spustit devět starších mutací ještě jednou nad finálním kódem a výstupy
přepsat (Coder to udělal po round 1 přesně takto a bylo to správně), nebo — minimum —
nadepsat sekce s mutacemi 1–9 poznámkou, že jsou naměřené nad fixturou před round 3,
a opravit dvě id. První varianta je poctivější a stojí jeden běh sady.

## Follow-up — dvě věci, které tento diff nezavádí a netvrdí o nich nepravdu

Obojí zapisuji tak, aby to Human mohl vzít a vložit do pozdějšího běhu bez odvozování
znovu.

### FU1 — větev `for_implementation=True` je navštívená, ale prázdná

**Co je stav.** `target` ve fixtuře nemá `code_paths` ani `test_paths`, takže
`result.code == []` a `result.tests == []` a obě větve vracejí bit za bitem stejný
`result.files` (změřeno: `code/tests: [] []` v obou větvích). Mutace
`result.files.extend(result.code)` v `slicing.py:89` proto zůstává zelená —
přeměřeno v round 3, `Ran 82 tests … OK`.

**Proč to není blokátor.** `c6` mluví o „these **intent nodes**" a kód není intent-uzel,
takže věta zůstává pravdivá. Snažil jsem se to zlomit v round 1 i round 3 a nezlomil jsem
to. Diff tedy nic nepravdivého netvrdí; jen ta jedna interakce není pozorovaná.

**Co by běh měl udělat.** Dát `target` ve fixtuře `code_paths` (a povinný kontrakt, jinak
padne `V4`) plus soubor přes `builder.write_file`, aby `result.code` nebyl prázdný a obě
větve nebyly identické. Mutace, která se tím zpřístupní, je `result.files.extend(result.code)`.
Pozor na hranici rozsahu: skutečná otázka za tím je, co smí být v sekci
„## Intent nodes (read as truth)", kterou tiskne `render_slice` — a kontrakt nad
`render_slice` Human odložil do `doc/new_ideas/`. Tenhle follow-up má proto zůstat
u fixtury a mutace, dokud se Human nerozhodne o té sekci.

### FU2 — predikát `c19` matchuje celý text nálezu

**Co je stav.** `"path" in finding.message` nad všemi nálezy `V1`. Dnes je to
nezneužitelné — ověřil jsem, že v té fixtuře jsou jediné nálezy obsahující slova
`path` / `depth` právě hlášení o neznámých polích, a že když hlášení přestane jmenovat pole,
test padne. Slugy `path-only` a `depth-only` ale obsahují přesně ta slova, na která se
matchuje, a zpráva `V1` „file should be named `i0003-path-only.md`" by uzel označila za
nesprávný důvod, kdyby kdy vznikla.

**Proč to není blokátor.** Jednou mutací se to zlomit nedá; potřebuje dvě shody zároveň.

**Co by běh měl udělat.** Kotvit predikát na prefix zprávy (`unknown fields:`) místo na
volný text, nebo porovnávat proti `finding.message.split(":", 1)[1]`. Dvě řádky.

## Eskalace — nárok před recenzí (nesu dál nezměněně)

Nález z round 1 platí beze změny a nepřepisuji ho: `skills/ice-run/SKILL.md:94-98` nechává
`realization claim` proběhnout v kroku 7, tedy **před** krokem 8, kde běží Adversář.
Round 2 mu dal druhý empirický doklad a round 3 třetí: `realization status --node i0004`
hlásí `realized` i teď a hlásil to nepřerušeně přes **dva** verdikty REQUEST CHANGES.
Důvod je aritmetický, ne náhodný — všechny čtyři blokátory se opravovaly v testech, takže
se nepohnul ani otisk `contracts`, ani `meaning`, a nárok se sám opravit nemohl. `unclaim`
neexistuje. Návrh se nemění: přesunout `claim` do kroku 9, za `review.md`.

Pro tento běh z toho plyne konkrétní úkol při uzavírání: nárok na `i0004` **přepsat**
(`realization claim i0004 --evidence doc/runs/20260817-1853-slice-and-derived-truth-66
--by Coordinator`) proti finálnímu stavu, aby evidence ukazovala na běh, jehož recenze je
uzavřená, a ne na stav, který mezitím třikrát prošel opravou.

## Minor / neblokující (round 3)

1. `M2` z round 1 je **opravená**: `grader.md:1` je dnes
   `# Grader for run doc/runs/20260817-1853-slice-and-derived-truth-66`, bez rozbité
   pomlčky.
2. `report.md` „Reference do kódu" uvádí u `c7` `~155–165`; aserce jsou dnes na 159–173.
   Tilda naznačuje přibližnost, takže to netvrdím jako nepravdu, jen bych to opravil při
   přepisu evidence.
3. Poznámka o `AGENT_MODELS.md` z round 1 zůstává **eskalací**, ne blokátorem: v pásmu
   `high` má Kritik i Coder tentýž slug, a je to podle katalogu, ne proti němu.

## Co jsem sám ověřil (round 3)

| Příkaz | Výstup | Exit |
|---|---|---|
| `python3 tools/intent/cli.py validate` | `5 node(s): 0 error(s), 0 warning(s)` | 0 |
| `python3 tools/intent/cli.py realization check` | `realization layer consistent (2 entry/entries)` | 0 |
| `python3 tools/intent/cli.py realization status --node i0004` | `i0004  realized` | 0 |
| `python3 tools/intent/cli.py coverage` | `contracts: 28`, `machine-enforced: 28 (100%)`, `files outside any node: 0` | 0 |
| `python3 tools/intent/cli.py scope --run doc/runs/20260817-1853-slice-and-derived-truth-66` | `scope clean (8 declared path(s))` | 0 |
| `python3 -m unittest discover -s tools/intent/tests -t tools` | `Ran 82 tests … OK` | 0 |
| `python3 tools/checks/template_checks.py --root .` | `template contracts satisfied` | 0 |
| `python3 tools/checks/hook_checks.py --root .` | `hook contracts satisfied` | 0 |
| `ruff check tools/` | `All checks passed!` | 0 |
| `ruff format --check tools/` | `19 files already formatted` | 0 |
| `git diff --stat -- tools/intent/{slicing,generate,model,coverage,scope}.py` | prázdný | 0 |

Deset mutací na scratch kopii `/tmp/adv3` (šest odvození, tři třídy příbuznosti, plus
`node_id`), šest kontrolních mutací na `c7` a `c19`, jedna na follow-up FU1. Po každé
reverze s kontrolou bajtové shody proti repozitáři. Scratch kopie je smazaná,
`git status --short` má pořád právě osm změněných souborů a všechny jsou v `outputs` nebo
`incidental`.

## Co tento diff o uzlu `i0004` dokazuje a co ne

**Dokazuje** tohle a nic víc: tři konkrétní věty na `i0004` — `c6`, `c7` a `c19` — jsou
pravdivé o kódu v `tools/` a každá z nich je svým jmenovaným vynucovačem dosažená v každé
hranici, kterou sama vyslovuje. U `c6` to znamená šest odvozovacích míst a čtyři třídy
vyloučení, každé s mutací, která je opravdu shodí; u `c7` tři odvozené hodnoty nesené
generovaným indexem; u `c19` případ „jen path", „jen depth", „obě", „čistý uzel" a soubor
v `_retired/`, s vědomě netvrzenou úrovní nálezu. Ověřeno mutacemi, ne čtením, a ne z tabulky
Codera. **Nedokazuje** ale, že je uzel `i0004` jako celek splněný. Zbývajících sedmnáct
kontraktů (`c1`–`c5`, `c8`–`c18`, `c20`) tento běh jen spustil — nikdo v něm neauditoval,
jak daleko sahají jejich vynucovače, a vzorec „věta sahá dál než test", který se u tří
kontraktů našel čtyřikrát ve třech kolech, je dobrý důvod předpokládat, že u některých
z těch sedmnácti sedí taky. Nedokazuje, že je nástroj správný: 82 unit testů pokrývá
chování, které by budoucí změna mohla věrohodně rozbít, ne úplnost `tools/`. Nedokazuje nic
o textu, který `render_slice` vytiskne, ani o příkazu `owner` — to Human odložil. A hlavně:
značka `realized` v realizační vrstvě znamená „někdo tvrdil splnění proti tomuhle znění
a vynucovače jsou dosažitelné", nikoli „ty testy řežou". Že to jsou dvě různé věci, není
teorie — tenhle běh to předvedl třikrát: značka byla zelená nepřerušeně přes dva verdikty
REQUEST CHANGES a čtyři blokátory. Kdo bude tuhle větu čtený za rok, ať z ní vezme
tohle: zelená vrstva je záznam tvrzení, ne důkaz, a jediný důkaz je ten, který někdo
zkusil zlomit.
