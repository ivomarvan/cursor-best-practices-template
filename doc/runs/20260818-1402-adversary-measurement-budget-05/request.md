---
run_id: 20260818-1402-adversary-measurement-budget-05
intent_ids: ["i0003"]
role: Coordinator
model: claude-opus-5-thinking-high
complexity: low
status: in-progress
---

# Požadavek — rozpočet měření pro Adversáře

## Co se stalo

Adversář v běhu `20260818-0853-harness-and-hooks-audit-86` měřil skoro tři hodiny:
53 kandidátů krát 6 tvarů, 29 strukturálních útoků, 13 mutací. Našel skutečnou vadu,
takže ta práce nebyla zbytečná — ale nikdo mu nedal hranici a nikdo po něm nechtěl, aby
řekl, kde přestal.

## Proč to nespravit časovým stropem

Human tuhle možnost zvážil a zamítl ji z věcného důvodu: recenze useknutá v polovině
skončí s částečným měřením, o kterém **nikdo neví, co nepokrývá**. Nedoměřená recenze,
která mlčí, vypadá v `review.md` stejně jako schvalující. To je horší než drahá recenze.

## Co se místo toho žádá

Dvě věty do `skills/ice-review/SKILL.md`, které z neomezeného hledání udělají ohraničené
hledání s přiznaným zbytkem:

1. **Rozpočet v jednotkách práce, ne v čase.** Coordinator dá Adversáři strop počtu
   měření a pořadí priorit; Adversář měří shora dolů a u stropu přestane.
2. **Povinný výčet neměřeného.** `review.md` končí seznamem toho, co Adversář
   nezměřil — ať už kvůli stropu, nebo protože na to nedosáhl. Verdikt `APPROVE` nad
   nevyčerpaným rozpočtem znamená „změřil jsem, co bylo v plánu", ne „nic víc neexistuje".

Adversář v kole 3 tenhle výčet napsal sám od sebe v sekci „co by čtenář neměl
předpokládat". Je to důkaz, že ta věc jde napsat — jen nebyla zadaná, takže ji nešlo
zkrátit ani vynutit.

Do `skills/ice-run/SKILL.md` patří druhá polovina téhož: Coordinator ten rozpočet má
**zadat**, jinak není co dodržet.

## Hranice

Tento běh nemění žádný kontrakt ani žádný uzel stromu. Sahá jen na dva soubory pod
`skills/`, tedy uvnitř `code_paths` uzlu `i0003`. Nepřidává závislost ani veřejné
rozhraní. Podle deterministických spouštěčů v `07-ice-workflow.mdc` je to `low`.

Vědomě se sem **nebalí** oprava hooku. Běh `…-0853-…` selhal mimo jiné proto, že nesl
čtyři audity, tři follow-upy a přepis hooku najednou. Hook má vlastní běh a poběží až
podle pravidla, které vznikne tady.
