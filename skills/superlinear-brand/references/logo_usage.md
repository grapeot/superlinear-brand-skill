# Logo usage

Current production work uses the internal six-layer identity pack in `theme/logos/private/`, installed separately
through authorized internal channels. It is not publicly distributed or MIT-licensed. Keep the source pack and
renders embedding it out of public repositories. If it is missing, request it or use an explicit placeholder.

The public files in `theme/logos/` are historical eight-layer screen SVGs, renamed to ASCII. They remain for
archival work and public sample templates (see `theme/logos/TRADEMARKS.md`); do not mix them with current marks.

## Current internal asset selection

Paths below are relative to `theme/logos/private/`. Retain original filenames and folder hierarchy.

| File | Recommended surface / context |
|---|---|
| `logo horizontal.png` | Green transparent horizontal lockup; default on light headers, decks and documents |
| `logo horizontal 2.png` | White horizontal lockup on a green tile; self-contained brand panels |
| `logo vertical.png` | Green transparent vertical lockup; light square or vertical layouts |
| `logo vertical 2.png` | White vertical lockup on a green tile; large brand panels, not small avatars |
| `App Logo.png` | 3840×3840 mark-only white-on-green App icon; high-resolution source for small icons |
| `App 左上角logo.png` | Green transparent App header lockup |
| `Linkedin logo 1.png` | Mark-only white-on-green avatar; suited to social profile placement |
| `Linkedin logo 白底.png` | Green mark on a white square |
| `Linkedin logo 透明底.png` | Green transparent mark |
| `开屏.jpg` | Complete bilingual splash composition; preserve the entire canvas |
| `视频logo/横向logo_white.png` | Approved white transparent horizontal master; dark wide surfaces |
| `视频logo/竖向logo_white.png` | Approved white transparent vertical master; dark portrait surfaces |
| `视频logo/图像部分_white.png` | Approved white transparent standalone mark; dark surfaces |

All three `*_green.png` video masters are **on hold**: their green is `#24BC57`, not canonical `#238343`.
Request corrected source exports; do not patch them by recolouring. Video masters are tightly cropped around
the artwork, so the layout must supply clear space. Use the supplied green PNG on light surfaces and approved
white PNG on dark surfaces, preserving proportions and symbol-to-wordmark scale. A green logo is an identity
exception to the single-bright-accent rule, not permission to add green decoration.

For a deck with the theme copied into `brand/`:

```html
<img class="sa-chrome-logo" src="brand/logos/private/logo%20horizontal.png" alt="Superlinear Academy">
```

Ignore `brand/logos/private/` and private render paths in the destination repository **before** copying the theme.
For a copied skill install, ignore its local `theme/logos/private/` path as well. Keep `<img>` sources local for
offline rendering; use one logo per frame, with padding outside the artwork. Do not stretch, filter, shadow or
rebuild the mark. Never shrink a wordmark lockup into a small avatar; use a mark-only asset instead.

## Historical public assets

| File | Official asset | Use |
|---|---|---|
| `primary-black.svg` | Primary_Black_NoBgd | Full lockup with its clear space built into the file (1440×500 canvas). Closing slides, centred placements |
| `primary-white.svg` | Primary_White_NoBgd | The same on a dark background |
| `primary-black-compact.svg` | Primary_Black_NoBgd_Compact | Tight crop (2400×580). Running headers, promo headers: anywhere you set the clear space yourself |
| `primary-white-compact.svg` | Primary_White_NoBgd_Compact | The same on a dark background |
| `icon-black.svg` / `icon-white.svg` | Icon_Black_NoBgd / Icon_White_NoBgd | The mark alone, square canvas with clear space. Avatars, tiny spaces |
| `favicon.svg` | Favicon | Below 50 px only: browser tabs |

## Choosing historical assets

1. **Brand level.** Superlinear Academy by default. The sub-brand **Superlinear AI** only when the piece promotes an
   AI course or the AI community specifically; its files are not bundled, so ask for them rather than improvising.
2. **Background.** Light background → black logo. Dark background (`--sa-forest`, `--sa-primary-dark`, a dark photo)
   → white logo. Nothing else.
3. **Space.** Wide and short (running header, promo header) → compact lockup. Centred with room → full lockup.
   Square → icon.

## Historical size and clear space

- Minimum digital size of the full primary lockup: **144×50 px** (its whole canvas, which includes clear space).
  That corresponds to a compact lockup about **30 px tall**. The theme uses 34 px in slide headers and 36–40 px on
  promos.
- **Clear space:** the full files carry it. With the compact file, keep at least **0.4 × the logo height** of empty
  space on every side (the proportion the full file uses). In the slide header the running text starts 176 px from
  the page margin for that reason.
- Favicon under 50 px; never shrink the full lockup that far.

## Historical palette and shared don'ts (from the brand manual)

- Do not stretch or squash: set only `height` (or only `width`), never both.
- Do not add shadows, glows, gradients, outlines or CSS filters.
- Do not recolour. In particular, do not tint the logo or the mark brand green with a CSS mask or `fill` override:
  the historical SVG colours are black, white and (retired) blue. Current supplied green PNGs are a separate identity,
  not a recoloured legacy mark.
- Do not scale the symbol and the wordmark separately, or rebuild the wordmark in a font.
- Do not use outline / stroke-only versions.
- Do not crowd it: no text or rule inside the clear space.
- When a long line of text would force the lockup wider, change the layout, not the logo.

## Historical implementation

Always an `<img>` of the file: `<img class="sa-chrome-logo" src="brand/logos/primary-black-compact.svg"
alt="Superlinear Academy">`. Do not use `mask-image` / `-webkit-mask` with a local file: under `file://` the mask
fails to load in Chromium and the logo disappears, and a mask is a recolouring tool anyway. Show the logo once per
frame: in the running header for slides, top-left on promos.

## Co-branding

Partner and sponsor marks need a visible separator rule between the Superlinear Academy logo and the partner mark.
Separator thickness scales with the lockup: `α = H / H_min`, thickness `= α × 1 px` (1 px at minimum size). Align
the two marks on their optical centres and give them equal visual weight.
