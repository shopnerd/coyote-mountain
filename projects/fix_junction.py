"""After remove_road.py: clear a removed road's ramp where it met another road, then re-run that road there (applyPath).
    python fix_junction.py "removed road" "kept road"   (removed road's line read from the -stalls16.json before removal)"""
import json, math, os, sys, numpy as np
from geo import cs, W, H
HERE = os.path.dirname(os.path.abspath(__file__)); FILE = os.path.join(HERE, 'centro-equino-2026-09-26-stalls16-nopad.json')
gone_name, keep_name = sys.argv[1], sys.argv[2]
old = json.load(open(os.path.join(HERE, 'centro-equino-2026-09-26-stalls16.json'), encoding='utf-8'))
d = json.load(open(FILE, encoding='utf-8'))
z = np.array(d['z'], float).reshape(H, W); base = np.array(d['base'], float).reshape(H, W); z0 = z.copy()
I, J = np.meshgrid(np.arange(W), np.arange(H))
def resample(pts, step):
    out = []
    for a, b in zip(pts, pts[1:]):
        n = max(1, int(math.dist(a, b) / step)); out += [(a[0] + (b[0] - a[0]) * q / n, a[1] + (b[1] - a[1]) * q / n) for q in range(n)]
    return np.array(out + [tuple(pts[-1])])
dist_to = lambda P: np.min(np.hypot(I[..., None] - P[:, 0], J[..., None] - P[:, 1]), axis=2)
G = resample([p[:2] for p in [s for s in old['strokes'] if s.get('name') == gone_name][0]['pts']], .5)
K = [s for s in d['strokes'] if s.get('name') == keep_name][0]; KP = resample([p[:2] for p in K['pts']], .5)
dK, dG = dist_to(KP), dist_to(G)
junction = (dG <= K['pw'] / 2 / cs + 3) & (dK <= K['pw'] / 2 / cs + 4)          # where the two met
z[junction] = base[junction]
# re-run the kept road (applyPath), written only in the junction
raw = np.array([z[min(int(round(q[1])), H - 1), min(int(round(q[0])), W - 1)] for q in KP]); win = max(2, min(60, round(12 / (cs * .5))))
prof = np.array([raw[max(0, i - win):i + win + 1].mean() for i in range(len(KP))]); R = K['pw'] / 2 / cs; sl = 1 / float(d['sliders'].get('side', 3))
for j, i in zip(*np.where(junction)):
    dd = np.hypot(KP[:, 0] - i, KP[:, 1] - j); k = dd.argmin(); zt = prof[k] + (K.get('ph') or 0); zc = z[j, i]
    if dd[k] <= R: z[j, i] = zt
    else:
        e = (dd[k] - R) * cs; nz = zt - e * sl if zc < zt else zt + e * sl
        if not ((zc < zt and nz <= zc) or (zc >= zt and nz >= zc)): z[j, i] = nz
d['z'] = [round(float(q), 3) for q in z.flatten()]; json.dump(d, open(FILE, 'w', encoding='utf-8'))
tot = lambda a: (-a[a < 0].sum() * cs * cs / .7646, a[a > 0].sum() * cs * cs / .7646)
print('junction cells', junction.sum(), '| max leftover there %.1f ft' % (np.abs(z - base)[junction].max() / .3048), '| site cut %.0f fill %.0f yd3' % tot(z - base))
