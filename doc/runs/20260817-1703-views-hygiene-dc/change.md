---
run_id: 20260817-1703-views-hygiene-dc
intent_ids: ["i0004"]
role: Planner
model: claude-opus-5-thinking-high
complexity: high
status: in-progress
---

# Změna záměru

## Nejvyšší uzel, kterého se změna dotýká

`i0004 — Intent tooling`. Mění se text `c7` a vynucovač `c20`. `i0004` nemá potomky a žádný
uzel ho neuvádí v `uses`.

## Autorizace

Zúžení `c7` je oslabení kontraktu, tedy věc Humana. **Schváleno** při zastavení běhu
`20260816-2145-contract-hygiene-cd`, zapsáno v jeho `status.md` jako rozhodnutí 2, i s
podkladem ověřeným ve zdroji. Složitost `high`.

## Změny

| Id | Před | Po | Vynucovač po změně |
|----|------|-----|---|
| `c7` | „Path and depth are derived into the generated views" | „The generated index carries a path and a depth derived from the parent chain" | `test_tools.py::test_index_holds_derived_path_and_depth` (beze změny) |
| `c20` | beze změny | beze změny | `test_tools.py::test_a_path_in_a_node_file_does_not_reach_a_generated_view` (přejmenovaný a rozšířený) |

## Proč se každá strana řeší opačně

Tohle je jádro změny a není to libovůle.

**`c7` se zužuje k realitě.** Množné číslo u něj není jen nedokázané, ale u poloviny věty
nepravdivé: `render_map` vypisuje sloupce `Id | Path | Title | Contracts | Code`, takže
`MAP.md` cestu nese, ale `depth` **nemá vůbec**. Větu „path a depth jsou v generovaných
pohledech" by o druhém pohledu nepravdivou neudělal ani sebelepší test. Text se proto
srovnává s tím, co jeho test prokazuje, a jméno testu to říká rovnou.

**`c20` se nezužuje a dotahuje se mu důkaz.** Tady je situace opačná: `MAP.md` cestu nese,
takže závazek „zapsaná cesta se do pohledu nedostane" o něm dává smysl a je porušitelný —
Adversář to předvedl. Zúžit text na index by znamenalo ten závazek odepsat, a to zrovna u
pohledu, který agenti čtou jako směrovací mapu. Přizpůsobit text slabému testu je přesně
ten tah, kvůli kterému oba běhy vznikly.

Pravidlo, které z toho plyne a které už v uzlu stojí, se tím neporušuje: kontrakt smí tvrdit
jen to, co jeho test prokazuje. Splnit se to dá dvěma směry — zúžit tvrzení, nebo rozšířit
důkaz. Zúžení je správné, když je tvrzení nepravdivé; rozšíření, když je pravdivé a jen
nedokázané.

## Rozsah zastarání

`i0004` je od předchozího běhu `stale`. Tato změna otisk `contracts` posune znovu; výsledek
je tentýž stav z téhož důvodu. Nový důkaz vzniká v tomto běhu a tvrzení o realizaci zapíše
Coordinator až po zelené bráně.
