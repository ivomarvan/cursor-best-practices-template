---
run_id: 20260817-1743-methodology-debt-ea
intent_ids: ["i0002"]
role: Critic
model: cursor-grok-4.5-high
complexity: high
status: done
---

# Kritika plánu

## Verdikt
ACCEPT

Codera **neblokuje**. Oba blokery z kola 1 jsou v revidovaném plánu uzavřené; R1/R3
drží rozpočet; R4 po šesti buňkách nerozbíjí tvrdá omezení v žádném pásmu.

---

## Kolo 2

### Verdikt kola 2
ACCEPT

### R4 — šest buněk, omezení, DoD

Simulace po substituci:

| Band | Planner | Critic | ≠? | Coder | Adversary | ≠? |
|------|---------|--------|----|-------|-----------|-----|
| `low` | `cursor-grok-4.6-medium` | `claude-sonnet-5-thinking-high` | ano | `composer-2.5` | `claude-sonnet-5-thinking-high` | ano |
| `medium` | `cursor-grok-4.6-medium` | `claude-sonnet-5-thinking-high` | ano | `cursor-grok-4.6-medium` | `claude-sonnet-5-thinking-high` | ano |
| `high` | `claude-opus-5-thinking-high` | `cursor-grok-4.5-high` | ano | `cursor-grok-4.5-high` | `claude-opus-5-thinking-high` | ano |

`cursor-grok-4.6-medium` v Coder `medium` **nekoliduje** s Adversary `medium` (Sonnet 5).
Tvrzení plánu o omezeních souhlasí; kontrolní tabulka po úpravě musí v `high` ukazovat
Grok 4.5 (ne 4.6) a v `low`/`medium` Grok 4.6 — to DoD teď výslovně žádá včetně `low`.
DoD je splnitelné: R4 pokrývá všech šest buněk a žádá absenci starého slugu právě v nich.

Volba „úsilí vs generace" jako úsudek do `status.md` (ne jako fakt) je správný postoj
vůči `authority: Human` a vůči větě v `AGENT_MODELS.explanation.md` o Grok 4.5.

### R2 — překlad proti českému originálu

České znění v `doc/runs/20260816-1302-realization-layer-91/status.md` (ř. 83–91) nese tři
nosné závazky. Angličtina v plánu je nese všechny:

1. autorita UI pro roli rodičovského okna; katalog pro ni neplatí; **nehlásí se jako
   odchylka**;
2. při kolizi ustupuje **druhá** role, nikdy volba Humana; ustupuje **uvnitř katalogu** na
   nejbližší pásmo s jiným slugem; jinak se Coordinator ptá;
3. katalog vládne Coderovi jen tehdy, je-li Coder subagent; jinak ekonomika okna.

**Nic nosného v překladu nechybí.** „druhá role" / „the other role" odpovídá originálu
lépe než zúžení na „delegated" z kola 1. Drobný stylový posun („Chceš-li…" → „For the
catalog to govern…") nemění závazek.

Zbytek z kola 1 (sloučit se sekcí „Cursor limitation", nepřidat třetí paralelní odstavec)
plán stále nepojmenovává souborově — to je **instrukce pro Codera**, ne důvod k REVISE.

### R1 a R3 — rozpočet a znění jako pravidla

Znovu spočítáno:

- R1 = 3 fyzické řádky; R3 = 3; s jedním prázdným řádkem mezi nimi = **7 ≤ 8**.
- Projekce `07-ice-workflow.mdc`: 110 + 7 = **117 ≤ 150**.
- R2 ≈ 11 řádků do scoped souboru: 84 + 11 ≈ **95 ≤ 250**.

R1 teď váže znovuotevření na **same run** a pokračování vlastního počítadla — obejití
„nová smyčka pod jiným jménem" z kola 1 je uzavřené. R3 říká **intent delta** a kotvu
**before the Coder started** — obě dřívější díry (ACCEPT plánu místo delty; „first line
of code" psaná rodičem) jsou uzavřené. Zbývající jemnost („Coder started" u rodičovského
okna hrajícího Codera) čte se jako start té role, ne start subagenta; to stačí.

### Definition of Ready (kolo 2)

Všechny položky z kola 1 drží; položka DoD o absenci `cursor-grok-4.6-high` teď sedí na
R4 (šest buněk). Plán je připravený k implementaci.

### Co jsem ověřil v kole 2

- Spočítány řádky R1/R3/R2 proti 8 / 150 / 250.
- Spočítána matice Planner≠Critic a Coder≠Adversary ve `low`/`medium`/`high` po
  deklarované substituci (vše True).
- Angličtina R2 porovnána větu po větě s českým blokem v
  `20260816-1302-realization-layer-91/status.md`.
- `wc -l`: stále 110 a 84 u cílových rules před zápisem.

---

## Kolo 1 (záznam) — verdikt REVISE

Níže beze změny smyslu; historický záznam prvního kola.

### Verdikt kola 1
REVISE

### Zjištění k rozsahu a k chybějícímu change.md

Absence `change.md` je **správně**. `rules/07-run-artifacts.mdc` ho vyžaduje jen když se
mění strom. Plán nemění `contracts`, `## Meaning`, hrany ani status žádného uzlu — jen
text v `code_paths` uzlu `i0002` a hodnotu v souboru, který strom vědomě nevlastní.

To, že always-applied pravidlo zaváže každého budoucího agenta, **není** samo o sobě
záměr. `i0002` říká, *co jsou rules* (standing constraints, aktivace jako vzácný zdroj,
limity 150/250), ne *které věty* v nich musí stát. Kdyby každé doplnění metodiky
vyžadovalo deltu Meaning, každý editorial zásah do `rules/` by budil Kritika záměru a
kazil fingerprint realizace — to je proti A6 (frugalita) i proti oddělení vrstvy
realizace od znění uzlu.

`i0002` **nemá** říkat R1–R3 jmenovitě. Má dál držet kontrakty na aktivaci a délku;
obsah workflow patří do souborů, které už vlastní. Závažnost pokrývá klasifikace `high`
(dotyk `.cursor/` / metodiky) a povinná brána Humana po výsledku — ne falešná změna
stromu.

Rozsah outputs je v pořádku vůči `slice.md` (rules pod `i0002`) plus výslovně
deklarovaný `AGENT_MODELS.md` (owner: žádný uzel; `i0001` Non-goals). `incidental: []`
je přijatelné: `_realization.yaml` je vždy povolený.

### Zjištění k umístění pravidel

**R1 → `07-ice-workflow.mdc`.** Správně. Jediný always-applied text, který už říká
„Loops are bounded: after 3 rounds…". Čtenář, který počítá kola, čte právě ten odstavec.
Umístit R1 jen do skillu by znamenalo, že Coordinator při skládání běhu pravidlo
nevidí, dokud skill nenačte.

**R3 → `07-ice-workflow.mdc`, ne jen `skills/intent-change/SKILL.md`.** Správně jako
*invariant běhu*. Skill už v kroku 8 říká „Only now may implementation start" — to je
postup Plannera při změně stromu. R3 řeší jinou otázku: *kdy smí jeden run_id sloučit
delu a kód*. Tu skládá Coordinator *před* volbou skillu. Kdyby R3 žilo jen ve skillu,
čtenář při „implementuj podle accepted plánu + drobná delta" skill nemusí otevřít a
díru z `20260816-1302` zopakuje. Co čtenář ztratí bez skillu: detail pořadí promote →
validate → code; ten ve skillu má zůstat. Co ztratí bez workflow: tvrdé „smí / nesmí"
pro kombinovaný běh. Plán správně nechává skill nedotčený a nabízí Kritiku nález — ten
nález **neplatí** jako důvod k přesunu; dual write by jen plýtval rozpočtem.

**R2 → `00-model-policy.mdc`.** Umístění správné (scoped, self-described authority for
resolution/constraints; 84/250). Útok: soubor už má sekci „Cursor limitation" a katalog
už má téměř tutéž větu. Plán musí říct **kam přesně** R2 vstoupí (rozšířit / nahradit
„Cursor limitation", ne přidat třetí paralelní odstavec). Jinak Coder vyrobí rozporné
dvojí znění v jednom always-requested souboru.

**R4 → `AGENT_MODELS.md`.** Správně jako hodnota, ne pravidlo.

### Zjištění ke znění pravidel

#### R1 (3 řádky) — téměř doslovně z `status.md` běhu `20260816-2145`

Počítáno: 3 fyzické řádky. S R3 (3) a jedním prázdným řádkem mezi nimi = **7 ≤ 8**.
Rozpočet drží; po vložení `07-ice-workflow.mdc` ≈ 117 řádků ≪ 150.

Útok na termíny: „gate" je v tabulce Gates pojmenované; „round counter" stávající text
jen říká „after 3 rounds" bez explicitního „per gate" — R1 to *zavádí*, což je v pořádku,
ale Coder musí R1 nalepit těsně za větu o Loops, jinak „earlier gate's round counter"
visí ve vzduchu. „Reopens" není definované: kompetentní agent může tvrdit, že nález
Adversáře je *nová* brána, ne znovuotevření Kritika, a počítadlo „nenuluje", protože
začne nové. Záměr Humana (čtvrté kolo Kritika po ACCEPT) R1 pokrývá jen tehdy, když
„reopen" čteme jako „stejná role-brána znovu běží v témže run_id". To v textu chybí.
**Při revizi doplnit jednu krátkou kotvu** (např. same gate name / same run), jinak R1
jde obejít přejmenováním smyčky. Jinak je znění použitelné.

#### R3 (3 řádky)

Útok: „the Critic accepted the delta" — která brána? U `high` jsou dvě (intent change i
plan). Záměr z `20260816-1302` je ACCEPT **delty záměru** před kódem; znění to říká
slovem „delta", ale agent může splnit ACCEPT plánu a deltu nechat bez Kritika.
„Before the first line of code" — undefined: testy, scaffold, úprava `VERIFY.md`, zápis
do `report.md`? Lze psát testy „ještě to není production code". „Accepted … afterwards
… stamp" je dobré zdůvodnění, ne díra.

**Revize:** nahradit „first line of code" kotvou vázanou na roli Coder / změnu souborů
mimo `doc/runs/` a `doc/intent/` proposed, **nebo** na start Codera; a říct výslovně
„Critic on the intent change" (ne jen „the Critic"). Bez toho R3 zakazuje scénář
`20260816-1302` jen proti poctivému čtenáři.

#### R2 (4 řádky) — **blocker**

Plánované znění je **ořez** proti rozhodnutí Humana v
`doc/runs/20260816-1302-realization-layer-91/status.md` (odstavce o autoritě UI, o tom
že se to **nehlásí jako odchylka**, a o kolizi s tvrdým omezením: ustupuje druhá role
*uvnitř katalogu na nejbližší pásmo s jiným slugem*; nelíší-li se žádný → ptát se;
důsledek „Coder musí být subagent").

Znění v plánu říká jen „the delegated role yields". Kompetentní agent **splní** R2 tím,
že libovolně substituuje jiný slug — přesně chování, které `00-model-policy.mdc` bod 4
už zakazuje („do not substitute silently") a které R4 má léčit. Chybí také zákaz hlásit
volbu Humana jako odchylku od katalogu.

**Revize (konkrétně):** do `00-model-policy.mdc` zapracovat tři závazky z Humanova
statusu, ne jen první větu: (1) UI volba je autoritativní pro roli rodičovského okna a
**není odchylka**; (2) při kolizi s `adversary_differs_from_coder` /
`critic_differs_from_planner` ustupuje **delegovaná** role uvnitř katalogu (nejbližší
pásmo s jiným slugem; jinak se ptát); (3) má-li katalog vládnout Coderovi, musí být
Coder subagent. Sloučit se sekcí „Cursor limitation", nepřidávat třetí kopii. Rozsah
řádků scoped pravidla to unese (84 → stále ≪ 250).

#### R4 — **blocker**

V YAML je `cursor-grok-4.6-high` na **šesti** místech: Coordinator `medium`, Planner
`low`/`medium`, Critic `high`, Coder `medium`/`high`. Plán mění jen Critic+Coder
`high`. Definition of Done ale vyžaduje: „`AGENT_MODELS.md` neobsahuje
`cursor-grok-4.6-high`". To je vnitřní rozpor plánu: po provedení R4 jak je napsané v
sekci „Znění" DoD **neprojde**, dokud zůstanou čtyři výskyty.

Substituce Critic/Coder `high` → `cursor-grok-4.5-high` **sama o sobě** omezení
`critic_differs_from_planner` a `adversary_differs_from_coder` v pásmu `high` nerozbije
(Planner/Adversary = Opus). Stejně by držela náhrada všech šesti výskytů za
`cursor-grok-4.5-high` nebo za `cursor-grok-4.6-medium`.

**Revize:** buď (A) R4 = odstranit **všechny** výskyty `cursor-grok-4.6-high` a
aktualizovat kontrolní tabulku ve všech pásmech, nebo (B) zúžit DoD na „Critic a Coder
`high` neobsahují …" a výslovně nechat ostatní výskyty jako známý dluh s odkazem na
navazující běh. Varianta A je konzistentní se zadáním „slug, který nejde spustit". Při
A zvolit slug vědomě: `AGENT_MODELS.explanation.md` píše, že Grok 4.5 do katalogu
nepatří — buď `cursor-grok-4.6-medium` (dostupný, rodina 4.6), nebo 4.5-high s
explicitním zápisem v `status.md`, že se tím přepisuje věta z explanation. Mlčet o tom
nejde.

### Vědomá odmítnutí

**Kontrakt na spustitelnost slugů** — upřímná střídmost, ne únik. Seznam modelů prostředí
repozitář neobsahuje; `enforced_by: review` je vždy Human (`07-realization.mdc`). Bod 4
v `00-model-policy.mdc` už říká „verify … ask — do not substitute silently". Zakládat
review-kontrakt v úklidovém běhu by jen přesunulo dluh do fronty akceptací.

**Vlastnictví `AGENT_MODELS.md` stromem** — upřímné. `i0001` Non-goals: „Not a model
catalogue authority". Sahat na to by bylo změnou non-goals = vždy Human a jiný běh.
Oprava hodnoty katalogu bez vlastnictví uzlem je přesně to, co non-goal dovoluje.

### Definition of Ready (kolo 1)

| Položka | Verdikt |
|---|---|
| Měřitelný cíl | OK — tři rozhodnutí zapsaná + slug opravený |
| Konkrétní outputs | OK — tři cesty |
| Slice z `intent slice` | OK — `slice.md` odpovídá `intent slice i0002 --for plan` |
| Dotčené kontrakty mají enforcer | OK — žádný nový; `i0002` c1/c2 beze změny |
| Test spec (happy/edge/error) | Hraníčně OK — žádný nový test; regresní sada = `template_checks` + validate + scope. Pro čistě textový zásah do rules přijatelné, pokud DoD zůstane vázané na příkazy |
| DoD mapuje na artefakt/příkaz | **FAIL** — položka „neobsahuje `cursor-grok-4.6-high`" nesedí na R4 jak je vymezené |
| Incidental vyjmenované | OK — prázdný seznam je výslovný |
| Žádná blokující open question | OK — `i0002.open_questions: []` |
| Izolovaně implementovatelné | OK po opravě R2/R4 |

Povinná failing-test evidence z `07-run-artifacts.mdc` se netýká (nevznikají nové testy);
to plán správně říká.

### Co jsem ověřil sám (kolo 1)

- `wc -l`: `rules/07-ice-workflow.mdc` = 110, `rules/00-model-policy.mdc` = 84.
- R1 = 3 řádky, R3 = 3, R1+R3 + 1 blank = 7 (≤ 8); projekce always-applied ≈ 117 ≤ 150.
- `python3 tools/intent/cli.py owner` → obě rules → `i0002`; `AGENT_MODELS.md` → no owner.
- `intent slice i0002 --for plan` shodný se `slice.md`; `i0002` realization `not_claimed`.
- `intent validate` → 0 error(s), 0 warning(s).
- `AGENT_MODELS.md`: 6× `cursor-grok-4.6-high` (ne 2).
- Po náhradě Critic+Coder `high` → `cursor-grok-4.5-high` platí Planner≠Critic a
  Coder≠Adversary v `high`; stejné omezení drží i plná náhrada všech šesti výskytů.
- Humanova znění: R1 v `20260816-2145-…/status.md`; R2+R3 kritérium v
  `20260816-1302-…/status.md`; `i0001` non-goal o katalogu ověřen ve front matter uzlu.
- `skills/intent-change/SKILL.md` Step 8 už zakazuje implementaci před Kritika delty —
  neřeší kombinovaný run_id; proto R3 patří do workflow.

### Co musí plán změnit, aby prošel (bez dalšího kola otázek)

1. **Sjednotit R4 a DoD:** buď odstranit všechny výskyty `cursor-grok-4.6-high` (+ tabulka
   ve všech pásmech) a zvolit slug (`4.6-medium` vs `4.5-high`) s poznámkou vůči
   `AGENT_MODELS.explanation.md`, nebo zúžit DoD na dvě buňky a pojmenovat zbytek jako
   dluh mimo tento běh.
2. **R2:** zapsat plné Humanovo pravidlo (autorita UI ≠ odchylka; ustoupení delegované
   role uvnitř katalogu / ptát se; Coder-subagent), sloučit do „Cursor limitation".
3. **R3 (a doporučeně R1):** zpřesnit „delta" = Critic on the intent change; „before
   code" = před startem Codera / před zápisem mimo run+proposed intent; u R1 kotva
   „same gate in the same run".
4. DoD po úpravách znovu projít položku po položce — položka o absenci
   `cursor-grok-4.6-high` musí být splnitelná přesně tím, co R4 slibuje.
