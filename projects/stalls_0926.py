"""Covered stalls at the yellow line (9/26): 8 stalls 16x20 ft, 4 a side, 12 ft corridor.
Places the block along the line, reads the palms off the z18 photo, grades gently, draws two roof options.
    python stalls_0926.py  ->  scratchpad/stalls-options.png + numbers
"""
import json, math, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
from geo18 import mosaic, tile_xy
from geo import GR, cs, W, H
OUT = sys.argv[1] if len(sys.argv) > 1 else 'stalls-options.png'
FT = .3048
d = json.load(open('centro-equino-2026-09-26.json', encoding='utf-8'))
z = np.array(d['z']).reshape(H, W) / FT
M, (x0, y0) = mosaic(); G = M.mean(2)
PXFT = FT / (156543.03 * math.cos(math.radians(32)) / 2**18)
st = [(-116.7637927468709,31.99970749966619),(-116.7635094983617,31.99998532313917),(-116.7633790473066,31.99988684382775),(-116.7636714287398,31.99959200352455)]
LLp = [(la, lo) for lo, la in st]
def pix(la, lo): x, y = tile_xy(la, lo); return np.array([(x - x0) * 256, (y - y0) * 256])
P = [pix(*q) for q in LLp]; A, B, C, D = P
u = (B - A) / np.linalg.norm(B - A); v = (D - A) / np.linalg.norm(D - A)
def TS(t, s): return A + (u * t + v * s) * PXFT                    # outline frame (ft) -> photo px
def px2ll(p):                                                          # photo px -> lat, lon
    n = 2**18; X = p[0] / 256 + x0; Y = p[1] / 256 + y0
    lon = X / n * 360 - 180; lat = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * Y / n)))); return lat, lon
def zAt(t, s):
    gi, gj = GR(*px2ll(TS(t, s))); i, j = int(gi), int(gj); fx, fy = gi - i, gj - j
    return z[j,i]*(1-fx)*(1-fy)+z[j,i+1]*fx*(1-fy)+z[j+1,i]*(1-fx)*fy+z[j+1,i+1]*fx*fy

T0, L = 0, 64                    # block frame: t along the corridor 0-64 (4 stalls x 16 ft)
ANG, TC, SC = (float(x) for x in (sys.argv[2:5] if len(sys.argv) > 4 else (0, 42, 28)))   # turn (deg) and centre in the outline frame
S0, SD, CW = 0, 20, 12           # NW stalls s 0-20, corridor 20-32, SE stalls 32-52
def BT(bt, bs):                  # block frame -> outline frame
    a = math.radians(ANG); x, y = bt - 32, bs - 26
    return TC + x * math.cos(a) - y * math.sin(a), SC + x * math.sin(a) + y * math.cos(a)
def TB(t, s):
    a = math.radians(ANG); x, y = t - TC, s - SC
    return x * math.cos(a) + y * math.sin(a) + 32, -x * math.sin(a) + y * math.cos(a) + 26
TSo = None
cA, cB = S0 + SD, S0 + SD + CW
OV = 8                            # roof overhang onto each stall front

# palms: dark pixels on the photo, 1 ft grid
bg = np.median([G[int(TS(t, s)[1]), int(TS(t, s)[0])] for t in range(-40, 140, 3) for s in range(-10, 66, 3)])
palm = [(t, s) for t in range(-40, 140) for s in range(-12, 68) if G[int(TS(t, s)[1]), int(TS(t, s)[0])] < bg - 25]
def zone(t, s, opt):
    t, s = TB(t, s)
    if not (T0 <= t <= T0 + L and S0 <= s <= S0 + 2 * SD + CW): return 'outside'
    if cA <= s <= cB: return 'corridor, roofed' if opt == 'A' else 'corridor, open'
    if cA - OV <= s < cA or cB < s <= cB + OV: return 'stall front, under roof'
    return 'stall back, open sky'
for opt in 'AB':
    cnt = {}
    for q in palm: k = zone(*q, opt); cnt[k] = cnt.get(k, 0) + 1
    print(opt, {k: f'{v} ft2' for k, v in cnt.items()})

# grading: corridor follows the ground along its length, level across; stall floors fall at most 5 %
# away from / toward the corridor edge (natural grade where it is gentler). 1 ft cells.
cut = fill = 0; mx = 0
for t in range(T0, T0 + L):
    zc = np.mean([zAt(*BT(t + .5, s + .5)) for s in range(cA, cB)])
    for s in range(S0, S0 + 2 * SD + CW):
        g = zAt(*BT(t + .5, s + .5))
        if cA <= s < cB: dz = zc
        else:
            e = (cA - (s + .5)) if s < cA else ((s + .5) - cB)       # ft from the corridor edge
            nat = g - zc; lim = .05 * e
            dz = zc + max(-lim, min(lim, nat))
        h = dz - g; mx = max(mx, abs(h))
        if h > 0: fill += h
        else: cut -= h
print(f'grading: cut {cut/27:.0f} yd3, fill {fill/27:.0f} yd3, max {mx:.1f} ft')
zc0 = np.mean([zAt(*BT(T0 + 1, s)) for s in range(cA, cB)]); zc1 = np.mean([zAt(*BT(T0 + L - 1, s)) for s in range(cA, cB)])
print(f'corridor ground {zc0:.1f} (SW) -> {zc1:.1f} (NE), {abs(zc1-zc0)/L*100:.1f} % along; across the block {zAt(*BT(T0+32,S0)):.1f} -> {zAt(*BT(T0+32,S0+52)):.1f}')

# clearances to the main road and the round pen ring road (edges, ft)
def roadpx(name):
    s = [x for x in d['strokes'] if x.get('name') == name][0]; return s, [pix(*LLfromG(p[0], p[1])) for p in s['pts']]
from geo import LL as LLfromG
def clear(name):
    s, R = roadpx(name); hw = s.get('pw', 3.66) / 2 / FT
    best = 1e9
    for t in np.linspace(T0, T0 + L, 33):
        for sv in np.linspace(S0, S0 + 52, 27):
            if not (t in (T0, T0 + L) or sv in (S0, S0 + 52)): continue
            p = TS(*BT(t, sv)); best = min(best, min(np.linalg.norm(p - r) for r in R) / PXFT - hw)
    return best
for n in ('main road, north-east gate to south gate', 'round pen ring road', 'existing scrub-side road'):
    print(f'clear of {n}: {clear(n):.0f} ft')

# picture: two panels, north up
def panel(opt):
    cx, cy = TS(*BT(T0 + L / 2, 26)); r = 95
    box = (int(cx - r * 1.35), int(cy - r), int(cx + r * 1.35), int(cy + r)); K = 5
    im = Image.fromarray(M[box[1]:box[3], box[0]:box[2]]).resize(((box[2]-box[0]) * K, (box[3]-box[1]) * K), Image.LANCZOS).convert('RGBA')
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); dr = ImageDraw.Draw(ov)
    Q = lambda p: ((p[0] - box[0]) * K, (p[1] - box[1]) * K)
    poly = lambda pts, **kw: dr.polygon([Q(TS(*BT(*p))) for p in pts], **kw)
    rect = lambda t0, t1, s0, s1: [(t0, s0), (t1, s0), (t1, s1), (t0, s1)]
    for nm in ('main road, north-east gate to south gate', 'round pen ring road', 'existing scrub-side road', 'barn to cross-fence road'):
        s, R = roadpx(nm); dr.line([Q(p) for p in R], fill=(240, 235, 225, 150), width=int(s.get('pw', 3.66) / FT * PXFT * K))
    dr.line([Q(p) for p in P], fill=(255, 200, 0, 255), width=3)
    if opt == 'A': poly(rect(T0 - 2, T0 + L + 2, cA - OV, cB + OV), fill=(201, 107, 58, 120))
    else:
        poly(rect(T0 - 2, T0 + L + 2, cA - OV, cA), fill=(201, 107, 58, 120)); poly(rect(T0 - 2, T0 + L + 2, cB, cB + OV), fill=(201, 107, 58, 120))
    poly(rect(T0, T0 + L, S0, S0 + 52), outline=(255, 255, 255, 255), width=3)
    for k in range(1, 4):
        dr.line([Q(TS(*BT(T0 + 16 * k, S0))), Q(TS(*BT(T0 + 16 * k, cA)))], fill=(255, 255, 255, 255), width=2)
        dr.line([Q(TS(*BT(T0 + 16 * k, cB))), Q(TS(*BT(T0 + 16 * k, S0 + 52)))], fill=(255, 255, 255, 255), width=2)
    for s_ in (cA, cB): dr.line([Q(TS(*BT(T0, s_))), Q(TS(*BT(T0 + L, s_)))], fill=(255, 255, 255, 255), width=3)
    im = Image.alpha_composite(im, ov); dr = ImageDraw.Draw(im)
    try: f = ImageFont.truetype('consola.ttf', 26); f2 = ImageFont.truetype('consola.ttf', 20)
    except Exception: f = f2 = ImageFont.load_default()
    title = {'A': 'A  roofed corridor (Walker)', 'B': 'B  palm corridor, roofs over stall fronts'}[opt]
    dr.rectangle((0, 0, im.size[0], 40), fill=(240, 240, 236)); dr.text((14, 7), title, font=f, fill=(42, 42, 40))
    dr.text((14, im.size[1] - 30), 'north up · white = 8 stalls 16x20 + 12 ft corridor · orange = roof · yellow = your line', font=f2, fill=(255, 255, 255))
    return im
a, b = panel('A'), panel('B')
out = Image.new('RGB', (a.size[0] * 2 + 12, a.size[1]), (240, 240, 236)); out.paste(a, (0, 0)); out.paste(b, (a.size[0] + 12, 0)); out.save(OUT); print(OUT, out.size)
