"""Write data/coverage.json: "Questions covered" on the two sample drafts, before and after the suggestions.

Never writes data/scores.json. That file holds the checklist scores the paper cites (40 -> 69, 42 -> 68) with the
tool commit that made them (its ce_commit). The question-first tool has no score, and those numbers cannot be
reproduced through its v2 API (the old CLI fed heading questions to one check and page questions to the other; v2
measures one set), so an --out that resolves to scores.json is refused (CE spec 2026-11-03 section 14).

Runs the tool's own CLI from its TypeScript source, read only, the way the bench's `ce` script does (tsx with the
@citation-equity/source condition), so the counts belong to the recorded commit and never to an older dist/ build:
`ce analyze <CE_ROOT>/samples/<sample>/{before,after}.md --questions <file> --json`, with the sample pack's
questions (pack.json queries, in order) as the readers' questions. Records per draft questions.covered, the number
of questions measured (questions.rows), questions.from and the draft's SHA-256; per sample the questions and the
pack's SHA-256; and the engine version, the CLI's schemaVersion, the tool commit and whether its tree was clean.

Usage: .venv/bin/python -I -B scripts/collect_scores.py [--ce-root ../citation-equity] [--out data/coverage.json]
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figdata  # noqa: E402
import figstyle  # noqa: E402

SCHEMA = 2  # the `ce analyze --json` schemaVersion this script reads (questions, no scores)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ce-root", default=figdata.CE_ROOT_DEFAULT)
    ap.add_argument("--out", default=os.path.join(figdata.DATA, "coverage.json"))
    a = ap.parse_args()
    # samefile catches the case-insensitive spellings macOS accepts (data/SCORES.json) and hard links; realpath
    # covers an --out that does not exist yet.
    scores = figdata.scores_path()
    same = (os.path.exists(a.out) and os.path.exists(scores) and os.path.samefile(a.out, scores)) or \
        os.path.normcase(os.path.realpath(a.out)) == os.path.normcase(os.path.realpath(scores))
    if same:
        raise SystemExit("collect_scores: data/scores.json is never written (it records the pre-redesign checklist "
                         "scores the paper cites); write data/coverage.json")
    ce = os.path.abspath(a.ce_root)
    bench = os.path.join(ce, "packages", "bench")
    tsx = os.path.join(bench, "node_modules", ".bin", "tsx")
    if not os.path.exists(tsx):
        raise SystemExit(f"collect_scores: {tsx} missing (run pnpm install in the tool repo)")
    cli = [tsx, "--conditions=@citation-equity/source", os.path.join(bench, "src", "node", "cli.ts"), "analyze"]
    git = ["git", "-C", ce]
    commit = subprocess.run(git + ["rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    dirty = subprocess.run(git + ["status", "--porcelain"], capture_output=True, text=True, check=True).stdout.strip()
    rows = {}
    engine = None
    with tempfile.TemporaryDirectory() as tmp:
        for sample, short in figdata.SAMPLES:
            pack = os.path.join(ce, "samples", sample, "pack.json")
            with open(pack, encoding="utf-8") as fh:
                questions = [q["query"] for q in json.load(fh)["queries"]]
            qfile = os.path.join(tmp, f"{sample}.txt")
            with open(qfile, "w", encoding="utf-8") as fh:
                fh.write("\n".join(questions) + "\n")
            rows[sample] = {"label": short, "questions": questions, "pack": os.path.relpath(pack, ce),
                            "pack_sha256": figstyle.sha256(pack)}
            for cond in ("before", "after"):
                draft = os.path.join(ce, "samples", sample, f"{cond}.md")
                res = subprocess.run(cli + [draft, "--questions", qfile, "--json"], capture_output=True, text=True,
                                     cwd=ce)
                if res.returncode != 0:
                    raise SystemExit(f"collect_scores: ce analyze failed on {draft}:\n{res.stderr.strip()}")
                d = json.loads(res.stdout)
                if d.get("schemaVersion") != SCHEMA:
                    raise SystemExit(f"collect_scores: ce analyze --json schemaVersion {d.get('schemaVersion')}, "
                                     f"expected {SCHEMA}")
                engine = engine or d["engineVersion"]
                if d["engineVersion"] != engine:
                    raise SystemExit("collect_scores: engine version changed between runs")
                q = d["questions"]
                rows[sample][cond] = {"covered": q["covered"], "measured": len(q["rows"]), "from": q["from"],
                                      "draft": os.path.relpath(draft, ce), "draft_sha256": figstyle.sha256(draft)}
    out = {"source": "ce analyze <draft> --questions <the sample pack's questions> --json (from the bench's source)",
           "ce_commit": commit, "ce_tree_clean": not dirty, "engine_version": engine, "schema_version": SCHEMA,
           "samples": rows}
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(f"wrote {a.out}")
    for s, r in rows.items():
        b, f = r["before"], r["after"]
        print(f"  {s}: questions covered {b['covered']} of {b['measured']} -> {f['covered']} of {f['measured']}")


if __name__ == "__main__":
    main()
