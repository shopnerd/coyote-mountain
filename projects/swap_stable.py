"""Swap the stable in the drawings for the current centro-equino-barn.obj, same spot and bearing (27 Sep: clerestory +
woven sticks). The old mesh is recognised from centro-equino-barn-2026-09-24.obj, whose origin (the barn centre) fixes
where the new one goes. Mirrors topo.html's objFromMesh / objPlace.

    python swap_stable.py
"""
import json, math, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); FT = .3048
from geo import cs
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
    pts = sorted(map(tuple, pts)); cross = lambda o_, a, b: (a[0] - o_[0]) * (b[1] - o_[1]) - (a[1] - o_[1]) * (b[0] - o_[0])
    lo, up = [], []
    for q in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], q) <= 0: lo.pop()
        lo.append(q)
    for q in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], q) <= 0: up.pop()
        up.append(q)
    return [list(p) for p in lo[:-1] + up[:-1]]

def from_mesh(t):
    P = t.reshape(-1, 3); sx, sy, mz = P[:, 0].mean(), P[:, 1].mean(), P[:, 2].min()
    return np.round(np.c_[(P[:, 0] - sx) * FT, (P[:, 1] - sy) * FT, (P[:, 2] - mz) * FT] * 1000) / 1000, (sx * FT, sy * FT)

t_old, _ = parse_obj(os.path.join(HERE, 'centro-equino-barn-2026-09-24.obj')); Q_old, o_old = from_mesh(t_old)
t_new, hdr = parse_obj(os.path.join(HERE, 'centro-equino-barn.obj')); Q, o = from_mesh(t_new)
for fn in ('centro-equino-2026-09-26.json', 'centro-equino-2026-09-26-stalls16.json', 'centro-equino-2026-09-26-stalls16-nopad.json'):
    p = os.path.join(HERE, fn); d = json.load(open(p, encoding='utf-8'))
    k = [i for i, s in enumerate(d['strokes']) if s.get('name') == 'walker barn 72x40'][0]; old = d['strokes'][k]
    tr = np.array(old['tris'] if not isinstance(old['tris'], str) else json.loads(old['tris']), float)
    if not np.allclose(Q_old.flatten()[:30], tr[:30], atol=2e-3):
        print(fn, ': the stored stable is not the 24 Sep mesh, skipped'); continue
    r = math.radians(old['rot']); x, y = -o_old[0], -o_old[1]
    g = (old['c'][0] + (x * math.cos(r) - y * math.sin(r)) / cs, old['c'][1] - (x * math.sin(r) + y * math.cos(r)) / cs)   # the barn centre, grid
    x, y = o
    c = [g[0] + (x * math.cos(r) - y * math.sin(r)) / cs, g[1] - (x * math.sin(r) + y * math.cos(r)) / cs]
    new = dict(old); new.update(tris=[float(v) for v in Q.flatten()], foot=hull2(Q[:, :2]), h=float(Q[:, 2].max()), c=c, pts=[[c[0], c[1], .5]])
    d['strokes'][k] = new; json.dump(d, open(p, 'w', encoding='utf-8'))
    print(fn, ': stable swapped,', len(Q) // 3, 'triangles, height %.1f ft' % (new['h'] / FT))
