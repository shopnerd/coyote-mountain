/* design mode — prototype. open topo.html?design and the rail becomes editable by hand:
   click selects · drag moves a piece (its neighbours reflow) · double-click edits the words ·
   the numbers beside the selection scrub like a slider · delete hides · arrows nudge · ctrl-z undoes.
   every change is written down in plain english (copy) and as data (save) so the source can be patched to match.
   nothing here touches the page unless ?design is in the address. */
(() => {
  const RAIL = document.querySelector('aside'); if (!RAIL) return;
  const UNIT = 'button,.p,.sec,.desc,.stat,select,input[type=text]';
  const BOX = '.seg,.actions,.params,.stats,aside';
  const px = v => (Math.round(v * 4) / 4) + 'px';
  const num = s => parseFloat(s) || 0;

  const css = document.createElement('style'); css.textContent = `
  .dm{position:fixed;z-index:9000;font:11.5px/1.5 var(--font);color:var(--ink)}
  #dmBar{bottom:40px;left:50%;transform:translateX(-50%);display:flex;align-items:center;gap:6px;background:var(--paper);border:1px solid var(--accent);border-radius:3px;padding:4px 8px;box-shadow:0 4px 18px rgba(0,0,0,.18);white-space:nowrap}
  #dmBar b{color:var(--accent);font-weight:500;margin-right:4px}
  #dmBar .n{color:var(--ink3);margin-right:6px}
  .dm button{border:1px solid var(--line);background:transparent;color:var(--ink);font:inherit;font-size:11px;padding:2px 9px;border-radius:3px;cursor:pointer}
  .dm button:hover{background:var(--hover)}
  #dmBox{pointer-events:none;border:1px solid var(--accent);box-shadow:0 0 0 3px rgba(201,107,58,.18);border-radius:3px;display:none}
  #dmBox i{position:absolute;left:-1px;bottom:100%;margin-bottom:3px;background:var(--accent);color:#fff;font-style:normal;font-size:10px;padding:1px 6px;border-radius:2px;white-space:nowrap}
  #dmHover{pointer-events:none;border:1px dashed var(--accent);opacity:.5;border-radius:3px;display:none}
  #dmKnobs{width:200px;background:var(--paper);border:1px solid var(--accent);border-radius:3px;box-shadow:0 6px 24px rgba(0,0,0,.2);padding:8px 10px;display:none}
  #dmKnobs .t{font-size:11px;color:var(--ink2);margin-bottom:6px;display:flex;align-items:center;gap:6px}
  #dmKnobs .t b{flex:1;font-weight:500;color:var(--ink);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  #dmKnobs .t button{padding:0 6px;font-size:10px}
  .dmK{display:flex;align-items:center;gap:6px;padding:3px 0;cursor:ew-resize;user-select:none;border-top:1px solid var(--line)}
  .dmK .l{flex:1;color:var(--ink2);font-size:10.5px;text-transform:uppercase;letter-spacing:.05em}
  .dmK .v{min-width:34px;text-align:right;font-variant-numeric:tabular-nums;padding:0 3px;border-radius:2px;outline:none;cursor:text}
  .dmK .v:focus{background:#fdf3ea;box-shadow:0 0 0 1px var(--accent)}
  .dmK .u{color:var(--ink3);width:16px;font-size:10px}
  .dmK:hover .l{color:var(--ink)}
  #dmList{right:12px;bottom:12px;width:300px;max-height:40vh;overflow:auto;background:var(--paper);border:1px solid var(--line);border-radius:3px;padding:6px 10px;display:none}
  #dmList div{padding:2px 0;border-top:1px solid var(--line);color:var(--ink2);font-size:11px}
  #dmList div:first-child{border:0}
  #dmList div b{font-weight:500;color:var(--ink)}
  .dmGhost{position:fixed;z-index:9001;pointer-events:none;opacity:.75;transform:rotate(-1deg);box-shadow:0 8px 24px rgba(0,0,0,.25)}
  .dmDrag{opacity:.35!important}
  .dmEdit{outline:none;box-shadow:inset 0 0 0 1px var(--accent);background:#fdf3ea!important;cursor:text!important}
  #dmHint{bottom:14px;left:50%;transform:translateX(-50%);color:var(--ink3);font-size:10.5px;pointer-events:none;white-space:nowrap}
  :root[data-theme=dark] .dmK .v:focus,:root[data-theme=dark] .dmEdit{background:#3a2a20!important}`;
  document.head.appendChild(css);

  const el = (id, cls) => { const d = document.createElement('div'); d.id = id; d.className = 'dm' + (cls ? ' ' + cls : ''); document.body.appendChild(d); return d; };
  const bar = el('dmBar'), box = el('dmBox'), hov = el('dmHover'), knobs = el('dmKnobs'), list = el('dmList'), hint = el('dmHint');
  bar.innerHTML = '<b>design mode</b><span class="n" id="dmN">no changes</span><button id="dmUndo">undo</button><button id="dmCopy">copy</button><button id="dmSave">save</button><button id="dmClear">clear</button><button id="dmDone">done</button>';
  hint.textContent = 'click to select · drag to move · double-click to edit the words · scrub the numbers · delete hides · esc';

  /* ---------- naming things for humans and for the patch ---------- */
  const words = e => {
    if (!e) return '';
    if (e.matches('.p')) { const l = e.querySelector('label'); return l ? (l.firstChild && l.firstChild.textContent || l.textContent).trim() : 'slider'; }
    if (e.matches('select,input')) return e.id || e.tagName.toLowerCase();
    return (e.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 28);
  };
  const path = e => {
    if (e === RAIL) return 'aside';
    if (e.id) return '#' + e.id;
    const p = e.parentElement, i = [...p.children].indexOf(e) + 1;
    return path(p) + ' > ' + e.tagName.toLowerCase() + ':nth-child(' + i + ')';
  };
  const section = e => {
    let n = e; while (n && n !== RAIL) { let s = n.previousElementSibling; while (s) { if (s.matches('.sec')) return words(s); s = s.previousElementSibling; } n = n.parentElement; }
    return 'rail';
  };
  const describe = e => {
    if (e === RAIL) return 'the rail';
    if (e.matches('.sec')) return 'heading “' + words(e) + '”';
    if (e.matches(BOX)) return section(e) + ' › ' + (e.id ? '#' + e.id : e.className.split(' ')[0] || e.tagName.toLowerCase()) + ' row';
    return '“' + words(e) + '”' + (e.matches('.p') ? ' slider' : '');
  };

  /* ---------- the ledger ---------- */
  let ops = []; try { ops = JSON.parse(localStorage.getItem('dm-ops') || '[]'); } catch (_) { ops = []; }
  const english = o => {
    if (o.kind === 'move') return 'move <b>' + o.what + '</b> to position ' + (o.to.index + 1) + ' in ' + o.to.where;
    if (o.kind === 'text') return 'rename <b>' + o.from + '</b> → <b>' + o.to + '</b>';
    if (o.kind === 'hide') return 'hide <b>' + o.what + '</b>';
    if (o.kind === 'var') return 'rail width ' + o.from + ' → <b>' + o.to + '</b>';
    return '<b>' + o.what + '</b>: ' + o.label + ' ' + (o.from || 'default') + ' → <b>' + o.to + '</b>';
  };
  const plain = s => s.replace(/<\/?b>/g, '');
  const show = () => {
    document.getElementById('dmN').textContent = ops.length ? ops.length + (ops.length === 1 ? ' change' : ' changes') : 'no changes';
    list.style.display = ops.length ? 'block' : 'none';
    list.innerHTML = ops.map((o, i) => '<div>' + (i + 1) + '. ' + english(o) + '</div>').join('');
    list.scrollTop = 1e6;
    try { localStorage.setItem('dm-ops', JSON.stringify(ops)); } catch (_) {}
  };
  const live = (o, e, fp, tp) => { for (const [k, v] of [['el', e], ['fp', fp], ['tp', tp]]) if (v) Object.defineProperty(o, k, { value: v, enumerable: false, writable: true }); return o; };
  const record = (o, e, fp, tp) => { ops.push(live(o, e, fp, tp)); show(); };

  const apply = o => {
    if (o.kind === 'var') { document.documentElement.style.setProperty('--rail', o.to); return; }
    const e = o.sel === 'aside' ? RAIL : document.querySelector(o.sel); if (!e) return;
    if (o.kind === 'move') { const p = o.to.sel === 'aside' ? RAIL : document.querySelector(o.to.sel); if (!p) return; live(o, e, e.parentElement, p); const kids = [...p.children].filter(k => k !== e); p.insertBefore(e, kids[o.to.index] || null); return; }
    live(o, e);
    if (o.kind === 'text') { textNode(e).textContent = o.to; }
    else if (o.kind === 'hide') { e.style.display = 'none'; }
    else e.style[o.prop] = o.to;
  };
  const revert = o => {
    if (o.kind === 'var') { document.documentElement.style.setProperty('--rail', o.from); return; }
    const e = o.el || (o.sel === 'aside' ? RAIL : document.querySelector(o.sel)); if (!e) return;
    if (o.kind === 'move') { const p = o.fp || (o.from.sel === 'aside' ? RAIL : document.querySelector(o.from.sel)); if (!p) return; const kids = [...p.children].filter(k => k !== e); p.insertBefore(e, kids[o.from.index] || null); }
    else if (o.kind === 'text') { textNode(e).textContent = o.from; }
    else if (o.kind === 'hide') { e.style.display = o.from; }
    else e.style[o.prop] = o.from;
  };
  const textNode = e => {
    let t = e.matches('.p') ? e.querySelector('label') : e;
    for (const n of t.childNodes) if (n.nodeType === 3 && n.textContent.trim()) return n;
    const n = document.createTextNode(''); t.appendChild(n); return n;
  };
  ops.forEach(o => { try { apply(o); } catch (_) {} });

  /* ---------- selection ---------- */
  let sel = null, editing = null;
  const rect = (d, e, pad) => { const r = e.getBoundingClientRect(); d.style.left = (r.left - pad) + 'px'; d.style.top = (r.top - pad) + 'px'; d.style.width = (r.width + pad * 2) + 'px'; d.style.height = (r.height + pad * 2) + 'px'; };
  const select = e => {
    sel = e; if (!e) { box.style.display = 'none'; knobs.style.display = 'none'; return; }
    box.style.display = 'block'; box.innerHTML = '<i>' + plain(describe(e)) + '</i>'; buildKnobs(e);
  };
  const tick = () => {
    if (sel && sel.isConnected) {
      rect(box, sel, 2);
      const r = RAIL.getBoundingClientRect(), s = sel.getBoundingClientRect();
      knobs.style.left = (r.right + 14) + 'px'; knobs.style.top = Math.max(48, Math.min(s.top, innerHeight - knobs.offsetHeight - 12)) + 'px';
      knobs.style.display = 'block';
    }
    requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);

  const unitAt = t => { const u = t.closest(UNIT); if (u && RAIL.contains(u)) return u; const b = t.closest(BOX); return b && RAIL.contains(b) ? b : null; };

  /* ---------- knobs: the numbers that scrub ---------- */
  const KN = [
    ['text size', 'fontSize', 'font-size', 'px', 6, 30, .5],
    ['height', 'minHeight', 'min-height', 'px', 0, 80, 1],
    ['pad ↕', 'py', null, 'px', 0, 30, .5],
    ['pad ↔', 'px', null, 'px', 0, 40, .5],
    ['corner', 'borderRadius', 'border-radius', 'px', 0, 24, .5],
    ['space above', 'marginTop', 'margin-top', 'px', -10, 40, 1],
    ['weight', 'flexGrow', 'flex-grow', '', 0, 6, 1],
    ['gap', 'gap', 'gap', 'px', 0, 30, 1],
    ['letters', 'letterSpacing', 'letter-spacing', 'px', -1, 6, .1],
    ['rail width', '--rail', null, 'px', 180, 520, 2]
  ];
  const read = (e, k) => {
    const cs = getComputedStyle(e);
    if (k === '--rail') return num(getComputedStyle(document.documentElement).getPropertyValue('--rail')) || RAIL.getBoundingClientRect().width;
    if (k === 'py') return num(cs.paddingTop); if (k === 'px') return num(cs.paddingLeft);
    return num(cs[k]);
  };
  const applyKnob = (e, k, v, unit) => {
    if (k === '--rail') { document.documentElement.style.setProperty('--rail', v + 'px'); return v + 'px'; }
    if (k === 'py' || k === 'px') { const cs = getComputedStyle(e), py = k === 'py' ? v : num(cs.paddingTop), pxx = k === 'px' ? v : num(cs.paddingLeft); e.style.padding = px(py) + ' ' + px(pxx); return e.style.padding; }
    e.style[k] = unit ? px(v) : String(v); return e.style[k];
  };
  const buildKnobs = e => {
    const isBox = e.matches(BOX), pFlex = e !== RAIL && getComputedStyle(e.parentElement).display.includes('flex') && getComputedStyle(e.parentElement).flexDirection === 'row';
    const rows = KN.filter(([, k]) => {
      if (k === '--rail') return e === RAIL;
      if (k === 'gap') return isBox && e !== RAIL;
      if (k === 'flexGrow') return pFlex;
      if (k === 'letterSpacing') return e.matches('.sec');
      if (k === 'py' || k === 'px' || k === 'borderRadius' || k === 'minHeight') return !isBox;
      if (k === 'fontSize') return e !== RAIL;
      return !isBox || e.matches('.seg,.actions');
    });
    knobs.innerHTML = '<div class="t"><b>' + plain(describe(e)) + '</b>' + (e !== RAIL ? '<button data-up>▲ parent</button>' : '') + '</div>' +
      rows.map(([l, k, , u, , , ]) => '<div class="dmK" data-k="' + k + '"><span class="l">' + l + '</span><span class="v" contenteditable spellcheck="false">' + (+read(e, k).toFixed(2)) + '</span><span class="u">' + u + '</span></div>').join('');
    knobs.querySelector('[data-up]')?.addEventListener('click', () => { const p = e.parentElement.closest(BOX); if (p) select(p); });
  };
  knobs.addEventListener('pointerdown', ev => {
    const row = ev.target.closest('.dmK'); if (!row || ev.target.classList.contains('v') || !sel) return;
    ev.preventDefault(); const e = sel, spec = KN.find(s => s[1] === row.dataset.k), [label, k, prop, unit, lo, hi, step] = spec;
    const v0 = read(e, k), x0 = ev.clientX, before = k === '--rail' ? v0 + 'px' : (k === 'py' || k === 'px') ? e.style.padding : e.style[k];
    let v = v0; row.setPointerCapture(ev.pointerId);
    const mv = m => { const fine = m.altKey ? .25 : m.shiftKey ? 5 : 1; v = Math.min(hi, Math.max(lo, v0 + Math.round((m.clientX - x0) / 3 * fine / step) * step)); row.querySelector('.v').textContent = +v.toFixed(2); applyKnob(e, k, v, unit); };
    const up = () => { row.removeEventListener('pointermove', mv); row.removeEventListener('pointerup', up); if (v !== v0) commitKnob(e, spec, before, v); };
    row.addEventListener('pointermove', mv); row.addEventListener('pointerup', up);
  });
  knobs.addEventListener('keydown', ev => {
    if (!ev.target.classList.contains('v')) return; ev.stopPropagation();
    if (ev.key === 'Enter') { ev.preventDefault(); ev.target.blur(); }
    if (ev.key === 'Escape') { ev.preventDefault(); ev.target.blur(); }
  });
  knobs.addEventListener('focusout', ev => {
    if (!ev.target.classList.contains('v') || !sel) return;
    const row = ev.target.closest('.dmK'), spec = KN.find(s => s[1] === row.dataset.k), [, k, , unit, lo, hi] = spec, e = sel;
    const v0 = read(e, k), v = Math.min(hi, Math.max(lo, num(ev.target.textContent))); ev.target.textContent = +v.toFixed(2);
    if (v === v0) return; const before = k === '--rail' ? v0 + 'px' : (k === 'py' || k === 'px') ? e.style.padding : e.style[k];
    applyKnob(e, k, v, unit); commitKnob(e, spec, before, v);
  });
  const commitKnob = (e, [label, k, prop, unit], before, v) => {
    if (k === '--rail') { record({ kind: 'var', name: '--rail', from: before, to: v + 'px' }); return; }
    const styleProp = (k === 'py' || k === 'px') ? 'padding' : k;
    record({ kind: 'style', sel: path(e), what: plain(describe(e)), where: section(e), label: (k === 'py' || k === 'px') ? 'padding' : label, prop: styleProp, css: (k === 'py' || k === 'px') ? 'padding' : prop, from: before, to: e.style[styleProp] }, e);
  };

  /* ---------- pointer: select, drag to move ---------- */
  let drag = null;
  const boxes = () => [...RAIL.querySelectorAll(BOX)].filter(b => b.offsetParent !== null).concat(RAIL);
  window.addEventListener('pointerdown', ev => {
    if (editing) { if (!editing.contains(ev.target)) endEdit(true); else return; }
    if (ev.target.closest('.dm')) return;
    if (!RAIL.contains(ev.target)) { if (ev.target.id !== 'railGrip') select(null); return; }
    ev.preventDefault(); ev.stopImmediatePropagation();
    const u = unitAt(ev.target); if (!u) { select(RAIL); return; }
    select(u); if (u === RAIL) return;
    drag = { e: u, sel: path(u), x: ev.clientX, y: ev.clientY, on: false, from: { sel: path(u.parentElement), index: [...u.parentElement.children].indexOf(u), where: section(u) } };
  }, true);
  window.addEventListener('pointermove', ev => {
    if (!RAIL.contains(ev.target) && !drag?.on) { hov.style.display = 'none'; }
    if (drag && !drag.on && Math.hypot(ev.clientX - drag.x, ev.clientY - drag.y) > 4) {
      drag.on = true; const g = drag.e.cloneNode(true); g.className += ' dmGhost'; const r = drag.e.getBoundingClientRect();
      g.style.width = r.width + 'px'; g.style.height = r.height + 'px'; g.style.margin = 0; document.body.appendChild(g); drag.g = g; drag.dx = ev.clientX - r.left; drag.dy = ev.clientY - r.top;
      drag.e.classList.add('dmDrag'); drag.fp = drag.e.parentElement; document.body.style.cursor = 'grabbing';
    }
    if (drag?.on) {
      ev.preventDefault(); drag.g.style.left = (ev.clientX - drag.dx) + 'px'; drag.g.style.top = (ev.clientY - drag.dy) + 'px';
      const under = document.elementsFromPoint(ev.clientX, ev.clientY).find(t => RAIL.contains(t) || t === RAIL); if (!under) return;
      let b = under.closest(BOX) || RAIL; if (drag.e.contains(b)) return;
      const kids = [...b.children].filter(k => k !== drag.e && k.offsetParent !== null && !k.matches('input[type=file]'));
      const cs = getComputedStyle(b), row = cs.display.includes('flex') && cs.flexDirection === 'row';
      const over = kids.find(k => { const r = k.getBoundingClientRect(); return ev.clientX >= r.left && ev.clientX <= r.right && ev.clientY >= r.top && ev.clientY <= r.bottom; });
      let ref;
      if (over) { const r = over.getBoundingClientRect(), before = row ? ev.clientX < r.left + r.width / 2 : ev.clientY < r.top + r.height / 2; ref = before ? over : over.nextElementSibling; }
      else if (b !== drag.e.parentElement) { const last = kids[kids.length - 1], lr = last && last.getBoundingClientRect(); ref = !last || ev.clientY > lr.top + lr.height / 2 ? null : kids[0]; }
      else return;
      if (ref === drag.e) return;
      if (ref === null ? b.lastElementChild !== drag.e : drag.e.nextSibling !== ref) b.insertBefore(drag.e, ref);
      return;
    }
    if (RAIL.contains(ev.target) && !editing) { const u = unitAt(ev.target); if (u && u !== sel && u !== RAIL) { hov.style.display = 'block'; rect(hov, u, 1); } else hov.style.display = 'none'; }
  }, true);
  window.addEventListener('pointerup', ev => {
    if (!drag) return; if (drag.on) {
      ev.preventDefault(); ev.stopImmediatePropagation(); drag.g.remove(); drag.e.classList.remove('dmDrag'); document.body.style.cursor = '';
      const to = { sel: path(drag.e.parentElement), index: [...drag.e.parentElement.children].indexOf(drag.e), where: section(drag.e) };
      if (to.sel !== drag.from.sel || to.index !== drag.from.index) record({ kind: 'move', sel: drag.sel, what: plain(describe(drag.e)), from: drag.from, to }, drag.e, drag.fp, drag.e.parentElement);
    }
    drag = null;
  }, true);
  window.addEventListener('click', ev => { if (RAIL.contains(ev.target) && !editing) { ev.preventDefault(); ev.stopImmediatePropagation(); } }, true);
  RAIL.addEventListener('scroll', () => { hov.style.display = 'none'; });

  /* ---------- double-click: edit the words ---------- */
  window.addEventListener('dblclick', ev => {
    if (!RAIL.contains(ev.target) || editing) return; ev.preventDefault(); ev.stopImmediatePropagation();
    const u = unitAt(ev.target); if (!u || u === RAIL || u.matches(BOX) || u.matches('select,input')) return;
    const t = u.matches('.p') ? u.querySelector('label') : u; const node = textNode(u);
    editing = t; t.dataset.dmFrom = node.textContent; t.contentEditable = 'true'; t.classList.add('dmEdit'); t.focus();
    const r = document.createRange(); r.selectNodeContents(node); const s = getSelection(); s.removeAllRanges(); s.addRange(r);
  }, true);
  const endEdit = (keep) => {
    const t = editing; if (!t) return; editing = null; t.contentEditable = 'false'; t.classList.remove('dmEdit');
    const u = t.closest(UNIT) || t, node = textNode(u), from = t.dataset.dmFrom, to = node.textContent.replace(/\s+/g, ' ').trim();
    if (!keep || to === from || !to) { node.textContent = from; return; }
    node.textContent = to; record({ kind: 'text', sel: path(u), what: plain(describe(u)), from, to }, u); box.innerHTML = '<i>' + plain(describe(u)) + '</i>'; buildKnobs(u);
  };

  /* ---------- keys ---------- */
  window.addEventListener('keydown', ev => {
    if (knobs.contains(ev.target)) return;
    if (editing) { if (ev.key === 'Enter') { ev.preventDefault(); endEdit(true); } else if (ev.key === 'Escape') { ev.preventDefault(); endEdit(false); } ev.stopImmediatePropagation(); return; }
    if ((ev.ctrlKey || ev.metaKey) && ev.key === 'z') { ev.preventDefault(); ev.stopImmediatePropagation(); undo(); return; }
    if (!sel) return; ev.stopImmediatePropagation();
    if (ev.key === 'Escape') { select(null); return; }
    if (ev.key === 'p') { const p = sel.parentElement?.closest(BOX); if (p) select(p); return; }
    if ((ev.key === 'Delete' || ev.key === 'Backspace') && sel !== RAIL) { ev.preventDefault(); record({ kind: 'hide', sel: path(sel), what: plain(describe(sel)), from: sel.style.display }, sel); sel.style.display = 'none'; select(null); return; }
    const back = ev.key === 'ArrowLeft' || ev.key === 'ArrowUp', fwd = ev.key === 'ArrowRight' || ev.key === 'ArrowDown';
    if ((back || fwd) && sel !== RAIL) {
      ev.preventDefault(); const p = sel.parentElement, kids = [...p.children].filter(k => k.offsetParent !== null), i = kids.indexOf(sel), j = i + (back ? -1 : 1); if (j < 0 || j >= kids.length) return;
      const from = { sel: path(p), index: [...p.children].indexOf(sel), where: section(sel) }, s0 = path(sel);
      p.insertBefore(sel, back ? kids[j] : kids[j].nextSibling);
      record({ kind: 'move', sel: s0, what: plain(describe(sel)), from, to: { sel: path(p), index: [...p.children].indexOf(sel), where: section(sel) } }, sel, p, p);
    }
  }, true);

  /* ---------- the bar ---------- */
  const undo = () => { const o = ops.pop(); if (!o) return; try { revert(o); } catch (_) {} show(); if (sel) buildKnobs(sel); };
  document.getElementById('dmUndo').onclick = undo;
  const brief = () => {
    const page = location.pathname.split('/').pop() || 'index.html', when = new Date().toLocaleString('en-US', { hour12: false });
    return 'design mode · ' + page + ' · ' + when + '\n\n' + ops.map((o, i) => (i + 1) + '. ' + plain(english(o)) + '\n   ' + JSON.stringify(o)).join('\n') + '\n';
  };
  document.getElementById('dmCopy').onclick = async () => { const b = document.getElementById('dmCopy'); try { await navigator.clipboard.writeText(brief()); b.textContent = 'copied'; } catch (_) { b.textContent = 'no clipboard'; } setTimeout(() => b.textContent = 'copy', 1200); };
  document.getElementById('dmSave').onclick = () => { const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([brief()], { type: 'text/plain' })); a.download = 'design-changes.txt'; a.click(); };
  document.getElementById('dmClear').onclick = () => { while (ops.length) { const o = ops.pop(); try { revert(o); } catch (_) {} } show(); select(null); };
  document.getElementById('dmDone').onclick = () => { const u = new URL(location.href); u.searchParams.delete('design'); location.href = u.toString(); };
  show();
  window.__dm = { ops, select, brief };
})();
