---
title: Skills System Reference
source_phases: [Phase 4]
hermes_version_documented: v0.21.5 (tag v2026.9.24, Sep 24 2026) — Phase 4 version not pinned; docs don't state version
research_date: Friday, October 2, 2026
last_built_in: Chat 2
confidence_legend: OFFICIAL = official repo/docs/source; COMMUNITY = third-party; INFERRED = deduced; UNVERIFIED = needs checking
used_by_playbooks: [10-skill-authoring-and-memory-curation.md, 01-coding-and-dev.md, 02-devops-and-server-admin.md, 03-research-and-analysis.md, 04-content-and-social.md, 08-multi-agent-and-parallel.md]
---

# Skills System Reference

## WHEN TO READ THIS FILE
Use this file for everything about Hermes Agent skills: the exact SKILL.md frontmatter format, installation locations and precedence, invocation syntax (slash commands, bundles), all management commands (verbatim), hubs/registries with trust levels, **corrected bundled (58) and optional (200+) catalogs**, community sources, lifecycle/curator, and authoring best practices.

## TABLE OF CONTENTS
1. What a Skill Is (Progressive Disclosure)
2. SKILL.md File Format (Complete Frontmatter)
3. Minimal and Real Examples
4. Locations and Precedence
5. Invocation (Slash Commands, Bundles, Stacking)
6. Management Commands (Verbatim)
7. Hubs, Registries, Trust, and Scanning
8. Bundled Skills Catalog (58 skills, 12 categories) — CORRECTED
9. Optional Skills Catalog (~200 skills, 25 categories) — NEW
10. Community Sources
11. Self-Created Skills and Lifecycle
12. Curator Lifecycle
13. Background Review and Approval
14. Authoring Tutorial
15. Common Mistakes
16. Conflicts
17. Gaps
18. Sources

---

## 1. What a Skill Is (Progressive Disclosure)

**Definition** [OFFICIAL]: A skill is an on-demand knowledge document — the agent's "procedural memory." It is loaded only when relevant.

**Three-tier loading** [OFFICIAL]:
```
Level 0: skills_list()           → [{name, description, category}, ...]   (~3k tokens)
Level 1: skill_view(name)        → Full content + metadata       (varies)
Level 2: skill_view(name, path)  → Specific reference file       (varies)
```

**Token cost**: Index ~3k tokens. Full SKILL.md stays in context for session once loaded. Advisory linter warns on `oversized-body` past ~24k chars.

**Role vs other concepts** [OFFICIAL]:
| Concept | Role |
|---------|------|
| Skill | On-demand procedural knowledge (text) |
| Memory | Small durable facts always in context |
| Context file | Project instructions injected every conversation |
| Tool / toolset | Callable functions |
| Plugin / MCP | External integrations (not compared in skills pages) |

**Conditional activation** [OFFICIAL]:
- `requires_toolsets` / `requires_tools` — hidden when unavailable
- `fallback_for_toolsets` / `fallback_for_tools` — hidden when those ARE available
- `platforms` — hidden on other OSes

---

## 2. SKILL.md File Format (Complete Frontmatter)

```markdown
---
name: my-skill                          # REQUIRED: unique slug (kebab-case)
description: Brief description ≤60 chars  # REQUIRED: states trigger condition
version: 1.0.0                          # Optional: semver
platforms: [macos, linux]               # Optional: restrict to OS (macos, linux, windows)
metadata:
  hermes:
    tags: [python, automation]          # Optional: searchable tags
    category: devops                    # Optional: category for browsing
    fallback_for_toolsets: [web]        # Optional: hide when toolsets available
    requires_toolsets: [terminal]       # Optional: hide when toolsets unavailable
    fallback_for_tools: []              # Optional: per-tool
    requires_tools: []                  # Optional: per-tool
    config:                             # Optional: config.yaml settings
      - key: my.setting
        description: "What this controls"
        default: "value"
        prompt: "Prompt for setup"
    required_environment_variables:     # Optional: env vars needed
      - name: MY_API_KEY
        prompt: "Enter API key"
        help: "Get from https://..."
        required_for: "production"
author: "Your Name"                     # Optional: appears in tap example
---
# Skill Title (H1)
## When to Use
Trigger conditions for this skill.
## Procedure
1. Step one
2. Step two
## Pitfalls
- Known failure modes and fixes
## Verification
How to confirm it worked.
```

### Frontmatter Fields Reference

| Field | Required | Type | Behavior |
|-------|----------|------|----------|
| `name` | Yes | string | Unique slug; becomes slash command `/name` |
| `description` | Yes | string | ≤60 chars; states WHEN to use (trigger) |
| `version` | No | semver | Skill version |
| `platforms` | No | array | `macos`, `linux`, `windows` — hides on others |
| `metadata.hermes.tags` | No | array | Searchable tags |
| `metadata.hermes.category` | No | string | Category for browsing (see catalog categories) |
| `metadata.hermes.fallback_for_toolsets` | No | array | Hide skill WHEN these toolsets ARE available |
| `metadata.hermes.requires_toolsets` | No | array | Hide skill WHEN these toolsets are NOT available |
| `metadata.hermes.fallback_for_tools` | No | array | Per-tool fallback |
| `metadata.hermes.requires_tools` | No | array | Per-tool requirement |
| `metadata.hermes.config` | No | array | Config settings stored under `skills.config` in config.yaml |
| `metadata.hermes.required_environment_variables` | No | array | Env vars with `name`, `prompt`, `help`, `required_for` |
| `author` | No | string | Attribution |

---

## 3. Minimal and Real Examples

### 3.1 Minimal Example [OFFICIAL, from tap docs]

```markdown
---
name: deploy-runbook
description: Our deployment runbook — services, rollback, Slack channels
version: 1.0.0
author: My Org Platform Team
metadata:
  hermes:
    tags: [deployment, runbook, internal]
---
# Deploy Runbook
Step 1: ...
```

### 3.2 Full Example with Config and Env Vars

```markdown
---
name: github-pr-review
description: Review GitHub PRs with security, performance, and style checks
version: 2.1.0
platforms: [linux, macos]
metadata:
  hermes:
    tags: [github, code-review, security]
    category: software-development
    requires_toolsets: [github, terminal]
    config:
      - key: github_pr_review.severity_threshold
        description: "Minimum severity to report"
        default: "medium"
        prompt: "Severity threshold (low/medium/high/critical)"
      - key: github_pr_review.auto_approve
        description: "Auto-approve if no issues"
        default: false
        prompt: "Auto-approve clean PRs?"
    required_environment_variables:
      - name: GITHUB_TOKEN
        prompt: "GitHub Personal Access Token"
        help: "Create at https://github.com/settings/tokens (repo scope)"
        required_for: "all"
author: Platform Team
---
# GitHub PR Review
## When to Use
- Reviewing pull requests via `/github-pr-review <pr-url>`
- Automated review via webhook or cron
## Procedure
1. Load PR context with `github` toolset
2. Run security checks...
## Pitfalls
- Rate limits: set GITHUB_TOKEN in .env
- Large PRs: use pagination
## Verification
- Check PR for review comments
- Run `hermes skills check github-pr-review`
```

---

## 4. Locations and Precedence [OFFICIAL]

| Source | Path or Setting | Notes |
|--------|-----------------|-------|
| **Primary** | `~/.hermes/skills/` | Source of truth. Bundled skills seeded on install and every `hermes update`. |
| **External** | `skills.external_dirs` | Supports `~` and `${VAR}`. Missing paths skipped silently. Local copy wins on name clash. Writable external dirs can be modified by `skill_manage`. |
| **Project** | `<project-root>/.hermes/skills/` and `<project-root>/.agents/skills/` | **Highest precedence**. Needs `hermes skills trust`. Curator never touches them. |
| **Creation target** | `skills.create_dir` | Where new agent-created skills are written. |

**Config**:
```yaml
skills:
  external_dirs:
    - ~/.agents/skills
    - /home/shared/team-skills
    - ${SKILLS_REPO}/skills
  create_dir: /opt/brain/skills
  project_discovery: false      # turn project skills off entirely
  trusted_project_dirs: []      # written by `hermes skills trust`
```

**Order: project, then local (`~/.hermes/skills/`), then `external_dirs`.** Project skills tagged `[project]` in skill index.

**Directory layout**:
```
~/.hermes/skills/
├── mlops/axolotl/{SKILL.md, references/, templates/, scripts/, examples/, assets/}
├── .hub/{lock.json, quarantine/, audit.log}
└── .bundled_manifest
```

**Project skills scanning**: Hub scanner runs before entering index. `dangerous` rated skills are quarantined. Cron jobs inherit trust decision from their `workdir`.

---

## 5. Invocation [OFFICIAL]

### 5.1 Slash Commands (CLI and All Messaging Platforms)

```bash
/gif-search funny cats
/github-pr-workflow /test-driven-development fix issue #123 and open a PR   # stack up to 5
/excalidraw                       # name only: load it and let the agent ask
hermes chat --toolsets skills -q "What skills do you have?"
```

- Every installed skill becomes a slash command `/<skill-name>`
- On messaging platforms, `/<skill-name>` works but `/skills` browsing shown only for CLI in README table
- **Parsing stops at first token that isn't an installed skill**
- Stack up to 5 skills: `/skill-a /skill-b /skill-c task description`

### 5.2 Built-in Commands

```bash
/learn <source>        # Build skill from directory, URL, conversation, notes, book, PDF
/plan [request]        # Write plan under .hermes/plans/
/skills ...            # In-session skill management (see below)
/bundles               # Bundle management
```

### 5.3 `/learn` [OFFICIAL]

- Sources: directory, URL, current conversation, pasted notes, book, PDF
- Saves through `skill_manage`
- Large sources → lean `SKILL.md` + one distilled file per topic under `references/`

### 5.4 Skill Bundles [OFFICIAL]

A YAML alias for several skills:

```yaml
# ~/.hermes/skill-bundles/backend-dev.yaml
name: backend-dev
description: Backend feature work — review, test, PR workflow.
skills:
  - github-code-review
  - test-driven-development
  - github-pr-workflow
instruction: |
  Always start by writing failing tests, then implement.
```

```bash
hermes bundles create backend-dev --skill github-code-review --skill test-driven-development -d "desc"
hermes bundles list | show <name> | delete <name> | reload
/bundles
```

- Bundle wins over skill with same slug
- Missing skills are skipped
- Bundles don't invalidate prompt cache

---

## 6. Management Commands [OFFICIAL, VERBATIM]

```bash
# Browse and search
hermes skills browse
hermes skills browse --source official
hermes skills search kubernetes
hermes skills search react --source skills-sh
hermes skills search https://mintlify.com/docs --source well-known

# Inspect and install
hermes skills inspect openai/skills/k8s
hermes skills install openai/skills/k8s
hermes skills install official/security/1password
hermes skills install skills-sh/vercel-labs/json-render/json-render-react --force
hermes skills install well-known:https://mintlify.com/docs/.well-known/skills/mintlify
hermes skills install https://sharethis.chat/SKILL.md
hermes skills install https://example.com/SKILL.md --name my-skill
hermes skills install https://example.com/my-skill/SKILL.md --category productivity

# List and verify
hermes skills list --source hub
hermes skills check

# Update and audit
hermes skills update
hermes skills update react --force
hermes skills audit

# Reset and uninstall
hermes skills uninstall k8s
hermes skills reset google-workspace
hermes skills reset google-workspace --restore

# Publish and snapshots
hermes skills publish skills/my-skill --to github --repo owner/repo
hermes skills snapshot export setup.json

# Taps (external registries)
hermes skills tap add|remove|list  myorg/skills-repo

# Trust (for project skills)
hermes skills trust [path] | untrust

# Opt-out of bundled skills
hermes skills opt-out [--remove] | opt-in --sync

# Profile without skills
hermes profile create research --no-skills
```

### 6.1 In-Session Skill Commands

```bash
/skills browse|search|inspect|install|check|update|reset|list|tap …
/skills pending   /skills diff <id>   /skills approve <id|all>   /skills reject <id|all>   /skills approval on|off
```

### 6.2 Key Behaviors

- **Enable/disable per platform**: `skills.disabled` exists (curator doc mentions it). Exact per-platform syntax [UNVERIFIED].
- **GitHub rate limit**: Unauthenticated = 60 req/hr. Set `GITHUB_TOKEN` in `.env` for 5,000.
- **Local edits**: `hermes skills update` skips skills whose content no longer matches recorded hash. `--force` overwrites.
- **Bundled skills**: Changed copy = "user-modified" and skipped on sync. `hermes skills reset` re-baselines it.
- **Restore missing bundled skill**: `hermes skills reset <name> --restore`

---

## 7. Hubs, Registries, Trust, and Scanning [OFFICIAL]

| Source ID | What It Is | Trust Level |
|-----------|------------|-------------|
| `official` | `optional-skills/` in repo | `official`, built-in trust |
| `skills-sh` | Vercel's skills.sh directory | `community` |
| `well-known` | Sites serving `/.well-known/skills/index.json` | `community` |
| `url` | Direct `SKILL.md` URL + support files | `community` |
| `github` | Repo/path installs + taps. Default taps: `openai/skills`, `anthropics/skills`, `huggingface/skills`, `NVIDIA/skills` (signed), `garrytan/gstack`, `K-Dense-AI/scientific-agent-skills`, `synthetic-sciences/openscience` (~480 science) | `trusted` for major repos, `community` for rest |
| `clawhub` | clawhub.ai marketplace | `community` |
| `lobehub` | LobeHub agent catalog, converted | `community` |
| `browse-sh` | Browserbase's 200+ site-specific skills. IDs: `browse-sh/<hostname>/<task-id>` | `community` |

**Trust levels**: `builtin`, `official`, `trusted`, `community`.

**Scanner** [OFFICIAL]: Checks for data exfiltration, prompt injection, destructive commands, supply-chain signals. `--force` overrides non-dangerous policy blocks only. `dangerous` verdict **cannot be overridden**.

**Install records**: `skills/.hub/lock.json` stores source URL, content hash, scanner version, findings, timestamp.

**Advisory scans**: NVIDIA SkillEvaluator Tier 1 and SkillSpector. Optional, off with `skills.tier1_advisory: false`.

**Agent-created skills**: `skills.guard_agent_created` — separate content scanner.

**Hub index**: Browsable snapshot at `https://hermes-agent.nousresearch.com/docs/api/skills.json`.

**Pre-install audit**: `hermes skills inspect <id>` shows repo URL, installs, upstream audit status. Then `hermes skills install` without `--force`, read findings. `hermes skills audit` re-scans everything.

---

## 8. Bundled Skills Catalog (58 Skills, 12 Categories) — LIVE CATALOG [OFFICIAL]

**Source**: `https://hermes-agent.nousresearch.com/docs/reference/skills-catalog` (fetched live)

**Note**: `llms.txt` says "~90", community v0.20.6 list says 82. Catalog changed between releases. **Use 58 from live catalog.** Old names in docs examples (e.g., `github-pr-workflow`, `github-code-review`, `blogwatcher`, `duckduckgo-search`, `ocr-and-documents`) are **deprecated/consolidated**.

| Category | Skills (Purpose) |
|----------|------------------|
| **apple** (macOS only) | `apple-notes` (memo CLI), `apple-reminders` (remindctl), `findmy` (FindMy.app), `imessage` (imsg CLI) |
| **autonomous-ai-agents** | `claude-code` (delegate to Claude Code), `codex` (delegate to Codex), `opencode` (delegate to OpenCode), `computer-use` (desktop driving), `hermes-agent` (use, configure, orchestrate Hermes) |
| **creative** | `architecture-diagram`, `ascii-video`, `baoyu-infographic`, `claude-design`, `design-md`, `humanizer`, `manim-video`, `p5js`, `popular-web-designs` (54 design systems), `songwriting-and-ai-music` |
| **devops** | `sdlc-review` (Kanban handoff review) |
| **email** | `email-inbox-triage`, `himalaya` (IMAP/SMTP CLI) |
| **media** | `gif-search` (Tenor; needs `TENOR_API_KEY`), `songsee`, `youtube-content` |
| **note-taking** | `obsidian` |
| **productivity** | `airtable`, `box`, `document-to-action-items`, `docx`, `google-workspace` (gws CLI or Python), `maps` (OpenStreetMap/OSRM), `meeting-action-items`, `notion`, `pdf`, `powerpoint`, `product-price-monitor`, `teams-meeting-pipeline`, `weekly-review-planning`, `xlsx` |
| **research** | `arxiv`, `competitor-news-monitor`, `grounded-citations`, `llm-wiki` |
| **social-media** | `xurl` (X/Twitter CLI) |
| **software-development** | `codebase-inspection`, `dogfood`, `github`, `hermes-agent-skill-authoring`, `inspecting-hermes-desktop-dom`, `node-inspect-debugger`, `python-debugpy`, `requesting-code-review`, `simplify-code`, `spike`, `systematic-debugging`, `test-driven-development` |
| **web** | `blocked-page-recovery` |

**Dependencies and keys**: Not captured per skill beyond `TENOR_API_KEY` for `gif-search`. Each skill's detail page documents its setup.

**Skill-authoring helper**: `software-development/hermes-agent-skill-authoring` covers in-repo `SKILL.md` frontmatter and structure.

---

## 9. Optional Skills Catalog (~200 Skills, 25 Categories) — LIVE CATALOG [OFFICIAL]

**Source**: `https://hermes-agent.nousresearch.com/docs/reference/optional-skills-catalog`

**Install**: `hermes skills install official/<category>/<skill>`

**Review security-sensitive entries before enabling**: `godmode` (LLM jailbreaks), `obliteratus` (refusal removal), `web-pentest`, `unbroker`, `sherlock`, `osint-investigation` can have real-world consequences. `web-pentest` described as for authorized testing only.

| Category | Skills |
|----------|--------|
| **autonomous-ai-agents** | `antigravity-cli`, `blackbox`, `grok`, `honcho`, `openhands` |
| **blockchain** | `evm`, `hyperliquid`, `solana` |
| **communication** | `one-three-one-rule` |
| **creative** | `audiocraft-audio-generation`, `baoyu-article-illustrator`, `baoyu-comic`, `concept-diagrams`, `creative-ideation`, `draw-your-font`, `heartmula`, `hyperframes`, `kanban-video-orchestrator`, `meme-generation`, `pixel-art`, `simple-english`, `social-media-content-calendar`, `tldraw-offline`, `unreal-mcp` |
| **data-science** | `jupyter-notebook` |
| **devops** | `actual-setup`, `docker-management`, `hermes-s6-container-supervision`, `inference-sh-cli`, `pinggy-tunnel`, `setup-wizard-generator`, `watchers` (RSS/JSON/GitHub polling with dedup) |
| **dogfood** | `adversarial-ux-test` |
| **email** | `agentmail` |
| **finance** | `3-statement-model`, `comps-analysis`, `dcf-model`, `excel-author`, `lbo-model`, `merger-model`, `polymarket`, `pptx-author`, `stocks` |
| **gaming** | `minecraft-modpack-server`, `pokemon-player` |
| **health** | `fitness-nutrition`, `neuroskill-bci` |
| **mcp** | `fastmcp`, `mcp-oauth-remote-gateway`, `mcporter` |
| **migration** | `openclaw-migration` |
| **mlops** | `accelerate`, `axolotl`, `chroma`, `clip`, `dspy`, `faiss`, `flash-attention`, `guidance`, `huggingface-tokenizers`, `instructor`, `lambda-labs`, `llava`, `modal`, `nemo-curator`, `obliteratus`, `outlines`, `peft`, `pinecone`, `pytorch-fsdp`, `pytorch-lightning`, `qdrant`, `saelens`, `segment-anything-model`, `simpo`, `slime`, `stable-diffusion`, `tensorrt-llm`, `torchtitan`, `trl-fine-tuning`, `unsloth`, `whisper` |
| **payments** | `mpp-agent`, `stripe-link-cli`, `stripe-projects` |
| **productivity** | `canvas`, `decision-questionnaire`, `here-now`, `memento-flashcards`, `shop`, `shopify`, `siyuan`, `telephony` |
| **research** | `bioinformatics`, `darwinian-evolver`, `domain-intel`, `drug-discovery`, `duckduckgo-search`, `gitnexus-explorer`, `osint-investigation`, `parallel-cli`, `pinecone-research`, `qmd`, `scrapling`, `searxng-search` |
| **security** | `1password`, `godmode`, `oss-forensics`, `sherlock`, `unbroker`, `web-pentest` |
| **software-development** | `code-wiki`, `grill-me`, `rest-graphql-debug`, `subagent-driven-development` |
| **web-development** | `cloudflare-temporary-deploy`, `page-agent`, `publish-site` |
| **yuanbao** | `yuanbao` |

---

## 10. Community Sources [COMMUNITY, PARTLY VERIFIED]

| Source | What It Is |
|--------|------------|
| `github.com/ZeroPointRepo/awesome-hermes-skills` | Curated list: 82 built-in, 117 optional, 169 community items, labelled v0.20.6 |
| `github.com/0xarkstar/awesome-hermes-agent` | Curated list. Points to `black-forest-labs/skills` (FLUX), `chainlink-agent-skills`, `wondelai/skills`, `hermes-agent-docker`, `nix-hermes-agent` |
| `github.com/itgoyo/hermes-skills` | 310+ skills, last seen ~163 days ago (possibly stale) |
| `github.com/TechNickAI/hermes-config` | Starter kit with SOUL presets, skills, `cortex` memory plugin |
| `github.com/aliaihub/awesome-hermes-usecases` | Use-case catalog including Fly.io and headless-VPS deployment patterns |
| `browse.sh` (`browse-sh` source) | 200+ site-specific skills. Example: `hermes skills install browse-sh/airbnb.com/search-listings-ddgioa` |
| `K-Dense-AI/scientific-agent-skills` + `synthetic-sciences/openscience` | Default taps with ~480 science skills. **Check licenses; some GPL** |

**Plugins** (install with `hermes plugins install <name>`):
- `hookdeck/hermes-hookdeck`
- `pocket-watch`
- `custodian` (registers 3 recurring cron jobs on `/custodian init`)
- `identity`

**Verify**: Install counts, quality, safety of any individual community skill. Run `hermes skills inspect <id>` and `hermes skills audit` first.

---

## 11. Self-Created Skills and Lifecycle [OFFICIAL]

### 11.1 Triggers
System prompt asks agent to save a skill when:
- Worked out a multi-step workflow worth repeating
- Found a working path after errors
- Was corrected by you
- Third-party doc (`mudrii/hermes-agent-docs`, v0.2.0, [COMMUNITY]): "after complex tasks (5+ tool calls)" — **not confirmed in current official page**

### 11.2 `skill_manage` Actions

| Action | Params |
|--------|--------|
| `create` | `name`, `content`, optional `category` |
| `patch` | `name`, `old_string`, `new_string` (preferred) |
| `patch` with `content` | Full rewrite (`edit` is legacy alias) |
| `delete` | `name` |
| `write_file` | `name`, `file_path`, `file_content` |
| `remove_file` | `name`, `file_path` |

### 11.3 Background Review
- Fork runs after a turn, can save memory or patch skills
- Curator doc: runs ~every 10 agent turns
- Tuning: `memory.nudge_interval`, `skills.creation_nudge_interval` (defaults not verified)

```yaml
auxiliary:
  background_review:
    enabled: true
    provider: openrouter
    model: google/gemini-3-flash-preview   # auto = main model
    max_input_tokens: 48000
    defer: auto
display:
  memory_notifications: on    # off | on | verbose
```

`/refine` runs review manually. `/review` is different: reviews work product with subagent.

### 11.4 Approve or Block

```yaml
skills:
  write_approval: true
```
Staged writes live in `~/.hermes/pending/skills/`.

```bash
/skills pending   /skills diff <id>   /skills approve <id|all>   /skills reject <id|all>   /skills approval on|off
```

---

## 12. Curator Lifecycle [OFFICIAL]

**Config**:
```yaml
curator:
  enabled: true
  interval_hours: 168
  min_idle_hours: 2
  stale_after_days: 14
  archive_after_days: 30
  consolidate: false
  prune_builtins: false
  archive_ttl_days: 0
  backup: {enabled: true, keep: 2}
auxiliary:
  curator: {provider: openrouter, model: google/gemini-3-flash-preview, timeout: 600}
```

**Commands**:
```bash
hermes curator status | run [--dry-run|--consolidate|--background] | pause | resume
hermes curator pin|unpin|adopt|restore|archive <skill>
hermes curator list-unmanaged | list-archived | prune [--days N] | purge [--days N] [--dry-run]
hermes curator backup [--reason "..."] | rollback [--list|--id <ts>|-y|<entry-id>] | ledger [--skill X --limit N]
```

**Behavior**:
- First run deferred by one full interval. Use `--dry-run` to preview.
- Only skills marked `agent-created` are curated (background review fork sets this mark).
- Skills from `/learn` or foreground = `created_by: learn` — left alone.
- Hand-written, bundled, hub skills = left alone.
- **Docs discrepancy**: Config says stale at 14 days, archive at 30. Prose says stale at 30, archive at 90. **Trust config keys.**
- Files: `~/.hermes/skills/.usage.json`, `.archive/`, `.curator_ledger.jsonl`, reports in `~/.hermes/logs/curator/<ts>/REPORT.md`.
- Curator protects skills named in any cron job's `skills:` list.

---

## 13. Background Review and Approval [OFFICIAL]

**Config**:
```yaml
auxiliary:
  background_review:
    enabled: true
    provider: openrouter
    model: google/gemini-3-flash-preview
    max_input_tokens: 48000
    defer: auto
display:
  memory_notifications: on
skills:
  write_approval: false
memory:
  write_approval: false
```

**Linter rules** (warn only, never block):
- `incident-log-shape` — skills logging incidents instead of rules
- `references-sprawl` — more than 60 reference files
- `oversized-body` — body past ~24k chars

---

## 14. Authoring Tutorial [INFERRED from OFFICIAL]

1. Make directory: `~/.hermes/skills/<category>/<name>/SKILL.md`
2. Write `name` and short `description` (≤60 chars, states trigger)
3. Use sections: `## When to Use`, `## Procedure`, `## Pitfalls`, `## Verification`
4. Move bulky material into `references/`, `scripts/`, load with `skill_view(name, path)`
5. Declare `required_environment_variables`, `requires_toolsets`, `platforms`
6. Test with `/<name> task`, then `hermes skills list`

**Common mistakes**:
- Restating `AGENTS.md`
- Logging incidents (PR numbers, dates) instead of rules
- Creating hundreds of reference files
- Writing bodies over ~24k characters

---

## 15. Conflicts

| # | Conflict | Resolution |
|---|----------|------------|
| 1 | Bundled count: `llms.txt` says ~90, live catalog = 58, community v0.20.6 = 82 | Use live catalog (58). Note discrepancies. |
| 2 | Deprecated bundled skill names in docs examples (`github-pr-workflow`, `github-code-review`, `blogwatcher`, `duckduckgo-search`, `ocr-and-documents`) | Live catalog has consolidated `github` skill, no `blogwatcher`. `duckduckgo-search` moved to optional. Mark old names deprecated. |
| 3 | `skills.disabled` per-platform syntax | [UNVERIFIED] — curator doc mentions it exists |
| 4 | Curator stale/archive days discrepancy (config vs prose) | Trust config keys (14/30). |
| 5 | Background review nudge interval defaults | [UNVERIFIED] — curator doc says ~every 10 turns |
| 6 | `memory.nudge_interval` and `skills.creation_nudge_interval` defaults | [UNVERIFIED] |
| 7 | Complete bundled skill catalog with all 58 detail pages | Not fetched — only index page |
| 8 | 40 best community skills list | Not completed — partial only |

---

## 16. Gaps

1. Exact per-skill dependencies and env vars (beyond `TENOR_API_KEY`)
2. `skills.disabled` per-platform syntax
3. `memory.nudge_interval` and `skills.creation_nudge_interval` defaults
4. Full 40 community skills with install lines
5. `hermes skills config` command (not confirmed)
6. Complete example skill copied from repo
7. agentskills.io compatibility matrix verification
8. Import from Claude Code / Codex details (doc page exists, not read)

---

## 17. Sources

- https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
- https://hermes-agent.nousresearch.com/docs/user-guide/features/curator
- https://hermes-agent.nousresearch.com/docs/reference/skills-catalog
- https://hermes-agent.nousresearch.com/docs/reference/optional-skills-catalog
- https://hermes-agent.nousresearch.com/docs/llms.txt
- https://github.com/NousResearch/hermes-agent
- https://github.com/mudrii/hermes-agent-docs [COMMUNITY, v0.2.0]
- Phase 4 Sections 1, 7

---

**FILE COMPLETE: references/11-skills-system.md** — Complete frontmatter, 58 bundled skills (corrected), ~200 optional skills, all management commands verbatim, hubs/trust, lifecycle, curator, authoring.