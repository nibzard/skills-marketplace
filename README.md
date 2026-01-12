# Skills Marketplace

A comprehensive marketplace for discovering, sharing, and managing Claude Code Agent Skills and plugins.

## Overview

The Skills Marketplace provides a centralized platform for distributing and discovering Agent Skills that extend Claude Code's capabilities. It serves as a hub where developers can:

- **Discover** skills for specific workflows and use cases
- **Share** custom skills with teams and communities
- **Install** skills with a single command
- **Contribute** to the growing ecosystem of AI capabilities

## What are Agent Skills?

Agent Skills are modular capabilities that extend Claude's functionality through organized folders containing instructions, scripts, and resources. Unlike traditional plugins or slash commands, Skills are **model-invoked**—Claude autonomously decides when to use them based on your request and the Skill's description.

### Key Features

- **Autonomous Invocation**: Claude selects and uses Skills automatically based on context
- **Modular Design**: Each Skill is a self-contained directory with metadata and resources
- **Progressive Disclosure**: Skills load additional files only when needed
- **Tool Permissions**: Fine-grained control over which tools Skills can access
- **Version Management**: Track and update Skills through git and marketplace systems

## Quick Start

### 1. Install the Plugin

```bash
# Install directly from GitHub (recommended)
/plugin install nibzard/skills-marketplace

# Or install from a local clone
git clone https://github.com/nibzard/skills-marketplace.git
/plugin install ./skills-marketplace
```

### 2. Browse Available Skills

```bash
# List all available skills
What Skills are available?

# Or interactively browse
/plugin
```

### 3. Use the Skills

Once the plugin is installed, Claude lists available Skills and invokes them automatically when relevant to your request.

## Marketplace Structure

```
skills-marketplace/
├── .claude-plugin/
│   └── plugin.json           # Plugin manifest
├── .claude/skills/           # Project-specific skills
├── skills/                    # Distributed skill packages
│   ├── marimo/
│   ├── marp-slide-quality/
│   ├── claude-thread-publisher/
│   └── pentest-toolkit/
├── examples/                  # Example skills and templates
├── docs/                      # Additional documentation
└── README.md                  # This file
```

## Available Skills

### Bundled Skills

- **marimo**: Reactive Python notebook assistant
- **marp-slide-quality**: Analyze Marp slides with SlideGauge
- **claude-thread-publisher**: Publish Claude threads to GitHub Gists
- **pentest-toolkit**: Agent-oriented security testing scripts

## Installation Methods

### For Users

1. **Install as Plugin** (Recommended):
   ```bash
   /plugin install nibzard/skills-marketplace
   ```

2. **Manual Installation of Individual Skills**:
   ```bash
   git clone https://github.com/nibzard/skills-marketplace.git
   mkdir -p ~/.claude/skills
   cp -r skills-marketplace/skills/<skill-name> ~/.claude/skills/
   ```

### For Developers

1. **Fork and Customize**:
   ```bash
   # Fork on GitHub, then add your fork
   /plugin install your-username/skills-marketplace
   # Add your custom skills to the forked repository
   ```

2. **Create Private Plugin**:
   ```bash
   # Clone and customize for your organization
   git clone https://github.com/your-org/skills-marketplace.git
   # Add company-specific skills
   # Host on private git repository
   /plugin install https://git.company.com/skills-marketplace.git
   ```

## Skill Categories

### 🛠️ Development Tools
Skills for software development, code quality, and workflow automation.

### 📊 Data & Analytics
Skills for data processing, analysis, and visualization.

### 📝 Documentation
Skills for creating, maintaining, and organizing documentation.

### 🚀 DevOps & Infrastructure
Skills for deployment, monitoring, and infrastructure management.

### 🔒 Security
Skills for security analysis, vulnerability scanning, and compliance.

### 📈 Productivity
Skills for task management, communication, and workflow optimization.

### 🎨 Design & Media
Skills for design tasks, media processing, and creative workflows.

## Creating Custom Skills

### Skill Structure

Each skill follows this structure:

```
skill-name/
├── SKILL.md                 # Required: Main skill definition
├── reference.md             # Optional: Detailed documentation
├── examples.md              # Optional: Usage examples
├── scripts/                 # Optional: Helper scripts
│   └── helper.py
└── templates/               # Optional: Code/file templates
    └── template.txt
```

### Minimal Skill Example

Create `SKILL.md` with frontmatter:

```yaml
---
name: text-analyzer
description: Analyze text for sentiment, entities, and patterns. Use when processing documents, analyzing feedback, or extracting insights from text.
---

# Text Analyzer

## Instructions
1. Analyze the provided text for sentiment
2. Extract key entities and patterns
3. Provide actionable insights based on the analysis

## Examples
- Customer feedback analysis
- Document summarization
- Content categorization
```

### Contributing Skills

1. **Fork the Repository**:
   ```bash
   fork https://github.com/your-org/skills-marketplace.git
   ```

2. **Add Your Skill**:
   ```bash
   cd skills-marketplace
   mkdir -p skills/your-skill-name
   # Create your skill files
   ```

3. **Verify Plugin**:
   Ensure your new Skill folder contains `SKILL.md` and supporting files, and that `What Skills are available?` lists it after reinstalling the plugin.

4. **Submit Pull Request**:
   ```bash
   git add skills/your-skill-name
   git commit -m "Add your-skill-name skill"
   git push
   # Create pull request
   ```

## Configuration

For team deployments, you can preconfigure enabled plugins in `.claude/settings.json`:

```json
{
  "enabledPlugins": [
    "nibzard/skills-marketplace"
  ]
}
```

## Documentation

- **[Skills Overview](docs/skills-overview.md)**: Comprehensive guide to Agent Skills
- **[Skill Development](docs/skills-development.md)**: Creating and testing custom skills
- **[Marketplace Management](docs/marketplace-management.md)**: Managing marketplaces and distributions
- **[API Reference](docs/api-reference.md)**: Technical specifications and schemas
- **[Best Practices](docs/best-practices.md)**: Guidelines for skill creation and usage

## Support and Community

### Getting Help

- **Documentation**: Check the [docs/](docs/) directory for detailed guides
- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/your-org/skills-marketplace/issues)
- **Discussions**: Join community discussions and share ideas

### Contributing Guidelines

1. **Code of Conduct**: Follow our [Code of Conduct](CODE_OF_CONDUCT.md)
2. **Contributing Guide**: See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution process
3. **Skill Standards**: Follow the [Skill Creation Guidelines](docs/skills-development.md#best-practices)

### Community Resources

- **[Official Claude Code Documentation](https://docs.claude.com/en/plugins)**: Core plugin and skill documentation
- **[Agent Skills Engineering Blog](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)**: Deep dive into Agent Skills architecture
- **[Community Forum](https://community.anthropic.com)**: Connect with other Claude Code users

## License

This marketplace is licensed under the [MIT License](LICENSE). Individual skills may have their own licenses - please check each skill's documentation.

## Roadmap

### Version 1.1 (Planned)
- [ ] Skill rating and review system
- [ ] Advanced search and filtering
- [ ] Skill dependency management
- [ ] Integration with package managers

### Version 1.2 (Future)
- [ ] Skill marketplace web interface
- [ ] Automated skill testing and validation
- [ ] Skill analytics and usage metrics
- [ ] Enterprise features for private skill distribution

## Changelog

### v1.0.0
- Initial marketplace release
- Core skill categories established
- Basic marketplace functionality
- Documentation and examples

---

**Ready to get started?** [Browse available skills](docs/skills-overview.md#available-skills) or [create your own skill](docs/skills-development.md)!

For more information about Agent Skills and Claude Code, visit the [official documentation](https://docs.claude.com/en/agents-and-tools/agent-skills).
