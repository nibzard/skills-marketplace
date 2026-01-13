#!/usr/bin/env python3
"""
Builder Methods Brand Illustration Generator

Creates on-brand hand-drawn line art images using Google's Gemini image generation (via `google-genai`),
while applying Builder Methods style + color system.

This script is intentionally defensive:
- If the google-genai package isn't installed, it prints install instructions.
- If API key isn't available, it writes a prompt artifact instead of failing silently.
- It always saves a metadata JSON next to the output for reproducibility.

Usage examples:
  python3 scripts/generate.py --prompt "A coffee mug with steam" --color coral --type icon --output out.png
  python3 scripts/generate.py --prompt "Desk scene" --color teal --type scene --width 1200 --height 630 --output out.png
  python3 scripts/generate.py --prompt "Corner element" --color teal --type periphery --output out.png
  python3 scripts/generate.py --prompt "Replace mug with notebook" --reference input.png --color coral --type icon --output out.png
"""

import argparse
import base64
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple

# --- Optional dependency: google-genai ---
try:
    from google import genai  # type: ignore
    from google.genai import types  # type: ignore
except Exception:
    genai = None
    types = None  # type: ignore

# --- Paths ---
SKILL_DIR = Path(__file__).resolve().parent.parent
REFERENCES_DIR = SKILL_DIR / "references"
ASSETS_DIR = SKILL_DIR / "assets"

# --- Load single source of truth colors (references/colors.md) ---
# ⚠️ IMPORTANT: colors.md is the SINGLE SOURCE OF TRUTH for all hex values.
# If you update colors.md, you MUST update the ACCENT_HEX and SYSTEM_COLORS
# mappings below to maintain consistency. Consider adding a validation test.
ACCENT_HEX = {
    "coral": "#ff6b6b",
    "teal": "#2ec4b6",
    "indigo": "#5b5fdd",
    "amber": "#f4b400",
}
SYSTEM_COLORS = {
    "line": "#1a1a1a",
    "background": "#faf9f7",
    "shadow_light": "#ded7ca",
    "shadow_dark": "#534f4f",
}

DEFAULT_DIMS = {
    "scene": (1200, 630),
    "icon": (512, 512),
    "periphery": (500, 500),
}

NEGATIVE_SNIPPET = (
    "no photorealism, no 3D render, no gradients, no glossy shading, "
    "no brand logos, no realistic faces, no cluttered background"
)

@dataclass
class Params:
    prompt: str
    color: str
    type: str
    width: int
    height: int
    output: Path
    reference: Optional[Path] = None
    dark_mode: bool = False
    add_negative: bool = True

def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""

def build_prompt(user_prompt: str, accent_name: str, image_type: str, add_negative: bool) -> str:
    """
    Wraps the user prompt with global style constraints.
    """
    accent_hex = ACCENT_HEX.get(accent_name.lower(), "")
    style = read_text(REFERENCES_DIR / "style.md")
    # We only embed a small, stable snippet from style.md to avoid overly long prompts.
    # Keep this short but authoritative.
    style_snippet = (
        "Style: hand-drawn ink line illustration on warm off-white paper background, "
        "confident black linework, minimal shading, one accent color in flat fills."
    )
    type_hint = {
        "icon": "Single-object icon. Centered composition with lots of negative space.",
        "periphery": "Edge-friendly periphery element. Asymmetric with generous negative space.",
        "scene": "Restrained scene with 2–4 objects and only suggested environment; leave room for headline text.",
    }.get(image_type, "Keep composition restrained with negative space.")
    palette_hint = (
        f"Palette: line {SYSTEM_COLORS['line']}, background {SYSTEM_COLORS['background']}, "
        f"accent {accent_name} {accent_hex} (20–30% coverage), "
        f"subtle shadows (5–10%)."
    )
    parts = [
        user_prompt.strip(),
        "",
        style_snippet,
        type_hint,
        palette_hint,
        "Avoid: logos or trademarks; keep any screen content generic.",
    ]
    if add_negative:
        parts.append(NEGATIVE_SNIPPET)
    return "\n".join(parts).strip()

def b64_image(path: Path) -> str:
    data = path.read_bytes()
    return base64.b64encode(data).decode("utf-8")

def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

def save_metadata(params: Params, final_prompt: str) -> None:
    meta = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "params": {
            "prompt": params.prompt,
            "color": params.color,
            "type": params.type,
            "width": params.width,
            "height": params.height,
            "output": str(params.output),
            "reference": str(params.reference) if params.reference else None,
            "dark_mode": params.dark_mode,
            "add_negative": params.add_negative,
        },
        "final_prompt": final_prompt,
        "colors": {
            "accent_hex": ACCENT_HEX.get(params.color.lower()),
            "system": SYSTEM_COLORS,
        },
    }
    meta_path = params.output.with_suffix(params.output.suffix + ".json")
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

def generate_with_gemini(params: Params, final_prompt: str) -> bytes:
    """
    Calls Gemini image generation via google-genai.

    Uses gemini-3-pro-image-preview with streaming for image generation.
    """
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or os.getenv("GENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing API key. Set GEMINI_API_KEY (or GOOGLE_API_KEY / GENAI_API_KEY).")
    if genai is None or types is None:
        raise RuntimeError("google-genai package not installed. Run: pip install google-genai")

    client = genai.Client(api_key=api_key)

    # Use gemini-3-pro-image-preview model (nanobanana pro)
    model = os.getenv("GEMINI_IMAGE_MODEL", "gemini-3-pro-image-preview")

    # Build content parts
    parts: list[types.Part] = [types.Part.from_text(text=final_prompt)]

    # Reference-guided edit (if a reference image is provided)
    if params.reference:
        ref_b64 = b64_image(params.reference)
        parts.append(
            types.Part.from_inline_data(
                types.InlineData(
                    mime_type="image/png",
                    data=ref_b64,
                )
            )
        )

    contents = [types.Content(role="user", parts=parts)]

    # Configure generation for image response
    generate_content_config = types.GenerateContentConfig(
        response_modalities=["IMAGE", "TEXT"],
        image_config=types.ImageConfig(image_size="1K"),
    )

    # Stream response and extract image data
    data = None
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if (
            chunk.candidates is None
            or chunk.candidates[0].content is None
            or chunk.candidates[0].content.parts is None
        ):
            continue
        if chunk.candidates[0].content.parts[0].inline_data and chunk.candidates[0].content.parts[0].inline_data.data:
            data = chunk.candidates[0].content.parts[0].inline_data.data
            break

    if not data:
        raise RuntimeError("No image data returned from gemini-3-pro-image-preview.")

    # Data may be base64 string or bytes
    if isinstance(data, str):
        return base64.b64decode(data)
    return data

def write_prompt_artifact(params: Params, final_prompt: str) -> None:
    """
    If we can't generate (missing API), we still want a useful artifact:
    - <output>.prompt.txt contains the final prompt
    - <output>.json contains metadata
    """
    ensure_parent(params.output)
    prompt_path = params.output.with_suffix(params.output.suffix + ".prompt.txt")
    prompt_path.write_text(final_prompt + "\n", encoding="utf-8")
    save_metadata(params, final_prompt)
    print(f"Wrote prompt artifact (no image generated): {prompt_path}")

def parse_args() -> Params:
    parser = argparse.ArgumentParser(description="Generate Builder Methods brand illustrations.")
    parser.add_argument("--prompt", required=True, help="Core subject prompt (short).")
    parser.add_argument("--color", required=True, choices=["coral", "teal", "indigo", "amber"], help="Accent color.")
    parser.add_argument("--type", required=True, choices=["icon", "scene", "periphery"], help="Image type.")
    parser.add_argument("--width", type=int, default=0, help="Width in pixels (default depends on type).")
    parser.add_argument("--height", type=int, default=0, help="Height in pixels (default depends on type).")
    parser.add_argument("--output", required=True, help="Output PNG path.")
    parser.add_argument("--reference", default=None, help="Optional reference image path for edit/variation.")
    parser.add_argument("--dark-mode", action="store_true", help="If set, prefer dark-mode grounding shadows.")
    parser.add_argument("--no-negative", action="store_true", help="Disable negative prompt snippet.")
    args = parser.parse_args()

    if args.width <= 0 or args.height <= 0:
        w, h = DEFAULT_DIMS[args.type]
        width = args.width if args.width > 0 else w
        height = args.height if args.height > 0 else h
    else:
        width, height = args.width, args.height

    ref = Path(args.reference).expanduser().resolve() if args.reference else None
    out = Path(args.output).expanduser().resolve()
    return Params(
        prompt=args.prompt,
        color=args.color,
        type=args.type,
        width=width,
        height=height,
        output=out,
        reference=ref,
        dark_mode=bool(args.dark_mode),
        add_negative=not bool(args.no_negative),
    )

def main() -> None:
    params = parse_args()
    final_prompt = build_prompt(params.prompt, params.color, params.type, params.add_negative)

    ensure_parent(params.output)

    # Try generation if possible; otherwise produce prompt artifact.
    try:
        img_bytes = generate_with_gemini(params, final_prompt)
    except Exception as e:
        print(f"[WARN] Could not generate image via Gemini: {e}")
        if genai is None:
            print("Install dependency: pip install google-genai")
        print("Falling back to prompt artifact.")
        write_prompt_artifact(params, final_prompt)
        return

    # Save image
    params.output.write_bytes(img_bytes)
    save_metadata(params, final_prompt)
    print(f"Wrote image: {params.output}")

if __name__ == "__main__":
    main()
