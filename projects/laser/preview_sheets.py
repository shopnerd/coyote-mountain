"""Render the laser SVG sheets to PNG previews with visible line weights (red cut, blue score, green grid)."""
import glob, os, re
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
files = sorted(glob.glob(os.path.join(OUT, 'centro-equino-site-sheet-*.svg')))
def subpaths(d):
    for part in re.findall(r'M[^M]*', d):
        closed = part.strip().endswith('Z')
        pts = [tuple(map(float, p.split(','))) for p in re.findall(r'-?[\d.]+,-?[\d.]+', part)]
        if closed and pts: pts.append(pts[0])
        yield pts
cols = 4; rows = (len(files) + cols - 1) // cols
fig, axes = plt.subplots(rows, cols, figsize=(cols * 6.4, rows * 3.8), dpi=90)
for ax, fn in zip(axes.flat, files):
    s = open(fn, encoding='utf-8').read()
    for d, col in re.findall(r'<path d="([^"]*)" fill="none" stroke="(#[0-9a-f]+)"', s):
        lw = {'#ff0000': .9, '#0000ff': .5, '#00a000': .3}.get(col, .5)
        for pts in subpaths(d):
            if len(pts) > 1:
                xs, ys = zip(*pts); ax.plot(xs, ys, color=col, lw=lw)
    for x, y, fs, t in re.findall(r'<text x="([\d.]+)" y="([\d.]+)"[^>]*font-size="([\d.]+)"[^>]*>([^<]*)</text>', s):
        ax.text(float(x), float(y), t, fontsize=float(fs) * 18, ha='center', va='baseline')
    ax.add_patch(plt.Rectangle((0, 0), 32, 18, fill=False, ec='#999', lw=.8))
    ax.set_xlim(-.3, 32.3); ax.set_ylim(18.3, -.3); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title(os.path.basename(fn).replace('centro-equino-site-', '').replace('.svg', ''), fontsize=10)
for ax in list(axes.flat)[len(files):]: ax.axis('off')
fig.tight_layout(); fig.savefig(os.path.join(OUT, 'preview-sheets.png'))
print('ok', len(files))
