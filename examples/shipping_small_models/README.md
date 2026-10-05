# Example deck: "Shipping small models"

A made-up 13-slide talk that shows every layout of the Superlinear Academy brand theme inside a presentation-skill
HTML canvas deck. The content is placeholder: the speaker, figures and course details are illustrative.

| File | Source |
|---|---|
| `index.html` | Hand-written frames (one per layout) between `FRAMES:BEGIN` / `FRAMES:END`; brand chrome in `#chrome` |
| `js/engine.js`, `css/deck.css` | The presentation skill's canvas scaffold (MIT), unmodified except the font block |
| `js/deck.js`, `js/copy.js` | Slide table and speaker notes |
| `vendor/reveal/` | Reveal.js 5 (MIT, `vendor/reveal/LICENSE`) |
| Theme | `../../skills/superlinear-brand/theme/` (in a real deck, copy it in as `brand/`) |
| `screenshots/` | Every slide at its last step and `contact_sheet.jpg`, produced by `render.py deck` |

## View

The deck links the theme two levels up, so serve the repository root:

```bash
python3 -m http.server 8765 --bind 127.0.0.1      # from the repository root
# open http://127.0.0.1:8765/examples/shipping_small_models/
```

Arrow keys or space to step, S for the speaker view, M for the slide navigator.

## Re-render the screenshots

```bash
.venv/bin/python skills/superlinear-brand/scripts/render.py deck examples/shipping_small_models
```
