# PC critique of NARRATIVE.md (WWW 2027 demo track)

Reviewer stance: a senior demo-track PC member, reading notes/NARRATIVE.md (draft 1, 2026-10-24) as if it were the paper. Written 2026-10-24. Requirements rechecked the same day at https://www2027.thewebconf.org/demos/ (4 pages including references, sigconf review, single-blind, implemented and tested system, venue setup section required, ethics section required, code/video/live system "strongly encouraged", criteria originality, significance, quality, clarity).

## Verdict

**As planned: weak accept, leaning borderline.** The honesty is real and rare, the system is live (the demo URL returned HTTP 200 on 2026-10-24) and open, and the related-work positioning is unusually careful. What holds it back is that the plan reads as a short measurement paper with a tool attached, not a demo paper. It is over-stuffed for 4 pages, its headline rests on the weakest data in the repo, the screenshot and E1 are both placeholders, there is no demo video, and the booth script cannot run in the time a visitor gives you.

**With the changes below: a clear accept** is realistic. The demo has one memorable, interactive idea that no other GEO tool shows: *the visitor applies the tool's own advice, watches the score jump, and then watches the citation test refuse to move*. Build the paper and the booth around that moment.

## What I would write as the reviewer (strengths)

1. **Originality of stance.** A GEO tool that grades its own checks, counts nulls against them, and ships a bench that can falsify its own advice is a new position among the tools surveyed. The "not new, and we say so" list (aiseo-audit, geo-score, answerlint, GEO Optimizer, Bajemon and Rochet) pre-empts the obvious "this exists" review and builds trust.
2. **Significance for the Web community.** Creator control and creator compensation under AI search are on-topic for Responsible Web and Web Economics, and the field badly needs tools that do not sell uplift.
3. **Quality signals.** Live static demo, MIT code, replay test that pins demo numbers to recordings, a pre-registration committed before the run (`3c86c02` before `4d77fa0`), and the failed bar reported without moving it.
4. **Red-team table.** R1 to R15 is the right list. Most reviewer objections are already answered.

## What would make me score it down (weaknesses, ranked)

### W1. It is a measurement paper wearing a demo badge

- Section 3 (600 words) plus Figure 4 is larger than any single description of what the user does. The demo call judges the *system* and the *experience at the venue*.
- PREREG_sensitivity.md says that if H2 fails "the paper leads with the measurement result". That rule was written for a research paper; VENUE.md already says the opposite for this venue ("the measurement work is supporting evidence, not the headline method"). Follow VENUE.md.
- **Change:** reframe the measurement as a *feature of the tool* ("Test it"), shown through the interface. The claim becomes: "the tool can check its own advice, and in our sample setting the check says the score is a checklist, not a lever." Section 3 shrinks to about 350 words.

### W2. Figure 1's headline panel uses the weakest evidence

- The arrows come from llama3.2:3b, n = 4 questions per sample, synthetic packs, smallest p 0.125. A reviewer will say the headline figure shows noise.
- The stronger, registered data (4 models of 9B to 31B, 8 questions x 8 seeds, `per_question` split by sample) is pushed to an inset.
- **Change:** draw the headline from the sensitivity JSONs. x = checklist score (before vs after, per sample, foundation preset, from `ce analyze`), y = target share; one thin arrow per model per sample (4 models x 2 samples, plus llama3.2:3b greyed), chance at 0.125, off-topic floor as a grey band near 0. `per_question` keys are `espresso-bitterness/q*` and `rag-explained/q*`, so the per-sample means are computable by script. The visual point (long horizontal, short vertical arrows) survives and now rests on registered data.

### W3. "Roughly doubles" is not true for both samples

- 35 to 73 is 2.1x; 45 to 76 is 1.7x. A careful reviewer will check.
- **Change:** say "raises the checklist score by 31 to 38 points (35 to 73, 45 to 76)", or "nearly doubles". Same fix in the Figure 1 caption ("doubles" appears there too).

### W4. Too much for 4 pages including references

- The plan has a `figure*` plus three single-column figures plus about 22 references plus 2,650 to 2,750 body words. In sigconf at 4 pages including references this will not fit; a realistic body with that figure load is about 2,000 to 2,200 words, and 22 references take closer to 0.75 page than 0.6.
- VENUE.md already set the rule "Figure 1 and at most one results figure"; the narrative breaks it.
- **Change:**
  - Figures: Figure 1 (schematic + headline, `figure*`), Figure 2 (real screenshot with callouts), Figure 3 (one results figure: the sensitivity dot plot, Figure 4a as planned). Evidence matrix becomes a compact 10-row table *only if* it fits, otherwise one sentence plus the `/evidence` URL. Figure 4b (E1 frame) goes (see W5).
  - References: about 14 to 16. Keep Aggarwal, C-SEO Bench, What Gets Cited, SAGEO Arena, Martinez, AutoGEO or AgentGEO (one), ConflictingQA, Schulte, Pew, the AI-Mode experiment, Draxler, Dhillon, AnchoredAI, aiseo-audit, geo-score, Google Search Central. Push GEO-SFE, E-GEO, Zhang-He-Yao, Bajemon and Rochet to the arXiv version unless a sentence depends on them.
  - Word budget: Intro 400, System 850, Test-it findings 350, Related 180, Venue 220, Ethics and limits 200. About 2,200.

### W5. Placeholders that cannot survive to submission

- **E1.** A demo paper with a "results pending" paragraph and an empty forest plot reads as unfinished, and it spends about a quarter column on a design the reviewer cannot evaluate. The pre-registration also still says "frozen at commit `<hash>`", and the GEO-bench licence question (R10) is unresolved, so even a design paragraph invites an ethics question.
  - **Change:** make the default the fallback, not the exception. Decide by **8 Nov** (not 12 Nov: figures and the screenshot also need the last week). If E1 has frozen, registered results by then, it gets one sentence of result and one row in the results figure. Otherwise it is one sentence of future work with a pointer to PREREG_E1.md. No placeholder figure in the submitted PDF either way.
- **Screenshot.** Demo reviewers weigh the screenshot heavily. A placeholder frame in the submitted PDF is a reject signal.
  - **Change:** draft the paper now against the current workspace (`CE/docs/screenshot.png` exists, and the Playwright capture script can shoot the deployed build). Swap to the dashboard only if it is merged and deployed by about 9 Nov. Describe features in the text, never layout, so either screenshot works (R15 already says this; make it the plan, not the fallback).

### W6. No demo video

- The call "strongly encourages" a video. The plan has the live URL and the repo but no video. Many demo reviewers will not install Ollama; a 2 to 3 minute video is how they see "Test it" run.
- **Change:** record a 2:30 screen capture of the booth path (W7), put it on the repo README and the paper's first page footnote. Kokoro narration if voiced (macOS voices are personal-use only). Owner's call on hosting.

### W7. The booth script does not fit a booth

- Six steps in five minutes is too many; booth visits are 2 to 3 minutes and people arrive mid-demo.
- **"Run Test it live on the local model"**: a full before/after bench is 2 drafts x 4 questions x 8 seeds = 64 generations on llama3.2:3b. The paper must state how long that takes on the demo laptop; my guess is minutes, not seconds. Measure it (`date` before and after, on the actual laptop) before writing the sentence.
- **"Paste a visitor's own published page into Your site"**: offline, the visitor cannot fetch their page's HTML; and the bench on the visitor's own topic needs a competitor pack (`ce pack from-urls` needs network). Only check and suggest work on a visitor's own text offline.
- **Change:** a three-station script, each self-contained:
  1. **The 90-second loop (core):** load the espresso example, apply two suggestions one at a time, watch the score climb, then open the pre-recorded Test it result and the chance line. Optional: start a one-question live run (1 question x 8 seeds) and let it finish while you talk. State its measured runtime.
  2. **Bring your own text (optional):** paste a paragraph or post; see checks, anchored suggestions, and the evidence grade of each; nothing leaves the laptop.
  3. **Is your site reachable? (optional, needs network):** the readiness report on their live URL via the hosted demo on a phone hotspot, with the honest note that this is the part graded strong.
  - Name the hardware (laptop model, RAM), the fallback when the model is slow (recorded results, which the replay test guarantees match), and the poster.

### W8. The "useful now" answer is buried

- R1 is answered by "the instrument and its honesty". A reviewer will still ask: what does a writer get today?
- The repo's strongest-graded material is site readiness: indexing directives and AI crawler access are graded strong, rendering without JavaScript moderate (CE/docs/evidence.md). That is the part of the tool with actionable, well-supported value, and it sits in a 90 to 130 word subsection.
- **Change:** give readiness one crisp paragraph in the intro and a station at the booth. Frame the tool as three honest answers: *can engines reach you* (well supported), *is your draft easy to cite* (mixed evidence, shown), *did it change anything* (test it yourself). This also lets the score be a checklist without the tool looking useless.

### W9. Evaluation of the *system* is missing

- A demo paper is expected to show the system works as a system, not only what it found. The plan has tests and CI in one sentence, no performance numbers, no robustness check of the engine, no usage.
- **Change (cheap, no human subjects):** a short "System checks" paragraph with numbers generated by a script in this repo and saved to `data/`:
  - engine analysis time per draft in the browser and in Node, on the two samples and on a larger set of real public pages that the repo already uses for research (only aggregates committed);
  - static bundle size and confirmation that no request leaves the origin on load (the Playwright smoke test);
  - anchor robustness: the fraction of suggestions that still Apply after unrelated edits elsewhere in the draft, if the test suite exposes it.
  - Only report numbers that a script produces and commits; cite the path in a comment.
- Do **not** claim usability or agency gains. Keep R13 as is.

### W10. Wording that invites attack

- "to our knowledge, the first published measurement floor for this kind of bench": drop it. "Among the N tools we surveyed" claims are defensible; "first" over the whole literature is not, and What Gets Cited and C-SEO Bench both report small or null effects.
- "Claim 2 cannot detect a 0.10 share gain here": correct and good. Keep the companion sentence "we do not claim that the suggestions do nothing" in the paper verbatim; the exploratory consistent direction (8/8 questions on two models) earns one clause, not a sentence.
- The score label "a writing checklist, not a forecast" is excellent. Use it in the abstract.
- The superseded first recording: keep the one-sentence lesson; cut the three-cause breakdown.

### W11. Small accuracy items to fix before prose

- The tool README's "37 to 72" versus the samples README and a fresh `ce analyze` run giving 35 to 73: the narrative already flags it; also open an issue in the tool repo so the live README matches the paper before reviewers click through.
- The design spec says "Vercel"; the paper must say GitHub Pages.
- The nightly GitHub Actions template and `ce live` are tested only against recorded responses (CE/docs/roadmap.md "Open items"). The paper must not imply live-engine results; say "recorded-response tested".
- R250 (API versus consumer gap) is a vendor study and R243 is trade press: label both in the text, or drop them from a 4-page paper.

## Title

Both drafts are fine. A sharper one carries the booth moment:

- "Citation Equity: A Writing Tool for AI Search That Tests Its Own Advice"

**[OWNER]** as before.

## Concrete change list (in order of payoff)

1. Reframe: the demo is the loop "apply advice, watch score, test citation"; measurement is a feature of the tool (W1, W8).
2. Rebuild the Figure 1 headline from the registered sensitivity data split by sample; llama3.2:3b greyed (W2).
3. Replace "doubles" with the point gains (W3).
4. Cut to three figures and about 15 references; body about 2,200 words (W4).
5. E1 decision date 8 Nov; no placeholder figure in the submission; default is one future-work sentence (W5).
6. Use the current screenshot now; swap only if the dashboard ships by 9 Nov (W5).
7. Record a 2:30 demo video and link it on page 1 (W6).
8. Rewrite the venue section as three stations, with measured bench runtime on the demo laptop and an offline fallback (W7).
9. Add a scripted "System checks" paragraph: analysis latency, bundle size, no-egress check (W9).
10. Remove "first"; label vendor and trade-press sources; fix the README score range upstream (W10, W11).

## Owner items raised by this critique

- E1 cut-off date (proposed 8 Nov) and whether E1 appears at all.
- Video: who records, where it is hosted.
- Demo laptop: which machine, so the bench runtime can be measured on it.
- Whether a phone hotspot is acceptable at the booth for the readiness station.
- Who presents in Dublin, and registration (unchanged from NARRATIVE.md).
