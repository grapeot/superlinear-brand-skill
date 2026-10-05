# PRD: Superlinear Academy brand skill

## Problem

Superlinear Academy visuals are increasingly made by AI agents: lecture decks, promo images for live sessions,
event covers for the community platform, link-preview cards. Each agent session starts without the brand. The
result drifts in predictable ways: CDN fonts that break offline, a logo rebuilt from CSS or recoloured, the retired
blue accents of an older manual, a course website's palette mistaken for the brand, cropped headshots, titles that
wrap badly in the real render, wide covers whose edges the platform crops. The knowledge to avoid all of this exists
(a brand manual, a token set, one well-made reference deck, a handful of promo images and their lessons) but it is
scattered and partly private, so it is not available to an agent at the moment it needs it.

## Users

The primary users are **AI agents** producing Superlinear Academy visuals on behalf of a person: a coding agent
building a talk deck with the presentation skill, or an agent asked for "a promo image for Wednesday's session".
Secondary users are the people who review those visuals and want them right on the first render.

## Goals

1. An agent that loads the skill produces on-brand slides and promo images on the first attempt, without having seen
   any earlier Superlinear Academy material.
2. The brand is encoded as files the agent uses directly (CSS tokens, a theme, templates, logo files, fonts), not as
   prose it has to reinterpret.
3. Slides compose with the presentation skill's HTML canvas engine without changing that engine.
4. Every output can be verified mechanically (offline, no overflow, no unexpected wraps, safe areas, uncropped
   headshots) and the skill tells the agent what to look at by eye.
5. The repository is public and general: no private content, people, paths or IDs.

## Non-goals

- A deck engine, a writing workflow or argument design (the presentation skill owns those).
- Generating new logo variants, a new palette, or image-generation prompts for illustrations.
- The Superlinear AI sub-brand assets (rules are documented; files are not bundled).
- Print production (CMYK, PDF/EPS logos) and web UI component libraries.
- A dark theme (documented as a manual variant; no template yet).

## Requirements

- **Tokens:** brand core (green `#238343`, text green `#22683b`, forest, tints, web surface tokens) and the editorial
  theme (paper, card, three inks, rule, oxblood), with contrast guidance.
- **Typography:** Fraunces display/reading, Outfit labels, Inter sans body, JetBrains Mono numbers; vendored WOFF2
  with OFL; CJK fallback stacks (Noto Serif SC / Songti SC; PingFang SC / Source Han Sans SC) and rules for glyph
  coverage.
- **Logos:** official primary (black, white, compact) and icon SVGs, favicon; usage rules from the brand manual.
- **Slide theme:** a CSS layer for presentation-skill canvas decks (token mapping, chrome with logo and brand line,
  kicker rule, flat cards, plate treatment).
- **Layouts:** cover, section opener, one-claim headline, two-column compare, numbered steps, big-number stat,
  inline-SVG chart, quote, figure with caption, timeline, speaker bio with uncropped headshot, CTA / course promo,
  Q&A / closing.
- **Promo templates:** 16:9 (1920×1080), event cover 2.8:1 (2100×750) with safe area, OG (1200×630).
- **Render and audit:** one script for promo pages and canvas decks, with a contact sheet.
- **Reference implementation:** an example canvas deck (one slide per layout) and rendered promo examples,
  including a Chinese promo.

## Acceptance criteria

- `render.py page` on the three templates and the Chinese example, and `render.py deck` on the example deck, exit 0:
  zero console errors, zero failed or external requests, all fonts loaded, nothing off-canvas or outside safe areas,
  no `data-max-lines` violations.
- Every rendered image has been inspected at full size against `references/verification.md`.
- `SKILL.md` has frontmatter with triggers for slides, on-brand decks, brand style, promo images and event covers,
  and links every reference.
- The tree contains no personal names, emails, private paths, internal IDs or lecture content from the sources.
- The logos are documented as trademarks outside the MIT licence; fonts ship with their OFL text.
