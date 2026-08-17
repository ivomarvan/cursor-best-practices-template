---
run_id: 20260816-2145-contract-hygiene-cd
intent_ids: ["i0004"]
role: Coordinator
model: claude-opus-5-thinking-high
complexity: high
status: in-progress
---

# Zadání

## Odkud přišlo

Z uzavření předchozího běhu `20260816-1302-realization-layer-91`. Kritik tam na žádost
Coordinatora prošel svým kritériem i sedm kontraktů, které ten běh nezaložil, a našel ve
dvou z nich tutéž vadu, jakou se v něm tři kola opravovalo na nových kontraktech. Human to
v `status.md` uzavřel rozhodnutím, že to bude samostatný běh, a to hned následující.

## Co je špatně

Uzel `i0004` má dva kontrakty, jejichž text tvrdí dvě nezávislé věci, ale jejichž
`enforced_by` prokazuje jen jednu z nich:

| Kontrakt | Text | Co test dokazuje | Co nedokazuje nikdo |
|---|---|---|---|
| `c4` | „`code_paths` se smí překrývat jen po linii předků, **nikdy** mezi sourozenci" | zápornou půlku (`test_siblings_may_not_overlap`) | kladnou půlku — existuje na ni test `test_parent_and_child_may_overlap`, ale není `enforced_by` ničeho |
| `c7` | „path a depth existují jen v generovaných pohledech, **nikdy** v souboru uzlu" | kladnou půlku (`test_index_holds_derived_path_and_depth`) | zápornou půlku — na tu neexistuje **žádný** test |

`c7` je horší případ: u `c4` aspoň důkaz existuje a jen visí bez vazby, u `c7` chybí úplně.

## Proč na tom záleží

Kontrakt, jehož text sahá dál než jeho vynucovač, je nevynucený slib v šatech vynuceného.
Čtenář stromu vidí `enforced_by` a uzavře, že tvrzení hlídá stroj. Polovina tvrzení ale
nehlídá nic a rozbije se beze slova. Je to přesně ten druh tiché nepravdy, kvůli které
`enforced_by` vůbec existuje.

## Co má vzniknout

1. `c4` a `c7` tvrdí jen to, co dokazuje jejich test.
2. Odpojené půlky mají vlastní kontrakt a vlastní důkaz — u `c4` adopcí existujícího
   osiřelého testu, u `c7` napsáním testu, který zatím neexistuje.
3. Pravidlo v `## Contracts` uzlu `i0004` je zpřesněné podle kritéria, které Kritik
   formuloval ostřeji než Planner předchozího běhu.

## Co do zadání nepatří

- Zpřísňování validátoru. Pole `path` ve front matteru dnes končí jako varování V1
  („unknown fields") a hodnota se ignoruje. Udělat z toho chybu je samostatné rozhodnutí
  o chování nástroje, ne úklid kontraktů — a nový kontrakt musí popisovat, co nástroj
  **dělá**, ne co by se komu líbilo.
- Ostatní kontrakty. `c1`, `c2`, `c3`, `c5`, `c6` a `c8`–`c17` Kritik prošel týmž
  kritériem a neshledal nález; tento běh se jich nedotýká.
- Dvě metodická pravidla, která Human schválil při uzavírání předchozího běhu (model
  rodičovského okna, kritérium pro sdílený běh). Leží pod `.cursor/` a patří do vlastního
  běhu.
