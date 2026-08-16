---
run_id: 20260816-1302-realization-layer-91
intent_ids: ["i0004"]
role: Coordinator
model: claude-opus-5-thinking-high
complexity: high
status: done
---

# Status

## Výsledek

Vrstva realizace záměru je implementovaná, otestovaná, popsaná v pravidlech i v
`README.md` a uzel `i0004` je proti tomuto běhu prohlášen za realizovaný.

| Brána | Kolo 1 | Kolo 2 | Kolo 3 |
|-------|--------|--------|--------|
| `intent validate` | 0 | 0 | 0 |
| `intent realization check` | 0 | 0 | 0 |
| `unittest` (80 testů) | 0 | 0 | 0 |
| `template_checks`, `hook_checks` | 0 | 0 | 0 |
| kontrola rozsahu | 0 | 0 | 0 |
| Kritik nad změnou záměru | REVISE | REVISE | **ACCEPT** |
| Adversář nad diffem | REQUEST CHANGES | REQUEST CHANGES | **APPROVE** |

Strojové brány byly zelené od začátku. Obě čtenářské brány zamítly dvakrát. To je hlavní
poznatek tohoto běhu: testy neuměly odhalit, že *text kontraktu slibuje víc, než jeho
test dokazuje* — na to je potřeba čtenář.

## Modely

| Role | Model | Poznámka |
|------|-------|----------|
| Coordinator | `claude-opus-5-thinking-high` | podle `AGENT_MODELS.md`, pásmo `high` |
| Planner | `claude-opus-5-thinking-high` | tentýž agent |
| Coder | `claude-opus-5-thinking-high` | **odchylka**, viz níže |
| Critic | `claude-sonnet-5-thinking-high` | **odchylka**, viz níže |
| Adversary | `claude-sonnet-5-thinking-high` | **odchylka**, viz níže |
| Grader | žádný | příkazy `VERIFY.md`, ne jazykový model |

## Odchylky od metodiky — k rozhodnutí Humana

### 1. Kritik přišel až po implementaci

`skills/intent-change/SKILL.md` říká „Only now may implementation start" — kritika změny
záměru má předcházet kódu. V tomto běhu byla implementace hotová dřív, než Kritik poprvé
vydal verdikt, protože Human zadal implementaci přímo v rodičovském okně a role se
oddělily až zpětně.

Nešlo o neškodnou formalitu. Adversář v kole 2 ukázal, že právě touhle mezerou prošla
vada v `c15`, kterou by Kritik podle vlastního kritéria z kola 1 zachytil hned. Náprava
proběhla v rámci běhu (kola 2 a 3 už Kritik viděl aktuální stav), ale pořadí zůstává
porušené a je to tady zapsané, ne zameteno.

**Rozhodnutí Humana: přijato jako jednorázová odchylka.** Náprava proběhla uvnitř běhu a
obě brány nakonec schválily aktuální stav, takže se běh kvůli pořadí neopakuje. Odchylka
se neopakuje tichým precedentem: příští běh s `change.md` má Kritika před implementací,
jinak je to nález pro Adversáře.

### 2. Rolí Codera byl model z pásma Coordinatora

Katalog přiděluje Coderovi v pásmu `high` `claude-sonnet-5-thinking-high`. Kód psal
`claude-opus-5-thinking-high`, protože Human zadal práci přímo rodičovskému oknu a Cursor
model rodičovského okna nepřepíná.

Důsledek: tvrdé omezení `adversary_differs_from_coder` vylučovalo katalogovou volbu
Adversáře v pásmu `high` (`claude-opus-5-thinking-high`), protože to je model, který psal
kód. Adversář i Kritik proto dostali `claude-sonnet-5-thinking-high` — slug, který katalog
pro tyto role zná, jen v jiném pásmu. Omezení „jiný model než Coder" mělo přednost před
pásmem, protože je v `00-model-policy.mdc` vedené jako tvrdé.

**Rozhodnutí Humana: přijato, a nadále to není odchylka.** Šetření v produktové
dokumentaci Cursoru ukázalo, že model rodičovského okna přepíná výhradně člověk v UI —
žádné API, hook ani deeplink to neumí. Katalog tedy mlčky předpokládal něco, co platforma
neumožňuje: že model každé role je výstupem katalogu. Pro role delegované na subagenty to
platí (model se předává při spuštění), pro roli, kterou hraje rodičovské okno, nikdy.

Human proto rozhodl, že jeho volba modelu v UI je **autoritativní pro roli, kterou
rodičovské okno právě hraje**, a katalog pro tu roli neplatí. Hlásit ji jako odchylku byl
chybný požadavek metodiky, ne chyba běhu. Do `00-model-policy.mdc` patří toto pravidlo:

> Model, který Human vybral v UI, je autoritativní pro roli, kterou rodičovské okno právě
> hraje. Není to výjimka z katalogu — katalog pro tu roli neplatí a nehlásí se jako
> odchylka. Role delegované na subagenty berou model z katalogu.
>
> Kolize s tvrdým omezením: ustupuje druhá role, nikdy volba Humana. Ustupuje uvnitř
> katalogu, na nejbližší pásmo, jehož slug se liší; nelíší-li se žádný, Coordinator se ptá.
>
> Chceš-li, aby Coderovi vládl katalog, musí být Coder subagent. Píše-li kód rodičovské
> okno, platí ekonomika toho okna, ne ekonomika katalogu.

Postup tohoto běhu (Adversář ustoupil do nižšího pásma, volba Humana zůstala) je s tímto
pravidlem shodný — jednalo se podle něj dřív, než bylo zapsané.

**Zápis pravidla je vlastní běh.** `00-model-policy.mdc` leží pod `.cursor/`, což je tvrdý
spouštěč složitosti `high`. Do uzavření tohoto běhu se nepropašuje.

Vedlejší zjištění téhož šetření, které si zaslouží samostatné rozhodnutí: role tohoto
repozitáře existují jako **skills, ne jako `.cursor/agents/`**. Skill běží na modelu toho,
kdo ho volá, takže „každá role na jiném modelu" dnes nezajišťuje konfigurace, ale to, že
si Coordinator vzpomene předat slug při spuštění Tasku. Strojově kontrolovatelné by to
bylo hookem `subagentStart`, který na vstupu dostává model subagenta i model rodiče.

### 3. Změna záměru a implementace v jednom běhu

Metodika je nerozděluje explicitně, ale duch pravidla je, že změna stromu se schválí dřív,
než se podle ní kóduje. Tady se to sešlo. Jako polehčující okolnost tu původně stálo, že
vrstva realizace byla prázdná, takže rozsah zastarání byl nulový.

**Ten argument míří vedle a Human ho nepřijal v této podobě.** Důvodem k oddělení změny
záměru není zastarání, ale Kritik: nad významem se má vyslovit dřív, než na něj někdo
napíše kód. Nulový rozsah zastarání o tom neříká nic.

**Rozhodnutí Humana: přijato, s kritériem do metodiky.** Změna záměru a implementace smí
sdílet jeden běh **právě tehdy, když Kritik přijal deltu dřív, než začal kód**; jinak jsou
to dva běhy. Odchylky 1 a 3 tedy nejsou nezávislé — sdílený běh je neškodný přesně tehdy,
když odchylka 1 nenastane. Tento běh je důkaz z opačné strany: Kritik neproběhl v pořadí a
stálo to kolo navíc.

Zápis kritéria patří do `07-ice-workflow.mdc` nebo `skills/intent-change/SKILL.md`, což je
opět dotyk na `.cursor/` a tedy vlastní běh složitosti `high`.

## Nálezy přijaté a vědomě nezměněné

| Nález | Kdo | Proč se nemění |
|-------|-----|----------------|
| `enforcer_problem` počítá symbol v komentáři za přítomný | Adversář | odlišit definici od zmínky vyžaduje parser pro každý jazyk; nástroj je bezzávislostní. Kompromis je od kola 3 popsaný v komentáři funkce, ne skrytý. |
| `acceptance: pending` i u uzlu, který nikdo neprohlásil | Adversář | čtvrtá hodnota by rozšířila slovník, který popisuje pravidlo i `README.md`, kvůli kosmetice. Adversář s ponecháním souhlasí, výhradu má za kosmetickou. Zapsáno jako nesouhlas, ne jako vada. |

**Rozhodnutí Humana: oba nálezy zůstávají nezměněné.** Human byl při rozhodování
seznámen i se střední cestou u `enforcer_problem`, která v původním zápisu chyběla — u
souborů `.py` vyžadovat, aby symbol stál za `def ` nebo `class `, a ostatní jazyky nechat
na hledání celého slova. Odmítl ji ve prospěch zachování dnešního chování; obě položky
tedy zůstávají jako vědomě nesené meze, ne jako dluh k opravě.

## Nálezy mimo rozsah tohoto běhu — pro Humana

Kritik na žádost prošel vlastním kritériem i sedm kontraktů, které tento běh nezaložil ani
se jich nedotkl, a našel v `c4` a `c7` tutéž vadu, jakou opravoval v `c9`, `c10` a `c15`:
text tvrdí dvě věci, jmenovaný test dokazuje jednu. U `c4` na druhou polovinu existuje
osiřelý test (`test_parent_and_child_may_overlap`), u `c7` neexistuje žádný.

Není to důvod blokovat tento běh — `git diff` potvrzuje, že se jich nedotkl.

**Rozhodnutí Humana: samostatný běh proběhne jako další v pořadí, před commitem.**

Rozsah toho běhu: rozdělit `c4` a `c7` na tvrzení, která jejich testy skutečně dokazují,
adoptovat osiřelý `test_parent_and_child_may_overlap` jako vynucovač, napsat chybějící test
na zápornou půlku `c7`, a zpřesnit pravidlo v `## Contracts` uzlu `i0004` podle Kritikova
kritéria: nerozhoduje tvar věty, ale zda obě půlky dokazuje jeden a týž test — a druhá
půlka, která je přímým logickým důsledkem první, se nedělí (`c6` a `c14` jsou ten případ).

Dva důsledky, se kterými Human rozhodoval. Rozdělení kontraktu hne otiskem `contracts`,
takže tvrzení zapsané tímto během spadne do `stale` a bude potřebovat nový důkaz — to je
očekávané chování vrstvy, ne chyba. A protože běh proběhne se **správným pořadím bran**
(Kritik nad deltou dřív, než začne kód), je zároveň dokladem, že odchylky 1 a 3 se
neopakují.

## Tvrzení o realizaci

```
intent realization claim i0004 \
  --evidence doc/runs/20260816-1302-realization-layer-91 --by Coordinator
```

Profil souhlasu je `standard` a žádný kontrakt `i0004` není `enforced_by: review`, takže
lidský souhlas se nevyžaduje a uzel je po zapsání `realized`. Zbylé čtyři uzly stromu
zůstávají `not_claimed` — to není dluh z nepozornosti, ale pravdivý výchozí stav, který
si vrstva zavedením sama o sobě vytvořila. `intent realization worklist` je od teď
seznamem, co šabloně chybí dokázat.

## Brána Humana

Složitost `high`, takže lidské posouzení bylo **povinné**, nikoli přeskočitelné.

```yaml
human_review: approved
reviewed_by: ivo
run_state: done
```

**Verdikt: schváleno.** Human prošel všech šest rozhodnutí jedno po druhém (tři odchylky,
dva nesené nálezy, následný běh na `c4`/`c7`) a jejich znění je zapsané u příslušných
sekcí výše, ne shrnuté zvlášť.

Souhlas ve vrstvě se **nezapisuje**. Profil `standard` ho pro `i0004` nevyžaduje — žádný
jeho kontrakt není `enforced_by: review` — a Human rozhodl, že podepisovat se tam, kde to
politika nežádá, by z výjimky udělalo zvyk a časem znehodnotilo podpis tam, kde na něm
záleží. Uzel je `realized` na základě tvrzení Coordinatora proti důkazu tohoto běhu.

Commit tento běh neprovedl. Podle `02-git.mdc` a explicitního přání Humana se necommituje
bez vyžádání; Human navíc rozhodl, že commit přijde až po běhu na `c4` a `c7`, aby vznikl
v jednom konzistentním stavu.
