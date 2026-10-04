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
SRC, OUT = os.path.join(HERE, os.environ.get('GAL_SRC', 'model')), os.path.join(HERE, os.environ.get('GAL_OUT', 'gallery3')); os.makedirs(OUT, exist_ok=True)   # 3 Oct: GAL_OUT=gallery4 keeps earlier rounds
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

BLOCK3 = ('This render is an exact 3D model: ONE rectangular block of land cut out of the ground, floating on a plain white background, like a '
    'high-end architectural presentation model photographed in a studio. Show exactly one block, once, exactly where it is: no copy, no second block. '
    'Keep the block outline, the camera, the terrain on top and every building, roof, road, fence, trough, tree and vehicle exactly where it is, with '
    'the same size, shape and count; add or move nothing built. The top is photoreal at golden hour: dry golden grass, sage scrub and granite '
    'boulders, pale dirt roads, the tan stone stable with its dark charcoal roof, the covered stalls with a galvanised butterfly roof, BLACK pipe '
    'fences everywhere, sand arena and round pen, a small grove of round pines, vineyard rows where shown, the white trailer (no sign) with its '
    'wooden deck and steps. Tiny horses, riders and people at true scale. The four cut sides are smooth plain light grey, no soil or texture. The '
    'background is pure white with a soft shadow under the block.')

PICNIC = (' Focus on the wooden deck and the three curved, stepped wooden platforms in front of the white trailer (plain weathered white, no sign, no '
    'lettering): families and friends having a picnic on them, sitting on blankets and cushions on the wide steps, a basket, food and drinks, kids, '
    'someone leaning on the rail, all watching a rider in the arena. Keep the platforms exactly the shape and height the render shows.')

EXTRA = {   # per-view fixes from the gallery notes (28 Sep)
    '16-stable-sw': ' Behind the stable is the vineyard (rows of vines on the slope) exactly where the render shows it, NOT an arena. No fence and no shadow across the dirt road in the foreground.',
    '11-arena': ' The camera stands inside the arena looking out: keep the far buildings small and exactly where the render has them; the white trailer with its deck and steps stays a trailer, not a building. The two plastered rooms (wash and tack) sit at the WEST end of the stable’s south side, by the road, exactly where the render has them.',
    '10-stable-aisle': ' This is INSIDE the stable, down its aisle: low walls of tan stacked fieldstone between the stalls, black steel pipe stall fronts with swinging pipe gates, exposed dark STEEL trusses and a dark corrugated roof, light coming through the open clerestory and the stick panels, a plastered room with a door on the right, packed-earth aisle floor. Horses looking out over the gates, a person leading a horse down the aisle, a dog. Keep every wall, gate, truss and opening exactly where the render has it.',
    '4-hill-s': ' Keep the stable, the covered stalls and every road exactly as small and as placed as in the render. The two plastered rooms (wash and tack) sit at the WEST end of the stable’s south side, by the road, exactly where the render has them.',
    # 3 Oct gallery notes (Will)
    '18-stable-west-elev': ' At this corner the plastered wash room has ONE outside opening 6 ft wide and 9 ft tall with a WOODEN PLANK SLIDING DOOR hung on a steel track above it, slid open to the right (east) of the opening over the plastered wall, exactly as the render shows; the opening gives onto a flat concrete pad 12 ft by 24 ft along the stable wall, with a low fieldstone water trough along the pad’s west edge running out from the building corner. There is NO metal roof, canopy or shed on this side.',
    '8-stable': ' The stable’s runs and stalls hold horses only: NO hay, NO alfalfa bales anywhere in or around the stable (alfalfa lives only at the covered stalls far away). The ground in front is plain dry grass and dirt exactly as the render shows it: no gully, ditch, wash or draw. The old white semi-trailer stays exactly where and as the render shows it, a plain weathered white box trailer, no sign (Will, 3 Oct).',
    '20-front-yard': ' Two low beds of grey-green native shrubs (sage, buckwheat, brittlebush, knee-high mounds) flank the dirt drive-in between the long stone trough and the stable’s west gable, exactly where the render shows the rounded mounds: nothing taller than 3 ft, no lawn, no flowers, the rest of the ground stays dry grass and dirt (Will, 3 Oct).',
    '6-west': ' Two low beds of grey-green native shrubs (sage, buckwheat, brittlebush, knee-high mounds) flank the dirt drive-in between the long stone trough and the stable’s west gable, exactly where the render shows the rounded mounds: nothing taller than 3 ft, no lawn (Will, 3 Oct).',
    '14-bleachers-high': ' The deck and the three curved stepped platforms are NATURAL WOOD: warm weathered timber planks, no paint, no white, no rendered or concrete surfaces (Walker, 3 Oct).',
    'b5-top': ' This is a straight-down plan of the floating block: keep it exactly top-down, square to the frame, the whole rectangle visible with white margin all round; nothing cropped.',
    'b3-sw': ' The small boxes in the parking strip are CARS and PICKUPS, never tanks or farm machinery. The riding track and its infield are well vegetated with sage scrub and grasses. The blue area in the low spot below the track is shallow standing water in a natural sink: paint it as water.',
    'wash-farrier': ' THE SCENE: the concrete wash pad beside the stable under a steel pipe pergola covered by a living GRAPEVINE: broad green vine leaves overhead and ripe pale GREEN grape bunches (white wine grapes, no purple) hanging down through the pipes, dappled golden light on the concrete. On the pad a calm bay horse stands on all four legs, its whole body side-on to the camera and parallel to the stable wall, its head tied short to the bent black steel pipe hoop. The farrier works at its hind end the real way: he stands beside the hind leg facing the horse’s tail, bent forward with his back flat, the horse’s lower hind leg lifted and cradled across his thighs just above his knees, hoof sole up, rasp in hand; his leather apron on, his tool box on the concrete behind him. A rider stands at the horse’s head holding the lead rope. Horse and people at true scale, fully on the concrete pad, nothing floating or overlapping. At the end of the stone trough a small lower stone basin catches a thin stream of water pouring from a stone spout. Keep the plastered wash room wall, its wooden plank sliding door and every pipe exactly where the render has them.',
    '5-corridor-out': ' The camera is under the butterfly roof at eye level looking down the corridor, which runs straight through to the far open end; the alfalfa bales sit behind pipe panels on BOTH sides of the far bay, never across the corridor.',

}

if __name__ == '__main__':
    k = key('OPENAI_API_KEY') if ENGINE == 'openai' else gemini_key()
    if not k: sys.exit('no key for ' + ENGINE)
    for v in (ONLY or VIEWS):
        t = time.time()
        try:
            im = (openai if ENGINE == 'openai' else google)(os.path.join(SRC, f'model-{v}.png'), (BLOCK3 + (' This view looks STRAIGHT DOWN from directly above: keep it exactly top-down, a flat plan, no tilt or perspective.' if v == 'b7-plan' else '')) if v.startswith('b') else BRIEF + (PICNIC if v.split('-fan-')[0] in ('14-bleachers-high', '19-spiral', '22-picnic', '23-picnic-side') else '') + EXTRA.get(v, EXTRA.get(v.split('-fan-')[0], '')), [], k)   # fans (`<base>-fan-<tag>`) use their base view's notes
            im.save(os.path.join(OUT, f'{v}-{ENGINE}.png')); print(f'{v} {ENGINE}: ok in {time.time() - t:.0f}s')
        except Exception as e: print(f'{v} {ENGINE}: FAILED {str(e)[:160]}')
