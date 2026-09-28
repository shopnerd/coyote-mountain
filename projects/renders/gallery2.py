"""The big gallery (27 Sep): every model render (renders/model/) finished by BOTH painters, OpenAI gpt-image-2 and Google
Gemini, with people and animals (Will). Money shots keep the camera and everything built; the b-views are the site as a
photoreal cut-out block of land floating on white.

    python gallery2.py <openai|google> [view-id ...]   ->  gallery2/<view>-<engine>.png
The Gemini key is read from Will's notes file (never printed) unless GEMINI_API_KEY is set.
"""
import os, re, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import paint
from paint import openai, google, key
from finish import BRIEF
paint.QUAL = 'high'
SRC, OUT = os.path.join(HERE, 'model'), os.path.join(HERE, 'gallery2'); os.makedirs(OUT, exist_ok=True)
ENGINE = sys.argv[1]; ONLY = sys.argv[2:]
LIFE = (' Bring the place to life, at true scale and only on the ground, in the arena, on the roads and inside the stalls and runs: horses (bay, chestnut, '
        'grey) in several stalls and runs, a rider on a horse in the arena, a person leading a horse along a road, one or two people working at the stable and '
        'the covered stalls, a ranch dog. People and animals are the only things you may add.')
BLOCK = ('This image is a render of an accurate 3D model: a rectangular block of land cut out of the ground, floating in a plain white void, with an '
         'equestrian centre built on it. Make it a photorealistic image of that block, like a high-end architectural visualisation. KEEP EXACTLY: the block\'s '
         'outline and the camera; the terrain on top; every building, roof, fence, road and trough, with the same count, position, size and shape; add no '
         'building, fence or road. The top is the real place in golden-hour light: dry golden grass, olive scrub and granite boulders, compacted pale dirt '
         'roads, the stone-and-tomato-stake stable with its dark corrugated roof and clerestory and black-fenced runs on both sides, the covered stalls with '
         'their white pipe panels and matte corrugated butterfly roof, the sand arena and round pen with white fences, vineyard rows where the render shows '
         'them. The four cut sides are smooth, plain light grey, like the base of an '
         'architectural presentation model: no soil, no layers, no texture (Will, 27 Sep). The background stays pure, empty white with only a soft shadow directly under the block.')
def gemini_key():
    k = os.environ.get('GEMINI_API_KEY') or key('GEMINI_API_KEY')
    if k: return k
    t = open(r'G:\My Drive\Claude Private\SECRETS\note_PAD\Google studio.txt', encoding='utf-8').read()
    m = re.search(r'\b(AQ\.[A-Za-z0-9_\-]{20,}|AIza[0-9A-Za-z_\-]{30,})', t); return m.group(1) if m else None
BLEACH = (' The long box is an old 40 ft semi-trailer, textured in the render with photographs of the real one: keep it exactly as it appears - faded white '
          'horizontally corrugated aluminium sides with a weathered ochre stripe near the top, rusty ochre ends with a boarded wooden hatch. The hand-painted '
          'sign on its side (cream panel, red border, CENTRO EQUINO in red, CHICHIHUAS in green, small ochre stars and red scrolls) is already painted on: keep '
          'its position, size, colours and spelling exactly, just give it the look of real brush-painted enamel on corrugated metal. In front of the trailer, '
          'facing the arena: a flat weathered-wood deck about 4 ft high and 6 ft deep running the full length of the trailer, and stepping down from it toward '
          'the arena three CURVED, FANNED sections of wide wooden terrace steps, like overlapping fan blades or a spiral of scallops, each with a curved front '
          'edge, set on slim steel legs; NO spiral staircase. A corrugated metal shade roof on slim steel posts runs off the top of the trailer over the deck '
          'along its whole length. People sit and lounge on the wide steps watching a rider in the arena; a family has a picnic on one of the wide curved steps.')
RAIN = (' It is just after a rain, late afternoon: the sky clearing with broken clouds and low golden light, the ground darkened and damp, roofs wet and '
        'glinting. Standing water ONLY where the render shows blue water: a shallow pond filling the natural low spot, water running in the drainage ditches; '
        'besides that only small puddles in road ruts. Keep every building, road, fence and ditch exactly where the render has it.')
TROUGH = (' At the end of the covered stalls the round water trough is low and built of rounded field stone with a stone cap, iron tie rings set in its '
          'side; a horse or two is tied at it, drinking.')
STABLE = (' The stable (27 Sep design): a 5 ft stacked fieldstone wall all round in fairly uniform light tan / buff stone; a black steel pipe floats 1 ft above the stone on short posts, '
          'and above it, up to the eave, panels of thin horizontal wooden branches/tomato stakes held in slim dark steel frames, loose and organic like a '
          'bird nest screen, in 3 ft wide panels. The clerestory along the ridge is OPEN, no glass: just posts under its little roof. Inside, exposed timber roof trusses on timber posts. The two rooms at the road end (rendered plain beige) are solid, '
          'lime-plastered straw bale or cob, with one wooden door. Each gable end has a big wooden sliding barn door on a '
          'steel track, shown slid open. Each stall opens straight out to its run through an open doorway with a steel lintel, NO gate there; toward the aisle the stalls have black pipe fronts with pipe gates. Horses stand in the black pipe-fenced runs.')
AISLE = (' This is inside the stable, down its 14 ft aisle under exposed timber trusses: both sides are stall fronts of black steel pipe with a pipe '
         'gate each, horses looking out; the plain walls are the plastered tack room. Add NO water tank, tub or trough; the aisle floor is packed earth.')

WIDE = ('1-hero-sw', '3-site-ne', '12-high-south', '9-arrival', '11-arena', '6-west', '4-hill-s', 'r2-sink-rain', 'r3-stable-rain', '8-stable', '18-stable-west-elev', '2-corridor', '5-corridor-out')   # views where the stable shows
# 28 Sep: fixes from Will's and Walker's gallery notes, for every view
NOTES = (' Keep to the render: add NO building, arena, fence, tank, machinery or vehicle that it does not show (people and animals only). The small '
         'boxes in the parking area are parked cars and pickups, nothing else; no car next to the stable. The few round green trees between the parking area and the stable are a SMALL grove of modest, round-crowned pines (15-22 ft), the walking path running through it; there is NO big forest anywhere. The large '
         'rounded-rectangle dirt track in the west is a riding trail around NATURAL ground: keep its inside natural, dry grass, scrub and oaks as the photo '
         'shows, never a sand arena; the blue patch below it is the natural low spot where rain water pools. The long, low rectangular stone water trough (same tan fieldstone as the stable wall, about 40 ft, in two level sections stepping up the slope) stands along the inside of the west road, well away from the stable front, which stays open so you can drive right up to the stable. The '
         'round stone trough at the end of the covered stalls sits right under the end of the butterfly roof gutter chute. The covered stalls have a '
         'butterfly (V) roof, white pipe panels, and stand where the render puts them. The old white semi-trailer, when it shows, is the photographed one '
         'with the hand-painted sign, with the wooden bleachers, spiral stair and shade roof in front of it. People and horses at true scale (a horse is '
         'about 5 ft at the withers); nothing oversized.')
WASH = (' At the road end of the stable, the south wall of the plastered rooms has one wide wooden door, 6 ft wide and 9 ft tall, into the wash room, opening '
        'onto a 12 x 24 ft concrete pad along the wall.')

if __name__ == '__main__':
    k = key('OPENAI_API_KEY') if ENGINE == 'openai' else gemini_key()
    if not k: sys.exit('no key for ' + ENGINE)
    for f in sorted(os.listdir(SRC)):
        if not (f.startswith('model-') and f.endswith('.png')): continue
        v = f[6:-4]
        if ONLY and v not in ONLY: continue
        blockv = v.startswith('b')
        prompt = (BLOCK if blockv else BRIEF) + LIFE + (' This view looks straight down from above: keep it exactly top-down.' if v in ('7-plan', 'b5-top') else '') + (BLEACH if ('bleachers' in v or v == '19-spiral') else '') + (RAIN if 'rain' in v else '') + (STABLE if ('stable' in v or v in WIDE) else '') + (AISLE if v == '10-stable-aisle' else '') + (TROUGH if v in ('2-corridor', '5-corridor-out', '1-hero-sw') else '') + NOTES + (WASH if v in ('18-stable-west-elev', '16-stable-sw', 'r3-stable-rain') else '')
        t = time.time()
        try:
            im = openai(os.path.join(SRC, f), prompt, [], k) if ENGINE == 'openai' else google(os.path.join(SRC, f), prompt, [], k)
            im.save(os.path.join(OUT, f'{v}-{ENGINE}.png')); print(f'{v} {ENGINE}: ok in {time.time() - t:.0f}s')
        except Exception as e: print(f'{v} {ENGINE}: FAILED {str(e)[:200]}')
