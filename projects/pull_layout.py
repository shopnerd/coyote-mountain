"""Pull the web layout editor's saved changes into the pack build (4 Oct 2026).

    python pull_layout.py            # writes pack_layout.json (+ fetches swapped photos), then:  python pack.py

Photo swaps arrive as  lib:<gallery image>.jpg  or  upload:<id>.  A gallery image is matched to its full-resolution render in
renders/ (newest file with the same name); if none is found, the web copy (1536 px) is used. Uploads are saved to the Drive pack
folder under renderings/uploads/. The editor's history stays on the site (GET /equino/api/layout).
"""
import json, os, glob, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.environ.get('EQUINO_SITE', 'https://will.100xbtr.com')
OUTDIR = os.environ.get('EQUINO_PACK_DIR', 'G:/My Drive/MEXICO/Chichihaus/2026-09-23 Centro Equino pack')
UP = os.path.join(OUTDIR, 'renderings', 'uploads'); WEBLIB = os.path.join(OUTDIR, 'renderings', 'from-gallery')

def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'pull_layout'}), timeout=60) as r: return r.read()

def resolve(src):
    if src.startswith('upload:'):
        uid = src.split(':', 1)[1]; os.makedirs(UP, exist_ok=True); p = os.path.join(UP, uid + '.jpg')
        if not os.path.exists(p): open(p, 'wb').write(get(f'{SITE}/equino/api/upload?id={uid}'))
        return p
    if src.startswith('lib:'):
        name = src.split(':', 1)[1]; stem = name[:-4]
        hits = [f for ext in ('png', 'jpg', 'jpeg') for f in glob.glob(os.path.join(HERE, 'renders', '**', f'{stem}.{ext}'), recursive=True)]
        hits += [f for ext in ('png', 'jpg') for f in glob.glob(os.path.join(OUTDIR, 'renderings', '**', f'{stem}.{ext}'), recursive=True)]
        if hits: return max(hits, key=os.path.getmtime).replace('\\', '/')
        os.makedirs(WEBLIB, exist_ok=True); p = os.path.join(WEBLIB, name)
        if not os.path.exists(p): open(p, 'wb').write(get(f'{SITE}/equino/img/{name}'))
        return p
    return src

data = json.loads(get(f'{SITE}/equino/api/layout'))
L = data.get('layout') or {}
out = {'slots': {}, 'boxes': L.get('boxes') or {}, 'texts': L.get('texts') or {}, 'sizes': L.get('sizes') or {}}   # sizes: 10 Oct
for k, v in (L.get('slots') or {}).items():
    v = dict(v)
    if 'src' in v:
        try: v['src'] = resolve(v['src']).replace('\\', '/')
        except Exception as e: print('could not fetch', v['src'], e); v.pop('src')
    out['slots'][k] = v
json.dump(out, open(os.path.join(HERE, 'pack_layout.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print(f"pack_layout.json: {len(out['slots'])} photo changes, {len(out['boxes'])} drawing moves, {len(out['texts'])} text edits, {len(out['sizes'])} text sizes")
for h in (data.get('history') or [])[:8]: print('  ', h.get('at', '')[:16], h.get('by', ''), h.get('op'), h.get('kind'), h.get('key'))
