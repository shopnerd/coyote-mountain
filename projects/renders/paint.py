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

SCENE = (   # 27 Sep, Will: "not very accurate to the terrain and to the buildings" -> strict, one-to-one with the model view
    ' STRICT FIDELITY. This is a faithful photographic rendering of an architectural model, not a reinterpretation. '
    'Everything built in the first image appears in the result one-to-one: the same number of buildings, fences, roads, troughs and vehicles, '
    'each with the same outline, the same position in the frame, the same size, the same orientation and the same roof shape. '
    'Add nothing that the first image does not show: no extra building, shed, room, wall, roof, fence, gate, tree, palm, vehicle, pond or water. '
    'Remove nothing. Do not straighten, lengthen, widen, rotate, shrink, enlarge or rearrange anything. '
    'The terrain keeps exactly the silhouette, ridgelines, slopes and horizon of the first image; hills stay the same height and shape. '
    'Only surfaces, materials, light and sky change. '
    'Light: golden hour, the sun low in the west about half an hour before sunset, warm light, long soft shadows; big puffy cumulus clouds lit gold and pink against clear blue. '
    'Place: the Valle de Guadalupe, Baja California, dry season: golden grass, olive-green scrub and granite boulders on the ground the model shows. '
    'The low building whose roof dips to a valley along its middle is a set of covered horse stalls. Its roof is ONE continuous, nearly flat, light grey '
    'standing-seam metal surface, a shallow but clearly visible V in cross-section (the centre line over the corridor is the lowest part, the two long outer edges the highest), '
    'with no notch, gap, cutout, step, ridge or skylight anywhere in it, carried on slim steel posts. Under it are two rows of four open stalls '
    'made of white-painted steel pipe panels facing a sand corridor; the back part of each stall is open to the sky. A few horses stand in the stalls. '
    'The bay at the north-east end of the same building, under the same roof, is the alfalfa bay: a stack of green-gold alfalfa bales behind pipe panels, '
    'with no walls and no separate roof. '
    'At the south-west end a round galvanised stock-water trough sits on the ground, fed by a short open chute from the roof valley; nothing stands under the chute. '
    'The larger gabled building is the main stable: a stacked fieldstone base about 4.5 ft high all the way round; above it, thin wooden tomato stakes laid HORIZONTALLY '
    'in loose, slightly uneven courses with small gaps, like a bird\'s nest, between dark steel posts; '
    'dark steel frames with trusses showing at the two open gable ends, and a dark charcoal corrugated metal roof with a raised glazed clerestory strip along the ridge; '
    'its six runs on one long side have black pipe fences. '
    'The oval is a raked-sand riding arena and the circle a round pen, both with white pipe fences; roads are compacted pale dirt. '
    'Beyond the edge of the modelled ground, where the first image shows a flat pale band, continue the real landscape (the valley floor with vineyards '
    'and blue hills in the far distance), never an empty plane, a sea or fog. Keep the camera exactly where the first image puts it. '
    'Photorealistic, like a professional architectural photograph: natural colour, sharp detail, no text, no labels.')

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

def google(png_path, prompt, refs, k, model=None, aspect='16:9', size=None):
    model = model or os.environ.get('GEMINI_MODEL', 'gemini-3-pro-image')   # 6 Oct: GEMINI_MODEL=gemini-nano-banana-2.1 to try the new one
    parts = [{'text': prompt}, {'inlineData': {'mimeType': 'image/png', 'data': base64.b64encode(open(png_path, 'rb').read()).decode()}}] + \
            [{'inlineData': {'mimeType': 'image/jpeg', 'data': base64.b64encode(open(r, 'rb').read()).decode()}} for r in refs]
    body = {'contents': [{'parts': parts}], 'generationConfig': {'responseModalities': ['IMAGE'], 'imageConfig': {'aspectRatio': aspect, 'imageSize': size or os.environ.get('GEMINI_SIZE', '2K')}}}
    r = requests.post(f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent', headers={'x-goog-api-key': k, 'Content-Type': 'application/json'}, json=body, timeout=600)
    j = r.json()
    for c in j.get('candidates', []):
        for p in c.get('content', {}).get('parts', []):
            if 'inlineData' in p: return Image.open(io.BytesIO(base64.b64decode(p['inlineData']['data']))).convert('RGB')
    raise RuntimeError(j.get('error', {}).get('message', f'status {r.status_code}: no image'))

PLAN_NOTE = (' This view looks straight down from above like an aerial survey photograph, north up: keep it exactly top-down with no horizon and no sky; '
             'the long evening shadows fall toward the east.')

FIXES = {'3-site-ne': ' The last attempt got this wrong and it must be right this time: the long building in the foreground with six fenced runs along one side is the MAIN STABLE, '
         'not the covered stalls: paint it with a dark charcoal roof with the raised glazed clerestory along its ridge, a stone base and woven stick walls, exactly as the stable reference shows. '
         'The covered stalls are the smaller light-roofed building further away.',
         '7-plan': ' The last attempt got this wrong and it must be right this time: the large fenced area on the left is OPEN GROUND, a turnout with a dirt riding track around '
         'its edge; there is no roof, building, cover or arena structure over it. The only roofed buildings are the two the first image shows: the dark-roofed stable with '
         'its clerestory and the light-roofed covered stalls.',
'5-corridor-out': ' The last attempt got this wrong and it must be right this time: the first image is taken standing at eye level INSIDE the covered corridor, '
         'under the roof, looking straight down the corridor between the two rows of stalls toward the far open end and the low sun. The roof fills the top of '
         'the picture seen from below, posts line both sides, stall panels run along both sides at waist to shoulder height. It is never an aerial view.'}

STABLE_REF = os.path.join(HERE, 'ref', 'stable-ref.jpg')     # Walker's image of the stable, 27 Sep
STABLE_NOTE = (' The last image shows the main stable as designed. Wherever the first image shows the main stable (the gabled building with the raised '
    'clerestory along its ridge and six fenced runs on one long side), paint it as the building in that last image: its stone base, '
    'dark steel frames and trusses, dark roof with the clerestory, wood stall fronts and black run fences, with ONE change: the sticks above the stone run '
    'HORIZONTALLY, as stacked tomato stakes like a bird\'s nest, not vertically as in that image. Take only the building from that image, never '
    'its mountains, vineyard, trough, sky or camera; keep the stable exactly at the size, position, angle and outline the first image shows.')

if __name__ == '__main__':
    k = key('OPENAI_API_KEY' if ENGINE == 'openai' else 'GEMINI_API_KEY')
    if not k: sys.exit(f'no {"OPENAI" if ENGINE == "openai" else "GEMINI"}_API_KEY in this user\'s environment')
    views = sorted(f[4:-4] for f in os.listdir(CTL) if f.startswith('ctl-') and f.endswith('.png'))
    for v in views:
        if ONLY and v not in ONLY: continue
        prompt = open(os.path.join(CTL, f'prompt-{v}.txt'), encoding='utf-8').read() + SCENE + (PLAN_NOTE if v == '7-plan' else '') + FIXES.get(v, '')
        refs = sorted(os.path.join(CTL, f) for f in os.listdir(CTL) if f.startswith(f'ref-{v}-')) + ([STABLE_REF] if os.path.exists(STABLE_REF) else [])
        if os.path.exists(STABLE_REF): prompt += STABLE_NOTE
        n = 1 + sum(1 for f in os.listdir(OUT) if f.startswith(f'{v}-{ENGINE}-'))
        t = time.time()
        try:
            im = (openai if ENGINE == 'openai' else google)(os.path.join(CTL, f'ctl-{v}.png'), prompt, refs, k)
            dst = os.path.join(OUT, f'{v}-{ENGINE}-{n}.png'); im.save(dst); print(f'{v}: ok in {time.time() - t:.0f}s -> {os.path.basename(dst)}')
        except Exception as e: print(f'{v}: FAILED {e}')
