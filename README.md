# Citation Equity: the WWW 2027 demo paper and its evidence

This repo holds the demo-track paper for The Web Conference 2027 (WWW '27), "Citation Equity: A Writing Tool for AI Search That Tests Its Own Advice", together with every result it reports. The paper is a working draft: blue `[OWNER: ...]` marks in the PDF are decisions still open.

- **The tool, live:** https://shehral.github.io/citation-equity/
- **The tool's code:** https://github.com/shehral/citation-equity (the experiments' code and pipeline READMEs are under `experiments/`)
- **The paper:** `main_www.pdf` (4 pages including references, the venue's limit)
- **Demo video (unlisted):** https://youtu.be/kbU9t3ewVUk
- **Plan to submission (Nov 16 AoE):** `notes/REDESIGN-AND-E5-PLAN-2026-10-27.md` (redesign, the E5 plan, week by week)

## Working on it together

- Make changes on a branch and open a pull request against `main`, so `build.sh` and `results/verify_numbers.py` can be run before merging. Small text fixes can go straight to `main`.
- After any edit, run `bash build.sh` (it fails on more than 4 pages) and `.venv/bin/python -I -B results/verify_numbers.py`.
- **Second rater:** if you are rating the evidence (`notes/second-rater/`), do it before opening `data/grades.json`, `data/evidence_matrix.csv`, `data/evidence_grades_loose.json` or Figure 3, so the rating stays blind.

## Build the PDF

```sh
bash build.sh            # regenerate the figures from data/, then compile main_www.tex with tectonic
bash build.sh --derive   # first rebuild data/ from a checkout of the tool repo next to this one (read only)
```

You need [tectonic](https://tectonic-typesetting.github.io/) (the build calls `/opt/homebrew/bin/tectonic`; edit `TECTONIC` in `build.sh` if yours is elsewhere), `pdfinfo` (poppler), and a Python 3.12 virtualenv at `.venv/` with matplotlib and numpy (`python3 -m venv .venv && .venv/bin/pip install matplotlib numpy`). The build fails on undefined references, overfull boxes, or more than 4 pages.

## What is where

| Path | What it holds |
|---|---|
| `main_www.tex`, `sections/` | The paper. Every number in the LaTeX carries a `% src:` comment naming its source. |
| `figures/` | Figure PDFs, rebuilt by `build.sh` from `data/` (`scripts/fig_*.py`). |
| `data/` | Small derived tables behind the figures and the prose, each with its producer and the sha256 of its inputs (see `data/README.md`). |
| `results/` | The reproducibility package: plans, every experiment's results, the cluster jobs and GPU-hours, software and model versions, and hashes of the withheld data. Start with `results/README.md`, which maps each section and figure to its results file. |
| `scripts/` | Derive scripts (`derive_*.py`), figure scripts (`fig_*.py`), and `build_results.py`, which writes `results/`. |
| `notes/` | Working notes: outline, narrative, cuts made to fit 4 pages, claim checks, simulated reviews, status. Drafting aids, not part of the submission. |
| `STYLE.md`, `smpreprint.sty`, `references.bib` | Writing rules, the shared style package, the bibliography. |

## Data we do not share

The experiments edit real web pages from GEO-bench and C-SEO Bench. Those pages belong to third parties, so this repo holds only aggregate results, per-answer scores and sha256 hashes: no page text, edited pages, prompts, editor logs or raw model answers. `results/README.md` explains what is withheld and how to regenerate it from the tool repo's pipeline.

## Data on Hugging Face

- [Shehral/citation-equity-experiments](https://huggingface.co/datasets/Shehral/citation-equity-experiments): every result and score, page metadata and hashes, and the plans (public, no page text).
- [Shehral/citation-equity-experiments-pages](https://huggingface.co/datasets/Shehral/citation-equity-experiments-pages): the fetched pages, edited versions, judge prompts and answers (gated, non-commercial research only).

`results/` in this repo is the same evidence in the form the paper's checks read (`results/verify_numbers.py`).
