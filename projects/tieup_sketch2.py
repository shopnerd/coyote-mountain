"""Tie-up sketch v2 (4 Oct 2026, night): Will's three tie lines across the wash pad, each different. Not placed yet."""
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle as R, Circle as C, FancyBboxPatch, Arc
import sys, textwrap
OUT = sys.argv[1] if len(sys.argv) > 1 else 'tieup-sketch-2.png'
INK, MUTED, CLAY, WATER, STEEL, RUB, WOOD = '#2a2824', '#6a655a', '#b5602e', '#1f78c8', '#4a4f57', '#5a5248', '#8a6a42'
HL, HD, RT = 36.0, 21.0, .75
WALL = -HD - RT; PAD_N, PAD_S = WALL, WALL - 12
fig = plt.figure(figsize=(17, 11), dpi=130); fig.patch.set_facecolor('#faf8f3')
fig.text(.03, .95, 'Amarres en la losa de lavado, v2 · Tie-ups on the wash pad, v2', fontsize=18, weight='bold', color=INK)
fig.text(.03, .915, 'Las tres líneas rojas de Will, cada una distinta · Will’s three red lines, each one different · boceto, nada colocado · sketch, nothing placed · 4 oct 2026', fontsize=10.5, color=MUTED)

# ---------------- plan ----------------
ax = fig.add_axes([0.02, 0.39, 0.56, 0.46]); ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-42, -6); ax.set_ylim(PAD_S - 9, WALL + 9)
ax.add_patch(R((-HL, WALL), 24, 2 * RT, color='#c9b8a0')); ax.add_patch(R((-HL, WALL + 2 * RT), 24, 7, color='#f1ece2'))
ax.text(-30, WALL + 4.6, 'lavado · wash room', ha='center', fontsize=8.5, color=INK); ax.text(-18, WALL + 4.6, 'monturas · tack / feed', ha='center', fontsize=8.5, color=INK)
ax.add_patch(R((-33, WALL - .3), 6, .6 + 2 * RT, color='#faf8f3')); ax.plot([-33, -27], [WALL - .3, WALL - .3], color=INK, lw=1)
ax.text(-30, WALL + .35, 'abertura 6 ft · opening', ha='center', fontsize=6.2, color=MUTED)
# the sliding door PARKED east of the opening (where it lives when the wash room is open): planks on the outside face
ax.add_patch(R((-27, WALL - .55), 7.3, .3, color=WOOD)); ax.text(-23.3, WALL + 2.4, 'puerta corrediza estacionada aquí · sliding door parks here', ha='center', fontsize=6.0, color=WOOD)
ax.plot([-33.5, -19.4], [WALL - .9, WALL - .9], color=STEEL, lw=.8, dashes=(3, 2)); ax.text(-19, WALL - .9, 'riel · track', fontsize=5.6, color=STEEL, va='center')
for x in (-36, -24, -12): ax.add_patch(C((x, WALL + RT), .4, color=STEEL))
ax.add_patch(R((-39, PAD_S - 1.5), 3, 13.5, color=WATER, alpha=.55)); ax.text(-37.5, PAD_S + 5.5, 'bebedero 14 × 3 · trough', ha='center', va='center', fontsize=6.2, color='white', rotation=90)
ax.add_patch(R((-HL, PAD_S), 24, 12, facecolor='#dcd7cd', edgecolor=INK, lw=1.2))
ax.plot([-HL, -12], [PAD_S + .4, PAD_S + .4], color=WATER, lw=2.4); ax.text(-24, PAD_S - 1.1, 'canal con rejilla · trench drain', ha='center', fontsize=6.0, color=WATER, va='top')
# the first south run's west fence = the pad's east edge (x = -12): three-rail pipe fence, posts every 10 ft
for y in (WALL - 1.0, WALL - 11.0): ax.add_patch(C((-12, y), .3, color=STEEL))
ax.plot([-12, -12], [WALL - .3, WALL - 40], color=STEEL, lw=2.2); ax.text(-11.3, PAD_S - 3, 'cerca del corral 1 · run 1 fence\n(tubo negro 5.5 ft · black pipe)', fontsize=6.0, color=STEEL, va='top')
ax.add_patch(R((-12, WALL - 40), 12, 40 - .3, facecolor='#f1ead9', edgecolor=INK, lw=.6, alpha=.5)); ax.text(-6.5, PAD_S - 4, 'corral · run 1', fontsize=6.4, color=MUTED, rotation=90, va='top')
def horse(cx, cy, col='#9a8f7f'):
    ax.add_patch(R((cx - 1.3, cy - 4), 2.6, 8, facecolor=col, edgecolor=INK, lw=.8, alpha=.75)); ax.add_patch(C((cx, cy + 4.3), .9, facecolor=col, edgecolor=INK, lw=.8, alpha=.9))
ring = lambda x, y, c=CLAY: ax.add_patch(C((x, y), .32, facecolor='white', edgecolor=c, lw=1.6, zorder=6))
tie = lambda a, b: ax.plot([a[0], b[0]], [a[1], b[1]], color=CLAY, lw=1.6, dashes=(4, 2), zorder=5)
# the three red lines, drawn faint for reference
for x in (-35.3, -24, -12.7): ax.plot([x, x], [WALL - .6, PAD_S + .6], color='#d33', lw=2.2, alpha=.25)
# W: one ring on the corner post, horse along the west edge, nothing at the tail end
horse(-33.6, PAD_N - 6.0, '#a9b7c6'); ring(-36, WALL - .35); tie((-36, WALL - .35), (-33.6, PAD_N - 1.4))
ax.add_patch(C((-36, WALL - .35), 1.2, fill=False, edgecolor=CLAY, lw=.8, ls=':'))
ax.text(-35.8, WALL + 1.6, 'W', fontsize=10, weight='bold', color=CLAY, ha='center')
# M: a bent-pipe hoop (inverted U) on the centre line, 2 ft off the wall, 8 ft long; a horse can tie to either face
ax.plot([-24, -24], [WALL - 2.0, WALL - 10.0], color=STEEL, lw=5.5, solid_capstyle='round'); ring(-24, WALL - 2.0, STEEL); ring(-24, WALL - 10.0, STEEL)
horse(-26.9, PAD_N - 6.0, '#a9b7c6'); tie((-24, WALL - 3.5), (-26.9, PAD_N - 1.4))
horse(-21.1, PAD_N - 6.0); tie((-24, WALL - 3.5), (-21.1, PAD_N - 1.4))
ax.text(-24, WALL + 1.6, 'M', fontsize=10, weight='bold', color=STEEL, ha='center')
# E: rings on the run fence posts, horse along the east edge
ring(-12, WALL - 1.0, STEEL); horse(-14.4, PAD_N - 6.0); tie((-12, WALL - 1.0), (-14.4, PAD_N - 1.4))
ax.text(-12.2, WALL + 1.6, 'E', fontsize=10, weight='bold', color=STEEL, ha='center')
ax.text(-HL, PAD_S - 1.1, 'losa 12 × 24 · 1.5 % · pad', fontsize=6.0, color=MUTED, va='top')
ax.set_title('Planta · Plan: W una argolla en el poste de la esquina · M arco de tubo doblado en el eje · E la cerca del corral\n'
             'W one ring on the corner post · M a bent-pipe hoop on the centre line · E the run fence itself', fontsize=9.2, color=INK, loc='left')

# ---------------- the hoop, elevation ----------------
hx = fig.add_axes([0.60, 0.39, 0.38, 0.46]); hx.set_aspect('equal'); hx.axis('off'); hx.set_xlim(-2.5, 12.5); hx.set_ylim(-5.0, 9.5)
hx.add_patch(R((-2.5, -3.5), 15, 3.5, color='#dcd7cd')); hx.plot([-2.5, 12.5], [0, 0], color=INK, lw=1)
L, Hh, rb = 8.0, 4.5, 1.0                                                  # 8 ft long, 4.5 ft high, 12 in bend radius
hx.plot([1, 1], [-3, Hh - rb], color=STEEL, lw=7, solid_capstyle='butt'); hx.plot([1 + L, 1 + L], [-3, Hh - rb], color=STEEL, lw=7, solid_capstyle='butt')
hx.plot([1 + rb, 1 + L - rb], [Hh, Hh], color=STEEL, lw=7, solid_capstyle='butt')
hx.add_patch(Arc((1 + rb, Hh - rb), 2 * rb, 2 * rb, theta1=90, theta2=180, color=STEEL, lw=7)); hx.add_patch(Arc((1 + L - rb, Hh - rb), 2 * rb, 2 * rb, theta1=0, theta2=90, color=STEEL, lw=7))
for x in (1, 1 + L): hx.add_patch(R((x - .9, -3.2), 1.8, 3.0, facecolor='#bdb7ab', edgecolor=INK, lw=.7, alpha=.8))
hx.text(1 + L / 2, -1.6, 'patas 3 ft en concreto · legs 3 ft in concrete', ha='center', va='center', fontsize=6.4, color=INK)
hx.add_patch(C((1, Hh - 1.0), .22, facecolor='white', edgecolor=CLAY, lw=1.6)); hx.add_patch(C((1 + L, Hh - 1.0), .22, facecolor='white', edgecolor=CLAY, lw=1.6))
hx.add_patch(C((1 + L / 2, Hh - .35), .22, facecolor='white', edgecolor=CLAY, lw=1.6))
hx.text(1 + L / 2, Hh + .6, f'tubo de 3 in doblado · 3 in pipe, bent · {L:.0f} ft × {Hh:.1f} ft · radio 12 in · 12 in bends', ha='center', fontsize=7.2, color=STEEL)
hx.text(1 + L / 2, -3.4, 'argollas soldadas a 3.5 ft y arriba al centro · welded rings at 3.5 ft and top centre', ha='center', fontsize=6.4, color=CLAY, va='top')
hx.annotate('', xy=(11.6, 0), xytext=(11.6, Hh), arrowprops=dict(arrowstyle='<->', lw=.8, color=INK)); hx.text(11.9, Hh / 2, f'{Hh:.1f} ft', va='center', fontsize=7.5, color=INK)
hx.add_patch(R((3, 0), 4.0, 5.0, facecolor='#9a8f7f', alpha=.35, edgecolor='none')); hx.text(5, 2.5, 'caballo detrás\nhorse behind', ha='center', fontsize=6.6, color=INK)
hx.set_title('M · el arco, visto de frente · the hoop, seen from the aisle side\n(una “C” grande boca abajo · a big upside-down C)', fontsize=9.2, color=INK, loc='left')

# ---------------- notes ----------------
notes = [
 ('W · esquina del bebedero · trough corner', 'Una sola argolla de amarre a 6 ft en el poste de 6 in de la esquina suroeste, nada más: el caballo se para a lo largo del borde oeste de la losa con la cabeza en la esquina y la cola hacia el bebedero. Sin poste ni riel allí, como pidió Will. Amarre alto y corto, con eslabón desprendible. · One tie ring at 6 ft on the 6 in corner post, nothing else: the horse stands along the pad’s west edge, head at the corner, tail toward the trough. No post or rail there, as Will asked. Tie high and short, with a breakaway link.'),
 ('M · el arco en el eje · the hoop on the centre line', 'Tubo de acero de 3 in doblado en “C” boca abajo: 8 ft de largo, 4.5 ft de alto, radios de 12 in, patas 3 ft en el concreto, 2 ft separado del muro para que la puerta corrediza pase detrás. Divide la losa en lavado (oeste) y herraje (este); un caballo a cada lado, atado a las argollas soldadas. · 3 in steel pipe bent into an upside-down C: 8 ft long, 4.5 ft high, 12 in bends, legs 3 ft in concrete, 2 ft off the wall so the sliding door passes behind it. Splits the pad into wash (west) and farrier (east); one horse each side, tied to the welded rings.'),
 ('E · la cerca del corral · the run fence', 'El borde este de la losa es la cerca oeste del corral 1 (tubo negro, 5.5 ft): argollas a 6 ft en sus postes y el caballo se para a lo largo del borde. Nada nuevo que construir. · The pad’s east edge is run 1’s west fence (black pipe, 5.5 ft): rings at 6 ft on its posts and the horse stands along the edge. Nothing new to build.'),
 ('La puerta · the door', 'Con el lavado abierto la puerta queda estacionada al este de la abertura (x -27 a -20), justo donde antes iba el amarre cruzado del muro; por eso los amarres se van a los extremos y al arco, y el muro queda libre. · With the wash room open the door parks east of the opening (x -27 to -20), exactly where the wall cross-ties used to be; so the ties move to the two ends and the hoop, and the wall stays clear.'),
 ('Lo que se mantiene · what stays', 'Losa 12 × 24 con 1.5 % al canal con rejilla; tapetes de hule de borde a borde en la mitad este para el herrador; luz lateral; mangueras en el muro. El herrador trabaja al caballo atado al arco o a la cerca, con 12 ft libres detrás. · 12 × 24 pad falling 1.5 % to the grated trench; rubber mats edge to edge on the east half for the farrier; side light; hose bibs on the wall. The farrier works a horse tied to the hoop or the fence with 12 ft clear behind.'),
]
cols = [fig.add_axes([0.03, 0.03, 0.45, 0.33]), fig.add_axes([0.52, 0.03, 0.45, 0.33])]
for c in cols: c.axis('off')
for col, group in zip(cols, (notes[:3], notes[3:])):
    y = .98
    for h, t in group:
        col.text(0, y, h, fontsize=8.6, weight='bold', color=INK, va='top'); y -= .07
        for line in textwrap.wrap(t, 118): col.text(0, y, line, fontsize=6.6, color=INK, va='top'); y -= .048
        y -= .03
fig.savefig(OUT); print('saved', OUT)
