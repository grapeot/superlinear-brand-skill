# The slide theme in a presentation-skill canvas deck

The snippets below use historical public SVGs so the public example runs without the internal pack.
For current work, install the private six-layer assets and replace **both** the header logo and favicon;
use `brand/logos/private/logo%20horizontal.png` for the light header and a mark-only PNG for the favicon
(with `type="image/png"`). Ignore `brand/logos/private/` and private render paths before copying the theme.
See [logo_usage.md](logo_usage.md) for dark surfaces and the full selection table.

The presentation skill (<https://github.com/grapeot/presentation_skill>) builds an HTML deck as one world canvas
with a camera: `index.html` holds 1920×1080 frames, `js/deck.js` the slide table, `js/engine.js` the engine (Reveal.js
underneath for clicks, notes and the speaker view), `css/deck.css` the scaffold's tokens and motion vocabulary,
`js/copy.js` the writer's copy that fills `data-slot` elements. This theme changes paint and type only. It never moves
frames, the camera or the click logic, so every presentation-skill rule (one claim per slide, state as a function of
(slide, step), the copy workflow, `tools/shoot.py`, critic rounds, `export-pdf`) still applies.

The reference implementation is the example deck in the source repository,
[`examples/shipping_small_models/`](https://github.com/grapeot/superlinear-brand-skill/tree/master/examples/shipping_small_models) (not part of a skill-only install; the minimal
skeleton below is enough to start without it). It is laid out exactly like the install below (`brand/` inside the deck; in this repo `brand/` is a symlink to the skill's `theme/`, in your deck it is
a real copy). Its `<head>`, `#chrome` and script block can be copied verbatim.

## Install into a deck

1. **Scaffold** with the presentation skill: `scripts/presentation-skill "Topic" --mode html --assets none
   --output deck` (or `--assets mixed` if you will generate plates), then `npm install && npm run vendor` as that
   skill says (Reveal.js is still needed).
2. **Copy the theme:** this skill's `theme/` folder → `deck/brand/` (fonts, logos, placeholders and `typeset.js` come
   along, so the deck stays self-contained and offline).
3. **Fonts: delete the scaffold's `@font-face` block.** `css/deck.css` starts with five `@font-face` lines that load
   Fraunces, Inter and JetBrains Mono from `vendor/fonts/`; `brand/tokens.css` declares the same families (plus
   Outfit) from `brand/fonts/` with a Latin `unicode-range` so CJK text falls through correctly. Keeping both works,
   but every face is declared twice and the winner depends on load order. Delete the five lines; leave the rest of
   `deck.css` untouched.
4. **Stylesheets** in `<head>`, after `css/deck.css`:

   ```html
   <link rel="icon" href="brand/logos/favicon.svg" type="image/svg+xml">
   <link rel="stylesheet" href="css/deck.css">
   <link rel="stylesheet" href="brand/tokens.css">
   <link rel="stylesheet" href="brand/layouts.css">
   <link rel="stylesheet" href="brand/canvas.css">
   ```

5. **Scripts** at the end of `<body>`: `typeset.js` goes after `copy.js` and before `engine.js`:

   ```html
   <script src="vendor/reveal/reveal.js"></script>
   <script src="vendor/reveal/notes/notes.js"></script>
   <script src="js/copy.js"></script>
   <script src="brand/typeset.js"></script>
   <script src="js/deck.js"></script>
   <script src="js/engine.js"></script>
   ```

6. **Chrome:** in `#chrome` (outside the generated `FRAMES` block), add the logo and the brand line; keep the
   scaffold's runs:

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

7. **Patch the scaffold's `tools/shoot.py` before the first run.** The stock harness serves the deck with
   `http.server.ThreadingHTTPServer`, whose listen backlog is 5. With the theme installed, every page load requests
   about 30 files at once (four stylesheets, six fonts, logos, scripts), the backlog overflows, and `shoot.py` reports
   `net::ERR_CONNECTION_RESET` on a random stylesheet as console errors and failed requests. Replace the line that
   creates the server:

   ```python
   # tools/shoot.py: replace  srv = http.server.ThreadingHTTPServer(("127.0.0.1", a.port), handler)
   class Server(http.server.ThreadingHTTPServer):
       request_queue_size = 128      # the default 5 resets connections once the brand theme adds ~30 files per load
       daemon_threads = True
   srv = Server(("127.0.0.1", a.port), handler)
   ```

   Alternatively run this skill's renderer, which already does this and can capture every step like `shoot.py`:
   `python <skill_dir>/scripts/render.py deck deck/ --all-steps --out deck/verification/<round>`. The presentation
   skill's `start-server.py` for live preview is unaffected in practice (a browser opens few connections at a time),
   but if a preview shows a missing stylesheet, reload.
8. **Frames:** write them in `tools/build_index.py` with the layouts in [layouts.md](layouts.md) (each frame:
   `<div class="frame" id="..."><div class="sa-pad sa-LAYOUT">…</div></div>`), or keep the scaffold's own components
   (`.specimen`, `.pipeline`, `.quote`, `.timeline` …): `canvas.css` re-skins those too.
9. **Register:** record in the deck's `visual_guideline.md`: "Superlinear Academy monochrome editorial theme
   (superlinear-brand skill)", plus what green and oxblood mean in this deck.
10. **Verify** with both tools: the patched `tools/shoot.py` (every step, the presentation skill's acceptance) and
   `python <skill_dir>/scripts/render.py deck deck/ --out deck/verification/brand_<round>` (layout, SVG and typography audit). Use
   `--final` on the version you ship. See [verification.md](verification.md).

## Copy slots, emphasis and typography

The presentation skill's copy workflow puts on-screen text in `copy/copy.md` → `js/copy.js`, and the engine fills
each `data-slot` element with `textContent`. Plain text cannot carry a `<span class="sa-em">`, so the theme defines one
inline convention, implemented by `brand/typeset.js`:

- **`==phrase==` in a slot string becomes the green emphasis** (`<span class="sa-em">phrase</span>`). Example from the
  reference deck (`js/copy.js`):

  ```js
  claim: { headline: "A model that runs where the user is beats a better one that ==waits on a network==", … }
  ```
  ```html
  <h2 class="sa-display sa-h1" data-slot="claim.headline" data-max-lines="3"></h2>
  ```

  Tell the writer the convention in the voice contract: at most one `==…==` per frame, only on the phrase that carries
  the claim, only in headline or claim fields (`headline`, `claim`, `takeaway`), never in notes. Oxblood emphasis and
  any other markup stay in the builder's markup, not in copy.
- **Typography is automatic for slot text:** straight quotes become ’ ‘ “ ”, and a number followed by a unit (`115 ms`,
  `2 s`, `40 %`, `8 GB`) gets a no-break space so the pair never splits across lines. Static text written in the frames
  is typeset too.
- **Static markup:** text written directly in frames is typeset too (quotes, units). To allow `==phrase==` in static
  markup as well, put `data-typeset` on the element. `data-no-typeset` exempts a subtree; `<code>`, `<pre>`, `<kbd>`
  and `<samp>` are always skipped.
- **Extra units:** set `window.SA_TYPESET_UNITS = ["tokens", "GPUs"]` before loading `typeset.js`; they are added to
  the defaults (`ms s min h px pt fps % × x B K M KB MB GB TB tok`). The audit's number+unit check uses the defaults.
- **Limits:**
  - Quotes are decided from the character before them, so an apostrophe that starts a word (`'90s`, `'em`) becomes ‘
    instead of ’; type ’ there yourself. A quotation that opens in one block and closes in another is handled per block.
  - A `==…==` pair must sit inside one text node (not split across elements), must not start or end with a space, and
    cannot contain `=`; `a == b` is left as it is.
  - The scaffold's typewriter effect (`.type`) splits text into letters before the helper runs, so it cannot carry
    `==` emphasis (a console warning names the slot), and its word split turns the no-break space back into a plain
    space. Keep emphasis and number+unit pairs out of `.type` elements.
- Without `typeset.js`, `render.py` reports visible `==` markers as a problem and straight quotes or breakable
  number+unit spaces as warnings.

## Minimal `index.html` skeleton

Everything a themed canvas deck needs, in one place (frames normally come from `tools/build_index.py`):

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Talk title</title>
<link rel="icon" href="brand/logos/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="vendor/reveal/reset.css">
<link rel="stylesheet" href="vendor/reveal/reveal.css">
<link rel="stylesheet" href="css/deck.css">          <!-- scaffold, with its @font-face block deleted -->
<link rel="stylesheet" href="brand/tokens.css">
<link rel="stylesheet" href="brand/layouts.css">
<link rel="stylesheet" href="brand/canvas.css">
</head>
<body>
<div class="reveal"><div class="slides"></div></div>
<div id="stage">
<div id="viewport"><div id="world">
<!-- FRAMES:BEGIN -->
<div class="frame" id="claim">
  <div class="sa-pad sa-claim">
    <div class="sa-kicker">The claim</div>
    <h2 class="sa-display sa-h1 rise" data-in="claim.0" data-max-lines="3" data-slot="claim.headline"></h2>
  </div>
</div>
<!-- FRAMES:END -->
</div></div>
<div id="grain"></div>
<div id="chrome">
  <img class="sa-chrome-logo" src="brand/logos/primary-black-compact.svg" alt="Superlinear Academy">
  <div class="run top"><span>Talk title · Occasion</span><span id="part"></span></div>
  <div class="rule top"></div>
  <div class="rule bot"></div><div class="progress" id="progress"></div>
  <div class="run bot"><span>Speaker · Date</span><span id="folio"></span></div>
  <div class="sa-brandline">Make what lasts.</div>
</div>
</div>
<script src="vendor/reveal/reveal.js"></script>
<script src="vendor/reveal/notes/notes.js"></script>
<script src="js/copy.js"></script>        <!-- window.COPY = { claim: { headline: "… ==key phrase==", notes: "…" } } -->
<script src="brand/typeset.js"></script>
<script src="js/deck.js"></script>        <!-- window.DECK = [ { id: "claim", part: "I · Part", steps: 1 } ] -->
<script src="js/engine.js"></script>
</body>
</html>
```

## What `canvas.css` does

- Maps the scaffold tokens onto the brand: `--paper`, `--card`, `--ink*`, `--rule` → editorial theme;
  `--problem` (the lasting / main point) → green; `--patch` (the expiring side) → oxblood; `--serif` → Fraunces,
  `--sans` → Outfit, `--mono` → JetBrains Mono.
- Hides the paper-grain layer (`#grain`): the theme is clean paper.
- **Chrome, neutral by design:** compact logo at top-left (34 px tall), running header in Outfit 500 letter-spaced,
  progress rule and centred "Make what lasts." in `--sa-ink-2`, folio in mono. Green in the chrome would appear on
  every frame and teach the audience that green is decoration; keeping it neutral lets green inside a frame mean
  "this is the point". The short green rule before each kicker is the one structural green mark. For a short,
  brand-forward reel you may set `--sa-brandline-color` / `--sa-progress-color` to `var(--sa-green-text)` /
  `var(--sa-green)` on `:root`.
- Display text in Fraunces with soft optical sizing; labels in Outfit.
- Cards flat with hairlines (all shadows removed); the lasting card half keeps its 6 px green inset bar; the expiring
  half keeps oxblood hatching.
- Plates in neutral grey ink (`grayscale(1) contrast(1.08) brightness(.92)`).
- Inline SVG written with the scaffold's literal colours (`#23407a`, `#b6422a`, `#1b2130`, `#8b8f99` …) is remapped
  onto the brand by attribute selectors, so scaffold examples recolour without edits.
- The navigator button (bottom right, key M) becomes a quiet hairline control on the paper colour. `render.py` hides it
  in captures; add `class="sa-no-navbtn"` to `<body>` to hide it for recordings or kiosk playback.

## Running header vs kicker

The running header's `#part` (set per slide in `js/deck.js`) names the section of the talk, the same on every slide of
that part: "II · How". The frame's kicker names what this frame is about: "Cost per 1,000 requests". Never repeat the
part name in the kicker; if a kicker would say the same thing as `#part`, write what the frame measures or compares
instead.

## Motion and media

Keep the presentation skill's vocabulary (rise, pen, counters, split cards, camera push-in) and its rule that motion
explains. Recordings play through `window.DECK_HOOKS` (see `js/deck.js` in the example: play on enter, `pause()` and
`load()` on leave so the poster returns). Screenshots and the PDF show the poster, so the poster must be a
representative frame of that recording, not a shared title card.

## Class-name collisions

The scaffold's `deck.css` styles some short class names **globally**. Using one of these on your own element inside a
`.sa-*` layout inherits its borders, positioning or fonts (a `.role` line got a bordered card; a `.note` line got an
absolutely positioned italic block with a left rule). Avoid:

`.note .label .small .lede .source .quote .role .roles .closer .numeral .cell .cells .col .course .timeline .pipeline
.pstage .window .trace .slab .stack .scale .duty .duties .lever .levers .board .specimen .strike .veil .tri .tcol .answers
.rulelist .mitem .mrow .mspec .erow .erows .jcase .jtag .jtext .beat .beats .bracket .docs .rungtext`

`render.py` warns (`scaffold_class`) when it finds one inside `.sa-pad`. The scaffold classes you **may** use on
purpose are the engine and motion vocabulary: `.frame`, `.rise`, `.pop`, `.pen`, `.plate`, `.type`, `.counter`, and
the type classes `.display .h1 .h2 .h3 .kicker` (re-skinned by `canvas.css`).

Names the scaffold uses only as descendants of its own components (`.row`, `.tick`, `.track`, `.name`, `.tag`,
`.body`, `.n`, `.t`, `.q` …) are safe inside `.sa-*` layouts; the layout library itself uses `.sa-spec .row`,
`.sa-timeline .track` and `.tick`.

## Content box

Layouts sit in `.sa-pad`: x 160–1760, y 130–950, the presentation skill's content box. The running header (y 0–72)
and footer (y 1012–1080) sit outside it.

## Dark stage variant

There is no dark theme in this skill yet. If a venue needs one (a projector in a bright room is not a reason; the
sage paper projects well), set the page to `--sa-forest` or `--sa-primary-dark`, text to `--sa-paper`, swap the
logo to `primary-white-compact.svg`, use a lighter green of the same hue for marks, and invert line plates with
`filter: invert(1)`. Render and check contrast before using it.
