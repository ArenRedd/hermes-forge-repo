#!/usr/bin/env python3
"""
Validate reference files integrity for hermes-knowledge-skill.
Checks: file existence, required sections, cross-references, unverified markers.
"""

import os
import re
from pathlib import Path

REFERENCES_DIR = Path(__file__).parent.parent / "references"
REQUIRED_FILES = [
    "00-index-and-routing.md",
    "01-foundations-architecture.md",
    "02-install-vps-config-basics.md",
    "03-providers-and-models.md",
    "04-cli-command-reference-a.md",
    "04-cli-command-reference-b.md",
    "05-slash-commands-sessions-interactive.md",
    "06-config-keys-and-env-vars.md",
    "07-tools-and-toolsets.md",
    "08-terminal-backends.md",
    "09-messaging-gateway.md",
    "10-mcp-plugins-api.md",
    "11-skills-system.md",
    "12-memory-and-context.md",
    "13-scheduling-and-automation.md",
    "14-subagents-and-delegation.md",
    "15-learning-loop-and-advanced.md",
    "16-security-and-hardening.md",
    "17-vps-operations.md",
    "18-troubleshooting.md",
    "19-cost-and-optimization.md",
    "20-use-case-catalog.md",
    "21-glossary.md",
    "22-unverified-and-gaps.md",
    "23-sources.md",
]

# Playbook files referenced from reference files (not in this skill's references dir)
PLAYBOOK_FILES = [
    "01-coding-and-dev.md",
    "02-devops-and-server-admin.md",
    "03-research-and-analysis.md",
    "04-content-and-social.md",
    "05-automation-and-scheduling.md",
    "06-messaging-gateway-setups.md",
    "07-browser-and-data-collection.md",
    "08-multi-agent-and-parallel.md",
    "09-personal-productivity.md",
    "10-skill-authoring-and-memory-curation.md",
    "11-maintenance-backup-recovery.md",
]

# Combined valid references (reference files + playbook files)
ALL_VALID_REFS = set(REQUIRED_FILES) | set(PLAYBOOK_FILES)

REQUIRED_FRONTMATTER = ["title", "source_phases", "hermes_version_documented", "research_date"]


def validate_frontmatter(content: str, filepath: Path) -> list:
    """Validate YAML frontmatter exists and has required fields."""
    errors = []
    if not content.startswith('---'):
        errors.append(f"{filepath.name}: Missing frontmatter (no ---)")
        return errors
    
    end_idx = content.find('\n---', 3)
    if end_idx == -1:
        errors.append(f"{filepath.name}: Frontmatter not closed")
        return errors
    
    frontmatter = content[3:end_idx]
    for field in REQUIRED_FRONTMATTER:
        if field not in frontmatter:
            errors.append(f"{filepath.name}: Missing required frontmatter field: {field}")
    
    return errors


def validate_hermes_version(content: str, filepath: Path) -> list:
    """Check that hermes version is documented."""
    errors = []
    if "v0.21.5" not in content and "v2026.9.24" not in content:
        errors.append(f"{filepath.name}: Missing Hermes version reference (v0.21.5 / v2026.9.24)")
    return errors


def validate_cross_references(content: str, filepath: Path, all_files: set) -> list:
    """Check that cross-references to other reference files are valid."""
    errors = []
    # Find references like "04-cli-command-reference-a.md" or "references/04-cli-command-reference-a.md"
    refs = re.findall(r'(?:references/)?(\d{2}-[\w-]+\.md)', content)
    for ref in refs:
        if ref not in all_files:
            errors.append(f"{filepath.name}: Invalid cross-reference to {ref}")
    return errors


def validate_unverified_markers(content: str, filepath: Path) -> list:
    """Check for [VERIFY] and ⚠ UNVERIFIED markers."""
    warnings = []
    verify_count = content.count('[VERIFY')
    unverified_count = content.count('⚠ UNVERIFIED') + content.count('UNVERIFIED')
    if verify_count > 0:
        warnings.append(f"{filepath.name}: {verify_count} [VERIFY] markers found")
    if unverified_count > 0:
        warnings.append(f"{filepath.name}: {unverified_count} UNVERIFIED markers found")
    return warnings


def validate_command_format(content: str, filepath: Path) -> list:
    """Check that hermes commands use backticks."""
    warnings = []
    # Look for hermes commands not in backticks
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        if re.search(r'\bhermes\s+\w+', line) and '`' not in line and not line.strip().startswith('#'):
            # Might be in a code block - check context
            context = '\n'.join(lines[max(0,i-3):i+2])
            if '```' not in context:
                warnings.append(f"{filepath.name}:L{i}: Possible unformatted command: {line.strip()[:80]}")
    return warnings


def main():
    all_files = ALL_VALID_REFS
    all_errors = []
    all_warnings = []
    
    print("Validating hermes-knowledge-skill references...\n")
    
    # Check file existence
    for req_file in REQUIRED_FILES:
        path = REFERENCES_DIR / req_file
        if not path.exists():
            all_errors.append(f"MISSING: {req_file}")
        else:
            content = path.read_text(encoding='utf-8')
            
            # Run validations
            all_errors.extend(validate_frontmatter(content, path))
            all_errors.extend(validate_hermes_version(content, path))
            all_errors.extend(validate_cross_references(content, path, all_files))
            all_warnings.extend(validate_unverified_markers(content, path))
            all_warnings.extend(validate_command_format(content, path))
            
            # Size check
            size = path.stat().st_size
            if size < 1000:
                all_warnings.append(f"{req_file}: Very small ({size} bytes)")
    
    # Report
    print(f"Files checked: {len(REQUIRED_FILES)}")
    print(f"Errors: {len(all_errors)}")
    print(f"Warnings: {len(all_warnings)}\n")
    
    if all_errors:
        print("ERRORS:")
        for err in all_errors:
            print(f"  ❌ {err}")
    
    if all_warnings:
        print("\nWARNINGS:")
        for warn in all_warnings[:20]:  # Limit output
            print(f"  ⚠️  {warn}")
        if len(all_warnings) > 20:
            print(f"  ... and {len(all_warnings) - 20} more warnings")
    
    if not all_errors:
        print("\n✅ All critical validations passed!")
        return 0
    else:
        print(f"\n❌ {len(all_errors)} critical errors found")
        return 1


if __name__ == "__main__":
    exit(main())