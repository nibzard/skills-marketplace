# Marketplace Management Guide

This comprehensive guide covers how to create, manage, and distribute skills marketplaces for Claude Code. Learn how to set up marketplaces for teams, organizations, and public communities.

## Overview

A skills marketplace is a centralized catalog that makes it easy to discover, install, and manage Agent Skills. Marketplaces provide:

- **Centralized Discovery**: Browse skills from multiple sources in one place
- **Version Management**: Track and update skill versions automatically
- **Team Distribution**: Share required skills across your organization
- **Flexible Sources**: Support for git repositories, GitHub repos, local paths, and package managers

## Marketplace Types

### Public Marketplaces
- **Open Access**: Available to anyone with Claude Code
- **Community Driven**: Skills contributed by developers worldwide
- **GitHub Hosted**: Easy discovery and installation
- **Examples**: Official Claude Code marketplace, community collections

### Private Marketplaces
- **Organization Only**: Restricted to company employees or team members
- **Custom Skills**: Proprietary tools and workflows
- **Security Focused**: Internal security policies and compliance
- **Self-Hosted**: Deployed on internal git infrastructure

### Development Marketplaces
- **Testing**: Skills under development and testing
- **Local Development**: Skills being actively developed
- **Staging**: Pre-release skills for validation
- **Feature Branches**: Experimental features and capabilities

## Creating a Marketplace

### Prerequisites

- Claude Code installed and running
- Git repository (GitHub, GitLab, or other git hosting)
- Basic familiarity with JSON file format
- One or more skills to distribute

### Step 1: Repository Setup

Create a new git repository for your marketplace:

```bash
# Create new repository
mkdir my-skills-marketplace
cd my-skills-marketplace
git init

# Create directory structure
mkdir -p .claude-plugin skills docs examples
```

### Step 2: Create Marketplace Configuration

Create `.claude-plugin/marketplace.json`:

```json
{
  "name": "my-skills-marketplace",
  "owner": {
    "name": "Your Name/Organization",
    "email": "contact@example.com"
  },
  "metadata": {
    "description": "A collection of custom skills for specific workflows",
    "version": "1.0.0",
    "homepage": "https://github.com/your-org/my-skills-marketplace",
    "license": "MIT"
  },
  "plugins": [
    {
      "name": "example-skill",
      "source": "./skills/example-skill",
      "description": "An example skill for demonstration purposes",
      "version": "1.0.0",
      "author": {
        "name": "Skill Author",
        "email": "author@example.com"
      },
      "category": "productivity",
      "keywords": ["example", "demonstration", "workflow"],
      "license": "MIT"
    }
  ]
}
```

### Step 3: Add Skills

Add skills to the `skills/` directory:

```bash
# Add a skill
mkdir skills/my-skill
cat > skills/my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: Demonstrate skill marketplace functionality. Use when testing marketplace installation and skill discovery.
---

# My Skill

## Instructions
1. Demonstrate marketplace functionality
2. Show skill discovery and invocation
3. Provide example usage patterns

## Examples
- Testing marketplace installation
- Validating skill discovery
- Demonstrating skill invocation
EOF
```

### Step 4: Deploy and Share

Deploy your marketplace and make it available:

```bash
# Commit and push to git
git add .
git commit -m "Initial marketplace setup"
git remote add origin https://github.com/your-org/my-skills-marketplace.git
git push -u origin main

# Share with users:
# /plugin marketplace add your-org/my-skills-marketplace
```

## Marketplace Configuration

### Required Fields

| Field | Type | Description |
| :----- | :--- | :---------- |
| `name` | string | Marketplace identifier (kebab-case, no spaces) |
| `owner` | object | Marketplace maintainer information |
| `plugins` | array | List of available skills |

### Optional Metadata

| Field | Type | Description |
| :----- | :--- | :---------- |
| `metadata.description` | string | Brief marketplace description |
| `metadata.version` | string | Marketplace version |
| `metadata.homepage` | string | Marketplace homepage URL |
| `metadata.license` | string | SPDX license identifier |
| `metadata.pluginRoot` | string | Base path for relative skill sources |

### Plugin Entry Schema

Each skill entry in the `plugins` array supports these fields:

#### Required Fields

| Field | Type | Description |
| :----- | :--- | :---------- |
| `name` | string | Skill identifier (kebab-case, no spaces) |
| `source` | string\|object | Where to fetch the skill from |

#### Optional Fields

| Field | Type | Description |
| :----- | :--- | :---------- |
| `description` | string | Brief skill description |
| `version` | string | Skill version |
| `author` | object | Skill author information |
| `homepage` | string | Skill homepage or documentation URL |
| `repository` | string | Source code repository URL |
| `license` | string | SPDX license identifier |
| `keywords` | array | Tags for skill discovery |
| `category` | string | Skill category for organization |
| `tags` | array | Additional tags for searchability |
| `strict` | boolean | Require SKILL.md (default: true) |
| `commands` | string\|array | Custom paths to command files |
| `agents` | string\|array | Custom paths to agent files |
| `hooks` | string\|object | Custom hooks configuration |
| `mcpServers` | string\|object | MCP server configurations |

## Skill Sources

### Relative Paths

For skills in the same repository:

```json
{
  "name": "local-skill",
  "source": "./skills/local-skill"
}
```

### GitHub Repositories

```json
{
  "name": "github-skill",
  "source": {
    "source": "github",
    "repo": "owner/skill-repo"
  }
}
```

### Git Repositories

```json
{
  "name": "git-skill",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/skill.git"
  }
}
```

### Direct URLs

```json
{
  "name": "url-skill",
  "source": "https://example.com/skill.tar.gz"
}
```

## Installation Methods

### For End Users

#### Install from GitHub Marketplace

```bash
# Add marketplace
/plugin marketplace add your-org/my-skills-marketplace

# Browse available skills
/plugin

# Install specific skill
/plugin install skill-name@marketplace-name
```

#### Install from Git Repository

```bash
# Add any git repository
/plugin marketplace add https://gitlab.com/company/marketplace.git

# Install skills
/plugin install skill-name@marketplace-name
```

#### Install from Local Directory

```bash
# Add local marketplace for development
/plugin marketplace add ./my-marketplace

# Test installation
/plugin install test-skill@my-marketplace
```

### For Teams and Organizations

#### Configure in Project Settings

Create `.claude/settings.json` in your project:

```json
{
  "extraKnownMarketplaces": {
    "team-skills": {
      "source": {
        "source": "github",
        "repo": "your-org/team-skills"
      }
    },
    "company-tools": {
      "source": {
        "source": "git",
        "url": "https://git.company.com/skills.git"
      }
    }
  },
  "enabledPlugins": [
    "git-automation@team-skills",
    "code-reviewer@company-tools"
  ]
}
```

#### Automatic Installation for Trusted Repositories

When team members trust a repository folder, Claude Code automatically:

1. Installs configured marketplaces
2. Installs specified skills from `enabledPlugins`
3. Makes skills available without manual intervention

## Marketplace Operations

### Managing Marketplaces

#### List Marketplaces

```bash
# List all configured marketplaces
/plugin marketplace list
```

Output:
```
Known Marketplaces:
- skills-marketplace (local) - /path/to/skills-marketplace
- team-skills (github) - your-org/team-skills
- official (github) - anthropics/claude-code
```

#### Update Marketplace

```bash
# Refresh marketplace metadata and skill listings
/plugin marketplace update marketplace-name
```

This operation:
- Fetches latest marketplace configuration
- Updates skill metadata and versions
- Detects new and removed skills
- Refreshes skill descriptions and categories

#### Remove Marketplace

```bash
# Remove marketplace from configuration
/plugin marketplace remove marketplace-name
```

**Warning**: Removing a marketplace will uninstall all skills installed from it.

### Skill Management

#### Install Skills

```bash
# Install specific skill from marketplace
/plugin install skill-name@marketplace-name

# Install without specifying marketplace (searches all)
/plugin install skill-name

# Install specific version
/plugin install skill-name@1.2.3@marketplace-name
```

#### List Installed Skills

```bash
# Show all installed skills and their sources
/plugin list

# Get details about specific skill
/plugin info skill-name
```

#### Update Skills

```bash
# Update specific skill to latest version
/plugin update skill-name

# Update all skills from a marketplace
/plugin update --all

# Update marketplace first, then skills
/plugin marketplace update marketplace-name && /plugin update --all
```

#### Uninstall Skills

```bash
# Remove specific skill
/plugin uninstall skill-name

# Remove all skills from marketplace
/plugin uninstall --all marketplace-name
```

## Hosting Strategies

### GitHub Hosting (Recommended)

**Benefits:**
- Built-in version control and collaboration
- Issue tracking and pull requests
- Easy sharing and discovery
- GitHub Actions integration
- Free for public repositories

**Setup:**
```bash
# Create repository
gh repo create your-org/skills-marketplace --public --clone
cd skills-marketplace

# Add marketplace configuration
# Add skills

# Push to GitHub
git push origin main
```

**Best Practices:**
- Use semantic versioning
- Maintain clear commit history
- Use branches for skill development
- Enable issue templates for feedback
- Set up GitHub Actions for validation

### GitLab Hosting

**Benefits:**
- Self-hosting options
- Integrated CI/CD
- Advanced permission controls
- Enterprise features

**Setup:**
```bash
# Create repository on GitLab
# Clone repository
git clone https://gitlab.com/your-org/skills-marketplace.git
cd skills-marketplace

# Add marketplace configuration and skills
git add .
git commit -m "Initial marketplace setup"
git push origin main
```

### Self-Hosted Git

**Benefits:**
- Complete control over infrastructure
- Enhanced security for proprietary skills
- Custom integration possibilities
- Internal compliance requirements

**Setup:**
```bash
# Setup internal git server
# Create repository
git clone https://git.company.com/skills-marketplace.git
cd skills-marketplace

# Configure marketplace
git add .
git commit -m "Internal skills marketplace"
git push origin main
```

### Static File Hosting

**Benefits:**
- Simple deployment
- Fast access
- CDN integration
- No git dependencies

**Setup:**
```bash
# Create marketplace.json
# Host on web server or CDN
# Users add via URL:
/plugin marketplace add https://company.com/marketplace.json
```

## Team Management

### Setting Up Team Marketplaces

#### 1. Create Organization Repository

```bash
# Create organization repository on GitHub
# Add team members with appropriate permissions
# Set up branch protection rules
# Configure team access controls
```

#### 2. Configure Access Controls

**GitHub Teams:**
- Create teams for different access levels
- Assign repository permissions (read, write, admin)
- Use branch protection for quality control

**Access Levels:**
- **Read**: Can install and use skills
- **Write**: Can contribute and modify skills
- **Admin**: Can manage marketplace configuration

#### 3. Establish Workflow

**Development Workflow:**
```bash
# 1. Create feature branch
git checkout -b new-skill-feature

# 2. Add or modify skill
mkdir skills/new-skill
# Create skill files

# 3. Test locally
/plugin marketplace add ./skills-marketplace
/plugin install new-skill@skills-marketplace

# 4. Commit and create pull request
git add .
git commit -m "Add new-skill for specific workflow"
git push origin new-skill-feature
# Create PR on GitHub
```

**Review Process:**
- Code review for skill quality
- Security review for sensitive skills
- Testing review for functionality
- Documentation review for clarity

### Onboarding Team Members

#### 1. Initial Setup

```bash
# Clone repository
git clone https://github.com/your-org/skills-marketplace.git
cd skills-marketplace

# Add marketplace to Claude Code
/plugin marketplace add ./skills-marketplace

# Install required skills
/plugin install git-automation@skills-marketplace
/plugin install code-reviewer@skills-marketplace
```

#### 2. Project Configuration

Create `.claude/settings.json` in team projects:

```json
{
  "extraKnownMarketplaces": {
    "team-skills": {
      "source": {
        "source": "github",
        "repo": "your-org/skills-marketplace"
      }
    }
  },
  "enabledPlugins": [
    "git-automation@team-skills",
    "code-reviewer@team-skills"
  ]
}
```

#### 3. Documentation and Training

**Team Documentation:**
- Create onboarding guide
- Document custom skills and usage
- Provide examples and workflows
- Establish best practices

**Training Sessions:**
- Introduction to Agent Skills
- Custom skill walkthroughs
- Marketplace usage training
- Troubleshooting and support

## Validation and Testing

### Marketplace Validation

#### JSON Schema Validation

```bash
# Validate marketplace configuration
claude plugin validate .

# Check for syntax errors
cat .claude-plugin/marketplace.json | jq .
```

#### Skill Validation

```bash
# Validate skill structure
claude plugin validate ./skills/skill-name

# Test skill installation
/plugin marketplace add ./skills-marketplace
/plugin install skill-name@skills-marketplace
```

### Testing Strategies

#### Local Testing

```bash
# Test marketplace locally
/plugin marketplace add ./skills-marketplace

# Test skill installation
/plugin install test-skill@skills-marketplace

# Test skill functionality
# Ask Claude to use the skill
```

#### Staging Environment

```bash
# Create staging branch
git checkout -b staging

# Deploy to staging repository
git push origin staging

# Test staging marketplace
/plugin marketplace add https://github.com/your-org/skills-marketplace/tree/staging
```

#### Automated Testing

**GitHub Actions Example:**
```yaml
name: Validate Marketplace

on:
  push:
    branches: [ main, staging ]
  pull_request:
    branches: [ main ]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Setup Claude Code
      run: |
        curl -fsSL https://code.claude.com/install.sh | sh

    - name: Validate marketplace
      run: claude plugin validate .

    - name: Test skill installation
      run: |
        claude plugin marketplace add .
        claude plugin install test-skill
```

### Quality Assurance

#### Skill Quality Checklist

- [ ] Skill has clear, specific description
- [ ] SKILL.md follows best practices
- [ ] Examples are provided and tested
- [ ] Dependencies are documented
- [ ] Tool permissions are appropriate
- [ ] Error handling is robust
- [ ] Documentation is comprehensive

#### Marketplace Quality Checklist

- [ ] JSON syntax is valid
- [ ] All skill sources are accessible
- [ ] Skills install without errors
- [ ] Categories and keywords are consistent
- [ ] Version information is maintained
- [ ] License information is complete
- [ ] Contact information is current

## Troubleshooting

### Common Issues

#### Marketplace Not Loading

**Symptoms:**
- Can't add marketplace
- `/plugin marketplace list` doesn't show marketplace
- Skills not visible from marketplace

**Solutions:**
1. **Verify URL/Path**: Ensure marketplace source is accessible
2. **Check File Path**: Confirm `.claude-plugin/marketplace.json` exists
3. **Validate JSON**: Check JSON syntax with validation tools
4. **Check Permissions**: Verify git access for private repositories
5. **Network Issues**: Ensure internet connectivity for remote sources

**Debug Commands:**
```bash
# Validate JSON syntax
cat .claude-plugin/marketplace.json | jq .

# Test repository access
git ls-remote https://github.com/owner/repo.git

# Check file exists
ls -la .claude-plugin/marketplace.json

# Test with debug mode
claude --debug plugin marketplace add ./marketplace
```

#### Skill Installation Failures

**Symptoms:**
- Marketplace loads but skill installation fails
- Skills install but don't work correctly
- Version conflicts or dependency issues

**Solutions:**
1. **Check Skill Sources**: Verify skill URLs and paths are accessible
2. **Validate Skill Structure**: Ensure SKILL.md exists and is valid
3. **Check Dependencies**: Verify required packages are available
4. **Test Manually**: Try cloning/installing skills manually
5. **Check Permissions**: Ensure necessary tool access is available

**Debug Commands:**
```bash
# Test skill source accessibility
git clone https://github.com/owner/skill-repo.git

# Validate skill structure
ls -la skills/skill-name/
cat skills/skill-name/SKILL.md

# Test installation with verbose output
claude --debug plugin install skill-name@marketplace
```

#### Version Conflicts

**Symptoms:**
- Multiple versions of same skill
- Outdated skill behavior
- Update failures

**Solutions:**
1. **Update Marketplace**: Refresh marketplace metadata
2. **Reinstall Skills**: Remove and reinstall affected skills
3. **Check Versions**: Verify version compatibility
4. **Clear Cache**: Restart Claude Code to clear caches

**Debug Commands:**
```bash
# Check installed versions
/plugin list

# Update marketplace
/plugin marketplace update marketplace-name

# Reinstall skill
/plugin uninstall skill-name
/plugin install skill-name@marketplace-name
```

### Performance Issues

#### Slow Marketplace Loading

**Causes:**
- Large number of skills
- Remote repository latency
- Complex skill configurations
- Network connectivity issues

**Optimizations:**
- Use local marketplaces for development
- Limit skill count per marketplace
- Optimize skill descriptions for faster matching
- Use CDN for static file hosting

#### Memory Usage

**Causes:**
- Many installed skills
- Large skill files
- Complex skill dependencies
- Insufficient system resources

**Solutions:**
- Remove unused skills
- Optimize skill file sizes
- Use progressive disclosure effectively
- Monitor system resources

## Best Practices

### Marketplace Design

#### 1. Clear Organization

```json
{
  "name": "company-dev-tools",
  "metadata": {
    "description": "Development tools and workflows for Company XYZ engineering team",
    "version": "2.1.0"
  }
}
```

#### 2. Consistent Categories

Use standard categories:
- `development-tools`
- `data-analytics`
- `productivity`
- `security`
- `documentation`
- `devops`

#### 3. Comprehensive Metadata

```json
{
  "name": "git-automation",
  "description": "Automated Git workflows and repository management",
  "category": "development-tools",
  "keywords": ["git", "automation", "workflow", "repository"],
  "author": {
    "name": "DevTools Team",
    "email": "devtools@company.com"
  },
  "homepage": "https://docs.company.com/tools/git-automation",
  "license": "MIT",
  "version": "1.2.0"
}
```

### Skill Management

#### 1. Version Control

- Use semantic versioning (major.minor.patch)
- Maintain CHANGELOG for significant changes
- Tag releases in git repository
- Document breaking changes

#### 2. Quality Assurance

- Test skills in various contexts
- Validate skill descriptions for discovery
- Ensure tool permissions are appropriate
- Document dependencies clearly

#### 3. Documentation Standards

```markdown
---
name: skill-name
description: Clear description of what this skill does and when to use it
---

# Skill Name

## Quick Start
Brief getting started instructions

## Instructions
Step-by-step guidance for Claude

## Examples
Concrete usage examples

## Requirements
Dependencies and prerequisites

## Notes
Additional context or limitations
```

### Team Collaboration

#### 1. Contribution Guidelines

- Create CONTRIBUTING.md file
- Define skill submission process
- Establish code review standards
- Set up testing requirements

#### 2. Communication Channels

- Use GitHub Issues for bug reports
- Set up discussions for feature requests
- Create communication channels for team coordination
- Document escalation procedures

#### 3. Change Management

- Use feature branches for development
- Implement pull request reviews
- Maintain release notes
- Communicate changes to team

### Security Considerations

#### 1. Access Control

- Use private repositories for sensitive skills
- Implement appropriate team permissions
- Regular audits of repository access
- Secure credential management

#### 2. Skill Validation

- Review skill code for security issues
- Validate tool permissions are minimal
- Test skill behavior with edge cases
- Document security considerations

#### 3. Compliance

- Ensure skills meet organizational policies
- Document data handling practices
- Validate external dependencies
- Maintain audit trails

## Advanced Features

### Skill Dependencies

Declare skill dependencies in marketplace:

```json
{
  "name": "advanced-workflow",
  "source": "./skills/advanced-workflow",
  "dependencies": [
    "git-automation@1.0.0+",
    "code-reviewer@2.0.0+"
  ]
}
```

### Conditional Installation

Configure skills based on environment:

```json
{
  "plugins": [
    {
      "name": "enterprise-feature",
      "source": "./skills/enterprise",
      "condition": {
        "environment": "enterprise",
        "license": "valid"
      }
    }
  ]
}
```

### Skill Updates and Notifications

Configure automatic update policies:

```json
{
  "metadata": {
    "autoUpdate": true,
    "updateNotification": "email",
    "updateChannel": "stable"
  }
}
```

### Analytics and Usage Tracking

Track skill usage and performance:

```json
{
  "metadata": {
    "analytics": {
      "enabled": true,
      "endpoint": "https://analytics.company.com",
      "events": ["install", "usage", "error"]
    }
  }
}
```

## Future Roadmap

### Enhanced Marketplace Features

- **Skill Rating System**: Community ratings and reviews
- **Advanced Search**: Category filtering, keyword search
- **Dependency Management**: Automatic dependency resolution
- **Usage Analytics**: Skill usage statistics and insights

### Integration Improvements

- **Package Manager Integration**: npm, pip, cargo integration
- **CI/CD Integration**: Automated skill testing and deployment
- **IDE Integration**: VS Code, IntelliJ marketplace integration
- **Web Interface**: Browser-based skill browsing and management

### Enterprise Features

- **Skill Approval Workflow**: Multi-level approval for skill publication
- **Security Scanning**: Automated security vulnerability scanning
- **Compliance Reporting**: Built-in compliance and audit reporting
- **Custom Branding**: White-label marketplace for organizations

---

**Next Steps**:
- [Create your first marketplace](#creating-a-marketplace)
- [Set up team distribution](#team-management)
- [Learn about skill development](skills-development.md)
- [Explore API reference](api-reference.md)