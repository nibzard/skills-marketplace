---
name: documentation-helper
description: Generate, update, and maintain technical documentation including README files, API docs, and code comments. Use when creating project documentation, API references, or maintaining code documentation.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Documentation Helper

## Instructions
1. **Analyze Project Structure**: Examine the codebase to understand the project architecture, technologies used, and key components
2. **Identify Documentation Needs**: Determine what type of documentation is needed (README, API docs, guides, etc.)
3. **Review Existing Documentation**: Check for existing documentation files and assess their completeness and accuracy
4. **Extract Key Information**:
   - Identify main project purpose and features
   - Locate configuration files and dependencies
   - Find API endpoints, functions, or classes that need documentation
   - Identify setup and installation requirements
5. **Generate Appropriate Documentation**:
   - Create comprehensive README files for project overview
   - Generate API documentation from code analysis
   - Write getting started guides and tutorials
   - Update code comments and docstrings
6. **Structure Content Organizontally**:
   - Use clear headings and logical sections
   - Include code examples and usage instructions
   - Add tables of contents for navigation
   - Provide links between related documentation
7. **Validate Documentation**: Ensure accuracy, completeness, and clarity of all generated content

## Capabilities
- Generate comprehensive README files from project analysis
- Create API documentation from code inspection
- Write technical guides and tutorials
- Update and maintain existing documentation
- Generate code comments and docstrings
- Create changelogs and release notes
- Develop architecture documentation
- Write troubleshooting guides

## Documentation Types

### Project Documentation
- **README.md**: Project overview, installation, usage
- **CONTRIBUTING.md**: Contribution guidelines and standards
- **LICENSE**: Legal terms and conditions
- **CHANGELOG.md**: Version history and release notes
- **SECURITY.md**: Security policies and reporting procedures

### API Documentation
- **API Reference**: Complete endpoint/function documentation
- **Authentication**: Auth methods and security considerations
- **Error Handling**: Error codes and response formats
- **Rate Limiting**: Usage limits and throttling information
- **SDK/Client Libraries**: Integration examples and libraries

### Technical Guides
- **Getting Started**: Initial setup and first steps
- **Architecture Overview**: System design and component interaction
- **Configuration**: Setup and customization options
- **Deployment**: Production deployment instructions
- **Troubleshooting**: Common issues and solutions

### Code Documentation
- **Comments**: Inline code explanations
- **Docstrings**: Function and class documentation
- **Type Hints**: Parameter and return type specifications
- **Examples**: Usage examples in code
- **Architecture Decisions**: Design rationale and trade-offs

## Documentation Standards

### Markdown Formatting
- Use ATX-style headings (# ## ###)
- Include table of contents for long documents
- Use code blocks with language specification
- Include proper link formatting
- Add appropriate emoji for visual clarity

### Code Examples
- Provide complete, working examples
- Include installation/setup instructions
- Show expected outputs
- Handle error cases appropriately
- Use realistic, practical scenarios

### Structure Guidelines
- Start with brief introduction/overview
- Follow with prerequisites and setup
- Include detailed usage instructions
- End with troubleshooting and support info
- Provide links to additional resources

## Template Structures

### README Template
```markdown
# Project Name

[One-sentence description of the project]

## Overview
[Brief description of what the project does and its main features]

## Installation
[Step-by-step installation instructions]

## Usage
[Basic usage examples with code blocks]

## Configuration
[Configuration options and environment variables]

## API Documentation
[Link to detailed API docs or brief overview]

## Contributing
[Link to contributing guidelines]

## License
[License information]

## Support
[How to get help or report issues]
```

### API Documentation Template
```markdown
# API Documentation

## Overview
[API purpose and capabilities]

## Authentication
[Authentication methods and requirements]

## Base URL
```
https://api.example.com/v1
```

## Endpoints

### GET /resource
[Description of endpoint]

**Parameters:**
- `param1` (string, required): Parameter description
- `param2` (number, optional): Parameter description

**Response:**
```json
{
  "id": "string",
  "name": "string",
  "created_at": "datetime"
}
```

**Example:**
```bash
curl -X GET "https://api.example.com/v1/resource?param1=value"
```

## Error Handling
[Error codes and response formats]

## Rate Limiting
[Usage limits and throttling]
```

## Requirements
- Project files and source code access
- Understanding of project domain and context
- Markdown formatting knowledge
- Basic understanding of technical writing principles

## Examples

**README Generation**:
"I just created a new Python package for data processing. Can you help me write a comprehensive README file?"

**API Documentation**:
"Can you analyze my Flask application and generate API documentation for all the endpoints?"

**Code Comments**:
"Please review this Python code and add appropriate docstrings and comments to make it more maintainable."

**Architecture Documentation**:
"I need to create architecture documentation for this microservices system. Can you help document the components and their interactions?"

**Getting Started Guide**:
"Write a getting started guide for developers who want to contribute to this open source project."

**Changelog**:
"Can you generate a changelog for version 2.0 based on the Git commit history?"

**Troubleshooting Guide**:
"Create a troubleshooting guide for common issues users might encounter with this application."

**API Integration Examples**:
"Write code examples showing how to integrate with our REST API using Python and JavaScript."

**Migration Guide**:
"I need to document the migration process from version 1.x to 2.0. Can you create a comprehensive migration guide?"

## Documentation Quality Checklist

### Content Quality
- [ ] Information is accurate and up-to-date
- [ ] Examples are complete and tested
- [ ] Instructions are clear and unambiguous
- [ ] Code examples follow best practices
- [ ] Error handling is documented

### Structure and Organization
- [ ] Logical flow and progression
- [ ] Clear headings and subheadings
- [ ] Table of contents for navigation
- [ ] Cross-references between sections
- [ ] Consistent formatting and style

### Technical Accuracy
- [ ] Command examples work as shown
- [ ] File paths and names are correct
- [ ] Dependencies and versions are accurate
- [ ] API endpoints and parameters are correct
- [ ] Configuration options are documented

### User Experience
- [ ] Easy to find relevant information
- [ ] Examples are realistic and useful
- [ ] Troubleshooting addresses common issues
- [ ] Links to additional resources are helpful
- [ ] Language is clear and concise

## Best Practices

### Writing Style
- Use clear, simple language
- Write in active voice
- Be consistent with terminology
- Use present tense for descriptions
- Include relevant keywords for searchability

### Technical Accuracy
- Verify all code examples work
- Test all command-line instructions
- Check all file paths and references
- Validate API endpoints and parameters
- Ensure version compatibility

### Accessibility
- Use descriptive headings
- Provide alt text for images
- Use sufficient color contrast
- Ensure keyboard navigation
- Write for international audience

## Common Pitfalls to Avoid

### Content Issues
- **Outdated information**: Regularly review and update
- **Missing context**: Provide sufficient background information
- **Unclear instructions**: Test examples with actual users
- **Incomplete coverage**: Document edge cases and errors
- **Inconsistent terminology**: Use style guides

### Technical Issues
- **Broken links**: Verify all internal and external links
- **Incorrect code examples**: Test all code snippets
- **Missing prerequisites**: List all required tools and dependencies
- **Version conflicts**: Document compatibility requirements
- **Security concerns**: Avoid exposing sensitive information

## Integration with Development Workflow

### Pre-commit Documentation
- Check for documentation updates
- Validate code examples
- Ensure all new features are documented
- Update changelog for significant changes

### Documentation Generation
- Automated API documentation from code
- Schema documentation from database models
- Configuration documentation from config files
- Test coverage documentation

### Review Process
- Technical review for accuracy
- User review for clarity and completeness
- Copy editing for style and grammar
- Security review for sensitive information

## Tools and Technologies

### Static Analysis
- Use linting tools for consistency
- Validate markdown formatting
- Check for broken links
- Verify code syntax in examples

### Documentation Generators
- Sphinx for Python projects
- JSDoc for JavaScript
- Swagger/OpenAPI for REST APIs
- Doxygen for C/C++ projects

### Content Management
- Version control for documentation
- Review workflows for updates
- Documentation as code practices
- Automated testing of examples

## Notes
- Documentation should be maintained alongside code changes
- Consider multiple audience types (beginners, experts, operators)
- Include both "how-to" guides and "why" explanations
- Regular review and updates are essential for accuracy
- Provide feedback mechanisms for users to report issues or suggest improvements