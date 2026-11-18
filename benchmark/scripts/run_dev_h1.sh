#!/bin/bash
# H1 pipeline (METHODOLOGY §15). Stops before each costly stage if weekly usage is at or above GUARD (default 0.82).
set -u
cd "$(dirname "$0")/../.."
PY=benchmark/.venv/bin/python
G=benchmark/scripts/usage_guard.sh
GUARD=${GUARD:-0.82}
step() { printf "\n=== %s\n" "$1  $(date '+%H:%M:%S')"; }
step guard-before-generation; $G $GUARD || { echo "STOP: usage limit"; exit 2; }
step generation; $PY benchmark/scripts/run_generation.py --phase dev-h1 --parallel 4
for s in audit_runs extract_deck e2e_metrics; do step $s; $PY benchmark/scripts/$s.py --phase dev-h1; done
step guard-before-evaluation; $G $GUARD || { echo "STOP: usage limit"; exit 2; }
for s in normalize blind units check; do step $s; $PY benchmark/scripts/explore_h1.py $s --parallel 4; done
step guard-before-pairwise; $G $GUARD || { echo "STOP: usage limit"; exit 2; }
for s in pairwise analyse; do step $s; $PY benchmark/scripts/explore_h1.py $s --parallel 4; done
step guard-after; $G 1.0
step done
