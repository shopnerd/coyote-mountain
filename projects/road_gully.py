"""Gully on the uphill side of the existing scrub-side road (4 Oct 2026, Will; talked over with the owner).

Two legs, both 15 ft off the road's centre line on the hill side (about 6 ft past the 16 ft road's edge):
  east leg  : from the road's east end down to the road-bend crossing (culvert 1), so the hill water that now lands
              on the road about 290 ft in is caught and handed to the main waterway -> natural sink below the track;
  west leg  : from just past the bend down to a NEW crossing at the site's south-west corner (grid x ~30); inside the
              fence the ground runs north along the west fence to the spreader (outlet 5).
Bottom = smoothed natural ground - 1 ft, forced to keep falling (monotone envelope), so the ditch never climbs over a
terrain bump and never rises above ground; 2 ft bottom, 2:1 sides. Carves the three `_bak_0928` chain inputs (so a
chain rerun keeps it) and adds records.ditches + a culvert stroke. Idempotent.

    python road_gully.py
"""
import json, math, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); FT = .3048
from geo import LL, GR, cs
FILES = ('centro-equino-2026-09-26.json', 'centro-equino-2026-09-26-stalls16.json', 'centro-equino-2026-09-26-stalls16-nopad.json')
OFF, DEPTH, BW, SIDE = 15.0 * FT / cs, .3, .6, 2.0        # offset (cells), depth m, bottom width m, side slope
CULV_X = 30.0                                              # the new west crossing, grid x (south-west corner of the site)
NAMES = ('road gully, east leg to the road-bend crossing', 'road gully, west leg to the south-west crossing')
CULV = 'culvert · road gully, west leg under existing scrub-side road'

def offset_line(P):
    """offset the road polyline to its larger-y (hill) side"""
    Q = []
    for k in range(len(P)):
        a = P[max(k - 1, 0)]; b = P[min(k + 1, len(P) - 1)]; d = b - a; d /= np.hypot(*d)
        n = np.array([-d[1], d[0]])
        if n[1] < 0: n = -n
        Q.append(P[k] + n * OFF)
    return np.array(Q)

def carve(d, z, pts, name):
    P = []
    for a_, b_ in zip(pts, pts[1:]):
        n = int(math.dist(a_, b_) / .25) + 1
        P += [(a_[0] + (b_[0] - a_[0]) * q / n, a_[1] + (b_[1] - a_[1]) * q / n) for q in range(n)]
    P.append(tuple(pts[-1])); P = np.array(P)
    def samp(p):
        i, j, fx, fy = int(p[0]), int(p[1]), p[0] % 1, p[1] % 1
        return z[j, i] * (1 - fx) * (1 - fy) + z[j, i + 1] * fx * (1 - fy) + z[j + 1, i] * (1 - fx) * fy + z[j + 1, i + 1] * fx * fy
    g = np.array([samp(q) for q in P]); Dq = np.r_[0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))] * cs
    win = max(1, round(3 / (.25 * cs))); gs = np.array([g[max(0, q - win):q + win + 1].mean() for q in range(len(P))])
    bot = np.minimum.accumulate(gs - DEPTH)                 # keeps falling from the high end
    for j in range(int(P[:, 1].min()) - 3, int(P[:, 1].max()) + 4):
        for i in range(int(P[:, 0].min()) - 3, int(P[:, 0].max()) + 4):
            dd = np.hypot(P[:, 0] - i, P[:, 1] - j); q = dd.argmin(); dm = dd[q] * cs
            if dm > 6: continue
            z[j, i] = min(z[j, i], bot[q] + max(0, dm - BW / 2) / SIDE)
    rec = dict(pts=[list(LL(*q)) for q in pts], depth=DEPTH, bw=BW, side=SIDE, berm='none', tb=.6, gap=.3, bottom='ground',
               dug=True, name=name, hb=0, sd=-1)
    d['records']['ditches'].append(rec)
    print(f'  {name}: {Dq[-1]/FT:.0f} ft, bottom {bot[0]/FT:.1f} -> {bot[-1]/FT:.1f} ft, deepest cut {(g-bot).max()/FT:.1f} ft, mean {(g-bot).mean()/FT:.1f} ft')

for fn in FILES:
    path = os.path.join(HERE, '_bak_0928', fn); d = json.load(open(path, encoding='utf-8'))
    W, H = d['grid']; z = np.array(d['z'], float).reshape(H, W)
    d['records']['ditches'] = [r for r in d['records']['ditches'] if r['name'] not in NAMES]
    d['strokes'] = [s for s in d['strokes'] if s.get('name') != CULV]
    road = [s for s in d['strokes'] if s.get('name') == 'existing scrub-side road'][0]
    P = np.array([q[:2] for q in road['pts']]); P = P[np.argsort(-P[:, 0])]            # east -> west
    Q = offset_line(P)
    culv1 = [s for s in d['strokes'] if (s.get('name') or '').startswith('culvert') and 'scrub-side' in s['name'] and 'main waterway' in s['name']][0]
    inlet = np.array(culv1['pts'][0][:2])                                               # south (uphill) end of crossing 1
    kb = int(np.argmin(np.hypot(*(Q - inlet).T)))
    east = list(map(tuple, Q[:kb])) + [tuple(inlet)]
    west0 = inlet + (Q[kb + 1] - inlet) / np.hypot(*(Q[kb + 1] - inlet)) * (12 * FT / cs)   # start 12 ft past the inlet
    kw = int(np.argmin(np.abs(Q[:, 0] - CULV_X)))
    # the new crossing: from the ditch line straight across the road to its north edge
    rp = P[kw]; nrm = (Q[kw] - rp) / np.hypot(*(Q[kw] - rp)); half = (8 * FT) / cs
    c_in = rp + nrm * (half + .2); c_out = rp - nrm * (half + .4)
    west = [tuple(west0)] + list(map(tuple, Q[kb + 2:kw])) + [tuple(c_in)]
    print(fn)
    carve(d, z, east, NAMES[0]); carve(d, z, west, NAMES[1])
    d['strokes'].append(dict(color='water', shape=True, name=CULV, w=3.2, a=1, dash=False,
                             pts=[[round(float(c_in[0]), 2), round(float(c_in[1]), 2), .5], [round(float(c_out[0]), 2), round(float(c_out[1]), 2), .5]]))
    d['z'] = [round(float(q), 3) for q in z.flatten()]
    json.dump(d, open(path, 'w', encoding='utf-8'))
    print(f'  crossing 2 at grid ({c_in[0]:.1f},{c_in[1]:.1f}) -> ({c_out[0]:.1f},{c_out[1]:.1f}), ground {z[int(round(c_out[1])), int(round(c_out[0]))]/FT:.1f} ft')
