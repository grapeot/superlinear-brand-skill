/* Slide table in speaking order. steps = clicks inside the slide (1 = no fragments).
   frame defaults to id; frames are laid out on the sheet in this order by js/engine.js.
   cam (optional) = [dx, dy, zoom] relative to the frame centre, or one entry per step. */
(function () {
  const S = (id, part, steps, cam, opts) => ({ id, part, steps, cam, ...opts });
  const P1 = "I · Why small", P2 = "II · How", P3 = "III · Ship it";
  window.DECK = [
    S("cover", "", 1),
    S("part1", P1, 1),
    S("claim", P1, 2),
    S("compare", P1, 3),
    S("recipe", P2, 4),
    S("latency", P2, 2),
    S("accuracy", P2, 2),
    S("rule", P2, 2),
    S("distil", P2, 1),
    S("plan", P3, 2),
    S("speaker", P3, 1),
    S("course", P3, 2),
    S("close", "", 1),
  ];
})();
