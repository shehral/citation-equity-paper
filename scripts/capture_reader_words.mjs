// Figure 5 capture: the deployed draft view after the author follows the reader's-words tips on the espresso example.
// Modelled on scripts/capture_screens.mjs (Figure 2). Steps, all on the live site:
//   1. load the example (score 37), read the reader's-words tip in Start here ("Use the words of ...");
//   2. type the word it names into the title: "Why does my espresso taste bitter?" -> "..., and how do I fix it?";
//   3. read the next reader's-words tip and add one opening sentence with the words it and the last tip name;
//   4. check that no reader's-words tip is left, read the score and its "since you started" chip, screenshot.
// Writes data/screens/reader_words.png and data/fig5_callouts.json (callout anchors measured from the page, as
// fractions from the crop's top-left, never placed by hand; the UI strings read in the same run). It then reruns
// the engine of the tool repo on the sample draft before and after the same two edits (tsx, the four sample
// questions as questions and as the reader's questions, as the workspace does) and records each check's score,
// so the figure can say which check moved the score.
// Usage: node scripts/capture_reader_words.mjs   (Playwright resolved from the tool repo; CE, CE_URL override)
import { execFileSync } from 'node:child_process';
import { mkdtempSync, readFileSync, writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const PAPER = join(dirname(fileURLToPath(import.meta.url)), '..');
const CE = process.env.CE ?? '../citation-equity';
const { chromium } = createRequire(join(CE, 'apps/workspace/package.json'))('@playwright/test');
const BASE = process.env.CE_URL ?? 'https://shehral.github.io/citation-equity/';
const W = 1100; // the narrowest width that keeps the draft and the rail side by side
const H = 800;
const TITLE_ADD = ', and how do I fix it';
const OPENING = 'How long the shot runs and the water temperature are the first things to check. ';

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 2, colorScheme: 'light' });
await page.goto(BASE);
await page.evaluate(() => localStorage.clear());
await page.reload();
await page.getByRole('button', { name: 'Try it with an example' }).click();
await page.goto(`${BASE}draft/`);
const score = page.getByRole('img', { name: /^AI-ready score/ });
await score.waitFor();
await page.waitForTimeout(800);
const start = page.getByRole('region', { name: 'Start here' });
const tip = async () => {
  const card = start.getByRole('article').filter({ hasText: /^\s*\d*\s*Use the words of/ });
  return (await card.count()) ? (await card.first().innerText()).replace(/\s+/g, ' ').trim() : null;
};
const strings = { score_before: await score.getAttribute('aria-label'), tips: [] };
strings.tips.push(await tip());

// Edit 1: the word the first tip names, into the title (before its question mark).
const lines = page.locator('.cm-content .cm-line');
await lines.first().click();
await page.keyboard.press('End');
await page.keyboard.press('ArrowLeft');
await page.keyboard.type(TITLE_ADD);
await page.waitForTimeout(1200);
strings.tips.push(await tip());
// Edit 2: one opening sentence (the title, a blank line, then the first paragraph).
await page.keyboard.press('End');
await page.keyboard.press('ArrowRight');
await page.keyboard.press('ArrowRight');
await page.keyboard.type(OPENING);
await page.waitForTimeout(1500);
strings.tips.push(await tip());
if (strings.tips[2] !== null) throw new Error(`a reader's-words tip is left: ${strings.tips[2]}`);
strings.score_after = await score.getAttribute('aria-label');
strings.chip = (await page.getByText(/since you started/).first().innerText()).trim();
strings.title = (await lines.first().innerText()).replace(/^#\s*/, '');
strings.all_fixes = (await page.getByRole('region', { name: 'All fixes' }).innerText()).replace(/\s+/g, ' ').trim();
const draft = await page.evaluate(() => localStorage.getItem('ce:v1:draft:espresso-bitterness'));
const questions = JSON.parse(await page.evaluate(() => localStorage.getItem('ce:v1:questions:espresso-bitterness')))
  .map((q) => q.text);

// Quiet screen: no focus ring, no hover, rail and page at the top.
await page.evaluate(() => {
  window.scrollTo(0, 0);
  document.activeElement?.blur();
});
await page.mouse.move(0, H - 1);
await page.waitForTimeout(800);

// Crop: from just above the score card to just below the first Start-here card; the full content width.
const box = async (loc) => {
  const b = await loc.first().boundingBox();
  if (!b) throw new Error('element not found');
  return b;
};
const card = await box(score.locator('xpath=ancestor::section[1]'));
const first = await box(start.getByRole('article').first());
const sheet = await box(page.locator('.cm-editor'));
const banner = await box(page.getByText('This is an example post.'));
const x0 = Math.floor(Math.min(sheet.x, banner.x) - 6);
const CROP = { x: x0, y: Math.floor(card.y - 6), w: Math.ceil(card.x + card.width + 6) - x0, h: 0 };
CROP.h = Math.ceil(first.y + first.height + 4) - CROP.y;

// Text ranges inside the editor: the added title words and the added opening sentence.
const rangeBox = (needle) => page.evaluate((s) => {
  const walker = document.createTreeWalker(document.querySelector('.cm-content'), NodeFilter.SHOW_TEXT);
  for (let n = walker.nextNode(); n; n = walker.nextNode()) {
    const i = n.textContent.indexOf(s);
    if (i < 0) continue;
    const r = document.createRange();
    r.setStart(n, i);
    r.setEnd(n, i + s.length);
    const rects = [...r.getClientRects()];
    const a = rects[0];
    const z = rects[rects.length - 1];
    return { first: { x: a.left, y: a.top, w: a.width, h: a.height }, last: { x: z.right, y: z.top, h: z.height } };
  }
  return null;
}, needle);
const t = await rangeBox('fix it?');
const o = await rangeBox(OPENING.trim());
if (!t || !o) throw new Error('added text not found in the editor');
const chip = await box(page.getByText(/since you started/));
const frac = (x, y) => {
  const fx = (x - CROP.x) / CROP.w;
  const fy = (y - CROP.y) / CROP.h;
  if (fx < 0 || fx > 1 || fy < 0 || fy > 1) throw new Error(`callout outside the frame: ${fx}, ${fy}`);
  return [Number(fx.toFixed(4)), Number(fy.toFixed(4))];
};
// dx, dy (CSS px) move a marker off its target so it never hides it.
const xy = {
  1: frac(t.last.x + 16, t.last.y + t.last.h / 2),
  2: frac(o.first.x + 4, o.first.y - 12),
  3: frac(chip.x + chip.width + 14, chip.y + chip.height / 2),
};
await page.screenshot({ path: join(PAPER, 'data/screens/reader_words.png'), clip: { x: CROP.x, y: CROP.y, width: CROP.w, height: CROP.h } });
await browser.close();

// The engine on the same drafts: which checks moved?
const sample = readFileSync(join(CE, 'samples/espresso-bitterness/before.md'), 'utf8');
const edited = sample.replace('# Why does my espresso taste bitter?', `# Why does my espresso taste bitter${TITLE_ADD}?`)
  .replace('If you have ever pulled a shot', `${OPENING}If you have ever pulled a shot`);
if (edited.trim() !== draft.trim()) throw new Error('the browser draft differs from the sample plus the two edits');
const tmp = mkdtempSync(join(tmpdir(), 'ce-fig5-'));
writeFileSync(join(tmp, 'before.md'), sample);
writeFileSync(join(tmp, 'after.md'), edited);
writeFileSync(join(tmp, 'questions.json'), JSON.stringify(questions));
const probe = join(tmp, 'probe.mts');
writeFileSync(probe, `import { readFileSync } from 'node:fs';
const { analyze } = await import(${JSON.stringify(join(CE, 'packages/engine/src/index.ts'))});
const qs = JSON.parse(readFileSync(${JSON.stringify(join(tmp, 'questions.json'))}, 'utf8'));
const run = (f) => analyze(readFileSync(${JSON.stringify(tmp)} + '/' + f, 'utf8'), { questions: qs, authorQuestions: qs });
const [b, a] = [run('before.md'), run('after.md')];
const checks = {};
b.checks.forEach((c, i) => { checks[c.checkId] = [c.score, a.checks[i].score]; });
console.log(JSON.stringify({ standard: [b.scores.foundation, a.scores.foundation], evidence: [b.scores.evidence, a.scores.evidence], checks }));
`);
const engineOut = execFileSync('pnpm', ['--filter', '@citation-equity/bench', 'exec', 'tsx', '--conditions=@citation-equity/source', probe],
  { cwd: CE, encoding: 'utf8' }).trim().split('\n').pop();
const engine = JSON.parse(engineOut);
engine.changed = Object.entries(engine.checks).filter(([, [b, a]]) => b !== a).map(([id]) => id);
const commit = execFileSync('git', ['rev-parse', '--short', 'HEAD'], { cwd: CE, encoding: 'utf8' }).trim();

const named = `\u201c${strings.tips[0].match(/Add "([^"]+)"/)[1]}\u201d`;
const num = (label) => Number(label.match(/(\d+) out of 100/)[1]);
const co = {
  _provenance: {
    producer: 'scripts/capture_reader_words.mjs',
    note: 'strings read from the deployed build in the same run; xy anchors measured from element and text boxes; engine = the tool repo engine on the sample draft before and after the same two edits',
    ce_commit_for_engine: commit,
  },
  status: 'captured',
  screenshot: 'data/screens/reader_words.png',
  edits: { title_added: TITLE_ADD, opening_added: OPENING.trim() },
  callouts: [
    { n: 1, what: `The word the first tip named (${named}), typed into the title`, xy: xy[1] },
    { n: 2, what: 'A new opening sentence with the words of the other two questions', xy: xy[2] },
    { n: 3, what: `Score ${num(strings.score_before)} to ${num(strings.score_after)}; rerun on the same edits, the engine moves only the reader's-words check`,
      xy: xy[3] },
  ],
  captured: { url: `${BASE}draft/`, viewport: `${W}x${H} CSS px at 2x, light`, crop: CROP, strings, questions },
  engine,
};
writeFileSync(join(PAPER, 'data/fig5_callouts.json'), `${JSON.stringify(co, null, 2)}\n`);
console.log(JSON.stringify({ strings, engine, CROP }, null, 1));
