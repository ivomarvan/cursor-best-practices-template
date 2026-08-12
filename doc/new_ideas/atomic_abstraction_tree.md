### 1. Definice pravidel (Rámec "Atomic Abstraction Tree")

#### A) Pravidla pro definiční dokument (Struktura)

1.  **Hierarchická unikátnost**: Každý uzel $v$ je identifikován
    řetězcem (např. `#1.5.2`). Každý uzel smí přidávat pouze
    novou informační entropii (podrobnosti); nesmí duplikovat
    definice svých předků.

2.  **Kontextová soběstačnost**: Plná sémantika uzlu je dána
    výhradně cestou od kořene k tomuto uzlu. Externí odkazy
    (horizontální vazby) jsou povoleny pro vyjádření závislostí,
    nikoliv pro definici identity.

3.  **Atomické zjemnění**: Přechod z úrovně $L_n$ na $L_{n+1}$
    musí být totální – nesmí existovat implementační detail,
    který nemá svého abstraktního předka.

4.  **Formální kontrakty**: Každý uzel definuje své
    **Invarianty** (co se nemění), **Pre-kondice**
    a **Post-kondice**.
    Tyto kontrakty jsou děděny směrem dolů.

#### B) Pravidla pro vývoj a modifikaci (Proces)

1.  **Priorita abstrakce (Single Source of Truth)**: Zdrojový kód
    je pouze projekcí definičního dokumentu.
    Žádná změna nesmí začít v kódu.

2.  **Top-Down validace požadavku**: Každý nový požadavek je
    nejprve konfrontován s kořenem. Pokud je v rozporu, musí být
    iniciována "změnová vlna" od nejvyššího bodu konfliktu.

3.  **Atomická transakce dokument-kód**: Implementace
    (reimplementace) začíná až po schválení konzistence
    dokumentu.
    Testy jsou generovány přímo z kontraktů v dokumentu
    (Property-based testing).

4.  **Verifikace cyklů**: Horizontální odkazy nesmí vytvářet
    logické kruhy v definici identity (např. A je definováno
    pomocí B a B pomocí A), ale mohou existovat
    v datech/komunikaci.

---

### 2. Návrh formátu: "Markdown-Graph Hybrid"

Pro software projekt spravovaný v Gitu je nejlepším řešením
**kombinace Markdownu a strukturované adresářové hierarchie**.
Toto řešení využívá přirozenou vlastnost souborových systémů
a je snadno čitelné pro lidi i stroje (LLM, kompilátory).

#### Návrh struktury:

```text
/spec
  /1-system-root.md
  /1-system-root/
    /1.1-ui-layer.md
    /1.2-data-engine.md
    /1.2-data-engine/
      /1.2.1-db-schema.md
```

#### Proč toto řešení?

1.  **Git-Native**: Každá úroveň abstrakce je soubor.
    Diffy v Gitu přesně ukazují, na jaké úrovni abstrakce došlo
    ke změně.

2.  **Markdown + Frontmatter (YAML)**: Umožňuje definovat
    metadata a kontrakty v hlavičce souboru, zatímco tělo je
    lidsky čitelný popis.

3.  **Nástroje**: Snadno se generuje vizualizace (např. pomocí
    Mermaid.js nebo Graphviz), která z adresářové struktury
    a odkazů vykreslí graf.

#### Příklad obsahu souboru (`1.2.1-db-schema.md`):

```markdown
---
id: 1.2.1
parent: 1.2
depends_on: [1.5.8]  # Horizontální vazba (graf)
invariants: [ "user_id is unique", "created_at < updated_at" ]
---
# Specifikace DB Schématu
Tato kapitola rozvíjí Data Engine (#1.2) o konkrétní relační
modely...
```

### Shrnutí vylepšení

- **Zavedení Frontmatteru**: Pro strojové zpracování pravidel
  (kontrola invariantů).

- **Zrcadlení adresářů**: Fyzická struktura souborů vynucuje
  hierarchickou disciplínu.

- **Dependency Map**: Speciální soubor `graph.json` nebo
  `Mermaid` blok v rootu, který automaticky mapuje
  horizontální vazby (cykly v datech), zatímco stromová struktura
  souborů drží hierarchii abstrakce.

Tento systém je **"Self-Documenting Codebase"** v nejčistší
podobě. Pokud automatizační skript (např. v CI/CD) zjistí, že kód
neodpovídá kontraktům v Markdownu, sestavení selže.
