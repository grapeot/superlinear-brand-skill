# Verification

A visual is done when the audit passes **and** you have looked at every rendered image at full size against the
checklist below. The audit catches geometry and offline problems; only looking catches taste.

## 1. Render and audit

```bash
# promo pages (size and safe area come from the page's <meta> tags)
python scripts/render.py page path/to/promo.html [more.html …] --out-dir out/

# a presentation-skill canvas deck: every slide at its last step (or its `print` step),
# NN_<id>.png per slide + contact_sheet.jpg
python scripts/render.py deck path/to/deck --out path/to/deck/screenshots
```

The JSON report lists, per page or slide, any of:

| Key | Meaning |
|---|---|
| `console_errors`, `failed_requests` | Something did not load or threw |
| `external_requests` | A request left `file://` / the loopback server (CDN fonts, analytics, remote images) |
| `font_errors` | A vendored font failed to load (wrong path) |
| `offcanvas` | Text or an image extends past the canvas (page mode) or past its frame (deck mode) |
| `unsafe` | Text or an image is outside the `sa:safe` area |
| `wrapped` | A `[data-max-lines]` element wrapped to more lines than allowed |
| `images` | An `<img>` did not load |
| `cropped` | An `img.sa-uncropped` is cropped or stretched |
| `missing_slots` | (deck) a presentation-skill copy slot was not filled |

Exit code 0 means none of these. `fonts_loaded` lists the faces actually used, a quick check that the brand fonts
(not fallbacks) rendered.

For decks, also run the presentation skill's own `tools/shoot.py` (every step, not only the last) and its critic
round; this audit does not replace them.

## 2. Look at every frame

Open each PNG (for decks, the contact sheet first, then every slide at full size). Check:

**Brand**
- [ ] Paper is the pale sage `#eef0ec` (or the card colour), not white, not yellow.
- [ ] Green appears only where it marks something (kicker rule, the point, the recommended side, the highlighted
      data, the button, the brand line, the progress rule). At most one green emphasis inside the content per frame.
- [ ] Oxblood only for the rejected / expiring side, never decoration.
- [ ] No shadows, gradients, glows, icon grids, stock photos.
- [ ] Logo: correct file (black on light), not stretched, not recoloured, clear space respected, once per frame.

**Type**
- [ ] Headlines in Fraunces, labels in Outfit, numbers in mono. No fallback faces (compare with the example renders).
- [ ] No title wrapped unexpectedly, no orphaned single word on a title's last line, no clipped descenders.
- [ ] Chinese glyphs render in the intended serif or sans, punctuation not orphaned at a line start.
- [ ] Nothing below 20 px except source lines and the chrome.
- [ ] Straight quotes replaced by typographic ones (’ “ ”) in display text.

**Layout**
- [ ] Nothing overlaps; nothing touches the frame edge or the running header and footer.
- [ ] Event covers: everything inside the safe area; still legible when the image is scaled to 600 px wide.
- [ ] Headshots whole (no cropped head or shoulders), in a hairline frame.
- [ ] Every data slide has a source line; every number traces to a source.

**Content**
- [ ] No placeholder text left (`Speaker Name`, `Month DD`, `EDIT`, the silhouette) in a final image.
- [ ] No private data: emails, internal links, student names, IDs.

## 3. Contrast spot check

The token pairs are pre-checked (table in [brand_tokens.md](brand_tokens.md)). Re-check only when you introduce a
new pairing: text on an image, text on the forest band, green text under 24 px. Target 4.5:1 for text under 24 px,
3:1 for larger text and non-text marks.

## 4. Record

In a deck, write what you rendered and what you fixed in the presentation skill's `validation.md`. For a promo,
keep the HTML next to the PNG so the next edit starts from source, not from pixels.
