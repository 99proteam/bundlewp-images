# Expense tracking: receipts flow into an expense dashboard on a laptop (categories donut, monthly bars, ledger).
from kit import Scene
s = Scene("mint", seed=4).background("both")
s.receipt(70, 150, 150, 220, rot=-10); s.receipt(150, 250, 150, 220, rot=6, accent=s.p["a3"])
s.arrow(320, 330, 420, 300, bend=30)
x, y, w, h = s.laptop(430, 95, 560, 360)
s.donut(x + 110, y + 120, 70, [40, 25, 20, 15])
s.bars(x + 230, y + 40, 270, 150, [.45, .7, .55, .85, .6, .4], [s.p["a1"], s.p["a2"]])
s.table(x + 20, y + 215, w - 40, 100, cols=4, rows=3, head=s.p["a1"], highlight=2)
s.badge("wallet", 1050, 140, 42, bg=s.p["a1"]); s.badge("credit-card", 1080, 470, 34, bg=s.p["a2"])
s.badge("piggy-bank", 360, 520, 34, bg=s.p["a3"]); s.sparkles(7)
