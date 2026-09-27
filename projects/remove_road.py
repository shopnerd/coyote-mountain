"""Remove one road from the drawing and put its ground back (26 Sep: 'paddocks to cross-fence gate', unneeded once the
paddocks went; the gates stay). Cells the road reached go back to the existing ground, except where another road,
the natural sink or a pad owns them; then the ditches that cross it are re-dug (dbShape, no berm), and its culvert
marks go with it.

    python remove_road.py ["road name"]  ->  edits centro-equino-2026-09-26-stalls16-nopad.json in place
"""
import json, math, os, sys, numpy as np
from matplotlib.path import Path
from geo import GR, cs, W, H
HERE = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(HERE, 'centro-equino-2026-09-26-stalls16-nopad.json')
NAME = sys.argv[1] if len(sys.argv) > 1 else 'paddocks to cross-fence gate'
d = json.load(open(FILE, encoding='utf-8'))
z = np.array(d['z'], float).reshape(H, W); base = np.array(d['base'], float).reshape(H, W); z0 = z.copy()
I, J = np.meshgrid(np.arange(W), np.arange(H)); XY = np.c_[I.ravel(), J.ravel()]

def resample(pts, step):
    out = []
    for a, b in zip(pts, pts[1:]):
        n = max(1, int(math.dist(a, b) / step))
        out += [(a[0] + (b[0] - a[0]) * q / n, a[1] + (b[1] - a[1]) * q / n) for q in range(n)]
    return np.array(out + [tuple(pts[-1])])
def dist_to(P):                                          # distance (cells) from every node to a polyline
    return np.min(np.hypot(I[..., None] - P[:, 0], J[..., None] - P[:, 1]), axis=2)

road = [s for s in d['strokes'] if s.get('kind') == 'path' and s.get('name') == NAME][0]
RP = resample([p[:2] for p in road['pts']], .5); dr = dist_to(RP)
reach = (dr <= road['pw'] / 2 / cs + 3) & (np.abs(z - base) > .01)
for s in d['strokes']:                                   # other roads keep their ground
    if s.get('kind') == 'path' and s is not road:
        reach &= dist_to(resample([p[:2] for p in s['pts']], .5)) > s.get('pw', 1.5) / 2 / cs + 1.5
for s in d['strokes']:                                   # so do the sink and any closed outline marked as a pad
    if s.get('name') == 'natural water sink':
        reach &= ~Path(np.array([p[:2] for p in s['pts']])).contains_points(XY).reshape(H, W)
z[reach] = base[reach]

surf = np.where(reach, z, base)                          # never read a ditch's own dug bottom
def sample(p):
    i, j = min(int(p[0]), W - 2), min(int(p[1]), H - 2); fx, fy = p[0] - i, p[1] - j
    return surf[j, i] * (1 - fx) * (1 - fy) + surf[j, i + 1] * fx * (1 - fy) + surf[j + 1, i] * (1 - fx) * fy + surf[j + 1, i + 1] * fx * fy
near = dr <= road['pw'] / 2 / cs + 4
for rec in d['records']['ditches']:
    P = resample([tuple(GR(*p)) for p in rec['pts']], .25)
    if dist_to(P)[near].min() > 3: continue
    g = np.array([sample(q) for q in P]); Dq = np.r_[0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))] * cs
    if rec['bottom'] == 'level': bot = np.full(len(P), g.mean() - rec['depth'])
    elif rec['bottom'] == 'ground':
        win = max(1, round(3 / (.25 * cs))); bot = np.array([g[max(0, q - win):q + win + 1].mean() for q in range(len(P))]) - rec['depth']
    else:
        fall = float(rec['bottom']) / 100; bot = (g[0] - fall * Dq if g[0] >= g[-1] else g[-1] - fall * (Dq[-1] - Dq)) - rec['depth']
    for j, i in zip(*np.where(near & reach)):
        dd = np.hypot(P[:, 0] - i, P[:, 1] - j); q = dd.argmin()
        z[j, i] = min(z[j, i], bot[q] + max(0, dd[q] * cs - rec['bw'] / 2) / rec['side'])
    print('ditch re-dug:', rec['name'])

gone = [s.get('name') for s in d['strokes'] if s is road or (s.get('name') or '').endswith('under ' + NAME)]
d['strokes'] = [s for s in d['strokes'] if s is not road and not (s.get('name') or '').endswith('under ' + NAME)]
d['z'] = [round(float(q), 3) for q in z.flatten()]
json.dump(d, open(FILE, 'w', encoding='utf-8'))
tot = lambda a: (-a[a < 0].sum() * cs * cs / .7646, a[a > 0].sum() * cs * cs / .7646)
print('removed:', gone)
print('cells restored %d; site earthwork before cut %.0f fill %.0f | after cut %.0f fill %.0f yd3' % (reach.sum(), *tot(z0 - base), *tot(z - base)))
