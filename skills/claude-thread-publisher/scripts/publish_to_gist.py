#!/usr/bin/env python3
"""
GitHub Gist publisher for Claude Code thread publisher.

This script creates and updates GitHub Gists with rendered thread content.
"""

import argparse
import json
import os
import sys
import requests
from datetime import datetime
from pathlib import Path


class GistPublisher:
    def __init__(self, config_path="~/.claude/thread-publisher/config.json", index_path="~/.claude/thread-publisher/index.json"):
        self.config_path = Path(config_path).expanduser()
        self.index_path = Path(index_path).expanduser()
        self.config = self.load_config()
        self.index = self.load_index()

    def ensure_config_dir(self):
        """Ensure configuration directory exists."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.index_path.parent.mkdir(parents=True, exist_ok=True)

    def load_config(self):
        """Load configuration from file."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load config: {e}", file=sys.stderr)

        return {
            "github_token": None,
            "gists_private_by_default": True
        }

    def save_config(self):
        """Save configuration to file."""
        self.ensure_config_dir()
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except IOError as e:
            print(f"Error saving config: {e}", file=sys.stderr)
            return False

    def load_index(self):
        """Load thread-to-gist index from file."""
        if self.index_path.exists():
            try:
                with open(self.index_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load index: {e}", file=sys.stderr)

        return {"threads": {}}

    def save_index(self):
        """Save thread-to-gist index to file."""
        self.ensure_config_dir()
        try:
            with open(self.index_path, 'w') as f:
                json.dump(self.index, f, indent=2)
            return True
        except IOError as e:
            print(f"Error saving index: {e}", file=sys.stderr)
            return False

    def ensure_github_token(self):
        """Ensure we have a GitHub token."""
        if self.config.get("github_token"):
            return self.config["github_token"]

        print("GitHub Personal Access Token (PAT) required for Gist operations.")
        print("Please create a token with 'gist' scope at: https://github.com/settings/tokens")
        print("The token will be stored locally on your machine.")
        print()

        token = input("Enter your GitHub PAT (with gist scope): ").strip()
        if not token:
            print("Error: GitHub token is required", file=sys.stderr)
            return None

        if not token.startswith("ghp_") and not token.startswith("github_pat_"):
            print("Warning: Token doesn't look like a GitHub PAT", file=sys.stderr)

        self.config["github_token"] = token
        if self.save_config():
            print("GitHub token saved locally.")
            return token
        else:
            print("Error: Could not save GitHub token", file=sys.stderr)
            return None

    def create_gist(self, description, files, public=False):
        """Create a new Gist."""
        token = self.ensure_github_token()
        if not token:
            return None

        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }

        payload = {
            "description": description,
            "public": public,
            "files": files
        }

        try:
            response = requests.post(
                "https://api.github.com/gists",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error creating Gist: {e}", file=sys.stderr)
            if hasattr(e, 'response') and e.response:
                try:
                    error_data = e.response.json()
                    print(f"GitHub API error: {error_data.get('message', 'Unknown error')}", file=sys.stderr)
                except:
                    pass
            return None

    def update_gist(self, gist_id, description, files):
        """Update an existing Gist."""
        token = self.ensure_github_token()
        if not token:
            return None

        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }

        payload = {
            "description": description,
            "files": files
        }

        try:
            response = requests.patch(
                f"https://api.github.com/gists/{gist_id}",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error updating Gist: {e}", file=sys.stderr)
            if hasattr(e, 'response') and e.response:
                try:
                    error_data = e.response.json()
                    print(f"GitHub API error: {error_data.get('message', 'Unknown error')}", file=sys.stderr)
                except:
                    pass
            return None

    def publish_thread(self, html_path, json_path, metadata_path, thread_hash, project_path=None, session_file=None, update_existing=True):
        """Publish a thread to GitHub Gist."""
        # Load files
        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()

            with open(json_path, 'r', encoding='utf-8') as f:
                json_content = f.read()

            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
        except IOError as e:
            print(f"Error reading files: {e}", file=sys.stderr)
            return None

        title = metadata.get("title", "Claude Code Thread")
        created_at = metadata.get("created_at", datetime.now().isoformat())

        description = f"Claude Code Thread: {title} ({created_at})"

        files = {
            "index.html": {"content": html_content},
            "thread.json": {"content": json_content},
            "metadata.json": {"content": json.dumps(metadata, indent=2)}
        }

        # Check if we already have a Gist for this thread
        existing_entry = self.index["threads"].get(thread_hash)
        public = not self.config.get("gists_private_by_default", True)

        if existing_entry and update_existing:
            gist_id = existing_entry["gist_id"]
            print(f"Updating existing Gist: {gist_id}")
            result = self.update_gist(gist_id, description, files)
            if result:
                # Update index with new timestamp
                existing_entry["last_published_at"] = datetime.now().isoformat()
                existing_entry["project_path"] = project_path
                existing_entry["session_file"] = session_file
                self.save_index()
                print(f"Updated existing Gist: {gist_id}")
        else:
            print("Creating new Gist...")
            result = self.create_gist(description, files, public=public)
            if result:
                # Add to index
                self.index["threads"][thread_hash] = {
                    "gist_id": result["id"],
                    "gist_url": result["html_url"],
                    "last_published_at": datetime.now().isoformat(),
                    "project_path": project_path,
                    "session_file": session_file,
                    "title": title
                }
                self.save_index()
                print(f"Created new Gist: {result['id']}")

        if not result:
            return None

        return {
            "gist_id": result["id"],
            "gist_url": result["html_url"],
            "permalink": f"https://gistpreview.github.io/?{result['id']}",
            "thread_hash": thread_hash,
            "title": title,
            "action": "updated" if existing_entry and update_existing else "created"
        }

    def list_published_threads(self):
        """List all published threads."""
        return self.index["threads"]

    def get_thread_info(self, thread_hash):
        """Get information about a published thread."""
        return self.index["threads"].get(thread_hash)


def main():
    parser = argparse.ArgumentParser(description="Publish Claude Code thread to GitHub Gist")
    parser.add_argument("--html", required=True, help="HTML file path")
    parser.add_argument("--thread-json", required=True, help="Thread JSON file path")
    parser.add_argument("--metadata", required=True, help="Metadata file path")
    parser.add_argument("--config", help="Config file path (default: ~/.claude/thread-publisher/config.json)")
    parser.add_argument("--index", help="Index file path (default: ~/.claude/thread-publisher/index.json)")
    parser.add_argument("--project-path", help="Project path for metadata")
    parser.add_argument("--session-file", help="Session file path for metadata")
    parser.add_argument("--no-update", action="store_true", help="Don't update existing gist, always create new")
    parser.add_argument("--list", action="store_true", help="List all published threads")
    parser.add_argument("--thread-hash", help="Get info about specific thread hash")

    args = parser.parse_args()

    # Initialize publisher
    publisher = GistPublisher(
        config_path=args.config if args.config else "~/.claude/thread-publisher/config.json",
        index_path=args.index if args.index else "~/.claude/thread-publisher/index.json"
    )

    if args.list:
        threads = publisher.list_published_threads()
        if not threads:
            print("No published threads found.")
        else:
            print(f"Found {len(threads)} published threads:")
            for thread_hash, info in threads.items():
                print(f"  {thread_hash[:16]}...")
                print(f"    Title: {info.get('title', 'Unknown')}")
                print(f"    Gist: {info.get('gist_url', 'Unknown')}")
                print(f"    Published: {info.get('last_published_at', 'Unknown')}")
                print(f"    Permalink: https://gistpreview.github.io/?{info.get('gist_id', 'unknown')}")
                print()
        return

    if args.thread_hash:
        info = publisher.get_thread_info(args.thread_hash)
        if info:
            print(json.dumps(info, indent=2))
        else:
            print("Thread not found in published threads.", file=sys.stderr)
            sys.exit(1)
        return

    # Load metadata to get thread hash
    try:
        with open(args.metadata, 'r') as f:
            metadata = json.load(f)
        thread_hash = metadata["thread_hash"]
    except (IOError, json.JSONDecodeError, KeyError) as e:
        print(f"Error reading metadata: {e}", file=sys.stderr)
        sys.exit(1)

    # Publish thread
    result = publisher.publish_thread(
        html_path=args.html,
        json_path=args.thread_json,
        metadata_path=args.metadata,
        thread_hash=thread_hash,
        project_path=args.project_path,
        session_file=args.session_file,
        update_existing=not args.no_update
    )

    if result:
        print(json.dumps(result, indent=2))
        print()
        print(f"✅ Thread published successfully!")
        print(f"🔗 Permalink: {result['permalink']}")
        print(f"📄 Gist URL: {result['gist_url']}")
        print(f"🆔 Gist ID: {result['gist_id']}")
        print(f"🔐 Thread Hash: {result['thread_hash']}")
    else:
        print("❌ Failed to publish thread", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()