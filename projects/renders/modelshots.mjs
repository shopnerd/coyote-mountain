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
];
const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
const page = await browser.newPage({ viewport: { width: 1536, height: 864 }, deviceScaleFactor: 1 });
page.on('pageerror', e => console.log('page error:', e.message));
await page.goto(URL_); await page.waitForFunction(() => window.__shot && !document.getElementById('load'), null, { timeout: 90000 });
await page.waitForTimeout(1500);                                                   // the photo texture
for (const v of VIEWS) {
  if (ONLY && v.id !== ONLY) continue;
  await page.evaluate(v => window.__shot({ ...v, fov: 70, hour: 17.4 }), v);
  await page.waitForTimeout(400);
  await page.locator('#view canvas').screenshot({ path: path.join(OUT, `model-${v.id}.png`) });
  console.log(v.id, 'ok');
}
await browser.close();
