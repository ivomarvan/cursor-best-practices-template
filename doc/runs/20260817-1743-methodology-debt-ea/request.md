---
run_id: 20260817-1743-methodology-debt-ea
intent_ids: ["i0002"]
role: Coordinator
model: claude-opus-5-thinking-high
complexity: high
status: in-progress
---

# Zadání

## Odkud přišlo

Ze tří běhů na uzlu `i0004`. Human v nich rozhodl tři metodické otázky, ale text metodiky
zatím žádnou z nich neříká. Rozhodnutí jsou zapsaná v `status.md` běhů
`20260816-1302-realization-layer-91` a `20260816-2145-contract-hygiene-cd`.

Dluh mezi rozhodnutím a pravidlem je nebezpečnější než chybějící rozhodnutí: příští běh
narazí na tutéž díru a bude si ji řešit znovu, protože pravidlo, které existuje jen v
záznamu jednoho běhu, není pravidlo.

## Co má vzniknout

### R1 — znovuotevřená brána nenuluje počítadlo kol

Metodika omezuje počet kol **téže** brány na tři, ale neříká nic o případu, kdy pozdější
brána otevře dřívější. Přesně to nastalo v běhu `20260816-2145`: Kritik svá tři kola dojel
verdiktem `ACCEPT`, a znovu ho otevřel až nález Adversáře. Coordinator si čtvrté kolo
odůvodnil sám, což je pravomoc, kterou nemá.

### R2 — model rodičovského okna je rozhodnutí Humana

Human vybírá model v UI a agent ho za něj přepnout nemůže. Katalog proto nemůže tu volbu
přebít pro roli, kterou rodičovské okno hraje; pro delegované subagenty platí katalog.
Věta o tom už je v `AGENT_MODELS.md`, ale ten je katalog, ne metodika — rozlišení a
omezení podle vlastní věty v tom souboru patří do `rules/00-model-policy.mdc`.

### R3 — kdy smí jeden běh měnit záměr i implementovat

Human rozhodl, že sdílený běh je přípustný jen tehdy, když Kritik přijal deltu **dřív**,
než začal kód. Bez toho vzniká to, co se stalo v běhu `20260816-1302`: kód napsaný podle
delty, kterou nikdo neposoudil, a Kritik dodaný zpětně jako razítko.

### R4 — katalog obsahuje slug, který nejde spustit

`AGENT_MODELS.md` dává na `high` Kritikovi a Coderovi `cursor-grok-4.6-high`. Ten slug
není mezi dostupnými pro delegované role; běh `20260817-1703` musel substituovat
`cursor-grok-4.5-high`. `AGENT_MODELS.explanation.md` přitom sám píše, že do katalogu jdou
jen slugy, které Coordinator umí předat subagentovi, „jinak by řádek v YAML byl přání, ne
spustitelná politika". Dnes to nekontroluje nic.

## Co do zadání nepatří

- Kontrakt na spustitelnost slugů. Zjistit, které slugy prostředí nabízí, nejde strojově z
  repozitáře; takový kontrakt by musel být `enforced_by: review`, a to je podle
  `07-realization.mdc` vždy věc Humana. Zakládat ho mimochodem v úklidovém běhu je špatně.
- Vlastnictví `AGENT_MODELS.md` stromem. `i0001` má v Non-goals výslovně „Not a model
  catalogue authority" — soubor je mimo strom **záměrně**, ne přehlédnutím.
- Nález `c6` a posílení vynucovačů z běhu `20260817-1703`. Míří do `i0004`, mají vlastní běh.
