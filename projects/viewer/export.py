"""Data for the Centro Equino 3D viewer (27 Sep): graded terrain, the aerial photo for it, every placed object as a
triangle soup in site metres (roofs split off so they can be hidden), roads, ditches, the natural sink and labels.

    python export.py [outdir]   ->  data.json + aerial.jpg      (reads ../centro-equino-2026-09-26-stalls16-nopad.json)
Frame: x = grid i * cs, z = grid j * cs (site grid, rotated 318 deg from north), y = elevation - base (metres).
"""
import base64, json, math, os, sys, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from geo import GR, W, H, cs
import geo18
OUT = sys.argv[1] if len(sys.argv) > 1 else HERE
os.makedirs(OUT, exist_ok=True)
d = json.load(open(os.path.join(os.path.dirname(HERE), 'centro-equino-2026-09-26-stalls16-nopad.json'), encoding='utf-8'))
z = np.array(d['z'], float).reshape(H, W); Y0 = float(z.min()) - 1.0
b64 = lambda a: base64.b64encode(np.asarray(a, np.float32).tobytes()).decode()

def samp(i, j):
    i = min(max(i, 0), W - 1.001); j = min(max(j, 0), H - 1.001); i0, j0 = int(i), int(j); fx, fy = i - i0, j - j0
    return z[j0, i0] * (1 - fx) * (1 - fy) + z[j0, i0 + 1] * fx * (1 - fy) + z[j0 + 1, i0] * (1 - fx) * fy + z[j0 + 1, i0 + 1] * fx * fy

STYLE = {   # name -> (group, body colour, roof colour, roof threshold above its own base in m)
    'walker barn 72x40': ('stable', '#a89c86', '#4a4f55', 3.3),
    'covered stalls': ('stalls', '#f1efe9', '#c3c7c9', 2.9),
    'arena fence': ('fence', '#f4f2ec', None, 0), 'round pen fence': ('fence', '#f4f2ec', None, 0),
    'site fence': ('fence', '#e9e6de', None, 0), 'cross fence': ('fence', '#e9e6de', None, 0),
    'stone trough 12x4': ('water', '#a79f90', None, 0), 'watering station 10ft': ('water', '#a79f90', None, 0),
    'trailer 8 x 40': ('vehicle', '#f2f2f0', None, 0),
}
MATOBJ = {'walker barn 72x40': 'centro-equino-barn.obj', 'covered stalls': 'covered-stalls.obj'}   # tagged meshes: split by material
def obj_labels(path):                    # one material label per triangle, in the order topo.html triangulates the faces
    lab, cur, vn = [], 'body', 0
    for line in open(path, encoding='utf-8'):
        if line.startswith('usemtl '): cur = line.split()[1]
        elif line.startswith('f '): lab += [cur] * (len(line.split()) - 3)
    return lab
objs = []
for s in d['strokes']:
    if s.get('kind') != 'obj': continue
    t = s['tris'] if not isinstance(s['tris'], str) else json.loads(s['tris'])
    T = np.array(t, float).reshape(-1, 3, 3) * s.get('sc', 1)
    r = math.radians(s['rot']); c0, c1 = s['c']; z0 = samp(c0, c1) + s.get('lift', 0)
    gi = c0 + (T[..., 0] * math.cos(r) - T[..., 1] * math.sin(r)) / cs
    gj = c1 - (T[..., 0] * math.sin(r) + T[..., 1] * math.cos(r)) / cs
    X, Z, Yv = gi * cs, gj * cs, z0 + T[..., 2] - Y0
    P = np.stack([X, Yv, Z], -1)                                        # (n, 3 verts, xyz)
    name = s['name']; grp, col, rcol, thr = STYLE.get(name, ('vehicle', {'white': '#f2f2f0', 'silver': '#b9bcbf', 'grey': '#4a4d50', 'red': '#b0302a'}.get(name.split()[-1], '#cccccc'), None, 0))
    roof = np.zeros(len(P), bool)
    if rcol:
        nrm = np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]); nz = np.abs(nrm[:, 1]) / (np.linalg.norm(nrm, axis=1) + 1e-9)
        roof = (T[..., 2].min(1) > thr) & (nz > .3)
    o = dict(name=name, group=grp, color=col, body=b64(P[~roof].reshape(-1)))
    if roof.any(): o.update(roof=b64(P[roof].reshape(-1)), roofColor=rcol)
    if name in MATOBJ:
        lab = np.array(obj_labels(os.path.join(os.path.dirname(HERE), MATOBJ[name])))
        if len(lab) == len(P):
            o = dict(name=name, group=grp, parts={m_: b64(P[lab == m_].reshape(-1)) for m_ in sorted(set(lab))})
        else: print('!! material labels do not match the mesh for', name, len(lab), len(P))
    objs.append(o)

paths = [dict(name=s['name'], w=float(s.get('pw', 1.5)), pts=[[round(p[0] * cs, 2), round(p[1] * cs, 2)] for p in s['pts']])
         for s in d['strokes'] if s.get('kind') == 'path']
ditches = [dict(name=r['name'], pts=[[round(q[0] * cs, 2), round(q[1] * cs, 2)] for q in (GR(*p) for p in r['pts'])]) for r in d['records']['ditches']]
sink = [s for s in d['strokes'] if s.get('name') == 'natural water sink']
sink = [[round(p[0] * cs, 2), round(p[1] * cs, 2)] for p in sink[0]['pts']] if sink else []

def centre(name):
    for s in d['strokes']:
        if s.get('name') == name: c = s.get('c') or s['pts'][0]; return [round(c[0] * cs, 1), round(c[1] * cs, 1)]
LABELS = [('Establo', 'Stable', 'walker barn 72x40'), ('Caballerizas techadas', 'Covered stalls', 'covered stalls'),
          ('Pista oval', 'Arena', 'arena fence'), ('Corral redondo', 'Round pen', 'round pen fence'),
          ('Bebedero de piedra', 'Stone trough', 'stone trough 12x4'), ('Bajo natural', 'Natural sink', 'natural water sink'),
          ('Bebedero existente', 'Watering station', 'watering station 10ft'), ('Estacionamiento', 'Parking', 'parked car 3 · dark grey')]
labels = []
for es, en, nm in LABELS:
    c = centre(nm)
    if c is None: c = centre(nm.replace('·', '·')) or next((centre(s['name']) for s in d['strokes'] if (s.get('name') or '').startswith('parked car 3')), None)
    if c: labels.append(dict(es=es, en=en, x=c[0], z=c[1]))

# north in this frame: the site grid is turned 318 deg; grid (i, j) of true north and east
t = math.radians(float(d['sliders']['rot']))
north = [round(math.sin(t) * -1 * -1, 4), 0]
n_ij = (-math.sin(t), -math.cos(t)); e_ij = (math.cos(t), -math.sin(t))          # from geo.GR: sx = dx cos t - dy sin t, j = -sy/cs
data = dict(grid=[W, H], cs=cs, y0=Y0, z=b64(z.reshape(-1) - Y0), objects=objs, paths=paths, ditches=ditches, sink=sink, labels=labels,
            north=[round(n_ij[0], 4), round(-(-math.cos(t)) * -1, 4)], lat=float(d['world']['lat']),
            n_ij=[round(v, 4) for v in n_ij], e_ij=[round(v, 4) for v in e_ij])
# check the directions against the conversion itself
la0, lo0 = d['world']['lat'], d['world']['lon']; g0 = GR(la0, lo0); gN = GR(la0 + .001, lo0); gE = GR(la0, lo0 + .001)
vn = np.array(gN) - g0; ve = np.array(gE) - g0; data['n_ij'] = list(np.round(vn / np.linalg.norm(vn), 4)); data['e_ij'] = list(np.round(ve / np.linalg.norm(ve), 4))
data.pop('north')
json.dump(data, open(os.path.join(OUT, 'data.json'), 'w'), separators=(',', ':'))
im = geo18.render(0, 0, W - 1, H - 1, 10); im.save(os.path.join(OUT, 'aerial.jpg'), quality=82, optimize=True)
print('objects', len(objs), 'paths', len(paths), 'ditches', len(ditches), 'labels', len(labels), '| data.json', os.path.getsize(os.path.join(OUT, 'data.json')) // 1024, 'KB | aerial', im.size, os.path.getsize(os.path.join(OUT, 'aerial.jpg')) // 1024, 'KB')
print('north', data['n_ij'], 'east', data['e_ij'])
