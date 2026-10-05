#!/usr/bin/env python3
"""Render Superlinear Academy brand pages to PNG and audit them.

Two modes:

  render.py page <file.html> [<file.html> ...] [--out-dir DIR] [--size 1920x1080] [--scale 1]
      Static promo / cover / OG pages. The canvas size comes from --size, or from
      <meta name="sa:canvas" content="2100x750"> in the page. Writes <name>.png.

  render.py deck <deck_dir> [--root DIR] [--out DIR] [--sheet FILE]
      A presentation-skill HTML canvas deck (window.DECK + window.deckGoto). Serves --root
      (default: the git root above the deck, else the deck itself) on a loopback port, prints every
      slide at its last step to <out>/NN_<id>.png and writes a contact sheet.

Audits (any failure gives exit code 1):
  - console errors, page errors, failed requests
  - any request that is not file://, data: or the loopback server (no Google Fonts, no CDNs)
  - web fonts that failed to load
  - text or images that leave the canvas (or the active frame, in deck mode)
  - [data-max-lines="N"] elements that wrap to more than N lines (titles that must not wrap)
  - pages with <meta name="sa:safe" content="L,T,R,B">: text and images must stay inside the
    safe area (L/T/R/B are insets in px); elements inside [data-bleed] are exempt
  - <img> elements that did not load, and <img class="sa-uncropped"> whose box crops the image

Requires: playwright (with a Chromium build: `python -m playwright install chromium`) and Pillow.
"""
from __future__ import annotations

import argparse
import functools
import http.server
import json
import re
import pathlib
import subprocess
import sys
import threading

from playwright.sync_api import sync_playwright

NO_MOTION = "*, *::before, *::after { transition: none !important; animation: none !important; }"

AUDIT_JS = r"""
([scopeSel, W, H, safe]) => {
  const scope = scopeSel ? document.querySelector(scopeSel) : document.body;
  const out = { offcanvas: [], wrapped: [], unsafe: [], images: [], cropped: [] };
  if (!scope) { out.offcanvas.push("scope not found: " + scopeSel); return out; }
  const visible = el => { const cs = getComputedStyle(el); return cs.visibility !== "hidden" && cs.display !== "none" && +cs.opacity > 0.01; };
  const label = el => (el.id ? "#" + el.id : el.tagName.toLowerCase() + (el.className && typeof el.className === "string" ? "." + el.className.trim().split(/\s+/).join(".") : "")) + " «" + (el.textContent || el.getAttribute("src") || "").trim().replace(/\s+/g, " ").slice(0, 50) + "»";
  // scope box: in deck mode the active frame as it sits on the stage
  const sb = scopeSel ? scope.getBoundingClientRect() : { left: 0, top: 0, right: W, bottom: H };
  const leaves = [];
  scope.querySelectorAll("*").forEach(el => {
    if (el.closest("svg") && el.tagName.toLowerCase() !== "svg") return;
    const hasText = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (hasText || el.tagName === "IMG" || el.tagName.toLowerCase() === "svg") leaves.push(el);
  });
  for (const el of leaves) {
    if (!visible(el)) continue;
    let r;
    if (el.tagName === "IMG" || el.tagName.toLowerCase() === "svg") r = el.getBoundingClientRect();
    else { const rg = document.createRange(); rg.selectNodeContents(el); r = rg.getBoundingClientRect(); }
    if (!r.width || !r.height) continue;
    const tol = 1.5;
    if (r.left < sb.left - tol || r.top < sb.top - tol || r.right > sb.right + tol || r.bottom > sb.bottom + tol)
      if (!el.closest("[data-bleed]")) out.offcanvas.push(label(el) + ` [${Math.round(r.left)},${Math.round(r.top)} → ${Math.round(r.right)},${Math.round(r.bottom)}]`);
    if (safe && !el.closest("[data-bleed]")) {
      const [L, T, R, B] = safe;
      if (r.left < L - tol || r.top < T - tol || r.right > W - R + tol || r.bottom > H - B + tol)
        out.unsafe.push(label(el) + ` [${Math.round(r.left)},${Math.round(r.top)} → ${Math.round(r.right)},${Math.round(r.bottom)}]`);
    }
  }
  scope.querySelectorAll("[data-max-lines]").forEach(el => {
    if (!visible(el)) return;
    const rg = document.createRange(); rg.selectNodeContents(el);
    const tops = [];
    for (const rc of rg.getClientRects()) { if (rc.width < 1) continue; if (!tops.some(t => Math.abs(t - rc.top) < rc.height * 0.5)) tops.push(rc.top); }
    const max = +el.dataset.maxLines;
    if (tops.length > max) out.wrapped.push(label(el) + ` (${tops.length} lines, max ${max})`);
  });
  scope.querySelectorAll("img").forEach(img => {
    if (!img.complete || !img.naturalWidth) out.images.push("not loaded: " + img.getAttribute("src"));
    if (img.classList.contains("sa-uncropped") && img.naturalWidth) {
      const cs = getComputedStyle(img);
      const boxAR = img.clientWidth / img.clientHeight, imgAR = img.naturalWidth / img.naturalHeight;
      if (cs.objectFit === "cover" && Math.abs(boxAR - imgAR) > 0.01) out.cropped.push(label(img) + " object-fit: cover crops the image");
      if (cs.objectFit === "fill" && Math.abs(boxAR - imgAR) > 0.01) out.cropped.push(label(img) + " stretched (object-fit: fill)");
    }
  });
  return out;
}
"""

FONTS_JS = """async () => { await document.fonts.ready; return [...document.fonts].map(f => [f.family.replace(/"/g, ''), f.style, String(f.weight), f.status]); }"""


def git_root(p: pathlib.Path) -> pathlib.Path | None:
    try:
        r = subprocess.run(["git", "-C", str(p), "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True)
        return pathlib.Path(r.stdout.strip())
    except Exception:
        return None


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
            size = args.size
            html = src.read_text(encoding="utf-8")
            if not size:
                m = re.search(r'<meta\s+name="sa:canvas"\s+content="(\d+)x(\d+)"', html)
                size = f"{m.group(1)}x{m.group(2)}" if m else "1920x1080"
            W, H = map(int, size.split("x"))
            ms = re.search(r'<meta\s+name="sa:safe"\s+content="([\d.,\s]+)"', html)
            safe = [float(v) for v in ms.group(1).split(",")] if ms else None
            pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=args.scale)
            watch = Watch(pg, ("file://", "data:", "blob:", "about:"))
            pg.goto(src.as_uri())
            pg.add_style_tag(content=NO_MOTION)
            bad_fonts, loaded = font_problems(pg)
            pg.wait_for_timeout(300)
            audit = pg.evaluate(AUDIT_JS, [None, W, H, safe])
            out_dir = pathlib.Path(args.out_dir).resolve() if args.out_dir else src.parent
            out_dir.mkdir(parents=True, exist_ok=True)
            png = out_dir / (src.stem + ".png")
            pg.screenshot(path=str(png), clip={"x": 0, "y": 0, "width": W, "height": H})
            pg.close()
            problems = {k: v for k, v in {**audit, "console_errors": watch.errors, "failed_requests": watch.failed,
                                          "external_requests": watch.external, "font_errors": bad_fonts}.items() if v}
            ok &= not problems
            report.append({"page": src.name, "png": str(png), "size": size, "safe_area": safe, "fonts_loaded": loaded, "problems": problems})
        b.close()
    print(json.dumps(report, indent=1, ensure_ascii=False))
    return 0 if ok else 1


def run_deck(args) -> int:
    deck = pathlib.Path(args.deck).resolve()
    root = pathlib.Path(args.root).resolve() if args.root else (git_root(deck) or deck)
    rel = deck.relative_to(root).as_posix()
    out = pathlib.Path(args.out).resolve() if args.out else deck / "screenshots"
    out.mkdir(parents=True, exist_ok=True)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(root))
    http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
    class Server(http.server.ThreadingHTTPServer):
        request_queue_size = 128          # the default (5) resets connections when the page loads ~30 files at once
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
        pg.add_style_tag(content=NO_MOTION)
        bad_fonts, loaded = font_problems(pg)
        slides = pg.evaluate("window.DECK.map(s => [s.id, s.frame || s.id, s.steps, s.print])")
        for i, (sid, frame, steps, prn) in enumerate(slides):
            step = prn if isinstance(prn, int) else steps - 1
            pg.evaluate(f"deckGoto({i}, {step})")
            pg.wait_for_timeout(args.wait)
            audit = pg.evaluate(AUDIT_JS, [f"#{frame}", 1920, 1080, None])
            f = out / f"{i + 1:02d}_{sid}.png"
            pg.screenshot(path=str(f))
            shots.append((f"{i + 1:02d} {sid}", f))
            problems = {k: v for k, v in audit.items() if v}
            ok &= not problems
            per_slide.append({"slide": sid, "png": f.name, "problems": problems})
        missing = pg.evaluate("[...document.querySelectorAll('.missing')].map(e => e.dataset.slot)")
        b.close()
    srv.shutdown()
    sheet = pathlib.Path(args.sheet).resolve() if args.sheet else out / "contact_sheet.jpg"
    contact_sheet(shots, sheet)
    glob = {k: v for k, v in {"console_errors": watch.errors, "failed_requests": watch.failed, "external_requests": watch.external,
                               "font_errors": bad_fonts, "missing_slots": missing}.items() if v}
    ok &= not glob
    print(json.dumps({"deck": rel, "slides": len(shots), "contact_sheet": str(sheet), "fonts_loaded": loaded,
                      "problems": glob, "per_slide": [s for s in per_slide if s["problems"]]}, indent=1, ensure_ascii=False))
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="mode", required=True)
    a = sub.add_parser("page", help="render static promo / cover pages")
    a.add_argument("files", nargs="+")
    a.add_argument("--out-dir")
    a.add_argument("--size", help="WxH; default from <meta name=sa:canvas>")
    a.add_argument("--scale", type=float, default=1, help="device scale factor (2 for retina exports)")
    d = sub.add_parser("deck", help="print every slide of a canvas deck")
    d.add_argument("deck")
    d.add_argument("--root", help="directory to serve (must contain the deck and every file it links)")
    d.add_argument("--out")
    d.add_argument("--sheet")
    d.add_argument("--wait", type=int, default=500, help="ms to settle after each jump")
    d.add_argument("--scale", type=float, default=1)
    args = ap.parse_args()
    return run_page(args) if args.mode == "page" else run_deck(args)


if __name__ == "__main__":
    sys.exit(main())
