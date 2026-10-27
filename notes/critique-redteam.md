# Red-team critique of notes/NARRATIVE.md (draft 1)

Written 2026-10-24 by a hostile but fair reviewer, applying the Nanda checklist (memory file `feedback-paper-writing-nanda-principles.md`). Every finding below was checked against the source files; paths are given so the owner can recheck. Ordered by how hard a WWW demo reviewer would hit it.

Abbreviations as in NARRATIVE.md: CE = `../citation-equity`, LS = the landscape doc, Rnnn = corpus ids.

---

## 1. Claim 2 understates what the data show, and its key phrase is wrong (most important)

**The problem.** Claim 2 says open models cite the revised drafts "at most a few points more, an effect the bench's pre-registered sensitivity bar cannot separate". The one-line takeaway says the score is "not a lever". The sensitivity JSONs say something different:

| Model | before | after | after minus before | relative | questions up | p (sign-flip, 8 q) |
|---|---|---|---|---|---|---|
| Qwen3.5-9B | 0.164 | 0.178 | +0.014 | +8% | 5 of 8 | 0.52 |
| Gemma-4-12B-it | 0.178 | 0.201 | +0.023 | +13% | 8 of 8 | 0.008 |
| Qwen3.8-27B | 0.154 | 0.180 | +0.026 | +17% | 8 of 8 | 0.008 |
| Gemma-4-31B-it | 0.180 | 0.211 | +0.031 | +17% | 6 of 8 | 0.039 |

Source: CE/experiments/results/sensitivity/sensitivity_*.json (`summary.mean_target_share`, `summary.after_minus_before_exploratory`; per-question signs recomputed from `per_question` on 2026-10-24).

- The after draft is cited more on every model, on every question for two models, at the smallest p a sign-flip over 8 questions can give (0.0078). That is not "cannot separate".
- The pre-registered bar (H2) is about `answer_first`, a one-sentence oracle insertion, not about the after draft. Claim 2 attaches the failed bar to the wrong condition.
- "Cannot separate" is true only of the llama3.2:3b sample run (n = 4 questions, smallest p 0.125; CE/samples/README.md line 92).
- A reviewer reads this as overclaiming in the *negative* direction, which Nanda treats the same as overclaiming for attention.

**What the evidence does support.** Following the suggestions gave small, consistent, exploratory gains of +0.014 to +0.031 in citation share (8% to 17% relative) on four 9B to 31B models. This was not pre-registered as a test, it is uncorrected across 4 models x 2 contrasts, and no p reaches the p < 0.001 bar Nanda asks for in exploratory work. So the direction is suggestive, not established. Separately, a one-sentence answer-first edit missed a pre-registered +0.10 bar on all four models.

**Fixes.**
1. Rewrite Claim 2 and the takeaway: replace "barely more", "cannot separate" and "not a lever" with "small and consistent, far below the size that vendors' uplift figures imply, and not yet confirmed". A candidate: *"Following the tool's suggestions raised the draft's citation share by 1 to 3 points (8% to 17%) on four open models: a consistent but exploratory gain, an order of magnitude below the uplift figures in circulation."*
2. Keep the llama run as a demonstration of the in-tool bench, not as the evidence for Claim 2.
3. Report effect sizes with bootstrap intervals over questions, not p alone.

## 2. "The bench cannot detect a 0.10 gain" has no positive control behind it

**The problem.** NARRATIVE 1.2 says "We claim that the bench cannot detect a 0.10 share gain here", and section 2.2 calls the result "the first published measurement floor". Neither follows from the data.

- The test shows that the *edits tried* did not move share by 0.10. It does not show that a 0.10 move would go undetected. That would need a condition known to move share by at least 0.10.
- The bench did detect +0.025 at p = 0.008. So its sensitivity is better than "cannot detect" implies. The small number is the size of the effect, not the limit of the instrument.
- The only control is the off-topic floor (a negative control). There is no positive control, so the dynamic range is unknown.
- No power or minimum-detectable-effect calculation exists for the sensitivity test; PREREG_E1.md computes one for E1, in a different metric.

**Fixes (cheap; about 3 to 4 minutes of generation per model, per the `generate_seconds` fields).**
1. Add a positive control, with conditions added to `sensitivity.py`: for example, target = the most-cited competitor's text, or a dose series (answer-first for 1, 2 and 4 of the questions, or the answer sentence repeated). Pre-register it in a new commit before it runs.
2. Compute the per-question SD of the differences and report an MDE for n = 8.
3. Until then, drop "measurement floor" and "to our knowledge the first". Say only: "realistic edits moved share by 1 to 3 points; a single before/after run cannot validate GEO advice at that size."

## 3. Figure 1's headline panel mixes two metrics and two protocols on one axis

**The problem.** The planned headline plots llama share (0.087 to 0.137) and an inset of the larger models (0.154 to 0.211) as the same quantity. They are not the same quantity.

- **Shipped bench (llama).** The metric is the GEO paper's position-adjusted word count (PAWC; CE/NOTICE, `packages/bench/src/metrics.ts`). BM25 retrieves the top 8, so the draft can be missing: espresso before was retrieved in 24 of 32 runs, and its even-split level is 0.094, not 0.125 (CE/samples/README.md line 90).
- **Sensitivity test.** The metric is citation markers pointing at the target divided by all markers (`experiments/explorer/sensitivity.py` line 96). The target is always inserted among the 8 sources (no retrieval), and whole pages are passed.
- NARRATIVE R8 calls the sensitivity metric "PAWC". It is not.
- The visual point, "long horizontal arrows, short vertical ones", comes from the axis scales: a 0 to 100 score against a 0 to 1 share. A reviewer will call it a chart crime.
- "Roughly doubles" holds for espresso (35 to 73, 2.1x) but not RAG (45 to 76, 1.7x), and less so on the evidence preset (37 to 70 and 48 to 74; re-run with `ce analyze --json` on 2026-10-24).

**Fixes.**
1. Base the headline on the sensitivity data (4 models, n = 8, paired) rather than the n = 4 llama run.
2. Put both quantities on one relative scale: percent change in score and percent change in share, per model, side by side. Or use two small panels with honest axes.
3. Name the metric in every caption. If llama and sensitivity results share a figure, either recompute marker share for llama from `recording.json` or recompute PAWC for the sensitivity `rows`.
4. Write "raises 35 to 73 and 45 to 76", not "doubles".

## 4. The score rise is built in, and the after drafts carry a length confound

**The problem.**
- The after drafts were written by acting on the tool's own suggestions (CE/samples/README.md Protocol step 3). The tool's score therefore has to rise. Presenting "the score rises a lot" as half of a finding treats a tautology as a result.
- There are two rewrites (one per topic), both by the tool's authors. The protocol order (committed before any run) answers tuning to the bench. It does not answer that n = 2, or that the rewriter is the builder.
- The after drafts are longer: espresso 831 to 946 words (+14%), RAG 1,041 to 1,275 (+22%) (`wc -w` on samples/*/{before,after}.md). Longer pages get more PAWC words and more chances to be cited. The water-temperature retrieval gain (0 of 8 to 8 of 8) is plausibly added keywords. There is no length-matched placebo for after against before; E1's placebos exist for exactly this reason.
- The before drafts already sit above chance against the synthetic competitors (0.154 to 0.180 against 0.125). So the result depends on how good the authors made the synthetic pack, which is a design choice, not a property of the web.

**Fixes.** Frame the score change as "what following the advice looks like on the checklist", not as evidence. Report the lengths. Name length as the main confound and point to E1's placebos. State that the competitor pages are synthetic and that the baseline share is above chance.

## 5. "0 of 10 checks strong or moderate" is mostly a property of the rubric

**The problem.** A reviewer will say the rubric was built so that nothing can pass. The files give them material:

- **Asymmetry.** Observational studies "cannot by themselves make it strong" (CE/docs/evidence.md line 31), yet an observational negative can make a check mixed (question headings: Q&A format 5.74% lower influence, observational).
- **Non-significance counted as a null.** Comparisons: What Gets Cited found positive odds ratios in all six models (7.45, 4.55, 4.72, 2.14 significant; 1.78 and 1.61 not), and the check is graded mixed. Question coverage: ConflictingQA reports "a substantial positive effect", Martinez rates relevance "strong in controlled settings", What Gets Cited is significant in 4 of 6, and the check is graded mixed. Absence of evidence in two subgroups is not a null result.
- **One label for very different evidence.** "Mixed" covers "positive in every model, significant in four" and "lowered rank in 19 of 24 settings" (statistics).
- **Indirect nulls used as direct.** The What Gets Cited formatting factors are section organisation and grouping. "Lists, tables and question headings were not tested one by one" (CE/docs/research/evidence-notes.md line 50). The paper still uses that null against lists and question headings.
- **Single rater**, with no agreement statistic.
- **Two standards.** Site readiness reaches strong on operator documentation (evidence.md line 209). Fine, but the paper must not set "2 strong" beside "0 strong" as if the bar were the same.
- **Missed irony.** Question coverage, the best-supported check in the literature, is the one the answer_first condition tests, and it moved in the expected direction.

**Fixes.**
1. Phrase the result as rubric-relative: "under a rule where any null, even in a subgroup, makes a check mixed, none qualifies".
2. Add a one-row sensitivity analysis: grades under a looser rule (null = a significant null or harm only). Comparisons and question coverage probably move to moderate. Showing that the conclusion moves is what makes the rubric credible.
3. Have Ishan grade the 10 checks blind from the same sources and report agreement. This takes an afternoon.
4. Keep Figure 3, and do not cut it first. A matrix with direction and significance per cell is the only way a reader can see that "mixed" is not "no effect". Cut Figure 4b instead (see 8).

## 6. Novelty is narrower than written: credit R39, aiseo-audit and SAGEO up front

**The problem.**
- **R39 (Bajemon and Rochet, arXiv 2609.07559).** Its corpus summary says that re-measuring "the 2023 levers" on ten modern engine families moved citation on none. That is the null in Claim 2, on stronger setups. NARRATIVE cites R39 only as "a content score as a stand-in". It must also be cited as prior evidence for the null. It is vendor-linked and not peer-reviewed; say so.
- **aiseo-audit.** It already tags lists, tables and answer capsules "diagnostic", citing the same C-SEO "19 of 24" and What Gets Cited formatting null (CE/docs/research/2026-10-23-oss-sweep.json, entry verified in a clone). Novelty item 1, "a rubric that lets a null count", is therefore an increment on aiseo-audit: an explicit decision rule, and surfacing it to the author in the UI.
- **Retrieved against cited.** "No product separates retrieved from cited" (LS line 508) is a claim about products. SAGEO Arena (research) measures each stage separately, and the narrative's own evidence table says so ("Visibility at each stage separately"). Say "among the commercial and open tools we surveyed".
- **Firsts.** "To our knowledge, the first published measurement floor" should go (see 2).

**Fix.** One honest novelty sentence: *the contribution is putting graded evidence, a self-test that separates retrieval from citation, and a pre-registered sensitivity result into one offline, author-side tool that shows the author all three.* Each component has prior art, named.

## 7. "The tool measures its own advice" overstates what the tool ran

**The problem.**
- The 9B to 31B results come from a separate Python harness on a GPU cluster (`experiments/explorer/sensitivity.py`). It uses a different metric, no retrieval and whole pages. Byte-identity with `packages/bench/src/prompt.ts` was not checked for this test; it is only planned for E1 (PREREG_E1.md line 114).
- What the author can run on a laptop is the 3B bench, which is also the noisiest result.
- "No server and no paid API" is true of the static site and the 3B bench. The stronger evidence needed an HPC cluster. Also check whether `ce live` on Gemini needs an API key, and word it accordingly.

**Fixes.** Say "a companion harness, using the bench's prompt, on larger open models". Run the 10-prompt byte-identity check against `--export-prompts` now, since it is cheap, and report it. State that the in-browser test is a demonstration, and that the claims rest on the cluster runs.

## 8. Claim 3 is not a claim; drop the placeholder figure

**The problem.**
- E1 has no results.
- PREREG_E1.md line 3 still reads "frozen at commit `<hash>`", so the paper cannot yet call E1 pre-registered.
- A 4-page demo paper that spends about 0.3 page on a placeholder figure and a design paragraph invites the review "incomplete; resubmit when done".
- E1's MDE (0.018 to 0.021) is in first-citation rank-score units. Set beside Claim 2's share differences it will confuse readers.
- PREREG_E1.md line 194 admits that the judges come from a test whose H2 failed. The sensitivity pre-registration said "A model that fails H2 is dropped from E2". A reviewer who reads both will ask why the failed models judge E1. "E2" never needs to appear in the paper.

**Fixes.**
1. Default to the fallback now, not on about 12 Nov: E1 becomes two or three sentences of future work, with a pointer to the frozen plan once the hash exists. Remove Figure 4b.
2. Promote Claim 3 back only if results exist with the required n by about 9 Nov (owner's call).
3. Remove "E2" from the paper. Explain in one clause why the E1 judges are kept: they were chosen for consistency, not for H2.

## 9. The pre-registration story needs one more honest sentence

**The problem.**
- The H2 bar asked a one-sentence insertion to lift share from about 0.16 to about 0.26, a 60% relative gain. That bar was ambitious, and the paper should say so plainly, not only "kept, not moved".
- PREREG_sensitivity.md's fallback says that if all models fail, report "the bench cannot detect content differences with these models". The data show the opposite: relevance is detected sharply, and small edits move share consistently. Following the fallback text verbatim would put a false sentence in the paper.

**Fix.** Report H2 as failed. Then say in one sentence that the planned fallback wording does not fit the data, and why. That is a labelled deviation, which is exactly what pre-registration is for.

## 10. Selective reporting in the per-question bullets

**The problem.**
- "No single question gained 0.10 for any model (largest answer_first gain 0.088)" is true for answer_first only. In the after condition, Gemma-4-31B gained 0.141 on one question (recomputed from `per_question`).
- Heterogeneity is not mentioned. Qwen3.5-9B after minus before is +0.034 on espresso and -0.007 on RAG. Gemma-4-31B answer_first is 4 up and 4 down.

**Fix.** Report the maximum for both conditions, and show the per-question dots in Figure 4a (already planned). Mention the split by sample in one clause.

## 11. Demo-track fit: the system is under-shown

**The problem.**
- Reviewers judge a demo paper on the system. The plan gives about 600 words and two of four figures to the bench.
- Figure 2, the only image of the system, is a placeholder for an unshipped redesign. "Implemented and tested" is a stated requirement of the call.
- There is no evidence of use at all: no users, no analytics (by design), no user study. That is acceptable, but it must be said in one line.

**Fixes.**
1. Put a real screenshot in Figure 2 now (CE/docs/screenshot.png, or a Playwright capture of the current deploy), and swap it later if the dashboard ships.
2. Rebalance toward the system: architecture, the evidence-to-UI path, per-span Apply, and the venue script.
3. Keep the results to one figure (4a, or fold it into Figure 1).

## 12. Citation hygiene: three items to fix before refs.bib

1. **R77 "cut click-through by 18.8 pp".** The number is not in the arXiv abstract (fetched 2026-10-24) or in the corpus `key_numbers`. Verify it in the full text, with table or section, or drop the number. "Preregistered" is confirmed: the abstract says "We conduct a preregistered field experiment (N=1,100)". The corpus verifier had left that unchecked.
2. **What Gets Cited "over 252,000 trials".** 252,000 is the whole study, across 18 factors and six LLMs (evidence-notes.md line 45); formatting-only is a subset. Write "in a 252,000-trial study of 18 factors, formatting-only edits had little impact", and note that lists and headings were not isolated.
3. **"Entry prices run up to $800/month (Evertune Pro)".** This mixes tiers. Write "listed tiers range from free trials to $800 per month". The "24 products" count checks out (24 rows in the LS table).
4. **The LS landscape doc is internal and unpublished.** Quotes such as "Every product here assumes a brand with competitors" are the authors' own words. Present them as "our review of 24 product pages (October 2026)" and cite the product pages, not LS.
5. **Pew (R76).** Use the verified wording: users clicked a result on 8% of visits with an AI summary against 15% without, and clicked a link inside the summary on 1%. The arXiv extension (2608.04831) has a different title; use the right one if it is cited.
6. **Martinez quotes.** Section 11.1, Section 11.2 ("placebo of comparable length", "outcomes, not data to be discarded"), Section 13.7 and the Table 5 "Rejected as a general claim" entry all verified in the PDF text. Keep them.
7. Label R39, R243 and R250 as vendor, trade press or non-peer-reviewed in the text, not only in comments.

## 13. Illusion of transparency: terms a WWW reader will not know

The following appear without a definition, or with two meanings: PAWC; "share among valid answers"; "chance level", which holds only when the draft is retrieved; format failure; k; the foundation and evidence presets; `answer_first` / "oracle"; off-topic floor; mixed; E1; E2.

**Fixes.**
- Define each once, in the intro or in 2.5, in plain words.
- Rename `answer_first` in the paper to "one-sentence answer edit".
- Drop "oracle" and "E2".
- Give each metric one name and use it everywhere.

## 14. Space: the budget does not fit four pages

- Title block (0.35 page), about 22 references (about 0.45 page in sigconf), a figure* (0.33 page) and three single-column figures (about 0.45 page) leave about 2.4 pages of text. That is about 2,300 words, not 2,650 (the running total is already 2,750).
- **Fix.** Plan for 3 figures (1, 2 and 3; 4a folded into Figure 1 or into a half-width panel), about 15 references and about 2,100 words of body.

## 15. Smaller points

- **Dilution.** The dilution account (6.2 to 7.0 of 8 sources cited) is post hoc. A page's share is not capped at 1/6.5. Keep it labelled exploratory, and note that E1's 4-source design is its test.
- **The CE/README.md "37 to 72" inconsistency.** Already flagged by the narrative. The re-run confirms 35 to 73 and 45 to 76 (foundation). Owner to fix the README.
- **HCI motivation (R93, R100, R102).** It supports the design intent only. AnchoredAI is N = 22 and a preprint. Do not imply the tool raises agency.
- **Dual use.** The ethics section should also say that the bench can test manipulative edits as easily as honest ones, and that the shipped tool offers no such arms.

---

## Priority list (do in this order)

1. Rewrite Claim 2 and the takeaway to match the after minus before data (small, consistent, exploratory gain). Drop "cannot separate" and "not a lever".
2. Add a pre-registered positive control to the sensitivity harness, or drop "cannot detect 0.10" and "measurement floor".
3. Rebuild Figure 1's headline on one metric and a relative scale. Fix R8 (the sensitivity metric is marker share, not PAWC).
4. Name the built-in score rise and the length confound (after drafts 14% and 22% longer).
5. Make the rubric result rubric-relative. Add a looser-rule row and a second rater. Keep Figure 3.
6. Credit R39 (the same null on ten engine families), aiseo-audit (diagnostic tags from the same studies) and SAGEO (stagewise visibility) in the novelty paragraph.
7. Reword "the tool tests its own advice" to reflect the separate cluster harness. Run the byte-identity check.
8. Demote E1 to future work now, and remove Figure 4b and "E2".
9. Add the labelled pre-registration deviation sentence.
10. Report the after-condition maximum (0.141) and the heterogeneity.
11. Use a real screenshot of the shipped UI for Figure 2.
12. Fix R77 18.8 pp, the 252,000 wording, the price phrasing and the LS self-citations.
13. Add the glossary and renames.
14. Re-budget to about 2,100 words and 3 figures.
