"""Three-rail pipe fence around the arena and the round pen, to match the barn's runs
(5 ft 6 in posts, three rails). Feet, z up, x east, y north, bearings baked in, and a
# geo line so topo.html drops each one on its own centre.

    python pipe-fence.py   ->  arena-fence.obj, roundpen-fence.obj
"""
import math, os

POST_H, POST_W, SPACING = 5.5, 0.35, 8.0     # as the barn's runs: 5 ft 6 in, three rails
RAILS, RAIL_T = (1.8, 3.6, 5.3), 0.22
ARENA = dict(lat=32.0003093, lon=-116.7640215, length=182.3, width=78.1, bearing=45.01, gate=12.0)
PEN = dict(lat=31.9999996, lon=-116.7638056, diameter=60.4, gate=10.0)


def loop_stadium(length, width, step=1.0):
    """Centreline of a stadium: two straights with a half circle at each end."""
    r = width / 2.0
    s = max(0.0, length / 2.0 - r)
    pts, n = [], max(8, int(math.pi * r / step))
    for k in range(n + 1):                     # east end, -90 to +90
        a = -math.pi / 2 + math.pi * k / n
        pts.append((s + r * math.cos(a), r * math.sin(a)))
    for k in range(n + 1):                     # west end
        a = math.pi / 2 + math.pi * k / n
        pts.append((-s + r * math.cos(a), r * math.sin(a)))
    return pts


def loop_circle(diameter, step=1.0):
    r = diameter / 2.0
    n = max(16, int(2 * math.pi * r / step))
    return [(r * math.cos(2 * math.pi * k / n), r * math.sin(2 * math.pi * k / n)) for k in range(n)]


def resample(loop, spacing):
    """Even stations around a closed loop, and its total length."""
    pts = loop + [loop[0]]
    segs = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    total = sum(segs)
    n = max(4, round(total / spacing))
    step = total / n
    out, d_target, acc, i = [], 0.0, 0.0, 0
    for _ in range(n):
        while i < len(segs) and acc + segs[i] < d_target:
            acc += segs[i]; i += 1
        if i >= len(segs): break
        t = (d_target - acc) / segs[i]
        a, b = pts[i], pts[i + 1]
        out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
        d_target += step
    return out, total


class Mesh:
    def __init__(self, bearing):
        self.V, self.F = [], []
        r = math.radians(90 - bearing)         # x along the long axis -> east/north
        self.c, self.s = math.cos(r), math.sin(r)

    def world(self, x, y, z):
        return (x * self.c - y * self.s, x * self.s + y * self.c, z)

    def box(self, cx, cy, z0, z1, along, w, length):
        """A box centred on cx,cy: `length` along the unit vector `along`, `w` across."""
        ax, ay = along
        px, py = -ay, ax
        i = len(self.V) + 1
        for z in (z0, z1):
            for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
                self.V.append(self.world(cx + ax * length / 2 * sx + px * w / 2 * sy,
                                         cy + ay * length / 2 * sx + py * w / 2 * sy, z))
        for f in ((0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)):
            self.F.append(tuple(i + k for k in f))

    def write(self, path, header, lat, lon, name):
        with open(path, 'w', newline='\n') as f:
            f.write('# %s\n# geo %.7f %.7f\n# unit ft\n# name %s\n' % (header, lat, lon, name))
            for v in self.V: f.write('v %.3f %.3f %.3f\n' % v)
            for fc in self.F: f.write('f ' + ' '.join(map(str, fc)) + '\n')


def fence(loop, spec, gate, out_path, header, name):
    """Posts at even stations with three rails between them; one station left open as the gate."""
    stations, total = resample(loop, SPACING)
    m = Mesh(spec.get('bearing', 0.0))
    n = len(stations)
    skip = n // 2                              # the gate bay: the middle station of the run
    for k, (x, y) in enumerate(stations):
        if k == skip: continue                 # no post inside the gate opening
        m.box(x, y, 0, POST_H, (1.0, 0.0), POST_W, POST_W)
    for k in range(n):
        a, b = stations[k], stations[(k + 1) % n]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy)
        if k == skip or k == skip - 1:          # leave the gate bay open
            continue
        along = (dx / L, dy / L)
        for h in RAILS:
            m.box((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, h - RAIL_T / 2, h + RAIL_T / 2, along, RAIL_T, L)
    m.write(out_path, header % (total, gate), spec['lat'], spec['lon'], name)
    return total, len(m.F)


here = os.path.dirname(os.path.abspath(__file__))
a_len, a_f = fence(loop_stadium(ARENA['length'], ARENA['width']), ARENA, ARENA['gate'],
                   os.path.join(here, 'arena-fence.obj'),
                   'arena pipe fence, three rails at 5 ft 6 in, %.0f ft around, one %.0f ft gate bay', 'arena fence')
p_len, p_f = fence(loop_circle(PEN['diameter']), PEN, PEN['gate'],
                   os.path.join(here, 'roundpen-fence.obj'),
                   'round pen pipe fence, three rails at 5 ft 6 in, %.0f ft around, one %.0f ft gate bay', 'round pen fence')
print('arena  %.0f ft around, %d faces' % (a_len, a_f))
print('pen    %.0f ft around, %d faces' % (p_len, p_f))
