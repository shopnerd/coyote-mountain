# 4 Oct (Will): architectural drawings as LINE WORK on the paper, no tone fills. Real-life sticks (wavy, uneven, cut to one length,
# stacked in steel frames), stones drawn as outlines in courses, plank doors, hatched ground. Shared by the stable elevations and
# the structure page. Units are feet in a data-aspect-equal axes.
import math, random as _rnd, numpy as _np
from matplotlib.patches import Polygon as _LPoly
LW_INK = '#2a2824'; LW_STICK = '#4d3f30'
def lw_line(ax, xs, ys, lw=.8, color=LW_INK, **k): ax.plot(xs, ys, color=color, lw=lw, solid_capstyle='round', solid_joinstyle='round', **k)
def lw_box(ax, x0, y0, x1, y1, lw=.8, color=LW_INK): lw_line(ax, [x0, x1, x1, x0, x0], [y0, y0, y1, y1, y0], lw=lw, color=color)

def lw_sticks(ax, x0, x1, z0, z1, rng, gap=.19, lw=(.35, .8), amp=.045, frame=True, frame_lw=1.0, outline=False, dia=(.15, .22)):
    """horizontal natural sticks in a frame: each one wavy, slightly bowed, its own thickness; ends tucked into the frame"""
    if frame == 'sides': lw_line(ax, [x0, x0], [z0, z1], lw=frame_lw); lw_line(ax, [x1, x1], [z0, z1], lw=frame_lw)   # 4 Oct (Will): fixed verticals only
    elif frame: lw_box(ax, x0, z0, x1, z1, lw=frame_lw)
    z = z0 + gap * .7
    while z < z1 - gap * .4:
        n = 14; xs = _np.linspace(x0 + .03, x1 - .03, n)
        ph, ph2 = rng.uniform(0, 6.3), rng.uniform(0, 6.3); bow = rng.uniform(-amp, amp) * 1.4
        ys = z + amp * _np.sin(xs * rng.uniform(1.3, 2.6) + ph) * .6 + amp * _np.sin(xs * rng.uniform(3.5, 6) + ph2) * .35 \
               + bow * _np.sin(_np.pi * (xs - x0) / max(x1 - x0, 1e-6))
        ys = _np.clip(ys, z0 + .02, z1 - .02)
        w = rng.uniform(*lw)
        if outline:                                                              # a real stick: two edges, tapering, its ends cut
            n2 = 40; xx = _np.linspace(x0 + .03, x1 - .03, n2); yc = _np.interp(xx, xs, ys)
            d0, d1 = rng.uniform(*dia), rng.uniform(*dia); r = (d0 + (d1 - d0) * (xx - x0) / max(x1 - x0, 1e-6)) / 2
            r = r * (1 + .12 * _np.sin(xx * rng.uniform(4, 9) + rng.uniform(0, 6)))
            top, bot = _np.minimum(yc + r, z1 - .015), _np.maximum(yc - r, z0 + .015)
            _bg = globals().get('PAPER', '#faf8f3')
            ax.add_patch(_LPoly(_np.r_[_np.c_[xx, top], _np.c_[xx[::-1], bot[::-1]]], closed=True, fc=_bg, ec=LW_STICK, lw=w, joinstyle='round', zorder=2 + rng.random()))   # paper-filled: sticks in front hide the ones behind
            for _ in range(1 if rng.random() < .35 else 0):                           # an occasional knot
                kx = rng.uniform(x0 + .2, x1 - .2); ky = _np.interp(kx, xx, yc); kr = _np.interp(kx, xx, r) * .45
                t = _np.linspace(0, 2 * _np.pi, 10); ax.plot(kx + kr * 1.6 * _np.cos(t), ky + kr * _np.sin(t), color=LW_STICK, lw=w * .5, zorder=3.5)
            z += gap * rng.uniform(.9, 1.12); continue
        lw_line(ax, xs, ys, lw=w, color=LW_STICK)
        if rng.random() < .18:                                                     # a knot or side-twig stub
            kx = rng.uniform(x0 + .2, x1 - .2); ky = _np.interp(kx, xs, ys); lw_line(ax, [kx, kx + rng.uniform(.05, .14)], [ky, ky + rng.uniform(.03, .08)], lw=w * .7, color=LW_STICK)
        z += gap * rng.uniform(.85, 1.15)

def _stone(ax, cx, cy, rx, ry, rng, lw, clip):
    """one site stone, like the tabular blocks stacked on site: a rough rectangle (flat beds, slightly sloped top and bottom), chipped
    corners, edges a little uneven; one light rounding pass"""
    tilt = rng.uniform(-.14, .14) * ry
    pts = []
    for (sx, sy) in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        ch = rng.uniform(.12, .55) * min(rx, ry * 1.4)                         # chip the corner
        x, y = cx + sx * rx * rng.uniform(.9, 1.0), cy + sy * ry * rng.uniform(.82, 1.0) + sx * tilt
        if sy < 0: pts += [(x, y + ch * (1 if sx < 0 else 0)), (x - sx * ch, y)] if sx < 0 else [(x - sx * ch, y), (x, y + ch)]
        else: pts += [(x, y - ch), (x - sx * ch, y)] if sx > 0 else [(x - sx * ch, y), (x, y - ch)]
    P = []                                                                    # uneven edges: a mid point nudged on each side
    for a_, b_ in zip(pts, pts[1:] + pts[:1]):
        P.append(a_); m = ((a_[0] + b_[0]) / 2, (a_[1] + b_[1]) / 2)
        L = math.hypot(b_[0] - a_[0], b_[1] - a_[1])
        if L > .25: nx_, ny_ = -(b_[1] - a_[1]) / L, (b_[0] - a_[0]) / L; d = rng.uniform(-.13, .1) * min(rx, ry) * 2; P.append((m[0] + nx_ * d, m[1] + ny_ * d))
    P = _np.array(P)
    Q = []
    for a_, b_ in zip(P, _np.roll(P, -1, axis=0)): Q += [.9 * a_ + .1 * b_, .1 * a_ + .9 * b_]
    P = _np.array(Q)
    x0, z0, x1, z1 = clip; P[:, 0] = _np.clip(P[:, 0], x0, x1); P[:, 1] = _np.clip(P[:, 1], z0, z1)
    ax.add_patch(_LPoly(P, closed=True, fill=False, ec=LW_INK, lw=lw * rng.uniform(.85, 1.2), joinstyle='round'))
    if rng.random() < .25:                                                    # a bedding line or crack across the face
        yy = cy + rng.uniform(-.3, .3) * ry; a = cx - rx * rng.uniform(.2, .8); b = a + rx * rng.uniform(.4, .9)
        lw_line(ax, [a, b], [yy, yy + rng.uniform(-.05, .05) * ry], lw=lw * .45)

def lw_stones(ax, x0, x1, z0, z1, rng, big=1.35, small=.5, lw=.6, course=None, length=None):
    """a dry-laid wall of stones from the site: irregular sizes and shapes, the big ones low, smaller toward the top, some gaps and
    chinking stones. course/length kept for old callers (troughs): they just shrink the stones."""
    if course: big = small = sum(course) / 2
    clip = (x0, z0, x1, z1); z = z0
    while z < z1 - .12:
        t = (z - z0) / max(z1 - z0, 1e-6); sc = big * (1 - t) + small * t
        h = min(sc * rng.uniform(.5, .85), z1 - z)
        x = x0 - rng.uniform(0, sc * .9)
        while x < x1:
            w = sc * rng.uniform(1.3, 2.8)
            sh = h * rng.uniform(.66, .98); gap = sc * rng.uniform(.04, .14)
            a, b = max(x, x0) + gap / 2, min(x + w, x1) - gap / 2
            if b - a > .18:
                cy = z + h / 2 + rng.uniform(-.12, .12) * h
                _stone(ax, (a + b) / 2, cy, (b - a) / 2, sh / 2, rng, lw, clip)
                if False:                             # a small chinking stone in the joint above
                    r = sc * rng.uniform(.12, .2); _stone(ax, b + gap / 2, z + h - r * .3, r * 1.3, r, rng, lw * .8, clip)
            x += w + gap
        z += h * rng.uniform(.9, 1.0)

def lw_planks(ax, x0, z0, x1, z1, rng, n=7, lw=.7, zorder=6):
    """a wooden leaf: vertical boards with a little grain, three ledges"""
    ax.add_patch(_LPoly([(x0, z0), (x1, z0), (x1, z1), (x0, z1)], closed=True, fc=globals().get('PAPER', '#faf8f3'), ec=LW_INK, lw=lw, zorder=zorder))
    for k in range(1, n): xx = x0 + (x1 - x0) * k / n; lw_line(ax, [xx, xx], [z0 + .05, z1 - .05], lw=.35, zorder=zorder + .1)
    for k in range(n):                                                       # a grain line or two per board
        bx = x0 + (x1 - x0) * (k + .5) / n
        for _ in range(rng.randint(0, 2)):
            zz = rng.uniform(z0 + .5, z1 - 1.5); L = rng.uniform(.6, 1.6); lw_line(ax, [bx + rng.uniform(-.2, .2)] * 2, [zz, zz + L], lw=.2, color='#6e5233', zorder=zorder + .1)
    for zz in (z0 + .12 * (z1 - z0), z0 + .5 * (z1 - z0), z0 + .88 * (z1 - z0)): lw_line(ax, [x0 + .1, x1 - .1], [zz, zz], lw=.5, zorder=zorder + .2)   # ledges

def lw_ground(ax, x0, x1, z=0, tick=.7, step=1.2, lw=1.1):
    lw_line(ax, [x0, x1], [z, z], lw=lw)
    x = x0 + .3
    while x < x1 - .3: lw_line(ax, [x, x - tick * .55], [z, z - tick], lw=.35); x += step

def lw_pipe(ax, x, z0, z1, d=.55, lw=.7):                      # a post seen in elevation: two lines and caps
    lw_box(ax, x - d / 2, z0, x + d / 2, z1, lw=lw)

def lw_vine(ax, x0, x1, z, rng, depth=1.0, lw=.4):
    """a grapevine canopy in line: loose leaf loops along the top of a trellis"""
    x = x0
    while x < x1:
        r = rng.uniform(.35, .7); cx, cy = x + r, z + rng.uniform(.1, depth)
        t = _np.linspace(0, 2 * _np.pi, 14); ax.plot(cx + r * _np.cos(t) * (1 + .15 * _np.sin(3 * t)), cy + r * .7 * _np.sin(t), color='#55663f', lw=lw)
        x += r * rng.uniform(1.1, 1.7)
