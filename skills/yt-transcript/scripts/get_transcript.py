#!/usr/bin/env python3
"""
YouTube Transcript Fetcher for Claude Skills

Fetches transcripts from YouTube videos and outputs to stdout or file.
Designed for use with Claude Code Agent Skills.

Usage:
  python get_transcript.py <url>                           # Output to stdout
  python get_transcript.py <url> --output transcript.txt   # Save to file
  python get_transcript.py <url1> <url2>                   # Multiple URLs

Requires: pip install youtube-transcript-api
"""

import argparse
import re
import sys
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url):
    """Extract YouTube video ID from various URL formats."""
    url = url.strip()

    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com/watch\?.*v=([a-zA-Z0-9_-]{11})',
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    # If it's already just a video ID
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url):
        return url

    return None


def get_transcript(video_id, include_timestamps=True):
    """Get transcript for a single video."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        return None


def format_transcript(transcript, include_timestamps=True):
    """Format transcript for output."""
    lines = []
    for snippet in transcript:
        if include_timestamps:
            lines.append(f"{snippet.start:.2f}  {snippet.text}")
        else:
            lines.append(snippet.text)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch YouTube transcripts for Claude Skills"
    )
    parser.add_argument("urls", nargs="+", help="YouTube video URL(s)")
    parser.add_argument(
        "-o", "--output", help="Output file (default: stdout)"
    )
    parser.add_argument(
        "--no-timestamps", action="store_true",
        help="Exclude timestamps from output"
    )

    args = parser.parse_args()

    all_transcripts = []

    for url in args.urls:
        video_id = extract_video_id(url)

        if not video_id:
            print(f"Error: Invalid YouTube URL: {url}", file=sys.stderr)
            continue

        transcript = get_transcript(video_id)

        if transcript is None:
            print(f"Error: Could not fetch transcript for: {url}", file=sys.stderr)
            continue

        formatted = format_transcript(transcript, not args.no_timestamps)
        all_transcripts.append(f"# Transcript for {url} (Video ID: {video_id})\n\n{formatted}")

    if not all_transcripts:
        print("Error: No transcripts could be fetched.", file=sys.stderr)
        sys.exit(1)

    output = "\n\n---\n\n".join(all_transcripts)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Transcript(s) saved to: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
