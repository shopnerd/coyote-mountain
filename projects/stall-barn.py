"""The covered stalls Will marked with the small blue rectangle: two rows facing each other
across a covered aisle, with a run off every stall. Feet, z up, x along the rows, turned to the
rectangle's own bearing, with a # geo line so topo.html drops it on the rectangle's centre.

    python stall-barn.py   ->  stall-barn.obj
"""
import math, os

CENTRE = (31.9989880, -116.7642460)   # the middle of his rectangle
BEARING = 49.35                       # its long axis, degrees from north
PER_SIDE = 14                         # stalls each side; 28 in all
STALL = 12.0                          # square stalls
AISLE = 14.0                          # covered aisle between the rows
RUN = 20.0                            # run off each stall, out the back
EAVE, RIDGE = 10.0, 14.5              # roof over stalls and aisle
POST, PANEL = 0.67, 4.5               # posts 8 in square; stall panels 4 ft 6 in
RAILS, RAIL_T, RAIL_H = (1.8, 3.4, 5.0), 0.2, 5.0

L = PER_SIDE * STALL                  # 168 ft of roof
D = 2 * STALL + AISLE                 # 38 ft deep
HL, HD = L / 2, D / 2

V, F = [], []
rot = math.radians(90 - BEARING)
C, Sn = math.cos(rot), math.sin(rot)
world = lambda x, y, z: (x * C - y * Sn, x * Sn + y * C, z)

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

# posts: down both outer walls and both sides of the aisle, at every stall line
for k in range(PER_SIDE + 1):
    x = -HL + k * STALL
    for y in (-HD, -AISLE / 2, AISLE / 2, HD):
        box(x - POST / 2, x + POST / 2, y - POST / 2, y + POST / 2, 0, EAVE)

# stall floors and their dividers, both rows
for sy in (-1, 1):
    y0, y1 = sy * AISLE / 2, sy * HD
    lo, hi = min(y0, y1), max(y0, y1)
    box(-HL, HL, lo, hi, 0, .3)                                   # the stall floor slab
    for k in range(PER_SIDE + 1):
        x = -HL + k * STALL
        box(x - .25, x + .25, lo + .3, hi - .3, .3, PANEL)        # divider between stalls
    box(-HL, HL, sy * HD - sy * .3, sy * HD, .3, PANEL + 1.5)     # back wall of the row

# the aisle floor
box(-HL, HL, -AISLE / 2, AISLE / 2, 0, .25)

# roof: a gable over the whole width, 1 ft overhang, thin slabs so it reads from below
T, OVER = .35, 1.0
for sy in (-1, 1):
    for z in (0, T):
        quad((-HL - OVER, sy * (HD + OVER), EAVE + z), (HL + OVER, sy * (HD + OVER), EAVE + z),
             (HL + OVER, 0, RIDGE + z), (-HL - OVER, 0, RIDGE + z))
box(-HL - OVER, HL + OVER, -.35, .35, RIDGE, RIDGE + .45)          # ridge cap

# runs: one off every stall, out the back of each row, three-rail pipe
for sy in (-1, 1):
    y0 = sy * HD
    y1 = sy * (HD + RUN)
    for k in range(PER_SIDE + 1):
        x = -HL + k * STALL
        for h in RAILS:
            box(x - RAIL_T / 2, x + RAIL_T / 2, min(y0, y1), max(y0, y1), h - RAIL_T / 2, h + RAIL_T / 2)
        box(x - .3, x + .3, y1 - sy * .3 if sy > 0 else y1 + .3, y1 if sy > 0 else y1 - .0, 0, RAIL_H)
    for h in RAILS:                                                # the fence across the far end
        box(-HL, HL, min(y1, y1 - sy * RAIL_T), max(y1, y1 - sy * RAIL_T) + RAIL_T, h - RAIL_T / 2, h + RAIL_T / 2)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stall-barn.obj')
with open(out, 'w', newline='\n') as f:
    f.write('# covered stalls: %d stalls, two rows of %d facing across a %g ft aisle, %g x %g ft of roof, %g ft runs off every stall\n'
            % (PER_SIDE * 2, PER_SIDE, AISLE, L, D, RUN))
    f.write('# geo %.7f %.7f\n# unit ft\n# name covered stalls %d\n' % (CENTRE[0], CENTRE[1], PER_SIDE * 2))
    for v in V: f.write('v %.3f %.3f %.3f\n' % v)
    for fc in F: f.write('f ' + ' '.join(map(str, fc)) + '\n')
print(out, len(V), 'verts', len(F), 'faces', f'roof {L} x {D} ft, {PER_SIDE*2} stalls, runs {RUN} ft')
