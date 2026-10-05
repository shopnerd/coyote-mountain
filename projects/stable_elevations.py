# 4 Oct (Will): two simple architectural elevations on the stable plan page, left of the plan: east (top) and south (below).
# LINE WORK on the paper (Will, same night): no tone fills; sticks wavy and real; stones in outline; plank doors; hatched ground.
# Numbers from centro-equino-barn.py: 84 x 42 (4 Oct: one more bay at the west end; drawn in the old frame, walls x -48..36), eave 12, ridge 17, 2 ft overhangs, 5 ft rock + pipe at 6, 3 ft stick frames to the
# eave, clerestory 48 x 10 (2.5 ft), 14 ft aisle with sliding doors at the gables, wash pad + trellis + trough on the SW corner.
exec(open('linework.py', encoding='utf-8').read())
import random as _r
def stable_elevations(fig):
    HL, HD, OH, EAVE, RIDGE, RT = 36.0, 21.0, 2.0, 12.0, 17.0, .75
    slope = (RIDGE - EAVE) / HD; rz = lambda y: RIDGE - slope * abs(y) + .55
    rng = _r.Random(14); BG = PAPER if 'PAPER' in globals() else 'white'
    SG = dict(gap=.42, lw=(.25, .5), amp=.08, frame_lw=.7)                      # sticks at this small scale: fewer, finer
    def frames(ax, x0, x1, z0, z1):                                               # 3 ft stick frames between two posts
        n = max(1, round((x1 - x0) / 3)); w = (x1 - x0) / n
        for k in range(n): lw_sticks(ax, x0 + k * w, x0 + (k + 1) * w, z0, z1, rng, frame='sides', **SG)
    def fence(ax, x0, x1):
        for h in (1.8, 3.6, 5.5): lw_line(ax, [x0, x1], [h, h], lw=.55)
        k = x0; s = 10 if x1 > x0 else -10
        while (k <= x1 + .01) if s > 0 else (k >= x1 - .01): lw_line(ax, [k, k], [0, 5.6], lw=.7); k += s
    def opening(ax, x0, z0, x1, z1, lw=.8):                                       # a cut-out: paper behind, outline on top
        ax.add_patch(matplotlib.patches.Rectangle((x0, z0), x1 - x0, z1 - z0, fc=BG, ec=LW_INK, lw=lw, zorder=3))

    # ---------------- east elevation (looking west; north is to the right) ----------------
    ax = fig.add_axes([0.031, 0.56, 0.29, 0.22]); ax.set_aspect('equal'); ax.set_anchor('W'); ax.axis('off'); ax.set_gid('elev-east')   # 4 Oct (Will): bigger, a bit lower
    ax.set_xlim(-28.5, 60.5); ax.set_ylim(-4, 22)
    lw_ground(ax, -28.5, 60.5)
    W = HD + RT
    for a, b in ((-W, -7), (7, W)):
        lw_stones(ax, a, b, 0, 5, rng, big=2.0, small=.9, lw=.45)                                     # rock; 4 Oct (Will): the sticks sit right on it
        frames(ax, a + .3, b - .3, 5.0, EAVE - .1)
    gable = lambda x: RIDGE - slope * abs(x) - .1
    for k in range(-7, 7):                                                         # the gable triangle, 3 ft frames under the roof
        a, b = k * 3, (k + 1) * 3; zt = min(gable(a), gable(b))
        if zt > EAVE + .6: lw_sticks(ax, a, b, EAVE, zt, rng, **SG)
    lw_line(ax, [-HD, 0, HD], [EAVE, RIDGE, EAVE], lw=.9)
    opening(ax, -7, 0, 7, 11.5, lw=.9)                                             # the 14 ft aisle opening
    for a in (-14.6, 7.1):                                                         # both sliding leaves, parked open
        ax.add_patch(matplotlib.patches.Rectangle((a, .1), 7.5, 11.4, fc=BG, ec='none', zorder=4)); lw_planks(ax, a, .1, a + 7.5, 11.5, rng, lw=.6)
    lw_line(ax, [-15, 15], [11.85, 11.85], lw=1.2, zorder=5)
    for p in (-HD, HD): lw_pipe(ax, p, 0, EAVE, d=1.06)
    rl = rz(HD + OH)
    ax.add_patch(_LPoly([(-HD - OH, rl - .45), (0, RIDGE + .1), (HD + OH, rl - .45), (HD + OH, rl), (0, RIDGE + .6), (-HD - OH, rl)], closed=True, fc=BG, ec=LW_INK, lw=.9, zorder=5))
    zb = rz(5.0)
    opening(ax, -5, zb, 5, zb + 2.5, lw=.7)
    for x in (-2.5, 0, 2.5): lw_line(ax, [x, x], [zb, zb + 2.5], lw=.4, zorder=4)
    ax.add_patch(_LPoly([(-6, zb + 2.25), (0, zb + 2.5 + slope * 5), (6, zb + 2.25), (6, zb + 2.6), (0, zb + 2.85 + slope * 5), (-6, zb + 2.6)], closed=True, fc=BG, ec=LW_INK, lw=.8, zorder=5))
    fence(ax, W, W + 40); fence(ax, -W, -W - 6)
    lw_stones(ax, W + 3.5, W + 35.5, 0, 2.0, rng, course=(.9, 1.0), length=(1.4, 2.6), lw=.45)   # east trough on the run fence
    lw_line(ax, [W + 3.9, W + 35.1], [1.75, 1.75], lw=.6, color='#1f78c8')
    ax.text(W + 19.5, -1.4, 'bebedero 32 ft · trough', ha='center', va='top', fontsize=6.5, color=CLAY)
    ax.text(W + 20, 7.0, 'corrales norte · north runs', ha='center', fontsize=6.5, color=MUTED)
    ax.text(0, -1.4, 'pasillo 14 ft · puertas corredizas · aisle, sliding doors', ha='center', va='top', fontsize=6.5, color=INK)
    ax.text(-28.5, 33.5, 'Alzado este · East elevation', fontsize=11, weight='bold', color=INK, clip_on=False)   # titles ride with the drawing when it is moved
    ax.text(-28.5, 31.0, 'la entrada desde el estacionamiento, mirando al oeste · the entry from the parking, looking west', fontsize=7, color=MUTED, style='italic', clip_on=False)
    ax.text(-28.5, 28.4, 'alero 12 ft · cumbrera 17 ft · claraboya a 20.7 ft · eave 12 ft, ridge 17 ft, clerestory top 20.7 ft', fontsize=7, color=MUTED, clip_on=False)

    # ---------------- south elevation (looking north; west is to the left) ----------------
    ax = fig.add_axes([0.031, 0.075, 0.42, 0.18]); ax.set_aspect('equal'); ax.set_anchor('SW'); ax.axis('off'); ax.set_gid('elev-south')   # 4 Oct (Will): moved down; the 3D-model link sits between the two
    XW = -48.0                                                                      # 4 Oct: the new west wall
    ax.set_xlim(-52.5, 39.5); ax.set_ylim(-5, 22)
    lw_ground(ax, -52.5, 39.5)
    L = HL + RT
    lw_stones(ax, XW - RT, L, 0, 5, rng, big=2.0, small=.9, lw=.45)
    lw_box(ax, XW, 5.0, -12, EAVE, lw=.7)                                          # wash + tack rooms: plastered bale / cob to the eave
    for k in range(4): frames(ax, -12 + 12 * k + .3, -12 + 12 * (k + 1) - .3, 5.0, EAVE - .1)
    for c in (-6, 6, 18, 30):                                                       # stall doorways to the runs: open, steel lintel
        opening(ax, c - 3, 0, c + 3, 9); lw_line(ax, [c - 3.1, c + 3.1], [9.1, 9.1], lw=1.4, zorder=4)
    opening(ax, -33, 0, -27, 9)                                                     # wash room opening
    ax.add_patch(matplotlib.patches.Rectangle((-27, .15), 7.3, 9.15, fc=BG, ec='none', zorder=4)); lw_planks(ax, -27, .15, -19.7, 9.3, rng, lw=.6)   # sliding door, parked
    lw_line(ax, [-33.5, -19.4], [9.9, 9.9], lw=1.1, zorder=5)
    for k in range(8): lw_pipe(ax, XW + 12 * k, 0, EAVE, d=1.06)
    r0 = rz(HD + OH) - .45
    ax.add_patch(matplotlib.patches.Rectangle((XW - OH, r0), HL - XW + 2 * OH, RIDGE + .6 - r0, fc=BG, ec=LW_INK, lw=.9, zorder=5))   # roof plane to the ridge
    for x in _np.arange(XW - OH + 2, HL + OH, 2.0): lw_line(ax, [x, x], [r0 + .45, RIDGE + .6], lw=.18, color=MUTED, zorder=6)  # standing seams
    zb = rz(5.0)
    ax.add_patch(matplotlib.patches.Rectangle((-44, zb), 76, 2.5, fc=BG, ec=LW_INK, lw=.7, zorder=6))
    for k in range(14): lw_line(ax, [-44 + 76 / 13 * k] * 2, [zb, zb + 2.5], lw=.45, zorder=7)
    ax.add_patch(matplotlib.patches.Rectangle((-44.8, zb + 2.5), 77.6, .35 + slope * 5, fc=BG, ec=LW_INK, lw=.8, zorder=7))
    lw_line(ax, [XW, -12], [.35, .35], lw=.6, zorder=5)                             # wash pad, 36 ft now
    for x in (XW + .5, -36, -24, -12.5): lw_pipe(ax, x, 0, 10.3, d=.35, lw=.6)      # trellis posts (in front of the wall)
    lw_line(ax, [XW - .3, -11.7], [10.3, 10.3], lw=1.0, zorder=5)
    lw_vine(ax, XW, -12.2, 10.3, rng)
    lw_stones(ax, XW - 3.0, XW, 0, 2.0, rng, course=(.9, 1.0), length=(1.2, 1.6), lw=.45)   # pad trough at the building's corner
    for h in (1.8, 3.6, 5.5): lw_line(ax, [-12, L], [h, h], lw=.45, color=MUTED, zorder=8)   # the south runs' far fence, in front
    ax.text(-30, -1.4, 'baño, eléctrico, lavado · losa · pérgola con parra', ha='center', va='top', fontsize=6.5, color=INK)
    ax.text(-30, -3.3, 'bathroom, electrical, wash · pad · grape trellis', ha='center', va='top', fontsize=6.5, color=MUTED, style='italic')
    ax.text(12, -1.4, 'caballerizas 7-10 · puertas a los corrales', ha='center', va='top', fontsize=6.5, color=INK)
    ax.text(12, -3.3, 'stalls 7-10 · doorways to the runs', ha='center', va='top', fontsize=6.5, color=MUTED, style='italic')
    ax.text(-52.5, 26.5, 'Alzado sur · South elevation', fontsize=11, weight='bold', color=INK, clip_on=False)
    ax.text(-52.5, 24.3, 'el lado del camino, mirando al norte; 84 ft entre muros · the road side, looking north; 84 ft wall to wall', fontsize=7, color=MUTED, style='italic', clip_on=False)
