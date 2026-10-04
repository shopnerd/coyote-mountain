# Stable pages for the pack, 28 Sep 2026 design (exec'd by pack.py after its own helpers; replaces barn_plan() and the
# pipe-portal structure pages). 72 x 42 ft on a 12 ft grid; wash room at the west corner, tack next to it; steel trusses
# on 6 in pipe posts; 5 ft rock + pipe rail to 6 ft + 3 ft framed stake panels; open clerestory; tan dirt floor.
Rect = matplotlib.patches.Rectangle
STONE2, STAKE2, STEEL2, CONC2, DIRT2 = '#cdb892', '#8a6a48', '#3a3f44', '#d7d3cb', '#e7d8bd'

def barn_plan():
    fig = newpage(); heading(fig, 'Planos arquitectónicos · Establo', 'Architectural drawings · Stable')
    ax = fig.add_axes([0.03, 0.1, 0.62, 0.76]); ax.set_aspect('equal'); ax.set_anchor('E'); ax.axis('off')   # 4 Oct: pushed right so the 3D-model caption clears the runs
    L, D, RUN, ST, AI = 72, 42, 40, 12, 14; HL, HD = L / 2, D / 2; RD = (D - AI) / 2; W5 = 1.5
    for k in range(6):                                       # north runs
        x = -HL + ST * k; ax.add_patch(Rect((x, HD), ST, RUN, fc='#f1ead9', ec=INK, lw=.8)); ax.text(x + 6, HD + RUN / 2, 'corral\nrun\n12×40', ha='center', va='center', fontsize=6.5, color=MUTED)
    for k in range(4):                                       # south runs, east end
        x = -HL + 24 + ST * k; ax.add_patch(Rect((x, -HD - RUN), ST, RUN, fc='#f1ead9', ec=INK, lw=.8)); ax.text(x + 6, -HD - RUN / 2, 'corral\nrun\n12×40', ha='center', va='center', fontsize=6.5, color=MUTED)
    ax.plot([-HL + 24, HL], [-HD - RUN, -HD - RUN], color='#8a7d66', lw=4, solid_capstyle='butt')
    ax.add_patch(Rect((-HL, -HD - W5 / 2 - 12), 24, 12, fc=CONC2, ec=INK, lw=.8)); ax.text(-HL + 12, -HD - 7, 'losa de concreto\nconcrete pad 12 × 24', ha='center', va='center', fontsize=6.3)
    ax.plot([-HL, HL, HL, -HL, -HL], [-HD - 2, -HD - 2, HD + 2, HD + 2, -HD - 2], color=MUTED, lw=.7, ls=(0, (4, 3)))
    ax.add_patch(Rect((-HL, -HD), L, D, fc=STONE2, ec=INK, lw=2.2))
    ax.add_patch(Rect((-HL + W5, -HD + W5), L - 2 * W5, D - 2 * W5, fc=DIRT2, ec='none'))       # tan dirt floor
    for k in range(6):                                       # north stalls 1-6, rock partitions, pipe fronts + gates, open doorway to the run
        x = -HL + ST * k; ax.add_patch(Rect((x + (W5 if k == 0 else 0), HD - RD), ST - (W5 if k in (0, 5) else 0), RD - W5, fc=DIRT2, ec=INK, lw=.6)); ax.text(x + 6, HD - RD / 2, f'{k + 1}\ncaballeriza\nstall', ha='center', va='center', fontsize=6.3)
        if k: ax.add_patch(Rect((x - .6, HD - RD), 1.2, RD - W5, fc=STONE2, ec=INK, lw=.5))
        ax.add_patch(Rect((x + 3, HD - .9), 6, 1.8, fc='white', ec='none')); ax.plot([x + 3.5, x + 8.5], [HD - RD, HD - RD], color=CLAY, lw=2.2)
    x = -HL
    for es, en, kind in (('lavado', 'wash', 'room'), ('monturas\ny alimento', 'tack / feed', 'room'), ('7\ncaballeriza', 'stall', 's'), ('8\ncaballeriza', 'stall', 's'), ('9\ncaballeriza', 'stall', 's'), ('10\ncaballeriza', 'stall', 's')):
        fc = CONC2 if kind == 'room' else DIRT2
        ax.add_patch(Rect((x + (W5 if x == -HL else 0), -HD + W5), ST - (W5 if x in (-HL, HL - ST) else 0), RD - W5, fc=fc, ec=INK, lw=1.4 if kind == 'room' else .6)); ax.text(x + 6, -HD + RD / 2, f'{es}\n{en}', ha='center', va='center', fontsize=6.3)
        if x > -HL: ax.add_patch(Rect((x - .6, -HD + W5), 1.2, RD - W5, fc='#cbb393' if kind == 'room' or x == -HL + 24 else STONE2, ec=INK, lw=.5))
        if kind == 's': ax.add_patch(Rect((x + 3, -HD - .9), 6, 1.8, fc='white', ec='none')); ax.plot([x + 3.5, x + 8.5], [-HD + RD, -HD + RD], color=CLAY, lw=2.2)
        x += ST
    ax.add_patch(Rect((-HL + 3, -HD - .9), 6, 1.8, fc='white', ec='none')); ax.text(-HL + 1, -HD - 3, 'puerta corrediza 7×9 · sliding door', ha='left', va='top', fontsize=5.5, color=CLAY); ax.add_patch(Rect((-HL + 9.3, -HD - 1.4), 7, .5, fc='#8a6a42', ec='none'))   # 3 Oct: wooden sliding door, parked east of the opening
    ax.add_patch(Rect((-HL - 3, -HD - 0.75 - 13.5), 3, 13.5, fc='#a79f90', ec=INK, lw=.6)); ax.add_patch(Rect((-HL - 2.4, -HD - 0.75 - 12.9), 1.8, 12.3, fc='#8fb3c7', ec='none'))   # 3 Oct: 14 x 3 ft stone trough on the pad's west edge
    ax.text(-HL - 4.5, -HD - 0.75 - 6.75, 'bebedero · trough 14×3', ha='center', va='center', fontsize=5.5, color=CLAY, rotation=90)
    ax.add_patch(Rect((HL + 30 - 1.75, -25), 3.5, 20, fc='#a79f90', ec=INK, lw=.6)); ax.add_patch(Rect((HL + 30 - 1.15, -24.4), 2.3, 18.8, fc='#8fb3c7', ec='none'))   # 4 Oct (Will, option B): east trough 20 x 3.5 at the gable where the path arrives
    ax.text(HL + 26.6, -15, 'bebedero este · east trough 20×3.5', ha='center', va='center', fontsize=5.5, color=CLAY, rotation=90)
    ax.text(HL + 31.8, -3.4, '← sendero · path', ha='right', va='bottom', fontsize=5.2, color=CLAY)
    ax.text(0, 0, 'pasillo · aisle 14 ft  (piso de tierra · dirt floor)', ha='center', va='center', fontsize=8.5, color=MUTED)
    for sx in (-1, 1):
        xg = sx * HL; ax.add_patch(Rect((xg - 1, -AI / 2), 2, AI, fc='white', ec='none'))
        for s in (-1, 1): ax.add_patch(Rect((xg + sx * .8, s * AI / 2 + (0 if s > 0 else -7.5)), .5 * sx, 7.5, fc=STAKE2, ec=INK, lw=.4))
        ax.text(sx * (HL + 4.5), 0, 'puerta corrediza\nsliding door', ha='center', va='center', fontsize=6.5, color=CLAY, rotation=90)
    for x in range(-36, 37, 12):
        for y in (-HD, HD): ax.add_patch(matplotlib.patches.Circle((x, y), .55, fc=STEEL2, ec=INK, lw=.5, zorder=5))
        ax.plot([x, x], [-HD, HD], color=STEEL2, lw=.5, ls=(0, (2, 3)), zorder=4)
    ax.annotate('', xy=(-HL, HD + RUN + 5), xytext=(HL, HD + RUN + 5), arrowprops=dict(arrowstyle='<->', lw=.8)); ax.text(0, HD + RUN + 6, '72 ft (21.9 m) · 6 crujías de 12 ft · 6 bays of 12 ft', ha='center', va='bottom', fontsize=8)
    ax.annotate('', xy=(HL + 8, -HD), xytext=(HL + 8, HD), arrowprops=dict(arrowstyle='<->', lw=.8)); ax.text(HL + 10, 0, '42 ft\n(12.8 m)', va='center', fontsize=9)
    ax.annotate('', xy=(HL + 8, HD), xytext=(HL + 8, HD + RUN), arrowprops=dict(arrowstyle='<->', lw=.8)); ax.text(HL + 10, HD + RUN / 2, '40 ft\ncorrales\nruns', va='center', fontsize=8)
    ax.text(12, -HD - RUN - 3, 'muro bajo de piedra · low rock wall', ha='center', va='top', fontsize=7, color=MUTED)
    ax.text(-HL - 13, 0, 'camino\nroad →', ha='center', va='center', fontsize=7.5, color=MUTED); ax.text(-HL, HD + RUN + 11, 'N ↑   oeste (camino) ← · → este (estacionamiento)', fontsize=8.5, weight='bold')
    ax.set_xlim(-57, 72); ax.set_ylim(-HD - RUN - 8, HD + RUN + 13)   # 4 Oct: room for the east trough
    y = 0.85
    specs = [('Planta 72 × 42 ft sobre una retícula de 12 ft: 6 crujías, cerchas de acero cada 12 ft. Pasillo central de 14 ft abierto de punta a punta con una puerta corrediza grande en cada extremo; el camino llega directo a la puerta oeste.',
              '72 × 42 ft on a 12 ft grid: 6 bays, steel trusses every 12 ft. A 14 ft centre aisle open end to end with a big sliding door at each end; the road comes straight into the west door.'),
             ('10 caballerizas de 12 × 14 ft, 6 al norte y 4 al sur, separadas por muros de piedra de 5 ft con un tubo arriba; frentes de tubo negro con puerta hacia el pasillo; cada una sale por una abertura libre de 6 × 9 ft a su corral de 12 × 40 ft. Piso de tierra color arena.',
              '10 stalls of 12 × 14 ft, 6 north and 4 south, divided by 5 ft rock walls with a pipe on top; black pipe fronts with a gate to the aisle; each opens through a 6 × 9 ft open doorway to its 12 × 40 ft run. Tan dirt floor.'),
             ('En la esquina oeste del lado sur, junto al camino: el lavado (abertura de 6 × 9 ft con puerta corrediza de madera sobre riel, hacia una losa de concreto de 12 × 24 ft con un bebedero de piedra en su borde oeste) y monturas y alimento; los dos cerrados con paca de paja o cob aplanado, y con piso de concreto.',
              'At the west corner of the south side, by the road: the wash room (a 6 × 9 ft opening with a wooden sliding door on a track, onto a 12 × 24 ft concrete pad with a stone trough along its west edge) and tack and feed; both closed in straw bale or plastered cob, with concrete floors.'),
             ('Muro de piedra de 5 ft en todo el perímetro, un tubo negro que flota 1 ft arriba (6 ft en total) y, hasta el alero, paneles de 3 ft de varas horizontales en marco de acero oscuro.',
              'A 5 ft rock wall all round, a black pipe floating 1 ft above it (6 ft overall) and, up to the eave, 3 ft panels of horizontal sticks in dark steel frames.'),
             ('Alero a 12 ft, cumbrera a 17 ft. Techo metálico gris oscuro con una claraboya abierta de 48 × 10 ft sobre el pasillo (sin vidrio) para luz y ventilación.',
              'Eave 12 ft, ridge 17 ft. Dark grey metal roof with an open 48 × 10 ft clerestory over the aisle (no glass) for light and ventilation.')]
    for es, en in specs: y = para(fig, 0.68, y, es, en, w=64, fs=7.3)
    fig.text(0.68, 0.1, 'Esquema preliminar a partir del diseño de Walker; no es plano de construcción.', fontsize=8, color=MUTED)
    fig.text(0.68, 0.085, 'Preliminary diagram from Walker’s design; not a construction drawing.', fontsize=8, color=MUTED, style='italic')
    tblock(fig, nxt(), 'Planos arquitectónicos', 'Architectural drawings'); PAGES.append(fig)

def truss_page():
    fig = newpage(); heading(fig, 'Estructura · cerchas de acero, piedra y varas', 'Structure · steel trusses, rock and sticks')
    HD, EAVE, RIDGE = 21, 12, 17; rz = lambda y: RIDGE - (RIDGE - EAVE) / HD * abs(y)
    # ---- cross-section through a truss ----
    ax = fig.add_axes([0.02, 0.44, 0.44, 0.44]); ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-27, 30); ax.set_ylim(-5, 22)
    ax.add_patch(Rect((-27, -5), 54, 5, fc='#efe6d2', ec='none')); ax.plot([-27, 27], [0, 0], color=INK, lw=1)
    ax.add_patch(Rect((-HD + .75, 0), 2 * HD - 1.5, .35, fc=DIRT2, ec='none'))
    for sx in (-1, 1):
        x = sx * HD
        ax.add_patch(Rect((x - .75, 0), 1.5, 5, fc=STONE2, ec=INK, lw=.7, zorder=3))
        ax.add_patch(Rect((x - .3, -3), .6, EAVE + 3, fc=STEEL2, ec=INK, lw=.5, zorder=4))                 # 6 in pipe post on its footing
        ax.add_patch(Rect((x - 1.2, -3.8), 2.4, .9, fc=CONC2, ec=INK, lw=.5, hatch='..', zorder=2))
        ax.plot([x - .6, x + .6], [6, 6], color='black', lw=2.2, zorder=5)                                   # the floating pipe
        for yy in np.arange(6.5, EAVE - .2, .42): ax.plot([x - .25, x + .25], [yy, yy], color=STAKE2, lw=2, zorder=4)
        ax.plot([x + sx * 2, 0], [rz(HD + 2), RIDGE], color=STEEL2, lw=2.6, zorder=6)                       # top chords with a 2 ft overhang
        for k in (1, 2, 3):                                                                                    # verticals and webs
            yv = sx * HD * k / 4; yw = sx * HD * (k - 1) / 4
            ax.plot([yv, yv], [EAVE, rz(yv)], color=STEEL2, lw=1.2, zorder=6); ax.plot([yv, yw], [EAVE, rz(yw)], color=STEEL2, lw=1, zorder=6)
    ax.plot([-HD, HD], [EAVE, EAVE], color=STEEL2, lw=2, zorder=6); ax.plot([0, 0], [EAVE, RIDGE], color=STEEL2, lw=1.4, zorder=6)
    ax.plot([-5, -5], [rz(5), rz(5) + 2.5], color=STEEL2, lw=1.2); ax.plot([5, 5], [rz(5), rz(5) + 2.5], color=STEEL2, lw=1.2)
    ax.plot([-6, 0, 6], [rz(5) + 2.3, RIDGE + 3.4, rz(5) + 2.3], color=STEEL2, lw=2.2)                        # clerestory roof
    ax.text(0, RIDGE + 4.3, 'claraboya abierta · open clerestory', ha='center', fontsize=7.5, color=MUTED)
    for (a, b, t) in (((-HD - 3.2, 0), (-HD - 3.2, 5), '5 ft'), ((-HD - 3.2, 5), (-HD - 3.2, 6), '6 ft'), ((HD + 3.2, 0), (HD + 3.2, EAVE), 'alero · eave 12 ft'), ((27, 0), (27, RIDGE), 'cumbrera · ridge 17 ft')):
        ax.annotate('', xy=a, xytext=b, arrowprops=dict(arrowstyle='<->', lw=.7)); ax.text(a[0] + (.6 if a[0] > 0 else -.6), (a[1] + b[1]) / 2, t, fontsize=6.8, ha='left' if a[0] > 0 else 'right', va='center', rotation=90 if a[0] > 20 else 0)
    ax.annotate('', xy=(-HD, -4.4), xytext=(HD, -4.4), arrowprops=dict(arrowstyle='<->', lw=.7)); ax.text(0, -4.1, '42 ft', ha='center', va='bottom', fontsize=8)
    ax.text(-8, 2.6, 'caballeriza · stall', ha='center', fontsize=7, color=MUTED); ax.text(8, 2.6, 'pasillo · aisle', ha='center', fontsize=7, color=MUTED)
    fig.text(0.02, 0.43, 'Corte por una cercha · Section through a truss', fontsize=11, weight='bold', color=INK)
    # ---- elevation of two bays ----
    ae = fig.add_axes([0.02, 0.1, 0.44, 0.28]); ae.set_aspect('equal'); ae.axis('off'); ae.set_xlim(-1, 25); ae.set_ylim(-1.5, 13.5)
    ae.plot([-1, 25], [0, 0], color=INK, lw=1)
    for x0 in (0, 12):
        ae.add_patch(Rect((x0, 0), 12, 5, fc=STONE2, ec=INK, lw=.6))
        ae.plot([x0, x0 + 12], [6, 6], color='black', lw=2)
        for k in range(4):
            px = x0 + 3 * k; ae.add_patch(Rect((px, 6.2), 3, EAVE - 6.4, fc='none', ec=STEEL2, lw=1.1))
            for yy in np.arange(6.6, EAVE - .3, .42): ae.plot([px + .15, px + 2.85], [yy, yy], color=STAKE2, lw=1.4)
    ae.add_patch(Rect((15, 0), 6, 9, fc='white', ec=INK, lw=.8)); ae.plot([15, 21], [9.1, 9.1], color=STEEL2, lw=2.4); ae.text(18, 4, 'abertura\nlibre al\ncorral\n6 × 9 ft\nopen\ndoorway', ha='center', va='center', fontsize=6.3)
    for x in (0, 12, 24): ae.add_patch(Rect((x - .25, 0), .5, EAVE, fc=STEEL2, ec=INK, lw=.4))
    ae.plot([-1, 25], [EAVE + .1, EAVE + .1], color=STEEL2, lw=3)
    ae.annotate('', xy=(0, -1), xytext=(12, -1), arrowprops=dict(arrowstyle='<->', lw=.7)); ae.text(6, -1.4, '12 ft', ha='center', va='top', fontsize=7.5)
    ae.annotate('', xy=(12, 12.8), xytext=(15, 12.8), arrowprops=dict(arrowstyle='<->', lw=.7)); ae.text(13.5, 13.1, '3 ft', ha='center', fontsize=7)
    fig.text(0.02, 0.385, 'Alzado de dos crujías · Elevation of two bays', fontsize=11, weight='bold', color=INK)
    y = 0.86
    specs = [('Cerchas de acero cada 12 ft sobre postes de tubo de 6 in (6⅝ in de diámetro), cada uno sobre su zapata: cuerdas superiores hasta la cumbrera, cuerda inferior al alero, montantes y diagonales.',
              'Steel trusses every 12 ft on 6 in pipe posts (6⅝ in outside diameter), each on its own footing: top chords to the ridge, bottom chord at the eave, verticals and diagonals.'),
             ('Muro de piedra apilada de 5 ft en todo el perímetro y entre caballerizas. Un tubo negro flota 1 ft arriba del muro sobre postes cortos: 6 ft en total.',
              'Stacked rock wall 5 ft high all round and between the stalls. A black pipe floats 1 ft above it on short posts: 6 ft overall.'),
             ('Del tubo al alero, paneles de 3 ft de ancho con varas horizontales (tipo nido de pájaro) en marco de acero oscuro; cuatro paneles por crujía de 12 ft.',
              'From the pipe to the eave, 3 ft wide panels of horizontal sticks (bird’s-nest style) in dark steel frames; four panels to each 12 ft bay.'),
             ('Cada caballeriza abre a su corral por una abertura libre de 6 × 9 ft con dintel de acero; hacia el pasillo, frente de tubo negro con puerta.',
              'Each stall opens to its run through an open 6 × 9 ft doorway with a steel lintel; toward the aisle, a black pipe front with a gate.'),
             ('Techo metálico gris oscuro, claraboya abierta de 48 × 10 ft, dos puertas corredizas de madera de 7½ × 11½ ft en cada extremo sobre riel de acero.',
              'Dark grey metal roof, an open 48 × 10 ft clerestory, two 7½ × 11½ ft wooden sliding doors at each end on a steel track.')]
    for es, en in specs: y = para(fig, 0.52, y, es, en, w=74, fs=8.2)
    fig.text(0.52, 0.12, 'Dimensiones de cerchas, postes y zapatas por el ingeniero estructural.', fontsize=8.5, color=CLAY)
    fig.text(0.52, 0.105, 'Truss, post and footing sizes to be set by the structural engineer.', fontsize=8.5, color=CLAY, style='italic')
    tblock(fig, nxt(), 'Estructura', 'Structure'); PAGES.append(fig)
