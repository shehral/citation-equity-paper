// Median wall time of the engine's analyze() per sample draft (warm, in Node), for data/system_checks.json.
// Run by scripts/system_checks.py through the tool repo's tsx: argv = <tool repo root>.
import { readFileSync } from 'node:fs';
import { join } from 'node:path';

const CE = process.argv[2];
const { analyze } = await import(join(CE, 'packages/engine/src/index.ts'));
const RUNS = 60;
const out: Record<string, { words: number; median_ms: number; runs: number }> = {};
for (const slug of ['espresso-bitterness', 'rag-explained']) {
  const text = readFileSync(join(CE, 'samples', slug, 'before.md'), 'utf8');
  for (let i = 0; i < 10; i++) analyze(text); // warm-up
  const times: number[] = [];
  for (let i = 0; i < RUNS; i++) {
    const t = performance.now();
    analyze(text);
    times.push(performance.now() - t);
  }
  times.sort((a, b) => a - b);
  out[slug] = { words: text.split(/\s+/).filter(Boolean).length, median_ms: Number(times[RUNS / 2].toFixed(2)), runs: RUNS };
}
console.log(JSON.stringify(out));
