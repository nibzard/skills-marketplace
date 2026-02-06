# Contributing to Skills Marketplace

Note: This repository is distributed as a single Claude Code plugin that bundles multiple Skills. Marketplace mode and `.claude-plugin/marketplace.json` are deprecated here. Install via `/plugin install nibzard/skills-kit` and add new Skills under `skills/<your-skill>/`.

Thank you for your interest in contributing to the Skills Marketplace! This guide will help you get started with contributing skills, improving documentation, and enhancing the marketplace ecosystem.

## Table of Contents

- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
  - [Contributing Skills](#contributing-skills)
  - [Improving Documentation](#improving-documentation)
  - [Reporting Issues](#reporting-issues)
  - [Submitting Pull Requests](#submitting-pull-requests)
- [Development Workflow](#development-workflow)
- [Guidelines and Standards](#guidelines-and-standards)
- [Review Process](#review-process)
- [Community](#community)

## Getting Started

### Prerequisites

- Claude Code installed and configured
- Basic understanding of Git and Markdown
- Familiarity with the skills you want to contribute
- For skills with scripts: knowledge of relevant programming languages

### Setup

1. **Fork the Repository**:
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/your-username/skills-kit.git
   cd skills-kit
   ```

2. **Add Upstream Remote**:
   ```bash
   git remote add upstream https://github.com/nibzard/skills-kit.git
   ```

3. **Create Development Branch**:
   ```bash
   git checkout -b feature-your-skill-name
   ```

4. **Test Plugin Locally**:
   ```bash
   # Install the plugin from the working directory
   /plugin install .
   ```

## How to Contribute

### Contributing Skills

We welcome contributions of new skills that address specific workflows and problems. Before creating a skill:

1. **Check Existing Skills**: Review the current marketplace to avoid duplication
2. **Choose a Focus**: Select a specific, well-defined capability
3. **Plan Your Skill**: Design the skill structure and functionality

#### Skill Creation Process

1. **Create Skill Directory**:
   ```bash
   mkdir skills/your-skill-name
   cd skills/your-skill-name
   ```

2. **Create SKILL.md**:
   ```yaml
   ---
   name: your-skill-name
   description: Clear description of what this skill does and when to use it
   allowed-tools: Read, Write, Edit  # Optional tool restrictions
   ---

   # Your Skill Name

   ## Instructions
   [Step-by-step guidance for Claude]

   ## Examples
   [Concrete usage examples]

   ## Requirements
   [Dependencies and prerequisites]
   ```

3. **Add Supporting Files** (Optional):
   ```bash
   mkdir scripts templates docs
   # Add helper scripts, templates, or additional documentation
   ```

4. **Test Your Skill**:
   ```bash
   # Reinstall the plugin so Claude discovers your new Skill
   /plugin install .

   # Test skill functionality
   # Ask Claude questions that should trigger your skill
   ```

5. **No Manifest Edits Required**:
   This plugin auto-discovers skills under `skills/<your-skill>/SKILL.md`. Keep content one level deep and reference any supporting files from `SKILL.md`.

#### Skill Quality Standards

**Required**:
- Clear, specific description that helps Claude discover when to use it
- Well-structured instructions that Claude can follow
- Examples showing when and how to use the skill
- Documentation of dependencies and requirements

**Recommended**:
- Tool permissions that restrict access to necessary tools only
- Supporting files (scripts, templates) that enhance functionality
- Error handling and edge case coverage
- Testing instructions or validation scripts

### Improving Documentation

We welcome improvements to all documentation, including:

#### Main Documentation
- README.md improvements and corrections
- New guides and tutorials
- Translation into other languages
- Accessibility improvements

#### Skill Documentation
- Better examples and use cases
- Additional edge case handling
- Performance optimization notes
- Troubleshooting guides

#### Developer Documentation
- API documentation improvements
- Development setup guides
- Architecture explanations
- Contributing guidelines enhancements

### Reporting Issues

Help us improve by reporting issues:

#### Bug Reports
- Clear description of the problem
- Steps to reproduce
- Expected vs. actual behavior
- Environment information (OS, Claude Code version)
- Relevant skill configurations

#### Feature Requests
- Clear description of desired functionality
- Use case and motivation
- Possible implementation approaches
- Priority and importance

#### Documentation Issues
- Specific documentation problems
- Suggestions for improvements
- Missing or unclear information
- Outdated content

### Submitting Pull Requests

1. **Create Pull Request**:
   - Use descriptive title and description
   - Reference any relevant issues
   - Include testing instructions
   - Document breaking changes

2. **PR Template**:
   ```markdown
   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Other

   ## Testing
   - [ ] Tested skill installation
   - [ ] Tested skill functionality
   - [ ] Verified documentation accuracy

   ## Checklist
   - [ ] Code follows project style guidelines
   - [ ] Self-review completed
   - [ ] Documentation updated
   - [ ] No breaking changes (or clearly documented)
   ```

## Development Workflow

### Branching Strategy

- **main**: Stable, released versions
- **develop**: Integration branch for new features
- **feature/skill-name**: Feature branches for new skills
- **hotfix/issue**: Quick fixes for critical issues

### Commit Guidelines

Use conventional commits for clarity:

```
type(scope): description

feat(git-automation): add branch conflict resolution
fix(data-analysis): handle CSV parsing errors
docs(readme): update installation instructions
style(marketplace): fix JSON formatting
```

**Types**:
- `feat`: New features or skills
- `fix`: Bug fixes
- `docs`: Documentation changes
- `style`: Code style/formatting
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Local Development

1. **Install and Test**:
   ```bash
   # Install plugin from working tree
   /plugin install .
   ```

2. **Validate Configuration**:
   ```bash
   # Validate skill structure
   /plugin validate
   ```

3. **Test Multiple Skills**:
   ```bash
   # Test skill discovery
   /plugin list

   # Test various skills to ensure no conflicts
   ```

## Guidelines and Standards

### Skill Development Guidelines

#### 1. Specific Focus
Each skill should address a specific, well-defined problem. Avoid broad, vague skills that overlap with existing functionality.

**Good Examples**:
- "Generate conventional commit messages from Git diffs"
- "Analyze Excel spreadsheets for business insights"
- "Review code for security vulnerabilities"

**Avoid**:
- "Help with files" (too broad)
- "Improve productivity" (too vague)

#### 2. Clear Discovery
Write descriptions that help Claude understand when to use your skill:

```yaml
description: Analyze Excel spreadsheets, create pivot tables, and generate business insights. Use when working with Excel files, .xlsx documents, or analyzing tabular data for business intelligence.
```

Include both:
- **Capabilities**: What the skill can do
- **Triggers**: When Claude should use it

#### 3. Comprehensive Instructions
Provide clear, step-by-step guidance:

```markdown
## Instructions
1. Check if file exists and is readable
2. Validate file format and structure
3. Process data with error handling
4. Generate appropriate output
5. Report any issues found
```

#### 4. Error Handling
Include robust error handling:

```markdown
## Instructions
1. Verify input parameters and file existence
2. Check dependencies and system requirements
3. Handle network timeouts and API failures
4. Provide clear error messages with actionable guidance
```

#### 5. Practical Examples
Provide concrete, realistic examples:

```markdown
## Examples
- "Analyze this sales data spreadsheet and identify top-performing products"
- "Create a summary report from quarterly financial data"
- "Extract insights from customer feedback spreadsheet"
```

### Documentation Standards

#### 1. Markdown Format
- Use ATX-style headings (# ## ###)
- Include tables of contents for long documents
- Use code blocks with language specification
- Add appropriate emoji for visual clarity

#### 2. Structure and Organization
- Start with brief introduction/overview
- Follow with prerequisites and setup
- Include detailed usage instructions
- End with troubleshooting and support information

#### 3. Code Examples
- Provide complete, working examples
- Include installation/setup instructions
- Show expected outputs
- Handle error cases appropriately

#### 4. Accessibility
- Use descriptive headings
- Provide alt text for images
- Use sufficient color contrast
- Write for international audience

### Testing Guidelines

#### 1. Functional Testing
Test that skills work as intended:
```bash
# Install plugin from working tree
/plugin install .

# Test skill discovery
What skills do you have available for [use case]?

# Test skill functionality
Can you help me [task that should trigger skill]?
```

#### 2. Error Testing
Test error handling:
- Invalid inputs
- Missing dependencies
- Network failures
- Permission issues

#### 3. Performance Testing
Consider performance implications:
- Large file handling
- Memory usage
- Processing time
- Resource constraints

## Review Process

### Pull Request Review

All pull requests undergo review focusing on:

#### 1. Skill Quality
- **Functionality**: Does the skill work as intended?
- **Documentation**: Is the skill well-documented?
- **Examples**: Are examples clear and helpful?
- **Error Handling**: Does the skill handle errors gracefully?

#### 2. Plugin Integration
- **Discovery**: Will Claude find and use the skill appropriately?
- **Compatibility**: Does the skill conflict with existing skills?
- **Dependencies**: Are dependencies documented and reasonable?

#### 3. Standards Compliance
- **Format**: Does the skill follow project guidelines?
- **Style**: Is the code and documentation consistent?
- **Security**: Are there any security concerns?
- **Performance**: Are there performance implications?

### Review Timeline

- **Initial Response**: Within 2-3 business days
- **Detailed Review**: Within 5-7 business days
- **Approval/Discussion**: Within 10 business days

### Merge Requirements

- **Approval Required**: At least one maintainer approval
- **Tests Passing**: All automated checks must pass
- **Documentation Updated**: Relevant documentation updated
- **No Conflicts**: No merge conflicts with main branch

## Community

### Getting Help

- **GitHub Issues**: Report bugs or request features
- **GitHub Discussions**: Ask questions and share ideas
- **Documentation**: Check existing guides and tutorials
- **Community Forum**: Connect with other contributors

### Communication Channels

- **Maintainers**: Core team responsible for project direction
- **Contributors**: Community members who contribute code and documentation
- **Users**: People who use the skills marketplace

### Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

#### Expected Behavior

- Use welcoming and inclusive language
- Be respectful of different viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy toward other community members

#### Unacceptable Behavior

- Harassment, trolling, or discriminatory language
- Personal attacks or political discussions
- Publishing private information
- Any other conduct that could be considered inappropriate

## Recognition

### Contributor Recognition

We recognize and appreciate all contributions:

- **Contributors List**: All contributors are listed in README.md
- **Release Notes**: Significant contributions are mentioned in releases
- **Blog Features**: Outstanding contributions may be featured in blog posts
- **Community Highlights**: Active contributors may be highlighted in community communications

### Types of Contributions

All types of contributions are valuable:

- **Code**: New skills, bug fixes, improvements
- **Documentation**: Guides, tutorials, examples
- **Design**: User experience improvements, visual design
- **Testing**: Bug reports, testing, quality assurance
- **Community**: Support, discussions, feedback
- **Translation**: Localizing documentation and skills

## Maintainer Guidelines

### Becoming a Maintainer

Active contributors who demonstrate commitment to the project may be invited to become maintainers. Criteria include:

- **Consistent Contributions**: Regular, high-quality contributions
- **Community Engagement**: Active participation in discussions and reviews
- **Technical Knowledge**: Strong understanding of the project and skills
- **Leadership**: Ability to guide project direction and mentor others

### Maintainer Responsibilities

- **Code Review**: Review and approve pull requests
- **Issue Triage**: Prioritize and address issues and bugs
- **Release Management**: Coordinate releases and version management
- **Community Support**: Help users and guide contributors
- **Project Direction**: Contribute to roadmap and strategic decisions

---

Thank you for contributing to the Skills Marketplace! Your contributions help make Claude Code more powerful and useful for everyone.

For questions about contributing, please:
- Open an issue on GitHub
- Start a discussion in the repository
- Contact the maintainers directly
