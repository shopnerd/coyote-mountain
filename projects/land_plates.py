"""The landscape-section page's four plates (12 Oct 2026, Will + Walker: the four sections tagged on the every-render page).
Each plate is cut from its source with ALL of its plants and roots, then padded with its own sky or paper to one shared shape,
so nothing is cropped (Will: "the palms got cropped, all of them should have more root shown"). Plates 3 and 4 sit side by
side, so their ground lines are set to the same height. Writes renders/picks/land-<n>.png for walker_v14_slots.json land-a-*.

    python land_plates.py
"""
import os
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'renders', 'picks')
G = 'G:/My Drive/MEXICO/Chichihaus/2026-09-23 Centro Equino pack/renderings/'
ASPECT = 1090 / 482                                    # the page slots
PLATES = [  # (out, source, content box x0 y0 x1 y1 as fractions, ground row fraction or None, paper/plain plate)
    ('land-1-valley.png', os.path.join(HERE, 'renders', 'picks', 'valley-painted-color.png'), (.052, .07, .992, .752), None, False),
    ('land-2-palms.png', G + '2026-10-11 cortes para Andres · sections for Andres/5-IJ-palmas-de-las-caballerizas.png', (.032, .06, .968, .82), None, False),
    ('land-3-oaks.png', G + '2026-10-11 cortes para Andres · sections for Andres/encinos y nativas, sin enredaderas · oaks and natives, no vines/otros-intentos · other tries - enc-centro-equino-encinos-0-1.png', (.045, .10, .98, .70), .558, False),
    ('land-4-entry.png', os.path.join(HERE, 'renders', 'picks', 'entry-natives-2026-10-12.png'), (.045, .045, .985, .585), .51, True),   # 12 Oct: redrawn, 15 species, no deergrass
]

def fit(c, Hc, Wc, top_pad, paper):
    """Place the content c (h, w, 3) on a Wc x Hc canvas, top_pad rows down, centred across; fill with its own edge colours."""
    h, w = c.shape[:2]; px = (Wc - w) // 2; can = np.empty((Hc, Wc, 3))
    top = np.median(c[:6].reshape(-1, 3), 0) if not paper else np.median(c[:6, int(w * .42):int(w * .47)].reshape(-1, 3), 0)   # the paper at the drawing's top edge, so the padding meets it with no seam
    can[:] = top
    rows = np.median(np.concatenate([c[:, :8], c[:, -8:]], 1), 1) if not paper else np.median(c[:, int(w * .42):int(w * .47)], 1)
    can[top_pad:top_pad + h] = rows[:, None, :]
    if top_pad + h < Hc: can[top_pad + h:] = rows[-1]
    m = np.ones((h, w))
    if paper:                                          # paper plates melt into their padding
        f = 60; r = np.linspace(0, 1, f); m[:, :f] *= r; m[:, -f:] *= r[::-1]; ft = min(220, h // 3); m[:ft] *= np.linspace(0, 1, ft)[:, None]
    else:                                              # painted skies: a short blend at the top edge only
        f = min(40, top_pad); r = np.linspace(0, 1, max(f, 1)); m[:f] *= r[:, None] if f else 1
    reg = can[top_pad:top_pad + h, px:px + w]; can[top_pad:top_pad + h, px:px + w] = c * m[..., None] + reg * (1 - m[..., None])
    if paper: can += np.random.default_rng(3).normal(0, 1.6, can.shape)
    return can

if __name__ == '__main__':
    g34 = None
    for out, src, (x0, y0, x1, y1), gnd, paper in PLATES:
        im = Image.open(src).convert('RGB'); W, H = im.size
        c = np.asarray(im.crop((int(W * x0), int(H * y0), int(W * x1), int(H * y1)))).astype(float); h, w = c.shape[:2]
        if gnd is None:
            Wc = max(w, int(round(h * ASPECT))); Hc = int(round(Wc / ASPECT)); pad = Hc - h      # all padding goes on top (sky)
        else:
            gy = int(H * gnd) - int(H * y0); below = h - gy
            if g34 is None:                            # plate 3 sets the shared ground line
                Wc = w; Hc = max(h, int(round(Wc / ASPECT))); pad = Hc - h; g34 = (pad + gy) / Hc
            else:                                      # plate 4 follows it: ground at the same fraction, roots kept
                Hc = int(round(below / (1 - g34))); Wc = int(round(Hc * ASPECT)); pad = int(round(Hc * g34)) - gy
                if Wc < w: Wc = w; Hc = int(round(Wc / ASPECT)); pad = int(round(Hc * g34)) - gy
        if not paper and w < Wc <= w * 1.05:           # a few % short: stretch the painting across rather than pad its sides with bands
            c = np.asarray(Image.fromarray(c.astype(np.uint8)).resize((Wc, h), Image.LANCZOS)).astype(float); w = Wc
        can = fit(c, Hc, Wc, pad, paper)
        Image.fromarray(can.clip(0, 255).astype(np.uint8)).save(os.path.join(OUT, out))
        print(out, f'{Wc}x{Hc}', f'content {100 * w / Wc:.0f}% wide', '' if gnd is None else f'ground at {(pad + (int(H * gnd) - int(H * y0))) / Hc:.3f}')
