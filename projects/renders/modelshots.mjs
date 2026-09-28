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
  { id: '4-hill-s', i: 76, j: 76, h: 10, yaw: 2.41, pitch: 1.72 },
  { id: '5-corridor-out', i: 89.6, j: 64.2, h: 1.7, yaw: -1.436, pitch: 1.56 },
  { id: '6-west', i: 64.5, j: 46.5, h: 18, yaw: 0.838, pitch: 1.82 },
  { id: '7-plan', top: { i: 88, j: 56, w: 420 } },
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
  { id: 'b3-sw', white: true, block: true, orbit: { ti: 85, tj: 53, az: 140, el: 32, dist: 560 } },
  { id: 'b4-nw', white: true, block: true, orbit: { ti: 85, tj: 53, az: 230, el: 32, dist: 560 } },
  { id: 'b5-top', white: true, block: true, orbit: { ti: 85, tj: 53, az: 0, el: 90, dist: 500 } },
  { id: '15-stable-south', orbit: { ti: 107.3, tj: 58.6, az: 75, el: 24, dist: 48, fov: 55 } },
  { id: '16-stable-sw', orbit: { ti: 107.3, tj: 58.6, az: 140, el: 22, dist: 48, fov: 55 } },
  { id: '18-stable-west-elev', orbit: { ti: 107.3, tj: 58.6, az: 138, el: 6, dist: 36, fov: 50 } },
  { id: '19-spiral', orbit: { ti: 97.7, tj: 45.7, az: 180, el: 18, dist: 16, fov: 55 } },
  { id: '20-front-yard', orbit: { ti: 102.04, tj: 58.36, az: 176.8
, el: 30, dist: 40, fov: 55 } },
  { id: '21-bleachers-top', top: { i: 99.6, j: 45.2, w: 26 } },
  { id: '22-picnic', orbit: { ti: 99.77, tj: 42.65, az: 225, el: 18, dist: 14, fov: 55 } },
  { id: '23-picnic-side', orbit: { ti: 99.77, tj: 42.65, az: 190, el: 14, dist: 13, fov: 55 } },
  { id: '24-stable-east-roofless', noroof: true, orbit: { ti: 110.5, tj: 60.5, az: -60, el: 50, dist: 30, fov: 55 } },
  { id: '25-cover', orbit: { ti: 90, tj: 63, az: 185, el: 24, dist: 48, fov: 55 } },
  { id: '25b-cover', orbit: { ti: 92, tj: 62, az: 200, el: 26, dist: 58, fov: 55 } },
  { id: 'r1-plan-rain', water: true, top: { i: 88, j: 60, w: 420 } },
  { id: 'r2-sink-rain', water: true, orbit: { ti: 66, tj: 72, az: -70, el: 42, dist: 170 } },
  { id: 'r3-stable-rain', water: true, orbit: { ti: 104, tj: 62, az: 95, el: 48, dist: 150 } },
  { id: 'r4-top-rain', water: true, contours: true, orbit: { ti: 88, tj: 62, az: 0, el: 90, dist: 330 } },
  { id: 'b7-plan', white: true, block: true, top: { i: 85, j: 53, w: 400 } },
  { id: 'b6-low', white: true, block: true, orbit: { ti: 85, tj: 55, az: 115, el: 16, dist: 450 } },
];
const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
const page = await browser.newPage({ viewport: { width: 1536, height: 864 }, deviceScaleFactor: 1 });
page.on('pageerror', e => console.log('page error:', e.message));
await page.goto(URL_); await page.waitForFunction(() => window.__shot && !document.getElementById('load'), null, { timeout: 90000 });
await page.waitForTimeout(1500);                                                   // the photo texture
for (const v of VIEWS) {
  if (ONLY && !ONLY.split(',').includes(v.id)) continue;
  await page.evaluate(v => window.__shot({ fov: 70, hour: v.white ? 16.6 : 17.4, ...v }), v);
  await page.waitForTimeout(400);
  await page.locator('#view canvas').screenshot({ path: path.join(OUT, `model-${v.id}.png`) });
  console.log(v.id, 'ok');
}
await browser.close();
