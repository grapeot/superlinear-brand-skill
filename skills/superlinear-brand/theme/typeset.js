/* Superlinear Academy typesetting helper (optional, no dependencies).

   What it does
   1. Typographic quotes: ' and " become ’ ‘ “ ” (apostrophes and quotes in copy).
   2. Number + unit stay together: "115 ms" gets a no-break space (U+00A0) so the pair never splits across lines.
   3. Inline emphasis in copy slots: "a better one that ==waits on a network==" renders the marked phrase as
      <span class="sa-em">. "==" is the only markup it understands. It works on text nodes and builds DOM nodes
      (never innerHTML), so copy cannot inject markup and existing child elements are preserved.

   Where it acts
   - Emphasis: inside elements with [data-slot] (filled by the presentation skill's engine) and inside elements you
     mark with [data-typeset] (for static markup that should accept ==markers== too).
   - Quotes and units: in window.COPY strings (before the engine fills the slots) and in the text of every .frame,
     .sa-pad, body.sa-promo and [data-typeset] element.
   - Skipped: [data-no-typeset] subtrees, <code>, <pre>, <kbd>, <samp>, <script>, <style>, <textarea>, and
     typewriter (.type) elements.

   Where to load it
   - Canvas deck (presentation skill): AFTER js/copy.js and BEFORE js/engine.js:
       <script src="js/copy.js"></script>
       <script src="brand/typeset.js"></script>
       <script src="js/deck.js"></script>
       <script src="js/engine.js"></script>
   - Promo page: in <head>, after the stylesheets. It runs on DOMContentLoaded.

   Limits
   - Quotes are decided from the preceding character only: an apostrophe at the start of a word ('90s, 'em) becomes
     an opening quote ‘ instead of ’ (type ’ yourself there), and quotes that open in one block and close in another
     are treated per block.
   - ==marker== pairs must sit inside one text node (do not split a marked phrase across elements), must not start or
     end with a space, and cannot contain "=" (so "a == b" is left alone).
   - Typewriter elements (.type) are split into letters by the engine: emphasis inside them is not supported (a console
     warning names the slot) and the engine's word split turns the no-break space back into a normal space.
   - Units recognised: ms s min h px pt fps % × x B K M KB MB GB TB tok. To ADD units, set
     window.SA_TYPESET_UNITS = ["tokens", "GPUs"] before loading this file; they extend the default list. */
(function () {
  const DEFAULT_UNITS = ["ms", "s", "min", "h", "px", "pt", "fps", "%", "×", "x", "B", "K", "M", "KB", "MB", "GB", "TB", "tok"];
  const UNITS = DEFAULT_UNITS.concat(window.SA_TYPESET_UNITS || [])
    .sort((a, b) => b.length - a.length)
    .map(u => u.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).join("|");
  const NBSP = "\u00a0";
  const reUnit = new RegExp("(\\d)[ \\t]+(" + UNITS + ")(?![\\p{L}\\p{N}])", "gu");
  const reEm = /==(\S(?:[^=]*?\S)?)==/g;
  const OPENERS = /[\s([{—–\-\/“‘]/;
  const SKIP_SEL = "[data-no-typeset], .type, code, pre, kbd, samp, script, style, textarea";

  /* prev: the character before s in reading order ("" at the start of a block) */
  function smart(s, prev) {
    let out = "", p = prev || "";
    for (const c of s) {
      if (c === '"') out += (p === "" || OPENERS.test(p)) ? "“" : "”";
      else if (c === "'") out += (p === "" || OPENERS.test(p)) ? "‘" : "’";
      else out += c;
      p = c;
    }
    return out.replace(reUnit, "$1" + NBSP + "$2");
  }

  function prepCopy(o) {
    if (!o || typeof o !== "object") return;
    for (const k of Object.keys(o)) {
      if (typeof o[k] === "string") o[k] = smart(o[k], "");
      else if (o[k] && typeof o[k] === "object") prepCopy(o[k]);
    }
  }

  const skipped = el => !el || !!el.closest(SKIP_SEL);
  function textNodes(root) {
    const out = [], w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: n => skipped(n.parentElement) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT });
    let n; while ((n = w.nextNode())) out.push(n);
    return out;
  }

  /* ==phrase== -> <span class="sa-em">phrase</span>, text node by text node */
  function emphasize(root) {
    (root || document).querySelectorAll("[data-slot], [data-typeset]").forEach(el => {
      if (el.closest(".type")) { if (el.textContent.includes("==")) console.warn("typeset: ==emphasis== is not supported inside .type:", el.dataset.slot || el); return; }
      for (const n of textNodes(el)) {
        const t = n.nodeValue;
        reEm.lastIndex = 0;
        if (!reEm.test(t)) continue;
        reEm.lastIndex = 0;
        const frag = document.createDocumentFragment();
        let last = 0, m;
        while ((m = reEm.exec(t))) {
          if (m.index > last) frag.appendChild(document.createTextNode(t.slice(last, m.index)));
          const s = document.createElement("span"); s.className = "sa-em"; s.textContent = m[1]; frag.appendChild(s);
          last = m.index + m[0].length;
        }
        if (last < t.length) frag.appendChild(document.createTextNode(t.slice(last)));
        n.parentNode.replaceChild(frag, n);
      }
    });
  }

  /* typographic pass over static text under root, in reading order */
  function typesetText(root) {
    const BLOCK = "p, div, li, h1, h2, h3, h4, h5, td, th, figcaption, blockquote, text";
    let prev = "", block = null;
    for (const n of textNodes(root)) {
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
    const sel = ".frame, .sa-pad, body.sa-promo, [data-typeset]";
    const roots = [...document.querySelectorAll(sel)].filter(r => !(r.parentElement && r.parentElement.closest(sel)));
    roots.forEach(typesetText);
  }

  if (window.COPY) prepCopy(window.COPY);
  window.saTypeset = { smart, prepCopy, emphasize, typesetText, run };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", run); else run();
})();
