// 4 Oct: quick check shots of the stable with phase-1 solar and the electrical room (not part of the render set)
//   node checkshot.mjs   (viewer served on 8792)
import { createRequire } from 'module'; import path from 'path'; import { execSync } from 'child_process';
const require = createRequire(import.meta.url);
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), '@playwright/cli/node_modules/playwright-core'));
const b = await chromium.launch(); const page = await b.newPage({ viewport: { width: 1400, height: 800 } });
await page.goto('http://127.0.0.1:8792/index.html'); await page.waitForFunction(() => window.__shot && !document.getElementById('load'), null, { timeout: 90000 });
for (const [id, v] of [['check-solar-sw', { solar: true, orbit: { ti: 107.3, tj: 58.6, az: 150, el: 32, dist: 52, fov: 55 } }],
                       ['check-elecroom', { solar: true, orbit: { ti: 103.0, tj: 60.5, az: 125, el: 12, dist: 20, fov: 60 } }]]) {
  await page.evaluate(v => window.__shot({ fov: 70, hour: 15.5, ...v }), v); await page.waitForTimeout(1500);
  await page.screenshot({ path: `model/${id}.png` }); console.log(id);
}
await b.close();
