"""Plate 4, 'Nativas de la entrada · Entry natives', redrawn (12 Oct 2026, Will): smaller plants so whole roots show, more species,
no deergrass (not one to encourage), more native bunchgrass. Builds centro-equino-entry.json from centro-equino-roots.json:
one section along the entry drive (the C-D line, stretched to LEN m so the plants draw smaller) with a designed sage-scrub
mix laid along it. Paint it with the topo app's own painter (paper plate mood).

    python entry_plate.py
"""
import json, math, os, random
HERE = os.path.dirname(os.path.abspath(__file__)); cs = 400 / 149
LEN = 26.0                                           # metres of section (was 32): the same plate width holds smaller plants
d = json.load(open(os.path.join(HERE, 'centro-equino-roots.json'), encoding='utf-8'))
(a, b), (c, e) = d['secs'][1]                        # C-D, the entry drive
mx, my = (a + c) / 2, (b + e) / 2; ux, uy = c - a, e - b; n = math.hypot(ux, uy); ux, uy = ux / n, uy / n
half = LEN / 2 / cs; A = [mx - ux * half, my - uy * half]; B = [mx + ux * half, my + uy * half]
d['secs'] = [[A, B]]; d['secI'] = 0; d['sec'] = [A, B]
# clear every plant within 6 m of the line, then lay the mix along it (metres from C, species, years)
def near(t):
    x, y = t['c']; s = ((x - A[0]) * ux + (y - A[1]) * uy); px, py = A[0] + s * ux, A[1] + s * uy
    return -2 <= s * cs <= LEN + 2 and math.hypot(x - px, y - py) * cs < 6
d['strokes'] = [s for s in d['strokes'] if not (s.get('kind') == 'tree' and near(s))]
MIX = ['yucca', 'GRASS1', 'sage', 'needlegrass', 'buckwheat', 'clevesage', 'GRASS2', 'dudleya', 'blacksage', 'needlegrass',
       'rabbitbrush', 'munzsage', 'wildrye', 'shawagave', 'sagebrush', 'GRASS1', 'malva', 'needlegrass']
GR = [k for k in ('foothillneedle', 'melic') if k in open(os.path.join(HERE, '..', 'roots-data.js'), encoding='utf-8').read()]
rnd = random.Random(12); x = 1.2
for sp in MIX:
    sp = {'GRASS1': GR[0] if GR else 'needlegrass', 'GRASS2': GR[-1] if GR else 'needlegrass'}[sp] if sp.startswith('GRASS') else sp
    s = x / cs; off = rnd.uniform(-.6, .6) / cs
    gi, gj = A[0] + ux * s - uy * off, A[1] + uy * s + ux * off
    d['strokes'].append({'color': 'ink', 'shape': False, 'kind': 'tree', 'c': [gi, gj], 'r': 1.0, 'sp': sp, 'age': 15, 'grow': False,
                         'w': 1, 'a': 1, 'dash': False, 'pts': [[gi, gj, None]]})
    x += (LEN - 2.4) / (len(MIX) - 1)
d['records']['roots'] = {'on': True, 'ink': 'color', 'layout': 'slope', 'look': 'massing', 'people': 'none', 'back': False, 'mixed': False}
json.dump(d, open(os.path.join(HERE, 'centro-equino-entry.json'), 'w', encoding='utf-8'))
print('section', round(LEN, 1), 'm,', len(MIX), 'plants; grasses', GR or ['needlegrass only'])
