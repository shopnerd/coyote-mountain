"""Centro Equino stable as glue-up print parts at the site-model scale (1 in = 40 ft, 1:480).

24 Sep design: 72 x 40 ft on 12 in pipe portal frames, 12 ft eave, 17 ft ridge, rock to 4.5 ft
all round with tomato stakes above, a 14 ft entry open to the rafters at both gable ends, 2 ft roof
overhang on the long sides only. Walker's layout: 6 stalls north, each with a 12 x 40 ft run;
wash, tack, feed and a 36 ft alfalfa store on the south. (The 76 x 42 ten-stall parts are kept in
out-2026-09-23-76x42/stable-1-480.) At this scale the stakes and pipes are below a nozzle width, so
the walls print solid with the rock line scored; the runs' fences are thickened to print.

Parts (all mm, each its own STL, oriented to print without supports):
  1 body          walls + gable ends, stone line groove, stall and aisle door recesses
  2 roof panel    x2, printed flat, glued at the ridge (2 ft eave and gable overhangs)
  3 runs north    6 runs of 12 x 40 ft on a thin floor plate, fences upright
    python stable_parts.py
"""
import os, math, numpy as np, trimesh
from trimesh import creation, boolean

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'stable-1-480')
os.makedirs(OUT, exist_ok=True)
MM_PER_FT = 25.4 / 40.0          # 0.635

L, D, EAVE, RIDGE = 72.0, 40.0, 12.0, 17.0
STONE = 4.5
RUN = 40.0
OVER = 2.0                        # roof overhang on the long sides, ft
ENTRY = 14.0                      # gable entries, open to the rafters
NOZ_FT = 0.8 / MM_PER_FT          # 0.8 mm printable wall, in feet (~1.26 ft)

def box(x0, x1, y0, y1, z0, z1):
    b = creation.box(extents=[x1 - x0, y1 - y0, z1 - z0])
    b.apply_translation([(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2]); return b

def U(ms): return boolean.union(ms, engine='manifold')
def Dff(a, bs): return boolean.difference([a] + list(bs), engine='manifold')

# ---------- 1 body: open-top walls on a floor, stalls inside ----------
WALL = 2.0; T = NOZ_FT                 # outer walls 2 ft; inside partitions one nozzle-width
AISLE = 14.0; ROW = 12.0; PART_H = 8.0; ROOM_H = 10.0
FLOOR_B = 0.6 / MM_PER_FT
hx, hy = L / 2, D / 2
solid = [box(-hx, hx, -hy, hy, 0, FLOOR_B)]                                  # floor
solid += [box(-hx, hx, hy - WALL, hy, 0, EAVE), box(-hx, hx, -hy, -hy + WALL, 0, EAVE),    # long walls
          box(-hx, -hx + WALL, -hy, hy, 0, EAVE), box(hx - WALL, hx, -hy, hy, 0, EAVE)]   # end walls
ix0 = -hx + WALL
STALL = (L - 2 * WALL) / 6                                                                # 11.7 ft inside the model walls
xs = [ix0 + STALL * (k + .5) for k in range(6)]
south_x = [ix0 + STALL * k for k in (1, 2, 3)]                                           # wash | tack | feed | alfalfa (3 stalls wide)
south_c = [ix0 + STALL * .5, ix0 + STALL * 1.5, ix0 + STALL * 2.5, ix0 + STALL * 4.5]
for k in range(1, 6):                                                                      # north stall dividers
    x = ix0 + STALL * k
    solid.append(box(x - T / 2, x + T / 2, AISLE / 2, hy - WALL, 0, PART_H))
for x in south_x:                                                                          # south room walls
    solid.append(box(x - T / 2, x + T / 2, -hy + WALL, -AISLE / 2, 0, ROOM_H))
solid.append(box(ix0, -ix0, AISLE / 2 - T, AISLE / 2, 0, PART_H))                        # north stall fronts
solid.append(box(ix0, -ix0, -AISLE / 2, -AISLE / 2 + T, 0, ROOM_H))                      # south room fronts, taller
body = U(solid)
cuts = []
g = 0.3 / MM_PER_FT
cuts += [box(-hx - 1, hx + 1, -hy - 1, -hy + g, STONE - .35, STONE + .35), box(-hx - 1, hx + 1, hy - g, hy + 1, STONE - .35, STONE + .35),
         box(-hx - 1, -hx + g, -hy - 1, hy + 1, STONE - .35, STONE + .35), box(hx - g, hx + 1, -hy - 1, hy + 1, STONE - .35, STONE + .35)]
for sx in (-1, 1):                                                                         # the big gable entries, full wall height
    cuts.append(box(sx * hx - WALL - 1, sx * hx + WALL + 1, -ENTRY / 2, ENTRY / 2, FLOOR_B, EAVE + 1))
for x in xs:
    cuts.append(box(x - 2, x + 2, hy - WALL - 1, hy + 1, FLOOR_B, 8))                     # north stall doors to the runs
    cuts.append(box(x - 2, x + 2, AISLE / 2 - T - 1, AISLE / 2 + 1, FLOOR_B, 8))          # north stall doors to the aisle
for x in south_c:
    cuts.append(box(x - 2, x + 2, -AISLE / 2 - 1, -AISLE / 2 + T + 1, FLOOR_B, 8))        # south doors to the aisle
    cuts.append(box(x - 2, x + 2, -hy - 1, -hy + WALL + 1, FLOOR_B, 8))                   # south doors out
body = Dff(body, cuts)

# ---------- 5/6 trusses: flat on the bed; gable ends solid, middle two open-web ----------
TR_T = NOZ_FT                                       # truss thickness (printed height)
CH = 0.8 / MM_PER_FT                                 # chord and web width
def truss(solid_gable):
    pts = [(-hy, 0), (hy, 0), (0, RIDGE - EAVE)]
    Poly = trimesh.path.polygons.Polygon
    tri_p = Poly(pts); band = tri_p.difference(tri_p.buffer(-CH))            # perimeter band: both rafters + eave chord
    if solid_gable:                                                           # solid over the rooms, open over the entry, band all round
        m = creation.extrude_polygon(tri_p.difference(Poly([(-ENTRY / 2, -1), (ENTRY / 2, -1), (ENTRY / 2, RIDGE), (-ENTRY / 2, RIDGE)]).intersection(tri_p.buffer(-CH))), TR_T)
    else:
        parts = [box(-hy, hy, 0, CH, 0, TR_T)]
        for sgn in (-1, 1):
            ang_ = math.atan2(RIDGE - EAVE, hy); ln = math.hypot(hy, RIDGE - EAVE)
            c = creation.box(extents=[ln, CH, TR_T]); c.apply_translation([ln / 2, -CH / 2, TR_T / 2])
            c.apply_transform(trimesh.transformations.rotation_matrix(sgn * 0 + (math.pi - ang_ if sgn < 0 else ang_), [0, 0, 1]))
            c.apply_translation([sgn * -hy if False else (-hy if sgn > 0 else hy), 0, 0]); parts.append(c)
        for f in (-2 / 3, -1 / 3, 0, 1 / 3, 2 / 3):          # verticals
            x = f * hy; top = (RIDGE - EAVE) * (1 - abs(x) / hy)
            parts.append(box(x - CH / 2, x + CH / 2, 0, max(top, CH), 0, TR_T))
        for f0, f1 in ((-2 / 3, -1 / 3), (-1 / 3, 0), (1 / 3, 0), (2 / 3, 1 / 3)):   # diagonals
            xa, xb = f0 * hy, f1 * hy; ya, yb = 0, (RIDGE - EAVE) * (1 - abs(xb) / hy)
            ln = math.hypot(xb - xa, yb - ya); c = creation.box(extents=[ln, CH, TR_T]); c.apply_translation([ln / 2, 0, TR_T / 2])
            c.apply_transform(trimesh.transformations.rotation_matrix(math.atan2(yb - ya, xb - xa), [0, 0, 1])); c.apply_translation([xa, ya, 0]); parts.append(c)
        m = U(parts)
        m = boolean.intersection([m, creation.extrude_polygon(tri_p, TR_T)], engine='manifold')
        m = U([m, creation.extrude_polygon(band, TR_T)])
    # locating tabs that drop just inside the long walls, so the lid can't slide sideways
    tab = 0.9 / MM_PER_FT
    tabs = [box(sx * (hy - WALL) - (tab if sx > 0 else 0), sx * (hy - WALL) + (0 if sx > 0 else tab), -tab, 0, 0, TR_T) for sx in (-1, 1)]
    return U([m] + tabs)
gable, mid = truss(True), truss(False)

# ---------- 2 roof panel (print flat, x2) ----------
run = D / 2 + OVER; rise = (RIDGE - EAVE) * run / (D / 2)
slope_len = math.hypot(run, rise)
panel = box(0, L + 1, 0, slope_len, 0, NOZ_FT)          # 0.5 ft past the end frames; overhang on the long side only

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

north = runs(6)

def save(m, name):
    m = m.copy(); m.apply_scale(MM_PER_FT)
    b = m.bounds; m.apply_translation([-b[0][0], -b[0][1], -b[0][2]])    # sit on the bed at the origin
    fn = os.path.join(OUT, name); m.export(fn)
    ext = m.extents
    print(f'{name:28s} {ext[0]:6.1f} x {ext[1]:5.1f} x {ext[2]:5.1f} mm  watertight={m.is_watertight}  tris={len(m.faces)}')
    return m

pb = save(body, '1-body-open.stl')
save(gable, '5-truss-gable-end-print-2.stl')
save(mid, '6-truss-middle-print-2.stl')
save(panel, '2-roof-panel-print-2.stl')
save(north, '3-runs-north-6.stl')

# ---------- exploded preview: lid lifted off ----------
LIFT = 24.0
roofA = panel.copy(); ang = math.atan2(rise, run)
roofA.apply_translation([-(L + 1) / 2, -slope_len, 0]); roofA.apply_transform(trimesh.transformations.rotation_matrix(ang, [1, 0, 0])); roofA.apply_translation([0, 0, RIDGE + LIFT])
roofB = roofA.copy(); roofB.apply_transform(trimesh.transformations.rotation_matrix(math.pi, [0, 0, 1]))
trs = []
for x, tm in ((-hx + WALL + TR_T, gable), (-12, mid), (12, mid), (hx - WALL, gable)):
    t = tm.copy(); v = t.vertices.copy(); t.vertices = np.column_stack([v[:, 2], v[:, 0], v[:, 1]])   # thickness->x, span->y, height->z
    t.apply_translation([x, 0, EAVE + LIFT]); trs.append(t)
nr = north.copy(); nr.apply_translation([ix0, D / 2, 0])
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
fig = plt.figure(figsize=(10, 7), dpi=130); ax = fig.add_subplot(111, projection='3d')
tris, fcs = [], []
for m, c in [(body, '#b9ad97'), (roofA, '#6fa8d8'), (roofB, '#5d95c2'), (nr, '#c9b48f')] + [(t, '#6f7d86') for t in trs]:
    mm = m.copy(); mm.apply_scale(MM_PER_FT)
    shade = 0.5 + 0.5 * np.clip(mm.face_normals @ np.array([-.4, -.5, .77]), 0, 1)
    base = np.array(matplotlib.colors.to_rgb(c))
    tris.append(mm.triangles); fcs.append(np.clip(base[None, :] * shade[:, None], 0, 1))
pc = Poly3DCollection(np.concatenate(tris), facecolors=np.concatenate(fcs), edgecolor='none'); ax.add_collection3d(pc)
ax.set_xlim(-32, 32); ax.set_ylim(-32, 32); ax.set_zlim(0, 34); ax.set_box_aspect((64, 64, 34)); ax.view_init(38, -60); ax.axis('off')
ax.set_title('Stable at 1:480 · roof lid lifted: 2 panels + 4 trusses · stalls inside', fontsize=10)
fig.savefig(os.path.join(OUT, 'assembled-preview.png'), bbox_inches='tight')

# ---------- plan of the stall layout (body only, from above) ----------
fig, ax = plt.subplots(figsize=(9, 6), dpi=130)
mm = body.copy()
sl = mm.section(plane_origin=[0, 0, 4.0], plane_normal=[0, 0, 1])
p2, _ = sl.to_planar(to_2D=np.eye(4))
for poly in p2.polygons_full:
    xs_, ys_ = poly.exterior.xy; ax.fill(xs_, ys_, color='#8c8374')
    for h in poly.interiors: xs_, ys_ = h.xy; ax.fill(xs_, ys_, color='white')
NL = chr(10)
south_lbl = ['lavado' + NL + 'wash', 'montura' + NL + 'tack', 'alimento' + NL + 'feed', 'alfalfa' + NL + 'storage']
for k, x in enumerate(xs):
    ax.text(x, (AISLE / 2 + hy - WALL) / 2, 'caballeriza' + NL + 'stall', ha='center', va='center', fontsize=7)
for k, x in enumerate(south_c):
    ax.text(x, -(AISLE / 2 + hy - WALL) / 2, south_lbl[k], ha='center', va='center', fontsize=7)
ax.text(0, 0, 'pasillo · aisle 14 ft', ha='center', va='center', fontsize=9, color='#555')
ax.set_aspect('equal'); ax.axis('off'); ax.set_title('Body cut at 4 ft: 6 stalls north; wash, tack, feed, alfalfa south; 14 ft aisle; open gable entries · N at top', fontsize=10)
fig.savefig(os.path.join(OUT, 'body-plan.png'), bbox_inches='tight')
