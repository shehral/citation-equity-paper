#!/usr/bin/env bash
# build.sh -- regenerate every figure from data, then compile the WWW 2027 demo paper with tectonic.
#   bash build.sh            figures (scripts/fig_all.py, palette check included), then main_www.pdf
#   bash build.sh --derive   first rebuild data/ from the tool repo (read only), then as above
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

"$TECTONIC" --keep-logs main_www.tex

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
