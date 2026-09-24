def posts_page():
    fig = newpage()
    heading(fig, 'Estructura · postes de tubo sobre pilas y trabes de liga', 'Structure · pipe posts on piers with grade beams')
    R = matplotlib.patches.Rectangle
    # ---------- section at a post
    ax = fig.add_axes([0.02, 0.09, 0.30, 0.78]); ax.set_aspect('equal'); ax.axis('off')
    ax.set_xlim(-7, 7); ax.set_ylim(-8.5, 14.8)
    ax.add_patch(R((-7, -8.5), 14, 8.5, fc='#efe6d2', ec='none'))
    ax.plot([-7, 7], [0, 0], color=INK, lw=1.2)
    ax.add_patch(R((-1.25, -7.0), 2.5, 6.0, fc='#cfcac0', ec=INK, lw=1.1, hatch='..'))
    ax.add_patch(R((-6.5, -2.2), 13, 2.0, fc='#cfcac0', ec=INK, lw=1.1, hatch='..'))
    for y in (-2.0, -0.45): ax.plot([-6.4, 6.4], [y, y], color='#8c3b1f', lw=1.2)
    for x in np.arange(-6, 6.5, 1): ax.plot([x, x], [-2.1, -0.3], color='#8c3b1f', lw=.5)
    ax.add_patch(R((-.95, -0.2), 1.9, .12, fc='#777'))
    ax.add_patch(R((-.95, -0.08), 1.9, .18, fc=INK))
    for x in (-.75, .75): ax.plot([x, x], [-1.9, .3], color=INK, lw=2)
    ax.add_patch(R((-.53, .1), 1.06, 12.0, fc='#6f7d86', ec=INK, lw=1))
    for s_ in (-1, 1): ax.add_patch(matplotlib.patches.Polygon([(s_*.53, .1), (s_*.53, 1.1), (s_*.9, .1)], fc='#6f7d86', ec=INK, lw=.6))
    ax.add_patch(R((-6.5, -.2), 5.9, 4.7, fc='#b9ad97', ec=INK, lw=.8))
    ax.add_patch(R((.6, -.2), 5.9, 4.7, fc='#b9ad97', ec=INK, lw=.8))
    for yy in np.arange(4.8, 11.8, .45):
        ax.plot([-6.5, -.6], [yy, yy], color='#8a6a42', lw=2.2, solid_capstyle='round')
        ax.plot([.6, 6.5], [yy, yy], color='#8a6a42', lw=2.2, solid_capstyle='round')
    ax.plot([-6.5, 6.5], [4.5, 4.5], color='#4a4a4a', lw=2.4)
    ax.add_patch(R((-6.5, 11.8), 13, .5, fc='#4a4a4a'))
    ax.add_patch(R((-.9, 12.1), 1.8, .14, fc=INK))
    ax.plot([-4, 5], [12.3, 14.5], color='#5d95c2', lw=3)
    ax.text(-3.6, 2.2, 'piedra · stone', ha='center', fontsize=7)
    ax.text(3.6, 8.3, 'varas · sticks', ha='center', fontsize=7, color='white', bbox=dict(fc='#8a6a42', ec='none', pad=1))
    ax.text(0, -3.2, 'trabe de liga · grade beam 24 × 24 in', ha='center', fontsize=7, bbox=dict(fc='white', ec='none', pad=1))
    ax.text(0, -7.9, 'pila · pier Ø 30 in × 6 ft', ha='center', fontsize=7)
    ax.text(3.5, 12.6, 'canal de alero · eave channel', fontsize=6.5)
    ax.annotate('', xy=(6.8, 12), xytext=(6.8, 0), arrowprops=dict(arrowstyle='<->', lw=.8)); ax.text(6.95, 6, '12 ft', fontsize=7.5, rotation=90, va='center')
    ax.text(0, 14.6, 'Corte por un poste · Section at a post', ha='center', fontsize=9, weight='bold')
    # ---------- foundation plan: 8 posts at 24 ft
    ax2 = fig.add_axes([0.34, 0.52, 0.30, 0.34]); ax2.set_aspect('equal'); ax2.axis('off'); ax2.set_xlim(-45, 45); ax2.set_ylim(-31, 30)
    ax2.add_patch(R((-39, -22), 78, 44, fc='none', ec='#cfcac0', lw=7))
    ax2.add_patch(R((-39, -22), 78, 44, fc='none', ec='#8a8478', lw=.6))
    for x in (-36, -12, 12, 36):
        ax2.plot([x, x], [-21, 21], color='#5d95c2', lw=1.4)
        for y in (-21, 21): ax2.add_patch(R((x-1.8, y-1.8), 3.6, 3.6, fc='#6f7d86', ec=INK, lw=.6))
    for x in np.arange(-36, 37, 12): ax2.plot([x, x], [-22, -19], color='#999', lw=.5)
    ax2.text(0, 26, 'Planta de cimentación · Foundation plan', ha='center', fontsize=9, weight='bold')
    ax2.text(0, -27, '8 postes a cada 24 ft (uno por cada dos caballerizas), 4 armaduras de 42 ft', ha='center', fontsize=7.5)
    ax2.text(0, -30.5, '8 posts at 24 ft (one every two stalls), 4 trusses spanning 42 ft', ha='center', fontsize=7.5, style='italic', color=MUTED)
    rows = [('Poste · Post', 'tubo de 12 in cortado a 12 ft; los sobrantes sirven para corrales y puertas', '12 in tube cut to 12 ft; offcuts serve runs and gates'),
            ('Placa base · Base plate', '22 × 22 × 1¼ in, 4 cartelas; 4 anclas de 1¼ in grado 55', '22 × 22 × 1¼ in, 4 gussets; 4 × 1¼ in grade 55 anchor rods'),
            ('Pila · Pier', 'Ø 30 in (0.75 m) × 6 ft (1.8 m) bajo cada poste', 'under each post'),
            ('Trabe de liga · Grade beam', '24 × 24 in, 4 varillas #5 arriba y abajo, estribos #3 @ 12 in', '4 #5 bars top and bottom, #3 stirrups at 12 in'),
            ('Viento · Wind (180 km/h)', 'succión ≈ 18 kip por poste; trabe, muro y pila detienen ≈ 20 kip', 'uplift ≈ 18 kip per post; beam, wall and pier hold ≈ 20 kip')]
    y = 0.47
    for a, b_, c in rows:
        fig.text(0.34, y, a, fontsize=8.8, weight='bold', color=INK)
        fig.text(0.34, y-.018, b_, fontsize=8, color=INK)
        fig.text(0.34, y-.033, c, fontsize=7.8, color=MUTED, style='italic'); y -= .056
    notes = [('Propuesta: 8 tubos, uno cada 24 ft, con placa base soldada y atornillada a una pila; una trabe de liga enterrada corre de pila en pila alrededor del establo.',
              'Proposal: 8 tubes, one every 24 ft, each with a welded base plate bolted to a pier; a buried grade beam runs pier to pier around the stable.'),
             ('Menos postes, más carga por poste: cada tubo usa ≈ 46 % de su capacidad y cada ancla ≈ 60 %. Sigue sobrado.',
              'Fewer posts, more load on each: every tube uses ≈ 46% of its capacity and every anchor rod ≈ 60%. Still comfortable.'),
             ('La trabe da cimiento corrido al muro de piedra, amarra los postes, y con el muro encima detiene el techo contra la succión del viento.',
              'The beam gives the stone wall a continuous footing, ties the posts together, and with the wall on it holds the roof down against wind uplift.'),
             ('Soldadura: si los tubos son de pozo petrolero (probable), precalentar, electrodo E7018 y soldadura de prueba.',
              'Welding: if the tubes are oil-field casing (likely), preheat, E7018 rod, and a test weld first.'),
             ('Antes de construir: medir diámetro y espesor, estudio de suelo, y cálculo firmado por ingeniero estructural (DRO / corresponsable).',
              'Before building: measure diameter and wall, a soil test, and calculations signed by a structural engineer (DRO / co-responsible).')]
    y = 0.86
    for es, en in notes: y = para(fig, 0.67, y, es, en, w=60, fs=7.9)
    fig.text(0.67, 0.1, 'Cálculo preliminar de viabilidad, no es diseño estructural.', fontsize=8.5, weight='bold', color=CLAY)
    fig.text(0.67, 0.085, 'Preliminary feasibility check, not a structural design.', fontsize=8.5, color=CLAY, style='italic')
    tblock(fig, nxt(), 'Estructura', 'Structure'); PAGES.append(fig)


def roof_page():
    fig = newpage()
    heading(fig, 'Estructura del techo · primer esquema', 'Roof structure · first scheme')
    # ---------- truss elevation
    ax = fig.add_axes([0.02, 0.50, 0.62, 0.36]); ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-26, 26); ax.set_ylim(-2, 20)
    ax.plot([-26, 26], [0, 0], color=INK, lw=1)
    for x in (-21, 21):
        ax.add_patch(matplotlib.patches.Rectangle((x-.53, 0), 1.06, 12, fc='#6f7d86', ec=INK, lw=.8))
    top = [(-22, 11.95), (0, 17), (22, 11.95)]
    ax.plot([p[0] for p in top], [p[1] for p in top], color=INK, lw=3)
    ax.plot([-21, 21], [12, 12], color=INK, lw=2.4)
    n = 6
    xs = np.linspace(-21, 21, 2*n+1)
    for k, x in enumerate(xs):
        yt = 12 + 5*(1 - abs(x)/21)
        ax.plot([x, x], [12, yt], color=INK, lw=1)
        if k < len(xs)-1:
            x2 = xs[k+1]; yt2 = 12 + 5*(1 - abs(x2)/21)
            if x < 0: ax.plot([x, x2], [12, yt2], color=INK, lw=1)
            else: ax.plot([x2, x], [12, yt], color=INK, lw=1)
    for x in np.linspace(-21, 21, 11):
        y_ = 12 + 5*(1 - abs(x)/21) + .25
        ax.add_patch(matplotlib.patches.Rectangle((x-.3, y_), .6, .7, fc='#9a9487', ec=INK, lw=.4))
    ax.plot([-22.5, 0, 22.5], [11.9+.9, 17+.95, 11.9+.9], color='#5d95c2', lw=2.2)
    ax.annotate('', xy=(-21, -1.2), xytext=(21, -1.2), arrowprops=dict(arrowstyle='<->', lw=.8)); ax.text(0, -1.9, '42 ft (12.8 m)', ha='center', va='top', fontsize=8.5)
    ax.annotate('', xy=(24, 12), xytext=(24, 17), arrowprops=dict(arrowstyle='<->', lw=.8)); ax.text(24.4, 14.5, '5 ft', fontsize=8.5, va='center')
    ax.annotate('', xy=(-24, 0), xytext=(-24, 12), arrowprops=dict(arrowstyle='<->', lw=.8)); ax.text(-24.4, 6, '12 ft', fontsize=8.5, va='center', ha='right')
    ax.text(0, 19.3, 'Armadura tipo · Typical truss', ha='center', fontsize=10, weight='bold')
    ax.text(8, 9.6, 'cuerda inferior · bottom chord HSS 4×4×¼', fontsize=7.5)
    ax.text(-19, 16.3, 'cuerda superior · top chord HSS 4×4×¼', fontsize=7.5)
    ax.text(-4, 13.2, 'diagonales · webs HSS 2×2×³⁄₁₆', fontsize=7, color=MUTED)
    ax.text(10, 16.8, 'larguero Z · Z purlin', fontsize=7, color=MUTED)
    # ---------- roof framing plan
    ax2 = fig.add_axes([0.02, 0.09, 0.62, 0.36]); ax2.set_aspect('equal'); ax2.axis('off'); ax2.set_xlim(-45, 45); ax2.set_ylim(-26, 28)
    ax2.add_patch(matplotlib.patches.Rectangle((-40, -22), 80, 44, fc='#dfeaf3', ec='#5d95c2', lw=1))
    for x in (-36, -12, 12, 36):
        ax2.plot([x, x], [-22, 22], color=INK, lw=2.2)
        for y in (-21, 21): ax2.add_patch(matplotlib.patches.Rectangle((x-1.3, y-1.3), 2.6, 2.6, fc='#6f7d86', ec=INK, lw=.5))
    for y in list(np.arange(-20, 0, 4)) + list(np.arange(4, 21, 4)):
        ax2.plot([-40, 40], [y, y], color='#8a8478', lw=.7)
    ax2.plot([-40, 40], [0, 0], color='#3d6a94', lw=1.2, ls='--')
    for y in (-21, 21): ax2.plot([-37, 37], [y, y], color='#4a4a4a', lw=2.4)
    for (x0, x1) in ((-36, -12), (12, 36)):
        ax2.plot([x0, x1], [-21, 21], color=CLAY, lw=.8); ax2.plot([x0, x1], [21, -21], color=CLAY, lw=.8)
    ax2.text(0, 25.5, 'Planta de techo · Roof framing plan', ha='center', fontsize=10, weight='bold')
    ax2.text(-24, 23, 'cumbrera · ridge', fontsize=7, color='#3d6a94')
    ax2.text(0, -25, 'armaduras a cada 24 ft · largueros Z a cada 4 ft · contravientos en las crujías extremas · alero 2 ft',
             ha='center', fontsize=7.5)
    ax2.text(0, -27.7, 'trusses at 24 ft · Z purlins at 4 ft · rod bracing in the end bays · 2 ft eaves', ha='center', fontsize=7.5, style='italic', color=MUTED)
    rows = [('Armaduras · Trusses', '4, de 42 ft de claro, 5 ft de peralte al centro, soldadas en taller de HSS; apoyan en la placa tapa de cada poste', '4, spanning 42 ft, 5 ft deep at the ridge, shop-welded HSS; bear on each post\'s cap plate'),
            ('Largueros · Purlins', 'Z de 10 in, calibre 12, a cada 4 ft, traslapados sobre las armaduras (≈ 960 ft lineales)', '10 in Z, 12 ga, 4 ft apart, lapped over the trusses (≈ 960 linear ft)'),
            ('Canal de alero · Eave channel', 'C8 corrido de poste a poste en cada lado largo; amarra las armaduras y recibe las varas', 'C8 running post to post on each long side; ties the trusses and takes the sticks'),
            ('Contravientos · Bracing', 'varilla en X en las dos crujías extremas, techo y muros', 'X-rod bracing in both end bays, roof and walls'),
            ('Lámina · Roofing', 'lámina metálica azul cielo, ≈ 3,500 ft² (325 m²)', 'sky-blue metal sheeting, ≈ 3,500 ft² (325 m²)')]
    y = 0.86
    for a, b_, c in rows:
        fig.text(0.67, y, a, fontsize=9.5, weight='bold', color=INK); y -= .02
        y = para(fig, 0.67, y, b_, c, w=58, fs=8)
    y = para(fig, 0.67, y - .01, 'La succión de diseño en los largueros es ≈ 150 lb/ft a 180 km/h; el proveedor de la nave debe confirmar calibres y conexiones.',
             'Design uplift on the purlins is ≈ 150 lb/ft at 180 km/h; the building supplier should confirm gauges and connections.', w=58, fs=8)
    fig.text(0.67, 0.1, 'Esquema preliminar, no es diseño estructural.', fontsize=8.5, weight='bold', color=CLAY)
    fig.text(0.67, 0.085, 'Preliminary scheme, not a structural design.', fontsize=8.5, color=CLAY, style='italic')
    tblock(fig, nxt(), 'Estructura del techo', 'Roof structure'); PAGES.append(fig)


def views2(items, es, en):
    fig = newpage(); heading(fig, es, en)
    for k, (src, tes, ten, des, den) in enumerate(items):
        x = 0.02 + k * 0.49; w = 0.47
        anchor = 'center'
        if isinstance(src, tuple): src, anchor = src
        ax = fig.add_axes([x, 0.30, w, 0.56]); a = img(src)
        H0, W0 = a.shape[:2]; tgt = (w * 17) / (0.56 * 11)
        if W0 / H0 > tgt:
            c = int(H0 * tgt); o = 0 if anchor == 'left' else (W0 - c if anchor == 'right' else (W0 - c) // 2); a = a[:, o:o + c]
        else: c = int(W0 / tgt); a = a[(H0-c)//2:(H0-c)//2 + c]
        ax.imshow(a, aspect='auto'); ax.axis('off')
        fig.text(x, 0.27, tes, fontsize=12, weight='bold', color=INK)
        fig.text(x, 0.248, ten, fontsize=10, color=MUTED, style='italic')
        para(fig, x, 0.215, des, den, w=92, fs=9)
    tblock(fig, nxt(), es, en); PAGES.append(fig)
