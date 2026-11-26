"""Shared helpers: paths, config, a clean environment, and headless Claude Code calls."""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import time

BENCH = pathlib.Path(__file__).resolve().parents[1]
REPO = BENCH.parent
# HYM_BENCH_CONFIG: a phase with its own config file (e.g. config/speed.json), so it does not touch experiment.json
CONFIG = json.loads((BENCH / os.environ.get("HYM_BENCH_CONFIG", "config/experiment.json")).read_text())

# Variables a parent Claude Code session sets; a child session must not inherit them.
PARENT_VARS = ["CLAUDECODE", "CLAUDE_CODE_SESSION_ID", "CLAUDE_CODE_CHILD_SESSION", "CLAUDE_CODE_MESSAGING_SOCKET",
               "CLAUDE_CODE_MESSAGING_TOKEN", "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_PID", "CLAUDE_EFFORT",
               "CLAUDE_CODE_SESSION_ATTENDED", "AI_AGENT", "CLAUDE_CODE_EXECPATH"]


def claude_bin() -> str:
    return shutil.which("claude") or str(pathlib.Path.home() / ".local/bin/claude")


def claude_version() -> str:
    try:
        return subprocess.run([claude_bin(), "--version"], capture_output=True, text=True, timeout=60).stdout.strip()
    except Exception as e:  # pragma: no cover
        return f"unknown ({e})"


def clean_env(path_prefix: str | None = None, extra: dict | None = None) -> dict:
    env = {k: v for k, v in os.environ.items() if k not in PARENT_VARS}
    env["CLAUDE_CODE_DISABLE_AUTO_MEMORY"] = "1"
    if path_prefix:
        env["PATH"] = path_prefix + os.pathsep + env.get("PATH", "")
        env.pop("PYTHONHOME", None)
    if extra:
        env.update(extra)
    return env


def sha256_file(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def tree_hash(root: pathlib.Path) -> str:
    h = hashlib.sha256()
    for p in sorted(root.rglob("*")):
        if p.is_file() and "__pycache__" not in p.parts:
            h.update(str(p.relative_to(root)).encode())
            h.update(sha256_file(p).encode())
    return h.hexdigest()


def git_head() -> str:
    try:
        return subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    except Exception:
        return "unknown"


def run_claude_json(prompt: str, model: str, effort: str, schema: dict | None = None, timeout: int = 3600,
                    tools: str = "", cwd: str | None = None, retries: int = 3) -> dict:
    """One isolated, tool-less headless call. Returns the result event (with structured_output if a schema is given)."""
    args = [claude_bin(), "-p", "--model", model, "--effort", effort, "--setting-sources", "", "--strict-mcp-config",
            "--no-session-persistence", "--tools", tools, "--output-format", "json", "--disable-slash-commands"]
    if schema is not None:
        schema = {k: v for k, v in schema.items() if k != "$schema"}  # the CLI's validator rejects the meta-schema key
        args += ["--json-schema", json.dumps(schema)]
    last = None
    for attempt in range(retries):
        t0 = time.time()
        proc = subprocess.run(args, input=prompt, capture_output=True, text=True, timeout=timeout,
                              env=clean_env(), cwd=cwd or str(BENCH / "eval"))
        try:
            res = json.loads(proc.stdout)
        except json.JSONDecodeError:
            res = {"is_error": True, "result": proc.stdout[-2000:], "stderr": proc.stderr[-2000:]}
        res["_wall_s"] = time.time() - t0
        if not res.get("is_error") and (schema is None or res.get("structured_output") is not None):
            return res
        last = res
        time.sleep(30 * (attempt + 1))
    return last
