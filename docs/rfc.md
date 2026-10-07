# RFC: design of the Superlinear Academy brand skill

## Summary

A layered package: **tokens → CSS theme → layout library (+ typesetting helper) → templates → render/verify loop**, exposed through one
root skill (`skills/superlinear-brand/SKILL.md`) with focused references. Slides reuse the presentation skill's HTML
canvas engine (<https://github.com/grapeot/presentation_skill>) untouched; this skill only adds stylesheets and chrome markup. Promo images are single HTML pages
rendered by Playwright.

## Sources and how they were used

- **The reference deck's default theme ("B · monochrome editorial").** Its token values, type roles and devices
  (logo in the running header, green kicker rule, centred brand line, hairline cards, no shadows, grey plates) were
  generalised into `tokens.css` and `canvas.css`. Its lecture copy, plates and speaker details were not used.
- **The brand folder.** Current theme green and the web token set; the April 2026 manual for logo rules (black on
  light, white on dark, SVG first, no stretch or effects, clear space, sub-brand scope) with its blue accents marked
  as retired. Seven logo SVGs were copied unmodified and renamed.
- **Promo images made for a live session.** Their structure (logo top-left, event tag top-right, kicker, title,
  subtitle, time block with a green rule, square headshot in a hairline frame, footer brand line; cover with a green
  bottom band and wide margins) became the templates. Their lessons became audits or pitfalls: Google Fonts → offline
  audit; subset fonts lacking CJK → fallback stacks and `.sa-zh`; CSS masks failing under `file://` → `<img>` logos;
  long CJK titles wrapping → `data-max-lines` audit; platform crop → `sa:safe` audit; cropped headshots →
  `img.sa-uncropped` audit; the course-site palette → explicit "not the brand" note.

## Design

### 1. Tokens (`theme/tokens.css`)

`@font-face` for the four vendored families, each with the Latin `unicode-range` of its subset, so CJK text never
waits on or falls into a Latin-only face. Custom properties in two groups: brand core (`--sa-green`, `--sa-green-text`,
`--sa-forest`, tints, web tokens) and editorial theme (`--sa-paper`, `--sa-card`, `--sa-ink*`, `--sa-rule`,
`--sa-second`). Font stacks put the CJK families directly after the Latin face. All names are `--sa-` prefixed so they
never collide with a host stylesheet.

Two decisions here:

- **`--sa-green-text: #22683b`.** The brand green is 4.2:1 on the paper, below AA for small text. The brand's web
  token set already has `#22683b` for small emphasis text; the theme uses it for kickers and the footer line and
  keeps `#238343` for marks and large text.
- **Editorial paper `#eef0ec` rather than the web background `#eeede8`.** The deck's sage paper is the approved slide
  look and is the same family as the green; the web tokens stay available for web UI.

### 2. Theme (`theme/canvas.css`, `theme/promo.css`)

`canvas.css` is loaded after the scaffold's `deck.css` and re-maps the scaffold's own variables (`--paper`,
`--problem`, `--patch`, `--serif`, `--sans` …) onto brand tokens, then overrides only paint: shadows removed, hatching
recoloured, plates greyed, inline-SVG literal colours remapped by attribute selector, chrome styled. It does not touch
frame layout, camera or state classes, so the engine's guarantees hold. Unlike the reference deck, the theme is not
behind a body class: linking the file is the opt-in.

`promo.css` defines three fixed canvases on `<body>` (`.f-16x9`, `.f-cover`, `.f-og`) with absolutely positioned
regions. Fixed geometry is deliberate: these are images, and absolute placement makes the safe area and the audit
predictable.

### 3. Layout library (`theme/layouts.css`)

Type primitives plus 18 layouts and patterns, each a `.sa-pad` box (x 160–1760, y 130–950, the presentation skill’s content box)
with a layout class. Layouts use flex/grid inside the box instead of per-element pixel positions, so an agent can
change copy length without recomputing coordinates. They are engine-agnostic: they work inside a canvas `.frame` or a
plain `.sa-slide` section. Inner element names avoid the scaffold's global class names (a collision with `.role`
produced a stray bordered box during development).

### 3b. Typesetting helper (`theme/typeset.js`)

The presentation skill's copy workflow fills `data-slot` elements with `textContent`, which cannot carry markup, so
the claim layout's green phrase was unavailable to slotted copy. Rather than change the engine, `typeset.js` is loaded
between `copy.js` and `engine.js`: it typesets the strings in `window.COPY` (typographic quotes, no-break space between
a number and its unit) before the engine runs, and after the engine has filled the slots it turns `==phrase==` into
`<span class="sa-em">` by building DOM nodes (never `innerHTML`). `==` was chosen because it is Markdown's highlight
syntax, rare in prose, and unambiguous with the notes' `**bold**`. The engine's typewriter (`.type`) splits text into
letters first, so emphasis and no-break pairs are not supported there; the limit is documented and the audit catches
leftover markers.

### 4. Templates (`templates/`)

Plain HTML with `EDIT` comments on the lines meant to change, a `<meta name="sa:canvas">` for size and
`<meta name="sa:safe">` for the safe area, and the placeholder headshot in an `img.sa-uncropped`.

### 5. Render and verify (`scripts/render.py`)

One Playwright script, two modes. `page` opens each HTML file over `file://` at its declared size; `deck` serves the
repository (or a given root) on a loopback port and prints every slide at its last (or `print`) step through the
engine's `deckGoto`. Transitions are disabled before capture. Audits: console and page errors, failed requests,
requests outside `file://`/loopback, font load errors, text, images or videos leaving the canvas or frame, safe-area
violations, `data-max-lines` violations (counted from the text's client rects), a line break between a number and its
unit, images not loaded or videos without a poster, `sa-uncropped` media cropped or stretched, and inside every inline
SVG: text outside the SVG box, text running out of the rect its centre sits in, and text overlapping other text.
Warnings (non-fatal): straight quotes, breakable number+unit spaces, scaffold global class names inside brand layouts,
and placeholders (fatal with `--final`). Deck mode serves the deck directory (not a repository root) with a listen
backlog of 128, can capture every step (`--all-steps`), hides the navigator button and resets videos to their
posters before each capture, and writes a contact sheet. Since v0.3: requests to non-local origins are aborted (and recorded), HTTP
responses ≥ 400 are recorded, page geometry is read from the DOM rather than regex-matched HTML, frames are looked up
with `getElementById`, `--final` also catches stand-in images and text, slide-table `steps`/`print` values are
validated, the local server refuses directory listings, and setup failures exit with code 2 and `{"error": …}` so a
broken setup is never confused with a failing slide. The audit catches
geometry; the skill's verification checklist covers what only eyes catch.

## Composition with the presentation skill

| Concern | Owner |
|---|---|
| Argument, slide list, one claim per slide, notes, copy workflow, critic review | presentation skill |
| Engine (camera, (slide, step) state, Reveal, navigator, PDF export) | presentation skill |
| `tools/shoot.py` (every step), `export-pdf` | presentation skill |
| Colours, fonts, logo, chrome, card and plate treatment, layouts | this skill |
| Last-step render + layout audit, promo images | this skill |

The deck's `visual_guideline.md` (required by the presentation skill) names this theme as its register.

## Reference implementation: why a real canvas deck, not a static gallery

A static gallery of `.sa-slide` sections would have been simpler (no Reveal, no engine). It was rejected because
the main claim of the skill is that the theme drops into a presentation-skill deck unchanged; a gallery would leave
that claim untested, and agents learn most from an example in the exact shape they will build. The cost was small:
the scaffold's `engine.js` and `deck.css` are copied as is (only the font block of `deck.css` removed so fonts come
from the theme), Reveal.js is vendored (≈350 KB, MIT), and frames are hand-written instead of generated by
`build_index.py`. The deck reaches the theme through `brand/`, exactly as a real deck does; in this repository
`brand/` is a symlink to the skill's `theme/` so fonts and logos are not duplicated. (The first version linked
`../../skills/…` directly, which a tester copied verbatim into a real deck where it broke.)

## Chrome colour budget

The first version put green in the footer brand line and the progress rule as well as the kicker rule. In a real
20-slide deck an independent critic read the green as decoration at thumbnail scale, which undermines the rule that
green marks the point. The chrome is now neutral ink (`--sa-brandline-color`, `--sa-progress-color`, both overridable),
the kicker rule is the single structural green, the big-number stat is ink unless marked `.accent`, and the docs state
a per-frame budget: structural marks are fixed, one content emphasis.

**Revised 2026-10-07 (owner decision).** The owner compared a deck built on the neutral chrome with an approved lecture
deck that keeps the footer brand line and progress rule in brand green, and chose the green chrome as the default. The
reasoning: chrome that is identical on every frame reads as structure, not emphasis, so it does not compete with the
one green point inside a frame. The defaults are now `--sa-green` for both variables; the per-frame content budget
is unchanged, and a quiet deck can still set both to `--sa-ink-2`. The footer line uses `#238343` at 15 px (about
4.2:1 on paper), as in the approved deck, rather than `--sa-green-text`; it is a decorative brand line, not body text.

## Media

Recordings are first-class: `.sa-frame` accepts `<video>`, `.sa-frame.tight.dark` removes the light mat around dark
footage, `video.sa-uncropped` is audited like images, and every video needs a representative poster because
screenshots and the PDF print the poster. The example uses two synthetic WebM recordings generated by a script
(VP9 rather than H.264 because headless Chromium builds often lack H.264).

## Illustrations

The example uses inline line drawings (nested squares for distillation on the cover, a funnel and flask plate)
written as SVG with hatching patterns. No raster engravings are bundled: generating or sourcing them licence-clean
was not needed to demonstrate the plate treatment, which `canvas.css` and `.sa-plate-img` apply to any image.

## Alternatives considered

- **One monolithic `brand.css`.** Rejected: promo pages do not need the canvas glue, and decks may not want the
  layout library. Four files with a fixed load order keep each concern small.
- **Body-class themes (`theme-a/b/c`) as in the reference deck.** Rejected for now: only one theme is approved; a
  theme switcher adds engine changes. A dark variant is documented as a manual recipe.
- **Bundling CJK web fonts.** Rejected: Noto Serif SC and Source Han Sans are tens of megabytes; system fonts plus
  explicit stacks are reliable on the machines that render (macOS ships Songti SC and PingFang SC; Linux needs
  `fonts-noto-cjk`). The verification step requires looking at CJK renders.
- **Recoloured green logo mark as the kicker device** (used in some earlier images). Rejected: the brand manual does
  not allow recolouring; the theme's short green rule carries the accent instead.
- **Albert Sans (the logo typeface) as the text face.** The manual names it; the approved slide look uses Fraunces
  and Outfit. The logo files carry Albert Sans themselves, so text type stays with the approved theme.

## Risks and open points

- Logo licensing: the owner confirmed that the logos may be published under the trademark carve-out in `LICENSE`.
- If the logo set is updated, replace the files in `theme/logos/` (keeping the file names) and re-render the
  examples.
- CJK rendering depends on installed system fonts at render time.
