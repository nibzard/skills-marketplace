# Skills Plugin

This directory contains the Claude Code plugin configuration for this repository.

## Plugin Structure

```
.claude-plugin/
├── plugin.json     # Plugin manifest
└── README.md       # This file
skills/
├── marimo/
├── marp-slide-quality/
├── claude-thread-publisher/
└── pentest-toolkit/
```

## Installation

Install this plugin in Claude Code:

```bash
# Install directly from GitHub
/plugin install nibzard/skills-marketplace

# Or clone locally and add from a path
git clone https://github.com/nibzard/skills-marketplace.git
/plugin install ./skills-marketplace
```

The plugin exposes the bundled Skills automatically. Claude will discover and invoke them when relevant.

## Skills Bundled

- marimo: Assistant for reactive Python notebooks (marimo)
- marp-slide-quality: Analyze and improve Marp slide decks using SlideGauge
- claude-thread-publisher: Publish Claude Code threads to GitHub Gists
- pentest-toolkit: Agent-oriented security testing scripts (uv-based)

## Contributing

1. Add a new Skill under `skills/<your-skill>/SKILL.md`
2. Keep supporting files one level deep and referenced from `SKILL.md`
3. Use `allowed-tools` to restrict tool usage appropriately
4. Submit a pull request

## Support

- Open an issue in the repository
- Review each skill’s `SKILL.md` for usage and requirements
