"""Gallery · "One view, many ways" for Centro Equino, rebuilt from Will's tagged picks (6 Oct 2026: he tagged 99 on the
every-render sheet, will.100xbtr.com/equino/all/, and asked Claude to choose). Each view opens with the plain model shot, then
the paintings. Paintings that invent buildings (the el-east 'cabin barn') were left out on purpose.

    python ce_build.py        (copies from ../../will-os/equino/img into ce/ and ce/t/, rewrites the VIEWS line in index.html)
"""
import json, os, re
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(HERE, '..', '..', 'will-os', 'equino', 'img')
CE, CT = os.path.join(HERE, 'ce'), os.path.join(HERE, 'ce', 't')

# (id, title, model shot, [paintings]) -- paintings by key in will-os/equino/img, in the order shown
VIEWS = [
 ('stable-night', 'The stable at night, lit from inside', '16-stable-sw-lantern-fan-closer-model',
  ['16-stable-sw-lantern-fan-closer-google', '16-stable-sw-lantern-fan-right-google', '16-stable-sw-lantern-fan-low-openai', '16-stable-sw-lantern-fan-high-google', '16-stable-sw-lantern-fan-wider-google']),
 ('runs', 'The north side and its runs', '8-stable-fan-golden-model',
  ['8-stable-fan-golden-google', '8-stable-fan-right-openai', '8-stable-fan-low-openai', '8-stable-fan-left-openai', '8-stable-fan-blue-google']),
 ('hill', 'From the hill', '4-hill-s-fan-golden-model',
  ['4-hill-s-fan-golden-openai', '4-hill-s-fan-fog-openai', '4-hill-s-fan-dusk-openai', '4-hill-s-fan-storm-openai', '4-hill-s-watercolor-openai']),
 ('north', 'North elevation', 'el-north-fan-golden-model',
  ['el-north-fan-golden-openai', 'el-north-fan-dawn-google', 'el-north-fan-golden-google', 'el-north-fan-blue-google', 'el-north-fan-storm-google']),
 ('south', 'South elevation, the wash pad under the vine', 'el-south-fan-golden-model',
  ['el-south-fan-golden-openai', 'el-south-fan-dawn-google', 'el-south-fan-blue-google', 'el-south-fan-storm-google', 'el-south-watercolor-openai']),
 ('west', 'The road entry, a horse drinking', 'el-west-horse-fan-golden-model',
  ['el-west-horse-fan-golden-openai', 'el-west-horse-fan-golden-google', 'el-west-horse-fan-storm-google', 'el-west-horse-oct3o']),
 ('aisle', 'Inside the stable', '10-stable-aisle-fan-golden-model',
  ['10-stable-aisle-fan-golden-openai', '10-stable-aisle-fan-golden-google', '10-stable-aisle-fresh', '10-stable-aisle-watercolor-openai']),
 ('cafe', 'The café end', 'cafe-end-fan-closer-model',
  ['cafe-end-fan-closer-openai', 'cafe-end-fan-high-google', 'cafe-end-fan-low-google', 'cafe-end-fan-wider-google', 'cafe-end-watercolor-openai']),
 ('stalls', 'Under the covered stalls', '5-corridor-out-fan-golden-model',
  ['5-corridor-out-fan-golden-openai', '5-corridor-out-fan-dawn-google', '5-corridor-out-fan-blue-google']),
 ('block', 'The site as a block', 'b3-sw-fan-golden-model',
  ['b3-sw-fan-golden-openai', 'b4-nw-fan-golden-openai', 'b1-ne-freshoa', 'b7-plan-oct3o']),
]
LIGHT = [('lantern', 'night, lit from inside'), ('watercolor', 'watercolour'), ('golden', 'golden hour'), ('dawn', 'dawn'), ('dusk', 'dusk'), ('fog', 'fog'),
         ('storm', 'storm'), ('blue', 'blue hour'), ('plan', 'plan')]
STEP = {'left': 'step left', 'right': 'step right', 'high': 'higher', 'low': 'lower', 'closer': 'closer', 'wider': 'wider'}
def light(k):
    step = STEP.get(k.split('-fan-')[1].rsplit('-', 1)[0], '') if '-fan-' in k else ''
    for w, l in LIGHT:
        if w in k: return l if w != 'lantern' else 'night' + (' · ' + step if step else '')
    return step or 'painted'
def who(k): return 'Gemini' if re.search(r'(google|oct\dg|-fresh)$', k) else 'OpenAI'

if __name__ == '__main__':
    os.makedirs(CT, exist_ok=True)
    for f in os.listdir(CE):
        if f.endswith('.jpg') and not f.startswith('sheet-'): os.remove(os.path.join(CE, f))
    for f in os.listdir(CT):
        if not f.startswith('sheet-'): os.remove(os.path.join(CT, f))
    out = []
    for vid, title, model, keys in VIEWS:
        items = []
        for n, k in enumerate([model] + keys):
            src = os.path.join(SRC, k + '.jpg')
            if not os.path.exists(src): print('MISSING', k); continue
            name = f'{vid}-{n}.jpg'; im = Image.open(src).convert('RGB')
            im.thumbnail((1536, 1536)); im.save(os.path.join(CE, name), quality=88)
            t = im.copy(); t.thumbnail((760, 760)); t.save(os.path.join(CT, name), quality=82)
            items.append([name, 'the model, no AI', 'model'] if n == 0 else [name, light(k), who(k)])
        out.append({'id': vid, 'title': title, 'items': items})
    p = os.path.join(HERE, 'index.html'); s = open(p, encoding='utf-8').read()
    m = re.search(r'^const VIEWS = .*$', s, re.M)
    s = s[:m.start()] + 'const VIEWS = ' + json.dumps(out, ensure_ascii=False) + ';' + s[m.end():]
    open(p, 'w', encoding='utf-8').write(s)
    print(len(out), 'views,', sum(len(v['items']) for v in out), 'pictures')
