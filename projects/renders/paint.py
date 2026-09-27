"""Paint the money shots from the control views (shoot.mjs), the way topo.html's painter does: an image-to-image edit
with the aerial photo as the colour reference. OpenAI (gpt-image-2, letterboxed to 1536 x 1024 and cropped back) or
Google (gemini image). Keys come from the user-scope env vars; nothing is printed.

    python paint.py [openai|google] [quality: medium|high] [view-id ...]   ->  out/<view>-<engine>-<n>.png
"""
import base64, io, json, os, subprocess, sys, time, requests
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); CTL = os.path.join(HERE, 'ctl'); OUT = os.path.join(HERE, 'out'); os.makedirs(OUT, exist_ok=True)
ENGINE = sys.argv[1] if len(sys.argv) > 1 else 'openai'; QUAL = sys.argv[2] if len(sys.argv) > 2 else 'medium'; ONLY = sys.argv[3:]

def key(name):
    v = os.environ.get(name)
    if not v and os.name == 'nt':
        v = subprocess.run(['powershell', '-NoProfile', '-Command', f"[Environment]::GetEnvironmentVariable('{name}','User')"], capture_output=True, text=True).stdout.strip()
    return v or None

SCENE = (' Golden hour: the sun is low in the west about half an hour before sunset, warm golden light, long soft shadows and glowing rim light on the '
         'buildings, fences and horses; the sky is full of big puffy cumulus clouds lit gold, peach and pink against clear blue. '
         'This is a small equestrian centre in the Valle de Guadalupe, Baja California, in the dry season: golden grass, olive-green scrub and '
         'granite boulders on the hills, vineyard rows in the valley beyond. '
         'The long low building whose roof dips to a valley along its middle (a butterfly roof) is a set of covered horse stalls: two rows of open '
         'stalls made of white-painted steel pipe panels, facing a sand corridor under a light grey corrugated metal butterfly roof on slim steel posts; '
         'the roof is a butterfly roof: V-shaped in cross-section, its two halves slope DOWN toward the middle so the centre line over the corridor is the LOWEST part and the two outer edges are the highest; never a peaked or gabled roof. The back part of every stall is open to the sky, and several tall date palms with full green crowns stand in and around the open stall backs. Horses (bay, chestnut, grey) stand in about half of the stalls. '
         'At its south-west end a round galvanised stock-water trough sits directly on the ground, fed from above by a short open metal chute that sticks out from the roof valley; nothing stands under the chute: no pole, no post, no pipe, no stand, no downspout. '
         'The larger building is the main stable: stacked fieldstone walls to about 4.5 ft with horizontal wooden stakes above, under a sky-blue metal roof. '
         'The oval is a raked-sand riding arena and the circle a round pen, both with white pipe fences; roads are compacted pale dirt. '
         'Where the first image shows a flat pale band or an empty plane beyond the edge of the modelled ground, continue the real landscape there: the valley floor with vineyards, oak and scrub, and blue hills in the far distance; never an empty grey plane, a sea or fog. Keep the camera exactly where the first image puts it: if it is a view at eye level standing under a roof, the result is at eye level under that roof, never an aerial view. '
         'Photorealistic, like a professional architectural photograph: natural colour, sharp detail, no text, no labels, no people posing.')

def openai(png_path, prompt, refs, k):
    im = Image.open(png_path).convert('RGB'); W2, H2 = 1536, 1024; pad = (H2 - 864) // 2
    c = Image.new('RGB', (W2, H2)); c.paste(im.crop((0, 0, im.width, 1)).resize((W2, pad)), (0, 0)); c.paste(im.crop((0, im.height - 1, im.width, im.height)).resize((W2, pad)), (0, H2 - pad)); c.paste(im.resize((W2, 864)), (0, pad))
    b = io.BytesIO(); c.save(b, 'PNG')
    files = [('image[]', ('view.png', b.getvalue(), 'image/png'))] + [('image[]', (f'ref{n + 1}.jpg', open(r, 'rb').read(), 'image/jpeg')) for n, r in enumerate(refs)]
    data = {'model': 'gpt-image-2', 'prompt': prompt + ' The plain bands along the top and bottom edges are outside the picture: leave them exactly as they are.',
            'size': '1536x1024', 'quality': QUAL, 'n': '1', 'input_fidelity': 'high'}
    r = requests.post('https://api.openai.com/v1/images/edits', headers={'Authorization': 'Bearer ' + k}, files=files, data=data, timeout=600)
    j = r.json()
    if 'data' not in j and 'input_fidelity' in json.dumps(j.get('error', {})):
        data.pop('input_fidelity'); r = requests.post('https://api.openai.com/v1/images/edits', headers={'Authorization': 'Bearer ' + k}, files=files, data=data, timeout=600); j = r.json()
    if 'data' not in j: raise RuntimeError(j.get('error', {}).get('message', f'status {r.status_code}'))
    out = Image.open(io.BytesIO(base64.b64decode(j['data'][0]['b64_json']))); s = out.height / H2
    return out.crop((0, int(pad * s), out.width, int((pad + 864) * s))).resize((1536, 864), Image.LANCZOS)

def google(png_path, prompt, refs, k, model='gemini-3-pro-image'):
    parts = [{'text': prompt}, {'inlineData': {'mimeType': 'image/png', 'data': base64.b64encode(open(png_path, 'rb').read()).decode()}}] + \
            [{'inlineData': {'mimeType': 'image/jpeg', 'data': base64.b64encode(open(r, 'rb').read()).decode()}} for r in refs]
    body = {'contents': [{'parts': parts}], 'generationConfig': {'responseModalities': ['IMAGE'], 'imageConfig': {'aspectRatio': '16:9', 'imageSize': '2K'}}}
    r = requests.post(f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent', headers={'x-goog-api-key': k, 'Content-Type': 'application/json'}, json=body, timeout=600)
    j = r.json()
    for c in j.get('candidates', []):
        for p in c.get('content', {}).get('parts', []):
            if 'inlineData' in p: return Image.open(io.BytesIO(base64.b64decode(p['inlineData']['data']))).convert('RGB')
    raise RuntimeError(j.get('error', {}).get('message', f'status {r.status_code}: no image'))

PLAN_NOTE = (' This view looks straight down from above like an aerial survey photograph, north up: keep it exactly top-down with no horizon and no sky; '
             'the long evening shadows fall toward the east.')

if __name__ == '__main__':
    k = key('OPENAI_API_KEY' if ENGINE == 'openai' else 'GEMINI_API_KEY')
    if not k: sys.exit(f'no {"OPENAI" if ENGINE == "openai" else "GEMINI"}_API_KEY in this user\'s environment')
    views = sorted(f[4:-4] for f in os.listdir(CTL) if f.startswith('ctl-') and f.endswith('.png'))
    for v in views:
        if ONLY and v not in ONLY: continue
        prompt = open(os.path.join(CTL, f'prompt-{v}.txt'), encoding='utf-8').read() + SCENE + (PLAN_NOTE if v == '7-plan' else '')
        refs = sorted(os.path.join(CTL, f) for f in os.listdir(CTL) if f.startswith(f'ref-{v}-'))
        n = 1 + sum(1 for f in os.listdir(OUT) if f.startswith(f'{v}-{ENGINE}-'))
        t = time.time()
        try:
            im = (openai if ENGINE == 'openai' else google)(os.path.join(CTL, f'ctl-{v}.png'), prompt, refs, k)
            dst = os.path.join(OUT, f'{v}-{ENGINE}-{n}.png'); im.save(dst); print(f'{v}: ok in {time.time() - t:.0f}s -> {os.path.basename(dst)}')
        except Exception as e: print(f'{v}: FAILED {e}')
