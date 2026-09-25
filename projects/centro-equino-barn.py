"""Walker's Centro Equino stable as an OBJ for the topo tool, 24 Sep 2026 design:
72 x 40 ft on 12 in pipe portal frames (4 frames at 24 ft), stacked rock to 4.5 ft all round,
tomato-stake walls above, a big entry at both gable ends, metal roof with 2 ft overhangs on the
long sides, 8 in pipe purlins and eave beams. Walker's layout: 6 stalls north with 12 x 40 ft runs,
wash / tack / feed / alfalfa-storage south, 14 ft aisle. Feet, z up, x along the long axis, y north,
turned to her bearing; the origin is the barn centre. The # geo line tells topo.html where it goes.

    python centro-equino-barn.py   ->  centro-equino-barn.obj
(The 76 x 42 ten-stall version is kept as centro-equino-barn-76x42.obj.)
"""
import math, os

L, D = 72.0, 40.0                        # column centre lines
HL, HD = L / 2, D / 2
AISLE, STALL, RUN_D = 14.0, 12.0, 40.0
ROW_D = (D - AISLE) / 2                  # 13 ft
EAVE, RIDGE, OH = 12.0, 17.0, 2.0
ROCK_H, ROCK_T, STICK_T = 4.5, 1.5, 0.4
FRAMES = [-36.0, -12.0, 12.0, 36.0]
COL_D, PURL_D = 12.75 / 12, 8.625 / 12
ENTRY_W = AISLE                          # the big gable entries, open up to the rafters
DOOR = (4.0, 8.0)
RAIL_H = 5.5
NORTH = ['stall'] * 6
SOUTH = [('wash', 12), ('tack', 12), ('feed', 12), ('alfalfa', 36)]
LAT, LON, GABLE = 32.0002846, -116.7632631, 65.84

slope = (RIDGE - EAVE) / HD
def roof_z(y): return RIDGE - slope * abs(y)       # rafter centre line

V, F = [], []
ROT = math.radians(90 - GABLE)
rc, rs = math.cos(ROT), math.sin(ROT)
def world(x, y, z): return (x * rc - y * rs, x * rs + y * rc, z)

def quad(a, b, c, d):
    i = len(V) + 1; V.extend(world(*p) for p in (a, b, c, d)); F.append((i, i + 1, i + 2, i + 3))
def box(x0, x1, y0, y1, z0, z1):
    if x1 - x0 < 1e-6 or y1 - y0 < 1e-6 or z1 - z0 < 1e-6: return
    i = len(V) + 1
    for z in (z0, z1):
        for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)): V.append(world(x, y, z))
    for f in ((0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)):
        F.append(tuple(i + k for k in f))
def bar(p, q, d, n=8):                   # a round-ish tube from p to q
    p, q = [float(v) for v in p], [float(v) for v in q]
    ax_ = [q[k] - p[k] for k in range(3)]; Ln = math.sqrt(sum(a * a for a in ax_)); u = [a / Ln for a in ax_]
    t = [0, 0, 1] if abs(u[2]) < .9 else [1, 0, 0]
    a = [u[1] * t[2] - u[2] * t[1], u[2] * t[0] - u[0] * t[2], u[0] * t[1] - u[1] * t[0]]; na = math.sqrt(sum(v * v for v in a)); a = [v / na for v in a]
    b = [u[1] * a[2] - u[2] * a[1], u[2] * a[0] - u[0] * a[2], u[0] * a[1] - u[1] * a[0]]
    ring = lambda c: [tuple(c[k] + d / 2 * (math.cos(2 * math.pi * j / n) * a[k] + math.sin(2 * math.pi * j / n) * b[k]) for k in range(3)) for j in range(n)]
    i = len(V) + 1; V.extend(world(*v) for v in ring(p) + ring(q))
    for j in range(n):
        j2 = (j + 1) % n; F.append((i + j, i + j2, i + n + j2, i + n + j))
    F.append(tuple(i + j for j in range(n))[::-1]); F.append(tuple(i + n + j for j in range(n)))

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
for kind in NORTH: rooms.append(dict(kind=kind, x0=x, x1=x + STALL, side=+1)); x += STALL
x = -HL
for kind, w in SOUTH: rooms.append(dict(kind=kind, x0=x, x1=x + w, side=-1)); x += w
for r in rooms: r['c'] = (r['x0'] + r['x1']) / 2

# ---- long walls: rock to 4.5 ft, stakes to the eave, a door per room ----
for s in (1, -1):
    y = s * HD
    holes = [(r['c'] - DOOR[0] / 2, r['c'] + DOOR[0] / 2, DOOR[1]) for r in rooms if r['side'] == s]
    wall_x(-HL, HL, y, ROCK_T, 0, ROCK_H, holes)
    wall_x(-HL, HL, y, STICK_T, ROCK_H, EAVE, holes)

# ---- gable ends: rock and stakes either side of the big entry; stakes fill the gable over the rooms ----
for sx in (-1, 1):
    x = sx * HL
    for s in (-1, 1):
        y0, y1 = sorted((s * ENTRY_W / 2, s * HD))
        box(x - ROCK_T / 2, x + ROCK_T / 2, y0, y1, 0, ROCK_H)
        n = 6                               # stake panel stepped up under the rafter
        for k in range(n):
            ya, yb = y0 + (y1 - y0) * k / n, y0 + (y1 - y0) * (k + 1) / n
            box(x - STICK_T / 2, x + STICK_T / 2, ya, yb, ROCK_H, roof_z((ya + yb) / 2) - COL_D / 2)

# ---- the frames: 12 in pipe columns and rafters, rafters run 2 ft past the columns ----
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
for s in (-1, 1):
    y_out = s * (HD + OH)
    for dz in (0, T):
        quad((-HL - .5, y_out, roof_z(y_out) + zr + dz), (HL + .5, y_out, roof_z(y_out) + zr + dz),
             (HL + .5, 0, RIDGE + zr + dz), (-HL - .5, 0, RIDGE + zr + dz))

# ---- inside: stall partitions to 4.5 ft with a grille look (solid here), rooms walled to 10 ft ----
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

# ---- runs: 12 x 40 ft off every north stall, three-rail pipe fence at 5 ft 6 in ----
P, R = .35, .2
for r in rooms:
    if r['kind'] != 'stall': continue
    yw, ye = HD + ROCK_T / 2, HD + RUN_D
    for x in (r['x0'], r['x1']):
        for k in range(5): y = yw + (ye - yw) * k / 4; box(x - P / 2, x + P / 2, y - P / 2, y + P / 2, 0, RAIL_H)
        for h in (1.8, 3.6, RAIL_H - R): box(x - R / 2, x + R / 2, yw, ye, h, h + R)
    for h in (1.8, 3.6, RAIL_H - R): box(r['x0'], r['x1'], ye - R / 2, ye + R / 2, h, h + R)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'centro-equino-barn.obj')
with open(out, 'w', newline='\n') as f:
    f.write(f"# Centro Equino stable, 24 Sep design: {L:.0f} x {D:.0f} ft pipe portal frames, rock 4.5 ft + tomato stakes, gable entries, 2 ft overhangs, 6 stalls + 12x40 runs north\n")
    f.write(f"# geo {LAT} {LON}\n# unit ft\n# name walker barn 72x40\n")
    for v in V: f.write('v %.3f %.3f %.3f\n' % v)
    for fc in F: f.write('f ' + ' '.join(map(str, fc)) + '\n')
print(out, len(V), 'verts', len(F), 'faces', f'{L:.0f} x {D:.0f} ft')
