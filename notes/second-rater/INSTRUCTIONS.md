# Second rating of Figure 3: instructions

Time: about 2.5 to 3 hours for 74 cells (about 10 minutes of reading per study, then 1 to 2 minutes a cell). Two sittings are fine.

## What you are doing

Our paper has a figure (Figure 3) that shows what nine published studies found about each of eleven content practices ("checks"). One person coded it. You are the independent second rater, so we can report how much two people agree. Your job: for each row of `rating_sheet.csv`, open the study, find what it found about that practice, and write one label in the `rating` column.

## Rules

1. **Do not look at the existing coding.** Do not open `data/evidence_matrix.csv`, `docs/evidence.md`, `docs/research/evidence-notes.md`, Figure 3, `data/evidence_grades_loose.json`, or any paper section that discusses the evidence. Read only the nine studies themselves (the `study_link` column). Do not ask the first rater what they chose.
2. Work alone. Do not compare answers with anyone until both sheets are done.
3. Rate what the study says, not what you expect or what other studies say.
4. Some rows have nothing in the study. That is expected: label them `empty`.

## The practices (what each check means)

standalone-paragraphs: paragraphs that make sense on their own. question-headings: headings phrased as questions. lists: bulleted or numbered lists. statistics: adding numbers or statistics. tables: tables as a page format. expert-quotes: adding quotations from experts or credible sources. cited-sources: adding citations or references to sources. direct-answer-lead: putting the answer or a summary at the start. question-coverage: content that addresses the reader's question. comparisons: explicit comparisons with alternatives. reader-words: the query's key words placed in the title, first heading or opening paragraph.

## The labels (write the label exactly as shown)

The examples are invented, not taken from the studies.

| Label | Use it when | Invented example |
|---|---|---|
| `controlled_gain` | The study changed that practice itself, changed little else, compared with and without it, and it helped. | "We added statistics to otherwise identical pages; they were cited 20% more." |
| `indirect_gain` | It helped, but not by a clean test of that practice: the evidence is observational (pages that happen to differ), rules reported by engines, or the test changed a nearby thing or a bundle that includes the practice. | "Pages with lists were cited more" (no one edited the lists); or "restructuring (headings, lists, tables together) helped". |
| `gain_part` | It helped in some settings (domains, engines, models) and had no significant effect or hurt in others. | "Significant in 4 of 6 models, not in the other 2." |
| `null` | The study tested it (or a nearby practice) and found no effect or no significant gain. | "Adding quotations gave no significant gain." |
| `harm` | The study found a statistically significant decrease from it. | "The rewrite lowered rank, significant in 19 of 24 settings." |
| `obs_negative` | Observational comparison in the harmful direction (pages with it did worse), no experiment. | "Pages in Q&A format were less influential." |
| `survey_support` | The study is a literature survey and rates the practice as supported. | "Rated moderate to strong support." |
| `survey_caution` | The survey rates it weak, heterogeneous, or says to test without assuming a direction. | "Evidence is mixed; test it." |
| `background` | The study mentions the practice only as mechanism, hypothesis, or something it did not test. | "We hypothesise that this might matter." |
| `empty` | The study says nothing relevant about the practice. | |

## When a study is ambiguous

- Use the `where_to_look` column to find the relevant part, then search the whole paper for the practice's words before choosing `empty`. A one-line mention counts.
- A study that tested only a nearby practice (a related format, a bundle, a summary instead of the exact practice): rate what it found, using the closest label, and write `nearby` in `note`.
- Mixed results (a gain in one part, none in another): `gain_part`. A gain with a harm elsewhere is also `gain_part`; say so in `note`.
- If the paper reports a difference but no test, still call it a gain or null by the authors' own words; put `no test` in `note`.
- Gain versus null when the paper is unclear: go with the authors' own stated conclusion.
- Still torn between two labels after 5 minutes: pick the one you would defend, and write the other in `note` (for example `or null`). Do not leave it blank.
- Anything you needed to guess, or any page or table number worth keeping: write it in `note`. A short note on every close call helps us resolve disagreements later.

## Returning it

Save as `rating_sheet_<yourname>.csv` (keep the columns and rows as they are; fill only `rating` and `note`) and send it back. Do not edit the other columns.
