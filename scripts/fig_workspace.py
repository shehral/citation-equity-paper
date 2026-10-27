"""Figure 2: the draft view. The author applies one fix at a time, and every fix shows how strong its evidence is.

Two modes, chosen by what exists in data/:
  * data/screens/draft_view.png present (captured by scripts/capture_screens.mjs from the deployed build) (now):
    the screenshot at its own aspect ratio with numbered callouts at the anchors measured in the same capture
    (data/fig2_callouts.json `xy`, fractions from the image's top-left);
  * otherwise: a marked PLACEHOLDER frame, a wireframe of the planned capture (dashboard state 3, Draft
    (working), in the redesign mockup) with the numbered callouts where they will sit, and the callout list.
    Nothing in the wireframe is data; it shows layout only.

Input: data/fig2_callouts.json (and the screenshot, when it exists).

Usage: .venv/bin/python -I -B scripts/fig_workspace.py [--out figures] [--png <dir>]
"""
from __future__ import annotations

import os
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figdata  # noqa: E402
import figstyle as fs  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

W_IN, H_IN = fs.COLUMN_IN, 2.75
N, S, C = fs.NEUTRAL, fs.SURFACE, fs.CONCEPT
OWN = N["owner"]


def box(ax, x, y, w, h, fc, ec=None, lw=0.6, r=0.012, z=2, ls="-"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc,
                                ec=ec or "none", lw=lw, zorder=z, ls=ls))


def callout(ax, x, y, n):
    ax.scatter([x], [y], s=34, facecolor=C["after"], edgecolor="white", linewidths=0.8, zorder=10)
    ax.text(x, y - 0.002, str(n), ha="center", va="center", fontsize=fs.FS["small"] - 2.2, color="white",
            fontweight="bold", zorder=11)


def wireframe(ax):
    """Layout of the planned capture (redesign mockup, state 3). Grey blocks only; no text from the app."""
    ink = fs.tint(N["ink_soft"], 0.55)
    line = fs.tint(N["ink_soft"], 0.78)
    box(ax, 0.0, 0.0, 1.0, 1.0, "white", N["rule"], lw=0.7, r=0.02, z=1)
    box(ax, 0.0, 0.905, 1.0, 0.095, S["sunken"], None, r=0.0, z=2)                  # header
    box(ax, 0.03, 0.932, 0.16, 0.04, ink, z=3)                                        # brand
    box(ax, 0.73, 0.925, 0.20, 0.055, S["brand_soft"], C["after"], lw=0.5, r=0.025, z=3)  # privacy chip
    # draft sheet (left)
    box(ax, 0.03, 0.05, 0.55, 0.82, S["paper"], S["paper_rule"], lw=0.6, z=2)
    y = 0.80
    widths = [0.40, 0.47, 0.45, 0.30, None, 0.32, 0.48, 0.46, 0.44, 0.21, None, 0.36, 0.47, 0.42, 0.25]
    for w in widths:
        if w is None:
            y -= 0.035
            continue
        ax.plot([0.07, 0.07 + w], [y, y], color=line, lw=2.0, solid_capstyle="round", zorder=3)
        y -= 0.045
    ax.plot([0.07, 0.40], [0.664, 0.664], color=S["mark"], lw=0.9, ls=(0, (1, 1.2)), zorder=4)  # flagged span
    # right rail
    box(ax, 0.62, 0.70, 0.35, 0.17, "white", S["paper_rule"], z=2)                    # score card
    box(ax, 0.65, 0.80, 0.10, 0.045, C["after"], z=3)
    box(ax, 0.65, 0.745, 0.28, 0.018, S["sunken"], z=3)
    box(ax, 0.65, 0.745, 0.18, 0.018, fs.tint(C["after"], 0.35), z=4)
    box(ax, 0.62, 0.47, 0.35, 0.19, S["brand_soft"], C["after"], lw=0.6, z=2)         # Start-here fix (active)
    ax.plot([0.65, 0.90], [0.62, 0.62], color=ink, lw=1.6, solid_capstyle="round", zorder=3)
    ax.plot([0.65, 0.86], [0.585, 0.585], color=line, lw=1.4, solid_capstyle="round", zorder=3)
    box(ax, 0.65, 0.495, 0.12, 0.045, C["after"], z=3)                                # Apply
    box(ax, 0.79, 0.495, 0.10, 0.045, "white", N["rule"], z=3)                        # Undo / skip
    for k, yy in enumerate((0.385, 0.31)):                                           # fix groups
        box(ax, 0.62, yy, 0.35, 0.06, "white", S["paper_rule"], z=2)
        ax.plot([0.65, 0.80], [yy + 0.03] * 2, color=line, lw=1.4, solid_capstyle="round", zorder=3)
        box(ax, 0.83, yy + 0.014, 0.11, 0.032, fs.tint(C["mixed"], 0.8), C["mixed"], lw=0.5, r=0.016, z=3)
    box(ax, 0.62, 0.17, 0.35, 0.10, "white", S["paper_rule"], z=2)                    # Test it
    ax.plot([0.65, 0.76], [0.235, 0.235], color=ink, lw=1.4, solid_capstyle="round", zorder=3)
    ax.plot([0.65, 0.93], [0.195, 0.195], color=line, lw=1.2, solid_capstyle="round", zorder=3)
    return {1: (0.62, 0.86), 2: (0.62, 0.64), 3: (0.97, 0.415), 4: (0.97, 0.26), 5: (0.73, 0.952)}


def main():
    args = fs.cli(__doc__)
    fs.apply()
    co, cpath = figdata.fig2_callouts()
    shot = os.path.join(figdata.PAPER, co["screenshot"])
    inputs = [cpath]
    captured = os.path.exists(shot) and all(c.get("xy") for c in co["callouts"])
    img = fs.plt.imread(shot) if captured else None

    # Layout in inches: the image keeps its own aspect ratio, the callout list sits under it.
    pad, img_w = 0.06, W_IN - 0.12
    img_h = img_w * img.shape[0] / img.shape[1] if captured else 0.585 * H_IN
    items = []
    for c in co["callouts"]:
        text = c["what"] + (f": \u201c{c['ui_string']}\u201d" if c.get("ui_string") else "")
        items.append((c["n"], textwrap.wrap(text, 92)))
    line_h, gap = 0.083, 0.035
    list_h = sum(len(lines) * line_h + gap for _, lines in items) + 0.05
    note_h = 0.0 if captured else 0.1
    fig_h = pad + img_h + 0.06 + list_h + note_h
    fig = fs.plt.figure(figsize=(W_IN, fig_h))
    ax = fig.add_axes([pad / W_IN, (fig_h - pad - img_h) / fig_h, img_w / W_IN, img_h / fig_h])
    ax.axis("off")

    if captured:
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.imshow(img, extent=(0, 1, 0, 1), aspect="auto", zorder=1, interpolation="lanczos")
        ax.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0,rounding_size=0.006", fc="none",
                                    ec=N["rule"], lw=0.6, zorder=2))
        anchors = {c["n"]: (c["xy"][0], 1 - c["xy"][1]) for c in co["callouts"]}
        inputs.append(shot)
    else:
        ax.set_xlim(-0.01, 1.01)
        ax.set_ylim(-0.01, 1.01)
        anchors = wireframe(ax)
        ax.text(0.305, 0.43, "[PLACEHOLDER]\nscreenshot of the\ndraft view of the\nshipped dashboard", ha="center",
                va="center", fontsize=fs.FS["small"] - 0.6, color=OWN, fontweight="semibold", zorder=12,
                linespacing=1.15, bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=OWN, lw=0.7))
    for n, (x, y) in anchors.items():
        callout(ax, x, y, n)

    # callout list under the image
    y = fig_h - pad - img_h - 0.09
    for n, lines in items:
        fig.text(0.11 / W_IN, y / fig_h, str(n), ha="center", va="top", fontsize=fs.FS["small"] - 1.2,
                 color="white", fontweight="bold", bbox=dict(boxstyle="circle,pad=0.18", fc=C["after"], ec="none"))
        fig.text(0.24 / W_IN, (y + 0.012) / fig_h, "\n".join(lines), ha="left", va="top",
                 fontsize=fs.FS["small"] - 1.3, color=N["ink"], linespacing=1.1)
        y -= len(lines) * line_h + gap
    if not captured:
        fig.text(0.035, 0.004, "Wireframe of the redesign mockup, state 3; wording to be checked on the deployed build.",
                 ha="left", va="bottom", fontsize=fs.FS["small"] - 1.8, color=OWN)

    fs.save(fig, args, "fig2_workspace", inputs=inputs, script=__file__)


if __name__ == "__main__":
    main()
