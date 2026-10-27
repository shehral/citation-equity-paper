# Validity counts: E1 (main and replication)

From `versions.jsonl` (withheld; hash in `results/manifests/`). valid / invalid / not_applicable per (set, arm); reasons are validator message categories with quoted text, URLs and word lists stripped and numbers masked as N; one invalid version can carry several reasons.

| set | arm | versions | valid | invalid | not applicable | most common reason |
|---|---|---|---|---|---|---|
| main | 1 | 25 | 24 | 1 | 0 | The answer must be one JSON object mapping span ids to replacements. (1) |
| main | 2 | 50 | 27 | 23 | 0 | The heading may use only words from the heading or its section's first paragraph (not: …). (22) |
| main | 3 | 46 | 39 | 7 | 0 | The answer must be one JSON object mapping span ids to replacements. (4) |
| main | 4 | 4 | 0 | 4 | 0 | After the edit the tables check is not applicable. (4) |
| main | 5 | 32 | 11 | 21 | 0 | The statistics check did not rise (N -> N). (15) |
| main | 6 | 59 | 36 | 23 | 0 | The expert-quotes check did not rise (N -> N). (16) |
| main | 7 | 73 | 30 | 8 | 35 | not applicable: the editor returned NONE (35) |
| main | 8 | 34 | 25 | 9 | 0 | The direct-answer-lead check did not rise (N -> N). (8) |
| main | 9 | 55 | 54 | 1 | 0 | The page length went from N to N words (Nx; allowed N-Nx). (1) |
| main | 10 | 21 | 8 | 13 | 0 | The comparisons check did not rise (N -> N). (13) |
| main | 11 | 30 | 30 | 0 | 0 | |
| main | 12 | 63 | 50 | 13 | 0 | Add only the query's key terms and function words (not: …). (7) |
| main | 13 | 43 | 42 | 1 | 0 | No section was split under a new heading. (1) |
| main | 14 | 7 | 7 | 0 | 0 | |
| main | P2 | 27 | 17 | 10 | 0 | Do not add facts that are not in the allowed sources: name '…'. (6) |
| main | P3 | 39 | 33 | 6 | 0 | Keep exactly the query key terms the spans contain (lost: …, added: …). (1) |
| main | P5 | 11 | 4 | 7 | 0 | Do not add facts that are not in the allowed sources: name '…'. (3) |
| main | P6 | 36 | 26 | 10 | 0 | Reword the spans: the answer left every span unchanged. (5) |
| main | P7 | 30 | 25 | 5 | 0 | The paraphrase changed the cited-sources check (N -> N); keep the same structure, figures, quotes and links. (4) |
| main | P8 | 25 | 20 | 5 | 0 | Do not add facts that are not in the allowed sources: name '…'. (2) |
| main | P10 | 8 | 8 | 0 | 0 | |
| main | P12 | 50 | 33 | 17 | 0 | Do not add facts that are not in the allowed sources: name '…'. (11) |
| main | ALL | 79 | 78 | 1 | 0 | every step failed (1) |
| main | P_ALL | 75 | 53 | 22 | 0 | Do not add facts that are not in the allowed sources: name '…'. (12) |
| main | original | 80 | 80 | 0 | 0 | |
| replication | 5 | 21 | 3 | 18 | 0 | The statistics check did not rise (N -> N). (13) |
| replication | 6 | 54 | 26 | 28 | 0 | The expert-quotes check did not rise (N -> N). (22) |
| replication | 7 | 53 | 30 | 3 | 20 | not applicable: the editor returned NONE (20) |
| replication | 9 | 53 | 52 | 1 | 0 | The page length went from N to N words (Nx; allowed N-Nx). (1) |
| replication | 11 | 18 | 18 | 0 | 0 | |
| replication | 12 | 28 | 14 | 14 | 0 | Do not add facts that are not in the allowed sources: name '…'. (6) |
| replication | P5 | 3 | 2 | 1 | 0 | The paraphrase must keep the spans' length within N% (N -> N words). (1) |
| replication | P6 | 26 | 18 | 8 | 0 | Do not add facts that are not in the allowed sources: name '…'. (3) |
| replication | P7 | 30 | 29 | 1 | 0 | Do not add facts that are not in the allowed sources: name '…'. (1) |
| replication | P12 | 14 | 12 | 2 | 0 | Reword the spans: the answer left every span unchanged. (1) |
| replication | ALL | 60 | 58 | 2 | 0 | every step failed (2) |
| replication | P_ALL | 35 | 32 | 3 | 0 | Reword the spans: the answer left every span unchanged. (2) |
| replication | original | 60 | 60 | 0 | 0 | |
