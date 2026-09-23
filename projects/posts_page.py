def posts_page():
    fig = newpage()
    heading(fig, 'Estructura · postes de tubo sobre pilas y trabes de liga', 'Structure · pipe posts on piers with grade beams')
    R = matplotlib.patches.Rectangle
    # ---------- section: post, base plate, pier, grade beam, stone wall, sticks
    ax = fig.add_axes([0.02, 0.09, 0.30, 0.78]); ax.set_aspect('equal'); ax.axis('off')
    ax.set_xlim(-7, 7); ax.set_ylim(-7.5, 14.8)
    ax.add_patch(R((-7, -7.5), 14, 7.5, fc='#efe6d2', ec='none'))
    ax.plot([-7, 7], [0, 0], color=INK, lw=1.2)
    ax.add_patch(R((-1.25, -6.0), 2.5, 5.0, fc='#cfcac0', ec=INK, lw=1.1, hatch='..'))          # pier
    ax.add_patch(R((-6.5, -2.2), 13, 2.0, fc='#cfcac0', ec=INK, lw=1.1, hatch='..'))           # grade beam (elevation)
    for y in (-2.0, -0.45):
        ax.plot([-6.4, 6.4], [y, y], color='#8c3b1f', lw=1.2)                                  # rebar
    for x in np.arange(-6, 6.5, 1): ax.plot([x, x], [-2.1, -0.3], color='#8c3b1f', lw=.5)      # stirrups
    ax.add_patch(R((-.75, -0.2), 1.5, .12, fc='#777'))                                         # grout pad
    ax.add_patch(R((-.8, -0.08), 1.6, .16, fc=INK))                                            # base plate
    for x in (-.55, .55): ax.plot([x, x], [-1.6, .25], color=INK, lw=1.6)                      # anchor rods
    ax.add_patch(R((-.53, .08), 1.06, 12.0, fc='#6f7d86', ec=INK, lw=1))                       # pipe post
    for s_ in (-1, 1): ax.add_patch(matplotlib.patches.Polygon([(s_*.53, .08), (s_*.53, 1.0), (s_*.8, .08)], fc='#6f7d86', ec=INK, lw=.6))
    ax.add_patch(R((-6.5, -.2), 5.9, 4.7, fc='#b9ad97', ec=INK, lw=.8))                        # stone wall left
    ax.add_patch(R((.6, -.2), 5.9, 4.7, fc='#b9ad97', ec=INK, lw=.8))                          # stone wall right
    for yy in np.arange(4.8, 12, .45):
        ax.plot([-6.5, -.6], [yy, yy], color='#8a6a42', lw=2.2, solid_capstyle='round')
        ax.plot([.6, 6.5], [yy, yy], color='#8a6a42', lw=2.2, solid_capstyle='round')
    for yy in (4.5, 12):
        ax.plot([-6.5, 6.5], [yy, yy], color='#4a4a4a', lw=2.4)                                # girts
    ax.add_patch(R((-.8, 12.08), 1.6, .14, fc=INK)); ax.plot([-4, 5], [12.2, 14.4], color='#5d95c2', lw=3)
    ax.text(-3.6, 2.2, 'piedra · stone', ha='center', fontsize=7)
    ax.text(3.6, 8.3, 'varas · sticks', ha='center', fontsize=7, color='white', bbox=dict(fc='#8a6a42', ec='none', pad=1))
    ax.text(0, -3.2, 'trabe de liga · grade beam 24 × 24 in', ha='center', fontsize=7, bbox=dict(fc='white', ec='none', pad=1))
    ax.text(0, -6.9, 'pila · pier Ø 30 in × 5 ft', ha='center', fontsize=7)
    ax.annotate('', xy=(6.8, 12), xytext=(6.8, 0), arrowprops=dict(arrowstyle='<->', lw=.8)); ax.text(6.95, 6, '12 ft', fontsize=7.5, rotation=90, va='center')
    ax.text(0, 14.6, 'Corte por un poste · Section at a post', ha='center', fontsize=9, weight='bold')
    # ---------- plan: posts on a ring of grade beams
    ax2 = fig.add_axes([0.34, 0.52, 0.30, 0.34]); ax2.set_aspect('equal'); ax2.axis('off'); ax2.set_xlim(-45, 45); ax2.set_ylim(-31, 30)
    ax2.add_patch(R((-39, -22), 78, 44, fc='none', ec='#cfcac0', lw=7))
    ax2.add_patch(R((-39, -22), 78, 44, fc='none', ec='#8a8478', lw=.6))
    for x in np.arange(-36, 37, 12): ax2.plot([x, x], [-21, 21], color='#5d95c2', lw=.9)
    for x in np.arange(-36, 37, 12):
        for y in (-21, 21): ax2.add_patch(R((x-1.6, y-1.6), 3.2, 3.2, fc='#6f7d86', ec=INK, lw=.6))
    ax2.text(0, 26, 'Planta de cimentación · Foundation plan', ha='center', fontsize=9, weight='bold')
    ax2.text(0, -27, '14 postes a cada 12 ft, trabe de liga perimetral, armaduras de 42 ft', ha='center', fontsize=7.5)
    ax2.text(0, -30.5, '14 posts at 12 ft, perimeter grade beam, 42 ft trusses', ha='center', fontsize=7.5, style='italic', color=MUTED)
    rows = [('Poste · Post', 'tubo de 12 in cortado a 12 ft; el sobrante de 8 ft sirve para corrales y puertas', '12 in tube cut to 12 ft; the 8 ft offcut serves runs and gates'),
            ('Placa base · Base plate', '18 × 18 × 1 in, soldada al tubo con 4 cartelas; 4 anclas de 1 in', '18 × 18 × 1 in, welded with 4 gussets; 4 × 1 in anchor rods'),
            ('Pila · Pier', 'Ø 30 in (0.75 m) × 5 ft (1.5 m) bajo cada poste', 'under each post'),
            ('Trabe de liga · Grade beam', '24 × 24 in, 4 varillas #5 arriba y abajo, estribos #3 @ 12 in', '4 #5 bars top and bottom, #3 stirrups at 12 in'),
            ('Viento · Wind (180 km/h)', 'succión ≈ 9 kip por poste; peso de trabe, muro y pila ≈ 11 kip', 'uplift ≈ 9 kip per post; beam + wall + pier hold ≈ 11 kip')]
    y = 0.47
    for a, b_, c in rows:
        fig.text(0.34, y, a, fontsize=8.8, weight='bold', color=INK)
        fig.text(0.34, y-.018, b_, fontsize=8, color=INK)
        fig.text(0.34, y-.033, c, fontsize=7.8, color=MUTED, style='italic'); y -= .056
    notes = [('Propuesta: cada tubo lleva una placa base soldada y se atornilla a una pila de concreto. Una trabe de liga enterrada corre de pila en pila alrededor del establo.',
              'Proposal: each tube gets a welded base plate and bolts to a concrete pier. A buried grade beam runs pier to pier around the stable.'),
             ('La trabe hace tres trabajos: da cimiento corrido al muro de piedra, amarra los postes entre sí, y su peso junto con el del muro detiene el techo contra la succión del viento.',
              'The beam does three jobs: a continuous footing for the stone wall, a tie between posts, and, with the wall on it, the weight that holds the roof down against wind uplift.'),
             ('Con el muro de piedra encima, el peso por poste (≈ 11 kip) supera la succión de diseño (≈ 9 kip a 180 km/h), así las pilas pueden ser más chicas: Ø 30 in × 5 ft.',
              'With the stone wall on it, the weight per post (≈ 11 kip) beats the design uplift (≈ 9 kip at 180 km/h), so the piers can shrink to 30 in × 5 ft.'),
             ('Soldadura: si los tubos son de pozo petrolero (probable), precalentar, usar electrodo E7018 y probar una soldadura de muestra antes de la producción.',
              'Welding: if the tubes are oil-field casing (likely), preheat, use E7018 rod, and test a sample weld before production.'),
             ('Muros: la piedra se asienta en la trabe; las varas se amarran a largueros soldados entre postes a 4.5 y 12 ft. En las puertas la trabe sigue corrida bajo el piso.',
              'Walls: the stone sits on the beam; the sticks tie to girts welded between posts at 4.5 and 12 ft. At doors the beam continues under the floor.'),
             ('Antes de construir: medir diámetro y espesor de los tubos, estudio de suelo, y cálculo firmado por ingeniero estructural (DRO / corresponsable en seguridad estructural).',
              'Before building: measure tube diameter and wall, a soil test, and calculations signed by a structural engineer (DRO / structural co-responsible).')]
    y = 0.86
    for es, en in notes: y = para(fig, 0.67, y, es, en, w=60, fs=7.9)
    fig.text(0.67, 0.1, 'Cálculo preliminar de viabilidad, no es diseño estructural.', fontsize=8.5, weight='bold', color=CLAY)
    fig.text(0.67, 0.085, 'Preliminary feasibility check, not a structural design.', fontsize=8.5, color=CLAY, style='italic')
    tblock(fig, nxt(), 'Estructura', 'Structure'); PAGES.append(fig)
