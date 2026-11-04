"""Figure 1: what moved citation. A two-panel forest plot at the text width (the page-1 teaser).

Every row is a per-query difference in citation score (5 - r) / 4, edit minus its reference (a same-length paraphrase
of the same spans, or the unedited page where marked with a ring, or the edit the row names), averaged over 8 seeds and
two judges, then over queries; mean and 95% bootstrap interval. Filled: at least 30 queries and a planned reading
(indigo helps, slate no effect or inconclusive, black the retention reading); hollow: no verdict (too few queries,
descriptive by design, or reported without a verdict). The grey band is the +-0.03 margin.
Teal diamonds: the 60-query C-SEO Bench replication set, where the row ran there. Labels to the right: n and result.

(a) The eleven checks, one change at a time, plus all fixes together and two rows that test whether the question
    section gains from its heading or its words (heading vs the same text as plain text; heading vs a same-size section
    without the question's words, 9P).
    Source: data/e1_results.json ("main", "replication", "e2", "e3"; scripts/derive_e1_results.py): E1's 80 GEO-bench
    queries, E3's pooled 260 for the checks E1 could not judge, E2a's two rows under the question section.
(b) E5: the reader's exact question on 180 GEO-bench test queries E1 never used, and the same section made from a
    guess, over all 260 main queries (E1's 80 included): a keyword's two rarest key words, or a question a local model
    wrote from that keyword. Every answer is judged against the reader's true question. Source: data/e5_results.json
    (scripts/derive_e5.py). The two bottom rows are differences between edits, the guess minus the exact question
    ("9K vs 9" as is, "9 vs 9A" sign flipped), so that the reading attaches to the guess: a negative value means the
    exact question did better. The first carries the planned retention reading, which the plan calls "loses the gain"
    and the figure and paper call "falls short" (of the exact question): d(exact - guess) with its 95% CI above 0
    (PLAN_E5.md r2, Primary analysis item 3).

Row names are the tool's check names (Figure 3, the engine registry), never experiment arm numbers.
Usage: .venv/bin/python -I -B scripts/fig_result.py [--out figures] [--png <dir>]
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figstyle as fs  # noqa: E402

PAPER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N, C = fs.NEUTRAL, fs.CONCEPT
DELTA = 0.03  # PREREG_E1.md, Verdicts 4; PLAN_E5.md reuses it (checked against data/e5_results.json settings.delta)
WIDTH_IN = 7.0  # acmart sigconf \textwidth: a teaser figure spans both columns
ROW_IN = 0.125
XLIM = (-0.065, 0.12)
AX_W = 0.18  # each panel's plot width, figure fraction
AX_A, AX_B = 0.214, 0.706  # left edge of each panel's plot, figure fraction (names sit to its left)
SHORT = {"helps, possibly through length or query-term overlap": "helps*", "no effect larger than δ": "no effect",
         "insufficient n": "too few", "descriptive": "descriptive", "inconclusive": "inconclusive", "helps": "helps",
         "reported without a verdict": "no verdict", "loses the gain": "falls short"}

# Panel (a): (source, arm, ref, name, sub-row). None draws a rule between groups.
A_ROWS = [
    ("e1", "12", "P12", "Your reader's words up top", False),
    ("e1", "9", "original", "Target questions answered", False),
    ("e2a", "9", "9W", "heading vs the same text as plain text", True),
    ("e2a", "9", "9P", "heading vs a section without its words", True),
    None,
    ("e3", "2", "P2", "Question headings", False),
    ("e1", "3", "P3", "Lists for enumerations", False),
    ("e3", "7", "P7", "Cited sources", False),
    ("e3", "8", "P8", "Direct answer first", False),
    ("e3", "6", "P6", "Attributed expert quotes", False),
    ("e3", "5", "P5", "Statistics", False),
    ("e3", "10", "P10", "Explicit comparisons", False),
    ("e3", "4", "original", "Tables for comparisons", False),
    ("e1", "1", "original", "Standalone paragraphs", False),
    None,
    ("e1", "ALL", "P_ALL", "All fixes together, vs placebo", False),
    ("e1", "ALL", "original", "All fixes together", False),
]
# Panel (b): (key in data/e5_results.json "contrasts", name, sub-row, sign, replication key, retention guess).
B_ROWS = [
    ("main:9-original:new queries", "Exact question, new queries", False, 1, None, None),
    ("main:12-P12:new queries", "Missing words up top, new queries", False, 1, None, None),
    None,
    ("main:9K-original:pooled", "A keyword's two words", False, 1, "replication:9K-original:pooled", None),
    ("main:9K-9P:pooled", "vs a section without the reader's words", True, 1, "replication:9K-9P:pooled", None),
    ("main:12K-P12K:pooled", "Keyword's missing words up top", False, 1, None, None),
    ("main:9L-original:pooled", "Local model's question", False, 1, "replication:9L-original:pooled", None),
    ("main:9L-9P:pooled", "vs a section without the reader's words", True, 1, "replication:9L-9P:pooled", None),
    None,
    ("main:9K-9:pooled", "Keyword vs the exact question", False, 1, None, "9K"),
    ("main:9-9A:pooled", "All key words vs the exact question", False, -1, None, None),
]


def mark(ax, y, d, ci, label, n, *, filled=None, color=None):
    verdict = n >= 30 and label not in ("descriptive", "reported without a verdict") if filled is None else filled
    if color is None:
        color = C["after"] if label.startswith("helps") else (C["before"] if verdict else N["ink_soft"])
    ax.plot(ci, [y, y], color=color, lw=1.2, solid_capstyle="round", zorder=3)
    ax.scatter([d], [y], s=20, facecolor=color if verdict else "white", edgecolor=color, linewidths=1.0, zorder=4)
    return verdict


def rep_mark(ax, y, d, ci):
    ax.plot(ci, [y - 0.32] * 2, color=C["answer"], lw=0.7, zorder=3)
    ax.scatter([d], [y - 0.32], marker="D", s=8, color=C["answer"], zorder=4, linewidths=0)


def frame(ax, nrows, used):
    """Axes for nrows rows; the band and the zero line span only the top `used` rows (the rest holds the key)."""
    ax.set_xlim(*XLIM)
    ax.set_ylim(-0.8, nrows - 0.4)
    y_lo = -0.8 if used == nrows else nrows - used - 0.5
    ax.fill_betweenx([y_lo, nrows - 0.4], -DELTA, DELTA, color=fs.tint(N["ink_soft"], 0.88), zorder=0, lw=0)
    ax.plot([0, 0], [y_lo, nrows - 0.4], color=N["ink_soft"], lw=fs.LW["ref"], zorder=1)
    ax.set_yticks([])
    ax.set_xticks([-0.03, 0.03, 0.09], minor=True)
    ax.set_xticks([-0.06, 0, 0.06, 0.12])
    ax.set_xticklabels(["−0.06", "0", "+0.06", "+0.12"], fontsize=fs.FS["small"] - 0.6)
    ax.set_xlabel("citation score, edit minus reference", fontsize=fs.FS["small"] - 0.6, labelpad=2)
    fs.despine(ax, left=False)
    yt = ax.get_yaxis_transform()
    ax.text(1.03, nrows - 0.35, "  n  result", ha="left", va="bottom", fontsize=fs.FS["small"] - 0.6,
            color=N["ink_soft"], transform=yt, clip_on=False)
    return yt


def row_text(ax, yt, y, name, sub, ring, n, short, verdict):
    ax.text(-0.03, y, name + ("°" if ring else ""), ha="right", va="center",
            fontsize=fs.FS["small"] - 0.6, color=N["ink_soft"] if sub else N["ink"],
            fontstyle="italic" if sub else "normal", transform=yt, clip_on=False)
    ax.text(1.03, y, f"{n:>3}  {short}", ha="left", va="center", fontsize=fs.FS["small"] - 0.6,
            color=N["ink"] if verdict else N["ink_soft"], transform=yt, clip_on=False)


def rules(ax, ys, rows):
    """A thin rule between groups: a None in the row list marks a rule above the next row."""
    k = 0
    for r in rows:
        if r is None:
            ax.axhline(ys[k] + 0.5, color=N["rule"], lw=0.5, zorder=1)
        else:
            k += 1


def draw_key(fig, x0, y0, step):
    """The marker key, in figure coordinates, under panel (b): one line of marks, then two lines of notes."""
    fsz = fs.FS["small"] - 0.6
    marks = [("o", C["after"], C["after"], "helps"),
             ("o", C["before"], C["before"], "no effect or inconclusive"),
             ("o", "white", N["ink_soft"], "no verdict"),
             ("D", C["answer"], C["answer"], "60-query replication set")]
    renderer = fig.canvas.get_renderer()
    x = x0
    for m, fc, ec, text in marks:
        ax = fig.add_axes([x, y0 - step / 2, 0.012, step], frameon=False)
        ax.set_axis_off()
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.scatter([0], [0], marker=m, s=14 if m == "o" else 8, facecolor=fc, edgecolor=ec, linewidths=0.9)
        t = fig.text(x + 0.014, y0, text, ha="left", va="center", fontsize=fsz, color=N["ink_soft"])
        w = t.get_window_extent(renderer).width / fig.bbox.width
        x += 0.014 + w + 0.018
    lines = ["°  vs the unedited page; others vs a same-length placebo, or the edit named",
             "grey band ±0.03: the margin for no effect;  helps*: possibly length or query-word overlap",
             "falls short (black): the exact question beat the guess, 95% interval above 0, by",
             "the rule set before the run"]
    for j, text in enumerate(lines, 1):
        fig.text(x0 + 0.002, y0 - step * j, text, ha="left", va="center", fontsize=fsz, color=N["ink_soft"])


def main():
    args = fs.cli(__doc__)
    fs.apply()
    p1 = os.path.join(PAPER, "data", "e1_results.json")
    p5 = os.path.join(PAPER, "data", "e5_results.json")
    d1 = json.load(open(p1))
    d5 = json.load(open(p5))
    if abs(d5["settings"]["delta"] - DELTA) > 1e-12:
        raise SystemExit("fig_result: E5's margin differs from E1's")

    main_rows = {("e1", r["arm"], r["ref"]): r for r in d1["main"]["contrasts"]}
    main_rows.update({("e3", r["arm"], r["ref"]): r for r in d1["e3"]["contrasts"]})
    main_rows.update({("e2a", r["arm"], r["ref"]): r for r in d1["e2"]["e2a"]["main"]["planned"]})
    rep_rows = {("e1", r["arm"], r["ref"]): r for r in d1["replication"]["contrasts"] if r["n"] > 0}
    rep_rows.update({("e2a", r["arm"], r["ref"]): r for r in d1["e2"]["e2a"]["replication"]["planned"] if r["n"] > 0})
    E5 = d5["contrasts"]

    a_rows = [r for r in A_ROWS if r is not None]
    b_rows = [r for r in B_ROWS if r is not None]
    nrows = len(a_rows)
    H_IN = 0.60 + ROW_IN * nrows
    fig = fs.plt.figure(figsize=(WIDTH_IN, H_IN))
    bottom, top = 0.30 / H_IN, 1 - 0.30 / H_IN
    axa = fig.add_axes([AX_A, bottom, AX_W, top - bottom])
    per_row = (top - bottom) / (nrows + 0.4)
    nb = sum(r is not None for r in B_ROWS)
    axb = fig.add_axes([AX_B, top - per_row * (nb + 0.4), AX_W, per_row * (nb + 0.4)])
    ys = list(range(nrows))[::-1]
    title_y = 1 - 0.13 / H_IN
    for x, text in ((0.004, "(a)  Eleven checks, one change at a time"),
                    (0.505, "(b)  New queries, and sections built from a guess")):
        fig.text(x, title_y, text, ha="left", va="center", fontsize=fs.FS["title"] - 0.5, fontweight="semibold",
                 color=N["ink"])

    # ---- (a)
    yt = frame(axa, nrows, nrows)
    for y, (src, arm, ref, name, sub) in zip(ys, a_rows):
        r = main_rows[(src, arm, ref)]
        verdict = mark(axa, y, r["d"], r["ci95"], r["label"], r["n"])
        rep = rep_rows.get((src, arm, ref))
        if rep:
            rep_mark(axa, y, rep["d"], rep["ci95"])
        row_text(axa, yt, y, name, sub, ref == "original", r["n"], SHORT.get(r["label"], r["label"]), verdict)
    rules(axa, ys, A_ROWS)

    # ---- (b)
    yt = frame(axb, nb, nb)
    ysb = list(range(nb))[::-1]
    for y, (key, name, sub, sign, rkey, guess) in zip(ysb, b_rows):
        r = E5[key]
        d = sign * r["d"]
        ci = sorted(sign * x for x in r["ci95"])
        label, color, filled = r["label"], None, None
        if guess:  # the planned retention reading for this guess (exact question minus guess, 95% CI above 0)
            label, color, filled = d5["readings"]["retention"][guess], N["ink"], True
        verdict = mark(axb, y, d, ci, label, r["n"], filled=filled, color=color)
        if rkey:
            rr = E5[rkey]
            rep_mark(axb, y, rr["d"], rr["ci95"])
        row_text(axb, yt, y, name, sub, r["ref"] == "original", r["n"], SHORT.get(label, label), verdict)
    rules(axb, ysb, B_ROWS)

    # the key, in the empty rows under panel (b)
    draw_key(fig, 0.512, bottom + per_row * 2.2, per_row * 1.0)
    fs.save(fig, args, "fig1_result", inputs=[p1, p5], script=__file__)


if __name__ == "__main__":
    main()
