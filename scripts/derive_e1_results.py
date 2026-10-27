"""E1, E2 and E3 results for the paper: data/e1_results.json from the tool repo's committed aggregates.

Reads CE/experiments/results/e1/analysis.json (the pre-registered analysis, aggregates only; RESULTS_E1.md is its
report) and keeps, per set and contrast: arm, reference, family, label, n, d, 95% and 90% CIs, Holm p, per-judge d,
and the confound-adjusted intercept. Also reads CE/experiments/results/e2/analysis_e2.json (RESULTS_E2.md: E2a's
planned and reported contrasts per set, E2b's editor check) and CE/experiments/results/e3/analysis_e3.json
(RESULTS_E3.md: the pooled 260-query contrasts for arms 2, 4, 5, 6, 7, 8 and 10). Records, per source file, the
tool commit and the file's sha256. No page text is read.

Usage: .venv/bin/python -I -B scripts/derive_e1_results.py [--ce-root CE]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess

PAPER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Arm -> the check or candidate it tests; names as in Figure 3 (scripts/figdata.py) for the tool's checks.
ARM_NAMES = {
    "1": "Standalone paragraphs", "2": "Question headings", "3": "Lists for enumerations",
    "4": "Tables for comparisons", "5": "Statistics", "6": "Attributed expert quotes", "7": "Cited sources",
    "8": "Direct answer first", "9": "Target questions answered", "10": "Explicit comparisons",
    "11": "Definition up top", "12": "Query words in title and lead", "13": "Shorter sections",
    "14": "Visible date", "ALL": "All tool fixes together",
}


def _load(ce_root, rel):
    raw = open(os.path.join(ce_root, rel), "rb").read()
    commit = subprocess.run(["git", "log", "-1", "--format=%H", "--", rel], cwd=ce_root, capture_output=True,
                            text=True, check=True).stdout.strip()
    return json.loads(raw), {"source": "citation-equity/" + rel, "source_sha256": hashlib.sha256(raw).hexdigest(),
                             "ce_commit": commit}


def _row(c):
    return {"arm": c["arm"], "ref": c["ref"], "label": c.get("label"), "n": c["n"], "d": c.get("mean_d"),
            "ci95": c.get("ci95"), "ci90": c.get("ci90"), "p": c.get("p"), "p_holm": c.get("p_holm")}


def derive_e2(ce_root):
    """E2a (heading markup vs the query's words; d = arm 9 minus 9W or 9P) and E2b (Qwen3.8-27B as editor)."""
    d, prov = _load(ce_root, "experiments/results/e2/analysis_e2.json")
    prov["note"] = "E2 aggregates (PLAN_E2.md, written before any E2 version or answer); report RESULTS_E2.md."
    out = {"_provenance": prov, "e2a": {}}
    for st in ("main", "replication"):
        s = d["e2a"][st]
        out["e2a"][st] = {"n_queries": s["n_queries"], "judges": s["judges"],
                          "planned": [_row(c) for c in s["planned"]], "reported": [_row(c) for c in s["reported"]]}
    b = d["e2b"]
    out["e2b"] = {"editor": b["editor"], "judges": b["judges"], "n_queries": b["n_queries"],
                  "contrasts": [_row(c) for c in b["contrasts"]], "reported": [_row(c) for c in b["reported"]]}
    return out


def derive_e3(ce_root):
    """E3: the pooled contrasts (E1's 80 queries plus 180 new) for the arms E1 could not judge."""
    d, prov = _load(ce_root, "experiments/results/e3/analysis_e3.json")
    prov["note"] = "E3 aggregates (PLAN_E3.md, written before any E3 version or answer); report RESULTS_E3.md."
    return {"_provenance": prov, "n_queries": d["n_queries"], "queries_by_part": d["queries_by_part"],
            "judges": d["judges"], "family": d["family"], "contrasts": [_row(c) for c in d["contrasts"]]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ce-root", default=os.environ.get("CE", "../citation-equity"))
    a = ap.parse_args()
    path = os.path.join(a.ce_root, "experiments", "results", "e1", "analysis.json")
    raw = open(path, "rb").read()
    d = json.loads(raw)
    commit = subprocess.run(["git", "log", "-1", "--format=%H", "--", "experiments/results/e1/analysis.json"],
                            cwd=a.ce_root, capture_output=True, text=True, check=True).stdout.strip()
    out = {"_provenance": {"producer": "scripts/derive_e1_results.py",
                           "source": "citation-equity/experiments/results/e1/analysis.json",
                           "source_sha256": hashlib.sha256(raw).hexdigest(), "ce_commit": commit,
                           "note": "Aggregates of the pre-registered E1 analysis (PREREG_E1.md, frozen at 7859b07)."},
           "names": ARM_NAMES}
    for st in ("main", "replication"):
        s = d[st]
        rows = []
        for c in s["contrasts"]:
            conf = c.get("confound") or {}
            rows.append({
                "arm": c["arm"], "ref": c["ref"], "family": c["family"], "label": c["label"], "n": c["n"],
                "d": c.get("mean_d"), "ci95": c.get("ci95"), "ci90": c.get("ci90"), "p": c.get("p"),
                "p_holm": c.get("p_holm"),
                "per_judge": {j: v["mean_d"] for j, v in (c.get("per_judge") or {}).items()},
                "adjusted_ci95": conf.get("ci95"),
            })
        out[st] = {"n_queries": s["n_queries"], "judges": s["judges"], "tags": s.get("tags"), "contrasts": rows}
    out["e2"] = derive_e2(a.ce_root)
    out["e3"] = derive_e3(a.ce_root)
    p = os.path.join(PAPER, "data", "e1_results.json")
    with open(p, "w") as f:
        json.dump(out, f, indent=2)
        f.write("\n")
    for st in ("main", "replication"):
        print(st, out[st]["n_queries"], [(r["arm"], r["ref"], r["n"], r["label"]) for r in out[st]["contrasts"]])
    print("e3", out["e3"]["n_queries"], [(r["arm"], r["ref"], r["n"], r["label"]) for r in out["e3"]["contrasts"]])
    print("e2a", [(st, r["arm"], r["ref"], r["n"], r["label"]) for st in ("main", "replication")
                  for r in out["e2"]["e2a"][st]["planned"]])


if __name__ == "__main__":
    main()
