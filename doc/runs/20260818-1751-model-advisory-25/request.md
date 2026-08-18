---
run_id: 20260818-1751-model-advisory-25
intent_ids: ["i0002"]
role: Coordinator
model: claude-opus-5-thinking-high
complexity: low
status: in-progress
---

# Požadavek — ohlásit model dřív, než se běh rozjede

## Odkud to přichází

Human zvažoval novou roli „ChatRunner": chat by volal ji, ona by zvolila složitost
a spustila Coordinatora jako subagenta se správným modelem z katalogu. Motivace je
správná — Coordinator je dnes jediná role, které katalog model vybrat nemůže, protože
agent si v Cursoru vlastní model nezvolí.

Návrh se zamítl ze tří důvodů, které stojí za zapsání, protože se k té myšlence někdo
vrátí:

1. **Viditelnost.** Vnořování v Cursoru sice funguje (hlavní chat → subagent → subagent,
   hlouběji ne), ale subagent nemá žádný dokumentovaný kanál, kterým by Humanovi průběžně
   hlásil postup; rodič vidí až závěrečné shrnutí. Přesunout Coordinatora do subagenta
   znamená, že chat po celou dobu běhu mlčí. Human si přitom stěžuje právě na to, že
   uprostřed běhu neví, co se děje.
2. **Nezdokumentovaná neznámá.** Není nikde psáno, jestli vnořený subagent smí svým
   vlastním subagentům vybírat model. Kdyby ne, celý katalog by se složil do dědění
   a přestavba by nezískala nic.
3. **Hodnota.** Role, které katalog model vybrat nemůže, je zároveň ta, u které na modelu
   záleží nejmíň. Coordinator nepíše kód a nesoudí — směruje, klasifikuje, pouští příkazy,
   zapisuje. Schopnost potřebují Planner, Critic, Coder a Adversary, a ty katalog řídí už dnes.

## Co se místo toho žádá

`rules/00-model-policy.mdc` dnes v sekci `## Cursor limitation` říká, že připomenout
Humanovi model rodičovského okna je **courtesy** — laskavost, bez určeného okamžiku a bez
určeného obsahu. Praxe ukázala, že se to tím pádem neděje: v žádném z dnešních běhů to
Coordinator neudělal, a Human se o nesouladu s katalogem dozvěděl až zpětně ze `status.md`.

Udělat z toho **povinnost s daným momentem a daným obsahem**:

- **Kdy:** ve chvíli, kdy Coordinator klasifikuje složitost běhu — tedy dřív, než spustí
  jakoukoli roli. Později už je volba modelu utracená.
- **Co:** klasifikovaná úroveň, slug, který katalog pro tu roli a tu úroveň žádá, a slug,
  na kterém rodičovské okno skutečně běží.
- **Proč:** volba Humana je podle stávajícího pravidla autoritativní. Autoritativní volba
  má být informovaná; dnes je informovaná náhodou.

Zůstává v platnosti, co už tam je: **není to hlášení odchylky.** Human smí pokračovat beze
změny a nic se tím neporušuje — katalog na roli, kterou hraje rodičovské okno, neplatí.

## Hranice

Sahá se jen na `rules/00-model-policy.mdc`, tedy dovnitř `code_paths` uzlu `i0002`. Žádný
kontrakt se nemění, strom se nehýbe, nepřidává se závislost — `low`.

Do `skills/ice-run/SKILL.md` se to **nepíše**. Skills citují pravidla, neopisují je, a
okamžik lze pojmenovat přímo v pravidle.

Změna metodiky patří vždy Humanovi; tuhle Human zvolil sám, když zamítl ChatRunnera ve
prospěch levné varianty. Tenhle běh je zápis jeho rozhodnutí.
