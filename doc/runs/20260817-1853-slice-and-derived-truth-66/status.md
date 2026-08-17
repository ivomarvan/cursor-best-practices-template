---
run_id: 20260817-1853-slice-and-derived-truth-66
intent_ids: ["i0004"]
role: Coordinator
complexity: high
status: closed
verdict: APPROVE
human_gate: required
closed: 2026-08-17
---

# Závěr běhu

Tři místa, kde uzel `i0004` tvrdil víc, než jeho vynucovač dokazoval, jsou uzavřená.
Všech osm bran je zelených, Adversář dal ve třetím kole `APPROVE`, tvrzení o realizaci
`i0004` je zapsané proti tomuto běhu. Zbývá brána Humana — složitost `high` ji vyžaduje.

## Co se změnilo

| Kontrakt | Změna | Důvod |
|---|---|---|
| `c6` | nový text i vynucovač | dosavadní věta „never siblings" byla **nepravdivá** a vyvracel ji test v téže sadě |
| `c7` | text beze změny, delší dosah testu | `build_index` odvozuje hloubku na dvou místech, test sahal na jedno |
| `c19` | text beze změny, silnější nástroj | `_check_identity` četl jen `tree.nodes`, soubor v `_retired/` nikdy |

Produkční kód se změnil na **jediném** místě: `_check_identity` posílá hlášení o neznámých
polích i na `tree.retired`. `slicing.py` a `generate.py` jsou bajt za bajtem shodné s HEAD —
F1 i F2 byly opravy tvrzení a důkazů, ne chování.

Nové znění `c6`: *„A slice carries exactly these intent nodes: the node, its ancestors, its
`uses` targets and the far end of every `talks_to` edge — kinship alone adds none"*. Slovo
**exactly** je nový závazek: členství ve slice je od teď vyčerpávající, takže i vyloučení
potomků je napříště věc změny záměru, ne refaktoru. Je to zpřísnění a je v uzlu napsané.

## Role, modely, kola

| Role | Model | Kol | Výsledek |
|---|---|---|---|
| Coordinator | `claude-opus-5-thinking-high` (volba Humana v UI) | — | — |
| Planner | `claude-opus-5-thinking-high` | 1 | delta + plán |
| Critic | `cursor-grok-4.5-high` | 1 | `ACCEPT` bez blokátorů |
| Coder | `cursor-grok-4.5-high` | 3 + oprava záznamu | 4 blokátory opraveny |
| Grader | stroj (bez LLM) | 4 | 8 bran zelených |
| Adversary | `claude-opus-5-thinking-high` | 3 | `REQUEST CHANGES`, `REQUEST CHANGES`, `APPROVE` |

Katalogové sloty pro pásmo `high` dodrženy včetně omezení `adversary_differs_from_coder`
a `critic_differs_from_planner`. Coordinator běžel na modelu, který Human zvolil v UI —
podle `rules/00-model-policy.mdc` je ta volba pro roli rodičovského okna rozhodující, a
shodou okolností odpovídá i katalogu.

## Vzorec, který se v tomto běhu potvrdil počtvrté

Kritik i Adversář dostali výslovný pokyn číst větu kontraktu **proti kódu** a najít každé
místo, kterého se týká. Kritik s ním našel nulu blokátorů, Adversář čtyři — a všechny čtyři
byly týž druh vady, kvůli které běh vznikl: věta sahá dál než důkaz.

1. `c6` prokazovalo „exactly" jen na vzdálenost jedné hrany (fixtura byla hvězda).
2. Větev `for_implementation=True` test vůbec nevolal.
3. `c19` říká „path **or** depth", ale fixtura měla vždy obě.
4. Hrana `talks_to` má dvě odvozovací místa; prohloubená fixtura fixovala hranici jen u
   vlastní hrany, ne u příchozí.

Adversář si v druhém kole vypsal závaznou tabulku šesti odvozovacích míst `c6` a ve třetím
kole každé z nich zavřel vlastní mutací, včetně toho, které v druhém kole nechal jen na
členství v množině. Tabulka je v `review.md` a je to podepsaný konec sporu, ne shrnutí.

Praktický závěr pro metodiku: ten pokyn patří do `skills/ice-review/SKILL.md`, ne do
zadání, které si Coordinator musí pamatovat. Je to položka běhu B.

## Eskalace na Humana

**E1 — `realization claim` se zapisuje před nezávislou recenzí.** `skills/ice-run/SKILL.md`
krok 7 nařizuje zapsat tvrzení, jakmile je `grader.md` zelený; Adversář startuje až v kroku
8. V tomto běhu proto uzel `i0004` hlásil `realized` nepřerušeně přes dva verdikty
`REQUEST CHANGES` a čtyři blokátory. Není to teoretická vada: otisk tvrzení pokrývá jen
text uzlu, takže oprava v testech s ním nehne a nepravdivé tvrzení nikdy samo nezčervená,
a `unclaim` neexistuje — Adversář nemá jak tvrzení stáhnout. Jediná strojová podmínka
`claim`u je „vynucovače jsou dosažitelné", nikoli „vynucovač svou větu dokazuje", a přesně
ten soud vzniká až v recenzi.

Nejmenší oprava: přesunout `realization claim` z kroku 7 do kroku 9, za `review.md`.
Změna metodiky je rozhodnutí Humana. Kandidát na běh B.

Postupoval jsem podle skillu vědomě, i když jsem tu díru viděl předem: odchýlit se od
závazného pravidla uprostřed běhu by ji zakrylo místo aby ji doložilo.

## Navazující práce

Dvě položky, obě popsané v `review.md` tak, aby šly vložit do pozdějšího běhu bez
odvozování znovu. **Nejsou to úkoly, které by tento běh dlužil** — ani jednu jeho diff
nezavádí a ani jednu netvrdí za vyřešenou.

- **F1** — větev `for_implementation=True` je v testu `c6` navštívená, ale prázdná:
  `target` nemá `code_paths`, takže obě větve vrací identický `result.files`. K úniku by
  byly potřeba dvě shody zároveň, proto to Adversář nedal jako blokátor.
- **F2** — predikát testu `c19` matchuje volný text zprávy nálezu, ne jeho strukturu.

## Brána Humana

Složitost `high` — Human musí běh přijmout. K rozhodnutí jsou tři věci: nové znění `c6`
včetně závazku „potomci ve slice nejsou", eskalace **E1** o pořadí nároku a recenze, a zda
`i0004` označit jako `accepted` (dnes profil přijetí nic nevyžaduje, `acceptance: 0
required`).

Commit tohoto běhu je věc Humana; agent nekomitoval nic.
