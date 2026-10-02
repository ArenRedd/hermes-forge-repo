---
title: Scheduling and Automation Reference
source_phases: [Phase 4]
hermes_version_documented: v0.21.5 (tag v2026.9.24, Sep 24 2026) — Phase 4 version not pinned; docs don't state version
research_date: Friday, October 2, 2026
last_built_in: Chat 2
confidence_legend: OFFICIAL = official repo/docs/source; COMMUNITY = third-party; INFERRED = deduced; UNVERIFIED = needs checking
used_by_playbooks: [05-automation-and-scheduling.md, 06-messaging-gateway-setups.md, 08-multi-agent-and-parallel.md, 09-personal-productivity.md, 11-maintenance-backup-recovery.md]
---

# Scheduling and Automation Reference

## WHEN TO READ THIS FILE
Use this file for everything about Hermes Agent's cron system, scheduling formats, delivery targets, script-only mode, wakeAgent gates, job chaining, hooks, webhooks, and the 25 official automation recipes.

## TABLE OF CONTENTS
1. Cron Mechanics
2. Cron Commands (Verbatim)
3. Schedule Formats (5 Types)
4. Delivery Targets and Behavior
5. Script-Only Mode and wakeAgent Gates
6. Job Chaining (context_from, continuity)
7. Hooks and Webhooks
8. 25 Official Recipes (Verbatim)
9. Cron Configuration Keys
10. Conflicts
11. Gaps
12. Sources

---

## 1. Cron Mechanics [OFFICIAL]

- **Tool**: Single `cronjob_manage` tool with `action=` create/list/update/pause/resume/run/remove. Examples call it as `cronjob(...)`.
- **Scheduler**: Gateway daemon ticks every 60 seconds, starts a fresh `AIAgent` session per due job.
- **Lock**: `~/.hermes/cron/.tick.lock` prevents double runs.
- **Storage**: 
  - Jobs: `~/.hermes/cron/jobs.json`
  - Output: `~/.hermes/cron/output/{job_id}/{timestamp}.md`
  - Attempt ledger: `~/.hermes/cron/executions.db`
- **Model resolution**: Per-job pin → `cron.model` → main model. Per-job `--reasoning-effort` accepts `none` through `ultra`.
- **Toolsets**: `cron` platform config from `hermes tools`, or per-job `enabled_toolsets`. Cron-run agents **cannot create cron jobs** unless `cron.allow_agent_scheduling: true`.
- **Systemd**: Jobs run as workers in transient scope (`systemd-run --user --scope`). Gateway restart doesn't kill them. **Requires** `sudo loginctl enable-linger <gateway-user>`. Otherwise cron degrades by default, or fails closed with `cron.require_restart_safe_scope: true`.
- **VPS Service Install**:
```bash
hermes gateway install
sudo hermes gateway install --system
hermes cron status
```

---

## 2. Cron Commands (Verbatim) [OFFICIAL]

```bash
# Slash commands (in-session)
/cron add "in 30m" "Remind me to check the build"
/cron add "every 1h" "Summarize new feed items" --skill blogwatcher

# CLI commands
hermes cron create "every 2h" "Check server status"
hermes cron create "every 1h" "Use both skills and combine the result" --skill blogwatcher --skill maps --name "Skill combo"
hermes cron create "every 1d at 09:00" "Audit open PRs..." --workdir /home/me/projects/acme
hermes cron create "every 1h" "Post the digest" --paused --paused-reason "Awaiting review"
hermes cron create "every 5m" --no-agent --script memory-watchdog.sh --deliver telegram --name "memory-watchdog"
hermes cron create "every 6h" "Scan for news" --continuity

# List and status
hermes cron list | status | tick | doctor | runs [job-id] --limit 20 | incidents [--state alerted] | incidents ack <id>

# Control
hermes cron pause|resume|run|remove <job_id_or_name>

# Edit (all options)
hermes cron edit <id> --schedule "every 4h" --prompt "..." --skill X --add-skill Y --remove-skill X --clear-skills --pin --unpin --model M --provider P --reasoning-effort high --continuity

# Global pause/resume
hermes pause [--reason ...]    hermes resume
```

**Job references**: By name (case-insensitive) or ID. Ambiguous names refused.

---

## 3. Schedule Formats (5 Types) [OFFICIAL]

| Type | Examples |
|------|----------|
| **One-shot delays** | `in 30m`, `in 2h`, `in 1d` |
| **Intervals** | `30m`, `every 2h`, `every hour` |
| **Natural language** | `every monday 9am`, `weekdays at 9am`, `daily at 7am`, `monday, wednesday at 9am` |
| **Cron expressions** | `0 9 * * 1-5`, `0 */6 * * *`, `0 9 * * MON-FRI` |
| **ISO timestamp** | `2026-03-15T09:00:00` |

**Repeat count**: `repeat=5` overrides default. One-shots default to 1. Others run forever.

---

## 4. Delivery Targets and Behavior [OFFICIAL]

### 4.1 Targets (`--deliver`)

| Target | Syntax | Description |
|--------|--------|-------------|
| Origin chat | `origin` | Reply to originating chat (CLI or messaging) |
| Local file | `local` | Save to `~/.hermes/cron/output/{job_id}/{timestamp}.md` |
| Telegram | `telegram` or `telegram:<chat_id>[:thread]` | Bot sends to chat |
| Discord | `discord:#channel` | Channel mention or ID |
| Slack | `slack` or `slack:#channel` | Default or specific channel |
| Email | `email` or `email:address@domain.com` | Via SMTP |
| SMS | `sms` or `sms:+15551234567` | Via Twilio |
| All platforms | `all` | Broadcast to all enabled |
| Comma list | `telegram,discord,slack` | Multiple targets |
| Bot chat | `bot-chat` or `bot-chat:<profile>` | Inter-agent (Bot Mode) |

**Defaults**:
- CLI-created jobs: `local`
- Messaging-created jobs: `origin`

### 4.2 Delivery Modifiers

| Modifier | Effect |
|----------|--------|
| `[SILENT]` as first line of response | Suppresses delivery (still saved to output) |
| `[CRON_FAILURE]` as first line | Marks run as failed (always delivers) |
| `cron.wrap_response: true` (default) | Adds `Cronjob Response:` header |
| `cron.wrap_response: false` | Raw output only |
| `deliver_only: true` (webhook) | Renders prompt as literal message, zero LLM cost |

### 4.3 Secret Redaction
All delivered text is automatically secret-redacted (API keys, tokens, passwords).

---

## 5. Script-Only Mode and wakeAgent Gates [OFFICIAL]

### 5.1 Script-Only Mode (`--no-agent`)

```bash
hermes cron create "every 5m" --no-agent --script memory-watchdog.sh --deliver telegram --name "memory-watchdog"
```

- Script stdout delivered verbatim
- Empty stdout = silent tick
- Non-zero exit = error alert
- Scripts must live in `$HERMES_HOME/scripts/`
- Default timeout: 3600 s (`cron.script_timeout_seconds`, env `HERMES_CRON_SCRIPT_TIMEOUT`)

### 5.2 wakeAgent Gate

A script can end with `{"wakeAgent": false}` to skip the LLM entirely.

```bash
#!/bin/bash
# memory-watchdog.sh
MEMORY_PCT=$(free | awk '/Mem:/ {print int($3/$2 * 100)}')
if [ $MEMORY_PCT -gt 85 ]; then
  echo "RAM at ${MEMORY_PCT}% - OVER THRESHOLD"
  exit 0  # wakeAgent defaults to true
else
  echo '{"wakeAgent": false}'  # Skip LLM, silent tick
  exit 0
fi
```

**Default**: `wakeAgent: true` (run LLM). Set `false` to suppress.

---

## 6. Job Chaining [OFFICIAL]

### 6.1 context_from

```bash
hermes cron create "every 1h" "Summarize feed" --skill blogwatcher --name collector
hermes cron create "30m after collector" "Triage and rank" --context_from collector --name triage
hermes cron create "1h after collector" "Write brief" --context_from collector,triage --name brief
```

- Accepts job ID, name, or list
- Feeds previous job's output as context

### 6.2 continuity

```bash
hermes cron create "every 6h" "Scan for news" --continuity
```

- Feeds the job its **own previous output**
- Use with `continuity=true` in tool call
- Enables deduplication (e.g., "report only items not in previous run")

### 6.3 3-Stage Pipeline Example (Recipe 8)

```bash
# Stage 1: Collector at 07:00
hermes cron create "0 7 * * *" "Collect AI news from sources" --name collector --skill arxiv

# Stage 2: Triage at 07:30, context from collector
hermes cron create "30 7 * * *" "Triage and rank collected items" --context_from collector --name triage

# Stage 3: Brief at 08:00, context from both
hermes cron create "0 8 * * *" "Write final brief" --context_from collector,triage --name brief --deliver telegram
```

---

## 7. Hooks and Webhooks [OFFICIAL]

### 7.1 Event Systems

| System | Declared In | Scope |
|--------|-------------|-------|
| Gateway hooks | `~/.hermes/hooks/<name>/HOOK.yaml` + `handler.py` | Gateway only |
| Shell hooks | `hooks:` block in `~/.hermes/config.yaml` (`hooks_auto_accept: true` skips prompts) | CLI and gateway |
| Plugin hooks | `register()` in `plugin.yaml` (e.g., `pre_llm_call`, `subagent_stop`) | Both |
| Outbound webhooks | `hooks.outbound:` list in `config.yaml` | CLI and gateway |

- Gateway events: `gateway:startup`, `agent:*`, `command:*`, `session:*` (full list not captured)
- Outbound: `X-Hermes-Event`, `X-Hermes-Signature-256` (sha256, GitHub-style) when secret set
- All hooks non-blocking — errors caught and logged
- `BOOT.md` hook now a user-built pattern, not built-in

### 7.2 Inbound Webhooks (see 09-messaging-gateway.md Section 8)

```yaml
platforms:
  webhook:
    enabled: true
    extra:
      port: 8644
      secret: "global-fallback-secret"
      routes:
        github-pr:
          events: ["pull_request"]
          secret: "github-webhook-secret"
          prompt: |
            Review this pull request:
            Repository: {repository.full_name}
            PR #{number}: {pull_request.title}
          skills: ["github-code-review"]
          deliver: "github_comment"
          deliver_extra:
            repo: "{repository.full_name}"
            pr_number: "{number}"
```

**Route keys**: `events`, `secret`, `profile`, `prompt`, `filters`, `script`, `skills`, `toolsets`, `deliver`, `deliver_extra`, `deliver_only`, `cron_job`, `coalesce`, `mirror_to_session`.

```bash
hermes webhook subscribe <name> --events "..." --prompt "..." --skills X --deliver telegram --deliver-chat-id ID --deliver-only --cron-job NAME --route-profile NAME --mirror-to-session --description "..."
hermes webhook list | remove <name> | test <name> [--payload '{}']
```

- Dynamic subscriptions in `~/.hermes/webhook_subscriptions.json` (hot-reloaded)
- Webhook runs default to constrained toolset (`web_search`, `web_extract`, `vision_analyze`, `clarify`)
- Per-route `toolsets` = manual edit only
- Rate limit: 30 req/min per route
- Idempotency TTL: 1 hour
- Body limit: 1 MB
- `INSECURE_NO_AUTH` only on loopback

### 7.3 Event-Triggered Cron

`cron_job: "pr-review-sweeper"` on a route fires existing cron job. Webhook prompt becomes transient run context. Returns HTTP 202.

### 7.4 Direct Delivery

`deliver_only: true` makes rendered prompt the literal message, zero LLM cost.

---

## 8. 25 Official Recipes (Verbatim) [OFFICIAL]

**Sources**: `/docs/guides/automation-blueprints`, `/docs/user-guide/features/cron`, `/docs/guides/daily-briefing-bot`, `/docs/user-guide/messaging/webhooks`.

| # | Recipe | Setup |
|---|--------|-------|
| 1 | Daily briefing | `/cron add "0 8 * * *" "Search the web for the latest news about AI agents and open source LLMs. Summarize the top 3 most important stories in a concise daily briefing format."` |
| 2 | Weekday-only briefing | Use schedule `0 8 * * 1-5` |
| 3 | Morning market and news | `hermes cron create "0 8 * * *" "Generate a morning business metrics summary..." --name "Morning briefing" --deliver telegram` |
| 4 | Weekly AI digest | `hermes cron create "0 9 * * 1" "Generate a weekly AI news digest..." --name "Weekly AI digest" --deliver telegram` |
| 5 | Nightly GitHub backlog triage | `hermes cron create "0 2 * * *" "...gh issue list..." --name "Nightly backlog triage" --deliver telegram`. Respond `[SILENT]` if no new issues. |
| 6 | PR code review | `hermes webhook subscribe github-pr-review --events "pull_request" --skills github-code-review --deliver github_comment --prompt "..."` |
| 7 | Docs drift detection | `hermes cron create "0 9 * * 1" "...gh pr list --state merged..." --name "Docs drift detection"` |
| 8 | Dependency security audit | `hermes cron create "0 6 * * *" "Run a dependency security audit..." --name "Dependency audit" --deliver telegram` |
| 9 | Deploy verification | `hermes webhook subscribe deploy-verify --events "deployment" --deliver telegram --prompt "..."` |
| 10 | Alert triage | `hermes webhook subscribe alert-triage --prompt "Monitoring alert received:..." --deliver slack` |
| 11 | Uptime monitor | `hermes cron create "every 30m" "If the script reports OUTAGE DETECTED..." --script ~/.hermes/scripts/check-uptime.py --name "Uptime monitor" --deliver telegram` |
| 12 | Competitor repo scout | `--skill competitive-pr-scout` (user skill). Schedule `0 8 * * *`. |
| 13 | arXiv paper digest to Obsidian | `hermes cron create "0 8 * * *" "Search arXiv for the 3 most interesting papers..." --skill arxiv --skill obsidian --deliver local` |
| 14 | Issue auto-labeling | `hermes webhook subscribe github-issues --events "issues" --deliver github_comment` |
| 15 | CI failure analysis | A `check_run` webhook route with `deliver: "github_comment"` |
| 16 | Auto-port changes across repos | `hermes webhook subscribe auto-port --events "pull_request" --skills github-pr-workflow --deliver log` |
| 17 | Stripe payment monitoring | `hermes webhook subscribe stripe-payments --events "payment_intent.succeeded,payment_intent.payment_failed,charge.dispute.created" --deliver slack` |
| 18 | Weekly security audit | `hermes cron create "0 3 * * 0" "Run a comprehensive security audit..." --skill codebase-security-audit` (user skill) |
| 19 | Weekly blog outline | `hermes cron create "0 10 * * 3" "...Save the outline to ~/drafts/blog-$(date +%Y%m%d).md" --deliver local` |
| 20 | RAM watchdog, no LLM | `hermes cron create "every 5m" --no-agent --script memory-watchdog.sh --deliver telegram --name "memory-watchdog"` |
| 21 | Quiet nginx check | Prompt: `Check if nginx is running. If everything is healthy, respond with only [SILENT]. Otherwise, report the issue.` |
| 22 | Repo audit with project context | `hermes cron create "every 1d at 09:00" "Audit open PRs, summarize CI health, and post to #eng" --workdir /home/me/projects/acme` |
| 23 | File-change gate | Pre-run script emits `{"wakeAgent": false}` unless file mtime changed |
| 24 | Dedup news scout | `cronjob(action="create", prompt="...", schedule="every 6h", continuity=True)` |
| 25 | Webhook to cron | `hermes webhook subscribe pr-feedback --events "pull_request_review" --cron-job "pr-review-sweeper" --prompt "..."` |

### Further Patterns from Docs [OFFICIAL]

- `deliver_only` Supabase push to Telegram
- Todoist label filter with script
- SQL-count `wakeAgent` gate
- 3-stage `context_from` chain (Recipe 8)
- Twice-daily briefings

### Not Found as Official Recipes [INFERRED]

- SSL expiry watch
- Backup verification
- Social-media drafting (optional `social-media-content-calendar` skill covers planning)
- Inbox summary (bundled `email-inbox-triage` and `himalaya` skills)
- Price and stock monitoring (bundled `product-price-monitor` and optional `stocks` skills)
- Log analysis

### Blueprint Command

```bash
/blueprint    # alias /bp — parameterized templates
```
"Cron Recipes" PR #41309 describes 5 curated starters. Automation Blueprints Catalog reference page exists.

---

## 9. Cron Configuration Keys [OFFICIAL]

```yaml
cron:
  model: ""                    # per-job model pin (overrides main)
  provider: ""                 # per-job provider pin
  enabled_toolsets: []         # default toolsets for cron jobs
  allow_agent_scheduling: false # allow cron-run agents to create cron jobs
  require_restart_safe_scope: false # fail closed if systemd scope unavailable
  script_timeout_seconds: 3600  # env HERMES_CRON_SCRIPT_TIMEOUT
  max_parallel_jobs: 0         # concurrency limit (0 = no limit)
  retry_unreachable: true      # auto re-runs at 5, 15, 30 min on unreachable model
  catch_up_missed: true        # catch up missed runs once
  failure_repeat_alert_hours: 6 # alert cooldown for repeated failures
  failure_nudge_threshold: 3   # review nudge after N failures
  preflight: true              # validate job config before scheduling (marks blocked_config)
  wrap_response: true          # add "Cronjob Response:" header
```

---

## 10. Conflicts

| # | Conflict | Resolution |
|---|----------|------------|
| 1 | Cron schedule syntax: Phase 1/2 placeholder | **Phase 4 resolves**: 5 explicit formats |
| 2 | Delivery targets: Phase 1/2 placeholder | **Phase 4 resolves**: 10+ targets with exact syntax |
| 3 | Script-only mode: not documented in Phase 1/2 | **Phase 4 resolves**: `--no-agent`, `wakeAgent` gate |
| 4 | Job chaining: not documented | **Phase 4 resolves**: `context_from`, `continuity` |
| 5 | Hook event list incomplete | Mark UNVERIFIED |

---

## 11. Gaps

1. Full gateway hook event list
2. Shell hooks `hooks:` block exact schema
3. Plugin hook `register()` API details
4. Outbound webhook `hooks.outbound:` schema
5. `hermes-session-reset-policy` catalog plugin details
6. `/blueprint` command full syntax
7. Automation Blueprints Catalog page not fully read
8. Cron job overlap behavior beyond tick lock (scheduled-tick overlap)

---

## 12. Sources

- https://hermes-agent.nousresearch.com/docs/user-guide/features/cron
- https://hermes-agent.nousresearch.com/docs/user-guide/messaging/webhooks
- https://hermes-agent.nousresearch.com/docs/guides/automation-blueprints
- https://hermes-agent.nousresearch.com/docs/guides/daily-briefing-bot
- https://hermes-agent.nousresearch.com/docs/llms.txt
- Phase 4 Sections 4, 8

---

**FILE COMPLETE: references/13-scheduling-and-automation.md** — Cron mechanics, verbatim commands, 5 schedule formats, delivery targets, script-only mode, wakeAgent, job chaining, hooks/webhooks, 25 recipes verbatim, config keys.