---
run_id: 20260818-0853-harness-and-hooks-audit-86
intent_ids: ["i0001", "i0005", "i0003", "i0004", "i0002"]
role: Planner
model: claude-opus-5-thinking-high
complexity: high
status: in-progress
outputs:
  - "tools/checks/template_checks.py"
  - "tools/checks/hook_checks.py"
  - "tools/intent/tests/test_checks.py"
  - "tools/intent/tests/test_realization.py"
  - "hooks/git/commit-msg"
  - "hooks/README.md"
  - "skills/ice-review/SKILL.md"
  - "skills/ice-run/SKILL.md"
  - "rules/07-run-artifacts.mdc"
incidental:
  - "doc/intent/_realization.yaml"
---

# Plán — audit čtyř `cmd:` kontraktů a tři follow-upy

## Cíl

Prodloužit dva kontrolní skripty tak, aby čtyři věty, které dosud nekontroloval nikdo
(`i0001` c1, c2 a `i0005` c1, c2), padaly na **každém** místě, o kterém mluví: odkazy ve
druhé vrstvě skillů a v pravidlech, `.cursor` symlink mířící jinam, obě půlky odstranění
attribution, oba trailery `Intent:` i `Run:`, tělo zprávy znak za znak, a **každý** hook
pod `hooks/` včetně toho, který tam někdo přidá zítra, plus mód, se kterým hook opravdu
odchází do klonu. Kde je věta dnes nepravdivá (dvě místa v `i0005` c1, změřeno), opravuje
se **kód hooku** tak, že půlka „removes attribution" mazané trailery jen přidává (na
trailerech je nadmnožinou dneška — změřeno v A3c, ne tvrzeno) a půlka „keeps everything
else" přestává mazat prózu; žádný text kontraktu se nemění a žádná intent delta v tomto
běhu nevzniká. K tomu tři follow-upy
z předchozího běhu: FU-B (chybějící test na druhém odvozovacím místě `i0004` c12), FU-C
(jedna věta do kroku 3 `ice-review`) a FU-D (`request.md` je soubor na každé úrovni).

## Metoda auditu — co je v tabulkách změřené a co odvozené

Všechno v tabulkách níž je **změřené** na scratch kopii celého repozitáře
(`/tmp/plan-audit/repo`, včetně `.git` a `.cursor` symlinků, zelený baseline u obou
skriptů), po každé mutaci reverze; kopie je smazaná, pracovní strom jsem nezměnil.
Sloupec „padá dnes?" je exit code příkazu z `enforced_by`, ne úsudek. Kandidáty ze
`request.md` jsem bral jako začátek, ne jako seznam: šest míst níž v požadavku jmenovaných
není (nedovřená ohrada, symlink na nesprávný cíl u obou jmen, `Made-with: Cursor`, mazání
prózy, mód v gitovém indexu, hook deklarovaný v `hooks.json`).

Formát tabulek je ten, který předepisuje krok 3 `skills/ice-review/SKILL.md`: místo →
mutace → chování sady/příkazu → uzavřeno / otevřeno. Rozdíl proti Adversáři je jediný:
u nás „sada" znamená `cmd:` příkaz z `enforced_by`, protože právě jeho nedosah se auditoval.

## A1 — `i0001` c1: „Relative links inside rules and skills resolve to existing files"

Enforcer: `python3 tools/checks/template_checks.py --root .`, funkce `check_links`
(`:116-129`) a `strip_code_blocks` (`:103-113`). Plocha, na kterou dnes sahá:
`rules/*.mdc` a `skills/*/SKILL.md`.

| # | Místo, kam věta sahá | Mutace | Padá dnes? | Co s tím |
|---|---|---|---|---|
| 1 | `rules/*.mdc` — půlka „rules" | přidat `[x](../rules/does-not-exist.mdc)` do `rules/09-testing.mdc` | **ano**, `broken link: ../rules/does-not-exist.mdc`, exit 1 | uzavřeno; **ale** dnes v žádném pravidle relativní odkaz mimo ohradu není (změřeno: 0), takže tuhle půlku doteď nemohl nikdo mutovat — zafixovat testem |
| 2 | `skills/*/SKILL.md` — půlka „skills" | `../../rules/07-realization.mdc` → `-x.mdc` **v cíli odkazu**, tedy uvnitř `](…)`, ne v textu `[…]` (naivní `str.replace` přepíše jen text a check zůstane zelený — nález Kritika) | **ano**, exit 1 | uzavřeno (mutace 6 předchozích recenzí); zafixovat testem |
| 3 | druhá vrstva skillu — `skills/<s>/reference.md` | vytvořit `skills/ice-review/reference.md` s odkazem na `../../rules/nope.mdc` | **ne**, `template contracts satisfied`, exit 0 | **otevřeno** → glob na `skills/**/*.md`; `rules/00-meta-rules-and-skills.mdc:41,99` autory do těch souborů přímo posílá |
| 4 | vnořený soubor skillu — `skills/<s>/sub/examples.md` | totéž o adresář hlouběji | **ne**, exit 0 | **otevřeno** → `rglob`, ne `glob` |
| 5 | odkaz uvnitř ohrady (```) | odkaz v ohradě na neexistující soubor | ne (záměrně) | uzavřeno **rozhodnutím** — ilustrace není reference; zafixovat testem, aby to bylo rozhodnutí, ne mlčení |
| 6 | soubor s **nedovřenou** ohradou | vložit jedno osamocené ```` ``` ```` za front matter `skills/ice-run/SKILL.md` a na konec rozbitý odkaz | **ne**, exit 0 — zbytek souboru se přestane číst a nikdo se nedozví | **otevřeno** → ohlásit nedovřenou ohradu jako chybu |
| 7 | `#anchor`-only odkaz (`skills/commit-task/SKILL.md`, 2×) | — | přeskočeno (`target` je prázdný) | uzavřeno rozhodnutím; zafixovat testem |
| 8 | `http(s)://`, `mailto:` | — | přeskočeno | uzavřeno rozhodnutím; zafixovat testem |
| 9 | `[x](<cesta v lomených>)` | — | přeskočeno | uzavřeno rozhodnutím; zafixovat testem |
| 10 | odkaz na existující **adresář** | `[x](../../rules/)` | projde (`exists()`, ne `is_file()`) | uzavřeno rozhodnutím: „files" ve větě čteme jako „existující cesta", protože smysl uzlu je „a link that leads nowhere" (`i0001-harness.md:34-36`), a odkaz na adresář nikam nevede špatně; zafixovat testem, ať to není mlčení |
| 11 | `doc/runs/**`, `README.md`, `commands/*.md` | — | nekontrolováno | **mimo větu** — nejsou to rules ani skills; pokrýt je znamená **rozšířit větu**, což je rozhodnutí Humana, ne tohoto běhu (viz poslední sekce) |

## A2 — `i0001` c2: „Cursor discovers rules and skills through the .cursor symlinks"

Enforcer: tentýž skript, funkce `check_symlinks` (`:132-139`).

| # | Místo, kam věta sahá | Mutace | Padá dnes? | Co s tím |
|---|---|---|---|---|
| 12 | `.cursor/rules` chybí | odklidit symlink | **ano**, `expected a symlink…`, exit 1 | uzavřeno |
| 13 | `.cursor/skills` chybí | totéž | **ano**, exit 1 | uzavřeno (obě jména iterována týmž cyklem) |
| 14 | symlink nahrazen **skutečným adresářem** s kopií | `rm .cursor/skills && mkdir … && cp -a skills/ice-run …` | **ano**, `expected a symlink…`, exit 1 | uzavřeno — request tohle jmenoval jako podezření, měřením je to v pořádku |
| 15 | **visící** symlink | `ln -s ../skills-gone .cursor/skills` | **ano**, `symlink does not resolve to a directory`, exit 1 | uzavřeno |
| 16 | symlink mířící na **nesprávné místo** | `ln -s ../doc .cursor/rules` | **ne**, exit 0 — Cursor by načítal `doc/`, tedy nenačte ani jedno pravidlo | **otevřeno** → porovnat `link.resolve()` s `(root / name).resolve()`; platí pro obě jména |
| 17 | `.cursor/commands`, `.cursor/hooks.json` | — | nekontrolováno | **mimo větu** (jmenuje rules a skills); v tomto repozitáři `/push` a hooky přes `.cursor/` opravdu objevené nejsou — nález pro Humana, ne pro tento běh |

## A3 — `i0005` c1: „The commit-msg hook removes agent attribution and keeps everything else"

Enforcer: `python3 tools/checks/hook_checks.py --root .`, funkce
`check_commit_msg_strips_attribution` (`:44-69`) nad jedinou zprávou `SAMPLE_MESSAGE`
(`:21-29`). Věta má dvě půlky a obě jsou dnes netěsné; dvě místa jsou nepravdivá **teď**,
ne jen nedokázaná.

| # | Místo, kam věta sahá | Mutace | Padá dnes? | Co s tím |
|---|---|---|---|---|
| 18 | odstranění: stage `grep -v "Co-authored-by: Cursor"` | stage smazat | **ne**, exit 0 — druhý grep tu **stejnou** řádku odstraní taky, protože v `SAMPLE_MESSAGE` nesou oba markery jednu řádku | **otevřeno** → případ, kde je attribution jen ve jmenné formě (`Co-authored-by: Cursor <bot@example.com>`) |
| 19 | odstranění: stage `grep -v "cursoragent@cursor.com"` | stage smazat | **ne**, exit 0 — symetricky totéž | **otevřeno** → případ, kde je attribution jen v adresní formě |
| 20 | odstranění: `Made-with: Cursor` | žádná mutace není potřeba — `commands/push.md:64,87` tuhle formu **jmenuje jako attribution**, hook ji nechává | **věta je nepravdivá teď** (změřeno: řádka přežije) | **otevřeno** → hook opravit; nová podmínka pokrývá každý trailer, jehož hodnota začíná `Cursor`, tedy i `Made-with:` a `Generated-with:` |
| 21 | odstranění: velká písmena v klíči (`Co-Authored-By: Cursor <bot@example.com>`) | — | **věta je nepravdivá teď** (řádka přežije; dnešní grep je case-sensitive a adresa chybí) | **otevřeno** → `grep -i` |
| 21a | odstranění: `Cursor` jako **předpona** delšího tokenu — `Co-authored-by: CursorAgent <bot@example.com>` | — | **ano**, dnešní neukotvený substring `Co-authored-by: Cursor` řádku smaže | uzavřeno dnes; **oprava to nesmí ztratit** → hodnota se v novém výrazu porovnává jako předpona, ne jako celý token (nález Kritika, round 2) |
| 21b | totéž pro `Co-authored-by: Cursor-bot <bot@example.com>` | — | **ano** | jako 21a |
| 21c | totéž pro `Co-authored-by: CursorXYZ` (bez adresy i bez závorek) | — | **ano** | jako 21a |
| 21d | totéž pro `Co-authored-by: Cursorina Smith <c@x.com>` (člověk, jehož jméno `Cursor` začíná) | — | **ano**, dnes se smaže | uzavřeno; oprava se zachová **stejně** jako dnešek — je to cena testu nadmnožiny, ne regrese |
| 23a | zachování: **subjekt**, který slovo `Cursor` jmenuje (`docs: Cursor attribution note`) | — | zachováno dnes; **první návrh opravy ho mazal** (změřeno) | uzavřeno až opraveným výrazem: klíč musí končit na `-by`/`-with`, což `docs:` nesplňuje |
| 22 | zachování: `Intent:` | hook navíc `grep -v "^Intent: "` | **ano**, `removed content it should keep`, exit 1 | uzavřeno |
| 23 | zachování: **subjekt** | hook navíc `grep -v "^feat"` | **ano**, exit 1 | uzavřeno |
| 24 | zachování: `Run:` | hook navíc `grep -v "^Run: "` | **ne**, exit 0 — kontrola trailer `Run:` netvrdí vůbec | **otevřeno** → přesná (bajtová) rovnost celého výstupu |
| 25 | zachování: struktura těla a vnitřní prázdné řádky | hook navíc `grep -v "^$"` (zprávu slepí do jednoho bloku) | **ne**, exit 0 | **otevřeno** → bajtová rovnost; `SAMPLE_MESSAGE` navíc žádnou prózu v těle nemá, takže „everything else" se dnes měří na zprávě bez těla |
| 26 | zachování: **próza**, která attribution cituje | žádná mutace — dnešní `grep` je bez ukotvení, takže smaže i řádku těla, která adresu jen zmiňuje | **věta je nepravdivá teď** (změřeno: řádka těla zmizí) | **otevřeno** → ukotvit oba markery na trailer (řádek začínající `klíč:`); próza se přestane mazat |
| 27 | zachování: lidský spoluautor (`Co-authored-by: Ivo Example <ivo@example.com>`) | — | zachováno dnes i po opravě | uzavřeno; zafixovat případem, ať oprava tuhle půlku neposune |
| 28 | zachování: `Run:` slug obsahující slovo `cursor` | `Run: 20260818-0853-cursor-audit-86` | zachováno dnes i po opravě (hodnota nezačíná `Cursor`) | uzavřeno; zafixovat případem — je to nejtěsnější místo nové podmínky |
| 29 | odstranění trailing prázdných řádků (`awk` stage) | stage smazat | **ano**, `trailing blank lines were not trimmed`, exit 1 | uzavřeno |
| 30 | zpráva složená **jen** z attribution | vstup = jediná attribution řádka | **ne**, exit 0 — `grep -v` nevypíše nic, skončí exit 1, `&& mv` se neprovede a attribution v souboru **zůstane** | **otevřeno** → `\|\| true` + nepodmíněný `mv`; výsledkem je prázdná zpráva, kterou git sám odmítne |

## A3b — počítá se `Co-authored-by: CursorAgent` za attribution? (rozhodnuto, ne zděděno)

Kritik tuhle otázku nechal otevřenou a na odpovědi visí, jestli je oprava utažení, nebo
zúžení věty. **Rozhodnutí: ano, počítá se.** Ne z definice slova, ale ze tří textů, které
v repozitáři už jsou:

1. `commands/push.md:64-65` zakazuje `Co-authored-by: Cursor <cursoragent@cursor.com>`,
   `Made-with: Cursor` — a výslovně **„or any similar AI/Cursor trailer"**. `CursorAgent`
   je „similar Cursor trailer" v nejpřímějším možném smyslu.
2. `commands/push.md:87` dává **detekční recept**: „If the output contains
   `Co-authored-by: Cursor`, `Made-with: Cursor`, or `cursoragent@cursor.com`". Je to test
   na **substring**, a `Co-authored-by: CursorAgent <bot@example.com>` ten substring
   obsahuje. Politika repozitáře tedy takový commit už dnes posílá k `--amend`.
3. `doc/intent/nodes/i0005-git-hooks.md:28-31` říká, proč: historie má nést „the author
   who is accountable for the change rather than **the editor that typed it**". Trailer,
   jehož jméno autora začíná na `Cursor`, jmenuje editor, ne odpovědného člověka.

Důsledek pro tento běh: `CursorAgent` **musí** zůstat mazaný, takže oprava hooku je
utažení a Humana nepotřebuje. Kdyby odpověď byla „nepočítá se", byla by oprava zúžením
věty c1 a plán by se tady zastavil — nezastavuje se, protože odpověď je „počítá se".

Vedlejší, ale zapsané: `Co-authored-by: Cursorina Smith` (člověk, jehož jméno začíná na
`Cursor`) se maže dnes i po opravě. Není to nová vada — je to přesně dnešní chování a cena
za to, že se předpona porovnává jako předpona. Rozlišit člověka od agenta podle jména
hook neumí a umět nemá.

## A3c — důkaz nadmnožiny, ne tvrzení o ní

Round 1 tvrdil „na trailerech nadmnožina" a Kritik to empiricky vyvrátil. Tady je to
změřené: obě verze hooku (dnešní i opravená) jsem pustil na každou třídu zpráv, v níž se
mohou lišit, a porovnal, které řádky zmizí. `old` = dnešní hook, `new` = opravený.
Řádek je vždy vložen do trailer bloku skutečné zprávy (subjekt + tělo + trailery), aby
se měřilo chování hooku, ne artefakt izolované řádky.

| Třída | Vzorová řádka | `old` | `new` | Vztah |
|---|---|---|---|---|
| T1 attribution, jak ji Cursor vstřikuje | `Co-authored-by: Cursor <cursoragent@cursor.com>` | maže | maže | = |
| T2 `Cursor` jako **předpona** delšího tokenu | `Co-authored-by: CursorAgent <bot@example.com>` | maže | maže | = ← blokátor Kritika |
| T2 | `Co-authored-by: Cursor-bot <bot@example.com>` | maže | maže | = ← blokátor Kritika |
| T2 | `Co-authored-by: CursorXYZ` | maže | maže | = ← blokátor Kritika |
| T2 | `Co-authored-by: Cursorina Smith <c@x.com>` | maže | maže | = |
| T3 hodnota přesně `Cursor`, bez adresy | `Co-authored-by: Cursor` | maže | maže | = |
| T4 odsazený trailer | `··Co-authored-by: Cursor <x@y.com>` | maže | maže | = |
| T5 klíč velkými písmeny, bez adresy | `Co-Authored-By: Cursor <bot@example.com>` | **nechává** | maže | `new` ⊃ |
| T6 jiný klíč `-with`, bez adresy | `Made-with: Cursor` | **nechává** | maže | `new` ⊃ |
| T6 | `Generated-with: Cursor 1.2` | **nechává** | maže | `new` ⊃ |
| T7 adresa na jiném klíči `-by` | `Signed-off-by: Cursor Agent <cursoragent@cursor.com>` | maže | maže | = |
| T8 adresa na klíči bez `-by`/`-with` | `Reported-by: someone <cursoragent@cursor.com>` | maže | maže | = |
| T9 legitimní trailery | `Intent: i0005`, `Run: 20260818-0853-cursor-audit-86`, `Co-authored-by: Ivo Example <ivo@example.com>` | nechává | nechává | = |
| T10 trailer jmenující Cursor bez `-by`/`-with` a bez adresy | `Tool: Cursor`, `X-Cursor-Agent: yes` | nechává | nechává | = (známý limit, viz položka 5) |
| T11 trailer-tvarovaná řádka s adresou | `Note: mail cursoragent@cursor.com for access` | maže | maže | = |
| T12 **próza** citující trailer | `Never write Co-authored-by: Cursor by hand.` | maže | **nechává** | `new` ⊂ |
| T12 | `The hook removes Co-authored-by: Cursor <cursoragent@cursor.com> from history.` | maže | **nechává** | `new` ⊂ |
| T13 **subjekt** jmenující Cursor | `docs: Cursor attribution note`, `docs: cursor rules cleanup` | nechává | nechává | = (návrh z round 1 je **mazal**) |
| T13 | `fix: strip Co-authored-by: Cursor properly` | maže | **nechává** | `new` ⊂ |

Co z toho plyne, přesně a bez zaokrouhlení:

- **Na attribution trailerech je `new` nadmnožina `old`.** Množina „řádka je trailer,
  jehož *vlastní hodnota* jmenuje agenta Cursor (předponou jména nebo adresou)" — třídy
  T1–T8, T11 — je v `new` mazaná celá, a `old` z ní maže vlastní podmnožinu. Přírůstek je
  T5 a T6. Ani jedna třída neobsahuje řádku, kterou by `old` mazal a `new` nechal.
- **Jediné, kde `new` maže méně, jsou třídy T12 a T13**: řádky, kde marker stojí jako
  **citace uvnitř prózy** (včetně subjektu). Tam `old` maže obsah, který attribution není
  — podle `i0005-git-hooks.md:28-31` je attribution to, co Cursor **vstřikuje** jako
  trailer, ne zmínka o něm. Tohle je tedy utažení půlky „keeps everything else", ne
  oslabení půlky „removes agent attribution".
- **Rozhodovací kritérium je tím ostré**: řádka se maže právě tehdy, když je to trailer
  a jeho vlastní hodnota jmenuje Cursor. Půlka „removes" se vyhodnocuje na trailerech,
  půlka „keeps everything else" na všem ostatním, a obě jsou po opravě silnější než dnes.
- **T13 je nález round 2 nad rámec blokátoru**: výraz z round 1 mazal subjekt
  `docs: Cursor attribution note`. Opravený výraz to nedělá, protože vyžaduje klíč končící
  na `-by`/`-with`, a žádný Conventional Commit `type` ani `type(scope)` tak nekončí.

## A4 — `i0005` c2: „Every shipped hook is executable"

Enforcer: tentýž skript, funkce `check_executable` (`:32-41`) nad **pevnou dvojicí**
`("hooks/git/commit-msg", "hooks/session-start.sh")`.

| # | Místo, kam věta sahá | Mutace | Padá dnes? | Co s tím |
|---|---|---|---|---|
| 31 | `hooks/git/commit-msg` | `chmod -x` | **ano**, `not executable`, exit 1 | uzavřeno |
| 32 | `hooks/session-start.sh` | `chmod -x` | **ano**, exit 1 | uzavřeno |
| 33 | chybějící jmenovaný hook | smazat soubor | **ano**, `missing`, exit 1 | uzavřeno |
| 34 | git hook přidaný později | `hooks/git/pre-push`, `chmod 644` | **ne**, exit 0 | **otevřeno** → objevovat, ne jmenovat |
| 35 | Cursor hook přidaný později | `hooks/after-edit.sh`, `chmod 644` | **ne**, exit 0 | **otevřeno** → totéž; „every shipped hook" znamená každý soubor pod `hooks/`, který není dokumentace |
| 36 | mód, se kterým hook **odchází do klonu** | `git update-index --chmod=-x hooks/git/commit-msg` (pracovní strom zůstane 755) | **ne**, exit 0 — v klonu by hook přišel jako 644, tedy nespustitelný | **otevřeno** → porovnat i mód v gitovém indexu (100755) |
| 37 | hook deklarovaný v `hooks.json`, který neexistuje | `session-start.sh` → `session-gone.sh` v `hooks.json` | **ne**, exit 0 — Cursor by spouštěl neexistující soubor | **otevřeno** → deklarace v `hooks.json` je druhý zdroj výčtu |
| 38 | `hooks/README.md` | — | není hook | uzavřeno rozhodnutím: dokumentace (`*.md`) do výčtu nepatří; zafixovat testem |
| 39 | prázdný výčet (past objevování) | `hooks/` bez souborů | dnes neaplikovatelné (výčet je pevný) | po přechodu na objevování hrozí **vakuum**: prázdný glob projde. Proto výčet musí navíc tvrdit, že v něm **jsou** oba povinné hooky |

## Co se prodlužuje — přesné zadání pro Codera

Žádná věta kontraktu se nemění, žádný soubor pod `doc/intent/nodes/` se nemění.

### `tools/checks/template_checks.py`

1. **Plocha odkazů** (řádky 3, 4 tabulky A1). `check_links` bere
   `sorted({*(root / "rules").rglob("*.mdc"), *(root / "skills").rglob("*.md")})`.
   Vyčlenit do `link_targets(root) -> list[Path]`, ať se to dá testovat samostatně.
2. **Nedovřená ohrada** (řádek 6). `strip_code_blocks` vrací `tuple[str, bool]` — prózu
   a příznak „ohrada zůstala otevřená". `check_links` na `True` hlásí
   `"unterminated code block: links after the last fence are unchecked"`.
   Docstring řekne proč: mlčky přeskočený zbytek souboru je horší než rozbitý odkaz.
3. **Cíl symlinku** (řádek 16). V `check_symlinks` přidat třetí větev:
   `elif link.resolve() != (root / name).resolve(): findings.fail(link, f"symlink resolves to {link.resolve()}, not to {(root / name).resolve()}")`.
   Pořadí větví zůstává (chybí → nevede na adresář → vede jinam), aby hlášení bylo jedno
   na jednu příčinu.

Limity, které si Coder ověří sám: soubor má dnes 164 řádků a žádný limit `i0002`/`i0003`
na `tools/` nesahá; limity 150/250/500 se týkají `rules/*.mdc` a `SKILL.md`.

### `tools/checks/hook_checks.py`

4. **Tabulka zpráv místo jedné zprávy** (řádky 18–21, 24–28, 30). Modulová konstanta
   `CASES: tuple[Case, ...]`, kde `Case` je `frozen` dataclass `(name, message, expected)`
   a `expected` je **celý** očekávaný text výstupu, znak za znak. Kontrola pouští hook na
   každý případ zvlášť a hlásí `f"hooks/git/commit-msg: case '{case.name}': …"` s diffem
   (`difflib.unified_diff` nebo `repr` obou stran — hlavně ať je v hlášení vidět, který
   řádek přebývá nebo chybí). Případů je **čtrnáct**, jmenovitě:
   `cursor_trailer`, `cursor_agent_prefix`, `cursor_hyphen_bot`, `cursor_xyz`,
   `capitalised_key`, `made_with`, `generated_with`, `signed_off_by_agent`,
   `human_co_author`, `body_quotes_the_address`, `subject_names_cursor`,
   `run_slug_contains_cursor`, `trailing_blank_lines`, `attribution_only`.
   Pět z nich je přírůstek round 2: `cursor_agent_prefix`, `cursor_hyphen_bot` a
   `cursor_xyz` drží test nadmnožiny z A3c (dnešní hook je maže, opravený je musí mazat
   taky), `subject_names_cursor` drží subjekt, který mazal návrh z round 1, a
   `generated_with` drží druhou půlku klíčové větve `-with`. `expected` každého případu je
   změřený výstup opraveného hooku, ne odhad — hodnoty jsou v sekci Failing-test evidence.
   Bajtová rovnost dělá práci za tři dosavadní podmínky (attribution, „content it should
   keep", trailing blanks) a navíc za `Run:`, prózu a vnitřní prázdné řádky.
5. **Výčet hooků** (řádky 34, 35, 37, 38, 39). `shipped_hooks(root) -> list[Path]` =
   sjednocení
   (a) `p for p in (root / "hooks").rglob("*") if p.is_file() and p.suffix != ".md"` a
   (b) `declared_hooks(root)` — příkazy z `root/hooks.json` (`json`, stdlib), z každé cesty
   se odřízne úvodní `.cursor/` a zbytek se skládá relativně k `root`; když `hooks.json`
   není, je (b) prázdné.
   Chyba když: `hooks/` chybí; některý z `REQUIRED_HOOKS = ("hooks/git/commit-msg",
   "hooks/session-start.sh")` ve výčtu není (pojistka proti prázdnému globu); hook
   neexistuje; hook nemá `stat.S_IXUSR`.
6. **Mód v gitovém indexu** (řádek 36). `check_committed_mode(root) -> tuple[list[str], str]`:
   `git -C root rev-parse --show-toplevel` a jen když se výsledek rovná `root`, spustit
   `git -C root ls-files -s -- hooks` a pro každý **trackovaný** shipped hook porovnat mód
   s `100755`. Netrackovaný hook není chyba (ještě neodešel), ale patří do poznámky.
   Když se toplevel nerovná `root` nebo git chybí, poznámka řekne
   `"committed modes not verified: <root> is not the top of a git work tree"`.
   Degradace musí být **nahlas**: `main` tiskne při úspěchu
   `f"hook contracts satisfied ({n} shipped hook(s), {m} message case(s); {note})"`.
   Proč nahlas a ne jako chyba: repozitář se dá do projektu vendorovat bez `.git`
   (změřeno: `git -C .cursor rev-parse` tam skončí 128), a půlka o pracovním stromu běží
   vždy, takže vakuum nevzniká.

### `hooks/git/commit-msg`

7. Jeden `grep` místo dvou stagí, ukotvený na trailer, case-insensitive, bez `&&`
   (znění po opravě blokátoru round 2 — **hodnota se porovnává jako předpona**, nikoli
   jako celý token, jinak by `CursorAgent` přežil):

```bash
# Attribution is a git trailer, not prose: a `-by` / `-with` key whose value names the
# Cursor agent, or any trailer carrying its address. `Cursor` is matched as a prefix, so
# `CursorAgent` and `Cursor-bot` go too. A body line quoting such a trailer is prose and
# stays; a Conventional Commit subject never ends its key in `-by` or `-with`.
grep -viE '^[[:space:]]*[a-z][a-z0-9]*(-[a-z0-9]+)*-(by|with):[[:space:]]*cursor|^[[:space:]]*[a-z][a-z0-9-]*:.*cursoragent@cursor\.com' \
    "$msg_file" > "$msg_file.tmp" || true
mv "$msg_file.tmp" "$msg_file"
```

Dvě větve mají různě široký klíč a je to úmyslné, ne nedůslednost: jmenná větev musí klíč
omezit (`-by`/`-with`), aby nemazala subjekt ani trailer-tvarovanou prózu; adresní větev
klíč omezit **nesmí**, protože dnešní hook maže adresu na kterémkoli klíči a bez toho by
se test nadmnožiny (`Reported-by:`, `X-…:`) porušil. `awk` stage zůstává nedotčená
a dosavadní komentář `# Strip Co-authored-by: Cursor trailer …` se novým nahrazuje, ne
doplňuje — jinak nad jedním `grep`em stojí dva popisy, z nichž jeden je neúplný.

Změřeno na scratch kopii: opravený hook projde **i dnešní, nezměněnou**
`hook_checks.py` (exit 0). To je dvakrát důležité. Pro Codera to znamená, že pořadí
editací (hook vs. kontrola) nevytvoří červený mezistav. A pro tento audit je to poslední
důkaz, že dnešní enforcer je vůči téhle větě vakuózní: rozdíl mezi hookem, který
`Made-with: Cursor` maže, a hookem, který ho nechává, dnešní kontrola nepozná.

### `hooks/README.md`

8. Popis chování srovnat s novým hookem (dnes `:18-21` mluví jen o jediném traileru) a
   opravit strukturní schéma: `:9` ukazuje `hooks/hooks.json`, ale `hooks.json` leží
   v **rootu** repozitáře. Je to soubor pod `hooks/`, tedy v `code_paths` `i0005`, a
   pravidlo `01-general-programming.mdc` žádá README aktualizovat se změnou kódu.

## Proč strengthened checky drží i při montáži jako `.cursor/`

Ne úvahou — konstrukcí a měřením:

1. **Všechny cesty jsou relativní k `--root`.** Ani jedno ze šesti prodloužení nezavádí
   absolutní cestu, `git rev-parse --show-toplevel` jako *zdroj* rootu, ani konstantu
   `.cursor` v roli kotvy. Jediný výskyt `.cursor` je (a) `root / ".cursor" / name`
   v `check_symlinks`, což je vlastní `.cursor/` **šablony**, a (b) odříznutí prefixu
   `.cursor/` z deklarací v `hooks.json`, kde ten prefix stojí právě proto, že v projektu
   je šablona namontovaná na `.cursor/`.
2. **Identita symlinku je odvozená z rootu, ne z textu symlinku.** Porovnává se
   `link.resolve()` s `(root / name).resolve()`, takže výsledek nezávisí na tom, kolik
   segmentů je nad rootem. Změřeno v obou režimech na kopii: v šabloně
   (`--root .`) i v projektu (`project/.cursor/`, `--root .cursor`) je
   `link.resolve() == (root/name).resolve()` → `True` pro `rules` i `skills`.
3. **Oba skripty jsem v namontovaném layoutu spustil.** `mkdir project && cp -a repo
   project/.cursor && rm -rf project/.cursor/.git` →
   `python3 .cursor/tools/checks/template_checks.py --root .cursor` a
   `… hook_checks.py --root .cursor` → obojí exit 0. Vnitřní `.cursor/.cursor/rules`
   symlink v namontované šabloně existuje a míří na `project/.cursor/rules`, takže věta
   c2 se má o co opřít i tam.
4. **Test to drží dál**, ne jen tento plán: dva testy v `test_checks.py` staví syntetický
   root přímo v podobě `<tmp>/project/.cursor/…` — jeden čeká exit 0, druhý po odklizení
   symlinku exit 1. Ten druhý je tam proto, aby první nebyl vakuózní.
5. **Půlka o gitovém módu montáž snese**, protože submodul je vlastní work tree
   (`git -C .cursor rev-parse --show-toplevel` == `<project>/.cursor`); u vendorované
   kopie bez `.git` se toplevel nerovná rootu, půlka se neprovede a **řekne to** ve
   výstupu. Změřeno oběma směry.

## Test spec

`tools/checks/*.py` nejsou unittest moduly, jsou to skripty s `main(argv) -> int`. Jejich
chování se proto dokazuje **dvouvrstvě** a ani jedna vrstva není „spusť to a uvidíš":

- **Vrstva 1 — kontrakt.** `enforced_by` zůstává `cmd: … --root .`; Grader ho pouští nad
  skutečným repozitářem (VERIFY 4 a 5). To dokazuje, že repozitář dnes věty splňuje.
- **Vrstva 2 — dosah kontroly.** Nový modul `tools/intent/tests/test_checks.py` importuje
  `from checks import hook_checks, template_checks` a volá `main(["--root", <syntetický
  root>])`, takže se dá vyrobit **rozbitý** repozitář a čekat exit 1. Bez téhle vrstvy je
  „check padá" tvrzení jednoho běhu; s ní je to regrese, kterou zdědí každý další.

Kde ten modul žije a proč tam: `python3 -m unittest discover -s tools/intent/tests -t tools`
(VERIFY 3) je jediná discovery, kterou Grader spouští, `VERIFY.md` je soubor Humana a
`tools/intent/tests/` je `test_paths` uzlu `i0004`. Import `from checks import …` pod
`-t tools` funguje (namespace package, ověřeno spuštěním i `ruff check`), takže nový modul
nepotřebuje ani řádek ve `VERIFY.md`, ani změnu front matteru uzlu. Čistší domov
(`tools/checks/tests/` + řádek ve `VERIFY.md`) je rozhodnutí Humana — viz poslední sekce.

Pomocník v `test_checks.py`: `HarnessBuilder` staví minimální šablonu pod
`<tmp>/project/.cursor/` (`rules/00-demo.mdc` s `alwaysApply: true`, `skills/demo/SKILL.md`
s `name` a `description`, symlinky `.cursor/rules` → `../rules` a `.cursor/skills` →
`../skills`, `hooks/git/commit-msg` zkopírovaný ze skutečného repozitáře,
`hooks/session-start.sh`, `hooks.json`), metody `write`, `symlink`, `chmod`,
`run_template()` a `run_hooks()` vracející `(exit_code, stdout)`. Skutečný root si najde
jako `Path(template_checks.__file__).resolve().parents[2]` — relativně, takže to platí
i namontované. Výstup skriptů se v testech odchytává `contextlib.redirect_stdout`.

### Odkazy — `i0001` c1

| Test | Co tvrdí | Řádek A1 |
|---|---|---|
| `test_a_broken_link_in_a_rule_is_reported` | rozbitý odkaz v `rules/*.mdc` → exit 1 | 1 |
| `test_a_broken_link_in_a_skill_is_reported` | totéž v `skills/*/SKILL.md` | 2 |
| `test_a_broken_link_in_a_second_tier_skill_file_is_reported` | totéž v `skills/demo/reference.md` | 3 |
| `test_a_broken_link_in_a_nested_skill_file_is_reported` | totéž v `skills/demo/sub/examples.md` | 4 |
| `test_a_link_inside_a_fenced_block_is_not_a_reference` | rozbitý odkaz v ohradě → exit 0 | 5 |
| `test_an_unterminated_fenced_block_is_reported` | osamocená ohrada → exit 1, hlášení jmenuje soubor | 6 |
| `test_an_anchor_only_link_is_not_resolved` | `[x](#section)` → exit 0 | 7 |
| `test_an_external_link_is_not_resolved` | `https://`, `mailto:` → exit 0 | 8 |
| `test_a_bracketed_target_is_not_resolved` | `[x](<a b.md>)` → exit 0 | 9 |
| `test_a_link_to_an_existing_directory_is_accepted` | odkaz na adresář → exit 0 | 10 |

### Symlinky — `i0001` c2

| Test | Co tvrdí | Řádek A2 |
|---|---|---|
| `test_a_missing_cursor_symlink_is_reported` | `subTest` pro `rules` **i** `skills` → exit 1 | 12, 13 |
| `test_a_real_directory_in_place_of_the_symlink_is_reported` | `subTest` pro obě jména | 14 |
| `test_a_dangling_symlink_is_reported` | `subTest` pro obě jména | 15 |
| `test_a_symlink_pointing_outside_the_harness_is_reported` | `subTest` pro obě jména, cíl `../doc` | 16 |
| `test_the_checks_pass_with_the_harness_mounted_as_cursor` | syntetický `project/.cursor` → exit 0 (oba skripty) | montáž |
| `test_a_mounted_harness_still_reports_a_broken_symlink` | tentýž layout, odklizený symlink → exit 1 | montáž |

`subTest` nad dvojicí jmen je tam schválně: „rules **and** skills" je „and", a obě půlky
se testují zvlášť, i když je dnes obsluhuje jeden cyklus.

### Chování commit-msg — `i0005` c1

Testy netvrdí, co hook dělá (to tvrdí `CASES` uvnitř kontroly). Testy tvrdí, že
**kontrola pozná** hook, který jednu z půlek nesplní. Stub hook se do syntetického rootu
zapíše jako bash skript odvozený od skutečného, s jednou odebranou nebo přidanou
podmínkou.

| Test | Stub hook | Očekávání | Řádky A3 |
|---|---|---|---|
| `test_the_check_accepts_the_shipped_hook` | skutečný hook, skutečný root | exit 0 | baseline |
| `test_the_check_reports_attribution_that_survived` | `subTest` × 4: hook bez jmenné větve, bez adresní větve, bez `-i`, a „hook, který nedělá nic" | každý → exit 1, hlášení jmenuje případ | 18–21 |
| `test_the_check_reports_attribution_matched_only_as_a_whole_token` | stub s výrazem z round 1 (`cursor([[:space:]<]\|$)` místo předpony) | exit 1, a hlášení jmenuje `cursor_agent_prefix` — tenhle test je regresní pojistka testu nadmnožiny z A3c | 21a–21c |
| `test_the_check_reports_a_subject_that_was_deleted` | stub, který místo `-by`/`-with` klíče bere klíč jakýkoli (tedy maže i `docs: Cursor …`) | exit 1, hlášení jmenuje `subject_names_cursor` | 23a |
| `test_the_check_reports_a_trailer_that_was_deleted` | `subTest` × 3: stub navíc mazající `^Intent: `, `^Run: `, subjekt | každý → exit 1 | 22, 23, 24 |
| `test_the_check_reports_a_body_that_was_reflowed` | stub navíc mazající prázdné řádky | exit 1 | 25 |
| `test_the_check_reports_prose_that_was_deleted` | stub s dnešním neukotveným `grep -v "cursoragent@cursor.com"` | exit 1 | 26 |
| `test_the_check_reports_trailing_blank_lines` | stub bez `awk` stage | exit 1 | 29 |
| `test_the_check_reports_attribution_that_survived_an_all_attribution_message` | stub s `&& mv` místo `\|\| true` + `mv` | exit 1 | 30 |

Případy `human_co_author` a `run_slug_contains_cursor` (řádky 27, 28) jsou pokryté
testem `test_the_check_accepts_the_shipped_hook`: jsou v `CASES` a jejich `expected`
tu řádku obsahuje, takže hook, který by je smazal, kontrolu neprojde. Aby to nebylo
tvrzení bez řezu, přidat jeden stub navíc:
`test_the_check_reports_a_human_co_author_that_was_deleted` (stub mazající každý
`^Co-authored-by:`) → exit 1.

### Spustitelnost hooků — `i0005` c2

| Test | Co tvrdí | Řádek A4 |
|---|---|---|
| `test_the_check_reports_a_hook_that_is_not_executable` | `subTest` × 4: `hooks/git/commit-msg`, `hooks/session-start.sh`, dodaný `hooks/git/pre-push`, dodaný `hooks/after-edit.sh` | 31, 32, 34, 35 |
| `test_the_check_reports_a_required_hook_that_is_missing` | smazaný `session-start.sh` → exit 1 | 33, 39 |
| `test_documentation_under_hooks_is_not_a_shipped_hook` | `hooks/README.md` s módem 644 → exit 0 | 38 |
| `test_the_check_reports_a_hook_declared_in_hooks_json_that_is_absent` | `hooks.json` → `session-gone.sh` → exit 1 | 37 |
| `test_the_check_reports_a_committed_mode_without_the_exec_bit` | `git init` nad syntetickým rootem, `git add`, `git update-index --chmod=-x`, pracovní strom dál 755 → exit 1 | 36 |
| `test_the_committed_mode_half_says_when_it_did_not_run` | root bez `.git` → exit 0 **a** ve výstupu `not verified` | 36 (degradace) |

`git` v testech: hooky, které tenhle uzel popisuje, bez gitu nic neznamenají a celá
metodika stojí na `git diff`, takže `git` je legitimní předpoklad. Test se
**nepřeskakuje** — přeskočený test je vakuózní; když `git` chybí, test selže, a to je
pravdivá informace.

### FU-B — `i0004` c12, druhé odvozovací místo

Do `tools/intent/tests/test_realization.py`, do třídy `ConsistencyTest`:
`test_a_hand_written_coder_claim_is_reported`.

1. `claim(…, "Coordinator")` a `save_layer(layer)`.
2. V textu `layer.source` zaměnit `by: Coordinator` → `by: Coder` (tedy CLI se obejde,
   což je právě ta hrozba, kterou `check()` hlídá).
3. `reloaded = load_layer(tree.intent_dir)`, `self.assertEqual(reloaded.claim_of(node).by,
   "Coder")` — loader podpis nesanitizuje.
4. `problems = check_layer(tree, reloaded, self.policy)`; tvrdit, že některý problém
   `startswith("R6")` **a** obsahuje id uzlu, a že `problems` není prázdný (prázdnost je
   přesně to, co v `main.py:288` rozhoduje o exit code).

Postup jsem prošel na scratch kopii; vrací
`['R6 i0002: a claim may not be written by the Coder']`.

## Failing-test evidence — jedna minimální mutace na každý změněný enforcer

Adversář má tohle spustit znovu. Všechno na scratch kopii, po každé mutaci reverze.

| # | Mutace (přesná editace) | Očekávané selhání |
|---|---|---|
| E1 | `template_checks.py`: v `link_targets` vrátit `(root / "skills").glob("*/SKILL.md")` místo `rglob("*.md")` | padá `test_a_broken_link_in_a_second_tier_skill_file_is_reported` a `…_nested_…` |
| E2 | `template_checks.py`: v `link_targets` vypustit `rules` | padá `test_a_broken_link_in_a_rule_is_reported` |
| E3 | `template_checks.py`: smazat hlášení nedovřené ohrady | padá `test_an_unterminated_fenced_block_is_reported` |
| E4 | `template_checks.py`: smazat větev `link.resolve() != (root / name).resolve()` | padá `test_a_symlink_pointing_outside_the_harness_is_reported`, oba `subTest`y |
| E5 | `hook_checks.py`: vypustit z `CASES` případ `made_with` | padá `subTest` `made_with` v `test_the_check_reports_attribution_that_survived` |
| E6 | `hook_checks.py`: nahradit bajtovou rovnost dnešními substringovými podmínkami | padají `subTest`y `^Run: ` a `test_the_check_reports_a_body_that_was_reflowed` |
| E7 | `hook_checks.py`: vrátit pevnou dvojici místo `shipped_hooks` | padají `subTest`y `pre-push` a `after-edit.sh` |
| E8 | `hook_checks.py`: smazat porovnání s `100755` | padá `test_the_check_reports_a_committed_mode_without_the_exec_bit` |
| E9 | `hook_checks.py`: smazat tvrzení o `REQUIRED_HOOKS` | padá `test_the_check_reports_a_required_hook_that_is_missing` |
| E10 | `hooks/git/commit-msg`: vrátit dnešní dvě neukotvené `grep` stage | `python3 tools/checks/hook_checks.py --root .` skončí **exit 1** a jmenuje případy `made_with`, `capitalised_key`, `body_quotes_the_address`, `attribution_only` |
| E11 | `tools/intent/realization.py:480`: `== "coder"` → `== "coderx"` | padá `test_a_hand_written_coder_claim_is_reported` (dnes na téhle mutaci zůstává sada zelená — to je celý FU-B) |
| E12 | `hooks/git/commit-msg`: v jmenné větvi vrátit tokenovou kotvu `cursor([[:space:]<]\|$)` místo předpony `cursor` | `python3 tools/checks/hook_checks.py --root .` skončí **exit 1** a jmenuje `cursor_agent_prefix`, `cursor_hyphen_bot`, `cursor_xyz` — tohle je regresní pojistka testu nadmnožiny, tedy blokátoru round 2 |

E10 a E12 jsou zároveň důkaz, že oprava hooku není kosmetika a že se nedá vrátit tiše:
dnešní hook nový enforcer neprojde (E10) a ani znění z round 1 ho neprojde (E12).
Referenční chování opraveného hooku, změřené na čtrnácti zprávách, pro `expected`
v `CASES`:

```
vstup                                              výsledek opraveného hooku
Co-authored-by: Cursor <cursoragent@cursor.com>    smazáno
Co-authored-by: CursorAgent <bot@example.com>      smazáno   (round 1 by nechal)
Co-authored-by: Cursor-bot <bot@example.com>       smazáno   (round 1 by nechal)
Co-authored-by: CursorXYZ                          smazáno   (round 1 by nechal)
Co-Authored-By: Cursor <bot@example.com>           smazáno   (dnes přežije)
Made-with: Cursor                                  smazáno   (dnes přežije)
Generated-with: Cursor 1.2                         smazáno   (dnes přežije)
Signed-off-by: Cursor Agent <cursoragent@…>        smazáno
Co-authored-by: Ivo Example <ivo@example.com>      zachováno
"…the trailer Co-authored-by: Cursor <…>" v těle   zachováno (dnes se smaže)
subjekt "docs: Cursor attribution note"            zachováno (round 1 by smazal)
Run: 20260818-0853-cursor-audit-86                 zachováno
Intent: i0005 + subjekt + vnitřní prázdné řádky    zachováno, bajt za bajt
zpráva jen z attribution                           prázdný soubor (dnes attribution zůstane)
```

## FU-C — jedna věta do kroku 3 `skills/ice-review/SKILL.md`

Na konec bodu 1 kroku 3 (dnes `:47-48`), jako pokračovací řádky téže odrážky, **verbatim**:

```markdown
   Before mutating, confirm the sentence holds in that place as the code stands — by
   observation, not by the suite.
```

Znění je Adversářovo z `20260817-2334.../review.md` (Mi-1, FU-C), přebírám ho bez úprav.
Délka: 133 → 135 řádků, limit skillu 500.

## FU-D — `request.md` je soubor na každé úrovni

**Rozhodnutí: soubor.** Tři důvody, všechny z textů, které v repozitáři už jsou:

1. **Pořadí.** `skills/ice-run/SKILL.md:25-32` (krok 1) zakládá adresář běhu a píše
   `request.md` **dřív**, než krok 3 (`:50-53`) úroveň klasifikuje. Artefakt, který vzniká
   před rozhodnutím, nemůže mít formu závislou na tom rozhodnutí.
2. **Autorství.** `rules/07-run-artifacts.mdc:22` říká „`run.md` is the Coder's", zatímco
   `:28` dává `request.md` Coordinatorovi. Vložit Coordinatorův požadavek do souboru, který
   týž odstavec označí za Coderův, je přesně ta záměna, kterou předchozí běh odstranil
   u `grader.md`.
3. **Rule si dnes protiřečí sama.** `:20` dává `low` sekci `status` v `run.md`, ale `:129`
   („Write `status.md`: final state, …") a `skills/ice-run/SKILL.md:125` i `:149` mluví
   o **souboru** `status.md`. Táž nejednoznačnost, o dvě věty vedle. Řeším ji stejným
   směrem a v téže větě, protože opravit `request.md` a nechat `status.md` netěsný by byla
   ta samá past, kvůli které tento běh vznikl: věc opravená v jednom pohledu, netěsná
   v sousedním.

Nic se tím neoslabuje: `low` běh vyrábí **víc** artefaktů, ne méně, a žádný nástroj to
nerozbije (`scope.py:17` má `PLAN_FILENAMES = ("plan.md", "run.md")`,
`evidence_profile: standard` žádá `grader.md` — obojí dál platí).

### Edit 1 — `rules/07-run-artifacts.mdc`, náhrada řádků 20-22, **verbatim**

```markdown
**`low`** — `run.md` with sections plan and report, plus three files of its own:
`request.md`, `grader.md` and `status.md`. The request is written in Step 1, before the
level is known, so its form cannot depend on the level. The gate log cannot live inside
`run.md` either: `grader.md` and `status.md` belong to the Coordinator, which writes them
from commands it ran and decisions it made itself, while `run.md` carries the work.
```

Délka: 141 → 143 řádků, limit `globs` pravidla 250.

### Edit 2 — `skills/ice-run/SKILL.md`, náhrada řádku 144, **verbatim**

```markdown
- [ ] Run directory with `request.md`, `grader.md`, `status.md` and either `run.md` (low) or the full set
```

Nikde jinde se nesahá: krok 1 (`:31`), krok 9 (`:125`), položka checklistu `:149`,
`rules/07-run-artifacts.mdc:129` i tabulka `:26-37` se novou větou stávají pravdivými bez
úpravy. Ověřeno grepem: `sections: request` je v platné metodice na **jediném** místě
(`07-run-artifacts.mdc:20`). Řetězec `run.md` je na sedmi řádcích ve čtyřech souborech
(`07-run-artifacts.mdc` 4×, `skills/ice-run/SKILL.md` 1×, `tools/intent/scope.py:17`,
`tools/intent/main.py:388`) a mimo `:20-22` zůstávají všechny pravdivé — `:54`
(„`plan.md` (or `run.md`) additionally declares…") i oba výskyty v nástroji mluví o `run.md`
jako o plánovacím souboru `low` běhu, což se nemění.

## Definition of Done

Každá položka je příkaz nebo tvrzení, které spustí někdo jiný.

1. `python3 tools/intent/cli.py validate` → exit 0, `5 node(s): 0 error(s), 0 warning(s)`.
2. `python3 tools/intent/cli.py realization check` → exit 0.
3. `python3 -m unittest discover -s tools/intent/tests -t tools` → exit 0; počet testů
   vzroste z 82 (nové: `test_checks.py` + jeden v `test_realization.py`).
4. `python3 tools/checks/template_checks.py --root .` → exit 0,
   `template contracts satisfied`.
5. `python3 tools/checks/hook_checks.py --root .` → exit 0, a úvodní řádek jmenuje počet
   objevených hooků, počet případů a stav půlky o gitovém módu.
6. `python3 tools/intent/cli.py coverage` → `contracts: 28`, `machine-enforced: 28 (100%)`,
   `review exceptions: 0`, `files outside any node: 0` (žádný kontrakt nevznikl ani
   nezmizel).
7. `python3 tools/intent/cli.py scope --run doc/runs/20260818-0853-harness-and-hooks-audit-86`
   → `scope clean (10 declared path(s))` — devět `outputs` a jeden `incidental`
   (`doc/intent/_realization.yaml`, který guard povolí i tak).
8. `ruff check tools/` a `ruff format --check tools/` → exit 0.
9. **Failing-test evidence**: všech dvanáct mutací E1–E12 v `report.md` s příkazem,
   výstupem a exit codem; každá řeže právě to, co má. K tomu:
   - **Test nadmnožiny přeměřený, ne opsaný**: `report.md` obsahuje tabulku tříd z A3c,
     spuštěnou nad **oběma** verzemi hooku (dnešní z `git show HEAD:hooks/git/commit-msg`
     a opravenou z pracovního stromu), a v ní ani jeden řádek `old maže / new nechává`
     mimo třídy T12 a T13 (próza a subjekt).
10. **Montáž**: `python3 .cursor/tools/checks/template_checks.py --root .cursor` a
    `… hook_checks.py --root .cursor` nad kopií namontovanou jako `project/.cursor/`
    → obojí exit 0; a testy `test_the_checks_pass_with_the_harness_mounted_as_cursor`
    plus `test_a_mounted_harness_still_reports_a_broken_symlink` jsou v sadě zelené.
11. **Délky přeměřené, ne přečtené**: `wc -l rules/07-run-artifacts.mdc`
    `skills/ice-run/SKILL.md skills/ice-review/SKILL.md` → 143 / 156 / 135, tedy pod
    250 / 500 / 500.
12. `git diff --stat` obsahuje právě devět souborů z `outputs` (plus adresář tohoto běhu);
    nic pod `doc/intent/nodes/`, `VERIFY.md`, `AGENT_MODELS.md` ani
    `doc/intent/_policy.yaml`.
13. **Nárok až po recenzi.** `intent realization claim i0001 …` a `… claim i0005 …` píše
    **Coordinator** teprve po verdiktu `APPROVE` od Adversáře, per pravidlo, které
    repozitář přijal v předchozím běhu („claim once every gate the level requires has
    passed"). Coder nárok nezapisuje; `git diff -- doc/intent/_realization.yaml` musí být
    v okamžiku recenze prázdný.
14. `i0002`, `i0003` a `i0004` zůstávají `realized` bez nového nároku: mění se kód
    a metodický text, ne text uzlů, takže ani jeden fingerprint se nepohne
    (`realization status` → `realized` u všech tří).

## Co patří Humanovi, ne tomuto běhu

Zapsáno tak, aby to šlo naplánovat bez odvozování znovu.

1. **Rozšíření věty `i0001` c1 na `README.md`, `commands/*.md` a `doc/runs/**`** (řádek 11
   tabulky A1). Dnes rozbitý relativní odkaz v `README.md` nikdo nekontroluje. Pokrýt to
   znamená změnit **text kontraktu**, tedy intent delta — a ta v tomto běhu autorizovaná
   není.
2. **`.cursor/commands` a `.cursor/hooks.json`** (řádek 17). V šabloně samotné Cursor
   `/push` ani hooky přes `.cursor/` neobjeví, protože symlinky existují jen pro `rules`
   a `skills`. Věta c2 mluví o rules a skills, takže to není vada enforceru; je to otázka,
   jestli má věta znít šířeji.
3. **`hooks.json` nevlastní žádný uzel.** `intent owner hooks.json` → `no node owns
   hooks.json` (exit 1), zatímco `intent coverage` hlásí `files outside any node: 0`.
   Přidat `hooks.json` do `code_paths` `i0005` je intent delta; rozpor mezi `owner`
   a `coverage` je mimo rozsah rozhodnutím Humana (`doc/new_ideas/`).
4. **Domov testů kontrolních skriptů.** `test_checks.py` jde do `tools/intent/tests/`
   jen proto, že `VERIFY.md` je soubor Humana a tohle je jediná discovery, kterou Grader
   spouští. Čistší je `tools/checks/tests/` + jeden řádek ve `VERIFY.md`; obojí je
   Humanovo rozhodnutí a stojí to jednu položku v `VERIFY.md`.
5. **Attribution mimo dosah opraveného výrazu.** Opravený hook smaže trailer s klíčem na
   `-by`/`-with`, jehož hodnota začíná `Cursor`, plus každý trailer s adresou
   `cursoragent@cursor.com`. Dvě věci proto **nesmaže**, obě vědomě a obě stejné povahy:
   `Co-Authored-By: Claude <noreply@anthropic.com>` (jiný agent) a `Tool: Cursor` (klíč
   bez `-by`/`-with` a bez adresy). Ani jedna z nich se nesmaže **ani dnes**, takže to není
   regrese; je to hranice věty. `Meaning` uzlu (`i0005-git-hooks.md:28-31`) i
   `commands/push.md:64` mluví o attribution, kterou vkládá **Cursor**, a ta má formu
   trailer-u `-by`/`-with`. Kdyby to Human chtěl šířeji, je to intent delta, ne prodloužení
   kontroly.

## Změny po kritice (round 2) — co se pohnulo a co ne

Aby se to nemuselo dohledávat diffem:

- **Opraven blokátor**: jmenná větev `grep`u v sekci 7 porovnává `Cursor` jako **předponu**
  hodnoty, ne jako celý token, a klíč omezuje na `-by`/`-with`. Nová sekce A3c to dokládá
  měřením obou hooků nad třinácti třídami zpráv, v nichž se mohou lišit.
- **Rozhodnuta otevřená otázka Kritika** o `CursorAgent` (nová sekce A3b): počítá se za
  attribution, takže oprava je utažení a Humana nepotřebuje.
- **Doplněno do A3**: řádky 21a–21d (předponové formy včetně tří případů Kritika) a 23a
  (subjekt jmenující Cursor — vada round 1, kterou nikdo nenašel).
- **`CASES` z devíti na čtrnáct**, dva nové stub testy, jedna nová mutace E12, jedna nová
  položka DoD 9a.
- **`i0002` doplněno do `intent_ids`** a položka 6 z tohoto seznamu zmizela: nebyla to
  věc Humana, ale hygiena front matteru, a je vyřízená. Stejný jednoslovný doplněk patří
  do `request.md`, což je artefakt Coordinatora, nikoli Plannerův — nesahám na něj.
- **Zpřesněn recept mutace u řádku 2** tabulky A1 (nahradit cíl v `](…)`, ne text
  v `[…]`), protože Kritik na naivní variantě naměřil zeleno.
- **Nepohnulo se nic jiného**: auditovací tabulka a její verdikty closed/open, šest
  prodloužení enforcerů, domov `test_checks.py`, řešení FU-D, znění FU-C, limity souborů,
  `outputs`/`incidental` ani zbývajících pět položek pro Humana.
