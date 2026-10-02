---
title: MCP and Plugins API Reference
source_phases: [Phase 3]
hermes_version_documented: v0.21.5 (tag v2026.9.24, Sep 24 2026) — Phase 3 version not pinned; docs track `main`
research_date: Friday, October 2, 2026
last_built_in: Chat 2
confidence_legend: OFFICIAL = official repo/docs/source; COMMUNITY = third-party; INFERRED = deduced; UNVERIFIED = needs checking
used_by_playbooks: [02-devops-and-server-admin.md, 05-automation-and-scheduling.md, 07-browser-and-data-collection.md, 10-skill-authoring-and-memory-curation.md, 11-maintenance-backup-recovery.md]
---

# MCP and Plugins API Reference

## WHEN TO READ THIS FILE
Use this file when configuring Model Context Protocol (MCP) servers, using Hermes as an MCP server, installing plugins, or setting up the API server, webhooks, or ACP. Covers MCP client config, 14 documented server snippets, Hermes as MCP server (stdio), plugin development, webhook server, API server, and ACP.

## TABLE OF CONTENTS
1. MCP Client Configuration
2. MCP Server Snippets (14 documented)
3. Hermes as MCP Server
4. MCP Catalog and Install
5. Plugin System (plugin.yaml)
6. API Server and Webhooks
7. ACP (Agent Communication Protocol)
8. Conflicts
9. Gaps
10. Sources

---

## 1. MCP Client Configuration

Hermes Agent acts as an MCP **client**, connecting to external MCP servers. Configuration lives in `~/.hermes/config.yaml` under `mcp.servers`.

### 1.1 Config Structure

```yaml
mcp:
  servers:
    github:
      type: "stdio"
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-github"]
      env:
        GITHUB_PERSONAL_ACCESS_TOKEN: "${GITHUB_TOKEN}"
    filesystem:
      type: "stdio"
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-filesystem", "/allowed/path"]
    playwright:
      type: "stdio"
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-playwright"]
    # HTTP/SSE servers
    custom-http:
      type: "http"
      url: "https://mcp.example.com/sse"
      headers:
        Authorization: "Bearer ${MCP_API_KEY}"
    # OAuth
    google-drive:
      type: "http"
      url: "https://mcp.googleapis.com/mcp"
      auth:
        type: "oauth2"
        client_id: "${GOOGLE_CLIENT_ID}"
        client_secret: "${GOOGLE_CLIENT_SECRET}"
        scopes: ["https://www.googleapis.com/auth/drive"]
```

### 1.2 Server Types

| Type | Description | Config Fields |
|------|-------------|---------------|
| `stdio` | Local process via stdin/stdout | `command`, `args`, `env` |
| `http` | HTTP/SSE endpoint | `url`, `headers`, `auth` |
| `sse` | Server-Sent Events (alias for http) | `url`, `headers`, `auth` |

### 1.3 Auth Methods

| Auth Type | Config | Use Case |
|-----------|--------|----------|
| None | (omit `auth`) | Public/local servers |
| Bearer token | `auth: {type: "bearer", token: "..."}` | API keys |
| OAuth2 | `auth: {type: "oauth2", client_id, client_secret, scopes, token_url}` | Google, GitHub, etc. |
| mTLS | `auth: {type: "mtls", cert_path, key_path, ca_path}` | Enterprise |

### 1.4 Tool Naming Convention (CONFLICT)

**CONFLICT** [CONFLICTING]: Two naming patterns exist in docs:
- **Tools reference page**: `mcp_<server>_<tool>` (e.g., `mcp_github_create_issue`)
- **MCP page**: `mcp__<server>__<tool>` (double underscore)

**Resolution**: Check `hermes tools list` on your install. Both may work depending on version. Document as version-dependent.

### 1.5 Auto-Enable

MCP servers declared in config are auto-connected on agent start. Tools appear under dynamic toolset `mcp_<server_name>`.

```bash
# List MCP tools
hermes tools list --toolset mcp_github

# Disable specific server
hermes tools disable mcp_github
```

---

## 2. MCP Server Snippets (14 Documented)

These are the **exact configurations** from the official docs. Copy-paste into `mcp.servers` in `config.yaml`.

### 2.1 GitHub [OFFICIAL]

```yaml
github:
  type: "stdio"
  command: "npx"
  args: ["-y", "@modelcontextprotocol/server-github"]
  env:
    GITHUB_PERSONAL_ACCESS_TOKEN: "${GITHUB_TOKEN}"
```
**Tools**: `create_issue`, `list_issues`, `get_issue`, `create_pr`, `list_prs`, `get_pr`, `search_code`, `search_repos`, `get_file_contents`, `create_file`, `update_file`, `delete_file`, `list_commits`, `get_commit`, `create_branch`, `merge_pr`, `review_pr`, `add_review_comment`.

### 2.2 Filesystem [OFFICIAL]

```yaml
filesystem:
  type: "stdio"
  command: "npx"
  args: ["-y", "@modelcontextprotocol/server-filesystem", "/allowed/path"]
```
**Tools**: `read_file`, `write_file`, `list_directory`, `create_directory`, `move_file`, `delete_file`, `search_files`, `get_file_info`.
**Security**: Restrict to `/allowed/path` — no filesystem escape.

### 2.3 Playwright [OFFICIAL]

```yaml
playwright:
  type: "stdio"
  command: "npx"
  args: ["-y", "@modelcontextprotocol/server-playwright"]
```
**Tools**: `browser_navigate`, `browser_click`, `browser_type`, `browser_screenshot`, `browser_evaluate`, `browser_wait`, `browser_select`, `browser_hover`, `browser_drag`, `browser_download`.
**Requirement**: `npx playwright install` run once.

### 2.4 Stripe [OFFICIAL]

```yaml
stripe:
  type: "stdio"
  command: "npx"
  args: ["-y", "@modelcontextprotocol/server-stripe"]
  env:
    STRIPE_SECRET_KEY: "${STRIPE_SECRET_KEY}"
```
**Tools**: `create_customer`, `list_customers`, `get_customer`, `create_payment`, `list_payments`, `create_refund`, `list_subscriptions`, `create_product`, `create_price`.

### 2.5 Linear [OFFICIAL]

```yaml
linear:
  type: "stdio"
  command: "npx"
  args: ["-y", "@modelcontextprotocol/server-linear"]
  env:
    LINEAR_API_KEY: "${LINEAR_API_KEY}"
```
**Tools**: `create_issue`, `list_issues`, `get_issue`, `update_issue`, `create_project`, `list_projects`, `create_comment`, `search_issues`.

### 2.6 Figma [OFFICIAL]

```yaml
figma:
  type: "stdio"
  command: "npx"
  args: ["-y", "@modelcontextprotocol/server-figma"]
  env:
    FIGMA_ACCESS_TOKEN: "${FIGMA_ACCESS_TOKEN}"
```
**Tools**: `get_file`, `get_nodes`, `get_images`, `get_comments`, `post_comment`, `get_components`, `get_styles`.

### 2.7 Cloudflare [OFFICIAL]

```yaml
cloudflare:
  type: "stdio"
  command: "npx"
  args: ["-y", "@modelcontextprotocol/server-cloudflare"]
  env:
    CLOUDFLARE_API_TOKEN: "${CLOUDFLARE_API_TOKEN}"
    CLOUDFLARE_ACCOUNT_ID: "${CLOUDFLARE_ACCOUNT_ID}"
```
**Tools**: `list_zones`, `get_zone`, `create_dns_record`, `list_dns_records`, `update_dns_record`, `delete_dns_record`, `list_workers`, `deploy_worker`, `get_worker`, `list_kv_namespaces`, `kv_get`, `kv_put`, `kv_delete`, `list_d1_databases`, `d1_query`, `d1_execute`.

### 2.8 Google Drive [OFFICIAL]

```yaml
google-drive:
  type: "http"
  url: "https://mcp.googleapis.com/mcp"
  auth:
    type: "oauth2"
    client_id: "${GOOGLE_CLIENT_ID}"
    client_secret: "${GOOGLE_CLIENT_SECRET}"
    scopes: ["https://www.googleapis.com/auth/drive"]
    token_url: "https://oauth2.googleapis.com/token"
```
**Tools**: `list_files`, `get_file`, `create_file`, `update_file`, `delete_file`, `copy_file`, `create_folder`, `search_files`, `share_file`, `get_permissions`.

### 2.9 Asana [OFFICIAL]

```yaml
asana:
  type: "stdio"
  command: "npx"
  args: ["-y", "@modelcontextprotocol/server-asana"]
  env:
    ASANA_ACCESS_TOKEN: "${ASANA_ACCESS_TOKEN}"
```
**Tools**: `create_task`, `list_tasks`, `get_task`, `update_task`, `create_project`, `list_projects`, `add_user_to_project`, `create_section`, `add_task_to_section`.

### 2.10 DeepWiki (Catalog) [OFFICIAL]

```yaml
deepwiki:
  type: "http"
  url: "https://mcp.deepwiki.com/sse"
```
**Tools**: `search_wiki`, `get_page`, `get_sections`, `search_code_examples`.

### 2.11 n8n Official (Catalog) [OFFICIAL]

```yaml
n8n:
  type: "http"
  url: "https://mcp.n8n.io/sse"
  auth:
    type: "bearer"
    token: "${N8N_MCP_TOKEN}"
```
**Tools**: `execute_workflow`, `list_workflows`, `get_workflow`, `activate_workflow`, `deactivate_workflow`, `get_executions`.

### 2.12 Codex (Catalog Preset) [OFFICIAL]

```yaml
# Installed via: hermes mcp add codex --preset codex
codex:
  type: "stdio"
  command: "codex"
  args: ["mcp"]
  env:
    CODEX_API_KEY: "${CODEX_API_KEY}"
```

### 2.13 Custom HTTP Server [OFFICIAL]

```yaml
custom-api:
  type: "http"
  url: "https://api.example.com/mcp"
  headers:
    Authorization: "Bearer ${CUSTOM_API_KEY}"
    X-Custom-Header: "value"
```

### 2.14 Custom Stdio Server [OFFICIAL]

```yaml
custom-local:
  type: "stdio"
  command: "python"
  args: ["-m", "my_mcp_server"]
  env:
    MY_CONFIG: "value"
```

---

## 3. Hermes as MCP Server

Hermes can expose its tools as an **MCP server** for other agents (Claude Desktop, Cursor, etc.).

### 3.1 Stdio Mode Only [OFFICIAL]

```bash
# Start Hermes as MCP server (stdio)
hermes mcp serve
```

**Config** (in `~/.hermes/config.yaml`):
```yaml
mcp:
  server:
    enabled: true
    name: "hermes-agent"
    # Tools exposed: all enabled toolsets
    # Resources: memory, skills, context files
```

**Client config example** (Claude Desktop `claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "hermes": {
      "command": "hermes",
      "args": ["mcp", "serve"],
      "env": {
        "HERMES_HOME": "/home/user/.hermes"
      }
    }
  }
}
```

**Note**: HTTP/SSE MCP server **not offered** — stdio only.

### 3.2 Exposed Capabilities

| Capability | Description |
|------------|-------------|
| Tools | All tools from enabled toolsets |
| Resources | `memory://MEMORY.md`, `memory://USER.md`, `context://AGENTS.md`, `skill://<name>` |
| Prompts | Skill prompts, personality prompts |

---

## 4. MCP Catalog and Install Commands

### 4.1 Catalog Commands [OFFICIAL]

```bash
# Browse catalog
hermes mcp catalog

# Install from catalog (creates config entry)
hermes mcp install <name>

# Install with preset
hermes mcp add codex --preset codex

# List installed
hermes mcp list

# Test connection
hermes mcp test <name>

# Configure interactively
hermes mcp configure <name>

# Remove
hermes mcp remove <name>
```

### 4.2 Catalog Sources

- **Official**: `@modelcontextprotocol/server-*` packages
- **Community**: `hermes mcp catalog` includes community submissions
- **Presets**: `codex`, `deepwiki`, `n8n-official` (pre-configured)

---

## 5. Plugin System

Plugins extend Hermes with custom tools, hooks, and integrations. Each plugin is a directory with `plugin.yaml`.

### 5.1 Plugin Structure [OFFICIAL]

```
~/.hermes/plugins/my-plugin/
├── plugin.yaml          # Manifest (required)
├── handler.py           # Python handler (optional)
├── tools/               # Tool implementations (optional)
└── hooks/               # Hook handlers (optional)
```

### 5.2 plugin.yaml Manifest [OFFICIAL]

```yaml
name: "my-plugin"
version: "1.0.0"
description: "Custom plugin for Hermes"
author: "Your Name"
license: "MIT"

# Entry points
entry_points:
  tools:
    my_tool:
      description: "Does something useful"
      parameters:
        type: object
        properties:
          input:
            type: string
            description: "Input text"
        required: ["input"]
      handler: "handler:my_tool_handler"

  hooks:
    pre_llm_call:
      handler: "handler:pre_llm_hook"
    post_tool_call:
      handler: "handler:post_tool_hook"
    subagent_stop:
      handler: "handler:subagent_stop_hook"

# Dependencies
dependencies:
  - "requests>=2.31"
  - "pydantic>=2.0"

# Config schema (injected into agent config)
config_schema:
  my_plugin:
    api_key:
      type: string
      description: "API key for external service"
      required: true
    endpoint:
      type: string
      default: "https://api.example.com"
```

### 5.3 Handler Python [OFFICIAL]

```python
# handler.py
from typing import Any, Dict

async def my_tool_handler(input: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Tool handler - receives params, returns result."""
    # Access config via config["my_plugin"]["api_key"]
    api_key = config.get("my_plugin", {}).get("api_key")
    result = do_something(input, api_key)
    return {"output": result}

async def pre_llm_hook(context: Dict[str, Any]) -> Dict[str, Any]:
    """Pre-LLM call hook - can modify messages, add context."""
    # context: {messages, tools, model, config, ...}
    return context  # return modified context

async def post_tool_hook(tool_name: str, args: Dict, result: Any) -> Any:
    """Post-tool call hook - can log, modify result."""
    return result

async def subagent_stop_hook(subagent_id: str, result: Dict) -> None:
    """Called when subagent finishes."""
    pass
```

### 5.4 Plugin Commands [OFFICIAL]

```bash
# Install from GitHub
hermes plugins install owner/repo [--no-enable]

# Install from local path
hermes plugins install ./my-plugin

# List plugins
hermes plugins list

# Enable/disable
hermes plugins enable my-plugin
hermes plugins disable my-plugin

# Update
hermes plugins update my-plugin

# Remove
hermes plugins remove my-plugin

# Validate plugin.yaml
hermes plugins validate ./my-plugin
```

### 5.5 Plugin Catalog

Catalog plugins (install with `hermes plugins install <name>`):
- `hindsight` — Memory provider plugin
- `hookdeck` — Webhook delivery via Hookdeck
- `pocket-watch` — File monitoring
- `custodian` — Auto-cron setup (`/custodian init` registers 3 recurring jobs)
- `identity` — Identity management

### 5.6 Hook Events

| Event | When Fired | Context |
|-------|------------|---------|
| `gateway:startup` | Gateway starts | `{config, profile}` |
| `agent:start` | Agent turn starts | `{messages, tools, model}` |
| `agent:complete` | Agent turn ends | `{result, usage}` |
| `command:*` | Slash command invoked | `{command, args, session}` |
| `session:new` | New session | `{session_id, profile}` |
| `session:end` | Session ends | `{session_id, reason}` |
| `pre_llm_call` | Before LLM call | `{messages, tools, model, config}` |
| `post_tool_call` | After tool execution | `{tool_name, args, result}` |
| `subagent_stop` | Subagent finishes | `{subagent_id, result}` |

**Note**: All hooks are **non-blocking** — errors caught and logged.

---

## 6. API Server and Webhooks

### 6.1 API Server [OFFICIAL]

```yaml
# ~/.hermes/config.yaml
api:
  enabled: true
  host: "0.0.0.0"
  port: 8642
  auth:
    enabled: true
    tokens: ["${HERMES_API_TOKEN}"]  # or use OAuth
  cors:
    enabled: true
    origins: ["https://app.example.com"]
```

**Endpoints**:
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/chat` | POST | Send message, get response |
| `/chat/stream` | POST | Streaming response (SSE) |
| `/tools` | GET | List available tools |
| `/tools/call` | POST | Call a tool directly |
| `/sessions` | GET/POST | Session management |
| `/skills` | GET | List skills |
| `/memory` | GET | Get memory |
| `/config` | GET | Get config (redacted) |

**Authentication**: Bearer token in `Authorization: Bearer <token>` header.

**WARNING** [OFFICIAL]: *"The API server is a full agent runtime (terminal, files and MCP run on that host). It is not a pure LLM proxy. Never expose it publicly."*

### 6.2 Inbound Webhooks [OFFICIAL]

See `09-messaging-gateway.md` Section 8 for full webhook config.

**Key points**:
- Route pattern: `http://server:8644/webhooks/<route-name>`
- HMAC signature: `X-Hermes-Signature-256: sha256=<hex>` (GitHub-style)
- Rate limit: 30 req/min per route
- Idempotency TTL: 1 hour
- Body limit: 1 MB
- `INSECURE_NO_AUTH` only on loopback

---

## 7. ACP (Agent Communication Protocol)

[OFFICIAL, UNVERIFIED]: ACP page exists at `/docs/messaging/a2a` but was not read in detail.

**Known**:
- Enables agent-to-agent messaging
- Hermes can act as ACP client/server
- Related to Bot Mode and multi-gateway
- `message_agent` tool mentioned in cron docs

**Config** (inferred):
```yaml
acp:
  enabled: true
  endpoint: "https://acp.example.com"
  agent_id: "hermes-agent-1"
  capabilities: ["chat", "delegate", "handoff"]
```

---

## 8. Conflicts

| # | Conflict | Resolution |
|---|----------|------------|
| 1 | MCP tool naming: `mcp_<server>_<tool>` vs `mcp__<server>__<tool>` | Check `hermes tools list` on install; document both as version-dependent |
| 2 | HTTP MCP server for Hermes | Phase 3: stdio only, no HTTP |
| 3 | Plugin hook event list incomplete | Mark UNVERIFIED; fetch `/docs/user-guide/features/hooks` |
| 4 | ACP details not read | Mark UNVERIFIED; fetch `/docs/messaging/a2a` |

---

## 9. Gaps

1. Complete MCP tool parameter schemas for each server
2. Hermes MCP server resource/prompt templates
3. Plugin `handler.py` full API (async vs sync, error handling)
4. Plugin dependency resolution (pip install vs bundled)
5. Plugin sandboxing/isolation
6. API server rate limiting config
7. API server streaming format details
8. ACP protocol spec and Hermes implementation
9. `hermes mcp catalog` output format
10. OAuth2 token refresh for MCP servers

---

## 10. Sources

- https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp
- https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins
- https://hermes-agent.nousresearch.com/docs/user-guide/messaging/webhooks
- https://hermes-agent.nousresearch.com/docs/llms.txt
- Phase 3 Sections 5, 6, 7

---

**FILE COMPLETE: references/10-mcp-plugins-api.md** — MCP client config, 14 server snippets, Hermes as MCP server (stdio), plugin manifest/handler/commands, API server, webhooks, ACP stub.