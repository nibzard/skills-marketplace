# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository is a **Claude Code plugin marketplace** that catalogs multiple plugins. Each plugin bundles one or more **Agent Skills**.

**Install marketplace**: `/plugin marketplace add nibzard/skills-marketplace`

## Architecture

### Marketplace Structure

```
skills-marketplace/
├── .claude-plugin/
│   └── marketplace.json      # Marketplace catalog
├── skills/                   # Plugin directories
│   ├── marimo/               # .claude-plugin/plugin.json + skills/
│   ├── claude-thread-publisher/
│   ├── marp-slide-quality/
│   ├── pentest-toolkit/
│   ├── release-runbook/
│   ├── skill-creator/
│   ├── yt-transcript/
│   └── brand-illustrator/
└── docs/                     # Documentation
```

### Agent Skills Pattern

Skills are **model-invoked**, and can also be invoked directly via the plugin namespace. Claude discovers them via:
1. Personal: `~/.claude/skills/`
2. Project: `.claude/skills/`
3. Plugin: Bundled with installed plugins (namespaced as `/plugin-name:skill-name`)

**Skill Discovery**: Claude matches user requests against Skill `description` frontmatter. Be specific about when to use the skill.

**Progressive Disclosure**: `SKILL.md` is always loaded; supporting files (`reference.md`, `examples.md`, scripts) load only when referenced.

## Adding New Plugins / Skills

### 1. Create Plugin Directory

```bash
mkdir skills/your-plugin-name
```

### 2. Create Plugin Manifest and Skill

```bash
mkdir -p skills/your-plugin-name/.claude-plugin
cat > skills/your-plugin-name/.claude-plugin/plugin.json <<'EOF'
{
  "name": "your-plugin-name",
  "description": "Short description for the plugin manager",
  "version": "1.0.0"
}
EOF

mkdir -p skills/your-plugin-name/skills/your-skill-name
```

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

### 3. Update Marketplace Catalog

Add your plugin to `.claude-plugin/marketplace.json` so it appears in the marketplace.

### 4. Test Locally

```bash
# Add the marketplace locally (once)
/plugin marketplace add .

# Install the plugin from the marketplace
/plugin install your-plugin-name@skills-marketplace
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
/plugin marketplace add .
/plugin install your-plugin-name@skills-marketplace
```

## Environment Variables in Skills

- `${CLAUDE_PLUGIN_ROOT}`: Points to skill installation directory
- `${PWD}`, `${USER}`, `${HOME}`: Standard environment variables

Use `${CLAUDE_PLUGIN_ROOT}` for portable paths to scripts/templates:
```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/your-skill-name/scripts/helper.py input.xlsx
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

This repo is distributed as a marketplace via GitHub. Users add it with:
```bash
/plugin marketplace add nibzard/skills-marketplace
```

Plugins are installed individually from the marketplace.

## Documentation References

- `README.md`: Installation and overview
- `CONTRIBUTING.md`: Contribution workflow and skill standards
- `docs/skills-overview.md`: Comprehensive Agent Skills guide
- `docs/skills-development.md`: Creating and testing skills

## Key Constraints

- **Marketplace catalog**: Plugins must be listed in `.claude-plugin/marketplace.json`
- **Plugin structure**: Each plugin must contain `.claude-plugin/plugin.json` and `skills/<skill>/SKILL.md`
- **Namespacing**: Plugin skills are invoked as `/plugin-name:skill-name`
- **Progressive loading**: Keep `SKILL.md` focused; reference additional files as needed
