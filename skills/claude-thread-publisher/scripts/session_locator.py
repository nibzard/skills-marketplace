#!/usr/bin/env python3
"""
Session locator for Claude Code thread publisher.

This script helps locate the current Claude Code session file and project information.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime


def find_claude_projects_root():
    """Find the Claude projects root directory."""
    # Check common locations
    candidates = [
        Path.home() / ".claude" / "projects",
        Path.home() / ".config" / "claude" / "projects",
    ]

    for candidate in candidates:
        if candidate.exists() and candidate.is_dir():
            return candidate

    return None


def find_project_for_cwd(cwd=None):
    """Find the Claude project corresponding to the current working directory."""
    if cwd is None:
        cwd = Path.cwd()

    projects_root = find_claude_projects_root()
    if not projects_root:
        return None

    # Try to find a project that matches the current directory
    # Look for directories with similar names or paths
    cwd_str = str(cwd)

    for project_dir in projects_root.iterdir():
        if not project_dir.is_dir():
            continue

        # Check if any metadata file might link this to our cwd
        metadata_file = project_dir / "metadata.json"
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                    if metadata.get("path") == cwd_str:
                        return project_dir
            except (json.JSONDecodeError, IOError):
                continue

    # Fallback: try to find project by matching directory name
    dir_name = cwd.name.lower().replace(" ", "-").replace("_", "-")
    for project_dir in projects_root.iterdir():
        if not project_dir.is_dir():
            continue
        if project_dir.name.lower() == dir_name:
            return project_dir

    return None


def find_latest_session(project_dir):
    """Find the latest session file in the given project directory."""
    if not project_dir or not project_dir.exists():
        return None

    sessions_dir = project_dir / "sessions"
    if not sessions_dir.exists():
        return None

    # Find all .jsonl files in sessions directory
    session_files = list(sessions_dir.glob("*.jsonl"))
    if not session_files:
        return None

    # Return the most recently modified file
    latest = max(session_files, key=lambda f: f.stat().st_mtime)
    return latest


def get_session_info(session_file):
    """Extract basic information from a session file."""
    if not session_file or not session_file.exists():
        return None

    try:
        messages = []
        with open(session_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        msg = json.loads(line)
                        messages.append(msg)
                    except json.JSONDecodeError:
                        continue

        if not messages:
            return None

        # Get first user message as potential title
        title = "Untitled Thread"
        for msg in messages:
            if msg.get("role") == "user":
                content = msg.get("content", "")
                if isinstance(content, str) and content.strip():
                    # Truncate to reasonable length
                    title = content[:100] + ("..." if len(content) > 100 else "")
                    break

        return {
            "title": title,
            "message_count": len(messages),
            "first_message_time": messages[0].get("timestamp") if messages else None,
            "last_message_time": messages[-1].get("timestamp") if messages else None,
        }

    except IOError:
        return None


def main():
    parser = argparse.ArgumentParser(description="Locate Claude Code session files")
    parser.add_argument("--mode", choices=["current", "list", "project"], default="current",
                       help="Mode of operation")
    parser.add_argument("--session-file", type=str, help="Explicit session file path")
    parser.add_argument("--project-dir", type=str, help="Explicit project directory path")
    parser.add_argument("--cwd", type=str, help="Current working directory (default: actual cwd)")

    args = parser.parse_args()

    if args.mode == "current":
        # Find current session
        if args.session_file:
            session_file = Path(args.session_file)
            project_dir = Path(args.project_dir) if args.project_dir else None
            cwd = Path(args.cwd) if args.cwd else Path.cwd()
        else:
            cwd = Path(args.cwd) if args.cwd else Path.cwd()
            project_dir = find_project_for_cwd(cwd)
            session_file = find_latest_session(project_dir) if project_dir else None

        if not session_file:
            result = {
                "error": "No session file found",
                "cwd": str(cwd),
                "project_dir": str(project_dir) if project_dir else None
            }
        else:
            session_info = get_session_info(session_file)
            result = {
                "session_file": str(session_file),
                "project_path": str(cwd),
                "project_dir": str(project_dir) if project_dir else None,
                "session_info": session_info
            }

        print(json.dumps(result, indent=2))

    elif args.mode == "list":
        # List all projects and their sessions
        projects_root = find_claude_projects_root()
        if not projects_root:
            print(json.dumps({"error": "Claude projects directory not found"}, indent=2))
            sys.exit(1)

        projects = []
        for project_dir in projects_root.iterdir():
            if not project_dir.is_dir():
                continue

            sessions = []
            sessions_dir = project_dir / "sessions"
            if sessions_dir.exists():
                for session_file in sessions_dir.glob("*.jsonl"):
                    session_info = get_session_info(session_file)
                    if session_info:
                        sessions.append({
                            "file": str(session_file),
                            "info": session_info
                        })

            projects.append({
                "directory": str(project_dir),
                "sessions": sorted(sessions, key=lambda s: s["info"]["last_message_time"] or "", reverse=True)
            })

        result = {
            "projects_root": str(projects_root),
            "projects": projects
        }

        print(json.dumps(result, indent=2))

    elif args.mode == "project":
        # Find project for a specific directory
        cwd = Path(args.cwd) if args.cwd else Path.cwd()
        project_dir = find_project_for_cwd(cwd)

        if project_dir:
            sessions = []
            sessions_dir = project_dir / "sessions"
            if sessions_dir.exists():
                for session_file in sessions_dir.glob("*.jsonl"):
                    session_info = get_session_info(session_file)
                    if session_info:
                        sessions.append({
                            "file": str(session_file),
                            "info": session_info
                        })

            result = {
                "cwd": str(cwd),
                "project_dir": str(project_dir),
                "sessions": sorted(sessions, key=lambda s: s["info"]["last_message_time"] or "", reverse=True)
            }
        else:
            result = {
                "cwd": str(cwd),
                "project_dir": None,
                "sessions": []
            }

        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()