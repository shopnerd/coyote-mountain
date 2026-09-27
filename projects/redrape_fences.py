"""Set the draped fences back on the ground (27 Sep): the site fence and the cross fence were draped over the ground
before the regrading, so where the ground changed they sit up to 2 m under it. Each vertex keeps its height above the
fence's own local foot (the lowest vertex within ~2 m, i.e. the nearest post base) and is re-seated on today's ground.

    python redrape_fences.py        (edits the three working drawings in place)
"""
import json, math, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
from geo import W, H, cs
NAMES = ('site fence', 'cross fence')
for fn in ('centro-equino-2026-09-26.json', 'centro-equino-2026-09-26-stalls16.json', 'centro-equino-2026-09-26-stalls16-nopad.json'):
    p = os.path.join(HERE, fn); d = json.load(open(p, encoding='utf-8')); z = np.array(d['z'], float).reshape(H, W)
    def samp(i, j):
        i = np.clip(i, 0, W - 1.001); j = np.clip(j, 0, H - 1.001); i0, j0 = i.astype(int), j.astype(int); fx, fy = i - i0, j - j0
        return z[j0, i0] * (1 - fx) * (1 - fy) + z[j0, i0 + 1] * fx * (1 - fy) + z[j0 + 1, i0] * (1 - fx) * fy + z[j0 + 1, i0 + 1] * fx * fy
    for s in d['strokes']:
        if s.get('name') not in NAMES: continue
        T = np.array(s['tris'] if not isinstance(s['tris'], str) else json.loads(s['tris']), float).reshape(-1, 3)
        r = math.radians(s['rot']); c0, c1 = s['c']; z0 = float(samp(np.array(c0), np.array(c1))) + s.get('lift', 0)
        # local foot: lowest vertex in a 2 m neighbourhood (binned 1 m, 5 x 5 window)
        bx, by = np.floor(T[:, 0]).astype(int), np.floor(T[:, 1]).astype(int); key = {}
        for k in range(len(T)): kk = (bx[k], by[k]); key[kk] = min(key.get(kk, 1e9), T[k, 2])
        foot = np.array([min(key.get((bx[k] + a, by[k] + b), 1e9) for a in range(-2, 3) for b in range(-2, 3)) for k in range(len(T))])
        hloc = T[:, 2] - foot
        gi = c0 + (T[:, 0] * math.cos(r) - T[:, 1] * math.sin(r)) / cs; gj = c1 - (T[:, 0] * math.sin(r) + T[:, 1] * math.cos(r)) / cs
        world = samp(gi, gj) - .05 + hloc                        # 5 cm into the ground, as a post sits
        tz = world - z0; m = tz.min(); s['lift'] = float(s.get('lift', 0) + m); tz -= m
        T[:, 2] = np.round(tz * 1000) / 1000; s['tris'] = [float(v) for v in T.reshape(-1)]; s['h'] = float(tz.max())
        after = world - samp(gi, gj)
        print(f'{fn}: {s["name"]} re-seated, height above ground now {after.min():.2f} .. {after.max():.2f} m')
    json.dump(d, open(p, 'w', encoding='utf-8'))
