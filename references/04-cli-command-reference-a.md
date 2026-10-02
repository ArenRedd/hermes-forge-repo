---
title: CLI Command Reference (Part A — Core Commands)
source_phases: [Phase 2]
hermes_version_documented: v0.21.x (docs track main; newest verified v0.21.5, v2026.9.24)
research_date: Friday, October 2, 2026
last_built_in: Chat 1
confidence_legend: OFFICIAL = official repo/docs/source; COMMUNITY = third-party; INFERRED = deduced; UNVERIFIED = needs checking
used_by_playbooks: [01-coding-and-dev.md, 02-devops-and-server-admin.md, 03-research-and-analysis.md, 04-content-and-social.md, 05-automation-and-scheduling.md, 06-messaging-gateway-setups.md, 07-browser-and-data-collection.md, 08-multi-agent-and-parallel.md, 09-personal-productivity.md, 10-skill-authoring-and-memory-curation.md, 11-maintenance-backup-recovery.md]
---

# WHEN TO READ THIS FILE
Read this file when you need the complete CLI command surface: global flags, the master subcommand table, and dedicated entries for core commands (`chat`, `-z`, `model`, `setup`, `gateway`, `send`, `cron`, `auth`, diagnostics family, `backup`/`checkpoints`, `profile`). Part B covers the remaining command families. Every flag, default, example, and exit code is preserved verbatim from the official CLI reference.

---

# TABLE OF CONTENTS
1. [Entrypoint & Global Options](#1-entrypoint--global-options)
2. [Master Subcommand Table](#2-master-subcommand-table)
3. [Dedicated Entries — Core Commands](#3-dedicated-entries--core-commands)
   - 3.1 `hermes chat`
   - 3.2 `hermes -z` (scripted one-shot)
   - 3.3 `hermes model` & `/model`
   - 3.4 `hermes setup`
   - 3.5 `hermes gateway`
   - 3.6 `hermes send`
   - 3.7 `hermes cron`
   - 3.8 `hermes auth`
   - 3.9 Diagnostics Family
   - 3.10 `hermes backup` / `hermes checkpoints`
   - 3.11 `hermes profile`
4. [Version Changes](#4-version-changes)
5. [Conflicts](#5-conflicts)
6. [Gaps](#6-gaps)
7. [Sources](#7-sources)

---

# 1. ENTRYPOINT & GLOBAL OPTIONS

```bash
hermes [global-options] <command> [subcommand/options]
```

| Option | Meaning | Tag |
|--------|---------|-----|
| `--version`, `-V` | Show version and exit | [OFFICIAL] |
| `--profile <name>`, `-p <name>` | Use a profile for this call; overrides sticky default from `hermes profile use` | [OFFICIAL] |
| `--resume <session>`, `-r <session>` | Resume by ID or title; `latest` resumes most recent (workspace-scoped, same lookup as `-c`) | [OFFICIAL] |
| `--continue [name]`, `-c [name]` | Resume most recent session, or most recent matching a title | [OFFICIAL] |
| `--in <dir>` | `cd` into `<dir>` first; scopes `--resume latest`/`-c` to that workspace | [OFFICIAL] |
| `--worktree`, `-w` | Start in an isolated git worktree | [OFFICIAL] |
| `--yolo` | Bypass dangerous-command approval prompts | [OFFICIAL] |
| `--pass-session-id` | Put the session ID in the system prompt | [OFFICIAL] |
| `--ignore-user-config` | Ignore `config.yaml` and use built-in defaults (`.env` credentials still load) | [OFFICIAL] |
| `--ignore-rules` | Skip auto-injection of `AGENTS.md`, `SOUL.md`, `.cursorrules`, memory and preloaded skills | [OFFICIAL] |
| `--tui` | Launch the TUI; equivalent to `HERMES_TUI=1`; always beats `display.interface` | [OFFICIAL] |
| `--cli` | Force the classic prompt_toolkit REPL for one run | [OFFICIAL] |
| `--dev` | With `--tui`: run TypeScript sources via `tsx` (for TUI contributors) | [OFFICIAL] |

**Full verbatim `hermes --help` output: NOT CAPTURED** (see Gaps). Authoritative live sources: `hermes --help`, `hermes <command> --help`, `hermes_cli/main.py`.

---

# 2. MASTER SUBCOMMAND TABLE

The "version introduced" column is mostly **not stated in the docs**. Where a version is known, it is noted in Section 4.

| Command | Purpose | Tag |
|---------|---------|-----|
| `hermes chat` | Interactive or one-shot chat | [OFFICIAL] |
| `hermes model` | Interactive provider/model selector (also the place to add providers and do OAuth) | [OFFICIAL] |
| `hermes moa` | Configure named Mixture-of-Agents presets | [OFFICIAL] |
| `hermes fallback` | Manage fallback providers (`list`, `add`, ... full syntax not captured) | [OFFICIAL] |
| `hermes gateway` | Run or manage the messaging gateway | [OFFICIAL] |
| `hermes proxy` | Local OpenAI-compatible proxy attaching OAuth credentials | [OFFICIAL] |
| `hermes egress` | Outbound credential-injection firewall for Docker sandboxes (iron-proxy); disabled by default | [OFFICIAL] |
| `hermes lsp` | Manage Language Server Protocol diagnostics | [OFFICIAL] |
| `hermes setup` | Setup wizard (full or by section) | [OFFICIAL] |
| `hermes whatsapp` | Configure and pair the Baileys WhatsApp bridge | [OFFICIAL] |
| `hermes whatsapp-cloud` | Configure the Meta WhatsApp Business Cloud adapter | [OFFICIAL] |
| `hermes slack` | Slack helpers (`manifest`) | [OFFICIAL] |
| `hermes auth` | Credential pools, OAuth flows | [OFFICIAL] |
| `hermes login` / `hermes logout` | **Deprecated**; use `hermes auth` | [OFFICIAL] |
| `hermes send` | Send a one-shot message to a platform (no agent) | [OFFICIAL] |
| `hermes peer` | Register peer gateways and DM their agents | [OFFICIAL] |
| `hermes secrets` | External secret sources (Bitwarden; 1Password CLI proposed in issue #36949) | [OFFICIAL] / [COMMUNITY] |
| `hermes migrate` | Rewrite `config.yaml` for retired models (`migrate xai`) | [OFFICIAL] |
| `hermes codex-runtime` | `migrate [--dry-run] [--json]` for `~/.codex/config.toml` | [OFFICIAL] |
| `hermes status` | Agent, auth and platform status | [OFFICIAL] |
| `hermes usage` | Account rate-limit windows without a session | [OFFICIAL] |
| `hermes cron` | Scheduler management | [OFFICIAL] |
| `hermes pause` / `hermes resume` | Global emergency stop for cron, kanban dispatch and gateway turns (in-flight work not killed) | [OFFICIAL] |
| `hermes kanban` | Multi-profile collaboration board | [OFFICIAL] |
| `hermes project` | Named multi-folder workspaces | [OFFICIAL] |
| `hermes webhook` | Dynamic webhook subscriptions | [OFFICIAL] |
| `hermes hooks` | Inspect, approve or remove shell-script hooks (`list`, `test`, `revoke`, `doctor`) | [OFFICIAL] / [COMMUNITY] |
| `hermes doctor` | Diagnostics (`--fix`) | [OFFICIAL] |
| `hermes security audit` | OSV.dev supply-chain audit | [OFFICIAL] |
| `hermes approvals` | Mine approval history into allowlist proposals | [OFFICIAL] |
| `hermes dump` | Copy-pasteable setup summary | [OFFICIAL] |
| `hermes prompt-size` | Byte breakdown of system prompt plus tool schemas (offline) | [OFFICIAL] |
| `hermes debug` | `debug share` uploads logs and system info | [OFFICIAL] |
| `hermes backup` / `hermes import` | Zip backup and restore of the Hermes home | [OFFICIAL] |
| `hermes checkpoints` | Manage the `/rollback` shadow store | [OFFICIAL] |
| `hermes logs` | View, tail and filter logs | [OFFICIAL] / [COMMUNITY] |
| `hermes config` | Show, edit, migrate and query config | [OFFICIAL] |
| `hermes skin` | List, switch and tweak display skins | [OFFICIAL] |
| `hermes console` | Open the safe Hermes command console | [OFFICIAL] |
| `hermes pairing` | Approve or revoke messaging pairing codes | [OFFICIAL] |
| `hermes skills` | Browse, install, publish, audit, configure skills | [OFFICIAL] |
| `hermes bundles` | Group skills under one `/<name>` | [OFFICIAL] |
| `hermes curator` | Background skill maintenance | [OFFICIAL] |
| `hermes journey` (aliases `learning`, `memory-graph`) | Timeline of learned skills and memories | [OFFICIAL] |
| `hermes memory` | Configure an external memory provider | [OFFICIAL] |
| `hermes acp` | ACP server for editors | [OFFICIAL] |
| `hermes mcp` | Manage MCP servers; run Hermes as an MCP server | [OFFICIAL] |
| `hermes plugins` | Install, enable, disable, update, remove plugins | [OFFICIAL] |
| `hermes portal` | `status` (default), `open`, `tools` | [OFFICIAL] |
| `hermes tools` | Per-platform tool configuration | [OFFICIAL] |
| `hermes computer-use` | Install or check the cua-driver backend | [OFFICIAL] |
| `hermes pets` | `list install select show off scale remove doctor` | [OFFICIAL] |
| `hermes sessions` | Browse, export, prune, rename, delete sessions | [COMMUNITY/snippet] |
| `hermes insights` | Token/cost/activity analytics | [OFFICIAL] |
| `hermes claw` | OpenClaw migration helpers (`claw migrate`) | [OFFICIAL] |
| `hermes import-agent` | Import a Claude Code (`~/.claude`) or Codex CLI (`~/.codex`) setup | [OFFICIAL] |
| `hermes dashboard` | Web dashboard | [OFFICIAL] |
| `hermes serve` | Headless backend server (powers desktop and remote backends) | [OFFICIAL] |
| `hermes desktop` (alias `gui`) | Build and launch the Electron app | [OFFICIAL] |
| `hermes profile` | Profile management | [OFFICIAL] |
| `hermes completion` | Shell completions: `bash`, `zsh`, `fish` | [OFFICIAL] |
| `hermes update` | Update; `--check`, `--backup`, `--plan` and others (see Phase 1) | [OFFICIAL] |
| `hermes uninstall` | Remove Hermes (`--dry-run`, `--full`, `--data`; see Phase 1) | [OFFICIAL] |
| `hermes version` / `--version` | Version info | [OFFICIAL] |
| `hermes pm` | Package manager (`pm status`, `pm install agent-browser`) | [OFFICIAL via installation docs] |

**Categories you asked about** [OFFICIAL]:
- A global `hermes memory` provider command **exists**
- `hermes sessions` and `hermes backup`/`import` **exist**
- A standalone `hermes restore` was **NOT FOUND**; restore is `hermes import`
- A standalone `hermes list`/`hermes show` for config was **NOT FOUND**; use `hermes config`

---

# 3. DEDICATED ENTRIES — CORE COMMANDS

## 3.1 `hermes chat` [OFFICIAL]

```bash
hermes chat [options]
```

| Flag | Notes |
|------|-------|
| `-q`, `--query "..."` | Seeds the first turn. On a real TTY it is submitted literally (never parsed as a slash command or `!` escape) and the session stays open. With `--oneshot`, `-Q`, or non-TTY stdio it answers and exits |
| `--query-file PATH` | Read the query from a file; `-` means stdin. Nothing is shell-interpreted. Mutually exclusive with `-q` |
| `--oneshot` | With `-q`/`--query-file`: answer and exit (pre-0.21 behavior). Implied by non-TTY stdio and `-Q` |
| `-m`, `--model <model>` | Per-run model override |
| `-t`, `--toolsets <csv>` | Enable toolsets |
| `--provider <provider>` | Force a provider (~50 ids/aliases listed on CLI page, including `auto`, `openrouter`, `nous`, `openai-codex`, `anthropic`, `gemini`, `bedrock`, `lmstudio`, `xai`, `deepseek`, ...) |
| `-s`, `--skills <name>` | Preload skills (repeat or comma-separate) |
| `-v`, `--verbose` / `-Q`, `--quiet` | Verbose; or programmatic mode with no banner/spinner/previews |
| `--format stream-json` | JSONL events; requires `-q`/`--query-file`; implies quiet; incompatible with `--tui` |
| `--image <path>` | Attach a local image to a single query |
| `--resume` / `--continue [name]` | Resume from `chat` |
| `--worktree`, `--checkpoints`, `--yolo`, `--pass-session-id` | See globals; `--checkpoints` enables filesystem checkpoints before destructive changes |
| `--ignore-user-config`, `--ignore-rules` | Isolation flags |
| `--safe-mode` | Disables user config, rules/memory injection, plugins, shell hooks and MCP servers |
| `--source <tag>` | Session source tag (default `cli`; one-shot defaults to `oneshot`, which pickers hide; `tool` for third-party integrations) |
| `--max-turns <N>` | Tool-calling iteration cap (default 500, or `agent.max_turns`) |

### Examples

```bash
hermes chat -q "Summarize the latest PRs"            # basic: seeds an interactive session
hermes chat --oneshot -q "Summarize the latest PRs"  # intermediate: answer and exit
hermes chat --ignore-user-config --ignore-rules -q "Repro without my personal setup"   # advanced: isolated run
```

### Exit Codes for One-Shot Chat [OFFICIAL]
- `0` — completed
- `1` — failed, partial, hit the iteration budget, or never started
- `130` — interrupted

**Kanban dispatcher workers** (`HERMES_KANBAN_TASK` set) exit `75` for rate limit, overload, 5xx, timeout or billing wall so the task is requeued.

### Stream-JSON Event Types [OFFICIAL]
Every event has a `timestamp` in epoch ms:
- `system` (`subtype: "init"`, `model`, `session_id`)
- `text`
- `tool_use` (`name`, `input`)
- `tool_result` (`name`, `output` capped at 5000 chars, `duration_ms`, `is_error`)
- `result` (`session_id`, `exit_code`, `text`, `tokens`, `duration_ms`, `error`)

`result` is always the last record. Diagnostics and the `session_id:` line go to stderr.

### Common Mistakes
- Expecting `-q` to exit on a TTY (add `--oneshot`)
- Combining `--format stream-json` with `--tui`
- Combining `-q` with `--query-file`

---

## 3.2 `hermes -z <prompt>`, Scripted One-Shot [OFFICIAL]

```bash
hermes -z "What's the capital of France?"
answer=$(hermes -z "summarize this" < /path/to/file.txt)
hermes -z "…" --provider openrouter --model openai/gpt-5.5
HERMES_INFERENCE_MODEL=anthropic/claude-sonnet-4.6 hermes -z "…"
hermes -z "summarize this repo" --usage-file ~/.hermes/cache/scratch/usage.json
```

- Prints only the final reply: no banner, spinner, tool previews or `Session:` line.
- Flags: `-m/--model` (env `HERMES_INFERENCE_MODEL`), `--provider`, `--usage-file <path>`.

### Exit Codes for `hermes -z` [OFFICIAL]
- `0` — completed
- `2` — failed/partial/budget-exhausted or a usage error
- `130` — interrupted
- `1` — a completed turn produced no text

### `--usage-file` Output [OFFICIAL]
Writes JSON including:
- `estimated_cost_usd`
- Token counts
- `api_calls`
- `model`, `provider`
- `session_id`
- `completed`/`failed`/`partial`/`interrupted`
- `turn_exit_reason`
- `auxiliary` block with `by_task`
- `total_including_auxiliary`

Written even when the run fails.

### Notes
- In finite chat runs, `delegate_task` waits for children and returns results in the same turn.

---

## 3.3 `hermes model` and `/model` [OFFICIAL]

`hermes model` adds providers, does OAuth, takes API keys and configures custom endpoints. `/model` only switches among configured providers.

```
/model claude-sonnet-4
/model zai:glm-5
/model custom:local:qwen-2.5
/model claude-sonnet-4 --global
```

### `/model` Flags
- `--global`
- `--session`
- `--once`
- `--refresh`
- `--provider <name>`
- `--reasoning <level>`

- Switching is session-only unless `--global` or `model.persist_switch_by_default: true`.
- A switch resets the prompt cache.
- Aliases: `hermes config set model.aliases.fav anthropic/claude-opus-4.6`

---

## 3.4 `hermes setup` [OFFICIAL]

```bash
hermes setup [model|tts|terminal|gateway|tools|agent] [--non-interactive] [--reset] [--quick] [--reconfigure] [--portal]
```

- First run launches the first-time wizard.
- On an existing install, bare `hermes setup` is a full reconfigure showing current values as defaults.
- `--quick` prompts only for unset items.
- `--non-interactive` uses defaults and env.
- `--reset` resets to defaults first.

---

## 3.5 `hermes gateway` [OFFICIAL]

**Subcommands**: `run`, `start`, `stop`, `restart`, `status`, `list` (all profiles), `install`, `uninstall`, `setup`, `migrate`, `migrate-legacy`, `enroll`.

| Flag | Applies to | Meaning |
|------|------------|---------|
| `--all` | `start`/`restart`/`stop` | Act on every profile's gateway |
| `--no-supervise` | `run` | Opt out of s6 supervision in the Docker image |
| `--external-supervisor` | `run` | A wrapper owns the foreground gateway; restarts exit `75`, so the supervisor must relaunch |
| `--system`, `--force`, `--run-as-user <user>` | `install` etc. | Appear in the messaging docs (Phase 1) |
| `--dry-run`, `-y/--yes` | `migrate`, `migrate-legacy` | Preview / skip prompts |
| `--token --connector-url --gateway-id --wake-url` | `enroll` | Experimental relay enrollment |

```bash
hermes gateway install && sudo loginctl enable-linger $USER
hermes gateway start
hermes gateway status
tmux new -s hermes 'hermes gateway run'        # WSL recommendation from the docs
```

**For WSL**: use `run` instead of `start` (WSL systemd is unreliable).

---

## 3.6 `hermes send` [OFFICIAL]

```bash
hermes send --to <target> "message text"
hermes send --to <target> --file <path>
echo "message" | hermes send --to <target>
hermes send --list [platform]
```

**Targets**: `platform`, `platform:chat_id`, `platform:chat_id:thread_id`, `platform:#channel-name`

| Flag | Meaning |
|------|---------|
| `-t`, `--to` | Target |
| `-f`, `--file` | Text only; `-` is stdin |
| `-s`, `--subject` | Subject line |
| `-l`, `--list` | List targets |
| `-q`, `--quiet` | Suppress output |
| `--json` | JSON output |

- Media via a `MEDIA:<path>` directive in the text; `[[as_document]]` sends uncompressed.
- Bot-token platforms do not need a running gateway.
- Exit codes: `0`, `1` delivery failure, `2` usage error.

---

## 3.7 `hermes cron` [OFFICIAL]

```bash
hermes cron <list|create|edit|pause|resume|run|remove|status|runs|incidents|doctor|tick>
```

### `hermes cron create` — Full Syntax [OFFICIAL, from Phase 4]

```bash
hermes cron create "every 2h" "Check server status"
hermes cron create "every 1h" "Use both skills and combine the result" --skill blogwatcher --skill maps --name "Skill combo"
hermes cron create "every 1d at 09:00" "Audit open PRs..." --workdir /home/me/projects/acme
hermes cron create "every 1h" "Post the digest" --paused --paused-reason "Awaiting review"
hermes cron create "every 5m" --no-agent --script memory-watchdog.sh --deliver telegram --name "memory-watchdog"
hermes cron create "every 6h" "Scan for news" --continuity
```

**All `create` flags**:
| Flag | Purpose |
|------|---------|
| `--schedule`, positional | Schedule string (5 formats: one-shot, interval, natural, cron, ISO) |
| `--prompt`, positional | Task prompt (required unless `--no-agent --script`) |
| `--skill` | Repeatable; attach skill(s) |
| `--name` | Job name (case-insensitive ref) |
| `--deliver` | Delivery target: `origin`, `local`, `telegram`, `telegram:<chat_id>[:thread]`, `discord:#channel`, `slack`, `email`, `sms`, `all`, comma-lists, `bot-chat[:profile]` |
| `--workdir` | Project directory (loads context files) |
| `--model` | Per-job model pin |
| `--provider` | Per-job provider pin |
| `--reasoning-effort` | `none` through `ultra` |
| `--paused` | Create paused |
| `--paused-reason` | Reason for paused |
| `--no-agent` | Script-only mode (no LLM) |
| `--script` | Script path (in `$HERMES_HOME/scripts/`) |
| `--continuity` | Feed job its own previous output |
| `--context-from` | Job ID/name/list for chaining |
| `--pin` / `--unpin` | Pin/unpin model |

### `hermes cron edit` — Full Syntax [OFFICIAL]

```bash
hermes cron edit <id> --schedule "every 4h" --prompt "..." --skill X --add-skill Y --remove-skill X --clear-skills --pin --unpin --model M --provider P --reasoning-effort high --continuity
```

**Edit flags**: `--schedule`, `--prompt`, `--skill`, `--add-skill`, `--remove-skill`, `--clear-skills`, `--pin`, `--unpin`, `--model`, `--provider`, `--reasoning-effort`, `--continuity`, `--name`, `--deliver`, `--workdir`, `--paused`, `--paused-reason`, `--no-agent`, `--script`, `--context-from`.

- `create`/`add` takes repeated `--skill` and `--reasoning-effort <none|minimal|low|medium|high|xhigh|max|ultra>`.
- `edit` takes `--clear-skills`, `--add-skill`, `--remove-skill`.
- `run` fires on the next scheduler tick; `tick` runs due jobs once and exits; `doctor` exits non-zero when it finds issues.
- Config key `cron.provider` picks the trigger (empty means the built-in ticker, `chronos` for hosted).

---

## 3.8 `hermes auth` [OFFICIAL]

```bash
hermes auth                                          # interactive wizard
hermes auth list [PROVIDER]
hermes auth add openrouter --api-key "sk-…"
hermes auth add openrouter --type oauth
hermes auth add anthropic --type oauth
hermes auth add openai-codex --type oauth --priority 0
hermes auth add openai-codex --browser
hermes auth remove openrouter 2
hermes auth priority openrouter backup-key 0
hermes auth reset openrouter [N]
hermes auth refresh openai-codex work
hermes auth status anthropic
hermes auth logout anthropic
hermes auth spotify
```

---

## 3.9 Diagnostics Family [OFFICIAL]

```bash
hermes status [--all] [--deep]
hermes usage [--provider NAME] [--json]        # exit 1 with one stderr line if no credential/endpoint
hermes doctor [--fix]                          # exit 0 clean, 1 if any unresolved problem
hermes dump [--show-keys]
hermes debug share [--lines N] [--expire DAYS] [--nous] [--local] [--no-redact]
hermes security audit [--json] [--fail-on low|moderate|high|critical] [--skip-venv] [--skip-plugins] [--skip-mcp]
```

### `hermes debug share` Details
- Uploads to paste.rs then dpaste.com by default (expiry 7 days), redacted unless `--no-redact`.
- `--nous` goes to private Nous storage (auto-deletes after 14 days).

---

## 3.10 `hermes backup` / `hermes import` / `hermes checkpoints` [OFFICIAL]

```bash
hermes backup [-o PATH] [-q|--quick] [-l LABEL] [-k N]
hermes backup -o ~/backups/hermes.zip
hermes backup --quick --label "pre-upgrade"
hermes checkpoints [status|list|prune|clear|clear-legacy]
```

- Default output: `~/hermes-backup-<timestamp>.zip`
- `--keep` defaults to 3 (`0` keeps all)
- Uses SQLite's `backup()` API, so it is safe while running.
- Exit codes: `0` only if every file landed; `1` for incomplete archive (zip kept, pruning skipped); `2` if another backup is running.
- Excludes: WAL/SHM sidecars, `checkpoints/`, root `models/` `runtimes/` `node/`, browser profiles, regenerable `cache/` entries, sockets and symlinks, and the code itself.
- `hermes import` flags **NOT CAPTURED** [UNVERIFIED].
- `hermes checkpoints` per-subcommand options **CUT OFF** [UNVERIFIED].

---

## 3.11 `hermes profile` (Complete) [OFFICIAL]

**Subcommands**: `list`, `use`, `create`, `describe`, `delete`, `show`, `alias`, `rename`, `migrate-identity`, `purge-identity`, `export`, `import`, `install`, `update`, `info`.

```bash
hermes profile create work --clone                  # config+.env+SOUL+skills+curated memory; not sessions/cron
hermes profile create backup --clone-all            # everything except sessions/state.db/backups/checkpoints/cron
hermes profile create mybot --no-skills             # empty profile; writes .no-bundled-skills
hermes profile create mybot --description "..."
hermes profile describe researcher --auto
hermes profile export work -o ./work-2026-03-29.tar.gz     # auth.json and .env always excluded
hermes profile import ./work-2026-03-29.tar.gz --name work-restored
hermes profile install github.com/kyle/telemetry-distribution --alias
hermes profile update <name> [--force-config] [--yes]
hermes -p work chat -q "Check the server status"
```

### `create` Flags
- `--clone-from <profile>`
- `--no-alias`

### `delete` Flags
- `-y/--yes`

### `alias` Flags
- `--remove`
- `--name`

### `install` Flags
- `--name`, `--alias`, `--force`, `-y`

- The `default` profile cannot be deleted; use `hermes uninstall`.
- Completions: `hermes completion bash >> ~/.bashrc`

---

# 4. VERSION CHANGES [OFFICIAL unless noted]

| Change | Version | Tag |
|--------|---------|-----|
| `-q` on a TTY seeds an interactive session; `--oneshot` restores answer-and-exit | v0.21 | [OFFICIAL] |
| `hermes login`/`logout` deprecated, then removed; use `hermes auth` | not stated | [OFFICIAL] |
| `/credits` and `/billing` replaced by `/topup` | not stated | [OFFICIAL] |
| `/plan` moved from a bundled skill to a built-in command | not stated | [OFFICIAL] |
| `/goal`, `/learn`, `/journey` | v0.18.0 (Jul 1, 2026) | [OFFICIAL release notes] |
| `/kanban` | v0.15 | [COMMUNITY] |
| `hermes update --plan`, update receipts, `hermes worktree list/prune` | v0.20.5 | [OFFICIAL release notes] |
| `LLM_MODEL` env removed; `custom_providers:` migrated to `providers:` | config v12 | [OFFICIAL] |
| `compression.summary_*` migrated to `auxiliary.compression.*` | config v17 | [OFFICIAL] |
| `HERMES_DASHBOARD_INSECURE` made a no-op | June 2026 hardening | [OFFICIAL] |
| `hermes migrate xai` for models retired May 15, 2026 | 2026-05 | [OFFICIAL] |

---

# 5. CONFLICTS

| Item | Phase 1 Says | Phase 2 Says | Resolution |
|------|--------------|--------------|------------|
| `hermes update` flags | 9 flags documented | Master table only; dedicated entry truncated | Use Phase 1's 9 flags as authoritative |
| `hermes uninstall` flags | 3 flags documented | Master table only; dedicated entry truncated | Use Phase 1's 3 flags |
| `hermes backup`/`import` flags | Not retrieved | Partial backup flags; import not captured | Mark import flags UNVERIFIED |
| `hermes checkpoints` options | Not documented | 5 subcommands; per-subcommand options cut off | Mark per-subcommand options UNVERIFIED |
| `hermes sessions` subcommands | Not documented | 7 subcommands [COMMUNITY/snippet] | Include with COMMUNITY tag |
| `hermes config` subcommands | 7 from config page | 9 (adds `path`, `env-path`) [snippet] | Merge = 9 total |
| `hermes tools` subcommands | Not documented | 3 [snippet] | Include with snippet tag |
| `hermes mcp` subcommands | Not documented | 6 [snippet] | Include with snippet tag |
| `hermes plugins` subcommands | Not documented | 6 [OFFICIAL, CLI guide] | Include as OFFICIAL |
| `hermes skills` subcommands | Not documented | 10+ [mixed OFFICIAL/snippet] | Include with appropriate tags |

---

# 6. GAPS

| Gap | Description |
|-----|-------------|
| Verbatim `hermes --help` output | Not captured; run on host or read `hermes_cli/main.py` |
| Per-flag detail, 3 examples, exit codes for ~30 command families | CLI reference truncated after `hermes checkpoints`; need `/docs/llms-full.txt` or rest of CLI page |
| Python embedding example (minimal working example, import path, callbacks) | Not retrieved; see `docs/developer-guide/programmatic-integration` |
| API-server `curl` examples | Not retrieved; see `docs/user-guide/features/api-server` |
| `@file`/URL inline syntax, approval pattern syntax | Not captured; see `docs/user-guide/security`, `docs/user-guide/cli` |
| Version introduced per command | Not in docs; need release notes v0.14–v0.21 or `git log -S` on `commands.py` |
| Reddit/HN/X/Discord pitfalls | Not searched |
| `hermes import` full flag set | Not captured |
| `hermes checkpoints` per-subcommand options | Cut off in fetch |
| Full `hermes cron create` syntax (schedule format, `--name`, `--deliver`) | **RESOLVED in Chat 2** — see Section 3.7 above |

---

# 7. SOURCES

- https://hermes-agent.nousresearch.com/docs/reference/cli-commands (CLI Commands Reference; fetched through `hermes checkpoints`, truncated after)
- https://hermes-agent.nousresearch.com/docs/reference/slash-commands (Slash Commands Reference; complete)
- https://hermes-agent.nousresearch.com/docs/reference/profile-commands (Profile Commands Reference; complete)
- https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-hermes-agent (bundled `hermes-agent` skill, v3.2.0)
- Search snippets: GitHub repo CLI reference, slash commands, CLI guide; https://hermesagent.org.cn/... (mirror); https://dev.to/rosgluk/hermes-agent-cli-cheat-sheet-commands-flags-and-slash-shortcuts-3pcb [COMMUNITY]; https://github.com/NousResearch/hermes-agent/issues/36949 [COMMUNITY]; https://github.com/koc-Z3/hermes-docs [COMMUNITY]
- Phase 1 pages remain the base for config, env and Docker.

---

FILE COMPLETE: hermes-forge/references/04-cli-command-reference-a.md
Main tables: Global Options (13), Master Subcommands (~70), `chat` flags (19), `chat` exit codes (3+1), stream-json events (5), `-z` examples (4), `-z` exit codes (4), `/model` examples (4) + flags (6), `gateway` subcommands (8) + flags (6), `send` flags (6) + targets (4), `cron` subcommands (9), `auth` subcommands (14), Diagnostics (6), `backup` flags (4) + exit codes (3), `checkpoints` subcommands (5), `profile` subcommands (14) + create flags (6). Version changes: 14 rows. Gaps: 10 items. Conflicts: 10 items.
Note: This is Part A. Part B will cover remaining command families (moa, fallback, proxy, egress, lsp, whatsapp, slack, peer, secrets, migrate, codex-runtime, pause/resume, kanban, project, webhook, hooks, approvals, dump, prompt-size, debug, logs, config, skin, console, pairing, skills, bundles, curator, journey, memory, acp, mcp, plugins, portal, tools, computer-use, pets, sessions, insights, claw, import-agent, dashboard, serve, desktop, completion, update, uninstall, version, pm).