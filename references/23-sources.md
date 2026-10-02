---
title: Sources Master List (v2 — Chat 1 + Chat 2)
source_phases: [Phase 1, Phase 2, Phase 3, Phase 4]
hermes_version_documented: v0.21.5 (tag v2026.9.24, Sep 24 2026) — Phase 3/4 version not pinned; docs track `main`
research_date: Friday, October 2, 2026
last_built_in: Chat 2
confidence_legend: OFFICIAL = official repo/docs/source; COMMUNITY = third-party; INFERRED = deduced; UNVERIFIED = needs checking
used_by_playbooks: []
---

# WHEN TO READ THIS FILE
This is the deduplicated master list of all sources cited in all research phases, plus repo file paths worth inspecting. Each reference file in `references/` ends with a Sources list pointing back to this master list.

---

# OFFICIAL REPO & RELEASES

| ID | Source | Type | URL | Used By |
|----|--------|------|-----|---------|
| S01 | GitHub Repo | Official | https://github.com/NousResearch/hermes-agent | All files |
| S02 | GitHub Releases | Official | https://github.com/NousResearch/hermes-agent/releases | 01, 02, 03, 04, 05, 06, 22, 23 |
| S03 | Release Tag v2026.5.16 | Official | https://github.com/NousResearch/hermes-agent/releases/tag/v2026.5.16 | 01, 22 |
| S04 | Release Tag v2026.7.1 | Official | https://github.com/NousResearch/hermes-agent/releases/tag/v2026.7.1 | 01, 22 |
| S05 | Release Tag v2026.7.7 | Official | https://github.com/NousResearch/hermes-agent/releases/tag/v2026.7.7 | 01, 22 |
| S06 | Release Tag v2026.7.7.2 | Official | https://github.com/NousResearch/hermes-agent/releases/tag/v2026.7.7.2 | 01, 22 |
| S07 | Release Tag v2026.7.20 | Official | https://github.com/NousResearch/hermes-agent/releases/tag/v2026.7.20 | 01, 22 |
| S08 | Release Tag v2026.7.30 | Official | https://github.com/NousResearch/hermes-agent/releases/tag/v2026.7.30 | 01, 22 |
| S09 | Release Tag v2026.8.16.2 | Official | https://github.com/NousResearch/hermes-agent/releases/tag/v2026.8.16.2 | 01, 22 |
| S10 | Release Tag v2026.8.18 | Official | https://github.com/NousResearch/hermes-agent/releases/tag/v2026.8.18 | 01, 22 |
| S11 | Release Tag v2026.8.19 | Official | https://github.com/NousResearch/hermes-agent/releases/tag/v2026.8.19 | 01, 22 |
| S12 | Release Tag v2026.9.7 | Official | https://github.com/NousResearch/hermes-agent/releases/tag/v2026.9.7 | 01, 22 |
| S13 | Self-Evolution Repo | Official | https://github.com/NousResearch/hermes-agent-self-evolution | 01, 15, 22 |

---

# OFFICIAL DOCS (FETCHED — Phase 1/2)

| ID | Source | Type | URL | Used By |
|----|--------|------|-----|---------|
| D01 | Architecture Guide | Official | https://hermes-agent.nousresearch.com/docs/developer-guide/architecture | 01, 22 |
| D02 | Quickstart | Official | https://hermes-agent.nousresearch.com/docs/getting-started/quickstart | 01, 02, 03, 05, 06, 22 |
| D03 | Installation | Official | https://hermes-agent.nousresearch.com/docs/getting-started/installation | 02, 22 |
| D04 | Updating | Official | https://hermes-agent.nousresearch.com/docs/getting-started/updating | 02, 22 |
| D05 | Docker Guide | Official | https://hermes-agent.nousresearch.com/docs/user-guide/docker | 02, 22 |
| D06 | Messaging/Gateway | Official | https://hermes-agent.nousresearch.com/docs/user-guide/messaging/ | 02, 09, 22 |
| D07 | Configuration | Official | https://hermes-agent.nousresearch.com/docs/user-guide/configuration | 02, 03, 06, 22 |
| D08 | Environment Variables | Official | https://hermes-agent.nousresearch.com/docs/reference/environment-variables | 03, 06, 22 |
| D09 | Providers | Official | https://hermes-agent.nousresearch.com/docs/integrations/providers | 03, 22 |
| D10 | CLI Commands Reference | Official | https://hermes-agent.nousresearch.com/docs/reference/cli-commands | 04, 05, 06, 22 |
| D11 | Slash Commands Reference | Official | https://hermes-agent.nousresearch.com/docs/reference/slash-commands | 05, 06, 22 |
| D12 | Profile Commands Reference | Official | https://hermes-agent.nousresearch.com/docs/reference/profile-commands | 04, 05, 22 |
| D13 | Bundled Skill: hermes-agent | Official | https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-hermes-agent | 04, 05, 06, 11, 22 |

---

# OFFICIAL DOCS (FETCHED — Phase 3/4)

| ID | Source | Type | URL | Used By |
|----|--------|------|-----|---------|
| D34 | Tools Reference | Official | https://hermes-agent.nousresearch.com/docs/reference/tools | 07, 22 |
| D35 | Terminal Backends | Official | https://hermes-agent.nousresearch.com/docs/user-guide/features/terminal | 08, 22 |
| D36 | Messaging Platforms | Official | https://hermes-agent.nousresearch.com/docs/user-guide/messaging/platforms | 09, 22 |
| D37 | Webhooks | Official | https://hermes-agent.nousresearch.com/docs/user-guide/messaging/webhooks | 09, 13, 22 |
| D38 | MCP Feature | Official | https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp | 10, 22 |
| D39 | Plugins Feature | Official | https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins | 10, 22 |
| D40 | Skills Feature | Official | https://hermes-agent.nousresearch.com/docs/user-guide/features/skills | 11, 22 |
| D41 | Curator Feature | Official | https://hermes-agent.nousresearch.com/docs/user-guide/features/curator | 11, 22 |
| D42 | Memory Feature | Official | https://hermes-agent.nousresearch.com/docs/user-guide/features/memory | 12, 22 |
| D43 | Context Files | Official | https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files | 12, 22 |
| D44 | Personality Feature | Official | https://hermes-agent.nousresearch.com/docs/user-guide/features/personality | 12, 22 |
| D45 | Context Compression | Official | https://hermes-agent.nousresearch.com/docs/developer-guide/context-compression-and-caching | 12, 22 |
| D46 | Prompt Assembly | Official | https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly | 12, 22 |
| D47 | Cron Feature | Official | https://hermes-agent.nousresearch.com/docs/user-guide/features/cron | 13, 22 |
| D48 | Automation Blueprints | Official | https://hermes-agent.nousresearch.com/docs/guides/automation-blueprints | 13, 22 |
| D49 | Daily Briefing Bot | Official | https://hermes-agent.nousresearch.com/docs/guides/daily-briefing-bot | 13, 22 |
| D50 | Delegation Feature | Official | https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation | 14, 22 |
| D51 | Skills Catalog (Live) | Official | https://hermes-agent.nousresearch.com/docs/reference/skills-catalog | 11, 22 |
| D52 | Optional Skills Catalog | Official | https://hermes-agent.nousresearch.com/docs/reference/optional-skills-catalog | 11, 22 |
| D53 | llms.txt (docs index) | Official | https://hermes-agent.nousresearch.com/docs/llms.txt | All, 22 |

---

# OFFICIAL DOCS (NOT FETCHED / PARTIAL — TARGET FOR CHAT 3)

| ID | Source | Type | URL | Target File |
|----|--------|------|-----|-------------|
| D14 | Platform Support | Official | https://hermes-agent.nousresearch.com/docs/getting-started/platform-support | 02, 17, 22 |
| D15 | Security Guide | Official | https://hermes-agent.nousresearch.com/docs/user-guide/security | 05, 16, 22 |
| D16 | Configuration (truncated tail) | Official | https://hermes-agent.nousresearch.com/docs/user-guide/configuration | 06, 22 |
| D17 | Programmatic Integration | Official | https://hermes-agent.nousresearch.com/docs/developer-guide/programmatic-integration | 04, 14, 22 |
| D18 | Agent Loop | Official | https://hermes-agent.nousresearch.com/docs/developer-guide/agent-loop | 01, 15, 22 |
| D19 | Prompt Assembly | Official | https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly | 01, 12, 22 |
| D20 | Session Storage | Official | https://hermes-agent.nousresearch.com/docs/developer-guide/session-storage | 01, 12, 18, 22 |
| D21 | Gateway Internals | Official | https://hermes-agent.nousresearch.com/docs/developer-guide/gateway-internals | 01, 09, 22 |
| D22 | Skills Feature | Official | https://hermes-agent.nousresearch.com/docs/user-guide/features/skills | 11, 22 |
| D23 | Memory Feature | Official | https://hermes-agent.nousresearch.com/docs/user-guide/features/memory | 12, 22 |
| D24 | MCP Feature | Official | https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp | 10, 22 |
| D25 | Cron Feature | Official | https://hermes-agent.nousresearch.com/docs/user-guide/features/cron | 13, 22 |
| D26 | Fallback Providers | Official | https://hermes-agent.nousresearch.com/docs/user-guide/features/fallback-providers | 03, 22 |
| D27 | Profiles & Multi-Profile Gateways | Official | https://hermes-agent.nousresearch.com/docs/user-guide/profiles | 06, 09, 22 |
| D28 | FAQ (Backup vs Export, Troubleshooting) | Official | https://hermes-agent.nousresearch.com/docs/reference/faq | 02, 18, 22 |
| D29 | Context Files | Official | https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files | 05, 06, 12, 22 |
| D30 | API Server Feature | Official | https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server | 04, 09, 22 |
| D31 | CLI Reference (rest) | Official | https://hermes-agent.nousresearch.com/docs/reference/cli-commands | 04, 22 |
| D32 | llms.txt (one-line index) | Official | https://hermes-agent.nousresearch.com/docs/llms.txt | All, 22 |
| D33 | llms-full.txt (everything) | Official | https://hermes-agent.nousresearch.com/docs/llms-full.txt | All, 22 |
| D54 | Hooks Feature | Official | https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks | 10, 13, 22 |
| D55 | Kanban Feature | Official | https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban | 14, 22 |
| D56 | A2A Messaging | Official | https://hermes-agent.nousresearch.com/docs/messaging/a2a | 14, 22 |
| D57 | Batch Processing | Official | https://hermes-agent.nousresearch.com/docs/developer-guide/batch-processing | 15, 22 |
| D58 | Trajectory Format | Official | https://hermes-agent.nousresearch.com/docs/developer-guide/trajectory-format | 15, 22 |
| D59 | Micro Compaction | Official | https://hermes-agent.nousresearch.com/docs/developer-guide/micro-compaction | 12, 22 |
| D60 | Memory Providers | Official | https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers | 12, 22 |
| D61 | Honcho Feature | Official | https://hermes-agent.nousresearch.com/docs/user-guide/features/honcho | 12, 22 |
| D62 | Which File Does What | Official | https://hermes-agent.nousresearch.com/docs/user-guide/which-file-does-what | 06, 12, 22 |
| D63 | Troubleshooting Agent Quality | Official | https://hermes-agent.nousresearch.com/docs/guides/troubleshooting-agent-quality | 18, 22 |
| D64 | Secure Hermes on Work Machine | Official | https://hermes-agent.nousresearch.com/docs/guides/secure-hermes-on-a-work-machine | 16, 22 |
| D65 | Cron Script Only | Official | https://hermes-agent.nousresearch.com/docs/guides/cron-script-only | 13, 22 |
| D66 | Automation Blueprints Catalog | Official | https://hermes-agent.nousresearch.com/docs/reference/automation-blueprints-catalog | 13, 22 |
| D67 | Webhook Events | Official | https://hermes-agent.nousresearch.com/docs/user-guide/messaging/webhooks#event-triggered-cron-jobs | 13, 22 |

---

# REPO SOURCE FILES (WORTH INSPECTING DIRECTLY)

| ID | Path | Description | Used By |
|----|------|-------------|---------|
| R01 | `run_agent.py` | AIAgent facade | 01, 14 |
| R02 | `cli.py`, `hermes_cli/` | CLI facade, subcommands, setup, config, commands, auth | 04, 05, 06, 22 |
| R03 | `hermes_cli/main.py` | CLI entrypoint, parsers | 04, 22 |
| R04 | `hermes_cli/commands.py` | `COMMAND_REGISTRY` (slash commands) | 05, 22 |
| R05 | `hermes_cli/config.py` | `DEFAULT_CONFIG`, `OPTIONAL_ENV_VARS`, migrations | 06, 22 |
| R06 | `hermes_cli/setup.py` | Setup wizard | 02, 22 |
| R07 | `hermes_cli/auth.py` | `PROVIDER_REGISTRY` | 03, 06, 22 |
| R08 | `hermes_cli/gateway.py` | Gateway install/unit generation | 02, 09, 22 |
| R09 | `model_tools.py`, `toolsets.py`, `tools/` | Tool discovery, dispatch, registry | 07, 22 |
| R10 | `tools/environments/` | Terminal backends (7) | 08, 22 |
| R11 | `agent/` | Prompt builder, compression, context, memory, trajectory | 01, 12, 15, 22 |
| R12 | `gateway/` | GatewayRunner, session, delivery, pairing, platforms | 09, 22 |
| R13 | `plugins/` | Platform plugins, memory plugins, context engine plugins | 09, 10, 12, 22 |
| R14 | `cron/` | Scheduler (jobs.py, scheduler.py) | 13, 22 |
| R15 | `acp_adapter/` | ACP server | 10, 22 |
| R16 | `skills/`, `optional-skills/`, `optional-mcps/` | Bundled/optional skills and MCPs | 11, 22 |
| R17 | `hermes_state*.py` | Session DB facade, schema, search, portability | 12, 18, 22 |
| R18 | `batch_runner.py`, `trajectory_compressor.py`, `evals/` | Research/trajectory | 15, 22 |
| R19 | `docker/`, `Dockerfile`, `docker-compose.yml` | Packaging | 02, 22 |
| R20 | `scripts/install.sh` | Installer script | 02, 22 |
| R21 | `cli-config.yaml.example` | Example config (full schema) | 06, 22 |
| R22 | `.env.example` | Example env vars | 06, 22 |
| R23 | `SOUL.md`, `AGENTS.md` | Identity and agent instructions | 01, 06, 12, 22 |
| R24 | `hermes_cli/subcommands/` | Individual command implementations | 04, 22 |
| R25 | `tools/delegate_tool_registry.py` | Delegation registry | 14, 22 |
| R26 | `tools/skills_guard.py` | Hub scanner and `TRUSTED_REPOS` | 11, 22 |
| R27 | `tools/skill_provenance.py` | Skill provenance tracking | 11, 22 |
| R28 | `cron/scheduler.py`, `cron/jobs.py`, `cron/recipe_catalog.py` | Cron internals | 13, 22 |
| R29 | `agent/context_compressor.py`, `agent/context_engine.py` | Compression engine | 12, 22 |
| R30 | `agent/prompt_builder.py`, `agent/prompt_caching.py` | Prompt assembly | 12, 22 |
| R31 | `agent/trajectory.py` | Trajectory format | 15, 22 |
| R32 | `toolset_distributions.py` | Toolset distributions for batch | 15, 22 |
| R33 | `gateway/hooks.py` | Gateway hooks | 13, 22 |
| R34 | `website/scripts/generate-skill-docs.py` | Skill catalog generator | 11, 22 |
| R35 | `agent/subdirectory_hints.py` | Subdirectory context discovery | 12, 22 |
| R36 | `hermes_cli/goals.py` | Goals implementation | 15, 22 |
| R37 | `tools/memory_tool.py` | Memory tool (search term) | 12, 22 |
| R38 | `tools/skills_hub.py` | Skills hub client (search term) | 11, 22 |

---

# COMMUNITY / THIRD-PARTY SOURCES

| ID | Source | Type | URL | Used By |
|----|--------|------|-----|---------|
| C01 | Awesome Hermes Agent (0xNyk) | Community | https://github.com/0xNyk/awesome-hermes-agent | 01, 22 |
| C02 | Awesome Hermes Agent (0xarkstar) | Community | https://github.com/0xarkstar/awesome-hermes-agent | 01, 22 |
| C03 | Awesome Hermes Use Cases (aliaihub) | Community | https://github.com/aliaihub/awesome-hermes-usecases | 01, 20, 22 |
| C04 | ForgeGuard Fork Releases | Community | https://github.com/forgeguard-ai/hermes-agent/releases | 01, 22 |
| C05 | Hermes Portable (zpage) | Community | https://github.com/zpage/hermes-portable | 02, 22 |
| C06 | Stack Fund Agent (Silavater) | Community | https://github.com/Silavater/stack_fund_agent | 01, 22 |
| C07 | Backup/Migrate Guide (toolnavs.com) | Community | https://toolnavs.com/en/article/1689-how-to-backup-and-migrate-hermes-agent-server | 02, 22 |
| C08 | Gradually.ai Changelogs | Community | https://www.gradually.ai/en/changelogs/hermes-agent/ | 01, 22 |
| C09 | ReleaseBot Updates | Community | https://releasebot.io/updates/nousresearch/hermes-agent | 01, 22 |
| C10 | Dev.to Cheat Sheet (rosgluk) | Community | https://dev.to/rosgluk/hermes-agent-cli-cheat-sheet-commands-flags-and-slash-shortcuts-3pcb | 04, 05, 06, 22 |
| C11 | GitHub Issue #36949 (1Password) | Community | https://github.com/NousResearch/hermes-agent/issues/36949 | 06, 22 |
| C12 | Hermes Docs Mirror (koc-Z3) | Community | https://github.com/koc-Z3/hermes-docs | 04, 05, 22 |
| C13 | Hermes Agent Mirror (hermesagent.org.cn) | Community | https://hermesagent.org.cn/... | 04, 22 |
| C14 | mudrii/hermes-agent-docs | Community | https://github.com/mudrii/hermes-agent-docs | 11, 12, 15, 22 |
| C15 | ZeroPointRepo/awesome-hermes-skills | Community | https://github.com/ZeroPointRepo/awesome-hermes-skills | 11, 22 |
| C16 | itgoyo/hermes-skills | Community | https://github.com/itgoyo/hermes-skills | 11, 22 |
| C17 | TechNickAI/hermes-config | Community | https://github.com/TechNickAI/hermes-config | 11, 22 |
| C18 | Hookdeck Hermes | Community | https://github.com/hookdeck/hermes-hookdeck | 10, 22 |
| C19 | The Agent Stack Substack | Community | https://theagentstack.substack.com | 15, 22 |
| C20 | dev.to/truongpx396 | Community | https://dev.to/truongpx396 | 15, 22 |
| C21 | vectorize.io provider comparison | Community | https://vectorize.io | 12, 22 |
| C22 | dev.to/rosgluk provider comparison | Community | https://dev.to/rosgluk | 12, 22 |

---

# SOURCE USAGE BY REFERENCE FILE

| Reference File | Source IDs |
|----------------|------------|
| 01-foundations-architecture.md | S01-S13, D01-D02, D09-D13, D34-D35, C01-C03, C08-C09 |
| 02-install-vps-config-basics.md | S01-S13, D02-D06, C07, C05 |
| 03-providers-and-models.md | S01, D02, D07, D08, D09 |
| 04-cli-command-reference-a.md | S01, D10-D13, D34, C10, C11, C12, C13 |
| 04-cli-command-reference-b.md | S01, D10-D13, D34, C10, C11, C12, C13 |
| 05-slash-commands-sessions-interactive.md | D11-D13, D10, D44 |
| 06-config-keys-and-env-vars.md | D07-D08, D10-D13, D45, R05, R21, R22 |
| 07-tools-and-toolsets.md | D34, D38, R09, R25 |
| 08-terminal-backends.md | D35, R10 |
| 09-messaging-gateway.md | D06, D36, D37, D48, R12, R13 |
| 10-mcp-plugins-api.md | D38, D39, D54, R13, R15, R25 |
| 11-skills-system.md | D40, D41, D51, D52, R16, R24, R26, R27, C14, C15, C16, C17 |
| 12-memory-and-context.md | D42, D43, D44, D45, D46, D59, D60, D61, R11, R17, C19, C20, C21, C22 |
| 13-scheduling-and-automation.md | D47, D48, D49, D54, D65, D66, R14, R28 |
| 14-subagents-and-delegation.md | D50, D55, D56, R25 |
| 15-learning-loop-and-advanced.md | D18, D57, D58, R18, R31, R32 |
| 00-index-and-routing.md | Derived from all above |
| 22-unverified-and-gaps.md | All gaps from all sources |
| 23-sources.md | This file |

---

# FETCH PRIORITY FOR CHAT 3

| Priority | Source IDs | Reason |
|----------|------------|--------|
| **Critical** | D15, D16, D29, D31, D32, D33 | Security, config tail, context files, complete CLI, full docs index |
| **Critical** | D54, D55, D56, D57, D58, D59, D60, D61, D62, D63, D64, D65, D66, D67 | Hooks, Kanban, A2A, Batch, Trajectory, Micro-compaction, Memory providers, Honcho, Which-file, Troubleshooting, Secure, Cron script-only, Blueprints catalog, Webhook events |
| **High** | D14, D17, D18, D19, D20, D21 | Platform support, Programmatic integration, Agent loop, Prompt assembly, Session storage, Gateway internals |
| **High** | R04, R05, R07, R21, R25, R26, R27, R28, R29, R30, R31, R32, R33, R34, R35, R36, R37, R38 | Command registry, config schema, provider registry, example config, delegation, skills guard/provenance, cron internals, compression, prompt, trajectory, toolset dist, hooks, skill catalog, subdirectory hints, goals, memory tool, skills hub |
| **Medium** | D22, D23, D24, D25, D26, D27, D28, D30 | Skills, Memory, MCP, Cron, Fallback, Profiles, FAQ, API Server |
| **Medium** | R06, R08, R12, R13, R14, R15 | Setup, Gateway, Plugins, Cron, ACP |
| **Low** | C01-C22 | Community awesome lists, mirrors, issues, docs |

---

# END OF SOURCES MASTER LIST (v2)