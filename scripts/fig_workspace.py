"""Figure 2: the draft view now and before. The Questions covered card at native resolution, the full window small,
and the old build's score card as the before.

Layout (column width 3.33 in):
  * right: the right rail of data/screens/draft_view.png (captured by scripts/capture_screens.mjs, Task 16: the
    espresso example after the two typed edits, "Questions covered: 2 of 4") cropped to the Questions covered card
    (RAIL_CROP, image pixels; the card's Edit questions button below is cut) and drawn about 2 in wide, so the card's UI
    text prints at 5 to 7 pt instead of the 2 pt it had at the full-window scale (review of 2026-11-08, Figure 2
    legibility). Numbered callouts sit at the anchors of data/fig2_callouts.json (`xy`, fractions of the full image);
    every one points to text a reader can read in the crop;
  * left, top to bottom: the full window (2500 x 1800) small, with the crop outlined; the old build's score card
    (data/screens/draft_view_before.png, a byte copy of the pre-redesign capture, score ring 37; BEFORE_CROP) as the
    before; the callout list.

Both screenshots are drawn with interpolation "none", so the PDF embeds the captures' own pixels, never a resampled
copy. The script fails if a screenshot or a kept callout is missing (the build reads data/ only, where both are
committed).

Usage: .venv/bin/python -I -B scripts/fig_workspace.py [--out figures] [--png <dir>]
"""
from __future__ import annotations

import os
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figdata  # noqa: E402
import figstyle as fs  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Rectangle  # noqa: E402

W_IN = fs.COLUMN_IN
PAD, GAP, LABEL_H = 0.04, 0.07, 0.10   # inches: outer margin, gap between the columns, a label line above an image
RAIL_W_IN = 2.02                        # the card crop's printed width; LEFT_W_IN takes the rest
LEFT_W_IN = W_IN - 2 * PAD - GAP - RAIL_W_IN
BEFORE = "data/screens/draft_view_before.png"
# The Questions covered card in the capture, in image pixels (2500 x 1800): the card spans x 1724 to 2471 and
# y 162 to 1380; its last text line ends at y 1254 and its Edit questions button starts at y 1284 (measured
# 2026-11-08 with PIL, logged in the private working log).
# Tightened in the third round (2026-11-08): the draft sheet's edge at x 1664 and the button left the crop.
RAIL_CROP = (1696, 2486, 150, 1282)  # x0, x1, y0, y1
# The old score card in BEFORE, in image pixels: the card ("37", "AI-ready score", "A writing checklist, not a
# forecast. Why?") and the "0 of 29 handled" line under it. Callout 1 of fig2_callouts_before.json (xy 0.6832,
# 0.1578, i.e. pixel 1708, 284) marks the card's left edge; the right edge stops short of the card's border
# (third round, 2026-11-08) so the inset stays short.
BEFORE_CROP = (1708, 2350, 160, 540)  # x0, x1, y0, y1
TEXT = fs.FS["small"] - 0.6   # 6.2 pt: the labels and the callout list (STYLE.md section 6; review S5)
# Callouts drawn and listed, by their number in data/fig2_callouts.json, renumbered 1, 2, 3 in the figure: the count
# (1), the card's label chip (4) and an open row that names the missing words (6, hand-measured on the committed
# screenshot; 1 and 4 re-measured by hand for the tightened crop, _provenance.re_measured). The Quick edit (2) is
# below the card, outside the crop, so it is no longer called out (Section 4 describes it); the Show passage (3)
# and the privacy chip (5) stay in the data only.
KEEP = (1, 4, 6)
N, S, C = fs.NEUTRAL, fs.SURFACE, fs.CONCEPT


def frame(ax, x, y, w, h, lw=0.6, r=0.006, z=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc="none",
                                ec=N["rule"], lw=lw, zorder=z, clip_on=False))


def callout(ax, x, y, n):
    ax.scatter([x], [y], s=34, facecolor=C["after"], edgecolor="white", linewidths=0.8, zorder=10, clip_on=False)
    ax.text(x, y, str(n), ha="center", va="center", fontsize=fs.FS["small"] - 2.2, color="white",
            fontweight="bold", zorder=11)


def label(fig, x_in, y_in, fig_h, text):
    fig.text(x_in / W_IN, y_in / fig_h, text, ha="left", va="center", fontsize=TEXT, color=N["ink"],
             fontweight="semibold")


def main():
    args = fs.cli(__doc__)
    fs.apply()
    co, cpath = figdata.fig2_callouts()
    shot = os.path.join(figdata.PAPER, co["screenshot"])
    before = os.path.join(figdata.PAPER, BEFORE)
    for p in (shot, before):
        if not os.path.exists(p):
            raise SystemExit(f"fig_workspace: {os.path.relpath(p, figdata.PAPER)} is missing")
    kept = [c for c in co["callouts"] if c["n"] in KEEP]
    if [c["n"] for c in kept] != list(KEEP) or not all(c.get("xy") for c in kept):
        raise SystemExit(f"fig_workspace: callouts {KEEP} missing, out of order or without xy in {cpath}")
    shown = {c["n"]: k for k, c in enumerate(kept, 1)}  # data number -> number printed in the figure
    heading = co.get("captured", {}).get("strings", {}).get("heading")
    img = fs.plt.imread(shot)
    old = fs.plt.imread(before)
    ih, iw = img.shape[0], img.shape[1]

    # Geometry in inches; axes use image pixel coordinates (y down), so the callout anchors need no flip.
    x0, x1, y0, y1 = RAIL_CROP
    rail_h = RAIL_W_IN * (y1 - y0) / (x1 - x0)
    fig_h = PAD + LABEL_H + rail_h + PAD
    fig = fs.plt.figure(figsize=(W_IN, fig_h))

    def axes_in(x, y, w, h):
        ax = fig.add_axes([x / W_IN, y / fig_h, w / W_IN, h / fig_h])
        ax.axis("off")
        return ax

    # ---- right: the Questions covered card, cropped, at native resolution
    rail_x, rail_y = W_IN - PAD - RAIL_W_IN, PAD
    ax = axes_in(rail_x, rail_y, RAIL_W_IN, rail_h)
    ax.set_xlim(x0, x1)
    ax.set_ylim(y1, y0)
    ax.imshow(img[y0:y1, x0:x1], extent=(x0, x1, y1, y0), aspect="auto", zorder=1, interpolation="none")
    frame(ax, x0, y0, x1 - x0, y1 - y0, r=8)
    label(fig, rail_x, rail_y + rail_h + LABEL_H / 2, fig_h, "The Questions covered card (the right rail), enlarged")
    for c in kept:
        px, py = c["xy"][0] * iw, c["xy"][1] * ih
        if not (x0 < px < x1 and y0 < py < y1):
            raise SystemExit(f"fig_workspace: callout {c['n']} at pixel ({px:.0f}, {py:.0f}) falls outside RAIL_CROP")
        callout(ax, px, py, shown[c["n"]])

    # ---- left, top: the full window, small, with the crop outlined
    lx, y = PAD, fig_h - PAD
    thumb_h = LEFT_W_IN * ih / iw
    label(fig, lx, y - LABEL_H / 2, fig_h, "The draft view, full window")
    y -= LABEL_H + thumb_h
    axt = axes_in(lx, y, LEFT_W_IN, thumb_h)
    axt.set_xlim(0, iw)
    axt.set_ylim(ih, 0)
    axt.imshow(img, extent=(0, iw, ih, 0), aspect="auto", zorder=1, interpolation="none")
    frame(axt, 0, 0, iw, ih, r=12)
    axt.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc="none", ec=C["after"], lw=0.8, zorder=3))

    # ---- left, middle: the old build's score card
    bx0, bx1, by0, by1 = BEFORE_CROP
    before_h = LEFT_W_IN * (by1 - by0) / (bx1 - bx0)
    # The two left-column gaps (0.10 and 0.14 in before the third round) shrank by 0.05 in each when the crops of
    # 2026-11-08 made the before inset taller and the rail shorter; the list ran 0.08 in past the bottom check below.
    y -= 0.05
    label(fig, lx, y - LABEL_H / 2, fig_h, "Before: the old build’s card")
    y -= LABEL_H + before_h
    axb = axes_in(lx, y, LEFT_W_IN, before_h)
    axb.set_xlim(bx0, bx1)
    axb.set_ylim(by1, by0)
    axb.imshow(old[by0:by1, bx0:bx1], extent=(bx0, bx1, by1, by0), aspect="auto", zorder=1, interpolation="none")
    frame(axb, bx0, by0, bx1 - bx0, by1 - by0, r=8)

    # ---- left, bottom: the callout list (what each number points at; the strings as the capture read them)
    items = []
    for c in kept:
        text = c.get("text") or c["what"] + (f": “{c['ui_string']}”" if c.get("ui_string") else "")
        text = text.replace("'", "\u2019")  # typographic apostrophes in the printed labels (the data keeps its own)
        if c["n"] == 1 and not (heading and text.startswith(heading)):
            raise SystemExit("fig_workspace: callout 1 must print the captured count (captured.strings.heading)")
        # callout 6 wraps at 25: at 27 its second line crossed the right panel's frame (third round, 2026-11-08)
        items.append((shown[c["n"]], textwrap.wrap(text, 25 if c["n"] == 6 else 27)))
    line_h, gap, indent = 0.092, 0.035, 0.15
    y -= 0.09
    for n, lines in items:
        fig.text((lx + 0.04) / W_IN, y / fig_h, str(n), ha="center", va="top", fontsize=TEXT - 0.4,
                 color="white", fontweight="bold", bbox=dict(boxstyle="circle,pad=0.18", fc=C["after"], ec="none"))
        fig.text((lx + indent) / W_IN, (y + 0.012) / fig_h, "\n".join(lines), ha="left", va="top",
                 fontsize=TEXT, color=N["ink"], linespacing=1.1)
        y -= len(lines) * line_h + gap
    if y < PAD:
        raise SystemExit(f"fig_workspace: the callout list runs {PAD - y:.2f} in past the figure's bottom; shorten it")

    fs.save(fig, args, "fig2_workspace", inputs=[cpath, shot, before], script=__file__)


if __name__ == "__main__":
    main()
