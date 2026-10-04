# 4 Oct (Will): two simple architectural elevations on the stable plan page, left of the plan: east (top) and south (below).
# Same numbers as centro-equino-barn.py: 72 x 42, eave 12, ridge 17, 2 ft overhangs, 5 ft rock + pipe at 6, stick panels to the eave,
# clerestory 48 x 10 (2.5 ft glazing), 14 ft aisle with sliding doors at the gables, wash pad + trellis + trough on the SW corner.
from matplotlib.patches import Polygon as _Poly
def stable_elevations(fig):
    HL, HD, OH, EAVE, RIDGE, RT = 36.0, 21.0, 2.0, 12.0, 17.0, .75
    slope = (RIDGE - EAVE) / HD; rz = lambda y: RIDGE - slope * abs(y) + .55            # top of the roof sheets
    ROOF, GLASS, WOOD, COB, VINE = '#4a4e53', '#c9d6dd', '#8a6a42', '#e3d6bd', '#8fa070'
    def sticks(ax, x0, x1, z0, z1, top=None):                          # horizontal stick panels; top(x) clips a gable
        z = z0 + .25
        while z < z1:
            if top is None: ax.plot([x0, x1], [z, z], color=STAKE2, lw=.45)
            else:
                xa, xb = x0, x1
                if top(x0) < z or top(x1) < z:                         # clip to the gable line
                    xs = [x for x in (x0 + (x1 - x0) * k / 200 for k in range(201)) if top(x) >= z]
                    if not xs: z += .5; continue
                    xa, xb = xs[0], xs[-1]
                ax.plot([xa, xb], [z, z], color=STAKE2, lw=.45)
            z += .5
    def rock(ax, x0, x1, z1=5.0): ax.add_patch(Rect((x0, 0), x1 - x0, z1, fc=STONE2, ec=INK, lw=.6))
    def fence(ax, x0, x1, alpha=1.0):
        for h in (1.8, 3.6, 5.3): ax.plot([x0, x1], [h, h], color=STEEL2, lw=.9, alpha=alpha)
        k = x0
        while k <= x1 + .01: ax.plot([k, k], [0, 5.5], color=STEEL2, lw=.9, alpha=alpha); k += 10 if x1 > x0 else -10
    def dims(ax, x):
        for z, t in ((EAVE, 'alero · eave 12 ft'), (RIDGE, 'cumbrera · ridge 17 ft')):
            ax.plot([x - .6, x + .6], [z, z], color=MUTED, lw=.7); ax.text(x - 1.2, z, t, ha='right', va='center', fontsize=5.8, color=MUTED)
        ax.plot([x, x], [0, RIDGE], color=MUTED, lw=.5)

    # ---------------- east elevation (looking west; north is to the right) ----------------
    ax = fig.add_axes([0.012, 0.585, 0.272, 0.235]); ax.set_aspect('equal'); ax.axis('off')
    ax.set_xlim(-28.5, 60.5); ax.set_ylim(-4, 22)
    ax.plot([-28.5, 60.5], [0, 0], color=INK, lw=1.1)
    W = HD + RT
    rock(ax, -W, -7); rock(ax, 7, W)
    ax.plot([-W, -7], [6, 6], color=STEEL2, lw=1.2); ax.plot([7, W], [6, 6], color=STEEL2, lw=1.2)
    gable = lambda x: rz(x) - .55
    for a, b in ((-W, -7), (7, W)): sticks(ax, a, b, 6.2, EAVE)
    ax.add_patch(_Poly([(-HD, EAVE), (0, RIDGE), (HD, EAVE)], closed=True, fc='none', ec='none'))
    sticks(ax, -HD, HD, EAVE, RIDGE, top=gable)                                                   # the gable triangle, stick panels
    ax.add_patch(Rect((-7, 0), 14, 11.5, fc='#b9a888', ec=INK, lw=.6))                           # the 14 ft aisle opening
    for a in (-14.6, 7.1):                                                                        # the two sliding leaves, parked open
        ax.add_patch(Rect((a, .1), 7.5, 11.4, fc=WOOD, ec=INK, lw=.5))
        for k in range(1, 7): ax.plot([a + k * 7.5 / 7] * 2, [.3, 11.3], color='#6e5233', lw=.35)
    ax.plot([-15, 15], [11.9, 11.9], color=STEEL2, lw=1.4)                                       # door track
    for p in (-HD, -7, 7, HD): ax.plot([p, p], [0, EAVE], color=STEEL2, lw=1.1)                  # posts in this frame
    ax.add_patch(_Poly([(-HD - OH, rz(HD + OH) - .5), (0, RIDGE + .05), (HD + OH, rz(HD + OH) - .5), (HD + OH, rz(HD + OH)), (0, RIDGE + .6), (-HD - OH, rz(HD + OH))], closed=True, fc=ROOF, ec=INK, lw=.6))
    zb = rz(5.0)                                                                                  # clerestory monitor, end on
    ax.add_patch(Rect((-5, zb), 10, 2.5, fc=GLASS, ec=INK, lw=.5))
    ax.add_patch(_Poly([(-6, zb + 2.5 - .25), (0, zb + 2.5 + slope * 5), (6, zb + 2.5 - .25), (6, zb + 2.85 - .25), (0, zb + 2.85 + slope * 5), (-6, zb + 2.85 - .25)], closed=True, fc=ROOF, ec=INK, lw=.5))
    fence(ax, W, W + 40); fence(ax, -W, -W - 6, alpha=.8)                                        # north runs (full) / south runs (stub)
    ax.add_patch(Rect((W + 3.5, 0), 32, 2.0, fc='#a79f90', ec=INK, lw=.6)); ax.add_patch(Rect((W + 3.9, 1.4), 31.2, .45, fc="#8fb3c7", ec='none'))   # east trough on the run fence
    ax.text(W + 19.5, -1.6, 'bebedero 32 ft · trough', ha='center', va='top', fontsize=6.5, color=CLAY)
    ax.text(W + 20, 7.0, 'corrales norte · north runs', ha='center', fontsize=6.5, color=MUTED)
    ax.text(0, -1.6, 'pasillo 14 ft · puertas corredizas · aisle, sliding doors', ha='center', va='top', fontsize=6.5, color=INK)
    fig.text(0.02, 0.858, 'Alzado este · East elevation', fontsize=11, weight='bold', color=INK)
    fig.text(0.02, 0.841, 'la entrada desde el estacionamiento, mirando al oeste · the entry from the parking, looking west', fontsize=7, color=MUTED, style='italic')
    fig.text(0.02, 0.826, 'alero 12 ft · cumbrera 17 ft · claraboya a 20.7 ft · eave 12 ft, ridge 17 ft, clerestory top 20.7 ft', fontsize=7, color=MUTED)

    # ---------------- south elevation (looking north; west is to the left) ----------------
    ax = fig.add_axes([0.012, 0.29, 0.272, 0.235]); ax.set_aspect('equal'); ax.axis('off')
    ax.set_xlim(-40.5, 39.5); ax.set_ylim(-5, 22)
    ax.plot([-40.5, 39.5], [0, 0], color=INK, lw=1.1)
    L = HL + RT
    rock(ax, -L, L)
    ax.add_patch(Rect((-HL, 5.0), 24, EAVE - 5.0, fc=COB, ec=INK, lw=.5))                      # wash + tack rooms: plastered bale / cob to the eave
    ax.plot([-12, L], [6, 6], color=STEEL2, lw=1.2); sticks(ax, -12, L, 6.2, EAVE)
    for c in (-6, 6, 18, 30): ax.add_patch(Rect((c - 3, 0), 6, 9, fc='#b9a888', ec=INK, lw=.5))    # stall doorways to the runs
    ax.add_patch(Rect((-33, 0), 6, 9, fc='#9aa6ad', ec=INK, lw=.5))                              # wash room opening
    ax.add_patch(Rect((-27, .15), 7.3, 9.15, fc=WOOD, ec=INK, lw=.5))                            # the sliding door, parked east of it
    for k in range(1, 7): ax.plot([-27 + k * 7.3 / 7] * 2, [.3, 9.1], color='#6e5233', lw=.35)
    ax.plot([-33.5, -19.4], [9.9, 9.9], color=STEEL2, lw=1.3)
    for k in range(7): ax.plot([-HL + 12 * k] * 2, [0, EAVE], color=STEEL2, lw=1.1)            # posts every 12 ft
    ax.add_patch(Rect((-HL - OH, rz(HD + OH) - .5), 2 * (HL + OH), RIDGE + .6 - (rz(HD + OH) - .5), fc=ROOF, ec=INK, lw=.6))   # roof plane rising to the ridge
    zb = rz(5.0)
    ax.add_patch(Rect((-24, zb), 48, 2.5, fc=GLASS, ec=INK, lw=.5))
    for k in range(9): ax.plot([-24 + 6 * k] * 2, [zb, zb + 2.5], color=STEEL2, lw=.6)
    ax.add_patch(Rect((-24.8, zb + 2.5), 49.6, .35 + slope * 5, fc=ROOF, ec=INK, lw=.5))
    ax.add_patch(Rect((-HL, 0), 24, .35, fc=CONC2, ec=INK, lw=.5))                               # wash pad
    for x in (-35.5, -24, -12.5): ax.plot([x, x], [0, 10.3], color=STEEL2, lw=1.2)              # trellis posts
    ax.plot([-HL, -12], [10.3, 10.3], color=STEEL2, lw=1.4)
    import random as _r; rv = _r.Random(3)
    for k in range(26):
        x = -HL + .6 + k * 22.8 / 25; ax.add_patch(matplotlib.patches.Ellipse((x, 10.9 + rv.uniform(0, .5)), rv.uniform(1.6, 2.6), rv.uniform(1.0, 1.6), fc=VINE, ec='#6f8255', lw=.3))
    ax.add_patch(Rect((-HL - 3.0, 0), 3.0, 2.0, fc='#a79f90', ec=INK, lw=.6))                    # pad trough, west edge
    fence(ax, -12, L, alpha=.45)                                                                  # the south runs' far fence, in front
    ax.text(-24, -1.6, 'lavado · losa · pérgola con parra', ha='center', va='top', fontsize=6.5, color=INK)
    ax.text(-24, -3.6, 'wash room · pad · trellis with grapes', ha='center', va='top', fontsize=6.5, color=MUTED, style='italic')
    ax.text(12, -1.6, 'caballerizas 7-10 · puertas a los corrales', ha='center', va='top', fontsize=6.5, color=INK)
    ax.text(12, -3.6, 'stalls 7-10 · doorways to the runs', ha='center', va='top', fontsize=6.5, color=MUTED, style='italic')
    fig.text(0.02, 0.555, 'Alzado sur · South elevation', fontsize=11, weight='bold', color=INK)
    fig.text(0.02, 0.538, 'el lado del camino, mirando al norte; 72 ft entre muros · the road side, looking north; 72 ft wall to wall', fontsize=7, color=MUTED, style='italic')
