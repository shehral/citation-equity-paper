"""Figure 4(a): applying the suggestions moved mean citation share by 1 to 3 points on every model, and the one-sentence
answer edit stayed far below the pre-registered +0.10 bar.

One row per open model (smallest at the top). Two lanes per row:
  after - before (the tool's suggestions applied; exploratory, uncorrected), indigo;
  one-sentence answer edit - before (the registered H2 contrast), teal.
Small dots: the 8 per-question differences (each a mean over 8 seeds); large dot and bar: the model mean with its 95%
t interval over the 8 questions (post hoc); right of the plot, the mean and the exact two-sided sign-flip p over the
8 questions (the p the text reports; uncorrected). Coral band: at or above the pre-registered bar (H2 minimum gain, parsed
from the harness). Hairline: zero. Row label: the model and the mean number of sources it cites of the 8 given
(rounded half-up to two decimals, trailing zero dropped, so 6.95 prints as in the text).

Input: data/sensitivity_derived.json (scripts/derive_sensitivity.py, from CE/experiments/results/sensitivity/).
Every plotted value and printed number is read from it.

Usage: .venv/bin/python -I -B scripts/fig_sensitivity.py [--out figures] [--png <dir>]
"""
from __future__ import annotations

import os
import sys
from decimal import ROUND_HALF_UP, Decimal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figdata  # noqa: E402
import figstyle as fs  # noqa: E402

WIDTH_IN, HEIGHT_IN = fs.COLUMN_IN, 2.30
LANE = 0.19          # lane offset from the row centre (data units; rows are 1 apart)
JIT = 0.045          # deterministic vertical spread of the per-question dots


def jitter(vals):
    """Alternate the dots above and below the lane, by rank, so near-equal values do not hide each other."""
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    out = [0.0] * len(vals)
    for r, i in enumerate(order):
        out[i] = JIT if r % 2 == 0 else -JIT
    return out


def cites(x):
    """Sources cited per answer, half-up to two decimals without a trailing zero (6.2, 6.95, 6.25, 6.65)."""
    d = Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return format(d.normalize(), "f")


def pfmt(p):
    """An exact sign-flip p as the text gives it: three decimals below 0.1 (0.0078 -> 0.008, 0.0391 -> 0.039,
    0.0547 -> 0.055), two above (0.5156 -> 0.52), leading zero dropped."""
    nd = 3 if p < 0.1 else 2
    d = Decimal(str(p)).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP)
    return "p " + format(d, "f").lstrip("0")


def main():
    args = fs.cli(__doc__)
    fs.apply()
    d, dpath = figdata.sensitivity_derived()
    C, N = fs.CONCEPT, fs.NEUTRAL
    bar = d["thresholds"]["h2_min_gain"]["value"]
    models = d["models"]

    lanes = [("diff_after_minus_before", "after_minus_before", C["after"], +LANE),
             ("diff_answer_first_minus_before", "answer_first_minus_before", C["answer"], -LANE)]
    allv = [v for m in models for key, *_ in lanes for v in m[key]]
    lo = min(min(allv), 0.0) - 0.012
    hi = max(max(allv), bar) + 0.022

    fig = fs.plt.figure(figsize=(WIDTH_IN, HEIGHT_IN))
    AX = [0.285, 0.165, 0.505, 0.685]
    ax = fig.add_axes(AX)
    ax.set_xlim(lo, hi)
    ax.set_ylim(-len(models) + 0.45, 0.55)

    # pre-registered bar: band to the right, labelled at the top
    ax.axvspan(bar, hi, color=C["bar"], alpha=0.14, lw=0, zorder=0.5)  # translucent, so it tints the zebra rows too
    ax.axvline(bar, color=C["bar"], lw=1.0, zorder=1)
    ax.annotate(f"pre-registered bar {fs.fmt(bar, 2, sign=True)}", xy=(bar, 1.0), xycoords=("data", "axes fraction"),
                xytext=(0, 2.5), textcoords="offset points", ha="center", va="bottom", fontsize=fs.FS["small"] - 0.8,
                color=fs.text_color(C["bar"]), fontweight="semibold", annotation_clip=False)
    ax.axvline(0.0, color=N["ink_soft"], lw=0.6, zorder=1)

    for i, m in enumerate(models):
        y0 = -i
        if i % 2 == 1:  # quiet zebra band so each model reads as one row
            ax.axhspan(y0 - 0.5, y0 + 0.5, color=fs.SURFACE["sunken"], lw=0, zorder=0)
        for key, stat, col, off in lanes:
            vals = m[key]
            ys = [y0 + off + j for j in jitter(vals)]
            ax.scatter(vals, ys, s=9, facecolor=fs.tint(col, 0.45), edgecolor="white", linewidths=0.35, zorder=3)
            s = m[stat]
            ax.plot(s["ci95_t"], [y0 + off] * 2, color=col, lw=1.7, solid_capstyle="butt", zorder=4)
            ax.scatter([s["mean"]], [y0 + off], s=30, facecolor=col, edgecolor="white", linewidths=0.7, zorder=5)
            # the mean's value in a column right of the plot, level with its lane
            ax.annotate(f"{fs.fmt(s['mean'], 3, sign=True)}  {pfmt(s['p_sign_flip'])}", xy=(1.0, y0 + off), xycoords=("axes fraction", "data"),
                        xytext=(5, 0), textcoords="offset points", ha="left", va="center",
                        fontsize=fs.FS["small"] - 0.6, color=fs.text_color(col), annotation_clip=False)
        # row label: model, then sources cited (of the 8 given)
        ax.annotate(m["label"], xy=(0, y0 + 0.08), xycoords=("axes fraction", "data"), xytext=(-6, 0),
                    textcoords="offset points", ha="right", va="bottom", fontsize=fs.FS["small"],
                    fontweight="semibold", color=N["ink"], annotation_clip=False)
        ax.annotate(f"cites {cites(m['mean_sources_cited'])} of 8 sources", xy=(0, y0 + 0.02),
                    xycoords=("axes fraction", "data"), xytext=(-6, 0), textcoords="offset points", ha="right",
                    va="top", fontsize=fs.FS["small"] - 0.9, color=N["ink_soft"], annotation_clip=False)

    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    step = 0.05
    ticks = [round(k * step, 2) for k in range(int(lo / step) - 1, int(hi / step) + 2) if lo <= k * step <= hi]
    ax.set_xticks(ticks, [fs.fmt(t, 2, sign=t != 0) for t in ticks])
    ax.set_xlabel("Change in citation share against the before draft", fontsize=fs.FS["small"])
    ax.grid(axis="x", color=N["grid"], lw=fs.LW["grid"], zorder=0)

    # lane key above the plot (two encodings shared by every row)
    kx, ky = 0.285, 0.962
    fig.text(0.015, ky, "(a)", ha="left", va="center", fontsize=fs.FS["title"], fontweight="semibold", color=N["ink"])
    items = [("after \u2212 before (exploratory)", C["after"]),
             ("answer edit \u2212 before (registered)", C["answer"])]
    y = ky
    for text, col in items:
        fig.text(kx - 0.012, y, "●", ha="right", va="center", fontsize=fs.FS["small"], color=col)
        fig.text(kx, y, text, ha="left", va="center", fontsize=fs.FS["small"] - 0.4, color=fs.text_color(col))
        y -= 0.05
    fig.text(AX[0] + AX[2] + 0.012, AX[1] + AX[3] + 0.012, "mean, sign-flip p", ha="left", va="bottom",
             fontsize=fs.FS["small"] - 0.8, color=N["ink_soft"])

    fs.save(fig, args, "fig4_sensitivity", inputs=[dpath], script=__file__)


if __name__ == "__main__":
    main()
