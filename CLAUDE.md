# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Claude Code Plugin** that bundles multiple **Agent Skills** for distribution. Agent Skills are model-invoked capabilities—Claude autonomously selects and uses them based on request context and the Skill's description.

**Installation**: `/plugin install nibzard/skills-marketplace`

## Architecture

### Plugin Bundle Structure

```
skills-marketplace/
├── .claude-plugin/
│   ├── plugin.json           # Plugin metadata
│   └── marketplace.json      # Skills catalog (auto-discovers skills/)
├── skills/                   # Bundled Agent Skills
│   ├── marimo/              # Reactive Python notebooks
│   ├── claude-thread-publisher/  # Export threads to GitHub Gists
│   ├── marp-slide-quality/  # Analyze Marp presentations
│   └── pentest-toolkit/     # Security testing toolkit
└── docs/                    # Documentation
```

### Agent Skills Pattern

Skills are **model-invoked**, not user-invoked. Claude discovers them via:
1. Personal: `~/.claude/skills/`
2. Project: `.claude/skills/`
3. Plugin: Bundled with installed plugins

**Skill Discovery**: Claude matches user requests against Skill `description` frontmatter. Be specific about when to use the skill.

**Progressive Disclosure**: `SKILL.md` is always loaded; supporting files (`reference.md`, `examples.md`, scripts) load only when referenced.

## Adding New Skills

### 1. Create Skill Directory

```bash
mkdir skills/your-skill-name
```

### 2. Create SKILL.md with Frontmatter

```yaml
---
name: your-skill-name
description: Clear description of what this skill does and when to use it. Include specific triggers and keywords.
allowed-tools: Read, Write, Edit  # Optional: restrict tool access
---

# Your Skill Title

## Instructions
[Step-by-step guidance for Claude]

## Examples
[Concrete usage scenarios]

## Requirements
[Dependencies and prerequisites]
```

### 3. No Manifest Edits Required

Skills are auto-discovered from `skills/*/SKILL.md`. The `marketplace.json` is for display purposes only.

### 4. Test Locally

```bash
# Reinstall plugin to discover new Skill
/plugin install .

# Verify discovery
What Skills are available?

# Test invocation
[Ask a question that should trigger your skill]
```

## Frontmatter Specification

- **name** (required): kebab-case identifier, max 64 chars
- **description** (required): What the skill does + when to use it, max 1024 chars
- **allowed-tools** (optional): Comma-separated tool list for permission control

**Critical**: The `description` is Claude's primary signal for when to invoke the skill. Include both capabilities and triggers.

## Testing Skills

There are no automated tests. Skills are validated through:

1. **Discovery Testing**: `What Skills are available?` lists the skill
2. **Invocation Testing**: Natural language queries trigger the skill appropriately
3. **Functional Testing**: The skill produces expected outputs

Test locally before committing:
```bash
/plugin install .
```

## Environment Variables in Skills

- `${CLAUDE_PLUGIN_ROOT}`: Points to skill installation directory
- `${PWD}`, `${USER}`, `${HOME}`: Standard environment variables

Use `${CLAUDE_PLUGIN_ROOT}` for portable paths to scripts/templates:
```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/helper.py input.xlsx
```

## Tool Permissions

Skills can restrict tool access via `allowed-tools` frontmatter:

```yaml
---
allowed-tools: Read, Grep, Glob  # Read-only access
---
```

Benefits: Security, focus, reduced permission prompts.

## Distribution

This repo is distributed as a single plugin via GitHub. Users install with:
```bash
/plugin install nibzard/skills-marketplace
```

All bundled skills become available immediately. No marketplace mode—just a plugin bundle.

## Documentation References

- `README.md`: Installation and overview
- `CONTRIBUTING.md`: Contribution workflow and skill standards
- `docs/skills-overview.md`: Comprehensive Agent Skills guide
- `docs/skills-development.md`: Creating and testing skills

## Key Constraints

- **No marketplace mode**: This is a plugin bundle, not a marketplace
- **Auto-discovery**: Skills under `skills/*/SKILL.md` are discovered automatically
- **Model-invoked**: Skills are triggered by semantic matching, not slash commands
- **Progressive loading**: Keep `SKILL.md` focused; reference additional files as needed
