# Final polish (2026-10-26)

Scope: src pointers, number checks, a skeptical-reviewer pass with cheap fixes only, and the owner's five-author
byline. No restructuring, no new claims. `bash build.sh` and `bash build.sh --derive` both pass at **4 pages
including references**; no font, margin or spacing change. Cuts are logged in notes/CUTS.md (71 to 78).

Tool repo (CE, read only): feat head `c908431`. Public main `b10887e` has the same files except
`docs/superpowers/` and `docs/research/*.json` (internal design notes), which two src comments still cite; they say so.

## 1. src pointers

- Every `% src:` pointer to a tool file in `sections/*.tex`, `main_www.tex` and `figures/fig1_overview.tex` was
  checked against the file at c908431 by printing the cited line (script run, then reread by eye). Fixed:
  - CE/README.md: every line number was stale after the README rewrite (the old ones pointed past its 103 lines,
    such as line 108). They now cite lines 3, 11 to 23, 27, 32, 40 to 47, 59, 68 and 103, with quoted anchors.
    Where the README no longer says a thing, the pointer moved to the file that does (CE/docs/cli.md lines 22, 73
    and 89; CE/NOTICE lines 10 to 39 and 133 to 145; CE/docs/architecture.md lines 81 and 84).
  - CE/docs/evidence.md: lines after 37 moved by +2 (the Hugging Face paragraph). The studies table is 76 to 88,
    the reader's-words sources are 255 to 258, readiness is 260 to 273, its grades are 277 to 372, and the FTC
    passages are 456 and 492. Line 7 now says "AI-ready score", so the old note ("still says GEO Score") is gone.
  - CE/samples/README.md: the first recording is 43 to 50, settings 81, hardware 82, run times 83, results 87 to
    98, scores 100, and the format reminder 55.
  - CE/docs/architecture.md: lines 26, 27, 34, 44, 49 to 59, 63, 67, 74, 78, 81, 84 and 104 (the old 32, 40 to 43,
    53 to 55, 57 to 62 and 79 to 83 had drifted).
  - score-card.tsx line 113 is now 112. rank.ts is now lines 69 to 95 (`startHereFixes`, which keeps one ready edit).
    `before.md`'s flagged heading is line 11, not 7.
  - Every tool path now uses the `CE/` form (RESULTS_E1/E2/E3.md, out/score_summary.json, oss-sweep.json, NOTICE,
    lib/apply.ts, NARRATIVE.md and others).
- Station 1's src comment was stale: since CE 5e7ac43, Start here keeps the "?" ready edit. I rechecked it with the
  engine source (pack questions as `questions` and `authorQuestions`). Start here holds the reader-question advice,
  the reader's-words advice and the "?" edit. The score is 37, and the edit leaves it at 37. Figure 2 shows the
  same three fixes, and the Station 1 text was already right.
- Data pointers refreshed the same way: `data/evidence_matrix.csv` `source_line` +2 for all 37 cells (identical text
  checked, so `derive_loose_grades.py` passes again); `data/README.md`, `scripts/figdata.py` and
  `scripts/collect_scores.py` comments.
- `data/scores.json` was rerun at c908431 and is unchanged: 40 -> 69, 42 -> 68 (the engine's checks did not change,
  only rank.ts). `bash build.sh --derive` reran every derive script. Only provenance hashes changed, including
  E2/E3's from CE 01f4b67's sanitizer, and no number moved.

## 2. Numbers

- `.venv/bin/python -I results/verify_numbers.py` passes (exit 0): every E1 to E3 contrast matches cells,
  analysis JSONs and prose. `results/CLAIMS.md` and `results/VERIFY.txt` were regenerated with `--claims`.
- Sensitivity numbers checked by hand against `results/sensitivity/*.json` "summary" and data/sensitivity_derived.json.
  Answer edit +0.007 to +0.034 matches, after drafts +0.014 to +0.031 (8% to 17%) match, the off-topic share of
  at most 0.0031 matches, and 256 answers per model match. **Fixed:** the answer edit's "could have detected
  (0.019 to 0.069)" mixed two contrasts. 0.069 is the after contrast's largest detectable difference. The answer
  edit's range is **0.019 to 0.047**, which the text now says. "14% and 22% longer" was rechecked with `wc -w`
  (831 -> 946, 1,041 -> 1,275).
- Sample scores were rechecked against data/scores.json and CE/samples/README.md line 100.
- **System facts were stale.** They had been measured at CE 2851854, before the reader's-words check existed. I
  reran `scripts/system_checks.py` at c908431: 1,248 Vitest tests (was 1,171), 78 Playwright tests, and analyze()
  median 7.5 ms (espresso) and 10.2 ms (RAG; three reruns gave 10.6 to 11.0). The text now says "about 10 ms" and
  "1,248 unit". The machine was under some load, so the owner may want one quiet rerun.

## 3. Reviewer pass: what changed in the rendered text

- **Figure 2 takeaway was false.** Since CE 008e68e the draft view shows no grades. A fix group carries at most one
  chip, "Helps" or "Not scored", and grades live on /research. "Every fix shows how strong its evidence is" became
  "The deployed draft view (espresso example): the author applies one fix at a time; a tag marks the checks our
  tests found to help."
- **Figure 4 takeaway:** "Only the reader's own words near the top clearly raised citation" read as covering the
  all-fixes rows, which also show "helps*". It now reads "Of single changes, only the reader's words up top clearly
  raised citation".
- **Terms:** the abstract said "a writing checklist, not a prediction", while the score card, Section 2.1 and
  Figure 1 say "not a forecast". It now says "not a forecast". The intro's "the heading form, cited sources, ..."
  now reads "question headings, cited sources, ..." to match the abstract. The "heading form" wording stays where
  it means E2's heading-versus-plain test.
- The answer edit's detectable-difference range is now 0.019 to 0.047 (see 2).
- The system facts are now "about 10 ms" and "1,248 unit" (see 2).
- **Byline:** five authors in the owner's order: Shehral, Gupta, Prajapati, Zargarian, Bayat (last).
  - Prajapati: Northeastern Khoury, San Jose, prajapati.aksh@northeastern.edu.
  - Zargarian: Northeastern University, USA only, zargarian.p@northeastern.edu.
  - The running head is now "Shehral et al.".
  - notes/STATUS.md, notes/OUTLINE.md and notes/NARRATIVE.md were updated. No `\owner` mark was added for the byline.
- **Cuts to absorb the second author row:** CUTS.md 71 to 78. The biggest is the intro's contributions sentence;
  the novelty sentence above it stays. The others: a merged p-floor sentence, shorter Figure 1 to 4 captions, and
  small wording trims.
- **Checked and fine:** no "ten checks", "GEO Score", old sample numbers (32/44, 35/73, 37/72), wireframe or
  placeholder text remains. "Eleven checks" and "nine mixed, two untested" are consistent throughout. Quotes are
  "inconclusive" everywhere. "Three too few" (11, 11, 24) matches. "Open models over fixed sources, not live
  engines" is stated in the abstract and the limitations. All four links return HTTP 200 (demo, code, both HF
  datasets).

## Left for the owner

1. **Visible `\owner` marks (6):** the video link (footnote 2), the second rater for Figure 3, the same M4 laptop,
   the phone hotspot, who presents and registration, and funding in the Acknowledgments.
2. **Figure 1 schematic vs the current UI.** The stage-2 card shows a "mixed" grade chip on a question-headings
   fix, and the Check panel says "each shown with its evidence grade". The working screens now show only
   "Helps" or "Not scored" and keep grades on /research. The panel is still true of the tool, but the card's chip
   is not what the draft view shows. Swapping "mixed" for "Not scored" on the card is a TikZ edit I did not make.
3. **Figure 4 row labels use arm names.** "Query words in title" is the check the text and Figure 3 call "your
   reader's words up top", and "Question-headed section" relates to "Target questions answered". Renaming rows
   means editing scripts/fig_e1.py. I left it.
4. **Byte check (Limitations).** `CE/experiments/e1/check_prompt_twin.ts` exists and is in the E1 freeze manifest,
   but no recorded run of it is in the repo. Run it (`pnpm --filter @citation-equity/bench exec tsx
   --conditions=@citation-equity/source "$PWD/experiments/e1/check_prompt_twin.ts"`). If it passes, the sentence
   could narrow to the sensitivity harness. I did not run it, because the sentence is an owner decision.
5. **Engine timing:** "about 10 ms" comes from a loaded machine. One quiet rerun of `scripts/system_checks.py`
   would confirm it.
6. **Emails:** Ishan Gupta and Akram Bayat have no `\email` (unchanged from before). Add them if wanted.
7. **Internal-only sources:** two src comments cite `CE/docs/superpowers/...design.md` and
   `CE/docs/research/2026-10-23-oss-sweep.json`, which are not on public main. That is fine for provenance, but a
   reviewer cannot open them.
8. **Title** ("Tests Its Own Advice") and **AI-use statement** wording are unchanged and still yours.
