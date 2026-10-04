"""Roof structure for the covered stalls (4 Oct 2026, Will: a viewer switch like the stable's): rafters at every post line
from the eaves down to the valley, purlins along the length under the sheets, all tagged `truss` so the viewer's
"Estructura del techo" switch hides them. Appends to covered-stalls.obj (idempotent: strips an earlier truss block first)
and refreshes the 'covered stalls' stroke in the three drawings + the _bak_0928 copies without moving it.

    python stalls_frame.py
"""
import json, math, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); FT = .3048
OBJ = os.path.join(HERE, 'covered-stalls.obj')
FILES = ('centro-equino-2026-09-26.json', 'centro-equino-2026-09-26-stalls16.json', 'centro-equino-2026-09-26-stalls16-nopad.json')
# the stalls' own numbers (covered_stalls.py): 8 stalls 16 x 20, 12 ft corridor, 24 ft alfalfa bays, roof 12 ft over each front
PER_SIDE, STALL_W, STALL_D, CORR, OVER, ALF_L = 4, 16.0, 20.0, 12.0, 12.0, 24.0
VALLEY_NE, FALL, RISE = 10.7, .005, 1.5
L, D = PER_SIDE * STALL_W + ALF_L, 2 * STALL_D + CORR
HL, HD, HC = L / 2, D / 2, CORR / 2; RE = HC + OVER; RX = HL + 2; XS = -HL + PER_SIDE * STALL_W
def roof_z(x, y): return VALLEY_NE - FALL * (RX - x) + RISE * abs(y) / RE
BEAM, PURL, UNDER = .55, .45, .32                        # 8 in rafters, 6 in purlins, hung just under the sheets

MARK = '# --- roof structure (stalls_frame.py) ---'
src = open(OBJ, encoding='utf-8').read()
if MARK in src: src = src[:src.index(MARK)].rstrip('\n') + '\n'
nv = sum(1 for l in src.split('\n') if l.startswith('v '))
V, F = [], []
def bar(a, b, w):
    """a square bar of side w between 3D points a and b (ft): 8 vertices, 12 triangles"""
    a, b = np.array(a, float), np.array(b, float); d = b - a; d /= np.linalg.norm(d)
    up = np.array([0, 0, 1.0]) if abs(d[2]) < .9 else np.array([1.0, 0, 0])
    n1 = np.cross(d, up); n1 /= np.linalg.norm(n1); n2 = np.cross(d, n1)
    c = [(-n1 - n2), (n1 - n2), (n1 + n2), (-n1 + n2)]
    base = len(V) + nv + 1
    for p in (a, b):
        for q in c: V.append(p + q * w / 2)
    quads = [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
    for q in quads: F.append((base + q[0], base + q[1], base + q[2])); F.append((base + q[0], base + q[2], base + q[3]))
posts = [-HL + q * STALL_W for q in range(PER_SIDE + 1)] + [XS + ALF_L / 2, HL]
for x in posts:
    x = max(-HL + .3, min(HL - .3, x))
    for s in (-1, 1): bar((x, s * RE, roof_z(x, s * RE) - UNDER), (x, 0, roof_z(x, 0) - UNDER), BEAM)      # rafters, eave to valley
for s in (-1, 1):
    for y in (RE * .33, RE * .66, RE - .4):                                                                 # purlins along the slope
        yy = s * y; bar((-RX, yy, roof_z(-RX, yy) - UNDER), (RX, yy, roof_z(RX, yy) - UNDER), PURL)
    bar((-RX, s * RE, roof_z(-RX, s * RE) - UNDER - BEAM / 2), (RX, s * RE, roof_z(RX, s * RE) - UNDER - BEAM / 2), BEAM)   # eave beams
out = [MARK, 'usemtl truss'] + ['v %.3f %.3f %.3f' % tuple(v) for v in V] + ['f %d %d %d' % f for f in F]
open(OBJ, 'w', encoding='utf-8', newline='\n').write(src + '\n'.join(out) + '\n')
print(f'{len(F)} triangles of roof structure appended to covered-stalls.obj')

# refresh the stroke everywhere, keeping its place: re-centre the whole mesh exactly as the stroke was centred before
import sys; sys.path.insert(0, HERE)
from objtools import parse_obj, hull2
T, hdr = parse_obj(OBJ); P = T.reshape(-1, 3)
def refresh(path):
    d = json.load(open(path, encoding='utf-8')); ks = [i for i, s in enumerate(d['strokes']) if s.get('name') == 'covered stalls']
    if not ks: print(os.path.basename(path), ': no covered stalls here'); return
    k = ks[0]
    s = d['strokes'][k]; old = np.array(s['tris'] if not isinstance(s['tris'], str) else json.loads(s['tris']), float).reshape(-1, 3)
    # the old stroke was the obj centred on its own mean (x, y) and min z: the new mesh shares every old vertex, so the
    # old centring offset = old obj mean; recover it from the first stored triangle vs the first obj triangle
    off = P[0] * FT - old[0]
    Q = np.round(P * FT - off, 3)
    new = dict(s); new.update(tris=[float(v) for v in Q.flatten()], foot=hull2(Q[:, :2]), h=float(Q[:, 2].max()))
    d['strokes'][k] = new; json.dump(d, open(path, 'w', encoding='utf-8'))
    print(os.path.basename(path), ': covered stalls refreshed,', len(Q) // 3, 'triangles')
for fn in FILES:
    refresh(os.path.join(HERE, fn)); refresh(os.path.join(HERE, '_bak_0928', fn))
