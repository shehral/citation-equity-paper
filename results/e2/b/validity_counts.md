# Validity counts: E2b (editor Qwen3.8-27B)

From `versions.jsonl` (withheld; hash in `results/manifests/`). valid / invalid / not_applicable per (set, arm); reasons are validator message categories with quoted text, URLs and word lists stripped and numbers masked as N; one invalid version can carry several reasons.

| set | arm | versions | valid | invalid | not applicable | most common reason |
|---|---|---|---|---|---|---|
| main | 12 | 63 | 49 | 14 | 0 | Unknown span id '…'; use only the ids given (…). (5) |
| main | P12 | 49 | 29 | 20 | 0 | The paraphrase must keep the spans' length within N% (N -> N words). (8) |
| main | ALL | 79 | 77 | 2 | 0 | every step failed (2) |
| main | P_ALL | 71 | 44 | 27 | 0 | Do not add facts that are not in the allowed sources: name '…'. (12) |
| main | original | 80 | 80 | 0 | 0 | |
