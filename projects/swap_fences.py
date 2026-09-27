"""Put the rebuilt arena and round-pen fences (pipe-fence.py, gates at the drawing's gate marks, 27 Sep) into the
drawings at the same spot as the ones they replace. The spot is learned once from the old obj that matches the stored
mesh and kept in fence_origins.json. Runs in the chain after swap_stable.py.

    python swap_fences.py
"""
import json, math, os, sys, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from geo import cs
from objtools import parse_obj, hull2, from_mesh
FILES = ('centro-equino-2026-09-26.json', 'centro-equino-2026-09-26-stalls16.json', 'centro-equino-2026-09-26-stalls16-nopad.json')
JOBS = [('arena fence', 'arena-fence-2026-09-23.obj', 'arena-fence.obj'), ('round pen fence', 'roundpen-fence-2026-09-23.obj', 'roundpen-fence.obj')]
ORIG = os.path.join(HERE, 'fence_origins.json'); origins = json.load(open(ORIG)) if os.path.exists(ORIG) else {}
for name, old_obj, new_obj in JOBS:
    if name not in origins:
        Q0, o0 = from_mesh(parse_obj(os.path.join(HERE, old_obj))[0])
        d = json.load(open(os.path.join(HERE, FILES[-1]), encoding='utf-8')); s = [s for s in d['strokes'] if s.get('name') == name][0]
        tr = np.array(s['tris'] if not isinstance(s['tris'], str) else json.loads(s['tris']), float)
        assert np.allclose(Q0.flatten()[:30], tr[:30], atol=2e-3), f'{old_obj} is not the {name} in the drawing'
        r = math.radians(s['rot']); x, y = -o0[0], -o0[1]
        origins[name] = dict(grid=[s['c'][0] + (x * math.cos(r) - y * math.sin(r)) / cs, s['c'][1] - (x * math.sin(r) + y * math.cos(r)) / cs], rot=s['rot'])
json.dump(origins, open(ORIG, 'w'), indent=1)
for fn in FILES:
    p = os.path.join(HERE, fn); d = json.load(open(p, encoding='utf-8'))
    for name, old_obj, new_obj in JOBS:
        Q, o = from_mesh(parse_obj(os.path.join(HERE, new_obj))[0]); g, rot = origins[name]['grid'], origins[name]['rot']; r = math.radians(rot)
        c = [g[0] + (o[0] * math.cos(r) - o[1] * math.sin(r)) / cs, g[1] - (o[0] * math.sin(r) + o[1] * math.cos(r)) / cs]
        k = [i for i, s in enumerate(d['strokes']) if s.get('name') == name][0]
        new = dict(d['strokes'][k]); new.update(tris=[float(v) for v in Q.flatten()], foot=hull2(Q[:, :2]), h=float(Q[:, 2].max()), c=c, pts=[[c[0], c[1], .5]], rot=rot)
        d['strokes'][k] = new
    json.dump(d, open(p, 'w', encoding='utf-8')); print(fn, ': arena and round pen fences placed')
