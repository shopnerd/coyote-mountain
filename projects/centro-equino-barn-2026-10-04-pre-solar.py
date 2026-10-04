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

L, D = 72.0, 42.0                        # 27 Sep: a 12 ft grid (Will: trusses 12 ft apart, things lined up): 6 bays x 12 = 72 ft (Walker's sketch had 76); gable 14 + 14 entry + 14
HL, HD = L / 2, D / 2
AISLE, STALL, RUN_D = 14.0, 12.0, 40.0
ROW_D = (D - AISLE) / 2                  # 14 ft
EAVE, RIDGE, OH = 12.0, 17.0, 2.0
ROCK_H, ROCK_T, STICK_T = 5.0, 1.5, 0.4    # 27 Sep (Will): rock walls 5 ft, a pipe floating 1 ft above them (6 ft overall)
RAIL_Z, PIPE = 6.0, .2                      # top of that pipe, pipe size (ft)
STAKES = True                              # horizontal stakes in dark steel frames above the rail, to the eave (Will's reference photo, 27 Sep)
FRAMES = [-38.0, -19.0, 0.0, 19.0, 38.0]   # 5 frames at 19 ft
COL_D, PURL_D = 12.75 / 12, 8.625 / 12
ENTRY_W = AISLE                          # the big gable entries, open up to the rafters
DOOR = (6.0, 9.0)                        # open doorways stall -> run, no gate (27 Sep): 6 ft wide between two 3 ft panel posts, 9 ft tall
RAIL_H = 5.5
MON_HW, MON_H, MON_X = 5.0, 2.5, 24.0   # clerestory monitor: half width, glazing height, half length (27 Sep)
STAKE_H, STAKE_T, STAKE_P = .12, .16, .3   # tomato stakes, horizontal: height, thickness, course spacing (gaps between)
NORTH = ['stall'] * 6                    # 6 x 12 ft, one per truss bay
SOUTH = [('wash', 12), ('tack / feed', 12)] + [('stall', 12)] * 4   # 28 Sep (Will markup): wash room at the west corner, its 6 x 9 door right by the entry   # 27 Sep (Will): rooms at the WEST end by the barn road, so the open ground is by the road; 4 stalls with runs east of them
SOLID = ('tack / feed', 'wash')           # both rooms at the road end closed (27 Sep, Will's markup: 'enclose the tack room as well')           # Walker's elevation: solid infill above the rock at the rooms (straw bale or cob, plastered), not stakes
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

def sticks_x(xa, xb, y, z0, z1, holes):      # 3 Oct (Will + Walker): sticks cut to ONE common length, laid horizontal in 3 ft
    n = max(1, round((xb - xa) / 3))               # steel-framed panels; each course is a row of panel-length sticks, a little in/out
    edges = [xa + (xb - xa) * q / n for q in range(n + 1)]
    zz, k = z0 + .25, 0
    while zz < z1 - .1:
        w = .06 * (1, -1, .5, -.5)[k % 4]
        for pa, pb in zip(edges, edges[1:]):
            if any(ha < (pa + pb) / 2 < hb and zz < top for ha, hb, top in holes): continue
            box(pa + .12, pb - .12, y - STAKE_T / 2 + w, y + STAKE_T / 2 + w, zz, zz + STAKE_H)
        zz += STAKE_P; k += 1
    keep = CUR[0]; mat('steel')                     # dark steel frame: posts every ~4 ft, top and bottom members
    n = max(1, round((xb - xa) / 3))                # stake panels 3 ft wide (Walker)
    for k in range(n + 1):
        xv = xa + (xb - xa) * k / n; zb_ = max([top for a, b, top in holes if a + .05 < xv < b - .05] + [z0])
        box(xv - .1, xv + .1, y - .12, y + .12, zb_, z1)
    xs_ = xa
    for a, b, top in sorted(holes): box(xs_, a, y - .12, y + .12, z0, z0 + .15); xs_ = b
    box(xs_, xb, y - .12, y + .12, z0, z0 + .15); box(xa, xb, y - .12, y + .12, z1 - .15, z1)
    mat(keep)

# ---- walls (27 Sep, Will): rock 5 ft all round, a black pipe floating 1 ft above on short pipe posts, open above;
# the tack room alone is closed to the roof (straw bale / cob, plastered). Pipe gates from each stall to its run.
def rail_x(xa, xb, y):                        # the floating pipe along x, with short posts down to the rock every ~6 ft
    if xb - xa < .3: return
    mat('fence'); box(xa, xb, y - PIPE / 2, y + PIPE / 2, RAIL_Z - PIPE, RAIL_Z)
    n = max(1, round((xb - xa) / 6))
    for k in range(n + 1): xp = xa + (xb - xa) * k / n; box(xp - PIPE / 2, xp + PIPE / 2, y - PIPE / 2, y + PIPE / 2, ROCK_H, RAIL_Z)
def rail_y(ya, yb, x):
    if yb - ya < .3: return
    mat('fence'); box(x - PIPE / 2, x + PIPE / 2, ya, yb, RAIL_Z - PIPE, RAIL_Z)
    n = max(1, round((yb - ya) / 6))
    for k in range(n + 1): yp = ya + (yb - ya) * k / n; box(x - PIPE / 2, x + PIPE / 2, yp - PIPE / 2, yp + PIPE / 2, ROCK_H, RAIL_Z)
def gate_x(xa, xb, y, h=RAIL_Z):              # a pipe gate across an opening along x: two stiles and four rails
    mat('fence')
    for xx in (xa, xb): box(xx - PIPE / 2, xx + PIPE / 2, y - PIPE / 2, y + PIPE / 2, .4, h)
    for zz in (.6, 2.4, 4.2, h - PIPE): box(xa, xb, y - PIPE / 2, y + PIPE / 2, zz, zz + PIPE)
TACK_DOOR = (4.0, 8.0)                        # inside doors to the aisle
WASH_DOOR = (6.0, 9.0)                        # the one outside door, into the wash room (Walker, gallery note 28 Sep)
for s in (1, -1):
    y = s * HD; holes, solid = [], []
    for r in rooms:
        if r['side'] != s: continue
        if r['kind'] == 'stall': holes.append((r['c'] - DOOR[0] / 2, r['c'] + DOOR[0] / 2, 99))           # open doorway to the run
        elif r['kind'] in SOLID:
            solid.append((r['x0'], r['x1']))
            if r['kind'] == 'wash': holes.append((r['c'] - WASH_DOOR[0] / 2, r['c'] + WASH_DOOR[0] / 2, WASH_DOOR[1]))   # the one outside door: 6 x 9 ft into the wash room
    mat('rock'); wall_x(-HL, HL, y, ROCK_T, 0, ROCK_H, [(a, b, t if t != 99 else ROCK_H) for a, b, t in holes])
    for a, b, t in holes:
        if t == 99: mat('steel'); box(a, b, y - .12, y + .12, DOOR[1], DOOR[1] + .25)                   # lintel over the doorway
    xs = -HL
    for a, b in sorted(solid) + [(HL, HL)]:
        xx = xs
        for ha, hb, _ in sorted(h for h in holes if h[2] == 99 and xs <= h[0] < a): rail_x(xx, ha, y); xx = hb
        rail_x(xx, a, y)
        if STAKES and a > xs: mat('stakes'); sticks_x(xs, a, y, RAIL_Z, EAVE - .3, [(ha, hb, DOOR[1] + .25) for ha, hb, t in holes if t == 99 and xs <= ha < a])   # stakes stop at the doorways, carry on above the lintel
        if b > a: mat('cob'); wall_x(a, b, y, ROCK_T * .8, ROCK_H, EAVE - .3, [h for h in holes if a <= h[0] < b])
        xs = b

# ---- gable ends: rock and rail either side of the big entry; the tack room's gable bay solid up to the truss;
# ---- wooden sliding door on the wash room's outside opening (Will, 3 Oct, from the 28 Sep 'stable from the road' painting):
# a 7 x 9.3 ft plank leaf hung on a steel track above the 6 x 9 opening, parked open to the EAST of it over the plastered wall ----
wr_ = [r for r in rooms if r['kind'] == 'wash'][0]
yd = -HD - ROCK_T / 2 - .3                                                                  # just outside the south wall face
da, db = wr_['c'] - WASH_DOOR[0] / 2, wr_['c'] + WASH_DOOR[0] / 2
mat('steel'); box(da - .5, db + 7.6, yd - .15, yd + .15, WASH_DOOR[1] + .6, WASH_DOOR[1] + .9)      # the track (wash pad sliding door)
for xx in (db + .9, db + 6.7): box(xx - .1, xx + .1, yd - .1, yd + .1, WASH_DOOR[1] + .3, WASH_DOOR[1] + .6)   # hangers
mat('wood')
for k in range(7): xk = db + .3 + k * 1.0; box(xk + .03, xk + .97, yd - .12, yd + .12, .15, WASH_DOOR[1] + .3)   # vertical planks
for zz in (.6, WASH_DOOR[1] / 2 - .25, WASH_DOOR[1] - .6): box(db + .3, db + 7.3, yd - .24, yd - .12, zz, zz + .5)   # ledges on the outside face
# a big sliding door at each end (two leaves on a track above the entry, shown parked open over the rock) ----
for sx in (-1, 1):
    x = sx * HL
    for s in (-1, 1):
        y0, y1 = sorted((s * ENTRY_W / 2, s * HD))
        mat('rock'); box(x - ROCK_T / 2, x + ROCK_T / 2, y0, y1, 0, ROCK_H)
        cob = any(r['side'] == s and r['kind'] in SOLID and abs(r['x0' if sx < 0 else 'x1'] - x) < .1 for r in rooms)
        if cob: mat('cob'); box(x - ROCK_T * .4, x + ROCK_T * .4, y0, y1, ROCK_H, EAVE - .3)
        else:
            rail_y(y0, y1, x)
            if STAKES:                         # framed stakes on the gable bays too, up to the eave
                mat('stakes'); zz, k = RAIL_Z + .25, 0; n = max(1, round((y1 - y0) / 3)); E = [y0 + (y1 - y0) * q / n for q in range(n + 1)]
                while zz < EAVE - .4:
                    w = .06 * (1, -1, .5, -.5)[k % 4]
                    for pa, pb in zip(E, E[1:]): box(x - STAKE_T / 2 + w, x + STAKE_T / 2 + w, pa + .12, pb - .12, zz, zz + STAKE_H)
                    zz += STAKE_P; k += 1
                mat('steel')
                for q in range(n + 1): yv = y0 + (y1 - y0) * q / n; box(x - .12, x + .12, yv - .1, yv + .1, RAIL_Z, EAVE - .3)
                for zz in (RAIL_Z, EAVE - .45): box(x - .12, x + .12, y0, y1, zz, zz + .15)
    xo = x + sx * (ROCK_T / 2 + .35)
    mat('steel'); box(min(xo, xo + sx * .2), max(xo, xo + sx * .2), -HD + 1, HD - 1, EAVE - .2, EAVE + .2)          # the door track
    for s in (-1, 1):                          # leaves 7.5 x 11.5 ft: a steel frame clad in the same common-length sticks (3 Oct)
        ya, yb = sorted((s * (ENTRY_W / 2 + .3), s * (ENTRY_W / 2 + 7.8)))
        xa_, xb_ = min(xo, xo + sx * .3), max(xo, xo + sx * .3); xm = (xa_ + xb_) / 2
        mat('steel')
        for yy in (ya, (ya + yb) / 2, yb): box(xa_, xb_, yy - .12, yy + .12, .3, EAVE - .2)          # stiles + a centre stile
        for zz in (.3, (EAVE - .2 + .3) / 2, EAVE - .35): box(xa_, xb_, ya, yb, zz, zz + .15)        # rails
        mat('stakes'); zz, k = .55, 0; E = [ya, (ya + yb) / 2, yb]
        while zz < EAVE - .5:
            w = .05 * (1, -1)[k % 2]
            for pa, pb in zip(E, E[1:]): box(xm - STAKE_T / 2 + w, xm + STAKE_T / 2 + w, pa + .12, pb - .12, zz, zz + STAKE_H)
            zz += STAKE_P; k += 1

# ---- gable triangles above the end trusses (3 Oct): closed with the same framed stick panels, eave to ridge ----
for sx in (-1, 1):
    x = sx * HL; xi = x - sx * .3                                            # just inside the end truss
    n = round(2 * HD / 3); E = [-HD + 2 * HD * q / n for q in range(n + 1)]
    zz, k = EAVE + .25, 0
    mat('stakes')
    while zz < RIDGE - .3:
        lim = HD - (zz + STAKE_H - EAVE) / slope                             # half-width under the rafters at this height
        w = .06 * (1, -1, .5, -.5)[k % 4]
        for pa, pb in zip(E, E[1:]):
            a, b = max(pa + .12, -lim), min(pb - .12, lim)
            if b - a > .4: box(xi - STAKE_T / 2 + w, xi + STAKE_T / 2 + w, a, b, zz, zz + STAKE_H)
        zz += STAKE_P; k += 1
    mat('steel')
    for yv in E[1:-1]: box(xi - .1, xi + .1, yv - .1, yv + .1, EAVE, roof_z(yv))      # frame verticals up to the rafter

# ---- structure (27 Sep, Will): steel trusses on steel posts (4 Oct: Andrés’ heavy 12 in tubes, see POST) instead of the pipe portal frames, one at every
# north stall line (7 lines, 12.7 ft apart): top chords, a bottom chord at the eave, king post, verticals and webs ----
TRUSS = [-HL + L * k / 6 for k in range(7)]
POST = 12.75 / 12                               # 4 Oct (Will): back to Andrés' heavy 12 in tubes (12 3/4 in OD), as first planned; was 6 in pipe
for x in TRUSS:
    mat('steel')
    for s in (-1, 1): bar((x, s * HD, 0), (x, s * HD, EAVE), POST, 10)
    mat('truss')                                                                                                 # 4 Oct: roof structure gets its own tag so the viewer can hide it
    for s in (-1, 1): bar((x, s * (HD + OH), roof_z(HD + OH)), (x, 0, RIDGE), .5, 12)                            # top chords
    bar((x, -HD, EAVE), (x, HD, EAVE), .4, 8)                                                                     # bottom chord
    bar((x, 0, EAVE), (x, 0, RIDGE), .3, 6)                                                                       # king post
    for k in (1, 2, 3):
        for s in (-1, 1):
            yv = s * HD * k / 4; yw = s * HD * (k - 1) / 4
            bar((x, yv, EAVE), (x, yv, roof_z(yv)), .25, 6)                                                        # verticals
            bar((x, yv, EAVE), (x, yw, roof_z(yw)), .22, 6)                                                        # webs toward the ridge
mat('truss')
# eave beams and purlins, 8 in pipe on top of the rafters, about 5 ft apart along the slope
top = .5 / 2 + PURL_D / 2                      # 4 Oct (Will): purlins sit ON the .5 ft top chords (COL_D was the old pipe rafter; it left a 3 in gap)
run = HD + OH; n_p = 5
for s in (-1, 1):
    for k in range(n_p + 1):
        y = s * run * k / n_p
        if k == 0: y = s * 0.6
        bar((-HL - 2.0 + .3, y, roof_z(y) + top), (HL + 2.0 - .3, y, roof_z(y) + top), PURL_D, 16)   # purlins carry the 2 ft gable overhang   # round, not hexagonal (Will, 4 Oct)
    bar((-HL, s * HD, EAVE - 0.2), (HL, s * HD, EAVE - 0.2), PURL_D, 16)      # eave beam at the column heads

# ---- roof: two sheets on the purlins, 2 ft past the walls on the long sides, a little thickness ----
T, zr = .25, top + PURL_D / 2
GOH = 2.0                                        # 4 Oct (Will): 2 ft overhang at the gable ends too (long sides already OH = 2)
mat('roof')
for s in (-1, 1):
    y_out = s * (HD + OH)
    for dz in (0, T):
        quad((-HL - GOH, y_out, roof_z(y_out) + zr + dz), (HL + GOH, y_out, roof_z(y_out) + zr + dz),
             (HL + GOH, 0, RIDGE + zr + dz), (-HL - GOH, 0, RIDGE + zr + dz))

# ---- clerestory monitor along the ridge: glazing on both long sides, its own low gable roof above (27 Sep) ----
zb = roof_z(MON_HW) + zr
for sgn in (-1, 1):
    mat('truss')   # 4 Oct: clerestory mullions are roof structure too
    for k in range(int(2 * MON_X / 6) + 1): xm = -MON_X + 6 * k; box(xm - .2, xm + .2, sgn * MON_HW - .2, sgn * MON_HW + .2, zb, zb + MON_H)   # mullions
    mat('roof')
    for dz in (0, T):
        quad((-MON_X - .8, sgn * (MON_HW + 1), zb + MON_H - slope + dz), (MON_X + .8, sgn * (MON_HW + 1), zb + MON_H - slope + dz),
             (MON_X + .8, 0, zb + MON_H + slope * MON_HW + dz), (-MON_X - .8, 0, zb + MON_H + slope * MON_HW + dz))
for xm in (-MON_X, MON_X):
    mat('roof'); quad((xm, -MON_HW, zb + MON_H), (xm, MON_HW, zb + MON_H), (xm, 0, zb + MON_H + slope * MON_HW), (xm, 0, zb + MON_H + slope * MON_HW))

# ---- inside (27 Sep): stall partitions 5 ft wood with the floating pipe above (6 ft), pipe fronts with a pipe gate
# to the aisle; the tack room walled to the eave with a door; the wash bay open to the aisle ----
for s in (1, -1):
    rr = [r for r in rooms if r['side'] == s]
    y0, y1 = sorted((s * (HD - ROCK_T / 2), s * (HD - ROW_D)))
    for a, b in zip(rr, rr[1:]):
        if a['kind'] in SOLID or b['kind'] in SOLID: mat('cob'); box(b['x0'] - .3, b['x0'] + .3, y0, y1, 0, EAVE - .3)
        else: mat('rock'); box(b['x0'] - .6, b['x0'] + .6, y0, y1, 0, ROCK_H); rail_y(y0, y1, b['x0'])   # stall partitions: 5 ft stacked rock (Will, 28 Sep)
    yi = s * (HD - ROW_D)
    for r in rr:
        if r['kind'] in SOLID:
            mat('cob'); wall_x(r['x0'] + .1, r['x1'] - .1, yi, .6, 0, EAVE - .3, [(r['c'] - TACK_DOOR[0] / 2, r['c'] + TACK_DOOR[0] / 2, TACK_DOOR[1])])
        elif r['kind'] == 'stall':
            ga, gb = r['c'] - 2.5, r['c'] + 2.5
            mat('fence')
            for xx in (r['x0'] + .2, r['x1'] - .2): box(xx - PIPE / 2, xx + PIPE / 2, yi - PIPE / 2, yi + PIPE / 2, 0, RAIL_Z)
            for xa, xb in ((r['x0'] + .2, ga), (gb, r['x1'] - .2)):
                for zz in (.6, 2.4, 4.2, RAIL_Z - PIPE): box(xa, xb, yi - PIPE / 2, yi + PIPE / 2, zz, zz + PIPE)
            gate_x(ga, gb, yi)

# ---- 4 Oct (Will): wooden swing doors on the wash room and the tack room, into the aisle wall's door holes. Plank leaves like the
# outside sliding door (7 vertical boards, 3 ledges), hung on the jamb nearer the gable, standing open ~50 deg into the room ----
def swing_door(hx, hy, w, h, ang, into):
    """leaf hinged at (hx, hy) on the aisle wall line, swung by ang (rad) toward `into` (+1/-1 in y); boards along the leaf"""
    ux, uy = math.cos(ang), into * math.sin(ang); nx, ny = -uy * .06, ux * .06         # along the leaf, and half its thickness
    def slab(a, b, z0, z1):
        p0 = (hx + ux * a, hy + uy * a); p1 = (hx + ux * b, hy + uy * b)
        c = [(p0[0] - nx, p0[1] - ny), (p1[0] - nx, p1[1] - ny), (p1[0] + nx, p1[1] + ny), (p0[0] + nx, p0[1] + ny)]
        i = len(V) + 1
        for zz in (z0, z1):
            for x, y in c: V.append(world(x, y, zz))
        for f in ((0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 6, 7, 3), (3, 7, 4, 0)): F.append(tuple(i + k for k in f)); MAT.append(CUR[0])
    mat('wood'); n = 7
    for k in range(n): slab(k * w / n + .02, (k + 1) * w / n - .02, .1, h - .1)                 # boards
    for zz in (.5, h / 2 - .25, h - .75): slab(.05, w - .05, zz, zz + .45)                      # ledges
    mat('steel')
    for zz in (1.2, h - 1.2): slab(-.05, .25, zz, zz + .3)                                      # strap hinges at the jamb
for s_ in (1, -1):
    for r in [r_ for r_ in rooms if r_['side'] == s_ and r_['kind'] in SOLID]:
        yi_ = s_ * (HD - ROW_D); hinge_x = r['c'] - TACK_DOOR[0] / 2 if r['c'] < 0 else r['c'] + TACK_DOOR[0] / 2
        a_ = 0.0 if r['c'] < 0 else math.pi                                                         # shown CLOSED in the wall plane so the plank face reads from the aisle (swings into the room)
        swing_door(hinge_x, yi_, TACK_DOOR[0], TACK_DOOR[1], a_, s_)

# ---- concrete wash pad (Walker, 28 Sep): 12 x 24 ft running parallel to the barn outside the wash-room door, on the south side ----
mat('concrete')
wr = [r for r in rooms if r['kind'] == 'wash'][0]
box(-HL, -HL + 24, -HD - ROCK_T / 2 - 12, -HD - ROCK_T / 2, 0.0, 0.35)          # along the two rooms, clear of the first run; the wash door opens onto it
# ---- 4 Oct (Walker, via Will): a pipe trellis over the whole wash pad with grapes on it, like the ranch's other arbours. Steel pipe
# like the buildings: 4 in posts at the pad's south edge, a 3 in beam there and a 3 in ledger on the wall posts, 2 in cross pipes every
# 3 ft, three wires; the vine as a loose leaf canopy. Deck at 10.3 ft clears the sliding door's track (9.9 ft); the eave is 12. ----
import random as _rnd
TR_H = 10.3
py0, py1 = -HD - ROCK_T / 2 - 12, -HD - ROCK_T / 2
mat('steel')
for x in (-HL + .5, -HL + 12, -HL + 24 - .5): bar((x, py0 + .5, 0), (x, py0 + .5, TR_H), 4.5 / 12, 10)          # posts
bar((-HL, py0 + .5, TR_H), (-HL + 24, py0 + .5, TR_H), 3.5 / 12, 10)                                              # south beam
bar((-HL, py1 - .3, TR_H), (-HL + 24, py1 - .3, TR_H), 3.5 / 12, 10)                                              # ledger on the wall posts
for k in range(9): xx = -HL + 24 * k / 8; bar((xx, py0 + .5, TR_H + .22), (xx, py1 - .3, TR_H + .22), 2.0 / 12, 8)   # cross pipes
for k in range(1, 4): yy = py0 + .5 + (py1 - .8 - py0) * k / 4; bar((-HL, yy, TR_H + .4), (-HL + 24, yy, TR_H + .4), .6 / 12, 6)   # wires
mat('sage'); _rv = _rnd.Random(5)
for _ in range(80):                                                                                                 # the grapevine canopy
    xx = _rv.uniform(-HL + .4, -HL + 23.6); yy = _rv.uniform(py0 + .9, py1 - .5); rr = _rv.uniform(.9, 1.7)
    box(xx - rr, xx + rr, yy - rr * .75, yy + rr * .75, TR_H + .4, TR_H + .4 + _rv.uniform(.5, 1.2))
# ---- tie-ups on the wash pad (Will approved sketch v2, 4 Oct night). The sliding door parks east of the opening, so nothing ties to
# the wall there: W one ring on the SW corner post (head at the corner, tail to the trough, nothing at the tail end), M a 3 in pipe
# hoop bent like a big upside-down C on the pad's centre line, 2 ft off the wall so the door passes behind, E rings on run 1's fence ----
def tie_ring(cx, cy, cz, face):                          # a 5 in steel ring standing off a post, its plane facing `face` ('x' or 'y')
    mat('steel'); n_ = 10; rr_ = 5 / 24
    for k in range(n_):
        a0, a1 = 2 * math.pi * k / n_, 2 * math.pi * (k + 1) / n_
        if face == 'y': p0, p1 = (cx + rr_ * math.cos(a0), cy, cz + rr_ * math.sin(a0)), (cx + rr_ * math.cos(a1), cy, cz + rr_ * math.sin(a1))
        else: p0, p1 = (cx, cy + rr_ * math.cos(a0), cz + rr_ * math.sin(a0)), (cx, cy + rr_ * math.cos(a1), cz + rr_ * math.sin(a1))
        bar(p0, p1, .05, 5)
WALL_O = -HD - ROCK_T / 2                                # outside face of the south wall
bar((-HL, -HD - POST / 2 + .05, 6.0), (-HL, WALL_O - .45, 6.0), .1, 6); tie_ring(-HL, WALL_O - .62, 6.0, 'y')   # 4 Oct (Will): W ring on a stub welded to the corner post, 6 ft
mat('steel'); HY0, HY1, HH, HB = WALL_O - 2.0, WALL_O - 10.0, 4.5, 1.0     # M: hoop on x = -24, from 2 ft to 10 ft off the wall
HX = -HL + 12
bar((HX, HY0, -.2), (HX, HY0, HH - HB), 3.5 / 12, 10); bar((HX, HY1, -.2), (HX, HY1, HH - HB), 3.5 / 12, 10)
for k in range(4):                                       # the two 12 in bends, four pieces each
    a0, a1 = math.pi / 2 * k / 4, math.pi / 2 * (k + 1) / 4
    bar((HX, HY0 - HB + HB * math.cos(a0), HH - HB + HB * math.sin(a0)), (HX, HY0 - HB + HB * math.cos(a1), HH - HB + HB * math.sin(a1)), 3.5 / 12, 10)
    bar((HX, HY1 + HB - HB * math.cos(a0), HH - HB + HB * math.sin(a0)), (HX, HY1 + HB - HB * math.cos(a1), HH - HB + HB * math.sin(a1)), 3.5 / 12, 10)
bar((HX, HY0 - HB, HH), (HX, HY1 + HB, HH), 3.5 / 12, 10)
for yy_, zz_ in ((HY0, 3.5), (HY1, 3.5), ((HY0 + HY1) / 2, HH - .35)):
    for sx_ in (-1, 1): tie_ring(HX + sx_ * .3, yy_, zz_, 'x')
for yy_ in (WALL_O - .25, WALL_O - (RUN_D - ROCK_T / 2) / 4):   # E: the first two posts of run 1's west fence (x = -12), 5 ft, facing the pad
    tie_ring(-HL + 24 - .35, yy_, 5.0, 'x')
# ---- 4 Oct (Will): pose figures for the renders, material `figure` (hidden in the viewer unless a shot asks for them). A horse
# centred in the EAST bay of the wash pad (between the tie hoop and run 1's fence), head to the wall and tied to the hoop's ring,
# its near (west) hind leg lifted onto the farrier's thighs; the farrier beside that leg facing the tail, back bent flat; a rider
# at the horse's head. Plain blockout shapes: they give the painter the place, scale and pose, nothing more. ----
mat('figure')
HXc, HY0f = -18.0, WALL_O - 2.6                        # horse centre line, head end (the wall end)
BL_, BW_, BZ0, BZ1 = 5.6, 1.9, 3.2, 5.3                # barrel length, width, underside, top (ft)
by0, by1 = HY0f - 2.2, HY0f - 2.2 - BL_                # barrel front / rear (y falls away from the wall)
box(HXc - BW_ / 2, HXc + BW_ / 2, by1, by0, BZ0, BZ1)                                         # barrel
bar((HXc, by0 - .2, BZ1 - .3), (HXc, HY0f - .6, 6.6), 1.0, 8)                                # neck
box(HXc - .38, HXc + .38, HY0f - .9, HY0f + .7, 5.6, 6.6)                                    # head, nose to the wall
bar((HXc, by1, BZ1 - .2), (HXc, by1 - .6, 2.6), .35, 6)                                       # tail
for sx in (-1, 1):
    bar((HXc + sx * .6, by0 - .5, BZ0 + .2), (HXc + sx * .6, by0 - .45, 0), .38, 6)           # forelegs
bar((HXc + .6, by1 + .7, BZ0 + .2), (HXc + .6, by1 + .75, 0), .42, 6)                         # far hind leg, standing
bar((HXc - .6, by1 + .7, BZ0 + .3), (HXc - .75, by1 - .2, 2.2), .42, 6)                       # near hind: thigh to hock
bar((HXc - .75, by1 - .2, 2.2), (HXc - .85, by1 - 1.6, 2.15), .3, 6)                          # cannon resting back across the farrier's thighs, sole up
FX, FY = HXc - 1.6, by1 - 1.0                          # the farrier, beside the near hind leg, facing the tail (south)
for sy in (-.35, .35): bar((FX + sy * .4, FY + .2, 0), (FX + sy * .3, FY - .2, 2.4), .45, 6)     # legs, knees bent toward the tail
bar((FX, FY - .1, 2.5), (FX + .5, FY - 1.9, 3.3), 1.1, 8)                                     # torso bent forward, back flat
box(FX + .25, FX + .95, FY - 2.6, FY - 1.95, 3.0, 3.7)                                       # head, down over the hoof
for sx in (.15, .9): bar((FX + .5, FY - 1.6, 3.1), (FX + sx, FY - .9, 2.2), .28, 6)           # arms down to the hoof
box(FX - 1.4, FX - .5, FY + .6, FY + 1.3, 0, .9)                                             # tool box on the concrete
RX, RY = HXc - 2.1, HY0f - .4                          # a rider at the horse's head, holding the lead
for sy in (-.3, .3): bar((RX, RY + sy, 0), (RX, RY + sy * .7, 2.9), .45, 6)
bar((RX, RY, 2.9), (RX, RY, 5.0), 1.0, 8); box(RX - .38, RX + .38, RY - .38, RY + .38, 5.0, 5.8)
bar((RX + .3, RY - .2, 4.4), (HXc - .4, HY0f - .3, 5.6), .1, 4)                              # lead rope
mat('steel')

# ---- tan dirt floor over the whole stable inside the walls (Will, 28 Sep); the rooms get concrete on top of it ----
mat('dirt'); box(-HL + ROCK_T / 2, HL - ROCK_T / 2, -HD + ROCK_T / 2, HD - ROCK_T / 2, 0.0, 0.12)

# ---- concrete floors in the two closed rooms (Will, 28 Sep) ----
mat('concrete')
for r in rooms:
    if r['kind'] in SOLID: box(r['x0'] + .3, r['x1'] - .3, -HD + ROCK_T / 2, -HD + ROW_D - .3, 0.0, 0.28)

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
    f.write(f"# Centro Equino stable, 27 Sep: {L:.0f} x {D:.0f} ft steel trusses on 12 in tube posts, rock 5 ft all round with a floating pipe to 6 ft, open above, big sliding doors at both ends, pipe stall fronts and gates, clerestory monitor {2*MON_X:.0f} ft along the ridge, gable entries, 2 ft overhangs, 6 stalls north + 4 south with 12x40 runs, tack/feed (closed, straw bale/cob) + open wash bay at the west end by the barn road\n")
    f.write(f"# geo {LAT} {LON}\n# unit ft\n# name walker barn 72x40\n")
    for v in V: f.write('v %.3f %.3f %.3f\n' % v)
    last = None
    for fc, m in zip(F, MAT):
        if m != last: f.write(f'usemtl {m}\n'); last = m
        f.write('f ' + ' '.join(map(str, fc)) + '\n')
print(out, len(V), 'verts', len(F), 'faces', f'{L:.0f} x {D:.0f} ft')
