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
    d['strokes'] = [s for s in d['strokes'] if (s.get('name') or '') not in ('stone trough 12x4', 'stone trough', 'trough water', 'stone trough (long)', 'pine forest', 'forest trail', 'stable roof water to the long trough (buried pipe)')]
    # ---- long stone trough (Will's markup, 28 Sep; 40 ft after 'a lot of water'): along the inside of the west road, from where the old 12x4 trough stood
    # south toward the scrub-side road, clear of the stable front so you can drive right up. The ground rises ~9 ft going south,
    # so it is three level stone sections stepping up the slope, each on its own levelled strip.
    A = np.array([-56.0, -9.0]); B = np.array([-56.0, -49.0])   # 28 Sep (Will markup 2): 20 ft off the west gable, just south of the entry's drive lanes, 40 ft running south
    u = (B - A) / np.linalg.norm(B - A); nv = np.array([-u[1], u[0]]); LEN = np.linalg.norm(B - A); TW, WT = 3.5, .8
    m = Mesh(); NS = 1; secs = []   # one level (Will, 28 Sep)
    for k in range(NS):
        a, b = A + u * (LEN * k / NS + (0 if k == 0 else .6)), A + u * (LEN * (k + 1) / NS)
        zc = ground(z, *b2grid(*((a + b) / 2)))
        for j_ in range(H):                                        # level a strip 5 ft round this section at its middle height
            for i_ in range(W):
                q = np.array(grid2b(i_, j_)) - a; t = q @ u; w = abs(q @ nv)
                if -3 <= t <= np.linalg.norm(b - a) + 3 and w <= TW / 2 + 5: z[j_, i_] = zc
        secs.append((a, b, zc))
    d['z'] = [round(float(q), 3) for q in z.flatten()]
    def obox(a, b, w0, w1, z0, z1, mat_):                          # a box between a and b along u, from w0 to w1 across (ft)
        c = [a + nv * w0, b + nv * w0, b + nv * w1, a + nv * w1]
        m.face([(*p_, z1) for p_ in c], mat_); m.face([(*p_, z0) for p_ in c[::-1]], mat_)
        for p1, p2 in zip(c, c[1:] + c[:1]): m.face([(*p1, z0), (*p2, z0), (*p2, z1), (*p1, z1)], mat_)
    RIM, BASE = 2.0 * FT, -1.5 * FT
    for a, b, zc in secs:
        obox(a, b, -TW / 2, TW / 2, zc + BASE, zc + .5 * FT, 'rock')                                   # base and floor
        obox(a, b, -TW / 2, -TW / 2 + WT, zc + .5 * FT, zc + RIM, 'rock'); obox(a, b, TW / 2 - WT, TW / 2, zc + .5 * FT, zc + RIM, 'rock')
        obox(a, a + u * WT, -TW / 2 + WT, TW / 2 - WT, zc + .5 * FT, zc + RIM, 'rock'); obox(b - u * WT, b, -TW / 2 + WT, TW / 2 - WT, zc + .5 * FT, zc + RIM, 'rock')
        wl = zc + RIM - .35 * FT; c = [a + u * WT + nv * (-TW / 2 + WT), b - u * WT + nv * (-TW / 2 + WT), b - u * WT + nv * (TW / 2 - WT), a + u * WT + nv * (TW / 2 - WT)]
        m.face([(*p_, wl) for p_ in c], 'water')
    d['strokes'].append(stroke(m, 'stone trough (long)', 'stone-trough-long.obj', z,
        'long stone water trough along the west road, 40 ft, one level on a levelled strip, rim 2 ft, ~650 gal (Will markup, 28 Sep)'))
    # roof water from the stable (Will: capture it into the trough): a gutter downpipe at the stable's south-west corner, buried pipe to the trough's north end
    tpl = [q for q in d['strokes'] if (q.get('name') or '') == 'stalls trough overflow pipe']
    if tpl:
        rp = dict(tpl[0]); rp.update(name='stable roof water to the long trough (buried pipe)', pts=[[*b2grid(-37.0, -22.0), .5], [*b2grid(*(A + u * 2)), .5]])
        d['strokes'].append(rp)
    # ---- the pine grove between the parking and the stable (Will, 28 Sep: a small outcrop of modest, round-crowned pines),
    # placed where the aerial photo shows dark tree cover, clear of the walking path ----
    from PIL import Image
    AER = np.array(Image.open(os.path.join(HERE, 'viewer', 'aerial-src.jpg')).convert('RGB')).astype(int)
    sx, sy = AER.shape[1] / (W - 1), AER.shape[0] / (H - 1)
    WALK = [(140, 43), (125, 37), (121, 34), (118, 31), (111, 28), (104, 25), (96, 22), (89, 19), (81, 17), (72, 16), (68, 16), (64, 15), (47, 13)]
    def near_walk(x, y): return min(math.hypot(x - a, y - b) for a, b in WALK) < 8
    rnd = random.Random(11); trees = []
    for _ in range(3000):
        x, y = rnd.uniform(42, 160), rnd.uniform(-25, 85)
        i_, j_ = b2grid(x, y); px = AER[min(int(j_ * sy), AER.shape[0] - 1), min(int(i_ * sx), AER.shape[1] - 1)]
        if not (px[1] >= px[0] and px.sum() < 300) or near_walk(x, y) or (x < 40 and y > -25): continue
        if all(math.hypot(x - a, y - b) > 13 for a, b, _h in trees): trees.append((x, y, rnd.uniform(14, 22)))
        if len(trees) >= 45: break
    m = Mesh(); n = 8
    for x, y, h in trees:
        zg = ground(z, *b2grid(x, y)); tw = .35; m.box(x - tw, x + tw, y - tw, y + tw, zg - .2, zg + h * .45 * FT, 'trunk')
        R_ = h * .36; zc = zg + h * .68 * FT; hz = h * .3 * FT                          # a rounded crown: two stacked octagonal rings
        ring = lambda rr, zz: [(x + rr * math.cos(2 * math.pi * q / n), y + rr * math.sin(2 * math.pi * q / n), zz) for q in range(n)]
        bot, mid, top = ring(R_ * .55, zc - hz), ring(R_, zc), ring(R_ * .6, zc + hz * .8)
        for q in range(n):
            q2 = (q + 1) % n
            m.face([bot[q], bot[q2], mid[q2], mid[q]], 'pine'); m.face([mid[q], mid[q2], top[q2], top[q]], 'pine')
        m.face(bot[::-1], 'pine'); m.face(top, 'pine')
    d['strokes'].append(stroke(m, 'pine forest', 'pine-forest.obj', z, f'pine grove between the parking and the stable: {len(trees)} round-crowned pines 14-22 ft (Will, 28 Sep)'))
    # ---- the concrete wash pad (in the stable model, 24 x 12 ft along the solid rooms): level the ground under it to the stable
    # floor so it reads as one clean rectangle, not poked through by the slope (Will, 28 Sep) ----
    stb = [q for q in d['strokes'] if q.get('name') == 'walker barn 72x40'][0]
    floor = ground(z, *stb['c']) + stb.get('lift', 0)
    for j_ in range(H):
        for i_ in range(W):
            bx, by = grid2b(i_, j_)
            if -38 <= bx <= -10 and -36 <= by <= -21.5: z[j_, i_] = floor - .02
    d['z'] = [round(float(q), 3) for q in z.flatten()]
    # ---- the barn road comes straight into the middle of the west entry (Will, 28 Sep), not to the stable's corner ----
    rd = [q for q in d['strokes'] if q.get('name') == 'barn to cross-fence road'][0]
    keep = [q for q in rd['pts'] if grid2b(q[0], q[1])[0] < -84]                   # the road as drawn, up to ~48 ft from the gable
    zc_ = rd['pts'][0][2] if len(rd['pts'][0]) > 2 else .5
    P0 = np.array(grid2b(*keep[0][:2])); P1b = np.array(grid2b(*keep[1][:2]))       # join smoothly: leave the old line along its own heading
    t0 = (P0 - P1b) / np.linalg.norm(P0 - P1b)
    P3 = np.array([-38.0, 0.0]); c1 = P0 + t0 * 20; c2 = P3 - np.array([16.0, 0.0])  # and arrive square to the entry
    approach = [tuple((1 - s_) ** 3 * P3 + 3 * (1 - s_) ** 2 * s_ * c2 + 3 * (1 - s_) * s_ ** 2 * c1 + s_ ** 3 * P0) for s_ in np.linspace(0, 1, 14)[:-1]]
    rd['pts'] = [[*b2grid(x, y), zc_] for x, y in approach] + keep
    json.dump(d, open(p, 'w', encoding='utf-8'))
    print(fn, ': long trough', round(LEN, 1), 'ft in', NS, 'sections at', [round(q[2], 2) for q in secs], 'm;', len(trees), 'pines')
