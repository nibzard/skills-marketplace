#!/usr/bin/env python3
"""
Thread renderer for Claude Code thread publisher.

This script converts Claude Code JSONL sessions into normalized JSON and beautiful HTML.
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path
import html
import re


def parse_jsonl_session(session_file):
    """Parse a Claude Code JSONL session file into normalized format."""
    messages = []

    try:
        with open(session_file, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue

                try:
                    msg = json.loads(line)
                    normalized = normalize_message(msg, line_num)
                    if normalized:
                        messages.append(normalized)
                except json.JSONDecodeError as e:
                    # Skip malformed lines but continue processing
                    print(f"Warning: Skipping malformed JSON at line {line_num}: {e}", file=sys.stderr)
                    continue
    except IOError as e:
        print(f"Error reading session file: {e}", file=sys.stderr)
        return None

    return messages


def normalize_message(msg, line_num=None):
    """Normalize a Claude Code message to our internal format."""
    # Handle different message formats Claude Code might use
    role = msg.get("role", "unknown")
    content = msg.get("content", "")
    timestamp = msg.get("timestamp")

    # Convert timestamps to ISO format if they're not already
    if timestamp:
        if isinstance(timestamp, (int, float)):
            try:
                # Assume Unix timestamp
                dt = datetime.fromtimestamp(timestamp)
                timestamp = dt.isoformat()
            except (ValueError, OSError):
                timestamp = None
        elif isinstance(timestamp, str):
            # Already a string, assume it's in ISO format or close enough
            pass
        else:
            timestamp = None

    # Extract tool calls if present
    tool_calls = []
    if "tool_calls" in msg:
        for tool_call in msg["tool_calls"]:
            normalized_call = {
                "name": tool_call.get("name", "unknown"),
                "input": tool_call.get("input", ""),
                "output": tool_call.get("output", "")
            }
            tool_calls.append(normalized_call)

    return {
        "role": role,
        "timestamp": timestamp,
        "content": content,
        "tool_calls": tool_calls,
        "line_number": line_num
    }


def compute_thread_hash(messages):
    """Compute SHA-256 hash of normalized thread content."""
    # Create a deterministic representation for hashing
    hash_content = {
        "messages": [
            {
                "role": msg["role"],
                "timestamp": msg["timestamp"],
                "content": msg["content"],
                "tool_calls": msg["tool_calls"]
            }
            for msg in messages
        ]
    }

    content_str = json.dumps(hash_content, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(content_str.encode('utf-8')).hexdigest()


def get_thread_title(messages):
    """Extract a meaningful title from the thread messages."""
    for msg in messages:
        if msg["role"] == "user":
            content = msg["content"]
            if isinstance(content, str) and content.strip():
                # Remove markdown formatting and truncate
                clean_content = re.sub(r'[#*`\[\]()]', '', content)
                clean_content = re.sub(r'\s+', ' ', clean_content).strip()
                return clean_content[:100] + ("..." if len(clean_content) > 100 else "")

    return "Untitled Claude Code Thread"


def format_timestamp(ts):
    """Format timestamp for display."""
    if not ts:
        return "Unknown time"

    try:
        dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, AttributeError):
        return ts


def render_content_to_html(content):
    """Convert message content to HTML, handling markdown."""
    if not isinstance(content, str):
        content = str(content)

    # HTML escape first
    html_content = html.escape(content)

    # Basic markdown-like formatting
    # Code blocks
    html_content = re.sub(
        r'```(\w+)?\n(.*?)\n```',
        lambda m: f'<pre><code class="language-{m.group(1) or "text"}">{html.escape(m.group(2))}</code></pre>',
        html_content,
        flags=re.DOTALL
    )

    # Inline code
    html_content = re.sub(
        r'`([^`]+)`',
        r'<code>\1</code>',
        html_content
    )

    # Bold
    html_content = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', html_content)
    html_content = re.sub(r'__([^_]+)__', r'<strong>\1</strong>', html_content)

    # Italic
    html_content = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', html_content)
    html_content = re.sub(r'_([^_]+)_', r'<em>\1</em>', html_content)

    # Line breaks
    html_content = html_content.replace('\n', '<br>\n')

    return html_content


def render_tool_calls_to_html(tool_calls):
    """Render tool calls as HTML."""
    if not tool_calls:
        return ""

    html_parts = ['<div class="tool-calls">']

    for call in tool_calls:
        html_parts.append('<div class="tool-call">')
        html_parts.append(f'<div class="tool-name">🔧 {html.escape(call["name"])}</div>')

        if call.get("input"):
            input_str = str(call["input"])
            if len(input_str) > 500:
                input_str = input_str[:500] + "..."
            html_parts.append(f'<div class="tool-input"><strong>Input:</strong> <code>{html.escape(input_str)}</code></div>')

        if call.get("output"):
            output_str = str(call["output"])
            if len(output_str) > 500:
                output_str = output_str[:500] + "..."
            html_parts.append(f'<div class="tool-output"><strong>Output:</strong> <pre>{html.escape(output_str)}</pre></div>')

        html_parts.append('</div>')

    html_parts.append('</div>')
    return '\n'.join(html_parts)


def generate_html(messages, thread_hash, title, metadata=None):
    """Generate complete HTML document for the thread."""

    # HTML template
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            background-color: #1a1a1a;
            color: #e0e0e0;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }}

        .header {{
            border-bottom: 2px solid #333;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}

        .title {{
            font-size: 1.5em;
            font-weight: bold;
            color: #fff;
            margin-bottom: 10px;
        }}

        .metadata {{
            font-size: 0.9em;
            color: #888;
        }}

        .message {{
            margin-bottom: 25px;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #444;
        }}

        .message.user {{
            background-color: #2d2d2d;
            border-left-color: #4CAF50;
        }}

        .message.assistant {{
            background-color: #1e1e1e;
            border-left-color: #2196F3;
        }}

        .message.system {{
            background-color: #2a2a2a;
            border-left-color: #FF9800;
        }}

        .message-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
            font-size: 0.9em;
        }}

        .role {{
            font-weight: bold;
            text-transform: uppercase;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.8em;
        }}

        .role.user {{
            background-color: #4CAF50;
            color: white;
        }}

        .role.assistant {{
            background-color: #2196F3;
            color: white;
        }}

        .role.system {{
            background-color: #FF9800;
            color: white;
        }}

        .timestamp {{
            color: #666;
            font-size: 0.8em;
        }}

        .content {{
            white-space: pre-wrap;
            word-wrap: break-word;
        }}

        .tool-calls {{
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #333;
        }}

        .tool-call {{
            background-color: #1a1a1a;
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 10px;
        }}

        .tool-name {{
            font-weight: bold;
            color: #9C27B0;
            margin-bottom: 5px;
        }}

        .tool-input, .tool-output {{
            margin: 5px 0;
            font-size: 0.9em;
        }}

        .tool-input code, .tool-output pre {{
            background-color: #000;
            padding: 5px;
            border-radius: 3px;
            overflow-x: auto;
            display: block;
        }}

        pre {{
            background-color: #000;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
            margin: 10px 0;
        }}

        code {{
            background-color: #333;
            padding: 2px 4px;
            border-radius: 3px;
        }}

        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #333;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}

        .copy-button {{
            position: fixed;
            top: 20px;
            right: 20px;
            background-color: #333;
            color: #fff;
            border: none;
            padding: 10px 15px;
            border-radius: 5px;
            cursor: pointer;
            font-family: inherit;
        }}

        .copy-button:hover {{
            background-color: #555;
        }}

        @media (max-width: 768px) {{
            .container {{
                padding: 10px;
            }}
            .copy-button {{
                position: relative;
                top: auto;
                right: auto;
                margin-bottom: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <button class="copy-button" onclick="copyLink()">Copy Link</button>

        <div class="header">
            <div class="title">{title}</div>
            <div class="metadata">
                <div>Thread Hash: {thread_hash_short}</div>
                <div>Generated: {generation_time}</div>
                <div>Messages: {message_count}</div>
            </div>
        </div>

        {messages_html}

        <div class="footer">
            Generated from Claude Code conversation<br>
            <a href="{gist_url}" target="_blank" style="color: #666;">View on GitHub Gist</a>
        </div>
    </div>

    <script>
        function copyLink() {{
            navigator.clipboard.writeText(window.location.href).then(function() {{
                const button = document.querySelector('.copy-button');
                const originalText = button.textContent;
                button.textContent = 'Copied!';
                setTimeout(function() {{
                    button.textContent = originalText;
                }}, 2000);
            }});
        }}
    </script>
</body>
</html>"""

    # Render individual messages
    messages_html = []
    for msg in messages:
        content_html = render_content_to_html(msg["content"])
        tool_calls_html = render_tool_calls_to_html(msg["tool_calls"])

        message_html = f"""
        <div class="message {msg['role']}">
            <div class="message-header">
                <span class="role {msg['role']}">{msg['role']}</span>
                <span class="timestamp">{format_timestamp(msg['timestamp'])}</span>
            </div>
            <div class="content">{content_html}</div>
            {tool_calls_html}
        </div>"""
        messages_html.append(message_html)

    # Fill template
    return html_template.format(
        title=html.escape(title),
        thread_hash_short=thread_hash[:16],
        generation_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        message_count=len(messages),
        messages_html='\n'.join(messages_html),
        gist_url=metadata.get("gist_url", "#") if metadata else "#"
    )


def main():
    parser = argparse.ArgumentParser(description="Render Claude Code session as HTML and JSON")
    parser.add_argument("--input", required=True, help="Input JSONL session file")
    parser.add_argument("--output-html", help="Output HTML file")
    parser.add_argument("--output-json", help="Output normalized JSON file")
    parser.add_argument("--metadata", help="Output metadata file")
    parser.add_argument("--project-path", help="Project path for metadata")
    parser.add_argument("--session-file", help="Session file path for metadata")

    args = parser.parse_args()

    # Parse session
    messages = parse_jsonl_session(args.input)
    if messages is None:
        print("Error: Failed to parse session file", file=sys.stderr)
        sys.exit(1)

    if not messages:
        print("Error: No messages found in session file", file=sys.stderr)
        sys.exit(1)

    # Compute thread hash
    thread_hash = compute_thread_hash(messages)
    title = get_thread_title(messages)

    # Create normalized thread JSON
    thread_data = {
        "messages": messages,
        "thread_hash": thread_hash,
        "title": title,
        "source": {
            "project_path": args.project_path or str(Path(args.input).parent.parent.parent),
            "session_file": args.session_file or str(Path(args.input)),
            "generated_at": datetime.now().isoformat()
        }
    }

    # Create metadata
    metadata = {
        "version": 1,
        "thread_hash": thread_hash,
        "title": title,
        "created_at": datetime.now().isoformat(),
        "message_count": len(messages),
        "source": {
            "project_path": args.project_path or str(Path(args.input).parent.parent.parent),
            "session_file": args.session_file or str(Path(args.input))
        }
    }

    # Write HTML
    if args.output_html:
        html_content = generate_html(messages, thread_hash, title, metadata)
        with open(args.output_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML written to: {args.output_html}")
    else:
        print("HTML output not specified", file=sys.stderr)

    # Write JSON
    if args.output_json:
        with open(args.output_json, 'w', encoding='utf-8') as f:
            json.dump(thread_data, f, indent=2, ensure_ascii=False)
        print(f"JSON written to: {args.output_json}")
    else:
        print("JSON output not specified", file=sys.stderr)

    # Write metadata
    if args.metadata:
        with open(args.metadata, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        print(f"Metadata written to: {args.metadata}")

    # Print summary for scripting
    summary = {
        "thread_hash": thread_hash,
        "title": title,
        "message_count": len(messages),
        "html_file": args.output_html,
        "json_file": args.output_json,
        "metadata_file": args.metadata
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()