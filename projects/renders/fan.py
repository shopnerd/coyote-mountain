"""Camera fan (4 Oct 2026, Will): one hero view -> six nearby cameras from the 3D model -> painted by Gemini and OpenAI ->
published to the gallery's "Abanico de cámaras · Camera fan" section to star the best. The geometry stays true because every
painting starts from a real model shot of its own camera (no AI re-angling).

    python fan.py <view id> [--n 6] [--engines google,openai] [--no-paint]
    e.g. python fan.py 8-stable          python fan.py b3-sw --engines google

Needs the viewer served at http://127.0.0.1:8792/index.html (cd projects/viewer && python -m http.server 8792).
Walk cameras (i, j, h, yaw, pitch) fan around the point they look at: step left/right, higher, lower, closer, wider.
Orbit cameras (ti, tj, az, el, dist) fan by azimuth, elevation and distance. Top-down plans are not fanned.
"""
import json, math, os, re, subprocess, sys, threading, datetime
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); WEB = os.path.join(HERE, '..', '..', '..', 'will-os', 'equino', 'img')
CS = 400 / 149                                                     # metres per grid cell
args = sys.argv[1:]
if not args: sys.exit(__doc__)
BASE = args[0]
N = int(args[args.index('--n') + 1]) if '--n' in args else 6
ENGINES = (args[args.index('--engines') + 1] if '--engines' in args else 'google,openai').split(',')
PAINT = '--no-paint' not in args

def base_view(vid):
    src = open(os.path.join(HERE, 'modelshots.mjs'), encoding='utf-8').read()
    m = re.search(r"\{\s*id:\s*'" + re.escape(vid) + r"'.*?\}\s*\}?\s*,?\s*(?://[^\n]*)?\n", src)
    if not m: sys.exit(f'no camera called {vid} in modelshots.mjs')
    lit = m.group(0).strip().rstrip(',')
    lit = re.sub(r'//[^\n]*', '', lit).strip().rstrip(',')
    lit = re.sub(r"([{,]\s*)([A-Za-z_]\w*)\s*:", r'\1"\2":', lit).replace("'", '"')
    lit = re.sub(r',\s*}', '}', lit)
    return json.loads(lit)

def walk_fan(v):
    i, j, h, yaw, pitch = v['i'], v['j'], v['h'], v['yaw'], v['pitch']
    sp, cp, D = math.sin(pitch), math.cos(pitch), 40.0                   # the point it looks at, 40 m out along the view
    E = (i * CS, h, j * CS); F = (E[0] + math.sin(yaw) * sp * D, E[1] + cp * D, E[2] + math.cos(yaw) * sp * D)
    def look(ex, ey, ez, tag, fov=None):
        dx, dy, dz = F[0] - ex, F[1] - ey, F[2] - ez; L = math.sqrt(dx * dx + dy * dy + dz * dz)
        out = {k: v[k] for k in v if k not in ('id', 'i', 'j', 'h', 'yaw', 'pitch')}
        out.update(id=f'{BASE}-fan-{tag}', i=round(ex / CS, 2), j=round(ez / CS, 2), h=round(max(1.2, ey), 2), yaw=round(math.atan2(dx, dz), 3), pitch=round(math.acos(dy / L), 3))
        if fov: out['fov'] = fov
        return out
    px, pz = math.cos(yaw), -math.sin(yaw)                                 # sideways (perpendicular to the view, level)
    side = max(6.0, D * .2); fx, fz = F[0] - E[0], F[2] - E[2]
    return [look(E[0] - px * side, h, E[2] - pz * side, 'left'), look(E[0] + px * side, h, E[2] + pz * side, 'right'),
            look(E[0], h * 2.2 + 4, E[2], 'high'), look(E[0], max(1.4, h * .45), E[2], 'low'),
            look(E[0] + fx * .3, h, E[2] + fz * .3, 'closer'), look(E[0] - fx * .4, h + 1, E[2] - fz * .4, 'wider', fov=60)]

def orbit_fan(v):
    o = v['orbit']; rest = {k: v[k] for k in v if k not in ('id', 'orbit')}
    def mk(tag, **d): q = {**o, **d}; q['el'] = max(3, min(85, q['el'])); return {**rest, 'id': f'{BASE}-fan-{tag}', 'orbit': q}
    return [mk('left', az=o['az'] - 18), mk('right', az=o['az'] + 18), mk('high', el=o['el'] + 12), mk('low', el=o['el'] - 10),
            mk('closer', dist=round(o['dist'] * .72, 1)), mk('wider', dist=round(o['dist'] * 1.35, 1))]

v = base_view(BASE)
if 'top' in v: sys.exit('top-down plans are not fanned')
if '--light' in args:                                   # 4 Oct: same camera, other times of day and weather (gallery3.LIGHT)
    sys.argv = [sys.argv[0], 'google']; import gallery3 as _G
    TAGS = (args[args.index('--tags') + 1].split(',') if '--tags' in args else list(_G.LIGHT))
    fan = [{**{k: v[k] for k in v if k != 'id'}, 'id': f'{BASE}-fan-{tag}', 'hour': _G.LIGHT[tag][0]} for tag in TAGS][:N]
else:
    fan = (orbit_fan(v) if 'orbit' in v else walk_fan(v))
    if '--tags' in args: fan = [f for f in fan if f['id'].split('-fan-')[1] in args[args.index('--tags') + 1].split(',')]
    fan = fan[:N]
FF = os.path.join(HERE, f'fan-views-{BASE}-{os.getpid()}.json'); json.dump(fan, open(FF, 'w'))   # one per run, so fans can run side by side
ids = [f['id'] for f in fan]
print('fan:', ', '.join(ids))
MD = os.path.join(HERE, 'fans', 'model'); os.makedirs(MD, exist_ok=True)
env = {**os.environ, 'FAN_FILE': FF}
r = subprocess.run(['node', 'modelshots.mjs', 'http://127.0.0.1:8792/index.html', MD, ','.join(ids)], cwd=HERE, env=env, capture_output=True, text=True)
print(r.stdout.strip()[-400:]); ok = [i for i in ids if os.path.exists(os.path.join(MD, f'model-{i}.png'))]
if not ok: sys.exit('no model shots: is the viewer served on 8792?\n' + r.stderr[-600:])

done = {'model': ok}
if PAINT:
    def run(eng):
        e = {**os.environ, 'GAL_SRC': os.path.join('fans', 'model'), 'GAL_OUT': os.path.join('fans', 'painted'), 'GEMINI_SIZE': '2K'}
        p = subprocess.run([sys.executable, 'gallery3.py', eng] + ok, cwd=HERE, env=e, capture_output=True, text=True); print(p.stdout.strip())
    th = [threading.Thread(target=run, args=(e,)) for e in ENGINES]; [t.start() for t in th]; [t.join() for t in th]
    for eng in ENGINES: done[eng] = [i for i in ok if os.path.exists(os.path.join(HERE, 'fans', 'painted', f'{i}-{eng}.png'))]

# publish: 1536 px JPEGs in will-os/equino/img + the fans manifest the gallery reads
os.makedirs(WEB, exist_ok=True)
for eng, lst in done.items():
    for i in lst:
        srcp = os.path.join(HERE, 'fans', 'model' if eng == 'model' else 'painted', f'model-{i}.png' if eng == 'model' else f'{i}-{eng}.png')
        im = Image.open(srcp).convert('RGB'); im.thumbnail((1536, 1536)); im.save(os.path.join(WEB, f'{i}-{eng}.jpg'), quality=85)
MF = os.path.join(WEB, 'fans.json')
man = json.load(open(MF, encoding='utf-8')) if os.path.exists(MF) else []
old = next((m for m in man if m.get('base') == BASE), None); man = [m for m in man if m.get('base') != BASE]
NAMES = {'dawn': ('amanecer', 'dawn'), 'golden': ('hora dorada', 'golden hour'), 'storm': ('tormenta que se despeja', 'clearing storm'), 'blue': ('hora azul', 'blue hour'), 'fog': ('niebla de la mañana', 'morning fog'), 'dusk': ('al anochecer, luces encendidas', 'just after sundown, lights on'), 'left': ('a la izquierda', 'step left'), 'right': ('a la derecha', 'step right'), 'high': ('más alto', 'higher'), 'low': ('más bajo', 'lower'), 'closer': ('más cerca', 'closer'), 'wider': ('más abierto', 'wider')}
man.insert(0, {'base': BASE, 'made': datetime.date.today().isoformat(),
               'views': [{'id': i, 'es': NAMES[i.split('-fan-')[1]][0], 'en': NAMES[i.split('-fan-')[1]][1], 'eng': [e for e in ENGINES if i in done.get(e, [])], 'old': ['model']} for i in ok]})
if old:                                                   # keep earlier views of this base and add engines to repeated ones
    new = man[0]; ids = {x['id']: x for x in new['views']}
    for ov in old['views']:
        if ov['id'] in ids: ids[ov['id']]['eng'] = sorted(set(ids[ov['id']]['eng']) | set(ov['eng']))
        else: new['views'].append(ov)
json.dump(man, open(MF, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
try: os.remove(FF)
except OSError: pass
print(f'published {sum(len(l) for l in done.values())} images; gallery section "Abanico de cámaras" lists {len(man)} fan(s)')
