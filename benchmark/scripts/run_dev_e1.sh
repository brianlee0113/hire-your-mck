#!/bin/bash
# Overnight pipeline for the E1 development arm. Stops before each costly stage if usage is at or above 80%.
set -u
cd "$(dirname "$0")/../.."
PY=benchmark/.venv/bin/python
G=benchmark/scripts/usage_guard.sh
step() { printf "\n=== %s\n" "$1  $(date '+%H:%M:%S')"; }
step guard-before-generation; $G 0.80 || { echo "STOP: usage limit"; exit 2; }
step generation; $PY benchmark/scripts/run_generation.py --phase dev-e1 --parallel 3
for s in audit_runs extract_deck e2e_metrics; do step $s; $PY benchmark/scripts/$s.py --phase dev-e1; done
step guard-before-evaluation; $G 0.80 || { echo "STOP: usage limit"; exit 2; }
for s in normalize blind judge; do step $s; $PY benchmark/scripts/explore_e1.py $s --parallel 4; done
step guard-before-pairwise; $G 0.80 || { echo "STOP: usage limit"; exit 2; }
for s in pairwise decision analyse; do step $s; $PY benchmark/scripts/explore_e1.py $s --parallel 4; done
step guard-after; $G 1.0
step done
