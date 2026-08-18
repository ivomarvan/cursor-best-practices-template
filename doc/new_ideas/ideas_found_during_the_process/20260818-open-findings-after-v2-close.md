# Otevřené nálezy po uzavření v2

Sesbíráno 2026-08-18, když strom došel na 100 %. Nic z toho nedělá žádnou dnešní větu
stromu nepravdivou — proto to nejsou dluhy, ale materiál k rozhodnutí. Každý nález má
zdroj v `doc/runs/`, kde je i měření, které ho našlo.

Účel tohoto souboru je jediný: aby se příští změna metodiky nebo stromu nesrazila
s něčím, co už někdo změřil a vědomě odložil.

## Skupina A — rozšíření dosahu vět, tedy změna záměru

Tohle nejsou opravy. Věty `i0001` dnes platí přesně tak, jak jsou napsané; rozšířit jejich
dosah znamená napsat jinou větu, což je práce pro `intent-change` a rozhodnutí Humana.

| # | Nález | Zdroj |
|---|---|---|
| FU-7 | `i0001` c1 hlídá odkazy v `rules/` a `skills/`, ale ne v `README.md`, `commands/*.md` ani `doc/runs/**` | běh `…-0853-…`, review kolo 1 |
| FU-8 | `i0001` c2 mluví o symlincích na `rules` a `skills`, ne o objevitelnosti `.cursor/commands` a `.cursor/hooks.json` | tamtéž |
| FU-9 | pod `skills/` jsou přípony, které kontrola odkazů nerozebírá | tamtéž |

Otázka pro Humana zní: má harness ručit za odkazy v dokumentech, které agent normálně
nečte jako instrukci? U `README.md` bych řekl ano, u `doc/runs/**` spíš ne — běhy jsou
audit, a rozbitý odkaz ve starém běhu je historický fakt, ne vada.

## Skupina B — dosah enforceru `i0005`, bez změny věty

Tady by věta zůstala, jak je; jen by se prodloužila kontrola. Menší rozhodnutí než
skupina A, ale pořád rozhodnutí, protože každý řez něco stojí.

| # | Nález | Zdroj |
|---|---|---|
| FU-2 | řádky s adresou, které git za trailer nemá, nejsou ukotvené | běh `…-0853-…`, review kolo 2 |
| FU-3 | cena předpony (`Reviewed-by: Cursory …` se smaže) je dokumentovaná, ne pojistkovaná | tamtéž |
| FU-4 | `git ls-files -- hooks` je užší než skutečný výčet hooků; hook mimo `hooks/` kontrola nevidí | tamtéž |
| FU-5 | `hooks.json` s argumentem u příkazu hlásí falešné „missing"; absolutní cesta shodí `ValueError` | tamtéž |
| FU-6 | zdvojená hláška „untracked" | tamtéž |
| FU-17 | odsazená próza **v** trailerové zóně, která cituje attribution, se zahodí | tamtéž, kolo 3 |

## Skupina C — známé limity hooku

Tyhle jsou už zapsané v `hooks/README.md` v sekci `Known limits, not addressed here`,
takže je čtenář hooku najde na správném místě. Sem patří jen jako připomínka a proto, že
u prvního z nich existuje hypotéza opravy.

| # | Nález | Zdroj |
|---|---|---|
| FU-A | ručně vepsaná scissors řádka **před** trailerovým blokem usekne i legitimní trailery. Git ten tvar nevyrábí. | běh `…-1414-…`, review kolo 1 |
| FU-B | první ze dvou odříznutí koncových blanků nemá test, který by ho izoloval | tamtéž, kolo 2 |
| FU-C | `core.commentChar` v konfiguraci neodpovídá znaku v souboru | tamtéž, kolo 1 |
| FU-D | próza **za** koncovým komentářovým blokem se čte jako poslední odstavec | tamtéž |

**Hypotéza k FU-A, neměřená.** Porovnávat scissors s **přesným tvarem**, který git píše
(`# ------------------------ >8 ------------------------`), místo hledání jakékoli řádky
obsahující `>8`. Nekouká se na zbytek zprávy, takže nemůže vzniknout defekt, který
v běhu `…-1414-…` vznikl v kole 2 — heuristika „přijmi scissors, jen když za ní nejsou
trailerové řádky" se dala porazit obyčejným diffem obsahujícím `-Intent:`.

Než na tom někdo začne pracovat, ať si přečte kolo 2 a 3 v
`doc/runs/20260818-1414-commit-msg-block-boundary-4f/review.md`. Ta epizoda stála dvě
kola a skončila revertem.

## Skupina D — zaplacené ceny, ne nálezy

Uvedeno pro úplnost, aby si to někdo příště nespletl s vadou. Obojí je záměr a obojí je
zapsané v `hooks/README.md`.

- **FU-15** — attribution v subjectu nebo v próze těla **zůstává**. Próza před trailerovým
  blokem je nedotknutelná konstrukcí, a git ten text jako trailer taky neparsuje, takže
  historie, kterou git vede, se tím nezkresluje.
- **FU-16** — legitimní trailer padá **celý**, když jeho pokračovací řádka nese adresu
  agenta. Nutný důsledek toho, že se attribution odstraňuje jako jeden celek.

## Co tady vědomě není

Nápady na rozšíření metodiky (editor stromu záměru, metakoordinátor, síla agentů) leží
jinde v `doc/new_ideas/`. Tenhle soubor je jen o tom, co se našlo měřením a co zůstalo
otevřené — ne o tom, co by bylo hezké mít.
