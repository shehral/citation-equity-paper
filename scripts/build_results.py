"""Build the reproducibility package under results/ from the tool repo and the cluster (both read only).

    .venv/bin/python -I -B scripts/build_results.py --fetch   # pull logs, sacct, hashes and env from Explorer first
    .venv/bin/python -I -B scripts/build_results.py           # rebuild from the cached pulls in .cache/cluster/

Inputs:
  CE (default ../citation-equity, or --ce-root): experiments/ plans, RESULTS_*.md, results/, and the gitignored
     local outputs experiments/{e1,e2,e3}/out and data dirs (data files are hashed, never copied).
  Explorer (ssh host alias `explorer`, --fetch only): job .out logs, sacct, sha256 of every data/answer file,
     the env's package versions and the HF cache refs. Nothing on the cluster is written.

Rules this script enforces (see results/README.md, "What is withheld"):
  - no page text, edited versions, prompts, editor logs or raw model answers are copied;
  - validator messages lose quoted fragments ('...' -> '…'), URLs (-> <url>) and word lists;
  - every copied text has cluster paths, the user name and the Slurm account replaced by placeholders.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import io
import json
import re
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "results"
CACHE = REPO / ".cache" / "cluster"
SSH = ["ssh", "-o", "BatchMode=yes", "explorer"]
MODELS = ["Qwen/Qwen3.5-9B", "Qwen/Qwen3.8-27B", "google/gemma-4-12B-it", "google/gemma-4-31B-it"]
JOB_PREFIXES = ("ce-sens", "ce-smoke", "ce-e1-", "ce-e2a-", "ce-e2b-", "ce-e3-")
GZIP_OVER = 5 * 1024 * 1024

# ---------------------------------------------------------------- settings and sanitizing
# Cluster user, paths and account live in .cache/cluster/settings.json (gitignored), never in this repo:
#   {"user": "...", "ce_root_parent": "/projects/<project>/<user>", "scratch": "/scratch/<user>",
#    "slurm_account": "...", "project": "<ce_root_parent>/geo", "python": "<env>/bin/python",
#    "hf_hub": "<scratch>/monitors/hf/hub"}
SETTINGS = json.loads((CACHE / "settings.json").read_text()) if (CACHE / "settings.json").exists() else {}


def subs() -> list[tuple[str, str]]:
    s = SETTINGS
    pairs = [(s.get("ce_root_parent"), "$CE_ROOT_PARENT"), (s.get("scratch"), "$SCRATCH"),
             (s.get("slurm_account"), "$SLURM_ACCOUNT"), (s.get("user"), "$USER"), (str(Path.home()), "$HOME")]
    return [(a, b) for a, b in pairs if a]


def sanitize(text: str) -> str:
    for old, new in subs():
        text = text.replace(old, new)
    return text


URL_RE = re.compile(r"https?://\S+|web\.archive\.org\S*|www\.\S+")

# Validator messages are rebuilt from known templates, never edited in place: a message can quote page text with
# apostrophes, double quotes or " | " inside it, so stripping quotes by regex can leak. Each template keeps only
# fixed text and numbers; anything that matches no template becomes "unrecognized validator message".
VARIABLE_TEMPLATES = [  # (fixed start, the message with its page-derived part replaced by …)
    ("Add only the query's key terms and function words", "Add only the query's key terms and function words (not: …)."),
    ("Do not add facts that are not in the allowed sources", "Do not add facts that are not in the allowed sources: name '…'."),
    ("Do not remove any heading of the original", "Do not remove any heading of the original (removed: …)."),
    ("Do not remove any link of the original", "Do not remove any link of the original (removed: …)."),
    ("Do not remove any list item of the original", "Do not remove any list item of the original (removed: …)."),
    ("Do not remove any table row of the original", "Do not remove any table row of the original (removed: …)."),
    ("Keep exactly the query key terms the spans contain", "Keep exactly the query key terms the spans contain (lost: …, added: …)."),
    ("The heading may use only words from the heading or its section's first paragraph", "The heading may use only words from the heading or its section's first paragraph (not: …)."),
    ("Unknown span id", "Unknown span id '…'; use only the ids given (…)."),
]
FIXED_TEMPLATES = [re.compile(p) for p in (
    r"The [\w-]+ check did not rise \([\d.]+ -> [\d.]+\)\.",
    r"The paraphrase changed the [\w-]+ check \([\d.]+ -> [\d.]+\); keep the same structure, figures, quotes and links\.",
    r"The paraphrase must keep the spans' length within \d+% \(\d+ -> \d+ words\)\.",
    r"The page length went from \d+ to \d+ words \([\d.]+x; allowed [\d.]+-[\d.]+x\)\.",
    r"After the edit the [\w-]+ check is not applicable\.",
    r"The quotation must be \d+ words or fewer\.",
    r"The quotation must be copied verbatim from the source document\.",
    r"Keep the original sentence exactly as it is and only insert the new material\.",
    r"No section was split under a new heading\.",
    r"Pick a passage that has no double quote marks inside it\.",
    r"Reword the spans: the answer left every span unchanged\.",
    r"The answer must be one JSON object mapping span ids to replacements\.",
    r"The answer was cut off at the token limit\. Return only the JSON object, with short replacements\.",
    r"Work the missing query key terms into the title, the first heading or the first paragraph\.",
    r"every step failed",
    r"the editor returned NONE",
)]
STARTS = tuple(t for t, _ in VARIABLE_TEMPLATES) + (
    "The ", "After the edit", "Keep the original", "No section", "Pick a passage", "Reword the spans", "Work the missing", "every step")


def strip_fragments(msg: str) -> str:
    """A validator message rebuilt from templates: no quoted page text, URL or word list survives."""
    prefix = ""
    for p in ("invalid:", "not applicable:"):
        if msg.startswith(p):
            prefix, msg = p + " ", msg[len(p):].strip()
    segments: list[str] = []
    for piece in msg.split(" | "):
        if segments and not piece.startswith(STARTS):
            segments[-1] += " | " + piece  # a " | " inside a quoted fragment, not a new message
        else:
            segments.append(piece)
    out = []
    for seg in segments:
        seg = seg.strip()
        hit = next((rep for start, rep in VARIABLE_TEMPLATES if seg.startswith(start)), None)
        if hit:
            out.append(hit)
        elif any(t.fullmatch(seg) for t in FIXED_TEMPLATES):
            out.append(seg)
        else:
            out.append("unrecognized validator message")
    return prefix + " | ".join(out)


def strip_tool_reason(msg: str) -> str:
    """An applicability reason (tool-authored text): URLs out, numbers kept."""
    return URL_RE.sub("<url>", msg)


def category(msg: str, tool_authored: bool = False) -> str:
    """A reason category: fragments stripped (validator messages) and every number masked as N."""
    base = strip_tool_reason(msg) if tool_authored else strip_fragments(msg)
    return re.sub(r"\d+(?:\.\d+)?", "N", base).strip()


def sanitize_json_strings(obj, key=None):
    """Strip fragments from validator reasons in an analysis JSON; leave the tool's own prose alone."""
    if isinstance(obj, dict):
        return {k: sanitize_json_strings(v, k) for k, v in obj.items()}
    if isinstance(obj, list):
        return [sanitize_json_strings(v, key) for v in obj]
    if isinstance(obj, str):
        s = sanitize(obj)
        if key == "reason" or s.startswith(("invalid:", "not applicable:")):
            s = strip_fragments(s)
        return URL_RE.sub("<url>", s)
    return obj


# ---------------------------------------------------------------- helpers


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def count_lines(path: Path) -> int:
    n = 0
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            n += chunk.count(b"\n")
    return n


def git_commits(ce: Path, rel: str) -> list[str]:
    out = subprocess.run(["git", "-C", str(ce), "log", "--format=%h", "--", rel], capture_output=True, text=True, check=True)
    return out.stdout.split()


def git_head(ce: Path) -> str:
    return subprocess.run(["git", "-C", str(ce), "rev-parse", "--short", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, obj) -> None:
    write_text(path, json.dumps(obj, indent=1, ensure_ascii=False) + "\n")


def place(path: Path, data: bytes) -> Path:
    """Write bytes, gzipped (deterministic, mtime 0) when over 5 MB."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if len(data) > GZIP_OVER:
        gz = path.with_name(path.name + ".gz")
        buf = io.BytesIO()
        with gzip.GzipFile(filename=path.name, mode="wb", fileobj=buf, mtime=0) as fh:
            fh.write(data)
        gz.write_bytes(buf.getvalue())
        return gz
    path.write_bytes(data)
    return path


def copy_numbers_jsonl(src: Path, dst: Path) -> Path:
    """Copy a numbers-only JSONL after checking that no string field is long enough to hold text."""
    data = src.read_bytes()
    for i, line in enumerate(data.decode().splitlines()):
        for k, v in json.loads(line).items():
            if isinstance(v, str) and len(v) > 64:
                sys.exit(f"{src}:{i + 1}: field {k} holds a long string; refusing to copy")
    return place(dst, data)


# ---------------------------------------------------------------- fetch (read only on the cluster)


def fetch() -> None:
    S = SETTINGS
    if not S:
        sys.exit("--fetch needs .cache/cluster/settings.json (see the comment at the top of this script)")
    CLUSTER_ROOT, CLUSTER_PY, HF_HUB = S["project"], S["python"], S["hf_hub"]
    CACHE.mkdir(parents=True, exist_ok=True)
    logs = CACHE / "logs"
    if logs.exists():
        shutil.rmtree(logs)
    logs.mkdir()
    tar = subprocess.run(SSH + [f"cd {CLUSTER_ROOT}/logs && tar czf - ."], capture_output=True, check=True).stdout
    subprocess.run(["tar", "xzf", "-", "-C", str(logs)], input=tar, check=True)
    sacct = f"sacct -u {S['user']} --starttime 2026-10-23 -X -n -P -o JobID,JobName%60,Partition,AllocTRES%60,State,Elapsed,Start,End,NodeList"
    (CACHE / "sacct.txt").write_text(subprocess.run(SSH + [sacct], capture_output=True, text=True, check=True).stdout)
    nodes = "sinfo -N -h -o '%N|%G' | sort -u"
    (CACHE / "nodes.txt").write_text(subprocess.run(SSH + [nodes], capture_output=True, text=True, check=True).stdout)
    manifest = (
        f"cd {CLUSTER_ROOT} && find data e1 e2 e3 logs -type f | sort | while read f; do "
        'printf "%s\\t%s\\t%s\\t%s\\n" "$f" "$(wc -l < "$f")" "$(stat -c %s "$f")" "$(sha256sum "$f" | cut -d" " -f1)"; done'
    )
    (CACHE / "cluster_manifest.tsv").write_text(subprocess.run(SSH + [manifest], capture_output=True, text=True, check=True, timeout=1200).stdout)
    # importlib.metadata only: importing torch or vllm on the login node gets the process killed.
    pyver = (
        f"{CLUSTER_PY} -I -c \"import sys; from importlib.metadata import version as v; print('python', sys.version.split()[0]); "
        "[print(m, v(m)) for m in ['vllm','torch','transformers','tokenizers','huggingface_hub','numpy','scipy','flashinfer-python','triton']]\""
    )
    (CACHE / "env_python.txt").write_text(subprocess.run(SSH + [pyver], capture_output=True, text=True, check=True).stdout)
    refs = "; ".join(
        f"echo {m} $(cat {HF_HUB}/models--{m.replace('/', '--')}/refs/main)" for m in MODELS
    ) + "; head -2 /etc/os-release"
    (CACHE / "env_hf.txt").write_text(subprocess.run(SSH + [refs], capture_output=True, text=True, check=True).stdout)


# ---------------------------------------------------------------- 1. plans

PLANS = [
    ("PREREG_sensitivity.md", "experiments/PREREG_sensitivity.md"),
    ("PREREG_E1.md", "experiments/PREREG_E1.md"),
    ("PREREG_E1_revisions.md", "experiments/PREREG_E1_revisions.md"),
    ("PLAN_E2.md", "experiments/PLAN_E2.md"),
    ("PLAN_E3.md", "experiments/PLAN_E3.md"),
    ("E1_freeze_MANIFEST.md", "experiments/e1/freeze/MANIFEST.md"),
]


def build_plans(ce: Path, head: str) -> list[dict]:
    rows = []
    for name, rel in PLANS:
        commits = git_commits(ce, rel)
        first, last = commits[-1], commits[0]
        header = (
            f"> Copy of `citation-equity/{rel}`. First in tool commit `{first}`, last changed in `{last}` "
            f"(`git log --format=%h -- {rel}`: {' '.join(commits)}). Copied at tool HEAD `{head}`.\n\n"
        )
        write_text(OUT / "plans" / name, header + sanitize((ce / rel).read_text()))
        rows.append({"file": name, "source": rel, "first": first, "last": last, "commits": commits})
    return rows


# ---------------------------------------------------------------- 2. per-experiment results


def strip_answers(obj: dict) -> dict:
    """Sensitivity and smoke JSONs: every raw model answer becomes its sha256 and length."""
    for row in obj.get("rows", []):
        if "answer" in row:
            ans = row.pop("answer")
            row["answer_sha256"] = hashlib.sha256(ans.encode()).hexdigest()
            row["answer_chars"] = len(ans)
    return obj


def validity_counts(versions: Path, applicability: Path | None) -> dict:
    per = defaultdict(lambda: {"versions": 0, "valid": 0, "invalid": 0, "not_applicable": 0, "attempts": Counter(), "reasons": Counter()})
    for line in versions.open():
        d = json.loads(line)
        c = per[(d["set"], d["arm"])]
        c["versions"] += 1
        c["attempts"][str(d.get("attempts"))] += 1
        reason = d.get("excluded_reason") or ""
        if d["valid"]:
            c["valid"] += 1
        elif reason.startswith("not applicable"):
            c["not_applicable"] += 1
            c["reasons"][category(reason)] += 1
        else:
            c["invalid"] += 1
            body = reason.removeprefix("invalid:").strip()
            for part in strip_fragments(body).split(" | "):
                c["reasons"][category(part)] += 1
    out = {"source": versions.name, "note": "valid / invalid / not_applicable per (set, arm); reasons are validator message categories with quoted text, URLs and word lists stripped and numbers masked as N; one invalid version can carry several reasons", "arms": []}
    for (s, a), c in sorted(per.items(), key=lambda kv: (kv[0][0], arm_key(kv[0][1]))):
        out["arms"].append({"set": s, "arm": a, "versions": c["versions"], "valid": c["valid"], "invalid": c["invalid"], "not_applicable": c["not_applicable"], "attempts": dict(sorted(c["attempts"].items())), "reasons": dict(c["reasons"].most_common())})
    if applicability and applicability.exists():
        pre = defaultdict(lambda: {"applicable": 0, "not_applicable": 0, "reasons": Counter()})
        for line in applicability.open():
            d = json.loads(line)
            p = pre[d["arm"]]
            if d["applicable"]:
                p["applicable"] += 1
            else:
                p["not_applicable"] += 1
                p["reasons"][category(d.get("reason") or "", tool_authored=True)] += 1
        out["applicability_precheck"] = {
            "source": applicability.name,
            "note": "per arm, how many queries the frozen applicability table marked applicable before editing",
            "arms": [{"arm": a, "applicable": p["applicable"], "not_applicable": p["not_applicable"], "reasons": dict(p["reasons"].most_common())} for a, p in sorted(pre.items(), key=lambda kv: arm_key(kv[0]))],
        }
    return out


def arm_key(arm: str):
    if arm.isdigit():
        return (0, int(arm), "")
    if re.fullmatch(r"\d+[A-Z]", arm):
        return (0, int(arm[:-1]), arm)
    if re.fullmatch(r"P\d+", arm):
        return (1, int(arm[1:]), "")
    return (2, 0, arm)


def validity_md(v: dict, title: str) -> str:
    lines = [f"# Validity counts: {title}", "", f"From `{v['source']}` (withheld; hash in `results/manifests/`). {v['note']}.", "",
             "| set | arm | versions | valid | invalid | not applicable | most common reason |", "|---|---|---|---|---|---|---|"]
    for a in v["arms"]:
        top = next(iter(a["reasons"].items()), ("", 0))
        lines.append(f"| {a['set']} | {a['arm']} | {a['versions']} | {a['valid']} | {a['invalid']} | {a['not_applicable']} | {top[0].replace('|', '/')} ({top[1]}) |" if top[0] else f"| {a['set']} | {a['arm']} | {a['versions']} | {a['valid']} | {a['invalid']} | {a['not_applicable']} | |")
    return "\n".join(lines) + "\n"


def write_validity(dst: Path, versions: Path, applicability: Path | None, title: str) -> None:
    v = validity_counts(versions, applicability)
    write_json(dst / "validity_counts.json", v)
    write_text(dst / "validity_counts.md", validity_md(v, title))


def build_results(ce: Path) -> None:
    ex = ce / "experiments"
    # sensitivity (+ the vLLM smoke test it came after)
    d = OUT / "sensitivity"
    write_text(d / "RESULTS_sensitivity.md", sanitize((ex / "RESULTS_sensitivity.md").read_text()))
    for src in sorted((ex / "results" / "sensitivity").glob("*.json")):
        write_json(d / src.name, strip_answers(json.loads(src.read_text())))
    write_json(d / "smoke_google__gemma-4-12B-it.json", strip_answers(json.loads((ex / "results" / "smoke_google__gemma-4-12B-it.json").read_text())))

    # E1
    d = OUT / "e1"
    write_text(d / "RESULTS_E1.md", sanitize((ex / "RESULTS_E1.md").read_text()))
    write_json(d / "analysis.json", sanitize_json_strings(json.loads((ex / "e1/out/analysis.json").read_text())))
    write_json(d / "score_summary.json", json.loads((ex / "e1/out/score_summary.json").read_text()))
    shutil.copyfile(ex / "e1/freeze/null_simulation.json", d / "null_simulation.json")
    for name in ("cells.jsonl", "scores.jsonl", "retrieval.jsonl"):
        copy_numbers_jsonl(ex / "e1/out" / name, d / name)
    write_validity(d, ex / "e1/data/versions.jsonl", ex / "e1/data/applicability.jsonl", "E1 (main and replication)")

    # E2: a = words or structure (9W, 9P), b = editor check (Qwen3.8-27B edits)
    d = OUT / "e2"
    write_text(d / "RESULTS_E2.md", sanitize((ex / "RESULTS_E2.md").read_text()))
    write_json(d / "analysis_e2.json", sanitize_json_strings(json.loads((ex / "e2/out/analysis_e2.json").read_text())))
    for part, vdir in (("a", ex / "e2/data"), ("b", ex / "e2/data/b")):
        write_json(d / part / "score_summary.json", json.loads((ex / f"e2/out/{part}/score_summary.json").read_text()))
        for name in ("cells.jsonl", "scores.jsonl"):
            copy_numbers_jsonl(ex / f"e2/out/{part}" / name, d / part / name)
        write_validity(d / part, vdir / "versions.jsonl", vdir / "applicability.jsonl" if part == "b" else None,
                       "E2a (9W, 9P)" if part == "a" else "E2b (editor Qwen3.8-27B)")

    # E3: new queries, the extra attempt on E1's queries, and the pooled analysis
    d = OUT / "e3"
    write_text(d / "pooled" / "RESULTS_E3.md", sanitize((ex / "RESULTS_E3.md").read_text()))
    write_json(d / "pooled" / "analysis_e3.json", sanitize_json_strings(json.loads((ex / "e3/out/analysis_e3.json").read_text())))
    for part, vdir in (("new", ex / "e3/data"), ("retry", ex / "e3/data/retry")):
        write_json(d / part / "score_summary.json", json.loads((ex / f"e3/out/{part}/score_summary.json").read_text()))
        for name in ("cells.jsonl", "scores.jsonl"):
            copy_numbers_jsonl(ex / f"e3/out/{part}" / name, d / part / name)
        write_validity(d / part, vdir / "versions.jsonl", vdir / "applicability.jsonl",
                       "E3 new queries (sets e3, e3-four)" if part == "new" else "E3 extra attempt on E1's main set")


# ---------------------------------------------------------------- 3. manifests of withheld files

WHAT = [
    (r"^data/(espresso-bitterness|rag-explained)/", "copy of the synthetic sample in CE samples/ (public there; listed so the sensitivity input can be checked)"),
    (r"(^|/)\.pages\.jsonl\.\w+$", "temporary copy of pages.jsonl left by an interrupted write (same bytes as pages.jsonl)"),
    (r"raw/live\.jsonl$", "live fetches of the GEO-bench source URLs (page text)"),
    (r"raw/wayback\.jsonl$", "2023 Wayback fetches for pages whose live fetch failed (page text)"),
    (r"raw/cseo\.jsonl$", "C-SEO Bench pages as fetched (page text)"),
    (r"candidates\.jsonl$", "every fetched candidate page per query, with text, usability and sha256"),
    (r"fetch_log\.jsonl$", "per-URL fetch outcome (URL, source, status, word and token counts, sha256)"),
    (r"wayback_needed\.jsonl$", "pages queued for a Wayback fetch"),
    (r"versions\.main-only\.jsonl$", "edited versions of the main set only (kept from before the replication edit job)"),
    (r"pages\.jsonl$", "normalized pages used by the experiment (page text, roles target/other)"),
    (r"applicability\.jsonl$", "frozen per-query, per-arm applicability table (which checks flag something)"),
    (r"admission(_e3)?\.json$", "admitted query ids and set sizes"),
    (r"versions\.jsonl$", "edited page versions per arm with validity flags and validator messages (page text)"),
    (r"editor_log\.jsonl$", "editor model requests and responses per edit attempt (page text)"),
    (r"prompts\.jsonl$", "judge prompts, one per (version, judge, seed); they hold the full page text"),
    (r"prompt_build\.json$", "prompt counts per batch and the token-limit refusals"),
    (r"make_versions\.json$", "counts from E2a's 9W and 9P version builder"),
    (r"reuse\.json$", "which answers were reused from E1 for byte-identical prompts"),
    (r"engine_original\.jsonl$", "engine check results on each original page (spans quote page text)"),
    (r"answers/reused-e1\.[\w.-]+\.jsonl$", "E1 answers reused for byte-identical prompts (raw model answers)"),
    (r"answers/[\w.-]+\.jsonl$", "raw judge answers for one batch (raw model answers)"),
    (r"fetch-run\.log$", "local console log of the live fetch run"),
    (r"logs/[\w.-]+\.err$", "job stderr (vLLM and Python warnings; holds cluster paths)"),
    (r"logs/[\w.-]+\.out$", "job stdout; summary lines are in results/runs/logs/"),
]


def what_is(path: str) -> str:
    for pat, desc in WHAT:
        if re.search(pat, path):
            return desc
    return "withheld data file"


def experiment_of(path: str) -> str:
    p = path
    if re.match(r"data/(espresso-bitterness|rag-explained)/", p):
        return "sensitivity"
    if re.search(r"(^|/)timing\d?(/|\.)", p):
        return "e1-timing"
    for exp in ("e1", "e2", "e3"):
        if re.search(rf"(^|/){exp}(/|-)", p) or p.startswith(f"data/{exp}/"):
            return exp
    if "ce-sens" in p:
        return "sensitivity"
    if "ce-smoke" in p:
        return "smoke"
    m = re.search(r"ce-(e1|e2a|e2b|e3)-", p)
    if m:
        return m.group(1)
    return "?"


def build_manifests(ce: Path) -> dict:
    ex = ce / "experiments"
    rows = []
    for exp in ("e1", "e2", "e3"):
        base = ex / exp
        for f in sorted((base / "data").rglob("*")):
            if f.is_file():
                rel = f.relative_to(base).as_posix()
                rows.append({"location": "local", "experiment": exp if "timing" not in rel else "e1-timing", "path": f"{exp}/{rel}", "lines": count_lines(f), "bytes": f.stat().st_size, "sha256": sha256(f), "what": what_is(rel)})
    f = ex / "e1/out/fetch-run.log"
    rows.append({"location": "local", "experiment": "e1", "path": "e1/out/fetch-run.log", "lines": count_lines(f), "bytes": f.stat().st_size, "sha256": sha256(f), "what": what_is(f.name)})
    for line in (CACHE / "cluster_manifest.tsv").read_text().splitlines():
        path, lines, size, digest = line.split("\t")
        if path.startswith("logs/") and not re.search(r"logs/ce-", path):
            continue
        rows.append({"location": "cluster", "experiment": experiment_of(path), "path": path, "lines": int(lines), "bytes": int(size), "sha256": digest, "what": what_is(path)})
    for f in sorted((CACHE / "logs").glob("ce-*.out")):
        rows.append({"location": "cluster", "experiment": experiment_of(f.name), "path": f"logs/{f.name}", "lines": count_lines(f), "bytes": f.stat().st_size, "sha256": sha256(f), "what": what_is(f"logs/{f.name}")})
    rows.sort(key=lambda r: (r["experiment"], r["location"], r["path"]))
    d = OUT / "manifests"
    d.mkdir(parents=True, exist_ok=True)
    with open(d / "withheld.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    md = ["# Withheld files: path, line count, sha256", "",
          "Every file below stays on the owner's machine (`local`, paths relative to `citation-equity/experiments/`) or on Explorer (`cluster`, paths relative to the project folder `$CE_ROOT_PARENT/geo`). None is in this repo: they hold third-party page text, edited versions, prompts, editor logs or raw model answers. A rerun that produces the same bytes has the same sha256. Machine-readable copy: `withheld.csv`.", ""]
    for exp in sorted({r["experiment"] for r in rows}):
        md += [f"## {exp}", "", "| location | path | lines | bytes | sha256 | what it is |", "|---|---|---|---|---|---|"]
        md += [f"| {r['location']} | `{r['path']}` | {r['lines']} | {r['bytes']} | `{r['sha256']}` | {r['what']} |" for r in rows if r["experiment"] == exp]
        md.append("")
    write_text(d / "README.md", "\n".join(md))
    return {"files": len(rows), "local": sum(r["location"] == "local" for r in rows), "cluster": sum(r["location"] == "cluster" for r in rows)}


# ---------------------------------------------------------------- 4. runs


def elapsed_hours(s: str) -> float:
    days = 0
    if "-" in s:
        d, s = s.split("-", 1)
        days = int(d)
    h, m, sec = (int(x) for x in s.split(":"))
    return days * 24 + h + m / 60 + sec / 3600


def gpu_group(name: str) -> str:
    for exp, pre in (("smoke", "ce-smoke"), ("sensitivity", "ce-sens"), ("e1", "ce-e1-"), ("e2a", "ce-e2a-"), ("e2b", "ce-e2b-"), ("e3", "ce-e3-")):
        if name.startswith(pre):
            return exp
    return ""


def log_summary(path: Path) -> tuple[str, dict]:
    """Start/end lines, GPU and torch lines and the JSON summary blocks of a job .out log; nothing else."""
    keep, info = [], {}
    in_json = False
    skip = False
    for line in path.read_text(errors="replace").splitlines():
        if line.startswith("--- first answer ---"):
            skip = True  # the smoke test prints its first raw answer: never copied
            keep.append("--- first answer --- [raw model answer withheld]")
            continue
        if line.startswith("=== "):
            skip = False
            keep.append(line)
            m = re.search(r"start: .*? on (\S+)", line)
            if m:
                info["node"] = m.group(1)
            for k in ("model", "judge", "prompts", "sets", "extra"):
                mm = re.search(rf"\b{k}=(.*?)(?= \w+=| ===$)", line)
                if mm:
                    info[k] = mm.group(1)
            continue
        if skip:
            continue
        if in_json:
            keep.append(line)
            if line == "}":
                in_json = False
            continue
        if line == "{":
            in_json = True
            keep.append(line)
            continue
        if line.startswith(("NVIDIA ", "torch ", "node v", "settings ok")):
            keep.append(line)
            if line.startswith("NVIDIA ") and "gpu_name" not in info:
                info["gpu_name"] = line.split(",")[0].removeprefix("NVIDIA ").strip()
    return sanitize("\n".join(keep)) + "\n", info


def role_of(name: str, info: dict) -> str:
    p = info.get("prompts", "") + " " + info.get("sets", "") + " " + info.get("extra", "")
    if "timing" in p:
        return "timing smoke (held-out query, outcomes discarded)"
    if name.startswith("ce-e1-norm"):
        return "normalize pages (CPU)"
    if name.startswith("ce-smoke"):
        return "vLLM smoke test"
    if name.startswith("ce-sens"):
        return "sensitivity test"
    if "edit" in name:
        return "edit pages"
    if "retry" in p:
        return "judge answers (E1 queries, extra attempt)"
    return "judge answers"


def build_runs() -> dict:
    nodes = {}
    for line in (CACHE / "nodes.txt").read_text().splitlines():
        if "|" in line:
            n, g = line.split("|", 1)
            nodes.setdefault(n.strip(), g.strip())
    logs = {}
    for f in (CACHE / "logs").glob("ce-*.out"):
        m = re.search(r"-(\d+)\.out$", f.name)
        if m:
            logs[m.group(1)] = f
    rows = []
    sumdir = OUT / "runs" / "logs"
    if sumdir.exists():
        shutil.rmtree(sumdir)
    sumdir.mkdir(parents=True)
    for line in (CACHE / "sacct.txt").read_text().splitlines():
        parts = line.split("|")
        if len(parts) < 8:
            continue
        jobid, name, part, tres, state, elapsed, start, end = (p.strip() for p in parts[:8])
        state = re.sub(r"^CANCELLED by \d+$", "CANCELLED", state)
        node = parts[8].strip() if len(parts) > 8 else ""
        if not name.startswith(JOB_PREFIXES):
            continue
        m = re.search(r"gres/gpu(?::(\w+))?=(\d+)", tres)
        gpus = int(m.group(2)) if m else 0
        tres_type = m.group(1) if m and m.group(1) else ""
        info, summary_file = {}, ""
        if jobid in logs:
            text, info = log_summary(logs[jobid])
            summary_file = f"logs/{logs[jobid].stem}.summary.txt"
            write_text(OUT / "runs" / summary_file, text)
        gm = re.search(r"gpu:(\w+):", nodes.get(node, ""))
        gpu_type = tres_type or (gm.group(1) if gm else "")
        hours = elapsed_hours(elapsed)
        rows.append({
            "job_id": jobid, "job_name": name, "experiment": gpu_group(name), "role": role_of(name, info),
            "partition": part, "node": sanitize(node), "gpus": gpus, "gpu_type": gpu_type, "gpu_model": info.get("gpu_name", ""),
            "alloc_tres": tres, "state": state, "elapsed": elapsed, "hours": round(hours, 4), "gpu_hours": round(hours * gpus, 4),
            "start": start, "end": end, "model": info.get("model", ""), "log_summary": summary_file,
        })
    rows.sort(key=lambda r: r["start"] if r["start"] != "None" else r["end"])
    d = OUT / "runs"
    with open(d / "jobs.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    totals = defaultdict(float)
    by_type = defaultdict(float)
    by_role = defaultdict(float)
    for r in rows:
        totals[r["experiment"]] += r["gpu_hours"]
        by_role[f"{r['experiment']}:{r['role']}"] += r["gpu_hours"]
        if r["gpus"]:
            by_type[f"{r['experiment']}:{r['gpu_type']}"] += r["gpu_hours"]
    order = ["smoke", "sensitivity", "e1", "e2a", "e2b", "e3"]
    gh = {"per_experiment": {e: round(totals[e], 2) for e in order}, "e2_total": round(totals["e2a"] + totals["e2b"], 2),
          "overall": round(sum(totals.values()), 2), "per_experiment_and_gpu_type": {k: round(v, 2) for k, v in sorted(by_type.items())},
          "per_experiment_and_role": {k: round(v, 2) for k, v in sorted(by_role.items()) if v},
          "jobs": len(rows), "note": "GPU-hours = Slurm Elapsed x GPUs allocated (gres/gpu); every GPU job used 1 GPU. CPU-only jobs (ce-e1-norm) count 0. The cancelled job never started. Times are the cluster's clock (US Eastern)."}
    write_json(d / "gpu_hours.json", gh)
    md = ["# Cluster jobs", "", "Every Slurm job of the sensitivity test, the smoke test and E1 to E3 on Explorer, from",
          "`sacct -u $USER --starttime 2026-10-23 -X -n -P -o JobID,JobName%60,Partition,AllocTRES%60,State,Elapsed,Start,End` (plus NodeList).",
          "AllocTRES records the GPU count but not its type, so the type comes from the node's gres (`sinfo -N -o '%N|%G'`) and the exact model from the `nvidia-smi` line the job printed. Times are the cluster's clock (US Eastern). Machine-readable copy: `jobs.csv`; totals: `gpu_hours.json`; each job's start/end lines and JSON summary: `logs/`.", "",
          "## GPU-hours", "", "| experiment | GPU-hours |", "|---|---|"]
    md += [f"| {e} | {gh['per_experiment'][e]:.2f} |" for e in order]
    md += [f"| E2 (a + b) | {gh['e2_total']:.2f} |", f"| **overall** | **{gh['overall']:.2f}** |", "",
           "| experiment : GPU type | GPU-hours |", "|---|---|"]
    md += [f"| {k} | {v:.2f} |" for k, v in gh["per_experiment_and_gpu_type"].items()]
    md += ["", "| experiment : role | GPU-hours |", "|---|---|"]
    md += [f"| {k} | {v:.2f} |" for k, v in gh["per_experiment_and_role"].items()]
    md += ["", "## Jobs", "", "| job | name | role | partition | GPU | elapsed | GPU-h | state | start | model | summary |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        gpu = f"{r['gpus']} x {r['gpu_model'] or r['gpu_type']}" if r["gpus"] else "none"
        summ = f"[log]({r['log_summary']})" if r["log_summary"] else ""
        md.append(f"| {r['job_id']} | `{r['job_name']}` | {r['role']} | {r['partition']} | {gpu} | {r['elapsed']} | {r['gpu_hours']:.2f} | {r['state']} | {r['start']} | {r['model']} | {summ} |")
    write_text(d / "README.md", "\n".join(md) + "\n")
    return gh


# ---------------------------------------------------------------- 5. env


def build_env(ce: Path) -> dict:
    env = {"cluster": {}, "models": {}, "local": {}}
    for line in (CACHE / "env_python.txt").read_text().splitlines():
        k, _, v = line.partition(" ")
        env["cluster"][k] = v
    hf_lines = (CACHE / "env_hf.txt").read_text().splitlines()
    for line in hf_lines:
        parts = line.split()
        if len(parts) == 2 and "/" in parts[0]:
            env["models"][parts[0]] = {"hf_revision": parts[1], "source": f"$SCRATCH/monitors/hf/hub/models--{parts[0].replace('/', '--')}/refs/main"}
        elif line.startswith(("NAME=", "VERSION=")):
            env["cluster"]["os_" + line.split("=")[0].lower()] = line.split("=", 1)[1].strip('"')
    logs_text = "\n".join(f.read_text(errors="replace") for f in (CACHE / "logs").glob("ce-*.out"))
    m = re.search(r"torch (\S+) NVIDIA", logs_text)
    env["cluster"]["torch_in_job_logs"] = m.group(1) if m else ""
    m = re.search(r"Initializing a V1 LLM engine \((v[\d.]+)\)", logs_text)
    env["cluster"]["vllm_in_job_logs"] = m.group(1) if m else ""
    m = re.search(r"^node (v[\d.]+)", logs_text, re.M)
    env["cluster"]["node_in_edit_jobs"] = m.group(1) if m else ""
    env["cluster"]["gpus_used"] = sorted(set(re.findall(r"^NVIDIA ([^,]+),", logs_text, re.M)))

    def run(cmd):
        try:
            return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout.strip()
        except Exception as e:  # noqa: BLE001
            return f"unavailable ({type(e).__name__})"

    env["local"]["node"] = run(["node", "--version"])
    env["local"]["pnpm"] = run(["pnpm", "--version"])
    env["local"]["python3"] = run(["python3", "--version"]).removeprefix("Python ")
    env["local"]["ollama"] = run(["ollama", "--version"]).removeprefix("ollama version is ")
    lst = run(["ollama", "list"])
    m = re.search(r"^llama3\.2:3b\s+(\w+)", lst, re.M)
    mf = run(["ollama", "show", "llama3.2:3b", "--modelfile"])
    mm = re.search(r"sha256-([0-9a-f]{64})", mf)
    env["models"]["llama3.2:3b (Ollama)"] = {"ollama_id": m.group(1) if m else "", "weights_blob_sha256": mm.group(1) if mm else "", "source": "ollama list; ollama show llama3.2:3b --modelfile (FROM blob)"}
    env["local"]["machine"] = run(["uname", "-m"]) + ", macOS " + run(["sw_vers", "-productVersion"])
    pkg = json.loads((ce / "package.json").read_text())
    env["local"]["tool_packageManager"] = pkg.get("packageManager", "")
    env["local"]["tool_engines_node"] = pkg.get("engines", {}).get("node", "")
    env["note"] = "Cluster package versions read with importlib.metadata from the env the jobs used ($CE_ROOT_PARENT/conda_envs/monitors) on the date of this build; the *_in_job_logs fields are what the jobs themselves printed. HF revisions are the cache's refs/main, which every job loaded (the vLLM model path is the snapshot of that revision)."
    env["generated"] = datetime.now().astimezone().isoformat(timespec="seconds")
    d = OUT / "env"
    write_json(d / "env.json", env)
    md = ["# Environment", "", env["note"], "", "## Cluster (Explorer)", "", "| item | version |", "|---|---|"]
    md += [f"| {k} | {', '.join(v) if isinstance(v, list) else v} |" for k, v in env["cluster"].items()]
    md += ["", "## Models", "", "| model | revision | source |", "|---|---|---|"]
    for k, v in env["models"].items():
        rev = v.get("hf_revision") or f"Ollama id {v.get('ollama_id')}, weights blob sha256 {v.get('weights_blob_sha256')}"
        md.append(f"| {k} | `{rev}` | {v['source']} |")
    md += ["", "## Local (bench, analysis, Ollama samples)", "", "| item | version |", "|---|---|"]
    md += [f"| {k} | {v} |" for k, v in env["local"].items()]
    write_text(d / "README.md", "\n".join(md) + "\n")
    return env


# ---------------------------------------------------------------- checks


def final_checks() -> None:
    bad = []
    for f in OUT.rglob("*"):
        if not f.is_file():
            continue
        if f.stat().st_size > 50 * 1024 * 1024:
            bad.append(f"{f}: over 50 MB")
        if f.suffix == ".gz":
            text = gzip.decompress(f.read_bytes()).decode(errors="replace")
        else:
            text = f.read_text(errors="replace")
        for needle in [a for a, _ in subs()] + ["SBATCH_ACCOUNT=", "CE_PYTHON="]:
            if needle in text:
                bad.append(f"{f}: contains {needle!r}")
        if f.suffix in (".md",) and "\u2014" in text and "plans" not in f.parts and not f.name.startswith("RESULTS"):
            bad.append(f"{f}: em dash in prose")
    if bad:
        sys.exit("final checks failed:\n" + "\n".join(bad))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ce-root", default=str(REPO.parent / "citation-equity"))
    ap.add_argument("--fetch", action="store_true", help="pull logs, sacct, hashes and env from Explorer (read only)")
    args = ap.parse_args()
    ce = Path(args.ce_root).resolve()
    if args.fetch:
        fetch()
    head = git_head(ce)
    for sub in ("plans", "sensitivity", "e1", "e2", "e3", "manifests", "runs", "env"):
        if (OUT / sub).exists():
            shutil.rmtree(OUT / sub)
    plans = build_plans(ce, head)
    build_results(ce)
    man = build_manifests(ce)
    gh = build_runs()
    build_env(ce)
    write_json(OUT / "build_info.json", {"tool_head": head, "plans": plans, "manifest_counts": man, "gpu_hours": gh["per_experiment"], "gpu_hours_overall": gh["overall"], "built": datetime.now().astimezone().isoformat(timespec="seconds")})
    final_checks()
    print(json.dumps({"tool_head": head, "manifest": man, "gpu_hours": gh}, indent=1))


if __name__ == "__main__":
    main()
