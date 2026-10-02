---
title: Installation, VPS Setup & Configuration Basics
source_phases: [Phase 1]
hermes_version_documented: v0.21.5 (tag v2026.9.24, Sep 24 2026)
research_date: Friday, October 2, 2026
last_built_in: Chat 1
confidence_legend: OFFICIAL = official repo/docs/source; COMMUNITY = third-party; INFERRED = deduced; UNVERIFIED = needs checking
used_by_playbooks: [02-devops-and-server-admin.md, 05-automation-and-scheduling.md, 06-messaging-gateway-setups.md, 11-maintenance-backup-recovery.md]
---

# WHEN TO READ THIS FILE
Read this file when you need to install Hermes Agent on a Linux VPS, understand the fresh-VPS walkthrough, configure systemd or Docker deployment, run updates/backups/migrations, troubleshoot common install errors, or learn the home directory layout and secrets handling. This covers every install method, the first-run wizard, and the core configuration fundamentals.

---

# TABLE OF CONTENTS
1. [Official Install Methods](#1-official-install-methods)
2. [Prerequisites](#2-prerequisites)
3. [Fresh Ubuntu VPS Walkthrough (Native)](#3-fresh-ubuntu-vps-walkthrough-native)
4. [Docker & Docker Compose (Official)](#4-docker--docker-compose-official)
5. [VPS Providers, Sizes & Cost](#5-vps-providers-sizes--cost)
6. [Update, Migrate, Uninstall, Backup & Restore](#6-update-migrate-uninstall-backup--restore)
7. [Windows/macOS/WSL Brief](#7-windowsmacoswsl-brief)
8. [Common Errors & Fixes](#8-common-errors--fixes)
9. [First-Run Setup Wizard](#9-first-run-setup-wizard)
10. [Home Directory Layout & Precedence](#10-home-directory-layout--precedence)
11. [Secrets Handling](#11-secrets-handling)
12. [Conflicts](#12-conflicts)
13. [Gaps](#13-gaps)
14. [Sources](#14-sources)

---

# 1. OFFICIAL INSTALL METHODS

| Method | Command / Action | Tag |
|--------|------------------|-----|
| **Linux/macOS/WSL2 one-liner** | `curl -fsSL https://hermes-agent.nousresearch.com/install.sh \| bash` | [OFFICIAL] |
| Raw-script variant (README, older form) | `curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh \| bash` | [OFFICIAL] |
| Docker | `docker run ... nousresearch/hermes-agent` (see Section 4) | [OFFICIAL] |
| Desktop app (macOS Apple Silicon, Windows) | Download from website | [OFFICIAL] |
| Termux APT (aarch64 Android) | `pkg install hermes-agent` (after adding signed repo) | [OFFICIAL] |
| Windows native | `iex (irm https://hermes-agent.nousresearch.com/install.ps1)` | [OFFICIAL] |
| Nix flake | "No longer explicitly supported (best-effort only)" | [OFFICIAL] |
| PyPI (`pip install hermes-agent`) | Appeared in v0.14.0/v0.18.x notes; **current docs say plain `pip install .` on Python <3.14 is unsupported and installs no dependencies** | [OFFICIAL, conflicting] |

**Install flags (verbatim from docs)** [OFFICIAL]:
- `--skip-browser`
- `--skip-computer-use`
- `--non-interactive`
- `--include-desktop`
- `--verbose`
- `--dir`
- Env: `HERMES_INSTALL_VERBOSE=1`

Install log: `logs/install.log` under the Hermes data directory. The script downloads its own pinned `uv` and never uses one already on your PATH [OFFICIAL].

**Post-install**:
```bash
source ~/.bashrc   # or: source ~/.zshrc
hermes             # Start chatting!
```

---

# 2. PREREQUISITES

| Item | Requirement | Tag |
|------|-------------|-----|
| OS | Linux, macOS (Apple Silicon only for desktop installer; Intel macOS unsupported), WSL2, native Windows, Termux | [OFFICIAL] |
| Linux distro list | **Not found**; see Platform Support page | [UNVERIFIED] |
| Packages | Git, curl, tar, SHA-256 utilities | [OFFICIAL] |
| Python/Node | Managed by PM (Python 3.14, Node per `pm/lock.json`); no system Python needed | [OFFICIAL] |
| Compiler | Source builds can need a native compiler and dev libraries | [OFFICIAL] |
| Chromium libs | Linux Chromium needs system libraries from the distro; the installer does **not** run Playwright `--with-deps` or `sudo` for them | [OFFICIAL] |
| GPU | Not required for API-based use | [INFERRED from docs; README says "$5 VPS"] |
| RAM/CPU/disk | Docker doc: minimum 1 GB / 1 core / 500 MB; recommended 2–4 GB / 2 cores / 2+ GB. Browser tools need at least 2 GB. Image about 5.3 GB on Docker Hub | [OFFICIAL] / [COMMUNITY for 5.3 GB] |

---

# 3. FRESH UBUNTU VPS WALKTHROUGH (NATIVE INSTALL)

Steps 1–2 are generic Ubuntu administration, not from Hermes docs [INFERRED]. Steps 3 onward use documented commands.

```bash
# 1. [INFERRED] SSH in, then create a non-root user
adduser hermes
usermod -aG sudo hermes

# 2. [INFERRED] Update and install prerequisites
apt update && apt upgrade -y
apt install -y git curl tar
```

**Critical**: Connect over SSH, not a provider's browser console. The docs warn that some browser consoles (Hetzner is named) corrupt `:`, `@` and `=` in pasted commands and API keys [OFFICIAL].

```bash
# 3. As the hermes user: official installer
su - hermes
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
source ~/.bashrc
export PATH="$HOME/.local/bin:$PATH"   # documented for service-user installs

# 4. Verify
hermes --version
hermes doctor

# 5. Provider and first chat
hermes model          # or: hermes setup --portal   (Nous Portal OAuth path)
hermes --tui          # or: hermes
hermes --continue     # verify session resume works

# 6. Messaging gateway
hermes gateway setup
```

**Gateway allowlist** (in `~/.hermes/.env`) [OFFICIAL]:
```bash
TELEGRAM_ALLOWED_USERS=123456789
```

---

## 3.1 Persistent Service — Option A: User Service + Linger (Docs' Recommendation for Headless VMs) [OFFICIAL]

```bash
hermes gateway install
sudo loginctl enable-linger $USER
hermes gateway start
hermes gateway status
journalctl --user -u hermes-gateway -f
```

## 3.2 Persistent Service — Option B: Boot-Time System Service (Runs as Your User) [OFFICIAL]

```bash
sudo hermes gateway install --system
sudo hermes gateway start --system
sudo hermes gateway status --system
journalctl -u hermes-gateway -f
```

**Notes from docs** [OFFICIAL]:
- A system service needs root for every restart, including the automatic restart at the end of `hermes update`.
- Do not install both the user and system units at once.
- Do not add an `ExecStopPost=/bin/kill -9 $MAINPID` drop-in; it causes an infinite restart loop.
- The generated unit uses `KillMode=mixed`, `KillSignal=SIGTERM` and `Restart=always`.

**Verbatim systemd unit file**: **Not retrieved. Use `hermes gateway install` to generate it** [UNVERIFIED for contents].
- Optional hardening: set `gateway.systemd_watchdog_seconds: 120` in `config.yaml`, then run `hermes gateway install --force` [OFFICIAL].

## 3.3 tmux/screen Alternative [INFERRED]

`hermes gateway` runs in the foreground; tmux wrapper is an addition:

```bash
tmux new -s hermes
hermes gateway
# detach: Ctrl+b then d
```

---

# 4. DOCKER & DOCKER COMPOSE (OFFICIAL)

## 4.1 First-Time Setup Wizard

```sh
mkdir -p ~/.hermes
docker run -it --rm \
  -v ~/.hermes:/opt/data \
  nousresearch/hermes-agent setup
```

## 4.2 Persistent Gateway

```sh
docker run -d \
  --name hermes \
  --restart unless-stopped \
  -v ~/.hermes:/opt/data \
  -p 8642:8642 \
  nousresearch/hermes-agent gateway run
```

## 4.3 Docker Compose (from Docs)

```yaml
services:
  hermes:
    image: nousresearch/hermes-agent:latest
    container_name: hermes
    restart: unless-stopped
    command: gateway run
    ports:
      - "8642:8642"   # gateway API
      - "9119:9119"   # dashboard (only reached when HERMES_DASHBOARD=1)
    volumes:
      - ~/.hermes:/opt/data
    environment:
      - HERMES_DASHBOARD=1
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: "2.0"
```

## 4.4 VPS-Relevant Facts [OFFICIAL]

- **Image tags**: `latest` and `stable` (release-gated), `main` (development), and `X.Y.Z` versioned. Builds are amd64 and arm64. Pin by digest for exact deployments.
- **Supervision**: inside the image, `gateway run` is supervised by s6-overlay. Opt out with `--no-supervise` or `HERMES_GATEWAY_NO_SUPERVISE=1`.
- **Dashboard auth**: a non-loopback dashboard bind fails closed unless an auth provider is configured. Options:
  - `HERMES_DASHBOARD_BASIC_AUTH_USERNAME` + `HERMES_DASHBOARD_BASIC_AUTH_PASSWORD`
  - Nous OAuth
  - Self-hosted OIDC (`HERMES_DASHBOARD_OIDC_ISSUER` + `HERMES_DASHBOARD_OIDC_CLIENT_ID`)
  - `HERMES_DASHBOARD_INSECURE` is now a deprecated no-op.
  - Safer alternative: bind `HERMES_DASHBOARD_HOST=127.0.0.1` and use an SSH tunnel.
- **API server**: requires `API_SERVER_ENABLED=true`. To expose beyond localhost, set `API_SERVER_HOST=0.0.0.0` and `API_SERVER_KEY` (8+ chars, e.g., `openssl rand -hex 32`).
- **One data dir per gateway**: never run two gateway containers against the same data directory.
- **Browser tools** need `--shm-size=1g`.
- **Snap-packaged Docker** (common on Ubuntu cloud images such as Azure) breaks `--init` and `no-new-privileges`. Preferred fix: install Docker from Docker's apt repo. Fallback: `terminal.docker_snap_compat: true`.
- **Permissions**: runtime user is UID 10000. Match host ownership with `HERMES_UID`/`HERMES_GID` or `PUID`/`PGID`.
- **Network filesystems**: `state.db` is WAL by default. On virtiofs/9p/NFS-style mounts, set `database.journal_mode: delete` or use a named Docker volume.
- **Upgrade**: pull image, recreate container, keep data mount:
```sh
docker pull nousresearch/hermes-agent:latest
docker rm -f hermes
docker run -d --name hermes --restart unless-stopped -v ~/.hermes:/opt/data nousresearch/hermes-agent gateway run
```

---

# 5. VPS PROVIDERS, SIZES & COST

- The README says "a $5 VPS" is sufficient [OFFICIAL].
- The Docker docs give 2–4 GB as recommended [OFFICIAL].
- Specific providers, plans and monthly cost ranges from guides: **not found** [UNVERIFIED].

---

# 6. UPDATE, MIGRATE, UNINSTALL, BACKUP & RESTORE

## 6.1 Update (Native Source Install) [OFFICIAL]

```bash
hermes update
hermes update --check          # preview only
hermes update --plan           # fleet preview, read-only
hermes update --backup         # full pre-update zip
hermes update --no-backup
hermes update --branch release-candidate
hermes update --set-channel stable
hermes update --install-id
hermes update --no-gateway-restart
```

**What the update does** [OFFICIAL]:
- Saves a pre-update snapshot (default `quick`) of config, `.env`, `auth.json`, cron jobs and pairing data into `state-snapshots/`.
- Pulls code.
- Validates syntax and **auto-rolls back** if critical files do not parse.
- Prepares dependencies through PM, then migrates config.
- Restarts gateways in a drain-first way (up to `agent.restart_after_turn_timeout`, 30 minutes by default).
- Writes receipts to `~/.hermes/logs/update_receipts/`.
- Mirrors output to `~/.hermes/logs/update.log`, and ignores `SIGHUP` so a dropped SSH session does not kill it.

**Settings**: `updates.pre_update_backup` (`quick`, `full` or `off`) and `updates.backup_keep` (5). Docker, Nix and Termux installs refuse `hermes update` and use their package manager instead. Messaging platforms can run `/update`.

**After updating**:
```bash
git status --short
hermes doctor
hermes --version
hermes gateway status
hermes pm status
```

## 6.2 Config Drift [OFFICIAL]
```bash
hermes config check
hermes config migrate
```

## 6.3 Backup/Restore and Migrate to New Server [OFFICIAL for commands, COMMUNITY for walkthrough]

```bash
hermes backup                    # full archive; includes credentials; excludes runtimes/caches/browser profiles
hermes import <backup-file>      # on the new machine, after installing Hermes
hermes doctor && hermes status
hermes profile export / hermes profile import   # one profile; excludes credentials by design
```

**Exact flags for `hermes backup` and `hermes import` were not retrieved** [UNVERIFIED]. One community tool, `hermes-portable`, exists but is third-party [COMMUNITY].

**State lives in `~/.hermes/`** (config, `.env`, `auth.json`, `SOUL.md`, `memories/`, `skills/`, `cron/`, `sessions/`, `logs/`, `state.db`) [OFFICIAL]. Rotate tokens after migrating.

## 6.4 Uninstall [OFFICIAL]

```bash
hermes uninstall --dry-run
hermes uninstall           # default can preserve config/data
hermes uninstall --full    # also removes data
hermes uninstall --data
```

**Manual removal** (stop the gateway first):
```bash
hermes gateway stop
systemctl --user disable hermes-gateway
rm -f ~/.local/bin/hermes
rm -rf /path/to/hermes-agent
rm -rf ~/.hermes            # optional; keep if you plan to reinstall
```

---

# 7. WINDOWS/macOS/WSL (BRIEF) [OFFICIAL]

- Native Windows is supported via the PowerShell installer, with data in `%LOCALAPPDATA%\hermes`.
- WSL2 uses `~/.hermes` as on Linux.
- macOS is Apple Silicon only for the desktop installer. The gateway runs as a launchd service.
- If your model server runs on the Windows host and Hermes runs in WSL2, see the WSL2 networking section of the providers doc (mirrored networking mode).

---

# 8. COMMON ERRORS & FIXES [OFFICIAL]

| Symptom | Fix |
|---------|-----|
| `hermes: command not found` | `source ~/.bashrc` or fix PATH (`$HOME/.local/bin`) |
| `API key not set` | `hermes model`, or `hermes config set OPENROUTER_API_KEY your_key` |
| Missing config after update | `hermes config check` then `hermes config migrate` |
| Empty or broken replies | Re-run `hermes model`; verify provider, model and auth |
| Gateway starts but nobody can message it | Re-run `hermes gateway setup`; check allowlist/token; `hermes gateway status` |
| `hermes --continue` cannot find a session | Wrong profile; `hermes sessions list` |
| Fetch fails with `should_include_obj should only be called on existing objects` | Git 2.53+ partial-clone bug; the docs give a `.promisor` marker workaround |
| Docker "Permission denied" | Set `HERMES_UID`/`HERMES_GID` or `PUID`/`PGID` |
| Zombie `<defunct>` processes | Do not override the entrypoint; or add `init: true` |
| Container dies at start on snap Docker | Use apt Docker, or `docker_snap_compat: true` |

**Recovery order from quickstart**: `hermes doctor`, `hermes model`, `hermes setup`, `hermes sessions list`, `hermes --continue`, `hermes gateway status`.

---

# 9. FIRST-RUN SETUP WIZARD [OFFICIAL]

On a fresh install, `hermes setup` offers three modes:

| Mode | Behavior |
|------|----------|
| Quick Setup (Nous Portal) | OAuth login, no API keys; sets the model plus the Tool Gateway tools. The documented fast path. |
| Full Setup | Walks through every provider, tool and option (bring your own keys). |
| Blank Slate | Only provider/model plus File Operations and Terminal toolsets. Everything else is off, including compression, checkpoints, smart routing and memory capture. You then choose "everything disabled" or "walk through all configurations". |

**Also documented**:
- The wizard detects `~/.openclaw` and offers to migrate it first.
- Interactive installs also run gateway setup.
- Targeted wizards: `hermes setup agent`, `hermes setup terminal`.
- `hermes setup --portal` skips the mode prompt.

**The question-by-question prompts and what each answer writes were not captured** [UNVERIFIED].

---

# 10. HOME DIRECTORY LAYOUT & PRECEDENCE [OFFICIAL]

```text
~/.hermes/
├── config.yaml     # non-secret settings
├── .env            # API keys and secrets
├── auth.json       # OAuth provider credentials
├── SOUL.md         # primary agent identity (slot #1 in system prompt)
├── memories/       # MEMORY.md, USER.md
├── skills/         # bundled + agent-created skills
├── cron/           # scheduled jobs
├── sessions/       # gateway sessions
├── state.db        # SQLite sessions/messages/routing
├── logs/           # agent.log, errors.log, gateway.log, update.log, tool_calls.log
├── backups/config/ # point-in-time config copies
└── state-snapshots/# pre-update snapshots
```

**Other documented paths**: `cache/scratch` (`TMPDIR` target), `cache/terminal`, `cache/spillover/`, `kanban.db`, `verification_evidence.db`, `modal_snapshots.json`, `profiles/<name>/`, `hooks/`, `skins/`, `pending/skills/`. `HERMES_HOME` overrides the home (Docker uses `/opt/data`).

**Precedence (high to low)**: CLI args, `config.yaml`, `.env`, built-in defaults. Secrets go in `.env`. Non-secret values in `config.yaml` win over `.env`. `${VAR}` substitution works in `config.yaml` (and `${env:VAR}`) [OFFICIAL].

---

# 11. SECRETS HANDLING [OFFICIAL]

- Secrets live in `.env` and `auth.json`.
- `hermes config set UPPER_SNAKE value` automatically writes to `.env`.
- Outside containers, Hermes locks `HERMES_HOME` to mode `0700` at startup. Inside containers it leaves modes alone, and `HERMES_HOME_MODE` can force one.
- Do not make the data tree world-readable.
- External secret sources (Bitwarden, 1Password) were added in v0.19.0, via a `secrets:` block.
- An opt-in Docker egress proxy keeps real keys out of sandboxes: `hermes egress setup && hermes egress start`.

`chmod 600 ~/.hermes/.env` is [INFERRED] best practice; the docs mainly cite the 0700 home lock.

---

# 12. CONFLICTS

| Item | Phase 1 Says | Phase 2 Says | Resolution |
|------|--------------|--------------|------------|
| PyPI install | Supported in v0.14/v0.18; current docs say unsupported | Not mentioned | Mark PyPI as **deprecated/unsupported** in reference. |
| Systemd unit contents | Not retrieved; generated by `hermes gateway install` | Not mentioned | Mark as **UNVERIFIED**. |
| `hermes backup`/`import` flags | Not retrieved | Partial backup flags; import flags not captured | Mark import flags **UNVERIFIED**. |
| VPS provider/cost specifics | "$5 VPS" and 2-4GB Docker recs only | Not mentioned | Mark specific providers **UNVERIFIED**. |

---

# 13. GAPS

| Gap | Description |
|-----|-------------|
| Linux distro support list | Platform Support page not read |
| Setup wizard question-by-question | Only 3 modes documented; individual prompts not captured |
| Verbatim systemd unit file | Generated by `hermes gateway install`; contents not fetched |
| `hermes backup` / `hermes import` full flag sets | Not retrieved from CLI reference |
| VPS provider guides | Only "$5 VPS" mentioned; no specific provider/plan data |
| Nix flake status | "Best-effort only" — details not fetched |
| Windows/macOS/WSL details | Only brief mentions; Platform Support page not read |

---

# 14. SOURCES

- https://hermes-agent.nousresearch.com/docs/getting-started/installation
- https://hermes-agent.nousresearch.com/docs/getting-started/quickstart
- https://hermes-agent.nousresearch.com/docs/getting-started/updating
- https://hermes-agent.nousresearch.com/docs/user-guide/docker
- https://hermes-agent.nousresearch.com/docs/user-guide/messaging/ (service management)
- https://toolnavs.com/en/article/1689-how-to-backup-and-migrate-hermes-agent-server [COMMUNITY]
- https://github.com/zpage/hermes-portable [COMMUNITY]

---

FILE COMPLETE: hermes-forge/references/02-install-vps-config-basics.md
Main tables: Install Methods (8), Prerequisites (8), Common Errors (11), Setup Wizard Modes (3), Home Layout (13 paths), VPS Facts (11). Gaps: 7 items. Conflicts: 4 items.