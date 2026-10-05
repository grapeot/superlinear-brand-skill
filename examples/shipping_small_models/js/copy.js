/* Speaker notes for the example deck. A scaffolded deck generates this file from copy/copy.md
   with tools/copy_to_js.py; on-screen copy can live here too and be bound with data-slot. */
window.COPY = {
  cover:    { notes: "Example cover. The kicker names the occasion, the title is the talk, the lede is the promise." },
  part1:    { notes: "Section opener. One line for why this part exists." },
  /* on-screen copy for slotted elements: "==phrase==" becomes green emphasis (brand/typeset.js);
     straight quotes and "40 ms" are typeset automatically */
  claim:    { headline: "A model that runs where the user is beats a better one that ==waits on a network==",
              support: "Users judge the answer they get in the moment, not the benchmark score behind it. A 40 ms reply doesn't feel like waiting.",
              notes: "One claim, set large. The support line arrives on the next click.\n\n[click]\n\nThe source line stays small and grey." },
  compare:  { notes: "Two hairline cards. Green inset bar for the side we recommend, oxblood hatching for the side we reject.\n\n[click]\n\n[click]\n\nThe closing line says what to do." },
  tradeoffs: { notes: "A real table. The recommended column gets a green rule under its header and nothing louder." },
  recipe:   { notes: "Four steps, one per click. The current step carries the green rule." },
  latency:  { notes: "One big number in brand green, with its label and source beside it." },
  accuracy: { notes: "Inline SVG chart. Only the bar the slide is about is green; the rest are hairline outlines.\n\n[click]\n\nThe callout arrives on its own beat." },
  cost:     { notes: "Horizontal bars with a muted second line under each category, a side note for the price, and a takeaway row.\n\n[click]\n\nThe note and the takeaway arrive together." },
  rule:     { notes: "A quote with a green rule. The gloss explains why it matters." },
  distil:   { notes: "A textless line plate in a hairline frame, with a mono figure number and an italic caption." },
  demo:     { notes: "One recording, shown whole in a tight dark frame. It plays on enter; the poster is a representative frame." },
  side_by_side: { notes: "Two recordings side by side, each with its own number. Only our number is green." },
  offline:  { notes: "A placeholder for a recording that does not exist yet. render.py lists it; --final fails on it." },
  plan:     { notes: "Timeline. Past ticks are grey rings, the current one is a solid green dot." },
  speaker:  { notes: "Speaker bio. The headshot is shown whole, letterboxed if needed, never cropped." },
  course:   { notes: "Course call to action. The only solid green block in the system is the button." },
  close:    { notes: "Questions. The full logo appears once, with its clear space built in." },
};
