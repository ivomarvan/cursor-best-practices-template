---
run_id: 20260816-1302-realization-layer-91
intent_ids: ["i0004"]
role: Coder
model: claude-opus-5-thinking-high
complexity: high
status: done
---

# Report

## Co bylo implementováno

Vrstva realizace záměru: mechanismus, který ke stromu záměru přidává druhou vrstvu pravdy
— nikoli *co systém znamená*, ale *zda to projekt už naplňuje*.

Jádrem je jedno rozhodnutí, ze kterého plyne všechno ostatní: **ukládají se jen tvrzení,
stav se počítá.** Do `doc/intent/_realization.yaml` se zapíše, že někdo prohlásil uzel za
realizovaný, s odkazem na důkaz a se dvěma otisky znění, proti kterému to prohlásil.
Jestli tvrzení pořád platí, proč přestalo platit, co je zablokované a co dělat dál — to
se odvozuje při čtení. Nekonzistentní kombinace (realizovaný potomek pod předkem, jehož
význam se pohnul) se proto nedá uložit a nemusí ji žádné pravidlo zakazovat.

Osm podpříkazů `intent realization`, nové pravidlo metodiky, úpravy čtyř skills, oddíl
v `README.md` a deset nových kontraktů uzlu `i0004` (`c8`–`c17`) s vlastními testy.

## Vstupy a výstupy

### Přečteno

- `doc/runs/20260816-1302-realization-layer-91/slice.md`
- `doc/intent/nodes/i0001-harness.md`
- `doc/intent/nodes/i0004-intent-tooling.md`
- `tools/intent/model.py`
- `tools/intent/miniyaml.py`
- `tools/intent/validate.py`
- `tools/intent/slicing.py`
- `tools/intent/scope.py`
- `tools/intent/main.py`
- `tools/intent/tests/helpers.py`
- `tools/intent/tests/test_tools.py`
- `tools/intent/tests/test_validate.py`
- `tools/checks/template_checks.py`
- `doc/new_ideas/intent-realization.Opus5.md`
- `doc/new_ideas/intent-realization-status.critique-Opus5.md`
- `rules/07-ice-workflow.mdc`
- `rules/07-intent-tree.mdc`
- `rules/07-run-artifacts.mdc`
- `rules/00-model-policy.mdc`
- `AGENT_MODELS.md`
- `VERIFY.md`
- `README.md`

### Vytvořeno

- `tools/intent/realization.py`
- `tools/intent/tests/test_realization.py`
- `rules/07-realization.mdc`
- `doc/intent/_policy.yaml`
- `doc/intent/_realization.yaml`

### Změněno

- `tools/intent/main.py`
- `tools/intent/model.py`
- `tools/intent/scope.py`
- `tools/intent/slicing.py`
- `tools/intent/validate.py`
- `doc/intent/nodes/i0004-intent-tooling.md`
- `rules/07-ice-workflow.mdc`
- `rules/07-intent-tree.mdc`
- `rules/07-run-artifacts.mdc`
- `skills/ice-run/SKILL.md`
- `skills/ice-implement/SKILL.md`
- `skills/ice-review/SKILL.md`
- `skills/intent-change/SKILL.md`
- `VERIFY.md`
- `README.md`
- `doc/new_ideas/intent-realization.Opus5.md`
- `doc/new_ideas/intent-realization-status.critique-Opus5.md`

### Nedotčeno

- `doc/intent/nodes/i0001-harness.md`
- `doc/intent/nodes/i0002-rules.md`
- `doc/intent/nodes/i0003-skills.md`
- `doc/intent/nodes/i0005-git-hooks.md`
- `doc/intent/_registry.yaml`
- `tools/intent/miniyaml.py`
- `tools/intent/coverage.py`
- `tools/intent/generate.py`
- `tools/checks/template_checks.py`
- `tools/checks/hook_checks.py`
- `AGENT_MODELS.md`

## Použité metody a rozhodnutí

**Otisky místo příznaků.** Zastarání se nepočítá z časových razítek ani z příznaku
`dirty`, ale z porovnání dvou SHA-256 otisků. `contracts` pokrývá seznam kontraktů
seřazený podle id; `meaning` pokrývá sekce `## Refines`, `## Meaning`, `## Contracts`,
`## Non-goals` plus `parent` a `uses`. Ven zůstaly `slug`, `title`, `status`,
`code_paths`, `test_paths`, `talks_to` a otevřené otázky — přejmenovat uzel nebo přesunout
jeho soubory není změna toho, k čemu se zavazuje.

**Šíří se text, nikdy stav.** Uzel, kterému se pohnul otisk, otevře celý svůj podstrom a
(u kontraktů) své přímé spotřebitele po hraně `uses`, jeden krok. Uzel, který je jen
nedokázaný, nešíří nic. Alternativa zní přísněji, ale obrací zavádění: po startu není
prokázáno nic nikde, takže prvním uzlem k dokázání by byl kořen — v každém stromě ten
nejhůř dokazatelný. Rozhodnutí je zapsané jako kontrakt `c9` a doložené v `grader.md`
tím, že pod zamítnutou variantou padne jedenáct testů.

**Uniformní pravidlo i pro uzly bez kontraktů.** Schválený koncept počítal s tím, že
čistě strukturální uzel je realizovaný, když jsou realizované jeho děti. Při implementaci
se ukázalo, že tím vzniká díra: takový uzel by nikdy neměl tvrzení, tedy ani otisk, a
přepis jeho `## Meaning` by se neměl od čeho odrazit — děti by zůstaly `realized`. To je
přesně ta nekonzistence, kterou má vrstva vylučovat. Pravidlo je proto jednotné a oba
koncepční dokumenty jsou opravené včetně zdůvodnění.

**Sdílená kontrola vynucovače.** `enforcer_problem` je vytažená z `validate.py` a používá
ji jak pravidlo V5, tak odvozený stav `broken`. „Test byl přejmenován pryč" je jeden fakt
a má mít jednu implementaci. Po nálezu Adversáře porovnává celý symbol, ne podřetězec.

**Kontrola rozsahu.** `doc/intent/_realization.yaml` je vždy povolený výstup. Bez toho by
každý běh shodil vlastní bránu v okamžiku, kdy zapíše svůj výsledek — a zápis do vrstvy
není změna záměru, takže nemá zvedat složitost ani budit Adversáře.

**Co se vědomě neukládá.** Aktuální zelenost buildu. Ta se mění s každým commitem a strom
záměru není nástěnka CI; `broken` znamená „vynucovač neexistuje", což je trvalá vlastnost.
Přibylo to jako non-goal do `i0004`.

## Reference do kódu

| Soubor | Řádky | Shrnutí |
|--------|-------|---------|
| `tools/intent/realization.py` | 1–696 | celá vrstva: otisky, uložený tvar, odvozené stavy, worklist, kontroly R1–R7, zápisové operace, vykreslení |
| `tools/intent/realization.py` | 76–105 | kanonizace otisků — co do nich vstupuje a co vědomě ne |
| `tools/intent/realization.py` | 300–380 | `compute_states`: jediné místo, kde vzniká `stale`, `broken`, `rejected`, `blocked_by` |
| `tools/intent/realization.py` | 452–520 | `check_layer`: R1–R7 nad uloženou vrstvou |
| `tools/intent/main.py` | 216–330 | osm podpříkazů `realization` a jejich argumenty |
| `tools/intent/validate.py` | 129–152 | `enforcer_problem` sdílená mezi V5 a stavem `broken`, se shodou na celý symbol |
| `tools/intent/scope.py` | 20–24, 85–99 | trvale povolená cesta a oddělený výpočet povolených cest |
| `tools/intent/slicing.py` | 89–95, 100 | stav realizace v hlavičce řezu |
| `tools/intent/tests/test_realization.py` | 1–497 | 35 testů v 11 třídách |
| `rules/07-realization.mdc` | 1–148 | metodická část: dvě vrstvy pravdy, kdo co smí zapsat, politika |

## Důkazy

| Příkaz | Výsledek | Exit code |
|--------|----------|-----------|
| `python3 tools/intent/cli.py validate` | 5 uzlů, 0 chyb, 0 varování | 0 |
| `python3 tools/intent/cli.py realization check` | vrstva konzistentní | 0 |
| `python3 -m unittest discover -s tools/intent/tests -t tools` | 80 testů | 0 |
| `python3 tools/checks/template_checks.py --root .` | kontrakty šablony splněny | 0 |
| `python3 tools/checks/hook_checks.py --root .` | kontrakty hooků splněny | 0 |
| `python3 tools/intent/cli.py scope --run <run> --node i0004` | 30 deklarovaných cest, čisté | 0 |
| `ruff check tools/` a `ruff format --check tools/` | čisté | 0 |
| Sada pod zamítnutým pravidlem šíření | 11 pádů | 1 |
| Sada pod původní podřetězcovou shodou vynucovače | 1 pád | 1 |

Čísla v této tabulce jsou tvrzení; záznam je `grader.md`. Přepis zápisových příkazů přes
CLI je v `cli-evidence.md` — jednotkové testy volají funkce přímo, takže vrstvu argparse
neprokazují.

## Definition of Done

Splněno všech deset bodů plánu. Dva body byly splněny až ve druhém kole, po nálezech
obou recenzních bran: důkaz o padajících testech pro nově přidaný kontrakt `c16` a přepis
CLI, který do té doby existoval jen v terminálu a ne v artefaktech běhu. Ani jeden z nich
nebyl odškrtnutý dřív, než k němu vznikl artefakt.
