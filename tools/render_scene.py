"""Render a scene script to a WEBP featured image.
Usage (repo root): python3 tools/render_scene.py tools/scenes/<slug>.py blog/<yyyy>/<mm>/<slug>.webp
A scene script imports Scene from kit, draws into a variable named `s`. Saves <out>.preview.png too."""
import sys, os, runpy
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
from playwright.sync_api import sync_playwright
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
s = runpy.run_path(src)["s"]; svg = s.svg()
os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
prev = out.rsplit(".", 1)[0] + ".preview.png"
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1200, "height": 630})
    pg.set_content('<html><body style="margin:0">' + svg + "</body></html>"); pg.screenshot(path=prev); b.close()
Image.open(prev).convert("RGB").save(out, "WEBP", quality=88, method=6)
print(out, os.path.getsize(out), "bytes; preview:", prev)
