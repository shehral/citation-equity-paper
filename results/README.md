# results/: the evidence behind the paper's numbers

The withheld files listed in `manifests/` (pages, versions, prompts, answers) are now available for research through the gated Hugging Face dataset [Shehral/citation-equity-experiments-pages](https://huggingface.co/datasets/Shehral/citation-equity-experiments-pages); every result here is also in the public [Shehral/citation-equity-experiments](https://huggingface.co/datasets/Shehral/citation-equity-experiments).

This folder holds every result the paper reports, in the form the experiments produced it, plus what you need to check or rerun them: the plans as written before each run, the cluster jobs and their compute, the software and model versions, and the sha256 of every input we cannot share.

Everything except this README, `verify_numbers.py`, `VERIFY.txt` and `CLAIMS.md` is written by `scripts/build_results.py` from the tool repo ([shehral/citation-equity](https://github.com/shehral/citation-equity), "CE" below) and from the Explorer cluster, both read only. Rebuild it with

```sh
.venv/bin/python -I -B scripts/build_results.py --fetch   # pulls logs, sacct, hashes and versions from Explorer first
.venv/bin/python -I -B scripts/build_results.py           # rebuilds from the cached pulls in .cache/cluster/
```

`--fetch` needs ssh access to Explorer and a gitignored `.cache/cluster/settings.json` with the cluster user, paths and Slurm account (the format is in the script's header). `build_info.json` records the CE commit the copies were taken at (`edb6354`; the paper text is synced to CE `4831ff9`, and no experiment file changed between the two).

## Layout

| Folder | What it holds |
|---|---|
| `plans/` | The sensitivity pre-registration, the E1 pre-registration and its revision log, the E2 and E3 plans, and E1's freeze manifest. Each starts with a line naming the CE commit that first contained it and the commit it last changed in. |
| `sensitivity/` | The bench sensitivity test (4 models x 256 answers) and the vLLM smoke test that came before it. |
| `e1/` | E1, one suggestion at a time on real pages: 80 GEO-bench queries (main) and 60 C-SEO Bench queries (replication). |
| `e2/` | E2: `a/` asks whether the question-heading edit works through heading markup or through the reader's words (arms 9W and 9P); `b/` repeats E1's arm 12 and ALL with a second editor model (Qwen3.8-27B). |
| `e3/` | E3, seven checks E1 could not judge: `new/` (180 new queries), `retry/` (one more editing attempt on E1's failed pairs), `pooled/` (the analysis over 260 queries). |
| `manifests/` | Path, line count, size and sha256 of every withheld file, on the owner's machine and on the cluster. |
| `runs/` | Every cluster job of these experiments, its GPU, run time and GPU-hours, and the summary lines of its log. |
| `env/` | Python, vLLM, torch and transformers versions on the cluster, Node and pnpm locally, and the exact revision of every model. |

Per experiment, the files are:

| File | What it is |
|---|---|
| `RESULTS_*.md` | The report the analysis script wrote (copied from CE `experiments/`). |
| `analysis*.json` | The analysis output: every contrast, interval, p value, Holm family and label. Validator messages inside it are reduced to their template (see below); every number is identical to CE `experiments/results/`. |
| `score_summary.json` | Answer counts and completion per set, judge and arm. |
| `cells.jsonl` | One row per (query, version, judge): answers, valid answers, mean citation score, cited rate, word share. |
| `scores.jsonl` | One row per answer: key, seed, valid, rank of the target page, score, cited, word share. Numbers and ids only. |
| `retrieval.jsonl` | (E1) The lexical retriever's rank of each version in its pool. |
| `null_simulation.json` | (E1) The null simulation frozen before E1 ran (identical to CE `experiments/e1/freeze/null_simulation.json`). |
| `validity_counts.{json,md}` | Per set and arm: edited versions, valid, invalid, not applicable, attempts used, and the validator message categories; plus the frozen applicability pre-check per arm. |
| `sensitivity_*.json`, `smoke_*.json` | Summaries, per-question results and per-answer rows; each raw answer is replaced by its sha256 and length. |

## Where each number in the paper comes from

Section and figure numbers are those of `main_www.pdf`. Every number in the LaTeX also carries a `% src:` comment.

`CLAIMS.md` lists every number in the rendered prose and figure captions with the `% src:` comment that covers it. `verify_numbers.py` recomputes the E1, E2 and E3 contrasts the paper reports from the `cells.jsonl` files alone, checks them against the analysis JSONs (to 1e-9) and `../data/e1_results.json`, and checks every printed number for them in `../sections/*.tex`; it exits non-zero on any mismatch. Run it from the repo root with `.venv/bin/python -I results/verify_numbers.py --claims results/CLAIMS.md`; its last output is `VERIFY.txt`.

| Paper | Numbers | Results file |
|---|---|---|
| Abstract, Introduction | citation share +8% to +17% (+0.014 to +0.031) after the suggested edits; the answer edit missing the +0.10 bar on all four models | `sensitivity/sensitivity_*.json` (`summary.after_minus_before_exploratory`, `summary.answer_first_minus_before`), `sensitivity/RESULTS_sensitivity.md` |
| Abstract, Introduction | E1, E2 and E3 outcomes (the reader's-words result, 260 queries pooled) | `e1/analysis.json`, `e2/analysis_e2.json`, `e3/pooled/analysis_e3.json` |
| Abstract, Introduction, Figure 1 | checklist score 40 to 69 and 42 to 68 | not a cluster result: `../data/scores.json` (`ce analyze` on the two sample drafts) |
| Section 2 (Citation Equity) | check counts, evidence grades, analyze() timing | `../data/system_checks.json`, `../data/evidence_grades_loose.json`, CE `docs/evidence.md` |
| Section 2.3 (the citation bench) | laptop runs on llama3.2:3b | CE `samples/README.md`; the model's Ollama digest is in `env/` |
| Section 3, "On larger models" | 4 models x 256 valid answers, off-topic share, answer edit +0.007 to +0.034, plan before results | `sensitivity/`, `plans/PREREG_sensitivity.md` (commit `3c86c02`, results `4d77fa0`), `../data/sensitivity_derived.json` |
| Section 3, E1 | arm 9 (question headings) +0.027 [+0.010, +0.043], Holm 0.006, n 54; replication +0.036, n 52; other arms "insufficient n" | `e1/RESULTS_E1.md`, `e1/analysis.json`; n per arm in `e1/validity_counts.md` |
| Section 3, E2 | 9 vs 9W and 9 vs 9P per set; E2b with Qwen3.8-27B as editor and Qwen3.5-9B as a second judge | `e2/RESULTS_E2.md`, `e2/analysis_e2.json`, `e2/a/`, `e2/b/` |
| Section 3, E3 | pooled contrasts over 260 queries (180 new), which checks reach 30 valid pairs | `e3/pooled/RESULTS_E3.md`, `e3/pooled/analysis_e3.json`, `e3/new/validity_counts.md`, `e3/retry/validity_counts.md` |
| Figure 3 | grades per check and source | not a cluster result: `../data/grades.json`, `../data/evidence_matrix.csv`, `../data/evidence_grades_loose.json` |
| Figure 4 | E1 main and replication, E2, E3 pooled contrasts | `../data/e1_results.json`, derived by `scripts/derive_e1_results.py` from the three analysis files above (numbers identical) |
| Section 6 (Ethics and use of data) | only aggregates and hashes are shared | `plans/PREREG_E1.md` ("Data"), `manifests/` |
| Section 7 (Limitations and future work) | 320 queries = 260 GEO-bench (E3 pooled) + 60 C-SEO Bench (E1 replication); Gemma-4-31B-it edits; the smoke test before any run | `e3/pooled/`, `e1/`, `sensitivity/smoke_google__gemma-4-12B-it.json` |
| Compute (any mention) | GPU-hours | `runs/gpu_hours.json`: 16.87 GPU-hours in all (E1 7.60, E2 3.81, E3 4.16, sensitivity 0.86, smoke 0.44) |

## How each experiment was run

All runs used the tool's own prompts, retrieval, seeds and metrics: the bench exports prompts, the cluster only generates answers (vLLM, one GPU per job), and scoring and analysis run locally. The pipeline READMEs in CE list every command in order.

| Experiment | Plan (CE commit) | Pipeline | Results (CE commit) | Commands |
|---|---|---|---|---|
| Sensitivity | `PREREG_sensitivity.md` (`3c86c02`) | `experiments/explorer/sensitivity.py`, `sensitivity.sbatch` | `4d77fa0` (report text edited in `8bd5575`, `f125bef`) | CE `experiments/README.md` |
| E1 | `PREREG_E1.md`, frozen as r3 with amendments 1 to 10 (`7859b07`; code `a2322d7`) | `experiments/e1/` | `e258a1a` | CE `experiments/e1/README.md` |
| E2 | `PLAN_E2.md` (`cf2f9a1`, amendment 1 in `d90fc84`) | `experiments/e2/` (merged in `8f0de5f`) | `2e9bb7d` (aggregates cleaned in `c8e5fc6`) | CE `experiments/e2/README.md` |
| E3 | `PLAN_E3.md` (`571e8fc`, amendment 1 in `248a2ec`) | `experiments/e3/` (merged in `e0705db`) | `82aa8b3` | CE `experiments/e3/README.md` |

Each plan's commit can be checked against the job start times in `runs/` (the cluster clock is US Eastern; in Eastern time the plan commits are: sensitivity `3c86c02` 2026-10-23 23:18:42, E1 freeze `7859b07` 2026-10-24 04:33:28, E2 `cf2f9a1` 17:26:11, E3 `571e8fc` 19:19:27). Every editing and answer job of E1, E2 and E3 starts after its plan's commit (and after the amendments). The E1 jobs before the freeze are page normalization (no edits, no answers) and the timing smoke on a held-out query, whose outcomes were discarded. Three of the four sensitivity jobs started at 23:18:39, three seconds before the plan's commit, and the fourth (Gemma-4-31B-it) at 23:34:02, after it: the plan was committed as the jobs were submitted, and the results came in a later commit (`4d77fa0`).

## What is withheld, and why

Not in this repo, on purpose:

- **Page text.** GEO-bench's source pages and C-SEO Bench's pages belong to third parties, and the GEO-bench card's license text is inconsistent. The E1 pre-registration promises that nothing derived from the pages is shared beyond aggregate results and hashes (`plans/PREREG_E1.md`, "Data"). So `pages.jsonl`, `candidates.jsonl`, the raw fetches and the fetch logs stay local.
- **Edited versions** (`versions.jsonl`): every version is a full page.
- **Prompts** (`prompts.jsonl` and the cluster batch files): each prompt carries the full text of all sources.
- **Editor logs** (`editor_log.jsonl`): the editor model's requests and replies quote the pages.
- **Raw model answers** (`answers/*.jsonl`): answers quote and paraphrase the pages. For the sensitivity and smoke tests (synthetic sample pages) the answers are replaced by their sha256; the full rows are public in CE `experiments/results/`.
- **Job logs in full** and their stderr: they hold cluster paths and vLLM chatter. `runs/logs/` keeps each job's start and end lines, GPU line and JSON summary, with paths replaced by `$CE_ROOT_PARENT`, `$SCRATCH` and `$USER`.

Validator messages are kept only as templates. A message such as "Do not add facts that are not in the allowed sources: name '…'" can quote page text, so each one is rebuilt from a list of known templates with the quoted part, URL or word list replaced by `…`; nothing matched no template. Validity counts are counts only.

`manifests/` lists every withheld file with its line count and sha256, so a rerun can be checked byte for byte, and so can a copy of the data a reviewer receives under the datasets' terms.

## How to regenerate the withheld files

From a CE checkout at the commits above, follow the pipeline READMEs:

1. **E1** (CE `experiments/e1/README.md`, "Running it" and "On Explorer"): fetch the GEO-bench test split live (`fetch_geobench.ts`) and the C-SEO Bench pages (`cseo_replication.ts`), normalize (`normalize.py`, on Explorer with `normalize.sbatch` for the real tokenizers), fetch Wayback copies for failed pages, then `draw.py` and `applicability.ts`; edit on Explorer with `edit.sbatch`; build prompts (`build_prompts.py`), generate with `generate.sbatch` per batch, and score and analyze locally (`score.py`, `analyze.py`, `report.py`). The live fetch depends on the web on the day, so compare `pages.jsonl` against `manifests/` first: a different hash means different pages.
2. **E2** (CE `experiments/e2/README.md`, "On Explorer, in order"): `make_versions.py` for 9W and 9P, prompts and four generation jobs for E2a; `edit.sbatch` with `MODEL=Qwen/Qwen3.8-27B --arms 12` for E2b, then `reuse_answers.py`, prompts and generation; `analyze_e2.py`, `report_e2.py`.
3. **E3** (CE `experiments/e3/README.md`, "On Explorer, in order"): `admit.py`, two editing jobs (new queries, and the extra attempt with `--retry-from`), `reuse_e3.py`, prompts and generation; `analyze_e3.py`, `report_e3.py`.
4. **Sensitivity** (CE `experiments/README.md`): `sensitivity.sbatch` once per model; the pages are the synthetic samples in CE `samples/`.

Use the model revisions in `env/` (each job read the Hugging Face cache offline at that revision) and the cluster settings from CE `experiments/explorer/local.env.example`. vLLM ran with `enforce_eager=True` and fixed seeds; batched GPU decoding can still differ in the last digits between GPU types, so compare reruns on the aggregate results, not answer by answer.
