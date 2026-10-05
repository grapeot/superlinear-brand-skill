# Layout catalogue

Thirteen layouts in `theme/layouts.css`. Each lives in a `.sa-pad` box (content area x 160–1760, y 140–950 of a
1920×1080 frame) inside a canvas `.frame` or a plain `<section class="sa-slide">`. Full working markup for every
one is in `examples/shipping_small_models/index.html`; screenshots are in
`examples/shipping_small_models/screenshots/` (file names below) with a contact sheet at `contact_sheet.jpg`.

Shared primitives: `.sa-kicker` (letter-spaced label with the green rule; `.no-rule` to drop it), `.sa-display` +
`.sa-h1/.sa-h2/.sa-h3`, `.sa-lede`, `.sa-read` (serif reading text), `.sa-small`, `.sa-source`, `.sa-em` (green, ≥ 24 px),
`.sa-em-text` (green, small), `.sa-em-2` (oxblood), `.sa-card` (+ `.keep` / `.drop`), `.sa-frame`, `img.sa-uncropped`,
`.sa-note`, `.sa-button`, `.sa-zh`.

Put `data-max-lines="N"` on every headline and lede: `scripts/render.py` fails if it wraps further.

## 01 Cover — `01_cover.png`
Talk title, promise, speaker and date, with a line illustration. One per deck.
```html
<div class="sa-pad sa-cover">
  <div class="text">
    <div class="sa-kicker">Occasion · Format</div>
    <h1 class="sa-display sa-h1" data-max-lines="2">Title</h1>
    <p class="sa-lede" data-max-lines="3">One-sentence promise</p>
    <div class="byline"><span class="who">Speaker · Role</span><span class="when">Date</span></div>
  </div>
  <div class="art"><svg viewBox="0 0 700 640">…line drawing…</svg></div>
</div>
```
The art column is 650 px wide. Use a textless line illustration or an engraving plate, never a photo collage.

## 02 Section opener — `02_part1.png`
Starts a part of the talk. A faint italic numeral sits behind the title (decorative, `aria-hidden`).
```html
<div class="sa-pad sa-section">
  <div class="sa-numeral" aria-hidden="true">II</div>
  <div class="sa-kicker">Part II</div>
  <h2 class="sa-display sa-h1" data-max-lines="2">What this part argues</h2>
  <p class="sa-lede" data-max-lines="2">Why it matters, in one line</p>
  <div class="marker"></div>
</div>
```

## 03 One-claim headline — `03_claim.png`
The default slide: one claim set large, with one supporting line. Use `.sa-em` on the phrase that carries the claim.
```html
<div class="sa-pad sa-claim">
  <div class="sa-kicker">The claim</div>
  <h2 class="sa-display sa-h1" data-max-lines="3">A claim with <span class="sa-em">the key phrase</span></h2>
  <div class="support"><p class="sa-lede">Support</p><span class="sa-source">Source</span></div>
</div>
```
Three lines of h1 (96 px) is the ceiling; past that, shorten the claim.

## 04 Two-column compare — `04_compare.png`
Recommended vs rejected. Green inset bar on the side you recommend, oxblood hatching on the other.
```html
<div class="sa-pad sa-compare">
  <div class="sa-kicker">What is being compared</div>
  <div class="cols">
    <div class="sa-card keep"><div class="sa-tag">Label</div><div class="name">Option A</div><p class="sa-read">…</p><div class="sa-small">…</div></div>
    <div class="sa-card drop"><div class="sa-tag">Label</div><div class="name">Option B</div><p class="sa-read">…</p><div class="sa-small">…</div></div>
  </div>
  <p class="sa-display conclusion" data-max-lines="1">What to do</p>
</div>
```
For a neutral comparison (no winner), use two plain `.sa-card`s.

## 05 Numbered steps — `05_recipe.png`
A procedure or ordered list, 3–5 items, mono numbers, hairline separators. `li.now` marks the current step with green.
```html
<div class="sa-pad sa-steps">
  <div class="head"><div class="sa-kicker">The recipe</div><h2 class="sa-display sa-h2">Headline</h2></div>
  <ol><li class="now"><span class="n">01</span><span class="t">Step</span><span class="d">Detail</span></li>…</ol>
</div>
```

## 06 Big-number stat — `06_latency.png`
One number that carries the slide, in green Fraunces Light, with its meaning and source to the right.
```html
<div class="sa-pad sa-stat">
  <div class="big">40<span class="unit">ms</span></div>
  <div class="side"><div class="sa-kicker no-rule">What was measured</div><h2 class="sa-display sa-h3">So what</h2>
    <p class="sa-lede">Context</p><div class="sa-source">Source</div></div>
</div>
```
Up to four characters at 330 px. Fraunces figures have ball terminals (the 4 has a teardrop); that is the face.

## 07 Chart (inline SVG) — `07_accuracy.png`
Bars, lines or dots drawn as inline SVG with real `<text>`. Only the series the slide is about is green; the rest are
hairline outlines on card fill. Gridlines in `--sa-rule`, axis in ink. Values in Fraunces, ticks in mono.
```html
<div class="sa-pad sa-chart">
  <div><div class="sa-kicker">What is plotted</div><h2 class="sa-display sa-h2">The finding as a sentence</h2></div>
  <div class="plot"><svg viewBox="0 0 1600 560">
    <line class="grid" …/><rect class="bar" …/><rect class="bar hi" …/><text class="value hi" …>88.4</text>
    <line class="axis" …/><text class="cat" …>Category</text><text class="callout" …>Annotation</text>
  </svg></div>
  <div class="sa-source">Source line, from the first step</div>
</div>
```
Classes: `.grid .axis .bar .bar.hi .bar.ghost .value .value.hi .cat .callout .callout-line`. One unit = one pixel at
1080p, so text sizes obey the same minimums. Give the SVG an `aria-label` that states the data.

## 08 Quote — `08_rule.png`
A sentence worth quoting, green left rule, attribution in sans plus source in mono, an optional gloss.
```html
<div class="sa-pad sa-quote">
  <blockquote><div class="q" data-max-lines="3">Quote without quotation marks (CSS adds them)</div>
    <div class="who">Name<span class="sa-source">Context</span></div></blockquote>
  <p class="sa-lede gloss">Why it matters</p>
</div>
```
Only quote real, attributable words. A working rule of your own is labelled as such.

## 09 Image / plate with caption — `09_distil.png`
A figure in a hairline frame with a mono figure number and an italic caption; the explanation sits beside it.
```html
<div class="sa-pad sa-figure">
  <figure><div class="sa-frame"><svg>…</svg> or <img class="sa-plate-img" src="…"></div>
    <figcaption><span class="fig">Fig. 1</span><span class="cap">Caption</span></figcaption></figure>
  <div class="text"><div class="sa-kicker">…</div><h2 class="sa-display sa-h2">…</h2><p class="sa-lede">…</p></div>
</div>
```
Plates are textless (labels go in the caption or in DOM), grey ink (`.sa-plate-img`), never behind text being read.
Screenshots of software go in the same frame, unfiltered.

## 10 Timeline — `10_plan.png`
Phases or dates left to right; past ticks are grey rings, the current one is a solid green dot. Set `--n` to the
number of ticks (3–5).
```html
<div class="sa-pad sa-timeline">
  <div><div class="sa-kicker">…</div><h2 class="sa-display sa-h2">…</h2></div>
  <div class="track" style="--n:4"><div class="tick past"><div class="when">Week 1</div><div class="what">…</div><div class="why">…</div></div>…<div class="tick now">…</div></div>
</div>
```

## 11 Speaker bio — `11_speaker.png`
Square headshot, shown whole, in a hairline frame; name, role, three facts, a link.
```html
<div class="sa-pad sa-bio">
  <div class="photo"><img class="sa-uncropped" src="headshot.jpg" alt="Name"></div>
  <div><div class="sa-kicker">About the speaker</div><h2 class="sa-display sa-h2">Name</h2><div class="position">Role · Org</div>
    <ul><li>Fact</li><li>Fact</li><li>Fact</li></ul><div class="links">site.example</div></div>
</div>
```
Use the person's own full square photo. If it is not square, it letterboxes on the card colour; do not switch to
`object-fit: cover`. Grayscale is optional and only with the person's consent to editing; never retouch.

## 12 CTA / course promo — `12_course.png`
The ask: what you get, one action. The `.sa-button` is the only solid green block in the system.
```html
<div class="sa-pad sa-cta">
  <div><div class="sa-kicker">Superlinear Academy course</div><h2 class="sa-display sa-h2">Course title</h2>
    <ul><li>Outcome</li><li>Outcome</li><li>Outcome</li></ul>
    <div class="action"><span class="sa-button">Join the course</span><span class="url">superlinear.academy</span></div></div>
  <div class="sa-spec"><div class="row"><span class="k">Format</span><span class="v">…</span></div>…</div>
</div>
```
Outcomes are things the learner makes, not topics covered. Only state facts (dates, price, length) you have a source
for; otherwise leave the row out.

## 13 Q&A / closing — `13_close.png`
The last frame: an invitation, the full logo once, a contact line.
```html
<div class="sa-pad sa-close">
  <h2 class="sa-display sa-h1">Questions</h2><p class="sa-lede">Invitation</p>
  <img class="sa-logo" src="brand/logos/primary-black.svg" alt="Superlinear Academy"><div class="contact">superlinear.academy</div>
</div>
```

## Choosing

| You want to say | Layout |
|---|---|
| One thing | 03 claim (default) or 06 stat if it is a number |
| A versus B | 04 compare |
| How to do it | 05 steps |
| What the data shows | 07 chart |
| What it looks like / how it works | 09 figure |
| When | 10 timeline |
| Who said it / a rule | 08 quote |

Do not invent new decorative layouts (icon grids, three-card feature rows with icons, photo collages). If none fits,
compose from the primitives and keep one primary relationship per frame.
