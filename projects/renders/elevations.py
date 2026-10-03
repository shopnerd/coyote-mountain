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
 'el-west': 'the WEST end of the stable, its main entry: the open gable entry with its stick-clad sliding doors slid aside, the dirt road sweeping in from the left into the aisle, the plastered rooms at the right end, and in the foreground the long low tan fieldstone water trough running across the whole view, acting as a low retaining wall',
 'el-south-wash': 'the WEST end of the stable’s long SOUTH side, square on, centred on the plastered wash room: its one wide 6 x 9 ft doorway opening onto a flat concrete pad 12 x 24 ft that runs along the wall, a low tan fieldstone water trough 12 ft long along the outer edge of that pad (a horse drinks from it), the tack room wall beside it, and to the right the stalls with their black pipe runs climbing the slope; the white trailer far off on the left',
 'el-east': 'the EAST end of the stable from the parking path, framed by two pines: the open gable entry with its stick-clad sliding doors, looking straight down the aisle, black pipe runs on both sides. The ridge carries only the long low open clerestory strip that runs along the roof; there is NO cupola, lantern or raised box at the gable peak',
}
BRIEF = ('Turn the FIRST image, an exact 3D model render, into an architectural photograph taken at standing eye level, perfectly STRAIGHT ON: the camera is level and square to the facade, verticals stay vertical, the roof line stays horizontal and centred, a true frontal elevation. It shows {side}. '
 'STRICT: keep the camera, the horizon, the terrain and every wall, roof, truss, opening, fence, gate, trough and tree exactly where they are, '
 'same size, shape and count; add no building. The stable: walls of light tan stacked fieldstone to 5 ft, a black steel pipe rail floating 1 ft above '
 'the stone, then up to the eave panels of thin HORIZONTAL wooden branches (bird nest style) in slim dark steel frames, 3 ft wide; 6 in black steel '
 'pipe posts; the big sliding doors and the gable triangles above the trusses are clad in the same horizontal sticks in steel frames, every stick cut to the same length; dark charcoal corrugated metal roof; a small raised open clerestory roof along the ridge; the plastered rooms are warm lime-washed '
 'straw bale. All fences and gates are black steel pipe. '
 'The OTHER images are real photos of this exact site in Baja California: use them ONLY for the landscape, light and colour: the rounded granite '
 'hills, the soil, the shrubs, the vineyards. Do not copy any building from them. Season: late spring, a little green: fresh green in the low '
 'ground and grass tips among golden dry grass, not lush. Golden hour, warm low sun, long soft shadows, a sky of big lit cumulus clouds. '
 'Two or three horses in the runs or being led, one person, maybe a ranch dog, all at true scale. Photoreal, high-end architectural photography.')
REFS = [os.path.join(HERE, 'site-ref-0576.jpg'), os.path.join(HERE, 'site-ref-0577.jpg')]
EXTRA = {   # per-view fixes from the gallery notes
 'el-east': ' Two pine trees stand in the foreground, one at the LEFT edge and one at the RIGHT edge of the frame, exactly where the render shows their trunks and crowns: keep BOTH pines, framing the stable (Will, 3 Oct: "I liked when it had two pine trees in the front").',
}
if __name__ == '__main__':
    eng = sys.argv[1]; views = sys.argv[2:] or list(SIDE)
    k = key('OPENAI_API_KEY') if eng == 'openai' else gemini_key()
    EL_OUT = os.path.join(HERE, os.environ.get('EL_OUT', 'elevations')); os.makedirs(EL_OUT, exist_ok=True)   # 3 Oct: EL_OUT keeps earlier rounds
    for v in views:
        t = time.time()
        try:
            im = (openai if eng == 'openai' else google)(os.path.join(HERE, 'model', f'model-{v}.png'), BRIEF.format(side=SIDE[v]) + EXTRA.get(v, ''), REFS, k)
            im.save(os.path.join(EL_OUT, f'{v}-{eng}.png')); print(v, eng, 'ok', round(time.time() - t))
        except Exception as e: print(v, eng, 'FAILED', str(e)[:200])
