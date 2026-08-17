# Automatizace obnovy AGENT_MODELS.md

Status: poznámka z procesu, ne specifikace.
Datum: 2026-08-17
Týká se: `AGENT_MODELS.md`, `AGENT_MODELS.explanation.md`, `doc/cursor_models/`

Ceny a schopnosti modelů se mění vlnami. Metodika ICE proto drží jen záměr
schopnosti role; slug je data. Obnova katalogu by se neměla dít tak, že jeden
LLM stáhne web a přepíše `AGENT_MODELS.md`. Má se dít jako ICE běh složitosti
`high` nad strojovým snapshotem.

---

## 1. Proč to dává smysl

- Názvy modelů nepatří do pravidel (`00-model-policy.mdc`). Katalog je data.
- Ceník se hýbe (17. 8. 2026: týdenní launch sleva 50 % u Grok 4.6, kterou
  ruční extrakt v `doc/cursor_models/cursor_models_prices.260817.md` ztratil).
- Benchmarky se hýbou a jsou díravé. Člověk nemá pokaždé skládat tabulku ručně.
- Změna `AGENT_MODELS.md` je rozhodnutí Humana a tvrdý spouštěč `high`. To se
  automatizací nesmí obejít.

Frekvence: **jednou za vlnu modelů**, ne cron každý týden. Jinak se katalog
rozhoupe a běhy přestanou být srovnatelné.

## 2. Tři vrstvy, ne jeden skript s LLM

| Vrstva | Co dělá | Proč |
|--------|---------|------|
| Strojový snapshot | stáhne ceník a vybrané benchmarky; uloží datum, surová čísla, promo poznámky | důkaz, ne názor |
| ICE běh (`high`) | Planner navrhne nový katalog proti snapshotu i proti stávajícímu souboru; Critic zkontroluje omezení | stejné brány jako u každé změny harnessu |
| Human | přijme, upraví, nebo zahodí | katalog vlastní člověk |

Mapování skóre → slug **nesmí** být čistě aritmetické. Na 17. 8. by čistá
tabulka dala Coderovi Lunu ($0,20, 93 % SWE-Verified) a ignorovala pool
Cursor Models. To je úsudek, ne výpočet.

## 3. Snapshot (stroj, ne jazykový model)

Navrhovaný výstup, stejné místo jako dnešní ruční podklady:

```
doc/cursor_models/
  cursor_models_prices.YYMMDD.md
  cursor_models_benchmark.YYMMDD.md
  cursor_models_task_slugs.YYMMDD.md   # co umí předat subagent
```

Povinné vlastnosti snapshotu:

1. **Oddělit ceník od akce.** Pole `list_price`, `promo_price`, `promo_until`.
   Návrh katalogu se opírá o ceník po akci. Dnešní extrakt u Grok 4.6 slevu
   ztratil — přesně to skript nesmí umět.
2. **Nemyslet si chybějící skóre.** `—` zůstane `—`. Žádné dopočítávání z
   příbuzné verze modelu, leda jako výslovně označený proxy se zdrojem.
3. **Allowlist zdrojů**, ne „prohledej internet“. Výchozí sada jako v
   `cursor_models_benchmark.260817.md`: vals.ai SWE-Verified, SWE-bench Pro,
   DeepPlanning, SWE-PRBench.
4. **Slugy subagentů zvlášť.** Ceník Cursoru neříká, které slugy jde předat
   Tasku. Řádek katalogu bez spustitelného slugu je přání.
5. **Fast varianty značit**, ne doporučovat. Stejná váha, jiná sazba.

Zdroj cen: [cursor.com/docs/models-and-pricing](https://cursor.com/docs/models-and-pricing).
Je to dokumentace, ne API. Parsování HTML/MD se při změně layoutu rozbije —
snapshot má uložit i surový dokument, aby šlo poznat, že parser přestal
rozumět, místo aby tiše vyplnil prázdno.

## 4. Bezpečnost

Stažený web je nedůvěryhodný obsah (`08-agent-security.mdc`). Fetch má běžet
izolovaně, zapsat soubory do `doc/cursor_models/`, a teprve **druhý krok bez
další sítě** má číst strom, katalog a navrhnout diff.

Jinak se v jednom kontextu sejde soukromý repo + cizí HTML + odchozí síť
(lethal trifecta).

## 5. ICE běh nad snapshotem

Až existuje nový snapshot:

1. Coordinator založí běh, klasifikace `high` (dotyk `AGENT_MODELS.md`).
2. Planner dostane řez: stávající `AGENT_MODELS.md`, nový snapshot, starý
   snapshot, `AGENT_MODELS.explanation.md`, omezení z `00-model-policy.mdc`.
3. Výstup Planera: navržený YAML + seznam rozhodnutí, která nejsou v číslech
   (pool vs. API dolary, kdo je čtenář kontraktů, diverzita laboratoří).
4. Critic: `critic_differs_from_planner`, `adversary_differs_from_coder`, žádný
   Fast jako default, žádná promo cena jako ceník, žádný slug mimo Task.
5. Human přijme. Commit jen na výslovné požádání.

Nekommitovat z cronu. Výstup skriptu je snapshot + (volitelně) pracovní diff,
ne nová pravda.

## 6. Co skript nemá dělat

- Přepisovat `AGENT_MODELS.md` na disku bez běhu a bez Humana.
- Dosazovat model, který umí jen rodičovské okno, ne subagent.
- Optimalizovat na jediný sloupec (SWE-Verified). ICE potřebuje plánování a
  recenzi; public review benchmarky v srpnu 2026 pokrývají katalog skoro vůbec.
- Brát included usage poolu jako časově omezenou slevu — je to konstrukce
  tarifu, má zůstat ve vysvětlení, ne ve vzorci „USD za 1M“.

## 7. Nejužší užitečná podoba (až se to bude stavět)

Skript udělá to, co se 17. 8. udělalo ručně: dvě tabulky do
`doc/cursor_models/`, plus detekci promo poznámek a seznam slugů dostupných
v Task. Mapování na role nechá ICE běhu.

Není to uzel stromu. Až se to bude programovat, nejdřív ověřit, že to
neporušuje `current` intent — katalog je v `i0001` výslovně mimo invariant
stromu — a teprve pak běh `high` na tooling.
