---
run_id: 20260817-1853-slice-and-derived-truth-66
intent_ids: ["i0004"]
role: Planner
model: claude-opus-5-thinking-high
complexity: high
status: in-progress
outputs:
  - doc/intent/nodes/i0004-intent-tooling.md
  - tools/intent/validate.py
  - tools/intent/tests/helpers.py
  - tools/intent/tests/test_tools.py
  - tools/intent/tests/test_validate.py
incidental:
  - doc/intent/MAP.md
  - doc/intent/INDEX.json
  - doc/intent/_realization.yaml
---

# Plán

## Cíl

Po tomto běhu je každý kontrakt `i0004` pravdivý a dosažený svým vynucovačem ve všech třech
místech, kde to dnes neplatí: `c6` říká, co `build_slice` skutečně dělá, a jeho test to
prokazuje rovností množin (ne podřetězcem jedné fixtury); `c7` má důkaz na **obou** místech,
kde `build_index` odvozuje `depth`; `c19` platí i o souboru uzlu v `_retired/`, protože
`_check_identity` tam hlášení o neznámých polích od teď pošle. Měřitelně: pro každý z těch
tří kontraktů existuje mutace produkčního kódu, pod kterou padne právě jeho test a nic
jiného, a všechny jsou zaznamenané v `grader.md`.

Cíl se vědomě netýká ničeho dalšího. Zejména se nedotýká `c1`–`c5`, `c8`–`c18` a `c20`,
neřeší `render_slice` ani příkaz `owner`, nezavádí `scope --base` a nemění `AGENT_MODELS.md`
— to jsou položky, které Human přesunul do `doc/new_ideas/`.

## Výstupy

`doc/intent/nodes/i0004-intent-tooling.md` — nový text a nový vynucovač `c6`, plus jeden
vložený odstavec v `## Contracts`. Přesná znění jsou v `change.md` a Coder je opisuje
doslova, nepřeformulovává.

`tools/intent/validate.py` — **jediná** změna produkčního kódu v běhu: hlášení o neznámých
polích se pošle i na `tree.retired`.

`tools/intent/tests/helpers.py` — `TreeBuilder.add` umí postavit retired soubor uzlu.

`tools/intent/tests/test_tools.py` — přepsaný a přejmenovaný test slice, rozšířený test
indexu.

`tools/intent/tests/test_validate.py` — rozšířený test odvozených polí.

Nic jiného. Zejména se **nemění** `tools/intent/slicing.py`, `generate.py`, `model.py`,
`coverage.py` ani `scope.py`: F1 a F2 jsou opravy tvrzení a důkazů, ne chování. Počet testů
zůstává 82 — jeden se přejmenovává, dva se rozšiřují, žádný nepřibývá ani nemizí.

## Testovací specifikace

Každý test musí ve **svém vlastním těle** prokázat celou větu svého kontraktu.

### `c6` — `test_tools.py::SliceTest::test_slice_carries_exactly_ancestors_uses_and_talks_to_ends`

Přejmenovaný a přepsaný `test_slice_contains_ancestors_and_uses_but_not_siblings`. Nový
test nevzniká: starý pokrývá tutéž větu, jen v jediné její větvi.

Fixtura (osm uzlů, všechny hrany deklarované ve front matteru, žádná mutace `tree` po
`finish()`; pořadí vzniku je dané tím, že `TreeBuilder` přiděluje id postupně):

| Uzel | Vztah k `target` | Ve slice |
|---|---|---|
| `root` | předek | ano |
| `shared` | `target.uses = [shared]` | ano |
| `listener` | `target.talks_to = [listener]` | ano |
| `target` | sám uzel | ano |
| `caller` | `caller.talks_to = [target]` — příchozí hrana | ano |
| `sibling` | dítě `root`, žádná hrana | **ne** |
| `consumer` | `consumer.uses = [target]` — hrana obráceným směrem | **ne** |
| `child` | dítě `target` | **ne** |

Tělo musí prokázat rovnost množin, ne příslušnost podřetězce:

```python
result = build_slice(tree, target, for_implementation=False)
carried = {path.split("/")[-1].split("-")[0] for path in result.files}
self.assertEqual(carried, {root, target, shared, listener, caller})
# Implied by the equality above; kept so a leak names the relation that leaked.
self.assertEqual(carried & {sibling, consumer, child}, set())
```

Druhá aserce je z první odvoditelná a je tam schválně: `assertEqual` nad množinami vypíše
při pádu id, ne roli, a tenhle řádek udrží ve zdroji pojmenované, která příbuznost se do
slice pustila. Zároveň drží proměnné použité, takže `ruff` nehlásí F841.

`test_slice_includes_incoming_talks_to` zůstává **nedotčený** a nadále bez kontraktu.
Není to duplikát: asertuje `result.talks_to` (hrana je rozpoznaná), zatímco nový test
asertuje `result.files` (soubor je nesen). Právě na tom rozdílu stojí mutace 1 — ta nechá
seznam hran správný a vezme jen soubor, takže starý test zůstane zelený. Kdo ho sloučí do
nového, přijde o tu rozlišovací schopnost.

### `c7` — `test_tools.py::GeneratedViewTest::test_index_holds_derived_path_and_depth`

Rozšíření, ne nový test: věta `c7` je jedna a nejde jí přiřadit dvě těla. Fixtura se doplní
o `code_paths` na nejhlubším uzlu, aby vůbec vznikl řádek reverzní mapy:

```python
grandchild = self.builder.add(
    "schema",
    parent=child,
    code_paths=["src/schema/"],
    contracts=[{"id": "c1", "text": "x", "enforced_by": "cmd: true"}],
)
```

Stávající aserce (`path`, `depth == 2`, `children`, `schema_version`) zůstávají a přibývá
druhé místo odvození:

```python
# The index derives depth twice: once per node entry, once per reverse row.
row = next((item for item in index["reverse_code_map"] if item["node"] == grandchild), None)
self.assertIsNotNone(row, f"no reverse row for node {grandchild}")
self.assertEqual(str(row["depth"]), "2")
```

`next(..., None)` s `assertIsNotNone` je záměr, ne opomenutí: chybějící řádek má být FAIL se
jménem uzlu, ne `StopIteration` ERROR (poučení z recenze běhu 1703). `str(row["depth"])`
snáší dnešní řetězcovou reprezentaci i případný přechod na `int`, ale hodnotu drží pevně —
kontrakt mluví o odvozené hodnotě, ne o typu v JSON.

Řazení reverzní mapy se **neasertuje**. Je to jiné tvrzení než „nese odvozenou hloubku" a
tento běh ho nezavádí; zdůvodnění je v `change.md`.

### `c19` — `test_validate.py::DerivedFieldTest::test_derived_fields_in_a_node_file_are_reported`

Rozšíření o třetí případ. Test už má kladný (`engine`) a záporný (`clean`) případ; přibývá
kladný případ v `_retired/`, protože věta kontraktu mluví o souboru uzlu bez rozlišení:

```python
# A retired file is a node file too, and its derived fields are the same mistake.
gone = self.builder.add("gone", parent=root, retired=True, path="nonsense/place", depth=99)
...
self.assertIn(gone, flagged)
```

Predikát `names_path_and_depth` zůstává, jak je — úroveň nálezu se dál **netvrdí**
(`c19` říká „is reported", ne „is an error"), takže zpřísnění varování na chybu v budoucnu
kontrakt neporuší.

Triáda z Definition of Ready je tím pokrytá: happy path (uzel s poli je ohlášen), hranice
(retired soubor mimo `nodes/`; příchozí hrana a příbuznost u `c6`; druhé místo odvození u
`c7`), chybový případ (čistý uzel ohlášen být **nesmí** — `assertNotIn(clean, flagged)`).

### Pomocník `TreeBuilder.add`

Nový **explicitní** keyword `retired: bool = False`, nikoli položka v `**fields` — ta by
skončila ve front matteru jako neznámé pole a fixtura by si sama vyrobila nález, který má
měřit. Při `retired=True`:

- soubor jde do `doc/intent/_retired/` místo `nodes/` (`RETIRED_DIRNAME` z `intent.model`),
- výchozí `status` je `retired` (dál přepsatelný přes `fields`),
- záznam v `_registry.yaml` dostane `retired: true`.

Bez posledních dvou bodů by fixtura padala na `V7` a test by měřil něco jiného, než tvrdí.
Ověřeno: takový strom dá dvě varování `V1` (current + retired uzel) a **nula chyb**.

### Produkční změna pro `c19`

V `_check_identity` (`tools/intent/validate.py:52`) se hlášení vytkne do funkce a zavolá
nad oběma slovníky. Tvar, který jsem ověřil:

```python
def _report_unknown_fields(node: Node, out: _Collector) -> None:
    if node.unknown_fields:
        out.warn("V1", node.id, f"unknown fields: {', '.join(node.unknown_fields)}")


def _check_identity(tree: Tree, out: _Collector) -> None:
    # A retired file is still a node file, so derived data written into it is the same
    # mistake. Only this one report reaches it: the rest of V1 fires on exactly what
    # makes a node retired.
    for node in tree.retired.values():
        _report_unknown_fields(node, out)
    for node in tree.nodes.values():
        ...
        _report_unknown_fields(node, out)   # nahrazuje dnešní dvojici řádků :70-71
```

Past je v tom komentáři a je závazná: `tree.retired` se **nesmí** protáhnout celou funkcí.
Retired uzel z definice padá na „id is marked retired in the registry but the node is
active" a celá funkce by z každého retired souboru udělala chybu. `Node` je potřeba doplnit
do importů z `intent.model`.

## Failing-test evidence — čtyři mutace, každá jeden padající test

Coder je spustí v tomto pořadí, po každé zaznamená výstup do `grader.md`, vrátí zdroj do
původního stavu a doloží, že sada je zpět zelená. Mutace jsem naměřil na kopii v `/tmp`;
hodnoty ve sloupci „Očekávaný pád" jsou skutečné výstupy, ne odhad, a Adversář je má
reprodukovat samostatně.

### Mutace 1 — `c6`, kladná půlka (příchozí hrana nese soubor)

`tools/intent/slicing.py`, funkce `build_slice`, řádek 80.

```python
# před
    node_ids = [*ancestors, node_id, *result.uses, *result.talks_to]
# po
    node_ids = [*ancestors, node_id, *result.uses, *node.talks_to]
```

Očekávaný pád: **jen** `test_slice_carries_exactly_ancestors_uses_and_talks_to_ends`,
`AssertionError: Items in the second set but not the first: 'i0005'`. Zbytek sady zelený,
včetně `test_slice_includes_incoming_talks_to` — mutace bere soubor, ne seznam hran, a přesně
to je ta mezera, kterou `c6` dosud mělo.

### Mutace 2 — `c6`, vyčerpávající půlka (příbuznost sama nepřidává)

`tools/intent/slicing.py`, funkce `build_slice`, řádek 80.

```python
# před
    node_ids = [*ancestors, node_id, *result.uses, *result.talks_to]
# po
    siblings = [n.id for n in tree.nodes.values() if n.parent == node.parent and n.id != node_id]
    node_ids = [*ancestors, node_id, *result.uses, *result.talks_to, *siblings]
```

Očekávaný pád: **jen** týž test, `AssertionError: Items in the first set but not the second:
'i0006' 'i0007'` (sourozenec bez hrany a spotřebitel s hranou obráceným směrem). Že obě
mutace padají na jedné a téže aserci, je zároveň důkaz rozhodnutí z `change.md`, že `c6` je
jeden kontrakt, ne dva.

### Mutace 3 — `c7`, druhé místo odvození

`tools/intent/generate.py`, funkce `build_index`, řádek 92.

```python
# před
            reverse.append({"code_path": code_path, "node": node.id, "depth": str(len(path) - 1)})
# po
            reverse.append({"code_path": code_path, "node": node.id, "depth": "0"})
```

Očekávaný pád: **jen** `test_index_holds_derived_path_and_depth`, `AssertionError: '0' != '2'`.
`test_reverse_lookup_prefers_the_deepest_node` zůstává zelený, protože `find_node_for_path`
si hloubku počítá sám (`coverage.py:94`) a řádky indexu nečte — mutace je tedy opravdu
mířená na `c7`, ne na chování příkazu `owner`.

### Mutace 4 — `c19`, dosah na `_retired/`

`tools/intent/validate.py`, funkce `_check_identity`, nový první cyklus.

```python
# před
    for node in tree.retired.values():
# po
    for node in tree.nodes.values():
```

Očekávaný pád: **jen** `test_derived_fields_in_a_node_file_are_reported`,
`AssertionError: 'i0004' not found in {'i0002'}` (retired uzel není mezi ohlášenými).
Zdvojené varování u current uzlů nic nerozbije, protože test pracuje s množinou — mutace je
jednotoková a nedotkne se ničeho jiného.

## Definition of Done

- [ ] `c6` v uzlu nese **doslova** text a `enforced_by` z `change.md`;
      `grep -rn "never siblings" doc/intent tools` nic nenajde
- [ ] `grep -rn "test_slice_contains_ancestors_and_uses_but_not_siblings" . --exclude-dir=doc/runs --exclude-dir=.git`
      nic nenajde (staré jméno testu nezůstalo ani v `INDEX.json`)
- [ ] Tělo `test_slice_carries_exactly_ancestors_uses_and_talks_to_ends` obsahuje rovnost
      množin nad `result.files` a fixtura obsahuje všech osm uzlů z tabulky výše, včetně
      `consumer` a `child`
- [ ] `test_index_holds_derived_path_and_depth` asertuje `depth` řádku `reverse_code_map`
      a stávající čtyři aserce zůstaly
- [ ] `test_derived_fields_in_a_node_file_are_reported` asertuje retired uzel mezi
      ohlášenými a čistý uzel mimo ně; predikát dál netvrdí úroveň nálezu
- [ ] `_check_identity` posílá na `tree.retired` **jen** hlášení o neznámých polích
      (`git diff tools/intent/validate.py` neobsahuje nic jiného)
- [ ] Do sekce `## Contracts` vložen odstavec ze `change.md`; ostatní tři odstavce sekce má
      `git diff` nedotčené
- [ ] `git diff` je prázdný pro `tools/intent/slicing.py`, `generate.py`, `model.py`,
      `coverage.py` a `scope.py`
- [ ] Čtyři mutace v `grader.md`, každá s diffem, s pádem právě jednoho jmenovaného testu
      a s návratem sady do zelené
- [ ] `python3 tools/intent/cli.py validate` → exit 0, `0 error(s), 0 warning(s)`
      (stejně jako před během — `_retired/` v tomto repozitáři není)
- [ ] `python3 tools/intent/cli.py realization check` → exit 0
- [ ] `python3 -m unittest discover -s tools/intent/tests -t tools` → `Ran 82 tests ... OK`
- [ ] `python3 tools/checks/template_checks.py --root .` a
      `python3 tools/checks/hook_checks.py --root .` → exit 0
- [ ] `python3 tools/intent/cli.py map` proběhl, `MAP.md` i `INDEX.json` nesou nové znění
      `c6` a `validate` nehlásí `V9`
- [ ] `ruff check tools/` a `ruff format --check tools/` čisté
- [ ] `python3 tools/intent/cli.py scope --run doc/runs/20260817-1853-slice-and-derived-truth-66`
      → exit 0, **bez** `--node` (s `--node i0004` by brána povolila celé `tools/`)
- [ ] `doc/intent/_realization.yaml` není v `git status --short` po práci Codera;
      `realization status --node i0004` hlásí `stale`, dokud tvrzení nezapíše Coordinator

## Co plán vědomě nedělá

- Nezavádí nové id kontraktů. `c6` je jeden kontrakt (zdůvodnění v `change.md`), `c7` a
  `c19` mění jen dosah důkazu, takže posloupnost zůstává na `c20`.
- Nekontraktuje řazení `reverse_code_map` ani odvozenou cestu v `render_slice` a v příkazu
  `owner`.
- Nemění úroveň nálezu `V1` z varování na chybu. Je to obhajitelné, ale je to rozhodnutí o
  nástroji, ne úklid tvrzení.
- Nemaže ani neslučuje `test_slice_includes_incoming_talks_to`.
- Nezapisuje vrstvu realizace. `claim` patří Coordinatorovi po zelené bráně.
