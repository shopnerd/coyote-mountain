"""The trees already on the site (11 Oct 2026, Will after the site visit: "add those pines and other trees that aren't in the model").
Positions and crowns come from the Esri aerial; what each one is comes from the 83 GPS + compass photos of the visit
(existing_trees_pick.py -> existing_trees.json). The east pine grove is already modelled (site_extras.py 'pine forest') and is left out.
- pines: short, bushy to the ground, never limbed up, ~20 ft at most (Will)
- fan palms in the west rows, tall Washingtonias in the north clump, a few young palms
- the potted palm nursery under the covered stalls is moving (Will); only its 4 tallest palms stay, and none inside a structure
- big native shrubs (the round ones by the north road, the east thicket), small growth along the south fence, the pepper tree
Anything that would stand inside a building, the bleachers or a trough is dropped; trees on a planned fence line stay (and are listed).

    python existing_trees.py     ->  existing-trees.obj and an 'existing trees' object in the three drawings (rerun after site_extras.py)
"""
import json, math, os, random
import numpy as np
from matplotlib.path import Path
HERE = os.path.dirname(os.path.abspath(__file__))
from geo import cs, W, H
FILES = ('centro-equino-2026-09-26.json', 'centro-equino-2026-09-26-stalls16.json', 'centro-equino-2026-09-26-stalls16-nopad.json', 'centro-equino-2026-10-10-cafe-option2-trees.json')   # + café option 2 (trailer in the trees, Walker)
NAME, OBJ = 'existing trees', 'existing-trees.obj'
KEEP_CLEAR = ('walker barn 72x40', 'covered stalls', 'bleachers', 'trailer 8 x 40', 'stone trough (long)', 'wash pad trough', 'east trough', 'watering station 10ft', 'electrical room')

def ground(z, i, j):
    i = min(max(i, 0), W - 1.001); j = min(max(j, 0), H - 1.001); i0, j0 = int(i), int(j); fx, fy = i - i0, j - j0
    return z[j0, i0] * (1 - fx) * (1 - fy) + z[j0, i0 + 1] * fx * (1 - fy) + z[j0 + 1, i0] * (1 - fx) * fy + z[j0 + 1, i0 + 1] * fx * fy

def footprints(d):   # each structure's plan outline in grid i, j (the app's object frame: rot about c)
    out = {}
    for s in d['strokes']:
        if s.get('kind') != 'obj' or s.get('name') not in KEEP_CLEAR or not s.get('foot'): continue
        r = math.radians(s['rot']); c0, c1 = s['c']; sc = s.get('sc', 1)
        out[s['name']] = Path([(c0 + (x * sc * math.cos(r) - y * sc * math.sin(r)) / cs, c1 - (x * sc * math.sin(r) + y * sc * math.cos(r)) / cs) for x, y in s['foot']])
    return out

def edge_dist(P, i, j):   # grid distance from a point to a footprint outline
    V = P.vertices; best = 1e9
    for (ax, ay), (bx, by) in zip(V, np.roll(V, -1, 0)):
        dx, dy = bx - ax, by - ay; L = dx * dx + dy * dy or 1e-9; u = min(1, max(0, ((i - ax) * dx + (j - ay) * dy) / L)); best = min(best, math.hypot(ax + u * dx - i, ay + u * dy - j))
    return best

def lines(d):        # fences and the arena / round pen: trees keep 1 m off them
    L = []
    for s in d['strokes']:
        if s.get('kind') == 'obj' and 'fence' in (s.get('name') or ''):
            T = np.array(s['tris'] if not isinstance(s['tris'], str) else json.loads(s['tris'])).reshape(-1, 3); r = math.radians(s['rot']); c0, c1 = s['c']
            L.append(np.stack([c0 + (T[:, 0] * math.cos(r) - T[:, 1] * math.sin(r)) / cs, c1 - (T[:, 0] * math.sin(r) + T[:, 1] * math.cos(r)) / cs], 1)[::6])
    return np.concatenate(L) if L else np.zeros((0, 2))

class Mesh:          # faces in site metres: x = grid i * cs, y = -grid j * cs (north-ish up), z absolute
    def __init__(s): s.F, s.M = [], []
    def face(s, pts, m): s.F.append(pts); s.M.append(m)
    def ring(s, x, y, r, z, n, ph=0, sq=1): return [(x + r * math.cos(2 * math.pi * q / n + ph), y + r * sq * math.sin(2 * math.pi * q / n + ph), z) for q in range(n)]
    def band(s, a, b, m):
        n = len(a)
        for q in range(n): s.face([a[q], a[(q + 1) % n], b[(q + 1) % n], b[q]], m)
    def trunk(s, x, y, z0, z1, w, m='trunk'):
        a, b = s.ring(x, y, w, z0, 5), s.ring(x, y, w * .75, z1, 5); s.band(a, b, m)

def build(trees, z, rnd):
    m = Mesh()
    for t in trees:
        k, h, R_ = t['kind'], t['h'], max(.7, t['r']); x, y = t['i'] * cs, -t['j'] * cs; zg = ground(z, t['i'], t['j']); ph = rnd.uniform(0, 1)
        if k == 'pine':            # bushy to the ground, a soft irregular dome (never limbed up)
            m.trunk(x, y, zg - .2, zg + h * .35, .16)
            rings = [m.ring(x, y, R_ * f * rnd.uniform(.9, 1.08), zg + h * hz, 9, ph) for f, hz in ((.72, .05), (1, .33), (.92, .6), (.5, .86))]
            for a, b in zip(rings, rings[1:]): m.band(a, b, 'pine')
            m.face(rings[0][::-1], 'pine')
            for q in range(9): m.face([rings[-1][q], rings[-1][(q + 1) % 9], (x, y, zg + h)], 'pine')
        elif k in ('palm', 'tallpalm', 'youngpalm'):   # a trunk and a star of drooping fronds; short ones are fronds from the ground
            top = zg + h - .4; fr = {'tallpalm': 2.2, 'palm': min(2.2, max(1.2, R_)), 'youngpalm': .9}[k]
            if h > 2.4: m.trunk(x, y, zg - .2, top, {'tallpalm': .28, 'palm': .22, 'youngpalm': .1}[k])
            else: top = zg + h * .6
            nf = 11
            for q in range(nf):
                a = 2 * math.pi * q / nf + ph * 6; up = .35 if q % 2 else -.15
                tip = (x + fr * math.cos(a), y + fr * math.sin(a), top + up - fr * .45); mid = (x + fr * .55 * math.cos(a), y + fr * .55 * math.sin(a), top + up * .6 + .15)
                l = (x + fr * .5 * math.cos(a - .32), y + fr * .5 * math.sin(a - .32), top + .1); rr = (x + fr * .5 * math.cos(a + .32), y + fr * .5 * math.sin(a + .32), top + .1)
                m.face([(x, y, top + .25), l, tip], 'palm'); m.face([(x, y, top + .25), tip, rr], 'palm'); m.face([l, mid, tip], 'palm')
        elif k == 'pepper':        # a weeping, open crown on a short trunk
            m.trunk(x, y, zg - .2, zg + h * .45, .25)
            rings = [m.ring(x, y, R_ * f, zg + h * hz, 10, ph) for f, hz in ((.95, .22), (1.05, .5), (.8, .8), (.35, .97))]
            for a, b in zip(rings, rings[1:]): m.band(a, b, 'pepper')
            m.face(rings[0][::-1], 'pepper'); m.face(rings[-1], 'pepper')
        else:                      # shrubs: a low lumpy mound from the ground
            n = 8; rings = [m.ring(x, y, R_ * f * rnd.uniform(.88, 1.1), zg + h * hz, n, ph) for f, hz in ((.85, -.05), (1, .35), (.7, .78))]
            for a, b in zip(rings, rings[1:]): m.band(a, b, 'scrub')
            for q in range(n): m.face([rings[-1][q], rings[-1][(q + 1) % n], (x, y, zg + h)], 'scrub')
    return m

def stroke(m, z, objname=OBJ):
    V = np.array([p for f in m.F for p in f]); cx, cy, mz = V[:, 0].mean(), V[:, 1].mean(), V[:, 2].min()
    tris = []
    for f in m.F:
        for k in range(1, len(f) - 1):
            for q in (f[0], f[k], f[k + 1]): tris += [round(q[0] - cx, 3), round(q[1] - cy, 3), round(q[2] - mz, 3)]
    with open(os.path.join(HERE, objname), 'w', newline='\n') as fo:   # the obj keeps the material groups for the viewer export
        fo.write(f'# {NAME}: the trees already on the site, from the aerial and the 11 Oct 2026 site photos\n# unit m\n# name {NAME}\n')
        for f in m.F:
            for p in f: fo.write('v %.3f %.3f %.3f\n' % (p[0] - cx, p[1] - cy, p[2] - mz))
        n, last = 1, None
        for f, mt in zip(m.F, m.M):
            if mt != last: fo.write(f'usemtl {mt}\n'); last = mt
            fo.write('f ' + ' '.join(str(n + k) for k in range(len(f))) + '\n'); n += len(f)
    c = [cx / cs, -cy / cs]; T = np.array(tris).reshape(-1, 3)
    pts = sorted(map(tuple, T[:, :2].round(2))); cross = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]); lo, up = [], []
    for q in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], q) <= 0: lo.pop()
        lo.append(q)
    for q in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], q) <= 0: up.pop()
        up.append(q)
    return dict(color='ink', shape=False, kind='obj', c=c, name=NAME, unit='m', rot=0, sc=1, lift=float(mz - ground(z, *c)), tris=tris,
                foot=[list(p) for p in lo[:-1] + up[:-1]], h=float(T[:, 2].max()), w=1, a=1, dash=False, pts=[[c[0], c[1], .5]])

if __name__ == '__main__':
    src = json.load(open(os.path.join(HERE, 'existing_trees.json')))['trees']
    for fn in FILES:
        p = os.path.join(HERE, fn); d = json.load(open(p, encoding='utf-8')); z = np.array(d['z'], float).reshape(H, W)
        FP, FL = footprints(d), lines(d); trees, gone, onfence = [], [], []
        # 12 Oct (Will: "more plants represented, but not under the covered stalls or other undesirable places"): the full existing
        # layer (existing_conditions.py: design + aerial + Will's markup), minus the moving nursery rows and the east grove (its own
        # object), minus anything on a road/trail or inside the arena and round pen; the structure rule below still applies
        full = (d.get('records') or {}).get('existingAll')
        if full:
            PATHS = [(np.array([q[:2] for q in s_['pts']]), s_.get('pw', 1.5)) for s_ in d['strokes'] if s_.get('kind') == 'path']
            def on_path(t):
                for P_, w_ in PATHS:
                    seg = np.diff(P_, axis=0); L2 = (seg ** 2).sum(1) + 1e-9; q_ = np.array([t['i'], t['j']]) - P_[:-1]
                    u = np.clip((q_ * seg).sum(1) / L2, 0, 1); dmin = np.hypot(*(P_[:-1] + seg * u[:, None] - [t['i'], t['j']]).T).min() * cs
                    if dmin < w_ / 2 + max(.6, t['r'] * .4): return True
                return False
            RINGS = []
            for nm in ('arena fence', 'round pen fence'):
                o = next((s_ for s_ in d['strokes'] if s_.get('name') == nm), None)
                if o: r_ = math.radians(o['rot']); RINGS.append(Path([(o['c'][0] + (x * math.cos(r_) - y * math.sin(r_)) / cs, o['c'][1] - (x * math.sin(r_) + y * math.cos(r_)) / cs) for x, y in o['foot']]))
            rng_h = random.Random(5)
            def hgt(t):
                if 'h' in t: return t
                k = t['kind']; rr = t['r']
                t = dict(t, h=round({'pine': min(6.4, max(3.5, rr * 1.9)), 'palm': rng_h.uniform(1.8, 4.3), 'shrub': min(2.5, max(1.2, rr * .9)),
                                     'bigshrub': min(4.2, max(2, rr * 1.2)), 'tallpalm': 6.8, 'youngpalm': 1.4, 'pepper': 7.0}.get(k, 2.0), 1)); return t
            design_h = {(round(q['i'], 2), round(q['j'], 2)): q for q in src}
            src_ = []
            for t in full:
                if t.get('src') in ('forest', 'will-nursery'): continue
                if any(R_.contains_point((t['i'], t['j'])) for R_ in RINGS) or on_path(t): continue
                t = dict(design_h.get((round(t['i'], 2), round(t['j'], 2)), t)); src_.append(hgt(t))
        else: src_ = src
        for t in src_:
            hit = [nm for nm, P in FP.items() if P.contains_point((t['i'], t['j'])) or edge_dist(P, t['i'], t['j']) * cs < max(.8, t['r'] * .5)]   # trunk at least ~1 m off a wall
            if not hit and len(FL) and np.hypot(FL[:, 0] - t['i'], FL[:, 1] - t['j']).min() * cs < max(1.0, t['r'] * .6): onfence.append((t['kind'], t['i'], t['j']))   # kept; the fence works around it
            (gone if hit else trees).append((t, hit))
        trees = [t for t, _ in trees]
        d.setdefault('records', {})['existingTrees'] = [{k: t[k] for k in ('i', 'j', 'r', 'h', 'kind')} for t in trees]   # 11 Oct: the plans draw these crowns
        d['strokes'] = [s for s in d['strokes'] if s.get('name') != NAME] + [stroke(build(trees, z, random.Random(17)), z, OBJ if fn == 'centro-equino-2026-09-26-stalls16-nopad.json' else OBJ.replace('.obj', '-' + fn[:-5] + '.obj'))]   # one obj per drawing (the viewer export reads its materials)
        json.dump(d, open(p, 'w', encoding='utf-8'))
        from collections import Counter
        print(fn, ':', len(trees), 'existing trees', dict(Counter(t['kind'] for t in trees)), '; left out (inside a structure):', [(t['kind'], h[0]) for t, h in gone], '; on a fence line:', onfence)
