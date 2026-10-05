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
 'el-south-sun': None, 'el-west-horse': None,
 'el-north': 'the long NORTH side of the stable: six stalls, each opening through a 6 x 9 ft open doorway to its own 12 x 40 ft run fenced in black steel pipe, the runs in front of the camera; at the right (west) end a plastered kitchen bay with no run in front of it',
 'el-south': 'the long SOUTH side of the stable: at the left end three plastered bays (the corner bay with the bathroom and electrical room, then the wash room with a wooden sliding door beside its opening, then tack), all fronting one long concrete pad under a steel pipe pergola with a grapevine, a low fieldstone trough out from the building corner; then four stalls opening to their runs that climb the slope toward the camera, fenced in black steel pipe; the long low tan fieldstone water trough at far left',
 'el-west': 'the WEST end of the stable, its main entry: the open gable entry with its stick-clad sliding doors slid aside, the dirt road sweeping in from the left into the aisle, plastered rooms closing both corners of the gable (on the left the kitchen with a small window, on the right the bathroom and electrical room with a small plank door); the stick-clad sliding doors and the stick panels in the gable triangle are backed on the inside with milky translucent corrugated polycarbonate, so the sticks read against a soft pale glow rather than open air; and in the foreground the long low tan fieldstone water trough running across the whole view, acting as a low retaining wall',
 'el-south-wash': 'the WEST end of the stable’s long SOUTH side, square on, centred on the plastered wash room: its one wide 6 x 9 ft doorway opening onto a flat concrete pad 12 x 24 ft that runs along the wall, a low tan fieldstone water trough 12 ft long along the outer edge of that pad (a horse drinks from it), the tack room wall beside it, and to the right the stalls with their black pipe runs climbing the slope; the white trailer far off on the left',
 'el-east': 'the EAST end of the stable from the parking path, framed by two pines: the open gable entry with its stick-clad sliding doors, looking straight down the aisle, black pipe runs on both sides. The ridge carries only the long low open clerestory strip that runs along the roof; there is NO cupola, lantern or raised box at the gable peak',
}
BRIEF = ('Turn the FIRST image, an exact 3D model render, into an architectural photograph taken at standing eye level, perfectly STRAIGHT ON: the camera is level and square to the facade, verticals stay vertical, the roof line stays horizontal and centred, a true frontal elevation. It shows {side}. '
 'STRICT: keep the camera, the horizon, the terrain and every wall, roof, truss, opening, fence, gate, trough and tree exactly where they are, '
 'same size, shape and count; add no building. The stable: walls of light tan stacked fieldstone to 5 ft, then, sitting RIGHT ON the stone with no gap, no rail and no bottom frame, '
 'thin HORIZONTAL wooden branches (bird nest style) up to the eave, fitted between slim fixed dark steel verticals every 3 ft; heavy 12 in black steel '
 'tube posts; the big sliding doors and the gable triangles above the trusses are clad in the same horizontal sticks in steel frames, every stick cut to the same length; dark charcoal corrugated metal roof; a small raised open clerestory roof along the ridge; the plastered rooms are warm lime-washed '
 'straw bale. All fences and gates are black steel pipe. '
 'The OTHER images are real photos of this exact site in Baja California: use them ONLY for the landscape, light and colour: the rounded granite '
 'hills, the soil, the shrubs, the vineyards. Do not copy any building from them. Season: late spring, a little green: fresh green in the low '
 'ground and grass tips among golden dry grass, not lush. Golden hour, warm low sun, long soft shadows, a sky of big lit cumulus clouds. '
 'Two or three horses in the runs or being led, one person, maybe a ranch dog, all at true scale. Photoreal, high-end architectural photography.')
REFS = [os.path.join(HERE, 'site-ref-0576.jpg'), os.path.join(HERE, 'site-ref-0577.jpg')]
EXTRA = {   # per-view fixes from the gallery notes
 'el-south-sun': ' LIGHT, overriding anything above: this one is shot in BRIGHT late-morning sun, high clear light, well exposed and airy, a pale blue sky with a few small white clouds; nothing dark, no dusk, no long golden shadows (Will, 3 Oct: "sunnier, it always looks dark").',
 'el-west-horse': ' The dirt entry drive is 14 ft wide and runs from the trough straight into the gable, LINED on BOTH sides with a mixed row of native plants exactly where the render shows the mounds: sage, buckwheat, deer grass, brittlebush, a few taller accents, varied sizes and greens. The rounded mounds either side of the drive are SHRUBS: soft grey-green sage and buckwheat foliage, leafy, not rocks, not boulders, no stone anywhere on the ground except the trough wall. Add ONE horse standing just behind the long stone trough at the LOWER RIGHT of the frame, head down drinking from it, true to scale; the trough and everything else stay exactly as rendered (Will, 3 Oct).',
 'el-west': ' Two low beds of grey-green native shrubs (sage, buckwheat, brittlebush, knee-high rounded mounds) flank the dirt drive-in on both sides between the long stone trough in the foreground and the gable, exactly where the render shows the mounds: nothing taller than 3 ft, no lawn, no flowers; the rest stays dry grass and dirt (Will, 3 Oct, red markup).',
 'el-south-wash': ' The wash room’s 6 x 9 ft opening has a WOODEN PLANK SLIDING DOOR on a steel track above it, slid open to the right (east) of the opening over the plastered wall, exactly where the render shows it; a horse drinks from the low fieldstone trough along the west edge of the concrete pad (Will, 3 Oct).',
 'el-south': ' The wash room at the left end has a WOODEN PLANK SLIDING DOOR on a steel track above its opening, slid open to the right of the opening, exactly where the render shows it; the low fieldstone trough runs along the west edge of the concrete pad, out from the building corner (Will, 3 Oct).',
 'el-east': ' Two pine trees stand in the foreground, one at the LEFT edge and one at the RIGHT edge of the frame, exactly where the render shows their trunks and crowns: keep BOTH pines, framing the stable (Will, 3 Oct: "I liked when it had two pine trees in the front").',
}
if __name__ == '__main__':
    eng = sys.argv[1]; views = sys.argv[2:] or list(SIDE)
    k = key('OPENAI_API_KEY') if eng == 'openai' else gemini_key()
    EL_OUT = os.path.join(HERE, os.environ.get('EL_OUT', 'elevations')); os.makedirs(EL_OUT, exist_ok=True)   # 3 Oct: EL_OUT keeps earlier rounds
    for v in views:
        t = time.time()
        try:
            im = (openai if eng == 'openai' else google)(os.path.join(HERE, 'model', f'model-{v}.png'), BRIEF.format(side=SIDE[v] or SIDE[v.rsplit('-', 1)[0]]) + EXTRA.get(v, ''), REFS, k)
            im.save(os.path.join(EL_OUT, f'{v}-{eng}.png')); print(v, eng, 'ok', round(time.time() - t))
        except Exception as e: print(v, eng, 'FAILED', str(e)[:200])
