"""Write data/evidence_grades_loose.json: each draft check's grade under the tool's strict rule and a looser rule.

Inputs (this repo, both checked against the tool repo):
  data/evidence_matrix.csv  one row per (check, study) cell, coded from CE/docs/evidence.md; `source_line` is the
                            evidence.md line the cell rests on (the study's bullet under that check's Sources)
  data/grades.json          the shipped grades and source lists (scripts/dump_grades.mjs, engine registry)

The coding (data/README.md has the conventions):
  result      gain | gain_part_null | gain_part_harm | null | harm | negative | survey_support | survey_caution |
              background
  design      controlled | observational | elicited | survey | background
  directness  direct (the practice the check looks for) | near (a nearby practice: CE/docs/evidence.md line 32) |
              none (mechanism, hypothesis, a different practice, or a survey judgement)
  sig         significant | partly | not_reported | na
  own_conclusion  yes when the null or negative is the study's own stated finding for that practice

Rules (the four grade definitions of CE/docs/evidence.md lines 20 to 25 are shared; only what counts as a null
or negative finding differs):
  tested       a cell with directness direct or near, other than a survey judgement or background
  strict       counts every null or negative: null, harm, negative, and the null or harm part of a gain_part_* cell,
               direct or near, significant or not (evidence.md lines 24 and 29)
  loose        counts only (a) a null or negative that is the study's own finding for the practice the check looks
               for (directness direct, own_conclusion yes), or (b) a significant harm on that practice;
               non-significant subgroups (gain_part_*) and nulls about a nearby practice do not count
  grade        untested if nothing is tested; else mixed if a counted null exists; else strong if two or more
               studies found a controlled, direct gain, one of them with real retrieval or live engines (live = yes);
               else moderate if at least one controlled gain (direct or near) exists; otherwise the script stops,
               because the rubric gives no grade and the coding needs a second look

The script fails if a strict grade differs from the shipped one, if a check's coded studies differ from the
registry's sources, or if a cited line is outside the check's section or does not name the study.

Usage: .venv/bin/python -I -B scripts/derive_loose_grades.py [--ce-root <CE>]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figdata  # noqa: E402
import figstyle  # noqa: E402

NEG_RESULTS = {"null", "harm", "negative", "gain_part_null", "gain_part_harm"}
GAIN_RESULTS = {"gain", "gain_part_null", "gain_part_harm"}
ALLOWED = {
    "result": {"gain", "gain_part_null", "gain_part_harm", "null", "harm", "negative", "survey_support",
               "survey_caution", "background"},
    "design": {"controlled", "observational", "elicited", "survey", "background"},
    "directness": {"direct", "near", "none"},
    "sig": {"significant", "partly", "not_reported", "na"},
    "own_conclusion": {"yes", "no", "na"},
    "live": {"yes", "no", "na"},
}


def tested(c):
    return c["directness"] in ("direct", "near") and c["result"] not in ("survey_support", "survey_caution", "background")


def counts_strict(c):
    return tested(c) and c["result"] in NEG_RESULTS


def counts_loose(c):
    if not tested(c) or c["directness"] != "direct":
        return False
    if c["result"] in ("null", "negative") and c["own_conclusion"] == "yes":
        return True
    return c["result"] == "harm" and c["sig"] == "significant"


def grade(cells, counts):
    if not any(tested(c) for c in cells):
        return "untested", "no study tests the check or a nearby practice"
    nulls = [c for c in cells if counts(c)]
    if nulls:
        return "mixed", "counted null or negative: " + ", ".join(c["study_id"] for c in nulls)
    direct_gain = [c for c in cells if c["result"] in GAIN_RESULTS and c["design"] == "controlled"
                   and c["directness"] == "direct"]
    if len({c["study_id"] for c in direct_gain}) >= 2 and any(c["live"] == "yes" for c in direct_gain):
        return "strong", "controlled direct gains: " + ", ".join(c["study_id"] for c in direct_gain)
    ctrl_gain = [c for c in cells if tested(c) and c["result"] in GAIN_RESULTS and c["design"] == "controlled"]
    if ctrl_gain:
        return "moderate", "controlled gains, none counted against: " + ", ".join(c["study_id"] for c in ctrl_gain)
    raise SystemExit(f"derive_loose_grades: no rubric grade fits {cells[0]['check_id']}; revisit the coding")


def section_of(lines):
    """Map each evidence.md line number to the check id of the '## Title (`id`)' section it sits in."""
    sec, out = None, {}
    for i, line in enumerate(lines, 1):
        m = re.match(r"^##\s+.*\(`([a-z-]+)`\)\s*$", line)
        if m:
            sec = m.group(1)
        elif line.startswith("## "):
            sec = None
        out[i] = sec
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ce-root", default=figdata.CE_ROOT_DEFAULT)
    ap.add_argument("--out", default=os.path.join(figdata.DATA, "evidence_grades_loose.json"))
    a = ap.parse_args()
    ce = os.path.abspath(a.ce_root)
    cells, mpath = figdata.evidence_matrix()
    reg, gpath = figdata.grades()
    lines, epath = figdata.evidence_doc(ce)
    sec = section_of(lines)
    key = {s["id"]: s["key"] for s in figdata.STUDIES}

    for c in cells:
        for f, allowed in ALLOWED.items():
            if c[f] not in allowed:
                raise SystemExit(f"derive_loose_grades: bad {f}={c[f]!r} in {c['check_id']}/{c['study_id']}")
        ln = c["source_line"]
        if sec.get(ln) != c["check_id"]:
            raise SystemExit(f"derive_loose_grades: line {ln} is not in the {c['check_id']} section of evidence.md")
        if key[c["study_id"]] not in lines[ln - 1]:
            raise SystemExit(f"derive_loose_grades: line {ln} does not name {c['study_id']} ({key[c['study_id']]!r})")

    out_checks, fails = [], []
    for chk in reg["checks"]:
        cs = [c for c in cells if c["check_id"] == chk["id"]]
        if sorted(c["study_id"] for c in cs) != sorted(chk["sources"]):
            raise SystemExit(f"derive_loose_grades: coded studies for {chk['id']} differ from the registry's sources")
        strict, why_s = grade(cs, counts_strict)
        loose, why_l = grade(cs, counts_loose)
        if strict != chk["grade"]:
            fails.append(f"{chk['id']}: strict rule gives {strict}, registry ships {chk['grade']}")
        out_checks.append({"id": chk["id"], "title": chk["title"], "in_foundation_design": chk["in_foundation_design"],
                           "shipped": chk["grade"], "strict": strict, "strict_reason": why_s,
                           "loose": loose, "loose_reason": why_l, "changed": strict != loose})
    if fails:
        raise SystemExit("derive_loose_grades: " + "; ".join(fails))

    def tally(field):
        return {g: sum(1 for c in out_checks if c[field] == g) for g in figdata.GRADES}

    out = {
        "_provenance": {
            "producer": "scripts/derive_loose_grades.py",
            "note": ("Strict = the tool's shipped rule (reproduced from the coded matrix and checked against the "
                     "registry). Loose = only a study's own null or negative finding for the practice, or a "
                     "significant harm, counts; non-significant subgroups and nulls about a nearby practice do not. "
                     "Single rater coding; see data/README.md."),
            "inputs": [{"path": os.path.relpath(mpath, figdata.PAPER), "repo": "citation-equity-paper",
                        "sha256": figstyle.sha256(mpath)},
                       {"path": os.path.relpath(gpath, figdata.PAPER), "repo": "citation-equity-paper",
                        "sha256": figstyle.sha256(gpath)},
                       {"path": os.path.relpath(epath, ce), "repo": "citation-equity", "sha256": figstyle.sha256(epath)}],
        },
        "checks": out_checks,
        "tally": {"strict": tally("strict"), "loose": tally("loose")},
        "readiness": reg["readiness"],
        "readiness_tally": {g: sum(1 for r in reg["readiness"] if r["grade"] == g) for g in figdata.GRADES},
    }
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
        fh.write("\n")
    print(f"wrote {a.out}")
    for c in out_checks:
        print(f"  {c['id']:22s} strict {c['strict']:9s} loose {c['loose']:9s} {'CHANGED' if c['changed'] else ''}")
    print(f"  tally strict {out['tally']['strict']}  loose {out['tally']['loose']}  readiness {out['readiness_tally']}")


if __name__ == "__main__":
    main()
