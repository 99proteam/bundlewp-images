# Calculator website on WordPress: a website full of calculator tools, plus the mobile view.
from kit import Scene
s = Scene("lilac", seed=21).background("blobs")
x, y, w, h = s.browser(90, 70, 720, 480)
s.pill(x, y + 4, 180, 22, s.p["a1"]); s.pill(x + w - 260, y + 8, 60, 12, s.p["soft"]); s.pill(x + w - 180, y + 8, 60, 12, s.p["soft"]); s.pill(x + w - 100, y + 8, 60, 12, s.p["soft"])
tools = ["calculator", "percent", "piggy-bank", "landmark", "chart-line", "coins", "house", "car"]
cols = [s.p["a1"], s.p["a2"], s.p["a3"]]
for i, t in enumerate(tools):
    cx, cy = x + 10 + (i % 4) * 166, y + 60 + (i // 4) * 170
    s.box(cx, cy, 148, 150, r=14)
    s.badge(t, cx + 74, cy + 58, 32, bg=cols[i % 3], shadow=False)
    s.lines(cx + 24, cy + 108, 100, 2, 16, 8, widths=(1, .6))
px, py, pw, ph = s.phone(890, 120, 190, 380)
s.box(px, py, pw, 60, fill=s.p["a1"], r=10, shadow=False)
for r_ in range(4):
    for c in range(3):
        s.box(px + c * 52, py + 76 + r_ * 52, 44, 44, fill=s.p["bg2"], r=10, shadow=False)
s.badge("wordpress" if False else "globe", 850, 90, 30, bg=s.p["a2"]); s.sparkles(6)
