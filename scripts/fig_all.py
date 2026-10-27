"""Regenerate every figure of the paper (and, with --derive, the derived data tables first).

  .venv/bin/python -I -B scripts/fig_all.py              # palette check, then every scripts/fig_*.py
  .venv/bin/python -I -B scripts/fig_all.py --derive     # first rebuild data/ from the tool repo (read only):
                                                         #   dump_grades.mjs, collect_scores.py,
                                                         #   derive_sensitivity.py, derive_loose_grades.py,
                                                         #   derive_e1_design.py
  options: --png <dir> (previews), --ce-root <tool repo>, --check-repeat (rerun and require byte-identical PDFs)

Figure scripts are discovered (scripts/fig_*.py except this one), so a new figure joins the build by existing.
Each must accept --out and --png. A figure script never writes a number file; only the derive scripts write data/.
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PAPER = os.path.dirname(HERE)
PY = [sys.executable, "-I", "-B"]
DERIVE = [  # order matters: loose grades need grades.json
    ["node", os.path.join(HERE, "dump_grades.mjs")],
    PY + [os.path.join(HERE, "collect_scores.py")],
    PY + [os.path.join(HERE, "derive_sensitivity.py")],
    PY + [os.path.join(HERE, "derive_loose_grades.py")],
    PY + [os.path.join(HERE, "derive_e1_design.py")],
    PY + [os.path.join(HERE, "derive_e1_results.py")],
]


def run(cmd):
    print("$", " ".join(os.path.relpath(c, PAPER) if c.startswith(PAPER) else c for c in cmd), flush=True)
    subprocess.run(cmd, check=True, cwd=PAPER)


def digest(paths):
    return {p: hashlib.sha256(open(p, "rb").read()).hexdigest() for p in paths}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--derive", action="store_true")
    ap.add_argument("--png", default=None)
    ap.add_argument("--ce-root", default=None)
    ap.add_argument("--out", default=os.path.join(PAPER, "figures"))
    ap.add_argument("--check-repeat", action="store_true")
    a = ap.parse_args()
    env_ce = ["--ce-root", a.ce_root] if a.ce_root else []

    if a.derive:
        for cmd in DERIVE:
            if not os.path.exists(cmd[-1]):
                print(f"skip {os.path.relpath(cmd[-1], PAPER)} (missing)")
                continue
            run(cmd + (["--ce", a.ce_root] if a.ce_root and cmd[0] == "node" else env_ce if a.ce_root else []))

    run(PY + [os.path.join(HERE, "figstyle.py"), "--check-sty", os.path.join(PAPER, "smpreprint.sty")])
    scripts = sorted(p for p in glob.glob(os.path.join(HERE, "fig_*.py")) if os.path.basename(p) != "fig_all.py")
    extra = (["--png", a.png] if a.png else []) + env_ce
    for s in scripts:
        run(PY + [s, "--out", a.out] + extra)
    pdfs = sorted(glob.glob(os.path.join(a.out, "*.pdf")))
    if a.check_repeat:
        first = digest(pdfs)
        for s in scripts:
            subprocess.run(PY + [s, "--out", a.out] + env_ce, check=True, cwd=PAPER, capture_output=True)
        again = digest(pdfs)
        changed = [os.path.basename(p) for p in pdfs if first[p] != again[p]]
        if changed:
            raise SystemExit(f"fig_all: not byte-identical on rerun: {', '.join(changed)}")
        print(f"rerun byte-identical: {len(pdfs)} PDFs")
    print(f"{len(scripts)} figure scripts ran; figures: {', '.join(os.path.basename(p) for p in pdfs)}")


if __name__ == "__main__":
    main()
