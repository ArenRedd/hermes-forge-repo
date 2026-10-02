---
title: Foundations & Architecture
source_phases: [Phase 1]
hermes_version_documented: v0.21.5 (tag v2026.9.24, Sep 24 2026)
research_date: Friday, October 2, 2026
last_built_in: Chat 1
confidence_legend: OFFICIAL = official repo/docs/source; COMMUNITY = third-party; INFERRED = deduced; UNVERIFIED = needs checking
used_by_playbooks: [01-coding-and-dev.md, 02-devops-and-server-admin.md, 03-research-and-analysis.md, 04-content-and-social.md, 05-automation-and-scheduling.md, 06-messaging-gateway-setups.md, 07-browser-and-data-collection.md, 08-multi-agent-and-parallel.md, 09-personal-productivity.md, 10-skill-authoring-and-memory-curation.md, 11-maintenance-backup-recovery.md]
---

# WHEN TO READ THIS FILE
Read this file when you need the fundamental identity of Hermes Agent: what it is, its relationship to Hermes models and Nous Portal, official links, license and governance, release cadence, the complete advertised feature list, how it compares to other agents, the system architecture, repository structure, language/runtime dependencies, and the architecture diagram. This is the grounding context for every other reference file.

---

# TABLE OF CONTENTS
1. [Identity & Context](#1-identity--context)
2. [Official Links](#2-official-links)
3. [Release History](#3-release-history)
4. [Relationship to Hermes Language Models](#4-relationship-to-hermes-language-models)
5. [Advertised Features](#5-advertised-features)
6. [Comparison with Other Agents](#6-comparison-with-other-agents)
7. [Stack & Runtime](#7-stack--runtime)
8. [Repository Structure](#8-repository-structure)
9. [Architecture Internals](#9-architecture-internals)
10. [Architecture Diagram](#10-architecture-diagram)
11. [Conflicts](#11-conflicts)
12. [Gaps](#12-gaps)
13. [Sources](#13-sources)

---

# 1. IDENTITY & CONTEXT

## 1.1 What It Is

| Fact | Detail | Tag |
|------|--------|-----|
| Name and tagline | "Hermes Agent ☤"; repo description "The agent that grows with you" | [OFFICIAL] |
| Maker | Nous Research | [OFFICIAL] |
| Stated purpose | A self-improving agent with a built-in learning loop. It creates skills from experience, improves them in use, nudges itself to persist knowledge, searches past conversations, and builds a model of the user across sessions | [OFFICIAL] |
| Deployment pitch | Runs on a "$5 VPS", a GPU cluster, or serverless infrastructure that is cheap when idle. Not tied to your laptop; you can talk to it from Telegram while it works on a cloud VM | [OFFICIAL] |
| Model policy | "Use any model you want", with no lock-in. Switch with `hermes model` | [OFFICIAL] |
| License | MIT | [OFFICIAL] |
| First release date | **Not verified** (see Section 12) | n/a |
| Release manager | `@teknium1` appears as the releaser on GitHub release pages | [OFFICIAL] |
| Contributors | 450+ community contributors in the v0.19.0 window | [OFFICIAL] |
| GitHub stats (when fetched) | ~239k stars, 48.6k forks, 26,383 commits | [OFFICIAL] |

## 1.2 Governance and Contribution

- The repo has `CONTRIBUTING.md`, `SECURITY.md`, `AGENTS.md`, `.coderabbit.yaml` and a docs Contributing page [OFFICIAL].
- Contributors are told to use the standard installer and work from `$HERMES_HOME/hermes-agent` [OFFICIAL].
- A formal governance document was not found [UNVERIFIED].

## 1.3 Release Cadence

- Minor releases every 2–4 weeks (v0.18.0 Jul 1, v0.19.0 Jul 20, v0.20.0 Aug 3, v0.21.0 Aug 31) with patch tags every few days [INFERRED from OFFICIAL dates].
- Release policy: patch tags ship uncurated; full curated notes deferred to next minor release (stated in release notes) [OFFICIAL].
- Version documented in this research: **v0.21.5, tag `v2026.9.24`, released Sep 24, 2026** [OFFICIAL].

---

# 2. OFFICIAL LINKS

| Resource | URL | Tag |
|----------|-----|-----|
| GitHub | https://github.com/NousResearch/hermes-agent | [OFFICIAL] |
| Docs | https://hermes-agent.nousresearch.com/docs/ | [OFFICIAL] |
| Website and Desktop download | https://hermes-agent.nousresearch.com/ | [OFFICIAL] |
| Install script | https://hermes-agent.nousresearch.com/install.sh | [OFFICIAL] |
| Discord | https://discord.gg/NousResearch | [OFFICIAL] |
| Nous Portal | https://portal.nousresearch.com | [OFFICIAL] |
| Skills hub / open standard | https://agentskills.io | [OFFICIAL] |
| Releases | https://github.com/NousResearch/hermes-agent/releases | [OFFICIAL] |
| Companion repo: self-evolution (DSPy + GEPA) | https://github.com/NousResearch/hermes-agent-self-evolution | [OFFICIAL] |
| Community subreddit r/hermesagent, forum | Listed by third-party awesome list, not independently verified | [COMMUNITY] |
| X/Twitter, Hugging Face org, blog posts | **Not verified** | n/a |

---

# 3. RELEASE HISTORY

| Version | Tag | Date | Notes | Tag |
|---------|-----|------|-------|-----|
| v0.14.0 | v2026.5.16 | May 16, 2026 | "Foundation Release". PyPI package (`pip install hermes-agent`), Teams, LINE and SimpleX; 22 platforms | [OFFICIAL] |
| v0.18.0 | v2026.7.1 | Jul 1 | "Judgment Release". Verification evidence, `/goal` contracts, `/learn`, `/journey` | [OFFICIAL] |
| v0.18.1 / v0.18.2 | v2026.7.7 / .7.2 | Jul 7 | Patch rollups; Baileys WhatsApp dependency fix | [OFFICIAL] |
| v0.19.0 | v2026.7.20 | Jul 20 | "Quicksilver". Cold start ~4.3s → ~0.9s; Bitwarden and 1Password secret sources | [OFFICIAL] |
| v0.19.1 | v2026.7.30 | Jul 30 | Patch rollup | [OFFICIAL] |
| v0.20.0 | v2026.8.3 | Aug 3 | Wake words and hands-free voice | [OFFICIAL] |
| v0.20.1–v0.20.5 | v2026.8.13–8.19 | Aug 13–19 | MCP 2.x SDK migration, Bot Mode, keyless web tier, `hermes update` receipts | [OFFICIAL] |
| v0.21.0 | v2026.8.31 | Aug 31 | Rollup of v0.20.x (tag inferred from a fork's "upstream release" note) | [COMMUNITY] |
| v0.21.1 | v2026.9.7 | Sep 7 | Codebase modularization, MCP authorization | [OFFICIAL] |
| v0.21.4 | v2026.9.21 | Sep 21 | Patch rollup (~1,800 PRs) | [OFFICIAL] |
| **v0.21.5** | **v2026.9.24** | **Sep 24** | **Latest verified**; curated notes deferred to v0.22.0 | [OFFICIAL] |

**Not seen**: v0.21.2, v0.21.3 (a "Sep 14" patch exists) and v0.20.6 as standalone pages.

**Update mechanics** [OFFICIAL]:
- `hermes update` for existing installs
- `pip install -U hermes-agent` appeared in earlier release notes (v0.18.x)
- Current docs call plain `pip install .` unsupported for current releases

---

# 4. RELATIONSHIP TO HERMES LANGUAGE MODELS

- Hermes Agent is a **model-agnostic harness**. The docs say it works with Nous Portal, OpenRouter, OpenAI, Anthropic, Google, local servers and many others [OFFICIAL].
- A Hermes-model-based hackathon (NVIDIA × Stripe × Nous) required a Hermes model, with Nous or an OpenAI-compatible endpoint serving Hermes-4. That shows Hermes models are supported but not mandatory [COMMUNITY].
- The docs' vLLM section lists `--tool-call-parser hermes` as the parser for Hermes 2/3 and Qwen 2.5 tool calling [OFFICIAL].
- Which Hermes model is "recommended" for the agent was **not verified** [UNVERIFIED].

---

# 5. ADVERTISED FEATURES

Everything below is from the README or docs [OFFICIAL] unless marked.

| # | Feature | Detail |
|---|---------|--------|
| 1 | Real TUI | Multiline editing, slash-command autocomplete, history, interrupt-and-redirect, streaming tool output. `hermes --tui` is the modern TUI |
| 2 | Messaging gateway | One process serving Telegram, Discord, Slack, WhatsApp, Signal, Email, and more. Cross-platform continuity and voice-memo transcription |
| 3 | Closed learning loop | Agent-curated memory with nudges, autonomous skill creation, skills that self-improve, FTS5 session search with LLM summarization, Honcho user modeling |
| 4 | Open skills standard | Compatible with agentskills.io; Skills Hub |
| 5 | Cron scheduler | Natural-language scheduled jobs delivered to any platform |
| 6 | Subagents and RPC scripts | Isolated parallel subagents; Python scripts that call tools via RPC |
| 7 | Seven terminal backends | local, docker, ssh, singularity, modal, daytona, vercel_sandbox |
| 8 | Research-ready | Batch trajectory generation, trajectory compression, Atropos RL environments |
| 9 | Nous Portal and Tool Gateway | 300+ models plus web search (Firecrawl), image gen (FAL), TTS (OpenAI), cloud browser (Browser Use) |
| 10 | OpenClaw migration | `hermes claw migrate` |
| 11 | MCP client | `mcp_servers:` in config |
| 12 | ACP server | `hermes acp` for VS Code, Zed, JetBrains |
| 13 | Desktop app | macOS (Apple Silicon only) and Windows |
| 14 | Web dashboard and OpenAI-compatible API server | Port 8642 (API) and 9119 (dashboard) |
| 15 | Profiles | Multiple isolated agents via `hermes -p <name>` |
| 16 | Other | Kanban multi-agent swarm, Bot Mode, `/goal` standing goals, voice mode and wake words, plugins, memory-provider plugins, context-engine plugins, git worktree isolation, checkpoints and rollback, LSP diagnostics on writes (v0.14.0) |

---

# 6. COMPARISON WITH OTHER AGENTS

**[INFERRED].** This table is drawn only from Hermes's own documented capabilities and general knowledge. Treat as hypothesis to verify in later phases.

| Agent | Where Hermes Plausibly Differs | Where the Other May Be Stronger | Verified? |
|-------|-------------------------------|--------------------------------|-----------|
| OpenClaw (Clawdbot/Moltbot-style) | Hermes ships a documented migration command, so the two are close relatives with the same personal-agent pattern | Unknown | Migration only [OFFICIAL] |
| Claude Code, Codex CLI, Aider | Hermes is a general, always-on, multi-platform agent with persistent memory and scheduling. Those tools are coding-focused CLIs | Tighter first-party integration with their own models | [INFERRED] |
| OpenHands, AutoGPT, LangChain agents | Hermes bundles gateway, memory, skills and cron in one runtime | Different ecosystems and eval stories | [INFERRED] |

---

# 7. STACK & RUNTIME

| Item | Detail | Tag |
|------|--------|-----|
| Core language | Python. `pyproject.toml` declares `requires-python = ">=3.11,<3.15"`, but the docs say current first-party installs run on **3.14 only** and every runtime dependency is gated to 3.14 | [OFFICIAL] |
| Package/tool manager | **PM** (a Hermes-internal manager) provisions pinned Python, Node.js, npm, ripgrep, FFmpeg from `pm/lock.json`; the installer bootstraps `uv` | [OFFICIAL] |
| Frontend | `ui-tui/`, `tui_gateway/`, `web/`, `apps/` (Electron desktop), `website/` (Docusaurus docs) | [OFFICIAL] |
| Browser | Installer adds `agent-browser` with pinned Chromium; `cua-driver` for computer use | [OFFICIAL] |
| DB | SQLite with FTS5 (`state.db`), WAL journal by default | [OFFICIAL] |
| Tests | About 25,000 tests across about 1,250 files | [OFFICIAL] |

**Discrepancy to flag** [OFFICIAL]: the GitHub README says the Windows installer handles "Python 3.11", while the docs say Python 3.14. The docs are more recent and more specific, so trust them, but verify with `hermes doctor` on your host.

---

# 8. REPOSITORY STRUCTURE (TOP LEVEL)

| Path | Role | Tag |
|------|------|-----|
| `run_agent.py` | `AIAgent` facade; the loop itself lives in `agent/conversation_loop.py` and `agent/turn_*.py` | [OFFICIAL] |
| `cli.py`, `hermes_cli/` | CLI facade, subcommands, setup wizard, `config.py` (`DEFAULT_CONFIG`, `OPTIONAL_ENV_VARS`), `commands.py` (slash registry), `auth.py` (`PROVIDER_REGISTRY`), `runtime_provider.py` | [OFFICIAL] |
| `model_tools.py`, `toolsets.py`, `tools/` | Tool discovery and dispatch; one file per tool; `tools/registry.py`; terminal backends in `tools/environments/` | [OFFICIAL] |
| `agent/` | `prompt_builder.py`, `context_compressor.py`, `context_engine.py`, `prompt_caching.py`, `auxiliary_client.py`, `memory_manager.py`, `memory_provider.py`, `trajectory.py` | [OFFICIAL] |
| `gateway/` | `run.py` (GatewayRunner), `session.py`, `delivery.py`, `pairing.py`, `hooks.py`, `mirror.py`, `status.py`, `platforms/` | [OFFICIAL] |
| `plugins/` | `plugins/platforms/` (telegram, discord, slack, whatsapp, matrix, email, etc.), `plugins/memory/`, `plugins/context_engine/` | [OFFICIAL] |
| `cron/` | Scheduler (`jobs.py`, `scheduler.py`) | [OFFICIAL] |
| `acp_adapter/` | ACP server | [OFFICIAL] |
| `skills/`, `optional-skills/`, `optional-mcps/` | Bundled and optional skills and MCPs | [OFFICIAL] |
| `hermes_state*.py` | Session DB facade, schema, search, portability | [OFFICIAL] |
| `batch_runner.py`, `trajectory_compressor.py`, `mini_swe_runner.py`, `datagen-config-examples/`, `evals/` | Research and trajectory generation | [OFFICIAL] |
| `docker/`, `Dockerfile`, `docker-compose.yml`, `nix/`, `flake.nix`, `scripts/` | Packaging; `scripts/install.sh` | [OFFICIAL] |
| `cli-config.yaml.example`, `.env.example`, `SOUL.md`, `AGENTS.md` | Example config and identity | [OFFICIAL] |

---

# 9. ARCHITECTURE INTERNALS (CONDENSED FROM OFFICIAL DOC)

- **Agent loop.** One `AIAgent` class serves CLI, gateway, ACP, batch runner and API server. It handles provider selection, prompt build, tool execution, retries, fallback, compression and persistence. The three API modes are `chat_completions`, `codex_responses` and `anthropic_messages` [OFFICIAL].
- **Prompt assembly.** Ordered tiers, `stable` then `context` then `volatile`: identity, tool guidance and skills first; then context files; then memory, profile and timestamp blocks. Design principle: the system prompt does not change mid-conversation, which keeps prompt caches valid [OFFICIAL].
- **Tools.** 70+ tools across about 28 toolsets, self-registering at import time [OFFICIAL]. Backends: terminal (7), browser (5), web (4), MCP (dynamic).
- **Memory layers.** `~/.hermes/memories/` holds `MEMORY.md` and `USER.md`, with char limits (see 02-install-vps-config-basics.md). `SOUL.md` is the identity slot. Skills hold procedural memory. FTS5 search over past sessions provides recall. Pluggable memory providers (single-select) include Honcho, Mem0, Hindsight, Supermemory and others [OFFICIAL].
- **Skills.** `SKILL.md` files; only short descriptions are loaded until a task needs the full text. Every installed skill becomes a slash command [OFFICIAL].
- **Gateway.** One long-running process with 25+ adapters, per-chat session routing, allowlists and DM pairing, slash commands, hooks, the cron tick (every 60s) and maintenance [OFFICIAL].
- **Cron.** Jobs live in `jobs.json`. Each run creates a fresh `AIAgent` with no history, injects attached skills, runs the prompt, and delivers to the target platform [OFFICIAL].
- **Subagents.** `delegate_task`. Docker-backend subagents share the parent's container [OFFICIAL].
- **Context compression.** Default engine is lossy summarization at 50% of the context window. A separate "auxiliary" model does the summarizing, and it must have a context window at least as large as the main model's, or the middle turns are silently dropped [OFFICIAL].
- **Session storage.** SQLite with lineage tracking. A delivery ledger redelivers final replies after a crash [OFFICIAL].
- **Trajectories.** ShareGPT-format export for training data [OFFICIAL].
- **Logs.** `~/.hermes/logs/` (`agent.log`, `errors.log`, `gateway.log`), with secrets auto-redacted [OFFICIAL].

---

# 10. ARCHITECTURE DIAGRAM (FROM OFFICIAL DOC, CONDENSED)

```text
Entry points: CLI | Gateway | ACP | Batch runner | API server | Python lib
                       │
                       ▼
        AIAgent (run_agent.py)
   ┌─ Prompt builder ── Provider resolution ── Tool dispatch (model_tools.py)
   │  Compression/caching   3 API modes          Tool registry: 70+ tools, ~28 toolsets
   └────────────┬──────────────────────────────────────┬──────────
                ▼                                      ▼
   Session storage (SQLite + FTS5)         Tool backends: Terminal (7), Browser (5),
   hermes_state.py                         Web (4), MCP, File, Vision, ...

Cron:    scheduler tick → jobs.json → fresh AIAgent → deliver → update next_run
Gateway: platform event → adapter → authorize → session key → AIAgent → deliver
```

---

# 11. CONFLICTS

| Item | Phase 1 Says | Phase 2 Says | Resolution |
|------|--------------|--------------|------------|
| Python version | `pyproject.toml`: `>=3.11,<3.15`; **docs: Python 3.14 only** | Not restated | Both recorded. Runtime = 3.14 per docs. |
| Provider count | Quickstart: ~40 providers | Architecture page: "18+"; quickstart newer | Use ~40; note discrepancy. |
| First release date | Not verified | Not mentioned | Mark UNVERIFIED in gaps. |
| Governance doc | Not found | Not mentioned | Mark UNVERIFIED in gaps. |

---

# 12. GAPS

| Gap | Description | Suggested Resolution |
|-----|-------------|----------------------|
| First release date | Not found in any fetched page | Search repo's first tag, launch announcement |
| Maintainers beyond `@teknium1` | Only releaser handle known | Check CODEOWNERS, CONTRIBUTING.md |
| Nous Research blog/X/HF org links | Not verified | Search "Nous Research Hermes Agent blog" |
| Competitor comparison | Only OpenClaw migration verified | Research Reddit, Discord, HN |
| Platform Support distro list | Not read | Fetch Platform Support page |
| Full config schema | ~70 keys captured; `cli-config.yaml.example` and `DEFAULT_CONFIG` not fetched | Fetch in Chat 2 |
| Personality presets list | Not found | Fetch `/personality` source or CLI guide |
| Context file load order | Not stated | Fetch `docs/user-guide/features/context-files` |

---

# 13. SOURCES

- https://github.com/nousresearch/hermes-agent (repo page, README, file tree)
- https://hermes-agent.nousresearch.com/docs/developer-guide/architecture
- https://github.com/NousResearch/hermes-agent/releases (plus tag pages: v2026.5.16, v2026.7.1, v2026.7.7, v2026.7.7.2, v2026.7.20, v2026.7.30, v2026.8.16.2, v2026.8.18, v2026.8.19, v2026.9.7)
- https://github.com/NousResearch/hermes-agent/releases/tag/v2026.5.16
- https://www.gradually.ai/en/changelogs/hermes-agent/ and https://releasebot.io/updates/nousresearch/hermes-agent [COMMUNITY aggregators]
- https://github.com/NousResearch/hermes-agent-self-evolution

---

FILE COMPLETE: hermes-forge/references/01-foundations-architecture.md
Main tables: Identity (9), Official Links (10), Release History (12), Advertised Features (16), Comparison (3), Stack/Runtime (6), Repo Structure (14), Architecture Internals (10 items), Diagram (1). Gaps: 8 items. Conflicts: 4 items.