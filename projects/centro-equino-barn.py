"""Walker's Centro Equino stable as an OBJ for the topo tool, 27 Sep 2026: the 24 Sep plan unchanged, with a clerestory
monitor along the ridge (Walker's image) and horizontal tomato stakes above the rock, bird's-nest style (Will, 27 Sep).
The 24 Sep design:
76 x 42 ft (27 Sep, Walker's elevation sketch; was 72 x 40) on 12 in pipe portal frames (5 frames at 19 ft), stacked rock to 4.5 ft all round,
tomato-stake walls above, a big entry at both gable ends, metal roof with 2 ft overhangs on the
long sides, 8 in pipe purlins and eave beams. Walker's layout: 6 stalls north with 12 x 40 ft runs,
wash / tack / feed / alfalfa-storage south, 14 ft aisle. Feet, z up, x along the long axis, y north,
turned to her bearing; the origin is the barn centre. The # geo line tells topo.html where it goes.

    python centro-equino-barn.py   ->  centro-equino-barn.obj
(The 76 x 42 ten-stall version is kept as centro-equino-barn-76x42.obj.)
"""
import math, os

L, D = 76.0, 42.0                        # column centre lines: Walker's elevation sketch, 27 Sep (76 ft south face; gable 14 + 14 entry + 14)
HL, HD = L / 2, D / 2
AISLE, STALL, RUN_D = 14.0, 12.0, 40.0
ROW_D = (D - AISLE) / 2                  # 14 ft
EAVE, RIDGE, OH = 12.0, 17.0, 2.0
ROCK_H, ROCK_T, STICK_T = 4.5, 1.5, 0.4
FRAMES = [-38.0, -19.0, 0.0, 19.0, 38.0]   # 5 frames at 19 ft
COL_D, PURL_D = 12.75 / 12, 8.625 / 12
ENTRY_W = AISLE                          # the big gable entries, open up to the rafters
DOOR = (5.0, 10.0)                       # Walker's sketch: tall openings, near the eave
RAIL_H = 5.5
MON_HW, MON_H, MON_X = 5.0, 2.5, 30.0   # clerestory monitor: half width, glazing height, half length (27 Sep)
STAKE_H, STAKE_T, STAKE_P = .12, .16, .3   # tomato stakes, horizontal: height, thickness, course spacing (gaps between)
NORTH = ['stall'] * 6                    # 6 x 12.67 ft
SOUTH = [('tack / feed', 13), ('wash', 13)] + [('stall', 12.5)] * 4   # 27 Sep (Will): rooms at the WEST end by the barn road, so the open ground is by the road; 4 stalls with runs east of them
SOLID = ('tack / feed', 'wash')           # Walker's elevation: solid infill above the rock at the rooms (straw bale or cob, plastered), not stakes
RUN_FALL = .05                           # the south runs climb the slope at 5 % (graded), a low rock wall at their uphill end
LAT, LON, GABLE = 32.0002846, -116.7632631, 65.84

slope = (RIDGE - EAVE) / HD
def roof_z(y): return RIDGE - slope * abs(y)       # rafter centre line

V, F, MAT = [], [], []
CUR = ['rock']                           # material of the faces being made (written as usemtl groups for the renders)
def mat(m): CUR[0] = m
ROT = math.radians(90 - GABLE)
rc, rs = math.cos(ROT), math.sin(ROT)
def world(x, y, z): return (x * rc - y * rs, x * rs + y * rc, z)

def quad(a, b, c, d):
    i = len(V) + 1; V.extend(world(*p) for p in (a, b, c, d)); F.append((i, i + 1, i + 2, i + 3)); MAT.append(CUR[0])
def box(x0, x1, y0, y1, z0, z1):
    if x1 - x0 < 1e-6 or y1 - y0 < 1e-6 or z1 - z0 < 1e-6: return
    i = len(V) + 1
    for z in (z0, z1):
        for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)): V.append(world(x, y, z))
    for f in ((0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)):
        F.append(tuple(i + k for k in f)); MAT.append(CUR[0])
def bar(p, q, d, n=8):                   # a round-ish tube from p to q
    p, q = [float(v) for v in p], [float(v) for v in q]
    ax_ = [q[k] - p[k] for k in range(3)]; Ln = math.sqrt(sum(a * a for a in ax_)); u = [a / Ln for a in ax_]
    t = [0, 0, 1] if abs(u[2]) < .9 else [1, 0, 0]
    a = [u[1] * t[2] - u[2] * t[1], u[2] * t[0] - u[0] * t[2], u[0] * t[1] - u[1] * t[0]]; na = math.sqrt(sum(v * v for v in a)); a = [v / na for v in a]
    b = [u[1] * a[2] - u[2] * a[1], u[2] * a[0] - u[0] * a[2], u[0] * a[1] - u[1] * a[0]]
    ring = lambda c: [tuple(c[k] + d / 2 * (math.cos(2 * math.pi * j / n) * a[k] + math.sin(2 * math.pi * j / n) * b[k]) for k in range(3)) for j in range(n)]
    i = len(V) + 1; V.extend(world(*v) for v in ring(p) + ring(q))
    for j in range(n):
        j2 = (j + 1) % n; F.append((i + j, i + j2, i + n + j2, i + n + j)); MAT.append(CUR[0])
    F.append(tuple(i + j for j in range(n))[::-1]); F.append(tuple(i + n + j for j in range(n))); MAT.extend([CUR[0]] * 2)

def wall_x(xa, xb, y, t, z0, z1, holes):    # wall along x between z0 and z1, door holes [(x0, x1, top)]
    x = xa
    for a, b, top in sorted(holes):
        box(x, a, y - t / 2, y + t / 2, z0, z1)
        if top < z1: box(a, b, y - t / 2, y + t / 2, max(z0, top), z1)
        x = b
    box(x, xb, y - t / 2, y + t / 2, z0, z1)

# ---- rooms ----
rooms = []
x = -HL
for kind in NORTH: rooms.append(dict(kind=kind, x0=x, x1=x + L / len(NORTH), side=+1)); x += L / len(NORTH)
x = -HL
for kind, w in SOUTH: rooms.append(dict(kind=kind, x0=x, x1=x + w, side=-1)); x += w
for r in rooms: r['c'] = (r['x0'] + r['x1']) / 2

def sticks_x(xa, xb, y, z0, z1, holes):      # tomato stakes laid HORIZONTAL, bird's-nest style (Will, 27 Sep): loose courses with gaps,
    zz, k = z0 + .25, 0                           # each stake a little in or out and a little long or short, on light verticals every 4 ft
    while zz < z1 - .1:
        w = .08 * (1, -1, .5, -.5)[k % 4]; xs = xa
        segs = []
        for a, b, top in sorted(holes):
            if zz < top: segs.append((xs, a)); xs = b
        segs.append((xs, xb))
        for a, b in segs:
            if b - a > .3: box(a - (.3 if k % 3 == 0 else 0), b + (.3 if k % 3 == 1 else 0), y - STAKE_T / 2 + w, y + STAKE_T / 2 + w, zz, zz + STAKE_H)
        zz += STAKE_P; k += 1
    xv = xa
    while xv <= xb + .01:
        box(xv - .08, xv + .08, y - .1, y + .1, z0, z1); xv += 4.0

# ---- long walls: rock to 4.5 ft, woven sticks to the eave, a door per room ----
for s in (1, -1):
    y = s * HD
    holes = [(r['c'] - DOOR[0] / 2, r['c'] + DOOR[0] / 2, DOOR[1]) for r in rooms if r['side'] == s and r['kind'] != 'wash']   # the sketch: one door in the solid rooms (tack), none to the wash
    mat('rock'); wall_x(-HL, HL, y, ROCK_T, 0, ROCK_H, holes)
    solid = sorted((r['x0'], r['x1']) for r in rooms if r['side'] == s and r['kind'] in SOLID)
    xs = -HL
    for a, b in solid + [(HL, HL)]:                   # stakes between the solid rooms, infill across them
        if a > xs: mat('stakes'); sticks_x(xs, a, y, ROCK_H, EAVE - .3, [h for h in holes if xs <= h[0] < a])
        if b > a: mat('cob'); wall_x(a, b, y, ROCK_T * .8, ROCK_H, EAVE - .3, [h for h in holes if a <= h[0] < b])
        xs = b

# ---- gable ends: rock and stakes either side of the big entry; stakes fill the gable over the rooms ----
for sx in (-1, 1):
    x = sx * HL
    for s in (-1, 1):
        y0, y1 = sorted((s * ENTRY_W / 2, s * HD))
        mat('rock'); box(x - ROCK_T / 2, x + ROCK_T / 2, y0, y1, 0, ROCK_H)
        cob = any(r['side'] == s and r['kind'] in SOLID and abs(r['x0' if sx < 0 else 'x1'] - x) < .1 for r in rooms)   # gable wall of a solid room
        mat('cob' if cob else 'stakes'); zz, k = ROCK_H + (0 if cob else .25), 0                     # horizontal stakes stepping up under the rafter
        while True:
            ya, yb = y0, y1
            yin, yout = (ya, yb) if abs(ya) < abs(yb) else (yb, ya)          # the entry side stays, the outer end stops under the rafter
            lim = HD - (zz + STAKE_H - EAVE) / slope if zz + STAKE_H > EAVE else HD
            if lim <= abs(yin) + .5: break
            yo = math.copysign(min(abs(yout), lim - COL_D / 2), yout)
            w = 0 if cob else .08 * (1, -1, .5, -.5)[k % 4]
            if cob: box(x - ROCK_T * .4, x + ROCK_T * .4, min(yin, yo), max(yin, yo), zz, zz + STAKE_P)
            else: box(x - STAKE_T / 2 + w, x + STAKE_T / 2 + w, min(yin, yo), max(yin, yo), zz, zz + STAKE_H)
            zz += STAKE_P; k += 1

# ---- the frames: 12 in pipe columns and rafters, rafters run 2 ft past the columns ----
mat('steel')
for x in FRAMES:
    for s in (-1, 1):
        bar((x, s * HD, 0), (x, s * HD, EAVE), COL_D)
        bar((x, s * (HD + OH), roof_z(HD + OH)), (x, 0, RIDGE), COL_D)
# eave beams and purlins, 8 in pipe on top of the rafters, about 5 ft apart along the slope
top = COL_D / 2 + PURL_D / 2
run = HD + OH; n_p = 5
for s in (-1, 1):
    for k in range(n_p + 1):
        y = s * run * k / n_p
        if k == 0: y = s * 0.6
        bar((-HL, y, roof_z(y) + top), (HL, y, roof_z(y) + top), PURL_D, 6)
    bar((-HL, s * HD, EAVE - 0.2), (HL, s * HD, EAVE - 0.2), PURL_D, 6)      # eave beam at the column heads

# ---- roof: two sheets on the purlins, 2 ft past the walls on the long sides, a little thickness ----
T, zr = .25, top + PURL_D / 2
mat('roof')
for s in (-1, 1):
    y_out = s * (HD + OH)
    for dz in (0, T):
        quad((-HL - .5, y_out, roof_z(y_out) + zr + dz), (HL + .5, y_out, roof_z(y_out) + zr + dz),
             (HL + .5, 0, RIDGE + zr + dz), (-HL - .5, 0, RIDGE + zr + dz))

# ---- clerestory monitor along the ridge: glazing on both long sides, its own low gable roof above (27 Sep) ----
zb = roof_z(MON_HW) + zr
for sgn in (-1, 1):
    mat('glass'); box(-MON_X, MON_X, sgn * MON_HW - .1, sgn * MON_HW + .1, zb, zb + MON_H)
    mat('steel')
    for k in range(9): xm = -MON_X + 2 * MON_X * k / 8; box(xm - .2, xm + .2, sgn * MON_HW - .2, sgn * MON_HW + .2, zb, zb + MON_H)   # mullions
    mat('roof')
    for dz in (0, T):
        quad((-MON_X - .8, sgn * (MON_HW + 1), zb + MON_H - slope + dz), (MON_X + .8, sgn * (MON_HW + 1), zb + MON_H - slope + dz),
             (MON_X + .8, 0, zb + MON_H + slope * MON_HW + dz), (-MON_X - .8, 0, zb + MON_H + slope * MON_HW + dz))
for xm in (-MON_X, MON_X):
    mat('glass'); quad((xm, -MON_HW, zb), (xm, MON_HW, zb), (xm, MON_HW, zb + MON_H), (xm, -MON_HW, zb + MON_H))
    mat('roof'); quad((xm, -MON_HW, zb + MON_H), (xm, MON_HW, zb + MON_H), (xm, 0, zb + MON_H + slope * MON_HW), (xm, 0, zb + MON_H + slope * MON_HW))

# ---- inside: stall partitions to 4.5 ft with a grille look (solid here), rooms walled to 10 ft ----
mat('wood')
for s in (1, -1):
    rr = [r for r in rooms if r['side'] == s]
    y0, y1 = sorted((s * (HD - ROCK_T / 2), s * (HD - ROW_D)))
    for a, b in zip(rr, rr[1:]):
        h = ROCK_H if a['kind'] == b['kind'] == 'stall' else 10
        box(b['x0'] - .25, b['x0'] + .25, y0, y1, 0, h)
    yi = s * (HD - ROW_D)
    for r in rr:
        h = ROCK_H if r['kind'] == 'stall' else 10
        wall_x(r['x0'] + .1, r['x1'] - .1, yi, .4, 0, h, [(r['c'] - DOOR[0] / 2, r['c'] + DOOR[0] / 2, DOOR[1])])

# ---- runs: 12 x 40 ft off every stall on both sides, three-rail black pipe fence at 5 ft 6 in; the south ones climb at RUN_FALL ----
mat('fence')
P, R = .35, .2
for r in rooms:
    if r['kind'] != 'stall': continue
    sg = r['side']; lift = (lambda d: 0.0) if sg > 0 else (lambda d: RUN_FALL * d)          # d = ft out from the wall
    yw, ye = sg * (HD + ROCK_T / 2), sg * (HD + RUN_D)
    for x in (r['x0'], r['x1']):
        for k in range(5):
            d = RUN_D * k / 4; y = sg * (HD + ROCK_T / 2) + sg * (RUN_D - ROCK_T / 2) * k / 4
            box(x - P / 2, x + P / 2, y - P / 2, y + P / 2, lift(d), lift(d) + RAIL_H)
        for k in range(4):                                                                  # rails in four pieces so the south ones can step up the slope
            ya, yb = yw + (ye - yw) * k / 4, yw + (ye - yw) * (k + 1) / 4; dm = abs((ya + yb) / 2) - HD
            for h in (1.8, 3.6, RAIL_H - R): box(x - R / 2, x + R / 2, min(ya, yb), max(ya, yb), lift(dm) + h, lift(dm) + h + R)
    for h in (1.8, 3.6, RAIL_H - R): box(r['x0'], r['x1'], ye - R / 2, ye + R / 2, lift(RUN_D) + h, lift(RUN_D) + h + R)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'centro-equino-barn.obj')
with open(out, 'w', newline='\n') as f:
    f.write(f"# Centro Equino stable, 27 Sep: {L:.0f} x {D:.0f} ft pipe portal frames, rock 4.5 ft all round + horizontal tomato stakes, clerestory monitor {2*MON_X:.0f} ft along the ridge, gable entries, 2 ft overhangs, 6 stalls north + 4 south with 12x40 runs, tack/feed + wash at the west end (by the barn road) with solid straw-bale/cob infill above the rock\n")
    f.write(f"# geo {LAT} {LON}\n# unit ft\n# name walker barn 72x40\n")
    for v in V: f.write('v %.3f %.3f %.3f\n' % v)
    last = None
    for fc, m in zip(F, MAT):
        if m != last: f.write(f'usemtl {m}\n'); last = m
        f.write('f ' + ' '.join(map(str, fc)) + '\n')
print(out, len(V), 'verts', len(F), 'faces', f'{L:.0f} x {D:.0f} ft')
