// writes book/reference.md from the tool itself: every task, tool, control and hover description, so the manual cannot drift from the page
// run: python -m http.server 8765 (in coyote-studio), then: node book/tools/make-reference.js <path to playwright-core> [http://localhost:8765]
const { chromium } = require(process.argv[2]); const fs = require('fs'), path = require('path');
const base = process.argv[3] || 'http://localhost:8765';
const clean = t => String(t || '').replace(/\s+/g, ' ').trim();
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1400, height: 900 } });
  await p.goto(base + '/topo.html'); await p.waitForFunction(() => window.__dbg && window.__dbg(({ S }) => !!(S.world && S.terrainVer)), null, { timeout: 60000 }); await p.waitForTimeout(1500);
  await p.evaluate(() => { const c = document.getElementById('tourCard'); if (c) c.classList.remove('show'); });
  const read = sel => p.evaluate(sel => { const out = []; const seen = new Set();
    for (const el of document.querySelectorAll(sel)) { const r = el.getBoundingClientRect(); if (!r.width || !r.height) continue;
      if (el.closest('#u2tools') && !el.closest('.u2panel')) continue;
      let label; if (el.tagName === 'SELECT' || el.tagName === 'INPUT') label = el.getAttribute('aria-label') || ''; else if (el.classList.contains('p')) { const lb = el.querySelector('label'); label = lb ? [...lb.childNodes].filter(n => n.tagName !== 'OUTPUT').map(n => n.textContent).join(' ') : el.textContent; } else label = el.textContent;
      label = label.replace(/\s+/g, ' ').trim(); if (!label || label.length > 60 || /^[\d.,]+( [a-z%²³]+)?$/.test(label)) continue;
      const host = el.closest('button,.p,[data-tip]') || el, tip = (window.__tipFor(host) || host.dataset.tip || '').replace(/\s+/g, ' ').trim();
      const kind = el.tagName === 'SELECT' ? 'menu' : el.tagName === 'INPUT' ? 'box' : el.classList.contains('p') ? 'slider' : 'button';
      const k = label + '|' + kind; if (seen.has(k)) continue; seen.add(k); out.push({ label, tip, kind }); }
    return out; }, sel);
  const md = [];
  md.push('# Coyote Mountain topo · reference', '', 'Every task, tool and control in coyotemountainfarm.com/topo.html, with what each one does. Generated from the tool itself by `book/tools/make-reference.js`, so it matches the page. Run it again after the tool changes.', '', `Generated ${new Date().toISOString().slice(0, 10)}.`, '');
  md.push('## Around the drawing', '');
  const head = await read('#u2head button, #u2head summary, #u2head a.u2b');
  md.push('### Top bar', '', ...head.map(c => `- **${c.label}**${c.tip ? ': ' + c.tip : ''}`), '');
  const views = await read('#u2views button'); md.push('### Views', '', ...views.map(c => `- **${c.label}**${c.tip ? ': ' + c.tip : ''}`), '');
  await p.evaluate(() => { window.__ui2.state.view = '3d'; window.__ui2.applyView(); }); await p.waitForTimeout(500);
  const cam = await read('#views button'); md.push('### Camera (3D)', '', ...cam.map(c => `- **${c.label}**${c.tip ? ': ' + c.tip : ''}`), '');
  await p.evaluate(() => { window.__ui2.state.view = 'plan'; window.__ui2.applyView(); }); await p.waitForTimeout(300);
  const layers = new Map(); for (const v of ['plan', '3d']) { await p.evaluate(v => { window.__ui2.state.view = v; window.__ui2.applyView(); const L = document.getElementById('u2layers'); if (!L.classList.contains('show')) document.getElementById('u2layBtn').click(); }, v); await p.waitForTimeout(500); for (const c of await read('#u2layers button, #u2layers .p, #u2layers select')) layers.set(c.label, c); }
  await p.evaluate(() => { document.getElementById('u2layers').classList.remove('show'); window.__ui2.state.view = 'plan'; window.__ui2.applyView(); });
  md.push('### Layers & look', '', 'Opened with the layers & look button over the drawing. Some appear only in 3D or where the site has them.', '', ...[...layers.values()].map(c => `- **${c.label}**${c.tip ? ': ' + c.tip : ''}`), '');
  const status = await read('#u2status .p, #u2status select'); md.push('### Status bar', '', 'The place, cut and fill for the whole design, and units, always in sight.', '', ...status.map(c => `- **${c.label}**${c.tip ? ': ' + c.tip : ''}`), '');
  const learn = await p.evaluate(() => { const d = [...document.querySelectorAll('#u2head details')].find(x => /learn/.test(x.textContent)); d.open = true; return [...document.querySelectorAll('#u2learn button')].map(x => x.querySelector('span') ? x.querySelector('span').textContent : x.textContent); });
  md.push('### Learn', '', 'Short chapters on a sample site; your own project comes back after each. Some steps wait for you to do the thing.', '', ...learn.map(t => `- ${t}`), '');
  await p.evaluate(() => { document.querySelectorAll('#u2head details').forEach(d => d.open = false); });
  const T = await p.evaluate(() => window.__ui2.TASKS.map(t => ({ id: t.id, name: t.name, tools: t.tools.map(x => ({ id: x.id, name: x.name, note: x.note || '', group: x.group || '' })) })));
  for (const task of T) {
    const ttip = await p.evaluate(id => { window.__ui2.chooseTask(id); const b = [...document.querySelectorAll('#u2tasks button')].find(x => x.classList.contains('on')); return b ? b.dataset.tip || '' : ''; }, task.id);
    md.push(`## ${task.name}`, '', ttip ? ttip.charAt(0).toUpperCase() + ttip.slice(1) + '.' : '', '');
    let grp = '';
    for (const tool of task.tools) {
      if (tool.group && tool.group !== grp) { grp = tool.group; md.push(`*${grp}*`, ''); }
      const found = new Map(); let tip = '';
      for (const v of ['plan', '3d']) { await p.evaluate(([t, tl, v]) => { window.__ui2.chooseTask(t); window.__ui2.chooseTool(tl); window.__ui2.state.view = v; window.__ui2.applyView(); }, [task.id, tool.id, v]); await p.waitForTimeout(450);
        if (!tip) tip = await p.evaluate(() => { const b = document.querySelector('#u2tools button.on'); return b ? b.dataset.tip || '' : ''; });
        for (const c of await read('.u2panel button, .u2panel .p, .u2panel select, .u2panel input[aria-label]')) if (!found.has(c.label)) found.set(c.label, { ...c, only: v }); else if (found.get(c.label).only !== v) found.get(c.label).only = ''; }
      md.push(`### ${task.name} · ${tool.name}`, '');
      if (tip) md.push(tip.charAt(0).toUpperCase() + tip.slice(1) + '.', '');
      if (tool.note && tool.note !== tip) md.push(`*${tool.note}*`, '');
      const rows = [...found.values()].filter(c => c.label !== tool.name);
      if (rows.length) { md.push('| control | what it does |', '| --- | --- |'); for (const c of rows) md.push(`| ${c.label.replace(/\|/g, '/')}${c.kind !== 'button' ? ' (' + c.kind + ')' : ''}${c.only === '3d' ? ' · 3D' : ''} | ${(c.tip || '').replace(/\|/g, '/')} |`); md.push(''); }
    }
  }
  md.push('## Keys', '', '- **1 · 2 · 3**: plan, 3D, section', '- **/**: find a tool', '- **ctrl+z · ctrl+shift+z or ctrl+y**: undo, redo', '- **r**: rain in study · water', '- **0**: fit the drawing to the window', '');
  md.push('## Flight planner', '', 'coyotemountainfarm.com/flight.html plans drone survey flights for the ground models the topo tool reads. Its tasks:', '');
  await p.goto(base + '/flight.html'); await p.waitForTimeout(3000);
  const F = await p.evaluate(() => window.__ui2.TASKS.map(t => ({ id: t.id, name: t.name, tools: t.tools.map(x => ({ id: x.id, name: x.name, note: x.note || '' })) })));
  for (const task of F) { md.push(`### ${task.name}`, ''); for (const tool of task.tools) { await p.evaluate(([t, tl]) => { window.__ui2.chooseTask(t); window.__ui2.chooseTool(tl); }, [task.id, tool.id]); await p.waitForTimeout(350);
      const rows = await p.evaluate(() => [...document.querySelectorAll('.u2panel button, .u2panel .p, .u2panel select')].filter(el => el.getBoundingClientRect().width).map(el => { const lb = el.classList.contains('p') ? el.querySelector('label') : null; const label = (el.tagName === 'SELECT' ? (el.getAttribute('aria-label') || el.closest('.p') && '') : lb ? [...lb.childNodes].filter(n => n.tagName !== 'OUTPUT').map(n => n.textContent).join(' ') : el.textContent).replace(/\s+/g, ' ').trim(); const h = el.closest('[data-tip]'); return { label, tip: h ? h.dataset.tip.replace(/\s+/g, ' ') : '' }; }).filter(r => r.label && r.label.length < 60));
      const seen = new Set(); md.push(`- **${tool.name}**${tool.note ? ': ' + tool.note : ''}`); for (const r of rows) { if (seen.has(r.label) || r.label === tool.name) continue; seen.add(r.label); md.push(`  - ${r.label}${r.tip ? ': ' + r.tip : ''}`); } }
    md.push(''); }
  md.push('---', 'Coyote Mountain · free for learning and the commons · PolyForm Noncommercial 1.0.0', '');
  const out = path.join(__dirname, '..', 'reference.md'); fs.writeFileSync(out, md.filter((l, i, a) => !(l === '' && a[i - 1] === '')).join('\n')); console.log('wrote', out, md.length, 'lines');
  await b.close();
})();
