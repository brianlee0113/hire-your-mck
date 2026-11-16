"""Evaluation pipeline: normalise → blind → judge (absolute, two models) → judge (pairwise).

Usage:
  python benchmark/scripts/evaluate.py normalize --phase pilot
  python benchmark/scripts/evaluate.py blind     --phase pilot
  python benchmark/scripts/evaluate.py judge     --phase pilot --judge primary|secondary
  python benchmark/scripts/evaluate.py pairwise  --phase pilot
  python benchmark/scripts/evaluate.py all       --phase pilot

Every model call is a fresh, tool-less, settings-free headless session with no memory and no access to the run's
condition. Judges see only the blind id, the briefing pack, the answer key and the anonymised document.
Outputs that already exist are never regenerated (delete a file to force it).
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import pathlib
import random
import re
import sys
import threading

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import BENCH, CONFIG, run_claude_json  # noqa: E402

LOCK = threading.Lock()
PROMPTS = BENCH / "prompts" / "eval"
SCHEMAS = BENCH / "schemas"


def log(m):
    with LOCK:
        print(m, flush=True)


def runs(phase):
    out = []
    for d in sorted((BENCH / "runs" / phase).glob(f"{phase}-*")):
        if (d / "meta.json").exists():
            out.append((d, json.loads((d / "meta.json").read_text())))
    return out


# ---------------------------------------------------------------------------------------------- normalise
WORD = re.compile(r"[a-z0-9$%.,'’-]+")


def toks(s):
    return [t.strip(".,") for t in WORD.findall(s.lower()) if t.strip(".,")]


def fidelity(norm: dict, deck_text: str) -> dict:
    """Share of extracted strings whose word trigrams (or words, for short strings) appear in the deck text."""
    dt = toks(deck_text)
    tri = set(zip(dt, dt[1:], dt[2:]))
    uni = set(dt)
    strings = []
    if norm.get("governing_thought"):
        strings.append(norm["governing_thought"])
    strings += norm.get("executive_summary", [])
    for s in norm.get("slides", []):
        strings.append(s["title"])
        for c in s["claims"]:
            strings.append(c["claim"])
            strings += c["evidence"]
    if norm.get("recommendation"):
        strings.append(norm["recommendation"])
    scores = []
    for s in strings:
        t = [x for x in toks(s.replace("[from image]", "")) if x]
        if not t:
            continue
        if len(t) < 3:
            scores.append(sum(x in uni for x in t) / len(t))
        else:
            g = list(zip(t, t[1:], t[2:]))
            scores.append(sum(x in tri for x in g) / len(g))
    n = len(scores)
    return {"n_strings": n, "mean_overlap": sum(scores) / n if n else None,
            "share_ge_0_8": sum(s >= 0.8 for s in scores) / n if n else None,
            "share_lt_0_5": sum(s < 0.5 for s in scores) / n if n else None}


def normalize_one(run_dir, meta):
    out_p = run_dir / "normalized.json"
    if out_p.exists():
        return
    deck = json.loads((run_dir / "extract" / "deck.json").read_text())
    text = (run_dir / "extract" / "deck.txt").read_text()
    if not text.strip():
        out_p.write_text(json.dumps({"normalized": None, "error": deck.get("error", "empty deliverable")}, indent=1))
        log(f"{run_dir.name}: nothing to normalise ({deck.get('error')})")
        return
    prompt = (PROMPTS / "normalize.md").read_text().replace("{deck_text}", text)
    tools, cwd = "", None
    if deck.get("n_pictures"):
        tools, cwd = "Read", str(run_dir / "extract" / "images")
        files = sorted(p.name for p in (run_dir / "extract" / "images").glob("*"))
        prompt += ("\n\nThe deck's pictures are in the current directory; view them with the Read tool: " + ", ".join(files))
    schema = json.loads((SCHEMAS / "normalized_storyline.schema.json").read_text())
    nc = CONFIG["normalizer"]
    res = run_claude_json(prompt, nc["model"], nc["effort"], schema, tools=tools, cwd=cwd)
    norm = res.get("structured_output")
    if norm is None:
        (run_dir / "normalized.error.json").write_text(json.dumps(res, indent=1, default=str)[:20000])
        log(f"{run_dir.name}: normalisation FAILED (see normalized.error.json)")
        return
    rec = {"normalized": norm, "model": nc["model"], "effort": nc["effort"], "cost_usd": res.get("total_cost_usd"),
           "wall_s": res.get("_wall_s"), "is_error": res.get("is_error"),
           "fidelity": fidelity(norm, text) if norm else None}
    out_p.write_text(json.dumps(rec, indent=1, ensure_ascii=False))
    log(f"{run_dir.name}: normalised · fidelity {rec['fidelity']}")


# ---------------------------------------------------------------------------------------------- blind
SCRUB = [
    (re.compile(r"ILLUSTRATIVE\s*[—-]\s*DATA NEEDED", re.I), ""),
    (re.compile(r"hire[- ]?your[- ]?mck|\bMcK\b|McKinsey", re.I), "[tool]"),
    (re.compile(r"\b[\w-]+-sources\.xlsx\b", re.I), "[source workbook]"),
    (re.compile(r"\bBACKUP:\s*"), "Backup: "),
]
TREE_CODE = re.compile(r"^(\[Title\]\s*)\d{1,2}[a-z]?\s*[:·]\s+", re.M)
PAGE_NUM = re.compile(r"^\s*-\s*\d{1,3}\s*$", re.M)
# navigation leftovers: page references ("p. 5–8"), lone node-code badges ("1a"), section trackers ("1 Demand    2 Unit economics ...")
NAV = [re.compile(r"^\s*-\s*p\.\s*[\d,–\- ]+\s*$", re.M), re.compile(r"^\s*-\s*\d{1,2}[a-z]\s*$", re.M),
       re.compile(r"^\s*-\s*(?:\d{1,2}\s+[A-Z][^\n]{1,30}?\s{3,}){2,}[^\n]*$", re.M)]


def scrub(t: str) -> str:
    for pat, rep in SCRUB:
        t = pat.sub(rep, t)
    t = TREE_CODE.sub(r"\1", t)
    t = PAGE_NUM.sub("", t)
    for pat in NAV:
        t = pat.sub("", t)
    return re.sub(r"\n{3,}", "\n\n", t)


def strip_code(s):
    return re.sub(r"^\d{1,2}[a-z]?\s*[:·]\s+", "", s or "")


def render_doc(norm, deck_text):
    L = ["## Part 1 · Normalised storyline", ""]
    if norm is None:
        L += ["(The run produced no readable deliverable.)", ""]
    else:
        L += [f"**Governing thought:** {norm.get('governing_thought') or '(none stated)'}", "", "**Executive summary:**"]
        L += [f"{i}. {x}" for i, x in enumerate(norm.get("executive_summary") or [], 1)] or ["(none)"]
        L += ["", "**Slides (title → claims → evidence):**", ""]
        for s in norm.get("slides", []):
            L.append(f"- Slide {s['n']}: {strip_code(s['title'])}")
            for c in s["claims"]:
                L.append(f"  - Claim: {c['claim']}")
                for e in c["evidence"]:
                    L.append(f"    - Evidence: {e}")
        L += ["", f"**Recommendation:** {norm.get('recommendation') or '(none stated)'}", "", "**Alternatives considered:**"]
        L += [f"- {a['option']}: {a['treatment']}" for a in norm.get("alternatives_considered") or []] or ["(none)"]
        L += ["", "**Assumptions and uncertainties:**"] + ([f"- {x}" for x in norm.get("assumptions_and_uncertainties") or []] or ["(none)"])
        L += ["", "**Next steps:**"] + ([f"- {x}" for x in norm.get("next_steps") or []] or ["(none)"])
    L += ["", "## Part 2 · Full slide text (mechanical extraction)", "", deck_text or "(empty)"]
    return scrub("\n".join(L))


def blind(phase):
    out = BENCH / "eval" / phase
    (out / "blinded").mkdir(parents=True, exist_ok=True)
    key_p = out / "blinding_key.json"
    key = json.loads(key_p.read_text()) if key_p.exists() else {}
    rng = random.Random(CONFIG["seeds"]["blinding"] + (0 if phase == "main" else 1))
    used = set(key)
    by_run = {v: k for k, v in key.items()}
    rs = runs(phase)
    rng.shuffle(rs)
    for run_dir, meta in rs:
        if run_dir.name in by_run:
            continue
        while True:
            bid = "D" + "".join(rng.choice("ABCDEFGHJKLMNPQRSTUVWXYZ23456789") for _ in range(5))
            if bid not in used:
                break
        used.add(bid)
        key[bid] = run_dir.name
    for bid, rid in key.items():
        run_dir = BENCH / "runs" / phase / rid
        np_ = run_dir / "normalized.json"
        if not np_.exists():
            continue
        norm = json.loads(np_.read_text()).get("normalized")
        deck_text = (run_dir / "extract" / "deck.txt").read_text()
        doc = render_doc(norm, deck_text)
        words = json.loads((run_dir / "extract" / "deck.json").read_text()).get("words", 0)
        (out / "blinded" / f"{bid}.md").write_text(doc)
        (out / "blinded" / f"{bid}.json").write_text(json.dumps({"blind_id": bid, "case": json.loads((run_dir / "meta.json").read_text())["case"], "words": words}))
    key_p.write_text(json.dumps(dict(sorted(key.items())), indent=1))
    log(f"blinded {len(key)} documents → {out / 'blinded'}")


# ---------------------------------------------------------------------------------------------- judges
def packet(case):
    return (BENCH / "cases" / case / "packet.md").read_text()


def answer_key(case):
    return (BENCH / "answer_keys" / f"{case}.json").read_text()


def judge_one(phase, which, bid):
    jc = CONFIG["judges"][which]
    out = BENCH / "eval" / phase / "auto" / jc["model"]
    out.mkdir(parents=True, exist_ok=True)
    p = out / f"{bid}.json"
    if p.exists():
        return
    info = json.loads((BENCH / "eval" / phase / "blinded" / f"{bid}.json").read_text())
    doc = (BENCH / "eval" / phase / "blinded" / f"{bid}.md").read_text()
    prompt = ((PROMPTS / "judge_absolute.md").read_text()
              .replace("{rubric}", (PROMPTS / "rubric.md").read_text())
              .replace("{packet}", packet(info["case"])).replace("{answer_key}", answer_key(info["case"]))
              .replace("{blind_id}", bid).replace("{words}", str(info["words"])).replace("{document}", doc))
    schema = json.loads((SCHEMAS / "judge_absolute.schema.json").read_text())
    res = run_claude_json(prompt, jc["model"], jc["effort"], schema)
    if not res.get("structured_output"):
        (out / f"{bid}.error.json").write_text(json.dumps(res, indent=1, default=str)[:20000])
        log(f"judge {jc['model']} {bid}: ERROR")
        return
    p.write_text(json.dumps({"blind_id": bid, "judge": jc, "output": res.get("structured_output"), "cost_usd": res.get("total_cost_usd"),
                             "wall_s": res.get("_wall_s"), "is_error": res.get("is_error"),
                             "error_text": None if res.get("structured_output") else str(res.get("result"))[:2000]}, indent=1, ensure_ascii=False))
    log(f"judge {jc['model']} {bid}: {'ok' if res.get('structured_output') else 'ERROR'}")


def judge(phase, which, parallel):
    bids = sorted(p.stem for p in (BENCH / "eval" / phase / "blinded").glob("*.md"))
    with cf.ThreadPoolExecutor(parallel) as ex:
        list(ex.map(lambda b: judge_one(phase, which, b), bids))


def pairwise(phase, parallel):
    key = json.loads((BENCH / "eval" / phase / "blinding_key.json").read_text())
    by = {}
    for bid, rid in key.items():
        m = json.loads((BENCH / "runs" / phase / rid / "meta.json").read_text())
        by[(m["case"], m["condition"], m["rep"])] = bid
    rng = random.Random(CONFIG["seeds"]["pairwise"])
    jobs = []
    for (case, cond, rep), bid in sorted(by.items()):
        if cond != "A":
            continue
        trio = {c: by.get((case, c, rep)) for c in ("A", "B", "C")}
        for a, b in (("A", "C"), ("B", "C"), ("A", "B")):
            if trio[a] and trio[b]:
                first = rng.random() < 0.5
                pair = (trio[a], trio[b]) if first else (trio[b], trio[a])
                jobs += [(case, pair[0], pair[1]), (case, pair[1], pair[0])]  # both orders
    jc = CONFIG["judges"]["pairwise"]
    out = BENCH / "eval" / phase / "pairwise" / jc["model"]
    out.mkdir(parents=True, exist_ok=True)
    schema = json.loads((SCHEMAS / "judge_pairwise.schema.json").read_text())

    def one(job):
        case, x, y = job
        p = out / f"{x}__{y}.json"
        if p.exists():
            return
        bx = BENCH / "eval" / phase / "blinded"
        prompt = ((PROMPTS / "judge_pairwise.md").read_text().replace("{packet}", packet(case)).replace("{answer_key}", answer_key(case))
                  .replace("{doc_x}", (bx / f"{x}.md").read_text()).replace("{doc_y}", (bx / f"{y}.md").read_text())
                  .replace("{words_x}", str(json.loads((bx / f"{x}.json").read_text())["words"]))
                  .replace("{words_y}", str(json.loads((bx / f"{y}.json").read_text())["words"])))
        res = run_claude_json(prompt, jc["model"], jc["effort"], schema)
        if not res.get("structured_output"):
            (out / f"{x}__{y}.error.json").write_text(json.dumps(res, indent=1, default=str)[:20000])
            log(f"pairwise {x} vs {y}: ERROR")
            return
        p.write_text(json.dumps({"x": x, "y": y, "case": case, "judge": jc, "output": res.get("structured_output"),
                                 "cost_usd": res.get("total_cost_usd"), "wall_s": res.get("_wall_s"),
                                 "error_text": None if res.get("structured_output") else str(res.get("result"))[:2000]}, indent=1, ensure_ascii=False))
        log(f"pairwise {x} vs {y}: {'ok' if res.get('structured_output') else 'ERROR'}")

    with cf.ThreadPoolExecutor(parallel) as ex:
        list(ex.map(one, jobs))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["normalize", "blind", "judge", "pairwise", "all"])
    ap.add_argument("--phase", required=True)
    ap.add_argument("--judge", default="primary", choices=["primary", "secondary"])
    ap.add_argument("--parallel", type=int, default=4)
    a = ap.parse_args()
    if a.step in ("normalize", "all"):
        with cf.ThreadPoolExecutor(a.parallel) as ex:
            list(ex.map(lambda rm: normalize_one(*rm), [(d, m) for d, m in runs(a.phase) if (d / "extract" / "deck.json").exists()]))
    if a.step in ("blind", "all"):
        blind(a.phase)
    if a.step == "judge":
        judge(a.phase, a.judge, a.parallel)
    if a.step == "all":
        judge(a.phase, "primary", a.parallel)
        judge(a.phase, "secondary", a.parallel)
    if a.step in ("pairwise", "all"):
        pairwise(a.phase, a.parallel)


if __name__ == "__main__":
    main()
