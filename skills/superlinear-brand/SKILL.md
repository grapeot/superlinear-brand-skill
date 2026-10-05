---
name: superlinear-brand
description: >-
  Visual brand layer for Superlinear Academy: tokens, fonts, logos, a slide theme for HTML canvas decks,
  a slide layout library, promo-image templates and a render-and-audit script. Use when making
  Superlinear Academy slides, an on-brand deck, anything "in the Superlinear Academy brand style",
  a promo image, a social or video title card, an event cover (2.8:1 community event header),
  an OG / link-preview image, or when choosing a Superlinear Academy logo, colour or font.
---

# Superlinear Academy brand skill

## Goal

Make every visual that carries the Superlinear Academy name look like it came from one publication: a printed
editorial page that happens to be on screen. Pale sage paper, near-black ink, one bright colour (brand green
`#238343`), a serif display face, hairline structure, no shadows, no gradients, no decoration that does not carry
meaning. An agent using this skill should produce on-brand output on the first render and prove it with the audit.

This skill owns the **visual layer**. It does not own the deck engine, the argument or the copy:

- **Slides:** the presentation skill (the `presentation_skill` package, root skill `skills/skill_presentation.md`,
  HTML canvas mode in `html_decks.md`) supplies the engine, the workflow and its acceptance criteria. This skill
  supplies the theme you drop into that deck. Read both.
- **Promo images, covers, OG cards:** this skill is complete on its own (templates + `scripts/render.py`).

## What is in the folder

| Path | What it is |
|---|---|
| `theme/tokens.css` | Fonts (`@font-face`, vendored) and every colour and type token. Load first, always |
| `theme/layouts.css` | Type primitives (`.sa-kicker`, `.sa-display`, `.sa-lede` …) and 13 slide layouts (`.sa-pad.sa-*`) |
| `theme/canvas.css` | Re-skins a presentation-skill canvas deck: scaffold tokens, running header with logo, footer brand line |
| `theme/promo.css` | Promo canvases: 16:9 (1920×1080), event cover 2.8:1 (2100×750), OG (1200×630) |
| `theme/fonts/` | Fraunces, Outfit, Inter, JetBrains Mono (Latin subsets, SIL OFL; `OFL.txt`) |
| `theme/logos/` | Official logo SVGs (trademarks, see `TRADEMARKS.md`) |
| `theme/placeholders/headshot.svg` | Neutral headshot stand-in |
| `templates/` | `promo_16x9.html`, `event_cover_2_8.html`, `og_1200x630.html` |
| `scripts/render.py` | Headless render to PNG + audit (`page` mode for promos, `deck` mode for canvas decks) |
| `references/` | The rules, one topic per file (below) |

A worked example lives in the repo, outside the skill: `examples/shipping_small_models/` (a 13-slide canvas deck,
one slide per layout, with screenshots and a contact sheet) and `examples/promo/` (all templates rendered, plus a
Chinese variant).

## Workflow

1. **Identify the output.** Deck → step 2. Promo / cover / OG → step 3. Logo or colour question only → answer from
   [references/logo_usage.md](references/logo_usage.md) or [references/brand_tokens.md](references/brand_tokens.md).
2. **Deck.** Scaffold with the presentation skill in HTML mode. Copy `theme/` into the deck as `brand/`, link
   `brand/tokens.css`, `brand/layouts.css`, `brand/canvas.css` after `css/deck.css`, and add the logo and brand line
   to `#chrome`. Build frames from the layout catalogue. Details: [references/slide_theme.md](references/slide_theme.md),
   [references/layouts.md](references/layouts.md).
3. **Promo image.** Copy the matching template, keep the theme paths valid, edit only the `EDIT` lines, swap in the
   real headshot (full square image). Details: [references/promo_formats.md](references/promo_formats.md).
4. **Render and audit.** `python scripts/render.py page <file.html>` or `python scripts/render.py deck <deck_dir>`.
   Exit code 0 is required, then **look at every PNG yourself**. Checklist:
   [references/verification.md](references/verification.md).
5. **Fix and re-render** until the audit is clean and the images pass the visual checklist. Known failure modes:
   [references/pitfalls.md](references/pitfalls.md).

Setup for the script (once): `uv venv .venv && uv pip install --python .venv/bin/python playwright pillow`
then `.venv/bin/python -m playwright install chromium` (it falls back to an installed Google Chrome).

## Hard rules

- **Brand green `#238343` is the only bright colour.** Use it for one thing per frame: the point, the recommended
  side, the highlighted bar, the kicker rule, the button. Green text under 24 px uses `#22683b` (contrast).
- **Oxblood `#8f3a2e` is the only second colour,** with one meaning per deck (the thing that expires, the
  anti-pattern). Never decorative. The April 2026 manual's blue accents (Azure, Maya) are retired.
- **Serif display (Fraunces), Outfit for labels, Inter for sans body, JetBrains Mono for numbers and sources.**
  Chinese falls through to Noto Serif SC / Songti SC (serif) and PingFang SC / Source Han Sans SC (sans).
- **Logos are `<img>` of the shipped SVG files.** Black on light, white on dark; never recoloured, stretched,
  outlined, shadowed or rebuilt in CSS; symbol and wordmark scale together; keep clear space.
- **No shadows, no gradients, no glows, no icon grids, no stock imagery.** Cards are flat with hairlines. Shading is
  hatching.
- **Headshots are never cropped.** Full square image in a hairline frame, `object-fit: contain`.
- **Everything renders offline.** Vendored fonts only; no Google Fonts, no CDNs. The audit fails on any external request.
- **Superlinear Academy is the default brand.** The sub-brand "Superlinear AI" is only for promotions of an AI
  course or the AI community; its logo files are not bundled here.

## References

| File | Covers |
|---|---|
| [brand_tokens.md](references/brand_tokens.md) | Colour roles, contrast, type families and sizes, CJK pairing and glyph coverage |
| [logo_usage.md](references/logo_usage.md) | Which logo file where, sizes, clear space, the don'ts, sub-brand and co-branding |
| [slide_theme.md](references/slide_theme.md) | Dropping the theme into a presentation-skill canvas deck; chrome; class collisions |
| [layouts.md](references/layouts.md) | The 13 layouts: when to use each, markup skeleton, screenshot |
| [promo_formats.md](references/promo_formats.md) | 16:9 promo, 2.8:1 event cover with safe area, OG card; copy rules for promos |
| [pitfalls.md](references/pitfalls.md) | Traps seen in practice and what to do |
| [verification.md](references/verification.md) | The render-and-look loop, audit output, visual checklist |
