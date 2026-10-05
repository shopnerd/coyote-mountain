"""Animate a finished painting with Veo 3.1 image-to-video (5 Oct 2026, Will: 'animate some of those scenes').
The painting is the first frame; the prompt asks for camera drift and life only, nothing built may change.

    python animate.py <painting.jpg> <out.mp4> "<motion prompt>" [fast|full]
"""
import base64, json, os, sys, time, urllib.request
sys.argv, ARGS = [sys.argv[0], 'google'], sys.argv[1:]
from gallery2 import gemini_key

RULES = (' Keep every building, roof, wall, fence, road, trough and tree exactly as in the first frame: same shapes, same places, '
         'nothing added, removed or morphing. Only the camera moves, slowly and smoothly, and the living things move: horses, people, '
         'a dog, grass, dust, clouds and light. No text, no cuts.')

def animate(img, out, prompt, model='veo-3.1-fast-generate-preview'):
    k = gemini_key(); base = 'https://generativelanguage.googleapis.com/v1beta'
    body = {'instances': [{'prompt': prompt + RULES, 'image': {'bytesBase64Encoded': base64.b64encode(open(img, 'rb').read()).decode(), 'mimeType': 'image/jpeg'}}],
            'parameters': {'aspectRatio': '16:9', 'durationSeconds': 8, 'resolution': '1080p'}}
    req = urllib.request.Request(f'{base}/models/{model}:predictLongRunning', data=json.dumps(body).encode(), headers={'content-type': 'application/json', 'x-goog-api-key': k})
    op = json.load(urllib.request.urlopen(req, timeout=120))['name']
    t = time.time()
    while True:
        time.sleep(10)
        st = json.load(urllib.request.urlopen(urllib.request.Request(f'{base}/{op}', headers={'x-goog-api-key': k}), timeout=60))
        if st.get('done'): break
        if time.time() - t > 900: raise RuntimeError('timed out')
    if 'error' in st: raise RuntimeError(st['error'])
    vids = st['response']['generateVideoResponse'].get('generatedSamples') or []
    if not vids: raise RuntimeError('no video: ' + json.dumps(st['response'])[:300])
    uri = vids[0]['video']['uri']
    with urllib.request.urlopen(urllib.request.Request(uri, headers={'x-goog-api-key': k}), timeout=300) as r, open(out, 'wb') as f: f.write(r.read())
    print(f'{out}: ok in {time.time() - t:.0f}s')

if __name__ == '__main__':
    img, out, prompt = ARGS[:3]
    animate(img, out, prompt, 'veo-3.1-generate-preview' if ARGS[3:4] == ['full'] else 'veo-3.1-fast-generate-preview')
