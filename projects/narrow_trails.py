"""Narrow riding trails (11 Oct 2026, Will): the ring road around the arena, the ring road around the round pen, and the trail
between them that goes west to the track all become 5 ft, like the walking path from the parking to the stable.
The 'barn to cross-fence road' is split where it crosses the main road: the east part stays the 14 ft entry drive to the
stable trough (4 Oct, site_extras.py); the west part becomes its own 5 ft path, 'trail to the track'.
Idempotent; run after site_extras.py / bleachers.py / existing_trees.py in the build chain.

    python narrow_trails.py [drawing.json ...]     (default: the Centro Equino drawings and their roots-study copies)
"""
import copy, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); FT = .3048; W5 = 5 * FT
FILES = sys.argv[1:] or ['centro-equino-2026-09-26.json', 'centro-equino-2026-09-26-stalls16.json', 'centro-equino-2026-09-26-stalls16-nopad.json',
                         'centro-equino-2026-10-10-cafe-option2-trees.json', 'centro-equino-roots.json', 'centro-equino-islas.json', 'centro-equino-encinos.json']
TRAIL = 'trail to the track'

def path(d, name): return next((s for s in d['strokes'] if s.get('kind') == 'path' and s.get('name') == name), None)

for fn in FILES:
    p = os.path.join(HERE, fn); d = json.load(open(p, encoding='utf-8')); out = []
    for nm in ('arena ring road', 'round pen ring road'):
        s = path(d, nm)
        if s and abs(s['pw'] - W5) > 1e-6: out.append(f"{nm} {s['pw'] / FT:.0f} -> 5 ft"); s['pw'] = W5
    rd, mr = path(d, 'barn to cross-fence road'), path(d, 'main road, north-east gate to south gate')
    if rd and mr and not path(d, TRAIL):
        R = np.array([q[:2] for q in rd['pts']]); M = np.array([q[:2] for q in mr['pts']])
        k = int(np.argmin([np.hypot(*(M - r).T).min() for r in R]))          # where the barn road crosses the main road
        west = copy.deepcopy(rd); west.update(name=TRAIL, pts=copy.deepcopy(rd['pts'][k:]), pw=W5); west['c'] = west['pts'][0][:2]
        rd['pts'] = rd['pts'][:k + 1]
        d['strokes'].insert(d['strokes'].index(rd) + 1, west)
        out.append(f"barn road split at point {k} of {len(R)} ({R[k][0]:.1f}, {R[k][1]:.1f}): entry drive stays {rd['pw'] / FT:.0f} ft, {TRAIL} 5 ft")
    elif path(d, TRAIL) and abs(path(d, TRAIL)['pw'] - W5) > 1e-6: path(d, TRAIL)['pw'] = W5; out.append(f'{TRAIL} -> 5 ft')
    if out: json.dump(d, open(p, 'w', encoding='utf-8'))
    print(fn, ':', '; '.join(out) or 'already narrow')
