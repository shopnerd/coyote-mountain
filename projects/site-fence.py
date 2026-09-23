"""The fences Will marked: the whole-site boundary (his red loop) and the interior fence line
(his red dashed line). Posts every 20 ft with three wires, in feet, x east, y north, anchored by
a # geo line so topo.html drops each one on its own centre.

    python site-fence.py   ->  site-fence.obj, cross-fence.obj
"""
import math, os

POST_H, POST_W, SPACING = 4.5, 0.3, 20.0
WIRES, WIRE_T = (1.5, 3.0, 4.3), 0.12

SITE = [                                   # his red loop, corner to corner, already closed
    (31.999563, -116.765630), (32.001186, -116.763654), (32.000503, -116.762971),
    (32.000930, -116.762395), (32.000879, -116.762344), (32.000434, -116.762678),
    (31.999619, -116.763552), (31.998942, -116.763839), (31.998470, -116.764456),
]
CROSS = [(32.000270, -116.764745), (31.999281, -116.763705)]   # the dashed line

FT = 0.3048


def local(pts):
    """lat/lon -> feet east/north from the centre of the run, plus that centre."""
    la0 = sum(p[0] for p in pts) / len(pts)
    lo0 = sum(p[1] for p in pts) / len(pts)
    kx = 111320 * math.cos(math.radians(la0)) / FT
    ky = 111320 / FT
    return [((p[1] - lo0) * kx, (p[0] - la0) * ky) for p in pts], (la0, lo0)


def stations(pts, closed, spacing):
    """Even stations along a run, and its length."""
    line = pts + [pts[0]] if closed else pts
    segs = [math.dist(line[i], line[i + 1]) for i in range(len(line) - 1)]
    total = sum(segs)
    n = max(2, int(round(total / spacing)))
    step = total / n
    out, target, acc, i = [], 0.0, 0.0, 0
    count = n if closed else n + 1
    for _ in range(count):
        while i < len(segs) and acc + segs[i] < target:
            acc += segs[i]; i += 1
        if i >= len(segs):
            out.append(line[-1]); break
        t = (target - acc) / segs[i]
        a, b = line[i], line[i + 1]
        out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
        target += step
    return out, total


class Mesh:
    def __init__(self): self.V, self.F = [], []

    def box(self, cx, cy, z0, z1, along, w, length):
        ax, ay = along
        px, py = -ay, ax
        i = len(self.V) + 1
        for z in (z0, z1):
            for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
                self.V.append((cx + ax * length / 2 * sx + px * w / 2 * sy,
                               cy + ay * length / 2 * sx + py * w / 2 * sy, z))
        for f in ((0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)):
            self.F.append(tuple(i + k for k in f))

    def write(self, path, header, lat, lon, name):
        with open(path, 'w', newline='\n') as f:
            f.write('# %s\n# geo %.7f %.7f\n# unit ft\n# name %s\n' % (header, lat, lon, name))
            for v in self.V: f.write('v %.3f %.3f %.3f\n' % v)
            for fc in self.F: f.write('f ' + ' '.join(map(str, fc)) + '\n')


def fence(pts_ll, closed, out_path, header, name):
    pts, centre = local(pts_ll)
    st, total = stations(pts, closed, SPACING)
    m = Mesh()
    for x, y in st:
        m.box(x, y, 0, POST_H, (1.0, 0.0), POST_W, POST_W)
    n = len(st)
    spans = n if closed else n - 1
    for k in range(spans):
        a, b = st[k], st[(k + 1) % n]
        L = math.dist(a, b)
        if L < 0.5: continue
        along = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
        for h in WIRES:
            m.box((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, h - WIRE_T / 2, h + WIRE_T / 2, along, WIRE_T, L)
    m.write(out_path, header % total, centre[0], centre[1], name)
    return total, len(m.F), len(st)


here = os.path.dirname(os.path.abspath(__file__))
a = fence(SITE, True, os.path.join(here, 'site-fence.obj'),
          'site boundary fence, %.0f ft around, posts every 20 ft with three wires at 4 ft 6 in', 'site fence')
b = fence(CROSS, False, os.path.join(here, 'cross-fence.obj'),
          'interior fence line, %.0f ft long, posts every 20 ft with three wires at 4 ft 6 in', 'cross fence')
print('site  %.0f ft · %d posts · %d faces' % (a[0], a[2], a[1]))
print('cross %.0f ft · %d posts · %d faces' % (b[0], b[2], b[1]))
