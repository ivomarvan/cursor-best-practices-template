---
run_id: 20260817-1703-views-hygiene-dc
intent_ids: ["i0004"]
role: Planner
model: claude-opus-5-thinking-high
complexity: high
status: in-progress
outputs:
  - doc/intent/nodes/i0004-intent-tooling.md
  - tools/intent/tests/test_tools.py
  - tools/intent/tests/test_validate.py
incidental:
  - doc/intent/MAP.md
  - doc/intent/INDEX.json
  - doc/intent/_realization.yaml
---

# Plán

## Cíl

Každý kontrakt uzlu `i0004`, který mluví o generovaném pohledu, je pravdivý o každém
pohledu, o kterém mluví, a je o něm doložený. Po běhu je `i0004` realizovaný s důkazem.

## Výstupy

`doc/intent/nodes/i0004-intent-tooling.md` — nový text `c7`, nový `enforced_by` u `c20`.

`tools/intent/tests/test_tools.py` — rozšíření a přejmenování testu pro `c20`.

`tools/intent/tests/test_validate.py` — **beze změny v tomto běhu.** Deklaruje se proto, že
nese nezacommitovanou práci předchozího běhu, kterou tento běh přebírá; bez deklarace by ji
brána rozsahu ohlásila jako nedeklarovanou změnu.

## Testovací specifikace

Jediný měněný test, `test_a_path_in_a_node_file_does_not_reach_a_generated_view`:

| Co | Očekávané chování |
|----|---|
| index | uzel s `path: "nonsense/place"` ve front matteru má v `build_index` cestu z řetězce předků |
| mapa | týž uzel má v `render_map` cestu z řetězce předků a `nonsense/place` se v `MAP.md` nevyskytuje |

Obě poloviny v **jednom těle**: kontrakt mluví o generovaném pohledu obecně, takže ho
neprokáže dvojice testů, z nichž každý zná jen jeden pohled.

Tělo nesmí hledat `nonsense/place` jen jako podřetězec celého `MAP.md` — musí se opřít o
cestu uzlu na jeho řádku, jinak by test prošel i tehdy, když by se hodnota objevila jinde.

## Failing-test evidence

| Mutace | Očekávaný pád |
|---|---|
| pole `path` v `Node` plněné z front matteru + přednost v `build_index` | padne polovina o indexu |
| totéž + přednost v `render_map` místo `build_index` | padne polovina o mapě |

Druhou mutaci naměřil Adversář předchozího běhu a doložil, že pod ní zůstává všech 82 testů
zelených. Obě se po zachycení výstupu vracejí.

Pro `c7` se mutace nepíše: jeho vynucovač se nemění a jeho failing-test evidence je v
`grader.md` předchozího běhu. Mění se jen text, aby přestal tvrdit nepravdu.

## Definition of Done

- [ ] `c7` mluví o generovaném indexu a nic v uzlu netvrdí, že `MAP.md` nese `depth`
- [ ] `c20` má vynucovač, jehož tělo prokazuje obě poloviny na obou pohledech
- [ ] Žádný kontrakt neukazuje na symbol, který po přejmenování neexistuje
- [ ] Obě mutace zaznamenané v `grader.md`, každá s pádem a s návratem do zelené
- [ ] `intent validate`, `realization check`, celá testovací sada, `template_checks`,
      `hook_checks` končí 0
- [ ] `ruff check` a `ruff format --check` nad `tools/` jsou čisté
- [ ] Kontrola rozsahu končí 0 **bez** `--node`
- [ ] `i0004` je po zápisu tvrzení `realized`, podepsaný Coordinatorem, ne Coderem

## Co plán vědomě nedělá

- Nemění `generate.py`, `model.py` ani `validate.py`.
- Neřeší tři metodická pravidla ani ověření slugů — mají vlastní běh.
- Nepřidává kontrakt na to, že `MAP.md` cestu vůbec **má**. Dnes to netvrdí nikdo a tento
  běh nový závazek nezakládá; zůstat u toho je vědomé, ne přehlédnuté.
