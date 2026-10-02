---
title: Slash Commands, Sessions & Interactive Usage
source_phases: [Phase 2]
hermes_version_documented: v0.21.x (docs track main; newest verified v0.21.5, v2026.9.24)
research_date: Friday, October 2, 2026
last_built_in: Chat 1
confidence_legend: OFFICIAL = official repo/docs/source; COMMUNITY = third-party; INFERRED = deduced; UNVERIFIED = needs checking
used_by_playbooks: [01-coding-and-dev.md, 03-research-and-analysis.md, 04-content-and-social.md, 05-automation-and-scheduling.md, 06-messaging-gateway-setups.md, 08-multi-agent-and-parallel.md, 09-personal-productivity.md, 10-skill-authoring-and-memory-curation.md]
---

# WHEN TO READ THIS FILE
Read this file when you need the complete slash command reference, keyboard shortcuts, inline reference syntax, approval/permission behavior, CLI vs messaging command differences, session management commands, and interrupt/resume behavior. This is the interactive session reference.

---

# TABLE OF CONTENTS
1. [Slash Command Registry & Mechanics](#1-slash-command-registry--mechanics)
2. [Slash Commands — Complete Tables](#2-slash-commands--complete-tables)
   - 2.1 Session Commands
   - 2.2 Configuration Commands
   - 2.3 Tools & Skills Commands
   - 2.4 Info & Exit Commands
   - 2.5 Messaging-Only Commands
3. [Keyboard, Input & Attachments](#3-keyboard-input--attachments)
4. [Approvals & Unattended Runs](#4-approvals--unattended-runs)
5. [CLI vs Messaging Command Comparison](#5-cli-vs-messaging-command-comparison)
6. [Access Control & Custom Commands](#6-access-control--custom-commands)
7. [Session Management](#7-session-management)
8. [Interrupt / Resume Behavior](#8-interrupt--resume-behavior)
9. [Conflicts](#9-conflicts)
10. [Gaps](#10-gaps)
11. [Sources](#11-sources)

---

# 1. SLASH COMMAND REGISTRY & MECHANICS

- All slash commands come from one `COMMAND_REGISTRY` in `hermes_cli/commands.py`, shared by CLI and messaging gateway [OFFICIAL].
- Prefix matching works: `/h` → `/help` [OFFICIAL].
- Skills become `/<skill-name>`; a skill whose name collides with a built-in is reachable via `/skill <name>` [OFFICIAL].
- User-defined `quick_commands` and `model_aliases` are supported [OFFICIAL].
- Roughly 20 slash commands are CLI-only and about 8 are messaging-only [OFFICIAL].

---

# 2. SLASH COMMANDS — COMPLETE TABLES

## 2.1 Session Commands

| Command | Purpose | Tag |
|---------|---------|-----|
| `/new [name]` (alias `/reset`) | New session; `now`, `--yes`, `-y` skip confirmation | [OFFICIAL] |
| `/clear` | Clear screen and start a new session (CLI only) | [OFFICIAL] |
| `/history`, `/save`, `/copy [N]` | Show history; save; copy last reply (CLI only) | [OFFICIAL] |
| `/prompt` (alias `/compose`) | Write the next prompt in `$EDITOR` (CLI only) | [OFFICIAL] |
| `/retry`, `/undo` | Resend last message; remove last exchange | [OFFICIAL] |
| `/title [name]` | Set or show the title | [OFFICIAL] |
| `/compress [here [N] \| focus topic]` | Manual compression; `here N` keeps last N exchanges (default 2) | [OFFICIAL] |
| `/rollback [N]`, `/diff [staged\|all\|session] [--stat] [path...]` | Restore checkpoints; show git changes | [OFFICIAL] |
| `/snapshot [create\|restore <id>\|prune]` (alias `/snap`) | State snapshots (CLI only) | [OFFICIAL] |
| `/stop` | Kill background processes (gateway also interrupts the agent) | [OFFICIAL] |
| `/queue <prompt>` (alias `/q`) | Queue for next turn; CLI adds `list`, `edit N`, `rm N`, `move A B`, `clear`, `add` | [OFFICIAL] |
| `/steer <prompt>` | Inject a note after the next tool call, with no interrupt | [OFFICIAL] |
| `/goal <text>`, `/subgoal <text>` | Standing goal; subcommands `status pause resume clear`; budget `goals.max_turns` (20) | [OFFICIAL] |
| `/heartbeat every <interval> <prompt>` (alias `/hb`) | Recurring in-session prompt (min 60s) | [OFFICIAL] |
| `/loop [interval] <prompt> [--times N] [--until <cond>]` (alias `/proactive`) | Recurring re-run; `status pause resume stop` | [OFFICIAL] |
| `/refine [focus]`, `/review [instructions]`, `/moa <prompt>` | Run self-improvement review now; reviewer subagent; one prompt through default MoA preset | [OFFICIAL] |
| `/resume [name]`, `/sessions` (TUI alias `/switch`) | Resume; session picker | [OFFICIAL] |
| `/branch [--here] [name]` (alias `/fork`) | Branch the session | [OFFICIAL] |
| `/worktree [new [name]\|list]` | Create or inspect git worktrees (CLI only) | [OFFICIAL] |
| `/handoff <platform>` | Hand the session to a messaging platform (CLI only) | [OFFICIAL] |
| `/status`, `/context [all]` (alias `/ctx`), `/agents` (alias `/tasks`) | Session info with recap; context-window breakdown; running agents | [OFFICIAL] |
| `/bg <prompt>`, `/btw <question>` | Separate background session; side question without interrupting | [OFFICIAL] |
| `/egress [status]`, `/redraw`, `/journey [list\|delete <id>\|edit <id>]` | Egress status; repaint; learning timeline (CLI/TUI/desktop) | [OFFICIAL] |

---

## 2.2 Configuration Commands

| Command | Purpose | Tag |
|---------|---------|-----|
| `/config` | Show config (CLI only) | [OFFICIAL] |
| `/model [model-name]` | Switch model/provider (see 04-cli-command-reference-a.md Section 3.3) | [OFFICIAL] |
| `/codex-runtime [auto\|codex_app_server\|on\|off]` | Toggle the Codex app-server runtime | [OFFICIAL] |
| `/personality [name]` | Set a personality; `none`/`default`/`neutral` clears | [OFFICIAL] |
| `/verbose`, `/focus [on\|off\|status]` | Cycle tool-progress display; reduced-output focus view | [OFFICIAL] |
| `/fast [normal\|fast\|auto\|cold\|status]` | Provider fast/priority modes | [OFFICIAL] |
| `/reasoning [level\|show\|hide\|full\|clamp] [--global]` | Effort levels: `none minimal low medium high xhigh max ultra` | [OFFICIAL] |
| `/skin`, `/statusbar` (alias `/sb`), `/battery`, `/indicator`, `/timestamps`, `/wake` | UI toggles (CLI only) | [OFFICIAL] |
| `/export [profile] [-o out.tar.gz]`, `/import <archive> [--name]` | Profile archive (CLI only) | [OFFICIAL] |
| `/voice [on\|off\|tts\|status]` | CLI voice mode; record key `voice.record_key` (default `Ctrl+B`); gateway adds `join channel leave` | [OFFICIAL] |
| `/yolo`, `/approvals [manual\|smart\|off]` | Skip approvals; set persistent approval mode | [OFFICIAL] |
| `/footer [on\|off\|status]`, `/busy [queue\|steer\|interrupt\|status]` | Reply footer; busy-input mode | [OFFICIAL] |

---

## 2.3 Tools & Skills Commands

| Command | Purpose | Tag |
|---------|---------|-----|
| `/tools [list\|disable\|enable] [name...]`, `/toolsets` | Manage tools; disabling resets the session (CLI only) | [OFFICIAL] |
| `/browser [connect\|disconnect\|status]` | Local Chromium CDP connection (default `http://127.0.0.1:9222`) | [OFFICIAL] |
| `/skills` | Search/install (CLI only); review subcommands `pending diff approve reject approval` also on messaging | [OFFICIAL] |
| `/memory [pending\|approve\|reject\|approval]` | Memory-write approval (both surfaces) | [OFFICIAL] |
| `/bundles`, `/learn <what>`, `/plan [task]`, `/init [notes]` | Skill bundles; distill a skill; write a plan to `.hermes/plans/`; generate `AGENTS.md` | [OFFICIAL] |
| `/cron`, `/suggestions`, `/blueprint [name] [slot=value ...]` (alias `/bp`), `/curator`, `/kanban <action>` | Scheduling and automation | [OFFICIAL] |
| `/reload-mcp`, `/reload-skills`, `/reload` | Re-read MCP, skills, `.env` | [OFFICIAL] |
| `/plugins`, `/pet`, `/hatch <description>` | Plugin list; pets | [OFFICIAL] |

---

## 2.4 Info & Exit Commands

| Command | Purpose | Tag |
|---------|---------|-----|
| `/help` (`/help skills`, `/help <text>`) | Help system | [OFFICIAL] |
| `/palette` (also `Ctrl+P`) | Command palette; inserts selection, never auto-runs | [OFFICIAL] |
| `/version` | Show version | [OFFICIAL] |
| `/whoami` | Show current user/identity | [OFFICIAL] |
| `/usage` | Token/cost for session | [OFFICIAL] |
| `/topup` | Add credits (replaces `/credits`/`/billing`) | [OFFICIAL] |
| `/subscription` (alias `/upgrade`, CLI only) | Subscription info | [OFFICIAL] |
| `/login` | Legacy; use `/auth` or `hermes auth` | [OFFICIAL] |
| `/insights` | Analytics | [OFFICIAL] |
| `/update` | Trigger update check | [OFFICIAL] |
| `/platforms` (alias `/gateway`, CLI only) | Platform status | [OFFICIAL] |
| `/paste` | Paste from clipboard (CLI only) | [OFFICIAL] |
| `/image <path>` | Attach image (CLI only) | [OFFICIAL] |
| `/debug` | Debug info | [OFFICIAL] |
| `/profile` | Profile info | [OFFICIAL] |
| `/quit` (also `/exit`; `--delete` also deletes the session) | Exit session | [OFFICIAL] |

**Confirmation prompts** (CLI asks for confirmation on `/clear`, `/new`, `/undo` and `/exit --delete`; set `approvals.destructive_slash_confirm: false` to disable) [OFFICIAL].

---

## 2.5 Messaging-Only Commands

| Command | Purpose | Tag |
|---------|---------|-----|
| `/start` | Start conversation on messaging platform | [OFFICIAL] |
| `/sethome` (alias `/set-home`) | Set home channel | [OFFICIAL] |
| `/restart` | Restart the gateway session | [OFFICIAL] |
| `/approve [session\|always]` | Approve action; `always` adds to permanent allowlist | [OFFICIAL] |
| `/deny` | Deny action (v0.19.0 notes mention optional reason) | [OFFICIAL] |
| `/topic` | Telegram DM only | [OFFICIAL] |
| `/platform <list\|pause\|resume> [name]` | Platform management | [OFFICIAL] |
| `/commands [page]` | List available commands | [OFFICIAL] |

**On Slack**: use `!stop`, `!new`, `!status` inside threads, or `/hermes <cmd>` for some commands [OFFICIAL].

---

# 3. KEYBOARD, INPUT & ATTACHMENTS

| Item | Detail | Tag |
|------|--------|-----|
| Multi-line | `Alt+Enter`, `Ctrl+J`, `Shift+Enter` (last needs terminal that sends it distinctly) | [OFFICIAL] |
| Interrupt | Type a new message and Enter, or `Ctrl+C` | [OFFICIAL] |
| Command palette | `Ctrl+P` or `/palette`; inserts selection, never auto-runs | [OFFICIAL] |
| Voice | `/voice on`, then `Ctrl+B` to record (`voice.record_key`) | [OFFICIAL] |
| Image/file | `/image <path>`, `/paste` (clipboard), `--image <path>` on `chat`; a `!` shell escape exists (named in the `-q` docs) | [OFFICIAL] |
| Mouse/modal UI | `hermes --tui` supports modal overlays, mouse selection, non-blocking input | [OFFICIAL] |
| Inline `@file` / URL syntax | **NOT FOUND** in what was read | [UNVERIFIED] |

---

# 4. APPROVALS & UNATTENDED RUNS

## 4.1 Approval Modes [OFFICIAL]
- `/approvals [manual|smart|off]` — set persistent mode
- `/yolo` and the `--yolo` flag skip all prompts
- `HERMES_YOLO_MODE` cannot be written via `hermes config set` (it is on the env writer's denylist)

## 4.2 Gateway Approvals [OFFICIAL]
- `/approve [session|always]` — `always` adds to permanent allowlist
- `/deny` — optional reason (v0.19.0)
- `hermes approvals` mines approval history into allowlist proposals

## 4.3 Config Keys [OFFICIAL]
- `approvals.single_query_mode`
- `approvals.destructive_slash_confirm`

## 4.4 Unattended Sessions [OFFICIAL]
- Unattended gateway and cron sessions enable tool-loop hard stops by default (`tool_loop_guardrails.non_interactive_hard_stop_enabled`)
- **Exact pattern allow/deny syntax was NOT CAPTURED**; see Security page [UNVERIFIED]

---

# 5. CLI vs MESSAGING COMMAND COMPARISON

| Group | Commands |
|-------|----------|
| **CLI-only** | `/skin /snapshot /export /import /reload /tools /toolsets /browser /config /cron /platforms /paste /image /statusbar /battery /focus /plugins /indicator /wake /journey /redraw /clear /history /save /copy /handoff /prompt /pet /hatch /timestamps /subscription /quit` |
| **Messaging-only** | `/sethome /restart /approve /deny /topic /platform /commands /start` |
| **Both** | `/status /egress /version /whoami /bg /btw /queue /steer /voice /reload-mcp /reload-skills /rollback /diff /debug /fast /approvals /busy /footer /curator /kanban /topup /login /suggestions /blueprint /learn /init /sessions /loop /yolo /new /model /retry /undo /compress /usage /insights /reasoning /goal /memory` and others |
| **Conditional** | `/verbose` (messaging needs `display.tool_progress_command: true`); `/skills` search/install is CLI-only |

---

# 6. ACCESS CONTROL & CUSTOM COMMANDS

## 6.1 Access Control [OFFICIAL]
```yaml
platforms.<name>.extra:
  allow_from: <user_id>           # who can message the bot
  allow_admin_from: <user_id>     # who gets admin commands
  user_allowed_commands: ["/cmd1", "/cmd2"]  # commands for regular users
  group_allowed_commands: [...]   # group variant
  group_admin_from: <group_id>    # group admin
```
- Regular users get only the listed commands plus `/help` and `/whoami`.
- If `allow_admin_from` is unset, every allowed user can run everything.

## 6.2 Custom Commands (quick_commands) [OFFICIAL]

```yaml
quick_commands:
  status:
    type: exec
    command: systemctl status hermes-agent
  inbox:
    type: alias
    target: /gmail unread
```

```bash
hermes config set model.aliases.fav anthropic/claude-opus-4.6
```

- `type: exec` runs a shell command
- `type: alias` maps to another slash command

---

# 7. SESSION MANAGEMENT

## 7.1 Session Lifecycle
- Sessions are created via `/new`, `--continue`, `--resume`, or automatically on first message.
- Each session has a unique ID (format: `20260225_143052_a1b2c3`).
- Sessions persist in SQLite (`state.db`) with FTS5 search.
- Gateway sessions are routed per-chat; CLI sessions are workspace-scoped.

## 7.2 Session Commands Summary
| Action | CLI Command | Slash Command |
|--------|-------------|---------------|
| New session | `hermes chat` | `/new [name]` |
| Resume last | `hermes --continue` | `/resume` |
| Resume by ID | `hermes --resume <id>` | `/resume <name>` |
| List sessions | `hermes sessions list` | `/sessions` (TUI: `/switch`) |
| Branch session | N/A | `/branch [--here] [name]` |
| Fork (worktree) | `hermes -w` | `/worktree new [name]` |
| Handoff to platform | N/A | `/handoff <platform>` |
| View context usage | N/A | `/context [all]` |
| View agents/tasks | N/A | `/agents` |
| Kill background | N/A | `/stop` |

## 7.3 Session Storage
- `state.db` — canonical sessions, messages, routing (SQLite + FTS5, WAL by default)
- `sessions/` — gateway routing index, request dumps, `*.jsonl`
- `checkpoints/` — filesystem checkpoints for `/rollback`
- `kanban.db` — kanban board state
- `verification_evidence.db` — verification evidence

---

# 8. INTERRUPT / RESUME BEHAVIOR

## 8.1 Interrupt [OFFICIAL]
- **Type a new message and press Enter** — interrupts current turn, submits new message
- **`Ctrl+C`** — hard interrupt
- In TUI: non-blocking input allows interrupt during streaming

## 8.2 Resume [OFFICIAL]
- `hermes --continue` — resumes most recent session (workspace-scoped)
- `hermes --resume <session-id>` — resumes specific session
- `hermes -c [name]` — resumes most recent, or most recent matching title
- `--in <dir>` scopes `--resume latest`/`-c` to that workspace
- `/resume [name]` — in-session resume
- Session ID lookup is the same for `--resume latest` and `-c`

## 8.3 Gateway Session Resume
- Gateway sessions persist across restarts
- `/model` overrides on gateway survive restarts
- Pairing data survives in `auth.json` and `state.db`

## 8.4 Checkpoints & Rollback [OFFICIAL]
- `/rollback [N]` — restore from checkpoint
- `/diff [staged|all|session] [--stat] [path...]` — show git changes
- `/snapshot [create|restore <id>|prune]` — state snapshots (CLI only)
- `hermes checkpoints` CLI manages the shadow store
- `--checkpoints` flag on `hermes chat` enables filesystem checkpoints before destructive changes

---

# 9. CONFLICTS

| Item | Phase 1 Says | Phase 2 Says | Resolution |
|------|--------------|--------------|------------|
| Personality presets | Not mentioned | Built-in preset list NOT FOUND [UNVERIFIED] | Mark presets UNVERIFIED |
| Inline `@file`/URL syntax | Not mentioned | NOT FOUND [UNVERIFIED] | Mark UNVERIFIED |
| Approval pattern syntax | Not mentioned | NOT CAPTURED [UNVERIFIED] | Mark UNVERIFIED |
| Context file load order | Not mentioned | NOT STATED [UNVERIFIED] | Defer to Chat 2 (file 12) |

---

# 10. GAPS

| Gap | Description |
|-----|-------------|
| Personality preset list | Not found; only "pirate" example in quickstart |
| Inline `@file` / URL reference syntax | Not found in fetched pages |
| Approval pattern allow/deny syntax | Not captured; see Security page |
| Context file load order & precedence | Not stated; need `docs/user-guide/features/context-files` |
| `/moa` full subcommand syntax | Not captured |
| `/refine`/`/review` detailed behavior | Not detailed |
| `/blueprint` slot syntax | Not captured |
| `/curator` subcommand details | Not captured |
| `/kanban` action details | Not captured |
| `/journey` subcommand details | Not captured |
| `/plugins` subcommand details | Not captured |
| `/pet`/`/hatch` details | Not captured |

---

# 11. SOURCES

- https://hermes-agent.nousresearch.com/docs/reference/slash-commands (Slash Commands Reference; complete)
- https://hermes-agent.nousresearch.com/docs/reference/profile-commands (Profile Commands Reference; complete)
- https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-hermes-agent (bundled `hermes-agent` skill, v3.2.0)
- https://hermes-agent.nousresearch.com/docs/reference/cli-commands (CLI Commands Reference; partial)

---

FILE COMPLETE: hermes-forge/references/05-slash-commands-sessions-interactive.md
Main tables: Session Commands (25), Configuration Commands (14), Tools & Skills (8), Info & Exit (19), Messaging-Only (8), Keyboard/Input (7), CLI vs Messaging (4 groups ~60 commands), Access Control (1 YAML + 1 bash), Session Management (10 actions), Interrupt/Resume (4 methods). Gaps: 12 items. Conflicts: 4 items.