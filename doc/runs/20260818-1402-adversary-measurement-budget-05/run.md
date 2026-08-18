---
run_id: 20260818-1402-adversary-measurement-budget-05
intent_ids: ["i0003"]
role: Coder
model: cursor-grok-4.6-medium
complexity: low
status: done
outputs: ["skills/ice-review/SKILL.md", "skills/ice-run/SKILL.md"]
incidental: []
---

# Běh — rozpočet měření pro Adversáře

## Plán

Cíl: v `skills/ice-review/SKILL.md` jednoznačně zavést (1) strop měření v jednotkách
práce a pořadí priorit, s odmítnutím časového stropu, a (2) povinný výčet toho, co
Adversář nezměřil; v `skills/ice-run/SKILL.md` Kroku 8 donutit Coordinátora ten strop
a pořadí při startu Adversáře **říct**.

Test spec (prozaická změna, bez nového testu): enforcer `template_checks.py` musí
soubory dosáhnout — dočasně rozbitý odkaz v `ice-review` dá exit 1 a jmenuje soubor;
po vrácení exit 0. `intent validate` exit 0. Obě SKILL.md pod 500 řádků.

Definition of Done: obě myšlenky v `ice-review`; Krok 8 zadává strop a pořadí;
oba enforcery zelené; počty řádků v reportu; tento `run.md`.

Mimo rozsah: hook, strom záměru, `rules/`, ostatní skilly. Procedura patří do skillů,
ne do `07-ice-workflow.mdc`.

## Report

### Co bylo implementováno

Do skillu Adversáře přibyl strop v počtech práce (ne v minutách), měření shora dolů
a zastavení u stropu, výslovné odmítnutí wall-clock limitu, povinná sekce
`What I did not measure` ve `review.md` a význam `APPROVE` nad nevyčerpaným rozpočtem.
Do Kroku 8 Coordinátora přibylo, že bez zadaného stropu a pořadí není co dodržet.

Existující tabulka „Where the contract reaches“ zůstala: to je výčet míst věty, ne
výčet neměřené práce.

### Vstupy a výstupy

#### Read

- `skills/ice-implement/SKILL.md`
- `rules/07-run-artifacts.mdc`
- `VERIFY.md`
- `doc/runs/20260818-1402-adversary-measurement-budget-05/request.md`
- `doc/runs/20260818-1402-adversary-measurement-budget-05/slice.md`
- `doc/intent/nodes/i0001-harness.md`
- `doc/intent/nodes/i0002-rules.md`
- `doc/intent/nodes/i0003-skills.md`
- `skills/ice-review/SKILL.md`
- `skills/ice-run/SKILL.md`
- `doc/runs/20260818-0853-harness-and-hooks-audit-86/review.md` (kalibrace tónu výčtu; obsah nekopírován)

#### Created

- `doc/runs/20260818-1402-adversary-measurement-budget-05/run.md`

#### Changed

- `skills/ice-review/SKILL.md`
- `skills/ice-run/SKILL.md`

#### Not touched

- `hooks/`
- `tools/`
- `rules/`
- `doc/intent/`
- ostatní soubory pod `skills/`

### Použité metody a rozhodnutí

Obě myšlenky jsou procedura role, ne standing constraint — proto skilly, ne
`07-ice-workflow.mdc`. Hustota a hlas okolního textu (krátké věty, žádné emoji,
žádné vycpávkové odrážky) zůstaly. Dočasný rozbitý odkaz byl vrácen; ve stromu
zůstává jen zamýšlená změna.

### Reference do kódu

| File | Lines | Summary |
|------|-------|---------|
| `skills/ice-review/SKILL.md` | 22–25 | strop v jednotkách práce, top-down, zákaz wall-clock |
| `skills/ice-review/SKILL.md` | 118–123 | povinný výčet neměřeného; význam `APPROVE` |
| `skills/ice-review/SKILL.md` | 141 | Do not: nestavět recenzi na čase |
| `skills/ice-run/SKILL.md` | 104–108 | Coordinator zadá strop a pořadí, jinak není co držet |

### Důkazy

Počty řádků: před `ice-review` 135, `ice-run` 156; po `ice-review` 147, `ice-run` 158
(obojí pod 500).

Dočasné selhání enforceru (odkaz `../../rules/does-not-exist.mdc` v
`skills/ice-review/SKILL.md`), pak vrácení:

```
ERROR /home/ivo/workspace/git.hub.lab.ivo/cursor-best-practices-template/skills/ice-review/SKILL.md: broken link: ../../rules/does-not-exist.mdc

1 template contract violation(s)
EXIT:1
```

Po revertu:

```
template contracts satisfied
TEMPLATE_EXIT:0

5 node(s): 0 error(s), 0 warning(s)
VALIDATE_EXIT:0
```

| Command | Result | Exit code |
|---------|--------|-----------|
| `python3 tools/checks/template_checks.py --root .` (rozbitý odkaz) | jmenuje `skills/ice-review/SKILL.md` | 1 |
| `python3 tools/checks/template_checks.py --root .` (po revertu) | satisfied | 0 |
| `python3 tools/intent/cli.py validate` | 5 nodes, 0 errors | 0 |
| `python3 tools/intent/cli.py realization check` | consistent | 0 |
| `python3 -m unittest discover -s tools/intent/tests -t tools` | 99 tests OK | 0 |
| `python3 tools/checks/hook_checks.py --root .` | satisfied | 0 |

### Definition of Done

Obě myšlenky jsou v `ice-review` jednoznačné. Krok 8 v `ice-run` strop a pořadí
skutečně zadává. Enforcer i validátor končí 0. Řádky obou skillů jsou pod 500.
`outputs` jsou jen ty dva skilly. Hook, strom a pravidla zůstaly stranou — to je
vědomý mimo-rozsah, ne opomenutí.
