#!/bin/sh
# Rebuild spec, QA, render, then list text-shown numbers on each page sheet of the workbook.
set -e
cd "$(dirname "$0")/.."
S=/Users/brianlee0113/hym-bench-work/_plugin/hire-your-mck-6f05966a12b9/skills/hire-your-mck/scripts
python3 build/build_spec.py build/boreal-exclusivity.json
python3 $S/check.py build/boreal-exclusivity.json > build/check.txt || { cat build/check.txt; exit 1; }
tail -1 build/check.txt
python3 $S/render.py build/boreal-exclusivity.json --out deliverable --theme navy
python3 build/augment_workbook.py build/boreal-exclusivity.json deliverable/boreal-exclusivity-sources.xlsx
