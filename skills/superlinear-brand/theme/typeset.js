/* Superlinear Academy typesetting helper (optional, no dependencies).

   What it does
   1. Typographic quotes: ' " -> ’ ‘ “ ” (apostrophes and quotes in copy).
   2. Number + unit stay together: "115 ms" -> "115 ms" (no line break between them).
   3. Inline emphasis in copy slots: "a better one that ==waits on a network==" renders the marked phrase as
      <span class="sa-em">. "==" is the only markup it understands; everything else stays plain text (it builds DOM
      nodes, never innerHTML, so copy cannot inject markup).

   Where to load it
   - Canvas deck (presentation skill): AFTER js/copy.js and BEFORE js/engine.js:
       <script src="js/copy.js"></script>
       <script src="brand/typeset.js"></script>
       <script src="js/deck.js"></script>
       <script src="js/engine.js"></script>
     It typesets the strings in window.COPY before the engine fills the slots, then (on DOMContentLoaded, after the
     engine has run) turns ==markers== in filled slots into .sa-em spans and typesets static text in frames.
   - Promo page: in <head>, after the stylesheets. It typesets text on DOMContentLoaded.

   Limits
   - Typewriter elements (.type) are split into letters by the engine: ==markers== inside them are not supported
     (a console warning names the slot), and the engine's word split turns the no-break space back into a normal
     space. Keep numbers with units and emphasis out of .type elements.
   - Elements (and their subtree) with data-no-typeset, and <code>, <pre>, <script>, <style>, <textarea> are skipped.
   - Units recognised: ms s min h px pt fps % × x B K M KB MB GB TB tok (extend window.SA_TYPESET_UNITS before loading). */
(function () {
  const UNITS = (window.SA_TYPESET_UNITS || ["ms", "s", "min", "h", "px", "pt", "fps", "%", "×", "x", "B", "K", "M", "KB", "MB", "GB", "TB", "tok"])
    .map(u => u.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).join("|");
  const reUnit = new RegExp("(\\d)[ \\t]+(" + UNITS + ")(?![\\p{L}\\p{N}])", "gu");
  const OPENERS = /[\s([{—–\-\/“‘]/;

  /* prev: the character before s in reading order ("" at the start of a block) */
  function smart(s, prev) {
    let out = "", p = prev || "";
    for (const c of s) {
      if (c === '"') out += (p === "" || OPENERS.test(p)) ? "“" : "”";
      else if (c === "'") out += (p === "" || OPENERS.test(p)) ? "‘" : "’";
      else out += c;
      p = c;
    }
    return out.replace(reUnit, "$1 $2");
  }

  function prepCopy(o) {
    if (!o || typeof o !== "object") return;
    for (const k of Object.keys(o)) {
      if (typeof o[k] === "string") o[k] = smart(o[k], "");
      else if (o[k] && typeof o[k] === "object") prepCopy(o[k]);
    }
  }

  const SKIP = new Set(["CODE", "PRE", "SCRIPT", "STYLE", "TEXTAREA"]);
  const skipped = el => !el || el.closest("[data-no-typeset], .type") || SKIP.has(el.tagName);

  /* ==phrase== -> <span class="sa-em">phrase</span>, for elements whose text carries markers */
  function emphasize(root) {
    (root || document).querySelectorAll("[data-slot], [data-typeset]").forEach(el => {
      const t = el.textContent;
      if (!t.includes("==")) return;
      if (el.closest(".type")) { console.warn("typeset: ==emphasis== is not supported inside .type:", el.dataset.slot || el); return; }
      const parts = t.split(/==(.+?)==/);
      el.textContent = "";
      parts.forEach((part, i) => {
        if (!part) return;
        if (i % 2) { const s = document.createElement("span"); s.className = "sa-em"; s.textContent = part; el.appendChild(s); }
        else el.appendChild(document.createTextNode(part));
      });
    });
  }

  /* typographic pass over static text under each root, in reading order */
  function typesetText(root) {
    const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: n => skipped(n.parentElement) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT });
    const BLOCK = "p, div, li, h1, h2, h3, h4, h5, td, th, figcaption, blockquote, text";
    let prev = "", block = null, n;
    while ((n = w.nextNode())) {
      const b = n.parentElement.closest(BLOCK) || root;
      if (b !== block) prev = "";          // a new block starts a new sentence context
      block = b;
      const v = smart(n.nodeValue, prev);
      if (v !== n.nodeValue) n.nodeValue = v;
      if (n.nodeValue.length) prev = n.nodeValue.slice(-1);
    }
  }

  function run() {
    emphasize(document);
    const roots = document.querySelectorAll(".frame, .sa-pad, body.sa-promo, [data-typeset]");
    (roots.length ? roots : [document.body]).forEach(r => { if (!r.parentElement || !r.parentElement.closest(".frame, .sa-pad, body.sa-promo")) typesetText(r); });
  }

  if (window.COPY) prepCopy(window.COPY);
  window.saTypeset = { smart, prepCopy, emphasize, typesetText, run };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", run); else run();
})();
