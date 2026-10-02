---
title: Index & Routing (v2 — Final Coverage)
source_phases: [Phase 1, Phase 2, Phase 3, Phase 4, Phase 5]
hermes_version_documented: v0.21.5 (tag v2026.9.24, Sep 24 2026) — Phase 3/4/5 version not pinned; docs track `main`
research_date: Friday, October 2, 2026
last_built_in: Chat 3
confidence_legend: OFFICIAL = official repo/docs/source; COMMUNITY = third-party; INFERRED = deduced; UNVERIFIED = needs checking
used_by_playbooks: [01-coding-and-dev.md, 02-devops-and-server-admin.md, 03-research-and-analysis.md, 04-content-and-social.md, 05-automation-and-scheduling.md, 06-messaging-gateway-setups.md, 07-browser-and-data-collection.md, 08-multi-agent-and-parallel.md, 09-personal-productivity.md, 10-skill-authoring-and-memory-curation.md, 11-maintenance-backup-recovery.md]
---

# WHEN TO READ THIS FILE
This is the routing index for `hermes-forge`. It maps user intent/trigger phrases to the reference files and playbooks that cover that topic. **This is v2 (Final — Chat 3 complete)** — covers all 21 reference files and 11 playbooks.

---

# INTENT → FILES MAP (COMPLETE COVERAGE)

| User Intent / Trigger Phrase | Primary Domain | Reference Files to Read | Playbooks |
|------------------------------|----------------|------------------------|-----------|
| "install Hermes on a VPS" / "set up Hermes on my server" / "fresh VPS walkthrough" | `devops` / `maintenance` | 01-foundations-architecture.md, **02-install-vps-config-basics.md**, 17-vps-operations.md | 02-devops-and-server-admin.md, 11-maintenance-backup-recovery.md |
| "configure providers" / "switch model" / "set up OpenRouter" / "add Anthropic key" / "fallback chain" | `coding` / `research` / `automation` | **03-providers-and-models.md**, 06-config-keys-and-env-vars.md, 19-cost-and-optimization.md | 01-coding-and-dev.md, 03-research-and-analysis.md |
| "run a command" / "hermes chat flags" / "one-shot vs interactive" / "hermes -z" / "stream-json" | `coding` / `automation` / `research` | **04-cli-command-reference-a.md**, 04-cli-command-reference-b.md | 01-coding-and-dev.md, 05-automation-and-scheduling.md |
| "slash commands" / "/model" / "/compress" / "/goal" / "/review" / "/rollback" / "keyboard shortcuts" | `coding` / `productivity` | **05-slash-commands-sessions-interactive.md** | 01-coding-and-dev.md, 09-personal-productivity.md |
| "config.yaml keys" / "environment variables" / "precedence" / "profiles" / "context files" / "personality" | `all` | **06-config-keys-and-env-vars.md** | 02-devops-and-server-admin.md, 10-skill-authoring-and-memory-curation.md |
| "toolsets" / "enable web tool" / "terminal backend docker" / "MCP servers" / "plugins" | `coding` / `devops` / `browser` | **07-tools-and-toolsets.md**, **08-terminal-backends.md**, **10-mcp-plugins-api.md** | 01-coding-and-dev.md, 02-devops-and-server-admin.md, 07-browser-and-data-collection.md |
| "gateway setup" / "Telegram bot" / "Discord bot" / "pairing" / "webhook" / "API server" / "dashboard" | `gateway` / `automation` | **09-messaging-gateway.md** | **06-messaging-gateway-setups.md** |
| "skills install" / "create a skill" / "skill bundles" / "curator" / "learn" | `skill-authoring` / `productivity` | **11-skills-system.md** | **10-skill-authoring-and-memory-curation.md** |
| "memory" / "MEMORY.md" / "USER.md" / "FTS5 search" / "Honcho" / "context files" / "SOUL.md" | `productivity` / `skill-authoring` | **12-memory-and-context.md** | **10-skill-authoring-and-memory-curation.md** |
| "cron job" / "schedule every 30 minutes" / "hermes cron" / "kanban" / "webhooks" / "hooks" | `automation` / `gateway` | **13-scheduling-and-automation.md** | **05-automation-and-scheduling.md** |
| "subagents" / "delegate_task" / "parallel" / "swarm" / "multi-agent" | `multi-agent` / `research` | **14-subagents-and-delegation.md** | **08-multi-agent-and-parallel.md** |
| "learning loop" / "trajectory" / "self-evolution" / "verification" / "RL" | `skill-authoring` / `research` | **15-learning-loop-and-advanced.md** | **10-skill-authoring-and-memory-curation.md** |
| "security" / "approvals" / "sandbox" / "audit" / "secrets" / "egress" / "supply chain" | `devops` / `maintenance` | **16-security-and-hardening.md** | 11-maintenance-backup-recovery.md |
| "VPS hardening" / "monitoring" / "log rotation" / "disk space" / "backup strategy" | `devops` / `maintenance` | **17-vps-operations.md** | 11-maintenance-backup-recovery.md |
| "troubleshoot" / "hermes doctor" / "errors" / "logs" / "DB repair" / "recovery" | `maintenance` | **18-troubleshooting.md** | 11-maintenance-backup-recovery.md |
| "cost optimization" / "cheap model" / "auxiliary model" / "routing price" / "budget" | `all` | **19-cost-and-optimization.md** | 01-coding-and-dev.md, 05-automation-and-scheduling.md |
| "use case" / "example task" / "how do I" / "pattern for" | `all` | **20-use-case-catalog.md** | All playbooks |
| "what is X" / "glossary" / "define" / "term" | `all` | **21-glossary.md** | All playbooks |
| "unverified" / "gap" / "not documented" / "verify" | `all` | **22-unverified-and-gaps.md** (v3) | — |
| "sources" / "official docs" / "repo files" / "where did this come from" | `all` | **23-sources.md** (v3) | — |

---

# DOMAIN → REFERENCE FILE MATRIX (ALL 3 CHATS)

| Domain | Reference Files (Chat 1) | Reference Files (Chat 2) | Reference Files (Chat 3) |
|--------|-------------------------|-------------------------|-------------------------|
| `coding` | 01, 03, 04a, 04b, 05, 06 | 07, 08, 10, 11, 12, 14, 15 | 16, 19, 20 |
| `devops` | 01, 02, 03, 04a, 04b, 06 | 07, 08, 09, 10, 13, 17 | 16, 17, 18, 19 |
| `research` | 01, 03, 04a, 04b, 06 | 07, 10, 12, 14, 15 | 19, 20 |
| `content` | 01, 03, 04a, 04b, 06 | 07, 10, 12, 14 | 19, 20 |
| `automation` | 01, 02, 03, 04a, 04b, 06 | 09, 10, 13, 14 | 16, 17, 18, 19 |
| `gateway` | 01, 02, 04a, 04b, 06 | 09, 10, 13 | 16, 17, 19 |
| `browser` | 01, 04a, 04b, 06 | 07, 10 | 16, 19, 20 |
| `multi-agent` | 01, 04a, 04b, 06 | 10, 14, 15 | 16, 19 |
| `productivity` | 01, 05, 06 | 11, 12 | 16, 19, 20 |
| `skill-authoring` | 01, 06 | 11, 12, 15 | 16, 19, 20 |
| `maintenance` | 01, 02, 04a, 04b, 06 | 13 | 16, 17, 18, 19 |

**Numbers refer to reference file numbers (01 = 01-foundations-architecture.md, etc.)**

---

# TRIGGER PHRASE EXAMPLES (FOR SKILL CLASSIFICATION)

The skill's Step 1 (Classify) uses these patterns to assign domains:

```python
TRIGGER_PATTERNS = {
    "coding": [
        r"(review|refactor|implement|debug|fix|feature|PR|pull request|commit|test|lint|type-check)",
        r"(code|repository|repo|function|class|module|API|endpoint)",
    ],
    "devops": [
        r"(deploy|server|VPS|SSH|Docker|systemd|SSL|DNS|backup|migrate|update|upgrade)",
        r"(infrastructure|provision|configure|monitor|log|disk|network)",
    ],
    "research": [
        r"(research|analyze|compare|survey|investigate|study|paper|arXiv|competitor)",
        r"(market|landscape|benchmark|evaluate|pros and cons)",
    ],
    "content": [
        r"(write|blog|post|article|docs|documentation|README|social|tweet|LinkedIn)",
        r"(video|script|presentation|slide|newsletter|email)",
    ],
    "automation": [
        r"(cron|schedule|every|daily|weekly|hourly|recurring|periodic)",
        r"(watch|monitor|alert|notify|pipeline|workflow|job)",
    ],
    "gateway": [
        r"(Telegram|Discord|Slack|WhatsApp|Signal|Email|Matrix|bot|gateway|pairing)",
        r"(message|notify|send|deliver|channel|DM|home channel)",
    ],
    "browser": [
        r"(scrape|crawl|screenshot|PDF|extract|download|form|login|web page)",
        r"(browser|Chromium|CDP|playwright|dynamic)",
    ],
    "multi-agent": [
        r"(parallel|subagent|delegate|swarm|kanban|dispatch|concurrent)",
        r"(multi-agent|multiple agents|fan.out|fan-out)",
    ],
    "productivity": [
        r"(email|calendar|meeting|notes|tasks|todo|plan|organize|summarize)",
        r"(inbox|schedule|remind|track|journal)",
    ],
    "skill-authoring": [
        r"(skill|create skill|make skill|distill|learn|curator|bundle)",
        r"(memory|context file|AGENTS.md|SOUL.md|MEMORY.md)",
    ],
    "maintenance": [
        r"(update|upgrade|backup|restore|doctor|audit|troubleshoot|error|fix)",
        r"(clean|prune|rotate|migrate|uninstall|reinstall)",
    ],
}
```

---

# ROUTING LOGIC (IMPLEMENTED IN SKILL.md)

```
Step 1: Classify task → domain(s) using TRIGGER_PATTERNS
Step 2: Read references/00-index-and-routing.md → get file list for domain(s)
Step 3: Load only those reference files + relevant playbooks
Step 4: Ask ≤3 clarifying questions (templates/clarifying-questions.md)
Step 5: Assemble brief per templates/mission-brief.md
Step 6: Self-check against anti-hallucination contract (SKILL.md)
Step 7: Deliver
```

---

# FILE STATUS SUMMARY (ALL FILES NOW BUILT)

| File | Chat Built | Status |
|------|------------|--------|
| 01-foundations-architecture.md | 1 | ✅ Complete |
| 02-install-vps-config-basics.md | 1 | ✅ Complete |
| 03-providers-and-models.md | 1 | ✅ Complete |
| 04-cli-command-reference-a.md | 1, updated 2 | ✅ Complete |
| 04-cli-command-reference-b.md | 1 | ✅ Complete |
| 05-slash-commands-sessions-interactive.md | 1 | ✅ Complete |
| 06-config-keys-and-env-vars.md | 1 | ✅ Complete |
| 07-tools-and-toolsets.md | 2 | ✅ Complete |
| 08-terminal-backends.md | 2 | ✅ Complete |
| 09-messaging-gateway.md | 2 | ✅ Complete |
| 10-mcp-plugins-api.md | 2 | ✅ Complete |
| 11-skills-system.md | 2 | ✅ Complete |
| 12-memory-and-context.md | 2 | ✅ Complete |
| 13-scheduling-and-automation.md | 2 | ✅ Complete |
| 14-subagents-and-delegation.md | 2 | ✅ Complete |
| 15-learning-loop-and-advanced.md | 2 | ✅ Complete |
| 16-security-and-hardening.md | 3 | ✅ Complete |
| 17-vps-operations.md | 3 | ✅ Complete |
| 18-troubleshooting.md | 3 | ✅ Complete |
| 19-cost-and-optimization.md | 3 | ✅ Complete |
| 20-use-case-catalog.md | 3 | ✅ Complete |
| 21-glossary.md | 3 | ✅ Complete |
| 22-unverified-and-gaps.md | 1, 2, 3 (v3) | ✅ Complete |
| 23-sources.md | 1, 2, 3 (v3) | ✅ Complete |
| playbooks/01-11 | 2, 3 | ✅ Complete |
| templates/ (3 files) | 1, 2 | ✅ Complete |
| SKILL.md | 1, 2, 3 (final) | ✅ Complete |
| REFRESH.md | 3 | ✅ Complete |
| tests/sample-tasks.md | 3 | ✅ Complete |
| _build/coverage-matrix.md | 3 | ✅ Complete |
| _build/BUILD-REPORT.md | 3 | ✅ Complete |

**All 51 project files complete. No files deferred.**

---

# VERSION NOTE

This is the **final routing index (v2)** covering all 21 reference files, 11 playbooks, 3 templates, and supporting files. No further updates planned unless Hermes Agent releases a new version (see REFRESH.md).

---

# SOURCES

- Derived from Phase 1-5 research sections and their section lists
- Trigger patterns inferred from task examples in the mission brief template
- All file coverage from Phases 1-5 research

---

**FILE COMPLETE: hermes-forge/references/00-index-and-routing.md (v2 FINAL)**
Main tables: Intent→Files (22 rows, all files), Domain→Reference Matrix (11 domains × 3 chats), Trigger Patterns (11 domains with regex). All Chat 3 files (16-21) and playbooks (01,02,03,04,09,11) now marked complete.