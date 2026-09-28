"""Site pieces around the stable (28 Sep 2026, Will's and Walker's gallery notes):
- the long stone water trough in front of the stable's road (west) end: 20 ft off the gable, as long as the barn road
  allows (~37 ft), same fieldstone, level on a stone base, the ground under it levelled; it replaces the 12x4 trough
- the pine forest on the hill behind the stable (past the scrub-side road): pines up to ~34 ft, with a winding trail
Both are built in the stable's own frame (ft, x along the barn toward the parking, y north) and placed like the stable.

    python site_extras.py     ->  stone-trough-long.obj, pine-forest.obj and their strokes (+ 'forest trail') in the three drawings
"""
import json, math, os, random, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); FT = .3048
from geo import cs, W, H
FILES = ('centro-equino-2026-09-26.json', 'centro-equino-2026-09-26-stalls16.json', 'centro-equino-2026-09-26-stalls16-nopad.json')
O = json.load(open(os.path.join(HERE, 'stable_origin.json'))); G0, ROTW = O['grid'], O['rot']
r, ROT = math.radians(ROTW), math.radians(90 - 65.84)
def b2m(bx, by):                                      # stable frame ft -> the objects' rotated frame, metres
    return ((bx * math.cos(ROT) - by * math.sin(ROT)) * FT, (bx * math.sin(ROT) + by * math.cos(ROT)) * FT)
def m2grid(x, y): return G0[0] + (x * math.cos(r) - y * math.sin(r)) / cs, G0[1] - (x * math.sin(r) + y * math.cos(r)) / cs
def b2grid(bx, by): return m2grid(*b2m(bx, by))
def grid2b(i, j):
    x = ((i - G0[0]) * math.cos(r) - (j - G0[1]) * math.sin(r)) * cs; y = (-(i - G0[0]) * math.sin(r) - (j - G0[1]) * math.cos(r)) * cs
    x, y = x / FT, y / FT
    return x * math.cos(ROT) + y * math.sin(ROT), -x * math.sin(ROT) + y * math.cos(ROT)
def ground(z, i, j):
    i = min(max(i, 0), W - 1.001); j = min(max(j, 0), H - 1.001); i0, j0 = int(i), int(j); fx, fy = i - i0, j - j0
    return z[j0, i0] * (1 - fx) * (1 - fy) + z[j0, i0 + 1] * fx * (1 - fy) + z[j0 + 1, i0] * (1 - fx) * fy + z[j0 + 1, i0 + 1] * fx * fy

class Mesh:                                           # faces in stable-frame ft (x, y) with ABSOLUTE z in metres
    def __init__(s): s.F, s.M = [], []
    def face(s, pts, m): s.F.append(pts); s.M.append(m)
    def box(s, x0, x1, y0, y1, z0, z1, m):
        c = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        s.face([(x, y, z1) for x, y in c], m); s.face([(x, y, z0) for x, y in c[::-1]], m)
        for (xa, ya), (xb, yb) in zip(c, c[1:] + c[:1]): s.face([(xa, ya, z0), (xb, yb, z0), (xb, yb, z1), (xa, ya, z1)], m)
def hull2(pts):
    pts = sorted(map(tuple, pts)); cross = lambda o_, a, b: (a[0] - o_[0]) * (b[1] - o_[1]) - (a[1] - o_[1]) * (b[0] - o_[0])
    lo, up = [], []
    for q in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], q) <= 0: lo.pop()
        lo.append(q)
    for q in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], q) <= 0: up.pop()
        up.append(q)
    return [list(p) for p in lo[:-1] + up[:-1]]
def stroke(mesh, name, objname, zgrid, header):
    V = [[*b2m(x, y), z] for f in mesh.F for (x, y, z) in f]
    A = np.array(V); cx, cy = A[:, 0].mean(), A[:, 1].mean(); mz = A[:, 2].min()
    tris = []
    for f in mesh.F:
        P = [(*b2m(x, y), z) for (x, y, z) in f]
        for k in range(1, len(P) - 1):
            for q in (P[0], P[k], P[k + 1]): tris += [round(q[0] - cx, 3), round(q[1] - cy, 3), round(q[2] - mz, 3)]
    with open(os.path.join(HERE, objname), 'w', newline='\n') as fo:      # the obj is kept for its material groups (the viewer export reads them)
        fo.write(f'# {header}\n# unit m\n# name {name}\n')
        for v in V: fo.write('v %.3f %.3f %.3f\n' % (v[0] - cx, v[1] - cy, v[2] - mz))
        n, last = 1, None
        for f, m in zip(mesh.F, mesh.M):
            if m != last: fo.write(f'usemtl {m}\n'); last = m
            fo.write('f ' + ' '.join(str(n + k) for k in range(len(f))) + '\n'); n += len(f)
    c = list(m2grid(cx, cy)); T = np.array(tris).reshape(-1, 3)
    return dict(color='ink', shape=False, kind='obj', c=c, name=name, unit='m', rot=ROTW, sc=1, lift=float(mz - ground(zgrid, *c)),
                tris=tris, foot=hull2(T[:, :2]), h=float(T[:, 2].max()), w=1, a=1, dash=False, pts=[[c[0], c[1], .5]])

# the scrub-side road in the stable frame (from the drawing), for the forest edge and the trail
ROAD = [(344, 83), (310, 64), (263, 26), (224, 1), (178, -23), (146, -38), (109, -54), (65, -70), (22, -89), (-22, -109), (-64, -130), (-107, -152), (-142, -170), (-168, -186)]
def road_y(x):
    R_ = sorted(ROAD); xs = [p[0] for p in R_]; ys = [p[1] for p in R_]
    return float(np.interp(x, xs, ys))

for fn in FILES:
    p = os.path.join(HERE, fn); d = json.load(open(p, encoding='utf-8')); z = np.array(d['z'], float).reshape(H, W)
    d['strokes'] = [s for s in d['strokes'] if (s.get('name') or '') not in ('stone trough 12x4', 'stone trough', 'trough water', 'stone trough (long)', 'pine forest', 'forest trail')]
    # ---- long stone trough ----
    TX, Y0, Y1, TW = -56.0, -21.0, 16.0, 3.5                       # centre line 20 ft off the gable (x = -36), 37 ft long, 3.5 ft wide
    zc = ground(z, *b2grid(TX, (Y0 + Y1) / 2))
    for j in range(H):                                            # level the ground under it (and 5 ft round) at its centre height
        for i in range(W):
            bx, by = grid2b(i, j)
            if TX - TW / 2 - 5 <= bx <= TX + TW / 2 + 5 and Y0 - 5 <= by <= min(Y1 + 1, 17.0): z[j, i] = zc
    d['z'] = [round(float(q), 3) for q in z.flatten()]
    m = Mesh(); RIM, WT, BASE = 2.0 * FT, .8, -1.5 * FT
    x0, x1 = TX - TW / 2, TX + TW / 2
    m.box(x0, x1, Y0, Y1, zc + BASE, zc + .5 * FT, 'rock')                           # the stone base and floor
    for a, b, c0, c1 in ((x0, x0 + WT, Y0, Y1), (x1 - WT, x1, Y0, Y1), (x0 + WT, x1 - WT, Y0, Y0 + WT), (x0 + WT, x1 - WT, Y1 - WT, Y1)):
        m.box(a, b, c0, c1, zc + .5 * FT, zc + RIM, 'rock')                          # the four walls
    m.face([(x0 + WT, Y0 + WT, zc + RIM - .35 * FT), (x1 - WT, Y0 + WT, zc + RIM - .35 * FT), (x1 - WT, Y1 - WT, zc + RIM - .35 * FT), (x0 + WT, Y1 - WT, zc + RIM - .35 * FT)], 'water')
    d['strokes'].append(stroke(m, 'stone trough (long)', 'stone-trough-long.obj', z,
        'long stone water trough in front of the stable, 37 x 3.5 ft, rim 2 ft, 20 ft off the west gable (Will + Walker, 28 Sep)'))
    # ---- pine forest past the scrub-side road, with a winding trail ----
    rnd = random.Random(7)
    trail = []
    for k in range(15):
        t = k / 14; x = 40 + 28 * math.sin(t * 2.4) + 9 * math.sin(t * 7.1); y = road_y(40) - 4 - t * 210
        trail.append((x, y))
    def near_trail(x, y): return min(math.hypot(x - a, y - b) for a, b in trail) < 9
    trees = []
    for _ in range(4000):
        x = rnd.uniform(-170, 270); y = road_y(x) - rnd.uniform(18, 240)
        i, j = b2grid(x, y)
        if not (1 <= i <= W - 2 and 1 <= j <= H - 2) or near_trail(x, y): continue
        if all(math.hypot(x - a, y - b) > 17 for a, b, _h in trees): trees.append((x, y, rnd.uniform(22, 34)))
        if len(trees) >= 240: break
    m = Mesh()
    for x, y, h in trees:
        zg = ground(z, *b2grid(x, y)); n = 7
        tw = .45; m.box(x - tw, x + tw, y - tw, y + tw, zg - .2, zg + h * .35 * FT, 'trunk')
        for lo, hi, rad in ((.22, .75, .30), (.45, 1.0, .21)):                        # two stacked cones
            base = [(x + rad * h * math.cos(2 * math.pi * q / n), y + rad * h * math.sin(2 * math.pi * q / n)) for q in range(n)]
            apex = (x, y, zg + h * hi * FT)
            for q in range(n): m.face([(*base[q], zg + h * lo * FT), (*base[(q + 1) % n], zg + h * lo * FT), apex], 'pine')
            m.face([(*b, zg + h * lo * FT) for b in base[::-1]], 'pine')
    d['strokes'].append(stroke(m, 'pine forest', 'pine-forest.obj', z, f'pine forest behind the stable: {len(trees)} pines 22-34 ft (Will, 28 Sep)'))
    tmpl = [s for s in d['strokes'] if s.get('kind') == 'path'][0]
    tp = dict(tmpl); tp.update(name='forest trail', pw=1.2, pts=[[*b2grid(x, y), .5] for x, y in trail])
    d['strokes'].append(tp)
    json.dump(d, open(p, 'w', encoding='utf-8'))
    print(fn, ': long trough at', round(zc, 2), 'm;', len(trees), 'pines; trail', len(trail), 'pts')
