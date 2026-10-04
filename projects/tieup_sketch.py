"""Sketch (not placed): tie-up / cross-tie / farrier bay on the stable's wash pad, two options (4 Oct 2026, Will)."""
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle as R, Circle as C
import sys, textwrap
OUT = sys.argv[1] if len(sys.argv) > 1 else 'tieup-sketch.png'
INK, MUTED, CLAY, WATER, STEEL, RUB = '#2a2824', '#6a655a', '#b5602e', '#1f78c8', '#4a4f57', '#5a5248'
HL, HD, RT = 36.0, 21.0, .75
WALL = -HD - RT; PAD_N, PAD_S = WALL, WALL - 12
fig = plt.figure(figsize=(17, 11), dpi=130); fig.patch.set_facecolor('#faf8f3')
fig.text(.03, .95, 'Amarre y herraje en la losa de lavado · Tie-up and farrier bay on the wash pad', fontsize=18, weight='bold', color=INK)
fig.text(.03, .915, 'Boceto para decidir, nada colocado aún · Sketch to decide, nothing placed yet · 4 oct 2026', fontsize=11, color=MUTED)

def plan(ax, opt):
    ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-41, -9); ax.set_ylim(PAD_S - 13, WALL + 8)
    ax.add_patch(R((-HL, WALL), 24, 2 * RT, color='#c9b8a0'))
    ax.add_patch(R((-HL, WALL + 2 * RT), 24, 6, color='#f1ece2'))
    ax.text(-30, WALL + 4.2, 'lavado · wash room', ha='center', fontsize=8, color=INK); ax.text(-18, WALL + 4.2, 'monturas · tack / feed', ha='center', fontsize=8, color=INK)
    ax.add_patch(R((-33, WALL - .3), 6, .6 + 2 * RT, color='#faf8f3')); ax.plot([-33, -27], [WALL - .3, WALL - .3], color=INK, lw=1)
    ax.text(-30, WALL + .55, 'puerta 6 ft · door', ha='center', fontsize=6.4, color=MUTED)
    for x in (-36, -24, -12): ax.add_patch(C((x, WALL + RT), .4, color=STEEL))
    ax.text(-36, WALL + 2.0, 'postes 6 in · 6 in posts', fontsize=6.2, color=STEEL, ha='left')
    ax.add_patch(R((-39, PAD_S - 1.5), 3, 13.5, color=WATER, alpha=.55)); ax.text(-37.5, PAD_S + 5.5, 'bebedero 14 × 3', ha='center', va='center', fontsize=6.4, color='white', rotation=90)
    ax.add_patch(R((-HL, PAD_S), 24, 12, facecolor='#dcd7cd', edgecolor=INK, lw=1.2))
    ax.plot([-HL, -12], [PAD_S + .4, PAD_S + .4], color=WATER, lw=2.4)
    def horse(cx, cy, col='#9a8f7f'):
        ax.add_patch(R((cx - 1.3, cy - 4), 2.6, 8, facecolor=col, edgecolor=INK, lw=.8, alpha=.75)); ax.add_patch(C((cx, cy + 4.3), .9, facecolor=col, edgecolor=INK, lw=.8, alpha=.9))
    tie = lambda a, b: ax.plot([a[0], b[0]], [a[1], b[1]], color=CLAY, lw=1.6, dashes=(4, 2))
    ring = lambda x, y: ax.add_patch(C((x, y), .32, facecolor='white', edgecolor=CLAY, lw=1.5, zorder=5))
    if opt == 'A':
        ax.set_title('A · argollas en los postes del muro + riel de amarre pesado al borde sur\nrings on the wall posts + heavy hitching rail at the south edge   (recomendado · recommended)', fontsize=9, color=INK, loc='left')
        ax.add_patch(R((-24, PAD_S - 4), 12, 4, facecolor='#dcd7cd', edgecolor=INK, lw=1.2, ls='--'))
        ax.add_patch(R((-23.6, PAD_S - 3.6), 11.2, 15.2, facecolor=RUB, alpha=.22, edgecolor='none'))
        horse(-18, PAD_N - 6.2); tie((-24, WALL - .3), (-18, PAD_N - 1.4)); tie((-12, WALL - .3), (-18, PAD_N - 1.4)); ring(-24, WALL - .3); ring(-12, WALL - .3)
        horse(-30, PAD_N - 6.2, '#a9b7c6'); tie((-36, WALL - .3), (-30, PAD_N - 1.4)); ring(-36, WALL - .3)
        ax.plot([-28, -20], [PAD_S - 1.0, PAD_S - 1.0], color=STEEL, lw=6, solid_capstyle='round'); ring(-28, PAD_S - 1.0); ring(-20, PAD_S - 1.0)
        ax.text(-31, PAD_S - 8.6, 'lavado · wash bay 12 × 12\nmangueras en el muro\nhose bibs on the wall', ha='center', fontsize=6.6, color=INK, va='top')
        ax.text(-18, PAD_S - 8.6, 'herraje · farrier bay 12 × 16\n+4 ft de losa, tapetes de borde a borde\n+4 ft of pad, mats edge to edge', ha='center', fontsize=6.6, color=INK, va='top')
        ax.text(-24, PAD_S - 5.4, 'riel 3 in a 42 in · postes 4 in, 3 ft en concreto · argollas a 5.5 ft\n3 in rail at 42 in · 4 in posts 3 ft in concrete · rings at 5.5 ft', ha='center', fontsize=6.2, color=STEEL, va='top', bbox=dict(boxstyle='round,pad=.2', fc='#faf8f3', ec='none'))
    else:
        ax.set_title('B · marco de acero sobre la losa, el caballo mira al bebedero\nfree-standing steel cross-tie frame on the pad, horse facing the trough', fontsize=9, color=INK, loc='left')
        ax.add_patch(R((-35.6, PAD_S + .5), 23.2, 11.1, facecolor=RUB, alpha=.2, edgecolor='none'))
        for x in (-33, -21): ax.add_patch(C((x, PAD_S + .7), .4, color=STEEL))
        ax.plot([-33, -21], [PAD_S + .7, PAD_S + .7], color=STEEL, lw=2.6, dashes=(1, 1.2))
        ax.add_patch(R((-28.3, PAD_S + 1.6), 2.6, 8, facecolor='#a9b7c6', edgecolor=INK, lw=.8, alpha=.75)); ax.add_patch(C((-27, PAD_S + 1.3), .9, facecolor='#a9b7c6', edgecolor=INK, lw=.8))
        tie((-33, PAD_S + .7), (-27, PAD_S + 1.8)); tie((-21, PAD_S + .7), (-27, PAD_S + 1.8)); ring(-33, PAD_S + .7); ring(-21, PAD_S + .7)
        ax.text(-27, PAD_N - 1.2, 'cola a 2 ft del muro · tail 2 ft off the wall', ha='center', fontsize=6.4, color=MUTED)
        horse(-18, PAD_N - 6.2); tie((-24, WALL - .3), (-18, PAD_N - 1.4)); tie((-12, WALL - .3), (-18, PAD_N - 1.4)); ring(-24, WALL - .3); ring(-12, WALL - .3)
        ax.text(-27, PAD_S - 5.4, 'marco: postes 4 in a 12 ft, viga a 8 ft, argollas a 6 ft\nframe: 4 in posts 12 ft apart, beam at 8 ft, rings at 6 ft', ha='center', fontsize=6.2, color=STEEL, va='top')
        ax.text(-18, PAD_S - 8.6, 'segundo caballo en las argollas del muro\nsecond horse on the wall rings', ha='center', fontsize=6.6, color=INK, va='top')
    ax.text(-12.2, PAD_S - .9, 'canal con rejilla → bebedero / zanja\ntrench drain → trough / ditch', ha='right', fontsize=6.0, color=WATER, va='top') if opt == 'B' else None
    ax.text(-HL, PAD_S - .9, 'losa 12 × 24 · 1.5 %\npad, falls to the drain', fontsize=6.0, color=MUTED, va='top')

ax1 = fig.add_axes([0.02, 0.44, 0.31, 0.42]); plan(ax1, 'A')
ax2 = fig.add_axes([0.345, 0.44, 0.31, 0.42]); plan(ax2, 'B')
sx = fig.add_axes([0.67, 0.44, 0.31, 0.42]); sx.set_aspect('equal'); sx.axis('off'); sx.set_xlim(-2, 16); sx.set_ylim(-3.5, 13)
sx.add_patch(R((-2, -3.5), 18, 3.5, color='#dcd7cd')); sx.plot([-2, 16], [0, 0], color=INK, lw=1)
sx.add_patch(R((13, 0), 1.5, 12, color='#c9b8a0')); sx.text(13.75, 12.4, 'muro · wall', ha='center', fontsize=7, color=MUTED)
sx.add_patch(R((1.0, -3), .33, 8.5, color=STEEL)); sx.add_patch(R((.3, 3.3), 1.7, .3, color=STEEL))
sx.text(1.2, 8.9, 'poste 4 in\n3 ft en concreto\n4 in post, 3 ft in', ha='center', fontsize=6.6, color=STEEL)
for yv, t in ((3.5, '42 in · riel · rail'), (5.5, '5.5 ft · argolla del poste · post ring'), (6.0, '6 ft · argolla del muro · wall ring')):
    sx.plot([2.2, 12.6], [yv, yv], color=CLAY, lw=.8, dashes=(2, 2)); sx.text(7.4, yv + .15, t, ha='center', fontsize=6.6, color=CLAY)
sx.add_patch(C((1.17, 5.5), .22, facecolor='white', edgecolor=CLAY, lw=1.4)); sx.add_patch(C((12.8, 6.0), .22, facecolor='white', edgecolor=CLAY, lw=1.4))
sx.add_patch(R((4.5, 0), 5.5, 5.2, facecolor='#9a8f7f', alpha=.6, edgecolor=INK, lw=.8)); sx.text(7.25, 2.6, 'cruz 5 ft\nwithers 5 ft', ha='center', fontsize=6.8, color='white')
sx.plot([1.17, 7.25], [5.5, 6.3], color=CLAY, lw=1.6, dashes=(4, 2)); sx.plot([12.8, 7.25], [6.0, 6.3], color=CLAY, lw=1.6, dashes=(4, 2))
sx.set_title('Sección · Section: alturas de amarre · tie heights', fontsize=9, color=INK, loc='left')
notes = [
 ('Amarre cruzado · Cross-ties', 'Dos cuerdas a los lados de la cabeza, 10–12 ft entre anclajes, argollas a la altura de la cruz + 6 in (≈6 ft), siempre a un poste estructural, nunca a un riel; gancho de liberación rápida en el muro y eslabón desprendible. · Two lines either side of the head, anchors 10–12 ft apart, rings at withers + 6 in (≈6 ft), always on a structural post, never a rail; quick-release at the wall end and a breakaway link.'),
 ('Herraje · Farrier bay', 'Piso nivelado, seco y antiderrapante; tapetes de hule de borde a borde (una pezuña en el borde de un tapete arranca clavos); 12 × 16 a 12 × 18 ft para estirar la pata trasera sin pegar en el muro; luz lateral a la altura de la cintura, no solo arriba; sombra; acceso de camioneta. · Level, dry, non-slip; mats edge to edge; 12 × 16 to 12 × 18 ft so a hind leg stretches back clear of the wall; side light at waist height; shade; truck access.'),
 ('Lavado · Wash bay', 'Mínimo 10 × 12, mejor 12 × 14; concreto escobillado antiderrapante, 1–2 % a un canal con rejilla; manguera fría y caliente en el muro; nada que sobresalga a la altura del caballo. · 10 × 12 minimum, 12 × 14 better; broom-finish concrete, 1–2 % to a grated trench; hot and cold bibs on the wall; nothing protruding at horse height.'),
 ('Amarre sencillo · Single tie', 'Alto y corto, a un poste de 4 in enterrado 3 ft en concreto o a una argolla a 6 ft; un riel de 3 in a 42 in sirve para el amarre rápido del día a día. · High and short, to a 4 in post set 3 ft in concrete or a ring at 6 ft; a 3 in rail at 42 in serves everyday quick tying.'),
 ('Por qué A · Why A', 'La losa ya tiene 12 ft de fondo y tres postes de 6 in en la línea del muro: las argollas van ahí sin estructura nueva; el riel pesado al borde sur es el amarre “en medio de la losa” sin estorbar la manguera; 4 ft más de losa dan el espacio del herrador. B pone al caballo de cara al bebedero, bonito en los renders, pero la cola queda a 2 ft del muro. · The pad is already 12 ft deep with three 6 in posts in the wall line: the rings go there with no new structure; the heavy rail at the south edge is the “tie in the middle of the slab” without being in the hose’s way; 4 more ft of pad give the farrier room. B faces the horse to the trough, pretty in renders, but leaves the tail 2 ft from the wall.'),
]
cols = [fig.add_axes([0.03, 0.03, 0.45, 0.37]), fig.add_axes([0.52, 0.03, 0.45, 0.37])]
for c in cols: c.axis('off')
for col, group in zip(cols, (notes[:3], notes[3:])):
    y = .98
    for h, t in group:
        col.text(0, y, h, fontsize=8.6, weight='bold', color=INK, va='top'); y -= .06
        for line in textwrap.wrap(t, 120): col.text(0, y, line, fontsize=6.6, color=INK, va='top'); y -= .042
        y -= .025
fig.savefig(OUT); print('saved', OUT)
