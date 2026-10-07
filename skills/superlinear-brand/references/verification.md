# Verification

A visual is done when the audit passes **and** you have looked at every rendered image at full size against the
checklist below. The audit catches geometry, offline loading and typography; only looking catches taste.

## 1. Render and audit

```bash
# promo pages (size and safe area come from the page's <meta> tags); PNGs land next to the pages unless --out-dir
python <skill_dir>/scripts/render.py page path/to/promo.html [more.html …] [--out-dir out/] [--scale 2] [--final]

# a presentation-skill canvas deck: every slide at its last step (or its `print` step) → NN_<id>.png + contact_sheet.jpg
python <skill_dir>/scripts/render.py deck path/to/deck [--out path/to/deck/verification/brand_r1] [--all-steps] [--final]
```

Deck mode serves the **deck directory** on a loopback port (with a deep listen backlog, see
[pitfalls.md](pitfalls.md)) and writes to `<deck>/verification/brand/` unless `--out` is given; give each review round
its own `--out`, as the presentation skill does. Pass `--root DIR` only if the deck links files above its own
directory (it then serves `DIR`). `--all-steps` captures every step of every slide (`NN_<id>_<step>.png`), like the
presentation skill's `shoot.py`. Captures hide the navigator button and show each `<video>` at its poster. The local
server serves files only (no directory listings). Requests to any other origin are recorded and **aborted**, so a render
never reaches the network.

In page mode the canvas size and safe area are read from the page's `<meta name="sa:canvas">` / `<meta
name="sa:safe">` through the DOM (attribute order and quoting do not matter); `--size` overrides the canvas.

**Exit codes:** `0` clean; `1` audit problems (JSON report on stdout); `2` the render could not run at all (missing
page, deck directory not found or outside `--root`, no `index.html`, not a presentation-skill canvas deck, Chromium
not installed). Exit 2 prints `{"error": "…"}`; fix the setup, not the slides.

**Problems** (exit code 1):

| Key | Meaning |
|---|---|
| `console_errors`, `failed_requests` | Something did not load or threw; `failed_requests` also lists every HTTP response ≥ 400 with its URL |
| `external_requests` | A request to anything but `file://` / the loopback server (CDN fonts, analytics, remote images); it was blocked |
| `meta` | An `sa:canvas` / `sa:safe` meta that cannot be parsed (the page is then rendered at 1920×1080 / without a safe-area check), or an unknown `sa:` meta |
| `slide_table` | (deck) a slide whose `steps` is not an integer ≥ 1 or whose `print` is outside `0..steps-1` |
| `font_errors` | A vendored font failed to load (wrong path) |
| `offcanvas` | HTML text, an image or a video extends past the canvas (page mode) or past its frame (deck mode) |
| `unsafe` | ... is outside the `sa:safe` area (`[data-bleed]` exempt) |
| `wrapped` | A `[data-max-lines]` element wrapped to more lines than allowed |
| `number_unit_break` | A line break falls between a number and its unit ("115" / "ms") |
| `images` | An `<img>` did not load, or a `<video>` has no poster |
| `cropped` | An `img`/`video.sa-uncropped` is cropped (`object-fit: cover`) or stretched |
| `svg_text_outside` | SVG `<text>` extends past its `<svg>` box |
| `svg_text_overflow` | SVG `<text>` whose centre lies inside a `<rect>` is not fully inside that rect (a label running out of its box) |
| `svg_text_overlap` | Two SVG `<text>` boxes overlap (an axis title on a tick label, two value labels) |
| `unprocessed_markup` | `==` emphasis markers are visible (`typeset.js` not loaded, or used inside `.type`) |
| `placeholders` | Only with `--final`: draft content still on the page, i.e. any `.sa-placeholder` element (box or marker), any `<img>`/`<video>` loaded from a `placeholders/` folder, and visible stand-in text (`Speaker Name`, `Month DD`, `讲者姓名`, `某月某日`) |
| `missing_slots` | (deck) a presentation-skill copy slot was not filled |

**Warnings** (reported under `warnings`, exit code unaffected):

| Key | Meaning |
|---|---|
| `straight_quotes` | `'` or `"` in visible text (load `typeset.js`, or type ’ “ ”) |
| `number_unit_space` | A breakable space between a number and its unit; it may break after an edit (use U+00A0 or `typeset.js`) |
| `scaffold_class` | An element inside `.sa-pad` uses a class the scaffold's `deck.css` styles globally (`.note`, `.role` …) |
| `placeholders` | Without `--final`: the same list, as a reminder of what the draft still lacks |

`fonts_loaded` lists the faces actually used, a quick check that the brand fonts (not fallbacks) rendered.

**What the audit does not check:** SVG text against lines, paths, circles or images (only against other text and
rects); HTML elements overlapping each other (only against the frame, canvas and safe area); text over an image; colour
use and contrast of new pairings; whether a poster is representative; anything about taste. Elements marked
`data-audit-skip` are excluded from the SVG checks. Use it for deliberate overlaps only, and say why in a comment.

For decks, also run the presentation skill's own `tools/shoot.py` (patched as in [slide_theme.md](slide_theme.md)
step 7) and its critic round; this audit does not replace them.

## 2. Look at every frame

Open each PNG (for decks, the contact sheet first, then every slide at full size). Check:

**Brand**
- [ ] Paper is the pale sage `#eef0ec` (or the card colour), not white, not yellow.
- [ ] Green budget: the chrome's fixed green (footer brand line, progress rule) and the other structural marks (kicker rule, CTA bullet dashes, the timeline's current
      dot, a recommended table column's header rule) do not count; beyond them at most **one** green emphasis per frame
      (the claim's phrase, the recommended card, your own number or bar, the button). Nobody else's number is green.
- [ ] Oxblood only for the rejected / expiring side or a stated cost, never decoration.
- [ ] No shadows, gradients, glows, icon grids, stock photos.
- [ ] Logo: correct file (black on light), not stretched, not recoloured, clear space respected, once per frame.

**Type**
- [ ] Headlines in Fraunces, labels in Outfit, numbers in mono. No fallback faces (compare with the example renders).
- [ ] No title wrapped unexpectedly, no orphaned single word on a title's last line, no clipped descenders.
- [ ] Chinese glyphs render in the intended serif or sans, punctuation not orphaned at a line start.
- [ ] Nothing below 20 px except source lines and the chrome.
- [ ] Typographic quotes (’ “ ”) and unbroken number+unit pairs.

**Layout**
- [ ] Nothing overlaps; nothing touches the frame edge or the running header and footer.
- [ ] Diagram and chart labels clear of lines, bars and each other (the audit only checks text against text and rects).
- [ ] Event covers: everything inside the safe area; still legible when the image is scaled to 600 px wide.
- [ ] Headshots, screenshots and recordings whole; dark media in a tight dark frame, not on a light mat.
- [ ] Every data slide has a source line; every number traces to a source.

**Content**
- [ ] No placeholder text or `.sa-placeholder` left in a final image (`--final`).
- [ ] Kicker and running header say different things.
- [ ] No private data: emails, internal links, student names, IDs.

## 3. Contrast spot check

The token pairs are pre-checked (table in [brand_tokens.md](brand_tokens.md)). Re-check only when you introduce a
new pairing: text on an image, text on the forest band, green text under 24 px. Target 4.5:1 for text under 24 px,
3:1 for larger text and non-text marks.

## 4. Record

In a deck, write what you rendered and what you fixed in the presentation skill's `validation.md`. For a promo,
keep the HTML next to the PNG so the next edit starts from source, not from pixels.
