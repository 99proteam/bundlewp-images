# One-time payment billing/POS software for shops: a till screen with an invoice, a printed receipt,
# barcode scanning, stock boxes and a card payment.
from kit import Scene
s = Scene("peach", seed=55).background("blobs")
x, y, w, h = s.pos_terminal(360, 70, 480, 400)
s.table(x, y, w * .62, h, cols=3, rows=5, head=s.p["a1"], highlight=2)
s.box(x + w * .66, y, w * .34, h * .5, fill=s.p["bg1"], r=10, shadow=False)
for r_ in range(3):
    for c in range(3):
        s.box(x + w * .66 + 8 + c * 32, y + h * .55 + r_ * 26, 26, 20, fill=s.p["bg2"], r=5, shadow=False)
s.circle(x + w * .83, y + h * .25, 26, s.p["a1"]); s.icon("receipt", x + w * .83, y + h * .25, 28, "#ffffff")
s.receipt(890, 170, 160, 260, rot=8, accent=s.p["a2"])
s.badge("scan-barcode", 250, 160, 40, bg=s.p["a2"])
for i in range(3):
    bx, by = 120 + i * 70 - (i // 2) * 35, 420 - (i // 2) * 60
    s.box(bx, by, 80, 70, fill="#d6a46c", r=8); s.pill(bx + 30, by, 20, 70, "#c08a52")
s.badge("credit-card", 1000, 500, 36, bg=s.p["a3"]); s.badge("infinity", 300, 300, 30, bg=s.p["a1"]); s.sparkles(6)
