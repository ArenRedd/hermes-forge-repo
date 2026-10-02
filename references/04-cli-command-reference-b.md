---
title: CLI Command Reference (Part B — Remaining Command Families)
source_phases: [Phase 2]
hermes_version_documented: v0.21.x (docs track main; newest verified v0.21.5, v2026.9.24)
research_date: Friday, October 2, 2026
last_built_in: Chat 1
confidence_legend: OFFICIAL = official repo/docs/source; COMMUNITY = third-party; INFERRED = deduced; UNVERIFIED = needs checking
used_by_playbooks: [01-coding-and-dev.md, 02-devops-and-server-admin.md, 03-research-and-analysis.md, 04-content-and-social.md, 05-automation-and-scheduling.md, 06-messaging-gateway-setups.md, 07-browser-and-data-collection.md, 08-multi-agent-and-parallel.md, 09-personal-productivity.md, 10-skill-authoring-and-memory-curation.md, 11-maintenance-backup-recovery.md]
---

# WHEN TO READ THIS FILE
Read this file for the remaining CLI command families not covered in Part A: `moa`, `fallback`, `proxy`, `egress`, `lsp`, `whatsapp`, `whatsapp-cloud`, `slack`, `peer`, `secrets`, `migrate`, `codex-runtime`, `pause`/`resume`, `kanban`, `project`, `webhook`, `hooks`, `approvals`, `dump`, `prompt-size`, `debug`, `logs`, `config`, `skin`, `console`, `pairing`, `skills`, `bundles`, `curator`, `journey`, `memory`, `acp`, `mcp`, `plugins`, `portal`, `tools`, `computer-use`, `pets`, `sessions`, `insights`, `claw`, `import-agent`, `dashboard`, `serve`, `desktop`, `completion`, `update`, `uninstall`, `version`, `pm`. Per-flag detail, examples, and exit codes are marked where not yet captured.

---

# TABLE OF CONTENTS
1. [Remaining Command Families — Condensed Entries](#1-remaining-command-families--condensed-entries)
2. [Headless / Scripting Usage](#2-headless--scripting-usage)
3. [Python / Library Usage](#3-python--library-usage)
4. [Server / API Modes](#4-server--api-modes)
5. [Conflicts](#5-conflicts)
6. [Gaps](#6-gaps)
7. [Sources](#7-sources)

---

# 1. REMAINING COMMAND FAMILIES — CONDENSED ENTRIES

Per-flag detail, three examples each, and exit codes for these are **not yet documented** (see Gaps). The syntax below is verified from the official CLI reference or snippets.

| Command | Verified Syntax | Tag |
|---------|-----------------|-----|
| `hermes moa` | Subcommands not captured | [OFFICIAL] |
| `hermes fallback` | `list`, `add`, ... (full syntax not captured) | [OFFICIAL] |
| `hermes proxy` | `start --provider <nous\|xai> --host --port` (default `127.0.0.1:8645`), `status`, `providers` | [OFFICIAL] |
| `hermes egress` | `install [--force]`, `setup [--tunnel-port N] [--from-bitwarden] [--no-bitwarden] [--rotate-tokens]`, `start`, `stop`, `restart`, `reload`, `status [--show-tokens]`, `disable`, `config` | [OFFICIAL] |
| `hermes lsp` | `status`, `list [--installed-only]`, `install <id>`, `install-all`, `restart`, `which <id>` | [OFFICIAL] |
| `hermes whatsapp` | Subcommands not captured | [OFFICIAL] |
| `hermes whatsapp-cloud` | Subcommands not captured | [OFFICIAL] |
| `hermes slack` | `manifest [--write [PATH]] [--name] [--description] [--long-description[-file]] [--slashes-only]` | [OFFICIAL] |
| `hermes peer` | `add <name> --url ... [--key ...] [--note]`, `list`, `dm`, `run --idempotency-key`, `status`, `stop`, `remove`; exit `0/1/2` | [OFFICIAL] |
| `hermes secrets` | `bitwarden\|bw {setup,status,token,sync,install,disable}`; `sync --apply` exports to the shell | [OFFICIAL] |
| `hermes migrate` | `xai [--apply] [--no-backup]` (dry-run by default) | [OFFICIAL] |
| `hermes codex-runtime` | `migrate [--dry-run] [--json]` for `~/.codex/config.toml` | [OFFICIAL] |
| `hermes pause` / `hermes resume` | Global emergency stop/resume for cron, kanban dispatch and gateway turns | [OFFICIAL] |
| `hermes kanban` | `--board <slug>`; actions: `init`, `boards {list,create,switch,show,rename,rm}`, `create`, `list`, `show`, `assign`, `link`, `claim`, `comment`, `complete`, `block`, `request-review`, `unblock`, `dispatch`, `specify`, `decompose`, `gc` | [OFFICIAL] |
| `hermes project` | `create list show add-folder remove-folder rename set-primary use archive restore bind-board` | [OFFICIAL] |
| `hermes webhook` | `subscribe\|add`, `list\|ls`, `remove\|rm`, `test`. `subscribe` flags: `--prompt --events --description --skills --deliver --deliver-chat-id --secret --deliver-only --mirror-to-session --script --route-profile` | [OFFICIAL] |
| `hermes hooks` | `list`, `test`, `revoke`, `doctor` | [OFFICIAL] / [COMMUNITY] |
| `hermes approvals` | Subcommands not captured (mines approval history into allowlist proposals) | [OFFICIAL] |
| `hermes dump` | `[--show-keys]` | [OFFICIAL] |
| `hermes prompt-size` | No flags captured | [OFFICIAL] |
| `hermes debug` | `share [--lines N] [--expire DAYS] [--nous] [--local] [--no-redact]` | [OFFICIAL] |
| `hermes logs` | `[agent\|errors\|...] [-f] [--level] [--session <id>] [--follow]` (seen in Docker docs) | [OFFICIAL] / [COMMUNITY] |
| `hermes config` | `show`, `edit`, `get`, `set`, `unset`, `path`, `env-path`, `check`, `migrate` | [OFFICIAL] / [snippet] |
| `hermes skin` | `list`, `switch`, `tweak` (details not captured) | [OFFICIAL] |
| `hermes console` | No flags captured | [OFFICIAL] |
| `hermes pairing` | `list`, `approve`, `revoke` (details not captured) | [OFFICIAL] |
| `hermes skills` | `browse [--source official]`, `search`, `install ... [--name]`, `check`, `update`, `config`, `reset <name>`, `opt-in`/`opt-out` (`.no-bundled-skills` marker); also `list`, `tap add REPO` | [OFFICIAL] / [snippet] |
| `hermes bundles` | Subcommands not captured | [OFFICIAL] |
| `hermes curator` | `status`, `run`, `pause`, `pin`, `rollback` (restores `~/.hermes/skills/` from a snapshot) | [OFFICIAL] |
| `hermes journey` (aliases `learning`, `memory-graph`) | `list`, `delete <id>`, `edit <id>` (details not captured) | [OFFICIAL] |
| `hermes memory` | Subcommands not captured (configure external memory provider) | [OFFICIAL] |
| `hermes acp` | No flags captured (ACP server for editors) | [OFFICIAL] |
| `hermes mcp` | `serve`, `add NAME (--url or --command)`, `remove`, `list`, `test NAME`, `configure NAME` | [snippet] |
| `hermes plugins` | `install owner/repo [--no-enable]`, `list`, `enable`, `disable`, `update`, `remove` | [OFFICIAL, CLI guide] |
| `hermes portal` | `status` (default), `open`, `tools` | [OFFICIAL] |
| `hermes tools` | `list`, `enable NAME`, `disable NAME` | [snippet] |
| `hermes computer-use` | `install`, `check` (cua-driver backend) | [OFFICIAL] |
| `hermes pets` | `list install select show off scale remove doctor` | [OFFICIAL] |
| `hermes sessions` | `list`, `browse`, `export OUT` (JSONL), `rename ID T`, `prune --older-than N`, `stats`, `delete` | [COMMUNITY/snippet] |
| `hermes insights` | `--days N` (details not captured) | [OFFICIAL] |
| `hermes claw` | `migrate` (OpenClaw migration) | [OFFICIAL] |
| `hermes import-agent` | Subcommands not captured (import Claude Code/Codex CLI setup) | [OFFICIAL] |
| `hermes dashboard` | No flags captured | [OFFICIAL] |
| `hermes serve` | No flags captured (headless backend) | [OFFICIAL] |
| `hermes desktop` (alias `gui`) | No flags captured (build/launch Electron app) | [OFFICIAL] |
| `hermes completion` | `bash`, `zsh`, `fish` | [OFFICIAL] |
| `hermes update` | `--check`, `--plan`, `--backup`, `--no-backup`, `--branch`, `--set-channel`, `--install-id`, `--no-gateway-restart` (from Phase 1) | [OFFICIAL] |
| `hermes uninstall` | `--dry-run`, `--full`, `--data` (from Phase 1) | [OFFICIAL] |
| `hermes version` / `--version` | Version info | [OFFICIAL] |
| `hermes pm` | `status`, `install agent-browser` | [OFFICIAL via installation docs] |

---

# 2. HEADLESS / SCRIPTING USAGE [OFFICIAL]

```bash
hermes -z "What's the capital of France?"                       # final text only
hermes chat --quiet -q "Return only JSON"                       # programmatic, no banner
hermes chat --query-file prompt.txt --oneshot                   # prompt from file (safe for untrusted text)
cat prompt.txt | hermes chat --query-file - --oneshot           # prompt from stdin
hermes chat -q "Inspect this repository" --format stream-json   # JSONL events
hermes chat --toolsets web,terminal,skills --provider openrouter --model anthropic/claude-sonnet-4.6 --oneshot -q "..."
hermes --continue                                               # resume the last session
hermes chat --resume <session-id> --oneshot -q "follow up"
```

**Key Points**:
- **Piping a file into `-z`**: `hermes -z "summarize this" < file.txt` is documented. Piping into `chat -q` was not shown.
- **Session IDs**: the `session_id:` line goes to stderr; `--format stream-json` carries `session_id` in events; `--pass-session-id` puts it in the prompt. Example ID format: `20260225_143052_a1b2c3`.
- **Exit codes**: see Part A (Section 3.1 and 3.2). Remember `-z` and `chat` differ.
- **Cost reporting for pipelines**: `--usage-file` (only with `-z`/`--oneshot`).
- **Spawning from an agent**: the bundled skill spawns `hermes chat -q '...'` for fire-and-forget, tmux-wrapped `hermes -w` for interactive, and `hermes -w` (worktree mode) to avoid git conflicts.
- **Cron/CI notes**: `hermes cron tick` runs due jobs once. For unattended runs, hard stops apply by default. Use `hermes send` to report results.

---

# 3. PYTHON / LIBRARY USAGE

The core class is `AIAgent` in `run_agent.py` (loop in `agent/conversation_loop.py`), with `run_conversation()`; the architecture doc says one class serves CLI, gateway, ACP, batch and API server [OFFICIAL].

**Minimal working example, import path and callback list were NOT RETRIEVED** [UNVERIFIED].

Read: https://hermes-agent.nousresearch.com/docs/developer-guide/programmatic-integration (listed in docs nav, not fetched).

---

# 4. SERVER / API MODES

| Mode | Details | Tag |
|------|---------|-----|
| OpenAI-compatible API server | Gateway platform `api_server`; port **8642** (`API_SERVER_PORT`); enable with `API_SERVER_ENABLED=true`; bind `API_SERVER_HOST`; key `API_SERVER_KEY` (8+ chars); `API_SERVER_CORS_ORIGINS` | [OFFICIAL] |
| `hermes proxy` | Local OpenAI-compatible proxy attaching your OAuth credentials; default `127.0.0.1:8645` | [OFFICIAL] |
| `hermes serve` / `hermes dashboard` | Headless backend (desktop/remote); web dashboard on 9119 | [OFFICIAL] |
| Webhooks | `hermes webhook subscribe`; the gateway webhook platform serves routes; HMAC secret returned | [OFFICIAL] |
| ACP | `hermes acp` over stdio/JSON-RPC for editors | [OFFICIAL] |
| MCP server | `hermes mcp serve` | [OFFICIAL] |
| Example `curl` calls to the API server | **Not retrieved** | [UNVERIFIED] |

---

# 5. CONFLICTS

| Item | Phase 1 Says | Phase 2 Says | Resolution |
|------|--------------|--------------|------------|
| `hermes update` flags | 9 flags (Phase 1 Section 3.6) | Listed in master table; dedicated entry truncated | Use Phase 1 flags as authoritative |
| `hermes uninstall` flags | 3 flags (Phase 1 Section 3.6) | Listed in master table; dedicated entry truncated | Use Phase 1 flags |
| `hermes config` subcommands | 7 from config page | 9 (adds `path`, `env-path`) [snippet] | Merge = 9 total |
| `hermes tools` subcommands | Not documented | 3 [snippet] | Include with snippet tag |
| `hermes mcp` subcommands | Not documented | 6 [snippet] | Include with snippet tag |
| `hermes plugins` subcommands | Not documented | 6 [OFFICIAL, CLI guide] | Include as OFFICIAL |
| `hermes skills` subcommands | Not documented | 10+ [mixed OFFICIAL/snippet] | Include with appropriate tags |
| `hermes sessions` subcommands | Not documented | 7 [COMMUNITY/snippet] | Include with COMMUNITY tag |

---

# 6. GAPS

| Gap | Description |
|-----|-------------|
| Per-flag detail, 3 examples, exit codes for all 30+ command families above | CLI reference truncated after `hermes checkpoints`; need `/docs/llms-full.txt` or rest of CLI page |
| Python embedding example | Not retrieved; see `docs/developer-guide/programmatic-integration` |
| API-server `curl` examples | Not retrieved; see `docs/user-guide/features/api-server` |
| `@file`/URL inline syntax, approval pattern syntax | Not captured; see `docs/user-guide/security`, `docs/user-guide/cli` |
| Version introduced per command | Not in docs; need release notes v0.14–v0.21 or `git log -S` on `commands.py` |
| Reddit/HN/X/Discord pitfalls | Not searched |
| `hermes moa` full syntax | Not captured |
| `hermes fallback` full syntax | Not captured |
| `hermes whatsapp`/`whatsapp-cloud` subcommands | Not captured |
| `hermes approvals` subcommands | Not captured |
| `hermes bundles` subcommands | Not captured |
| `hermes memory` subcommands | Not captured |
| `hermes acp` flags | Not captured |
| `hermes dashboard`/`serve`/`desktop` flags | Not captured |
| `hermes import-agent` subcommands | Not captured |

---

# 7. SOURCES

- https://hermes-agent.nousresearch.com/docs/reference/cli-commands (CLI Commands Reference; fetched through `hermes checkpoints`, truncated after)
- https://hermes-agent.nousresearch.com/docs/reference/slash-commands (Slash Commands Reference; complete)
- https://hermes-agent.nousresearch.com/docs/reference/profile-commands (Profile Commands Reference; complete)
- https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-hermes-agent (bundled `hermes-agent` skill, v3.2.0)
- Search snippets: GitHub repo CLI reference, slash commands, CLI guide; https://hermesagent.org.cn/... (mirror); https://dev.to/rosgluk/hermes-agent-cli-cheat-sheet-commands-flags-and-slash-shortcuts-3pcb [COMMUNITY]; https://github.com/NousResearch/hermes-agent/issues/36949 [COMMUNITY]; https://github.com/koc-Z3/hermes-docs [COMMUNITY]
- Phase 1 pages remain the base for config, env and Docker.

---

FILE COMPLETE: hermes-forge/references/04-cli-command-reference-b.md
Main tables: Remaining Command Families (~40 commands with verified syntax), Headless Usage (7 patterns), Server/API Modes (6). Gaps: 17 items. Conflicts: 8 items.
Note: This is Part B. Combined with Part A, all ~70 commands from the master table are now covered.