---
run_id: 20260817-1853-slice-and-derived-truth-66
intent_ids: ["i0004"]
role: Planner
model: claude-opus-5-thinking-high
complexity: high
status: in-progress
---

# Změna záměru

## Nejvyšší uzel, kterého se změna dotýká

`i0004 — Intent tooling`. Mění se text **jednoho** kontraktu (`c6`), vynucovač jednoho
kontraktu (`c6`), dosah těla testu u dalších dvou (`c7`, `c19`) a přidává se jeden odstavec
do sekce `## Contracts`. Rodič `i0001` se nemění, `i0004` nemá potomky a žádný uzel ho
neuvádí v `uses` ani `talks_to` (ověřeno `grep -n "i0004" doc/intent/nodes/*.md`).

## Přehled: tři nálezy, jedna změna textu

| Nález | Co je vadné | Směr opravy | Mění se text kontraktu? |
|---|---|---|---|
| F1 `c6` | věta je **nepravdivá** — sada sama dokazuje opak | přeformulovat text, přepsat vynucovač | **ano** |
| F2 `c7` | věta je pravdivá, ale vynucovač sahá na jedno ze dvou míst | rozšířit tělo testu | ne |
| F3 `c19` | věta je pravdivá jen o `nodes/`, ne o `_retired/` | posílit nástroj, aby věta platila i tam | ne |

Nová id kontraktů se **nealokují**; posloupnost zůstává na `c20`. Zdůvodnění u F1 níž;
u F2 a F3 je to přímý důsledek toho, že se nemění žádná věta, jen její důkaz.

## Autorizace zúžení `c6`

Přeformulování `c6` je při přísném čtení oslabení kontraktu, tedy věc Humana. Autorizace
existuje a je zapsaná: nález je veden jako `N1` ve `status.md` běhu
`20260817-1703-views-hygiene-dc` s poznámkou „rozhodnutí Humana", Adversář ho tam doložil
spuštěním, a Human ho do tohoto běhu poslal s pokynem přeformulovat `c6` tak, aby říkal, co
je pravda. Nic jiného v tomto běhu netvrdí méně než dnes.

## F1 — `c6`: jeden kontrakt, ne dva

### Co dnes `build_slice` skutečně dělá

Ověřeno spuštěním, ne čtením (`tools/intent/slicing.py:63-95`). Do `result.files` se
dostanou právě uzly z množiny: cílový uzel, celý řetězec předků, cíle jeho `uses` a
**oba směry** hrany `talks_to` — vlastní i příchozí (`slicing.py:70-71`, `:80-84`).
Mimo množinu zůstane sourozenec bez hrany, uzel, který cílový uzel uvádí v **svém**
`uses` (hrana obráceným směrem se nesbírá) a potomek cílového uzlu.

Naměřeno na dočasném stromu s osmi uzly:

```
files ids: ['i0001', 'i0002', 'i0003', 'i0004', 'i0005']
expected:  ['i0001', 'i0002', 'i0003', 'i0004', 'i0005']   (root, uses target, talks_to target, node, talks_to caller)
equal: True                                                 (sibling, uses consumer, child chybí)
```

### Starý a nový text

Staré znění, které je nepravdivé:

```yaml
  - id: c6
    text: "A slice carries ancestors and semantic dependencies but never siblings"
    enforced_by: "tools/intent/tests/test_tools.py::test_slice_contains_ancestors_and_uses_but_not_siblings"
```

Nové znění:

```yaml
  - id: c6
    text: "A slice carries exactly these intent nodes: the node, its ancestors, its `uses` targets and the far end of every `talks_to` edge — kinship alone adds none"
    enforced_by: "tools/intent/tests/test_tools.py::test_slice_carries_exactly_ancestors_uses_and_talks_to_ends"
```

Tři věci ve znění jsou úmyslné a stojí za vysvětlení:

1. **„these intent nodes"** — referentem je seznam uzlů, ne celý dokument slice. `Slice`
   nese vedle uzlů i ADR (`_find_adrs`) a při `--for implement` vlastní kód a testy.
   Kdyby věta říkala jen „a slice carries exactly", byla by nepravdivá o ADR — tedy táž
   vada, jakou opravujeme.
2. **„the far end of every `talks_to` edge"** — pokrývá oba směry jedním slovem. „`talks_to`
   targets" by pokrylo jen vlastní hrany a příchozí polovina, kvůli které je `c6` dnes
   nepravdivé, by zůstala nevyslovená.
3. **Pomlčka, ne středník** — `_contract_summary` (`tools/intent/generate.py:16-20`) spojuje
   texty kontraktů do sloupce `MAP.md` právě středníkem. Středník uvnitř textu by řádek
   mapy udělal dvojznačným.

Znění projde omezenou podmnožinou YAML: `parse` → `dump` → `parse` je identita, dvojtečka
i backticky uvnitř uvozovek se přečtou správně (ověřeno).

### Proč jeden kontrakt, a ne dva

Pravidlo z `## Contracts` uzlu má dvě větve: buď „jeden a týž test prokáže obě půlky", nebo
„půlky patří dvěma kontraktům". `c6` prochází **první** větví, a to v nejsilnější možné
podobě: obě půlky prokazuje jedna a táž **aserce** — rovnost množin. Nesahá tedy po výjimce
pro odvozenou půlku, kterou v uzlu drží `c14`; kalibrační věta o `c14` proto zůstává
nedotčená.

Doloženo dvěma mutacemi, které jsou opačné a padají na tomtéž řádku testu:

- vypustit příchozí hranu ze seznamu souborů → aserce hlásí `Items in the second set but not the first: 'i0005'`;
- přidat do slice sourozence → aserce hlásí `Items in the first set but not the second: 'i0006' 'i0007'`.

Rozdělení na dva kontrakty by navíc vyrobilo dva téměř identické testy: vyčerpávající
polovinu („nic dalšího") nelze prokázat bez členů, kteří v množině být mají, takže záporný
test by musel postavit skoro tentýž strom jako kladný. Preferovat rozšíření existujícího
testu před téměř duplikátem je pokyn tohoto běhu; dvě id by ho porušila.

### Co se na tom zpřísnilo a co povolilo

Povolilo: sourozenec **s** deklarovanou hranou ve slice být smí. To je ta schválená
korekce; dnešní univerzální „never siblings" je nepravda a jeho vlastní sada
(`test_slice_includes_incoming_talks_to`) ji vyvrací.

Zpřísnilo: členství je od teď **vyčerpávající**. Stará věta nemluvila o potomcích, o
bratrancích ani o hraně `uses` obráceným směrem; nová o nich mluví slovem „exactly" a test
je má ve fixtuře. Rozhodnutí, které tím vzniká a které nikdo dosud nevyslovil: **potomci
ve slice nejsou**. Je to dnešní chování a věříme, že správné (uzel se nevysvětluje svými
rozpracováními), ale od teď je to závazek — kdo bude chtít nést do slice děti, projde
změnou záměru, ne refaktorem. V uzlu je to napsané, aby se to za rok nedalo přehlédnout.

## F2 — `c7`: text zůstává, mění se dosah důkazu

`c7` říká „The generated index carries a path and a depth derived from the parent chain".
Ta věta je pravdivá a **není potřeba ji měnit**: `build_index` odvozuje `depth` na dvou
místech a obě jsou součástí generovaného indexu — `nodes[*].depth` (`generate.py:73`) a
`reverse_code_map[*].depth` (`generate.py:92`). Krátký je důkaz, ne věta:
`test_index_holds_derived_path_and_depth` sahá jen na první z nich, takže mutace druhého
projde zeleně (naměřeno Adversářem v běhu 1703 i mnou).

Oprava je tedy **zpřísnění vynucovače**, ne zúžení textu. Zúžit `c7` na `nodes[*]` by bylo
oslabení, na které tento běh autorizaci nemá a nepotřebuje ji — rozšířit tělo testu je
levnější a poctivější.

Vědomě **nekontraktované** zůstává, že řazení reverzní mapy dává vyhrát nejhlubšímu
vlastníkovi (`generate.py:94`). Věta `c7` mluví o nesené hodnotě, ne o pořadí, a vlastní
reverzní vyhledávání nástroje si hloubku počítá samo (`coverage.py:86-97`), takže na řadě
řádků v `INDEX.json` nezávisí. Zda je pořadí závazkem vůči vnějším konzumentům indexu, je
otázka o veřejném tvaru `INDEX.json`, ne o tomto nálezu. Zapsáno, ne přehlédnuto.

## F3 — `c19`: posílit nástroj, nezužovat větu

`c19` říká „A path or depth written into a node file is reported as an unknown field".
`_check_identity` (`tools/intent/validate.py:52-74`) iteruje jen `tree.nodes`, takže soubor
v `_retired/` se na neznámá pole nikdy nepodívá, přestože `parse_node` je do
`unknown_fields` poslušně dá. Naměřeno: retired soubor s `path` a `depth` má
`unknown_fields: ['depth', 'path']`, a `validate` na něj nevydá **žádný** nález.

**Volba: rozšířit hlášení, ne zúžit větu.** Důvody, v tomto pořadí:

1. Zúžení věty na „current node file" je oslabení kontraktu, tedy rozhodnutí Humana. Tento
   běh má autorizaci na jedno oslabení (`c6`) a jen proto, že je dnešní věta nepravdivá.
   Věta `c19` nepravdivá není — je pravdivá o výřezu a nedokázaná mimo něj.
2. Retired soubor je pořád soubor uzlu a odvozená data v něm jsou tatáž chyba. Čte ho
   člověk, který se dívá do historie, a `path: nonsense/place` mu tam lže stejně.
3. Cena je šest řádků a nula nových nálezů na tomto stromu — `doc/intent/_retired/`
   neexistuje. Naměřeno s hotovou úpravou: `5 nodes; 0 errors; 0 warnings`, tedy přesně
   stav před změnou.

**Past je respektována.** Do `tree.retired` se pouští **jen** hlášení o neznámých polích,
nikoli celý `_check_identity`: retired uzel z definice padá na pravidlu „id is marked
retired in the registry but the node is active" a projít jím celou funkcí by vyrobilo chybu
u každého retired souboru. Naměřeno s hotovou úpravou na dočasném stromu s jedním retired
uzlem: dvě varování `V1` (jedno na current, jedno na retired uzlu) a **nula chyb**.

## Změna prózy v `## Contracts`

Existující tři odstavce sekce zůstávají **znak za znak** stejné; zejména se nemění odstavec
s pravidlem o dosahu testu ani kalibrace na `c14`. Před tento odstavec s pravidlem se
vkládá nový, protože `c6` se na pravidlo odvolává a musí být nad ním:

> `c6` describes a computation, not a family relation. Slice membership is a set built from
> the ancestor chain and from declared edges, and `talks_to` counts in both directions,
> because an operational partner is context whichever end declared the edge. Nothing in
> that computation looks at kinship, so "kinship alone adds none" is the exhaustive half of
> one set rather than a second claim: a single set comparison proves both halves, which is
> the first branch of the rule below and not the exception `c14` needs. Descendants are
> outside the set as well — carrying them would be a change of intent, not a refactor.

Odstavec vědomě neobsahuje historii („dřív tam stálo never siblings"). Uzel je záznam
platného významu; historie patří do `change.md` a do běhů.

První odstavec sekce se nemění: mluví o „five contracts between them" pro `c4`, `c18`, `c7`,
`c19`, `c20` a tento běh ten počet nemění — `c6` do té dvojice rozhodnutí nepatří.

K F2 ani F3 se do prózy nepíše nic. U obou se nemění věta, jen její důkaz, a „jak daleko
sahá tělo testu" není význam uzlu; kdyby se to psalo do prózy, uzel by zastarával při každém
rozšíření testu.

## Dotčené hrany

Žádná. `parent`, `uses`, `talks_to`, `code_paths` ani `test_paths` se nemění.

## Rozsah zastarání, který změna způsobí

**`i0004` tímto během zastará, a je to očekávané.** Mění se text i vynucovač `c6`, takže se
hne otisk `contracts`; přidaný odstavec v `## Contracts` hne otiskem `meaning`. Tvrzení z
běhu `20260817-1703-views-hygiene-dc` proto spadne do `stale` s důvody „own contracts
changed; own meaning changed". Nový důkaz vzniká v tomto běhu a **Coordinator uzel znovu
nárokuje až po zelené bráně Gradera** (`realization claim i0004 --evidence
doc/runs/20260817-1853-slice-and-derived-truth-66 --by Coordinator`).

Nikdo další zasažen není: `i0004` nemá potomky a žádný uzel ho neuvádí v `uses`, takže
propagace po hraně `uses` nemá kam jít. Tvrzení o `i0002` zůstává nedotčené. Ověří se
strojově příkazem `realization worklist`, ne odhadem.

## Jak jsem si nálezy ověřil

Vše na kopii v `/tmp/planner-probe` (`tools/` + `ruff.toml`), v repozitáři jsem nezměnil
nic než tento soubor a `plan.md`; kopie je po dopsání smazaná. Naměřeno: obsah slice pro
osmiuzlový strom, chování `validate` nad retired souborem před i po úpravě, `depth` v
`reverse_code_map`, průchod celé sady (82 testů) s navrženými testy a čtyři mutace z
`plan.md`, každá právě s jedním padajícím testem.
