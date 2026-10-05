# Logo usage

The logo files in `theme/logos/` are the official screen SVGs, renamed to ASCII. They are trademarks, provided for
on-brand use only (see `theme/logos/TRADEMARKS.md`).

| File | Official asset | Use |
|---|---|---|
| `primary-black.svg` | Primary_Black_NoBgd | Full lockup with its clear space built into the file (1440×500 canvas). Closing slides, centred placements |
| `primary-white.svg` | Primary_White_NoBgd | The same on a dark background |
| `primary-black-compact.svg` | Primary_Black_NoBgd_Compact | Tight crop (2400×580). Running headers, promo headers: anywhere you set the clear space yourself |
| `primary-white-compact.svg` | Primary_White_NoBgd_Compact | The same on a dark background |
| `icon-black.svg` / `icon-white.svg` | Icon_Black_NoBgd / Icon_White_NoBgd | The mark alone, square canvas with clear space. Avatars, tiny spaces |
| `favicon.svg` | Favicon | Below 50 px only: browser tabs |

## Choosing

1. **Brand level.** Superlinear Academy by default. The sub-brand **Superlinear AI** only when the piece promotes an
   AI course or the AI community specifically; its files are not bundled, so ask for them rather than improvising.
2. **Background.** Light background → black logo. Dark background (`--sa-forest`, `--sa-primary-dark`, a dark photo)
   → white logo. Nothing else.
3. **Space.** Wide and short (running header, promo header) → compact lockup. Centred with room → full lockup.
   Square → icon.

## Size and clear space

- Minimum digital size of the full primary lockup: **144×50 px** (its whole canvas, which includes clear space).
  That corresponds to a compact lockup about **30 px tall**. The theme uses 34 px in slide headers and 36–40 px on
  promos.
- **Clear space:** the full files carry it. With the compact file, keep at least **0.4 × the logo height** of empty
  space on every side (the proportion the full file uses). In the slide header the running text starts 176 px from
  the page margin for that reason.
- Favicon under 50 px; never shrink the full lockup that far.

## Don'ts (from the brand manual)

- Do not stretch or squash: set only `height` (or only `width`), never both.
- Do not add shadows, glows, gradients, outlines or CSS filters.
- Do not recolour. In particular, do not tint the logo or the mark brand green with a CSS mask or `fill` override:
  the shipped colours are black, white and (retired) blue. The green kicker rule is the theme's brand accent instead.
- Do not scale the symbol and the wordmark separately, or rebuild the wordmark in a font.
- Do not use outline / stroke-only versions.
- Do not crowd it: no text or rule inside the clear space.
- When a long line of text would force the lockup wider, change the layout, not the logo.

## Implementation

Always an `<img>` of the file: `<img class="sa-chrome-logo" src="brand/logos/primary-black-compact.svg"
alt="Superlinear Academy">`. Do not use `mask-image` / `-webkit-mask` with a local file: under `file://` the mask
fails to load in Chromium and the logo disappears, and a mask is a recolouring tool anyway. Show the logo once per
frame: in the running header for slides, top-left on promos.

## Co-branding

Partner and sponsor marks need a visible separator rule between the Superlinear Academy logo and the partner mark.
Separator thickness scales with the lockup: `α = H / H_min`, thickness `= α × 1 px` (1 px at minimum size). Align
the two marks on their optical centres and give them equal visual weight.
