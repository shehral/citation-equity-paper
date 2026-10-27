#!/usr/bin/env python3
"""Recompute the paper's E1, E2 and E3 headline contrasts from the cells alone and check them.

What it does
  (a) Recomputes every headline contrast from results/*/cells.jsonl (or cells.jsonl.gz) and nothing
      else: for each query with a cell of the arm and of its reference for every judge (and no cell
      below 4 valid answers), d_q = mean over the two judges of (arm score - reference score); the
      contrast is the mean of d_q over those queries, and n is their count. This is E1's
      query_differences (CE experiments/e1/analyze.py), with one assumption: a cell exists only for
      an applicable, valid version (true of these files; the analysis JSONs agree to 1e-9 below).
  (b) Checks each recomputed (d, n) against the analysis JSON in results/ (e1/analysis.json,
      e2/analysis_e2.json, e3/pooled/analysis_e3.json) to within 1e-9, and against the paper's
      data/e1_results.json, which the figures and prose are built from.
  (c) Reads the rendered prose of sections/*.tex (comments, \\owner marks and \\Description text
      removed) and checks every printed number of these contrasts: d and n against the recomputed
      values (printed to 3 decimals), intervals, Holm p and labels against the analysis JSONs (which
      hold the bootstrap and sign-flip results; those are not recomputed here). A sentence the
      script cannot find counts as a mismatch, so a rewrite of a sentence shows up instead of
      passing silently.

How the cells are pooled
  E1        results/e1/cells.jsonl, set main (80 GEO-bench queries) or replication (60 C-SEO Bench).
  E2a       E1's cells for the original and arm 9, results/e2/a cells for 9W and 9P, per set.
  E2b       results/e2/b cells only (editor Qwen3.8-27B; judges Gemma-4-12B and Qwen3.5-9B).
  E3 pooled sets main, e3 and e3-four only (never the C-SEO replication set): E1's main-set cells,
            minus each (query, arm) that E3 edited again, plus results/e3/retry cells (the extra
            attempt on E1's failed pairs) and results/e3/new cells (180 new queries).

Usage (from the repo root)
  .venv/bin/python -I results/verify_numbers.py            # table; exit 1 on any mismatch
  .venv/bin/python -I results/verify_numbers.py --claims results/CLAIMS.md
                                                           # also rewrite the claims list
Standard library only; numpy is used for the means when it is installed (results agree either way).
"""

from __future__ import annotations

import argparse
import gzip
import json
import re
import sys
from pathlib import Path

try:
    import numpy as np
except ImportError:  # pragma: no cover
    np = None

RESULTS = Path(__file__).resolve().parent
ROOT = RESULTS.parent
TOL = 1e-9
E1_JUDGES = ("gemma-4-12b", "qwen3.8-27b")
E2B_JUDGES = ("gemma-4-12b", "qwen3.5-9b")
E3_SETS = ("main", "e3", "e3-four")
E3_ARMS = {"original", "2", "4", "5", "6", "7", "8", "10", "P2", "P5", "P6", "P7", "P8", "P10"}


def mean(xs):
    xs = list(xs)
    if not xs:
        return None
    if np is not None:
        return float(np.mean(xs))
    return sum(xs) / len(xs)


# ---------------------------------------------------------------- cells


def read_cells(rel: str) -> list[dict]:
    path = RESULTS / rel
    gz = path.with_name(path.name + ".gz")
    if path.exists():
        text = path.read_text(encoding="utf-8")
    elif gz.exists():
        text = gzip.decompress(gz.read_bytes()).decode("utf-8")
    else:
        raise SystemExit(f"verify_numbers: missing results/{rel} (or .gz)")
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def load_pools() -> dict[str, list[dict]]:
    e1 = read_cells("e1/cells.jsonl")
    e2a = read_cells("e2/a/cells.jsonl")
    e2b = read_cells("e2/b/cells.jsonl")
    new = read_cells("e3/new/cells.jsonl")
    retry = read_cells("e3/retry/cells.jsonl")
    pools = {}
    for s in ("main", "replication"):
        pools[f"e1:{s}"] = [c for c in e1 if c["set"] == s]
        pools[f"e2a:{s}"] = ([c for c in e1 if c["set"] == s and c["arm"] in ("original", "9")]
                             + [c for c in e2a if c["set"] == s and c["arm"] in ("9W", "9P")])
    pools["e2b"] = [c for c in e2b if c["set"] == "main"]
    # E3: E1's cells for the pairs valid in E1 (a cell exists only for a valid version), E3's retry cells
    # (E1's failed pairs, edited again) and E3's new cells. As in CE experiments/e3/analyze_e3.py
    # with_retries(), a retried (query, arm) replaces any E1 row for it; for these files no retried pair
    # has an E1 cell, which is checked and printed below.
    redone = {(c["query_id"], c["arm"]) for c in retry}
    e1_main_all = [c for c in e1 if c["set"] == "main" and c["arm"] in E3_ARMS]
    e1_main = [c for c in e1_main_all if (c["query_id"], c["arm"]) not in redone]
    retry_main = [c for c in retry if c["set"] == "main" and c["arm"] in E3_ARMS]
    new_e3 = [c for c in new if c["set"] in ("e3", "e3-four") and c["arm"] in E3_ARMS]
    pools["e3"] = e1_main + retry_main + new_e3
    assert all(c["set"] in E3_SETS for c in pools["e3"]), "E3 pool must hold sets main, e3, e3-four only"
    pools["_e3_parts"] = {"e1 cells": len(e1_main), "e1 cells displaced by a retry": len(e1_main_all) - len(e1_main),
                          "retry cells": len(retry_main), "new cells": len(new_e3),
                          "retry pairs": len(redone),
                          "sets": sorted({c["set"] for c in pools["e3"]})}
    return pools


def contrast(cells: list[dict], arm: str, ref: str, judges) -> dict:
    """E1's d_q and its mean over queries, from cells only."""
    ix = {(c["query_id"], c["arm"], c["judge"]): c for c in cells}
    queries = sorted({c["query_id"] for c in cells})
    d, dropped = {}, 0
    for q in queries:
        pairs = [(ix.get((q, arm, j)), ix.get((q, ref, j))) for j in judges]
        if any(a is None or r is None for a, r in pairs):
            continue
        if any(a["dropped"] or r["dropped"] for a, r in pairs):
            dropped += 1
            continue
        d[q] = mean(float(a["score"]) - float(r["score"]) for a, r in pairs)
    return {"n": len(d), "d": mean(d.values()), "dropped": dropped, "d_q": d}


# ---------------------------------------------------------------- the contrasts

# id, experiment, pool, arm, ref, judges, what the paper calls it, the label the paper gives (prefix of
# the analysis label; None = the paper states no label).
CONTRASTS = [
    ("E1.main.9-original", "E1 main", "e1:main", "9", "original", E1_JUDGES, "question-headed section", "helps"),
    ("E1.main.12-P12", "E1 main", "e1:main", "12", "P12", E1_JUDGES, "question words in title and lead", "helps"),
    ("E1.main.ALL-P_ALL", "E1 main", "e1:main", "ALL", "P_ALL", E1_JUDGES, "all fixes vs paraphrase", "helps"),
    ("E1.main.ALL-original", "E1 main", "e1:main", "ALL", "original", E1_JUDGES, "all fixes vs original", "helps"),
    ("E1.main.3-P3", "E1 main", "e1:main", "3", "P3", E1_JUDGES, "lists", "no effect larger than"),
    ("E1.rep.9-original", "E1 replication", "e1:replication", "9", "original", E1_JUDGES,
     "question-headed section", "helps"),
    ("E1.rep.ALL-P_ALL", "E1 replication", "e1:replication", "ALL", "P_ALL", E1_JUDGES,
     "all fixes vs paraphrase", "helps"),
    ("E2a.main.9-9W", "E2a main", "e2a:main", "9", "9W", E1_JUDGES, "heading vs same text plain",
     "no effect larger than"),
    ("E2a.main.9-9P", "E2a main", "e2a:main", "9", "9P", E1_JUDGES, "heading vs heading without query words",
     "inconclusive"),
    ("E2a.main.9W-original", "E2a main", "e2a:main", "9W", "original", E1_JUDGES, "plain question vs original",
     "reported without a verdict"),
    ("E2a.rep.9-9W", "E2a replication", "e2a:replication", "9", "9W", E1_JUDGES, "heading vs same text plain",
     "no effect larger than"),
    ("E2a.rep.9-9P", "E2a replication", "e2a:replication", "9", "9P", E1_JUDGES,
     "heading vs heading without query words", "helps"),
    ("E2a.rep.9W-original", "E2a replication", "e2a:replication", "9W", "original", E1_JUDGES,
     "plain question vs original", "reported without a verdict"),
    ("E2b.12-P12", "E2b", "e2b", "12", "P12", E2B_JUDGES, "question words in title and lead", "stands"),
    ("E2b.ALL-P_ALL", "E2b", "e2b", "ALL", "P_ALL", E2B_JUDGES, "all fixes vs paraphrase", "stands"),
    ("E3.2-P2", "E3 pooled", "e3", "2", "P2", E1_JUDGES, "question headings", "no effect larger than"),
    ("E3.6-P6", "E3 pooled", "e3", "6", "P6", E1_JUDGES, "attributed quotes", "inconclusive"),
    ("E3.7-P7", "E3 pooled", "e3", "7", "P7", E1_JUDGES, "cited sources", "no effect larger than"),
    ("E3.8-P8", "E3 pooled", "e3", "8", "P8", E1_JUDGES, "direct-answer lead", "no effect larger than"),
    ("E3.4-original", "E3 pooled", "e3", "4", "original", E1_JUDGES, "tables (too few)", "insufficient n"),
    ("E3.5-P5", "E3 pooled", "e3", "5", "P5", E1_JUDGES, "statistics (too few)", "insufficient n"),
    ("E3.10-P10", "E3 pooled", "e3", "10", "P10", E1_JUDGES, "comparisons (too few)", "insufficient n"),
]


def _find(rows, arm, ref):
    for r in rows:
        if r.get("arm") == arm and r.get("ref") == ref:
            return r
    return None


def load_json(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def analysis_row(cid: str, arm: str, ref: str, A: dict) -> tuple[dict | None, str]:
    """The contrast's row in results/'s analysis JSON, and where it was found."""
    exp, part = cid.split(".")[0], cid.split(".")[1]
    if exp == "E1":
        s = "main" if part == "main" else "replication"
        return _find(A["e1"][s]["contrasts"], arm, ref) or _find(A["e1"][s]["vs_original"], arm, ref), \
            f"e1/analysis.json {s}"
    if exp == "E2a":
        s = "main" if part == "main" else "replication"
        blk = A["e2"]["e2a"][s]
        return _find(blk["planned"], arm, ref) or _find(blk["reported"], arm, ref), f"e2/analysis_e2.json e2a.{s}"
    if exp == "E2b":
        blk = A["e2"]["e2b"]
        return _find(blk["contrasts"], arm, ref) or _find(blk["reported"], arm, ref), "e2/analysis_e2.json e2b"
    return _find(A["e3"]["contrasts"], arm, ref), "e3/pooled/analysis_e3.json"


def paper_row(cid: str, arm: str, ref: str, P: dict) -> dict | None:
    """The contrast's row in data/e1_results.json (field 'd' holds the mean)."""
    exp, part = cid.split(".")[0], cid.split(".")[1]
    if exp == "E1":
        return _find(P["main" if part == "main" else "replication"]["contrasts"], arm, ref)
    if exp == "E2a":
        blk = P["e2"]["e2a"]["main" if part == "main" else "replication"]
        return _find(blk["planned"], arm, ref) or _find(blk["reported"], arm, ref)
    if exp == "E2b":
        blk = P["e2"]["e2b"]
        return _find(blk["contrasts"], arm, ref) or _find(blk.get("reported", []), arm, ref)
    return _find(P["e3"]["contrasts"], arm, ref)


def close(a, b) -> bool:
    if a is None or b is None:
        return a is None and b is None
    return abs(float(a) - float(b)) <= TOL


# ---------------------------------------------------------------- the paper's prose

def strip_comment(line: str) -> str:
    return re.sub(r"(?<!\\)%.*$", "", line)


def _drop_braced(text: str, macro: str) -> str:
    """Remove \\macro{...} with nested braces."""
    out, i, key = [], 0, "\\" + macro + "{"
    while True:
        j = text.find(key, i)
        if j < 0:
            out.append(text[i:])
            return "".join(out)
        out.append(text[i:j])
        depth, k = 0, j + len(key) - 1
        while k < len(text):
            depth += {"{": 1, "}": -1}.get(text[k], 0)
            k += 1
            if depth == 0:
                break
        i = k


def prose_lines(path: Path, captions_only: bool = False):
    """(line number, rendered text without comments) for each prose line of a .tex file."""
    in_caption = False
    lines = path.read_text(encoding="utf-8").splitlines()
    for no, raw in enumerate(lines, 1):
        text = strip_comment(raw).strip()
        if captions_only:
            if "\\caption{" in text:
                in_caption = True
            if not in_caption:
                continue
            if "\\label{" in text:
                in_caption = False
                text = text.split("\\label{")[0]
        if not text or text.startswith(("\\Description", "\\providecommand", "\\includegraphics", "\\input")):
            continue
        text = _drop_braced(text, "owner")
        yield no, text


def _src_block(lines: list[str], start: int, end: int) -> tuple[str, int | None]:
    parts, first, keep = [], None, False
    for k in range(start, end + 1):
        t = lines[k].strip()
        if t.startswith("% src"):
            keep = True
            first = first or k + 1
            parts.append(t[1:].strip())
        elif keep and re.match(r"%\s{2,}\S", t):
            parts.append(t[1:].strip())
        else:
            keep = False
    return " ".join(parts), first


def src_for(lines: list[str], no: int) -> tuple[str, int | None, str]:
    """The '% src' lines (with their indented continuations) that cover line `no` (1-based): those of the
    comment block directly above it ("above"), else of the nearest block above that holds one
    ("inherited"), else of the next block below ("below"); with the block's first src line."""
    i = no - 2
    adjacent = True
    while i >= 0:
        if not lines[i].strip().startswith("%"):
            adjacent = False
            i -= 1
            continue
        start = i
        while start > 0 and lines[start - 1].strip().startswith("%"):
            start -= 1
        text, first = _src_block(lines, start, i)
        if text:
            return text, first, "above" if adjacent else "inherited"
        adjacent = False
        i = start - 1
    j = no
    while j < len(lines):
        if lines[j].strip().startswith("%"):
            end = j
            while end + 1 < len(lines) and lines[end + 1].strip().startswith("%"):
                end += 1
            text, first = _src_block(lines, j, end)
            if text:
                return text, first, "below"
            j = end + 1
        else:
            j += 1
    return "", None, "none"


S = r"\$(?P<{}>[+-]\d+\.\d+)\$"  # a signed number in math mode, e.g. $+0.027$
N = r"\$n = (?P<{}>\d+)\$"


def g(name):
    return S.format(name)


def gn(name):
    return N.format(name)


# Each anchor: (file, regex over the rendered line, {group: (contrast id or count key, field)}).
# field: d / n (recomputed), lo / hi / holm / label (analysis JSON), approx (|d - value| <= 0.01).
ANCHORS = [
    ("sections/evidence.tex",
     r"a section headed by the question \(" + g("d") + r", 95\\% CI \$\[(?P<lo>[+-][\d.]+), (?P<hi>[+-][\d.]+)\]\$,"
     r" Holm \$p = (?P<holm>[\d.]+)\$; replication " + g("rep") + r"\)",
     {"d": ("E1.main.9-original", "d"), "lo": ("E1.main.9-original", "lo"), "hi": ("E1.main.9-original", "hi"),
      "holm": ("E1.main.9-original", "holm"), "rep": ("E1.rep.9-original", "d")}),
    ("sections/evidence.tex", r"missing words in title and lead \(" + g("d") + r"\)",
     {"d": ("E1.main.12-P12", "d")}),
    ("sections/evidence.tex", r"set as plain \(" + g("w") + r"; replication " + g("wr") + r"\)",
     {"w": ("E2a.main.9-9W", "d"), "wr": ("E2a.rep.9-9W", "d")}),
    ("sections/evidence.tex", r"scored higher than the untouched page \(" + g("m") + r"; " + g("r") + r"\)",
     {"m": ("E2a.main.9W-original", "d"), "r": ("E2a.rep.9W-original", "d")}),
    ("sections/evidence.tex",
     r"reader's-words gain kept its sign \(" + g("d12") + ", " + gn("n12") + r"\), as did all fixes together \("
     + g("dall") + ", " + gn("nall") + r"\)",
     {"d12": ("E2b.12-P12", "d"), "n12": ("E2b.12-P12", "n"), "dall": ("E2b.ALL-P_ALL", "d"),
      "nall": ("E2b.ALL-P_ALL", "n")}),
    ("sections/evidence.tex", r"added (?P<new>\d+) queries for the checks with too few pages: over (?P<pool>\d+),",
     {"new": ("q:e3.new", "n"), "pool": ("q:e3.pooled", "n")}),
    ("sections/evidence.tex", r"real pages \((?P<q>\d+) informational GEO-bench queries",
     {"q": ("q:e1.main", "n")}),
    ("sections/evidence.tex", r"replicated on (?P<q>\d+) from C-SEO Bench~\\cite\{puerto2025cseo\}",
     {"q": ("q:e1.replication", "n")}),
    ("sections/conclusion.tex", r"the one-change tests (?P<q>\d+) English queries",
     {"q": ("q:all", "n")}),
    ("sections/abstract.tex", r"clearly raised citation, by about (?P<a>0\.\d+) on a 0-to-1 scale",
     {"a": ("E1.main.9-original|E1.main.12-P12|E2a.main.9W-original", "approx")}),
    ("sections/intro.tex", r"clearly helped, by about (?P<a>0\.\d+) on a 0-to-1 citation score",
     {"a": ("E1.main.9-original|E1.main.12-P12|E2a.main.9W-original", "approx")}),
]

# Label claims the prose makes in words (checked against the analysis JSON labels).
LABEL_ANCHORS = [
    ("sections/abstract.tex", r"question headings, cited sources, direct answer first and lists showed no effect larger than 0\.03",
     ["E3.2-P2", "E3.7-P7", "E3.8-P8", "E1.main.3-P3"]),
    ("sections/abstract.tex", r"attributed quotes were inconclusive", ["E3.6-P6"]),
    ("sections/abstract.tex", r"kept its sign with another editor", ["E2b.12-P12", "E2b.ALL-P_ALL"]),
    ("sections/intro.tex", r"lists showed no effect larger than 0\.03 and attributed quotes were inconclusive",
     ["E3.2-P2", "E3.7-P7", "E3.8-P8", "E1.main.3-P3", "E3.6-P6"]),
    ("sections/evidence.tex", r"reader's-words gain kept its sign .* as did all fixes together", ["E2b.12-P12", "E2b.ALL-P_ALL"]),
    ("sections/evidence.tex", r"only the two that add the reader's own words near the top clearly raised the score",
     ["E1.main.9-original", "E1.main.12-P12"]),
    ("sections/evidence.tex", r"question heading did no better than the same text set as plain",
     ["E2a.main.9-9W", "E2a.rep.9-9W"]),
    ("sections/evidence.tex", r"showed no effect larger than 0\.03 and attributed quotes were inconclusive; tables, statistics and comparisons still had too few",
     ["E3.2-P2", "E3.7-P7", "E3.8-P8", "E3.6-P6", "E3.4-original", "E3.5-P5", "E3.10-P10"]),
    ("sections/evidence.tex", r"the heading form, sources and answer-first showed no effect larger than 0\.03; quotes were inconclusive",
     ["E2a.main.9-9W", "E2a.rep.9-9W", "E3.7-P7", "E3.8-P8", "E3.6-P6"]),
]

# Analysis settings the prose prints (the 0.03 equivalence margin, the 30-query minimum), checked in every
# analysis JSON: (regex with group v, settings key).
SETTING_ANCHORS = [
    (r"no effect larger than (?P<v>0\.\d+)", "delta"),
    (r"band: \$\\pm (?P<v>0\.\d+)\$", "delta"),
    (r"filled: (?P<v>\d+)\+ pages", "min_n"),
]


def fmt(x, kind="d") -> str:
    if x is None:
        return "-"
    if kind == "n":
        return str(int(x))
    if kind == "holm":
        return f"{x:.3f}"
    return f"{x:+.3f}"


# ---------------------------------------------------------------- claims list

NUM = re.compile(r"(?<![\w.])[+-]?\d+(?:\{,\}\d{3})*(?:\.\d+)?(?:\\%|%)?(?![\w])")
WORDS = ("two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen "
         "seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred").split()
WORD = re.compile(r"\b(" + "|".join(WORDS) + r")\b", re.IGNORECASE)
NAME = re.compile(r"\b[A-Za-z][A-Za-z]*(?:[-.:]?[A-Za-z0-9]+)*\d[A-Za-z0-9.:\-]*")


def render(text: str) -> str:
    for macro in ("url", "ref", "label", "href"):
        text = _drop_braced(text, macro)
    text = re.sub(r"\\cite(?:\[[^\]]*\])?\{[^}]*\}", "", text)
    text = re.sub(r"(Figures?|Section|Sec\.)~", r"\1 ", text)
    return text


def numbers_in(text: str) -> list[str]:
    t = render(text)
    t = NAME.sub(" ", t)  # model and tool names such as Qwen3.8-27B or llama3.2:3b are not numbers
    found = [m.group(0) for m in NUM.finditer(t)]
    found += [m.group(0) for m in WORD.finditer(t)]
    return found


def plain(text: str, limit: int = 200) -> str:
    t = render(text)
    t = re.sub(r"\\(emph|textbf|texttt|figtakeaway|panel|footnote|caption|paragraph|section|subsection)\{", "", t)
    t = t.replace("$", "").replace("\\%", "%").replace("{,}", ",").replace("~", " ").replace("\\,", " ")
    t = re.sub(r"\\times", "x", t)
    t = re.sub(r"\\pm ?", "+/-", t)
    t = re.sub(r"\\[A-Za-z]+", "", t).replace("{", "").replace("}", "")
    t = re.sub(r"\s+", " ", t).strip()
    return t if len(t) <= limit else t[: limit - 3].rstrip() + "..."


def write_claims(path: Path, verified: dict[tuple[str, int], list[str]]) -> int:
    files = [ROOT / "sections" / f for f in ("abstract.tex", "intro.tex", "system.tex", "evidence.tex",
                                               "related.tex", "demo.tex", "conclusion.tex")]
    out = [
        "# Every number in the rendered paper",
        "",
        "Written by `.venv/bin/python -I results/verify_numbers.py --claims results/CLAIMS.md`; rerun it after any",
        "edit to the text. One row per prose line or figure-caption line that prints a number, in reading order",
        "(abstract, Figure 1's caption, then Sections 1 to 7). Numbers spelled as words (two to twenty, and the",
        "tens) are listed too; \"one\" is not, nor are model names (Qwen3.8-27B), `\\owner` marks, alt text",
        "(`\\Description`), URLs and citation keys. The text column is the rendered sentence, shortened.",
        "",
        "**src** is the `% src:` comment that covers the line, by its line number in the same file: *above* is the",
        "comment block directly above the line, *inherited* the nearest src block further up (it covers the whole",
        "paragraph), *below* the block right after the line. \"same as line N\" repeats the previous row's src.",
        "Each src names its results file; `results/README.md` maps the paper's sections to `results/`.",
        "",
        "**check**: \"verified by verify_numbers.py\" lists the numbers on that line that the script recomputes from",
        "`results/*/cells.jsonl` (contrast d and n, query counts) or checks against the analysis JSONs (95%",
        "intervals, Holm p) and data/e1_results.json; \"labels\" marks a verdict stated in words (no effect larger",
        "than 0.03, inconclusive, kept its sign) that the script checks against the analysis labels. Unmarked",
        "numbers (the sensitivity test, the system, the literature) are checked by their src only.",
        "",
    ]
    rows = 0
    order = [files[0], ROOT / "main_www.tex"] + files[1:]
    for f in order:
        captions = f.name == "main_www.tex"
        lines = f.read_text(encoding="utf-8").splitlines()
        rel = f.relative_to(ROOT).as_posix()
        block = []
        for no, text in prose_lines(f, captions_only=captions):
            nums = numbers_in(text)
            if not nums:
                continue
            src, src_line, how = src_for(lines, no)
            vals = verified.get((rel, no))
            mark = ""
            if vals is not None:
                shown = [v for v in vals if v != "labels"]
                mark = "verified by verify_numbers.py" + (": " + ", ".join(shown) if shown else "")
                if "labels" in vals:
                    mark += ("; " if shown else ": ") + "labels"
            block.append((no, nums, plain(text), src, src_line, how, mark))
        if not block:
            continue
        out += [f"## {rel}" + (" (figure captions)" if captions else ""), "",
                "| line | numbers | text (rendered, shortened) | src | check |", "|---|---|---|---|---|"]
        prev = None
        for no, nums, txt, src, src_line, how, mark in block:
            nums_s = ", ".join(n.replace("{,}", ",").replace("\\%", "%") for n in nums)
            if not src:
                src_s = "none"
            elif prev is not None and prev[0] == src_line:
                src_s = f"same as line {prev[1]}"
            else:
                src_s = f"line {src_line} ({how}): {src}"
            prev = (src_line, no)
            out.append(f"| {no} | {nums_s} | {txt.replace('|', '/')} | {src_s.replace('|', '/')} | {mark} |")
            rows += 1
        out.append("")
    text = "\n".join(out) + "\n"
    text = text.replace("\u2014", ", ")
    path.write_text(text, encoding="utf-8")
    return rows


# ---------------------------------------------------------------- main


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--claims", help="also write the list of every number in the paper to this path")
    args = ap.parse_args(argv)

    pools = load_pools()
    parts = pools.pop("_e3_parts")
    A = {"e1": load_json("results/e1/analysis.json"), "e2": load_json("results/e2/analysis_e2.json"),
         "e3": load_json("results/e3/pooled/analysis_e3.json")}
    P = load_json("data/e1_results.json")
    problems: list[str] = []

    # (a) recompute, (b) compare with the analysis JSONs and data/e1_results.json
    R = {}
    print("verify_numbers: E1, E2 and E3 headline contrasts recomputed from results/*/cells.jsonl")
    print("d = mean over queries of the per-query mean over two judges of (arm score - reference score)")
    print("E3 pool: " + ", ".join(f"{k} {v}" for k, v in parts.items()))
    if parts["e1 cells displaced by a retry"]:
        problems.append(f"E3 pool: {parts['e1 cells displaced by a retry']} E1 cells exist for retried pairs "
                        "(a retry should only redo pairs that failed in E1)")
    print()
    hdr = f"{'contrast':<22} {'what':<40} {'n':>3} {'d (cells)':>11} {'analysis':>9} {'e1_results':>10}  label (analysis)"
    print(hdr)
    print("-" * len(hdr))
    for cid, exp, pool, arm, ref, judges, what, paper_label in CONTRASTS:
        r = contrast(pools[pool], arm, ref, judges)
        a, where = analysis_row(cid, arm, ref, A)
        p = paper_row(cid, arm, ref, P)
        ok_a = a is not None and a["n"] == r["n"] and close(a["mean_d"], r["d"])
        ok_p = p is not None and p["n"] == r["n"] and close(p["d"], r["d"])
        if not ok_a:
            problems.append(f"{cid}: cells give n={r['n']} d={r['d']!r}, {where} gives "
                            f"{None if a is None else (a['n'], a['mean_d'])}")
        if not ok_p:
            problems.append(f"{cid}: cells give n={r['n']} d={r['d']!r}, data/e1_results.json gives "
                            f"{None if p is None else (p['n'], p['d'])}")
        label = a.get("label") if a else None
        if paper_label and not (label or "").startswith(paper_label):
            problems.append(f"{cid}: the paper calls it '{paper_label}', {where} labels it '{label}'")
        if p is not None and a is not None and p.get("label") != label:
            problems.append(f"{cid}: label '{p.get('label')}' in data/e1_results.json, '{label}' in {where}")
        R[cid] = {"n": r["n"], "d": r["d"], "a": a, "label": label}
        print(f"{cid:<22} {what:<40} {r['n']:>3} {r['d'] if r['d'] is not None else float('nan'):>+11.6f} "
              f"{'match' if ok_a else 'DIFFERS':>9} {'match' if ok_p else 'DIFFERS':>10}  {label}")

    # E2b's "kept E1's sign": the E1 d it compares with is E1's own cells for the same contrast
    for cid, e1id in (("E2b.12-P12", "E1.main.12-P12"), ("E2b.ALL-P_ALL", "E1.main.ALL-P_ALL")):
        a = R[cid]["a"]
        if not (a["e1_n"] == R[e1id]["n"] and close(a["e1_mean_d"], R[e1id]["d"])):
            problems.append(f"{cid}: e1_mean_d/e1_n in the analysis differ from {e1id} recomputed")
        if not (R[cid]["d"] > 0) == (R[e1id]["d"] > 0):
            problems.append(f"{cid}: sign differs from {e1id}")

    # query counts
    def qcount(cells, sets):
        return len({c["query_id"] for c in cells if c["set"] in sets})
    Q = {"q:e1.main": qcount(pools["e1:main"], {"main"}),
         "q:e1.replication": qcount(pools["e1:replication"], {"replication"}),
         "q:e3.new": qcount(pools["e3"], {"e3", "e3-four"}),
         "q:e3.pooled": qcount(pools["e3"], set(E3_SETS))}
    Q["q:all"] = Q["q:e3.pooled"] + Q["q:e1.replication"]
    expect_q = {"q:e1.main": A["e1"]["main"]["n_queries"], "q:e1.replication": A["e1"]["replication"]["n_queries"],
                "q:e3.new": A["e3"]["queries_by_part"]["new"], "q:e3.pooled": A["e3"]["n_queries"],
                "q:all": A["e3"]["n_queries"] + A["e1"]["replication"]["n_queries"]}
    print()
    print("queries with at least one cell: " + ", ".join(f"{k[2:]} {v}" for k, v in Q.items())
          + "  (analysis JSONs: " + ", ".join(f"{expect_q[k]}" for k in Q) + ")")
    for k, v in Q.items():
        if v != expect_q[k]:
            problems.append(f"{k}: {v} queries with cells, analysis JSON says {expect_q[k]}")

    # (c) the paper's prose
    print()
    print("Paper numbers for these contrasts (sections/*.tex, rendered text):")
    hdr2 = f"{'file:line':<26} {'contrast':<46} {'field':<6} {'paper':>8} {'expected':>8}  source of expected"
    print(hdr2)
    print("-" * len(hdr2))
    verified: dict[tuple[str, int], list[str]] = {}
    covered: set[tuple[str, int, str]] = set()
    prose_cache = {}
    for rel in sorted({a[0] for a in ANCHORS} | {a[0] for a in LABEL_ANCHORS}):
        prose_cache[rel] = list(prose_lines(ROOT / rel))
    for rel, rx, groups in ANCHORS:
        hits = [(no, m) for no, t in prose_cache[rel] for m in [re.search(rx, t)] if m]
        if not hits:
            problems.append(f"{rel}: sentence not found for /{rx[:60]}.../ (the text changed; update the anchor)")
            print(f"{rel:<26} {'(sentence not found)':<46}")
            continue
        for no, m in hits:
            for grp, (key, field) in groups.items():
                val = m.group(grp)
                covered.add((rel, no, val))
                verified.setdefault((rel, no), []).append(val)
                if key.startswith("q:"):
                    exp_s, why = str(Q[key]), "query count (cells)"
                elif field == "approx":
                    ds = [R[k]["d"] for k in key.split("|")]
                    ok = all(abs(x - float(val)) <= 0.01 for x in ds)
                    exp_s = "~" + val if ok else "/".join(fmt(x) for x in ds)
                    why = "within 0.01 of " + ", ".join(fmt(x) for x in ds)
                    if not ok:
                        problems.append(f"{rel}:{no}: 'about {val}' but the contrasts are {why}")
                    print(f"{rel + ':' + str(no):<26} {'about: ' + key.replace('|', ', '):<46} {field:<6} {val:>8} "
                          f"{exp_s:>8}  {why}")
                    continue
                elif field in ("d", "n"):
                    exp_s, why = fmt(R[key][field], field), "recomputed from cells"
                elif field in ("lo", "hi"):
                    ci = R[key]["a"]["ci95"]
                    exp_s, why = fmt(ci[0] if field == "lo" else ci[1]), "analysis JSON ci95"
                elif field == "holm":
                    exp_s, why = fmt(R[key]["a"]["p_holm"], "holm"), "analysis JSON p_holm"
                else:
                    raise ValueError(field)
                same = val == exp_s
                if not same:
                    problems.append(f"{rel}:{no}: {key} {field} printed {val}, expected {exp_s} ({why})")
                print(f"{rel + ':' + str(no):<26} {key:<46} {field:<6} {val:>8} {exp_s:>8}  "
                      f"{why}{'' if same else '  <-- MISMATCH'}")
    for rel, rx, keys in LABEL_ANCHORS:
        hits = [no for no, t in prose_cache[rel] if re.search(rx, t)]
        if not hits:
            problems.append(f"{rel}: sentence not found for /{rx[:60]}.../")
            continue
        for no in hits:
            verified.setdefault((rel, no), []).append("labels")
            labels = "; ".join(f"{k} '{R[k]['label']}'" for k in keys)
            print(f"{rel + ':' + str(no):<26} {'labels: ' + ', '.join(keys):<46} label  (words)  analysis labels: {labels}")

    settings = {"e1": A["e1"]["main"]["settings"], "e1 replication": A["e1"]["replication"]["settings"],
                "e2": A["e2"]["settings"], "e3": A["e3"]["settings"]}
    for f in sorted((ROOT / "sections").glob("*.tex")):
        rel = f.relative_to(ROOT).as_posix()
        for no, t in prose_lines(f):
            for rx, key in SETTING_ANCHORS:
                for m in re.finditer(rx, t):
                    val = m.group("v")
                    vals = {k: v[key] for k, v in settings.items()}
                    ok = all(float(v) == float(val) for v in vals.values())
                    covered.add((rel, no, val))
                    verified.setdefault((rel, no), []).append(val)
                    if not ok:
                        problems.append(f"{rel}:{no}: prints {key} {val}, analysis settings say {vals}")
                    print(f"{rel + ':' + str(no):<26} {'setting: ' + key:<46} {'set':<6} {val:>8} "
                          f"{'same' if ok else 'DIFFERS':>8}  settings.{key} in the e1, e2, e3 analysis JSONs")

    # signed numbers in the prose that no anchor covers (other results, e.g. the sensitivity test)
    print()
    print("Signed numbers in sections/*.tex prose not tied to an E1-E3 contrast (not checked here):")
    for f in sorted((ROOT / "sections").glob("*.tex")):
        rel = f.relative_to(ROOT).as_posix()
        for no, t in prose_lines(f):
            for m in re.finditer(r"\$([+-]\d+\.\d+)\$", t):
                if (rel, no, m.group(1)) not in covered:
                    print(f"  {rel}:{no} {m.group(1)}")

    if args.claims:
        path = Path(args.claims)
        path = path if path.is_absolute() else Path.cwd() / path
        rows = write_claims(path, verified)
        print()
        print(f"wrote {path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else path.name} ({rows} lines with numbers)")

    print()
    if problems:
        print(f"MISMATCHES: {len(problems)}")
        for p in problems:
            print("  " + p)
        return 1
    print("All recomputed contrasts match the analysis JSONs (1e-9) and data/e1_results.json, "
          "and every paper number for them matches.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
