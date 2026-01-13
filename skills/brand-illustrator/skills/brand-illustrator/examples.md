# Brand Illustrator Examples

Full end-to-end workflows showing how to generate brand illustrations.

## Example 1: Blog Hero for "Deep Work"

### Input
**Article**: "Deep Work: How to Focus in a Distracted World"
**Core idea**: Focus requires eliminating distractions and creating intentional work environments
**Where it will live**: Blog header (needs room for headline text)

### Requirements Gathering
- Content context: Article about deep work and focus
- Visual context: Blog header, needs negative space for text
- Accent color: `teal`
- Image type: `scene`
- Dimensions: 1200×630

### Concepting

#### Option A (Metaphor - Focus)
- Connection type: Metaphorical
- Category: Metaphor
- Objects: Single object on empty desk (headphones)
- Rationale: Represents focus through isolation and the "tunnel" metaphor

#### Option B (Atmospheric - Environment)
- Connection type: Atmospheric
- Category: Builder's World
- Objects: Closed door with desk lamp glow, showing late-night work
- Rationale: Captures the "deep work" environment through lighting and setting

#### Option C (Digital Artifact)
- Connection type: Direct
- Category: Digital Artifact
- Objects: Terminal window with single cursor, minimalist editor
- Rationale: Direct representation of focused coding work

### Selected Direction
**Chosen option**: A (with tweak: add subtle desk edge for grounding)

### Final Prompt

> Hand-drawn ink line illustration of over-ear noise-canceling headphones resting on a desk edge. Warm off-white paper background. Confident black linework. Accent color Teal fills the ear cushions. Minimal shadow grounding (5–10%). Centered composition with generous negative space for headline text. No photorealism, no 3D, no gradients, no logos.

### Generation Command

```bash
python3 scripts/generate.py \
  --prompt "Hand-drawn ink line illustration of over-ear noise-canceling headphones resting on a desk edge. Warm off-white paper background. Confident black linework. Accent color Teal fills the ear cushions. Minimal shadow grounding. Centered composition with generous negative space for headline text. No photorealism, no 3D, no gradients, no logos." \
  --color teal \
  --type scene \
  --width 1200 \
  --height 630 \
  --output projects/2026-01-13-deep-work/hero.png
```

### Output
`projects/2026-01-13-deep-work/hero.png`

---

## Example 2: Social Post for "Ship It"

### Input
**Topic**: Shipping a project and celebrating completion
**Context**: Twitter/social media post, needs to be eye-catching at small sizes

### Requirements Gathering
- Content context: Celebrating shipping/completion
- Visual context: Social post (square format, needs to work at small sizes)
- Accent color: `coral`
- Image type: `icon`
- Dimensions: 512×512

### Concepting

#### Option A (Metaphor - Completion)
- Connection type: Metaphorical
- Category: Metaphor
- Objects: Checkbox with checkmark
- Rationale: Universal symbol of completion, clean and iconic

#### Option B (Builder's World - Ritual)
- Connection type: Emotional
- Category: Builder's World
- Objects: Raised coffee mug in celebration
- Rationale: The "ship it" ritual, warm and human

#### Option C (Atmospheric - Time)
- Connection type: Atmospheric
- Category: Builder's World
- Objects: Sunset light through window with closed laptop
- Rationale: End of day, satisfaction of completion

### Selected Direction
**Chosen option**: B (the mug is a recurring brand element that builds recognition)

### Final Prompt

> Hand-drawn ink line illustration of a ceramic coffee mug raised slightly as if in a toast, with steam rising. Warm off-white paper background. Confident black linework. Accent color Coral fills the mug body. Minimal shadow grounding. Centered icon composition with lots of negative space. No photorealism, no 3D, no gradients, no logos.

### Generation Command

```bash
python3 scripts/generate.py \
  --prompt "Hand-drawn ink line illustration of a ceramic coffee mug raised slightly as if in a toast, with steam rising. Warm off-white paper background. Confident black linework. Accent color Coral fills the mug body. Minimal shadow grounding. Centered icon composition with lots of negative space. No photorealism, no 3D, no gradients, no logos." \
  --color coral \
  --type icon \
  --output projects/2026-01-13-ship-it/social.png
```

### Output
`projects/2026-01-13-ship-it/social.png`

---

## Example 3: Course Graphic for "Iterate"

### Input
**Course Module**: "The Art of Iteration: Refinement in Software Development"
**Core idea**: Great software is built through cycles of refinement, not instant perfection
**Where it will live**: Course module thumbnail, needs to convey "craft" and "improvement"

### Requirements Gathering
- Content context: Course about iteration and refinement
- Visual context: Course thumbnail (landscape, needs visual interest)
- Accent color: `amber`
- Image type: `scene`
- Dimensions: 1200×630

### Concepting

#### Option A (Metaphor - Craft)
- Connection type: Metaphorical
- Category: Metaphor
- Objects: Woodworking plane with small wood shavings
- Rationale: Iteration as physical craft, "shaving away" what doesn't belong

#### Option B (Digital - Process)
- Connection type: Direct
- Category: Digital Artifact
- Objects: Terminal showing git history with multiple commits
- Rationale: Direct representation of iterative development

#### Option C (Emotional - Struggle → Progress)
- Connection type: Emotional
- Category: Builder's World
- Objects: Notebook with crossed-out text and cleaner writing below
- Rationale: Shows the messy reality of iteration

### Selected Direction
**Chosen option**: A (woodworking plane is the brand's signature metaphor for iteration)

### Final Prompt

> Hand-drawn ink line illustration of a woodworking plane resting on a desk with small wood curl shavings beside it. Warm off-white paper background. Confident black linework. Accent color Amber fills the plane handle and body. Minimal shadow grounding. Restrained composition with 2–3 objects, suggested environment only. Leave negative space for text. No photorealism, no 3D, no gradients, no logos.

### Generation Command

```bash
python3 scripts/generate.py \
  --prompt "Hand-drawn ink line illustration of a woodworking plane resting on a desk with small wood curl shavings beside it. Warm off-white paper background. Confident black linework. Accent color Amber fills the plane handle and body. Minimal shadow grounding. Restrained composition with 2–3 objects, suggested environment only. Leave negative space for text. No photorealism, no 3D, no gradients, no logos." \
  --color amber \
  --type scene \
  --width 1200 \
  --height 630 \
  --output projects/2026-01-13-iterate/course-thumbnail.png
```

### Output
`projects/2026-01-13-iterate/course-thumbnail.png`

---

## Example 4: Periphery Element for Newsletter Footer

### Input
**Context**: Newsletter footer needs decorative corner element
**Theme**: "Builder's Toolkit" newsletter

### Requirements Gathering
- Content context: Newsletter footer decoration
- Visual context: Periphery element, should be edge-friendly
- Accent color: `indigo`
- Image type: `periphery`
- Dimensions: 500×500

### Concepting

#### Option A (Brand Icon)
- Connection type: Direct
- Category: Builder's World
- Objects: Notebook and pen, slightly overlapping
- Rationale: Core brand elements, recognizable

#### Option B (Digital + Analog)
- Connection type: Atmospheric
- Category: Mixed
- Objects: Small UI card with pen resting on it
- Rationale: Bridges digital work with analog thinking

#### Option C (Simple Accent)
- Connection type: Direct
- Category: Builder's World
- Objects: Single coffee mug with steam
- Rationale: Simple, warm, effective at small sizes

### Selected Direction
**Chosen option**: C (simple and effective for footer usage)

### Final Prompt

> Hand-drawn ink line illustration of a simple ceramic coffee mug with steam rising above it. Warm off-white paper background. Confident black linework. Accent color Indigo fills the mug body. Minimal shadow grounding. Asymmetric, edge-friendly composition with generous negative space. No photorealism, no 3D, no gradients, no logos.

### Generation Command

```bash
python3 scripts/generate.py \
  --prompt "Hand-drawn ink line illustration of a simple ceramic coffee mug with steam rising above it. Warm off-white paper background. Confident black linework. Accent color Indigo fills the mug body. Minimal shadow grounding. Asymmetric, edge-friendly composition with generous negative space. No photorealism, no 3D, no gradients, no logos." \
  --color indigo \
  --type periphery \
  --output projects/2026-01-13-newsletter/footer-accent.png
```

### Output
`projects/2026-01-13-newsletter/footer-accent.png`

---

## Project Documentation Template

Each project should have a `project.md` file documenting the process:

```markdown
# Project: <slug>

## Requirements
- Content context: <article topic or description>
- Core idea: <the single insight this illustrates>
- Visual context: <where it will live, layout notes>
- Accent color: <coral|teal|indigo|amber>
- Image type: <icon|scene|periphery>
- Dimensions: <width>×<height>

## Concepts
### Option A
- Connection type: <direct|metaphorical|atmospheric|emotional>
- Category: <Builder's World|Metaphor|Digital Artifact>
- Objects: <list>
- Rationale: <why it fits>

### Option B
...

### Option C
...

## Selected Direction
- Chosen option: <A|B|C>
- Notes / tweaks: <any feedback or modifications>

## Final Prompt
```text
<final prompt here>
```

## Generation Params
- color: <coral|teal|indigo|amber>
- type: <icon|scene|periphery>
- width: <pixels>
- height: <pixels>
- output: <file path>

## Outputs
- <filename1>
- <filename2>
```
