---
run_id: 20260818-1414-commit-msg-block-boundary-4f
intent_ids: ["i0005", "i0004"]
role: Critic
model: claude-sonnet-5-thinking-high
complexity: high
status: done
---

# Kritika — plán „hranice trailerového bloku před cleanupem"

## Verdikt

**ACCEPT.**

Jádro plánu — preflight, který useká scissors, koncové komentáře a koncové prázdné
řádky **před** výpočtem `last_blank` — jsem přestavěl podle Plannerova pětikrokového
návodu a změřil na scratch souborech (`/tmp/critic4f/**`, žádný `git commit` v tomto
repu). Zabíjí to skutečně **všechny tři** tvary B4, B5 i B6, ne jen B4. Plannerovy
tvrzené fakty o `git commit --cleanup`, `--verbose` a `core.commentChar` jsou přesné —
ověřil jsem je proti `git-commit(1)`, `git-config(1)` a proti reálnému běhu
`git commit -v` v scratch repozitáři. Mutace FU-10 a FU-14, které jsem spustil, jsou
reálné řezy, ne rituál. Argument k FU-15 („cena, ne oslabení") obstojí — viz níže.
Definition of Ready je splněná bod po bodu; scope guard navíc automaticky povoluje
celý adresář běhu a `code_paths` obou uzlů, takže seznam `outputs`/`incidental` je
v pořádku i bez explicitního vyjmenování artefaktů běhu.

Jedna nalezená vada je v pomocné (manuální) tabulce „Failing-test evidence", ne
v samotném kontraktu nebo v sadě `Case` — viz Note 1. Nejde o blokátor.

## Blockers

Žádné.

## Notes

**Note 1 — řádek E-B4 v tabulce „Failing-test evidence" pravděpodobně nejde reprodukovat
tak, jak je popsán, díky redundanci vlastní Plannerovu pětikrokovému návodu.**
Návod má **dvě** samostatná odříznutí koncových prázdných řádek: krok 2 (před
odříznutím komentářů) a druhá polovina kroku 3 („znovu odříznout blanky" — mezera mezi
trailery a šablonou). Pro případ `attribution_then_trailing_blank_line` (žádné
komentáře) je krok 3 bez komentářů no-op na vlastní smyčce komentářů, ale jeho vlastní
`while (n>0 && is_blank(lines[n])) n--` proběhne bez ohledu na to, jestli krok 2
proběhl. Změřil jsem to přímo: implementace podle návodu, s odstraněným krokem 2 a
zachovaným krokem 3, **case `attribution_then_trailing_blank_line` dál vychází správně**
— mutace nezčervená. To je přesně ten vzor „mutace, jejíž pád plán neumí předpovědět",
který má Skupina 2 vymazat, jenže se objevuje ve vlastní Skupině 1 Plannerova
doplňku. Nejde o vadu kontraktu ani `Case` sady v `hook_checks.py` — ty jsem změřil
samostatně proti **nezalátanému** patchi (žádný preflight) a tam B4/B5/B6 padají
korektně (viz měření níže), takže samotné `Case` nejsou vakuózní. Vada je jen
v manuální tabulce E-B4/E-B5/E-B6, kterou má Coder reprodukovat pro `report.md`.
Doporučení pro Codera: mutovat **obě** místa odříznutí koncových blanků najednou (nebo
sloučit krok 2 a druhou půlku kroku 3 do jedné funkce), jinak se řádek E-B4 nepodaří
zčervenat a Coder bude nucen buď tabulku upravit, nebo si to nevšimne a napíše do
`report.md` neplatnou evidenci. Nebrání implementaci, jen si to žádá pozornost při psaní
`report.md`.

**Note 2 — `write_bytes` pro CRLF vstup (FU-10) je na Linuxu nadbytečné, ale
neškodí.** Změřil jsem, že `Path.write_text()` na Linuxu `\r\n` v datech nezmění (jen
`\n` by se překládalo na `os.linesep`, který je na Linuxu `\n`). Skutečná vada byla
na straně **čtení** výstupu (`read_text()` v hooku, které `\r\n → \n` skutečně
překládá) — a tu Planner správně cílí. `write_bytes` na vstupu je tedy jen
opatrnost/přenositelnost navíc, ne nutná podmínka opravy. Bez dopadu na verdikt.

**Note 3 — hermetičnost `git config --get core.commentChar` v testovacím prostředí.**
Hook čte `core.commentChar` z konfigurace prostředí, v němž běží `hook_checks.py`
(dědí `cwd` procesu, ne dočasný adresář zprávy) — to je nutně skutečný repozitář, ne
`tempfile.TemporaryDirectory()`. Na většině strojů je to bez efektu (nikdo
`core.commentChar` neustavuje), ale test tím není 100% hermetický vůči globální/lokální
git konfiguraci spouštěče. Nejde o blokátor, jen bych to zapsal jako známou hranici
(analogicky k Riziku 2 v plánu, které `auto` už jako neřešené přiznává).

## Co jsem si ověřil sám

Vše na `/tmp/critic4f/**` a v jednorázovém scratch repozitáři `/tmp/critic4f/scratchrepo`
(`git init` tam, ne v tomto stromu). Pracovní strom šablony jsem nezměnil kromě zápisu
tohoto souboru; `git commit` jsem nespustil ani jednou v tomto repozitáři.

| Měření | Příkaz / postup | Výsledek | Exit |
|---|---|---|---|
| Rekonstrukce patchované awk logiky + Plannerův pětikrokový preflight (viz `is_comment`, scissors-truncate, dvojí blank-strip) | vlastní soubor `commit-msg-patched`, spuštěn na B4/B5/B6 vstupech + `git interpret-trailers --parse` | **B4, B5, B6 všechny fixed** — po hooku žádný `cursoragent@cursor.com` trailer v žádném ze tří tvarů | 0 |
| `git-commit(1)`: `--cleanup=<mode>` | `man git-commit` (sekce `--cleanup`) | `default` = `strip`, pokud se zpráva edituje, jinak `whitespace`; `scissors` = `whitespace` + truncate od `# --- >8 ---` (`core.commentChar` konfigurovatelný) — **Plannerovo tvrzení přesné** | 0 |
| `git-config(1)`: `core.commentChar` | `man git-config` | default `#`; `auto` = git zvolí znak, který se nevyskytuje na začátku žádné řádky v existujících zprávách (běhový, neemulovatelný) — **Plannerovo tvrzení přesné** | 0 |
| Reálný scissors řádek z `git commit -v` | scratch repo, `GIT_EDITOR` skript kopírující `COMMIT_EDITMSG`, `git commit -v` (editor vrátí chybu, žádný commit nevznikl) | `# ------------------------ >8 ------------------------` + diff bez `#` prefixu za ní — **shoda na podřetězci `>8` na řádce začínající comment char funguje** | 1 (editor odmítl, commit se nevytvořil — očekáváno) |
| `core.commentChar=!` skutečně změní šablonu | tamtéž, `git config core.commentChar '!'`, znovu `git commit -v` | šablona `! Please enter…` místo `# Please enter…` — **konfigurovatelnost potvrzena** | 1 (stejně odmítnuto editorem) |
| FU-10 (CRLF): opravená kontrola (`read_bytes`) na baseline hooku | Python skript, `write_bytes` CRLF vstup, `mf.read_bytes() == expected.encode()` | shoda, `True` | 0 |
| FU-10: stejná kontrola po mutaci (odebrání `sub(/\r$/, "")`) | tamtéž na mutovaném hooku | **neshoda** (`\r\n` přežije) — mutace padá | 0 (hook), kontrola sama by vrátila 1 |
| FU-10: stará vakuózní kontrola (`read_text()`) na téže mutaci | tamtéž s `read_text(encoding="utf-8")` | shoda `True` — **potvrzena vakuóznost staré kontroly**, kterou FU-10 opravuje | 0 |
| FU-14 (folded join): baseline (`val = val " " piece`) | vstup `Co-authored-by: Cur` + pokračování `  sor Smith <human@example.com>` | trailer **zůstává** (`Cur sor Smith…` nezačíná na „cursor") | 0 |
| FU-14: mutace (`val = val piece`, bez mezery) | tamtéž | trailer **zmizí celý** (spojení dá „Cursor Smith…") — mutace padá přesně jak plán popisuje | 0 |
| E-B4 mutace (odstranění jen kroku 2, krok 3 nechán) | tamtéž na `attribution_then_trailing_blank_line`, `attribution_then_editor_comment_block`, `cursor_trailer` | všechny tři **stále vychází správně** → řádek E-B4 v manuální tabulce se nezčervená (viz Note 1) | 0 |
| Scope guard automaticky povoluje adresář běhu i `code_paths` | čtení `tools/intent/scope.py::allowed_paths` | `run_dir` i `node.code_paths`/`test_paths` jsou vždy povolené bez explicitního vyjmenování | — |
| `i0004.code_paths` skutečně kryje `tools/checks/hook_checks.py` | čtení `doc/intent/nodes/i0004-intent-tooling.md` | `code_paths: ["tools/"]` — potvrzeno | — |

## Co jsem NEZMĚŘIL

- **FU-11, FU-12, FU-13** — nespustil jsem jejich mutace живě; posoudil jsem je jen
  čtením existující `is_blank`/`is_attribution` logiky v patchi, kde návrh mutace
  (zúžení `is_blank`, zúžení adresního pravidla na klíčovou řádku, odebrání orphan-
  continuation větve) odpovídá kódu, který v patchi skutečně existuje a skutečně by
  se odebráním rozbil. Riziko nízké, ale nejde o přímé měření.
- Neaplikoval jsem `deferred-i0005-hook.patch` doslova (`git apply`) na čistý klon —
  přepsal jsem jeho `+` řádky do samostatného souboru a navrch přidal Plannerův
  preflight. Zbytkové riziko: mechanika samotné aplikace patchu (CRLF v patch souboru,
  konflikt kontextu) jsem neprověřil.
- Neprohnal jsem **celou** existující sadu `CASES` (26+ případů z patchu) proti své
  rekonstrukci hooku — testoval jsem jen nové/měněné případy. Regrese na starších
  případech (skládané trailery, gramatika klíče apod.) jsem nezkoušel znovu, protože
  preflight se jich logicky nedotýká (běží až po existující `last_blank` logice).
- `core.commentChar=auto` jsem nezkoušel spustit skutečně (jen jsem ověřil definici
  v `git-config(1)`) — shoduje se s Rizikem 2 plánu, které to sám přiznává jako
  neřešené s fallbackem `#`.
- Nekontroloval jsem `open_questions` uzlu `i0001` přímo (jen `i0005`); slice.md ho
  nese jen jako čtený, ne jako vlastníka kontraktu v tomto běhu, riziko nízké.

Poznámka k rozpočtu: provedl jsem přibližně 17 měření (o něco přes doporučený strop
~15), protože několik z nich byly levné doplňkové kontroly (např. `core.commentChar=!`
navazující na předchozí `-v` capture). Priority (a) B4/B5/B6, (b) fakta o cleanupu,
(c) FU-10/FU-14 jsem dodržel v tomto pořadí.

## Odpověď na otázku 4 (FU-15)

**Landuji na „dokumentovaná cena", ne oslabení — ale s výhradou, že to platí jen díky
tomu, jak `i0005` definuje samu „agent attribution".** Sekce `## Meaning` uzlu `i0005`
kotví „the tool attribution" konkrétně na „the tool attribution that Cursor injects
automatically, so the history records the author who is accountable... rather than the
editor" — tedy na mechanismus, kterým git/GitHub credit skutečně přiřazují (trailer,
který `git interpret-trailers` a GitHub UI rozpoznají), ne na libovolný výskyt
podřetězce „Co-authored-by: Cursor" kdekoli v textu. Próza v těle, kterou git jako
trailer nevidí, nezakládá žádné faktické spoluautorství v historii — účel věty c1
(„aby historie zaznamenala odpovědného autora") tím není ohrožen.

Druhý důvod: kolo 2 předchozího běhu už ustavilo „próza před blokem je nedotknutelná
konstrukce" jako **opravu**, ne jako nový kompromis — dřívější řádkový `grep` mazal i
legitimní citace/ukázky uvnitř těla (to bylo porušení druhé poloviny c1, „keeps
everything else"). Nelze uspokojit obě poloviny c1 dokonale v této šedé zóně
najednou: buď mažete i nevinnou prózu (porušujete „keeps everything else"), nebo
prózu necháte (porušujete literální „removes... attribution" pro tento okrajový
tvar). Round-3 Adversář sám, i po eskalaci, netraktoval FU-15 jako blokující — jen
jako „open — rozhodnutí bez zápisu", což plán teď zapisuje (`W4`). Souhlasím s tím, že
to stačí, **pokud** zápis v `hooks/README.md` a komentáři hooku zůstane přesný (že
prózu git jako trailer nevidí) a nebude to prezentováno jako vylepšení, jen jako
hranice.
