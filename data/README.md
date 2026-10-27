# data/: small derived tables behind the figures and the prose

Every file here is either written by a script from the tool repo (`../citation-equity`, "CE", read only, never
written) or hand-coded with a line reference into CE. No raw third-party page text and no model answer text is
copied here. Rebuild everything with `.venv/bin/python -I -B scripts/fig_all.py --derive` (CE must be present;
`CE_ROOT` or `--ce-root` points elsewhere). Each JSON carries a `_provenance` block with its producer and the
SHA-256 of its inputs, so a rebuild against a changed CE is visible in the diff.

| File | Producer | Source in CE | Used by |
|---|---|---|---|
| `grades.json` | `scripts/dump_grades.mjs` | `packages/engine/dist/index.js` (built from `src/evidence.ts`, `src/readiness.ts`; the script refuses a stale build) | `derive_loose_grades.py`, `fig_evidence.py` |
| `evidence_matrix.csv` | hand-coded (single rater), checked by `derive_loose_grades.py` | `docs/evidence.md`, one `source_line` per cell | `derive_loose_grades.py`, `fig_evidence.py` |
| `evidence_grades_loose.json` | `scripts/derive_loose_grades.py` | the two files above plus `docs/evidence.md` | `fig_evidence.py`, prose (Section 2.2) |
| `sensitivity_derived.json` | `scripts/derive_sensitivity.py` | `experiments/results/sensitivity/sensitivity_*.json` (`summary`, `per_question` only) and `experiments/explorer/sensitivity.py` (registered thresholds, with line numbers) | `fig_sensitivity.py`, prose (Section 3.2) |
| `e1_design.json` | `scripts/derive_e1_design.py` | `experiments/PREREG_E1.md` (design values with line and quote; **no results**) | `fig_e1_frame.py` |
| `fig2_callouts.json` | hand-written | dashboard spec and mockup under `docs/superpowers/specs/` (file:line per UI string) | `fig_workspace.py` |
| `fig5_callouts.json` (and `screens/reader_words.png`) | `scripts/capture_reader_words.mjs` (live site, Playwright; then the tool repo's engine through tsx) | the deployed draft view after the two reader's-words edits; UI strings, measured anchors and the engine's per-check scores before and after | `fig_reader_words.py` |
| `scores.json` | `scripts/collect_scores.py` | `ce analyze --json` on `samples/*/{before,after}.md` | `fig_headline.py` |

## Coding conventions for `evidence_matrix.csv`

One row per (check, study) pair that the engine registry lists as a source for that check (the script fails if the
coded studies differ from the registry's). Columns:

- `result`: `gain`; `gain_part_null` (a gain in some settings and no significant effect in others, e.g. significant
  in 4 of 6 models); `gain_part_harm` (a gain in one part and a harm in another); `null`; `harm`; `negative`
  (an observational difference in the harmful direction); `survey_support` and `survey_caution` (the Martinez
  survey's rating, not a test); `background` (mechanism, hypothesis, or a different practice).
- `design`: `controlled`, `observational`, `elicited` (rules elicited from engines, AutoGEO), `survey`, `background`.
- `directness`: `direct` (the practice the check looks for), `near` (a nearby practice, CE/docs/evidence.md line 32:
  a whole-page summary for a per-section answer, a formatting-only null for a specific format, relevance edits for
  the key-word rule), `none`.
- `sig`: `significant`, `partly`, `not_reported` (no test reported, e.g. GEO's word-share gains), `na`.
- `own_conclusion`: `yes` when the null or negative is the study's own stated finding for that practice.
- `live`: the study used real retrieval or live engines (only matters for the strong grade).

Judgement calls a second rater should look at first (all affect only the looser rule):

- Zhang et al.'s Q&A-format result for question headings is coded `direct` with `own_conclusion = yes` (the study
  names it a negative case). Coded `near`, the looser rule would find no counted null and no controlled gain for
  question headings, and the script would stop rather than invent a grade.
- What Gets Cited's formatting-only null is coded `near` for lists and question headings (the tested factors were
  section organisation and grouping; CE/docs/research/evidence-notes.md line 50).
- GEO-SFE's bundled structural rewrite is coded `controlled`, `near` for lists (lists not isolated; a preprint with
  automated judges). It is the only controlled gain behind the looser rule's "moderate" for lists.
- SAGEO Arena's case studies are coded `controlled`, `near`.
- The four reader-words cells (added 2026-10-24 for CE 4831ff9; CE/docs/evidence.md lines 255 to 258 at CE c908431) are all `near`: none
  tests the check's rule (key words in the title, first heading or first paragraph; CE/docs/research/evidence-notes.md
  "Reader's words up top"). GEO's Keyword Stuffing (17.7 vs 19.3 at baseline, no test reported, "little to no
  improvement" in the authors' words) is coded `null` with `own_conclusion = yes`, not `harm`, because Figure 3's cross
  means a significant harm. Coded `direct`, it would make the looser grade mixed instead of moderate.

The strict rule reproduces every shipped grade (the script checks it). The looser rule's grades are whatever the
script computes from this coding; they were not predicted.
