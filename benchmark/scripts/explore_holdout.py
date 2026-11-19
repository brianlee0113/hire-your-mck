"""Holdout (METHODOLOGY.md §16): B, E1 and H2a-restyle on the six held-out cases c6–c11.

Usage (after run_generation / audit_runs / extract_deck / e2e_metrics and `evaluate.py normalize|blind|judge`
for --phase holdout):
  benchmark/.venv/bin/python benchmark/scripts/explore_holdout.py units|check|pairwise|analyse|all [--parallel 4]

Two comparisons, kept apart:
· B → H2a (does compiling keep the analysis?)
    units:    per B deck, Fable 5.2 lists its decision units (critical / valid); known errors = the numerical errors
              and contradictions the answer-key judge found in that B deck. Written before any H2a deck is checked.
    check:    per H2a deck, fidelity checker v2 (preserved / verified_correction / unsupported_alteration / missing /
              inherited_error, new errors by severity), reading the deck's own correction log.
    pairwise: H2a vs its B deck, both orders, no word counts.
· E1 vs H2a (which is the better final deliverable?)
    pairwise: E1 vs H2a, both orders, no word counts; E1 vs B for context. Rubric scores come from evaluate.py judge.
analyse:  results/holdout/{summary.json,tables.md}.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import pathlib
import random
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import analyze as AN  # noqa: E402
import evaluate as EV  # noqa: E402
from common import BENCH, CONFIG, run_claude_json  # noqa: E402
from explore_h1 import number_check  # noqa: E402

PHASE = "holdout"
EVAL = BENCH / "eval" / PHASE
JUDGE = CONFIG["judges"]["pairwise"]  # Fable 5.2 for pairwise, units and check
PRIMARY = CONFIG["judges"]["primary"]["model"]
PAIRS = (("H2a", "B"), ("E1", "H2a"), ("E1", "B"))


def runs():
    """{case: {condition: (run_dir, meta)}} for completed runs."""
    out = {}
    for d, m in EV.runs(PHASE):
        out.setdefault(m["case"], {})[m["condition"]] = (d, m)
    return out


def bkey():
    p = EVAL / "blinding_key.json"
    return json.loads(p.read_text()) if p.exists() else {}


def bid_of(run_name):
    return {v: k for k, v in bkey().items()}.get(run_name)


def call(prompt, schema_name, out_p, extra):
    if out_p.exists():
        return
    out_p.parent.mkdir(parents=True, exist_ok=True)
    res = run_claude_json(prompt, JUDGE["model"], JUDGE["effort"], json.loads((EV.SCHEMAS / schema_name).read_text()))
    if not res.get("structured_output"):
        out_p.with_suffix(".error.json").write_text(json.dumps(res, indent=1, default=str)[:20000])
        print(f"{out_p.name}: ERROR", flush=True)
        return
    out_p.write_text(json.dumps({**extra, "judge": JUDGE, "output": res["structured_output"], "cost_usd": res.get("total_cost_usd")},
                                indent=1, ensure_ascii=False))
    print(f"{out_p.name}: ok", flush=True)


def find_spec(run_dir):
    for p in sorted((run_dir / "workspace").glob("deliverable/*.json")) + sorted((run_dir / "workspace").glob("work/*.json")):
        try:  # the spec may be saved next to the deck or in the run's work folder
            js = json.loads(p.read_text())
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        if isinstance(js, dict) and "slides" in js and "data_points" in js:
            return js
    return {}


def units(parallel):
    jobs = [(case, rs["B"]) for case, rs in sorted(runs().items()) if "B" in rs]

    def one(job):
        case, (d, _) = job
        bid = bid_of(d.name)
        jp = EVAL / "auto" / PRIMARY / f"{bid}.json"
        if not bid or not jp.exists():
            print(f"{case}: B deck not yet judged; run evaluate.py judge first", flush=True)
            return
        o = json.loads(jp.read_text())["output"]
        known = {"numerical_errors": o["numerical_errors"], "logical_contradictions": o["logical_contradictions"]}
        prompt = ((EV.PROMPTS / "fidelity_units.md").read_text().replace("{packet}", EV.packet(case))
                  .replace("{known_errors}", json.dumps(known, indent=1, ensure_ascii=False))
                  .replace("{source}", (d / "extract" / "deck.txt").read_text()))
        call(prompt, "fidelity_units.schema.json", EVAL / "fidelity" / "units" / f"{case}.json", {"case": case, "source_run": d.name})

    with cf.ThreadPoolExecutor(parallel) as ex:
        list(ex.map(one, jobs))


def check(parallel):
    jobs = [(case, rs["H2a"]) for case, rs in sorted(runs().items()) if "H2a" in rs]

    def one(job):
        case, (d, _) = job
        up = EVAL / "fidelity" / "units" / f"{case}.json"
        if not up.exists() or not (d / "extract" / "deck.txt").exists():
            return
        u = json.loads(up.read_text())["output"]["units"]
        corr = (find_spec(d).get("compile") or {}).get("corrections") or []
        prompt = ((EV.PROMPTS / "fidelity_check_v2.md").read_text().replace("{packet}", EV.packet(case))
                  .replace("{units}", json.dumps(u, indent=1, ensure_ascii=False))
                  .replace("{corrections}", json.dumps(corr, indent=1, ensure_ascii=False) if corr else "(none logged)")
                  .replace("{remake}", (d / "extract" / "deck.txt").read_text()))
        call(prompt, "fidelity_check_v2.schema.json", EVAL / "fidelity" / "check" / f"{d.name}.json", {"run_id": d.name, "case": case})

    with cf.ThreadPoolExecutor(parallel) as ex:
        list(ex.map(one, jobs))


def pairwise(parallel):
    rng = random.Random(CONFIG["seeds"]["pairwise"] + 16)
    jobs = []
    for case, rs in sorted(runs().items()):
        for a, b in PAIRS:
            if a not in rs or b not in rs:
                continue
            x, y = bid_of(rs[a][0].name), bid_of(rs[b][0].name)
            if not x or not y:
                continue
            first, second = (x, y) if rng.random() < 0.5 else (y, x)
            jobs += [(case, first, second), (case, second, first)]
    out = EVAL / "pairwise_nowords" / JUDGE["model"]
    tmpl = (EV.PROMPTS / "judge_pairwise_nowords.md").read_text()
    bx = EVAL / "blinded"

    def one(job):
        case, x, y = job
        prompt = (tmpl.replace("{packet}", EV.packet(case)).replace("{answer_key}", EV.answer_key(case))
                  .replace("{doc_x}", (bx / f"{x}.md").read_text()).replace("{doc_y}", (bx / f"{y}.md").read_text()))
        call(prompt, "judge_pairwise.schema.json", out / f"{x}__{y}.json", {"x": x, "y": y, "case": case})

    with cf.ThreadPoolExecutor(parallel) as ex:
        list(ex.map(one, jobs))


STATUSES = ("preserved", "verified_correction", "unsupported_alteration", "missing", "inherited_error")


def analyse():
    key = bkey()
    cond_of = {}
    for bid, rid in key.items():
        m = json.loads((BENCH / "runs" / PHASE / rid / "meta.json").read_text())
        cond_of[bid] = (m["case"], m["condition"])
    rs = runs()
    # rubric (answer-key judge), per run
    rubric = {r["run_id"]: r for r in AN.load(PHASE)[0]}
    # pairwise: per case and pair, both orders; a win counts only when both orders agree
    pw = {}
    pdir = EVAL / "pairwise_nowords" / JUDGE["model"]
    for p in sorted(pdir.glob("*.json")) if pdir.exists() else []:
        if p.name.endswith(".error.json"):
            continue
        o = json.loads(p.read_text())
        (case, cx), (_, cy) = cond_of[o["x"]], cond_of[o["y"]]
        w = o["output"]["overall"]["winner"]
        winner = "tie" if w == "tie" else (cx if w == "X" else cy)
        pair = next((a, b) for a, b in PAIRS if {a, b} == {cx, cy})
        pw.setdefault((case, pair), []).append({"winner": winner, "strength": o["output"]["overall"].get("strength"),
                                                "reasons": o["output"]["overall"]["reasons"]})
    rows = []
    for case in sorted(rs, key=lambda c: int(c.split("-")[0][1:])):
        r = {"case": case, "runs": {}}
        for cond, (d, m) in rs[case].items():
            e2e = json.loads((d / "e2e.json").read_text()) if (d / "e2e.json").exists() else {}
            rr = rubric.get(d.name, {})
            r["runs"][cond] = {"run_id": d.name, "status": m["status"], "slides": e2e.get("slides"), "words": e2e.get("words"),
                               "check_py_fail": (e2e.get("check_py") or {}).get("fail"), "cost_usd": m["totals"]["cost_usd"],
                               "api_min": m["totals"]["api_s"] / 60, "weighted": rr.get(PRIMARY + "|weighted")}
        h = rs[case].get("H2a")
        if h:
            d = h[0]
            spec = find_spec(d)
            cp = spec.get("compile") or {}
            r["compile"] = {"corrections": cp.get("corrections") or [], "untraceable": cp.get("untraceable") or [],
                            "critical_untraceable": sum(1 for u in cp.get("untraceable") or [] if u.get("critical"))}
            cpath, upath = EVAL / "fidelity" / "check" / f"{d.name}.json", EVAL / "fidelity" / "units" / f"{case}.json"
            if cpath.exists() and upath.exists():
                ul = {u["id"]: u for u in json.loads(upath.read_text())["output"]["units"]}
                ch = json.loads(cpath.read_text())["output"]
                cnt = {"valid": {s: 0 for s in STATUSES}, "invalid": {s: 0 for s in STATUSES}}
                for x in ch["units"]:
                    u = ul.get(x["id"])
                    if u and u["critical"]:
                        cnt["valid" if u["valid"] else "invalid"][x["status"]] += 1
                ne = ch["new_errors"]
                bad = [x for x in ch["units"] if x["id"] in ul and ul[x["id"]]["critical"]
                       and x["status"] not in ("preserved", "verified_correction")]
                r["fidelity"] = {"critical": cnt, "new_errors": ne,
                                 "problems": [{"id": x["id"], "status": x["status"], "unit": ul[x["id"]]["text"], "note": x["note"]}
                                              for x in ch["units"] if x["id"] in ul and x["status"] not in ("preserved", "verified_correction")],
                                 "corrections": [{"id": x["id"], "unit": ul[x["id"]]["text"], "note": x["note"]}
                                                 for x in ch["units"] if x["id"] in ul and x["status"] == "verified_correction"]}
                f, t, miss = number_check(list(ul.values()), (d / "extract" / "deck.txt").read_text())
                r["fidelity"]["numbers"] = {"found": f, "total": t, "missing": miss}
                r["fidelity"]["pass"] = (not bad and not any(e["severity"] == "critical" for e in ne)
                                         and r["runs"]["H2a"]["check_py_fail"] == 0)
        r["pairwise"] = {f"{a} vs {b}": pw.get((case, (a, b)), []) for a, b in PAIRS}
        rows.append(r)
    out = BENCH / "results" / PHASE
    out.mkdir(parents=True, exist_ok=True)
    (out / "summary.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False, default=str))

    def verdict(v, a, b):
        if len(v) < 2:
            return "–"
        ws = {x["winner"] for x in v}
        if ws == {a}:
            return f"{a} (both)"
        if ws == {b}:
            return f"{b} (both)"
        return "tie/split"

    def pct(a, b):
        return "–" if not b else f"{a}/{b} ({100 * a / b:.0f}%)"
    L = ["# Holdout · B, E1 and H2a-restyle on c6–c11", "",
         "Pairwise: Fable 5.2, no word counts, both orders; a win counts only when both orders agree. Rubric: weighted "
         f"score from the answer-key judge ({PRIMARY}). H2a cost = B + compile.", "",
         "## 1. B → H2a: does compiling keep the analysis?", "",
         "| Case | Preserved (critical valid) | Verified corrections (critical invalid) | Unsupported alteration / missing / inherited | New errors c/m/m | Numbers found | check.py fails | Pass | H2a vs B |",
         "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        fd = r.get("fidelity")
        if not fd:
            L.append(f"| {r['case']} | – | – | – | – | – | – | – | – |")
            continue
        v, iv = fd["critical"]["valid"], fd["critical"]["invalid"]
        alt = sum(v[s] + iv[s] for s in ("unsupported_alteration",))
        mis = sum(v[s] + iv[s] for s in ("missing",))
        inh = iv["inherited_error"]
        sev = "/".join(str(sum(1 for e in fd["new_errors"] if e["severity"] == s)) for s in ("critical", "material", "minor"))
        n = fd["numbers"]
        L.append(f"| {r['case']} | {pct(v['preserved'], sum(v.values()))} | {pct(iv['verified_correction'], sum(iv.values()))} | "
                 f"{alt} / {mis} / {inh} | {sev} | {pct(n['found'], n['total'])} | {r['runs']['H2a']['check_py_fail']} | "
                 f"{'yes' if fd['pass'] else 'no'} | {verdict(r['pairwise']['H2a vs B'], 'H2a', 'B')} |")
    L += ["", "## 2. E1 vs H2a: which is the better final deliverable?", "",
          "| Case | E1 vs H2a | E1 vs B | Rubric B / E1 / H2a | Slides B / E1 / H2a | Cost B / E1 / H2a (= B + compile) | API min B / E1 / H2a |",
          "|---|---|---|---|---|---|---|"]
    for r in rows:
        g = lambda c, k: (r["runs"].get(c) or {}).get(k)  # noqa: E731
        f2 = lambda x: "–" if x is None else f"{x:.2f}"  # noqa: E731
        hc = (g("B", "cost_usd") or 0) + (g("H2a", "cost_usd") or 0) if g("H2a", "cost_usd") is not None else None
        hm = (g("B", "api_min") or 0) + (g("H2a", "api_min") or 0) if g("H2a", "api_min") is not None else None
        L.append(f"| {r['case']} | {verdict(r['pairwise']['E1 vs H2a'], 'E1', 'H2a')} | {verdict(r['pairwise']['E1 vs B'], 'E1', 'B')} | "
                 f"{f2(g('B', 'weighted'))} / {f2(g('E1', 'weighted'))} / {f2(g('H2a', 'weighted'))} | "
                 f"{g('B', 'slides')} / {g('E1', 'slides')} / {g('H2a', 'slides')} | "
                 f"${f2(g('B', 'cost_usd'))} / ${f2(g('E1', 'cost_usd'))} / ${f2(hc)} | "
                 f"{f2(g('B', 'api_min'))} / {f2(g('E1', 'api_min'))} / {f2(hm)} |")
    e1h = [verdict(r["pairwise"]["E1 vs H2a"], "E1", "H2a") for r in rows]
    L += ["", f"H2a ahead in {sum(x.startswith('H2a') for x in e1h)} of {len(rows)} cases, E1 ahead in "
          f"{sum(x.startswith('E1') for x in e1h)}, tie or split in {sum(x == 'tie/split' for x in e1h)}. "
          "Reading rule (§16): 5 of 6 is the strongest wording allowed; 4 or fewer is mixed.", "",
          "## 3. What changed, went missing or was inherited (H2a)", ""]
    for r in rows:
        fd = r.get("fidelity") or {}
        L.append(f"**{r['case']}**")
        for x in fd.get("problems", []):
            L.append(f"- [{x['status']}] {x['unit'][:160]} → {x['note'][:240]}")
        for x in fd.get("corrections", []):
            L.append(f"- [verified_correction] {x['unit'][:160]} → {x['note'][:240]}")
        for e in fd.get("new_errors", []):
            L.append(f"- [new error, {e['severity']}] \"{e['quote'][:120]}\": {e['problem'][:200]}")
        for c in (r.get("compile") or {}).get("corrections", []):
            L.append(f"- (logged by H2a) {str(c.get('was', ''))[:100]} → {str(c.get('now', ''))[:100]} ({str(c.get('why', ''))[:120]})")
        if r.get("compile"):
            L.append(f"- untraceable numbers: {len(r['compile']['untraceable'])} ({r['compile']['critical_untraceable']} critical, acknowledged, not verified)")
        L.append("")
    (out / "tables.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["units", "check", "pairwise", "analyse", "all"])
    ap.add_argument("--parallel", type=int, default=4)
    a = ap.parse_args()
    steps = ["units", "check", "pairwise", "analyse"] if a.step == "all" else [a.step]
    for s in steps:
        print(f"== {s}", flush=True)
        {"units": lambda: units(a.parallel), "check": lambda: check(a.parallel), "pairwise": lambda: pairwise(a.parallel),
         "analyse": analyse}[s]()


if __name__ == "__main__":
    main()
