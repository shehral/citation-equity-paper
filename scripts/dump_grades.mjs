#!/usr/bin/env node
// Dump the tool's evidence registry (grades, titles, sources per check and per readiness item, preset weights)
// to data/grades.json, so the paper's figures read the shipped grades instead of retyping them.
//
// Reads (never writes) the tool repo's built engine: <ce>/packages/engine/dist/index.js, which is built from
// packages/engine/src/evidence.ts (draft checks) and packages/engine/src/readiness.ts (site readiness).
// The script refuses to run if dist is older than either source file, so a stale build cannot leak in.
//
// Usage: node scripts/dump_grades.mjs [--ce <tool repo>] [--out <data dir>]
import { createHash } from 'node:crypto';
import { readFileSync, statSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join, relative, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const paper = resolve(here, '..');
const arg = (name, fallback) => {
  const i = process.argv.indexOf(name);
  return i > 0 ? resolve(process.argv[i + 1]) : fallback;
};
const ce = arg('--ce', process.env.CE_ROOT ? resolve(process.env.CE_ROOT) : resolve(paper, '..', 'citation-equity'));
const outDir = arg('--out', join(paper, 'data'));

const dist = join(ce, 'packages/engine/dist/index.js');
const srcs = ['packages/engine/src/evidence.ts', 'packages/engine/src/readiness.ts'].map((p) => join(ce, p));
for (const s of srcs) {
  if (statSync(s).mtimeMs > statSync(dist).mtimeMs) {
    console.error(`dump_grades: ${relative(ce, dist)} is older than ${relative(ce, s)}; rebuild the engine in the tool repo first`);
    process.exit(1);
  }
}
const sha = (p) => createHash('sha256').update(readFileSync(p)).digest('hex');

const m = await import(pathToFileURL(dist).href);
const checks = m.CHECK_DEFINITIONS.map((d) => ({
  id: d.id,
  title: d.title,
  in_foundation_design: d.inFoundationDesign,
  grade: m.EVIDENCE[d.id].grade,
  sources: m.EVIDENCE[d.id].sources.map((s) => s.id),
}));
if (checks.map((c) => c.id).join() !== m.CHECK_IDS.join()) throw new Error('CHECK_DEFINITIONS and CHECK_IDS disagree');
const readiness = m.READINESS_IDS.map((id) => ({
  id,
  title: m.READINESS_TITLES[id],
  grade: m.READINESS_EVIDENCE[id].grade,
}));

const out = {
  _provenance: {
    producer: 'scripts/dump_grades.mjs',
    note: 'Grades as shipped in the tool engine registry; regenerate after any change to evidence.ts or readiness.ts.',
    inputs: [dist, ...srcs].map((p) => ({ path: relative(ce, p), repo: 'citation-equity', sha256: sha(p) })),
  },
  checks,
  readiness,
  preset_weights: m.PRESET_WEIGHTS,
  grade_weights: m.GRADE_WEIGHTS,
};
mkdirSync(outDir, { recursive: true });
const path = join(outDir, 'grades.json');
writeFileSync(path, JSON.stringify(out, null, 2) + '\n');
console.log(`wrote ${path}`);
