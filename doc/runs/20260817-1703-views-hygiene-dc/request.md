---
run_id: 20260817-1703-views-hygiene-dc
intent_ids: ["i0004"]
role: Coordinator
model: claude-opus-5-thinking-high
complexity: high
status: in-progress
---

# Zadání

## Odkud přišlo

Z běhu `20260816-2145-contract-hygiene-cd`, který Human zastavil po recenzi Adversáře s
jedním otevřeným blokujícím nálezem. Rozhodnutí a podklady jsou v jeho `status.md`.

## Nález, který se má uzavřít

Uzel `i0004` má **dva** generované pohledy a každý si cestu počítá vlastním voláním
`tree.path_of`: `build_index` píše `INDEX.json` a `render_map` píše `MAP.md`. Dva kontrakty
o nich mluví v množném čísle, ale jejich testy sahají jen na index.

Adversář to doložil mutací, ne úvahou: dvoubodová mutace mířená na `render_map` propustila
`nonsense/place` do `MAP.md`, zatímco všech 82 testů zůstalo zelených a `intent validate`
vrátil 0.

Je to tatáž vada, kterou předchozí běh uklízel u `c4` a `c7` — jen přestěhovaná ze „souboru
uzlu" do „toho druhého generovaného pohledu".

## Co má vzniknout

1. `c7` mluví o generovaném indexu, protože o druhém pohledu je jeho věta rovnou nepravdivá
   — `MAP.md` sloupec `depth` nemá.
2. `c20` si text nechává a dostává důkaz na **oba** pohledy.
3. `i0004` je poprvé od změny kontraktů znovu prokazatelně realizovaný.

## Vztah k nezacommitované práci v pracovním stromě

Předchozí běh nechal svoje výstupy nezacommitované, protože je Human nechtěl uzavírat s
otevřeným nálezem. Tento běh je **přebírá jako své vlastní výstupy** a deklaruje je v
`plan.md`. Uzavře se to jedním commitem, který ponese celou opravu — hotovou i dodělanou.

Praktický důvod je v `scope.py`: brána čte `git diff` proti pracovnímu stromu, takže
nedeklarovaná cizí změna by ji shodila bez ohledu na to, kdo ji udělal.

## Co do zadání nepatří

- Změna chování nástroje. `render_map` ani `build_index` se nemění; běh popisuje, co dělají.
- Tři metodická pravidla čekající na vlastní běh (znovuotevřená brána, model rodičovského
  okna do `00-model-policy.mdc`, kritérium pro sdílený běh) a ověření slugů v katalogu.
- `scope --base`, zapsané v předchozím běhu jako pozorování.
