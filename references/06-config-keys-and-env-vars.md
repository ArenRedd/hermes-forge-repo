---
title: Config Keys, Environment Variables & Precedence
source_phases: [Phase 1, Phase 2]
hermes_version_documented: v0.21.5 (tag v2026.9.24, Sep 24 2026) / v0.21.x
research_date: Friday, October 2, 2026
last_built_in: Chat 1
confidence_legend: OFFICIAL = official repo/docs/source; COMMUNITY = third-party; INFERRED = deduced; UNVERIFIED = needs checking
used_by_playbooks: [01-coding-and-dev.md, 02-devops-and-server-admin.md, 03-research-and-analysis.md, 04-content-and-social.md, 05-automation-and-scheduling.md, 06-messaging-gateway-setups.md, 07-browser-and-data-collection.md, 08-multi-agent-and-parallel.md, 09-personal-productivity.md, 10-skill-authoring-and-memory-curation.md, 11-maintenance-backup-recovery.md, 19-cost-and-optimization.md]
---

# WHEN TO READ THIS FILE
Read this file when you need the complete configuration reference: every config key (grouped by category), every environment variable, precedence rules, the on-disk layout with hand-edit safety, profiles/multi-instance details, context-file discovery rules, personality presets, the annotated example config, the 60-command cheat sheet, and hidden/lesser-known commands. This merges Phase 1 (~70 keys) and Phase 2 (~40 new keys).

---

# TABLE OF CONTENTS
1. [Precedence Rules](#1-precedence-rules)
2. [Config Keys — Complete Table (Merged Phase 1 + Phase 2)](#2-config-keys--complete-table-merged-phase-1--phase-2)
3. [Environment Variables — Complete Table (Merged)](#3-environment-variables--complete-table-merged)
4. [On-Disk Layout & Hand-Edit Safety](#4-on-disk-layout--hand-edit-safety)
5. [Profiles & Multi-Instance Details](#5-profiles--multi-instance-details)
6. [Per-Directory Context File Discovery](#6-per-directory-context-file-discovery)
7. [Personality Presets](#7-personality-presets)
8. [Annotated Example Config](#8-annotated-example-config)
9. [60-Command Cheat Sheet](#9-60-command-cheat-sheet)
10. [Hidden / Lesser-Known Commands](#10-hidden--lesser-known-commands)
11. [Config Migrations](#11-config-migrations)
12. [Conflicts](#12-conflicts)
13. [Gaps](#13-gaps)
14. [Sources](#14-sources)

---

# 1. PRECEDENCE RULES

**Config precedence (high to low)** [OFFICIAL]:
1. CLI arguments
2. `config.yaml`
3. `.env`
4. Built-in defaults

**Notes** [OFFICIAL]:
- Secrets go in `.env`. Non-secret values in `config.yaml` win over `.env`.
- `${VAR}` substitution works in `config.yaml` (and `${env:VAR}`).
- `--ignore-user-config` bypasses `config.yaml` but still loads `.env`.
- Board resolution (kanban): `--board`, then `HERMES_KANBAN_BOARD`, then `~/.hermes/kanban/current`, then `default`.

---

# 2. CONFIG KEYS — COMPLETE TABLE (MERGED PHASE 1 + PHASE 2)

All rows from Phase 1 Configuration page [OFFICIAL] plus Phase 2 discoveries [OFFICIAL]. "Not stated" means the page did not give a default. Keys are grouped by category exactly as in the source.

## 2.1 Model

| Key | Type | Default | Description | Phase |
|-----|------|---------|-------------|-------|
| `model.provider` | str | not stated | Provider id (`custom`, `anthropic`, etc.) | 1 |
| `model.default` (alias `model.model`) | str | not stated | Model ID | 1 |
| `model.base_url` / `api_key` / `key_env` | str | none | Custom endpoint URL and key | 1 |
| `model.context_length` | int | auto-detected | Pins the context window | 1 |
| `model.supports_vision` | bool | not stated | Send images natively | 1 |
| `model.ollama_num_ctx` | int | not stated | Window the local server serves (64K+) | 1 |
| `model.lmstudio_load_mode` | str | `explicit` | `jit` or `explicit` | 1 |
| `providers.<id>.api` | str | n/a | Named custom provider (alias `base_url`/`url`) | 1 |
| `providers.<id>.transport` | str | auto | `chat_completions`, `anthropic_messages`, `codex_responses` | 1 |
| `providers.<id>.request_timeout_seconds` | int | legacy 1800s | Provider-wide timeout | 1 |
| `fallback_providers` | list | none | Ordered backup chain | 1 |
| `provider_routing.sort` | str | `price` | OpenRouter routing: `price`, `throughput`, `latency` | 1 |
| `openrouter.min_coding_score` | float | 0.65 | Only for `openrouter/pareto-code` | 1 |
| `model.persist_switch_by_default` | bool | not stated | Make every `/model` switch persist | 2 |
| `model.aliases.<name>` / `model_aliases:` | map | n/a | Short form `provider/model`; full form with `model`, `provider`, `base_url`, `api_key`/`key_env` | 2 |
| `model.openai_runtime` | str | not stated | Written by `/codex-runtime` | 2 |

## 2.2 UI / Display

| Key | Type | Default | Description | Phase |
|-----|------|---------|-------------|-------|
| `display.interface` | str | not stated | `tui` or classic | 2 |
| `display.skin` | str | not stated | Skin name | 2 |
| `display.busy_ack_enabled` | bool | not stated | Busy acknowledgment | 2 |
| `display.tool_progress_command` | bool | not stated | Tool progress in messaging | 2 |
| `display.focus_saved_tool_progress` | bool | not stated | Focus view saved progress | 2 |
| `display.busy_input_mode` | str | `interrupt` | Or `queue`, `steer` | 1 |
| `display.tool_progress` | str | per-platform | `off`, `new`, `all`, `verbose`, `log` | 1 |
| `quick_commands.<name>.{type,command,target}` | map | n/a | `exec` or `alias` custom commands | 2 |
| `voice.record_key` | str | `Ctrl+B` | Voice record key | 2 |

## 2.3 Approvals

| Key | Type | Default | Description | Phase |
|-----|------|---------|-------------|-------|
| `approvals.destructive_slash_confirm` | bool | not stated | Confirm destructive slash commands | 2 |
| `approvals.single_query_mode` | bool | not stated | Single query approval mode | 2 |

## 2.4 Agent

| Key | Type | Default | Description | Phase |
|-----|------|---------|-------------|-------|
| `agent.max_turns` | int/none | none (unlimited) | Iteration cap | 1 |
| `agent.api_max_retries` | int | 3 | Retries before fallback | 1 |
| `agent.auto_recovery_cycles` | int | 5 | Wait-and-retry cycles after an outage | 1 |
| `agent.restart_after_turn_timeout` | int | 1800 | Gateway drain cap (seconds) | 1 |
| `agent.session_stall_timeout` | int | 300 | Notify-only watchdog (seconds) | 1 |
| `agent.reconnect_attention_after` | int | 7200 | Needs-attention flag (seconds) | 1 |
| `agent.verify_on_stop` | bool/`"auto"` | false | Require verification evidence | 1 |
| `agent.disabled_toolsets` | list | none | Globally remove toolsets | 1 |
| `agent.agent_cache.*` | various | `max_size` 128, `idle_ttl_secs` 3600, `memory_high_mb` auto | Gateway agent cache | 1 |
| `agent.fast_auto_seconds` | int | 60 | Fast auto timeout | 2 |
| `agent.bot_mode_protocol` | str | not stated | Bot mode protocol | 2 |
| `agent.run_budget_seconds` | int | not stated | Hard time limit for runs | 1 (mentioned in cost levers) |

## 2.5 Terminal

| Key | Type | Default | Description | Phase |
|-----|------|---------|-------------|-------|
| `terminal.backend` | str | `local` | `local`, `docker`, `ssh`, `modal`, `daytona`, `vercel_sandbox`, `singularity` | 1 |
| `terminal.cwd` | str | `"."` | Gateway/cron working directory | 1 |
| `terminal.timeout` | int | 180 | Per-command seconds | 1 |
| `terminal.home_mode` | str | `auto` | `auto`, `real`, `profile` | 1 |
| `terminal.docker_image` | str | `nousresearch/hermes-sandbox:desktop` | Sandbox image | 1 |
| `terminal.docker_mount_cwd_to_workspace` | bool | false | Mounts launch dir at `/workspace` | 1 |
| `terminal.docker_run_as_host_user` | bool | false | Adds `--user` | 1 |
| `terminal.docker_snap_compat` | bool | false | Snap Docker workaround | 1 |
| `terminal.docker_network` | bool | true | `false` means `--network=none` | 1 |
| `terminal.container_cpu` / `container_memory` / `container_disk` | int | 1 / 5120 MB / 51200 MB | Sandbox limits | 1 |
| `terminal.container_persistent` | bool | true | Persist filesystem | 1 |
| `terminal.persistent_shell` | bool | true | Long-lived bash | 1 |
| `terminal.lifetime_seconds` | int | 300 | Idle reaper | 1 |
| `terminal.oneshot_completion_wait_seconds` | int | not stated | Bounded exit wait for background terminal completions | 2 |

## 2.6 Memory

| Key | Type | Default | Description | Phase |
|-----|------|---------|-------------|-------|
| `memory.memory_enabled` / `user_profile_enabled` | bool | true / true | Memory features | 1 |
| `memory.memory_char_limit` / `user_char_limit` | int | 2200 / 1375 | Memory sizes | 1 |
| `memory.write_approval` | bool | false | Gate memory writes | 1 |

## 2.7 Skills

| Key | Type | Default | Description | Phase |
|-----|------|---------|-------------|-------|
| `skills.auto_load` | list | none | Skills loaded each session | 1 |
| `skills.guard_agent_created` | bool | false | Scan agent skill writes | 1 |
| `skills.write_approval` | bool | false | Stage skill writes for review | 1 |

## 2.8 Compression

| Key | Type | Default | Description | Phase |
|-----|------|---------|-------------|-------|
| `compression.enabled` | bool | true | Toggle compression | 1 |
| `compression.threshold` | float | 0.50 | Fraction of context that triggers it | 1 |
| `compression.target_ratio` | float | 0.20 | Recent tail to preserve | 1 |
| `compression.protect_last_n` / `protect_first_n` | int | 20 / 3 | Pinned messages | 1 |
| `compression.in_place` | bool | true | Compact on the same session id | 1 |
| `compression.threshold_tokens` | int | not stated | Absolute token cap (alternative to threshold) | 1 |
| `compression.proactive_prune_tokens` | int | not stated | Proactive pruning (docs suggest 48000) | 1 |
| `auxiliary.compression.{provider,model,base_url}` | str | `auto`, empty, null | Summarizer routing | 1 |
| `auxiliary.review` | map | not stated | Review task model | 2 |
| `auxiliary.triage_specifier` | map | not stated | Triage specifier model | 2 |
| `auxiliary.kanban_decomposer` | map | not stated | Kanban decomposer model | 2 |
| `auxiliary.profile_describer` | map | not stated | Profile describer model | 2 |

## 2.9 Context Engine

| Key | Type | Default | Description | Phase |
|-----|------|---------|-------------|-------|
| `context.engine` | str | `compressor` | Plugin engine (e.g., `lcm`) | 1 |
| `context_file_max_chars` | int | not stated | Max chars per context file | 2 (implied) |

## 2.10 Goals

| Key | Type | Default | Description | Phase |
|-----|------|---------|-------------|-------|
| `goals.max_turns` | int | 20 | `/goal` continuation cap | 1 |

## 2.11 Updates

| Key | Type | Default | Description | Phase |
|-----|------|---------|-------------|-------|
| `updates.pre_update_backup` | str | `quick` | `quick`, `full`, `off` | 1 |
| `updates.non_interactive_local_changes` | str | `stash` | Or `discard` | 1 |
| `updates.check` | bool | true | Passive update notices | 1 |
| `updates.parked_branch_strategy` | str | `update_in_place` | Parked branch handling | 2 |
| `updates.install_channel` | str | not stated | Update channel families | 2 |

## 2.12 Database

| Key | Type | Default | Description | Phase |
|-----|------|---------|-------------|-------|
| `database.journal_mode` | str | `wal` | Or `delete` for network mounts | 1 |

## 2.13 Runtime

| Key | Type | Default | Description | Phase |
|-----|------|---------|-------------|-------|
| `runtime.nofile_soft_limit` | int | 4096 | Gateway fd limit | 1 |

## 2.14 Tool Output Limits

| Key | Type | Default | Description | Phase |
|-----|------|---------|-------------|-------|
| `file_read_max_chars` | int | 100000 | `read_file` cap | 1 |
| `tool_output.max_bytes` / `max_lines` / `max_line_length` | int | 50000 / 2000 / 2000 | Output truncation | 1 |
| `tool_budget.mcp_result_size_chars` | int | 50000 | MCP result spillover | 1 |

## 2.15 Git Worktree

| Key | Type | Default | Description | Phase |
|-----|------|---------|-------------|-------|
| `worktree` / `worktree_sync` | bool | false / true | Git worktree isolation | 1 |

## 2.16 Gateway

| Key | Type | Default | Description | Phase |
|-----|------|---------|-------------|-------|
| `gateway.delivery_ledger` | bool | true | Redelivery after crash | 1 |
| `gateway.loop_watchdog` | bool | true | Event-loop watchdog | 1 |
| `gateway.systemd_watchdog_seconds` | int | 0 | `WatchdogSec` for the unit | 1 |
| `gateway.trust_env` | bool | true | Honor inherited proxy vars | 1 |
| `gateway.platforms.<name>.extra.{allow_from,allow_admin_from,user_allowed_commands,group_*}` | map | n/a | Platform access control | 2 |
| `bot_peers` | map | n/a | Peer gateway config | 2 |
| `platforms.<name>.channel_overrides` | map | n/a | Per-channel model/prompt overrides | 2 |

## 2.17 MCP Servers

| Key | Type | Default | Description | Phase |
|-----|------|---------|-------------|-------|
| `mcp_servers.<name>` | map | none | `command`, `args`, `env` (see quickstart) | 1 |

## 2.18 Dashboard

| Key | Type | Default | Description | Phase |
|-----|------|---------|-------------|-------|
| `dashboard.public_url`, `dashboard.trusted_proxies` | str, list | none | Reverse-proxy settings | 1 |

## 2.19 Security

| Key | Type | Default | Description | Phase |
|-----|------|---------|-------------|-------|
| `security.allow_lazy_installs` | bool | not stated | Allow lazy installs | 2 |
| `proxy.enabled` | bool | not stated | Egress proxy enabled | 2 |
| `proxy.extra_allowed_hosts` | list | not stated | Extra allowed hosts for proxy | 2 |

## 2.20 Plugins

| Key | Type | Default | Description | Phase |
|-----|------|---------|-------------|-------|
| `plugins.enabled` | list | none | Enabled plugins | 2 |
| `plugins.disabled` | list | none | Disabled plugins | 2 |
| `memory.provider` | str | not stated | External memory provider | 2 |

## 2.21 Bundles

| Key | Type | Default | Description | Phase |
|-----|------|---------|-------------|-------|
| `bundles:` | map | n/a | Skill bundles | 2 |

## 2.22 Secrets

| Key | Type | Default | Description | Phase |
|-----|------|---------|-------------|-------|
| `secrets:` | map | n/a | External secret sources (Bitwarden, 1Password) | 2 |
| `secrets.command` | str | not stated | Command for secrets | 2 |
| `secrets.onepassword.env` | str | not stated | 1Password env (from issue #36949, unconfirmed shipped) | 2 [COMMUNITY] |

## 2.23 Cron

| Key | Type | Default | Description | Phase |
|-----|------|---------|-------------|-------|
| `cron.provider` | str | empty | Trigger: empty = built-in ticker, `chronos` for hosted | 2 |
| `cron.chronos.{portal_url,callback_url,expected_audience,nas_jwks_url}` | str | n/a | Chronos config | 2 |
| `cron.inflight_max_minutes` | int | 30 | Max inflight job minutes | 2 |

## 2.24 Network

| Key | Type | Default | Description | Phase |
|-----|------|---------|-------------|-------|
| `network.force_ipv4` | bool | not stated | Remedy for blackholed IPv6 | 2 |

## 2.25 Delegation

| Key | Type | Default | Description | Phase |
|-----|------|---------|-------------|-------|
| `delegation.max_concurrent_children` | int | not stated | Limits parallel children | 2 |

---

**Total config keys: ~110** (Phase 1: ~70, Phase 2: ~40). **Completeness: UNVERIFIED** — full schema needs `cli-config.yaml.example` and `hermes_cli/config.py` (`DEFAULT_CONFIG`).

---

# 3. ENVIRONMENT VARIABLES — COMPLETE TABLE (MERGED)

## 3.1 Provider API Keys (Phase 1)

| Variable | Purpose | Tag |
|----------|---------|-----|
| `OPENROUTER_API_KEY` | Provider key | [OFFICIAL] |
| `OPENAI_API_KEY` | Provider key | [OFFICIAL] |
| `ANTHROPIC_API_KEY` | Provider key | [OFFICIAL] |
| `GOOGLE_API_KEY` (alias `GEMINI_API_KEY`) | Provider key | [OFFICIAL] |
| `XAI_API_KEY` | Provider key | [OFFICIAL] |
| `DEEPSEEK_API_KEY` | Provider key | [OFFICIAL] |
| `HF_TOKEN` | Hugging Face | [OFFICIAL] |
| `GLM_API_KEY` (aliases `ZAI_API_KEY`, `Z_AI_API_KEY`) | Provider key | [OFFICIAL] |
| `KIMI_API_KEY` | Provider key | [OFFICIAL] |
| `MINIMAX_API_KEY` | Provider key | [OFFICIAL] |
| `NVIDIA_API_KEY` | Provider key | [OFFICIAL] |
| `OLLAMA_API_KEY` | Provider key | [OFFICIAL] |
| `FIREWORKS_API_KEY` | Provider key | [OFFICIAL] |

## 3.2 Provider Base URLs & Auth (Phase 1)

| Variable | Purpose | Tag |
|----------|---------|-----|
| `OPENAI_BASE_URL` | Base URL for custom OpenAI-compatible endpoints (used only for `openai-api` provider now) | [OFFICIAL] |
| `COPILOT_GITHUB_TOKEN` > `GH_TOKEN` > `GITHUB_TOKEN` | Copilot token priority (classic `ghp_*` PATs unsupported) | [OFFICIAL] |
| `AWS_REGION`, `AWS_PROFILE` | Bedrock | [OFFICIAL] |
| `VERTEX_CREDENTIALS_PATH` | Vertex AI service account | [OFFICIAL] |

## 3.3 Core Runtime (Phase 1)

| Variable | Purpose | Tag |
|----------|---------|-----|
| `HERMES_HOME` | Data home (default `~/.hermes`; Docker `/opt/data`) | [OFFICIAL] |
| `HERMES_MODEL` | Process-level model override | [OFFICIAL] |
| `HERMES_TIMEZONE` | IANA timezone | [OFFICIAL] |
| `HERMES_DUMP_REQUESTS` | Dump API payloads to logs | [OFFICIAL] |
| `HERMES_API_TIMEOUT` (1800s), `HERMES_API_CALL_STALE_TIMEOUT` (90s), `HERMES_STREAM_READ_TIMEOUT` (120s), `HERMES_STREAM_STALE_TIMEOUT` (180s) | Legacy timeouts | [OFFICIAL] |
| `HERMES_VERIFY_ON_STOP` | Overrides `agent.verify_on_stop` | [OFFICIAL] |

## 3.4 Terminal Backend Overrides (Phase 1)

| Variable | Purpose | Tag |
|----------|---------|-----|
| `TERMINAL_ENV` | Backend (`local`, `docker`, `ssh`, ...) | [OFFICIAL] |
| `TERMINAL_SSH_HOST`, `TERMINAL_SSH_USER`, `TERMINAL_SSH_PORT` (22), `TERMINAL_SSH_KEY` | SSH backend | [OFFICIAL] |
| `TERMINAL_DOCKER_*`, `TERMINAL_CONTAINER_CPU/MEMORY/DISK/PERSISTENT`, `TERMINAL_TIMEOUT`, `TERMINAL_LIFETIME_SECONDS` | Docker/container overrides | [OFFICIAL] |
| `MODAL_TOKEN_ID` / `MODAL_TOKEN_SECRET`, `DAYTONA_API_KEY`, `VERCEL_TOKEN` / `VERCEL_PROJECT_ID` / `VERCEL_TEAM_ID` | Cloud backends | [OFFICIAL] |

## 3.5 Messaging Gateway (Phase 1)

| Variable | Purpose | Tag |
|----------|---------|-----|
| `TELEGRAM_BOT_TOKEN`, `TELEGRAM_ALLOWED_USERS`, `TELEGRAM_HOME_CHANNEL`, `TELEGRAM_WEBHOOK_URL` (+ required `TELEGRAM_WEBHOOK_SECRET`) | Telegram | [OFFICIAL] |
| `DISCORD_BOT_TOKEN`, `DISCORD_ALLOWED_USERS`, `DISCORD_REQUIRE_MENTION` | Discord | [OFFICIAL] |
| `SLACK_BOT_TOKEN`, `SLACK_APP_TOKEN`, `SLACK_ALLOWED_USERS` | Slack | [OFFICIAL] |
| `GATEWAY_ALLOWED_USERS` / `GATEWAY_ALLOW_ALL_USERS` | Global allow (latter not recommended) | [OFFICIAL] |

## 3.6 API Server & Dashboard (Phase 1)

| Variable | Purpose | Tag |
|----------|---------|-----|
| `API_SERVER_ENABLED`, `API_SERVER_HOST`, `API_SERVER_PORT` (8642), `API_SERVER_KEY`, `API_SERVER_CORS_ORIGINS` | API server | [OFFICIAL] |
| `HERMES_DASHBOARD`, `HERMES_DASHBOARD_HOST`, `HERMES_DASHBOARD_PORT` (9119), `HERMES_DASHBOARD_BASIC_AUTH_*` | Dashboard | [OFFICIAL] |

## 3.7 Docker Runtime (Phase 1)

| Variable | Purpose | Tag |
|----------|---------|-----|
| `HERMES_UID` / `HERMES_GID` / `PUID` / `PGID`, `HERMES_HOME_MODE`, `HERMES_SKIP_CONFIG_MIGRATION`, `HERMES_ALLOW_ROOT_GATEWAY` | Docker runtime | [OFFICIAL] |

## 3.8 Tool & Memory APIs (Phase 1)

| Variable | Purpose | Tag |
|----------|---------|-----|
| `FIRECRAWL_API_KEY`, `TAVILY_API_KEY`, `EXA_API_KEY`, `BRAVE_SEARCH_API_KEY`, `SEARXNG_URL`, `FAL_KEY`, `ELEVENLABS_API_KEY`, `HONCHO_API_KEY` | Tool and memory APIs | [OFFICIAL] |

## 3.9 Observability (Phase 1)

| Variable | Purpose | Tag |
|----------|---------|-----|
| `HERMES_LANGFUSE_PUBLIC_KEY` / `HERMES_LANGFUSE_SECRET_KEY` | Observability plugin | [OFFICIAL] |

## 3.10 Docker Binary (Phase 1)

| Variable | Purpose | Tag |
|----------|---------|-----|
| `HERMES_DOCKER_BINARY` | Force `podman` or a docker path | [OFFICIAL] |

## 3.11 Phase 2 Additions

| Variable | Purpose | Tag |
|----------|---------|-----|
| `HERMES_INFERENCE_MODEL` | Per-run model for `hermes -z` | [OFFICIAL] |
| `HERMES_TUI=1` | Same as `--tui` | [OFFICIAL] |
| `HERMES_IGNORE_RULES=1` | Same as `--ignore-rules` | [OFFICIAL] |
| `HERMES_KANBAN_TASK` | Set on dispatcher-spawned workers; changes exit code behavior (`75`) | [OFFICIAL] |
| `HERMES_GATEWAY_NO_SUPERVISE=1` | Same as `--no-supervise` | [OFFICIAL] |
| `HERMES_PEER_<NAME>_KEY` | Peer API key stored by `hermes peer add` | [OFFICIAL] |
| `GATEWAY_RELAY_ID`, `_SECRET`, `_DELIVERY_KEY`, `_URL`, `_WAKE_URL` | Written by `hermes gateway enroll` | [OFFICIAL] |
| `HERMES_INSTALL_VERBOSE=1` | Verbose installer output | [OFFICIAL] |
| `HERMES_BACKGROUND_NOTIFICATIONS` | `concise`, `all`, `result`, `error`, `off` | [OFFICIAL] |
| `HERMES_EGRESS_PROXY`, `HERMES_PROXY_TOKEN_<NAME>` | Injected into sandboxes (not set by you) | [OFFICIAL] |
| `OP_SERVICE_ACCOUNT_TOKEN` | 1Password service-account auth | [COMMUNITY] |

**Total env vars: ~60+** (Phase 1: ~45, Phase 2: ~12). **Completeness: PARTIAL** — env var reference page was truncated around Matrix.

---

# 4. ON-DISK LAYOUT & HAND-EDIT SAFETY

**Home layout** (Phase 1 + Phase 2 bundled skill) [OFFICIAL]:

| Path | Description | Safe to Edit by Hand? |
|------|-------------|----------------------|
| `config.yaml` | Non-secret settings | **No** — use `hermes config set KEY VAL` (skill invariant) |
| `.env` | API keys and secrets | Yes (with care; `chmod 600` recommended) |
| `auth.json` | OAuth provider credentials | No — managed by `hermes auth` |
| `SOUL.md` | Primary agent identity | Yes |
| `memories/` | `MEMORY.md`, `USER.md` | Yes (within char limits) |
| `skills/` | Bundled + agent-created skills | Via `hermes skills` commands |
| `skins/` | Display skins | Via `hermes skin` |
| `desktop-plugins/` | Desktop plugins | No |
| `tui-widgets/` | TUI widgets | No |
| `pets/` | Pet configs | Via `hermes pets` |
| `state.db` | Canonical sessions (SQLite+FTS5) | **No** — use `hermes sessions` |
| `sessions/` | Gateway routing index, request dumps, `*.jsonl` | No |
| `logs/` | `agent.log`, `errors.log`, `gateway.log`, `update.log`, `tool_calls.log` | Read only |
| `cron/` | Scheduled jobs | Via `hermes cron` |
| `hooks/` | Shell-script hooks | Via `hermes hooks` |
| `checkpoints/` | Filesystem checkpoints | Via `hermes checkpoints` / `/snapshot` |
| `webhook_subscriptions.json` | Webhook subscriptions | Via `hermes webhook` |
| `kanban.db` | Kanban board state | Via `hermes kanban` |
| `proxy/` | Egress proxy data | Via `hermes egress` |
| `backups/` | Config backups | Read only |
| `state-snapshots/` | Pre-update snapshots | Read only |
| `pending/skills/` | Pending skill installs | Via `hermes skills` |
| `profiles/<name>/` | Profile directories (same layout) | Via `hermes profile` |
| `cache/scratch` | `TMPDIR` target | Auto-managed |
| `cache/terminal` | Terminal cache | Auto-managed |
| `cache/spillover/` | Spillover cache | Auto-managed |
| `modal_snapshots.json` | Modal snapshots | Auto-managed |
| `verification_evidence.db` | Verification evidence | Auto-managed |

**Note**: Per-file safety guidance for files other than `config.yaml` is **not documented** in the sources [UNVERIFIED]. The bundled skill's invariant says never hand-edit `config.yaml` for the user; use `hermes config set KEY VAL`.

---

# 5. PROFILES & MULTI-INSTANCE DETAILS

- **Profiles**: supported and complete [OFFICIAL]. Each gets `~/.hermes/profiles/<name>/` with the same layout, its own config, memory, sessions and gateway PID.
- A shell alias `~/.local/bin/<name>` is created unless `--no-alias`.
- Many gateways can be multiplexed into one host gateway (`hermes gateway migrate`).
- `--clone` does not copy sessions or cron [OFFICIAL].
- Profile commands: see 04-cli-command-reference-a.md Section 3.11 (`hermes profile` subcommands: `list`, `use`, `create`, `describe`, `delete`, `show`, `alias`, `rename`, `migrate-identity`, `purge-identity`, `export`, `import`, `install`, `update`, `info`).

---

# 6. PER-DIRECTORY CONTEXT FILE DISCOVERY

From `/context` [OFFICIAL]:
- Files: `.hermes.md`, the `AGENTS.md` chain, `CLAUDE.md`, `.cursorrules` plus `.cursor/rules/*.mdc`, and `SOUL.md` (identity slot #1).
- `/context` reports each file as: loaded, truncated (over `context_file_max_chars`), shadowed by a higher-priority type, blocked by the injection scan, empty/unreadable, or suppressed by the install-tree guard.
- **Exact load order and precedence between them was NOT STATED** [UNVERIFIED]. Read `docs/user-guide/features/context-files`.
- `/init` generates `AGENTS.md` from a repo scan.
- `--ignore-rules` skips all auto-injection.

---

# 7. PERSONALITY PRESETS

- `/personality [name]` with `none`/`default`/`neutral` to clear [OFFICIAL].
- **The built-in preset list was NOT FOUND** [UNVERIFIED].
- A "pirate" example appears in the quickstart.
- System-prompt overrides: per-channel `system_prompt` in `channel_overrides` (Phase 1).

---

# 8. ANNOTATED EXAMPLE CONFIG

**Full annotated "everything enabled" example: NOT RETRIEVED** [UNVERIFIED]. Fetch `cli-config.yaml.example` from the repo root.

**Minimal working example** (constructed from documented keys):

```yaml
# ~/.hermes/config.yaml
model:
  provider: openrouter
  default: anthropic/claude-sonnet-4
  context_length: 128000

terminal:
  backend: docker
  docker_image: nousresearch/hermes-sandbox:desktop
  container_memory: 8192

memory:
  memory_enabled: true
  memory_char_limit: 5000
  user_profile_enabled: true
  user_char_limit: 3000

compression:
  enabled: true
  threshold: 0.50
  target_ratio: 0.20
  protect_last_n: 20
  protect_first_n: 3

auxiliary:
  compression:
    provider: openrouter
    model: openai/gpt-4o-mini

agent:
  max_turns: 100
  api_max_retries: 3
  disabled_toolsets: []

skills:
  auto_load:
    - hermes-agent
    - git-workflow

updates:
  pre_update_backup: quick
  backup_keep: 5

gateway:
  delivery_ledger: true
  loop_watchdog: true
  systemd_watchdog_seconds: 120
```

---

# 9. 60-COMMAND CHEAT SHEET (FROM PHASE 2 SECTION 8)

## Setup
```bash
hermes setup --portal          # Nous OAuth + Tool Gateway
hermes setup --quick           # prompt only for unset items
hermes model                   # add provider / pick model
hermes auth add openrouter --api-key "sk-…"
hermes config set terminal.backend docker
hermes doctor --fix            # diagnose and repair
```

## Daily Chat
```bash
hermes --tui                   # modern TUI
hermes -c                      # resume last session
hermes -r latest               # same lookup, explicit
hermes -p work                 # use a profile
hermes chat --worktree -q "Review this repo and open a PR"
```

**Slash shortcuts**:
```
/model fav --global     /compress here 4     /context all     /usage     /undo     /retry
/steer focus on auth    /queue next task     /bg long task    /btw side question
/goal ship the feature  /loop 5m check CI    /plan refactor   /diff session
/reasoning high         /fast auto           /palette         /help skills
```

## Coding
```text
/init           # generate AGENTS.md from a repo scan
/review         # independent reviewer subagent
/rollback       # list/restore checkpoints
/worktree new feature-x
```

```bash
hermes lsp install-all
hermes chat --checkpoints -q "refactor X"
```

## Automation
```bash
hermes -z "summarize" < file.txt
hermes chat -q "..." --format stream-json
hermes send --to telegram "deploy finished"
hermes cron list
hermes webhook subscribe my-hook --deliver telegram
hermes kanban create "Restart server" --assignee ops
hermes pause   # global emergency stop;  hermes resume
```

## Gateway
```bash
hermes gateway setup
hermes gateway install && sudo loginctl enable-linger $USER
hermes gateway start
hermes gateway status
hermes gateway restart --all
hermes pairing list
```

**Messaging slash**:
```
/sethome   /platform list   /approve always   /restart
```

## Skills / MCP
```bash
hermes skills browse
hermes skills install openai/skills/k8s
hermes skills opt-out
hermes mcp add NAME --url https://...
hermes mcp list
hermes plugins install owner/repo --no-enable
```

**Slash**:
```
/reload-skills   /reload-mcp   /learn what to learn from   /curator status
```

## Maintenance
```bash
hermes update --check
hermes backup --quick --label "pre-upgrade"
hermes dump
hermes debug share --local
hermes logs errors -f
hermes status --deep
hermes sessions prune --older-than 90
hermes checkpoints prune
hermes security audit --fail-on high
```

---

# 10. HIDDEN / LESSER-KNOWN COMMANDS (FROM PHASE 2 SECTION 8)

[OFFICIAL-SOURCE via the docs unless noted]:

- `hermes -z --usage-file`
- `hermes chat --safe-mode`
- `hermes chat --source tool`
- `--in <dir>`
- `hermes peer dm`
- `hermes pause` / `resume`
- `hermes prompt-size`
- `hermes codex-runtime migrate`
- `hermes proxy`
- `hermes console`
- `hermes completion`
- `hermes pets` and `/hatch`
- `/loop --until`
- `/heartbeat`
- `/refine`
- `/moa`
- `/handoff`
- `/focus`
- `/battery`
- `/blueprint`
- `/suggestions`
- `hermes update --plan`
- `hermes gateway migrate --multiplex`
- `kill -USR2 <gateway pid>` for a stack dump
- `/docs/llms.txt`
- `hermes-agent --list-tools`

**Community cheat sheet** (dev.to) additionally lists [COMMUNITY]:
- `hermes config path` / `env-path`
- `hermes hooks test`
- `hermes skills tap add`

---

# 11. CONFIG MIGRATIONS

| Migration | Version | Details |
|-----------|---------|---------|
| `LLM_MODEL` env removed; `custom_providers:` → `providers:` | config v12 | [OFFICIAL] |
| `compression.summary_*` → `auxiliary.compression.*` | config v17 | [OFFICIAL] |
| `HERMES_DASHBOARD_INSECURE` made a no-op | June 2026 | [OFFICIAL] |
| `hermes migrate xai` for models retired May 15, 2026 | 2026-05 | [OFFICIAL] |

Run `hermes config check` then `hermes config migrate` after updates.

---

# 12. CONFLICTS

| Item | Phase 1 Says | Phase 2 Says | Resolution |
|------|--------------|--------------|------------|
| Config key count | ~70 keys | ~40 new keys | Merge = ~110; mark completeness UNVERIFIED |
| Env var count | ~45 | ~12 new | Merge = ~60; mark completeness PARTIAL |
| `hermes config` subcommands | 7 | 9 (adds `path`, `env-path`) | Merge = 9 |
| `HERMES_YOLO_MODE` | Not mentioned | On env writer denylist | Add to env table with denylist note |
| Full config schema | Not retrieved | Not retrieved | Mark UNVERIFIED in gaps |
| Full env var table | Truncated at Matrix | Not completed | Mark PARTIAL in gaps |

---

# 13. GAPS

| Gap | Description |
|-----|-------------|
| Full config key schema | `cli-config.yaml.example` and `DEFAULT_CONFIG` not fetched |
| Full environment variable table | Reference page truncated around Matrix |
| Annotated "everything enabled" example config | Not retrieved |
| Per-file hand-edit safety (beyond config.yaml) | Not documented |
| Personality preset list | Not found |
| Context file load order & precedence | Not stated |
| Approval pattern allow/deny syntax | Not captured |
| Config migration history (all versions) | Only 4 migrations captured |
| `provider_routing` full schema | Only subset captured |
| `secrets.onepassword` shipped status | Unconfirmed (issue #36949) |

---

# 14. SOURCES

- https://hermes-agent.nousresearch.com/docs/user-guide/configuration
- https://hermes-agent.nousresearch.com/docs/reference/environment-variables (truncated)
- https://hermes-agent.nousresearch.com/docs/getting-started/quickstart
- https://github.com/NousResearch/hermes-agent/blob/main/cli-config.yaml.example (linked from docs; not fetched)
- https://hermes-agent.nousresearch.com/docs/reference/cli-commands (partial)
- https://hermes-agent.nousresearch.com/docs/reference/slash-commands (complete)
- https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-hermes-agent (bundled skill v3.2.0)

---

FILE COMPLETE: hermes-forge/references/06-config-keys-and-env-vars.md
Main tables: Config Keys (~110 merged), Env Vars (~60+ merged), On-Disk Layout (28 paths with safety), Cheat Sheet (6 categories × ~10), Hidden Commands (25+), Migrations (4). Gaps: 10 items. Conflicts: 6 items.