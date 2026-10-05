"""Generates the two synthetic screen recordings used by the example deck (no real footage). Needs Pillow and ffmpeg."""
import math, pathlib, subprocess, sys, tempfile
from PIL import Image, ImageDraw
out = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).parent; W, H, N = 960, 540, 60
def path(kind, t):
    if kind == "a":  # slow, wandering
        x = 80 + 800 * t; y = 300 + 120 * math.sin(t * 9) * (1 - t * .6)
    else:            # fast, settles
        x = 80 + 800 * min(1, t * 1.6); y = 300 - 150 * (1 - math.exp(-6 * min(1, t * 1.6))) + 10 * math.sin(t * 30) * math.exp(-5 * t)
    return x, y
for kind, trail in (("a", (170, 176, 170)), ("b", (88, 196, 120))):
    d = pathlib.Path(tempfile.mkdtemp(prefix=f"frames_{kind}_"))
    for i in range(N):
        t = i / (N - 1)
        im = Image.new("RGB", (W, H), (17, 19, 18)); g = ImageDraw.Draw(im)
        for gx in range(80, 900, 80): g.line([(gx, 60), (gx, 480)], fill=(32, 35, 33))
        for gy in range(60, 500, 70): g.line([(80, gy), (880, gy)], fill=(32, 35, 33))
        g.rectangle([0, 0, W, 34], fill=(26, 28, 27)); [g.ellipse([16 + k * 20, 12, 26 + k * 20, 22], fill=(60, 64, 62)) for k in range(3)]
        pts = [path(kind, s / 200 * t) for s in range(201)]
        g.line(pts, fill=trail, width=4, joint="curve")
        x, y = pts[-1]; g.ellipse([x - 9, y - 9, x + 9, y + 9], fill=(238, 240, 236))
        g.rectangle([80, 500, 80 + 800 * t, 506], fill=trail)
        im.save(d / f"f{i:03d}.png")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", "15", "-i", str(d / "f%03d.png"), "-c:v", "libvpx-vp9", "-crf", "38", "-b:v", "0", "-pix_fmt", "yuv420p", str(out / f"run_{kind}.webm")], check=True)
    Image.open(d / f"f{int(N*0.7):03d}.png").save(out / f"run_{kind}_poster.jpg", quality=86)
