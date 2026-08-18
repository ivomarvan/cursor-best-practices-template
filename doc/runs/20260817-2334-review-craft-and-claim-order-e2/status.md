---
run_id: 20260817-2334-review-craft-and-claim-order-e2
intent_ids: ["i0002", "i0003", "i0004"]
role: Coordinator
complexity: high
status: closed
verdict: APPROVE
human_gate: required
closed: 2026-08-18
---

# Závěr běhu

Tři věci, na které se metodika spoléhala, že si je někdo zapamatuje, jsou napsané. Osm bran
zelených, Adversář dal ve třetím kole `APPROVE`, uzel `i0003` je nárokovaný — a poprvé
podle pravidla, které tenhle běh zavádí: až po verdiktu recenze, ne po zelené bráně.

## Co se změnilo

**R5 — `grader.md` je artefakt Coordinatora.** Coder svá měření píše do `coder-evidence.md`
a shrnutí do `report.md`. Brána, jejíž log pořídil autor kódu, není brána. Řečeno tam, kde
to Coder čte, ne jen tam, kde to čte Coordinator.

**R6 — nárok na realizaci až po recenzi.** Přesunut z kroku 7 do kroku 9. Jedna **kanonická
věta**, znak za znak stejná na osmi místech v sedmi souborech — `once every gate the level
requires has passed`. Je pravdivá na každé úrovni, protože jmenuje požadavek, ne konkrétní
bránu: u `low` žádný Adversář neběží a celý požadavek jsou brány. Ta bajtová shoda není
puntičkářství, je to jediný mechanický zámek, který na textu máme: rozejití chytí `grep`,
a Definition of Done ho porovnává se dvěma počty, aby varianta neproklouzla.

**R7 — technika recenze zapsaná do skillu.** Nový krok 3 v `skills/ice-review/SKILL.md`:
čti větu kontraktu proti kódu, pojmenuj každé místo, kterého se týká, a v každém ho mutací
zkus udělat nepravdivým. Test recenze není „projde sada", ale „spadl by tenhle test, kdyby
se ta věta stala nepravdivou" — že sada projde, dokázal už Grader. Na konci recenze se
místa vypíšou do tabulky se stavem zavřeno/otevřeno, aby smyčka měla pravidlo zastavení.

Dosud to žilo v promptu, který jsem musel napsat, a fungovalo to jen tehdy, když jsem si
vzpomněl. Teď to čte Adversář sám.

## Dvě věci, které vyšly najevo až tím, že se to napsalo

**Rozpor u `low`.** Adversář ukázal, že `_policy.yaml` vyžaduje `grader.md` v adresáři
běhu, zatímco `07-run-artifacts.mdc` dával `low` běhu jediný `run.md` — nárok na `low` tedy
strojově neprošel a kanonická věta by tam byla jen zbožné přání. Opraveno na straně
pravidla, ne politiky: z R5 plyne, že `grader.md` nemůže bydlet uvnitř `run.md`, který píše
Coder. Adversář si `low` běh **sestavil** a doložil, že nárok teď projde (`exit=0`) a bez
`grader.md` je dál odmítnutý.

**Kontrola, která se nedala provést.** Nová kontrola „nepředběhl se nárok přede mě?" nejdřív
předepisovala `realization status --node`, který `evidence` nároku nikdy netiskne — u dvou
ze tří uzlů tohoto běhu by vrátila `realized` bez ohledu na odpověď. Nahrazeno za
`git diff -- doc/intent/_realization.yaml`; vrstva je verzovaná, takže se to rozhodne očima.
Adversář to ověřil oběma směry na sestaveném protipříkladu.

## Role, modely, kola

| Role | Model | Kol | Výsledek |
|---|---|---|---|
| Coordinator | `claude-opus-5-thinking-high` (volba Humana v UI) | — | — |
| Planner | `claude-opus-5-thinking-high` | 3 | 21 doslovných náhrad, revize 3 |
| Critic | `cursor-grok-4.5-high` | 3 | `REVISE`, `REVISE`, `ACCEPT` |
| Coder | `cursor-grok-4.5-high` | 3 | blokátor + Major + 7 dalších oprav |
| Grader | stroj (bez LLM) | 3 | 8 bran zelených |
| Adversary | `claude-opus-5-thinking-high` | 3 | `REQUEST CHANGES`, `APPROVE`, `APPROVE` |

Smyčky byly plné, ale ne zbytečné: každé kolo přineslo nález, který by jinak zůstal v textu.
Kritik našel, že „nárok až po recenzi" by uvázlo `low` běh; Adversář našel, že předepsaná
kontrola se nedá provést, a pak že vlastní znění kroku 3 by osm z devíti historických
blokátorů tohoto repozitáře přeřadilo na follow-upy.

## Kolik toho zadání nevidělo

Zadání jsem psal já a jmenovalo pro R6 tři místa. Planner našel sedm, Kritik osmé
(v `tools/intent/realization.py`, text výjimky — místo, kam jsem se nedíval), a teprve pak
dvě nezávislá pátrání potvrdila, že deváté není. Stojí to za zapsání: **žádost Humana ani
Coordinatora není inventura.** Úplnost vyrábí až pátrání, které někdo jiný zkontroluje.

## Navazující práce

Tři follow-upy, všechny napsané v `review.md` tak, aby šly vložit do pozdějšího běhu bez
odvozování znovu. Ani jeden není dluh tohoto běhu.

- **FU-B** — `c12` nemá test na druhém odvozovacím místě (`realization.py:480`, hlášení `R6`
  v `check()`). Adversář doložil ručním zápisem `by: Coder` do vrstvy, že věta `c12` je
  **pravdivá v obou směrech**; chybí jen test. Zadání hotové: jeden test, uzel `i0004`,
  složitost `low`.
- **FU-C** — krok 3 se ptá „je věta nepravdivá **teď**", ale mutace vypovídá o tom, co by
  bylo. Chybí věta o tom, jak se ten predikát měří. Návrh znění je v recenzi.
- **FU-D** — checklist `ice-run` žádá `request.md` jako soubor, `07-run-artifacts.mdc` dává
  `low` běhu `request` jako sekci v `run.md`. Nejednoznačnost je starší než tento běh.

## Brána Humana

Složitost `high`. K rozhodnutí: přijetí běhu, a zda FU-B zavřít krátkým během ještě v této
fázi, nebo ho nechat jako zapsanou položku. Uzel `i0003` je nárokovaný, strom je na 60 %;
zbývají `i0001` a `i0005`.

Commit je věc Humana; agent nekomitoval nic.
