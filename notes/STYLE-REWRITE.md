# Style rewrite (2026-10-24): planning stated plainly, no lab-notebook labels

Brief: `../citation-equity/.superpowers/sdd/2026-10-23-citation-equity/task-PAPERSTYLE-brief.md`.

What changed: the words pre-registered / registered / preregistered / frozen, the commit hashes 3c86c02 and 4d77fa0, the run-in labels "Exploratory" and "(E1)" are gone from the rendered text. Planning is stated once, in an ordinary sentence, where each test is introduced. Every number, interval, p value, n, model name and citation is unchanged; no claim was added; all `% src:` comments and `\owner{}` marks are kept (two new src comments sit above the two new planning sentences). No text was cut; the build stays at 4 pages.

Left as they are, for the owner to judge:
- "post hoc" (Section 2.1 and the Figure 3 caption: "a looser rule, defined post hoc") is an ordinary phrase, not a run-in label, so it stays.
- The owner mark "Who presents, and registration." (venue registration) contains "registration"; owner marks are kept.
- The aiseo-audit reference prints "Commit 6c888aa" in the bibliography; references are unchanged.
- Intro: "In a preregistered field experiment" describes the cited study (Wang et al.), whose registration a reader can check. It became "planned in advance" only because the brief bans the word everywhere; restoring it there is reasonable.
- Keyword "pre-registration" became "null results"; any other keyword works.

## Changed sentences (old -> new, LaTeX source)

1. `main_www.tex`: Figure 1 caption: 'pre-registered' and the 'exploratory' label replaced by a plain statement of what was and was not planned.

   - old: \panel{b} Citation share of the target in the pre-registered harness (synthetic competitors), one line per model; the contrast is exploratory.
   - new: \panel{b} Citation share of the target in the sensitivity harness (synthetic competitors), one line per model; no target was set in advance for this contrast.

2. `main_www.tex`: Keywords: the banned word removed; 'null results' names the paper's rule for nulls (owner may prefer another keyword).

   - old: evidence grading, pre-registration}
   - new: evidence grading, null results}

3. `sections/abstract.tex`: Abstract: run-in '(exploratory)' and 'pre-registered bar' replaced.

   - old: On our two sample drafts, following its suggestions raised that score from 32 to 69 and from 44 to 72 but moved mean citation share on four open models by only 1 to 3 points (exploratory), and a one-sentence answer edit missed a pre-registered bar of $+0.10$ on all four.
   - new: On our two sample drafts, following its suggestions raised that score from 32 to 69 and from 44 to 72 but moved mean citation share on four open models by only 1 to 3 points (no target set in advance), and a one-sentence answer edit missed a $+0.10$ target we set in advance on all four.

4. `sections/abstract.tex`: Abstract: planning stated plainly where the second test is introduced.

   - old: In a second pre-registered test of each suggestion alone on 80 real web pages, only edits that add the question's own words raised citation, by about 0.03 on a 0-to-1 scale, and most checks applied to too few pages to judge.
   - new: A second test, planned before any page was edited, applied each suggestion alone to 80 real web pages: only edits that add the question's own words raised citation, by about 0.03 on a 0-to-1 scale, and most checks applied to too few pages to judge.

5. `sections/intro.tex`: Intro: describes the cited study (Wang et al.), not ours; reworded only because the brief bans the word everywhere in the rendered text. Owner may restore 'preregistered' here, since that study's registration is public.

   - old: In a preregistered field experiment, a search page
   - new: In a field experiment planned in advance, a search page

6. `sections/intro.tex`: Intro contributions: 'pre-registered' replaced.

   - old: a self-test of the advice, and a pre-registered check of that test's sensitivity.
   - new: a self-test of the advice, and a check of that test's sensitivity against targets set in advance.

7. `sections/intro.tex`: Intro findings: 'pre-registered bar' replaced.

   - old: and a one-sentence answer edit missed a pre-registered bar of $+0.10$ on all four.
   - new: and a one-sentence answer edit missed a $+0.10$ target we set in advance on all four.

8. `sections/intro.tex`: Intro contributions list: 'pre-registered results' replaced.

   - old: and a citation test inside the tool, with two pre-registered results
   - new: and a citation test inside the tool, with the results of two tests planned in advance

9. `sections/evidence.tex`: Section 3 run-in heading: takeaway first (matches 'On a laptop, the test demonstrates the loop.'), banned word removed.

   - old: \paragraph{A pre-registered sensitivity test.}
   - new: \paragraph{On larger models, an answer edit fell short of its target.}

10. `sections/evidence.tex`: Sensitivity test: commit hashes removed; planning stated once, plainly, where the test is introduced.

   - old: Four open models (Qwen3.5-9B, Gemma-4-12B-it, Qwen3.8-27B, Gemma-4-31B-it) gave 256 valid answers each, and the plan (\texttt{3c86c02}) preceded the results (\texttt{4d77fa0}).
   - new: Four open models (Qwen3.5-9B, Gemma-4-12B-it, Qwen3.8-27B, Gemma-4-31B-it) gave 256 valid answers each. / % src: plan 3c86c02 written before results 4d77fa0 (CE/experiments/PREREG_sensitivity.md, "Criteria (fixed before running)") / We wrote the design and success criteria before the results; the plan is in the repository.

11. `sections/evidence.tex`: Sensitivity test: 'registered bar' -> 'the +0.10 target' (the planning was stated in the sentence before).

   - old: gained only $+0.007$ to $+0.034$ against a registered bar of $+0.10$, which the harness could have detected (0.019 to 0.069).
   - new: gained only $+0.007$ to $+0.034$ against the $+0.10$ target, which the harness could have detected (0.019 to 0.069).

12. `sections/evidence.tex`: Sensitivity test: run-in 'Exploratory:' label replaced by an ordinary sentence (it changes how the number should be read).

   - old: Exploratory: the after drafts raised mean share on every model by $+0.014$ to $+0.031$ (8\% to 17\%), but they are also 14\% and 22\% longer.
   - new: The plan set no target for the full after drafts, which raised mean share on every model by $+0.014$ to $+0.031$ (8\% to 17\%) but are also 14\% and 22\% longer.

13. `sections/evidence.tex`: Section 3 run-in heading: the internal label 'E1' dropped.

   - old: \paragraph{Which single suggestions change citation (E1).}
   - new: \paragraph{Which single suggestions change citation?}

14. `sections/evidence.tex`: Per-suggestion test: 'frozen before any page was edited' moved into a plain planning sentence (next entry).

   - old: To separate the advice from length, a second test, frozen before any page was edited, applies each suggestion alone
   - new: To separate the advice from length, a second test applies each suggestion alone

15. `sections/evidence.tex`: Per-suggestion test: planning stated once, plainly, where the test is introduced (sentence from the brief).

   - old: 60 C-SEO Bench queries~\cite{puerto2025cseo} replicate the text edits.
   - new: 60 C-SEO Bench queries~\cite{puerto2025cseo} replicate the text edits. / % src: CE/experiments/PREREG_E1.md status line (fixed at 7859b07 before any page was edited; amendments 1-10 at its end) / We fixed the design, sample and analysis before editing any page; the plan and its amendments are in the repository.

16. `sections/evidence.tex`: Per-suggestion test: 'registered' replaced; 'as planned' marks that the outcome follows the plan's rule.

   - old: Lists showed no effect beyond the registered $\pm 0.03$, so by our rule it becomes an unscored note;
   - new: Lists showed no effect beyond the $\pm 0.03$ margin we set in advance, so, as planned, it becomes an unscored note;

17. `sections/conclusion.tex`: Limitations: the internal label 'E1' replaced by the name the prose uses.

   - old: the sensitivity test covers two synthetic topics and 8 questions, E1 140 English queries edited by one model family,
   - new: the sensitivity test covers two synthetic topics and 8 questions, the per-suggestion test 140 English queries edited by one model family,

## Follow-up (main session, after review)
- Abstract: "(no target set in advance)" dropped; "missed a +0.10 target we set in advance" -> "fell short of its +0.10 target".
- Intro: Wang et al. is again "a preregistered field experiment" (their study, checkably registered; the rule targets our own wording). "missed a +0.10 target we set in advance" -> "fell short of its +0.10 target"; contributions: "with the results of two tests planned in advance" -> "with two tests of whether the advice changes citation".
- Figure 1 caption: "no target was set in advance for this contrast" dropped.
- Section 3: "the +-0.03 margin we set in advance, so, as planned, it becomes" -> "the +-0.03 margin we set beforehand, so it becomes".
Planning is now stated where each test is introduced (Section 3) and in the abstract's E1 sentence ("planned before any page was edited").
