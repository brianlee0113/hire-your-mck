"""Freeze the holdout (METHODOLOGY.md §16): hashes of the design files, cases, keys and both plugin trees.

Usage: python benchmark/scripts/freeze_holdout.py            -> writes FREEZE-holdout.json (refuses to overwrite)
       python benchmark/scripts/freeze_holdout.py --verify   -> exit 1 if anything frozen changed
"""
import datetime as dt
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import BENCH, CONFIG, REPO, claude_version, git_head, sha256_file, tree_hash  # noqa: E402

FP = BENCH / "FREEZE-holdout.json"
CASES = CONFIG["phases"]["holdout"]["cases"]
FILES = (["METHODOLOGY.md", "config/experiment.json", "env/requirements-gen.txt",
          "prompts/conditions/B_strong_baseline.md", "prompts/conditions/E1_hire_your_mck_audit.md",
          "prompts/conditions/H2a_compile_restyle.md", "prompts/conditions/task.md", "prompts/conditions/autoreply.md",
          "prompts/eval/rubric.md", "prompts/eval/judge_absolute.md", "prompts/eval/judge_pairwise_nowords.md",
          "prompts/eval/fidelity_units.md", "prompts/eval/fidelity_check_v2.md",
          "schemas/judge_absolute.schema.json", "schemas/judge_pairwise.schema.json",
          "schemas/fidelity_units.schema.json", "schemas/fidelity_check_v2.schema.json",
          "cases/build_holdout_cases.py", "cases/holdout_models.py", "cases/validate_holdout_cases.py"]
         + [f"scripts/{s}" for s in ("run_generation.py", "common.py", "audit_runs.py", "extract_deck.py", "e2e_metrics.py",
                                     "evaluate.py", "analyze.py", "explore_h1.py", "explore_holdout.py", "run_holdout.sh",
                                     "usage_guard.sh", "freeze_holdout.py")]
         + [f"cases/{c}/packet.md" for c in CASES]
         + [f"answer_keys/{c}{ext}" for c in CASES for ext in (".json", ".md", ".calc.json")])
TREES = {"plugin (H2a)": REPO / "plugin", "env/plugin-E1 (E1)": BENCH / "env" / "plugin-E1"}


def current():
    return {"files": {f: sha256_file(BENCH / f) for f in FILES},
            "plugin_trees": {k: tree_hash(p) for k, p in TREES.items()}}


def main():
    if "--verify" in sys.argv:
        frozen, now = json.loads(FP.read_text()), current()
        changed = [k for k, v in frozen["files"].items() if now["files"].get(k) != v]
        changed += [k for k, v in frozen["plugin_trees"].items() if now["plugin_trees"].get(k) != v]
        print("freeze check:", "changed " + ", ".join(changed) if changed else "nothing changed")
        sys.exit(1 if changed else 0)
    if FP.exists():
        sys.exit(f"{FP.name} exists; a freeze is not rewritten (record a deviation instead)")
    rec = {"frozen_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
           "scope": "holdout (METHODOLOGY §16): B, E1, H2a-restyle on c6-c11, recorded before the first holdout run",
           "repo_head": git_head(), "claude_code_version": claude_version(), **current()}
    FP.write_text(json.dumps(rec, indent=1) + "\n")
    print(f"froze {len(rec['files'])} files and {len(rec['plugin_trees'])} plugin trees at {rec['frozen_at']}")


if __name__ == "__main__":
    main()
