"""Development arms after E1 (METHODOLOGY.md §14): one new condition against earlier documents, on the dev cases.

Generalises explore_e1.py (kept unchanged, frozen with the E1 arm). Example:
  benchmark/.venv/bin/python benchmark/scripts/explore_dev.py all --phase dev-e2 --cond E2 --vs B:main E1:dev-e1 --reps 1 --ref dev-e1

· reference: per case, a decision checklist written from the pack and answer key only (no deck seen); run before
             any E1 document is scored, then frozen
· normalize / blind / judge: as explore_c2.py; fresh blind ids that cannot collide with main or explore-c2
· pairwise:  E1 vs B (main) and E1 vs C2 (explore-c2), replicate-matched on replicates 1-2, both orders
· decision:  the decision-completeness check (secondary judge) on every E1, B and C2 document of replicates 1-2
· analyse:   results/dev-e1/{summary.json,tables.md}
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import pathlib
import random
import statistics as st
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import analyze as AN  # noqa: E402
import evaluate as EV  # noqa: E402
from common import BENCH, CONFIG, run_claude_json  # noqa: E402

PHASE, COND, VS, REPS, REF_PHASE = None, None, {}, (), None
EVAL = COMPS = None


def configure(a):
    global PHASE, COND, VS, REPS, REF_PHASE, EVAL, COMPS
    PHASE, COND, REF_PHASE = a.phase, a.cond, a.ref
    VS = dict(x.split(":") for x in a.vs)
    REPS = tuple(a.reps)
    EVAL = BENCH / "eval" / PHASE
    COMPS = tuple((COND, o) for o in VS)


def phases():
    return sorted(set(VS.values())) + [PHASE]
REF_JUDGE = CONFIG["judges"]["pairwise"]          # Fable 5.2 writes the reference checklists
DEC_JUDGE = CONFIG["judges"]["secondary"]         # Sonnet 5.5 applies them to every document


def reference(parallel):
    out = EVAL / "decision_reference"
    out.mkdir(parents=True, exist_ok=True)
    schema = json.loads((EV.SCHEMAS / "decision_reference.schema.json").read_text())

    def one(case):
        p = out / f"{case}.json"
        if p.exists():
            return
        prompt = (EV.PROMPTS / "decision_reference.md").read_text().replace("{packet}", EV.packet(case)).replace("{answer_key}", EV.answer_key(case))
        res = run_claude_json(prompt, REF_JUDGE["model"], REF_JUDGE["effort"], schema)
        if not res.get("structured_output"):
            (out / f"{case}.error.json").write_text(json.dumps(res, indent=1, default=str)[:20000])
            print(f"reference {case}: ERROR", flush=True)
            return
        p.write_text(json.dumps({"case": case, "judge": REF_JUDGE, "output": res["structured_output"], "cost_usd": res.get("total_cost_usd")},
                                indent=1, ensure_ascii=False))
        print(f"reference {case}: ok", flush=True)

    with cf.ThreadPoolExecutor(parallel) as ex:
        list(ex.map(one, CONFIG["phases"][PHASE]["cases"]))


def normalize(parallel):
    todo = [(d, m) for d, m in EV.runs(PHASE) if (d / "extract" / "deck.json").exists()]
    with cf.ThreadPoolExecutor(parallel) as ex:
        list(ex.map(lambda rm: EV.normalize_one(*rm), todo))


def blind():
    (EVAL / "blinded").mkdir(parents=True, exist_ok=True)
    key_p = EVAL / "blinding_key.json"
    key = json.loads(key_p.read_text()) if key_p.exists() else {}
    used = set(key)
    for kp in (BENCH / "eval").glob("*/blinding_key.json"):
        used |= set(json.loads(kp.read_text()))
    by_run = set(key.values())
    rng = random.Random(CONFIG["seeds"]["blinding"] + 3 + sum(map(ord, PHASE)))
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
    print(f"blinded {len(key)} {COND} documents")


def judge(parallel):
    bids = sorted(p.stem for p in (EVAL / "blinded").glob("*.md"))
    for which in ("primary", "secondary"):
        with cf.ThreadPoolExecutor(parallel) as ex:
            list(ex.map(lambda b: EV.judge_one(PHASE, which, b), bids))


def doc_index():
    """(case, condition, rep) -> (blind id, blinded dir) for the new condition and the reused comparison documents."""
    idx = {}
    for phase in phases():
        ev = BENCH / "eval" / phase
        kp = ev / "blinding_key.json"
        if not kp.exists():
            continue
        for bid, rid in json.loads(kp.read_text()).items():
            m = json.loads((BENCH / "runs" / phase / rid / "meta.json").read_text())
            if (m["condition"] == COND or VS.get(m["condition"]) == phase) and m["rep"] in REPS and (ev / "blinded" / f"{bid}.md").exists():
                idx[(m["case"], m["condition"], m["rep"])] = (bid, ev / "blinded")
    return idx


def pairwise(parallel):
    idx = doc_index()
    rng = random.Random(CONFIG["seeds"]["pairwise"] + 3 + sum(map(ord, PHASE)))
    jobs = []
    for (case, cond, rep), _ in sorted(idx.items()):
        if cond != COND:
            continue
        for _, other in COMPS:
            o = idx.get((case, other, rep))
            if not o:
                continue
            pair = (idx[(case, COND, rep)], o) if rng.random() < 0.5 else (o, idx[(case, COND, rep)])
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


def decision(parallel):
    idx = doc_index()
    out = EVAL / "decision" / DEC_JUDGE["model"]
    out.mkdir(parents=True, exist_ok=True)
    schema = json.loads((EV.SCHEMAS / "judge_decision.schema.json").read_text())

    def one(item):
        (case, cond, rep), (bid, d) = item
        p = out / f"{bid}.json"
        if p.exists() or any((BENCH / "eval" / ph / "decision" / DEC_JUDGE["model"] / f"{bid}.json").exists() for ph in phases()):
            return
        ref = json.loads((BENCH / "eval" / REF_PHASE / "decision_reference" / f"{case}.json").read_text())["output"]
        prompt = ((EV.PROMPTS / "judge_decision.md").read_text().replace("{packet}", EV.packet(case))
                  .replace("{reference}", json.dumps(ref, indent=1, ensure_ascii=False))
                  .replace("{words}", str(json.loads((d / f"{bid}.json").read_text())["words"]))
                  .replace("{document}", (d / f"{bid}.md").read_text()))
        res = run_claude_json(prompt, DEC_JUDGE["model"], DEC_JUDGE["effort"], schema)
        if not res.get("structured_output"):
            (out / f"{bid}.error.json").write_text(json.dumps(res, indent=1, default=str)[:20000])
            print(f"decision {bid}: ERROR", flush=True)
            return
        p.write_text(json.dumps({"blind_id": bid, "case": case, "judge": DEC_JUDGE, "output": res["structured_output"],
                                 "cost_usd": res.get("total_cost_usd")}, indent=1, ensure_ascii=False))
        print(f"decision {bid}: ok", flush=True)

    with cf.ThreadPoolExecutor(parallel) as ex:
        list(ex.map(one, sorted(idx.items())))


def fmt(x, d=2):
    return "–" if x is None else f"{x:.{d}f}"


def analyse():
    rows = []
    for ph in phases():
        rows += [r for r in AN.load(ph)[0] if (r["condition"] == COND or VS.get(r["condition"]) == ph) and r["rep"] in REPS]
    pairs = {}
    for jd in (EVAL / "pairwise").glob("*") if (EVAL / "pairwise").exists() else []:
        pairs[jd.name] = [json.loads(p.read_text()) for p in jd.glob("*.json") if not p.name.endswith(".error.json")]
    conds = list(VS) + [COND]
    S = {"phase": PHASE, "exploratory": True, "reps": list(REPS), "n": {c: sum(r["condition"] == c for r in rows) for c in conds}}
    S["pairwise"] = AN.pairwise_summary(pairs, None, rows, comps=COMPS) if pairs else {}
    S["absolute"] = {}
    for which in ("primary", "secondary"):
        jm = CONFIG["judges"][which]["model"]
        S["absolute"][jm] = {
            "weighted": {c: AN.hier_boot_mean([r for r in rows if r["condition"] == c], jm + "|weighted")[0] for c in conds},
            "dims": {c: {k: AN.mean([r.get(f"{jm}|{k}") for r in rows if r["condition"] == c]) for k in AN.DIMS} for c in conds},
            "paired": {f"{x}-{y}": AN.paired(rows, jm + "|weighted", x, y) for x, y in COMPS}}
    # decision completeness
    idx = doc_index()
    cond_of = {bid: c for (case, c, rep), (bid, _) in idx.items()}
    dec = {c: [] for c in conds}
    dfiles = [p for ph in phases() for p in (BENCH / "eval" / ph / "decision" / DEC_JUDGE["model"]).glob("*.json")]
    for p in dfiles:
        if p.name.endswith(".error.json"):
            continue
        o = json.loads(p.read_text())
        c = cond_of.get(o["blind_id"])
        if c:
            dec[c].append(o["output"])

    def share(items, good):
        return st.mean(1.0 if x["status"] in good else 0.0 for x in items) if items else None
    S["decision"] = {c: {
        "n": len(v),
        "constraints_reflected": AN.mean([share(o["constraints"], ("reflected",)) for o in v]),
        "alternatives_tested": AN.mean([share(o["alternatives"], ("tested",)) for o in v]),
        "sensitivities_quantified": AN.mean([share(o["sensitivities"], ("quantified",)) for o in v]),
        "overclaim_share": AN.mean([1.0 if o["overclaim"]["present"] else 0.0 for o in v]),
        "omissions_per_doc": AN.mean([len(o["omissions"]) for o in v]),
        "unsupported_assumptions_per_doc": AN.mean([len(o["unsupported_assumptions"]) for o in v])} for c, v in dec.items()}
    S["e2e"] = {c: {k: AN.mean([r.get(k) for r in rows if r["condition"] == c]) for k in ("slides", "words", "cost_usd", "duration_min", "native_charts")}
                for c in conds}
    out = BENCH / "results" / PHASE
    out.mkdir(parents=True, exist_ok=True)
    (out / "summary.json").write_text(json.dumps(S, indent=1, default=str))

    L = [f"# Development arm {COND} ({PHASE})", "",
         f"Exploratory, on the development cases, replicates {list(REPS)}. Documents of {', '.join(f'{c} ({p})' for c, p in VS.items())} "
         f"and their judgments are reused; {COND} documents are judged later by the same models and prompts.", "",
         "## Pairwise (Fable 5.2, both orders, replicate-matched)", "",
         "| Comparison | Overall | 95% CI | Wins–losses (ties, splits) | Coherence | Judgment | Evidence | Revision |", "|---|---:|---|---|---:|---:|---:|---:|"]
    for jm, pj in S["pairwise"].items():
        for comp, q in pj["by_comparison"].items():
            o, c = q["overall"], q["overall"]["consistent"]
            L.append(f"| {comp} | {o['score']:.2f} | {AN.fmt_pref_ci(o)} | {c['win']}–{c['loss']} ({c['tie']}, {c['split']}) | "
                     f"{q['coherence']['score']:.2f} | {q['judgment']['score']:.2f} | {q['evidence']['score']:.2f} | {q['revision']['score']:.2f} |")
        L += ["", f"Position bias (first-shown wins, non-tied): {fmt(pj['position_bias_first_wins_overall'])}", ""]
    L += ["## Absolute (weighted 1–5)", "", "| Judge | " + " | ".join(conds) + " | " + " | ".join(f"{x} − {y}" for x, y in COMPS) + " |",
          "|---|" + "---:|" * (len(conds) + len(COMPS))]
    for jm, A in S["absolute"].items():
        diffs = []
        for x, y in COMPS:
            p = A["paired"][f"{x}-{y}"]
            diffs.append("–" if not p else f"{p['diff']:+.2f} [{p['ci95'][0]:+.2f}, {p['ci95'][1]:+.2f}], {p['cases_x_better']}/{p['cases']} cases")
        L.append(f"| {jm} | " + " | ".join(fmt(A["weighted"][c]) for c in conds) + " | " + " | ".join(diffs) + " |")
    jm = CONFIG["judges"]["primary"]["model"]
    L += ["", f"Dimensions ({jm}):", "", "| Dimension | " + " | ".join(conds) + " |", "|---|" + "---:|" * len(conds)]
    for k in AN.DIMS:
        L.append(f"| {k} | " + " | ".join(fmt(S["absolute"][jm]["dims"][c][k]) for c in conds) + " |")
    L += ["", f"## Decision completeness ({DEC_JUDGE['model']}, against a checklist written from the pack alone)", "",
          "| | " + " | ".join(conds) + " |", "|---|" + "---:|" * len(conds)]
    for k in ("n", "constraints_reflected", "alternatives_tested", "sensitivities_quantified", "overclaim_share", "omissions_per_doc", "unsupported_assumptions_per_doc"):
        L.append(f"| {k} | " + " | ".join(fmt(S["decision"][c][k], 0 if k == "n" else 2) for c in conds) + " |")
    L += ["", "## End-to-end (mean per run)", "", "| | " + " | ".join(conds) + " |", "|---|" + "---:|" * len(conds)]
    for k in ("slides", "words", "cost_usd", "duration_min", "native_charts"):
        L.append(f"| {k} | " + " | ".join(fmt(S["e2e"][c][k], 1) for c in conds) + " |")
    (out / "tables.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["reference", "normalize", "blind", "judge", "pairwise", "decision", "analyse", "all"])
    ap.add_argument("--parallel", type=int, default=4)
    ap.add_argument("--phase", required=True)
    ap.add_argument("--cond", required=True)
    ap.add_argument("--vs", nargs="+", required=True, help="COND:PHASE of the documents to compare with")
    ap.add_argument("--reps", nargs="+", type=int, required=True)
    ap.add_argument("--ref", required=True, help="phase whose decision_reference checklists to use")
    a = ap.parse_args()
    configure(a)
    steps = ["normalize", "blind", "judge", "pairwise", "decision", "analyse"] if a.step == "all" else [a.step]
    for s in steps:
        print(f"== {s}", flush=True)
        {"reference": lambda: reference(a.parallel), "normalize": lambda: normalize(a.parallel), "blind": blind,
         "judge": lambda: judge(a.parallel), "pairwise": lambda: pairwise(a.parallel), "decision": lambda: decision(a.parallel),
         "analyse": analyse}[s]()


if __name__ == "__main__":
    main()
