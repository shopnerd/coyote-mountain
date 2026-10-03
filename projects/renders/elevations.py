"""Eye-level elevation renders of the stable, one per side (Walker, 3 Oct 2026). Model render = truth; two real site photos
(Chichihaus/Site photos IMG_0576, IMG_0577) are references for the landscape, light and colour only."""
import os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.argv = sys.argv[:2] + sys.argv[2:]
import paint
from paint import openai, google, key
from gallery2 import gemini_key
paint.QUAL = 'high'
SIDE = {
 'el-north': 'the long NORTH side of the stable: six stalls, each opening through a 6 x 9 ft open doorway to its own 12 x 40 ft run fenced in black steel pipe, the runs in front of the camera',
 'el-south': 'the long SOUTH side of the stable: at the left end the two plastered rooms (wash room with one wide wooden door onto a concrete pad), then four stalls opening to their runs that climb the slope toward the camera, fenced in black steel pipe; the long low tan fieldstone water trough at far left',
 'el-west': 'the WEST end of the stable, its main entry: a big open gable with a large wooden sliding door slid aside, the dirt road running straight into the aisle, the steel truss visible in the gable, and the long low tan fieldstone water trough running along the front on the right',
 'el-east': 'the EAST end of the stable from the parking path: the open gable entry with its sliding door slid aside, looking down the aisle, the steel truss in the gable, black pipe runs on both sides',
}
BRIEF = ('Turn the FIRST image, an exact 3D model render, into an architectural photograph taken at standing eye level. It shows {side}. '
 'STRICT: keep the camera, the horizon, the terrain and every wall, roof, truss, opening, fence, gate, trough and tree exactly where they are, '
 'same size, shape and count; add no building. The stable: walls of light tan stacked fieldstone to 5 ft, a black steel pipe rail floating 1 ft above '
 'the stone, then up to the eave panels of thin HORIZONTAL wooden branches (bird nest style) in slim dark steel frames, 3 ft wide; 6 in black steel '
 'pipe posts; dark charcoal corrugated metal roof; a small raised open clerestory roof along the ridge; the plastered rooms are warm lime-washed '
 'straw bale. All fences and gates are black steel pipe. '
 'The OTHER images are real photos of this exact site in Baja California: use them ONLY for the landscape, light and colour: the rounded granite '
 'hills, the soil, the shrubs, the vineyards. Do not copy any building from them. Season: late spring, a little green: fresh green in the low '
 'ground and grass tips among golden dry grass, not lush. Golden hour, warm low sun, long soft shadows, a sky of big lit cumulus clouds. '
 'Two or three horses in the runs or being led, one person, maybe a ranch dog, all at true scale. Photoreal, high-end architectural photography.')
REFS = [os.path.join(HERE, 'site-ref-0576.jpg'), os.path.join(HERE, 'site-ref-0577.jpg')]
if __name__ == '__main__':
    eng = sys.argv[1]; views = sys.argv[2:] or list(SIDE)
    k = key('OPENAI_API_KEY') if eng == 'openai' else gemini_key()
    os.makedirs(os.path.join(HERE, 'elevations'), exist_ok=True)
    for v in views:
        t = time.time()
        try:
            im = (openai if eng == 'openai' else google)(os.path.join(HERE, 'model', f'model-{v}.png'), BRIEF.format(side=SIDE[v]), REFS, k)
            im.save(os.path.join(HERE, 'elevations', f'{v}-{eng}.png')); print(v, eng, 'ok', round(time.time() - t))
        except Exception as e: print(v, eng, 'FAILED', str(e)[:200])
