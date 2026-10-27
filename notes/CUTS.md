# Cuts made to fit the WWW 2027 demo limit (4 pages including references)

Date: 2026-10-24. Build: `main_www.tex` (`\documentclass[sigconf,screen,review]{acmart}`), `bash build.sh`.

Starting point: the draft-1 sections assembled as is gave **6 pages**. After the cuts below: **4 pages**, with a few lines of slack at the foot of the reference list. No font size, margin, column or spacing change was made; the only layout setting added is `\emergencystretch` (interword stretch, to remove overfull lines caused by unbreakable numeric citations in narrow columns), plus one `\newpage` before the Acknowledgments so that heading is not stranded at the foot of a column.

Words of prose per file (captions and owner marks included; comments excluded), before -> after:

| File | Before | After |
|---|---|---|
| abstract.tex | 174 | 153 |
| intro.tex | 460 | about 350 |
| system.tex | 1,141 | 659 |
| evidence.tex | 1,432 | 588 |
| related.tex | 274 | 135 |
| demo.tex | 274 | 178 |
| conclusion.tex | 373 | 236 |

Every cut removes words or whole items; no claim was strengthened, and every number that stayed keeps its `% src:` comment. Material cut here is still in git history (commit before this one) and in `notes/OUTLINE.md` / `notes/NARRATIVE.md`, so the arXiv version can restore it.

## Figures

1. **Figure 1 moved to the page-1 teaser** (`teaserfigure`), since sigconf cannot float a `figure*` onto page 1. Not a cut; it saves a float page.
2. **Figure 1 caption** shortened from about 170 to about 110 words: dropped the hollow-versus-filled marks sentence, the "faint lines per sample draft" detail and the "target always among the 8 sources" clause (all still visible in the panel or stated in Section 3).
3. **Figure 4(b), the E1 frame**: the full empty-axes frame (`figures/fig4b_e1_frame.pdf`, 2.55 in tall) is replaced in the submission by a 1.25 cm text frame that describes the planned forest plot and stays marked as an owner placeholder. The script and PDF are kept; the full frame returns when registered E1 results exist.
4. **Figure 2 caption**: the five-item callout list is no longer repeated in the caption (the figure itself lists the callouts under the frame).
5. **Figure 3 caption**: the cell-glyph legend sentence and the "each cell cites its line" sentence dropped (the glyph legend is drawn in the figure).
6. **Figure 4 caption**: dropped the row-label sentence (sources cited per model, shown in the panel), the off-topic sentence (in the text and Figure 1) and the harness design sentence (in the text).

## Abstract

7. Merged the two opening sentences (context and gap) into one; the "8 to 17%, exploratory" and "+0.10 on all four" sentences merged into one. The UI label is now paraphrased ("a writing checklist, not a prediction") rather than quoted.

## Introduction

8. Dropped the Pew Research figures (8% versus 15% of visits, 1% on links in the summary) and its citation `chapekis2025pew`; the field-experiment figure (18.8 points) carries the context.
9. Dropped the formatting-only-edits sentence (252,000 trials, `vishwakarma2026cited`; that study is still cited in Sections 2 and 4) and the SAGEO-in-the-intro clause.
10. Dropped the three-questions walkthrough (*can engines reach the site?* / *is the draft easy to cite?* / *did the advice change citation?*); the same structure is in Figure 1.
11. Contributions bullet list -> one sentence with the same three pointers. The optional takeaway box (already commented out) stays out.
12. One product URL footnote (Ahrefs Brand Radar) dropped; Evertune and Writesonic remain. The demo, code and video links moved into a footnote on the first mention of the tool.

## Section 2 (system)

13. "Design principles and architecture" subsection heading removed; the four principles and the three packages are one paragraph each, shortened. The unit-test and replay-test sentence dropped (the replay test also dropped from Section 5); the no-egress browser test kept.
14. Check subsection: dropped "with findings anchored to its text" and the statistics example (GEO 19.3 to 25.2 against 19 of 24 C-SEO settings; the 19 of 24 figure stays in the intro); the comparisons example kept. Preset weights (foundation 1 / 0.5; evidence 1.0, 0.7, 0.25, 0.15) dropped.
15. Looser-rule placeholder filled from `data/evidence_grades_loose.json` (four of the eight mixed checks become moderate; script output, not predicted). Not a cut; recorded because it replaced an owner placeholder.
16. Suggest subsection: the ownership citations (Draxler, Dhillon) are cited once in the intro instead of twice; the live-update sentence and the local-model wording sentence dropped.
17. Beyond the draft: the list of the seven readiness items, the browser-versus-`ce site` split, the moderate/mixed/untested readiness tally, the Google AI-features sentence and citation (`google-ai-features`), `ce live`, and the server-log and Bing export sentence all dropped. Kept: seven items, operator documentation as evidence, the two strong items, who gets cited, "neither changes the score".
18. Bench subsection: dropped "the samples have 4 questions with 12 competitor pages each" and the definition of a valid answer by "in-range marker"; the caveat is quoted in its short form ("It does not predict live AI engines.").

## Section 3 (what the test found; was "Evidence and measurement")

19. Section retitled "What the test found" and the three subsections turned into run-in paragraphs (saves heading space).
20. Grades paragraph: dropped "eight studies and a survey", the reading date and "claims we could not find were dropped".
21. Laptop bench lesson: the four-sentence account of the withdrawn first recording (4,096-token window, about 3,500-token prompts, 3 truncated calls; 13 of 128 invalid answers; share 0.13 to 0.22 against 0.20 over 5 sources) -> one sentence naming the three faults. The per-sample word shares (0.087 -> 0.137, 0.086 -> 0.095) and the retrieval example (0 of 8 -> 8 of 8 runs) dropped; the chance-level result and p-values kept.
22. Sensitivity design: dropped "drawn from that question's 12 synthetic pages", the explicit commit times (20:18 and 20:43 PDT; the 24-minute gap and both hashes kept) and "to the public repository".
23. Registered outcomes: the deviation sentence shortened.
24. Exploratory: dropped the per-model list (+0.014, +0.023, +0.026, +0.031; now the range) and the single-question maxima (0.088 and 0.141).
25. Reading: dropped "80% power, paired t" wording (the method stays in the `% src:` comment), the confound that the score rise is built in (stated in the intro and Figure 1) and "the competitors are synthetic" (stated in Limitations and the captions).
26. E1 placeholder paragraph shortened (Holm families, the MDE values in rank-score units, the judge-model sentence and the 8 Nov decision rule dropped from the visible mark; the design source and "Results: PENDING" kept; the decision rule stays in the file's comments).

## Section 4 (related work)

27. Dropped the survey-protocol sentence (the survey is cited in Sections 2 and 6), the Schulte et al. day-to-day variance sentence and citation (`schulte2026measure`), the two footnoted tools (answerlint, GEO Optimizer) and the "Writing with AI" paragraph (those citations are in the intro and Section 2.2). ConflictingQA dropped from the counterfactual-style sentence (still cited among the nine graded sources).

## Section 5 (demonstration)

28. Section retitled "Demonstration at the venue". Paragraph headings -> run-in emphasis. Dropped the video sentence (the link is in the page-1 footnote), the replay-test guarantee and the "open: in-browser run not timed" comment's prose.

## Section 6 (ethics, limitations, future work)

29. Ethics: dropped "contacts anyone" and "reads consumer AI apps" from the never-does list, and "platform rules" from the off-page cards clause (FTC rules kept). Every required ethics element kept: no participants, no user data, invented samples, C-SEO Bench not redistributed, robots.txt, dual use, IRB for a future study.
30. Limitations and future work merged into one paragraph; "passage-level retrieval in the bench" dropped from future work.
31. Closing paragraph dropped (it repeated the intro's "reported as it came").

## References

32. Cited entries fell from 19 to 16: `chapekis2025pew`, `schulte2026measure` and `google-ai-features` are no longer cited (they stay in `references.bib`, unused).
33. `references.bib`: the `url` field removed from arXiv entries whose `eprint` field already prints the same id, and from the ACL entry that has a DOI. Bibliographic content is unchanged; the URLs remain in `notes/BIB-VERIFICATION.md`.

## Restore first if space appears (for example, after the owner items shrink)

1. The full Figure 4(b) frame (or the real E1 panel).
2. The per-model exploratory numbers and the laptop-run word shares.
3. The statistics example in Section 2.1.
4. The readiness item list in Section 2.3.

## Pass 2 (2026-10-24): verify-claims fixes and review changes, re-fit to 4 pages

Applying `notes/verify-claims.md` (A1 to A5, B1 to B9, C1 to C3, C8, C9) and the review changes that fit
(`notes/verify-review.md`: statistics matched to the figure, power of the in-tool test, harness differences, traceable
Figure 3 columns, undefined terms, product-review method, booth clause in the abstract) took the build to 5 pages.
Cuts made to return to 4 (no font, margin or spacing change; one figure height reduced):

27. The `\newpage` before the Acknowledgments removed (its comment said to remove it if the text changed).
28. Owner marks shortened to a few words each; their full text moved to `% Owner item` comments and `notes/STATUS.md`
    (system facts, Figure 2 wireframe, E1 paragraph and frame, E1 data-use sentence, booth laptop). The byte-check mark
    became one plain sentence of limitation ("The harness prompt has not been byte-checked against the bench's").
29. Section 2 opening: the four-principle sentence (repeated from the intro) cut to the two that are not stated
    elsewhere (outcomes beside the score; the draft stays local unless the author picks a hosted model).
30. "Beyond the draft" turned from a subsection into a run-in paragraph.
31. Figure 3's column citations are given once, in the grades paragraph (in column order), not repeated in the caption.
32. Figure 1 caption: the "readiness and who gets cited never change the score" clause (drawn in the schematic) and
    "8 questions x 8 seeds" (printed under panel b) dropped; the stage sentence shortened.
33. Figure 4: height 2.45 in -> 2.30 in; the E1 text frame 1.25 cm -> 0.95 cm with a shorter description.
34. Ethics: the privacy clause (stated in Section 2) dropped from the first sentence.
35. Intro: "and we report it as it came" dropped.

Cuts after the real Figure 2 screenshot (2026-10-24; the figure grew 2.75 in -> 3.07 in, no font, margin or spacing change):

36. Section 2 bench sentence: "and a null there is uninformative" -> "; a null is uninformative".
37. System facts: "a draft of 800 to 1,000 words in 4 to 6 ms" -> "a 1,000-word draft in about 6 ms" (data/system_checks.json: 5.98 ms at 1,041 words).
38. Sensitivity confound: "the planned per-suggestion test compares each edit with a placebo of matched length" -> "the per-suggestion test pairs each edit with a length-matched placebo".
39. Ethics: "it publishes aggregates and hashes, never their text" -> "publishes only aggregates and hashes".
40. Demo station 1: the live-run sentence shortened ("A live run of the example (64 answers, 15 minutes) starts each session ...").
41. Ethics: "the hosted site has no server" dropped (stated in Section 2).
42. Future work: the per-suggestion test dropped from "Next are ..." (it is running; Section 3 describes it).
43. Limitations: the smoke-test parenthetical shortened ("a one-model smoke test cited a planted answering page in 8 of 8").
44. Ethics: "The tool never posts or writes reviews." dropped; the dual-use sentence (generates no page text on its own) carries it.
45. Owner marks for byline/acknowledgments and the AI-use statement shortened to a few words (full text in notes/STATUS.md). When the owner fills them, the real text needs about 3 to 4 lines: budget them from the E1 paragraph or Figure 4 when E1 lands.

E1 results added (2026-10-24): Figure 4 is now the E1 forest plot (the sensitivity panel and the E1 placeholder frame retired; fig_e1_frame.py removed, fig_e1.py added); the sensitivity test is one text paragraph. To fit:

46. Sensitivity: the Registered / Exploratory / Reading / Confound run-ins merged into one paragraph; the fallback-reading deviation and per-model p values moved to the source (RESULTS_sensitivity.md).
47. Laptop paragraph: two sentences (the 5.3 to 6.5 of 8 sources and the paired p values stay in the src comment).
48. Figure 4: candidate rows 13 (descriptive) and 14 (n 7) left to RESULTS_E1.md; caption shortened.
49. Abstract: "(9B to 31B parameters)" and "(8% to 17%, ...)" dropped; the sensitivity setting sentence merged into "Both tests use open models given fixed sources".
50. Section 2: "(shown in the tool as the GEO Score) ... under editable weight presets ... not a prediction of citations" -> "(the tool's AI-ready score) ... under editable weights ... not a forecast" (also matches the redesigned UI).
51. Laptop: "so our claims rest on larger models" -> "so we rely on larger models"; grades: "a C-SEO Bench result reports nulls" -> "C-SEO Bench reports nulls". Figure 1: "Ignore" -> "Skip" (the redesigned UI's word).

Style rewrite (2026-10-24, notes/STYLE-REWRITE.md): planning stated in plain sentences, hashes and run-in labels removed. No cut was needed; the build stays at 4 pages with no font, margin or spacing change.

E2 and E3 added (2026-10-24, notes/E23-UPDATE.md). The build was already at 5 pages (the acknowledgments and AI-use
statement had been written in); adding two Section 3 paragraphs and three Figure 4 rows took it to about one column
over. Cuts made to return to 4 (no font, margin or spacing change):

52. Abstract and intro: the sensitivity clause "and a one-sentence answer edit fell short of its +0.10 target on all four" dropped (Section 3 keeps it).
53. Abstract: "in a design planned before any page was edited" dropped (planning is stated in Section 3, once per test); "with another editing model" -> "with another editor".
54. Intro: "Testing the advice gave an unflattering answer." and the Bajemon and Rochet "points the same way" sentence dropped (Related work keeps the citation); "with the draft kept on the author's machine unless the author picks a hosted model" dropped (Section 2 states it); contributions wording shortened.
55. Related work: the SAGEO Arena and AutoGEO contrast sentences dropped (both stay cited as Figure 3 columns); the geo-score clause dropped (the intro cites it); "In the 341 sources we reviewed, we found no user study of a GEO tool." dropped.
56. Section 2: "Mixed is not 'no effect', so the tool shows each grade's studies ..." and its Vishwakarma odds-ratio example dropped (Figure 3 shows directions); the looser-rule sentence shortened (owner mark kept); "the draft view loads 0.8 MB of compressed JavaScript" dropped (data/system_checks.json keeps it); "Beyond the draft" merged into one sentence; "; a null is uninformative" dropped.
57. Section 3 grades: "The figure shows what mixed hides." and "The rule has overruled us once: the direct-answer lead, first graded moderate, is mixed because C-SEO Bench reports nulls." dropped.
58. Section 3 laptop: one sentence ("After we withdrew a first recording that misread a drop in citation (truncated prompts), every 95% interval ..."); the invalid-answers and llama3.2:3b detail stay in Section 2.3 and the src comment.
59. Section 3 sensitivity: "Python", "(the question as a heading plus one answering sentence)", "on every model", "(8% to 17%)" and "the plan is in the repository" dropped; E1: "the plan and its amendments are in the repository" and "17,823 of 17,824 answers valid" dropped (src comments keep them).
60. Section 3 E1: the lists sentence and "six checks applied to too few pages ... no table edit passed validation" replaced by the E3 results; "(a candidate check)" dropped.
61. Section 3 E3: "(an extra editing attempt added few pairs)" dropped (RESULTS_E3.md "Where the queries come from"; src comment keeps it).
62. Figure 1 caption: the "Left: ... (1) ... (2) ... (3)" stage sentence (drawn in the schematic) and "the off-topic control stays at or below 0.0031" (Section 3) dropped.
63. Figure 2 caption: "Test it sits collapsed further down the rail" dropped. Figure 3 caption: "Columns: sources in the order cited in Section 3", "where operator documentation counts" and "mixed checks" -> "four" dropped.
64. Figure 4 caption: "Mean per-query difference against" -> "Difference from"; "bootstrap" dropped; row notes compressed.
65. Limitations: the smoke-test parenthetical dropped (src comment keeps it); "Next are a report of how local results agree with live engines" -> "Next are a comparison with live engines".

Review fixes (2026-10-24, task-PAPERE23-review.md findings 1-4): the softer claims ("clearly", quotes inconclusive,
"kept its sign") added about two lines and pushed the references to page 5. Cuts made to return to 4 (no font,
margin or spacing change):

66. Abstract: "the only change that clearly raised citation was adding ..." -> "only adding ... clearly raised citation"; intro the same pattern ("the only one that clearly helped was" -> "only ... clearly helped").
67. Figure 4 takeaway: "question headings, cited sources and direct answer first ... and attributed quotes were inconclusive" -> "sources and answer-first ...; quotes were inconclusive" (Section 3 names each check with its n).

Final tool sync (2026-10-24, notes/FINAL-TOOL-SYNC.md): "eleven checks", the four unscored notes and the new check in
Section 2.1, and a longer Station 1 pushed reference 16 to page 5. Cuts made to return to 4 (no font, margin or spacing
change):

68. Section 3: the closing sentence "By our rule, checks with no effect larger than 0.03 become unscored notes (...), and a new scored check, Your reader's words up top, asks for what helped." dropped; Section 2.1 now states the outcome once (the src comment stays in Section 3).
69. Section 2.1: the two name lists "(standalone paragraphs, question headings, lists, statistics, tables, expert quotes)" and "(cited sources, a direct-answer lead, coverage of the target questions, comparisons)" replaced by "(Figure 3 names them all)"; Figure 3's rows carry every name. The two sentences on where the checks come from and which four are unscored merged into one.
70. Section 5, Station 1: "previews and applies a ready edit (a heading's missing question mark, ...)" -> "applies a ready edit through Preview (a heading's question mark, ...)"; "in Start here" dropped.

Final polish (2026-10-26, notes/FINAL-POLISH.md): the five-author byline adds a second author row above the teaser,
and the reference list ran onto page 5 (about 8 lines over). Cuts made to return to 4 (no font, margin or spacing
change):

71. Intro: the contributions sentence ("Our contributions are the system, live and open (Section 2); graded evidence for every check (Section 2.1, Figure 3); and a citation test inside the tool, with tests of its advice one change at a time (Section 3, Figure 4).") dropped; the novelty sentence before it states the contribution, and the text is kept as a comment in sections/intro.tex.
72. Section 2.3: "With a sample's 4 questions the smallest possible p is 0.125, so a laptop run shows a direction at most." dropped; Section 3's laptop paragraph now says "and with 4 questions p cannot fall below 0.125".
73. Figure 1 caption: "On our two sample drafts" -> "On two sample drafts"; (a) "of the two sample drafts" dropped (the panel says "2 sample drafts"); (b) "of the target", "one line per model" and "Dotted: chance." dropped (the panel labels each model and the chance line).
74. Figure 3 caption: "Chips: the shipped (strict) and looser grades. The strip grades the readiness items." dropped (the column heads read "strict rule (shipped)" and "looser rule"; the strip has its own label). "One rater." kept.
75. Figure 2 caption: the second sentence "The deployed draft view on the espresso example." folded into the takeaway ("The deployed draft view (espresso example): ...").
76. Section 3, The grades: "each opened and read, which are the columns of Figure 3 from left to right" -> "the columns of Figure 3 in order" (Section 2.1 keeps "each opened and read").
77. Section 2: "(browser and command line)" -> "(browser and CLI)"; "asserts that no request" -> "asserts no request"; ", and 1,248 unit" -> "; 1,248 unit"; "the draft stays on the author's machine unless the author chooses a hosted model" -> "drafts stay local unless the author picks a hosted model". Section 2.3: "the bench exports its prompts" -> "it exports the prompts".
78. Figure 4 caption: "``vs'' rows: question heading minus two variants." dropped (the two rows are labelled "vs same text, plain" and "vs heading w/o its words" under "Question-headed section"; Section 3 explains both). Its takeaway now starts "Of single changes, only the reader's words up top" (was "Only the reader's own words near the top"), so it no longer reads as excluding the all-fixes rows.

Clarity pass (2026-10-26, notes/CLARITY-PASS.md): Section 3 rewritten around one outcome metric (the rank-based citation
score), a second screenshot (Figure 5, about 1.6 in) added and about 4 lines reserved for the Gemini judge check (E4).
The build was checked at 4 pages with 4 lines of filler in place of the E4 owner mark. Cuts, all logged here (no font,
margin or spacing change):

79. Clarity-pass cuts and moves:
    - Section 3, "The grades": the nine source citations moved into Figure 3's caption ("Columns: ...", column order); Section 2.1 points to Figure 3.
    - Section 3, laptop: one sentence ("shows a direction at most: every 95% interval ... included the 0.125 chance level, p >= 0.125 with 4 questions, and a first recording, misread through truncated prompts, was withdrawn").
    - Section 3, sensitivity: one sentence. Dropped from the text: the four model names (Figure 1b labels them), "on a GPU cluster", "re-implements the bench's prompt without retrieval", "8 questions x 8 seeds, ... 7 synthetic competitors", "256 valid answers each", the off-topic control <= 0.0031 (Figure 1b shows it), the detectable difference 0.019 to 0.047 (now "a +0.10 target the harness could detect"), "We wrote the design and success criteria before the results" (now "planned in advance"). All stay in the src comment.
    - Section 3, method: one sentence plus a pointer to footnote 2 (the Research page URL joined the intro footnote). Dropped: the editor's name (Gemma-4-31B-it), the validators clause, the judges' names and "8 seeds", "We fixed the design, sample and analysis before editing any page" (now "plans fixed in advance").
    - Section 3, results: dropped numbers that Figure 4 shows: all fixes +0.049 / +0.071 / replication +0.044; heading vs a no-words heading +0.048 (replication) and +0.017 (main), with its clause; E3's d and n for question headings, cited sources, direct answer first, attributed quotes (with its CI) and the three too-few counts (11, 11, 24); "Two follow-up tests were each planned before their answers existed" folded into one clause; "(difference" dropped before +0.003.
    - Figure 4 caption: "260 queries for question headings and statistics to tables, 80 for the rest;" dropped (Section 3 says which checks the 260-query follow-up covers); takeaway names the two reader's-words changes.
    - Figure 1 caption: (b) "Citation share in the sensitivity harness (synthetic competitors)" -> "Citation share in the sensitivity test".
    - Intro: the sensitivity test's "but moved mean citation share on four open models by only 1 to 3 points" dropped (abstract, Figure 1 and Section 3 keep it); "as it is built to, so the score alone cannot show that the advice works" -> "as built in"; "in one author-side tool with no server" -> "in one serverless author-side tool".
    - Section 2: "Beyond the draft." run on in the Suggest paragraph (was a \paragraph); Section 2.3 "An answer takes 14 to 17 s on the authors' laptop;" dropped (Section 5 keeps 64 answers in 15 minutes).
    - Section 5: "with llama3.2:3b" -> "(llama3.2:3b)"; "A live run of the example" -> "A live run"; "and opens the recorded citation test" -> "and the recorded citation test".
    - Section 6: "building a set of competitor pages" -> "building competitor pages". Section 7: "and no user study" dropped (the next sentence names a study with writers); "per-suggestion tests" -> "one-change tests".
