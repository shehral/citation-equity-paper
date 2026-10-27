"""Figure 5: following the reader's-words tips raises the score, because that check is scored for having helped.

The deployed draft view after the author typed the words the reader's-words tips named into the title and the
opening (espresso example), with numbered callouts at anchors measured in the same capture and a callout list
under the image. Captured by scripts/capture_reader_words.mjs, which also reran the tool's engine on the same two
edits (data/fig5_callouts.json "engine": only the reader's-words check changed).

Input: data/fig5_callouts.json and data/screens/reader_words.png. This script writes no number file.
Usage: .venv/bin/python -I -B scripts/fig_reader_words.py [--out figures] [--png <dir>]
"""
from __future__ import annotations

import os
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figdata  # noqa: E402
import figstyle as fs  # noqa: E402
from fig_workspace import callout  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

W_IN = fs.COLUMN_IN
N, C = fs.NEUTRAL, fs.CONCEPT


def main():
    args = fs.cli(__doc__)
    fs.apply()
    co, cpath = figdata.data_json("fig5_callouts.json")
    shot = os.path.join(figdata.PAPER, co["screenshot"])
    if co.get("status") != "captured" or not os.path.exists(shot):
        raise SystemExit("fig_reader_words: run scripts/capture_reader_words.mjs first")
    if co["engine"]["changed"] != ["reader-words"]:
        raise SystemExit(f"fig_reader_words: the engine says other checks moved too: {co['engine']['changed']}")
    img = fs.plt.imread(shot)

    pad, img_w = 0.03, W_IN - 0.12
    img_h = img_w * img.shape[0] / img.shape[1]
    items = []
    for c in co["callouts"]:
        text = c["what"] + (f": “{c['ui_string']}”" if c.get("ui_string") else "")
        items.append((c["n"], textwrap.wrap(text, 92)))
    line_h, gap = 0.084, 0.018
    list_h = sum(len(lines) * line_h + gap for _, lines in items)
    fig_h = pad + img_h + 0.05 + list_h
    fig = fs.plt.figure(figsize=(W_IN, fig_h))
    ax = fig.add_axes([pad / W_IN, (fig_h - pad - img_h) / fig_h, img_w / W_IN, img_h / fig_h])
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.imshow(img, extent=(0, 1, 0, 1), aspect="auto", zorder=1, interpolation="lanczos")
    ax.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0,rounding_size=0.006", fc="none",
                                ec=N["rule"], lw=0.6, zorder=2))
    for c in co["callouts"]:
        callout(ax, c["xy"][0], 1 - c["xy"][1], c["n"])

    y = fig_h - pad - img_h - 0.075
    for n, lines in items:
        fig.text(0.11 / W_IN, y / fig_h, str(n), ha="center", va="top", fontsize=fs.FS["small"] - 1.2,
                 color="white", fontweight="bold", bbox=dict(boxstyle="circle,pad=0.12", fc=C["after"], ec="none"))
        fig.text(0.24 / W_IN, (y + 0.012) / fig_h, "\n".join(lines), ha="left", va="top",
                 fontsize=fs.FS["small"] - 1.3, color=N["ink"], linespacing=1.1)
        y -= len(lines) * line_h + gap

    fs.save(fig, args, "fig5_reader_words", inputs=[cpath, shot], script=__file__)


if __name__ == "__main__":
    main()
