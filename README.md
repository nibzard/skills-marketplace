# Skills Kit

> An opinionated collection of Agent Skills I use daily in my work.

Not a marketplace—a toolkit. These are skills I've built and curated for my own workflows with Claude Code. If they're useful to you too, great.

---

## Quick Start

```bash
# Add the kit
/plugin marketplace add nibzard/skills-kit

# Install a skill
/plugin install yt-transcript@skills-kit
```

---

## The Skills

### Data & Notebooks
| Skill | What it does |
|-------|--------------|
| **[marimo](skills/marimo/)** | Reactive Python notebooks for data analysis, dashboards, and interactive apps |

### Media & Content
| Skill | What it does |
|-------|--------------|
| **[yt-transcript](skills/yt-transcript/)** | Fetch YouTube video transcripts for analysis and summarization |
| **[brand-illustrator](skills/brand-illustrator/)** | Generate Builder Methods-style line art illustrations with accent colors |

### Productivity
| Skill | What it does |
|-------|--------------|
| **[claude-thread-publisher](skills/claude-thread-publisher/)** | Publish Claude Code conversations as shareable HTML via GitHub Gists |
| **[tmux](skills/tmux/)** | Test interactive CLI/TUI applications end-to-end using tmux sessions |

### Development
| Skill | What it does |
|-------|--------------|
| **[release-runbook](skills/release-runbook/)** | Universal release workflow: detect project type, test, bump, tag, push |
| **[skill-creator](skills/skill-creator/)** | Create new Agent Skills from templates or interactively |

### Security
| Skill | What it does |
|-------|--------------|
| **[pentest-toolkit](skills/pentest-toolkit/)** | Authorized security testing and vulnerability assessment tools |

---

## Why This Exists

Agent Skills are how Claude Code extends its capabilities—model-invoked, context-aware, and progressively loaded. I built this collection because:

1. **I use them**—every skill here solves a real problem I encounter
2. **They work**—each is tested in production workflows
3. **They're opinionated**—built my way, for my workflows

If you're looking for a public marketplace with community contributions, this isn't it. If you want tools that have been battle-tested in real work, read on.

---

## Installing

### Install the Kit
```bash
/plugin marketplace add nibzard/skills-kit
```

### Install Individual Skills
```bash
# YouTube transcripts
/plugin install yt-transcript@skills-kit

# Publish conversations
/plugin install claude-thread-publisher@skills-kit

# Run releases
/plugin install release-runbook@skills-kit
```

### Install Everything
```json
// .claude/settings.json
{
  "enabledPlugins": [
    "marimo@skills-kit",
    "yt-transcript@skills-kit",
    "claude-thread-publisher@skills-kit",
    "tmux@skills-kit",
    "release-runbook@skills-kit"
  ]
}
```

---

## Contributing

This is a personal toolkit, but I accept quality PRs that align with the collection's scope:

- **New skills** must solve a real, generalizable problem
- **Improvements** should maintain existing functionality
- **Documentation** must be clear and complete

Before contributing, check that your skill isn't better suited as a standalone plugin or separate marketplace.

---

## Structure

```
skills-kit/
├── .claude-plugin/
│   └── marketplace.json       # Kit manifest
├── skills/
│   ├── marimo/                # Reactive notebooks
│   ├── yt-transcript/         # YouTube transcripts
│   ├── claude-thread-publisher/  # Share conversations
│   ├── tmux/                  # TUI testing
│   ├── release-runbook/       # Release automation
│   ├── skill-creator/         # Skill scaffolding
│   ├── pentest-toolkit/       # Security tools
│   └── brand-illustrator/     # Illustration generation
├── docs/                      # Additional docs
└── README.md
```

---

## About Agent Skills

Agent Skills extend Claude Code through organized folders containing instructions, scripts, and resources. Unlike traditional commands, Skills are **model-invoked**—Claude decides when to use them based on your request and the skill's description.

**Key characteristics:**
- **Autonomous**—Claude selects skills automatically based on context
- **Modular**—Each skill is self-contained with metadata
- **Progressive**—Load additional files only when referenced
- **Permission-aware**—Fine-grained tool access control

---

## Documentation

- **[Skills Overview](docs/skills-overview.md)**—Comprehensive guide to Agent Skills
- **[Skill Development](docs/skills-development.md)**—Creating and testing skills
- **[Marketplace Management](docs/marketplace-management.md)**—Managing skill distributions

---

## License

MIT — see [LICENSE](LICENSE). Individual skills may have their own licenses.

---

**[nibzard](https://github.com/nibzard)** · [Issues](https://github.com/nibzard/skills-kit/issues) · [Discussion](https://github.com/nibzard/skills-kit/discussions)
