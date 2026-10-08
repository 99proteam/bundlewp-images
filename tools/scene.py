"""Topic illustration generator (no text): a glowing hub icon with orbiting
topic icons joined by circuit lines. Free: Lucide icons (ISC licence) + code."""
import math, re, sys, json, random
import os
ICONS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "node_modules/lucide-static/icons/")

PALETTES = {
    "emerald": dict(bg1="#022c22", bg2="#064e3b", glow="#34d399", line="#6ee7b7", icon="#d1fae5", hub="#10b981"),
    "cyan":    dict(bg1="#020617", bg2="#0c2a4a", glow="#22d3ee", line="#67e8f9", icon="#cffafe", hub="#06b6d4"),
    "amber":   dict(bg1="#1c1003", bg2="#4a2504", glow="#fbbf24", line="#fcd34d", icon="#fef3c7", hub="#f59e0b"),
    "violet":  dict(bg1="#13072e", bg2="#2e1065", glow="#a78bfa", line="#c4b5fd", icon="#ede9fe", hub="#8b5cf6"),
    "rose":    dict(bg1="#1f0410", bg2="#4c0519", glow="#fb7185", line="#fda4af", icon="#ffe4e6", hub="#f43f5e"),
    "indigo":  dict(bg1="#0b0b2e", bg2="#1e1b6b", glow="#818cf8", line="#a5b4fc", icon="#e0e7ff", hub="#6366f1"),
}

def icon_inner(name):
    s = open(ICONS + name + ".svg").read()
    return re.search(r"<svg[^>]*>(.*)</svg>", s, re.S).group(1)

def icon(name, cx, cy, size, color, sw=2):
    k = size / 24
    return (f'<g transform="translate({cx - size/2:.1f},{cy - size/2:.1f}) scale({k:.3f})" fill="none" '
            f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{icon_inner(name)}</g>')

def build(hub, sats, pal, seed=1):
    p = PALETTES[pal]; rnd = random.Random(seed)
    W, H, cx, cy = 1200, 630, 600, 315
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
           '<defs>',
           f'<radialGradient id="bg" cx="50%" cy="50%" r="75%"><stop offset="0" stop-color="{p["bg2"]}"/><stop offset="1" stop-color="{p["bg1"]}"/></radialGradient>',
           f'<radialGradient id="glow" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{p["glow"]}" stop-opacity=".55"/><stop offset=".6" stop-color="{p["glow"]}" stop-opacity=".12"/><stop offset="1" stop-color="{p["glow"]}" stop-opacity="0"/></radialGradient>',
           '<filter id="blur"><feGaussianBlur stdDeviation="3"/></filter>',
           '</defs>', f'<rect width="{W}" height="{H}" fill="url(#bg)"/>']
    # dot grid
    for x in range(30, W, 40):
        for y in range(25, H, 40):
            out.append(f'<circle cx="{x}" cy="{y}" r="1.2" fill="{p["line"]}" opacity=".12"/>')
    # satellites on ellipse
    n = len(sats); pos = []
    for i, name in enumerate(sats):
        a = -math.pi/2 + 2*math.pi*i/n + 0.25
        x = cx + 400*math.cos(a); y = cy + 215*math.sin(a)
        pos.append((x, y, name))
    # circuit lines (L-shaped) hub -> satellite
    for x, y, _ in pos:
        midx = cx + (x-cx)*0.55
        d = f"M{cx},{cy} L{midx:.0f},{cy + (y-cy)*0.15:.0f} L{midx:.0f},{y:.0f} L{x:.0f},{y:.0f}"
        out.append(f'<path d="{d}" fill="none" stroke="{p["line"]}" stroke-width="2" opacity=".45"/>')
        out.append(f'<circle cx="{midx:.0f}" cy="{y:.0f}" r="4" fill="{p["glow"]}"/>')
    # extra decorative short traces
    for _ in range(14):
        x = rnd.randint(40, W-40); y = rnd.randint(30, H-30)
        if abs(x-cx) < 160 and abs(y-cy) < 140: continue
        L = rnd.randint(30, 80); d = rnd.choice([(L,0),(0,L),(L,L//2)])
        out.append(f'<path d="M{x},{y} l{d[0]},0 l0,{d[1]}" fill="none" stroke="{p["line"]}" stroke-width="1.5" opacity=".18"/>')
        out.append(f'<circle cx="{x+d[0]}" cy="{y+d[1]}" r="2.5" fill="{p["line"]}" opacity=".35"/>')
    # satellite badges (hexagons)
    for x, y, name in pos:
        r = 46
        pts = " ".join(f"{x + r*math.cos(math.pi/6 + k*math.pi/3):.1f},{y + r*math.sin(math.pi/6 + k*math.pi/3):.1f}" for k in range(6))
        out.append(f'<polygon points="{pts}" fill="{p["bg1"]}" stroke="{p["line"]}" stroke-width="2" opacity=".95"/>')
        out.append(icon(name, x, y, 40, p["icon"]))
    # hub glow + rings
    out.append(f'<circle cx="{cx}" cy="{cy}" r="190" fill="url(#glow)"/>')
    for r, o in ((128, .25), (108, .45)):
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{p["line"]}" stroke-width="2" stroke-dasharray="6 10" opacity="{o}"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="88" fill="{p["hub"]}" opacity=".9"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="88" fill="none" stroke="{p["icon"]}" stroke-width="3" opacity=".7"/>')
    out.append(icon(hub, cx, cy, 96, "#ffffff", 1.8))
    out.append('</svg>')
    return "\n".join(out)

if __name__ == "__main__":
    spec = json.loads(sys.argv[1])
    open(sys.argv[2], "w").write(build(**spec))
