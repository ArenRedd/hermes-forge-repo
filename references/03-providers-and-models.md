---
title: Model Providers and Selection
source_phases: [Phase 1]
hermes_version_documented: v0.21.5 (tag v2026.9.24, Sep 24 2026)
research_date: Friday, October 2, 2026
last_built_in: Chat 1
confidence_legend: OFFICIAL = official repo/docs/source; COMMUNITY = third-party; INFERRED = deduced; UNVERIFIED = needs checking
used_by_playbooks: [01-coding-and-dev.md, 03-research-and-analysis.md, 04-content-and-social.md, 05-automation-and-scheduling.md, 08-multi-agent-and-parallel.md, 19-cost-and-optimization.md]
---

# WHEN TO READ THIS FILE
Read this file when you need to configure model providers, switch models, set up fallback chains, use auxiliary models, understand routing features, handle context windows/cost/rate limits, run local models on a VPS, or optimize for budget. Every provider, config key, env var, and command for model management is here.

---

# TABLE OF CONTENTS
1. [Providers Overview](#1-providers-overview)
2. [Per-Provider Setup](#2-per-provider-setup)
3. [Switching, Fallback & Routing](#3-switching-fallback--routing)
4. [Recommended Models by Job](#4-recommended-models-by-job)
5. [Context, Cost & Rate Limits](#5-context-cost--rate-limits)
6. [Local Models on a VPS](#6-local-models-on-a-vps)
7. [Low-Budget Tips](#7-low-budget-tips)
8. [Conflicts](#8-conflicts)
9. [Gaps](#9-gaps)
10. [Sources](#10-sources)

---

# 1. PROVIDERS OVERVIEW

- The quickstart table lists **about 40 provider paths** [OFFICIAL].
- The architecture page says "18+ providers"; the quickstart table is newer [OFFICIAL].
- Providers include: Nous Portal, OpenAI Codex (ChatGPT subscription), Anthropic, OpenRouter, GitHub Copilot, AWS Bedrock, Azure Foundry, Google AI Studio and Vertex, xAI, Hugging Face, DeepSeek, Z.AI, Kimi, MiniMax, Qwen/Alibaba, NVIDIA NIM, Ollama Cloud, LM Studio, Custom Endpoint, and others.

---

# 2. PER-PROVIDER SETUP

| Provider | Setup | Tag |
|----------|-------|-----|
| Nous Portal | `hermes setup --portal` or `hermes model`; check with `hermes portal info` | [OFFICIAL] |
| OpenRouter | `OPENROUTER_API_KEY` in `~/.hermes/.env` | [OFFICIAL] |
| Anthropic | `ANTHROPIC_API_KEY` (pay-per-token), or OAuth via `hermes model`. **OAuth needs Claude Max plus purchased extra usage credits; it does not work on Claude Pro** | [OFFICIAL] |
| OpenAI direct | `OPENAI_API_KEY` (provider `openai-api`) | [OFFICIAL] |
| OpenAI Codex | `hermes model` then "ChatGPT or Codex Subscription" (device-code login). Over SSH the browser flow needs a tunnel: `ssh -N -L 1455:127.0.0.1:1455 user@host` | [OFFICIAL] |
| Hugging Face | `HF_TOKEN`; provider `huggingface`; routing suffixes `:fastest`, `:cheapest` | [OFFICIAL] |
| Custom/self-hosted | `hermes model` then "Custom endpoint", or the YAML below | [OFFICIAL] |

## 2.1 Custom Endpoint YAML

```yaml
model:
  default: your-model-name
  provider: custom
  base_url: http://localhost:8000/v1
  api_key: your-key-or-leave-empty-for-local
```

## 2.2 Anthropic Example

```bash
export ANTHROPIC_API_KEY=***
hermes chat --provider anthropic --model claude-sonnet-4-6
```

## 2.3 Removed Env Var

`LLM_MODEL` in `.env` is **removed**; `config.yaml` is the source of truth [OFFICIAL].

---

# 3. SWITCHING, FALLBACK & ROUTING

## 3.1 Terminal Wizard
- `hermes model` adds or switches providers.

## 3.2 In-Chat (Already-Configured Providers Only)
- `/model [provider:model]`
- Variants:
  - `/model <name> --global` writes to `config.yaml`
  - `--once` applies for a single turn
- Gateway `/model` overrides survive restarts.
- Named custom providers: `/model custom:<name>:<model>`

**Examples**:
```
/model claude-sonnet-4
/model zai:glm-5
/model custom:local:qwen-2.5
/model claude-sonnet-4 --global
```

**Flags**: `--global`, `--session`, `--once`, `--refresh`, `--provider <name>`, `--reasoning <level>`
- Switching is session-only unless `--global` or `model.persist_switch_by_default: true`.
- A switch resets the prompt cache.
- Aliases: `hermes config set model.aliases.fav anthropic/claude-opus-4.6`

## 3.3 Per-Channel Overrides
```yaml
platforms.<name>.channel_overrides:
  model: <model>
  provider: <provider>
  system_prompt: <custom prompt>
```

## 3.4 One-Off CLI
```bash
hermes chat --provider <p> --model <m> -q "..."
```

## 3.5 Fallback Chain

```yaml
fallback_providers:
  - provider: openrouter
    model: anthropic/claude-sonnet-4
  - provider: anthropic
    model: claude-sonnet-4
```

- The legacy `fallback_model:` dict still works.
- Each fallback activation is **one-shot per session**.
- Set `agent.api_max_retries: 0` to fail over faster [OFFICIAL].

## 3.6 Auxiliary Models
- Vision, web summarization, MoA and compression use a separate "auxiliary" model.
- By default (`auto`) that is your main model.
- Override per task:
  - `auxiliary.compression.provider`
  - `auxiliary.compression.model`
- **The summarizer's context window must be at least as large as the main model's** [OFFICIAL].

## 3.7 OpenRouter Routing
- `provider_routing` config: `sort` (`price`, `throughput`, `latency`), `only`, `ignore`, `order`, `data_collection`
- Model suffixes: `:nitro`, `:floor`
- `openrouter/pareto-code` with `openrouter.min_coding_score`

## 3.8 Credential Pools & Named Provider Keys
- `providers.<id>.key_env` — env var name for the key
- `providers.<id>.key_cmd` — command to generate short-lived tokens

---

# 4. RECOMMENDED MODELS BY JOB

**⚠ NOT VERIFIED** — The docs do not give a ranking, and no benchmarks or community consensus were pulled [UNVERIFIED].

Items seen in docs examples (these are examples, not endorsements):
- `anthropic/claude-sonnet-4`
- `claude-sonnet-4-6`
- `gpt-5.4`
- `glm-5`
- `MiniMax-M2.7`
- `qwen3-coder-plus`
- `kimi-k2.5`
- `nvidia/nemotron-3-super-120b-a12b`

Docs navigation lists a guide titled "Run Nemotron 3 Ultra free" (not read).
v0.20.5 notes mention a zero-auth `opencode-free` provider and a keyless web-search tier (not tested).

---

# 5. CONTEXT, COST & RATE LIMITS

## 5.1 Minimum Context
- **Minimum context: 64,000 tokens** for any model, or it is rejected at startup [OFFICIAL].

## 5.2 Context Detection Chain (9 Steps) [OFFICIAL]
1. Config pin (`model.context_length`)
2. Per-model setting
3. Cache
4. Endpoint `/models`
5. Anthropic
6. OpenRouter
7. Nous
8. models.dev
9. 128K fallback

## 5.3 Cost & Usage Visibility
- `/usage` — current session
- `/insights [--days N]` — historical analytics

## 5.4 Rate-Limit Handling [OFFICIAL]
- Retries: `agent.api_max_retries: 3` (default)
- Fallback chain (Section 3.5)
- Auto-recovery ladder for outages: jittered 15/30/60/60/60s
- Honors `Retry-After` up to 120s

## 5.5 Cost Levers

| # | Lever | Detail |
|---|-------|--------|
| 1 | Auxiliary models | Point `auxiliary.compression` and vision at a cheap model [DOCUMENTED; specific model choice INFERRED] |
| 2 | Compression threshold | Tune `compression.threshold` or `compression.threshold_tokens` (absolute token cap) |
| 3 | Proactive pruning | Opt in to `compression.proactive_prune_tokens` (docs suggest trying `48000`) |
| 4 | OpenRouter price routing | `provider_routing.sort: price` or `:floor` suffix |
| 5 | Disable unused tools | `hermes tools` or `agent.disabled_toolsets` |
| 6 | Cap iterations | `agent.max_turns` and `goals.max_turns` |
| 7 | Run budget | `agent.run_budget_seconds` for bounded runs |
| 8 | Nous Portal discount | Bills 10% less on token-billed providers, per config page |

---

# 6. LOCAL MODELS ON A VPS

## 6.1 Supported Servers [OFFICIAL]
Custom Endpoint for: Ollama, vLLM, SGLang, llama.cpp, LM Studio, LiteLLM, and others.

## 6.2 Ollama Context Fix [OFFICIAL]
Ollama defaults to 4,096-token context below 24 GB VRAM, which Hermes rejects. Fixes:
- `OLLAMA_CONTEXT_LENGTH=64000 ollama serve`
- `PARAMETER num_ctx 64000` in a Modelfile
- `model.ollama_num_ctx` in config

## 6.3 Tool Calling Server Flags [OFFICIAL]
- **llama.cpp**: `--jinja`
- **vLLM**: `--enable-auto-tool-choice --tool-call-parser hermes` (or another parser)
- **SGLang**: `--tool-call-parser qwen`

## 6.4 llama.cpp Context
- Needs `-c 64000` or more.
- With parallel slots (`-np`), each slot's share must still be above the minimum.

## 6.5 Docker Networking
- Inside the container, use the container name, not `localhost`.

## 6.6 Hardware Realism [INFERRED]
- The docs give no CPU-only VPS guidance.
- Expectation: a cheap CPU-only VPS cannot serve a 64K-context tool-calling model at usable speed, so API providers are the practical choice on small VPSes.

---

# 7. LOW-BUDGET TIPS

1. **Use Nous Portal** — 10% discount on token-billed providers.
2. **Route via OpenRouter** with `sort: price` or `:floor` models.
3. **Offload compression/vision** to a cheap auxiliary model (`auxiliary.compression.provider/model`).
4. **Tune compression** — raise `threshold`, set `proactive_prune_tokens: 48000`.
5. **Disable toolsets** you don't need (`agent.disabled_toolsets`).
6. **Cap turns** — `agent.max_turns`, `goals.max_turns`.
7. **Use `hermes -z`** for one-shot tasks (no session overhead).
8. **Set `agent.run_budget_seconds`** for hard time limits.
9. **Prefer `hermes chat --oneshot`** over interactive for automation.
10. **Monitor with `/usage` and `/insights`** regularly.

---

# 8. CONFLICTS

| Item | Phase 1 Says | Phase 2 Says | Resolution |
|------|--------------|--------------|------------|
| Provider count | ~40 (quickstart) | Architecture: 18+; quickstart newer | Use ~40; note discrepancy. |
| Model recommendations | None (UNVERIFIED) | Not mentioned | Mark UNVERIFIED in gaps. |
| `LLM_MODEL` env | Removed; config.yaml is truth | Same | Consistent. |
| Fallback format | `fallback_providers:` list | Same | Consistent. |
| Auxiliary context req | Summarizer window ≥ main | Not restated | Phase 1 authoritative. |

---

# 9. GAPS

| Gap | Description |
|-----|-------------|
| Model benchmarks/rankings | No official recommendations; community consensus not researched |
| Full provider list (all ~40) | Quickstart table truncated in fetch; need complete list |
| Nous Portal Tool Gateway details | 300+ models, web search, image gen, TTS, cloud browser — specifics not fetched |
| Custom endpoint auth patterns | `key_env`, `key_cmd` mentioned but not detailed |
| Provider routing `provider_routing` full schema | Only subset captured |
| Local model CPU-only VPS guidance | None in docs; marked INFERRED |
| Anthropic OAuth credit requirements | "Max plus extra credits" — exact threshold not specified |
| OpenRouter `:nitro`/`:floor` details | Suffixes mentioned; behavior not detailed |

---

# 10. SOURCES

- https://hermes-agent.nousresearch.com/docs/integrations/providers
- https://hermes-agent.nousresearch.com/docs/getting-started/quickstart
- https://hermes-agent.nousresearch.com/docs/user-guide/configuration
- https://hermes-agent.nousresearch.com/docs/reference/environment-variables

---

FILE COMPLETE: hermes-forge/references/03-providers-and-models.md
Main tables: Providers Setup (7), Fallback YAML (1), Auxiliary Models (1), Cost Levers (8), Local Model Fixes (4), Low-Budget Tips (10). Gaps: 8 items. Conflicts: 1 (provider count).