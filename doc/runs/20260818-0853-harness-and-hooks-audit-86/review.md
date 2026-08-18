---
run_id: 20260818-0853-harness-and-hooks-audit-86
intent_ids: ["i0001", "i0005", "i0003", "i0004", "i0002"]
role: Adversary
model: claude-opus-5-thinking-high
complexity: high
status: in-progress
rounds: 3
---

> **Aktuální verdikt je verdikt kola 3 na konci tohoto dokumentu: REQUEST CHANGES
> a eskalace na Humana** (tři kola jsou vyčerpaná). Záznamy kol 1 a 2 zůstávají nezměněné
> jako audit. Uzavřeno: B1, B2 (kolo 1) i B3 (kolo 2). Otevřeno: jedna vada ve třech
> tvarech (B4, B5, B6) — blok se hledá nad surovým souborem, ne nad zprávou, kterou git
> nechá. `i0001` podepisuji, `i0005` c2 podepisuji, `i0005` c1 zatím ne.

# Recenze — audit čtyř `cmd:` kontraktů (round 1)

Model Codera byl `cursor-grok-4.5-high`, můj je `claude-opus-5-thinking-high` — různé, jak
`00-model-policy.mdc` žádá. Vše níž jsem měřil na scratch kopiích (`/tmp/adv86/**`,
`/tmp/audit-*`, `/tmp/mut-*`, `/tmp/probe-*`); pracovní strom jsem nezměnil kromě tohoto
souboru (kontrola na konci). Hook jsem nikdy nevolal přes `git commit`, jen na dočasných
souborech.

## Verdikt

**REQUEST CHANGES**

Dva blokátory, oba na `i0005` c1. Šest prodloužení enforcerů drží, audit je poctivý
(21 z 22 mých mutací řeže, všech dvanáct E1–E12 se reprodukuje beze zbytku, žádné místo
označené *closed* jsem falešně uzavřené nenašel) — ale půlka logiky opraveného hooku je
pro jeho vlastní enforcer neviditelná, a tvrzení o nadmnožině neplatí tak obecně, jak ho
plán, Kritik i report formulují.

## Blockers

- **B1 — enforcer nedosahuje na adresní větev hooku; slíbené uzavření řádku 19 tabulky A3
  chybí** — `tools/checks/hook_checks.py:40-125` (`CASES`), `hooks/git/commit-msg:12` —
  doplnit aspoň jeden `Case`, jehož attribution chytne **jen** adresní větev (hodnota
  nezačíná `Cursor`), např. `Reported-by: someone <cursoragent@cursor.com>` nebo
  `Note: mail cursoragent@cursor.com for access`; po doplnění musí mutace „smaž adresní
  větev" skončit exit 1.

  Reprodukce (scratch kopie repozitáře, z `hooks/git/commit-msg:12` odstraněna druhá
  alternativa `|^[[:space:]]*[a-z][a-z0-9-]*:.*cursoragent@cursor\.com`, nic jiného):

  ```
  $ python3 tools/checks/hook_checks.py --root .
  hook contracts satisfied (2 shipped hook(s), 14 message case(s); committed modes checked)
  exit_code=0
  $ python3 -m unittest discover -s tools/intent/tests -t tools
  Ran 115 tests in 9.684s
  OK
  exit_code=0
  $ printf 'feat(x): s\n\nbody\n\nIntent: i0005\nReported-by: someone <cursoragent@cursor.com>\n' > /tmp/m
  $ bash hooks/git/commit-msg /tmp/m && cat /tmp/m
  feat(x): s

  body

  Intent: i0005
  Reported-by: someone <cursoragent@cursor.com>     ← dnešní hook tuhle řádku maže
  ```

  Plán tohle místo jmenoval a slíbil uzavřít: A3 řádek 19 („odstranění: stage
  `grep -v "cursoragent@cursor.com"` … **otevřeno** → případ, kde je attribution jen
  v adresní formě"). Všech čtrnáct `CASES` ale chytí už jmenná předpona — `signed_off_by_agent`
  má hodnotu začínající `Cursor`, takže i on padne na jmenné větvi. Coder odchylku v reportu
  poctivě zapsal („Čistá jmenná větev nového regexu nestačí k pádu"), ale místo případu
  dodal stub `no_address_branch`, který emuluje **dnešní** první stage; ten padá kvůli
  `Made-with` a `capitalised_key`, tedy z jiného důvodu, než jeho jméno tvrdí. Kritérium
  kroku 3 mé metodiky („would this test fail if the sentence became false") je tím na této
  půlce nesplněné: sada i `cmd:` příkaz zůstávají zelené, i když z hooku zmizí polovina.

- **B2 — na trailerech `new` není nadmnožinou `old`: klíčová gramatika nového výrazu je
  užší než gramatika gitového traileru** — `hooks/git/commit-msg:12` — buď obě větve
  rozšířit na token, který za trailer považuje git (včetně nepovinné mezery před
  dvojtečkou), nebo tu hranici nechat rozhodnout Humanovi a **přestat tvrdit nadmnožinu**.

  Čtyři řádky, které dnešní hook maže a nový nechává, mimo autorizované třídy T12/T13
  (próza a subjekt). První dvě čte jako trailer sám git:

  | Řádka | `git interpret-trailers --parse` | `old` | `new` |
  |---|---|---|---|
  | `Co-authored-by : Cursor <cursoragent@cursor.com>` | **ano**, normalizuje na `Co-authored-by: Cursor <cursoragent@cursor.com>` | maže | **nechává** |
  | `2fa-note: cursoragent@cursor.com` | **ano** | maže | **nechává** |
  | `Co_authored_by: Cursor <cursoragent@cursor.com>` | ne | maže | **nechává** |
  | `co.authored.by: cursoragent@cursor.com` | ne | maže | **nechává** |

  Reprodukce první řádky (nejtvrdší z nich — git ji čte jako přesně tu attribution, kterou
  Cursor vstřikuje):

  ```
  $ git show HEAD:hooks/git/commit-msg > /tmp/old-hook
  $ printf 'feat(x): s\n\nbody\n\nIntent: i0005\nCo-authored-by : Cursor <cursoragent@cursor.com>\n' > /tmp/b2
  $ cp /tmp/b2 /tmp/b2.old
  $ bash /tmp/old-hook /tmp/b2.old && tail -1 /tmp/b2.old
  Intent: i0005                                      ← attribution smazána
  $ bash hooks/git/commit-msg /tmp/b2 && tail -1 /tmp/b2
  Co-authored-by : Cursor <cursoragent@cursor.com>    ← attribution přežila
  ```

  Příčina: jmenná větev žádá `[a-z][a-z0-9]*(-[a-z0-9]+)*-(by|with):` a adresní
  `[a-z][a-z0-9-]*:` — obě odmítají klíč začínající číslicí, klíč s podtržítkem či tečkou
  a jakoukoli mezeru před dvojtečkou, zatímco `old` maže **kdekoli na řádce**. Tvrzení
  A3c („Ani jedna třída neobsahuje řádku, kterou by `old` mazal a `new` nechal") je pravdivé
  pro dvacet čtyři měřených řádek — přeměřil jsem je všechny a souhlasí — ale závěr
  „rozhodovací kritérium je tím ostré: řádka se maže právě tehdy, když je to trailer a jeho
  vlastní hodnota jmenuje Cursor" obecně neplatí, a právě tenhle závěr je to, na co se
  Human při uzavírání verze spoléhá. Formy, které Cursor skutečně vstřikuje, mažou obě
  verze; blokátor je ve **tvrzení o dosahu**, ne v každodenním provozu.

## Major

- **M1 — nový hook maže obsah, který dnešní nechává, i mimo dokumentovaný `Cursorina
  Smith`** — `hooks/git/commit-msg:12`. Zmizí každý trailer s klíčem na `-by`/`-with`,
  jehož hodnota jen *začíná* na „cursor". Změřeno (vlevo dnešek, vpravo po opravě):

  ```
  Reviewed-by: Cursory glance at the diff        keep → DEL
  Fixed-by: Cursory reading of the spec          keep → DEL
  Made-with: cursory care                        keep → DEL
  Tested-with: Cursor-free toolchain             keep → DEL
  Reported-by: Cursor Smith <smith@example.com>  keep → DEL
  ```

  Ani jeden `Case` tuhle mez nedrží, takže se dá tiše rozšířit i zúžit. Rozhodnutí A3b
  (předpona místo tokenu) beru a souhlasím s ním — tokenová kotva vrací blokátor Kritika
  z round 1 — ale plán dokládá cenu jen na klíči `Co-authored-by:`, a `i0005-git-hooks.md:37-39`
  přitom jmenuje právě tuhle vadu („Half of that is easy to satisfy by deleting too much").
  Chce to případ, který cenu zapíše jako **záměr** (řádka, kterou hook mazat má, i když
  attribution není), nebo rozhodnutí Humana.

- **M2 — `hooks.json` s příkazem, který nese argument, vyrobí falešnou chybu** —
  `tools/checks/hook_checks.py:128-142`. `declared_hooks` čte celý `command` jako cestu:

  ```
  $ # hooks.json: "command": "bash .cursor/hooks/session-start.sh"
  $ python3 tools/checks/hook_checks.py --root .
  ERROR bash .cursor/hooks/session-start.sh: missing
  exit_code=1
  ```

  Šablona se vendoruje; první projekt, který si do `hooks.json` napíše interpretr, dostane
  červený `i0005` c2 s bezvadnými hooky. Dnešní `hooks.json` je bare cesta, takže enforcer
  na tomto repozitáři nelže — proto Major, ne blokátor.

- **M3 — `check_committed_mode` neošetřuje `relative_to`, na rozdíl od `check_executable`** —
  `tools/checks/hook_checks.py:274`. `hooks.json` s absolutním příkazem (`/bin/sh`) skončí
  tracebackem `ValueError: '/bin/sh' is not in the subpath of …` místo hlášení. Selhává
  bezpečným směrem (exit 1), ale chová se to jako pád nástroje, ne jako nález.

## Minor / non-blocking

- **Mi1 — druhé odvozovací místo módové půlky.** `git ls-files -s -- hooks`
  (`hook_checks.py:252`) je užší než výčet `shipped_hooks()`. Hook deklarovaný
  v `hooks.json` **mimo** `hooks/`, commitnutý jako `100644` a v pracovním stromu `755`,
  projde a hlásí se jako „untracked" (změřeno: `session-extra.sh untracked`, exit 0);
  tentýž soubor v `hooks/` je zachycen (exit 1). Follow-up pro pozdější běh — plán tuhle
  scope sám předepsal a takový hook dnes neexistuje.
- **Mi2** — poznámka o netrackovaných hookách zdvojuje slovo:
  `committed modes checked (hooks/git/pre-push untracked untracked)` (`hook_checks.py:276,283`).
- **Mi3** — `_BASE` a `_CLEAN` (`hook_checks.py:29-30`) jsou znak za znak totožné konstanty;
  dvě jména pro jeden řetězec svádí ke čtení, že se liší.
- **Mi4** — `strip_code_blocks` přepíná stav na každé značce začínající ```` ``` ````, takže
  legitimní vnořená ohrada `````` ```` `````` by hlásila nedovřenou ohradu. Dnes takový
  soubor v `rules/` ani `skills/` není.
- **Mi5** — `skills/` nekontroluje jiné přípony než `.md`; odkaz v `skills/x/notes.txt` je
  neviděn. Souhlasím, že je to mimo větu („rules and skills" čteno jako Markdown), ale je
  to mlčení, ne rozhodnutí zafixované testem.

## Kde věty dosahují

Kompletní výčet míst, která diff může učinit nepravdivými, plus všechna, jež běh označuje
za uzavřená. „Sada" = `python3 -m unittest discover -s tools/intent/tests -t tools`,
„cmd" = příkaz z `enforced_by`.

### `i0001` c1 — „Relative links inside rules and skills resolve to existing files"

| # | Místo | Mutace | Sada / cmd | Stav |
|---|---|---|---|---|
| 1 | `rules/*.mdc` | rozbitý odkaz; a `link_targets` bez `rules` (E2) | exit 1; padá `test_a_broken_link_in_a_rule_is_reported` | closed |
| 2 | `skills/*/SKILL.md` | rozbitý cíl v `](…)` | exit 1 | closed |
| 3 | `skills/<s>/reference.md` | rozbitý odkaz; `rglob`→`glob` (E1) | exit 1; padá `…second_tier…` | closed |
| 4 | `skills/<s>/sub/examples.md` | totéž o úroveň hlouběji (E1) | exit 1; padá `…nested…` | closed |
| 5 | `rules/<sub>/*.mdc` (podadresář pravidel) | rozbitý odkaz | exit 1 | closed (mé měření, plán neuvádí) |
| 6 | odkaz v ohradě | rozbitý odkaz v ohradě | exit 0 | closed rozhodnutím + test |
| 7 | nedovřená ohrada | smazat hlášení (E3); `inside`→`False` (X9) | exit 1; padá `…unterminated…` | closed |
| 8 | `#anchor`, `http(s)`, `mailto:`, `[x](<…>)`, odkaz na adresář | vložit každou formu | exit 0 | closed rozhodnutím + testy |
| 9 | odkaz na visící symlink | cíl `dangling.md` → nikam | exit 1 | closed (mé měření) |
| 10 | výčet cílů jako celek | `link_targets` vrací `[]` (X10) | padají čtyři odkazové testy | closed |
| 11 | `README.md`, `commands/*.md`, `doc/runs/**` | rozbitý relativní odkaz | exit 0 | **open — mimo větu, Human (položka 1)** |
| 12 | `skills/**/*.txt` a jiné nemarkdownové soubory | rozbitý odkaz | exit 0 | **open — mimo větu, mlčením (Mi5)** |

### `i0001` c2 — „Cursor discovers rules and skills through the .cursor symlinks"

| # | Místo | Mutace | Sada / cmd | Stav |
|---|---|---|---|---|
| 13 | `.cursor/rules` chybí | odklidit | exit 1 | closed |
| 14 | `.cursor/skills` chybí | odklidit | exit 1 | closed |
| 15 | symlink → skutečný adresář s kopií | `rm` + `mkdir` + `cp -a` | exit 1 | closed |
| 16 | visící symlink | cíl `../skills-gone` | exit 1 | closed |
| 17 | symlink mimo šablonu, `rules` | `../doc`; a smazat větev identity (E4) | exit 1; padá `…pointing_outside…` (oba `subTest`y) | closed |
| 18 | symlink mimo šablonu, `skills` | `../doc` | exit 1 | closed |
| 19 | ekvivalentní nepřímá cesta (`./../rules`) | přesměrovat symlink | exit 0 (správně) | closed |
| 20 | namontovaná šablona `project/.cursor` | postavil jsem ji sám, oba skripty | exit 0; po odklizení symlinku exit 1 | closed |
| 21 | `.cursor/commands`, `.cursor/hooks.json` | — | nekontrolováno | **open — mimo větu, Human (položka 2)** |

### `i0005` c1 — „The commit-msg hook removes agent attribution and keeps everything else"

| # | Místo | Mutace | Sada / cmd | Stav |
|---|---|---|---|---|
| 22 | jmenná větev `grep`u | odstranit ji (X2) | cmd exit 1, šest případů | closed |
| 23 | **adresní větev `grep`u** | odstranit ji (X1) | **cmd exit 0, sada zelená** | **open — B1** |
| 24 | předpona `Cursor` delšího tokenu (`CursorAgent`, `Cursor-bot`, `CursorXYZ`) | tokenová kotva round 1 (E12) | cmd exit 1, tři případy | closed |
| 25 | `|| true` + nepodmíněný `mv` (zpráva jen z attribution) | vrátit `&& mv` (X3) | cmd exit 1, `attribution_only` | closed |
| 26 | `awk` stage (trailing prázdné řádky) | odstranit ji (X4) | cmd exit 1, devět případů | closed |
| 27 | bajtová rovnost (`Run:`, tělo, vnitřní prázdné řádky) | vrátit substringové podmínky (E6) | padá pět testů | closed |
| 28 | `Made-with` / `Generated-with` / velká písmena v klíči | vypustit `made_with` z `CASES` (E5); vrátit dnešní hook (E10) | padá `subTest made_with`; cmd exit 1 | closed |
| 29 | próza citující trailer (T12) | dnešní neukotvený `grep` jako stub | exit 1 | closed |
| 30 | subjekt jmenující Cursor (T13) | stub s klíčem bez `-by`/`-with` | exit 1, `subject_names_cursor` | closed |
| 31 | lidský spoluautor, `Run:` slug s „cursor" | stub mazající `^Co-authored-by:` | exit 1 | closed |
| 32 | odsazení, `Co-authored-by:Cursor`, dvě mezery, CRLF, zpráva bez trailer bloku | přeměřeno oběma hooky | shodné chování | closed |
| 33 | **klíč mimo gramatiku výrazu, hodnota jmenuje agenta** (`Co-authored-by :`, `2fa-note:`, `Co_authored_by:`, `co.authored.by:`) | vložit řádku | cmd exit 0, sada zelená | **open — B2** |
| 34 | **`-by`/`-with` klíč, jehož hodnota jen začíná na „cursor" a agentem není** (`Reviewed-by: Cursory …`) | vložit řádku | cmd exit 0, sada zelená | **open — M1** |
| 35 | attribution jiného agenta (`Co-Authored-By: Claude …`), `Tool: Cursor` | — | nemaže dnes ani po opravě | **open — mimo větu, Human (položka 5)** |

### `i0005` c2 — „Every shipped hook is executable"

| # | Místo | Mutace | Sada / cmd | Stav |
|---|---|---|---|---|
| 36 | `hooks/git/commit-msg`, `hooks/session-start.sh` v pracovním stromu | `chmod 644`; a smazat test bitu (X8) | exit 1; padá `…not_executable` | closed |
| 37 | hook přidaný později do `hooks/git/`, do `hooks/`, do **nového podadresáře** | přidat jako 644; `rglob`→`glob` (X6) | exit 1 ve všech třech; padá pět testů | closed |
| 38 | chybějící povinný hook / prázdný `hooks/` (vakuum objevování) | smazat soubor; vyprázdnit adresář; smazat `REQUIRED_HOOKS` (E9) | exit 1; padá `…required_hook_that_is_missing` | closed |
| 39 | `hooks/` úplně chybí | smazat adresář | exit 1 (`hooks/: missing`) | closed |
| 40 | `hooks/README.md` (dokumentace) | mód 644 | exit 0 | closed rozhodnutím + test |
| 41 | hook deklarovaný v `hooks.json`, který neexistuje / není spustitelný | přejmenovat cíl; ukázat na 644 soubor; vypustit `declared_hooks` (X5) | exit 1; padá `…declared_in_hooks_json…` | closed |
| 42 | mód v gitovém indexu (`100644`), pracovní strom 755 | `update-index --chmod=-x` na obou hookách; smazat porovnání (E8); vypnout půlku (X7) | exit 1; padá `…committed_mode…` | closed |
| 43 | degradace bez `.git` (vendorovaná kopie) | montáž bez `.git` | exit 0 **a** „not verified" ve výstupu | closed |
| 44 | montáž jako submodul (s `.git`) | `--root .cursor` v `project/` | půlka běží; 644 v indexu → exit 1 | closed |
| 45 | netrackovaný, ale spustitelný hook | přidat 755, necommitovat | exit 0 + poznámka | closed rozhodnutím |
| 46 | **hook deklarovaný mimo `hooks/`, v indexu 100644** | `ls-files -- hooks` ho nevidí | cmd exit 0, hlásí „untracked" | **open — Mi1** |
| 47 | `hooks.json` s argumentem / absolutní cestou | změnit `command` | falešné „missing" / `ValueError` | **open — M2, M3** |

### `i0004` c12 (FU-B) a metodické texty (FU-C, FU-D)

| # | Místo | Mutace | Sada | Stav |
|---|---|---|---|---|
| 48 | `claim()` v `realization.py` | (pokryto dřív) | červená | closed |
| 49 | `R6` v `check()` — druhé odvozovací místo | `== "coder"` → `== "coderx"` (E11) | padá `test_a_hand_written_coder_claim_is_reported` | closed |
| 50 | FU-C věta v `skills/ice-review/SKILL.md:48-49` | srovnáno s plánem | verbatim, 135 řádků | closed |
| 51 | FU-D: `rules/07-run-artifacts.mdc:20-24`, `skills/ice-run/SKILL.md:144` | grep na `run.md`, `request.md`, `status.md`, „low" | žádné místo neříká `low` jinak; 143 a 156 řádků | closed |
| 52 | FU-D vs. `_policy.yaml` | `evidence_profile: standard` → `_evidence_problems` žádá adresář s `grader.md` | `low` běh `grader.md` dál vyrábí; `_policy.yaml` bez diffu | closed |

## Co jsem si ověřil sám

| Příkaz / měření | Výsledek | Exit |
|---|---|---|
| `python3 tools/intent/cli.py validate` | `5 node(s): 0 error(s), 0 warning(s)` | 0 |
| `python3 tools/intent/cli.py coverage` | `contracts: 28`, `machine-enforced: 28 (100%)`, `files outside any node: 0` | 0 |
| `python3 tools/intent/cli.py scope --run doc/runs/20260818-0853-harness-and-hooks-audit-86` | `scope clean (10 declared path(s))` | 0 |
| `python3 tools/intent/cli.py realization check` | `realization layer consistent (3 entry/entries)` | 0 |
| `python3 tools/intent/cli.py realization status` | `i0001` a `i0005` `not_claimed` — nárok nepředběhl recenzi | 0 |
| `git diff -- doc/intent/_realization.yaml` | prázdný | — |
| `git diff --stat doc/intent/_policy.yaml`, `VERIFY.md`, `AGENT_MODELS.md`, `doc/intent/nodes/` | prázdné | — |
| suita v pracovním stromu / na `HEAD` | 115 / **82** testů, obojí OK | 0 |
| oba enforcery na `HEAD` i v pracovním stromu | exit 0 | 0 |
| dnešní `hook_checks.py` nad **opraveným** hookem | `hook contracts satisfied` → dnešní enforcer ty dva hooky nerozliší (vakuum potvrzeno) | 0 |
| dnešní hook nad zprávou jen z attribution | attribution zůstane → řádek 30 tabulky A3 potvrzen | — |
| 22 mutací enforcerů (E1–E12 + 10 vlastních) | 21 řeže; jediná mlčící je X1 = B1 | — |
| 23 mutací tabulky A1/A2 (včetně všech *closed* řádků) | žádný falešný *closed*; všechny verdikty souhlasí | — |
| 14 mutací tabulky A4 + pět montážních scénářů | žádný falešný *closed* | — |
| nadmnožina: 53 kandidátních řádek × 6 tvarů zprávy, oba hooky | 60 případů `old maže / new nechává` ve 12 třídách: 5 tříd je próza/subjekt (T12/T13, autorizováno), **7 tříd má tvar `klíč: hodnota` s adresou nebo jménem agenta (B2)**, z nich 2 bere za trailer sám git | — |
| `git interpret-trailers --parse` jako arbitr trailerovosti | `Co-authored-by :` i `2fa-note:` jsou trailery | — |
| A3c tabulka Codera (24 řádek) | přeměřena řádek po řádku, **souhlasí beze zbytku** | — |
| tři odchylky reportu | všechny tři přeměřeny a **zapsané pravdivě** (viz níž) | — |
| `wc -l` na třech textových souborech | 143 / 156 / 135 | — |
| `git status --short` na konci | shodný se stavem na začátku + tento `review.md` | — |

### Tři odchylky, které Coder ohlásil

Všechny tři jsou popsané přesně; ani jedna není zamlčená ani nadsazená.

1. **Stub `no_address_branch`** — Coder tvrdí, že jmenná větev sama by test nechala zeleným.
   Přeměřeno (X1): pravda, a je to přesně blokátor B1. Odchylka je poctivá, ale její důsledek
   měl vést k novému `Case`, ne k jinému stubu.
2. **Stub / E5 `made_with`** — tvrzení, že stub musí nechávat *jen* `Made-with`, jinak by
   E5 nepadal. Přeměřeno: E5 padá na `test_the_check_reports_attribution_that_survived`, a
   kdyby stub vypouštěl celou `-with` větev, držel by ho `generated_with`. Správně.
3. **Verbatim FU-C/FU-D** — „sedí, žádná odchylka". Srovnal jsem znak za znak s `plan.md:493-496`
   a `:526-530`, `:538`. Souhlasí.

## Podepsal bych, že `i0001` a `i0005` jsou dokázané?

- **`i0001` c1 a c2 — ano.** Přeměřil jsem všech dvanáct míst c1 a devět míst c2 z tabulky
  výše, včetně každého, které předchozí audity označily za *closed*, a včetně druhé vrstvy
  skillů, nedovřené ohrady, symlinku mířícího jinam a namontovaného layoutu. Otevřené zůstává jen to, co plán správně dává Humanovi
  (`README.md`, `commands/*.md`, `doc/runs/**`, `.cursor/commands`, `.cursor/hooks.json`) —
  a to jsou hranice **věty**, ne děravý enforcer.
- **`i0005` c2 — ano, s jednou výhradou.** „Every shipped hook" je teď opravdu objevování
  (mé mutace to potvrdily i pro hook v novém podadresáři), vakuum prázdného globu je
  ohrazené `REQUIRED_HOOKS`, mód v indexu se kontroluje a bez `.git` to nahlas přizná.
  Výhrada je Mi1/M2/M3: výčet a `ls-files` scope se rozcházejí a `hooks.json` s argumentem
  nebo absolutní cestou enforcer rozbije. Žádná z nich nedělá dnešní tvrzení nepravdivým.
- **`i0005` c1 — ne, ne dnes.** Půlka „removes agent attribution" se dá z hooku odstranit
  do poloviny a nikdo si toho nevšimne (B1), a tvrzení o nadmnožině, na které stojí
  argument, že oprava je utažení bez intent delty, neplatí obecně (B2). Obě věci jsou malé
  opravy — jeden `Case` a jedna úprava klíčové gramatiky — ale dokud nejsou hotové,
  podepsal bych jen to, že hook zvládá čtrnáct pojmenovaných zpráv, ne že „odstraňuje
  attribution a zachovává všechno ostatní".

**Co by čtenář po tomto běhu neměl předpokládat.** Že `cmd:` enforcer `i0005` c1 rozhoduje
o libovolné zprávě — rozhoduje o čtrnácti, a jejich seznam je celý obsah kontraktu; že
oprava hooku maže nadmnožinu dneška (na trailerech mimo gramatiku klíče a v próze nemaže);
že hook rozliší agenta od člověka nebo od anglického slova, které začíná na „cursor"
(nerozliší — `Reviewed-by: Cursory glance` zmizí); že kontrola módu vidí hooky mimo
`hooks/`; a že „every shipped hook" pokrývá i hooky, které Cursor spouští přes
`.cursor/commands` nebo `.cursor/hooks.json` (o těch věta c2 nemluví).

Kolo 1 ze tří. Po opravě B1 a B2 stačí přeměřit body 23 a 33 tabulky výše; ostatní řádky
jsou uzavřené a znovu je otevírat nebudu.

---

# Recenze — kolo 2

Měřeno znovu na scratch kopiích (`/tmp/adv86/**`, `/tmp/mut2-*`, `/tmp/audit-*`,
`/tmp/probe-*`, `/tmp/adv86/p5`); pracovní strom jsem nezměnil kromě tohoto souboru, hook
jsem volal jen na dočasných souborech, `git commit` ani jednou. Arbitrem trailerovosti je
`git interpret-trailers --parse`, stejně jako v kole 1.

## Verdikt

**REQUEST CHANGES**

Oba blokátory z kola 1 jsou opravené a **přeměřené**, ne odkývané. Zůstává jeden nový
blokátor téhož druhu: gramatika je teď dost široká na klíče, ale ne na **skládaný
(folded) trailer**, a právě tam nový hook nechává celou attribution, kterou dnešní hook
odstraňuje. Je to poslední položka; devět follow-upů níž jsou piles, ne blokátory.

## Co je z kola 1 uzavřené

- **B1 — adresní větev je konečně pokrytá.** E13 (smazání adresní alternativy z hooku):
  `python3 tools/checks/hook_checks.py --root .` → exit 1 a jmenuje
  `address_only_trailer`, `digit_key_address`, `underscore_key_address`, `dot_key_address`.
  Symetricky X2r2 (smazání jmenné alternativy) → exit 1 a šest jiných případů. Stub
  `no_address_branch` je teď skutečná jmenná větev a test na něm tvrdí přítomnost
  `address_only_trailer` ve výstupu (`test_checks.py:302-306,332-333`), takže padá z
  adresního důvodu, ne náhodou. Mutace, která v kole 1 mlčela (X1), dnes řeže.
- **B2 — všechny čtyři řádky mažou obě verze hooku.** Přeměřeno:
  `Co-authored-by : Cursor <cursoragent@cursor.com>`, `2fa-note: cursoragent@cursor.com`,
  `Co_authored_by: Cursor <cursoragent@cursor.com>`, `co.authored.by: cursoragent@cursor.com`
  → `old` maže, `new` maže. E14 (návrat úzké gramatiky) → exit 1 a jmenuje
  `space_before_colon` + tři klíčové případy; X12 (odebrání nepovinné mezery před
  dvojtečkou v obou větvích) → exit 1 a jmenuje `space_before_colon`. Klíčová třída
  `[a-z0-9-][a-z0-9-]*` už pokrývá celý token, který git za klíč traileru přijímá
  (alnum + pomlčka), a adresní větev navíc `_` a `.`, což je nadmnožina.
- **Major (cena předpony) je dokumentovaný pravdivě.** Neposuzoval jsem to čtením:
  změřil jsem všechny čtyři jmenované příklady a všechny čtyři se opravdu chovají, jak
  komentář hooku a `hooks/README.md` tvrdí — `old` je nechává, `new` je maže:

  ```
  Reviewed-by: Cursory glance at the diff        keep → DEL
  Made-with: cursory care                       keep → DEL
  Reported-by: Cursor Smith <smith@example.com> keep → DEL
  Tested-with: Cursor-free toolchain            keep → DEL
  ```

  Navíc jsem si ověřil, že popis je **úplný v druhu**, ne jen v příkladech: všech 39 tříd,
  kde `new` maže víc než `old`, spadá pod jedno ze dvou dokumentovaných pravidel (klíč na
  `-by`/`-with` s hodnotou začínající „cursor"; trailer-tvarovaný klíč s adresou). Žádná
  třída mimo ně. Regex se nezúžil — ověřeno diffem.

## Blockers

- **B3 — skládaný (folded) attribution trailer přežije celý; dnešní hook z něj agenta
  odstraňuje** — `hooks/git/commit-msg:16` — buď adresní/jmennou větev rozšířit na
  pokračovací řádku (řádka začínající mezerou/tabem, která nese adresu nebo jméno agenta),
  **nebo** — a to je legitimní a levnější — nechat Humana zapsat, že věta c1 mluví
  o nesložených trailerech, jaké Cursor vstřikuje, a přidat `Case`, který dnešní chování
  ukotví, ať se nedá tiše změnit. Redesign hooku nežádám.

  Git tuhle formu skládá na **přesně tu attribution, kterou Cursor vstřikuje**:

  ```
  $ git show HEAD:hooks/git/commit-msg > /tmp/old-hook
  $ printf 'feat(x): subject\n\nReason: body.\n\nIntent: i0005\nCo-authored-by:\n  Cursor <cursoragent@cursor.com>\n' > /tmp/fold
  $ cp /tmp/fold /tmp/fold.old
  $ bash /tmp/old-hook /tmp/fold.old && git interpret-trailers --parse < /tmp/fold.old
  Intent: i0005
  Co-authored-by:                                    ← hodnota prázdná: agent i adresa zmizeli
  $ bash hooks/git/commit-msg /tmp/fold && git interpret-trailers --parse < /tmp/fold
  Intent: i0005
  Co-authored-by: Cursor <cursoragent@cursor.com>    ← attribution beze změny
  ```

  Čtyři varianty, všechny čtyři git skládá na kanonický `Co-authored-by: Cursor
  <cursoragent@cursor.com>`, u všech čtyř `old` maže nosnou řádku a `new` nechává:

  | Forma | Nosná řádka |
  |---|---|
  | `Co-authored-by:` + odsazená pokračovací řádka | `··Cursor <cursoragent@cursor.com>` |
  | totéž s tabem | `→Cursor <cursoragent@cursor.com>` |
  | jméno na prvním řádku, adresa na pokračovacím | `··<cursoragent@cursor.com>` |
  | mezera před dvojtečkou + pokračovací řádka | `··Cursor <cursoragent@cursor.com>` |

  Proč to považuji za blokátor, a ne za follow-up, i když Cursor takovou formu nevstřikuje:
  je to **regrese zavedená tímto během** (dnešní hook identifikující obsah odstraní, nový
  nechá celý trailer), je to půlka „removes agent attribution", ne půlka „keeps everything
  else", `git` sám tu řádku čte jako attribution — a report kola 2 znovu tvrdí „no
  `old removes / new keeps` outside T12/T13", což pro tuhle třídu neplatí. Přesně tímto
  standardem jsem v kole 1 blokoval B2, kde byly příklady umělejší (`2fa-note:` je můj
  vymyšlený klíč, tohle git normalizuje na to, co Cursor opravdu posílá). Držím stejné
  měřítko oběma směry.

## Follow-upy — s pilou, k naplánování bez odvozování

Každý je napsaný tak, že se dá vzít do dalšího běhu jak stojí.

### `i0005` c1

- **FU-1 — jmenná větev nemá ukotvenou toleranci mezery před dvojtečkou.** Mutace E14b
  (zúžím **jen** jmennou větev na znění z kola 1, adresní nechám širokou):
  `hook_checks.py --root .` → **exit 0**, sada zelená. Případ `space_before_colon` totiž
  nese adresu, takže ho zachytí adresní větev, i když jmenná selže. Věta tím nepřestává
  platit — dnešní hook `Made-with : Cursor` maže (změřeno; git ji čte jako
  `Made-with: Cursor`) — chybí jen řez. **Pila:** jeden `Case` s hodnotou bez adresy,
  např. `Made-with : Cursor`, a E14b začne řezat.
- **FU-2 — řádky s adresou, které git za trailer nepovažuje, teď přežívají.** Změřeno:
  `Co-authored by: Cursor <cursoragent@cursor.com>` (mezera **uvnitř** klíče), `x+by:`,
  `x/by:`, `x#by:` — u všech `old` maže, `new` nechává, a `git interpret-trailers --parse`
  je za trailer **nepovažuje**. Podle kritéria, které tento běh přijal („attribution je
  trailer, ne próza"), je to tedy autorizované utažení půlky „keeps everything else",
  ne vada — patří do stejné třídy jako T12. Zapisuji to jako follow-up, protože je to dnes
  **mlčení**: žádný případ to nedrží, takže se to dá obojím směrem tiše změnit. Zpětně
  přiznávám, že v kole 1 jsem do B2 zabalil i tři takové ne-trailerové klíče
  (`Co_authored_by:`, `co.authored.by:`, `X_Custom:`); Coder je opravil taky, což neškodí
  (maže se víc), ale blokovat je nebylo nutné. **Pila:** jeden `Case`, který drží, že
  ne-trailerová řádka s adresou zůstává.
- **FU-3 — cena předpony je dokumentovaná, ale ne ukotvená.** Komentář hooku a
  `hooks/README.md` ji popisují pravdivě (změřeno výše), žádný `Case` ji ale netvrdí.
  **Pila:** jeden `Case`, jehož `expected` **neobsahuje** `Reviewed-by: Cursory glance at
  the diff` — tím se z vedlejšího účinku stane rozhodnutí.

### `i0005` c2 — nesené z kola 1, přeměřené a nezměněné

- **FU-4 — `git ls-files -s -- hooks` je užší než výčet `shipped_hooks()`.**
  `hook_checks.py:252` vs `:145-156`. Hook deklarovaný v `hooks.json` **mimo** `hooks/`,
  commitnutý jako `100644` a v pracovním stromu `755`, projde (exit 0) a hlásí se jako
  „untracked", ačkoli trackovaný je; tentýž soubor v `hooks/` je zachycen (exit 1).
  Přeměřeno v kole 2, beze změny. **Pila:** pathspec sjednotit s výčtem, nebo výčet omezit
  na `hooks/` a deklarace mimo `hooks/` odmítat.
- **FU-5 — `hooks.json`, jaké šablona nepoužívá, rozbije enforcer `i0005` c2.** Dvě formy,
  obě přeměřené v kole 2: příkaz s argumentem (`bash .cursor/hooks/session-start.sh`) →
  `ERROR bash .cursor/hooks/session-start.sh: missing`, exit 1 (falešná chyba v projektu
  s bezvadnými hooky); příkaz absolutní cestou (`/bin/sh`) → `ValueError: '/bin/sh' is not
  in the subpath of …` z `hook_checks.py:274`, tedy traceback místo nálezu (`check_executable`
  tuhle výjimku ošetřenou má, `check_committed_mode` ne). **Pila:** `command` rozdělit
  (`shlex.split`, první token = cesta) a `relative_to` ošetřit stejně jako v
  `check_executable`.
- **FU-6 (minor) — poznámka zdvojuje slovo:**
  `committed modes checked (hooks/git/pre-push untracked untracked)` (`hook_checks.py:276,283`).

### `i0001` — hranice věty, Humanovo teritorium (z plánu, beze změny)

- **FU-7** — c1 nesahá na `README.md`, `commands/*.md`, `doc/runs/**`; rozšíření je změna
  textu kontraktu, tedy intent delta (položka 1 plánu).
- **FU-8** — c2 nemluví o `.cursor/commands` ani `.cursor/hooks.json`; v šabloné je Cursor
  přes `.cursor/` neobjeví (položka 2 plánu).
- **FU-9 (minor)** — pod `skills/` se nekontrolují jiné přípony než `.md`, a legitimní
  vnořená čtyřznaková ohrada uvnitř trojznakového bloku by se ohlásila jako nedovřená.
  Dnes takový soubor neexistuje.

### Minor, nová v kole 2

- **Mi6** — komentář hooku (`hooks/git/commit-msg:9`) má rozbitou větu: „…so unanchored
  address matches the old hook still remove stay removed." Text nad jediným regexem, na
  kterém stojí celý kontrakt, by měl jít přečíst.
- **Mi3 (z kola 1, trvá)** — `_BASE` a `_CLEAN` jsou znak za znak totožné konstanty.

## Kde věty dosahují — tabulka pokračuje

Číslování z kola 1 platí dál. Řádky 1–22, 24–32 a 36–52 jsem v kole 2 **přeměřil
znovu** (23 mutací tabulky A1/A2, 14 tabulky A4, pět montážních scénářů, E11, FU-C/FU-D
grepy) a ani jedna se nepohnula; níž vypisuji jen řádky, které kolo 2 mění, a nové.

| # | Místo | Mutace | Sada / cmd | Stav v kole 1 | Stav teď |
|---|---|---|---|---|---|
| 23 | adresní větev `grep`u | E13: smazat ji | cmd exit 1, jmenuje `address_only_trailer` + 3 | **open (B1)** | **closed** |
| 33 | klíč mimo gramatiku (`Co-authored-by :`, `2fa-note:`, `Co_authored_by:`, `co.authored.by:`) | E14: vrátit úzkou gramatiku | cmd exit 1, jmenuje `space_before_colon` + 3 | **open (B2)** | **closed** |
| 34 | `-by`/`-with` klíč s hodnotou začínající „cursor", který agentem není | vložit řádku | cmd exit 0 | open (M1) | **open — FU-3** (rozhodnutí zapsáno v kódu i README, chybí řez) |
| 53 | **skládaný trailer: pokračovací řádka nese adresu nebo jméno** | vložit fold | cmd exit 0, sada zelená | (neměřeno) | **open — B3** |
| 54 | jmenná větev: mezera před dvojtečkou **bez** adresy | E14b: zúžit jen jmennou větev | cmd exit 0, sada zelená | (neměřeno) | **open — FU-1** |
| 55 | řádka s adresou, kterou git za trailer nepovažuje (mezera v klíči, `+`, `/`, `#`) | vložit řádku | cmd exit 0 | (částečně v B2) | **open — FU-2**, autorizovaná próza |
| 56 | jednoznakový klíč, tab před dvojtečkou, více mezer, CRLF, trailing whitespace, odsazení tabem | vložit každou formu, oba hooky | shodné chování, attribution mizí | (částečně) | **closed** |
| 57 | dvojitá pomlčka v klíči, klíč s číslicí a velkými písmeny (`X2-Authored-By:`) | vložit řádku | `new` maže, `old` nechával | (neměřeno) | **closed** (utažení) |
| 58 | `-i` (case-insensitivita) | X11: odebrat `-i` | cmd exit 1, devět případů | (neměřeno) | **closed** |
| 46 | hook deklarovaný mimo `hooks/`, v indexu 100644 | pathspec `-- hooks` ho nevidí | cmd exit 0 | open (Mi1) | **open — FU-4** |
| 47 | `hooks.json` s argumentem / absolutní cestou | změnit `command` | falešné „missing" / `ValueError` | open (M2, M3) | **open — FU-5** |

Uzavřené řádky (1–22, 24–32, 36–45, 48–52, 56–58) znovu neotevírám; otevřená demanda je
řádek 53 (blokátor) a řádky 34, 46, 47, 54, 55 (follow-upy).

## Co jsem si ověřil sám v kole 2

| Příkaz / měření | Výsledek | Exit |
|---|---|---|
| nadmnožina znovu: 53 kandidátních řádek × 6 tvarů, `old` vs finální hook | 30 případů `old maže / new nechává` v **6 třídách**: 5 je próza/subjekt (T12/T13, autorizováno), 1 je `Co-authored by:` s mezerou v klíči (git ji za trailer nemá → FU-2). **Čtyři třídy z B2 zmizely.** | — |
| gramatika: 21 forem klíče a skládání, `git interpret-trailers --parse` jako arbitr | git přijímá klíč = alnum + pomlčka, mezery/taby okolo `:` — to gramatika pokrývá celé; **skládání ne** (B3) | — |
| E13 / E14 / E14b / E14c / X2r2 / X3r2 / X11 / X12 | 7 z 8 řeže a jmenuje slíbené případy; mlčí jen E14b → FU-1 | — |
| `no_address_branch` stub | padá s `address_only_trailer` ve výstupu, tedy z adresního důvodu | 1 |
| dokumentovaná cena předpony, všechny 4 příklady | změřeno: `old` keep → `new` DEL u všech čtyř; popis je pravdivý a v druhu úplný (39 tříd, žádná mimo dvě pravidla) | — |
| 23 mutací A1/A2 + 14 A4 + 5 montážních scénářů | beze změny proti kolu 1; žádný falešný *closed* | — |
| tři follow-upy c2 z kola 1 (P1, P2, `hooks.json` s argumentem) | reprodukují se beze změny | — |
| FU-B test, FU-C věta, FU-D obě editace | přítomné a nezměněné; 143 / 156 / 135 řádků | — |
| `git diff --stat doc/intent/_policy.yaml doc/intent/nodes/ VERIFY.md AGENT_MODELS.md` | prázdný | — |
| `validate` / `coverage` / `scope` / `realization check` | 5 nodes 0/0; 28/28, `files outside any node: 0`; `scope clean (10 declared path(s))`; `consistent (3 entry/entries)` | 0 |
| `realization status` | `i0001` i `i0005` dál `not_claimed`; `git diff -- doc/intent/_realization.yaml` prázdný | 0 |
| `template_checks` / `hook_checks` | `satisfied`; `19 message case(s)`, `committed modes checked` | 0 |
| `unittest discover` / `ruff check` / `ruff format --check` | `Ran 115 tests OK`; passed; 20 files formatted | 0 |
| `git status --short` na konci | shodný se stavem na začátku kola 2 + tento `review.md` | — |

## Podepsal bych, že `i0001` a `i0005` jsou dokázané?

- **`i0001` c1 a c2 — ano, bez výhrady k enforceru.** Beze změny proti kolu 1, celé
  přeměřeno. Otevřené je jen to, co plán správně dává Humanovi (FU-7, FU-8) — to jsou
  hranice **věty**, ne děravá kontrola.
- **`i0005` c2 — ano, s třemi zapsanými follow-upy** (FU-4, FU-5, FU-6). Ani jeden nedělá
  dnešní tvrzení nepravdivým: „every shipped hook" je objevování včetně nových
  podadresářů, prázdný glob je ohrazený, mód v indexu se kontroluje a bez `.git` to nahlas
  přizná. FU-4 a FU-5 jsou o formách `hooks.json`, které tato šablona nepoužívá.
- **`i0005` c1 — ještě ne, a chybí k tomu jedna věc.** Půlka „removes agent attribution"
  je po opravě B1/B2 podstatně silnější než na začátku běhu: adresní i jmenná větev jsou
  řezané, klíčová gramatika pokrývá celý gitový token, devatenáct případů je bajtově
  přesných. Jediné, co brání podpisu, je B3: existuje forma, kterou `git` čte jako přesně
  tu attribution, kterou Cursor vstřikuje, kterou dnešní hook odstraňuje a nový nechává
  projít, a žádný test o ní nemluví. Až bude B3 uzavřen — opravou nebo zapsaným
  rozhodnutím Humana plus ukotvujícím případem — podepíšu i c1.

**Co by čtenář ani po tomto kole neměl předpokládat.** Že enforcer `i0005` c1 rozhoduje
o libovolné zprávě — rozhoduje o **devatenácti**, a jejich seznam je celý obsah kontraktu;
že hook zvládá skládané trailery (nezvládá, B3) nebo trailery, jejichž klíč git odmítá
(nechává je, FU-2); že rozliší agenta od člověka nebo od anglického slova začínajícího na
„cursor" (nerozliší, a je to zapsané rozhodnutí, ne omyl); že kontrola módu vidí hooky
mimo `hooks/` (nevidí, FU-4); a že `i0001` c1 hlídá odkazy v `README.md`, `commands/*.md`
nebo `doc/runs/**` (nehlídá, FU-7).

Kolo 2 ze tří. Otevřený je řádek 53 tabulky; ostatní zavřené řádky znovu otevírat nebudu.

---

# Recenze — kolo 3 (poslední, které metodika dovoluje)

Měřeno na scratch kopiích (`/tmp/adv86/**`, `/tmp/mut3-*`, `/tmp/mut3b-*`, `/tmp/audit-*`);
pracovní strom jsem nezměnil kromě tohoto souboru, hook jsem volal jen na dočasných
souborech, `git commit` ani jednou. Arbitrem trailerovosti zůstává
`git interpret-trailers --parse`.

## Verdikt

**REQUEST CHANGES — a protože je to třetí kolo, současně eskalace na Humana.**

Přestavba na strukturu je z větší části velké zlepšení a **B3 z kola 2 je uzavřený**:
skládané trailery se odstraňují celé, próza před blokem je nedotknutelná konstrukcí, a
v celém měření 53 kandidátů × 6 tvarů git po hooku **neparsuje ani jednu attribution**.
Jenže „poslední odstavec" se počítá nad **surovým souborem**, ne nad zprávou, kterou git
nechá — a ve třech dosažitelných tvarech proto neprojde nic a attribution přežije celá.
Tam, kde dnešní ranní hook mazal, nový nemaže. To je slabší než před tímto během, tedy
blokátor; ale je to **jedna vada s jednou dvouřádkovou opravou**, ne třetí neúspěšný pokus.

## Blockers

Jedna příčina, tři dosažitelné tvary. `hooks/git/commit-msg:57-75` — blok se hledá dřív,
než se ze zprávy odstraní to, co git zahodí. Hook si trailing blanky už zahazuje, ale až
**na konci** (`:102`); stejný krok musí přijít **před** výpočtem `last_blank`, a spolu
s ním vynechání komentářových řádek a všeho za `# --- >8 ---`, tedy přesně to, co dělá
`git commit --cleanup`.

- **B4 — koncová prázdná řádka vyřadí detekci bloku úplně; attribution přežije.**
  `last_blank` ukazuje na poslední prázdnou řádku *souboru*, takže `trailer_start = n+1`
  a v trailerové zóně není nic. Nejmenší reprodukce, dvě řádky rozdílu:

  ```
  $ printf 'feat: x\n\nIntent: i0005\nCo-authored-by: Cursor <cursoragent@cursor.com>\n\n' > /tmp/a
  $ bash hooks/git/commit-msg /tmp/a && git interpret-trailers --parse < /tmp/a
  Intent: i0005
  Co-authored-by: Cursor <cursoragent@cursor.com>     ← attribution beze změny
  $ git show HEAD:hooks/git/commit-msg > /tmp/old-hook   # dnešní ranní hook
  $ printf 'feat: x\n\nIntent: i0005\nCo-authored-by: Cursor <cursoragent@cursor.com>\n\n' > /tmp/b
  $ bash /tmp/old-hook /tmp/b && git interpret-trailers --parse < /tmp/b
  Intent: i0005                                        ← ranní hook ji odstraní
  ```

  Totéž s koncovou řádkou z mezer. Dosažitelné bez editoru: `git commit -F soubor`, kde
  soubor končí prázdnou řádkou, nebo `git commit -m $'…\n\n'`. Cleanup, který blanky
  zahodí, běží **po** hooku, takže git pak trailer normálně zaparsuje a zapíše.
- **B5 — komentářový blok, který `git commit` do zprávy sám napíše, přesune „poslední
  odstavec" na sebe.** Zpráva z editoru končí blokem `# Please enter the commit
  message…`; poslední odstavec je pak tenhle blok, skutečný trailerový blok leží před
  `trailer_start` a opisuje se doslova — attribution přežije. Že komentáře v souboru
  v době hooku opravdu jsou, není můj dohad: `githooks(5)` u `prepare-commit-msg` píše, že
  ukázkový hook, který git dodává, *„removes the help message found in the commented
  portion of the commit template"* — kdyby tam v té fázi nebyla, nebylo by co odstraňovat,
  a cleanup běží až po `commit-msg`. Měřeno: nový hook nechá `Co-authored-by: Cursor
  <cursoragent@cursor.com>`, ranní hook ji odstraní.
- **B6 — `git commit -v`: za komentáři je ještě diff, takže poslední odstavec je uvnitř
  diffu.** Stejná příčina, stejný výsledek: attribution v trailerovém bloku zůstane
  (a git ji po odstranění scissors části zapíše). Navíc si všimni, že v zahozené části
  diffu hook naopak maže řádky (`-Co-authored-by: …` je pro `is_key` klíč) — to je bez
  následku, protože ta část stejně padá, ale ukazuje, že zóna je určená chybně.

**Důkaz, že je krátký i enforcer, ne jen hook.** Přidal jsem do `CASES` na scratch kopii
dva řádky v idiomu té tabulky — nic jiného — a kontrola padá:

```
$ python3 tools/checks/hook_checks.py --root .        # + 2 Case()
ERROR hooks/git/commit-msg: case 'attribution_then_trailing_blank_line': output mismatch
+Co-authored-by: Cursor <cursoragent@cursor.com>
ERROR hooks/git/commit-msg: case 'attribution_then_editor_comment_block': output mismatch
+Co-authored-by: Cursor <cursoragent@cursor.com>
2 hook contract violation(s)                                                    exit=1
```

Případ 13 `trailing_blank_lines` (`_BASE + "\n\n\n"`) stojí od zachycení B4 jednu editaci:
nemá v sobě žádnou attribution, takže testuje jen doříznutí blanků, ne jejich interakci
s detekcí bloku.

## Co je naopak uzavřené — a je to hodně

- **B3 z kola 2 (skládaný trailer) uzavřen.** Všech pět mých skládaných útoků (mezera,
  tab, jméno a adresa rozdělené, mezera před dvojtečkou, CRLF) attribution odstraní
  **celou**, včetně klíčové řádky. E16 (odebrání pokračovacích řádek) řeže právě na třech
  skládaných případech.
- **FU-1 z kola 2 uzavřen** případem 28 `made_with_space_before_colon` (`Made-with : Cursor`,
  bez adresy) — přesně to, co jsem v kole 2 žádal.
- **Mi6 z kola 2 uzavřen** — rozbitá věta v komentáři hooku je čitelná.
- **Obě rozhodovací pravidla jsou po přestavbě dál pojistkovaná zvlášť:** odstranění
  adresního pravidla → exit 1 na 4 případech, odstranění jmenného → exit 1 na 7 případech.
- **E15 i E16 řežou z uvedených důvodů.** E15 jmenuje 26 případů včetně
  `indented_prose_quotes_attribution`, E16 přesně `folded_space_continuation`,
  `folded_tab_continuation`, `folded_space_before_colon`.
- **Půlka „keeps everything else" je poprvé strukturální.** V celém měření
  (53 × 6 = 318 kombinací) nový hook **nezahodil ani jednu řádku, která by neobsahovala
  slovo „cursor"**; prázdná zpráva, jednořádková zpráva, próza jako poslední odstavec,
  próza s dvojtečkou v první větě, chybějící koncový newline — všechno projde nedotčené.
- **Vše z kol 1 a 2 stojí:** 23 mutací A1/A2, 14 A4, montovaná varianta (`.cursor/`) i její
  čestné přiznání bez `.git`, kontrola módu, FU-B/C/D, `_policy.yaml`, nody, `VERIFY.md`
  a `_realization.yaml` bez diffu, `i0001` i `i0005` dál `not_claimed`.

## Follow-upy — nesené i nové, žádný z nich blokátor

Humana rozhodl, že FU-1 … FU-9 z kol 1 a 2 jdou do `doc/new_ideas/` jako materiál; nové
patří tam samé. Ani jeden nedělá dnešní větu nepravdivou — ve všech pěti případech níž je
kód správný a chybí jen řez.

- **FU-10 — případ `crlf_line_endings` je vakuózní.** Odebral jsem hooku normalizaci CRLF
  (`sub(/\r$/, "")`) a kontrola zůstala **zelená**, přitom hook nechal `\r` na každé řádce
  (`cat -A` → `^M$`). Příčina je v kontrole, ne v hooku: `hook_checks.py:340` čte výstup
  přes `Path.read_text()`, který v textovém režimu překládá `\r\n` → `\n`, takže rozdíl,
  o který tomu případu jde, zmizí ještě před srovnáním. **Pila:** čtení přes
  `read_text(newline="")` nebo `read_bytes()`.
- **FU-11 — oddělovač složený jen z mezer není pojistkovaný.** Zúžení `is_blank` na
  `/^$/` nechá kontrolu zelenou, i když dnešní hook mezerovou oddělovací řádku správně
  bere jako prázdnou. **Pila:** jeden `Case`, jehož oddělovač jsou tři mezery.
- **FU-12 — adresa na pokračovací řádce u klíče, který není `-by`/`-with`.** Zúžení
  `is_attribution` na hledání adresy jen v klíčové řádce nechá kontrolu zelenou:
  `folded_name_then_address` totiž zachytí jmenné pravidlo, ne adresní. **Pila:** `Case`
  s `Note:` a adresou na odsazené pokračovací řádce.
- **FU-13 — osiřelá pokračovací řádka s adresou** (`commit-msg:94-97`) není pojistkovaná;
  odebrání té větve nechá kontrolu zelenou.
- **FU-14 — spojování složené hodnoty bez oddělovací mezery** není pojistkované.
- **FU-15 — attribution mimo trailerový blok (v těle nebo v subjectu) teď zůstává.**
  66 z 90 řádkových rozdílů `old maže / new nechává` je právě tohle. Je to **záměr**
  („próza před blokem je nedotknutelná") a git v těch tvarech žádný trailer nevidí, takže
  věta tím neztrácí pravdivost — ale je to zásadní změna chování proti ranní verzi a nikde
  není zapsaná jako rozhodnutí, jen jako důsledek. **Pila:** jedna věta v komentáři hooku
  a v `hooks/README.md`, plus `Case`, který to drží.
- **FU-16 — legitimní trailer se zahodí celý, když jeho pokračovací řádka nese adresu.**
  `Intent: i0005` + odsazené `see cursoragent@cursor.com` zmizí **oba** (ranní hook nechal
  `Intent: i0005`). Je to nutný důsledek toho, co Human zvolil — odstraňovat trailer jako
  celek — a `Intent:` s adresou agenta reálně nevzniká; patří to ale do dokumentace ceny,
  vedle ceny předpony.
- **FU-17 — odsazená próza v posledním odstavci, která cituje attribution, se zahodí.**
  Věta „próza je nedotknutelná" platí jen pro prózu **před** blokem. Ranní hook ji mazal
  taky, takže to není zhoršení; případ 26 `indented_prose_quotes_attribution` hlídá jen
  variantu před blokem.
- Nesené bez změny: **FU-2 … FU-9** z kol 1 a 2 (mezera v klíči a klíče `+`/`/`/`#`, cena
  předpony bez řezu, `ls-files -- hooks` užší než výčet, `hooks.json` s argumentem nebo
  absolutní cestou, zdvojené „untracked", hranice `i0001`, přípony pod `skills/`), plus
  **Mi3** (`_BASE` = `_CLEAN`).

## Kde věty dosahují — závěrečná tabulka

Číslování z kol 1 a 2 platí. Řádky 1–22, 24–32, 36–52 jsem přeměřil znovu a nepohnuly se;
níž jsou jen změněné a nové.

| # | Místo | Mutace | cmd | Stav |
|---|---|---|---|---|
| 23 | adresní pravidlo | odebrat celé | exit 1, 4 případy | **closed** (přeneseno z regexu do `is_attribution`) |
| 33 | gramatika klíče | zúžit na `[A-Za-z][A-Za-z-]*:` | exit 1, 6 případů | **closed** |
| 34 | cena předpony | vložit `Reviewed-by: Cursory …` | exit 0 | open — FU-3 (dokumentováno, bez řezu) |
| 53 | **skládaný trailer** | E16: odebrat pokračovací řádky | exit 1, 3 skládané případy | **closed** (B3 z kola 2) |
| 54 | jmenné pravidlo, mezera před dvojtečkou bez adresy | zúžit jmennou větev | exit 1, `made_with_space_before_colon` | **closed** (FU-1 z kola 2) |
| 55 | řádka s adresou, kterou git za trailer nemá | vložit ji | exit 0 | open — FU-2, autorizovaná próza |
| 59 | **koncová prázdná řádka** | žádná — vada je v kódu | exit 0, sada zelená | **open — B4** |
| 60 | **komentářový blok za trailery** | žádná — vada je v kódu | exit 0, sada zelená | **open — B5** |
| 61 | **`commit -v`: scissors a diff** | žádná — vada je v kódu | exit 0, sada zelená | **open — B6** |
| 62 | detekce bloku vůbec | E15: `trailer_start = 1` | exit 1, 26 případů | **closed** |
| 63 | normalizace CRLF | odebrat `sub(/\r$/,"")` | exit 0 | open — FU-10 (vakuózní případ) |
| 64 | oddělovač z mezer | `is_blank` → `/^$/` | exit 0 | open — FU-11 |
| 65 | adresa na pokračovací řádce | hledat ji jen v klíčové řádce | exit 0 | open — FU-12 |
| 66 | osiřelá pokračovací řádka s adresou | odebrat větev | exit 0 | open — FU-13 |
| 67 | spojení složené hodnoty | zahodit oddělovací mezeru | exit 0 | open — FU-14 |
| 68 | próza před blokem se opisuje doslova | pustit smyčku na celou zprávu | exit 1, 27 případů | **closed** |
| 69 | cesta „celá zpráva jsou trailery" | vypnout ji | exit 1, `attribution_only` | **closed** |
| 70 | attribution v těle nebo v subjectu | vložit ji tam | exit 0 (záměr) | open — FU-15, rozhodnutí bez zápisu |
| 71 | trailer, jehož pokračovací řádka nese adresu | vložit `Intent:` + adresu | maže se celý | open — FU-16 |
| 46 | hook mimo `hooks/` v indexu 100644 | pathspec `-- hooks` ho nevidí | exit 0 | open — FU-4 |
| 47 | `hooks.json` s argumentem / absolutní cestou | změnit `command` | falešné „missing" / `ValueError` | open — FU-5 |

Demanda: **řádky 59, 60, 61 jsou blokátory**; 34, 46, 47, 55, 63–67, 70, 71 jsou
follow-upy. Ostatní jsou uzavřené a znovu je neotevírám.

## Co jsem si ověřil sám

| Měření | Výsledek | Exit |
|---|---|---|
| 53 kandidátů × 6 tvarů, arbitrem git nad **výstupem hooku** | **0 z 318**: git po hooku neparsuje žádnou attribution; **0** zahozených řádek bez markeru „cursor" | — |
| týchž 318 kombinací, řádkově | 90 rozdílů `old maže / new nechává`, z toho git ve **0** vidí přeživší attribution (66 = tělo/subject, 24 = próza a klíče mimo gramatiku) | — |
| 29 strukturálních útoků na `awk` | 26 ok, **3 blokátory** (B4, B5, B6), 1 hraniční (FU-16) | — |
| 13 mutací struktury (E15, E16, X20–X29, E13′, X2′) | 8 řeže a jmenuje slíbené případy; 5 mlčí → FU-10 … FU-14 | — |
| dva `Case`y přidané do `CASES` na scratch kopii | oba padají na nasazeném hooku, `2 hook contract violation(s)` | 1 |
| 23 mutací A1/A2 + 14 A4 + 5 montážních scénářů | beze změny proti kolům 1 a 2; žádný falešný *closed* | — |
| `validate` / `scope` / `realization check` | 5 nodes 0/0; `scope clean (10 declared path(s))`; `consistent (3 entry/entries)` | 0 |
| `realization status`; diff `_realization.yaml` | `i0001` i `i0005` `not_claimed`; diff prázdný — nárok nikdo nepředběhl | 0 |
| `_policy.yaml`, `doc/intent/nodes/`, `VERIFY.md`, `AGENT_MODELS.md` | `git diff --stat` prázdný | — |
| `template_checks` / `hook_checks` | `satisfied`; `28 message case(s)`, `committed modes checked` | 0 |
| `unittest discover` / `ruff check` / `ruff format --check` | `Ran 115 tests OK`; passed; 20 files formatted | 0 |
| `git status --short` na konci | shodný se stavem na začátku kola 3 + tento `review.md` | — |

## Eskalace na Humana — co je potřeba rozhodnout

Tři kola jsou vyčerpaná, takže rozhodnutí je tvoje. Prostě řečeno: **`i0005` c1 je dnes
pravdivější než ráno ve všem kromě jedné věci — kde blok leží.** Oprava je malá a
lokální: doříznout koncové prázdné řádky a vynechat komentářové řádky (a vše za scissors)
**před** výpočtem `last_blank`, plus dva `Case`y, které mám změřené a které padají. Nejde
o čtvrtý pokus o regex; jde o dvě řádky v `END` bloku. Alternativa „zapsat hranici" tady
podle mě neobstojí: komentářový blok píše do zprávy git sám, takže by věta musela říkat,
že hook nefunguje na běžném commitu z editoru.

## Podepsal bych, že `i0001` a `i0005` jsou dokázané, a že nic v tomto stromu není slabší než před těmito třemi běhy?

- **`i0001` c1 a c2 — ano.** Třikrát přeměřeno, beze změny, otevřené je jen to, co plán
  správně dává Humanovi (FU-7, FU-8).
- **`i0005` c2 — ano**, se třemi zapsanými follow-upy (FU-4, FU-5, FU-6); žádný z nich
  nedělá dnešní tvrzení nepravdivým.
- **`i0005` c1 — ne, ještě ne, a na přímou otázku odpovídám přímo: ano, v jednom ohledu je
  tenhle strom slabší než byl dnes ráno.** Ve všem ostatním je nesrovnatelně silnější —
  skládané trailery, gramatika klíčů, adresní i jmenné pravidlo, 28 bajtově přesných
  případů proti jedné ukázkové zprávě, próza chráněná konstrukcí. Ale pro zprávu, jejíž
  poslední surový odstavec není trailerový blok — koncová prázdná řádka, komentáře
  z editoru, `commit -v` — projde attribution, kterou ranní hook odstraňoval. Dokud to
  platí, c1 nepodepíšu; s tou dvouřádkovou opravou a dvěma případy podepíšu bez výhrad.

**Co by čtenář neměl předpokládat ani po třech kolech.** Že hook chrání commity z editoru
(dnes ne, B5); že „poslední odstavec" znamená to, co git nechá (znamená to, co je
v souboru, B4); že attribution v těle nebo v subjectu zmizí (nezmizí, FU-15 — a je to
záměr); že kontrola vidí rozdíl mezi CRLF a LF (nevidí, FU-10); že „every shipped hook"
zahrnuje hooky mimo `hooks/` (nezahrnuje, FU-4); a že `i0001` c1 hlídá odkazy v
`README.md`, `commands/*.md` nebo `doc/runs/**` (nehlídá, FU-7).

Kolo 3 ze tří — dál to metodika nedovoluje. Předávám Humanovi.
