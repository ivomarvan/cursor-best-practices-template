---
run_id: 20260818-1414-commit-msg-block-boundary-4f
intent_ids: ["i0005", "i0004"]
role: Coordinator
model: claude-opus-5-thinking-high
complexity: high
status: in-progress
---

# Požadavek — kde leží trailerový blok

## Odkud to přichází

Běh `20260818-0853-harness-and-hooks-audit-86` přestavěl `commit-msg` hook z řádkového
grepu na strukturu nad trailerovým blokem (POSIX `awk`). Přestavba je z většiny velké
zlepšení a Adversář to změřil: v 318 kombinacích git po hooku nezaparsuje žádnou
attribution a hook nezahodí jedinou řádku bez markeru „cursor". Skládané trailery,
gramatika klíčů, adresní i jmenné pravidlo — to všechno je poprvé pokryté.

Adversář ale vyčerpal tři kola a v kole 3 eskaloval s `REQUEST CHANGES`. Human čtvrté kolo
v tom běhu nepovolil a poslal předmět sem, s čerstvým rozpočtem. Hookovou práci jsem
z běhu `…-0853-…` stáhl a leží v
`doc/runs/20260818-0853-harness-and-hooks-audit-86/deferred-i0005-hook.patch`.
**Tento běh z toho patche začíná, ne od nuly.**

## Vada — jedna příčina, tři dosažitelné tvary

Hook hledá trailerový blok v **surovém souboru** místo ve zprávě, kterou git nakonec
nechá. `last_blank` ukazuje na poslední prázdnou řádku souboru, takže když poslední
odstavec souboru není trailerový blok, zóna se posune jinam a attribution přežije celá.

- **B4** — zpráva končí prázdnou řádkou (nebo řádkou z mezer). `trailer_start = n+1`
  a v zóně není nic. Dosažitelné bez editoru: `git commit -F soubor`, `git commit -m $'…\n\n'`.
- **B5** — komentářový blok, který `git commit` do zprávy sám napíše. Poslední odstavec je
  pak ten blok, skutečné trailery leží před `trailer_start` a opíšou se doslova. **Tohle je
  ten vážný tvar: znamená to, že běžný commit z editoru dnes chráněný není.**
- **B6** — `git commit -v`: za komentáři je ještě diff, poslední odstavec je uvnitř diffu.

Ve všech třech tvarech ranní verze hooku attribution odstraňovala. Jde tedy o **oslabení**
věty `i0005` c1, ne o nedodělek — a proto se to nesmělo commitnout.

## Směr opravy

Adversář opravu popsal a změřil: doříznout koncové prázdné řádky, vynechat komentářové
řádky a všechno za `# --- >8 ---` **před** výpočtem `last_blank` — tedy udělat totéž, co
dělá `git commit --cleanup`. Hook si koncové blanky už zahazuje, ale až na konci; ten krok
musí přijít dřív. Není to čtvrtý pokus o regex.

Planner tenhle směr nemá brát jako hotový návrh. Má ho ověřit a případně opravit; je to
nález recenzenta, ne specifikace.

## Druhá polovina — enforcer, který mlčí

Adversář našel pět mutací, které nechávají `hook_checks.py` zelený. Vada je v kontrole,
ne v hooku; kód je správný a chybí jen řez.

- **FU-10** — případ `crlf_line_endings` je vakuózní. `hook_checks.py:340` čte výstup přes
  `Path.read_text()`, který v textovém režimu překládá `\r\n` na `\n`, takže rozdíl, o který
  tomu případu jde, zmizí ještě před srovnáním. Pila: `read_text(newline="")` nebo `read_bytes()`.
- **FU-11** — oddělovač složený jen z mezer není pojistkovaný.
- **FU-12** — adresa na pokračovací řádce u klíče mimo `-by`/`-with`.
- **FU-13** — osiřelá pokračovací řádka s adresou.
- **FU-14** — spojování složené hodnoty bez oddělovací mezery.

## Třetí polovina — zapsat cenu

- **FU-15** — attribution v těle nebo v subjectu nově **zůstává**. Je to záměr („próza před
  blokem je nedotknutelná") a git v těch tvarech žádný trailer nevidí, takže věta tím
  pravdivost neztrácí. Ale je to zásadní změna chování proti ranní verzi a nikde není
  zapsaná jako rozhodnutí, jen jako důsledek. Patří do komentáře hooku a do `hooks/README.md`.
- **FU-16** — legitimní trailer se zahodí celý, když jeho pokračovací řádka nese adresu
  (`Intent: i0005` + odsazené `see cursoragent@cursor.com` zmizí oba). Nutný důsledek toho,
  že se trailer odstraňuje jako celek. Patří do dokumentace ceny, vedle ceny předpony.

## Co se sem vědomě nebalí

FU-1 … FU-6 (dosah `i0005` z kol 1 a 2) a FU-7 … FU-9 (hranice `i0001`). První skupina je
na rozhodnutí, jestli se věta má rozšířit; druhá je změna záměru, ne oprava. Obojí patří
Humanovi, ne do opravného běhu. Rozšiřovat předmět je právě ta chyba, kterou tenhle běh
napravuje.

## Hranice běhu

Uzly `i0005` (hook) a `i0004` (`tools/checks/hook_checks.py` leží v jeho `code_paths`).
Sahá se na `hooks/` — deterministický spouštěč, takže složitost je **high** a běží Critic
i Adversář. Věty stromu se nemění: c1 i c2 zůstávají doslova, jak jsou. Tenhle běh je má
splnit, ne přeformulovat.

## Rozpočet měření pro Adversáře

Podle pravidla z běhu `…-1402-…`, které vzniklo právě kvůli tomuhle předmětu. Strop a
pořadí priorit zadám při startu Kroku 8; Adversář měří shora dolů, u stropu přestane a
`review.md` zakončí výčtem toho, co nezměřil.
