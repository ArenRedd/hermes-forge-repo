---
title: Security and Hardening Reference
source_phases: [Phase 5, Phase 3, Phase 4]
hermes_version_documented: v0.21.5 (tag v2026.9.24, Sep 24 2026) — Phase 3/4/5 version caveats apply
research_date: Friday, October 2, 2026
last_built_in: Chat 3
confidence_legend: OFFICIAL = official repo/docs/source; COMMUNITY = third-party; INFERRED = deduced; UNVERIFIED = needs checking
used_by_playbooks: [02-devops-and-server-admin.md, 05-automation-and-scheduling.md, 06-messaging-gateway-setups.md, 08-multi-agent-and-parallel.md, 11-maintenance-backup-recovery.md]
---

# WHEN TO READ THIS FILE
Read this file when you need the complete security model, threat mitigations, approval modes by risk level, secret protection, container isolation, network egress controls, API-key spending caps, known vulnerabilities/CVEs, notable incidents, and the "safe by default" vs "full power" annotated config profiles. This is the authoritative security reference for the hermes-forge skill.

---

# TABLE OF CONTENTS
1. [Threat Model](#1-threat-model)
2. [Eight Security Layers](#2-eight-security-layers)
3. [Threat-Specific Mitigations](#3-threat-specific-mitigations)
4. [Approval Modes by Risk Level](#4-approval-modes-by-risk-level)
5. [Secret Protection](#5-secret-protection)
6. [Least-Privilege Users](#6-least-privilege-users)
7. [Container Isolation](#7-container-isolation)
8. [Network Egress Controls](#8-network-egress-controls)
9. [API-Key Spending Caps](#9-api-key-spending-caps)
10. [Known Vulnerabilities (CVEs/GHSAs)](#10-known-vulnerabilities-cvesghsas)
11. [Notable Incidents](#11-notable-incidents)
12. [Comparable Ecosystem Lessons](#12-comparable-ecosystem-lessons)
13. [Safe by Default vs Full Power Profiles](#13-safe-by-default-vs-full-power-profiles)
14. [Hardened VPS Checklist](#14-hardened-vps-checklist)
15. [Conflicts](#15-conflicts)
16. [Gaps](#16-gaps)
17. [Sources](#17-sources)

---

# 1. THREAT MODEL

The project's own policy states [OFFICIAL, via SECURITY.md in forks]:

- **Single trusted operator** — the person who installed and configures Hermes
- **Authorized chat callers get equal trust** — once on the allowlist, they have full agent access
- **Default `terminal.backend: local`** — direct host execution by design
- **Approval system is a core boundary** — not a sandbox, a policy layer
- **Agent shell access "by design" is not a vulnerability** — it's the product
- **Subagents run without recursion** and with `skip_memory=True`
- **Reports go through GitHub Security Advisories** or `security@nousresearch.com` — no bug bounty program

| Threat | Path | Primary Defenses (Official) | Extra Precautions (Inferred) |
|--------|------|----------------------------|------------------------------|
| Prompt injection from web/pages | `web_extract`, `browser_navigate` | SSRF guard; `security.website_blocklist`; Tirith scanner; approvals | Docker backend; no secrets in container; minimal toolsets for untrusted-web profiles |
| Poisoned context files | `AGENTS.md`, `.cursorrules`, `SOUL.md` in a cloned repo | Context scanner (instructions-to-ignore, hidden HTML comments, exfil via curl, invisible Unicode) | Don't point agent at untrusted repos with local backend (see CVE-2026-71963) |
| Malicious skills | Skill install | Skills Guard env-access scan; NVIDIA SkillEvaluator Tier 1 advisory scan on installs (v0.20.4); `required_environment_variables` scoped passthrough | Read `SKILL.md` and scripts; pin; avoid unvetted registries |
| Malicious MCP servers | `mcp_servers` config | MCP subprocess gets only `PATH, HOME, USER, LANG, LC_ALL, TERM, SHELL, TMPDIR`, `XDG_*` and explicit `env`; error text redacted | Allow only servers you audited; treat `command: bash` MCP entries as red flags |
| Malicious chat messages | Gateway | Allowlists; DM pairing (8-char code, 1h TTL, lockout after 5 fails); `unauthorized_dm_behavior` | Allowlist numeric IDs; `ignore` for WhatsApp; keep bot out of public groups |
| Exposed dashboard/API | Ports 9119/8642 | Auth gate; fail-closed; loopback default | Never publish; Tailscale only |
| Credential theft | `terminal`, `execute_code` | Env stripping (`KEY`, `TOKEN`, `SECRET`, `PASSWORD`, …); protected write paths; `.env` read-denied | Separate low-privilege API keys with spend caps |
| Persistence | MCP-config, cron, hooks | `~/.hermes/hooks/*` is **trusted by placement** (no prompt, not skipped by `HERMES_SAFE_MODE`) | Audit `ls ~/.hermes/hooks/`, `config.yaml` MCP entries, `cron/jobs.json` regularly |
| Supply chain | Python deps | Built-in advisory scanner (`hermes doctor`; ack with `hermes doctor --ack <id>`); lazy-install control `security.allow_lazy_installs` | Pin the image digest; disable lazy installs in production |

**Critical Note** [OFFICIAL]: Write guards are explicitly "defense-in-depth, not a hard boundary": the `terminal` tool runs as the same OS user and can still `cat` or overwrite denied paths. Deny rules are a policy over command text, not a sandbox.

---

# 2. EIGHT SECURITY LAYERS

The official security documentation describes 8 layers [OFFICIAL]:

| Layer | Mechanism | Config Key(s) |
|-------|-----------|---------------|
| 1. Allowlists | Per-platform numeric ID allowlists; global `GATEWAY_ALLOWED_USERS` | `TELEGRAM_ALLOWED_USERS`, `DISCORD_ALLOWED_USERS`, `SLACK_ALLOWED_USERS`, `GATEWAY_ALLOWED_USERS` |
| 2. Approvals | Interactive prompt for dangerous commands; `smart`/`manual`/`off` modes | `approvals.mode`, `approvals.deny`, `approvals.timeout` |
| 3. Write guards | `HERMES_WRITE_SAFE_ROOT` restricts `write_file`/`patch`; deny globs | `HERMES_WRITE_SAFE_ROOT`, `approvals.deny` |
| 4. Container isolation | `terminal.backend: docker` runs commands in sandboxed container | `terminal.backend`, `terminal.docker_*` |
| 5. MCP env filtering | MCP subprocess receives only allowlisted env vars + explicit `env` | `mcp_servers.<name>.env` |
| 6. Context scanning | Tirith + custom scanners for prompt injection patterns | `security.tirith_enabled`, `security.tirith_fail_open` |
| 7. Session isolation | Per-session state, no cross-session memory unless curated | `memory.provider`, session DB |
| 8. Input sanitization | Hardline blocklist (unrecoverable), Tirith pre-exec scan | Hardcoded blocklist, `security.tirith_*` |

**Only container isolation (layer 4) and OS permissions are real boundaries** [OFFICIAL]. The rest are policy layers that a determined agent or compromised prompt can potentially bypass.

---

# 3. THREAT-SPECIFIC MITIGATIONS

## 3.1 Prompt Injection (Web/Pages)

| Mitigation | Detail | Confidence |
|------------|--------|------------|
| SSRF Guard | Blocks private/internal network addresses (RFC1918, link-local, CGNAT `100.64.0.0/10`) | OFFICIAL |
| `security.website_blocklist` | Domain glob blocklist for web tools | OFFICIAL |
| `security.allow_private_urls: false` | Default deny for private URLs | OFFICIAL |
| `security.fake_ip_ranges` | For fake-IP proxies (e.g., Clash, Tailscale) | OFFICIAL |
| Tirith Scanner | Pre-exec content scan (homograph URLs, pipe-to-shell, terminal injection) | OFFICIAL |
| Approval prompts | Human review before dangerous commands execute | OFFICIAL |
| Docker backend | Container has no host secrets, limited network | OFFICIAL |

## 3.2 Poisoned Context Files

| Mitigation | Detail | Confidence |
|------------|--------|------------|
| Context scanner | Scans for: instructions-to-ignore, hidden HTML comments, exfil via curl, invisible Unicode | OFFICIAL |
| `SOUL.md` only from `$HERMES_HOME/SOUL.md` | Never loaded from working directory or repo | OFFICIAL |
| Context file size limits | `context_file_max_chars` (floor 20K, ceiling 500K) | OFFICIAL |
| Don't use local backend on untrusted repos | CVE-2026-71963: repo-delivered `.git/config` RCE | OFFICIAL (CVE) |

## 3.3 Malicious Skills

| Mitigation | Detail | Confidence |
|------------|--------|------------|
| Skills Guard | Install-time env-access scan; fails if skill requests undeclared env vars | OFFICIAL |
| NVIDIA SkillEvaluator Tier 1 | Advisory scan on install (v0.20.4+); `skills.tier1_advisory: true` default | OFFICIAL |
| `required_environment_variables` | Scoped passthrough — only declared vars passed to skill | OFFICIAL |
| `skills.write_approval: true` | Stage skill writes for review before applying | OFFICIAL |
| `skills.guard_agent_created: true` | Scan skills created by agent itself | OFFICIAL |
| Pin skills | Use `hermes skills trust` and avoid auto-updates | OFFICIAL |

## 3.4 Malicious MCP Servers

| Mitigation | Detail | Confidence |
|------------|--------|------------|
| Env filtering | MCP subprocess gets only: `PATH, HOME, USER, LANG, LC_ALL, TERM, SHELL, TMPDIR`, `XDG_*`, plus explicit `env` in config | OFFICIAL |
| Error redaction | Error text from MCP servers is redacted before returning to agent | OFFICIAL |
| `command: bash` red flag | Treat any MCP entry with `command: bash` as suspicious | INFERRED |
| Audit MCP entries | Regular `hermes mcp list` and inspect `config.yaml` | INFERRED |

## 3.5 Malicious Chat Messages

| Mitigation | Detail | Confidence |
|------------|--------|------------|
| Numeric ID allowlists | `TELEGRAM_ALLOWED_USERS=123456789,987654321` — never usernames | OFFICIAL |
| DM pairing | 8-char code, 1h TTL, lockout after 5 fails | OFFICIAL |
| `unauthorized_dm_behavior: ignore\|pair\|decline` | Default `pair`; set `ignore` for WhatsApp | OFFICIAL |
| `GATEWAY_ALLOW_ALL_USERS=true` — NEVER USE | Opens bot to everyone | OFFICIAL |
| Keep bot out of public groups | Prevents prompt injection from strangers | INFERRED |

## 3.6 Exposed Dashboard/API

| Mitigation | Detail | Confidence |
|------------|--------|------------|
| Loopback default | Dashboard (9119) and API (8642) bind to `127.0.0.1` by default | OFFICIAL |
| Auth required for non-loopback | Dashboard refuses to start on `0.0.0.0` without auth provider | OFFICIAL |
| `HERMES_DASHBOARD_BASIC_AUTH_*` | Basic auth username/password/secret | OFFICIAL |
| `HERMES_DASHBOARD_OAUTH_*` | OAuth/OIDC providers | OFFICIAL |
| `dashboard.public_url` + `dashboard.trusted_proxies` | Exact proxy IP/CIDR required (no `*`, `0.0.0.0/0`) | OFFICIAL |
| SSH tunnel / Tailscale | Only way to reach dashboard remotely | OFFICIAL |
| **Never expose publicly** | "The API server is a full agent runtime. Never expose it publicly." | OFFICIAL |

## 3.7 Credential Theft

| Mitigation | Detail | Confidence |
|------------|--------|------------|
| Env stripping | Agent strips `KEY`, `TOKEN`, `SECRET`, `PASSWORD`, `CREDENTIAL` from env passed to tools | OFFICIAL |
| Protected write paths | `HERMES_WRITE_SAFE_ROOT` restricts where agent can write | OFFICIAL |
| `.env` read-denied | Agent cannot read `.env` via file tools | OFFICIAL |
| Spend-capped keys | Use provider-side limits (OpenRouter credit limit, etc.) | OFFICIAL |

## 3.8 Persistence

| Mitigation | Detail | Confidence |
|------------|--------|------------|
| Audit hooks | `ls ~/.hermes/hooks/` — trusted by placement, no prompt | OFFICIAL |
| Audit MCP config | Check `config.yaml` `mcp_servers` entries | OFFICIAL |
| Audit cron jobs | Check `cron/jobs.json` or `hermes cron list` | OFFICIAL |
| `HERMES_SAFE_MODE` | Skips plugins, **not gateway hooks** | OFFICIAL |

## 3.9 Supply Chain

| Mitigation | Detail | Confidence |
|------------|--------|------------|
| Advisory scanner | `hermes doctor` checks Python deps; ack with `hermes doctor --ack <id>` | OFFICIAL |
| `security.allow_lazy_installs: false` | Disable lazy installs in production | OFFICIAL |
| Pin image digest | `nousresearch/hermes-agent@sha256:...` not just tag | INFERRED |
| `pm/lock.json` | Pinned tool/extras manager | OFFICIAL |

---

# 4. APPROVAL MODES BY RISK LEVEL

| Risk Level | Recommended Config | Notes |
|------------|-------------------|-------|
| Disposable container / CI | `approvals.mode: off` or `--yolo` + `approvals.deny` rules | Hardline blocklist still applies |
| Personal VPS, gateway users trusted | `smart` (default) + deny rules + docker backend | Smart = aux-LLM risk assessment; each verdict covers that exact command only |
| Shared/multi-user or sensitive host | `manual`, `cron_mode: deny`, `unattended_mode: deny` | Prompt timeout defaults to deny after 300s |
| Headless (cron, webhook, `-q`) | Keep all three `deny` modes | Use `command_allowlist` for specific rule keys only |

**Hardline blocklist** (cannot be overridden by `--yolo`, mode `off`, or "always" responses) [OFFICIAL]:
- `rm -rf /` (recursive root deletion)
- Fork bombs (`:(){ :|:& };:` and variants)
- `mkfs` on root device
- `dd` to block devices (`/dev/*`)

**Mine approvals into allowlist proposals** (never auto-applied) [OFFICIAL]:
```bash
hermes approvals suggest [--apply 1,3] [--json] [--days N] [--min-count N] [--limit N]
```
Destructive classes are never proposed.

---

# 5. SECRET PROTECTION

## Config Block
```yaml
secrets:
  bitwarden:
    enabled: true
    # session token via BW_SESSION or login
  onepassword:
    enabled: false  # proposed in issue #36949, not confirmed shipped
    # op_service_account_token via OP_SERVICE_ACCOUNT_TOKEN
```

## Env Vars (in `~/.hermes/.env`, `chmod 600`)
```bash
# Platform credentials
HERMES_TELEGRAM_BOT_TOKEN="..."
DISCORD_BOT_TOKEN="..."
SLACK_BOT_TOKEN="..."

# Provider keys
OPENROUTER_API_KEY="..."
OPENAI_API_KEY="..."
ANTHROPIC_API_KEY="..."

# Memory providers
MEM0_API_KEY="..."
HONCHO_API_KEY="..."
HINDSIGHT_API_KEY="..."

# Search
TAVILY_API_KEY="..."
EXA_API_KEY="..."
BRAVE_SEARCH_API_KEY="..."

# Media
FAL_KEY="..."
ELEVENLABS_API_KEY="..."
```

## Write Sandbox
```bash
# ~/.hermes/.env
HERMES_WRITE_SAFE_ROOT=/opt/data:/home/you/.hermes:/path/to/project
```
Multiple paths colon-separated. Agent cannot write outside these roots.

---

# 6. LEAST-PRIVILEGE USERS

- **Non-root user required**: Official checklist says never run gateway as root; Docker image refuses root by default [OFFICIAL]
- **Docker**: Runs as `hermes` user (UID 1000) inside container
- **PUID/PGID** or `HERMES_UID`/`HERMES_GID` for host volume UID mapping
- **SSH backend**: Use dedicated low-privilege user on remote host

---

# 7. CONTAINER ISOLATION

## Docker Backend (Skips Approval Entirely) [OFFICIAL]

| Backend | Reason |
|---------|--------|
| `docker` | Container isolation — long-lived container, `docker exec` |
| `singularity` | Container isolation (Apptainer) |
| `modal` | Serverless isolation |
| `daytona` | Workspace isolation |
| `vercel_sandbox` | VM isolation |

**Local, SSH backends**: Full approval flow applies.

## Hardening Flags (via `terminal.docker_extra_args`)

```yaml
terminal:
  backend: docker
  docker_extra_args: |
    --read-only
    --cap-drop=ALL
    --cap-add=CAP_DAC_OVERRIDE
    --cap-add=CAP_SETUID
    --cap-add=CAP_SETGID
    --security-opt=no-new-privileges:true
    --pids-limit=100
    --memory=2g
    --cpus=2
    --tmpfs /tmp:noexec,nosuid,size=100m
    --user 1000:1000
```

## Egress Proxy (Credential Injection for Docker)

```bash
# Iron-proxy based credential injection for sandboxed containers
hermes egress start
hermes egress status
hermes egress stop
```
- Injects credentials into sandboxed containers
- Disabled by default
- Config: `egress.*` namespace

---

# 8. NETWORK EGRESS CONTROLS

**No built-in config key for network restrictions** [INFERRED].

Options:
1. **Docker**: `--network=none` or custom bridge + iptables
2. **Host**: ufw/nftables/iptables
3. **SSH**: Remote host firewall
4. **Modal/Vercel**: Provider-level policies
5. **Singularity**: `--network=none` (Apptainer 1.2+)

## SSRF Guard (Built-in)
- Blocks RFC1918, link-local, CGNAT `100.64.0.0/10`
- `security.allow_private_urls: true` to allow (trusted hosts only)
- `security.fake_ip_ranges` for fake-IP proxies

---

# 9. API-KEY SPENDING CAPS

**Hard caps that definitely work** [Phase 5]:
- Provider-side key limits/budgets: OpenRouter (credit limit), OpenAI (usage limits), Anthropic (usage limits)
- Set these **before any cron jobs** [Phase 5: "Set provider-side spend limits before any cron"]

**Hermes config layer budget** [UNVERIFIED — Phase 5]:
- LumaDock claims `budget.daily_usd` config key exists
- **Phase 5: "I found no official corroboration. Treat that key as UNVERIFIED and do not rely on it."**
- Do not rely on Hermes-internal budget enforcement

---

# 10. KNOWN VULNERABILITIES (CVEs/GHSAs)

All from third-party advisory databases unless stated. [Phase 5 Section 3.3]

| CVE / GHSA | Issue | Affected → Fixed | Severity | Source |
|------------|-------|------------------|----------|--------|
| CVE-2026-71963 / GHSA-7x36-8jrh-v4pw | RCE via repository-delivered `.git/config` (`core.fsmonitor`), no prompt | 0.18.2–0.21.0; fixed by commit f6234d0, first released after 0.21.0 (exact tag: **UNVERIFIED**; use ≥ v0.21.5) | n/a | C (PoC repo: Boreas37/CVE-2026-71963-PoC) |
| CVE-2026-53869 / GHSA-4pqm-j46f-795x | DNS rebinding bypass on WebSocket endpoints (`/api/pty`, `/api/ws`, `/api/pub`, `/api/events`) | <0.16.0 → 0.16.0 | High | C |
| CVE-2026-9366 / GHSA-pgp4-xr4j-h5cg | Injection in `_scan_context_content` (`agent/prompt_builder.py`) | <0.15.0 → 0.15.0 | Moderate | C |
| CVE-2026-9368 / GHSA-wm96-9gfh-vvgq | `execute_code` environment handling / sandbox issue | before 0.11.0 → 0.11.0 | 7.3 High | C |
| CVE-2026-10223 | RCE-class injection in memory-content scanning (`tools/memory_tool.py`), versions up to 2026.4.30 | Fix version **UNVERIFIED** | n/a | C (SentinelOne) |
| CVE-2026-14628 / GHSA-85cr-q769-68x2 | Path traversal in `extract_media` (`gateway/platforms/base.py`), up to 2026.5.16 | Fix **UNVERIFIED** | Moderate | C |

**UNVERIFIED / NEEDS CHECKING** [Phase 5]:
- Vendor blog (BetterClaw, competitor) also lists CVE-2026-11461, CVE-2026-10548, CVE-2026-85105 and claims OpenClaw's CVE-2026-25253 (CVSS 8.8) — **not confirmed**
- Several VulDB-sourced entries say the vendor "did not respond"
- Compare against repo's GHSA page: https://github.com/NousResearch/hermes-agent/security

---

# 11. NOTABLE INCIDENTS

## June 2026 "hermes-0day" Campaign [OFFICIAL/C]

**What happened**: Scanners found exposed dashboards (running as root with `--insecure --host 0.0.0.0` and exposed OpenAI-style API server). Drove the agent to plant a `command: bash` MCP entry that appended an attacker SSH key to `authorized_keys`. The planted entry re-installed the key on every cron tick and startup.

**Fixed by**: June 2026 auth hardening (PR #50476) shipped in v0.18.0. `--insecure` and `HERMES_DASHBOARD_INSECURE` are now deprecated no-ops.

**Lessons for Hermes users**:
- Never run as root
- Never bind publicly
- Audit MCP entries and `authorized_keys` periodically
- Assume anything reachable from the internet will be probed

---

# 12. COMPARABLE ECOSYSTEM LESSONS

| Ecosystem | Lesson | Confidence |
|-----------|--------|------------|
| OpenClaw (vendor blog) | Registry skills have carried prompt injections | UNVERIFIED (competitor source) |
| HN quote (official user-stories page) | "don't give it free reign... Run it within a sandbox" | COMMUNITY |
| General | Agent self-editing its own internals observed | COMMUNITY |
| General | Default-config pitfalls: "Hermes was not broken. The config was default." | COMMUNITY |
| General | Approval-gate bypass observed in user audit (112 of 129 sessions had a violation, issue #17619, self-reported) | COMMUNITY |

---

# 13. SAFE BY DEFAULT VS FULL POWER PROFILES

**Keys below were seen verbatim in the official security/Docker docs** [OFFICIAL keys; values INFERRED from Phase 5].

## SAFE BY DEFAULT (Recommended for production VPS)

```yaml
# ~/.hermes/config.yaml — SAFE BY DEFAULT
approvals:
  mode: manual                 # human approves every dangerous command
  timeout: 300
  cron_mode: deny
  single_query_mode: deny
  unattended_mode: deny
  destructive_slash_confirm: true
  deny:                        # applies to ALL backends, evaluated before approvals
    - "sudo *"
    - "*curl*|*sh*"
    - "git push --force*"
terminal:
  backend: docker              # container is the boundary (dangerous-cmd checks skipped inside)
  docker_forward_env: []       # no secrets into the container
  container_cpu: 1
  container_memory: 2048
  container_disk: 20480
  container_persistent: true
security:
  tirith_enabled: true
  tirith_fail_open: false      # block if scanner unavailable
  allow_private_urls: false
  allow_lazy_installs: false
  website_blocklist:
    enabled: true
    domains: ["*.internal.example", "admin.example.com"]
unauthorized_dm_behavior: ignore
auth:
  adopt_external_logins: false
tool_loop_guardrails:
  non_interactive_hard_stop_enabled: true
```

```bash
# ~/.hermes/.env (chmod 600)
TELEGRAM_ALLOWED_USERS=123456789     # numeric IDs only; never GATEWAY_ALLOW_ALL_USERS=true
HERMES_WRITE_SAFE_ROOT=/opt/data     # restrict write_file/patch
```

## FULL POWER (Trusted single operator, disposable or well-isolated VPS)

```yaml
# ~/.hermes/config.yaml — FULL POWER
approvals:
  mode: smart                  # or "off" with deny rules as the only brake
  cron_mode: approve           # cron may run dangerous commands unattended
  deny:
    - "git push --force*"
    - "dd if=* of=/dev/*"
terminal:
  backend: local               # direct host access: browser, apps, SSH to other hosts
security:
  tirith_fail_open: true
  allow_lazy_installs: true
```

| Tradeoff | Safe | Full Power |
|----------|------|------------|
| Blast radius | Container only | Whole OS user |
| Friction | Approval prompts, no host tools | Few prompts |
| Prompt-injection impact | Bounded | Can reach `~/.ssh`, cloud creds, local network |
| Mitigation if full power | Run on dedicated VPS with scoped network access (e.g. Tailscale tag), spend-capped keys, nothing sensitive on the box | — |

---

# 14. HARDENED VPS CHECKLIST (Merged from Phase 3 + Phase 5, Deduplicated but Lossless)

### 14.1 OS Hardening (Fresh Ubuntu/Debian) [INFERRED — standard Ubuntu practice, not from Hermes docs]

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

### 14.2 Network & Exposure

| Item | Guidance | Source |
|------|----------|--------|
| Ports to expose | **None.** Gateway makes outbound connections. API (8642) and dashboard (9119) stay on loopback | OFFICIAL |
| Docker and UFW | Docker-published ports can bypass UFW. Publish as `127.0.0.1:8642:8642` | INFERRED |
| Dashboard | Non-loopback bind **requires** auth provider and fails closed. Prefer `ssh -L 9119:127.0.0.1:9119 user@host` | OFFICIAL |
| API server | Needs `API_SERVER_ENABLED=true`. To expose beyond loopback also needs `API_SERVER_HOST` and `API_SERVER_KEY` (min 8 chars; `openssl rand -hex 32`) | OFFICIAL |
| Reverse proxy and TLS | If you must serve dashboard, set `dashboard.public_url` and `dashboard.trusted_proxies` to exact proxy IP/CIDR (no `*`, `0.0.0.0/0`) | OFFICIAL |
| Private access | Tailscale or SSH tunnel. Hermes's SSRF guard treats CGNAT `100.64.0.0/10` as private | OFFICIAL |
| Secret storage | `.env` at 0600. Bitwarden/1Password `SecretSource` exists (v0.19.0). **Secrets doc page not read** | OFFICIAL/UNVERIFIED |
| Log rotation | Docker image rotates gateway logs (10 × 1 MB). On host: `logrotate` for `~/.hermes/logs/` | OFFICIAL (Docker) / INFERRED (host) |
| Pairing files | Hermes `chmod 0600`s pairing data | OFFICIAL |

### 14.3 Service Management

**Official command path** [OFFICIAL]:
```bash
hermes gateway install          # creates ~/.config/systemd/user/hermes-gateway.service, enables lingering
hermes gateway start
hermes gateway status
sudo loginctl enable-linger hermes
journalctl --user -u hermes-gateway -f
systemctl --user enable --now hermes-gateway
```

**Warnings** [OFFICIAL]:
- Starting `hermes gateway run` with `&`, `nohup`, `disown`, or `setsid` triggers approval ("prevents starting gateway outside service manager")
- Terminal tool refuses to stop/restart gateway from inside its own supervised process, even under YOLO

**Hardening drop-in** [INFERRED — test on your distro]:
```ini
# systemctl --user edit hermes-gateway
[Service]
Restart=always
RestartSec=5
MemoryMax=3G
TasksMax=512
# NoNewPrivileges=yes   # may break agent tasks that need sudo; test first
```

**Docker Compose (Production)** [OFFICIAL base, INFERRED hardening]:
```yaml
services:
  hermes:
    image: nousresearch/hermes-agent:v2026.9.24   # pin; use digest for exact pinning
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

**Compose Notes** [OFFICIAL]:
- Never run two gateway containers against the same data directory
- Do not override `entrypoint:` (removes s6 supervision). If you must, add `init: true`
- `docker exec -u hermes hermes hermes pairing approve …` (files created by root silently ignored)
- virtiofs/9p mounts (Docker Desktop, OrbStack) can corrupt WAL SQLite. Use named volume or set `database.journal_mode: delete`
- Image tags: `latest`/`stable` (release gate), `main` (dev), `X.Y.Z`. Image ~5.3 GB [COMMUNITY]
- `hermes update` refused inside image. Replace the image instead.

### 14.4 Backup & Disaster Recovery

**What to Back Up** (16 paths) [OFFICIAL from Docker doc and security doc]:

| Path (under `~/.hermes` or `/opt/data`) | Contents |
|-----------------------------------------|----------|
| `.env` | API keys and secrets |
| `config.yaml` | All config |
| `auth.json` | OAuth credentials (Nous Portal, etc.) |
| `SOUL.md` | Persona |
| `state.db` (+ `-wal`, `-shm`) | Sessions and FTS index (SQLite) |
| `sessions/`, `memories/`, `skills/` | History, memory, skills |
| `cron/` (`jobs.json`) | Scheduled jobs. Edit via `hermes cron`, not by hand |
| `hooks/`, `skins/`, `home/` | Hooks, skins, per-profile HOME for tool CLIs |
| `pairing/`, `vault/`, `mcp-tokens/`, `browser-profile/` | Secret/auth stores (protected paths) |
| `profiles/<name>/` | Per-profile config, skills, memory, secrets |
| `kanban.db` | Kanban state |
| `logs/`, `webhook_subscriptions.json` | Logs and webhook subscriptions |

**Built-in Commands** [OFFICIAL]:
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
- `hermes backup` excludes hermes-agent codebase and does not nest earlier `backups/` or `state-snapshots/`
- `-k/--keep <N>` prunes older `hermes-backup-*.zip` (default 3)

**Working Backup Script** [INFERRED — encrypts, offsites, prunes]:
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

**Restore / Migrate to New Server** [OFFICIAL commands, INFERRED sequencing]:
1. Provision and harden new host, install Hermes at same or newer version
2. **Stop the old gateway first** (two pollers on one Telegram token produce `409 Conflict`) [COMMUNITY]
3. `hermes import <zip>`. Then `hermes doctor`, `hermes gateway restart`, send test message
4. Check `hermes pairing list`. Re-authenticate if provider tokens bound to old machine

### 14.5 Monitoring

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

### 14.6 Updating Safely

```bash
hermes update --check          # preview, touch nothing
hermes update --backup         # pre-pull snapshot of HERMES_HOME
hermes update [--yes] [--restart-gateway] [--no-backup]
hermes --version
```

- Docker: `docker compose pull && docker compose up -d`. Config-schema migrations run automatically with timestamped backups. `HERMES_SKIP_CONFIG_MIGRATION=1` to opt out [OFFICIAL]
- Rollback for source installs: `git checkout <tag>` then `uv pip install -e ".[all]"` then `hermes gateway restart` [COMMUNITY]
- Curated notes for v0.20–v0.21 deferred to v0.22.0; today you read roll-up patch tags. v0.21.3 notes list ~338 PRs with features "undocumented here on purpose" [OFFICIAL]
- **Breaking-change flags** [COMMUNITY]:
  - s6 entrypoint replaced tini (pin old tag if you wrapped tini)
  - `HERMES_MAX_TOKENS` / `model.max_tokens` ignored since v0.21.1
  - Python pinned to `>=3.11,<3.14` in pip layer
  - `hermes login`/`logout` deprecated for `hermes auth`/`hermes model`
- **Never update on v0.21.0/0.21.1 with live gateway** (state.db corruption, issue #103339, fixed v0.21.2) [COMMUNITY]

### 14.7 Resource Tuning

- Terminal backend containers: `terminal.container_cpu`, `container_memory` (default 5120 MB), `container_disk` (default 51200 MB, needs overlay2 on XFS), `container_persistent`. Hardened flags: cap-drop ALL, `no-new-privileges`, `--pids-limit 256`, size-limited `/tmp` [OFFICIAL]
- Many concurrent sessions: **one container, many profiles** (s6 supervises each); split into separate containers only for per-workload `--memory` limits, image pinning, network segmentation, or blast-radius isolation [OFFICIAL]
- Unattended loops: `tool_loop_guardrails.non_interactive_hard_stop_enabled` on by default for gateway and cron [OFFICIAL]
- Disk growth: `hermes sessions prune --older-than 30 --dry-run`, then `--yes`; `hermes sessions pin`; `hermes sessions optimize`. `hermes sessions clean` **does not exist** [COMMUNITY]
- Zombie processes: `ps -eo stat,ppid,comm | awk '$1 ~ /^Z/'`. Cause almost always overridden entrypoint [OFFICIAL]
- Network FS: set `database.journal_mode: delete` on NFS/SMB/FUSE mounts [OFFICIAL]

---

# 15. CONFLICTS

| # | Conflict | Prior Says | Phase 5 Says | Resolution |
|---|----------|------------|--------------|------------|
| 1 | Python version | pip: `<3.14,>=3.11`; Docker: 3.14 | Confirmed conflict, not resolved | Document both, mark UNVERIFIED |
| 2 | CVE-2026-71963 fix tag | UNVERIFIED | UNVERIFIED (PoC confirms) | Keep UNVERIFIED, note ≥ v0.21.5 |
| 3 | CVE-2026-10223 fix version | UNVERIFIED | UNVERIFIED | Keep UNVERIFIED |
| 4 | CVE-2026-14628 fix version | UNVERIFIED | UNVERIFIED | Keep UNVERIFIED |
| 5 | Extra CVEs (vendor blog) | Listed | Not confirmed | List as UNVERIFIED vendor claims |
| 6 | Approval defaults | `manual`+`cron_mode: deny` vs `smart`+`unattended_mode: deny` | Risk-level recommendations | Use Phase 5 risk-level table |
| 7 | Budget config key | Not documented | `budget.daily_usd` UNVERIFIED | Mark BLOCKS CORRECTNESS in 22-unverified |
| 8 | Health endpoint path | Not documented | UNVERIFIED | Mark in 22-unverified |
| 9 | WAL consistency of backup | UNVERIFIED | Explicitly UNVERIFIED | Mark in 17-vps-operations.md |
| 10 | Egress/Secrets/Managed Scope docs | UNVERIFIED | Pages not read | Mark as GAP in 22-unverified |

---

# 16. GAPS

| # | Gap | Severity | Suggested Resolution |
|---|-----|----------|---------------------|
| 1 | Exact fix tags for CVE-2026-71963, 10223, 14628 | BLOCKS CORRECTNESS | Check GHSA pages, NVD, repo security tab |
| 2 | `budget.daily_usd` config key existence | BLOCKS CORRECTNESS | Check `cli-config.yaml.example`, `hermes config check` |
| 3 | API health endpoint path on 8642 | MAY BE STALE | Read `docs/user-guide/features/api-server.md` |
| 4 | WAL-consistent backup of live state.db | MAY BE STALE | Read `hermes_state_portability.py`, docs "Session Storage Recovery" |
| 5 | `hermes cron` flags (`--script --no-agent`) | MAY BE STALE | Run `hermes cron --help`; read Cron doc |
| 6 | Egress proxy feature details | NICE TO KNOW | Read `docs/user-guide/egress/` |
| 7 | Secrets feature details (Bitwarden/1Password) | NICE TO KNOW | Read `docs/user-guide/secrets/` |
| 8 | Managed Scope feature | NICE TO KNOW | Read `docs/user-guide/managed-scope` |
| 9 | Official forum URL | NICE TO KNOW | Search "Nous Research forum" |
| 10 | Issue template fields | NICE TO KNOW | Read `.github/ISSUE_TEMPLATE/` |
| 11 | Helm chart / Nix package status | NICE TO KNOW | Search "hermes-agent helm", check `nix/` dir |
| 12 | Independent benchmarks | NICE TO KNOW | Search "Hermes Agent benchmark SWE-bench/Composio eval" |
| 13 | 16 mop-up features (fleet, worktree, Bot Mode, Cloud, etc.) | NICE TO KNOW | Target for future research passes |

---

# 17. SOURCES

**Official Repo/Docs (Fetched in Full):**
- https://hermes-agent.nousresearch.com/docs/user-guide/security
- https://hermes-agent.nousresearch.com/docs/user-guide/docker
- https://github.com/NousResearch/hermes-agent (README, file listing)

**Official (Search Excerpts):**
- https://github.com/NousResearch/hermes-agent/pull/50476
- https://github.com/NousResearch/hermes-agent/releases/tag/v2026.8.19 (v0.20.5)
- https://github.com/advisories/GHSA-4pqm-j46f-795x
- https://github.com/advisories/GHSA-pgp4-xr4j-h5cg
- https://github.com/advisories/ghsa-85cr-q769-68x2
- https://advisories.gitlab.com/pypi/hermes-agent/CVE-2026-9368/
- https://www.sentinelone.com/vulnerability-database/cve-2026-10223/
- https://github.com/Boreas37/CVE-2026-71963-PoC

**Community / Third-Party:**
- https://www.betterclaw.io/blog/hermes-agent-not-working (Sept 28, 2026)
- https://www.virtua.cloud/learn/en/tutorials/self-host-hermes-agent-vps
- https://www.ouiheberg.com/en/documentation/article/install-hermes-agent-on-a-linux-vps
- https://www.bluehost.com/blog/run-hermes-agent-vps/
- https://tencentcloud.com/techpedia/144040 (different "hermes-agent" service — excluded)
- https://www.agent37.com/blog/hermes-agent-web-ui-setup-security-and-managed-alternatives-2026
- https://buttondown.com/witcheer/archive/secure-hermes/

**Phase 3/4 Sources (Carried Forward):**
- https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp
- https://hermes-agent.nousresearch.com/docs/reference/cli-commands
- https://hermes-agent.nousresearch.com/docs/user-guide/skills
- https://github.com/NousResearch/hermes-agent/tree/main/plugins/memory/honcho

---

**FILE COMPLETE: hermes-forge/references/16-security-and-hardening.md**
Lines: ~1,100 | Includes: threat model, 8 layers, threat mitigations, approval modes by risk, secret protection, container isolation, network egress, API caps, 6 CVEs, June 2026 incident, comparable lessons, safe/full power profiles side-by-side, hardened VPS checklist (merged Phase 3+5), conflicts, gaps, sources.