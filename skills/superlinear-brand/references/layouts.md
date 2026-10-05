# Layout catalogue

Eighteen layouts and patterns in `theme/layouts.css`. Each lives in a `.sa-pad` box (content area x 160–1760,
y 130–950 of a 1920×1080 frame, the presentation skill's content box) inside a canvas `.frame` or a plain `<section class="sa-slide">`. Full working markup for every
one is in the example deck's [`index.html`](https://github.com/grapeot/superlinear-brand-skill/blob/master/examples/shipping_small_models/index.html) (in the source repository,
not in a skill-only install); screenshots are in [`screenshots/`](https://github.com/grapeot/superlinear-brand-skill/tree/master/examples/shipping_small_models/screenshots) (file names
below) with a contact sheet at `contact_sheet.jpg`. The skeletons below are complete enough to build from without it.

Shared primitives: `.sa-kicker` (letter-spaced label with the green rule; `.no-rule` to drop it), `.sa-display` +
`.sa-h1/.sa-h2/.sa-h3`, `.sa-lede`, `.sa-read` (serif reading text), `.sa-small`, `.sa-source`, `.sa-em` (green, ≥ 24 px),
`.sa-em-text` (green, small), `.sa-em-2` (oxblood), `.sa-card` (+ `.keep` / `.drop`), `.sa-frame` (+ `.tight`, `.dark`),
`img.sa-uncropped` / `video.sa-uncropped`, `.sa-placeholder`, `.sa-note`, `.sa-button`, `.sa-zh`.

Put `data-max-lines="N"` on every headline and lede: `<skill_dir>/scripts/render.py` fails if it wraps further.

**Green budget.** Structural marks are fixed and do not count: the kicker rule, bullet dashes in the CTA list, the
timeline's current dot, the recommended table column's header rule. Beyond those, a frame gets **one** green
emphasis: the claim's key phrase, the recommended card, your own number or bar, or the button. Someone else's number
(a competitor, a baseline, a hosted model) stays ink, even when it is the biggest thing on the slide.

**Copy slots.** Any text element can be filled from the writer's copy with `data-slot`; for green emphasis inside a
slotted headline use `==phrase==` in the copy and load `brand/typeset.js` ([slide_theme.md](slide_theme.md), "Copy
slots"). Layout 03 below is slotted in the example deck.

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

**Title capacity** (measured, Fraunces in the 860 px column; word breaks cost about 15%):

| Title length | Use | Size | Lines |
|---|---|---|---|
| up to ~36 characters | `.sa-cover` | 104 px (≈ 22 characters per line at best) | `data-max-lines="2"` |
| ~37–65 characters | `.sa-cover.long` | 80 px (≈ 27 per line at best) | `data-max-lines="3"` |
| over ~65 characters | shorten the title; move the rest to the lede | | |
| Chinese (`.sa-zh` on the h1) | `.sa-cover` | 104 px ≈ 8 characters per line; `.long` ≈ 11 | 2 or 3 |

Do not shrink below 80 px on a cover: the title stops reading as a title. Put subtitles and qualifiers in the lede,
not the h1.

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
The default slide: one claim set large, with one supporting line. Green on the phrase that carries the claim.
```html
<div class="sa-pad sa-claim">
  <div class="sa-kicker">The claim</div>
  <h2 class="sa-display sa-h1" data-max-lines="3">A claim with <span class="sa-em">the key phrase</span></h2>
  <!-- or, from the writer's copy: <h2 class="sa-display sa-h1" data-slot="claim.headline"></h2>
       with  headline: "A claim with ==the key phrase=="  in js/copy.js and brand/typeset.js loaded -->
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

## 05 Numbered steps — `06_recipe.png`
A procedure or ordered list, 3–5 items, mono numbers, hairline separators. `li.now` marks the current step with green.
```html
<div class="sa-pad sa-steps">
  <div class="head"><div class="sa-kicker">The recipe</div><h2 class="sa-display sa-h2">Headline</h2></div>
  <ol><li class="now"><span class="n">01</span><span class="t">Step</span><span class="d">Detail</span></li>…</ol>
</div>
```

## 06 Big-number stat — `07_latency.png`
One number that carries the slide, in Fraunces Light, with its meaning and source to the right. The number is ink by
default; add `.accent` to make it green only when it is your own result (the point of the talk). A competitor's or a
baseline's number stays ink.
```html
<div class="sa-pad sa-stat">
  <div class="big accent">40<span class="unit">ms</span></div>   <!-- drop .accent for someone else's number -->
  <div class="side"><div class="sa-kicker no-rule">What was measured</div><h2 class="sa-display sa-h3">So what</h2>
    <p class="sa-lede">Context</p><div class="sa-source">Source</div></div>
</div>
```
Up to four characters at 330 px. Fraunces figures have ball terminals (the 4 has a teardrop); that is the face.

## 07 Chart (inline SVG) — `08_accuracy.png`
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
Classes: `.grid .axis .bar .bar.hi .bar.ghost .value .value.hi .value.sm .cat .sub .callout .callout-line`. One unit
= one pixel at 1080p, so text sizes obey the same minimums. Give the SVG an `aria-label` that states the data.
Keep axis titles, tick labels and value labels apart: `render.py` fails on SVG text that overlaps other text, runs out
of the rect it sits in, or leaves the SVG box.

**Takeaway row.** Add `<p class="takeaway">One sentence</p>` between the plot and the source line; the grid adds the
row automatically.

## 17 Horizontal bars with a side note (a chart variant) — `09_cost.png`
For ranked categories with long names, and when the chart needs a "but" beside it (the price, a caveat). Add
`.with-note` to `.sa-chart`; the `.plot` becomes a grid of the SVG (left) and a 400 px note column (right).
```html
<div class="sa-pad sa-chart with-note">
  <div><div class="sa-kicker">What is measured</div><h2 class="sa-display sa-h2">Finding</h2></div>
  <div class="plot">
    <svg viewBox="0 0 1130 440">
      <line class="axis" x1="330" y1="10" x2="330" y2="430"/>
      <text class="cat" x="0" y="54">Category</text><text class="sub" x="0" y="80">muted second line</text>
      <rect class="bar" x="330" y="34" width="680" height="44"/><text class="value sm" x="1024" y="66">$4.10</text>
      …one row per 104 px…  <rect class="bar hi" …/><text class="value sm hi" …>$0.02</text>
    </svg>
    <div class="side-note"><div class="sa-note second">The price, as one sentence.</div><div class="sa-small">Qualifier</div></div>
  </div>
  <p class="takeaway" data-max-lines="1">What to do about it</p>
  <div class="sa-source">Source</div>
</div>
```
Labels go in a 300 px column left of the axis; `.value.sm` (28 px) fits rows 104 px apart. The note uses `.sa-note`
(green rule) or `.sa-note.second` (oxblood rule) when it states a cost. Three to six rows.

## 08 Quote — `10_rule.png`
A sentence worth quoting, green left rule, attribution in sans plus source in mono, an optional gloss.
```html
<div class="sa-pad sa-quote">
  <blockquote><div class="q" data-max-lines="3">Quote without quotation marks (CSS adds them)</div>
    <div class="who">Name<span class="sa-source">Context</span></div></blockquote>
  <p class="sa-lede gloss">Why it matters</p>
</div>
```
Only quote real, attributable words. A working rule of your own is labelled as such.

## 09 Image / plate with caption — `11_distil.png`
A figure in a hairline frame with a mono figure number and an italic caption; the explanation sits beside it.
```html
<div class="sa-pad sa-figure">
  <figure><div class="sa-frame"><svg>…</svg> or <img class="sa-plate-img" src="…"></div>
    <figcaption><span class="fig">Fig. 1</span><span class="cap">Caption</span></figcaption></figure>
  <div class="text"><div class="sa-kicker">…</div><h2 class="sa-display sa-h2">…</h2><p class="sa-lede">…</p></div>
</div>
```
Plates are textless (labels go in the caption or in DOM), grey ink (`.sa-plate-img`), never behind text being read.
Screenshots of software go in the same frame, unfiltered; dark screenshots use `.sa-frame.tight.dark` (no light mat).
For a recording, see 14.

## 10 Timeline — `15_plan.png`
Phases or dates left to right; past ticks are grey rings, the current one is a solid green dot. Set `--n` to the
number of ticks (3–5).
```html
<div class="sa-pad sa-timeline">
  <div><div class="sa-kicker">…</div><h2 class="sa-display sa-h2">…</h2></div>
  <div class="track" style="--n:4"><div class="tick past"><div class="when">Week 1</div><div class="what">…</div><div class="why">…</div></div>…<div class="tick now">…</div></div>
</div>
```

## 11 Speaker bio — `16_speaker.png`
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

## 12 CTA / course promo — `17_course.png`
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

## 13 Q&A / closing — `18_close.png`
The last frame: an invitation, the full logo once, a contact line.
```html
<div class="sa-pad sa-close">
  <h2 class="sa-display sa-h1">Questions</h2><p class="sa-lede">Invitation</p>
  <img class="sa-logo" src="brand/logos/primary-black.svg" alt="Superlinear Academy"><div class="contact">superlinear.academy</div>
</div>
```

## 14 Media: one recording or screenshot — `12_demo.png`
A screen recording (or a large screenshot) with its claim beside it. The frame is 1060 px wide at 16:9.
```html
<div class="sa-pad sa-media">
  <figure>
    <div class="sa-frame tight dark"><video class="sa-uncropped" src="media/run.webm" poster="media/run_poster.jpg"
         muted playsinline loop preload="metadata"></video></div>
    <figcaption><span class="fig">Fig. 2</span><span class="cap">What the recording shows</span></figcaption>
  </figure>
  <div class="text"><div class="sa-kicker">Demo</div><h2 class="sa-display sa-h3" data-max-lines="4">Claim</h2><p class="sa-lede">Context</p></div>
</div>
```
Rules for recordings:
- **Shown whole:** `video.sa-uncropped` (`object-fit: contain`); never `cover`. Portrait phone footage letterboxes.
- **Dark footage gets a dark frame:** `.sa-frame.tight.dark` (no padding, near-black letterbox). The default
  `.sa-frame` puts a light card mat around media, which makes dark footage look pasted on. Light screenshots use
  `.sa-frame.tight`.
- **Every video has a poster,** and the poster is a representative frame of *that* recording (mid-action, not a
  shared title card): screenshots, the PDF handout and slow connections show the poster. Extract it with
  `ffmpeg -ss <t> -i run.webm -frames:v 1 run_poster.jpg`. `render.py` fails on a video without a poster.
- **Format:** WebM (VP9) or MP4 (H.264); headless Chromium builds often lack H.264, so WebM renders everywhere
  (encode with `ffmpeg -i in.mov -c:v libvpx-vp9 -crf 36 -b:v 0 -an out.webm`; needs an ffmpeg built with libvpx).
  Muted, `playsinline`, `loop`, `preload="metadata"`.
- **Playback:** start and stop it from `window.DECK_HOOKS` (example `js/deck.js`: play on enter; pause and `load()`
  on leave so the poster returns). Do not autoplay on load: the deck preloads every frame.
- Recordings are unfiltered (no grayscale), like screenshots.

## 15 Media pair — `13_side_by_side.png`
Two recordings side by side, each with its own number and label. For "same input, two players".
```html
<div class="sa-pad sa-pair">
  <div><div class="sa-kicker">Same input, two players</div><h2 class="sa-display sa-h2" data-max-lines="1">Finding</h2></div>
  <div class="items">
    <div class="item"><div class="sa-frame tight dark"><video class="sa-uncropped" … poster="a_poster.jpg"></video></div>
      <div class="meta"><div class="num">2.4<span class="unit">s</span></div><div><div class="who">Player A</div><div class="desc">What the number is</div></div></div></div>
    <div class="item">… <div class="num accent">0.4<span class="unit">s</span></div> …</div>
  </div>
  <div class="sa-source">Source</div>
</div>
```
Give the two players different posters. Only your own number takes `.accent`; for a neutral comparison, neither does.

## 16 Table / matrix — `05_tradeoffs.png`
Two to four options compared across three to six dimensions. A real `<table>`; row headers are labels, cells are
serif sentences.
```html
<div class="sa-pad sa-tablewrap">
  <div><div class="sa-kicker">What is compared</div><h2 class="sa-display sa-h2" data-max-lines="1">Finding</h2></div>
  <table class="sa-table">
    <thead><tr><th></th><th>Option A</th><th class="ours">Option B</th></tr></thead>
    <tbody><tr><th scope="row">Dimension</th><td>Short sentence</td><td>Short sentence<span class="sa-small">qualifier</span></td></tr>…</tbody>
  </table>
  <div class="sa-source">Source</div>
</div>
```
`th.ours` puts a green rule under the recommended column's header; omit it for a neutral comparison. Numeric columns:
`td.num` / `th.num` (mono, right-aligned). Cells hold one short sentence; if a cell needs two, the table is the wrong
layout.

## 18 Missing-asset placeholder — `14_offline.png`
When a recording, screenshot or photo does not exist yet and the draft must still render. It is deliberately
unmistakable (oxblood dashed border, hatching, a "Placeholder" tag) so nobody mistakes it for content.
```html
<div class="sa-frame tight"><div class="sa-placeholder">
  <div class="sa-tag">Placeholder · recording pending</div>
  <div class="what">What the asset will show</div>
  <div class="spec">Format and length: portrait, about 30 s</div>
</div></div>
```
Use it inside any frame slot (media, figure, bio photo). On a `<div>` the class draws this box; on any other element
(`<img>`, a `<span>` around stand-in text) it is only a marker with no styling, which is how the promo templates flag
their example photo, name and date. `render.py` lists every placeholder as a warning, and `render.py --final` fails on
them, and also on images from a `placeholders/` folder and on the stand-in strings `Speaker Name`, `Month DD`. Never ship one; never fill the gap with a stock image or a generated look-alike.

## Choosing

| You want to say | Layout |
|---|---|
| One thing | 03 claim (default) or 06 stat if it is a number |
| A versus B | 04 compare |
| How to do it | 05 steps |
| What the data shows | 07 chart (17 for ranked categories or a chart with a caveat) |
| Options across several dimensions | 16 table |
| What it looks like running | 14 media; 15 pair for two side by side |
| An asset you do not have yet | 18 placeholder, in the slot where it will go |
| What it looks like / how it works | 09 figure |
| When | 10 timeline |
| Who said it / a rule | 08 quote |

Do not invent new decorative layouts (icon grids, three-card feature rows with icons, photo collages). If none fits,
compose from the primitives and keep one primary relationship per frame.
