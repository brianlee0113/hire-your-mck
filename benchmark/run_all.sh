#!/usr/bin/env bash
# One-command workflow. Usage: benchmark/run_all.sh [pilot|main]   (default: main)
# Needs: Claude Code logged in (`claude` on PATH), uv. Long-running: the main phase takes many hours.
set -euo pipefail
PHASE="${1:-main}"
B="$(cd "$(dirname "$0")" && pwd)"
export HYM_BENCH_WORK="${HYM_BENCH_WORK:-$HOME/hym-bench-work}"
[ -x "$B/.venv/bin/python" ] || { uv venv -q --python 3.14 "$B/.venv"; uv pip install -q --python "$B/.venv/bin/python" -r "$B/env/requirements-analysis.txt"; }
PY="$B/.venv/bin/python"
python3 "$B/cases/build_cases.py"
if [ "$PHASE" = main ]; then "$PY" "$B/scripts/freeze.py" --verify; fi
python3 "$B/scripts/run_generation.py" --phase "$PHASE" --work-root "$HYM_BENCH_WORK"
"$PY" "$B/scripts/audit_runs.py" --phase "$PHASE"
"$PY" "$B/scripts/extract_deck.py" --phase "$PHASE"
"$PY" "$B/scripts/e2e_metrics.py" --phase "$PHASE"
"$PY" "$B/scripts/evaluate.py" all --phase "$PHASE"
"$PY" "$B/scripts/make_human_eval.py" --phase "$PHASE"
"$PY" "$B/scripts/analyze.py" --phase "$PHASE"
echo "done: $B/results/$PHASE/tables.md"
