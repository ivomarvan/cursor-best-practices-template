---
run_id: 20260818-1414-commit-msg-block-boundary-4f
intent_ids: ["i0005", "i0004"]
role: Coder
model: claude-sonnet-5-thinking-high
complexity: high
status: in-progress
---

# Report — hranice trailerového bloku před cleanupem

## Co bylo implementováno

Aplikoval jsem odložený patch `deferred-i0005-hook.patch` (strukturální přestavba
`commit-msg` hooku nad trailerovým blokem, POSIX `awk`) a nad ním doplnil preflight, který
před výpočtem `last_blank` anticipuje to, co git se zprávou udělá **po** doběhnutí hooku:
useká scissors řádku a vše za ní (`git commit -v` / `--cleanup=scissors`), pak koncový
komentářový blok šablony editoru a koncové prázdné řádky kolem obojího. Bez toho hledal
hook trailerový blok v surovém souboru z editoru, ne ve zprávě, kterou git nakonec uloží —
a ve třech tvarech (B4, B5, B6) tak nechal celou attribution na místě.

Dále jsem do `tools/checks/hook_checks.py` dopsal sedm nových `Case` (tři pro B4/B5/B6,
čtyři pro FU-11…FU-14) a opravil čtení výstupu hooku na byte-exact porovnání (FU-10), a do
komentáře hooku i do `hooks/README.md` zapsal FU-15 a FU-16 jako vědomě zaplacenou cenu.

**Patch se aplikoval čistě** (`git apply --check` i `git apply` bez konfliktu, žádný hunk
jsem nemusel řešit ručně).

## Vstupy a výstupy

### Read

- `.cursor/skills/ice-implement/SKILL.md`
- `.cursor/rules/07-run-artifacts.mdc`
- `doc/runs/20260818-1414-commit-msg-block-boundary-4f/request.md`
- `doc/runs/20260818-1414-commit-msg-block-boundary-4f/plan.md`
- `doc/runs/20260818-1414-commit-msg-block-boundary-4f/critique.md`
- `doc/runs/20260818-1414-commit-msg-block-boundary-4f/slice-implement.md`
- `doc/intent/nodes/i0005-git-hooks.md`
- `doc/intent/nodes/i0001-harness.md`
- `doc/runs/20260818-0853-harness-and-hooks-audit-86/deferred-i0005-hook.patch`
- `doc/runs/20260818-0853-harness-and-hooks-audit-86/review.md` (kolo 3, od řádku 552)
- `hooks/git/commit-msg` (před i po aplikaci patche)
- `hooks/README.md` (před i po aplikaci patche)
- `tools/checks/hook_checks.py` (před i po aplikaci patche)

### Created

- `doc/runs/20260818-1414-commit-msg-block-boundary-4f/report.md`
- `doc/runs/20260818-1414-commit-msg-block-boundary-4f/coder-evidence.md`

### Changed

- `hooks/git/commit-msg`
- `hooks/README.md`
- `tools/checks/hook_checks.py`

### Not touched

- `doc/intent/nodes/**`
- `VERIFY.md`
- `doc/intent/_policy.yaml`
- `AGENT_MODELS.md`
- `doc/intent/_realization.yaml` (nepíšu nárok — to je na Coordinátorovi)

## Použité metody a rozhodnutí

1. **Aplikace patche jako povinný základ.** `git apply --check` prošel bez chyb, takže
   jsem patch aplikoval doslova a Group 1–4 stavěl nad ním, ne místo něj.

2. **Preflight přesně podle Plannerova pětikrokového návodu, ověřeného Kritikem** — scissors
   truncate → strip koncových blanků → strip koncových komentářů → strip koncových blanků
   znovu → teprve pak `last_blank`. `comment_char` čtu z `git config --get core.commentChar`
   s fallbackem `#` (i pro `auto`, jak plán žádá).

3. **Chyba v bash quotování, kterou jsem musel opravit sám.** Dva komentáře, které jsem
   chtěl vložit do awk skriptu (uvnitř jednoduchých uvozovek), obsahovaly apostrof
   (`editor's`, `-m $'…\n\n'`). Apostrof uvnitř `'...'` v bash ukončí řetězec předčasně —
   výsledkem byl syntax error a bash se pokoušel interpretovat zbytek awk skriptu jako
   shellové příkazy. Přeformuloval jsem obě věty bez apostrofu; nejde o změnu chování
   hooku, jen o opravu vlastní chyby při psaní komentáře.

4. **Note 1 Kritika (E-B4) — jednal jsem přesně podle doporučení.** Kritik změřil, že plánem
   popsaná mutace „přeskočit krok 2" nezčervená case `attribution_then_trailing_blank_line`,
   protože druhá polovina kroku 3 (vlastní odříznutí koncových blanků) běží bez ohledu na
   to, jestli komentáře skutečně existovaly, a sama o sobě odstraní i osamocené koncové
   blanky beze komentářů. Ověřil jsem to sám na scratch kopii a mutace „jen krok 2" opravdu
   nepadá. Pro `report.md`/`coder-evidence.md` jsem tedy mutoval **obě** místa odříznutí
   koncových blanků najednou — to už case zčervená. Netýká se to samotné implementace
   hooku (ta zůstává přesně podle pětikrokového návodu, dva samostatné kroky), jen manuální
   evidenční tabulky.

5. **B4/B5/B6 jsem demonstroval na reálném gitu, ne jen na syntetickém vstupu.** Pro B5 a
   B6 jsem vytvořil throwaway repozitáře pod `/tmp/coder4f/{b4,b5,b6}repo` a spustil skutečný
   `git commit` / `git commit -v` s `GIT_EDITOR` skriptem, který jen předsadí naši zprávu
   před šablonu, kterou git sám napsal (žádná ruční konstrukce „co by git mohl napsat" —
   zachytil jsem to, co git skutečně napsal, `cat -A`). B4 jsem demonstroval přes
   `git commit -F`, což je neinteraktivní cesta bez editoru. Arbitrem je vždy
   `git interpret-trailers --parse` na finální zprávě commitu. Žádný `git commit` neběhl
   v tomto repozitáři — jen ve třech throwaway repozitářích pod `/tmp`.

6. **FU-10 (byte-exact porovnání)** — přepsal jsem čtení výstupu z `read_text()` na
   `read_bytes()` a porovnání proti `case.expected.encode("utf-8")`; zápis vstupu jsem
   přesunul na `write_bytes()` pro všechny case (ne jen CRLF), aby srovnání bylo
   konzistentní a nezávislé na platformním překladu nových řádků.

7. **FU-11…FU-14 — jen nové `Case`, hook se neměnil.** Kód v hooku byl už z patche
   správný (`is_blank` široké, adresní pravidlo skenuje celý blok, orphan-continuation
   větev existuje, spojení se mezerou); chyběl jen řez v kontrole. Přidal jsem čtyři case
   podle tabulky v plánu a změřil, že příslušná mutace na hooku každý z nich samostatně
   zčervená (viz `coder-evidence.md`).

8. **FU-15/FU-16 zapsané jako cena, ne vylepšení** — přidal jsem dva odstavce do komentáře
   hooku (u horního bloku, ne u `END`) a do `hooks/README.md`, formulované jako důsledek
   rozhodnutí („próza před blokem nedotknutelná", „trailer se maže jako celek"), ne jako
   nová schopnost.

## Reference do kódu

| File | Lines | Summary |
|---|---|---|
| `hooks/git/commit-msg` | 27–39 | `comment_char` z `git config`, fallback `#`/`auto`→`#`; `is_comment` |
| `hooks/git/commit-msg` | 74–97 | Preflight: scissors truncate → blank strip → comment strip → blank strip |
| `hooks/git/commit-msg` | 20–25 | FU-15/FU-16 zapsané jako cena |
| `hooks/README.md` | 23–41 | Popis hranice bloku + sekce „Two prices, paid on purpose" |
| `tools/checks/hook_checks.py` | 243–312 | Sedm nových `Case` (B4/B5/B6 + FU-11…14) |
| `tools/checks/hook_checks.py` | 324–351 | `check_commit_msg_strips_attribution`: byte-exact čtení/zápis (FU-10) |

## Důkazy

| Command | Result | Exit code |
|---|---|---|
| `git apply --check deferred-i0005-hook.patch` | bez konfliktu | 0 |
| `python3 tools/checks/hook_checks.py --root .` | `hook contracts satisfied (2 shipped hook(s), 35 message case(s); committed modes checked)` | 0 |
| `python3 tools/checks/template_checks.py --root .` | `template contracts satisfied` | 0 |
| `python3 tools/intent/cli.py validate` | `5 node(s): 0 error(s), 0 warning(s)` | 0 |
| `python3 tools/intent/cli.py scope --run doc/runs/20260818-1414-commit-msg-block-boundary-4f` | `scope clean (4 declared path(s))` | 0 |
| `python3 -m unittest discover -s tools/intent/tests -t tools` | `Ran 99 tests in 0.286s — OK` | 0 |
| `ruff check tools/` | `All checks passed!` | 0 |
| `ruff format --check tools/` | `20 files already formatted` | 0 |
| B4 (`git commit -F`, throwaway repo) → `git interpret-trailers --parse` | jen `Intent: i0005`, žádná attribution | 0 |
| B5 (`git commit`, editor s komentářovým blokem, throwaway repo) → `git interpret-trailers --parse` | jen `Intent: i0005`, žádná attribution | 0 |
| B6 (`git commit -v`, scissors+diff, throwaway repo) → `git interpret-trailers --parse` | jen `Intent: i0005`, žádná attribution | 0 |
| E-B4 mutace (odstranění obou míst odříznutí koncových blanků) | case `attribution_then_trailing_blank_line` padá | 1 |
| E-B5 mutace (přeskočení odříznutí koncových komentářů) | case `attribution_then_editor_comment_block` padá | 1 |
| E-B6 mutace (přeskočení truncate na scissors) | case `attribution_then_scissors_and_diff` padá | 1 |
| E-10 mutace (odebrání `sub(/\r$/, "")`) | case `crlf_line_endings` padá | 1 |
| E-11 mutace (`is_blank` → `/^$/`) | case `blank_separator_only_spaces` padá | 1 |
| E-12 mutace (adresa jen na klíčové řádce) | case `address_on_continuation_non_by_with` padá | 1 |
| E-13 mutace (odebrání orphan-continuation větve) | case `orphan_continuation_with_address` padá | 1 |
| E-14 mutace (spojení bez mezery) | case `folded_join_requires_space` padá | 1 |

Číslo `35` case je claim, ne nezávislý zápis — plné surové výstupy (`cat -A`, diffy,
transkripty throwaway repozitářů) jsou v `coder-evidence.md`.

## Definition of Done (kolo 1)

Všechny povinné body z plánu jsou splněné artefaktem nebo příkazem výše: patch je
aplikovaný základ a Group 1–4 leží navrch (diff `git diff --stat` ukazuje jen tři soubory
z `outputs`); preflight v hooku existuje přesně v pořadí scissors→komentáře→blanky před
`last_blank`, `comment_char` má fallback; `hook_checks.py` prochází s 35 case (28 původních
+ 7 nových) a exit 0; failing-test evidence existuje pro každou řádku tabulky E-* v plánu,
včetně opravené (obě místa najednou) E-B4 podle Note 1 Kritika; B4/B5/B6 jsou ručně
demonstrované na reálném gitu ve throwaway repozitářích s `git interpret-trailers --parse`
jako arbitrem; FU-15 a FU-16 jsou zapsané jako cena v komentáři hooku i v README; `intent
validate` a scope guard běží čistě beze změny stromu; žádný `git commit`/`git add` neběhl
v tomto repozitáři; FU-1…FU-9 se v diffu neobjevují. Nezaškrtávám jen položky, které
patří Coordinátorovi (`grader.md`, realization claim) — ty jsem ani nepsal, ani se
nesnažil vyplnit.

---

## Kolo 2 — M1 (FU-A) a M2 (FU-B)

Adversary vrátil `APPROVE` bez blokátorů (viz `review.md`); tohle kolo řeší jen dva jeho
follow-upy, které Coordinátor vybral jako podmínku podpisu bez hvězdičky.

### M1 — FU-A: scissors řádka před trailerovým blokem

**Adversárův návrh („první scissors od konce, ne od začátku") jsem změřil a je
nedostatečný — řekl jsem to a udělal jsem něco jiného.** Když je v souboru jen jedna
scissors-tvarovaná řádka (přesně FU-A tvar), směr skenování na výsledek nemá vliv: „první
od začátku" a „první od konce" jmenují **tu samou** jedinou řádku. Ověřil jsem to přímo na
starém (nefixovaném) hooku — Intent/Run zmizí bez ohledu na směr skenu, protože chybějící
ingredience není směr, ale to, že se nikdy nekontroluje, co scissors řádka useká.

**Implementovaná oprava:** skenuji od konce a přijmu **první kandidátku, jejíž zbytek (vše
za ní až do konce souboru) neobsahuje žádnou neschovanou trailer-klíčovou řádku**. Git sám
píše scissors řádku vždy jen bezprostředně před diff (za ní jsou jen dvě pevné
help-textové komentářové řádky a pak diff, který nikdy neobsahuje holou `Klíč:` řádku —
řádky diffu začínají `+`/`-`/`@` nebo dvojtečku vůbec neobsahují), takže reálná hranice má
vždy „čistý zbytek" a je přijata. Podvržená řádka před `Intent:`/`Run:` čistý zbytek nemá
(za ní jsou reálné trailery), takže je odmítnuta a zůstává jako běžný text — nic za ní se
nezahazuje. Ověřil jsem i scénář se dvěma scissors řádkami (podvržená + reálná na konci se
skutečným diffem) — algoritmus správně vybere tu vpravo, protože jen její zbytek je čistý.

**Vedlejší pozorování, které patří do zápisu, ne pod koberec:** `git interpret-trailers
--parse`, spuštěný přímo na zprávu, která podvrženou `>8` řádku ještě obsahuje jako
literární text, vrátí prázdno — `interpret-trailers` má svoje **vlastní**, nepodmíněné
scissors-useknutí na libovolné takto tvarované řádce, bez ohledu na pozici, nezávisle na
našem hooku. To jsem si ověřil samostatně (jednořádkový pipe do `git interpret-trailers
--parse`) a taky přes reálný `git commit --edit` bez `-v` a bez explicitního
`--cleanup=scissors`: git sám v tomto (výchozím, `strip`) cleanup módu podvrženou řádku
smaže jako běžný komentář a nic za ní neuseká — Intent/Run v reálném commitu přežijí vždy.
**Nezkoušel jsem hook donutit tu podvrženou řádku sám smazat** — nejde o attribution, git
takový tvar sám nevyrábí a mazání cizího obsahu na heuristiku by vyměnilo teoretickou ztrátu
trailer-rozpoznatelnosti (na tvaru, který git nepíše) za skutečné porušení „keeps
everything else". Podrobně v `coder-evidence.md` §6.3–6.4.

Nový case `scissors_before_trailer_block_keeps_trailers` v `hook_checks.py` (řádka s
podvrženým scissors markerem před `Intent:`/`Run:`, plus attribution navíc); mutace zpět
na starý algoritmus (první-od-začátku, žádná kontrola zbytku) ho a jen ho zčervená.

### M2 — FU-B: první odříznutí koncových blanků

**Rozhodnutí: odstranil jsem ho — je to prokazatelně mrtvý kód, ne jen těžko testovatelný.**
Formální důkaz (viz `coder-evidence.md` §6.6): druhý blank-strip (ten za odříznutím
koncových komentářů) vždy dosáhne stejného `n` jako oba kroky společně, pro libovolný
vstup — pokud zpráva na konci komentářem nekončí, první odříznutí je no-op podle definice
(zkoumá jen aktuální poslední řádku); pokud zpráva na konci blankem končí (bez
komentářového bloku), odříznutí koncových komentářů je no-op tak jako tak a druhý
blank-strip smaže přesně to, co by smazal první. Nikdy nenastane vstup, kde by výsledek
závisel na tom, jestli první krok proběhl. To je přesně Kritikova a Adversárova pozorování
(mutace jen prvního kroku nikdy nezčervená), jen dotažené do závěru: první krok nechráníme
proto, že je nechráněný, ale proto, že nedělá nic, co by druhý krok neudělal sám.
Odstranění je jediný awk řádek v preflightu; komentář nad zbylým krokem to teď vysvětluje.

Mutace **jediného zbylého** blank-stripu (ten po odříznutí komentářů) zčervená hned tři
case (`attribution_then_trailing_blank_line`, `attribution_then_editor_comment_block`,
`attribution_then_scissors_and_diff`) — dokazuje, že zbylý krok je řezající, ne
neschovaný. Nový case jsem nepřidával: existující case už na tuto mutaci padají bez
jakéhokoli přetestování toho, co by druhý mechanismus (teď jediný) stejně krylo — přidání
by bylo přesně to vakuózní přetestování, které je zakázané.

### FU-C a FU-D — zapsané jako known limits, neimplementované

Do `hooks/README.md` jsem doplnil sekci „Two known limits, not addressed here" hned za
„Two prices…": `core.commentChar` neshoda mezi configem a znakem ve souboru (FU-C) a próza
*za* koncovým komentářovým blokem, čtená jako poslední odstavec zprávy (FU-D). Obojí je
formulované jako stanovený limit, ne jako omluva nebo příslib vylepšení — přesně v tónu
existující sekce o cenách.

### Regrese kola 1

Znovu jsem změřil B4/B5/B6 na reálném gitu (throwaway repozitáře, `git interpret-trailers
--parse` jako arbitr) a všechny mutace E-B5/E-10 z kola 1 na aktuálním kódu — nic
nezregredovalo (`coder-evidence.md` §6.8–6.9).

## Reference do kódu (kolo 2)

| File | Lines | Summary |
|---|---|---|
| `hooks/git/commit-msg` | 82–97 | M1: scissors od konce, přijata jen kandidátka s „čistým zbytkem" |
| `hooks/git/commit-msg` | 99–105 | M2: jediný blank-strip po odříznutí komentářů (druhý krok odstraněn) |
| `hooks/README.md` | 32–39 | Doplněná věta o scissors „čistém zbytku" |
| `hooks/README.md` | 52–58 | Nová sekce „Two known limits, not addressed here" (FU-C, FU-D) |
| `tools/checks/hook_checks.py` | 313–330 | Nový case `scissors_before_trailer_block_keeps_trailers` |

## Důkazy (kolo 2)

| Command | Result | Exit code |
|---|---|---|
| `python3 tools/checks/hook_checks.py --root .` | `hook contracts satisfied (2 shipped hook(s), 36 message case(s); committed modes checked)` | 0 |
| `python3 tools/checks/template_checks.py --root .` | `template contracts satisfied` | 0 |
| `python3 tools/intent/cli.py validate` | `5 node(s): 0 error(s), 0 warning(s)` | 0 |
| `python3 tools/intent/cli.py scope --run doc/runs/20260818-1414-commit-msg-block-boundary-4f` | `scope clean (4 declared path(s))` | 0 |
| `python3 -m unittest discover -s tools/intent/tests -t tools` | `Ran 99 tests in 0.503s — OK` | 0 |
| `ruff check tools/` | `All checks passed!` | 0 |
| `ruff format --check tools/` | `20 files already formatted` | 0 |
| FU-A na pre-fix hooku (žádná oprava) | `Intent:`/`Run:` zmizí i s attribution | — |
| FU-A na fixovaném hooku, jedna scissors řádka | `Intent:`/`Run:` přežijí, attribution pryč | — |
| FU-A na fixovaném hooku, dvě scissors řádky | vpravo umístěná (reálná) je useknuta, podvržená vlevo přežije jako text | — |
| M1 mutace (návrat na první-od-začátku, žádná kontrola zbytku) | case `scissors_before_trailer_block_keeps_trailers` padá, a jen ten | 1 |
| M2 mutace (odebrání jediného zbylého blank-stripu) | padají `attribution_then_trailing_blank_line`, `attribution_then_editor_comment_block`, `attribution_then_scissors_and_diff` | 1 |
| B4/B5/B6 regrese na reálném gitu s fixovaným hookem | jen `Intent: i0005`, žádná attribution, ve všech třech | 0 |

## Definition of Done (kolo 2)

`hook_checks.py` prochází s 36 case (35 + 1 nový pro M1) a exit 0 spolu se všemi ostatními
příkazy výše; nový case má failing-test evidence (mutace návratu ke starému algoritmu);
M2 mutace na jediném zbylém blank-stripu dokazuje, že neni mrtvý kód po odstranění
duplicitního kroku; FU-A je opravené (ne jen zdokumentované) a demonstrované na
syntetickém i dvou-scissors vstupu; FU-B rozhodnuté (odstraněno jako mrtvý kód,
s formálním důkazem i mutačním ověřením zbylého kroku); FU-C/FU-D zapsané v
`hooks/README.md` jako known limits, neimplementované; diff zůstává jen ve třech
`outputs` souborech (`hooks/git/commit-msg`, `hooks/README.md`,
`tools/checks/hook_checks.py`); žádný `git commit`/`git add` neběhl v tomto repozitáři;
strom záměru (`i0005` c1, c2) beze změny formulace. Nezapisuji `grader*` ani realization
claim — to zůstává na Coordinátorovi.

---

## Kolo 3 — revert kola 2

Adversary v kole 2 vrátil `REQUEST CHANGES` (B7, B8) — viz `review.md`, sekce „kolo 2".
Coordinátorovo rozhodnutí: žádost o kolo 2 byla chyba; kolo 1 mělo `APPROVE` bez
blokátorů a FU-A je tvar, který git sám nikdy nevyrábí. Toto kolo je **čistý revert**,
ne nový návrh.

### Co se vracelo

- **`hooks/git/commit-msg`** — scissors detekce zpátky na „první výskyt od začátku, bez
  kontroly zbytku" (kolo 1); vrácen první ze dvou odříznutí koncových blanků, které kolo
  2 odstranilo pro M2.
- **`tools/checks/hook_checks.py`** — odstraněn case `scissors_before_trailer_block_keeps_trailers`,
  který existoval jen jako pojistka pro zrušenou heuristiku. Ostatních 35 case beze
  změny.
- **`hooks/README.md`** — vrácena věta o hranici bloku na kolo-1 znění (bez zmínky o
  „čistém zbytku"). Sekce o cenách a limitech zůstává, jen rozšířená (viz níž).

### Ověření přesnosti revertu

Aktuální `hooks/git/commit-msg` jsem porovnal bajt po bajtu s verzí, kterou jsem četl na
začátku kola 2 (před jakoukoli M1/M2 úpravou) — `diff` je prázdný, `EXACT MATCH`. Detaily
a syrový výstup v `coder-evidence.md` §7.1.

### B7 — reprodukce na vráceném hooku

Reálný throwaway repozitář: soubor s `Intent: i0042` ve verzi před commitem, `git commit
-v` po úpravě téhož souboru (diff tedy obsahuje `-Intent: i0042` jako odebranou řádku).
S kolo-1 scissors detekcí (první `>8` řádka od začátku, bez ohledu na to, co je za ní) se
scissors marker najde a useká **celý** diff včetně té `-Intent:` řádky — attribution v
`git interpret-trailers --parse` chybí. Přesně scénář, který kolo 2 (heuristikou „čistý
zbytek") rozbilo, protože `-Intent:` v diffu je pro `is_key` nerozeznatelná od skutečného
traileru. Podrobný výstup v `coder-evidence.md` §7.2.

### Co jsem si nechal z kola 2

Dvě věty o FU-C/FU-D v `hooks/README.md` zůstávají — jsou to zápisy limitů, ne součást
vráceného mechanismu. Přidal jsem k nim FU-A (scissors řádka před trailerovým blokem
useká i legitimní trailery; git takový tvar sám nevyrábí) a FU-B (první ze dvou odříznutí
koncových blanků nemá vlastní izolující mutaci) ve stejném rejstříku — stanovený limit,
ne omluva.

### Definition of Done (kolo 3)

`hook_checks.py` hlásí 35 case (přesně jako po kole 1) a exit 0; `template_checks.py`,
`intent validate`, `intent scope`, `unittest discover`, `ruff check`, `ruff format
--check` — všechny exit 0; B4/B5/B6 znovu ověřené na reálném gitu ve throwaway repu bez
attribution; B7 scénář na vráceném hooku správně useká attribution. Diff zůstává jen ve
třech `outputs` souborech. Žádný `git commit`/`git add` v tomto repozitáři. Nic, co bych
při revertu našel, mě nevede k pochybnosti, že je čistý — bajtový diff proti zachycenému
kolo-1 stavu je prázdný.

---

## Kolo 4 — FU-G: oprava věty v `hooks/README.md`

Adversary schválil revert (`APPROVE`, kolo 3, bez blokátorů) a při schválení upřesnil
jednu větu v `hooks/README.md`: tvrzení „every input the first one handles, the second
one also reaches" je nepravdivé — je to přesně to tvrzení, které vyvrátilo B8 (zpráva
končící komentáři a pak koncovým blankem první odříznutí potřebuje). Přeformuloval jsem
příslušnou odrážku v sekci „Known limits, not addressed here" tak, aby tvrdila jen to, co
je pravda: na první odříznutí není žádná izolující mutace, beze slova o nadbytečnosti.
Žádný jiný soubor jsem neupravoval; `hooks/git/commit-msg` a `tools/checks/hook_checks.py`
zůstávají beze změny. `template_checks.py`, `hook_checks.py` (35 case) a `intent validate`
po opravě prošly, exit 0.
