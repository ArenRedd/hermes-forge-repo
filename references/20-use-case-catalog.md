---
title: Use Case Catalog Reference
source_phases: [Phase 5]
hermes_version_documented: v0.21.5 (tag v2026.9.24, Sep 24 2026) — Phase 5 version caveat applies
research_date: Friday, October 2, 2026
last_built_in: Chat 3
confidence_legend: OFFICIAL = official repo/docs/source; COMMUNITY = third-party; INFERRED = deduced; UNVERIFIED = needs checking
used_by_playbooks: [01-coding-and-dev.md, 02-devops-and-server-admin.md, 03-research-and-analysis.md, 04-content-and-social.md, 05-automation-and-scheduling.md, 06-messaging-gateway-setups.md, 07-browser-and-data-collection.md, 08-multi-agent-and-parallel.md, 09-personal-productivity.md, 11-maintenance-backup-recovery.md, 20-use-case-catalog.md]
---

# WHEN TO READ THIS FILE
Read this file when you need the complete catalog of 100+ use cases for Hermes Agent, organized by domain. Contains all 98 rows from Phase 5 research with domain, task, tools/toolsets/skills/config needed, example prompt, source tag, and difficulty level. Also includes the top 20 things to do first on a new VPS (ranked), case studies with links, and a use case → playbook index.

---

# TABLE OF CONTENTS
1. [Use Case → Playbook Index](#1-use-case--playbook-index)
2. [Master Use Case Catalog (98 Rows)](#2-master-use-case-catalog-98-rows)
3. [Top 20 Things to Do First on a New VPS (Ranked)](#3-top-20-things-to-do-first-on-a-new-vps-ranked)
4. [Case Studies and Showcases](#4-case-studies-and-showcases)
5. [Conflicts](#5-conflicts)
6. [Gaps](#6-gaps)
7. [Sources](#7-sources)

---

# 1. USE CASE → PLAYBOOK INDEX

| Domain | Playbook | Use Case Numbers |
|--------|----------|------------------|
| Dev | 01-coding-and-dev.md | 1–17 |
| DevOps | 02-devops-and-server-admin.md | 18–28 |
| Research | 03-research-and-analysis.md | 29–37 |
| Content | 04-content-and-social.md | 38–46 |
| Social | 04-content-and-social.md | 47–50 |
| Scraping | 07-browser-and-data-collection.md | 51–55 |
| Biz | 09-personal-productivity.md | 56–68 |
| Finance | 09-personal-productivity.md | 69–71 |
| Learn | 10-skill-authoring-and-memory-curation.md | 72–75 |
| Home | 09-personal-productivity.md | 76–81 |
| SecOps | 02-devops-and-server-admin.md | 82–86 |
| Creative | 04-content-and-social.md | 87–90 |
| RL/data | 08-multi-agent-and-parallel.md | 91–94 |
| Platform | 02-devops-and-server-admin.md | 95–98 |

---

# 2. MASTER USE CASE CATALOG (98 ROWS)

**Legend:** Src = [O] official or official-repo-linked, [C] community-reported. Level: B=Beginner, I=Intermediate, A=Advanced. "Example prompt" cells are illustrative wording and are [INFERRED]. Tool names are generic categories unless the identifier was seen verbatim. **Target was ≥100; 98 rows below. PARTIAL: most are community-reported and not independently verified.** [Phase 5 Section 1]

| # | Domain | Task | Needs | Example Prompt | Src | Lvl |
|---|--------|------|-------|----------------|-----|-----|
| 1 | Dev | Solo-build a full-stack app, review via Telegram | `terminal`, file tools, git, gateway | "Implement the invoice module, run tests, report" | C | I |
| 2 | Dev | Periodic PR review (no webhook) | cron, GitHub skill | "Every hour review new PRs on repo X" | O/C | I |
| 3 | Dev | Real-time PR comments via signed GitHub webhook | gateway webhook, GitHub skill | "On PR opened, post a review" | O/C | A |
| 4 | Dev | Spec PDF forwarded on Telegram → reviewed PR | gateway, terminal, git | "Add this PDF's data to the site, run tests" | C | I |
| 5 | Dev | Work to a completion contract | `/goal`, verification hooks | "/goal: all tests green and lint clean" | O | I |
| 6 | Dev | Undo agent damage | `/rollback` checkpoints | "/rollback 1" | O/C | B |
| 7 | Dev | Parallel branches via worktrees | `hermes worktree`, git | "Work on 3 issues in separate worktrees" | O | A |
| 8 | Dev | Multi-agent swarm from Slack (workers, verifier, synthesizer) | `/kanban`, `~/.hermes/kanban.db` | "/kanban build X with a verifier" | O | A |
| 9 | Dev | Specialist dev-team profiles with toolset limits | profiles, toolset restrictions | "Install the 9-role team installer" | C | A |
| 10 | Dev | Delegate coding to Codex/Claude Code/OpenCode | ACP skill, `delegate_task` | "Hand refactor to Claude Code, review result" | C | A |
| 11 | Dev | One model builds, another audits overnight | `delegate_task`, cron | "Audit yesterday's diff with a second model" | C | A |
| 12 | Dev | Ship micro-apps to Val Town | terminal, API key | "Deploy this idea as a Val" | C | I |
| 13 | Dev | Code intelligence via tree-sitter MCP | MCP server (jMunch) | "Map call graph for module Y" | C | I |
| 14 | Dev | Expose Hermes tools to Claude Desktop/Cursor | `hermes mcp serve` | "Serve Hermes tools over MCP" | C | A |
| 15 | Dev | Accumulate repo knowledge as skills | `skill_manage`, memory | "Remember our deploy quirks as a skill" | C | B |
| 16 | Dev | Desktop coding Projects (project→repo→lane) | Hermes Desktop | "Open project, start lane" | O | I |
| 17 | Dev | Local-model coding on GPU | local model, `custom` provider | "Refactor this file" (Qwen/Gemma local) | C | A |
| 18 | DevOps | 24/7 VPS server management | `terminal`, SSH backend | "Check disk and failed units, fix" | C | I |
| 19 | DevOps | One-command client deployments | Ansible, Docker, 1Password | "Deploy agent for client Z" | C | A |
| 20 | DevOps | Run on Kubernetes, config via PR review | operator/manifests | "kubectl get declared agent state" | C | A |
| 21 | DevOps | Watch blockchain validators, alert on state change | skill, cron, Telegram | "Alert only on up↔down transitions" | C | I |
| 22 | DevOps | Auto-redeploy from private fork | Gitea, Watchtower, podman | "Build image on merge to main" | C | A |
| 23 | DevOps | Nightly config+DB backup to GitHub | cron, git | "Back up ~/.hermes nightly" | C | I |
| 24 | DevOps | 20 cron "signals" → daily ledger → triage job | cron, scripts | "Triage today's ledger" | C | A |
| 25 | DevOps | Home Assistant add-on host | HA add-on | "Run agent inside HA" | C | I |
| 26 | DevOps | Track everything the agent installs | audit plugin/script | "List packages installed this week" | C | I |
| 27 | DevOps | Reach locked-down laptop via outbound WSS | custom bridge | "Run command on my work laptop" | C | A |
| 28 | DevOps | Tool-call audit into SQLite + Grafana | community plugin | "Show top tools by cost" | C | A |
| 29 | Research | Daily research brief to Discord/Slack/Notion | cron, web tools, delivery | "Brief me daily on agent news" | C | I |
| 30 | Research | LLM-maintained wiki second brain | git, Telegram, static site | "Ingest this link into the wiki" | C | I |
| 31 | Research | Parse a huge PDF manual with SQLite FTS5 skill | custom skill | "Index this 3,799-page manual" | C | A |
| 32 | Research | Vectorless RAG (PageIndex) | skill/MCP | "Answer from this doc's outline" | C | A |
| 33 | Research | Mixture-of-Agents council as a model | MoA preset | "/model my-council" | O | I |
| 34 | Research | Autonomous experiment bookkeeping | hermes-lab | "Schedule next experiment" | C | A |
| 35 | Research | Pharma data workflows (ChEMBL/OpenFDA) | skills | "Summarize target X" | C | A |
| 36 | Research | Low-cost research stack (SearXNG + MCPs) | SearXNG, MCP | "Research Z with free-tier sources" | C | A |
| 37 | Research | Competitor-analysis swarm | `delegate_task` | "Find gaps vs 5 rivals" | C | A |
| 38 | Content | Dictate ideas on phone → structured docs | Telegram, voice transcription | (voice memo) | C | B |
| 39 | Content | Draft in your voice from past scripts | memory, file reads | "Write tweets in my style" | C | B |
| 40 | Content | LinkedIn post skill that remembers style | skill | "Draft today's post" | C | B |
| 41 | Content | Weekly YouTube-topic research | cron + skill | "Mondays 9:00 research top AI tools" | C | B |
| 42 | Content | Autonomous novel pipeline (19 chapters, 79,456 words, audiobook, site) | autonovel repo | (pipeline-driven) | O | A |
| 43 | Content | Tech-news triage into Discord channels | cron, Discord | "Sort news by urgency" | C | I |
| 44 | Content | Locale skill pack (TRY markets, Turkish news) | skills, cron | "Daily briefing card" | C | I |
| 45 | Content | Manim explainer videos | skill | "Animate this concept" | C | I |
| 46 | Content | Generative visuals in TouchDesigner | skill/MCP | "Build a generative scene" | C | A |
| 47 | Social | Scheduled X posting (check ToS) | `xurl` skill | "Post one tip daily" | C | I |
| 48 | Social | Meta Ads skill pack | Meta CLI/MCP | "Pull ad performance" | C | I |
| 49 | Social | UGC ad brief from product URL | scraping skills | "Brief from this URL" | C | I |
| 50 | Social | Lifecycle email campaigns | Sequenzy skills/CLI | "Draft onboarding sequence" | O/C | I |
| 51 | Scraping | Route agents via residential IP to avoid 403s | proxy | "Fetch site through home IP" | C | A |
| 52 | Scraping | Free web search/fetch/crawl via MCP (Hound) | MCP | "Crawl this docs site" | C | I |
| 53 | Scraping | Scrape/search with Firecrawl | Firecrawl key | "Extract pricing table" | C | I |
| 54 | Scraping | Browser harness on VPS | browser tool | "Log in and download report" | C | A |
| 55 | Scraping | Keyless web tier (5-vendor rotation) | built in (v0.20.5) | "Search the web" | O | B |
| 56 | Biz | Weekday inbox summary to Slack | email skill, cron | "9am summarize inbox" | C | I |
| 57 | Biz | Two-tier email: script detects, LLM acts | `hermes chat -q` | "Only call LLM when new mail" | C | A |
| 58 | Biz | Daily apartment scouting from alerts | Himalaya CLI, cron | "Curate 1–3 listings by 8:30" | C | I |
| 59 | Biz | Summarize 11 WhatsApp groups | WhatsApp gateway | "Digest site updates" | C | I |
| 60 | Biz | Agent runs support/X/finance follow-ups (Gumroad) | cron, dedicated host | "Check tickets, update finance doc" | C | A |
| 61 | Biz | Triage tickets in PM software | Plane, MCP | "Triage and start new tickets" | C | A |
| 62 | Biz | Business brain in Obsidian | vault sync | "Log this SOP" | C | I |
| 63 | Biz | Chief-of-Staff + per-project sub-profiles | profiles, Slack, backup | "Daily WhatsApp report" | C | A |
| 64 | Biz | Google Workspace automation | google-workspace skill, OAuth | "Create slides from outline" | O/C | I |
| 65 | Biz | Family assistant on WhatsApp | gateway, allowlist | "Remind us Friday" | C | I |
| 66 | Biz | Sell install/config service to SMBs | VPS, Docker | (service business) | C | I |
| 67 | Biz | Meeting transcription | skill | "Transcribe this Meet" | C | I |
| 68 | Biz | Supabase CRM assistant | MCP | "Add lead, set follow-up" | C | I |
| 69 | Finance | Daily ETF-yield summary | sheet access, cron | "Cross-check yields daily" | C | I |
| 70 | Finance | ETF research desk (research only) | skills, Docker, egress proxy | "Research allocation scenarios" | C | A |
| 71 | Finance | Prediction-market monitors (profit claims unverified; high risk) | cron, APIs | "Scan markets hourly" | C | A |
| 72 | Learn | Turn workflow into skill | `/learn` | "/learn the deploy flow" | O | B |
| 73 | Learn | Evolve skills/prompts with DSPy+GEPA (~$2–10/run) | self-evolution repo | "--skill github-code-review" | O | A |
| 74 | Learn | Learn-for-the-human plugin | plugin | "Quiz me on today's work" | C | I |
| 75 | Learn | Workshop on open-weight agents | local model | "Personalized news briefing" | C | I |
| 76 | Home | Pellet smoker monitoring | custom tool | "Hold 225°F overnight" | C | A |
| 77 | Home | Vehicle status and remote start | skill | "Battery level?" | C | I |
| 78 | Home | Pi/mini-PC always-on home server | Linux, Telegram | "Daily digest" | C | I |
| 79 | Home | ESP32 status light | bridge, hooks | (status LEDs) | C | A |
| 80 | Home | Health data (Whoop/Health Connect) | local webhook/plugin | "Sleep average?" | C | A |
| 81 | Home | Voice front end on smart glasses | app | (voice) | C | A |
| 82 | SecOps | DFIR/CTI work in isolated profile | profiles | "Summarize IOC feed" | C | A |
| 83 | SecOps | Daily cybersec briefing on local k8s | cron | "Morning threat brief" | C | I |
| 84 | SecOps | Mail gatekeeper hiding 2FA/banking mail | local proxy | "Draft replies, never show codes" | C | A |
| 85 | SecOps | Audit approval-gate compliance in history | session DB | (issue #17619) | C | A |
| 86 | SecOps | Exposure audit script (ports, `.env` 600, backups) | shell | "Run exposure audit" | C | I |
| 87 | Creative | Kid-mode console | custom UI | (voice) | C | A |
| 88 | Creative | Live2D desktop pet | TTS, Tailscale | (cron-triggered speech) | C | A |
| 89 | Creative | CLI skins | skins dir | "Matrix theme" | O/C | B |
| 90 | Creative | Spotify playlists | Spotify integration | "10-min rowing playlist" | C | B |
| 91 | RL/data | Batch trajectory generation | `batch_runner.py` | (CLI) | O | A |
| 92 | RL/data | Atropos RL environments | tinker-atropos | (research) | O | A |
| 93 | RL/data | Trajectory compression for training | repo tooling | (research) | O | A |
| 94 | RL/data | Export sessions as HF-ready traces | `hermes sessions export --redact` | (CLI) | O | I |
| 95 | Platform | Android host via Termux (signed APT repo) | Termux | "hermes" | O | I |
| 96 | Platform | iMessage via Photon | `hermes photon login` | (iMessage) | O | I |
| 97 | Platform | Run Hermes as Paperclip managed employee | hermes-paperclip-adapter | (Paperclip tasks) | O | A |
| 98 | Platform | Linux desktop control MCP | computer-use-linux | "Click Save" | O (README link) | A |

---

# 3. TOP 20 THINGS TO DO FIRST ON A NEW VPS (RANKED)

Items marked **(I)** are judgment from official security guidance. Others are official procedures. [INFERRED unless noted] [Phase 5 Section 1]

| Rank | Action | Justification |
|------|--------|---------------|
| 1 | Create a non-root user. The official checklist says never run the gateway as root, and the Docker image refuses root by default. | [OFFICIAL] |
| 2 | SSH keys only, no root login, firewall default-deny. A VPS with public SSH is scanned within minutes. | (I) |
| 3 | Install Hermes (`curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash`), then `hermes doctor`. | [OFFICIAL] |
| 4 | Pick a model: `hermes model`, or `hermes setup --portal` for Nous Portal. | [OFFICIAL] |
| 5 | `chmod 600 ~/.hermes/.env`. | [OFFICIAL] |
| 6 | Set an explicit chat allowlist (`TELEGRAM_ALLOWED_USERS=…`). Never `GATEWAY_ALLOW_ALL_USERS=true`. | [OFFICIAL] |
| 7 | Set `terminal.backend: docker` for gateway use. | [OFFICIAL] |
| 8 | Install the gateway as a service (`hermes gateway install`) with lingering. | [OFFICIAL/C] |
| 9 | Make a first backup (`hermes backup`) and test `hermes import` on a scratch box. | [OFFICIAL] |
| 10 | Add `approvals.deny` rules and keep `approvals.mode` at `smart` or `manual`. | [OFFICIAL] |
| 11 | Keep dashboard and API server on loopback; reach them over SSH tunnel or Tailscale. | [OFFICIAL] |
| 12 | Set provider-side spend limits (OpenRouter key limit and others) before any cron. | (I) |
| 13 | Use `hermes update --check`, then `--backup`, on a schedule you control. | [OFFICIAL] |
| 14 | Create one boring, reliable cron job (daily digest) before adding more. | [C: "start with one small workflow"] |
| 15 | Use `--script --no-agent` cron where no LLM reasoning is needed. | [C] |
| 16 | Install only first-party and well-known skills; read `SKILL.md` before enabling. | (I) |
| 17 | Split work/personal into profiles (`hermes profile create <name>`). | [OFFICIAL] |
| 18 | Enable log tailing (`hermes logs --follow`) and a weekly `hermes sessions prune --older-than 30 --dry-run`. | [C/O] |
| 19 | Wire up one notification path (Telegram/Discord) for failures. | (I) |
| 20 | Try `/learn` on one real workflow after a week of use. | [O] |

---

# 4. CASE STUDIES AND SHOWCASES

Links are from the official user-stories page (326 stories at fetch time), so each is a pointer, not a verified outcome. [COMMUNITY] [Phase 5 Section 1]

- Solo job-site app built via Telegram review (Reddit, Jun 18): https://www.reddit.com/r/hermesagent/comments/1u9fa2w/
- 28 cron jobs and a 3am "Dreaming" job: https://www.reddit.com/r/hermesagent/comments/1udesr1/
- €2,700/mo installing Hermes for French SMBs (self-reported): https://www.reddit.com/r/hermesagent/comments/1u4l0dj/
- 11 construction WhatsApp groups digest: https://www.reddit.com/r/hermesagent/comments/1uhyift/
- Local mail gatekeeper (no 2FA access for the agent): https://www.reddit.com/r/hermesagent/comments/1unuk20/
- DFIR analyst running three profiles: https://www.reddit.com/r/hermesagent/comments/1urri8w/
- Cron mode that costs zero tokens: https://www.reddit.com/r/hermesagent/comments/1uxwlyj/
- Gumroad's agent on a dedicated Mac: https://x.com/scotty529/status/2079686465513279615
- "12 Hermes instances every day" (Teknium): https://x.com/Teknium/status/2047869295686975529
- Token overhead measured (issue #4379): https://github.com/NousResearch/hermes-agent/issues/4379
- StackFund hackathon entry (Docker, egress proxy, skills): https://github.com/Silavater/stack_fund_agent
- Curated use-case list: https://github.com/aliaihub/awesome-hermes-usecases

---

# 5. CONFLICTS

| # | Conflict | Prior Says | Phase 5 Says | Resolution |
|---|----------|------------|--------------|------------|
| 1 | Use case count | Target ≥100 | 98 rows (PARTIAL) | Mark as PARTIAL; add 2 more from community sources if found |
| 2 | Source reliability | Most community | "Mostly community-reported and not independently verified" | Keep all tags as [C] unless [O] |
| 3 | Autonomous novel pipeline (row 42) | Not in prior | Official user-stories page | Mark [O] |
| 4 | Mixture-of-Agents (row 33) | Not in prior | Official feature v0.18.0 | Mark [O] |
| 5 | Keyless web tier (row 55) | Phase 3: built in v0.20.5 | Phase 5 confirms | Consistent |

---

# 6. GAPS

| # | Gap | Severity | Suggested Resolution |
|---|-----|----------|---------------------|
| 1 | Only 98 use cases vs 100 target | MAY BE STALE | Search Reddit r/hermesagent for 2 more verified cases |
| 2 | Most use cases community-reported, not verified | MAY BE STALE | Verify top 20 against official docs |
| 3 | Tool/skill specifics often generic | NICE TO KNOW | Map each use case to exact toolset/skill names from refs |
| 4 | Difficulty levels subjective | NICE TO KNOW | Define B/I/A criteria based on feature complexity |
| 5 | Case studies are pointers, not verified outcomes | NICE TO KNOW | Note as [COMMUNITY] pointers |

---

# 7. SOURCES

**Phase 5 (Fetched):**
- https://hermes-agent.nousresearch.com/docs/user-stories (fetched Oct 2, 2026)
- https://github.com/NousResearch/hermes-agent (README, fetched)
- https://github.com/aliaihub/awesome-hermes-usecases
- https://github.com/NousResearch/hermes-agent-self-evolution
- v0.20.5 release notes: https://github.com/NousResearch/hermes-agent/releases/tag/v2026.8.19

**Community / Third-Party:**
- Reddit r/hermesagent (multiple threads linked above)
- X/Twitter posts from @Teknium, @scotty529
- GitHub issues #4379, #17619
- StackFund agent: https://github.com/Silavater/stack_fund_agent

---

**FILE COMPLETE: hermes-forge/references/20-use-case-catalog.md**
Lines: ~600 | Includes: use case → playbook index, 98-row master catalog across 13 domains, top 20 VPS first steps ranked with justifications, 12 case study links from official user-stories page, conflicts, gaps, sources. PARTIAL: 98/100 target, mostly community-reported.