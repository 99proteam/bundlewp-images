"""BundleWP illustration kit: building blocks for content-specific featured images.
Everything is plain SVG drawn with code + free Lucide icons (ISC licence). No AI.

Compose a scene per post (see scenes/*.py for examples), then render with render_svg.py.
Canvas is 1200x630. Keep the main subject inside x 120-1080, y 60-570.
Never put words/numbers in the image (the blog card already shows the title).
"""
import os, re, math, random

ICONS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "node_modules/lucide-static/icons/")
W, H = 1200, 630

# ---------- palettes (dark and light, so cards don't all look alike) ----------
PAL = {
    # name: bg1, bg2, surface, line(soft), ink(main shapes), a1, a2, a3 (accents), dark?
    "mint":     dict(bg1="#ecfdf5", bg2="#d1fae5", surf="#ffffff", soft="#e2e8f0", ink="#0f172a", a1="#10b981", a2="#0ea5e9", a3="#f59e0b", dark=False),
    "sky":      dict(bg1="#eff6ff", bg2="#dbeafe", surf="#ffffff", soft="#e2e8f0", ink="#0f172a", a1="#2563eb", a2="#7c3aed", a3="#f97316", dark=False),
    "peach":    dict(bg1="#fff7ed", bg2="#ffe4e6", surf="#ffffff", soft="#e7e5e4", ink="#1c1917", a1="#f43f5e", a2="#f97316", a3="#14b8a6", dark=False),
    "lilac":    dict(bg1="#f5f3ff", bg2="#ede9fe", surf="#ffffff", soft="#e5e7eb", ink="#1e1b4b", a1="#7c3aed", a2="#ec4899", a3="#10b981", dark=False),
    "sand":     dict(bg1="#fefce8", bg2="#fef3c7", surf="#ffffff", soft="#e7e5e4", ink="#1c1917", a1="#d97706", a2="#2563eb", a3="#e11d48", dark=False),
    "midnight": dict(bg1="#020617", bg2="#0f2a4a", surf="#0f172a", soft="#1e293b", ink="#e2e8f0", a1="#22d3ee", a2="#a78bfa", a3="#34d399", dark=True),
    "forest":   dict(bg1="#022c22", bg2="#064e3b", surf="#053b2f", soft="#0b5a46", ink="#d1fae5", a1="#34d399", a2="#fbbf24", a3="#60a5fa", dark=True),
    "plum":     dict(bg1="#1e0b2e", bg2="#3b0764", surf="#2a1145", soft="#43206b", ink="#f3e8ff", a1="#c084fc", a2="#f472b6", a3="#38bdf8", dark=True),
    "ember":    dict(bg1="#1c0a03", bg2="#431407", surf="#2b1206", soft="#5a2310", ink="#ffedd5", a1="#fb923c", a2="#facc15", a3="#f43f5e", dark=True),
}

def _icon_inner(name):
    s = open(ICONS + name + ".svg").read()
    return re.search(r"<svg[^>]*>(.*)</svg>", s, re.S).group(1)

def icon(name, cx, cy, size, color, sw=2):
    k = size / 24
    return (f'<g transform="translate({cx-size/2:.1f},{cy-size/2:.1f}) scale({k:.3f})" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{_icon_inner(name)}</g>')

class Scene:
    def __init__(self, pal, seed=1):
        self.p = PAL[pal]; self.r = random.Random(seed); self.parts = []; self.defs = []
        self._shadow = False
    def add(self, s): self.parts.append(s); return self

    # ---------- background ----------
    def background(self, style="blobs"):
        p = self.p
        self.defs.append(f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{p["bg1"]}"/><stop offset="1" stop-color="{p["bg2"]}"/></linearGradient>')
        self.add(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
        if style in ("blobs", "both"):
            for _ in range(3):
                x, y, rr = self.r.randint(0, W), self.r.randint(0, H), self.r.randint(140, 260)
                c = self.r.choice([p["a1"], p["a2"], p["a3"]])
                self.add(f'<circle cx="{x}" cy="{y}" r="{rr}" fill="{c}" opacity="{.10 if not p["dark"] else .12}"/>')
        if style in ("grid", "both"):
            for x in range(0, W, 48):
                self.add(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="{p["ink"]}" opacity=".04"/>')
            for y in range(0, H, 48):
                self.add(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{p["ink"]}" opacity=".04"/>')
        if style == "dots":
            for x in range(24, W, 36):
                for y in range(24, H, 36):
                    self.add(f'<circle cx="{x}" cy="{y}" r="1.4" fill="{p["ink"]}" opacity=".10"/>')
        return self

    def _sh(self):
        if not self._shadow:
            self.defs.append('<filter id="sh" x="-50%" y="-50%" width="200%" height="200%"><feDropShadow dx="0" dy="10" stdDeviation="14" flood-color="#000" flood-opacity=".18"/></filter>')
            self._shadow = True
        return 'filter="url(#sh)"'

    # ---------- primitives ----------
    def box(self, x, y, w, h, fill=None, r=14, stroke=None, shadow=True, opacity=1):
        fill = fill or self.p["surf"]; st = f' stroke="{stroke}" stroke-width="2"' if stroke else ""
        return self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{st} opacity="{opacity}" {self._sh() if shadow else ""}/>')

    def lines(self, x, y, w, n=3, gap=18, h=9, color=None, widths=None):
        color = color or self.p["soft"]
        for i in range(n):
            ww = w * (widths[i % len(widths)] if widths else (1 if i % 3 == 0 else (0.75 if i % 3 == 1 else 0.55)))
            self.add(f'<rect x="{x}" y="{y+i*gap}" width="{ww:.0f}" height="{h}" rx="{h/2}" fill="{color}"/>')
        return self

    def pill(self, x, y, w, h, color, opacity=1):
        return self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{color}" opacity="{opacity}"/>')

    def circle(self, cx, cy, r, color, opacity=1, stroke=None):
        st = f' stroke="{stroke}" stroke-width="3"' if stroke else ""
        return self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" opacity="{opacity}"{st}/>')

    def icon(self, name, cx, cy, size=40, color=None, sw=2):
        return self.add(icon(name, cx, cy, size, color or self.p["ink"], sw))

    def badge(self, name, cx, cy, r=34, bg=None, fg="#ffffff", shadow=True):
        bg = bg or self.p["a1"]
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{bg}" {self._sh() if shadow else ""}/>')
        return self.icon(name, cx, cy, r * 1.05, fg)

    def arrow(self, x1, y1, x2, y2, color=None, bend=0, dash=True, width=4):
        color = color or self.p["a1"]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - bend
        ang = math.atan2(y2 - my, x2 - mx); L = 16
        hx1, hy1 = x2 - L*math.cos(ang - .45), y2 - L*math.sin(ang - .45)
        hx2, hy2 = x2 - L*math.cos(ang + .45), y2 - L*math.sin(ang + .45)
        d = ' stroke-dasharray="10 10"' if dash else ""
        self.add(f'<path d="M{x1},{y1} Q{mx:.0f},{my:.0f} {x2},{y2}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round"{d}/>')
        return self.add(f'<path d="M{hx1:.0f},{hy1:.0f} L{x2},{y2} L{hx2:.0f},{hy2:.0f}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>')

    def sparkles(self, n=8, area=(80, 60, 1120, 570), colors=None):
        colors = colors or [self.p["a1"], self.p["a2"], self.p["a3"]]
        for _ in range(n):
            x, y = self.r.randint(area[0], area[2]), self.r.randint(area[1], area[3]); c = self.r.choice(colors); s = self.r.randint(5, 10)
            self.add(f'<path d="M{x},{y-s} L{x+s*.3},{y-s*.3} L{x+s},{y} L{x+s*.3},{y+s*.3} L{x},{y+s} L{x-s*.3},{y+s*.3} L{x-s},{y} L{x-s*.3},{y-s*.3}Z" fill="{c}" opacity=".7"/>')
        return self

    # ---------- composite objects ----------
    def browser(self, x, y, w, h, bar=None):
        p = self.p; bar = bar or (p["soft"])
        self.box(x, y, w, h)
        self.add(f'<path d="M{x},{y+14} a14,14 0 0 1 14,-14 h{w-28} a14,14 0 0 1 14,14 v24 h{-w} z" fill="{bar}"/>')
        for i, c in enumerate(("#f87171", "#fbbf24", "#34d399")):
            self.circle(x + 22 + i*18, y + 19, 6, c)
        self.pill(x + 90, y + 12, min(260, w - 120), 14, p["surf"], .9)
        return (x + 18, y + 54, w - 36, h - 70)   # inner content area

    def laptop(self, x, y, w, h):
        p = self.p
        self.box(x, y, w, h, fill=p["ink"] if not p["dark"] else "#0b1220", r=16)
        inner = (x + 14, y + 14, w - 28, h - 28)
        self.box(*inner, fill=p["surf"], r=8, shadow=False)
        self.add(f'<path d="M{x-40},{y+h} h{w+80} l-24,22 h{-(w+32)} z" fill="{p["soft"] if not p["dark"] else "#334155"}" {self._sh()}/>')
        return inner

    def phone(self, x, y, w=150, h=290):
        p = self.p
        self.box(x, y, w, h, fill="#111827", r=26)
        self.box(x + 9, y + 9, w - 18, h - 18, fill=p["surf"], r=20, shadow=False)
        self.pill(x + w/2 - 22, y + 16, 44, 8, "#111827")
        return (x + 20, y + 36, w - 40, h - 56)

    def bars(self, x, y, w, h, values, colors=None, gap=0.35):
        colors = colors or [self.p["a1"], self.p["a2"], self.p["a3"]]
        n = len(values); bw = w / (n + (n - 1) * gap)
        for i, v in enumerate(values):
            bh = h * v; bx = x + i * bw * (1 + gap)
            self.add(f'<rect x="{bx:.0f}" y="{y+h-bh:.0f}" width="{bw:.0f}" height="{bh:.0f}" rx="5" fill="{colors[i % len(colors)]}"/>')
        return self

    def line_chart(self, x, y, w, h, values, color=None, fill=True):
        color = color or self.p["a1"]; n = len(values)
        pts = [(x + w * i / (n - 1), y + h - h * v) for i, v in enumerate(values)]
        d = "M" + " L".join(f"{a:.0f},{b:.0f}" for a, b in pts)
        if fill: self.add(f'<path d="{d} L{x+w},{y+h} L{x},{y+h} Z" fill="{color}" opacity=".15"/>')
        self.add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
        a, b = pts[-1]; return self.circle(a, b, 8, color, stroke=self.p["surf"])

    def donut(self, cx, cy, r, parts, colors=None, width=26):
        colors = colors or [self.p["a1"], self.p["a2"], self.p["a3"], self.p["soft"]]
        tot = sum(parts); a0 = -math.pi / 2; C = 2 * math.pi * r
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{self.p["soft"]}" stroke-width="{width}"/>')
        off = 0
        for i, v in enumerate(parts):
            L = C * v / tot
            self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{colors[i % len(colors)]}" stroke-width="{width}" '
                     f'stroke-dasharray="{L-4:.1f} {C-L+4:.1f}" stroke-dashoffset="{-off:.1f}" transform="rotate(-90 {cx} {cy})"/>')
            off += L
        return self

    def table(self, x, y, w, h, cols=4, rows=5, head=None, highlight=None):
        p = self.p; head = head or p["a1"]; rh = h / rows; cw = w / cols
        self.box(x, y, w, h, r=10)
        self.add(f'<path d="M{x},{y+10} a10,10 0 0 1 10,-10 h{w-20} a10,10 0 0 1 10,10 v{rh-10} h{-w} z" fill="{head}"/>')
        for c in range(cols):
            self.pill(x + c*cw + 14, y + rh/2 - 5, cw * .55, 10, "#ffffff", .85)
        for r_ in range(1, rows):
            if highlight == r_:
                self.add(f'<rect x="{x+4}" y="{y+r_*rh+3}" width="{w-8}" height="{rh-6}" rx="6" fill="{p["a3"]}" opacity=".18"/>')
            self.add(f'<line x1="{x}" y1="{y+r_*rh}" x2="{x+w}" y2="{y+r_*rh}" stroke="{p["soft"]}" stroke-width="2"/>')
            for c in range(cols):
                ww = cw * self.r.choice([.35, .5, .62])
                self.pill(x + c*cw + 14, y + r_*rh + rh/2 - 5, ww, 10, p["soft"] if not p["dark"] else "#334155")
        for c in range(1, cols):
            self.add(f'<line x1="{x+c*cw}" y1="{y+rh}" x2="{x+c*cw}" y2="{y+h}" stroke="{p["soft"]}" stroke-width="2"/>')
        return self

    def receipt(self, x, y, w=150, h=220, rot=0, accent=None):
        p = self.p; accent = accent or p["a1"]
        n = 8; step = w / n
        zig = "".join(f" l{-step/2:.1f},10 l{-step/2:.1f},-10" for _ in range(n))
        g = (f'<g transform="rotate({rot} {x+w/2} {y+h/2})">'
             f'<path d="M{x},{y} h{w} v{h}{zig} z" fill="{p["surf"]}" {self._sh()}/>')
        inner = ""
        inner += f'<rect x="{x+w/2-26}" y="{y+18}" width="52" height="10" rx="5" fill="{accent}"/>'
        for i in range(5):
            inner += f'<rect x="{x+16}" y="{y+46+i*24}" width="{w*0.4:.0f}" height="8" rx="4" fill="{p["soft"]}"/>'
            inner += f'<rect x="{x+w-16-w*0.2:.0f}" y="{y+46+i*24}" width="{w*0.2:.0f}" height="8" rx="4" fill="{p["soft"]}"/>'
        inner += f'<rect x="{x+16}" y="{y+h-36}" width="{w-32}" height="12" rx="6" fill="{accent}" opacity=".85"/>'
        return self.add(g + inner + "</g>")

    def document(self, x, y, w=200, h=260, accent=None, rot=0):
        p = self.p; accent = accent or p["a2"]
        self.add(f'<g transform="rotate({rot} {x+w/2} {y+h/2})">')
        self.box(x, y, w, h, r=12)
        self.pill(x + 20, y + 22, w * .4, 14, accent)
        self.lines(x + 20, y + 56, w - 40, 6, 22)
        self.add(f'<rect x="{x+w-20-w*.38:.0f}" y="{y+h-48}" width="{w*.38:.0f}" height="24" rx="8" fill="{accent}" opacity=".85"/>')
        return self.add("</g>")

    def product_card(self, x, y, w=150, h=190, accent=None, icon_name="package"):
        p = self.p; accent = accent or p["a2"]
        self.box(x, y, w, h, r=12)
        self.add(f'<rect x="{x+10}" y="{y+10}" width="{w-20}" height="{h*.48:.0f}" rx="8" fill="{accent}" opacity=".16"/>')
        self.icon(icon_name, x + w/2, y + 10 + h*.24, h*.24, accent)
        self.lines(x + 14, y + h*.62, w - 28, 2, 16, 8)
        for i in range(5):
            self.icon("star", x + 18 + i*13, y + h - 22, 11, p["a3"], 2.4)
        return self.pill(x + w - 44, y + h - 30, 32, 16, accent)

    def map_panel(self, x, y, w, h, pins=(), accent=None):
        p = self.p; accent = accent or p["a3"]
        self.box(x, y, w, h, fill="#e8f0e3" if not p["dark"] else "#14231c", r=16)
        clip = f"mapclip{len(self.defs)}"
        self.defs.append(f'<clipPath id="{clip}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16"/></clipPath>')
        g = f'<g clip-path="url(#{clip})">'
        g += f'<path d="M{x-20},{y+h*.65} C{x+w*.3},{y+h*.55} {x+w*.5},{y+h*.95} {x+w+20},{y+h*.8}" stroke="#93c5fd" stroke-width="22" fill="none" opacity=".8"/>'
        for i in range(1, 5):
            g += f'<line x1="{x+w*i/5}" y1="{y-10}" x2="{x+w*i/5 + 40}" y2="{y+h+10}" stroke="#ffffff" stroke-width="{10 if i%2 else 6}" opacity=".9"/>'
        for i in range(1, 4):
            g += f'<line x1="{x-10}" y1="{y+h*i/4}" x2="{x+w+10}" y2="{y+h*i/4 - 30}" stroke="#ffffff" stroke-width="{9 if i==2 else 5}" opacity=".9"/>'
        for _ in range(7):
            bx, by = self.r.randint(x + 10, x + w - 70), self.r.randint(y + 10, y + h - 60)
            g += f'<rect x="{bx}" y="{by}" width="{self.r.randint(30,60)}" height="{self.r.randint(24,44)}" rx="6" fill="#cfe3c4" opacity=".9"/>'
        self.add(g + "</g>")
        for i, (px, py) in enumerate(pins):
            self.pin(px, py, accent if i == 0 else p["a1"], big=(i == 0))
        return self

    def pin(self, x, y, color, big=False):
        s = 1.5 if big else 1.0
        self.add(f'<g transform="translate({x},{y}) scale({s})" {self._sh()}><path d="M0,0 C-14,-18 -18,-24 -18,-34 a18,18 0 1 1 36,0 c0,10 -4,16 -18,34z" fill="{color}"/>'
                 f'<circle cx="0" cy="-34" r="7" fill="#ffffff"/></g>')
        return self

    def person(self, cx, cy, r=26, color=None):
        color = color or self.p["a2"]
        self.circle(cx, cy, r, color, .18)
        self.circle(cx, cy - r*.25, r*.36, color)
        return self.add(f'<path d="M{cx-r*.62:.0f},{cy+r*.62:.0f} a{r*.62:.0f},{r*.5:.0f} 0 0 1 {r*1.24:.0f},0 z" fill="{color}"/>')

    def contact_row(self, x, y, w, color=None, icons=("phone", "mail")):
        p = self.p; color = color or p["a2"]
        self.box(x, y, w, 62, r=12)
        self.person(x + 34, y + 31, 22, color)
        self.lines(x + 66, y + 18, w * .42, 2, 18, 9, widths=(1, .65))
        for i, n in enumerate(icons):
            self.badge(n, x + w - 30 - i*44, y + 31, 16, bg=color, shadow=False)
        return self

    def pos_terminal(self, x, y, w=320, h=230):
        p = self.p
        scr = (x, y, w, h * .78)
        self.box(*scr, fill="#111827", r=16)
        self.box(x + 12, y + 12, w - 24, h * .78 - 24, fill=p["surf"], r=8, shadow=False)
        self.add(f'<path d="M{x+w/2-30},{y+h*.78} h60 l18,{h*.18} h-96 z" fill="#374151"/>')
        self.add(f'<rect x="{x+w/2-90}" y="{y+h*.96}" width="180" height="16" rx="8" fill="#1f2937"/>')
        return (x + 24, y + 24, w - 48, h * .78 - 48)

    def gear(self, cx, cy, r, color=None, teeth=8):
        color = color or self.p["a2"]; pts = []
        for i in range(teeth * 2):
            a = math.pi * i / teeth; rr = r if i % 2 == 0 else r * .78
            pts.append(f"{cx + rr*math.cos(a):.1f},{cy + rr*math.sin(a):.1f}")
        self.add(f'<polygon points="{" ".join(pts)}" fill="{color}"/>')
        return self.circle(cx, cy, r * .35, self.p["surf"])

    def svg(self):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
                f'<defs>{"".join(self.defs)}</defs>' + "".join(self.parts) + "</svg>")
