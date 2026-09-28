"""Walker's bleachers in front of the trailer, facing the arena. 28 Sep: rebuilt to Walker's grid-paper sketch (deck + three curved fan sections); earlier (27 Sep, Will's top-view sketch): wooden stadium seating
that fans out from narrow to wide along the trailer's arena side, the wide end deep enough for a blanket and a picnic,
with a shade roof extended off the trailer over the wide half.

Built in the trailer's own frame (metres, x along the trailer -3.57..8.63, y across, the arena side is -y, z up from the
trailer's base) so it shares the trailer's placement in the drawing. The arena ring road passes 10-14 ft off that side,
so the wedge is sized to stop short of it (the sketch's full 20 ft wide end would need the road moved ~7 ft).

    python bleachers.py      ->  bleachers.obj (usemtl-tagged) and the stroke 'bleachers' in the three working drawings
"""
import json, math, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); FT = .3048
X0, X1, YS = -3.57, 8.63, -1.22            # trailer ends and its arena-side face
RISE, TREAD = 0.30, 0.75                   # per tier: rise 12 in (wide terrace steps to sit and picnic on)
DECK_D = 6 * FT                            # the flat top deck along the whole trailer (Walker's sketch, 28 Sep)
YD = YS - DECK_D                           # the deck's front edge
CLEAR = 3 * FT                             # 28 Sep (Will): full size, may run over the walking path round the arena; only the arena fence is a limit (3 ft clear)
V, F, MAT = [], [], []
def face(pts, m): i = len(V) + 1; V.extend(pts); F.append(tuple(range(i, i + len(pts)))); MAT.append(m)
def quad(a, b, c, d, m): face([a, b, c, d], m)
def prism(pts, z0, z1, m):                 # a vertical prism over a convex footprint pts (x, y)
    for (xa, ya), (xb, yb) in zip(pts, pts[1:] + pts[:1]): quad((xa, ya, z0), (xb, yb, z0), (xb, yb, z1), (xa, ya, z1), m)
    face([(x, y, z1) for x, y in pts], m); face([(x, y, z0) for x, y in pts[::-1]], m)
def beam(p0, p1, w, m, up=(0, 0, 1)):     # a square steel member between two points
    p0, p1 = np.array(p0, float), np.array(p1, float); d = p1 - p0; d /= np.linalg.norm(d)
    u = np.cross(d, up); u = u / np.linalg.norm(u) if np.linalg.norm(u) > 1e-6 else np.array([1., 0, 0]); v = np.cross(u, d)
    c = [tuple(p + (su * u + sv * v) * w / 2) for p in (p0, p1) for su, sv in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    for q in range(4): quad(c[q], c[(q + 1) % 4], c[4 + (q + 1) % 4], c[4 + q], m)
    quad(c[3], c[2], c[1], c[0], m); quad(c[4], c[5], c[6], c[7], m)

# Walker's sketch (28 Sep), measured off the grid paper: three curved fan sections ("spiral steps") below the deck, each a
# curved triangle whose straight edge the next one springs from. (along the 40 ft trailer from the X0 end, depth past the
# deck), ft. Curved edges bulge outward. Depth is scaled to fit the ring road; the along-trailer positions are kept.
BLADES = [((0.0, 0.0), (8.7, 11.7), (29.3, 0.0)),
          ((12.3, 10.0), (20.7, 13.0), (33.7, 0.0)),
          ((24.7, 12.7), (34.3, 15.7), (40.0, 0.0))]
def blade_pts(b, sc, n=10):                # the curved triangle as a polygon: arc P->Q (bulging outward), straight Q->R, R->P along... closing
    (px, pd), (qx, qd), (rx, rd) = b
    P = np.array([px, pd]); Q = np.array([qx, qd]); R = np.array([rx, rd])
    mid = (P + Q) / 2; nrm = np.array([-(Q - P)[1], (Q - P)[0]]); nrm /= np.linalg.norm(nrm)
    if np.dot(nrm, mid - (P + Q + R) / 3) < 0: nrm = -nrm                       # bulge away from the blade's middle
    ctrl = mid + nrm * .22 * np.linalg.norm(Q - P)
    arc = [(1 - t) ** 2 * P + 2 * (1 - t) * t * ctrl + t * t * Q for t in np.linspace(0, 1, n)]
    pts = arc + [R]
    L = X1 - X0
    return [(X0 + a * FT / 40 * (L / FT), YD - dd * FT * sc) for a, dd in pts]       # 40 ft of sketch = the trailer's length
# the ring road (and any road) in the trailer's frame, for the clearance
d0 = json.load(open(os.path.join(HERE, 'centro-equino-2026-09-26-stalls16-nopad.json'), encoding='utf-8'))
from geo import cs
tr0 = [q for q in d0['strokes'] if q.get('name') == 'trailer 8 x 40'][0]; rr = math.radians(tr0['rot']); c0 = tr0['c']
def local(i, j):
    a = (i - c0[0]) * cs; b = -(j - c0[1]) * cs
    return a * math.cos(rr) + b * math.sin(rr), -a * math.sin(rr) + b * math.cos(rr)
FENCE = []                                   # the arena fence's points in the trailer's frame
for s_ in d0['strokes']:
    if s_.get('name') == 'arena fence':
        T_ = np.array(s_['tris'] if not isinstance(s_['tris'], str) else json.loads(s_['tris']), float).reshape(-1, 3) * s_.get('sc', 1)
        r_ = math.radians(s_['rot']); gi = s_['c'][0] + (T_[:, 0] * math.cos(r_) - T_[:, 1] * math.sin(r_)) / cs; gj = s_['c'][1] - (T_[:, 0] * math.sin(r_) + T_[:, 1] * math.cos(r_)) / cs
        FENCE = np.array([local(i, j) for i, j in zip(gi[::7], gj[::7])])
def clearance(x, y): return float(np.min(np.hypot(FENCE[:, 0] - x, FENCE[:, 1] - y))) if len(FENCE) else 1e9
MIRROR = False
def place(b):                               # the sketch runs left->right; MIRROR puts its right end at X0
    return tuple(((40 - x) if MIRROR else x, dd) for x, dd in b)
def fit(b):                                 # the largest depth scale (<= 1) at which this section clears the road
    lo, hi = 0.0, 1.0
    for _ in range(25):
        mid = (lo + hi) / 2; lo, hi = (mid, hi) if all(clearance(x, y) >= CLEAR for x, y in blade_pts(place(b), mid)) else (lo, mid)
    return lo
best = None
for MIRROR in (False, True):                # keep the orientation of the sketch that gives the most seating
    scs = [fit(b) for b in BLADES]; area = sum(sc * max(q[1] for q in b) for sc, b in zip(scs, BLADES))
    if best is None or area > best[0]: best = (area, MIRROR, scs)
_, MIRROR, SCS = best
DMAX = max(max(q[1] for q in b) * FT * sc for b, sc in zip(BLADES, SCS))   # deepest seating, m
NT = 3                                                           # three terrace steps; the deck sits at the trailer floor, ~4 ft
H = RISE * (NT + 1)                                              # the deck is one rise above the top tier
def clip(poly, y_hi, y_lo):                                      # keep the part of a convex polygon with y_lo <= y <= y_hi
    def cut(pts, keep, yc):
        out = []
        for a, b in zip(pts, pts[1:] + pts[:1]):
            ia, ib = keep(a[1]), keep(b[1])
            if ia: out.append(a)
            if ia != ib: t = (yc - a[1]) / (b[1] - a[1]); out.append((a[0] + (b[0] - a[0]) * t, yc))
        return out
    pts = cut(poly, lambda y: y <= y_hi, y_hi)
    return cut(pts, lambda y: y >= y_lo, y_lo) if pts else []
# ---- the seating: each fan section cut into tiers by distance from the deck; plank tops on steel legs, open underneath ----
band = DMAX / NT if NT else 1
for b, sc in zip(BLADES, SCS):
    poly = blade_pts(place(b), sc)
    for t in range(NT):
        piece = clip(poly, YD - t * band + 1e-6, YD - (t + 1) * band - 1e-6)
        if len(piece) < 3: continue
        top = H - (t + 1) * RISE
        prism(piece, top - .09, top, 'wood')
        for k in range(0, len(piece), 3):                        # steel legs under the tier's corners
            x, y = piece[k]; beam((x, y, -.3), (x, y, top - .09), .07, 'steel')
# ---- the top deck along the trailer, on steel legs, with a front beam ----
prism([(X0, YS), (X1, YS), (X1, YD), (X0, YD)], H - .12, H, 'wood')
for x in np.linspace(X0 + .1, X1 - .1, 8):
    for y in (YS - .1, YD + .1): beam((x, y, -.3), (x, y, H - .12), .08, 'steel')
beam((X0, YD + .05, H - .2), (X1, YD + .05, H - .2), .1, 'steel')
# ---- shade roof the full length over the deck: from the trailer's top edge down to a front beam on four posts at the deck front ----
RX0, RX1, RZ0, RZ1 = X0 - .3, X1 + .3, 3.96, 3.2
fy = lambda x: YD + .15
for x in [X0 + .1 + (X1 - X0 - .2) * k / 3 for k in range(4)]:
    prism([(x - .07, fy(x) - .07), (x + .07, fy(x) - .07), (x + .07, fy(x) + .07), (x - .07, fy(x) + .07)], H, RZ1 - .02, 'steel')
beam((RX0, fy(RX0), RZ1 - .1), (RX1, fy(RX1), RZ1 - .1), .16, 'steel')
for dz in (0, .03): quad((RX0, YS, RZ0 + dz), (RX1, YS, RZ0 + dz), (RX1, fy(RX1) - .4, RZ1 + dz), (RX0, fy(RX0) - .4, RZ1 + dz), 'roof')
out = os.path.join(HERE, 'bleachers.obj')
with open(out, 'w', newline='\n') as f:
    f.write('# bleachers in front of the trailer (Walker sketch 28 Sep): 6 ft top deck along the 40 ft trailer, three curved fan sections of seating stepping down toward the arena, scaled to clear the ring road, shade roof over the deck\n# unit m\n# name bleachers\n')
    for v in V: f.write('v %.3f %.3f %.3f\n' % v)
    last = None
    for fc, m in zip(F, MAT):
        if m != last: f.write(f'usemtl {m}\n'); last = m
        f.write('f ' + ' '.join(map(str, fc)) + '\n')
# into the drawings, in the trailer's frame: same c, rot, lift; triangles in the order topo.html fans the faces
tris = []
for fc in F:
    for kk in range(1, len(fc) - 1): tris += list(V[fc[0] - 1]) + list(V[fc[kk] - 1]) + list(V[fc[kk + 1] - 1])
T = np.array(tris).reshape(-1, 3); zmin = T[:, 2].min()
for fn in ('centro-equino-2026-09-26.json', 'centro-equino-2026-09-26-stalls16.json', 'centro-equino-2026-09-26-stalls16-nopad.json'):
    p = os.path.join(HERE, fn); d = json.load(open(p, encoding='utf-8'))
    tr = [s for s in d['strokes'] if s.get('name') == 'trailer 8 x 40'][0]
    d['strokes'] = [s for s in d['strokes'] if s.get('name') != 'bleachers']
    Tz = T.copy(); Tz[:, 2] -= zmin
    xy = Tz[:, :2]; from itertools import product
    st = dict(color='ink', shape=False, kind='obj', c=list(tr['c']), name='bleachers', unit='m', rot=tr['rot'], sc=1, lift=float(tr.get('lift', 0) + zmin),
              tris=[round(float(v), 3) for v in Tz.flatten()], foot=[[float(xy[:, 0].min()), float(xy[:, 1].min())], [float(xy[:, 0].max()), float(xy[:, 1].min())], [float(xy[:, 0].max()), float(xy[:, 1].max())], [float(xy[:, 0].min()), float(xy[:, 1].max())]],
              h=float(Tz[:, 2].max()), w=1, a=1, dash=False, pts=[list(tr['pts'][0])])
    d['strokes'].append(st); json.dump(d, open(p, 'w', encoding='utf-8'))
print(out, len(F), 'faces; mirror', MIRROR, 'section scales', [round(v, 2) for v in SCS], 'section depths ft', [round(max(q[1] for q in b) * v, 1) for b, v in zip(BLADES, SCS)], '-> seating up to', round(DMAX / FT, 1), 'ft past the 6 ft deck;', NT, 'tiers; deck', round(H / FT, 1), 'ft high')
