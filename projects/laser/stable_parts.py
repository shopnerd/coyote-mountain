"""Centro Equino stable as glue-up print parts at the site-model scale (1 in = 40 ft, 1:480).

Walker's spec: 76 x 42 ft, 12 ft eave, 17 ft ridge, stone to 4.5 ft with stacked sticks above,
10 stalls (6 north, 4 on the east part of the south side, wash + tack at the south-west),
a 12 x 30 ft pipe-fenced run off every stall, 10 x 11 ft aisle doors in both gable ends.
At this scale the pipe posts and trusses are far below a nozzle width, so the structure is
shown by the body shape only; the runs' fences are thickened to print.

Parts (all mm, each its own STL, oriented to print without supports):
  1 body          walls + gable ends, stone line groove, stall and aisle door recesses
  2 roof panel    x2, printed flat, glued at the ridge (2 ft eave and gable overhangs)
  3 runs north    6 runs on a thin floor plate, fences upright
  4 runs south    4 runs, same
    python stable_parts.py
"""
import os, math, numpy as np, trimesh
from trimesh import creation, boolean

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'stable-1-480')
os.makedirs(OUT, exist_ok=True)
MM_PER_FT = 25.4 / 40.0          # 0.635

L, D, EAVE, RIDGE = 76.0, 42.0, 12.0, 17.0
STONE = 4.5
STALL, RUN = 12.0, 30.0
OVER = 2.0                        # roof overhang, ft
NOZ_FT = 0.8 / MM_PER_FT          # 0.8 mm printable wall, in feet (~1.26 ft)

def box(x0, x1, y0, y1, z0, z1):
    b = creation.box(extents=[x1 - x0, y1 - y0, z1 - z0])
    b.apply_translation([(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2]); return b

def U(ms): return boolean.union(ms, engine='manifold')
def Dff(a, bs): return boolean.difference([a] + list(bs), engine='manifold')

# ---------- 1 body: gable prism along x ----------
sec = trimesh.path.polygons.Polygon([(-D / 2, 0), (D / 2, 0), (D / 2, EAVE), (0, RIDGE), (-D / 2, EAVE)])
prism = creation.extrude_polygon(sec, L)            # section in XY, extruded along Z
v = prism.vertices.copy(); prism.vertices = np.column_stack([v[:, 2] - L / 2, v[:, 0], v[:, 1]])   # -> x along length
prism.fix_normals()
cuts = []
g = 0.3 / MM_PER_FT               # 0.3 mm groove depth
cuts.append(box(-L / 2 - 1, L / 2 + 1, -D / 2 - 1, -D / 2 + g, STONE - .35, STONE + .35))     # stone line, south
cuts.append(box(-L / 2 - 1, L / 2 + 1, D / 2 - g, D / 2 + 1, STONE - .35, STONE + .35))       # north
cuts.append(box(-L / 2 - 1, -L / 2 + g, -D / 2 - 1, D / 2 + 1, STONE - .35, STONE + .35))     # west
cuts.append(box(L / 2 - g, L / 2 + 1, -D / 2 - 1, D / 2 + 1, STONE - .35, STONE + .35))       # east
rd = 0.45 / MM_PER_FT             # door recess depth
for sx in (-1, 1):                # aisle doors 10 x 11 in both gable ends
    x = sx * L / 2
    cuts.append(box(x - rd if sx > 0 else x - 1, x + 1 if sx > 0 else x + rd, -5, 5, 0, 11))
xs = [-L / 2 + 2 + STALL * (k + .5) for k in range(6)]
for x in xs:                      # north stall doors 4 x 8
    cuts.append(box(x - 2, x + 2, D / 2 - rd, D / 2 + 1, 0, 8))
for x in xs:                      # south: wash, tack, 4 stalls, all with 4 x 8 doors
    cuts.append(box(x - 2, x + 2, -D / 2 - 1, -D / 2 + rd, 0, 8))
body = Dff(prism, cuts)

# ---------- 2 roof panel (print flat, x2) ----------
run = D / 2 + OVER; rise = (RIDGE - EAVE) * run / (D / 2)
slope_len = math.hypot(run, rise)
panel = box(0, L + 2 * OVER, 0, slope_len, 0, NOZ_FT)

# ---------- 3/4 runs: floor plate + 3-rail fences with posts ----------
FLOOR = 0.6 / MM_PER_FT
POST = 1.0 / MM_PER_FT           # 1 mm posts
RAIL_T = NOZ_FT; RAIL_H = 0.5 / MM_PER_FT
RAILS = (1.6, 3.4, 5.5 - RAIL_H)  # rail bottoms, ft (fence 5.5 ft)
def runs(n):
    parts = [box(0, n * STALL, 0, RUN, 0, FLOOR)]
    def fence(xa, ya, xb, yb):
        segL = math.hypot(xb - xa, yb - ya); nposts = max(2, int(math.ceil(segL / 12)) + 1)
        for k in range(nposts):
            t = k / (nposts - 1); px, py = xa + (xb - xa) * t, ya + (yb - ya) * t
            parts.append(box(px - POST / 2, px + POST / 2, py - POST / 2, py + POST / 2, FLOOR, FLOOR + 5.5))
        for h in RAILS:
            if xa == xb: parts.append(box(xa - RAIL_T / 2, xa + RAIL_T / 2, min(ya, yb), max(ya, yb), FLOOR + h, FLOOR + h + RAIL_H))
            else: parts.append(box(min(xa, xb), max(xa, xb), ya - RAIL_T / 2, ya + RAIL_T / 2, FLOOR + h, FLOOR + h + RAIL_H))
    for k in range(n + 1):
        fence(k * STALL, POST / 2, k * STALL, RUN - POST / 2)        # dividers (end ones are the outer sides)
    fence(0, RUN - POST / 2, n * STALL, RUN - POST / 2)                # outer long side
    return U(parts)

north, south = runs(6), runs(4)

def save(m, name):
    m = m.copy(); m.apply_scale(MM_PER_FT)
    b = m.bounds; m.apply_translation([-b[0][0], -b[0][1], -b[0][2]])    # sit on the bed at the origin
    fn = os.path.join(OUT, name); m.export(fn)
    ext = m.extents
    print(f'{name:28s} {ext[0]:6.1f} x {ext[1]:5.1f} x {ext[2]:5.1f} mm  watertight={m.is_watertight}  tris={len(m.faces)}')
    return m

pb = save(body, '1-body.stl')
save(panel, '2-roof-panel-print-2.stl')
save(north, '3-runs-north-6.stl')
save(south, '4-runs-south-4.stl')

# ---------- assembled preview (for the pack and a sanity check) ----------
roofA = panel.copy(); ang = math.atan2(rise, run)
roofA.apply_translation([-(L + 2 * OVER) / 2, -slope_len, 0]); roofA.apply_transform(trimesh.transformations.rotation_matrix(ang, [1, 0, 0])); roofA.apply_translation([0, 0, RIDGE])
roofB = roofA.copy(); roofB.apply_transform(trimesh.transformations.rotation_matrix(math.pi, [0, 0, 1]))
nr = north.copy(); nr.apply_translation([-L / 2 + 2, D / 2, 0])
sr = south.copy(); sr.apply_transform(trimesh.transformations.rotation_matrix(math.pi, [0, 0, 1])); sr.apply_translation([L / 2 - 2, -D / 2, 0])
scene = trimesh.util.concatenate([body, roofA, roofB, nr, sr]); scene.apply_scale(MM_PER_FT)
scene.export(os.path.join(OUT, 'assembled-preview.stl'))
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
fig = plt.figure(figsize=(9, 6), dpi=130); ax = fig.add_subplot(111, projection='3d')
tris, fcs = [], []
for m, c in ((body, '#b9ad97'), (roofA, '#6fa8d8'), (roofB, '#5d95c2'), (nr, '#c9b48f'), (sr, '#c9b48f')):
    mm = m.copy(); mm.apply_scale(MM_PER_FT)
    shade = 0.55 + 0.45 * np.clip(mm.face_normals @ np.array([-.4, -.5, .77]), 0, 1)
    base = np.array(matplotlib.colors.to_rgb(c))
    tris.append(mm.triangles); fcs.append(np.clip(base[None, :] * shade[:, None], 0, 1))
pc = Poly3DCollection(np.concatenate(tris), facecolors=np.concatenate(fcs), edgecolor='none'); ax.add_collection3d(pc)
ax.set_xlim(-35, 35); ax.set_ylim(-35, 35); ax.set_zlim(0, 25); ax.set_box_aspect((70, 70, 25)); ax.view_init(28, -55); ax.axis('off')
ax.set_title('Stable at 1:480 · 4 part types, 5 prints (roof panel x2)', fontsize=10)
fig.savefig(os.path.join(OUT, 'assembled-preview.png'), bbox_inches='tight')
