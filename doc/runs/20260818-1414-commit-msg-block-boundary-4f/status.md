---
run_id: 20260818-1414-commit-msg-block-boundary-4f
intent_ids: ["i0005", "i0004"]
role: Coordinator
model: claude-opus-5-thinking-high
complexity: high
status: done
---

# Stav běhu — hranice trailerového bloku

## Výsledek

Hotovo, `i0005` nárokovaný. Tím je strom na 100 %: pět uzlů, pět nároků, žádný `stale`,
`broken` ani čekající na přijetí.

`commit-msg` hook je nasazený ve strukturální podobě nad trailerovým blokem a hranici toho
bloku počítá ve zprávě, kterou git nechá, ne v surovém souboru. Tím zmizely všechny tři
tvary, kvůli kterým předchozí běh skončil eskalací — a hlavně B5, tedy běžný commit
z editoru, který dnes ráno chráněný nebyl.

## Role, modely, kola

| Role | Model | Kol |
|---|---|---|
| Coordinator + Grader | `claude-opus-5-thinking-high` (volba Humana v UI) | 4 |
| Planner | `cursor-grok-4.5-high` | 1 |
| Critic | `claude-sonnet-5-thinking-high` | 1 — `ACCEPT` bez blokátorů |
| Coder | `claude-sonnet-5-thinking-high` | 4 |
| Adversary | `cursor-grok-4.5-high` | 3 — `APPROVE` / `REQUEST CHANGES` / `APPROVE` |

Adversář poprvé pracoval pod rozpočtem podle pravidla z běhu `…-1402-…`: ~40 měření
v kole 1, ~25 v kole 2, ~15 v kole 3, a každé kolo končí výčtem neměřeného. Předchozí běh
nad týmž předmětem měřil bez stropu skoro tři hodiny. Pravidlo funguje.

## Chyba Coordinátora, a co z ní plyne

**Kolo 2 jsem si vyžádal a neměl jsem.** Adversář po kole 1 dal `APPROVE` bez blokátorů
a výslovně napsal, že FU-A nárok neblokuje. FU-A je tvar, který git sám nikdy nevyrobí —
ručně vepsaná scissors řádka před trailery. Přesto jsem si vyžádal kolo navíc, aby
z podpisu zmizela hvězdička.

Coder v něm zavedl heuristiku „přijmi scissors jen tehdy, když za ní nejsou trailerové
řádky". Ta FU-A opravila a rozbila `git commit -v`: `is_key` matchuje i `-Intent:` v diffu,
takže skutečná hranice byla odmítnuta a attribution přežila (B7). Druhá půlka kola 2
odstranila odříznutí blanků na základě důkazu, který neplatil (B8).

Vyměnil jsem doložený stav za nedoložený, kvůli tvaru, o kterém recenzent řekl, že nevadí.
Human rozhodl kolo 2 vrátit celé; Adversář revert ověřil a potvrdil, že B7 i B8 odešly
s ním a B4/B5/B6 drží.

**Poučení, které patří do metodiky, ne jen sem:** `APPROVE` s pojmenovanou výhradou je
uzavřený verdikt. Otevřít ho kvůli follow-upu, který recenzent sám označil za neblokující,
je rozhodnutí o riziku — a Coordinator ho nemá dělat sám. Navrhuji to Humanovi jako
kandidáta na větu do `07-ice-workflow.mdc`, ne jako hotovou změnu.

## Kolo 4 — jedna věta

Adversář v kole 3 pojmenoval jednu opravu k provedení při uzavírání: `hooks/README.md`
tvrdil, že první odříznutí koncových blanků je nadbytečné, což jeho vlastní měření B8
vyvrátilo. Nechal jsem tu větu opravit na to, co je pravda — chybí test, který ten krok
izoluje, ne že je zbytečný. Nepovažuji to za čtvrté kolo recenze: je to závěrečná akce,
kterou recenzent jmenovitě předepsal a předem schválil. Kód se nehnul, jen próza.

## Co zůstává jako známý limit

Zapsané v `hooks/README.md` v sekci `Known limits, not addressed here`, ne schované:

- **FU-A** — ručně vepsaná scissors řádka před trailerovým blokem usekne i legitimní
  trailery. Git ten tvar nevyrábí. Správná oprava podle mého odhadu existuje a je
  jednodušší než ta, co selhala: porovnávat s **přesným tvarem**, který git píše, místo
  hledání jakékoli řádky s `>8`. Nekouká se na zbytek, takže B7 nemůže vzniknout.
  Nezkoušel jsem to a nikdo to neměřil — je to hypotéza pro budoucí běh.
- **FU-B** — první odříznutí koncových blanků nemá test, který by ho izoloval.
- **FU-C** — `core.commentChar` v konfiguraci neodpovídá znaku v souboru.
- **FU-D** — próza *za* koncovým komentářovým blokem.
- **FU-15, FU-16** — dvě ceny zaplacené záměrně: attribution v subjectu nebo v těle
  zůstává; legitimní trailer padá celý, když jeho pokračovací řádka nese adresu agenta.

Nesené z předchozích běhů a mimo rozsah: **FU-1 … FU-9**, **FU-17**.

## Human gate

Složitost `high`, takže Human review je **required**. Předkládám k rozhodnutí: uzavření
běhu, nárok na `i0005`, a otázku, jestli se poučení z kola 2 má zapsat do metodiky.
