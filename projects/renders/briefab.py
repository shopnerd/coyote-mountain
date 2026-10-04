"""Side-by-side brief test (4 Oct 2026, Will: "we almost got better results the first time, just inside the Topo app").
A = the gallery brief as it stands (gallery3.BRIEF + EXTRA, long, rule-heavy).
B = a topo-style brief: short and factual (place, month, time, sky, what is built and how big), the aerial photo of the site as a
    second reference image, people and horses described loosely.
Same model shot, both engines -> briefab/<view>-<A|B>-<engine>.png and a 2 x 2 comparison sheet.

    python briefab.py wash-farrier
"""
import os, sys, threading
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
view = sys.argv[1]; sys.argv = [sys.argv[0], 'google']
import gallery3 as G, paint
from gallery2 import gemini_key
paint.QUAL = 'high'
SRC = os.path.join(HERE, 'model', f'model-{view}.png'); AER = os.path.join(HERE, '..', 'viewer', 'aerial-src.jpg')
OUT = os.path.join(HERE, 'briefab'); os.makedirs(OUT, exist_ok=True)

A = G.BRIEF + G.EXTRA.get(view, '')
TOPO_B = {
 'wash-farrier': (
  'Make the first image a photograph of the real place. October, late afternoon golden hour before sunset, fair-weather cumulus clouds. '
  'The place is Centro Equino, a small horse ranch in the dry granite hills of the Valle de Guadalupe, Baja California; the second image is '
  'the aerial photo of the site, use it for the colours of the ground and scrub. '
  'Built here, drawn as plain solids in the first image: keep each exact shape, size and place. A stone and timber horse stable 72 ft long, '
  'its end room plastered with a wooden plank sliding door; a 12 by 24 ft concrete wash pad in front of it; over the pad a steel pipe pergola '
  '10 ft tall covered by a grapevine with green grapes; a bent black pipe tie hoop in the middle of the pad; a fieldstone water trough 14 ft long '
  'along the pad edge, its water pouring from a stone spout into a small lower stone basin at its end; black steel pipe fences. '
  'Life: a horse tied at the hoop, a farrier and a rider with it, at true scale.'),
}
B = TOPO_B[view]
gk, ok_ = gemini_key(), paint.key('OPENAI_API_KEY')
jobs = [('A', 'google', A, []), ('B', 'google', B, [AER]), ('A', 'openai', A, []), ('B', 'openai', B, [AER])]
res = {}
def run(tag, eng, prompt, refs):
    try:
        im = (paint.google(SRC, prompt, refs, gk) if eng == 'google' else paint.openai(SRC, prompt, refs, ok_))
        p = os.path.join(OUT, f'{view}-{tag}-{eng}.png'); im.save(p); res[(tag, eng)] = p; print(tag, eng, 'ok')
    except Exception as e: print(tag, eng, 'FAILED', str(e)[:160])
th = [threading.Thread(target=run, args=j) for j in jobs]; [t.start() for t in th]; [t.join() for t in th]
open(os.path.join(OUT, f'{view}-B-brief.txt'), 'w', encoding='utf-8').write(B)
cw, ch = 960, 540; sheet = Image.new('RGB', (2 * cw + 30, 2 * ch + 110), '#faf8f3'); d = ImageDraw.Draw(sheet)
try: f = ImageFont.truetype(os.path.join(HERE, '..', 'fonts', 'PJS-Bold.ttf'), 26); f2 = ImageFont.truetype(os.path.join(HERE, '..', 'fonts', 'PJS-Regular.ttf'), 20)
except Exception: f = f2 = None
d.text((10, 8), 'A · brief actual de la galería · current gallery brief', fill='#2a2824', font=f); d.text((cw + 30, 8), 'B · estilo Topo: corto, con la foto aérea · topo-style: short, with the aerial photo', fill='#2a2824', font=f)
for r, eng in enumerate(('google', 'openai')):
    for c, tag in enumerate(('A', 'B')):
        p = res.get((tag, eng))
        if p: im = Image.open(p).convert('RGB'); im.thumbnail((cw, ch)); sheet.paste(im, (c * (cw + 30), 50 + r * (ch + 30)))
        d.text((c * (cw + 30) + 10, 50 + r * (ch + 30) + ch - 30), 'Gemini' if eng == 'google' else 'OpenAI', fill='white', font=f2)
sheet.save(os.path.join(OUT, f'{view}-AB.jpg'), quality=90); print(os.path.join(OUT, f'{view}-AB.jpg'))
