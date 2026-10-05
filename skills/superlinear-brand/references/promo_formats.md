# Promo images, event covers, OG cards

Each image is one HTML page whose `<body>` is the canvas. Templates are in `templates/`; rendered examples are in
`examples/promo/screenshots/` (`promo_16x9.png`, `event_cover_2_8.png`, `og_1200x630.png`, and the Chinese
`promo_16x9_zh.png`).

| Format | Size | Template | Safe area (L,T,R,B) | Typical use |
|---|---|---|---|---|
| 16:9 promo | 1920×1080 | `promo_16x9.html` | 60, 24, 60, 24 | Social post, video title card, a promo slide in someone else's deck |
| Event cover 2.8:1 | 2100×750 | `event_cover_2_8.html` | 220, 60, 220, 60 | Community event header (the platform crops and overlays edges) |
| OG / link preview | 1200×630 | `og_1200x630.html` | 36, 36, 36, 36 | Shared-link card on social sites and chat apps |

Each template declares its size and safe area in `<meta name="sa:canvas">` and `<meta name="sa:safe">`;
`scripts/render.py page` reads both, so the audit enforces the safe area.

## Making one

1. Copy the template next to your working files. Keep the theme reachable: either copy `theme/` beside it and change
   `../theme/` to `theme/`, or point the paths at the installed skill's `theme/` with absolute paths. The page must
   load only local files.
2. Edit the lines marked `EDIT`. Delete optional lines rather than leaving placeholder text.
3. Replace `theme/placeholders/headshot.svg` with the speaker's **full square photo** (`img.sa-uncropped`, shown
   whole). Do not crop to the face, do not use `object-fit: cover`, do not add a circle mask. If the photo is not
   square, it letterboxes on the card colour; better, get a square original.
4. Chinese copy: add `.sa-zh` to the title, subtitle, tag and secondary time line (see `examples/promo/promo_16x9_zh.html`).
   Primary language first; the other language on its own line, never in brackets.
5. Render: `python scripts/render.py page my_promo.html --out-dir out/` (add `--scale 2` for a 2× export). Fix
   every problem the audit reports, then open the PNG and run the checklist in [verification.md](verification.md).

## Copy rules for promos

- **Title:** the promise or the thing made, at most two lines (`data-max-lines="2"`). 16:9 at 96 px holds about
  20 Latin characters per line in the 900 px column; the cover at 76 px about 28; Chinese at 76 px about 11
  characters per line. Shorten the words before shrinking the type; never go below 64 px on 16:9.
- **Subtitle:** one sentence, one line on the cover.
- **Kicker:** facts about the format (Live · Online · 60 min). No hype words.
- **Time:** day, date, time with zones (PT / ET), in the audience's language first.
- **Tag (top right):** what kind of event (Free live session, Course, Workshop).
- **Footer (16:9):** brand name, "Make what lasts." centred in green, the site URL. Only real URLs.
- No emojis, no exclamation marks, no stock photos, no screenshots of the logo.

## Format notes

**16:9.** The text column is vertically centred against the 600 px headshot. Without a speaker, delete the
`<figure>` and widen `.sa-p-text` to 1400 px (`style="width:1400px"`).

**Event cover 2.8:1.** Platforms crop the left and right edges at narrow widths and draw buttons over the corners, so
nothing but the green band goes outside the 220 / 60 px insets (the band carries `data-bleed`). The kicker rule is
inline here, not hanging in the margin. Check the render at full size and at 600 px wide: the title must still read.

**OG.** Previews are shown at 300–500 px wide. One short title at 84 px, an optional subtitle, the URL. No photo, no
date, unless the date is the news.

## Dark variant

For a dark placement, set `body` background to `--sa-forest`, text colours to `--sa-paper` and a light grey, swap
the logo to `primary-white-compact.svg`, and keep the green for the band and the time rule only (green text on forest
does not have enough contrast). Render and check contrast; there is no dark template yet.
