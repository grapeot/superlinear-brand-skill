# Working log

## 2026-10-04 — v0.1

**Done**

- [x] Studied the sources: the approved slide theme of a reference canvas deck, the brand manual and token set, the
      logo set, a set of promo images and their lessons, and the presentation skill's HTML canvas mode.
- [x] `theme/tokens.css`: vendored fonts (Latin subsets with unicode-range), brand core + editorial tokens, CJK stacks.
- [x] `theme/canvas.css`: presentation-skill scaffold re-skin and chrome (logo, brand line, progress rule).
- [x] `theme/layouts.css`: type primitives + 13 layouts.
- [x] `theme/promo.css` + templates for 16:9, event cover 2.8:1, OG 1200×630.
- [x] `scripts/render.py`: page and deck modes, audits, contact sheet.
- [x] Example canvas deck (13 slides) and promo examples (including Chinese), rendered and inspected.
- [x] SKILL.md, seven references, README, LICENSE (MIT + trademark and OFL carve-outs), PRD, RFC.

**Verification (final run)**

- `render.py deck examples/shipping_small_models`: 13 slides, exit 0; no console errors, failed or external requests,
  font errors, off-frame elements, wrap violations or unfilled slots. Fonts loaded: Fraunces normal + italic, Outfit,
  Inter, JetBrains Mono 400/500.
- `render.py page` on the three templates + `promo_16x9_zh.html`: exit 0; safe areas respected.
- Negative test: a page with a Google Fonts link, a missing image, a headshot pushed into the crop zone and an
  over-long title reported `external_requests`, `failed_requests`, `images`, `unsafe` and `wrapped`, exit 1.
- Every PNG inspected at full size.

**Fixed during the build**

- Scaffold class collision: the speaker's role line named `.role` picked up the scaffold's bordered role card →
  renamed inner classes (`.position`, `.conclusion`, `.sa-numeral`, `.cat`) and documented the collision list.
- The rolling counter in the stat layout inherited the scaffold's mono font → kept the serif inside `.sa-stat .big`.
- Deck render hit `ERR_CONNECTION_RESET` on one stylesheet (default listen backlog of 5) → server backlog raised.
- Cover illustration: projection lines crossed the boxes and a label → redrawn corner to corner, behind the boxes.
- Compare cards had a large empty middle → added a large serif name per card.
- Event cover kicker rule hung into the crop zone → inline rule on covers.
- Straight apostrophes in display text → typographic.

**Next**

- [ ] Owner confirmation that the logo SVGs may be redistributed in a public repository.
- [ ] Optional dark-stage theme and dark promo template, with contrast checks.
- [ ] Superlinear AI sub-brand assets and a sub-brand promo variant, if wanted.
- [ ] Run a fresh agent with only this skill on a real brief and fold its mistakes into `pitfalls.md`.
