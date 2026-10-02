---
title: Simulated Test Suite — hermes-forge Skill Verification
source_phases: [Phase 1, Phase 2, Phase 3, Phase 4, Phase 5]
hermes_version_documented: v0.21.5 (tag v2026.9.24, Sep 24 2026)
test_date: 2026-10-02
---

# tests/sample-tasks.md — Simulated Test Suite

This file contains 25 test tasks covering every playbook domain and major feature. Each test includes:
- **Raw task** (user input)
- **Expected mission brief fragments** (what the skill should produce)
- **Verification criteria** (how to confirm the skill output is correct)
- **Anti-hallucination checks** (specific identifiers that must appear verbatim)

Run these by invoking the hermes-forge skill with each raw task and comparing output to expected fragments.

---

## TEST 1: Coding — Build a Feature

**Raw Task**: "Build a user authentication feature with JWT tokens for my FastAPI app"

**Expected Mission Brief Fragments**:
- Mode: Interactive (`hermes`)
- Backend: `docker`
- Toolsets: `coding` preset
- Skills: `fastapi` (community), `pytest` (community)
- Commands: `hermes -z`, `/model`, `/skill`, `/toolset`
- Config: `model.provider`, `model.default`, `toolset`
- Delivery: Origin

**Anti-Hallucination Checks** (must appear verbatim):
- `toolset: coding` (not "dev" or "developer")
- `hermes -z "..."` (not `hermes chat "..."`)
- `/toolset coding` (slash command, not `--toolset`)
- `docker` (not `local` for web-facing code)
- `HERMES_WRITE_SAFE_ROOT` mentioned for file writes

**Verification**:
- [ ] Output contains complete mission brief with all 18 sections
- [ ] All commands use exact identifiers from reference files
- [ ] No invented skill names (e.g., "fastapi-auth" not in browse)
- [ ] Paste-ready prompt includes ordered steps and tool hints
- [ ] Delivery method specified

---

## TEST 2: Coding — Review PR Nightly

**Raw Task**: "Review every new PR in my repo each night and post summary to Slack"

**Expected Mission Brief Fragments**:
- Mode: Scheduled (`hermes cron`)
- Schedule: `0 2 * * *` (daily 2 AM) or `every night`
- Toolsets: `coding` preset + `github` skill
- Skills: `github` (community)
- Delivery: `slack:#channel` or `slack:@user`
- Config: `approvals.mode: smart`, `github.token`

**Anti-Hallucination Checks**:
- `hermes cron create --schedule "0 2 * * *" --command "..." --name "nightly-pr-review" --deliver "slack:#code-reviews"`
- `--deliver` with comma-separated targets (not space-separated)
- `github` skill (not "github-pr-review" — verify in browse)
- `approvals.mode: smart` (not `manual` for cron)

**Verification**:
- [ ] Cron syntax uses 5-field or natural language from 13-scheduling-and-automation.md
- [ ] Slack delivery format matches 09-messaging-gateway.md
- [ ] GitHub skill name verified against browse
- [ ] Approval mode appropriate for cron

---

## TEST 3: DevOps — Deploy to AWS

**Raw Task**: "Deploy my Docker app to AWS ECS with blue-green"

**Expected Mission Brief Fragments**:
- Mode: Interactive (`hermes`)
- Backend: `docker`
- Toolsets: `devops` preset
- Skills: `aws` (community), `docker` (community)
- Commands: `hermes -z`, terminal commands via `process_manage`
- Config: `aws.profile`, `aws.region`, `approvals.mode: manual`

**Anti-Hallucination Checks**:
- `process_manage` (not `terminal` or `shell`)
- `aws` skill name verified
- `approvals.mode: manual` for production deploy
- `HERMES_WRITE_SAFE_ROOT` for any file operations

**Verification**:
- [ ] Blue-green strategy mentioned with exact AWS CLI commands
- [ ] Manual approval gate before production switch
- [ ] Rollback procedure included

---

## TEST 4: DevOps — Server Health Monitor

**Raw Task**: "Monitor my server health and alert on Telegram if CPU > 90%"

**Expected Mission Brief Fragments**:
- Mode: Scheduled (`hermes cron`)
- Schedule: `*/5 * * * *` (every 5 min)
- Toolsets: `devops` preset + `terminal` (for `htop`/`ps`)
- Backend: `docker` (for isolation)
- Delivery: `telegram`
- Script: `--script ~/scripts/cpu-check.sh --no-agent`

**Anti-Hallucination Checks**:
- `--script --no-agent` for zero-token monitoring
- `telegram` delivery (not `telegram:` with colon in cron create)
- `*/5 * * * *` cron expression (5-field)

**Verification**:
- [ ] Script exits non-zero on alert, zero on OK
- [ ] Cron delivers on non-zero exit
- [ ] Telegram allowlist mentioned

---

## TEST 5: Research — Daily AI Briefing

**Raw Task**: "Brief me daily on AI agent news at 8 AM via Telegram"

**Expected Mission Brief Fragments**:
- Mode: Scheduled (`hermes cron`)
- Schedule: `0 8 * * *`
- Toolsets: `research` preset (or `web` + `browser`)
- Delivery: `telegram`
- Model: Flash class for cost
- Reasoning: `medium`

**Anti-Hallucination Checks**:
- `hermes cron create "0 8 * * *" "..." --deliver telegram --reasoning-effort medium`
- `research` toolset preset (verify exists in `hermes tools preset list`)
- `[SILENT]` fallback if no news

**Verification**:
- [ ] Sources listed (HN, Twitter, arXiv, labs)
- [ ] Top 5 format with links
- [ ] Cost optimization: Flash model, keyless web tier

---

## TEST 6: Research — Competitor Analysis Swarm

**Raw Task**: "Analyze 5 competitors and find gaps vs my product"

**Expected Mission Brief Fragments**:
- Mode: Multi-agent (`/kanban` + `delegate_task`)
- Orchestrator: `delegate_task` with `toolsets: ["research"]`
- Leaves: 5 `delegate_task` with `toolsets: ["web", "browser"]`
- Model: Leaves = Flash, Orch = Sonnet
- Delivery: Kanban + Telegram

**Anti-Hallucination Checks**:
- `/kanban build "..." --workers 5 --verifier`
- `delegate_task` schema: `goal`, `context`, `toolsets`, `model`, `provider`
- `max_concurrent_children=10` (default)
- `max_spawn_depth=1` (flat)

**Verification**:
- [ ] 5 rival tasks + 1 synthesis task
- [ ] Verifier cross-checks
- [ ] Gap matrix output format specified

---

## TEST 7: Research — Paper Query with PageIndex

**Raw Task**: "Answer questions from this 500-page PDF using PageIndex"

**Expected Mission Brief Fragments**:
- Mode: Interactive or one-shot
- Toolsets: `research` + `pageindex` skill/MCP
- Backend: `docker`
- Commands: `hermes skills install pageindex` or `hermes mcp add pageindex`

**Anti-Hallucination Checks**:
- `pageindex` skill/MCP name verified
- Vectorless RAG mentioned
- Page citations required: `[p. X-Y]`

**Verification**:
- [ ] PageIndex explicitly named (not "vector RAG")
- [ ] Confidence levels: high/medium/low
- [ ] Not found handling specified

---

## TEST 8: Content — Draft in Brand Voice

**Raw Task**: "Write 5 tweets in my brand voice about our launch"

**Expected Mission Brief Fragments**:
- Mode: Interactive (`hermes`)
- Personality: `/personality creative` or custom
- Memory: `/memory add "brand voice: ..."`
- Toolsets: `creative` preset
- Delivery: Origin

**Anti-Hallucination Checks**:
- `/personality creative` (exact slash command)
- `/memory add` for voice examples
- 280 char limit per tweet
- Hashtags specified

**Verification**:
- [ ] Voice examples from memory used
- [ ] Character count enforced
- [ ] No auto-post (approval required)

---

## TEST 9: Content — Scheduled LinkedIn Post

**Raw Task**: "Draft weekly LinkedIn post every Monday 9 AM for review"

**Expected Mission Brief Fragments**:
- Mode: Scheduled (`hermes cron`)
- Schedule: `0 9 * * 1`
- Skills: `linkedin-post` (community) or memory-based
- Delivery: `telegram` for review
- Approval: `/approvals manual` before publish

**Anti-Hallucination Checks**:
- `--deliver telegram` for review (not auto-post)
- `/approvals manual` in workflow
- LinkedIn style: hook, 3-5 bullets, CTA, 3-5 hashtags

**Verification**:
- [ ] Draft saved to file for review
- [ ] Telegram delivery for approval
- [ ] No publish without `/approve`

---

## TEST 10: Content — Autonomous Novel Pipeline

**Raw Task**: "Run the autonomous novel pipeline from autonovel repo"

**Expected Mission Brief Fragments**:
- Mode: Pipeline (autonovel repo)
- Backend: `docker`
- Stages: outline → chapters → audiobook → site
- Skills: `autonovel` from NousResearch repo
- Delivery: File + Telegram milestones

**Anti-Hallucination Checks**:
- `git clone https://github.com/NousResearch/autonovel`
- 19 chapters specified
- ElevenLabs TTS for audiobook
- Checkpoint after each stage

**Verification**:
- [ ] Repo URL exact
- [ ] 19 chapters hardcoded
- [ ] Milestone delivery via Telegram

---

## TEST 11: Content — Tech News Triage

**Raw Task**: "Sort tech news by urgency into Discord channels every 30 min"

**Expected Mission Brief Fragments**:
- Mode: Scheduled (`hermes cron`)
- Schedule: `*/30 * * * *`
- Toolsets: `research` preset
- Delivery: `discord:#breaking,discord:#important,discord:#interesting`
- Classification: 🔴 🟡 🟢

**Anti-Hallucination Checks**:
- Discord delivery format: `discord:#channel` (comma-separated)
- Classification emojis exact
- Deduplication against 24h memory

**Verification**:
- [ ] Three channels specified
- [ ] Max items per run limited
- [ ] Low reasoning effort

---

## TEST 12: Personal — Daily Morning Briefing

**Raw Task**: "Brief me every morning at 8 AM with calendar, tasks, news, weather"

**Expected Mission Brief Fragments**:
- Mode: Scheduled (`hermes cron`)
- Schedule: `0 8 * * *`
- Toolsets: `personal` preset
- Delivery: `telegram`
- Sections: Calendar, Tasks, News, Weather, Reminders

**Anti-Hallucination Checks**:
- `personal` toolset preset (verify)
- Calendar skill or memory
- Task skill or memory
- Weather from memory (user-set)

**Verification**:
- [ ] Telegram card format with emojis
- [ ] [SILENT] fallback
- [ ] Data sources for each section

---

## TEST 13: Personal — Two-Tier Email

**Raw Task**: "Only call LLM when new mail arrives"

**Expected Mission Brief Fragments**:
- Mode: Two-tier (script + LLM)
- Tier 1: `--script ~/scripts/check-mail.sh --no-agent` every 15 min
- Tier 2: `--continuity --context-from mail-check` on detection
- Skills: `himalaya` or `email-inbox-triage`
- Delivery: `telegram` (Tier 2)

**Anti-Hallucination Checks**:
- `--script --no-agent` for Tier 1
- `--continuity --context-from` for chaining
- Script exits 1 on new mail, 0 on none
- Himalaya CLI for IMAP

**Verification**:
- [ ] Zero tokens for Tier 1
- [ ] Tier 2 only triggers on detection
- [ ] Drafts saved to file

---

## TEST 14: Personal — Apartment Scouting

**Raw Task**: "Curate top 3 apartment listings by 8:30 AM daily"

**Expected Mission Brief Fragments**:
- Mode: Chained cron (scout 8:00 → deliver 8:30)
- Toolsets: `personal` + `browser` + `web`
- Schedule: `0 8 * * *` + `30 8 * * *`
- Delivery: `telegram`
- Criteria in memory

**Anti-Hallucination Checks**:
- Two cron jobs with `--context-from`
- Criteria in memory (location, price, bedrooms, must-haves)
- Scoring algorithm specified

**Verification**:
- [ ] Scout saves file, deliver reads file
- [ ] Photos, links, contact in delivery
- [ ] Sources listed

---

## TEST 15: Personal — Family WhatsApp

**Raw Task**: "Friday family reminder via WhatsApp at 9 AM"

**Expected Mission Brief Fragments**:
- Mode: Gateway (WhatsApp) + cron
- Schedule: `0 9 * * 5`
- Gateway: `hermes whatsapp` pairing
- Allowlist: `WHATSAPP_ALLOWED_USERS`
- Delivery: `whatsapp` (group)

**Anti-Hallucination Checks**:
- `hermes whatsapp` pairing command
- `WHATSAPP_ALLOWED_USERS` in `.env`
- Group delivery (not DM)
- Memory for plans, grocery, chores

**Verification**:
- [ ] Gateway paired before cron
- [ ] Allowlist numeric IDs only
- [ ] Friendly format with emojis

---

## TEST 16: Personal — ETF Yield Check

**Raw Task**: "Cross-check ETF yields daily at 7 AM weekdays"

**Expected Mission Brief Fragments**:
- Mode: Scheduled (`hermes cron`)
- Schedule: `0 7 * * 1-5`
- Toolsets: `personal` + `web` + sheet skill
- Delivery: `telegram`
- Watchlist in memory

**Anti-Hallucination Checks**:
- `1-5` for weekdays in cron
- Yield comparison with previous day
- Flag threshold: > 0.1%
- Full table in file, flags only in Telegram

**Verification**:
- [ ] Sources: Yahoo Finance, ETF.com
- [ ] Change calculation correct
- [ ] File + Telegram dual output

---

## TEST 17: Personal — Voice Assistant

**Raw Task**: "Set up voice assistant on smart glasses"

**Expected Mission Brief Fragments**:
- Mode: Gateway + `/voice` + TTS
- Backend: `docker`
- Skills: `elevenlabs` (community)
- Commands: `/voice on`, `Ctrl+B` record key
- Delivery: Voice channel

**Anti-Hallucination Checks**:
- `/voice on` slash command
- `voice.record_key: Ctrl+B` config
- ElevenLabs TTS skill/MCP
- Gateway auto-transcribe + TTS reply

**Verification**:
- [ ] End-to-end voice flow described
- [ ] CLI and gateway both covered
- [ ] Language from memory

---

## TEST 18: Personal — Smoker Monitor

**Raw Task**: "Monitor pellet smoker overnight, alert if temp drifts >10°F"

**Expected Mission Brief Fragments**:
- Mode: Scheduled script (`hermes cron --script --no-agent`)
- Schedule: `*/15 22-6 * * *` (10 PM - 6 AM)
- Script: curls smoker API, checks temp
- Delivery: `telegram` on alert
- Tolerance: ±10°F

**Anti-Hallucination Checks**:
- `--script --no-agent` (zero tokens)
- Schedule `22-6` for overnight
- Script exits 1 + alert on drift, 0 + [SILENT] on OK
- Smoker API endpoint in script

**Verification**:
- [ ] Target temp and tolerance specified
- [ ] Alert format exact
- [ ] Fallback for API failure

---

## TEST 19: Maintenance — Safe Update

**Raw Task**: "Update Hermes safely with backup and verification"

**Expected Mission Brief Fragments**:
- Mode: Interactive
- Commands: `hermes update --check`, `hermes backup --label`, `hermes update --backup --restart-gateway --yes`, `hermes doctor`, `hermes gateway status`
- Rollback: `hermes import <backup> --force`

**Anti-Hallucination Checks**:
- `--check` before update
- `--label` with timestamp
- `--backup --restart-gateway --yes` together
- `hermes doctor` after update
- Rollback procedure explicit

**Verification**:
- [ ] Gateway stop NOT required (handled by --restart-gateway)
- [ ] Test message after update
- [ ] Version verification

---

## TEST 20: Maintenance — Weekly Encrypted Backup

**Raw Task**: "Weekly encrypted backup to offsite storage"

**Expected Mission Brief Fragments**:
- Mode: Scheduled script (`--script --no-agent`)
- Schedule: `0 3 * * 0` (Sunday 3 AM)
- Script: `hermes backup` + `age` encrypt + `rclone` sync + prune
- Delivery: `telegram` status

**Anti-Hallucination Checks**:
- `age -r <recipient>` encryption
- `rclone copy` to remote
- Prune local >14 days
- Zero tokens

**Verification**:
- [ ] Encryption before upload
- [ ] Offsite remote configured
- [ ] Telegram status format

---

## TEST 21: Maintenance — Monthly Restore Drill

**Raw Task**: "Monthly restore test on scratch server"

**Expected Mission Brief Fragments**:
- Mode: Interactive on scratch server
- Steps: Provision → Install → Stop prod gateway → Download → Decrypt → Import → Verify → Test → Report
- Critical: Stop production gateway FIRST (409 Conflict)
- Report: `telegram` PASS/FAIL

**Anti-Hallucination Checks**:
- `hermes gateway stop` on production BEFORE backup
- Same Hermes version on scratch
- `hermes import --force`
- `hermes doctor`, `hermes gateway start`, test message

**Verification**:
- [ ] 409 Conflict prevention emphasized
- [ ] Version matching
- [ ] Production gateway restarted after

---

## TEST 22: Maintenance — Session Hygiene

**Raw Task**: "Clean old sessions and optimize database weekly"

**Expected Mission Brief Fragments**:
- Mode: Scheduled (`hermes cron`)
- Schedule: `0 4 * * 0`
- Commands: `hermes sessions prune --older-than 30 --dry-run`, then `--yes`, `hermes sessions optimize`, `hermes sessions pin`
- Delivery: `telegram`

**Anti-Hallucination Checks**:
- `--older-than 30` (days)
- `--dry-run` first
- `--yes` only if >100 sessions
- `optimize` after prune
- Pin from memory

**Verification**:
- [ ] Before/after counts in report
- [ ] Disk freed reported
- [ ] Pinned sessions preserved

---

## TEST 23: Maintenance — Key Rotation

**Raw Task**: "Rotate all API keys quarterly"

**Expected Mission Brief Fragments**:
- Mode: Interactive (manual)
- Steps: Inventory `.env` → Generate new at each provider → Update `.env` → `hermes gateway restart` → Test each → Revoke old
- Log: `/memory add "Key rotation: $(date +%F)"`

**Anti-Hallucination Checks**:
- Edit `~/.hermes/.env` directly (not `config set`)
- `chmod 600 ~/.hermes/.env`
- `hermes gateway restart` after update
- Test each integration
- Revoke at provider dashboards

**Verification**:
- [ ] All keys in .env inventoried
- [ ] Each tested after rotation
- [ ] Old keys revoked
- [ ] Rotation logged

---

## TEST 24: Maintenance — Health Monitor

**Raw Task**: "Daily health check with metrics at 6 AM"

**Expected Mission Brief Fragments**:
- Mode: Scheduled script (`--script --no-agent`)
- Schedule: `0 6 * * *`
- Script: version, gateway, disk, sessions, skills, cron, errors, usage
- Delivery: `telegram`

**Anti-Hallucination Checks**:
- `--script --no-agent`
- `hermes --version`, `hermes gateway status`, `df -h ~/.hermes`
- `hermes logs --level ERROR --since 24h`
- `hermes usage --days 7`

**Verification**:
- [ ] All metrics collected
- [ ] Telegram at 6 AM
- [ ] Errors section actionable

---

## TEST 25: Maintenance — Migration to New Server

**Raw Task**: "Migrate Hermes to new VPS"

**Expected Mission Brief Fragments**:
- Mode: Interactive (both servers)
- Old: `hermes gateway stop` → `hermes backup` → encrypt → transfer
- New: Provision → Install → Decrypt → `hermes import --force` → Verify → Switch
- Critical: Old gateway stopped first

**Anti-Hallucination Checks**:
- `hermes gateway stop` BEFORE backup
- Encrypt for transfer
- Same/higher version on new
- `hermes import --force`
- Verify before DNS switch

**Verification**:
- [ ] 409 Conflict prevention
- [ ] Pairing data works on new
- [ ] All skills, memory, cron present
- [ ] Old decommissioned after verification

---

## ANTI-HALLUCINATION MASTER CHECKLIST

For EVERY test output, verify these identifiers appear EXACTLY as documented:

| Category | Must Appear Verbatim | Must NOT Appear |
|----------|---------------------|-----------------|
| CLI | `hermes`, `hermes -z`, `hermes cron`, `hermes gateway`, `hermes skill`, `hermes mcp`, `hermes auth`, `hermes backup`, `hermes import`, `hermes doctor`, `hermes update`, `hermes profile`, `hermes config`, `hermes sessions`, `hermes tools`, `hermes skills`, `hermes curator`, `hermes webhook`, `hermes pairing`, `hermes whatsapp` | `hermes-cli`, `hermes chat`, `hermes run` |
| Slash Commands | `/model`, `/skill`, `/toolset`, `/context`, `/memory`, `/checkpoint`, `/compact`, `/cost`, `/approve`, `/deny`, `/approvals`, `/mode`, `/personality`, `/reasoning`, `/voice`, `/exit`, `/quit`, `/help`, `/status`, `/logs`, `/usage`, `/journey`, `/kanban`, `/learn` | `/set-model`, `/use-skill`, `--toolset` |
| Config Keys | `model.provider`, `model.default`, `model.temperature`, `model.max_tokens`, `toolset`, `skills`, `approvals.mode`, `approvals.cron_mode`, `approvals.unattended_mode`, `terminal_backend`, `gateway_port`, `gateway_host`, `mcp_servers`, `context_files`, `persona`, `schedule`, `subagent_delegation`, `cost_limit`, `delivery_method`, `notification_target` | `model_name`, `provider_name`, `toolsets`, `skill_list`, `approval_mode` |
| Env Vars | `HERMES_MODEL`, `HERMES_PROVIDER`, `HERMES_API_KEY`, `HERMES_HOME`, `HERMES_CONFIG`, `HERMES_GATEWAY_PORT`, `HERMES_MCP_CONFIG`, `HERMES_TOOLSETS`, `HERMES_SKILLS`, `HERMES_APPROVAL_MODE`, `HERMES_TERMINAL_BACKEND`, `HERMES_COST_LIMIT`, `HERMES_DELIVERY_WEBHOOK`, `HERMES_TELEGRAM_BOT_TOKEN`, `HERMES_TELEGRAM_CHAT_ID` | `HERMES_MODEL_NAME`, `HERMES_APIKEY`, `HERMES_CONFIG_FILE` |
| Toolsets | `coding`, `debugging`, `safe`, `research`, `devops`, `creative`, `personal` (verify exact names) | `developer`, `dev`, `researcher`, `admin`, `writer` |
| Skills | Exact names from `hermes skills browse` | Invented names like "fastapi-auth", "github-pr-review" |
| Gateway Delivery | `telegram`, `discord:#channel`, `slack:#channel`, `slack:@user`, `whatsapp`, `email`, `webhook`, `local` | `telegram:`, `discord:`, `slack:` without channel |
| Cron Schedule | `0 8 * * *`, `*/30 * * * *`, `every 2h`, `every monday 9am`, `in 30m`, ISO format | `daily`, `weekly`, `monthly` (unless natural language) |
| Backends | `local`, `docker`, `ssh`, `singularity`, `modal`, `daytona`, `vercel_sandbox` | `container`, `vm`, `remote`, `cloud` |
| Tools | `process_manage`, `todo_list`, `cronjob_manage`, `web_search`, `web_extract`, `browser_navigate`, `browser_click`, `browser_type`, `read_file`, `write_file`, `patch`, `search_files`, `terminal`, `skill_manage`, `skill_view`, `memory`, `delegate_task` | `shell`, `bash`, `cmd`, `execute`, `run` |
| Memory | `MEMORY.md`, `USER.md`, `/memory add`, `/memory list`, `honcho_profile`, `honcho_search`, `honcho_reasoning`, `honcho_context`, `honcho_conclude` | `memory.txt`, `user.txt`, `remember`, `recall` |
| Delegation | `delegate_task`, `max_concurrent_children`, `max_spawn_depth`, `orchestrator`, `subagent` | `spawn_agent`, `sub_agent`, `parallel_agent` |

---

## RUNNING THE TEST SUITE

```bash
# For each test task:
/skill hermes-forge "Raw task from test"

# Compare output to expected fragments
# Check anti-hallucination checklist
# Mark verification items

# Aggregate results:
# PASS: All fragments present, all anti-hallucination checks pass
# FAIL: Missing fragments, invented identifiers, wrong syntax
# PARTIAL: Most correct but minor issues (unverified items, missing optional sections)
```

---

## EXPECTED RESULTS SUMMARY

| Test | Domain | Expected Status |
|------|--------|-----------------|
| 1 | Coding | PASS |
| 2 | Coding | PASS |
| 3 | DevOps | PASS |
| 4 | DevOps | PASS |
| 5 | Research | PASS |
| 6 | Research | PASS |
| 7 | Research | PARTIAL (pageindex UNVERIFIED) |
| 8 | Content | PASS |
| 9 | Content | PASS |
| 10 | Content | PARTIAL (autonovel pipeline details UNVERIFIED) |
| 11 | Content | PASS |
| 12 | Personal | PASS |
| 13 | Personal | PASS |
| 14 | Personal | PASS |
| 15 | Personal | PASS |
| 16 | Personal | PASS |
| 17 | Personal | PARTIAL (smart glasses UNVERIFIED) |
| 18 | Personal | PASS |
| 19 | Maintenance | PASS |
| 20 | Maintenance | PASS |
| 21 | Maintenance | PASS |
| 22 | Maintenance | PARTIAL (sessions prune flags UNVERIFIED) |
| 23 | Maintenance | PASS |
| 24 | Maintenance | PASS |
| 25 | Maintenance | PASS |

**Target**: 20+ PASS, 5 PARTIAL (due to UNVERIFIED items), 0 FAIL

---

**FILE COMPLETE: hermes-forge/tests/sample-tasks.md**
Lines: ~750 | 25 test tasks covering all 11 playbooks, anti-hallucination master checklist, running instructions, expected results.