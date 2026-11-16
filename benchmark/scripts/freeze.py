"""Freeze the experimental design: record the SHA-256 of every design file before the main benchmark.

Usage: python benchmark/scripts/freeze.py            -> writes FREEZE.json
       python benchmark/scripts/freeze.py --verify   -> exit 1 if any frozen file changed since
"""
import datetime as dt
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import BENCH, claude_version, git_head, sha256_file, tree_hash, REPO  # noqa: E402

PATTERNS = ["METHODOLOGY.md", "config/*.json", "prompts/**/*.md", "schemas/*.json", "cases/*.py", "cases/*/packet.md",
            "answer_keys/*", "scripts/*.py", "env/*.txt"]


def files():
    out = set()
    for p in PATTERNS:
        out |= {f for f in BENCH.glob(p) if f.is_file()}
    return sorted(out)


def main():
    fp = BENCH / "FREEZE.json"
    if "--verify" in sys.argv:
        frozen = json.loads(fp.read_text())["files"]
        changed = [k for k, v in frozen.items() if not (BENCH / k).exists() or sha256_file(BENCH / k) != v]
        added = [str(f.relative_to(BENCH)) for f in files() if str(f.relative_to(BENCH)) not in frozen]
        print("changed:", changed or "none", "| added:", added or "none")
        sys.exit(1 if changed else 0)
    rec = {"frozen_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "repo_head": git_head(),
           "claude_code_version": claude_version(), "plugin_tree_sha256": tree_hash(REPO / "plugin"),
           "files": {str(f.relative_to(BENCH)): sha256_file(f) for f in files()}}
    fp.write_text(json.dumps(rec, indent=1))
    print(f"froze {len(rec['files'])} files at {rec['frozen_at']}")


if __name__ == "__main__":
    main()
