---
run_id: 20260817-2334-review-craft-and-claim-order-e2
intent_ids: ["i0002", "i0003", "i0004"]
role: Planner
model: claude-opus-5-thinking-high
complexity: high
status: in-progress
revision: 3
outputs: ["rules/07-ice-workflow.mdc", "rules/07-realization.mdc", "rules/07-run-artifacts.mdc", "skills/ice-run/SKILL.md", "skills/ice-review/SKILL.md", "skills/ice-implement/SKILL.md", "README.md", "tools/intent/realization.py"]
incidental: []
---

# Plán běhu — R5, R6, R7

> **Revize 2** po verdiktu `REVISE` v `critique.md`. Změněno: jednotná formulace výjimky
> pro `low` běhy na všech místech (B1–B3), schematická příkladová tabulka v R7 (B4), osmé
> místo `tools/intent/realization.py` v rozsahu, doložené pátrání po devátém místě,
> rozhodnutí o `grader-evidence.md` a přeměřené délky.
>
> **Revize 3** po druhé kritice. Změněny **jen tři věci**: R6-m nese kanonickou větu znak
> za znak (dřív to byla nepřiznaná varianta), Definition of Done položka 9 grepuje celou
> větu a hlídá nulový počet variant, položka 8 mluví o třech mutacích místo dvou. K tomu
> dva řádky do tabulky pátrání (`commands/`, `AGENT_MODELS.explanation.md`), oba čisté.
> Nic jiného se nehýbalo; délky se nepřeměřovaly, shell dál nevrací výsledky.

## Cíl

Zapsat do metodiky tři věci, které dnes drží jen tím, že si je někdo pamatuje: že
`grader.md` píše Coordinator z příkazů, které sám spustil (R5); že se nárok na realizaci
zapisuje až po **všech branách, které si úroveň složitosti žádá** — u `medium` a `high`
tedy až po nezávislé recenzi — a to na **všech místech**, která pořadí vyslovují nebo
z něj vycházejí (R6); a jak Adversář vlastně recenzuje — věta kontraktu proti kódu,
mutace místo přečtení, a na posledním povoleném kole vyčerpávající tabulka míst, která
větu nesou (R7). Běh nemění žádnou produkční logiku, žádný uzel záměru ani žádný kontrakt;
mění text pravidel, skillů, dvou míst v `README.md` a jednoho hlášení v
`tools/intent/realization.py`. Po běhu musí platit, že čtenář, který otevře **jediný**
z dotčených souborů, si z něj neodnese staré pořadí — a to na **každé** úrovni složitosti,
včetně `low`, kde Adversář neběží — a že všechny brány `VERIFY.md` plus
`template_checks.py` jsou zelené se soubory pod svými limity.

## Rozsah — osm míst se starým pořadím

Požadavek jmenuje pro R6 „step list, output checklist a `rules/07-realization.mdc`".
To je **neúplný** výčet. Staré pořadí vyslovuje nebo implikuje osm míst:

| # | Místo | Co dnes říká | Kde se opravuje |
|---|---|---|---|
| 1 | `skills/ice-run/SKILL.md` krok 7 | „Once `grader.md` is green, record the realization claim" | R6-a |
| 2 | `skills/ice-run/SKILL.md` output checklist | „Realization claimed for the affected node" bez pořadí | R6-c |
| 3 | `rules/07-realization.mdc` tabulka „Who may write what" | „`claim` \| Coordinator, after the Grader is green" | R6-d |
| 4 | `rules/07-realization.mdc` sekce „How it fits the run" | „After `VERIFY.md` is green, the Coordinator writes the claim" | R6-f |
| 5 | `rules/07-run-artifacts.mdc` odstavec u Definition of Done | „after the Grader is green, the **Coordinator** runs …" | R6-g |
| 6 | `rules/07-ice-workflow.mdc` tabulka rolí | Coordinator „claim realization after a green Grader" | R6-h |
| 7 | `README.md` diagram „How a change happens" + tabulka „Who may write what" | `GRADE -- green --> CLAIM`, pak `CLAIM --> ADV`, a tatáž řádka tabulky jako v pravidle | R6-k, R6-l |
| 8 | `tools/intent/realization.py:548` — text výjimky `TreeError` | „the Coordinator claims after the Grader" | R6-m |

Místo 7 je mimo slice (`intent owner README.md` → `no node owns README.md`), a proto ho
uvádím výslovně, ne potichu. Tři důvody, proč do běhu patří: je to nejčtenější soubor
repozitáře a čte se v izolaci, tedy přesně případ, který R6 zakazuje; **žádný uzel ho
nevlastní**, takže se jeho úpravou nemění ani kontrakt, ani záměr, a intent delta není
potřeba; a `README.md` si dnes protiřečí sám — druhý diagram (`README.md:426-429`) už
ukazuje pořadí Grader → Adversary → Human → Realization claim, tedy to nové. Zásah je
sedm řádků diagramu (7 → 7) a jedna řádka tabulky. `README.md` je proto v `outputs`,
ne v `incidental` — je to zamýšlený výstup, ne vedlejší škoda.

Místo 8 našel Kritik a Human rozsah běhu o něj **výslovně rozšířil**. `tools/` vlastní
uzel `i0004`, který je proto v `intent_ids`; jeho text se nemění, takže `i0004` zůstává
`realized` a nic se nestává `stale` (otisky pokrývají text uzlu, ne kód). Kontrakt `c12`
(„A realization claim signed by the Coder is refused") popisuje **odmítnutí**, ne jeho
formulaci, takže ho záměna textu hlášení neporušuje.

Jeden úkol tím padá na Coordinatora ještě před předáním plánu: `slice.md` byl vygenerovaný
pro `i0002` a `i0003`, takže ho je potřeba doplnit řezem pro `i0004`
(`python3 tools/intent/cli.py slice i0004 --for implement`). Coder čte jen slice; bez toho
by na `tools/intent/realization.py` neměl mandát, i když ho plán jmenuje.

Co v rozsahu **není**: `VERIFY.md` (jeho zmínka o kroku 7 zůstává pravdivá — krok 7 dál
běží brány a zapisuje `grader.md`), `AGENT_MODELS.md`, uzly záměru, zbytek `tools/`, a obě
follow-up položky z předchozího běhu (F1, F2). Žádný příkaz `realization unclaim` — Human
ho zvážil a zamítl, a plán se o něj nikde neopírá. **Nic pod `doc/runs/`** kromě adresáře
tohoto běhu (viz „Rozhodnutí o `grader-evidence.md`").

## Jedna formulace pro všechny úrovně — a proč právě takhle

Blokátory B1–B3 jsou jedna chyba: moje znění vyžadovalo verdikt recenze **absolutně**,
zatímco tabulka Gates v `rules/07-ice-workflow.mdc` říká u `low` Adversary = `no`. Běh
s úrovní `low` by pak nemohl nikdy nárokovat — pravidlo by bylo nepravdivé o většině
jednoduchých běhů, což je horší vada než ta, kterou R6 opravuje.

Řešení je **jedna kanonická formulace**, která je pravdivá na každé úrovni, protože
neříká „která brána", ale „všechny, které si úroveň žádá":

> **once every gate the level requires has passed**

Ta věta je přenositelná do všech osmi míst, je krátká, a její obsah je odvoditelný
z tabulky Gates — jediné definice toho, které brány si která úroveň žádá. Kde je místa
dost (scoped pravidla, skill, README), doplňuje ji jedna doslovná dovětková polověta
„at `low` the Grader, above it the Adversary too". Kde místo dost není (always-applied
pravidlo), stojí kanonická věta sama.

### Rozhodnutí o always-applied řádku (otevřená otázka Kritika)

`rules/07-ice-workflow.mdc` je jediné always-applied pravidlo v této sadě, které o nároku
mluví, a jeho 118 řádků se čte v **každém** obratu. Rozhodl jsem: řádek zůstane **terse
a bez výčtu úrovní**, ale bude nesen kanonickou formulací, tedy pravdivou na každé úrovni.
Důvody, v tomto pořadí:

1. **Pravdivost není otázka délky.** Kritik správně říká, že nepravdivý řádek je horší než
   dlouhý. Kanonická věta ale nepravdivá není — je jen nespecifická, a nespecifická věta,
   která ukazuje na definici, nikoho nesvádí k nesprávnému kroku.
2. **Definice je v témž souboru.** Tabulka Gates je 40 řádků pod tím řádkem. Čtenář, který
   potřebuje vědět, co si `low` žádá, ji najde bez otevření dalšího souboru. Výčet
   „the Grader at `low`, the Adversary above it" by tabulku Gates duplikoval — a duplikát
   je druhé místo, které se rozejde, tedy přesně vada, kterou tento běh zavírá.
3. **Cena je reálná.** Výčet by v nejdražším místě repozitáře stál asi deset slov
   v každém obratu. Scoped pravidlo `07-realization.mdc` (limit 250, dnes 148) a skill
   `ice-run` se čtou jen tehdy, když na nárok skutečně dojde — tam výčet patří.

Kdyby Human rozhodl jinak, změna je jedna náhrada v R6-h a délka to unese (32 řádků
rezervy). Zapisuji to jako rozhodnutí Plannera, ne jako jedinou možnost.

## Pátrání po devátém místě — kde jsem hledal a co jsem našel

Kritik našel osmé místo v adresáři, do kterého jsem se nedíval. Prohledal jsem proto celý
repozitář ještě jednou, a ne jen na slovo „claim". Zapisuji **dotazy i zásahy**, aby to
Adversář mohl zkontrolovat, ne zopakovat.

Dva řádky tabulky (`commands/`, `AGENT_MODELS.explanation.md`) doplnil až třetí kolo —
druhý z nich je gitignorovaný, takže ho výpis souborů nevrátil a musel jsem si na něj
vzpomenout z odkazu v `AGENT_MODELS.md`. Oba jsou čisté; je to doplnění pro úplnost, ne nález.

Vzorce (všechny case-insensitive tam, kde to má smysl):
`grader` · `claim` · `realiz` · `Adversary` · `review` · `after the Grader` ·
`Grader is green` · `green Grader` · `claims after` · `green` · `as soon as` ·
`immediately after` · `Once ` · `Step 7|Step 8|Step 9`.

| Kde | Nález |
|---|---|
| `rules/*.mdc` | pět míst, všechna už v tabulce rozsahu (`07-ice-workflow`, `07-realization` ×2, `07-run-artifacts` ×2 včetně pasti „failing-test evidence → `grader.md`") |
| `skills/*/SKILL.md` | `ice-run` ×2, `ice-implement` ×1, `ice-review` ×2 (kontrola 8, závažnost) — všechna v plánu |
| `skills/commit-task/SKILL.md:178` | „Finish the run (Grader green, review closed) before committing" — **už dnes správné pořadí**; nic neměnit, ale patří sem jako doklad, že jsem to čtení kontroloval, ne přeskočil |
| `tools/` (mimo testy) | **jediné** místo je `realization.py:548` (osmé místo). Ostatní zmínky jsou neutrální: `_policy.yaml` a `realization.py:512` mluví o `grader.md` jako o **evidenci** (profil `standard`), `main.py:329` říká „never the Coder" bez pořadí, docstringy popisují, co se ukládá |
| `tools/intent/tests/` | žádná aserce na text hlášení; `assertRaisesRegex` se v celém `test_realization.py` nevyskytuje |
| `hooks/`, `hooks.json` | žádný výskyt slov `grader`, `claim`, `realiz`, `Adversary` |
| `commands/` (jediný soubor `commands/push.md`) | prohledáno, **čisté**: mluví o CI, `git add`, commit message a push; o nároku ani o Graderovi ani slovo |
| `VERIFY.md` | „The Coordinator runs it as part of step 7 and records the output in `grader.md`" — o **rozsahové bráně**, ne o nároku; po revizi pravdivé, nemění se |
| `AGENT_MODELS.md` | jen slugy a `constraints`; řádek 81 naopak potvrzuje, že `low` běhy Kritika ani Adversáře nespouštějí |
| `AGENT_MODELS.explanation.md` (gitignorovaný, proto v prvním průchodu chyběl) | prohledáno, **čisté**: Gradera zmiňuje dvakrát jako roli („Grader není LLM", „Grader chytí uklouznutí"), nikde jako podmínku nároku |
| `doc/intent/nodes/*.md`, `_policy.yaml`, `_registry.yaml` | žádná věta o pořadí. `i0004` c8–c17 mluví o tom, co nárok **znamená**, nikdy kdy se píše. `i0004` „Non-goals" zmiňuje Gradera ve smyslu „co se neukládá" |
| `doc/intent/MAP.md`, `INDEX.json` | generované z textu uzlů; nic vlastního |
| `README.md` | dvě místa (diagram, tabulka) = místo 7. Třetí diagram (`:426-429`) a řádek `:446` už nové pořadí **potvrzují**; `:513` „Step 7 — pay down the realization debt" je adopční průvodce, ne krok běhu |
| `doc/guides/`, `img/`, `LICENSE`, `ruff.toml`, `.gitignore` | nic věcného |
| `doc/new_ideas/` | mimo rozsah rozhodnutím Humana. Pro úplnost prohledáno: **žádný** výskyt vzorců `after the Grader`, `Grader is green`, `green Grader`, `claims after`, `after a green`. Nic tam tedy neuniká, i kdyby se to čtenář rozhodl číst |
| `doc/runs/` | audit. Staré pořadí tam **je** (např. `20260816-1302-realization-layer-91/cli-evidence.md:35` cituje dnešní text hlášení), a je to správně: záznam běhu má říkat, co nástroj tehdy dělal. Nepřepisuje se — viz níž |

**Výsledek: devátý výskyt v platné metodice není.** Míst je osm; devátým kandidátem by byly
jen záznamy pod `doc/runs/`, které se z principu neopravují. Jediné, co po revizi
v `rules/`, `skills/`, `README.md` a `tools/` zůstane ze staré formulace, jsou dvě věty,
které ji **popírají** nebo správně omezují — vyjmenované v Definition of Done, položka 9.

## Rozhodnutí o `grader-evidence.md`

Coder minulého běhu (`20260817-1853-slice-and-derived-truth-66`) pojmenoval svá měření
`grader-evidence.md`, tedy jménem, které nová konvence z R5 zakazuje („never named
`grader*`"). **Nepřejmenovávat a nemazat.** Tři důvody:

1. **Je to zavřený a zacommitovaný audit.** `report.md` i `review.md` toho běhu ten soubor
   citují jménem a číslem řádku (`grader-evidence.md:38`, `:75`, `:114`). Přejmenování by
   z těch citací udělalo odkazy na neexistující soubor — audit by se stal nečitelným
   přesně v běhu, který si vysloužil tři kola recenze.
2. **Nové pravidlo je dopředné, ne retroaktivní.** Metodika popisuje, co se má psát od
   teď. Konvence, která přepisuje historii, aby si sama nekazila statistiku, je horší než
   jedna doložená nekonzistence — a ta nekonzistence je právě ten důkaz, proč R5 vzniklo.
3. **Mechanicky už je to jméno vyřazené.** Kombinace „vlastní soubor se jmenuje
   `coder-evidence.md`" + „never named `grader*`" znamená, že se příště nevyrobí. Kritik
   došel k témuž: výslovné „retire" není potřeba.

Plán proto o tom souboru **nic nemění** a Definition of Done to hlídá: diff nesmí
obsahovat žádnou cestu pod `doc/runs/` mimo adresář tohoto běhu (položka 15).

## R5 — `grader.md` je artefakt Coordinatora

Vada, kterou to opravuje: Coder v běhu `20260817-1853` napsal svoje měření do
`grader-evidence.md`, tedy do jména na jeden znak od artefaktu brány. Text proto musí
říct dvě věci zvlášť — kam měření patří (`report.md` + vlastní soubor s jasným jménem) a
co se psát nesmí (`grader.md` ani nic, co se dá za něj přečíst).

### R5-a — `skills/ice-implement/SKILL.md`, konec kroku 5

Vlož **za** poslední odstavec kroku 5 (`Step 5 — Self-check before handing over`), tedy za
řádek `claims; the Grader's log is the record.`, prázdný řádek a tento text:

```markdown
Put your own measurements in `report.md` under Evidence, and any long raw output — test
logs, mutation transcripts — in a file of your own in the run directory, named
`coder-evidence.md`. **Never write `grader.md`, and never write a file whose name can be
read as it.** `grader.md` belongs to the Coordinator, which writes it from commands it ran
itself; a gate whose log the author of the code produced is not a gate.
```

### R5-b — `skills/ice-implement/SKILL.md`, output checklist

Nahraď řádek

```markdown
- [ ] No realization claim written — that is the Coordinator's, after the Grader
```

dvěma řádky (druhý je R5, první nese i změnu z R6):

```markdown
- [ ] No realization claim written — the Coordinator's, once every gate the level requires has passed
- [ ] `grader.md` neither written nor edited; your evidence is `report.md` + `coder-evidence.md`
```

### R5-c — `rules/07-run-artifacts.mdc`, tabulka artefaktů

Aby jméno `coder-evidence.md` existovalo na jednom místě jako konvence a ne jen v jednom
skillu, nahraď dva řádky tabulky „How many files"

```markdown
| `report.md` | Coder | what was done, read, changed, decided |
| `grader.md` | Grader | machine log of `VERIFY.md` |
```

třemi:

```markdown
| `report.md` | Coder | what was done, read, changed, decided |
| `coder-evidence.md` | Coder | raw output the Coder measured; optional, never named `grader*` |
| `grader.md` | Grader = the Coordinator itself | machine log of `VERIFY.md`, never the Coder's |
```

### R5-d — `rules/07-run-artifacts.mdc`, Definition of Done, řádek 80

Nález, který požadavek nejmenuje, a je to past téhož druhu jako ta, kterou R5 opravuje:
dnešní povinná položka posílá Coderův důkaz o padajícím testu **do `grader.md`**, zatímco
`skills/ice-implement/SKILL.md` krok 3 ho posílá do `report.md`. Coder, který otevře
pravidlo a ne skill, tím dostane pokyn napsat soubor, který psát nesmí. Nahraď

```markdown
- [ ] Failing-test evidence: the new test fails on unchanged code (log in `grader.md`).
```

za

```markdown
- [ ] Failing-test evidence: the new test fails on unchanged code (`report.md`, not `grader.md`).
```

Řádek za řádek; obě sdělení (kam ano, kam ne) jsou tím na místě, kde se Definition of Done
odškrtává.

### R5-e — `skills/ice-run/SKILL.md`, krok 7 (viz R6-a)

Text kroku 7 níž nese i R5 z druhé strany: Coordinator píše `grader.md` sám a měření
Codera do něj nepatří.

## R6 — nárok až po branách, které si úroveň žádá

Devět náhrad, R6-a až R6-m, pokrývá všech osm míst z tabulky rozsahu a k tomu tři místa
v `skills/ice-review/SKILL.md`, která z nového pořadí dělají něco, co Adversář kontroluje
(R6-i, R6-j). Kanonická věta „once every gate the level requires has passed" je ve všech
osmi znak za znak stejná — přesně proto, aby se ta místa nemohla rozejít a aby to šlo
zkontrolovat jedním `grep` (Definition of Done, položka 9).

### R6-a — `skills/ice-run/SKILL.md`, krok 7

Nahraď celý blok od `Write the raw output to` po `refusal is a finding about the run, not
an obstacle to route around.` (dnes 12 řádků, řádky 90–101) tímto textem:

```markdown
Write the raw output to `grader.md` yourself, from the commands you just ran. The Coder's
own measurements stay in `report.md` and `coder-evidence.md`; a `grader.md` written by the
author of the code is not evidence.

Failures go back to the Coder — at most three rounds, then escalate. A scope violation
raises the run to `medium` and wakes the Adversary regardless of the original level.

Record no realization claim here. A green gate proves that the commands passed, not that
an enforcer reaches every place its sentence speaks about. At `medium` and `high` that
judgement comes from Step 8; at `low`, where no Adversary runs, the gates are the whole
requirement. Either way the claim belongs to Step 9.
```

### R6-b — `skills/ice-run/SKILL.md`, krok 9

Přepiš nadpis

```markdown
## Step 9 — Close
```

na

```markdown
## Step 9 — Claim, then close
```

a **za nadpis** (tedy před dnešní odstavec `Write `status.md`: final state, …`) vlož:

````markdown
Now — and not before — record the realization claim, you and never the Coder:

```bash
$TOOL realization claim <iNNNN> --evidence doc/runs/<run> --by Coordinator
```

Claim once every gate the level requires has passed: at `low` that is the green Grader, at
`medium` and `high` also an Adversary verdict of `APPROVE`. A run closing on
`REQUEST CHANGES` or on an escalation claims nothing, and `status.md` says so. There is no
`unclaim`: the fingerprints cover only the node's text, so a claim written against a diff
that was later rejected never reddens by itself.

The tool refuses a node with an open question or with an unreachable enforcer. Such a
refusal is a finding about the run, not an obstacle to route around.

````

### R6-c — `skills/ice-run/SKILL.md`, output checklist

Nahraď

```markdown
- [ ] Realization claimed for the affected node, or the reason it could not be
```

za (kanonická formulace i tady — „after the review verdict" by u `low` nešlo splnit)

```markdown
- [ ] Realization claimed in Step 9, once every gate the level requires has passed — or why not
```

### R6-d — `rules/07-realization.mdc`, tabulka „Who may write what"

Nahraď

```markdown
| `claim` | Coordinator, after the Grader is green | the **Coder** — nobody grades their own work |
```

za

```markdown
| `claim` | Coordinator, once every gate the level requires has passed — at `low` the Grader, above it the Adversary too | the **Coder** — nobody grades their own work |
```

### R6-e — `rules/07-realization.mdc`, odůvodnění pod tou tabulkou

Vlož **za** odstavec končící `in `by` is visible in the diff, which is exactly where the
Adversary and the Human look.` prázdný řádek a tento text:

```markdown
A claim written before the review is one that nobody can withdraw: the fingerprints cover
the node's **text**, so repairing a blocker in a test never reddens it, and there is no
`unclaim` command. Where a review runs, the claim waits for its verdict — `REQUEST CHANGES`
leaves the node honestly unclaimed instead of claimed and contradicted.
```

### R6-f — `rules/07-realization.mdc`, sekce „How it fits the run"

Nahraď řádek

```markdown
- **Grader** — unchanged. After `VERIFY.md` is green, the Coordinator writes the claim.
```

třemi řádky:

```markdown
- **Grader** — unchanged, and above `low` not sufficient alone. It proves the commands ran
  and passed, never that an enforcer reaches every place its sentence speaks about. That
  judgement is what a review produces, so where one runs, the claim waits for it too.
```

### R6-g — `rules/07-run-artifacts.mdc`, odstavec u Definition of Done

Nahraď

```markdown
The Coder does not tick realization: after the Grader is green, the **Coordinator** runs
`intent realization claim <iNNNN> --evidence doc/runs/<run> --by Coordinator`. A claim
written by the Coder is refused by the tool.
```

za

```markdown
Realization is not ticked by the Coder, and above `low` not by a green Grader alone either.
The **Coordinator** runs
`intent realization claim <iNNNN> --evidence doc/runs/<run> --by Coordinator` while closing
the run, once every gate the level requires has passed: at `low` the gates themselves, at
`medium` and `high` also `APPROVE` in `review.md`. A claim written by the Coder is refused
by the tool.
```

### R6-h — `rules/07-ice-workflow.mdc`, tabulka rolí

Nahraď řádek

```markdown
| **Coordinator** (parent chat) | start other roles, pick models, count loops, allocate ids, claim realization after a green Grader | write production code; grade its own output |
```

za

```markdown
| **Coordinator** (parent chat) | start other roles, pick models, count loops, allocate ids, claim realization once every gate the level requires has passed | write production code; grade its own output |
```

Řádek za řádek — soubor je `alwaysApply: true` a nesmí narůst. Bez výčtu úrovní, viz
rozhodnutí výš: „gate the level requires" je definované tabulkou Gates o čtyřicet řádků
níž v témž souboru.

### R6-i — `skills/ice-review/SKILL.md`, kontrola č. 8

Kontrola dnes předpokládá, že nárok při recenzi **existuje** („`evidence` points at this
run's `grader.md`"). Po R6 je pravda opačná a Adversář má hlídat, že se nárok nepředběhl.
Nahraď řádek

```markdown
| 8 | Is the realization claim honest? | `$TOOL realization check`; `by` is not the Coder, `evidence` points at this run's `grader.md` |
```

za

```markdown
| 8 | Did a claim jump ahead of you? | `$TOOL realization status --node <iNNNN>`: no claim may cite this run yet — it comes after your verdict |
```

### R6-j — `skills/ice-review/SKILL.md`, odstavec o závažnosti

Součást R6 i R7. Nahraď

```markdown
Severity: **blocker** = a contract is unenforced, a Definition of Done claim is false,
scope escaped, a test proves nothing, or a realization claim was signed by the author or
by an agent standing in for the Human. **Major** = correct but fragile. **Minor** = style
and naming, never a reason to block.
```

za

```markdown
Severity: **blocker** = a contract is unenforced, a Definition of Done claim is false,
scope escaped, a test proves nothing, a mutation left the suite green, or a realization
claim was signed by the author, recorded before this verdict, or signed by an agent
standing in for the Human. **Major** = correct but fragile. **Minor** = style and naming,
never a reason to block.
```

### R6-k — `README.md`, diagram „How a change happens"

Nahraď těchto sedm řádků

```
    GRADE -- red --> CODE
    GRADE -- green --> CLAIM["Coordinator records the claim<br/><code>realization claim</code>"]
    CLAIM --> ADV{"medium or high?"}
    ADV -- yes --> REV["Adversary reviews the diff<br/>APPROVE / REQUEST CHANGES"]
    ADV -- no --> CLOSE
    REV -- "REQUEST CHANGES" --> CODE
    REV -- APPROVE --> CLOSE["Close the run<br/><code>status.md</code>, ADR, Human gate"]
```

těmito sedmi:

```
    GRADE -- red --> CODE
    GRADE -- green --> ADV{"medium or high?"}
    ADV -- yes --> REV["Adversary reviews the diff<br/>APPROVE / REQUEST CHANGES"]
    ADV -- no --> CLAIM
    REV -- "REQUEST CHANGES" --> CODE
    REV -- APPROVE --> CLAIM["Coordinator records the claim<br/><code>realization claim</code>"]
    CLAIM --> CLOSE["Close the run<br/><code>status.md</code>, ADR, Human gate"]
```

### R6-l — `README.md`, tabulka „Who may write what"

Nahraď

```markdown
| `claim` | Coordinator, after the Grader is green | the **Coder** — nobody grades their own work |
```

za (znak za znak totéž znění jako v R6-d, aby se ta dvě místa nemohla rozejít)

```markdown
| `claim` | Coordinator, once every gate the level requires has passed — at `low` the Grader, above it the Adversary too | the **Coder** — nobody grades their own work |
```

### R6-m — `tools/intent/realization.py`, text hlášení ve funkci `claim`

Osmé místo. Je to **text výjimky**, ne komentář: `raise TreeError(...)` na řádcích 547–549.
Chování se nemění — mění se jen řetězec, který uživatel uvidí, když nárok podepíše Coder.
Ověřil jsem, že se na text nekotví žádný test: `test_coder_may_not_claim_its_own_work`
(`tools/intent/tests/test_realization.py:106-113`) používá `assertRaises(TreeError)`, ne
`assertRaisesRegex`, a v celém souboru `assertRaisesRegex` není. Nahraď

```python
        raise TreeError(
            "the Coder may not claim its own work; the Coordinator claims after the Grader"
        )
```

za

```python
        raise TreeError(
            "the Coder may not claim its own work; "
            "the Coordinator claims once every gate the level requires has passed"
        )
```

Hlášení nese kanonickou větu **znak za znak**, stejně jako ostatních sedm míst:
`once every gate the level requires has passed`. Žádná varianta, žádná pojmenovaná výjimka
— gramatika větu unese bez úprav. Znění z revize 2 („claims when the run closes, after
every gate the level requires") byl drift, který by `grep` na podřetězec propustil, a to je
přesně to, čemu má kanonická věta zabránit; proto DoD 9 grepuje celou větu a navíc porovnává
počet s podřetězcem.

Dva řetězcové segmenty místo jednoho jsou nutnost, ne styl: na jednom řádku by ta hláška
měla s odsazením 120 znaků a `ruff.toml` má `line-length = 100`. Takto má první segment
52 a druhý 82 znaků. Soubor roste o jeden řádek (697 → 698); `i0004` na `tools/` žádný
limit délky nemá.

## R7 — technika recenze

Umístění: nový **krok 3** v `skills/ice-review/SKILL.md` před dnešní krok „Attack the
tests specifically", protože dnešní krok 3 se ptá na testy, které běh napsal, kdežto R7
se ptá na věty kontraktu — a to je nadřazená otázka, ze které teprve plyne, které testy
mají řezat. Dnešní kroky 3 a 4 se přečíslují na 4 a 5.

Text je držený krátce a v rozkazovacím způsobu: tři numerované kroky, jedna věta o
scratch kopii, jedna věta o tom, kde vada obvykle je, a tabulka s pravidlem ukončení.
Žádný třetí odstavec odůvodnění.

Příkladová tabulka je po blokátoru B4 **schematická**: místo `slicing.py:69` a
`talks_to` je v ní `<file:line>` a popis role toho místa. Skill čte i Adversář
v cizím projektu, kde by živá jména z tohoto repozitáře byla nepravdivá — a v roli
povinného checklistu by ho odváděla od jeho vlastních kontraktů. Třetí řádek jsem přidal
schválně: dva řádky by se daly přečíst jako „dvě místa stačí", tři ukazují, že sloupec
`State` může zůstat otevřený i po enumeraci.

### R7-a — nový krok 3

Vlož **před** řádek `## Step 3 — Attack the tests specifically` tento text (a za něj
prázdný řádek, aby zůstal odstup od následujícího nadpisu):

```markdown
## Step 3 — Read each contract sentence against the code

Every contract in `slice.md` is a claim about the whole codebase, not about the diff.
Take them one sentence at a time:

1. Name every place where the sentence could be true or false — every derivation site,
   every branch, both directions of an edge, each half of an "or".
2. In each place, mutate the code so that the sentence becomes false, then run the suite.
   The test of a review is **"would this test fail if the sentence became false"**, not
   "does the suite pass" — the Grader already proved that the suite passes.
3. A place where the sentence turns false and the suite stays green is a **blocker**, even
   when the diff did not create it.

Mutate a scratch copy, never the working tree, and revert byte-exact after each mutation.

The defect is rarely where the run looked: it is the same claim repaired in one view while
it leaks in a neighbouring one, a second derivation site, or an unexercised branch.

### At the last permitted round, enumerate

Before your third verdict, list the complete set of places the sentence reaches and mark
each one closed or open:

| # | Place the sentence reaches | Mutation | Suite | State |
|---|---|---|---|---|
| 1 | `<file:line>` — first derivation site | shorten it to one step | fails as named | closed |
| 2 | `<file:line>` — the symmetric second one | the same shortening | stays green | **open** |
| 3 | `<file:line>` — the branch no test enters | make it disagree | stays green | **open** |

That table is the stopping rule: what it marks closed you may not reopen, and what it
marks open is the whole remaining demand.
```

### R7-b — přečíslování

Nahraď `## Step 3 — Attack the tests specifically` za
`## Step 4 — Attack the tests specifically` a `## Step 4 — Verdict` za
`## Step 5 — Verdict`.

### R7-c — kontrola č. 4 v tabulce osmi kontrol

Aby tabulka na novou techniku ukazovala místo aby ji duplikovala, nahraď

```markdown
| 4 | Do the new tests actually cut? | would they fail if the implementation were wrong? |
```

za

```markdown
| 4 | Do the new tests actually cut? | Step 3 — mutate the code, do not read it |
```

### R7-d — sekce „Do not"

Vlož za řádek `- Do not approve because the report is well written.` jeden řádek:

```markdown
- Do not conclude from reading. A sentence you never tried to falsify is unverified.
```

### R7-e — šablona `review.md` v kroku 5

Aby enumerace z R7-a měla v `review.md` své místo a nezávisela na tom, že si na ni
Adversář vzpomene, nahraď v šabloně uvnitř bloku ```` ```markdown ```` dva řádky

```markdown
## Minor / non-blocking
## What I verified myself
```

čtyřmi:

```markdown
## Minor / non-blocking
## Where the contract reaches   <!-- mandatory at the last permitted round -->
- <place> — <mutation> — closed | open
## What I verified myself
```

## Limity — ověřit, ne uvěřit

Limity čte `tools/checks/template_checks.py`: `ALWAYS_APPLY_LIMIT = 150`,
`SCOPED_RULE_LIMIT = 250`, `SKILL_LIMIT = 500`; počítá se `len(text.splitlines())` nad
celým souborem, tedy včetně front matteru. Aktivace se bere z front matteru:
`07-ice-workflow.mdc` má `alwaysApply: true` (limit 150), `07-realization.mdc` i
`07-run-artifacts.mdc` mají `globs` (limit 250). `README.md` ani `tools/` žádný limit
nemají — kontrola sahá jen na `rules/*.mdc` a `skills/*/SKILL.md`. Kritik uvádí pro
`ice-run` 155 řádků tam, kde mně vyšlo 154; rozdíl o jeden řádek nic nerozhoduje (limit je
500) a rozhoduje měření Coderovo, ne kterýkoli z našich dvou suchých průchodů.

| Soubor | Aktivace | Limit | Dnes | Δ | Po běhu | Rezerva |
|---|---|---|---|---|---|---|
| `rules/07-ice-workflow.mdc` | `alwaysApply` | 150 | 118 | 0 | 118 | 32 |
| `rules/07-realization.mdc` | `globs` | 250 | 148 | +7 | 155 | 95 |
| `rules/07-run-artifacts.mdc` | `globs` | 250 | 135 | +4 | 139 | 111 |
| `skills/ice-run/SKILL.md` | skill | 500 | 142 | +14 | 156 | 344 |
| `skills/ice-review/SKILL.md` | skill | 500 | 90 | +36 | 126 | 374 |
| `skills/ice-implement/SKILL.md` | skill | 500 | 101 | +7 | 108 | 392 |
| `README.md` | — | — | 652 | 0 | 652 | — |
| `tools/intent/realization.py` | — | — | 697 | +1 | 698 | — |

**Jak jsou ta čísla podložená, a co ještě není.** V revizi 1 jsem všechny náhrady nasucho
aplikoval na kopie mimo repozitář a přepočítal; tehdy vyšlo 118 / 155 / 138 / 154 / 125 /
108 / 652 a zároveň se potvrdilo, že každé `old_string` je v cíli **právě jednou**. Čísla
revize 2 jsou ta měření plus přepočtená delta pěti bloků, které revize změnila: `07-run-artifacts`
+1 (odstavec R6-g má 6 řádků místo 5), `ice-run` +2 (krok 7 o řádek delší, krok 9 o řádek
delší), `ice-review` +1 (třetí řádek příkladové tabulky), `realization.py` +1 (řetězec
rozdělený na dva segmenty kvůli `line-length = 100`). Suchý průchod revize 2 jsem
**nespustil** — shell v tomto prostředí přestal vracet výsledky. Proto to říkám na rovinu:
tato čísla jsou aritmetika nad ověřeným základem, ne nové měření, a Definition of Done
položka 7 je proto povinná: Coder je přeměří `wc -l` a odchylku zapíše. Rezervy jsou tak
velké, že ani chyba o pár řádků nikde nepřekročí limit; nejtěsnější je `07-ice-workflow.mdc`,
a tam je zásah **jeden řádek za jeden**.

Nová `old_string` v revizi 2 je jediná — blok `raise TreeError(...)` v R6-m. Ověřil jsem,
že text `may not claim its own work` je v celém `tools/` **jednou**
(`tools/intent/realization.py`), takže je záměna jednoznačná. Ostatní `old_string` jsou
znak za znak ta z revize 1.

Nic zkracovat není potřeba a nic se nezkracuje. Kdyby Coderovi vyšel jiný počet řádků než
v tabulce, řídí se limitem, ne tabulkou — a odchylku zapíše do `report.md`.

## Zkušební specifikace

Běh nepřidává kód ani test, takže „test" znamená stroj, který kontrakty `i0002` a `i0003`
vynucuje: `python3 tools/checks/template_checks.py --root .`. U osmého místa (`i0004`, `c12`)
je vynucovačem `tools/intent/tests/test_realization.py::test_coder_may_not_claim_its_own_work`.

- **Happy path** — po všech úpravách je `template_checks.py` zelený (`template contracts
  satisfied`, exit 0) a všech pět příkazů `VERIFY.md` je zelených.
- **Edge case** — `rules/07-ice-workflow.mdc` je `alwaysApply` a končí na 118 řádcích,
  tedy pod 150; `07-realization.mdc` na 155 pod 250. Doloženo výpisem `wc -l`.
- **Error case (mutace, ne úvaha)** — vynucovač musí umět tuto změnu odmítnout. Tři
  mutace, každá zvlášť, každá s reverzí a `git diff --stat` prázdným pro dotčený soubor:
  1. přidat na konec `rules/07-ice-workflow.mdc` 40 prázdných řádků → `template_checks.py`
     musí skončit exit 1 a vypsat `158 lines exceeds the alwaysApply limit of 150`
     (číslo podle skutečnosti);
  2. v `skills/ice-review/SKILL.md` rozbít relativní odkaz (např.
     `../../rules/07-realization.mdc` → `../../rules/07-realization-x.mdc`) →
     `template_checks.py` musí skončit exit 1 s `broken link:`;
  3. v `tools/intent/realization.py` obejít odmítnutí Coderova nároku
     (`by.strip().lower() == "coder"` → `== "coderx"`) → `python3 -m unittest discover
     -s tools/intent/tests -t tools` musí skončit exit 1 a padnout **právě**
     `test_coder_may_not_claim_its_own_work`.
  Mutace 3 dokazuje dvě věci naráz: že `c12` je po záměně textu hlášení dál vynucené a že
  ten test na formulaci hlášení nikdy nezávisel — tedy že R6-m je opravdu jen text.
  Všechny tři jsou důkazem, že brány, které tento běh chrání, opravdu řežou. Doslovné
  výstupy jdou do `coder-evidence.md` — a tím se konvence z R5 hned na tomto běhu použije.

## Definition of Done

Každá položka je příkaz nebo tvrzení, které umí zkontrolovat někdo jiný.

1. `python3 tools/intent/cli.py validate` → exit 0.
2. `python3 tools/intent/cli.py realization check` → exit 0.
3. `python3 -m unittest discover -s tools/intent/tests -t tools` → `OK`, exit 0, počet
   testů nezměněný (82).
4. `python3 tools/checks/template_checks.py --root .` → `template contracts satisfied`,
   exit 0.
5. `python3 tools/checks/hook_checks.py --root .` → exit 0.
6. `python3 tools/intent/cli.py scope --run doc/runs/20260817-2334-review-craft-and-claim-order-e2`
   → `scope clean`, exit 0. Změněné soubory jsou právě těch **osm** z `outputs` (plus
   adresář běhu); `git status --short` to doloží.
7. `wc -l` pro všech osm dotčených souborů. Šest z `rules/` a `skills/` musí být pod svým
   limitem; čísla v `report.md` proti tabulce výš, s vysvětlením **každé** odchylky —
   tabulka revize 2 je aritmetika, ne měření, takže tohle je první skutečné měření.
8. Mutační důkaz z „Error case": **tři** mutace (limit řádků, rozbitý odkaz, obejití
   odmítnutí Coderova nároku), u každé příkaz, exit code, hlášení, a po reverzi
   `git diff --stat <soubor>` prázdný. Doslovné výstupy v `coder-evidence.md`.
9. **Kanonická věta je všude a je znak za znak jedna.** Grepuje se **celá** věta, ne její
   podřetězec — podřetězec by propustil variantu, tedy právě ten drift, kterému se běh brání:
   `grep -rn "once every gate the level requires has passed" rules/ skills/ README.md tools/`
   → **právě osm** řádků v **sedmi** souborech: `rules/07-ice-workflow.mdc`,
   `rules/07-realization.mdc`, `rules/07-run-artifacts.mdc`, `skills/ice-run/SKILL.md`
   (dvakrát — krok 9 a checklist), `skills/ice-implement/SKILL.md`, `README.md`,
   `tools/intent/realization.py`. Kontrolní součet proti variantám:
   `grep -rn "every gate the level requires" rules/ skills/ README.md tools/ | wc -l` → **8**,
   tedy stejné číslo jako u úplné věty. Rozdíl mezi těmi dvěma čísly = počet variant, a ten
   musí být **nula**; žádná pojmenovaná výjimka v tomto běhu neexistuje.
10. **Nikde nezůstala podmínka „jen zelená brána".**
    `grep -rn "Grader is green" rules/ skills/ README.md tools/` → prázdný (exit 1).
    `grep -rn "green Grader" rules/ skills/ README.md tools/` → **právě dva** řádky, oba
    správné: `rules/07-run-artifacts.mdc` („above `low` not by a green Grader alone
    either" — popření) a `skills/ice-run/SKILL.md` krok 9 („at `low` that is the green
    Grader" — správně omezené na úroveň). Vypisuji očekávané výskyty místo predikátu
    `grep -v review`, protože ten by na popírající větě spadl — predikát nad volným textem
    je přesně vada, kterou minulý běh zapsal jako `FU2`.
11. **Výjimka pro `low` je čitelná i v izolaci.** Čtyři místa, která ji smějí vyslovit,
    ji vyslovují: `rules/07-realization.mdc` a `README.md` („at `low` the Grader, above it
    the Adversary too"), `rules/07-run-artifacts.mdc` („at `low` the gates themselves, at
    `medium` and `high` also `APPROVE`") a `skills/ice-run/SKILL.md` kroky 7 a 9. Žádné
    z osmi míst netvrdí verdikt recenze absolutně — to je ta vada, kterou revize 2 opravuje.
12. **Osmé místo v `tools/`.**
    `grep -n "claims after the Grader" tools/intent/realization.py` → prázdný;
    `python3 -m unittest discover -s tools/intent/tests -t tools` → `Ran 82 tests … OK`;
    `ruff check tools/` → `All checks passed!`; `ruff format --check tools/` → beze změny.
    `git diff -- tools/intent/realization.py` obsahuje **jen** ty tři řádky uvnitř
    `raise TreeError(...)`, žádnou změnu chování.
13. `grep -n '\$TOOL realization claim' skills/ice-run/SKILL.md` → **jeden** výskyt, na
    řádku vyšším než `grep -n "^## Step 9" skills/ice-run/SKILL.md`. Krok 7 obsahuje větu
    `Record no realization claim here.`, tedy zákaz, ne příkaz.
14. `grep -rn "grader.md" skills/ice-implement/SKILL.md` → obsahuje zákaz z R5-a i položku
    checklistu z R5-b. `grep -n "grader.md" rules/07-run-artifacts.mdc` → řádek
    o failing-test evidence už neposílá Coderův důkaz do `grader.md` (R5-d), a jméno
    `coder-evidence.md` je v tabulce artefaktů.
15. `grep -n "## Step" skills/ice-review/SKILL.md` → kroky jdou 1, 2, 3, 4, 5 bez duplikátu
    a bez děr. `grep -n "slicing.py\|talks_to" skills/ice-review/SKILL.md` → **prázdný**:
    v příkladové tabulce nezůstalo žádné živé jméno z tohoto repozitáře (B4).
16. Diff neobsahuje `doc/intent/nodes/`, `VERIFY.md`, `AGENT_MODELS.md`, a z `tools/`
    **jen** `tools/intent/realization.py`.
    `grep -rnw "unclaim" tools/` → prázdný (exit 1): žádný nový podpříkaz nevznikl.
    `grep -rnw "unclaim" rules/ skills/ README.md` → **právě dva** řádky
    (`rules/07-realization.mdc`, `skills/ice-run/SKILL.md`) a oba to slovo **popírají**
    („there is no `unclaim`"), nezavádějí. Přepínač `-w` je podstatný: bez něj se do
    výsledku připočtou tři starší výskyty slova `unclaimed`, které s příkazem nesouvisejí.
17. **Audit se nepřepisuje.** `git status --short doc/runs/` a `git diff --name-only` →
    žádná cesta pod `doc/runs/` mimo
    `doc/runs/20260817-2334-review-craft-and-claim-order-e2/`. Zejména
    `doc/runs/20260817-1853-slice-and-derived-truth-66/grader-evidence.md` zůstává
    nedotčený (viz rozhodnutí výš).
18. `report.md` podle struktury z `07-run-artifacts.mdc`, prózou v češtině, s jedním
    repo-path na odrážku.

## Co Coder nesmí

- Měnit uzly záměru, `VERIFY.md`, `AGENT_MODELS.md`, `doc/intent/_policy.yaml` ani cokoli
  v `tools/` mimo tři řádky hlášení v `tools/intent/realization.py` (R6-m).
- Přejmenovat, smazat nebo upravit **cokoli** pod `doc/runs/` mimo adresář tohoto běhu —
  ani `grader-evidence.md` minulého běhu, přestože ho nová konvence zakazuje.
- Zavádět `realization unclaim` nebo jakýkoli nový příkaz.
- Zapisovat nárok na realizaci (`realization claim`) — po R6 je to krok 9 Coordinatora.
- Psát nebo upravovat `grader.md`. Vlastní měření jdou do `coder-evidence.md` a
  `report.md`.
- Přeformulovávat texty výš „lépe". Jsou to doslovná znění; když je některé věcně špatné,
  Coder se zastaví a napíše to do `report.md` místo aby improvizoval.
