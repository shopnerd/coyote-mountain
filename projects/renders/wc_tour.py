"""Watercolour site tour (6 Oct 2026, Will: 'a long one that is only watercolours ... a site tour ... make sunsets dissolve into
darkness'). Ten watercolour keyframes of the current model, each morphing into the next with Veo 3.1 fast (first + last frame,
8 s), so the washes bleed and spread from one place to the next; the last three share one camera: golden -> dusk -> night.

    python wc_tour.py            (clips already in wc-tour/ are kept; delete one to remake it)
"""
import os, subprocess, sys, time, concurrent.futures as cf
HERE = os.path.dirname(os.path.abspath(__file__)); IMG = os.path.join(HERE, '..', '..', '..', 'will-os', 'equino', 'img'); A = os.path.join(HERE, 'wc-tour')
os.makedirs(A, exist_ok=True)
sys.argv = [sys.argv[0], 'veo']
import morph
import reel as R

KEYS = [   # (name, picture)
 ('dawn',    os.path.join(HERE, 'wc-dawn', 'p4-site-ne-openai.png')),
 ('hill',    os.path.join(IMG, '4-hill-s-watercolor-openai.jpg')),
 ('stable',  os.path.join(IMG, '16-stable-sw-watercolor-openai.jpg')),
 ('aisle',   os.path.join(IMG, '10-stable-aisle-watercolor-openai.jpg')),
 ('wash',    os.path.join(IMG, 'wash-farrier-watercolor-openai.jpg')),
 ('south',   os.path.join(IMG, 'el-south-watercolor-openai.jpg')),
 ('cafe',    os.path.join(IMG, 'cafe-end-watercolor-openai.jpg')),
 ('golden',  os.path.join(HERE, 'wc-golden', '16-stable-sw-openai.png')),
 ('dusk',    os.path.join(HERE, 'wc-dusk', '16-stable-sw-openai.png')),
 ('night',   os.path.join(HERE, 'wc-night-nb21', '16-stable-sw-google.png')),   # 6 Oct: Nano Banana 2.1 made the truest watercolour nocturne
 # 6 Oct (Will): the ending: the topo app's night view (points from the model) painted as glowing contour threads
 ('glow',    os.path.join(HERE, 'night-glow', 'n1-stable-wc.png')),
 ('site',    os.path.join(HERE, 'night-glow', 'n3-site-wc.png')),
]
WC = ('A loose hand-made watercolour painting on cotton paper comes alive and travels: the camera glides slowly and dreamily, and the washes '
      'bleed, spread and bloom wet-in-wet, pigment flowing across the paper, pencil lines appearing and dissolving, until the painting has '
      'become the next scene. It stays a watercolour the whole time, never a photograph. ')
STEP = {'dawn': 'Dawn light spreads over the whole ranch as the camera descends toward the hill.',
        'hill': 'From the hill the camera floats down toward the long stable.',
        'stable': 'The camera glides into the open end of the stable and the aisle opens up inside.',
        'aisle': 'The camera drifts out through the aisle to the wash pad under the grapevine.',
        'wash': 'The camera pulls back along the south side of the stable.',
        'south': 'The camera rises and drifts across the ranch to the cafe and its stone steps.',
        'cafe': 'The light turns deep gold as the camera floats back to the stable at sunset.',
        'golden': 'The sun sets: the gold drains away and washes of rose and violet spread across the sky while the stable lights begin to glow.',
        'dusk': 'Darkness spreads like ink through wet paper: indigo washes flood the sky and the land until only the stable glows amber, a lantern in the night.',
        'night': 'The amber glow cools and spreads: the land dissolves into the dark and is redrawn as glowing threads of light along the contours, violet, teal and gold, while the stable and trees turn to pale moonlit white.',
        'glow': 'The camera rises slowly and pulls back into the night sky until the whole ranch lies below, drawn in glowing contour threads on dark indigo paper, stars blooming.'}

def make(k):
    (a, pa), (b, pb) = KEYS[k], KEYS[k + 1]; out = os.path.join(A, f'{k + 1:02d}-{a}-to-{b}.mp4')
    if os.path.exists(out): return out
    for tries in range(6):
        try: morph.veo(pa, pb, out, WC + STEP[a], 8); return out
        except RuntimeError as e:
            if '429' in str(e) or 'RESOURCE_EXHAUSTED' in str(e): time.sleep(60 * (tries + 1)); continue
            raise

if __name__ == '__main__':
    todo = [k for k in range(len(KEYS) - 1) if os.path.exists(KEYS[k][1]) and os.path.exists(KEYS[k + 1][1])]
    if len(sys.argv) > 2 and sys.argv[2] == 'clips-only': pass
    with cf.ThreadPoolExecutor(3) as ex: clips = list(ex.map(make, todo))
    if len(clips) == len(KEYS) - 1:
        t0, t1 = os.path.join(A, '00-title.mp4'), os.path.join(A, '99-end.mp4')
        R.title(t0, 'Centro Equino', 'en acuarela · in watercolour'); R.title(t1, 'Centro Equino', 'Chichihuas · Baja California')
        R.FADE = 0.5
        R.assemble([t0] + clips + [t1], os.path.join(A, 'centro-equino-watercolour-tour.mp4'))
    else: print('made', len(clips), 'of', len(KEYS) - 1, 'clips; waiting on keyframes')
