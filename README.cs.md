# cursor-best-practices-template — průvodce po česku

Tento text vysvětluje, **co** je `cursor-best-practices-template`, **proč** vznikl a
**jak** se s ním pracuje den za dnem. Je psaný pro člověka, který vyvíjí software v Cursoru
s pomocí AI agentů — sám nebo v malém týmu — a chce, aby výsledek vypadal jako práce jedné
disciplinované firmy, ne jako sled náhodných chatů.

Technická dokumentace v angličtině: [`README.md`](README.md) (instalace, pravidla, skilly)
a [`README.project_management.md`](README.project_management.md) (metodika APM do detailu).
Angličtina je vždy zdrojem pravdy; tento průvodce ji shrnuje a vysvětluje.

---

## Obsah

1. [O co jde — jednou větou a jedním přirovnáním](#1-o-co-jde--jednou-větou-a-jedním-přirovnáním)
2. [Jaké problémy to řeší](#2-jaké-problémy-to-řeší)
3. [Slovníček pojmů](#3-slovníček-pojmů)
4. [Instalace do projektu krok za krokem](#4-instalace-do-projektu-krok-za-krokem)
5. [Co se v projektu objeví a co s tím](#5-co-se-v-projektu-objeví-a-co-s-tím)
6. [Nastavení: jazyk, modely, projektové zásady](#6-nastavení-jazyk-modely-projektové-zásady)
7. [Metodika APM — jak vypadá práce na projektu](#7-metodika-apm--jak-vypadá-práce-na-projektu)
8. [Co dělám já a co dělá agent — typický den](#8-co-dělám-já-a-co-dělá-agent--typický-den)
9. [Git: co agent nikdy neudělá sám](#9-git-co-agent-nikdy-neudělá-sám)
10. [Vlastní pravidla projektu](#10-vlastní-pravidla-projektu)
11. [Aktualizace šablony](#11-aktualizace-šablony)
12. [Časté situace a co s nimi](#12-časté-situace-a-co-s-nimi)
13. [Mapa: kde co najdu](#13-mapa-kde-co-najdu)

---

## 1. O co jde — jednou větou a jedním přirovnáním

**Jednou větou:** je to sada pravidel, pracovních postupů a malého instalačního nástroje,
která se jedním příkazem nahraje do každého vašeho projektu a řídí, jak se v něm chovají
AI agenti v Cursoru.

**Přirovnání:** představte si, že do firmy nastupují noví kolegové — velmi rychlí, sečtělí,
ale bez paměti mezi směnami a s tendencí chválit vlastní práci. Aby to fungovalo, dáte jim:

- **firemní směrnice** (jak psát kód, jak commitovat, kdy použít Docker, čemu nevěřit) —
  to jsou *pravidla*;
- **pracovní postupy** pro opakující se úkony (rozjeď Docker, spusť testy, naplánuj etapu,
  zreviduj práci kolegy) — to jsou *skilly* a *příkazy*;
- **organizaci práce**: kdo plánuje, kdo programuje, kdo nezávisle kontroluje a kdy se má
  zeptat šéfa — to je *APM*, metodika řízení projektu.

Šablona je ta složka směrnic. Instalátor ji rozdá do projektů a umí ji později aktualizovat,
aniž by přepsal to, co jste si v projektu nastavili sami.

---

## 2. Jaké problémy to řeší

Když člověk nechá agenta „prostě to naprogramuj", opakují se stejné potíže:

| Problém | Co s tím šablona dělá |
|---|---|
| Každý chat programuje jinak — jiný styl, jiné konvence, jiné komentáře. | Pravidla (`.mdc`) se načítají do každého chatu automaticky. Styl je stejný ve všech projektech. |
| Agent napíše kód **a sám prohlásí**, že testy prošly a zadání je splněné. Přeceňuje se. | Kód kontroluje **jiný model v čistém kontextu** (Reviewer) proti zadání a skutečnému `git diff`, ne proti tvrzení autora. Navíc běží mechanická kontrola `make check` (linter, typy, testy). |
| Rozhodnutí z chatu se ztratí, když se okno zaplní. Další agent je tiše poruší. | Paměť projektu jsou **soubory** (specifikace, plány, reporty) a krátký **registr rozhodnutí** `DECISIONS.md`, který agent před každou fází projde. |
| Kontrolovat každou změnu ručně je práce na plný úvazek — tak to člověk přestane dělat. | **Pásma rizika** (`low`/`medium`/`high`): rutinní změny si projdou jen mechanickou kontrolou, riskantní přijdou na váš stůl s krátkým briefingem. |
| Agent commitne, pushne nebo smaže něco, co jsem nechtěl. | Git operace jsou zakázané bez **výslovné spouštěcí fráze**. Commit agent nabídne, nikdy neprovede. |
| Agent přečte stránku z webu a splní instrukci, která je v ní schovaná. | Pravidlo bezpečnosti: vše, co agent načte, jsou **data, ne příkazy**. |
| Pravidla stojí tokeny na každém dotazu. | Vždy načtená pravidla jsou krátká (limit 150 řádků, dohromady ~600), ostatní se připojují jen k odpovídajícím souborům. Instalátor odstraní dvojjazyčné komentáře — kopie je zhruba poloviční. |
| Dotazy agenta na mě chodí po pěti najednou a bez doporučení. | **Protokol rozhodování**: jedno rozhodnutí na zprávu, polopaticky vysvětlený problém, 2–4 možnosti, jedno doporučení, pak čekat. |

---

## 3. Slovníček pojmů

Nejdřív pojmy z Cursoru, potom naše.

**Cursor** — editor kódu s vestavěnými AI agenty. Agent čte a píše soubory, spouští
příkazy a řídí se konfigurací v adresáři `.cursor/` v projektu.

**Pravidlo (rule)** — soubor `.cursor/rules/*.mdc`: Markdown s hlavičkou. Cursor jeho text
vloží agentovi do kontextu. Tři režimy: `alwaysApply: true` (vždy — proto krátké),
`globs` (jen když je v kontextu odpovídající soubor, např. `**/*.py`) a *jen popis*
(agent si ho přitáhne, když se popis hodí k úkolu).

**Skill** — `.cursor/skills/<název>/SKILL.md`: pracovní postup s očíslovanými kroky a
přesnými příkazy. Agent si ho vybere podle popisu, nebo ho pojmenujete („postupuj podle
skillu `execute-task`").

**Příkaz (command)** — `.cursor/commands/<název>.md`: to samé, ale spouští se lomítkem
v chatu: `/push`, `/role-show`.

**Hook** — skript, který Cursor spustí při události. Používáme `sessionStart`: při otevření
projektu zapne git hook, který z commit zpráv maže automaticky přidávanou stopu
`Co-authored-by: Cursor`.

**Subagent** — samostatný agent, kterého hlavní chat spustí na jednu ohraničenou práci.
Má čistý kontext a **vlastní model**. V APM tak běží Coder i Reviewer.

**APM (Agentic Project Management)** — naše metodika: Planner plánuje, Coder programuje,
Reviewer nezávisle kontroluje, člověk rozhoduje. Práce je členěná na *epiky* a *tasky*.

**Role** — Planner, Coder, Reviewer, Human. Role je popis práce, ne konkrétní model; který
model roli hraje, je nastavení (`AGENT_MODELS`).

**Epika, task** — epika je kus roadmapy velikosti jednoho dodání (6–8 tasků). Task je
půl dne až dva dny práce Codera, samostatně implementovatelný a testovatelný.

**Pásmo (band)** — třída rizika tasku: `low`, `medium`, `high`. Určuje se předem podle
pevných spouštěčů (změna schématu databáze, mazání, nedůvěryhodný vstup, …), ne podle
pocitu. Pásmo rozhoduje, jaký model task dostane **a** kolik kontroly.

**Lidská brána (Human gate)** — místo, kde se agent zastaví a čeká na vaše rozhodnutí.
Otevírá se u každého `high` tasku, u každého plánu epiky a u každé revize roadmapy — ne
po každém tasku.

**Deterministický gate** — mechanická kontrola bez LLM: `make check` = linter + formát +
striktní typy + testy. Stejný příkaz spouští Coder, Reviewer i CI, takže „prošlo" znamená
všude totéž. Hotové pro Python.

**DoR / DoD** — *Definition of Ready*: kontrolní seznam, kterým musí projít zadání tasku,
než ho dostane Coder. *Definition of Done*: kontrolní seznam, který Coder vyplní a Reviewer
ověří proti skutečným artefaktům.

**Zdroj pravdy (SoT) a `DECISIONS.md`** — SoT jsou dokumenty, které projekt zavazují
(výchozí je `spec.md`). `DECISIONS.md` je krátký registr už rozhodnutých otázek, který agent
projde před každou fází — proto nikdy tiše neporuší starší rozhodnutí.

**Config Resolution** — mechanismus tří nastavení (`LANGUAGE`, `AGENT_MODELS`,
`DESIGN_RULES`): šablona dodá výchozí soubor `.cursor/apm_config/<NÁZEV>.default.md`,
vy ho můžete **celý nahradit** souborem `doc/apm_config/<NÁZEV>.user.md`.

**`TEMPLATE_MANIFEST`, `TEMPLATE_VERSION`** — dva soubory, které instalátor zapíše do
`.cursor/`. Manifest vyjmenuje soubory patřící šabloně (jen ty se při aktualizaci přepíšou);
verze říká, jaká revize šablony je nainstalovaná.

---

## 4. Instalace do projektu krok za krokem

Potřebujete Python 3.10+ (bez dalších knihoven), git a Cursor.

```bash
# 1. Šablonu naklonujte jednou, kamkoli — zůstává oddělená od vašich projektů
git clone git@github.com:ivomarvan/cursor-best-practices-template.git ~/dev/cursor-best-practices-template

# 2. Nainstalujte do projektu; --lang cs znamená, že s vámi agent bude mluvit česky
python3 ~/dev/cursor-best-practices-template/scripts/install_into_project.py ~/dev/muj-projekt --lang cs

# 3. Zkontrolujte (jen čte; vrátí 1, když něco nesedí)
python3 ~/dev/cursor-best-practices-template/scripts/check_installation.py ~/dev/muj-projekt
```

Pak projekt otevřete v Cursoru. Hook se aktivuje sám, pravidla platí okamžitě. V prvním
chatu udělejte dvě věci:

```text
/role-show                          # ukáže, který model hraje kterou roli — zpočátku vše "unassigned"
/role-assign Planner high <model>   # …přiřaďte; nebo odpovězte, až se agent zeptá sám
```

Adresáře `.cursor/` a `doc/apm_config/` **commitněte** do repozitáře projektu — jsou jeho
součástí a kolegové po `git pull` dostanou stejné chování agenta.

> Šablona uvnitř nese dvojjazyčné komentáře `<!-- cs: … -->` pro své správce. Instalátor je
> při kopírování odstraní — v projektu je `.cursor/` jen anglický a o polovinu menší. To,
> že s vámi agent mluví česky, řídí `LANGUAGE.user.md`, ne komentáře.

---

## 5. Co se v projektu objeví a co s tím

```
muj-projekt/
├── .cursor/                          ← soubory šablony + vaše vlastní přídavky
│   ├── rules/        *.mdc           ← pravidla (šablona) + 9xx-*.mdc (vaše)
│   ├── skills/       <název>/SKILL.md
│   ├── commands/     push.md, role-assign.md, role-show.md
│   ├── hooks/, hooks.json
│   ├── apm_config/   *.default.md    ← výchozí nastavení (needitovat)
│   ├── TEMPLATE_MANIFEST             ← seznam souborů šablony (generovaný, needitovat)
│   └── TEMPLATE_VERSION              ← nainstalovaná revize + čas
└── doc/apm_config/                   ← VAŠE nastavení — vznikne jednou, nikdy se nepřepíše
    ├── AGENT_MODELS.user.md          ← který model hraje kterou roli × pásmo
    ├── DESIGN_RULES.user.md          ← závazné zásady projektu, zakázané technologie, výjimky z Dockeru
    └── LANGUAGE.user.md              ← jazyk komunikace (z --lang)
```

Zlaté pravidlo: **soubor, který je v `TEMPLATE_MANIFEST`, neupravujte** — příští
aktualizace ho tiše vrátí. Všechno, co chcete změnit, má své místo v `doc/apm_config/` nebo
ve vlastních `9xx-` pravidlech (kapitola 10).

---

## 6. Nastavení: jazyk, modely, projektové zásady

### Jazyk
`doc/apm_config/LANGUAGE.user.md` — vznikne z `--lang`. Kdykoli ho ručně upravte. Řídí
jazyk chatu **i** jazyk APM dokumentů (reportů, revizí). Kód a komentáře v kódu jsou vždy
anglicky.

### Modely
Role nejsou přivázané ke jménům modelů — modely a ceny se mění. Tabulka **role × pásmo**
v `AGENT_MODELS.user.md` říká, kdo co hraje:

| Role | `low` | `medium` | `high` |
|---|---|---|---|
| Planner | — | … | … |
| Coder | … | … | … |
| Reviewer | — | … | … |

- `unassigned` → agent se **zeptá**, než v té roli začne pracovat, a nabídne uložení.
- `—` → buňka se neuplatní: Planner `low` nenastává (Planner má pásmo za celou epiku),
  Reviewer `low` je jen mechanický gate — LLM by tam nic nepřidal.
- Ekonomika: **silný model na myšlení** (Planner, Reviewer), **levnější na psaní** (Coder).

Cursor sám nepřepne model hlavního okna — agent vám to připomene. Subagentům (Coder,
Reviewer) předá model automaticky jako parametr volání.

### Projektové zásady — `DESIGN_RULES.user.md`
Sem patří vše, co má **přebít obecná pravidla**: zakázané technologie, výjimky
z povinného Dockeru, seznam zdrojů pravdy, neporušitelné architektonické invarianty. Agent
si ho musí přečíst před každým programováním. Pište stručně, jako smlouvu.

---

## 7. Metodika APM — jak vypadá práce na projektu

```
Napíšu brief (neformálně, jakkoli dlouhý)
   ↓  Fáze 0 — skill project-init (Planner ↔ já)
spec.md + roadmap.md                                          [schvaluji]
   ↓  Fáze E — skill plan-epic (Planner)              pro každou epiku
plán epiky + zadání tasků + DoD   [kontrola DoR]              [schvaluji plán]
   ↓  Fáze T — skill execute-task (Coder, subagent)   pro každý task
kód + testy + make check + report.md
   ↓  Fáze R — skill review-task (Reviewer, subagent, jiný model)
review.md: APPROVE / REQUEST CHANGES  (max 3 kola; 2. REQUEST CHANGES zvedne pásmo)
   ↓                                                          [vidím jen high tasky]
   ↓  Fáze ER — skill review-epic (Coder + Planner)
report epiky (každý task, pásmo, kola revize, počet BLOCKED) + kontrola roadmapy  [rozhoduji]
```

### Fáze 0 — zahájení projektu
Dáte Plannerovi zadání v libovolné podobě; uloží ho **doslova** do `brief.md`. Pokud
v zadání chybí podstatné věci, ptá se — **po jednom**, s možnostmi a doporučením. Pokud už
zadání obsahuje registr rozhodnutí a nemá otevřené otázky, ptaní přeskočí. Napíše
`spec.md` (co stavíme: cíl, rozsah, ne-cíle, klíčová technická rozhodnutí, předpoklady,
kritéria hotovosti, zdroje pravdy) a `roadmap.md` (seznam epik v pořadí). Podrobné části
zadání — architektura, datový model — **nekomprimuje**, přesune je beze změny do
`doc/architecture/` a odkáže. Vy oba dokumenty schválíte.

### Fáze E — plánování epiky
Planner rozloží epiku na **6–8 tasků**. Každý má zadání s osmi částmi: cíl, vstupy,
výstupy, **kontextový balík** (co číst, čeho se nedotýkat, jaká rozhraní už existují),
závislosti, specifikace testů, DoD, doporučená úroveň Codera. Zadání musí projít **DoR** —
je cíl měřitelný? jsou výstupy konkrétní? jsou pojmenované testy pro šťastnou cestu, hranu
i chybu? Vy plán schválíte; Planner vám ho předloží s briefingem.

### Fáze T — provedení tasku
Coder (subagent) přečte zadání, implementuje **přesně to a nic víc**, napíše testy, spustí
`make check`, vyplní DoD a napíše `report.md` česky. Rozsah reportu závisí na pásmu: `high`
sedm sekcí (včetně **odchylek od zadání** — nezveřejněná odchylka je nález Revieweru),
`medium` čtyři, `low` pět řádků. Když zadání něco nepokrývá, Coder se **neptá vás**, vrátí
otázku Plannerovi. Architektonická rozhodnutí zapisuje jako ADR do
`doc/architecture/decisions/`.

### Fáze R — nezávislá revize
Reviewer (subagent, **jiný model než Coder**) si nálezy udělá z `git diff`, zadání, DoD a
vlastního běhu testů — Coderův report otevře až nakonec, aby ověřil jeho poctivost. Ověří
každé ✅ v DoD proti skutečnému artefaktu, hledá práci mimo zadání, slabé testy, chybějící
chybové případy, nepřiznané odchylky. Napíše `review.md` s verdiktem. Smyčka s Coderem má
**nejvýš 3 kola**; druhé `REQUEST CHANGES` zvedne pásmo tasku (u `high` se rovnou zastaví
a jde k vám — problém je v zadání, ne v modelu). Po APPROVE vám Planner **nabídne commit**
jednou větou; provedete ho vy spouštěcí frází.

### Fáze ER — uzavření epiky
Coder sepíše report epiky s tabulkou **všech** tasků: pásmo, zda jste ho gatovali, počet
kol revize, počet `BLOCKED`. Tam poprvé vidíte `medium`/`low` tasky. Planner znovu přečte
roadmapu a specifikaci a předloží jeden ze tří závěrů: roadmapa beze změny · potřebuje
úpravu (konkrétně a proč) · zásadní revize (nejdřív probrat). Rozhodnete vy.

### Průzkumné epiky (spike)
Když otázka zní „je A nebo B rychlejší/levnější?", nejde o feature. Spike má vlastní
pravidla: DoR pojmenuje metriku, data a kandidáty; výstupem je tabulka výsledků + krátké
README, ne nutně produkční kód; testy pokrývají jen měřicí nástroj; DoD = vyplněné metriky
**a** ADR s volbou; Reviewer kontroluje **reprodukovatelnost**, ne kvalitu kódu; ukončení
je vaše rozhodnutí, nikdy automatický práh.

### Co není task
Překlep, dokumentace, drobná konfigurace, o kterou požádáte přímo — **žádná ceremonie**.
Žádné zadání, report ani Reviewer; platí jen pravidla Gitu a `make check`. Agent nesmí
odpovědět „BLOCKED, chybí epika".

---

## 8. Co dělám já a co dělá agent — typický den

| Situace | Co napíšu / udělám | Co se stane |
|---|---|---|
| Začínám projekt | Vložím brief a řeknu: „Zahaj projekt podle skillu project-init." | Planner uloží brief, doptá se po jednom, napíše spec + roadmapu, požádá o schválení. |
| Chci naplánovat další epiku | „Naplánuj epiku E020 (plan-epic)." | Planner napíše `plan.md` a zadání tasků, zkontroluje DoR, přijde s briefingem: kde jsme, co je nové, **jedno** rozhodnutí, co se stane, když nic neudělám. |
| Epika běží | Většinou nic. Odpovídám na `BLOCKED` otázky, které Planner přenese, a na nabídky commitu. | Planner spouští Codera a Reviewera jako subagenty; ti vrací jen `DONE: <cesta>` nebo `BLOCKED: <otázka>`. |
| Přijde brána `high` tasku | Přečtu briefing, rozhodnu. | Bez mě se nepokračuje. |
| Reviewer po APPROVE | „…s commitem do feature" (nebo neodpovím) | Commit na feature větev; nebo se pokračuje bez commitu a příští Reviewer si diff omezí na soubory tasku. |
| Chat se zaplnil | Otevřu nový a napíšu: *„Přečti `epic-NNN/plan.md` a stav všech adresářů tasků; pokračuj od prvního tasku bez `review.md` s verdiktem APPROVE."* | Planner naváže ze souborů, nic se nerekonstruuje z paměti. |
| Epika hotová | „Uzavři epiku (review-epic)." | Report epiky s tabulkou tasků; Planner navrhne, co s roadmapou; rozhodnu. |
| Drobnost mimo epiku | „Oprav překlep v README a pushni." → `/push` | Bez zadání a revize; `/push` spustí gate a commitne. |
| Nevím, jaký model kde běží | `/role-show` | Tabulka role × pásmo. |

Klíčový návyk: **rozhodnutí chci po jednom.** Pokud agent někdy začne sypat otázky dávkově,
odkažte ho na pravidlo `005-decision-protocol.mdc` — je vždy načtené.

---

## 9. Git: co agent nikdy neudělá sám

Pravidlo `020-git.mdc` zakazuje `commit`, `push`, `pull`, `merge`, `rebase`, `reset` a
force push bez vašeho výslovného souhlasu. Souhlas je **jen** jedna z těchto forem:

| Napíšu | Výsledek |
|---|---|
| `… s commitem` | commit přímo na `master` |
| `… s commitem s CI` | commit na `master`, hlídá CI, opraví max 3× |
| `… s commitem do feature` | nová větev `feature/eNNN-tNNN-slug` |
| `… s commitem do feature s CI` | feature větev + CI + squash merge do `master` |
| `/push` | `make check` → commit → push na `master` |

Před každým commitem skill `commit-task` vyžaduje APPROVE Revieweru (u `low` stačí gate),
spustí `make check` lokálně a odmítne přidat `.env`, klíče nebo `nogit_data/`. Commit zprávy
mají formát Conventional Commits (`feat(scope): …`), anglicky, v rozkazovacím způsobu, bez
stopy Cursoru (hook ji smaže).

---

## 10. Vlastní pravidla projektu

Vaše soubory žijí **vedle** souborů šablony v `.cursor/` a aktualizaci přežijí, protože
instalátor maže jen to, co je v `TEMPLATE_MANIFEST`.

| Co | Kam | Konvence |
|---|---|---|
| Pravidlo projektu | `.cursor/rules/9xx-<slug>.mdc` | `9xx-` je vyhrazeno projektům; šablona končí u `2xx` |
| Skill projektu | `.cursor/skills/<název>/SKILL.md` | jakýkoli název, který šablona nepoužívá |
| Příkaz projektu | `.cursor/commands/<název>.md` | totéž |
| Nastavení | `doc/apm_config/<NÁZEV>.user.md` | nahrazuje výchozí soubor celý |
| Závazné zásady, zákazy, výjimky z Dockeru | `doc/apm_config/DESIGN_RULES.user.md` | má přednost před pravidly šablony |

Pravidlo projektu smí pravidlo šablony **zúžit nebo rozšířit**. Chcete-li ho **přebít**,
napište to výslovně do `DESIGN_RULES.user.md` — ten má přednost; samotné konkurenční `.mdc`
by agentovi nechalo dvě protichůdné instrukce. `check_installation.py` vaše soubory vypíše
jako *project-owned (kept)* a upozorní na pravidlo mimo `9xx-`, které manifest nezná
(pravděpodobně sirotek ze starší verze).

---

## 11. Aktualizace šablony

```bash
cd ~/dev/cursor-best-practices-template && git pull
python3 scripts/install_into_project.py ~/dev/muj-projekt     # přepíše jen soubory šablony
python3 scripts/check_installation.py  ~/dev/muj-projekt      # kontrola, jen čte
cat ~/dev/muj-projekt/.cursor/TEMPLATE_VERSION                # co je teď nainstalované
```

Co se mezi verzemi změnilo, je v [`CHANGELOG.md`](CHANGELOG.md). Projekt se zaostávající
verzí běží s pravidly, která už nesedí ke skillům — nejdřív aktualizovat, potom pracovat.

---

## 12. Časté situace a co s nimi

**Agent se pořád ptá, jaký model má použít.** V `AGENT_MODELS.user.md` je buňka
`unassigned`. Přiřaďte ji přes `/role-assign` — nebo odpovězte a nechte agenta odpověď
uložit.

**Reviewer píše, že revize byla „path-scoped".** V pracovním stromu byly změny z více tasků
(mezi nimi se necommitovalo), tak porovnal jen soubory z výstupů tasku. Čistší je commit po
každém tasku — Planner ho po APPROVE nabízí; stačí odpovědět spouštěcí frází.

**Task dostal druhé REQUEST CHANGES a „zvedl pásmo".** Záměr: nejspíš bylo slabé zadání.
Task dostane silnějšího Codera a víc kontroly; u `high` se místo toho zastaví u vás. Report
epiky tyhle případy počítá — jsou to signály, kde Planner podcenil DoR.

**Chci, aby agent u drobnosti nezakládal epiku.** Nemusí — kapitola 7, „Co není task".
Pokud odpoví `BLOCKED`, odkažte ho na `090-apm-orchestration.mdc` § E.

**Šablona říká Docker povinně, ale tenhle projekt je firmware / jednoduchý skript.**
Výjimky jsou v pravidle `030` (firmware, desktop GUI, jednoduché skripty, jen dokumentace).
Projektově specifickou výjimku zapište do `DESIGN_RULES.user.md`, nikdy do pravidla
v `.cursor/`.

**Chci Reviewera i pro `low` tasky.** V `AGENT_MODELS.user.md` dejte místo `—` model.
Nikdy tam nenechte `unassigned` — každý `low` task by se zastavil dotazem.

**Mám vlastní git hooky (husky, pre-commit).** `session-start.sh` váš `core.hooksPath`
nepřepíše; vypíše návod, jak z vašeho `commit-msg` zavolat ten náš.

**Chci šablonu upravit pro sebe.** Forkněte ji, změny dělejte v `rules/`, `skills/`,
`apm_config/*.default.md`, držte anglický text jako zdroj pravdy a `<!-- cs: -->` komentáře
synchronní, spusťte `make check` (ruff, mypy, pytest — testy nainstalují šablonu do
dočasného projektu a zkontrolují ji). Rozhodnutí o šabloně jsou v `doc/DECISIONS.md`,
vědomě neopravené nálezy v `doc/KNOWN_LIMITATIONS.md`.

---

## 13. Mapa: kde co najdu

| Hledám | Soubor |
|---|---|
| Jak agent mluví a v jakém jazyce | `rules/000-communication-language.mdc`, `apm_config/LANGUAGE.default.md` |
| Kdo hraje kterou roli, pásma, eskalace | `rules/000-model-policy.mdc`, `apm_config/AGENT_MODELS.default.md` |
| Jak se mě agent ptá na rozhodnutí | `rules/005-decision-protocol.mdc` |
| Obecné programátorské zásady | `rules/010-general-programming.mdc` |
| Git, spouštěcí fráze, větve | `rules/020-git.mdc`, `skills/commit-task/SKILL.md`, `commands/push.md` |
| Docker — kdy a jak | `rules/030-docker-policy.mdc`, `rules/040-docker-standards.mdc`, `skills/docker-*` |
| Struktura adresářů, ADR, `.gitignore` | `rules/060-project-structure.mdc` |
| APM — dokumenty, fáze, DoR, spike, formát reportu | `rules/070-project-management.mdc` |
| APM — subagenti, brány, briefing, rozsah ceremonie | `rules/090-apm-orchestration.mdc` |
| Bezpečnost proti podvrženým instrukcím | `rules/080-agent-security.mdc` |
| Výchozí vs. projektové nastavení, vlastnictví `.cursor/` | `rules/200-project-design-rules.mdc` |
| Jazykové standardy | `rules/1xx-*.mdc` (Python, Vue, C++/ESP32, SQL, FastAPI, Qdrant, SQLAlchemy, Redis, Celery) |
| Skilly APM po fázích | `skills/project-init`, `plan-epic`, `execute-task`, `review-task`, `review-epic` |
| Python gate `make check` a CI | `skills/python-dev/templates/Makefile`, `ci.yml` |
| Příklady APM dokumentů | `doc/project-progress/` |
| Slovník APM pojmů (dvojjazyčný) | `skills/project-init/templates/GLOSSARY.md` |
| Instalace, kontrola, migrace ze submodulu | `scripts/install_into_project.py`, `check_installation.py`, `migrate_submodule_to_copy.py` |
| Co je nového | `CHANGELOG.md` |
