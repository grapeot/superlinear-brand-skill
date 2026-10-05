# Pitfalls

| Trap | How it shows up | Do this |
|---|---|---|
| Web fonts from a CDN | `fonts.googleapis.com` in a `<link>`; the render works online, fails offline or in CI, and leaks a request | Use `tokens.css` only (vendored WOFF2). `render.py` fails on any external request |
| Subset fonts and CJK | Chinese renders in a random system face, or tofu boxes, because the Latin-subset web font has no CJK glyphs and the stack ends in a bare `serif` | Use the token stacks (CJK families listed after the Latin face) and `.sa-zh` on Chinese elements |
| Negative tracking on Chinese | CJK glyphs touch or overlap in a headline | `.sa-zh` resets letter-spacing to slightly positive |
| Logo through `mask-image` | Logo invisible when the page is opened from `file://` (Chromium blocks the local mask); or the logo got recoloured green | Always `<img src="…/logos/*.svg">`; never recolour |
| Full logo file in a tight header | The logo looks tiny: the full SVG includes clear space (about 40% padding) | Use `primary-black-compact.svg` in headers; the full file where it stands alone |
| Title wraps on the real render | A long title, sized by guess, breaks into three lines or orphans one word; CJK titles wrap at different points than expected | Put `data-max-lines` on titles; size against the real container; shorten words first; re-render |
| Wide cover cropped | Logo or speaker name cut off on the event page; buttons drawn over the date | Keep everything in the 220/60 px safe area (`sa:safe` meta, audited) |
| Cropped headshot | `object-fit: cover` cuts the chin or hair; circle masks cut shoulders | `img.sa-uncropped` (contain) in a square hairline frame; get a square original |
| Course-site palette mistaken for the brand | Light green `#79d287`, coral, sticky-note cards appear in a brand piece | That is a course website's palette. Brand = `#238343` + editorial neutrals |
| Retired blue accents | Azure / Maya blue from the April 2026 manual | Superseded by the green. Do not use |
| Green small text too light | `#238343` at 15 px fails contrast (4.2:1) | `--sa-green-text` `#22683b` under 24 px |
| Grey as the second colour | The rejected option reads as disabled, the punchline disappears | Oxblood `--sa-second` with one meaning |
| Shadows and gradients creep back | Cards with drop shadows, gradient backgrounds, glow on the logo | Flat cards with hairlines; hatching for shading. `canvas.css` removes scaffold shadows |
| Class collision with the scaffold | A bordered box appears around a line of text (a `.role` element picked up the scaffold's role card) | Avoid the scaffold's global class names inside layouts (list in [slide_theme.md](slide_theme.md)) |
| Decorative filler | An icon grid or stock illustration fills empty space | Empty space is fine. Add a figure only if it explains something |
| Placeholder text shipped | "Speaker Name", "Month DD" or the placeholder silhouette in a published image | Search the HTML for `Speaker Name`, `Month DD`, `headshot.svg`, `EDIT` before rendering the final |
| Invented facts | A date, price, statistic or quote filled in to make the template look complete | Leave the row or line out until there is a source |
| Sub-brand misuse | "Superlinear AI" mark on a general community promo | Parent brand by default; sub-brand only for AI course / AI community promotions |
| Judging from the code | The HTML "looks right" but the PNG has a clipped descender or an overlap | Always open the rendered PNG at full size; the audit catches geometry, not taste |
| Server resets during deck render | Random `ERR_CONNECTION_RESET` on one stylesheet | `render.py deck` uses a deep listen backlog; if you serve a deck yourself, do the same or use the presentation skill's `start-server.py` |
