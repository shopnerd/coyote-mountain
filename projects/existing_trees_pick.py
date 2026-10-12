# existing trees from the aerial + the 11 Oct site photos -> coyote-studio/projects/existing_trees.json (grid i, j; crown radius m; height m)
import json, math, sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
from skimage.feature import peak_local_max
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
D, PROJ, OUT = sys.argv[1], sys.argv[2], sys.argv[3]; S = 4; CS = 400 / 149
A = np.asarray(Image.open(D + '/aerial-grid.png')).astype(float); R, G, B = A[..., 0], A[..., 1], A[..., 2]
exg = 2 * G - R - B; v = A.mean(2)
veg = ndi.binary_opening((exg > 14) | ((v < 95) & (G >= R - 4)), iterations=1)
sm = ndi.gaussian_filter(veg.astype(float) * (200 - v), 1.6)
dt = ndi.distance_transform_edt(veg)
pk = peak_local_max(sm, min_distance=4, threshold_abs=28)
# the model's procedural east pine grove: where its trunks stand, so we do not double it
p = json.load(open(PROJ, encoding='utf-8')); pf = [s for s in p['strokes'] if s.get('name') == 'pine forest'][0]
T = np.array(pf['tris']).reshape(-1, 3); r = math.radians(pf['rot']); c0, c1 = pf['c']
low = T[::3]; gi = c0 + (low[:, 0] * math.cos(r) - low[:, 1] * math.sin(r)) / CS; gj = c1 - (low[:, 0] * math.sin(r) + low[:, 1] * math.cos(r)) / CS
PF = np.stack([gi, gj], 1)[::2]
def zone(i, j):   # what grows where, read from the photos (heading -> which crown) and the aerial
    if j < 17 or j > 73: return None
    if j < 22.5 and not (107 <= i <= 122): return None                       # vineyard north of the road (except the roadside pines, 8855)
    if i > 123 and j < 57: return None                                       # the east vineyard
    if 70 <= i <= 99 and 57 <= j <= 69: return 'nursery'                     # potted palm nursery under the covered stalls (8808-8820)
    if 99 <= i <= 102 and 35 <= j <= 51: return 'youngpalm'                  # the line of young palms (8847)
    if 65 <= i <= 79 and 23 <= j <= 30: return 'palmgrove'                   # north palm clump (8782-8784)
    if 107 <= i <= 122 and 17 <= j <= 33: return 'pine'                      # roadside and NE pines (8853-8855)
    if 94 <= i <= 107 and 23 <= j <= 33: return 'shrubpine'                  # big round shrubs + a pine (8779-8781)
    if 108.5 <= i <= 113 and 36.5 <= j <= 40.5: return 'pepper'              # the pepper tree (8851, 8852)
    if 108 <= i <= 124 and 41 <= j <= 54: return 'thicket'                   # shrub thicket (8845-8850)
    if 108 <= i <= 135 and 62 <= j <= 68: return 'shrub'                     # small growth along the south fence (8836-8839)
    if 28 <= i <= 67 and 28 <= j <= 73: return 'westblock'                   # west block: pines (dark) among fan palm rows (8782-8806)
    return 'other'
trees = []
for y, x in pk:
    i, j = x / S, y / S; z = zone(i, j)
    if z is None or z == 'nursery' and v[y, x] > 70: continue
    if len(PF) and np.hypot(PF[:, 0] - i, PF[:, 1] - j).min() * CS < 2.5: continue   # inside the model's own east pine grove already
    if j > 69 and i > 66 and not (77 <= i <= 79.5): continue                 # south of the road: the hillside scrub, left out
    if j > 71 and not (61 <= i <= 65): continue
    rad = min(4.5, max(.8, dt[y, x] / S * CS)); dark = v[max(0, y - 2):y + 3, max(0, x - 2):x + 3].mean() < 78
    if z == 'other' and not dark and rad < 1.6: continue                  # specks in the open field
    if z == 'westblock' or z == 'other': kind = 'pine' if dark and rad > 1.6 else ('palm' if rad < 2.6 else 'shrub')
    elif z == 'shrubpine': kind = 'pine' if dark and rad > 2.6 else 'bigshrub'
    elif z == 'palmgrove': kind = 'tallpalm' if dark else 'palm'
    elif z == 'nursery': kind = 'tallpalm'
    elif z == 'youngpalm': kind = 'youngpalm'
    elif z == 'thicket': kind = 'bigshrub'
    else: kind = z
    trees.append(dict(i=round(float(i), 2), j=round(float(j), 2), r=round(float(rad), 2), kind=kind, zone=z))
# nursery: keep only the few tallest (darkest, biggest) palms (Will: the potted ones get moved, maybe a few taller ones stay)
nur = sorted([t for t in trees if t['zone'] == 'nursery'], key=lambda t: -t['r'])
trees = [t for t in trees if t['zone'] != 'nursery'] + nur[:4]
# heights (m): pines short and bushy, ~20 ft max (Will); fan palms 2-6 m, tall Washingtonias 8-11 m; shrubs 1.5-4 m
rng = np.random.default_rng(7)
for t in trees:
    k, rr = t['kind'], t['r']
    t['h'] = round(float({'pine': min(6.4, max(3.5, rr * 1.9)), 'pepper': 7.0, 'tallpalm': rng.uniform(8, 11), 'palm': rng.uniform(2.5, 6), 'youngpalm': rng.uniform(1.2, 2.2),
                          'bigshrub': min(4.2, max(2, rr * 1.2)), 'shrub': min(2.5, max(1.2, rr * .9))}[k]), 1)
json.dump({'note': 'existing trees and big shrubs on the Centro Equino site, from the Esri aerial + the 11 Oct 2026 site photos (Will); grid i, j; crown radius r and height h in metres',
           'trees': trees}, open(OUT, 'w'), indent=0)
from collections import Counter; print(len(trees), Counter(t['kind'] for t in trees))
COL = {'pine': 'red', 'palm': 'yellow', 'tallpalm': 'orange', 'youngpalm': 'gold', 'bigshrub': 'cyan', 'shrub': 'deepskyblue', 'pepper': 'magenta'}
fig, ax = plt.subplots(figsize=(22, 14.6), dpi=110); ax.imshow(A.astype(np.uint8), extent=(0, 149, 99, 0))
ax.plot(PF[::10, 0], PF[::10, 1], '.', ms=1, color='white')
for t in trees: ax.add_patch(plt.Circle((t['i'], t['j']), t['r'] / CS, fill=False, color=COL[t['kind']], lw=1))
for k, c in COL.items(): ax.plot([], [], 'o', mfc='none', color=c, label=k)
ax.legend(loc='lower left'); ax.set_xticks(range(0, 150, 10)); ax.set_yticks(range(0, 100, 10)); ax.grid(color='w', lw=.2, alpha=.4); ax.set_ylim(75, 14); ax.set_xlim(25, 140)
fig.tight_layout(); fig.savefig(D + '/trees-pick.jpg', pil_kwargs={'quality': 80})
