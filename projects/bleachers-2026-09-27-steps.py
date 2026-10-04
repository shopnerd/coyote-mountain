"""Walker's bleachers in front of the trailer, facing the arena (27 Sep, Will's top-view sketch): wooden stadium seating
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
TIERS = 4
DEEP_WIDE, DEEP_NARROW = 1.0, 0.61         # tier depth at the wide (x0) end and the narrow (x1) end, m: 3.3 ft and 2 ft
RISE = 0.45                                # per tier, m (18 in)
V, F, MAT = [], [], []
def quad(a, b, c, d, m):
    i = len(V) + 1; V.extend([a, b, c, d]); F.append((i, i + 1, i + 2, i + 3)); MAT.append(m)
def prism(pts, z0, z1, m):                 # a vertical prism over a quadrilateral footprint pts (x, y)
    for (xa, ya), (xb, yb) in zip(pts, pts[1:] + pts[:1]): quad((xa, ya, z0), (xb, yb, z0), (xb, yb, z1), (xa, ya, z1), m)
    quad(*[(x, y, z1) for x, y in pts], m); quad(*[(x, y, z0) for x, y in pts[::-1]], m)
def line_y(k, x):                          # the k-th fan line: straight from the narrow end to the wide end
    t = (X1 - x) / (X1 - X0); return YS - k * (DEEP_NARROW + (DEEP_WIDE - DEEP_NARROW) * t)
def beam(p0, p1, w, m, up=(0, 0, 1)):     # a square steel member between two points
    p0, p1 = np.array(p0, float), np.array(p1, float); d = p1 - p0; d /= np.linalg.norm(d)
    u = np.cross(d, up); u = u / np.linalg.norm(u) if np.linalg.norm(u) > 1e-6 else np.array([1., 0, 0]); v = np.cross(u, d)
    c = [tuple(p + (su * u + sv * v) * w / 2) for p in (p0, p1) for su, sv in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    for q in range(4): quad(c[q], c[(q + 1) % 4], c[4 + (q + 1) % 4], c[4 + q], m)
    quad(c[3], c[2], c[1], c[0], m); quad(c[4], c[5], c[6], c[7], m)
def depth(x): return line_y(0, x) - line_y(1, x)
def board(k, a, b, z, x0=X0, x1=X1):       # a plank along fan line k, from a to b metres out from it (numbers, or functions of the row depth), top at z
    f = lambda o, x: o(depth(x)) if callable(o) else o
    prism([(x0, line_y(k, x0) - f(a, x0)), (x1, line_y(k, x1) - f(a, x1)), (x1, line_y(k, x1) - f(b, x1)), (x0, line_y(k, x0) - f(b, x0))], z - .04, z, 'wood')
SEAT, FOOT = (.06, .36), (.40, None)       # seat: two planks at the back of each row; footboard: planks across the front, one rise lower
FR = np.linspace(X0 + .15, X1 - .15, 6)    # steel frames across the tiers
for k in range(TIERS):                     # row 0 against the trailer is the highest
    top = RISE * (TIERS - k)
    board(k, .06, .20, top); board(k, .22, .36, top)
    if k < TIERS - 1:                      # footboards (the lowest row puts its feet on the ground)
        for q in range(2): board(k, lambda D, q=q: .40 + (D - .43) * q / 2, lambda D, q=q: .40 + (D - .43) * (q + 1) / 2 - .015, top - RISE)
for x in FR:
    yb, yf = line_y(0, x), line_y(TIERS, x)
    beam((x, yf + .05, 0), (x, yb - .05, RISE * TIERS - .06), .1, 'steel')          # the raking stringer
    for k in range(TIERS):
        top = RISE * (TIERS - k); y0 = line_y(k, x)
        beam((x, y0 - .03, -.3), (x, y0 - .03, top - .04), .07, 'steel')            # seat post
        beam((x, y0 - .02, top - .07), (x, y0 - .38, top - .07), .06, 'steel', (1, 0, 0))   # seat bearer
        if k < TIERS - 1:
            beam((x, y0 - .38, top - RISE - .07), (x, line_y(k + 1, x) + .02, top - RISE - .07), .06, 'steel', (1, 0, 0))   # footboard bearer
for k in range(TIERS):                     # long rails tying the frames at each seat
    top = RISE * (TIERS - k); beam((X0 + .1, line_y(k, X0 + .1) - .03, top - .12), (X1 - .1, line_y(k, X1 - .1) - .03, top - .12), .05, 'steel', (0, 0, 1))
# open steps at the narrow end: plank treads on two steel stringers
for k in range(TIERS):
    top = RISE * (k + 1); ya = line_y(TIERS - 1 - k, X1)
    prism([(X1 + .05, ya), (X1 + .5, ya), (X1 + .5, ya - .3), (X1 + .05, ya - .3)], top - .04, top, 'wood')
for xx in (X1 + .08, X1 + .47):
    beam((xx, line_y(TIERS, X1) + .05, 0), (xx, line_y(0, X1) - .1, RISE * TIERS - .05), .07, 'steel', (1, 0, 0))
# shade roof off the trailer over the wide half: from the trailer's top edge down to three posts
RX0, RX1, RY, RZ0, RZ1 = X0 - .3, 3.2, line_y(TIERS, X0) + .3, 3.96, 3.2
for x in (X0 + .1, (X0 + RX1) / 2, RX1 - .1):
    prism([(x - .07, RY - .07), (x + .07, RY - .07), (x + .07, RY + .07), (x - .07, RY + .07)], -0.4, RZ1 - .02, 'steel')
prism([(RX0, RY - .08), (RX1, RY - .08), (RX1, RY + .08), (RX0, RY + .08)], RZ1 - .18, RZ1 - .02, 'steel')   # beam
for dz in (0, .03): quad((RX0, YS, RZ0 + dz), (RX1, YS, RZ0 + dz), (RX1, RY - .3, RZ1 + dz), (RX0, RY - .3, RZ1 + dz), 'roof')
out = os.path.join(HERE, 'bleachers.obj')
with open(out, 'w', newline='\n') as f:
    f.write('# bleachers in front of the trailer, facing the arena: open steel frames with plank seats and footboards (no risers), 4 rows fanning 8 -> 13 ft deep, 18 in rise, shade roof over the wide half\n# unit m\n# name bleachers\n')
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
print(out, len(F), 'faces; wide end', round((YS - line_y(TIERS, X0)) / FT, 1), 'ft deep, narrow end', round((YS - line_y(TIERS, X1)) / FT, 1), 'ft; top tier', round(RISE * TIERS / FT, 1), 'ft')
