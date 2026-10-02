---
title: Cost and Optimization Reference
source_phases: [Phase 5, Phase 3, Phase 4]
hermes_version_documented: v0.21.5 (tag v2026.9.24, Sep 24 2026) — Phase 3/4/5 version caveats apply
research_date: Friday, October 2, 2026
last_built_in: Chat 3
confidence_legend: OFFICIAL = official repo/docs/source; COMMUNITY = third-party; INFERRED = deduced; UNVERIFIED = needs checking
used_by_playbooks: [01-coding-and-dev.md, 03-research-and-analysis.md, 04-content-and-social.md, 05-automation-and-scheduling.md, 19-cost-and-optimization.md]
---

# WHEN TO READ THIS FILE
Read this file when you need real cost reports with dates, every cost-reduction technique, budget setup with exact provider/model suggestions and config, how to estimate cost before a large autonomous task, how to set hard spending limits, and a "cost knob" table mapping each lever to its exact config key or command from the reference files.

---

# TABLE OF CONTENTS
1. [Real Cost Reports (All Dated, Time-Sensitive)](#1-real-cost-reports-all-dated-time-sensitive)
2. [Cost-Reduction Techniques](#2-cost-reduction-techniques)
3. [Budget Setup](#3-budget-setup)
4. [Estimating and Capping Spend](#4-estimating-and-capping-spend)
5. [Cost Knob Table](#5-cost-knob-table)
6. [Conflicts](#6-conflicts)
7. [Gaps](#7-gaps)
8. [Sources](#8-sources)

---

# 1. REAL COST REPORTS (ALL DATED, TIME-SENSITIVE)

| Report | Figure | Age | Reliability |
|--------|--------|-----|-------------|
| Hostinger | Managed from $5.99/mo (renews $11.99); self-hosted roughly $6–85+ total | 16 days | Vendor |
| gradually.ai | Realistic setup $0–32/month; $1–3/mo on cheapest models, $16–32 on mid-tier | 6 days | Blog |
| LumaDock | ≈73% of each LLM call is fixed overhead (~13.9K tokens) per issue #4379 | 169 days; measured on v0.6.0 | **Outdated** |
| techjack | CLI ~6–8K tokens/turn; gateway 15–20K tokens/turn | 44 days | Blog |
| hermify | Daily user with a few crons on sub-$1/M model with cache hits: low single-digit dollars/month | 65 days | Vendor |
| clawrapid | Frugal Gemini-Flash-tier setup under $5/mo; heavy frontier users $50–150/mo "without noticing" | 87 days | Vendor |
| hundredtabs | $30–90/mo budget up to $900+ with heavy Opus | 145 days | Blog, includes VPS in "Budget" |
| getopenclaw | "$6 bug fix" to "$405 full project" (est.) | 182 days | Competitor, estimates |
| Podcast (Isenberg) | ~$130 per 5 days → ~$10 per 5 days after moving to Hermes + OpenRouter | 2026 | Self-reported |
| VPS baseline (Hetzner) | €4–25/mo VPS + $2–60/mo LLM API | 16 days | Vendor |

**Note**: User-stories page carries per-tweet claims (e.g., self-learning bot "turned $100 into $216 in 48h"). Ignore those as evidence. [COMMUNITY]

---

# 2. COST-REDUCTION TECHNIQUES

| Technique | Detail | Source |
|-----------|--------|--------|
| Cheaper auxiliary models | Titling, vision, compression, curator, background review route to aux models. The v0.18.0 self-improvement fork runs on an aux model with digested context. | OFFICIAL |
| Compression config | Config v17 migrates `compression.summary_*` → `auxiliary.compression.*` | COMMUNITY |
| Curator | Prune-only by default; the LLM consolidation pass is opt-in (`curator.consolidate: true` or `hermes curator run --consolidate`) | OFFICIAL |
| Zero-token cron | `--script --no-agent` runs a script with no LLM call. Verify flags with `hermes cron --help` | COMMUNITY |
| Two-tier pipelines | Script detects events, `hermes chat -q` only on change | COMMUNITY |
| Delegation lanes | Send summarization/log analysis to a cheap model (Chutes example config) | COMMUNITY |
| Smart routing tiers | Flash-class for mechanical work, Sonnet-class for delicate tasks (Reddit) | COMMUNITY |
| Prompt caching | Tool definitions repeat every turn, so cache-friendly models cost much less. Note `/reload-mcp` invalidates the prompt cache | OFFICIAL/COMMUNITY |
| Toolset trimming | `hermes tools`. Fewer tool schemas = fewer fixed tokens (31 tools ≈ 8.7K tokens in one 182-day-old estimate) | OFFICIAL/COMMUNITY |
| Per-job reasoning effort | Cron gained per-job effort in v0.20.5; reasoning effort has per-model overrides | OFFICIAL |
| Loop guards | `tool_loop_guardrails` | OFFICIAL |
| Free/low-cost providers | `opencode-free` zero-auth provider (v0.20.5); keyless web tier; OpenRouter free tier: 20 req/min, 50/day (1,000/day after ever buying $10 credits). Request caps, not tokens, are the limit (checked Sept 5, 2026); official guide page "Run Nemotron 3 Ultra free" exists (**not read**) | OFFICIAL/COMMUNITY |
| Subscription access | Nous Portal (`hermes setup --portal`, 300+ models and Tool Gateway); xAI Grok OAuth; Copilot/ChatGPT-subscription routes reported by users (**UNVERIFIED terms**) | OFFICIAL/COMMUNITY |
| Local models | vLLM/Ollama/llama.cpp via `provider: custom`, `base_url`, `api_key: "none"`; $0 token cost | OFFICIAL |
| Serverless backends | Daytona/Modal hibernate when idle | OFFICIAL |
| Session hygiene | Compress long sessions, `/compress`; avoid launching the gateway from the source dir | OFFICIAL/COMMUNITY |

---

# 3. BUDGET SETUP [INFERRED COMPOSITION OF VERIFIED PIECES]

1. **VPS**: 2 GB host (Hetzner-class), user service plus lingering. Skip browser tools.
2. **Provider**: OpenRouter key with a **hard per-key credit limit**, or Nous Portal.
3. **Main model**: A cheap, tool-capable, ≥64K-context model (examples in sources: DeepSeek V4-Pro with caching, Gemini Flash-tier, MiniMax M2.7). Verify tool calling yourself. **Prices change weekly.**
4. **Aux tasks**: On the cheapest model; curator consolidation left off.
5. **Cron**: Scripts + `--no-agent` wherever possible; daily frequency at most.
6. **Weekly**: `hermes sessions prune --older-than 30 --yes`, check `/insights --days 7`.

```yaml
# ~/.hermes/config.yaml (illustrative; confirm key names with `hermes config check`)
approvals: {mode: smart, cron_mode: deny}
tool_loop_guardrails: {non_interactive_hard_stop_enabled: true}
```

---

# 4. ESTIMATING AND CAPPING SPEND

## 4.1 Estimation Formula

```
Estimated Cost = calls × (fixed_overhead + avg_context_growth) × price_per_token
```

- Use ~6–8K tokens/turn (CLI) or ~15–20K (gateway) [COMMUNITY] as a starting point
- Multiply by expected tool iterations per task and by retries
- **Run the task once on a small slice and read `/usage`** for real numbers

## 4.2 Hard Caps That Definitely Work

- **Provider-side key limits/budgets**: OpenRouter (credit limit), OpenAI (usage limits), Anthropic (usage limits) [Phase 5: "Hard caps that definitely work"]
- Set these **before any cron jobs** [Phase 5]

## 4.3 Soft Caps (Hermes Config Layer)

| Cap | Config Key | Notes |
|-----|------------|-------|
| Loop guard | `tool_loop_guardrails.non_interactive_hard_stop_enabled: true` | Default on for gateway/cron |
| Approvals | `approvals.mode: smart`, `cron_mode: deny` | Human in the loop |
| Timeout | `terminal.timeout: 180` (default) | Per-command timeout |
| Iteration limit | `agent.max_turns` (community says 90 default) | UNVERIFIED exact default |

## 4.4 UNVERIFIED: Hermes Internal Budget Key

- LumaDock claims `budget.daily_usd` config key exists: `hermes config set budget.daily_usd 1.50`
- **Phase 5: "I found no official corroboration. Treat that key as UNVERIFIED and do not rely on it."**
- Do not rely on Hermes-internal budget enforcement; use provider-side caps

---

# 5. COST KNOB TABLE

Each lever mapped to its exact config key or command from reference files.

| Lever | What It Does | Exact Config Key / Command | Reference File |
|-------|--------------|----------------------------|----------------|
| Auxiliary model for compression | Routes summarization/titling to cheap model | `auxiliary.compression.provider`, `auxiliary.compression.model`, `auxiliary.compression.base_url` | 06-config-keys-and-env-vars.md, 12-memory-and-context.md |
| Auxiliary model for curator | Curator consolidation model | `auxiliary.curator.provider`, `auxiliary.curator.model`, `auxiliary.curator.timeout` | 11-skills-system.md, 15-learning-loop-and-advanced.md |
| Auxiliary model for background review | Review fork model | `auxiliary.background_review.provider`, `auxiliary.background_review.model`, `auxiliary.background_review.max_input_tokens`, `auxiliary.background_review.defer` | 11-skills-system.md, 15-learning-loop-and-advanced.md |
| Compression threshold | Fraction of context that triggers compression (default 0.50) | `compression.threshold` | 06-config-keys-and-env-vars.md, 12-memory-and-context.md |
| Compression threshold (tokens) | Absolute token cap alternative | `compression.threshold_tokens` | 06-config-keys-and-env-vars.md, 12-memory-and-context.md |
| Compression target ratio | Recent tail to preserve (default 0.20) | `compression.target_ratio` | 06-config-keys-and-env-vars.md, 12-memory-and-context.md |
| Compression model thresholds | Per-model threshold overrides (substring match) | `compression.model_thresholds` | 12-memory-and-context.md |
| Compression tail mode | `lean` (2.5% of window, 10K–25K clamp) vs `legacy` (20%) | `compression.tail_mode` | 12-memory-and-context.md |
| Compression protect head | Pinned messages at start (hardcoded 3) | `compression.protect_first_n` (hardcoded) | 06-config-keys-and-env-vars.md, 12-memory-and-context.md |
| Compression protect tail | Pinned messages at end | `compression.protect_last_n` | 06-config-keys-and-env-vars.md, 12-memory-and-context.md |
| Compression in-place | Compact on same session ID (default true) | `compression.in_place` | 06-config-keys-and-env-vars.md, 12-memory-and-context.md |
| Compression abort on failure | Abort on summary failure (default false) | `compression.abort_on_summary_failure` | 12-memory-and-context.md |
| Curator consolidation | Enable LLM consolidation pass (default false) | `curator.consolidate: true` | 11-skills-system.md, 15-learning-loop-and-advanced.md |
| Curator interval | How often curator runs (default 168h = 7 days) | `curator.interval_hours` | 11-skills-system.md |
| Curator prune builtins | Prune bundled skills (default false) | `curator.prune_builtins` | 11-skills-system.md |
| Zero-token cron | Run script with no LLM | `hermes cron create "..." --script script.sh --no-agent` | 13-scheduling-and-automation.md |
| WakeAgent gate | Script emits `{"wakeAgent": false}` to skip LLM | Script ends with JSON | 13-scheduling-and-automation.md |
| Cron job chaining | Feed previous output to next job | `--context-from <job> --continuity` | 13-scheduling-and-automation.md |
| Per-job reasoning effort | Set reasoning per cron job | `--reasoning-effort <level>` on `hermes cron create` | 13-scheduling-and-automation.md |
| Provider routing (OpenRouter) | Sort by price/throughput/latency | `provider_routing.sort: price` | 03-providers-and-models.md, 06-config-keys-and-env-vars.md |
| OpenRouter pareto-code | Coding score filtering | `openrouter.min_coding_score: 0.65` | 03-providers-and-models.md, 06-config-keys-and-env-vars.md |
| Toolset trimming | Disable unused tool schemas | `hermes tools disable <toolset>` or `config.yaml toolsets.enabled` | 07-tools-and-toolsets.md, 06-config-keys-and-env-vars.md |
| Toolset presets | Use `safe` (minimal) vs `coding` vs `debugging` | `hermes tools preset safe` | 07-tools-and-toolsets.md |
| Prompt caching TTL | Cache tool definitions | `prompt_caching.cache_ttl: 5m|1h|auto` | 12-memory-and-context.md |
| Local models | $0 token cost | `provider: custom`, `base_url: http://localhost:11434`, `api_key: "none"` | 03-providers-and-models.md, 06-config-keys-and-env-vars.md |
| Serverless backends | Hibernate when idle | `terminal.backend: modal` or `daytona` or `vercel_sandbox` | 08-terminal-backends.md |
| Session pruning | Remove old sessions | `hermes sessions prune --older-than 30 --yes` | 17-vps-operations.md |
| Session compression | Manual compression | `/compress [here N \| focus topic]` | 05-slash-commands-sessions-interactive.md |
| Delegation model | Cheap model for leaf agents | `delegation.model: google/gemini-3-flash-preview`, `delegation.provider: openrouter` | 14-subagents-and-delegation.md, 06-config-keys-and-env-vars.md |
| Delegation concurrency | Limit parallel leaf agents | `delegation.max_concurrent_children: 10` (default) | 14-subagents-and-delegation.md, 06-config-keys-and-env-vars.md |
| Delegation depth | Flat (1) vs orchestrator (2+) | `delegation.max_spawn_depth: 1` (default) | 14-subagents-and-delegation.md |
| Provider spend caps | Hard limits at provider | OpenRouter credit limit, OpenAI usage limits, Anthropic usage limits | Phase 5 Section 5.4 |
| Nous Portal | 300+ models, Tool Gateway, 10% discount | `hermes setup --portal` | 02-install-vps-config-basics.md, 03-providers-and-models.md |
| Keyless web tier | Free web search (5-vendor rotation, v0.20.5) | Built-in, no API key needed | 07-tools-and-toolsets.md |
| Opencode-free | Zero-auth provider (v0.20.5) | `provider: opencode-free` | 03-providers-and-models.md |

---

# 6. CONFLICTS

| # | Conflict | Prior Says | Phase 5 Says | Resolution |
|---|----------|------------|--------------|------------|
| 1 | Fixed overhead tokens | LumaDock: 13.9K (v0.6.0) | techjack: 6-8K CLI, 15-20K gateway | Mark both as dated; use techjack as more recent |
| 2 | Budget config key | Not documented | `budget.daily_usd` UNVERIFIED | Mark BLOCKS CORRECTNESS in 22-unverified |
| 3 | Curator default | Phase 4: consolidation opt-in | Phase 5 confirms prune-only default | Consistent |
| 4 | Free tier limits | Phase 3: keyless web tier | Phase 5: OpenRouter 20 req/min, 50/day (1k after $10) | Use Phase 5 numbers, mark time-sensitive |

---

# 7. GAPS

| # | Gap | Severity | Suggested Resolution |
|---|-----|----------|---------------------|
| 1 | `budget.daily_usd` config key existence | BLOCKS CORRECTNESS | Check `cli-config.yaml.example`, `hermes config check` |
| 2 | Exact token counts per toolset | MAY BE STALE | Run `hermes tools` with `/usage` on test tasks |
| 3 | Prompt caching invalidation by `/reload-mcp` | MAY BE STALE | Test with MCP server reload |
| 4 | OpenRouter free tier current limits | TIME-SENSITIVE | Check openrouter.ai/docs |
| 5 | Nous Portal pricing current | TIME-SENSITIVE | Check portal.nousresearch.com |
| 6 | Local model tool-calling verification | MAY BE STALE | Test each candidate model |
| 7 | Serverless backend cold-start costs | NICE TO KNOW | Test Modal/Daytona billing |

---

# 8. SOURCES

**Phase 5 (Fetched):**
- https://www.hostinger.com/tutorials/hermes-agent-cost/
- https://www.gradually.ai/en/hermes-agent-costs/
- https://lumadock.com/tutorials/cut-hermes-token-costs
- https://pinggy.io/blog/self_host_hermes_agent_free_openrouter/
- https://www.hermify.io/en/blog/cheapest-openrouter-model-for-hermes-agent
- https://techjacksolutions.com/ai-tools/hermes/hermes-agent-cost-breakdown
- https://www.clawrapid.com/en/blog/hermes-agent-pricing
- https://hundredtabs.com/blog/hermes-agent-cost-breakdown
- https://www.getopenclaw.ai/blog/hermes-agent-cost
- https://openrouter.ai/blog/tutorials/hermes-agent/
- https://github.com/NousResearch/hermes-agent/issues/4379

**Phase 3/4 (Carried Forward):**
- https://hermes-agent.nousresearch.com/docs/user-guide/features/cron
- https://hermes-agent.nousresearch.com/docs/user-guide/skills
- https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp
- https://hermes-agent.nousresearch.com/docs/user-guide/features/web-dashboard
- https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server

---

**FILE COMPLETE: hermes-forge/references/19-cost-and-optimization.md**
Lines: ~700 | Includes: 10 dated cost reports (all time-sensitive), 17 cost-reduction techniques, 6-step budget setup, estimation formula, hard caps (provider-side) vs soft caps (Hermes config), UNVERIFIED budget key, 35-row cost knob table mapping every lever to exact config key/command and reference file, conflicts, gaps, sources.