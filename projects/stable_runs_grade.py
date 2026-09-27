"""Grade the stable's south runs (27 Sep): the four south stalls get 12 x 40 ft runs on the uphill side. The ground
there climbs ~16 %, so the runs are graded to climb 5 % from the stable pad, and the difference is taken by a low rock
retaining wall along their uphill end and sides (vertical edge, no bank, so the barn diversion ditch 12 ft beyond is
untouched). Runs in the chain after swap_stable.py.

    python stable_runs_grade.py
"""
import json, math, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); FT = .3048
from geo import W, H, cs
O = json.load(open(os.path.join(HERE, 'stable_origin.json'))); g, r = O['grid'], math.radians(O['rot'])
ROT = math.radians(90 - 65.84)                              # the stable's own turn (centro-equino-barn.py)
X0, X1, Y0, Y1, FALL = -12.5, 36.5, -21.75, -61.75, .05       # barn frame ft: the four south runs (east end since 27 Sep; the old west-end grading stays as the open apron by the rooms), and their climb
def barn_xy(i, j):                                           # grid -> barn frame ft
    wx = ((i - g[0]) * math.cos(r) - (j - g[1]) * math.sin(r)) * cs; wy = (-(i - g[0]) * math.sin(r) - (j - g[1]) * math.cos(r)) * cs
    wx, wy = wx / FT, wy / FT
    return wx * math.cos(ROT) + wy * math.sin(ROT), -wx * math.sin(ROT) + wy * math.cos(ROT)
for fn in ('centro-equino-2026-09-26.json', 'centro-equino-2026-09-26-stalls16.json', 'centro-equino-2026-09-26-stalls16-nopad.json'):
    p = os.path.join(HERE, fn); d = json.load(open(p, encoding='utf-8')); z = np.array(d['z'], float).reshape(H, W)
    gi, gj = int(round(g[0])), int(round(g[1])); pad = float(z[gj, gi])                      # the stable pad level
    z0 = z.copy(); wall = 0.0
    for j in range(H):
        for i in range(W):
            x, y = barn_xy(i, j)
            if X0 <= x <= X1 and Y1 <= y <= Y0:
                zd = pad + FALL * (abs(y) - abs(Y0)) * FT; wall = max(wall, z[j, i] - zd); z[j, i] = zd
    d['z'] = [round(float(q), 3) for q in z.flatten()]; json.dump(d, open(p, 'w', encoding='utf-8'))
    dz = (z - z0) * cs * cs / .7646
    print(f'{fn}: pad {pad / FT:.1f} ft, south runs graded, cut {-dz[dz < 0].sum():.0f} yd3 fill {dz[dz > 0].sum():.0f} yd3, rock wall up to {wall / FT:.1f} ft')
