#!/usr/bin/env python3
"""
Build search index for hermes-knowledge-skill references.
Creates a JSON index for fast topic lookup across all 21 reference files.
"""

import json
import os
import re
from pathlib import Path
from collections import defaultdict

REFERENCES_DIR = Path(__file__).parent.parent / "references"
OUTPUT_FILE = Path(__file__).parent.parent / "assets" / "search_index.json"

# Keywords to index for each reference file
FILE_KEYWORDS = {
    "00-index-and-routing.md": ["routing", "index", "intent", "trigger", "domain", "classification"],
    "01-foundations-architecture.md": ["architecture", "identity", "stack", "repository", "diagram", "hermes-agent", "nous-research"],
    "02-install-vps-config-basics.md": ["install", "vps", "docker", "systemd", "hardening", "walkthrough", "configuration", "setup"],
    "03-providers-and-models.md": ["provider", "model", "openrouter", "anthropic", "openai", "google", "local", "fallback", "routing", "switching"],
    "04-cli-command-reference-a.md": ["cli", "command", "hermes", "chat", "model", "setup", "gateway", "send", "cron", "auth", "diagnostics", "backup", "profile"],
    "04-cli-command-reference-b.md": ["cli", "command", "headless", "python", "api", "server"],
    "05-slash-commands-sessions-interactive.md": ["slash", "command", "session", "interactive", "approval", "personality", "keyboard", "compact", "cost", "reasoning", "voice"],
    "06-config-keys-and-env-vars.md": ["config", "environment", "variable", "precedence", "profile", "context", "file", "layout", "cheat"],
    "07-tools-and-toolsets.md": ["tool", "toolset", "preset", "platform", "mcp", "browser", "web", "file", "terminal", "process", "todo", "cronjob"],
    "08-terminal-backends.md": ["backend", "terminal", "docker", "ssh", "singularity", "modal", "daytona", "vercel", "sandbox", "file", "transfer", "hardening"],
    "09-messaging-gateway.md": ["gateway", "messaging", "telegram", "discord", "slack", "whatsapp", "pairing", "allowlist", "webhook", "bot", "mode", "delivery", "platform"],
    "10-mcp-plugins-api.md": ["mcp", "plugin", "api", "server", "client", "stdio", "acp", "proxy", "egress"],
    "11-skills-system.md": ["skill", "bundle", "curator", "hub", "trust", "install", "author", "create", "official", "community"],
    "12-memory-and-context.md": ["memory", "context", "honcho", "fts5", "soul", "personality", "compression", "priority", "layer", "provider"],
    "13-scheduling-and-automation.md": ["cron", "schedule", "automation", "job", "kanban", "webhook", "hook", "wakeagent", "continuity", "context-from", "script", "no-agent"],
    "14-subagents-and-delegation.md": ["subagent", "delegate", "orchestrator", "kanban", "bot", "mode", "a2a", "rpc", "concurrency", "merge"],
    "15-learning-loop-and-advanced.md": ["goal", "checkpoint", "rollback", "reasoning", "moa", "mixture", "agents", "batch", "rl", "pattern", "anti-pattern"],
    "16-security-and-hardening.md": ["security", "approval", "sandbox", "allowlist", "secret", "audit", "supply", "chain", "tirith", "blocklist", "network", "egress"],
    "17-vps-operations.md": ["vps", "hardening", "monitoring", "log", "rotation", "disk", "network", "backup", "migration", "provision", "ops"],
    "18-troubleshooting.md": ["troubleshoot", "error", "doctor", "log", "database", "repair", "recovery", "gateway", "config", "migration", "session", "waled"],
    "19-cost-and-optimization.md": ["cost", "optimization", "budget", "routing", "auxiliary", "compression", "free", "tier", "monitoring", "usage"],
    "20-use-case-catalog.md": ["use", "case", "catalog", "task", "pattern", "example", "workflow"],
    "21-glossary.md": ["glossary", "term", "definition", "word"],
    "22-unverified-and-gaps.md": ["unverified", "gap", "verify", "unknown", "missing", "confirm"],
    "23-sources.md": ["source", "reference", "phase", "research", "url", "repo"],
}


def extract_headings(content: str) -> list:
    """Extract markdown headings with their level."""
    headings = []
    for line in content.split('\n'):
        match = re.match(r'^(#{1,4})\s+(.+)$', line)
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            headings.append({"level": level, "text": text})
    return headings


def extract_code_blocks(content: str) -> list:
    """Extract code blocks with language hint."""
    blocks = []
    pattern = r'```(\w+)?\n(.*?)\n```'
    for match in re.finditer(pattern, content, re.DOTALL):
        lang = match.group(1) or "text"
        code = match.group(2)[:200]  # First 200 chars
        blocks.append({"language": lang, "preview": code})
    return blocks


def extract_tables(content: str) -> list:
    """Extract markdown tables."""
    tables = []
    lines = content.split('\n')
    in_table = False
    table_lines = []
    for line in lines:
        if '|' in line and line.strip().startswith('|'):
            if not in_table:
                in_table = True
                table_lines = [line]
            else:
                table_lines.append(line)
        else:
            if in_table:
                if len(table_lines) > 2:  # Header + separator + at least one row
                    tables.append('\n'.join(table_lines))
                in_table = False
                table_lines = []
    if in_table and len(table_lines) > 2:
        tables.append('\n'.join(table_lines))
    return tables


def build_index():
    index = {
        "version": "1.0.0",
        "hermes_version": "v0.21.5 (tag v2026.9.24)",
        "research_date": "2026-10-02",
        "files": {},
        "global_keywords": defaultdict(list),
        "commands": [],
        "config_keys": [],
        "env_vars": [],
    }

    for ref_file in sorted(REFERENCES_DIR.glob("*.md")):
        if ref_file.name in FILE_KEYWORDS:
            content = ref_file.read_text(encoding='utf-8')
            
            # Extract structured data
            headings = extract_headings(content)
            code_blocks = extract_code_blocks(content)
            tables = extract_tables(content)
            
            # Extract hermes commands
            hermes_commands = re.findall(r'`(hermes\s+\S+(?:\s+\S+)*)`', content)
            hermes_commands += re.findall(r'hermes\s+\w+(?:\s+\w+)*', content)
            
            # Extract config keys
            config_keys = re.findall(r'`([a-z_]+(?:\.[a-z_]+)+)`', content)
            
            # Extract env vars
            env_vars = re.findall(r'`(HERMES_[A-Z_]+)`', content)
            
            file_data = {
                "name": ref_file.name,
                "size_bytes": ref_file.stat().st_size,
                "keywords": FILE_KEYWORDS[ref_file.name],
                "headings": headings,
                "code_blocks": len(code_blocks),
                "tables": len(tables),
                "hermes_commands": list(set(hermes_commands))[:50],  # Limit
                "config_keys": list(set(config_keys))[:50],
                "env_vars": list(set(env_vars))[:50],
            }
            
            index["files"][ref_file.name] = file_data
            
            # Build global keyword index
            for kw in FILE_KEYWORDS[ref_file.name]:
                index["global_keywords"][kw].append(ref_file.name)
            
            # Collect commands, config keys, env vars
            index["commands"].extend(file_data["hermes_commands"])
            index["config_keys"].extend(file_data["config_keys"])
            index["env_vars"].extend(file_data["env_vars"])

    # Deduplicate
    index["commands"] = sorted(set(index["commands"]))
    index["config_keys"] = sorted(set(index["config_keys"]))
    index["env_vars"] = sorted(set(index["env_vars"]))
    index["global_keywords"] = dict(index["global_keywords"])

    # Save
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(index, indent=2))
    print(f"Index built: {OUTPUT_FILE}")
    print(f"Files indexed: {len(index['files'])}")
    print(f"Commands found: {len(index['commands'])}")
    print(f"Config keys found: {len(index['config_keys'])}")
    print(f"Env vars found: {len(index['env_vars'])}")


if __name__ == "__main__":
    build_index()