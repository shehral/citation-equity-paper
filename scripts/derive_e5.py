"""E5 results for the paper: data/e5_results.json from the tool repo's committed E5 aggregates.

E5 (CE/experiments/PLAN_E5.md r2, amendments 1 to 3; report CE/experiments/RESULTS_E5.md) asks whether the gain from the
reader's exact question holds on GEO-bench test queries E1 never used, and whether the same edit helps when it is made
from a guess: a keyword's two rarest key words (9K, 12K) or a question a local model wrote from that keyword (9L).

Reads, from CE/experiments/results/e5/ (aggregates only, written through CE/experiments/e5/sanitize_e5.py; no page text):
  e5_results.json   every planned and reported contrast (n, d, 95% and 90% CIs, p, Holm p, label) and the readings;
  analysis_e5.json  query counts, settings, the share of the gain each guess keeps, the length and key-term regression
                    of each planned test, the drift check and the amendment-3 sensitivity verdict;
  score_summary.json answer counts.
Records, per source file, the tool commit that last changed it and its sha256.

Rows are keyed "<set>:<arm>-<ref>:<scope>" (scope "pooled", "new queries", "all main queries", "same-sentence subset"),
plus the planned step. Labels are kept exactly as the analysis writes them.

Usage: .venv/bin/python -I -B scripts/derive_e5.py [--ce-root CE]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess

PAPER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REL = "experiments/results/e5"

# Version labels as RESULTS_E5.md words them (its "Short labels" list).
VERSION_NAMES = {
    "original": "the unedited page",
    "9": "the reader's exact question",
    "9P": "a section without the reader's words",
    "9K": "a keyword's two words",
    "9L": "a question a local model wrote from the keyword",
    "9A": "all the reader's key words, without the exact question",
    "9G": "a question in the page's own words",
    "12": "the reader's missing words worked into the top",
    "P12": "a rewording of the same spans (placebo for the reader's missing words)",
    "12K": "the keyword's missing words worked into the top",
    "P12K": "a rewording of the spans the keyword edit changed (placebo)",
}


def _load(ce_root: str, name: str):
    rel = f"{REL}/{name}"
    raw = open(os.path.join(ce_root, rel), "rb").read()
    commit = subprocess.run(["git", "log", "-1", "--format=%H", "--", rel], cwd=ce_root, capture_output=True,
                            text=True, check=True).stdout.strip()
    return json.loads(raw), {"source": "citation-equity/" + rel, "source_sha256": hashlib.sha256(raw).hexdigest(),
                             "ce_commit": commit}


def _key(c: dict) -> str:
    scope = c["scope"]
    if c["step"] == "amendment 3 sensitivity":
        scope = "amendment 3: " + scope
    return f"{c['set']}:{c['arm']}-{c['ref']}:{scope}"


def _share(blk: dict) -> dict:
    out = {}
    for g in ("9K", "9L"):
        s = blk[g]
        out[g] = {"n": s["n"], "share": s["share"], "ci90": s["ci90"], "estimable": s["estimable"],
                  "d_guess_minus_exact": {k: s["d_G_minus_9"][k] for k in ("n", "mean_d", "ci95", "ci90", "p")}}
    return {"strata": blk["strata"], "caveat": blk["caveat"], **out}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ce-root", default=os.environ.get("CE", "../citation-equity"))
    a = ap.parse_args()
    res, p_res = _load(a.ce_root, "e5_results.json")
    ana, p_ana = _load(a.ce_root, "analysis_e5.json")
    summ, p_sum = _load(a.ce_root, "score_summary.json")

    rows = {}
    for c in res["contrasts"]:
        k = _key(c)
        if k in rows:
            if rows[k]["step"] != c["step"]:  # the same contrast listed under two steps (12K vs original): keep both
                rows[k]["also_step"] = c["step"]
            continue
        rows[k] = {f: c[f] for f in ("contrast", "arm", "ref", "set", "step", "scope", "n", "d", "ci95", "ci90", "p",
                                     "p_holm", "label", "single_model", "cross_run", "mde")}

    m = ana["main"]
    planned = m["planned"]
    confound = {}
    for name, blk in (("gate", planned["gate"]), ("step5", planned["step5"]), ("arm12", planned["arm12"])):
        confound[name] = blk["confound"]["ci95"]
    for blk in planned["family"]:
        confound[f"{blk['arm']}-{blk['ref']}"] = blk["confound"]["ci95"]

    out = {
        "_provenance": {
            "producer": "scripts/derive_e5.py",
            "sources": [p_res, p_ana, p_sum],
            "plan": ana["plan"],
            "snapshot_started_at": ana["snapshot"]["started_at"],
            "note": "Aggregates of the planned E5 analysis (CE/experiments/PLAN_E5.md r2 with amendments 1 to 3; "
                    "freeze manifest CE/experiments/e5/freeze/MANIFEST.md); report CE/experiments/RESULTS_E5.md.",
        },
        "names": VERSION_NAMES,
        "settings": {k: ana["settings"][k] for k in ("alpha", "delta", "min_n", "margin", "judges")},
        "queries": {k: ana["queries"][k] for k in ("main", "new", "e1", "replication", "by_stratum")},
        "answers": {"answers": summ["answers"], "valid": summ["valid"], "prompts": summ["prompts"],
                    "dropped_cells": summ["dropped_cells"],
                    "answer_files": ana["snapshot"]["scoring"]["answer_files"]},
        "readings": res["readings"],
        "contrasts": rows,
        "share_kept_new": _share(m["share_kept_new"]),
        "share_kept_e1": _share(m["share_kept_e1"]),
        "confound_ci95": confound,
        "drift": {k: ana["drift"]["overall"][k] for k in ("n_queries", "n_cells", "mean", "ci95", "p")},
        "amendment_3_every_label_unchanged": ana["amendment_3_sensitivity"]["every_label_unchanged"],
        "gate_without_near_duplicates": {k: ana["added_analyses"]["gate_without_near_duplicates"][k]
                                         for k in ("n", "mean_d", "ci95", "p", "label")},
        # The gate's new-query estimate reweighted to E1's key-term-count mix (PLAN_E5 r2: the new queries are longer;
        # a planned secondary, reported without a verdict).
        "gate_reweighted_new": {k: planned["gate"]["reweighted_new"][k]
                                for k in ("n", "estimate", "ci95", "weights", "unweighted")},
        # How often the current tool counts the reader's question covered on a page with the tested question section
        # (arm 9): RESULTS_E5.md "Edits that passed validation", column "Tool: covers q".
        "tool_covers_q_arm9": {s: ana["validity"][s]["all"]["9"]["tool_flags"]["tool_covers_q"]
                               for s in ("main", "replication")},
    }
    path = os.path.join(PAPER, "data", "e5_results.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"data/e5_results.json: {len(rows)} contrasts; main {out['queries']['main']} queries "
          f"({out['queries']['new']} new), replication {out['queries']['replication']}")
    for k in ("main:9-original:new queries", "main:9K-original:pooled", "main:9L-original:pooled",
              "main:9K-9:pooled", "main:12K-P12K:pooled", "main:12-P12:new queries", "main:9-original:all main queries"):
        r = rows[k]
        print(f"  {k:<40} n {r['n']:>3}  d {r['d']:+.4f}  {r['label']}")


if __name__ == "__main__":
    main()
