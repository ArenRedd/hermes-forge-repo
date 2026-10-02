---
title: Learning Loop and Advanced Features Reference
source_phases: [Phase 4]
hermes_version_documented: v0.21.5 (tag v2026.9.24, Sep 24 2026) — Phase 4 version not pinned; docs don't state version
research_date: Friday, October 2, 2026
last_built_in: Chat 2
confidence_legend: OFFICIAL = official repo/docs/source; COMMUNITY = third-party; INFERRED = deduced; UNVERIFIED = needs checking
used_by_playbooks: [10-skill-authoring-and-memory-curation.md, 01-coding-and-dev.md, 09-personal-productivity.md, 11-maintenance-backup-recovery.md]
---

# Learning Loop and Advanced Features Reference

## WHEN TO READ THIS FILE
Use this file for the automatic vs manual learning mechanisms, goals, checkpoints/rollback, reasoning controls, batch/RL tooling, and the pro-user playbook (30-day path, 30 prompting patterns, anti-patterns).

## TABLE OF CONTENTS
1. Automatic vs Manual Mechanisms
2. Goals (`/goal`)
3. Checkpoints and Rollback
4. Reasoning Controls
5. Batch and RL (Research)
6. 30-Day Pro-User Path
7. 30 Prompting Patterns
8. Anti-Patterns
9. Conflicts
10. Gaps
11. Sources

---

## 1. Automatic vs Manual Mechanisms [OFFICIAL]

| Mechanism | Automatic? | Control |
|-----------|------------|---------|
| Foreground memory and skill saves | Agent's choice (guided by system prompt) | `memory.write_approval`, `skills.write_approval` |
| Background review after turns (~every 10 turns per curator doc) | Yes | `auxiliary.background_review.enabled`, `memory.nudge_interval`, `skills.creation_nudge_interval`, `display.memory_notifications` |
| Curator prune | Yes (when idle, every 7 days default) | `curator.*` |
| Curator consolidation | Off by default | `curator.consolidate`, `hermes curator run --consolidate` |
| `/learn`, `/refine`, `/journey` | Manual | — |
| `/review` | Manual (reviews work product, not memory) | — |
| Session summarization for recall | None. `session_search` returns real messages. Compression summaries separate. | — |

---

## 2. Goals (`/goal`) [OFFICIAL]

```bash
/goal <text>                    # Set standing goal
/goal status                    # Check progress
/goal pause                     # Pause goal
/goal resume                    # Resume goal
/goal clear                     # Clear goal
```

**Behavior**:
- Auxiliary judge decides after each turn whether goal is done
- Budget: `goals.max_turns` (default 20)
- A real user message preempts the loop
- State survives `/resume`
- **Setting a new goal on gateway requires `/stop` first**

---

## 3. Checkpoints and Rollback [OFFICIAL]

**Storage**: Shadow git store under `~/.hermes/checkpoints/` (store path `.../store/` per newest guide). Your real `.git` is untouched.

**Opt-in**:
```bash
hermes chat --checkpoints
# or config:
checkpoints:
  enabled: true
  max_snapshots: 10
```

**Commands**:
```bash
/rollback              # List checkpoints
/rollback diff <N>     # Preview restore
/rollback <N>          # Restore checkpoint N (also undoes last chat turn)
/rollback <N> <file>   # Restore one file
/diff [staged|all|session] [--stat]
```

**Restoring snapshots first** — so you can undo the undo.

**Also available**: `/undo`, `/retry`, `/branch`, `/fork`, `/steer`, `/queue`, `/background`.

**Delegation worktree isolation**: `delegation.worktree_isolation: true` for isolated parallel edits.

**Config keys** (older PR #824): `checkpoints.enabled`, `checkpoints.max_snapshots` — verify against current source.

---

## 4. Reasoning Controls [OFFICIAL]

### 4.1 Reasoning Effort Levels

`none`, `minimal`, `low`, `medium`, `high`, `xhigh`, `max`, `ultra`

### 4.2 Configuration

```yaml
agent:
  reasoning_effort: medium           # global default
  reasoning_overrides:               # per-model override
    "anthropic/claude-*": high
    "openai/o1-*": max
```

### 4.3 Per-Job Override

```bash
hermes cron create "every 1h" "Heavy analysis" --reasoning-effort high
```

### 4.4 Batch Override

```bash
python batch_runner.py --reasoning_effort high ...
python batch_runner.py --reasoning_disabled ...
```

### 4.5 `/fast` Command

Exists as a command; behavior not captured in research.

### 4.6 Mixture of Agents (MoA)

Named MoA presets selectable as models under the "Mixture of Agents" provider. Page not read. [UNVERIFIED]

---

## 5. Batch and RL (For Researchers) [OFFICIAL]

### 5.1 Batch Runner

```bash
# Run batch
python batch_runner.py --dataset_file=data/prompts.jsonl --batch_size=10 --run_name=my_first_run --model=anthropic/claude-sonnet-4.6 --num_workers=4

# Resume
python batch_runner.py --dataset_file=data/prompts.jsonl --batch_size=10 --run_name=my_first_run --resume

# List distributions
python batch_runner.py --list_distributions

# Compress trajectories
python trajectory_compressor.py --input=data/my_run --target_max_tokens=16000
```

### 5.2 Dataset Format

JSONL with `prompt` field. Optional: `image`, `docker_image`, `cwd`.

### 5.3 Defaults

| Parameter | Default |
|-----------|---------|
| `--max_turns` | 10 |
| `--num_workers` | 4 |
| `--distribution` | `default` |

### 5.4 Output

`data/<run_name>/` with:
- `trajectories.jsonl`
- `batch_N.jsonl`
- `checkpoint.json`
- `statistics.json`

Format: ShareGPT-style `from`/`value`.

### 5.5 Filters

- Samples with no reasoning → dropped
- Entries with hallucinated tool names → dropped at merge

### 5.6 Resume

Content-based resume.

### 5.7 RL (Atropos and Tinker)

- Integration via `tinker-atropos` git submodule and `environments/` directory
- Community docs mirror says: "model-training frameworks live in optional skills rather than a bundled Atropos runtime"
- README and mirror disagree — **check your checkout**
- Format reference: `developer-guide/trajectory-format`

---

## 6. 30-Day Pro-User Path [INFERRED, built from verified commands]

### Week 1: Foundations
1. Run `hermes doctor`, `hermes model`, `hermes tools`
2. Install gateway as service: `sudo hermes gateway install --system`
3. Edit `~/.hermes/SOUL.md`
4. Add one project `AGENTS.md`
5. Use `/new` at task boundaries
6. Turn on `memory.write_approval: true` and `skills.write_approval: true` while learning
7. Run `hermes chat --checkpoints`

### Week 2: Memory and Skills
1. Check `cat ~/.hermes/memories/MEMORY.md` after agent says it saved something
2. Try `/learn` on a doc URL
3. Review staged writes with `/skills pending`
4. Create a `hermes bundles create` bundle
5. Run `hermes curator status` and `hermes curator run --dry-run`

### Week 3: Automation
1. Create one natural-language cron job
2. Move one watchdog to `--no-agent`
3. Add a `wakeAgent` gate
4. Use `[SILENT]` on a monitor
5. Run `hermes cron status` and `hermes cron doctor`
6. Add a signed webhook route with a narrow toolset

### Week 4: Scale
1. Set `delegation.model` to a cheaper model
2. Try `/goal` on a bounded task
3. Create a second profile
4. Evaluate one external memory provider
5. Tune `compression.model_thresholds`

---

## 7. 30 Prompting Patterns (Each Tied to Verified Feature) [INFERRED from OFFICIAL]

1. `"Use the \`memory\` tool to save X"` — verifies a real write
2. `"Make this a skill: [workflow]"` or `/learn how I just deployed the staging server`
3. `"Load \`/<skill>\` and then do Y."`
4. Stack skills: `/skill-a /skill-b task`
5. `"Delegate A, B and C in parallel; pass each the full file paths and error text."`
6. `"Give each subagent this output schema."`
7. `"Use \`execute_code\` for the mechanical loop."`
8. `"Every weekday at 8, ... send to Telegram."`
9. `"Only message me if X; otherwise reply \`[SILENT]\`."`
10. `"Ping me if RAM > 85% every 5 minutes"` — lets agent pick `no_agent`
11. Give every cron prompt full context (hosts, commands)
12. `"Update the existing cron job, don't create a new one."`
13. `"Chain this job after job \`<name>\` with \`context_from\`."`
14. `"Report only items not in your previous run"` (`continuity`)
15. Pin a heavy job to `--reasoning-effort high`
16. `"Search past sessions for what we decided about X."`
17. `/goal <outcome>` with a clear done-criterion
18. `/review focus on security` after the PR is open
19. `"Plan first with \`/plan\`; don't execute."`
20. `"Checkpoint, then refactor,"` followed by `/rollback diff`
21. `/personality teacher` for explanations
22. Put stable rules in `AGENTS.md`, not in chat
23. `"Never modify migration files"` in the context file
24. For webhooks: `"template only \`{pull_request.title}\`, not the raw payload."`
25. `"Run the audit in a worktree."`
26. `"Compact now"` (`/compress`) before a long task
27. `"Archive unused skills"` via `/curator`
28. `"Show what you'd change in \`SKILL.md\`"` and then use `/skills diff`
29. `"Summarize cost"` (`/usage`)
30. `"Restate the plan in one paragraph before starting"` before long autonomous runs

---

## 8. Anti-Patterns [OFFICIAL where cited]

### Memory
- Trusting "I'll remember that" without checking the file
- Letting two agents share one Hermes home
- Storing procedures in the 2,200-character memory
- Never running `/new`
- Small models claiming saves they didn't make

### Skills
- Incident-log skills
- Bodies over ~24k characters
- Installing with `--force` without reading findings
- Expecting the curator to manage hand-written skills
- Skills duplicating `AGENTS.md`

### Cron
- Vague prompts
- Giving cron jobs `browser` or `delegation` toolsets
- Polling an LLM every minute without a `wakeAgent` gate
- Editing `jobs.json` by hand
- Forgetting `loginctl enable-linger` on a VPS

### Webhooks and Delegation
- Giving webhook routes the `terminal` toolset
- Setting `max_spawn_depth: 3` casually
- Delegating "fix the error" with no context

---

## 9. Conflicts

| # | Conflict | Resolution |
|---|----------|------------|
| 1 | Version pinning: Phase 3/4 couldn't verify | Use Chat 1's v0.21.5 as baseline; flag uncertainty |
| 2 | Curator stale/archive: config (14/30) vs prose (30/90) | Trust config keys |
| 3 | Background review nudge interval defaults | UNVERIFIED |
| 4 | `/fast` command behavior | UNVERIFIED |
| 5 | MoA details | UNVERIFIED |
| 6 | Atropos bundled vs optional skill | Check checkout |

---

## 10. Gaps

1. `/fast` exact behavior
2. MoA presets and configuration
3. `goals.max_turns` default (20 per doc, verify)
4. `checkpoints.*` keys since PR #824
5. Batch runner full parameter list
6. Trajectory format spec
7. Atropos integration details (bundled vs optional)
8. Kanban tutorial details
9. Bot Mode `message_agent` tool schema
10. A2A protocol

---

## 11. Sources

- https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation
- https://hermes-agent.nousresearch.com/docs/user-guide/features/curator
- https://hermes-agent.nousresearch.com/docs/guides/automation-blueprints
- https://hermes-agent.nousresearch.com/docs/guides/daily-briefing-bot
- https://hermes-agent.nousresearch.com/docs/developer-guide/trajectory-format
- https://hermes-agent.nousresearch.com/docs/developer-guide/batch-processing
- https://hermes-agent.nousresearch.com/docs/llms.txt
- Phase 4 Sections 6, 7
- GitHub PR #824 (checkpoints), #18262 (`/goal`), #41309 (blueprints)

---

**FILE COMPLETE: references/15-learning-loop-and-advanced.md** — Auto/manual mechanisms, goals, checkpoints/rollback, reasoning controls, batch/RL, 30-day path, 30 patterns, anti-patterns.