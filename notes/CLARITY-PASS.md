# Clarity pass (2026-10-26)

Goal: make the paper read like a demo paper with one message. The tool's advice was tested one change at a time on real
pages, only the reader's own words near the top clearly helped, and the tool now scores what helped. No reported result
was removed from the record: every number dropped from the prose is still in a `% src:` comment, in Figure 1b or
Figure 4, or on the Research page and in the data.

Result: `bash build.sh` gives 4 pages including references. `.venv/bin/python -I results/verify_numbers.py` passes and
`results/VERIFY.txt` and `results/CLAIMS.md` were regenerated. The build also fits 4 pages with 4 lines of filler in place
of the E4 owner mark (tested; see "Reserved space").

## 1. One outcome metric

| | Before | After |
|---|---|---|
| Main-text metrics | word share (laptop), citation share (sensitivity) and the rank score (E1-E3), each with its own paragraph and numbers | The rank-based **citation score** is the outcome. Citation share gets one sentence of context in Section 3 (plus the abstract and Figure 1, unchanged). Word share gets one sentence. |
| Intro results paragraph | "...raised the checklist score by 29 and 26 points, a rise that is built in, but moved mean citation share on four open models by only 1 to 3 points." | "...raises the checklist score by 29 and 26 points, as built in." The next sentence gives the one-change-at-a-time result in citation score and ends with "(Figure 5)". |
| Section 3 sensitivity | 5 sentences: harness design, four models, 256 answers, pre-registration, off-topic control, detectable difference, after drafts | 1 sentence: answer edit +0.007 to +0.034 against a +0.10 target the harness could detect; after drafts, 14% and 22% longer, +0.014 to +0.031 (Figure 1b) |
| Section 3 laptop | 1 sentence (already short) | 1 sentence, same facts, `p >= 0.125` |

## 2. Check names, not arm names

- Prose: "a direct-answer lead" became **direct answer first** everywhere (abstract, intro, Sections 2.1 and 3; the verify
  anchors follow). The two helpful changes are named as checks: *target questions answered* (done as a section headed by
  the question) and *your reader's words up top* (the question's missing words in title and lead).
- Figure 4 (`scripts/fig_e1.py`): rows now use Figure 3's check names. "Question-headed section" became "Target questions
  answered". "Reader's words up top" became "Your reader's words up top". "Attributed quotes" and "Comparison tables"
  became "Attributed expert quotes" and "Tables for comparisons". The two E2a rows became "heading vs plain text" and
  "heading vs no-words heading".
- E1/E2/E3: none appear in the prose. The text says "our first test", "follow-up tests" and "a second follow-up". "E4"
  appears once, in the owner mark the brief specified.

## 3. Section 3 shrunk (prose without comments or figure environments: 537 to 360 words)

| Moved / changed | Where it went |
|---|---|
| "The grades" paragraph (nine citations in column order) | Figure 3 caption: "Columns: [..]. One rater." Section 2.1 points to Figure 3 |
| Method: 3 sentences (editor, validators, paraphrase, judges, seeds, score, replication, pre-registration) | 1 sentence: one check's suggestion alone, 80 GEO-bench queries replicated on 60 from C-SEO Bench, edits only flagged spans, same-length paraphrase, two open judges, 4 sources, `(5-r)/4` (0 if uncited). Then "(plans fixed in advance, code and data: footnote 2)". The Research page URL joined the intro footnote (`\label{fn:links}`) |
| All fixes +0.049, +0.071, replication +0.044 | Figure 4 rows (text keeps only E2b's +0.069, n = 44, which the figure does not show) |
| Heading vs no-words heading (+0.048 replication, +0.017 main) | Figure 4 rows and src comment |
| E3 d, n, CI per check (question headings, cited sources, direct answer first, quotes, three too-few counts) | Figure 4 (n and verdict per row). The text keeps the verdicts in words and "180 / 260" |
| Kept exact in the text | +0.027 [+0.010, +0.043] Holm 0.006, replication +0.036; +0.035; +0.003 / -0.001; +0.023 / +0.037; E2b +0.029 (n 29), +0.069 (n 44); 80, 60, 180, 260; sensitivity +0.007 to +0.034, +0.10, +0.014 to +0.031, 14%, 22% |

`results/verify_numbers.py`: anchors were updated to the new sentences. Anchors for numbers no longer printed were
removed (E1 all-fixes, E2a 9P, E3 per-check d/n/CI, the Figure 4 caption's 260/80). New label anchors check "only the
two that add the reader's own words ... clearly raised the score" (arms 9 and 12 both "helps") and "the reader's-words
gain kept its sign ... as did all fixes together". "one-change tests" replaces "per-suggestion tests" in the Section 7
anchor.

## 4. New figure: Figure 5, the score rising after the reader's-words tips

- `scripts/capture_reader_words.mjs` (modelled on `capture_screens.mjs`; Playwright from the tool repo) runs against
  the live site (https://shehral.github.io/citation-equity/) at 1100x800 CSS px, 2x, light. It loads the espresso example
  (score 37) and reads the reader's-words tip (Add "fix"). It types ", and how do I fix it" into the title, reads the
  next tip (Add "long"), and adds the opening sentence "How long the shot runs and the water temperature are the first
  things to check." It then asserts no reader's-words tip is left, reads the score (40) and the chip ("+3 since you
  started"), and measures callout anchors from text and element boxes. It writes `data/screens/reader_words.png` and
  `data/fig5_callouts.json`.
- The same script reruns the tool's engine (tsx, CE c908431) on `samples/espresso-bitterness/before.md` before and
  after the same two edits, with the four sample questions as questions and as the reader's questions. It also checks
  that the browser draft equals sample plus edits. Result: Standard 37 to 40, and **only `reader-words` changed (0.667 to
  1.000)**. `scripts/fig_reader_words.py` refuses to build if any other check moved.
- `figures/fig5_reader_words.pdf`: one column, 1.60 in tall. It shows the screenshot with 3 numbered callouts and a
  callout list. Caption (takeaway first): "Following the reader's-words tips raises the score: the tool now scores what
  helped." It is referenced from the intro, Section 5 Station 1 and `data/README.md`.
- Placement: it is defined after Figure 4, so the numbers of Figures 1 to 4 do not change. It floats to page 4,
  column 1.

## 5. Reserved space for the Gemini judge check

`\owner{PENDING: Gemini judge check (E4), 2-4 lines}` ends Section 3 (after the E3 sentence, before Related work). A test
build with a 4-line filler sentence in its place stayed at 4 pages. A 5th line has not been tested. The layout around
page 3/4 is sensitive (page breaks before section heads), so rebuild after the result lands.

## Other edits made to fit

Section 2: "Beyond the draft" runs on in the Suggest paragraph, and the per-answer laptop timing was dropped (Section 5
keeps 64 answers in 15 minutes). The Figure 1 (b) label was shortened. There were small wording trims in Sections 5 to 7.
All are listed in `notes/CUTS.md` 79. Owner marks, the Ethics and Demonstration sections, the acknowledgments and the AI
statement are unchanged.

## Not touched

`notes/second-rater/` and `scripts/rater_agreement.py` belong to another task and are not part of this commit.
