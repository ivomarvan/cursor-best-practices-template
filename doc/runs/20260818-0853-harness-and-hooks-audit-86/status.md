# Stav běhu — audit dosahu `cmd:` kontraktů

Složitost: `high`. Uzavřeno 2026-08-18 v zúženém rozsahu po eskalaci Adversáře.

## Co se zavírá

| Předmět | Výsledek |
|---|---|
| `i0001` c1 — relativní odkazy v rules a skills | dosah rozšířen, nárokováno |
| `i0001` c2 — objevitelnost přes `.cursor` symlinky | dosah rozšířen, nárokováno |
| FU-B — druhé odvozovací místo `c12` bez testu | uzavřeno |
| FU-C — jak měřit „je věta nepravdivá **teď**" | uzavřeno |
| FU-D — `request.md` jako soubor versus sekce | uzavřeno |
| `i0005` c1, c2 — hook a jeho enforcer | **staženo, předáno běhu D** |

## Rozhodnutí Humana po eskalaci

Adversář vyčerpal tři kola a v kole 3 vydal `REQUEST CHANGES` s eskalací. Nález byl
jedna příčina ve třech dosažitelných tvarech (B4, B5, B6): přestavěný `commit-msg` hook
hledal trailerový blok v **surovém souboru** místo ve zprávě, kterou git nakonec nechá,
takže zpráva končící prázdnou řádkou, zpráva s komentářovým blokem od `git commit` a
`git commit -v` posunuly hranici bloku jinam a attribution prošla. Ranní verze hooku ji
v těch tvarech odstraňovala — šlo tedy o **oslabení** věty `i0005` c1, ne o nedodělek.

Human čtvrté kolo v tomto běhu nepovolil a rozhodl, že hook dostane vlastní běh s čerstvým
rozpočtem kol. Důvod je věcný: přepis na `awk` je nový kód, který dostal jedinou recenzi,
a zaslouží si plný rozpočet, ne zbytkové kolo.

## Co se stáhlo a kde to je

Vráceny do stavu před během: `hooks/git/commit-msg`, `hooks/README.md`,
`tools/checks/hook_checks.py`. Z `tools/intent/tests/test_checks.py` zůstaly jen třídy
`TemplateLinkTest` a `TemplateSymlinkTest`; třídy `HookAttributionCheckTest` a
`HookExecutableCheckTest` odešly s hookem.

Práce se nezahodila — celý diff leží v `deferred-i0005-hook.patch` (604 řádek) a běh D
z něj začíná, ne od nuly. Adversářova oprava je v `review.md` popsaná přesně: doříznout
koncové prázdné řádky a vynechat komentářové řádky i vše za scissors **před** výpočtem
hranice bloku, plus dva `Case`y, které má změřené a které na současné verzi padají.

`plan.md`, `report.md`, `critique.md` a `coder-evidence.md` proto popisují širší předmět,
než co běh nakonec dodal. Nepřepisuji je: jsou to předměty, které Critic a Adversář
posuzovali, a zpětný přepis by ten posudek smazal. Rozdíl je zaznamenán zde a čtenář má
tento soubor číst jako poslední. Scope guard hlásí `clean`, protože hlídá nedeklarované
změny, ne nedodané.

## Doklad

`grader.md` je přeměřený nad zúženým stavem (kolo 4): 99 testů, `validate` 5 uzlů bez
chyby, `scope clean`, `realization check consistent`, oba `checks` skripty zelené,
`coverage` 28 z 28 kontraktů strojově vymáhaných, ruff čistý.

Adversářova měření pro `i0001` stojí beze změny ze všech tří kol — 23 mutací A1/A2 a
14 mutací A4, přeměřeno v kole 3 s výsledkem „nepohnuly se". Adversář na přímou otázku
odpověděl, že `i0001` c1 i c2 podepisuje.

## Co zůstává otevřené

Pro běh D (hook):

- **B4, B5, B6** — hranice trailerového bloku se počítá nad surovým souborem.
- **FU-10 … FU-14** — pět mutací enforceru, které nechávají kontrolu zelenou: vakuózní
  případ CRLF (kontrola čte výstup přes `read_text()`, který `\r\n` přeloží), oddělovač
  z mezer, adresa na pokračovací řádce u klíče mimo `-by`/`-with`, osiřelá pokračovací
  řádka, spojování složené hodnoty bez mezery.
- **FU-15** — attribution v těle nebo v subjectu nově zůstává. Je to záměr („próza před
  blokem je nedotknutelná"), ale nikde to není zapsané jako rozhodnutí.
- **FU-16** — legitimní trailer se zahodí celý, když jeho pokračovací řádka nese adresu.
- **FU-1 … FU-6** — dosah `i0005` c1 a c2 z kol 1 a 2.

Materiál do `doc/new_ideas/`, ne dluh tohoto stromu:

- **FU-7, FU-8, FU-9** — hranice `i0001`: c1 nedosahuje na `README.md`, `commands/*.md`
  ani `doc/runs/**`; c2 nezahrnuje objevitelnost `.cursor/commands` a `.cursor/hooks.json`;
  přípony pod `skills/` nejsou probrané. Rozšířit dosah těchto vět je změna záměru, ne
  oprava — patří to Humanovi, ne do opravného běhu.

Do metodiky (běh D nebo samostatně):

- Recenze hooku trvala tři hodiny. Adversář má dostat **rozpočet v jednotkách práce**
  („změř nejvýš tolik mutací, v tomhle pořadí priorit") a **povinnost na konci vyjmenovat,
  co nezměřil**. Časový strop by tenhle problém neřešil — nedoměřená recenze, která mlčí,
  vypadá stejně jako schvalující.
- Tento běh nesl čtyři audity, tři follow-upy a přepis hooku. To je na jeden běh moc.

## Odchylky od metodiky

Kolo 4 Gradera po stažení předmětu autorizoval Coordinator. Není to čtvrté kolo hodnocení
téhož: kola 1 až 3 hodnotila širší předmět, tohle měří užší předmět, který z něj zbyl,
a strojová brána nemá co interpretovat. Adversář nad zúženým stavem znovu nešel — všechno,
co zůstalo, přeměřil v kole 3 jako „nepohnulo se".
