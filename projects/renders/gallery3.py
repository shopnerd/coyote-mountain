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
    'THE BACKGROUND IS THE RENDER’S TOO: everything behind the subject, the hills, the skyline, roads, fences and any buildings, stays exactly as the render shows it, in the same place and size. The descriptions below say what each thing is made of, NOT that it is in this view: if a building described below does not appear in the render, it is not in this picture, so do not paint it. Never invent a stable, barn, shed, car park, trees or a second building in the background.\n'
    'Materials: the ground is dry golden grass, sage scrub and granite boulders, with the colours of the aerial photo it is draped with; dirt roads '
    'are pale compacted earth. The large stable has walls of light tan stacked fieldstone to about 5 ft and, sitting right on the stone with no gap and no rail, thin '
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

PICNIC = (' Focus on the wooden deck and the three curved, stepped platforms with fieldstone sides and plank tops in front of the white trailer (plain weathered white, no sign, no '
    'lettering): families and friends having a picnic on them, sitting on blankets and cushions on the wide steps, a basket, food and drinks, kids, '
    'someone leaning on the rail, all watching a rider in the arena. Keep the platforms exactly the shape and height the render shows.')

EXTRA = {   # per-view fixes from the gallery notes (28 Sep)
    '16-stable-sw': ' Behind the stable is the vineyard (rows of vines on the slope) exactly where the render shows it, NOT an arena. No fence and no shadow across the dirt road in the foreground.',
    '11-arena': ' The camera stands inside the arena looking out: keep the far buildings small and exactly where the render has them; the white trailer with its deck and steps stays a trailer, not a building. The plastered rooms (kitchen, bathroom and electrical room in the end bay, then wash and tack) close the WEST end of the stable by the road, exactly where the render has them.',
    '10-stable-aisle': ' This is INSIDE the stable, down its aisle: low walls of tan stacked fieldstone between the stalls, black steel pipe stall fronts with swinging pipe gates, exposed dark STEEL trusses and a dark corrugated roof, light coming through the open clerestory and the stick panels, a plastered room with a door on the right, packed-earth aisle floor. Horses looking out over the gates, a person leading a horse down the aisle, a dog. Keep every wall, gate, truss and opening exactly where the render has it.',
    '4-hill-s': ' Keep the stable, the covered stalls and every road exactly as small and as placed as in the render. The plastered rooms (kitchen, bathroom and electrical room in the end bay, then wash and tack) close the WEST end of the stable by the road, exactly where the render has them. The covered stalls are the current design: a butterfly (V) roof, the corridor open straight through, the alfalfa stacked only in the two bays at the far end behind black pipe panels, and at this near end the ROUND FIELDSTONE trough (not a metal tank) with the roof chute pouring into it; no downspout pipe. The stable beyond has its plastered wash room with a grape-covered pergola over the concrete pad.',
    # 3 Oct gallery notes (Will)
    '18-stable-west-elev': ' At this corner the plastered wash room has ONE outside opening 6 ft wide and 9 ft tall with a WOODEN PLANK SLIDING DOOR hung on a steel track above it, slid open to the right (east) of the opening over the plastered wall, exactly as the render shows; the opening gives onto a flat concrete pad 12 ft by 24 ft along the stable wall, with a low fieldstone water trough along the pad’s west edge running out from the building corner. There is NO metal roof, canopy or shed on this side.',
    '8-stable': ' The stable’s runs and stalls hold horses only: NO hay, NO alfalfa bales anywhere in or around the stable (alfalfa lives only at the covered stalls far away). The ground in front is plain dry grass and dirt exactly as the render shows it: no gully, ditch, wash or draw. The old white semi-trailer stays exactly where and as the render shows it, a plain weathered white box trailer, no sign (Will, 3 Oct).',
    '20-front-yard': ' Two low beds of grey-green native shrubs (sage, buckwheat, brittlebush, knee-high mounds) flank the dirt drive-in between the long stone trough and the stable’s west gable, exactly where the render shows the rounded mounds: nothing taller than 3 ft, no lawn, no flowers, the rest of the ground stays dry grass and dirt (Will, 3 Oct).',
    '6-west': ' Two low beds of grey-green native shrubs (sage, buckwheat, brittlebush, knee-high mounds) flank the dirt drive-in between the long stone trough and the stable’s west gable, exactly where the render shows the rounded mounds: nothing taller than 3 ft, no lawn (Will, 3 Oct).',
    '14-bleachers-high': ' The deck and the three curved stepped platforms are NATURAL WOOD: warm weathered timber planks, no paint, no white, no rendered or concrete surfaces (Walker, 3 Oct).',
    'b5-top': ' This is a straight-down plan of the floating block: keep it exactly top-down, square to the frame, the whole rectangle visible with white margin all round; nothing cropped.',
    'b3-sw': ' The small boxes in the parking strip are CARS and PICKUPS, never tanks or farm machinery. The riding track and its infield are well vegetated with sage scrub and grasses. The blue area in the low spot below the track is shallow standing water in a natural sink: paint it as water.',
    'wash-farrier': ' THE SCENE: the concrete wash pad beside the stable under a steel pipe pergola covered by a living GRAPEVINE: broad green vine leaves overhead and ripe pale GREEN grape bunches (white wine grapes, no purple) hanging down through the pipes, dappled golden light on the concrete. On the pad a calm bay horse stands on all four legs, its whole body side-on to the camera and parallel to the stable wall, its head tied short to the bent black steel pipe hoop. The farrier works at its hind end the real way: he stands beside the hind leg facing the horse’s tail, bent forward with his back flat, the horse’s lower hind leg lifted and cradled across his thighs just above his knees, hoof sole up, rasp in hand; his leather apron on, his tool box on the concrete behind him. A rider stands at the horse’s head holding the lead rope. Horse and people at true scale, fully on the concrete pad, nothing floating or overlapping. At the end of the stone trough a small lower stone basin catches a thin stream of water pouring from a stone spout. Keep the plastered wash room wall, its wooden plank sliding door and every pipe exactly where the render has them.',
    '1-hero-sw': ' The covered stalls corridor runs straight through and is OPEN at this end: no wall, block, pillar or stone mass closes it; between the last two stall posts there is only open air, with the round fieldstone trough standing free in front of the opening and the roof chute pouring into it. Pipe stall fronts and panels only, no stone walls anywhere on the covered stalls.',
    'cafe-end': ' STONE RISERS, IMPORTANT: the side faces of every deck, every stair step and every curved picnic platform are TAN STACKED FIELDSTONE, the same rough stone as the stable walls and the troughs; ONLY their flat tops are wooden planks. No wooden or plank sides anywhere on the decks, steps or platforms.  THE VIEW: the end of the old white semi-trailer (a plain weathered box trailer, keep its rusty rear doors exactly), now a DOUBLE-SIDED café: a wooden deck on EACH long side, one gable roof over the trailer and both decks, covered on both slopes with black solar panels (the dark roof in the render), with a serving window and stools on each side, and each side fanning out into three curved stepped picnic platforms (stone sides, plank tops) with families on blankets; At this end there is NO stair: a short wooden deck runs across the trailer end and is closed by a chest-high fieldstone wall with a wooden cap, NO seats or stools at it, and above the cap the WHOLE gable face, up to the roof and into the peak, is a close screen of thin horizontal wooden sticks in dark steel frames (like the stable walls); the old trailer end is NOT visible from this side at all; against the outside of that wall, a fieldstone horse trough at horse height (17 ft long, rim 30 in): open water at both ends where a horse can drink, and in its middle, only along the BACK half against the wall, a clump of tall green water plants (papyrus, horsetail, cattails 4 to 7 ft); the FRONT half of the trough is open water along its whole length; a downspout from the café roof gutter comes down beside each END of the trough, outside it. Keep the trailer, decks, stairs, trough and platforms exactly as the render shows.',
    '23-picnic-side': ' STONE RISERS, IMPORTANT: the side faces of every deck, every stair step and every curved picnic platform are TAN STACKED FIELDSTONE, the same rough stone as the stable walls and the troughs; ONLY their flat tops are wooden planks. No wooden or plank sides anywhere on the decks, steps or platforms.  The old white trailer is a DOUBLE-SIDED café: a serving window on BOTH long sides, each side with its own wooden deck, shade roof and three curved stepped picnic platforms (stone sides, plank tops), and at each end of the trailer one wide wooden stair up to the decks, exactly as the render shows. The ground inside the fenced arena is groomed riding sand, freshly raked in fine even parallel lines (harrowed footing), pale and clean, no grass and no weeds inside the fence. The old white trailer has become a small café: a serving window opened in its side with a hinged wooden awning, a few stools at a narrow wooden counter, warm light inside, and ONE small, simple, tasteful hand-painted wooden sign above the window reading CAFÉ in plain lettering, nothing else, no logos, no neon, no banners.',
    '5-corridor-out': ' The camera is under the butterfly roof at eye level looking down the corridor, which runs straight through to the far open end; the alfalfa bales sit behind pipe panels on BOTH sides of the far bay, never across the corridor.',

}

# 4 Oct: the hybrid brief (Will liked both halves of the A/B test): the topo app's short factual scene + the aerial photo, plus one
# precise sentence for the posed figures. GAL_STYLE=hybrid uses it for views listed here; others keep BRIEF.
AERIAL = os.path.join(HERE, '..', 'viewer', 'aerial-src.jpg')
HYB = {
 'wash-farrier': (
  'Make the first image a photograph of the real place. October, late afternoon golden hour before sunset, fair-weather cumulus clouds. '
  'The place is Centro Equino, a small horse ranch in the dry granite hills of the Valle de Guadalupe, Baja California; the second image is '
  'the aerial photo of the site, use it for the colours of the ground and scrub. '
  'Built here, drawn as plain solids in the first image: keep each exact shape, size and place. A stone and timber horse stable 72 ft long, '
  'its end room plastered with a wooden plank sliding door; a 12 by 24 ft concrete wash pad in front of it; over the pad a steel pipe pergola '
  '10 ft tall covered by a grapevine with pale green grapes; a bent black pipe tie hoop in the middle of the pad; a fieldstone water trough '
  '14 ft long along the pad edge, its water pouring from a stone spout into a small lower stone basin at its end; black steel pipe fences. '
  'The plain pale figures on the pad are a horse, a farrier and a rider: keep each exactly where it stands and in its pose, and paint them as a '
  'real bay horse and real people at true scale. The horse stands in the bay between the black pipe hoop and the fence, head to the wall, tied '
  'to the hoop; the farrier is beside its lifted near hind leg facing the tail, bent forward with a flat back, the hoof across his thighs, '
  'sole up; the rider stands at its head holding the lead rope.'),
}
STYLE = os.environ.get('GAL_STYLE', '')
# 4 Oct (Will: "the background seems like the wrong view"): the brief describes every building on the site, and the painters paint
# them into empty backgrounds. modelshots.mjs now writes model-<view>.vis.json (objects in frame and their share of the picture);
# fit_brief() drops the sentences about things outside the frame and says what the frame does contain.
import json as _js, re as _re
VIS_WORDS = {'walker barn 72x40': ('The large stable', 'stable'), 'covered stalls': ('The open shed with the butterfly', 'covered stalls'),
             'trailer 8 x 40': ('The old white semi-trailer', 'café trailer'), 'bleachers': ('The old white semi-trailer', 'café decks and picnic platforms'),
             'stone trough (long)': ('The long low box', 'long stone trough'), 'arena fence': ('The oval with the fence', 'riding arena'),
             'round pen fence': ('The oval with the fence', 'round pen'), 'pine forest': ('The round trees', 'pine grove')}
def fit_brief(text, vid):
    f = os.path.join(SRC, f'model-{vid}.vis.json')
    if not os.path.exists(f): return text
    vis = _js.load(open(f)); keep = {k for k in vis if k in VIS_WORDS}
    for name, (lead, _) in VIS_WORDS.items():
        if any(VIS_WORDS[k][0] == lead for k in keep): continue
        text = _re.sub(_re.escape(lead) + r'[^.]*\.\s*', '', text)                     # the sentence about something not in frame
    seen = sorted({VIS_WORDS[k][1] for k in keep}, key=lambda s: -max(vis[k] for k in keep if VIS_WORDS[k][1] == s))
    return text + (' IN THIS FRAME there is only: ' + ', '.join(seen) + ', plus open ground, roads and fences. Nothing else is built in this picture: the background is open land, scrub and hills.' if seen else
                   ' Nothing built is in this frame beyond what the render shows: the background is open land, scrub and hills.')
# 4 Oct (Will: 'solar on'): model shots show the phase-1 panels; tell the painter what the dark block on the stable roof is
SOLAR = ' Black solar panels cover both slopes of the stable roof (either side of the long open clerestory) and both planes of the covered stalls’ butterfly roof, exactly where the render shows the dark panel fields; and on the café’s gable roof where the render shows them; nowhere else.'
# 4 Oct (Will: OpenAI looks flat; try other times of day and weather): the light fan. A fan view tagged with one of these keys swaps
# the brief's light sentence; fan.py --light also moves the model's sun to the matching hour so the shadows are true.
LIGHT_DEFAULT = 'Light: warm low golden-hour sun, long soft shadows, a sky with big lit cumulus clouds.'
LIGHT = {
 'dawn':   (7.3,  'Light: just after sunrise, the low sun from the east raking across the land, long cool blue shadows, a little morning haze in the valley, a pale gold sky.'),
 'golden': (17.7, 'Light: deep late golden hour, the sun just above the western hills, long dramatic raking shadows, strong warm contrast, glowing rim light on the horses and people, a rich sky with lit clouds.'),
 'storm':  (16.4, 'Light: a winter storm clearing, dark slate clouds breaking up with shafts of low sun through them, roofs and ground wet and glistening, puddles on the dirt roads, dramatic contrast.'),
 'blue':   (18.9, 'Light: blue hour just after sunset, a deep blue sky with a last orange band on the horizon, warm lights glowing inside the stable and the cafe, soft light without hard shadows.'),
 'fog':    (8.6,  'Light: early morning marine fog lifting off the valley, soft diffused light, the far hills fading into mist, damp ground, quiet.'),
 # 4 Oct (Will, night): the stable as a lantern, moody twilight
 'lantern': (19.1, 'Light: moody deep twilight, the last cold blue light after sunset, a dusky violet-blue sky with a faint ember line on the far hills, the land almost dark, no sun, no shadows. THE STABLE IS A LANTERN: soft warm amber light (2200 K) glows from INSIDE the stable and seeps out between the hundreds of thin, wiggly, irregular horizontal sticks of every wall panel and the gable ends, so each stick reads as a dark crooked silhouette against warm glowing gaps, like light through a bird nest or a woven basket; the glow is soft and diffuse, not bright beams; a little warm light spills onto the dirt and the fieldstone just below the walls and out of the open aisle doors, and a faint glow comes up through the open clerestory under the roof edge. Everything else stays dark and cool: no floodlights, no lamps outside, the hills and sky dark, maybe one or two quiet figures or a horse silhouetted at a doorway.'),
 # 4 Oct (Will): sheet E-1's dark-sky lighting, just after sundown: the hero is warm light pouring out between the stable's sticks
 'dusk':   (18.7, 'Light: early evening just after sundown, the sky a deep clear blue fading to a thin warm orange line over the western hills, the first star or two, the land in soft dusk with no hard shadows. The stable glows from inside: warm amber-gold light (2700 K) pours out between the thin horizontal sticks of its wall panels in fine glowing lines, and spills softly out of its open doorways and the open clerestory onto the dirt just around it; it is the brightest thing in the picture, a lantern. The covered stalls show a soft warm glow under their roof. Small amber lights at knee height dot the walking path between the pines and the stable, and a small shielded downlight over each stable door. Everything else stays DARK: no light on the roads, the arena, the round pen, the trees or the hills, no streetlights, no floodlights, no light shining up into the sky, the hills dark silhouettes. Calm, quiet, a few horses and people near the glowing stable.'),
}

# 5 Oct (Will): 'a few watercolor renderings'. The geometry rules above still hold; only the medium changes.
ART_STYLES = {
 'watercolor_night': ' STYLE, MOST IMPORTANT: this is NOT a photograph. Paint it as a hand-made WATERCOLOR NOCTURNE on cold-press cotton paper: '
   'it is NIGHT, so deep, layered washes of indigo, Payne’s grey and violet cover almost the whole sheet, wet-in-wet, with blooms in the dark sky and '
   'a few pinpricks of stars left as bare paper; the land is dark, the hills near-black silhouettes. The ONLY warm colour is the stable: soft amber-gold '
   'light glows from inside it and through the gaps between the thin wall sticks, bleeding gently into the surrounding dark washes, and a faint warm '
   'spill on the ground just around it. A light graphite underdrawing still shows on the roof lines and fences; the dark wash fades to bare paper only at the '
   'very edges. No other lights. Every building, roof, fence, road and tree stays exactly where and as the render shows: the same composition and camera.',
 'watercolor': ' STYLE, MOST IMPORTANT: this is NOT a photograph. Paint it as a loose, luminous hand-made architectural WATERCOLOR on '
   'cold-press cotton paper, like a landscape architect’s presentation sketch: transparent layered washes, a soft wet-in-wet sky with '
   'blooms, a light graphite pencil underdrawing still visible on the buildings, roof lines and fences, crisp dry-brush edges on the '
   'roofs and posts, granulating pigment in the shadows, white paper left bare for the brightest highlights, a little paint spatter, and '
   'the wash fading out into bare white paper toward the edges and corners (a vignette, no frame, no border, no signature, no text). '
   'Warm ochres, burnt sienna, sap green and ultramarine, the dry hills simplified into broad washes. Figures and horses as a few deft brush '
   'strokes. Every building, roof, wall, fence, road and trough stays exactly where and as the render shows: the same composition and camera.',
}

if __name__ == '__main__':
    k = key('OPENAI_API_KEY') if ENGINE == 'openai' else gemini_key()
    if not k: sys.exit('no key for ' + ENGINE)
    CAFE = {'23-picnic-side', 'cafe-end'}   # 4 Oct (Will): the trailer is a small cafe in these views, so drop the 'no sign' lines
    _BRIEF0, _HYB0 = BRIEF, dict(HYB)
    _o, _g = openai, google; CUR = ['']
    ART = ART_STYLES.get(os.environ.get('GAL_ART', ''), '')        # 5 Oct (Will): watercolor renderings; GAL_ART=watercolor
    art = lambda pr: (pr.replace('Photoreal, like a high-end architectural photograph.', '').replace('Photoreal, high-end architectural photography.', '') + ART) if ART else pr
    openai = lambda src, pr, refs, k_: _o(src, art(fit_brief(pr, CUR[0])), refs, k_)
    google = lambda src, pr, refs, k_, **kw: _g(src, art(fit_brief(pr, CUR[0])), refs, k_, **kw)
    for v in (ONLY or VIEWS):
        CUR[0] = v
        t = time.time()
        _lt = os.environ.get('GAL_LIGHT') or (v.split('-fan-')[1] if '-fan-' in v else '')   # 4 Oct: GAL_LIGHT = one light for a whole camera fan
        BRIEF = _BRIEF0.replace(LIGHT_DEFAULT, LIGHT[_lt][1]) if _lt in LIGHT else _BRIEF0
        HYB = {k_: (v_.replace('October, late afternoon golden hour before sunset, fair-weather cumulus clouds.', LIGHT[_lt][1]) if _lt in LIGHT else v_) for k_, v_ in _HYB0.items()}
        _base = v.split('-fan-')[0]
        if _base.startswith('el-'):                         # 4 Oct: elevations keep their own straight-on brief + site photos, light swapped for fans
            import elevations as EL
            _pr = EL.BRIEF.format(side=EL.SIDE.get(_base) or EL.SIDE[_base.rsplit('-', 1)[0]]) + EL.EXTRA.get(_base, '') + SOLAR
            if _lt in LIGHT: _pr = _pr.replace('Golden hour, warm low sun, long soft shadows, a sky of big lit cumulus clouds.', LIGHT[_lt][1])
            try:
                im = (openai if ENGINE == 'openai' else google)(os.path.join(SRC, f'model-{v}.png'), _pr, EL.REFS, k)
                im.save(os.path.join(OUT, f'{v}-{ENGINE}.png')); print(f'{v} {ENGINE} (elevation): ok in {time.time() - t:.0f}s')
            except Exception as e: print(f'{v} {ENGINE} (elevation): FAILED {str(e)[:160]}')
            continue
        hb = HYB.get(v, HYB.get(v.split('-fan-')[0])) if STYLE == 'hybrid' else None
        if hb:
            try:
                im = (openai if ENGINE == 'openai' else google)(os.path.join(SRC, f'model-{v}.png'), hb + SOLAR, [AERIAL], k)
                im.save(os.path.join(OUT, f'{v}-{ENGINE}.png')); print(f'{v} {ENGINE} (hybrid): ok in {time.time() - t:.0f}s')
            except Exception as e: print(f'{v} {ENGINE} (hybrid): FAILED {str(e)[:160]}')
            continue
        try:
            _pr = None
            im = (openai if ENGINE == 'openai' else google)(os.path.join(SRC, f'model-{v}.png'), (lambda t_: t_.replace('The old white semi-trailer keeps its photo texture exactly, with NO sign or lettering on it,', 'The old white semi-trailer is a small café,').replace('(plain weathered white, no sign, no lettering)', '(now a small café with one simple sign)') if v.split('-fan-')[0] in CAFE else t_)((BLOCK3 + (' This view looks STRAIGHT DOWN from directly above: keep it exactly top-down, a flat plan, no tilt or perspective.' if v == 'b7-plan' else '')) if v.startswith('b') else BRIEF + (PICNIC if v.split('-fan-')[0] in ('14-bleachers-high', '19-spiral', '22-picnic', '23-picnic-side', 'cafe-end') else '') + EXTRA.get(v, EXTRA.get(v.split('-fan-')[0], '')) + SOLAR), [], k)   # fans (`<base>-fan-<tag>`) use their base view's notes
            im.save(os.path.join(OUT, f'{v}-{ENGINE}.png')); print(f'{v} {ENGINE}: ok in {time.time() - t:.0f}s')
        except Exception as e: print(f'{v} {ENGINE}: FAILED {str(e)[:160]}')
