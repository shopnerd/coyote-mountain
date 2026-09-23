def existing():
    fig = newpage(); heading(fig, 'Topografía existente', 'Existing topography')
    ax = plain_axes(fig, [0.02, 0.075, 0.74, 0.82])
    ax.contour(X, Y, b, levels=np.arange(1050, 1125, 1), colors='#9a9487', linewidths=.35)
    ax.contour(X, Y, b, levels=np.arange(1050, 1125, 5), colors=INK, linewidths=.85)
    for nm in ('existing vineyard road', 'existing scrub-side road'):
        for s in byname(nm):
            P = np.array([q[:2] for q in s['pts']]); ax.plot(P[:, 0], P[:, 1], color='#b9a784', lw=6, alpha=.7, solid_capstyle='round', zorder=2)
    fence(ax); north(ax, 140, 8); scalebar(ax, 6, 96)
    y = 0.86
    y = para(fig, 0.78, y, 'Terreno natural antes de cualquier movimiento de tierra. Curvas cada 1 pie; las gruesas cada 5 pies.',
             'Natural ground before any earthwork. Contours every 1 ft; heavy lines every 5 ft.', w=40, fs=9.5)
    y = para(fig, 0.78, y, f'El sitio cae unos {b.max()-b.min():.0f} pies hacia el viñedo, cerca de 6 %.',
             f'The ground falls about {b.max()-b.min():.0f} ft toward the vineyard, about 6%.', w=40, fs=9.5)
    items = [(INK, '-', .85, 'Curva cada 5 ft · 5 ft contour'), ('#9a9487', '-', .4, 'Curva cada 1 ft · 1 ft contour'),
             ('#b9a784', '-', 6, 'Caminos existentes · Existing roads'), (INK, (0, (7, 2, 1, 2)), 1.4, 'Cerca del predio · Site fence')]
    ly = 0.30
    for c, st, lw, t in items:
        fig.add_artist(matplotlib.lines.Line2D([0.78, 0.81], [ly, ly], color=c, lw=lw, ls=st)); fig.text(0.818, ly-.005, t, fontsize=8.5, color=INK); ly -= .025
    tblock(fig, nxt(), 'Topografía existente', 'Existing topography'); PAGES.append(fig)


def min_rect(P):
    P = np.array(P); from itertools import product
    best = None
    hull = P
    for k in range(len(hull)):
        a, c = hull[k], hull[(k+1) % len(hull)]
        e = c - a; Ln = np.hypot(*e)
        if Ln < 1e-6: continue
        u = e / Ln; v = np.array([-u[1], u[0]])
        s_ = P @ u; t_ = P @ v
        A = (s_.max()-s_.min())*(t_.max()-t_.min())
        if best is None or A < best[0]: best = (A, u, v, s_.min(), s_.max(), t_.min(), t_.max())
    _, u, v, s0, s1, t0, t1 = best
    return [u*s + v*t for s, t in ((s0, t0), (s1, t0), (s1, t1), (s0, t1))]


def operator_sheet():
    fig = newpage(); heading(fig, 'Plano de nivelación para el operador', 'Grading sheet for the machine operator')
    ax = plain_axes(fig, [0.02, 0.075, 0.70, 0.82])
    dd = z - b
    ax.contour(X, Y, b, levels=np.arange(1050, 1125, 1), colors='#b5b0a5', linewidths=.35, linestyles='dashed', zorder=1)
    c5 = ax.contour(X, Y, z, levels=np.arange(1050, 1125, 1), colors=INK, linewidths=.4, zorder=2)
    for s in S:
        if s.get('kind') == 'path':
            P = np.array([q[:2] for q in s['pts']]); ax.plot(P[:, 0], P[:, 1], color='#8a7a5a', lw=.8, dashes=(10, 3, 2, 3), zorder=3)
    for nm in ('walker barn 76x42', 'four paddocks'):
        for s in byname(nm):
            P = np.array(foot(s) + [foot(s)[0]]); ax.plot(P[:, 0], P[:, 1], color=INK, lw=1.1, zorder=4)
    for i in (1, 2):
        P = np.array([q[:2] for q in S[i]['pts']]); ax.plot(P[:, 0], P[:, 1], color=INK, lw=1.1, zorder=4)
    fence(ax, col='#666')
    # 50 ft staking grid, lettered columns and numbered rows
    step = 50 / cf
    xs = np.arange(step/2, W-1, step); ys = np.arange(step/2, H-1, step)
    for k, x in enumerate(xs):
        ax.plot([x, x], [0, H-1], color='#c9d6e3', lw=.5, zorder=0)
        ax.text(x, -1.2, chr(65+k) if k < 26 else 'A'+chr(39+k), ha='center', va='bottom', fontsize=7, color='#3d6a94', weight='bold')
    for k, y in enumerate(ys):
        ax.plot([0, W-1], [y, y], color='#c9d6e3', lw=.5, zorder=0)
        ax.text(-1, y, str(k+1), ha='right', va='center', fontsize=7, color='#3d6a94', weight='bold')
    ax.set_xlim(-3, W-1); ax.set_ylim(H-1, -3)
    n = 0
    for x in xs:
        for y in ys:
            v = samp(dd, x, y)
            if abs(v) < 0.3: continue
            n += 1
            col = '#9a3a1a' if v < 0 else '#1f5f9a'
            ax.plot(x, y, marker='o', ms=2.4, color=col, zorder=6)
            ax.text(x+.5, y-.5, f'{"C" if v < 0 else "F"} {abs(v):.1f}', fontsize=6, color=col, weight='bold', zorder=6)
            ax.text(x+.5, y+1.3, f'{samp(z, x, y):.1f}', fontsize=4.8, color='#555', zorder=6)
    # pad corner stakes with finished elevation
    for nm in ('walker barn 76x42', 'four paddocks'):
        for s in byname(nm):
            rc = min_rect(foot(s)); cc = np.mean(rc, axis=0)
            for q in rc:
                cx, cy = q + (cc - q) / np.linalg.norm(cc - q) * 1.8
                ax.plot(cx, cy, marker='s', ms=4, mfc='white', mec=INK, mew=1, zorder=7)
                ax.text(cx+.6, cy+.6, f'{samp(z, cx, cy):.1f}', fontsize=6, color=INK, zorder=7, bbox=dict(fc='white', ec='none', pad=.5))
    north(ax, 140, 8); scalebar(ax, 6, 96)
    # legend and notes
    fig.add_artist(matplotlib.patches.FancyBboxPatch((0.735, 0.60), 0.245, 0.26, boxstyle='round,pad=0.006', transform=fig.transFigure, fc='#fff4e8', ec=CLAY, lw=1.4))
    fig.text(0.745, 0.845, 'PRIMERO: TRAZAR · STAKE FIRST', fontsize=11, weight='bold', color=CLAY)
    y = 0.822
    y = para(fig, 0.745, y, 'Las elevaciones salen de mapas públicos de terreno de 30 m y NO son exactas (pueden variar varios pies). Antes de mover tierra: estacar, tender hilo y banderear cada esquina de plataforma, eje de camino, zanja y el bajo natural; poner un banco de nivel fijo; medir el terreno real en cada estaca con nivel láser y ajustar corte y relleno.',
             'Elevations come from 30 m public terrain maps and are NOT exact (they can be off by several feet). Before any earthwork: stake, string and flag every pad corner, road centreline, swale and the water sink; set a fixed benchmark; measure the real ground at every stake with a laser level and adjust cut and fill.', w=52, fs=7.9)
    y = 0.57
    fig.text(0.745, y, 'Cómo leer · How to read', fontsize=10, weight='bold', color=INK); y -= .025
    rows = [('#9a3a1a', 'C 2.3', 'corte de 2.3 ft · cut 2.3 ft'), ('#1f5f9a', 'F 1.1', 'relleno de 1.1 ft · fill 1.1 ft'),
            ('#555', '1082.4', 'rasante terminada en la estaca · finished grade at the stake'), (INK, '□ 1087.6', 'esquina de plataforma · pad corner')]
    for c, a, t in rows:
        fig.text(0.745, y, a, fontsize=8.5, color=c, weight='bold'); fig.text(0.80, y, t, fontsize=8, color=INK); y -= .021
    y -= .01
    y = para(fig, 0.745, y, f'Cuadrícula de estacas cada 50 ft (columnas A–{chr(64+len(xs))}, filas 1–{len(ys)}). {n} estacas marcadas donde el corte o relleno pasa de 0.3 ft.',
             f'Stake grid every 50 ft (columns A–{chr(64+len(xs))}, rows 1–{len(ys)}). {n} stakes marked where cut or fill exceeds 0.3 ft.', w=52, fs=7.9)
    y = para(fig, 0.745, y, 'Revisar: los caminos junto a los corrales y al establo se nivelaron después de las plataformas y bajan sus bordes; confirmar en campo el nivel de cada plataforma.',
             'Check: the roads beside the paddocks and the barn were graded after the pads and drop their edges; confirm each pad level on site.', w=52, fs=7.9)
    y = para(fig, 0.745, y, 'Curvas continuas: rasante terminada cada 1 ft. Punteadas: terreno existente. Taludes 3:1 con bordes suaves. Descapotar y guardar la tierra vegetal antes de rellenar.',
             'Solid contours: finished grade every 1 ft. Dashed: existing ground. 3:1 side slopes with soft edges. Strip and stockpile topsoil before filling.', w=52, fs=7.9)
    tblock(fig, nxt(), 'Plano para el operador', 'Operator grading sheet'); PAGES.append(fig)
