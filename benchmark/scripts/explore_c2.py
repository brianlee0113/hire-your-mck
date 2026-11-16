"""Exploratory arm C2 (METHODOLOGY.md §12): the skill in its full-deck mode, compared with the main A, B and C.

Usage (after run_generation / audit_runs / extract_deck / e2e_metrics for --phase explore-c2):
  benchmark/.venv/bin/python benchmark/scripts/explore_c2.py normalize|blind|judge|pairwise|analyse|all

· normalise: the same normaliser as the main phase (evaluate.normalize_one)
· blind:     fresh blind ids for the C2 documents, never colliding with the main phase's ids
· judge:     both absolute judges on the C2 documents (evaluate.judge_one); main judgments are reused unchanged
· pairwise:  C2 vs A, C2 vs B, C2 vs C, replicate-matched, both presentation orders, primary pairwise judge
· analyse:   results/explore-c2/{per_doc.csv,summary.json,tables.md}
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import csv
import gzip
import json
import random
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import analyze as AN  # noqa: E402
import evaluate as EV  # noqa: E402
from common import BENCH, CONFIG, run_claude_json  # noqa: E402

PHASE, MAIN = "explore-c2", "main"
EVAL, EVAL_MAIN = BENCH / "eval" / PHASE, BENCH / "eval" / MAIN
COMPS = (("C2", "A"), ("C2", "B"), ("C2", "C"))


def normalize(parallel):
    todo = [(d, m) for d, m in EV.runs(PHASE) if (d / "extract" / "deck.json").exists()]
    with cf.ThreadPoolExecutor(parallel) as ex:
        list(ex.map(lambda rm: EV.normalize_one(*rm), todo))


def blind():
    (EVAL / "blinded").mkdir(parents=True, exist_ok=True)
    key_p = EVAL / "blinding_key.json"
    key = json.loads(key_p.read_text()) if key_p.exists() else {}
    used = set(key) | set(json.loads((EVAL_MAIN / "blinding_key.json").read_text()))
    by_run = set(key.values())
    rng = random.Random(CONFIG["seeds"]["blinding"] + 2)
    rs = EV.runs(PHASE)
    rng.shuffle(rs)
    for run_dir, _ in rs:
        if run_dir.name in by_run:
            continue
        while True:
            bid = "D" + "".join(rng.choice("ABCDEFGHJKLMNPQRSTUVWXYZ23456789") for _ in range(5))
            if bid not in used:
                break
        used.add(bid)
        key[bid] = run_dir.name
    for bid, rid in key.items():
        run_dir = BENCH / "runs" / PHASE / rid
        if not (run_dir / "normalized.json").exists():
            continue
        norm = json.loads((run_dir / "normalized.json").read_text()).get("normalized")
        doc = EV.render_doc(norm, (run_dir / "extract" / "deck.txt").read_text())
        words = json.loads((run_dir / "extract" / "deck.json").read_text()).get("words", 0)
        (EVAL / "blinded" / f"{bid}.md").write_text(doc)
        (EVAL / "blinded" / f"{bid}.json").write_text(json.dumps({"blind_id": bid, "case": json.loads((run_dir / "meta.json").read_text())["case"], "words": words}))
    key_p.write_text(json.dumps(dict(sorted(key.items())), indent=1))
    print(f"blinded {len(key)} C2 documents")


def judge(parallel):
    bids = sorted(p.stem for p in (EVAL / "blinded").glob("*.md"))
    for which in ("primary", "secondary"):
        with cf.ThreadPoolExecutor(parallel) as ex:
            list(ex.map(lambda b: EV.judge_one(PHASE, which, b), bids))


def doc_index():
    """(case, condition, rep) -> (blind id, blinded dir) across both phases."""
    idx = {}
    for phase, ev in ((MAIN, EVAL_MAIN), (PHASE, EVAL)):
        for bid, rid in json.loads((ev / "blinding_key.json").read_text()).items():
            m = json.loads((BENCH / "runs" / phase / rid / "meta.json").read_text())
            if (ev / "blinded" / f"{bid}.md").exists():
                idx[(m["case"], m["condition"], m["rep"])] = (bid, ev / "blinded")
    return idx


def pairwise(parallel):
    idx = doc_index()
    rng = random.Random(CONFIG["seeds"]["pairwise"] + 2)
    jobs = []
    for (case, cond, rep), (bid, _) in sorted(idx.items()):
        if cond != "C2":
            continue
        for _, other in COMPS:
            o = idx.get((case, other, rep))
            if not o:
                continue
            pair = (idx[(case, "C2", rep)], o) if rng.random() < 0.5 else (o, idx[(case, "C2", rep)])
            jobs += [(case, pair[0], pair[1]), (case, pair[1], pair[0])]
    jc = CONFIG["judges"]["pairwise"]
    out = EVAL / "pairwise" / jc["model"]
    out.mkdir(parents=True, exist_ok=True)
    schema = json.loads((EV.SCHEMAS / "judge_pairwise.schema.json").read_text())

    def one(job):
        case, (x, dx), (y, dy) = job
        p = out / f"{x}__{y}.json"
        if p.exists():
            return
        prompt = ((EV.PROMPTS / "judge_pairwise.md").read_text().replace("{packet}", EV.packet(case)).replace("{answer_key}", EV.answer_key(case))
                  .replace("{doc_x}", (dx / f"{x}.md").read_text()).replace("{doc_y}", (dy / f"{y}.md").read_text())
                  .replace("{words_x}", str(json.loads((dx / f"{x}.json").read_text())["words"]))
                  .replace("{words_y}", str(json.loads((dy / f"{y}.json").read_text())["words"])))
        res = run_claude_json(prompt, jc["model"], jc["effort"], schema)
        if not res.get("structured_output"):
            (out / f"{x}__{y}.error.json").write_text(json.dumps(res, indent=1, default=str)[:20000])
            print(f"pairwise {x} vs {y}: ERROR", flush=True)
            return
        p.write_text(json.dumps({"x": x, "y": y, "case": case, "judge": jc, "output": res["structured_output"],
                                 "cost_usd": res.get("total_cost_usd"), "wall_s": res.get("_wall_s")}, indent=1, ensure_ascii=False))
        print(f"pairwise {x} vs {y}: ok", flush=True)

    with cf.ThreadPoolExecutor(parallel) as ex:
        list(ex.map(one, jobs))


def mode_used(run_dir):
    """'deck_deep' if the run read the skill's deep-deck workflow file, else 'deck_detailed'."""
    for tp in sorted(run_dir.glob("transcript-attempt*.jsonl.gz")):
        with gzip.open(tp, "rt") as f:
            for line in f:
                if '"Read"' in line and "references/deep-deck.md" in line:
                    try:
                        e = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    for b in (e.get("message") or {}).get("content", []) if isinstance(e.get("message"), dict) else []:
                        if b.get("type") == "tool_use" and b.get("name") == "Read" and "deep-deck.md" in str(b.get("input", {}).get("file_path")):
                            return "deck_deep"
    return "deck_detailed"


def fmt(x, d=2):
    return "–" if x is None else f"{x:.{d}f}"


def analyse():
    rows_main = AN.load(MAIN)[0]
    rows_c2, _, pairs, _ = AN.load(PHASE)
    for ph, rs in ((MAIN, rows_main), (PHASE, rows_c2)):
        for r in rs:
            r["phase"] = ph
    for r in rows_main + rows_c2:
        r["mode"] = mode_used(BENCH / "runs" / r["phase"] / r["run_id"]) if r["condition"] in ("C", "C2") else None
    rows = rows_main + rows_c2
    out = BENCH / "results" / PHASE
    out.mkdir(parents=True, exist_ok=True)
    cols = sorted({k for r in rows_c2 for k in r})
    lead = ["run_id", "case", "condition", "rep", "status", "mode", "blind_id"]
    with open(out / "per_doc.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=lead + [c for c in cols if c not in lead], extrasaction="ignore")
        w.writeheader()
        w.writerows(rows_c2)
    conds = ["A", "B", "C", "C2"]
    judges = [CONFIG["judges"]["primary"]["model"], CONFIG["judges"]["secondary"]["model"]]
    for r in rows:
        for jm in judges:
            if r.get(jm + "|weighted") is not None:
                r[jm + "|weighted_no_clarity"] = sum(AN.W[k] * r[jm + "|" + k] for k in AN.DIMS if k != "clarity_and_concision") / 0.9
    S = {"phase": PHASE, "exploratory": True, "n_c2_docs": len(rows_c2),
         "modes_c2": {m: sum(r["mode"] == m for r in rows_c2) for m in ("deck_detailed", "deck_deep")},
         "modes_c_main": {m: sum(r["mode"] == m for r in rows_main if r["condition"] == "C") for m in ("deck_detailed", "deck_deep")},
         "status_c2": {s: sum(r["status"] == s for r in rows_c2) for s in sorted({r["status"] for r in rows_c2})},
         "audit_clean_c2": sum(bool(r["audit_clean"]) for r in rows_c2), "by_judge": {}}
    for jm in judges:
        J = {"by_condition": {}, "paired": {}, "paired_no_clarity": {}}
        for c in conds:
            rc = [r for r in rows if r["condition"] == c]
            est, lo, hi = AN.hier_boot_mean(rc, jm + "|weighted")
            J["by_condition"][c] = {"n": sum(r.get(jm + "|weighted") is not None for r in rc), "weighted": est, "ci95": [lo, hi],
                                    **{k: AN.mean([r.get(jm + "|" + k) for r in rc]) for k in AN.DIMS},
                                    **{k: AN.mean([r.get(jm + "|" + k) for r in rc]) for k in ("numerical_errors", "contradictions", "defensible", "hyp_appropriate", "traps", "insights", "calcs_correct")}}
        for x, y in COMPS:
            J["paired"][f"{x}-{y}"] = AN.paired(rows, jm + "|weighted", x, y)
            J["paired_no_clarity"][f"{x}-{y}"] = AN.paired(rows, jm + "|weighted_no_clarity", x, y)
        S["by_judge"][jm] = J
    S["pairwise"] = AN.pairwise_summary(pairs, None, rows, comps=COMPS)
    e2e = {}
    for c in conds:
        rc = [r for r in rows if r["condition"] == c]
        e2e[c] = {k: AN.mean([r.get(k) for r in rc]) for k in ("slides", "words", "cost_usd", "duration_min", "native_charts", "pictures", "output_tokens")}
        e2e[c]["source_workbook"] = sum(bool(r.get("source_workbook")) for r in rc)
        e2e[c]["pptx"] = sum(bool(r.get("pptx")) for r in rc)
        e2e[c]["check_py_fail_runs"] = sum((r.get("check_py_fail") or 0) > 0 for r in rc) if c in ("C", "C2") else None
        e2e[c]["slides_range"] = [min(r["slides"] for r in rc), max(r["slides"] for r in rc)] if rc else None
    S["e2e"] = e2e
    S["cost_c2_generation_usd"] = sum(r["cost_all_attempts_usd"] for r in rows_c2)
    (out / "summary.json").write_text(json.dumps(S, indent=1, default=str))

    P = CONFIG["judges"]["primary"]["model"]
    names = {c: CONFIG["conditions"][c]["name"] for c in conds}
    L = [f"# Exploratory arm C2 · the skill in full-deck mode", "",
         "**Exploratory, added after the main results (METHODOLOGY.md §12).** A, B and C are the main-benchmark documents "
         "and their v2 judgments, reused unchanged; C2 documents were judged later by the same models and prompts.", "",
         f"Mode check: C2 runs in `deck_detailed` {S['modes_c2']['deck_detailed']}/{len(rows_c2)}; main C runs in `deck_deep` "
         f"{S['modes_c_main']['deck_deep']}/15. Audit clean: {S['audit_clean_c2']}/{len(rows_c2)}. Status: {S['status_c2']}.", "",
         "## Absolute scores (weighted, 1–5; 95% hierarchical bootstrap)", "",
         "| Judge | " + " | ".join(names[c] for c in conds) + " |", "|---|" + "---:|" * len(conds)]
    for jm in judges:
        bc = S["by_judge"][jm]["by_condition"]
        L.append(f"| {jm} | " + " | ".join(f"{fmt(bc[c]['weighted'])} [{fmt(bc[c]['ci95'][0])}, {fmt(bc[c]['ci95'][1])}]" for c in conds) + " |")
    L += ["", f"Per dimension ({P}):", "", "| Dimension | " + " | ".join(conds) + " |", "|---|" + "---:|" * len(conds)]
    for k in AN.DIMS:
        L.append(f"| {k} | " + " | ".join(fmt(S['by_judge'][P]['by_condition'][c][k]) for c in conds) + " |")
    L += ["", "## Paired case-level differences (5 cases; sign-flip p ≥ 0.0625 by design)", "",
          "| Judge | Comparison | Diff | 95% CI | Cases C2 better | Sign-flip p | No-clarity diff | No-clarity 95% CI |", "|---|---|---:|---|---:|---:|---:|---|"]
    for jm in judges:
        for comp in (f"{x}-{y}" for x, y in COMPS):
            p, q = S["by_judge"][jm]["paired"][comp], S["by_judge"][jm]["paired_no_clarity"][comp]
            if p:
                L.append(f"| {jm} | {comp} | {p['diff']:+.2f} | [{p['ci95'][0]:+.2f}, {p['ci95'][1]:+.2f}] | {p['cases_x_better']}/{p['cases']} | "
                         f"{p['p_signflip_cases']:.3f} | {q['diff']:+.2f} | [{q['ci95'][0]:+.2f}, {q['ci95'][1]:+.2f}] |")
    L += ["", "## Pairwise preference (order-balanced; 0.5 = no preference; both orders judged)", "",
          "| Judge | Comparison | Overall score | 95% CI | Consistent C2 wins–losses (ties, splits) | Coherence | Judgment | Evidence |", "|---|---|---:|---|---|---:|---:|---:|"]
    for jm, pj in S["pairwise"].items():
        for comp, per_q in pj["by_comparison"].items():
            if "overall" not in per_q:
                continue
            o = per_q["overall"]
            c = o["consistent"]
            L.append(f"| {jm} | {comp} | {o['score']:.2f} | [{o['ci95'][0]:.2f}, {o['ci95'][1]:.2f}] | {c['win']}–{c['loss']} ({c['tie']}, {c['split']}) | "
                     f"{per_q['coherence']['score']:.2f} | {per_q['judgment']['score']:.2f} | {per_q['evidence']['score']:.2f} |")
        L.append(f"\nPosition bias (first-shown document wins, non-tied): {fmt(pj['position_bias_first_wins_overall'])}")
    L += ["", "## End-to-end (means per run)", "", "| | " + " | ".join(conds) + " |", "|---|" + "---:|" * len(conds)]
    for k, d in (("slides", 1), ("words", 0), ("cost_usd", 2), ("duration_min", 1), ("native_charts", 1), ("output_tokens", 0)):
        L.append(f"| {k} | " + " | ".join(fmt(e2e[c][k], d) for c in conds) + " |")
    L.append("| slides range | " + " | ".join(f"{e2e[c]['slides_range'][0]}–{e2e[c]['slides_range'][1]}" for c in conds) + " |")
    L.append("| source workbook (runs) | " + " | ".join(str(e2e[c]["source_workbook"]) for c in conds) + " |")
    L.append("| check.py fail (runs) | " + " | ".join("–" if e2e[c]["check_py_fail_runs"] is None else str(e2e[c]["check_py_fail_runs"]) for c in conds) + " |")
    L += ["", f"C2 generation cost (all attempts, list-price estimate): ${S['cost_c2_generation_usd']:.2f}", ""]
    (out / "tables.md").write_text("\n".join(L))
    print(f"wrote {out / 'tables.md'}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["normalize", "blind", "judge", "pairwise", "analyse", "all"])
    ap.add_argument("--parallel", type=int, default=4)
    a = ap.parse_args()
    if a.step in ("normalize", "all"):
        normalize(a.parallel)
    if a.step in ("blind", "all"):
        blind()
    if a.step in ("judge", "all"):
        judge(a.parallel)
    if a.step in ("pairwise", "all"):
        pairwise(a.parallel)
    if a.step in ("analyse", "all"):
        analyse()


if __name__ == "__main__":
    main()
