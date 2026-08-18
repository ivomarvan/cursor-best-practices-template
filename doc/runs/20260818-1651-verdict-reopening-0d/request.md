---
run_id: 20260818-1651-verdict-reopening-0d
intent_ids: ["i0002"]
role: Coordinator
model: claude-opus-5-thinking-high
complexity: low
status: in-progress
---

# Požadavek — kdo smí znovu otevřít uzavřený verdikt

## Co se stalo

V běhu `20260818-1414-commit-msg-block-boundary-4f` dal Adversář po prvním kole `APPROVE`
bez blokátorů a k tomu jednu pojmenovanou výhradu: follow-up FU-A, tvar, který git sám
nikdy nevyrobí. Výslovně napsal, že nárok neblokuje.

Coordinator si přesto vyžádal další kolo, aby ta výhrada z podpisu zmizela. Oprava,
která v něm vznikla, zavedla heuristiku porazitelnou obyčejným diffem a znovu otevřela
tvar, který byl v prvním kole prokazatelně mrtvý. Kolo 2 se muselo celé vrátit.

Čistá bilance: doložený stav se vyměnil za nedoložený, spotřebovala se dvě ze tří kol,
a skončilo se tam, kde se začalo — kvůli nálezu, o kterém recenzent řekl, že nevadí.

## Proč je to mezera v metodice, ne jen chyba

Metodika dnes počítá rounds jako strop **selhání**: po třetím `REVISE` nebo
`REQUEST CHANGES` se eskaluje. Nemá ale nic o tom, co se smí dít po **úspěchu**.
`APPROVE` s pojmenovanou výhradou vypadá jako pozvánka k doladění, a Coordinator ji tak
přečetl. Přitom je to uzavřený verdikt: recenzent už zvážil, co výhrada stojí, a rozhodl,
že za otevření nestojí.

Rozhodnutí „vyměním prokázaný stav za lepší, ale neprokázaný" je rozhodnutí o riziku.
Metodika takové rozhodnutí jinde důsledně dává Humanovi — snížení složitosti, oslabení
kontraktu, povolení dalšího kola po vyčerpání. Tohle do stejné rodiny patří a chybí tam.

## Co se žádá

Jedna věta, případně dvě, do `rules/07-ice-workflow.mdc`. Podstata:

Verdikt `APPROVE` nebo `ACCEPT` je uzavřený, včetně follow-upů, které v něm recenzent
označil za neblokující. Znovu ho otevřít kvůli takovému nálezu smí jen Human; Coordinator
buď nález zapíše jako známý limit a běh uzavře, nebo se zeptá. Blokátor je jiná věc —
ten uzavřený verdikt nikdy nebyl.

Umístění nechávám na Coderovi. Nabízí se sekce `Gates` (kde se dnes počítají kola) nebo
`Always the Human` (kde už jsou ostatní rozhodnutí o riziku). Druhá varianta mi přijde
věcnější, protože to je právě takové rozhodnutí — ale ať se rozhodne ten, kdo to pravidlo
čte v kontextu celého souboru.

## Hranice

Sahá se jen na `rules/07-ice-workflow.mdc`, tedy dovnitř `code_paths` uzlu `i0002`. Žádný
kontrakt se nemění, žádný uzel stromu se nehýbe, nepřidává se závislost. Podle
deterministických spouštěčů je to `low`.

Změna metodiky patří podle `07-ice-workflow.mdc` vždy Humanovi. Human ji schválil, když
mu Coordinator kolo 2 přiznal a nabídl tři varianty; tenhle běh je zápis jeho rozhodnutí,
ne návrh.
