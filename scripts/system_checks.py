"""System facts for Section 2 (bundle, engine time, tests), measured from the tool repo; writes data/system_checks.json.

Measures, at the tool repo's current commit (the tree must be clean):
  * unit tests: `pnpm -s test` (Vitest), the "Tests N passed" line;
  * browser tests: `playwright test --list` in apps/workspace (each spec runs against the root and Pages builds);
  * the static site: a fresh `pnpm -s build` of apps/workspace, total size of out/, and the gzipped JavaScript the
    /draft/ page loads (script tags in out/draft/index.html, gzip level 9);
  * engine time: median of 60 warm analyze() calls per sample draft (scripts/engine_time.mts), on this machine.

Usage: .venv/bin/python -I -B scripts/system_checks.py
"""
from __future__ import annotations

import gzip
import json
import os
import platform
import re
import subprocess

PAPER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CE = os.environ.get("CE", "../citation-equity")
APP = os.path.join(CE, "apps", "workspace")


def sh(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True, shell=isinstance(cmd, str)).stdout


def main():
    commit = sh(["git", "rev-parse", "HEAD"], CE).strip()
    clean = sh(["git", "status", "--porcelain", "--untracked-files=no"], CE).strip() == ""
    if not clean:
        raise SystemExit("system_checks: the tool repo has uncommitted changes; commit or stash them first")

    unit = int(re.search(r"Tests\s+(\d+) passed", sh("pnpm -s test 2>&1", CE)).group(1))
    listed = sh("npx playwright test --list 2>&1", APP)
    e2e_total = int(re.search(r"Total: (\d+) tests? in (\d+) files?", listed).group(1))
    projects = sorted(set(re.findall(r"^\s*\[(\w+)\]", listed, re.M)))

    sh("pnpm -s build", APP)
    out = os.path.join(APP, "out")
    site_bytes = sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(out) for f in fs)
    html = open(os.path.join(out, "draft", "index.html"), encoding="utf8").read()
    srcs = sorted(set(re.findall(r'<script[^>]+src="([^"]+\.js)"', html)))
    js_gz = 0
    for s in srcs:
        path = os.path.join(out, s.lstrip("/"))
        js_gz += len(gzip.compress(open(path, "rb").read(), 9))

    tsx = ["pnpm", "--filter", "@citation-equity/bench", "exec", "tsx", "--conditions=@citation-equity/source",
           os.path.join(PAPER, "scripts", "engine_time.mts"), CE]
    engine = json.loads(sh(tsx, CE).strip().splitlines()[-1])

    data = {
        "_provenance": {"producer": "scripts/system_checks.py", "ce_commit": commit, "ce_tree_clean": clean,
                        "machine": f"{platform.machine()} {platform.mac_ver()[0] or platform.platform()}",
                        "node": sh(["node", "--version"], CE).strip()},
        "unit_tests_passed": unit,
        "browser_tests": {"total": e2e_total, "projects": projects},
        "site": {"total_bytes": site_bytes, "draft_js_files": len(srcs), "draft_js_gzip_bytes": js_gz},
        "engine_analyze_median_ms": engine,
    }
    p = os.path.join(PAPER, "data", "system_checks.json")
    with open(p, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    print(json.dumps(data, indent=1))


if __name__ == "__main__":
    main()
