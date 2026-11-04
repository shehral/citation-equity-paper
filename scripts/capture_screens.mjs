// Figure 2 capture: the question-first draft view of the workspace, on the espresso example after two typed edits.
// Steps (tool repo docs/superpowers/specs/2026-11-03-question-first-design.md (local feat branch only) section 14, Ruling Q1):
//   Try it with an example on the home, open /draft/ (it reads "Questions covered: 0 of 4"), type the two edits
//   (the title gains a second question; the first paragraph under "## Why espresso turns bitter" opens with a
//   direct answer), wait for exactly "Questions covered: 2 of 4" (any other count fails the run), press Show on
//   the first open line (it marks a passage in the draft), and scroll the rail so the heading and the Quick
//   edit's Preview are both in view (callout 2 is dropped when they cannot be).
// Writes data/screens/draft_view.png and data/fig2_callouts.json: the callout anchors (fractions from the image's
// top-left), measured from element boxes, never placed by hand; the UI strings, read from the page; and the
// hand-written fields (_provenance, capture_plan, each callout's `what`), all from this script.
// Usage: [CE_URL=<site>/] [CE=<tool repo>] node scripts/capture_screens.mjs [--explore]
//   CE_URL  the site, ending in a slash (default: the live site); CE  the tool repo Playwright is loaded from
//   (default: ../citation-equity next to this repo). Headless Chromium. Against the local Pages build, from the
//   tool repo (out/ is never touched):
//     pnpm --filter workspace build:pages
//     OUT_DIR=apps/workspace/.next/pages-e2e BASE_PATH=/citation-equity PORT=<p> node apps/workspace/scripts/serve-out.mjs
//     CE_URL=http://127.0.0.1:<p>/citation-equity/ node <paper>/scripts/capture_screens.mjs
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const PAPER = join(dirname(fileURLToPath(import.meta.url)), '..');
const CE = resolve(process.env.CE ?? join(PAPER, '..', 'citation-equity'));
const { chromium } = createRequire(join(CE, 'apps/workspace/package.json'))('@playwright/test');
const BASE = process.env.CE_URL ?? 'https://shehral.github.io/citation-equity/';
const W = 1440;
const H = 900;
const CROP = { x: 95, y: 0, w: 1250, h: 900 }; // the content column only, without the empty margins
const explore = process.argv.includes('--explore');
// A local URL is the Pages build of the tool checkout CE (header): its commit goes into the record.
const LOCAL = ['127.0.0.1', 'localhost'].includes(new URL(BASE).hostname);
const git = (...args) => execFileSync('git', ['-C', CE, ...args], { encoding: 'utf8' }).trim();

// The two typed edits (spec section 14): `type` goes in right after the first `after` in the draft.
const EDITS = [
  {
    where: 'the title line',
    after: '# Why does my espresso taste bitter',
    type: ', and how do I fix it',
  },
  {
    where: 'the start of the first paragraph under "## Why espresso turns bitter"',
    after: '## Why espresso turns bitter\n\n',
    type: 'Espresso tastes bitter when too much comes out of the coffee, and you fix it with a coarser grind or cooler water. ',
  },
];
const START = 'Questions covered: 0 of 4';
const TARGET = 'Questions covered: 2 of 4';
const CHIP = 'Helped in our test';
const PRIVACY = 'Stays in your browser';
// The card's line under the heading (spec section 7.3, row "Line"; apps/workspace/components/draft/questions-card.tsx).
const LINE = 'Each needs its key words up top and a section that answers it.';

// The draft editor's CodeMirror view, found from its content element as EditorView.findFromDOM does
// (the tool's e2e helpers read it the same way).
const draft = (page) => page.locator('.cm-content[aria-label="Draft text"]');
const editorState = (page) =>
  draft(page).evaluate((content) => {
    const view = content.cmTile?.root?.view;
    if (!view) throw new Error('no CodeMirror view on .cm-content');
    const { from, to } = view.state.selection.main;
    return { text: view.state.doc.toString(), from, to };
  });

/** Puts the cursor right after the only occurrence of `after`, then types `text` there. */
async function typeAfter(page, after, text) {
  await draft(page).evaluate((content, after) => {
    const view = content.cmTile?.root?.view;
    if (!view) throw new Error('no CodeMirror view on .cm-content');
    const doc = view.state.doc.toString();
    const at = doc.indexOf(after);
    if (at < 0 || doc.indexOf(after, at + 1) >= 0) throw new Error(`edit anchor not found once: ${JSON.stringify(after)}`);
    view.dispatch({ selection: { anchor: at + after.length } });
    view.focus();
  }, after);
  await page.keyboard.insertText(text);
}

/** `text` with `type` inserted after the first `after`, as typeAfter does it. */
const applied = (text, { after, type }) => {
  const at = text.indexOf(after) + after.length;
  return text.slice(0, at) + type + text.slice(at);
};

const browser = await chromium.launch({ headless: true });
try {
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 2, colorScheme: 'light' });
  await page.goto(BASE);
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  await page.getByRole('button', { name: 'Try it with an example' }).click();
  await page.goto(`${BASE}draft/`);
  const start = page.getByRole('region', { name: 'Start here' });
  const heading = start.getByRole('heading', { name: /^Questions covered: \d+ of \d+$/ });
  await start.getByRole('heading', { name: START, exact: true }).waitFor();

  // The two edits, typed into the draft; the text must then be the example with exactly these two insertions.
  const original = (await editorState(page)).text;
  const expected = EDITS.reduce(applied, original);
  for (const e of EDITS) await typeAfter(page, e.after, e.type);
  const edited = (await editorState(page)).text;
  if (edited !== expected) throw new Error('the typed edits did not give the expected draft');
  try {
    await start.getByRole('heading', { name: TARGET, exact: true }).waitFor({ timeout: 15000 });
  } catch {
    throw new Error(`expected "${TARGET}" after the two edits; the card reads "${await heading.first().innerText()}"`);
  }
  const card = start.getByRole('region', { name: TARGET, exact: true });
  await card.locator('p[aria-live]').filter({ hasText: /^$/ }).waitFor({ state: 'attached' }); // not "Updating"

  // Show on the first open line: the first Show of the first row not covered yet (its words line when words are
  // missing up top, else its answer line). It selects the passage in the draft and focuses the editor.
  const open = card.getByRole('article').filter({ hasText: 'Not covered yet' }).first();
  const show = open.getByRole('button', { name: /^Show where: / }).first();
  const showName = await show.getAttribute('aria-label');
  await show.click();
  let sel = await editorState(page);
  for (let i = 0; i < 50 && sel.from === sel.to; i++) {
    await page.waitForTimeout(100);
    sel = await editorState(page);
  }
  if (sel.from === sel.to) throw new Error('Show selected no passage');
  const passage = sel.text.slice(sel.from, sel.to);
  await page.waitForTimeout(500);

  // The page and every scroller back to the top (the passage marked by Show stays selected), then the rail
  // scrolled just enough for the Quick edit's Preview, if the Questions covered heading stays in view.
  await page.evaluate(() => {
    window.scrollTo(0, 0);
    for (const el of document.querySelectorAll('*')) if (el.scrollTop > 0) el.scrollTop = 0;
  });
  await page.mouse.move(0, H - 1);
  await page.evaluate(() => document.activeElement?.blur());
  await page.waitForTimeout(500);
  const rail = page.getByRole('complementary', { name: 'Questions and notes' });
  const preview = start.getByRole('region', { name: 'Quick edit' }).getByRole('button', { name: 'Preview' });
  const MARGIN = 16; // CSS px kept clear between a target and the edge of the visible rail
  const r = await rail.boundingBox();
  const visibleTop = Math.max(r.y, 0) + MARGIN;
  const visibleBottom = Math.min(r.y + r.height, H) - MARGIN;
  const h0 = await heading.boundingBox();
  const p0 = await preview.boundingBox();
  if (!h0 || !p0) throw new Error('Questions covered heading or Quick edit Preview not found');
  const need = Math.max(0, p0.y + p0.height - visibleBottom);
  if (need > 0 && h0.y - need >= visibleTop) {
    await rail.evaluate((el, need) => {
      el.scrollTop += need;
    }, need);
    await page.waitForTimeout(300);
  }
  // Re-measure after the scroll (it may be clamped, or another element may scroll): callout 1 needs the heading
  // inside the visible rail, and callout 2 is kept only when Preview is inside it too.
  const h1 = await heading.boundingBox();
  const p1 = await preview.boundingBox();
  if (!h1 || !p1) throw new Error('Questions covered heading or Quick edit Preview lost after the scroll');
  if (h1.y < visibleTop || h1.y + h1.height > visibleBottom) throw new Error('the Questions covered heading is outside the visible rail');
  const fits = p1.y >= visibleTop && p1.y + p1.height <= visibleBottom;

  // fx, fy pick a point on the element's box; dx, dy (CSS px) move the marker off it so it never hides it.
  const anchorBox = (b, fx, fy, dx = 0, dy = 0) => {
    const x = (b.x + b.width * fx + dx - CROP.x) / CROP.w;
    const y = (b.y + b.height * fy + dy - CROP.y) / CROP.h;
    if (x < 0 || x > 1 || y < 0 || y > 1) throw new Error(`callout outside the frame: ${x}, ${y}`);
    return [Number(x.toFixed(4)), Number(y.toFixed(4))];
  };
  const anchor = async (loc, ...at) => {
    const b = await loc.first().boundingBox();
    if (!b) throw new Error('callout target not found');
    return anchorBox(b, ...at);
  };
  // The passage Show marked: the union of the editor's drawn selection boxes.
  const marks = await page.locator('.cm-selectionBackground').evaluateAll((els) =>
    els
      .map((el) => el.getBoundingClientRect())
      .filter((b) => b.width > 0 && b.height > 0)
      .map(({ left, top, right, bottom }) => ({ left, top, right, bottom })),
  );
  if (marks.length === 0) throw new Error('no marked passage in the draft');
  const left = Math.min(...marks.map((m) => m.left));
  const right = Math.max(...marks.map((m) => m.right));
  const top = Math.min(...marks.map((m) => m.top));
  const bottom = Math.max(...marks.map((m) => m.bottom));
  const marked = { x: left, y: top, width: right - left, height: bottom - top };

  const cardChip = card.locator('[data-card-chips] [data-label-chip]');
  const privacy = page.getByRole('banner').getByText(PRIVACY, { exact: true });
  const strings = {
    heading: await heading.first().innerText(),
    line: await card.locator(':scope > p:not(.sr-only)').first().innerText(),
    chip: (await cardChip.allInnerTexts()).join(' | '),
    privacy: await privacy.first().innerText(),
  };
  if (strings.chip !== CHIP) throw new Error(`the card's chip reads "${strings.chip}", not "${CHIP}"`);
  if (strings.line !== LINE) throw new Error(`the card's line reads "${strings.line}", not "${LINE}"`);
  const xy = {
    1: await anchor(heading, 0, 0.5, -24, 0),
    2: fits ? await anchor(preview, 1, 0.5, 28, 0) : null,
    3: anchorBox(marked, 1, 0.5, 26, 0),
    4: await anchor(cardChip, 0.5, 0, 0, -16),
    5: await anchor(privacy, 0, 0.5, -46, 0),
  };
  // The tool commit (local URLs only) is read before the screenshot is written, so a git failure leaves the old
  // PNG and JSON together.
  const localBuild = LOCAL ? { ce_commit: git('rev-parse', 'HEAD'), ce_tree_clean: git('status', '--porcelain') === '' } : null;
  await page.screenshot({ path: join(PAPER, 'data/screens/draft_view.png'), clip: { x: CROP.x, y: CROP.y, width: CROP.w, height: CROP.h } });
  if (explore) console.log(JSON.stringify({ xy, strings, showName, passage, rail: r, heading: h1, preview: p1, need, fits, marked }, null, 1));

  const CALLOUTS = [
    { n: 1, what: 'Questions covered', ui_string: strings.line },
    { n: 2, what: 'The Quick edit: Preview first, Apply only inside the preview', ui_string: null },
    { n: 3, what: 'The passage marked by Show on the first open line', ui_string: null },
    { n: 4, what: "The card's label from our own tests", ui_string: strings.chip },
    { n: 5, what: 'Privacy chip', ui_string: strings.privacy },
  ];
  const co = {
    _provenance: {
      producer: 'scripts/capture_screens.mjs (Figure 2 per spec section 14 of the tool repo, docs/superpowers/specs/2026-11-03-question-first-design.md, local feat branch only); `what` and capture_plan are written in the script',
      note: 'ui_string values were read from the build in the same run (captured.strings); xy anchors are measured from element boxes in that run; captured.edits are the two typed edits and draft_sha256 hashes the draft after them; captured.local_build (local URLs only) is the tool commit the build was made from.',
    },
    status: 'captured',
    screenshot: 'data/screens/draft_view.png',
    capture_plan: `scripts/capture_screens.mjs (Playwright, headless Chromium, ${W}x${H} at 2x, light: Try it with an example, /draft/, the two typed edits of spec section 14 (title; first sentence under "## Why espresso turns bitter"), waits for exactly "${TARGET}", Show on the first open line, the rail scrolled so the heading and the Quick edit's Preview are both in view, against ${BASE})`,
    callouts: CALLOUTS.filter((c) => xy[c.n] !== null).map((c) => ({ ...c, xy: xy[c.n] })),
    captured: {
      url: `${BASE}draft/`,
      viewport: `${W}x${H} CSS px at 2x, light`,
      crop: CROP,
      edits: EDITS.map(({ where, type }) => ({ where, typed: type })),
      draft_sha256: createHash('sha256').update(edited).digest('hex'),
      show: { button: showName, passage },
      strings,
      ...(localBuild ? { local_build: localBuild } : {}),
      ...(xy[2] === null ? { dropped: [{ n: 2, why: 'the Quick edit Preview and the heading do not fit in the rail together' }] } : {}),
    },
  };
  writeFileSync(join(PAPER, 'data/fig2_callouts.json'), `${JSON.stringify(co, null, 2)}\n`);
  console.log(`${strings.heading}; ${co.callouts.length} callouts; wrote data/screens/draft_view.png and data/fig2_callouts.json`);
} finally {
  await browser.close();
}
