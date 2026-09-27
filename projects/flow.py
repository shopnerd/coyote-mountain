"""D8 flow on a priority-flood-filled surface, like topo.html's analysis (fillPits + D8 + accumulation).
The drawing export carries the app's flow grid in `__flow`, but it goes stale as soon as the ground is changed
outside the app, so drain.py recomputes it here.

    from flow import flow;  acc, down = flow(z)     # acc in cells, down = downstream node index or -1 at the edge
    python flow.py <export.json>                    # compares against the export's own __flow
"""
import heapq, json, sys, numpy as np

def flow(z):
    H, W = z.shape; zf = z.astype(float).copy(); seen = np.zeros((H, W), bool); pq = []; eps = 1e-5
    for j in range(H):
        for i in range(W):
            if i in (0, W - 1) or j in (0, H - 1): heapq.heappush(pq, (zf[j, i], j, i)); seen[j, i] = True
    while pq:                                             # Barnes priority flood with a small epsilon so flats drain
        h, j, i = heapq.heappop(pq)
        for dj in (-1, 0, 1):
            for di in (-1, 0, 1):
                jj, ii = j + dj, i + di
                if (di or dj) and 0 <= jj < H and 0 <= ii < W and not seen[jj, ii]:
                    seen[jj, ii] = True; zf[jj, ii] = max(zf[jj, ii], h + eps); heapq.heappush(pq, (zf[jj, ii], jj, ii))
    down = -np.ones(H * W, int)
    for j in range(1, H - 1):
        for i in range(1, W - 1):
            best, bn = 0, -1
            for dj in (-1, 0, 1):
                for di in (-1, 0, 1):
                    if not (di or dj): continue
                    s = (zf[j, i] - zf[j + dj, i + di]) / (1.41421356 if di and dj else 1)
                    if s > best: best, bn = s, (j + dj) * W + i + di
            down[j * W + i] = bn
    acc = np.ones(H * W); order = np.argsort(-zf.ravel(), kind='stable')
    for n in order:
        if down[n] >= 0: acc[down[n]] += acc[n]
    return acc.reshape(H, W), down

if __name__ == '__main__':
    p = json.load(open(sys.argv[1], encoding='utf-8')); W, H = p['grid']
    z = np.array(p['z']).reshape(H, W); acc, down = flow(z)
    fl = p.get('__flow')
    if fl:
        d0 = np.array(fl['down']); a0 = np.array(fl['acc']).reshape(H, W)
        inner = np.zeros((H, W), bool); inner[1:-1, 1:-1] = True
        print('same downstream cell: %.1f %%' % (100 * (d0 == down)[inner.ravel()].mean()))
        big = a0 > 50
        print('cells with > 50 upstream: app %d, here %d, overlap %d' % (big.sum(), (acc > 50).sum(), (big & (acc > 50)).sum()))
