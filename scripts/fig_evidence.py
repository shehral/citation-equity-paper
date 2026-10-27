"""Figure 3: the evidence behind each draft check, cell by cell, with its grade under the strict and a looser rule.

Rows: the eleven draft checks (the PI's six first, then the four added from the literature and the one added from
our own test, reader-words), in the engine's order.
Columns: the nine studies of CE/docs/evidence.md. One glyph per (check, study) cell, coded in data/evidence_matrix.csv
from that check's section of evidence.md (one source line per cell):
  filled dot      controlled gain on the practice the check looks for
  half dot        gain that is observational, elicited, or about a nearby practice (evidence.md line 32)
  dot in a ring   gain in some settings, null (grey ring) or harm (coral ring) in others
  ring            null: no effect found
  cross           significant harm
  coral half dot  observational negative
  diamond         the survey's rating (filled: supportive; open: cautious)
  dash            cited as background only (mechanism, hypothesis, a different practice)
Two chip columns: the shipped grade (strict rule) and the grade under a looser rule, both computed by
scripts/derive_loose_grades.py (the strict one is checked against the engine registry). An arrow marks a change.
Below: the seven site-readiness items, graded on a different standard (operator documentation counts).

Inputs: data/evidence_matrix.csv, data/evidence_grades_loose.json, data/grades.json. Nothing is typed.

Usage: .venv/bin/python -I -B scripts/fig_evidence.py [--out figures] [--png <dir>]
"""
from __future__ import annotations

import os
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figdata  # noqa: E402
import figstyle as fs  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

C, N = fs.CONCEPT, fs.NEUTRAL
GAIN = C["strong"]                      # green: a finding in the check's favour
NULLC = "#8E939C"                       # grey ring: no effect found
HARM = fs.shade(C["bar"], 0.12)         # coral: harm
SURVEY_POS = C["moderate"]
BG = "#B9BDC4"

W_IN, H_IN = fs.COLUMN_IN, 3.08
LABEL_IN = 1.12       # row-label column (from the figure's left edge)
COL_IN = 0.144        # one study column
CHIP_IN = 0.368       # one grade-chip column
GAP_IN = 0.055        # matrix to chips
ROW_IN = 0.142
MAT_Y0_IN = 0.96      # bottom of the matrix, from the figure bottom (room for the key and readiness strip)
KEY_Y_IN = [0.82, 0.69, 0.56]       # key rows
KEY_X_IN = [0.06, 1.16, 2.30]       # key columns
READY_Y_IN = 0.43                   # top rule of the readiness strip

R_DOT = 23            # marker areas (pt^2)
R_RING = 46


def glyph(ax, x, y, cell):
    r, design, direct = cell["result"], cell["design"], cell["directness"]
    full = design == "controlled" and direct == "direct"
    fill = "full" if full else "left"
    if r in ("gain", "gain_part_null", "gain_part_harm"):
        inner = R_DOT if r == "gain" else R_DOT * 0.62
        ax.plot([x], [y], marker="o", ms=(inner ** 0.5), mfc=GAIN, mfcalt="white", fillstyle=fill, mec=GAIN,
                mew=0.8, ls="none", zorder=4)
        if r != "gain":
            ring = NULLC if r == "gain_part_null" else HARM
            ax.scatter([x], [y], s=R_RING * 1.05, facecolor="none", edgecolor=ring, linewidths=1.0, zorder=3)
    elif r == "null":
        ax.scatter([x], [y], s=R_DOT * 1.1, facecolor="white", edgecolor=NULLC, linewidths=1.2, zorder=4)
    elif r == "harm":
        ax.scatter([x], [y], s=R_DOT * 1.45, marker="X", facecolor=HARM, edgecolor="white", linewidths=0.4, zorder=4)
    elif r == "negative":
        ax.plot([x], [y], marker="o", ms=(R_DOT ** 0.5), mfc=HARM, mfcalt="white", fillstyle="left", mec=HARM,
                mew=0.8, ls="none", zorder=4)
    elif r == "survey_support":
        ax.scatter([x], [y], s=R_DOT * 0.85, marker="D", facecolor=SURVEY_POS, edgecolor="white", linewidths=0.4,
                   zorder=4)
    elif r == "survey_caution":
        ax.scatter([x], [y], s=R_DOT * 0.7, marker="D", facecolor="white", edgecolor=NULLC, linewidths=1.0, zorder=4)
    elif r == "background":
        ax.plot([x - 0.16, x + 0.16], [y, y], color=BG, lw=1.3, solid_capstyle="round", zorder=4)
    else:
        raise SystemExit(f"fig_evidence: unknown result {r!r}")


def chip(ax, x, y, w, h, grade, transform=None, bold=False, size=None, rounding=None, aspect=1.0):
    """A grade chip: tinted fill, the grade's hue as border, darkened text. rounding in x data units;
    aspect = (x data units per inch) / (y data units per inch) keeps the corners round on unequal axes."""
    rounding = rounding if rounding is not None else 0.32 * h / aspect
    col = C[grade]
    kw = {"transform": transform} if transform is not None else {}
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle=f"round,pad=0,rounding_size={rounding}",
                                fc=fs.tint(col, 0.80), ec=col, lw=0.6, zorder=3, mutation_aspect=aspect, **kw))
    ax.text(x, y - 0.01 * h, grade, ha="center", va="center", fontsize=size or fs.FS["small"] - 1.2,
            color=fs.text_color(col), fontweight="semibold" if bold else "normal", zorder=4, **kw)


def main():
    args = fs.cli(__doc__)
    fs.apply()
    cells, mpath = figdata.evidence_matrix()
    eg, epath = figdata.evidence_grades()
    reg, gpath = figdata.grades()
    studies = figdata.STUDIES
    checks = eg["checks"]
    if [c["id"] for c in checks] != [c["id"] for c in reg["checks"]]:
        raise SystemExit("fig_evidence: check order differs between the grade files")
    by = {(c["check_id"], c["study_id"]): c for c in cells}

    fig = fs.plt.figure(figsize=(W_IN, H_IN))
    nS, nR = len(studies), len(checks)
    mat_w = nS * COL_IN + GAP_IN + 2 * CHIP_IN
    ax = fig.add_axes([LABEL_IN / W_IN, MAT_Y0_IN / H_IN, mat_w / W_IN, nR * ROW_IN / H_IN])
    # data units: one study column = 1, one row = 1
    chip_w = CHIP_IN / COL_IN
    xs_chip = [nS - 0.5 + GAP_IN / COL_IN + chip_w * (k + 0.5) for k in range(2)]
    ax.set_xlim(-0.5, nS - 0.5 + GAP_IN / COL_IN + 2 * chip_w)
    ax.set_ylim(nR - 0.5, -0.5)
    ax.axis("off")

    n_pi = sum(c["in_foundation_design"] for c in checks)
    for i in range(nR):  # zebra rows over the study columns
        if i % 2 == 0:
            ax.add_patch(fs.plt.Rectangle((-0.5, i - 0.5), nS, 1, fc=fs.SURFACE["sunken"], ec="none", zorder=0))
    for j in range(nS + 1):
        ax.plot([j - 0.5] * 2, [-0.5, nR - 0.5], color="white", lw=0.8, zorder=1)
    ax.plot([-0.5, nS - 0.5 + GAP_IN / COL_IN + 2 * chip_w], [n_pi - 0.5] * 2, color=N["rule"], lw=0.7, zorder=2)

    for i, chk in enumerate(checks):
        for j, st in enumerate(studies):
            cell = by.get((chk["id"], st["id"]))
            if cell:
                glyph(ax, j, i, cell)
        changed = chk["strict"] != chk["loose"]
        asp = (1 / COL_IN) / (1 / ROW_IN)
        chip(ax, xs_chip[0], i, chip_w * 0.86, 0.72, chk["strict"], aspect=1 / asp)
        chip(ax, xs_chip[1], i, chip_w * 0.86, 0.72, chk["loose"], bold=changed, aspect=1 / asp)
        if changed:
            ax.annotate("", xy=(xs_chip[1] - chip_w * 0.43, i), xytext=(xs_chip[0] + chip_w * 0.43, i),
                        arrowprops=dict(arrowstyle="-|>", lw=0.6, color=N["ink_soft"], mutation_scale=5,
                                        shrinkA=0.5, shrinkB=0.5), zorder=5)
        ax.annotate(chk["title"], xy=(-0.5, i), xytext=(-4, 0), textcoords="offset points", ha="right", va="center",
                    fontsize=fs.FS["small"] - 0.75, color=N["ink"], annotation_clip=False)

    # group brackets at the far left: the PI's design, then the checks added later (four from the literature, one from
    # our own test; CE/packages/engine/src/registry.ts lines 13 to 17)
    for (a, b, text) in ((0, n_pi - 1, "PI's design"), (n_pi, nR - 1, "added")):
        ya = (MAT_Y0_IN + (nR - a - 0.10) * ROW_IN) / H_IN
        yb = (MAT_Y0_IN + (nR - b - 0.90) * ROW_IN) / H_IN
        xb = 0.024
        fig.add_artist(fs.plt.Line2D([xb, xb], [yb, ya], color=N["rule"], lw=0.8, transform=fig.transFigure))
        fig.text(xb - 0.006, (ya + yb) / 2, text, rotation=90, ha="right", va="center",
                 fontsize=fs.FS["small"] - 1.6, color=N["ink_soft"])

    # column headers: study names (rotated), chip headers
    for j, st in enumerate(studies):
        ax.annotate(st["label"], xy=(j, -0.5), xytext=(0, 3), textcoords="offset points", rotation=58,
                    ha="left", va="bottom", rotation_mode="anchor", fontsize=fs.FS["small"] - 0.9, color=N["ink"],
                    annotation_clip=False)
    for x, text in zip(xs_chip, ("strict rule\n(shipped)", "looser\nrule")):
        ax.annotate(text, xy=(x, -0.5), xytext=(0, 3), textcoords="offset points", ha="center", va="bottom",
                    fontsize=fs.FS["small"] - 1.0, color=N["ink"], fontweight="semibold", linespacing=0.95,
                    annotation_clip=False)
    # title block in the free corner left of the rotated study names
    fig.text(0.012, 0.992, "Draft checks", ha="left", va="top", fontsize=fs.FS["title"] - 0.4,
             fontweight="semibold", color=N["ink"])
    t = eg["tally"]
    sub = (f"strict rule: {t['strict']['strong'] + t['strict']['moderate']} strong or moderate,\n"
           f"{t['strict']['mixed']} mixed, {t['strict']['untested']} untested; looser rule:\n"
           f"{t['loose']['strong'] + t['loose']['moderate']} strong or moderate, {t['loose']['mixed']} mixed")
    fig.text(0.012, 0.948, sub, ha="left", va="top", fontsize=fs.FS["small"] - 1.3, color=N["ink_soft"],
             linespacing=1.15)

    # ---------------------------------------------------------------- key (glyph legend; shared by every cell)
    kax = fig.add_axes([0.0, 0.0, 1.0, 1.0], facecolor="none")
    kax.set_xlim(0, W_IN)
    kax.set_ylim(0, H_IN)
    kax.axis("off")
    key = [
        ({"result": "gain", "design": "controlled", "directness": "direct"}, "controlled gain"),
        ({"result": "gain", "design": "observational", "directness": "near"}, "indirect or observational gain"),
        ({"result": "gain_part_null", "design": "controlled", "directness": "near"}, "gain in part, null in part"),
        ({"result": "null", "design": "controlled", "directness": "direct"}, "null"),
        ({"result": "harm", "design": "controlled", "directness": "direct"}, "significant harm"),
        ({"result": "negative", "design": "observational", "directness": "direct"}, "observational negative"),
        ({"result": "survey_support"}, "survey: supportive"),
        ({"result": "survey_caution"}, "survey: cautious"),
        ({"result": "background"}, "background only"),
    ]
    # key glyphs live on an axes whose data units equal inches; use a helper axes per glyph scale
    y_key, x_key = KEY_Y_IN, KEY_X_IN
    gx = fig.add_axes([0, 0, 1, 1], facecolor="none")
    gx.set_xlim(0, W_IN / COL_IN)
    gx.set_ylim(H_IN / ROW_IN, 0)
    gx.axis("off")
    for k, (cell, text) in enumerate(key):
        r, c = k % 3, k // 3
        cell = {"design": "survey", "directness": "none", **cell}
        x_in, y_in = x_key[c], y_key[r]
        glyph(gx, x_in / COL_IN, (H_IN - y_in) / ROW_IN, cell)
        kax.text(x_in + 0.085, y_in, text, ha="left", va="center", fontsize=fs.FS["small"] - 1.4, color=N["ink"])

    # ---------------------------------------------------------------- site readiness strip
    ry = READY_Y_IN
    kax.plot([0.03, W_IN - 0.03], [ry] * 2, color=N["rule"], lw=0.6)
    kax.text(0.03, ry - 0.06, "Site readiness, graded on operator documentation (a different standard)",
             ha="left", va="center", fontsize=fs.FS["small"] - 1.2, color=N["ink_soft"])
    groups = {g: [r["title"] for r in eg["readiness"] if r["grade"] == g] for g in figdata.GRADES}
    colw = (W_IN - 0.06) / 4
    for k, g in enumerate(figdata.GRADES):
        x0 = 0.03 + k * colw
        chip(kax, x0 + 0.20, ry - 0.165, 0.38, 0.098, g, size=fs.FS["small"] - 1.4)
        names = ", ".join(groups[g]) if groups[g] else "none"
        lines = textwrap.wrap(names, 22)
        kax.text(x0 + 0.01, ry - 0.235, "\n".join(lines), ha="left", va="top", fontsize=fs.FS["small"] - 1.6,
                 color=N["ink"], linespacing=1.05)

    fs.save(fig, args, "fig3_evidence", inputs=[mpath, epath, gpath], script=__file__)


if __name__ == "__main__":
    main()
