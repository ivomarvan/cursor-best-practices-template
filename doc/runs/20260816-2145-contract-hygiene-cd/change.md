---
run_id: 20260816-2145-contract-hygiene-cd
intent_ids: ["i0004"]
role: Planner
model: claude-opus-5-thinking-high
complexity: high
status: in-progress
---

# Změna záměru

## Nejvyšší uzel, kterého se změna dotýká

`i0004 — Intent tooling`. Mění se jeho kontrakty a jeden odstavec výkladu. Rodič `i0001`
ani sourozenci se nemění a `i0004` nemá potomky.

## Autorizace zúžení textu

Přeformulování kontraktu je při přísném čtení spouštěč „weakening a contract", vyhrazený
Humanovi. Autorizace existuje: Human ji vyslovil při uzavírání běhu
`20260816-1302-realization-layer-91`, zapsaná je v jeho `status.md` jako rozhodnutí 5 ze 6.
Složitost je `high`; Coordinator smí zvyšovat, snižovat jen Human.

## Co říká validátor, a proti čemu se tedy měří

`tools/intent/validate.py::_check_code_paths` ohlásí `V6`, když se `code_paths` dvou uzlů
překrývají a **ani jeden z nich není předkem druhého**. Zákaz tedy neplatí pro sourozence,
ale pro každou dvojici mimo linii předků — sourozence, bratrance, uzly z různých větví.

Tohle je jádro první revize této delty. Původní verze zužovala `c4` na sourozence a tvrdila
u toho, že se množina závazků nezmenšuje. Kritik ukázal, že to je nepravda: případ
bratranců by po změně netvrdil nikdo, přestože ho nástroj vynucuje. V běhu, jehož tématem
jsou tvrzení sahající dál než jejich důkaz, to byla tatáž vada o patro výš.

## Změněné a nové kontrakty

| Id | Text po změně | Vynucovač |
|----|---------------|-----------|
| `c4` | „`code_paths` of two different nodes may not overlap unless one is an ancestor of the other" | `test_validate.py::test_overlap_outside_the_ancestor_chain_is_rejected` |
| `c18` | „`code_paths` of a node and any of its ancestors may overlap" | `test_validate.py::test_the_ancestor_chain_may_overlap` |
| `c7` | „Path and depth are derived into the generated views" | `test_tools.py::test_index_holds_derived_path_and_depth` (beze změny) |
| `c19` | „A path or depth written into a node file is reported as an unknown field" | `test_validate.py::test_derived_fields_in_a_node_file_are_reported` |
| `c20` | „A path written into a node file never becomes the node's path in a generated view" | `test_tools.py::test_a_path_in_a_node_file_does_not_reach_the_index` |

Id `c18`–`c20` navazují za `c17`. Existující id se nepřečíslovávají: id je jméno, ne
pořadí, a odkazuje na ně historie běhů.

### Proč se dva testy přejmenovávají

`c4` po opravě mluví o linii předků, ne o sourozencích, takže jeho důkaz musí pokrýt i
bratrance. Dnešní `test_siblings_may_not_overlap` pokrývá jen sourozence a jeho jméno by po
rozšíření lhalo. Totéž na kladné straně: `c18` mluví o **libovolném** předkovi, dnešní
`test_parent_and_child_may_overlap` prokazuje jen vzdálenost jedna.

Oba testy se tedy rozšíří tak, aby každý ve svém těle prokázal celou větu svého kontraktu,
a přejmenují se podle toho, co po rozšíření dělají. Alternativa — nechat jména a zúžit
texty na „sourozenci" a „rodič s dítětem" — by závazek o bratrancích a o vzdálenějších
předcích nechala nevyslovený, což je právě to, co běh napravuje.

### Proč se `c7` rozpadá na tři, ne na dvě

Původní `c7` říkalo „path a depth existují jen v generovaných pohledech, **nikdy** v souboru
uzlu". To nejsou dvě tvrzení, ale tři, a každé se dá rozbít samostatně:

1. generované pohledy je nesou — `c7`, dnešní test stačí;
2. zápis do souboru uzlu se ohlásí — `c19`;
3. zapsaná hodnota se nedostane do generovaného pohledu — `c20`.

Bod 3 by bez vlastního kontraktu zůstal nedokázaný. Test u `c7` staví uzly, které `path` ve
front matteru nemají, takže by prošel i tehdy, kdyby generátor zapsanou hodnotu upřednostnil.
Vypustit bod 3 by tedy bylo tiché oslabení — přesně to, co Kritik zachytil u `c4`.

### Znění `c19` odpovídá skutečnosti, ne přání

Ověřeno ve zdroji. `path` ani `depth` nejsou v `KNOWN_FIELDS` (`tools/intent/model.py`),
takže skončí v `unknown_fields` a `validate.py` na ně vydá **varování** `V1`, nikoli chybu.

Kontrakt proto říká „is reported as an unknown field" a **neuvádí úroveň nálezu**. Kdyby
řekl „warning", zakotvil by dnešní volbu úrovně jako závazek a budoucí zpřísnění na chybu
by kontrakt porušilo, přestože by šlo o zlepšení. Test to musí respektovat: doloží, že
nález `V1` existuje a jmenuje obě pole, ale úroveň netvrdí.

Chování validátoru se **nemění**. Udělat z varování chybu je obhajitelné, ale je to
rozhodnutí o nástroji, ne úklid kontraktů, a smísit obojí v jednom běhu je ta samá záměna,
kterou tento běh napravuje.

## Změna výkladu v `## Contracts`

Mění se **dva** odstavce, ne jeden. Kritik našel, že první odstavec sekce dosud shrnuje
staré, sourozenecké znění, takže by uzel po změně tvrdil ve front matteru obecné pravidlo a
v próze jeho zúženou variantu. Nesedí ale ani počet: „Two of them encode decisions" mluví o
dvou kontraktech, zatímco po změně ta dvě rozhodnutí nese pět. Celý odstavec proto zní:

> The contracts describe behaviour a future change could plausibly break, not the shape of
> the code. Two decisions in there cost real thought and take five contracts between them:
> overlapping `code_paths` are legal along the ancestor chain and nowhere else, and derived
> data such as path and depth is generated rather than stored, so inserting a level of
> abstraction does not rewrite an entire subtree.


Předchozí běh zapsal do uzlu pravidlo, aby se táž vada neobjevila potřetí, ale zapsal ho
podle tvaru věty („středník nebo *but never*"). Kritik při jeho aplikaci ukázal, že tvar
věty nerozhoduje: `c6` má v jedné větě tři půlky a je v pořádku, protože je prokazuje jedno
tělo testu. Kritérium se proto přeformuluje na dosah testu a doplní se, odkud smí plynout
výjimka pro logický důsledek — jinak by se jí dal protlačit jakýkoli vágní dovětek.

Nahrazuje se odstavec začínající „Each contract states exactly one thing" tímto:

> A contract may claim only what its `enforced_by` proves. What decides is not the shape of
> the sentence but the reach of the test: where a sentence has two halves, one and the same
> test must prove both, or the halves belong to two contracts. A half that follows directly
> from the other, using only the terms the contract itself names, is not a second claim and
> is not split. `c14` is that case and the tightest one here: "cannot trip its own gate"
> follows from "always allows", because the gate in question is the run's own write.

`c14` tou výjimkou projde, ale odvození nese jiné slovo, než tvrdila první verze tohoto
odstavce. Nenese ho *guard*, nýbrž **always allows** ve spojení s referentem *its own
gate*: když brána vždy povolí zápis vrstvy, nemůže ji shodit právě ten zápis, kterým běh
končí. Nic mimo pojmy kontraktu k tomu potřeba není.

Kritik zároveň upozornil, že `c14` je v uzlu nejtěsnější případ té výjimky, takže jako
příklad kalibruje na hranu. Zůstává tam právě proto: příklad z prostředka pásma by
nikomu neřekl, kde pásmo končí. Odvození se v uzlu vysloví vsuvkou, aby čtenář nemusel
hádat, které slovo je nosné.

## Dodatek po recenzi Adversáře — NEPROVEDENO, přeneseno do navazujícího běhu

> **Tento dodatek se v tomto běhu neimplementoval.** Human běh po recenzi zastavil a nález
> poslal do vlastního běhu; podrobnosti a rozhodnutí jsou ve `status.md`. Uzel proto stále
> obsahuje znění `c7` z tabulky výše, ne to z tabulky pod tímto odstavcem. Zúžení `c7` má
> schválení Humana, chybí mu provedení a důkaz.

Adversář doložil mutací, že `c7` i `c20` mluví o generovaných pohledech v množném čísle,
zatímco jejich testy sahají jen na jeden z nich. Pohledy jsou dva a každý si cestu počítá
vlastním voláním `tree.path_of`: `build_index` do `INDEX.json` a `render_map` do `MAP.md`.
Podvrženou cestu propustil do `MAP.md`, aniž by kterýkoli test zčervenal.

Je to tatáž vada, kterou běh uklízí, jen přestěhovaná o patro dál. Delta se proto opravuje:

| Id | Text po dodatku | Vynucovač |
|----|-----------------|-----------|
| `c7` | „The generated index carries a path and a depth derived from the parent chain" | beze změny |
| `c20` | beze změny | tělo testu se rozšíří i na `render_map` |

Obě strany se řeší **opačně**, a ten rozdíl je věcný, ne libovolný.

`c7` se zužuje na index, protože množné číslo je u něj rovnou nepravdivé: `MAP.md` sloupec
`depth` vůbec nemá, takže větu „path a depth jsou v generovaných pohledech" nelze o tom
druhém pohledu tvrdit ani po sebelepším testu. Text se srovnává s tím, co jeho test
prokazuje, a jméno testu to říká rovnou.

`c20` se naopak **nezužuje** a rozšiřuje se jeho důkaz. Zúžit na index by znamenalo
odepsat závazek u `MAP.md` — a to je pohled, který agenti čtou jako směrovací mapu, takže
tam podvržená cesta škodí víc než v indexu. Přizpůsobit text slabému testu je přesně ten
tah, kvůli kterému tenhle běh existuje.

## Dotčené hrany

Žádná. `parent`, `uses`, `talks_to`, `code_paths` ani `test_paths` se nemění.

## Rozsah zastarání, který změna způsobí

Nenulový, a je to záměr. `i0004` je od předchozího běhu `realized`; změna kontraktů hne
otiskem `contracts`, takže tvrzení spadne do `stale` s důvodem „own contracts changed" a
bude potřebovat nový důkaz z tohoto běhu. Nikoho dalšího to nezasáhne: `i0004` nemá potomky
a žádný uzel ho neuvádí v `uses`. Ověří se strojově, ne odhadem.
