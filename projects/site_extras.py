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


def spill_basin(m, x0, x1, y_end, sgn, floor_z, rim_z):
    """4 Oct (Will, photo of two stepped stone basins): the trough spills over a stone spout at its end into a small, lower stone
    basin butted right against it; a small pump in that basin sends the water back. x0..x1 = trough width (ft), y_end = its end
    face (ft), sgn = +1/-1 outward along y, floor_z / rim_z = the trough's floor and rim (m)."""
    BW, BL, WT_ = (x1 - x0) * .95, 3.2, .55
    xc = (x0 + x1) / 2; a0, a1 = xc - BW / 2, xc + BW / 2
    y0, y1 = sorted((y_end, y_end + sgn * BL))
    brim = rim_z - .9 * FT; bfl = floor_z - .25 * FT
    m.box(a0, a1, y0, y1, bfl - .3, bfl, 'rock')                                                   # base
    m.box(a0, a0 + WT_, y0, y1, bfl, brim, 'rock'); m.box(a1 - WT_, a1, y0, y1, bfl, brim, 'rock')   # side walls
    ye = y1 if sgn > 0 else y0; m.box(a0, a1, min(ye, ye - sgn * WT_), max(ye, ye - sgn * WT_), bfl, brim, 'rock')   # far wall (the near side is the trough)
    bwl = brim - .3 * FT
    m.face([(a0 + WT_, y0 + (WT_ if sgn < 0 else 0), bwl), (a1 - WT_, y0 + (WT_ if sgn < 0 else 0), bwl), (a1 - WT_, y1 - (WT_ if sgn > 0 else 0), bwl), (a0 + WT_, y1 - (WT_ if sgn > 0 else 0), bwl)], 'water')
    sy0, sy1 = sorted((y_end - sgn * .45, y_end + sgn * .75))                                     # the spout: a stone lip notched in the end wall
    m.box(xc - .35, xc + .35, sy0, sy1, rim_z - .2 * FT, rim_z - .05 * FT, 'rock')
    ly = y_end + sgn * .75; zt = rim_z - .12 * FT                                                  # the falling sheet of water
    m.face([(xc - .22, ly, zt), (xc + .22, ly, zt), (xc + .22, ly + sgn * .35, bwl), (xc - .22, ly + sgn * .35, bwl)], 'water')

for fn in FILES:
    p = os.path.join(HERE, fn); d = json.load(open(p, encoding='utf-8')); z = np.array(d['z'], float).reshape(H, W)
    d['strokes'] = [s for s in d['strokes'] if (s.get('name') or '') not in ('stone trough 12x4', 'stone trough', 'trough water', 'stone trough (long)', 'east trough', 'pine forest', 'forest trail', 'stable roof water to the long trough (buried pipe)', 'wash pad trough', 'native planting')]
    # ---- long stone trough (Will's markup, 28 Sep; 40 ft after 'a lot of water'): along the inside of the west road, from where the old 12x4 trough stood
    # south toward the scrub-side road, clear of the stable front so you can drive right up. The ground rises ~9 ft going south,
    # so it is three level stone sections stepping up the slope, each on its own levelled strip.
    Z_PRE = z.copy()                                                # 3 Oct: ground before the trough, so the road can keep its own smooth grade
    TXW = -93.0                                                     # 3 Oct, Will moved it again: 57 ft off the west gable
    A = np.array([TXW, -22.0]); B = np.array([TXW, 22.0])   # 3 Oct (Will placed it in the app): 49 ft off the west gable, across the front, centred on the stable, 44 ft; retaining wall, stable side held at the rim
    u = (B - A) / np.linalg.norm(B - A); nv = np.array([-u[1], u[0]]); LEN = np.linalg.norm(B - A); TW, WT = 3.5, .8
    m = Mesh(); NS = 1; secs = []   # one level (Will, 28 Sep)
    for k in range(NS):
        a, b = A + u * (LEN * k / NS + (0 if k == 0 else .6)), A + u * (LEN * (k + 1) / NS)
        zc = ground(z, *b2grid(*((a + b) / 2 + nv * (TW / 2 + 1))))      # floor level = the low (road, north) side
        RW = 2.0 * FT                                               # retaining: the high (south) side is held up level with the rim
        Lk = np.linalg.norm(b - a)
        for j_ in range(H):
            for i_ in range(W):
                q = np.array(grid2b(i_, j_)) - a; t = q @ u; w = q @ nv
                tgt = zc + RW if w < -TW / 2 else zc                              # held at the rim on the high side, floor level under and on the low side
                ot = max(-t, 0, t - Lk); ow = max(w - (TW / 2 + 5), 0, -(TW / 2 + 4) - w)
                o = math.hypot(ot, ow)                                            # ft outside the levelled area
                if o >= 10: continue
                f = o / 10; z[j_, i_] = tgt * (1 - f) + z[j_, i_] * f            # eases back to natural over 10 ft all round (3 Oct: no steps at the ends)
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
    spill_basin(m, TXW - TW / 2, TXW + TW / 2, secs[-1][1][1], 1, secs[-1][2] + .5 * FT, secs[-1][2] + RIM)   # 4 Oct: spill basin at the north end
    d['strokes'].append(stroke(m, 'stone trough (long)', 'stone-trough-long.obj', z,
        'long stone water trough as a retaining wall between the stable and the main road, 44 ft, one level, rim 2 ft, uphill side backfilled to the rim (Will + Walker, 3 Oct)'))
    # roof water from the stable (Will: capture it into the trough): a gutter downpipe at the stable's south-west corner, buried pipe to the trough's north end
    tpl = [q for q in d['strokes'] if (q.get('name') or '') == 'stalls trough overflow pipe']
    if tpl:
        rp = dict(tpl[0]); rp.update(name='stable roof water to the long trough (buried pipe)', pts=[[*b2grid(-37.0, -22.0), .5], [*b2grid(*(B - u * 2)), .5]])
        d['strokes'].append(rp)
    # ---- 4 Oct (Will, night): the path from the parking meanders gently through the pines and arrives ON AXIS at the east gable's
    # big doors, so you are brought to the view straight down the aisle. A smooth Hermite curve from the parking end to a point 30 ft
    # off the gable, with a soft double bend (zero offset and zero slope at both ends), then straight on the centre line. 5 ft wide.
    # The pines below keep 8 ft clear of it, so a tree in the way moves. ----
    wp_ = [q for q in d['strokes'] if q.get('name') == 'walking path, parking to barn']
    if wp_:
        p0x, p0y = grid2b(*wp_[0]['pts'][0][:2])                      # keep the parking end where it was
        ax_, ay_ = 36.0 + 2.0 + 30.0, 0.0                              # onto the axis 30 ft before the doors (gable x = 36, overhang 2)
        ex_, ey_ = 36.0 + 2.5, 0.0                                     # ends at the doors, just past the overhang
        L_ = math.hypot(ax_ - p0x, ay_ - p0y); m0 = ((ax_ - p0x) * .9, (ay_ - p0y) * .9); m1 = (-L_ * .9, 0.0)
        nx_, ny_ = -(ay_ - p0y) / L_, (ax_ - p0x) / L_
        WALK_NEW = []
        for k in range(41):
            t = k / 40; h00 = 2*t**3 - 3*t**2 + 1; h10 = t**3 - 2*t**2 + t; h01 = -2*t**3 + 3*t**2; h11 = t**3 - t**2
            x = h00 * p0x + h10 * m0[0] + h01 * ax_ + h11 * m1[0]; y = h00 * p0y + h10 * m0[1] + h01 * ay_ + h11 * m1[1]
            off = 7.0 * math.sin(2 * math.pi * t) * math.sin(math.pi * t)          # the meander: two gentle bends, dead flat at both ends
            WALK_NEW.append((x + nx_ * off, y + ny_ * off))
        for k in range(1, 11): WALK_NEW.append((ax_ + (ex_ - ax_) * k / 10, 0.0))   # the straight run to the doors
        wp_[0]['pts'] = [[round(v, 3) for v in b2grid(x, y)] + [.5] for x, y in WALK_NEW]; wp_[0]['c'] = [round(v, 3) for v in b2grid(*WALK_NEW[0])]
        print(fn, ': walking path re-routed,', len(WALK_NEW), 'pts, parking end (%.0f, %.0f) ft -> doors (%.1f, %.1f)' % (p0x, p0y, ex_, ey_))
    else: WALK_NEW = None
    # ---- the pine grove between the parking and the stable (Will, 28 Sep: a small outcrop of modest, round-crowned pines),
    # placed where the aerial photo shows dark tree cover, clear of the walking path ----
    from PIL import Image
    AER = np.array(Image.open(os.path.join(HERE, 'viewer', 'aerial-src.jpg')).convert('RGB')).astype(int)
    sx, sy = AER.shape[1] / (W - 1), AER.shape[0] / (H - 1)
    WALK = WALK_NEW or [(140, 43), (125, 37), (121, 34), (118, 31), (111, 28), (104, 25), (96, 22), (89, 19), (81, 17), (72, 16), (68, 16), (64, 15), (47, 13)]   # 4 Oct: the re-routed path above
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
            # 3 Oct: the ground is levelled a little past the pad and the trough on its west edge, easing to natural over 10 ft
            o = math.hypot(max(-42 - bx, 0, bx + 10), max(-37 - by, 0, by + 21.5))
            if o < 10 and by < -21.5: f = o / 10; z[j_, i_] = (floor - .02) * (1 - f) + z[j_, i_] * f
    d['z'] = [round(float(q), 3) for q in z.flatten()]
    # ---- a fieldstone trough along the wash pad's WEST edge, running out from the stable's south-west corner (Will, 3 Oct, from
    # the 28 Sep 'stable from the road' painting he liked): 14 x 3 ft just outside the gable line, rim 2 ft above the pad ----
    PAD_S = -21.0 - .75 - 12.0                                      # the pad's south edge (stable: HD 21, ROCK_T/2 .75, pad 12 ft deep)
    TW2, WT2 = 3.0, .7
    x0, x1, y0, y1 = -36.0 - TW2, -36.0, PAD_S - 1.5, -21.75          # west of the pad (x -36 is the gable line), wall to 1.5 ft past the pad
    m = Mesh(); fz = floor - .02; top = fz + 2.0 * FT; lip = fz + .4 * FT
    m.box(x0, x1, y0, y1, fz - .3, lip, 'rock')                                                  # base and floor
    m.box(x0, x0 + WT2, y0, y1, lip, top, 'rock'); m.box(x1 - WT2, x1, y0, y1, lip, top, 'rock')   # long walls
    m.box(x0, x1, y0, y0 + WT2, lip, top, 'rock'); m.box(x0, x1, y1 - WT2, y1, lip, top, 'rock')   # end walls
    wl = fz + 1.65 * FT; m.face([(x0 + WT2, y0 + WT2, wl), (x1 - WT2, y0 + WT2, wl), (x1 - WT2, y1 - WT2, wl), (x0 + WT2, y1 - WT2, wl)], 'water')
    spill_basin(m, x0, x1, y0, -1, lip, top)                                     # 4 Oct: spill basin at the south end, away from the wall
    d['strokes'].append(stroke(m, 'wash pad trough', 'wash-pad-trough.obj', z, 'fieldstone trough 14 x 3 ft along the west edge of the wash pad, out from the SW corner, rim 2 ft (Will, 3 Oct)'))
    # ---- 4 Oct (Will, revised that night: red lines on the plan shot): a third stone trough ALONG THE EAST RUN FENCE, just outside
    # the north-east run's east fence (x = 36), 32 x 3.5 ft, from 4 ft past the wall line out along the run; the horse in that run
    # drinks through the rails, arrivals from the parking drink from the outside. Fed by the NORTH gutter's east downspout; the
    # south gutter feeds the west troughs (irrigation sheet D-3). Rim 2 ft above a small level apron on the OUTSIDE only. ----
    ex0, ex1, ey0, ey1 = 36.0 + 1.0, 36.0 + 1.0 + 3.5, 21.0 + 4.0, 21.0 + 36.0
    ecx, ecy = (ex0 + ex1) / 2, (ey0 + ey1) / 2; efz = ground(z, *m2grid(*b2m(ecx, ecy)))
    for j_ in range(H):
        for i_ in range(W):
            bx, by = grid2b(i_, j_)
            if bx < 36.0 + .3: continue                                                                     # never touch the graded run inside the fence
            o = math.hypot(max(ex0 - .3 - bx, 0, bx - ex1 - 4), max(ey0 - 3 - by, 0, by - ey1 - 3))
            if o < 6: f = o / 6; z[j_, i_] = efz * (1 - f) + z[j_, i_] * f
    d['z'] = [round(float(q), 3) for q in z.flatten()]
    m = Mesh(); top = efz + 2.0 * FT; lip = efz + .4 * FT
    m.box(ex0, ex1, ey0, ey1, efz - .3, lip, 'rock')
    m.box(ex0, ex0 + WT2, ey0, ey1, lip, top, 'rock'); m.box(ex1 - WT2, ex1, ey0, ey1, lip, top, 'rock')
    m.box(ex0, ex1, ey0, ey0 + WT2, lip, top, 'rock'); m.box(ex0, ex1, ey1 - WT2, ey1, lip, top, 'rock')
    wl = efz + 1.65 * FT; m.face([(ex0 + WT2, ey0 + WT2, wl), (ex1 - WT2, ey0 + WT2, wl), (ex1 - WT2, ey1 - WT2, wl), (ex0 + WT2, ey1 - WT2, wl)], 'water')
    spill_basin(m, ex0, ex1, ey1, 1, lip, top)                                   # 4 Oct: spill basin at the far (north) end
    d['strokes'].append(stroke(m, 'east trough', 'east-trough.obj', z, 'fieldstone trough 32 x 3.5 ft along the outside of the north-east run fence, 4 ft off the wall line, rim 2 ft, fed by the north gutter (Will, 4 Oct night)'))
    # ---- the covered stalls' pad (3 Oct: the building grew 8 ft for the through-hallway alfalfa bay): level the ground under its
    # footprint (+3 ft) to its floor, easing back to natural over 8 ft ----
    cvl = [q for q in d['strokes'] if q.get('name') == 'covered stalls']
    cvs = cvl[0] if cvl else None
    if cvs:
        # 4 Oct: the obj is written in east/north feet (covered_stalls.py `world`), so its bounding box is a 92 x 98 ft square,
        # not the 92 x 36 building: test the TRUE rotated rectangle instead (that square had flattened a tongue up to the scrub road)
        from objtools import parse_obj as _po
        _T, _ = _po(os.path.join(HERE, 'covered-stalls.obj')); _P = _T.reshape(-1, 3); _mx, _my = _P[:, 0].mean() * FT, _P[:, 1].mean() * FT
        _st = [(-116.7637927468709, 31.99970749966619), (-116.7635094983617, 31.99998532313917), (-116.7633790473066, 31.99988684382775), (-116.7636714287398, 31.99959200352455)]
        from geo import la0 as _la0, lo0 as _lo0
        _k = 111320 * math.cos(math.radians(_la0)); _enu = lambda la, lo: np.array([(lo - _lo0) * _k, (la - _la0) * 111320])
        _A, _B, _C, _D = (_enu(la, lo) for lo, la in _st)
        _u = (_B - _A) / np.linalg.norm(_B - _A); _v = (_D - _A) / np.linalg.norm(_D - _A); _v = _v - _u * (_v @ _u); _v /= np.linalg.norm(_v)
        cfl = ground(z, *cvs['c']) + cvs.get('lift', 0); cr_ = math.radians(cvs['rot']); RXs, HDs = 46.0, 26.0          # roof 92 ft, building 52 ft
    for j_ in (range(H) if cvs else []):
        for i_ in range(W):
            dx, dy = (i_ - cvs['c'][0]) * cs, -(j_ - cvs['c'][1]) * cs
            ex, ey = dx * math.cos(cr_) + dy * math.sin(cr_) + _mx, -dx * math.sin(cr_) + dy * math.cos(cr_) + _my   # east/north from the obj origin (m)
            t_, s_ = (ex * _u[0] + ey * _u[1]) / FT, (ex * _v[0] + ey * _v[1]) / FT                                   # along / across the building (ft)
            o = math.hypot(max(-RXs - t_, 0, t_ - RXs), max(-HDs - s_, 0, s_ - HDs))
            if o <= 3: z[j_, i_] = cfl
            elif o <= 11: f = (o - 3) / 8; z[j_, i_] = cfl * (1 - f) + z[j_, i_] * f
    d['z'] = [round(float(q), 3) for q in z.flatten()]
    # ---- the stable pad (Will, 28 Sep: a corner of ground poked through the floor): cut the ground under the whole footprint
    # (+2 ft) down to the stable floor so the hillside never shows inside ----
    for j_ in range(H):
        for i_ in range(W):
            bx, by = grid2b(i_, j_)
            if -38.5 <= bx <= 38.5 and -23.5 <= by <= 23.5 and z[j_, i_] > floor: z[j_, i_] = floor
    d['z'] = [round(float(q), 3) for q in z.flatten()]
    # ---- the barn road comes straight into the middle of the west entry (Will, 28 Sep), not to the stable's corner ----
    rd = [q for q in d['strokes'] if q.get('name') == 'barn to cross-fence road'][0]
    keep = [q for q in rd['pts'] if grid2b(q[0], q[1])[0] < -118]   # 3 Oct: one long direct sweep from further out (Will)                   # the road as drawn, up to ~48 ft from the gable
    zc_ = rd['pts'][0][2] if len(rd['pts'][0]) > 2 else .5
    P0 = np.array(grid2b(*keep[0][:2])); P1b = np.array(grid2b(*keep[1][:2]))       # join smoothly: leave the old line along its own heading
    t0 = (P0 - P1b) / np.linalg.norm(P0 - P1b)
    P3 = np.array([-38.0, 0.0]); Lb = np.linalg.norm(P3 - P0); c1 = P0 + t0 * Lb * .35; c2 = P3 - np.array([Lb * .3, 0.0])  # and arrive square to the entry
    approach = [tuple((1 - s_) ** 3 * P3 + 3 * (1 - s_) ** 2 * s_ * c2 + 3 * (1 - s_) * s_ ** 2 * c1 + s_ ** 3 * P0) for s_ in np.linspace(0, 1, 14)[:-1]]
    rd['pts'] = [[*b2grid(x, y), zc_] for x, y in approach] + keep
    # the road keeps a smooth even grade past the trough (3 Oct, Will: no glitch): along the new curve, take the pre-trough
    # ground, smooth it, and lay it under the road (7 ft each side), easing out over 4 ft more
    C_ = np.array([grid2b(*q[:2]) for q in rd['pts']])
    D_ = np.r_[0, np.cumsum(np.hypot(*np.diff(C_, axis=0).T))]
    prof = np.array([ground(Z_PRE, *b2grid(x, y)) for x, y in C_]); prof = np.convolve(np.pad(prof, 3, mode='edge'), np.ones(7) / 7, mode='valid')
    sel = (C_[:, 0] > -135) & (C_[:, 0] < -55)
    for j_ in range(H):
        for i_ in range(W):
            P_ = np.array(grid2b(i_, j_)); dd = np.hypot(*(C_[sel] - P_).T); k_ = int(np.argmin(dd)); dmin = dd[k_]
            if dmin > 11: continue
            zr = prof[sel][k_]; f = 0 if dmin <= 7 else (dmin - 7) / 4
            z[j_, i_] = zr * (1 - f) + z[j_, i_] * f
    d['z'] = [round(float(q), 3) for q in z.flatten()]
    # ---- minimal native planting (Will, 3 Oct, red markup on the west elevation): two low beds flanking the drive-in between the
    # long trough and the west gable: sage / buckwheat / brittlebush mounds 1.5-3.5 ft, kept 9 ft off the road, 6 ft apart ----
    rd_ = [q for q in d['strokes'] if q.get('name') == 'barn to cross-fence road']   # AFTER the re-route below, so the rows follow the real drive
    RP = [grid2b(*q[:2]) for q in rd_[0]['pts']] if rd_ else []
    def near_road(x, y): return RP and min(math.hypot(x - a, y - b) for a, b in RP) < 9.5
    rd_[0]['pw'] = 14 * FT                                            # 4 Oct (Will): the entry drive is 14 ft wide all the way to the trough
    # plants LINE the drive on both sides from the trough to the gable (4 Oct, Will): a row 1-4 ft off each edge, mixed sizes
    # (sage, buckwheat, deer grass, a few taller accents), with a second loose row behind
    rnd2 = random.Random(7); shrubs = []
    seg = [(x, y) for x, y in RP if -90 <= x <= -40]                  # the straight approach between trough and gable
    seg.sort()
    def along(t):                                                   # point + normal at fraction t of the approach
        k = min(int(t * (len(seg) - 1)), len(seg) - 2); a, b = seg[k], seg[k + 1]
        dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy) or 1
        return (a[0] + dx * (t * (len(seg) - 1) - k), a[1] + dy * (t * (len(seg) - 1) - k)), (-dy / L, dx / L)
    for side in (-1, 1):
        t = .04
        while t < .97:
            (px, py), (nx, ny) = along(t); off = 7 + rnd2.uniform(1.0, 4.0); R_ = rnd2.choice([1.4, 1.8, 2.2, 2.6, 3.0, 3.6])
            shrubs.append((px + nx * off * side, py + ny * off * side, R_, side))
            if rnd2.random() < .45:                                   # a second, looser row behind
                off2 = off + rnd2.uniform(4.5, 8.0); shrubs.append((px + nx * off2 * side, py + ny * off2 * side, rnd2.uniform(1.5, 3.2), side))
            t += (R_ * 2 + rnd2.uniform(1.5, 3.5)) / 50.0
    m = Mesh(); n = 8
    for x, y, R_, _side in shrubs:
        zg = ground(z, *b2grid(x, y)); h = R_ * .9 * FT
        ring = lambda rr, zz: [(x + rr * math.cos(2 * math.pi * q / n + .3), y + rr * math.sin(2 * math.pi * q / n + .3), zz) for q in range(n)]
        bot, mid, top = ring(R_ * .9, zg - .05), ring(R_, zg + h * .45), ring(R_ * .5, zg + h)
        for q in range(n):
            q2 = (q + 1) % n
            m.face([bot[q], bot[q2], mid[q2], mid[q]], 'sage'); m.face([mid[q], mid[q2], top[q2], top[q]], 'sage')
        m.face(top, 'sage')
    d['strokes'].append(stroke(m, 'native planting', 'native-planting.obj', z, f'native planting: {len(shrubs)} mixed sage/buckwheat/deer-grass mounds lining both sides of the 14 ft entry drive from the trough to the gable (Will, 4 Oct)'))
    d['z'] = [round(float(q), 3) for q in z.flatten()]
    json.dump(d, open(p, 'w', encoding='utf-8'))
    print(fn, ': long trough', round(LEN, 1), 'ft in', NS, 'sections at', [round(q[2], 2) for q in secs], 'm;', len(trees), 'pines')
