"""Structure pages for Walker's stable: pipe portal frames, stone facades, stick walls; base detail; metal building spec."""
Rt = matplotlib.patches.Rectangle
PIPE = '#6f7d86'; STONE_C = '#b9ad97'; STICK = '#8a6a42'; CONC = '#cfcac0'; TIMB = '#a0764a'

def _dim(ax, a, b, txt, off=(0, 0), fs=7.5, **kw):
    ax.annotate('', xy=a, xytext=b, arrowprops=dict(arrowstyle='<->', lw=.7))
    ax.text((a[0] + b[0]) / 2 + off[0], (a[1] + b[1]) / 2 + off[1], txt, fontsize=fs, ha='center', va='center', **kw)

def _pipe_seg(ax, p, q, d=1.06, color=PIPE):
    p = np.array(p, float); q = np.array(q, float); u = (q - p) / np.linalg.norm(q - p); n = np.array([-u[1], u[0]]) * d / 2
    ax.add_patch(matplotlib.patches.Polygon([p + n, q + n, q - n, p - n], fc=color, ec=INK, lw=.7, zorder=5))

def _wavy(ax, x0, x1, y, amp=.08, color=STICK, lw=1.6, seed=0):
    rng = np.random.default_rng(seed); xs = np.linspace(x0, x1, 40)
    ys = y + amp * np.sin(xs * rng.uniform(.6, 1.2) + rng.uniform(0, 6)) + rng.normal(0, amp * .25, len(xs))
    ax.plot(xs, ys, color=color, lw=lw, solid_capstyle='round', zorder=3)

def portal_page():
    fig = newpage()
    heading(fig, 'Estructura · marcos rígidos de tubo, piedra y varas', 'Structure · pipe portal frames, rock and stakes')
    sl = 5 / 20; rz = lambda y: 17 - sl * abs(y)                                  # rafter centre line
    PD = .72                                                                        # 8 in pipe
    # ---------- 1 cross-section through a frame ----------
    ax = fig.add_axes([0.02, 0.47, 0.40, 0.40]); ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-26, 26); ax.set_ylim(-11, 21)
    ax.add_patch(Rt((-26, -11), 52, 11, fc='#efe6d2', ec='none')); ax.plot([-26, 26], [0, 0], color=INK, lw=1)
    for sx in (-1, 1):
        ax.add_patch(Rt((sx * 20 - 1.5, -9), 3, 8.6, fc=CONC, ec=INK, lw=.8, hatch='..', zorder=2))      # pier 36 in x 9 ft
        ax.add_patch(Rt((sx * 20 - 1.1, -.35), 2.2, .3, fc=INK, zorder=6))                                   # base plate
        _pipe_seg(ax, (sx * 20, 0), (sx * 20, 12))
        _pipe_seg(ax, (sx * 22, rz(22)), (0, 17))
        ax.add_patch(matplotlib.patches.Polygon([(sx * 20, 9.5), (sx * 20, 12.4), (sx * 15.5, 13.5)], fc='#55616a', ec=INK, lw=.6, zorder=6))   # knee haunch
        ax.add_patch(Rt((sx * 20 - .75, 0), 1.5, 4.5, fc=STONE_C, ec=INK, lw=.6, zorder=4))                   # rock wall on the column line
        for yy in np.arange(4.9, 11.6, .45): ax.plot([sx * 20 - .2, sx * 20 + .2], [yy, yy], color=STICK, lw=2.2, zorder=4)
    ax.add_patch(Rt((-20, -2.3), 40, 1.6, fc=CONC, ec=INK, lw=.8, hatch='//', zorder=2))                     # tie beam across the aisle
    ax.add_patch(matplotlib.patches.Polygon([(-.9, 16.2), (.9, 16.2), (0, 17.9)], fc='#55616a', ec=INK, lw=.6, zorder=6))   # ridge plates
    off = .53 + PD / 2
    for yy in [k * 22 / 5 for k in range(-5, 6)]:
        y_ = yy if yy else .6
        ax.add_patch(matplotlib.patches.Circle((y_, rz(y_) + off), PD / 2, fc=PIPE, ec=INK, lw=.5, zorder=7))  # 8 in pipe purlins
    ax.plot([-22.3, 0, 22.3], [rz(22.3) + off + PD / 2 + .1, 17 + off + PD / 2 + .1, rz(22.3) + off + PD / 2 + .1], color='#5d95c2', lw=3, zorder=8)   # roof sheet
    _dim(ax, (-20, -10.3), (20, -10.3), '40 ft (12.2 m) a ejes · on centres', off=(0, -.6))
    _dim(ax, (-22, 20), (-20, 20), '2 ft', off=(0, .7), fs=6.5)
    _dim(ax, (24.5, 0), (24.5, 12), '12 ft', off=(1.3, 0)); _dim(ax, (24.5, 12), (24.5, 17), '5 ft', off=(1.3, 0))
    ax.text(0, 20.6, 'Corte por un marco · Section through a frame', ha='center', fontsize=9.5, weight='bold')
    ax.text(-12, 8.2, 'columna tubo 12 in', fontsize=6.5); ax.text(-12, 7.3, '12 in pipe column', fontsize=6.5, style='italic', color=MUTED)
    ax.text(-15.5, 18.9, 'largueros tubo 8 in · 8 in pipe purlins', fontsize=6.5)
    ax.text(-18.5, 10.3, 'cartela · haunch', fontsize=6, color='white', zorder=8)
    ax.text(-17.3, 2, 'piedra', fontsize=6.3); ax.text(-17.3, 6.5, 'varas', fontsize=6.3, color=STICK)
    ax.text(0, -1.5, 'trabe de amarre · tie beam', fontsize=6.5, ha='center', zorder=8)
    ax.text(20, -9.9, 'pila Ø 36 in', fontsize=6.5, ha='center')
    # ---------- 2 gable end: the big entry, frame exposed ----------
    ax3 = fig.add_axes([0.44, 0.47, 0.22, 0.40]); ax3.set_aspect('equal'); ax3.axis('off'); ax3.set_xlim(-24, 24); ax3.set_ylim(-3, 21)
    ax3.plot([-24, 24], [0, 0], color=INK, lw=1)
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 7, sx * 20))
        ax3.add_patch(Rt((x0, 0), x1 - x0, 4.5, fc=STONE_C, ec=INK, lw=.8))
        rng = np.random.default_rng(3 + sx)
        for yy in (1.5, 3.0):
            ax3.plot([x0, x1], [yy, yy], color='#8f836d', lw=.5)
            for x in x0 + np.cumsum(rng.uniform(1.2, 2.8, 12)):
                if x < x1: ax3.plot([x, x], [yy - 1.5, yy], color='#8f836d', lw=.5)
        for v in np.arange(x0 + 2, x1, 4): _pipe_seg(ax3, (v, 4.5), (v, rz(v) - .5), d=.22, color='#4a4a4a')
        for k_, yy in enumerate(np.arange(5.0, 16.4, .42)):
            lim = (17 - yy) / sl - .6                                           # stakes stop under the rafter
            xa, xb = max(x0, -lim) + .2, min(x1, lim) - .2
            if xb - xa > .6: _wavy(ax3, xa, xb, yy, seed=k_ + 30 * (sx + 2), lw=1.2)
    for sx in (-1, 1): _pipe_seg(ax3, (sx * 20, 0), (sx * 20, 12)); _pipe_seg(ax3, (sx * 22, rz(22)), (0, 17))
    ax3.plot([-22.3, 0, 22.3], [rz(22.3) + 1.4, 18.4, rz(22.3) + 1.4], color='#5d95c2', lw=3)
    _dim(ax3, (-7, -1.4), (7, -1.4), '14 ft', off=(0, -.8), fs=7)
    ax3.text(0, 20.3, 'Extremo de acceso · Gable entry', ha='center', fontsize=9.5, weight='bold')
    ax3.text(0, 8, 'entrada abierta\nopen entry', ha='center', va='center', fontsize=7, color=MUTED)
    # ---------- 3 long wall elevation ----------
    ax2 = fig.add_axes([0.02, 0.08, 0.64, 0.33]); ax2.set_aspect('equal'); ax2.axis('off'); ax2.set_xlim(-40, 40); ax2.set_ylim(-3.5, 16)
    ax2.plot([-40, 40], [0, 0], color=INK, lw=1)
    cols = (-36, -12, 12, 36)
    ax2.add_patch(Rt((-36, 0), 72, 4.5, fc=STONE_C, ec=INK, lw=.7))
    for yy in (1.5, 3.0): ax2.plot([-36, 36], [yy, yy], color='#8f836d', lw=.5)
    for v in np.arange(-34, 35, 4):
        if all(abs(v - x) > 1 for x in cols): _pipe_seg(ax2, (v, 4.5), (v, 11.4), d=.22, color='#4a4a4a')      # stake verticals
    for k_, yy in enumerate(np.arange(5.0, 11.2, .42)):
        for i_, (a, b) in enumerate(zip(cols[:-1], cols[1:])): _wavy(ax2, a + .6, b - .6, yy, seed=k_ + 10 * i_)
    for x in (-30, -18, -6, 6, 18, 30):
        ax2.add_patch(Rt((x - 2, 0), 4, 8, fc='#5a4a38', ec=INK, lw=.6, zorder=7))    # stall doors to the runs
    for x in cols: _pipe_seg(ax2, (x, -.2), (x, 12))
    _pipe_seg(ax2, (-36.5, 11.8), (36.5, 11.8), d=PD)                                  # 8 in pipe eave beam
    ax2.plot([-37, 37], [12.9, 12.9], color='#5d95c2', lw=3)
    for x in (-24, 0, 24): ax2.add_patch(Rt((x - 1.75, 12.75), 3.5, .3, fc='#f4f7f2', ec=INK, lw=.5, zorder=9))   # skylight strips (seen edge on)
    for a_, b_ in zip(cols[:-1], cols[1:]): _dim(ax2, (a_, -2.6), (b_, -2.6), '24 ft', off=(0, -.7))
    ax2.text(0, 14.6, 'Muro lateral · Long side wall (norte · north, 72 ft)', ha='center', fontsize=9.5, weight='bold')
    ax2.text(-24, 2.0, 'piedra 4.5 ft · rock', ha='center', fontsize=6.5, zorder=9); ax2.text(-24, 9.7, 'varas de tomate · tomato stakes', ha='center', fontsize=6.5, color='white', zorder=9, bbox=dict(fc=STICK, ec='none', pad=1))
    ax2.text(24, 10.4, 'viga de alero tubo 8 in · 8 in pipe eave beam', ha='center', fontsize=6.3, color='white', zorder=9, bbox=dict(fc='#4a4a4a', ec='none', pad=1))
    # ---------- notes ----------
    rows = [('Marcos · Frames', '4 marcos rígidos, uno cada 24 ft (los dos extremos quedan a la vista en las entradas): 2 columnas y 2 vigas de tubo de 12 in, soldadas en la rodilla y atornilladas en la cumbrera; las vigas siguen 2 ft afuera para el alero', '4 rigid frames at 24 ft (the two end frames exposed at the entries): two 12 in pipe columns and two pipe rafters, welded at the knees, bolted at the ridge; rafters run 2 ft out for the overhang'),
            ('Trabajo del tubo · Pipe use', 'carga máx. 68 % (cédula 40) · flecha en cumbrera ≈ ⅔ in', 'worst case 68% of capacity (Sch 40) · ridge deflection ≈ ⅔ in'),
            ('Largueros y alero · Purlins, eave', 'tubo de 8 in cédula 40 a cada ≈ 5 ft, claro de 24 ft: 38–49 % y ≈ ½ in de flecha. El tubo de 6 in resiste pero rebota demasiado', '8 in Sch 40 pipe at about 5 ft, 24 ft span: 38–49% and ≈ ½ in sag. 6 in pipe is strong enough but too bouncy'),
            ('Cimentación · Foundation', 'pila Ø 36 in × 9 ft por columna, trabe de amarre bajo el pasillo, trabe de liga perimetral bajo la piedra', '36 in × 9 ft pier per column, tie beam under the aisle, perimeter grade beam under the rock')]
    y = 0.875
    for a, b_, c in rows:
        fig.text(0.68, y, a, fontsize=9.3, weight='bold', color=INK); y -= .019
        y = para(fig, 0.68, y, b_, c, w=70, fs=7.2)
    fig.text(0.68, y, 'Por etapas · In stages', fontsize=9.3, weight='bold', color=INK); y -= .019
    for es, en in (('1 · Marcos, largueros y techo: el establo ya funciona con frentes de caballeriza de tubo. Las pilas se diseñan para sostener el techo SIN la piedra.', '1 · Frames, purlins and roof: the stable works with pipe stall fronts. Piers are sized to hold the roof down WITHOUT the rock.'),
                   ('2 · Piedra a 4.5 ft en todo el perímetro, sobre la trabe de liga, con una cadena de concreto arriba y varillas de amarre a las columnas.', '2 · Rock to 4.5 ft all round on the grade beam, with a concrete cap on top and tie rods to the columns.'),
                   ('3 · Varas de tomate horizontales sobre verticales de tubo de 2 in cada 4 ft, fijas a la cadena y a la viga de alero.', '3 · Horizontal tomato stakes on 2 in pipe verticals every 4 ft, fixed to the cap and the eave beam.')):
        y = para(fig, 0.68, y, es, en, w=70, fs=7.0)
    y = para(fig, 0.68, y, 'Sismo: con la piedra sólo a 4.5 ft ya no hay fachadas altas de piedra; el muro bajo lleva castillos de varilla cada ~8 ft y la cadena arriba.',
             'Earthquakes: with rock only to 4.5 ft there are no tall stone facades any more; the low wall gets rebar cores every ~8 ft and the cap on top.', w=70, fs=7.0)
    fig.text(0.68, 0.1, 'Cálculo preliminar de viabilidad, no es diseño estructural.', fontsize=8.5, weight='bold', color=CLAY)
    fig.text(0.68, 0.085, 'Preliminary feasibility check, not a structural design.', fontsize=8.5, color=CLAY, style='italic')
    tblock(fig, nxt(), 'Estructura', 'Structure'); PAGES.append(fig)


def base_page():
    fig = newpage()
    heading(fig, 'Detalle de placa base y anclas', 'Base plate and anchor detail')
    # plan of the plate (inches)
    ax = fig.add_axes([0.02, 0.40, 0.28, 0.46]); ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-16, 16); ax.set_ylim(-16, 17)
    ax.add_patch(Rt((-11, -11), 22, 22, fc='#9aa3a9', ec=INK, lw=1.2))
    ax.add_patch(matplotlib.patches.Circle((0, 0), 6.375, fc='#6f7d86', ec=INK, lw=1.2)); ax.add_patch(matplotlib.patches.Circle((0, 0), 5.97, fc='white', ec=INK, lw=.6))
    for ang in (0, 90, 180, 270):
        c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        ax.add_patch(matplotlib.patches.Polygon([(6.375 * c - .375 * s, 6.375 * s + .375 * c), (11 * c - .375 * s, 11 * s + .375 * c), (11 * c + .375 * s, 11 * s - .375 * c), (6.375 * c + .375 * s, 6.375 * s - .375 * c)], fc='#55616a', ec=INK, lw=.6))
    for sx in (-1, 1):
        for sy in (-1, 1):
            ax.add_patch(Rt((sx * 8 - 1.75, sy * 8 - 1.75), 3.5, 3.5, fc='#c8cdd0', ec=INK, lw=.6))
            ax.add_patch(matplotlib.patches.Circle((sx * 8, sy * 8), 1.03, fc='white', ec=INK, lw=.7)); ax.add_patch(matplotlib.patches.Circle((sx * 8, sy * 8), .625, fc=INK))
    _dim(ax, (-11, -13.5), (11, -13.5), '22 in', off=(0, -.9)); _dim(ax, (-8, 13.2), (8, 13.2), '16 in', off=(0, .9)); _dim(ax, (13.5, -11), (13.5, 11), '22 in', off=(1.3, 0))
    ax.text(0, 16.2, 'Planta · Plan', ha='center', fontsize=9.5, weight='bold')
    # section
    ax2 = fig.add_axes([0.31, 0.40, 0.30, 0.46]); ax2.set_aspect('equal'); ax2.axis('off'); ax2.set_xlim(-22, 22); ax2.set_ylim(-40, 26)
    ax2.add_patch(Rt((-18, -38), 36, 38, fc=CONC, ec=INK, lw=1, hatch='..'))
    ax2.add_patch(Rt((-11, 0), 22, 2, fc='#bbb', ec=INK, lw=.6, hatch='xx'))
    ax2.add_patch(Rt((-11, 2), 22, 1.25, fc='#9aa3a9', ec=INK, lw=1))
    ax2.add_patch(Rt((-6.375, 3.25), 12.75, 22, fc=PIPE, ec=INK, lw=1)); ax2.add_patch(Rt((-5.97, 3.25), 11.94, 22, fc='#8d9aa3', ec='none'))
    for sx in (-1, 1):
        ax2.add_patch(matplotlib.patches.Polygon([(sx * 6.375, 3.25), (sx * 6.375, 12.25), (sx * 11, 3.25)], fc='#55616a', ec=INK, lw=.6))
        x = sx * 8
        ax2.add_patch(Rt((x - .625, -30), 1.25, 34.5, fc=INK))
        ax2.add_patch(Rt((x - 1.4, -31), 2.8, 1, fc=INK)); ax2.add_patch(Rt((x - 1.1, -30), 2.2, .9, fc='#555'))
        ax2.add_patch(Rt((x - 1.1, 1.0), 2.2, .9, fc='#555')); ax2.add_patch(Rt((x - 1.75, 3.25), 3.5, .5, fc='#c8cdd0', ec=INK, lw=.5)); ax2.add_patch(Rt((x - 1.1, 3.75), 2.2, .9, fc='#555'))
    for y in (-34, -6): ax2.plot([-16, 16], [y, y], color='#8c3b1f', lw=1.2)
    for x in (-15, -8, 0, 8, 15): ax2.plot([x, x], [-36, -2], color='#8c3b1f', lw=.8)
    _dim(ax2, (19.5, -30), (19.5, 2), '30 in', off=(1.8, 0)); _dim(ax2, (-18, -39.3), (18, -39.3), 'Ø 36 in', off=(0, -1.3)); _dim(ax2, (-20, 0), (-20, 2), '2 in', off=(-1.8, 0), fs=6.5)
    ax2.text(0, 24.3, 'Corte · Section', ha='center', fontsize=9.5, weight='bold')
    for txt, xy in (('tubo 12¾ × 0.406 in', (7, 18)), ('cartela ¾ in', (11.5, 9)), ('placa 22×22×1¼', (12, 2.6)), ('grout 2 in', (12, .5)), ('tuerca niveladora', (12, -1.3)), ('ancla con cabeza', (10, -18)), ('placa + tuerca', (10, -30.5))):
        ax2.text(*xy, txt, fontsize=6.5)
    # bolt schedule + steps
    rows = [('Anclas · Anchor rods', '4 × 1¼ in ASTM F1554 grado 55, con cabeza (tuerca y placa al fondo), 30 in empotradas, 4 in de rosca arriba', '4 × 1¼ in F1554 Gr 55, headed (nut + plate at the bottom), 30 in embedment, 4 in of thread above'),
            ('NO pernos en J · NO J-bolts', 'el gancho se endereza y se sale con la succión del viento', 'the hook straightens and pulls out under wind uplift'),
            ('Placa base · Base plate', '22 × 22 × 1¼ in A36, agujeros de 2 1/16 in (holgura para ajuste), 4 cartelas ¾ in', '22 × 22 × 1¼ in A36, 2-1/16 in holes (oversize for fit-up), 4 gussets ¾ in'),
            ('Rondanas · Plate washers', '3½ × 3½ × ½ in con agujero estándar, soldadas a la placa después de nivelar', '3½ × 3½ × ½ in, standard hole, welded to the plate after levelling'),
            ('Soldadura · Welds', 'tubo a placa: filete de ½ in todo alrededor; cartelas: filete de ⅜ in, electrodo E7018, precalentar si es tubo de pozo', 'pipe to plate: ½ in fillet all round; gussets ⅜ in, E7018, preheat if oil-field casing'),
            ('Nivelación · Levelling', 'tuercas niveladoras, luego grout sin contracción de 2 in bajo la placa', 'levelling nuts, then 2 in non-shrink grout under the plate'),
            ('Momento en la base · Base moment', '≈ 44 kip-ft; tensión por ancla ≈ 15 kip de 27 kip admisibles', '≈ 44 kip-ft; tension per rod ≈ 15 kip of 27 kip allowable')]
    y = 0.86
    for a, b_, c in rows:
        fig.text(0.64, y, a, fontsize=9.2, weight='bold', color=CLAY if 'J-' in a else INK); y -= .019
        y = para(fig, 0.64, y, b_, c, w=62, fs=7.9)
    steps = [('1', 'Plantilla de triplay de 22 × 22 in con los 4 agujeros; colgar las anclas de la plantilla antes de colar.', 'A 22 × 22 in plywood template with the 4 holes; hang the rods from it before the pour.'),
             ('2', 'Colar la pila y la trabe juntas; revisar ejes y nivel de las anclas con cinta y nivel láser.', 'Pour the pier and beam together; check rod positions and levels with tape and laser.'),
             ('3', 'Soldar la placa al tubo en el taller, a escuadra; levantar el marco completo y asentarlo en las tuercas.', 'Weld the plate to the pipe in the shop, square; lift the whole frame and set it on the nuts.')]
    ax4 = fig.add_axes([0.02, 0.08, 0.59, 0.28]); ax4.axis('off')
    fig.text(0.02, 0.35, 'Colocación · Setting out', fontsize=10, weight='bold', color=INK)
    yy = 0.32
    for n_, es, en in steps:
        fig.text(0.02, yy, n_, fontsize=11, weight='bold', color=CLAY); yy2 = para(fig, 0.045, yy, es, en, w=110, fs=8.4); yy = yy2 - .005
    fig.text(0.64, 0.1, 'Detalle preliminar para cotizar y discutir; lo firma un ingeniero estructural.', fontsize=8.3, weight='bold', color=CLAY)
    fig.text(0.64, 0.085, 'Preliminary detail for pricing and discussion; a structural engineer signs the final.', fontsize=8.3, color=CLAY, style='italic')
    tblock(fig, nxt(), 'Placa base', 'Base plate'); PAGES.append(fig)


def metal_page():
    fig = newpage()
    heading(fig, 'Nave metálica · especificación', 'Metal building · specification')
    cols_x = [0.02, 0.20, 0.47, 0.54]
    hdr = [('Elemento · Item', 0.02), ('Especificación · Spec', 0.20), ('Cant. · Qty', 0.49), ('Notas · Notes', 0.555)]
    y = 0.865
    for t_, x in hdr: fig.text(x, y, t_, fontsize=9, weight='bold', color=INK)
    fig.add_artist(matplotlib.lines.Line2D([0.02, 0.98], [y - .008, y - .008], color=INK, lw=.8))
    items = [
        ('Columnas · Columns', 'tubo 12¾ × 0.406 in (o más grueso), 12 ft', '8', 'de los tubos de 20 ft de Andrés; sobrante 8 ft · from Andrés\' 20 ft tubes; 8 ft offcut'),
        ('Vigas del marco · Rafters', 'tubo 12¾ in, 22.7 ft a lo largo de la pendiente con el alero de 2 ft', '8', '20 ft + 2.7 ft del sobrante, empalme soldado con camisa · 20 ft + 2.7 ft offcut, sleeved weld splice'),
        ('Rodillas · Knee haunches', 'placa ¾ in, cartela triangular 5 × 3 ft', '8', 'donde el momento es mayor · where the moment peaks'),
        ('Cumbrera · Ridge joint', 'dos placas ¾ in atornilladas, 4 × 1 in A325', '4', 'permite armar el marco en dos mitades · lets each frame go up in halves'),
        ('Placas base · Base plates', '22 × 22 × 1¼ in + 4 cartelas', '8', 'ver detalle · see detail'),
        ('Anclas · Anchor rods', '1¼ in F1554 gr. 55 con cabeza, 34 in', '32', 'sin pernos en J · no J-bolts'),
        ('Viga de alero · Eave beams', 'tubo 8⅝ × 0.322 in (8 in céd. 40), 24 ft', '6', 'madera de Andrés después, si las medidas dan · Andrés\' timber later if sizes work'),
        ('Largueros · Purlins', 'tubo 8 in céd. 40 a cada ≈ 5 ft, 24 ft', '30', '10 líneas × 3 crujías, ≈ 690 lb c/u · 10 lines × 3 bays, ≈ 690 lb each'),
        ('Contravientos · Bracing', 'varilla ¾ in en X con tensor', '4 X', 'crujías extremas, techo y muros · end bays, roof and walls'),
        ('Lámina · Roofing', 'Galvalume cal. 26 azul cielo, 72 × 45.4 ft ≈ 3,270 ft² (304 m²)', '1 lote', 'tornillos autotaladrantes con rondana de neopreno · self-drilling screws, neoprene washers'),
        ('Tragaluces · Skylights', 'lámina traslúcida de policarbonato, mismo perfil, 3½ × 10 ft', '6', 'sobre el pasillo, sin ventila de cumbrera · over the aisle, no ridge vent'),
        ('Remates · Trim', 'caballete, goteros, remates de hastial', '1 lote', 'mismo color · matching colour'),
        ('Canal y bajada · Gutter', 'canal en ambos lados largos → bebedero de piedra', '2 × 72 ft', 'el techo da ≈ 7,500 L por cada 2.5 cm de lluvia · ≈ 2,000 gal per inch of rain'),
        ('Acabado · Finish', 'limpieza con chorro, primario rico en zinc, esmalte', '—', 'tubos, placas, varillas · pipes, plates, rods'),
        ('Pilas · Piers', 'Ø 36 in × 9 ft, f\'c 3,000 psi, 8 varillas #6', '8', 'bajo cada columna · under each column'),
        ('Trabes · Beams', 'de liga 24 × 24 in (perímetro) y de amarre bajo el pasillo', '≈ 385 ft', 'la piedra se apoya en la de liga · the rock sits on the grade beam'),
    ]
    y -= .03
    for a, b_, q_, n_ in items:
        fig.text(0.02, y, a, fontsize=8.2, color=INK, weight='bold')
        fig.text(0.20, y, b_, fontsize=8.0, color=INK)
        fig.text(0.49, y, q_, fontsize=8.0, color=INK)
        fig.text(0.555, y, n_, fontsize=7.6, color=MUTED, style='italic')
        y -= .0355
        fig.add_artist(matplotlib.lines.Line2D([0.02, 0.98], [y + .014, y + .014], color='#ddd6c6', lw=.5))
    y -= .01
    fig.text(0.02, y, 'Tubos necesarios · Tubes needed:', fontsize=9, weight='bold', color=INK)
    fig.text(0.19, y, '16 tubos de 12 in de 20 ft (8 columnas + 8 vigas); cada sobrante de 8 ft da 2.7 ft a una viga y deja 5 ft para postes. Más ≈ 865 ft de tubo de 8 in (44 tubos de 20 ft) para 10 líneas de largueros y 2 aleros.', fontsize=8.2, color=INK)
    fig.text(0.19, y - .018, '16 × 20 ft 12 in tubes (8 columns + 8 rafters); each 8 ft offcut gives 2.7 ft to a rafter and leaves 5 ft for posts. Plus ≈ 865 ft of 8 in pipe (44 × 20 ft) for 10 purlin lines and 2 eave beams.', fontsize=8, color=MUTED, style='italic')
    fig.text(0.02, 0.1, 'Cantidades aproximadas para cotizar; confirmar con el ingeniero y el proveedor de la lámina.', fontsize=8.3, weight='bold', color=CLAY)
    fig.text(0.02, 0.085, 'Approximate quantities for pricing; confirm with the engineer and the roofing supplier.', fontsize=8.3, color=CLAY, style='italic')
    tblock(fig, nxt(), 'Nave metálica', 'Metal building'); PAGES.append(fig)
