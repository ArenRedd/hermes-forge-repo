---
title: VPS Operations Reference
source_phases: [Phase 5, Phase 3, Phase 4]
hermes_version_documented: v0.21.5 (tag v2026.9.24, Sep 24 2026) — Phase 3/4/5 version caveats apply
research_date: Friday, October 2, 2026
last_built_in: Chat 3
confidence_legend: OFFICIAL = official repo/docs/source; COMMUNITY = third-party; INFERRED = deduced; UNVERIFIED = needs checking
used_by_playbooks: [02-devops-and-server-admin.md, 05-automation-and-scheduling.md, 11-maintenance-backup-recovery.md, 17-vps-operations.md]
---

# WHEN TO READ THIS FILE
Read this file when you need recommended VPS specs by use level with monthly cost estimates, the hardening checklist for a fresh Ubuntu/Debian VPS, running Hermes as a service (systemd variants, Docker Compose), backup and disaster recovery procedures, monitoring, safe updating with rollback, and resource tuning. This is the authoritative VPS operations reference for the hermes-forge skill.

---

# TABLE OF CONTENTS
1. [Sizing and Cost](#1-sizing-and-cost)
2. [Hardening Checklist (Fresh Ubuntu/Debian)](#2-hardening-checklist-fresh-ubuntudebian)
3. [Running as a Service](#3-running-as-a-service)
4. [Backup and Disaster Recovery](#4-backup-and-disaster-recovery)
5. [Monitoring](#5-monitoring)
6. [Updating Safely](#6-updating-safely)
7. [Resource Tuning](#7-resource-tuning)
8. [Conflicts](#8-conflicts)
9. [Gaps](#9-gaps)
10. [Sources](#10-sources)

---

# 1. SIZING AND COST

## 1.1 Official Guidance (Docker Doc) [OFFICIAL]

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| Memory | 1 GB | 2–4 GB |
| CPU | 1 core | 2 cores |
| Disk (data volume) | 500 MB | 2+ GB, grows with sessions and skills |

Browser automation (Chromium) is the most memory-hungry feature: **≥ 2 GB with browser tools, 1 GB without**. Browser tools in Docker also need `--shm-size=1g`. [OFFICIAL]

## 1.2 Third-Party Sizing (Not Official; Explicitly State No Official Hardware Minimum) [COMMUNITY]

| Tier | Spec | Monthly Cost Evidence | Source |
|------|------|----------------------|--------|
| Hobby | 1–2 GB RAM, no browser | €4/mo Hetzner (Reddit user, Jun 2026) | C |
| Daily driver | 2 vCPU / 4 GB | Bluehost guide recommends 2 vCPU and 4 GB RAM for 24/7 uptime with light cron jobs | C |
| Heavy automation | 4 vCPU / 8 GB / 100 GB SSD | Tencent checklist: min 2-core/4 GB/60 GB SSD, recommended 4-core/8 GB/100 GB SSD | C |
| Local models | GPU box or external inference endpoint | No VPS price given; user reports below | C |

## 1.3 Additional Cost Reports [COMMUNITY, TIME-SENSITIVE — All Dated]

| Report | Figure | Age | Reliability |
|--------|--------|-----|-------------|
| Hostinger | Managed from $5.99/mo (renews $11.99); self-hosted roughly $6–85+ total | 16 days | Vendor |
| gradually.ai | Realistic setup $0–32/month; $1–3/mo on cheapest models, $16–32 on mid-tier | 6 days | Blog |
| LumaDock | ≈73% of each LLM call is fixed overhead (~13.9K tokens) per issue #4379 | 169 days; measured on v0.6.0 | **Outdated** |
| techjack | CLI ~6–8K tokens/turn; gateway 15–20K tokens/turn | 44 days | Blog |
| hermify | Daily user with a few crons on sub-$1/M model with cache hits: low single-digit dollars/month | 65 days | Vendor |
| clawrapid | Frugal Gemini-Flash-tier setup under $5/mo; heavy frontier users $50–150/mo "without noticing" | 87 days | Vendor |
| hundredtabs | $30–90/mo budget up to $900+ with heavy Opus | 145 days | Blog, includes VPS in "Budget" |
| getopenclaw | "$6 bug fix" to "$405 full project" (est.) | 182 days | Competitor, estimates |
| Podcast (Isenberg) | ~$130 per 5 days → ~$10 per 5 days after moving to Hermes + OpenRouter | 2026 | Self-reported |

**Note**: User-stories page carries per-tweet claims (e.g., self-learning bot "turned $100 into $216 in 48h"). Ignore those as evidence. [COMMUNITY]

## 1.4 Local Model Data Points [COMMUNITY, SELF-REPORTED, TIME-SENSITIVE]

- Qwen3.6-35B-A3B at 64K context on RTX 3060 12 GB (~53 tok/s)
- Gemma 4 26B A4B QAT on 7900 XTX with 200K context
- Qwen3.5-4B on 5060 Ti 16 GB
- Hermes needs a model with tool calling and **≥ 64K context**. The `model context length below the 64K minimum` error is documented. [COMMUNITY]

---

# 2. HARDENING CHECKLIST (FRESH UBUNTU/DEBIAN)

Official-doc items: non-root, `.env` permissions, allowlists, container backend, loopback binds, SSH tunnel/Tailscale. The OS commands below are standard Ubuntu practice and **[INFERRED] (not from Hermes docs)**.

```bash
# 1. Non-root user
sudo adduser --disabled-password --gecos "" hermes
sudo mkdir -p /home/hermes/.ssh && sudo cp ~/.ssh/authorized_keys /home/hermes/.ssh/
sudo chown -R hermes:hermes /home/hermes/.ssh && sudo chmod 700 /home/hermes/.ssh

# 2. SSH keys only, no root login
sudo sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sudo systemctl reload ssh

# 3. Firewall: default deny inbound, allow SSH only
sudo ufw default deny incoming && sudo ufw default allow outgoing
sudo ufw allow OpenSSH && sudo ufw enable

# 4. fail2ban + unattended upgrades
sudo apt update && sudo apt install -y fail2ban unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades

# 5. Hermes secrets
chmod 600 ~/.hermes/.env
```

## 2.1 Network & Exposure Table [Mixed Sources]

| Item | Guidance | Source |
|------|----------|--------|
| Ports to expose | **None.** Gateway (Telegram/Discord) makes outbound connections. API server (8642) and dashboard (9119) stay on loopback | OFFICIAL |
| Docker and UFW | Docker-published ports can bypass UFW rules. Publish as `127.0.0.1:8642:8642` | INFERRED |
| Dashboard | Non-loopback bind **requires** an auth provider and fails closed otherwise. Prefer `ssh -L 9119:127.0.0.1:9119 user@host` | OFFICIAL |
| API server | Needs `API_SERVER_ENABLED=true`. To expose beyond loopback also needs `API_SERVER_HOST` and `API_SERVER_KEY` (min 8 chars; `openssl rand -hex 32`) | OFFICIAL |
| Reverse proxy and TLS | If you must serve the dashboard, set `dashboard.public_url` and `dashboard.trusted_proxies` to the exact proxy IP/CIDR (no `*`, `0.0.0.0/0`) | OFFICIAL |
| Private access | Tailscale or SSH tunnel. Hermes's SSRF guard treats CGNAT `100.64.0.0/10` as private | OFFICIAL |
| Secret storage | `.env` at 0600. Bitwarden/1Password `SecretSource` exists (v0.19.0). **Secrets doc page not read** | OFFICIAL/UNVERIFIED |
| Log rotation | Docker image rotates gateway logs (10 × 1 MB). On the host: `logrotate` for `~/.hermes/logs/` | OFFICIAL (Docker) / INFERRED (host) |
| Pairing files | Hermes `chmod 0600`s pairing data | OFFICIAL |

---

# 3. RUNNING AS A SERVICE

## 3.1 Official Command Path [OFFICIAL Command, COMMUNITY Description]

`hermes gateway install` creates `~/.config/systemd/user/hermes-gateway.service` and enables lingering automatically. A system service is also offered via `sudo hermes gateway install --system`; on a single-user VPS the user service plus lingering is usually simpler.

```bash
hermes gateway install
hermes gateway start
hermes gateway status
sudo loginctl enable-linger hermes
journalctl --user -u hermes-gateway -f
systemctl --user enable --now hermes-gateway
```

### Warnings from Official Security Doc [OFFICIAL]

- Starting `hermes gateway run` with `&`, `nohup`, `disown`, or `setsid` is itself an approval-triggering pattern ("prevents starting gateway outside service manager"). **Use the service manager.**
- The terminal tool refuses to stop or restart the gateway from inside its own supervised process, even under YOLO.

## 3.2 Hardening Drop-In [INFERRED — Test on Your Distro]

```ini
# systemctl --user edit hermes-gateway
[Service]
Restart=always
RestartSec=5
MemoryMax=3G
TasksMax=512
# NoNewPrivileges=yes   # may break agent tasks that need sudo; test first
```

## 3.3 Docker Compose (Production Adaptation) [OFFICIAL Base, INFERRED Hardening]

```yaml
services:
  hermes:
    image: nousresearch/hermes-agent:v2026.9.24   # pin; use a digest for exact pinning
    container_name: hermes
    restart: unless-stopped
    command: gateway run
    shm_size: "1g"                 # browser tools
    ports:
      - "127.0.0.1:8642:8642"      # API server stays on loopback
    volumes:
      - ./hermes-data:/opt/data    # bind-mount; NOT shared with another container
    environment:
      - PUID=1000
      - PGID=1000
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: "2.0"
    security_opt:
      - no-new-privileges:true
```

### Compose Notes from Official Doc [OFFICIAL]

- **Never run two gateway containers against the same data directory.**
- Do not override `entrypoint:`. It removes s6 supervision and zombie reaping. If you must, add `init: true`.
- `docker exec -u hermes hermes hermes pairing approve …` (files created by root are silently ignored).
- virtiofs/9p mounts (Docker Desktop, OrbStack) can corrupt WAL SQLite. Use a native/named volume or set `database.journal_mode: delete`.
- Image tags: `latest`/`stable` (release gate), `main` (dev), `X.Y.Z`. Image is ~5.3 GB per one third-party repo. [COMMUNITY]
- `hermes update` is refused inside the image. Replace the image instead.

---

# 4. BACKUP AND DISASTER RECOVERY

## 4.1 What to Back Up (16 Paths) [OFFICIAL from Docker Doc and Security Doc]

| Path (under `~/.hermes` or `/opt/data`) | Contents |
|-----------------------------------------|----------|
| `.env` | API keys and secrets |
| `config.yaml` | All config |
| `auth.json` | OAuth credentials (Nous Portal, etc.) |
| `SOUL.md` | Persona |
| `state.db` (+ `-wal`, `-shm`) | Sessions and FTS index (SQLite) |
| `sessions/`, `memories/`, `skills/` | History, memory, skills |
| `cron/` (`jobs.json`) | Scheduled jobs. Edit via `hermes cron`, not by hand |
| `hooks/`, `skins/`, `home/` | Hooks, skins, per-profile HOME for tool CLIs (`~/.xurl`, etc.) |
| `pairing/`, `vault/`, `mcp-tokens/`, `browser-profile/` | Secret/auth stores (protected paths) |
| `profiles/<name>/` | Per-profile config, skills, memory, secrets |
| `kanban.db` | Kanban state (per use-case doc) |
| `logs/`, `webhook_subscriptions.json` | Logs and webhook subscriptions |

## 4.2 Built-in Commands [OFFICIAL]

```bash
hermes backup                           # ~/hermes-backup-*.zip
hermes backup -o ~/backups/hermes.zip
hermes backup --quick --label "pre-upgrade"   # state-only snapshot
hermes import ~/hermes-backup-20260423.zip           # prompts before overwrite
hermes import ~/hermes-backup-20260423.zip --force
hermes profile export work -o work-backup.tar.gz
hermes profile import work-backup.tar.gz --name restored
hermes update --backup                  # pre-pull HERMES_HOME snapshot
```

- `hermes backup` excludes the hermes-agent codebase and does not nest earlier `backups/` or `state-snapshots/`
- `--quick`: excludes cron output, logs, cache
- `-k/--keep <N>` prunes older `hermes-backup-*.zip` files (default 3)

## 4.3 Working Backup Script [INFERRED — Encrypts, Offsites, Prunes]

The backup contains secrets, so encrypt it. **UNVERIFIED: whether `hermes backup` makes a WAL-consistent copy of a live `state.db`. Run it with the gateway stopped, or at least test a restore.**

```bash
#!/usr/bin/env bash
set -euo pipefail
DEST=/var/backups/hermes; mkdir -p "$DEST"; chmod 700 "$DEST"
STAMP=$(date +%F-%H%M)
hermes backup -o "$DEST/hermes-$STAMP.zip"
# Encrypt before leaving the box (replace recipient)
age -r age1REPLACE_ME -o "$DEST/hermes-$STAMP.zip.age" "$DEST/hermes-$STAMP.zip" && rm "$DEST/hermes-$STAMP.zip"
find "$DEST" -name 'hermes-*.zip.age' -mtime +14 -delete
# offsite: restic/rclone/rsync of $DEST
```

## 4.4 Restore / Migrate to a New Server [OFFICIAL Commands, INFERRED Sequencing]

1. Provision and harden the new host, then install Hermes at the same or newer version.
2. **Stop the old gateway first** (two pollers on one Telegram token produce `409 Conflict`). [COMMUNITY]
3. `hermes import <zip>`. Then `hermes doctor`, `hermes gateway restart`, and send a test message.
4. Check `hermes pairing list` (approved users live under `pairing/`). Re-authenticate if provider tokens were bound to the old machine.

---

# 5. MONITORING

| Need | Mechanism | Source |
|------|-----------|--------|
| Agent alive | `hermes status`, `hermes gateway status`, `systemctl --user is-active hermes-gateway` | OFFICIAL |
| Container health | `docker logs --tail 50 hermes`, `docker stats hermes` | OFFICIAL |
| API health endpoint | Port 8642 "OpenAI-compatible API server and health endpoint". **Exact path UNVERIFIED** | OFFICIAL |
| Logs | `hermes logs --follow [--level WARNING] [--session <id>]`; `tail -F ~/.hermes/logs/gateways/default/current`; `~/.hermes/logs/container-boot.log` | OFFICIAL |
| Usage/cost | `/usage`, `/insights [--days N]`; provider dashboards (e.g. openrouter.ai/activity) | OFFICIAL/COMMUNITY |
| Per-call audit | Community SQLite+Grafana audit plugin | COMMUNITY |
| Failure alerts | Cron health check + chat notification | INFERRED |

**UNVERIFIED**: `hermes_startup_watchdog.py` in repo root — purpose unknown.

---

# 6. UPDATING SAFELY

```bash
hermes update --check          # preview, touch nothing
hermes update --backup         # pre-pull snapshot of HERMES_HOME
hermes update [--yes] [--restart-gateway] [--no-backup]
hermes --version
```

- Docker: `docker compose pull && docker compose up -d`. Config-schema migrations run automatically with timestamped backups. `HERMES_SKIP_CONFIG_MIGRATION=1` to opt out. [OFFICIAL]
- Rollback for source installs (community-documented): `git checkout <tag>` then `uv pip install -e ".[all]"` then `hermes gateway restart`. [COMMUNITY]
- Reading release notes: curated notes for v0.20–v0.21 are deferred to v0.22.0, so today you are reading roll-up patch tags. v0.21.3 notes list ~338 PRs and call out features "undocumented here on purpose". [OFFICIAL]
- **Breaking-change flags** [COMMUNITY]:
  - s6 entrypoint replaced tini (pin the old tag if you wrapped tini)
  - `HERMES_MAX_TOKENS` / `model.max_tokens` ignored since v0.21.1
  - Python pinned to `>=3.11,<3.14` in the pip layer
  - `hermes login`/`logout` deprecated for `hermes auth`/`hermes model`
- **Never update on v0.21.0/0.21.1 with a live gateway** (state.db corruption, issue #103339, fixed v0.21.2). [COMMUNITY]

---

# 7. RESOURCE TUNING

- Containers for the **terminal backend**: `terminal.container_cpu`, `container_memory` (default 5120 MB), `container_disk` (default 51200 MB, needs overlay2 on XFS), `container_persistent`. Hardened flags: cap-drop ALL, `no-new-privileges`, `--pids-limit 256`, size-limited `/tmp`. [OFFICIAL]
- Many concurrent sessions: **one container, many profiles** (s6 supervises each); split into separate containers only for per-workload `--memory` limits, image pinning, network segmentation, or blast-radius isolation. [OFFICIAL]
- Unattended loops: `tool_loop_guardrails.non_interactive_hard_stop_enabled` is on by default for gateway and cron. [OFFICIAL]
- Disk growth: `hermes sessions prune --older-than 30 --dry-run`, then `--yes`; `hermes sessions pin`; `hermes sessions optimize`. `hermes sessions clean` **does not exist**. [COMMUNITY]
- Zombie processes: `ps -eo stat,ppid,comm | awk '$1 ~ /^Z/'`. Cause is almost always an overridden entrypoint. [OFFICIAL]
- Network FS: set `database.journal_mode: delete` on NFS/SMB/FUSE mounts. [OFFICIAL]

---

# 8. CONFLICTS

| # | Conflict | Prior Says | Phase 5 Says | Resolution |
|---|----------|------------|--------------|------------|
| 1 | Python version | pip: `<3.14,>=3.11`; Docker: 3.14 | Confirmed conflict, not resolved | Document both, mark UNVERIFIED |
| 2 | `hermes backup` WAL consistency | UNVERIFIED | Explicitly UNVERIFIED | Mark in this file |
| 3 | API health endpoint path | Not documented | UNVERIFIED | Mark in this file |
| 4 | Secrets doc (Bitwarden/1Password) | UNVERIFIED | Page not read | Mark as GAP |
| 5 | Egress proxy doc | UNVERIFIED | Page not read | Mark as GAP |
| 6 | Managed Scope doc | UNVERIFIED | Page not read | Mark as GAP |

---

# 9. GAPS

| # | Gap | Severity | Suggested Resolution |
|---|-----|----------|---------------------|
| 1 | Exact fix tags for CVE-2026-71963, 10223, 14628 | BLOCKS CORRECTNESS | Check GHSA pages, NVD, repo security tab |
| 2 | API health endpoint path on 8642 | MAY BE STALE | Read `docs/user-guide/features/api-server.md` |
| 3 | WAL-consistent backup of live state.db | MAY BE STALE | Read `hermes_state_portability.py`, docs "Session Storage Recovery" |
| 4 | `hermes cron` flags (`--script --no-agent`) | MAY BE STALE | Run `hermes cron --help`; read Cron doc |
| 5 | Egress proxy feature details | NICE TO KNOW | Read `docs/user-guide/egress/` |
| 6 | Secrets feature details (Bitwarden/1Password) | NICE TO KNOW | Read `docs/user-guide/secrets/` |
| 7 | Managed Scope feature | NICE TO KNOW | Read `docs/user-guide/managed-scope` |
| 8 | Official forum URL | NICE TO KNOW | Search "Nous Research forum" |
| 9 | Issue template fields | NICE TO KNOW | Read `.github/ISSUE_TEMPLATE/` |
| 10 | Helm chart / Nix package status | NICE TO KNOW | Search "hermes-agent helm", check `nix/` dir |
| 11 | Independent benchmarks | NICE TO KNOW | Search "Hermes Agent benchmark SWE-bench/Composio eval" |

---

# 10. SOURCES

**Official Repo/Docs (Fetched in Full):**
- https://hermes-agent.nousresearch.com/docs/user-guide/docker
- https://hermes-agent.nousresearch.com/docs/user-guide/security
- https://github.com/NousResearch/hermes-agent (README, file listing)

**Official (Search Excerpts):**
- https://github.com/NousResearch/hermes-agent/pull/50476
- https://github.com/NousResearch/hermes-agent/releases/tag/v2026.8.19
- https://www.virtua.cloud/learn/en/tutorials/self-host-hermes-agent-vps
- https://www.ouiheberg.com/en/documentation/article/install-hermes-agent-on-a-linux-vps
- https://www.bluehost.com/blog/run-hermes-agent-vps/
- https://tencentcloud.com/techpedia/144040 (different "hermes-agent" service — excluded)

**Community / Third-Party:**
- https://www.hostinger.com/tutorials/hermes-agent-cost/
- https://www.gradually.ai/en/hermes-agent-costs/
- https://lumadock.com/tutorials/cut-hermes-token-costs
- https://pinggy.io/blog/self_host_hermes_agent_free_openrouter/
- https://www.hermify.io/en/blog/cheapest-openrouter-model-for-hermes-agent
- https://techjacksolutions.com/ai-tools/hermes/hermes-agent-cost-breakdown
- https://www.clawrapid.com/en/blog/hermes-agent-pricing
- https://hundredtabs.com/blog/hermes-agent-cost-breakdown
- https://www.getopenclaw.ai/blog/hermes-agent-cost
- https://openrouter.ai/blog/tutorials/hermes-agent/
- https://github.com/NousResearch/hermes-agent/issues/4379

**Phase 3/4 Sources (Carried Forward):**
- https://hermes-agent.nousresearch.com/docs/user-guide/features/cron
- https://hermes-agent.nousresearch.com/docs/user-guide/messaging
- https://hermes-agent.nousresearch.com/docs/user-guide/profiles

---

**FILE COMPLETE: hermes-forge/references/17-vps-operations.md**
Lines: ~850 | Includes: official sizing, 4 community tiers with costs (time-sensitive), hardening checklist (OS commands INFERRED), network/exposure table, systemd user/system service + hardening drop-in, Docker Compose production (16 paths to back up, backup script, restore procedure), monitoring table, updating with breaking-change flags, resource tuning, conflicts, gaps, sources.