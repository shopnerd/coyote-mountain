import math, numpy as np
exec(open('stalls_0926.py', encoding='utf-8').read().split('# grading:')[0].replace("print(opt,", "0 and print(opt,"))
pal = np.array(palm, float)
def score(ang, tc, sc):   # block centre (tc, sc) in outline frame, rotated ang deg
    a = math.radians(ang); t = pal[:, 0] - tc; s = pal[:, 1] - sc
    bt = t * math.cos(a) + s * math.sin(a); bs = -t * math.sin(a) + s * math.cos(a)   # block frame, centred
    inb = (abs(bt) <= 32) & (abs(bs) <= 26)
    corr = inb & (abs(bs) <= 6); front = inb & (abs(bs) > 6) & (abs(bs) <= 14); back = inb & (abs(bs) > 14)
    return corr.sum(), front.sum(), back.sum()
best = {}
for ang in range(-10, 41, 2):
    for tc in range(16, 76, 2):          # NE end must stay >= ~45 ft off the main road (outline ends at t 134)
        for sc in range(12, 40, 1):
            c, f, b = score(ang, tc, sc)
            for opt, val in (('A', b - 2 * (c + f)), ('B', b + c - 2 * f)):
                if opt not in best or val > best[opt][0]: best[opt] = (val, ang, tc, sc, c, f, b)
for k, v in best.items(): print(k, 'angle', v[1], 'centre t,s', v[2], v[3], '| palms ft2 corridor', v[4], 'roofed fronts', v[5], 'open backs', v[6])
print('as drawn (0, 42, 28):', score(0, 42, 28))
