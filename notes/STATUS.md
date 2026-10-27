# Status: WWW 2027 demo paper (Citation Equity)

Updated 2026-10-24. Build: `bash build.sh` (tectonic only). Output: `main_www.pdf`. Length: **4 pages including references**, which is the limit. Format: acmart `sigconf,screen,review`. Commit `ff6fd1e`. Deadline 16 Nov 2026 AoE.

## What the draft argues

1. Citation Equity is an open-source writing tool for AI search that runs in the browser. It shows the graded evidence behind each of its ten checks. Under a strict rule for nulls, none of the checks is strong: 8 are mixed and 2 untested. It suggests anchored fixes that the author applies one at a time.
2. The tool tests its own advice. On two sample drafts, following the suggestions raised the checklist score by 31 to 38 points but moved mean citation share on four open models by only 1 to 3 points (exploratory). A one-sentence answer edit missed the pre-registered +0.10 bar on all four models.
3. What is new is the combination: graded evidence with an explicit null rule, a self-test of the advice, and a pre-registered check of that test's sensitivity, all in one author-side tool with no server.

## What is still a placeholder (blue `[OWNER: ...]` marks; 12 are visible in the PDF)

- **E1:** there are no results, and no E1 number appears anywhere. A placeholder paragraph ("Which single suggestions matter (planned)") describes the design from `CE/experiments/PREREG_E1.md`, which is not yet frozen. Figure 4(b) is a text frame that describes the planned forest plot. The submission default if no registered results exist by 8 Nov is in the comments of `sections/evidence.tex`.
- **Screenshots:** Figure 2 is a wireframe of the planned dashboard draft view, marked PLACEHOLDER. It needs to be replaced by a screenshot of the build that is actually deployed. Figure 1's schematic is drawn and needs no screenshot.
- **Byline (settled 2026-10-26):** Shehral, Gupta, Prajapati, Zargarian, Bayat (last). All Northeastern Khoury, San Jose, except Pegah Zargarian (Northeastern University, USA; alumna). Emails for Shehral, Prajapati and Zargarian; running head "Shehral et al.". No owner mark remains for the byline.
- **AI-use statement:** a placeholder for you to write.
- **Other placeholders:**
  - Video link (intro footnote).
  - One sentence of system facts. `scripts/system_checks.py` does not exist yet.
  - Second rater for Figure 3.
  - Acknowledgments and funding.
  - Booth laptop, phone hotspot, who presents.
  - The E1 data-use sentence in Ethics, needed only if E1 runs.

## Reviewer score (simulated PC review, `notes/verify-review.md`)

- **Before the fixes:** weak reject as submitted. Weak accept once the placeholders are resolved, and accept with the five changes. Originality 4, significance 3, quality 3, clarity 3.
- **After the fixes:** this is my own reading against the same rubric, not a fresh review.
  - The PDF as it stands is still a **weak reject**, because the reviewer's blocking reasons are the placeholders: the wireframe, no video, the empty E1 slot and the visible owner marks.
  - Once the placeholders are resolved, I expect **weak accept, leaning accept**.
  - Expected criterion scores: originality 4, significance 3, quality 3 to 4 (W4 is fixed; W5 is only half fixed until a second rater grades the grid), clarity 4 (the W8 terms are fixed).
- **Applied in this pass:**
  - All of `verify-claims.md` A1 to A5 and B1 to B9, plus C1, C2, C3, C8 and C9.
  - Review change 3 in part: the test's power on a laptop is stated, the null is called uninformative, and the harness differences are named (no retrieval; citation share instead of word share; prompt not byte-checked).
  - Review change 4 in full: registered and exploratory sign-flip p-values are in the text and in Figure 4; "uncorrected" is stated; length is named as a confound, with E1's placebo as the fix; "on every model" now refers to means only.
  - Review change 5 in part: the Figure 3 columns now trace to reference numbers. There is still no second rater.
  - Smaller fixes: "pack building", `ce site` and "three-module" are defined or dropped; "Bayat's design" is now "the project's initial design"; the p-values say which test they come from; one clause gives the product-review method; one booth clause is in the abstract; Figure 4 label rounding is fixed; the BIB-VERIFICATION log is updated.
- **Not applied:**
  - Changes 1 and 2 need real assets or your decision.
  - The replay bridge in change 3 is not something the tool has been shown to do.
  - The second rater in change 5.
  - C4 (a chance-level footnote) did not fit.
  - C10 (the stale README in the tool repo) cannot be fixed here because that repo is read only for this paper.

## Remaining decisions (yours)

1. **E1:** fill Figure 4(b) with registered results by early November, or cut the paragraph and the frame to one future-work sentence. Cutting frees about 10 lines, which the reviewer suggests spending on a Station 1 walkthrough and a "what a writer gets" paragraph.
2. **Screenshot and video:** capture whichever build is deployed on 16 Nov rather than waiting for the redesign, then record about 2:30 of Station 1 and choose where to host it.
3. **(Resolved 2026-10-26: the paper uses "AI-ready score" and "not a forecast" everywhere, as the tool now does.)** **One UI label everywhere:** the text and Figure 1 use the shipped label ("not a prediction", "GEO Score"). Figure 2's callouts quote the redesign ("not a forecast", "AI-ready score"). If the redesign is live on submission day, switch all of them together.
4. **Figure 1(a):** the reviewer says the checklist-score panel is tautological (W3) and suggests folding its numbers into the caption. It is kept for now, with "the rise is built in" in the caption.
5. **Title:** the reviewer says "Tests Its Own Advice" overpromises, since the decisive test ran in an external harness. Keep it, or retitle toward "a writing tool for AI search that grades its own evidence".
6. **Second rater for Figure 3:** have a coauthor grade the grid blind and report agreement. Also add one clause on why these nine sources. `CE/docs/evidence.md` gives no selection rule, so none was invented.
7. **Byte check:** run the 10-prompt `--export-prompts` comparison between the harness and the bench, then drop or keep the limitation sentence.
8. **Byline:** done 2026-10-26 (five authors, see above). Still yours: the Acknowledgments funding mark; the AI-use statement is drafted.
9. **Booth:** confirm the laptop, the hotspot, who presents and registration.
10. **(Resolved: CE/README.md no longer gives sample scores; CE/samples/README.md line 100 matches the paper.)** **Tool repo before submission:** `CE/README.md` line 57 still says "37 to 72". The paper and `samples/README.md` say 35 to 73. Reviewers will open the README.

## Update 2026-10-24 morning: E1 results are in

- E1 ran as frozen (7859b07): 80 main + 60 replication queries, two judges, 17,823 of 17,824 answers valid. Results: CE/experiments/RESULTS_E1.md (commit e258a1a); headline contrasts recomputed independently (same n, d, p).
- Figure 4 is now the E1 forest plot; the sensitivity test is one text paragraph (cuts 46-51 in CUTS.md). Abstract, intro, Section 3, Section 7 updated.
- Findings: only edits that add the question's own words helped (question-as-heading +0.027, Holm p 0.006, replicated +0.036; query words in title and lead +0.035, a candidate check); both lose their interval once length and question-word changes are regressed out. Lists: no effect beyond +-0.03. Six checks: too few pages. Tables: no valid edit. All fixes together +0.049 (+0.071 vs paraphrase).
- Owner decisions (new):
  1. The registered rule makes the lists check an unscored note (one of Prof. Akram's six). The tool change is built on a branch; the paper already states the rule's outcome. Confirm before the public republish.
  2. If lists is unscored, the sample scores in the abstract and intro (35 -> 73, 45 -> 76; "38 and 31 points") change; update them from the tool's regenerated numbers.
  3. Figure 1's headline panels still show the sensitivity result; switching panel (b) to E1 is optional.

## Update 2026-10-24: E2 and E3 are in (notes/E23-UPDATE.md)
- Owner item: Section 3 states the tool update as the rule's outcome (lists, question headings, cited sources and
  direct-answer lead become unscored notes; new scored check "Your reader's words up top"). Confirm, or soften to
  "will become".
- Owner item: sample scores (32 -> 69, 44 -> 72; Figure 1 "31 to 38 points", 35 -> 73 / 45 -> 76) are marked
  `% TODO scores after the tool update`; the main session updates them.
- The paper still says "ten checks" and Figure 3 has ten rows; with four checks unscored and one added, decide how
  the count is stated.

## Update 2026-10-24: synced to the final tool (CE 4831ff9; notes/FINAL-TOOL-SYNC.md)
- Resolved: the owner approved the tool update (four unscored notes, the reader's-words check). Section 2.1 states it
  once; Section 3's repeat was cut.
- Resolved: sample scores from data/scores.json (Standard preset): espresso 40 -> 69, RAG 42 -> 68; Figure 1 "26 to 29
  points"; intro "29 and 26 points". No `% TODO scores` marker remains.
- Resolved: "eleven checks" everywhere; Figure 1 has eleven pips; Figure 3 has an eleventh row (reader's words).
- Open: Figure 2 is the deployed site's screenshot (score 32, the "?" edit first in Start here); retake it with
  scripts/capture_screens.mjs after the tool is republished (the deployed site predates 4831ff9).

## Update 2026-10-26: final polish (notes/FINAL-POLISH.md, notes/SIM-REVIEW-FINAL.md)
- Byline: five authors (Shehral, Gupta, Prajapati, Zargarian, Bayat); Zargarian's block is Northeastern University, USA only; emails
  for Prajapati and Zargarian added; running head "Shehral et al.". No owner mark for it.
- Every `% src:` pointer rechecked against the tool's feat head c908431; data/scores.json, data/system_checks.json and the
  evidence-matrix line numbers refreshed; `bash build.sh --derive` passes at 4 pages; verify_numbers.py passes.
- Open owner marks in the PDF: video link, second rater, M4 laptop, hotspot, who presents, funding. Details and the rest of
  the owner list in notes/FINAL-POLISH.md.
