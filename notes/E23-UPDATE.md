# E2 and E3 in the paper (2026-10-24)

Brief: `../citation-equity/.superpowers/sdd/2026-10-23-citation-equity/task-PAPERE23-brief.md`.
Sources (tool repo, read only): `experiments/RESULTS_E2.md` and `results/e2/analysis_e2.json` (CE c8e5fc6),
`experiments/RESULTS_E3.md` and `results/e3/analysis_e3.json` (CE 82aa8b3). Build: 4 pages (`bash build.sh`).

## Story now told
The tool's advice was tested one change at a time on real pages; only adding the reader's own words near the top
helped (about +0.03), and that held with another editor (Qwen3.8-27B) and other judges (Gemma-4-12B, Qwen3.5-9B);
structural edits (heading form, cited sources, direct answer first, lists) showed no effect larger than 0.03; the
tool now scores what helped and marks what did not.

## What changed
- `scripts/derive_e1_results.py`: also reads `analysis_e2.json` and `analysis_e3.json`; `data/e1_results.json`
  gains `e2` (E2a planned/reported per set, E2b) and `e3` (pooled contrasts), each with its own `_provenance`
  (source path, sha256, CE commit). The E1 blocks are byte-unchanged.
- `scripts/fig_e1.py` / `figures/fig4_e1.pdf`: rows 2, 4, 5, 6, 7, 8, 10 show the E3 pooled estimate (260 queries;
  no replication diamond, E3 has none); ALL, 9, 3, 1, 12, 11 stay E1; two indented E2a rows under arm 9 (renamed
  "Question-headed section"): "vs same text, plain" (9 minus 9W) and "vs heading w/o its words" (9 minus 9P), main
  set with the replication as a diamond. 16 rows, one column. Verdict "inconclusive" added to the label map.
- Figure 4 caption: takeaway first ("Only the reader's own words near the top raised citation; the heading form and
  other structural edits showed no effect larger than 0.03."); Description rewritten.
- Abstract: the E1 sentence replaced by the one-change-at-a-time result plus "held with another editor and other
  judges" and the structural nulls; new sentence "The tool now scores what helped and marks the rest as unscored
  notes."; "Both tests" -> "All tests".
- Intro: the per-suggestion sentence rewritten to the same story; contributions end "with tests of its advice one
  change at a time".
- Section 3: E1 paragraph trimmed; new run-in paragraph "The reader's words carry the gain, not the heading." with
  E2a, E2b and E3, planning stated once ("Two follow-up tests were each planned before their answers existed."), and
  the tool consequence stated as the rule's outcome (unscored notes: lists, question headings, cited sources,
  direct-answer lead; new scored check "Your reader's words up top"). Every number has a `% src:` comment.
- Limitations: "the per-suggestion tests 320 English queries, nearly all edited by one model family" (260 GEO-bench
  pooled + 60 C-SEO Bench; Qwen edits only in E2b).
- `% TODO scores after the tool update` added above the sample-score src comments (abstract, intro, Figure 1).
- Cuts 52 to 65 in `notes/CUTS.md`. Acknowledgments and AI-use statement untouched; all `\owner` marks kept.

## Not placed / open
- "temperature-0 regeneration mostly repeats": not stated in RESULTS_E3.md; only the editor's temperature 0
  (PREREG_E1.md line 85) and the small rescue counts are sourced. The sentence on the extra attempt was then cut
  for space (cut 61); the src comment keeps the evidence.
- E2a "reported without a verdict" rows 9P vs original (+0.010 main, -0.012 replication) are in data, not in text.
- The tool update is pending the owner's OK (see notes/STATUS.md).

## Review fixes (task-PAPERE23-review.md)
- Finding 1 (important): abstract, intro and Figure 4 takeaway now say the reader's words were the only change that *clearly* helped and that attributed quotes were inconclusive.
- Finding 2: "indented" removed from the Figure 4 caption and Description (the E2a rows are not indented; the caption now says `"vs" rows`); the query-count note now reads "260 queries for question headings and statistics to tables, 80 for the rest" (lists is an E1 row).
- Finding 3: Section 3 E2a paragraph heading "The reader's words carry the gain, not the heading." -> "The heading form adds nothing."; "beat a same-size heading" -> "outscored ... (a clear gain in the replication; inconclusive in the main set)"; 9W vs original "beat" -> "scored higher than" (no verdict in RESULTS_E2.md).
- Finding 4: abstract and intro "held with another editor and other judges" -> "kept its sign".
- Not changed: finding 5 (Section 2, "ten checks", sample scores and Figure 3 still describe the pre-update tool; waits on the owner's OK and the score update, see STATUS.md), finding 6 (question-headings CI touches the band edge; the label is the rule's), finding 7 (note only).
