// Money shots rendered straight from the 3D viewer (27 Sep, Will: "model render + light AI finish"): the same cameras as
// shoot.mjs, drawn by the viewer's own three.js scene with its materials and the golden-hour sun, 1536 x 864.
//   node modelshots.mjs <viewer url> [outdir] [only-view-id]      e.g. http://127.0.0.1:8792/index.html
import { createRequire } from 'module'; import fs from 'fs'; import path from 'path'; import { execSync } from 'child_process';
const require = createRequire(import.meta.url);
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), '@playwright/cli/node_modules/playwright-core'));
const URL_ = process.argv[2] || 'http://127.0.0.1:8792/index.html';
const OUT = process.argv[3] || 'model'; const ONLY = process.argv[4];
fs.mkdirSync(OUT, { recursive: true });
const HOUR = 17.4;
const VIEWS = [   // grid (i, j) and eye height in metres, yaw/pitch as in topo.html's walk camera (pitch pi/2 = level)
  { id: '1-hero-sw', i: 67, j: 66.7, h: 20, yaw: 1.67, pitch: 1.83 },
  { id: '2-corridor', i: 77.4, j: 65.8, h: 1.7, yaw: 1.716, pitch: 1.57 },
  { id: '3-site-ne', i: 124, j: 53, h: 45, yaw: -1.52, pitch: 1.92 },
  { id: 'p4-site-ne', i: 124, j: 53, h: 45, yaw: -1.52, pitch: 1.92 },   // 3 Oct: pack p4 slot (Walker's crop of 3-site-ne), run with SHOT_W=1376 SHOT_H=1203 SHOT_DSF=2
  { id: '4-hill-s', i: 76, j: 76, h: 10, yaw: 2.41, pitch: 1.72 },
  { id: '5-corridor-out', i: 89.6, j: 64.2, h: 1.7, yaw: -1.436, pitch: 1.56 },
  { id: '6-west', i: 64.5, j: 46.5, h: 18, yaw: 0.838, pitch: 1.82 },
  { id: '7-plan', top: { i: 88, j: 56, w: 420 } },
  { id: 'trough-opts', top: { i: 116, j: 58, w: 150 } },
  { id: 'wash-farrier', figures: true, orbit: { ti: 103.5, tj: 61.0, az: 122, el: 9, dist: 8.2, fov: 62 } },   // 4 Oct: the wash pad under the grape trellis, from the south-west   // 4 Oct: stable + parking, third-trough options
  { id: '8-stable', i: 112.5, j: 49, h: 9, yaw: -0.50, pitch: 1.72 },
  { id: '9-arrival', i: 128, j: 64.5, h: 2.2, yaw: -1.83, pitch: 1.6 },
  { id: '10-stable-aisle', i: 104.1, j: 57.56, h: 1.7, yaw: 1.26, pitch: 1.57 },
  { id: '11-arena', i: 89.4, j: 38.4, h: 3, yaw: 0.725, pitch: 1.6 },
  { id: '12-high-south', i: 95, j: 97, h: 55, yaw: 3.14, pitch: 1.97 },
  { id: '13-bleachers', i: 96.11, j: 39.25, h: 2.4, yaw: 0.648, pitch: 1.62 },
  { id: '14-bleachers-high', i: 99.4, j: 37.54, h: 9, yaw: 0.0, pitch: 1.9 },
  // white study model, floating on white (27 Sep): orbit views around the site centre
  { id: 'b1-ne', white: true, block: true, orbit: { ti: 85, tj: 53, az: -40, el: 32, dist: 560 } },
  { id: 'b2-se', white: true, block: true, orbit: { ti: 85, tj: 53, az: 50, el: 32, dist: 560 } },
  { id: 'b3-sw', white: true, block: true, water: true, orbit: { ti: 85, tj: 53, az: 140, el: 32, dist: 660 } },   // 3 Oct: more margin so OpenAI's letterbox crop keeps the whole block (Will: 'wish it wasn't cropped')   // 3 Oct: water in the sink (Will's note)
  { id: 'b4-nw', white: true, block: true, orbit: { ti: 85, tj: 53, az: 230, el: 32, dist: 560 } },
  { id: 'b5-top', white: true, block: true, orbit: { ti: 85, tj: 53, az: 0, el: 90, dist: 500 } },
  { id: '15-stable-south', orbit: { ti: 107.3, tj: 58.6, az: 75, el: 24, dist: 48, fov: 55 } },
  { id: '16-stable-sw', orbit: { ti: 107.3, tj: 58.6, az: 140, el: 22, dist: 48, fov: 55 } },
  { id: '18-stable-west-elev', orbit: { ti: 107.3, tj: 58.6, az: 138, el: 6, dist: 36, fov: 50 } },
  { id: 'p2-road', orbit: { ti: 107.3, tj: 58.6, az: 138, el: 6, dist: 36, fov: 50 } },   // 3 Oct: pack p2 #3 = Walker's crop of 18-stable-west-elev; run with SHOT_DSF=3.6, crop in p2crop
  { id: 'cafe-end', orbit: { ti: 101, tj: 43.8, az: 118, el: 16, dist: 26, fov: 55 } },   // 4 Oct: the double-sided café's road end (bar wall, stick face, trough)
  { id: '19-spiral', orbit: { ti: 97.7, tj: 45.7, az: 180, el: 18, dist: 16, fov: 55 } },
  { id: '20-front-yard', orbit: { ti: 102.04, tj: 58.36, az: 176.8
, el: 30, dist: 40, fov: 55 } },
  { id: '21-bleachers-top', top: { i: 99.6, j: 45.2, w: 26 } },
  { id: '22-picnic', orbit: { ti: 99.77, tj: 42.65, az: 225, el: 18, dist: 14, fov: 55 } },
  { id: '23-picnic-side', orbit: { ti: 99.77, tj: 42.65, az: 190, el: 14, dist: 13, fov: 55 } },
  { id: '24-stable-east-roofless', noroof: true, orbit: { ti: 110.5, tj: 60.5, az: -60, el: 50, dist: 30, fov: 55 } },
  { id: '25-cover', orbit: { ti: 90, tj: 63, az: 185, el: 24, dist: 48, fov: 55 } },
  { id: '25b-cover', orbit: { ti: 92, tj: 62, az: 200, el: 26, dist: 58, fov: 55 } },
  { id: 'el-south', i: 103.423, j: 70.729, h: 1.70, yaw: 2.8302, pitch: 1.5708, fov: 58 },
  { id: 'el-west', i: 94.565, j: 54.520, h: 3.25, yaw: 1.2594, pitch: 1.5708, fov: 48 },
  { id: 'el-west-horse', i: 94.565, j: 54.520, h: 3.25, yaw: 1.2594, pitch: 1.5708, fov: 48 },   // 4 Oct: same camera as el-west, for fans
  { id: 'el-north', i: 110.658, j: 48.249, h: 4.66, yaw: -0.3114, pitch: 1.5708, fov: 58 },
  { id: 'el-south-wash', i: 102.131, j: 67.332, h: 1.70, yaw: 2.8302, pitch: 1.5708, fov: 45 },   // 3 Oct: square to the south wall, centred on the wash door, pad and trough, 66 ft out (the fence is at ~90)
  { id: 'el-east', i: 115.316, j: 61.199, h: 1.70, yaw: -1.8822, pitch: 1.5708, fov: 58 },
  { id: 'r1-plan-rain', water: true, top: { i: 88, j: 60, w: 420 } },
  { id: 'r2-sink-rain', water: true, orbit: { ti: 66, tj: 72, az: -70, el: 42, dist: 170 } },
  { id: 'r3-stable-rain', water: true, orbit: { ti: 104, tj: 62, az: 95, el: 48, dist: 150 } },
  { id: 'r4-top-rain', water: true, contours: true, orbit: { ti: 88, tj: 62, az: 0, el: 90, dist: 330 } },
  { id: 'b7-plan', white: true, block: true, top: { i: 85, j: 53, w: 470 } },   // 3 Oct: wider so the whole block fits (Will: a perfect rectangular plan view)
  { id: 'b6-low', white: true, block: true, orbit: { ti: 85, tj: 55, az: 115, el: 16, dist: 450 } },
];
if (process.env.FAN_FILE) VIEWS.push(...JSON.parse(fs.readFileSync(process.env.FAN_FILE, 'utf8')));   // 4 Oct: camera fans (fan.py)
const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
const page = await browser.newPage({ viewport: { width: +(process.env.SHOT_W || 1536), height: +(process.env.SHOT_H || 864) }, deviceScaleFactor: +(process.env.SHOT_DSF || 1) });
page.on('pageerror', e => console.log('page error:', e.message));
await page.goto(URL_); await page.waitForFunction(() => window.__shot && !document.getElementById('load'), null, { timeout: 90000 });
await page.waitForTimeout(1500);                                                   // the photo texture
for (const v of VIEWS) {
  if (ONLY && !ONLY.split(',').includes(v.id)) continue;
  // 4 Oct: the shot and the in-frame list in ONE evaluate: the viewer's loop moves the camera object afterwards (the picture is already drawn)
  const vis = await page.evaluate(async v => { await window.__shot({ fov: 70, hour: v.white ? 16.6 : 17.4, ...v }); const c = window.__cam, out = {}; if (!c || !window.__boxes) return out; c.updateMatrixWorld(); const V3 = c.position.constructor;
    for (const [n, b] of Object.entries(window.__boxes)) { let x0 = 9, x1 = -9, y0 = 9, y1 = -9, front = 0;
      for (const xx of [b.min.x, b.max.x]) for (const yy of [b.min.y, b.max.y]) for (const zz of [b.min.z, b.max.z]) { const p = new V3(xx, yy, zz).project(c); if (p.z < 1 && p.z > -1) { front++; x0 = Math.min(x0, p.x); x1 = Math.max(x1, p.x); y0 = Math.min(y0, p.y); y1 = Math.max(y1, p.y); } }
      if (!front) continue; const w = Math.max(0, Math.min(1, x1) - Math.max(-1, x0)), h = Math.max(0, Math.min(1, y1) - Math.max(-1, y0)); const a = w * h / 4; if (a > .0015) out[n] = +a.toFixed(4); }
    return out; }, v);
  // 4 Oct (Will: backgrounds invented): which objects are actually in this frame, and how big, for the painter's brief
  fs.writeFileSync(path.join(OUT, `model-${v.id}.vis.json`), JSON.stringify(vis));
  await page.waitForTimeout(400);
  await page.locator('#view canvas').screenshot({ path: path.join(OUT, `model-${v.id}.png`) });
  console.log(v.id, 'ok');
}
await browser.close();
