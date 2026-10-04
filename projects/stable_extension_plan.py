# 4 Oct 2026 (Will, after seeing the stand-alone electrical room in the model): fold the electrical room into the stable and add a
# bathroom and a small kitchen. Proposal A: one more 12 ft bay at the WEST (road) end, 72 -> 84 ft, rooms at both new corners.
# Plan in the stable's existing frame (ft, x east along the aisle, y north; old walls x -36..36), so nothing east of x -36 moves.
#   python stable_extension_plan.py  ->  stable-extension-plan.png
import math, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle as R, Circle as C, FancyBboxPatch, Arc
INK, MUTED, CLAY, NEW, STONE, DIRT, CONC, WATER, POW = '#2a2824', '#6a655a', '#b5602e', '#f3d9b8', '#cdb892', '#efe6d2', '#ddd8cf', '#1f78c8', '#6a3d9a'
import glob, matplotlib.font_manager as fm
for _f in glob.glob('fonts/PJS-*.ttf'): fm.fontManager.addfont(_f)
plt.rcParams['font.family'] = ['Plus Jakarta Sans', 'DejaVu Sans']
fig = plt.figure(figsize=(17, 11), dpi=150); fig.patch.set_facecolor('#faf8f3')
ax = fig.add_axes([0.02, 0.06, 0.64, 0.84]); ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-104, 47); ax.set_ylim(-46, 50)
W0, E0, HD, AI = -48, 36, 21, 7
# runs (stubs), pad, trellis, troughs
for k in range(6): ax.add_patch(R((-36 + 12 * k, HD), 12, 18, fc='#f1ead9', ec=INK, lw=.6)); ax.text(-30 + 12 * k, HD + 12, 'corral\nrun', ha='center', va='center', fontsize=6.5, color=MUTED)
for k in range(4): ax.add_patch(R((-12 + 12 * k, -HD - 18), 12, 18, fc='#f1ead9', ec=INK, lw=.6)); ax.text(-6 + 12 * k, -HD - 12, 'corral\nrun', ha='center', va='center', fontsize=6.5, color=MUTED)
ax.add_patch(R((-36, -HD - .75 - 12), 24, 12, fc=CONC, ec=INK, lw=.7)); ax.add_patch(R((-36, -HD - .75 - 12), 24, 12, fill=False, ec='#3a3f44', lw=1, ls=(0, (3, 2))))
ax.text(-24, -HD - 7.5, 'losa de lavado + parra\nwash pad + grape trellis', ha='center', va='center', fontsize=7, color=MUTED)
ax.add_patch(R((-39, -36.75), 3, 13.5, fc='#a9c6dc', ec=INK, lw=.6))
# the building: rock wall outline 84 x 42, the new bay tinted
ax.add_patch(R((W0, -HD), E0 - W0, 2 * HD, fc=DIRT, ec=INK, lw=2.4))
ax.add_patch(R((W0, -HD), 12, 2 * HD, fc=NEW, ec='none'))
ax.add_patch(R((W0, -AI), E0 - W0, 2 * AI, fc='#f7f1e3', ec='none'))
ax.text(-6, 0, 'pasillo · aisle 14 ft', ha='center', va='center', fontsize=9, color=MUTED)
for k in range(6): ax.add_patch(R((-36 + 12 * k, AI), 12, HD - AI, fc='none', ec=INK, lw=.6)); ax.text(-30 + 12 * k, 14, f'{k + 1}\ncaballeriza\nstall', ha='center', va='center', fontsize=6.8)
for k in range(4): ax.add_patch(R((-12 + 12 * k, -HD), 12, HD - AI, fc='none', ec=INK, lw=.6)); ax.text(-6 + 12 * k, -14, f'{k + 7}\ncaballeriza\nstall', ha='center', va='center', fontsize=6.8)
def room(x0, y0, w, h, es, en, fc=CONC, lw=1.4, fs=7.6):
    ax.add_patch(R((x0, y0), w, h, fc=fc, ec=INK, lw=lw)); ax.text(x0 + w / 2, y0 + h / 2, f'{es}\n{en}', ha='center', va='center', fontsize=fs, weight='bold')
room(-36, -HD, 12, HD - AI, 'lavado', 'wash'); room(-24, -HD, 12, HD - AI, 'monturas\ny alimento', 'tack / feed')
# NEW rooms
ax.add_patch(R((W0, AI), 12, HD - AI, fc='#fbe7cc', ec=CLAY, lw=2.2)); ax.annotate('COCINA · kitchen\n12 × 14 ft', xy=(-46, 13.5), xytext=(-74, 13.5), fontsize=8.5, weight='bold', color=CLAY, ha='right', va='center', arrowprops=dict(arrowstyle='-', color=CLAY, lw=.8))
ax.add_patch(R((W0 + .8, 17.6), 10.4, 2.4, fc='white', ec=INK, lw=.6)); ax.add_patch(R((W0 + .8, 8.6), 2.4, 9, fc='white', ec=INK, lw=.6))   # L counter, north + west walls
ax.add_patch(C((-41.5, 18.8), .7, fc='#cfe3f3', ec=INK, lw=.5)); ax.add_patch(R((-38.6, 17.6), 2.4, 2.4, fc='#e9e9e9', ec=INK, lw=.6)); ax.text(-37.4, 18.8, 'R', fontsize=5.5, ha='center', va='center')
ax.add_patch(R((W0 + 1.1, 11.0), 1.8, 1.8, fc='none', ec=INK, lw=.5)); ax.text(W0 + 2, 11.9, '◦◦', fontsize=5, ha='center', va='center')
ax.add_patch(C((-40.5, 10.4), 1.6, fc='white', ec=INK, lw=.6))                                           # small table
ax.add_patch(R((W0, -HD), 12, 6, fc='#e9e2f2', ec=POW, lw=2.2)); ax.annotate('CUARTO ELÉCTRICO · electrical\n12 × 6 ft, puerta exterior · outside door', xy=(-49, -19.5), xytext=(-74, -19.5), fontsize=8.0, weight='bold', color=POW, ha='right', va='center', arrowprops=dict(arrowstyle='-', color=POW, lw=.8))
for x, t in ((-45.5, 'MP'), (-42, 'INV'), (-38.5, 'BAT')): ax.add_patch(R((x - 1.4, -15.9), 2.8, .9, fc='white', ec=POW, lw=.7)); ax.text(x, -16.9, t, fontsize=5, color=POW, ha='center', va='top')
ax.add_patch(R((W0, -15), 12, 8, fc='#d9eef7', ec=WATER, lw=2.2)); ax.annotate('BAÑO · bathroom\n12 × 8 ft, accesible + regadera · shower', xy=(-47, -11), xytext=(-74, -10.5), fontsize=8.0, weight='bold', color=WATER, ha='right', va='center', arrowprops=dict(arrowstyle='-', color=WATER, lw=.8))
ax.add_patch(R((-46.9, -14.4), 3.2, 3.2, fc='white', ec=INK, lw=.5)); ax.plot([-46.9, -43.7], [-14.4, -11.2], color=INK, lw=.4)   # shower
ax.add_patch(matplotlib.patches.Ellipse((-38.8, -13.4), 1.5, 2.1, fc='white', ec=INK, lw=.5)); ax.add_patch(R((-37.4, -10.9), .9, 2.6, fc='white', ec=INK, lw=.5))   # WC, basin
# doors (gaps + swings)
def door(x, y, w, horiz=True, col=INK, swing=1):
    if horiz: ax.add_patch(R((x, y - .45), w, .9, fc='white', ec='none', zorder=5)); ax.add_patch(Arc((x, y), 2 * w, 2 * w, theta1=0 if swing > 0 else 270, theta2=90 if swing > 0 else 360, color=col, lw=.7, zorder=6)); ax.plot([x, x], [y, y + swing * w], color=col, lw=1, zorder=6)
    else: ax.add_patch(R((x - .45, y), .9, w, fc='white', ec='none', zorder=5)); ax.add_patch(Arc((x, y), 2 * w, 2 * w, theta1=0, theta2=90, color=col, lw=.7, zorder=6)); ax.plot([x, x + w], [y, y], color=col, lw=1, zorder=6)
door(-40, AI, 3, swing=1, col=CLAY); door(-40, -AI, 3, swing=-1, col=WATER); door(W0, -20.5, 3, horiz=False, col=POW)
# big sliding doors at both ends (parked along the gable), windows
for xg in (W0, E0):
    ax.add_patch(R((xg - 1, -AI), 2, 2 * AI, fc='white', ec='none'))
    for s in (-1, 1): ax.add_patch(R((xg + (-.8 if xg < 0 else .3), s * AI + (0 if s > 0 else -7.5)), .5, 7.5, fc='#8a6a48', ec=INK, lw=.4))
ax.plot([W0, W0], [15.2, 20], color='#9fd0ea', lw=4, solid_capstyle='butt'); ax.text(W0 - 1.2, 18.6, 'ventana · window', fontsize=6, ha='right', va='center', color=MUTED)
# posts on the 12 ft grid, 8 truss lines now
for x in range(W0, E0 + 1, 12):
    for y in (-HD, HD): ax.add_patch(C((x, y), .55, fc='#3a3f44', ec=INK, lw=.4, zorder=7))
    ax.plot([x, x], [-HD, HD], color='#3a3f44', lw=.4, ls=(0, (2, 3)))
# outside: C1 moved, septic downhill NW, the road arriving at the west door
ax.add_patch(R((-66.5, -41.5), 13, 13, fc='none', ec=WATER, lw=1.2, ls=(0, (3, 2)))); ax.text(-60, -35, 'C1\n40 m³', ha='center', va='center', fontsize=7.5, color=WATER, weight='bold')
ax.text(-68, -35, 'cisterna C1, se corre ~10 ft\nC1 cistern, shifts ~10 ft', fontsize=6.8, color=WATER, ha='right', va='center')
ax.add_patch(R((-70, 26), 10, 6, fc='#e8e2d6', ec=INK, lw=1)); ax.text(-65, 29, 'fosa séptica\nseptic tank', ha='center', va='center', fontsize=6)
ax.plot([-48, -60], [12, 28], color='#7a5c3a', lw=1.1, ls=(0, (4, 2)))
ax.annotate('', xy=(-88, 44), xytext=(-71, 32), arrowprops=dict(arrowstyle='-|>', color='#7a5c3a', lw=1.1)); ax.text(-86, 45, 'campo de infiltración cuesta abajo · leach field, downhill NW', fontsize=7, color='#7a5c3a', ha='left', va='center')
ax.add_patch(R((-104, -4), 55, 8, fc='#e4d6b8', ec='none', zorder=0)); ax.text(-102, 0, 'camino de entrada · entry drive →', fontsize=7.5, color=MUTED, va='center')
# dims
ax.annotate('', xy=(W0, 43), xytext=(E0, 43), arrowprops=dict(arrowstyle='<->', lw=.8)); ax.text(-6, 44, '84 ft (25.6 m) · 7 crujías de 12 ft · 7 bays of 12 ft', ha='center', va='bottom', fontsize=8.5)
ax.annotate('', xy=(W0, 39), xytext=(-36, 39), arrowprops=dict(arrowstyle='<->', lw=.8, color=CLAY)); ax.text(-42, 37.5, '+12 ft nuevo · new', ha='center', va='top', fontsize=7.5, color=CLAY, weight='bold')
ax.annotate('', xy=(E0 + 3, -HD), xytext=(E0 + 3, HD), arrowprops=dict(arrowstyle='<->', lw=.8)); ax.text(E0 + 4, 0, '42 ft', va='center', fontsize=8.5)
ax.text(-102, -44, '←  oeste · camino', fontsize=8.5, weight='bold'); ax.text(46, -44, 'este · estacionamiento  →', fontsize=8.5, weight='bold', ha='right')
na = math.radians(24.16); ax.annotate('', xy=(42 + 6 * math.sin(na), 26 + 6 * math.cos(na)), xytext=(42, 26), arrowprops=dict(arrowstyle='-|>', lw=1.2)); ax.text(42 + 8.5 * math.sin(na), 26 + 8.5 * math.cos(na), 'N', fontsize=9, weight='bold', ha='center')
# side panel
px = 0.68
fig.text(px, 0.93, 'ESTABLO AMPLIADO · PROPUESTA A', fontsize=17, weight='bold', color=INK)
fig.text(px, 0.905, 'Enlarged stable · option A (recommended)', fontsize=12, color='#555')
import textwrap
y = 0.865
for h, en in [
 ('Una crujía más al oeste: 72 → 84 ft', 'One more 12 ft bay at the WEST (road) end, on the same grid, rock and sticks. Everything east of the old west wall stays where it is: the 10 stalls and runs, the wash pad and trellis, the east trough, the clerestory (it stays over the horses).'),
 ('Cocina · Kitchen, NW corner', '12 × 14 ft: L counter with sink and induction top, fridge, a small table; window on the west gable looking down the entry drive; door to the aisle. Coffee for riders and visitors, the hub at the arrival.'),
 ('Baño · Bathroom, SW corner', '12 × 8 ft, one accessible room with toilet, basin and a shower, door to the aisle. Shares a wet wall with the wash room; water heater here.'),
 ('Cuarto eléctrico · Electrical room, the very corner', '12 × 6 ft beside the wash room’s neighbour, its own outside door on the west gable (clear of the parked sliding door), so the main panel, inverter and battery and the firefighters’ shut-off are reached from outside. Dry, closed in cob, no hay nearby. The stand-alone hut goes.'),
 ('Agua y drenaje · Water and drainage', 'All the plumbing at one end (wash, bath, kitchen). The ground falls to the north-west: a septic tank off the kitchen corner and a leach field downhill, at least 15 m from troughs and cisterns (perc test on site). Cistern C1 shifts about 10 ft south-west to clear the new wall.'),
 ('Lo que cambia · What else changes', 'Roof 88 × 46 with overhangs; 8 truss lines; the rooms close the west corners in straw bale or plastered cob like wash and tack, so the west gable reads more solid with the big doors in the middle. Site: the planting rows by the gable shorten a little; the long trough stays 50 ft out. Pack: stable plan, structure, E-1, D-3 and the model all updated together.'),
 ('Otras opciones · Other options', 'B: the extra bay at the EAST end, by the parking (closer for visitors, but the plumbing splits from the wash room and it crowds the east trough and runs). C (no extension, give up a stall) is ruled out: stalls are the rent (Will, 4 Oct).'),
]:
    fig.text(px, y, h, fontsize=10, weight='bold', color=CLAY if 'Lo que' not in h and 'Otras' not in h else INK); y -= .02
    for line in textwrap.wrap(en, 66): fig.text(px, y, line, fontsize=8.6, color=INK); y -= .0165
    y -= .012
fig.text(px, 0.05, 'Propuesta para revisar, 4 oct 2026 · Proposal for review', fontsize=8.5, color=MUTED)
fig.savefig('stable-extension-plan.png', dpi=150); print('ok', round(y, 3))
