"""Everything growing on the site TODAY, for the existing-topography page (12 Oct 2026, Will: "quite a few missing plant dots,
e.g. where the covered stalls will go there are several stands of palms that need relocating; cross-reference the satellite").
Unlike existing_trees.json (the design: nursery palms moved, nothing under a building), this keeps every crown the Esri aerial
shows inside the site: nursery rows, the palm stands, shrubs. Kinds come from the same zones as existing_trees_pick.py.

    python existing_conditions.py <aerial-grid.png>   ->  existing_all.json  (+ existing_all_check.jpg overlay)
"""
import json, math, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
from skimage.feature import peak_local_max
HERE = os.path.dirname(os.path.abspath(__file__)); S = 4; CS = 400 / 149
A = np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float); R, G, B = A[..., 0], A[..., 1], A[..., 2]
exg = 2 * G - R - B; v = A.mean(2)
bg = ndi.median_filter(v, size=31)                          # the ground around each spot
con = bg - v                                                # a crown is clearly darker than the ground around it
veg = ndi.binary_opening((con > 16) & (G >= R - 8), iterations=1)
sm = ndi.gaussian_filter(np.where(veg, con, 0), 1.2)
dt = ndi.distance_transform_edt(veg)
pk = peak_local_max(sm, min_distance=3, threshold_abs=14)
d = json.load(open(os.path.join(HERE, 'centro-equino-2026-09-26-stalls16-nopad.json'), encoding='utf-8'))
fence = [s for s in d['strokes'] if s.get('name') == 'site fence'][0]
from existing_trees import footprints   # noqa: E402  (only its helpers)
from matplotlib.path import Path
r = math.radians(fence['rot']); c0, c1 = fence['c']
T = np.array(fence['tris']).reshape(-1, 3)
FP = np.stack([c0 + (T[:, 0] * math.cos(r) - T[:, 1] * math.sin(r)) / CS, c1 - (T[:, 0] * math.sin(r) + T[:, 1] * math.cos(r)) / CS], 1)
lo, hi = FP.min(0) - 1, FP.max(0) + 1                       # the fenced site's bounding box, a little margin
pick = {}
exec(open(os.path.join(HERE, 'existing_trees_pick.py'), encoding='utf-8').read().split('def zone')[1].join(['def zone', '']).split('\ntrees = []')[0].split('PF = ')[0]) if False else None
src = open(os.path.join(HERE, 'existing_trees_pick.py'), encoding='utf-8').read()
zsrc = src[src.index('def zone'):src.index("    return 'other'") + len("    return 'other'")]
exec(zsrc)                                                  # zone(i, j) from the design picker, same reading of the photos
out = []
for y, x in pk:
    i, j = x / S, y / S
    if not (lo[0] <= i <= hi[0] and lo[1] <= j <= hi[1]): continue
    if j < 19 or j > 72: continue                           # the vineyard road and the scrub-side road bound the site
    z = zone(i, j) or 'other'
    if z in (None,) : continue
    if i > 123 and j < 57: continue                         # east vineyard rows
    rad = float(min(4.5, max(.6, dt[y, x] / S * CS))); dark = v[max(0, y - 2):y + 3, max(0, x - 2):x + 3].mean() < 80
    if z == 'nursery': kind = 'palm'                         # potted palm rows (photos 8808-8820)
    elif z in ('palmgrove',): kind = 'palm'
    elif z == 'youngpalm': kind = 'palm'
    elif z == 'pine': kind = 'pine'
    elif z == 'pepper': kind = 'pepper'
    elif z in ('thicket', 'shrubpine', 'shrub'): kind = 'pine' if (dark and rad > 2.8) else 'shrub'
    else: kind = 'pine' if (dark and rad > 1.6) else ('palm' if rad < 2.4 else 'shrub')
    if con[y, x] < 20 and rad < 1.2: continue                                                  # faint specks
    out.append(dict(i=round(float(i), 2), j=round(float(j), 2), r=round(rad, 2), kind=kind, zone=z))
json.dump({'note': 'every crown on the site today (Esri aerial + 11 Oct photos), nothing removed for the design; for the existing-topography page', 'trees': out},
          open(os.path.join(HERE, 'existing_all.json'), 'w'), indent=0)
from collections import Counter; print(len(out), Counter(t['kind'] for t in out))
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
design = d['records'].get('existingTrees', [])
fig, axs = plt.subplots(1, 2, figsize=(26, 9), dpi=100)
for ax, L, t in ((axs[0], design, 'NOW on the page (design list)'), (axs[1], out, 'NEW: everything on the site today')):
    ax.imshow(A.astype(np.uint8), extent=(0, 149, 99, 0))
    for q in L: ax.add_patch(plt.Circle((q['i'], q['j']), q['r'] / CS, fill=False, lw=.9, color={'pine': 'red', 'palm': 'yellow', 'shrub': 'cyan', 'bigshrub': 'cyan', 'pepper': 'magenta', 'tallpalm': 'orange', 'youngpalm': 'yellow'}.get(q['kind'], 'w')))
    ax.set_xlim(25, 140); ax.set_ylim(75, 15); ax.set_title(f'{t}: {len(L)}', fontsize=14); ax.set_xticks([]); ax.set_yticks([])
fig.tight_layout(); fig.savefig(os.path.join(HERE, 'existing_all_check.jpg'), pil_kwargs={'quality': 80})

# merge (12 Oct): the design list's crowns are well sized (pines, shrubs, the east grove from site_extras), so keep those whole and
# add only what they miss, mostly the nursery and roadside palm rows. Written to records.existingAll for drain.existing_trees(all=True).
base = json.load(open(os.path.join(HERE, 'existing_trees.json')))['trees']          # before any structure was cleared
exec(open(os.path.join(HERE, 'drain.py'), encoding='utf-8').read().split('def existing_trees')[0].split("DRAWING=")[0])   # imports only
import importlib.util as _u
forest = []
try:
    src = open(os.path.join(HERE, 'drain.py'), encoding='utf-8').read()
    ns = {}; exec(src.split("plt.rcParams")[0], ns); exec(src[src.index('TREE_STYLE='):src.index('def existing_trees')], ns); forest = ns['_forest']()
except Exception as e: print('forest skipped:', e)
have = base + forest; add = []
for t in out:
    if t['i'] < 28 or (t['i'] > 85 and t['j'] > 69.5): continue                                # beyond the west road / south of the scrub-side road
    if any(math.hypot(t['i'] - q['i'], t['j'] - q['j']) * CS < max(1.2, q['r'] * .9) for q in have + add): continue
    add.append(t)
ALL = [{k: q[k] for k in ('i', 'j', 'r', 'kind')} for q in base + forest + add]
for fn in ('centro-equino-2026-09-26.json', 'centro-equino-2026-09-26-stalls16.json', 'centro-equino-2026-09-26-stalls16-nopad.json', 'centro-equino-2026-10-10-cafe-option2-trees.json'):
    p = os.path.join(HERE, fn); dd = json.load(open(p, encoding='utf-8')); dd.setdefault('records', {})['existingAll'] = ALL; json.dump(dd, open(p, 'w', encoding='utf-8'))
print('existing today:', len(base), 'design-list +', len(forest), 'east grove +', len(add), 'new =', len(ALL), Counter(t['kind'] for t in add))
fig, ax = plt.subplots(figsize=(14, 9), dpi=110); ax.imshow(A.astype(np.uint8), extent=(0, 149, 99, 0))
for q in base + forest: ax.add_patch(plt.Circle((q['i'], q['j']), q['r'] / CS, fill=False, lw=.9, color='red'))
for q in add: ax.add_patch(plt.Circle((q['i'], q['j']), max(.3, q['r'] / CS), fill=False, lw=1.1, color='yellow'))
ax.set_xlim(25, 140); ax.set_ylim(75, 15); ax.set_xticks([]); ax.set_yticks([]); ax.set_title('red = already drawn, yellow = added for the existing page')
fig.tight_layout(); fig.savefig(os.path.join(HERE, 'existing_all_check.jpg'), pil_kwargs={'quality': 82})
