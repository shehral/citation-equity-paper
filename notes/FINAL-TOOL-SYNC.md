# Final tool sync (2026-10-24)

The paper now matches the tool at CE commit 4831ff9 (`../citation-equity`, read only): eleven checks, four of
them unscored notes (lists, question headings, cited sources, direct answer first; weight 0, still checked and still
suggested), and the new scored check "Your reader's words up top" (`reader-words`). The owner approved the tool change.
`bash build.sh` passes at 4 pages including references; no font, margin or spacing change.

## Build steps run

1. In the tool repo: `pnpm -s --filter @citation-equity/engine --filter @citation-equity/bench build` (build output
   only; no tool source edited).
2. In this repo: `bash build.sh --derive`. It first stopped in `scripts/derive_loose_grades.py`: the cell line numbers in
   `data/evidence_matrix.csv` pointed at the old `CE/docs/evidence.md` (bbd1691, the same text as 12629e2), and the
   registry now lists a `reader-words` check with no coded cells. Fixes below; the derive then passed.

## Data

- `data/scores.json` (derived, CE 4831ff9, tree clean). Standard preset ("foundation"): espresso 40 -> 69, RAG
  42 -> 68 (+29, +26). By evidence: 47 -> 72 and 52 -> 67. These match the expected values and CE/README.md line 28.
- `data/grades.json` (derived): eleventh check `reader-words`, grade mixed, sources GEO, What Gets Cited, SAGEO Arena,
  ConflictingQA; preset weights now 0 for question headings, cited sources and direct answer first, 0.5 / 0.25 for
  reader-words.
- `data/evidence_matrix.csv`:
  - the 33 existing `source_line` values remapped from the old evidence.md to the current one by a line diff (each
    mapped line is the identical text);
  - four new hand-coded reader-words rows (evidence.md lines 253 to 256), all `near`. GEO Keyword Stuffing is coded
    `null` (no test reported; the authors call it "little to no improvement"), not `harm`, because the figure's cross
    means a significant harm. Single rater; listed as a judgement call in `data/README.md`.
- `data/evidence_grades_loose.json` (derived): strict 0 strong, 0 moderate, 9 mixed, 2 untested (reproduces the
  registry); looser rule 0 / 5 / 4 / 2 (reader-words moves to moderate, like lists, direct-answer lead, question
  coverage and comparisons).
- `data/README.md`: one more judgement-call bullet (the reader-words coding).

## Text (rendered)

- Abstract: "ten checks" -> "eleven checks"; "from 32 to 69 and from 44 to 72" -> "from 40 to 69 and from 42 to 68".
- Intro: "ten checks" -> "eleven checks"; "by 37 and 28 points" -> "by 29 and 26 points".
- Figure 1 caption: "by 31 to 38 points" -> "by 26 to 29 points". Its \Description: "ten checks" -> "eleven checks",
  "35 to 73 and from 45 to 76" -> "40 to 69 and from 42 to 68", "Ignore" -> "Skip" (the schematic's word),
  "not a prediction" -> "not a forecast".
- Section 2.1 heading: "ten checks" -> "eleven checks". The checks sentence now says six come from the initial design,
  four from the literature "(Figure 3 names them all)", and one, your reader's words up top, from our own test, where it
  helped; then, once: four (question headings, lists, cited sources, a direct-answer lead) are shown and still suggest
  fixes but are not scored, as our tests found no clear effect on citation. "eight are mixed" -> "nine are mixed";
  looser rule "makes four mixed checks moderate" -> "five".
- Section 3: the closing sentence restating the rule's outcome was cut (Section 2.1 states it once; CUTS.md 68).
- Figure 3 caption: "moves four to moderate" -> "moves five to moderate". \Description: eleven checks; 9 mixed, 2
  untested; looser 5 moderate, 4 mixed, 2 untested.
- Section 5, Station 1: "applies two suggestions and watches the score change" -> "follows the reader's-words advice and
  watches the score change, applies a ready edit through Preview (a heading's question mark, an unscored note, so the
  score holds)". Checked with the engine on the example and its four pack questions (as the workspace loads it): Start
  here holds three advice cards (reader-question advice, reader's-words advice, a real-number fix); the example's only
  ready edit, the heading "?", sits under All fixes (CE commit 9b7d6fb); applying it leaves the score at 37; working the
  questions' words into the opening raises it. So the brief's "two advice cards and one ready edit" in Start here is not
  what the tool shows; the new wording does not say where the edit sits.
- Abstract, intro, Section 5: no other wording change. Ethics, Demonstration, acknowledgments, AI statement and every
  \owner mark kept.

## Figures

- Figure 1, headline panel (`scripts/fig_headline.py`, from data): "rises 26 to 29 points", 40/42 -> 69/68. The before
  labels (40 and 42) overlapped, so they are now stacked with `figstyle.end_labels(side="left")`, as the after labels
  already were.
- Figure 1, schematic (`figures/fig1_overview.tex`): "eleven checks, each shown with its evidence grade"; eleven pips
  (step 0.194 -> 0.175 cm, still centred on the panel), the eleventh mixed; label "not a prediction" -> "not a forecast"
  (the shipped score card); the stage-2 card (the question-heading "?" edit) is kept: the engine still emits it, and the
  header comment now says it belongs to an unscored note.
- Figure 3 (`scripts/fig_evidence.py`): the reader-words row is added (the derive pipeline exposes it). It fits inside
  the figure's fixed height, so no row was dropped and no caption note was needed. The left bracket for checks 7 to 11
  reads "added" instead of "literature", since the eleventh came from our test. Row glyphs: GEO null ring, What Gets
  Cited gain-in-part / null-in-part, SAGEO Arena gain-in-part / harm-in-part, ConflictingQA indirect gain; chips mixed
  -> moderate.
- Figure 4 and Figure 2: unchanged (see concerns).

## src comments updated

- Every `% TODO scores after the tool update` marker removed (abstract, intro, Figure 1); their src comments now cite
  data/scores.json at CE 4831ff9 and CE/samples/README.md line 100.
- CE/docs/evidence.md line references re-pointed to the current file wherever they appear: line 3 and line 34 (now
  "Nine are mixed"), the rubric (16 to 32), the studies table (74 to 86, columns 78 to 86), the C-SEO "19 of 24"
  passage, the check grades (lines 90 to 241), the readiness rubric (258 to 271) and grades (275 to 370), the FTC
  passages (454 and 490), and line 260 for the five browser items and `ce site`. Also `scripts/figdata.py`.
- Section 2.1: CE/README.md lines 17, 21, 23, 24; CE/docs/architecture.md lines 30 and 39; registry.ts lines 13 to 17
  and 98 to 128; score-card.tsx line 113; presets.ts lines 11 to 12 (abstract too).
- Station 1: a new src comment for the Start-here and score facts.

## Cuts (notes/CUTS.md 68 to 70)

The additions pushed reference 16 onto page 5; cut 68 (Section 3 repeat), 69 (Section 2.1 name lists, which Figure 3
carries) and 70 (Station 1 wording) bring it back to 4 pages.

## Concerns, not fixed here

1. Figure 2 is stale: it is a screenshot of the deployed site, which predates 4831ff9 (score 32; the "?" edit first in
   Start here). Its caption and \Description describe that image correctly, but the tool now opens the example at 37
   with three advice cards. Retake with `node scripts/capture_screens.mjs` once the tool is republished (the commit is
   marked "not published"); the local `apps/workspace/out` build is also older than the reader-words check.
2. The paper's sample scores (40 -> 69, 42 -> 68) come from `ce analyze` without target questions, as the derive
   records. The workspace loads the four pack questions, so a visitor sees 37 -> 70 (espresso) and 41 -> 69 (RAG);
   CE/samples/README.md line 100 states both.
3. Older src comments not touched by this sync still cite CE/README.md and CE/docs/architecture.md by line numbers
   from an earlier README (for example "CE/README.md line 108"; the file now has 98 lines). They predate this sync
   (the README already had 98 lines at 12629e2); a full pass is still owed.
4. Tool-side inconsistencies (read only, not changed): CE/README.md line 11 still says "10 writing checks"; CE/docs/
   evidence.md line 7 still says "GEO Score".
5. The reader-words cells are single-rater coding, added today; the looser-rule count (five moderate) rests on them.
