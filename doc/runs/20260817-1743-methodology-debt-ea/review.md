---
run_id: 20260817-1743-methodology-debt-ea
intent_ids: ["i0002"]
role: Adversary
model: claude-opus-5-thinking-high
complexity: high
status: done
---

# Nezávislá recenze

## Verdikt

APPROVE

**Commitu nebrání nic.** Bloker B1 z kola 1 je zavřený, nález Z2 je opravený a zbylé dva
nálezy kola 1 rozhodl Human. Všech šest strojových bran jsem po druhé změně přehrál znovu
sám: `validate` 0, `realization check` 0, 82 testů OK, `template_checks` 0, `hook_checks` 0,
kontrola rozsahu čistá se **4 deklarovanými cestami**. Rozpočty drží (118 ≤ 150, 97 ≤ 250,
R1+R3 stále přesně 8 přidaných řádků), `stale 0`, `broken 0`, `i0002` `not_claimed`,
`i0004` `realized`, `_realization.yaml` nedotčený.

Zbývají tři neblokující doporučení: tabulka ve vysvětlení neukazuje zpátky na poznámku,
poznámka obsahuje jedno tvrzení, které repozitář neumí ověřit, a kontrolní tabulka v
katalogu dál píše rodinu bez úsilí (nález Z4 z kola 1, o kterém Human nerozhodoval).
Žádné z nich nemění, co je pravda po commitu, jen kolik práce dá to příště ověřit.

---

## Blokující

**Žádné.**

### B1 je zavřený — a zavřel se přesně na té cestě, kterou jsem pojmenoval

Bloker nestál na tom, že v repozitáři existuje zastaralá věta, ale na tom, že **katalog
sám** posílá čtenáře do dokumentu, který ho popírá (`AGENT_MODELS.md:11` → „Why these slugs
were chosen: see `AGENT_MODELS.explanation.md`"). Tuhle cestu poznámka přerušuje fyzicky:
sedí jako **druhá sekce souboru** (ř. 20–35), hned za `## Podklady` a před vším ostatním.
Kdo přijde po odkazu z katalogu, potká ji dřív než tabulku.

Není to třetí hlas, protože **jmenuje své cíle**: říká, které čtyři řádky tabulky Role ×
pásmo (Coder `medium`/`high`, Planner `low`/`medium`, Critic `high`, Coordinator `medium`)
a která věta („Grok 4.5 … do katalogu nepatří", dnes ř. 76) jsou překonané. Ověřil jsem, že
výčet sedí buňka po buňce se čtyřmi skutečnými výskyty v tabulce — nic nepřebývá a nic
nechybí. To je stejný vzor jako `superseded_by` ve stromu záměru: starý text zůstává
čitelný, ale ví se o něm, že už neplatí.

Rozhodnutí ponechat argumentaci Humana beze změny je navíc **správnější** než přepis, který
jsem v kole 1 připouštěl jako variantu. Zdůvodnění ze 17. 8. bylo pravdivé vůči tomu, co se
tehdy vědělo; neplatný je jediný fakt (předatelnost slugu), a přesně ten poznámka opravuje.
Přepsaná tabulka by smazala stopu, proč se rozhodovalo, jak se rozhodovalo.

---

## Závažné

Všechny tři jsou **neblokující** a všechny tři se zavírají jedním řádkem textu.

### Z5 — odkaz vede jen jedním směrem (nový)

Poznámka ukazuje na tabulku, tabulka neukazuje na poznámku. Čtenář, který do souboru
nevstoupí shora — hledáním slugu, nebo protože ho zajímá sekce „Proč Opus 5 zůstává (a
kde)" (ř. 91) — dostane na ř. 97–110 čtyři živě vypadající doporučení nespustitelného slugu
bez jakékoli značky. Přesně tak vznikl dluh, který tento běh uklízí: hodnota se přečetla z
tabulky, ne z argumentace kolem ní.

Human si vymínil, že se jeho úvaha nepřepisuje. Jedna věta **nad** tabulkou to neporušuje,
protože nemění ani řádek jeho zdůvodnění:

> Řádky s `cursor-grok-4.6-high` překonává „Poznámka (2026-08-17)" výše.

Neblokuje: kdo přijde po odkazu z katalogu, poznámku vidí, a ta cesta byla důvodem blokeru.

### Z6 — jedno tvrzení poznámky repozitář ověřit neumí (nové)

Poznámka má tři faktická tvrzení. Dvě jsem ověřil nezávisle:

| Tvrzení | Ověření |
|---|---|
| `cursor-grok-4.6-high` nejde předat subagentovi | ✓ potvrzeno — v seznamu slugů, které umím předat, tento slug není; empiricky totéž zjistil běh `20260817-1703` |
| dostupné Grok slugy jsou `cursor-grok-4.5-high` a `cursor-grok-4.6-medium` | ✓ potvrzeno, přesná shoda |
| „v Cursor UI je Grok 4.6 s vysokým úsilím dostupný" | **neověřitelné** — repozitář o nabídce UI nemá žádný podklad; `doc/cursor_models/` uvádí ceny a benchmarky, ne přepínače UI, a můj seznam modelů je seznam pro subagenty, ne pro UI |

Je to tvrzení o produktu, ne o repozitáři, zapsané do souboru, jehož vlastní zásada zní
„do katalogu jdou jen slugy, které Coordinator umí předat … jinak by řádek v YAML byl
přání". Tentýž druh nedoloženého faktu vyrobil dluh, který tady uklízíme, jen o pásmo vedle.

Navíc **není potřeba**: pointa věty (že katalog nesoudí kvalitu modelu a nemluví Humanovi
do volby v UI) plyne z R2 bez ohledu na to, co UI dnes nabízí. Stačí ubrat půlku věty, nebo
ji označit za pozorování k 17. 8. 2026.

### Z4 (z kola 1) — kontrolní tabulka v katalogu dál uvádí rodinu bez úsilí

`AGENT_MODELS.md:77–79` má v pásmech `low` a `medium` buňky „Grok 4.6", zatímco YAML nad
nimi má `cursor-grok-4.6-medium`. Na úrovni rodiny to sedí, ale celé R4 stojí na tom, že
**úsilí je součást slugu**. Human o tomto nálezu nerozhodoval a oprava se nestala; nechávám
ho otevřený, aby nezmizel mezi koly. Riziko je po poznámce menší (mapování pásem je teď
napsané i ve vysvětlení), fix je pořád `Grok 4.6 (medium)` / `Grok 4.5 (high)`.

---

## Drobné / neblokující

- **Přeformulovaný úvod `## Cursor limitation` není v „Znění k zapracování".** Oprava Z2 je
  věcně přesně to, co jsem žádal — „a courtesy for a role the catalog does not govern, not
  an instruction to apply a catalog value" ten šev zavírá. `report.md` ji poctivě přiznává,
  ale `plan.md` cituje doslovně jen tři odstavce R2, takže v záznamu běhu je změna pravidla,
  kterou žádná citace nekryje. Doplnit to znění do plánu nebo do `status.md`; jinak příští
  čtenář diffu najde úpravu bez předlohy — a přesně na tohle jsem si v kole 1 stěžoval.
- **`AGENT_MODELS.md:15`** dál říká „for the parent window, it reminds the Human to select
  it", tedy tón, který pravidlo právě zjemnilo. Rozpor to není: hned následující věta na
  ř. 16 autoritu UI přiznává, takže se to vysvětlí samo v místě. Kosmetické sladění.
- **Věta poznámky o pásmech** („katalog v pásmu `high` používá `cursor-grok-4.5-high` a v
  pásmech `low`/`medium` `cursor-grok-4.6-medium`") platí o **Grok sedadlech**; na `high`
  mají Planner, Coordinator i Adversary Opus 5. V kontextu odstavce je to jasné, izolovaně
  vytržené to není přesné.
- **Beze změny z kola 1:** kotva „later gate" u R1 neřeší znovuotevření jinou cestou než
  branou; R3 je nutná, ne postačující podmínka a agent s pouhou always-applied sadou si ji
  může přečíst jako povolení kódovat hned po ACCEPT Kritika; rozpočet R1+R3 je vyčerpaný na
  doraz (8 z 8); `grader.md` má ve front matter `status: in-progress`. Nic z toho neblokuje.

### Nálezy kola 1 uzavřené rozhodnutím Humana

| Nález | Rozhodnutí | Můj postoj |
|---|---|---|
| Z1 — `grader.md` napsal Coder | patří do metodiky, ale vlastním během; tento běh to nepropašuje | souhlasím; oddělení rolí je pravidlo, a pravidlo se zavádí branami, ne mimochodem — přesně jak to řekl R3 |
| Z3 — Critic a Coder sdílejí `cursor-grok-4.5-high` na `high` | zůstává; Kritik posuzuje Plannera, ne Codera | přijímám. Nález jsem podával jako vědomou volbu, ne jako porušení; deklarovaná tvrdá omezení drží dál a shoda existovala i před během |

---

## Co jsem ověřil sám (kolo 2)

**Brány přehrané znovu po obou změnách** (vše exit 0, nezávisle na `grader.md`):

| Příkaz | Výsledek |
|---|---|
| `python3 tools/intent/cli.py validate` | `5 node(s): 0 error(s), 0 warning(s)` |
| `python3 tools/intent/cli.py realization check` | `realization layer consistent (1 entry/entries)` |
| `python3 -m unittest discover -s tools/intent/tests -t tools` | `Ran 82 tests … OK` |
| `python3 tools/checks/template_checks.py --root .` | `template contracts satisfied` |
| `python3 tools/checks/hook_checks.py --root .` | `hook contracts satisfied` |
| `python3 tools/intent/cli.py scope --run doc/runs/…-methodology-debt-ea` | `scope clean (4 declared path(s))` |

- **Rozsah.** `plan.md` má `AGENT_MODELS.explanation.md` mezi `outputs` a v sekci
  „Rozšíření rozsahu … autorizoval Human" nese i důvod a obě věcná rozhodnutí. `git status`
  = čtyři deklarované soubory plus adresář běhu. Rozšíření tedy proběhlo deklarací, ne
  tichým zápisem, a kontrola rozsahu ho vidí (3 → 4 cesty).
- **Doslovnost.** Skript znovu: R1 → `07-ice-workflow.mdc` **True**, R3 → tamtéž **True**,
  R2 (tři odstavce) → `00-model-policy.mdc` **True**. Oprava Z2 se dotkla jen textu **před**
  R2, ani jedno slovo tří odstavců se nezměnilo.
- **Rozpočty.** `wc -l`: 118 (≤ 150) a 97 (≤ 250); `AGENT_MODELS.explanation.md` 163 řádků,
  limit se na něj nevztahuje (není to pravidlo). `git diff --numstat`: `8 0` u always-applied
  souboru — cap 8 řádků platí i po druhé změně, protože ta šla jinam. `template_checks`
  potvrzuje kontrakt `c2` uzlu `i0002`.
- **Sousedé — opakované hledání přes celý repozitář** (mimo tento soubor).
  `cursor-grok-4.6-high` je na **28 místech**: 22 v `doc/runs/` (audit, správně beze změny),
  **4 v tabulce Role × pásmo** (očekávané, jmenovitě překonané) a **2 v samotné poznámce**
  (nutné — poznámka musí slug pojmenovat, aby ho mohla překonat). V `rules/`, `skills/`,
  `README.md`, `VERIFY.md`, `AGENT_MODELS.md`, `hooks/`, `tools/` a `doc/intent/` **ani
  jeden**. Proti R1/R2/R3 jsem znovu pročetl `00-model-policy.mdc` celé, `07-ice-workflow.mdc`,
  `07-run-artifacts.mdc`, `07-intent-tree.mdc`, `07-realization.mdc`, skilly `ice-run`,
  `ice-implement`, `ice-review`, `intent-change`, `README.md` a katalog: **žádný text neříká
  opak**. Sekce „Rodičovské okno" ve vysvětlení (ř. 142–150) je s R2 i s novým „courtesy"
  úvodem ve shodě, jediné tření je kosmetické (`AGENT_MODELS.md:15`).
- **Poznámka proti tabulce.** Výčet překonaných řádků porovnán s obsahem tabulky (ř. 97–110):
  čtyři výskyty slugu = čtyři jmenované řádky. Citace věty o Grok 4.5 odpovídá ř. 76.
- **Realizace.** `realization status`: `i0002` `not_claimed`, `i0004` `realized`,
  `summary` → `stale 0, broken 0`. `git status doc/intent/` prázdný — nic v `doc/intent/`
  se nehnulo, takže druhá změna nezastarala žádný důkaz a Coder si nic nepřipsal.
- **Vymyšlené důkazy.** `grader.md` má tři oddíly (základ, přegradování po opravě Z2,
  přegradování po rozšíření rozsahu). Každý příkaz posledního oddílu jsem spustil a dostal
  shodný výstup včetně `4 declared path(s)` a `97` řádků. Žádný test, žádná mutace, nic
  navíc.

**Co ještě zbývá udělat před commitem** (proces, ne vada): `status.md` od Coordinatora s
modely, počty kol a záznamem, že rozšíření rozsahu udělil Human; povinná brána Humana pro
složitost `high`; a v commit message trailery `Intent: i0002` a
`Run: 20260817-1743-methodology-debt-ea`.

---

## Kolo 1 (záznam) — verdikt REQUEST CHANGES

Níže beze změny smyslu; historický záznam prvního kola. Nadpisy jsou o úroveň zanořené,
text je původní.

### Verdikt kola 1

REQUEST CHANGES

Vlastní zásah je poctivý: znění R1, R2 i R3 je **doslovné z plánu**, R2 nese všech sedm
závazků Humanova rozhodnutí, rozpočty drží (8 přidaných řádků z 8 povolených, 118 ≤ 150,
96 ≤ 250), všech šest buněk katalogu je opravených, kontrola rozsahu je čistá, žádné
tvrzení o realizaci Coder nezapsal a žádný test ani mutace si běh nevymyslel. Všech šest
strojových bran jsem přehrál sám a čísla v `grader.md` sedí do posledního řádku.

Zamítám kvůli **sousedovi, kterého běh vědomě nechal stát**: `AGENT_MODELS.explanation.md`
dál doporučuje `cursor-grok-4.6-high` ve čtyřech řádcích a dál tvrdí, že Grok 4.5 do
katalogu nepatří. Katalog na tento soubor **odkazuje** jako na vysvětlení svých hodnot, a
běh `20260817-1703` dokládá, že právě z něj se katalog obnovuje. Nespustitelný slug tedy
v repozitáři přežívá přesně tam, odkud se do katalogu vrátí.

### Blokující (kolo 1)

#### B1 — `AGENT_MODELS.explanation.md` popírá nový katalog a drží nespustitelný slug

Stav po běhu:

| Místo | Co říká | Co říká katalog po R4 |
|---|---|---|
| `AGENT_MODELS.explanation.md:83` | Coder `medium`/`high` = `cursor-grok-4.6-high` | `4.6-medium` / `4.5-high` |
| `AGENT_MODELS.explanation.md:84` | Planner `low`/`medium` = `cursor-grok-4.6-high` | `4.6-medium` |
| `AGENT_MODELS.explanation.md:87` | Critic `high` = `cursor-grok-4.6-high` | `4.5-high` |
| `AGENT_MODELS.explanation.md:91` | Coordinator `medium` = `cursor-grok-4.6-high` | `4.6-medium` |
| `AGENT_MODELS.explanation.md:59` | „Grok 4.5 … do katalogu **nepatří**" | katalog má `cursor-grok-4.5-high` ve dvou buňkách |

Proč to není jen zastaralý historický záznam, který se smí nechat být:

1. **Katalog na něj sám odkazuje.** `AGENT_MODELS.md:11` říká „Why these slugs were chosen:
   see `AGENT_MODELS.explanation.md`". Kdo se zeptá „proč tam je 4.5-high", dostane od
   odkazovaného souboru odpověď „4.5 tam nemá být" a tabulku se šesti starými hodnotami.
2. **Ta cesta už jednou zafungovala.** `doc/runs/20260817-1703-views-hygiene-dc/status.md:129`:
   „Katalog po obnově z 17. 8. 2026 dává na `high` Kritikovi i Coderovi
   `cursor-grok-4.6-high`. Ten slug **není spustitelný**." Obnova z tohoto zdůvodnění je
   přesně to, co dnešní dluh vyrobilo. Nechat zdroj beze změny znamená čekat na opakování.
3. **Hranice, kterou plán zvolil, není konzistentní.** Plán soubor vynechal s tím, že je to
   „lidský záznam Humana" — ale `AGENT_MODELS.md` má `authority: Human` také a běh ho
   přepsal. Buď se Humanových souborů běh nedotýká, nebo se jich dotýká s branou `high` a
   lidským posouzením po výsledku; obojí najednou nejde.
4. **Slíbená náhrada zatím neexistuje.** Plán i Kritik („Mlčet o tom nejde") odkazují zápis
   přehlasování do `status.md`. Ten v běhu není — je to krok 9 Coordinatora. Dnes tedy
   nedrží ani tato slabší varianta a repozitář o sobě tvrdí X i ne-X bez jediné značky.

**Co to zavírá.** Minimálně datovaná poznámka v `AGENT_MODELS.explanation.md`, která u
tabulky „Role × pásmo" a u věty o Grok 4.5 řekne, že je 17. 8. 2026 přehlasoval běh
`20260817-1743-methodology-debt-ea`, a proč (slug není předatelný delegované roli). Jestli
tu poznámku smí napsat agent, nebo ji píše Human, je rozhodnutí Humana — ale běh nesmí
skončit jako `done` ve stavu, kdy katalog odkazuje na dokument, který ho popírá.

Coder tímto nálezem nic neporušil: implementoval, co plán řekl. Nález patří Coordinatorovi
a Humanovi, ne do dalšího kola s Coderem.

### Závažné (kolo 1)

#### Z1 — `grader.md` napsal Coder

`report.md` v sekci „Vytvořeno" uvádí `doc/runs/20260817-1743-methodology-debt-ea/grader.md`.
Podle `rules/07-run-artifacts.mdc` je autorem `grader.md` Grader, podle `skills/ice-run`
kroku 7 spouští brány Coordinator (**„Run the machine gates yourself; do not trust numbers
from the report"**) a podle `skills/ice-implement` ř. 75–76 platí, že „numbers you write in
the report are claims; the Grader's log is the record". Tady je záznam i tvrzení od téhož
autora, takže brána, která má Coderovi nevěřit, je jeho vlastní výstup.

Věcně z toho tentokrát škoda nevznikla — přehrál jsem všech šest příkazů sám a každý řádek
`grader.md` odpovídá skutečnosti. Vada je v oddělení rolí, ne v číslech. Coordinator má
`grader.md` převzít (přegenerovat vlastním během příkazů), jinak si běh, jehož tématem je
„brána, kterou si nesmíš odsouhlasit sám", tuhle chybu dělá na sobě.

#### Z2 — R2 je sloučené polohou, ne významem

R2 leží uvnitř sekce `## Cursor limitation`, což Kritik žádal, a třetí paralelní kopie
opravdu nevznikla. Původní věta té sekce ale zůstala nedotčená:

> The Coordinator passes the slug when starting a subagent, and **reminds the Human** which
> model to select for the parent window.

O tři řádky níž stojí, že pro roli rodičovského okna **katalog neplatí**. Čtenář má pak
odvodit, na základě čeho ho Coordinator upomíná, když ta role katalogu nepodléhá. Sám
Human tenhle šev v `AGENT_MODELS.explanation.md:129` zašil — „Nesedí-li s řádkem katalogu,
Coordinator má připomenout přepnutí — a nesmí to hlásit jako odchylku" —, ale do pravidla
se ta spojka nedostala.

Není to rozpor, který by šlo splnit oběma směry naráz, proto ne bloker; je to zbytková
nejednoznačnost přesně na místě, kvůli kterému běh vznikl. Zavře ji doplnění dvou slov
(řádek katalogu je pro rodičovské okno **doporučení**, ne závazek), což je změna znění nad
rámec plánu, a tedy věc Humana.

#### Z3 — po R4 mají Critic `high` a Coder `high` tentýž slug

Katalog po substituci: Critic `high` = `cursor-grok-4.5-high`, Coder `high` =
`cursor-grok-4.5-high`. Deklarovaná tvrdá omezení to neporušuje (`critic_differs_from_planner`
i `adversary_differs_from_coder` drží ve všech třech pásmech, ověřeno) a **není to regrese**
— před během měly obě buňky `cursor-grok-4.6-high`, tedy taky shodu.

Tenhle běh je ale živá ukázka důsledku: `critique.md` má `model: cursor-grok-4.5-high` a
`report.md` má `model: cursor-grok-4.5-high`. Plán schválil model, který pak plán prováděl.
Substituce byla úsudek se dvěma dostupnými slugy, takže volba `cursor-grok-4.6-medium` pro
Critic `high` by tu shodu odstranila zadarmo. Human o tom má rozhodnout vědomě, ne ji
zdědit.

#### Z4 — kontrolní tabulka pod YAML uvádí rodinu bez úsilí

| Band | Planner | Critic | Coder | Adversary |
|---|---|---|---|---|
| `low` | Grok 4.6 | … | … | … |
| `medium` | Grok 4.6 | … | Grok 4.6 | … |

Buňky „Grok 4.6" odpovídají YAML (`cursor-grok-4.6-medium`) na úrovni rodiny, takže DoD
formálně splněné je. Jenže celé R4 stojí na tom, že **úsilí je součást slugu**: `4.6-high`
nejde spustit, `4.6-medium` ano. Tabulka je teď jediné místo v repozitáři, kde Grok 4.6
stojí bez úsilí — a je to tabulka, ze které se katalog čte při kontrole. Doplnit
`(medium)` / `(high)` je jednořádková oprava, která zavírá tutéž cestu zpět jako B1.

### Drobné / neblokující (kolo 1)

- **R1 a „later gate".** Pořadí bran, ze kterého plyne, co je „pozdější", nikde definované
  není: tabulka Gates je matice podle složitosti, sekvence žije až v `skills/ice-run`
  krocích 5–8. Kotva „same run" díru z kola 1 zavírá, ale znovuotevření **jinou** cestou
  než branou (Human, vlastní čtení Coordinatora) R1 neřeší. Znění je věrné Humanovu
  originálu z `20260816-2145-…/status.md:81–83`, takže to není vada překladu.
- **R3 jako nutná, ne postačující podmínka.** „only when" nepovoluje kódovat hned po ACCEPT
  Kritika; delší pořadí (validate → Kritik → brána Humana → promote → kód) drží
  `rules/07-intent-tree.mdc:150–153` a `skills/intent-change` krok 8. Ty soubory ale
  always-applied nejsou, kdežto R3 ano — agent s pouhou always-applied sadou si „smí, když
  Kritik přijal deltu" může přečíst jako povolení. Rozpor to není, riziko čtení ano.
- **Rozpočet vyčerpaný na doraz.** R1+R3 přidaly přesně 8 řádků z 8 (`git diff --numstat`:
  `8 0 rules/07-ice-workflow.mdc`). Splněno, ale bez rezervy: příští věta do téhož odstavce
  už rozpočet plánu překročí.
- **`grader.md` má ve front matter `status: in-progress`** u běhu, jehož `report.md` je
  `done`. Kosmetika.
- **README zůstává pravdivé.** Ř. 148 („Loops are bounded at three rounds; the fourth
  escalates to you") ani diagram na ř. 127–146 R1 neodporují — jen ten případ nekreslí.
  Doplnění šipky „REV → CRIT" je nabídka, ne nález.

### Co jsem ověřil sám (kolo 1)

**Brány přehrané nezávisle na `grader.md`** (vše exit 0):

| Příkaz | Výsledek |
|---|---|
| `python3 tools/intent/cli.py validate` | `5 node(s): 0 error(s), 0 warning(s)` |
| `python3 tools/intent/cli.py realization check` | `realization layer consistent (1 entry/entries)` |
| `python3 -m unittest discover -s tools/intent/tests -t tools` | `Ran 82 tests … OK` |
| `python3 tools/checks/template_checks.py --root .` | `template contracts satisfied` |
| `python3 tools/checks/hook_checks.py --root .` | `hook contracts satisfied` |
| `python3 tools/intent/cli.py scope --run doc/runs/20260817-1743-methodology-debt-ea` | `scope clean (3 declared path(s))` |

- **Rozsah (check 1).** `git status --short` = tři deklarované soubory plus adresář běhu;
  žádný soubor mimo `outputs`. Kontrola rozsahu bez `--node` čistá.
- **Doslovnost (check 2).** Skriptem jsem vytáhl tři citace z `plan.md` a hledal je jako
  přesné podřetězce v cílových souborech: R1 → `07-ice-workflow.mdc` **True**, R3 →
  tamtéž **True**, R2 (všechny tři odstavce) → `00-model-policy.mdc` **True**. Žádné tiché
  vylepšení.
- **Úplnost R2 (check 3).** Sedm závazků z `20260816-1302-…/status.md:83–91` větu po větě:
  (1) autorita UI pro roli rodičovského okna ✓, (2) není to výjimka / katalog pro tu roli
  neplatí ✓, (3) **nehlásí se jako odchylka** ✓, (4) delegované role berou model z katalogu
  ✓, (5) při kolizi ustupuje druhá role, nikdy volba Humana ✓, (6) ustupuje uvnitř katalogu
  na nejbližší pásmo s jiným slugem, jinak se Coordinator ptá ✓, (7) katalog vládne
  Coderovi jen je-li subagent, jinak platí ekonomika okna ✓. **Nic nechybí**; „the other
  role" je věrnější než „delegated" z kola 1.
- **Rozpočet (check 5).** `wc -l`: 118 (`07-ice-workflow.mdc`, ≤ 150), 96
  (`00-model-policy.mdc`, ≤ 250). `git diff --numstat`: +8 / +12 / 7 změněných řádků
  katalogu. Kontrakt `c2` uzlu `i0002` drží i podle `template_checks`.
- **R4 (check 6).** YAML buňka po buňce proti tabulce plánu — všech šest sedí. Matice
  omezení po substituci: `low` Planner Grok 4.6 ≠ Critic Sonnet 5, Coder Composer ≠
  Adversary Sonnet; `medium` Grok 4.6 ≠ Sonnet, Grok 4.6 ≠ Sonnet; `high` Opus ≠ Grok 4.5,
  Grok 4.5 ≠ Opus. Obě tvrdá omezení drží ve všech pásmech.
- **Sousedé (check 7).** `rg` přes celý repozitář (mimo tento soubor): `cursor-grok-4.6-high`
  má **22 výskytů** — 18 v `doc/runs/` (audit, správně beze změny) a **4 v
  `AGENT_MODELS.explanation.md`**
  (B1). V `rules/`, `skills/`, `README.md`, `VERIFY.md`, `hooks/`, `tools/` a `doc/intent/`
  ani jeden. Dále jsem proti R1/R2/R3 pročetl `skills/ice-run`, `ice-implement`,
  `ice-review`, `intent-change`, `rules/07-run-artifacts.mdc`, `07-intent-tree.mdc`,
  `07-realization.mdc`, `README.md` a uzly `i0001`/`i0002`: **žádný text neříká opak** —
  jediné tření je Z2 uvnitř samotného `00-model-policy.mdc`. `AGENT_MODELS.explanation.md`
  ř. 125–133 („Rodičovské okno") je s R2 naopak ve shodě.
- **Realizace (check 8).** `realization status --node i0004` → `realized`,
  `--node i0002` → `not_claimed`, `realization summary` → `stale 0, broken 0`.
  `git status doc/intent/` prázdný, takže `_realization.yaml` Coder nepsal.
- **Vymyšlené důkazy (check 9).** Žádný nový test, žádná mutace, žádný příkaz v `grader.md`
  neexistuje jen na papíře — každý jsem spustil a dostal shodný výstup. Tvrzení „failing-test
  evidence se netýká" je pravdivé; vynucovač `i0002` je `template_checks.py`.
- **Zdroj R1.** Znění porovnáno s `20260816-2145-…/status.md:81–83`; smysl zachován, kotva
  „in the same run" je doplněk Kritika, ne posun Humanova rozhodnutí.
