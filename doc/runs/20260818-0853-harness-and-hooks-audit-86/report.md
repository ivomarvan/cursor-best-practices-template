---
run_id: 20260818-0853-harness-and-hooks-audit-86
intent_ids: ["i0001", "i0005", "i0003", "i0004", "i0002"]
role: Coder
model: cursor-grok-4.5-high
complexity: high
status: in-progress
---

# Report — harness and hooks audit

## Co bylo implementováno

Prodlouženy enforcery čtyř `cmd:` kontraktů (`i0001` c1/c2, `i0005` c1/c2). Hook
`commit-msg` je po round 3 **strukturovaný** (trailer block + continuation), ne
řádkový `grep`. Enforcer má **28** bajtově přesných message cases. FU-B/C/D z round 1.

### Round 2 (po REQUEST CHANGES)

- **B1:** případ `address_only_trailer`; stub `no_address_branch` = jmenná větev.
  E13 → exit 1 na `address_only_trailer`.
- **B2:** širší gramatika klíče; E14 → exit 1 na `space_before_colon`.
- **M1:** cena předpony zdokumentována; regex nezužován.

### Round 3 (B3 — skládaný trailer)

- **Struktura:** poslední odstavec oddělený prázdnou řádkou = trailer block; próza před
  ním se nesahá. Trailer = klíč + odsazené continuation; attribution se maže jako celek.
  POSIX `awk`, bez volání `git` v hooku.
- **Cases:** čtyři foldy Adversáře + `subject_only_no_trailer_block`,
  `mixed_attribution_and_legitimate_trailers`, `indented_prose_quotes_attribution`,
  `crlf_line_endings`, `made_with_space_before_colon`.
- **E15:** bez detekce bloku → exit 1 (`indented_prose_quotes_attribution`).
- **E16:** bez continuation → exit 1 (`folded_space_continuation`).
- **Nadmnožina:** drží; próza/subjekt silnější. Cena předpony beze změny.
- **Neuzavřeno:** FU-1–FU-9 z review (nejsou B3).

## Vstupy a výstupy

### Read

- `skills/ice-implement/SKILL.md`
- `doc/runs/20260818-0853-harness-and-hooks-audit-86/plan.md`
- `doc/runs/20260818-0853-harness-and-hooks-audit-86/critique.md`
- `doc/runs/20260818-0853-harness-and-hooks-audit-86/request.md`
- `doc/runs/20260818-0853-harness-and-hooks-audit-86/review.md`
- `tools/checks/template_checks.py`
- `tools/checks/hook_checks.py`
- `hooks/git/commit-msg`
- `hooks/README.md`
- `hooks.json`
- `tools/intent/tests/test_realization.py`
- `tools/intent/realization.py`
- `skills/ice-review/SKILL.md`
- `skills/ice-run/SKILL.md`
- `rules/07-run-artifacts.mdc`

### Created

- `tools/intent/tests/test_checks.py`
- `doc/runs/20260818-0853-harness-and-hooks-audit-86/coder-evidence.md`
- `doc/runs/20260818-0853-harness-and-hooks-audit-86/report.md`

### Changed

- `tools/checks/template_checks.py`
- `tools/checks/hook_checks.py`
- `hooks/git/commit-msg`
- `hooks/README.md`
- `tools/intent/tests/test_realization.py`
- `skills/ice-review/SKILL.md`
- `skills/ice-run/SKILL.md`
- `rules/07-run-artifacts.mdc`

### Not touched

- `doc/intent/nodes/`
- `doc/intent/_realization.yaml`
- `VERIFY.md`
- `AGENT_MODELS.md`
- `doc/intent/_policy.yaml`
- předchozí běhy pod `doc/runs/` (mimo tento adresář)

## Použité metody a rozhodnutí

1. **Pořadí editací.** Nejdřív opravený hook, pak enforcery, pak testy.
2. **`CASES` = bajtová rovnost.** 19 pojmenovaných případů; `expected` změřený.
3. **Stub `made_with`.** Maže `-by`, `Generated-with` a adresu, nechává `Made-with`.
4. **Stub `no_address_branch` (opraveno v round 2).** Jmenná větev nového regexu bez
   adresní alternativy; pád na `address_only_trailer` (ne na `Made-with`).
5. **FU-D a FU-C** zkopírovány verbatim z plánu.
6. **Mutace** na pracovním stromu se zálohou; hook nikdy přes `git commit`.
7. **Nadmnožina (round 2).** Arbitr: `git interpret-trailers --parse` + oba hooky na
   kandidátech včetně Adversářových B2. Mimo T12/T13 žádný `old maže / new nechává`.

### Odchylky od plánu

| Místo | Round 1 | Round 2 |
|---|---|---|
| Stub `no_address_branch` | legacy první stage (padá kvůli Made-with) | **opraveno** — skutečná jmenná větev; pád na `address_only_trailer` |
| Stub / E5 `made_with` | stub nechává jen Made-with | beze změny (stále potřeba) |
| FU-C / FU-D | verbatim | beze změny |
| Klíčová gramatika | užší než git | **opraveno** — viz finální regex |

### Finální struktura hooku (round 3)

POSIX `awk` nad souborem zprávy (CRLF → LF). Trailer block = poslední odstavec za
prázdnou řádkou, nebo celá zpráva pokud je jen z trailerů; jinak subject-only beze
změny. Attribution: klíč `-(by|with)` s hodnotou (včetně continuation) začínající
`cursor`, nebo jakýkoli trailer nesoucí `cursoragent@cursor.com` — maže se celá
skupina řádek.

### Cena předpony (M1) — popis odpovídající kódu

Jmenná větev porovnává hodnotu jako **předponu** `cursor` (case-insensitive). Maže tedy
nejen `Cursor` / `CursorAgent` / `Cursor-bot`, ale i trailery, které dnešní hook nechává:
`Reviewed-by: Cursory glance at the diff`, `Made-with: cursory care`,
`Reported-by: Cursor Smith <…>`, `Tested-with: Cursor-free toolchain`. To je záměrná cena
testu nadmnožiny (Kritik ji přijal u `Cursorina Smith`); regex se kvůli tomu nezužuje.

## Reference do kódu

| File | Lines | Summary |
|---|---|---|
| `tools/checks/template_checks.py` | 103–162 | `strip_code_blocks` → `(prose, open)`, `link_targets`, identita symlinku |
| `tools/checks/hook_checks.py` | 25–320 | `CASES`, `shipped_hooks`, `check_committed_mode`, bajtová kontrola |
| `hooks/git/commit-msg` | 8–14 | ukotvený `grep -viE` z plánu + `\|\| true` |
| `tools/intent/tests/test_checks.py` | 1–527 | `HarnessBuilder` + dosah obou enforcerů |
| `tools/intent/tests/test_realization.py` | 484–515 | `test_a_hand_written_coder_claim_is_reported` (FU-B) |
| `skills/ice-review/SKILL.md` | 47–50 | FU-C věta |
| `rules/07-run-artifacts.mdc` | 20–24 | FU-D `low` soubory |
| `skills/ice-run/SKILL.md` | 144 | FU-D checklist |

## Důkazy

Surový výstup mutací E1–E12, A3c a montáže: `coder-evidence.md`.

| Command | Result | Exit code |
|---|---|---|
| `python3 tools/intent/cli.py validate` | `5 node(s): 0 error(s), 0 warning(s)` | 0 |
| `python3 tools/intent/cli.py realization check` | `realization layer consistent (3 entry/entries)` | 0 |
| `python3 -m unittest discover -s tools/intent/tests -t tools` | `Ran 115 tests` (bylo 82) | 0 |
| `python3 tools/checks/template_checks.py --root .` | `template contracts satisfied` | 0 |
| `python3 tools/checks/hook_checks.py --root .` | `hook contracts satisfied (2 shipped hook(s), 28 message case(s); committed modes checked)` | 0 |
| `python3 tools/intent/cli.py coverage` | `contracts: 28`, `machine-enforced: 28 (100%)`, `files outside any node: 0` | 0 |
| `python3 tools/intent/cli.py scope --run doc/runs/20260818-0853-harness-and-hooks-audit-86` | `scope clean (10 declared path(s))` | 0 |
| `ruff check tools/` | All checks passed | 0 |
| `ruff format --check tools/` | 20 files already formatted | 0 |
| mount `template_checks.py --root .cursor` | `template contracts satisfied` | 0 |
| mount `hook_checks.py --root .cursor` | `… committed modes not verified …` | 0 |
| `wc -l rules/07-run-artifacts.mdc skills/ice-run/SKILL.md skills/ice-review/SKILL.md` | 143 / 156 / 135 | — |
| `git diff -- doc/intent/_realization.yaml` | prázdný | — |
| `python3 tools/intent/cli.py realization status` | i0002/i0003/i0004 `realized`; i0001/i0005 `not_claimed` | 0 |

### Mutace E1–E12 (shrnutí; plný log v `coder-evidence.md`)

| # | Exit | Co padá |
|---|---|---|
| E1 | 1 | `…second_tier…`, `…nested…` |
| E2 | 1 | `…broken_link_in_a_rule…` |
| E3 | 1 | `…unterminated_fenced_block…` |
| E4 | 1 | `…symlink_pointing_outside…` (rules i skills) |
| E5 | 1 | subTest `made_with` |
| E6 | 1 | trailer + body reflow testy |
| E7 | 1 | subTesty `pre-push`, `after-edit.sh` |
| E8 | 1 | `…committed_mode_without_the_exec_bit` |
| E9 | 1 | `…required_hook_that_is_missing` |
| E10 | 1 | `made_with`, `capitalised_key`, `body_quotes_the_address`, `attribution_only` |
| E11 | 1 | `test_a_hand_written_coder_claim_is_reported` |
| E12 | 1 | `cursor_agent_prefix`, `cursor_hyphen_bot`, `cursor_xyz` |
| E13 | 1 | smazání adresní větve → `address_only_trailer` (+ digit/underscore/dot) |
| E14 | 1 | úzká gramatika klíče → `space_before_colon` |
| E15 | 1 | bez detekce trailer bloku → `indented_prose_quotes_attribution` |
| E16 | 1 | bez continuation → `folded_space_continuation` |

Po každé mutaci reverze; sada i oba check skripty znovu zelené.

### A3c / round 2 — test nadmnožiny (HEAD vs. pracovní strom, git jako arbitr)

V `coder-evidence.md` (sekce Round 2): kandidáti včetně Adversářových B2a–B2d a M1a–M1e.
Mimo T12/T13 žádný `old maže / new nechává`. M1 řádky jsou `old nechává / new maže`
(záměrná cena předpony).

### Failing-test evidence (nové chování)

Nové testy v `test_checks.py` a FU-B test jsou dokázané mutacemi E1–E12 a E11:
bez prodloužení enforceru / bez R6 kontroly na načteném YAML by sada zůstala zelená
(E11 na `coderx` je přesně ten případ, který FU-B otevírá).

## Definition of Done

1. `validate` → exit 0, `5 node(s): 0 error(s), 0 warning(s)` — **splněno**.
2. `realization check` → exit 0 — **splněno**.
3. unittest → exit 0, **115** testů; enforcer **28** message cases — **splněno**.
4. `template_checks.py --root .` → exit 0 — **splněno**.
5. `hook_checks.py --root .` → exit 0, 2 hooky / **28** případů / committed modes — **splněno**.
6. `coverage` → 28/28/0/0 — **splněno**.
7. `scope` → `scope clean (10 declared path(s))` — **splněno**.
8. ruff check + format --check → exit 0 — **splněno**.
9. E1–E12 + A3c v `coder-evidence.md` / výše — **splněno**.
10. Montáž + mount testy v sadě — **splněno**.
11. Délky 143 / 156 / 135 — **splněno**.
12. Diff: 8 upravených souborů z `outputs` + nový `test_checks.py` + adresář běhu;
    nic pod `doc/intent/nodes/`, `VERIFY.md`, `AGENT_MODELS.md`, `_policy.yaml` — **splněno**.
13. `_realization.yaml` beze změny; nárok nechávám Coordinatorovi — **splněno**.
14. i0002/i0003/i0004 zůstávají `realized` — **splněno**.
