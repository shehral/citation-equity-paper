# Withheld files: path, line count, sha256

Every file below stays on the owner's machine (`local`, paths relative to `citation-equity/experiments/`) or on Explorer (`cluster`, paths relative to the project folder `$CE_ROOT_PARENT/geo`). None is in this repo: they hold third-party page text, edited versions, prompts, editor logs or raw model answers. A rerun that produces the same bytes has the same sha256. Machine-readable copy: `withheld.csv`.

## e1

| location | path | lines | bytes | sha256 | what it is |
|---|---|---|---|---|---|
| cluster | `data/e1/.pages.jsonl.gHgMmU` | 705 | 6029573 | `b4ad4a6d84b403dbb94a6501bc83567084aeaf23b827aba5130cbc3938afb65a` | temporary copy of pages.jsonl left by an interrupted write (same bytes as pages.jsonl) |
| cluster | `data/e1/admission.json` | 25 | 408 | `fb08e42ed58eb45beaeb0fff87baa0d1a0fd439f950624e256562d094c8b61ab` | admitted query ids and set sizes |
| cluster | `data/e1/applicability.jsonl` | 2115 | 196157 | `1f17fb793294c029da02514f232318cf537d4afb454319f7524930cd9c7fda77` | frozen per-query, per-arm applicability table (which checks flag something) |
| cluster | `data/e1/batches/main.gemma-4-12b.tier1.prompts.jsonl` | 3176 | 114679608 | `f6e6f9e6782649d2e8465a7aaea6c1bcdfdfbf929ba0614ecc4463bfa2279d42` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e1/batches/main.gemma-4-12b.tier2.prompts.jsonl` | 1952 | 71902112 | `5563c3ba97da4329b2746dfe8fd9a517baddcbb2496b1e42494ca884e948333e` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e1/batches/main.gemma-4-12b.tier3.prompts.jsonl` | 952 | 34623480 | `db6560c4db31b679b482084586378ca202c164e324c45f842b011e2c70bc9766` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e1/batches/main.qwen3.8-27b.tier1.prompts.jsonl` | 3176 | 114663728 | `9cc996b5bad217a9d03d0d30fb6539bce996c5af73a6584379f469de013ee8d4` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e1/batches/main.qwen3.8-27b.tier2.prompts.jsonl` | 1952 | 71892352 | `63904b12ce44ae70c0455c855502be718f3626627e887f3ad06a83292486c08e` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e1/batches/main.qwen3.8-27b.tier3.prompts.jsonl` | 952 | 34618720 | `f24ba12392c63566b35f36cb53cb98c96036e96586b9f109bd4a5f84c0df691a` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e1/batches/replication.gemma-4-12b.tier1.prompts.jsonl` | 2480 | 84504016 | `ec366444a34aac55380cd2ee949e0744fe96e59c846d506329ca477dfb89f598` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e1/batches/replication.gemma-4-12b.tier2.prompts.jsonl` | 208 | 6715656 | `caa3720972709eb3c1fcb2ea6bef9bb67f23f3cc4694362d1539d1b97473e4ba` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e1/batches/replication.gemma-4-12b.tier3.prompts.jsonl` | 144 | 4874040 | `5ae3f92d6ae9f6bbc9e7a1addfee68a599c36d238ad8ef2d4dfa19815965ae11` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e1/batches/replication.qwen3.8-27b.tier1.prompts.jsonl` | 2480 | 84491616 | `1433df6676ad158fe9def54bd0d0a92fdd1b79c747d3dc8d2a2e8d095f33fad7` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e1/batches/replication.qwen3.8-27b.tier2.prompts.jsonl` | 208 | 6714616 | `24d1a21c3aa7ce1ba2aaf186087a7652ce48a68c8cbaaf5becfc7dfa846a9bde` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e1/batches/replication.qwen3.8-27b.tier3.prompts.jsonl` | 144 | 4873320 | `dfb2d50d105071d68f50164383d1a0495ac505bd6e701d6e1de91fa7154f46c5` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e1/candidates.jsonl` | 3455 | 24057209 | `4125789c6af5ab4839306e1900b1707df034b88772003c3d904520908fec1229` | every fetched candidate page per query, with text, usability and sha256 |
| cluster | `data/e1/editor_log.jsonl` | 1397 | 18693944 | `39aa19f011aa05115634f4cde3cfb9f9dcc7b66a83c995d470ae38d0dabeee61` | editor model requests and responses per edit attempt (page text) |
| cluster | `data/e1/fetch_log.jsonl` | 4273 | 1156443 | `3067940b7c2f6ca8acafed94fdfd5a8913a772929fa898b4d4234091e1569fa1` | per-URL fetch outcome (URL, source, status, word and token counts, sha256) |
| cluster | `data/e1/pages.jsonl` | 705 | 6029573 | `b4ad4a6d84b403dbb94a6501bc83567084aeaf23b827aba5130cbc3938afb65a` | normalized pages used by the experiment (page text, roles target/other) |
| cluster | `data/e1/prompt_build.json` | 20 | 538 | `d8a9f97075aac6974ae47fca9dc3d2193c9f6dd1c733cb1d181f8d248c00c8e4` | prompt counts per batch and the token-limit refusals |
| cluster | `data/e1/prompts.jsonl` | 17824 | 634184880 | `64740dd4f447b334a2ec733fcc731a81e169cb3fc079f34da49fb04990350dbc` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e1/raw/cseo.jsonl` | 1500 | 18331597 | `f27caa8b4f9282c3592f49f42525d6805db990d820c1af4843aae94e17d19200` | C-SEO Bench pages as fetched (page text) |
| cluster | `data/e1/raw/live.jsonl` | 1955 | 36796207 | `c57dcc28adc32c65e152cb470ffdb502cbc69b07b09a17efe4bc576e2bc974df` | live fetches of the GEO-bench source URLs (page text) |
| cluster | `data/e1/raw/wayback.jsonl` | 818 | 11085424 | `a8d77ca70d7273a4bbd4eecc7dbbc85322f971606347601ab0860e75e028aaea` | 2023 Wayback fetches for pages whose live fetch failed (page text) |
| cluster | `data/e1/rep/admission.json` | 25 | 408 | `fb08e42ed58eb45beaeb0fff87baa0d1a0fd439f950624e256562d094c8b61ab` | admitted query ids and set sizes |
| cluster | `data/e1/rep/applicability.jsonl` | 2115 | 196157 | `1f17fb793294c029da02514f232318cf537d4afb454319f7524930cd9c7fda77` | frozen per-query, per-arm applicability table (which checks flag something) |
| cluster | `data/e1/rep/editor_log.jsonl` | 547 | 11646558 | `4ab993075e92b6a7b0d431b1da486413141be5198d60cc1dc239e82b5f003295` | editor model requests and responses per edit attempt (page text) |
| cluster | `data/e1/rep/pages.jsonl` | 705 | 6029573 | `b4ad4a6d84b403dbb94a6501bc83567084aeaf23b827aba5130cbc3938afb65a` | normalized pages used by the experiment (page text, roles target/other) |
| cluster | `data/e1/rep/versions.jsonl` | 455 | 4155280 | `f3cca93b55f2d34e2ebfeb8453e4499c48c847cd67924b1116b87e92d42a4ff8` | edited page versions per arm with validity flags and validator messages (page text) |
| cluster | `data/e1/versions.jsonl` | 1457 | 12191521 | `016394ffaeee8d4d6ea66f5fa70a13bf6556096c7de096efe3fa51a4186abedb` | edited page versions per arm with validity flags and validator messages (page text) |
| cluster | `data/e1/versions.main-only.jsonl` | 1002 | 8036241 | `d1d7089ed0ba0582d69b219c328e975e367b776f35e3671d09d0a055a69d5333` | edited versions of the main set only (kept from before the replication edit job) |
| cluster | `data/e1/wayback_needed.jsonl` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | pages queued for a Wayback fetch |
| cluster | `e1/answers/main.gemma-4-12b.tier1.jsonl` | 3176 | 5808121 | `1d7dd1abf6edc320d228f454190757ee0cc63c2445ff87081de1915c31424e32` | raw judge answers for one batch (raw model answers) |
| cluster | `e1/answers/main.gemma-4-12b.tier2.jsonl` | 1952 | 3568549 | `87c7e67fa6669892f9b847f9a7b3774b8452b7946cae92ee0db3f84ec5b97baa` | raw judge answers for one batch (raw model answers) |
| cluster | `e1/answers/main.gemma-4-12b.tier3.jsonl` | 952 | 1647455 | `bd4f50ca152a7b9bed2308239a740f719210fbecb04f212d24d026c02c74bcce` | raw judge answers for one batch (raw model answers) |
| cluster | `e1/answers/main.qwen3.8-27b.tier1.jsonl` | 3176 | 5470780 | `b6136941b7eb3577160240fcc72ddae04d2d89444c7234d6673ffc5f61e71a93` | raw judge answers for one batch (raw model answers) |
| cluster | `e1/answers/main.qwen3.8-27b.tier2.jsonl` | 1952 | 3378269 | `ec9b00785e1f1faa8a64c2bc5a9a866468fa7f95c25fb06db93b38b5e2f954e9` | raw judge answers for one batch (raw model answers) |
| cluster | `e1/answers/main.qwen3.8-27b.tier3.jsonl` | 952 | 1526001 | `807b4614df040cf1582254e848a0f64066173f25ad436f3bf6e3078709737e2e` | raw judge answers for one batch (raw model answers) |
| cluster | `e1/answers/replication.gemma-4-12b.tier1.jsonl` | 2480 | 3193886 | `405a54709f6924c8a69abfb0278b62c9e7afd9e37bec300afffee63d0b2de353` | raw judge answers for one batch (raw model answers) |
| cluster | `e1/answers/replication.gemma-4-12b.tier2.jsonl` | 208 | 237852 | `c3a93aa0298851a5ddeaac160802c9194b6ec09355bd2d4d63a0b75d0454ed66` | raw judge answers for one batch (raw model answers) |
| cluster | `e1/answers/replication.gemma-4-12b.tier3.jsonl` | 144 | 167744 | `eb6903c919ca4bfc73db2d0c745b130eedd60f76134b4923a3c7104b930e3bbc` | raw judge answers for one batch (raw model answers) |
| cluster | `e1/answers/replication.qwen3.8-27b.tier1.jsonl` | 2480 | 3016147 | `d63052ca03e863af0ee2f7d7255b12d6eb5142821d24551f7db6622d1ce722f5` | raw judge answers for one batch (raw model answers) |
| cluster | `e1/answers/replication.qwen3.8-27b.tier2.jsonl` | 208 | 224819 | `493e85d7b4b3cf41808c200cc6d49d7a6a201518ef6d034eaeb02f7c3ab6fa55` | raw judge answers for one batch (raw model answers) |
| cluster | `e1/answers/replication.qwen3.8-27b.tier3.jsonl` | 144 | 158161 | `771a30de197f1f7fc1ea936ee94d6ebfeb6fc1fff71f0e6331cf357a941547ef` | raw judge answers for one batch (raw model answers) |
| cluster | `e1/batches/main.gemma-4-12b.tier1.prompts.jsonl` | 3176 | 114679608 | `f6e6f9e6782649d2e8465a7aaea6c1bcdfdfbf929ba0614ecc4463bfa2279d42` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e1/batches/main.gemma-4-12b.tier2.prompts.jsonl` | 1952 | 71902112 | `5563c3ba97da4329b2746dfe8fd9a517baddcbb2496b1e42494ca884e948333e` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e1/batches/main.gemma-4-12b.tier3.prompts.jsonl` | 952 | 34623480 | `db6560c4db31b679b482084586378ca202c164e324c45f842b011e2c70bc9766` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e1/batches/main.qwen3.8-27b.tier1.prompts.jsonl` | 3176 | 114663728 | `9cc996b5bad217a9d03d0d30fb6539bce996c5af73a6584379f469de013ee8d4` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e1/batches/main.qwen3.8-27b.tier2.prompts.jsonl` | 1952 | 71892352 | `63904b12ce44ae70c0455c855502be718f3626627e887f3ad06a83292486c08e` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e1/batches/main.qwen3.8-27b.tier3.prompts.jsonl` | 952 | 34618720 | `f24ba12392c63566b35f36cb53cb98c96036e96586b9f109bd4a5f84c0df691a` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e1/batches/replication.gemma-4-12b.tier1.prompts.jsonl` | 2480 | 84504016 | `ec366444a34aac55380cd2ee949e0744fe96e59c846d506329ca477dfb89f598` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e1/batches/replication.gemma-4-12b.tier2.prompts.jsonl` | 208 | 6715656 | `caa3720972709eb3c1fcb2ea6bef9bb67f23f3cc4694362d1539d1b97473e4ba` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e1/batches/replication.gemma-4-12b.tier3.prompts.jsonl` | 144 | 4874040 | `5ae3f92d6ae9f6bbc9e7a1addfee68a599c36d238ad8ef2d4dfa19815965ae11` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e1/batches/replication.qwen3.8-27b.tier1.prompts.jsonl` | 2480 | 84491616 | `1433df6676ad158fe9def54bd0d0a92fdd1b79c747d3dc8d2a2e8d095f33fad7` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e1/batches/replication.qwen3.8-27b.tier2.prompts.jsonl` | 208 | 6714616 | `24d1a21c3aa7ce1ba2aaf186087a7652ce48a68c8cbaaf5becfc7dfa846a9bde` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e1/batches/replication.qwen3.8-27b.tier3.prompts.jsonl` | 144 | 4873320 | `dfb2d50d105071d68f50164383d1a0495ac505bd6e701d6e1de91fa7154f46c5` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `logs/ce-e1-edit-11341421.err` | 26 | 9257 | `bf2f4ba76a0069f30f38c1f8bf080121a1b2a4169a8659496ab01ea8658ed2b4` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e1-edit-11341421.out` | 142 | 11958 | `5ef4ed428d4274a28eb0f112bf786a20a00f9ada97ade55fcd9e3d19eb3816f3` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-edit-11341421.out` | 142 | 11958 | `5ef4ed428d4274a28eb0f112bf786a20a00f9ada97ade55fcd9e3d19eb3816f3` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-edit-11341614.err` | 32 | 10926 | `c077c9a23036cbbdfa55a4f16fdaec958c33c7bd18bb1d39915e84de399bbe51` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e1-edit-11341614.out` | 153 | 12094 | `6ff69541260a31f4e302e2b00cd5381b36785408a1081bf50fe031c73f49fbcf` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-edit-11341614.out` | 153 | 12094 | `6ff69541260a31f4e302e2b00cd5381b36785408a1081bf50fe031c73f49fbcf` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-edit-11341710.err` | 32 | 10923 | `b5300d80b824f2dcf1b3a81be8c6a69427880a746077d04bfa4138ed98b096d4` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e1-edit-11341710.out` | 159 | 12249 | `a9fe99bf54e2a0e9d26ca9d9d3e8a00b968f1245e6ce74ddfa7ecdce7f47aaff` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-edit-11341710.out` | 159 | 12249 | `a9fe99bf54e2a0e9d26ca9d9d3e8a00b968f1245e6ce74ddfa7ecdce7f47aaff` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-edit-main-11342076.err` | 54 | 142768 | `6ce1a58ec304a0f3e3dffd8554cfaf49298ec49203ece39ede64d55812b7b0d8` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e1-edit-main-11342076.out` | 220 | 13263 | `f634671064ae03648240c185ee970820f4dacad3fae880ac9b16113a9e1c7c0d` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-edit-main-11342076.out` | 220 | 13263 | `f634671064ae03648240c185ee970820f4dacad3fae880ac9b16113a9e1c7c0d` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-edit-rep-11342083.err` | 38 | 58240 | `6babe4839ba4460485882eb4fbfe6cc743bfe9d9c68e747511418e5b87945bf3` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e1-edit-rep-11342083.out` | 146 | 12122 | `7d8299151130dd21f54348d096f4fd07bfc0b33cdd8823bec243ec41e1848958` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-edit-rep-11342083.out` | 146 | 12122 | `7d8299151130dd21f54348d096f4fd07bfc0b33cdd8823bec243ec41e1848958` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-gen-11341487.err` | 8 | 9737 | `006a1525204fb5357532df3452f87533b003301940a262ad193d23b6bc29713f` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e1-gen-11341487.out` | 68 | 11016 | `9ec3f32cf887aab07048288f8da6cc177cee2f2a86a2e1b6058dc67f74561b92` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-gen-11341487.out` | 68 | 11016 | `9ec3f32cf887aab07048288f8da6cc177cee2f2a86a2e1b6058dc67f74561b92` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-gen-11341488.err` | 24 | 9582 | `be7752d92f152dbea487ce2ae131b75dd1f217e462a03b71e20e98d22990bab4` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e1-gen-11341488.out` | 84 | 14234 | `d6c232dc2d8f6c30b6386aaee6b5afb4245828d2dcbe90f4a1e57be6c6880745` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-gen-11341488.out` | 84 | 14234 | `d6c232dc2d8f6c30b6386aaee6b5afb4245828d2dcbe90f4a1e57be6c6880745` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-gen-main.gemma-4-12b.tier1-11342630.err` | 7 | 338554 | `c6e563179257ad8d6eefa1c099f3a5c1a1681d19d8a533cf863df328172ccbea` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e1-gen-main.gemma-4-12b.tier1-11342630.out` | 87 | 11433 | `43ea17818a7f406d0d1f05a2cdd5dd9dbe067f00d02710f3578ef2618b86e516` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-gen-main.gemma-4-12b.tier1-11342630.out` | 87 | 11433 | `43ea17818a7f406d0d1f05a2cdd5dd9dbe067f00d02710f3578ef2618b86e516` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-gen-main.gemma-4-12b.tier2-11342631.err` | 8 | 257617 | `56422d56c7ef1a32c53509586925f1a3bd0a3f8265694a0f660d78d74d27561c` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e1-gen-main.gemma-4-12b.tier2-11342631.out` | 114 | 11834 | `8c215a5bc7b16ebc5dd40824aa1039f946df5dc2ede95a8af86a92748f287b53` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-gen-main.gemma-4-12b.tier2-11342631.out` | 114 | 11834 | `8c215a5bc7b16ebc5dd40824aa1039f946df5dc2ede95a8af86a92748f287b53` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-gen-main.gemma-4-12b.tier3-11342634.err` | 7 | 100199 | `96a140b11a73d37c45d6645e57bb998c6551e7a69e57a50b463bfa4adddd0a38` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e1-gen-main.gemma-4-12b.tier3-11342634.out` | 68 | 11026 | `1137f47c41efde7ba58417e108368441c52267bede83cbd26228704f674c5688` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-gen-main.gemma-4-12b.tier3-11342634.out` | 68 | 11026 | `1137f47c41efde7ba58417e108368441c52267bede83cbd26228704f674c5688` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-gen-main.qwen3.8-27b.tier1-11342633.err` | 24 | 383356 | `9acd6ffa570e2ce328f18136affc02a5551b00b4596f10b8c5225378a4b4fb19` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e1-gen-main.qwen3.8-27b.tier1-11342633.out` | 108 | 14734 | `3819106820cc22f1eb3d99f19521a309fc54e5b8b0cf0d800e58f2a2a6670783` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-gen-main.qwen3.8-27b.tier1-11342633.out` | 108 | 14734 | `3819106820cc22f1eb3d99f19521a309fc54e5b8b0cf0d800e58f2a2a6670783` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-gen-main.qwen3.8-27b.tier2-11342635.err` | 24 | 238583 | `eef3d26be4519d042e174263b13886e2c0e272c281c3e0043481daecef797930` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e1-gen-main.qwen3.8-27b.tier2-11342635.out` | 96 | 14493 | `1690bb94a609a58b1d1d744f26187925c141dafeec446de52d75fff9be2e26fb` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-gen-main.qwen3.8-27b.tier2-11342635.out` | 96 | 14493 | `1690bb94a609a58b1d1d744f26187925c141dafeec446de52d75fff9be2e26fb` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-gen-main.qwen3.8-27b.tier3-11342641.err` | 24 | 114148 | `6c8b6b6029b97bd795a1691767534034575b238d550b2f8e8f7982dd9c886a4a` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e1-gen-main.qwen3.8-27b.tier3-11342641.out` | 89 | 14272 | `0a739bfa72efda961bae8dbcfeb54a60be92d9e1498c956accad29123112ac05` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-gen-main.qwen3.8-27b.tier3-11342641.out` | 89 | 14272 | `0a739bfa72efda961bae8dbcfeb54a60be92d9e1498c956accad29123112ac05` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-gen-replication.gemma-4-12b.tier1-11342632.err` | 7 | 231817 | `91df6d44322a3fb5fedde30380dda0452a45fb3b58704f443133c29be3d457a4` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e1-gen-replication.gemma-4-12b.tier1-11342632.out` | 76 | 11223 | `591cd3a67fb4d985571bde2e19fcc93b7c2f5e9fdbf5ca5c4d6bb64332c6a91b` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-gen-replication.gemma-4-12b.tier1-11342632.out` | 76 | 11223 | `591cd3a67fb4d985571bde2e19fcc93b7c2f5e9fdbf5ca5c4d6bb64332c6a91b` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-gen-replication.gemma-4-12b.tier2-11342637.err` | 8 | 25819 | `127d097f49695e165afc28c82dc6eff738bc4fa778ef25dcf59d924ef366bd8f` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e1-gen-replication.gemma-4-12b.tier2-11342637.out` | 66 | 10989 | `298f98c54e4d22c1fe3fb80b0d48698f3aa0744151910d32c1e62a6b3197ce86` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-gen-replication.gemma-4-12b.tier2-11342637.out` | 66 | 10989 | `298f98c54e4d22c1fe3fb80b0d48698f3aa0744151910d32c1e62a6b3197ce86` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-gen-replication.gemma-4-12b.tier3-11342642.err` | 7 | 14397 | `f8e78562f7f1c96481128fe6292f09a354c6d6bcb9c3b363635ea06f99ea76cd` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e1-gen-replication.gemma-4-12b.tier3-11342642.out` | 59 | 10857 | `aac4cc1a243f0faffad92d6ef7723fe49a48aaa1a32effddb7bcffac3cb43edf` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-gen-replication.gemma-4-12b.tier3-11342642.out` | 59 | 10857 | `aac4cc1a243f0faffad92d6ef7723fe49a48aaa1a32effddb7bcffac3cb43edf` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-gen-replication.qwen3.8-27b.tier1-11342636.err` | 24 | 268988 | `05ca5ec5170357f242ff6c3c3443dc9729761548b70f26a6530dd580851b23c9` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e1-gen-replication.qwen3.8-27b.tier1-11342636.out` | 95 | 14426 | `90df04ac2fcbcbeca6d35354f2b53db81ce3e831b67b1c0fbdbcea5f71a26a79` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-gen-replication.qwen3.8-27b.tier1-11342636.out` | 95 | 14426 | `90df04ac2fcbcbeca6d35354f2b53db81ce3e831b67b1c0fbdbcea5f71a26a79` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-gen-replication.qwen3.8-27b.tier2-11342643.err` | 24 | 21268 | `b44b6b8bc84de0e9cc1eabb0387f881c21ebc925d231fca7a28956f991241bd9` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e1-gen-replication.qwen3.8-27b.tier2-11342643.out` | 83 | 14227 | `6576d199104be75d1933ff58ab0bbf504ccdea84e2c7f059886283e49310290c` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-gen-replication.qwen3.8-27b.tier2-11342643.out` | 83 | 14227 | `6576d199104be75d1933ff58ab0bbf504ccdea84e2c7f059886283e49310290c` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-gen-replication.qwen3.8-27b.tier3-11342644.err` | 24 | 15068 | `fa1d4839465af63d74a15556d703f87ab4c5a5664e34ef60cf618809eb43606c` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e1-gen-replication.qwen3.8-27b.tier3-11342644.out` | 83 | 14227 | `6d8ea843d35cf35ecade1fc767bab51b00c94167d07ceeab17e20648b4fbbe11` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-gen-replication.qwen3.8-27b.tier3-11342644.out` | 83 | 14227 | `6d8ea843d35cf35ecade1fc767bab51b00c94167d07ceeab17e20648b4fbbe11` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-norm-11341059.err` | 1 | 203 | `971659c1cbd4f1b3a26bd7efebc632c8eb7add8258421b325f8e3e71d9b726c9` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e1-norm-11341059.out` | 10 | 261 | `155bbff02794c7aab08dcc4e6a480a4b057c8d834a9dd771e693c11b58b2f10a` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-norm-11341059.out` | 10 | 261 | `155bbff02794c7aab08dcc4e6a480a4b057c8d834a9dd771e693c11b58b2f10a` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-norm-11341125.err` | 1 | 203 | `971659c1cbd4f1b3a26bd7efebc632c8eb7add8258421b325f8e3e71d9b726c9` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e1-norm-11341125.out` | 10 | 260 | `39db9cca32e4d810ff8473c6fb3e51133ac36e7ac4b7cf41a1fbceb5ac561065` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e1-norm-11341125.out` | 10 | 260 | `39db9cca32e4d810ff8473c6fb3e51133ac36e7ac4b7cf41a1fbceb5ac561065` | job stdout; summary lines are in results/runs/logs/ |
| local | `e1/data/admission.json` | 25 | 408 | `fb08e42ed58eb45beaeb0fff87baa0d1a0fd439f950624e256562d094c8b61ab` | admitted query ids and set sizes |
| local | `e1/data/answers/main.gemma-4-12b.tier1.jsonl` | 3176 | 5808121 | `1d7dd1abf6edc320d228f454190757ee0cc63c2445ff87081de1915c31424e32` | raw judge answers for one batch (raw model answers) |
| local | `e1/data/answers/main.gemma-4-12b.tier2.jsonl` | 1952 | 3568549 | `87c7e67fa6669892f9b847f9a7b3774b8452b7946cae92ee0db3f84ec5b97baa` | raw judge answers for one batch (raw model answers) |
| local | `e1/data/answers/main.gemma-4-12b.tier3.jsonl` | 952 | 1647455 | `bd4f50ca152a7b9bed2308239a740f719210fbecb04f212d24d026c02c74bcce` | raw judge answers for one batch (raw model answers) |
| local | `e1/data/answers/main.qwen3.8-27b.tier1.jsonl` | 3176 | 5470780 | `b6136941b7eb3577160240fcc72ddae04d2d89444c7234d6673ffc5f61e71a93` | raw judge answers for one batch (raw model answers) |
| local | `e1/data/answers/main.qwen3.8-27b.tier2.jsonl` | 1952 | 3378269 | `ec9b00785e1f1faa8a64c2bc5a9a866468fa7f95c25fb06db93b38b5e2f954e9` | raw judge answers for one batch (raw model answers) |
| local | `e1/data/answers/main.qwen3.8-27b.tier3.jsonl` | 952 | 1526001 | `807b4614df040cf1582254e848a0f64066173f25ad436f3bf6e3078709737e2e` | raw judge answers for one batch (raw model answers) |
| local | `e1/data/answers/replication.gemma-4-12b.tier1.jsonl` | 2480 | 3193886 | `405a54709f6924c8a69abfb0278b62c9e7afd9e37bec300afffee63d0b2de353` | raw judge answers for one batch (raw model answers) |
| local | `e1/data/answers/replication.gemma-4-12b.tier2.jsonl` | 208 | 237852 | `c3a93aa0298851a5ddeaac160802c9194b6ec09355bd2d4d63a0b75d0454ed66` | raw judge answers for one batch (raw model answers) |
| local | `e1/data/answers/replication.gemma-4-12b.tier3.jsonl` | 144 | 167744 | `eb6903c919ca4bfc73db2d0c745b130eedd60f76134b4923a3c7104b930e3bbc` | raw judge answers for one batch (raw model answers) |
| local | `e1/data/answers/replication.qwen3.8-27b.tier1.jsonl` | 2480 | 3016147 | `d63052ca03e863af0ee2f7d7255b12d6eb5142821d24551f7db6622d1ce722f5` | raw judge answers for one batch (raw model answers) |
| local | `e1/data/answers/replication.qwen3.8-27b.tier2.jsonl` | 208 | 224819 | `493e85d7b4b3cf41808c200cc6d49d7a6a201518ef6d034eaeb02f7c3ab6fa55` | raw judge answers for one batch (raw model answers) |
| local | `e1/data/answers/replication.qwen3.8-27b.tier3.jsonl` | 144 | 158161 | `771a30de197f1f7fc1ea936ee94d6ebfeb6fc1fff71f0e6331cf357a941547ef` | raw judge answers for one batch (raw model answers) |
| local | `e1/data/applicability.jsonl` | 2115 | 196157 | `1f17fb793294c029da02514f232318cf537d4afb454319f7524930cd9c7fda77` | frozen per-query, per-arm applicability table (which checks flag something) |
| local | `e1/data/candidates.jsonl` | 3455 | 24057209 | `4125789c6af5ab4839306e1900b1707df034b88772003c3d904520908fec1229` | every fetched candidate page per query, with text, usability and sha256 |
| local | `e1/data/engine_original.jsonl` | 141 | 1433872 | `2026faf179f639fda654939a667fe56e371cfedd5c8ea243d21d33917785f70e` | engine check results on each original page (spans quote page text) |
| local | `e1/data/fetch_log.jsonl` | 4259 | 1152296 | `6fc79e3a85580dba4e9850433530f881fa573715ed35cb4463d719812b386048` | per-URL fetch outcome (URL, source, status, word and token counts, sha256) |
| local | `e1/data/pages.jsonl` | 705 | 6029573 | `b4ad4a6d84b403dbb94a6501bc83567084aeaf23b827aba5130cbc3938afb65a` | normalized pages used by the experiment (page text, roles target/other) |
| local | `e1/data/prompt_build.json` | 20 | 538 | `d8a9f97075aac6974ae47fca9dc3d2193c9f6dd1c733cb1d181f8d248c00c8e4` | prompt counts per batch and the token-limit refusals |
| local | `e1/data/prompts.jsonl` | 17824 | 634184880 | `64740dd4f447b334a2ec733fcc731a81e169cb3fc079f34da49fb04990350dbc` | judge prompts, one per (version, judge, seed); they hold the full page text |
| local | `e1/data/raw/cseo.jsonl` | 1500 | 18331597 | `f27caa8b4f9282c3592f49f42525d6805db990d820c1af4843aae94e17d19200` | C-SEO Bench pages as fetched (page text) |
| local | `e1/data/raw/live.jsonl` | 1955 | 36796207 | `c57dcc28adc32c65e152cb470ffdb502cbc69b07b09a17efe4bc576e2bc974df` | live fetches of the GEO-bench source URLs (page text) |
| local | `e1/data/raw/wayback.jsonl` | 818 | 11085424 | `a8d77ca70d7273a4bbd4eecc7dbbc85322f971606347601ab0860e75e028aaea` | 2023 Wayback fetches for pages whose live fetch failed (page text) |
| local | `e1/data/versions.jsonl` | 1457 | 12191521 | `016394ffaeee8d4d6ea66f5fa70a13bf6556096c7de096efe3fa51a4186abedb` | edited page versions per arm with validity flags and validator messages (page text) |
| local | `e1/data/wayback_needed.jsonl` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | pages queued for a Wayback fetch |
| local | `e1/out/fetch-run.log` | 541 | 57234 | `4e90bb5218582b2c94d33f672096054b5e1cb2bb0633618bf3a0ee8c72222e50` | local console log of the live fetch run |

## e1-timing

| location | path | lines | bytes | sha256 | what it is |
|---|---|---|---|---|---|
| cluster | `data/e1/timing/applicability.jsonl` | 2115 | 196157 | `1f17fb793294c029da02514f232318cf537d4afb454319f7524930cd9c7fda77` | frozen per-query, per-arm applicability table (which checks flag something) |
| cluster | `data/e1/timing/batches/timing.gemma-4-12b.tier1.prompts.jsonl` | 32 | 1182536 | `b277dafc6b9a69f63812a3ecb29afc2903177bcea37ab7c1b76ef93c9f5c7821` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e1/timing/batches/timing.gemma-4-12b.tier2.prompts.jsonl` | 32 | 1180128 | `e5e79331f5ea90763c875c0760f88e0a5494ae51b465e21f76d5917b746a59ea` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e1/timing/batches/timing.qwen3.8-27b.tier1.prompts.jsonl` | 32 | 1182376 | `4b5d1ca8c260b376f19ae264cb6235b4c84be37b9dd987e4056d8e0d2cb16044` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e1/timing/batches/timing.qwen3.8-27b.tier2.prompts.jsonl` | 32 | 1179968 | `783b78ce3e79361e9ce1a2011d5ad3f37250772f6fc83369854f85324691088c` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e1/timing/editor_log.jsonl` | 20 | 257768 | `f313518aad83c2ca9eaf23fbd08654f765704b3847c8fbbae148a02b2d62d8b4` | editor model requests and responses per edit attempt (page text) |
| cluster | `data/e1/timing/pages.jsonl` | 705 | 6029573 | `b4ad4a6d84b403dbb94a6501bc83567084aeaf23b827aba5130cbc3938afb65a` | normalized pages used by the experiment (page text, roles target/other) |
| cluster | `data/e1/timing/prompt_build.json` | 12 | 228 | `70f4b24d38a3cfc9d9f7e9e3c24cffd5dac4770deef4606176431f3657cee1a8` | prompt counts per batch and the token-limit refusals |
| cluster | `data/e1/timing/prompts.jsonl` | 128 | 4722256 | `8046a291b617b23ee036e080031cf856c4273cfd4001e2b8fc78d25a7831db06` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e1/timing/versions.jsonl` | 14 | 137156 | `9bf3d07bac71670aec7ba3991582fdc6baa15fa27207c3491afb0e21c961175f` | edited page versions per arm with validity flags and validator messages (page text) |
| cluster | `data/e1/timing2/applicability.jsonl` | 2115 | 196157 | `1f17fb793294c029da02514f232318cf537d4afb454319f7524930cd9c7fda77` | frozen per-query, per-arm applicability table (which checks flag something) |
| cluster | `data/e1/timing2/editor_log.jsonl` | 20 | 291595 | `305a70c2aae4648c8d16074a35b1fab0c9d5ae87aee9b39c9fb50347da756e75` | editor model requests and responses per edit attempt (page text) |
| cluster | `data/e1/timing2/pages.jsonl` | 705 | 6029573 | `b4ad4a6d84b403dbb94a6501bc83567084aeaf23b827aba5130cbc3938afb65a` | normalized pages used by the experiment (page text, roles target/other) |
| cluster | `data/e1/timing2/versions.jsonl` | 15 | 147228 | `a7cff6b4f9d7c7789d7d2d1e71b57fe2af9f5847b0ac1332edf957a5ae5309bd` | edited page versions per arm with validity flags and validator messages (page text) |
| cluster | `data/e1/timing3/applicability.jsonl` | 2115 | 196157 | `1f17fb793294c029da02514f232318cf537d4afb454319f7524930cd9c7fda77` | frozen per-query, per-arm applicability table (which checks flag something) |
| cluster | `data/e1/timing3/editor_log.jsonl` | 20 | 291372 | `a92723ae0b11ca24e5ad5bb9e955de23394d3232eff6fe5ca616fbdaaffdacc1` | editor model requests and responses per edit attempt (page text) |
| cluster | `data/e1/timing3/pages.jsonl` | 705 | 6029573 | `b4ad4a6d84b403dbb94a6501bc83567084aeaf23b827aba5130cbc3938afb65a` | normalized pages used by the experiment (page text, roles target/other) |
| cluster | `data/e1/timing3/versions.jsonl` | 15 | 147035 | `f223baab4a0474583a2c3ed61f0e5460a584db124b301008ca796369553c2267` | edited page versions per arm with validity flags and validator messages (page text) |
| cluster | `e1/answers/timing.gemma-4-12b.tierall.jsonl` | 64 | 151080 | `813f6cdf70e3b95fd5891832b83163ebc7c400ce0ef53b1e982b66e108c2710a` | raw judge answers for one batch (raw model answers) |
| cluster | `e1/answers/timing.qwen3.8-27b.tierall.jsonl` | 64 | 142454 | `2bd5271d9ff8664b77b08e1a1fc18c3bc0442dd003575e815b0d092332e6bb58` | raw judge answers for one batch (raw model answers) |
| cluster | `e1/batches/timing.gemma-4-12b.tierall.prompts.jsonl` | 64 | 2362664 | `11b410be7401091982ecf5e3b8dc54b5f0a6607fabf4db30462ea0ae54900bc5` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e1/batches/timing.qwen3.8-27b.tierall.prompts.jsonl` | 64 | 2362344 | `d7636f7d577b16228ae19dfa9b1d60bee5c5f01fa511cc9bb59e9edad20f224a` | judge prompts, one per (version, judge, seed); they hold the full page text |

## e2

| location | path | lines | bytes | sha256 | what it is |
|---|---|---|---|---|---|
| cluster | `data/e2/a/applicability.jsonl` | 2115 | 196157 | `1f17fb793294c029da02514f232318cf537d4afb454319f7524930cd9c7fda77` | frozen per-query, per-arm applicability table (which checks flag something) |
| cluster | `data/e2/a/batches/main.gemma-4-12b.tier1.prompts.jsonl` | 864 | 32097792 | `7e7b89b1fc75a8ccdb3e5608d76fea33410874b3c399653d30da717c7ffa9f18` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e2/a/batches/main.qwen3.8-27b.tier1.prompts.jsonl` | 864 | 32093472 | `2df9dee8c244bfe43761cb24a78ca6580d3c706d7506512be381647bfeb432a7` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e2/a/batches/replication.gemma-4-12b.tier1.prompts.jsonl` | 832 | 28572552 | `e9772568e7165924230cae843070977b880e7ffdccb215aadeed9f98e76a3c7b` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e2/a/batches/replication.qwen3.8-27b.tier1.prompts.jsonl` | 832 | 28568392 | `b40bd4edc9f42320cebcd14145b3d1f5ab028688c2e24ac63db01d6ca8bcb0ec` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e2/a/pages.jsonl` | 705 | 6029573 | `b4ad4a6d84b403dbb94a6501bc83567084aeaf23b827aba5130cbc3938afb65a` | normalized pages used by the experiment (page text, roles target/other) |
| cluster | `data/e2/a/prompt_build.json` | 17 | 316 | `97d309543fd354916e7db292947c693379a43cb216c1b4dc74c212c5169ad768` | prompt counts per batch and the token-limit refusals |
| cluster | `data/e2/a/prompts.jsonl` | 3392 | 121259280 | `d94a8c9430edfcc1941b67e94b0708b93954934c6e5ef7a80e2edb07cd1d068c` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e2/a/versions.jsonl` | 212 | 1872524 | `172aee2ed5471cccf43a95437ada30d5b65740d2403889c8ff019992354becf7` | edited page versions per arm with validity flags and validator messages (page text) |
| cluster | `data/e2/b/applicability.jsonl` | 2115 | 196157 | `1f17fb793294c029da02514f232318cf537d4afb454319f7524930cd9c7fda77` | frozen per-query, per-arm applicability table (which checks flag something) |
| cluster | `data/e2/b/batches/main.gemma-4-12b.tier1.prompts.jsonl` | 968 | 35322176 | `491771d26fc589d741080b6e78420b6b1abb58cbac912a20daadcfd41295df80` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e2/b/batches/main.gemma-4-12b.tier2.prompts.jsonl` | 624 | 22465280 | `64939c2310fc66ba1543fd7e566bd976fa6e776e6328715c147ee3869c2d96ab` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e2/b/batches/main.qwen3.5-9b.tier1.prompts.jsonl` | 1608 | 58210424 | `29605688f027c620c4909313c39f58bdf70c0732e86737572e2804437e85231b` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e2/b/batches/main.qwen3.5-9b.tier2.prompts.jsonl` | 624 | 22460912 | `ee685ded180f0064c6edea7c66a7a4814b5037fe8dfd0cf393f978616a86a3a0` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e2/b/editor_log.jsonl` | 762 | 10016849 | `2875d995b6e21848508250434488e93b22c08c39a673fdb216865885dfe7a3af` | editor model requests and responses per edit attempt (page text) |
| cluster | `data/e2/b/pages.jsonl` | 705 | 6029573 | `b4ad4a6d84b403dbb94a6501bc83567084aeaf23b827aba5130cbc3938afb65a` | normalized pages used by the experiment (page text, roles target/other) |
| cluster | `data/e2/b/prompt_build.json` | 12 | 225 | `b964ef93720636328e71d0b79a82156bd0239cfb4583fd114d843284af62b0f1` | prompt counts per batch and the token-limit refusals |
| cluster | `data/e2/b/prompts.jsonl` | 4464 | 161273808 | `6ee4541b09be2be609e51b75c250b0b33b252af5382e8cc4aa6e42fc7d8ab651` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e2/b/reuse.json` | 19 | 262 | `cd4d4f91455aa19c6ce029e50d58f7751cda0578ae0dd6c78bc27632b8499441` | which answers were reused from E1 for byte-identical prompts |
| cluster | `data/e2/b/versions.jsonl` | 342 | 2690794 | `5a904636576d0433479957c6d838156385fa2c8192cb9c09b03fb83a9e9fa96d` | edited page versions per arm with validity flags and validator messages (page text) |
| cluster | `e2/a/answers/main.gemma-4-12b.tier1.jsonl` | 864 | 1650442 | `fd95b15bf719bb897c877f115020a08e7a6418e2770375cfa159da69c61906a4` | raw judge answers for one batch (raw model answers) |
| cluster | `e2/a/answers/main.qwen3.8-27b.tier1.jsonl` | 864 | 1536191 | `f679f6f9fbb33d5a79a40b08a88d660a54fe4a7ed58bd8166d2b4787e92b2f4b` | raw judge answers for one batch (raw model answers) |
| cluster | `e2/a/answers/replication.gemma-4-12b.tier1.jsonl` | 832 | 1068195 | `e715991ea12fb3da7e1b95a787a4ee9015329dceaf15a948cd9384a26edd33eb` | raw judge answers for one batch (raw model answers) |
| cluster | `e2/a/answers/replication.qwen3.8-27b.tier1.jsonl` | 832 | 1024063 | `5603e6ed05b40ff8311d1e8e597bc0994ebd9a463ab8937e05c423ad6c40b2cd` | raw judge answers for one batch (raw model answers) |
| cluster | `e2/a/batches/main.gemma-4-12b.tier1.prompts.jsonl` | 864 | 32097792 | `7e7b89b1fc75a8ccdb3e5608d76fea33410874b3c399653d30da717c7ffa9f18` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e2/a/batches/main.qwen3.8-27b.tier1.prompts.jsonl` | 864 | 32093472 | `2df9dee8c244bfe43761cb24a78ca6580d3c706d7506512be381647bfeb432a7` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e2/a/batches/replication.gemma-4-12b.tier1.prompts.jsonl` | 832 | 28572552 | `e9772568e7165924230cae843070977b880e7ffdccb215aadeed9f98e76a3c7b` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e2/a/batches/replication.qwen3.8-27b.tier1.prompts.jsonl` | 832 | 28568392 | `b40bd4edc9f42320cebcd14145b3d1f5ab028688c2e24ac63db01d6ca8bcb0ec` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e2/b/answers/main.gemma-4-12b.tier1.jsonl` | 968 | 1714858 | `a57a2fae93b21be42d86e1977e21dc0450030eb05d6efbdc323d08e6b03910f7` | raw judge answers for one batch (raw model answers) |
| cluster | `e2/b/answers/main.gemma-4-12b.tier2.jsonl` | 624 | 1080130 | `cc0c84181163502d3919c9a187d5cfe58e0b851b2f0c3424cb1e6093af435d6f` | raw judge answers for one batch (raw model answers) |
| cluster | `e2/b/answers/main.qwen3.5-9b.tier1.jsonl` | 1608 | 2511113 | `ece00c7c111a32d55b17e294691d1083a8d6a5ee6d59adb7864456c8ce524180` | raw judge answers for one batch (raw model answers) |
| cluster | `e2/b/answers/main.qwen3.5-9b.tier2.jsonl` | 624 | 967631 | `0b9292ce991a573efcc347b9a81b6ec4c68557554f5eb7782f4ea5af244d9626` | raw judge answers for one batch (raw model answers) |
| cluster | `e2/b/answers/reused-e1.gemma-4-12b.jsonl` | 640 | 1141319 | `8088a0e43b1dd235287be9a76ab214151df36e5d4d0502c917645b1aecd69826` | E1 answers reused for byte-identical prompts (raw model answers) |
| cluster | `e2/b/batches/main.gemma-4-12b.tier1.prompts.jsonl` | 968 | 35322176 | `491771d26fc589d741080b6e78420b6b1abb58cbac912a20daadcfd41295df80` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e2/b/batches/main.gemma-4-12b.tier2.prompts.jsonl` | 624 | 22465280 | `64939c2310fc66ba1543fd7e566bd976fa6e776e6328715c147ee3869c2d96ab` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e2/b/batches/main.qwen3.5-9b.tier1.prompts.jsonl` | 1608 | 58210424 | `29605688f027c620c4909313c39f58bdf70c0732e86737572e2804437e85231b` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e2/b/batches/main.qwen3.5-9b.tier2.prompts.jsonl` | 624 | 22460912 | `ee685ded180f0064c6edea7c66a7a4814b5037fe8dfd0cf393f978616a86a3a0` | judge prompts, one per (version, judge, seed); they hold the full page text |
| local | `e2/data/answers/main.gemma-4-12b.tier1.jsonl` | 864 | 1650442 | `fd95b15bf719bb897c877f115020a08e7a6418e2770375cfa159da69c61906a4` | raw judge answers for one batch (raw model answers) |
| local | `e2/data/answers/main.qwen3.8-27b.tier1.jsonl` | 864 | 1536191 | `f679f6f9fbb33d5a79a40b08a88d660a54fe4a7ed58bd8166d2b4787e92b2f4b` | raw judge answers for one batch (raw model answers) |
| local | `e2/data/answers/replication.gemma-4-12b.tier1.jsonl` | 832 | 1068195 | `e715991ea12fb3da7e1b95a787a4ee9015329dceaf15a948cd9384a26edd33eb` | raw judge answers for one batch (raw model answers) |
| local | `e2/data/answers/replication.qwen3.8-27b.tier1.jsonl` | 832 | 1024063 | `5603e6ed05b40ff8311d1e8e597bc0994ebd9a463ab8937e05c423ad6c40b2cd` | raw judge answers for one batch (raw model answers) |
| local | `e2/data/applicability.jsonl` | 2115 | 196157 | `1f17fb793294c029da02514f232318cf537d4afb454319f7524930cd9c7fda77` | frozen per-query, per-arm applicability table (which checks flag something) |
| local | `e2/data/b/answers/main.gemma-4-12b.tier1.jsonl` | 968 | 1714858 | `a57a2fae93b21be42d86e1977e21dc0450030eb05d6efbdc323d08e6b03910f7` | raw judge answers for one batch (raw model answers) |
| local | `e2/data/b/answers/main.gemma-4-12b.tier2.jsonl` | 624 | 1080130 | `cc0c84181163502d3919c9a187d5cfe58e0b851b2f0c3424cb1e6093af435d6f` | raw judge answers for one batch (raw model answers) |
| local | `e2/data/b/answers/main.qwen3.5-9b.tier1.jsonl` | 1608 | 2511113 | `ece00c7c111a32d55b17e294691d1083a8d6a5ee6d59adb7864456c8ce524180` | raw judge answers for one batch (raw model answers) |
| local | `e2/data/b/answers/main.qwen3.5-9b.tier2.jsonl` | 624 | 967631 | `0b9292ce991a573efcc347b9a81b6ec4c68557554f5eb7782f4ea5af244d9626` | raw judge answers for one batch (raw model answers) |
| local | `e2/data/b/answers/reused-e1.gemma-4-12b.jsonl` | 640 | 1141319 | `8088a0e43b1dd235287be9a76ab214151df36e5d4d0502c917645b1aecd69826` | E1 answers reused for byte-identical prompts (raw model answers) |
| local | `e2/data/b/applicability.jsonl` | 2115 | 196157 | `1f17fb793294c029da02514f232318cf537d4afb454319f7524930cd9c7fda77` | frozen per-query, per-arm applicability table (which checks flag something) |
| local | `e2/data/b/pages.jsonl` | 705 | 6029573 | `b4ad4a6d84b403dbb94a6501bc83567084aeaf23b827aba5130cbc3938afb65a` | normalized pages used by the experiment (page text, roles target/other) |
| local | `e2/data/b/prompt_build.json` | 12 | 225 | `b964ef93720636328e71d0b79a82156bd0239cfb4583fd114d843284af62b0f1` | prompt counts per batch and the token-limit refusals |
| local | `e2/data/b/prompts.jsonl` | 4464 | 161273808 | `6ee4541b09be2be609e51b75c250b0b33b252af5382e8cc4aa6e42fc7d8ab651` | judge prompts, one per (version, judge, seed); they hold the full page text |
| local | `e2/data/b/reuse.json` | 19 | 262 | `cd4d4f91455aa19c6ce029e50d58f7751cda0578ae0dd6c78bc27632b8499441` | which answers were reused from E1 for byte-identical prompts |
| local | `e2/data/b/versions.jsonl` | 342 | 2690794 | `5a904636576d0433479957c6d838156385fa2c8192cb9c09b03fb83a9e9fa96d` | edited page versions per arm with validity flags and validator messages (page text) |
| local | `e2/data/make_versions.json` | 33 | 437 | `dce5b054e476115126b9c5d5a2c320d1318a54ec906975b6019fce86880a0aa9` | counts from E2a's 9W and 9P version builder |
| local | `e2/data/pages.jsonl` | 705 | 6029573 | `b4ad4a6d84b403dbb94a6501bc83567084aeaf23b827aba5130cbc3938afb65a` | normalized pages used by the experiment (page text, roles target/other) |
| local | `e2/data/prompt_build.json` | 17 | 316 | `97d309543fd354916e7db292947c693379a43cb216c1b4dc74c212c5169ad768` | prompt counts per batch and the token-limit refusals |
| local | `e2/data/prompts.jsonl` | 3392 | 121259280 | `d94a8c9430edfcc1941b67e94b0708b93954934c6e5ef7a80e2edb07cd1d068c` | judge prompts, one per (version, judge, seed); they hold the full page text |
| local | `e2/data/versions.jsonl` | 212 | 1872524 | `172aee2ed5471cccf43a95437ada30d5b65740d2403889c8ff019992354becf7` | edited page versions per arm with validity flags and validator messages (page text) |

## e2a

| location | path | lines | bytes | sha256 | what it is |
|---|---|---|---|---|---|
| cluster | `logs/ce-e2a-main.gemma-4-12b.tier1-11351366.err` | 8 | 115661 | `90c8f5a1b357dd566bf2de319c436126f655f07f115d3cd2737ce97ced12eccd` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e2a-main.gemma-4-12b.tier1-11351366.out` | 94 | 11475 | `0e66cf761e3400f7041773e442a04aeb958cebf12fdb546c27dedd26a1e1b2a8` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e2a-main.gemma-4-12b.tier1-11351366.out` | 94 | 11475 | `0e66cf761e3400f7041773e442a04aeb958cebf12fdb546c27dedd26a1e1b2a8` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e2a-main.qwen3.8-27b.tier1-11351368.err` | 24 | 107642 | `b9abd8da8e2befe30169db7f52a605fd3135d0cd9646ec942ad9d185b4c7854d` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e2a-main.qwen3.8-27b.tier1-11351368.out` | 92 | 14255 | `58c8609330d8138ced8dceab27ec38cd5d6b4cb74ad6018bdf86505292c57ad2` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e2a-main.qwen3.8-27b.tier1-11351368.out` | 92 | 14255 | `58c8609330d8138ced8dceab27ec38cd5d6b4cb74ad6018bdf86505292c57ad2` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e2a-replication.gemma-4-12b.tier1-11351367.err` | 8 | 105921 | `7efb66cc56b7487f689fae77ed3f2adb0813af525535981462c64cca9092cce3` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e2a-replication.gemma-4-12b.tier1-11351367.out` | 88 | 11388 | `0558076c0008eb97c436b1028c34383d42e74a4892876d91f55b8ff40d2c28d2` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e2a-replication.gemma-4-12b.tier1-11351367.out` | 88 | 11388 | `0558076c0008eb97c436b1028c34383d42e74a4892876d91f55b8ff40d2c28d2` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e2a-replication.qwen3.8-27b.tier1-11351369.err` | 24 | 99407 | `0d5ccf7615c337d4740193dbba6462f493490fdb35e7e50a587708df8cae013a` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e2a-replication.qwen3.8-27b.tier1-11351369.out` | 90 | 14300 | `16cd1b6c5962c1f7cc061737173eaf76eee4d7701c00e5a98d7bf891454aef4c` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e2a-replication.qwen3.8-27b.tier1-11351369.out` | 90 | 14300 | `16cd1b6c5962c1f7cc061737173eaf76eee4d7701c00e5a98d7bf891454aef4c` | job stdout; summary lines are in results/runs/logs/ |

## e2b

| location | path | lines | bytes | sha256 | what it is |
|---|---|---|---|---|---|
| cluster | `logs/ce-e2b-edit-11351370.err` | 64 | 79160 | `9cf5a9da0a5bca0ef6d2184cd6b274402a79a9ca2796ea64635f1e8f9f0ec99a` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e2b-edit-11351370.out` | 122 | 14505 | `04489b30b650ff8d95054ba2f543b657f120fe5b7ff75067a787dd3d42415721` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e2b-edit-11351370.out` | 122 | 14505 | `04489b30b650ff8d95054ba2f543b657f120fe5b7ff75067a787dd3d42415721` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e2b-main.gemma-4-12b.tier1-11352310.err` | 7 | 103681 | `f3ea7d5c996134ac27c1ee9b64bc9f063260b7077b61b2c74dfb0c93d3a948dc` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e2b-main.gemma-4-12b.tier1-11352310.out` | 69 | 11053 | `be7386e103078486f5579f3bb6fefff88830d33211920b192e9d17cdf093d845` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e2b-main.gemma-4-12b.tier1-11352310.out` | 69 | 11053 | `be7386e103078486f5579f3bb6fefff88830d33211920b192e9d17cdf093d845` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e2b-main.gemma-4-12b.tier2-11352311.err` | 7 | 67171 | `8a25805de72adb061d21892b796d79c3ad5d9fd6ecf0035f3c9cc96841e25fa9` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e2b-main.gemma-4-12b.tier2-11352311.out` | 65 | 10968 | `eec4df1496526b616b9ca5ce30880558f5b8b93889d32d2e1aa23537c2c1a365` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e2b-main.gemma-4-12b.tier2-11352311.out` | 65 | 10968 | `eec4df1496526b616b9ca5ce30880558f5b8b93889d32d2e1aa23537c2c1a365` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e2b-main.qwen3.5-9b.tier1-11352316.err` | 13 | 214051 | `591c83e095199c4622b8d7e0e4bad44c6d6d70f0efd17d0891176dc95dbd0d70` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e2b-main.qwen3.5-9b.tier1-11352316.out` | 103 | 13850 | `cfbe2711d3f4a93d850b0321d47c2028f16a89a03e23e21679fd3d458bb271d3` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e2b-main.qwen3.5-9b.tier1-11352316.out` | 103 | 13850 | `cfbe2711d3f4a93d850b0321d47c2028f16a89a03e23e21679fd3d458bb271d3` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e2b-main.qwen3.5-9b.tier2-11352318.err` | 11 | 63116 | `947a0a24827e1ab21b681e9828cfa635b521cf6a99317f73217296a53d157339` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e2b-main.qwen3.5-9b.tier2-11352318.out` | 82 | 13724 | `507b6c50cd52817b2a141a26309eb076367be518ab781858a4d27304e0a2bb35` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e2b-main.qwen3.5-9b.tier2-11352318.out` | 82 | 13724 | `507b6c50cd52817b2a141a26309eb076367be518ab781858a4d27304e0a2bb35` | job stdout; summary lines are in results/runs/logs/ |

## e3

| location | path | lines | bytes | sha256 | what it is |
|---|---|---|---|---|---|
| cluster | `data/e3/new/applicability.jsonl` | 2700 | 306392 | `1c53da001cdc8a418329e48520809dfa6ea92a08092f8192646a7d8e9c616bba` | frozen per-query, per-arm applicability table (which checks flag something) |
| cluster | `data/e3/new/batches/e3-four.gemma-4-12b.tier1.prompts.jsonl` | 864 | 28762808 | `8ca327945a50df6acba5545e3c4e8a647dc7d597d77d79bf8e523bae5a39f179` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e3/new/batches/e3-four.gemma-4-12b.tier2.prompts.jsonl` | 976 | 32478880 | `c487f9544ecfbefd348f6bde7c7a905b2295850f15669d0a15f108acf51d78b3` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e3/new/batches/e3-four.gemma-4-12b.tier3.prompts.jsonl` | 104 | 3307304 | `ab2cfe6f845900a7dd53858fdd3f2dcd88e58aa8d7bb8d0f253c6c53a29dfcce` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e3/new/batches/e3-four.qwen3.8-27b.tier1.prompts.jsonl` | 864 | 28758488 | `065fd2053532fac28bb04bf89ab5ddcf5497525582a9cca962ccc9de5408e77e` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e3/new/batches/e3-four.qwen3.8-27b.tier2.prompts.jsonl` | 976 | 32474000 | `a803dd58582ad5215a65be9a7f0bb8ae1c877dc0b2a017f9938ba1b68c5956d0` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e3/new/batches/e3-four.qwen3.8-27b.tier3.prompts.jsonl` | 104 | 3306784 | `d968a591974db23b22a8a02130af56adcd0807de61594fb058208ef6f220fcd6` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e3/new/batches/e3.gemma-4-12b.tier1.prompts.jsonl` | 1768 | 64127472 | `654c7fe81e8e0e3f04b46de0222877349c3bf77dcc313370eb190764f1ca3d43` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e3/new/batches/e3.gemma-4-12b.tier2.prompts.jsonl` | 808 | 28285568 | `5c0c931c966a9ab02bd778d5648f3307409001e1c645abdc6d92eb27f9aa300f` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e3/new/batches/e3.gemma-4-12b.tier3.prompts.jsonl` | 256 | 9175232 | `9d7a4effba2bd40a64b6f178ece5b518f305e67dbc5bc13fad75a816e0834c9f` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e3/new/batches/e3.qwen3.8-27b.tier1.prompts.jsonl` | 1768 | 64118632 | `0d3909fa3a0109799f0717cb1f3a79e62d52b73ad3d6d68413fb49fc48001624` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e3/new/batches/e3.qwen3.8-27b.tier2.prompts.jsonl` | 808 | 28281528 | `cf2a6904581ae0d75dbfc2d572ccb7bc8bda30b14a075df6f52b654716407ddd` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e3/new/batches/e3.qwen3.8-27b.tier3.prompts.jsonl` | 256 | 9173952 | `35a80faa685127060cccfa31ceff50698988d69354a98465f9de8c927c482bfb` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e3/new/editor_log.jsonl` | 1210 | 16392986 | `c9afa7773557166358b2de33a379775ccec8930bc12c9008bc513808c38ec3e4` | editor model requests and responses per edit attempt (page text) |
| cluster | `data/e3/new/pages.jsonl` | 792 | 6835263 | `82c9bb56e2d2aaec25a13b8c7131534ea840cb60f4e3f9b5b39b6036b2d7794f` | normalized pages used by the experiment (page text, roles target/other) |
| cluster | `data/e3/new/prompt_build.json` | 20 | 497 | `982b7fa48ad899aece5a1323b970479535849b0b0148614786dedfa14876b601` | prompt counts per batch and the token-limit refusals |
| cluster | `data/e3/new/prompts.jsonl` | 9552 | 332059184 | `0dba2fde587fa5d3eaa5117a02296e60d38d752708cc9b634a202ff44fa86796` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e3/new/reuse.json` | 186 | 3763 | `3efece128f4d94ddf35c38934bb6ff0415c749b3f2dff0145e800a8470f879db` | which answers were reused from E1 for byte-identical prompts |
| cluster | `data/e3/new/versions.jsonl` | 863 | 7867474 | `dd7a6be80fb8aa12ac99ff3edff3587d52fc424ae654fdbe6c5839eac98d69c7` | edited page versions per arm with validity flags and validator messages (page text) |
| cluster | `data/e3/retry/applicability.jsonl` | 2115 | 196157 | `1f17fb793294c029da02514f232318cf537d4afb454319f7524930cd9c7fda77` | frozen per-query, per-arm applicability table (which checks flag something) |
| cluster | `data/e3/retry/batches/main.gemma-4-12b.tier1.prompts.jsonl` | 8 | 236704 | `7f9e0705a10532c22f9b023e70a6ab8b6ccf05414f8d8aec9a42c98a81618a49` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e3/retry/batches/main.gemma-4-12b.tier2.prompts.jsonl` | 8 | 332312 | `b7e810dd6f7c735846e97982827f9c168abb33361e2dcaaf45dd280bf2e4d4bd` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e3/retry/batches/main.gemma-4-12b.tier3.prompts.jsonl` | 32 | 1148432 | `3b463e6a5c15726e144571641dbd830d1a12a924b876cb673ec1cf4f59665fa9` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e3/retry/batches/main.qwen3.8-27b.tier1.prompts.jsonl` | 8 | 236664 | `a409cfaf7998e4b6365163dcc1fc6dfdd6b065cbefef592db816191a1ae3eecb` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e3/retry/batches/main.qwen3.8-27b.tier2.prompts.jsonl` | 8 | 332272 | `f9339329037fc3a53e92e17804dbf252086d3fdfc62adc48e4b1085a5d0c5d45` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e3/retry/batches/main.qwen3.8-27b.tier3.prompts.jsonl` | 32 | 1148272 | `80e0a8b7ea904741810eda41ca84e25848a8583dc94ca1659494ddd1d3d8b774` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e3/retry/editor_log.jsonl` | 136 | 1812736 | `dc311fe020589f98d74981b12374ff105034cfe6ad12bb12a85758a96513efb8` | editor model requests and responses per edit attempt (page text) |
| cluster | `data/e3/retry/pages.jsonl` | 705 | 6029573 | `b4ad4a6d84b403dbb94a6501bc83567084aeaf23b827aba5130cbc3938afb65a` | normalized pages used by the experiment (page text, roles target/other) |
| cluster | `data/e3/retry/prompt_build.json` | 19 | 356 | `47cb7c171b9b41c99b06332f7858efdae2a3a5c214898ad7ce028b5b71a413ba` | prompt counts per batch and the token-limit refusals |
| cluster | `data/e3/retry/prompts.jsonl` | 96 | 3432512 | `9ff03c68cbdd25f1a57c67c7293767af868e1a23cd49ff5b6e8081752bd0370d` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `data/e3/retry/reuse.json` | 140 | 2897 | `b79d010ae54ac8c863c28f611ce78d70638638c0402c929871b02f51bf706f69` | which answers were reused from E1 for byte-identical prompts |
| cluster | `data/e3/retry/versions.jsonl` | 138 | 1121177 | `8d726a30807e20140925f73fc2654116ff74afc25a05d9371f5a90f69d49461d` | edited page versions per arm with validity flags and validator messages (page text) |
| cluster | `e3/new/answers/e3-four.gemma-4-12b.tierall.jsonl` | 1944 | 3389905 | `250d333792a32bc121a6b5903384de3b8f482d96ff7b5bddfff97c5c5a39e82c` | raw judge answers for one batch (raw model answers) |
| cluster | `e3/new/answers/e3-four.qwen3.8-27b.tierall.jsonl` | 1944 | 3093561 | `6110fd036707d0e1c0a06c87dd3a655dbb2bb033dd1ed13fc84816640e6d8fc6` | raw judge answers for one batch (raw model answers) |
| cluster | `e3/new/answers/e3.gemma-4-12b.tierall.jsonl` | 2832 | 5867424 | `8eedc90acd7f7fdf6e1c650cd14c16de4822f57f6fe366de934e3c4aea953097` | raw judge answers for one batch (raw model answers) |
| cluster | `e3/new/answers/e3.qwen3.8-27b.tierall.jsonl` | 2832 | 5080707 | `c841e1cc5943b584ddc26ce79ac9d81cebf3be7ee57eedd5e9283b6f7a001511` | raw judge answers for one batch (raw model answers) |
| cluster | `e3/new/answers/reused-e1.gemma-4-12b.jsonl` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | E1 answers reused for byte-identical prompts (raw model answers) |
| cluster | `e3/new/answers/reused-e1.qwen3.8-27b.jsonl` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | E1 answers reused for byte-identical prompts (raw model answers) |
| cluster | `e3/new/batches/e3-four.gemma-4-12b.tier1.prompts.jsonl` | 864 | 28762808 | `8ca327945a50df6acba5545e3c4e8a647dc7d597d77d79bf8e523bae5a39f179` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e3/new/batches/e3-four.gemma-4-12b.tier2.prompts.jsonl` | 976 | 32478880 | `c487f9544ecfbefd348f6bde7c7a905b2295850f15669d0a15f108acf51d78b3` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e3/new/batches/e3-four.gemma-4-12b.tier3.prompts.jsonl` | 104 | 3307304 | `ab2cfe6f845900a7dd53858fdd3f2dcd88e58aa8d7bb8d0f253c6c53a29dfcce` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e3/new/batches/e3-four.gemma-4-12b.tierall.prompts.jsonl` | 1944 | 64548992 | `14d5b0740c11e95ec2b20c07aeec418e8a83f7a670519e6d579daddd51bcf0cb` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e3/new/batches/e3-four.qwen3.8-27b.tier1.prompts.jsonl` | 864 | 28758488 | `065fd2053532fac28bb04bf89ab5ddcf5497525582a9cca962ccc9de5408e77e` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e3/new/batches/e3-four.qwen3.8-27b.tier2.prompts.jsonl` | 976 | 32474000 | `a803dd58582ad5215a65be9a7f0bb8ae1c877dc0b2a017f9938ba1b68c5956d0` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e3/new/batches/e3-four.qwen3.8-27b.tier3.prompts.jsonl` | 104 | 3306784 | `d968a591974db23b22a8a02130af56adcd0807de61594fb058208ef6f220fcd6` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e3/new/batches/e3-four.qwen3.8-27b.tierall.prompts.jsonl` | 1944 | 64539272 | `25c96ab092429bd9fe2401ece0162cf636bd3de857fffee67a7fc6fb42829504` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e3/new/batches/e3.gemma-4-12b.tier1.prompts.jsonl` | 1768 | 64127472 | `654c7fe81e8e0e3f04b46de0222877349c3bf77dcc313370eb190764f1ca3d43` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e3/new/batches/e3.gemma-4-12b.tier2.prompts.jsonl` | 808 | 28285568 | `5c0c931c966a9ab02bd778d5648f3307409001e1c645abdc6d92eb27f9aa300f` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e3/new/batches/e3.gemma-4-12b.tier3.prompts.jsonl` | 256 | 9175232 | `9d7a4effba2bd40a64b6f178ece5b518f305e67dbc5bc13fad75a816e0834c9f` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e3/new/batches/e3.gemma-4-12b.tierall.prompts.jsonl` | 2832 | 101588272 | `77c1199e802c1c981b62899f2f710eb79f1b5198405e8bb072bada503a931ca8` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e3/new/batches/e3.qwen3.8-27b.tier1.prompts.jsonl` | 1768 | 64118632 | `0d3909fa3a0109799f0717cb1f3a79e62d52b73ad3d6d68413fb49fc48001624` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e3/new/batches/e3.qwen3.8-27b.tier2.prompts.jsonl` | 808 | 28281528 | `cf2a6904581ae0d75dbfc2d572ccb7bc8bda30b14a075df6f52b654716407ddd` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e3/new/batches/e3.qwen3.8-27b.tier3.prompts.jsonl` | 256 | 9173952 | `35a80faa685127060cccfa31ceff50698988d69354a98465f9de8c927c482bfb` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e3/new/batches/e3.qwen3.8-27b.tierall.prompts.jsonl` | 2832 | 101574112 | `8e43678ab87cda2a1a1b415517ac69cf5ad60365088edbe347e2603915ac7c92` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e3/retry/answers/main.gemma-4-12b.tierall.jsonl` | 48 | 95364 | `3e055112563aea81eb9c10f093a0a6469226e67cad84b8fc9bf8d5ea0dd4c088` | raw judge answers for one batch (raw model answers) |
| cluster | `e3/retry/answers/main.qwen3.8-27b.tierall.jsonl` | 48 | 92657 | `95a9bdcbbaaf20a3dfbc03854bd7dd7494469abfd60a9879a4a00fd2ecfe84fa` | raw judge answers for one batch (raw model answers) |
| cluster | `e3/retry/answers/reused-e1.gemma-4-12b.jsonl` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | E1 answers reused for byte-identical prompts (raw model answers) |
| cluster | `e3/retry/answers/reused-e1.qwen3.8-27b.jsonl` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | E1 answers reused for byte-identical prompts (raw model answers) |
| cluster | `e3/retry/batches/main.gemma-4-12b.tier1.prompts.jsonl` | 8 | 236704 | `7f9e0705a10532c22f9b023e70a6ab8b6ccf05414f8d8aec9a42c98a81618a49` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e3/retry/batches/main.gemma-4-12b.tier2.prompts.jsonl` | 8 | 332312 | `b7e810dd6f7c735846e97982827f9c168abb33361e2dcaaf45dd280bf2e4d4bd` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e3/retry/batches/main.gemma-4-12b.tier3.prompts.jsonl` | 32 | 1148432 | `3b463e6a5c15726e144571641dbd830d1a12a924b876cb673ec1cf4f59665fa9` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e3/retry/batches/main.gemma-4-12b.tierall.prompts.jsonl` | 48 | 1717448 | `0bc14edfe3278495c1345ac7a5c5c2677062a53a3017566a68381c3b9561c21b` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e3/retry/batches/main.qwen3.8-27b.tier1.prompts.jsonl` | 8 | 236664 | `a409cfaf7998e4b6365163dcc1fc6dfdd6b065cbefef592db816191a1ae3eecb` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e3/retry/batches/main.qwen3.8-27b.tier2.prompts.jsonl` | 8 | 332272 | `f9339329037fc3a53e92e17804dbf252086d3fdfc62adc48e4b1085a5d0c5d45` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e3/retry/batches/main.qwen3.8-27b.tier3.prompts.jsonl` | 32 | 1148272 | `80e0a8b7ea904741810eda41ca84e25848a8583dc94ca1659494ddd1d3d8b774` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `e3/retry/batches/main.qwen3.8-27b.tierall.prompts.jsonl` | 48 | 1717208 | `9864ff762f8a2a62c8c83077cfd3d906d41aa1512be979e12361a5e27daa02ce` | judge prompts, one per (version, judge, seed); they hold the full page text |
| cluster | `logs/ce-e3-e3-four.gemma-4-12b.tierall-11354085.err` | 8 | 257277 | `710008ca15dbab6947826f584d387fe625be2db39a0d59c38d00a2d91e11ee00` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e3-e3-four.gemma-4-12b.tierall-11354085.out` | 114 | 11865 | `8e5af2b077f6108c0e436e874e66b9ba116c79bb629cef0aa7a31a4522f41371` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e3-e3-four.gemma-4-12b.tierall-11354085.out` | 114 | 11865 | `8e5af2b077f6108c0e436e874e66b9ba116c79bb629cef0aa7a31a4522f41371` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e3-e3-four.qwen3.8-27b.tierall-11354088.err` | 24 | 234602 | `3175654c2689548ecdd5ffc3296127c918658b919009da025891166c6242c6d6` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e3-e3-four.qwen3.8-27b.tierall-11354088.out` | 98 | 14550 | `b2e8b8009aa791855461f46dd86683b3fc0e708644a27076ac8c31fa3f6009b9` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e3-e3-four.qwen3.8-27b.tierall-11354088.out` | 98 | 14550 | `b2e8b8009aa791855461f46dd86683b3fc0e708644a27076ac8c31fa3f6009b9` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e3-e3.gemma-4-12b.tierall-11354081.err` | 7 | 310628 | `a38ba1cc862bc78b17e16a45de3c644d8772a69350855f4bf96d75af9c710ecb` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e3-e3.gemma-4-12b.tierall-11354081.out` | 85 | 11396 | `87a3980e82033e7283504b63ccae8885db208f2c223a1e961f81f166da9d75fb` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e3-e3.gemma-4-12b.tierall-11354081.out` | 85 | 11396 | `87a3980e82033e7283504b63ccae8885db208f2c223a1e961f81f166da9d75fb` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e3-e3.qwen3.8-27b.tierall-11354087.err` | 24 | 345716 | `430bf9d9c7b783545a4ee5bd23486042bd69a40c6fe6514960443ef1c60277c7` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e3-e3.qwen3.8-27b.tierall-11354087.out` | 102 | 14637 | `646a95a404413a66163382b87d2921139ebc2401de8bc67d905feb7ea695b8cb` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e3-e3.qwen3.8-27b.tierall-11354087.out` | 102 | 14637 | `646a95a404413a66163382b87d2921139ebc2401de8bc67d905feb7ea695b8cb` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e3-edit-new-11353459.err` | 22 | 114247 | `4ff99a1a17f67b31e5f18db5527a00001415c38e5418ebfe9851dd0579f1959d` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e3-edit-new-11353459.out` | 171 | 12629 | `db29d653d13a3f5d7e129c768ad25ddecc7b28e49ed4c11c522b86f6fb555934` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e3-edit-new-11353459.out` | 171 | 12629 | `db29d653d13a3f5d7e129c768ad25ddecc7b28e49ed4c11c522b86f6fb555934` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e3-edit-retry-11353461.err` | 18 | 16250 | `a543eff170d76804c4a2f22bafcc7799d9a859447d8c3572270ebc0a1ff4ec92` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e3-edit-retry-11353461.out` | 199 | 13266 | `bbf64904d5632b3f557b39ce77c181d5207993b77eca0dc973765b663b68c33b` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e3-edit-retry-11353461.out` | 199 | 13266 | `bbf64904d5632b3f557b39ce77c181d5207993b77eca0dc973765b663b68c33b` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e3-main.gemma-4-12b.tierall-11354089.err` | 7 | 5512 | `7d13ede49494eaff71f2adae5767662f5c4ac957b6526b63f520bf9ef8b0f900` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e3-main.gemma-4-12b.tierall-11354089.out` | 63 | 10900 | `9999e58faff5f88babd019feb8b2c96611b992626f5fcad78f00c528401a528a` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e3-main.gemma-4-12b.tierall-11354089.out` | 63 | 10900 | `9999e58faff5f88babd019feb8b2c96611b992626f5fcad78f00c528401a528a` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e3-main.qwen3.8-27b.tierall-11354090.err` | 24 | 8509 | `845abd98ce477fa14e102518d416a7c15ab5fc4cc8a7b34f2311b73af46e1cc0` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-e3-main.qwen3.8-27b.tierall-11354090.out` | 82 | 14206 | `4a0137f0bd023fc7b4e7cb882217c9e7a6fe3bb55bb347f2884143ad3998ec5f` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-e3-main.qwen3.8-27b.tierall-11354090.out` | 82 | 14206 | `4a0137f0bd023fc7b4e7cb882217c9e7a6fe3bb55bb347f2884143ad3998ec5f` | job stdout; summary lines are in results/runs/logs/ |
| local | `e3/data/admission_e3.json` | 239 | 4086 | `41e6edc0e84091a841e4d8fa81056232a94ce1015c1cd074ba04d4b8f19bcd6b` | admitted query ids and set sizes |
| local | `e3/data/answers/e3-four.gemma-4-12b.tierall.jsonl` | 1944 | 3389905 | `250d333792a32bc121a6b5903384de3b8f482d96ff7b5bddfff97c5c5a39e82c` | raw judge answers for one batch (raw model answers) |
| local | `e3/data/answers/e3-four.qwen3.8-27b.tierall.jsonl` | 1944 | 3093561 | `6110fd036707d0e1c0a06c87dd3a655dbb2bb033dd1ed13fc84816640e6d8fc6` | raw judge answers for one batch (raw model answers) |
| local | `e3/data/answers/e3.gemma-4-12b.tierall.jsonl` | 2832 | 5867424 | `8eedc90acd7f7fdf6e1c650cd14c16de4822f57f6fe366de934e3c4aea953097` | raw judge answers for one batch (raw model answers) |
| local | `e3/data/answers/e3.qwen3.8-27b.tierall.jsonl` | 2832 | 5080707 | `c841e1cc5943b584ddc26ce79ac9d81cebf3be7ee57eedd5e9283b6f7a001511` | raw judge answers for one batch (raw model answers) |
| local | `e3/data/applicability.jsonl` | 2700 | 306392 | `1c53da001cdc8a418329e48520809dfa6ea92a08092f8192646a7d8e9c616bba` | frozen per-query, per-arm applicability table (which checks flag something) |
| local | `e3/data/pages.jsonl` | 792 | 6835263 | `82c9bb56e2d2aaec25a13b8c7131534ea840cb60f4e3f9b5b39b6036b2d7794f` | normalized pages used by the experiment (page text, roles target/other) |
| local | `e3/data/prompt_build.json` | 20 | 497 | `982b7fa48ad899aece5a1323b970479535849b0b0148614786dedfa14876b601` | prompt counts per batch and the token-limit refusals |
| local | `e3/data/prompts.jsonl` | 9552 | 332059184 | `0dba2fde587fa5d3eaa5117a02296e60d38d752708cc9b634a202ff44fa86796` | judge prompts, one per (version, judge, seed); they hold the full page text |
| local | `e3/data/retry/answers/main.gemma-4-12b.tierall.jsonl` | 48 | 95364 | `3e055112563aea81eb9c10f093a0a6469226e67cad84b8fc9bf8d5ea0dd4c088` | raw judge answers for one batch (raw model answers) |
| local | `e3/data/retry/answers/main.qwen3.8-27b.tierall.jsonl` | 48 | 92657 | `95a9bdcbbaaf20a3dfbc03854bd7dd7494469abfd60a9879a4a00fd2ecfe84fa` | raw judge answers for one batch (raw model answers) |
| local | `e3/data/retry/applicability.jsonl` | 2115 | 196157 | `1f17fb793294c029da02514f232318cf537d4afb454319f7524930cd9c7fda77` | frozen per-query, per-arm applicability table (which checks flag something) |
| local | `e3/data/retry/pages.jsonl` | 705 | 6029573 | `b4ad4a6d84b403dbb94a6501bc83567084aeaf23b827aba5130cbc3938afb65a` | normalized pages used by the experiment (page text, roles target/other) |
| local | `e3/data/retry/prompt_build.json` | 19 | 356 | `47cb7c171b9b41c99b06332f7858efdae2a3a5c214898ad7ce028b5b71a413ba` | prompt counts per batch and the token-limit refusals |
| local | `e3/data/retry/prompts.jsonl` | 96 | 3432512 | `9ff03c68cbdd25f1a57c67c7293767af868e1a23cd49ff5b6e8081752bd0370d` | judge prompts, one per (version, judge, seed); they hold the full page text |
| local | `e3/data/retry/reuse.json` | 140 | 2897 | `b79d010ae54ac8c863c28f611ce78d70638638c0402c929871b02f51bf706f69` | which answers were reused from E1 for byte-identical prompts |
| local | `e3/data/retry/versions.jsonl` | 138 | 1121177 | `8d726a30807e20140925f73fc2654116ff74afc25a05d9371f5a90f69d49461d` | edited page versions per arm with validity flags and validator messages (page text) |
| local | `e3/data/reuse.json` | 186 | 3763 | `3efece128f4d94ddf35c38934bb6ff0415c749b3f2dff0145e800a8470f879db` | which answers were reused from E1 for byte-identical prompts |
| local | `e3/data/versions.jsonl` | 863 | 7867474 | `dd7a6be80fb8aa12ac99ff3edff3587d52fc424ae654fdbe6c5839eac98d69c7` | edited page versions per arm with validity flags and validator messages (page text) |

## sensitivity

| location | path | lines | bytes | sha256 | what it is |
|---|---|---|---|---|---|
| cluster | `data/espresso-bitterness/after.md` | 75 | 5086 | `a7d59817740258387e06db3ae739a916d284d1cf38d0dd1c59923cb22806ae93` | copy of the synthetic sample in CE samples/ (public there; listed so the sensitivity input can be checked) |
| cluster | `data/espresso-bitterness/before.md` | 41 | 4445 | `180aa52dd65d0bc1417c127067909280c6014a202b8b0267f8d7764309f84d26` | copy of the synthetic sample in CE samples/ (public there; listed so the sensitivity input can be checked) |
| cluster | `data/espresso-bitterness/pack.json` | 322 | 101565 | `c7bd08ffaf4f2c7b6fb8547e846dff46438b131fe23d3424be85edb0e94c9cc5` | copy of the synthetic sample in CE samples/ (public there; listed so the sensitivity input can be checked) |
| cluster | `data/rag-explained/after.md` | 54 | 7602 | `10c18957e28f79d29c4667f2bbdd810c5c0e7c2664bfe8d442ec845953d11c32` | copy of the synthetic sample in CE samples/ (public there; listed so the sensitivity input can be checked) |
| cluster | `data/rag-explained/before.md` | 31 | 5909 | `f5ba3462facc6785214280a47af1648f35fff1cfd2a61bab1459edafec53f9c2` | copy of the synthetic sample in CE samples/ (public there; listed so the sensitivity input can be checked) |
| cluster | `data/rag-explained/pack.json` | 322 | 106700 | `1de3612d63113d43165e48aa276f293ec29b76ce6e6d2d76f5b43ed0aa1e4ef1` | copy of the synthetic sample in CE samples/ (public there; listed so the sensitivity input can be checked) |
| cluster | `logs/ce-sens-11339589.err` | 15 | 31134 | `fd5b44aa2a4d6bfec0dd76fd8670336c0a479c074ee2fd783bd343c1732c9a70` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-sens-11339589.out` | 121 | 14186 | `74ddb106438836c557d0d1e23248eed3d07aed3b25870ea9b7dc59875a1bef9e` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-sens-11339589.out` | 121 | 14186 | `74ddb106438836c557d0d1e23248eed3d07aed3b25870ea9b7dc59875a1bef9e` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-sens-11339592.err` | 7 | 23874 | `b66711314011af9b9c711357f6547acc63d3f3cd811a0be4671d62ebac8da323` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-sens-11339592.out` | 86 | 11068 | `8870195eeb58314c0b1dfd19e752658627424897a845c58d173e33e556a6b2f0` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-sens-11339592.out` | 86 | 11068 | `8870195eeb58314c0b1dfd19e752658627424897a845c58d173e33e556a6b2f0` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-sens-11339595.err` | 24 | 26251 | `c98c128541a2dc3bac7c653b0ba073317ee6e4335d7ec174d163aa37220564c8` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-sens-11339595.out` | 107 | 14359 | `b629164705a19611e3f5e3b4cdf9077717aee6447cbec57c6634fce7f2de1716` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-sens-11339595.out` | 107 | 14359 | `b629164705a19611e3f5e3b4cdf9077717aee6447cbec57c6634fce7f2de1716` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-sens-11339599.err` | 12 | 32498 | `8b0f18c6851afdafa3525539075fd36b76e91cdd4e454f2c633f203bb9d20162` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-sens-11339599.out` | 85 | 11241 | `814cae667eca6e90f75c6fa2a3f80dadde02cdec378d6c9c22a69a1cabe7491b` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-sens-11339599.out` | 85 | 11241 | `814cae667eca6e90f75c6fa2a3f80dadde02cdec378d6c9c22a69a1cabe7491b` | job stdout; summary lines are in results/runs/logs/ |

## smoke

| location | path | lines | bytes | sha256 | what it is |
|---|---|---|---|---|---|
| cluster | `logs/ce-smoke-11339224.err` | 11 | 8834 | `45023dd3681ff503f1a96cfcc3f83dc037597bbc4f47297b6d067a78690721c3` | job stderr (vLLM and Python warnings; holds cluster paths) |
| cluster | `logs/ce-smoke-11339224.out` | 81 | 13910 | `63a9d5de12b34661795a401ebd270c70e8c79c56e17a5ad4f1320a99fe4722be` | job stdout; summary lines are in results/runs/logs/ |
| cluster | `logs/ce-smoke-11339224.out` | 81 | 13910 | `63a9d5de12b34661795a401ebd270c70e8c79c56e17a5ad4f1320a99fe4722be` | job stdout; summary lines are in results/runs/logs/ |
