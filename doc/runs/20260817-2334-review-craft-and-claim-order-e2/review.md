---
run_id: 20260817-2334-review-craft-and-claim-order-e2
intent_ids: ["i0002", "i0003", "i0004"]
role: Adversary
model: claude-opus-5-thinking-high
complexity: high
status: done
rounds: 3
---

> **Aktuální verdikt je verdikt round 3 na konci tohoto dokumentu: APPROVE.**
> Záznamy round 1 a round 2 zůstávají nezměněné jako audit. Blokátor B1 (round 1) je
> opravený a ověřený konstrukcí; Major z round 1 (nárok na `low`) je opravený jako B6;
> Major a tři Minor z round 2 jsou opravené jako M1–M4 a v round 3 přeměřené.
> Otevřené po round 3: tři follow-upy (FU-B, FU-C, FU-D), žádný blokátor.

# Nezávislá recenze — round 1

Model Codera byl `cursor-grok-4.5-high`, můj je `claude-opus-5-thinking-high` — podmínka
`adversary_differs_from_coder` splněna.

Tato recenze má jednu zvláštnost: běh přepisuje `skills/ice-review/SKILL.md`, tedy skill,
kterým se řídím. Řídil jsem se jeho **novým** zněním z pracovního stromu, včetně nového
kroku 3, a co z něj nešlo splnit, píšu níž jako nález, ne jako svoji nešikovnost.

## Verdict

**REQUEST CHANGES** — jeden blokátor.

R6 je jinak hotové a ověřil jsem to vlastním pátráním, ne přečtením plánu: kanonická věta
je v platné metodice na **osmi** místech v sedmi souborech, znak za znak jedna, a devátý
výskyt starého pořadí v `rules/`, `skills/`, `README.md` ani `tools/` **neexistuje** —
včetně obou mermaid diagramů, všech checklistů a všech tabulek „kdo co píše". Přečíslování
kroků `ice-review` nezanechalo jediný zastaralý odkaz. `TreeError` se spojuje se správnou
mezerou a kanonickou větu opravdu nese v runtime hlášení, ne jen ve zdrojáku. R5 se na tomto
běhu sám aplikoval: `grader.md` je Coordinatorův a Coderova evidence je v `coder-evidence.md`.
Všech osm bran je zelených, rozsah neutekl, délky jsem přeměřil a sedí na řádek.

Blokátor je v tom jednom místě, kde diff sahá na mě: kontrola č. 8 předepisuje příkaz,
který na svou vlastní otázku odpovědět **nemůže**. Je to táž vada, kterou tento běh zavírá
(„věc opravená v jednom pohledu, netěsná v sousedním"), jen o pohled vedle — a je to
mechanická pojistka právě toho pořadí, kvůli kterému běh vznikl.

## Blockers

### B1 — kontrola č. 8 předepisuje příkaz, který nárok na tento běh neumí ukázat

`skills/ice-review/SKILL.md:40` — `$TOOL realization status --node <iNNNN>` nikdy nevypíše
`evidence` nároku, takže věta „no claim may cite this run yet" se tím příkazem nedá ověřit
ani vyvrátit. Reprodukce (spustil jsem to jako první vykonavatel té kontroly):

```
$ python3 tools/intent/cli.py realization status --node i0002
i0002  realized
        Rules
$ python3 tools/intent/cli.py realization status --node i0002 --json
{ "i0002": { "node": "i0002", "state": "realized", "acceptance": "not_required",
             "reasons": [], "blocked_by": null } }
```

`evidence` v tom výstupu není a není v **žádném** výstupu: `claim.evidence` se v celém
nástroji tiskne jedinkrát, a to v `tools/intent/main.py:264` při samotném zápisu nároku.
Ověřeno i negativně — `realization status`, `realization summary` a `realization worklist`
dohromady nevypíšou ani jeden řetězec `doc/runs`.

Praktický důsledek na **tomto** běhu: uzly `i0002` a `i0004` jsou `realized` z běhů
`20260817-1743` a `20260817-1853`. Předepsaný příkaz mi u dvou ze tří uzlů vrátí `realized`
bez ohledu na to, jestli se nárok předběhl, nebo ne. Adversář, který kontrolu vezme
doslova, buď nahlásí blokátor, který neexistuje, nebo — a to je horší — si odvykne
považovat `realized` během recenze za signál. Fungovala mi jen u `i0003`, který je
`not_claimed`, tedy náhodou, ne konstrukcí.

Předchozí znění bylo taky nepřesné (`realization check` `evidence` netiskne), ale aspoň
`evidence` **jmenovalo**. R6-i ho vyměnilo za příkaz, který ukazuje ještě méně, a udělalo
to na kontrole, která má nové pořadí vynucovat.

**Co musí změnit** (jedna buňka tabulky). Realizační vrstva je verzovaná a scope guard ji
vždy povolí, takže nárok zapsaný během běhu je vidět právě v diffu toho souboru:

```markdown
| 8 | Did a claim jump ahead of you? | `git diff -- doc/intent/_realization.yaml` must add no claim citing this run; `$TOOL realization check` exits 0 — the claim comes after your verdict |
```

Ověřil jsem, že tahle varianta funguje a na tomto běhu dává správnou odpověď:
`git status --porcelain doc/intent/_realization.yaml` je **prázdný**, tedy žádný nárok se
přede mě nepředběhl. `doc/intent/_realization.yaml` je `git ls-files`-tracked, takže se
na diff dá spolehnout.

## Major

### M1 — `low` běh se k nároku textově dostane, ale mechanicky ne

Textovou procházku `low` během změněným textem jsem udělal a **kontradikci v něm nenašel**:
krok 7 (`Record no realization claim here … at `low`, where no Adversary runs, the gates are
the whole requirement. Either way the claim belongs to Step 9`), krok 9 („at `low` that is
the green Grader"), output checklist, `07-realization.mdc:80` a `:132–134`,
`07-run-artifacts.mdc:84–89`, `README.md:257` i terse řádek v `07-ice-workflow.mdc:45` —
každé z těch míst je pravdivé i o `low` a žádné z nich by `low` běh nezastavilo. Kanonická
věta tuhle práci odvádí správně a rozhodnutí Plannera nechat always-applied řádek bez výčtu
úrovní obhájím.

Zastaví ho ale **nástroj**, a to z důvodu, který změněný text nezmiňuje.
`rules/07-run-artifacts.mdc` předepisuje pro `low` jediný `run.md` (bez `grader.md`),
zatímco `doc/intent/_policy.yaml` má `evidence_profile: standard`, tedy „a claim must point
at a run directory containing grader.md". Reprodukce na scratch kopii:

```
$ mkdir doc/runs/20260818-0800-low-run-test-zz   # jediný run.md, dle low konvence
$ python3 tools/intent/cli.py realization claim i0003 \
    --evidence doc/runs/20260818-0800-low-run-test-zz --by Coordinator
intent: R3 i0003: evidence doc/runs/20260818-0800-low-run-test-zz is not a run directory
        with grader.md (evidence_profile: standard)          exit=2
$ touch doc/runs/20260818-0800-low-run-test-zz/grader.md   # a hned to projde
i0003 claimed against doc/runs/20260818-0800-low-run-test-zz — now realized    exit=0
```

**Není to vada tohoto diffu** — kolize `low`/`run.md` versus `_policy.yaml` je starší a
staré pořadí („once `grader.md` is green") ji mělo úplně stejně. Uvádím to jako Major
proto, že R6 z nároku dělá **závěrečný krok každého běhu na každé úrovni**, takže se ta
díra z náhody stává něčím, na co `low` běh narazí systematicky. Oprava je jednou větou
v `07-run-artifacts.mdc` („at `low` the gate log is a `grader.md` beside `run.md`") — ale
druhá polovina té volby leží v `_policy.yaml`, a to je soubor Humana, takže to **eskaluji**,
ne požaduji.

### M2 — druhé odvozovací místo `c12` do sady nevstupuje

Věta `c12` („A realization claim signed by the Coder is refused") se v `tools/` odvozuje
**dvakrát**: v `claim()` (`tools/intent/realization.py:546`, zápisová odmítnutí) a v
`check()` (`:480`, hlášení `R6 … a claim may not be written by the Coder` nad už zapsanou
vrstvou). Mutoval jsem obě:

```
:546  == "coder" → == "coderx"   → FAILED (failures=1), padá právě
                                    test_coder_may_not_claim_its_own_work
:480  == "coder" → == "coderx"   → Ran 82 tests … OK      ← sada zůstává zelená
```

Druhé místo je jediná pojistka proti nároku, který někdo zapíše přímo do
`doc/intent/_realization.yaml` místo přes CLI, a žádný test do něj nevstoupí.

**Proč to nedávám jako blokátor**, přestože nový krok 3 říká, že takové místo blokátor je:
je starší než tento běh, běh na něj nesáhl, a `critique.md` round 3 ho **vědomě odložil**
(„Stejná záměna na druhém výskytu … → celá sada OK — mutace na špatném místě tedy důkaz
nepředá") — tedy Kritik ho vyhodnotil jako nesprávné místo pro důkaz `c12`, ne jako
otevřenou hranici. To čtení je hájitelné: `claim()` opravdu „refuses", `check()` nálezy
jen hlásí. Zapisuji to jako **follow-up** s hotovým zadáním: jeden test, který napíše
`by: Coder` do vrstvy ručně a čeká nenulový exit z `realization check`.

Tenhle rozpor mezi mým verdiktem a doslovným zněním kroku 3 je zároveň nález o kroku 3 —
viz níž.

## Minor / non-blocking

1. **Kontrola č. 4 ukazuje na krok, který o jejích testech nemluví.**
   `skills/ice-review/SKILL.md:36` se ptá „Do the new tests actually cut?" a posílá na
   „Step 3", ale nový krok 3 je o větách kontraktu z `slice.md`; o testech, které běh
   napsal, je krok **4**. Technika mutace v kroku 3 opravdu je, takže odkaz není nepravdivý,
   jen míří o krok dřív, než čtenář čeká.
2. **Pátrání plánu po `doc/new_ideas/` obstálo jazykovou náhodou.** `plan.md:153` tvrdí,
   že tam „žádný výskyt" starého pořadí není. Vzorce ale byly anglické, kdežto ty dokumenty
   jsou české a staré pořadí nesou:
   `doc/new_ideas/gemini3.5Flash.aktual_review.260817_6050.md:691` („Koordinátor, poté co je
   Grader zelený"), `:738`, a `doc/new_ideas/intent-realization.Opus5.md:427` („po zeleném
   `VERIFY.md` následuje `realization claim`"). Human `doc/new_ideas/` z rozsahu vyňal,
   takže to **není** nález o diffu — je to nález o metodě pátrání: predikát nad volným
   textem v jednom jazyce nedokazuje čistotu dvojjazyčného repozitáře.
3. **`realization.py` je v tabulce plánu dál o řádek jinde, ale Coder to přiznal a měřil.**
   `wc -l` dává **697**, `report.md:140` to jako odchylku uvádí. Přeměřil jsem všech osm
   souborů sám; ostatních sedm sedí na řádek.
4. **R5-d nic neoslabuje.** Přesun failing-test evidence z `grader.md` do `report.md`
   ladí pravidlo s `skills/ice-implement/SKILL.md:58` („Paste that output into `report.md`")
   a s bodem v kroku 4 `ice-review`, který `report.md` jmenoval už předtím (diff se ho
   nedotkl). Že tu evidenci nikdo strojově nepřebíhá, je starší stav, ne důsledek R5.

## Je nový krok 3 skutečně vykonatelný, jak je napsaný?

**Ano, splnil jsem ho celý** — všech osm vět kontraktu ze slice, každou samostatnou mutací,
enumerace je níž. Pro běh, který nemění chování, funguje překvapivě dobře: „kód" se čte
jako „to, na co vynucovač sahá", a u `i0002`/`i0003` to jsou samotné soubory pravidel a
skillů. Čtyři místa bych přesto upravil, a všechna čtyři jsem narazil při vykonávání, ne
při čtení:

1. **„Mutate a scratch copy, never the working tree, and revert byte-exact after each
   mutation" si protiřečí.** Když mutuji jen kopii, v pracovním stromu není co revertovat;
   „revert byte-exact" naopak předpokládá zásah na místě. Rozhodl jsem to tak, že mutuji
   a revertuji **uvnit** kopie a na konci porovnám kopii s pracovním stromem
   (`diff -r --brief` → `rules` i `skills` bajtově shodné, `realization.py` shodný).
   Věta by měla říct právě tohle: revertuj v kopii a shodu s pracovním stromem si na konci
   dokaž.
2. **Chybí výjimka pro kontrakty s `enforced_by: review`.** „A place where the sentence
   turns false and the suite stays green is a **blocker**" u kontraktu bez testu platí
   z definice **vždy** — každá mutace nechá sadu zelenou, protože žádná sada tam není.
   Doslovné čtení tedy z každého review-kontraktu dělá automatický blokátor, přestože
   `rules/07-ice-workflow.mdc` je výslovně přiděluje Humanovi a `intent coverage` je umí
   vyjmenovat. Dneska to nekouslo (`review exceptions: 0`), v cizím projektu kousne hned.
3. **„even when the diff did not create it" nemá vazbu na rozsah běhu.** Doslova aplikované
   je M2 blokátor běhu, který změnil tři řádky jednoho řetězce. Rozhodl jsem se M2
   neblokovat a napsal jsem proč — ale to rozhodnutí by mělo být ve skillu, ne v úvaze
   Adversáře. Chybí jedna věta typu: místo, které běh nezaložil ani nedotkl, je blokátor
   jen tehdy, když ho běh **tvrdí** za uzavřené (v plánu, v Definition of Done, nebo
   nárokem na realizaci).
4. **Spouštěč enumerace nevystřelí u recenzí, které skončí dobře.** „Before your third
   verdict" znamená, že tabulka „Where the contract reaches" vznikne jen v nejhorším
   případě. `request.md:62-65` ji přitom chtěl jako **pravidlo ukončení** — a ukončení
   nastává i tehdy, když Adversář schválí v prvním kole, jako teď. Tabulku proto přikládám
   dobrovolně; skill by ji měl žádat u **posledního kola, které Adversář opravdu píše**,
   ne u třetího.

Nic z těchhle čtyř věcí není blokátor: krok 3 je vykonatelný, jen na čtyřech místech
nechává rozhodnutí na tom, kdo ho čte. Ostatní části R7 (schematická tabulka bez živých
jmen z tohoto repozitáře, „Do not conclude from reading", `Where the contract reaches`
v šabloně) jsou podle mě přesně to, co má být napsané.

## Where the contract reaches

Vše na scratch kopii `/tmp/ice-scratch` (celý repozitář včetně `.cursor` symlinků, zelený
baseline), po každé mutaci reverze a na konci bajtová shoda s pracovním stromem. Kopie je
smazaná, `git status` má pořád právě osm změněných souborů a adresář běhu.

| # | Místo, kam věta sahá | Mutace | Sada | Stav |
|---|---|---|---|---|
| 1 | `template_checks.py:73` — `i0002` c2, půlka `alwaysApply` | +40 řádků do `rules/07-ice-workflow.mdc` | `158 lines exceeds the alwaysApply limit of 150`, exit 1 | uzavřeno |
| 2 | `template_checks.py:73` — `i0002` c2, půlka `scoped` | +100 řádků do `rules/07-realization.mdc` | `255 lines exceeds the scoped limit of 250`, exit 1 | uzavřeno |
| 3 | `template_checks.py:99` — `i0003` c2, limit skillu | +400 řádků do `skills/ice-review/SKILL.md` | `526 lines exceeds the skill limit of 500`, exit 1 | uzavřeno |
| 4 | `template_checks.py:70` — `i0002` c1, deklarace aktivace | vyřadit `description` i `globs` z front matteru `07-run-artifacts.mdc` | `needs a description, globs, or alwaysApply: true`, exit 1 | uzavřeno |
| 5 | `template_checks.py:94` — `i0003` c1, `name` ve SKILL.md | `name:` → `nam3:` v `ice-review` | `front matter is missing 'name'`, exit 1 | uzavřeno |
| 6 | `template_checks.py:128` — `i0001` c1, odkazy ve skillu | `../../rules/07-realization.mdc` → `-x.mdc` | `broken link: ../../rules/07-realization-x.mdc`, exit 1 | uzavřeno |
| 7 | `template_checks.py:136` — `i0001` c2, `.cursor` symlinky | odklidit `.cursor/skills` | `expected a symlink so Cursor discovers this directory`, exit 1 | uzavřeno |
| 8 | `realization.py:546` — `i0004` c12, odmítnutí v `claim()` | `== "coder"` → `== "coderx"` | `FAILED (failures=1)`, padá **právě** `test_coder_may_not_claim_its_own_work` | uzavřeno |
| 9 | `realization.py:480` — `i0004` c12, hlášení `R6` v `check()` | `== "coder"` → `== "coderx"` | `Ran 82 tests … OK` | **otevřeno → M2** |

Devět míst, osm uzavřených, jedno otevřené a vědomě neblokující. Půlky, u kterých se dá
uklouznout, jsem mutoval zvlášť — `i0002` c2 má dvě („always-applied … a scoped rule"),
`i0001` c1 dvě plochy (`rules/*.mdc` i `skills/*/SKILL.md`), `c12` dvě odvozovací místa.
Mimo tabulku jsem ověřil, že mutace 8 neshodí nic jiného, tedy že signál nic nezakrývá.

## R6 — vlastní pátrání po devátém místě

Nepoužil jsem vzorce plánu. Vypsal jsem **každý** řádek se slovem `claim` (case-insensitive)
v `rules/`, `skills/`, `README.md`, `VERIFY.md`, `AGENT_MODELS.md`, `doc/intent/`, `tools/`,
`commands/` a `hooks/`, a pak jsem ho filtroval na cokoli, co mluví o pořadí (`grader`,
`green`, `step`, `after`, `before`, `order`, `first`, `then`, `review`). Nezávisle na tom
jsem prošel celý repozitář včetně netrackovaných a ignorovaných cest.

- Kanonická věta: **8 výskytů v 7 souborech**, `full == sub == 8`, tedy **nula variant** —
  změřeno vlastním grepem přes `--include` masky nad celým repozitářem, ne nad seznamem
  souborů z plánu.
- `Grader is green`: prázdný. `green Grader`: právě dva výskyty a oba jsou správné —
  `rules/07-run-artifacts.mdc:84` větu **popírá**, `skills/ice-run/SKILL.md:116` ji
  **omezuje na `low`**.
- **Oba** mermaid diagramy v `README.md`: první (`:137-145`) po R6-k vede
  `GRADE → ADV → REV → CLAIM → CLOSE` s `ADV -- no --> CLAIM`, tedy `low` cesta k nároku
  vede taky; druhý (`:426-429`) měl nové pořadí `B4 → B5 → B6 → B7` už předtím. Kandidát
  `README.md:446` („Verification order … machine gates run first") mluví o V1 versus V2,
  ne o nároku, a je pravdivý.
- Neutrální zmínky, které jsem prověřil a **nepovažuji** za deváté místo:
  `doc/intent/_policy.yaml:12` (co je evidence, ne kdy se nárokuje),
  `rules/07-run-artifacts.mdc:109` (čísla v reportu versus log brány),
  `VERIFY.md:41` („step 7 … records the output in `grader.md`" — krok 7 dál brány spouští a
  `grader.md` píše, takže je to po R6 pořád pravda),
  `skills/commit-task/SKILL.md:178` (už dnes „Grader green, review closed"),
  `AGENT_MODELS.md`, `commands/push.md`, `hooks/`, `hooks.json`, `AGENT_MODELS.explanation.md`,
  uzly záměru, `MAP.md`, `INDEX.json`.
- `intent_tree_editor/` je prázdný adresář, `.veil` a `.ruff_cache` nic věcného nenesou.
- Staré pořadí zůstává jen v `doc/runs/` (audit, nepřepisuje se) a v `doc/new_ideas/`
  (mimo rozsah rozhodnutím Humana) — viz Minor 2.

**Devátý výskyt v platné metodice není.** Tvrzení plánu potvrzuji, ale z vlastního měření.

## R7 — přečíslování nikde neuniklo

Prošel jsem každý odkaz na číslo kroku v `rules/`, `skills/`, `README.md`, `VERIFY.md`,
`AGENT_MODELS.md` a `commands/`. Na kroky `ice-review` ukazuje **jediný** odkaz v celém
repozitáři, a je vnitřní: `skills/ice-review/SKILL.md:36` („Step 3"), a míří na nový krok 3
záměrně (R7-c). Žádný jiný soubor čísla kroků toho skillu necituje. Nadpisy jdou 1, 2, 3,
4, 5 bez duplikátu a bez děr; `slicing.py` ani `talks_to` v příkladové tabulce nezůstaly.
Odkazy `Step 8` a `Step 9` v `skills/ice-run/SKILL.md:99-100` a `:148` míří na kroky téhož
souboru a po R6-b sedí (`## Step 8 — Independent review`, `## Step 9 — Claim, then close`).
`VERIFY.md:41` mluví o kroku 7, který se nepřečísloval.

## R5 se na tomto běhu sám aplikoval

`doc/runs/20260817-2334-review-craft-and-claim-order-e2/` obsahuje `grader.md` **i**
`coder-evidence.md`. `grader.md:3` se hlásí ke Coordinatorovi („Run by the Coordinator,
2026-08-18T08:09:44+02:00") a osm příkazů v něm jsem si všech osm sám znovu spustil se
shodným výstupem a shodným exit codem — ten soubor tedy není Coderův výmysl. Coderova
měření (tři mutace, VERIFY, grepy) jsou v `coder-evidence.md`, tedy tam, kam je R5 posílá.
Žádný soubor se jménem, které jde přečíst jako `grader*`, Coder nevyrobil.

Nové znění **nezakazuje** nic, co metodika potřebuje: `07-run-artifacts.mdc:32` říká
o `grader.md` „never the Coder's", tedy zakazuje **autorství**, ne citaci. Coordinator může
Coderovu evidenci klidně zmínit odkazem a `report.md:97-98` to přesně takhle dělá.
Předchozí běh (`20260817-1853-slice-and-derived-truth-66/grader-evidence.md`) zůstal
nedotčený — `git status --porcelain` nemá pod `doc/runs/` nic než adresář tohoto běhu.

## `TreeError` — spojení segmentů, runtime text, kotvení testů

Nespoléhal jsem na čtení zdrojáku a hlášku jsem si vyvolal:

```
$ python3 tools/intent/cli.py realization claim i0002 --evidence doc/runs/<tento běh> --by Coder
intent: the Coder may not claim its own work; the Coordinator claims once every gate the level requires has passed
exit=2
```

Na hranici segmentů je **právě jedna** mezera (`work; ` + `the Coordinator`), nikde dvojitá,
a kanonická věta je v runtime hlášení znak za znak. Na text se nekotví žádný test:
`assertRaisesRegex`, `claims after the Grader` ani `every gate the level requires` se
v `tools/intent/tests/` nevyskytují (grep exit 1). Sada je `Ran 82 tests … OK` a počet
testů se nezměnil. `git diff -- tools/intent/realization.py` obsahuje jen ty tři řádky
uvnitř `raise TreeError(...)`, žádnou změnu chování.

## Délky — přeměřeno, ne přečteno

| Soubor | Aktivace | Limit | `wc -l` | Report | Rezerva |
|---|---|---|---|---|---|
| `rules/07-ice-workflow.mdc` | `alwaysApply` | 150 | 118 | 118 | 32 |
| `rules/07-realization.mdc` | `globs` | 250 | 155 | 155 | 95 |
| `rules/07-run-artifacts.mdc` | `globs` | 250 | 139 | 139 | 111 |
| `skills/ice-run/SKILL.md` | skill | 500 | 156 | 156 | 344 |
| `skills/ice-review/SKILL.md` | skill | 500 | 126 | 126 | 374 |
| `skills/ice-implement/SKILL.md` | skill | 500 | 108 | 108 | 392 |
| `README.md` | — | — | 652 | 652 | — |
| `tools/intent/realization.py` | — | — | 697 | 697 | — |

Osm z osmi sedí s `report.md`. Limity jsem si potvrdil mutací (řádky 1–3 enumerace), ne
přečtením konstant, a aktivaci jsem bral z front matteru týchž souborů, ne z tabulky plánu.

## Co jsem prověřoval nejtvrději a nenašel nic

**Existuje deváté místo, které tvrdí, že zelená brána na nárok stačí?** Tohle jsem tlačil
nejvíc, protože přesně v tom se plán mýlil dvakrát (Kritik našel osmé místo v `tools/`) a
protože jednou stačí jediný soubor čtený v izolaci a celé R6 je k ničemu. Prohledal jsem
repozitář **konceptem, ne vzorcem**: každý řádek se slovem `claim` v každém platném
adresáři, pak průsečík s devíti slovy o pořadí, pak celý repozitář ještě jednou na
`after the grader|grader is green|green grader|claims after|as soon as .*grader|once
.*grader.*green`, a to i v netrackovaných a gitignorovaných cestách. Vytáhl jsem si
kandidáty, které plán jmenuje jako „neutrální" (`_policy.yaml:12`, `VERIFY.md:41`,
`07-run-artifacts.mdc:109`, `README.md:446`), a přečetl je proti novému pořadí jednotlivě —
každý z nich mluví o **jiné** věci (co je evidence, kdo píše log brány, čemu se v reportu
věřit, V1 versus V2) a ani jeden neimplikuje, že nárok patří před recenzi. Prošel jsem oba
mermaid diagramy hranu po hraně a ověřil, že `low` cesta (`ADV -- no --> CLAIM`) k nároku
opravdu vede a že po R6-k první diagram druhému už neprotiřečí. Zkoušel jsem taky, jestli
se nová věta někde nerozešla o mezeru nebo o slovo — `full == sub == 8` znamená nula
variant, a to jsem měřil vlastním grepem nad `--include` maskami celého repozitáře, ne nad
seznamem cest z plánu. **Nenašel jsem nic.** R6 je v platné metodice úplné.

## Co jsem sám ověřil (příkaz → výstup → exit code)

| Příkaz | Výstup | Exit |
|---|---|---|
| `python3 tools/intent/cli.py validate` | `5 node(s): 0 error(s), 0 warning(s)` | 0 |
| `python3 tools/intent/cli.py realization check` | `realization layer consistent (2 entry/entries)` | 0 |
| `python3 tools/intent/cli.py realization status --node i0002` | `i0002  realized` (bez `evidence` → B1) | 0 |
| `python3 tools/intent/cli.py coverage` | `contracts: 28`, `machine-enforced: 28 (100%)`, `review exceptions: 0`, `files outside any node: 0` | 0 |
| `python3 tools/intent/cli.py scope --run doc/runs/20260817-2334-review-craft-and-claim-order-e2` | `scope clean (8 declared path(s))` | 0 |
| `python3 -m unittest discover -s tools/intent/tests -t tools` | `Ran 82 tests … OK` | 0 |
| `python3 tools/checks/template_checks.py --root .` | `template contracts satisfied` | 0 |
| `python3 tools/checks/hook_checks.py --root .` | `hook contracts satisfied` | 0 |
| `ruff check tools/` | `All checks passed!` | 0 |
| `ruff format --check tools/` | `19 files already formatted` | 0 |
| `wc -l` osm výstupů | `118 155 139 156 126 108 652 697` | 0 |
| `grep -rn "once every gate the level requires has passed"` (celý repozitář, `--include` masky) | 8 řádků / 7 souborů | 0 |
| `grep -rn "every gate the level requires"` | 8 řádků → variants = 0 | 0 |
| `grep -rn "Grader is green" rules/ skills/ README.md tools/` | prázdný | 1 |
| `grep -rn "green Grader" rules/ skills/ README.md tools/` | 2 řádky, obě správné | 0 |
| `grep -rn "assertRaisesRegex\|claims after the Grader" tools/intent/tests/` | prázdný | 1 |
| `git status --porcelain doc/intent/_realization.yaml` | prázdný — přede mě se nárok nepředběhl | 0 |
| `git status --porcelain` | právě 8 `M` + adresář běhu | 0 |
| devět mutací (tabulka výš) | osm řeže, jedna zelená | 1 / 0 |

Rozsah: `git diff --stat` je právě těch osm souborů z `outputs`, `incidental` je prázdné a
nic mimo ně se nezměnilo. Diff neobsahuje `doc/intent/nodes/`, `VERIFY.md`,
`AGENT_MODELS.md`, `doc/intent/_policy.yaml` ani nic pod `doc/runs/` mimo adresář tohoto
běhu; z `tools/` jen `tools/intent/realization.py`. Žádný nový podpříkaz nevznikl —
`grep -rnw "unclaim" tools/` je prázdný a dva výskyty v `rules/` a `skills/` to slovo
popírají, nezavádějí. Sám jsem nezměnil nic než tento `review.md`; scratch kopie je smazaná.

## Co tento diff dokazuje a co ne

**Dokazuje**, že staré pořadí nároku není v platné metodice ani na jednom místě a že nové
je vyslovené osmkrát jednou a touž větou, kterou nese i runtime hlášení nástroje; že
`grader.md` má v textu jediného autora; a že limity délky pravidel a skillů po zásahu drží
s rezervou, ověřeně mutací. **Nedokazuje**, že Adversář nový nárok umí zachytit — kontrola
č. 8 je dnes nefunkční (B1) a právě to je jediná mechanická pojistka R6. Nedokazuje, že
`low` běh nárok skutečně zapíše: textově ano, nástrojem ne (M1). A nedokazuje, že `c12`
platí všude, kde ji lze porušit: druhé odvozovací místo do sady nevstupuje (M2). Metodika
je po tomto běhu konzistentní **jako text**; jako stroj má tři místa, kde se na ni ještě
nedá spolehnout, a všechna tři jsou výš pojmenovaná s reprodukcí.

---

# Round 2

Řídil jsem se **novým** zněním `skills/ice-review/SKILL.md` z pracovního stromu, tedy verzí,
kterou tento běh po mém round 1 znovu přepsal. Vykonávám tak svůj vlastní krok 3 podruhé
a na změněné verzi jeho samotného; co z něj šlo a co ne, píšu níž jako nález.

## Verdict — round 2

**APPROVE.**

Všech šest položek je opravených a ověřil jsem každou vlastním spuštěním, ne přečtením
`report.md`. Nejdůležitější je B6, protože ta se dala pokazit tak, že by si toho nikdo
nevšiml — v repozitáři žádný `low` běh neexistuje, takže se na něm nedalo nic vyzkoušet.
Postavil jsem ho tedy sám a **nárok na `low` úrovni skutečně projde** (`exit=0`) proti
`_policy.yaml`, jak je dnes napsané. Kanonická věta je tím pravdivá na `low` nejen textově,
ale i strojově; M1 z round 1 je zavřená.

B1 jsem prověřil v obou směrech, včetně sestaveného kontrafaktu: nová kontrola č. 8 na
tomto běhu správně **projde** a v případě předběhnutého nároku správně **spadne**, a jméno
běhu je v tom diffu čitelné. Nic dalšího se nepohnulo: osm výskytů kanonické věty v sedmi
souborech, nula variant, přečíslování bez zastaralého odkazu, runtime text `TreeError`
i všech osm bran zelených, délky přeměřené.

Blokátor nemám žádný. Zbývá jeden Major o skladbě dvou vět v B4, tři Minor a jeden dřív
zapsaný follow-up. Protože běh končí u Humana, u každého píšu dispozici.

## Blockers

Žádný.

## Ověření šesti oprav

| # | Co bylo požadováno | Jak jsem to ověřil | Stav |
|---|---|---|---|
| B1 | kontrola č. 8 přes `git diff` vrstvy + `realization check` | oba směry sestavené na klonu s reálnou historií (níž) | **opraveno** |
| B2 | scratch kopie, restore po každé mutaci, na konci potvrdit nedotčený pracovní strom | řídil jsem se tím u devíti mutací; `diff -q` po každé reverzi, `git status` na konci | **opraveno** |
| B3 | `enforced_by: review` nejsou automatické blokátory | `skills/ice-review/SKILL.md:55-56`; `coverage` dnes hlásí `review exceptions: 0`, takže to zatím nekouše, ale je to pokryté | **opraveno** |
| B4 | věta nepravdivá **teď** = blokátor; jinak follow-up | aplikoval jsem to na M9 (`realization.py:480`) a vyšel správný výsledek — viz Major M3 k formulaci | **opraveno, s výhradou** |
| B5 | enumerace „When the review ends", povinná i v prvním kole | tabulka je níž; k formulaci spouštěče viz Minor 1 | **opraveno, s výhradou** |
| B6 | `low` = `run.md` **a** `grader.md`, odvozeno z R5; `_policy.yaml` beze změny | postavený `low` běh, nárok `exit=0`; `_policy.yaml` nedotčený | **opraveno** |

## B6 — sestavený `low` běh, protože v repozitáři žádný není

Postavil jsem `low` běh přesně podle nového `rules/07-run-artifacts.mdc:20-22`, tedy
`run.md` **a** vedle něj `grader.md`, a prohnal ho celým řetězem. Na čistém klonu
(prázdný `git status`), aby výsledek nezkresloval rozpracovaný strom:

```
$ ls doc/runs/20260818-0820-low-tier-clean-w3
grader.md  run.md

$ python3 tools/intent/cli.py scope --run doc/runs/20260818-0820-low-tier-clean-w3
scope clean (1 declared path(s))                                            exit=0

$ python3 tools/intent/cli.py realization claim i0003 \
    --evidence doc/runs/20260818-0820-low-tier-clean-w3 --by Coordinator
i0003 claimed against doc/runs/20260818-0820-low-tier-clean-w3 — now realized   exit=0
```

Tři věci, které z toho plynou, a všechny jsem chtěl vidět:

1. **Nárok na `low` projde.** To je ta odpověď, kterou jsem v round 1 neměl a kvůli které
   byl M1. `evidence_profile: standard` žádá „a run directory containing `grader.md`"
   (`tools/intent/realization.py:512`, `GRADER_FILENAME = "grader.md"` na `:43`) a `low`
   běh ten soubor teď vyrábí. R6 je tím pravdivé i o `low`.
2. **Odvození je správné, ne obcházející.** Politiku nikdo neohnul: `git status --porcelain
   doc/intent/_policy.yaml` je prázdný a `evidence_profile: standard` tam stojí dál.
   Opravila se ta strana, která byla vadná — `low` konvence, která gate log schovávala do
   souboru Codera, což R5 zakazuje. Tvrzení `report.md:168-169` potvrzuji.
3. **Scope guard `low` běh zvládá.** `tools/intent/scope.py:17` má
   `PLAN_FILENAMES = ("plan.md", "run.md")`, takže `run.md` je platný plánovací soubor
   a `low` běh projde i touhle branou. Ověřeno spuštěním, ne přečtením.

Kontratest, aby bylo doložené, že to nese opravdu `grader.md` a ne něco jiného: **tentýž**
adresář bez `grader.md` je dál odmítnutý.

```
$ rm doc/runs/<low>/grader.md && python3 tools/intent/cli.py realization claim i0003 …
intent: R3 i0003: evidence doc/runs/… is not a run directory with grader.md
        (evidence_profile: standard)                                        exit=2
```

**Nikde jinde už `low` jako jediný soubor popsaný není.** Prohledal jsem každý výskyt
`run.md` v `rules/`, `skills/`, `README.md`, `VERIFY.md`, `AGENT_MODELS.md`, `commands/`
a `tools/`: `07-run-artifacts.mdc:20-22` (nové znění), `:54` („`plan.md` (or `run.md`)
additionally declares what the run is allowed to touch" — dál pravdivé),
`skills/ice-run/SKILL.md:144` (nový checklist), `scope.py:17` a `main.py:388` (nástroj).
`README.md` o artefaktech `low` nemluví vůbec. Vzorce „a single file", „one file",
„single artifact" nedávají v metodice žádný zásah o `low` (jediné shody jsou o třídách,
uzlech a pravidlech).

## B1 — nová kontrola č. 8 v obou směrech, kontrafakt sestavený

Klon s reálnou historií, aby `git diff` měl proti čemu diffovat.

**Směr A — situace tohoto běhu (nárok se nepředběhl).** Přesně příkazy z kontroly:

```
$ git diff -- doc/intent/_realization.yaml
(prázdný)                                                                   exit=0
$ python3 tools/intent/cli.py realization check
realization layer consistent (2 entry/entries)                              exit=0
```

Kontrola tedy **projde** — a projde i na skutečném pracovním stromu, kde jsem ji spustil
znovu se stejným výsledkem. Žádný nárok přede mě nepředběhl.

**Směr B — kontrafakt, který jsem musel postavit.** Coordinator zapíše nárok citující
tento běh **před** mým verdiktem:

```
$ python3 tools/intent/cli.py realization claim i0003 \
    --evidence doc/runs/20260817-2334-review-craft-and-claim-order-e2 --by Coordinator
i0003 claimed against doc/runs/20260817-2334-review-craft-and-claim-order-e2 — now realized

$ git diff -- doc/intent/_realization.yaml
+  i0003:
+    claim:
+      evidence: doc/runs/20260817-2334-review-craft-and-claim-order-e2
+      by: Coordinator
+      contracts: sha256:a92653e006646cda
+      meaning: sha256:03eddcb5c7864430
```

Kontrola tím **spadne**, a spadne čitelně: jméno běhu je v diffu doslova (jeden výskyt,
změřeno `grep -c`), takže „must add no claim citing this run" se dá rozhodnout očima, bez
dalšího nástroje. To je právě to, co předchozí znění (`realization status --node`) neumělo.

Jedna poznámka k druhé polovině kontroly, ať se o ni nikdo neopírá špatně:
`realization check` zůstane v obou směrech `exit=0` — i s předběhnutým nárokem
(`realization layer consistent (3 entry/entries)`). Rozhodující polovinou je tedy
**`git diff`**; `realization check` hlídá jinou věc (že vrstva je konzistentní a podepsaná
někým jiným než Coderem). Znění kontroly je tak, jak je, správné — obě podmínky spojuje
`;`, ne „nebo" — jen ať nikdo nečte druhou jako zástupnou za první.

## Major

### M3 — dvě věty v B4 se neskládají a tichá varianta zahazuje nejcennější druh nálezu

`skills/ice-review/SKILL.md:46-51`. První věta: „A place where the sentence turns false and
the suite stays green is a **blocker** when the sentence is false **now**." Druhá:
„A gap the diff neither introduced nor asserted away — in the plan, the Definition of Done,
or a realization claim — is a **follow-up**."

Čtené jako sada dvou kritérií zbývá **jeden nezařazený případ**: věta je dnes pravdivá,
ale běh o té dosud nepokryté hranici tvrdí, že je zavřená. Odpověď se dá odvodit jedině
obrácením druhé věty (není-li to follow-up, je to blokátor). Kdo první větu přečte jako
**nutnou** podmínku — a to je přirozené čtení slova „when" — dostane opačný výsledek.

**Proč to není akademické.** Přesně v té škatulce leží osm z devíti blokátorů, které tenhle
repozitář kdy vyrobil. Adversář běhu `20260817-1853` u svého B1 napsal doslova: *„Text `c6`
se měnit nemusí — je pravdivý, jen nedokázaný"*
(`doc/runs/20260817-1853-slice-and-derived-truth-66/review.md:80`) — tedy věta **pravdivá
teď**, blokátor proto, že ji plán tvrdil za prokázanou. Totéž B2 a B3 téhož běhu; u B3 to
autor výslovně opřel o slib plánu (`review.md:124-129`). Při čtení první věty jako nutné
podmínky by se všechny čtyři staly follow-upy a čtyři reálné vady by se odložily.

**Že se to dá přečíst správně, jsem si dokázal na sobě:** M9 v tabulce níž (věta `c12` je
dnes **pravdivá**, protože `claim()` odmítá; nepokryté je jen hlášení v `check()`, a to
běh netvrdil za zavřené) mi podle B4 vyšlo správně jako follow-up. Text tedy funguje —
u čtenáře, který si druhou větu obrátí.

**Návrh, jedna věta místo dvou** (kritérium pozitivní a úplné):

```markdown
3. A place where the sentence turns false and the suite stays green is a **blocker** when
   the sentence is false now, or when this run asserted that place closed — in the plan,
   the Definition of Done, or a realization claim. Otherwise it is a **follow-up**: write
   it so the Human can drop it into a later run; do not block this one for it.
```

**Dispozice:** Major, ne blokátor — text dnes k správnému výsledku dovést umí a `Major
= correct but fragile` je přesně tahle kategorie. Zároveň mi vlastní nové B4 říká
neblokovat běh za mezeru, kterou diff neudělal nepravdivou. Human má dvě čisté možnosti:
vzít tu jednu větu ještě v tomto běhu (je to náhrada řádek za řádek, délka to unese —
`ice-review` má 132 řádků z 500), nebo ji naplánovat jako **FU-A** níž.

## Minor / non-blocking

1. **Spouštěč enumerace nejmenuje kolo, ve kterém jsem.** `skills/ice-review/SKILL.md:68`
   říká „In the verdict you are about to ship — round one or the last permitted round —",
   ale tohle je **round 2**: není to první kolo a není to poslední povolené (to je třetí).
   Nadpis („When the review ends, enumerate") a komentář v šabloně („mandatory when the
   review ends") jsou správné a jednoznačné, takže jsem se řídil jimi a tabulku přiložil.
   Ta vsuvka je ale výčtem dvou kol tam, kde má být podmínka. Návrh: „in the verdict you
   are about to ship, whichever round that is". **Dispozice:** oprava tří slov, nebo FU-A
   společně s M3 — obojí je v témž odstavci.
2. **Kolik vět se má enumerovat, není řečeno.** „Every contract in `slice.md` is a claim
   about the whole codebase" plus „list the complete set of places **the sentence** reaches"
   dohromady nedávají, které věty do tabulky patří. `slice.md` tohoto běhu nese
   **28** kontraktů (`coverage`: `contracts: 28`); enumerace všech by byl audit celého
   `tools/`, ne recenze diffu — a Adversář předchozího běhu to výslovně odmítl jako mimo
   možnosti jednoho běhu (`review.md:915-919`). Enumeroval jsem věty, které diff může
   udělat nepravdivými, plus tu jednu, kterou běh tvrdí za zavřenou. Návrh na jednu
   vsuvku: „the sentences this diff can make false, plus any the run asserts closed".
   **Dispozice:** FU-A.
3. **Checklist `ice-run` přestal odškrtávat `request.md`.**
   `skills/ice-run/SKILL.md:144` dnes: „Run directory with `run.md` and `grader.md` (low),
   or the full separate set (medium/high)". Předtím tam stálo „with `request.md` and
   either …". `request.md` tak zmizel z jediného checklistu, který Coordinator odškrtává;
   přežívá jen v tabulce artefaktů `07-run-artifacts.mdc:26` (medium/high) a jako sekce
   `run.md` na `low`. Informace se neztratila, ale krok 1 skillu píše `request.md` jako
   první soubor běhu a checklist to už nekontroluje. Návrh: „Run directory with
   `request.md`, plus `run.md` and `grader.md` (low) or the full separate set". Nespadá to
   pod žádnou z šesti oprav — je to vedlejší efekt B6. **Dispozice:** FU-A, nebo tři slova
   teď.

## Follow-up — zapsané tak, aby to Human mohl naplánovat bez odvozování

### FU-A — tři formulační opravy v `skills/ice-review/SKILL.md`

Jeden běh, tři náhrady, žádná změna chování nástroje: kritérium blokátor/follow-up jednou
pozitivní větou (M3), spouštěč enumerace bez výčtu kol (Minor 1), rozsah enumerace
(Minor 2). Doslovná znění všech tří jsou výš. Úroveň `medium` (mění se skill pod `i0003`,
délka zůstává hluboko pod limitem, žádný kontrakt se neoslabuje).

### FU-B — druhé odvozovací místo `c12` (přeneseno z round 1, M2)

`tools/intent/realization.py:480` — hlášení `R6 … a claim may not be written by the Coder`
ve funkci `check()`. Mutace `== "coder"` → `== "coderx"` tam nechá sadu zelenou (přeměřeno
i v round 2, viz M9 v tabulce). Je to jediná pojistka proti nároku zapsanému ručně do
`doc/intent/_realization.yaml` mimo CLI. Zadání: jeden test, který napíše `by: Coder` do
vrstvy ručně a čeká nenulový exit z `realization check`. Podle nového B4 je to **správně**
follow-up, ne blokátor: věta `c12` je dnes pravdivá (`claim()` odmítá) a tento diff tu
mezeru ani nezavedl, ani netvrdil za zavřenou. Human ho v round 1 vyňal z rozsahu.

## Where the contract reaches

Povinné podle nové sekce „When the review ends, enumerate". Přeměřeno **znovu** proti
znění po kole 2, ne přepsáno z round 1 — `skills/ice-review/SKILL.md` a
`rules/07-run-artifacts.mdc` mezitím narostly, takže dvě mutace limitů musely dostat jiné
množství řádků. Vše na scratch kopii `/tmp/adv-r2` (celý repozitář včetně `.git`
a `.cursor` symlinků, bajtově shodný s pracovním stromem před první mutací).

| # | Místo, kam věta sahá | Mutace | Sada | Stav |
|---|---|---|---|---|
| 1 | `template_checks.py:73` — `i0002` c2, půlka `alwaysApply` | +40 řádků do `rules/07-ice-workflow.mdc` | `158 lines exceeds the alwaysApply limit of 150`, exit 1 | uzavřeno |
| 2 | `template_checks.py:73` — `i0002` c2, půlka `scoped` | +110 řádků do `rules/07-run-artifacts.mdc` | `251 lines exceeds the scoped limit of 250`, exit 1 | uzavřeno |
| 3 | `template_checks.py:99` — `i0003` c2, limit skillu | +370 řádků do `skills/ice-review/SKILL.md` | `502 lines exceeds the skill limit of 500`, exit 1 | uzavřeno |
| 4 | `template_checks.py:70` — `i0002` c1, deklarace aktivace | vyřadit `description` i `globs` z front matteru `07-run-artifacts.mdc` | `needs a description, globs, or alwaysApply: true`, exit 1 | uzavřeno |
| 5 | `template_checks.py:94` — `i0003` c1, `name` ve SKILL.md | `name:` → `nam3:` v `ice-review` | `front matter is missing 'name'`, exit 1 | uzavřeno |
| 6 | `template_checks.py:128` — `i0001` c1, odkazy | `../../rules/07-realization.mdc` → `-x.mdc` v `ice-review` | `broken link: ../../rules/07-realization-x.mdc`, exit 1 | uzavřeno |
| 7 | `template_checks.py:136` — `i0001` c2, `.cursor` symlinky | odklidit `.cursor/rules` | `expected a symlink so Cursor discovers this directory`, exit 1 | uzavřeno |
| 8 | `realization.py:546` — `i0004` c12, odmítnutí v `claim()` | `== "coder"` → `== "coderx"` | `FAILED (failures=1)`, padá **právě** `test_coder_may_not_claim_its_own_work` | uzavřeno |
| 9 | `realization.py:480` — `i0004` c12, hlášení `R6` v `check()` | `== "coder"` → `== "coderx"` | `Ran 82 tests … OK` | **otevřeno → FU-B** |

Devět míst, osm uzavřených, jedno otevřené a podle nového B4 správně klasifikované jako
follow-up (věta je dnes pravdivá; diff tu mezeru nezavedl ani netvrdil za zavřenou).
Půlky, na kterých se dá uklouznout, jsem mutoval zvlášť — `i0002` c2 obě („always-applied …
a scoped rule"), `i0001` c1 na obou plochách (`rules/*.mdc` i `skills/*/SKILL.md`), `c12`
na obou odvozovacích místech. U mutace 8 jsem ověřil, že nepadá nic jiného, tedy že signál
nic nezakrývá. Tabulka je vůči round 1 nezměněná ve stavech; změnila se jen čísla řádků
v mutacích 2 a 3, protože oba soubory mezitím narostly.

Kontrakty s `enforced_by: review` v enumeraci nejsou, a podle nového B3 tam ani nepatří —
`coverage` hlásí `review exceptions: 0`, takže v tomto stromu dnes žádné nejsou.

## Jak se nový krok 3 chová podruhé, na změněné verzi sebe sama

**B2 se řídit dá a je lepší než předchozí znění.** „Mutate a scratch copy, never the
working tree. Restore the copy after each mutation; when finished, confirm the working tree
was never touched." — ta tři sdělení jdou po sobě a nezaměňují kopii za strom, což byla
vada původní věty. Splnil jsem je doslova: devět mutací, po každé `cp` zpět, po každé
`diff -q` proti pracovnímu stromu, a na konci `git status --porcelain`, který má pořád
právě osm změněných souborů a adresář běhu. Poslední klauzule je navíc **kontrolovatelná
třetí osobou**, což ta původní („revert byte-exact") nebyla.

**B3 kouše správně a nikde jinde.** Věta stojí až za bodem 3, takže neruší mutační
povinnost, jen z ní vyjímá kontrakty, u kterých mutovat není co. V tomto stromu je to
dnes bez efektu (`review exceptions: 0`) — ale právě proto je dobře, že to tam je: kdo
skill vezme do projektu s review-kontrakty, dostal by jinak automatické blokátory.

**B4 a B5 jsem musel použít na sebe a obojí drhne o jedno slovo**, což je M3 a Minor 1 výš.
Poctivě: nebylo to nejednoznačné tak, abych nevěděl, co udělat — nadpis a šablona spor
rozhodly a klasifikaci M9 jsem podle B4 dostal správně. Bylo to nejednoznačné tak, že
Adversář s jiným čtením by odešel s jiným verdiktem, a to je u textu, který má být
pravidlem ukončení, o jedno kolo víc, než je potřeba.

**Co bych na kroku 3 už neměnil.** Trojice „pojmenuj místa → mutuj → klasifikuj" je po
kole 2 vykonatelná od začátku do konce a tabulka opravdu funguje jako pravidlo ukončení:
tenhle verdikt je krátký ne proto, že bych přestal hledat, ale proto, že tabulka řekla,
kde hledání skončilo. Schematické `<file:line>` místo živých jmen je taky správné —
psal jsem tabulku pro `template_checks.py` a `realization.py`, tedy pro místa, která
v příkladu nejsou, a nic mě k nim netlačilo.

## Co jsem sám ověřil (round 2)

| Příkaz | Výstup | Exit |
|---|---|---|
| `python3 tools/intent/cli.py validate` | `5 node(s): 0 error(s), 0 warning(s)` | 0 |
| `python3 tools/intent/cli.py realization check` | `realization layer consistent (2 entry/entries)` | 0 |
| `python3 tools/intent/cli.py coverage` | `contracts: 28`, `machine-enforced: 28 (100%)`, `review exceptions: 0`, `files outside any node: 0` | 0 |
| `python3 tools/intent/cli.py scope --run doc/runs/20260817-2334-review-craft-and-claim-order-e2` | `scope clean (8 declared path(s))` | 0 |
| `python3 -m unittest discover -s tools/intent/tests -t tools` | `Ran 82 tests … OK` | 0 |
| `python3 tools/checks/template_checks.py --root .` | `template contracts satisfied` | 0 |
| `python3 tools/checks/hook_checks.py --root .` | `hook contracts satisfied` | 0 |
| `ruff check tools/` / `ruff format --check tools/` | `All checks passed!` / `19 files already formatted` | 0 |
| `git diff -- doc/intent/_realization.yaml` (kontrola č. 8, směr A) | prázdný | 0 |
| kontrola č. 8, směr B (kontrafakt na klonu) | diff přidá nárok citující tento běh, jméno běhu čitelné | 0 |
| `scope --run <sestavený low běh>` | `scope clean (1 declared path(s))` | 0 |
| `realization claim i0003 --evidence <low běh> --by Coordinator` | `i0003 claimed … — now realized` | 0 |
| tentýž `low` běh bez `grader.md` | `R3 … is not a run directory with grader.md` | 2 |
| `git status --porcelain doc/intent/_policy.yaml` | prázdný — politika nedotčená | 0 |
| `realization claim … --by Coder` (pracovní strom) | `the Coder may not claim its own work; the Coordinator claims once every gate the level requires has passed` | 2 |
| `grep -rn "once every gate the level requires has passed"` (celý repozitář, `--include` masky) | 8 řádků / 7 souborů | 0 |
| `grep -rn "every gate the level requires"` | 8 → variants = 0 | 0 |
| `grep -rn "Grader is green" rules/ skills/ README.md tools/` | prázdný | 1 |
| `grep -rn "green Grader"` | 2 řádky, obě správné (popření + omezení na `low`) | 0 |
| `grep -n "^## Step" skills/ice-review/SKILL.md` | 1, 2, 3, 4, 5 bez duplikátu a bez děr | 0 |
| křížové odkazy na čísla kroků | jediný odkaz na kroky `ice-review` je vnitřní (`:36` → Step 3); `ice-run` `Step 4/8/9` sedí; `VERIFY.md:41` „step 7" dál platí | — |
| `wc -l` osm výstupů | `118 155 141 156 132 108 652 697` | 0 |
| devět mutací (tabulka výš) | osm řeže, jedna zelená (FU-B) | 1 / 0 |

**Délky po kole 2**, přeměřené: `07-run-artifacts.mdc` 139 → **141** (limit 250),
`ice-review/SKILL.md` 126 → **132** (limit 500), ostatních šest bez změny. Tabulka
v `report.md:143-152` s tím sedí na řádek. Nejtěsnější zůstává `07-ice-workflow.mdc`
na 118 ze 150; nesáhl na něj ani jeden ze šesti fixů.

**Rozsah:** `git diff --stat` je pořád právě těch osm souborů z `outputs`, `incidental`
prázdné. Diff neobsahuje `doc/intent/nodes/`, `doc/intent/_policy.yaml`,
`doc/intent/_realization.yaml`, `VERIFY.md`, `AGENT_MODELS.md` ani nic pod `doc/runs/`
mimo adresář tohoto běhu; z `tools/` jen `tools/intent/realization.py`, a v něm jen ty tři
řádky uvnitř `raise TreeError(...)`. Předchozí běh
(`20260817-1853-slice-and-derived-truth-66/grader-evidence.md`) zůstal nedotčený. Sám jsem
nezměnil nic než tento `review.md`; obě scratch kopie (`/tmp/adv-r2`, `/tmp/adv-r2-clean`)
jsou smazané.

## Co tento diff mění a co nemění na chování metodiky

Mění tři věci, a všechny tři jsou strojově ověřitelné, ne otázka dobré vůle: nárok na
realizaci se zapisuje po branách, které si úroveň žádá — tedy nad `low` až po verdiktu
recenze — a to je vyslovené jednou a touž větou na osmi místech v sedmi souborech, včetně
runtime hlášení nástroje, takže se ta místa nemohou rozejít bez toho, aby to `grep` chytil;
`grader.md` má jediného autora, Coordinatora, a `low` běh proto vyrábí dva soubory místo
jednoho, čímž se `low` nárok stává splnitelným proti `evidence_profile: standard` — dokázáno
sestaveným během, ne úvahou; a Adversář má napsanou techniku, kterou dosud dostával
v promptu, plus enumerační tabulku, která recenzi ukončuje, a kontrolu č. 8, která
předběhnutý nárok opravdu odhalí — ověřeno v obou směrech. **Nemění** nic v chování
nástroje: `tools/` se pohnul o tři řádky textu jedné výjimky, sada je dál `Ran 82 tests …
OK` a `_policy.yaml` je nedotčený, takže co bylo mechanicky vynutitelné před během, je
vynutitelné po něm, a nic nového vynutitelné nezačalo být. Nemění to, co značka `realized`
znamená: pořád je to záznam tvrzení proti otisku textu, ne důkaz, že vynucovač svou větu
prokazuje — jen se to tvrzení teď zapisuje v okamžiku, kdy už ho někdo zkusil vyvrátit.
A nezavírá to `c12` na jeho druhém odvozovacím místě (FU-B) ani nedodává recenzi rozsahové
pravidlo pro to, kolik vět enumerovat (FU-A); obojí je zapsané tak, aby to šlo naplánovat
bez odvozování znovu.

# Round 3 (poslední povolený)

## Verdikt

**APPROVE**

Všechny čtyři opravy jsou v pracovním stromu. **M1 je bajt za bajt** ta věta, kterou jsem
v round 2 navrhl — ověřeno strojově, ne očima: vytáhl jsem svůj vlastní návrh z bloku
v tomto `review.md` a hledal jsem ho jako podřetězec v `skills/ice-review/SKILL.md`.
Nic, co jsem už ověřil, se nepohnulo; šest netknutých souborů má bajtově tentýž diff jako
v kole 2. Devět míst z enumerační tabulky jsem přeměřil proti finálnímu textu: osm řeže,
jedno zůstává zelené a je to zapsaný follow-up FU-B.

Rozhodující test, který jsem v prvních dvou kolech neudělal a bez kterého se FU-B zařadit
nedá, jsem doplnil až tady — viz „Je věta `c12` nepravdivá **teď**?" níž. Vyšel ve prospěch
follow-upu, a to na základě měření, ne argumentu.

## Blokátory

Žádné.

## Ověření čtyř oprav

| # | Oprava | Jak jsem to měřil (ne přečetl) | Výsledek |
|---|---|---|---|
| M1 | kritérium blokátor / follow-up | Python: extrahoval jsem svůj návrh z fenced bloku v `review.md` (round 2, sekce M1) a testoval `proposal in SKILL.md` | `True` — **bajt za bajt**, včetně em-dash a odsazení pokračovacích řádků |
| M2/M3 | spouštěč a rozsah enumerace | `sed -n '66,72p' skills/ice-review/SKILL.md` | `### When the review ends, enumerate` + „In the verdict you are about to ship, whichever round that is, list the complete set of places reached by the sentences this diff can make false, plus any the run asserts closed" |
| M4 | checklist `ice-run` | `grep -n "Run directory with" skills/ice-run/SKILL.md` | `:144` — „Run directory with `request.md`, plus `run.md` and `grader.md` (low) or the full separate set" |

M2/M3 je jedna náhrada, která uzavírá obě moje výtky naráz: „whichever round that is"
odstraňuje mezeru kol 2 a n−1 a „the sentences this diff can make false, plus any the run
asserts closed" dodává rozsah, který v round 2 chyběl. Nezávislý test toho rozsahu je
v sekci „Kam sahá kontrakt": aplikoval jsem ho od nuly a vyšla mi **táž devítka míst**,
kterou jsem v kole 2 sestavil bez pravidla. Pravidlo tedy neškrtá nic, co jsem považoval
za nutné, ani nepřidává řádky, které bych neuměl obhájit.

## Nic jiného se nepohnulo — měřeno

| Invariant | Měření | Round 2 | Round 3 |
|---|---|---|---|
| rozsah diffu | `git diff --stat` | 8 souborů | **8 souborů**, `114+/36−` |
| šest netknutých souborů | `git diff --stat -- README.md rules/ skills/ice-implement tools/` | `10 2 11 18 9 3` | **`10 2 11 18 9 3`** — bajtově tytéž hunky |
| kanonická věta | `grep -rn` napříč `*.md *.mdc *.py *.yaml *.json` mimo `doc/runs/`, `doc/new_ideas/` | 8 v 7 souborech | **8 v 7 souborech** (`ice-implement:98`, `ice-run:116,148`, `README:257`, `realization.py:549`, `07-run-artifacts:89`, `07-ice-workflow:45`, `07-realization:80`) |
| žádná varianta věty | `grep -rn "every gate the level requires"` | 8 | **8** — tedy nula parafrází |
| „zelený Grader stačí" | `grep -rn "Grader is green"` / `"green Grader"` | 0 / 2 legitimní | **0 / 2** (`07-run-artifacts:86` popírá, `ice-run:116` je `low` větev kanonické věty) |
| přečíslování | `grep -n "^## Step" skills/ice-review/SKILL.md` | 1–5 | **1–5** bez děr a duplikátů; jediný odkaz na číslo je vnitřní `:36` → Step 3 a míří správně |
| křížové odkazy jinde | `grep -rniE "step[ -]?[0-9]"` nad `rules/ skills/ README.md VERIFY.md AGENT_MODELS.md` | 6 zásahů, všechny na `ice-run` / `VERIFY.md` | **6 zásahů**, tytéž; žádný nemíří na krok `ice-review` |
| `TreeError` | runtime, ne zdroj: `claim … --by Coder` | jedna mezera na hranici segmentů | **`the Coder may not claim its own work; the Coordinator claims once every gate the level requires has passed`**, exit **2** |
| sada | `python3 -m unittest discover -s tools/intent/tests -t tools` | `Ran 82 tests … OK` | **`Ran 82 tests … OK`** |
| délky | `wc -l` osmi výstupů | `118 155 141 156 132 108 652 697` | **`118 155 141 156 133 108 652 697`** |
| `low` jako jediný soubor | `grep -rn "run\.md"` nad `rules/ skills/ README.md VERIFY.md tools/` | nikde | **nikde**; `07-run-artifacts:20-22` má „**and** a separate `grader.md`" |
| brány | osm příkazů `VERIFY.md` | zelené | **zelené**, exit 0 (validate, realization check, coverage 28/28, scope, unittest, template_checks, hook_checks, ruff) |

Jediný pohyb v číslech je `skills/ice-review/SKILL.md` **132 → 133** řádků; M1 je o řádek
delší než text, který nahradila, M2/M3 a M4 jsou náhrady řádek za řádek. Limit je 500,
takže od stropu je to 367 řádků daleko. Nejtěsnější soubor v repozitáři zůstává
`rules/07-ice-workflow.mdc` na 118 ze 150 a žádná ze čtyř oprav na něj nesáhla.

## Je věta `c12` nepravdivá **teď**? — test, který zařazuje FU-B

M1 mě nutí odpovědět na otázku „je ta věta nepravdivá teď", a krok 2 pro ni důkaz nevyrábí
(mutace ukazuje, co by bylo, ne co je). Musel jsem tedy `c12` zkusit vyvrátit
v nezmutovaném kódu, oběma cestami, jimiž nárok do vrstvy vstupuje:

| Cesta zápisu nároku | Příkaz | Výsledek |
|---|---|---|
| přes CLI | `realization claim i0003 --evidence <run> --by Coder` | odmítnuto, exit **2**, hlášení s kanonickou větou |
| ručně do YAML, CLI obejito | `i0002.claim.by: Coordinator` → `Coder`, pak `realization check` | `ERROR R6 i0002: a claim may not be written by the Coder`, exit **1** |

`validate` na ruční zápis reaguje exit 0 — to je v pořádku, `R6` patří do `realization
check`, ne do validátoru, a `VERIFY.md` obojí volá.

Věta `c12` je tedy **dnes pravdivá v obou směrech**. Mezera je čistě testovací: druhé
odvozovací místo (`realization.py:480`, `check()`) není pokryté sadou, takže tam mutace
`== "coder"` → `== "coderx"` nechá `Ran 82 tests … OK`. Podle M1 v jeho finálním znění:
věta není nepravdivá teď **a** tento běh to místo za zavřené netvrdil — plán a Definition
of Done mluví o mutaci v `claim()` a Critic to místo explicitně vyloučil, nárok na
realizaci tento běh nezapsal a stávající nárok na `i0004` cituje běh předchozí. Tedy
**follow-up**, ne blokátor. Říkám to výslovně, jak Human žádal: **FU-B blokátor není**,
i po tomto testu.

## Kam sahá kontrakt   <!-- mandatory when the review ends -->

Rozsah podle M2/M3, odvozený od nuly: *věty, které tento diff může udělat nepravdivými* =
kontrakty uzlů, do jejichž `code_paths` diff sahá (`rules/` → `i0002`, `skills/` →
`i0003`, `README.md` a linky → `i0001`, `tools/intent/realization.py` → `i0004`); u `i0004`
je to jen `c12`, protože změna je třířádková náhrada textu jedné výjimky a žádnou jinou
větu uzlu se dotknout nemůže. *Plus věty, které běh tvrdí za zavřené* = `c12`, kterou
Definition of Done bod 8 (mutace 3) a bod 12 prohlašují za dál vynucenou. Součet: sedm
šablonových míst + dvě odvozovací místa `c12` = devět. Všechny mutace na čerstvé scratch
kopii, po každé obnova, na konci `git status --porcelain` beze změny.

| # | Místo, kam věta sahá | Mutace | Sada | Stav |
|---|---|---|---|---|
| 1 | `rules/07-ice-workflow.mdc` — `i0002` c2, větev `alwaysApply` (limit 150) | +40 řádků → 158 | `ERROR … exceeds the alwaysApply limit of 150`, exit 1 | zavřeno |
| 2 | `rules/07-run-artifacts.mdc` — `i0002` c2, větev `globs` (limit 250) | +110 řádků → 251 | `ERROR … exceeds the scoped limit of 250`, exit 1 | zavřeno |
| 3 | `skills/ice-review/SKILL.md` — `i0003` c2 (limit 500) | +370 řádků → 503 | `ERROR … exceeds the skill limit of 500`, exit 1 | zavřeno |
| 4 | `rules/07-ice-workflow.mdc` — `i0002` c1, aktivace v front matter | `alwaysApply:` → `xalwaysApply:` | `ERROR … needs a description, globs, or alwaysApply: true`, exit 1 | zavřeno |
| 5 | `skills/ice-review/SKILL.md` — `i0003` c1, `name` ve front matter | `name:` → `nam3:` | `ERROR … front matter is missing 'name'`, exit 1 | zavřeno |
| 6 | `skills/ice-run/SKILL.md` — `i0001` c1, integrita odkazů | `07-realization.mdc` → `07-realization-x.mdc` | `ERROR … broken link`, exit 1 | zavřeno |
| 7 | `.cursor/skills` — `i0001` c2, symlinky pro Cursor | symlink odstraněn | `ERROR … expected a symlink`, exit 1 | zavřeno |
| 8 | `tools/intent/realization.py:547` — `i0004` c12, odmítnutí v `claim()` | `== "coder"` → `== "coderx"` | `FAIL: test_coder_may_not_claim_its_own_work`, `FAILED (failures=1)` — a nic jiného | zavřeno |
| 9 | `tools/intent/realization.py:480` — `i0004` c12, hlášení `R6` v `check()` | `== "coder"` → `== "coderx"` | `Ran 82 tests … OK` | **otevřeno → FU-B** |

Tabulka je pravidlo zastavení: řádky 1–8 jsou zavřené a nikdo je nesmí znovu otevřít,
řádek 9 je celý zbytek požadavku a je zapsaný jako follow-up.

## Major

Žádný.

## Minor / non-blocking

**Mi-1 — M1 zavádí predikát, pro který krok 3 nevyrábí důkaz.** Bod 3 se ptá, zda je věta
„false now"; body 1 a 2 učí jen mutovat, a mutace o nezmutovaném stavu nevypovídá.
U testovaných směrů to zakryje Grader, u netestovaného (řádek 9) ne — a právě tam na
odpovědi visí zařazení do hromádky. Musel jsem si test vymyslet sám (tabulka „Je věta
`c12` nepravdivá teď?"). Chybí jedna větička, například na konec bodu 1: *„Before mutating,
confirm the sentence holds in that place as the code stands — by observation, not by the
suite."* **Dispozice:** FU-C. Nezdržuje: kdo bod 3 čte pozorně, ten si test odvodí, jen ho
musí odvodit.

**Mi-2 — M4 obnovil spolu s formulací i dřívější nejednoznačnost o `request.md` na `low`.**
Checklist teď žádá `request.md` *plus* `run.md` a `grader.md`, zatímco
`rules/07-run-artifacts.mdc:20` dává `low` běhu `run.md` **se sekcí** `request` a soubor
`request.md` uvádí až v tabulce pro `medium` a `high`. Ověřil jsem, že to není vada tohoto
běhu: `git show HEAD:skills/ice-run/SKILL.md` má „Run directory with `request.md` and
either `run.md` (low) or the full set" a `git show HEAD:rules/07-run-artifacts.mdc` má
„a single `run.md` with sections: request, …" — táž nejednoznačnost, slovo za slovem, už
před během. Přiznávám ji jako svou: tu formulaci jsem v round 2 navrhl obnovit a nevšiml
jsem si, že s ní přijde i tohle. **Dispozice:** FU-D.

## Dispozice všeho, co zůstává otevřené

| Id | Co | Hromádka | Proč tam |
|---|---|---|---|
| **FU-B** | `c12` není vynucená testem na druhém odvozovacím místě (`realization.py:480`) | **follow-up** | věta je dnes pravdivá v obou směrech (změřeno, exit 2 a exit 1), diff tu mezeru nezavedl a běh ji za zavřenou netvrdil |
| **FU-C** | krok 3 v `ice-review` nemá krok pro zjištění „false now" | **follow-up** | vada čitelnosti návodu, ne nevynucený kontrakt; jedna věta ji zavírá |
| **FU-D** | `request.md` na `low`: soubor, nebo sekce v `run.md`? | **follow-up** | nejednoznačnost existovala před během slovo za slovem; tento diff ji nezhoršil |

Blokátory: **žádné**. Nic z výše uvedeného neeskaluje.

### FU-B — druhé odvozovací místo `c12` (přeneseno z round 1, M2)

`tools/intent/realization.py:480` hlásí `R6` pro nárok podepsaný Coderem, který se do
vrstvy dostal ručně. Mutace `== "coder"` → `== "coderx"` na tom řádku nechá sadu zelenou.
Hotové zadání: jeden test v `tools/intent/tests/test_realization.py`, který zapíše
`by: Coder` přímo do `_realization.yaml`, zavolá `realization check` a čeká nenulový exit
a `R6` ve výstupu. Reprodukce vady je v tabulce výš, řádek 9; ověřená podoba správného
chování je v tabulce „Je věta `c12` nepravdivá teď?", druhý řádek. Uzel `i0004`,
komplexita `low`.

### FU-C — doplnit do kroku 3 zjištění stavu „teď"

Do `skills/ice-review/SKILL.md`, na konec bodu 1 kroku 3, přidat: *„Before mutating,
confirm the sentence holds in that place as the code stands — by observation, not by the
suite."* Uzel `i0003`, komplexita `low`, 133 ze 500 řádků, místo je.

### FU-D — srovnat `request.md` na úrovni `low`

Rozhodnout jednu z dvou možností a napsat ji na obou místech: buď `low` běh vyrábí
`request.md` jako soubor (pak `rules/07-run-artifacts.mdc:20` vypustí `request` ze seznamu
sekcí `run.md`), nebo `request` zůstává sekcí (pak checklist v `skills/ice-run/SKILL.md:144`
řekne „`request.md`, or its section in `run.md` at `low`"). Uzly `i0002` a `i0003`,
komplexita `low`. Věcné rozhodnutí patří Humanovi, protože jde o to, co je artefakt.

## Jak se mi řídilo podle vlastního finálního textu

Poctivě: **lépe než v obou předchozích kolech, a jedna škvíra zůstala.**

M1 dal poprvé jednoznačnou odpověď, aniž bych musel vymýšlet tie-break. V round 2 jsem
si u řádku 9 musel druhou větu logicky obracet; teď má rozhodnutí dvě podmínky spojené
„nebo" a explicitní `Otherwise`, takže každé místo padne do právě jedné hromádky. Cena je
ta v Mi-1: predikát „false now" je správný, ale text neříká, čím se zjišťuje, a u jediného
místa, kde na tom záleželo, jsem měření musel doplnit sám.

M2/M3 funguje a je to na tomto dokumentu vidět. Rozsah jsem odvodil od nuly z formulace
a vyšla mi táž devítka jako v kole 2, kdy jsem ji sestavoval podle citu — což je nejlepší
zpráva o kalibraci, jakou jsem schopen dodat. „plus any the run asserts closed" udělalo
kus práce: bez té půlky věty by řádek 9 do tabulky nepatřil (diff `check()` nemění), a
právě on je celý zbytek požadavku. Slovo „complete" mě nutí tvrdit úplnost výčtu; opírám
ji o `intent owner` nad každou změněnou cestou plus o to, že do `realization.py` jde
třířádková náhrada textu jedné výjimky. Kdyby diff sahal do stovky souborů, „complete"
by bylo drahé — na velikost běhů, které tahle metodika popisuje, je to únosné.

M4 je věcně správný a přinesl Mi-2, který jsem si přivodil sám.

## Co jsem ověřil sám (round 3)

| Příkaz / měření | Výsledek | Exit |
|---|---|---|
| `python3 tools/intent/cli.py validate` | `5 node(s): 0 error(s), 0 warning(s)` | 0 |
| `python3 tools/intent/cli.py realization check` | `realization layer consistent (2 entry/entries)` | 0 |
| `python3 tools/intent/cli.py coverage` | 28 kontraktů, 28 strojově (100 %), 0 review výjimek, 0 souborů mimo uzel | 0 |
| `python3 tools/intent/cli.py scope --run doc/runs/20260817-2334-…-e2` | `scope clean (8 declared path(s))` | 0 |
| `python3 -m unittest discover -s tools/intent/tests -t tools` | `Ran 82 tests in 0.348s … OK` | 0 |
| `python3 tools/checks/template_checks.py --root .` | `template contracts satisfied` | 0 |
| `python3 tools/checks/hook_checks.py --root .` | `hook contracts satisfied` | 0 |
| `ruff check tools/` / `ruff format --check tools/` | `All checks passed!` / `19 files already formatted` | 0 / 0 |
| M1 bajtová identita se svým návrhem | `proposal in SKILL.md` → `True` | — |
| kontrola č. 8 na tomto běhu | `git diff -- doc/intent/_realization.yaml` prázdný; `realization check` konzistentní | 0 / 0 |
| devět mutací (tabulka „Kam sahá kontrakt") | osm řeže, jedna zelená (FU-B) | 1× `FAILED (failures=1)`, 1× `OK` |
| `claim … --by Coder` (CLI) | hlášení s kanonickou větou, jedna mezera na hranici segmentů | 2 |
| ruční `by: Coder` v YAML + `realization check` | `ERROR R6 i0002` | 1 |
| `git status --porcelain` po všech mutacích | osm `M` + neverzovaný adresář běhu, nic víc | — |

Scratch kopie `/tmp/adv-r3` a všechny záložní soubory `/tmp/s1`–`/tmp/s10` jsou smazané.
Pracovní strom jsem nezměnil jinde než v tomto `review.md`.

## Pro Humana — co metodika po tomto běhu garantuje a co ne

**Garantuje nově tři věci.** Nárok na realizaci se nezapisuje dřív, než proběhly brány,
které si daná úroveň žádá — nad `low` tedy až po verdiktu recenze — a je to řečeno jednou
a touž větou na osmi místech v sedmi souborech včetně runtime hlášení nástroje, takže
`grep` odhalí, kdyby se ta místa rozešla; recenze má kontrolu, která předběhnutý nárok
skutečně najde (ověřeno v obou směrech na sestaveném protipříkladu, ne úvahou); a `grader.md`
má jediného autora, Coordinatora, takže `low` běh vyrábí dva soubory a `low` nárok je proti
`evidence_profile: standard` splnitelný — dokázáno sestaveným `low` během v kole 2. K tomu
má Adversář poprvé napsanou techniku, kterou dosud dostával v promptu: falzifikovat věty
mutací, a recenzi ukončit tabulkou míst, kam kontrakt sahá.

**Negarantuje to, co si čtenář snadno domyslí: že `realized` znamená „dokázáno".** Značka
je pořád záznam tvrzení proti otisku textu uzlu; tento běh změnil jen okamžik, kdy se
tvrzení zapisuje — po tom, co se ho někdo pokusil vyvrátit —, ne jeho povahu. `coverage`
říká 28 z 28 kontraktů strojově vynucených, a to znamená „každý kontrakt má vynucovač",
ne „každý vynucovač pokrývá každé místo, o kterém jeho věta mluví"; přesně tenhle rozdíl
je FU-B, kde `c12` je dnes pravdivá v obou směrech, ale test hlídá jen jeden z nich.
Nezměnilo se ani chování nástroje: `tools/` se pohnul o tři řádky uvnitř jedné výjimky,
sada je dál `Ran 82 tests … OK`, `_policy.yaml` je nedotčený. Co bylo mechanicky
vynutitelné ráno, je vynutitelné i teď, a nic nového vynutitelné začít nemohlo — nové
záruky drží texty a jejich `grep`ovatelná shoda, a ty texty vynucuje čtení, ne CI.
Zbytek je zapsaný ve třech follow-upech tak, aby se dal naplánovat bez odvozování znovu.
