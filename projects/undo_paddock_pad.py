"""Undo the paddock pad (26 Sep): the shelters moved to the covered stalls, so the paddocks go back on their natural
ground (about 5 % fall, fine for turnout). Inside the pad's reach the ground returns to the existing surface, then the
roads and ditches that cross it are re-run over it in the replay order (roads, then ditches), mirroring applyPath and
dbShape in topo.html, writing only inside that reach. The natural water sink is left exactly as it is.

    python undo_paddock_pad.py  ->  centro-equino-2026-09-26-stalls16-nopad.json
"""
import json, math, os, numpy as np
from matplotlib.path import Path
from geo import GR, cs, W, H
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'centro-equino-2026-09-26-stalls16.json'); DST = SRC.replace('.json', '-nopad.json')
FT = .3048
d = json.load(open(SRC, encoding='utf-8'))
z = np.array(d['z'], float).reshape(H, W); base = np.array(d['base'], float).reshape(H, W); z0 = z.copy()
I, J = np.meshgrid(np.arange(W), np.arange(H)); XY = np.c_[I.ravel(), J.ravel()]

o = [s for s in d['strokes'] if s.get('name') == 'four paddocks'][0]; r = math.radians(o['rot']); F = np.array(o['foot'])
foot = np.c_[o['c'][0] + (F[:, 0] * math.cos(r) - F[:, 1] * math.sin(r)) / cs, o['c'][1] - (F[:, 0] * math.sin(r) + F[:, 1] * math.cos(r)) / cs]
ctr = foot.mean(0); grow = lambda P, k: ctr + (P - ctr) * (1 + k / np.hypot(*(P - ctr).T).mean())   # polygon pushed out ~k cells
reach = Path(grow(foot, 3.5)).contains_points(XY).reshape(H, W) & (np.abs(z - base) > .01)
sink = [s for s in d['strokes'] if s.get('name') == 'natural water sink']
if sink:
    P = np.array([p[:2] for p in sink[0]['pts']]); keep = Path(grow(P, 1.5)).contains_points(XY).reshape(H, W)
    print('sink cells kept as they are:', int((reach & keep).sum())); reach &= ~keep
write = reach.copy()
z[reach] = base[reach]

def sample(p, A=None):
    A = z if A is None else A
    i, j = min(int(p[0]), W - 2), min(int(p[1]), H - 2); fx, fy = p[0] - i, p[1] - j
    return A[j, i] * (1 - fx) * (1 - fy) + A[j, i + 1] * fx * (1 - fy) + A[j + 1, i] * (1 - fx) * fy + A[j + 1, i + 1] * fx * fy
def resample(pts, step):
    out = []
    for a, b in zip(pts, pts[1:]):
        n = max(1, int(math.dist(a, b) / step))
        out += [(a[0] + (b[0] - a[0]) * q / n, a[1] + (b[1] - a[1]) * q / n) for q in range(n)]
    return np.array(out + [tuple(pts[-1])])

# roads: applyPath over the restored ground, written only where the pad was (and a cell round it)
near = Path(grow(foot, 4.5)).contains_points(XY).reshape(H, W)
sl = 1 / float(d['sliders'].get('side', 3))
roads = [s for s in d['strokes'] if s.get('kind') == 'path' and Path(grow(foot, 4.5)).contains_points(np.array([p[:2] for p in s['pts']])).any()]
for s in roads:
    P = resample([p[:2] for p in s['pts']], .5); raw = np.array([sample(q) for q in P]); win = max(2, min(60, round(12 / (cs * .5))))
    prof = np.array([raw[max(0, i - win):i + win + 1].mean() for i in range(len(P))]); R = s.get('pw', 1.5) / 2 / cs; ph = s.get('ph', 0) or 0
    for j, i in zip(*np.where(near)):
        dd = np.hypot(P[:, 0] - i, P[:, 1] - j); k = dd.argmin(); dist = dd[k]; zt = prof[k] + ph; zc = z[j, i]
        if dist <= R: nz = zt
        else:
            e = (dist - R) * cs
            nz = zt - e * sl if zc < zt else zt + e * sl
            if (zc < zt and nz <= zc) or (zc >= zt and nz >= zc): continue
        z[j, i] = nz; write[j, i] = True
    print('road re-run:', s['name'])

# ditches: dbShape (no berm) over the new ground, same window
for rec in d['records']['ditches']:
    P0 = np.array([GR(*p) for p in rec['pts']])
    if not Path(grow(foot, 4.5)).contains_points(P0).any() and min(np.hypot(*(foot[None] - q).T).min() for q in P0) > 6: continue
    surf = np.where(write, z, base)   # never read a ditch's own dug bottom: natural ground outside what this script rebuilt
    P = resample([tuple(q) for q in P0], .25); g = np.array([sample(q, surf) for q in P]); Dq = np.r_[0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))] * cs
    if rec['bottom'] == 'level': bot = np.full(len(P), g.mean() - rec['depth'])
    elif rec['bottom'] == 'ground':
        win = max(1, round(3 / (.25 * cs))); bot = np.array([g[max(0, q - win):q + win + 1].mean() for q in range(len(P))]) - rec['depth']
    else:
        fall = float(rec['bottom']) / 100
        bot = (g[0] - fall * Dq if g[0] >= g[-1] else g[-1] - fall * (Dq[-1] - Dq)) - rec['depth']
    for j, i in zip(*np.where(write & near)):
        dd = np.hypot(P[:, 0] - i, P[:, 1] - j); q = dd.argmin(); dm = dd[q] * cs
        z[j, i] = min(z[j, i], bot[q] + max(0, dm - rec['bw'] / 2) / rec['side'])
    print('ditch re-dug:', rec['name'])

d['z'] = [round(float(q), 3) for q in z.flatten()]
# 26 Sep: the paddocks themselves go (fence + 4 gates), and Will's yellow-line sketch is no longer needed
gone = lambda n: n == 'four paddocks' or n.startswith('new covered stalls, yellow line') or ('gate' in n and n.endswith('paddock'))
d['strokes'] = [s_ for s_ in d['strokes'] if not gone(s_.get('name') or '')]
json.dump(d, open(DST, 'w', encoding='utf-8'))
dz = (z - z0) * cs * cs; before = (z0 - base) * cs * cs; after = (z - base) * cs * cs
tot = lambda a: (-a[a < 0].sum() / .7646, a[a > 0].sum() / .7646)
print('cells restored %d, touched %d' % (reach.sum(), write.sum()))
print('site earthwork before: cut %.0f fill %.0f yd3 | after: cut %.0f fill %.0f yd3' % (*tot(before), *tot(after)))
inside = Path(foot).contains_points(XY).reshape(H, W)
print('paddocks now: ground %.1f .. %.1f ft, largest leftover change inside %.1f ft' % (z[inside].min() / FT, z[inside].max() / FT, np.abs(z - base)[inside].max() / FT))
print('->', DST)
