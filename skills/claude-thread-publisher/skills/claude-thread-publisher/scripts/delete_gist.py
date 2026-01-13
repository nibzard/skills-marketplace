#!/usr/bin/env python3
"""
GitHub Gist deleter for Claude Code thread publisher.

This script deletes GitHub Gists that were created by the thread publisher.
"""

import argparse
import json
import os
import sys
import requests
from datetime import datetime
from pathlib import Path


class GistDeleter:
    def __init__(self, config_path="~/.claude/thread-publisher/config.json", index_path="~/.claude/thread-publisher/index.json"):
        self.config_path = Path(config_path).expanduser()
        self.index_path = Path(index_path).expanduser()
        self.config = self.load_config()
        self.index = self.load_index()

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
        try:
            self.index_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.index_path, 'w') as f:
                json.dump(self.index, f, indent=2)
            return True
        except IOError as e:
            print(f"Error saving index: {e}", file=sys.stderr)
            return False

    def get_github_token(self):
        """Get GitHub token from config."""
        token = self.config.get("github_token")
        if not token:
            print("Error: No GitHub token found in configuration.", file=sys.stderr)
            print("Please run the publisher first to set up your token.", file=sys.stderr)
            return None
        return token

    def delete_gist(self, gist_id):
        """Delete a Gist by ID."""
        token = self.get_github_token()
        if not token:
            return None

        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }

        try:
            response = requests.delete(
                f"https://api.github.com/gists/{gist_id}",
                headers=headers,
                timeout=30
            )

            if response.status_code == 204:
                return {"success": True, "gist_id": gist_id}
            elif response.status_code == 404:
                print(f"Warning: Gist {gist_id} not found (may have been already deleted)", file=sys.stderr)
                return {"success": True, "gist_id": gist_id, "note": "already_deleted"}
            else:
                response.raise_for_status()
                return None

        except requests.RequestException as e:
            print(f"Error deleting Gist: {e}", file=sys.stderr)
            if hasattr(e, 'response') and e.response:
                try:
                    error_data = e.response.json()
                    print(f"GitHub API error: {error_data.get('message', 'Unknown error')}", file=sys.stderr)
                except:
                    pass
            return None

    def delete_thread_by_hash(self, thread_hash, confirm=True):
        """Delete a published thread by its hash."""
        if thread_hash not in self.index["threads"]:
            print(f"Error: No published thread found with hash: {thread_hash[:16]}...", file=sys.stderr)
            return None

        thread_info = self.index["threads"][thread_hash]
        gist_id = thread_info["gist_id"]
        title = thread_info.get("title", "Unknown thread")
        published_at = thread_info.get("last_published_at", "Unknown time")

        if confirm:
            print(f"Preparing to delete published thread:")
            print(f"  Title: {title}")
            print(f"  Thread Hash: {thread_hash[:16]}...")
            print(f"  Gist ID: {gist_id}")
            print(f"  Published: {published_at}")
            print(f"  Gist URL: {thread_info.get('gist_url', 'Unknown')}")
            print(f"  Permalink: https://gistpreview.github.io/?{gist_id}")
            print()

            response = input("Are you sure you want to delete this Gist? (yes/no): ").strip().lower()
            if response not in ["yes", "y"]:
                print("Deletion cancelled.")
                return None

        # Delete the gist
        result = self.delete_gist(gist_id)
        if result and result.get("success"):
            # Remove from index
            del self.index["threads"][thread_hash]
            self.save_index()

            print(f"✅ Successfully deleted Gist: {gist_id}")
            return result
        else:
            print(f"❌ Failed to delete Gist: {gist_id}", file=sys.stderr)
            return None

    def delete_thread_by_current_session(self, session_file=None, project_path=None, confirm=True):
        """Delete a thread based on the current session."""
        # Import here to avoid circular imports
        from render_thread import parse_jsonl_session, compute_thread_hash

        if not session_file:
            # Try to find current session
            from session_locator import find_project_for_cwd, find_latest_session

            cwd = Path.cwd()
            project_dir = find_project_for_cwd(cwd)
            if not project_dir:
                print("Error: Could not find Claude project for current directory", file=sys.stderr)
                return None

            session_file = find_latest_session(project_dir)
            if not session_file:
                print("Error: Could not find current session file", file=sys.stderr)
                return None

        # Parse and compute hash
        messages = parse_jsonl_session(session_file)
        if not messages:
            print("Error: Could not parse session file", file=sys.stderr)
            return None

        thread_hash = compute_thread_hash(messages)
        return self.delete_thread_by_hash(thread_hash, confirm=confirm)

    def list_published_threads(self):
        """List all published threads."""
        return self.index["threads"]

    def cleanup_orphaned_gists(self, dry_run=True):
        """Find and optionally delete gists that are no longer in the index."""
        token = self.get_github_token()
        if not token:
            return None

        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }

        try:
            # Get all gists for the authenticated user
            response = requests.get(
                "https://api.github.com/gists",
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            all_gists = response.json()

            # Find gists that look like they were created by this tool
            candidate_gists = []
            for gist in all_gists:
                description = gist.get("description", "")
                files = gist.get("files", {})

                # Look for indicators this is a thread publisher gist
                if ("Claude Code Thread:" in description or
                    any(filename in ["index.html", "thread.json", "metadata.json"]
                       for filename in files.keys())):
                    candidate_gists.append({
                        "id": gist["id"],
                        "description": description,
                        "created_at": gist["created_at"],
                        "updated_at": gist["updated_at"],
                        "html_url": gist["html_url"],
                        "files": list(files.keys())
                    })

            # Check which ones are in our index
            known_gist_ids = {info["gist_id"] for info in self.index["threads"].values()}
            orphaned_gists = [gist for gist in candidate_gists if gist["id"] not in known_gist_ids]

            print(f"Found {len(candidate_gists)} thread publisher gists")
            print(f"Found {len(orphaned_gists)} orphaned gists (not in index)")

            if orphaned_gists:
                print("\nOrphaned gists:")
                for gist in orphaned_gists:
                    print(f"  {gist['id']}: {gist['description']}")
                    print(f"    Created: {gist['created_at']}")
                    print(f"    Files: {', '.join(gist['files'])}")
                    print(f"    URL: {gist['html_url']}")
                    print()

                if not dry_run:
                    response = input("Delete all orphaned gists? (yes/no): ").strip().lower()
                    if response in ["yes", "y"]:
                        deleted_count = 0
                        for gist in orphaned_gists:
                            if self.delete_gist(gist["id"]):
                                deleted_count += 1
                                print(f"Deleted: {gist['id']}")
                            else:
                                print(f"Failed to delete: {gist['id']}")
                        print(f"\nDeleted {deleted_count} orphaned gists.")
                    else:
                        print("Cleanup cancelled.")
            else:
                print("No orphaned gists found.")

            return orphaned_gists

        except requests.RequestException as e:
            print(f"Error listing gists: {e}", file=sys.stderr)
            return None


def main():
    parser = argparse.ArgumentParser(description="Delete published Claude Code threads from GitHub Gists")
    parser.add_argument("--config", help="Config file path (default: ~/.claude/thread-publisher/config.json)")
    parser.add_argument("--index", help="Index file path (default: ~/.claude/thread-publisher/index.json)")
    parser.add_argument("--thread-hash", help="Delete thread by hash")
    parser.add_argument("--session-file", help="Delete thread by session file")
    parser.add_argument("--project-path", help="Project path for session resolution")
    parser.add_argument("--gist-id", help="Delete specific gist by ID (bypasses index)")
    parser.add_argument("--list", action="store_true", help="List all published threads")
    parser.add_argument("--cleanup", action="store_true", help="Cleanup orphaned gists")
    parser.add_argument("--cleanup-execute", action="store_true", help="Actually delete orphaned gists (not dry run)")
    parser.add_argument("--force", action="store_true", help="Skip confirmation prompts")

    args = parser.parse_args()

    # Initialize deleter
    deleter = GistDeleter(
        config_path=args.config if args.config else "~/.claude/thread-publisher/config.json",
        index_path=args.index if args.index else "~/.claude/thread-publisher/index.json"
    )

    if args.list:
        threads = deleter.list_published_threads()
        if not threads:
            print("No published threads found.")
        else:
            print(f"Found {len(threads)} published threads:")
            for thread_hash, info in threads.items():
                print(f"  {thread_hash[:16]}...")
                print(f"    Title: {info.get('title', 'Unknown')}")
                print(f"    Gist: {info.get('gist_url', 'Unknown')}")
                print(f"    Published: {info.get('last_published_at', 'Unknown')}")
                print()
        return

    if args.cleanup:
        deleter.cleanup_orphaned_gists(dry_run=not args.cleanup_execute)
        return

    if args.gist_id:
        # Direct gist deletion
        if not args.force:
            response = input(f"Delete gist {args.gist_id}? This action cannot be undone. (yes/no): ").strip().lower()
            if response not in ["yes", "y"]:
                print("Deletion cancelled.")
                return

        result = deleter.delete_gist(args.gist_id)
        if result and result.get("success"):
            print(f"✅ Successfully deleted Gist: {args.gist_id}")
        else:
            print(f"❌ Failed to delete Gist: {args.gist_id}", file=sys.stderr)
            sys.exit(1)
        return

    if args.thread_hash:
        result = deleter.delete_thread_by_hash(args.thread_hash, confirm=not args.force)
    elif args.session_file or not args.thread_hash:
        # Delete by current session
        result = deleter.delete_thread_by_current_session(
            session_file=args.session_file,
            project_path=args.project_path,
            confirm=not args.force
        )
    else:
        parser.print_help()
        sys.exit(1)

    if result and result.get("success"):
        print("✅ Thread deletion completed successfully.")
    else:
        print("❌ Thread deletion failed.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()