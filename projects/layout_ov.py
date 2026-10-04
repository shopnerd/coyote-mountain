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

def apply_layout(PAGES):
    """text edits on single Text artists, then drawing moves; returns the export map (after the moves)"""
    import matplotlib.transforms as _mt
    out = {}
    for k, fig in enumerate(PAGES):
        pid = f'p{k+1:02d}'
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
