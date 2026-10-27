"""Read-only loaders for the Citation Equity paper's figures and derive scripts.

Two layers, so every figure can be rebuilt from this repo alone:
  * raw loaders read the tool repo (CE, default ../citation-equity next to this repo, or $CE_ROOT) and are used by
    the derive scripts (scripts/derive_*.py, scripts/dump_grades.mjs), which write small derived tables to data/;
  * data loaders read those tables from data/; figure scripts (fig_*.py) use only these.

Nothing here writes a file. Numbers are never typed here: thresholds are parsed from the harness source, grades come
from the engine registry dump, E1 design values from PREREG_E1.md through data/e1_design.json.
Each loader returns the paths it read, so a figure can stamp them (figstyle.save(inputs=...)).
"""
from __future__ import annotations

import csv
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
PAPER = os.path.dirname(HERE)
DATA = os.path.join(PAPER, "data")


CE_ROOT_DEFAULT = os.environ.get("CE_ROOT") or os.path.join(os.path.dirname(PAPER), "citation-equity")


def ce_root() -> str:
    root = CE_ROOT_DEFAULT
    if not os.path.isdir(os.path.join(root, "experiments")):
        raise SystemExit(f"figdata: tool repo not found at {root} (set CE_ROOT)")
    return os.path.abspath(root)


# ------------------------------------------------------------------------------------------- names (labels, not data)
# Sensitivity models in the order of RESULTS_sensitivity.md (smallest first). file = results file stem in CE.
MODELS = [
    {"id": "Qwen/Qwen3.5-9B", "file": "Qwen__Qwen3.5-9B", "label": "Qwen3.5-9B"},
    {"id": "google/gemma-4-12B-it", "file": "google__gemma-4-12B-it", "label": "Gemma-4-12B-it"},
    {"id": "Qwen/Qwen3.8-27B", "file": "Qwen__Qwen3.8-27B", "label": "Qwen3.8-27B"},
    {"id": "google/gemma-4-31B-it", "file": "google__gemma-4-31B-it", "label": "Gemma-4-31B-it"},
]
CONDITIONS = ["offtopic", "before", "after", "answer_first"]
# The two sample drafts (CE/samples/<key>/) and their short names in the paper.
SAMPLES = [("espresso-bitterness", "espresso"), ("rag-explained", "RAG")]

# The nine studies of CE/docs/evidence.md ("The studies", table rows at lines 80 to 88 at CE c908431), in that order, with short display labels.
# ids are the engine registry's source ids (packages/engine/src/evidence.ts WORKS); `key` is a word that must occur
# on every evidence.md line a cell of that study cites (checked by derive_loose_grades.py).
STUDIES = [
    {"id": "aggarwal-2024-geo", "label": "GEO", "key": "Aggarwal"},
    {"id": "puerto-2025-cseo-bench", "label": "C-SEO Bench", "key": "C-SEO"},
    {"id": "vishwakarma-2026-what-gets-cited", "label": "What Gets Cited", "key": "What Gets Cited"},
    {"id": "kim-2026-sageo-arena", "label": "SAGEO Arena", "key": "SAGEO"},
    {"id": "zhang-2026-citation-absorption", "label": "Zhang et al.", "key": "Zhang"},
    {"id": "wan-2024-conflictingqa", "label": "ConflictingQA", "key": "ConflictingQA"},
    {"id": "wu-2025-autogeo", "label": "AutoGEO", "key": "AutoGEO"},
    {"id": "yu-2026-geo-sfe", "label": "GEO-SFE", "key": "GEO-SFE"},
    {"id": "martinez-2026-survey", "label": "Martinez (survey)", "key": "Martinez"},
]
GRADES = ["strong", "moderate", "mixed", "untested"]


# ------------------------------------------------------------------------------------------- raw loaders (tool repo)
def sensitivity_raw(ce: str | None = None):
    """Per model: summary and per_question from CE/experiments/results/sensitivity/sensitivity_<file>.json.
    The answer rows (model output text) are never returned."""
    ce = ce or ce_root()
    out, paths = [], []
    for m in MODELS:
        p = os.path.join(ce, "experiments", "results", "sensitivity", f"sensitivity_{m['file']}.json")
        d = json.load(open(p, encoding="utf-8"))
        if d["summary"]["model"] != m["id"]:
            raise SystemExit(f"figdata: {p} holds {d['summary']['model']}, expected {m['id']}")
        out.append({**m, "path": p, "summary": d["summary"], "per_question": d["per_question"]})
        paths.append(p)
    return out, paths


def sensitivity(ce: str | None = None):
    """The sensitivity results as a list of per-model dicts (keys: id, file, label, name, path, summary,
    per_question), in MODELS order. Used by fig_headline.py."""
    rows, _ = sensitivity_raw(ce)
    return [{**r, "name": r["label"]} for r in rows]


def per_sample_mean(per_question: dict, cond: str, sample_key: str) -> float:
    """Mean of per_question[cond] over the questions of one sample (keys '<sample>/<qid>')."""
    vals = [v for k, v in per_question[cond].items() if k.split("/")[0] == sample_key and v is not None]
    if not vals:
        raise SystemExit(f"figdata: no {cond} values for {sample_key}")
    return sum(vals) / len(vals)


def harness_thresholds(ce: str | None = None):
    """The registered criteria as the harness applies them (CE/experiments/explorer/sensitivity.py), with line numbers."""
    ce = ce or ce_root()
    p = os.path.join(ce, "experiments", "explorer", "sensitivity.py")
    lines = open(p, encoding="utf-8").read().splitlines()
    found = {}
    pats = {
        "h1_offtopic_max": r'h1 = mean\["offtopic"\] <= ([0-9.]+)',
        "h2_min_gain": r'h2 = \(mean\["answer_first"\] - mean\["before"\] >= ([0-9.]+)\)',
        "h2_max_p": r'and p_af <= ([0-9.]+)',
        "usable_min_valid_rate": r'"usable_for_E2": valid_rate >= ([0-9.]+)',
    }
    for key, pat in pats.items():
        for i, line in enumerate(lines, 1):
            mt = re.search(pat, line)
            if mt:
                found[key] = {"value": float(mt.group(1)), "line": i, "text": line.strip()}
                break
        else:
            raise SystemExit(f"figdata: {key} not found in {p}")
    return found, [p]


def evidence_doc(ce: str | None = None):
    ce = ce or ce_root()
    p = os.path.join(ce, "docs", "evidence.md")
    return open(p, encoding="utf-8").read().splitlines(), p


def prereg_e1(ce: str | None = None):
    ce = ce or ce_root()
    p = os.path.join(ce, "experiments", "PREREG_E1.md")
    return open(p, encoding="utf-8").read().splitlines(), p


# ------------------------------------------------------------------------------------------- data loaders (this repo)
def data_path(name: str) -> str:
    p = os.path.join(DATA, name)
    if not os.path.exists(p):
        raise SystemExit(f"figdata: {p} missing; run the derive scripts (scripts/fig_all.py --derive)")
    return p


def data_json(name: str):
    p = data_path(name)
    return json.load(open(p, encoding="utf-8")), p


def scores_path() -> str:
    """data/scores.json, written by scripts/collect_scores.py (`ce analyze --json` on the sample drafts)."""
    return os.path.join(DATA, "scores.json")


def scores():
    return json.load(open(data_path("scores.json"), encoding="utf-8"))


def evidence_matrix():
    p = data_path("evidence_matrix.csv")
    with open(p, encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        r["source_line"] = int(r["source_line"])
    return rows, p


def grades():
    return data_json("grades.json")


def evidence_grades():
    """Strict (shipped) and looser-rule grades per check (data/evidence_grades_loose.json)."""
    return data_json("evidence_grades_loose.json")


def sensitivity_derived():
    return data_json("sensitivity_derived.json")


def e1_design():
    return data_json("e1_design.json")


def fig2_callouts():
    return data_json("fig2_callouts.json")
