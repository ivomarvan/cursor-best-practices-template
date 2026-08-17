# Cursor Models & Pricing

> **Source:** https://cursor.com/docs/models-and-pricing  
> **Extracted:** 2026-08-17 · **Renamed:** 2026-08-17  
> **Unit:** USD per million tokens (unless noted otherwise)

## Usage pools

| Pool | Models | Billing |
|------|--------|---------|
| **Cursor Models** | Grok 4.6, Grok 4.5, Composer 2.5 | Significantly more included usage on Pro+ |
| **Other Models** | All third-party models below | Charged at API rate; Pro/Pro Plus/Ultra include ≥ $20/mo |

---

## Cursor Models

| Model | Provider | Input | Cache write | Cache read | Output | Notes |
|-------|----------|------:|------------:|-----------:|-------:|-------|
| Grok 4.6 | Cursor | $2 | — | $0.5 | $6 | Jointly trained by Cursor and SpaceXAI |
| Grok 4.6 (Fast) | Cursor | $4 | — | $1 | $12 | Jointly trained by Cursor and SpaceXAI |
| Grok 4.5 | Cursor | $2 | — | $0.5 | $6 | Jointly trained by Cursor and SpaceXAI |
| Grok 4.5 (Fast) | Cursor | $4 | — | $1 | $12 | Jointly trained by Cursor and SpaceXAI |
| Composer 2.5 | Cursor | $0.5 | — | $0.2 | $2.5 | — |
| Composer 2.5 (Fast) | Cursor | $3 | — | $0.5 | $15 | — |

---

## Other Models

### Anthropic

| Model | Input | Cache write | Cache read | Output | Notes |
|-------|------:|------------:|-----------:|-------:|-------|
| Claude 4 Sonnet | $3 | $3.75 | $0.3 | $15 | Hidden by default; Thinking variant counts as 2 requests in legacy pricing |
| Claude 4 Sonnet 1M | $6 | $7.5 | $0.6 | $22.5 | Hidden by default; 2× cost when input exceeds 200k tokens |
| Claude 4.5 Haiku | $1 | $1.25 | $0.1 | $5 | Hidden by default; Bedrock/Vertex regional endpoints +10% surcharge |
| Claude 4.5 Opus | $5 | $6.25 | $0.5 | $25 | Hidden by default; Requires Max Mode on legacy request-based plans |
| Claude 4.5 Sonnet | $3 | $3.75 | $0.3 | $15 | Hidden by default; Up to 1M tokens, no long-context surcharge |
| Claude 4.6 Opus | $5 | $6.25 | $0.5 | $25 | Hidden by default; Up to 1M tokens, no long-context surcharge |
| Claude 4.6 Sonnet | $3 | $3.75 | $0.3 | $15 | Hidden by default; Up to 1M tokens, no long-context surcharge |
| Claude 4.7 Opus | $5 | $6.25 | $0.5 | $25 | Hidden by default; Up to 1M tokens, no long-context surcharge |
| Claude Fable 5 | $10 | $12.5 | $1 | $50 | ~2× cost of Claude Opus 5; requires data retention approval for Enterprise |
| Claude Opus 4.7 (fast mode) | $30 | $37.5 | $3 | $150 | Hidden by default; Limited research preview |
| Claude Opus 4.8 | $5 | $6.25 | $0.5 | $25 | Hidden by default; Fast mode (`claude-opus-4-8-fast`) 3× lower than Opus 4.7 fast mode |
| Claude Opus 5 | $5 | $6.25 | $0.5 | $25 | Fast mode (`claude-opus-5-fast`); Up to 1M tokens |
| Claude Sonnet 5 | $2 | $2.5 | $0.2 | $10 | Up to 1M tokens; updated tokenizer |

### Google

| Model | Input | Cache write | Cache read | Output | Notes |
|-------|------:|------------:|-----------:|-------:|-------|
| Gemini 2.5 Flash | $0.3 | — | $0.03 | $2.5 | Hidden by default |
| Gemini 3 Flash | $0.5 | — | $0.05 | $3 | Hidden by default |
| Gemini 3 Pro | $2 | — | $0.2 | $12 | Hidden by default |
| Gemini 3 Pro Image Preview | $2 | — | $0.2 | $12 | Image output: $120/1M tokens (~$0.134 per 1K/2K image, ~$0.24 per 4K image) |
| Gemini 3.1 Pro | $2 | — | $0.2 | $12 | — |
| Gemini 3.5 Flash | $1.5 | — | $0.15 | $9 | Hidden by default |
| Gemini 3.6 Flash | $1.5 | — | $0.15 | $7.5 | Hidden by default |
| Gemini 3.7 Flash | $0.75 | — | $0.075 | $3.5 | — |

### OpenAI

| Model | Input | Cache write | Cache read | Output | Notes |
|-------|------:|------------:|-----------:|-------:|-------|
| GPT-5 | $1.25 | — | $0.125 | $10 | Hidden by default; reasoning variant: gpt-5-high |
| GPT-5 Fast | $2.5 | — | $0.25 | $20 | Hidden by default; 2× price; variants: gpt-5-high-fast, gpt-5-low-fast |
| GPT-5 Mini | $0.25 | — | $0.025 | $2 | Hidden by default |
| GPT-5-Codex | $1.25 | — | $0.125 | $10 | Hidden by default |
| GPT-5.1 Codex | $1.25 | — | $0.125 | $10 | Hidden by default |
| GPT-5.1 Codex Max | $1.25 | — | $0.125 | $10 | Hidden by default |
| GPT-5.1 Codex Mini | $0.25 | — | $0.025 | $2 | Hidden by default; 4× rate limits vs GPT-5.1 Codex |
| GPT-5.2 | $1.75 | — | $0.175 | $14 | Hidden by default; variant: gpt-5.2-high |
| GPT-5.2 Codex | $1.75 | — | $0.175 | $14 | Hidden by default |
| GPT-5.3 Codex | $1.75 | — | $0.175 | $14 | Hidden by default; variant: gpt-5.3-codex-high |
| GPT-5.4 | $2.5 | — | $0.25 | $15 | 90% discount on cached input; Fast mode 2× pricing; 1M context 2× input |
| GPT-5.4 Mini | $0.75 | — | $0.075 | $4.5 | Hidden by default; 90% discount on cached input |
| GPT-5.4 Nano | $0.2 | — | $0.02 | $1.25 | Hidden by default; 90% discount on cached input |
| GPT-5.5 | $5 | — | $0.5 | $30 | Fast mode at higher rates; 1M context 2× input |
| GPT-5.6 Luna | $0.2 | $0.25 | $0.02 | $1.2 | Fast mode 2× pricing; cache writes at 1.25× input |
| GPT-5.6 Sol | $5 | $6.25 | $0.5 | $30 | Fast mode 2× pricing; 1M context 2× input |
| GPT-5.6 Terra | $2 | $2.5 | $0.2 | $12 | Mid-tier between Sol and Luna; Fast mode 2× pricing |

### Other providers

| Model | Provider | Input | Cache write | Cache read | Output | Notes |
|-------|----------|------:|------------:|-----------:|-------:|-------|
| GLM 5.2 | Z.ai | $1.4 | — | $0.26 | $4.4 | Hidden by default |
| Kimi K2.7 Code | Moonshot | $0.95 | — | $0.19 | $4 | Hidden by default |
| Kimi K3 | Moonshot | $3 | — | $0.3 | $15 | Hidden by default; Up to 1M tokens; no cache-write fee |

---

## Subscription plans

| Plan | Price | Other Models included | Cursor Models |
|------|-------|----------------------:|---------------|
| **Start** (India only) | ₹649/mo, tax inclusive | $0 | Generous included usage |
| **Pro** | $20/mo | $20 | Generous included usage |
| **Pro Plus** | $60/mo | $70 | Generous included usage |
| **Ultra** | $200/mo | $400 | Generous included usage |

### Teams

| Seat type | Price |
|-----------|-------|
| Standard | $40/user/mo |
| Premium | $120/user/mo (5× Standard Agent limits) |

---

## Additional fees & surcharges

| Item | Rate | Applies to |
|------|------|------------|
| **Cursor Token Rate** | $0.25 / 1M tokens | Teams & Enterprise: third-party models (not Cursor Models, not Auto Cost) |
| **Regional data residency** | +10% on model pricing | Eligible models when opted in |
| **Max Mode** (legacy plans) | Model API rate + 20% | Legacy request-based plans only |

## Auto modes

| Mode | Pricing |
|------|---------|
| **Auto Cost** | Fixed per-million-token rate (model-independent) |
| **Auto Balance** | Model API rate + Cursor Token Rate (Teams/Enterprise) |
| **Auto Intelligence** | Model API rate + Cursor Token Rate (Teams/Enterprise) |
