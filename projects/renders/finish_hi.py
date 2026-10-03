"""High-resolution light finish for print slots (3 Oct): pad a model render to the nearest aspect Gemini takes, paint at 4K
with finish.py's strict brief, crop the pad back off. Keeps the render's own resolution or better.
    python finish_hi.py <view-id> [aspect e.g. 5:4]   ->  finished/<view>-hi-<n>.png
"""
import os, sys, time, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ARGS = sys.argv[1:]; sys.argv = sys.argv[:1] + ["google"]
from PIL import Image
from paint import google
from gallery2 import gemini_key
from finish import BRIEF, SRC, OUT
v = ARGS[0]; ar = ARGS[1] if len(ARGS) > 1 else '5:4'; EXTRA = ' '.join(ARGS[2:]); aw, ah = map(int, ar.split(':'))
im = Image.open(os.path.join(SRC, f'model-{v}.png')).convert('RGB'); W, H = im.size
if W / H < aw / ah:                                   # too tall: pad left/right with stretched edge columns
    W2 = round(H * aw / ah); p = (W2 - W) // 2; c = Image.new('RGB', (W2, H))
    c.paste(im.crop((0, 0, 1, H)).resize((p, H)), (0, 0)); c.paste(im.crop((W - 1, 0, W, H)).resize((W2 - W - p, H)), (p + W, 0)); c.paste(im, (p, 0)); box = (p / W2, 0, (p + W) / W2, 1)
else:
    H2 = round(W * ah / aw); p = (H2 - H) // 2; c = Image.new('RGB', (W, H2))
    c.paste(im.crop((0, 0, W, 1)).resize((W, p)), (0, 0)); c.paste(im.crop((0, H - 1, W, H)).resize((W, H2 - H - p)), (0, p + H)); c.paste(im, (0, p)); box = (0, p / H2, 1, (p + H) / H2)
tmp = os.path.join(tempfile.gettempdir(), f'pad-{v}.png'); c.save(tmp)
n = 1 + sum(1 for g in os.listdir(OUT) if g.startswith(v + '-hi-')); t = time.time()
out = google(tmp, BRIEF + ' The plain stretched bands along the edges are outside the picture: continue the scene naturally there.' + EXTRA, [], gemini_key(), aspect=ar, size='4K')
w, h = out.size; out = out.crop((round(box[0] * w), round(box[1] * h), round(box[2] * w), round(box[3] * h)))
if out.width < W: out = out.resize((W, H), Image.LANCZOS)
out.save(os.path.join(OUT, f'{v}-hi-{n}.png')); print(v, out.size, f'{time.time() - t:.0f}s')
