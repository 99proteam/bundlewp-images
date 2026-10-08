# Google Maps lead extraction: a map with business pins -> a list of business contacts ready to reach out.
from kit import Scene
s = Scene("sand", seed=33).background("grid")
s.map_panel(70, 80, 520, 470, pins=[(330, 300), (200, 210), (460, 190), (240, 430), (480, 420)])
s.box(340, 150, 200, 92, r=12); s.badge("store", 380, 196, 24, bg=s.p["a3"], shadow=False); s.lines(416, 178, 104, 2, 20, 9); 
for i in range(5): s.icon("star", 420 + i * 16, 226, 12, s.p["a1"], 2.4)
s.arrow(605, 315, 680, 315, color=s.p["a1"])
for i, c in enumerate([s.p["a2"], s.p["a3"], s.p["a1"], s.p["a2"]]):
    s.contact_row(700, 110 + i * 92, 420, color=c)
s.badge("send", 1110, 520, 32, bg=s.p["a1"]); s.sparkles(6)
