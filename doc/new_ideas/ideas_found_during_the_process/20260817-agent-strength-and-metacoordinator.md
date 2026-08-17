# Výběr síly agenta (low / medium / high) a MetaCoordinator

Status: poznámka z procesu, ne specifikace.
Datum: 2026-08-17
Týká se: `AGENT_MODELS.md`, `rules/00-model-policy.mdc`, `rules/07-ice-workflow.mdc`,
`skills/ice-run/SKILL.md`

Tento soubor popisuje, jak výběr modelu **dnes** funguje, a navrhuje změnu,
která by oddělila klasifikaci běhu od modelu rodičovského okna.

---

## 1. Co `low` / `medium` / `high` vůbec je

Nejsou to tři „síly myšlení“ v přepínači Cursoru. Jsou to pásma **náročnosti
běhu**. Coordinator je určí z pravidel v `07-ice-workflow.mdc`:

| Pásmo | Kdy |
|-------|-----|
| `low` | běh nemění strom záměru, drží se `code_paths` jednoho uzlu, nepřidává závislost ani veřejné rozhraní |
| `medium` | vše ostatní, co není `high` |
| `high` | aspoň jeden tvrdý spouštěč (oslabení kontraktu, `.cursor/`, CI, `VERIFY.md`, `AGENT_MODELS.md`, tajemství, migrace, mazání souborů, …) |

Z pásma plynou dvě věci naráz:

1. které **drahé brány** poběží (Kritik, Adversary, lidská brána);
2. který **slug** z `AGENT_MODELS.md` dostane každá role.

Strojové brány (`intent validate`, Grader, scope guard) běží vždy.

## 2. Kdo co dnes volí

| Rozhodnutí | Kdo |
|------------|-----|
| které slugy jsou vůbec povolené | Human (obsah `AGENT_MODELS.md`) |
| smí Coordinator sáhnout na řádek podle pásma | Human (`coordinator_may_select`, `lock`) |
| které pásmo platí pro **tento běh** | Coordinator, z náročnosti změny |
| zvednout pásmo (a tím model) | Coordinator |
| snížit pásmo | jen Human |
| výjimka mimo katalog | Human, zapsaná v souboru nebo v `status.md` |

`coordinator_may_select: true` neznamená „vyber si libovolný model“. Znamená:
Coordinator smí vzít z katalogu řádek `roles.<Role>.<pásmo_běhu>`. Při
`lock: true` bere `pinned` a pásmo ignoruje.

**Jedna klasifikace běhu platí pro všechny role.** Planner na `medium` nedostane
vlastní „medium myšlení“ — dostane přesně slug `Planner.medium`. Coordinator
ten slug předá při spuštění subagenta.

Tvrdé omezení má přednost před pásmem. Kdyby Coder i Adversary vyšli na stejný
slug, ustupuje druhá role (Adversary) na nejbližší jiný slug z katalogu; volba
Humana v rodičovském okně neustupuje.

Grader se nevolí. Je to seznam příkazů v `VERIFY.md`.

## 3. Rodičovské okno versus subagenti

Cursor si model rodičovského chatu **sám nepřepne**. Žádné API, hook ani
deeplink to v době tohoto zápisu neumí.

Důsledek, který Human už jednou rozhodl (běh `20260816-1302-realization-layer-91`):

> Model, který Human vybral v UI, je autoritativní pro roli, kterou rodičovské
> okno právě hraje. Není to výjimka z katalogu — katalog pro tu roli neplatí.
> Role delegované na subagenty berou model z katalogu.

Praktický tok dnes:

1. Human v chatu vybere slug — **to je skutečný model Coordinatora**.
2. Human zadá běh. Coordinator klasifikuje náročnost.
3. V katalogu najde doporučený slug pro `Coordinator × pásmo`.
4. Nesedí-li s UI, **má Humanovi připomenout přepnutí**.
5. Ostatní role spouští jako subagenty a slug jim předá.

Human tedy **nevybírá low/medium/high v přepínači agenta**. Vybírá model okna.
Pásmo vznikne až klasifikací běhu. Pokud Human nepřepne, Coordinator běží na
ekonomice okna, ne na ekonomice katalogu. Přesně tak v tom běhu psal kód Opus 5
místo katalogového Codera.

## 4. Návrh: MetaCoordinator (ChatCoordinator)

### Problém

Klasifikace pásma probíhá **uvnitř** Coordinatora, který už běží na nějakém
modelu. Katalogový slug Coordinatora se tím pádem uplatní jen tehdy, když
Human poslechne připomínku a přepne UI — nebo když Coordinatora nikdo v
rodičovském okně nehraje.

Chceme-li, aby katalog vládl i Coordinatorovi, musí být Coordinator subagent
spuštěný **už se správným slugem**.

### Navrhovaný řetězec

```
Rodičovské okno = MetaCoordinator (ChatCoordinator)
        │
        │  klasifikuje pásmo běhu
        │  spustí Coordinatora se slugem Coordinator.<pásmo>
        ▼
   Coordinator (subagent, úroveň 1)
        │
        ├── Planner  (úroveň 2)
        ├── Critic   (úroveň 2, medium/high)
        ├── Coder    (úroveň 2)
        └── Adversary (úroveň 2, medium/high)
```

Hloubka vnoření subagentů by byla 2. Domněnka k ověření: Cursor to povoluje.
Než se to zanese do skillu, musí existovat důkaz (krátký pokus: rodič spustí
subagenta, ten spustí dalšího, oba zapíší artefakt). Pokud platforma úroveň 2
ořeže, návrh padá, nebo se Coordinator musí vejít do rodičovského okna jako
dnes.

### Co by MetaCoordinator směl a nesměl

Smí:

- přečíst `doc/intent/MAP.md` a požadavek Humana;
- klasifikovat náročnost podle `07-ice-workflow.mdc`;
- založit adresář běhu a `request.md`;
- spustit Coordinatora s modelem z `roles.Coordinator.<pásmo>`;
- zvednout pásmo, když Coordinator nebo scope guard řekne, že je to málo —
  **novým** spuštěním Coordinatora, ne přepnutím modelu za běhu;
- skládat `status.md` po návratu.

Nesmí:

- psát produkční kód;
- schvalovat plán, kód ani recenzi;
- snižovat pásmo;
- spouštět Planera, Kritika, Codera, Adversary přímo — to zůstává
  Coordinatorovi, jinak se z MetaCoordinatora stane druhý Coordinator a
  zmizí smysl oddělení.

Model MetaCoordinatora může být levný (`composer-2.5`): jeho práce je
směrování, ne dekompozice. Riziko: levný model podhodnotí `high` jako
`medium` a Coordinator dostane slabší slug, než má. Mitigace:

- MetaCoordinator smí jen **zvedat** neurčitost (v pochybnosti `medium` nebo
  `high`);
- Coordinator po startu klasifikaci ověří a při nesouladu se vrátí s
  „raise“ místo práce;
- tvrdé spouštěče `high` (dotyk `.cursor/`, `AGENT_MODELS.md`, `VERIFY.md`,
  oslabení kontraktu) jsou deterministické — MetaCoordinator je má zkontrolovat
  seznamem cest, ne odhadem.

### Proč to stojí za zvážení

- Katalog by poprvé řídil i Coordinatora, ne jen jeho potomky.
- Human by v UI mohl nechat levný model a přesto dostat drahého Coordinatora
  jen na `high` bězích.
- Klasifikace by předcházela drahému oknu, ne naopak.

### Co ověřit dřív, než se to stane skill

1. Cursor opravdu dovolí subagentovi spustit subagenta (hloubka 2).
2. Předaný `model:` na úrovni 2 se opravdu použije, nezdědí se `inherit` z
   rodiče.
3. Artefakty (`plan.md`, `critique.md`) umí psát vnořený agent do stejného
   `doc/runs/<id>/`.
4. Kolik kontextu úroveň 2 ztratí — ICE spoléhá na souborový kontrakt, ne na
   chat mezi agenty, takže ztráta chatu by neměla vadit, ztráta přístupu k
   disku by vadila.

Až to bude ověřené, změna patří do `skills/ice-run/SKILL.md` a krátké poznámky
v `00-model-policy.mdc`. Je to spouštěč složitosti `high` (dotyk `.cursor/`).
Není to změna stromu záměru: `i0001` výslovně říká, že katalog modelů není
invariant stromu.
