# Claude Thread Publisher

A comprehensive skill for publishing Claude Code conversation threads as beautiful static HTML pages hosted on GitHub Gists, with shareable permalinks via gistpreview.github.io.

## Quick Start

### Installation
```bash
/plugin marketplace add nibzard/skills-marketplace
/plugin install claude-thread-publisher@skills-marketplace
```

### Basic Usage
> "Publish this Claude Code session as a shareable link."

### Setup
You'll need a GitHub Personal Access Token (PAT) with `gist` scope. The skill will guide you through creating one on first use.

## Features

- **Zero-friction publishing**: Just ask Claude to share the conversation
- **Beautiful static HTML**: Dark theme, syntax highlighting, responsive design
- **GitHub Gists integration**: Private by default, with automatic versioning
- **Shareable permalinks**: Clean URLs via gistpreview.github.io
- **Thread management**: Update, delete, and list published threads
- **Privacy-focused**: Local token storage, private gists by default

## Example Output

When you publish a thread, you'll get:

```
✅ Thread published successfully!
🔗 Permalink: https://gistpreview.github.io/?abcdef1234567890
📄 Gist URL: https://gist.github.com/abcdef1234567890
🆔 Gist ID: abcdef1234567890
🔐 Thread Hash: a1b2c3d4e5f67890abcdef1234567890
```

## File Structure

```
claude-thread-publisher/
├── SKILL.md                    # Complete skill documentation
├── examples.md                 # Example prompts and use cases
├── README.md                   # This file
└── scripts/
    ├── session_locator.py      # Find current Claude Code session
    ├── render_thread.py        # Convert JSONL to HTML/JSON
    ├── publish_to_gist.py      # Create/update GitHub Gists
    └── delete_gist.py          # Delete Gists and manage cleanup
```

## Configuration

- **Config**: `~/.claude/thread-publisher/config.json`
- **Index**: `~/.claude/thread-publisher/index.json`
- **Authentication**: GitHub PAT with `gist` scope (stored locally)

## Common Commands

### Publishing
> "Publish this conversation as a shareable link."
> "Create a permalink for this thread."
> "Update the published link with new messages."

### Management
> "Delete the public link for this thread."
> "Show me all my published threads."
> "Is this conversation already published?"

## Security & Privacy

- ✅ Local token storage only
- ✅ Private gists by default
- ✅ Minimal GitHub permissions (`gist` scope only)
- ✅ No external servers or databases
- ✅ Content-based verification for deletions

## Integration

This skill integrates seamlessly with:

- **Claude Code**: Automatically detects current sessions
- **GitHub Gists**: Uses official GitHub API
- **gistpreview.github.io**: Static HTML hosting service
- **Skills Marketplace**: Centralized discovery and installation

## Requirements

- Python 3.7+
- GitHub account
- GitHub Personal Access Token with `gist` scope
- Claude Code session data in `~/.claude/` directory

## Troubleshooting

### "No session file found"
- Make sure you're in a Claude Code project directory
- Check that `~/.claude/projects/` exists and contains your project

### "GitHub token required"
- Visit https://github.com/settings/tokens
- Create a new token with `gist` scope
- The skill will guide you through this process

### "Gist creation failed"
- Check GitHub API status
- Verify your token has `gist` scope
- Ensure you have internet connectivity

## Examples

See `examples.md` for comprehensive prompt examples covering:

- Basic publishing workflows
- Thread management operations
- Troubleshooting scenarios
- Advanced usage patterns

## License

MIT License - see Skills Marketplace for details.