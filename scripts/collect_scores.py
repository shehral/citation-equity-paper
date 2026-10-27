"""Write data/scores.json: the checklist (GEO) scores of the two sample drafts, before and after the suggestions.

Runs the tool's own CLI, read only: `node <CE_ROOT>/packages/bench/bin/ce.js analyze <draft>.md --json` on
<CE_ROOT>/samples/<sample>/{before,after}.md, with no --questions (the draft's own question headings are the targets,
as in CE/samples/README.md line 100, "The after drafts score much higher"). Records both presets, the engine version, the tool commit, whether its tree was
clean, and the SHA-256 of each draft, so a later rerun can be compared. The tool repo is never written to.

Usage: .venv/bin/python -I -B scripts/collect_scores.py [--ce-root ../citation-equity]
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figdata  # noqa: E402
import figstyle  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ce-root", default=figdata.CE_ROOT_DEFAULT)
    ap.add_argument("--out", default=figdata.scores_path())
    a = ap.parse_args()
    ce = os.path.abspath(a.ce_root)
    cli = os.path.join(ce, "packages", "bench", "bin", "ce.js")
    git = ["git", "-C", ce]
    commit = subprocess.run(git + ["rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    dirty = subprocess.run(git + ["status", "--porcelain"], capture_output=True, text=True, check=True).stdout.strip()
    rows = {}
    engine = None
    for sample, short in figdata.SAMPLES:
        rows[sample] = {"label": short}
        for cond in ("before", "after"):
            draft = os.path.join(ce, "samples", sample, f"{cond}.md")
            res = subprocess.run(["node", cli, "analyze", draft, "--json"], capture_output=True, text=True,
                                 check=True, cwd=ce)
            d = json.loads(res.stdout)
            engine = engine or d["engineVersion"]
            if d["engineVersion"] != engine:
                raise SystemExit("collect_scores: engine version changed between runs")
            rows[sample][cond] = {"foundation": d["scores"]["foundation"], "evidence": d["scores"]["evidence"],
                                  "word_count": d["wordCount"],
                                  "draft": os.path.relpath(draft, ce), "draft_sha256": figstyle.sha256(draft)}
    out = {"source": "ce analyze <draft> --json (no --questions)", "ce_commit": commit, "ce_tree_clean": not dirty,
           "engine_version": engine, "samples": rows}
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(f"wrote {a.out}")
    for s, r in rows.items():
        print(f"  {s}: foundation {r['before']['foundation']} -> {r['after']['foundation']}, "
              f"evidence {r['before']['evidence']} -> {r['after']['evidence']}")


if __name__ == "__main__":
    main()
