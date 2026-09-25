"""Centro Equino: stacked laser-cut site model of the FINISHED grade.

1 layer = 1 ft of elevation, 1/8 in board, horizontal scale 1 in = 40 ft (1:480, so 5x vertical).
Each layer is cut as a ring (hollow under the layer above, keeping a 3/4 in glue lip) and nested
onto 32 x 18 in sheets. On every layer we engrave: the outline of the next layer up (glue line),
the design (pads, roads, paddocks, arena, pen, barn, water), the operator sheet's 50 ft stake grid,
and the layer's elevation. The base layer also gets the grid letters/numbers, scale and north.

Colours for the laser: red = cut, blue = score/vector engrave, black text = raster engrave.

    python site_layers.py  [path to the topo drawing .json]
"""
import json, math, os, sys
import numpy as np
from scipy.ndimage import zoom
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, MultiPolygon, LineString, Point, box
from shapely.ops import unary_union
from shapely import affinity
from shapely.prepared import prep

SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser(r'~/Downloads/centro-equino-final-2026-09-24.json')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
os.makedirs(OUT, exist_ok=True)

FT = 0.3048
SCALE_FT_PER_IN = 40.0          # 1 in = 40 ft
MARGIN_FT = 20.0
LIP_IN = 0.75                   # glue lip under the next layer
SHEET = (32.0, 18.0)            # laser bed, in
EDGE = 0.25                     # sheet edge margin, in
GAP = 0.12                      # spacing between parts, in
UPS = 6                         # grid upsampling for smooth contours

p = json.load(open(SRC, encoding='utf-8'))
W, H = p['grid']
cell_ft = float(p['sliders']['siteW']) / (W - 1) / FT
z = np.array(p['z'], float).reshape(H, W) / FT
S = p['strokes']
to_in = cell_ft / SCALE_FT_PER_IN       # grid cells -> model inches

loop = [s for s in S if s.get('shape') and not s.get('name') and len(s['pts']) == 10 and abs(s['pts'][0][0] - 26.6) < .3][0]
fence = Polygon([q[:2] for q in loop['pts']])
M = fence.buffer(MARGIN_FT / cell_ft, join_style=2)          # model outline, grid coords
x0, y0, x1, y1 = M.bounds

# ---- smooth finished-grade surface on a fine grid ----
zf = zoom(z, UPS, order=3)
ys = np.arange(zf.shape[0]) / UPS
xs = np.arange(zf.shape[1]) / UPS
X, Y = np.meshgrid(xs, ys)

def region_at_or_above(e):
    """Polygon(s) where finished grade >= e, in grid coords."""
    fig, ax = plt.subplots()
    cs = ax.contourf(X, Y, zf, levels=[e, 1e6])
    polys = []
    for path in cs.get_paths():
        for poly in path.to_polygons():
            if len(poly) < 3: continue
            polys.append(Polygon(poly))
    plt.close(fig)
    # to_polygons returns outer rings and holes as separate rings; rebuild by even-odd
    geom = None
    for q in sorted(polys, key=lambda g: -abs(g.area)):
        q = q.buffer(0)
        geom = q if geom is None else geom.symmetric_difference(q)
    return (geom if geom is not None else Polygon()).buffer(0)

base_e = int(math.floor(min(z[j, i] for j in range(H) for i in range(W) if M.contains(Point(i, j)))))
top_e = int(math.ceil(max(z[j, i] for j in range(H) for i in range(W) if M.contains(Point(i, j)))))
levels = list(range(base_e, top_e + 1))

R = {}
for e in levels:
    g = M if e == base_e else region_at_or_above(e).intersection(M)
    g = g.buffer(0.15).buffer(-0.15).simplify(0.08)           # drop pixel noise
    if isinstance(g, MultiPolygon):
        g = MultiPolygon([q for q in g.geoms if q.area * to_in ** 2 > 0.02])
    elif g.area * to_in ** 2 <= 0.02:
        g = Polygon()
    R[e] = g
levels = [e for e in levels if not R[e].is_empty]

lip = LIP_IN / to_in
pieces = []
for k, e in enumerate(levels):
    above = R[levels[k + 1]] if k + 1 < len(levels) else Polygon()
    solid = R[e].difference(above.buffer(-lip)) if not above.is_empty else R[e]
    solid = solid.buffer(0)
    exposed = R[e].difference(above).buffer(0)
    pieces.append(dict(e=e, n=k + 1, solid=solid, next=above, exposed=exposed))

# ---- design features to engrave (grid coords) ----
def foot(o):
    r = math.radians(o['rot']); sc = o.get('sc', 1); c = o['c']; s = float(p['sliders']['siteW']) / (W - 1)
    return [(c[0] + (x * sc * math.cos(r) - y * sc * math.sin(r)) / s, c[1] - (x * sc * math.sin(r) + y * sc * math.cos(r)) / s) for x, y in o['foot']]

def min_rect(P):
    P = np.array(P); best = None
    for k in range(len(P)):
        a, c = P[k], P[(k + 1) % len(P)]; e = c - a; Ln = np.hypot(*e)
        if Ln < 1e-6: continue
        u = e / Ln; v = np.array([-u[1], u[0]]); s_ = P @ u; t_ = P @ v
        A = np.ptp(s_) * np.ptp(t_)
        if best is None or A < best[0]: best = (A, u, v, s_.min(), s_.max(), t_.min(), t_.max())
    _, u, v, s0, s1, t0, t1 = best
    return [tuple(u * a + v * b) for a, b in ((s0, t0), (s1, t0), (s1, t1), (s0, t1))]

features = []   # (geometry, kind)
for s in S:
    nm = s.get('name') or ''
    if s.get('kind') == 'path':
        features.append((LineString([q[:2] for q in s['pts']]), 'road'))
    elif s.get('kind') == 'obj' and nm in ('walker barn 72x40', 'four paddocks', 'stone trough 12x4', 'watering station 10ft'):
        r = min_rect(foot(s)) if nm != 'watering station 10ft' else None
        if r: features.append((Polygon(r).exterior, 'building'))
    elif nm in ('natural water sink', 'existing watering station'):
        features.append((Polygon([q[:2] for q in s['pts']]).exterior, 'water'))
for i in (1, 2):   # arena and round pen outlines
    features.append((LineString([q[:2] for q in S[i]['pts']]), 'building'))
features.append((fence.exterior, 'fence'))
barn = [s for s in S if s.get('name') == 'walker barn 72x40'][0]
barn_rect = min_rect(foot(barn))

# stake grid (same as the operator sheet): 50 ft, columns A.., rows 1..
step = 50 / cell_ft
gx = np.arange(step / 2, W - 1, step); gy = np.arange(step / 2, H - 1, step)
grid_lines = [LineString([(x, 0), (x, H - 1)]) for x in gx] + [LineString([(0, y), (W - 1, y)]) for y in gy]

# ---- nesting onto sheets ----
def to_model(g):
    """grid coords -> inches, origin at model bbox corner."""
    return affinity.scale(affinity.translate(g, -x0, -y0), to_in, to_in, origin=(0, 0))

for pc in pieces:
    pc['m_solid'] = to_model(pc['solid'])
    pc['area'] = pc['m_solid'].area

sheets = []   # list of dicts: placed list, occupied geometry
def try_place(pc):
    g0 = pc['m_solid']
    for sh in sheets:
        occ = prep(sh['occ']) if not sh['occ'].is_empty else None
        boxes = sh.setdefault('boxes', [])
        for ang in (0, 180, 90, 270):
            g = affinity.rotate(g0, ang, origin=(0, 0)).buffer(GAP / 2)
            bx0, by0, bx1, by1 = g.bounds; w, h = bx1 - bx0, by1 - by0
            if w > SHEET[0] - 2 * EDGE or h > SHEET[1] - 2 * EDGE: continue
            for ty in np.arange(EDGE, SHEET[1] - EDGE - h + 1e-6, 0.5):
                for tx in np.arange(EDGE, SHEET[0] - EDGE - w + 1e-6, 0.5):
                    # cheap test first: skip positions whose box sits wholly inside a placed part's solid box region
                    gg = affinity.translate(g, tx - bx0, ty - by0)
                    if occ is None or not occ.intersects(gg):
                        return sh, ang, (tx - bx0, ty - by0)
    return None

order = sorted(pieces, key=lambda q: -q['area'])
for pc in order:
    r = try_place(pc)
    if r is None:
        sheets.append(dict(placed=[], occ=Polygon()))
        r = try_place(pc)
    sh, ang, (dx, dy) = r
    pc['sheet'] = sheets.index(sh); pc['ang'] = ang; pc['dx'] = dx; pc['dy'] = dy
    sh['placed'].append(pc); print(f"layer {pc['n']:2d} ({pc['e']} ft) -> sheet {pc['sheet']+1}", flush=True)
    sh['occ'] = unary_union([sh['occ'], affinity.translate(affinity.rotate(pc['m_solid'], ang, origin=(0, 0)), dx, dy).buffer(GAP / 2).simplify(0.02)])

def place(pc, g_grid):
    return affinity.translate(affinity.rotate(to_model(g_grid), pc['ang'], origin=(0, 0)), pc['dx'], pc['dy'])

# ---- SVG writer ----
def path_d(g):
    out = []
    def ring(coords):
        c = list(coords)
        return 'M' + ' L'.join(f'{x:.4f},{y:.4f}' for x, y in c) + ' Z'
    def line(coords):
        c = list(coords)
        return 'M' + ' L'.join(f'{x:.4f},{y:.4f}' for x, y in c)
    geoms = getattr(g, 'geoms', [g])
    for q in geoms:
        if q.is_empty: continue
        if q.geom_type == 'Polygon':
            out.append(ring(q.exterior.coords)); out += [ring(r.coords) for r in q.interiors]
        elif q.geom_type in ('LineString', 'LinearRing'):
            out.append(line(q.coords))
        elif q.geom_type in ('MultiLineString', 'GeometryCollection', 'MultiPolygon'):
            out.append(path_d(q))
    return ' '.join(o for o in out if o)

def label_point(g):
    """a point well inside g for a label"""
    if g.is_empty: return None
    best = None
    for q in getattr(g, 'geoms', [g]):
        if q.geom_type != 'Polygon' or q.area < 1e-6: continue
        pt = q.representative_point()
        d = q.exterior.distance(pt)
        if best is None or d > best[1]: best = (pt, d, q)
    if best is None: return None
    # poles of inaccessibility, cheap version
    try:
        from shapely.ops import polylabel
        pt = polylabel(best[2], tolerance=0.02)
        return pt, best[2].exterior.distance(pt)
    except Exception:
        return best[0], best[1]

RED, BLUE, GREEN = '#ff0000', '#0000ff', '#00a000'
svgs = []
for si, sh in enumerate(sheets):
    parts = []
    for pc in sh['placed']:
        cut = place(pc, pc['solid'])
        parts.append(f'<path d="{path_d(cut)}" fill="none" stroke="{RED}" stroke-width="0.001"/>')
        if not pc['next'].is_empty:
            glue = place(pc, pc['next'].intersection(pc['solid'].buffer(0.01)).boundary)
            parts.append(f'<path d="{path_d(glue)}" fill="none" stroke="{BLUE}" stroke-width="0.001"/>')
        ex = pc['exposed']
        exp_prep = ex.buffer(-0.05)
        for f, kind in features:
            seg = f.intersection(exp_prep)
            if seg.is_empty: continue
            parts.append(f'<path d="{path_d(place(pc, seg))}" fill="none" stroke="{BLUE}" stroke-width="0.001"/>')
        for gl in grid_lines:
            seg = gl.intersection(exp_prep)
            if seg.is_empty: continue
            parts.append(f'<path d="{path_d(place(pc, seg))}" fill="none" stroke="{GREEN}" stroke-width="0.001"/>')
        lp = label_point(place(pc, ex))
        if lp:
            pt, d = lp; fs = max(0.08, min(0.22, d * 0.9))
            parts.append(f'<text x="{pt.x:.3f}" y="{pt.y + fs * .35:.3f}" font-family="Arial" font-size="{fs:.3f}" text-anchor="middle" fill="#000">{pc["n"]} · {pc["e"]}</text>')
        if pc['n'] == 1:   # base layer: stake grid labels, north, scale, title
            b = place(pc, M); bx0, by0, bx1, by1 = b.bounds
            for k, x in enumerate(gx):
                q = place(pc, Point(x, y0 + 1.2))
                if b.contains(q): parts.append(f'<text x="{q.x:.3f}" y="{q.y:.3f}" font-family="Arial" font-size="0.18" text-anchor="middle" fill="#000">{chr(65 + k)}</text>')
            for k, y in enumerate(gy):
                q = place(pc, Point(x0 + 1.5, y))
                if b.contains(q): parts.append(f'<text x="{q.x:.3f}" y="{q.y + .06:.3f}" font-family="Arial" font-size="0.18" text-anchor="middle" fill="#000">{k + 1}</text>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{SHEET[0]}in" height="{SHEET[1]}in" viewBox="0 0 {SHEET[0]} {SHEET[1]}">'
           f'<rect x="0" y="0" width="{SHEET[0]}" height="{SHEET[1]}" fill="none" stroke="#cccccc" stroke-width="0.01"/>' + ''.join(parts) + '</svg>')
    fn = os.path.join(OUT, f'centro-equino-site-sheet-{si + 1:02d}.svg')
    open(fn, 'w', encoding='utf-8').write(svg); svgs.append(fn)

# ---- stepped preview (what the stacked model looks like from above) ----
step_h = np.floor(np.clip(zf, base_e, top_e))
fig, ax = plt.subplots(figsize=(14, 8), dpi=110)
ls = matplotlib.colors.LightSource(azdeg=315, altdeg=35)
rgb = ls.shade(step_h, cmap=plt.cm.YlOrBr_r, vert_exag=5, blend_mode='soft', vmin=base_e - 10, vmax=top_e + 5)
ax.imshow(rgb, extent=(-.5 / UPS, W - 1, H - 1, -.5 / UPS))
for f, kind in features:
    for q in getattr(f, 'geoms', [f]):
        xy = np.array(q.coords); ax.plot(xy[:, 0], xy[:, 1], color={'road': '#7a5a2a', 'building': '#222', 'water': '#1f78c8', 'fence': '#444'}[kind], lw=.8)
mx, my = M.exterior.xy; ax.plot(mx, my, color='k', lw=1.5)
ax.set_xlim(x0 - 2, x1 + 2); ax.set_ylim(y1 + 2, y0 - 2); ax.set_aspect('equal'); ax.axis('off')
ax.set_title(f'Stacked model preview · {len(pieces)} layers of 1/8 in · 1 in = 40 ft · {len(sheets)} sheets 32 x 18 in', fontsize=11)
fig.savefig(os.path.join(OUT, 'preview-stepped.png'), bbox_inches='tight'); plt.close(fig)

# ---- summary ----
info = dict(layers=len(pieces), base_ft=base_e, top_ft=levels[-1], sheets=len(sheets),
            model_in=[round((x1 - x0) * to_in, 2), round((y1 - y0) * to_in, 2), round(len(pieces) * 0.125, 2)],
            barn_rect_grid=[list(map(float, q)) for q in barn_rect],
            barn_pad_layer=next((pc['n'] for pc in pieces if pc['exposed'].buffer(0.5).contains(Polygon(barn_rect).centroid)), None),
            board_sq_in=round(sum(pc['area'] for pc in pieces), 0))
json.dump(info, open(os.path.join(OUT, 'site-model-info.json'), 'w'), indent=1)
print(json.dumps(info, indent=1))
