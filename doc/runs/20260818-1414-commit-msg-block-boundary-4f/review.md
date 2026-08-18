---
run_id: 20260818-1414-commit-msg-block-boundary-4f
intent_ids: ["i0005", "i0004"]
role: Adversary
model: cursor-grok-4.5-high
complexity: high
status: done
# round 3 verdict (below) supersedes rounds 1–2: APPROVE (revert to round-1 state)
---

# Recenze — hranice trailerového bloku před cleanupem

> **Kolo 3: `APPROVE` — revert kola 2 je přesný; platí stav konce kola 1.** Kola 1–2 níž jsou historie.

Měřeno na scratch kopiích pod `/tmp/adv1414-*` a `/tmp/adv1414-mut`; pracovní strom
tohoto repa jsem neměnil kromě tohoto souboru. Hook jsem volal jen na dočasných
souborech. Pro B4/B5/B6 jsem navíc spouštěl skutečný `git commit` v throwaway repu
(hooksPath → `/tmp`), nikoli jen izolovaný hook. Arbitrem trailerovosti zůstává
`git interpret-trailers --parse`. Předchůdcovy B4/B5/B6 a FU-10…FU-16 jsem
přeměřil, ne opsal. Strop ~40 měření; pořadí dle zadání Coordinátora.

Coder: `claude-sonnet-5-thinking-high` — model se liší.

## Verdikt

**APPROVE**

B4, B5 a B6 proti živému gitu zmizely. Osm pojmenovaných mutací řeže a jmenuje
slíbené case. FU-15 a FU-16 jsou zapsané jako cena, ne jako zlepšení, a realita jim
odpovídá. `_realization.yaml` je bez diffu; nikdo nárok nepředběhl. Věty `i0005` c1
a c2 na tvarech, které git skutečně vyrábí, drží. Follow-upy níž nejsou blokátory.

## Blockers

Žádné.

## Follow-upy

- **FU-A — scissors uprostřed zprávy usekne i legitimní trailery.** Řádek začínající
  `comment_char` a obsahující `>8` *před* trailerovým blokem (ne na konci jako u
  `git commit -v`) zkrátí `n` a zahodí vše za ním, včetně `Intent:` / `Run:`. Ranní
  grep Intent nechal a attribution smazal. Git takový tvar sám nevyrábí; jde o
  řemeslný útok na preflight, ne o návrat B6. Stojí za zúžení „první scissors od
  konce“ / „jen když za ním není klíčový trailer“, ne za zamítnutí tohoto běhu.
- **FU-B — první odříznutí koncových blanků (site1) není samo pojistkované.** Mutace
  jen `while (n>0 && is_blank) n--` hned po scissors nechá suite **zelenou** (exit 0):
  druhé odříznutí po komentářích tu práci zopakuje. Critic Note 1 a Coder (obě místa
  najednou → `attribution_then_trailing_blank_line` padá) to přiznali. Důkaz E-B4
  jako rituál platí; unikátní řez na site1 v enforceru chybí.
- **FU-C — `core.commentChar` mimo shodu se znakem ve file.** Když config říká `!` a
  ve file jsou `#` komentáře (nebo naopak default `#` a ruční `!` patička), preflight
  komentáře nestripne a attribution může zůstat v těle. Živý git při `commentChar=!`
  píše `! Please enter…` a tam B5 projde (změřeno). Neshoda je umělá; limit `auto` už
  dokumentují.
- **FU-D — próza *za* koncovým komentářovým blokem** nechá attribution v souboru
  (poslední odstavec je ta próza). `interpret-trailers --parse` ji jako trailer
  nevidí; ranní grep ji mazal. Git takový buffer neprodukuje. Blízko FU-15.
- Nesené beze změny z předchozího běhu: **FU-1 … FU-9**, **FU-17** (odsazená próza
  *v* trailerové zóně), mimo rozsah tohoto requestu.

## Kde věty dosahují

Věty: `i0005` c1 — *removes agent attribution and keeps everything else*;
`i0005` c2 — *every shipped hook is executable*. Čísla 59–61 navazují na tabulku
předchůdce (kolo 3).

| # | Místo | Mutace / pozorování | Suite / arbitráž | Stav |
|---|---|---|---|---|
| 59 | koncová prázdná řádka (B4) | `git commit -F` + trailing `\n\n`; iso hook | parse bez attribution; exit 0 | **closed** |
| 60 | editor comment block (B5) | skutečný editor commit; capture měl `# Please enter…` + attribution | parse jen Intent/Run | **closed** |
| 61 | `commit -v` scissors+diff (B6) | skutečný `-v`; capture měl `>8` + `diff --git` | parse jen Intent/Run | **closed** |
| 72 | preflight: scissors truncate | E-B6: zakomentovat `n = scissors-1` | exit 1, `attribution_then_scissors_and_diff` | **closed** |
| 73 | preflight: koncové komentáře | E-B5: zakomentovat `while is_comment` | exit 1, `attribution_then_editor_comment_block` (+ scissors case) | **closed** |
| 74 | preflight: koncové blanky (obě místa) | E-B4: oba `while is_blank` pryč | exit 1, jmenovitě `attribution_then_trailing_blank_line` | **closed** (rituál) |
| 74b | preflight: jen site1 blank | odebrat jen první `while is_blank` | exit **0** | **open — FU-B** |
| 63 | CRLF normalizace | E-10: bez `sub(/\r$/,"")` | exit 1, `crlf_line_endings` | **closed** (FU-10) |
| 64 | `is_blank` spaces | E-11: `/^$/` | exit 1, `blank_separator_only_spaces` | **closed** (FU-11) |
| 65 | adresa na pokračování non-by/with | E-12: adresa jen na key řádce | exit 1, `address_on_continuation_non_by_with` | **closed** (FU-12) |
| 66 | orphan continuation + address | E-13: větev pryč | exit 1, `orphan_continuation_with_address` | **closed** (FU-13) |
| 67 | fold join mezera | E-14: `val piece` bez mezery | exit 1, `folded_join_requires_space` | **closed** (FU-14) |
| 70 | attribution v subject/těle | vložit před blok | zůstává; parse ji nevidí | **closed jako cena** (FU-15 zapsaná) |
| 71 | Intent + pokračování s adresou | vložit fold | padá celý Intent; morning Intent nechal | **closed jako cena** (FU-16 zapsaná) |
| 75 | scissors uprostřed před trailery | `# …>8…` před Intent | Intent pryč | **open — FU-A** |
| 76 | c2 executable + committed mode | suite / `stat` 775 | exit 0, modes checked | **closed** |
| — | realization claim tohoto běhu | `git diff -- _realization.yaml` | prázdný; `i0005 not_claimed` | **closed** (nárok nepředběhnut) |

Demanda tohoto běhu (B4/B5/B6 + FU-10…16): uzavřeno. Open zbývá FU-A, FU-B a nesené FU-1…9.

## Co jsem si ověřil sám

| # | Měření | Výsledek | Exit |
|---|---|---|---|
| 1 | `hook_checks.py --root .` baseline | `35 message case(s); committed modes checked` | 0 |
| 2 | B4: `git commit -F` se trailing blank + attribution (throwaway repo) | parse: Intent+Run, bez Cursor | 0 |
| 3 | B4 izolovaně: hook + `interpret-trailers --parse` | totéž | 0 |
| 4 | B5: skutečný editor commit; capture v hooku měl `# Please enter…` a attribution | parse čistý; tělo bez attribution | 0 |
| 5 | B6: `git commit -v`; capture měl scissors `>8` + `diff --git` + attribution | parse čistý | 0 |
| 6 | `core.commentChar=!` + editor commit | capture `! Please enter…`; parse čistý | 0 |
| 7–12 | preflight: mid-comment; scissors v próze; early-scissors; all-comments; prose-after; no trailing NL | mid/próza/all/NL ok; early-scissors maže Intent (**FU-A**); prose-after nechá řádek v těle (**FU-D**) | — |
| 13–15 | CRLF × B4/B5/B6 tvary | attribution pryč, `\r` pryč | — |
| 16–17 | early-scissors NEW vs morning; mismatch commentChar | NEW slabší na Intent; mismatch umělý (**FU-A/C**) | — |
| 18 | E-B4 site1 only | suite **zelená** | 0 |
| 19 | E-B4 site2 only | padá editor+scissors case, ne trailing_blank | 1 |
| 20 | E-B4 both | `attribution_then_trailing_blank_line` (+2) | 1 |
| 21 | E-B5 | `attribution_then_editor_comment_block` | 1 |
| 22 | E-B6 | `attribution_then_scissors_and_diff` | 1 |
| 23–27 | E-10 … E-14 | jmenované case, každý exit 1 | 1 |
| 28–34 | keep: human co-author, Intent/Run, próza s adresou, subject Cursor, empty, one-line, all-trailers | lidské a Intent/Run drží; attribution v all-trailers pryč | — |
| 35–36 | FU-15 / FU-16 NEW vs morning | tělo attribution přežije / Intent padá celý — shoda s dokumentací | — |
| 37 | wording hook komentář + `hooks/README.md` „Two prices…“ | cena, ne improvement; text sedí s měřením | — |
| 38 | `stat` módy + suite c2 | 775; modes checked | 0 |
| 39 | `intent validate` / `scope` / `realization check` | 0/0; scope clean; consistent | 0 |
| 40 | `realization status i0005`; diff `_realization.yaml` | `not_claimed`; diff prázdný | 0 |

Diff proti `outputs`: jen `hooks/git/commit-msg`, `hooks/README.md`, `tools/checks/hook_checks.py`. Intent nody, `VERIFY.md`, `_policy.yaml`, `AGENT_MODELS.md` bez změny.

## Co jsem neměřil

Strop ~40 spotřebován (výše 1–40). Z plánovaného pořadí zbývá / nebylo:

- **FU-1 … FU-9** z ranního běhu — mimo rozsah requestu; nepřeměřováno znovu (ceiling / out of scope).
- **Širší kandidátská mřížka** předchůdce (53 × 6 tvarů) — neopakována; stačily živé B4/B5/B6 + keep vzorek.
- **Montáž `.cursor/hooks` symlink / `hooks.json` argumenty** (staré FU-4/FU-5) — ceiling.
- **Mutace enforceru samotného** (např. vrátit `read_text()` bez `newline=""`) — ověřeno jen směrem hook→suite, ne suite→vakuum zpětně mimo E-10 důsledek.
- **`core.commentChar=auto`** za běhu gitu — dokumentovaný limit; nezkoušeno.
- **`i0004` kontrakty** — ve slice jen jako soused; diff tools/intent se netýkal; nepřepočítávány.
- **Wall-clock / CI mimo Grader log** — Grader je zelený; nepřespouštěl jsem celý `VERIFY.md` znovu po vlastních `/tmp` mutacích (pracovní strom hooku nezměněn).

## Podepsal bych, že `i0005` c1 a c2 jsou teď dokázané, a že nic ve stromě není slabší než před tímto během a dvěma předchozími?

**c1 a c2 na tvarech, které git opravdu dává do `COMMIT_EDITMSG` v době hooku — ano.** B4/B5/B6 jsem viděl na skutečném `git commit` (včetně `-v` a `commentChar=!`); attribution z parse zmizí, Intent/Run zůstanou; c2 drží executable + committed mode přes stejný enforcer. FU-15/FU-16 jsou vědomá cena proti rannímu grepu a jsou zapsané pravdivě — větu c1 neruší (git je v těch tvarech stejně jako trailer neparsuje / unit-drop je nutný důsledek zvolené struktury).

**Absolutní „nic není slabší“ bez výhrady — ne.** Preflight poprvé zavádí regresi na řemeslném scissors uprostřed zprávy (FU-A: Intent zmizí, ranní hook ho nechal) a první blank-strip zůstává bez vlastního řezu (FU-B). To není návrat B4/B5/B6 a nezneplatňuje věty na běžném commitu; je to přesně to, co chybí k podpisu bez hvězdičky. Na uzavření uzlu jako `realized` po tvém `APPROVE`/claim bych ty dvě věci neblokoval — ale „dokázané beze zbytku vůči rannímu chování ve všech contrived bufferech“ bych nepodepsal.

---

# Recenze — kolo 2 (FU-A heuristika, FU-B odstranění)

Měřeno na `/tmp/adv1414-r2-*`; pracovní strom mimo tento soubor nedotčen. Strop ~25.
Coderovo tvrzení o „čistém zbytku“ a důkaz §6.6 jsem neopsal — zaútočil jsem na ně.

## Verdikt

**REQUEST CHANGES**

Kolo 1 `APPROVE` tímto kolem **neplatí**. Oprava FU-A zavedla chytrou heuristiku, která
na běžném `git commit -v` s trailer-tvarovanou řádkou v diffu **znovu otevírá B6**
(attribution přežije). Odstranění site1 (FU-B) stojí na nepravdivém univerzálním
důkazu: vstup „komentáře + koncová prázdná řádka“ attribution zase nechá. FU-C/FU-D
v README jako limity — bez námitek. `_realization.yaml` beze změny.

## Blockers

- **B7 — FU-A heuristika `seen_key` / „čistý zbytek“ padá na reálném diffu s `-Klíč:`.**
  `is_key` začíná třídou `[A-Za-z0-9-]`, takže **odebraná** řádka unified diffu
  (`-Intent: i0042`, `-Signed-off-by: …`, `-Co-authored-by: …`) je „trailer key“.
  Sken od konce nastaví `seen_key` dřív, než dojde na skutečnou scissors řádku; kandidát
  se odmítne; diff i komentáře zůstanou v bufferu hooku; attribution se zkopíruje jako
  „tělo“; git po hooku scissors/diff uklidí a **zapíše attribution**. Změřeno:
  (1) živý `git commit -v` po úpravě souboru s `Intent:` — parse obsahuje
  `Co-authored-by: Cursor <cursoragent@cursor.com>`; (2) totéž s `-Co-authored-by:` /
  `-Signed-off-by:` v syntetickém i živém bufferu. Ranní grep attribution smaže.
  Coderova premissa v `report.md` (*„diff nikdy neobsahuje holou Klíč: řádku — řádky
  začínají +/-/@“*) je **nepravdivá**: `-` je povolený první znak klíče. Tohle je
  dosažitelný běžný commit (šablona zprávy, testy hooku, jakýkoli soubor citující
  trailer) — ne řemeslný FU-A z kola 1. Věta c1 je na tomto tvaru lživá a slabší než
  před kolem 2 i než ranní hook.
- **B8 — důkaz FU-B „site1 je mrtvý pro každý vstup“ neplatí; odstranění oslabuje B5-tvar.**
  Protiargument: zpráva končící komentářovým blokem **a** koncovou prázdnou řádkou.
  Bez site1: `while is_comment` je no-op (poslední je blank), `while is_blank` blank
  sežere, komentáře už nikdo neodřízne → attribution přežije (změřeno; s dočasným
  návratem site1 zmizí). Důkaz §6.6 tvrdí, že site2 vždy dosáhne stejného `n` —
  to platí jen když se po blank-stripu **nevrací** ke comment-stripu; právě ten
  chybějící druhý průchod dělá site1 nenahraditelný. Živý editorový B5 v mém vzorku
  končil řádkou `#` (ne blankem) a sám o sobě prošel — ale kolo 1 tento tvar krylo a
  kolo 2 ho znovu otevřelo. Slabší než před tímto kolem.

## Follow-upy

- **FU-E — dvě scissors, podvržená *za* reálnou / za diffem.** Sken od konce přijme
  pravou (prázdný zbytek), usekne jen ji, **diff zůstane** a attribution přežije.
  Méně běžné než B7; po opravě B7 znovu změřit.
- **FU-F — Coder měl pravdu, že „první od konce“ samo o sobě FU-A neřeší** při jediné
  podvržené řádce. Směr skenu nestačí; potřeba je jiná (nebo žádná) hranice než
  „zbytek bez is_key“. Samotný case `scissors_before_trailer_block_keeps_trailers`
  je neprázdný (mutace na first-from-start → exit 1, jen ten case) — ale chrání
  syntetický FU-A a **nevidí B7**.
- FU-C, FU-D — zapsané limity; nepřepočítávány.
- Nesené FU-1…9, FU-17.

## Kde věty dosahují (delta kola 2)

| # | Místo | Mutace / pozorování | Výsledek | Stav |
|---|---|---|---|---|
| 61 | B6 jednoduchý diff (bez `-Klíč:`) | živý `commit -v` | attribution pryč | closed (úzký) |
| 77 | B6 + `-Intent:` / `-Signed-off-by:` / `-Co-authored-by:` v diffu | živý / syntetický `-v` | attribution **přežije** | **open — B7** |
| 78 | FU-A case (scissors před trailery) | suite + mutace first-from-start | Intent drží; mutace řeže | closed pro tento case |
| 74 | jediný blank-strip po komentářích | odebrat ho | 3 case červeně | closed jako řez |
| 74c | site1 „mrtvý“ | důkaz §6.6 vs comments+blank | důkaz padá; attribution přežije | **open — B8** |
| 70/71 | FU-15/16 ceny | beze změny | — | closed jako cena |
| — | realization | diff prázdný | — | closed |

## Co jsem si ověřil sám (kolo 2)

| # | Měření | Výsledek | Exit |
|---|---|---|---|
| 1 | živý `-v`, diff mění `Intent:` v souboru | parse **s** Cursor attribution | 0 commit |
| 2 | syntetický `-v` + `-Signed-off-by:` v diffu | attribution + DIFF_PRESENT | — |
| 3 | jen `+Intent:` (new file) | scissors OK, attribution pryč | — |
| 4 | context ` Intent:` (mezera) | OK | — |
| 5 | dvě scissors, podvržená za diffem | attribution + diff (**FU-E**) | — |
| 6 | dvě scissors, podvržená před + reálná vzadu | Intent drží (Coder OK) | — |
| 7 | zbytek „trailer-shaped“ (`updated:`) před Intent | podvržená odmítnuta; Intent drží | — |
| 8 | diff obsahuje `+# …>8…` | reálná hranice OK | — |
| 9 | živý `-v`, diff mění `Co-authored-by:` v souboru | attribution přežije (**B7**) | 0 |
| 10–12 | B4 `-F` / B5 editor / B6-simple regrese | všechny PASS bez attribution | 0 |
| 13 | suite baseline 36 case | satisfied | 0 |
| 14 | mutace zbylého blank-stripu | 3 jmenované case | 1 |
| 15 | mutace → first-from-start | jen `scissors_before_trailer_block_keeps_trailers` | 1 |
| 16–18 | E-B5, E-10, E-14 spot-check | jmenují stejné case jako kolo 1 | 1 |
| 19 | morning vs new na `-Intent:` v diffu | morning maže attribution, new ne | — |
| 20 | `is_key` na `-Intent:` / `+Intent:` / `--- a` | KEY / no / no | — |
| 21 | comments+trailing blank, current hook | attribution přežije (**B8**) | — |
| 22 | totéž se site1 vráceným | attribution pryč | — |
| 23 | živý B5 capture: končí `#`, ne blankem | B5-simple OK; důkaz tím neplatí | — |
| 24 | `git diff -- _realization.yaml` | prázdný | — |
| 25 | `hook_checks` na pracovním stromě | 36 case, satisfied | 0 |

## Co jsem neměřil

Strop ~25 spotřebován (1–25). Nezměřeno / zbývá:

- Zbývající mutace kola 1 (E-B4 both, E-B6, E-11, E-12, E-13) — jen spot-check E-B5/E-10/E-14.
- `core.commentChar=!` znovu s heuristikou + trailer v diffu.
- CRLF × B7 tvar.
- Zda `---` / `+++` / `index` kdykoli spustí `seen_key` na exotických cestách.
- Obnova site1 vs. smyčka „opakovat comment+blank strip do pevného bodu“ jako alternativa k B8.
- Celý `VERIFY.md` / unittest / ruff znovu (Coder hlásí zelené; nepřepočítáváno).
- FU-1…9, FU-C/D útoky — mimo rozhodnutí Coordinátora.

## Podepsal bych teď `i0005` c1 a c2 bez hvězdičky?

**Ne.** Hvězdička z kola 1 se nezmenšila — **zvětšila se a stala se blokátorem.**

- c1 na `git commit -v` při změně souboru, který obsahuje trailer-tvarované řádky, je teď
  **nepravdivá** (B7). To je horší než „řemeslný scissors uprostřed“ z kola 1: jde o
  ordinary use.
- Odstranění site1 (B8) otevírá comments+blank, které kolo 1 umělo; důkaz o mrtvém kódu
  neobstojí.
- c2 (executable) jsem v tomto kole neútočil znovu — na něm podezření nemám; problém je c1.

Bez opravy B7 (a rozhodnutí k B8: vrátit site1, nebo dokázat dosažitelnost limitem) nelze
`i0005` považovat za dokázané ani tvrdit, že strom není slabší než před těmito běhy.

---

# Recenze — kolo 3 (revert kola 2)

Poslední kolo, které metodika dovoluje. Objekt je **revert**, ne nová práce. Měřeno na
`/tmp/adv1414-r3-*`; pracovní strom mimo tento soubor nedotčen. Strop ~15.
Snapshot Codera jsem nebral jako pravdu — přeměřil jsem chování, které jsem v kole 1
sám viděl.

## Verdikt

**APPROVE**

`hooks/git/commit-msg` je zpět ve stavu konce kola 1 (preflight blok bajtově shodný s
tím, co jsem v kole 1 četl: scissors first-from-start, oba blank-stripy, žádné
`seen_key`). `hook_checks.py` má znovu přesně 35 case — chybí jen
`scissors_before_trailer_block_keeps_trailers`, žádný jiný case nezmizel ani se
nepřejmenoval. B7 a B8 s heuristikou / bez site1 zmizely. B4, B5, B6 na živém gitu
stále mrtvé. `_realization.yaml` beze změny. Jediný záměrný pozůstatek kola 2 je
dokumentace limitů v `hooks/README.md`; FU-A/C/D sedí, FU-B je formulován příliš
silně (follow-up níž, neblokuje kód).

## Blockers

Žádné.

## Follow-upy

- **FU-G — bullet FU-B v `hooks/README.md` přestřeluje.** Text říká, že *„every input
  the first one handles, the second one also reaches"* — to je nepravdivý univerzální
  claim z „důkazu" kola 2. Pravda z kola 1: mutace *jen* prvního blank-stripu nechá
  suite zelenou (druhý kryje osamocené trailing blanky); první strip je přesto
  load-bearing, když po komentářovém bloku následuje blank (bez něj comment-strip
  nezačne). Špatně zapsaný limit zve k opakování chyby kola 2. **Opravit wording před
  nebo spolu s realization claim** — neblokuje věty c1/c2 na kódu, ale nesmí zůstat
  jako doklad, že site1 lze smazat.
- FU-A, FU-C, FU-D — zapsané limity; FU-A ověřeno: podvržený scissors před trailery
  opravdu usekne Intent (shoda s README).
- Nesené FU-1…9, FU-15/16 jako ceny, FU-17.

## Kde věty dosahují (delta kola 3)

| # | Místo | Pozorování | Stav |
|---|---|---|---|
| 59–61 | B4/B5/B6 | živý git po revertu, parse bez attribution | **closed** |
| 77 | B7 (`-Intent:` v diffu u `-v`) | attribution pryč (heuristika pryč) | **closed** |
| 74c / B8 | comments+trailing blank | attribution pryč (site1 zpět) | **closed** |
| 78 | case `scissors_before_…` | odstraněn; 35 jmen = sada kola 1 | **closed** (záměr) |
| — | README FU-A | truncates including Intent; git never produces | **closed** (přesné) |
| — | README FU-B | přestřeluje „second also reaches" | **open — FU-G** |

## Co jsem si ověřil sám (kolo 3)

| # | Měření | Výsledek | Exit |
|---|---|---|---|
| 1 | živý `-v` + `-Intent:` v diffu (B7 tvar) | parse Intent+Run, **bez** Cursor | 0 |
| 2 | B4 `commit -F` + trailing blank | PASS | 0 |
| 3 | B5 editor commit | PASS | 0 |
| 4 | B6-simple `-v` | PASS | 0 |
| 5 | B8 comments+trailing blank na hooku | attribution pryč | — |
| 6 | struktura hooku: `seen_key` / from-end / blank×2 / preflight blok | False / False / 2 / **exact round-1 block** | — |
| 7 | suite 35 case | satisfied | 0 |
| 8 | mutace jen site1 | suite **zelená** (stejné jako kolo 1) | 0 |
| 9 | mutace obou blank-stripů | 3 B-case červeně | 1 |
| 10 | seznam 35 jmen vs očekávaná sada kola 1 | identická; `scissors_before` nepřítomný | — |
| 11 | FU-A crafted scissors | Intent pryč — shoda s README | — |
| 12 | README FU-A/C/D vs chování | přesné | — |
| 13 | README FU-B vs M5+M8 | overclaim → FU-G | — |
| 14 | `realization` / diff `_realization.yaml` | `i0005 not_claimed`; prázdný | 0 |
| 15 | (rezerva stropu) — nepoužito na další mutace E-* | — | — |

## Co jsem neměřil

Strop ~15. Nezměřeno:

- Opakování všech osmi mutací E-B5…E-14 z kola 1 (jen site1 / oba blanky).
- Druhý živý B7 tvar (`-Co-authored-by:` v diffu) — analogie k `-Intent:` stačila.
- `core.commentChar=!` po revertu.
- Bajtový diff proti Coderovu souboru snapshotu (místo toho fingerprint z kola 1 + chování).
- Celý `VERIFY.md` / unittest / ruff (Coder hlásí; nepřepočítáváno).
- FU-1…9.

## Podepsal bych teď `i0005` — tři otázky

**1. Jsou c1 a c2 dokázané tímto během?**  
**Ano** — ve stejném smyslu jako po kole 1: enforcer 35 case, živé B4/B5/B6, B7/B8 po
revertu zase drží, c2 executable přes stejný cmd. Strom se nezměnil.

**2. Je něco ve stromě slabší než před tímto během a třemi předchozími?**  
**Ne oproti konci kola 1** (cíl revertu). Oproti kolu 2 je strom *silnější* (B7/B8 pryč).
Oproti rannímu řádkovému grepu zůstávají vědomé ceny FU-15/16 (zapsané) — to není
regrese tohoto revertu, je to rozhodnutí struktury z kola 1 / odloženého patche.

**3. Hvězdička — co ji nese, a má blokovat claim?**  
- **FU-A** (podvržený scissors před trailery maže Intent) — **known limit**, README
  přesné, git tvar nevyrábí → **neblokuje claim**.
- **FU-B** (první blank-strip nemá izolující mutaci v suite) — **known testing limit**;
  claim neblokuje, ale **FU-G** (špatný wording v README) opravte při zápisu claimu,
  ať nikdo znovu „nedokáže" mrtvý kód.
- **FU-C / FU-D** — known limits, README sedí → **neblokují claim**.
- Ceny **FU-15 / FU-16** — záměr, ne hvězdička nad pravdivostí c1.

**Verdikt pro Coordinátora:** `APPROVE` — můžeš zapsat `realization claim` na `i0005`
po zeleném Graderu; před nebo spolu s tím ideálně jedna věta FU-G v README.
