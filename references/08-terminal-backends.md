---
title: Terminal Backends Reference
source_phases: [Phase 3]
hermes_version_documented: v0.21.5 (tag v2026.9.24, Sep 24 2026) — Phase 3 version not pinned; docs track `main`
research_date: Friday, October 2, 2026
last_built_in: Chat 2
confidence_legend: OFFICIAL = official repo/docs/source; COMMUNITY = third-party; INFERRED = deduced; UNVERIFIED = needs checking
used_by_playbooks: [02-devops-and-server-admin.md, 05-automation-and-scheduling.md, 07-browser-and-data-collection.md, 08-multi-agent-and-parallel.md, 11-maintenance-backup-recovery.md]
---

# Terminal Backends Reference

## WHEN TO READ THIS FILE
Use this file when you need to select, configure, or troubleshoot a terminal backend for Hermes Agent. Covers all 7 backends, their exact config keys, environment variables, setup commands, hardening flags, and file transfer mechanisms.

## TABLE OF CONTENTS
1. Backend Overview and Selection
2. Local Backend (Default)
3. Docker Backend
4. SSH Backend
5. Singularity/Apptainer Backend
6. Modal Backend
7. Daytona Backend
8. Vercel Sandbox Backend
9. Decision Table
10. Host ↔ Sandbox File Transfer
11. Docker Hardening Flags
12. Network Restrictions
13. Conflicts
14. Gaps
15. Sources

---

## 1. Backend Overview and Selection

Hermes Agent supports **7 terminal backends** that provide isolated execution environments for the `terminal` tool and background processes. The backend is selected via:

- **Config key**: `terminal.backend` (values: `local`, `docker`, `ssh`, `singularity`, `modal`, `daytona`, `vercel_sandbox`)
- **CLI flag**: `hermes chat --in docker` (alias `--backend`)
- **Per-command**: `terminal(command="...", backend="docker")` in `execute_code`

**Default**: `local` (runs directly on host)

**Precedence**: CLI flag → `terminal.backend` config → `local`

---

## 2. Local Backend (Default)

| Property | Value |
|----------|-------|
| **Name** | `local` |
| **Description** | Runs commands directly on the host OS. No isolation. |
| **Config key** | `terminal.backend: local` |
| **Requirements** | None |
| **Use case** | Trusted single-user environments, maximum performance |
| **Security** | No isolation — full host access |

**Config snippet**:
```yaml
terminal:
  backend: local
```

---

## 3. Docker Backend

| Property | Value |
|----------|-------|
| **Name** | `docker` |
| **Description** | Long-lived Docker container. Uses `docker exec` for command execution (NOT ephemeral `docker run`). Container stays running; commands execute inside it. |
| **Config key** | `terminal.backend: docker` |
| **Config keys** | `terminal.docker_image` (default: `nousresearch/hermes-agent:latest`) |
| **Requirements** | Docker installed, user in `docker` group or root |
| **Setup** | `hermes setup` → select Docker backend → pulls image |
| **Container lifecycle** | Started on first use, kept alive, stopped on `hermes stop` or host shutdown |

**Critical detail** [OFFICIAL]: The Docker backend uses a **long-lived container with `docker exec`**, not ephemeral `docker run` per command. This means:
- State persists between commands (working directory, env vars, processes)
- Faster command startup (no container creation overhead)
- Container must be explicitly stopped/restarted

**Config snippet**:
```yaml
terminal:
  backend: docker
  docker_image: "nousresearch/hermes-agent:latest"
```

**Docker image tags** [OFFICIAL]:
- `latest` — rolling latest
- `stable` — latest stable release
- `main` — main branch build
- `X.Y.Z` — specific version (e.g., `0.21.5`)

**Architecture**: `amd64`, `arm64` (multi-arch)

---

## 4. SSH Backend

| Property | Value |
|----------|-------|
| **Name** | `ssh` |
| **Description** | Executes commands on a remote host via SSH. |
| **Config key** | `terminal.backend: ssh` |
| **Config keys** | `terminal.ssh_host`, `terminal.ssh_user`, `terminal.ssh_port` (default 22), `terminal.ssh_key_path`, `terminal.ssh_passphrase` |
| **Requirements** | SSH key access to remote host, `ssh` client installed |
| **Auth** | Key-based (preferred) or password (via `sshpass`) |

**Config snippet**:
```yaml
terminal:
  backend: ssh
  ssh_host: "myserver.example.com"
  ssh_user: "deploy"
  ssh_port: 22
  ssh_key_path: "~/.ssh/id_ed25519"
  ssh_passphrase: ""  # if key is encrypted
```

**Connection reuse**: Uses SSH multiplexing (`ControlMaster`) for speed.

---

## 5. Singularity/Apptainer Backend

| Property | Value |
|----------|-------|
| **Name** | `singularity` |
| **Description** | Runs commands inside a Singularity/Apptainer container (`.sif` image). Used in HPC/cluster environments where Docker is not available. |
| **Config key** | `terminal.backend: singularity` |
| **Config keys** | `terminal.singularity_image` (path to `.sif` file) |
| **Requirements** | Apptainer/Singularity installed (`apptainer` or `singularity` in PATH) |
| **Image build** | `apptainer build hermes.sif docker://nousresearch/hermes-agent:latest` |

**Config snippet**:
```yaml
terminal:
  backend: singularity
  singularity_image: "/opt/containers/hermes-agent.sif"
```

**Note** [UNVERIFIED]: Exact runtime flags (bind mounts, `--cleanenv`, `--contain`) not documented. Check `apptainer exec --help` on your system.

---

## 6. Modal Backend

| Property | Value |
|----------|-------|
| **Name** | `modal` |
| **Description** | Runs commands in Modal.com serverless containers. Requires Modal account and CLI setup. |
| **Config key** | `terminal.backend: modal` |
| **Requirements** | `uv pip install modal`, `modal setup` (authenticates), Modal account |
| **Config keys** | `terminal.modal_app_name`, `terminal.modal_image` |

**Setup commands** [OFFICIAL]:
```bash
uv pip install modal
modal setup  # opens browser for auth
hermes config set terminal.backend modal
hermes config set terminal.modal_app_name "hermes-agent"
hermes config set terminal.modal_image "nousresearch/hermes-agent:latest"
```

**Config snippet**:
```yaml
terminal:
  backend: modal
  modal_app_name: "hermes-agent"
  modal_image: "nousresearch/hermes-agent:latest"
```

**Billing** [INFERRED]: Modal charges per-second for container runtime. Monitor costs.

---

## 7. Daytona Backend

| Property | Value |
|----------|-------|
| **Name** | `daytona` |
| **Description** | Runs commands in Daytona (daytona.io) workspace. |
| **Config key** | `terminal.backend: daytona` |
| **Config keys** | **NOT FETCHED** — setup keys undocumented |
| **Requirements** | Daytona account, Daytona CLI |
| **Status** | **UNVERIFIED** — config keys not captured in research |

**Setup (inferred)**:
```bash
# Daytona CLI install
curl -fsSL https://download.daytona.io/install.sh | bash
daytona auth  # login

# Config (keys UNVERIFIED)
hermes config set terminal.backend daytona
# hermes config set terminal.daytona_workspace_id "..."  # UNVERIFIED
# hermes config set terminal.daytona_project_id "..."    # UNVERIFIED
```

---

## 8. Vercel Sandbox Backend

| Property | Value |
|----------|-------|
| **Name** | `vercel_sandbox` |
| **Description** | Runs commands in Vercel Sandbox (secure, isolated VMs). |
| **Config key** | `terminal.backend: vercel_sandbox` |
| **Requirements** | `pip install 'hermes-agent[vercel]'`, Vercel account, project, team |
| **Env vars required** | `VERCEL_TOKEN`, `VERCEL_PROJECT_ID`, `VERCEL_TEAM_ID` |

**Install command** [OFFICIAL]:
```bash
pip install 'hermes-agent[vercel]'
```

**Config snippet**:
```yaml
terminal:
  backend: vercel_sandbox
```

**Env vars** (in `~/.hermes/.env`):
```bash
VERCEL_TOKEN="vercel_xxx"
VERCEL_PROJECT_ID="prj_xxx"
VERCEL_TEAM_ID="team_xxx"
```

**Billing** [INFERRED]: Vercel Sandbox charges by compute time.

---

## 9. Decision Table

| Criterion | `local` | `docker` | `ssh` | `singularity` | `modal` | `daytona` | `vercel_sandbox` |
|-----------|---------|----------|-------|---------------|---------|-----------|------------------|
| **Isolation** | None | Container | Remote host | Container | Serverless | Workspace | VM |
| **Setup complexity** | None | Low (Docker) | Medium (SSH keys) | Medium (Apptainer) | Medium (Modal CLI) | High (Daytona) | Medium (Vercel) |
| **Latency** | Lowest | Low | Network-dependent | Low | Cold-start ~2s | Network-dependent | Cold-start ~2s |
| **Persistence** | Full host | Container FS | Remote host FS | Container FS | Ephemeral (per call) | Workspace FS | Ephemeral (per call) |
| **Cost** | Free | Host resources | Remote host | Host resources | Per-second | Subscription | Per-compute |
| **HPC/Cluster** | No | No | Yes | **Yes** | No | No | No |
| **Rootless** | N/A | Yes (rootless mode) | N/A | Yes | N/A | N/A | N/A |
| **GPU support** | Host | Via `--gpus all` | Remote | Via `--nv` | Yes (Modal GPU) | Yes | Limited |
| **Best for** | Dev, trusted | Prod isolation, CI | Remote servers | HPC clusters | Burst workloads | Team workspaces | Web sandboxing |

---

## 10. Host ↔ Sandbox File Transfer

**Docker backend** [OFFICIAL]:
```bash
# Copy file TO container
docker cp /host/path container_name:/container/path

# Copy file FROM container
docker cp container_name:/container/path /host/path

# Or use bind mounts in container config (persistent)
```

**SSH backend** [OFFICIAL]:
```bash
# scp / rsync
scp /host/path user@host:/remote/path
rsync -avz /host/path user@host:/remote/path
```

**Modal backend** [INFERRED]:
- Modal provides `modal volume` for persistent storage
- `modal run` can mount local dirs with `--mount`

**Vercel Sandbox** [INFERRED]:
- Sandbox is ephemeral; use Vercel Blob or external storage for persistence

**Singularity** [OFFICIAL]:
```bash
# Bind mount at runtime
apptainer exec --bind /host/path:/container/path image.sif command

# Or configure in definition file
```

**Daytona** [UNVERIFIED]: Daytona workspace has persistent `/workspace` directory.

---

## 11. Docker Hardening Flags

These flags can be added to the container create/run command (via `hermes config set terminal.docker_extra_args` or Docker daemon config):

| Flag | Purpose |
|------|---------|
| `--read-only` | Root filesystem read-only |
| `--cap-drop=ALL` | Drop all Linux capabilities |
| `--cap-add=CAP_DAC_OVERRIDE` | Add back only needed caps |
| `--security-opt=no-new-privileges:true` | Prevent privilege escalation |
| `--pids-limit=100` | Limit processes |
| `--memory=2g` | Memory limit |
| `--cpus=2` | CPU limit |
| `--network=none` | No network (or `--network=host` for host net) |
| `--tmpfs /tmp:noexec,nosuid,size=100m` | Secure /tmp |
| `--user 1000:1000` | Run as non-root user |

**Example hardened config**:
```yaml
terminal:
  backend: docker
  docker_image: "nousresearch/hermes-agent:latest"
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

---

## 12. Network Restrictions

**NOT FOUND AS BUILT-IN CONFIG KEY** [INFERRED]: Hermes does not have a `terminal.network_mode` or `terminal.allowed_destinations` config key. To restrict network access:

1. **Docker**: Use `--network=none` or custom bridge with iptables rules
2. **Host**: Host-level firewall (ufw, nftables, iptables)
3. **SSH**: Remote host firewall
4. **Modal/Vercel**: Provider-level network policies
5. **Singularity**: `--network=none` flag (Apptainer 1.2+)

**Recommendation**: Apply network restrictions at the infrastructure layer, not via Hermes config.

---

## 13. Conflicts

| # | Conflict | Resolution |
|---|----------|------------|
| 1 | Phase 1: "Docker backend uses ephemeral containers" | **Phase 3 corrects**: Long-lived container with `docker exec` |
| 2 | Daytona config keys not documented | Mark UNVERIFIED; user must discover via `daytona --help` |
| 3 | Singularity runtime flags not documented | Mark UNVERIFIED; check `apptainer exec --help` |
| 4 | Network restriction config key not found | Document as gap; use infrastructure-level controls |
| 5 | GPU support flags per backend not fully documented | Mark UNVERIFIED; infer from backend docs |

---

## 14. Gaps

1. Daytona backend: complete config keys, auth flow, workspace lifecycle
2. Singularity: exact `apptainer exec` flags used by Hermes
3. Modal: `modal_app_name` and `modal_image` config key names (inferred)
4. Vercel Sandbox: exact config key names (inferred from env vars)
5. Per-backend timeout configuration (`terminal.timeout_seconds`?)
6. Whether `terminal.backend` can be set per-profile (profiles have own config.yaml)
7. Container health check / auto-restart behavior
8. Resource limits (memory, CPU) config keys per backend

---

## 15. Sources

- https://hermes-agent.nousresearch.com/docs/reference/terminal-backends
- https://hermes-agent.nousresearch.com/docs/user-guide/features/terminal
- https://hermes-agent.nousresearch.com/docs/llms.txt
- Phase 3 research Sections 2, 4, 6, 7

---

**FILE COMPLETE: references/08-terminal-backends.md** — 7 backends with config keys, setup commands, decision table, file transfer, hardening flags, network restrictions.