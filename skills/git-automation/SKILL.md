---
name: git-automation
description: Automate Git workflows, generate conventional commit messages, manage branches, and handle repository operations. Use when working with Git repositories, making commits, or managing version control.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Git Automation

## Instructions
1. **Assess Current State**: Run `git status` to understand the current repository state and identify what needs attention
2. **Check for Staged Changes**: If no changes are staged, identify what files need to be added for the current task
3. **Analyze Changes**: Use `git diff` (unstaged) and `git diff --staged` to understand what changes have been made
4. **Generate Commit Message**: Create a conventional commit message following the format:
   - Type: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
   - Scope: Brief indication of what part of codebase is affected
   - Description: Present tense, imperative mood description of what the change does
   - Body (optional): Detailed explanation of what and why
   - Footer (optional): Breaking changes, issues referenced, etc.
5. **Suggest Git Actions**: Recommend appropriate Git commands based on the situation (add files, commit, branch operations, etc.)
6. **Provide Branch Management**: If working with branches, suggest appropriate branching strategies and commands

## Capabilities
- Generate conventional commit messages from Git diffs
- Suggest appropriate Git commands for various scenarios
- Manage branch creation, merging, and cleanup
- Handle repository maintenance and hygiene
- Assist with Git workflow optimization

## Commit Message Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only changes
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring without external behavior changes
- `test`: Adding or updating tests
- `chore`: Maintenance tasks, dependency updates, etc.

**Examples**:
```
feat(auth): add OAuth2 authentication flow

Implement complete OAuth2 authentication with support for:
- Google and GitHub providers
- Token refresh and revocation
- Secure token storage

Closes #123

fix(api): handle null response from user endpoint

Prevents application crash when user service returns null.
Adds proper error handling and fallback behavior.

docs: update API documentation for v2.0

Reflects breaking changes in authentication and user endpoints.
Adds new examples and clarifies deprecation timeline.
```

## Common Git Workflows

### Daily Development
1. Create feature branch from main/develop
2. Make changes and test locally
3. Stage relevant files for commit
4. Write conventional commit message
5. Push branch and create pull request

### Repository Maintenance
- `git fetch --prune`: Clean up stale remote branches
- `git rebase -i HEAD~N`: Interactive rebase to clean up commit history
- `git branch -d branch-name`: Delete merged local branches
- `git remote prune origin`: Remove stale remote-tracking branches

### Troubleshooting Common Issues
- **Uncommitted changes**: `git stash` or commit before switching branches
- **Merge conflicts**: Use `git status` to see conflicts, resolve manually, then add and commit
- **Wrong commit message**: `git commit --amend` (if not pushed) or `git rebase -i` (if pushed)

## Requirements
- Git installed and configured
- Repository initialized with Git
- Proper Git configuration (user.name, user.email)

## Examples

**Basic Commit Assistance**:
"I just finished implementing the user login feature. Can you help me commit these changes?"

**Branch Management**:
"I need to create a new feature branch for the payment system integration"

**Repository Cleanup**:
"Can you help me clean up these old feature branches that have been merged?"

**Git Troubleshooting**:
"I'm having a merge conflict, can you help me resolve it and complete the merge?"

**Commit History Cleanup**:
"I have several messy commits that should be combined into one, can you help me squash them?"

## Notes
- Always check `git status` before and after operations
- Use conventional commits for better project maintainability
- Verify changes before committing to avoid including unintended files
- Consider using Git hooks for automatic formatting or validation
- For complex operations, suggest creating a backup branch first