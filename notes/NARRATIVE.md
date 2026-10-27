# Narrative: Citation Equity, WWW 2027 demo paper (Nanda steps 1 to 3)

Status: DRAFT 2, 2026-10-24. Revised after two critiques (`notes/critique-pc.md`, `notes/critique-redteam.md`); what changed and why is in "Changes after critique" at the end. Nothing here is final until the owner reads it. Items marked **[OWNER]** are his call.

Target: The Web Conference 2027 (Dublin, 12 to 14 May 2027), demo track. Deadline 16 Nov 2026 AoE; notification 4 Jan 2027; camera-ready 31 Jan 2027.

What the call requires (read 2026-10-24 at https://www2027.thewebconf.org/demos/; full list in `notes/VENUE.md`):

- At most 4 pages **including references**; `\documentclass[sigconf, screen, review]{acmart}`.
- **Single-blind**: names, the live demo URL and the repo all appear.
- An implemented and tested system. Code, a video and a live system are "highly encouraged".
- The paper states context and contributions and says **how the demo is set up at the venue**.
- A section on the **ethical use of data and/or informed consent is required**.
- In-person presentation with a poster; each paper needs its own registration **[OWNER: travel, registration, who presents]**.
- Review criteria: originality, significance, quality, clarity.
- No AI-use rule on the page; ACM's authorship policy applies **[OWNER: AI-use statement]**.

Fitting topics (research-track list, read 2026-10-24): "Search, Recommendation, and Retrieval-Augmented AI"; "Responsible Web" ("the means for creators and site owners to control AI access to their content"); "Web Economics and Digital Society" ("creator compensation").

Byline (set by the owner 2026-10-26): Mohammad Ali Shehral, Ishan Gupta, Akshay Prajapati, Pegah Zargarian, Akram Bayat (last); Northeastern University, Khoury College of Computer Sciences, San Jose, CA, USA for all but Pegah Zargarian (Northeastern University, USA; alumna); emails shehral.m@, prajapati.aksh@ and zargarian.p@northeastern.edu.

Abbreviations:

- **CE** = `../citation-equity` (the tool repo; read only).
- **LS** = `our internal landscape review (not public)` (internal, unpublished: never cited as a source; its product facts are cited to the product pages themselves).
- **Rnnn** = an entry id in `our internal landscape corpus (not public)`. Every id used here has verdict `confirmed` or `corrected`; for `corrected` ids (R39, R76) the detail in `verifier_note` is the one we use.
- **S-JSON** = `CE/experiments/results/sensitivity/sensitivity_{Qwen__Qwen3.5-9B, google__gemma-4-12B-it, Qwen__Qwen3.8-27B, google__gemma-4-31B-it}.json`.

Terms, one name each, used the same way in every section, figure and caption (the glossary the red team asked for, item 13):

| Paper term | Meaning | Repo name |
|---|---|---|
| answer engine | a system that answers a question in prose and cites web sources | |
| GEO | generative engine optimization: changing a page so answer engines use or cite it | |
| checklist score | the tool's 0 to 100 content score under a weight preset | GEO Score |
| foundation preset | the PI's six checks weigh 1, the four added checks 0.5 | `foundation` |
| evidence preset | weights by grade: strong 1.0, moderate 0.7, mixed 0.25, untested 0.15 | `evidence` |
| word share | the GEO paper's position-adjusted word count, the in-tool bench's metric | PAWC, `pawcShares` |
| citation share | citation markers pointing at the target page, divided by all valid markers in the answer; the sensitivity harness's metric | `target_share` |
| chance level | the share a source gets if citations split evenly over the 8 sources given (0.125); it holds only when the page was given to the model | `chance_share` |
| valid answer | an answer with at least one in-range citation marker; others are format failures, counted separately | `valid` |
| one-sentence answer edit | the before draft with one answer sentence inserted under each question's heading; a fixed edit, not a tool suggestion | `answer_first` |
| off-topic control | the target slot filled with the other sample's before draft | `offtopic` |
| mixed | at least one study we opened found a null or negative result for the check | |

"Oracle" and "E2" do not appear in the paper. "E1" appears only as "a planned per-suggestion test".

---

## 1. What we learned, and the claims

### 1.1 What we learned (bullets, checked against the files)

**The tool**

- An author-side GEO tool can run with no server and no paid API.
  - The engine scores a draft in the browser and in Node; the hosted demo is a static export that makes no request at load except to its own origin (Playwright smoke test). Source: CE/docs/architecture.md "Testing and CI".
  - The in-tool bench runs a free local model through Ollama. `ce live` (Gemini with Google Search) is optional and needs the author's own `GEMINI_API_KEY` (CE/README.md line 93). It is tested only against recorded responses (CE/docs/roadmap.md "Open items"), so the paper says "recorded-response tested" and reports nothing from it.
- Ten checks: six from the PI's design (standalone paragraphs, question headings, lists, statistics, tables, expert quotes) and four from the literature (cited sources, direct-answer lead, question coverage, comparisons). Source: CE/docs/evidence.md line 3.
- Every check is graded strong, moderate, mixed or untested under a written rubric (CE/docs/evidence.md lines 16 to 34). Under its rule that a null or negative result anywhere, even in a subgroup, makes a check mixed: **0 of 10 checks are strong or moderate; 8 are mixed and 2 untested** (line 34). The grades rest on 9 studies, each opened on 2026-10-23 (lines 36 to 48).
  - The rubric is strict, and asymmetric in two places (red team, item 5, verified): an observational study cannot make a check strong (line 31) but an observational negative can make it mixed; and non-significance in some models counts as a null. Comparisons is the clearest case: What Gets Cited found positive odds ratios in all six models, significant in four (7.45, 4.55, 4.72, 2.14) and not in two (1.78, 1.61), and the check is mixed (CE/docs/evidence.md lines 185 to 199). Question coverage is similar (lines 168 to 183).
  - The formatting null in What Gets Cited covers section organisation and grouping; "Lists, tables and question headings were not tested one by one" (CE/docs/research/evidence-notes.md line 50).
  - "Mixed" therefore spans "positive in every model, significant in four" and "lowered citation rank in 19 of 24 settings" (statistics). The paper must show this spread, not hide it behind the label.
- Site readiness is graded on a different standard, where operator documentation counts: 7 items, 2 strong (indexing directives, AI crawler access), 1 moderate (renders without JavaScript), 2 mixed, 2 untested (CE/docs/evidence.md lines 201 to 323). This is the best-supported, most actionable part of the tool. The paper must not set "2 strong" beside "0 strong" as if the bar were the same.
- Readiness, off-page sources (8 site kinds plus blog-or-other) and real signals (logs, Bing AI Performance and Search Console exports, `ce live`) never change the checklist score. Source: CE/docs/evidence.md lines 201 to 461; CE/README.md items 1 and 4.
- The author stays in control: each suggestion is anchored to an exact text range; Apply works on one suggestion at a time and only if the anchored text is unchanged; Undo exists; there is no bulk action; an optional local model proposes wording side by side, applied only on a click. Source: CE/docs/architecture.md (Suggestions, `lib/apply.ts`); CE/README.md item 5; dashboard spec section 3 ("No bulk action anywhere").

**The in-tool bench (llama3.2:3b, what an author runs on a laptop)**

- It separates retrieved from cited, keeps format failures as outcomes, reports the chance level, and tests before against after with an exact paired sign-flip test. Source: CE/samples/README.md "What changed in the bench (report schemaVersion 2)".
- Its metric is word share (GEO's PAWC, ported in `CE/packages/bench/src/metrics.ts` lines 1 to 8 and 33 to 40). BM25 picks the top 8, so a draft can be missing: espresso before was retrieved in 24 of 32 runs, so its even-split level is 0.094, not 0.125 (CE/samples/README.md line 90).
- Sample run (2 synthetic topics, 4 questions each, 8 seeds, all 128 answers valid): word share 0.087 to 0.137 (espresso) and 0.086 to 0.095 (RAG); paired p 0.25 and 0.75; the smallest possible p at 4 questions is 0.125 (CE/samples/README.md lines 81 to 92). One gain is retrieval: the espresso after draft is retrieved for the water-temperature question in 8 of 8 runs against 0 of 8 (line 91). This run **cannot separate** a difference from noise, and is in the paper as a demonstration of the feature, not as evidence.
- Runtime on the authors' laptop (Apple M4 Pro, 24 GB, Ollama 0.40.9): 64 answers per sample took 15 minutes (espresso, 18:37 to 18:52 PDT) and 18 minutes (RAG, 18:52 to 19:10), about 14 to 17 s per answer (CE/samples/README.md "Canonical runs"). A one-question live run of 8 seeds on one draft is therefore about 2 minutes. **[OWNER: confirm this laptop is the booth machine; re-time on it with `date` if not.]**
- The first recording was wrong (truncated prompts, format failures scored as "not cited", no chance level), and its reading was withdrawn as a bench artifact (CE/samples/README.md "The first recording, and why it was superseded"). One sentence in the paper, no breakdown.

**The checklist score**

- Following the suggestions raises the score by 38 and 31 points: espresso 35 to 73, RAG 45 to 76 (foundation); 37 to 70 and 48 to 74 (evidence). Re-run 2026-10-24 with `node packages/bench/bin/ce.js analyze samples/<s>/<v>.md --json` in CE; matches CE/samples/README.md line 94. (CE/README.md still says "37 to 72"; stale, flagged to the owner.)
- **This rise is built in.** The after drafts were written by acting on the tool's own suggestions (CE/samples/README.md Protocol step 3), so the score had to rise. The paper presents it as "what following the advice looks like on the checklist", never as a finding.
- **Length confound.** The after drafts are longer: espresso 831 to 946 words (+14%), RAG 1,041 to 1,275 (+22%) (`wc -w` on CE/samples/*/{before,after}.md, 2026-10-24). There is no length-matched placebo for after against before.
- n = 2 rewrites, both by the tool's authors. The protocol (drafts and packs committed before any run; CE/samples/README.md Protocol steps 4 and 6) answers "tuned to the bench", not "n = 2" or "the rewriter built the tool".

**The sensitivity test (companion harness, 4 open models, pre-registered)**

- It is a separate Python harness on the Explorer cluster (`CE/experiments/explorer/sensitivity.py`), using the bench's prompt re-implemented in Python, with **citation share** as its metric (`score()`, lines 91 to 99), the target always placed among 8 sources (no retrieval), whole pages, 8 questions x 8 seeds x 4 conditions per model (256 answers). Byte-identity with `packages/bench/src/prompt.ts` was not checked for this test (planned for E1 only; CE/experiments/PREREG_E1.md "Generation").
- Pre-registration `3c86c02` (2026-10-23 20:18 PDT) precedes the results commit `4d77fa0` (20:43 PDT), per `git log` in CE.
- Registered outcomes (CE/experiments/RESULTS_sensitivity.md table; S-JSON `summary`):
  - H1, the off-topic control: share 0.000 to 0.003 against a bar of at most 0.05. **Holds** on all four models.
  - H2, the one-sentence answer edit minus before: +0.034 (p 0.055), +0.026 (p 0.008), +0.025 (p 0.008), +0.007 (p 0.58) for Qwen3.5-9B, Gemma-4-12B-it, Qwen3.8-27B, Gemma-4-31B-it, against a bar of at least +0.10 with p at most 0.05. **Fails** on all four.
  - The bar was ambitious: from a before share of about 0.16, +0.10 is a relative gain of about 60%. Say so.
- Exploratory (not pre-registered as a test; 4 models x 2 contrasts, uncorrected), after (the tool's suggestions applied) minus before (S-JSON `summary.after_minus_before_exploratory`; per-question signs recomputed from `per_question` on 2026-10-24):

  | Model | before | after | after minus before | relative | questions up | p (sign-flip, 8 q) |
  |---|---|---|---|---|---|---|
  | Qwen3.5-9B | 0.164 | 0.178 | +0.014 | +8% | 5 of 8 | 0.52 |
  | Gemma-4-12B-it | 0.178 | 0.201 | +0.023 | +13% | 8 of 8 | 0.008 |
  | Qwen3.8-27B | 0.154 | 0.180 | +0.026 | +17% | 8 of 8 | 0.008 |
  | Gemma-4-31B-it | 0.180 | 0.211 | +0.031 | +17% | 6 of 8 | 0.039 |

  - Small, positive on every model, and consistent across questions on two. No p reaches the p < 0.001 bar Nanda sets for exploratory work, and two of these p values are at the floor a sign-flip over 8 questions allows (0.0078). Suggestive, not established.
  - Heterogeneity (recomputed 2026-10-24 from `per_question`): Qwen3.5-9B after minus before is +0.034 on espresso and -0.007 on RAG; Gemma-4-31B's one-sentence answer edit went up on 4 questions and down on 4. The largest single-question gain is 0.088 for the answer edit (Qwen3.5-9B) and **0.141 for after** (Gemma-4-31B). Report both maxima.
  - Noise, derived post hoc on 2026-10-24 from `per_question` (to be regenerated by `scripts/derive_sensitivity.py` before any number enters the paper): the SD of per-question differences is about 0.02 to 0.06, so a paired test at n = 8 could detect differences of roughly 0.02 to 0.07. The +0.10 bar was within reach of the instrument; the edits were simply smaller. The bench is not "blind": it separates on-topic from off-topic sharply and resolves +0.025 on two models.
- Dilution (exploratory, post hoc): with every source on topic, models cite 6.2 to 7.0 of 8 sources per answer, and the target is cited at all in 86% to 97% of before answers (`target_cited_rate.before` 0.8594 to 0.9688). "Cited at all" is at its ceiling, and one page's share is spread thin. This is a reading, not a cap: a page's share is not bounded at 1/6.5. E1's 4-source design with a rank outcome is its test.
- **A labelled deviation.** PREREG_sensitivity.md line 37 says that if every model fails H2 the result is reported as "the bench cannot detect content differences with these models". The data do not fit that sentence (H1 shows sharp relevance detection; small edits move share consistently). The paper reports H2 as failed and says in one sentence that the planned fallback wording does not describe the data, and why. "E2" is not named.

**E1 (planned per-suggestion test)**

- Designed (CE/experiments/PREREG_E1.md r3): matched placebos for every LLM-edited arm, 4 sources, rotated target slots, a first-citation rank score (5 - r)/4 as primary outcome, Holm families, an equivalence margin of 0.03, a minimum detectable effect of about 0.018 to 0.021 in rank-score units, and a table mapping each verdict to a tool change.
- **No results.** The pipeline has fetched and drawn pages (CE/experiments/e1/out/fetch-run.log ends "draw done Fri Oct 23 23:16:07 PDT 2026"). PREREG_E1.md line 3 still reads "frozen at commit `<hash>`", so the paper cannot call E1 pre-registered yet **[OWNER]**.
- Its judges are models that failed H2; PREREG_E1.md "Limits" says so. If E1 is described at all, one clause says the judges were kept for answer validity and consistency, not for H2.
- Its MDE is in rank-score units and must never sit beside citation-share differences without the unit named.

### 1.2 The claims

What a reader should leave with: *an author-side GEO tool can show the evidence behind each of its checks and test its own advice; in our setting, following the advice raises the checklist score by 31 to 38 points but citation share by only 1 to 3 points, and the tool tells the author exactly that.*

The tool answers three questions for an author, with honest confidence on each (the PC's framing, W8): **can engines reach your site** (well supported: crawler access and indexing are graded strong), **is your draft easy to cite** (a checklist whose evidence is mixed, and shown), and **did following the advice change citation** (test it; in our setting, a little).

#### Claim 1 (existence)

**An author-in-control GEO workspace can run entirely on the author's machine, show graded evidence for every check, and include a citation test that separates retrieval from citation.**

- Type: existence proof (a working, tested, public system). Not a claim about user preference: there is no user study.
- Evidence: the live demo https://shehral.github.io/citation-equity/ and the code https://github.com/shehral/citation-equity (MIT); CE/docs/architecture.md "Testing and CI" (unit tests per check, metric tests against hand-computed values, the replay test `packages/bench/test/samples.test.ts` asserting the demo's numbers equal the committed recordings, a Playwright smoke test with no request leaving the origin on load); a scripted "system checks" paragraph (bundle size, engine latency per draft, test counts) written by a script in this repo to `data/system_checks.json`.
- Figures: Figure 1 (left, schematic) and Figure 2 (screenshot).

#### Claim 2 (rubric-relative, systematic over the 10 checks)

**Under a rule where any null or negative finding, even in a subgroup, makes a check mixed, none of the ten draft checks qualifies as strong or moderate; the tool shows each check's grade, studies and direction to the author.**

- Type: systematic over the tool's own checks, and explicitly relative to the rubric. A looser rule is shown beside it (null = a study's own no-effect conclusion for that practice, or a significant harm; non-significant subgroups and indirect nulls do not count). The looser grades are computed by script from the coded matrix; we do not predict them here.
- Readiness items reach strong on operator documentation, a different standard, said in the same sentence.
- Evidence: CE/docs/evidence.md (rubric lines 16 to 34; per-check sections); `data/evidence_matrix.csv`, coded from those sections with a `source_line` per cell.
- Rater: single rater so far. **[OWNER: ask Ishan to grade the ten checks blind from the same sources (about an afternoon) so the paper can report agreement; otherwise "single rater" goes in Limitations.]**
- Figure 3 (evidence matrix with direction and significance per cell, and both rules' grade chips).

#### Claim 3 (narrow and exploratory, with one pre-registered negative)

**Following the tool's suggestions raised its checklist score by 31 to 38 points, and on four open models of 9B to 31B parameters raised the draft's citation share by 1 to 3 points (8% to 17% relative): a consistent but exploratory gain. A one-sentence answer edit missed a pre-registered +0.10 bar on all four models.**

- Type: **narrow** (2 synthetic topics, 8 questions, a fixed 8-source context with no retrieval, open models, a companion harness, no live engine) and **hedged** (the after-minus-before contrast was exploratory and uncorrected; the dilution account is post hoc).
- The score half is built in and stated as such. The length confound is named, with E1's placebos as the planned answer.
- We do not claim the suggestions do nothing, and we do not claim the instrument cannot detect a 0.10 gain. We claim: the edits tried moved share by 1 to 3 points, so a single before/after run on one model cannot validate GEO advice of that size.
- Why it matters: popular uplift figures (the GEO paper's "up to 40%", from 19.3 to 27.2 word share in a fixed five-source context [Aggarwal et al. 2024]) are an order of magnitude above what these edits did here, and Martinez (2026, Table 5) rejects that figure "as a general claim". Bajemon and Rochet (R39; arXiv preprint, vendor-linked, not peer reviewed) report that re-measuring the 2023 levers on ten modern engine families moved citation on none. Our result points the same way on open models, with a small positive residue.
- Evidence: S-JSON; CE/experiments/PREREG_sensitivity.md; CE/experiments/RESULTS_sensitivity.md; the score re-run (1.1).
- Figures: Figure 1 (right, headline) and Figure 4 (per-question differences).

#### E1 (not a claim)

- In the working draft: a marked placeholder paragraph (design only) and a marked placeholder frame for its figure, as the stage brief requires.
- **For submission, the default is the fallback**: two sentences of future work pointing to the frozen plan, no placeholder frame in the PDF. E1 returns as one result sentence and one panel only if registered results with the required n exist by **8 Nov 2026 [OWNER: confirm the date]**.

---

## 2. Why a WWW demo reviewer should care, and what is new

### 2.1 Why care

- Answer engines sit between writers and readers, and they send fewer clicks. Pew (R76): users clicked a result on 8% of visits with an AI summary against 15% without, and clicked a link inside the summary on 1% (https://www.pewresearch.org/short-reads/2025/07/22/google-users-are-less-likely-to-click-on-links-when-an-ai-summary-appears-in-the-results/). A preregistered field experiment (N = 1,100) found that assignment to AI Mode search "reduced click-through rate by -18.8 percentage points" (Wang et al., R77, https://arxiv.org/abs/2608.18352, Section 3; verified in the full text 2026-10-24; preprint).
- Independent writers get the least help. In our review of 24 product pages (October 2026), the commercial tools sell brand-visibility tracking to companies, with listed tiers from free trials to $800 per month. Cite the product pages, never LS. **[Check before prose: which 3 or 4 product pages the sentence cites; verify each URL on the day.]**
- The advice in circulation rests on shaky evidence: the "up to 40%" comes from one fixed five-source setup (Aggarwal et al., KDD 2024, https://arxiv.org/abs/2311.09735), which Martinez rejects as a general claim (https://arxiv.org/abs/2607.14035, Table 5); in C-SEO Bench, adding statistics lowered citation rank in 19 of 24 settings (https://arxiv.org/abs/2506.11097, NeurIPS 2025 D&B); in SAGEO Arena, rewrites that helped in the fixed setup often made pages harder to find (https://arxiv.org/abs/2602.12187, KDD 2026); in a 252,000-trial study of 18 factors, formatting-only edits had little impact (What Gets Cited, https://arxiv.org/abs/2605.25517, SIGIR 2026), though lists and headings were not isolated.
- Tools that rewrite for the author raise a second problem: the more an AI writes, the less ownership writers feel (Draxler et al., TOCHI 2024, R93; Dhillon et al., CHI 2024, R100), and span-anchored AI comments raised writer agency over a chat interface (AnchoredAI, N = 22, preprint, R102). This motivates the design; the paper does not claim the tool raises agency.
- Fit for WWW: a deployed web system on generative search; creator control of AI access (crawler and indexing directives in the readiness report); creators' stake in AI search.

### 2.2 What is new, and what is not

**Not new, credited by name in the intro and related work:**

- **Evidence tiers on content checks.** aiseo-audit (MIT) keeps a factor registry with evidence tiers, paper citations and editable weights, and already tags lists, tables and answer capsules "diagnostic", citing the same C-SEO "19 of 24" and the What Gets Cited formatting null (CE/docs/research/2026-10-23-oss-sweep.json, line 14 and "gaps" item 5). Citation Equity adapts code from it (CE/NOTICE).
- **A readiness score kept apart from measured citations.** geo-score ("two scores, never one"; Wilson intervals on its API citation watch; R238).
- **No silent rewriting.** answerlint states it "never rewrites your content silently"; GEO Optimizer previews fixes (R239). Footnote-level credit if space is short.
- **Stagewise measurement.** SAGEO Arena measures visibility at each pipeline stage (retrieve, rerank, generate). Our "retrieved against cited" split is new only among the commercial and open tools we surveyed (CE/docs/research/2026-10-23-oss-sweep.json "gaps" item 3; our product-page review).
- **The bench's prompt and word-share metric** are the GEO paper's (Apache-2.0, adapted; CE/NOTICE). The counterfactual style follows C-SEO Bench, What Gets Cited and ConflictingQA.
- **The null itself.** R39 reports the same direction on stronger setups (preprint, vendor-linked).

**What is new (one honest sentence, each component's prior art named):** *Citation Equity puts graded evidence with an explicit null-counting rule, a self-test that separates retrieval from citation and reports a chance level, and a pre-registered sensitivity result into one offline, author-side tool that shows the author all three, and it never rewrites the draft.*

Supporting specifics, each phrased "among the tools we surveyed", never "first":

1. An explicit decision rule for grades, surfaced per check in the interface (an increment on aiseo-audit's tiers).
2. The test is built into the same tool (the in-tool bench), with format failures kept as outcomes, as Martinez asks ("Outputs without search, without citations, or with errors are outcomes, not data to be discarded", Section 11.2; the "denominator, exclusions, and threshold for a substantively meaningful difference must be prespecified", Section 11.1).
3. The unit is one writer and one draft, not a brand; there is no bulk action. Commercial optimizers generate or rewrite content (product pages); research optimizers rewrite automatically (GEO; AutoGEO, R10, ICLR 2026).
4. No peer-reviewed user test of a GEO tool exists in the landscape we read; we do not fill that gap either and name it as future work (IRB).

Positioning sentence (draft): *Citation Equity is not a better optimizer. It is a writing tool that tells an author what the evidence does and does not support, and tests its own advice in the open.*

---

## 3. Red team: objections and pre-emptions

| # | Objection | Pre-emption |
|---|---|---|
| R1 | "Your own results say the tool barely helps. Why demo it?" | The demo is the loop "apply advice, watch the score rise, test whether citation moves", and the honest answer it gives. Readiness is the well-supported, actionable part (strong grades). The score is labelled "a writing checklist, not a forecast" in the UI and in the abstract. Do not oversell either way: Claim 3 says small and consistent, not "does nothing". |
| R2 | "Local open models in a fixed 8-source context are not ChatGPT, Perplexity or Google." | Agree in the paper. Every bench report carries the caveat. `ce live` is optional, needs the author's key, and is recorded-response tested; nothing is reported from it. Cite Martinez Table 5 ("Engines differ and change over time"). R250 (vendor) is not cited in the 4-page version. |
| R3 | "Two synthetic topics, 8 questions, synthetic competitors." | Give n everywhere. The packs are synthetic so no third-party text is redistributed (CE/samples/README.md). The baseline share is above chance (0.154 to 0.180 against 0.125), which depends on how the pack was written; say so. |
| R4 | "The after drafts were written by the authors; the score rise is circular; they are longer." | The score rise is stated as built in. Lengths are reported (+14%, +22%) and length is named as the main confound, with E1's placebos as the planned answer. Drafts and packs were committed before any run (Protocol steps 4 and 6). |
| R5 | "Pre-registration in your own git repo is not a real pre-registration." | Call it "committed to the public repository before the run", with hashes and times. Report the failed bar as the outcome; add the labelled deviation sentence for the fallback wording. **[OWNER: an OSF registration before E1's freeze would answer this better.]** |
| R6 | "The rubric is built so nothing passes; the grades are your judgement." | Phrase the result rubric-relative; show a looser rule beside it (script-computed); show direction and significance per cell in Figure 3 so "mixed" is visibly not "no effect"; second rater if the owner agrees, else "single rater" in Limitations. One regrade on record (direct-answer lead, moderate to mixed). |
| R7 | "aiseo-audit and geo-score already do this." | Credit both by name, including aiseo-audit's diagnostic tags from the same studies. The novelty sentence is the combination, in one offline author-side tool, with a built-in test. |
| R8 | "Word share is the wrong outcome." | The two metrics are named apart (word share in the in-tool bench; citation share in the harness). Cited-at-all is at its ceiling (86% to 97%), which is why E1 uses first-citation rank with 4 sources. |
| R9 | "E1's judges failed H2." | One clause if E1 is mentioned: kept for answer validity and consistency; PREREG_E1.md "Limits" says so. "E2" never appears. |
| R10 | "E1 uses GEO-bench, whose licence the design excluded." | Only relevant if E1 appears. Research use only; pages fetched live or from Wayback; only aggregates and hashes committed; the shipped tool uses no GEO-bench data. **[OWNER: confirm with the PI.]** |
| R11 | "Isn't this SEO?" | One sentence: Google says AI features rest on core Search ranking and require indexing and snippet eligibility (Google Search Central, https://developers.google.com/search/docs/appearance/ai-features); the tool treats those as readiness items and keeps them out of the score. |
| R12 | "Could it help manipulators?" | It never generates content; advice says add only real, sourced material; the off-page cards carry platform rules and FTC guidance. The bench could test manipulative edits as easily as honest ones; the shipped tool offers no such arms. Ethics section. |
| R13 | "No user study." | Not claimed. HCI evidence motivates the design only; an IRB-gated study is the next step. One line: no users or analytics are reported, by design. |
| R14 | "A bug could explain a null." | It happened once and was caught (first recording). The replay test pins the demo's numbers. The off-topic control shows the harness detects relevance. The 10-prompt byte-identity check between the Python harness and `prompt.ts` is cheap; run it before submission and report it, or say it was not run **[OWNER: run `--export-prompts` comparison]**. |
| R15 | "The screenshot shows an unshipped redesign." | Figure 2 is a marked placeholder in the working draft. The submitted PDF carries a real capture: the dashboard if merged and deployed by about 9 Nov, otherwise the current workspace (CE/docs/screenshot.png, or a Playwright capture of the deploy). The text describes features, not layout, so either works. |
| R16 | "Two of four p values sit at the sign-flip floor; 8 comparisons uncorrected." | The after contrast is labelled exploratory and uncorrected in text and caption; intervals (95% t over 8 questions, as the tool itself reports) accompany every difference. |
| R17 | "Is the in-browser test the evidence?" | No. Say plainly: the in-browser run is a demonstration; Claim 3 rests on the companion harness on the cluster. |

**Inconsistencies in the tool repo (not ours to edit; flagged to the owner):**

1. CE/README.md "37 to 72"; the samples README and a fresh run give 35 to 73 and 45 to 76 (foundation). Fix the README before reviewers click through.
2. PREREG_E1.md line 3 "frozen at commit `<hash>`".
3. The design spec says "Vercel"; the demo is on GitHub Pages. The paper says GitHub Pages.
4. CE/docs/evidence.md lists AutoGEO as "(preprint)"; the corpus verified it as an ICLR 2026 poster (R10). The paper cites ICLR 2026.

---

## 4. Figure plan (summary; exact list in `notes/OUTLINE.md`)

Every figure is regenerated by a script from data (`scripts/fig_<name>.py` reading through `scripts/figdata.py`; numbers never typed). Each caption opens with a bold takeaway. The palette is chosen for prettiness, not colorblind safety (owner, 2026-10-21), and `figstyle.py` gets sigconf sizes (column about 3.33 in, `figure*` about 7.0 in).

Concept colours (one meaning each, everywhere):

- before draft: soft slate;
- after draft (suggestions applied): indigo, the dashboard spec's brand colour;
- one-sentence answer edit: teal;
- off-topic control: grey, dashed;
- chance level: thin dotted ink;
- pre-registered bar: coral band;
- grades: strong deep green, moderate light green, mixed amber, untested light grey;
- checklist score: indigo outline (score marks are hollow, citation marks filled, so score and citation never read as the same quantity).

1. **Figure 1** (`figure*`): TikZ schematic (Check, Suggest, Test, with readiness and off-page as side panels marked "never changes the score") plus a headline from the registered harness data on honest axes: score before to after per sample (0 to 100) beside citation share before to after per model (pooled over 8 questions, per-sample faint), chance and off-topic lines, relative changes as direct labels. No llama3.2:3b data (different metric).
2. **Figure 2** (column): annotated screenshot of the draft view; placeholder frame in the working draft only.
3. **Figure 3** (column): evidence matrix, 10 checks x 9 studies, direction and significance per cell, grade chips under the strict and the looser rule, with a thin readiness strip on its own standard.
4. **Figure 4** (column): per-question differences for the four models, after minus before (exploratory) and one-sentence answer edit minus before (registered), with the +0.10 bar and zero line. Panel (b), E1, is a marked placeholder frame in the working draft only.

Cut order if the build overflows: (1) Figure 4(b) frame (already out of the submission by default); (2) fold Figure 4 into Figure 1 as a per-question strip; (3) shrink Figure 3 to the strict-rule column and the readiness strip. Figure 3 is not cut first (red team, item 5).

---

## 5. Outline

Moved to `notes/OUTLINE.md` (sections, word budgets, figures, citations per section).

---

## Next steps (Nanda steps 4 to 6)

1. The owner reads this file and `notes/OUTLINE.md` and settles the [OWNER] items.
2. `scripts/figdata.py`, `scripts/collect_scores.py`, `scripts/derive_sensitivity.py`, `scripts/system_checks.py`; then the Figure 1 headline, Figure 3 and Figure 4(a) scripts (data exists now). Figure 2 and Figure 4(b) stay marked frames.
3. `refs.bib`, verified entry by entry.
4. The prose draft in acmart; build with tectonic.

---

## Changes after critique

Both critiques were checked against the files before acting; every number they cite was recomputed (S-JSON `per_question`, `wc -w`, `ce analyze`, `sensitivity.py`, evidence.md, the OSS sweep) and matched.

**Accepted**

1. *Claim 2 understated the data (red team 1).* The old claim ("cite the revised drafts at most a few points more, an effect the bar cannot separate"; "not a lever") attached the failed H2 bar to the wrong condition and called a +0.023 to +0.031 effect at p 0.008 to 0.039 inseparable. New Claim 3: small, consistent, exploratory gain of +0.014 to +0.031 (8% to 17%), with H2 reported for the one-sentence answer edit only. "Not a lever" and "barely" are gone from claims and captions.
2. *"The bench cannot detect 0.10" and "first published measurement floor" (red team 2, PC W10).* Dropped. There is no positive control, and the per-question noise suggests a 0.10 difference was detectable. Replaced by "the edits tried moved share by 1 to 3 points; a single before/after run cannot validate advice of that size". A post hoc MDE from the per-question SD is planned, labelled post hoc.
3. *Figure 1 mixed two metrics and a misleading scale (red team 3, PC W2).* The headline now uses only the registered harness data, on two honest axes, with relative changes as labels; llama3.2:3b is out of Figure 1. The two metrics get two names (word share, citation share); the old R8 row that called the harness metric "PAWC" is fixed.
4. *"Doubles" (PC W3, red team 3).* Replaced by "31 to 38 points (35 to 73, 45 to 76)".
5. *Built-in score rise and length confound (red team 4).* Stated as built in; lengths reported; length named as the main confound; baseline above chance named.
6. *Rubric-relative result (red team 5).* Claim phrased relative to the rule; looser-rule grades computed by script beside the strict ones; direction and significance per cell; readiness's different standard named. Figure 3 is kept and is no longer first to cut.
7. *Novelty narrower (red team 6).* R39 credited as prior evidence for the null (labelled preprint, vendor-linked); aiseo-audit's diagnostic tags credited; SAGEO's stagewise measurement credited; "retrieved against cited" limited to the tools we surveyed; one combined novelty sentence.
8. *"The tool tests its own advice" overstated (red team 7).* The paper says "a companion harness, using the bench's prompt, on larger open models"; the in-browser run is a demonstration; byte-identity check flagged to the owner; `ce live` worded as optional, key-required, recorded-response tested.
9. *E1 (PC W5, red team 8).* For submission, the fallback is the default (two sentences of future work, no frame), with a decision date of 8 Nov instead of 12 Nov. "E2" removed; one clause on the judges if E1 appears; MDE units named.
10. *Pre-registration deviation (red team 9).* H2 bar called ambitious (about +60% relative); one labelled sentence on why the pre-registered fallback wording is not used.
11. *Selective reporting (red team 10).* Both maxima reported (0.088 answer edit, 0.141 after); heterogeneity mentioned; per-question dots in Figure 4.
12. *Demo framing (PC W1, W8; red team 11).* The demo is the loop "apply, watch the score, test citation"; the measurement is a feature of the tool; the "three honest answers" framing (reach, citability, did it change) puts readiness up front. The findings section shrinks to about 360 words.
13. *Booth script (PC W7).* Three self-contained stations; a 90-second core loop on recorded results plus an optional one-question live run, whose runtime (about 2 minutes) comes from the measured sample runs; "bring your own text" offline; readiness on a hotspot as an owner item.
14. *System evaluation (PC W9).* A scripted "system checks" paragraph: bundle size, engine latency per draft, test counts, no-egress smoke test, from `data/system_checks.json`.
15. *Video (PC W6).* A 2:30 screen capture of station 1 linked on page 1; Kokoro narration if voiced. Owner item.
16. *Space (PC W4, red team 14).* Body about 2,100 words; about 20 references with a cut list; cut order for figures defined.
17. *Citation hygiene (red team 12, PC W11).* "252,000 trials" reworded as the whole study; price phrasing fixed; LS never cited (product pages instead); Pew wording as verified; R243 and R250 dropped from the 4-page version, with the llms.txt example; AutoGEO cited as ICLR 2026.
18. *Glossary (red team 13).* Term table at the top; `answer_first` renamed "one-sentence answer edit"; "oracle" and "E2" dropped.
19. *Dual use (red team 15).* Ethics says the bench could test manipulative edits as easily as honest ones and that the shipped tool offers none.

**Rejected or modified (with reasons)**

1. *Drop the R77 "18.8 pp" number unless verified (red team 12.1).* Kept: verified in the full text on 2026-10-24 ("Assignment to AI Mode Search significantly reduced click-through rate by -18.8 percentage points (pp)", Section 3), and "preregistered" is in Section 1. Cited as a preprint.
2. *Remove the E1 placeholder paragraph and figure frame now (red team 8.1, PC W5).* Modified. This stage's brief asks for a marked placeholder paragraph and a marked placeholder frame in the working draft, so both stay, clearly marked. The critiques' point is taken for the submitted PDF, where the fallback is the default.
3. *Put the current screenshot in Figure 2 now (PC W5, red team 11.1).* Modified for the same reason: the working draft carries a marked placeholder described by what it will show, as the brief asks. The rule that the submitted PDF has a real capture (dashboard by 9 Nov, otherwise the current workspace) is adopted.
4. *Add a pre-registered positive control to the sensitivity harness (red team 2.1).* Not done in this stage: it needs a change to the tool repo and cluster time, which are the owner's to authorise. The wording consequences are adopted in full, so the paper does not depend on it. **[OWNER: worth about 3 to 4 minutes of generation per model per condition (`generate_seconds` 165 to 245 s for 256 answers); pre-register in a new commit first.]**
5. *Bootstrap intervals over questions (red team 1.3).* Modified: 95% t intervals over the 8 questions, matching how the tool itself reports intervals (CE/samples/README.md switched to Student's t for few questions). A percentile bootstrap over 8 points under-covers.
6. *Second rater (red team 5.3).* Owner's call (it involves a co-author's time); the paper reports agreement if done, "single rater" otherwise.
7. *Engine latency on "a larger set of real public pages" (PC W9).* Rejected: it brings third-party text into the paper's pipeline and an ethics question for a minor number. Latency is measured on the two samples and the synthetic pack pages. "Anchor robustness" is reported only if an existing test exposes it; no new metric is invented.
8. *Cut the references to about 15 (PC W4).* Modified to about 20: Figure 3's columns name all nine studies, so Zhang-He-Yao and GEO-SFE must be cited, and R39 now carries a sentence. Tool repos beyond aiseo-audit and geo-score go to footnote URLs or are dropped first.
9. *"Section 3 shrinks to about 350 words" (PC W1).* Accepted in spirit at about 360, since the claim now carries more care (built-in score, length, heterogeneity, deviation sentence).
10. *Title "A Writing Tool for AI Search That Tests Its Own Advice" (PC).* Kept as a candidate, with a softer verb ("Checks Its Own Advice") offered because the test that carries the claim runs in a companion harness; owner picks.
