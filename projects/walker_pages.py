# Walker's v14 (2 Oct 2026, "Giant Nature") photo pages, rebuilt with vector text and every photo at its native resolution.
# Slots and crops come from her flattened v14 pages (walker_v14_slots.json: page px at 2550 x 1650 = 150 dpi on 17 x 11).
# Photos are NOT drawn by matplotlib: each figure only records PHOTOS; place_photos() drops them into the finished PDF
# as JPEG q92 at full source resolution (matplotlib would resample them to the save dpi and store them losslessly = huge).
import json, matplotlib.font_manager as fm
for _f in glob.glob(os.path.join(os.path.dirname(os.path.abspath('pack.py')), 'fonts', 'PJS-*.ttf')): fm.fontManager.addfont(_f)
GF = 'Plus Jakarta Sans'
BGW = PAPER; INKW = '#2a2220'; MUTEDW = '#6b6258'; GREEN = '#4f6b3a'; RULEW = '#c9b8a0'; TANW = '#a08a70'
SLOTS = json.load(open('walker_v14_slots.json', encoding='utf-8'))
for _k, _v in SLOTS.items():                               # 4 Oct (Will: even margins on every page): the 2 x 2 render grids span
    if _k.split('-')[0] in ('2', '3', '3b'):               # the full 80..2470 px frame (was 271..2280), same rows, a 47 px gutter
        _c = int(_k.split('-')[1]) % 2; _w = (2470 - 80 - 47) / 2
        _v['rect'] = [round(80 + _c * (_w + 47)), _v['rect'][1], round(80 + _c * (_w + 47) + _w), _v['rect'][3]]
for _k, _v in (LAYOUT.get('slots') or {}).items():          # 4 Oct: the web editor's photo moves and swaps
    if _k in SLOTS: SLOTS[_k] = {**SLOTS[_k], **_v}
PHOTOKEYS = []
PX = (2550, 1650)
MAXDPI = 400
PHOTOS = []                      # (page index, (x0, y0, x1, y1) page px, source file, crop fractions)

def fx(px): return px / PX[0]
def fy(py): return 1 - py / PX[1]
def wtext(fig, x, y, s, size, weight=400, style='normal', color=INKW, ha='left', va='baseline', **k):
    return fig.text(fx(x), fy(y), s, fontsize=size, fontfamily=GF, fontweight=weight, fontstyle=style, color=color, ha=ha, va=va, **k)
def wrule(fig, x0, x1, y, color=RULEW, lw=.9):
    fig.add_artist(matplotlib.lines.Line2D([fx(x0), fx(x1)], [fy(y), fy(y)], color=color, lw=lw))
def wpage():
    fig = plt.figure(figsize=(17, 11), dpi=100); fig.patch.set_facecolor(BGW); fig._walker = True; return fig
def wfoot(fig, num, es, en):
    wrule(fig, 80, 2470, 1555)
    wtext(fig, 82, 1593, 'CENTRO EQUINO · CHICHIHUAS', 10.5, 700)
    wtext(fig, 1142, 1593, f'{es} · {en}', 10.5, 400, color=MUTEDW)
    wtext(fig, 1744, 1593, 'GIANT NATURE', 10.5, 700, color=GREEN)
    wtext(fig, 1946, 1593, 'Diseño preliminar · Preliminary design · oct 2026', 9, 400, color=MUTEDW)
    wtext(fig, 2457, 1595, f'{num:02d}', 15, 700, ha='right')
def wtitle(fig, es, en):
    wtext(fig, 83, 132, es, 33, 700); wtext(fig, 83, 190, en, 19, 400, 'italic', MUTEDW)
def wsrc(src):                    # slots hold Will's absolute paths; map them onto this machine when they aren't here
    if not src or os.path.exists(src): return src
    for a, b in (('G:/My Drive/MEXICO/Chichihaus/2026-09-23 Centro Equino pack', OUTDIR),
                 ('C:/Users/wrollins/WebDev/coyote-studio', os.path.dirname(os.path.dirname(os.path.abspath('pack.py'))))):
        if src.startswith(a): return b + src[len(a):]
    return src
def slot(fig, key):
    s = SLOTS[key]; x0, y0, x1, y1 = s['rect']
    fig.add_artist(matplotlib.patches.Rectangle((fx(x0), fy(y1)), fx(x1 - x0), (y1 - y0) / PX[1], color='#ddd3c3', lw=0))   # shows only if a photo is missing
    PHOTOS.append((len(PAGES), s['rect'], wsrc(s['src']), s['crop'], s.get('paper', False))); PHOTOKEYS.append(key)
    return s['rect']
def label(fig, r, es, en, num=None, size=12.5, credit=None):
    x0, y0, x1, y1 = r; t = f'{num}  {es}' if num else es
    wtext(fig, x0 + 2, y1 + 36, t, size, 700); wtext(fig, x0 + 2, y1 + 66, en, size - 2, 400, 'italic', MUTEDW)
    if credit: wtext(fig, x1, y1 + 66, credit, 8.5, color=MUTEDW, ha='right')
def section(fig, y_top, text, x0=80, x1=2470):
    wtext(fig, x0 + 2, y_top - 36, text, 14.5, 700); wrule(fig, x0, x1, y_top - 8)

def w_cover():
    fig = wpage(); slot(fig, '1-0')
    wrule(fig, 134, 316, 186, TANW, 2)
    wtext(fig, 134, 262, 'CENTRO EQUINO', 13.5, 700, color='#5c4b3e')
    wtext(fig, 130, 470, 'Centro', 84, 700); wtext(fig, 130, 630, 'Equino', 84, 700)
    wtext(fig, 134, 772, 'Chichihuas · Valle de Guadalupe', 20); wtext(fig, 134, 844, 'Baja California, México', 20)
    wrule(fig, 134, 976, 936)
    wtext(fig, 134, 1016, 'Propuesta de diseño', 18); wtext(fig, 134, 1082, 'Design proposal', 16, 400, 'italic', MUTEDW)
    wrule(fig, 134, 976, 1342)
    wtext(fig, 134, 1396, 'DISEÑO · DESIGN', 9, 700, color=TANW)
    wtext(fig, 134, 1470, 'G I A N T   N A T U R E', 22, 700, color=GREEN)
    wtext(fig, 134, 1532, 'Diseño preliminar · Preliminary design   ·   octubre 2026 · October 2026', 11.5, color=MUTEDW)
    num[0] += 1; PAGES.append(fig)
def w_renders(page, items):
    fig = wpage(); wtitle(fig, 'Vistas arquitectónicas', 'Architectural renders')
    for k, (n, es, en) in enumerate(items): label(fig, slot(fig, f'{page}-{k}'), es, en, n, size=13.5)   # 4 Oct: captions up a step on the 2 x 2 pages
    wfoot(fig, nxt(), 'Vistas arquitectónicas', 'Architectural renders'); PAGES.append(fig)
def w_site():
    fig = wpage(); wtitle(fig, 'Vistas del sitio', 'Site views')
    for k, (n, es, en) in enumerate([(1, 'El centro desde el noreste, hacia el oeste', 'The centre from the north-east, looking west'),
                                     (2, 'La maqueta del sitio, desde el suroeste', 'The site model, from the south-west'),
                                     (3, 'La maqueta del sitio, desde el noroeste', 'The site model, from the north-west')]):
        label(fig, slot(fig, f'4-{k}'), es, en, n)
    wfoot(fig, nxt(), 'Vistas del sitio', 'Site views'); PAGES.append(fig)
def wpara(fig, x, y, es, en, w=68, size=10.5, lead=28):   # 4 Oct: was 74 / 9.8 / 26
    es, g1 = para_lines(es); en, g2 = para_lines(en)
    for line in textwrap.wrap(es, w): wtext(fig, x, y, line, size, gid=g1); y += lead
    y += 8
    for line in textwrap.wrap(en, w): wtext(fig, x, y, line, size, style='italic', color=MUTEDW, gid=g2); y += lead
def w_text_refs():
    fig = wpage(); wtitle(fig, 'Texto y referencias', 'Text and references')
    cols = [('La idea · The idea',
             'Un centro ecuestre sencillo y bien cuidado en el valle: un establo de piedra y varas bajo un techo oscuro con claraboya, 8 caballerizas techadas entre las palmas, gradas frente a la pista, una pista oval, un corral redondo y una pista de trote que aprovecha el camino existente.',
             'A simple, well-kept equestrian centre in the valley: a stable of stone and sticks under a dark roof with a clerestory, 8 covered stalls among the palms, bleachers facing the arena, an oval arena, a round pen and a riding track that uses the existing road.'),
            ('Materiales · Materials',
             'Cerchas de acero cada 12 ft sobre los tubos pesados de 12 in de Andrés; piedra del lugar hasta 5 ft y varas encima; paneles de varas horizontales en marco de acero oscuro; lámina gris oscuro con claraboya abierta; cocina, baño, cuarto eléctrico, lavado y monturas en paca de paja o cob aplanado; cercas de tubo negro; piso de tierra.',
             'Steel trusses every 12 ft on Andrés’ heavy 12 in tube posts; local stone to 5 ft with the sticks right on it; panels of horizontal sticks in dark steel frames; dark grey sheet roof with an open clerestory; kitchen, bathroom, electrical, wash and tack rooms in straw bale or plastered cob; black pipe fences; dirt floors.'),
            ('Agua · Water',
             'La mitad sur del techo del establo alimenta el bebedero largo y el de la losa, la mitad norte el bebedero de la cerca este; el techo mariposa llena un bebedero redondo; el agua del cerro baja por un canal empastado a un bajo natural abajo de la pista; el excedente sale al oeste.',
             'The stable roof’s south half feeds the long trough and the pad trough, its north half the trough on the east run fence; the butterfly roof fills a round trough; hillside water runs down a grassed waterway to a natural low spot below the track; overflow leaves to the west.')]
    for x, (h, es, en) in zip((82, 900, 1717), cols):
        wtext(fig, x, 262, h, 14, 700); wpara(fig, x, 300, es, en)
    section(fig, 668, 'Piedra · Stone')
    for k, (es, en) in enumerate([('Piedra apilada en hiladas', 'Stacked stone in courses'), ('Piedra abajo, aplanado arriba', 'Stone base, plaster above'),
                                  ('Muro de piedra y lámina', 'Stone wall and metal roof'), ('Piedra y madera en el piso', 'Stone and wood set in the floor')]):
        label(fig, slot(fig, f'6-{k}'), es, en, size=12)
    section(fig, 1129, 'Madera, varas y acero · Wood, sticks and steel')
    for k, (es, en) in enumerate([('Varas secas del lugar', 'Weathered local sticks'), ('Varas en marco de acero', 'Sticks held in a steel frame'),
                                  ('Vigas viejas de madera', 'Old timbers'), ('Tubo de acero de Andrés', 'Andrés’ steel pipe')]):
        label(fig, slot(fig, f'6-{k + 4}'), es, en, size=12)
    wfoot(fig, nxt(), 'Texto y referencias', 'Text and references'); PAGES.append(fig)
def w_site_materials():
    fig = wpage(); wtitle(fig, 'Materiales del sitio', 'Materials on site')
    section(fig, 287, 'Piedra y tierra del sitio · Stone and earth from the site')
    for k, (es, en) in enumerate([('Piedra del lugar, apilada', 'Local stone, stacked'), ('Bolos de granito del sitio', 'Granite boulders on site'),
                                  ('Empedrado de piedra', 'Stone cobble paving'), ('Varas tejidas y aplanado de tierra', 'Woven sticks and earth plaster')]):
        label(fig, slot(fig, f'7-{k}'), es, en, size=12)
    section(fig, 937, 'Madera, acero y cercas · Wood, steel and fencing')
    for k, (es, en) in enumerate([('Troncos y ramas del lugar', 'Local logs and branches'), ('Encino caído', 'A fallen oak'),
                                  ('Vigas de acero, lámina y tragaluz', 'Steel beams, sheet roof, skylight'), ('Postes negros y cable', 'Black posts and wire')]):
        label(fig, slot(fig, f'7-{k + 4}'), es, en, size=12)
    wfoot(fig, nxt(), 'Materiales del sitio', 'Materials on site'); PAGES.append(fig)
def w_inspirations():
    fig = wpage(); wtitle(fig, 'Inspiraciones', 'Inspirations')
    wtext(fig, 2467, 128, 'El ambiente que buscamos: piedra, madera, acero y sombra.', 15, ha='right')
    wtext(fig, 2467, 170, 'The feeling we are after: stone, timber, steel and shade.', 14, style='italic', color=MUTEDW, ha='right')
    section(fig, 289, 'Edificios · Buildings')
    for k, (es, en) in enumerate([('Caballerizas de madera y bebedero largo', 'Timber stalls and a long trough'), ('Bloque, celosía y puerta corrediza', 'Block, breeze-block screen and sliding door'),
                                  ('Puerta corrediza de listones', 'A slatted sliding barn door'), ('Piedra vieja y cerchas de acero', 'Old stone and steel trusses')]):
        label(fig, slot(fig, f'8-{k}'), es, en, size=12, credit='Foto: Luis Gordoa' if k == 0 else None)
    section(fig, 945, 'Detalles · Details')
    for k, (es, en) in enumerate([('Varas en marcos de acero', 'Sticks in steel frames'), ('Lavadero con muros de piedra', 'A stone-walled wash rack'),
                                  ('Lavado: drenaje, manguera, repisas', 'Wash stall: drain, hose, shelves'), ('Celosías de varas y luz', 'Stick screens and dappled light'),
                                  ('Llanta para rascarse', 'A tyre scratching post')]):
        label(fig, slot(fig, f'8-{k + 4}'), es, en, size=11.5)
    wfoot(fig, nxt(), 'Inspiraciones', 'Inspirations'); PAGES.append(fig)

def place_photos(pdf_path, out_path, q=92):
    """Drop every recorded photo into the PDF at native resolution; return a resolution report."""
    import pymupdf, io
    from PIL import ImageOps
    try:
        import pillow_heif; pillow_heif.register_heif_opener()
    except ImportError: pass
    doc = pymupdf.open(pdf_path); rep = []
    for pg, (x0, y0, x1, y1), src, cr, paper in PHOTOS:
        if not src or not os.path.exists(src): rep.append((pg + 1, src, 'MISSING', 0)); continue
        im = ImageOps.exif_transpose(Image.open(src)).convert('RGB'); W, H = im.size
        a, b, c, d = [min(max(v, 0), 1) for v in cr]
        box = [a * W, b * H, c * W, d * H]
        asp = (x1 - x0) / (y1 - y0); bw, bh = box[2] - box[0], box[3] - box[1]      # trim to the slot's exact aspect
        if bw / bh > asp: m = (bw - bh * asp) / 2; box[0] += m; box[2] -= m
        else: m = (bh - bw / asp) / 2; box[1] += m; box[3] -= m
        im = im.crop([round(v) for v in box])
        cap = round((x1 - x0) / 150 * MAXDPI)                     # no point carrying more than MAXDPI into an 11 x 17 print
        if im.width > cap: im = im.resize((cap, round(im.height * cap / im.width)), Image.LANCZOS)
        if paper:                                                 # studio-white model renders: multiply by the page colour so their white is the paper
            from PIL import ImageChops; im = ImageChops.multiply(im, Image.new('RGB', im.size, PAPER))
        buf = io.BytesIO(); im.save(buf, 'JPEG', quality=q, subsampling=0)
        k = 1224 / PX[0]
        doc[pg].insert_image(pymupdf.Rect(x0 * k, y0 * k, x1 * k, y1 * k), stream=buf.getvalue())
        dpi = im.width / ((x1 - x0) / 150)
        rep.append((pg + 1, src, f'{im.width}x{im.height}', round(dpi)))
    doc.save(out_path, garbage=4, deflate=True); return rep
