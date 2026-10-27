# Citation Equity: redesign, E5 plan and schedule to Nov 16

Written 2026-10-27 for our own reference. This is the work for weeks 9 and 10 (Nov 2 to 15) and the new framing of the paper. Nothing here is built or run yet.

The current draft (commit 93e151f, 4 pages, numbers check passing) stays complete and submittable as a fallback if the build or E5 slips.

---

## Part 1. Summary of the redesign

### What our tests found

| Finding | Source |
|---|---|
| Only one kind of edit clearly raised citation: the reader's own words near the top of the page (+0.035 vs a same-length paraphrase), and answering the reader's question in a section under the title (+0.027). | E1 arms 12 and 9 |
| The gain comes from the question's words, not from the heading form. | E2a |
| It kept its sign with a different editor model and other judges. | E2b |
| Question headings, lists, cited sources and direct answer first: no effect larger than 0.03. | E1, E3 (260 queries) |
| Attributed quotes: inconclusive (+0.026). Statistics, tables, comparisons: too few pages to judge. | E3 |
| All fixes together: +0.049 vs the original page, +0.071 vs a paraphrase. The two contrasts cover different query sets (n 78 and 53), so the gap between them is at most a weak hint that rewording a page away from its own words costs citation. | E1 |
| A page that blocks the engines' search crawlers, or is marked noindex, cannot be cited at all. This is the strongest evidence in the tool, from the engines' own documentation. | Site readiness evidence |

Every test used open models given fixed sources, not live engines. The effects are small.

The gap that matters most for real use: in E1 to E3 the edit was made with the reader's exact question. A real writer has to guess it. E5 (Part 2) tests that.

### What changes in the tool

The three-module architecture stays: diagnostic engine, test bench, and a workspace that suggests and never rewrites. What changes is the content of the checks and how the result is shown.

1. **No composite score.** Remove the "AI-ready score" from the app and the "GEO Score" from the command line and docs. The present weights give the four untested original checks about 73% of the score and the one tested check about 10%, so the number mostly measures checklist compliance. The engine keeps custom-weight scoring for researchers, and the app never shows a total.
2. **Start from the reader's questions.** The home page asks "What will your readers ask?": paste keywords, import Search Console or Bing data, or type questions. Today's Your questions view moves to the front. The example draft still loads in one click.
3. **"Questions covered: N of M" replaces the score.** For each question:
   - are its key words in the title, first heading or first paragraph? Missing words are named, never inserted;
   - does some section answer it directly?
4. **Other writing notes are collapsed and unscored.** The other nine checks stay as advice, each labelled "no effect in our test", "unclear" or "not tested".
5. **"Can engines reach it?"** Site readiness is shown as blockers (crawler access, indexing rules, renders without JavaScript), not as a score. Any blocker also shows on the home page.
6. **"Did it change anything?"** The Who gets cited bench stays, with its caveat: open models given fixed sources, a direction at most.
7. The Research page stays the evidence page. It gets an entry for E5.

Flow: Your readers' questions → Your draft (questions covered, then notes) → Can engines reach it? → Did it change anything?

### Likely new framing of the paper

- **Working title:** "Citation Equity: A Writing Tool Rebuilt Around the GEO Advice That Held Up in Testing".
- **Story:** small publishers are sold advice for being cited by AI engines whose value is unknown. We built that advice as an 11-check tool and tested each change on real pages against a same-length paraphrase. Only the reader's words near the top helped. So we removed the score, rebuilt the flow around the reader's questions, and kept the rest as labelled notes. The equity point: what helps costs nothing. Write in your readers' words, and do not block the crawlers.
- **Structure (4 pages):**
  1. Introduction: the problem and the equity angle.
  2. What we tested: E1 to E3, plus E5, compressed. The forest plot is the main figure.
  3. The tool: a before/after figure (checklist score vs question-first screen), the evidence ledger and the rule for nulls.
  4. Demo stations.
  5. Related work, limitations (open models, small effects, the sensitivity target we missed), ethics.
- **Why it is stronger:** the main reviewer objection so far is "the tool's own advice barely works, so what is the demo?" The new version makes acting on that result the demo.

---

## Part 2. E5 plan (draft; final version committed to the tool repo before any run)

### Question

Does the reader's-words gain survive when the writer has to guess the reader's question?

E5 reuses E1's pages, prompts, judges, seeds, citation score and statistics (experiments/PREREG_E1.md). Only the question used to make the edit changes. Every answer is still judged against the true query q.

### Versions

For each query q, a guessed question q' is built without reading q's wording, except through the keyword as stated below.

| Version | Edit | Question used | Simulates |
|---|---|---|---|
| 9 / 12 (from E1) | arm 9 (question as a section under the title) / arm 12 (missing key words worked into title, first heading, first paragraph) | q | the writer knows the exact question |
| 9K / 12K | the same edits | q' = `keywordQuestion(k)`, the tool's top template for keyword k | a writer with a Search Console style keyword |
| 9G | arm 9 | the page's own title or topic question (`pageQuestionsOf`) | a writer who enters nothing (the tool's default) |
| P12K | arm 12's placebo on 12K's spans | none | length control for 12K |

**Keyword k (to settle before the run):** the query's two highest-weight key terms in its original order, as a stand-in for the short phrase Search Console shows. This leaks part of q on purpose, since a real keyword is a real reader query. The report gives each q'-to-q key-term overlap, and the analysis uses it as the dose.

### Contrasts

Unit: the query. d is averaged over 8 seeds, then over the two judges, as in E1.

- **Planned (one Holm family, alpha 0.05):**
  - 9K vs original
  - 12K vs P12K
- **Reported without a verdict:**
  - 9G vs original
  - 9K vs 9 and 12K vs 12 (the loss from guessing)
  - the share of the true-question gain that is kept
  - d against q'-to-q overlap
- The replication set (C-SEO Bench) is run the same way and reported separately.

Labels as E1: helps, hurts, no effect larger than 0.03, inconclusive, insufficient n (fewer than 30 analyzable queries).

### What each result means for the tool

| Result | Tool | Paper |
|---|---|---|
| 9K and 12K help | the question-first flow stands; templates are a reasonable start | "the gain survives a keyword-level guess" |
| They do not help, but 9 and 12 did | the lever needs the reader's real words: import real queries first, label templates "a guess" | stated as the main limit |
| Inconclusive | no change; say so | reported as inconclusive |
| 9G helps | the default with no input is useful | noted |

### Size and runs

- **Power:** about 54 main queries for arm 9 and 33 for arm 12 (E1's valid sets). With E1's spread, the smallest detectable difference is about 0.02. The arm 12 side may be too small for a verdict, and we accept that.
- **Editing:** one Gemma job for 12K and P12K, the same editor and validators as E1. 9K and 9G are deterministic.
- **Judging:** about 80 queries × 4 versions × 8 seeds × 2 judges, about 5,100 answers on the main set, plus the replication set. Original and E1 answers are reused.
- **Compute:** about 4 to 6 GPU-hours on Explorer, E1's allocation, offline GPU jobs, smoke test via sbatch first. No paid API.

### What we will not do

No change to E1 to E3 results. No new arms. Any choice made after the answers exist is reported as an added analysis. Amendments are dated and made before the answers are read.

---

## Part 3. Schedule to Nov 16

Week 8 (Oct 26 to 27) is finished: the paper draft (93e151f), the video (https://youtu.be/kbU9t3ewVUk) and the live links.

### Week 9 (Mon Nov 2 to Sun Nov 8): build and run

| Day | Work | Who |
|---|---|---|
| Mon 2 | Share links with the team; redesign screens and copy | Ali |
| Mon 2 to Tue 3 | Finalize the E5 plan; commit PLAN_E5.md to the tool repo before any run; smoke test on Explorer | Ali (+ agents) |
| Wed 4 to Fri 6 | Build the redesign: question-first home, questions-covered count, collapsed notes, blockers, score removed from engine, CLI and docs, tests updated; publish to public main after the privacy scan | agents, Ali reviews |
| Wed 4 to Thu 5 | E5 runs (edit job, then judging) | cluster |
| Fri 6 | Second-rater sheet back (about 2.5 to 3 h) | Ishan |
| Sat 7 to Sun 8 | E5 analysis and RESULTS_E5.md; Research page entry; rater agreement into the paper | agents, Ali |
| Sun 8 | Team sync: try the new flow on a real page | Ali, Ishan, Akshay |

### Week 10 (Mon Nov 9 to Sun Nov 15): paper, video, checks

| Day | Work | Who |
|---|---|---|
| Mon 9 to Tue 10 | Rewrite the abstract, introduction and tool section around the new framing; new Figures 1, 2 and 5; E5 into Section 2 | agents, Ali |
| Tue 10 | Re-record the video with the existing pipeline; Ali uploads it unlisted (new link or replace) | agents, Ali |
| Wed 11 | Full draft to co-authors for review | Ali |
| Thu 12 to Fri 13 | Resolve reviews; hostile-reviewer pass; numbers checked against data | agents, Ali, Ishan, Akshay |
| Sat 14 | Clean-run test of the reproducibility package; link check | agents |
| Sun 15 | Final sign-off from Prof. Akram and co-authors | all |

### Mon Nov 16 (AoE): submit

Final read, page-limit and format checks, submission form, upload the paper and video, check the submitted version.

### Risks

- **E5 slips or fails:** the redesign does not depend on E5's verdict. The paper reports E5 as inconclusive or leaves it out.
- **Build slips past Fri Nov 6:** cut the "Can engines reach it?" restyle first. The score removal and the question-first home are the core.
- **Video:** keep the current upload until the new one is checked.
