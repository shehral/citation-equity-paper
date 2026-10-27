# Simulated WWW 2027 demo-track review of main_www.pdf

Reviewed: `main_www.pdf` built 2026-10-24 01:00 (commit f03af44), 4 pages, `sigconf,screen,review`.
Reviewer stance: a demo-track PC member who reads the PDF, opens the live demo and the repo, and scores on the call's four criteria (originality, significance, quality, clarity). Written 2026-10-24.
Links checked the same day: https://shehral.github.io/citation-equity/ returned HTTP 200; https://github.com/shehral/citation-equity returned HTTP 200.

---

## Summary

The paper presents Citation Equity, an open-source, client-side writing workspace for "generative engine optimization" (GEO). A writer pastes a draft and target questions; the tool scores the draft on ten checks (six from the PI's design, four from the literature), shows an evidence grade for each check under a strict rule in which any null or negative result makes a check "mixed", suggests span-anchored edits that the author applies one at a time (no rewriting, no "apply all"), and runs a local citation test (BM25 top 8, an Ollama model, 8 seeds) that reports retrieval, validity, citation and word share against a 0.125 chance line. Site readiness and "who gets cited" are reported apart from the score. The evaluation has three parts: (i) a grading of the ten checks over nine sources (Figure 3: 8 mixed, 2 untested; 4 become moderate under a looser rule); (ii) a laptop run of the in-tool test that is inconclusive (every interval includes chance); (iii) a pre-registered sensitivity test in a separate GPU harness on four open models (9B to 31B), where a one-sentence answer edit missed the registered +0.10 bar on all four models and applying all suggestions moved citation share by +0.014 to +0.031 (exploratory). The headline is the contrast between a 31 to 38 point checklist rise and a 1 to 3 point citation-share rise. A further experiment (E1) and the main screenshot are placeholders. The venue plan has three stations, one of them offline.

## Strengths

S1. **A rare and useful stance.** A GEO tool that grades its own advice, counts nulls against it, labels its score "a writing checklist, not a forecast", and ships a test that can come out against its own suggestions. Among the tools the paper positions against (aiseo-audit, geo-score, the commercial trackers), this combination is new, and the related-work paragraph is candid about what is not new.

S2. **Research hygiene that demo papers rarely show.** The pre-registration is committed before the results (3c86c02, 24 minutes before 4d77fa0), the failed bar is reported without moving it, the one deviation is labelled, and a first wrong reading of the laptop run is withdrawn with the three causes named. This is the most credible part of the paper.

S3. **Figure 3 is excellent.** Ten checks by nine sources, with glyphs for the kind of evidence and chips for the strict and looser rule, makes "mixed" inspectable in one glance. It is the figure a reader will remember and reuse.

S4. **Agency-preserving design with a reason.** Anchored suggestions, Undo on every action and no bulk apply are motivated by HCI results on ownership and anchoring [4, 5, 8], not by taste.

S5. **Deployable and private.** Static export, no server, a browser test that no request leaves the origin, MIT code and a live URL. The booth works without venue network, with an online station as an extra.

S6. **Ethics section is real,** not boilerplate: dual use, robots.txt, no redistribution of C-SEO Bench, invented sample pages.

## Weaknesses

W1. **The system is under-shown for a demo paper.** There is no screenshot of the running tool: Figure 2 is a wireframe marked PLACEHOLDER, the system-facts sentence (bundle size, engine time, test count) is a placeholder, and the video link is a placeholder. Roughly 40% of the body (Section 3 plus Figure 4) is measurement, while the user's path through the interface gets about 25 lines (Sections 2.2 to 2.3). The call judges an implemented and tested system and the experience at the venue; as written I have to visit the URL to know what the tool looks like.

W2. **The title promises more than the in-tool test can deliver.** "Tests Its Own Advice" refers to the bench, but the paper's own laptop run (llama3.2:3b, 128 answers, p floor 0.125) cannot reach significance by design, and the booth run is 64 answers in 15 minutes. The evidence that the advice moves citation comes from a different artifact: a Python harness on a GPU cluster that re-implements the prompt *without retrieval*, measures citation share rather than the tool's word share, and (per an owner note) has not been byte-checked against the tool's prompt. A reader will reasonably ask whether the tool tests its advice, or whether the authors did, once, outside the tool.

W3. **The headline contrast is apples to oranges, and panel 1(a) carries no information.** The caption itself says the checklist rise "is built in": the suggestions target exactly the checks the score averages, so a 31 to 38 point rise is tautological. Setting it beside 1 to 3 points of share on a 0 to 1 scale, where chance is 0.125 and the before share is already 0.154 to 0.180, makes the gap look larger than any substantive comparison supports. The relative numbers (+69% and +109% against +8% to +17%) are fairer, but the panel still spends prime page-1 space on a quantity with no variance to explain.

W4. **Statistical claims outrun the figure.** Section 3 says the after draft "beat the before draft on every model" and the Figure 4 caption says it "moved citation share by 1 to 3 points on every model", but in Figure 4(a) the 95% t intervals for Qwen3.5-9B and Gemma-4-31B include zero. The text uses sign-flip p-values while the figure draws t intervals, and the two disagree for Gemma-4-31B. Eight contrasts are uncorrected, the unit is 8 questions over 2 synthetic topics, and the after drafts are 14% and 22% longer, a confound the paper mentions only under "Reading (post hoc)". The registered contrast's p-values are never reported, so a reader cannot tell that the answer edit was small but reliable on two models.

W5. **The grades, a core contribution, rest on one rater and nine sources.** Figure 3 says "One rater" and the text carries an owner placeholder for a second rater. With a rule where one null in any subgroup makes a check mixed, "no check is strong or moderate" is partly a property of the rubric; the paper shows the looser rule (good), but without agreement statistics the grid cannot be trusted as a reusable resource. Why nine sources, given a field survey of 45 studies [9], is not said.

W6. **Placeholders and planned work consume scarce space.** The PDF carries 14 owner marks. The E1 paragraph (6 lines) and the Figure 4(b) frame (about 8 lines) describe an experiment with no results; a demo reviewer gives no credit for planned work and will read it as unfinished. About 5 lines under Figure 3 are blank.

W7. **The value to a writer is left implicit.** If no check is strongly supported and following all suggestions moves share by a point or two in a synthetic setting, the paper should say plainly what a writer gains by using the tool (honest calibration, readiness checks graded on operator documentation, agency, privacy) and for whom. There is no pilot with even a handful of writers; "we found no user study of a GEO tool" is offered as a gap but not acted on, even informally.

W8. **Clarity.** Several terms are used before or without definition: "pack building" (Ethics), `ce site` (Section 5), "the three-module design" (never described), "lost slightly on one sample" (sample of what? the figure pools samples), "p = 0.25 and 0.75" (which test, which contrast?). Referring to a co-author as "Bayat's design" and "our principal investigator's" reads oddly in a single-blind paper. Figure 3 column headers name sources without citation numbers, so the grid cannot be traced to the reference list. The 24-product commercial review is cited only through two pricing pages; its method is not stated.

## Questions for the authors

Q1. At booth scale (llama3.2:3b, 64 answers), what is the smallest change in word share the in-tool test can detect? Does the interface tell the writer that a null there is uninformative?
Q2. How close is the GPU harness to the tool's bench? Same prompt bytes, same source ordering, same metric? Why was retrieval removed, and does the result survive with it?
Q3. What informed the +0.10 bar, a 56% to 65% relative gain on the before share? Was any pilot or prior effect size used?
Q4. Is there inter-rater agreement for Figure 3, and how will grades be updated as new studies appear (versioning, who decides)?
Q5. Does a length-matched placebo explain the exploratory gain, given the after drafts are 14% to 22% longer?
Q6. With only two drafts, can you show anything about whether the checklist score and citation share co-vary across drafts at all, for example over the per-suggestion arms once E1 runs?
Q7. Who is the intended user (independent writers, newsrooms, small businesses), and has anyone outside the team used the tool?

## Score

**As submitted (this PDF): weak reject.** The idea and the honesty would carry a demo paper, but a demo submission whose only image of the interface is a wireframe marked PLACEHOLDER, with no video, an empty experiment slot and 14 visible owner notes, does not yet meet the "implemented and tested system" bar on paper.
**With the placeholders resolved (real screenshot, video, system facts, E1 either filled or cut): weak accept.**
**With the five changes below: accept** is realistic.

Per criterion (1 to 5): originality 4, significance 3, quality 3 (4 once W4 and W5 are fixed), clarity 3.

## The five changes that would most raise the score within 4 pages

1. **Show the real tool on page 1 and page 2.** Replace Figure 1(a) (the built-in checklist rise) with a cropped screenshot strip of the running interface, or fold the 35 to 73 and 45 to 76 numbers into the caption and give the space to the schematic. Replace the Figure 2 wireframe with an annotated screenshot of whatever build is deployed on 2026-11-16 (the current UI if the dashboard redesign is not live; do not wait for it). Fill the system-facts sentence from `data/system_checks.json` and put the video link in the footnote. This answers W1 and W3 and is the single largest gain.

2. **Decide E1 before submission: results or one sentence.** If registered E1 numbers exist by early November, they become Figure 4(b) and a takeaway. Otherwise delete the E1 paragraph and the Figure 4(b) frame, keep one future-work sentence, and spend the roughly 14 recovered lines on a step-by-step walkthrough of Station 1 (what the visitor clicks, what they see) and a "what a writer gets" paragraph (W6, W7). Clear every owner mark either way.

3. **Close the gap between the title and the in-tool test.** State in Section 2.4 the test's power at booth scale and that a null there is uninformative, and say how the harness differs (no retrieval, citation share, prompt check). Then make the bridge a feature: the bench "exports its prompts and replays answers generated elsewhere", so demo the replay of the cluster answers inside the tool at Station 1, so the visitor sees the same 1 to 3 point result in the interface. Run the prompt byte-comparison and drop that owner caveat. If the bridge cannot be shown, retitle toward "a writing tool for AI search that grades its own evidence".

4. **Make the statistics match the figure.** Replace "on every model" with what the intervals show (positive point estimates on all four; intervals exclude zero on two), use one inference procedure in both text and figure (sign-flip intervals, or say why t), report the registered contrast's p-values (small but reliable on two models is a better result than "missed the bar" alone), say "uncorrected across 8 contrasts", and move the 14% to 22% length difference from "Reading" to a named confound with E1 as its fix.

5. **Give Figure 3 a second rater and traceable columns.** Have a second author grade the 10 by 9 grid blind and report agreement (Cohen's kappa or percent agreement) in the caption; add citation numbers to the column headers; say in one clause why these nine sources (all controlled or survey evidence on draft-level edits, for example). This turns the paper's best figure into a reusable, defensible resource and answers W5.

## Smaller fixes

- Define "pack building", `ce site`, "the three-module design" in a clause each, or drop them.
- Replace "Bayat's design" with "the PI's design" consistently, or describe the design itself.
- "lost slightly on one sample": name the sample draft, or drop it since Figure 4 pools both.
- "p = 0.25 and 0.75": say which test and which contrast.
- Fill or rebalance the blank lines under Figure 3.
- Add one sentence on how the 24 commercial products were chosen and reviewed.
- The abstract could end with one clause on what visitors do at the booth.

## Internal notes for the authors (not part of the review; from checking the repo)

- `CE/experiments/RESULTS_sensitivity.md` gives the registered answer-edit p-values: 0.055, 0.008, 0.008, 0.58; and after minus before: 0.52, 0.008, 0.008, 0.039. Qwen3.5-9B's exploratory gain (p = 0.52) is the weakest; "beat on every model" holds only for point estimates.
- Figure 4 row labels round inconsistently against the same file: Qwen3.8-27B 6.25 shows as "6.2" while Gemma-4-31B 6.65 shows as "6.7" (float rounding in the plotting script), and Gemma-4-12B 6.95 shows as "7.0" while the text says "6.95". Use one rounding rule (two decimals, or Decimal half-up).
- The 18.8-point figure for [13] is logged as checked in the full text in `sections/intro.tex` (src comment) but `notes/BIB-VERIFICATION.md` line 25 still says "not re-checked here"; update the log so the two agree.
