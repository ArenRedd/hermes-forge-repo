---
title: Memory and Context Reference
source_phases: [Phase 4]
hermes_version_documented: v0.21.5 (tag v2026.9.24, Sep 24 2026) — Phase 4 version not pinned; docs don't state version
research_date: Friday, October 2, 2026
last_built_in: Chat 2
confidence_legend: OFFICIAL = official repo/docs/source; COMMUNITY = third-party; INFERRED = deduced; UNVERIFIED = needs checking
used_by_playbooks: [10-skill-authoring-and-memory-curation.md, 09-personal-productivity.md, 08-multi-agent-and-parallel.md, 11-maintenance-backup-recovery.md]
---

# Memory and Context Reference

## WHEN TO READ THIS FILE
Use this file for everything about Hermes Agent's memory system (built-in MEMORY.md, USER.md, session storage, external providers), context files (priority, truncation, security), personalities, compression, and prompt caching.

## TABLE OF CONTENTS
1. Memory Layers
2. The `memory` Tool
3. Configuration and Controls
4. Session Storage and Search
5. Learning Journey
6. External Memory Providers (9 providers)
7. Best Practices
8. Context Files (Priority, Size, Truncation, Security)
9. Personalities (14 built-in + custom)
10. Compression (Full Config)
11. Prompt Caching
12. Usage and Cost
13. Conflicts
14. Gaps
15. Sources

---

## 1. Memory Layers [OFFICIAL]

| Layer | Storage | Limit | Injected How | Cost |
|-------|---------|-------|--------------|------|
| `MEMORY.md` | `~/.hermes/memories/MEMORY.md` | 2,200 chars (~800 tokens) | Frozen snapshot in system prompt at session start | Fixed per session |
| `USER.md` | `~/.hermes/memories/USER.md` | 1,375 chars (~500 tokens) | Same | Fixed |
| Session history | `~/.hermes/state.db` (SQLite + FTS5) | Unbounded | On demand via `session_search` | No LLM calls, ~20ms/query |
| Skills | `~/.hermes/skills/` | See skills ref | Index in prompt; bodies load on demand | Index ~3k tokens |
| Context files | Project dirs | `context_file_max_chars` or scales (20K–500K) | Injected in system prompt (context tier) | Scales with content |
| External providers | Plugin-defined | Plugin-defined | Alongside built-in files, never replacing | Provider-dependent |

**Entry separator**: `§` (section sign). Each store's header shows usage: `MEMORY (your personal notes) [67% — 1,474/2,200 chars]`.

---

## 2. The `memory` Tool [OFFICIAL]

**Actions**: `add`, `replace`, `remove` — **NO `read` action** (memory already in prompt).

**Targets**: `memory` (personal notes) and `user` (user profile).

**Matching**: `replace` and `remove` use unique `old_text` substring. `replace` overwrites the **whole matched entry**.

```python
memory(action="replace", target="memory", old_text="dark mode",
       content="User prefers light mode in VS Code, dark mode in terminal")
```

**Full memory**: No auto-compaction. Over-limit write returns error with `current_entries` — agent must consolidate and retry.

**Safety**: Exact duplicates rejected. Entries scanned for injection, exfiltration, invisible Unicode.

**Freezing**: Writes hit disk immediately but appear in prompt **only in next session**. Run `/new` at natural boundaries. On gateways, one chat can stay a single session for weeks.

**User modeling**: `user` target = profile. Separate "dialectic" user model available through Honcho (not detailed here).

---

## 3. Configuration and Controls [OFFICIAL]

```yaml
memory:
  memory_enabled: true
  user_profile_enabled: true
  memory_char_limit: 2200
  user_char_limit: 1375
  write_approval: false
  provider: <name>        # external provider (honcho, mem0, openviking, etc.)
```

```bash
/memory pending | /memory approve <id|all> | /memory reject <id|all> | /memory approval on|off
```

- Setting both enable flags to `false` drops the `memory` tool. External providers keep working.
- Putting `memory` in `agent.disabled_toolsets` hides external provider tools too.
- Memory is scoped per profile. **Never point two agent processes at one Hermes home.**

---

## 4. Session Storage and Search [OFFICIAL]

- `hermes sessions list` — browses past sessions
- `session_search` — FTS5 full-text search over all past sessions in `~/.hermes/state.db`
- Three calling shapes (discovery, scroll, browse) — documented at `/docs/user-guide/sessions#session-search-tool` (not fully read)
- **Missing**: schema, export and delete commands, old-session summarization
- Related pages: `session-storage`, `state-db-recovery`, `session-storage-recovery`

---

## 5. Learning Journey [OFFICIAL]

```bash
hermes journey [--play --fps N --width N --height N --no-color --json]
hermes journey list | delete <node> [-y] | edit <node>
```

**Aliases**: `hermes learning`, `hermes memory-graph`. In sessions: `/journey`, `/learning`, `/memory-graph`.

- Deleting a skill node archives it
- Deleting a memory node removes it

---

## 6. External Memory Providers [OFFICIAL, partial]

```bash
hermes memory setup      # interactive picker
hermes memory status
hermes memory off        # disable the external provider
hermes config set memory.provider <name>
hermes plugins install hindsight   # Hindsight is plugin-catalog, not bundled
```

```yaml
memory:
  provider: openviking   # or honcho, mem0, holographic, retaindb, byterover, supermemory, hindsight
```

| Provider | Setup Details | Config File |
|----------|---------------|-------------|
| **Honcho** | `hermes memory setup`, select `honcho`. Legacy `hermes honcho setup` redirects. Cloud key from `app.honcho.dev`. [OFFICIAL] | `$HERMES_HOME/honcho.json` or `~/.honcho/config.json` |
| **Mem0** | Modes: Platform, Open Source, Self-hosted server. | `$HERMES_HOME/mem0.json` |
| **Hindsight** | `hermes plugins install hindsight`, `hermes memory setup`, select `hindsight` | `$HERMES_HOME/hindsight/config.json` |
| **Supermemory** | `hermes memory setup`. Self-hosted: `npx supermemory local`, set `base_url` in JSON first. | `$HERMES_HOME/supermemory.json` |
| **OpenViking** | Listed as bundled. Steps not captured. | Not captured |
| **Holographic** | Listed as bundled. Steps not captured. | Not captured |
| **RetainDB** | Listed as bundled. Steps not captured. | Not captured |
| **ByteRover** | Listed as bundled. Steps not captured. | Not captured |

**Mem0 commands** [COMMUNITY]:
```bash
hermes memory setup mem0 --mode oss --oss-llm openai --oss-llm-key sk-...
hermes memory setup mem0 --mode selfhosted --host http://localhost:8888 --api-key your-admin-api-key
```

**Env keys** [COMMUNITY]: `MEM0_API_KEY`, `HONCHO_API_KEY`, `HINDSIGHT_API_KEY` (cloud only).

**Tool names** [COMMUNITY]: Hindsight exposes `hindsight_recall`, `hindsight_retain`, `hindsight_reflect`. GitHub issue gives tool counts: Honcho 5, Holographic 2, Supermemory 4.

**Profiles**: Config-file providers store config in `$HERMES_HOME/`, so each profile has own credentials.

**Disabling**: `memory` in `agent.disabled_toolsets` hides external provider tools as well.

**Cost**: Provider-dependent, not documented in one place. Mem0 and Honcho cloud tiers paid/freemium per community comparison. Hindsight local runs local PostgreSQL daemon [COMMUNITY].

**Backup and migration**: Desktop app lists "backup/import" in Settings. No documented CLI for memory export.

**Unverified**: `memory.provider memori` snippet in one search. GitHub issue says Mnemosyne not bundled but works as plugin.

---

## 7. Best Practices [OFFICIAL, with INFERRED guidance]

- **Save**: Preferences, environment facts, corrections, conventions, completed-work notes.
- **Skip**: Trivia, easily rediscovered facts, raw dumps, session-only paths.
- **Where things go**: Repeating procedures and fixed locations → skill (doesn't use 2,200-char budget). Facts needed every session → memory. Project rules → context files.
- **Keep memory lean**: Consolidate once usage passes 80% [OFFICIAL].
- **Backups**: Copy `~/.hermes/memories/` and `state.db`. Docs say quick backups include cron ledger, but no documented memory backup procedure.
- **Troubleshooting "it forgot"**: Check file contents, staged write, active profile, memory enabled, frozen snapshot.
- **Privacy**: Memory writes scanned, but file contents plaintext on disk. Treat `~/.hermes/` as sensitive [INFERRED].

---

## 8. Context Files [OFFICIAL]

### 8.1 Priority (First Match Wins, One Project Type Per Session)

1. `.hermes.md` (or `HERMES.md`) — walks up to git root
2. `AGENTS.override.md` — **newer builds only** (older docs mirror lacks it)
3. `AGENTS.md` — chain (walks up)
4. `CLAUDE.md` — walks up
5. `.cursorrules` — walks up

**SOUL.md**: Loaded independently as identity (slot #1 in system prompt). Comes **only from `$HERMES_HOME/SOUL.md`** (`~/.hermes/SOUL.md`), **never from working directory**.

### 8.2 Starter File
Starter `SOUL.md` seeded if missing. Existing files never overwritten.

### 8.3 Subdirectories
`AGENTS.md` read at startup working directory. Nested ones discovered as agent reads files there (`agent/subdirectory_hints.py`) and enter through history, not system prompt. [COMMUNITY]

### 8.4 Size Limit
- Cap: `context_file_max_chars` if set
- Otherwise scales with model window: **floor 20,000, ceiling 500,000**
- Older docs: fixed 20,000 with 70% head / 20% tail truncation

### 8.5 Truncation Marker
```
[...truncated AGENTS.md: kept 14000+4000 of 25000 chars]
```

### 8.6 Security Scan
Injection patterns block file with:
```
[BLOCKED: AGENTS.md contained potential prompt injection (prompt_injection)]
```

### 8.7 Edits Mid-Session
Not picked up until new session.

### 8.8 Recommended AGENTS.md
- Keep concise
- State architecture, commands, ports
- Include "what NOT to do" (e.g., never modify migration files directly)

### 8.9 Cron and Subagents
- Cron loads these files **only when job has a `workdir`**
- Subagents get same files, **minus `SOUL.md`**

---

## 9. Personalities [OFFICIAL]

### 9.1 Built-in Presets (14)

| Personality | Description |
|-------------|-------------|
| `helpful` | Default, balanced |
| `concise` | Minimal, direct answers |
| `technical` | Precise, jargon-heavy |
| `creative` | Imaginative, exploratory |
| `teacher` | Explains concepts, pedagogical |
| `kawaii` | Cute, enthusiastic |
| `catgirl` | Playful, cat-themed |
| `pirate` | Arr, nautical |
| `shakespeare` | Elizabethan verse |
| `surfer` | Laid-back, beach vibes |
| `noir` | Gritty, detective style |
| `uwu` | Cutespeak |
| `philosopher` | Deep, contemplative |
| `hype` | Excited, promotional |

### 9.2 Switching

```bash
/personality                # show current
/personality concise        # switch to concise
/personality teacher        # switch to teacher
/personality none           # clear (also "default", "neutral")
```

### 9.3 Custom Personalities

```yaml
agent:
  personalities:
    codereviewer: >
      You are a meticulous code reviewer. Identify bugs, security issues,
      performance concerns, and unclear design choices. Be precise and constructive.
```

### 9.4 Storage and Layering

- Selection stored in `display.personality`
- **SOUL.md** = durable baseline identity
- **`/personality`** = temporary overlay
- `agent.system_prompt` = separate manual field, applies **only when no personality selected**

---

## 10. Compression [OFFICIAL]

**Source**: `/docs/developer-guide/context-compression-and-caching`. Source files: `agent/context_engine.py`, `agent/context_compressor.py`, `agent/prompt_caching.py`, `gateway/run_turn.py`, `agent/compression_facade.py`.

### 10.1 Triggers

| Layer | Trigger |
|-------|---------|
| Agent `ContextCompressor` | Prompt tokens ≥ `threshold × context_length` (default 0.50). Floored at 0.75 for windows < 512K. |
| Gateway session hygiene | Fixed at 85% of context. Only when history ≥ 4 messages. Safety net, set above agent trigger. |

### 10.2 Full Config

```yaml
compression:
  enabled: true
  threshold: 0.50
  threshold_tokens: null
  model_thresholds: {}      # substring match, longest wins; "provider:substr" allowed
  target_ratio: 0.20        # legacy tail mode only
  tail_mode: lean           # lean | legacy
  protect_last_n: 20
  min_tail_user_messages: 1
  idle_compact_after_seconds: 0
  in_place: true
  abort_on_summary_failure: false
  protect_first_n: 3        # HARDCODED
auxiliary:
  compression:
    model: null
    provider: auto
    base_url: null
context:
  engine: "compressor"      # or plugin engine e.g. "lcm"
```

### 10.3 Protected Regions

- **Protected head**: `protect_first_n` = 3 (hardcoded) — system prompt + first exchange
- **Protected tail**: By token budget, capped at 20% of window. In `lean` mode: 2.5% of window, clamped to 10K–25K tokens.

### 10.4 Algorithm

1. Prune old tool results >200 chars to `[Old tool output cleared to save context space]`
2. Set head and tail boundaries
3. Summarize middle with auxiliary model using structured template:
   - Goal
   - Constraints & Preferences
   - Progress
   - Key Decisions
   - Relevant Files
   - Next Steps
   - Critical Context
4. Reassemble messages

### 10.5 Re-compression
Later passes update previous summary rather than starting over.

### 10.6 Summary Model Requirement
Its context window must be **at least as large as main model's**, or middle turns can be dropped without summary.

### 10.7 Failures
Failure cooldown escalates: 60s → 300s → 900s. Manual `/compress` clears it. After repeated failures, deterministic fallback summary committed. `abort_on_summary_failure: true` aborts instead.

### 10.8 Session ID
With `in_place: true`, compaction stays on one session ID; old turns soft-archived, searchable via `session_search`.

### 10.9 Worked Example (200K model)
- Trigger: 100,000 tokens
- Tail budget: 20,000
- Summary at most: 10,000

### 10.10 Plugin Engines
Replace compressor via `context.engine`. Never auto-activated.

### 10.11 Micro-compaction
Separate doc (`/docs/developer-guide/micro-compaction`) — not read.

### 10.12 Long Autonomous Runs
- Use summary model with large window
- Consider `model_thresholds` per model
- `min_tail_user_messages: 3`
- Run `/new` at task boundaries

---

## 11. Prompt Caching [OFFICIAL]

### 11.1 Strategy
`system_and_3` — uses 4 Anthropic `cache_control` breakpoints: system prompt + last 3 non-system messages. Applies to Claude models (native or via OpenRouter).

### 11.2 TTL
`prompt_caching.cache_ttl: "5m"` (also `"1h"` or `"auto"`). `auto` picks 1h for human-paced, 5m for machine-paced (cron, subagent, webhook, batch).

### 11.3 What Breaks Cache
1. Any model change mid-session (`/model`, fallback activation, credential rotation)
2. Mutating the system prompt
3. Compression (invalidates compressed region, not system prompt)
4. Inserting or removing middle messages

### 11.4 What Does NOT Break Cache
- Memory writes (frozen snapshot)
- `/<skill>` or bundle invocations (arrive as user messages)

---

## 12. Usage and Cost [OFFICIAL, partial]

- `/usage` — tokens, estimated cost, context window state, live account limits (when provider reports)
- `/insights [days]` — analytics, default 30 days. CLI: `/insights [--days N]`
- `/topup` exists
- **Missing**: Hard spend-budget command or config key (not found)
- **Cost levers**: Delegation model, `auxiliary.background_review`, cron `enabled_toolsets`, `no_agent` jobs, `wakeAgent` gates, `curator.consolidate: false`

---

## 13. Conflicts

| # | Conflict | Resolution |
|---|----------|------------|
| 1 | Context file priority: Phase 2 had `.hermes.md`, `AGENTS.md`, `CLAUDE.md`, `.cursorrules` | **Phase 4 adds `AGENTS.override.md` between `.hermes.md` and `AGENTS.md`** — use corrected order |
| 2 | `SOUL.md` location: Phase 1 said `$HERMES_HOME/SOUL.md` | Consistent — never from working directory |
| 3 | Personality presets: Phase 2 NOT FOUND [UNVERIFIED] | **Phase 4 found 14 built-in** — resolved |
| 4 | Compression config: Phase 1 partial | **Phase 4 complete** — use full config |
| 5 | Context file size: Phase 1 not documented | Phase 4: scales 20K–500K or `context_file_max_chars` |
| 6 | Curator stale/archive days: config (14/30) vs prose (30/90) | Trust config keys |

---

## 14. Gaps

1. `session_search` exact schema (three shapes)
2. Session export and delete commands
3. `state.db` schema (schema version 14 per Substack [COMMUNITY])
4. Memory backup CLI procedure
5. Per-provider setup steps for OpenViking, Holographic, RetainDB, ByteRover
6. Honcho dialectic user-model details
7. `memory.nudge_interval` and `skills.creation_nudge_interval` defaults
8. `/fast` command behavior
9. MoA (Mixture of Agents) details
10. Kanban details

---

## 15. Sources

- https://hermes-agent.nousresearch.com/docs/user-guide/features/memory
- https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files
- https://hermes-agent.nousresearch.com/docs/user-guide/features/personality
- https://hermes-agent.nousresearch.com/docs/developer-guide/context-compression-and-caching
- https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly
- https://hermes-agent.nousresearch.com/docs/llms.txt
- Phase 4 Sections 2, 3, 6

---

**FILE COMPLETE: references/12-memory-and-context.md** — Memory layers, tool, config, session storage, 9 external providers, best practices, corrected context file priority, 14 personalities, full compression config, prompt caching, usage/cost.