#!/usr/bin/env python3
"""Render Superlinear Academy brand pages to PNG and audit them.

Two modes:

  render.py page <file.html> [<file.html> ...] [--out-dir DIR] [--size 1920x1080] [--scale 1] [--final]
      Static promo / cover / OG pages, opened over file://. The canvas size comes from --size, or from
      <meta name="sa:canvas" content="2100x750"> in the page. Writes <name>.png (next to the page by default).

  render.py deck <deck_dir> [--root DIR] [--out DIR] [--sheet FILE] [--all-steps] [--final]
      A presentation-skill HTML canvas deck (window.DECK + window.deckGoto). Serves --root (default: the deck
      directory itself; pass --root only when the deck links files above itself) on a loopback port with a deep
      listen backlog, prints every slide at its last step (or its `print` step; every step with --all-steps) to
      <out>/NN_<id>[_<step>].png (default <deck>/verification/brand/) and writes contact_sheet.jpg.

Problems (any one gives exit code 1):
  console_errors, failed_requests   something did not load or threw
  external_requests                 a request left file:// or the loopback server (CDN fonts, analytics ...)
  font_errors                       a vendored font failed to load
  offcanvas                         HTML text, an image or a video leaves the canvas (page) or its frame (deck)
  unsafe                            ... leaves the <meta name="sa:safe" content="L,T,R,B"> area ([data-bleed] exempt)
  wrapped                           a [data-max-lines="N"] element wraps to more than N lines
  number_unit_break                 a line break falls between a number and its unit ("115 / ms")
  images                            an <img> did not load, or a <video> has no poster
  cropped                           an img/video.sa-uncropped is cropped (object-fit: cover) or stretched
  svg_text_outside                  SVG <text> extends past its <svg> box (the viewBox as drawn)
  svg_text_overflow                 SVG <text> whose centre sits in a <rect> is not fully inside that rect
  svg_text_overlap                  two SVG <text> boxes overlap
  unprocessed_markup                "==" emphasis markers are visible (typeset.js not loaded, or inside .type)
  placeholders                      .sa-placeholder elements (a problem only with --final; else a warning)
  missing_slots                     (deck) a presentation-skill copy slot was not filled
Warnings (reported, exit code unaffected):
  straight_quotes                   ' or " in visible text (load theme/typeset.js, or use ’ “ ”)
  number_unit_space                 a breakable space between a number and its unit (use U+00A0 or typeset.js)
  scaffold_class                    an element inside .sa-pad uses a class the presentation skill's deck.css styles
                                    globally (.note, .label, .role, .quote ...): rename it
  placeholders                      without --final

Mark an element (or an SVG group) data-audit-skip to exempt it and its subtree from the SVG checks.
Captures hide the presentation skill's navigator button and show every <video> at its poster.

Requires: playwright (with a Chromium build: `python -m playwright install chromium`) and Pillow.
"""
from __future__ import annotations

import argparse
import functools
import http.server
import json
import pathlib
import re
import sys
import threading

from playwright.sync_api import sync_playwright

CAPTURE_CSS = ("*, *::before, *::after { transition: none !important; animation: none !important; }"
               " #navbtn { display: none !important; }")

POSTER_JS = """() => { document.querySelectorAll('video').forEach(v => { try { v.pause(); v.removeAttribute('autoplay'); v.load(); } catch (e) {} }); }"""

AUDIT_JS = r"""
([scopeSel, W, H, safe]) => {
  const out = { offcanvas: [], unsafe: [], wrapped: [], number_unit_break: [], images: [], cropped: [],
                svg_text_outside: [], svg_text_overflow: [], svg_text_overlap: [], unprocessed_markup: [], placeholders: [],
                straight_quotes: [], number_unit_space: [], scaffold_class: [] };
  const scope = scopeSel ? document.querySelector(scopeSel) : document.body;
  if (!scope) { out.offcanvas.push("scope not found: " + scopeSel); return out; }
  const tol = 1.5;
  const visible = el => { for (let e = el; e && e.nodeType === 1; e = e.parentElement) { const cs = getComputedStyle(e);
      if (cs.display === "none" || cs.visibility === "hidden" || +cs.opacity < 0.01) return false; if (e === scope) break; } return true; };
  const short = s => (s || "").trim().replace(/\s+/g, " ").slice(0, 60);
  const label = el => (el.id ? "#" + el.id : el.tagName.toLowerCase() + (typeof el.className === "string" && el.className.trim() ? "." + el.className.trim().split(/\s+/).join(".") : ""))
    + " «" + short(el.textContent || el.getAttribute("src") || el.getAttribute("poster")) + "»";
  const box = r => `[${Math.round(r.left)},${Math.round(r.top)} → ${Math.round(r.right)},${Math.round(r.bottom)}]`;
  const sb = scopeSel ? scope.getBoundingClientRect() : { left: 0, top: 0, right: W, bottom: H };
  const isMedia = el => ["IMG", "VIDEO"].includes(el.tagName) || el.tagName.toLowerCase() === "svg";

  /* ---------- HTML leaves: text-bearing elements, images, videos, svgs ---------- */
  const leaves = [];
  scope.querySelectorAll("*").forEach(el => {
    if (el.closest("svg") && el.tagName.toLowerCase() !== "svg") return;
    const hasText = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (hasText || isMedia(el)) leaves.push(el);
  });
  for (const el of leaves) {
    if (!visible(el)) continue;
    let r;
    if (isMedia(el)) r = el.getBoundingClientRect();
    else { const rg = document.createRange(); rg.selectNodeContents(el); r = rg.getBoundingClientRect(); }
    if (!r.width || !r.height) continue;
    const bleed = el.closest("[data-bleed]");
    if (!bleed && (r.left < sb.left - tol || r.top < sb.top - tol || r.right > sb.right + tol || r.bottom > sb.bottom + tol)) out.offcanvas.push(label(el) + " " + box(r));
    if (safe && !bleed) { const [L, T, R, B] = safe;
      if (r.left < L - tol || r.top < T - tol || r.right > W - R + tol || r.bottom > H - B + tol) out.unsafe.push(label(el) + " " + box(r)); }
  }

  /* ---------- wrapping ---------- */
  scope.querySelectorAll("[data-max-lines]").forEach(el => {
    if (!visible(el)) return;
    const rg = document.createRange(); rg.selectNodeContents(el);
    const tops = [];
    for (const rc of rg.getClientRects()) { if (rc.width < 1) continue; if (!tops.some(t => Math.abs(t - rc.top) < rc.height * 0.5)) tops.push(rc.top); }
    if (tops.length > +el.dataset.maxLines) out.wrapped.push(label(el) + ` (${tops.length} lines, max ${el.dataset.maxLines})`);
  });

  /* ---------- typography over visible text nodes ---------- */
  const UNIT = /(\d[\d.,]*)([ \t ]+)(ms|s|min|h|px|pt|fps|%|×|x|B|K|M|KB|MB|GB|TB|tok)(?![\p{L}\p{N}])/gu;
  const tw = document.createTreeWalker(scope, NodeFilter.SHOW_TEXT);
  let tn;
  while ((tn = tw.nextNode())) {
    const p = tn.parentElement; const v = tn.nodeValue;
    if (!v.trim() || !p || p.closest("script, style, code, pre, [data-no-typeset]") || !visible(p)) continue;
    if (v.includes("==")) out.unprocessed_markup.push(label(p));
    if (/['"]/.test(v) && !p.closest(".sa-source, .url, .links")) out.straight_quotes.push(label(p));
    for (const m of v.matchAll(UNIT)) {
      if (m[2] !== " ") out.number_unit_space.push(label(p) + " «" + m[0] + "»");
      const last = m.index + m[1].length - 1;                       // the number's last digit
      const a = document.createRange(); a.setStart(tn, last); a.setEnd(tn, last + 1);
      const uStart = m.index + m[1].length + m[2].length;
      const b = document.createRange(); b.setStart(tn, uStart); b.setEnd(tn, uStart + 1);
      const ra = a.getBoundingClientRect(), rb = b.getBoundingClientRect();
      if (ra.height && rb.height && Math.abs(ra.top - rb.top) > ra.height * 0.5) out.number_unit_break.push(label(p) + " «" + m[0] + "»");
    }
  }

  /* ---------- media ---------- */
  scope.querySelectorAll("img").forEach(img => { if (visible(img) && (!img.complete || !img.naturalWidth)) out.images.push("not loaded: " + img.getAttribute("src")); });
  scope.querySelectorAll("video").forEach(v => { if (visible(v) && !v.getAttribute("poster")) out.images.push("video without poster: " + (v.getAttribute("src") || "")); });
  scope.querySelectorAll("img.sa-uncropped, video.sa-uncropped").forEach(m => {
    const nw = m.naturalWidth || m.videoWidth, nh = m.naturalHeight || m.videoHeight;
    if (!nw || !nh || !visible(m)) return;
    const fit = getComputedStyle(m).objectFit, same = Math.abs(m.clientWidth / m.clientHeight - nw / nh) < 0.01;
    if (!same && fit === "cover") out.cropped.push(label(m) + " object-fit: cover crops it");
    if (!same && fit === "fill") out.cropped.push(label(m) + " stretched (object-fit: fill)");
  });
  scope.querySelectorAll(".sa-placeholder").forEach(el => { if (visible(el)) out.placeholders.push(label(el)); });

  /* ---------- class names that the presentation skill's deck.css styles globally, used inside brand layouts ---------- */
  const GLOBALS = new Set("answers beat beats board bracket cell cells closer col course docs duties duty erow erows jcase jtag jtext label lede lever levers mitem mrow mspec note numeral pipeline pstage quote role roles rulelist rungtext scale slab small source specimen stack strike tcol timeline trace tri veil window".split(" "));
  scope.querySelectorAll(".sa-pad *, body.sa-promo *").forEach(el => {
    if (typeof el.className !== "string") return;
    const hit = el.className.split(/\s+/).filter(c => GLOBALS.has(c));
    if (hit.length) out.scaffold_class.push(label(el) + " uses ." + hit.join(", ."));
  });

  /* ---------- inside SVG ---------- */
  scope.querySelectorAll("svg").forEach(svg => {
    if (!visible(svg) || svg.closest("[data-audit-skip]") || svg.closest("defs, pattern, clipPath, mask")) return;
    if (svg.parentElement && svg.parentElement.closest("svg")) return;            // nested svg: handled by the outer one
    const sr = svg.getBoundingClientRect();
    if (!sr.width || !sr.height) return;
    const texts = [...svg.querySelectorAll("text")]
      .filter(t => t.textContent.trim() && !t.closest("[data-audit-skip], defs, pattern, clipPath, mask") && visible(t))
      .map(t => [t, t.getBoundingClientRect()]).filter(([, r]) => r.width && r.height);
    const rects = [...svg.querySelectorAll("rect")]
      .filter(r => !r.closest("[data-audit-skip], defs, pattern, clipPath, mask") && visible(r))
      .map(r => r.getBoundingClientRect()).filter(r => r.width > 6 && r.height > 6 && r.width * r.height < 0.6 * sr.width * sr.height);
    const tlabel = t => "svg text «" + short(t.textContent) + "»";
    for (const [t, r] of texts) {
      if (r.left < sr.left - tol || r.right > sr.right + tol || r.top < sr.top - tol || r.bottom > sr.bottom + tol)
        out.svg_text_outside.push(tlabel(t) + " " + box(r) + " svg " + box(sr));
      const cx = (r.left + r.right) / 2, cy = (r.top + r.bottom) / 2;
      const host = rects.filter(b => cx > b.left && cx < b.right && cy > b.top && cy < b.bottom)
                        .sort((a, b) => a.width * a.height - b.width * b.height)[0];
      if (host && (r.left < host.left - tol || r.right > host.right + tol || r.top < host.top - tol || r.bottom > host.bottom + tol))
        out.svg_text_overflow.push(tlabel(t) + " " + box(r) + " box " + box(host));
    }
    const pad = 1;
    for (let i = 0; i < texts.length; i++) for (let j = i + 1; j < texts.length; j++) {
      const a = texts[i][1], b = texts[j][1];
      const w = Math.min(a.right, b.right) - Math.max(a.left, b.left) - 2 * pad, h = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) - 2 * pad;
      if (w > 0 && h > 0) out.svg_text_overlap.push(tlabel(texts[i][0]) + " × " + tlabel(texts[j][0]));
    }
  });
  return out;
}
"""

FONTS_JS = """async () => { await document.fonts.ready; return [...document.fonts].map(f => [f.family.replace(/"/g, ''), f.style, String(f.weight), f.status]); }"""

WARN_KEYS = {"straight_quotes", "number_unit_space", "scaffold_class"}


def split(audit: dict, final: bool) -> tuple[dict, dict]:
    problems, warnings = {}, {}
    for k, v in audit.items():
        if not v:
            continue
        if k in WARN_KEYS or (k == "placeholders" and not final):
            warnings[k] = sorted(set(v))
        else:
            problems[k] = v
    return problems, warnings


def launch(p):
    try:
        return p.chromium.launch()
    except Exception:
        return p.chromium.launch(channel="chrome")  # fall back to an installed Google Chrome


class Watch:
    """Collects console errors, failed requests and requests that leave the allowed origins."""

    def __init__(self, page, allowed: tuple[str, ...]):
        self.errors, self.failed, self.external = [], [], []
        page.on("console", lambda m: self.errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: self.errors.append(str(e)))
        page.on("requestfailed", lambda r: self.failed.append(f"{r.url} ({r.failure})"))
        page.on("request", lambda r: None if r.url.startswith(allowed) else self.external.append(r.url))


def font_problems(page) -> tuple[list, list]:
    fonts = page.evaluate(FONTS_JS)
    bad = [f for f in fonts if f[3] == "error"]
    loaded = sorted({f"{f[0]} {f[2]} {f[1]}" for f in fonts if f[3] == "loaded"})
    return bad, loaded


def contact_sheet(shots: list[tuple[str, pathlib.Path]], out: pathlib.Path, cols: int = 4, w: int = 480):
    from PIL import Image, ImageDraw
    if not shots:
        return
    first = Image.open(shots[0][1])
    h = round(w * first.height / first.width)
    rows = (len(shots) + cols - 1) // cols
    pad, lab = 16, 26
    sheet = Image.new("RGB", (cols * (w + pad) + pad, rows * (h + lab + pad) + pad), (226, 229, 224))
    d = ImageDraw.Draw(sheet)
    for k, (name, f) in enumerate(shots):
        im = Image.open(f).convert("RGB").resize((w, h), Image.LANCZOS)
        x, y = pad + (k % cols) * (w + pad), pad + (k // cols) * (h + lab + pad)
        sheet.paste(im, (x, y))
        d.text((x + 2, y + h + 7), name, fill=(40, 40, 40))
    sheet.save(out, quality=88)


def run_page(args) -> int:
    report, ok = [], True
    with sync_playwright() as p:
        b = launch(p)
        for src in args.files:
            src = pathlib.Path(src).resolve()
            html = src.read_text(encoding="utf-8")
            size = args.size
            if not size:
                m = re.search(r'<meta\s+name="sa:canvas"\s+content="(\d+)x(\d+)"', html)
                size = f"{m.group(1)}x{m.group(2)}" if m else "1920x1080"
            W, H = map(int, size.split("x"))
            ms = re.search(r'<meta\s+name="sa:safe"\s+content="([\d.,\s]+)"', html)
            safe = [float(v) for v in ms.group(1).split(",")] if ms else None
            pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=args.scale)
            watch = Watch(pg, ("file://", "data:", "blob:", "about:"))
            pg.goto(src.as_uri())
            pg.add_style_tag(content=CAPTURE_CSS)
            pg.evaluate(POSTER_JS)
            bad_fonts, loaded = font_problems(pg)
            pg.wait_for_timeout(400)
            audit = pg.evaluate(AUDIT_JS, [None, W, H, safe])
            out_dir = pathlib.Path(args.out_dir).resolve() if args.out_dir else src.parent
            out_dir.mkdir(parents=True, exist_ok=True)
            png = out_dir / (src.stem + ".png")
            pg.screenshot(path=str(png), clip={"x": 0, "y": 0, "width": W, "height": H})
            pg.close()
            problems, warnings = split({**audit, "console_errors": watch.errors, "failed_requests": watch.failed,
                                        "external_requests": watch.external, "font_errors": bad_fonts}, args.final)
            ok &= not problems
            report.append({"page": src.name, "png": str(png), "size": size, "safe_area": safe, "fonts_loaded": loaded,
                           "problems": problems, "warnings": warnings})
        b.close()
    print(json.dumps(report, indent=1, ensure_ascii=False))
    return 0 if ok else 1


def run_deck(args) -> int:
    deck = pathlib.Path(args.deck).resolve()
    root = pathlib.Path(args.root).resolve() if args.root else deck
    rel = deck.relative_to(root).as_posix()
    out = pathlib.Path(args.out).resolve() if args.out else deck / "verification" / "brand"
    out.mkdir(parents=True, exist_ok=True)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(root))
    http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None

    class Server(http.server.ThreadingHTTPServer):
        request_queue_size = 128   # the stdlib default (5) resets connections when a themed deck loads ~30 files at once
        daemon_threads = True

    srv = Server(("127.0.0.1", 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_address[1]}"
    shots, per_slide, ok = [], [], True
    with sync_playwright() as p:
        b = launch(p)
        pg = b.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=args.scale)
        watch = Watch(pg, (base, "data:", "blob:", "about:"))
        pg.goto(f"{base}/{rel}/index.html" if rel != "." else f"{base}/index.html")
        pg.wait_for_function("document.body.classList.contains('ready')", timeout=20000)
        pg.add_style_tag(content=CAPTURE_CSS)
        bad_fonts, loaded = font_problems(pg)
        slides = pg.evaluate("window.DECK.map(s => [s.id, s.frame || s.id, s.steps, s.print])")
        for i, (sid, frame, steps, prn) in enumerate(slides):
            last = prn if isinstance(prn, int) else steps - 1
            for step in (range(steps) if args.all_steps else [last]):
                pg.evaluate(f"deckGoto({i}, {step})")
                pg.evaluate(POSTER_JS)
                pg.wait_for_timeout(args.wait)
                audit = pg.evaluate(AUDIT_JS, [f"#{frame}", 1920, 1080, None])
                name = f"{i + 1:02d}_{sid}" + (f"_{step}" if args.all_steps else "")
                f = out / f"{name}.png"
                pg.screenshot(path=str(f))
                shots.append((f"{i + 1:02d} {sid}" + (f".{step}" if args.all_steps else ""), f))
                problems, warnings = split(audit, args.final)
                ok &= not problems
                per_slide.append({"slide": sid, "step": step, "png": f.name, "problems": problems, "warnings": warnings})
        missing = pg.evaluate("[...document.querySelectorAll('.missing')].map(e => e.dataset.slot)")
        b.close()
    srv.shutdown()
    sheet = pathlib.Path(args.sheet).resolve() if args.sheet else out / "contact_sheet.jpg"
    contact_sheet(shots, sheet)
    glob = {k: v for k, v in {"console_errors": watch.errors, "failed_requests": watch.failed, "external_requests": watch.external,
                               "font_errors": bad_fonts, "missing_slots": missing}.items() if v}
    ok &= not glob
    print(json.dumps({"deck": str(deck), "served_root": str(root), "shots": len(shots), "out": str(out), "contact_sheet": str(sheet),
                      "fonts_loaded": loaded, "problems": glob,
                      "per_slide": [s for s in per_slide if s["problems"] or s["warnings"]]}, indent=1, ensure_ascii=False))
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="mode", required=True)
    a = sub.add_parser("page", help="render static promo / cover pages")
    a.add_argument("files", nargs="+")
    a.add_argument("--out-dir")
    a.add_argument("--size", help="WxH; default from <meta name=sa:canvas>")
    a.add_argument("--scale", type=float, default=1, help="device scale factor (2 for retina exports)")
    a.add_argument("--final", action="store_true", help="treat .sa-placeholder elements as problems")
    d = sub.add_parser("deck", help="print every slide of a canvas deck")
    d.add_argument("deck")
    d.add_argument("--root", help="directory to serve (default: the deck). Use only if the deck links files above itself")
    d.add_argument("--out", help="default: <deck>/verification/brand")
    d.add_argument("--sheet")
    d.add_argument("--all-steps", action="store_true", help="capture every step, not only the last (like the presentation skill's shoot.py)")
    d.add_argument("--wait", type=int, default=500, help="ms to settle after each jump")
    d.add_argument("--scale", type=float, default=1)
    d.add_argument("--final", action="store_true", help="treat .sa-placeholder elements as problems")
    args = ap.parse_args()
    return run_page(args) if args.mode == "page" else run_deck(args)


if __name__ == "__main__":
    sys.exit(main())
