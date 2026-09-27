// Money-shot control views of the Centro Equino drawing (26 Sep): the topo app, driven headless, sets each
// camera at golden hour under cumulus, then saves the painter's control image, its prompt and the aerial reference.
//   node shoot.mjs [outdir] [only-view-id]      (needs the local server: python -m http.server 8791 in coyote-studio)
import { createRequire } from 'module'; import fs from 'fs'; import path from 'path'; import { execSync } from 'child_process';
const require = createRequire(import.meta.url);
const root = execSync('npm root -g').toString().trim();
const { chromium } = require(path.join(root, '@playwright/cli/node_modules/playwright-core'));
const OUT = process.argv[2] || path.join(path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Z]:)/, '$1')), 'ctl');
const ONLY = process.argv[3];
fs.mkdirSync(OUT, { recursive: true });
const URL_ = 'http://127.0.0.1:8791/topo.html?proj=projects/centro-equino-2026-09-26-stalls16-nopad.json';

// grid directions on this site (rotation 318): east ≈ (+.74, +.67), north ≈ (+.67, -.74) in (i, j)
// orbit: the camera sits toward (sin yaw, cos yaw) from its target; walk: it looks along (sin yaw, cos yaw)
export const VIEWS = [   // all first-person cameras (walk), some flown up to drone height, so every shot has a real horizon and sky
  { id: '1-hero-sw', what: 'drone view from the south-west over the trough and the covered stalls toward the barn', walk: { i: 67, j: 66.7, h: 20 }, yaw: 1.67, pitch: 1.83 },
  { id: '2-corridor', what: 'eye level beyond the round trough looking up the covered corridor', walk: { i: 77.4, j: 65.8, h: 1.7 }, yaw: 1.716, pitch: 1.57 },
  { id: '3-site-ne', what: 'high drone view of the whole centre from the north-east into the sunset', walk: { i: 124, j: 53, h: 45 }, yaw: -1.52, pitch: 1.92 },
  { id: '4-hill-s', what: 'from the hillside to the south over the stalls toward the arena and the vineyard', walk: { i: 70, j: 81, h: 12 }, yaw: 2.41, pitch: 1.78 },
  { id: '5-corridor-out', what: 'eye level at the north-east end of the corridor looking down it to the trough and the sunset', walk: { i: 89.6, j: 64.2, h: 1.7 }, yaw: -1.436, pitch: 1.56 },
  { id: '7-plan', what: 'straight down over the whole site, north up, for the plan-view page', yaw: 0, pitch: 0, zoom: 2.1, target: [88, 56], persp: false },
  { id: '6-west', what: 'drone view from the west with the low sun behind the camera', walk: { i: 64.5, j: 46.5, h: 18 }, yaw: 0.838, pitch: 1.82 },
];

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
page.on('pageerror', e => console.log('page error:', e.message));
await page.goto(URL_);
await page.waitForFunction(() => window.__dbg && window.__dbg(o => o.S.strokes.length > 200 && o.S.world), null, { timeout: 60000 });
await page.evaluate(() => { try { localStorage.setItem('coyote-tour-topo', '1'); } catch (_) {} });
// the photo under the model, for the ground's colour and as the painter's second reference
await page.evaluate(() => window.__dbg(o => { o.S.aerial = true; o.S.aerialM = true; o.aerialUI && o.aerialUI(); }));
await page.waitForFunction(() => window.__dbg(o => { const a = o.aerialCache(); return !!(a && a.canvas); }), null, { timeout: 90000 }).catch(() => console.log('no aerial photo loaded'));

for (const v of VIEWS) {
  if (ONLY && v.id !== ONLY) continue;
  const res = await page.evaluate(v => window.__dbg(o => {
    const S = o.S; S.ve = 1; S.boundary = null; S.strokes = S.strokes.filter(st => st.color !== 'ember'); S.mode = 'model'; S.rendOn = true; S.rendSky = 'cumulus'; S.rendCut = 'none'; S.month = 9; S.hour = 17.6; S.sunMode = 'hour';
    o.AI.style = 'photo'; o.AI.engine = 'openai-2'; o.AI.photos = [];
    S.cam = { yaw: v.yaw, pitch: v.pitch, zoom: v.zoom || 1, pan: { x: 0, y: 0 }, persp: v.persp !== false };
    S.walk = v.walk ? { ...v.walk } : null;
    if (!v.walk && v.target) {                 // pan so the target sits at the picture's centre (a few passes: perspective)
      const zt = o.sample(o.z(), v.target[0], v.target[1]);
      for (let k = 0; k < 4; k++) { const p = o.camera(1536, 864).proj(v.target[0], v.target[1], zt); S.cam.pan.x += 768 - p[0]; S.cam.pan.y += 432 - p[1]; }
    }
    S.dirty = true; const c = o.aiControl(); return { png: c.png, prompt: c.prompt, ref: c.ref };
  }), v);
  fs.writeFileSync(path.join(OUT, `ctl-${v.id}.png`), Buffer.from(res.png, 'base64'));
  fs.writeFileSync(path.join(OUT, `prompt-${v.id}.txt`), res.prompt);
  res.ref.forEach((r, k) => fs.writeFileSync(path.join(OUT, `ref-${v.id}-${k + 1}.jpg`), Buffer.from(r, 'base64')));
  console.log(v.id, 'ok', res.ref.length, 'refs');
}
await browser.close();
