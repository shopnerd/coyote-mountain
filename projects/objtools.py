"""OBJ helpers shared by the swap scripts: parse like topo.html, hull, objFromMesh centring (feet -> metres)."""
import numpy as np
FT = .3048

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
