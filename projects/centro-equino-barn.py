"""Walker's Centro Equino barn as an OBJ for the topo tool, built from the spec in her
artifact (claude.ai/artifact/7dHdStVCWd2rjz3UW1ezXq, 22 Sep 2026). Feet, z up, x east,
y north, already turned to her bearing; the origin is the barn centre. The # geo line
tells topo.html where on the earth the origin goes.

    python centro-equino-barn.py   ->  centro-equino-barn.obj
"""
import math, os

# ---- her spec (BARN / GEO in the artifact) ----
STALL, AISLE, ROW_D, RUN_D = 12, 14, 12, 30
WALL, DIVIDER, DADO, PARTITION = 2, 1.5, 4.5, 0.75
EAVE, RISE = 12, 5
AISLE_DOOR, STALL_DOOR, ROOM_DOOR = (10, 11), (4, 8), (4, 8)
RAIL_H = 5.5
ROWS = [  # north row first; sgn -1 = north in her frame (z south), +1 here = north
    {'side': +1, 'rooms': ['stall'] * 6},
    {'side': -1, 'rooms': ['wash', 'tack'] + ['stall'] * 4},
]
LAT, LON, GABLE = 32.0002846, -116.7632631, 65.84

INNER_L = 6 * STALL                      # 72
L = INNER_L + 2 * WALL                   # 76
D = 2 * ROW_D + AISLE + 2 * WALL         # 42
HL, HD = L / 2, D / 2

V, F = [], []
ROT = math.radians(90 - GABLE)           # long axis from east, counter-clockwise
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

def wall_x(xa, xb, y, t, h, holes):     # a wall along x with door holes [(x0, x1, dh)]
    x = xa
    for a, b, dh in sorted(holes):
        box(x, a, y - t / 2, y + t / 2, 0, h); box(a, b, y - t / 2, y + t / 2, dh, h); x = b
    box(x, xb, y - t / 2, y + t / 2, 0, h)
def wall_y(ya, yb, x, t, h, holes):
    y = ya
    for a, b, dh in sorted(holes):
        box(x - t / 2, x + t / 2, y, a, 0, h); box(x - t / 2, x + t / 2, a, b, dh, h); y = b
    box(x - t / 2, x + t / 2, y, yb, 0, h)

# rooms, laid out west to east from the inner face
rooms = []
for row in ROWS:
    s = row['side']; outer = s * (HD - WALL); inner = outer - s * ROW_D
    x = -INNER_L / 2
    for kind in row['rooms']:
        rooms.append({'kind': kind, 'x0': x, 'x1': x + STALL, 'side': s, 'outer': outer, 'inner': inner}); x += STALL

# long stone walls, a door per stall and one for the wash bay
for row in ROWS:
    s = row['side']
    holes = []
    for r in rooms:
        if r['side'] == s and r['kind'] in ('stall', 'wash'):
            c, (w, h) = (r['x0'] + r['x1']) / 2, (STALL_DOOR if r['kind'] == 'stall' else ROOM_DOOR)
            holes.append((c - w / 2, c + w / 2, h))
    wall_x(-HL, HL, s * (HD - WALL / 2), WALL, EAVE, holes)

# end walls with the aisle cut through, and the gable triangles over them
for sx in (-1, 1):
    x = sx * (HL - WALL / 2)
    wall_y(-HD + WALL, HD - WALL, x, WALL, EAVE, [(-AISLE_DOOR[0] / 2, AISLE_DOOR[0] / 2, AISLE_DOOR[1])])
    x0, x1 = x - WALL / 2, x + WALL / 2
    for xa in (x0, x1):
        i = len(V) + 1; V.extend(world(*p) for p in ((xa, -HD, EAVE), (xa, HD, EAVE), (xa, 0, EAVE + RISE))); F.append((i, i + 1, i + 2))
    quad((x0, -HD, EAVE), (x1, -HD, EAVE), (x1, 0, EAVE + RISE), (x0, 0, EAVE + RISE))
    quad((x0, 0, EAVE + RISE), (x1, 0, EAVE + RISE), (x1, HD, EAVE), (x0, HD, EAVE))

# dividers: stone dado between stalls, a timber partition beside wash and tack
for row in ROWS:
    rr = [r for r in rooms if r['side'] == row['side']]
    for a, b in zip(rr, rr[1:]):
        y0, y1 = sorted((b['inner'], b['outer']))
        if a['kind'] == b['kind'] == 'stall': box(b['x0'] - DIVIDER / 2, b['x0'] + DIVIDER / 2, y0, y1, 0, DADO)
        else: box(b['x0'] - PARTITION / 2, b['x0'] + PARTITION / 2, y0, y1, 0, 10)

# fronts onto the aisle: boarded stall fronts to the dado, full timber walls for wash and tack
for r in rooms:
    y = r['inner']; c = (r['x0'] + r['x1']) / 2
    if r['kind'] == 'stall':
        wall_x(r['x0'] + .1, r['x1'] - .1, y, .4, DADO, [(c - STALL_DOOR[0] / 2, c + STALL_DOOR[0] / 2, DADO)])
    else:
        wall_x(r['x0'], r['x1'], y, PARTITION, 10, [(c - ROOM_DOOR[0] / 2, c + ROOM_DOOR[0] / 2, ROOM_DOOR[1])])

# roof: two metal planes to a ridge on the long axis, no overhang, a little thickness so it reads from below
T = .3
for s in (-1, 1):
    for z in (0, T):
        quad((-HL, s * HD, EAVE + z), (HL, s * HD, EAVE + z), (HL, 0, EAVE + RISE + z), (-HL, 0, EAVE + RISE + z))

# runs: 12 x 30 ft off every stall, three-rail pipe fence at 5 ft 6 in
P, R = .35, .2
for r in rooms:
    if r['kind'] != 'stall': continue
    s = r['side']; yw, ye = s * HD, s * (HD + RUN_D)
    for x in (r['x0'], r['x1']):
        for k in range(4): y = yw + (ye - yw) * k / 3; box(x - P / 2, x + P / 2, min(y, y) - P / 2, y + P / 2, 0, RAIL_H)
        for h in (1.8, 3.6, RAIL_H - R): box(x - R / 2, x + R / 2, min(yw, ye), max(yw, ye), h, h + R)
    for h in (1.8, 3.6, RAIL_H - R): box(r['x0'], r['x1'], ye - R / 2, ye + R / 2, h, h + R)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'centro-equino-barn.obj')
with open(out, 'w', newline='\n') as f:
    f.write(f"# Centro Equino barn, from Walker's spec: {L} x {D} ft stone, eave {EAVE}, ridge {EAVE + RISE}, ten 12x12 stalls, 14 ft aisle, 12x30 runs\n")
    f.write(f"# geo {LAT} {LON}\n# unit ft\n# name walker barn 76x42\n")
    for v in V: f.write('v %.3f %.3f %.3f\n' % v)
    for fc in F: f.write('f ' + ' '.join(map(str, fc)) + '\n')
print(out, len(V), 'verts', len(F), 'faces', f'{L} x {D} ft')
