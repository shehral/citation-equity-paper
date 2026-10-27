# Cluster jobs

Every Slurm job of the sensitivity test, the smoke test and E1 to E3 on Explorer, from
`sacct -u $USER --starttime 2026-10-23 -X -n -P -o JobID,JobName%60,Partition,AllocTRES%60,State,Elapsed,Start,End` (plus NodeList).
AllocTRES records the GPU count but not its type, so the type comes from the node's gres (`sinfo -N -o '%N|%G'`) and the exact model from the `nvidia-smi` line the job printed. Times are the cluster's clock (US Eastern). Machine-readable copy: `jobs.csv`; totals: `gpu_hours.json`; each job's start/end lines and JSON summary: `logs/`.

## GPU-hours

| experiment | GPU-hours |
|---|---|
| smoke | 0.44 |
| sensitivity | 0.86 |
| e1 | 7.60 |
| e2a | 1.92 |
| e2b | 1.89 |
| e3 | 4.16 |
| E2 (a + b) | 3.81 |
| **overall** | **16.87** |

| experiment : GPU type | GPU-hours |
|---|---|
| e1:a100 | 3.44 |
| e1:h200 | 4.17 |
| e2a:a100 | 1.17 |
| e2a:h200 | 0.74 |
| e2b:a100 | 1.47 |
| e2b:h200 | 0.43 |
| e3:a100 | 2.17 |
| e3:h200 | 1.99 |
| sensitivity:a100 | 0.63 |
| sensitivity:h200 | 0.23 |
| smoke:a100 | 0.44 |

| experiment : role | GPU-hours |
|---|---|
| e1:edit pages | 0.82 |
| e1:judge answers | 5.73 |
| e1:timing smoke (held-out query, outcomes discarded) | 1.06 |
| e2a:judge answers | 1.92 |
| e2b:edit pages | 0.43 |
| e2b:judge answers | 1.47 |
| e3:edit pages | 0.60 |
| e3:judge answers | 3.29 |
| e3:judge answers (E1 queries, extra attempt) | 0.27 |
| sensitivity:sensitivity test | 0.86 |
| smoke:vLLM smoke test | 0.44 |

## Jobs

| job | name | role | partition | GPU | elapsed | GPU-h | state | start | model | summary |
|---|---|---|---|---|---|---|---|---|---|---|
| 11339224 | `ce-smoke` | vLLM smoke test | gpu | 1 x A100-SXM4-80GB | 00:26:15 | 0.44 | COMPLETED | 2026-10-23T22:41:26 | google/gemma-4-12B-it | [log](logs/ce-smoke-11339224.summary.txt) |
| 11339589 | `ce-sens` | sensitivity test | gpu-short | 1 x A100-SXM4-40GB | 00:23:39 | 0.39 | COMPLETED | 2026-10-23T23:18:39 | Qwen/Qwen3.5-9B | [log](logs/ce-sens-11339589.summary.txt) |
| 11339592 | `ce-sens` | sensitivity test | gpu-short | 1 x A100-SXM4-80GB | 00:14:24 | 0.24 | COMPLETED | 2026-10-23T23:18:39 | google/gemma-4-12B-it | [log](logs/ce-sens-11339592.summary.txt) |
| 11339595 | `ce-sens` | sensitivity test | gpu | 1 x H200 | 00:05:55 | 0.10 | COMPLETED | 2026-10-23T23:18:39 | Qwen/Qwen3.8-27B | [log](logs/ce-sens-11339595.summary.txt) |
| 11339599 | `ce-sens` | sensitivity test | gpu-short | 1 x H200 | 00:07:40 | 0.13 | COMPLETED | 2026-10-23T23:34:02 | google/gemma-4-31B-it | [log](logs/ce-sens-11339599.summary.txt) |
| 11341059 | `ce-e1-norm` | normalize pages (CPU) | short | none | 00:05:02 | 0.00 | COMPLETED | 2026-10-24T02:19:10 |  | [log](logs/ce-e1-norm-11341059.summary.txt) |
| 11341125 | `ce-e1-norm` | normalize pages (CPU) | short | none | 00:04:14 | 0.00 | COMPLETED | 2026-10-24T02:25:38 |  | [log](logs/ce-e1-norm-11341125.summary.txt) |
| 11341421 | `ce-e1-edit` | timing smoke (held-out query, outcomes discarded) | gpu | 1 x H200 | 00:03:46 | 0.06 | COMPLETED | 2026-10-24T03:11:02 | google/gemma-4-31B-it | [log](logs/ce-e1-edit-11341421.summary.txt) |
| 11341488 | `ce-e1-gen` | timing smoke (held-out query, outcomes discarded) | gpu | 1 x H200 | 00:08:02 | 0.13 | COMPLETED | 2026-10-24T03:20:33 | Qwen/Qwen3.8-27B | [log](logs/ce-e1-gen-11341488.summary.txt) |
| 11341487 | `ce-e1-gen` | timing smoke (held-out query, outcomes discarded) | gpu | 1 x A100-SXM4-40GB | 00:12:06 | 0.20 | COMPLETED | 2026-10-24T03:24:24 | google/gemma-4-12B-it | [log](logs/ce-e1-gen-11341487.summary.txt) |
| 11341614 | `ce-e1-edit` | timing smoke (held-out query, outcomes discarded) | gpu | 1 x H200 | 00:14:37 | 0.24 | COMPLETED | 2026-10-24T03:48:13 | google/gemma-4-31B-it | [log](logs/ce-e1-edit-11341614.summary.txt) |
| 11341710 | `ce-e1-edit` | timing smoke (held-out query, outcomes discarded) | gpu | 1 x H200 | 00:25:05 | 0.42 | COMPLETED | 2026-10-24T04:07:32 | google/gemma-4-31B-it | [log](logs/ce-e1-edit-11341710.summary.txt) |
| 11342078 | `ce-e1-edit-rep` | edit pages | gpu | none | 00:00:00 | 0.00 | CANCELLED | None |  |  |
| 11342076 | `ce-e1-edit-main` | edit pages | gpu | 1 x H200 | 00:26:46 | 0.45 | COMPLETED | 2026-10-24T04:34:28 | google/gemma-4-31B-it | [log](logs/ce-e1-edit-main-11342076.summary.txt) |
| 11342083 | `ce-e1-edit-rep` | edit pages | gpu | 1 x H200 | 00:22:19 | 0.37 | COMPLETED | 2026-10-24T04:46:32 | google/gemma-4-31B-it | [log](logs/ce-e1-edit-rep-11342083.summary.txt) |
| 11342630 | `ce-e1-gen-main.gemma-4-12b.tier1` | judge answers | gpu | 1 x A100-SXM4-80GB | 01:00:36 | 1.01 | COMPLETED | 2026-10-24T05:28:07 | google/gemma-4-12B-it | [log](logs/ce-e1-gen-main.gemma-4-12b.tier1-11342630.summary.txt) |
| 11342633 | `ce-e1-gen-main.qwen3.8-27b.tier1` | judge answers | gpu | 1 x H200 | 01:01:53 | 1.03 | COMPLETED | 2026-10-24T05:28:49 | Qwen/Qwen3.8-27B | [log](logs/ce-e1-gen-main.qwen3.8-27b.tier1-11342633.summary.txt) |
| 11342635 | `ce-e1-gen-main.qwen3.8-27b.tier2` | judge answers | gpu-short | 1 x H200 | 00:32:00 | 0.53 | COMPLETED | 2026-10-24T05:34:22 | Qwen/Qwen3.8-27B | [log](logs/ce-e1-gen-main.qwen3.8-27b.tier2-11342635.summary.txt) |
| 11342636 | `ce-e1-gen-replication.qwen3.8-27b.tier1` | judge answers | gpu-short | 1 x H200 | 00:29:49 | 0.50 | COMPLETED | 2026-10-24T05:47:16 | Qwen/Qwen3.8-27B | [log](logs/ce-e1-gen-replication.qwen3.8-27b.tier1-11342636.summary.txt) |
| 11342631 | `ce-e1-gen-main.gemma-4-12b.tier2` | judge answers | gpu | 1 x A100-SXM4-40GB | 00:57:48 | 0.96 | COMPLETED | 2026-10-24T05:50:56 | google/gemma-4-12B-it | [log](logs/ce-e1-gen-main.gemma-4-12b.tier2-11342631.summary.txt) |
| 11342641 | `ce-e1-gen-main.qwen3.8-27b.tier3` | judge answers | gpu-short | 1 x H200 | 00:16:46 | 0.28 | COMPLETED | 2026-10-24T06:07:21 | Qwen/Qwen3.8-27B | [log](logs/ce-e1-gen-main.qwen3.8-27b.tier3-11342641.summary.txt) |
| 11342643 | `ce-e1-gen-replication.qwen3.8-27b.tier2` | judge answers | gpu-short | 1 x H200 | 00:04:32 | 0.08 | COMPLETED | 2026-10-24T06:17:18 | Qwen/Qwen3.8-27B | [log](logs/ce-e1-gen-replication.qwen3.8-27b.tier2-11342643.summary.txt) |
| 11342644 | `ce-e1-gen-replication.qwen3.8-27b.tier3` | judge answers | gpu-short | 1 x H200 | 00:04:22 | 0.07 | COMPLETED | 2026-10-24T06:22:31 | Qwen/Qwen3.8-27B | [log](logs/ce-e1-gen-replication.qwen3.8-27b.tier3-11342644.summary.txt) |
| 11342632 | `ce-e1-gen-replication.gemma-4-12b.tier1` | judge answers | gpu | 1 x A100-SXM4-80GB | 00:38:26 | 0.64 | COMPLETED | 2026-10-24T06:29:08 | google/gemma-4-12B-it | [log](logs/ce-e1-gen-replication.gemma-4-12b.tier1-11342632.summary.txt) |
| 11342634 | `ce-e1-gen-main.gemma-4-12b.tier3` | judge answers | gpu-short | 1 x A100-SXM4-80GB | 00:22:59 | 0.38 | COMPLETED | 2026-10-24T06:32:28 | google/gemma-4-12B-it | [log](logs/ce-e1-gen-main.gemma-4-12b.tier3-11342634.summary.txt) |
| 11342637 | `ce-e1-gen-replication.gemma-4-12b.tier2` | judge answers | gpu-short | 1 x A100-SXM4-40GB | 00:08:36 | 0.14 | COMPLETED | 2026-10-24T06:48:52 | google/gemma-4-12B-it | [log](logs/ce-e1-gen-replication.gemma-4-12b.tier2-11342637.summary.txt) |
| 11342642 | `ce-e1-gen-replication.gemma-4-12b.tier3` | judge answers | gpu-short | 1 x A100-SXM4-80GB | 00:05:46 | 0.10 | COMPLETED | 2026-10-24T06:55:29 | google/gemma-4-12B-it | [log](logs/ce-e1-gen-replication.gemma-4-12b.tier3-11342642.summary.txt) |
| 11351366 | `ce-e2a-main.gemma-4-12b.tier1` | judge answers | gpu | 1 x A100-SXM4-40GB | 00:38:06 | 0.64 | COMPLETED | 2026-10-24T18:01:07 | google/gemma-4-12B-it | [log](logs/ce-e2a-main.gemma-4-12b.tier1-11351366.summary.txt) |
| 11351367 | `ce-e2a-replication.gemma-4-12b.tier1` | judge answers | gpu | 1 x A100-SXM4-40GB | 00:32:18 | 0.54 | COMPLETED | 2026-10-24T18:01:07 | google/gemma-4-12B-it | [log](logs/ce-e2a-replication.gemma-4-12b.tier1-11351367.summary.txt) |
| 11351370 | `ce-e2b-edit` | edit pages | gpu | 1 x H200 | 00:25:31 | 0.43 | COMPLETED | 2026-10-24T18:15:15 | Qwen/Qwen3.8-27B | [log](logs/ce-e2b-edit-11351370.summary.txt) |
| 11351368 | `ce-e2a-main.qwen3.8-27b.tier1` | judge answers | gpu-short | 1 x H200 | 00:24:01 | 0.40 | COMPLETED | 2026-10-24T18:22:22 | Qwen/Qwen3.8-27B | [log](logs/ce-e2a-main.qwen3.8-27b.tier1-11351368.summary.txt) |
| 11351369 | `ce-e2a-replication.qwen3.8-27b.tier1` | judge answers | gpu-short | 1 x H200 | 00:20:33 | 0.34 | COMPLETED | 2026-10-24T18:27:30 | Qwen/Qwen3.8-27B | [log](logs/ce-e2a-replication.qwen3.8-27b.tier1-11351369.summary.txt) |
| 11352310 | `ce-e2b-main.gemma-4-12b.tier1` | judge answers | gpu | 1 x A100-SXM4-80GB | 00:26:15 | 0.44 | COMPLETED | 2026-10-24T19:26:37 | google/gemma-4-12B-it | [log](logs/ce-e2b-main.gemma-4-12b.tier1-11352310.summary.txt) |
| 11352311 | `ce-e2b-main.gemma-4-12b.tier2` | judge answers | gpu | 1 x A100-SXM4-80GB | 00:17:53 | 0.30 | COMPLETED | 2026-10-24T19:27:39 | google/gemma-4-12B-it | [log](logs/ce-e2b-main.gemma-4-12b.tier2-11352311.summary.txt) |
| 11352316 | `ce-e2b-main.qwen3.5-9b.tier1` | judge answers | gpu | 1 x A100-SXM4-40GB | 00:30:22 | 0.51 | COMPLETED | 2026-10-24T19:30:10 | Qwen/Qwen3.5-9B | [log](logs/ce-e2b-main.qwen3.5-9b.tier1-11352316.summary.txt) |
| 11352318 | `ce-e2b-main.qwen3.5-9b.tier2` | judge answers | gpu-short | 1 x A100-SXM4-80GB | 00:13:25 | 0.22 | COMPLETED | 2026-10-24T19:45:39 | Qwen/Qwen3.5-9B | [log](logs/ce-e2b-main.qwen3.5-9b.tier2-11352318.summary.txt) |
| 11353459 | `ce-e3-edit-new` | edit pages | gpu | 1 x H200 | 00:30:42 | 0.51 | COMPLETED | 2026-10-24T20:01:08 | google/gemma-4-31B-it | [log](logs/ce-e3-edit-new-11353459.summary.txt) |
| 11353461 | `ce-e3-edit-retry` | edit pages | gpu | 1 x H200 | 00:05:34 | 0.09 | COMPLETED | 2026-10-24T20:08:33 | google/gemma-4-31B-it | [log](logs/ce-e3-edit-retry-11353461.summary.txt) |
| 11354081 | `ce-e3-e3.gemma-4-12b.tierall` | judge answers | gpu | 1 x A100-SXM4-80GB | 00:59:05 | 0.98 | COMPLETED | 2026-10-24T20:50:00 | google/gemma-4-12B-it | [log](logs/ce-e3-e3.gemma-4-12b.tierall-11354081.summary.txt) |
| 11354085 | `ce-e3-e3-four.gemma-4-12b.tierall` | judge answers | gpu | 1 x A100-SXM4-40GB | 00:57:59 | 0.97 | COMPLETED | 2026-10-24T20:57:55 | google/gemma-4-12B-it | [log](logs/ce-e3-e3-four.gemma-4-12b.tierall-11354085.summary.txt) |
| 11354087 | `ce-e3-e3.qwen3.8-27b.tierall` | judge answers | gpu | 1 x H200 | 00:43:38 | 0.73 | COMPLETED | 2026-10-24T20:57:55 | Qwen/Qwen3.8-27B | [log](logs/ce-e3-e3.qwen3.8-27b.tierall-11354087.summary.txt) |
| 11354088 | `ce-e3-e3-four.qwen3.8-27b.tierall` | judge answers | gpu | 1 x H200 | 00:36:25 | 0.61 | COMPLETED | 2026-10-24T21:04:10 | Qwen/Qwen3.8-27B | [log](logs/ce-e3-e3-four.qwen3.8-27b.tierall-11354088.summary.txt) |
| 11354089 | `ce-e3-main.gemma-4-12b.tierall` | judge answers (E1 queries, extra attempt) | gpu-short | 1 x A100-SXM4-80GB | 00:13:13 | 0.22 | COMPLETED | 2026-10-24T21:05:57 | google/gemma-4-12B-it | [log](logs/ce-e3-main.gemma-4-12b.tierall-11354089.summary.txt) |
| 11354090 | `ce-e3-main.qwen3.8-27b.tierall` | judge answers (E1 queries, extra attempt) | gpu-short | 1 x H200 | 00:02:58 | 0.05 | COMPLETED | 2026-10-24T21:17:58 | Qwen/Qwen3.8-27B | [log](logs/ce-e3-main.qwen3.8-27b.tierall-11354090.summary.txt) |
