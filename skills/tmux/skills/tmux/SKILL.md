---
name: cli-tmux
description: Use tmux to run and test our interactive CLI/TUI end-to-end. Includes how to start, send keys, capture output, and cleanly stop (double Ctrl+C).
---

# cli-tmux skill: run & test the CLI using tmux

## Use this skill when
- The user asks to test the CLI end-to-end and it is interactive (TUI prompts, key navigation).
- A command needs a real TTY or long-running process (dev server) that should keep running while we do other tasks.

## Golden rules
1. **Prefer `scripts/tmuxctl.sh` over raw tmux commands** for repeatability.
2. Use an **isolated tmux server socket** so we don't interfere with the user's real tmux sessions.
3. Use a predictable session name: `agent-cli`.
4. Always capture pane output after each interaction and summarize it before proceeding.
5. Always clean up: stop the TUI and kill the session at the end (unless the user wants it left running).

## tmuxctl.sh wrapper (preferred)
Prefer `scripts/tmuxctl.sh` over raw tmux commands for repeatability:
- `scripts/tmuxctl.sh start` - Create new tmux session
- `scripts/tmuxctl.sh run ./bin/ourcli` - Run command in the session
- `scripts/tmuxctl.sh keys Down Down C-m` - Send keystrokes
- `scripts/tmuxctl.sh capture` - Capture pane output
- `scripts/tmuxctl.sh stop` - Stop the TUI (double Ctrl+C)
- `scripts/tmuxctl.sh kill` - Kill the session

## Our CLI/TUI specifics
- To exit the TUI, send **double Ctrl+C**: `C-c` then `C-c`.
- If double Ctrl+C doesn't exit, fallback to killing the tmux pane/session.

## Standard tmux setup (isolated socket)
- Socket path: `.tmp/tmux-agent.sock`
- Session: `agent-cli`
- Pane target: `agent-cli:0.0`

### Create session (if missing)
- Ensure `.tmp/` exists.
- Start detached session in repo root:
  - `tmux -S .tmp/tmux-agent.sock new-session -d -s agent-cli -c "$PWD"`

### Start the CLI
- Send the run command (replace with our real command):
  - Example: `./bin/ourcli` OR `pnpm ourcli` OR `go run ./cmd/ourcli`
- Use:
  - `tmux -S .tmp/tmux-agent.sock send-keys -t agent-cli:0.0 "<COMMAND HERE>" C-m`

### Interact
- Send keys as needed:
  - Enter: `C-m`
  - Up/Down: `Up` / `Down`
  - Quit: `C-c C-c` (double)

### Capture output (after each step)
- `tmux -S .tmp/tmux-agent.sock capture-pane -t agent-cli:0.0 -p`

## End-to-end CLI test recipe
1. Start session (or reuse if running).
2. Launch CLI command.
3. Capture initial screen and confirm expected prompt/state.
4. Perform the requested flows (send keys + capture after each step).
5. Exit TUI with `C-c C-c`, capture output to confirm exit.
6. Kill session (unless user asked to keep it).

## Cleanup
- Preferred:
  - Send `C-c C-c`, then `tmux ... kill-session -t agent-cli`
- If tmux is wedged:
  - `tmux -S .tmp/tmux-agent.sock kill-server`

