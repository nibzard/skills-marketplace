# Skills Development Guide

Note: This repository is distributed as a single plugin bundling multiple Skills. Marketplace examples in this document are general; for this repo install via `/plugin install nibzard/skills-kit`.

This comprehensive guide covers how to create, test, and distribute Agent Skills for Claude Code. Learn best practices for skill development, testing strategies, and deployment workflows.

## Overview

Agent Skills are modular capabilities that extend Claude's functionality through organized folders containing instructions, scripts, and resources. This guide walks you through creating high-quality skills that integrate seamlessly with Claude's autonomous selection system.

## Prerequisites

- Claude Code version 1.0 or later
- Basic familiarity with Markdown and JSON
- Understanding of your target workflow or problem domain
- For advanced skills: knowledge of scripting languages (Python, bash, etc.)

## Skill Structure

### Basic Anatomy

```
skill-name/
├── SKILL.md                 # Required: Main skill definition
├── reference.md             # Optional: Detailed documentation
├── examples.md              # Optional: Usage examples
├── scripts/                 # Optional: Helper scripts and tools
│   ├── analyze.py
│   ├── process.sh
│   └── utils/
├── templates/               # Optional: Code and file templates
│   ├── config.json
│   ├── report.md
│   └── email.txt
└── tests/                   # Optional: Test files and validation
    ├── test_cases.md
    └── expected_outputs/
```

### File Purposes

- **SKILL.md**: Core skill definition with frontmatter and instructions
- **reference.md**: Extended documentation, API references, advanced usage
- **examples.md**: Detailed examples with expected inputs and outputs
- **scripts/**: Executable scripts that extend Claude's capabilities
- **templates/**: Reusable templates for consistent output formatting
- **tests/**: Test cases for validating skill behavior

## Creating Your First Skill

### Step 1: Choose a Focus

Select a specific, well-defined capability:

**Good Examples:**
- "Generate commit messages from Git diffs"
- "Analyze Excel spreadsheets for insights"
- "Review code for security vulnerabilities"
- "Create meeting summaries from transcripts"

**Avoid:**
- "Help with documents" (too broad)
- "Fix bugs" (too vague)
- "Write code" (too general)

### Step 2: Create Skill Directory

```bash
# Personal skill (for your use only)
mkdir -p ~/.claude/skills/my-skill

# Project skill (shared with team)
mkdir -p .claude/skills/my-skill

# Plugin skill (bundled with plugin)
mkdir -p my-plugin/skills/my-skill
```

### Step 3: Write SKILL.md

Create the main skill file with proper frontmatter:

```yaml
---
name: excel-analyzer
description: Analyze Excel spreadsheets, extract insights, and generate reports. Use when working with Excel files, .xlsx documents, or analyzing tabular data for business insights.
allowed-tools: Read, Write, Bash
---

# Excel Analyzer

## Instructions
1. Identify the Excel file(s) to analyze
2. Read and examine the spreadsheet structure and content
3. Look for patterns, trends, and insights in the data
4. Generate appropriate charts or visualizations if helpful
5. Create a summary report with key findings

## Capabilities
- Data extraction and cleaning
- Statistical analysis and trend identification
- Chart and visualization generation
- Report creation and formatting

## Requirements
- Python with pandas and matplotlib installed
- Excel files in .xlsx or .csv format
- Sufficient system memory for large datasets

## Examples
- "Analyze this sales data and identify top-performing products"
- "Extract insights from customer feedback spreadsheet"
- "Create a report from quarterly financial data"
```

### Step 4: Test Your Skill

Test that Claude can discover and use your skill:

```bash
# Test discovery
Claude, what skills do you have available for working with Excel files?

# Test invocation
Can you help me analyze this spreadsheet and find trends?
```

## Frontmatter Specification

### Required Fields

#### name
- **Format**: kebab-case, lowercase letters, numbers, hyphens only
- **Maximum**: 64 characters
- **Purpose**: Unique identifier for the skill
- **Example**: `excel-data-analyzer`

#### description
- **Format**: Clear, specific description
- **Maximum**: 1024 characters
- **Purpose**: Help Claude discover when to use this skill
- **Content**: Should include both what the skill does AND when to use it

**Effective Description Structure:**
```
[Primary capabilities]. Use when [specific triggers, contexts, or user scenarios].
```

**Examples:**

**Good:**
```
description: Analyze Excel spreadsheets, create pivot tables, and generate charts. Use when working with Excel files, spreadsheets, or analyzing tabular data in .xlsx format for business insights.
```

**Poor:**
```
description: Helps with Excel files
```

### Optional Fields

#### allowed-tools
- **Format**: Comma-separated list of tool names
- **Purpose**: Restrict what tools the skill can use without permission prompts
- **Benefits**: Security, focus, reduced permission friction

**Available Tools:**
- `Read`: File reading capabilities
- `Write`: File writing and editing
- `Edit`: File content modification
- `Bash`: Command execution
- `Grep`: Pattern searching
- `Glob`: File pattern matching
- `WebSearch`: Web search functionality

**Example:**
```yaml
allowed-tools: Read, Write, Grep
```

#### Custom Frontmatter
You can add custom frontmatter for your own documentation or tooling:

```yaml
---
name: custom-skill
description: A custom skill with additional metadata
author: "Your Name"
version: "1.2.0"
category: "data-analysis"
tags: ["excel", "analytics", "reporting"]
requires: ["python", "pandas", "matplotlib"]
---
```

## Content Guidelines

### Structure Template

```markdown
---
name: your-skill-name
description: [Clear description of capabilities and usage triggers]
allowed-tools: [Optional tool restrictions]
---

# Skill Title

## Quick Start
[2-3 sentence getting started guide]

## Instructions
[Step-by-step guidance for Claude]

## Capabilities
[Bulleted list of what the skill can do]

## Requirements
[List of dependencies, tools, or prerequisites]

## Examples
[Specific usage scenarios]

## Notes
[Additional context, limitations, or considerations]
```

### Writing Effective Instructions

#### Be Specific and Clear

**Good:**
```markdown
## Instructions
1. Run `git diff --staged` to see all staged changes
2. Analyze the changes for logical groupings and affected components
3. Generate a commit message following conventional commits format:
   - Type (feat, fix, docs, etc.)
   - Brief description under 50 characters
   - Optional detailed description explaining what and why
4. Review the message for clarity and accuracy
```

**Poor:**
```markdown
## Instructions
Look at the git changes and write a commit message.
```

#### Include Error Handling

```markdown
## Instructions
1. Check if there are any staged changes using `git status`
2. If no changes are staged, prompt user to stage files first
3. Run `git diff --staged` to examine changes
4. If diff is empty or unparseable, ask user to check their git repository
5. Generate commit message and confirm with user before suggesting
```

#### Handle Edge Cases

```markdown
## Instructions
1. Verify the file exists and is readable
2. Check if the file format is supported (.xlsx, .xls, .csv)
3. For CSV files, detect delimiter and encoding automatically
4. Handle missing or empty cells appropriately
5. If file is too large (>100MB), suggest sampling strategies
6. Report any data quality issues found during processing
```

### Documentation Best Practices

#### Progressive Disclosure

Structure information from general to specific:

```markdown
# Excel Analyzer

## Quick Start
I can analyze Excel spreadsheets to extract insights and create reports. Just share your Excel file and tell me what you're looking for.

## Instructions
[Detailed step-by-step process]

For advanced features like custom charts and statistical analysis, see [reference documentation](reference.md).
```

#### Cross-Reference Supporting Files

```markdown
For detailed API information, see [reference.md](reference.md).

For example usage patterns, check [examples.md](examples.md).

To run the analysis script:
```bash
python scripts/analyze.py input.xlsx
```
```

#### Use Code Blocks Effectively

```markdown
## Requirements
Install required Python packages:

```bash
pip install pandas matplotlib openpyxl seaborn
```

## Example Usage
```python
import pandas as pd

# Load and analyze data
df = pd.read_excel('data.xlsx')
print(df.describe())
```
```

## Advanced Features

### Tool Permissions

#### Restrictive Permissions
For skills that should only read files:

```yaml
---
name: safe-file-reader
description: Read and analyze files without making changes. Use when you need to examine files or extract information without modification risk.
allowed-tools: Read, Grep, Glob
---
```

#### Permissive Permissions
For skills that need full system access:

```yaml
---
name: system-optimizer
description: Optimize system performance and configuration. Use when tuning system settings, managing resources, or performance troubleshooting.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---
```

### Script Integration

#### Creating Helper Scripts

Create `scripts/helper.py`:

```python
#!/usr/bin/env python3
"""
Helper script for Excel analysis
"""
import pandas as pd
import sys
import json

def analyze_excel(file_path):
    """Analyze Excel file and return insights"""
    try:
        df = pd.read_excel(file_path)

        insights = {
            "rows": len(df),
            "columns": len(df.columns),
            "data_types": df.dtypes.to_dict(),
            "summary": df.describe().to_dict(),
            "missing_values": df.isnull().sum().to_dict()
        }

        return insights
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(json.dumps({"error": "Usage: python helper.py <excel_file>"}))
        sys.exit(1)

    result = analyze_excel(sys.argv[1])
    print(json.dumps(result, indent=2))
```

Make executable:
```bash
chmod +x scripts/helper.py
```

#### Using Scripts in SKILL.md

```markdown
## Instructions
1. Get the Excel file path from the user
2. Run the analysis script:
   ```bash
   python ${CLAUDE_PLUGIN_ROOT}/scripts/helper.py "file.xlsx"
   ```
3. Parse the JSON output for insights
4. Present findings in a clear, actionable format

${CLAUDE_PLUGIN_ROOT} is an environment variable that points to this skill's installation directory.
```

### Template Usage

#### Creating Templates

Create `templates/report.md`:

```markdown
# {{title}}

## Executive Summary
{{summary}}

## Key Findings
{{findings}}

## Recommendations
{{recommendations}}

## Data Overview
- Total records: {{total_records}}
- Analysis date: {{date}}
- Data quality score: {{quality_score}}%
```

#### Using Templates in Instructions

```markdown
## Instructions
1. Complete the data analysis
2. Generate a report using the template:
   ```bash
   # Replace template variables
   sed -e "s/{{title}}/Analysis Report/g" \
       -e "s/{{summary}}/${SUMMARY}/g" \
       -e "s/{{findings}}/${FINDINGS}/g" \
       ${CLAUDE_PLUGIN_ROOT}/templates/report.md > report.md
   ```
3. Review and customize the generated report
```

### Environment Variables

Claude provides several environment variables for skills:

- `${CLAUDE_PLUGIN_ROOT}`: Path to skill installation directory
- `${PWD}`: Current working directory
- `${USER}`: Current username
- `${HOME}`: User's home directory

```markdown
## Instructions
1. Access configuration files:
   ```bash
   config_file="${CLAUDE_PLUGIN_ROOT}/config/default.json"
   ```
2. Use relative paths for portability:
   ```bash
   data_dir="${CLAUDE_PLUGIN_ROOT}/data"
   ```
3. Respect user preferences:
   ```bash
   output_dir="${PWD}/output"
   ```
```

## Testing Strategies

### Manual Testing

#### Discovery Testing

Test that Claude can find your skill:

```bash
# Test keyword matching
Claude, can you help me with Excel analysis?

# Test description matching
Claude, I need to analyze some spreadsheet data for business insights.

# Test edge cases
Claude, what skills do you have available?
```

#### Functional Testing

Test the skill's core functionality:

```bash
# Test with sample data
Can you analyze this Excel file and tell me what insights you find?

# Test error handling
Can you analyze this corrupted Excel file?

# Test edge cases
Can you analyze an empty Excel file?
```

### Automated Testing

#### Test Case Structure

Create `tests/test_cases.md`:

```markdown
# Test Cases for Excel Analyzer

## Test Case 1: Basic Analysis
**Input**: Standard Excel file with sales data
**Expected**: Summary statistics, trends, recommendations
**Command**: Test with sample sales data

## Test Case 2: Empty File
**Input**: Empty Excel file
**Expected**: Graceful error message, guidance
**Command**: Test with empty.xlsx

## Test Case 3: Large File
**Input**: Large Excel file (>50MB)
**Expected**: Performance warning, sampling approach
**Command**: Test with large_dataset.xlsx
```

#### Validation Script

Create `tests/validate.py`:

```python
#!/usr/bin/env python3
"""
Validation script for Excel Analyzer skill
"""
import os
import json
import sys
from pathlib import Path

def validate_skill_structure():
    """Validate that required files exist"""
    required_files = [
        'SKILL.md',
        'scripts/helper.py',
        'templates/report.md'
    ]

    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)

    if missing_files:
        return {"valid": False, "missing": missing_files}

    return {"valid": True}

def validate_skill_markdown():
    """Validate SKILL.md structure and content"""
    try:
        with open('SKILL.md', 'r') as f:
            content = f.read()

        # Check for required frontmatter
        if 'name:' not in content:
            return {"valid": False, "error": "Missing name in frontmatter"}

        if 'description:' not in content:
            return {"valid": False, "error": "Missing description in frontmatter"}

        # Check for required sections
        required_sections = ['## Instructions', '## Examples']
        for section in required_sections:
            if section not in content:
                return {"valid": False, "error": f"Missing {section}"}

        return {"valid": True}

    except Exception as e:
        return {"valid": False, "error": str(e)}

def main():
    """Run all validations"""
    print("Validating skill structure...")
    structure = validate_skill_structure()

    print("Validating skill content...")
    content = validate_skill_markdown()

    results = {
        "structure": structure,
        "content": content
    }

    print(json.dumps(results, indent=2))

    if structure["valid"] and content["valid"]:
        print("✅ Skill validation passed!")
        sys.exit(0)
    else:
        print("❌ Skill validation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### Integration Testing

#### Plugin Testing

Test skill discovery from a local plugin:

```bash
# Install plugin from local path
/plugin install ./skills-kit

# Verify the new Skill appears
What Skills are available?

# Exercise the skill
Can you help me analyze some Excel data?
```

#### Environment Testing

Test skill in different environments:

```bash
# Test with Claude Code
claude "Can you analyze this Excel file?"

# Test with different Python versions
python3.8 scripts/helper.py test.xlsx
python3.9 scripts/helper.py test.xlsx
python3.10 scripts/helper.py test.xlsx

# Test with missing dependencies
pip uninstall pandas -y
python scripts/helper.py test.xlsx  # Should handle gracefully
```

## Distribution Methods

### Personal Skills

#### Installation
Skills placed in `~/.claude/skills/` are automatically available:

```bash
mkdir -p ~/.claude/skills/my-skill
# Create skill files
# Skill is immediately available
```

#### Sharing
Share personal skills via:

```bash
# Export skill
tar -czf my-skill.tar.gz -C ~/.claude/skills my-skill

# Others can import
mkdir -p ~/.claude/skills
tar -xzf my-skill.tar.gz -C ~/.claude/skills
```

### Project Skills

#### Team Distribution
Skills in `.claude/skills/` are shared via git:

```bash
# Add to project
mkdir -p .claude/skills/my-skill
git add .claude/skills/
git commit -m "Add my-skill for team workflow"
git push

# Team members get automatically
git pull
# Skill is now available
```

#### Configuration
Configure required skills in `.claude/settings.json`:

```json
{
  "enabledPlugins": [
    "my-skill"
  ]
}
```

### Plugin Distribution

#### Plugin Structure
```
my-plugin/
├── plugin.json
├── skills/
│   ├── skill-1/
│   └── skill-2/
└── commands/
```

#### plugin.json
```json
{
  "name": "my-excel-tools",
  "description": "Excel analysis and reporting tools",
  "version": "1.0.0",
  "author": "Your Name",
  "skills": [
    "excel-analyzer",
    "report-generator"
  ]
}
```

#### Marketplace Distribution
Add to marketplace configuration:

```json
{
  "plugins": [
    {
      "name": "excel-analyzer",
      "source": {
        "source": "github",
        "repo": "your-org/excel-plugin"
      },
      "description": "Analyze Excel spreadsheets and generate insights"
    }
  ]
}
```

## Best Practices

### Skill Design

#### 1. Focus on Specific Problems

**Good Examples:**
- "Generate conventional commit messages from Git diffs"
- "Analyze API responses for performance issues"
- "Convert Markdown documentation to HTML"

**Avoid:**
- "Help with Git" (too broad)
- "Fix performance problems" (too vague)

#### 2. Write Descriptive Descriptions

Include both capabilities and triggers:

```yaml
description: Analyze API responses, identify performance bottlenecks, and suggest optimizations. Use when working with HTTP responses, REST APIs, or troubleshooting API performance issues.
```

#### 3. Handle Errors Gracefully

```markdown
## Instructions
1. Check if input file exists and is readable
2. Validate file format and structure
3. If validation fails, provide clear error message and guidance
4. Process data with appropriate error handling
5. Report any issues found during processing
```

### Documentation Quality

#### 1. Provide Clear Examples

```markdown
## Examples

**Basic Analysis**:
"Can you analyze this sales spreadsheet and tell me which products performed best?"

**Custom Report**:
"I need to analyze customer feedback data and create a quarterly report summary."

**Data Quality Check**:
"Please check this Excel file for any data quality issues and missing values."
```

#### 2. Document Dependencies

```markdown
## Requirements
- Python 3.8+
- pandas 1.3.0+ for data processing
- matplotlib 3.5.0+ for visualization
- openpyxl 3.0.0+ for Excel file handling

Install with:
```bash
pip install pandas matplotlib openpyxl
```
```

#### 3. Include Limitations

```markdown
## Notes
- Maximum file size: 100MB (larger files require sampling)
- Supported formats: .xlsx, .xls, .csv
- Memory usage: Approximately 10x file size during processing
- Processing time: 1-5 seconds per 10,000 rows
```

### Performance Considerations

#### 1. Optimize for Large Files

```markdown
## Instructions
1. Check file size before processing
2. If >50MB, suggest sampling approach:
   ```bash
   python ${CLAUDE_PLUGIN_ROOT}/scripts/sample.py file.xlsx 10000
   ```
3. Process sample and inform user about sampling approach
4. Offer full analysis option with time estimate
```

#### 2. Cache Expensive Operations

```markdown
## Instructions
1. Check if analysis results already exist:
   ```bash
   if [ -f "analysis_cache.json" ]; then
       echo "Using cached analysis results"
       cat analysis_cache.json
   else
       # Perform analysis
       python scripts/analyze.py file.xlsx > analysis_cache.json
   fi
   ```
```

#### 3. Use Progressive Disclosure

```markdown
## Instructions
1. Provide initial overview immediately
2. Offer detailed analysis as optional step
3. Present visualizations for large datasets
4. Generate custom reports on request

For advanced features like custom filters and statistical tests, see [reference documentation](reference.md).
```

### Security Considerations

#### 1. Validate Inputs

```markdown
## Instructions
1. Sanitize file paths to prevent directory traversal
2. Validate file extensions and content types
3. Check file sizes to prevent resource exhaustion
4. Scan uploaded files for malicious content
```

#### 2. Restrict Tool Access

```yaml
---
name: secure-analyzer
description: Analyze files safely without system modifications. Use for secure file analysis and content inspection.
allowed-tools: Read, Grep
---
```

#### 3. Handle Sensitive Data

```markdown
## Security Notes
- Never log or cache sensitive personal information
- Clear temporary files immediately after use
- Use secure random naming for temp files
- Inform user about data retention policies
```

### Maintainability

#### 1. Version Control

```markdown
# Version History
- v2.0.0 (2024-01-15): Added support for CSV files
- v1.1.0 (2024-01-01): Enhanced visualization capabilities
- v1.0.0 (2023-12-15): Initial release
```

#### 2. Modular Design

Split complex functionality into separate scripts:

```markdown
## Instructions
1. Use data loader for file processing:
   ```bash
   python ${CLAUDE_PLUGIN_ROOT}/scripts/load_data.py file.xlsx
   ```

2. Use analyzer for insights:
   ```bash
   python ${CLAUDE_PLUGIN_ROOT}/scripts/analyze.py data.json
   ```

3. Use reporter for output formatting:
   ```bash
   python ${CLAUDE_PLUGIN_ROOT}/scripts/report.py insights.json
   ```
```

#### 3. Configuration Management

```markdown
## Configuration
Default settings are in `${CLAUDE_PLUGIN_ROOT}/config/default.json`:

```json
{
  "max_file_size": 104857600,
  "sample_size": 10000,
  "output_format": "markdown"
}
```

Override with environment variables or config files.
```

## Common Pitfalls

### Discovery Issues

#### 1. Vague Descriptions

**Problem**: Claude doesn't know when to use your skill

**Solution**: Be specific about triggers and capabilities:

```yaml
# Poor
description: Helps with documents

# Good
description: Extract text from PDF files, fill forms, and merge documents. Use when working with PDF files, form filling, or document processing.
```

#### 2. Missing Keywords

**Problem**: Users mention terms not in your description

**Solution**: Include relevant synonyms and alternate terms:

```yaml
description: Analyze Excel spreadsheets, process CSV files, and work with tabular data. Use when analyzing spreadsheets, .xlsx files, business data, financial reports, or data processing workflows.
```

### Functional Issues

#### 1. Missing Error Handling

**Problem**: Skill fails unexpectedly

**Solution**: Include comprehensive error handling:

```markdown
## Instructions
1. Validate input parameters and file existence
2. Check dependencies and system requirements
3. Handle network timeouts and API failures
4. Provide clear error messages with actionable guidance
5. Suggest alternative approaches when primary method fails
```

#### 2. Unclear Instructions

**Problem**: Claude doesn't understand what to do

**Solution**: Provide specific, step-by-step guidance:

```markdown
## Instructions
1. Run `git status` to check current repository state
2. If no changes are staged, run `git add .` to stage all changes
3. Execute `git diff --staged` to see staged changes
4. Analyze changes and identify logical groupings
5. Generate commit message following conventional commits format
6. Present the commit message to user for confirmation
```

### Performance Issues

#### 1. Inefficient Processing

**Problem**: Skill is slow or resource-intensive

**Solution**: Optimize for performance:

```markdown
## Performance Notes
- Use streaming for large files instead of loading entire file
- Cache expensive computations and reuse results
- Parallelize independent operations when possible
- Provide progress feedback for long-running operations
- Offer sampling options for very large datasets
```

#### 2. Memory Leaks

**Problem**: Skill consumes excessive memory

**Solution**: Manage resources properly:

```markdown
## Resource Management
1. Clean up temporary files immediately after use
2. Close file handles and database connections
3. Use generators for processing large datasets
4. Monitor memory usage and warn user about resource limits
5. Implement graceful degradation when resources are constrained
```

## Troubleshooting

### Debugging Skills

#### 1. Enable Debug Mode

```bash
# Run Claude Code with debug output
claude --debug

# Test skill and examine debug output
Can you analyze this Excel file for me?
```

#### 2. Validate Skill Structure

```bash
# Check required files exist
ls -la SKILL.md scripts/ templates/

# Validate JSON syntax if using config files
cat config/settings.json | jq .

# Test script execution
python scripts/helper.py --test
```

#### 3. Test Manual Invocation

```bash
# Test skill discovery
claude "What skills do you have available?"

# Test skill activation
claude "I need to analyze an Excel spreadsheet"

# Test error handling
claude "Can you analyze this non-existent file?"
```

### Common Issues

#### Skill Not Found

**Symptoms**: Claude doesn't recognize your skill exists

**Solutions**:
1. **Check Location**: Verify skill is in correct directory
2. **Validate Frontmatter**: Check YAML syntax and required fields
3. **Restart Claude**: Reload skill definitions by restarting Claude Code
4. **Check Permissions**: Ensure skill files are readable

```bash
# Verify skill location
ls ~/.claude/skills/  # Personal
ls .claude/skills/     # Project

# Validate frontmatter
cat SKILL.md | head -n 10

# Check syntax
python -c "import yaml; yaml.safe_load(open('SKILL.md'))"
```

#### Description Not Matching

**Symptoms**: Skill exists but Claude doesn't use it

**Solutions**:
1. **Improve Description**: Make it more specific and include trigger terms
2. **Add Examples**: Include concrete usage scenarios
3. **Test Keywords**: Try different phrasing in your requests
4. **Check Competition**: Ensure description is distinct from other skills

#### Script Execution Failures

**Symptoms**: Skill activates but script execution fails

**Solutions**:
1. **Check Permissions**: Ensure scripts are executable (`chmod +x`)
2. **Validate Dependencies**: Verify required packages are installed
3. **Test Manually**: Run scripts independently to isolate issues
4. **Check Paths**: Use absolute paths or `${CLAUDE_PLUGIN_ROOT}` variable

```bash
# Test script permissions
ls -la scripts/helper.py
chmod +x scripts/helper.py

# Test script execution
python scripts/helper.py test.xlsx

# Test with environment variable
CLAUDE_PLUGIN_ROOT=$(pwd) python scripts/helper.py test.xlsx
```

## Advanced Topics

### Conditional Logic

#### Environment-Based Behavior

```markdown
## Instructions
1. Detect current environment:
   ```bash
   if command -v conda >/dev/null 2>&1; then
       echo "Using conda environment"
   else
       echo "Using system Python"
   fi
   ```

2. Adapt processing based on available resources
3. Provide environment-specific recommendations
```

#### Feature Flags

```markdown
## Instructions
1. Check for experimental features:
   ```bash
   if [ "${ENABLE_EXPERIMENTAL}" = "true" ]; then
       python ${CLAUDE_PLUGIN_ROOT}/scripts/advanced_analysis.py
   else
       python ${CLAUDE_PLUGIN_ROOT}/scripts/basic_analysis.py
   fi
   ```

2. Provide user choice when multiple approaches available
3. Document feature differences clearly
```

### Integration Patterns

#### Multi-Skill Workflows

Design skills that work together:

```markdown
## Instructions
1. Complete initial analysis and generate insights
2. If report generation needed, delegate to report-generator skill
3. For visualization requests, use chart-creator skill
4. Coordinate with data-validator skill for quality checks
```

#### External API Integration

```markdown
## Instructions
1. Connect to external API with proper authentication:
   ```bash
   curl -H "Authorization: Bearer ${API_KEY}" \
        -H "Content-Type: application/json" \
        -d @data.json \
        https://api.example.com/analyze
   ```

2. Handle API rate limits and errors gracefully
3. Cache API responses when appropriate
4. Respect API terms of service and data privacy
```

### Custom Tool Development

#### Creating Reusable Tools

Develop tools that can be shared across skills:

```python
# tools/excel_processor.py
class ExcelProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def load_data(self):
        """Load Excel data with error handling"""
        try:
            self.data = pd.read_excel(self.file_path)
            return True
        except Exception as e:
            print(f"Error loading file: {e}")
            return False

    def get_summary(self):
        """Generate data summary"""
        if self.data is None:
            return None

        return {
            "shape": self.data.shape,
            "columns": list(self.data.columns),
            "dtypes": self.data.dtypes.to_dict(),
            "describe": self.data.describe().to_dict()
        }
```

#### Tool Documentation

```markdown
## ExcelProcessor Tool

### Description
A robust tool for reading and analyzing Excel files with comprehensive error handling.

### Usage
```python
from tools.excel_processor import ExcelProcessor

processor = ExcelProcessor('file.xlsx')
if processor.load_data():
    summary = processor.get_summary()
    print(summary)
```

### Features
- Automatic format detection
- Memory-efficient loading
- Error handling and recovery
- Progress reporting for large files
```

## Future Developments

### Enhanced Skill Features

- **Skill Composition**: Chain multiple skills for complex workflows
- **Dynamic Loading**: Load skills on-demand based on context
- **Parameter Passing**: Share data between skills efficiently
- **Caching**: Intelligent caching of skill outputs and results

### Development Tools

- **Skill Generator**: Automated skill creation from templates
- **Testing Framework**: Comprehensive skill testing and validation
- **Performance Profiler**: Analyze skill performance and optimization
- **Documentation Generator**: Auto-generate skill documentation

### Distribution Improvements

- **Skill Registry**: Centralized registry for skill discovery
- **Version Management**: Semantic versioning and compatibility checking
- **Dependency Resolution**: Automatic dependency management
- **Update Notifications**: Automatic updates and security patches

---

**Next Steps**:
- [Create your first skill](#creating-your-first-skill)
- [Learn about testing strategies](#testing-strategies)
- [Explore marketplace distribution](marketplace-management.md)
- [Check out the API reference](api-reference.md)
