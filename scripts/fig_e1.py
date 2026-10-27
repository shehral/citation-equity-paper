"""Figure 4: which single suggestions change citation (E1, with E3's pooled rows and E2a's two heading rows).

A forest plot of per-query differences in citation score (5 - r) / 4, arm minus its reference (a paraphrase placebo of
the same spans, or the original where the arm has no placebo, marked with a ring), averaged over 8 seeds and two
judges; mean and 95% bootstrap interval. Sources per row:
  - E1 (80 main-set queries; PREREG_E1.md): all fixes (vs placebo, vs original), target questions answered (arm 9),
    lists (3), standalone paragraphs (1, descriptive), query words in title (12), definition up top (11).
  - E3 pooled (260 queries, E1's 80 plus 180 new; PLAN_E3.md): question headings (2), statistics (5), attributed
    quotes (6), cited sources (7), direct answer first (8), comparisons (10), comparison tables (4, vs original).
  - E2a (PLAN_E2.md), indented under arm 9: arm 9 (query as a heading) minus 9W (the same text as plain text) and minus
    9P (a same-size heading without the query's words), on the main set, with the replication as a diamond.
Filled: at least 30 analyzable queries (a verdict); hollow: fewer (no verdict) or descriptive by design. The grey
band is the +-0.03 margin. Teal diamonds: the 60-query C-SEO Bench replication where that row ran (E1 or E2a; E3 has
no replication set). Labels to the right: n and verdict. Candidate arms 13 (descriptive) and 14 (n 7) are in
RESULTS_E1.md only.

Input: data/e1_results.json (scripts/derive_e1_results.py; its "e2" and "e3" blocks carry their own provenance).
Usage: .venv/bin/python -I -B scripts/fig_e1.py [--out figures] [--png <dir>]
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figstyle as fs  # noqa: E402

PAPER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N, C = fs.NEUTRAL, fs.CONCEPT
DELTA = 0.03  # PREREG_E1.md, Verdicts 4
# Row names are the check names of Figure 3 (the tool's names), not experiment-arm names; arm 9 is the target-questions
# check, done as a section headed by the question, and arm 12 is the reader's-words check.
SHORT_NAMES = {"12": "Your reader's words up top", "9": "Target questions answered"}
# (source, arm, reference); E2a rows are arm 9 minus its two variants.
ORDER = [("e1", "ALL", "P_ALL"), ("e1", "ALL", "original"), ("e1", "9", "original"), ("e2a", "9", "9W"),
         ("e2a", "9", "9P"), ("e3", "2", "P2"), ("e1", "3", "P3"), ("e3", "5", "P5"), ("e3", "6", "P6"),
         ("e3", "7", "P7"), ("e3", "8", "P8"), ("e3", "10", "P10"), ("e3", "4", "original"), ("e1", "1", "original"),
         ("e1", "12", "P12"), ("e1", "11", "original")]
E2A_NAMES = {"9W": "heading vs plain text", "9P": "heading vs no-words heading"}
SEPARATORS = (2, 5, 13, 14)  # above: arm 9 and E2a | the tool's checks | descriptive check | candidates
SHORT = {"helps, possibly through length or query-term overlap": "helps*", "no effect larger than δ": "no effect",
         "insufficient n": "too few", "descriptive": "descriptive", "inconclusive": "inconclusive", "helps": "helps"}


def main():
    args = fs.cli(__doc__)
    fs.apply()
    path = os.path.join(PAPER, "data", "e1_results.json")
    d = json.load(open(path))
    names = d["names"]
    main_rows = {("e1", r["arm"], r["ref"]): r for r in d["main"]["contrasts"]}
    main_rows.update({("e3", r["arm"], r["ref"]): r for r in d["e3"]["contrasts"]})
    main_rows.update({("e2a", r["arm"], r["ref"]): r for r in d["e2"]["e2a"]["main"]["planned"]})
    rep_rows = {("e1", r["arm"], r["ref"]): r for r in d["replication"]["contrasts"] if r["n"] > 0}
    rep_rows.update({("e2a", r["arm"], r["ref"]): r for r in d["e2"]["e2a"]["replication"]["planned"] if r["n"] > 0})
    keys = [k for k in ORDER if k in main_rows and main_rows[k]["n"] > 0]
    rows = [main_rows[k] for k in keys]

    H_IN = 0.44 + 0.142 * len(rows)
    fig = fs.plt.figure(figsize=(fs.COLUMN_IN, H_IN))
    ax = fig.add_axes([0.37, 0.30 / H_IN, 0.43, 1 - 0.44 / H_IN])
    yt = ax.get_yaxis_transform()  # x in axes fractions, y in data
    ys = list(range(len(rows)))[::-1]
    ax.axvspan(-DELTA, DELTA, color=fs.tint(N["ink_soft"], 0.88), zorder=0, lw=0)
    ax.axvline(0, color=N["ink_soft"], lw=fs.LW["ref"], zorder=1)
    for gap in SEPARATORS:
        if gap < len(rows):
            ax.axhline(ys[gap] + 0.5, color=N["rule"], lw=0.5, zorder=1)
    for y, k, r in zip(ys, keys, rows):
        verdict = r["n"] >= 30 and r["label"] != "descriptive"
        col = C["after"] if r["label"].startswith("helps") else (C["before"] if verdict else N["ink_soft"])
        lo, hi = r["ci95"]
        ax.plot([lo, hi], [y, y], color=col, lw=1.2, solid_capstyle="round", zorder=3)
        ax.scatter([r["d"]], [y], s=22, facecolor=col if verdict else "white", edgecolor=col, linewidths=1.0, zorder=4)
        rep = rep_rows.get(k)
        if rep:
            ax.plot(rep["ci95"], [y - 0.32] * 2, color=C["answer"], lw=0.7, zorder=3)
            ax.scatter([rep["d"]], [y - 0.32], marker="D", s=9, color=C["answer"], zorder=4, linewidths=0)
        if k[0] == "e2a":
            name, ring = E2A_NAMES[r["ref"]], ""
        elif r["arm"] == "ALL":
            name, ring = ("All fixes, vs placebo" if r["ref"] != "original" else "All fixes, vs original"), ""
        else:
            name = SHORT_NAMES.get(r["arm"], names[r["arm"]])
            ring = "°" if r["ref"] == "original" else ""
        ax.text(-0.03, y, name + ring, ha="right", va="center", fontsize=fs.FS["small"] - 0.6, color=N["ink"],
                transform=yt, clip_on=False)
        ax.text(1.03, y, f"{r['n']:>2}  {SHORT.get(r['label'], r['label'])}", ha="left", va="center",
                fontsize=fs.FS["small"] - 1.0, color=N["ink"] if verdict else N["ink_soft"], transform=yt, clip_on=False)
    ax.set_xlim(-0.065, 0.12)
    ax.set_ylim(-0.8, len(rows) - 0.4)
    ax.set_yticks([])
    ax.set_xticks([-0.03, 0.03, 0.09], minor=True)
    ax.set_xticks([-0.06, 0, 0.06, 0.12])
    ax.set_xticklabels(["−0.06", "0", "+0.06", "+0.12"],
                       fontsize=fs.FS["small"] - 1.0)
    ax.set_xlabel("citation score, arm minus reference", fontsize=fs.FS["small"] - 0.6, labelpad=2)
    fs.despine(ax, left=False)
    ax.text(1.03, len(rows) - 0.35, " n  verdict", ha="left", va="bottom", fontsize=fs.FS["small"] - 1.2,
            color=N["ink_soft"], transform=yt, clip_on=False)
    fs.save(fig, args, "fig4_e1", inputs=[path], script=__file__)


if __name__ == "__main__":
    main()
