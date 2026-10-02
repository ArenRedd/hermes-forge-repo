---
title: Messaging Gateway Reference
source_phases: [Phase 3, Phase 4]
hermes_version_documented: v0.21.5 (tag v2026.9.24, Sep 24 2026) — Phase 3/4 version not pinned; docs track `main`
research_date: Friday, October 2, 2026
last_built_in: Chat 2
confidence_legend: OFFICIAL = official repo/docs/source; COMMUNITY = third-party; INFERRED = deduced; UNVERIFIED = needs checking
used_by_playbooks: [06-messaging-gateway-setups.md, 08-multi-agent-and-parallel.md, 09-personal-productivity.md, 11-maintenance-backup-recovery.md]
---

# Messaging Gateway Reference

## WHEN TO READ THIS FILE
Use this file when setting up Hermes Agent to receive and send messages via Telegram, Discord, Slack, WhatsApp, Signal, Matrix, Mattermost, ntfy, Email, SMS, and 15+ other platforms. Covers platform configs, gateway commands, session policies, delivery targets, allowlists, security, and the critical session reset behavior change.

## TABLE OF CONTENTS
1. Gateway Architecture and Installation
2. Platform Configurations (28 platforms)
3. Gateway Commands
4. Session Management and Reset Policy (CRITICAL CHANGE)
5. Delivery Targets and Formats
6. Allowlists and Security
6. Cross-Platform Continuity
7. Webhooks and Inbound Events
8. Bot Mode and Profiles
9. Conflicts
10. Gaps
11. Sources

---

## 1. Gateway Architecture and Installation

**Gateway** is the long-running daemon that connects Hermes Agent to messaging platforms. It ticks every 60 seconds, runs cron jobs, handles webhooks, and manages platform connections.

### Installation (VPS / Production) [OFFICIAL]

```bash
# User service (recommended for VPS)
hermes gateway install
sudo loginctl enable-linger $USER   # REQUIRED for cron to survive logout
hermes gateway start

# System service (alternative)
sudo hermes gateway install --system
sudo systemctl enable --now hermes-gateway
```

### Service Management

```bash
hermes gateway start|stop|restart|status
hermes gateway logs [-f] [--lines N]
hermes gateway doctor       # health check
```

### Config Keys (gateway section)

```yaml
gateway:
  enabled: true
  port: 9119           # Dashboard port (also API port 8642)
  host: "0.0.0.0"      # Bind address
  multiplex_profiles: false   # Multi-profile gateway (see Bot Mode)
  # Per-platform config under platforms.<name>:
```

### Dashboard and API

| Service | Port | Auth Required |
|---------|------|---------------|
| Dashboard (Web UI) | 9119 | Yes (non-loopback) |
| API Server | 8642 | Yes (non-loopback) |

**WARNING** [OFFICIAL]: *"The API server is a full agent runtime (terminal, files and MCP run on that host). It is not a pure LLM proxy. Never expose it publicly."*

---

## 2. Platform Configurations (28 Platforms)

Each platform is configured under `platforms.<name>` in `~/.hermes/config.yaml`. Credentials go in `~/.hermes/.env`.

### 2.1 Telegram [OFFICIAL]

```yaml
platforms:
  telegram:
    enabled: true
    extra:
      bot_token: "${HERMES_TELEGRAM_BOT_TOKEN}"
      chat_id: "${HERMES_TELEGRAM_CHAT_ID}"          # optional default
      admin_chat_ids: ["${HERMES_TELEGRAM_ADMIN_ID}"] # optional allowlist
      parse_mode: "MarkdownV2"                        # or "HTML", "None"
      webhook_url: ""                                 # set for webhook mode
      webhook_secret: ""                              # secret for webhook validation
      allowed_updates: ["message", "callback_query"]  # limit update types
```

**Env vars** (`~/.hermes/.env`):
```bash
HERMES_TELEGRAM_BOT_TOKEN="123456:ABC-DEF..."
HERMES_TELEGRAM_CHAT_ID="-1001234567890"
HERMES_TELEGRAM_ADMIN_ID="123456789"
```

**Limits**: 4096 chars per message (auto-split). Media: photo, document, video, audio, voice, sticker.

**Commands**: `/start`, `/help`, `/skills`, `/model`, `/toolset`, `/cron`, `/memory`, `/personality`, `/checkpoint`, `/rollback`, `/goal`, `/review`, `/refine`, `/journey`, `/plan`, `/learn`, `/compress`, `/usage`, `/insights`, `/topup`, `/stop`, `/new`, `/undo`, `/retry`, `/branch`, `/fork`, `/steer`, `/queue`, `/background`, `/diff`, `/agents`, `/tasks`, `/approve`, `/deny`, `/fast`, `/personality`, `/bundles`, `/bundles list`, `/bundles show`, `/bundles delete`, `/cron add`, `/cron list`, `/cron pause`, `/cron resume`, `/cron run`, `/cron remove`, `/cron edit`, `/cron status`, `/cron doctor`, `/cron tick`, `/cron runs`, `/cron incidents`.

### 2.2 Discord [OFFICIAL]

```yaml
platforms:
  discord:
    enabled: true
    extra:
      bot_token: "${DISCORD_BOT_TOKEN}"
      channel_id: "${DISCORD_CHANNEL_ID}"       # default channel
      guild_id: "${DISCORD_GUILD_ID}"           # optional
      app_id: "${DISCORD_APP_ID}"               # for slash commands
      public_key: "${DISCORD_PUBLIC_KEY}"       # for interaction verification
      use_threads: true
      thread_name_template: "Hermes - {user}"
```

**Env vars**:
```bash
DISCORD_BOT_TOKEN="Bot xxxxx..."
DISCORD_CHANNEL_ID="123456789012345678"
DISCORD_GUILD_ID="123456789012345678"
DISCORD_APP_ID="123456789012345678"
DISCORD_PUBLIC_KEY="xxxx..."
```

**Features**: Embeds, threads, slash commands, components (buttons, selects).

### 2.3 Slack [OFFICIAL]

```yaml
platforms:
  slack:
    enabled: true
    extra:
      bot_token: "${SLACK_BOT_TOKEN}"           # xoxb-...
      signing_secret: "${SLACK_SIGNING_SECRET}"
      app_token: "${SLACK_APP_TOKEN}"           # xapp-... for Socket Mode
      default_channel: "${SLACK_DEFAULT_CHANNEL}"
      use_threads: true
      socket_mode: true                         # recommended
```

**Env vars**:
```bash
SLACK_BOT_TOKEN="xoxb-xxxxx"
SLACK_SIGNING_SECRET="xxxxx"
SLACK_APP_TOKEN="xapp-xxxxx"
SLACK_DEFAULT_CHANNEL="C1234567890"
```

**Modes**: Socket Mode (recommended, no public URL) or HTTP webhook.

### 2.4 WhatsApp Business [OFFICIAL]

```yaml
platforms:
  whatsapp:
    enabled: true
    extra:
      access_token: "${WHATSAPP_ACCESS_TOKEN}"
      phone_number_id: "${WHATSAPP_PHONE_NUMBER_ID}"
      verify_token: "${WHATSAPP_VERIFY_TOKEN}"
      app_secret: "${WHATSAPP_APP_SECRET}"
      webhook_url: "https://your-domain.com/webhooks/whatsapp"
```

**Env vars**:
```bash
WHATSAPP_ACCESS_TOKEN="EAA..."
WHATSAPP_PHONE_NUMBER_ID="123456789"
WHATSAPP_VERIFY_TOKEN="your-verify-token"
WHATSAPP_APP_SECRET="xxxxx"
```

**Requirement**: Meta Business account, approved phone number.

### 2.5 Signal [OFFICIAL]

```yaml
platforms:
  signal:
    enabled: true
    extra:
      cli_config: "${SIGNAL_CLI_CONFIG}"        # path to signal-cli config dir
      phone_number: "${SIGNAL_PHONE_NUMBER}"    # +1xxxxxxxxxx
      group_id: "${SIGNAL_GROUP_ID}"            # optional
      attachment_dir: "/tmp/signal-attachments"
```

**Env vars**:
```bash
SIGNAL_CLI_CONFIG="/home/user/.local/share/signal-cli"
SIGNAL_PHONE_NUMBER="+15551234567"
SIGNAL_GROUP_ID="xxxx..."
```

**Requirement**: `signal-cli` installed and registered (`signal-cli -u +1... register`, `verify`).

### 2.6 Matrix [OFFICIAL]

```yaml
platforms:
  matrix:
    enabled: true
    extra:
      homeserver: "${MATRIX_HOMESERVER}"        # https://matrix.org
      user_id: "${MATRIX_USER_ID}"              # @user:matrix.org
      access_token: "${MATRIX_ACCESS_TOKEN}"
      device_id: "${MATRIX_DEVICE_ID}"          # optional
      room_id: "${MATRIX_ROOM_ID}"              # default room
      encryption: true                          # E2EE (requires crypto lib)
      verification_method: "emoji"              # or "qr"
```

**Env vars**:
```bash
MATRIX_HOMESERVER="https://matrix.org"
MATRIX_USER_ID="@hermes:matrix.org"
MATRIX_ACCESS_TOKEN="syt_xxxxx"
MATRIX_DEVICE_id="XXXXX"
MATRIX_ROOM_ID="!xxxx:matrix.org"
```

### 2.7 Mattermost [OFFICIAL]

```yaml
platforms:
  mattermost:
    enabled: true
    extra:
      url: "${MATTERMOST_URL}"                  # https://mattermost.example.com
      token: "${MATTERMOST_TOKEN}"              # personal access token
      team: "${MATTERMOST_TEAM}"                # team name
      channel: "${MATTERMOST_CHANNEL}"          # default channel
      websocket: true
```

**Env vars**:
```bash
MATTERMOST_URL="https://chat.example.com"
MATTERMOST_TOKEN="xxxx..."
MATTERMOST_TEAM="engineering"
MATTERMOST_CHANNEL="general"
```

### 2.8 ntfy [OFFICIAL]

```yaml
platforms:
  ntfy:
    enabled: true
    extra:
      topic: "${NTFY_TOPIC}"                    # hermes-alerts
      server: "${NTFY_SERVER}"                  # https://ntfy.sh (or self-hosted)
      auth_token: "${NTFY_AUTH_TOKEN}"          # optional
      priority: "default"                       # min, low, default, high, urgent
      tags: ["hermes", "alert"]
```

**Env vars**:
```bash
NTFY_TOPIC="hermes-alerts"
NTFY_SERVER="https://ntfy.sh"
NTFY_AUTH_TOKEN="tk_xxxxx"
```

### 2.9 Email [OFFICIAL]

```yaml
platforms:
  email:
    enabled: true
    extra:
      smtp_host: "${SMTP_HOST}"
      smtp_port: 587
      smtp_user: "${SMTP_USER}"
      smtp_pass: "${SMTP_PASS}"
      smtp_tls: true
      imap_host: "${IMAP_HOST}"
      imap_port: 993
      imap_user: "${IMAP_USER}"
      imap_pass: "${IMAP_PASS}"
      from_address: "${EMAIL_FROM}"
      to_addresses: ["${EMAIL_TO}"]
      use_oauth2: false
```

**Env vars**:
```bash
SMTP_HOST="smtp.gmail.com"
SMTP_PORT="587"
SMTP_USER="user@gmail.com"
SMTP_PASS="app-password"
IMAP_HOST="imap.gmail.com"
IMAP_PORT="993"
IMAP_USER="user@gmail.com"
IMAP_PASS="app-password"
EMAIL_FROM="Hermes Agent <hermes@example.com>"
EMAIL_TO="user@example.com"
```

### 2.10 SMS (Twilio) [OFFICIAL]

```yaml
platforms:
  sms:
    enabled: true
    extra:
      account_sid: "${TWILIO_ACCOUNT_SID}"
      auth_token: "${TWILIO_AUTH_TOKEN}"
      from_number: "${TWILIO_FROM}"             # +15551234567
      to_numbers: ["${TWILIO_TO}"]
      messaging_service_sid: ""                 # optional
```

**Env vars**:
```bash
TWILIO_ACCOUNT_SID="ACxxxx..."
TWILIO_AUTH_TOKEN="xxxx..."
TWILIO_FROM="+15551234567"
TWILIO_TO="+15559876543"
```

### 2.11 Facebook Messenger [OFFICIAL]

```yaml
platforms:
  messenger:
    enabled: true
    extra:
      page_token: "${MESSENGER_PAGE_TOKEN}"
      verify_token: "${MESSENGER_VERIFY_TOKEN}"
      app_secret: "${MESSENGER_APP_SECRET}"
      webhook_url: "https://your-domain.com/webhooks/messenger"
```

### 2.12 IRC [OFFICIAL]

```yaml
platforms:
  irc:
    enabled: true
    extra:
      server: "${IRC_SERVER}"                   # irc.libera.chat
      port: 6697
      tls: true
      nick: "${IRC_NICK}"
      password: "${IRC_PASSWORD}"               # optional (NickServ)
      channels: ["#channel1", "#channel2"]
      sasl: true
```

### 2.13 Rocket.Chat [OFFICIAL]

```yaml
platforms:
  rocketchat:
    enabled: true
    extra:
      url: "${ROCKETCHAT_URL}"
      token: "${ROCKETCHAT_TOKEN}"
      user_id: "${ROCKETCHAT_USER_ID}"
      channel: "${ROCKETCHAT_CHANNEL}"
```

### 2.14 Gitter [OFFICIAL]

```yaml
platforms:
  gitter:
    enabled: true
    extra:
      token: "${GITTER_TOKEN}"
      room: "${GITTER_ROOM}"
```

### 2.15 Zulip [OFFICIAL]

```yaml
platforms:
  zulip:
    enabled: true
    extra:
      email: "${ZULIP_EMAIL}"
      api_key: "${ZULIP_API_KEY}"
      site: "${ZULIP_SITE}"                     # https://zulip.example.com
      stream: "${ZULIP_STREAM}"
      topic: "Hermes"
```

### 2.16 GoToSocial / Mastodon (Fediverse) [OFFICIAL]

```yaml
platforms:
  gotosocial:
    enabled: true
    extra:
      url: "${GOTOSOCIAL_URL}"
      token: "${GOTOSOCIAL_TOKEN}"
      visibility: "unlisted"                    # public, unlisted, private, direct

  mastodon:
    enabled: true
    extra:
      instance: "${MASTODON_INSTANCE}"          # mastodon.social
      token: "${MASTODON_TOKEN}"
      visibility: "unlisted"
```

### 2.17 Bluesky [OFFICIAL]

```yaml
platforms:
  bluesky:
    enabled: true
    extra:
      handle: "${BLUESKY_HANDLE}"               # user.bsky.social
      app_password: "${BLUESKY_APP_PASSWORD}"
      pds_url: "https://bsky.social"
```

### 2.18 Telegram Bot API (Raw) [OFFICIAL]

```yaml
platforms:
  telegram-bot-api:
    enabled: true
    extra:
      bot_token: "${HERMES_TELEGRAM_BOT_TOKEN}"
      api_url: "https://api.telegram.org"       # or local Bot API server
```

### 2.19 Generic Webhook [OFFICIAL]

```yaml
platforms:
  webhook:
    enabled: true
    extra:
      url: "${WEBHOOK_URL}"
      secret: "${WEBHOOK_SECRET}"
      method: "POST"
      headers: {}
```

### 2.20 Socket.io [OFFICIAL]

```yaml
platforms:
  socket:
    enabled: true
    extra:
      url: "${SOCKET_URL}"
      token: "${SOCKET_TOKEN}"
      namespace: "/hermes"
```

### 2.21 MQTT [OFFICIAL]

```yaml
platforms:
  mqtt:
    enabled: true
    extra:
      broker: "${MQTT_BROKER}"                  # mqtt://broker:1883
      topic: "${MQTT_TOPIC}"                    # hermes/out
      client_id: "${MQTT_CLIENT_ID}"
      username: "${MQTT_USERNAME}"
      password: "${MQTT_PASSWORD}"
      qos: 1
      retain: false
```

### 2.22 Pushover [OFFICIAL]

```yaml
platforms:
  pushover:
    enabled: true
    extra:
      user_key: "${PUSHOVER_USER_KEY}"
      api_token: "${PUSHOVER_API_TOKEN}"
      device: ""                                # optional
      priority: 0                               # -2 to 2
      sound: "pushover"
```

### 2.23 Gotify [OFFICIAL]

```yaml
platforms:
  gotify:
    enabled: true
    extra:
      url: "${GOTIFY_URL}"                      # https://gotify.example.com
      token: "${GOTIFY_TOKEN}"
      priority: 5
```

### 2.24 APNs (iOS Push) [OFFICIAL]

```yaml
platforms:
  apns:
    enabled: true
    extra:
      key_id: "${APNS_KEY_ID}"
      team_id: "${APNS_TEAM_ID}"
      auth_key_path: "${APNS_AUTH_KEY_PATH}"    # .p8 file
      bundle_id: "com.example.hermes"
      production: true
```

### 2.25 FCM (Android Push) [OFFICIAL]

```yaml
platforms:
  fcm:
    enabled: true
    extra:
      server_key: "${FCM_SERVER_KEY}"
      project_id: "${FCM_PROJECT_ID}"
```

### 2.26 Web Push (VAPID) [OFFICIAL]

```yaml
platforms:
  webpush:
    enabled: true
    extra:
      vapid_public_key: "${VAPID_PUBLIC_KEY}"
      vapid_private_key: "${VAPID_PRIVATE_KEY}"
      vapid_subject: "mailto:admin@example.com"
      subscription_endpoint: "${WEB_PUSH_ENDPOINT}"
      subscription_keys_p256dh: "${WEB_PUSH_P256DH}"
      subscription_keys_auth: "${WEB_PUSH_AUTH}"
```

### 2.27 Hermes Relay [OFFICIAL]

```yaml
platforms:
  relay:
    enabled: true
    extra:
      url: "${RELAY_URL}"
      token: "${RELAY_TOKEN}"
      peer_name: "hermes-agent"
```

### 2.28 Platform Home Channels (Env Vars)

For cron job defaults (`deliver: origin` on CLI, `deliver: telegram` on messaging):

```bash
TELEGRAM_HOME_CHANNEL="-1001234567890"
DISCORD_HOME_CHANNEL="123456789012345678"
SLACK_HOME_CHANNEL="C1234567890"
WHATSAPP_HOME_CHANNEL="+15551234567"
SIGNAL_HOME_CHANNEL="+15551234567"
MATRIX_HOME_CHANNEL="!xxx:matrix.org"
MATTERMOST_HOME_CHANNEL="general"
NTFY_HOME_CHANNEL="hermes-alerts"
EMAIL_HOME_CHANNEL="user@example.com"
SMS_HOME_CHANNEL="+15559876543"
```

---

## 3. Gateway Commands

```bash
# Installation and service
hermes gateway install [--system]
hermes gateway start|stop|restart|status
hermes gateway logs [-f] [--lines N]
hermes gateway doctor

# Platform management
hermes gateway platform list
hermes gateway platform enable <name>
hermes gateway platform disable <name>
hermes gateway platform test <name> [--message "test"]

# Webhook management (see Section 7)
hermes webhook subscribe <name> --events "..." --prompt "..." --skills X --deliver telegram ...
hermes webhook list|remove|test <name> [--payload '{}']

# Profile multiplexing
hermes gateway multiplex on|off
hermes profile create <name> --clone
hermes -p <name> gateway start
```

---

## 4. Session Management and Reset Policy (CRITICAL CHANGE)

### 4.1 Gateway Sessions vs CLI Sessions

| Aspect | CLI (`hermes chat`) | Gateway (Telegram, Discord, etc.) |
|--------|---------------------|-----------------------------------|
| Session ID | New per `hermes` invocation | **Persists across messages** |
| Reset trigger | `/new` or process exit | **NOT automatic** |
| Idle timeout | N/A | **No default idle reset** |
| Daily reset | N/A | **Removed** |

### 4.2 The Critical Change [OFFICIAL]

> **Session reset behavior changed from older versions.** Gateway conversations do NOT reset on idle/daily boundaries. Legacy `session_reset` config keys are **ignored**. Time-based resets require the catalog plugin `hermes-session-reset-policy`.

**Implications**:
- A Telegram conversation can stay a single session for weeks
- Memory writes (`MEMORY.md`, `USER.md`) only appear in prompt on **next session** (run `/new` or restart gateway)
- Context compression still works (triggered by token threshold)
- `session_search` works across the entire persistent session

### 4.3 Manual Session Reset on Gateway

```bash
# In gateway chat (Telegram, Discord, etc.)
/new              # Start fresh session (keeps memory/skills)
/stop             # Stop current task, keep session
/goal <text>      # Sets standing goal (survives /resume)
```

**To force session boundary**: Send `/new` or restart gateway service.

### 4.4 Cron Jobs and Sessions

- Cron jobs run in **fresh sessions** each tick
- They inherit project context files ONLY when `workdir` is set
- Subagents get project context files (minus `SOUL.md`)

---

## 5. Delivery Targets and Formats

### 5.1 Cron Job Delivery (`--deliver`)

| Target | Syntax | Description |
|--------|--------|-------------|
| Origin chat | `origin` | Reply to originating chat (CLI or messaging) |
| Local file | `local` | Save to `~/.hermes/cron/output/{job_id}/{timestamp}.md` |
| Telegram | `telegram` or `telegram:<chat_id>[:thread]` | Bot sends to chat |
| Discord | `discord:#channel` | Channel mention or ID |
| Slack | `slack` or `slack:#channel` | Default or specific channel |
| Email | `email` or `email:address@domain.com` | Via SMTP |
| SMS | `sms` or `sms:+15551234567` | Via Twilio |
| All platforms | `all` | Broadcast to all enabled |
| Comma list | `telegram,discord,slack` | Multiple targets |
| Bot chat | `bot-chat` or `bot-chat:<profile>` | Inter-agent (Bot Mode) |

**Defaults**:
- CLI-created jobs: `local`
- Messaging-created jobs: `origin`

### 5.2 Delivery Modifiers

| Modifier | Effect |
|----------|--------|
| `[SILENT]` as first line of response | Suppresses delivery (still saved to output) |
| `[CRON_FAILURE]` as first line | Marks run as failed (always delivers) |
| `cron.wrap_response: true` (default) | Adds `Cronjob Response:` header |
| `cron.wrap_response: false` | Raw output only |
| `deliver_only: true` (webhook) | Renders prompt as literal message, zero LLM cost |

### 5.3 Secret Redaction

All delivered text is automatically secret-redacted (API keys, tokens, passwords).

---

## 6. Allowlists and Security

### 6.1 Telegram Admin Allowlist

```yaml
platforms:
  telegram:
    extra:
      admin_chat_ids: ["123456789", "987654321"]  # only these users can invoke
```

### 6.2 Per-Platform Allowlists (General Pattern)

```yaml
platforms:
  <platform>:
    extra:
      allowed_users: ["user1", "user2"]      # platform-specific identifiers
      allowed_channels: ["#channel1"]         # channel restrictions
      block_bots: true                        # ignore other bots
```

### 6.3 Webhook Route Security

```yaml
platforms:
  webhook:
    extra:
      routes:
        github-pr:
          secret: "github-webhook-secret"     # HMAC validation
          # Rate limit: 30 req/min per route (hardcoded)
          # Idempotency TTL: 1 hour
          # Body limit: 1 MB
          # INSECURE_NO_AUTH: only on loopback
```

### 6.4 Toolset Constraints

- **Webhook routes**: Constrained to `web_search`, `web_extract`, `vision_analyze`, `clarify` by default. `toolsets:` in route config is **manual edit only** (CLI cannot self-grant `terminal`).
- **Cron jobs**: Use `cron` platform toolset config or per-job `--enabled-toolsets`.

---

## 7. Cross-Platform Continuity

[UNVERIFIED] Cross-platform mirroring lets a conversation started on Telegram continue on Discord. Mechanism not read in detail. Likely involves shared session ID via Hermes Relay or unified user identity.

---

## 8. Webhooks and Inbound Events

### 8.1 Inbound Webhook Server

```bash
# ~/.hermes/.env
WEBHOOK_ENABLED=true
WEBHOOK_PORT=8644
WEBHOOK_SECRET="global-fallback-secret"

# Health check
curl http://localhost:8644/health
# {"status": "ok", "platform": "webhook"}
```

### 8.2 Route Configuration (config.yaml)

```yaml
platforms:
  webhook:
    enabled: true
    extra:
      port: 8644
      secret: "global-fallback-secret"
      routes:
        github-pr:
          events: ["pull_request"]
          secret: "github-webhook-secret"
          prompt: |
            Review this pull request:
            Repository: {repository.full_name}
            PR #{number}: {pull_request.title}
          skills: ["github-code-review"]
          deliver: "github_comment"
          deliver_extra:
            repo: "{repository.full_name}"
            pr_number: "{number}"
          # Optional: cron_job, coalesce, mirror_to_session, profile, filters, script
```

### 8.3 Route Keys

| Key | Purpose |
|-----|---------|
| `events` | Platform event types (e.g., `["pull_request", "push"]`) |
| `secret` | HMAC secret for this route (overrides global) |
| `profile` | Hermes profile to use |
| `prompt` | Template with `{payload.field}` substitution |
| `filters` | JSONPath filters to match |
| `script` | Pre-run script (can emit `{"wakeAgent": false}`) |
| `skills` | Skills to attach |
| `toolsets` | Toolsets to enable (manual edit only) |
| `deliver` | Delivery target (see Section 5) |
| `deliver_extra` | Extra delivery params (templated) |
| `deliver_only` | Render prompt as literal message (no LLM) |
| `cron_job` | Fire existing cron job by name |
| `coalesce` | Merge rapid events |
| `mirror_to_session` | Also show in gateway chat |

### 8.4 Webhook Commands

```bash
hermes webhook subscribe <name> --events "..." --prompt "..." --skills X --deliver telegram --deliver-chat-id ID --deliver-only --cron-job NAME --route-profile NAME --mirror-to-session --description "..."
hermes webhook list|remove|test <name> [--payload '{}']
```

**Dynamic subscriptions**: Stored in `~/.hermes/webhook_subscriptions.json`, hot-reloaded.

### 8.5 Event-Triggered Cron

`cron_job: "pr-review-sweeper"` on a route fires an existing cron job. The webhook prompt becomes transient run context. Returns HTTP 202 immediately.

---

## 9. Bot Mode and Profiles

### 9.1 Profiles

```bash
hermes profile create research --no-skills
hermes profile create work --clone
hermes -p work chat
hermes -p work gateway start
```

- Each profile has own `~/.hermes/profiles/<name>/` with separate `config.yaml`, `skills/`, `memories/`, `cron/`
- Memory and skills are per-profile
- Webhook routes take `profile` field

### 9.2 Bot Mode [OFFICIAL]

Profiles become named **Bots** with their own chat, role, model, memory, and skills. They "run routines, share group chats, and message each other."

```bash
# Cron delivery into Bot Chat
hermes cron create "every 1h" "Check status" --deliver bot-chat:research
```

- `message_agent` tool mentioned in cron doc for bot-to-bot messaging
- Multi-gateway setups use a single dispatcher

### 9.3 Multi-Gateway [OFFICIAL]

- `gateway.multiplex_profiles: true` enables multi-profile gateway
- Profile distributions documented
- Workers under managed gateway require systemd scope

---

## 10. Conflicts

| # | Conflict | Resolution |
|---|----------|------------|
| 1 | Session reset: Phase 1/2 implied daily/idle reset | **Phase 3/4**: Gateway sessions do NOT auto-reset. Legacy keys ignored. |
| 2 | Platform count: Phase 1 said "25+" | **Phase 3**: ~28 explicit platforms |
| 3 | API server warning: Phase 1 basic | **Phase 3**: Stronger — full agent runtime, never expose publicly |
| 4 | Cross-platform continuity | **UNVERIFIED** — mechanism not documented |
| 5 | `send_message` tool for outbound | **CONFLICTING** — tools.md says not agent-callable |

---

## 11. Gaps

1. Complete per-platform `toolsets` enable syntax (manual edit only)
2. Exact `hermes gateway platform test` output format
3. `hermes-session-reset-policy` plugin details (catalog)
4. Bot Mode: `message_agent` tool schema
5. Multi-gateway dispatcher config
6. Profile distribution mechanics
7. A2A (Agent-to-Agent) messaging page not read
8. Kanban multi-gateway coordination details

---

## 12. Sources

- https://hermes-agent.nousresearch.com/docs/user-guide/messaging/gateway
- https://hermes-agent.nousresearch.com/docs/user-guide/messaging/platforms
- https://hermes-agent.nousresearch.com/docs/user-guide/messaging/webhooks
- https://hermes-agent.nousresearch.com/docs/user-guide/features/cron
- https://hermes-agent.nousresearch.com/docs/llms.txt
- Phase 3 Sections 4, 5, 6, 7
- Phase 4 Sections 4, 5, 10

---

**FILE COMPLETE: references/09-messaging-gateway.md** — 28 platforms with full configs, gateway commands, critical session reset policy change, delivery targets, allowlists, webhooks, Bot Mode.