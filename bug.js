/* report a bug: a button in the top bar (and in the project menu on phones) opens a note box. what the person writes goes off with what
   the page can say about itself — the page, language, theme, the tool and view open, the site, units, browser, screen, and any errors it
   hit — so a report can be acted on without a conversation.

   WHERE REPORTS LAND: fill in FORM below with a google form and reports drop straight into its sheet. Until then the box still works:
   it copies the report, or opens it in a mail app. To wire the form up:
     1. forms.google.com → blank form → three "paragraph" questions, in this order: what happened · name · details
     2. Send → the link icon → copy the form's address (…/viewform)
     3. open that address, view source, and read the three entry.NNNNNNN ids in order
     4. put the …/formResponse address in FORM.url and the three ids in FORM.text, FORM.name, FORM.info
     5. Responses → link to a sheet
   Nothing about the person is sent beyond what they type and the state above. */
(() => {
  const FORM = { url: '', text: '', name: '', info: '' };   // e.g. url: 'https://docs.google.com/forms/d/e/FORM_ID/formResponse', text: 'entry.1111', name: 'entry.2222', info: 'entry.3333'
  const MAIL = 'zolaray25@gmail.com';
  const errs = [];
  const note = e => { const s = String(e).slice(0, 300); if (!errs.includes(s)) errs.push(s); if (errs.length > 12) errs.shift(); };
  addEventListener('error', e => note((e.message || e.type) + (e.filename ? ' @ ' + e.filename.split('/').pop() + ':' + e.lineno : '')));
  addEventListener('unhandledrejection', e => note('promise: ' + (e.reason && (e.reason.message || e.reason))));

  /* what the page can say about itself */
  function state() {
    const o = { page: location.pathname.split('/').pop() || 'index.html', when: new Date().toISOString(), lang: document.documentElement.lang || 'en', theme: document.documentElement.dataset.theme || 'light',
      screen: `${innerWidth}×${innerHeight}`, browser: navigator.userAgent };
    try { const u = window.__ui2; if (u) { o.task = u.state.task; o.tool = u.state.tool && (u.state.tool[u.state.task] || u.state.tool); o.view = u.state.view; } } catch (_) {}
    try { window.__dbg(({ S }) => { o.site = S.world ? `${S.world.name} · ${S.world.lat.toFixed(5)}, ${S.world.lon.toFixed(5)}` : 'sample sheet';
      o.width_m = Math.round(S.siteW); o.rotation = S.rot + '°'; o.units = S.unit; o.brush = S.brush; o.mode = S.mode; o.drawings = (S.strokes || []).length; }); } catch (_) {}
    if (errs.length) o.errors = errs.slice();
    return o;
  }
  const asText = (what, who) => `${what.trim() || '(nothing written)'}\n\n— ${who.trim() || 'not given'}\n\n${Object.entries(state()).map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(' | ') : v}`).join('\n')}`;

  /* the box */
  const css = document.createElement('style'); css.textContent = `
#bugWrap{position:fixed;inset:0;z-index:120;background:rgba(20,20,18,.45);display:none;align-items:center;justify-content:center;padding:16px}
#bugWrap.show{display:flex}
#bugCard{background:var(--panel,#f4f3ee);color:var(--ink,#282826);border:1px solid var(--ink2,#8b8a84);border-radius:4px;box-shadow:0 10px 40px rgba(0,0,0,.3);width:min(460px,100%);max-height:90vh;overflow:auto;padding:14px 16px;font-size:12px}
#bugCard h3{margin:0 0 2px;font-size:13px;font-weight:600}
#bugCard p{margin:0 0 10px;color:var(--ink2,#6b6a65);line-height:1.45}
#bugCard label{display:block;margin-bottom:8px}
#bugCard span.lbl{display:block;font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--ink2,#6b6a65);margin-bottom:3px}
#bugCard textarea,#bugCard input{font:inherit;font-size:12px;width:100%;box-sizing:border-box;padding:6px 8px;border:1px solid #9a9992;border-radius:3px;background:var(--paper,#fbfaf6);color:var(--ink,#282826)}
#bugCard textarea{min-height:92px;resize:vertical}
#bugCard details{margin:2px 0 12px;color:var(--ink2,#6b6a65)}
#bugCard details pre{margin:6px 0 0;padding:8px;background:var(--paper,#fbfaf6);border:1px solid var(--line,#ddd);border-radius:3px;white-space:pre-wrap;word-break:break-word;font-size:11px;max-height:160px;overflow:auto}
#bugCard .row{display:flex;gap:6px;flex-wrap:wrap;align-items:center}
#bugCard .row .sp{flex:1}
#bugCard .said{color:var(--accent,#c96b3a)}
:root[data-theme=dark] #bugCard textarea,:root[data-theme=dark] #bugCard input{border-color:#55554f}
@media (max-width:760px){#bugBtn{display:none}}`;
  document.head.append(css);

  const el = (t, p = {}, kids = []) => { const n = document.createElement(t); for (const k in p) k === 'text' ? n.append(p[k]) : k === 'cls' ? n.className = p[k] : n.setAttribute(k, p[k]); kids.forEach(k => n.append(k)); return n; };
  const wrap = el('div', { id: 'bugWrap' }), card = el('div', { id: 'bugCard' });
  const what = el('textarea', { placeholder: 'what were you doing, and what went wrong?' }), who = el('input', { type: 'text', placeholder: 'your name (so we can ask)' });
  const info = el('pre'), said = el('span', { cls: 'said' });
  const send = el('button', { cls: 'u2b', type: 'button', text: 'send it' }), copy = el('button', { cls: 'u2b', type: 'button', text: 'copy it' }),
        mail = el('a', { cls: 'u2b', href: '#', text: 'email it' }), shut = el('button', { cls: 'u2b', type: 'button', text: 'close' });
  card.append(el('h3', { text: 'report a bug' }), el('p', { text: 'say what happened in your own words. what the page was doing goes along with it, so it can be fixed without asking you again.' }),
    el('label', {}, [el('span', { cls: 'lbl', text: 'what happened' }), what]), el('label', {}, [el('span', { cls: 'lbl', text: 'your name' }), who]),
    el('details', {}, [el('summary', { text: 'what goes with it' }), info]), el('div', { cls: 'row' }, [send, copy, mail, el('span', { cls: 'sp' }), shut, said]));
  wrap.append(card); document.body.append(wrap);

  const fill = () => { info.textContent = Object.entries(state()).map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(' | ') : v}`).join('\n'); };
  const open = () => { said.textContent = ''; send.disabled = false; fill(); wrap.classList.add('show'); what.focus(); };
  const close = () => { wrap.classList.remove('show'); what.value = ''; };
  shut.onclick = close; wrap.onclick = e => { if (e.target === wrap) close(); };
  addEventListener('keydown', e => { if (e.key === 'Escape' && wrap.classList.contains('show')) close(); });

  send.onclick = async () => {
    const body = asText(what.value, who.value);
    if (!FORM.url) { copy.click(); return; }
    const fd = new FormData(); fd.append(FORM.text, what.value.trim() || '(nothing written)'); if (FORM.name) fd.append(FORM.name, who.value.trim()); if (FORM.info) fd.append(FORM.info, body);
    send.disabled = true; said.textContent = 'sending…';
    try { await fetch(FORM.url, { method: 'POST', mode: 'no-cors', body: fd }); said.textContent = 'thank you · it is on its way'; setTimeout(close, 1800); }
    catch (_) { send.disabled = false; said.textContent = 'it would not send · copy it instead'; }
  };
  copy.onclick = async () => { const body = asText(what.value, who.value);
    try { await navigator.clipboard.writeText(body); said.textContent = 'copied · paste it in a message'; }
    catch (_) { what.value = body; what.select(); said.textContent = 'press copy on your keyboard'; } };
  mail.onclick = e => { e.preventDefault(); mail.href = `mailto:${MAIL}?subject=${encodeURIComponent('coyote mountain · bug report')}&body=${encodeURIComponent(asText(what.value, who.value))}`; location.href = mail.href; };

  /* the way in: the top bar on a screen with room, the project menu on a phone */
  const head = document.getElementById('u2head');
  const btn = el('button', { id: 'bugBtn', cls: 'u2b', type: 'button', text: 'report a bug', 'data-tip': 'something wrong? say what happened; what the page was doing goes with it' });
  btn.onclick = open;
  if (head) head.insertBefore(btn, head.lastElementChild); else document.body.append(btn);
  const proj = document.getElementById('u2proj');
  if (proj) { const b2 = el('button', { cls: 'u2b', type: 'button', text: 'report a bug', style: 'width:100%;margin-top:6px' }); b2.onclick = () => { open(); const d = proj.closest('details'); if (d) d.open = false; }; proj.append(b2); }
  window.coyoteBug = { open, state };
})();
