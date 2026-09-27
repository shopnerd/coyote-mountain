// Phone check of the 3D viewer: iPhone-sized, touch; closed toolbar and the open sheet, plus any element wider than the screen.
import { createRequire } from 'module'; import path from 'path'; import { execSync } from 'child_process';
const require = createRequire(import.meta.url);
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), '@playwright/cli/node_modules/playwright-core'));
const out = process.argv[3] || '.';
const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
const page = await browser.newPage({ viewport: { width: 393, height: 852 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
await page.goto(process.argv[2]); await page.waitForFunction(() => !document.getElementById('load'), null, { timeout: 90000 }); await page.waitForTimeout(1200);
await page.screenshot({ path: path.join(out, 'phone-closed.png') });
await page.evaluate(() => document.getElementById('moreBtn').click()); await page.waitForTimeout(500);
const r = await page.evaluate(() => { const a = document.querySelector('aside'); return { w: innerWidth, aside: a.getBoundingClientRect().width, scrollW: a.scrollWidth,
  wide: [...a.querySelectorAll('*')].filter(e => e.getBoundingClientRect().right > innerWidth + 1 && !e.closest('#views,#show')).map(e => e.tagName + '.' + e.className).slice(0, 6) }; });
console.log(JSON.stringify(r));
await page.screenshot({ path: path.join(out, 'phone-open.png') });
await page.evaluate(() => { const a = document.querySelector('aside'); a.scrollTop = a.scrollHeight; }); await page.waitForTimeout(300);
await page.screenshot({ path: path.join(out, 'phone-open-bottom.png') });
await browser.close();
