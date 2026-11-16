"""Run the generation phase: every (case, condition, replicate) job in a fixed, seeded random order.

Usage:
  python benchmark/scripts/run_generation.py --phase pilot [--parallel 3] [--work-root DIR] [--only RUN_ID ...]
  python benchmark/scripts/run_generation.py --phase main --dry-run      # print the schedule only

Each job runs in a fresh, isolated workspace that holds only the evidence packet. Every condition gets the same
model, effort, tools, Python environment and sandbox (no network, no access to this repository, ~/.claude or other
runs). Condition C additionally loads the Hire Your McK plugin from a frozen snapshot. Nothing is rerun once a
model has produced output: only infrastructure failures (API errors, usage limits) are retried, and every attempt
is preserved under runs/<phase>/<run_id>/.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import datetime as dt
import gzip
import json
import os
import pathlib
import random
import re
import shutil
import subprocess
import sys
import threading
import time
import uuid

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import BENCH, CONFIG, REPO, claude_bin, claude_version, clean_env, git_head, sha256_file, sha256_text, tree_hash  # noqa: E402

LOCK = threading.Lock()
CODE = {"c1-market-entry": "c1", "c2-profitability": "c2", "c3-ai-assistant": "c3", "c4-pricing-churn": "c4",
        "c5-negative-entry": "c5"}


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def log(msg):
    with LOCK:
        print(f"[{dt.datetime.now():%H:%M:%S}] {msg}", flush=True)


# ---------------------------------------------------------------------------------------------- setup
def schedule(phase: str):
    ph = CONFIG["phases"][phase]
    jobs = [{"run_id": f"{phase}-{CODE[c]}-{k}-r{r}", "case": c, "condition": k, "rep": r}
            for c in ph["cases"] for k in ph.get("conditions", list(CONFIG["conditions"])) for r in range(1, ph["reps"] + 1)]
    rng = random.Random(CONFIG["seeds"][f"{phase}_order"])
    rng.shuffle(jobs)
    for i, j in enumerate(jobs):
        j["order"] = i
    return jobs


def ensure_env(work_root: pathlib.Path) -> pathlib.Path:
    venv = work_root / "_env" / "venv-gen"
    py = venv / "bin" / "python"
    if not py.exists():
        log(f"creating generation venv at {venv}")
        subprocess.run(["uv", "venv", "--python", "3.14", str(venv)], check=True)
        subprocess.run(["uv", "pip", "install", "--python", str(py), "-r", str(BENCH / "env" / "requirements-gen.txt")], check=True)
    # `python` and `python3` both resolve to the venv
    for name in ("python3", "python"):
        link = venv / "bin" / name
        if not link.exists():
            link.symlink_to(py.resolve())
    return venv / "bin"


def ensure_plugin_snapshot(work_root: pathlib.Path) -> tuple[pathlib.Path, str]:
    src = REPO / "plugin"
    h = tree_hash(src)
    dst = work_root / "_plugin" / f"hire-your-mck-{h[:12]}"
    if not dst.exists():
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", ".DS_Store"))
    return dst, h


def sandbox_settings(work_root: pathlib.Path, run_dir: pathlib.Path, all_runs: list[str]) -> dict:
    home = pathlib.Path.home()
    # ~/.claude holds transcripts of other sessions, installed plugins (incl. hire-your-mck) and user instructions.
    # Deny all of it except the shell snapshots the Bash tool sources (denying those breaks PATH in the sandbox).
    claude_home = [str(p) for p in sorted((home / ".claude").iterdir()) if p.name not in ("shell-snapshots",)]
    others = {str(work_root / "ws" / r) for r in all_runs}
    if (work_root / "ws").exists():
        others |= {str(p) for p in (work_root / "ws").iterdir()}
    others.discard(str(run_dir))
    deny_paths = [str(REPO)] + claude_home + sorted(others)
    deny_rules = []
    for p in deny_paths:
        deny_rules += [f"Read(/{p}/**)", f"Edit(/{p}/**)", f"Write(/{p}/**)"]
    return {
        "sandbox": {"enabled": True, "autoAllowBashIfSandboxed": True, "allowUnsandboxedCommands": False,
                    "network": {"allowedDomains": []}, "filesystem": {"denyRead": deny_paths}},
        "permissions": {"deny": deny_rules + ["WebFetch", "WebSearch"]},
    }


def build_prompt(job) -> str:
    case = CONFIG["cases"][job["case"]]
    task = (BENCH / CONFIG["task_template"]).read_text().strip().format(**case)
    tmpl = (BENCH / CONFIG["conditions"][job["condition"]]["prompt"]).read_text().strip()
    return tmpl.replace("{task}", task)


# ---------------------------------------------------------------------------------------------- one turn
def claude_turn(args, prompt, cwd, env, transcript, timeout):
    """Run one headless turn, streaming events into the transcript. Returns (init, result, last_text, timed_out)."""
    init, result, last_text = None, None, ""
    t0 = time.time()
    with open(transcript, "a") as tf:
        proc = subprocess.Popen(args, cwd=cwd, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True)
        proc.stdin.write(prompt)
        proc.stdin.close()
        timed_out = False
        killer = threading.Timer(timeout, lambda: proc.kill())
        killer.start()
        try:
            for line in proc.stdout:
                tf.write(line)
                try:
                    ev = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if ev.get("type") == "system" and ev.get("subtype") == "init":
                    init = ev
                elif ev.get("type") == "result":
                    result = ev
                elif ev.get("type") == "assistant" and not ev.get("parent_tool_use_id"):
                    for b in ev.get("message", {}).get("content", []):
                        if b.get("type") == "text" and b.get("text", "").strip():
                            last_text = b["text"]
            proc.wait()
        finally:
            killer.cancel()
        if time.time() - t0 >= timeout - 1:
            timed_out = True
        err = proc.stderr.read()
        if err.strip():
            tf.write(json.dumps({"type": "harness_stderr", "text": err[-4000:]}) + "\n")
    return init, result, last_text, timed_out, time.time() - t0


INFRA_PAT = re.compile(r"rate.?limit|usage limit|overloaded|529|5\d\d |api error|connection|ECONN|timed out|credit", re.I)


def is_infra_failure(result, last_text) -> bool:
    if result is None:
        return True
    if result.get("is_error") and (result.get("api_error_status") or INFRA_PAT.search(str(result.get("result", "")))):
        return True
    return False


def deliverable_state(ws: pathlib.Path, last_text: str):
    files = [p for p in (ws / "deliverable").rglob("*") if p.is_file() and p.stat().st_size > 0]
    pptx = [p for p in files if p.suffix.lower() == ".pptx"]
    tail = (last_text or "")[-500:]
    asking = "?" in tail
    if pptx:
        return "complete", files
    if files and not asking:
        return "complete_no_pptx", files
    return "incomplete", files


# ---------------------------------------------------------------------------------------------- one job
def run_job(job, phase, work_root, venv_bin, plugin_dir, plugin_hash, all_runs):
    run_id = job["run_id"]
    out = BENCH / "runs" / phase / run_id
    meta_p = out / "meta.json"
    if meta_p.exists() and json.loads(meta_p.read_text()).get("status") != "infra_failure":
        log(f"{run_id}: already done, skipping")
        return json.loads(meta_p.read_text())
    out.mkdir(parents=True, exist_ok=True)
    cfg = CONFIG
    attempts = []
    for attempt in range(1, cfg["limits"]["max_infra_retries"] + 2):
        ws = work_root / "ws" / run_id
        if ws.exists():
            # keep the previous attempt's workspace with the run
            shutil.move(str(ws), str(out / f"attempt{attempt - 1}-workspace-raw"))
        (ws / "evidence").mkdir(parents=True)
        (ws / "deliverable").mkdir()
        shutil.copy(BENCH / "cases" / job["case"] / "packet.md", ws / "evidence" / "briefing-pack.md")
        settings_p = work_root / "_settings" / f"{run_id}.json"
        settings_p.parent.mkdir(parents=True, exist_ok=True)
        settings_p.write_text(json.dumps(sandbox_settings(work_root, ws, all_runs), indent=1))
        session = str(uuid.uuid4())
        env = clean_env(str(venv_bin), {"CLAUDE_CODE_SUBAGENT_MODEL": cfg["generator"]["subagent_model"]})
        base = [claude_bin(), "-p", "--model", cfg["generator"]["model"], "--effort", cfg["generator"]["effort"],
                "--setting-sources", "", "--settings", str(settings_p), "--strict-mcp-config",
                "--tools", ",".join(cfg["tools"]), "--allowedTools", " ".join(cfg["tools"]),
                "--permission-mode", "dontAsk", "--output-format", "stream-json", "--verbose",
                "--max-budget-usd", str(cfg["limits"]["max_budget_usd_per_run"])]
        if cfg["conditions"][job["condition"]]["plugin"]:
            base += ["--plugin-dir", str(plugin_dir)]
        transcript = out / f"transcript-attempt{attempt}.jsonl"
        prompt = build_prompt(job)
        autoreply = (BENCH / cfg["autoreply"]).read_text().strip()
        turns, status, started = [], None, now()
        log(f"{run_id}: attempt {attempt} start (order {job['order']})")
        for turn in range(cfg["limits"]["max_autoreplies"] + 1):
            args = base + (["--session-id", session] if turn == 0 else ["--resume", session])
            init, result, last_text, timed_out, wall = claude_turn(args, prompt if turn == 0 else autoreply, str(ws), env,
                                                                   transcript, cfg["limits"]["turn_timeout_s"])
            turns.append({"turn": turn, "prompt": "task" if turn == 0 else "autoreply", "wall_s": round(wall, 1),
                          "timed_out": timed_out, "init": {k: (init or {}).get(k) for k in ("model", "tools", "skills", "plugins", "claude_code_version", "permissionMode")},
                          "result": {k: (result or {}).get(k) for k in ("subtype", "is_error", "num_turns", "duration_ms", "duration_api_ms",
                                                                      "total_cost_usd", "usage", "modelUsage", "stop_reason", "terminal_reason",
                                                                      "api_error_status", "permission_denials", "subagent_stats")},
                          "result_text_tail": str((result or {}).get("result", ""))[-1500:]})
            if is_infra_failure(result, last_text) and not any(t["result"].get("num_turns") for t in turns[:-1]):
                status = "infra_failure"
                break
            state, files = deliverable_state(ws, last_text or str((result or {}).get("result", "")))
            if timed_out:
                status = "timeout"
                break
            if (result or {}).get("subtype") == "error_max_budget_usd":
                status = state if state != "incomplete" else "budget_exhausted"
                break
            if state != "incomplete":
                status = state
                break
            status = "incomplete"
            if (result or {}).get("is_error"):
                break
        attempts.append({"attempt": attempt, "status": status, "turns": turns, "started": started, "ended": now(),
                         "session_id": session, "transcript": transcript.name})
        if status == "infra_failure" and attempt <= cfg["limits"]["max_infra_retries"]:
            log(f"{run_id}: infrastructure failure, waiting {cfg['limits']['infra_retry_wait_s']}s before retry")
            time.sleep(cfg["limits"]["infra_retry_wait_s"])
            continue
        break
    # copy the workspace (minus the evidence packet) into the repo
    dst = out / "workspace"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(ws, dst, ignore=shutil.ignore_patterns("evidence", "__pycache__", ".DS_Store"))
    for tp in out.glob("transcript-attempt*.jsonl"):
        with open(tp, "rb") as f, gzip.open(str(tp) + ".gz", "wb") as g:
            shutil.copyfileobj(f, g)
    final = attempts[-1]
    tot = {"cost_usd": 0.0, "duration_s": 0.0, "api_s": 0.0, "turns": 0, "input_tokens": 0, "output_tokens": 0,
           "cache_read_tokens": 0, "cache_creation_tokens": 0}
    models_used = {}
    for t in final["turns"]:
        r = t["result"] or {}
        tot["cost_usd"] += r.get("total_cost_usd") or 0
        tot["duration_s"] += t["wall_s"]
        tot["api_s"] += (r.get("duration_api_ms") or 0) / 1000
        tot["turns"] += r.get("num_turns") or 0
        u = r.get("usage") or {}
        tot["input_tokens"] += u.get("input_tokens") or 0
        tot["output_tokens"] += u.get("output_tokens") or 0
        tot["cache_read_tokens"] += u.get("cache_read_input_tokens") or 0
        tot["cache_creation_tokens"] += u.get("cache_creation_input_tokens") or 0
        for m, mu in (r.get("modelUsage") or {}).items():
            agg = models_used.setdefault(m, {"cost_usd": 0.0, "input": 0, "output": 0, "cache_read": 0, "cache_creation": 0})
            agg["cost_usd"] += mu.get("costUSD") or 0
            agg["input"] += mu.get("inputTokens") or 0
            agg["output"] += mu.get("outputTokens") or 0
            agg["cache_read"] += mu.get("cacheReadInputTokens") or 0
            agg["cache_creation"] += mu.get("cacheCreationInputTokens") or 0
    tot["cost_all_attempts_usd"] = sum((t["result"] or {}).get("total_cost_usd") or 0 for a in attempts for t in a["turns"])
    files = sorted(p for p in dst.rglob("*") if p.is_file())
    meta = {**job, "phase": phase, "status": final["status"], "attempts": attempts, "totals": tot, "models_used": models_used,
            "autoreplies_used": max(0, len(final["turns"]) - 1), "prompt": build_prompt(job), "prompt_sha256": sha256_text(build_prompt(job)),
            "generator": CONFIG["generator"], "tools": CONFIG["tools"], "claude_code_version": claude_version(),
            "plugin_snapshot_sha256": plugin_hash if CONFIG["conditions"][job["condition"]]["plugin"] else None,
            "repo_head": git_head(), "packet_sha256": sha256_file(BENCH / "cases" / job["case"] / "packet.md"),
            "files": [{"path": str(p.relative_to(out)), "bytes": p.stat().st_size, "sha256": sha256_file(p)} for p in files]}
    meta_p.write_text(json.dumps(meta, indent=1))
    for tp in out.glob("transcript-attempt*.jsonl"):
        tp.unlink()
    log(f"{run_id}: {final['status']} · ${tot['cost_usd']:.2f} · {tot['duration_s']/60:.1f} min · {len(files)} files")
    return meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", required=True, choices=list(CONFIG["phases"]))
    ap.add_argument("--parallel", type=int, default=CONFIG["parallel"])
    ap.add_argument("--work-root", default=os.environ.get("HYM_BENCH_WORK", str(pathlib.Path.home() / "hym-bench-work")))
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    jobs = schedule(a.phase)
    (BENCH / "runs" / a.phase).mkdir(parents=True, exist_ok=True)
    sched_p = BENCH / "runs" / a.phase / "schedule.json"
    if not sched_p.exists():
        sched_p.write_text(json.dumps({"seed": CONFIG["seeds"][f"{a.phase}_order"], "created": now(), "jobs": jobs}, indent=1))
    if a.dry_run:
        for j in jobs:
            print(j["order"], j["run_id"])
        return
    work_root = pathlib.Path(a.work_root).resolve()
    work_root.mkdir(parents=True, exist_ok=True)
    venv_bin = ensure_env(work_root)
    plugin_dir, plugin_hash = ensure_plugin_snapshot(work_root)
    env_info = {"created": now(), "claude_code_version": claude_version(), "repo_head": git_head(), "work_root": str(work_root),
                "plugin_snapshot": str(plugin_dir), "plugin_sha256": plugin_hash, "python_gen": str(venv_bin / "python"),
                "gen_packages": subprocess.run(["uv", "pip", "freeze", "--python", str(venv_bin / "python")], capture_output=True, text=True).stdout.split(),
                "platform": os.uname().sysname + " " + os.uname().release + " " + os.uname().machine}
    (BENCH / "runs" / a.phase / f"environment-{dt.datetime.now():%Y%m%dT%H%M%S}.json").write_text(json.dumps(env_info, indent=1))
    todo = [j for j in jobs if not a.only or j["run_id"] in a.only]
    all_runs = [j["run_id"] for j in jobs]
    log(f"{a.phase}: {len(todo)} jobs, parallel {a.parallel}, work root {work_root}")
    with cf.ThreadPoolExecutor(max_workers=a.parallel) as ex:
        futs = []
        for j in todo:  # submit in schedule order; the pool starts them in that order
            futs.append(ex.submit(run_job, j, a.phase, work_root, venv_bin, plugin_dir, plugin_hash, all_runs))
            time.sleep(2)
        for f in cf.as_completed(futs):
            try:
                f.result()
            except Exception as e:  # keep going; the failure is visible in the log
                log(f"job crashed: {e!r}")


if __name__ == "__main__":
    main()
