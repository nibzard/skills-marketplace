# Builder Methods Brand Colors

> ⚠️ This file is the SINGLE SOURCE OF TRUTH for hex values used by the Brand Illustrator.
> If you modify any hex values in this file, you MUST also update the `ACCENT_HEX` and
> `SYSTEM_COLORS` mappings in `scripts/generate.py` to maintain consistency.

## Illustration System Colors

These are the specific colors used in brand illustrations:

| Role | Hex | Description |
|------|-----|-------------|
| Line | `#1a1a1a` | All line work |
| Background | `#faf9f7` | Warm off-white canvas (60–70% of image) |
| Shadow (light) | `#ded7ca` | Subtle depth/grounding for light mode |
| Shadow (dark) | `#534f4f` | Subtle depth/grounding for dark mode |
| Accent | *See Primary Accent Colors* | ONE per illustration (20–30% of image) |

## Primary Accent Colors (Illustrations)

> NOTE: If your canonical brand palette differs, replace these with the approved values.

| Name | Token | Hex |
|------|-------|-----|
| Coral | `coral` | `#ff6b6b` |
| Teal | `teal` | `#2ec4b6` |
| Indigo | `indigo` | `#5b5fdd` |
| Amber | `amber` | `#f4b400` |

## Light Mode Neutrals

| Name | Hex | CSS Variable | Usage |
|------|-----|--------------|-------|
| Neutral 100 | `#faf9f7` | `neutral-100` | Page background |
| Neutral 200 | `#f4f2ee` | `neutral-200` | Surface background |
| Neutral 300 | `#ded7ca` | `neutral-300` | Subtle borders, shadows |
| Neutral 400 | `#b6b4b1` | `neutral-400` | Darker borders, icons |

## Dark Mode Neutrals

| Name | Hex | CSS Variable | Usage |
|------|-----|--------------|-------|
| Neutral 600 | `#636363` | `neutral-100` | Borders, icons |
| Neutral 700 | `#534f4f` | `neutral-200` | Subtle borders, shadows |
| Neutral 800 | `#242424` | `neutral-300` | Surface background |
| Neutral 900 | `#121212` | `neutral-400` | Page background |

## Text Colors (Light Mode)

| Name | Hex | Usage |
|------|-----|-------|
| Emphasized | `#1a1a1a` | Headlines, strong text |
| Global | `#767676` | Body text |
| Muted | `#b2b2b2` | Secondary text, captions |
| Semimuted | `#aaaaaa` | Secondary text, captions |

## Text Colors (Dark Mode)

| Name | Hex | Usage |
|------|-----|-------|
| Emphasized | `#f5f4f2` | Headlines, strong text |
| Global | `#afafaf` | Body text |
| Muted | `#717171` | Secondary text, captions |
| Semimuted | `#7a7a7a` | Secondary text, captions |

## Utility Colors

| Name | Hex |
|------|-----|
| Black | `#1a1a1a` |
| White | `#ffffff` |
