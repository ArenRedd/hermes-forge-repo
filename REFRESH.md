---
title: Refresh Procedure — Keeping hermes-forge Current
source_phases: [Phase 1, Phase 2, Phase 3, Phase 4, Phase 5]
hermes_version_documented: v0.21.5 (tag v2026.9.24, Sep 24 2026)
last_refresh: 2026-10-02
next_refresh_due: 2026-12-02
---

# REFRESH.md — Updating hermes-forge

This document describes how to update the `hermes-forge` skill when Hermes Agent releases new versions, when new research is available, or when the skill itself needs improvement.

---

## 1. TRIGGERS FOR A REFRESH

| Trigger | Action Required | Priority |
|---------|-----------------|----------|
| New Hermes tag (e.g., v2026.11.15) | Full audit against changelog; update version in all files | HIGH |
| New official skill released | Add to 11-skills-system.md, update playbooks | MEDIUM |
| New provider/model added | Update 03-providers-and-models.md, 19-cost-and-optimization.md | MEDIUM |
| New CLI command/subcommand | Update 04-cli-command-reference-a/b.md, SKILL.md routing | HIGH |
| New config key/env var | Update 06-config-keys-and-env-vars.md, SKILL.md | HIGH |
| New platform gateway support | Update 09-messaging-gateway.md, playbooks 06/09 | MEDIUM |
| Security advisory | Update 16-security-and-hardening.md immediately | CRITICAL |
| User reports gap/error in playbook | Fix playbook, update unverified items | HIGH |
| Community skill becomes bundled | Move from COMMUNITY to OFFICIAL in tables | MEDIUM |

---

## 2. REFRESH WORKFLOW (STEP BY STEP)

### Step 1: Collect Changes
```bash
# On updated Hermes instance
hermes --version
hermes update --check
hermes doctor
# Check GitHub releases: https://github.com/NousResearch/hermes-agent/releases
# Check docs: https://hermes-agent.nousresearch.com/docs
```

### Step 2: Update Version Markers
Edit these files to reflect new version:
- `SKILL.md` frontmatter: `hermes_version: "v0.xx.x"`
- All reference files: `hermes_version_documented:` frontmatter
- `00-index-and-routing.md`: version note at top
- `23-sources.md`: add new source entries

### Step 3: Audit Each Reference File
For each reference file (01-21), check:
1. **Commands**: Run `hermes <command> --help` for any documented command; update flags
2. **Config keys**: Check `hermes config schema` or docs for new/removed keys
3. **Toolsets**: Run `hermes tools preset list` and `hermes tools list`
4. **Skills**: Run `hermes skills browse` for new bundled/optional skills
5. **Gateway platforms**: Check `hermes gateway setup` for new platforms
5. **Terminal backends**: Check for new backends
6. **MCP/Plugins**: Check `hermes mcp list` and plugin registry
7. **SLASH commands**: Check `hermes -z "/help"` or interactive `/help`
8. **Cron formats**: Verify `hermes cron create --help` for new schedule types
9. **Profiles**: Check `hermes profile --help`
10. **Memory/context**: Check for new features

### Step 4: Update Playbooks
For each playbook (01-11):
1. Verify all commands still work
2. Update toolset/skill names if changed
3. Check unverified items — promote to OFFICIAL if confirmed
4. Add new recipes for new features

### Step 5: Update Templates
- `templates/mission-brief.md`: Check section alignment with new features
- `templates/prompt-patterns.md`: Add patterns for new capabilities
- `templates/clarifying-questions.md`: Add questions for new domains

### Step 6: Rebuild Staging Files
```bash
# Rebuild glossary from all reference files
# Rebuild recipes-staging.md from playbooks
# Rebuild security-staging.md from 16-security-and-hardening.md
# Rebuild coverage-matrix.md from all phases
```

### Step 7: Run Full Audit
Run the audit checklist (see AUDIT.md or self-audit section below).

### Step 8: Update SKILL.md
- Bump version: `v1.0.0-chat2` → `v1.1.0` (minor) or `v2.0.0` (major)
- Update routing if new modes/domains added
- Update anti-hallucination contract if new identifiers added
- Update TO CONFIRM block if any resolved

### Step 9: Test the Skill
Run simulated test suite (see tests/sample-tasks.md).

### Step 10: Package and Distribute
```bash
# Create distribution package
tar -czf hermes-forge-vX.Y.Z.tar.gz hermes-forge/
# Or publish to skills hub if configured
hermes skill publish hermes-forge  # if supported
```

---

## 3. VERSIONING POLICY

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Bug fix in playbook/recipe | PATCH (vX.Y.Z+1) | v1.0.0 → v1.0.1 |
| New playbook/recipe added | MINOR (vX.Y+1.0) | v1.0.0 → v1.1.0 |
| New reference file added | MINOR | v1.0.0 → v1.1.0 |
| CLI command added/changed | MINOR | v1.0.0 → v1.1.0 |
| Config key added/changed | MINOR | v1.0.0 → v1.1.0 |
| Breaking change (routing, templates) | MAJOR (vX+1.0.0) | v1.0.0 → v2.0.0 |
| New Hermes major version | MAJOR | v1.0.0 → v2.0.0 |

---

## 4. SOURCE TRACKING

| Source | Location | How to Check for Updates |
|--------|----------|-------------------------|
| Hermes docs | https://hermes-agent.nousresearch.com/docs | Check "Last updated" footer, RSS if available |
| GitHub releases | https://github.com/NousResearch/hermes-agent/releases | Watch repo for releases |
| Discord/Community | Nous Research Discord #hermes-agent | Monitor announcements |
| Changelog | https://github.com/NousResearch/hermes-agent/blob/main/CHANGELOG.md | Check on release |
| Skills hub | `hermes skills browse` | Run weekly |
| This skill's conflict log | `_build/conflict-log.md` | Review on each refresh |

---

## 5. SELF-AUDIT CHECKLIST (RUN AFTER EVERY REFRESH)

```
[ ] 1. All 21 reference files have correct version in frontmatter
[ ] 2. All CLI commands in 04a/04b verified against `hermes --help` output
[ ] 3. All config keys in 06 verified against `hermes config schema`
[ ] 4. All toolsets in 07 verified against `hermes tools preset list`
[ ] 4. All skills in 11 verified against `hermes skills browse`
[ ] 5. All gateway platforms in 09 verified against `hermes gateway setup`
[ ] 6. All terminal backends in 08 verified against `hermes setup`
[ ] 7. All SLASH commands in 05 verified against interactive `/help`
[ ] 8. All cron formats in 13 verified against `hermes cron create --help`
[ ] 9. All playbooks (01-11) have working commands, no dead references
[ ] 10. Templates (mission-brief, prompt-patterns, clarifying-questions) complete
[ ] 11. No [VERIFY] placeholders remain unresolved (move to 22-unverified-and-gaps.md)
[ ] 12. Conflict log updated with any new contradictions
[ ] 13. Glossary (21) has entries for all new terms
[ ] 14. Coverage matrix (_build/coverage-matrix.md) maps all phases to files
[ ] 15. SKILL.md version bumped, routing current, contracts current
[ ] 16. Simulated test suite passes (tests/sample-tasks.md)
[ ] 17. Package builds without errors
```

---

## 6. KNOWN GAPS REQUIRING MANUAL CHECK

These items cannot be fully automated and must be verified manually each refresh:

| Gap | Why Manual | Where to Check |
|-----|------------|----------------|
| New community skills becoming bundled | No API for skill registry status | `hermes skills browse` + Discord |
| Provider model list changes | Provider APIs change without notice | Provider dashboards |
| Gateway platform OAuth flows | Platform-specific, undocumented | Platform developer docs |
| Terminal backend capabilities | New backends added silently | `hermes setup` interactive |
| Cost optimization features | Auxiliary model routing evolves | `hermes config schema`, docs |
| MCP server ecosystem | Explodes weekly | MCP registry, npm search |
| A2A protocol adoption | Emerging standard | Agent-to-Agent spec |

---

## 7. ROLLBACK PROCEDURE

If a refresh introduces regressions:
```bash
# 1. Revert to previous skill version
git checkout v1.0.0 -- hermes-forge/  # or extract from backup tar

# 2. Verify rollback works
hermes skill install ./hermes-forge
/skill hermes-forge "test task"

# 3. Document regression in conflict-log.md
```

---

## 8. AUTOMATION IDEAS (FUTURE)

- GitHub Action: on Hermes release → run audit → create PR
- Cron job: weekly `hermes skills browse` diff → alert on new bundled skills
- Webhook: docs change → trigger refresh workflow
- Test runner: automated simulated test suite on PR

---

**FILE COMPLETE: hermes-forge/REFRESH.md**
Lines: ~200 | Covers: triggers, 10-step workflow, versioning policy, source tracking, self-audit checklist, known gaps, rollback procedure, automation ideas.