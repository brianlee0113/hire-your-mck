#!/bin/bash
# Holdout pipeline (METHODOLOGY §16). Run inside `caffeinate -is` (a sleeping Mac hangs `claude -p` turns).
# Stops before each costly stage if weekly usage is at or above GUARD (default 0.82), and if any frozen file changed.
set -u
cd "$(dirname "$0")/../.."
PY=benchmark/.venv/bin/python
G=benchmark/scripts/usage_guard.sh
GUARD=${GUARD:-0.82}
P=holdout
step() { printf "\n=== %s\n" "$1  $(date '+%H:%M:%S')"; }
guard() { step "guard-$1"; $G $GUARD || { echo "STOP: usage limit"; exit 2; }; }
post() { for s in audit_runs extract_deck e2e_metrics; do step $s; $PY benchmark/scripts/$s.py --phase $P; done; }
step freeze-check; $PY benchmark/scripts/freeze_holdout.py --verify || { echo "STOP: frozen files changed"; exit 3; }
guard stage1; step "generation B E1"; $PY benchmark/scripts/run_generation.py --phase $P --conditions B E1 --parallel 4; post
guard stage2; step "generation H2a"; $PY benchmark/scripts/run_generation.py --phase $P --conditions H2a --parallel 4; post
guard evaluation
for s in normalize blind; do step $s; $PY benchmark/scripts/evaluate.py $s --phase $P; done
step judge; $PY benchmark/scripts/evaluate.py judge --phase $P --judge primary --parallel 4
guard fidelity; for s in units check; do step $s; $PY benchmark/scripts/explore_holdout.py $s --parallel 4; done
guard pairwise; for s in pairwise analyse; do step $s; $PY benchmark/scripts/explore_holdout.py $s --parallel 4; done
step guard-after; $G 1.0
step done
