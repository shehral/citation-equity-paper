# House style: arXiv preprint at the level of Anthropic's interpretability and alignment papers

This spec covers this paper and later ones. It implements two standing orders from the owner (2026-10-20). The first is an arXiv preprint whose diagrams, styling and aesthetics match Anthropic's interpretability and alignment papers, with a TMLR build kept switchable. The second is writing by Nanda's "Highly Opinionated Advice on How to Write ML Papers".

The implementation consists of:

- `paper/smpreprint.sty`: the LaTeX side.
- `paper/scripts/figstyle.py`: the matplotlib side.
- `paper/scripts/figdata.py`: read-only loaders for the result files.
- `paper/scripts/fig_*.py`: one script per figure.
- `paper/figures/fig1_schematic.tex`: the TikZ Figure 1 schematic.

## 1. What the exemplars taught (practices only; no asset copied)

The arXiv IDs and titles were verified on their abstract pages on 2026-10-21:

| Exemplar | ID | Verified |
|---|---|---|
| Alignment faking in large language models (Greenblatt et al.) | 2412.14093 | yes, 18 Dec 2024 |
| Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training (Hubinger et al.) | 2401.05566 | yes, 10 Jan 2024 |
| Auditing language models for hidden objectives (Marks et al.) | 2503.10965 | yes, 14 Mar 2025 |
| Constitutional Classifiers: Defending against Universal Jailbreaks across Thousands of Hours of Red Teaming (Sharma et al.) | 2501.18837 | yes, 31 Jan 2025 |
| On the Biology of a Large Language Model, transformer-circuits.pub/2025/attribution-graphs/biology.html | web | yes, 27 Mar 2025 |

Close reading covered the PDFs of Alignment Faking and Auditing (first pages and figure pages). The transformer-circuits page renders its figures in JavaScript, so its static HTML gave only the title, date and section list.

What these papers do, and what this style adopts:

- **Title block.**
  - The exemplars use an ICLR-derived template: title, then authors with affiliation symbols, emails in mono, then a centered "Abstract".
  - Adopted: a modern left-aligned variant. A sans title, then a byline (name and email on one line, affiliation below in a soft ink), then the date, then a hairline rule, then a letter-spaced ABSTRACT label.
- **Figure 1 is a schematic of the setup.**
  - Both papers open with a full-width diagram on page 2. It has a few rounded, light-grey panels; short bold stage labels above the columns; thin arrows; one colored highlight on the thing that matters; and a one-line outcome under each branch, set in the outcome's color.
  - Adopted: `fig1_schematic.tex` (three numbered stages, a tinted readout panel per measurement, the registered question between them), stacked over a headline panel generated from data.
- **Captions open with a bold takeaway sentence**, then say what is shown and how to read it. Examples: "**Claude 3 Opus fakes alignment when told it will be retrained ...**" and "**Blind auditing game structure.**".
  - Panel references are in the text: (a), (b), (left), (right).
  - Alignment Faking also highlights the color words of the legend inside the caption ("yellow for compliant ... blue for non-compliant").
  - Adopted: `\figtakeaway{}`, `\panel{}`, the inline key glyphs `\keydot` and the rest, and `\conceptmark{}`.
- **One meaning per color, everywhere.**
  - Auditing keeps red for the red team and blue for the blue teams in every figure and in the body text ("train biases" in blue, "test biases" in red).
  - Alignment Faking keeps one fill per behaviour across all bar panels (refuses, complies, alignment-faking reasoning).
  - Adopted: the concept map below.
- **Results plots.**
  - Left-aligned panel titles above the axes, sometimes colored to the concept.
  - Thin lines, light grids, shaded intervals, pastel fills for areas and saturated colors for marks.
  - Minimal spines; legends only when direct labels cannot work.
- **Findings up front.** The introduction carries a numbered list of findings with bold lead sentences. Adopted: the `keyfindings` box with a `findings` list, once, after the abstract.
- **Fonts.**
  - Both PDFs set Times for text. Alignment Faking uses matplotlib's default DejaVu Sans in figures; Auditing uses a proprietary brand sans in figures.
  - Not adopted: no Anthropic font, and no default DejaVu Sans either. One open sans (Lato) serves figures, captions, tables and headings, so figure text matches the caption beside it.
- **Transcript boxes.** The exemplars set model transcripts in mono boxes with colored highlights. This paper must not show prompt, completion or judge text from the study data, so no transcript box exists.

## 2. Palette and concept map

The palette is Okabe and Ito (2008), which is colorblind-safe. The key contrast (regressed against intact) is vermillion against blue, carried redundantly by shape (circle against square). Red against green is never a key contrast.

| Concept | Hex | LaTeX color | `figstyle.CONCEPT` key | Marks |
|---|---|---|---|---|
| base model (reference) | `#1A1A1A` | `smBase` | `base` | small black dot or tick; `+` for the base-vs-base control |
| derivative with a confirmed regression | `#D55E00` vermillion | `smRegressed` | `regressed` | filled circle; open circle = flagged by the primary reader only |
| derivative not flagged (within the margin, intact) | `#0072B2` blue | `smIntact` | `intact` | filled square |
| refusal direction; harm direction | `#009E73` bluish green | `smRefusal`, `smHarm` | `refusal`, `harm` | monitor readouts; recall |
| persona vectors | `#CC79A7` reddish purple | `smPersona` | `persona` | |
| decision probe | `#E69F00` orange | `smProbe` | `probe` | |
| behavioral canary | `#56B4E9` sky blue | `smCanary` | `canary` | |
| readers without white-box access (first-word reader, prompt-only classifier); demoted proxies (first-token margin) | `#8C8C8C` grey | `smBaseline` | `baseline` | dashed lines, open markers |
| behavioral judges | `#4A5A6E` slate | `smJudge` | `judge` | WildGuard solid or filled; J1 dashed or open |

The neutrals are:

- `smInk` `#1A1A1A`: text.
- `smInkSoft` `#5C5C5C`: axes, ticks and secondary text.
- `smRule` `#BFC5CC`: reference lines and box rules.
- `smGrid` `#E6E6E6`: grid lines.
- `smTint` `#F3F5F7`: box fill.
- `smAccent` `#2F3B4C`: box titles and the schematic's stage labels. It is not a data concept.
- `smLink` `#2B4F7A`: quiet links (`blue!50!black` in the TMLR build).
- `smOwner` `#0000FF`: owner marks.

The raw Okabe-Ito slots are `smOIBlack`, `smOIOrange`, `smOISkyBlue`, `smOIGreen`, `smOIYellow`, `smOIBlue`, `smOIVermillion` and `smOIPurple`.

Rules:

- Use a concept's hue for its marks. Text in a concept color goes through `figstyle.text_color()`, which darkens it to a 4.5:1 contrast.
- Fills in schematics use tints, `<color>!14` to `!16`.
- Several units of one status (for example three regressed units) share the hue and differ in lightness (`tint`, `shade`) and marker shape.
- Sequential data use `figstyle.seq_cmap(concept)`, white to the color. Signed data whose zero is meaningful use `figstyle.div_cmap()` with `centered_norm()`, which is white at zero.
- `python -I paper/scripts/figstyle.py --check-sty paper/smpreprint.sty` fails if the .sty and figstyle disagree on any of the 25 hexes.

## 3. Fonts and packages

| Role | Font | Source (tectonic bundle, loaded by file name) |
|---|---|---|
| body text | XCharter (Roman, Italic, Bold, BoldItalic, Slanted) | `xcharter`: `XCharter-*.otf` |
| math | XCharter Math, through `unicode-math` | `xcharter-math`: `XCharter-Math.otf` |
| headings, captions, tables, boxes, figure text, schematic | Lato (Regular, Italic, Semibold, Bold), `Scale=MatchLowercase` | `lato`: `Lato-*.ttf` |
| code, paths, model ids | Inconsolata (zi4), `Scale=MatchLowercase` | `inconsolata`: `Inconsolatazi4-*.otf` |

- **Why Lato, not Source Sans.** The bundle ships Source Sans Pro only as CFF-flavoured OpenType. Matplotlib 3.11 embeds such a font with `pdf.fonttype 42` but marks it with the wrong font type: poppler reports "Mismatch between font type and embedded font file", and other viewers may fail. Lato is TrueType, so the same sans embeds cleanly in figures (CID TrueType) and in the text.
- **Why XCharter.** It has a matching math font in the bundle; Source Serif has none.
- **Never** use system font files or Anthropic's fonts. The macOS system has none of these families installed, so every font in the PDFs comes from the bundle. `pdffonts` should list only XCharter, Lato and Inconsolata in the arXiv build, all embedded, with no Type 3.
- **Packages (arXiv build).**
  - geometry, fontspec, unicode-math (after amsmath, amssymb and mathtools), natbib (author-year, with the same citestyle as `tmlr.sty`), caption, enumitem, etoolbox.
  - xcolor, tikz (with `arrows.meta`), tcolorbox (`skins`, `breakable`).
  - main.tex adds microtype, booktabs, tabularx, longtable, hyperref and cleveref.
- **Packages (TMLR build).** `tmlr.sty` unchanged (Latin Modern, its layout and title), plus the shared part of `smpreprint.sty` (`[tmlr]` option): colors, boxes, caption macros and keys. Nothing that changes layout.

## 4. Layout

- US letter, a 6.1 in measure (about 95 to 100 characters a line, close to the exemplars' density), top margin 1 in, page number only in the footer.
- 10 pt XCharter with `\linespread{1.08}`, block paragraphs (no indent, 6.5 pt between paragraphs) and a ragged bottom.
- Moderately tolerant line breaking: `\tolerance=1000`, `\emergencystretch=3em`. TMLR uses `\sloppy`.
- Headings are Lato bold, with the section number in the soft ink. `\paragraph` stays a run-in XCharter bold with a slightly stretchable gap.
- Tables in floats are set in Lato with tabular lining figures and a 4.5 pt column gap. A table that sets its own `\tabcolsep` keeps it, and longtables keep their own sizes. Booktabs rules only.
- Floats: top fraction 0.9, generous `\textfloatsep`.

## 5. Captions and boxes

- **Captions.**
  - Write every caption as `\caption{\figtakeaway{One sentence that states the takeaway.} What is shown. How to read it (keys). The conclusion or caveat.}`.
  - Table captions sit above the table and use `\tabtakeaway{}`.
  - Keys go inline, without a legend box: `\keydot{smRegressed}` confirmed regression, `\keyring{smRegressed}` primary reader only, `\keysquare{smIntact}` not flagged, `\keyline{smRefusal}` refusal direction, `\keydash{smBaseline}` demoted proxy.
  - Panels are referenced with `\panel{a}`.
  - Captions are self-contained: tier word (registered, pre-specified or post hoc), reader, n and what the error bars are.
- **Key findings.**
  - Use `\begin{keyfindings}\begin{findings}\item \textbf{Claim.} Evidence and tier. ...\end{findings}\end{keyfindings}` once, right after the abstract, with 3 to 5 items.
  - Each item is one sentence of claim plus its tier and its generated number macro.
  - It is a highlights reel of the narrative, not a second abstract.
- **Takeaway.** Use `\begin{takeaway}[Takeaway.] ... \end{takeaway}` at most once per section, for the sentence a skimming reader must not miss.
- **Owner marks.** `\owner{...}` is always blue and always visible. Never restyle it away.

## 6. Figure-script conventions

- **One script per figure,** `paper/scripts/fig_<name>.py`, writing `paper/figures/fig_<name>.pdf`.
  - Usage: `--root <repo root>` (inputs), `--out <figures dir>` (output), and `--png <dir>` for optional previews.
  - Run with `.venv/bin/python -I`. Each script adds its own directory to `sys.path`, because `-I` drops it.
- **Read, never type, a number.**
  - Every plotted value and every number printed in a panel comes from a result file through `figdata.py`. Panel AUROCs come from the aggregate's `hypotheses.json`, the floor from the bank's `delta_threshold`, the bar from `config.h2_auroc_threshold`, and layer indices from the JSON.
  - Formatting goes through `figstyle.fmt()`, which rounds like `paper_numbers.py`, so a figure shows the same digits as the prose macro.
  - A figure script never writes a number or table file.
- **One takeaway per figure.** Emphasize the key series and fade the rest: the key unit in full color, context units as thin tints, controls dashed.
- **Direct labels.**
  - Use `figstyle.label()` (white halo, colored text darkened for legibility) or `figstyle.place_labels()`. The latter is a greedy placer that avoids markers and earlier labels, with hairline leaders when pushed out of a cluster.
  - Labels on line charts are placed explicitly where the lines leave room.
  - Use a legend only for a set of encodings shared by many marks (status keys), placed inside an empty corner or as one row above the panels.
- **Sizes.**
  - Draw at the width the paper includes the figure at: `figstyle.TEXTWIDTH_IN` = 6.1 in for `width=\textwidth`, and 0.78 x 6.1 in for `0.78\textwidth`, so text prints at its true size: 7.5 pt base, 6.8 pt ticks, 8 pt semibold panel titles.
  - The TMLR build scales figures by 6.5/6.1.
  - A main-text figure must not grow taller than the one it replaces while TMLR's 12-page main text is binding.
- **Output.**
  - Vector PDF only, with fonts embedded as TrueType (`pdf.fonttype 42`).
  - No creation date: rerunning a script gives a byte-identical PDF.
  - Inputs and their SHA-256 are stamped in the PDF's Subject field.
- **Fonts for figures.** `figstyle.ensure_fonts()` copies Lato from the tectonic bundle (`tectonic -X bundle cat`) into `SM_FONT_CACHE` (default `paper/scripts/.fontcache/`, to be gitignored) and registers it. Without tectonic it stops rather than fall back to a system font.
- **Diagrams.**
  - Draw them in TikZ with the `sm*` colors and `\sffamily`, as `.tex` files under `paper/figures/` that are `\input` inside a figure.
  - Prefix TikZ style names with `sm` (built-in keys such as `step` clash).
  - Nested key glyphs reset `rounded corners` themselves.

Regenerate everything with `.venv/bin/python -I -B paper/scripts/fig_all.py`, which also runs the palette check. `-B` stops Python from writing bytecode caches; `-I` ignores `PYTHONDONTWRITEBYTECODE`. Use it whenever the interpreter belongs to a tree that must stay read-only.

## 7. Building both versions

From `paper/`:

```
/opt/homebrew/bin/tectonic --keep-logs main.tex        # arXiv preprint  -> main.pdf      (smpreprint.sty)
/opt/homebrew/bin/tectonic --keep-logs main_tmlr.tex   # TMLR submission -> main_tmlr.pdf (tmlr.sty, same text)
bash lint.sh                                           # must flag only the owner marks until the owner clears them
```

How the switch works:

- `main.tex` loads `smpreprint` unless `\SMtmlrbuild` is defined.
- `main_tmlr.tex` defines it, holds the owner's anonymous/preprint switch (`\preprinttrue` or `\preprintfalse`, an owner-mark comment) and `\input`s `main.tex`. Every word lives in `main.tex`.
- Never use pdflatex, xelatex or latexmk.

Checks before sharing:

- Both builds report 0 overfull boxes and 0 undefined references or citations (`grep -c Overfull *.log`).
- `pdffonts` shows every font embedded and no Type 3, in both PDFs and every figure PDF.
- `figstyle.py --check-sty` passes.
- In the TMLR build the main content (through Related Work, the last main section; the Conclusion was cut in v9) still ends on page 12.

## 8. Reusing this style in a new paper

1. Copy `smpreprint.sty`, `scripts/figstyle.py` and `figures/fig1_schematic.tex` (as a starting point only), plus this file.
2. Replace the concept map with the new paper's concepts in **both** `CONCEPT`/`LATEX_NAMES` (figstyle) and the `\definecolor` block (sty); run `--check-sty`.
3. Write a `figdata.py` for the new result files; keep the rule that figure scripts read numbers and never type them.
4. Keep the venue template switchable in the same way: a thin `main_<venue>.tex` that sets a flag and `\input`s `main.tex`.
