"""Will's parked tractor trailer as an OBJ for the topo tool: a 40 x 8 ft box van with its
deck 4 ft off the ground, on wheels at the back and landing legs at the front. Feet, z up,
x along the trailer. No # geo line, so it imports at the middle of the site and is dragged
into place; turn it with select.

    python trailer-8x40.py   ->  trailer-8x40.obj
"""
import math, os

LEN, WID = 40.0, 8.0     # the box, as Will measured it
DECK = 4.0               # underside of the deck above the ground
BOX_H = 9.0              # box side height, from the photo: roof about 13 ft up
FRAME = 0.5              # the deck itself
WHEEL_R, WHEEL_W = 1.7, 0.85
AXLES = [-0.30, -0.44]   # axle centres, as a fraction of the length from the middle (rear pair)
LEG_X = 0.30             # landing legs, fraction of the length forward of the middle

V, F = [], []

def box(x0, x1, y0, y1, z0, z1):
    i = len(V) + 1
    for z in (z0, z1):
        for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)): V.append((x, y, z))
    for f in ((0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)):
        F.append(tuple(i + k for k in f))

def wheel(cx, cy, r, w, n=12):
    """A tyre as an n-sided drum, lying on the y axis."""
    i = len(V) + 1
    for y in (cy - w / 2, cy + w / 2):
        for k in range(n):
            a = 2 * math.pi * k / n
            V.append((cx + r * math.cos(a), y, r + r * math.sin(a)))
    for k in range(n):                       # tread
        a, b = k, (k + 1) % n
        F.append((i + a, i + b, i + n + b, i + n + a))
    F.append(tuple(i + k for k in range(n)))             # the two sides
    F.append(tuple(i + n + k for k in range(n - 1, -1, -1)))

hl, hw = LEN / 2, WID / 2
box(-hl, hl, -hw, hw, DECK, DECK + BOX_H)            # the box
box(-hl, hl, -hw + .1, hw - .1, DECK - FRAME, DECK)  # the deck under it
box(-hl + 1, hl - 1, -.35, .35, DECK - FRAME - .55, DECK - FRAME)   # the centre beam

for fx in AXLES:                                     # rear wheels, one pair each side
    x = fx * LEN
    for sy in (-1, 1):
        wheel(x, sy * (hw - 1.1), WHEEL_R, WHEEL_W)
    box(x - .3, x + .3, -hw + .8, hw - .8, WHEEL_R - .25, WHEEL_R + .25)   # the axle

for sy in (-1, 1):                                   # landing legs and their feet
    box(LEG_X * LEN - .25, LEG_X * LEN + .25, sy * 1.8 - .25, sy * 1.8 + .25, 0, DECK - FRAME)
    box(LEG_X * LEN - .8, LEG_X * LEN + .8, sy * 1.8 - .7, sy * 1.8 + .7, 0, .25)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'trailer-8x40.obj')
with open(out, 'w', newline='\n') as f:
    f.write('# tractor trailer, %g x %g ft box, deck %g ft off the ground, roof at %g ft\n' % (LEN, WID, DECK, DECK + BOX_H))
    f.write('# unit ft\n# name trailer 8 x 40\n')
    for v in V: f.write('v %.3f %.3f %.3f\n' % v)
    for fc in F: f.write('f ' + ' '.join(map(str, fc)) + '\n')
print(out, len(V), 'verts', len(F), 'faces')
