#!/usr/bin/env bash
# build.sh -- regenerate every figure from data, then compile the WWW 2027 demo paper with tectonic.
#   bash build.sh            figures (scripts/fig_all.py, palette check included), then main_www.pdf; reads data/ only,
#                            so it needs no tool repo (scripts/retired/ holds figure scripts the build does not run)
#   bash build.sh --derive   first rebuild data/ from the tool repo (read only), then as above
#   bash build.sh --final    as the default, then fail if an owner mark ([OWNER: ...], blue) is still printed in the PDF:
#                            run it before uploading a submission copy
# Only tectonic is used (never pdflatex, xelatex or latexmk). Fails on errors, undefined references or citations,
# overfull boxes, or a page count above the venue limit (4 pages including references).
set -euo pipefail
cd "$(dirname "$0")"

PY=.venv/bin/python
TECTONIC=/opt/homebrew/bin/tectonic
LIMIT=4

if [[ "${1:-}" == "--derive" ]]; then
  "$PY" -I -B scripts/fig_all.py --derive
else
  "$PY" -I -B scripts/fig_all.py
fi

# tectonic 0.17 writes main_www.log only with --keep-intermediates as well as --keep-logs (with --keep-logs alone it
# writes the .blg and skips the log). Delete the old log first, so the checks below can never read a stale one.
rm -f main_www.log
"$TECTONIC" --keep-logs --keep-intermediates main_www.tex
[[ -s main_www.log ]] || { echo "build.sh: main_www.log not written; the overfull and undefined checks cannot run" >&2; exit 1; }

if grep -qE "undefined|Citation .* undefined" main_www.log; then
  echo "build.sh: undefined references or citations:" >&2
  grep -nE "undefined" main_www.log >&2
  exit 1
fi
if grep -q "Overfull" main_www.log; then
  echo "build.sh: overfull boxes:" >&2
  grep -n "Overfull" main_www.log >&2
  exit 1
fi
pages=$(pdfinfo main_www.pdf | awk '/^Pages:/ {print $2}')
echo "main_www.pdf: $pages pages (limit $LIMIT, references included)"
if (( pages > LIMIT )); then
  echo "build.sh: over the page limit; cut text (log it in notes/CUTS.md), never shrink fonts or margins" >&2
  exit 1
fi
if [[ "${1:-}" == "--final" ]]; then
  # Capture first: under pipefail, "pdftotext | grep -q" reads as a failure when grep quits early (SIGPIPE to pdftotext).
  marks=$(pdftotext main_www.pdf - | grep -n "OWNER:" || true)
  if [[ -n "$marks" ]]; then
    echo "build.sh --final: an owner mark is still printed in main_www.pdf (clear it in the .tex before submitting):" >&2
    echo "$marks" >&2
    exit 1
  fi
  echo "build.sh --final: no owner mark is printed"
fi
