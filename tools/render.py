"""Render a BundleWP featured image to WEBP.
Usage (from the repo root):
  cd tools && npm install --silent && cd ..
  python3 tools/render.py '{"hub":"wallet","sats":["receipt","calculator","coins","credit-card","piggy-bank","chart-column","calendar","landmark"],"pal":"emerald","seed":3}' blog/2026/10/my-post-slug.webp
hub = centre icon, sats = 6-8 surrounding icons (Lucide names, see https://lucide.dev/icons),
pal = emerald|cyan|amber|violet|rose|indigo, seed = any number (changes background lines).
Prints the file size and saves a PNG preview next to the WEBP (preview is git-ignored)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scene import build, ICONS
from playwright.sync_api import sync_playwright
from PIL import Image
spec = json.loads(sys.argv[1]); out = sys.argv[2]
missing = [n for n in [spec["hub"], *spec["sats"]] if not os.path.exists(ICONS + n + ".svg")]
if missing: sys.exit("Unknown icon names: " + ", ".join(missing))
svg = build(**spec)
os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
prev = out.rsplit(".", 1)[0] + ".preview.png"
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1200, "height": 630})
    pg.set_content('<html><body style="margin:0">' + svg + "</body></html>"); pg.screenshot(path=prev); b.close()
Image.open(prev).convert("RGB").save(out, "WEBP", quality=88, method=6)
print(out, os.path.getsize(out), "bytes; preview:", prev)
