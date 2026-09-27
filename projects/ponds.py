"""Where water stands after a rain (27 Sep, Will): the low spots of the current graded ground that have no way out,
found by filling the surface (priority flood, no epsilon). Culverts are treated as open so the ditches pass under the
roads. Grid cells are 2.7 m, so this finds real hollows (the natural sink, pad corners, ditch pockets), not road ruts.

    from ponds import ponds; depth = ponds(d)       # metres of standing water per cell
    python ponds.py                                 # prints the ponds of the current drawing
"""
import heapq, json, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
def ponds(d):
    W, H = d['grid'] if 'grid' in d else (150, 100)
    z = np.array(d['z'], float).reshape(H, W); zc = z.copy()
    for s in d['strokes']:
        if not (s.get('name') or '').startswith('culvert'): continue
        P = np.array(s['pts'], float)[:, :2]
        lo = min(z[int(round(q[1])), int(round(q[0]))] for q in P) - .05
        for a, b in zip(P, P[1:]):
            for t in np.linspace(0, 1, 12):
                i, j = (a + (b - a) * t).round().astype(int)
                if 0 <= i < W and 0 <= j < H: zc[j, i] = min(zc[j, i], lo)
    zf = zc.copy(); seen = np.zeros((H, W), bool); pq = []
    for j in range(H):
        for i in range(W):
            if i in (0, W - 1) or j in (0, H - 1): heapq.heappush(pq, (zf[j, i], j, i)); seen[j, i] = True
    while pq:
        h, j, i = heapq.heappop(pq)
        for dj in (-1, 0, 1):
            for di in (-1, 0, 1):
                jj, ii = j + dj, i + di
                if (di or dj) and 0 <= jj < H and 0 <= ii < W and not seen[jj, ii]:
                    seen[jj, ii] = True; zf[jj, ii] = max(zf[jj, ii], h); heapq.heappush(pq, (zf[jj, ii], jj, ii))
    return zf - zc, zf
if __name__ == '__main__':
    d = json.load(open(os.path.join(HERE, 'centro-equino-2026-09-26-stalls16-nopad.json'), encoding='utf-8'))
    dep, zf = ponds(d); m = dep > .04
    from scipy import ndimage
    lab, n = ndimage.label(m, np.ones((3, 3)))
    cs = 400 / 149
    for k in range(1, n + 1):
        c = lab == k; jj, ii = np.nonzero(c)
        print(f'pond {k}: {c.sum()} cells = {c.sum() * cs * cs:.0f} m2, max {dep[c].max():.2f} m, centre i {ii.mean():.0f} j {jj.mean():.0f}')
