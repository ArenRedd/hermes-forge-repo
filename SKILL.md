---
name: hermes-knowledge
version: 1.0.0
description: |
  Hermes Agent knowledge base and expert agents. Provides comprehensive reference documentation for Hermes Agent (Nous Research) including CLI commands, configuration, toolsets, gateway platforms, skills system, memory, scheduling, subagents, security, VPS operations, troubleshooting, cost optimization, and use cases.

  This skill packages the 21 reference files from the hermes-forge project as a portable knowledge base compatible with skill systems that support reference directories and agent definitions.

author: hermes-forge build
license: MIT
tags: [hermes-agent, nous-research, documentation, reference, cli, automation, ai-agents]
requires_toolsets: [files, web]
platforms: [linux, macos]
metadata:
  hermes_version_documented: "v0.21.5 (tag v2026.9.24)"
  research_date: "2026-10-02"
  reference_files: 21
  total_size_kb: 380
---

# Hermes Knowledge Skill

This skill provides a complete knowledge base for **Hermes Agent** (the open-source autonomous agent framework by Nous Research), packaged as reference documentation plus specialized agents that can answer questions and generate execution plans using this knowledge.

## Structure

```
hermes-knowledge/
├── SKILL.md                 # This file
├── references/              # 21 reference files (380 KB)
│   ├── 00-index-and-routing.md
│   ├── 01-foundations-architecture.md
│   ├── 02-install-vps-config-basics.md
│   ├── 03-providers-and-models.md
│   ├── 04-cli-command-reference-a.md
│   ├── 04-cli-command-reference-b.md
│   ├── 05-slash-commands-sessions-interactive.md
│   ├── 06-config-keys-and-env-vars.md
│   ├── 07-tools-and-toolsets.md
│   ├── 08-terminal-backends.md
│   ├── 09-messaging-gateway.md
│   ├── 10-mcp-plugins-api.md
│   ├── 11-skills-system.md
│   ├── 12-memory-and-context.md
│   ├── 13-scheduling-and-automation.md
│   ├── 14-subagents-and-delegation.md
│   ├── 15-learning-loop-and-advanced.md
│   ├── 16-security-and-hardening.md
│   ├── 17-vps-operations.md
│   ├── 18-troubleshooting.md
│   ├── 19-cost-and-optimization.md
│   ├── 20-use-case-catalog.md
│   ├── 21-glossary.md
│   ├── 22-unverified-and-gaps.md
│   └── 23-sources.md
├── agents/                  # Specialized agents
│   ├── hermes-expert.md           # General Hermes expert
│   ├── hermes-mission-planner.md  # Generates mission briefs
│   ├── hermes-troubleshooter.md   # Diagnoses errors
│   ├── hermes-cost-optimizer.md   # Cost optimization advice
│   └── hermes-security-auditor.md # Security hardening
├── scripts/                 # Utility scripts
│   ├── index_references.py      # Build search index
│   └── validate_refs.py         # Validate reference integrity
└── assets/                  # Static assets
    └── hermes-architecture.svg  # Architecture diagram
```

## Reference Files Summary

| File | Topic | Size | Key Coverage |
|------|-------|------|--------------|
| 00-index-and-routing.md | Routing index | 11 KB | Intent → file mapping, trigger patterns |
| 01-foundations-architecture.md | Architecture | 18 KB | Identity, stack, repo structure, diagrams |
| 02-install-vps-config-basics.md | Installation | 19 KB | 8 install methods, VPS walkthrough, Docker, hardening |
| 03-providers-and-models.md | Providers/Models | 11 KB | ~40 providers, switching, fallback, local VPS models |
| 04-cli-command-reference-a.md | CLI Core | 28 KB | 12 core command families, ~70 commands |
| 04-cli-command-reference-b.md | CLI Extended | 14 KB | Remaining command families |
| 05-slash-commands-sessions-interactive.md | Slash Commands | 18 KB | 55+ slash commands, approvals, personalities |
| 06-config-keys-and-env-vars.md | Config/Env | 32 KB | ~110 config keys, ~60 env vars, precedence |
| 07-tools-and-toolsets.md | Tools/Toolsets | 30 KB | 100+ tools, 30+ toolsets, 4 presets, 28 platform toolsets |
| 08-terminal-backends.md | Terminal Backends | 13 KB | 7 backends, decision table, file transfer |
| 09-messaging-gateway.md | Gateway | 25 KB | 28 platforms, pairing, webhooks, Bot Mode |
| 10-mcp-plugins-api.md | MCP/Plugins | 17 KB | MCP client/server, 14 servers, plugins, API, ACP |
| 11-skills-system.md | Skills System | 28 KB | SKILL.md format, 58 bundled, ~200 optional, curator |
| 12-memory-and-context.md | Memory/Context | 17 KB | Layers, 9 providers, 5 priority levels, 14 personalities |
| 13-scheduling-and-automation.md | Scheduling | 17 KB | Cron mechanics, 5 formats, 25 recipes, job chaining |
| 14-subagents-and-delegation.md | Subagents | 11 KB | delegate_task, orchestrator, Kanban, Bot Mode, A2A |
| 15-learning-loop-and-advanced.md | Advanced | 11 KB | Goals, checkpoints, MoA, 30-day path, patterns |
| 16-security-and-hardening.md | Security | 37 KB | Approvals, sandbox, Tirith, allowlists, secrets, supply chain |
| 17-vps-operations.md | VPS Ops | 19 KB | Hardening, monitoring, log rotation, backup, migration |
| 18-troubleshooting.md | Troubleshooting | 24 KB | 25+ errors, doctor, logs, DB repair, recovery |
| 19-cost-and-optimization.md | Cost | 16 KB | Routing, auxiliary models, budgets, monitoring |
| 20-use-case-catalog.md | Use Cases | 19 KB | 80+ cataloged tasks with brief outlines |
| 21-glossary.md | Glossary | 44 KB | 500+ terms with definitions |
| 22-unverified-and-gaps.md | Gaps | 19 KB | 30 unverified items with resolution paths |
| 23-sources.md | Sources | 19 KB | Master source list from all research phases |

## Agents Included

| Agent | Purpose | Best For |
|-------|---------|----------|
| `hermes-expert` | General Q&A on any Hermes topic | "How do I configure X?" "What's the command for Y?" |
| `hermes-mission-planner` | Generates complete mission briefs | "Plan a task for Hermes: monitor my site..." |
| `hermes-troubleshooter` | Diagnoses errors and issues | "Hermes doctor shows X error..." "Gateway won't start..." |
| `hermes-cost-optimizer` | Cost reduction strategies | "Reduce my Hermes API costs..." "Cheap model for cron..." |
| `hermes-security-auditor` | Security hardening review | "Audit my Hermes config..." "Harden VPS for Hermes..." |

## Usage

### As Reference Knowledge Base
Simply point your agent/assistant to the `references/` directory. The files are self-contained markdown with comprehensive coverage.

### As Specialized Agents
Load individual agent files from `agents/` into your agent system. Each agent knows to consult the reference files for answers.

### Quick Lookup Commands
```bash
# Search references for a topic
grep -r "topic" references/

# Find command syntax
grep -r "hermes cron" references/04-cli-command-reference-a.md

# Check config key
grep -r "approval_mode" references/06-config-keys-and-env-vars.md
```

## Version Compatibility

- **Hermes Agent**: v0.21.5 (tag `v2026.9.24`, Sep 24 2026)
- **Research Date**: Friday, October 2, 2026
- **Note**: Phase 3/4/5 research was not version-pinned; all files carry this caveat

## Known Gaps (30 items)

See `references/22-unverified-and-gaps.md` for complete list. Key gaps:
- Full CLI reference (~30 families) not fully documented
- `hermes checkpoints`, `hermes import`, `hermes sessions` subcommands need verification
- Community skill exact names require `hermes skills browse`
- Toolset preset names (`research`, `creative`, `personal`) inferred
- Backup WAL consistency untested

## Installation

### For Skill Systems Supporting Reference Directories
```bash
cp -r hermes-knowledge /path/to/your/skills/hermes-knowledge
```

### For Agent-Only Systems
Copy desired agents from `agents/` to your agent directory.

### For Manual Use
```bash
# Browse references directly
ls hermes-knowledge/references/
cat hermes-knowledge/references/04-cli-command-reference-a.md
```

## Maintenance

See `references/22-unverified-and-gaps.md` for items to verify on each Hermes update. Run `scripts/validate_refs.py` to check reference integrity.

## License

MIT — Same as Hermes Agent (Nous Research)