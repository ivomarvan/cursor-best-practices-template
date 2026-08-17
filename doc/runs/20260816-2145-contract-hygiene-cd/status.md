---
run_id: 20260816-2145-contract-hygiene-cd
intent_ids: ["i0004"]
role: Coordinator
model: claude-opus-5-thinking-high
complexity: high
status: stopped-with-open-finding
---

# Stav běhu

## Výsledek

Běh **zastaven Humanem** po recenzi Adversáře, s jedním otevřeným blokujícím nálezem.
Nezastaven proto, že by práce byla špatná — brány jsou zelené a diff sedí na plán — ale
proto, že oprava nálezu je nová změna záměru a Human ji chce vyřídit samostatným během.

`i0004` zůstává `stale [own contracts changed; own meaning changed]`. **Žádné tvrzení o
realizaci nebylo zapsáno.** To je správný stav: uzel má nové kontrakty a jeden z nich
prokazatelně nesahá tam, kam tvrdí, takže se realizovaným prohlásit nesmí.

## Co v pracovním stromu zůstává

Změny **nejsou vráceny**. Jsou konzistentní, otestované a všechny brány nad nimi končí 0;
proti dnešnímu stavu jsou zlepšením, i když nedokončeným. Konkrétně:

| Soubor | Stav |
|---|---|
| `doc/intent/nodes/i0004-intent-tooling.md` | `c4`, `c7` přeformulované, `c18`–`c20` přidané, dva odstavce prózy přepsané |
| `tools/intent/tests/test_validate.py` | dva testy rozšířené a přejmenované, jeden nový |
| `tools/intent/tests/test_tools.py` | jeden nový test |
| `doc/intent/MAP.md`, `INDEX.json` | přegenerované |

O commitu rozhoduje Human. Dokud se nespustí navazující běh, platí, že `c7` a `c20` v uzlu
tvrdí o generovaných pohledech víc, než jejich testy dosahují — je to zapsané zde a v
`review.md`, ne přehlédnuté.

## Otevřený nález, který běh nedokončil

Adversář doložil mutací, že uzel má **dva** generované pohledy a každý si cestu počítá
vlastním voláním `tree.path_of`: `build_index` do `INDEX.json` a `render_map` do `MAP.md`.
Oba dotčené kontrakty mluví o pohledech v množném čísle, ale jejich testy sahají jen na
index. Mutace mířená na `render_map` propustila `nonsense/place` do `MAP.md`, přičemž všech
82 testů zůstalo zelených a `intent validate` vrátil 0.

Je to tatáž vada, kvůli které běh vznikl, jen přestěhovaná z „souboru uzlu" do „toho
druhého generovaného pohledu". Kritik ani Coordinator ji ve třech kolech nenašli; našel ji
až nezávislý model, který kontrakty četl proti kódu, ne proti plánu.

## Rozhodnutí Humana

### 1. Jak pokračovat — samostatný běh

Nález se nedoopraví v tomto běhu. Oprava je změna záměru a patří jí vlastní běh se
správným pořadím bran.

### 2. Zúžení `c7` — schváleno

Zúžení textu kontraktu je oslabení, a tedy věc Humana. Schváleno pro znění:

> The generated index carries a path and a depth derived from the parent chain

Podklad ověřen ve zdroji, ne převzat z recenze: `render_map` vypisuje sloupce
`Id | Path | Title | Contracts | Code`. Cestu tedy nese, **`depth` nemá vůbec**. Množné
číslo v `c7` proto není jen nedokázané, ale u poloviny věty rovnou nepravdivé a žádný test
by ho pravdivým neudělal.

Naopak `c20` se zužovat **nemá**: `MAP.md` cestu nese a agenti ho čtou jako směrovací mapu,
takže tam podvržená cesta škodí víc než v indexu. Text zůstává a rozšířit se má důkaz.
Asymetrie je záměrná — u `c7` se text srovnává s realitou, u `c20` se důkaz dotahuje k textu.

### 3. Chybějící pravidlo pro znovuotevřenou bránu — doplnit

Human potvrdil díru, kterou tento běh odhalil na sobě samém. Metodika omezuje počet kol
**téže** brány na tři, ale neříká nic o případu, kdy pozdější brána otevře dřívější:
Kritik svá tři kola řádně dojel verdiktem ACCEPT a znovu ho otevřel až nález Adversáře.
Coordinator si čtvrté kolo odůvodnil sám, což je přesně to, co si odůvodňovat nemá.

Znění k zapracování do `07-ice-workflow.mdc`:

> When a later gate reopens an earlier one, the earlier gate's round counter does not reset.
> The Coordinator may not authorise the extra round; it is an escalation to the Human, who
> either grants the round or sends the finding to a follow-up run.

## Použité modely a role

| Role | Model | Kde běžel |
|---|---|---|
| Coordinator, Planner | `claude-opus-5-thinking-high` | rodičovské okno |
| Critic | `claude-opus-5-thinking-high` | subagent, kola 1–3 |
| Coder | `claude-sonnet-5-thinking-high` | subagent |
| Grader | žádný — stroj | `VERIFY.md` |
| Adversary | `claude-opus-5-thinking-high` | subagent, jiná instance než Kritik |

Tvrdé omezení `adversary_differs_from_coder` splněno. Coder tentokrát běžel na katalogovém
modelu, ne na modelu rodičovského okna — odchylka z minulého běhu se neopakovala.

## Co běh potvrdil o metodice

Pořadí bran bylo tentokrát správné a **zaplatilo se hned**. Kritik před kódem vrátil pět
blokerů ve dvou kolech, z toho jeden vážný: první verze delty tiše rušila závazek o
překryvu `code_paths` mezi bratranci a u toho tvrdila, že se množina závazků nezmenšuje.
V minulém běhu by se tohle našlo až nad hotovým kódem.

Kritik si navíc ve druhém kole testy postavil a pustil je proti šesti mutacím, čímž našel,
že dvě mutace v plánu shazují jiný test, než plán sliboval. Bez toho by `grader.md`
obsahoval nepravdivý řádek podepřený zeleným během.

Kontrola rozsahu poprvé měřila proti čisté základně a bez `--node`, takže povolila jen
deklarované cesty. V okamžiku dokončení kódu prošla, a tentokrát to něco znamenalo.

### Nález o kontrole rozsahu samotné

Při závěrečném průchodu brána spadla, ale **žádná z odmítnutých cest nepatří tomuto běhu**:

```
AGENT_MODELS.md, AGENT_MODELS.explanation.md, doc/cursor_models/…,
doc/new_ideas/gemini3.5Flash.aktual_review…, doc/new_ideas/ideas_found_during_the_process/…,
doc/new_ideas/tmp_user_file.not_for_agents.tmp.txt
```

Jsou to soubory, které Human vytvořil ve svém editoru souběžně s během. `scope.py` čte
`git diff` proti pracovnímu stromu, takže nerozliší změnu agenta od změny člověka a ohlásí
obojí stejně — s doporučením „zvyš složitost a probuď nezávislou recenzi", které v tomto
případě nedává smysl.

Brána tedy měří „co je v pracovním stromu jinak", ne „co udělal agent". Dokud se běh a
člověk nepotkají v jednom stromu, je to totéž; jakmile se potkají, brána buď plaší, nebo
by se musela ignorovat — a ignorovaná brána je horší než žádná. Souvisí to s tím, že
`scope` nemá `--base`: bez pojmenované základny nelze říct „od tohoto commitu dál".

Zapsáno jako pozorování pro navazující práci, ne jako nález proti tomuto běhu.

## Navazující práce

| # | Co | Proč samostatně |
|---|---|---|
| 1 | Dotáhnout `c7` a `c20` na oba generované pohledy podle rozhodnutí 2 | změna záměru s vlastními branami |
| 2 | Pravidlo pro znovuotevřenou bránu podle rozhodnutí 3 | mění metodiku pod `.cursor/` |
| 3 | Model rodičovského okna má přednost před katalogem (z minulého běhu) | mění `00-model-policy.mdc` |
| 4 | Kritérium pro sdílený běh změny záměru a implementace (z minulého běhu) | mění `07-ice-workflow.mdc` |
| 5 | `scope --base <commit>`, aby brána měřila od pojmenované základny a nepletla si práci člověka s prací agenta | mění nástroj i kontrakty `i0004` |

Body 2, 3 a 4 míří do stejných souborů a nabízí se vyřídit je jedním během o metodice.
