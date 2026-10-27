# Simulated WWW 2027 demo-track review (final polish build)

Reviewed: `main_www.pdf` after the 2026-10-26 polish. It has 4 pages including references, five authors and six
visible owner marks. The reviewer stance is a demo-track PC member who reads the PDF and opens the demo, the
repository and the Hugging Face data (all HTTP 200 on 2026-10-26). It is written by the same assistant that
polished the paper, so it is not independent.

## Scores (1 to 5)

| Criterion | Score | Note |
|---|---|---|
| Originality | 4 | Few tools grade their own GEO advice or test it, and fewer ship the nulls. |
| Significance | 3 | The advice audience is real; the effects are small and measured on open models only. |
| Quality | 4 | Plans were committed before the runs, there is a recompute script, and the limits are stated plainly. |
| Clarity | 3 | The paper is dense. Three outcome metrics (word share, citation share, rank score) and arm names vs check names take work to follow. |
| Demo value | 4 | The demo is live, static and offline at the booth, with a 90-second loop and a bring-your-own-text station. |
| **Overall** | **Weak accept** | It becomes an accept once the video and the second rater land. |

## Strengths

1. **An honest stance that is rare in this space.** The tool calls its score "a writing checklist, not a forecast",
   counts any null against a check, and reports that its own suggestions barely move citation. Then it changes
   the tool (four unscored notes, one new check) from its own tests.
2. **Research hygiene.** The sensitivity bar is set in advance and reported as missed. E1 is frozen before any page
   was edited, E2 and E3 are planned before their answers, and there are replication and editor/judge swaps. The
   withdrawn first recording is reported, not hidden.
3. **Figure 3** makes "mixed" inspectable: one glance shows which studies found what, under the strict and the
   looser rule.
4. **Deployable and private.** The tool has no server, a browser test asserts no request leaves the origin, the
   code is MIT, the data is public with the page text gated, and the booth runs without venue network.
5. **The ethics section is specific:** dual use, robots.txt, no redistribution, invented sample pages, and gated
   research-only page text.

## Weaknesses

1. **The effects are small and indirect.** About 0.03 on a 0-to-1 score, from local judges over four fixed sources.
   The adjusted effect includes zero once length and question-word changes are regressed out.
2. **No live-engine or user evidence.** Every result uses open models over fixed sources. There is no study with
   writers, and "Tests Its Own Advice" in the title leans on an external cluster harness rather than the in-tool
   laptop bench, which "shows a direction at most".
3. **Single-rater evidence coding** for Figure 3, still marked for the owner.
4. **Density.** Three metrics across three test setups, Figure 4 rows named by experiment arm ("Query words in
   title") rather than by check, and a heavy Section 3 make the main result harder to extract than it should be.
5. **Under-shown interaction.** One screenshot and a schematic. The video is still a placeholder, and Figure 1's
   card shows a grade chip the current draft view no longer shows.

## The three most likely objections, and how the paper answers them

1. **"The tool's advice does not work, so what is being demonstrated?"**
   The paper makes this its point rather than hiding it. The checklist score rises by design. Citation moves 1 to
   3 points in the sensitivity harness, and only the reader's-words change clearly helps one change at a time
   (Abstract, Section 3, Figures 1 and 4). The tool then acts on its own tests: four checks become unscored notes
   and a reader's-words check is added (Section 2.1). The demo is a tool that tells writers what the evidence
   supports, which the related tools do not do (Section 4). *Residual risk:* a reviewer who wants a positive
   system result may still score significance low.
2. **"Open models over four fixed sources are not ChatGPT or Perplexity."**
   This is stated in the abstract ("All tests use open models given fixed sources, not live engines"), in the
   bench's own report text ("It does not predict live AI engines"), and in the Limitations, which name live-engine
   comparison as next work and cite drift [9]. Related work says the paper does not claim the score predicts
   citation. *Residual risk:* none beyond scope; the paper does not overclaim here.
3. **"The gains are length or keyword overlap, not better writing."**
   Each edit is compared with a same-length paraphrase of the same spans. The text reports that the adjusted
   effect includes zero after regressing out length and question-word changes, and Figure 4 marks "helps*:
   possibly via question-word overlap". E2 separates the heading form (no effect) from the question's words (the
   gain), and the after drafts' 14% and 22% length increase is stated. *Residual risk:* the paper concedes the
   mechanism may be overlap. That is honest, but it leaves "why it helps" open.

## Before submission (from the reviewer's view)

- Record and link the video (Station 1, about 2:30). This is the largest gain for a demo paper.
- Get a second rater for Figure 3, or keep "One rater." and accept the hit.
- Optionally relabel Figure 4's rows with the check names used in Figure 3 and the text.
