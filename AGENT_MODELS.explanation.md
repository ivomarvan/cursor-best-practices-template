# AGENT_MODELS.md — proč takhle (17. 8. 2026)

Tento soubor je lidský záznam rozhodnutí o výchozím katalogu
[`AGENT_MODELS.md`](AGENT_MODELS.md). Metodika ICE názvy modelů do pravidel
nepřibíjí (`rules/00-model-policy.mdc`): schopnost role je stálá, slug je data.

Katalog je rozhodnutí Humana. Starší verze zůstává v gitu.

## Podklady

| Soubor | Co z něj plyne |
|--------|----------------|
| [`doc/cursor_models/cursor_models_prices.260817.md`](doc/cursor_models/cursor_models_prices.260817.md) | sazby USD / 1M tokenů, dva usage pooly |
| [`doc/cursor_models/cursor_models_benchmark.260817.md`](doc/cursor_models/cursor_models_benchmark.260817.md) | SWE-bench Verified, SWE-bench Pro / DeepPlanning, mezery u review |
| Oficiální ceník Cursoru, 17. 8. 2026 | launch sleva 50 % u Grok 4.6 (jeden týden od 12. 8. 2026) |

Do katalogu jdou jen slugy, které Coordinator umí předat subagentovi v tomto
prostředí. Jinak by řádek v YAML byl přání, ne spustitelná politika.

## Ekonomické jádro ICE

Silný model na přemýšlení (Planner, Critic, Adversary), levnější na psaní
(Coder). Grader není LLM. Adversary se musí lišit od Codera, Critic od Plannera
— stejný model má sklon schválit vlastní úvahu.

Běhy na uzlu `i0004` to potvrdily empiricky: strojové brány byly zelené od
začátku, Kritik i Adversary dvakrát zamítli. Testy neodhalí, že text kontraktu
slibuje víc, než test dokazuje. Šetřit na Coderovi je správně; šetřit na
Critic / Adversary u `medium` a `high` je proti smyslu ICE.

Objem tokenů drží Coder (řez, kód, testy, smyčky). Critic a Adversary čtou a
píší málo — tam se vyplatí zaplatit čtenáře.

## Dva pooly, ne jen dolary za token

| Pool | Modely | Proč na tom záleží |
|------|--------|--------------------|
| **Cursor Models** | Grok 4.6, Grok 4.5, Composer 2.5 | štědřejší included usage na Pro / Pro+ / Ultra |
| **Other Models** | Claude, GPT, Gemini, … | API sazba; Pro zahrnuje od $20/měsíc |

Výchozí katalog šablony proto dává velkoobjemové role (Coder, střední
přemýšlení) do Cursor Models. Other Models se utrácí na máloobjemové brány,
kde je potřeba jiná laboratoř a silné čtení.

## Proč Grok 4.6 nahradil Sonnet 5

Na číslech z 17. 8. Grok 4.6 Sonnet 5 dominuje:

| | Grok 4.6 | Claude Sonnet 5 |
|--|----------|-----------------|
| SWE-Verified | 95,6 % | 79,6 % |
| SWE-Pro (proxy plánování) | 64,7 % | 63,2 % |
| vstup / výstup | $2 / $6 | $2 / $10 |
| pool | Cursor Models | Other Models |

Původní katalog dával Coderovi na `high` Sonnet 5. To nebyl upgrade: stejné
programování jako Composer 2.5 (79,6 %), výrazně horší než Grok 4.6.

Grok 4.5 při stejné ceně zaostává za 4.6 — do katalogu nepatří. Fast varianty
(Composer Fast, Grok Fast) stejnou kvalitu prodávají 2–6× dráž — taky ne.

## Launch sleva Grok 4.6

Oficiální stránka uvádí 50% launch slevu na jeden týden od 12. 8. 2026.
Hodnotili jsme **tabulkové** sazby `$2 / $6`, bez dalšího 50% krácení.
Extrakt v `cursor_models_prices.260817.md` promo poznámku nemá; Grok 4.5 bez
slevy má stejná čísla, takže `$2 / $6` je spíš ceník a sleva se strhává při
účtování.

Po ~19. 8. 2026 může Grok 4.6 zdražit (horní odhad: úroveň Fast, `$4 / $12`).
To neruší volbu Grok jako Coder v poolu Cursor Models. Mění to čistý API
poměr proti Sonnet 5. Až poběží další obnova katalogu, brát cenu **po** akci.

## Proč Opus 5 zůstává (a kde)

Opus 5 má SWE-Pro **79,2 %** proti ~65 % u Grok / Luna / Sol. To je jediná
velká mezera v plánování, která ospravedlní 2,5–4× cenu — a jen na málo
tokenech.

| Role × pásmo | Slug | Proč |
|--------------|------|------|
| Coder `low` | `composer-2.5` | $0,50 / $2,50, Cursor pool, 79,6 % SWE-Verified; Grader chytí uklouznutí |
| Coder `medium`/`high` | `cursor-grok-4.6-high` | 95,6 % SWE-Verified, Cursor pool |
| Planner `low`/`medium` | `cursor-grok-4.6-high` | plánovací proxy ~65 %, stejné nebo lepší než Sonnet 5, included pool |
| Planner `high` | `claude-opus-5-thinking-high` | SWE-Pro 79,2 % — změna stromu a dekompozice |
| Critic `low`/`medium` | `claude-sonnet-5-thinking-high` | jiná laboratoř než Grok Planner; na `low` se brána nepouští |
| Critic `high` | `cursor-grok-4.6-high` | musí se lišit od Opus Planner; pořád frontier kódování |
| Adversary `medium` | `claude-sonnet-5-thinking-high` | jiná laboratoř než Grok Coder; malý objem |
| Adversary `high` | `claude-opus-5-thinking-high` | poslední LLM brána; v tomto harnessu rozhodoval čtenář, ne pisatel |
| Coordinator `low` | `composer-2.5` | směrování uvnitř jednoho uzlu |
| Coordinator `medium` | `cursor-grok-4.6-high` | špatná klasifikace je drahá; Grok Sonnet 5 přebíjí |
| Coordinator `high` | `claude-opus-5-thinking-high` | směrování změny záměru |

Původní katalog dával Plannerovi i Criticovi na `high` stejný Opus 5. Tím
porušoval `critic_differs_from_planner`. Teď na `high` platí Planner = Opus,
Critic = Grok.

## Co do výchozího katalogu nepatří

| Kandidát | Důvod |
|----------|--------|
| `gpt-5.6-luna-medium` | $0,20 / $1,20 a 93 % SWE-Verified — nejlepší Coder na čistých API dolarech. Pálí ale pool Other Models. Patří do přepisu projektu, až dojde included usage Cursor Models. |
| `gpt-5.6-sol-medium` | cena jako Opus, plánování jako Grok |
| `claude-sonnet-5-thinking-high` jako Coder | žádný zisk proti Composeru, velká ztráta proti Groku |
| Fast varianty | stejná kvalita, 2–6× cena |
| Gemini 3.7 Flash, Kimi K3 | na 17. 8. nešly předat subagentovi |

Přepis jen Codera (varianta po vyčerpání Cursor poolu):

```yaml
roles:
  Coder:
    intent: implementation and tests; API-metered after Cursor-pool exhaustion
    lock: false
    pinned: null
    low: gpt-5.6-luna-medium
    medium: gpt-5.6-luna-medium
    high: gpt-5.6-luna-medium
```

Adversary může zůstat Sonnet / Opus (jiná laboratoř než Luna). Na `high`
Adversary by i potom měl zůstat Opus: chytá vady kontrakt vs. test, ne body
SWE-bench.

## Rodičovské okno

Cursor model rodičovského chatu sám nepřepne. Katalog platí pro subagenty.
Volba Humana v UI je autoritativní pro roli, kterou rodičovské okno právě
hraje. Nesedí-li s řádkem katalogu, Coordinator má připomenout přepnutí — a
nesmí to hlásit jako odchylku od metodiky.

Důsledek: chceš-li, aby Coderovi vládl katalog, musí být Coder subagent.
Píše-li kód rodičovské okno, platí ekonomika toho okna.

## Jak se pásmo zvolí

Pásmo `low` / `medium` / `high` není položka v přepínači modelu. Je to
náročnost **běhu**, kterou klasifikuje Coordinator podle
`rules/07-ice-workflow.mdc`. Jedna klasifikace platí pro všechny role.
Coordinator smí pásmo zvednout; snížit ho smí jen Human.

Podrobněji, včetně návrhu na MetaCoordinatora, viz
[`doc/new_ideas/ideas_found_during_the_process/20260817-agent-strength-and-metacoordinator.md`](doc/new_ideas/ideas_found_during_the_process/20260817-agent-strength-and-metacoordinator.md).

Obnova katalogu při nové vlně modelů:
[`doc/new_ideas/ideas_found_during_the_process/20260817-agent-models-catalog-refresh.md`](doc/new_ideas/ideas_found_during_the_process/20260817-agent-models-catalog-refresh.md).
