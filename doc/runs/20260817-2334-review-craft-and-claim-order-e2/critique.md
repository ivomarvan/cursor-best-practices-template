---
run_id: 20260817-2334-review-craft-and-claim-order-e2
intent_ids: ["i0002", "i0003"]
role: Critic
model: cursor-grok-4.5-high
complexity: high
status: done
---

# Kritika plánu — R5, R6, R7

## Verdikt

**REVISE**

Plán správně rozšiřuje R6 za neúplný výčet z `request.md`, R5 umisťuje zákaz tam, kde
Coder čte, R7 dává doslovně sledovatelný postup (pojmenuj místa → mutuj → enumerace), a
všechna `old_string`, která jsem na kopii ověřil, jsou v cíli právě jednou. Limity z
`template_checks.py` (`ALWAYS_APPLY_LIMIT=150`, `SCOPED_RULE_LIMIT=250`, `SKILL_LIMIT=500`)
po suchém průchodu drží; aritmetika tabulky sedí až na `skills/ice-run/SKILL.md` (155
řádků místo 154 — pod limitem, řídí se limitem). Po úpravách ale metodika **vnitřně
protiřečí** u `low` běhů: tři místa vyžadují verdikt recenze absolutně, zatímco R6-g a
tělo kroku 9 výjimku správně mají a tabulka Gates v `07-ice-workflow.mdc` říká Adversary
= no.

## Blokátory

1. **`rules/07-ice-workflow.mdc` (R6-h, řádek 45)** — po náhradě smí Coordinator nárokovat
   jen „after a green Grader **and** a review verdict“, ale v témže souboru Gates (`low` /
   Adversary = no) a R6-g v `07-run-artifacts.mdc` dovolují nárok po samotných branách.
   Always-applied pravidlo by učilo nepravdu o většině jednoduchých běhů.

2. **`rules/07-realization.mdc` tabulka „Who may write what“ (R6-d) a `README.md:257`
   (R6-l)** — totéž absolutní „review verdict is in“ bez výjimky pro úroveň bez recenze;
   čtenář jediného z těchto souborů si odnese jiné pořadí než ze skillu krok 9 / R6-g.

3. **`skills/ice-run/SKILL.md` krok 7 (R6-a)** — věta „that judgement arrives in Step 8“
   je absolutní; u `low` krok 8 Adversáře nespouští, takže zákaz nároku v kroku 7 sice
   platí, ale zdůvodnění učí, že verdikt vždy přijde z kroku 8.

4. **`skills/ice-review/SKILL.md` R7-a, příkladová tabulka** — řádky `slicing.py:69` a
   `incoming` / `talks_to` jsou živá místa **tohoto** stromu z běhu `20260817-1853`, ne
   schematické placeholdery; Adversář je může číst jako povinný checklist místo tvaru
   tabulky. Postup 1–3 je jinak dostatečně doslovný.

## Co není blokátor (ale patří do zprávy)

- **Osmé místo se starým pořadím:** `tools/intent/realization.py:548` — chybová hláška
  „the Coordinator claims after the Grader“. Plán ho nepočítal; `tools/` je mimo rozsah
  tohoto běhu → **eskalace na Humana**, ne požadavek na přepracování plánu směrem k
  produkčnímu kódu. Až se text opraví, stačí upravit řetězec (test na něj nekotví).
- **`grader-evidence.md`:** konvence `coder-evidence.md` + „never named `grader*`“ jméno
  z minulého běhu fakticky vyřazuje; výslovné „retire“ není nutné.
- **`unclaim`:** Human zamítl; plán ho jen popírá — v pořádku.
- **DoD grep (položka 9):** po opravě B1–B2 bude potřeba predikát sladit s novou
  formulací výjimky pro `low`; to je důsledek revize, ne samostatný nález.

## R5, limity, konzistence README (krátce)

- R5-a/b/c/d sahají na Coder skill i `07-run-artifacts.mdc`; opravují i past „failing-test
  evidence → `grader.md`“. V pořádku.
- README: první diagram (R6-k) se srovná s druhým (V2, už správné pořadí); tabulka s B2
  musí dostat tutéž výjimku jako R6-g, jinak README znovu protiřečí skillu.
- R7 přečíslování 3→4→5, kontrola č. 4 → Step 3, šablona `review.md` a „Do not“ — po
  suchém průchodu konzistentní; mění chování, ne jen tón.

## Co si nejméně jistý

Zda stačí u B1–B2 jedna společná formulace ve stylu R6-g / kroku 9 („review, where the
level requires one“), nebo jestli always-applied řádek musí zůstat kratší a výjimku nést
jen scoped pravidlo + skill — to je volba Plannerova, ne Criticova.

---

# Round 2

## Verdikt

**REVISE**

B1–B3 a B4 z kola 1 jsou uzavřené. Kanonická věta je u `low` pravdivá (pojmenuje
požadavek, ne konkrétní bránu); always-applied řádek smí zůstat terse — rozhodnutí
Plannera přijímám. Osmé místo je v rozsahu správně; test na text hlášení nekotví;
mutace `coder` → `coderx` je skutečný důkaz `c12`. Pátrání po devátém místě v platné
metodice obstojí. Zůstávají dva nové blokátory z vlastních tvrzení revize 2.

## Blokátory kola 1 — stav

| # | Stav | Proč |
|---|---|---|
| B1 | uzavřen | R6-h nese kanonickou větu; Gates o 40 řádků níž ji definují |
| B2 | uzavřen | R6-d / R6-l mají tutéž větu + dovětek pro `low` |
| B3 | uzavřen | R6-a rozlišuje `medium`/`high` vs `low`; „judgement arrives in Step 8“ pryč |
| B4 | uzavřen | schematická tabulka s `<file:line>`, tři řádky, bez `slicing.py` / `talks_to` |

## Always-applied řádek — rozhodnutí Plannera

**Přijímám.** Kanonická věta není nepravdivá o `low`; výčet úrovní by v always-applied
souboru duplikoval tabulku Gates a vytvořil druhé místo k driftu. To je přesně vada,
kterou tento běh zavírá. Scoped místa a skill nesou dovětek; to stačí.

## Blokátory kola 2

1. **`tools/intent/realization.py` (R6-m) vs tvrzení o bajtové shodě** — plán (ř. 85–87,
   251–253) slibuje kanonickou větu *„once every gate the level requires has passed“*
   znak za znak ve všech osmi místech. R6-m místo toho píše *„when the run closes, after
   every gate the level requires“* (bez `once` / `has passed`). Po suchém průchodu:
   přesná kanonická věta je **sedmkrát** (ice-workflow, realization, run-artifacts,
   ice-run ×2, ice-implement, README), v `realization.py` **nula**. DoD položka 9 s
   podřetězcem `every gate the level requires` to zamaskuje. Exact phrasing se pod
   `line-length = 100` vejde (segment 82 znaků).

2. **Definition of Done, položka 8** — stále říká „dvě mutace“, zatímco Error case a
   položka 12 vyžadují **tři** (včetně mutace `c12` na `realization.py`). Coder, který
   odškrtává DoD doslova, osmý důkaz přeskočí.

## Osmé místo — ověřeno

- `test_coder_may_not_claim_its_own_work` (`test_realization.py:106-113`) používá
  `assertRaises(TreeError)`, ne `assertRaisesRegex`; v `tools/intent/tests/` žádný
  `assertRaisesRegex` a žádná aserce na text „claims after the Grader“.
- Segmenty R6-m: 52 a 93 znaků (pod 100); `ruff.toml` má `line-length = 100`.
- Mutace `== "coder"` → `== "coderx"` mění chování, ne jen text; padá právě jmenovaný
  test — platný důkaz, že `c12` na formulaci nezávisí.

## Deváté místo — audit pátrání

Plánova tabulka je kontrolovatelná. Jedna plocha v ní **chybí**: kořenový
`AGENT_MODELS.explanation.md` (uveden je jen `AGENT_MODELS.md`); stejně tak
`commands/` (existuje `push.md`). Prohledal jsem obě — **žádná** věta o pořadí nároku.
Závěr „devátý výskyt v platné metodice není“ tím drží; díra je v úplnosti seznamu
„kde jsem hledal“, ne v závěru.

## Limity — měření dnes + suchý průchod revize 2

| Soubor | Dnes (měřeno) | Po revizi 2 (suchý průchod) | Limit | Plán „po běhu“ |
|---|---|---|---|---|
| `07-ice-workflow.mdc` | 118 | 118 | 150 | 118 |
| `07-realization.mdc` | 148 | 155 | 250 | 155 |
| `07-run-artifacts.mdc` | 135 | 139 | 250 | 139 |
| `ice-run/SKILL.md` | 142 | **157** | 500 | 156 |
| `ice-review/SKILL.md` | 90 | 126 | 500 | 126 |
| `ice-implement/SKILL.md` | 101 | 108 | 500 | 108 |
| `README.md` | 652 | 652 | — | 652 |
| `realization.py` | 696 | 697 | — | 698 |

Aritmetika je věrohodná; `ice-run` o 1 a `realization.py` o 1 proti tabulce — pod limity,
řídí se limitem a položkou DoD 7. Všechna vzorkovaná `old_string` z revize 2 (včetně
osmi kanonických míst a R6-m) jsou v cíli právě jednou.

## Co není blokátor

- `grader-evidence.md` nechat — souhlas; audit se nepřepisuje.
- `unclaim` — mimo rozsah.
- Dovětek „at `low` the Grader“ jako synekdocha za balík bran — stejný idiom jako dřív;
  R6-g říká přesněji „the gates themselves“.

---

# Round 3 (poslední)

## Verdikt

**ACCEPT**

Tři opravy z revize 3 drží. Plán jinak oproti tomu, co kolo 2 přijalo u B1–B4 a u
always-applied řádku, neposunul. Žádný blokátor; run může jít Coderovi. Níže jen poznámky
pro implementaci a jedna věta pro Adversáře.

## Blokátory kola 2 — stav

| # | Stav | Proč |
|---|---|---|
| B1 (R6-m drift) | uzavřen | R6-m nese `once every gate the level requires has passed` znak za znak; segmenty `"…work; "` + `"the Coordinator claims once…"` se spojí se správnou mezerou po středníku; řádky 52 a 82 znaků (jednořádková varianta 120 > 100) |
| B2 (DoD 8) | uzavřen | položka 8 jmenuje tři mutace: limit řádků, rozbitý odkaz, `coder`→`coderx` |

## Ověření DoD 9 (checksum)

Po suchém průchodu osmi míst: **full = 8**, **sub = 8**, **variants = 0**. Sedm souborů,
`ice-run` dvakrát. Kontroly driftu:

| Zásah | full | sub | variants | Chytí DoD 9? |
|---|---|---|---|---|
| varianta místo jednoho místa | 7 | 8 | 1 | ano (full≠8 i variants≠0) |
| smazání jednoho výskytu | 7 | 7 | 0 | ano (full≠8) |
| devátý výskyt | 9 | ≥9 | — | ano (full≠8) |

## Mutace `c12`

Na kopii s R6-m textem: `by.strip().lower() == "coder"` → `== "coderx"` **uvnitř
`def claim`** → `Ran 82`, `FAILED (failures=1)`, padá **právě**
`test_coder_may_not_claim_its_own_work`. Stejná záměna na druhém výskytu
(`claim.by.strip().lower() == "coder"` u R6 check, ~ř. 480) → celá sada **OK** — mutace
na špatném místě tedy důkaz nepředá.

## Jinak beze změny

R5, R6-a–l, R7, always-applied terse, rozhodnutí o `grader-evidence.md` a zamítnutí
`unclaim` — oproti přijatému stavu kola 2 beze změny. Do tabulky pátrání přibyly
`commands/` a `AGENT_MODELS.explanation.md` (oba čisté); to doplňuje díru z kola 2, nic
nemění.

## Poznámky pro Codera (ne blokátory)

1. Mutace 3: měň **jen** podmínku v `claim()` (dnes ~ř. 546), ne výskyt u
   `claim.by` v R6 check (~ř. 480). `replace_all` nebo první hit by buď rozbily víc, nebo
   nechaly `c12` zelené.
2. Tabulka délek stále říká `realization.py` 697→698; na disku je dnes **696** řádků.
   Po R6-m očekávej **697**. Řiď se `wc -l` a limitem, ne tabulkou (DoD 7).
3. Po všech náhradách hned spusť oba grepy z DoD 9 — full i sub musí být 8 a shodné,
   dřív než se píše `report.md`.

## Pro Adversáře po implementaci

Ověř mutací (ne čtením), že kanonická věta je v `realization.py` opravdu runtime text
`TreeError` po spojení segmentů — a že v `tools/intent/realization.py` nezůstala žádná
druhá věta o pořadí nároku mimo tu jednu.
