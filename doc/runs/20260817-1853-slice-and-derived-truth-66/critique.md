---
run_id: 20260817-1853-slice-and-derived-truth-66
intent_ids: ["i0004"]
role: Critic
model: cursor-grok-4.5-high
complexity: high
status: done
---

# Kritika změny záměru a plánu

## Verdikt

**ACCEPT** — změna záměru i plán. Blokátory nejsou. Coder může začít.

Každou navrhovanou větu jsem četl proti kódu v `tools/`, ne proti popisu v plánu. Čtyři
mutace jsem přeměřil na scratch kopii `tools/` (pracovní strom repozitáře jsem neměnil):
každá shodí právě jmenovaný test a nic jiného; po návratu zdroje je sada znovu zelená
(82 testů). Navržené úpravy testů + `validate.py` + `helpers.py` na téže kopii dají
`Ran 82 tests ... OK` ještě před mutacemi.

## F1 — `c6`: znění je pravda o kódu

### Co `build_slice` skutečně skládá do intent-uzlů

`tools/intent/slicing.py:63-95`: do `result.files` jdou jen cesty z `_node_file` pro
`[*ancestors, node_id, *uses, *talks_to]`, kde `talks_to` je sjednocení vlastních i
příchozích hran (`:70-71`). ADR jdou do `result.adrs` (`:86`), kód/testy při
`for_implementation=True` do `result.code` / `result.tests` (`:87-89`) — **ne** do
`result.files`. `render_slice` (`:98-138`) tiskne ty sekce odděleně.

Nová věta říká „exactly these **intent nodes**“, ne „exactly the slice“. Referent je
tedy množina uzlů v `result.files`, ne celý dokument. To je přesně ta past, na kterou
plán ukazuje, a formulace ji řeší: kdyby chybělo „intent nodes“, byla by věta nepravdivá
o ADR a o implementačním výřezu. Ověřeno i spuštěním: stejná množina id v `result.files`
při `for_implementation=False` i `True`; self-`talks_to` jen zdvojí id v seznamu, soubor
jednou.

### Odvození id z cesty

`path.split("/")[-1].split("-")[0]` sedí na skutečný tvar z `_node_file` + `TreeBuilder`:
`doc/intent/nodes/{id}-{slug}.md` → `{id}`. Na osmiuzlové fixtuře z plánu je výsledek
identický s lookupem přes `node.source`. Špatný klíč by fixturu neprošel; tady neprochází
„náhodou“.

### Granularita: jeden kontrakt

Pravidlo v `## Contracts` uzlu (`i0004`): dvě půlky → jeden test, který dokáže obě, jinak
dva kontrakty. Rovnost množin je nejsilnější forma té první větve: obě mutace (kladná i
záporná) padají na **tomtéž** `assertEqual` (`Items in the second… 'i0005'` /
`Items in the first… 'i0006' 'i0007'`). Druhá aserce `carried & {sibling, consumer, child}`
je odvoditelná a slouží jen pojmenování úniku — není druhý kontrakt. Kalibrace `c14`
zůstává nedotčená, jak delta slibuje.

### „Exactly“ a potomci — poctivé zpřísnění, ne scope creep

Stará věta o potomcích mlčela; nová slovem „exactly“ a fixturou s `child` závazně říká,
že potomci ve slice nejsou. To nikdo výslovně neobjednal, ale:

1. požadavek žádá říct, **co slice skutečně dělá** — vyčerpávající charakteristika je
   přirozený tvar pravdivé věty;
2. bez uzavřené množiny by „kinship alone adds none“ nešlo dokázat jednou rovností proti
   konkrétnímu pozitivnímu seznamu;
3. delta to přiznává nahlas (změna záměru, ne refaktor), takže závazek nejde přehlédnout.

Oslabení (sourozenec **s** hranou smí) je jediné autorizované. Nic jiného v deltě netvrdí
méně než dnes.

## F2 — `c7`: text drží, dosah sedí

V `tools/intent/generate.py::build_index` se `depth` odvozuje právě **dvakrát**:
`nodes[*].depth` (`:73`, `len(path) - 1` jako int) a `reverse_code_map[*].depth`
(`:92`, totéž jako `str`). Třetí odvození hloubky v `generate.py` není; `render_map`
(`:34`) skládá jen path do `MAP.md`, což není index a `c7` o něm nemluví. Řazení
(`:94`) plán správně nekontraktuje.

Doplnění `code_paths` + kontraktu na `grandchild` existující aserce nerozbije
(naměřeno na scratch): path/depth/`children`/`schema_version` zůstávají, přibude řádek
reverzní mapy s `depth == "2"`. `next(..., None)` + `assertIsNotNone` je správná obrana
proti `StopIteration`.

## F3 — `c19`: nástroj roste, past je dodržená

Dnes `_check_identity` (`validate.py:52-74`) iteruje jen `tree.nodes`; retired soubor s
`path`/`depth` má `unknown_fields`, ale validate o něm mlčí (naměřeno). Volba rozšířit
hlášení místo zúžení věty neoslabuje kontrakt a drží se jediné autorizované korekce (`c6`).

Explicitní keyword `retired=` v `TreeBuilder.add` je **nutný i dostatečný** v podobě, kterou
plán popisuje: položka v `**fields` by skončila ve front matteru jako neznámé pole a soubor
by zůstal v `nodes/` — fixtura by měřila sebe. Plánované chování (adresář `_retired/`,
`status: retired`, `retired: true` v registru) je přesně to, bez čeho by V7/V1 zastínily
`c19`.

Zdvojení u current uzlů nevznikne (`tree.nodes` ∩ `tree.retired` je prázdný). Na tomto
stromu `_retired/` není — `validate` dnes `0 error(s), 0 warning(s)`; rozšíření samo o sobě
nové nálezy nepřidá. Mutace 4 (`for node in tree.nodes` místo `tree.retired` v prvním
cyklu) shodí právě `test_derived_fields_…` se zprávou `'i0004' not found in {'i0002'}`.

## Definition of Done a rozsah

- Položky DoD jsou kontrolovatelné příkazem nebo diffem; žádná není širší než výstupy běhu.
- `scope --run …` **bez** `--node` je opravdu přísnější brána: `scope.py:95-99` při
  `--node i0004` přidá `code_paths`/`test_paths` uzlu (tedy celé `tools/`). Plán to má správně.
- Výstupy neobsahují `slicing.py` / `generate.py` — F1 a F2 mění tvrzení a důkaz, ne chování.
- Mimo rozsah (`render_slice`, `owner`, `scope --base`, `AGENT_MODELS.md`) neeskaluji;
  pro správnost tohoto běhu nejsou nosné.

## Mutace (přeměřeno)

| # | Kontrakt | Padá právě | Očekávaná zpráva (shodná s plánem) |
|---|---|---|---|
| 1 | `c6` kladná | `test_slice_carries_exactly_…` | `Items in the second set but not the first: 'i0005'` |
| 2 | `c6` vyčerpávající | totéž | `Items in the first set but not the second: 'i0006' 'i0007'` |
| 3 | `c7` | `test_index_holds_derived_path_and_depth` | `'0' != '2'` |
| 4 | `c19` | `test_derived_fields_in_a_node_file_are_reported` | `'i0004' not found in {'i0002'}` |

U mutace 1 zůstává `test_slice_includes_incoming_talks_to` zelený — bere soubor, ne seznam
hran. U mutace 3 zůstává `test_reverse_lookup_prefers_the_deepest_node` zelený —
`find_node_for_path` si hloubku počítá sám.

## Poznámky (neblokující)

1. Odvození id z basename je svázané s konvencí `{id}-{slug}.md` (V1 ji vynucuje). Křehčí
   než lookup přes `tree.nodes`, ale na dnešním kódu pravdivé.
2. Mutace 2 přidává **sourozence**, ne potomky; vyloučení `child` drží samotná rovnost
   množin ve fixtuře. Na jeden kontrakt to stačí.
3. Out of scope záměrně: kontrakt nad textem, který `render_slice` vytiskne. Věta `c6` o
   něm nemluví a po „intent nodes“ ani nemusí.

## Co jsem nejméně jistý

Zda by nepřátelský čtenář ještě dokázal přečíst „A slice carries exactly…“ jako tvrzení o
celém dokumentu slice navzdory kvalifikátoru „these intent nodes“. Já bych tu větu bránil:
gramatický referent je uzavřený seznam druhů uzlů a test sahá na `result.files`. Kdyby
Human chtěl ještě silnější ochranu proti tomu čtení, patřilo by to do follow-up o
`render_slice` (už je v `doc/new_ideas/`), ne do blokace tohoto běhu.
