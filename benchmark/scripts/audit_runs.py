"""Audit every run's transcript for isolation breaches and record what each session actually did.

Flags: any tool call that touches this repository, ~/.claude, another run's workspace or the answer keys; network
attempts (curl, wget, pip install); sandbox or permission denials. Also records whether the Hire Your McK skill text
reached the session (it must for C and must not for A/B), subagent use and the models that served the session.

Usage: python benchmark/scripts/audit_runs.py --phase pilot
Writes runs/<phase>/<run_id>/audit.json and runs/<phase>/audit-summary.json
"""
from __future__ import annotations

import argparse
import gzip
import json
import os
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import BENCH, CONFIG, REPO  # noqa: E402

HOME = str(pathlib.Path.home())
PAT_REPO = re.compile(re.escape(str(REPO)) + r"|answer_key|/\.claude/(?!shell-snapshots)|hym-bench-work/ws/|hymwork/ws/(?!{run})")
PAT_NET = re.compile(r"\bcurl\b|\bwget\b|pip3? install|uv pip install|npm install|allowed_domains|https?://", re.I)
SKILL_MARK = re.compile(r"You turn research, notes or a single message into a consulting-grade deck|deck_deep|storyline spec", re.I)


def audit(run_dir: pathlib.Path):
    meta = json.loads((run_dir / "meta.json").read_text())
    rid = meta["run_id"]
    flags = {"repo_or_key_access": [], "network_attempts": [], "sandbox_denials": 0, "permission_denials": 0}
    tools, skill_seen, subagents, n_events = {}, False, 0, 0
    pat_repo = re.compile(PAT_REPO.pattern.replace("{run}", re.escape(rid)))
    full = [p for p in sorted(run_dir.glob("transcript-attempt*.jsonl.gz")) if not p.name.endswith(".slim.jsonl.gz")]
    for tp in full or sorted(run_dir.glob("transcript-attempt*.slim.jsonl.gz")):  # slim copies when the full ones are absent
        for line in gzip.open(tp, "rt"):
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            n_events += 1
            msg = ev.get("message") if isinstance(ev.get("message"), dict) else {}
            content = msg.get("content") if isinstance(msg.get("content"), list) else []
            if isinstance(msg.get("content"), str) and SKILL_MARK.search(msg["content"]):
                skill_seen = True
            for b in content:
                if b.get("type") == "tool_use":
                    tools[b["name"]] = tools.get(b["name"], 0) + 1
                    if b["name"] in ("Task", "Agent"):
                        subagents += 1
                    s = json.dumps(b.get("input", {}))
                    # the session's own spill-over files (large tool outputs) live under ~/.claude/projects/<this run's cwd>/
                    s = re.sub(r"/[^\s\"'\\]+", lambda m: os.path.normpath(m.group(0)), s)  # resolve ../ before judging
                    s_chk = re.sub(r"/\.claude/projects/[^\\\"]*?ws-" + re.escape(rid) + r"/[^\\\"]*", "<own-session-file>", s)
                    if pat_repo.search(s_chk):
                        flags["repo_or_key_access"].append(s[:300])
                    if b["name"] == "Bash" and PAT_NET.search(s):
                        flags["network_attempts"].append(s[:300])
                elif b.get("type") == "tool_result":
                    s = json.dumps(b.get("content"))
                    if "sandbox_violations" in s or "Operation not permitted" in s:
                        flags["sandbox_denials"] += 1
                    if SKILL_MARK.search(s):
                        skill_seen = True
                elif b.get("type") == "text" and ev.get("type") == "user" and SKILL_MARK.search(b.get("text", "")):
                    skill_seen = True
    for a in meta["attempts"]:
        for t in a["turns"]:
            flags["permission_denials"] += len((t["result"] or {}).get("permission_denials") or [])
    init_skills = []
    for a in meta["attempts"]:
        for t in a["turns"]:
            init_skills = (t.get("init") or {}).get("skills") or init_skills
    rec = {"run_id": rid, "condition": meta["condition"], "status": meta["status"], "events": n_events, "tools": tools,
           "subagent_calls": subagents, "skill_available": any("hire-your-mck" in s for s in init_skills),
           "skill_text_seen": skill_seen, "models_used": list(meta.get("models_used", {})), "flags": flags,
           "clean": not flags["repo_or_key_access"] and CONFIG["conditions"][meta["condition"]]["plugin"] == any("hire-your-mck" in s for s in init_skills)}
    (run_dir / "audit.json").write_text(json.dumps(rec, indent=1))
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", required=True)
    a = ap.parse_args()
    out = []
    for d in sorted((BENCH / "runs" / a.phase).glob(f"{a.phase}-*")):
        if (d / "meta.json").exists():
            r = audit(d)
            out.append(r)
            print(f"{r['run_id']}: {r['status']:<16} clean={r['clean']} skill={r['skill_available']}/{r['skill_text_seen']} "
                  f"subagents={r['subagent_calls']} net={len(r['flags']['network_attempts'])} "
                  f"repo={len(r['flags']['repo_or_key_access'])} sandbox={r['flags']['sandbox_denials']} models={r['models_used']}")
    (BENCH / "runs" / a.phase / "audit-summary.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
