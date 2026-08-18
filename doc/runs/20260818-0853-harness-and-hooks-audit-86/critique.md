---
run_id: 20260818-0853-harness-and-hooks-audit-86
intent_ids: ["i0001", "i0005", "i0003", "i0004", "i0002"]
role: Critic
model: cursor-grok-4.5-high
complexity: high
status: done
---

# Kritika plánu

## Verdikt
REVISE

## Blockers

1. **Oprava `hooks/git/commit-msg` není na trailerech nadmnožinou dnešního chování** —
   `plan.md:107-112` a `:186-194` tvrdí oboustranné utažení (trailery ⊇ dnešek, próza ⊆).
   Reprodukce (scratch, současný hook vs. regex z plánu beze změny):

   ```
   vstup:  Co-authored-by: CursorAgent <bot@example.com>
   dnes:   řádek smazán
   návrh:  řádek zůstane
   ```

   Totéž pro `Co-authored-by: Cursor-bot <…>` a `Co-authored-by: CursorXYZ`. Příčina je
   kotva `([[:space:]<]|$)` za `cursor` v navrhovaném `grep -viE`. To je oslabení půlky
   „removes agent attribution“ na trailerech, ne utažení. Buď regex přepište tak, aby na
   trailerech opravdu mazal **nadmnožinu** toho, co maže dnešní neukotvený
   `grep -v "Co-authored-by: Cursor"`, nebo zastavte a zeptejte se Humana — Critic nesmí
   odkývat tiché oslabení bez intent delty. (Próza typu „Never write Co-authored-by:
   Cursor …“ je jiný případ: tam návrh posiluje „keeps everything else“ a pod Meaning uzlu
   to attribution není.)

## Major (neblokuje samo, ale musí se vypořádat v revizi)

- **`intent_ids` bez `i0002`.** FU-D sahá na `rules/07-run-artifacts.mdc` (`code_paths`
  `i0002`). Scope guard i tak projde, protože cesta je v `outputs` a `intent scope` bere
  deklaraci, ne `intent_ids`. Položka 6 v „Co patří Humanovi“ je ale **špatně zařazená**:
  nejde o rozhodnutí Humana, nýbrž o hygienu front matteru plánu/Coordinatora. Doplňte
  `i0002` do `intent_ids` v `plan.md` (a v `request.md`); `slice.md` už uzel má.

## Verdikt k hlavnímu tvrzení o hooku

- **Není čisté utažení**, dokud platí regex z `plan.md:190-192`. Na trailerech existují
  zprávy, kde dnešní hook attribution (substring `Co-authored-by: Cursor…`) maže a návrh
  ne. Na formách, které Cursor skutečně vstřikuje (`Co-authored-by: Cursor <cursoragent@…>`,
  plus `Made-with: Cursor` / `Co-Authored-By: …` z `commands/push.md`), návrh maže víc —
  ty poloviny jsou v pořádku. Mezera je právě `Cursor` jako prefix delšího tokenu.
- **„removes agent attribution“ po opravě:** poctivě jen vůči Meaning uzlu
  (`i0005-git-hooks.md:28-31` — attribution, kterou vstřikuje **Cursor**) a vůči seznamu
  v `commands/push.md`. Vůči nejširší angličtině věty c1 je enforcer vždy jen výčet, který
  si kontrola zvolí (`CASES`). To samo o sobě není blocker tohoto běhu; položka 5 (Claude
  a jiní agenti) je správně Human / intent delta.

## Auditovací tabulka — co jsem přeměřil sám

Metoda z `skills/ice-review/SKILL.md` Step 3 je pro `cmd:` správně přizpůsobená (exit
enforceru místo unittest sady). Scratch `/tmp/plan-audit-critic/repo`, po každé mutaci
reverze; pracovní strom repa mimo tento `critique.md` nezměněn.

| # | Tvrzení plánu | Moje měření |
|---|---|---|
| 1 | closed — rozbitý odkaz v `rules/*.mdc` | **souhlas** — exit 1 |
| 2 | closed — rozbitý odkaz v `skills/*/SKILL.md` | **souhlas po správné mutaci href** — naivní `str.replace` jednou rozbije jen text v `[…]`, ne cíl v `(…)`, a check zůstane zelený; `re.sub` jen na `](…)` → exit 1. Místo je uzavřené; recept mutace v tabulce je nepřesný. |
| 5 | closed rozhodnutím — odkaz v ohradě | **souhlas** — exit 0 |
| 10 | closed rozhodnutím — odkaz na adresář | **souhlas** — exit 0 |
| 12 | closed — chybí `.cursor/rules` | **souhlas** — exit 1 |
| 14 | closed — skutečný adresář místo symlinku | **souhlas** — exit 1 |
| 15 | closed — visící symlink | **souhlas** — exit 1 |
| 22 | closed — smazání `Intent:` | **souhlas** — exit 1 |
| 29 | closed — bez `awk` stage | **souhlas** — exit 1 |
| 31 | closed — `chmod -x` commit-msg | **souhlas** — exit 1 |
| 3 | open — `skills/*/reference.md` | **souhlas** — exit 0 |
| 16 | open — symlink na `../doc` | **souhlas** — exit 0 |
| 18/19 | open — jedna z dvou grep stages pryč | **souhlas** — exit 0 (oba markery na jedné SAMPLE řádce) |
| 20 | věta nepravdivá teď — `Made-with: Cursor` | **souhlas** — řádek přežije |
| — | 0 relativních odkazů mimo ohradu v `rules/` | **souhlas** |

Žádné místo označené *closed* jsem po korektní mutaci nenašel falešně uzavřené. Nejhorší
riziko tabulky u #2 je nepřesný recept mutace, ne falešný verdikt closed.

## Domov `test_checks.py`, ownership, coverage

- `from checks import hook_checks, template_checks` pod
  `python3 -m unittest discover -s tools/intent/tests -t tools` **funguje** (ověřeno
  dočasným testem, pak smazán).
- `ruff check tools/` — clean.
- `intent owner tools/checks/*.py` → `i0004` (už teď přes `code_paths: ["tools/"]`).
  Nový test pod `tools/intent/tests/` patří do `test_paths` téhož uzlu; **nepřesouvá**
  vlastnictví `tools/checks/` na cizí uzel. `coverage` dál hlásí `files outside: 0`
  (skenuje jen `DEFAULT_CODE_ROOTS`, ne rootový `hooks.json` — proto owner≠coverage u
  položky 3).

## `code_paths` / scope / FU-D / limity / zužování checků

- **Scope** s deklarovanými `outputs` projde i bez `i0002` v `intent_ids` (viz Major).
- **FU-D:** rozhodnutí „soubor“ přidává artefakty (`request.md`, `status.md` vedle
  `run.md` + už odděleného `grader.md`), nic z povinného nebere. Jediné metodické místo s
  `sections: request` je `rules/07-run-artifacts.mdc:20`; `skills/ice-run/SKILL.md:144` už
  `request.md` jako soubor chce. `_policy.yaml` (`evidence_profile: standard` → `grader.md`)
  zůstává splnitelný. Souhlasím s opravou i pro `status.md` (rozpor `:20` vs `:129`).
- **Limity** (`template_checks.py`): `07-run-artifacts.mdc` 141→143 ≪ 250 (globs);
  `ice-review` 133→135 ≪ 500; `ice-run` 156 ≪ 500. Na `tools/` limity 150/250/500
  nesahají.
- **Šest prodloužení enforcerů** z plánu (rglob, unterminated fence, cíl symlinku, CASES
  bajtová rovnost, objevování hooků, mód v indexu) jsem neviděl přijmout něco, co dnešní
  check odmítá — všechna jdou směrem přísněji. Jediné oslabení je v **navrhovaném hooku**,
  ne v check skriptech.

## Šest položek „Human, ne tento běh“

| # | Klasifikace Plannerem | Můj soud |
|---|----------------------|----------|
| 1 | Rozšíření c1 na README/commands/runs | **správně Human** — změna textu kontraktu |
| 2 | `.cursor/commands`, `.cursor/hooks.json` | **správně Human** — mimo větu c2 |
| 3 | `hooks.json` bez ownera | **správně Human** (intent delta); rozpor owner/coverage je reálný a vysvětlený skenem roots |
| 4 | Domov `tools/checks/tests/` + VERIFY | **správně Human** — `VERIFY.md` |
| 5 | Attribution jiného agenta než Cursor | **správně Human**; Meaning už teď zužuje na Cursor |
| 6 | Chybějící `i0002` v `intent_ids` | **špatně jako Human** — hygiena front matteru / Coordinator; scope stejně projde |

## Co jsem ověřil příkazy

- Současný vs. navrhovaný `commit-msg` na ≥15 zprávách (včetně `Made-with`, capitalised
  key, body quote, attribution-only, human co-author, Run slug s `cursor`, CursorAgent).
- Mutace closed/open míst výše na scratch kopii; baseline obou check skriptů exit 0.
- `intent owner`, `intent coverage`, import pod `-t tools`, `ruff check tools/`.
- `wc -l` na rule/skill souborech z DoD.
- Pracovní strom: měněn jen
  `doc/runs/20260818-0853-harness-and-hooks-audit-86/critique.md`.

## Čemu věřím nejméně

Zda musí `Co-authored-by: CursorAgent` počítat jako „attribution“ pro test nadmnožiny, když
Cursor takovou formu nevstřikuje. I kdyby Meaning řekl ne, **tvrzení plánu o trailerové
nadmnožině** je empiricky nepravdivé — a to stačí k REVISE bez filozofie o významu slova
attribution.

---

# Kritika plánu — kolo 2

## Verdikt
ACCEPT

Blokátor z kola 1 je uzavřený. Opravený regex (předpona `cursor` + klíč `-by`/`-with` na
jmenné větvi; adresní větev bez omezení klíče) je na attribution trailerech **změřená**
nadmnožina dneška; jediné místo, kde nový hook maže méně, je próza/subjekt citující
marker — utažení „keeps everything else". Implementace může začít.

## Blockers
žádné

## Vlastní měření nadmnožiny

Scratch `/tmp/hook-critique-r2`; `old` = dnešní `hooks/git/commit-msg`, `new` = regex z
`plan.md:277`. Každá zkušební řádka v trailer bloku skutečné zprávy (subjekt + tělo +
`Intent:`/`Run:`). Kritérium: žádná neprázdná řádka, kterou `old` smaže, nesmí v `new`
přežít — kromě očekávané výjimky prózy (keep-half).

| Případ | Výsledek |
|---|---|
| `Co-authored-by: CursorAgent <bot@example.com>` | oba maží |
| `Co-authored-by: Cursor-bot <bot@example.com>` | oba maží |
| `Co-authored-by: CursorXYZ` | oba maží |
| **INV** `Co-authored-by: Cursory review helper <x@y.com>` (prefix `Cursor`) | oba maží |
| **INV** `Co-authored-by: Cursed Soul <x@y.com>` (Cursor-like, ne prefix) | oba nechávají |
| **INV** `  Co-Authored-By: CursorAgent <…>` (odsazení + caps) | `old` nechá, `new` maže ⊃ |
| **INV** vícetrailerový blok (Ivo + CursorAgent + Signed-off-by adresa + Made-with) | `old` maže dvě attribution řádky; `new` totéž + `Made-with` ⊃; Ivo zůstane |
| próza `Never write Co-authored-by: Cursor by hand.` | `old` maže, `new` nechá ⊂ (očekáváno) |

**Trailer-superset violations: 0.** Žádná řádka smazaná dnes na trailerech v `new`
nepřežila.

## Adresní větev bez omezení klíče — nutná

Kdyby adresní větev sdílela filtr `-by`/`-with`, test nadmnožiny spadne. Změřeno variantou
s oběma větvemi omezenými na `-by`/`-with`:

| Řádka | `old` | `new` (plán) | `addr` omezená |
|---|---|---|---|
| `Note: mail cursoragent@cursor.com for access` | maže | maže | **nechá** ← porušení |
| `X-Agent-Id: build <cursoragent@cursor.com>` | maže | maže | **nechá** ← porušení |
| `Cc: cursoragent@cursor.com` | maže | maže | **nechá** ← porušení |
| `Reported-by: someone <cursoragent@cursor.com>` | maže | maže | maže (končí na `-by`) |

Asymetrie je nutná. Příklady `Note:` / `X-…:` / `Cc:` to dokazují ostřeji než samotné
`Reported-by:` z plánu (to by prošlo i s omezením, protože klíč končí na `-by`).

## E12 a subjekt `docs: Cursor attribution note`

- **E12** (jmenná větev s tokenovou kotvou `cursor([[:space:]<]|$)` místo předpony):
  `CursorAgent`, `Cursor-bot`, `CursorXYZ` v traileru **přežijí** — nový enforcer s
  `CASES` `cursor_agent_prefix` / `cursor_hyphen_bot` / `cursor_xyz` by tedy exit 1,
  jak plán slibuje.
- **Subjekt** `docs: Cursor attribution note`: `new` i E12-token (stále s `-by`/`-with`)
  ho **nechají**; plný regex z kola 1 (libovolný klíč + token) ho **maže**. Nález plánu
  o vadě round 1 potvrzen; oprava klíčem `-by`/`-with` je správná pojistka.
- Opravený hook proti **nezměněné** dnešní `hook_checks.py` → exit 0 (vakuum enforceru
  vůči větě dál platí).

## `Cursorina Smith`

**Přijatelná cena předpony, ne důvod pro Humana.** Dnes i po opravě se
`Co-authored-by: Cursorina Smith <c@x.com>` maže stejně (změřeno). Není to regrese ani
zúžení věty; rozlišit člověka od agenta podle křestního jména hook nemá a plán to
nezakrývá. Rozhodnutí z A3b, že `CursorAgent` **je** attribution (push.md substring +
„similar AI/Cursor trailer" + Meaning), beru — otevřená otázka z konce kola 1 je tím
uzavřená texty v repu, ne definicí Kritika.

## Co z kola 1 se nepohnulo

- Audit closed/open verdikty — beze změny; recept mutace řádku 2 A1 teď říká `](…)`.
- Šest prodloužení enforcerů — stále jen utahují.
- Domov `test_checks.py` pod `tools/intent/tests/` — beze změny, pořád OK.
- FU-D, limity, `outputs` (9) + `incidental` (1) — beze změny.
- `intent_ids` obsahuje `i0002`; `intent scope --run …` → `scope clean (10 declared
  path(s))`. Major z kola 1 tím odpadá.
- Pět Human položek zůstává; položka 5 rozšířená o `Tool: Cursor` je pořád Human
  (trailer bez `-by`/`-with` a bez adresy — ani dnes se nemaže).

## Stále otevřené (neblockuje)

Jen Human-teritorium z plánu (README/commands/runs; `.cursor/commands`+`hooks.json`;
owner `hooks.json`; domov testů + `VERIFY.md`; attribution mimo Cursor včetně
`Tool: Cursor`). Nic z toho nebrání Codera.

## Co jsem v kole 2 ověřil

- Superset tabulka výše; nutnost adresní větve; E12 vs. předpona; subjekt vs. full-r1;
  `hook_checks.py` exit 0 na novém hooku; `intent scope` exit 0.
- Pracovní strom: měněn jen tento `critique.md`.
