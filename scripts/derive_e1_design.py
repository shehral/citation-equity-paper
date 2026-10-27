"""Write data/e1_design.json: the design values the E1 placeholder frame (Figure 4b) draws, read from the plan.

E1 (the planned per-suggestion test) has NO results. This file holds design values only, each parsed from
CE/experiments/PREREG_E1.md with its line number and the exact text it was read from, so a figure can re-check the
quote against the plan (scripts/fig_e1_frame.py does). Nothing is typed by hand:
  * the equivalence margin delta (verdict 4, "no effect larger than delta");
  * the minimum detectable d at the two planned sizes (power paragraph);
  * the primary outcome's definition (first-citation rank score);
  * the arms of confirmatory families A and B and the ALL arm, with their names from the arms table;
  * whether the plan is frozen (line 3 still reads "frozen at commit `<hash>`" until the owner freezes it).

Usage: .venv/bin/python -I -B scripts/derive_e1_design.py [--ce-root <CE>]
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


def find(lines, pattern, what):
    for i, line in enumerate(lines, 1):
        m = re.search(pattern, line)
        if m:
            return i, line, m
    raise SystemExit(f"derive_e1_design: {what} not found in PREREG_E1.md")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ce-root", default=figdata.CE_ROOT_DEFAULT)
    ap.add_argument("--out", default=os.path.join(figdata.DATA, "e1_design.json"))
    a = ap.parse_args()
    lines, path = figdata.prereg_e1(os.path.abspath(a.ce_root))

    i_d, l_d, m_d = find(lines, r"with δ = ([0-9.]+) score units", "equivalence margin")
    i_m, l_m, m_m = find(lines, r"minimum detectable d is about ([0-9.]+) at n = (\d+) and about ([0-9.]+) at n = (\d+)",
                         "minimum detectable d")
    i_s, l_s, _ = find(lines, r"\*\*Citation score \(primary\):\*\* \(5 − r\) / 4", "primary outcome")
    i_a, l_a, m_a = find(lines, r"Arms (\d+)-(\d+) are the tool's checks\. They form confirmatory family A", "family A")
    i_b, l_b, m_b = find(lines, r"Arms (\d+), (\d+) and (\d+) are candidate checks\. They form confirmatory family B",
                         "family B")
    i_f, l_f, _ = find(lines, r"frozen at commit", "freeze status")
    frozen = "<hash>" not in l_f

    arms = {}
    for i, line in enumerate(lines, 1):
        m = re.match(r"^\|\s*(\d+|ALL)\s*([a-z-]*)\s*\|", line)
        if m:
            arms[m.group(1)] = {"name": (m.group(2) or "ALL"), "line": i}
    fam_a = [str(k) for k in range(int(m_a.group(1)), int(m_a.group(2)) + 1)]
    fam_b = [m_b.group(1), m_b.group(2), m_b.group(3)]
    for k in fam_a + fam_b + ["ALL"]:
        if k not in arms:
            raise SystemExit(f"derive_e1_design: arm {k} missing from the arms table")

    q = lambda i, line: {"line": i, "quote": line.strip()}  # noqa: E731
    out = {
        "_provenance": {
            "producer": "scripts/derive_e1_design.py",
            "note": "Design values only; E1 has no results. Each value carries its PREREG_E1.md line and quote.",
            "inputs": [{"path": os.path.relpath(path, os.path.abspath(a.ce_root)), "repo": "citation-equity",
                        "sha256": figstyle.sha256(path)}],
        },
        "results": None,
        "frozen": frozen,
        "freeze_status": q(i_f, l_f),
        "outcome": {"name": "first-citation rank score, (5 - r)/4", **q(i_s, l_s)},
        "delta": {"value": float(m_d.group(1)), "unit": "score units", **q(i_d, l_d)},
        "mde": {"values": [{"n": int(m_m.group(2)), "d": float(m_m.group(1))},
                           {"n": int(m_m.group(4)), "d": float(m_m.group(3))}], **q(i_m, l_m)},
        "family_a": {"arms": [{"arm": k, **arms[k]} for k in fam_a], **q(i_a, l_a)},
        "family_b": {"arms": [{"arm": k, **arms[k]} for k in fam_b], **q(i_b, l_b)},
        "all_arm": {"arm": "ALL", **arms["ALL"]},
    }
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"wrote {a.out}  (frozen: {frozen}; delta {out['delta']['value']}; MDE {out['mde']['values']})")


if __name__ == "__main__":
    main()
