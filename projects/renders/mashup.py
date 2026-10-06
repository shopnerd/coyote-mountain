"""Map mash-ups (6 Oct 2026, Will: 'try making a few mashups'): a topo model shot whose ground is a data map (slope, aspect,
elevation colours) painted with the topo app's own 'map mash-up' instruction (topo.html, AI.style 'mashup'), so the data stays
and the living place stands on it.

    python mashup.py <google|openai> <shot.png> [...]      -> mashups/<name>-<engine>.png
"""
import os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ENGINE, SHOTS = sys.argv[1], sys.argv[2:]
sys.argv = [sys.argv[0], ENGINE]
import paint
from paint import openai, google, key
from gallery2 import gemini_key
from PIL import Image
paint.QUAL = 'high'
OUT = os.path.join(HERE, 'mashups'); os.makedirs(OUT, exist_ok=True)

# the topo app's mash-up words, verbatim, plus the scene note
MASH = ('Keep the ground of the first image exactly as it is, colours and lines included, and paint realistic vegetation and cast shadows '
        'standing on it, with buildings only where the first image already shows them and none anywhere else, as if the model had been built '
        'at full size and photographed: a mash-up of the map and the living place.')
NOTE = {'encino-slope': ' Dry hills of northern Baja California: chaparral, oaks in the creases, golden grass; the coloured ground is a slope map.',
        'fonts-aspect': ' Desert badlands in Anza-Borrego: sparse creosote and ocotillo, no trees; the coloured ground is an aspect map.',
        'equino-elev': ' A small horse centre in dry Baja hills: horses in the runs and arena, a few people, pines by the stable; the coloured ground is an elevation map.',
        'sf-elev': ' Downtown San Francisco and its waterfront: street trees, people, boats at the piers, the bay; the coloured ground is an elevation map.'}

if __name__ == '__main__':
    k = key('OPENAI_API_KEY') if ENGINE == 'openai' else gemini_key()
    for shot in SHOTS:
        name = os.path.splitext(os.path.basename(shot))[0]; t = time.time()
        im = Image.open(shot).convert('RGB'); w, h = im.size; hh = round(w * 9 / 16)   # the painters take 16:9
        if h > hh: im = im.crop((0, (h - hh) // 2, w, (h - hh) // 2 + hh))
        src = os.path.join(OUT, name + '-in.png'); im.resize((1536, 864)).save(src)
        try:
            out = (openai if ENGINE == 'openai' else google)(src, MASH + NOTE.get(name, ''), [], k)
            out.save(os.path.join(OUT, f'{name}-{ENGINE}.png')); print(f'{name} {ENGINE}: ok in {time.time() - t:.0f}s')
        except Exception as e: print(f'{name} {ENGINE}: FAILED {str(e)[:160]}')
