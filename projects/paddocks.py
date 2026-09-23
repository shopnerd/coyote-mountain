"""Will's blue rectangle divided into four paddocks, each with its own covered stall.

Pipe fence around the rectangle and three cross fences; in every paddock a three-sided shelter
open to the paddock. Feet, z up, turned to the rectangle's own bearing, with a # geo line so
topo.html drops it on the rectangle's centre.

    python paddocks.py   ->  paddocks.obj
"""
import math, os

CENTRE = (31.9989880, -116.7642460)
BEARING = 49.35                  # the rectangle's long axis, degrees from north
L, D = 270.0, 75.0               # as he drew it
BAYS = 4
STALL_W, STALL_D, STALL_H = 12.0, 16.0, 8.5      # the covered stall in each paddock
ROOF_RISE, ROOF_OVER, ROOF_T = 1.8, 1.0, 0.3     # a shed roof, falling to the front
POST, RAIL_T, RAIL_H = 0.5, 0.2, 5.0
RAILS = (1.6, 3.0, 4.4)
SPACING = 10.0                   # fence posts

V, F = [], []
rot = math.radians(90 - BEARING)
C, S = math.cos(rot), math.sin(rot)
world = lambda x, y, z: (x * C - y * S, x * S + y * C, z)

def box(x0, x1, y0, y1, z0, z1):
    if min(x1 - x0, y1 - y0, z1 - z0) <= 0: return
    i = len(V) + 1
    for z in (z0, z1):
        for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)): V.append(world(x, y, z))
    for f in ((0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)):
        F.append(tuple(i + k for k in f))

def quad(a, b, c, d):
    i = len(V) + 1
    for p in (a, b, c, d): V.append(world(*p))
    F.append((i, i + 1, i + 2, i + 3))

def fence_line(x0, y0, x1, y1):
    """Posts and three rails from one point to another."""
    n = max(1, int(round(math.dist((x0, y0), (x1, y1)) / SPACING)))
    for k in range(n + 1):
        t = k / n
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        box(x - POST / 2, x + POST / 2, y - POST / 2, y + POST / 2, 0, RAIL_H)
    for h in RAILS:
        if abs(y1 - y0) < 1e-6:
            box(min(x0, x1), max(x0, x1), y0 - RAIL_T / 2, y0 + RAIL_T / 2, h - RAIL_T / 2, h + RAIL_T / 2)
        else:
            box(x0 - RAIL_T / 2, x0 + RAIL_T / 2, min(y0, y1), max(y0, y1), h - RAIL_T / 2, h + RAIL_T / 2)

HL, HD = L / 2, D / 2
# the rectangle and the three cross fences
fence_line(-HL, -HD, HL, -HD)
fence_line(-HL, HD, HL, HD)
fence_line(-HL, -HD, -HL, HD)
fence_line(HL, -HD, HL, HD)
for k in range(1, BAYS):
    x = -HL + k * (L / BAYS)
    fence_line(x, -HD, x, HD)

# one shelter per paddock, against the back fence, open to the paddock
for k in range(BAYS):
    cx = -HL + (k + 0.5) * (L / BAYS)
    x0, x1 = cx - STALL_W / 2, cx + STALL_W / 2
    y1 = HD - 1.0                      # its back wall stands just inside the back fence
    y0 = y1 - STALL_D
    box(x0, x1, y0, y1, 0, .3)                                   # floor slab
    box(x0, x1, y1 - .4, y1, .3, STALL_H)                        # back wall
    box(x0, x0 + .4, y0, y1, .3, STALL_H)                        # two side walls
    box(x1 - .4, x1, y0, y1, .3, STALL_H)
    for x in (x0 + .25, x1 - .25):                               # front posts
        box(x - .3, x + .3, y0, y0 + .5, .3, STALL_H + ROOF_RISE)
    for z in (0, ROOF_T):                                        # shed roof, high at the back
        quad((x0 - ROOF_OVER, y0 - ROOF_OVER, STALL_H + z),
             (x1 + ROOF_OVER, y0 - ROOF_OVER, STALL_H + z),
             (x1 + ROOF_OVER, y1 + ROOF_OVER, STALL_H + ROOF_RISE + z),
             (x0 - ROOF_OVER, y1 + ROOF_OVER, STALL_H + ROOF_RISE + z))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'paddocks.obj')
bay_w = L / BAYS
with open(out, 'w', newline='\n') as f:
    f.write('# four paddocks in the %g x %g ft rectangle: each %g x %g ft with one %g x %g ft covered stall, pipe fence at %g ft\n'
            % (L, D, bay_w, D, STALL_W, STALL_D, RAIL_H))
    f.write('# geo %.7f %.7f\n# unit ft\n# name four paddocks\n' % CENTRE)
    for v in V: f.write('v %.3f %.3f %.3f\n' % v)
    for fc in F: f.write('f ' + ' '.join(map(str, fc)) + '\n')
print(out, len(V), 'verts', len(F), 'faces')
print('each paddock %.1f x %.1f ft = %.2f acre, stall %g x %g ft' % (bay_w, D, bay_w * D / 43560, STALL_W, STALL_D))
