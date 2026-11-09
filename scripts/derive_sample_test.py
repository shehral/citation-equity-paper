#!/usr/bin/env python3
"""Copy the example's recorded citation test (Section 4, Station 1) into results/samples/espresso_test.json.

Reads, from the tool repo (CE, read only), samples/espresso-bitterness/results/{before,after,comparison}.json: the two
BenchReports of the espresso example's before and after drafts (llama3.2:3b, 4 questions x 8 runs each) and their paired
comparison. Writes the settings, each report's summary and its per-run numbers (query, run, seed, retrieved, cited, share,
valid citations, format failure; no answer text, no page ids), and the comparison (deltas, sign-flip p values, n), with a
_provenance block (producer, CE commit, sha256 of each input). results/verify_numbers.py recomputes the cited counts, the
mean shares and the share's sign-flip p from the per-run rows and checks Section 4's numbers against them.

Usage: .venv/bin/python -I -B scripts/derive_sample_test.py [--ce-root <path to the tool repo>]
       (CE_ROOT in the environment also works; default ../citation-equity)
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import subprocess
from pathlib import Path

PAPER = Path(__file__).resolve().parent.parent
SAMPLE = "espresso-bitterness"
RUN_KEYS = ("queryId", "run", "seed", "draftRetrieved", "draftCited", "draftPawc", "validCitations", "formatFailure")
SUMMARY_KEYS = ("retrieved", "validRuns", "formatFailures", "citedAmongValid", "pawcAmongValid", "chanceShare")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ce-root", default=os.environ.get("CE_ROOT", str(PAPER.parent / "citation-equity")))
    args = ap.parse_args()
    ce = Path(args.ce_root).resolve()
    src = ce / "samples" / SAMPLE / "results"
    inputs = {name: src / f"{name}.json" for name in ("before", "after", "comparison")}
    for p in inputs.values():
        if not p.is_file():
            raise SystemExit(f"derive_sample_test: missing {p}")
    try:
        commit = subprocess.run(["git", "-C", str(ce), "rev-parse", "--short", "HEAD"], capture_output=True, text=True,
                                check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        commit = None

    reports = {name: json.loads(inputs[name].read_text(encoding="utf-8")) for name in ("before", "after")}
    comparison = json.loads(inputs["comparison"].read_text(encoding="utf-8"))
    settings = reports["before"]["settings"]
    if reports["after"]["settings"] != settings:
        raise SystemExit("derive_sample_test: the before and after reports have different settings")
    out = {
        "_provenance": {
            "producer": "scripts/derive_sample_test.py",
            "ce_commit": commit,
            "inputs": {f"samples/{SAMPLE}/results/{name}.json": sha256(p) for name, p in inputs.items()},
            "written": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "note": "Summaries and per-run numbers only; the answers (recording.json) and page ids are not copied.",
        },
        "sample": SAMPLE,
        "settings": settings,
        "drafts": {
            name: {
                "createdAt": r["createdAt"],
                "summary": {k: r["summary"][k] for k in SUMMARY_KEYS},
                "runs": [{k: run[k] for k in RUN_KEYS} for run in r["runs"]],
                "caveat": r["caveat"],
            }
            for name, r in reports.items()
        },
        "comparison": {k: comparison[k] for k in ("delta", "pValue", "nQueries", "excludedQueries", "caveat")},
    }
    dest = PAPER / "results" / "samples" / "espresso_test.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {dest.relative_to(PAPER)} (CE {commit}; {sum(len(d['runs']) for d in out['drafts'].values())} runs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
