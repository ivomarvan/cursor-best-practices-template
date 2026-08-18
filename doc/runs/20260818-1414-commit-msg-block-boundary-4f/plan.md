---
run_id: 20260818-1414-commit-msg-block-boundary-4f
intent_ids: ["i0005", "i0004"]
role: Planner
model: cursor-grok-4.5-high
complexity: high
status: in-progress
outputs:
  - "hooks/git/commit-msg"
  - "hooks/README.md"
  - "tools/checks/hook_checks.py"
incidental:
  - "doc/intent/_realization.yaml"
---

# Plán — hranice trailerového bloku před cleanupem

## Cíl

Nasadit odložený přepis `hooks/git/commit-msg` (POSIX `awk` nad trailerovým blokem) z
`doc/runs/20260818-0853-harness-and-hooks-audit-86/deferred-i0005-hook.patch` a doplnit ho
tak, že:

1. **B4, B5, B6 zmizí.** Po hooku `git interpret-trailers --parse` na dočasném souboru
   **nevrátí** žádný trailer s `cursoragent@cursor.com` ani `-by`/`-with` hodnotou
   začínající `Cursor`, a to i když surový soubor končí prázdnou řádkou, komentářovým
   blokem šablony editoru, nebo scissors řádkou a diffem z `git commit -v`.
2. **FU-10 … FU-14 řežou.** Každá z pěti jmenovaných mutací enforceru / hooku nechá
   `python3 tools/checks/hook_checks.py --root .` s **exit 1** a ve výstupu jmenuje
   slíbený `case '…'`.
3. **FU-15 a FU-16 jsou zapsané.** Komentář hooku a `hooks/README.md` výslovně uvádějí
   dvě záměrné ceny proti rannímu řádkovému grepu (attribution v subjectu/těle zůstává;
   legitimní trailer padá celý, když pokračovací řádka nese adresu agenta).

Žádný text kontraktu `i0005` c1/c2 ani `i0004` se nemění. Strom se nehýbe.

## Verdikt ke směru Adversáře (ověřeno, ne opsáno)

**Směr je správný v jádru, detaily je potřeba zpřesnit.**

Adversář: doříznout koncové prázdné řádky, vynechat komentáře a vše za scissors **před**
výpočtem `last_blank`. To je správná diagnóza jedné příčiny B4/B5/B6.

Ověření proti `git-commit(1)` / `git-config(1)` a scratch repozitáři (bez `git commit` v
tomto stromu; jen `/tmp`):

| Tvrzení Adversáře | Skutečnost | Důsledek pro plán |
|---|---|---|
| Cleanup běží po `commit-msg` | Ano. Hook vidí surový `COMMIT_EDITMSG`; git teprve potom čistí. | Hook musí **anticipovat** cleanup, ne spoléhat na něj. |
| `default` = strip při editaci, jinak whitespace | Ano. `-m` / `-F` bez editoru → `whitespace` (zahodí trailing blanky, **komentáře nechá**). Editor → `strip` (komentáře zahodí). | B4 je společné oběma. B5 je cesta **editoru** (`strip`). |
| Scissors jen u `--cleanup=scissors` / `-v` | **-v / `commit.verbose` šablonu scissors+diff opravdu vloží** (`# ------------------------ >8 ------------------------`). Cleanup režim `scissors` odřízne od té řádky dál (diff není prefixovaný `#`, pouhý `strip` by ho nenechal). Adversářův zkrácený zápis `# --- >8 ---` je zjednodušení; shoda na podřetězci `--- >8 ---` / `>8` na řádce začínající comment char stačí. | B6 = truncate na scissors **před** detekcí bloku. |
| Comment char je `#` | **`core.commentChar` je konfigurovatelný** (změřeno: s `!` šablona začíná `! Please enter…`). Výchozí `#`. Hodnota `auto` git volí za běhu — hook ji nemá spolehlivě reimplementovat. | Číst `git config --get core.commentChar`, fallback `#`; při `auto` nebo prázdnu použít `#` a zapsat limit. |
| „Udělat totéž co cleanup“ | Hook **nesmí** věrně emulovat všechny módy. U `verbatim` by se nemělo sahat vůbec; u `whitespace` s uživatelským `#` za trailery by kompletní strip komentářů smazal obsah, který git nechá. | Anticipace jen: (1) truncate scissors+, (2) odříznout koncové blanky, (3) odříznout **koncové** komentářové řádky (a blanky mezi nimi a trailery). Netýká se komentářů uprostřed těla. |

**Opravený směr pro Codera (ne „dvě řádky v END“, ale malý preflight před `last_blank`):**

Po načtení `lines[1..n]` (včetně stávající normalizace `\r`):

1. Najít první řádek, který začíná `comment_char` a obsahuje `>8`; nastavit `n` těsně před něj (zahodit scissors i diff — git je stejně neuloží).
2. Od konce odříznout blanky (`is_blank`).
3. Od konce odříznout řádky začínající `comment_char`; znovu odříznout blanky (mezera mezi trailery a šablonou).
4. Teprve teď spočítat `last_blank` / `trailer_start` stávající logikou z patche.
5. Výstup tisknout jen z takto zkráceného `n` (koncové blanky už patch zahazuje na `out`; scissors/komentáře na konci surového souboru do `out` nepatří).

`comment_char` předat do `awk` přes `-v` z bash obálky (`git config --get core.commentChar 2>/dev/null`, fallback `#`). Žádné GNU `awk` rozšíření.

## Východisko

Coder **začne aplikací** `doc/runs/20260818-0853-harness-and-hooks-audit-86/deferred-i0005-hook.patch`
na tři soubory (`hooks/git/commit-msg`, `hooks/README.md`, `tools/checks/hook_checks.py`).
Pracovní strom dnes drží ranní řádkový grep — patch je povinný základ, ne inspirace.
Až potom Group 1–3 níž.

Mimo rozsah (explicitně): FU-1 … FU-9. Nepřidávat je do CASES, README ani komentářů
jako „opravy“.

## Work items

### W1 — Group 1: preflight hranice bloku (B4, B5, B6)

**Soubor:** `hooks/git/commit-msg` (nad patchem).

**Co:** Preflight výše; krátký anglický komentář u `END`, že hook anticipuje
`strip`/`scissors`/`whitespace` trailing-blank část, ne celý cleanup; limit
`core.commentChar=auto`.

**Proč:** Jedna příčina tří tvarů — `last_blank` nad surovým souborem. Bez preflightu je
přestavba slabší než ranní grep u běžného commitu z editoru (B5).

**Důkaz:** tři nové `Case` v `tools/checks/hook_checks.py` (W2) + ruční volání hooku na
`/tmp` souborech (nikdy `git commit` v tomto repu):

| ID | Vstup (podstata) | Po hooku `interpret-trailers --parse` |
|---|---|---|
| B4 | `_BASE` + attribution + `\n\n` | jen Intent/Run |
| B5 | trailery + attribution + blok `# Please enter…` / `# On branch…` | jen Intent/Run; komentáře pryč |
| B6 | jako B5 + scissors `# ---…>8…---` + několik řádek `diff --git` | jen Intent/Run; diff pryč |

Mutace „odebrat preflight“ → tyto tři case padají (viz Test spec).

### W2 — Group 1 enforcer: case, které dnes na patchi bez preflightu padají

**Soubor:** `tools/checks/hook_checks.py`.

Přidat (jména pevná — Adversář / Grader / Coder stejný řetězec):

| `Case.name` | `message` (záměr) | `expected` |
|---|---|---|
| `attribution_then_trailing_blank_line` | `_BASE + "\nCo-authored-by: Cursor <cursoragent@cursor.com>\n\n"` | `_CLEAN` |
| `attribution_then_editor_comment_block` | trailery + attribution + typický komentářový patičkový blok šablony (řádky začínající `#`) | `_CLEAN` |
| `attribution_then_scissors_and_diff` | jako výše + scissors s `>8` + 2–3 řádky falešného diffu bez `#` | `_CLEAN` |

Existující `trailing_blank_lines` (`_BASE + "\n\n\n"`) **nechat** — hlídá trim bez attribution;
nový B4 case hlídá interakci trim × detekce bloku.

### W3 — Group 2: FU-10 … FU-14 (enforcer musí kousat)

**Soubor:** `tools/checks/hook_checks.py` (+ drobnost ve čtení výstupu).

| ID | Vada | Oprava | Mutace → exit 1, jméno case |
|---|---|---|---|
| **FU-10** | `Path.read_text()` v textovém módu spolkne `\r` → `crlf_line_endings` je vakuum | Číst výstup `message_file.read_bytes()` a porovnat s `case.expected.encode("utf-8")` (nebo `read_text(newline="")`). Zápis vstupu u CRLF case přes `write_bytes`, ať se `\r\n` opravdu dostane na disk. | Odebrat v hooku `sub(/\r$/, "")` → case `crlf_line_endings` |
| **FU-11** | `is_blank` zúžené na `/^$/` zůstane zelené | `Case` `blank_separator_only_spaces`: oddělovač mezi subjectem a trailery jsou tři mezery (`"   \n"`), attribution za tím; expected `_CLEAN` | `is_blank` → `return s ~ /^$/` → `blank_separator_only_spaces` |
| **FU-12** | adresa jen na pokračovací řádce u klíče mimo `-by`/`-with` chybí v sadě | `Case` `address_on_continuation_non_by_with`: `Note:\n  see cursoragent@cursor.com\n` v trailerovém bloku; expected bez toho Note traileru | v `is_attribution` hledat adresu jen na klíčové řádce → tento case |
| **FU-13** | větev osiřelé pokračovací řádky s adresou bez case | `Case` `orphan_continuation_with_address`: v trailerové zóně samostatná odsazená řádka s `cursoragent@cursor.com` (ne pokračování klíče); expected ji nemá | smazat větev orphan+address v hooku → tento case |
| **FU-14** | spojení foldu bez mezery nepadá | `Case` `folded_join_requires_space`: klíč `Co-authored-by: Cur` + pokračování `  sor Smith <human@example.com>\n` — s mezerou hodnota `Cur sor Smith…` **není** attribution (expected trailer **zůstane**); bez mezery by vzniklo `Cursor Smith…` a trailer by zmizel | `val = val piece` místo `val " " piece` → tento case (output mismatch — chybí trailer) |

Každý nový case = jeden pojistkový řez. Sdílený harness `check_commit_msg_strips_attribution` zůstává; nepřidávat druhé aserci „napůl“.

### W4 — Group 3: zapsat cenu (FU-15, FU-16)

**Soubory:** `hooks/git/commit-msg` (komentář nahoře), `hooks/README.md` (odstavec u chování / ceny předpony).

Zapsat anglicky, vedle už dokumentované ceny předpony `Cursor`:

- **FU-15:** attribution v subjectu nebo v těle **před** trailerovým blokem se **neodstraňuje** (próza před blokem je nedotknutelná konstrukcí). Git z těchto tvarů attribution jako trailer neparsuje. Záměr, ne regrese věty c1. (Patch už má `body_quotes_the_address` a `subject_names_cursor` — ty chování drží; Group 3 nepřidává další case, jen dokumentaci.)
- **FU-16:** pokud pokračovací řádka legitimního traileru nese `cursoragent@cursor.com`, padá **celý** trailer (včetně klíčové řádky). Nutný důsledek „drop as a unit“. Do README jedna věta; volitelný ilustrační `Case` **není** v rozsahu requestu — jen dokumentace.

### W5 — mimo kód, povinné artefakty Codera

- `report.md` (česky, struktura z `07-run-artifacts`).
- `coder-evidence.md` (volitelně, doporučeno): surový výstup mutací z tabulky failing-test evidence.
- Nikdy neměnit `doc/intent/nodes/**`, `VERIFY.md`, `_policy.yaml`, `AGENT_MODELS.md`.

## Testovací specifikace

Enforcer zůstává `cmd: python3 tools/checks/hook_checks.py --root .` (`i0005` c1 i c2).

| Druh | Case / kontrola | Očekávání |
|---|---|---|
| Happy path | stávající `cursor_trailer`, `human_co_author`, `mixed_attribution_and_legitimate_trailers` | attribution pryč, lidský trailer a Intent/Run beze změny, exit 0 |
| Edge | `attribution_then_trailing_blank_line`, `attribution_then_editor_comment_block`, `attribution_then_scissors_and_diff`, `blank_separator_only_spaces`, `crlf_line_endings`, `folded_join_requires_space` | byte-exact `expected`, exit 0 |
| Error (pojistky) | mutace v tabulce níž | exit 1, ve stderr/stdout `case '<jméno>'` |

`i0005` c2: stávající `check_executable` + `check_committed_mode` z patche — neměnit smlouvu; jen ověřit, že po úpravách dál prochází.

## Failing-test evidence — mutace, které Coder musí spustit

Každá na scratch kopii souboru pod `/tmp` (nebo revertovatelná editace); pracovní `git` stav repa se nemění. Výstup uložit do `report.md` / `coder-evidence.md`.

| # | Co mutovat | Očekávaný pád (jméno case v hlášce) |
|---|---|---|
| E-B4 | v hotovém hooku přeskočit krok „odříznout koncové blanky před `last_blank`“ | `attribution_then_trailing_blank_line` |
| E-B5 | přeskočit odřezávání koncových komentářů | `attribution_then_editor_comment_block` |
| E-B6 | přeskočit truncate na `>8` | `attribution_then_scissors_and_diff` |
| E-10 | odebrat `sub(/\r$/, "")` | `crlf_line_endings` |
| E-11 | `is_blank` → jen `/^$/` | `blank_separator_only_spaces` |
| E-12 | adresu hledat jen na první řádce traileru | `address_on_continuation_non_by_with` |
| E-13 | smazat orphan-continuation+address větev | `orphan_continuation_with_address` |
| E-14 | `val = val piece` (bez mezery) | `folded_join_requires_space` |

Baseline před mutací: celá sada zelená (`hook contracts satisfied`, exit 0).
Na **neopraveném** patchi bez W1 musí E-B4/B5/B6 (resp. samotné nové case) padat — to je důkaz, že case nejsou vakuózní.

## Definition of Done

- [ ] Patch `deferred-i0005-hook.patch` je aplikovaný základ; diff W1–W4 je navrch.
- [ ] `hooks/git/commit-msg` má preflight (scissors → trailing comments → trailing blanks) před výpočtem `last_blank`; `comment_char` z configu s fallbackem `#`.
- [ ] `python3 tools/checks/hook_checks.py --root .` → exit 0; výstup hlásí počet case ≥ 28 + nově přidané.
- [ ] Failing-test evidence: tabulka E-* výše, každá mutace exit 1 a jmenovaný case (`report.md` / `coder-evidence.md`).
- [ ] Ruční B4/B5/B6 na `/tmp` + `git interpret-trailers --parse` bez attribution (exit 0 parse, žádný cursor trailer).
- [ ] FU-15 a FU-16 věty v komentáři hooku a v `hooks/README.md`.
- [ ] `python3 tools/intent/cli.py validate` → exit 0 (strom beze změny).
- [ ] `python3 tools/intent/cli.py scope --run doc/runs/20260818-1414-commit-msg-block-boundary-4f` → clean.
- [ ] `VERIFY.md` (Grader) projde včetně `hook_checks`.
- [ ] Žádný `git commit` / změna git stavu tohoto repa; hook jen na dočasných souborech.
- [ ] FU-1 … FU-9 se v diffu neobjeví jako nová práce.
- [ ] `report.md` vyplněný dle `07-run-artifacts`.

## Rizika

1. **Příliš chytřý cleanup** — emulovat `verbatim` / celé `whitespace` včetně uživatelských `#` by rozbilo vzácné `-F` zprávy. Mitigace: jen koncový preflight (scissors + koncové komentáře + blanky), zapsaný limit.
2. **`core.commentChar=auto`** — neřešíme; fallback `#`.
3. **FU-14 case musí expected držet lidský folded trailer** — špatně zvolený expected by case udělal vakuózní. Držet se `Cur` + `sor Smith`.
4. **Scope** — jen tři cesty v `outputs` (+ run dir automaticky). Nesahat na `tools/intent/tests/test_checks.py` ani jinam.
5. **Běh je splnitelný v zadaném rozsahu.** Blokátor je lokální, intent se nemění, enforcer gaps mají jasné řezy. Jediné eskalovat by bylo zjištění, že c1 musí změnit text kvůli FU-15 — to **odmítám**: git v subjectu/těle attribution jako trailer nevidí, věta zůstává pravdivá; stačí dokumentace.

## Definition of Ready (sebekontrola Planneru)

- [x] Cíl měřitelný (B4/B5/B6 + mutace FU-10…14 + zápis FU-15/16).
- [x] Outputs pojmenované.
- [x] Slice z Coordinátora; uzly bez blocking open questions.
- [x] Enforcer beze změny cesty (`hook_checks.py`).
- [x] Test spec: happy + edge + error.
- [x] DoD mapuje na příkazy/artefakty.
- [x] Incidental vyjmenované.
- [x] Implementovatelné izolovaně (patch + `/tmp` mutace).
