# Builder Methods Brand Illustrator

Generate on-brand hand-drawn line art illustrations with warm off-white backgrounds, confident black ink lines, and a single accent color.

## Quick Start

```bash
# Install dependencies
pip install google-genai

# Set your API key
export GEMINI_API_KEY="your-key-here"

# Generate an illustration
python3 scripts/generate.py \
  --prompt "A worn leather notebook with handwritten wireframe sketches" \
  --color coral \
  --type scene \
  --output my-illustration.png
```

## Image Types

| Type | Description | Default Size |
|------|-------------|--------------|
| `icon` | Single object, isolated, quick punctuation | 512×512 |
| `scene` | 2–4 objects with suggested environment, hero/header moments | 1200×630 |
| `periphery` | 1–3 objects for corner/edge decorations | 500×500 |

## Accent Colors

- `coral` — `#ff6b6b`
- `teal` — `#2ec4b6`
- `indigo` — `#5b5fdd`
- `amber` — `#f4b400`

## Documentation

- **[SKILL.md](SKILL.md)** — Complete skill instructions and workflow
- **[references/style.md](references/style.md)** — Visual style guide
- **[references/colors.md](references/colors.md)** — Color system (single source of truth)
- **[references/idea-mapping.md](references/idea-mapping.md)** — Connection types and object categories
- **[references/visual-world.md](references/visual-world.md)** — The "day in the life of a builder" concept
- **[references/prompts.md](references/prompts.md)** — Prompt templates and proven patterns

## Environment Variables

- `GEMINI_API_KEY` — Google Gemini API key (also accepts `GOOGLE_API_KEY` or `GENAI_API_KEY`)
- `GEMINI_IMAGE_MODEL` — Optional override (default: `gemini-2.0-flash-image`)

Get an API key from: https://ai.google.dev/
