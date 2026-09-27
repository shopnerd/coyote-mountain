"""Walker's covered stalls at the yellow line (26 Sep): 16 stalls 16 x 20 ft, 8 a side, a 12 ft corridor
down the middle under one roof that overhangs 8 ft onto each row of stalls (the back 12 ft of every stall
is open sky, where the palms can stay). Minimal grading: the corridor follows the ground along its length
and is level across; stall floors fall at most 5 % from the corridor edge. A small ditch above the uphill row.

    python covered_stalls.py  ->  covered-stalls-16.obj, paddocks-no-shelters.obj (via paddocks.py),
                                  centro-equino-2026-09-26-stalls16.json
"""
import json, math, os, subprocess, sys, numpy as np
from geo import GR, LL, cs, W, H, la0, lo0
FT = .3048
HERE = os.path.dirname(os.path.abspath(__file__))
SRC, DST = os.path.join(HERE, 'centro-equino-2026-09-26.json'), os.path.join(HERE, 'centro-equino-2026-09-26-stalls16.json')

PER_SIDE, STALL_W, STALL_D, CORR, OVER = 4, 16.0, 20.0, 12.0, 12.0  # 27 Sep: 8 stalls 16 x 20 (4 a side); roof reaches 12 ft over each stall front
NB = PER_SIDE + 1                                       # one more bay at the NE (stable) end, under the same roof: the alfalfa bay
HAY_H = 7.5                                             # top of the alfalfa stack
PANEL, POST = 5.0, .5
# butterfly roof (Will, 26 Sep): both planes fall to a valley gutter over the corridor, the valley falls 1 % to the SW end,
# where a leader carries the water 8 ft past the roof and down into the ditch outlet
VALLEY_NE, FALL, RISE = 10.7, .005, 1.5                # valley 10.7 ft at the NE end, 0.5 % fall to the SW; eaves 1.5 ft higher = 1:12 over 18 ft (27 Sep: 1/2:12 was too flat)
FLAT = 6.0                                              # level strip at every stall front: waterers + feeders (Will, 26 Sep)
L, D = NB * STALL_W, 2 * STALL_D + CORR                # 80 x 52 ft
T0 = float(sys.argv[1]) if len(sys.argv) > 1 else 114.0 - L   # the NE (stable) end stays where the 16-stall block ended (t = 114); the block shrinks from the SW
S0 = 2.0                                                  # and 2 ft in from its NW (downhill) side

# the yellow line's frame: A = open SW end on the NW (downhill) side, t toward B (NE), s toward D (SE, uphill)
st = [(-116.7637927468709, 31.99970749966619), (-116.7635094983617, 31.99998532313917), (-116.7633790473066, 31.99988684382775), (-116.7636714287398, 31.99959200352455)]
k = 111320 * math.cos(math.radians(la0))
enu = lambda la, lo: np.array([(lo - lo0) * k, (la - la0) * 111320])   # metres east, north
A, B, C, Dp = (enu(la, lo) for lo, la in st)
u = (B - A) / np.linalg.norm(B - A); v = (Dp - A) / np.linalg.norm(Dp - A); v = v - u * (v @ u); v /= np.linalg.norm(v)
def ts2enu(t, s): return A + (u * t + v * s) * FT
def enu2ts(p): q = p - A; return (q @ u) / FT, (q @ v) / FT
def enu2ll(p): return la0 + p[1] / 111320, lo0 + p[0] / k
BEARING = math.degrees(math.atan2(u[0], u[1])) % 360    # long axis, from north
ctr = enu2ll(ts2enu(T0 + L / 2, S0 + D / 2))

# ---------- the building: feet, x along the corridor (toward NE), y across (+y = uphill SE side) ----------
V, F = [], []
def world(x, y, zz):                                    # building frame (ft) -> east, north (ft)
    p = u * x + v * y; return (p[0], p[1], zz)
def box(x0, x1, y0, y1, z0, z1):
    if min(x1 - x0, y1 - y0, z1 - z0) <= 0: return
    i = len(V) + 1
    for zz in (z0, z1):
        for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)): V.append(world(x, y, zz))
    for f in ((0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)): F.append(tuple(i + q for q in f))
def quad(a, b, c, dd):
    i = len(V) + 1
    for p in (a, b, c, dd): V.append(world(*p))
    F.append((i, i + 1, i + 2, i + 3))
HL, HD, HC = L / 2, D / 2, CORR / 2
RE = HC + OVER                                          # roof edge, 14 ft each side of the centre line
RX = HL + 2                                             # the roof runs 2 ft past each end
def roof_z(x, y): return VALLEY_NE - FALL * (RX - x) + RISE * abs(y) / RE
XS = -HL + PER_SIDE * STALL_W                           # where the stalls end and the NE bay begins
for sgn in (-1, 1):
    y_in, y_out = sgn * HC, sgn * HD
    box(-HL, XS, min(y_in, y_in + sgn * .25), max(y_in, y_in + sgn * .25), 0, PANEL)          # stall fronts on the corridor
    box(-HL, XS, min(y_out, y_out - sgn * .25), max(y_out, y_out - sgn * .25), 0, PANEL)      # back fences
    for q in range(PER_SIDE + 1):                                                              # dividers + end panels
        x = -HL + q * STALL_W; box(x - .12, x + .12, min(y_in, y_out), max(y_in, y_out), 0, PANEL)
    for q in range(NB + 1):                                                                    # roof posts: corridor edge + eave line
        x = max(-HL + POST / 2, min(HL - POST / 2, -HL + q * STALL_W))
        for yy in (y_in, sgn * RE):
            box(x - POST / 2, x + POST / 2, yy - POST / 2, yy + POST / 2, 0, roof_z(x, yy))
for q in range(1, PER_SIDE, 2):                                                                 # waterers: one per pair of stalls, in the divider at the corridor edge
    x = -HL + q * STALL_W
    for sgn in (-1, 1): box(x - .75, x + .75, min(sgn * (HC + .3), sgn * (HC + 1.8)), max(sgn * (HC + .3), sgn * (HC + 1.8)), 0, 3.0)
for zz in (0, .25):                                                                             # the butterfly roof: two planes down to the valley
    quad((-RX, -RE, roof_z(-RX, -RE) + zz), (RX, -RE, roof_z(RX, -RE) + zz), (RX, 0, roof_z(RX, 0) + zz), (-RX, 0, roof_z(-RX, 0) + zz))
    quad((-RX, 0, roof_z(-RX, 0) + zz), (RX, 0, roof_z(RX, 0) + zz), (RX, RE, roof_z(RX, RE) + zz), (-RX, RE, roof_z(-RX, RE) + zz))
# the alfalfa bay (27 Sep, Will: part of the same roof, not a separate structure): the NE end bay, the full roofed width,
# pipe panels on three sides, a 12 ft gate on the road end for the truck; the corridor stops at it, horses can't reach the hay
box(XS - .12, XS + .12, -RE, RE, 0, PANEL)
for sgn in (-1, 1):
    box(XS, HL, min(sgn * RE, sgn * (RE - .25)), max(sgn * RE, sgn * (RE - .25)), 0, PANEL)
    box(HL - .25, HL, min(sgn * 6, sgn * RE), max(sgn * 6, sgn * RE), 0, PANEL)
box(XS + 1, HL - 1, -RE + 2, RE - 2, .4, HAY_H)                                                # the stack, on pallets
vz = roof_z(-RX, 0)                                                                             # valley gutter
box(-RX, RX, -.6, .6, vz - .6, vz)
# round trough past the SW end (Will, 26 Sep): the valley carries on as an open chute and pours into it, no downspout.
# GAP of clear ground between the building end and the trough, and all round it; overflow piped to the ditch outlet.
TROUGH_D, TROUGH_H, GAP = 8.0, 2.0, 10.0                 # GAP: clear ground round the trough's open sides
END_GAP, CHUTE = 7.0, 7.0                                # 7 ft walk-through at the building end; chute cantilevers 7 ft past the roof, no post (Will)
TX = -HL - END_GAP - TROUGH_D / 2                        # trough centre on the corridor's centre line
def ring(cx, r0, r1, z0, z1, n=24):                      # an open round tank: outer + inner wall, rim, bottom
    P = lambda r, a, zz: (cx + r * math.cos(a), r * math.sin(a), zz)
    for q in range(n):
        a, b = 2 * math.pi * q / n, 2 * math.pi * (q + 1) / n
        quad(P(r1, a, z0), P(r1, b, z0), P(r1, b, z1), P(r1, a, z1))
        quad(P(r0, b, z0), P(r0, a, z0), P(r0, a, z1), P(r0, b, z1))
        quad(P(r0, a, z1), P(r1, a, z1), P(r1, b, z1), P(r0, b, z1))
    i = len(V) + 1
    for q in range(n): V.append(world(*P(r0, 2 * math.pi * q / n, TROUGH_H * .75)))    # the water
    F.append(tuple(range(i, i + n)))
ring(TX, TROUGH_D / 2 - .25, TROUGH_D / 2, 0, TROUGH_H)
CH_END = -RX - CHUTE                                     # open chute, cantilevered, pours in 2 ft inside the near rim
assert TX + TROUGH_D / 2 - 1.5 > CH_END > TX, 'the chute must end over the trough'
cz = lambda x: vz - .02 * (-RX - x)                      # falls 2 % from the valley
box(CH_END, -RX, -.6, .6, cz(CH_END) - .5, vz - .1)
OBJ = os.path.join(HERE, 'covered-stalls.obj')
with open(OBJ, 'w', newline='\n') as f:
    f.write(f'# covered stalls: {2*PER_SIDE} stalls + alfalfa bay, {STALL_W:g} x {STALL_D:g} ft, {PER_SIDE} a side, {CORR:g} ft corridor, roof {2*RE:g} ft wide ({OVER:g} ft over each stall front), butterfly: valley over the corridor {VALLEY_NE:g} ft at the NE end falling {FALL*100:g} % to {vz:.1f} ft at the SW end, outer eaves {RISE:g} ft higher; the valley pours down an open chute into a round trough {TROUGH_D:g} ft across, {TROUGH_H:g} ft tall, {END_GAP:g} ft from the SW end, {GAP:g} ft clear on its open sides, chute cantilevered {CHUTE:g} ft, no post; {PER_SIDE} waterers (one per pair) on a {FLAT:g} ft level strip at the stall fronts; alfalfa bay {STALL_W:g} x {2*RE:g} ft under the roof at the NE end\n')
    f.write('# geo %.7f %.7f\n# unit ft\n# name covered stalls\n' % ctr)
    for p in V: f.write('v %.3f %.3f %.3f\n' % p)
    for fc in F: f.write('f ' + ' '.join(map(str, fc)) + '\n')

# ---------- helpers mirroring topo.html (parseObj, objFromMesh, objPlace) ----------
def parse_obj(path):
    vv, out, hdr = [], [], {}
    for line in open(path, encoding='utf-8'):
        if line.startswith('# ') and len(line.split()) > 2: hdr[line.split()[1]] = line.strip()[len(line.split()[1]) + 3:]
        if line.startswith('v '): vv.append([float(q) for q in line.split()[1:4]])
        elif line.startswith('f '):
            ix = [int(q.split('/')[0]) - 1 for q in line.split()[1:]]
            for kk in range(1, len(ix) - 1): out += vv[ix[0]] + vv[ix[kk]] + vv[ix[kk + 1]]
    return np.array(out, float), hdr
def hull2(pts):
    pts = sorted(map(tuple, pts)); cross = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for q in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], q) <= 0: lo.pop()
        lo.append(q)
    for q in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], q) <= 0: up.pop()
        up.append(q)
    return [list(p) for p in lo[:-1] + up[:-1]]
def obj_stroke(path, site_rot):
    t, hdr = parse_obj(path); P = t.reshape(-1, 3); sx, sy, mz = P[:, 0].mean(), P[:, 1].mean(), P[:, 2].min()
    Q = np.round(np.c_[(P[:, 0] - sx) * FT, (P[:, 1] - sy) * FT, (P[:, 2] - mz) * FT] * 1000) / 1000
    la, lo = map(float, hdr['geo'].split()); g = GR(la, lo); r = math.radians(site_rot); x, y = sx * FT, sy * FT
    c = [g[0] + (x * math.cos(r) - y * math.sin(r)) / cs, g[1] - (x * math.sin(r) + y * math.cos(r)) / cs]
    return dict(color='ink', shape=False, kind='obj', c=c, name=hdr['name'], unit='ft', rot=site_rot, sc=1, lift=0,
                tris=[float(q) for q in Q.flatten()], foot=hull2(Q[:, :2]), h=float(Q[:, 2].max()), w=1, a=1, dash=False, pts=[[c[0], c[1], .5]])

# ---------- grading ----------
d = json.load(open(SRC, encoding='utf-8'))
site_rot = float(d['sliders']['rot'])
z = np.array(d['z'], float).reshape(H, W)
z_before = z.copy()
def zs(t, s):                                           # graded ground (m) at a point of the frame
    gi, gj = GR(*enu2ll(ts2enu(t, s))); i, j = int(gi), int(gj); fx, fy = gi - i, gj - j
    return z[j, i] * (1 - fx) * (1 - fy) + z[j, i + 1] * fx * (1 - fy) + z[j + 1, i] * (1 - fx) * fy + z[j + 1, i + 1] * fx * fy
sc_mid = S0 + D / 2
tt = np.linspace(T0, T0 + L, 17)
zc_line = np.polyfit(tt, [np.mean([zs(t, s) for s in np.linspace(sc_mid - HC, sc_mid + HC, 5)]) for t in tt], 1)
def design(t, s):                                       # metres, inside the block
    zc = np.polyval(zc_line, t); e = abs(s - sc_mid) - HC - FLAT
    if e <= 0: return zc
    nat = zs(t, s) - zc; ec = max(0, OVER - FLAT)        # 5 % under the roof, up to 8 % on the open backs
    lim = (.05 * min(e, ec) + .08 * max(0, e - ec)) * FT
    return zc + max(-lim, min(lim, nat))
SIDE = 3.0                                              # 3:1 side slopes out to the ground
new = z.copy()
for j in range(H):
    for i in range(W):
        la, lo = LL(i, j); t, s = enu2ts(enu(la, lo))
        tc, sc_ = min(max(t, T0), T0 + L), min(max(s, S0), S0 + D)
        dist = math.hypot(t - tc, s - sc_) * FT
        if dist > 4: continue
        de = design(tc, sc_); g = z[j, i]
        new[j, i] = de if dist == 0 else min(max(g, de - dist / SIDE), de + dist / SIDE)
z = new
# a level apron round the trough (6 ft of footing past its rim), 3:1 to the ground
TT, TS_ = T0 + (TX + HL), sc_mid                         # trough centre in the line's frame
za = zs(TT, TS_); AR = TROUGH_D / 2 + 6
for j in range(H):
    for i in range(W):
        la, lo = LL(i, j); t, s = enu2ts(enu(la, lo)); e = max(0, math.hypot(t - TT, s - TS_) - AR) * FT
        if e > 4: continue
        z[j, i] = za if e == 0 else min(max(z[j, i], za - e / SIDE), za + e / SIDE)

# the ditch: 6 ft above the uphill row from 10 ft past the NE end, falling 1 % to the SW, then turning down the slope
# round the SW end to let the water go on the open ground (not toward the main road). Mirrors dbShape.
def carve(pts_ts, bottom, name):
    rec = dict(pts=[list(enu2ll(ts2enu(t, s))) for t, s in pts_ts], depth=.3, bw=.6, side=3, berm='none', tb=.6, gap=.3,
               bottom=bottom, dug=True, name=name, hb=0, sd=-1)
    gd = [GR(*q) for q in rec['pts']]; P = []
    for a_, b_ in zip(gd, gd[1:]):
        n = int(math.dist(a_, b_) / .25) + 1
        P += [(a_[0] + (b_[0] - a_[0]) * q / n, a_[1] + (b_[1] - a_[1]) * q / n) for q in range(n)]
    P.append(gd[-1]); P = np.array(P)
    def samp(p):
        i, j, fx, fy = int(p[0]), int(p[1]), p[0] % 1, p[1] % 1
        return z[j, i] * (1 - fx) * (1 - fy) + z[j, i + 1] * fx * (1 - fy) + z[j + 1, i] * (1 - fx) * fy + z[j + 1, i + 1] * fx * fy
    g = np.array([samp(q) for q in P]); Dq = np.r_[0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))] * cs
    if bottom == 'ground':
        win = max(1, round(3 / (.25 * cs))); bot = np.array([g[max(0, q - win):q + win + 1].mean() for q in range(len(P))]) - rec['depth']
    else: bot = g[0] - float(bottom) / 100 * Dq - rec['depth']          # falls from the first point
    for j in range(int(P[:, 1].min()) - 2, int(P[:, 1].max()) + 3):
        for i in range(int(P[:, 0].min()) - 2, int(P[:, 0].max()) + 3):
            dd = np.hypot(P[:, 0] - i, P[:, 1] - j); q = dd.argmin(); dm = dd[q] * cs
            z[j, i] = min(z[j, i], bot[q] + max(0, dm - rec['bw'] / 2) / rec['side'])
    d['records'].setdefault('ditches', []).append(rec)
    print(f'{name}: bottom {bot[0]/FT:.1f} -> {bot[-1]/FT:.1f} ft, {Dq[-1]/FT:.0f} ft long, deepest {(g - bot).max()/FT:.1f} ft')
    return bot
up = S0 + D + 6
TO = TT - TROUGH_D / 2 - GAP                             # the outlet runs GAP past the trough's far rim
carve([(t, up) for t in np.linspace(T0 + L + 10, TO, 10)], '1', 'covered stalls, ditch above the uphill row')
# ...and down the slope into the ditch above the barn road, so the roof, the trough overflow and the hill water join the water plan
J = np.array([GR(*p) for p in [r_ for r_ in d['records']['ditches'] if r_['name'] == 'ditch above the barn road'][0]['pts']])
aim = np.array(GR(*enu2ll(ts2enu(TO, S0 - 12)))); jn = J[np.hypot(*(J - aim).T).argmin()]
join = enu2ts(enu(*LL(*jn)))
bot = carve([(TO, up), (TO, S0 + D / 2), (TO, S0), join], 'ground', 'covered stalls, ditch outlet round the SW end')
# the trough's overflow: a buried pipe from the far rim, on its own fall, to the outlet ditch
ov = [(TT - TROUGH_D / 2, TS_), (TO, TS_)]
d['strokes'] = [s_ for s_ in d['strokes'] if s_.get('name') != 'stalls trough overflow pipe']
d['strokes'].append(dict(color='blue', shape=True, w=1.4, a=1, dash=True, name='stalls trough overflow pipe',
                         pts=[[round(g_[0], 2), round(g_[1], 2), .5] for g_ in (GR(*enu2ll(ts2enu(*q))) for q in ov)]))
d['z'] = [round(float(q), 3) for q in z.flatten()]

# ---------- objects: new stalls in, shelters out of the paddocks ----------
d['strokes'] = [s_ for s_ in d['strokes'] if not (s_.get('name') or '').startswith('covered stalls')]
d['strokes'].append(obj_stroke(OBJ, site_rot))
subprocess.run([sys.executable, os.path.join(HERE, 'paddocks.py'), '--no-shelters'], check=True, cwd=HERE)
ip = [q for q, s_ in enumerate(d['strokes']) if s_.get('name') == 'four paddocks'][0]; old = d['strokes'][ip]
pn = obj_stroke(os.path.join(HERE, 'paddocks-no-shelters.obj'), old['rot'])
pn.update(c=old['c'], pts=old['pts'], lift=old.get('lift', 0), name='four paddocks')   # same spot as before: only the shelters go
d['strokes'][ip] = pn
d['saved'] = '2026-09-26T23:00:00.000Z'
json.dump(d, open(DST, 'w', encoding='utf-8'))

# ---------- report ----------
dz = (z - z_before) * (cs ** 2); cut, fill = -dz[dz < 0].sum() / .7646, dz[dz > 0].sum() / .7646
print(f'bearing {BEARING:.1f} deg, centre {ctr[0]:.6f}, {ctr[1]:.6f}; building {L:g} x {D:g} ft, roof {2*RE:g} x {L+4:g} ft')
print(f'corridor {np.polyval(zc_line, T0)/FT:.1f} ft (SW) -> {np.polyval(zc_line, T0+L)/FT:.1f} ft (NE)')
print(f'this change: cut {cut:.0f} yd3, fill {fill:.0f} yd3 (incl. ditch), biggest change {abs(z-z_before).max()/FT:.1f} ft')
roads = {s_['name']: s_ for s_ in d['strokes'] if s_.get('kind') == 'path'}
def clear(name):
    s_ = roads[name]; R = [enu(*LL(p[0], p[1])) for p in s_['pts']]
    edge = [ts2enu(t, s) for t in np.linspace(T0 - 2, T0 + L + 2, 66) for s in (S0, S0 + D)] + [ts2enu(t, s) for t in (T0 - 2, T0 + L + 2) for s in np.linspace(S0, S0 + D, 27)]
    return min(min(np.linalg.norm(e - r) for r in R) for e in edge) / FT - s_.get('pw', 3.66) / 2 / FT
for n in ('main road, north-east gate to south gate', 'round pen ring road', 'existing scrub-side road', 'barn to cross-fence road'):
    print(f'clear of {n}: {clear(n):.0f} ft')
print('->', DST)
