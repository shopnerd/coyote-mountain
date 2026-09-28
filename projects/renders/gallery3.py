"""Fresh money shots (28 Sep 2026): one short, strict brief instead of the layered correction notes of gallery2.py.
The model render is the truth; the painter only adds materials, light, sky and life.

    python gallery3.py <google|openai> [view ...]   ->  gallery3/<view>-<engine>.png   (sources: model/model-<view>.png)
"""
import os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import paint
from paint import openai, google, key
from gallery2 import gemini_key
paint.QUAL = 'high'
SRC, OUT = os.path.join(HERE, 'model'), os.path.join(HERE, 'gallery3'); os.makedirs(OUT, exist_ok=True)
ENGINE = sys.argv[1]; ONLY = sys.argv[2:]
VIEWS = ['1-hero-sw', '3-site-ne', '20-front-yard', '16-stable-sw', '18-stable-west-elev', '8-stable', '14-bleachers-high', '13-bleachers',
         '11-arena', '5-corridor-out', '4-hill-s', '9-arrival']
BRIEF = (
    'Turn this 3D model render into a photograph of the real place, a ranch in the dry hills of northern Baja California at golden hour. '
    'STRICT: this is an exact model. Keep the camera, the terrain and every building, roof, road, fence, trough, tree and vehicle exactly where it is, '
    'with the same size, shape and count. Do not move, add, remove or redesign anything built. Only replace the flat model colours with real '
    'materials, add light, sky and life.\n'
    'Materials: the ground is dry golden grass, sage scrub and granite boulders, with the colours of the aerial photo it is draped with; dirt roads '
    'are pale compacted earth. The large stable has walls of light tan stacked fieldstone to about 5 ft, a black pipe rail above, panels of thin '
    'horizontal wooden branches in dark steel frames up to the eave, a dark charcoal corrugated roof with an open clerestory along the ridge, and '
    'two plastered rooms at one end. The open shed with the butterfly (V) roof is the covered stalls: matte galvanised corrugated roof, dark steel '
    'posts, black pipe panels, and a round fieldstone water trough at its end. All fences and gates everywhere are BLACK steel pipe. The long low box '
    'by the stable is a tan fieldstone water trough. The old white semi-trailer keeps its photo texture exactly, with NO sign or lettering on it, with wooden '
    'steps and a deck in front of it under a corrugated shade roof. The oval with the fence is a sand riding arena; the small circle a sand round pen. '
    'The round trees are modest pines. The small boxes in the parking area are cars and pickups.\n'
    'Life, at true scale and only on the ground: plenty of horses (bay, chestnut, grey, a paint) in the runs, stalls, arena and being led along the '
    'roads; people working, riding and watching; one ranch dog. Nothing oversized.\n'
    'Light: warm low golden-hour sun, long soft shadows, a sky with big lit cumulus clouds. Photoreal, like a high-end architectural photograph.')

if __name__ == '__main__':
    k = key('OPENAI_API_KEY') if ENGINE == 'openai' else gemini_key()
    if not k: sys.exit('no key for ' + ENGINE)
    for v in (ONLY or VIEWS):
        t = time.time()
        try:
            im = (openai if ENGINE == 'openai' else google)(os.path.join(SRC, f'model-{v}.png'), BRIEF, [], k)
            im.save(os.path.join(OUT, f'{v}-{ENGINE}.png')); print(f'{v} {ENGINE}: ok in {time.time() - t:.0f}s')
        except Exception as e: print(f'{v} {ENGINE}: FAILED {str(e)[:160]}')
