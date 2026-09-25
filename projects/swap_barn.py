"""Swap the barn object in the topo drawing export for the new centro-equino-barn.obj, same spot and bearing.
Mirrors topo.html's parseObj + objFromMesh + geo placement, so the result is what an import would give.

    python swap_barn.py  ->  ~/Downloads/centro-equino-final-2026-09-24.json
"""
import json, math, numpy as np
DL = r'C:\Users\zolar\Downloads'
SRC, DST = DL + r'\centro-equino-final-2026-09-23b.json', DL + r'\centro-equino-final-2026-09-24.json'
FT = 0.3048

def parse_obj(path):
    v, out, hdr = [], [], {}
    for line in open(path, encoding='utf-8'):
        if line.startswith('# ') and len(line.split()) > 2: hdr[line.split()[1]] = line.strip()[len(line.split()[1]) + 3:]
        if line.startswith('v '): v.append([float(q) for q in line.split()[1:4]])
        elif line.startswith('f '):
            ix = [int(q.split('/')[0]) - 1 for q in line.split()[1:]]
            for k in range(1, len(ix) - 1): out += v[ix[0]] + v[ix[k]] + v[ix[k + 1]]
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

def from_mesh(t, f=FT):                   # objFromMesh: centred on the vertex mean, lowest point at zero, metres
    P = t.reshape(-1, 3); sx, sy, mz = P[:, 0].mean(), P[:, 1].mean(), P[:, 2].min()
    Q = np.round(np.c_[(P[:, 0] - sx) * f, (P[:, 1] - sy) * f, (P[:, 2] - mz) * f] * 1000) / 1000
    return Q, (sx * f, sy * f)

d = json.load(open(SRC, encoding='utf-8'))
W, H = d['grid']; cs = float(d['sliders']['siteW']) / (W - 1)
i_old = [i for i, s in enumerate(d['strokes']) if s.get('name') == 'walker barn 76x42'][0]; old = d['strokes'][i_old]

# the old file's origin (barn centre) in grid coordinates, from the old obj
t_old, _ = parse_obj('centro-equino-barn-76x42.obj'); Q_old, o_old = from_mesh(t_old)
assert np.allclose(Q_old.flatten()[:30], np.array(old['tris'][:30]), atol=2e-3), 'old obj does not reproduce the stored mesh'
r = math.radians(old['rot']); x, y = -o_old[0], -o_old[1]
g = (old['c'][0] + (x * math.cos(r) - y * math.sin(r)) / cs, old['c'][1] - (x * math.sin(r) + y * math.cos(r)) / cs)

# the new barn sits 10 ft south (barn frame) of the old centre: the 40 ft north runs then stay on the
# flat pad, using the pad space the old south runs had. No re-grading.
SHIFT = -10.0
GABLE = math.radians(90 - 65.84)
def grid_of(bx, by, g0):                  # barn frame (ft) -> grid, via the obj's own turn and the placement
    wx, wy = (bx * math.cos(GABLE) - by * math.sin(GABLE)) * FT, (bx * math.sin(GABLE) + by * math.cos(GABLE)) * FT
    return g0[0] + (wx * math.cos(r) - wy * math.sin(r)) / cs, g0[1] - (wx * math.sin(r) + wy * math.cos(r)) / cs
g = grid_of(0, SHIFT, g)

t_new, hdr = parse_obj('centro-equino-barn.obj'); Q, o = from_mesh(t_new)
x, y = -o[0], -o[1]
c = [g[0] - (x * math.cos(r) - y * math.sin(r)) / cs, g[1] + (x * math.sin(r) + y * math.cos(r)) / cs]
new = dict(old); new.update(name=hdr['name'], tris=[float(v) for v in Q.flatten()], foot=hull2(Q[:, :2]), h=float(Q[:, 2].max()),
                            c=c, pts=[[c[0], c[1], .5]])
d['strokes'][i_old] = new
json.dump(d, open(DST, 'w', encoding='utf-8'))
print('origin grid', [round(v, 2) for v in g], '| old c', [round(v, 2) for v in old['c']], '| new c', [round(v, 2) for v in c])
print('faces', len(new['tris']) // 9, 'height', round(new['h'] / FT, 1), 'ft ->', DST)

# does it sit on the pad? graded elevation under the building and under the runs
z = np.array(d['z']).reshape(H, W) / FT
def samp(px, py):
    i, j = int(px), int(py); fx, fy = px - i, py - j
    return z[j, i] * (1 - fx) * (1 - fy) + z[j, i + 1] * fx * (1 - fy) + z[j + 1, i] * (1 - fx) * fy + z[j + 1, i + 1] * fx * fy
for lab, (xa, xb, ya, yb) in {'building 72x40': (-36, 36, -20, 20), 'north runs 72x40': (-36, 36, 20, 60)}.items():
    zz = [samp(*grid_of(xa + (xb - xa) * i / 12, ya + (yb - ya) * j / 8, g)) for i in range(13) for j in range(9)]
    print(f'{lab:18s} graded z {min(zz):.1f} .. {max(zz):.1f} ft (pad 1087.6)')
