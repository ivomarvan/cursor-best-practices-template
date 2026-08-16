---
run_id: 20260816-1302-realization-layer-91
intent_ids: ["i0004"]
role: Coordinator
model: claude-opus-5-thinking-high
complexity: high
status: in-progress
---

# Zadání

## Co Human chce

Zavést do metodiky ICE **vrstvu realizace záměru**: mechanismus, který odpoví na otázku
„co ještě zbývá udělat" tím, že u každého uzlu stromu záměru eviduje, zda ho projekt
skutečně naplňuje.

Zadání navazuje na dva schválené koncepční dokumenty:

- `doc/new_ideas/intent-realization.Opus5.md` — samostatný návrh vrstvy
- `doc/new_ideas/intent-realization-status.critique-Opus5.md` — proč se liší od původního
  konceptu Humana (`intent-realization-status.concept.md`)

Human ke čtyřem otevřeným otázkám návrhu potvrdil doporučené varianty:

| Otázka | Rozhodnutí |
|--------|-----------|
| Q1 fyzické uložení | jeden soubor `doc/intent/_realization.yaml` |
| Q2 profil souhlasu | `standard` — souhlas jen u kontraktů `enforced_by: review` |
| Q3 profil důkazu | `standard` — tvrzení ukazuje na adresář běhu s `grader.md` |
| Q4 šíření zastarání | šíří se **změna textu**, ne stav |

Doslovné zadání: *„Proveď prosím celou realizaci tohoto postupu! Nezapomeň celý koncept
popsat a vysvětlit v README.md tak, aby byl tento dokument aktuální."*

## Jak tomu rozumím

Nejde o dokument, ale o funkční mechanismus. Musí tedy vzniknout současně:

1. **nástroj** — podpříkazy `intent realization` a modul, který počítá odvozené stavy;
2. **kontrakty nad ním** — vlastní testy, napojené na uzel `i0004` šablony;
3. **metodika** — pravidlo, které říká, kdo co smí zapsat, a úpravy skills tak, aby
   vrstva byla součástí normálního běhu, ne volitelný doplněk;
4. **výklad pro člověka** — oddíl v `README.md`.

Bez kteréhokoli z těch čtyř kusů je zavedení poloviční, a poloviční zavedení je horší než
žádné: agent by o vrstvě četl v pravidle a nenašel by příkaz, nebo obráceně.

## Co do zadání nepatří

- Editor stromu záměru. Human ho zmínil jako motivaci, ne jako součást tohoto běhu.
  Vrstva pro něj jen musí být čitelná strojově (`--json`), což je splněno.
- Doplnění tvrzení za existující uzly šablony. Vrstva začíná prázdná; první tvrzení
  vzniká v tomto běhu a týká se jen `i0004`.
