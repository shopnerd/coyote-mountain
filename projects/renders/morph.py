"""Dreamscape morphs (6 Oct 2026, Will: 'animate different representations of the same site while it's panning around and
morphing from one to another, a weird AI hallucination dreamscape'). Low-cost tests.

  Veo 3.1 fast  : first AND last frame -> the motion between two real pictures (model -> painting -> watercolor ...)
  Sora 2 (API)  : first frame only -> the prompt asks it to dissolve into the next world

    python morph.py veo  <first.jpg> <last.jpg> <out.mp4> "<prompt>" [seconds=6]
    python morph.py sora <first.jpg> <out.mp4> "<prompt>" [seconds=4]
"""
import base64, io, json, os, sys, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
MODE, ARGS = sys.argv[1], sys.argv[2:]
sys.argv = [sys.argv[0], 'google']
from gallery2 import gemini_key
from paint import key
from PIL import Image

STAY = (' Keep the land, roads, fences and buildings in the same places throughout; only the way the world is depicted changes, '
        'smoothly and dreamily, like one medium melting into another. Slow, steady, continuous camera drift. No text, no cuts, no people running.')

def jpg(path, size=(1280, 720)):
    im = Image.open(path).convert('RGB'); w, h = im.size; th = round(w * size[1] / size[0])
    if h > th: im = im.crop((0, (h - th) // 2, w, (h - th) // 2 + th))
    im = im.resize(size); b = io.BytesIO(); im.save(b, 'JPEG', quality=92); return b.getvalue()

def veo(first, last, out, prompt, secs=8, model='veo-3.1-fast-generate-preview'):
    k = gemini_key(); base = 'https://generativelanguage.googleapis.com/v1beta'
    inst = {'prompt': prompt + STAY, 'image': {'bytesBase64Encoded': base64.b64encode(jpg(first)).decode(), 'mimeType': 'image/jpeg'},
            'lastFrame': {'bytesBase64Encoded': base64.b64encode(jpg(last)).decode(), 'mimeType': 'image/jpeg'}}
    body = {'instances': [inst], 'parameters': {'aspectRatio': '16:9', 'durationSeconds': secs, 'resolution': '720p'}}
    req = urllib.request.Request(f'{base}/models/{model}:predictLongRunning', data=json.dumps(body).encode(), headers={'content-type': 'application/json', 'x-goog-api-key': k})
    try: op = json.load(urllib.request.urlopen(req, timeout=120))['name']
    except urllib.error.HTTPError as e: raise RuntimeError(e.read().decode()[:400])
    t = time.time()
    while True:
        time.sleep(10); st = json.load(urllib.request.urlopen(urllib.request.Request(f'{base}/{op}', headers={'x-goog-api-key': k}), timeout=60))
        if st.get('done'): break
        if time.time() - t > 900: raise RuntimeError('timed out')
    if 'error' in st: raise RuntimeError(st['error'])
    uri = st['response']['generateVideoResponse']['generatedSamples'][0]['video']['uri']
    with urllib.request.urlopen(urllib.request.Request(uri, headers={'x-goog-api-key': k}), timeout=300) as r, open(out, 'wb') as f: f.write(r.read())
    print(f'{out}: veo ok in {time.time() - t:.0f}s')

def sora(first, out, prompt, secs=4, model='sora-2'):
    import requests
    k = key('OPENAI_API_KEY'); H = {'Authorization': 'Bearer ' + k}
    r = requests.post('https://api.openai.com/v1/videos', headers=H, timeout=120,
                      data={'model': model, 'prompt': prompt + STAY, 'seconds': str(secs), 'size': '1280x720'},
                      files={'input_reference': ('first.jpg', jpg(first), 'image/jpeg')})
    j = r.json()
    if 'id' not in j: raise RuntimeError(json.dumps(j)[:400])
    vid, t = j['id'], time.time()
    while True:
        time.sleep(10); j = requests.get(f'https://api.openai.com/v1/videos/{vid}', headers=H, timeout=60).json()
        if j.get('status') in ('completed', 'failed'): break
        if time.time() - t > 900: raise RuntimeError('timed out')
    if j.get('status') != 'completed': raise RuntimeError(json.dumps(j)[:400])
    c = requests.get(f'https://api.openai.com/v1/videos/{vid}/content', headers=H, timeout=300)
    open(out, 'wb').write(c.content); print(f'{out}: sora ok in {time.time() - t:.0f}s')

if __name__ == '__main__':
    if MODE == 'veo': veo(ARGS[0], ARGS[1], ARGS[2], ARGS[3], int(ARGS[4]) if len(ARGS) > 4 else 8)
    else: sora(ARGS[0], ARGS[1], ARGS[2], int(ARGS[3]) if len(ARGS) > 3 else 4)
