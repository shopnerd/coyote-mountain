# Pack layout editor, pack side (4 Oct 2026, Will + Walker: "move things myself, swap a photo, change the text").
# The web editor (will.100xbtr.com/equino/pack/edit/) saves overrides to the site; `pull_layout.py` writes them to pack_layout.json;
# this file applies them while pack.py builds and exports layout.json (every editable item with its place) for the editor.
#   slots : {slot key: {rect: [x0,y0,x1,y1] page px 2550x1650, src: local path, crop: [a,b,c,d]}}     -> photos (walker_v14_slots.json)
#   boxes : {'p03:plan': [x, y, w, h]}  fractions of the page, top-left origin = where the drawing's visible extent should sit
#   texts : {'t1a2b3c4d': 'new text'}   key = crc32 of the ORIGINAL source text, so it survives edits
import json as _lj, os as _lo, zlib as _lz
LAYOUT_FILE = 'pack_layout.json'
LAYOUT = {'slots': {}, 'boxes': {}, 'texts': {}}
if _lo.path.exists(LAYOUT_FILE):
    try: LAYOUT.update(_lj.load(open(LAYOUT_FILE, encoding='utf-8')))
    except Exception as e: print('pack_layout.json unreadable:', e)
def tkey(s): return 't' + format(_lz.crc32(str(s).encode('utf-8')), '08x')
def TXT(s): return LAYOUT['texts'].get(tkey(s), s)

def normalize_page(fig, k, M=80 / 2550, GMAX=.03, GMIN=.018):
    """4 Oct (Will: 'some pages have lots of room at the sides, others are crowded'): put every drawing page on one frame.
    The page's content (drawings, text blocks, legends, photo slots; not the title or footer) is grouped into columns by
    horizontal overlap. The columns are laid out so the outer ones sit exactly on the margins with equal gutters; a page that
    is too wide is scaled down a little (fonts too); where the gutters would get wider than GMAX, drawing-only columns grow
    (if the page has the height) and the rest is shared out as gutter."""
    from matplotlib.lines import Line2D
    from matplotlib.patches import Rectangle
    fig.canvas.draw(); r = fig.canvas.get_renderer(); inv = fig.transFigure.inverted()
    items = []
    for ax in fig.axes:
        p = ax.get_position()
        if not ax.get_visible() or p.width * p.height > .9: continue
        try: tb = ax.get_tightbbox(r).transformed(inv)
        except Exception: continue
        items.append(dict(x0=max(tb.x0, 0), x1=min(tb.x1, 1), y0=tb.y0, y1=tb.y1, kind='ax', o=ax))
    for t in fig.texts:
        if not t.get_visible() or not t.get_text().strip() or t.get_gid() == 'pagetitle': continue
        bb = t.get_window_extent(r).transformed(inv)
        if bb.y1 < .066: continue                                                            # the footer
        items.append(dict(x0=bb.x0, x1=bb.x1, y0=bb.y0, y1=bb.y1, kind='txt', o=t))
    for a in list(fig.artists) + list(fig.lines) + list(fig.patches):
        if a is fig.patch: continue
        try: bb = a.get_window_extent(r).transformed(inv)
        except Exception: continue
        if bb.y1 < .066 or bb.width > .9: continue
        items.append(dict(x0=bb.x0, x1=bb.x1, y0=bb.y0, y1=bb.y1, kind='art', o=a))
    PH = globals().get('PHOTOS', []); PXW = globals().get('PX', (2550, 1650))
    for i, (pg, rc, *_rest) in enumerate(PH):
        if pg == k: items.append(dict(x0=rc[0] / PXW[0], x1=rc[2] / PXW[0], y0=1 - rc[3] / PXW[1], y1=1 - rc[1] / PXW[1], kind='photo', o=i))
    if not items: return
    items.sort(key=lambda q: q['x0']); cols = []
    if getattr(fig, '_norm_single', False): cols = [dict(x0=min(q['x0'] for q in items), x1=max(q['x1'] for q in items), it=items)]; items = []   # 4 Oct: multi-row sheets (E-1) move as one block
    for q in items:
        if cols and q['x0'] < cols[-1]['x1'] - .012: cols[-1]['x1'] = max(cols[-1]['x1'], q['x1']); cols[-1]['it'].append(q)   # 4 Oct: touching or barely overlapping blocks stay separate columns
        else: cols.append(dict(x0=q['x0'], x1=q['x1'], it=[q]))
    A = 1 - 2 * M; n = len(cols); W = sum(c['x1'] - c['x0'] for c in cols)
    for c in cols:
        c['s'] = 1.0
        c['grow'] = all(q['kind'] == 'ax' or (q['kind'] == 'txt' and q['o'].axes is not None) for q in c['it'])   # drawing-only column
    if W + GMIN * (n - 1) > A:                                                              # too wide: scale everything down
        s = (A - GMIN * (n - 1)) / W
        for c in cols: c['s'] = s
        g = GMIN
    else:
        g = (A - W) / (n - 1) if n > 1 else 0
        if n > 1 and g > GMAX:                                                              # roomy: let drawings grow into it
            extra = (g - GMAX) * (n - 1); gw = sum(c['x1'] - c['x0'] for c in cols if c['grow'])
            for c in cols:
                if not c['grow'] or gw <= 0: continue
                top = max(q['y1'] for q in c['it']); h = top - min(q['y0'] for q in c['it'])
                fmax = (top - .075) / h if h > 0 else 1
                c['s'] = max(1.0, min(1 + extra / gw, fmax, 1.6))
            W2 = sum((c['x1'] - c['x0']) * c['s'] for c in cols); g = (A - W2) / (n - 1)
    x = M if n > 1 else M + (A - (cols[0]['x1'] - cols[0]['x0']) * cols[0]['s']) / 2
    for c in cols:
        s = c['s']; f = lambda v, c=c, s=s, x=x: x + (v - c['x0']) * s
        for q in c['it']:
            o = q['o']
            if q['kind'] == 'ax':
                p = o.get_position(); top = p.y1                                            # scale about the drawing's top edge
                new = [f(p.x0), top - p.height * s, p.width * s, p.height * s]
                o.set_position(new); o.set_position(new, which='original')
            elif q['kind'] == 'txt':
                X, Y = o.get_position(); o.set_position((f(X), Y))
                if s < 1: o.set_fontsize(o.get_fontsize() * s)
            elif q['kind'] == 'art':
                if isinstance(o, Line2D): o.set_xdata([f(v) for v in o.get_xdata()])
                elif isinstance(o, Rectangle): x0_ = o.get_x(); o.set_x(f(x0_)); o.set_width(o.get_width() * s)
            elif q['kind'] == 'photo':
                pg, rc, *rest = PH[o]; X0, X1 = f(rc[0] / PXW[0]) * PXW[0], f(rc[2] / PXW[0]) * PXW[0]
                PH[o] = (pg, [round(X0), rc[1], round(X1), rc[3]], *rest)
        x += (c['x1'] - c['x0']) * s + g

def apply_layout(PAGES):
    """text edits on single Text artists, then drawing moves; returns the export map (after the moves)"""
    import matplotlib.transforms as _mt
    out = {}
    for k, fig in enumerate(PAGES):
        pid = f'p{k+1:02d}'
        if not getattr(fig, '_walker', False): normalize_page(fig, k)
        arts = list(fig.texts) + [t for ax in fig.axes for t in ax.texts]
        for t in arts:
            g = t.get_gid() or ''
            if g.startswith('para:'): continue                                   # paragraphs were already rewrapped at build time
            src = getattr(t, '_orig_text', None) or t.get_text(); t._orig_text = src
            if tkey(src) in LAYOUT['texts']: t.set_text(LAYOUT['texts'][tkey(src)])
        fig.canvas.draw(); r = fig.canvas.get_renderer()
        boxes = []
        for i, ax in enumerate(fig.axes):
            p = ax.get_position()
            if p.width * p.height > .9 or not ax.get_visible(): continue
            key = f'{pid}:{ax.get_gid() or "ax" + str(i)}'
            try: tb = ax.get_tightbbox(r).transformed(fig.transFigure.inverted())
            except Exception: continue
            if tb.width * tb.height < .012: continue
            want = LAYOUT['boxes'].get(key)
            if want:
                x, y, w, h = want; s = min(w / tb.width, h / tb.height)
                nx0, ny1 = x, 1 - y                                                # target top-left in figure coords
                pos = ax.get_position(original=False)
                new = [nx0 + (pos.x0 - tb.x0) * s, ny1 - (tb.y1 - pos.y0) * s, pos.width * s, pos.height * s]
                ax.set_position(new); ax.set_position(new, which='original')
        fig.canvas.draw(); r = fig.canvas.get_renderer()
        for i, ax in enumerate(fig.axes):
            p = ax.get_position()
            if p.width * p.height > .9 or not ax.get_visible(): continue
            try: tb = ax.get_tightbbox(r).transformed(fig.transFigure.inverted())
            except Exception: continue
            if tb.width * tb.height < .012: continue
            boxes.append({'key': f'{pid}:{ax.get_gid() or "ax" + str(i)}', 'rect': [round(tb.x0, 4), round(1 - tb.y1, 4), round(tb.width, 4), round(tb.height, 4)]})
        texts, paras = [], {}
        for t in list(fig.texts) + [t for ax in fig.axes for t in ax.texts]:
            s = t.get_text()
            if not t.get_visible() or not s or sum(c.isalpha() for c in s) < 2: continue
            try: bb = t.get_window_extent(r).transformed(fig.transFigure.inverted())
            except Exception: continue
            if bb.x1 < 0 or bb.x0 > 1 or bb.y1 < 0 or bb.y0 > 1: continue
            rect = [bb.x0, 1 - bb.y1, bb.width, bb.height]; g = t.get_gid() or ''
            if g.startswith('para:'):
                _, key, orig = g.split(':', 2)
                P = paras.setdefault(key, {'key': key, 'text': LAYOUT['texts'].get(key, PARA_SRC.get(key, '')), 'rects': [], 'size': t.get_fontsize(), 'para': True})
                P['rects'].append(rect)
            else:
                src = getattr(t, '_orig_text', s)
                texts.append({'key': tkey(src), 'text': s, 'rect': [round(v, 4) for v in rect], 'size': round(t.get_fontsize(), 1)})
        for P in paras.values():
            R = P.pop('rects'); x0 = min(a[0] for a in R); y0 = min(a[1] for a in R); x1 = max(a[0] + a[2] for a in R); y1 = max(a[1] + a[3] for a in R)
            P['rect'] = [round(x0, 4), round(y0, 4), round(x1 - x0, 4), round(y1 - y0, 4)]; texts.append(P)
        out[pid] = {'boxes': boxes, 'texts': texts, 'photos': []}
    return out
PARA_SRC = {}
def para_lines(es_or_en):
    """an override-aware paragraph: returns (text to wrap, gid for its lines)"""
    k = tkey(es_or_en); PARA_SRC[k] = es_or_en
    return LAYOUT['texts'].get(k, es_or_en), f'para:{k}:x'
