# tmux Agent Skill

A Claude Code Agent Skill for running and testing interactive CLI/TUI applications using tmux.

## Overview

This skill enables Claude to test interactive command-line interfaces end-to-end by:
- Creating isolated tmux sessions that don't interfere with your real tmux sessions
- Sending keystrokes and commands to TUI applications
- Capturing and analyzing terminal output
- Properly cleaning up sessions after testing

## Use Cases

- Testing interactive CLI prompts and menus
- Running TUI applications that require a real TTY
- Starting long-running processes (dev servers, watchers)
- End-to-end testing of terminal applications

## Quick Start

The skill provides a wrapper script `scripts/tmuxctl.sh` for repeatability:

```bash
# Start a new tmux session
scripts/tmuxctl.sh start

# Run a command in the session
scripts/tmuxctl.sh run ./bin/yourcli

# Send keystrokes
scripts/tmuxctl.sh keys Down Down C-m

# Capture output
scripts/tmuxctl.sh capture

# Stop the TUI (double Ctrl+C)
scripts/tmuxctl.sh stop

# Kill the session
scripts/tmuxctl.sh kill
```

## Installation

This skill is part of the [Skills Marketplace](https://github.com/nibzard/skills-kit).

Install via the marketplace plugin:

```bash
/plugin install nibzard/skills-kit
```

## Skill Behavior

This skill automatically activates when:
- You ask to test an interactive CLI/TUI end-to-end
- A command needs a real TTY or long-running process
- You want to test keyboard navigation and prompts

## Features

- **Isolated Sessions**: Uses a dedicated tmux socket (`.tmp/tmux-agent.sock`) so tests don't interfere with your tmux sessions
- **Repeatable Workflows**: The `tmuxctl.sh` wrapper provides consistent commands for all tmux operations
- **Safe Cleanup**: Ensures sessions are properly killed after testing
- **Output Capture**: Automatically captures pane output after each interaction

## Requirements

- `tmux` installed on the system
- The `scripts/tmuxctl.sh` wrapper script

## License

MIT
