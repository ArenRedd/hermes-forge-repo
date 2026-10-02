---
title: Subagents and Delegation Reference
source_phases: [Phase 4]
hermes_version_documented: v0.21.5 (tag v2026.9.24, Sep 24 2026) — Phase 4 version not pinned; docs don't state version
research_date: Friday, October 2, 2026
last_built_in: Chat 2
confidence_legend: OFFICIAL = official repo/docs/source; COMMUNITY = third-party; INFERRED = deduced; UNVERIFIED = needs checking
used_by_playbooks: [08-multi-agent-and-parallel.md, 01-coding-and-dev.md, 02-devops-and-server-admin.md, 03-research-and-analysis.md, 10-skill-authoring-and-memory-curation.md]
---

# Subagents and Delegation Reference

## WHEN TO READ THIS FILE
Use this file when designing multi-agent workflows, configuring delegation parameters, spawning subagents via `delegate_task`, debugging subagent failures, or setting up orchestrator patterns.

## TABLE OF CONTENTS
1. Delegation Tool (`delegate_task`)
2. Per-Task Fields
3. Control Actions
4. Context Inheritance
5. Toolset Restrictions
6. Configuration Keys
7. Cost and Concurrency
8. Timeouts and Monitoring
9. Restart Behavior
10. `/review` Command
11. Delegation vs `execute_code`
12. Multi-Agent Patterns
13. Failure Modes
14. Conflicts
15. Gaps
16. Sources

---

## 1. Delegation Tool (`delegate_task`) [OFFICIAL]

**Tool**: `delegate_task` — top-level model calls run in background, return a handle. Result posted back as a new message later.

```python
# Single task
delegate_task(goal="Debug why tests fail", context="Error: assertion in test_foo.py line 42")

# Multiple tasks (parallel fan-out)
delegate_task(tasks=[
    {"goal": "Task A", "context": "..."},
    {"goal": "Task B", "context": "..."},
    {"goal": "Task C", "context": "..."}
])
```

---

## 2. Per-Task Fields [OFFICIAL]

| Field | Required | Notes |
|-------|----------|-------|
| `goal` | Yes | The task description |
| `context` | Yes | Everything the child needs (file paths, error text, full context) |
| `output_schema` | No | JSON Schema. One bounded correction retry. Adds `schema_valid` to result. |
| `images` | No | Up to 8 entries (local paths or URLs) |
| `group` | No | Only advertised when `delegation.independent_completions: true` |
| `role` | No | `leaf` (default) or `orchestrator` |

---

## 3. Control Actions [OFFICIAL]

```python
# List running delegations
delegate_task(action="list")

# Steer a running child (queue course-correction)
delegate_task(action="steer", subagent_id="...", message="Focus on security issues only")

# Stop a child early
delegate_task(action="stop", subagent_id="...")
```

---

## 4. Context Inheritance [OFFICIAL]

**Children start with a COMPLETELY FRESH CONVERSATION.** The only exception:

**Project context files** (in order):
1. `.hermes.md` (or `HERMES.md`) — walks up to git root
2. `AGENTS.override.md` — newer builds
3. `AGENTS.md` — chain
4. `CLAUDE.md` — walks up
5. `.cursorrules` — walks up

**EXCLUDED**: `SOUL.md` — never passed to subagents.

---

## 5. Toolset Restrictions [OFFICIAL]

- Children **inherit parent's enabled toolsets** — no `toolsets` parameter exists.
- **Blocked for leaf children**:
  - `delegate_task` (no recursive delegation)
  - `clarify` (cannot ask user)
  - `memory` (cannot write memory)
  - `send_message` (cannot send messages)
  - `cronjob` (cannot manage cron)
- **Both roles keep**: `execute_code`

- **API key and credential pool**: Inherited from parent.

---

## 6. Configuration Keys [OFFICIAL]

```yaml
delegation:
  max_iterations: 250
  max_concurrent_children: 10      # env DELEGATION_MAX_CONCURRENT_CHILDREN
  max_spawn_depth: 1               # 1 = flat; no ceiling
  orchestrator_enabled: true
  independent_completions: false
  worktree_isolation: false
  child_timeout_seconds: 0         # inactivity cap; 0 = none
  oneshot_max_children: 2
  surface_child_process_notifications: false
  compression_threshold_tokens: 0
  model: "google/gemini-3-flash-preview"
  provider: "openrouter"
  base_url: null
  api_key: null
  api_mode: null
  request_overrides: {}

auxiliary:
  review: {provider: openrouter, model: anthropic/claude-opus-4.6}
```

### Key Details

| Key | Default | Description |
|-----|---------|-------------|
| `max_iterations` | 250 | Max tool calls per child before forced exit |
| `max_concurrent_children` | 10 | Parallel children limit (env override) |
| `max_spawn_depth` | 1 | 1 = flat (no grandchildren). Orchestrator needs >1. |
| `orchestrator_enabled` | true | Allow `role: orchestrator` |
| `independent_completions` | false | If true, enables `group` field for coordinated completions |
| `worktree_isolation` | false | Git worktrees for parallel edits (set true for isolation) |
| `child_timeout_seconds` | 0 | Inactivity timeout (0 = none) |
| `oneshot_max_children` | 2 | Max children for one-shot delegations |
| `model` | `google/gemini-3-flash-preview` | Delegation model (cheap, fast) |
| `provider` | `openrouter` | Provider for delegation model |

---

## 7. Cost and Concurrency [OFFICIAL]

- **Children use most of a run's tokens**. Docs recommend: **frontier parent model + inexpensive `delegation.model`**.
- **Depth 3 with 3 children each = up to 27 concurrent leaf agents**.
- **Cost formula**: Roughly `parent_tokens + sum(child_tokens)`.
- **Savings**: Use `delegation.model` = cheap model (Gemini Flash, Haiku, etc.) via OpenRouter.

---

## 8. Timeouts and Monitoring [OFFICIAL]

| Timeout | Value | Behavior |
|---------|-------|----------|
| Idle timeout | 450 s | Stuck child interrupted |
| Tool timeout | 1200 s | Inside a tool call |
| Result status | `timeout` or `stalled` | For background runs |

### Monitoring Commands

```bash
# In-session
/agents          # or /tasks — shows running children
Ctrl+T or F6     # Live roster

# Logs
tail -f ~/.hermes/cache/delegation/live/<delegation_id>/task-<n>.log
# Kept for 7 days
```

---

## 9. Restart Behavior [OFFICIAL]

- A restart **does not resume** a running child.
- Its attempt becomes `unknown`.
- For durable work, use:
  - `cronjob` (scheduled, survives restart)
  - `terminal(background=True, notify_on_complete=True)` (background process)

---

## 10. `/review` Command [OFFICIAL]

```bash
/review                    # Reviews last 10 messages
/review focus on security  # Custom focus
```

- Spawns a **reviewer subagent** over recent messages.
- `/refine` is different: reviews for memory and skill updates (background review).

---

## 11. Delegation vs `execute_code` [OFFICIAL]

| Use Case | Tool |
|----------|------|
| Judgment, analysis, decision-making | `delegate_task` |
| Mechanical pipelines, data processing, loops | `execute_code` |

- `execute_code` reaches 7 tools via RPC, returns only stdout.
- `delegate_task` returns structured result with `status`, `exit_reason`, `schema_valid`.

---

## 12. Multi-Agent Patterns [OFFICIAL + INFERRED]

### 12.1 Orchestrator with Leaf Workers

```yaml
delegation:
  max_spawn_depth: 2
  orchestrator_enabled: true
```

```python
# Orchestrator delegates to leaves
delegate_task(
    role="orchestrator",
    goal="Build feature X",
    context="...",
    tasks=[
        {"goal": "Write tests", "context": "..."},
        {"goal": "Implement", "context": "..."},
        {"goal": "Document", "context": "..."}
    ]
)
```

### 12.2 Kanban (Durable Coordination) [OFFICIAL]

- "Durable SQLite-backed task board for coordinating multiple Hermes profiles"
- Per-task model override
- Docs: `kanban`, `kanban-tutorial`, `kanban-worker-lanes`, `kanban-multi-gateway`
- Single dispatcher for multi-gateway setups
- Workers under managed gateway require systemd scope

### 12.3 Bot Mode [OFFICIAL]

- Profiles become named **Bots** with own chat, role, model, memory, skills
- "Run routines, share group chats, and message each other"
- `message_agent` tool mentioned in cron doc
- Cron delivery into Bot Chat: `--deliver bot-chat` or `bot-chat:<profile>`

### 12.4 A2A (Agent-to-Agent) [OFFICIAL, UNVERIFIED]

- Messaging page exists at `/docs/messaging/a2a` — not read in detail.

### 12.5 Delegating to Other Agents [OFFICIAL]

- Bundled skills: `claude-code`, `codex`, `opencode`
- Optional skill: `subagent-driven-development` — executes plans via `delegate_task` with 2-stage review

### 12.6 Researcher/Writer/Reviewer Pipelines [INFERRED]

- Not documented as named feature
- Orchestrator pattern: `role="orchestrator"` + `max_spawn_depth: 2`
- `/review` as reviewer stage

---

## 13. Failure Modes (Documented) [OFFICIAL]

| Failure Mode | Symptom | Fix |
|--------------|---------|-----|
| Child given no context | `exit_reason: "empty_context"` | Always pass full `context` with file paths, errors |
| Exhausting `max_iterations` | `exit_reason: "max_iterations"`, `truncated: true` | Increase limit or simplify task |
| Provider errors | `status: "failed"` | Check API keys, quotas, fallback config |
| Parallel edits in same repo | Merge conflicts, corruption | Use `worktree_isolation: true` or separate repos |
| Background processes killed on child finish | Lost work | Use `process_manage handoff` or cron/terminal background |
| Missed steer | `missed_steer` in result | Child already finished; steer earlier |

---

## 14. Conflicts

| # | Conflict | Resolution |
|---|----------|------------|
| 1 | Delegation model default: Phase 3 not documented | Phase 4: `google/gemini-3-flash-preview` via `openrouter` |
| 2 | `max_spawn_depth` default: Phase 3 not documented | Phase 4: 1 (flat) |
| 3 | Blocked tools for leaf children: Phase 3 not documented | Phase 4: `delegate_task`, `clarify`, `memory`, `send_message`, `cronjob` |
| 4 | Kanban/A2A details | UNVERIFIED — docs pages not fully read |

---

## 15. Gaps

1. `delegate_task` exact JSON Schema for `output_schema` parameter
2. `group` field behavior when `independent_completions: true`
3. `worktree_isolation` exact implementation (git worktree commands)
4. Kanban: full CLI commands, schema, multi-gateway dispatcher config
5. Bot Mode: `message_agent` tool schema and parameters
6. A2A protocol details
7. `surface_child_process_notifications` exact behavior
8. `compression_threshold_tokens` for children (0 = use parent?)
9. Per-child reasoning effort override

---

## 16. Sources

- https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation
- https://hermes-agent.nousresearch.com/docs/llms.txt
- Phase 4 Section 5

---

**FILE COMPLETE: references/14-subagents-and-delegation.md** — `delegate_task` schema, per-task fields, control actions, context inheritance, toolset restrictions, config keys, cost/concurrency, timeouts, monitoring, restart behavior, `/review`, patterns, failure modes.