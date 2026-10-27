"""Second-rater packet for Figure 3: build the blind rating sheet, score a filled sheet, self-test.

Figure 3 (scripts/fig_evidence.py) codes each (draft check, study) cell from data/evidence_matrix.csv (single rater).
This script supports a blind second rating of a sample of those cells.

Modes (stdlib only):
  make-sheet            write notes/second-rater/rating_sheet.csv: every cell the current coding marks non-empty plus
                        an equal number of empty cells drawn at random (seed SEED), shuffled. Columns: check, study,
                        study_link, where_to_look, rating (blank), note (blank). Refuses to overwrite without --force.
  score SHEET.csv       read a filled sheet, compare with data/evidence_matrix.csv, print percent agreement and Cohen's
                        kappa (full 10-category set and collapsed set), list disagreements, write
                        notes/second-rater/agreement.json (override with --out).
  self-test             fill the sheet from our own coding and confirm kappa = 1 (also checks that a deliberately
                        perturbed sheet scores below 1 and that blanks / bad labels are rejected). Writes nothing
                        in notes/.

Categories (the rater's labels -> how our coding maps onto them; see fig_evidence.py glyph() for the figure):
  controlled_gain   result gain, design controlled, directness direct          (filled dot)
  indirect_gain     any other result gain (observational, elicited, or near)   (half dot)
  gain_part         gain_part_null or gain_part_harm                           (dot in a ring)
  null              null                                                       (open ring)
  harm              harm (significant)                                         (cross)
  obs_negative      negative (observational difference in the harmful way)     (coral half dot)
  survey_support    survey_support                                             (filled diamond)
  survey_caution    survey_caution                                             (open diamond)
  background        background                                                 (dash)
  empty             no row in the matrix                                       (blank cell)
Collapsed set: positive = controlled_gain, indirect_gain, gain_part; null = null; negative = harm, obs_negative;
other = survey_support, survey_caution, background, empty (the user-facing "survey or background" class; empty is
folded in because the collapsed set has four classes).

Usage: python3 -I -B scripts/rater_agreement.py {make-sheet [--force] | score SHEET [--out F] | self-test}
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import random
import sys
import tempfile
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MATRIX = os.path.join(ROOT, "data", "evidence_matrix.csv")
OUTDIR = os.path.join(ROOT, "notes", "second-rater")
SHEET = os.path.join(OUTDIR, "rating_sheet.csv")
AGREEMENT = os.path.join(OUTDIR, "agreement.json")
SEED = 20261026   # fixed; used for the empty-cell draw and the shuffle (random.Random(SEED), in that order)

CATEGORIES = ["controlled_gain", "indirect_gain", "gain_part", "null", "harm", "obs_negative",
              "survey_support", "survey_caution", "background", "empty"]
COLLAPSE = {"controlled_gain": "positive", "indirect_gain": "positive", "gain_part": "positive",
            "null": "null", "harm": "negative", "obs_negative": "negative",
            "survey_support": "other", "survey_caution": "other", "background": "other", "empty": "other"}
COLLAPSED = ["positive", "null", "negative", "other"]

STUDIES = ["aggarwal-2024-geo", "puerto-2025-cseo-bench", "vishwakarma-2026-what-gets-cited", "kim-2026-sageo-arena",
           "zhang-2026-citation-absorption", "wan-2024-conflictingqa", "wu-2025-autogeo", "yu-2026-geo-sfe",
           "martinez-2026-survey"]
CHECKS = ["standalone-paragraphs", "question-headings", "lists", "statistics", "tables", "expert-quotes",
          "cited-sources", "direct-answer-lead", "question-coverage", "comparisons", "reader-words"]

# Neutral: one pointer per study, identical for every check (so it cannot reveal which cells are coded).
LINKS = {
    "aggarwal-2024-geo": "https://arxiv.org/abs/2311.09735",
    "puerto-2025-cseo-bench": "https://arxiv.org/abs/2506.11097",
    "vishwakarma-2026-what-gets-cited": "https://arxiv.org/abs/2605.25517",
    "kim-2026-sageo-arena": "https://arxiv.org/abs/2602.12187",
    "zhang-2026-citation-absorption": "https://arxiv.org/abs/2604.25707",
    "wan-2024-conflictingqa": "https://aclanthology.org/2024.acl-long.403/",
    "wu-2025-autogeo": "https://arxiv.org/abs/2510.11438",
    "yu-2026-geo-sfe": "https://arxiv.org/abs/2603.29979",
    "martinez-2026-survey": "https://arxiv.org/abs/2607.14035",
}
STUDY_WHERE = {
    "aggarwal-2024-geo": "Section 2.3 (the list of rewriting methods), Table 1 and the results text of Sections 4 and 5",
    "puerto-2025-cseo-bench": "Section 5 (the list of methods) and Section 6 (results, per-domain and per-engine tables)",
    "vishwakarma-2026-what-gets-cited": "Table 1 (the 18 tested factors), Table 2 (odds ratios per model; bold = significant) and Sections 3 and 4",
    "kim-2026-sageo-arena": "Sections 5.1 and 5.2 (stage-by-stage results, domain analysis), Figure 3 and its case studies",
    "zhang-2026-citation-absorption": "Section 8 (the feature tables: 8.1 structure, 8.2 content types, 8.3 semantic roles) and the hypothesis/claim-level sections",
    "wan-2024-conflictingqa": "Section 5 (counterfactual edits) and Figure 2",
    "wu-2025-autogeo": "The extracted preference rules (Table 9 and the rule lists in the appendix)",
    "yu-2026-geo-sfe": "Table IV (results) and the ablation of the restructuring components",
    "martinez-2026-survey": "Table 4 (levels of support), Table 5 (confidence ratings), and Sections 4 and 7",
}
# Neutral: what to look for, per check; identical for every study.
CHECK_TERMS = {
    "standalone-paragraphs": "paragraphs that make sense on their own; self-contained passages; chunking",
    "question-headings": "headings phrased as questions; Q&A or FAQ format",
    "lists": "bulleted or numbered lists",
    "statistics": "adding numbers or statistics",
    "tables": "tables as a page format",
    "expert-quotes": "adding quotations from experts or credible sources",
    "cited-sources": "adding citations or references to sources",
    "direct-answer-lead": "putting the answer or a summary at the start of the page",
    "question-coverage": "content that addresses the question the reader asked",
    "comparisons": "explicit comparisons with alternatives",
    "reader-words": "the query's own key words placed in the title, first heading or opening paragraph",
}


def where(check, study):
    return f"{STUDY_WHERE[study]}. Look for: {CHECK_TERMS[check]}."


# --------------------------------------------------------------------------------------------- coding -> category
def category_of(row):
    r = row["result"]
    if r == "gain":
        return "controlled_gain" if (row["design"] == "controlled" and row["directness"] == "direct") else "indirect_gain"
    if r in ("gain_part_null", "gain_part_harm"):
        return "gain_part"
    return {"null": "null", "harm": "harm", "negative": "obs_negative", "survey_support": "survey_support",
            "survey_caution": "survey_caution", "background": "background"}[r]


def load_coding(path=MATRIX):
    with open(path, encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    return {(r["check_id"], r["study_id"]): category_of(r) for r in rows}


def norm(label):
    return (label or "").strip().lower().replace("-", "_").replace(" ", "_")


# --------------------------------------------------------------------------------------------- statistics
def kappa(a, b, labels):
    n = len(a)
    if n == 0:
        return float("nan")
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[l] * cb[l] for l in labels) / (n * n)
    if pe >= 1.0:
        return 1.0 if po == 1.0 else float("nan")
    return (po - pe) / (1 - pe)


def metrics(a, b, labels):
    n = len(a)
    return {"n": n, "agree": sum(x == y for x, y in zip(a, b)),
            "percent_agreement": round(100 * sum(x == y for x, y in zip(a, b)) / n, 2) if n else None,
            "cohens_kappa": round(kappa(a, b, labels), 4) if n else None}


# --------------------------------------------------------------------------------------------- sheet
def make_sheet_rows(coding):
    coded = sorted(coding)
    empties = sorted((c, s) for c in CHECKS for s in STUDIES if (c, s) not in coding)
    rng = random.Random(SEED)
    drawn = rng.sample(empties, len(coded))
    cells = coded + drawn
    rng.shuffle(cells)
    return [{"check": c, "study": s, "study_link": LINKS[s], "where_to_look": where(c, s), "rating": "", "note": ""}
            for c, s in cells], len(coded), len(empties)


def write_sheet(rows, path):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["check", "study", "study_link", "where_to_look", "rating", "note"])
        w.writeheader()
        w.writerows(rows)


def read_sheet(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def score(sheet_path, out_path=AGREEMENT, quiet=False, write=True, coding_path=MATRIX):
    coding = load_coding(coding_path)
    rows = read_sheet(sheet_path)
    errs, seen = [], set()
    pairs = []
    for i, r in enumerate(rows, 2):
        key = (r["check"], r["study"])
        lab = norm(r["rating"])
        if key[0] not in CHECKS or key[1] not in STUDIES:
            errs.append(f"line {i}: unknown cell {key}")
        if key in seen:
            errs.append(f"line {i}: duplicate cell {key}")
        seen.add(key)
        if not lab:
            errs.append(f"line {i}: blank rating for {key}")
        elif lab not in CATEGORIES:
            errs.append(f"line {i}: rating {r['rating']!r} is not one of {CATEGORIES}")
        else:
            pairs.append((key, coding.get(key, "empty"), lab, r.get("note", "")))
    if errs:
        raise SystemExit("rater_agreement: " + "\n  ".join(["sheet problems:"] + errs))
    ours = [p[1] for p in pairs]
    theirs = [p[2] for p in pairs]
    full = metrics(ours, theirs, CATEGORIES)
    co, ct = [COLLAPSE[x] for x in ours], [COLLAPSE[x] for x in theirs]
    coll = metrics(co, ct, COLLAPSED)
    ne = [(o, t) for _, o, t, _ in pairs if o != "empty"]
    nonempty = metrics([o for o, _ in ne], [t for _, t in ne], CATEGORIES)
    # cell present vs absent (does the rater find any finding where we did?)
    present = metrics([o != "empty" for o in ours], [t != "empty" for t in theirs], [True, False])
    dis = [{"check": k[0], "study": k[1], "ours": o, "rater": t, "collapsed_ours": COLLAPSE[o],
            "collapsed_rater": COLLAPSE[t], "rater_note": n} for k, o, t, n in pairs if o != t]
    conf = {o: {t: sum(1 for _, oo, tt, _ in pairs if oo == o and tt == t) for t in CATEGORIES
                if any(oo == o and tt == t for _, oo, tt, _ in pairs)} for o in CATEGORIES
            if any(oo == o for _, oo, _, _ in pairs)}
    res = {"sheet": os.path.basename(sheet_path), "sheet_sha256": hashlib.sha256(open(sheet_path, "rb").read()).hexdigest(),
           "matrix_sha256": hashlib.sha256(open(coding_path, "rb").read()).hexdigest(), "seed": SEED,
           "n_cells": len(pairs), "full_set": full, "collapsed_set": coll, "coded_cells_only_full_set": nonempty,
           "cell_present_vs_empty": present, "disagreements": dis, "confusion_ours_to_rater": conf}
    if write:
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(res, fh, indent=2)
            fh.write("\n")
    if not quiet:
        print(f"cells rated: {len(pairs)}")
        for name, m in (("full 10-category set", full), ("collapsed (positive/null/negative/other)", coll),
                        ("full set, coded cells only", nonempty), ("cell present vs empty", present)):
            print(f"  {name:42s} agreement {m['percent_agreement']}% ({m['agree']}/{m['n']})  kappa {m['cohens_kappa']}")
        print(f"disagreements: {len(dis)}")
        for d in dis:
            print(f"  {d['check']:22s} {d['study']:34s} ours {d['ours']:15s} rater {d['rater']:15s} {d['rater_note'][:60]}")
        if write:
            print(f"wrote {out_path}")
    return res


# --------------------------------------------------------------------------------------------- self-test
def self_test():
    coding = load_coding()
    rows, n_coded, n_empty = make_sheet_rows(coding)
    assert len(rows) == 2 * n_coded, "sheet is not balanced"
    assert len({(r["check"], r["study"]) for r in rows}) == len(rows), "duplicate cells"
    assert sum((r["check"], r["study"]) in coding for r in rows) == n_coded
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "filled.csv")
        for r in rows:
            r["rating"] = coding.get((r["check"], r["study"]), "empty")
        write_sheet(rows, p)
        res = score(p, quiet=True, write=False)
        k1, k2 = res["full_set"]["cohens_kappa"], res["collapsed_set"]["cohens_kappa"]
        assert res["full_set"]["percent_agreement"] == 100.0 and k1 == 1.0 and k2 == 1.0, (k1, k2)
        # perturb 5 coded cells: kappa must drop below 1 and 5 disagreements must be listed
        flip = {"controlled_gain": "null", "indirect_gain": "controlled_gain", "gain_part": "null", "null": "harm",
                "harm": "null", "obs_negative": "null", "survey_support": "background", "survey_caution": "background",
                "background": "empty"}
        n = 0
        for r in rows:
            if r["rating"] in flip and n < 5:
                r["rating"] = flip[r["rating"]]
                n += 1
        write_sheet(rows, p)
        bad = score(p, quiet=True, write=False)
        assert bad["full_set"]["cohens_kappa"] < 1 and len(bad["disagreements"]) == 5
        # a blank rating must be rejected
        rows[0]["rating"] = ""
        write_sheet(rows, p)
        try:
            score(p, quiet=True, write=False)
        except SystemExit:
            pass
        else:
            raise AssertionError("blank rating accepted")
    print(f"self-test OK: {len(rows)} cells ({n_coded} coded + {n_coded} of {n_empty} empty), "
          f"self-coded sheet gives agreement 100%, kappa full {k1}, collapsed {k2}; "
          f"5 perturbed cells give kappa {bad['full_set']['cohens_kappa']} with 5 disagreements listed; blank rating rejected")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="mode", required=True)
    m = sub.add_parser("make-sheet")
    m.add_argument("--force", action="store_true")
    s = sub.add_parser("score")
    s.add_argument("sheet")
    s.add_argument("--out", default=AGREEMENT)
    sub.add_parser("self-test")
    a = ap.parse_args()
    if a.mode == "make-sheet":
        if os.path.exists(SHEET) and not a.force:
            raise SystemExit(f"{SHEET} exists; pass --force to overwrite (a filled sheet would be lost)")
        rows, nc, ne = make_sheet_rows(load_coding())
        os.makedirs(OUTDIR, exist_ok=True)
        write_sheet(rows, SHEET)
        print(f"wrote {SHEET}: {len(rows)} cells = {nc} coded + {nc} random empty of {ne} (seed {SEED})")
    elif a.mode == "score":
        score(a.sheet, a.out)
    else:
        self_test()


if __name__ == "__main__":
    main()
