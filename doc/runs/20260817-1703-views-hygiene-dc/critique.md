---
run_id: 20260817-1703-views-hygiene-dc
intent_ids: ["i0004"]
role: Critic
model: cursor-grok-4.5-high
complexity: high
status: done
---

# Kritika změny záměru a plánu

## Verdikt
ACCEPT

## Zjištění ke změně záměru

### Asymetrie `c7` / `c20` — obě poloviny faktického tvrzení sedí

Ověřeno ve zdroji, ne převzato z plánu:

- `render_map` (`tools/intent/generate.py:30-38`) vypisuje hlavičku
  `| Id | Path | Title | Contracts | Code |` a do řádku dává
  `` `/".join(tree.path_of(node.id))` ``. Sloupec `depth` **neexistuje** — ani v
  hlavičce, ani v datech. Stejná hlavička je v aktuálním `doc/intent/MAP.md`.
- `build_index` (`generate.py:65-73`) ukládá **oba** klíče `"path"` a `"depth"`.
- Obě funkce volají `tree.path_of` **samostatně** (v `generate.py` dvě výskyty) —
  mutace mířená jen na jednu stranu je tedy možná, jak Adversář naměřil.

Zúžení `c7` na „The generated index carries a path and a depth derived from the
parent chain" je tedy srovnání textu s realitou: množné „views" + „path **and**
depth" je o `MAP.md` u poloviny věty **nepravdivé**, ne jen nedokázané. Žádný test
by větu o `depth` v mapě pravdivou neudělal. Autorizace Humana (status předchozího
běhu, rozhodnutí 2) je na místě.

`c20` naopak mluví jen o cestě. `MAP.md` cestu nese, závazek je o mapě pravdivý a
porušitelný — zúžit text na index by odepsalo právě ten pohled, který Adversář
prolomil. Rozšíření důkazů je správný směr.

### Pravidlo „zúžit nepravdu / rozšířit nedokázané" — útok a obhajoba

**Útok.** Bez dalšího omezení by tohle bylo povolení zužovat vždy, když je psaní
testu nepohodlné: stačí prohlásit tvrzení za „nepravdivé vůči dnešnímu kódu" a
text se přizpůsobí slabšímu stavu. To by obracelo směr ICE — záměr má řídit kód,
ne naopak.

**Obhajoba tady.** Pravidlo drží tři brzdy, a všechny tři jsou v této deltě
splněné:

1. Nepravdivost se měří proti **obsahu pohledu** (má/nemá sloupec), ne proti
   obtížnosti testu. `depth` v `MAP.md` chybí jako fakt výstupu.
2. Zúžení je oslabení → **Human** ho schválil výslovně; agent si ho nemůže
   odůvodnit sám.
3. Kde je tvrzení pravdivé (`c20` + cesta v mapě), plán **zakazuje** zúžení a
   nutí rozšířit důkaz — přesně opačný tah než „přizpůsobit text slabému testu",
   kvůli kterému oba běhy vznikly.

Kritérium v `## Contracts` uzlu („kontrakt smí tvrdit jen to, co `enforced_by`
prokazuje") se tím neohýbá: splnit se dá dvěma směry, ale volba směru je vázaná
na pravdivost, ne na pohodlí. Tady nejde o licenci k libovolnému zužování.

### Chybějící pozitivní závazek „`MAP.md` nese cestu"

Po zúžení `c7` **žádný kontrakt výslovně netvrdí**, že mapa nese odvozenou cestu.
Plán to vědomě nedělá (`plan.md` „Co plán vědomě nedělá").

To **není** mávnutí rukou přes mezeru nálezu Adversáře. Nález B1/`c20` se uzavírá
rozšířením důkazu; B2/`c7` se uzavírá zúžením textu (Human). Pozitivní „mapa má
cestu" by byl **nový** závazek — dnes ho nikdo nedrží a chování `render_map` se
nemění.

Rozšířený test `c20` přesto musí asertovat odvozenou cestu **na řádku uzlu**
(plán to vyžaduje). Tím se přítomnost odvozené cesty v mapě de facto hlídá jako
předpoklad negativního tvrzení, ne jako samostatný kontrakt. To je skromnost, ne
díra, kterou by šlo dnes prolomit stejnou mutací jako B1. Samostatný pozitivní
kontrakt na cestu v `MAP.md` by byl vítaný později; vynucovat ho v tomto běhu by
bylo rozšiřování rozsahu.

### Jeden test pro `c20`, ne dva pod jedním jménem

Kritérium uzlu: kde má věta dvě poloviny, **jeden** test musí dokázat obě, jinak
patří půlkám dva kontrakty.

Text `c20` je **jedno** univerzální tvrzení („nikdy … v generovaném pohledu")
kvantifikované přes pohledy, ne dvě různá tvrzení. Dvě instance (index + mapa)
v jednom těle jsou proto správné čtení kritéria — ne „dva testy sdílející jméno".
Dvojice testů, z nichž každý zná jen jeden pohled, by naopak větu neprokázala
(přesně to, co Adversář ukázal). Dělit `c20` není důvod.

### Mutace

| Mutace | Co má padnout | Proč jen ta polovina |
|---|---|---|
| `path` z front matteru + přednost v `build_index` | aserce o indexu | `render_map` dál volá `path_of` |
| totéž + přednost v `render_map` | aserce o mapě | `build_index` dál volá `path_of` |

Druhou naměřil Adversář (sada zelená). Pořadí asercí v těle musí být **index
pak mapa**, aby u mutace 1 padla viditelně indexová polovina a u mutace 2 prošla
indexová a padla mapová. Plán to říká dostatečně („padne polovina o …"); Coder
to nesmí sloučit do jediné neoddělitelné kontroly.

Pro `c7` se mutace nepíše — vynucovač se nemění, evidence je v předchozím
`grader.md`. Souhlas.

## Zjištění k plánu (Definition of Ready)

| Položka | Verdikt |
|---|---|
| Měřitelný cíl | Ano — každý kontrakt o pohledu je pravdivý o každém pohledu, o kterém mluví, a doložený; `i0004` realizovaný |
| Konkrétní výstupy | Ano — uzel, `test_tools.py`, převzatý `test_validate.py` |
| Slice z `intent slice` | Ano — `slice.md` existuje, čte `i0001`+`i0004` |
| Pojmenovaný vynucovač u dotčených kontraktů | Ano — `c7` beze změny symbolu; `c20` přejmenovaný rozšířený test |
| Test spec (happy / edge / error) | Ano v obsahu: odvozená cesta; kontrola na řádku uzlu (ne podřetězec celého `MAP.md`); injekce `nonsense/place`. Forma není označená štítky, ale DoR splňuje |
| DoD → artefakt/příkaz | Ano — validate, realization, sada, ruff, scope, mutace v `grader.md`, claim Coordinatorem |
| Incidental | Ano — `MAP.md`, `INDEX.json`, `_realization.yaml` |
| Blokující open questions | Ne — `open_questions: []` |
| Izolovaně implementovatelné | Ano — bez změny `generate.py` / `model.py` |

### Deklarace nezměněného `test_validate.py`

Plán ho dává do `outputs` s poznámkou „beze změny v tomto běhu", protože nese
nezacommitovanou práci zastaveného běhu a `scope` čte pracovní strom.

**To není díra v bráně.** Zadání výslovně říká, že tento běh práci **přebírá**;
bez deklarace by scope ohlásil cizí diff. `outputs` tu znamená „co běh dodá v
commitu", ne nutně „co Coder v tomto kole edituje". Alternativy (revert
předchozí práce, nebo tiše nechat nedeklarované) by byly horší. Poctivé převzetí,
ne obcházení.

Podmínka: Coder soubor opravdu **needituje** dál; jakákoli nová úprava by už
nebyla „převzetí", ale skrytý scope creep.

## Axiomy A1–A6

Žádný nový uzel, přesun ani změna `parent`/`uses`. A1–A3 a A5 se strukturou
stromu netýká — zůstávají.

- **A4** — zužování vlastního kontraktu je oslabení, ne posílení vůči rodiči.
  A4 reguluje vztah dítě↔rodič; `i0004` nemá potomky. Oslabení schválil Human.
  A4 neporušeno.
- **A6** — běh nezakládá nový uzel ani nový pozitivní kontrakt na cestu v mapě;
  drží se uzavření nálezu. Šetrné.

Po změně sedí kritérium v `## Contracts`: `c7` tvrdí jen index (test sahá na
index); `c20` tvrdí o generovaném pohledu obecně (jeden test, obě instance).

## Co jsem ověřil sám

| Úkon | Výsledek |
|---|---|
| Čtení `render_map` / `build_index` v `generate.py` | MAP: Path ano, depth ne; INDEX: path+depth; 2× `tree.path_of` |
| Čtení `doc/intent/MAP.md` | Hlavička `Id \| Path \| Title \| Contracts \| Code`; 5 sloupců; žádný Depth |
| `PYTHONPATH=tools python3` + `build_index(load_tree)` | Všechny uzly mají `path` i `depth` (např. `i0004` depth=1) |
| `python3 tools/intent/cli.py validate` | `5 node(s): 0 error(s), 0 warning(s)`, exit 0 |
| Stávající vynucovače `c7`/`c20` (unittest) | Oba OK; `c20` sahá jen na `build_index` — stav před tímto během, očekávaný |
| `git status` / diff | `i0004`, `test_tools.py`, `test_validate.py`, MAP, INDEX změněné; `test_validate.py` nese práci předchozího běhu |
| `status.md` / `review.md` předchozího běhu | Human schválil zúžení `c7`; `c20` zužovat nemá; B1/B2 mutací doložené |
| Kritérium v `## Contracts` uzlu `i0004` | Jedno tělo pro obě instance univerzálního `c20`; ne důvod k dělení |

Žádný soubor kromě tohoto `critique.md` jsem nezměnil.
