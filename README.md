# Superlinear Academy brand skill

An agent skill that lets any AI coding agent produce on-brand Superlinear Academy visuals: slide decks, promo
images, event covers and link-preview cards. It packages the brand's design tokens, vendored fonts, official logo
files, a slide theme, a library of 18 slide layouts (including video, tables, horizontal bars and a missing-asset
placeholder), a typesetting helper, three promo templates, and a script that renders HTML to PNG and audits the result.

The look is a "monochrome editorial" register: pale sage paper, near-black ink, the brand green `#238343` as the
only bright colour, a restrained oxblood second colour, Fraunces serif display type with Outfit labels, hairline
structure, no shadows.

| Slides (canvas deck) | 16:9 promo | Event cover 2.8:1 |
|---|---|---|
| ![contact sheet](examples/shipping_small_models/screenshots/contact_sheet.jpg) | ![promo](examples/promo/screenshots/promo_16x9.png) | ![cover](examples/promo/screenshots/event_cover_2_8.png) |

## What is inside

```
skills/superlinear-brand/      the skill (install this folder)
  SKILL.md                     root skill: workflow, hard rules, index of references
  references/                  tokens & type, logo usage, slide theme, layouts, promo formats, pitfalls, verification
  theme/                       tokens.css, layouts.css, canvas.css, promo.css, typeset.js, fonts/, logos/, placeholders/
  templates/                   promo_16x9.html, event_cover_2_8.html, og_1200x630.html
  scripts/render.py            HTML -> PNG with an offline / overflow / wrap / safe-area / SVG-label / typography audit
examples/
  shipping_small_models/       18-slide presentation-skill canvas deck, one slide per layout, screenshots
  promo/                       rendered templates + a Chinese 16:9 example
docs/                          prd.md, rfc.md, working.md
```

## Install as a skill

Give your agent this repository (<https://github.com/grapeot/superlinear-brand-skill>, branch `master`) and ask it
to install the skill:

```text
Install the skill from https://github.com/grapeot/superlinear-brand-skill into my workspace. Copy or link skills/superlinear-brand/ into my skills
directory (for Claude Code: ~/.claude/skills/superlinear-brand/ or .claude/skills/superlinear-brand/ in a project),
or register skills/superlinear-brand/SKILL.md in my workspace's skill index. Expose exactly one root skill.
```

The public theme, fonts, historical logos, templates and script all live under
`skills/superlinear-brand/`. For slides it composes with the presentation skill
(<https://github.com/grapeot/presentation_skill>): that skill provides the HTML canvas deck engine and workflow, this
one provides the visual layer.

## Getting started: internal logo assets

Current production work uses the official **six-layer** identity pack. This pack is internal-only, is not
publicly distributed, and is not MIT-licensed. Obtain it through authorized internal team channels; do not
include the pack or its access links in public pull requests.

The bundled SVGs are historical **eight-layer** marks previously authorized for public distribution. They remain
available for archival work and public sample templates. The screenshots above demonstrate layouts, not the
current identity. Do not mix the two generations in a deliverable.

Keep original downloads under `.local/drive/logo/` (ignored) or outside the repository. Copy the pack, retaining
its original filenames and hierarchy, into the ignored local asset folder:

```bash
mkdir -p skills/superlinear-brand/theme/logos/private
cp -R /path/to/internal-logo-pack/. skills/superlinear-brand/theme/logos/private/
git check-ignore skills/superlinear-brand/theme/logos/private/README.md
```

This repository ignores both `.local/` and `skills/superlinear-brand/theme/logos/private/`. A copied skill install
must add its corresponding private asset path to the destination repository's `.gitignore`; a symlinked install
keeps assets in the owning repository.

Before copying `theme/` into a deck as `brand/`, add `brand/logos/private/` and private render/export paths to that
project's `.gitignore`. Then replace the default logo `<img>` source with
`brand/logos/private/logo%20horizontal.png`, preserving proportions and alt text. For promos, adjust the source
relative to the copied theme location. Use the approved white master on dark backgrounds.

See [logo usage](skills/superlinear-brand/references/logo_usage.md) for the file selection table and the green
video masters that remain on hold. Do not publish the source pack or commit renders embedding its artwork to a
public repository. If the pack is absent, request it from the team or use an explicit placeholder; do not fabricate
the logo or silently fall back to the historical identity.

## Quick start

```bash
uv venv .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python -m playwright install chromium        # or rely on an installed Google Chrome

# render the promo templates
.venv/bin/python skills/superlinear-brand/scripts/render.py page \
  skills/superlinear-brand/templates/*.html --out-dir out/

# render every slide of the example deck + contact sheet
.venv/bin/python skills/superlinear-brand/scripts/render.py deck examples/shipping_small_models
```

The script exits non-zero if a page makes an external request, logs a console error, fails to load a font or image,
lets text leave the canvas or the safe area, wraps a title past its `data-max-lines`, splits a number from its unit,
lets SVG labels overlap or run out of their boxes, crops a headshot or recording, or (with `--final`) still contains
a placeholder or stand-in text. It warns about straight quotes and scaffold class-name collisions. Requests to the
network are blocked during a render. Exit code 2 (with `{"error": …}`) means the render could not run at all.

To use the theme in a new deck, scaffold an HTML canvas deck with the presentation skill, copy
`skills/superlinear-brand/theme/` into it as `brand/`, and follow
[references/slide_theme.md](skills/superlinear-brand/references/slide_theme.md) (including the one-line server patch
for the scaffold's `tools/shoot.py`). In this repository the example deck's `brand/` is a symlink to the skill's
`theme/`; on a system without symlink support, copy the folder instead.

## Licence

Code and documentation: MIT ([LICENSE](LICENSE)). The Superlinear Academy logos and marks are trademarks provided for
on-brand use only and are not MIT-licensed ([TRADEMARKS.md](skills/superlinear-brand/theme/logos/TRADEMARKS.md)).
Bundled fonts keep their SIL Open Font License ([OFL.txt](skills/superlinear-brand/theme/fonts/OFL.txt)). The
example deck vendors Reveal.js (MIT).
