"""Put the current centro-equino-barn.obj into the drawings at the stable's fixed spot and bearing.

The spot is kept in stable_origin.json (the obj origin = the stable centre, in site grid coordinates). If that file is
missing, it is worked out once from a drawing whose stored stable matches a known obj (--from <obj>).

    python swap_stable.py                       # place the current obj
    python swap_stable.py --from old.obj        # first run: learn the spot from the stable currently in the drawings
"""
import json, math, os, sys, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); FT = .3048
sys.path.insert(0, HERE)
from geo import cs
FILES = ('centro-equino-2026-09-26.json', 'centro-equino-2026-09-26-stalls16.json', 'centro-equino-2026-09-26-stalls16-nopad.json')
ORIGIN = os.path.join(HERE, 'stable_origin.json')

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
def stable(d): return [i for i, s in enumerate(d['strokes']) if s.get('name') == 'walker barn 72x40'][0]

if not os.path.exists(ORIGIN) or '--from' in sys.argv:
    src = sys.argv[sys.argv.index('--from') + 1]
    Q0, o0 = from_mesh(parse_obj(os.path.join(HERE, src))[0])
    d = json.load(open(os.path.join(HERE, FILES[-1]), encoding='utf-8')); s = d['strokes'][stable(d)]
    tr = np.array(s['tris'] if not isinstance(s['tris'], str) else json.loads(s['tris']), float)
    assert np.allclose(Q0.flatten()[:30], tr[:30], atol=2e-3), f'{src} is not the stable stored in the drawing'
    r = math.radians(s['rot']); x, y = -o0[0], -o0[1]
    g = [s['c'][0] + (x * math.cos(r) - y * math.sin(r)) / cs, s['c'][1] - (x * math.sin(r) + y * math.cos(r)) / cs]
    json.dump(dict(grid=g, rot=s['rot'], note='the stable centre (obj origin) in site grid coords; swap_stable.py places every rebuilt stable here'), open(ORIGIN, 'w'), indent=1)
    print('stable origin learned:', [round(v, 3) for v in g])
O = json.load(open(ORIGIN)); g, rot = O['grid'], O['rot']
Q, o = from_mesh(parse_obj(os.path.join(HERE, 'centro-equino-barn.obj'))[0])
r = math.radians(rot); x, y = o
c = [g[0] + (x * math.cos(r) - y * math.sin(r)) / cs, g[1] - (x * math.sin(r) + y * math.cos(r)) / cs]
for fn in FILES:
    p = os.path.join(HERE, fn); d = json.load(open(p, encoding='utf-8')); k = stable(d)
    new = dict(d['strokes'][k]); new.update(tris=[float(v) for v in Q.flatten()], foot=hull2(Q[:, :2]), h=float(Q[:, 2].max()), c=c, pts=[[c[0], c[1], .5]], rot=rot)
    d['strokes'][k] = new; json.dump(d, open(p, 'w', encoding='utf-8'))
    print(fn, ': stable placed,', len(Q) // 3, 'triangles, height %.1f ft' % (new['h'] / FT))
