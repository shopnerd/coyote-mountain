/* design mode — canonical copy (WebDev/shared-theme/design-mode.js; each site carries a synced copy at its root).
   open any page with ?design and it becomes editable by hand:
   click selects · drag moves a piece (its neighbours reflow) · double-click edits the words ·
   the numbers beside the selection scrub like a slider · delete hides · arrows nudge · p selects the parent · ctrl-z undoes.
   every change is written down in plain english (copy) and as data (save) so the source can be patched to match;
   changes replay from this browser's storage until "clear". nothing loads unless ?design is in the address. */
(() => {
  const ROOT = document.body; if (!ROOT || window.__dm) return;
  const UNIT = 'button,a,h1,h2,h3,h4,h5,h6,p,label,input,select,textarea,img,svg,canvas,video,li,output,.p,.sec,.desc,.stat,.card,.metric,[data-unit]';
  const TEXTY = 'h1,h2,h3,h4,h5,h6,p,label,span,b,i,em,strong,a,button,li,output,td,th,dt,dd,small,div';
  const px = v => (Math.round(v * 4) / 4) + 'px';
  const num = s => parseFloat(s) || 0;
  const layout = e => /flex|grid/.test(getComputedStyle(e).display);
  const isBox = e => e === ROOT || e.matches('nav,aside,header,footer,main,section,article,ul,ol,form,fieldset,[data-box]') || layout(e);
  const boxOf = e => { let n = e; while (n && n !== ROOT && !isBox(n)) n = n.parentElement; return n || ROOT; };
  const unitOf = t => {
    if (t.closest('.dm')) return null;
    let u = t.closest(UNIT); if (!u) return boxOf(t);
    while (u.parentElement && u.parentElement !== ROOT && u.parentElement.matches(UNIT)) u = u.parentElement;
    return u;
  };

  const css = document.createElement('style'); css.textContent = `
  .dm{position:fixed;z-index:2147483000;font:11.5px/1.5 var(--font,ui-monospace,Consolas,monospace);color:var(--ink,var(--tx,#1a1a18));--dmp:var(--paper,var(--card,var(--bg2,#f4f3ef)));--dml:var(--line,var(--border,var(--br,#c8c8c2)));--dma:var(--accent,#c96b3a);--dmm:var(--ink3,var(--muted,var(--tx3,#8b8a84)));--dmm2:var(--ink2,var(--muted,var(--tx2,#5a5954)))}
  #dmBar{bottom:40px;left:50%;transform:translateX(-50%);display:flex;align-items:center;gap:6px;background:var(--dmp);border:1px solid var(--dma);border-radius:3px;padding:4px 8px;box-shadow:0 4px 18px rgba(0,0,0,.18);white-space:nowrap}
  #dmBar b{color:var(--dma);font-weight:500;margin-right:4px}
  #dmBar .n{color:var(--dmm);margin-right:6px}
  .dm button{border:1px solid var(--dml);background:transparent;color:inherit;font:inherit;font-size:11px;padding:2px 9px;border-radius:3px;cursor:pointer}
  .dm button:hover{background:rgba(201,107,58,.12)}
  #dmBox{pointer-events:none;border:1px solid var(--dma);box-shadow:0 0 0 3px rgba(201,107,58,.18);border-radius:3px;display:none}
  #dmBox i{position:absolute;left:-1px;bottom:100%;margin-bottom:3px;background:var(--dma);color:#fff;font-style:normal;font-size:10px;padding:1px 6px;border-radius:2px;white-space:nowrap}
  #dmHover{pointer-events:none;border:1px dashed var(--dma);opacity:.5;border-radius:3px;display:none}
  #dmKnobs{width:200px;background:var(--dmp);border:1px solid var(--dma);border-radius:3px;box-shadow:0 6px 24px rgba(0,0,0,.2);padding:8px 10px;display:none}
  #dmKnobs .t{font-size:11px;color:var(--dmm2);margin-bottom:6px;display:flex;align-items:center;gap:6px}
  #dmKnobs .t b{flex:1;font-weight:500;color:inherit;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  #dmKnobs .t button{padding:0 6px;font-size:10px}
  .dmK{display:flex;align-items:center;gap:6px;padding:3px 0;cursor:ew-resize;user-select:none;border-top:1px solid var(--dml)}
  .dmK .l{flex:1;color:var(--dmm2);font-size:10.5px;text-transform:uppercase;letter-spacing:.05em}
  .dmK .v{min-width:34px;text-align:right;font-variant-numeric:tabular-nums;padding:0 3px;border-radius:2px;outline:none;cursor:text}
  .dmK .v:focus{background:rgba(201,107,58,.15);box-shadow:0 0 0 1px var(--dma)}
  .dmK .u{color:var(--dmm);width:16px;font-size:10px}
  .dmK:hover .l{color:inherit}
  #dmList{right:12px;bottom:12px;width:300px;max-height:40vh;overflow:auto;background:var(--dmp);border:1px solid var(--dml);border-radius:3px;padding:6px 10px;display:none}
  #dmList div{padding:2px 0;border-top:1px solid var(--dml);color:var(--dmm2);font-size:11px}
  #dmList div:first-child{border:0}
  #dmList div b{font-weight:500;color:inherit}
  .dmGhost{position:fixed;z-index:2147483001;pointer-events:none;opacity:.75;transform:rotate(-1deg);box-shadow:0 8px 24px rgba(0,0,0,.25);margin:0!important}
  .dmDrag{opacity:.35!important}
  .dmEdit{outline:none!important;box-shadow:inset 0 0 0 1px var(--accent,#c96b3a)!important;background:rgba(201,107,58,.15)!important;cursor:text!important}
  #dmHint{bottom:14px;left:50%;transform:translateX(-50%);color:var(--dmm);font-size:10.5px;pointer-events:none;white-space:nowrap}`;
  document.head.appendChild(css);

  const el = id => { const d = document.createElement('div'); d.id = id; d.className = 'dm'; ROOT.appendChild(d); return d; };
  const bar = el('dmBar'), box = el('dmBox'), hov = el('dmHover'), knobs = el('dmKnobs'), list = el('dmList'), hint = el('dmHint');
  bar.innerHTML = '<b>design mode</b><span class="n" id="dmN">no changes</span><button id="dmPause">pause</button><button id="dmUndo">undo</button><button id="dmCopy">copy</button><button id="dmSave">save</button><button id="dmClear">clear</button><button id="dmDone">done</button>';
  const HINT = 'click to select · drag to move · double-click to edit the words · scrub the numbers · delete hides · p for the parent · ctrl-click uses the page · esc';
  hint.textContent = HINT;

  /* ---------- naming things for humans and for the patch ---------- */
  const textNode = (e, make) => {
    for (const n of e.childNodes) if (n.nodeType === 3 && n.textContent.trim()) return n;
    for (const c of e.children) { if (c.closest('.dm')) continue; const n = textNode(c); if (n) return n; }
    if (!make) return null; const n = document.createTextNode(''); e.appendChild(n); return n;
  };
  const words = e => {
    if (!e) return '';
    if (e.matches('img,svg,canvas,video')) return e.id ? '#' + e.id : e.tagName.toLowerCase();
    if (e.matches('input,select,textarea')) return e.id ? '#' + e.id : (e.placeholder || e.tagName.toLowerCase());
    const n = textNode(e); return n ? n.textContent.replace(/\s+/g, ' ').trim().slice(0, 28) : (e.id ? '#' + e.id : e.tagName.toLowerCase());
  };
  const path = e => {
    if (e === ROOT) return 'body';
    if (e.id) return '#' + CSS.escape(e.id);
    const p = e.parentElement, i = [...p.children].indexOf(e) + 1;
    return path(p) + ' > ' + e.tagName.toLowerCase() + ':nth-child(' + i + ')';
  };
  const HEAD = 'h1,h2,h3,h4,.sec,.sec-title,.eyebrow,legend';
  const section = e => {
    let n = e; while (n && n !== ROOT) { let s = n.previousElementSibling; while (s) { if (s.matches(HEAD)) return words(s); const h = s.querySelector(HEAD); if (h && !s.contains(e)) { s = s.previousElementSibling; continue; } s = s.previousElementSibling; } n = n.parentElement; }
    return 'page';
  };
  const describe = e => {
    if (e === ROOT) return 'the page';
    if (e.matches(HEAD)) return 'heading “' + words(e) + '”';
    if (isBox(e) && !e.matches(UNIT)) return section(e) + ' › ' + (e.id ? '#' + e.id : (e.className && typeof e.className === 'string' && e.className.split(' ')[0]) ? '.' + e.className.split(' ')[0] : e.tagName.toLowerCase());
    if (e.matches('img,svg,canvas,video')) return 'image ' + words(e);
    return '“' + words(e) + '”';
  };

  /* ---------- the ledger ---------- */
  const KEY = 'dm-ops:' + location.pathname;
  let ops = []; try { ops = JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (_) { ops = []; }
  const english = o => {
    if (o.kind === 'move') return 'move <b>' + o.what + '</b> to position ' + (o.to.index + 1) + ' in ' + o.to.where;
    if (o.kind === 'text') return 'rename <b>' + o.from + '</b> → <b>' + o.to + '</b>';
    if (o.kind === 'hide') return 'hide <b>' + o.what + '</b>';
    if (o.kind === 'var') return o.label + ' ' + o.from + ' → <b>' + o.to + '</b>';
    return '<b>' + o.what + '</b>: ' + o.label + ' ' + (o.from || 'default') + ' → <b>' + o.to + '</b>' + (o.extra ? ' · ' + (o.extra.minHeight !== undefined ? 'height' : 'width') + ' now follows the padding' : '');
  };
  const plain = s => s.replace(/<\/?b>/g, '');
  const show = () => {
    document.getElementById('dmN').textContent = ops.length ? ops.length + (ops.length === 1 ? ' change' : ' changes') : 'no changes';
    list.style.display = ops.length ? 'block' : 'none';
    list.innerHTML = ops.map((o, i) => '<div>' + (i + 1) + '. ' + english(o) + '</div>').join('');
    list.scrollTop = 1e6;
    try { localStorage.setItem(KEY, JSON.stringify(ops)); } catch (_) {}
  };
  const live = (o, e, fp, tp) => { for (const [k, v] of [['el', e], ['fp', fp], ['tp', tp]]) if (v) Object.defineProperty(o, k, { value: v, enumerable: false, writable: true }); return o; };
  const record = (o, e, fp, tp) => { ops.push(live(o, e, fp, tp)); show(); };
  const find = s => s === 'body' ? ROOT : document.querySelector(s);
  const apply = o => {
    if (o.kind === 'var') { document.documentElement.style.setProperty(o.name, o.to); return; }
    const e = find(o.sel); if (!e) return;
    if (o.kind === 'move') { const p = find(o.to.sel); if (!p) return; live(o, e, e.parentElement, p); const kids = [...p.children].filter(k => k !== e); p.insertBefore(e, kids[o.to.index] || null); return; }
    live(o, e);
    if (o.kind === 'text') { textNode(e, true).textContent = o.to; }
    else if (o.kind === 'hide') { e.style.display = 'none'; }
    else { e.style[o.prop] = o.to; if (o.extra) for (const x in o.extra) e.style[x] = o.extra[x]; }
  };
  const revert = o => {
    if (o.kind === 'var') { document.documentElement.style.setProperty(o.name, o.from); return; }
    const e = o.el || find(o.sel); if (!e) return;
    if (o.kind === 'move') { const p = o.fp || find(o.from.sel); if (!p) return; const kids = [...p.children].filter(k => k !== e); p.insertBefore(e, kids[o.from.index] || null); }
    else if (o.kind === 'text') { textNode(e, true).textContent = o.from; }
    else if (o.kind === 'hide') { e.style.display = o.from; }
    else { e.style[o.prop] = o.from; if (o.extra) for (const x in o.extra) e.style[x] = o.extraFrom[x]; }
  };
  ops.forEach(o => { try { apply(o); } catch (_) {} });

  /* ---------- selection ---------- */
  let sel = null, editing = null, paused = false;
  const rect = (d, e, pad) => { const r = e.getBoundingClientRect(); d.style.left = (r.left - pad) + 'px'; d.style.top = (r.top - pad) + 'px'; d.style.width = (r.width + pad * 2) + 'px'; d.style.height = (r.height + pad * 2) + 'px'; };
  const select = e => {
    sel = e; if (!e) { box.style.display = 'none'; knobs.style.display = 'none'; return; }
    box.style.display = 'block'; box.innerHTML = '<i>' + plain(describe(e)) + '</i>'; buildKnobs(e);
  };
  const tick = () => {
    if (sel && sel.isConnected) {
      rect(box, sel, 2);
      const s = sel.getBoundingClientRect(), w = 214;
      knobs.style.left = (s.right + 14 + w <= innerWidth ? s.right + 14 : Math.max(8, Math.min(s.left - w, innerWidth - w))) + 'px';
      knobs.style.top = Math.max(8, Math.min(s.top, innerHeight - knobs.offsetHeight - 12)) + 'px';
      knobs.style.display = 'block';
    }
    requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);

  /* ---------- knobs: the numbers that scrub ---------- */
  const KN = [
    ['text size', 'fontSize', 'font-size', 'px', 6, 60, .5],
    ['height', 'minHeight', 'min-height', 'px', 0, 400, 1],
    ['pad ↕', 'py', null, 'px', 0, 60, .5],
    ['pad ↔', 'px', null, 'px', 0, 80, .5],
    ['corner', 'borderRadius', 'border-radius', 'px', 0, 40, .5],
    ['space above', 'marginTop', 'margin-top', 'px', -20, 80, 1],
    ['weight', 'flexGrow', 'flex-grow', '', 0, 6, 1],
    ['gap', 'gap', 'gap', 'px', 0, 60, 1],
    ['letters', 'letterSpacing', 'letter-spacing', 'px', -1, 6, .1],
    ['rail width', '--rail', null, 'px', 180, 520, 2]
  ];
  /* the space really around the content: a button sized by min-height or stretched by flex has more room than its css padding says */
  const eff = e => {
    const cs = getComputedStyle(e), pc = e.parentElement && getComputedStyle(e.parentElement), H = e.offsetHeight, W = e.offsetWidth, st = e.style, keep = st.cssText;
    st.padding = '0'; st.minHeight = '0'; st.minWidth = '0'; st.flex = '0 0 auto'; st.width = 'auto'; st.alignSelf = 'flex-start';
    const ch = e.offsetHeight, cw = e.offsetWidth; st.cssText = keep;
    return { py: Math.max(0, (H - ch) / 2), px: Math.max(0, (W - cw) / 2), minH: num(cs.minHeight) > 0, grow: num(cs.flexGrow) > 0 && !!pc && pc.display.includes('flex') && pc.flexDirection === 'row' };
  };
  const rootVar = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
  const read = (e, k) => {
    if (k === '--rail') return num(rootVar('--rail'));
    if (k === 'py' || k === 'px') return eff(e)[k];
    return num(getComputedStyle(e)[k]);
  };
  const applyKnob = (e, k, v, unit) => {
    if (k === '--rail') { document.documentElement.style.setProperty('--rail', v + 'px'); return v + 'px'; }
    if (k === 'py' || k === 'px') { const f = eff(e), py = k === 'py' ? v : f.py, pxx = k === 'px' ? v : f.px; e.style.padding = px(py) + ' ' + px(pxx); if (k === 'py' && f.minH) e.style.minHeight = '0'; if (k === 'px' && f.grow) e.style.flex = '0 0 auto'; return e.style.padding; }
    e.style[k] = unit ? px(v) : String(v); return e.style[k];
  };
  const buildKnobs = e => {
    const box_ = isBox(e) && !e.matches(UNIT), pFlex = e !== ROOT && getComputedStyle(e.parentElement).display.includes('flex') && getComputedStyle(e.parentElement).flexDirection === 'row';
    const rows = KN.filter(([, k]) => {
      if (k === '--rail') return e.matches('aside') && !!rootVar('--rail');
      if (k === 'gap') return layout(e);
      if (k === 'flexGrow') return pFlex;
      if (k === 'letterSpacing') return e.matches(HEAD);
      if (k === 'py' || k === 'px' || k === 'borderRadius' || k === 'minHeight') return !box_ || e.matches('nav,aside,header,footer,section,article');
      if (k === 'fontSize') return true;
      return e !== ROOT;
    });
    knobs.innerHTML = '<div class="t"><b>' + plain(describe(e)) + '</b>' + (e !== ROOT ? '<button data-up>▲ parent</button>' : '') + '</div>' +
      rows.map(([l, k, , u]) => '<div class="dmK" data-k="' + k + '"><span class="l">' + l + '</span><span class="v" contenteditable spellcheck="false">' + (+read(e, k).toFixed(2)) + '</span><span class="u">' + u + '</span></div>').join('');
    knobs.querySelector('[data-up]')?.addEventListener('click', () => { const p = e.parentElement && boxOf(e.parentElement); if (p) select(p); });
  };
  const before_ = (e, k) => k === '--rail' ? rootVar('--rail') : (k === 'py' || k === 'px') ? e.style.padding : e.style[k];
  knobs.addEventListener('pointerdown', ev => {
    const row = ev.target.closest('.dmK'); if (!row || ev.target.classList.contains('v') || !sel) return;
    ev.preventDefault(); const e = sel, spec = KN.find(s => s[1] === row.dataset.k), [, k, , unit, lo, hi, step] = spec;
    const v0 = read(e, k), x0 = ev.clientX, before = before_(e, k), exFrom = { minHeight: e.style.minHeight, flex: e.style.flex };
    let v = v0; row.setPointerCapture(ev.pointerId);
    const mv = m => { const fine = m.altKey ? .25 : m.shiftKey ? 5 : 1; v = Math.min(hi, Math.max(lo, v0 + Math.round((m.clientX - x0) / 3 * fine / step) * step)); row.querySelector('.v').textContent = +v.toFixed(2); applyKnob(e, k, v, unit); };
    const up = () => { row.removeEventListener('pointermove', mv); row.removeEventListener('pointerup', up); if (v !== v0) commitKnob(e, spec, before, v, exFrom); };
    row.addEventListener('pointermove', mv); row.addEventListener('pointerup', up);
  });
  knobs.addEventListener('keydown', ev => {
    if (!ev.target.classList.contains('v')) return; ev.stopPropagation();
    if (ev.key === 'Enter' || ev.key === 'Escape') { ev.preventDefault(); ev.target.blur(); }
  });
  knobs.addEventListener('focusout', ev => {
    if (!ev.target.classList.contains('v') || !sel) return;
    const row = ev.target.closest('.dmK'), spec = KN.find(s => s[1] === row.dataset.k), [, k, , unit, lo, hi] = spec, e = sel;
    const v0 = read(e, k), v = Math.min(hi, Math.max(lo, num(ev.target.textContent))); ev.target.textContent = +v.toFixed(2);
    if (v === v0) return; const before = before_(e, k), exFrom = { minHeight: e.style.minHeight, flex: e.style.flex };
    applyKnob(e, k, v, unit); commitKnob(e, spec, before, v, exFrom);
  });
  const commitKnob = (e, [label, k, prop], before, v, exFrom) => {
    if (k === '--rail') { record({ kind: 'var', name: '--rail', label: 'rail width', from: before, to: v + 'px' }); return; }
    const pad = k === 'py' || k === 'px', styleProp = pad ? 'padding' : k;
    const o = { kind: 'style', sel: path(e), what: plain(describe(e)), where: section(e), label: pad ? 'padding' : label, prop: styleProp, css: pad ? 'padding' : prop, from: before, to: e.style[styleProp] };
    if (exFrom) for (const x of ['minHeight', 'flex']) if (e.style[x] !== exFrom[x]) { (o.extra = o.extra || {})[x] = e.style[x]; (o.extraFrom = o.extraFrom || {})[x] = exFrom[x]; }
    record(o, e);
  };

  /* ---------- pointer: select, drag to move ---------- */
  let drag = null;
  const inPage = t => !paused && t instanceof Element && ROOT.contains(t) && !t.closest('.dm');
  window.addEventListener('pointerdown', ev => {
    if (editing) { if (!editing.contains(ev.target)) endEdit(true); else return; }
    if (!inPage(ev.target) || ev.ctrlKey) return;
    ev.preventDefault(); ev.stopImmediatePropagation();
    const u = unitOf(ev.target); if (!u) return;
    select(u); if (u === ROOT) return;
    drag = { e: u, sel: path(u), x: ev.clientX, y: ev.clientY, on: false, from: { sel: path(u.parentElement), index: [...u.parentElement.children].indexOf(u), where: section(u) } };
  }, true);
  window.addEventListener('pointermove', ev => {
    if (drag && !drag.on && Math.hypot(ev.clientX - drag.x, ev.clientY - drag.y) > 4) {
      drag.on = true; const g = drag.e.cloneNode(true); g.className += ' dmGhost'; const r = drag.e.getBoundingClientRect();
      g.style.width = r.width + 'px'; g.style.height = r.height + 'px'; ROOT.appendChild(g); drag.g = g; drag.dx = ev.clientX - r.left; drag.dy = ev.clientY - r.top;
      drag.e.classList.add('dmDrag'); drag.fp = drag.e.parentElement; document.body.style.cursor = 'grabbing'; hov.style.display = 'none';
    }
    if (drag?.on) {
      ev.preventDefault(); drag.g.style.left = (ev.clientX - drag.dx) + 'px'; drag.g.style.top = (ev.clientY - drag.dy) + 'px';
      const under = document.elementsFromPoint(ev.clientX, ev.clientY).find(t => inPage(t) && !drag.e.contains(t) && !t.classList.contains('dmGhost')); if (!under) return;
      const b = boxOf(under); if (drag.e.contains(b)) return;
      const kids = [...b.children].filter(k => k !== drag.e && !k.classList.contains('dm') && k.offsetParent !== null && !k.matches('input[type=file],script,style'));
      const cs = getComputedStyle(b), row = cs.display.includes('flex') && cs.flexDirection === 'row';
      const over = kids.find(k => { const r = k.getBoundingClientRect(); return ev.clientX >= r.left && ev.clientX <= r.right && ev.clientY >= r.top && ev.clientY <= r.bottom; });
      let ref;
      if (over) { const r = over.getBoundingClientRect(), before = row ? ev.clientX < r.left + r.width / 2 : ev.clientY < r.top + r.height / 2; ref = before ? over : over.nextElementSibling; }
      else if (b !== drag.e.parentElement && layout(b)) { const last = kids[kids.length - 1], lr = last && last.getBoundingClientRect(); ref = !last || ev.clientY > lr.top + lr.height / 2 ? null : kids[0]; }
      else return;
      if (ref === drag.e) return;
      if (ref === null ? b.lastElementChild !== drag.e : drag.e.nextSibling !== ref) b.insertBefore(drag.e, ref);
      return;
    }
    if (inPage(ev.target) && !editing) { const u = unitOf(ev.target); if (u && u !== sel && u !== ROOT) { hov.style.display = 'block'; rect(hov, u, 1); } else hov.style.display = 'none'; }
    else hov.style.display = 'none';
  }, true);
  window.addEventListener('pointerup', ev => {
    if (!drag) return; if (drag.on) {
      ev.preventDefault(); ev.stopImmediatePropagation(); drag.g.remove(); drag.e.classList.remove('dmDrag'); document.body.style.cursor = '';
      const to = { sel: path(drag.e.parentElement), index: [...drag.e.parentElement.children].indexOf(drag.e), where: section(drag.e) };
      if (to.sel !== drag.from.sel || to.index !== drag.from.index) record({ kind: 'move', sel: drag.sel, what: plain(describe(drag.e)), from: drag.from, to }, drag.e, drag.fp, drag.e.parentElement);
    }
    drag = null;
  }, true);
  window.addEventListener('click', ev => { if (inPage(ev.target) && !editing && !ev.ctrlKey) { ev.preventDefault(); ev.stopImmediatePropagation(); } }, true);
  window.addEventListener('scroll', () => { hov.style.display = 'none'; }, true);

  /* ---------- double-click: edit the words ---------- */
  window.addEventListener('dblclick', ev => {
    if (!inPage(ev.target) || editing || ev.ctrlKey) return; ev.preventDefault(); ev.stopImmediatePropagation();
    const u = unitOf(ev.target); if (!u || u === ROOT || u.matches('select,input,textarea,img,svg,canvas,video')) return;
    let t = ev.target.closest(TEXTY); while (t && t !== u && !textNode(t) && u.contains(t)) t = t.parentElement.closest(TEXTY);
    if (!t || !u.contains(t)) t = u; const node = textNode(t, true);
    editing = t; t.dataset.dmFrom = node.textContent; t.contentEditable = 'true'; t.classList.add('dmEdit'); t.focus();
    const r = document.createRange(); r.selectNodeContents(node); const s = getSelection(); s.removeAllRanges(); s.addRange(r);
  }, true);
  const endEdit = keep => {
    const t = editing; if (!t) return; editing = null; t.contentEditable = 'false'; t.classList.remove('dmEdit');
    const node = textNode(t, true), from = t.dataset.dmFrom, to = node.textContent.replace(/\s+/g, ' ').trim(); delete t.dataset.dmFrom;
    if (!keep || to === from || !to) { node.textContent = from; return; }
    node.textContent = to; record({ kind: 'text', sel: path(t), what: plain(describe(t)), from, to }, t); if (sel) { box.innerHTML = '<i>' + plain(describe(sel)) + '</i>'; buildKnobs(sel); }
  };

  /* ---------- keys ---------- */
  window.addEventListener('keydown', ev => {
    if (knobs.contains(ev.target) || paused) return;
    if (editing) { if (ev.key === 'Enter') { ev.preventDefault(); endEdit(true); } else if (ev.key === 'Escape') { ev.preventDefault(); endEdit(false); } ev.stopImmediatePropagation(); return; }
    if ((ev.ctrlKey || ev.metaKey) && ev.key === 'z') { ev.preventDefault(); ev.stopImmediatePropagation(); undo(); return; }
    if (!sel) return; ev.stopImmediatePropagation();
    if (ev.key === 'Escape') { select(null); return; }
    if (ev.key === 'p') { const p = sel.parentElement && boxOf(sel.parentElement); if (p) select(p); return; }
    if ((ev.key === 'Delete' || ev.key === 'Backspace') && sel !== ROOT) { ev.preventDefault(); record({ kind: 'hide', sel: path(sel), what: plain(describe(sel)), from: sel.style.display }, sel); sel.style.display = 'none'; select(null); return; }
    const back = ev.key === 'ArrowLeft' || ev.key === 'ArrowUp', fwd = ev.key === 'ArrowRight' || ev.key === 'ArrowDown';
    if ((back || fwd) && sel !== ROOT) {
      ev.preventDefault(); const p = sel.parentElement, kids = [...p.children].filter(k => k.offsetParent !== null && !k.classList.contains('dm')), i = kids.indexOf(sel), j = i + (back ? -1 : 1); if (j < 0 || j >= kids.length) return;
      const from = { sel: path(p), index: [...p.children].indexOf(sel), where: section(sel) }, s0 = path(sel);
      p.insertBefore(sel, back ? kids[j] : kids[j].nextSibling);
      record({ kind: 'move', sel: s0, what: plain(describe(sel)), from, to: { sel: path(p), index: [...p.children].indexOf(sel), where: section(sel) } }, sel, p, p);
    }
  }, true);

  /* ---------- the bar ---------- */
  const undo = () => { const o = ops.pop(); if (!o) return; try { revert(o); } catch (_) {} show(); if (sel) buildKnobs(sel); };
  document.getElementById('dmUndo').onclick = undo;
  const pauseBtn = document.getElementById('dmPause');
  pauseBtn.onclick = () => {
    paused = !paused; if (editing) endEdit(true); drag = null; select(null); hov.style.display = 'none';
    pauseBtn.textContent = paused ? 'resume' : 'pause'; bar.style.borderStyle = paused ? 'dashed' : 'solid';
    hint.textContent = paused ? 'paused · the page works as usual · resume to keep designing' : HINT;
  };
  const brief = () => {
    const page = location.pathname.replace(/^\//, '') || 'index.html', when = new Date().toLocaleString('en-US', { hour12: false });
    return 'design mode · ' + location.host + '/' + page + ' · ' + when + '\n\n' + ops.map((o, i) => (i + 1) + '. ' + plain(english(o)) + '\n   ' + JSON.stringify(o)).join('\n') + '\n';
  };
  document.getElementById('dmCopy').onclick = async () => { const b = document.getElementById('dmCopy'); try { await navigator.clipboard.writeText(brief()); b.textContent = 'copied'; } catch (_) { b.textContent = 'no clipboard'; } setTimeout(() => b.textContent = 'copy', 1200); };
  document.getElementById('dmSave').onclick = () => { const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([brief()], { type: 'text/plain' })); a.download = 'design-changes.txt'; a.click(); };
  document.getElementById('dmClear').onclick = () => { while (ops.length) { const o = ops.pop(); try { revert(o); } catch (_) {} } show(); select(null); };
  document.getElementById('dmDone').onclick = () => { const u = new URL(location.href); u.searchParams.delete('design'); location.href = u.toString(); };
  show();
  window.__dm = { ops, select, brief };
})();
