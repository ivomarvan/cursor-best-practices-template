# Cursor Models — Benchmark Overview

> **Compiled:** 2026-08-17  
> **Models:** same set as [cursor_models_prices.260817.md](cursor_models_prices.260817.md)  
> **Unit:** percent (%) unless noted otherwise

## How to read this table

| Column | Benchmark | What it approximates |
|--------|-----------|----------------------|
| **Planning** | [DeepPlanning](https://arxiv.org/html/2601.18137v1) avg. case accuracy | Long-horizon agentic planning with verifiable constraints (travel + shopping tasks) |
| **Planning (proxy)** | [SWE-bench Pro](https://www.swebench.com/) resolve rate | Multi-step, repo-scale software work when DeepPlanning score is unavailable |
| **Programming** | [SWE-bench Verified](https://www.vals.ai/benchmarks/swebench) | Real GitHub issue resolution (vals.ai harness, mini-swe-agent, bash-only) |
| **Review / critique** | [SWE-PRBench](https://arxiv.org/pdf/2603.26130) composite score | Detecting human-flagged PR issues (diff-only review task) |

**Conventions**

- `—` = no public score found for this exact model variant.
- **(Fast)** variants inherit the base model score (speed tier only).
- **Planning proxy** values are marked with `*` and use SWE-bench Pro instead of DeepPlanning.
- Review column uses SWE-PRBench only where the model was directly evaluated; c-CRAB evaluates review *agents* (tools), not bare models — see notes below.

### Sources

| Benchmark | Primary source | Snapshot date |
|-----------|----------------|---------------|
| SWE-bench Verified | [vals.ai](https://www.vals.ai/benchmarks/swebench) / [BenchLM mirror](https://benchlm.ai/benchmarks/valsswebench) | 2026-08-12 |
| SWE-bench Pro | [llm-stats](https://llm-stats.com/benchmarks/swe-bench-pro), [Benchmark Atlas](https://atlas.kevinhu.io/benchmarks/swe-bench-pro-public-dataset-scale-ai-2) | 2026-08 |
| DeepPlanning | [ACL 2026 paper](https://arxiv.org/html/2601.18137v1), [Qwen Agent leaderboard](https://qwenlm.github.io/Qwen-Agent/en/benchmarks/deepplanning/) | 2026-06 |
| SWE-PRBench | [arXiv:2603.26130](https://arxiv.org/pdf/2603.26130) | 2026-03 |

---

## Cursor Models

| Model | Planning | Programming | Review / critique | Notes |
|-------|:--------:|:-----------:|:-----------------:|-------|
| Grok 4.6 | — *64.7%* | 95.6% | — | SWE-Pro from Grok 4.5 (Grok 4.6 Pro not published) |
| Grok 4.6 (Fast) | — *64.7%* | 95.6% | — | Same capability tier as Grok 4.6 |
| Grok 4.5 | 19.1% † | 86.6% | — | † DeepPlanning: Grok 4.1-fast (reasoning), closest published proxy |
| Grok 4.5 (Fast) | 19.1% † | 86.6% | — | Same as Grok 4.5 |
| Composer 2.5 | — *—* | 79.6% | — | Cursor-native coding model |
| Composer 2.5 (Fast) | — *—* | 79.6% | — | Same as Composer 2.5 |

---

## Anthropic

| Model | Planning | Programming | Review / critique | Notes |
|-------|:--------:|:-----------:|:-----------------:|-------|
| Claude 4 Sonnet | — *—* | 72.7% | — | BenchLM aggregate |
| Claude 4 Sonnet 1M | — *—* | — | — | No separate public benchmark |
| Claude 4.5 Haiku | — *—* | 73.3% | 15.3% | Review: SWE-PRBench (Haiku 4.5) |
| Claude 4.5 Opus | 37.0% | — | — | DeepPlanning (w/ thinking) |
| Claude 4.5 Sonnet | 26.8% | 77.2% | — | DeepPlanning (w/ thinking) |
| Claude 4.6 Opus | 58.9% | 80.8% | — | DeepPlanning: Opus 4.6 Max |
| Claude 4.6 Sonnet | — *53.8%* | 79.6% | — | SWE-Pro proxy |
| Claude 4.7 Opus | — *64.3%* | 82.0% | — | SWE-Pro proxy |
| Claude Fable 5 | — *80.3%* | 95.0% | — | SWE-Pro proxy; premium tier |
| Claude Opus 4.7 (fast mode) | — *64.3%* | — | — | SWE-Pro proxy (Opus 4.7) |
| Claude Opus 4.8 | — *69.2%* | 88.6% | — | SWE-Pro proxy |
| Claude Opus 5 | — *79.2%* | 97.0% | — | SWE-Pro proxy |
| Claude Sonnet 5 | — *63.2%* | 79.6% | — | SWE-Pro proxy |

---

## Google

| Model | Planning | Programming | Review / critique | Notes |
|-------|:--------:|:-----------:|:-----------------:|-------|
| Gemini 2.5 Flash | — *—* | — | — | No vals.ai entry; Gemini 2.5 Pro = 54.4% |
| Gemini 3 Flash | 33.8% | 75.0% | — | DeepPlanning: Gemini 3 Flash Preview |
| Gemini 3 Pro | 27.4% | 76.4% | — | DeepPlanning: Gemini 3 Pro Preview |
| Gemini 3 Pro Image Preview | 27.4% | 76.4% | — | Same text model as Gemini 3 Pro |
| Gemini 3.1 Pro | — *54.2%* | 78.8% | — | SWE-Pro proxy |
| Gemini 3.5 Flash | — *55.1%* | 78.8% | — | SWE-Pro proxy |
| Gemini 3.6 Flash | — *58.7%* | 79.6% | — | SWE-Pro proxy |
| Gemini 3.7 Flash | — *—* | 87.0% | — | vals.ai difficulty aggregate; no SWE-Pro entry |

---

## OpenAI

| Model | Planning | Programming | Review / critique | Notes |
|-------|:--------:|:-----------:|:-----------------:|-------|
| GPT-5 | 30.5% | — | 11.3% | DeepPlanning: GPT-5-high; Review: SWE-PRBench uses GPT-4o (closest published) |
| GPT-5 Fast | 30.5% | — | — | Same as GPT-5 |
| GPT-5 Mini | — *—* | 60.8% | — | |
| GPT-5-Codex | — *—* | — | — | No separate public score |
| GPT-5.1 Codex | — *—* | 69.8% | — | vals: GPT-5.1 |
| GPT-5.1 Codex Max | — *—* | 69.8% | — | Proxy: GPT-5.1 |
| GPT-5.1 Codex Mini | — *—* | 60.8% | — | Proxy: GPT-5 mini |
| GPT-5.2 | 44.6% | 75.8% | — | DeepPlanning: GPT-5.2-high |
| GPT-5.2 Codex | — *56.4%* | 72.4% | — | SWE-Pro proxy |
| GPT-5.3 Codex | — *56.0%* | 78.0% | — | SWE-Pro proxy |
| GPT-5.4 | — *57.7%* | 78.2% | — | SWE-Pro proxy |
| GPT-5.4 Mini | — *54.4%* | 73.0% | — | SWE-Pro proxy |
| GPT-5.4 Nano | — *52.4%* | 69.8% | — | SWE-Pro proxy |
| GPT-5.5 | — *58.6%* | 82.6% | — | SWE-Pro proxy |
| GPT-5.6 Luna | — *62.7%* | 93.0% | — | SWE-Pro proxy |
| GPT-5.6 Sol | — *64.6%* | 96.2% | — | SWE-Pro proxy |
| GPT-5.6 Terra | — *63.4%* | 75.2% | — | SWE-Pro proxy |

---

## Other providers

| Model | Planning | Programming | Review / critique | Notes |
|-------|:--------:|:-----------:|:-----------------:|-------|
| GLM 5.2 | 14.6% † | 82.8% | — | † DeepPlanning: GLM-5 (w/ thinking) |
| Kimi K2.7 Code | — *—* | 78.2% | — | |
| Kimi K3 | 14.3% † | 93.4% | — | † DeepPlanning: Kimi K2.5 (w/ thinking) |

---

## Review / critique — what exists (and what does not)

Public benchmarks for *reviewing other agents' outputs* are immature compared to coding benchmarks:

| Benchmark | Scope | Relevant Cursor models | Key finding |
|-----------|-------|------------------------|-------------|
| **SWE-PRBench** | PR diff review vs. human ground truth | Claude Haiku 4.5 (15.3%), Claude Sonnet 4.6 (15.2%), GPT-4o (11.3%) | Best models detect only ~15–31% of human-flagged issues |
| **c-CRAB** | Test-based code review agent evaluation | Claude Code (Sonnet 4.6 backend): 32.1% pass rate | Evaluates review *tools*, not bare LLMs; union of 4 tools ≈ 41.5% |
| **SWR-Bench** | Real-world PR comment generation | No per-model public leaderboard for Cursor catalog | LLM-as-judge eval; systems generally underperform humans |

**Practical takeaway:** For adversarial review roles (Critic, Adversary, Grader), there is no comprehensive public leaderboard covering all Cursor models. SWE-PRBench suggests Claude Sonnet 4.6 and Haiku 4.5 lead among evaluated models, with GPT-4o trailing on precision (lower hallucination rate).

---

## Rankings snapshot (programming only)

Top 10 models from the Cursor catalog on **SWE-bench Verified** (vals.ai, Aug 2026):

| Rank | Model | Score |
|:----:|-------|------:|
| 1 | Claude Opus 5 | 97.0% |
| 2 | GPT-5.6 Sol | 96.2% |
| 3 | Grok 4.6 | 95.6% |
| 4 | Claude Fable 5 | 95.0% |
| 5 | Kimi K3 | 93.4% |
| 6 | GPT-5.6 Luna | 93.0% |
| 7 | Claude Opus 4.8 | 88.6% |
| 8 | Grok 4.5 | 86.6% |
| 9 | GLM 5.2 | 82.8% |
| 10 | GPT-5.5 | 82.6% |

---

## Caveats

1. **Harness matters.** SWE-bench scores depend heavily on the agent scaffold (vals.ai uses bash-only mini-swe-agent). Vendor-reported numbers can differ by 10–20 pp from standardized harnesses.
2. **SWE-bench Verified is saturating.** Top models cluster within ~4 points; [SWE-bench Pro](https://benchlm.ai/benchmarks/swe-bench-pro) better differentiates frontier models on long-horizon tasks.
3. **DeepPlanning ≠ software project planning.** It measures constrained travel/shopping planning, but correlates with long-horizon reasoning better than single-shot coding tests.
4. **Fast variants** are not separately benchmarked; scores assume identical model weights.
5. **Scores change.** Re-check sources before making cost/quality decisions.
