# Hermes Knowledge Skill

> **Comprehensive Hermes Agent (Nous Research) knowledge base packaged as a portable skill with specialized agents.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.txt)
[![Hermes Version](https://img.shields.io/badge/Hermes-v0.21.5-blue.svg)](https://github.com/NousResearch/hermes-agent/releases/tag/v2026.9.24)
[![Research Date](https://img.shields.io/badge/Research-2026.10.02-green.svg)]()
[![Reference Files](https://img.shields.io/badge/References-21-orange.svg)]()

---

## 🎯 Overview

This skill packages **21 reference files** (380 KB) covering every aspect of **Hermes Agent** — the open-source autonomous agent framework by Nous Research — into a portable format compatible with skill systems that support agent definitions and reference directories.

### What's Included

| Component | Count | Description |
|-----------|-------|-------------|
| **Reference Files** | 21 | Complete documentation: CLI, config, gateway, skills, memory, scheduling, security, troubleshooting, cost optimization |
| **Specialized Agents** | 5 | Expert agents for Q&A, mission planning, troubleshooting, cost optimization, security auditing |
| **Manifest** | 1 | Machine-readable skill definition (`manifest.json`) |
| **Documentation** | 3 | Coverage matrix, build report, refresh procedure |

---

## 📚 Reference Files (21)

| # | File | Topic | Size |
|---|------|-------|------|
| 00 | `index-and-routing.md` | Intent → file mapping, trigger patterns | 11 KB |
| 01 | `foundations-architecture.md` | Identity, architecture, repo structure | 18 KB |
| 02 | `install-vps-config-basics.md` | 8 install methods, VPS walkthrough, Docker | 19 KB |
| 03 | `providers-and-models.md` | ~40 providers, switching, fallback, local models | 11 KB |
| 04a | `cli-command-reference-a.md` | 12 core command families, ~70 commands | 28 KB |
| 04b | `cli-command-reference-b.md` | Remaining CLI families | 14 KB |
| 05 | `slash-commands-sessions-interactive.md` | 55+ slash commands, approvals, personalities | 18 KB |
| 06 | `config-keys-and-env-vars.md` | ~110 config keys, ~60 env vars, precedence | 32 KB |
| 07 | `tools-and-toolsets.md` | 100+ tools, 30+ toolsets, 4 presets, 28 platform toolsets | 30 KB |
| 08 | `terminal-backends.md` | 7 backends, decision table, file transfer | 13 KB |
| 09 | `messaging-gateway.md` | 28 platforms, pairing, allowlists, webhooks, Bot Mode | 25 KB |
| 10 | `mcp-plugins-api.md` | MCP client/server, 14 servers, plugins, API, ACP | 17 KB |
| 11 | `skills-system.md` | SKILL.md format, 58 bundled, ~200 optional, curator | 28 KB |
| 12 | `memory-and-context.md` | Memory layers, 9 providers, 5 priority levels, 14 personalities | 17 KB |
| 13 | `scheduling-and-automation.md` | Cron mechanics, 5 formats, 25 recipes, job chaining | 17 KB |
| 14 | `subagents-and-delegation.md` | delegate_task, orchestrator, Kanban, Bot Mode, A2A | 11 KB |
| 15 | `learning-loop-and-advanced.md` | Goals, checkpoints, MoA, 30-day path, 30 patterns | 11 KB |
| 16 | `security-and-hardening.md` | Approvals, sandbox, Tirith, allowlists, secrets, supply chain | 37 KB |
| 17 | `vps-operations.md` | Hardening, monitoring, log rotation, backup, migration | 19 KB |
| 18 | `troubleshooting.md` | 25+ errors, doctor, logs, DB repair, recovery | 24 KB |
| 19 | `cost-and-optimization.md` | Cost levers, routing, auxiliary models, budgets | 16 KB |
| 20 | `use-case-catalog.md` | 80+ cataloged tasks with brief outlines | 19 KB |
| 21 | `glossary.md` | 500+ terms with definitions | 44 KB |
| 22 | `unverified-and-gaps.md` | 30 unverified items with resolution paths | 19 KB |
| 23 | `sources.md` | Master source list from all research phases | 19 KB |

---

## 🤖 Specialized Agents (5)

| Agent | Purpose | Best For |
|-------|---------|----------|
| `hermes-expert` | General Q&A on any Hermes topic | "How do I configure X?" "What's the command for Y?" |
| `hermes-mission-planner` | Generates complete mission briefs | "Plan a Hermes task: monitor my site..." |
| `hermes-troubleshooter` | Diagnoses errors and issues | "Hermes doctor shows X error..." |
| `hermes-cost-optimizer` | Cost reduction strategies | "Reduce my Hermes API costs..." |
| `hermes-security-auditor` | Security hardening review | "Audit my Hermes config..." |

Each agent references the relevant documentation files and follows anti-hallucination rules (verbatim identifiers only, flag unverified items).

---

## 🚀 Installation

### For Skill Systems with Agent Support

```bash
# Clone or copy the skill
git clone https://github.com/your-org/hermes-forge-repo.git ~/.config/your-skill-system/skills/hermes-knowledge

# Or copy locally
cp -r hermes-forge-repo ~/.config/your-skill-system/skills/hermes-knowledge
```

### For Reference-Only Use

```bash
cp -r hermes-forge-repo/references ~/knowledge/hermes-docs
```

### For Manual Use

```bash
# Browse references directly
cat hermes-forge-repo/references/04-cli-command-reference-a.md

# Search across all references
grep -r "hermes cron" hermes-forge-repo/references/
```

---

## 📖 Usage Examples

### Ask the Expert
```
User: "How do I set up a Telegram gateway for Hermes?"
Agent (hermes-expert): Consults references/09-messaging-gateway.md §3-5
→ Provides exact pairing commands, allowlist config, delivery format
```

### Plan a Mission
```
User: "Plan a Hermes task: monitor my website every 5 minutes, alert on Telegram if down"
Agent (hermes-mission-planner): Produces full 18-section mission brief with:
→ Skills, commands, toolsets, config, schedule, delegation, delivery, verification
```

### Troubleshoot an Error
```
User: "Hermes gateway won't start, shows 409 Conflict"
Agent (hermes-troubleshooter): Diagnoses from references/18-troubleshooting.md
→ Root cause: duplicate poller → Fix: hermes gateway stop on old instance
```

### Optimize Costs
```
User: "My Hermes cron jobs are expensive. How to reduce?"
Agent (hermes-cost-optimizer): Recommends from references/19-cost-and-optimization.md
→ Switch to Flash models, use --script --no-agent for checks, enable auxiliary compression
```

### Security Audit
```
User: "Audit my Hermes production deployment"
Agent (hermes-security-auditor): Runs checklist from references/16-security-and-hardening.md
→ Approval modes, sandbox, allowlists, secrets, network egress, VPS hardening
```

---

## 📋 Version Compatibility

| Component | Version |
|-----------|---------|
| **Hermes Agent** | v0.21.5 (tag `v2026.9.24`, Sep 24 2026) |
| **Research Date** | Friday, October 2, 2026 |
| **Skill Version** | 1.0.0 |

⚠️ **Note**: Phase 3/4/5 research was not version-pinned; all files carry a version caveat. See `REFRESH.md` for update procedure.

---

## 🔍 Known Gaps (30 items)

See `references/22-unverified-and-gaps.md` for complete list. Key gaps:

- Full CLI reference (~30 families) not fully documented
- `hermes checkpoints`, `hermes import`, `hermes sessions` subcommands need verification
- Community skill exact names require `hermes skills browse`
- Toolset preset names (`research`, `creative`, `personal`) inferred
- Backup WAL consistency untested

---

## 🔄 Maintenance

### Refresh Procedure
See `REFRESH.md` for the complete 10-step workflow:
1. Collect changes from Hermes releases
2. Update version markers across all files
3. Audit each reference file against live `hermes --help` output
4. Update playbooks and agents
5. Rebuild staging files (glossary, recipes, coverage matrix)
6. Run full audit checklist
7. Bump skill version
8. Test with simulated task suite
9. Package and distribute

### Validation Scripts
```bash
# Validate reference integrity
python3 scripts/validate_refs.py

# Build search index
python3 scripts/index_references.py
```

---

## 📁 Repository Structure

```
hermes-forge-repo/
├── manifest.json              # Machine-readable skill definition
├── SKILL.md                   # Human-readable skill description
├── README.md                  # This file
├── LICENSE.txt                # MIT License
├── REFRESH.md                 # Update procedure
├── agents/                    # 5 specialized agent definitions
│   ├── hermes-expert.md
│   ├── hermes-mission-planner.md
│   ├── hermes-troubleshooter.md
│   ├── hermes-cost-optimizer.md
│   └── hermes-security-auditor.md
├── references/                # 21 reference files
│   ├── 00-index-and-routing.md through 23-sources.md
├── docs/
│   ├── coverage-matrix.md     # Phase → file bidirectional map
│   └── BUILD-REPORT.md        # Final build report
├── examples/
│   └── sample-tasks.md        # 25 test tasks with expected outputs
└── scripts/
    ├── index_references.py    # Build search index
    └── validate_refs.py       # Validate reference integrity
```

---

## 🤝 Contributing

1. **Source Fidelity**: All content must come from official Hermes sources (docs, repo, CLI help). No invented commands/config.
2. **Verbatim Identifiers**: Every command, flag, key, tool, skill, path must appear exactly as in source.
3. **Flag Unverified**: Use `⚠ UNVERIFIED` or `[VERIFY: ...]` for unconfirmed items.
4. **Update Gaps**: Add new unverified items to `references/22-unverified-and-gaps.md`.
5. **Run Validation**: `python3 scripts/validate_refs.py` must pass.

---

## 📄 License

MIT License — Same as Hermes Agent (Nous Research).

See [LICENSE.txt](LICENSE.txt) for full text.

---

## 🔗 Related

- **Hermes Agent**: https://github.com/NousResearch/hermes-agent
- **Hermes Docs**: https://hermes-agent.nousresearch.com/docs
- **Original hermes-forge Project**: 3-chat build producing 51 files (~18K lines)

---

## 🙏 Acknowledgments

- **Nous Research** for Hermes Agent
- **Anand's IT Studio** (Anandram Mohan) for sponsoring the research
- Built as part of the `hermes-forge` 3-chat construction project