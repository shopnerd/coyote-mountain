"""Light AI finish on the model renders (27 Sep, Will: "model render + light AI finish"): the render from the 3D viewer
is already exact; the painter may only turn surfaces into real materials, add golden-hour light and a cumulus sky.

    python finish.py [quality] [view-id ...]   ->  finished/<view>-<n>.png
"""
import os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import paint
from paint import openai, key
SRC, OUT = os.path.join(HERE, 'model'), os.path.join(HERE, 'finished'); os.makedirs(OUT, exist_ok=True)
QUAL = sys.argv[1] if len(sys.argv) > 1 else 'high'; ONLY = sys.argv[2:]
paint.QUAL = QUAL                                     # paint.py read its own argv at import; set the quality for this run
BRIEF = ('This image is a render of an accurate 3D architectural model of a small equestrian centre in the Valle de Guadalupe, Baja California. '
    'Make it look like a real photograph WITHOUT CHANGING THE DESIGN. Keep exactly: the camera, framing and horizon; every building, roof, post, rail, fence, '
    'gate opening, road, trough, trailer and car, and the shape of the ground: same count, position, size, outline and proportions. Add no building, roof, '
    'wall, fence, pond or tree, remove nothing, move nothing. Keep the direction of the light and the shadows the render shows. '
    'You may only: give the surfaces real materials, add golden-hour light, and replace the plain sky. Materials: the larger building is the stable, a stacked '
    'fieldstone base about 4.5 ft high with thin wooden tomato stakes laid HORIZONTALLY above it in loose courses with small gaps like a bird\'s nest, dark '
    'steel posts and frames, a matte dark charcoal corrugated metal roof with a glazed clerestory strip along its ridge, and black steel pipe fences around '
    'its runs. The smaller open building is the covered stalls: black-painted steel pipe panels, slim dark steel posts, and a matte galvanised corrugated '
    'metal butterfly roof whose corrugations run down each slope toward the centre valley, not shiny, not flat sheet; golden alfalfa bales stacked in its '
    'end bay; a galvanised round trough with water. Roads are compacted pale dirt; the ground is dry golden grass, olive-green scrub and a few granite '
    'boulders; the arena and round pen are raked sand with black pipe fences. Sky: a warm golden-hour sky with big puffy cumulus clouds lit gold and pink. '
    'A few horses may stand inside the stalls and runs. Beyond the edge of the modelled ground, continue the real valley with vineyards and distant hills. '
    'Photorealistic architectural photograph, natural colour, no text.')
if __name__ == '__main__':
    k = key('OPENAI_API_KEY')
    for f in sorted(os.listdir(SRC)):
        if not (f.startswith('model-') and f.endswith('.png')): continue
        v = f[6:-4]
        if ONLY and v not in ONLY: continue
        n = 1 + sum(1 for g in os.listdir(OUT) if g.startswith(v + '-')); t = time.time()
        try:
            im = openai(os.path.join(SRC, f), BRIEF + (' This view looks straight down from above: keep it exactly top-down, no horizon, no sky.' if v == '7-plan' else ''), [], k)
            im.save(os.path.join(OUT, f'{v}-{n}.png')); print(f'{v}: ok in {time.time() - t:.0f}s')
        except Exception as e: print(f'{v}: FAILED {e}')
