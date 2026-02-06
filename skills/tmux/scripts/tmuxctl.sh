#!/usr/bin/env bash
set -euo pipefail

SOCK="${TMUX_AGENT_SOCKET:-.tmp/tmux-agent.sock}"
SESSION="${TMUX_AGENT_SESSION:-agent-cli}"
PANE="${SESSION}:0.0"

mkdir -p .tmp

tmux_cmd() { tmux -S "$SOCK" "$@"; }

ensure_session() {
  if ! tmux_cmd has-session -t "$SESSION" 2>/dev/null; then
    tmux_cmd new-session -d -s "$SESSION" -c "${TMUX_AGENT_CWD:-$PWD}"
  fi
}

case "${1:-}" in
  start)
    ensure_session
    ;;
  run)
    shift
    ensure_session
    CMD="$*"
    tmux_cmd send-keys -t "$PANE" "$CMD" C-m
    ;;
  keys)
    shift
    ensure_session
    tmux_cmd send-keys -t "$PANE" "$@"
    ;;
  capture)
    ensure_session
    tmux_cmd capture-pane -t "$PANE" -p
    ;;
  stop)
    ensure_session
    # double Ctrl+C for TUIs that require it
    tmux_cmd send-keys -t "$PANE" C-c C-c
    ;;
  kill)
    tmux_cmd kill-session -t "$SESSION" 2>/dev/null || true
    ;;
  *)
    echo "Usage: $0 {start|run <cmd...>|keys <keys...>|capture|stop|kill}" >&2
    exit 2
    ;;
esac

