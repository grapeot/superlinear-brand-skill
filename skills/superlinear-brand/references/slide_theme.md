# The slide theme in a presentation-skill canvas deck

The presentation skill's HTML mode builds a deck as one world canvas with a camera: `index.html` holds 1920×1080
frames, `js/deck.js` the slide table, `js/engine.js` the engine (Reveal.js underneath for clicks, notes and the
speaker view), `css/deck.css` the scaffold's tokens and motion vocabulary. This theme changes paint and type only.
It never moves frames, the camera or the click logic, so every presentation-skill rule (one claim per slide, state
as a function of (slide, step), `tools/shoot.py`, critic rounds, `export-pdf`) still applies unchanged.

The reference implementation is `examples/shipping_small_models/` in this repo: the scaffold's engine and
stylesheet, unmodified except for font paths, plus this theme.

## Install into a deck

1. Scaffold: `scripts/presentation-skill "Topic" --mode html --assets none --output deck` (or `mixed` if you will
   generate plates), then `npm install && npm run vendor` as that skill says.
2. Copy this skill's `theme/` folder into the deck as `deck/brand/` (fonts, logos and placeholders come along, so the
   deck stays self-contained and offline).
3. In `index.html` `<head>`, after `css/deck.css`:

   ```html
   <link rel="icon" href="brand/logos/favicon.svg" type="image/svg+xml">
   <link rel="stylesheet" href="brand/tokens.css">
   <link rel="stylesheet" href="brand/layouts.css">
   <link rel="stylesheet" href="brand/canvas.css">
   ```

4. In `#chrome` (outside the generated `FRAMES` block), add the logo and the brand line; keep the scaffold's runs:

   ```html
   <div id="chrome">
     <img class="sa-chrome-logo" src="brand/logos/primary-black-compact.svg" alt="Superlinear Academy">
     <div class="run top"><span>Talk title · Occasion</span><span id="part"></span></div>
     <div class="rule top"></div>
     <div class="rule bot"></div><div class="progress" id="progress"></div>
     <div class="run bot"><span>Speaker · Date</span><span id="folio"></span></div>
     <div class="sa-brandline">Make what lasts.</div>
   </div>
   ```

5. Write frames in `tools/build_index.py` using the layouts in [layouts.md](layouts.md) (each frame:
   `<div class="frame" id="..."><div class="sa-pad sa-LAYOUT">…</div></div>`), or keep the scaffold's own components
   (`.specimen`, `.pipeline`, `.quote`, `.timeline` …): `canvas.css` re-skins those too.
6. Record the register in the deck's `visual_guideline.md`: "Superlinear Academy monochrome editorial theme
   (superlinear-brand skill)", plus anything deck-specific (what green and oxblood mean in this deck).
7. Verify with both tools: the presentation skill's `tools/shoot.py` (every step) and this skill's
   `scripts/render.py deck deck/` (last step of every slide + layout audit). See [verification.md](verification.md).

## What `canvas.css` does

- Maps the scaffold tokens onto the brand: `--paper`, `--card`, `--ink*`, `--rule` → editorial theme;
  `--problem` (the lasting / main point) → green; `--patch` (the expiring side) → oxblood; `--serif` → Fraunces,
  `--sans` → Outfit, `--mono` → JetBrains Mono.
- Hides the paper-grain layer (`#grain`): the theme is clean paper.
- Chrome: compact logo at top-left (34 px tall), running header in Outfit 500 letter-spaced, green 2 px progress
  rule, centred green "Make what lasts." in the footer, folio in mono.
- Display text in Fraunces with soft optical sizing; labels in Outfit; a short green rule before each frame-level
  kicker.
- Cards flat with hairlines (all shadows removed); the lasting card half keeps its 6 px green inset bar; the expiring
  half keeps oxblood hatching.
- Plates in neutral grey ink (`grayscale(1) contrast(1.08) brightness(.92)`).
- Inline SVG written with the scaffold's literal colours (`#23407a`, `#b6422a`, `#1b2130`, `#8b8f99` …) is remapped
  onto the brand by attribute selectors, so scaffold examples recolour without edits.

## Motion

Keep the presentation skill's vocabulary (rise, pen, counters, split cards, camera push-in) and its rule that motion
explains. The theme adds none. Staggered `rise` on list items and a separate beat for a takeaway line are the common
patterns in the example deck.

## Class-name collisions

The scaffold's `deck.css` defines many short global classes. Inside `.sa-*` layouts, do not reuse these names for
your own elements, or you inherit their borders and fonts:

`.role .roles .closer .numeral .label .note .quote .cell .cells .col .course .board .row .flap .track .station
.window .term .trace .slab .stack .duty .lever .scale .ledger .book .plate .pen .type .rise .pop .counter`

(The example once showed a bordered box under the speaker's name because the role line was called `.role`.) The
layout library uses `.position`, `.conclusion`, `.sa-numeral` and `.cat` for that reason.

## Dark stage variant

There is no dark theme in this skill yet. If a venue needs one (a projector in a bright room is not a reason; the
sage paper projects well), set the page to `--sa-forest` or `--sa-primary-dark`, text to `--sa-paper`, swap the
logo to `primary-white-compact.svg`, use a lighter green of the same hue for marks, and invert line plates with
`filter: invert(1)`. Render and check contrast before using it.
