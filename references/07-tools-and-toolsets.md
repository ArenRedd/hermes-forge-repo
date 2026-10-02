---
title: Tools and Toolsets Reference
source_phases: [Phase 3]
hermes_version_documented: v0.21.5 (tag v2026.9.24, Sep 24 2026) — Phase 3 version not pinned; docs track `main`
research_date: Friday, October 2, 2026
last_built_in: Chat 2
confidence_legend: OFFICIAL = official repo/docs/source; COMMUNITY = third-party; INFERRED = deduced; UNVERIFIED = needs checking
used_by_playbooks: [05-automation-and-scheduling.md, 06-messaging-gateway-setups.md, 07-browser-and-data-collection.md, 08-multi-agent-and-parallel.md, 10-skill-authoring-and-memory-curation.md]
---

# Tools and Toolsets Reference

## WHEN TO READ THIS FILE
Use this file when you need the complete list of Hermes Agent built-in tools, their exact names, which toolset they belong to, and their parameters. Use it to select toolsets for a mission brief, to verify a tool name before invoking it, or to understand which tools are available in which execution context (CLI, gateway, cron, subagent).

## TABLE OF CONTENTS
1. Tool Naming Conventions and Drift
2. Complete Tool Table (100+ tools)
3. Core Toolsets (30+)
4. Composite Toolset Presets
5. Platform Toolsets (28+)
5. Dynamic and Special Toolsets
6. Toolset Enable/Disable Commands
7. Tool Availability by Execution Context
8. Conflicts
9. Gaps
10. Sources

---

## 1. Tool Naming Conventions and Drift

**VERBATIM FROM SOURCE** — The live tools reference page uses these names (current):

| Current Name | Deprecated/Alias | Status |
|--------------|------------------|--------|
| `process_manage` | `process` | Deprecated alias |
| `todo_list` | `todo` | Deprecated alias |
| `cronjob_manage` | `cronjob` | Deprecated alias |

**NAMING DRIFT WARNING** [OFFICIAL]: The live tools reference shows `process_manage`, `todo_list`, `cronjob_manage`. An older snapshot of the same page shows `process`, `todo`, `cronjob`. The live page includes a notice: *"Naming drift: the live reference may differ from older documentation snapshots."* Always verify with `hermes tools list` on your install.

**CONFLICTING TOOL** [CONFLICTING/DEPRECATED]: `send_message` is referenced in ntfy docs and delegation docs but **tools.md says outbound delivery is not agent-callable**; the registry lists no such tool. Treat as version-dependent — may exist in older versions, not in current.

**HONCHO TOOLS** [OFFICIAL]: No longer built-in. Now a memory-provider plugin at `plugins/memory/honcho/`. Exposes `hindsight_recall`, `hindsight_retain`, `hindsight_reflect` (Hindsight plugin).

---

## 2. Complete Tool Table

| Tool Name | Toolset | Category | Description | Version/Notes | Confidence |
|-----------|---------|----------|-------------|---------------|------------|
| `web_search` | `web`, `search` | Web | Search the web (up to 100 results) | | OFFICIAL |
| `web_extract` | `web` | Web | Extract clean content from URLs (max 5 per call) | | OFFICIAL |
| `browser_navigate` | `browser` | Browser | Navigate to URL, initialize session | | OFFICIAL |
| `browser_snapshot` | `browser` | Browser | Get accessibility tree snapshot | | OFFICIAL |
| `browser_click` | `browser` | Browser | Click element by ref ID | | OFFICIAL |
| `browser_type` | `browser` | Browser | Type text into input field | | OFFICIAL |
| `browser_press` | `browser` | Browser | Press keyboard key | | OFFICIAL |
| `browser_scroll` | `browser` | Browser | Scroll page up/down | | OFFICIAL |
| `browser_console` | `browser` | Browser | Get console output / evaluate JS | | OFFICIAL |
| `browser_vision` | `browser` | Browser | Screenshot + vision analysis | | OFFICIAL |
| `browser_back` | `browser` | Browser | Navigate back | | OFFICIAL |
| `browser_get_images` | `browser` | Browser | List all images on page | | OFFICIAL |
| `browser_vault_list` | `browser` | Browser | List saved logins/cards/addresses | | OFFICIAL |
| `browser_vault_fill` | `browser` | Browser | Fill form from vault handle | | OFFICIAL |
| `browser_vault_save_login` | `browser` | Browser | Save login for current page | | OFFICIAL |
| `browser_vault_enter_code` | `browser` | Browser | Enter 2FA code | | OFFICIAL |
| `browser_vault_unlock` | `browser` | Browser | Unlock password manager | | OFFICIAL |
| `vision_analyze` | `vision` | Vision | Analyze image from URL/path | | OFFICIAL |
| `execute_code` | `execute_code` | Code | Run Python with Hermes tools | | OFFICIAL |
| `terminal` | `terminal` | Terminal | Run shell commands | | OFFICIAL |
| `process_manage` | `process` | Process | Poll/wait/kill background processes | Current name `process_manage` (was `process`) | OFFICIAL |
| `read_file` | `files` | Files | Read text file with pagination | | OFFICIAL |
| `write_file` | `files` | Files | Write content to file | | OFFICIAL |
| `patch` | `files` | Files | Targeted find-and-replace | | OFFICIAL |
| `search_files` | `files` | Files | Search content or find files | | OFFICIAL |
| `memory` | `memory` | Memory | Add/replace/remove memory entries | Actions: `add`, `replace`, `remove`; targets: `memory`, `user` | OFFICIAL |
| `session_search` | `memory` | Memory | Search past sessions (FTS5) | | OFFICIAL |
| `skill_view` | `skills` | Skills | Load skill content or linked file | | OFFICIAL |
| `skills_list` | `skills` | Skills | List available skills | | OFFICIAL |
| `skill_manage` | `skills` | Skills | Create/update/delete skills | Actions: `create`, `patch`, `write_file`, `remove_file`, `delete` | OFFICIAL |
| `delegate_task` | `delegation` | Delegation | Spawn subagents | Control actions: `spawn`, `list`, `steer`, `stop` | OFFICIAL |
| `clarify` | `clarify` | Clarify | Ask user questions | | OFFICIAL |
| `cronjob_manage` | `cron` | Cron | Manage scheduled jobs | Current name `cronjob_manage` (was `cronjob`); actions: `create`, `list`, `update`, `pause`, `resume`, `run`, `remove` | OFFICIAL |
| `todo_list` | `todo` | Todo | Track task list | Current name `todo_list` (was `todo`) | OFFICIAL |
| `tool_search` | `tools` | Tools | Search deferred tools | | OFFICIAL |
| `tool_describe` | `tools` | Tools | Load tool schemas | | OFFICIAL |
| `tool_call` | `tools` | Tools | Invoke deferred tools | | OFFICIAL |
| `honcho_profile` | `honcho` | Memory | Read/write peer card | | OFFICIAL |
| `honcho_search` | `honcho` | Memory | Search peer history | | OFFICIAL |
| `honcho_reasoning` | `honcho` | Memory | Synthesized answer about peer | | OFFICIAL |
| `honcho_context` | `honcho` | Memory | Standing snapshot for peer | | OFFICIAL |
| `honcho_conclude` | `honcho` | Memory | Write conclusions about peer | | OFFICIAL |
| `text_to_speech` | `tts` | TTS | Convert text to speech audio | | OFFICIAL |
| `airtable` | `airtable` | Productivity | Airtable REST API via curl | | OFFICIAL |
| `box` | `box` | Productivity | Box cloud files | | OFFICIAL |
| `docx` | `docx` | Productivity | Create/read/edit .docx | | OFFICIAL |
| `google_workspace` | `google-workspace` | Productivity | Gmail, Calendar, Drive, Docs, Sheets | | OFFICIAL |
| `maps` | `maps` | Productivity | Geocode, POIs, routes | | OFFICIAL |
| `notion` | `notion` | Productivity | Notion API | | OFFICIAL |
| `pdf` | `pdf` | Productivity | PDF create/read/merge/fill/OCR | | OFFICIAL |
| `powerpoint` | `powerpoint` | Productivity | Create/read/edit .pptx | | OFFICIAL |
| `xlsx` | `xlsx` | Productivity | Create/read/edit .xlsx/CSV | | OFFICIAL |
| `github` | `github` | Dev | GitHub via gh CLI | | OFFICIAL |
| `arxiv` | `arxiv` | Research | Search arXiv papers | | OFFICIAL |
| `youtube_content` | `youtube-content` | Media | YouTube transcripts | | OFFICIAL |
| `gif_search` | `gif-search` | Media | Search/download GIFs | | OFFICIAL |
| `songsee` | `songsee` | Media | Audio spectrograms | | OFFICIAL |
| `obsidian` | `obsidian` | Notes | Read/search/create/edit notes | | OFFICIAL |
| `sherlock` | `sherlock` | Security | Find accounts by username | | OFFICIAL |
| `xurl` | `xurl` | Social | X/Twitter via xurl CLI | | OFFICIAL |
| `code_wiki` | `code-wiki` | Dev | Generate wiki docs | | OFFICIAL |
| `codebase_inspection` | `codebase-inspection` | Dev | Inspect codebases | | OFFICIAL |
| `dogfood` | `dogfood` | Dev | Exploratory QA | | OFFICIAL |
| `hermes_agent` | `hermes-agent` | Dev | Use/configure Hermes Agent | | OFFICIAL |
| `node_inspect_debugger` | `node-inspect-debugger` | Dev | Debug Node.js | | OFFICIAL |
| `pr_lens` | `pr-lens` | Dev | Draw code changes as SVGs | | OFFICIAL |
| `python_debugpy` | `python-debugpy` | Dev | Debug Python | | OFFICIAL |
| `requesting_code_review` | `requesting-code-review` | Dev | Pre-commit review | | OFFICIAL |
| `simplify_code` | `simplify-code` | Dev | Parallel cleanup | | OFFICIAL |
| `spike` | `spike` | Dev | Throwaway experiments | | OFFICIAL |
| `subagent_driven_development` | `subagent-driven-development` | Dev | Execute plans via subagents | | OFFICIAL |
| `systematic_debugging` | `systematic-debugging` | Dev | 4-phase debugging | | OFFICIAL |
| `test_driven_development` | `test-driven-development` | Dev | TDD enforcement | | OFFICIAL |
| `blocked_page_recovery` | `blocked-page-recovery` | Web | Recover blocked pages | | OFFICIAL |
| `cloudflare_temporary_deploy` | `cloudflare-temporary-deploy` | Web | Deploy Worker live | | OFFICIAL |
| `har_derived_api_client` | `har-derived-api-client` | Web | Record XHR to HAR | | OFFICIAL |
| `page_agent` | `page-agent` | Web | In-page GUI copilot | | OFFICIAL |
| `scrollcraft` | `scrollcraft` | Web | Scroll-driven landing pages | | OFFICIAL |
| `ai_presenter_video` | `ai-presenter-video` | Creative | AI presenter video | | OFFICIAL |
| `architecture_diagram` | `architecture-diagram` | Creative | Dark-themed SVG diagrams | | OFFICIAL |
| `ascii_video` | `ascii-video` | Creative | ASCII video conversion | | OFFICIAL |
| `auteur` | `auteur` | Creative | Cinematic web pages | | OFFICIAL |
| `baoyu_article_illustrator` | `baoyu-article-illustrator` | Creative | Article illustrations | | OFFICIAL |
| `baoyu_comic` | `baoyu-comic` | Creative | Knowledge comics | | OFFICIAL |
| `baoyu_infographic` | `baoyu-infographic` | Creative | Infographics | | OFFICIAL |
| `brag` | `brag` | Creative | Project website to video | | OFFICIAL |
| `brag_slim` | `brag-slim` | Creative | Directory/URL to video | | OFFICIAL |
| `claude_design` | `claude-design` | Creative | One-off HTML artifacts | | OFFICIAL |
| `creative_ideation` | `creative-ideation` | Creative | Generate ideas | | OFFICIAL |
| `design_md` | `design-md` | Creative | DESIGN.md token spec | | OFFICIAL |
| `draw_your_font` | `draw-your-font` | Creative | Handwriting to TTF | | OFFICIAL |
| `dream_loop` | `dream-loop` | Creative | 3D scenes via loop | | OFFICIAL |
| `excalidraw` | `excalidraw` | Creative | Hand-drawn diagrams | | OFFICIAL |
| `heartmula` | `heartmula` | Creative | Song generation | | OFFICIAL |
| `humanizer` | `humanizer` | Creative | Humanize text | | OFFICIAL |
| `impeccable` | `impeccable` | Creative | Design/redesign/critique | | OFFICIAL |
| `ip_as_logo` | `ip-as-logo` | Creative | IP mascot marks | | OFFICIAL |
| `kanban_video_orchestrator` | `kanban-video-orchestrator` | Creative | Video production pipeline | | OFFICIAL |
| `manim_video` | `manim-video` | Creative | 3Blue1Brown animations | | OFFICIAL |
| `meme_generation` | `meme-generation` | Creative | Meme PNGs | | OFFICIAL |
| `mono_color` | `mono-color` | Creative | Editorial print posters | | OFFICIAL |
| `p5js` | `p5js` | Creative | p5.js sketches | | OFFICIAL |
| `pixel_art` | `pixel-art` | Creative | Pixel art with era palettes | | OFFICIAL |
| `popular_web_designs` | `popular-web-designs` | Creative | 54 design systems | | OFFICIAL |
| `pretext` | `pretext` | Creative | Browser demos | | OFFICIAL |
| `simple_english` | `simple-english` | Creative | Simplified Technical English | | OFFICIAL |
| `sketch` | `sketch` | Creative | Throwaway HTML mockups | | OFFICIAL |
| `social_media_content_calendar` | `social-media-content-calendar` | Creative | Social campaigns | | OFFICIAL |
| `songwriting_and_ai_music` | `songwriting-and-ai-music` | Creative | Songwriting + Suno | | OFFICIAL |
| `system_atlas` | `system-atlas` | Creative | Isometric architecture | | OFFICIAL |
| `messaging_gateway_setup` | `messaging-gateway-setup` | DevOps | Setup messaging gateways | | OFFICIAL |
| `watchers` | `watchers` | DevOps | Poll RSS/JSON/GitHub | | OFFICIAL |
| `diagnose_crash` | `diagnose-crash` | Diagnose | Diagnose program crashes | | OFFICIAL |
| `adversarial_ux_test` | `adversarial-ux-test` | Dogfood | Hostile user roleplay | | OFFICIAL |
| `email_inbox_triage` | `email-inbox-triage` | Email | Triage inbox | | OFFICIAL |
| `himalaya` | `himalaya` | Email | IMAP/SMTP CLI | | OFFICIAL |
| `omarchy` | `omarchy` | Omarchy | Linux desktop customization | | OFFICIAL |
| `omarchy_audio_quality_fix` | `omarchy-audio-quality-fix` | Omarchy | Fix Realtek audio | | OFFICIAL |
| `document_to_action_items` | `document-to-action-items` | Productivity | Extract obligations | | OFFICIAL |
| `meeting_action_items` | `meeting-action-items` | Productivity | Meeting notes to tasks | | OFFICIAL |
| `weekly_review_planning` | `weekly-review-planning` | Productivity | Weekly reset | | OFFICIAL |
| `product_price_monitor` | `product-price-monitor` | Productivity | Watch prices | | OFFICIAL |
| `teams_meeting_pipeline` | `teams-meeting-pipeline` | Productivity | Teams summaries | | OFFICIAL |
| `competitor_news_monitor` | `competitor-news-monitor` | Research | Watch companies | | OFFICIAL |
| `grounded_citations` | `grounded-citations` | Research | Ground answers in sources | | OFFICIAL |
| `llm_wiki` | `llm-wiki` | Research | Build/query markdown KB | OFFICIAL |
| `agent_merge_conflict_arbiter` | `agent-merge-conflict-arbiter` | Agents | Merge conflict arbiter | OFFICIAL |
| `claude_code` | `claude-code` | Agents | Delegate to Claude Code | OFFICIAL |
| `codex` | `codex` | Agents | Delegate to Codex | OFFICIAL |
| `computer_use` | `computer-use` | Agents | Drive desktop | OFFICIAL |
| `dynamic_workflow` | `dynamic-workflow` | Agents | Plan-in-code fan-outs | OFFICIAL |
| `opencode` | `opencode` | Agents | Delegate to OpenCode | OFFICIAL |

**TOTAL TOOLS DOCUMENTED: 100+** (exact count varies by install; above covers all categories from live tools reference)

---

## 3. Core Toolsets (30+)

| Toolset Name | Tools Included | Default | Description |
|--------------|----------------|---------|-------------|
| `web` | `web_search`, `web_extract` | ✅ ON | Web search and extraction |
| `search` | `web_search` | ❌ OFF | Search only (no extract) |
| `browser` | 14 browser tools | ❌ OFF | Full browser automation |
| `vision` | `vision_analyze` | ❌ OFF | Image analysis |
| `execute_code` | `execute_code` | ✅ ON | Python execution with tool access |
| `terminal` | `terminal` | ✅ ON | Shell commands |
| `process` | `process_manage` | ❌ OFF | Background process control |
| `files` | `read_file`, `write_file`, `patch`, `search_files` | ✅ ON | File operations |
| `memory` | `memory`, `session_search` | ✅ ON | Built-in memory + session search |
| `skills` | `skill_view`, `skills_list`, `skill_manage` | ✅ ON | Skill system |
| `delegation` | `delegate_task` | ❌ OFF | Subagent spawning |
| `clarify` | `clarify` | ✅ ON | User clarification |
| `cron` | `cronjob_manage` | ❌ OFF | Scheduling |
| `todo` | `todo_list` | ❌ OFF | Task tracking |
| `tools` | `tool_search`, `tool_describe`, `tool_call` | ✅ ON | Deferred tool access |
| `honcho` | `honcho_profile`, `honcho_search`, `honcho_reasoning`, `honcho_context`, `honcho_conclude` | ❌ OFF | External memory (Honcho) |
| `tts` | `text_to_speech` | ❌ OFF | Text-to-speech |
| `airtable` | `airtable` | ❌ OFF | Airtable API |
| `box` | `box` | ❌ OFF | Box cloud |
| `docx` | `docx` | ❌ OFF | Word documents |
| `google-workspace` | `google_workspace` | ❌ OFF | Google Workspace |
| `maps` | `maps` | ❌ OFF | Geocoding/routes |
| `notion` | `notion` | ❌ OFF | Notion API |
| `pdf` | `pdf` | ❌ OFF | PDF operations |
| `powerpoint` | `powerpoint` | ❌ OFF | PowerPoint |
| `xlsx` | `xlsx` | ❌ OFF | Excel/CSV |
| `github` | `github` | ❌ OFF | GitHub CLI |
| `arxiv` | `arxiv` | ❌ OFF | arXiv search |
| `youtube-content` | `youtube_content` | ❌ OFF | YouTube transcripts |
| `gif-search` | `gif_search` | ❌ OFF | GIF search |
| `songsee` | `songsee` | ❌ OFF | Audio analysis |
| `obsidian` | `obsidian` | ❌ OFF | Obsidian notes |
| `sherlock` | `sherlock` | ❌ OFF | Username search |
| `xurl` | `xurl` | ❌ OFF | X/Twitter |
| `code-wiki` | `code_wiki` | ❌ OFF | Code wiki gen |
| `codebase-inspection` | `codebase_inspection` | ❌ OFF | Codebase stats |
| `dogfood` | `dogfood` | ❌ OFF | Web app QA |
| `hermes-agent` | `hermes_agent` | ❌ OFF | Hermes self-config |
| `node-inspect-debugger` | `node_inspect_debugger` | ❌ OFF | Node debugging |
| `pr-lens` | `pr_lens` | ❌ OFF | PR visualization |
| `python-debugpy` | `python_debugpy` | ❌ OFF | Python debugging |
| `requesting-code-review` | `requesting_code_review` | ❌ OFF | Code review |
| `simplify-code` | `simplify_code` | ❌ OFF | Code cleanup |
| `spike` | `spike` | ❌ OFF | Experiments |
| `subagent-driven-development` | `subagent_driven_development` | ❌ OFF | Subagent plans |
| `systematic-debugging` | `systematic_debugging` | ❌ OFF | Debugging |
| `test-driven-development` | `test_driven_development` | ❌ OFF | TDD |
| `blocked-page-recovery` | `blocked_page_recovery` | ❌ OFF | Blocked pages |
| `cloudflare-temporary-deploy` | `cloudflare_temporary_deploy` | ❌ OFF | CF Workers |
| `har-derived-api-client` | `har_derived_api_client` | ❌ OFF | HAR to client |
| `page-agent` | `page_agent` | ❌ OFF | In-page copilot |
| `scrollcraft` | `scrollcraft` | ❌ OFF | Scroll pages |
| `ai-presenter-video` | `ai_presenter_video` | ❌ OFF | AI video |
| `architecture-diagram` | `architecture_diagram` | ❌ OFF | Architecture diagrams |
| `ascii-video` | `ascii_video` | ❌ OFF | ASCII video |
| `auteur` | `auteur` | ❌ OFF | Cinematic pages |
| `baoyu-article-illustrator` | `baoyu_article_illustrator` | ❌ OFF | Illustrations |
| `baoyu-comic` | `baoyu_comic` | ❌ OFF | Comics |
| `baoyu-infographic` | `baoyu_infographic` | ❌ OFF | Infographics |
| `brag` | `brag` | ❌ OFF | Project to video |
| `brag-slim` | `brag_slim` | ❌ OFF | Dir/URL to video |
| `claude-design` | `claude_design` | ❌ OFF | HTML artifacts |
| `creative-ideation` | `creative_ideation` | ❌ OFF | Ideation |
| `design-md` | `design_md` | ❌ OFF | DESIGN.md |
| `draw-your-font` | `draw_your_font` | ❌ OFF | Handwriting font |
| `dream-loop` | `dream_loop` | ❌ OFF | 3D scenes |
| `excalidraw` | `excalidraw` | ❌ OFF | Excalidraw |
| `heartmula` | `heartmula` | ❌ OFF | Song gen |
| `humanizer` | `humanizer` | ❌ OFF | Humanize |
| `impeccable` | `impeccable` | ❌ OFF | Design critique |
| `ip-as-logo` | `ip_as_logo` | ❌ OFF | Mascot marks |
| `kanban-video-orchestrator` | `kanban_video_orchestrator` | ❌ OFF | Video pipeline |
| `manim-video` | `manim_video` | ❌ OFF | Manim animations |
| `meme-generation` | `meme_generation` | ❌ OFF | Memes |
| `mono-color` | `mono_color` | ❌ OFF | Posters |
| `p5js` | `p5js` | ❌ OFF | p5.js |
| `pixel-art` | `pixel_art` | ❌ OFF | Pixel art |
| `popular-web-designs` | `popular_web_designs` | ❌ OFF | 54 design systems |
| `pretext` | `pretext` | ❌ OFF | Browser demos |
| `simple-english` | `simple_english` | ❌ OFF | Simplified English |
| `sketch` | `sketch` | ❌ OFF | HTML mockups |
| `social-media-content-calendar` | `social_media_content_calendar` | ❌ OFF | Social calendar |
| `songwriting-and-ai-music` | `songwriting_and_ai_music` | ❌ OFF | Songwriting |
| `system-atlas` | `system_atlas` | ❌ OFF | Architecture atlases |
| `messaging-gateway-setup` | `messaging_gateway_setup` | ❌ OFF | Gateway setup |
| `watchers` | `watchers` | ❌ OFF | Polling watchers |
| `diagnose-crash` | `diagnose_crash` | ❌ OFF | Crash diagnosis |
| `adversarial-ux-test` | `adversarial_ux_test` | ❌ OFF | UX testing |
| `email-inbox-triage` | `email_inbox_triage` | ❌ OFF | Email triage |
| `himalaya` | `himalaya` | ❌ OFF | Email CLI |
| `omarchy` | `omarchy` | ❌ OFF | Linux desktop |
| `omarchy-audio-quality-fix` | `omarchy_audio_quality_fix` | ❌ OFF | Audio fix |
| `document-to-action-items` | `document_to_action_items` | ❌ OFF | Extract actions |
| `meeting-action-items` | `meeting_action_items` | ❌ OFF | Meeting tasks |
| `weekly-review-planning` | `weekly_review_planning` | ❌ OFF | Weekly review |
| `product-price-monitor` | `product_price_monitor` | ❌ OFF | Price monitor |
| `teams-meeting-pipeline` | `teams_meeting_pipeline` | ❌ OFF | Teams pipeline |
| `competitor-news-monitor` | `competitor_news_monitor` | ❌ OFF | Competitor news |
| `grounded-citations` | `grounded_citations` | ❌ OFF | Cited answers |
| `llm-wiki` | `llm_wiki` | ❌ OFF | LLM wiki |
| `agent-merge-conflict-arbiter` | `agent_merge_conflict_arbiter` | ❌ OFF | Merge arbiter |
| `claude-code` | `claude_code` | ❌ OFF | Claude Code |
| `codex` | `codex` | ❌ OFF | Codex |
| `computer-use` | `computer_use` | ❌ OFF | Desktop driving |
| `dynamic-workflow` | `dynamic_workflow` | ❌ OFF | Fan-out workflows |
| `opencode` | `opencode` | ❌ OFF | OpenCode |

---

## 4. Composite Toolset Presets

| Preset Name | Type | Included Toolsets | Purpose |
|-------------|------|-------------------|---------|
| `safe` | Official | `web`, `execute_code`, `terminal`, `files`, `memory`, `skills`, `clarify`, `tools` | Safe default for untrusted tasks |
| `coding` | Official | `safe` + `github`, `codebase-inspection`, `dogfood`, `python-debugpy`, `node-inspect-debugger`, `systematic-debugging`, `test-driven-development`, `requesting-code-review`, `pr-lens`, `code-wiki` | Full development environment |
| `debugging` | Official | `coding` + `spike`, `simplify-code`, `subagent-driven-development` | Heavy debugging |
| `research` | Inferred | `safe` + `arxiv`, `youtube-content`, `grounded-citations`, `llm-wiki`, `competitor-news-monitor`, `obsidian` | Research workflows |
| `full-power` | Inferred | All core toolsets + all platform toolsets | Maximum capability (high risk) |

**NOTE** [INFERRED]: `research` and `full-power` are not in the official docs as named presets but are composed from available toolsets. Use `hermes tools enable <toolset>` to build custom combinations.

---

## 5. Platform Toolsets (28+)

Each messaging/platform integration provides a toolset. Enable with `hermes tools enable hermes-<platform>`.

| Platform Toolset | Platform | Key Tools | Config Required |
|------------------|----------|-----------|-----------------|
| `hermes-telegram` | Telegram | Send/receive messages, media, inline keyboards | `HERMES_TELEGRAM_BOT_TOKEN`, `HERMES_TELEGRAM_CHAT_ID` |
| `hermes-discord` | Discord | Send/receive, embeds, threads | `DISCORD_BOT_TOKEN`, `DISCORD_CHANNEL_ID` |
| `hermes-slack` | Slack | Send/receive, blocks, threads | `SLACK_BOT_TOKEN`, `SLACK_SIGNING_SECRET`, `SLACK_APP_TOKEN` |
| `hermes-whatsapp` | WhatsApp | Send/receive via WhatsApp Business | `WHATSAPP_ACCESS_TOKEN`, `WHATSAPP_PHONE_NUMBER_ID` |
| `hermes-signal` | Signal | Send/receive via signal-cli | `SIGNAL_CLI_CONFIG`, `SIGNAL_PHONE_NUMBER` |
| `hermes-matrix` | Matrix | Send/receive, encryption | `MATRIX_HOMESERVER`, `MATRIX_USER_ID`, `MATRIX_ACCESS_TOKEN` |
| `hermes-mattermost` | Mattermost | Send/receive | `MATTERMOST_URL`, `MATTERMOST_TOKEN` |
| `hermes-ntfy` | ntfy | Send/receive via ntfy.sh | `NTFY_TOPIC`, `NTFY_SERVER` |
| `hermes-email` | Email | Send/receive via SMTP/IMAP | `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `IMAP_HOST` |
| `hermes-sms` | SMS | Send via Twilio/Vonage | `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_FROM` |
| `hermes-messenger` | Messenger | Facebook Messenger | `MESSENGER_PAGE_TOKEN`, `MESSENGER_VERIFY_TOKEN` |
| `hermes-irc` | IRC | IRC channels | `IRC_SERVER`, `IRC_PORT`, `IRC_NICK`, `IRC_CHANNELS` |
| `hermes-rocketchat` | Rocket.Chat | Send/receive | `ROCKETCHAT_URL`, `ROCKETCHAT_TOKEN` |
| `hermes-gitter` | Gitter | Gitter rooms | `GITTER_TOKEN` |
| `hermes-zulip` | Zulip | Zulip streams | `ZULIP_EMAIL`, `ZULIP_API_KEY`, `ZULIP_SITE` |
| `hermes-gotosocial` | GoToSocial | Fediverse | `GOTOSOCIAL_URL`, `GOTOSOCIAL_TOKEN` |
| `hermes-mastodon` | Mastodon | Fediverse | `MASTODON_INSTANCE`, `MASTODON_TOKEN` |
| `hermes-bluesky` | Bluesky | AT Protocol | `BLUESKY_HANDLE`, `BLUESKY_APP_PASSWORD` |
| `hermes-telegram-bot-api` | Telegram Bot API | Raw Bot API | `HERMES_TELEGRAM_BOT_TOKEN` |
| `hermes-webhook` | Generic Webhook | HTTP callbacks | `WEBHOOK_URL`, `WEBHOOK_SECRET` |
| `hermes-socket` | Socket.io | Real-time sockets | `SOCKET_URL`, `SOCKET_TOKEN` |
| `hermes-mqtt` | MQTT | IoT messaging | `MQTT_BROKER`, `MQTT_TOPIC`, `MQTT_CLIENT_ID` |
| `hermes-pushover` | Pushover | Push notifications | `PUSHOVER_USER_KEY`, `PUSHOVER_API_TOKEN` |
| `hermes-gotify` | Gotify | Self-hosted push | `GOTIFY_URL`, `GOTIFY_TOKEN` |
| `hermes-apns` | APNs | iOS push | `APNS_KEY_ID`, `APNS_TEAM_ID`, `APNS_AUTH_KEY` |
| `hermes-fcm` | FCM | Android push | `FCM_SERVER_KEY`, `FCM_PROJECT_ID` |
| `hermes-webpush` | Web Push | Browser push | `VAPID_PUBLIC_KEY`, `VAPID_PRIVATE_KEY`, `VAPID_SUBJECT` |
| `hermes-relay` | Hermes Relay | Inter-agent messaging | `RELAY_URL`, `RELAY_TOKEN` |

**UNION TOOLSET**: `hermes-gateway` = all platform toolsets combined (use with caution).

---

## 6. Dynamic and Special Toolsets

| Toolset | Source | Description |
|---------|--------|-------------|
| `mcp_<server>` | MCP | Auto-generated per MCP server (e.g., `mcp_github`, `mcp_filesystem`) |
| `plugin_<name>` | Plugins | Auto-generated per plugin (e.g., `plugin_hindsight`) |
| `skill_<name>` | Skills | Skills can declare `requires_toolsets` / `fallback_for_toolsets` |

---

## 7. Toolset Enable/Disable Commands

```bash
# List all toolsets and status
hermes tools list

# Enable a toolset (persists in config.yaml under toolsets.enabled)
hermes tools enable web
hermes tools enable hermes-telegram
hermes tools enable coding

# Disable a toolset
hermes tools disable browser
hermes tools disable delegation

# Show tools in a toolset
hermes tools list --toolset web

# Enable multiple at once
hermes tools enable web terminal files memory skills clarify tools

# Disable all but safe preset
hermes tools disable --all && hermes tools enable safe
```

**Config location**: `toolsets.enabled: [...]` in `~/.hermes/config.yaml`

**Per-session override**: `hermes chat --toolsets web,terminal,files -q "task"`

---

## 8. Tool Availability by Execution Context

| Context | Default Toolsets | Can Add Toolsets | Restrictions |
|---------|------------------|------------------|--------------|
| CLI Interactive (`hermes`) | `web`, `execute_code`, `terminal`, `files`, `memory`, `skills`, `clarify`, `tools` | Yes (`--toolsets`, slash `/toolset`) | None |
| CLI One-shot (`hermes -z`, `hermes chat --oneshot -q`) | Same as interactive | Yes (`--toolsets`) | Must complete in one turn |
| Gateway Chat (Telegram, Discord, etc.) | Platform toolset + `safe` preset | Yes (per-route `toolsets:`) | Webhook routes: constrained to `web_search`, `web_extract`, `vision_analyze`, `clarify` by default |
| Cron Job | `cron` platform config from `hermes tools` | Yes (`--enabled-toolsets`) | Cannot create cron jobs unless `cron.allow_agent_scheduling: true` |
| Subagent (leaf) | Inherits parent's enabled toolsets | No (no `toolsets` parameter) | Blocked: `delegate_task`, `clarify`, `memory`, `send_message`, `cronjob` |
| Subagent (orchestrator) | Inherits parent's enabled toolsets | No | Keeps `execute_code` |
| Webhook Route | Constrained set (see above) | Manual edit only (`toolsets:` in route config) | Cannot self-grant `terminal` |
| API Server | Full agent runtime | Yes | **Warning**: Full terminal/file/MCP access on that host |

---

## 9. Conflicts

| # | Conflict | Resolution |
|---|----------|------------|
| 1 | Tool naming: `process_manage` vs `process`, `todo_list` vs `todo`, `cronjob_manage` vs `cronjob` | Use current names (`_manage`, `_list`); note deprecated aliases |
| 2 | `send_message` tool: referenced in docs but not in registry | Mark CONFLICTING/DEPRECATED; verify per install |
| 3 | Honcho tools: Phase 1 implied built-in; Phase 3 says plugin | Document as external plugin only |
| 4 | MCP tool naming: `mcp_<server>_<tool>` vs `mcp__<server>__<tool>` | Document both; mark version-dependent |
| 5 | Toolset count: Phase 1 said ~28; Phase 3 shows 30+ core + platform | Use Phase 3's complete tables |
| 6 | `research` and `full-power` presets not official | Mark INFERRED; build from components |

---

## 10. Gaps

1. Complete parameter schemas for each tool (not in Phase 3 source)
2. Exact tool count per default install (varies by bundled skills)
3. `daytona` and `vercel_sandbox` toolset names (not explicitly documented)
4. Whether `connections` toolset requires Portal enabled (Phase 3 says "only if Portal enabled")
5. `context_engine` toolset — exact tools included
6. Per-tool timeout/rate-limit configs
7. Toolset dependency graph (which toolsets require others)

---

## 11. Sources

- https://hermes-agent.nousresearch.com/docs/reference/tools (live tools reference)
- https://hermes-agent.nousresearch.com/docs/user-guide/features/tools (tools overview)
- https://hermes-agent.nousresearch.com/docs/llms.txt (docs index)
- https://github.com/NousResearch/hermes-agent (repo structure)
- Phase 3 research Sections 1, 2, 3, 5, 6, 7

---

**FILE COMPLETE: references/07-tools-and-toolsets.md** — 100+ tools, 30+ core toolsets, 4 composite presets, 28+ platform toolsets, dynamic toolsets, enable/disable commands, context availability table.