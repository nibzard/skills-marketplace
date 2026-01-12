# Skills Marketplace Plugin

This directory contains the Claude Code plugin configuration for the Skills Marketplace.

## Plugin Structure

```
.claude-plugin/
├── marketplace.json      # Main marketplace configuration
├── README.md             # This file
└── skills/               # Skill packages (symbolic link to ../skills/)
```

## Installation

To install this marketplace in Claude Code:

```bash
# Add the marketplace from GitHub (recommended)
/plugin marketplace add nibzard/skills-marketplace

# Browse available skills
/plugin

# Install a specific skill
/plugin install git-automation@skills-marketplace
```

## Configuration

The marketplace is configured in `marketplace.json` with:

- **Marketplace metadata**: Name, version, owner information
- **Skill catalog**: Available skills with descriptions and metadata
- **Categories**: Organized skill groupings
- **Dependencies**: Required tools and packages

## Skills Available

### Development Tools
- **git-automation**: Git workflow automation and commit message generation
- **code-reviewer**: Code quality analysis and security review

### Data & Analytics
- **data-analysis**: Data processing, statistics, and visualization
- **excel-analyzer**: Excel spreadsheet analysis and business insights

### Documentation
- **documentation-helper**: Technical documentation generation and maintenance

### Productivity
- **task-manager**: Project planning and task organization

## Usage

Once installed, skills are automatically available. Claude will invoke relevant skills based on your requests:

```bash
# Git automation
"I just made some changes to my code. Can you help me write a good commit message?"

# Data analysis
"Can you analyze this sales data spreadsheet and tell me what insights you find?"

# Documentation
"Please help me write documentation for this new API endpoint."

# Task management
"I need to plan a new project. Can you help me break it down into tasks?"
```

## Contributing

To add new skills to this marketplace:

1. Create skill in `../skills/skill-name/`
2. Add skill to `marketplace.json` plugins array
3. Test skill installation and functionality
4. Submit pull request

## Support

For issues or questions about this marketplace:
- Create an issue in the repository
- Check the main project documentation
- Review skill-specific documentation in each skill directory