# Environment

Cluster package versions read with importlib.metadata from the env the jobs used ($CE_ROOT_PARENT/conda_envs/monitors) on the date of this build; the *_in_job_logs fields are what the jobs themselves printed. HF revisions are the cache's refs/main, which every job loaded (the vLLM model path is the snapshot of that revision).

## Cluster (Explorer)

| item | version |
|---|---|
| python | 3.12.15 |
| vllm | 0.31.0 |
| torch | 2.13.0 |
| transformers | 5.17.0 |
| tokenizers | 0.23.2 |
| huggingface_hub | 1.33.0 |
| numpy | 2.4.6 |
| scipy | 1.18.1 |
| flashinfer-python | 0.7.0.post1 |
| triton | 3.7.1 |
| os_name | Rocky Linux |
| os_version | 9.7 (Blue Onyx) |
| torch_in_job_logs | 2.13.0+cu130 |
| vllm_in_job_logs | v0.31.0 |
| node_in_edit_jobs | v22.11.0 |
| gpus_used | A100-SXM4-40GB, A100-SXM4-80GB, H200 |

## Models

| model | revision | source |
|---|---|---|
| Qwen/Qwen3.5-9B | `c202236235762e1c871ad0ccb60c8ee5ba337b9a` | $SCRATCH/monitors/hf/hub/models--Qwen--Qwen3.5-9B/refs/main |
| Qwen/Qwen3.8-27B | `1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0` | $SCRATCH/monitors/hf/hub/models--Qwen--Qwen3.8-27B/refs/main |
| google/gemma-4-12B-it | `707f0a3b8a3c7ad586ed01e27eafbad8a27dd0f7` | $SCRATCH/monitors/hf/hub/models--google--gemma-4-12B-it/refs/main |
| google/gemma-4-31B-it | `842da3794eaa0b77d5f08bae87a17459d91ff475` | $SCRATCH/monitors/hf/hub/models--google--gemma-4-31B-it/refs/main |
| llama3.2:3b (Ollama) | `Ollama id a80c4f17acd5, weights blob sha256 dde5aa3fc5ffc17176b5e8bdc82f587b24b2678c6c66101bf7da77af9f7ccdff` | ollama list; ollama show llama3.2:3b --modelfile (FROM blob) |

## Local (bench, analysis, Ollama samples)

| item | version |
|---|---|
| node | v24.22.1 |
| pnpm | 10.20.0 |
| python3 | 3.13.13 |
| ollama | 0.40.9 |
| machine | arm64, macOS 26.5 |
| tool_packageManager | pnpm@10.20.0 |
| tool_engines_node | >=24 |
