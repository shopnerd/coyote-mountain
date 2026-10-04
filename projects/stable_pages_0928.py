exec(open('linework.py', encoding='utf-8').read())
POSTR = 12.75 / 24                                         # post radius, ft (12 3/4 in OD)
exec(open('stable_elevations.py', encoding='utf-8').read())
import math
from matplotlib.patches import Circle
# Stable pages for the pack, 28 Sep 2026 design (exec'd by pack.py after its own helpers; replaces barn_plan() and the
# pipe-portal structure pages). 84 x 42 ft on a 12 ft grid (4 Oct: kitchen, bathroom + electrical room in a new west bay); steel trusses
# on 12 in tube posts (4 Oct; were 6 in pipe); 5 ft rock + pipe rail to 6 ft + 3 ft framed stake panels; open clerestory; tan dirt floor.
Rect = matplotlib.patches.Rectangle
STONE2, STAKE2, STEEL2, CONC2, DIRT2 = '#cdb892', '#8a6a48', '#3a3f44', '#d7d3cb', '#e7d8bd'

def barn_plan():
    fig = newpage(); heading(fig, 'Planos arquitectónicos · Establo', 'Architectural drawings · Stable')
    ax = fig.add_axes([0.03, 0.1, 0.62, 0.76]); ax.set_aspect('equal'); ax.set_anchor('E'); ax.axis('off'); ax.set_gid('plan')   # 4 Oct: pushed right so the 3D-model caption clears the runs
    # 4 Oct (Will): 84 ft, one more 12 ft bay at the WEST end for the kitchen (NW) and the bathroom + electrical room (SW). Drawn in the
    # old frame: the old 72 ft walls were x -36..36, so the new west wall is XW = -48 and nothing east of -36 moved.
    L, D, RUN, ST, AI = 84, 42, 40, 12, 14; XW, XE, HD = -48, 36, D / 2; RD = (D - AI) / 2; W5 = 1.5; PY = -HD - W5 / 2   # PY = outside face of the south wall
    for k in range(6):                                       # north runs (none off the kitchen bay)
        x = XW + ST * (k + 1); ax.add_patch(Rect((x, HD), ST, RUN, fc='#f1ead9', ec=INK, lw=.8)); ax.text(x + 6, HD + RUN / 2, 'corral\nrun\n12×40', ha='center', va='center', fontsize=7.5, color=MUTED)
    for k in range(4):                                       # south runs, east end
        x = XW + 36 + ST * k; ax.add_patch(Rect((x, -HD - RUN), ST, RUN, fc='#f1ead9', ec=INK, lw=.8)); ax.text(x + 6, -HD - RUN / 2, 'corral\nrun\n12×40', ha='center', va='center', fontsize=7.5, color=MUTED)
    ax.plot([XW + 36, XE], [-HD - RUN, -HD - RUN], color='#8a7d66', lw=4, solid_capstyle='butt')
    ax.add_patch(Rect((XW, PY - 12), 36, 12, fc=CONC2, ec=INK, lw=.8)); ax.text(XW + 6, PY - 7.5, 'losa · pad\n12 × 36', ha='center', va='center', fontsize=7)
    ax.add_patch(Rect((XW, PY - 12), 36, 12, fill=False, ec=STEEL2, lw=1.1, ls=(0, (3, 2))))   # pipe trellis with grapes over the whole pad (Walker)
    for _x in (XW + .5, XW + 12, XW + 24, XW + 35.5): ax.add_patch(Circle((_x, PY - 11.5), .35, fc=STEEL2, ec='none'))
    ax.text(XW + 18, PY - 13.6, 'pérgola de tubo con parra · pipe trellis with grapes', ha='center', va='top', fontsize=6.5, color=STEEL2)
    ax.plot([XW + 24, XW + 24], [PY - 2, PY - 10], color=STEEL2, lw=2.6, solid_capstyle='round')   # M, the bent-pipe tie hoop
    for _x, _y in ((XW + 12.3, PY - .5), (XW + 24, PY - 2), (XW + 24, PY - 10), (XW + 35.7, PY - .5), (XW + 35.7, PY - 10.6)):
        ax.add_patch(Circle((_x, _y), .45, fc='white', ec=CLAY, lw=1.1, zorder=6))   # tie rings: W post, M hoop, E run fence
    ax.text(XW + 30, PY - 7.5, 'amarres\ntie-ups', ha='center', va='center', fontsize=6.5, color=CLAY)
    ax.plot([XW - 2, XE + 2, XE + 2, XW - 2, XW - 2], [-HD - 2, -HD - 2, HD + 2, HD + 2, -HD - 2], color=MUTED, lw=.7, ls=(0, (4, 3)))   # roof overhangs 2 ft on all four sides
    ax.add_patch(Rect((XW, -HD), L, D, fc=STONE2, ec=INK, lw=2.2))
    ax.add_patch(Rect((XW + W5, -HD + W5), L - 2 * W5, D - 2 * W5, fc=DIRT2, ec='none'))       # tan dirt floor
    # north: the kitchen, then stalls 1-6
    ax.add_patch(Rect((XW + W5, HD - RD), ST - W5, RD - W5, fc='#f6e3c8', ec=INK, lw=1.4)); ax.text(XW + 6, HD - RD / 2 - 1.5, 'cocina\nkitchen', ha='center', va='center', fontsize=7, weight='bold')
    ax.add_patch(Rect((XW + W5 + .3, HD - W5 - 2.3), ST - W5 - .6, 2, fc='white', ec=INK, lw=.5)); ax.add_patch(Rect((XW + W5 + .3, HD - RD + 2), 2, RD - W5 - 4.3, fc='white', ec=INK, lw=.5))   # L counter
    ax.add_patch(Rect((XW - .3, HD - 5.5), .6, 4, fc='#9fd0ea', ec='none'))                                     # window on the gable
    ax.add_patch(Rect((XW + ST - .6, HD - RD), 1.2, RD - W5, fc='#cbb393', ec=INK, lw=.5))
    for k in range(6):                                       # north stalls 1-6, rock partitions, pipe fronts + gates, open doorway to the run
        x = XW + ST * (k + 1); ax.add_patch(Rect((x, HD - RD), ST - (W5 if k == 5 else 0), RD - W5, fc=DIRT2, ec=INK, lw=.6)); ax.text(x + 6, HD - RD / 2, f'{k + 1}\ncaballeriza\nstall', ha='center', va='center', fontsize=7)
        if k: ax.add_patch(Rect((x - .6, HD - RD), 1.2, RD - W5, fc=STONE2, ec=INK, lw=.5))
        ax.add_patch(Rect((x + 3, HD - .9), 6, 1.8, fc='white', ec='none')); ax.plot([x + 3.5, x + 8.5], [HD - RD, HD - RD], color=CLAY, lw=2.2)
    ax.add_patch(Rect((XW + 4.5, HD - RD - .3), 3, .6, fc='white', ec='none'))                                     # kitchen door to the aisle
    # south: bathroom (inner 8) + electrical room (outer 6), wash, tack, stalls 7-10
    ax.add_patch(Rect((XW + W5, -HD + 6), ST - W5, RD - 6, fc='#dcecf4', ec=INK, lw=1.4)); ax.text(XW + 6.5, -HD + 10, 'baño\nbathroom', ha='center', va='center', fontsize=6.8, weight='bold')
    ax.add_patch(Rect((XW + W5, -HD + W5), ST - W5, 6 - W5, fc='#ebe4f3', ec=INK, lw=1.4)); ax.text(XW + 6.5, -HD + 3.6, 'eléctrico\nelectrical', ha='center', va='center', fontsize=6.2, weight='bold')
    ax.add_patch(Rect((XW - .3, -HD + 1.3), .6, 3, fc='white', ec='none'))     # its outside door in the west gable (see the text)
    ax.add_patch(Rect((XW + 4.5, -HD + RD - .3), 3, .6, fc='white', ec='none'))                                    # bathroom door to the aisle
    x = XW + ST
    for es, en, kind in (('lavado', 'wash', 'room'), ('monturas\ny alimento', 'tack / feed', 'room'), ('7\ncaballeriza', 'stall', 's'), ('8\ncaballeriza', 'stall', 's'), ('9\ncaballeriza', 'stall', 's'), ('10\ncaballeriza', 'stall', 's')):
        fc = CONC2 if kind == 'room' else DIRT2
        ax.add_patch(Rect((x, -HD + W5), ST - (W5 if x == XE - ST else 0), RD - W5, fc=fc, ec=INK, lw=1.4 if kind == 'room' else .6)); ax.text(x + 6, -HD + RD / 2, f'{es}\n{en}', ha='center', va='center', fontsize=7)
        ax.add_patch(Rect((x - .6, -HD + W5), 1.2, RD - W5, fc='#cbb393' if kind == 'room' or x == XW + 36 else STONE2, ec=INK, lw=.5))
        if kind == 's': ax.add_patch(Rect((x + 3, -HD - .9), 6, 1.8, fc='white', ec='none')); ax.plot([x + 3.5, x + 8.5], [-HD + RD, -HD + RD], color=CLAY, lw=2.2)
        x += ST
    ax.add_patch(Rect((XW + 15, -HD - .9), 6, 1.8, fc='white', ec='none')); ax.text(XW + 24.8, -HD - 1.9, 'puerta corrediza · sliding door', ha='left', va='top', fontsize=6, color=CLAY); ax.add_patch(Rect((XW + 21.3, -HD - 1.4), 7, .5, fc='#8a6a42', ec='none'))   # the wash room's wooden sliding door, parked east
    ax.add_patch(Rect((XW - 3, PY - 13.5), 3, 13.5, fc='#a79f90', ec=INK, lw=.6)); ax.add_patch(Rect((XW - 2.4, PY - 12.9), 1.8, 12.3, fc='#8fb3c7', ec='none'))   # 4 Oct (Will): the pad trough back at the building's corner
    ax.text(XW - 4.5, PY - 6.75, 'bebedero · trough 14×3', ha='center', va='center', fontsize=6.5, color=CLAY, rotation=90)
    ax.add_patch(Rect((XE + 1, HD + 4), 3.5, 32, fc='#a79f90', ec=INK, lw=.6)); ax.add_patch(Rect((XE + 1.6, HD + 4.6), 2.3, 30.8, fc='#8fb3c7', ec='none'))   # east trough 32 x 3.5 outside the NE run fence
    ax.text(XE + 5.6, HD + 20, 'bebedero este · east trough 32×3.5', ha='center', va='center', fontsize=6.5, color=CLAY, rotation=90)
    ax.text(-6, 0, 'pasillo · aisle 14 ft  (piso de tierra · dirt floor)', ha='center', va='center', fontsize=8.5, color=MUTED)
    for xg, sx in ((XW, -1), (XE, 1)):
        ax.add_patch(Rect((xg - 1, -AI / 2), 2, AI, fc='white', ec='none'))
        for s in (-1, 1): ax.add_patch(Rect((xg + sx * .8, s * AI / 2 + (0 if s > 0 else -7.5)), .5 * sx, 7.5, fc=STAKE2, ec=INK, lw=.4))
        ax.text(xg + sx * (4.5 if sx > 0 else -3.2), 0, 'puerta corrediza\nsliding door', ha='center', va='center', fontsize=6.5, color=CLAY, rotation=90)   # 4 Oct: the west one sits inside the aisle so it clears the elevations
    for x in range(XW, XE + 1, 12):
        for y in (-HD, HD): ax.add_patch(matplotlib.patches.Circle((x, y), .55, fc=STEEL2, ec=INK, lw=.5, zorder=5))
        ax.plot([x, x], [-HD, HD], color=STEEL2, lw=.5, ls=(0, (2, 3)), zorder=4)
    ax.annotate('', xy=(XW, HD + RUN + 5), xytext=(XE, HD + RUN + 5), arrowprops=dict(arrowstyle='<->', lw=.8)); ax.text(-6, HD + RUN + 6, '84 ft (25.6 m) · 7 crujías de 12 ft · 7 bays of 12 ft', ha='center', va='bottom', fontsize=8)
    ax.annotate('', xy=(XE + 8, -HD), xytext=(XE + 8, HD), arrowprops=dict(arrowstyle='<->', lw=.8)); ax.text(XE + 10, 0, '42 ft\n(12.8 m)', va='center', fontsize=9)
    ax.annotate('', xy=(XE + 8, HD), xytext=(XE + 8, HD + RUN), arrowprops=dict(arrowstyle='<->', lw=.8)); ax.text(XE + 10, HD + RUN / 2, '40 ft\ncorrales\nruns', va='center', fontsize=8)
    ax.text(12, -HD - RUN - 3, 'muro bajo de piedra · low rock wall', ha='center', va='top', fontsize=7, color=MUTED)
    ax.text(XW + 10, HD + RUN + 11, 'oeste (camino) ← · → este (estacionamiento)', fontsize=8.5, weight='bold')
    _na = math.radians(24.16); ax.annotate('', xy=(XW + 1 + 7 * math.sin(_na), HD + RUN + 8 + 7 * math.cos(_na)), xytext=(XW + 1, HD + RUN + 8), arrowprops=dict(arrowstyle='-|>', lw=1.2, color=INK), annotation_clip=False); ax.text(XW + 1 + 9.5 * math.sin(_na), HD + RUN + 8 + 9.5 * math.cos(_na), 'N', fontsize=9, weight='bold', ha='center', va='center')   # true north leans 24 deg east of the stable's axis
    ax.set_xlim(-57, 56); ax.set_ylim(-HD - RUN - 8, HD + RUN + 13)
    stable_elevations(fig)                                     # 4 Oct (Will): east + south elevations left of the plan
    y = 0.85
    specs = [('Planta 84 × 42 ft sobre una retícula de 12 ft: 7 crujías, cerchas de acero cada 12 ft. Pasillo central de 14 ft abierto de punta a punta con una puerta corrediza grande en cada extremo; el camino llega directo a la puerta oeste.',
              '84 × 42 ft on a 12 ft grid: 7 bays, steel trusses every 12 ft. A 14 ft centre aisle open end to end with a big sliding door at each end; the road comes straight into the west door.'),
             ('La crujía oeste (nueva, 4 oct): al norte una cocina pequeña de 12 × 14 ft con barra en L, tarja, parrilla de inducción, refri y una ventana al camino de entrada; al sur un baño accesible con regadera (12 × 8 ft) y, en la esquina, el cuarto eléctrico (12 × 6 ft) con su propia puerta exterior en el hastial oeste.',
              'The west bay (new, 4 Oct): to the north a small 12 × 14 ft kitchen with an L counter, sink, induction top, fridge and a window down the entry drive; to the south an accessible bathroom with a shower (12 × 8 ft) and, in the corner, the electrical room (12 × 6 ft) with its own outside door in the west gable.'),
             ('10 caballerizas de 12 × 14 ft, 6 al norte y 4 al sur, separadas por muros de piedra de 5 ft con un tubo arriba; frentes de tubo negro con puerta hacia el pasillo; cada una sale por una abertura libre de 6 × 9 ft a su corral de 12 × 40 ft. Piso de tierra color arena.',
              '10 stalls of 12 × 14 ft, 6 north and 4 south, divided by 5 ft rock walls with a pipe on top; black pipe fronts with a gate to the aisle; each opens through a 6 × 9 ft open doorway to its 12 × 40 ft run. Tan dirt floor.'),
             ('Junto a ellos, del lado sur: el lavado (abertura de 6 × 9 ft con puerta corrediza de madera sobre riel, hacia una losa de concreto de 12 × 36 ft bajo una pérgola con parra, con un bebedero de piedra en la esquina del edificio) y monturas y alimento; todos los cuartos cerrados con paca de paja o cob aplanado, con piso de concreto.',
              'Next to them on the south side: the wash room (a 6 × 9 ft opening with a wooden sliding door on a track, onto a 12 × 36 ft concrete pad under a grape trellis, with a stone trough at the building’s corner) and tack and feed; all the rooms closed in straw bale or plastered cob, with concrete floors.'),
             ('Muro de piedra de 5 ft en todo el perímetro, un tubo negro que flota 1 ft arriba (6 ft en total) y, hasta el alero, paneles de 3 ft de varas horizontales en marco de acero oscuro.',
              'A 5 ft rock wall all round, a black pipe floating 1 ft above it (6 ft overall) and, up to the eave, 3 ft panels of horizontal sticks in dark steel frames.'),
             ('Alero a 12 ft, cumbrera a 17 ft. Techo metálico gris oscuro con una claraboya abierta de 48 × 10 ft sobre el pasillo (sin vidrio) para luz y ventilación.',
              'Eave 12 ft, ridge 17 ft. Dark grey metal roof with an open 48 × 10 ft clerestory over the aisle (no glass) for light and ventilation.')]
    for es, en in specs: y = para(fig, 0.66, y, es, en, w=90, fs=7.6)   # 4 Oct: wider column, closer to the plan (Will)   # 4 Oct: 84 ft adds a paragraph (was 70 / 8.5)
    fig.text(0.68, 0.075, 'Esquema preliminar a partir del diseño de Walker; no es plano de construcción.', fontsize=8, color=MUTED)
    fig.text(0.68, 0.062, 'Preliminary diagram from Walker’s design; not a construction drawing.', fontsize=8, color=MUTED, style='italic')
    tblock(fig, nxt(), 'Planos arquitectónicos', 'Architectural drawings'); PAGES.append(fig)

def truss_page():
    fig = newpage(); heading(fig, 'Estructura · cerchas de acero, piedra y varas', 'Structure · steel trusses, rock and sticks')
    HD, EAVE, RIDGE = 21, 12, 17; rz = lambda y: RIDGE - (RIDGE - EAVE) / HD * abs(y)
    # ---- cross-section through a truss (4 Oct, Will: line work on the paper, no fills; real sticks; field stones) ----
    import random as _r2; rng = _r2.Random(21); BG = PAPER
    ax = fig.add_axes([0.02, 0.44, 0.44, 0.44]); ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-27, 30); ax.set_ylim(-5, 22); ax.set_gid('section')
    lw_ground(ax, -27, 27, step=1.0)
    lw_line(ax, [-HD + .75, HD - .75], [.35, .35], lw=.4, color=MUTED)                                   # dirt floor
    for sx in (-1, 1):
        x = sx * HD
        lw_stones(ax, x - .75, x + .75, 0, 5, rng, big=1.4, small=.8, lw=.5)                          # the rock wall, cut
        lw_box(ax, x - POSTR, -3, x + POSTR, EAVE, lw=.8)                                                    # 12 in tube post (12 3/4 in OD)
        lw_box(ax, x - 1.2, -3.8, x + 1.2, -2.9, lw=.6)                                                # footing
        for k in range(5): lw_line(ax, [x - 1.1 + k * .5, x - .85 + k * .5], [-3.8, -2.9], lw=.25)
        lw_line(ax, [x - .6, x + .6], [6, 6], lw=2.0)                                                  # the floating pipe, in section
        for yy in np.arange(6.4, EAVE - .15, .32):                                                     # sticks cut through: little irregular circles
            r = rng.uniform(.09, .14); t = np.linspace(0, 2 * np.pi, 9)
            ax.plot(x + rng.uniform(-.12, .12) + r * np.cos(t) * rng.uniform(.8, 1.2), yy + r * np.sin(t), color=LW_STICK, lw=.5)
        lw_box(ax, x - .35, 6.2, x + .35, EAVE - .05, lw=.6)                                           # the steel frame around them
        lw_line(ax, [x + sx * 2, 0], [rz(HD + 2), RIDGE], lw=1.8)                                      # top chords with a 2 ft overhang
        for k in (1, 2, 3):
            yv = sx * HD * k / 4; yw = sx * HD * (k - 1) / 4
            lw_line(ax, [yv, yv], [EAVE, rz(yv)], lw=.8); lw_line(ax, [yv, yw], [EAVE, rz(yw)], lw=.7)
    lw_line(ax, [-HD, HD], [EAVE, EAVE], lw=1.5); lw_line(ax, [0, 0], [EAVE, RIDGE], lw=1.0)
    lw_line(ax, [-5, -5], [rz(5), rz(5) + 2.5], lw=.8); lw_line(ax, [5, 5], [rz(5), rz(5) + 2.5], lw=.8)
    lw_line(ax, [-6, 0, 6], [rz(5) + 2.3, RIDGE + 3.4, rz(5) + 2.3], lw=1.5)                            # clerestory roof
    lw_line(ax, [-HD - 2, 0, HD + 2], [rz(HD + 2) + .35, RIDGE + .35, rz(HD + 2) + .35], lw=.6)       # roof sheets on the purlins
    ax.text(0, RIDGE + 4.3, 'claraboya abierta · open clerestory', ha='center', fontsize=8, color=MUTED)
    for (a, b, t) in (((-HD - 3.2, 0), (-HD - 3.2, 5), '5 ft'), ((-HD - 3.2, 5), (-HD - 3.2, 6), '6 ft'), ((HD + 3.2, 0), (HD + 3.2, EAVE), 'alero · eave 12 ft'), ((27, 0), (27, RIDGE), 'cumbrera · ridge 17 ft')):
        ax.annotate('', xy=a, xytext=b, arrowprops=dict(arrowstyle='<->', lw=.6)); ax.text(a[0] + (.6 if a[0] > 0 else -.6), (a[1] + b[1]) / 2, t, fontsize=7.5, ha='left' if a[0] > 0 else 'right', va='center', rotation=90 if a[0] > 20 else 0)
    ax.annotate('', xy=(-HD, -4.4), xytext=(HD, -4.4), arrowprops=dict(arrowstyle='<->', lw=.6)); ax.text(0, -4.1, '42 ft', ha='center', va='bottom', fontsize=8)
    ax.text(-8, 2.6, 'caballeriza · stall', ha='center', fontsize=7.5, color=MUTED); ax.text(8, 2.6, 'pasillo · aisle', ha='center', fontsize=7.5, color=MUTED)
    fig.text(0.02, 0.43, 'Corte por una cercha · Section through a truss', fontsize=12, weight='bold', color=INK)
    # ---- elevation of two bays: rock, the floating pipe, 3 ft frames of real sticks; the 6 x 9 doorway OPEN (Will) ----
    ae = fig.add_axes([0.02, 0.1, 0.44, 0.28]); ae.set_aspect('equal'); ae.axis('off'); ae.set_gid('two-bays'); ae.set_xlim(-1, 25); ae.set_ylim(-1.8, 13.5)
    lw_ground(ae, -1, 25, tick=.35, step=.6, lw=1.0)
    DX0, DX1 = 15, 21                                                                                   # the doorway to the run
    for x0 in (0, 12):
        for a, b in ((x0, x0 + 12),) if x0 == 0 else ((12, DX0), (DX1, 24)):
            lw_stones(ae, a + .25, b - .25, 0, 5, rng, big=2.0, small=.85, lw=.5)
            lw_line(ae, [a + .25, b - .25], [6, 6], lw=1.8)                                           # the floating pipe
            for px in np.arange(a + .25, b - .3, 3.0 if b - a >= 3 else b - a):
                q = min(px + 3.0, b - .25)
                if q - px > .6: lw_sticks(ae, px, q, 6.25, EAVE - .1, rng, gap=.2, lw=(.35, .55), amp=.06, frame_lw=1.1, outline=True)
    for px in np.arange(DX0, DX1 - .1, 3.0):                                                            # above the doorway: sticks from the lintel up
        lw_sticks(ae, px, px + 3.0, 9.35, EAVE - .1, rng, gap=.2, lw=(.35, .55), amp=.06, frame_lw=1.1, outline=True)
    lw_box(ae, DX0, 0, DX1, 9.1, lw=1.0); lw_line(ae, [DX0 - .1, DX1 + .1], [9.2, 9.2], lw=2.2)         # the open doorway and its steel lintel
    ae.text(18, 4.4, 'abertura libre al corral\n6 × 9 ft\nopen doorway to the run', ha='center', va='center', fontsize=7.5, color=INK)
    for x in (0, 12, 24): lw_pipe(ae, x, 0, EAVE, d=.5, lw=.9)
    lw_line(ae, [-1, 25], [EAVE + .1, EAVE + .1], lw=2.0)
    ae.annotate('', xy=(0, -1.1), xytext=(12, -1.1), arrowprops=dict(arrowstyle='<->', lw=.6)); ae.text(6, -1.4, '12 ft', ha='center', va='top', fontsize=8)
    ae.annotate('', xy=(12, 12.8), xytext=(15, 12.8), arrowprops=dict(arrowstyle='<->', lw=.6)); ae.text(13.5, 13.1, '3 ft', ha='center', fontsize=7.5)
    fig.text(0.02, 0.385, 'Alzado de dos crujías · Elevation of two bays', fontsize=11, weight='bold', color=INK)
    y = 0.86
    specs = [('Cerchas de acero cada 12 ft sobre los tubos pesados de 12 in de Andrés (12¾ in de diámetro) como postes, cada uno sobre su zapata: cuerdas superiores hasta la cumbrera, cuerda inferior al alero, montantes y diagonales.',
              'Steel trusses every 12 ft on Andrés’ heavy 12 in tubes as posts (12¾ in outside diameter), each on its own footing: top chords to the ridge, bottom chord at the eave, verticals and diagonals.'),
             ('Muro de piedra apilada de 5 ft en todo el perímetro y entre caballerizas. Un tubo negro flota 1 ft arriba del muro sobre postes cortos: 6 ft en total.',
              'Stacked rock wall 5 ft high all round and between the stalls. A black pipe floats 1 ft above it on short posts: 6 ft overall.'),
             ('Del tubo al alero, paneles de 3 ft de ancho con varas horizontales (tipo nido de pájaro) en marco de acero oscuro; cuatro paneles por crujía de 12 ft.',
              'From the pipe to the eave, 3 ft wide panels of horizontal sticks (bird’s-nest style) in dark steel frames; four panels to each 12 ft bay.'),
             ('Cada caballeriza abre a su corral por una abertura libre de 6 × 9 ft con dintel de acero; hacia el pasillo, frente de tubo negro con puerta.',
              'Each stall opens to its run through an open 6 × 9 ft doorway with a steel lintel; toward the aisle, a black pipe front with a gate.'),
             ('Techo metálico gris oscuro, claraboya abierta de 48 × 10 ft, dos puertas corredizas de madera de 7½ × 11½ ft en cada extremo sobre riel de acero.',
              'Dark grey metal roof, an open 48 × 10 ft clerestory, two 7½ × 11½ ft wooden sliding doors at each end on a steel track.')]
    for es, en in specs: y = para(fig, 0.52, y, es, en, w=74, fs=10)   # 4 Oct: was 8.2
    fig.text(0.52, 0.12, 'Dimensiones de cerchas, postes y zapatas por el ingeniero estructural.', fontsize=9.5, color=CLAY)
    fig.text(0.52, 0.105, 'Truss, post and footing sizes to be set by the structural engineer.', fontsize=9.5, color=CLAY, style='italic')
    tblock(fig, nxt(), 'Estructura', 'Structure'); PAGES.append(fig)
