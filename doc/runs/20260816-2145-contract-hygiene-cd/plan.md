---
run_id: 20260816-2145-contract-hygiene-cd
intent_ids: ["i0004"]
role: Planner
model: claude-opus-5-thinking-high
complexity: high
status: in-progress
outputs:
  - doc/intent/nodes/i0004-intent-tooling.md
  - tools/intent/tests/test_validate.py
  - tools/intent/tests/test_tools.py
incidental:
  - doc/intent/MAP.md
  - doc/intent/INDEX.json
  - doc/intent/_realization.yaml
---

# Plán

## Cíl

Žádný z kontraktů, kterých se tento běh dotýká — `c4`, `c7` a nově `c18`, `c19`, `c20` —
netvrdí víc, než dokazuje jeho `enforced_by`, a žádný z testů, které tento běh píše nebo
upravuje, nezůstane bez kontraktu, který se o něj opírá.

Měřitelně: každý z těch pěti kontraktů projde kritériem z `## Contracts` uzlu položku po
položce, a pro každý nový test existuje mutace, pod kterou padne.

**Cíl se vědomě netýká celé testovací sady.** První verze plánu slibovala, že v
`tools/intent/tests/` nezůstane test bez kontraktu. Kritik to strojově změřil: 68 z 85 testů
žádný kontrakt necituje, takže slib byl nesplnitelný. Většina testů jsou testy, ne důkazy
kontraktů, a nutit každému z nich kontrakt by strom nafouklo bez užitku. Který kód je
nekrytý kontraktem, je otázka pro `intent coverage`, ne pro tento běh.

Konkrétně `test_reverse_lookup_prefers_the_deepest_node` — nejbližší soused nálezu — zůstává
**vědomě mimo rozsah**. Popisuje chování příkazu `owner`, ne tvrzení, které by tento běh
uklízel. Rozhodnutí je zapsané, ne přehlédnuté.

## Výstupy

`doc/intent/nodes/i0004-intent-tooling.md` — přeformulování `c4` a `c7`, přidání `c18`,
`c19`, `c20`, a v `## Contracts` úprava **dvou** odstavců: shrnutí na začátku sekce, které
dosud cituje staré sourozenecké znění, a odstavec s kritériem.

`tools/intent/tests/test_validate.py` — rozšíření a přejmenování dvou existujících testů,
jeden nový test.

`tools/intent/tests/test_tools.py` — jeden nový test.

Nic jiného. Zejména se nemění `tools/intent/validate.py`, `model.py` ani `generate.py`: běh
popisuje chování, nemění ho.

## Testovací specifikace

Každý test musí ve **svém vlastním těle** prokázat celou větu svého kontraktu; test, který
prokazuje půlku, je důvod kontrakt rozdělit, ne důvod tvrdit víc.

| Kontrakt | Test | Co musí tělo prokázat |
|---|---|---|
| `c4` | `test_validate.py::test_overlap_outside_the_ancestor_chain_is_rejected` (z `test_siblings_may_not_overlap`) | `V6` u dvojice sourozenců **a** u dvojice bratranců (děti dvou různých rodičů); kontrakt mluví o dvou **různých** uzlech, protože překryv dvou `code_paths` téhož uzlu `_check_code_paths` přeskakuje |
| `c18` | `test_validate.py::test_the_ancestor_chain_may_overlap` (z `test_parent_and_child_may_overlap`) | žádné `V6` u dvojice rodič–dítě **a** u dvojice prarodič–vnuk |
| `c19` | `test_validate.py::test_derived_fields_in_a_node_file_are_reported` | nález `V1`, jehož zpráva jmenuje `path` i `depth`, u uzlu, který ta pole má ve front matteru; **úroveň nálezu se netvrdí**; uzel bez těch polí takový nález nevydá |
| `c20` | `test_tools.py::test_a_path_in_a_node_file_does_not_reach_the_index` | uzel s `path: "nonsense/place"` ve front matteru má v `build_index` cestu spočtenou z řetězce předků, ne tu zapsanou |

`TreeBuilder.add` přes `front.update(fields)` propíše libovolné pole do front matteru, takže
`self.builder.add("engine", parent=root, path="nonsense/place", depth=99)` je legální a
pomocník se nemusí měnit.

## Failing-test evidence — jedna mutace na každé tvrzení

Toto je druhá věc, kterou Kritik u první verze plánu zamítl: navržená jediná mutace
prokazovala jen půlku `c19`. Kritik ji spustil a doložil, že po přidání `path`/`depth` do
`KNOWN_FIELDS` varování zmizí, ale index dál vrací správnou cestu — takže půlka o ignorování
projde i na zmutovaném kódu. Každé tvrzení proto potřebuje vlastní mutaci:

| Test | Mutace | Očekávaný pád |
|---|---|---|
| `test_overlap_outside_the_ancestor_chain_is_rejected` | ve `_check_code_paths` hlásit `V6` jen u dvojic se **společným rodičem** | případ bratranců přestane hlásit `V6` |
| `test_the_ancestor_chain_may_overlap` | v `_is_ancestor` porovnávat jen přímého rodiče | prarodič–vnuk začne hlásit `V6` |
| `test_derived_fields_in_a_node_file_are_reported` | přidat `"path"` a `"depth"` do `KNOWN_FIELDS` | nález `V1` zmizí |
| `test_a_path_in_a_node_file_does_not_reach_the_index` | přidat `path` jako pole `Node` plněné z front matteru a v `build_index` ho upřednostnit před spočtenou cestou | index vrátí `nonsense/place` |

První a čtvrtá mutace jsou po kritice opravené a rozdíl není kosmetický. První verze u `c4`
navrhovala „přeskočit dvojice se společným rodičem" — to jsou ale **sourozenci**, tedy půlka,
kterou test uměl už dřív; Kritik naměřil, že bratranci pod ní procházejí a celá dnešní sada
zůstává zelená. Mutace musí shazovat tu půlku, která je na testu nová, jinak nedokazuje nic
o rozšíření.

Čtvrtá mutace byla o bod větší, než musí být, a ten bod navíc (`KNOWN_FIELDS`) shazoval
zároveň test `c19` — mutace shazující dva testy nedokazuje ani jeden. `KNOWN_FIELDS` s
`build_index` nesouvisí; dvoubodová varianta shodí právě jeden test, což Kritik naměřil.

Že je `c20` závazek a ne opis chování, plyne z toho, že implementace, která ho poruší, je
reálně napsatelná ve dvou řádcích.

Každá mutace se po zachycení výstupu vrací a sada musí být zelená.

### Pátá mutace, doplněná po recenzi Adversáře — NEPROVEDENA

> **Tato mutace ani rozšíření testu se v tomto běhu neprovedly.** Human běh po recenzi
> zastavil, viz `status.md`. Test se stále jmenuje
> `test_a_path_in_a_node_file_does_not_reach_the_index` a sahá jen na `INDEX.json`.


`c20` mluví o generovaném pohledu obecně, ale pohledy jsou dva a každý si cestu počítá sám.
Adversář doložil, že dvoubodová mutace mířená na `render_map` propustí `nonsense/place` do
`MAP.md`, zatímco celá sada zůstane zelená. Tělo testu se proto rozšiřuje i na `MAP.md` a
přibývá řádek:

| Test | Mutace | Očekávaný pád |
|---|---|---|
| `test_a_path_in_a_node_file_does_not_reach_the_index` | pole `Node` z front matteru + přednost v `render_map` | `MAP.md` obsahuje `nonsense/place` |

Jméno testu po rozšíření podhodnocuje, co dělá, takže se mění na
`test_a_path_in_a_node_file_does_not_reach_a_generated_view`, a `enforced_by` u `c20` s ním.

## Definition of Done

- [ ] `c4` a `c18` pokrývají dohromady celé pravidlo, které `_check_code_paths` vynucuje
- [ ] `c7`, `c19` a `c20` pokrývají dohromady celý původní výrok `c7`
- [ ] `c7` mluví o generovaném indexu, ne o pohledech v množném čísle, a `c20` je doložené
      na obou pohledech — `INDEX.json` i `MAP.md` — **NESPLNĚNO, přeneseno, viz `status.md`**
- [ ] Každý z pěti kontraktů má `enforced_by` na existující symbol, jehož tělo prokazuje
      celou jeho větu
- [ ] Shrnující odstavec na začátku `## Contracts` nahrazen zněním z `change.md` — obecné
      pravidlo místo sourozeneckého a správný počet kontraktů
- [ ] Odstavec o kritériu v `## Contracts` nahrazen zněním z `change.md`, včetně vsuvky,
      která u `c14` vyslovuje, ze kterých slov odvození plyne
- [ ] Čtyři mutace zaznamenané v `grader.md`, každá s pádem a s návratem do zelené
- [ ] `intent validate` končí 0 a generované soubory jsou aktuální
- [ ] Celá sada `tools/intent/tests` je zelená
- [ ] `template_checks` a `hook_checks` končí 0
- [ ] `ruff check` a `ruff format --check` nad `tools/` jsou čisté
- [ ] Kontrola rozsahu končí 0 **bez** `--node`

## Poznámka ke kontrole rozsahu

Předchozí běh ji spouštěl s `--node i0004`, což podle `scope.py` automaticky povolí celé
`code_paths` uzlu, tedy `tools/`. U uzlu vlastnícího široký adresář je tím brána hrubá.
Tento běh ji spouští **bez** `--node`: povolené je jen deklarované, adresář běhu a vrstva
realizace. Pracovní strom je po dvou commitech čistý, takže brána poprvé měří proti
smysluplné základně.

## Co plán vědomě nedělá

- Nemění validátor. Varování `V1` zůstává varováním a `c19` proto úroveň netvrdí.
- Nedotýká se `c1`, `c2`, `c3`, `c5`, `c6` ani `c8`–`c17`.
- Nepřečíslovává existující id.
- Nepřidává kontrakty k testům mimo rozsah, včetně jmenovaného
  `test_reverse_lookup_prefers_the_deepest_node`.
