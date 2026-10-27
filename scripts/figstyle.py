"""Shared matplotlib style for the Citation Equity paper (house kit from the stale-monitors paper, adapted).

What it fixes, once for every figure:
  * one concept-to-color map (CONCEPT), chosen for prettiness (the owner waived colorblind safety on 2026-10-21) and
    taken from the dashboard redesign's oklch tokens where the app has one (indigo brand, grade hues, paper
    surfaces: citation-equity/docs/superpowers/specs/assets/2026-10-23-dashboard/mockup-dashboard.html, converted to
    sRGB hex); the same hexes are xcolor colors in smpreprint.sty, and `--check-sty` fails if the two drift apart;
  * fonts from the tectonic bundle: Lato, the sans of the paper's headings, captions and tables, embedded as
    TrueType (pdf.fonttype 42), never a system font;
  * sizes for ACM sigconf (column 3.33 in, figure* 7.0 in; the WWW 2027 demo paper) and for the 6.1 in measure of
    the later arXiv build;
  * minimal spines, a light y grid, helpers for direct labels instead of legends,
    a sequential scale for positive data and a diverging scale centred on white for signed data;
  * deterministic, provenance-stamped PDFs (inputs and their SHA-256 in the PDF metadata, no creation date).

Use in a figure script (see fig_*.py):
    import figstyle as fs
    args = fs.cli(__doc__)                 # --root <repo root> --out <figures dir> [--png <preview dir>]
    fs.apply()
    fig, ax = fs.figure(height=2.4)
    ...
    fs.save(fig, args, "fig_name", inputs=[...])

Checks:
    python -I figstyle.py --check-sty ../smpreprint.sty      # palette in the .sty == palette here
    python -I figstyle.py --swatch <out.pdf>                  # one-page swatch of the concept map
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import colors as mcolors  # noqa: E402
from matplotlib import font_manager  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------------------------------- palette and concepts
OKABE_ITO = {  # Okabe & Ito (2008); colorblind-safe; LaTeX names smOI*
    "black": "#000000", "orange": "#E69F00", "sky_blue": "#56B4E9", "green": "#009E73",
    "yellow": "#F0E442", "blue": "#0072B2", "vermillion": "#D55E00", "purple": "#CC79A7",
}
NEUTRAL = {
    "ink": "#1A1A1A",       # text and the base model
    "ink_soft": "#5C5C5C",  # axes, ticks, secondary text
    "rule": "#BFC5CC",      # reference lines, box rules
    "grid": "#E6E6E6",      # grid lines
    "tint": "#F3F5F7",      # box fill, light bands
    "accent": "#2F3B4C",    # box titles and rules (not a data concept)
    "owner": "#0000FF",     # owner marks in the paper only
}
# Surfaces of the app (dashboard tokens), used by the schematic and by light bands in plots.
SURFACE = {
    "paper": "#FBF9F5",        # oklch(0.982 0.005 85): the draft sheet, warm paper
    "sunken": "#F4F2EE",       # oklch(0.962 0.006 85): wells, tracks
    "paper_rule": "#E2DFDA",   # oklch(0.905 0.008 85): borders on paper
    "brand_soft": "#E9EDFF",   # oklch(0.95 0.03 277): brand tint (active passage, chips)
    "mark": "#717ADF",         # oklch(0.62 0.15 277): dotted underline under flagged text
}
# One color per concept, in every figure, schematic and caption key (notes/NARRATIVE.md section 4).
# Score marks are hollow and citation marks filled, so the checklist score and citation never read as one quantity.
CONCEPT = {
    "before": "#7C8799",     # before draft: soft slate, oklch(0.62 0.03 260)
    "after": "#4A4CBA",      # after draft (suggestions applied) and the tool itself: indigo brand, oklch(0.48 0.17 277)
    "answer": "#009B8F",     # one-sentence answer edit (registered contrast): teal, oklch(0.62 0.11 185)
    "offtopic": "#9D9EA2",   # off-topic control: grey, dashed
    "chance": "#1A1A1A",     # chance level (1 of 8 sources): thin dotted ink
    "bar": "#ED7665",        # pre-registered bar (+0.10): coral band, oklch(0.70 0.15 30)
    "strong": "#048149",     # evidence grade strong: deep green, dashboard --g-strong oklch(0.53 0.13 155)
    "moderate": "#6DBA70",   # evidence grade moderate: light green, oklch(0.72 0.13 145)
    "mixed": "#AD721C",      # evidence grade mixed: amber, dashboard --g-mixed oklch(0.6 0.12 70)
    "untested": "#A9AAB1",   # evidence grade untested: light grey, oklch(0.74 0.01 275)
}
LATEX_NAMES = {  # name in smpreprint.sty -> hex here
    **{"smOI" + "".join(w.capitalize() for w in k.split("_")): v for k, v in OKABE_ITO.items()},
    "smInk": NEUTRAL["ink"], "smInkSoft": NEUTRAL["ink_soft"], "smRule": NEUTRAL["rule"], "smGrid": NEUTRAL["grid"],
    "smTint": NEUTRAL["tint"], "smAccent": NEUTRAL["accent"], "smOwner": NEUTRAL["owner"],
    "smPaper": SURFACE["paper"], "smSunken": SURFACE["sunken"], "smPaperRule": SURFACE["paper_rule"],
    "smBrandSoft": SURFACE["brand_soft"], "smMark": SURFACE["mark"],
    "smBefore": CONCEPT["before"], "smAfter": CONCEPT["after"], "smAnswer": CONCEPT["answer"],
    "smOfftopic": CONCEPT["offtopic"], "smChance": CONCEPT["chance"], "smBar": CONCEPT["bar"],
    "smStrong": CONCEPT["strong"], "smModerate": CONCEPT["moderate"], "smMixed": CONCEPT["mixed"],
    "smUntested": CONCEPT["untested"],
}

# ----------------------------------------------------------------------------------------------- sizes
TEXTWIDTH_IN = 6.1          # arXiv build (smpreprint.sty); figures are included at \textwidth
COLUMN_IN = 3.33            # ACM sigconf column (\columnwidth)
FIGSTAR_IN = 7.0            # ACM sigconf figure* (\textwidth)
FS = {"base": 7.5, "small": 6.8, "title": 8.0, "label": 7.0}
LW = {"axis": 0.6, "grid": 0.5, "ref": 0.7, "data": 1.5, "key": 2.0, "context": 0.9}
MARKER_S = 30               # scatter marker area (pt^2)

# ----------------------------------------------------------------------------------------------- color helpers


def mix(c1, c2, t):
    """Linear RGB mix: t = 0 gives c1, t = 1 gives c2."""
    a, b = mcolors.to_rgb(c1), mcolors.to_rgb(c2)
    return mcolors.to_hex(tuple((1 - t) * x + t * y for x, y in zip(a, b)))


def tint(c, t):
    return mix(c, "#FFFFFF", t)


def shade(c, t):
    return mix(c, "#000000", t)


def _lum(c):
    def ch(v):
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = mcolors.to_rgb(c)
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(c, bg="#FFFFFF"):
    hi, lo = sorted((_lum(c), _lum(bg)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def text_color(c, minimum=4.5):
    """The concept hue, darkened just enough to read as small text on white (WCAG 4.5:1)."""
    t = 0.0
    while contrast(shade(c, t)) < minimum and t < 0.9:
        t += 0.02
    return shade(c, t)


def seq_cmap(concept="after", name=None):
    """Sequential scale for positive data: white to the concept color to a darker shade."""
    c = CONCEPT.get(concept, concept)
    return mcolors.LinearSegmentedColormap.from_list(name or f"seq_{concept}", ["#FFFFFF", tint(c, 0.55), c, shade(c, 0.35)])


def div_cmap(neg="bar", pos="after", name=None):
    """Diverging scale centred on white, for signed data whose zero is meaningful (use with centered_norm)."""
    a, b = CONCEPT.get(neg, neg), CONCEPT.get(pos, pos)
    return mcolors.LinearSegmentedColormap.from_list(
        name or f"div_{neg}_{pos}", [shade(a, 0.3), a, tint(a, 0.6), "#FFFFFF", tint(b, 0.6), b, shade(b, 0.3)])


def centered_norm(vmin, vmax, center=0.0):
    return mcolors.TwoSlopeNorm(vmin=vmin, vcenter=center, vmax=vmax)


# ----------------------------------------------------------------------------------------------- fonts (tectonic bundle)
FONT_FILES = ["Lato-Regular.ttf", "Lato-Italic.ttf", "Lato-Bold.ttf", "Lato-BoldItalic.ttf",
              "Lato-Semibold.ttf", "Lato-SemiboldItalic.ttf"]


def _tectonic():
    for cand in (os.environ.get("TECTONIC"), "/opt/homebrew/bin/tectonic", shutil.which("tectonic")):
        if cand and os.path.exists(cand):
            return cand
    raise SystemExit("figstyle: tectonic not found (set TECTONIC); the figure font comes from its bundle")


def ensure_fonts():
    """Fetch Lato from the tectonic bundle into a cache (SM_FONT_CACHE, default scripts/.fontcache) and register it."""
    cache = os.environ.get("SM_FONT_CACHE") or os.path.join(HERE, ".fontcache")
    os.makedirs(cache, exist_ok=True)
    for name in FONT_FILES:
        path = os.path.join(cache, name)
        if not os.path.exists(path) or os.path.getsize(path) < 10000:
            out = subprocess.run([_tectonic(), "-X", "bundle", "cat", name], capture_output=True, check=True).stdout
            if out[:4] not in (b"\x00\x01\x00\x00", b"true"):
                raise SystemExit(f"figstyle: {name} from the bundle is not a TrueType font")
            with open(path, "wb") as fh:
                fh.write(out)
        font_manager.fontManager.addfont(path)
    return cache


# ----------------------------------------------------------------------------------------------- rcParams


def apply():
    ensure_fonts()
    ink, soft = NEUTRAL["ink"], NEUTRAL["ink_soft"]
    plt.rcParams.update({
        "font.family": "Lato", "font.size": FS["base"],
        "mathtext.fontset": "custom", "mathtext.rm": "Lato", "mathtext.it": "Lato:italic",
        "mathtext.bf": "Lato:bold", "mathtext.sf": "Lato", "mathtext.default": "it",
        "axes.titlesize": FS["title"], "axes.titleweight": "semibold", "axes.titlelocation": "left",
        "axes.titlepad": 6.0, "axes.titlecolor": ink,
        "axes.labelsize": FS["base"], "axes.labelcolor": ink, "axes.labelpad": 3.0,
        "axes.edgecolor": soft, "axes.linewidth": LW["axis"],
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": False, "grid.color": NEUTRAL["grid"], "grid.linewidth": LW["grid"],
        "axes.axisbelow": True, "axes.unicode_minus": True,
        "xtick.labelsize": FS["small"], "ytick.labelsize": FS["small"],
        "xtick.color": soft, "ytick.color": soft, "xtick.labelcolor": soft, "ytick.labelcolor": soft,
        "xtick.major.size": 2.5, "ytick.major.size": 2.5, "xtick.major.width": LW["axis"],
        "ytick.major.width": LW["axis"], "xtick.major.pad": 2.0, "ytick.major.pad": 2.0,
        "legend.fontsize": FS["label"], "legend.frameon": False, "legend.handlelength": 1.4,
        "legend.handletextpad": 0.5, "legend.borderaxespad": 0.2, "legend.columnspacing": 1.2,
        "lines.linewidth": LW["data"], "lines.markersize": 4.5, "lines.solid_capstyle": "round",
        "patch.linewidth": 0.6,
        "figure.dpi": 150, "savefig.dpi": 300, "figure.facecolor": "white", "savefig.facecolor": "white",
        "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none",
        "figure.constrained_layout.h_pad": 0.03, "figure.constrained_layout.w_pad": 0.03,
        "figure.constrained_layout.hspace": 0.04, "figure.constrained_layout.wspace": 0.04,
    })


def figure(height, width=TEXTWIDTH_IN, nrows=1, ncols=1, **kw):
    """A figure at the text width with constrained layout. Returns (fig, axes)."""
    return plt.subplots(nrows, ncols, figsize=(width, height), layout="constrained", **kw)


def freeze_layout(fig):
    """Run the layout once, then fix it, so labels placed afterwards do not move the axes."""
    fig.canvas.draw()
    fig.set_layout_engine("none")


# ----------------------------------------------------------------------------------------------- marks and labels


def despine(ax, left=True, bottom=True):
    ax.spines["left"].set_visible(left)
    ax.spines["bottom"].set_visible(bottom)
    if not left:
        ax.tick_params(axis="y", length=0)
    if not bottom:
        ax.tick_params(axis="x", length=0)


def ygrid(ax):
    ax.grid(axis="y", color=NEUTRAL["grid"], lw=LW["grid"], zorder=0)


def panel_title(ax, letter, text, sub=None):
    """Left-aligned panel title '(a) text', with an optional second line in the soft ink."""
    t = f"({letter})  {text}" if letter else text
    ax.set_title(t, loc="left", fontsize=FS["title"], fontweight="semibold", color=NEUTRAL["ink"],
                 pad=(14 if sub else 6))
    if sub:
        ax.annotate(sub, xy=(0, 1), xycoords="axes fraction", xytext=(0, 4), textcoords="offset points",
                    ha="left", va="bottom", fontsize=FS["small"], color=NEUTRAL["ink_soft"], annotation_clip=False)


def refline(ax, y=None, x=None, label=None, where="right", ls=(0, (3, 2.5)), color=None, lw=None, z=1, **tkw):
    """A thin reference line, directly labelled."""
    color = color or NEUTRAL["ink_soft"]
    if y is not None:
        ax.axhline(y, color=color, lw=lw or LW["ref"], ls=ls, zorder=z)
        if label:
            xa = 0.995 if where == "right" else 0.005
            ax.annotate(label, xy=(xa, y), xycoords=("axes fraction", "data"), xytext=(0, 2.5),
                        textcoords="offset points", ha="right" if where == "right" else "left", va="bottom",
                        fontsize=FS["small"], color=color, **tkw)
    if x is not None:
        ax.axvline(x, color=color, lw=lw or LW["ref"], ls=ls, zorder=z)
        if label:  # where="right" puts the label to the right of the line, otherwise to its left
            ax.annotate(label, xy=(x, 0.995), xycoords=("data", "axes fraction"), xytext=(3 if where == "right" else -3, 0),
                        textcoords="offset points", ha="left" if where == "right" else "right", va="top",
                        fontsize=FS["small"], color=color, **tkw)


def label(ax, x, y, text, color=None, dx=4, dy=0, ha="left", va="center", size=None, weight="normal", leader=False,
          halo=True, **kw):
    """A direct label at a data point, offset in points; colored text is darkened to stay legible. leader=True draws
    a hairline from the label to the point (for labels pushed away from a crowded cluster)."""
    c = text_color(color) if color else NEUTRAL["ink_soft"]
    if leader:
        kw.setdefault("arrowprops", dict(arrowstyle="-", lw=0.6, color="#9AA3AD", shrinkA=1.0, shrinkB=3.5))
    if halo:  # a white backing so grid and reference lines never cut through a label
        kw.setdefault("bbox", dict(boxstyle="square,pad=0.06", fc="white", ec="none"))
    return ax.annotate(text, (x, y), xytext=(dx, dy), textcoords="offset points", ha=ha, va=va,
                       fontsize=size or FS["label"], color=c, fontweight=weight, **kw)


_CANDIDATES = [(5, 0, "left", "center"), (-5, 0, "right", "center"), (0, 6, "center", "bottom"),
               (0, -6, "center", "top"), (5, 6, "left", "bottom"), (-5, 6, "right", "bottom"),
               (5, -6, "left", "top"), (-5, -6, "right", "top"), (9, 0, "left", "center"),
               (-9, 0, "right", "center"), (0, 11, "center", "bottom"), (0, -11, "center", "top"),
               # 12 onwards: pushed away from a cluster, with a hairline leader
               (-20, 10, "right", "bottom", True), (-20, -10, "right", "top", True), (20, 10, "left", "bottom", True),
               (20, -10, "left", "top", True), (-28, 0, "right", "center", True), (28, 0, "left", "center", True),
               (0, 20, "center", "bottom", True), (0, -20, "center", "top", True)]


def place_labels(ax, items, points=None, size=None, candidates=None):
    """Greedy direct labelling. items: dicts with x, y, text and optional color, prefer (index into candidates).
    Each label takes the first candidate offset whose box stays inside the axes and overlaps neither an earlier label
    nor any marker in `points` (list of (x, y)). Call after freeze_layout(fig)."""
    fig = ax.figure
    renderer = fig.canvas.get_renderer()
    cands = candidates or _CANDIDATES
    pts = [ax.transData.transform(p) for p in (points or [(it["x"], it["y"]) for it in items])]
    r_px = 4.2 * fig.dpi / 72.0
    axbox = ax.get_window_extent(renderer)
    placed = []
    for it in items:
        order = list(range(len(cands)))
        if "prefer" in it:
            order.remove(it["prefer"])
            order.insert(0, it["prefer"])
        best = None
        for k in order:
            dx, dy, ha, va, *ld = cands[k]
            a = label(ax, it["x"], it["y"], it["text"], it.get("color"), dx=dx, dy=dy, ha=ha, va=va, size=size,
                      leader=bool(ld and ld[0]))
            bb = a.get_window_extent(renderer).expanded(1.04, 1.10)
            inside = (bb.x0 >= axbox.x0 - 2 and bb.x1 <= axbox.x1 + 2 and bb.y0 >= axbox.y0 - 2 and bb.y1 <= axbox.y1 + 2)
            hits_label = any(bb.overlaps(o) for o in placed)
            own = ax.transData.transform((it["x"], it["y"]))
            hits_pt = any(bb.x0 - r_px < px < bb.x1 + r_px and bb.y0 - r_px < py < bb.y1 + r_px
                          for (px, py) in pts if abs(px - own[0]) > 0.5 or abs(py - own[1]) > 0.5)
            if inside and not hits_label and not hits_pt:
                best = (a, bb)
                break
            a.remove()
        if best is None:  # fall back to the preferred slot; reported so the script can be tuned
            dx, dy, ha, va, *ld = cands[order[0]]
            a = label(ax, it["x"], it["y"], it["text"], it.get("color"), dx=dx, dy=dy, ha=ha, va=va, size=size,
                      leader=bool(ld and ld[0]))
            best = (a, a.get_window_extent(renderer))
            print(f"figstyle.place_labels: no free slot for {it['text']!r}; used the preferred one", file=sys.stderr)
        placed.append(best[1])
    return placed


def end_labels(ax, items, x, dx=6, gap=None, size=None, side="right", leader_color="#9AA3AD"):
    """Labels at the ends of lines (slope charts), stacked so they never overlap. items: dicts with y, text and an
    optional color and weight. Labels are spread around their data y with a minimum gap (in points, default 1.15 x
    the font size) and joined to the line end by a hairline leader when moved. Call after freeze_layout(fig)."""
    size = size or FS["label"]
    gap = gap or 1.15 * size
    fig = ax.figure
    to_pt = 72.0 / fig.dpi
    ys = [ax.transData.transform((x, it["y"]))[1] * to_pt for it in items]
    order = sorted(range(len(items)), key=lambda i: ys[i])
    pos = [ys[i] for i in order]
    for _ in range(200):  # relax: push neighbours apart symmetrically until every gap is at least `gap`
        moved = False
        for k in range(1, len(pos)):
            d = pos[k] - pos[k - 1]
            if d < gap - 1e-6:
                shift = (gap - d) / 2
                pos[k - 1] -= shift
                pos[k] += shift
                moved = True
        if not moved:
            break
    sgn = 1 if side == "right" else -1
    out = []
    for k, i in enumerate(order):
        it = items[i]
        dy = pos[k] - ys[i]
        c = text_color(it["color"]) if it.get("color") else NEUTRAL["ink_soft"]
        kw = {}
        if abs(dy) > 0.6:
            kw["arrowprops"] = dict(arrowstyle="-", lw=0.5, color=leader_color, shrinkA=0.5, shrinkB=2.5,
                                    connectionstyle="arc3,rad=0")
        out.append(ax.annotate(it["text"], (x, it["y"]), xytext=(sgn * dx, dy), textcoords="offset points",
                               ha="left" if side == "right" else "right", va="center", fontsize=size, color=c,
                               fontweight=it.get("weight", "normal"), annotation_clip=False, **kw))
    return out


def key_handles(entries):
    """Legend handles from (label, scatter-kwargs or line-kwargs) pairs, for the rare figure that needs a legend."""
    from matplotlib.lines import Line2D
    hs = []
    for text, kw in entries:
        kw = dict(kw)
        if "marker" in kw and "s" in kw:
            hs.append(Line2D([], [], ls="none", marker=kw["marker"], markersize=(kw["s"] ** 0.5),
                             markerfacecolor=kw.get("facecolor"), markeredgecolor=kw.get("edgecolor"),
                             markeredgewidth=kw.get("linewidths", 0.6), label=text))
        else:
            hs.append(Line2D([], [], label=text, **kw))
    return hs


# ----------------------------------------------------------------------------------------------- numbers


def fmt(x, nd=3, sign=False):
    """Format like paper/scripts/paper_numbers.py f() (same rounding), with a true minus sign."""
    v = float(x)
    if abs(v) < 0.5 * 10 ** (-nd):
        v = 0.0
    s = f"{v:+.{nd}f}" if sign else f"{v:.{nd}f}"
    return s.replace("-", "\u2212")


# ----------------------------------------------------------------------------------------------- I/O, provenance


def cli(doc):
    p = argparse.ArgumentParser(description=(doc or "").strip().splitlines()[0] if doc else None)
    p.add_argument("--root", default=os.path.dirname(HERE), help="paper repo root (inputs are read under it)")
    p.add_argument("--out", default=os.path.join(os.path.dirname(HERE), "figures"), help="figures directory (output)")
    p.add_argument("--png", default=None, help="optional directory for 200 dpi PNG previews")
    p.add_argument("--ce-root", default=os.environ.get("CE_ROOT", "../citation-equity"),
                   help="the Citation Equity tool repo (read only)")
    a = p.parse_args()
    a.root, a.out, a.ce_root = os.path.abspath(a.root), os.path.abspath(a.out), os.path.abspath(a.ce_root)
    return a


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def save(fig, args, name, inputs, script):
    """Write <out>/<name>.pdf (deterministic: no creation date; inputs and their SHA-256 in the metadata)."""
    os.makedirs(args.out, exist_ok=True)
    def rel(p):
        for base, tag in ((args.root, ""), (getattr(args, "ce_root", None), "CE/")):
            if base and os.path.abspath(p).startswith(base + os.sep):
                return tag + os.path.relpath(p, base)
        return p
    prov = "; ".join(f"{rel(p)} sha256:{sha256(p)[:16]}" for p in inputs)
    meta = {"Title": name, "Author": "citation-equity-paper/scripts", "Subject": f"inputs: {prov}",
            "Creator": f"scripts/{os.path.basename(script)} via figstyle.py", "CreationDate": None}
    path = os.path.join(args.out, name + ".pdf")
    fig.savefig(path, metadata=meta)
    if args.png:
        os.makedirs(args.png, exist_ok=True)
        fig.savefig(os.path.join(args.png, name + ".png"), dpi=200)
    plt.close(fig)
    print(f"wrote {path}")
    return path


# ----------------------------------------------------------------------------------------------- checks


def check_sty(path):
    txt = open(path, encoding="utf-8").read()
    found = {m.group(1): "#" + m.group(2).upper() for m in re.finditer(r"\\definecolor\{(\w+)\}\{HTML\}\{([0-9A-Fa-f]{6})\}", txt)}
    bad = [(k, v, found.get(k)) for k, v in LATEX_NAMES.items() if found.get(k, "").upper() != v.upper()]
    for k, v, got in bad:
        print(f"MISMATCH {k}: figstyle {v} vs sty {got}")
    print(f"checked {len(LATEX_NAMES)} colors against {path}: {'OK' if not bad else 'FAIL'}")
    return 0 if not bad else 1


def swatch(path):
    apply()
    fig, ax = figure(height=2.0)
    ax.axis("off")
    for i, (k, c) in enumerate(CONCEPT.items()):
        x, y = (i % 5) * 0.2, 1 - (i // 5) * 0.5
        ax.add_patch(plt.Rectangle((x, y - 0.25), 0.05, 0.2, color=c, transform=ax.transAxes))
        ax.text(x + 0.06, y - 0.15, f"{k}\n{c}", transform=ax.transAxes, fontsize=FS["small"], va="center")
    fig.savefig(path, metadata={"CreationDate": None})
    print(f"wrote {path}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-sty")
    ap.add_argument("--swatch")
    a = ap.parse_args()
    rc = 0
    if a.check_sty:
        rc |= check_sty(a.check_sty)
    if a.swatch:
        swatch(a.swatch)
    sys.exit(rc)
