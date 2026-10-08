# Product data extraction: an online store page of product cards -> scan -> clean spreadsheet rows.
from kit import Scene
s = Scene("midnight", seed=8).background("dots")
x, y, w, h = s.browser(60, 90, 480, 430)
for i in range(3):
    for j in range(2):
        s.product_card(x + 8 + i * 150, y + 6 + j * 182, 135, 172, accent=[s.p["a1"], s.p["a2"], s.p["a3"]][(i + j) % 3],
                       icon_name=["shirt", "headphones", "watch", "camera", "package", "shopping-bag"][i + 3 * j])
s.badge("scan-search", 600, 300, 46, bg=s.p["a1"], fg="#020617")
s.arrow(545, 300, 552, 300, dash=False); s.arrow(650, 300, 700, 300, color=s.p["a1"])
s.table(710, 150, 430, 300, cols=4, rows=6, head=s.p["a2"], highlight=3)
s.badge("tag", 1110, 120, 30, bg=s.p["a3"], fg="#020617"); s.badge("star", 760, 495, 28, bg=s.p["a2"], fg="#020617")
s.sparkles(9)
