# Outline: Citation Equity, WWW 2027 demo paper (Nanda step 3)

Status: DRAFT 1, 2026-10-24, built from `notes/NARRATIVE.md` draft 2 (claims, terms and the critique decisions live there). **[OWNER]** marks his calls. Abbreviations as in NARRATIVE.md: CE = `../citation-equity`, S-JSON = the four `CE/experiments/results/sensitivity/sensitivity_*.json` files.

Format: `\documentclass[sigconf, screen, review]{acmart}`, at most 4 pages including references, single-blind. acmart keeps its own fonts and layout; from the house kit we load only the shared interface of `smpreprint.sty` (the branch its `tmlr` option selects: palette, `\owner`, `\figtakeaway`, `\panel`, keys, `takeaway` box), so nothing changes ACM's layout. Figures use `figstyle.py` with sigconf sizes (column 3.33 in, `figure*` 7.0 in) and a new, pretty (not colorblind-constrained) concept map. Build: `/opt/homebrew/bin/tectonic --keep-logs main.tex`. No em dashes in the prose.

Rules carried into every section: each number carries a `% src:` comment with the file it comes from; each citation is a verified source (listed below); the word "first" is never used as a priority claim; the in-tool run is a demonstration and the claims rest on the harness; E1 has no numbers.

## Space budget

| Item | Pages |
|---|---|
| Title block, abstract, CCS concepts, keywords, video/demo footnote | 0.40 |
| Figure 1 (`figure*`) | 0.33 |
| Figures 2, 3, 4 (one column each, about 0.15 page each) | 0.45 |
| References (about 19 entries in ACM style) | 0.60 |
| Body text, about 2,100 words | 2.20 |
| **Total** | **3.98** |

Body budget: Intro 400, System 760, Findings 360, Related work 160, Demonstration 200, Ethics and limitations 200, Acknowledgments 20 = **2,100 words** (abstract 150 on top).

Overflow order: (1) drop the Figure 4(b) frame (out of the submission by default anyway); (2) cut Section 2.4 to 60 words; (3) footnote URLs for answerlint and GEO Optimizer go; (4) fold Figure 4 into Figure 1 as a per-question strip; (5) Figure 3 keeps only the strict-rule chips and the readiness strip; (6) drop Schulte et al.

## Title (pick one) [OWNER]

- "Citation Equity: A Writing Tool for AI Search That Tests Its Own Advice" (PC's suggestion)
- "Citation Equity: A Writing Tool for AI Search That Checks Its Own Advice" (softer verb, since the claim rests on a companion harness)
- "Citation Equity: Evidence-Graded Writing Help for AI Search, Measured in the Open"

Byline (set by the owner 2026-10-26): Mohammad Ali Shehral, Ishan Gupta, Akshay Prajapati, Pegah Zargarian, Akram Bayat (last); Northeastern University, Khoury College of Computer Sciences, San Jose, CA, USA for all but Pegah Zargarian (Northeastern University, USA; alumna); emails shehral.m@, prajapati.aksh@ and zargarian.p@northeastern.edu.

Page-1 footnote: live demo https://shehral.github.io/citation-equity/ ; code https://github.com/shehral/citation-equity (MIT); video **[OWNER: 2:30 capture of station 1; hosting]**.

---

## Abstract (150 words)

1. Context: AI answer engines now choose which pages a reader sees cited, and they send fewer clicks.
2. Gap: writers get GEO advice whose evidence is weak, from tools that track brands or rewrite their text.
3. Contribution: Citation Equity, an open-source workspace that runs in the browser, checks a draft against ten checks each shown with its graded evidence, suggests span-anchored fixes the author applies one at a time, and includes a citation test that separates being retrieved from being cited.
4. Rubric outcome: under a rule where any null finding counts, none of the ten checks is strongly or moderately supported; the score is "a writing checklist, not a forecast".
5. Numbers: following the suggestions raised the score from 35 to 73 and 45 to 76, but citation share on four open models (9B to 31B) by only 1 to 3 points (8% to 17%, exploratory); a one-sentence answer edit missed a pre-registered +0.10 bar on all four.
6. Standard of evidence: two synthetic topics and open models in a fixed context, not live engines; links.

(No E1 sentence in the submitted abstract unless E1 results exist by 8 Nov.)

## Key-findings box: none

A demo paper at 4 pages has no room for both a key-findings box and Figure 1's headline; the headline carries it. (A deliberate departure from STYLE.md section 5 for this venue.)

---

## 1. Introduction (400 words)

- **P1 Context (80).** Answer engines sit between writers and readers. Clicks fall when an AI summary appears (8% against 15% of visits; 1% on links inside the summary) [chapekis2025pew]; a preregistered field experiment found AI-Mode-only search cut click-through by 18.8 points [wang2026aisearch]. Define *answer engine* and *GEO* here.
- **P2 Gap (120).** The advice in circulation rests on one fixed five-source setup ("up to 40%") [aggarwal2024geo], which a survey rejects as a general claim [martinez2026survey]; larger studies find no gain or a loss for the same edits [puerto2025cseo; kim2026sageo; vishwakarma2026cited]. The tools sell brand tracking or rewrite the text (our review of 24 product pages, October 2026; footnote 2 to 3 product URLs), and the more an AI writes, the less ownership writers feel [draxler2024ghostwriter; dhillon2024scaffolding].
- **P3 What we built (100).** Citation Equity, from the PI's three-module design, answers three questions for one writer and one draft: *can engines reach your site* (readiness; crawler access and indexing are the best-supported items), *is your draft easy to cite* (ten checks, each with its graded evidence), and *did following the advice change citation* (a built-in test). It suggests and never rewrites; nothing leaves the author's machine. Credit in one clause: evidence tiers (aiseo-audit [aiseoaudit]) and readiness-apart-from-citation (geo-score [geoscore]) exist; what is new is putting graded evidence with an explicit null rule, a retrieval-versus-citation self-test and a pre-registered sensitivity result into one offline author-side tool.
- **P4 What the test found (60).** Following the advice raised the checklist score 31 to 38 points, which is built in, but citation share by 1 to 3 points on four open models; a pre-registered bar of +0.10 for a one-sentence answer edit was missed on all four. Consequence for tool builders: a single before/after run cannot validate advice of this size. R39 points the same way on live engine families [bajemon2026scoring] (labelled preprint).
- **P5 Contributions (40), bullets with pointers.**
  - the system, live and open (Section 2; Figures 1, 2);
  - graded evidence shown per check, under a strict and a looser rule (Section 2.2; Figure 3);
  - a citation test inside the tool and a pre-registered sensitivity result on four open models (Sections 2.5, 3; Figures 1, 4).

Takeaway box (`\begin{takeaway}`), optional if space allows: the one-sentence positioning ("not a better optimizer; a writing tool that says what the evidence supports and tests its own advice in the open").

## 2. Citation Equity (760 words)

- **2.1 Architecture and system checks (150).**
  - pnpm monorepo: `engine` (pure check functions, runs in the browser and Node), `bench` (CLI `ce`), `workspace` (Next.js static export on GitHub Pages, no server). Contracts carry `schemaVersion`. Src: CE/docs/architecture.md.
  - System checks (numbers from `data/system_checks.json`, written by `scripts/system_checks.py`, which reads the tool repo and never writes to it): static bundle size; engine analysis time per draft in Node on the two samples and their pack pages (median of 20 runs); number of tests; the Playwright smoke test's no-egress assertion. Report only what the script writes.
  - One sentence: no users or analytics are reported, by design.
- **2.2 Check: ten checks with graded evidence (230).**
  - Six checks from the PI's design, four from the literature (list in one line). Src: CE/docs/evidence.md line 3.
  - The rubric in two sentences: strong, moderate, mixed, untested; a null or negative result anywhere, even in a subgroup, makes a check mixed. Src: evidence.md lines 16 to 34.
  - Outcome, rubric-relative: 0 strong or moderate, 8 mixed, 2 untested, over 9 studies opened on 2026-10-23 (line 34). Under a looser rule (only a study's own no-effect conclusion or a significant harm counts) the grades are **[from `data/evidence_grades_loose.json`, script output; not predicted]**. Rater: **[OWNER: second rater's agreement, or "single rater"]**.
  - Worked example showing why "mixed" is not "no effect": comparisons (positive in all six models of What Gets Cited, significant in four) against statistics (lower citation rank in 19 of 24 C-SEO settings). Src: evidence.md lines 93 to 107, 185 to 199.
  - Two presets (foundation, evidence) with weights visible and editable; the UI calls the score "a writing checklist, not a forecast" **[check the shipped UI wording; the label is from the dashboard spec line 24]**. Figure 3.
- **2.3 Suggest, never rewrite (170).**
  - Suggestions are anchored to exact text ranges; *edit* suggestions offer Apply, *advisory* ones explain; Apply runs only if the anchored text is unchanged; Undo; no bulk action. Src: CE/docs/architecture.md (Suggestions, `lib/apply.ts`); dashboard spec section 3.
  - Optional wording help from a local model on localhost, side by side, applied only on a click. Src: CE/README.md item 5.
  - Ranking of fixes ("Start here": applicable fixes first, then expected score gain). Src: dashboard spec. Text describes features, not layout. Figure 2.
- **2.4 Beyond the draft (90).** Site readiness: 7 items graded on operator documentation, a different standard (2 strong, 1 moderate, 2 mixed, 2 untested; evidence.md lines 201 to 323). Who gets cited: answers the author pastes, or the optional `ce live` on Gemini with the author's own key, recorded-response tested only (CE/README.md line 93; CE/docs/roadmap.md). Real signals: logs, Bing AI Performance and Search Console exports. None changes the score. One sentence on SEO overlap [google-ai-features].
- **2.5 Test it: the citation bench (120).**
  - Draft plus a pack of 7 competitor pages; BM25 top 8; the GEO prompt [aggarwal2024geo]; 8 seeded runs per question with shuffled source order; llama3.2:3b by default.
  - Reports retrieved, valid answers, cited among valid, word share against the chance level, and a paired sign-flip test; format failures are outcomes, as the survey asks [martinez2026survey, Section 11.2]. Define *word share*, *valid answer*, *chance level* here.
  - The caveat line on every report. Runtime: about 14 to 17 s per answer on the authors' laptop (CE/samples/README.md "Canonical runs"). Export and replay for larger models.

## 3. What the test found (360 words)

- **3.1 In the tool (90).** On the two sample drafts, all 128 answers were valid; word share 0.087 to 0.137 and 0.086 to 0.095 against chance 0.125; paired p 0.25 and 0.75, where 0.125 is the smallest possible at 4 questions; one gain is retrieval (0 of 8 to 8 of 8 runs on one question). A demonstration of the feature, not evidence. One sentence: an earlier recording gave a confident wrong reading from truncated prompts and was withdrawn. Src: CE/samples/README.md lines 81 to 94 and "The first recording".
- **3.2 Pre-registered sensitivity test (220).**
  - Design: a companion Python harness on a GPU cluster using the bench's prompt; target always among 8 sources (no retrieval); 4 conditions (before, after, one-sentence answer edit, off-topic control); 8 questions x 8 seeds; Qwen3.5-9B, Gemma-4-12B-it, Qwen3.8-27B, Gemma-4-31B-it. Metric: *citation share*, defined. Plan committed (`3c86c02`, 20:18 PDT) before the results (`4d77fa0`, 20:43 PDT). Src: CE/experiments/PREREG_sensitivity.md; `sensitivity.py` lines 91 to 99.
  - Registered: the off-topic control held (share at most 0.003 against at most 0.05); the one-sentence answer edit gained +0.007 to +0.034 against a bar of +0.10, which fails on all four; the bar was ambitious (about +60% relative). Labelled deviation: the pre-registered fallback sentence ("cannot detect content differences") does not fit the data, because relevance is detected sharply. Src: RESULTS_sensitivity.md; S-JSON `summary`.
  - Exploratory, uncorrected: after minus before +0.014 to +0.031 (8% to 17%), positive on every model and on all 8 questions for two; 95% t intervals from `scripts/derive_sensitivity.py`; heterogeneity in one clause (Qwen3.5-9B's RAG questions go down); maxima 0.088 and 0.141.
  - Reading, post hoc: models cite 6.2 to 7.0 of 8 sources and the target is cited at all in 86% to 97% of before answers, so share is spread thin. Post hoc noise: per-question SD gives a detectable difference of about **[`derive_sensitivity.py` MDE range]**, so the bar was within the instrument's reach; the edits were small.
  - Confounds in one sentence: the score rise is built in; the after drafts are 14% and 22% longer; the competitor pages are synthetic and the before share is already above chance. Figure 4.
- **3.3 Which single suggestions matter (50).**
  - Working draft: `\owner{PLACEHOLDER: E1. Design only: per-suggestion edits on real pages against placebos of the same footprint, 4 sources, first-citation rank as outcome, a frozen table from each verdict to a tool change (CE/experiments/PREREG_E1.md). Results: PENDING; no numbers until the E1 report exists.}` plus the Figure 4(b) frame.
  - Submission default: two sentences of future work, pointing to the plan once frozen; no frame.

## 4. Related work (160 words)

- GEO methods and benchmarks, one sentence each on what we reuse or differ from: GEO's prompt and word share [aggarwal2024geo]; counterfactual edits [puerto2025cseo; vishwakarma2026cited; wan2024conflictingqa]; stagewise visibility [kim2026sageo]; automatic rewriters [wu2026autogeo]; the survey's reporting standards [martinez2026survey]; day-to-day variance of cited sources [schulte2026measure].
- Scores as stand-ins for engines: falsification gates and the null on ten engine families [bajemon2026scoring] (preprint, vendor-linked); we make no claim that our score predicts citation.
- Open audit tools: aiseo-audit's evidence tiers and diagnostic tags from the same studies [aiseoaudit]; geo-score's two scores [geoscore]; answerlint and GEO Optimizer (footnote URLs, cut first).
- Writing with AI: ownership [draxler2024ghostwriter; dhillon2024scaffolding] and span-anchored comments [lou2025anchoredai] motivate suggest-never-rewrite; no user study of a GEO tool exists in what we read.

## 5. Demonstration at the venue (200 words; required)

- Hardware: one laptop runs the static site and Ollama with llama3.2:3b offline, so no venue network is needed **[OWNER: confirm the M4 Pro 24 GB laptop; re-time if different]**; a second screen or tablet shows the hosted demo; a poster with Figures 1 and 4.
- **Station 1, the 90-second loop (core).** Load the espresso example; apply two suggestions one at a time and watch the score climb; open one fix's evidence (a mixed check); open the recorded test result with the chance line. Optional: start a one-question live run (8 seeds, about 2 minutes on this laptop, from the measured per-answer time) and let it finish while talking. Fallback when the model is slow: the recorded results, which the replay test guarantees match.
- **Station 2, bring your own text (optional, offline).** Paste a paragraph or post; see checks, anchored suggestions and each grade; nothing leaves the laptop.
- **Station 3, is your site reachable (optional, needs network).** The readiness report on the visitor's live URL, via the hosted demo on a phone hotspot; the part graded strong **[OWNER: hotspot acceptable?]**.
- Who presents **[OWNER]**.

## 6. Ethics, limitations and future work (200 words; ethics required)

- **Ethics and data (110).** No human participants and no user data: the site has no server, drafts stay in the browser, and no analytics run. Sample drafts and packs are synthetic and invented. C-SEO Bench data is fetched at run time and never redistributed. Fetching respects robots.txt. The tool never posts, never writes reviews and never scrapes consumer AI interfaces. Dual use: it generates no content and advises adding only real, sourced material; the off-page cards carry platform rules and FTC guidance; the bench could test manipulative edits as easily as honest ones, and the shipped tool offers none. If E1 appears: GEO-bench URLs used for research only, with only aggregates and hashes committed **[OWNER: confirm with the PI]**. A future user study goes through IRB.
- **Limitations (60).** Open models in a fixed context, not live engines; two synthetic topics and 8 questions; English only; the harness prompt not yet byte-checked against the tool's **[OWNER: run the 10-prompt check]**; grades depend on our rubric and **[one/two]** rater(s); no positive control; no user study.
- **Future work (30).** The per-suggestion test (E1) with placebos; a local-versus-live agreement report; chunk-level retrieval; the IRB study.

**Acknowledgments (20).** The SPARK program **[OWNER: funding line, if any]**.

**AI-use statement.** `\owner{PLACEHOLDER: AI-use statement, written by the owner.}` Not drafted by us.

---

## Figures (exact list)

All scripts follow STYLE.md section 6: `--root` (input repo), `--out figures/`, read only through `scripts/figdata.py`, numbers formatted by `figstyle.fmt()`, vector PDF, input SHA-256 in the Subject field, byte-identical on rerun, `.venv/bin/python -I -B`. A figure script never writes a number file.

| File | Placement | Takeaway (the caption's bold first sentence) | Data source | Producer |
|---|---|---|---|---|
| `figures/fig1_overview.tex` | `figure*`, top of page 1 or 2 | **Following the tool's suggestions raises its checklist score by 31 to 38 points, but raises citation share on four open models by only 1 to 3 points.** | TikZ (no data); embeds `fig1_headline.pdf` | hand-written TikZ with `sm*` styles |
| `figures/fig1_headline.pdf` | right 40% of Figure 1 | (part of Figure 1) | `data/scores.json` (from `scripts/collect_scores.py`: `ce analyze --json` on CE/samples/*/{before,after}.md, engine version stamped); S-JSON `per_question` and `summary.mean_target_share`, `chance_share` | `scripts/fig_headline.py` |
| `figures/fig2_workspace.pdf` | one column | **The author applies one fix at a time, and every fix shows how strong its evidence is.** | now: a marked placeholder frame; at submission: `data/screens/draft_view.png` from `scripts/capture_screens.mjs` (Playwright, fixed viewport, the espresso example loaded, against the deployed build) and callouts from `data/fig2_callouts.json` | `scripts/fig_workspace.py` |
| `figures/fig3_evidence.pdf` | one column | **Every draft check has at least one study with a null or negative result, but "mixed" ranges from positive-in-every-model to harmful, and a looser rule changes some grades.** (Second clause rewritten to the script's actual output before prose.) | `data/evidence_matrix.csv` (coded from CE/docs/evidence.md, one `source_line` per cell); `data/grades.json` dumped from `CE/packages/engine/src/evidence.ts` by `scripts/dump_grades.mjs`; the script fails if a coded grade disagrees with the registry; `data/evidence_grades_loose.json` from `scripts/derive_loose_grades.py` | `scripts/fig_evidence.py` |
| `figures/fig4_sensitivity.pdf` | one column, panel (a) | **(a) Applying the suggestions moved citation share by 1 to 3 points on every model, and the one-sentence answer edit stayed far below the pre-registered +0.10 bar.** | S-JSON `per_question` (before, after, answer_first, offtopic), `summary` (mean_sources_cited, H2 threshold); intervals from `data/sensitivity_derived.json` (`scripts/derive_sensitivity.py`) | `scripts/fig_sensitivity.py` |
| `figures/fig4b_e1_frame.pdf` | panel (b) of Figure 4, working draft only | **(b) [PLACEHOLDER: E1 takeaway, written only after results exist.]** | none now; empty axes, the ±delta band and the MDE tick read from `data/e1_design.json` (each value with its PREREG_E1.md line; the script checks the quoted string is in the file); the text "E1 results pending; design: CE/experiments/PREREG_E1.md" | `scripts/fig_e1_frame.py` |

What each figure shows:

- **Figure 1, left (schematic).** The author's draft in the centre; three numbered stages: (1) *Check*, ten checks each with its grade chip, the score labelled "a writing checklist, not a forecast"; (2) *Suggest, never rewrite*, a span-anchored fix with one Apply button and a struck-through "Apply all"; (3) *Test*, draft plus 7 competitors, BM25 top 8, an open model, then "retrieved?", "cited?", "share against chance". Side panels: site readiness (with its strong items highlighted) and who gets cited, marked "never changes the score". A lock glyph: "stays on your machine".
- **Figure 1, right (headline).** Two small aligned panels with honest axes. Left: checklist score (foundation), before to after, one hollow slope per sample (35 to 73, 45 to 76). Right: citation share, before to after, one filled slope per model pooled over 8 questions (faint per-sample slopes behind), chance 0.125 dotted, the off-topic control as a grey band near 0. Direct labels give the relative change (+109%, +69% on the left; +8% to +17% on the right). No llama3.2:3b data (it uses word share). Caption: harness, n = 8 questions x 8 seeds, synthetic packs, exploratory contrast, score rise built in.
- **Figure 2.** The draft view with the espresso example and numbered callouts: (1) the score with "A writing checklist, not a forecast"; (2) a Start-here fix with its before/after preview ("Nothing changes until you click Apply."); (3) a fix group with its grade label (mixed); (4) the Test-it section with its two numbers and the chance caveat; (5) the "stays in your browser" chip. The working draft shows a frame: "[PLACEHOLDER: screenshot of the draft view of the shipped dashboard; see CE/docs/superpowers/specs/assets/2026-10-23-dashboard/mockup-dashboard.html, state 3 Draft (working)]". The submitted PDF shows a real capture (dashboard if deployed by about 9 Nov, otherwise the current workspace).
- **Figure 3.** Rows: the 10 draft checks; columns: the 9 studies. Cells: filled dot = gain, significant; small dot = gain, not significant; ring = null; cross = harm; half dot = observational or indirect; blank = not tested. Two chip columns: strict rule (the shipped grade) and looser rule. Below, a thin strip for the 7 readiness items with a note that operator documentation counts there.
- **Figure 4(a).** One row per model; dots for the 8 per-question differences, after minus before (indigo, exploratory) and one-sentence answer edit minus before (teal, registered); the model mean with its 95% t interval; the +0.10 bar as a coral band; zero as a hairline; mean sources cited (6.2 to 7.0 of 8) as a row label. Off-topic shares (at most 0.003) in the caption.
- **Figure 4(b).** Planned forest plot of the per-arm rank-score difference against placebo; frame only.

Figure-to-claim map: Claim 1, Figures 1 (left) and 2; Claim 2, Figure 3; Claim 3, Figures 1 (right) and 4(a); E1, Figure 4(b) in the working draft only.

## Data and helper scripts (written before the figures)

- `scripts/figdata.py`: read-only loaders for S-JSON, CE/samples/*/results/*.json, and `data/*.json`.
- `scripts/collect_scores.py` writes `data/scores.json`.
- `scripts/derive_sensitivity.py` writes `data/sensitivity_derived.json`: per-model means, 95% t intervals over 8 questions, per-sample means, questions up, maxima, per-question SD and a post hoc MDE (labelled post hoc in every use).
- `scripts/derive_loose_grades.py` writes `data/evidence_grades_loose.json` from the coded matrix under the looser rule.
- `scripts/system_checks.py` writes `data/system_checks.json`.
- `scripts/paper_numbers.py` writes `numbers.tex` (macros for every number in the prose), so prose and figures show the same digits.

## Citations needed, by section

All are in the landscape corpus (verdict confirmed or corrected) or CE/docs/research/evidence-notes.md; each is re-checked on its arXiv, ACL, DOI or GitHub page when it enters `refs.bib`.

| Key | Source | Verified in | Sections |
|---|---|---|---|
| aggarwal2024geo | Aggarwal et al., GEO: Generative Engine Optimization, KDD 2024, arXiv 2311.09735 | evidence.md; corpus | 1, 2.5, 4 |
| puerto2025cseo | Puerto et al., C-SEO Bench, NeurIPS 2025 D&B, arXiv 2506.11097 | evidence.md; corpus | 1, 2.2 (fig 3), 4 |
| vishwakarma2026cited | Vishwakarma et al., What Gets Cited, SIGIR 2026, arXiv 2605.25517, DOI 10.1145/3805712.3808445 | evidence-notes.md line 44 | 1, 2.2 (fig 3), 4 |
| kim2026sageo | Kim et al., SAGEO Arena, KDD 2026, arXiv 2602.12187 | evidence.md; corpus | 1, fig 3, 4 |
| martinez2026survey | Martinez, critical survey of GEO, arXiv 2607.14035 (Table 5; Sections 11.1, 11.2) | PDF in geo-project; red team 12.6 | 1, 2.5, 4 |
| wan2024conflictingqa | Wan et al., ConflictingQA, ACL 2024, aclanthology 2024.acl-long.403 | evidence.md | fig 3, 4 |
| wu2026autogeo | Wu et al., AutoGEO, ICLR 2026, arXiv 2510.11438 | corpus R10 | fig 3, 4 |
| zhang2026absorption | Zhang, He, Yao, From Citation Selection to Citation Absorption, arXiv 2604.25707 (preprint) | evidence-notes.md line 61 | fig 3 |
| yu2026geosfe | Yu et al., GEO-SFE, arXiv 2603.29979 (preprint) | evidence-notes.md line 81 | fig 3 |
| bajemon2026scoring | Bajemon and Rochet, Scoring Without the Engine, arXiv 2609.07559 (preprint, vendor-linked) | corpus R39 (corrected author name) | 1, 4 |
| schulte2026measure | Schulte, Bleeker, Kaufmann, Don't Measure Once, arXiv 2604.07585 | corpus R46 | 4 (cut last) |
| chapekis2025pew | Chapekis and Lieb, Pew Research Center short read, 22 Jul 2025 | corpus R76 | 1 |
| wang2026aisearch | Wang et al., AI in Search Reduces Publisher Referrals Without Improving User Experience, arXiv 2608.18352 (preprint; 18.8 pp in Section 3) | corpus R77; full text 2026-10-24 | 1 |
| draxler2024ghostwriter | Draxler et al., The AI Ghostwriter Effect, ACM TOCHI 2024, DOI 10.1145/3637875 | corpus R93 | 1, 4 |
| dhillon2024scaffolding | Dhillon et al., Shaping Human-AI Collaboration, CHI 2024, DOI 10.1145/3613904.3642134 | corpus R100 | 1, 4 |
| lou2025anchoredai | Lou et al., AnchoredAI, arXiv 2509.16128 (preprint) | corpus R102 | 4 |
| aiseoaudit | agencyenterprise/aiseo-audit, GitHub (MIT) | CE/docs/research/2026-10-23-oss-sweep.json | 1, 4 |
| geoscore | jianruntech/geo-score, GitHub | corpus R238 | 1, 4 |
| google-ai-features | Google Search Central, "AI features and your website", https://developers.google.com/search/docs/appearance/ai-features | CE/README.md; evidence.md | 2.4 |

Footnote URLs (not bib entries, cut first): answerlint (https://github.com/rakeshcheekatimala/answerlint), GEO Optimizer (R239), and 2 to 3 commercial product pages for the "24 products" sentence **[verify each URL on the day; never cite LS]**.

Not cited in the 4-page version: R243 (trade press, llms.txt), R250 (vendor), E-GEO (R9), AgentGEO (R16).

## Open owner items (collected)

Title; byline and order; AI-use statement; E1 cut-off (8 Nov) and the PREREG_E1 freeze hash; GEO-bench use with the PI (only if E1 appears); second rater; positive control and the byte-identity check (tool repo and cluster time); booth laptop, hotspot, who presents, registration; video recording and hosting; funding line; CE/README.md "37 to 72" fix.
