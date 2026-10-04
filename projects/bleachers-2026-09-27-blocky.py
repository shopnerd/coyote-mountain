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
for k in range(TIERS):                     # tier 0 against the trailer is the highest
    top = RISE * (TIERS - k)
    pts = [(X0, line_y(k, X0)), (X1, line_y(k, X1)), (X1, line_y(k + 1, X1)), (X0, line_y(k + 1, X0))]
    prism(pts, -0.4, top, 'wood')
    for x in np.arange(X0 + .6, X1, 1.8):  # plank joints read on the top
        y0_, y1_ = line_y(k, x), line_y(k + 1, x); prism([(x - .01, y0_), (x + .01, y0_), (x + .01, y1_), (x - .01, y1_)], top, top + .01, 'steel')
# end steps at the narrow end
for k in range(TIERS):
    top = RISE * (k + 1); prism([(X1, line_y(TIERS - 1 - k, X1) + .02), (X1 + .45, line_y(TIERS - 1 - k, X1) + .02), (X1 + .45, line_y(TIERS, X1)), (X1, line_y(TIERS, X1))], -0.4, top, 'wood')
# shade roof off the trailer over the wide half: from the trailer's top edge down to three posts
RX0, RX1, RY, RZ0, RZ1 = X0 - .3, 3.2, line_y(TIERS, X0) + .3, 3.96, 3.2
for x in (X0 + .1, (X0 + RX1) / 2, RX1 - .1):
    prism([(x - .07, RY - .07), (x + .07, RY - .07), (x + .07, RY + .07), (x - .07, RY + .07)], -0.4, RZ1 - .02, 'steel')
prism([(RX0, RY - .08), (RX1, RY - .08), (RX1, RY + .08), (RX0, RY + .08)], RZ1 - .18, RZ1 - .02, 'steel')   # beam
for dz in (0, .03): quad((RX0, YS, RZ0 + dz), (RX1, YS, RZ0 + dz), (RX1, RY - .3, RZ1 + dz), (RX0, RY - .3, RZ1 + dz), 'roof')
out = os.path.join(HERE, 'bleachers.obj')
with open(out, 'w', newline='\n') as f:
    f.write('# bleachers in front of the trailer, facing the arena: 4 wooden tiers fanning 8 -> 13 ft deep, 18 in rise, shade roof over the wide half\n# unit m\n# name bleachers\n')
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
