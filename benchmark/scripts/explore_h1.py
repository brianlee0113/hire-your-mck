"""Development arm H1 (METHODOLOGY.md §15): compile mode on B's finished decks, checked for content fidelity first.

Usage (after run_generation / audit_runs / extract_deck / e2e_metrics for --phase dev-h1):
  benchmark/.venv/bin/python benchmark/scripts/explore_h1.py normalize|blind|pairwise|units|check|analyse|all

· pairwise: each H1 deck vs its source B deck, both orders, Fable 5.2, prompt WITHOUT word counts (secondary)
· units:    per source B deck, Fable 5.2 lists its decision units (critical / valid), with B's known errors from
            the main evaluation, without seeing any H1 deck
· check:    per H1 deck, Fable 5.2 marks each unit preserved / altered / missing / corrected / still_wrong and
            lists new errors by severity (primary outcome)
· analyse:  results/dev-h1/{summary.json,tables.md}: fidelity, deterministic number check, correction log, number
            classes, pairwise, cost and time
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import pathlib
import random
import re
import sys
import types

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import analyze as AN  # noqa: E402
import evaluate as EV  # noqa: E402
import explore_dev as XD  # noqa: E402
from common import BENCH, CONFIG, run_claude_json  # noqa: E402

PHASE = "dev-h1"
EVAL = BENCH / "eval" / PHASE
CONDS = ("H1s", "H1r")
JUDGE = CONFIG["judges"]["pairwise"]  # Fable 5.2 for pairwise, units and check
XD.configure(types.SimpleNamespace(phase=PHASE, cond="H1", vs=["B:main"], reps=[2, 3], ref="dev-e1"))


def h_runs():
    out = []
    for d, m in EV.runs(PHASE):
        if m["condition"] in CONDS:
            out.append((d, m))
    return out


def source_run(case):
    return BENCH / "runs" / CONFIG["phases"][PHASE]["analysis_from"][case]


def main_bid(run_name):
    return {v: k for k, v in json.loads((BENCH / "eval" / "main" / "blinding_key.json").read_text()).items()}[run_name]


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


def pairwise(parallel):
    hkey = {v: k for k, v in json.loads((EVAL / "blinding_key.json").read_text()).items()}
    rng = random.Random(CONFIG["seeds"]["pairwise"] + 15)
    jobs = []
    for d, m in sorted(h_runs()):
        if d.name not in hkey or not (EVAL / "blinded" / f"{hkey[d.name]}.md").exists():
            continue
        h = (hkey[d.name], EVAL / "blinded")
        b = (main_bid(source_run(m["case"]).name), BENCH / "eval" / "main" / "blinded")
        first, second = (h, b) if rng.random() < 0.5 else (b, h)
        jobs += [(m["case"], first, second), (m["case"], second, first)]
    out = EVAL / "pairwise_nowords" / JUDGE["model"]
    tmpl = (EV.PROMPTS / "judge_pairwise_nowords.md").read_text()

    def one(job):
        case, (x, dx), (y, dy) = job
        prompt = (tmpl.replace("{packet}", EV.packet(case)).replace("{answer_key}", EV.answer_key(case))
                  .replace("{doc_x}", (dx / f"{x}.md").read_text()).replace("{doc_y}", (dy / f"{y}.md").read_text()))
        call(prompt, "judge_pairwise.schema.json", out / f"{x}__{y}.json", {"x": x, "y": y, "case": case})

    with cf.ThreadPoolExecutor(parallel) as ex:
        list(ex.map(one, jobs))


def units(parallel):
    cases = sorted({m["case"] for _, m in h_runs()} | set(CONFIG["phases"][PHASE]["analysis_from"]))

    def one(case):
        src = source_run(case)
        o = json.loads((BENCH / "eval" / "main" / "auto" / CONFIG["judges"]["primary"]["model"] / f"{main_bid(src.name)}.json").read_text())["output"]
        known = {"numerical_errors": o["numerical_errors"], "logical_contradictions": o["logical_contradictions"]}
        prompt = ((EV.PROMPTS / "fidelity_units.md").read_text().replace("{packet}", EV.packet(case))
                  .replace("{known_errors}", json.dumps(known, indent=1, ensure_ascii=False))
                  .replace("{source}", (src / "extract" / "deck.txt").read_text()))
        call(prompt, "fidelity_units.schema.json", EVAL / "fidelity" / "units" / f"{case}.json", {"case": case, "source_run": src.name})

    with cf.ThreadPoolExecutor(parallel) as ex:
        list(ex.map(one, cases))


def check(parallel):
    def one(dm):
        d, m = dm
        up = EVAL / "fidelity" / "units" / f"{m['case']}.json"
        if not up.exists() or not (d / "extract" / "deck.txt").exists():
            return
        u = json.loads(up.read_text())["output"]["units"]
        prompt = ((EV.PROMPTS / "fidelity_check.md").read_text().replace("{packet}", EV.packet(m["case"]))
                  .replace("{units}", json.dumps(u, indent=1, ensure_ascii=False))
                  .replace("{remake}", (d / "extract" / "deck.txt").read_text()))
        call(prompt, "fidelity_check.schema.json", EVAL / "fidelity" / "check" / f"{d.name}.json", {"run_id": d.name, "case": m["case"]})

    with cf.ThreadPoolExecutor(parallel) as ex:
        list(ex.map(one, h_runs()))


NUM = re.compile(r"[−-]?\$?\d[\d,]*(?:\.\d+)?\s?(?:%|pp|M|B|K|x)?")


def _norm_num(t):
    t = t.replace("−", "-").replace(",", "").replace("$", "").replace(" ", "")
    return t


def number_check(unit_list, text):
    """Share of numbers in critical, valid units that appear verbatim (normalised) in the remake's text."""
    hay = _norm_num(text)
    found = total = 0
    missing = []
    for u in unit_list:
        if not (u["critical"] and u["valid"]):
            continue
        for n in {_norm_num(x) for x in NUM.findall(u["text"])}:
            if len(n.strip("-%.pMBKx")) < 2:  # single digits ("1", "2") are list markers, not evidence
                continue
            total += 1
            if n in hay:
                found += 1
            else:
                missing.append((u["id"], n))
    return found, total, missing


def analyse():
    rows = []
    for d, m in sorted(h_runs()):
        r = {"run_id": d.name, "case": m["case"], "condition": m["condition"], "status": m["status"]}
        e2e = json.loads((d / "e2e.json").read_text()) if (d / "e2e.json").exists() else {}
        meta = json.loads((d / "meta.json").read_text())
        r.update({"slides": e2e.get("slides"), "words": e2e.get("words"), "native_charts": e2e.get("native_charts"),
                  "check_py_fail": (e2e.get("check_py") or {}).get("fail"), "cost_usd": meta["totals"]["cost_usd"],
                  "api_min": meta["totals"]["api_s"] / 60})
        src = source_run(m["case"])
        se = json.loads((src / "e2e.json").read_text())
        r["source"] = {"run": src.name, "slides": se.get("slides"), "words": se.get("words")}
        spec = {}
        for p in sorted((d / "workspace").glob("deliverable/*.json")) + sorted((d / "workspace").glob("work/*.json")):
            try:  # the spec may be saved next to the deck or in the run's work folder
                js = json.loads(p.read_text())
            except (json.JSONDecodeError, UnicodeDecodeError):
                continue
            if isinstance(js, dict) and "slides" in js and "data_points" in js:
                spec = js
                break
        cp = spec.get("compile") or {}
        dps = spec.get("data_points") or []
        r["spec"] = {"units": len(cp.get("units") or []), "critical_units": sum(1 for u in cp.get("units") or [] if u.get("critical")),
                     "corrections": cp.get("corrections") or [], "untraceable": cp.get("untraceable") or [],
                     "data_points": len(dps), "derived": sum(1 for x in dps if x.get("derived_from")),
                     "estimates": sum(1 for x in dps if x.get("estimate"))}
        cpath = EVAL / "fidelity" / "check" / f"{d.name}.json"
        upath = EVAL / "fidelity" / "units" / f"{m['case']}.json"
        if cpath.exists() and upath.exists():
            ul = {u["id"]: u for u in json.loads(upath.read_text())["output"]["units"]}
            ch = json.loads(cpath.read_text())["output"]
            st = {}
            for x in ch["units"]:
                u = ul.get(x["id"])
                if not u:
                    continue
                key = ("critical" if u["critical"] else "other") + ("" if u["valid"] else "_invalid")
                st.setdefault(key, {}).setdefault(x["status"], 0)
                st[key][x["status"]] += 1
            r["fidelity"] = st
            r["altered_or_missing"] = [{"id": x["id"], "critical": ul[x["id"]]["critical"], "status": x["status"], "unit": ul[x["id"]]["text"], "note": x["note"]}
                                       for x in ch["units"] if x["status"] in ("altered", "missing", "still_wrong") and x["id"] in ul]
            r["corrected"] = [{"id": x["id"], "unit": ul[x["id"]]["text"], "note": x["note"]} for x in ch["units"] if x["status"] == "corrected" and x["id"] in ul]
            r["new_errors"] = ch["new_errors"]
            f, t, miss = number_check(list(ul.values()), (d / "extract" / "deck.txt").read_text())
            r["numbers"] = {"found": f, "total": t, "missing": miss}
        rows.append(r)
    # pairwise (secondary)
    pw = {}
    hkey = json.loads((EVAL / "blinding_key.json").read_text()) if (EVAL / "blinding_key.json").exists() else {}
    pdir = EVAL / "pairwise_nowords" / JUDGE["model"]
    for p in pdir.glob("*.json") if pdir.exists() else []:
        if p.name.endswith(".error.json"):
            continue
        o = json.loads(p.read_text())
        x, y = o["x"], o["y"]
        hid = x if x in hkey else y
        w = o["output"]["overall"]["winner"]
        score = 0.5 if w == "tie" else (1.0 if (w == "X") == (hid == x) else 0.0)
        pw.setdefault(hkey[hid], []).append({"score": score, "strength": o["output"]["overall"].get("strength"), "reasons": o["output"]["overall"]["reasons"]})
    for r in rows:
        r["pairwise_vs_B"] = pw.get(r["run_id"], [])
    out = BENCH / "results" / PHASE
    out.mkdir(parents=True, exist_ok=True)
    (out / "summary.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False, default=str))

    def pct(a, b):
        return "–" if not b else f"{a}/{b} ({100 * a / b:.0f}%)"
    L = ["# Development arm H1 · compile mode on B's finished decks", "",
         "Primary: content fidelity against decision units taken from the source B deck (Fable 5.2, written before any "
         "H1 deck was checked). Secondary: pairwise vs the source deck, without word counts in the judge prompt.", "",
         "| Run | Slides (B) | Words (B) | Critical units preserved | Altered / missing (critical) | Corrected | Still wrong | New errors c/m/m | Numbers found | check.py fails | Pairwise vs B | Cost | API min |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        fd = r.get("fidelity", {})
        crit = fd.get("critical", {})
        n_crit = sum(crit.values())
        allinv = {k: v for k, v in fd.items() if k.endswith("_invalid")}
        corr = sum(v.get("corrected", 0) for v in allinv.values())
        still = sum(v.get("still_wrong", 0) for v in allinv.values())
        ne = r.get("new_errors", [])
        sev = "/".join(str(sum(1 for e in ne if e["severity"] == s)) for s in ("critical", "material", "minor"))
        nums = r.get("numbers")
        pwv = r["pairwise_vs_B"]
        pws = f"{sum(x['score'] for x in pwv) / len(pwv):.2f} (n={len(pwv)})" if pwv else "–"
        L.append(f"| {r['run_id']} | {r['slides']} ({r['source']['slides']}) | {r['words']} ({r['source']['words']}) | "
                 f"{pct(crit.get('preserved', 0), n_crit)} | {crit.get('altered', 0)} / {crit.get('missing', 0)} | {corr} | {still} | {sev} | "
                 f"{pct(nums['found'], nums['total']) if nums else '–'} | {r['check_py_fail']} | {pws} | ${r['cost_usd']:.2f} | {r['api_min']:.1f} |")
    L += ["", "## What changed or went missing", ""]
    for r in rows:
        L.append(f"**{r['run_id']}**")
        for x in r.get("altered_or_missing", []):
            L.append(f"- [{x['status']}{', critical' if x['critical'] else ''}] {x['unit'][:160]} → {x['note'][:240]}")
        for e in r.get("new_errors", []):
            L.append(f"- [new error, {e['severity']}] \"{e['quote'][:120]}\": {e['problem'][:200]}")
        L.append("")
    L += ["## Correction log", ""]
    for r in rows:
        for c in r["spec"]["corrections"]:
            L.append(f"- {r['run_id']} (self-reported): {c.get('was', '')[:100]} → {c.get('now', '')[:100]} ({c.get('why', '')[:120]})")
        for c in r.get("corrected", []):
            L.append(f"- {r['run_id']} (checker): {c['unit'][:120]} — {c['note'][:160]}")
    L += ["", "## Numbers on the slides", "", "| Run | Data points | Derived | Estimates | Untraceable (critical) |", "|---|---:|---:|---:|---|"]
    for r in rows:
        s = r["spec"]
        L.append(f"| {r['run_id']} | {s['data_points']} | {s['derived']} | {s['estimates']} | {len(s['untraceable'])} ({sum(1 for u in s['untraceable'] if u.get('critical'))}) |")
    (out / "tables.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["normalize", "blind", "pairwise", "units", "check", "analyse", "all"])
    ap.add_argument("--parallel", type=int, default=4)
    a = ap.parse_args()
    steps = ["normalize", "blind", "units", "check", "pairwise", "analyse"] if a.step == "all" else [a.step]
    for s in steps:
        print(f"== {s}", flush=True)
        {"normalize": lambda: XD.normalize(a.parallel), "blind": XD.blind, "pairwise": lambda: pairwise(a.parallel),
         "units": lambda: units(a.parallel), "check": lambda: check(a.parallel), "analyse": analyse}[s]()


if __name__ == "__main__":
    main()
