#!/bin/bash
# While a pipeline runs, kill a generation turn whose transcript has been silent for STALL seconds (a hang after
# the machine slept). run_generation.py then records an infrastructure failure and retries the run from scratch.
PIPE_PID=$1; PHASE=$2; STALL=${3:-720}
cd "$(dirname "$0")/.."
while kill -0 "$PIPE_PID" 2>/dev/null; do
  for d in runs/$PHASE/*/; do
    # only the newest attempt: older attempts' transcripts stay on disk with old timestamps until the run ends
    t=$(ls -t "$d"transcript-attempt*.jsonl 2>/dev/null | head -1)
    [ -n "$t" ] && [ -f "$t" ] || continue
    rid=$(basename "$d")
    age=$(( $(date +%s) - $(stat -f %m "$t") ))
    if [ "$age" -gt "$STALL" ]; then
      pid=$(pgrep -f "_settings/$rid.json" | head -1)
      if [ -n "$pid" ]; then
        echo "$(date '+%H:%M:%S') $rid silent for ${age}s: killing $pid (infra retry)"
        kill "$pid"
      fi
    fi
  done
  sleep 60
done
echo "$(date '+%H:%M:%S') pipeline ended; watchdog exits"
