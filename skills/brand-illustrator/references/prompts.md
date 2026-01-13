# Prompt Patterns (Brand Illustrator)

This doc contains prompt templates and “known good” phrasing to keep outputs consistent.

## Global Prompt Ingredients

Always include:
- style: hand-drawn ink line art, warm off-white background
- linework: confident black lines
- palette: one accent color (and mention it by name)
- restraint: minimal composition, suggested environment only
- exclusions: no photorealism, no 3D, no gradients, no logos

## Negative Prompt Snippet

Add this (or equivalent) when generations drift:
- "no photorealism, no 3D render, no gradients, no glossy shading, no brand logos, no realistic faces, no cluttered background"

## Template: Icon

Use for single-object illustrations.

```text
Hand-drawn ink line illustration of {OBJECT}.
Warm off-white paper background. Confident black linework.
Use accent color {ACCENT_NAME} for a few filled shapes (20–30% coverage).
Minimal shadow grounding (5–10%). Centered composition, lots of negative space.
No photorealism, no 3D, no gradients, no logos.
```

## Template: Periphery

Used for corner decorations and supporting visuals.

```text
Hand-drawn ink line illustration of {OBJECT_1} with {OBJECT_2 optional}.
Warm off-white paper background. Confident black linework.
Accent color {ACCENT_NAME} in a few filled blocks (20–30%).
Keep composition asymmetric and “edge-friendly” with generous negative space.
No photorealism, no 3D, no gradients, no logos.
```

## Template: Scene (Hero)

Use for blog headers and hero moments.

```text
Hand-drawn ink line art scene showing {OBJECTS_LIST} on a desk.
Suggested environment only (e.g., hint of window light or desk edge), not a full room.
Warm off-white paper background. Confident black linework.
Accent color {ACCENT_NAME} used for key fills (20–30%).
Subtle grounding shadows (5–10%). Leave negative space for headline text.
No photorealism, no 3D, no gradients, no logos.
```

## Common “Builder World” Objects (safe defaults)

- worn notebook / open notebook
- ceramic mug with steam
- over-ear headphones
- desk lamp
- simple terminal window / code snippet (generic)
- folder tree / UI wireframe card
- plant / seedling (growth)
- woodworking plane (iteration/refinement metaphor)

## Example Prompts

### 1) Iteration (Metaphor)
"Hand-drawn ink line illustration of a woodworking plane with small eraser shavings beside it, on warm off-white paper. Confident black linework. Accent color Teal fills the plane handle and a small label. Minimal shadow grounding. Lots of negative space. No photorealism, no 3D, no gradients, no logos."

### 2) Planning (Builder World)
"Hand-drawn ink line illustration of an open slightly worn notebook with a pen uncapped, a calendar page peeking out. Warm off-white background, confident black linework. Accent color Coral fills the notebook cover and small highlights. Minimal shadows. Clean, restrained composition. No photorealism, no 3D, no gradients, no logos."

### 3) Digital Artifact (UI)
"Hand-drawn ink line illustration of a simple UI wireframe card and a small chat bubble overlapping it. Warm off-white background, confident black linework. Accent color Indigo fills the card header and a button. Subtle shadows. Lots of negative space. No photorealism, no 3D, no gradients, no logos."

## Prompt “Dial” Checklist

If output is too busy → reduce objects, increase negative space, remove environment details.
If output is too literal → switch to metaphor category objects.
If output looks digital/flat → add “ink on paper” language and “hand-drawn imperfections”.
If output adds logos → explicitly say “no logos, generic device, blank screens.”
