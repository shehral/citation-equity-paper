// Figure 2 capture: the draft view of the deployed workspace with the espresso example loaded.
// Writes data/screens/draft_view.png and the callout anchors (fractions from the top-left) into
// data/fig2_callouts.json, measured from the page, never placed by hand.
// Usage: node scripts/capture_screens.mjs [--explore]   (Playwright resolved from the tool repo)
import { readFileSync, writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const PAPER = join(dirname(fileURLToPath(import.meta.url)), '..');
const CE = process.env.CE ?? '../citation-equity';
const { chromium } = createRequire(join(CE, 'apps/workspace/package.json'))('@playwright/test');
const BASE = process.env.CE_URL ?? 'https://shehral.github.io/citation-equity/';
const W = 1440;
const H = 900;
const CROP = { x: 95, y: 0, w: 1250, h: 900 }; // the content column only, without the empty margins
const explore = process.argv.includes('--explore');

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 2, colorScheme: 'light' });
await page.goto(BASE);
await page.evaluate(() => localStorage.clear());
await page.reload();
await page.getByRole('button', { name: 'Try it with an example' }).click();
await page.goto(`${BASE}draft/`);
await page.getByRole('img', { name: /^AI-ready score/ }).waitFor();
const start = page.getByRole('region', { name: 'Start here' });
// "Show me" on the second fix marks its passage in the draft (only the selected fix is marked).
await start.getByRole('article').nth(1).getByRole('button', { name: 'Show me' }).click();
await page.waitForTimeout(800);
// Back to the top of the rail and the page, so the score card is in view.
await page.evaluate(() => {
  window.scrollTo(0, 0);
  for (const el of document.querySelectorAll('*')) {
    const st = getComputedStyle(el);
    if (/(auto|scroll)/.test(st.overflowY) && el.scrollHeight > el.clientHeight && el.scrollTop > 0) el.scrollTop = 0;
  }
});
await page.mouse.move(0, H - 1);
await page.evaluate(() => document.activeElement?.blur());
await page.waitForTimeout(800);

// fx, fy pick a point on the element's box; dx, dy (CSS px) move the marker off it so it never hides it.
const anchor = async (loc, fx, fy, dx = 0, dy = 0) => {
  const b = await loc.first().boundingBox();
  if (!b) throw new Error('callout target not found');
  const x = (b.x + b.width * fx + dx - CROP.x) / CROP.w;
  const y = (b.y + b.height * fy + dy - CROP.y) / CROP.h;
  if (x < 0 || x > 1 || y < 0 || y > 1) throw new Error(`callout outside the frame: ${x}, ${y}`);
  return [Number(x.toFixed(4)), Number(y.toFixed(4))];
};
const marked = page.locator('.cm-content').getByText('Why does my espresso taste bitter?');
const xy = {
  1: await anchor(page.getByRole('img', { name: /^AI-ready score/ }), 0, 0.5, -24, 0),
  2: await anchor(start.getByRole('button', { name: 'Preview' }), 1, 0.5, 28, 0),
  3: await anchor(marked, 1, 0.5, 26, 0),
  4: await anchor(page.getByRole('region', { name: 'All fixes' }).getByText(/^(Helps|Not scored)$/), 0.5, 0, 0, -16),
  5: await anchor(page.getByText('Stays in your browser'), 0, 0.5, -46, 0),
};
const strings = {
  caption: await page.getByText('A writing checklist, not a forecast.').first().innerText(),
  chip: await page.getByText('Stays in your browser').first().innerText(),
  tag: await page.getByRole('region', { name: 'All fixes' }).getByText(/^(Helps|Not scored)$/).first().innerText(),
};
await page.screenshot({ path: join(PAPER, 'data/screens/draft_view.png'), clip: { x: CROP.x, y: CROP.y, width: CROP.w, height: CROP.h } });
if (explore) {
  const hdr = await page.locator('header').first().boundingBox();
  console.log(JSON.stringify({ xy, strings, header: hdr }, null, 1));
}

const cpath = join(PAPER, 'data/fig2_callouts.json');
const co = JSON.parse(readFileSync(cpath, 'utf8'));
co.status = 'captured';
co.captured = { url: `${BASE}draft/`, viewport: `${W}x${H} CSS px at 2x, light`, crop: CROP, strings };
for (const c of co.callouts) c.xy = xy[c.n];
writeFileSync(cpath, `${JSON.stringify(co, null, 2)}\n`);
await browser.close();
