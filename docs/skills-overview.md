# Agent Skills Overview

Agent Skills are modular capabilities that extend Claude's functionality through organized folders containing instructions, scripts, and resources. This comprehensive guide explains how Skills work within the marketplace ecosystem.

## Understanding Agent Skills

### What are Agent Skills?

Agent Skills are self-contained packages of expertise that Claude can autonomously invoke when relevant to your request. Unlike traditional plugins or slash commands that require explicit user invocation, Skills are **model-invoked**—Claude decides when to use them based on context and the Skill's description.

### Core Concepts

#### Model-Invoked vs User-Invoked

- **Model-Invoked (Skills)**: Claude autonomously selects and uses Skills based on request context
- **User-Invoked (Commands)**: User explicitly triggers actions with slash commands like `/command`

#### Progressive Disclosure

Skills use progressive disclosure to manage context efficiently:
- **SKILL.md**: Always loaded with core instructions
- **Supporting files**: Loaded only when explicitly referenced
- **Scripts and templates**: Executed only when needed

#### Tool Permissions

Skills can specify allowed tools via `allowed-tools` frontmatter:
- Restricted tool access for security-sensitive workflows
- Fine-grained control over what Skills can do
- Reduced permission prompts for allowed tools

## Skill Anatomy

### Basic Structure

```
skill-name/
├── SKILL.md                 # Required: Main skill definition
├── reference.md             # Optional: Detailed documentation
├── examples.md              # Optional: Usage examples
├── scripts/                 # Optional: Helper scripts
│   ├── helper.py
│   └── process.sh
└── templates/               # Optional: Code/file templates
    ├── config.json
    └── template.md
```

### Frontmatter Schema

```yaml
---
name: skill-identifier        # Required: lowercase, numbers, hyphens only (max 64 chars)
description: Brief description of what this skill does and when to use it (max 1024 chars)
allowed-tools: Read, Grep, Glob  # Optional: Restrict tool access
---

# Skill Content
```

#### Required Fields

- **name**: Unique identifier (kebab-case, no spaces, max 64 characters)
- **description**: When to use the skill (max 1024 characters) - critical for discovery

#### Optional Fields

- **allowed-tools**: Comma-separated list of tools the skill can use without permission prompts

### Content Structure

```markdown
# Skill Title

## Instructions
Clear, step-by-step guidance for Claude

## Examples
Concrete examples of when and how to use this skill

## Requirements
List any required packages, tools, or dependencies

## Notes
Additional context, limitations, or considerations
```

## Skill Discovery and Invocation

### How Claude Discovers Skills

Claude discovers Skills from three sources:

1. **Personal Skills**: `~/.claude/skills/`
2. **Project Skills**: `.claude/skills/`
3. **Plugin Skills**: Bundled with installed plugins

### Selection Process

When you make a request, Claude:

1. **Analyzes Request**: Examines your question/task for key indicators
2. **Matches Descriptions**: Compares request context with Skill descriptions
3. **Selects Best Match**: Chooses the most relevant Skill based on description match
4. **Loads Skill**: Reads SKILL.md and follows instructions
5. **Executes Workflow**: Uses the Skill to address your request

### Description Best Practices

#### Effective Descriptions Include:

- **What the skill does**: Primary capabilities and functions
- **When to use it**: Specific triggers, keywords, and contexts
- **Key terms**: Words users would mention when needing this skill

#### Examples:

**Good Description:**
```
description: Analyze Excel spreadsheets, create pivot tables, and generate charts. Use when working with Excel files, spreadsheets, or analyzing tabular data in .xlsx format.
```

**Poor Description:**
```
description: Helps with files
```

## Available Skills

### 🛠️ Development Tools

#### git-automation
- **Description**: Automate Git workflows, generate commit messages, manage branches, and handle repository operations. Use when working with Git repositories, making commits, or managing version control.
- **Key Features**:
  - Automatic commit message generation from diffs
  - Branch management and merging guidance
  - Repository hygiene and best practices
- **Use Cases**: Daily Git operations, commit message writing, branch strategy

#### code-reviewer
- **Description**: Review code for best practices, security issues, and maintainability. Use when reviewing pull requests, analyzing code quality, or checking for potential issues.
- **Key Features**:
  - Security vulnerability detection
  - Code style and pattern analysis
  - Performance and maintainability feedback
- **Use Cases**: PR reviews, code quality checks, security audits

#### documentation-helper
- **Description**: Generate, update, and maintain technical documentation. Use when creating README files, API docs, or code comments.
- **Key Features**:
  - README generation from code analysis
  - API documentation creation
  - Documentation maintenance and updates
- **Use Cases**: Project documentation, API docs, code commenting

### 📊 Data & Analytics

#### data-analysis
- **Description**: Process, analyze, and visualize data from various sources. Use when working with spreadsheets, CSV files, or performing statistical analysis.
- **Key Features**:
  - Excel and CSV processing
  - Statistical analysis and insights
  - Data visualization guidance
- **Use Cases**: Data processing, statistical analysis, report generation

#### report-generator
- **Description**: Create structured reports from data sources and analysis results. Use when generating business reports, summaries, or analytical findings.
- **Key Features**:
  - Template-based report generation
  - Data integration and formatting
  - Executive summary creation
- **Use Cases**: Business reports, project summaries, analytical findings

### 🚀 DevOps & Infrastructure

#### deployment-tools
- **Description**: Manage CI/CD pipelines, deployment configurations, and infrastructure automation. Use when deploying applications, managing pipelines, or configuring infrastructure.
- **Key Features**:
  - CI/CD pipeline configuration
  - Deployment automation scripts
  - Infrastructure as code guidance
- **Use Cases**: Application deployment, pipeline management, infrastructure setup

#### monitoring-helper
- **Description**: Analyze logs, monitor system performance, and troubleshoot issues. Use when debugging applications, analyzing system metrics, or investigating incidents.
- **Key Features**:
  - Log analysis and pattern detection
  - Performance monitoring and alerting
  - Incident investigation and debugging
- **Use Cases**: System monitoring, log analysis, incident response

### 🔒 Security

#### security-scanner
- **Description**: Scan code and systems for security vulnerabilities, compliance issues, and security best practices. Use when conducting security audits, vulnerability assessments, or compliance checks.
- **Key Features**:
  - Vulnerability scanning and analysis
  - Security best practices enforcement
  - Compliance checking and reporting
- **Use Cases**: Security audits, vulnerability assessment, compliance verification

### 📈 Productivity

#### task-manager
- **Description**: Organize tasks, plan projects, and track progress. Use when managing projects, creating action items, or organizing workflows.
- **Key Features**:
  - Task breakdown and prioritization
  - Project planning and scheduling
  - Progress tracking and reporting
- **Use Cases**: Project management, task organization, workflow planning

#### meeting-assistant
- **Description**: Prepare for meetings, take notes, and manage action items. Use when organizing meetings, taking notes, or following up on discussions.
- **Key Features**:
  - Meeting preparation and agenda creation
  - Real-time note taking and summarization
  - Action item tracking and follow-up
- **Use Cases**: Meeting management, note taking, action item tracking

## Skill Categories

### Development Tools
Focus on software development, coding, and technical workflows.

**Common Patterns:**
- Code analysis and generation
- Build and deployment automation
- Testing and quality assurance
- Version control and repository management

### Data & Analytics
Centered around data processing, analysis, and visualization.

**Common Patterns:**
- Data cleaning and transformation
- Statistical analysis and modeling
- Visualization and reporting
- Database operations and queries

### Documentation
Skills for creating, maintaining, and organizing documentation.

**Common Patterns:**
- Technical writing and editing
- Template-based document generation
- API documentation creation
- README and guide maintenance

### DevOps & Infrastructure
Focused on deployment, operations, and infrastructure management.

**Common Patterns:**
- CI/CD pipeline automation
- Infrastructure as code
- Monitoring and alerting
- System administration and maintenance

### Security
Skills for security analysis, vulnerability scanning, and compliance.

**Common Patterns:**
- Security vulnerability detection
- Compliance checking and auditing
- Security best practices enforcement
- Incident response and analysis

### Productivity
General productivity tools and workflow optimization.

**Common Patterns:**
- Task management and organization
- Communication automation
- Meeting management and follow-up
- Workflow optimization

## Using Skills

### Automatic Invocation

Skills are automatically invoked when Claude determines they're relevant:

```bash
# Claude will automatically use git-automation skill
"I just made some changes to my code. Can you help me write a good commit message?"

# Claude will automatically use data-analysis skill
"Can you analyze this spreadsheet and tell me what insights you find?"

# Claude will automatically use code-reviewer skill
"Please review this pull request for any potential issues"
```

### Manual Skill Inspection

You can manually inspect available skills:

```bash
# List all available skills
What Skills are available?

# Get details about a specific skill
Tell me more about the git-automation skill

# Check your personal skills
ls ~/.claude/skills/

# Check project skills
ls .claude/skills/
```

### Skill Selection Criteria

Claude considers multiple factors when selecting skills:

1. **Description Match**: How well the request matches the skill's description
2. **Context Relevance**: Current project and file context
3. **Keyword Presence**: Specific terms in your request
4. **Skill Capabilities**: What the skill can actually do
5. **Tool Requirements**: Whether the skill needs specific tools

## Advanced Features

### Tool Permissions

Control what tools skills can access:

```yaml
---
name: safe-file-reader
description: Read files without making changes. Use for read-only file access.
allowed-tools: Read, Grep, Glob
---
```

**Benefits:**
- Security: Prevent unintended modifications
- Focus: Limit skills to their intended scope
- Efficiency: Reduce permission prompts

### Dependencies and Requirements

Skills can specify dependencies in their descriptions:

```markdown
## Requirements
- Python 3.8+
- pandas and numpy packages
- Access to database connection
```

Claude will automatically install required packages or ask for permission when needed.

### Progressive Disclosure

Skills load additional files only when referenced:

```markdown
# In SKILL.md
For advanced features, see [reference documentation](reference.md).

# When needed, Claude reads reference.md
For data processing examples, check the [examples guide](examples.md).

# Scripts are executed only when explicitly called
Run the analysis script:
```bash
python scripts/analyze.py input.csv
```
```

## Skill Integration

### With Plugins

Skills can be bundled with plugins:

```
plugin/
├── plugin.json
├── skills/
│   ├── skill-1/
│   └── skill-2/
└── commands/
```

Plugin skills are automatically available when the plugin is installed.

### With Marketplaces

Skills are distributed through marketplaces:

```json
{
  "plugins": [
    {
      "name": "my-skill",
      "source": "./skills/my-skill",
      "category": "development-tools",
      "keywords": ["automation", "productivity"]
    }
  ]
}
```

### Team Distribution

Skills can be shared across teams through:

1. **Project Skills**: Checked into git repositories
2. **Private Marketplaces**: Organization-specific skill collections
3. **Plugin Distribution**: Bundled with custom plugins

## Best Practices

### For Skill Users

1. **Understand When Skills Activate**: Learn what triggers skill invocation
2. **Provide Clear Context**: Give Claude enough information for skill selection
3. **Review Skill Output**: Verify that skills are working as expected
4. **Give Feedback**: Report issues or suggest improvements

### For Skill Developers

1. **Write Specific Descriptions**: Help Claude understand when to use your skill
2. **Include Examples**: Show concrete use cases and expected outcomes
3. **Specify Requirements**: List all dependencies and prerequisites
4. **Test Thoroughly**: Ensure skills work in various contexts
5. **Document Clearly**: Provide comprehensive instructions and examples

### For Team Managers

1. **Curate Skill Collections**: Build relevant skill sets for your team
2. **Establish Guidelines**: Set standards for skill creation and usage
3. **Monitor Usage**: Track which skills are most valuable
4. **Encourage Sharing**: Promote skill contribution and improvement

## Troubleshooting

### Skill Not Invoked

**Symptoms**: Relevant skill exists but Claude doesn't use it

**Solutions**:
1. **Check Description**: Is it specific enough for Claude to match?
2. **Verify Context**: Does your request match the skill's triggers?
3. **Confirm Availability**: Is the skill properly installed?
4. **Review Keywords**: Does your request contain the right terms?

### Skill Errors

**Symptoms**: Skill activates but produces errors

**Solutions**:
1. **Check Dependencies**: Are required packages installed?
2. **Verify Permissions**: Does the skill have necessary tool access?
3. **Review Instructions**: Are the skill's instructions clear and correct?
4. **Test Scripts**: Do helper scripts have execute permissions?

### Multiple Skills Conflict

**Symptoms**: Claude uses wrong skill or seems confused

**Solutions**:
1. **Improve Descriptions**: Make skill descriptions more distinct
2. **Add Context**: Provide more specific information in your request
3. **Use Specific Language**: Include keywords that target the right skill

## Future Developments

### Enhanced Skill Discovery
- Improved matching algorithms
- Category-based browsing
- Skill rating and recommendation system

### Advanced Features
- Skill composition and chaining
- Dynamic skill loading
- Context-aware skill selection

### Tool Integration
- Integration with external APIs
- Custom tool development
- Enhanced permission management

---

**Next Steps**:
- Learn [how to create your own skills](skills-development.md)
- Explore [marketplace management](marketplace-management.md)
- Check out the [API reference](api-reference.md)