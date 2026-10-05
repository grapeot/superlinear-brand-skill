# Brand tokens and typography

All values are CSS custom properties in `theme/tokens.css`. Use the variables, not the hex values, so a later
palette change lands everywhere.

## Two palettes, two jobs

Superlinear Academy has a **brand core** (the 2026 brand green and the token set of its web surfaces) and an
**editorial theme** derived from it for slides and images. Use the editorial theme for anything that is a picture:
slides, promo images, covers, OG cards. Use the web tokens only when you build web UI.

### Brand core

| Token | Value | Role |
|---|---|---|
| `--sa-green` | `#238343` | The brand colour. Shapes, rules, bars, buttons, text at 24 px and above |
| `--sa-green-text` | `#22683b` | Green text below 24 px: kickers, footer brand line, small labels |
| `--sa-green-hover` | `#1d7039` | Hover state on web surfaces |
| `--sa-forest` | `#183d27` | Dark green: a dark band or stage behind light text |
| `--sa-green-tint` | `#dcebdd` | Pale green fill, sparingly (a highlighted cell) |
| `--sa-green-wash` | `#f0f5ef` | Lightest green wash |
| `--sa-primary-dark` / `--sa-primary-light` | `#1e1e1e` / `#eeeeee` | The logo files' own ink colours |
| `--sa-web-bg` `--sa-web-surface` `--sa-web-ink` `--sa-web-muted` | `#eeede8` `#f9f8f4` `#18201d` `#545c57` | Web UI surfaces |

### Editorial theme (slides and images)

| Token | Value | Role |
|---|---|---|
| `--sa-paper` | `#eef0ec` | The page: pale sage, not white and not yellow paper |
| `--sa-paper-2` | `#e5e8e3` | A recessed band |
| `--sa-card` | `#f7f8f5` | Cards, photo and plate frames |
| `--sa-ink` | `#0b0b0b` | Headlines and body |
| `--sa-ink-2` | `#363936` | Secondary text (ledes, captions) |
| `--sa-ink-3` | `#646864` | Labels, running header, source lines. The lightest colour allowed for text |
| `--sa-rule` | `#d3d7d0` | Hairlines (1 px) |
| `--sa-line` | `#0b0b0b` | Strong borders (1.5 px) on cards, axes, timelines |
| `--sa-second` | `#8f3a2e` | Oxblood: the restrained second colour |
| `--sa-hatch` | oxblood at 7.5% | Hatching fill for the "expiring" side |

**Meaning, not decoration.** Green marks the point of a frame or the side you recommend; oxblood marks the side you
reject or the thing that expires. Keep one meaning per colour for the whole deck. The slide chrome (running header,
footer brand line, progress rule) is neutral ink so that green never becomes wallpaper; the short kicker rule is the
only green that appears on every frame. A frame with no claim to mark has no other green. Someone else's number
(a competitor, a baseline) is never green, however prominent. Grey was tried as the second colour and read as disabled text; oxblood keeps the
punchline legible without competing with green.

**Retired:** the April 2026 manual's accents Azure `#0E6EF4` and Maya `#4B96FF` are superseded by the green. The
light-green, coral and sticky-note palette of the course website is that site's palette, not the brand.

### Contrast (WCAG 2.x, against `--sa-paper`)

| Foreground | Ratio | Allowed for |
|---|---|---|
| `--sa-ink` | 17.2 | anything |
| `--sa-ink-2` | 10.2 | anything |
| `--sa-ink-3` | 4.9 | small text (labels, sources) |
| `--sa-second` | 6.5 | anything |
| `--sa-green-text` `#22683b` | 5.9 | small green text |
| `--sa-green` `#238343` | 4.2 | text at 24 px+ (or 18.7 px bold) only, and non-text marks |
| white on `--sa-green` | 4.8 | button labels at 24 px+ semibold |
| `--sa-paper` on `--sa-forest` | 10.6 | light text on a dark green band |

Never put text in `#8b8f99` or lighter on the paper (2.8:1).

## Type

| Variable | Family | Use |
|---|---|---|
| `--sa-serif` | Fraunces (variable, optical sizing) | Display headlines, card bodies, quotes, list items: the reading voice |
| `--sa-label` | Outfit (variable) | Kickers, tags, running header and footer, button labels: letter-spaced uppercase |
| `--sa-sans` | Inter (variable, opsz) | Ledes, captions, dates, UI-like body text |
| `--sa-mono` | JetBrains Mono 400/500 | Numbers, folios, source lines, figure numbers, URLs |

Fraunces settings used throughout: `font-optical-sizing: auto; font-variation-settings: "SOFT" 30, "WONK" 0;`,
weight 400 for display (300 for very large numerals), letter-spacing −0.02 em to −0.025 em on headlines.
Kickers: Outfit 600, 18 px, letter-spacing 0.2 em, uppercase, `--sa-ink-3`, with a 24×3 px green rule hanging 38 px
to the left.

Sizes at 1080p: display 96–132 px (h1), 64 px (h2), 44 px (h3); reading text 26–40 px; nothing under 20 px except
source lines (17 px), the running header and footer (15–16 px) and kickers (15–18 px). The logo typeface (Albert
Sans) is baked into the logo files; it is not a text face for slides.

## CJK pairing and glyph coverage

The vendored WOFF2 files are **Latin subsets** (each `@font-face` declares a Latin `unicode-range`). Chinese
characters therefore fall through to the next family in the stack:

| Role | Latin | Simplified Chinese fallback chain |
|---|---|---|
| Serif display / reading | Fraunces | Noto Serif SC → Source Han Serif SC → Songti SC → STSong → SimSun |
| Labels | Outfit | PingFang SC → Source Han Sans SC → Noto Sans SC → Microsoft YaHei |
| Sans body | Inter | PingFang SC → Source Han Sans SC → Noto Sans SC → Microsoft YaHei |

Rules:

- **Never declare a font stack with only a web font and a generic family** (`"Fraunces", serif`). The generic
  fallback for CJK differs per machine and can be a mismatched face. Use the token stacks.
- **For mostly-Chinese elements, add `.sa-zh`.** It switches display text to `--sa-serif-zh` at weight 600 and
  relaxes the negative tracking (negative letter-spacing collides CJK glyphs). Latin words inside the Chinese line
  still get Fraunces through the unicode-range.
- **Chinese display sizes run ~20% smaller** than Latin for the same visual weight (CJK glyphs fill the em box):
  96 px Latin ≈ 76 px Chinese.
- **Chinese uppercase tracking:** labels in Chinese use `letter-spacing: .3em`, no `text-transform`.
- **Do not mix in bracketed translations** ("中文 (English)"). Bilingual promos put the two languages on separate
  lines with the primary language first.
- **The renderer's fonts are the machine's fonts.** CJK output depends on what is installed where you render. On
  macOS, Songti SC and PingFang SC are present; on Linux install `fonts-noto-cjk`. Render on the machine that
  produces the final PNG and look at it.
- **Brand slogan:** Chinese 做出你的代表作; the English brand line used in the footer is "Make what lasts."
