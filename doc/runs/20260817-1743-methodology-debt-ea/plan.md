---
run_id: 20260817-1743-methodology-debt-ea
intent_ids: ["i0002"]
role: Planner
model: claude-opus-5-thinking-high
complexity: high
status: in-progress
outputs:
  - rules/07-ice-workflow.mdc
  - rules/00-model-policy.mdc
  - AGENT_MODELS.md
  - AGENT_MODELS.explanation.md
incidental: []
---

# Plán

## Cíl

Tři rozhodnutí Humana jsou v metodice napsaná tam, kde je čtenář hledá, a katalog neobsahuje
slug, který nejde spustit.

## Proč tento běh nemá `change.md`

Nemění se žádný uzel: ani kontrakty, ani `## Meaning`, ani hrany. Přibývá text v souborech,
které `i0002` už vlastní přes `code_paths: ["rules/"]`, a opravuje se hodnota v souboru,
který strom vědomě nevlastní.

Složitost je přesto `high`, protože `rules/` leží pod `.cursor/` a `AGENT_MODELS.md` je
jmenovaný tvrdý spouštěč. Kritik tedy posuzuje plán, Adversář výsledek, a Human rozhoduje
po běhu.

## Kam co patří, a proč zrovna tam

`07-ice-workflow.mdc` je **always-applied** a měří 110 řádků ze 150. Podle `i0002` je
aktivace vzácný zdroj: co je v tomto souboru, platí každý požadavek a soupeří o pozornost
s otázkou Humana. Nic se sem proto nepřidává, co se dá napsat jinde.

| Rozhodnutí | Soubor | Proč tam |
|---|---|---|
| R1 znovuotevřená brána | `07-ice-workflow.mdc`, odstavec o rolích a smyčkách | je to invariant o pořadí bran, sousedí s „Loops are bounded" a s „The Coder never starts the Adversary"; kdo počítá kola, čte právě tenhle odstavec |
| R3 sdílený běh | tamtéž | je to podmínka téhož druhu — kdo smí co spustit a kdy; oddělit ji do skillu by znamenalo, že ji Coordinator při skládání běhu nevidí |
| R2 model rodičovského okna | `00-model-policy.mdc` | ten soubor sám sebe označuje za místo, kde se definuje rozlišení a omezení; je scoped, 84 řádků z 250, takže výklad si tam může dovolit |
| R4 oprava slugů | `AGENT_MODELS.md` | katalog je hodnota, ne pravidlo |

### R4 se týká šesti buněk, ne dvou

Kritik napočítal, že `cursor-grok-4.6-high` je v katalogu **šestkrát**: Coordinator
`medium`, Planner `low` i `medium`, Critic `high`, Coder `medium` i `high`. První verze
plánu mluvila o dvou a Definition of Done přitom žádala soubor bez toho slugu — rozpor.

Náhrada se řídí jedním pravidlem, aby nešlo o šest samostatných dohadů: **pásmo pojmenovává
požadované úsilí, tak ať mu slug odpovídá.** Dostupné jsou `cursor-grok-4.6-medium` a
`cursor-grok-4.5-high`.

| Role a pásmo | Nově | Proč |
|---|---|---|
| Coordinator `medium`, Planner `low`, Planner `medium`, Coder `medium` | `cursor-grok-4.6-medium` | novější model, úsilí odpovídá pásmu |
| Critic `high`, Coder `high` | `cursor-grok-4.5-high` | v pásmu `high` má přednost vysoké úsilí před generací modelu |

Po substituci tvrdá omezení drží ve všech pásmech: `critic_differs_from_planner` (`low`
Grok 4.6 vs Sonnet 5, `medium` totéž, `high` Opus 5 vs Grok 4.5) i
`adversary_differs_from_coder` (`low` Composer vs Sonnet, `medium` Grok 4.6 vs Sonnet,
`high` Grok 4.5 vs Opus 5).

Volba mezi „novější model, nižší úsilí" a „starší model, vyšší úsilí" je úsudek o záměru
Humana, ne fakt. Katalog má `authority: Human`, takže se to zapíše do `status.md` k
přehlasování, ne jako tichý fakt.

R1 a R3 dohromady nesmí přidat víc než **8 řádků**. Když se to nevejde do dvou vět, patří
formulace přepracovat, ne rozpočet ohnout.

## Znění k zapracování

R1, do odstavce o rolích a smyčkách v `07-ice-workflow.mdc`:

> A gate reopened by a later gate in the same run continues its own round count instead of
> starting again. The Coordinator may not authorise that round; it is an escalation to the
> Human, who grants it or sends the finding to a follow-up run.

R3, tamtéž:

> One run may change intent and implement it only when the Critic accepted the intent delta
> before the Coder started. A Critic arriving afterwards reviews a decision already spent,
> which is a stamp, not a gate.

R2, do `00-model-policy.mdc`:

> The model the Human selected in the UI is authoritative for the role the parent window is
> currently playing. This is not an exception to the catalog — the catalog does not apply to
> that role, and it is not reported as a deviation. Roles delegated to subagents take their
> model from the catalog.
>
> On collision with a hard constraint the other role yields, never the Human's choice. It
> yields inside the catalog, to the nearest band whose slug differs; if no band differs, the
> Coordinator asks.
>
> For the catalog to govern the Coder, the Coder must be a subagent. When the parent window
> writes the code, the economics of that window apply, not the economics of the catalog.

Sloučení R2 se stávající sekcí `## Cursor limitation` si vyžádal Kritik, aby v pravidle
nevznikla třetí kopie téže myšlenky. Adversář pak našel, že sloučení proběhlo polohou, ne
významem: původní věta o tom, že Coordinator „reminds the Human which model to select",
četla se jako pokyn uplatnit hodnotu z katalogu, což nové odstavce popírají. Předloha pro
opravu, doplněná sem, aby změna pravidla nezůstala v záznamu bez znění:

> Reminding the Human about the parent window's model is a courtesy for a role the catalog
> does not govern, not an instruction to apply a catalog value.

Znění R1 a R3 je po kritice zpřesněné: „reopens" je svázané s **toutéž bránou v témž běhu**
a kotva u R3 je „před tím, než začal Coder", ne „před prvním řádkem kódu" — u sdíleného
běhu píše první řádky často rodičovské okno, takže původní kotva šla obejít.

Znění R2 je po kritice **rozšířené na celé rozhodnutí Humana**, jak je doslova zapsané v
`doc/runs/20260816-1302-realization-layer-91/status.md`. První verze z něj vypustila tři
věci, které nejsou ozdoba: že to **není odchylka** a nehlásí se, že ustupující role
ustupuje **uvnitř katalogu** na nejbližší pásmo s jiným slugem a jinak se Coordinator ptá,
a že katalog vládne Coderovi jen tehdy, je-li Coder subagent. Bez první věty by běh dál
hlásil odchylku, kterou Human zrušil; bez druhé by nebylo řečeno, kam se ustupuje.

## Testovací specifikace

Nevznikají nové testy a nová failing-test evidence není na co: vynucovač `i0002` je příkaz
`template_checks.py`, ne test, a rozhodnutí jsou textová. Doložit se dá jen to, že limity
platí a že se text neminul místem — obojí projde branou.

Vědomě se **nezakládá** kontrakt na spustitelnost slugů. Prostředí seznam dostupných modelů
repozitáři nenabízí, takže by šlo o `enforced_by: review`, a takový kontrakt patří Humanovi,
ne úklidovému běhu.

## Definition of Done

- [ ] R1, R2, R3 zapsané v uvedených souborech ve znění výše
- [ ] R1 a R3 dohromady přidaly nejvýše 8 řádků do always-applied pravidla
- [ ] `07-ice-workflow.mdc` má nejvýše 150 řádků, `00-model-policy.mdc` nejvýše 250
- [ ] `AGENT_MODELS.md` neobsahuje `cursor-grok-4.6-high` v žádné z šesti buněk a jeho
      tabulka kontroly omezení souhlasí s YAML nad ní, včetně pásma `low`
- [ ] `intent validate`, `realization check`, testová sada, `template_checks`,
      `hook_checks` končí 0
- [ ] Kontrola rozsahu končí 0 bez `--node`
- [ ] `i0002` a `i0004` nezůstaly `stale` kvůli tomuto běhu

## Rozšíření rozsahu o `AGENT_MODELS.explanation.md` — autorizoval Human

Adversář našel, že soubor dál doporučuje `cursor-grok-4.6-high` na čtyřech řádcích a píše,
že Grok 4.5 do katalogu nepatří — tedy opak toho, co katalog po R4 říká, přičemž katalog se
na ten soubor odkazuje jako na svůj podklad. Repozitář by tvrdil X i ne-X bez značky.

Původní hranice („je to Humanův soubor, nesaháme na něj") neplatila konzistentně:
`AGENT_MODELS.md` má `authority: Human` také a tento běh ho přepsal.

Přidat výstup do plánu po přijetí Kritikem je změna rozsahu, kterou si Coordinator podle
pravidla R1 z tohoto běhu nesmí odsouhlasit sám. Eskalováno Humanovi, **Human rozšíření
udělil** a zároveň rozhodl obě věcné otázky:

- na pásmu `high` zůstává `cursor-grok-4.5-high` — pásmo pojmenovává úsilí, a model v tomto
  běhu obstál: jako Kritik našel dva blokery, které Planner přehlédl;
- do vysvětlení jde **krátká datovaná poznámka**, ne přepis. Úvaha Humana zůstává, jak byla;
  mění se jen fakt, který v době psaní neplatil — že ten slug nejde předat subagentovi.

## Co plán vědomě nedělá
- Nedotýká se skillů. Kdyby se R3 ukázalo jako lépe umístěné v `skills/intent-change/`,
  je to nález pro Kritika, ne tichá změna rozsahu.
- Neřeší nálezy z `i0004`.
