"""Figure 1, right: the headline. Following the suggestions raises the checklist score a lot and citation share a little.

(a) Checklist score (foundation preset, 0 to 100), before to after, one hollow slope per sample draft.
    Input: data/scores.json (scripts/collect_scores.py: `ce analyze --json` on CE/samples/*/{before,after}.md).
(b) Citation share of the target page, before to after, one filled slope per open model, pooled over the 8 questions
    (faint: the per-sample means over 4 questions each). Chance (1 of 8 sources) dotted; the off-topic control dashed.
    Input: CE/experiments/results/sensitivity/sensitivity_*.json (summary.mean_target_share, summary.chance_share,
    per_question). The after-minus-before contrast is exploratory in CE/experiments/PREREG_sensitivity.md.

No llama3.2:3b data: the in-tool run reports word share on a different setup (CE/samples/README.md).
Every plotted value and every printed number is read from the inputs; nothing is typed.

Usage: .venv/bin/python -I -B scripts/fig_headline.py [--out figures] [--png <dir>] [--ce-root <CE>]
"""
from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figdata  # noqa: E402
import figstyle as fs  # noqa: E402

WIDTH_IN = 2.85   # right part of the figure* (7.0 in); the TikZ schematic takes the rest
HEIGHT_IN = 2.12


def pct(after, before):
    v = round(100.0 * (after / before - 1.0))
    return f"+{v}%" if v >= 0 else f"−{-v}%"


def main():
    args = fs.cli(__doc__)
    fs.apply()
    sc = figdata.scores()
    sens = figdata.sensitivity(args.ce_root)
    C, N = fs.CONCEPT, fs.NEUTRAL

    fig = fs.plt.figure(figsize=(WIDTH_IN, HEIGHT_IN))
    # Hand-set axes boxes (figure fractions): room on the right of each panel for the stacked end labels.
    AX_A = [0.092, 0.135, 0.178, 0.655]
    AX_B = [0.530, 0.135, 0.128, 0.655]
    axA, axB = fig.add_axes(AX_A), fig.add_axes(AX_B)
    X0, X1 = 0.0, 1.0

    for ax in (axA, axB):
        ax.set_xlim(-0.75 if ax is axA else -0.22, 1.22)
        ax.set_xticks([X0, X1], ["before", "after"])
        ax.tick_params(axis="x", length=0, pad=3, labelsize=fs.FS["small"] - 0.6)
        fs.ygrid(ax)
        ax.spines["bottom"].set_visible(False)

    # ---------------------------------------------------------------- (a) checklist score, hollow marks
    rises = []
    labA_r, labA_l = [], []  # end labels after (right) and before (left), stacked so close scores never overlap
    samples = [(k, sc["samples"][k]) for k, _ in figdata.SAMPLES]
    for i, (key, row) in enumerate(samples):
        b, a = row["before"]["foundation"], row["after"]["foundation"]
        rises.append(a - b)
        line_c = fs.tint(C["after"], 0.15 + 0.25 * i)
        axA.plot([X0, X1], [b, a], color=line_c, lw=1.3, zorder=2)
        axA.scatter([X0], [b], s=26, facecolor="white", edgecolor=C["before"], linewidths=1.3, zorder=3)
        axA.scatter([X1], [a], s=26, facecolor="white", edgecolor=C["after"], linewidths=1.3, zorder=3)
        labA_r.append({"y": a, "text": f"{a}  {pct(a, b)}", "color": C["after"]})
        labA_l.append({"y": b, "text": f"{b}", "color": C["before"]})
    # sample names: above the higher before mark, below the lower one
    order = sorted(range(len(samples)), key=lambda i: samples[i][1]["before"]["foundation"])
    for rank, i in enumerate(order):
        row = samples[i][1]
        up = rank == len(order) - 1
        axA.annotate(row["label"], (X0, row["before"]["foundation"]), xytext=(0, 6.5 if up else -6.5),
                     textcoords="offset points", ha="center", va="bottom" if up else "top",
                     fontsize=fs.FS["small"] - 0.6, color=N["ink_soft"])
    axA.set_ylim(0, 100)
    axA.set_yticks([0, 50, 100])

    # ---------------------------------------------------------------- (b) citation share, filled marks
    chance = sens[0]["summary"]["chance_share"]
    if any(m["summary"]["chance_share"] != chance for m in sens):
        raise SystemExit("fig_headline: chance share differs between models")
    offtop = max(m["summary"]["mean_target_share"]["offtopic"] for m in sens)
    gains, labB = [], []
    ymax = 0.0
    shades = [0.42, 0.28, 0.14, 0.0]  # lightness per model (smallest lightest), one hue: the after concept
    for m, t in zip(sens, shades):
        mts = m["summary"]["mean_target_share"]
        b, a = mts["before"], mts["after"]
        gains.append(a - b)
        col = fs.tint(C["after"], t)
        for s_key, _ in figdata.SAMPLES:  # faint per-sample slopes behind
            sb = figdata.per_sample_mean(m["per_question"], "before", s_key)
            sa = figdata.per_sample_mean(m["per_question"], "after", s_key)
            ymax = max(ymax, sb, sa)
            axB.plot([X0, X1], [sb, sa], color=fs.tint(C["after"], 0.80), lw=0.6, zorder=1)
        axB.plot([X0, X1], [b, a], color=col, lw=1.4, zorder=3)
        axB.scatter([X0], [b], s=18, facecolor=C["before"], edgecolor="white", linewidths=0.5, zorder=4)
        axB.scatter([X1], [a], s=20, facecolor=col, edgecolor="white", linewidths=0.5, zorder=4)
        labB.append({"y": a, "text": f"{m['name']}  {pct(a, b)}", "color": col})
        ymax = max(ymax, a, b)
    top = math.ceil(ymax / 0.05) * 0.05
    axB.set_ylim(0, top)
    axB.set_yticks([0, 0.1, 0.2] + ([0.3] if top >= 0.3 else []),
                   [fs.fmt(v, 1) for v in [0, 0.1, 0.2] + ([0.3] if top >= 0.3 else [])])
    axB.axhline(chance, color=C["chance"], lw=0.7, ls=(0, (1, 1.6)), zorder=2)
    axB.annotate(f"chance {fs.fmt(chance, 3)}", xy=(-0.2, chance), xycoords="data", xytext=(0, -2),
                 textcoords="offset points", ha="left", va="top", fontsize=fs.FS["small"] - 0.6,
                 color=N["ink_soft"])
    axB.axhline(offtop, color=C["offtopic"], lw=0.8, ls=(0, (3, 2)), zorder=2)
    # 4 places: the maximum is 0.0031 (Qwen3.5-9B); rounding it to 0.003 under a "≤" would be false (verify-claims A2)
    axB.annotate(f"off-topic control ≤ {fs.fmt(offtop, 4)}", xy=(-0.2, offtop), xycoords="data",
                 xytext=(0, 2), textcoords="offset points", ha="left", va="bottom", fontsize=fs.FS["small"] - 0.6,
                 color=fs.text_color(C["offtopic"]))

    # ---------------------------------------------------------------- titles carry the headline (numbers from data)
    lo, hi = min(rises), max(rises)
    glo, ghi = round(100 * min(gains)), round(100 * max(gains))
    for (ax_box, letter, title, sub, foot) in (
            (AX_A, "a", "Checklist score", f"rises {lo} to {hi} points", "2 sample drafts"),
            (AX_B, "b", "Citation share", f"mean rises {glo} to {ghi} points", "4 open models, 8 questions \u00d7 8 seeds")):
        x = ax_box[0] - 0.08
        fig.text(x, 0.985, f"({letter})  {title}", ha="left", va="top", fontsize=fs.FS["title"],
                 fontweight="semibold", color=N["ink"])
        fig.text(x, 0.905, sub, ha="left", va="top", fontsize=fs.FS["small"], color=N["ink_soft"])
        fig.text(x, 0.012, foot, ha="left", va="bottom", fontsize=fs.FS["small"] - 0.8, color=N["ink_soft"])

    fs.end_labels(axA, labA_r, X1, dx=5, size=fs.FS["small"] - 0.5, gap=7.4)
    fs.end_labels(axA, labA_l, X0, dx=5, size=fs.FS["small"] - 0.4, gap=7.4, side="left")
    fs.end_labels(axB, labB, X1, dx=5, size=fs.FS["small"] - 0.5, gap=7.4)

    inputs = [figdata.scores_path()] + [m["path"] for m in sens]
    fs.save(fig, args, "fig1_headline", inputs=inputs, script=__file__)


if __name__ == "__main__":
    main()
