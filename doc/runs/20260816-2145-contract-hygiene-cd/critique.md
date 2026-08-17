---
run_id: 20260816-2145-contract-hygiene-cd
intent_ids: ["i0004"]
role: Critic
model: claude-opus-5-thinking-high
complexity: high
status: done
---

# Kritika změny záměru a plánu (kolo 3 — poslední)

## Verdikt

**ACCEPT** — změna záměru i plán. Kód **neblokuji**, Coder může začít.

Obě opravené mutace jsem znovu naměřil a obě dělají přesně to, co plán slibuje: mutace pro
`c4` shodí právě půlku o bratrancích a nic jiného, mutace pro `c20` shodí právě jeden test.
Tím padl poslední věcný nález; failing-test evidence tohoto běhu je poprvé ověřená, ne
slíbená.

Zbývají tři textové nedodělky uvnitř editace uzlu. Zapisuji je jako **závazné podmínky**,
ne jako doporučení — jsou to věci, které si běh sám uložil a které se v diffu poznají na
první pohled. Nesplněná podmínka je pro Adversáře `REQUEST CHANGES`, ne věc vkusu.

| # | Podmínka | Jak se pozná v diffu |
|---|---|---|
| **P1** | Ve shrnutí `## Contracts` nesmí zůstat „**Two of them** encode decisions" — po změně nesou ta dvě rozhodnutí **pět** kontraktů | v uzlu nezůstane řetězec `Two of them` |
| **P2** | Odstavec s kritériem musí obsahovat odvození u `c14`, které `change.md` slibuje, ale jeho citovaný blok neobsahuje | v uzlu se u zmínky `c14` objeví *always allows* / *its own gate* |
| **P3** | Definition of Done musí mít položku i pro shrnující odstavec, ne jen pro odstavec s kritériem | v `plan.md` přibude jedna odrážka |

Proč je to ACCEPT, když jsem v kole 2 u téhož odstavce psal „blokuje kód": tehdy ten
odstavec nebyl v rozsahu vůbec, takže by běh skončil s uzlem, který si ve front matteru a v
próze odporuje, a nikdo by k němu neměl instrukci. Dnes je v rozsahu, edituje se táž věta a
zbývá dojít o tři slova dál. Zároveň v kole 2 byly na stole dvě vady důkazů, které by
vyrobily nepravdivý `grader.md` — ty už na stole nejsou. Eskalovat poslední kolo kvůli dvěma
větám, které nemění deltu, kontrakty, testy ani mutace, by bylo nepoměrné: eskalace se má
utratit za rozhodnutí, ne za korekturu.

Podmínky smí zapracovat Planner bez dalšího kola Kritika. Deltu v kole 3 neotevírám.

## Zjištění ke změně záměru

### Uzavření nálezů z kola 2

- **F1 (mutace mířila na špatnou půlku) — uzavřeno a přeměřeno.** Nové znění „hlásit `V6`
  jen u dvojic se **společným rodičem**" je přesně ta mutace, která u rozšířeného testu
  shodí novou půlku. Naměřeno v kole 3: padá `test_cousins_half`, `test_siblings_half`
  prochází, ostatních pět tvrzení prochází. Sada 80 dnešních testů pod ní zůstává zelená —
  bratranecká regrese je dnes skutečně nekrytá, takže rozšíření testu není kosmetika.
- **F2 (mutace o bod větší) — uzavřeno a přeměřeno.** Dvoubodová varianta (pole `Node`
  plněné z front matteru + přednost v `build_index`) shodí právě
  `test_a_path_in_a_node_file_does_not_reach_the_index` a nic dalšího; `c19` pod ní
  prochází. Věta v plánu „mutace shazující dva testy nedokazuje ani jeden" je správné
  zobecnění toho, co jsem naměřil, a stojí za to, že ji plán zapsal.
- **F3 (próza uzlu) — z větší části uzavřeno, zbytek je P1.** Náhrada „but not between
  siblings" → „and nowhere else" je správná: sedí na `c4` i `c18` dohromady a rozpor mezi
  front matterem a prózou mizí. Nedotčené zůstalo „**Two of them**", což byla druhá polovina
  téhož nálezu z kola 2. Po změně nesou ta dvě rozhodnutí `c4` + `c18` a `c7` + `c19` +
  `c20`, tedy pět kontraktů. Je to týž druh nepřesnosti, jakou předchozí běh opravoval
  („próza `c8`–`c14` proti skutečnému rozsahu `c8`–`c17`") a jakou si Kritik toho běhu
  započítal jako splněnou. Nechat ji tu podruhé by ten standard zrušilo.
- **`c4` „two different nodes" — přijato a zdůvodněno na správném místě.** Testová
  specifikace navíc říká proč (překryv dvou `code_paths` téhož uzlu `_check_code_paths`
  přeskakuje), takže příští čtenář nemusí ten roh objevovat znovu. Bez nálezu.

### P2 — slíbená vsuvka u `c14` v citovaném znění chybí

`change.md` říká: „Odvození se v uzlu vysloví vsuvkou, aby čtenář nemusel hádat, které slovo
je nosné." Citovaný blok, který se má do uzlu vložit, ale žádnou vsuvku neobsahuje, a
Definition of Done žádá odstavec „nahrazen zněním z `change.md`". Coder tedy vloží text bez
vsuvky a slib tiše zmizí — přičemž `change.md` bude nadále tvrdit, že tam je.

Není to formalita, protože právě na té vsuvce stojí moje odpověď na přímou otázku níže.
Oprava: doplnit vsuvku rovnou do citovaného bloku v `change.md` (preferuji — pak je DoD
splnitelná doslova), nebo slib z `change.md` vypustit. Znění je věc Plannera; pro
konkrétnost jedna možnost, jak to může vypadat:

> …— the second clause of `c14` is the case, and it follows from *always allows* together
> with what *its own gate* refers to — is not a second claim and is not split.

### Odpověď na otázku: nejtěsnější případ jako učebnicový příklad **ponechat**

Ustupuji, a ne ze zdvořilosti. Argument, že příklad z prostředka pásma neřekne, kde pásmo
končí, je lepší než moje doporučení z kola 2 — kritérium s výjimkou se v praxi láme na
hraně, ne uprostřed, a příklad, který na hranu neukazuje, kalibruje k falešnému bezpečí.

Platí to ale **jen s vsuvkou z P2**. Hraniční příklad bez vyslovené derivace učí, že hrana
je tam, kde si ji čtenář dohodne — což je přesně ta pružnost, kvůli které jsem výjimku
kritizoval v kole 1. S vsuvkou je `c14` dobrý příklad; bez ní je to nejlepší dostupný návod,
jak výjimku zneužít. Podmínka P2 a tohle ustoupení jsou jedno rozhodnutí, ne dvě.

Opravu odvození v `change.md` (nosné je „always allows" plus referent „its own gate", ne
slovo *guard*) jsem přečetl a je správná.

### Poznámka, kterou vědomě nezvedám na nález

Věta „legal along the ancestor chain **and nowhere else**" je při doslovném čtení nepřesná o
tentýž roh, kvůli kterému `c4` dostalo slovo „different": dva překrývající se `code_paths`
jednoho uzlu jsou legální a na linii předků nejsou. **Nedoporučuji to opravovat.** Ten
odstavec je shrnutí dvou rozhodnutí, ne kontrakt; přesnost tam patří v míře, která se čte,
a rohy patří do front matteru, kde už jsou. Zapisuji to jen proto, aby to za měsíc nikdo
neobjevil jako nový nález.

## Zjištění k plánu (Definition of Ready)

| Položka | Stav | Poznámka |
|---|---|---|
| Cíl je měřitelný | ano | zúžený na pět kontraktů; „pro každý nový test existuje mutace, pod kterou padne" je dnes doložené, ne slíbené |
| Výstupy jmenují konkrétní soubory | ano | tři soubory; u uzlu nově i to, které dva odstavce se mění |
| Slice pochází z `intent slice` | ano | beze změny |
| Každý dotčený kontrakt má jmenovaný vynucovač | ano | pět symbolů, u nových i soubor |
| Testová specifikace: happy + hrana + chyba | ano | `V6` jako chybový případ, uzel bez `path`/`depth` jako hrana |
| **Failing-test evidence** | **ano** | čtyři mutace, každá naměřená; dvě opravené v tomto kole a přeměřené |
| Každá položka DoD se mapuje na artefakt nebo příkaz | téměř | chybí položka pro shrnující odstavec — **P3** |
| Průvodní soubory vyjmenované | ano | `MAP.md`, `INDEX.json`, `_realization.yaml` |
| Žádný uzel ve slice nemá blokující otevřenou otázku | ano | `i0001` i `i0004` mají `open_questions: []` |
| Běh je implementovatelný a testovatelný izolovaně | ano | — |
| Kontrola rozsahu | ano | bez `--node`; pracovní strom je mimo adresář běhu čistý |

### P3 — Definition of Done zná jen jeden ze dvou odstavců

Výstupy plánu už mluví o dvou odstavcích, DoD pořád jen o odstavci s kritériem. Adversář
kontroluje DoD; co v ní není, se kontroluje z dobré vůle. Jedna odrážka navíc, například
„shrnutí na začátku `## Contracts` odpovídá seznamu kontraktů po změně".

### Pracovní poznámka k pořadí (opakuji z kola 2, není nález)

Přejmenování obou vynucovačů a úprava `enforced_by` musí padnout do jednoho kroku. Mezi tím
je strom nevalidní (V5 nenajde symbol) a vrstva realizace hlásí `broken` — je to přesně
jev, který popisuje `c17`. Konečný stav to neohrožuje; jde o to, aby Coder nezačal
mezistav „opravovat" v nástroji.

## Axiomy A1-A6

Posuzováno nad `i0004` po navržené změně, se splněnými podmínkami P1–P2.

- **A1 Refinement** — vztah k `i0001` beze změny; pět konkrétních tvrzení místo dvou
  smíšených uzel zkonkrétňuje. Bez nálezu.
- **A2 Preservation** — podmíněný nález z kola 2 je vyřešený: s „and nowhere else" už uzel
  neodporuje svému vlastnímu `c4`. Zbylé „Two of them" je zastaralý počet, ne rozpor —
  proto P1, a proto ne bloker. Vůči `i0001` bez nálezu.
- **A3 New information** — kritérium i všech pět kontraktů nese informaci, kterou `i0001`
  netvrdí. Že `c19` a `c20` nejsou dvě formulace téhož, je naměřené: každé padá pod jinou
  mutací a ani jedna mutace neshodí obojí. Bez nálezu.
- **A4 Contract strengthening** — potomci nejsou, kontrakty rodiče se nemění. Uvnitř uzlu
  závazek roste: `c4` + `c18` pokrývají celé pravidlo `_check_code_paths`, `c7` + `c19` +
  `c20` celý původní výrok `c7`. Nález z kola 1 uzavřen.
- **A5 Path sufficiency** — žádný cizí pojem; `KNOWN_FIELDS`, `build_index` i `V6` leží v
  `code_paths` uzlu. Bez nálezu.
- **A6 Frugality** — změna nezakládá uzel a nežádá si ho; tři kontrakty navíc patří k témuž
  nástroji a týmž cestám. Tělo uzlu zůstává hluboko pod hranicí V8. Bez nálezu.

## Co jsem ověřil sám

Kolo 3. Sondy běžely nad kopií `tools/` v `/tmp/critic_round2`; v repozitáři jsem nezměnil
nic než tento `critique.md`.

| Příkaz / úkon | Výsledek | Exit code |
|---|---|---|
| `python3 tools/intent/cli.py validate` | `5 node(s): 0 error(s), 0 warning(s)` | 0 |
| `python3 -m unittest discover -s intent/tests -t .` (v `tools/`) | `Ran 80 tests … OK` | 0 |
| Čtyři testy z testové specifikace proti nezměněné kopii | všech 7 tvrzení prochází | 0 |
| **Opravená mutace `c4`** (hlásit `V6` jen u dvojic se společným rodičem) | padá **právě** `test_cousins_half`; `test_siblings_half` i všech pět ostatních tvrzení prochází | 1 |
| Celá dnešní sada pod opravenou mutací `c4` | `Ran 80 tests … OK` — nová půlka je dnes nekrytá | 0 |
| **Opravená mutace `c20`** (pole `Node` z front matteru + přednost v `build_index`) | padá **právě** `test_index_ignores_the_written_path`; test `c19` prochází | 1 |
| Celá dnešní sada pod opravenou mutací `c20` | `Ran 80 tests … OK` — díra, kterou `c20` zavírá, je dnes nekrytá | 0 |
| Čtení `## Contracts` uzlu (řádky 85–101) proti výstupům plánu | „and nowhere else" pokryto, „Two of them" nikoli (**P1**) | — |
| Porovnání slibu v `change.md` s citovaným blokem kritéria | vsuvka u `c14` slíbena, v citovaném znění není (**P2**) | — |
| Porovnání sekce Výstupy s Definition of Done v `plan.md` | dva odstavce ve výstupech, jeden v DoD (**P3**) | — |
| Čtení opraveného odvození u `c14` v `change.md` | „always allows" + referent „its own gate"; správně | — |

Mutace z kol 1 a 2, které tato verze plánu opustila (`KNOWN_FIELDS` jako důkaz na
ignorování, „přeskočit dvojice se společným rodičem", tříbodová mutace `c20`), jsou
naměřené v předchozích verzích tohoto souboru a v `plan.md` shrnuté; neopakuji je zde.
