# Working log

## 2026-10-06 — internal current-identity setup

- Documented local workflow and ignore rules for the internal six-layer logo pack under
  `skills/superlinear-brand/theme/logos/private/`; `.local/` holds original downloads.
- Clarified licensing boundaries and preserved historical eight-layer SVGs for archives and public samples.
- Added current asset selection to `logo_usage.md`, including App, social, splash and video masters.
- Green video masters remain on hold (`#24BC57` instead of `#238343`); use approved white masters on dark surfaces
  and request corrected green source exports rather than recolouring.
- Root skill supports supplied PNG/SVG assets and prohibits mixing current and historical marks.

## 2026-10-04 — v0.1

**Done**

- [x] Studied the sources: the approved slide theme of a reference canvas deck, the brand manual and token set, the
      logo set, a set of promo images and their lessons, and the presentation skill's HTML canvas mode.
- [x] `theme/tokens.css`: vendored fonts (Latin subsets with unicode-range), brand core + editorial tokens, CJK stacks.
- [x] `theme/canvas.css`: presentation-skill scaffold re-skin and chrome (logo, brand line, progress rule).
- [x] `theme/layouts.css`: type primitives + 13 layouts (18 since v0.2).
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

- [x] Owner confirmation that the logo SVGs may be redistributed in a public repository (confirmed for v0.2).
- [ ] Optional dark-stage theme and dark promo template, with contrast checks.
- [ ] Superlinear AI sub-brand assets and a sub-brand promo variant, if wanted.
- [ ] Run a fresh agent with only this skill on a real brief and fold its mistakes into `pitfalls.md`.

## 2026-10-04 — v0.2: fixes from a real 20-slide deck built with the skill

A fresh agent built a real deck using only this skill and the presentation skill, and logged friction points; an
independent critic reviewed the deck. Changes, by finding:

- [x] **`shoot.py` connection resets (high).** `slide_theme.md` step 7 now gives the exact `tools/shoot.py` patch
      (`request_queue_size = 128`), explains why the theme triggers it, and offers `render.py deck --all-steps` as an
      alternative; pitfalls row rewritten. (Upstream fix in the presentation skill's scaffold suggested, not made here.)
- [x] **Audit blind inside SVG (high).** `render.py` now checks SVG `<text>` against the SVG box
      (`svg_text_outside`), against the rect its centre sits in (`svg_text_overflow`) and against other text
      (`svg_text_overlap`); `data-audit-skip` exempts deliberate overlaps. Limits documented in `verification.md`.
      Negative-tested with a label running out of its box, "250"+"requests" touching, and a label past the SVG edge.
- [x] **Emphasis through copy slots (high).** New `theme/typeset.js`: `==phrase==` in slot copy becomes `.sa-em`;
      loaded between `copy.js` and `engine.js`. The example's claim slide is now slotted. Leftover markers fail the audit.
- [x] **Typography automation (medium).** `typeset.js` makes quotes typographic and joins number+unit with U+00A0;
      `render.py` warns on straight quotes and breakable number+unit spaces and fails on an actual break.
- [x] **Missing layouts (medium).** Added media (video in `.sa-frame`, `.tight`, `.dark`, `video.sa-uncropped`,
      poster rules), media pair, table, horizontal bars with a side note, chart takeaway row, and `.sa-placeholder`
      (listed as a warning; `--final` fails on it). Five new example slides with synthetic footage.
- [x] **Cover title capacity (medium).** Measured characters per line; `.sa-cover.long` (80 px, 3 lines, verified up
      to 64 characters); table in `layouts.md`; promo capacities re-measured.
- [x] **Brand-default contradictions (medium).** Chrome neutral (brand line and progress rule in ink-2, overridable);
      `.sa-stat .big` ink by default with `.accent` for your own number; `.sa-frame.tight.dark` for dark media; the
      navigator button styled and hidden in captures; green budget written down in `layouts.md`, `verification.md`,
      `brand_tokens.md`, `promo_formats.md`.
- [x] **Small items.** Font de-duplication step in `slide_theme.md`; `render.py deck` serves the deck directory by
      default and writes to `<deck>/verification/brand/`; class-collision list split into dangerous globals vs safe
      scoped names, plus a `scaffold_class` audit warning (it caught a real `.note` collision while building the new
      pair layout); content box aligned to y 130–950; running header vs kicker guidance; the example now uses `brand/`
      exactly like the documented install (symlink in this repo).
- [x] Presentation skill URL added (README, SKILL.md, references); LICENSE copyright line kept as edited by the owner;
      logo publication confirmed by the owner.

**Verification (v0.2 final run)**

- `render.py deck examples/shipping_small_models --out …/screenshots`: 18 slides, exit 0; no problems; the only
  warning is the deliberate placeholder. `--final`: exit 1 (placeholder), as intended. `--all-steps`: 31 captures, exit 0.
- `render.py page` on the three templates and the Chinese promo: exit 0, no problems, no warnings.
- Negative tests: SVG overflow / overlap / outside, visible `==`, video without poster, placeholder with `--final`,
  straight quotes and number+unit spaces (warnings), and a "115 / ms" break across 21 column widths (flagged exactly
  on the 16 widths where it breaks).
- Every slide and promo PNG inspected at full size or on the contact sheet.

## 2026-10-05 — v0.3: code-review fixes before publishing

Public home: https://github.com/grapeot/superlinear-brand-skill (branch `master`).

- [x] **`--final` and template stand-ins.** `--final` now fails on `.sa-placeholder` (box or marker), on any
      `<img>`/`<video>` from a `placeholders/` folder, and on visible stand-in text (Speaker Name, Month DD, 讲者姓名,
      某月某日). The box styling moved to `div.sa-placeholder`, so the class is a plain marker elsewhere. The templates
      mark their example title, date, name and photo. Verified: all three untouched templates exit 1 with `--final`
      and 0 without.
- [x] **Paths.** `SKILL.md` states that `theme/`, `templates/`, `scripts/`, `references/` are relative to the skill
      directory; every command uses `<skill_dir>/scripts/render.py`; the bogus `brand-skill/` path is gone.
- [x] **Upstream notices.** The example's `js/engine.js` and `css/deck.css` carry the presentation skill's copyright
      and MIT notice; LICENSE lists them as item 4.
- [x] **Meta parsing** via the DOM after load; unparseable or unknown `sa:` metas are a `meta` problem.
- [x] **Frame lookup** by `getElementById` (verified with a frame id that starts with a digit).
- [x] **typeset.js emphasis** works on text nodes (keeps child markup), regex `==(\S(?:[^=]*?\S)?)==` leaves
      `a == b` alone, honours `data-no-typeset`, skips code/pre/kbd/samp; `[data-typeset]`, quote limits ('90s) and
      unit extension documented; `SA_TYPESET_UNITS` now extends the defaults.
- [x] **External requests are aborted** during renders (still recorded).
- [x] **Docs without the repo:** example links point to the GitHub tree; `slide_theme.md` has a complete minimal
      `index.html` skeleton (rendered clean in a scratch deck before committing).
- [x] **Exit code 2** with `{"error": …}` for setup failures (missing page, deck dir missing or outside `--root`, no
      `index.html`, not a canvas deck, Chromium missing); the server is shut down and closed in `finally`.
- [x] Nice-to-haves: HTTP ≥ 400 recorded in `failed_requests`; aborted media range requests and broken pipes from a
      video reset are not reported; directory listing disabled; `steps`/`print` validated (`slide_table`);
      `.gitignore` gains `out/` and `**/verification/`; template comments render to `--out-dir out/`; literal NBSPs
      replaced by ` ` escapes; `.sa-zh` without `!important`; layouts.css capacity comment matches layouts.md;
      `make_media.py` deletes its frame folders and documents the libvpx-vp9 dependency.

**Verification (v0.3)**

- Example deck: exit 0, no problems; warnings only for the deliberate stand-ins (cover and speaker text, the offline
  placeholder). `--final`: exit 1. `--all-steps`: exit 0, no server noise.
- Promos (3 templates + Chinese example): exit 0; templates with `--final`: exit 1.
- Negative suite: SVG outside / overflow / overlap, `==` leftovers, video without poster, placeholders, straight
  quotes and unit spaces (warnings), number+unit break (16 of 21 widths, the ones that break), bad `sa:safe` meta,
  blocked Google Fonts request, HTTP 404, out-of-range `print`, digit-leading frame id, exit 2 for a missing page /
  bad `--root` / missing deck dir / non-deck page.
- Contact sheet and promo renders inspected; no visual change apart from the Chinese footer slogan's tracking, which
  now follows its inline style.
