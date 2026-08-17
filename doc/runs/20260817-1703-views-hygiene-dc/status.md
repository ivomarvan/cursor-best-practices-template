---
run_id: 20260817-1703-views-hygiene-dc
intent_ids: ["i0004"]
role: Coordinator
model: claude-opus-5-thinking-high
complexity: high
status: done
---

# Stav běhu

## Výsledek

Běh **dokončen**. Adversář dal `APPROVE` ve druhém kole, Kritik `ACCEPT` v prvním. Otevřený
nález z předchozího běhu je uzavřený: `c7` mluví o generovaném indexu, `c20` je doložené na
obou pohledech, `INDEX.json` i `MAP.md`.

Běh přebral nezacommitovanou práci zastaveného běhu `20260816-2145-contract-hygiene-cd` a
deklaroval ji jako vlastní výstupy, takže se celá oprava — hotová i dodělaná — uzavírá
jedním commitem.

## Průběh bran

| Brána | Kolo | Výsledek |
|---|---|---|
| Kritik na deltě a plánu | 1 | `ACCEPT`, jedna podmínka: Coder nesmí editovat `test_validate.py` |
| Grader (`VERIFY.md`) | — | vše 0, ověřeno Coordinatorem nezávisle na Coderovi |
| Adversář | 1 | `REQUEST CHANGES`, jeden bloker |
| Adversář | 2 | `APPROVE` |

Pořadí bylo správné: Kritik před kódem, Adversář po něm, Grader mezi. Poprvé za tři běhy
bez odchylky.

## Bloker, který Adversář našel — vada se přestěhovala potřetí

`render_map` píše tři věci: řádek tabulky, mermaid diagram a souhrn kontraktů. Mapová
polovina nového testu vylučovala `nonsense/place` jen z **řádku uzlu**, takže Adversář nechal
zapsanou cestu prosáknout do labelu diagramu:

```
i0002["i0002<br/>engine<br/>nonsense/place"]
```

`nonsense/place` v `MAP.md`, `c20` porušené, `Ran 82 tests ... OK`.

Nešlo o přísnější výklad. `plan.md` tu aserci žádal jmenovitě a Coder ji zúžil na řádek;
v `report.md` to nejprve uvedl jako vlastní rozhodnutí. Testová specifikace plánu váže
Codera stejně jako kontrakt váže kód — zúžit ji smí Planner, ne ten, kdo ji plní.

Opraveno doplněním dokumentové aserce vedle řádkové (obě mají smysl: řádková drží, že
odvozená cesta je na správném místě, dokumentová, že zapsaná není nikde) a třetí mutací v
`grader.md`. Adversář si obojí přeměřil sám.

## Vzorec, který stojí za pojmenování

Třikrát po sobě byla oprava správná v tom, na co ukazovala, a slepá k sousedovi, kterého
nikdo nepojmenoval: `c4` a bratranci → `c7`/`c20` a druhý generovaný pohled → `c20` a
mermaid diagram uvnitř téhož pohledu. Pokaždé to našel až ten, kdo četl kontrakt **proti
kódu**, ne proti plánu, a hledal všechna místa, kterých se věta může týkat.

Do zadání Adversáře to od tohoto běhu patří výslovně. Zde to zabralo napoprvé.

## Otevřené nálezy pro navazující práci

Adversář si vymínil, že tu budou i s reprodukcí, ne jako holá řádka v tabulce — předchozí
běh ukázal, že nález přežije jen tak, jak je zapsaný.

### N1 — `c6` je nepravdivé a vyvrací ho vlastní testovací sada. **Rozhodnutí Humana.**

`c6` říká „A slice carries ancestors and semantic dependencies but **never siblings**".
`build_slice` (`tools/intent/slicing.py:70`, `:80-84`) ale bere i **příchozí** hrany
`talks_to`, takže sourozenec s takovou hranou se do slice dostane:

```
files: ['…/i0001-system.md', '…/i0003-target.md', '…/i0002-sibling.md']
SIBLING FILE IN SLICE: True
```

`test_slice_includes_incoming_talks_to` (`tools/intent/tests/test_tools.py:34-42`) přesně
tuhle dvojici sourozenců staví — sada tedy sama dokazuje opak toho, co `c6` tvrdí.
Vynucovač `c6` testuje jen sourozence **bez** hrany `talks_to`, tedy jedinou větev, ve
které věta platí.

Proč Human: opravit se to dá jen v textu. Druhá cesta — dotáhnout kód, aby slice sourozence
nenesla — by rozbila to, co metodika sama chce (`07-intent-tree.mdc`: „`talks_to` enters as
**context**"). Text se tedy bude zužovat, a to je oslabení kontraktu. Na výběr je
přeformulovat `c6` tak, aby `talks_to` jmenoval, nebo ho rozdělit na dva kontrakty.

### N2 — `build_index` počítá `depth` na dvou místech, test sahá na jedno

`tools/intent/generate.py:73` (`nodes[*].depth`) a `:92` (`reverse_code_map[*].depth`).
Mutace, která nechá zapsaný `depth` vyhrát **jen** v reverzní mapě, projde zeleně; mutace
`nodes[*]` padne (`AssertionError: 99 != 1`).

Zúžené `c7` tím nepadá — kvantifikátor v něm není a `nodes[*]` odvozený path i depth nese.
Je to ale táž konfigurace, ze které vyrostly předchozí dva nálezy, tentokrát uvnitř funkce,
kterou běh přezkoumával. Pro Humana to není: rozšíření vynucovače je posílení, tedy práce
běžného běhu.

### N3 — odvozenou cestu vypisují i dva pohledy, o kterých nemluví žádný kontrakt

`render_slice` (`tools/intent/slicing.py:100`, `:105`) a příkaz `owner`
(`tools/intent/main.py:213`). Generované pohledy to nejsou, takže `c20` o nich nic netvrdí a
běh nic neporušuje. Dopad je ale větší než u `INDEX.json`: slice je dokument, který Coder
čte jako pravdu.

### N4 — `c19` neplatí o node files v `_retired/`

`_check_identity` (`tools/intent/validate.py:53`) iteruje jen `tree.nodes`, takže hlášení o
neznámých polích retired uzly nikdy nepotká, přestože `parse_node` je do `unknown_fields`
poslušně dá. Ověřeno: retired soubor s `path` a `depth` má `unknown_fields: ['depth',
'path']`, ale `validate` vrátí jediný nález, `V7` o registru.

Pro Humana to není: poctivější směr je posílit vynucovač, tedy nechat `_check_identity`
projít i `tree.retired`.

## Použité modely

| Role | Model | Poznámka |
|---|---|---|
| Coordinator, Planner | `claude-opus-5-thinking-high` | rodičovské okno, volba Humana |
| Critic | `cursor-grok-4.5-high` | **substituce**, viz níže |
| Coder | `cursor-grok-4.5-high` | **substituce**, viz níže |
| Grader | žádný — stroj | |
| Adversary | `claude-opus-5-thinking-high` | jiná instance i model než Coder |

### Odchylka: substituce slugu

Katalog po obnově z 17. 8. 2026 dává na `high` Kritikovi i Coderovi `cursor-grok-4.6-high`.
Ten slug **není spustitelný** pro delegované role v tomto prostředí; dostupné jsou
`cursor-grok-4.5-high` a `cursor-grok-4.6-medium`. Použit `cursor-grok-4.5-high` jako
nejbližší dostupný, aby záměr Humana dostat Grok na `high` zůstal zachován.

Tvrdé omezení `adversary_differs_from_coder` splněno. Ověření dostupných slugů a srovnání
katalogu patří do metodického běhu.

Vedlejší pozorování: `AGENT_MODELS.explanation.md` sám píše, že do katalogu jdou jen slugy,
které Coordinator umí předat subagentovi, „jinak by řádek v YAML byl přání, ne spustitelná
politika". Tento běh ukázal, že to pravidlo zatím nic nekontroluje.

## Vrstva realizace

`i0004` byl po změně kontraktů `stale`. Coder žádné tvrzení nezapsal — ověřeno tím, že
`_realization.yaml` po jeho práci nebyl v `git status`. Tvrzení zapisuje Coordinator až po
zelené bráně a po `APPROVE`, podepsané rolí Coordinator.

## Navazující práce

| # | Co | Druh |
|---|---|---|
| 1 | `c6` — přeformulovat, nebo rozdělit (N1) | rozhodnutí Humana, pak běh |
| 2 | Metodika: znovuotevřená brána nenuluje počítadlo | běh o metodice |
| 3 | Metodika: model rodičovského okna do `00-model-policy.mdc` | běh o metodice |
| 4 | Metodika: kritérium pro sdílený běh změny záměru a implementace | běh o metodice |
| 5 | Ověřit dostupné slugy a srovnat katalog; případně to nechat kontrolovat strojem | běh o metodice |
| 6 | Vynucovač `c7` i na `reverse_code_map` (N2) | běžný běh |
| 7 | `_check_identity` i nad `tree.retired` (N4) | běžný běh |
| 8 | Rozhodnout, zda `render_slice` a `owner` mají kontrakt (N3) | běžný běh |
| 9 | `scope --base <commit>`, aby brána měřila od pojmenované základny | běžný běh |
