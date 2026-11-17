"""Analyse a phase: aggregate scores, paired comparisons, win rates, errors, revision, cost, agreement, figures.

Usage: benchmark/.venv/bin/python benchmark/scripts/analyze.py --phase main
Writes results/<phase>/per_doc.csv, summary.json, tables.md and figures/*.png|svg

Statistics are descriptive with uncertainty. Case is the unit of replication (5 cases in the main benchmark):
paired differences are computed per case (mean of the 3 replicates), with a hierarchical bootstrap (cases, then
replicates) for 95% intervals and an exact sign-flip test over cases. With 5 cases the smallest possible two-sided
sign-flip p-value is 0.0625, so no case-level comparison can reach p < 0.05; that is a property of the design.
A run-level permutation test within cases is also shown; it treats replicates as independent and overstates power.
"""
from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
import pathlib
import random
import statistics as st
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import BENCH, CONFIG  # noqa: E402

DIMS = ["problem_framing", "storyline_coherence", "evidence_and_reasoning", "strategic_judgment", "clarity_and_concision"]
W = {"problem_framing": 0.15, "storyline_coherence": 0.25, "evidence_and_reasoning": 0.25, "strategic_judgment": 0.25,
     "clarity_and_concision": 0.10}
YNP = {"yes": 1.0, "partial": 0.5, "no": 0.0}
CONDS = ["A", "B", "C"]
NAMES = {k: v["name"] for k, v in CONFIG["conditions"].items()}
RNG_SEED = 20261115


def jload(p):
    return json.loads(pathlib.Path(p).read_text())


# ---------------------------------------------------------------------------------------------- load
def load(phase):
    base = BENCH / "runs" / phase
    key_p = BENCH / "eval" / phase / "blinding_key.json"
    bkey = jload(key_p) if key_p.exists() else {}
    bid_of = {v: k for k, v in bkey.items()}
    judges = {}
    for jd in (BENCH / "eval" / phase / "auto").glob("*") if (BENCH / "eval" / phase / "auto").exists() else []:
        judges[jd.name] = {p.stem: jload(p) for p in jd.glob("*.json") if not p.name.endswith(".error.json")}
    rows = []
    for d in sorted(base.glob(f"{phase}-*")):
        if not (d / "meta.json").exists():
            continue
        m = jload(d / "meta.json")
        e2e = jload(d / "e2e.json") if (d / "e2e.json").exists() else {}
        norm = jload(d / "normalized.json") if (d / "normalized.json").exists() else {}
        aud = jload(d / "audit.json") if (d / "audit.json").exists() else {}
        r = {"run_id": m["run_id"], "case": m["case"], "condition": m["condition"], "rep": m["rep"], "order": m["order"],
             "status": m["status"], "autoreplies": m.get("autoreplies_used"), "cost_usd": m["totals"]["cost_usd"],
             "cost_all_attempts_usd": m["totals"].get("cost_all_attempts_usd", m["totals"]["cost_usd"]), "attempts": len(m["attempts"]),
             "duration_min": m["totals"]["duration_s"] / 60, "output_tokens": m["totals"]["output_tokens"],
             "input_tokens_total": m["totals"]["input_tokens"] + m["totals"]["cache_read_tokens"] + m["totals"]["cache_creation_tokens"],
             "agent_turns": m["totals"]["turns"], "models": ",".join(sorted(m.get("models_used", {}))),
             "words": e2e.get("words"), "slides": e2e.get("slides"), "native_charts": e2e.get("native_charts"),
             "pictures": e2e.get("pictures"), "source_workbook": e2e.get("source_workbook"), "pptx": e2e.get("pptx_delivered"),
             "share_numbers_in_pack": e2e.get("share_numbers_in_pack"), "check_py_fail": (e2e.get("check_py") or {}).get("fail"),
             "fidelity": (norm.get("fidelity") or {}).get("share_ge_0_8"), "audit_clean": aud.get("clean"),
             "subagents": aud.get("subagent_calls"), "blind_id": bid_of.get(m["run_id"])}
        for jm, res in judges.items():
            o = (res.get(r["blind_id"]) or {}).get("output")
            pre = jm + "|"
            if not o:
                r[pre + "weighted"] = None
                continue
            for k in DIMS:
                r[pre + k] = o["scores"][k]["score"]
            r[pre + "weighted"] = sum(W[k] * o["scores"][k]["score"] for k in DIMS)
            words = max(1, r["words"] or 1)
            r[pre + "unsupported"] = len(o["unsupported_claims"])
            r[pre + "unsupported_per_1k"] = 1000 * len(o["unsupported_claims"]) / words
            r[pre + "numerical_errors"] = len(o["numerical_errors"])
            r[pre + "contradictions"] = len(o["logical_contradictions"])
            ce = o["critical_evidence"]
            r[pre + "missed_critical"] = sum(1 - YNP[x["used"]] for x in ce)
            r[pre + "insights"] = st.mean(YNP[x["reached"]] for x in o["insights"]) if o["insights"] else None
            cal = {"correct": 1, "partly_correct": 0.5, "incorrect": 0, "absent": 0}
            r[pre + "calcs_correct"] = st.mean(cal[x["status"]] for x in o["calculations"]) if o["calculations"] else None
            r[pre + "tradeoffs"] = st.mean(YNP[x["identified"]] for x in o["tradeoffs"]) if o["tradeoffs"] else None
            r[pre + "traps"] = st.mean(YNP[x["fell_in"]] for x in o["traps"]) if o["traps"] else None
            r[pre + "defensible"] = YNP[o["recommendation"]["defensible"]]
            h = o["hypothesis_handling"]
            r[pre + "hyp_appropriate"] = YNP[h["appropriate"]]
            r[pre + "hyp_observed"] = h["observed"]
            r[pre + "noticed_contradictions"] = YNP[h["noticed_contradictions"]]
            r[pre + "challenged_assumptions"] = YNP[h["challenged_assumptions"]]
            r[pre + "acknowledges_uncertainty"] = YNP[h["acknowledges_uncertainty"]]
            r[pre + "unsupported_causal"] = h["unsupported_causal_claims"]
            r[pre + "source_guess"] = o["source_guess"]["guess"]
        rows.append(r)
    pair = {}
    pdir = BENCH / "eval" / phase / "pairwise"
    for jd in pdir.glob("*") if pdir.exists() else []:
        pair[jd.name] = [jload(p) for p in jd.glob("*.json") if not p.name.endswith(".error.json")]
    human = {}
    hdir = BENCH / "eval" / phase / "human" / "scores"
    for p in hdir.glob("*.json") if hdir.exists() else []:
        h = jload(p)
        human[h["reviewer"]] = h["scores"]
    return rows, bkey, pair, human


# ---------------------------------------------------------------------------------------------- stats
def mean(xs):
    xs = [x for x in xs if x is not None and not (isinstance(x, float) and math.isnan(x))]
    return sum(xs) / len(xs) if xs else None


def by(rows, *keys):
    out = {}
    for r in rows:
        out.setdefault(tuple(r[k] for k in keys), []).append(r)
    return out


def hier_boot_mean(rows, col, B=10000, seed=RNG_SEED):
    g = {}
    for r in rows:
        if r.get(col) is not None:
            g.setdefault(r["case"], []).append(r[col])
    cases = list(g)
    if not cases:
        return None, None, None
    rng = random.Random(seed)
    est = mean([mean(v) for v in g.values()])
    bs = []
    for _ in range(B):
        cs = [rng.choice(cases) for _ in cases]
        bs.append(mean([mean([rng.choice(g[c]) for _ in g[c]]) for c in cs]))
    bs.sort()
    return est, bs[int(0.025 * B)], bs[int(0.975 * B) - 1]


def paired(rows, col, x, y, B=10000, seed=RNG_SEED):
    """Case-level paired difference x − y."""
    g = {}
    for r in rows:
        if r.get(col) is None or r["condition"] not in (x, y):
            continue
        g.setdefault(r["case"], {}).setdefault(r["condition"], []).append(r[col])
    g = {c: v for c, v in g.items() if x in v and y in v}
    if not g:
        return None
    diffs = {c: mean(v[x]) - mean(v[y]) for c, v in g.items()}
    est = mean(diffs.values())
    rng = random.Random(seed)
    cases = list(g)
    bs = []
    for _ in range(B):
        cs = [rng.choice(cases) for _ in cases]
        bs.append(mean([mean([rng.choice(g[c][x]) for _ in g[c][x]]) - mean([rng.choice(g[c][y]) for _ in g[c][y]]) for c in cs]))
    bs.sort()
    # exact sign-flip over cases
    d = list(diffs.values())
    obs = abs(mean(d))
    cnt = tot = 0
    for signs in itertools.product([1, -1], repeat=len(d)):
        tot += 1
        cnt += abs(mean([s * v for s, v in zip(signs, d)])) >= obs - 1e-12
    p_sign = cnt / tot
    # run-level permutation within case
    rng2 = random.Random(seed + 1)
    perm_cnt, P = 0, 5000
    obs_run = est
    for _ in range(P):
        dd = []
        for c, v in g.items():
            pool = v[x] + v[y]
            rng2.shuffle(pool)
            dd.append(mean(pool[:len(v[x])]) - mean(pool[len(v[x]):]))
        perm_cnt += abs(mean(dd)) >= abs(obs_run) - 1e-12
    wins = sum(1 for v in d if v > 0)
    return {"diff": est, "ci95": [bs[int(0.025 * B)], bs[int(0.975 * B) - 1]], "per_case": diffs, "cases_x_better": wins,
            "cases": len(d), "p_signflip_cases": p_sign, "p_perm_runs": perm_cnt / P}


def win_rate_absolute(rows, col, x, y):
    g = by(rows, "case", "rep")
    w = l = t = 0
    for k, rs in g.items():
        dx = [r[col] for r in rs if r["condition"] == x and r.get(col) is not None]
        dy = [r[col] for r in rs if r["condition"] == y and r.get(col) is not None]
        if dx and dy:
            if dx[0] > dy[0] + 1e-9:
                w += 1
            elif dy[0] > dx[0] + 1e-9:
                l += 1
            else:
                t += 1
    n = w + l + t
    return {"wins": w, "losses": l, "ties": t, "n": n, "win_rate": (w + 0.5 * t) / n if n else None}


def exact_extreme_ci(x, n, alpha=0.05):
    """Clopper-Pearson interval when every trial went the same way (x = 0 or x = n), where it has a closed form.
    Used only as a reference when the bootstrap collapses: it assumes independent trials, which pairs within a case
    are not, so the per-case version is the conservative one."""
    if not n or x not in (0, n):
        return None
    edge = 1 - (alpha / 2) ** (1 / n)
    return [0.0, edge] if x == 0 else [1 - edge, 1.0]


def fmt_pref_ci(d, digits=2):
    """Format a pairwise preference CI. A bootstrap over unanimous results is a single point, not a population
    interval, so it is reported as degenerate together with the exact reference intervals."""
    if not d.get("ci95_degenerate"):
        return f"[{fmt(d['ci95'][0], digits)}, {fmt(d['ci95'][1], digits)}]"
    ref = d.get("exact_ref") or {}
    parts = [f"{k} {fmt(v[0], digits)}–{fmt(v[1], digits)}" for k, v in (("pairs", ref.get("pairs")), ("cases", ref.get("cases"))) if v]
    return "bootstrap degenerate" + (f"; exact ref. {', '.join(parts)}" if parts else "")


def pairwise_summary(pairs, bkey, rows, B=10000, seed=RNG_SEED, comps=(("C", "A"), ("C", "B"), ("B", "A"))):
    """Order-balanced preference. For a comparison 'C vs A' each presentation order gives C 1 (win), 0.5 (tie) or 0
    (loss); a pair's score is the mean of its two orders. A 'consistent win' needs both orders to pick the same doc.
    95% CI: hierarchical bootstrap over cases, then pairs within case. When every pair has the same result the
    bootstrap can only return that point, so the CI is flagged degenerate and exact Clopper-Pearson references are
    added (pairs treated as independent, and cases treated as independent). Neither is a valid interval for this
    clustered design; they bracket it."""
    cond_of = {r["blind_id"]: r["condition"] for r in rows}
    case_of = {r["blind_id"]: r["case"] for r in rows}
    Q = ("coherence", "judgment", "evidence", "revision", "overall")
    out = {}
    for jm, items in pairs.items():
        idx = {(it["x"], it["y"]): it["output"] for it in items if it.get("output")}
        first = [o["overall"]["winner"] == "X" for (x, y), o in idx.items() if o["overall"]["winner"] != "tie"]
        res = {}
        for hi, lo in comps:
            per_q = {}
            for q in Q:
                by_case, cons = {}, {"win": 0, "loss": 0, "tie": 0, "split": 0}
                for (x, y), o in idx.items():
                    if (y, x) not in idx or x > y:
                        continue
                    cx, cy = cond_of.get(x), cond_of.get(y)
                    if {cx, cy} != {hi, lo}:
                        continue
                    h = x if cx == hi else y
                    vals = []
                    for (a, b) in ((x, y), (y, x)):
                        w = idx[(a, b)][q]["winner"]
                        win_id = None if w == "tie" else (a if w == "X" else b)
                        vals.append(0.5 if win_id is None else (1.0 if win_id == h else 0.0))
                    by_case.setdefault(case_of[x], []).append(mean(vals))
                    if vals == [1.0, 1.0]:
                        cons["win"] += 1
                    elif vals == [0.0, 0.0]:
                        cons["loss"] += 1
                    elif vals == [0.5, 0.5]:
                        cons["tie"] += 1
                    else:
                        cons["split"] += 1
                if not by_case:
                    continue
                est = mean([mean(v) for v in by_case.values()])
                rng = random.Random(seed)
                cases = list(by_case)
                bs = sorted(mean([mean([rng.choice(by_case[c]) for _ in by_case[c]]) for c in [rng.choice(cases) for _ in cases]]) for _ in range(B))
                ci_lo, ci_hi = bs[int(0.025 * B)], bs[int(0.975 * B) - 1]
                pair_scores = [s for v in by_case.values() for s in v]
                case_scores = [mean(v) for v in by_case.values()]
                degenerate = ci_hi - ci_lo < 1e-12
                exact_ref = None
                if degenerate and est in (0.0, 1.0):
                    exact_ref = {"pairs": exact_extreme_ci(sum(s == 1.0 for s in pair_scores), len(pair_scores)),
                                 "cases": exact_extreme_ci(sum(s == 1.0 for s in case_scores), len(case_scores))}
                per_q[q] = {"score": est, "ci95": [ci_lo, ci_hi], "ci95_degenerate": degenerate, "exact_ref": exact_ref,
                            "n_pairs": len(pair_scores), "n_cases": len(case_scores),
                            "cases_won": sum(s > 0.5 for s in case_scores), "cases_lost": sum(s < 0.5 for s in case_scores),
                            "consistent": cons, "by_case": {c: mean(v) for c, v in by_case.items()}}
            res[f"{hi}-{lo}"] = per_q
        out[jm] = {"by_comparison": res, "position_bias_first_wins_overall": (sum(first) / len(first)) if first else None}
    return out


def qwk(a, b, k=5):
    """Quadratic weighted kappa for two raters on 1..k."""
    pairs = [(x, y) for x, y in zip(a, b) if x is not None and y is not None]
    if len(pairs) < 2:
        return None
    O = [[0] * k for _ in range(k)]
    for x, y in pairs:
        O[x - 1][y - 1] += 1
    n = len(pairs)
    ra = [sum(O[i]) for i in range(k)]
    rb = [sum(O[i][j] for i in range(k)) for j in range(k)]
    num = den = 0.0
    for i in range(k):
        for j in range(k):
            w = (i - j) ** 2 / (k - 1) ** 2
            num += w * O[i][j]
            den += w * ra[i] * rb[j] / n
    return 1 - num / den if den else None


def spearman(a, b):
    pairs = [(x, y) for x, y in zip(a, b) if x is not None and y is not None]
    if len(pairs) < 3:
        return None
    def rank(v):
        s = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(s):
            j = i
            while j + 1 < len(s) and v[s[j + 1]] == v[s[i]]:
                j += 1
            for k in range(i, j + 1):
                r[s[k]] = (i + j) / 2 + 1
            i = j + 1
        return r
    x, y = rank([p[0] for p in pairs]), rank([p[1] for p in pairs])
    mx, my = mean(x), mean(y)
    num = sum((a - mx) * (b - my) for a, b in zip(x, y))
    den = math.sqrt(sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y))
    return num / den if den else None


def kripp_alpha_interval(units):
    """units: list of lists of ratings (one list per item, any number of raters)."""
    vals = [u for u in units if len([v for v in u if v is not None]) >= 2]
    if not vals:
        return None
    pairs_within = []
    allv = []
    for u in vals:
        u = [v for v in u if v is not None]
        m = len(u)
        allv += u
        for i, j in itertools.permutations(range(m), 2):
            pairs_within.append(((u[i] - u[j]) ** 2, m))
    n = len(allv)
    Do = sum(d / (m - 1) for d, m in pairs_within) / n
    De = sum((a - b) ** 2 for a, b in itertools.permutations(allv, 2)) / (n * (n - 1))
    return 1 - Do / De if De else None


# ---------------------------------------------------------------------------------------------- report
def fmt(x, d=2):
    return "—" if x is None else (f"{x:.{d}f}" if isinstance(x, float) else str(x))


def analyse(phase):
    rows, bkey, pairs, human = load(phase)
    out = BENCH / "results" / phase
    (out / "figures").mkdir(parents=True, exist_ok=True)
    if not rows:
        print("no runs")
        return
    cols = sorted({k for r in rows for k in r})
    lead = ["run_id", "case", "condition", "rep", "status", "blind_id"]
    with open(out / "per_doc.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=lead + [c for c in cols if c not in lead])
        w.writeheader()
        w.writerows(rows)
    judge_models = sorted({k.split("|")[0] for r in rows for k in r if "|" in k})
    primary = CONFIG["judges"]["primary"]["model"]
    S = {"phase": phase, "n_docs": len(rows), "judges": judge_models, "status_counts": {}, "by_judge": {}}
    for c in CONDS:
        S["status_counts"][c] = {}
        for r in rows:
            if r["condition"] == c:
                S["status_counts"][c][r["status"]] = S["status_counts"][c].get(r["status"], 0) + 1
    metric_cols = ["weighted"] + DIMS + ["unsupported", "unsupported_per_1k", "numerical_errors", "contradictions", "missed_critical",
                                         "insights", "calcs_correct", "tradeoffs", "traps", "defensible", "hyp_appropriate",
                                         "noticed_contradictions", "challenged_assumptions", "acknowledges_uncertainty", "unsupported_causal"]
    for jm in judge_models:
        J = {"by_condition": {}, "paired": {}, "win_rate_absolute": {}, "by_case": {}, "variability": {}}
        for c in CONDS:
            rc = [r for r in rows if r["condition"] == c]
            J["by_condition"][c] = {}
            for mc in metric_cols:
                col = f"{jm}|{mc}"
                est, lo, hi = hier_boot_mean(rc, col)
                J["by_condition"][c][mc] = {"mean": est, "ci95": [lo, hi]}
            sds = [st.pstdev([r[f"{jm}|weighted"] for r in rs if r.get(f"{jm}|weighted") is not None])
                   for (case, cond), rs in by(rows, "case", "condition").items() if cond == c and len(rs) > 1]
            J["variability"][c] = {"mean_within_case_sd_weighted": mean(sds)}
        for x, y in (("C", "A"), ("C", "B"), ("B", "A")):
            J["paired"][f"{x}-{y}"] = {mc: paired(rows, f"{jm}|{mc}", x, y) for mc in ["weighted"] + DIMS + ["unsupported_per_1k", "numerical_errors", "defensible", "hyp_appropriate"]}
            J["win_rate_absolute"][f"{x}-{y}"] = win_rate_absolute(rows, f"{jm}|weighted", x, y)
        for (case, cond), rs in sorted(by(rows, "case", "condition").items()):
            v = [r[f"{jm}|weighted"] for r in rs if r.get(f"{jm}|weighted") is not None]
            J["by_case"].setdefault(case, {})[cond] = {"mean": mean(v), "min": min(v) if v else None, "max": max(v) if v else None, "n": len(v),
                                                       "hyp_appropriate": mean([r.get(f"{jm}|hyp_appropriate") for r in rs])}
        # EXPLORATORY (not pre-registered): weighted score without the clarity & concision dimension, to check
        # whether condition differences are only a length penalty
        for r in rows:
            if r.get(f"{jm}|weighted") is not None:
                r[f"{jm}|weighted_no_clarity"] = sum(W[k] * r[f"{jm}|{k}"] for k in DIMS if k != "clarity_and_concision") / 0.9
        J["exploratory_no_clarity_paired"] = {f"{x}-{y}": paired(rows, f"{jm}|weighted_no_clarity", x, y) for x, y in (("C", "A"), ("C", "B"), ("B", "A"))}
        # hypothesis revision by expected handling
        exp = {c: jload(BENCH / "answer_keys" / f"{c}.json")["initial_hypothesis"]["expected_handling"] for c in CONFIG["cases"]}
        J["hypothesis_by_expected"] = {}
        for r in rows:
            e = exp[r["case"]]
            J["hypothesis_by_expected"].setdefault(e, {}).setdefault(r["condition"], []).append(r.get(f"{jm}|hyp_appropriate"))
        J["hypothesis_by_expected"] = {e: {c: mean(v) for c, v in d.items()} for e, d in J["hypothesis_by_expected"].items()}
        # blinding check
        conf = {}
        for r in rows:
            g = r.get(f"{jm}|source_guess")
            if g:
                conf.setdefault(r["condition"], {}).setdefault(g, 0)
                conf[r["condition"]][g] += 1
        J["source_guess_confusion"] = conf
        J["length_score_spearman"] = spearman([r["words"] for r in rows], [r.get(f"{jm}|weighted") for r in rows])
        J["length_score_spearman_within_condition"] = {c: spearman([r["words"] for r in rows if r["condition"] == c],
                                                                   [r.get(f"{jm}|weighted") for r in rows if r["condition"] == c]) for c in CONDS}
        S["by_judge"][jm] = J
    # judge agreement
    if len(judge_models) >= 2:
        a, b = primary, [j for j in judge_models if j != primary][0]
        ag = {"pair": [a, b], "spearman_weighted": spearman([r.get(f"{a}|weighted") for r in rows], [r.get(f"{b}|weighted") for r in rows]),
              "mean_abs_diff_weighted": mean([abs(r[f"{a}|weighted"] - r[f"{b}|weighted"]) for r in rows if r.get(f"{a}|weighted") is not None and r.get(f"{b}|weighted") is not None]),
              "qwk": {k: qwk([r.get(f"{a}|{k}") for r in rows], [r.get(f"{b}|{k}") for r in rows]) for k in DIMS},
              "defensible_agreement": mean([1.0 if r.get(f"{a}|defensible") == r.get(f"{b}|defensible") else 0.0 for r in rows if r.get(f"{a}|defensible") is not None and r.get(f"{b}|defensible") is not None])}
        S["judge_agreement"] = ag
    S["pairwise"] = pairwise_summary(pairs, bkey, rows)
    # cost and effort
    S["cost"] = {c: {k: {"mean": mean([r[k] for r in rows if r["condition"] == c]),
                         "sd": (st.pstdev([r[k] for r in rows if r["condition"] == c and r[k] is not None]) if len([r for r in rows if r["condition"] == c]) > 1 else None)}
                     for k in ("cost_usd", "duration_min", "output_tokens", "input_tokens_total", "agent_turns", "words", "slides", "native_charts", "pictures", "share_numbers_in_pack", "fidelity", "autoreplies")}
                 for c in CONDS}
    S["cost_total_usd"] = sum(r["cost_usd"] for r in rows)
    S["cost_total_all_attempts_usd"] = sum(r["cost_all_attempts_usd"] for r in rows)
    S["eval_cost_usd"] = {}
    for sub in ("auto", "pairwise"):
        d = BENCH / "eval" / phase / sub
        for jd in d.glob("*") if d.exists() else []:
            S["eval_cost_usd"][f"{sub}/{jd.name}"] = sum((jload(p).get("cost_usd") or 0) for p in jd.glob("*.json") if not p.name.endswith(".error.json"))
    S["normalize_cost_usd"] = sum((jload(d / "normalized.json").get("cost_usd") or 0) for d in (BENCH / "runs" / phase).glob(f"{phase}-*") if (d / "normalized.json").exists())
    # human
    if human:
        bid_cond = {r["blind_id"]: r for r in rows}
        H = {"reviewers": sorted(human), "alpha_interval": {}, "by_condition": {}}
        bids = sorted({b for h in human.values() for b in h})
        for k in DIMS:
            H["alpha_interval"][k] = kripp_alpha_interval([[human[rv].get(b, {}).get(k) for rv in human] for b in bids])
        for b in bids:
            ws = []
            for rv in human:
                s = human[rv].get(b)
                if s and all(k in s for k in DIMS):
                    ws.append(sum(W[k] * s[k] for k in DIMS))
            if b in bid_cond and ws:
                bid_cond[b]["human|weighted"] = mean(ws)
        H["alpha_interval"]["weighted"] = kripp_alpha_interval([[sum(W[k] * human[rv][b][k] for k in DIMS) if b in human[rv] and all(k in human[rv][b] for k in DIMS) else None for rv in human] for b in bids])
        for c in CONDS:
            est, lo, hi = hier_boot_mean([r for r in rows if r["condition"] == c], "human|weighted")
            H["by_condition"][c] = {"mean": est, "ci95": [lo, hi]}
        H["paired"] = {f"{x}-{y}": paired(rows, "human|weighted", x, y) for x, y in (("C", "A"), ("C", "B"), ("B", "A"))}
        H["human_vs_primary_spearman"] = spearman([r.get("human|weighted") for r in rows], [r.get(f"{primary}|weighted") for r in rows])
        S["human"] = H
    (out / "summary.json").write_text(json.dumps(S, indent=1, default=str))
    tables(S, rows, out)
    figures(S, rows, out, primary)
    print(f"wrote {out}")


def tables(S, rows, out):
    L = [f"# Results · phase `{S['phase']}`", "", f"{S['n_docs']} documents. Judges: {', '.join(S['judges'])}.", "",
         "Status by condition: " + "; ".join(f"{NAMES[c]}: {S['status_counts'][c]}" for c in CONDS), ""]
    for jm, J in S["by_judge"].items():
        L += [f"## Judge `{jm}`", "", "### Weighted score and dimensions by condition (mean, 95% hierarchical bootstrap CI)", "",
              "| Metric | " + " | ".join(NAMES[c] for c in CONDS) + " |", "|---|" + "---|" * len(CONDS)]
        for mc in ["weighted"] + DIMS:
            L.append(f"| {mc} | " + " | ".join(f"{fmt(J['by_condition'][c][mc]['mean'])} [{fmt(J['by_condition'][c][mc]['ci95'][0])}, {fmt(J['by_condition'][c][mc]['ci95'][1])}]" for c in CONDS) + " |")
        L += ["", "### Errors, coverage, judgment (mean per document)", "", "| Metric | " + " | ".join(NAMES[c] for c in CONDS) + " |", "|---|" + "---|" * len(CONDS)]
        for mc in ["unsupported_per_1k", "unsupported", "numerical_errors", "contradictions", "missed_critical", "insights", "calcs_correct",
                   "tradeoffs", "traps", "defensible", "hyp_appropriate", "noticed_contradictions", "challenged_assumptions", "acknowledges_uncertainty", "unsupported_causal"]:
            L.append(f"| {mc} | " + " | ".join(fmt(J['by_condition'][c][mc]['mean']) for c in CONDS) + " |")
        L += ["", "### Paired case-level differences (weighted score)", "", "| Comparison | Mean diff | 95% CI | Cases better | p (sign-flip, cases) | p (perm, runs) | Win rate (rep-matched) |", "|---|---|---|---|---|---|---|"]
        for pn, d in J["paired"].items():
            p = d["weighted"]
            wr = J["win_rate_absolute"][pn]
            if p:
                L.append(f"| {pn} | {fmt(p['diff'])} | [{fmt(p['ci95'][0])}, {fmt(p['ci95'][1])}] | {p['cases_x_better']}/{p['cases']} | {fmt(p['p_signflip_cases'], 3)} | {fmt(p['p_perm_runs'], 3)} | {wr['wins']}-{wr['losses']}-{wr['ties']} ({fmt(wr['win_rate'])}) |")
        L += ["", "### Paired differences by dimension (mean diff, 95% CI)", "", "| Dimension | " + " | ".join(J["paired"]) + " |", "|---|" + "---|" * len(J["paired"])]
        for mc in DIMS + ["unsupported_per_1k", "numerical_errors", "defensible", "hyp_appropriate"]:
            L.append(f"| {mc} | " + " | ".join((f"{fmt(d[mc]['diff'])} [{fmt(d[mc]['ci95'][0])}, {fmt(d[mc]['ci95'][1])}]" if d[mc] else "—") for d in J["paired"].values()) + " |")
        L += ["", "### Exploratory (not pre-registered): weighted score without clarity & concision", "", "| Comparison | Mean diff | 95% CI | Cases better |", "|---|---|---|---|"]
        for pn, p in J.get("exploratory_no_clarity_paired", {}).items():
            if p:
                L.append(f"| {pn} | {fmt(p['diff'])} | [{fmt(p['ci95'][0])}, {fmt(p['ci95'][1])}] | {p['cases_x_better']}/{p['cases']} |")
        L += ["", "### By case (weighted score: mean [min–max] over replicates)", "", "| Case | " + " | ".join(NAMES[c] for c in CONDS) + " |", "|---|" + "---|" * len(CONDS)]
        for case, d in J["by_case"].items():
            L.append(f"| {case} | " + " | ".join((f"{fmt(d[c]['mean'])} [{fmt(d[c]['min'])}–{fmt(d[c]['max'])}]" if c in d else "—") for c in CONDS) + " |")
        L += ["", "### Hypothesis handling judged appropriate (share), by the case's expected handling", "", "| Expected | " + " | ".join(NAMES[c] for c in CONDS) + " |", "|---|" + "---|" * len(CONDS)]
        for e, d in J["hypothesis_by_expected"].items():
            L.append(f"| {e} | " + " | ".join(fmt(d.get(c)) for c in CONDS) + " |")
        L += ["", f"Within-case SD of weighted score across replicates: " + "; ".join(f"{NAMES[c]} {fmt(J['variability'][c]['mean_within_case_sd_weighted'])}" for c in CONDS),
              "", f"Blinding check (judge's guess of how each document was produced): `{json.dumps(J['source_guess_confusion'])}`",
              "", f"Length vs weighted score, Spearman: overall {fmt(J['length_score_spearman'])}; within condition {json.dumps({c: (round(v, 2) if v is not None else None) for c, v in J['length_score_spearman_within_condition'].items()})}", ""]
    if "judge_agreement" in S:
        a = S["judge_agreement"]
        L += ["## Agreement between automated judges", "", f"{a['pair'][0]} vs {a['pair'][1]}: Spearman on weighted score {fmt(a['spearman_weighted'])}; mean absolute difference {fmt(a['mean_abs_diff_weighted'])}; "
              f"same defensibility verdict {fmt(a['defensible_agreement'])}; quadratic weighted kappa by dimension " + ", ".join(f"{k} {fmt(v)}" for k, v in a["qwk"].items()), ""]
    for jm, P in S["pairwise"].items():
        L += [f"## Pairwise judge `{jm}`", "",
              "Preference score of the first-named condition: 1 = it wins in both presentation orders, 0.5 = tie, 0 = it loses "
              "in both; mean over rep-matched pairs, case-level bootstrap 95% CI. Consistent = both orders agree (win-loss-tie-split).", "",
              f"Position bias: the first-shown document won {fmt(P['position_bias_first_wins_overall'])} of non-tied overall verdicts.", "",
              "| Comparison | " + " | ".join(("overall", "coherence (H1)", "judgment (H2)", "evidence (H3)", "revision (H4)")) + " |", "|---|---|---|---|---|---|"]
        for cmp_, qs in P["by_comparison"].items():
            cells = []
            for q in ("overall", "coherence", "judgment", "evidence", "revision"):
                d = qs.get(q)
                cells.append("—" if not d else f"{fmt(d['score'])} {fmt_pref_ci(d)} · {d['consistent']['win']}-{d['consistent']['loss']}-{d['consistent']['tie']}-{d['consistent']['split']}")
            L.append(f"| {cmp_} | " + " | ".join(cells) + " |")
        L.append("")
    L += ["## Cost and effort per run (mean ± SD)", "", "| | " + " | ".join(NAMES[c] for c in CONDS) + " |", "|---|" + "---|" * len(CONDS)]
    for k in ("cost_usd", "duration_min", "output_tokens", "input_tokens_total", "agent_turns", "autoreplies", "words", "slides", "native_charts", "pictures", "share_numbers_in_pack", "fidelity"):
        L.append(f"| {k} | " + " | ".join(f"{fmt(S['cost'][c][k]['mean'])} ± {fmt(S['cost'][c][k]['sd'])}" for c in CONDS) + " |")
    L += ["", f"Total generation cost (list-price estimate reported by Claude Code): ${S['cost_total_usd']:.2f} for the evaluated attempts, "
          f"${S['cost_total_all_attempts_usd']:.2f} including failed attempts. Normalisation ${S['normalize_cost_usd']:.2f}; evaluation "
          + ", ".join(f"{k} ${v:.2f}" for k, v in S["eval_cost_usd"].items()) + ".", ""]
    if "human" in S:
        H = S["human"]
        L += ["## Human reviewers", "", f"Reviewers: {', '.join(H['reviewers'])}. Krippendorff's alpha (interval): " + ", ".join(f"{k} {fmt(v)}" for k, v in H["alpha_interval"].items()),
              "", "| | " + " | ".join(NAMES[c] for c in CONDS) + " |", "|---|" + "---|" * len(CONDS),
              "| weighted | " + " | ".join(f"{fmt(H['by_condition'][c]['mean'])} [{fmt(H['by_condition'][c]['ci95'][0])}, {fmt(H['by_condition'][c]['ci95'][1])}]" for c in CONDS) + " |",
              "", f"Human vs primary automated judge, Spearman: {fmt(H['human_vs_primary_spearman'])}", ""]
    else:
        L += ["## Human reviewers", "", "No human scores yet. See `eval/<phase>/human/INSTRUCTIONS.md`.", ""]
    (out / "tables.md").write_text("\n".join(L))


def figures(S, rows, out, primary):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib missing; no figures")
        return
    col = {"A": "#8a96a3", "B": "#3b6ea8", "C": "#c2512f"}
    J = S["by_judge"].get(primary)
    if not J:
        return
    # 1 · every document, by case and condition
    cases = list(CONFIG["cases"])
    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    for i, case in enumerate(cases):
        for k, c in enumerate(CONDS):
            v = [r.get(f"{primary}|weighted") for r in rows if r["case"] == case and r["condition"] == c and r.get(f"{primary}|weighted") is not None]
            x = i + (k - 1) * 0.22
            ax.scatter([x] * len(v), v, color=col[c], s=28, alpha=0.85, label=NAMES[c] if i == 0 else None, zorder=3)
            if v:
                ax.plot([x - 0.08, x + 0.08], [mean(v)] * 2, color=col[c], lw=2.2)
    ax.set_xticks(range(len(cases)))
    ax.set_xticklabels([c.split("-", 1)[1].replace("-", " ") for c in cases])
    ax.set_ylim(1, 5)
    ax.set_ylabel(f"Weighted score (1–5), judge {primary}")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, ncol=3, loc="lower center", bbox_to_anchor=(0.5, 1.0))
    fig.tight_layout()
    for ext in ("png", "svg"):
        fig.savefig(out / "figures" / f"scores_by_case.{ext}", dpi=160)
    plt.close(fig)
    # 2 · dimensions by condition with CI
    fig, ax = plt.subplots(figsize=(8.5, 3.8))
    labels = ["weighted"] + DIMS
    for k, c in enumerate(CONDS):
        m = [J["by_condition"][c][d]["mean"] or 0 for d in labels]
        lo = [(J["by_condition"][c][d]["mean"] or 0) - (J["by_condition"][c][d]["ci95"][0] or 0) for d in labels]
        hi = [(J["by_condition"][c][d]["ci95"][1] or 0) - (J["by_condition"][c][d]["mean"] or 0) for d in labels]
        xs = [i + (k - 1) * 0.25 for i in range(len(labels))]
        ax.errorbar(xs, m, yerr=[lo, hi], fmt="o", color=col[c], label=NAMES[c], capsize=3)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels([l.replace("_and_", " & ").replace("_", " ") for l in labels], fontsize=8.5)
    ax.set_ylim(1, 5)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, ncol=3, loc="lower center", bbox_to_anchor=(0.5, 1.0))
    fig.tight_layout()
    for ext in ("png", "svg"):
        fig.savefig(out / "figures" / f"dimensions.{ext}", dpi=160)
    plt.close(fig)
    # 2b · pairwise preference with CI
    P = (S.get("pairwise") or {}).get(CONFIG["judges"]["pairwise"]["model"])
    if P:
        qs = ["overall", "coherence", "judgment", "evidence", "revision"]
        qlab = ["Overall", "Coherence (H1)", "Judgment (H2)", "Evidence (H3)", "Revision (H4)"]
        fig, ax = plt.subplots(figsize=(8.5, 3.8))
        cmps = [c for c in ("C-A", "C-B", "B-A") if c in P["by_comparison"]]
        pc = {"C-A": "#c2512f", "C-B": "#7a2f1c", "B-A": "#3b6ea8"}
        for k, cmp_ in enumerate(cmps):
            for i, q in enumerate(qs):
                d = P["by_comparison"][cmp_].get(q)
                if not d:
                    continue
                y = i + (k - 1) * 0.25
                ax.errorbar([d["score"]], [y], xerr=[[d["score"] - d["ci95"][0]], [d["ci95"][1] - d["score"]]], fmt="o",
                            color=pc[cmp_], capsize=3, label=(f"{cmp_[0]} vs {cmp_[2]}" if i == 0 else None))
        ax.axvline(0.5, color="#999", lw=1, ls="--")
        ax.set_yticks(range(len(qs)))
        ax.set_yticklabels(qlab)
        ax.invert_yaxis()
        ax.set_xlim(-0.02, 1.02)
        ax.set_xlabel("Preference for the first-named condition (0 = always loses, 0.5 = even, 1 = always wins)")
        ax.spines[["top", "right"]].set_visible(False)
        ax.legend(frameon=False, ncol=3, loc="lower center", bbox_to_anchor=(0.5, 1.0))
        fig.tight_layout()
        for ext in ("png", "svg"):
            fig.savefig(out / "figures" / f"pairwise.{ext}", dpi=160)
        plt.close(fig)
    # 3 · cost vs score
    fig, ax = plt.subplots(figsize=(6, 4))
    for c in CONDS:
        rc = [r for r in rows if r["condition"] == c and r.get(f"{primary}|weighted") is not None]
        ax.scatter([r["cost_usd"] for r in rc], [r[f"{primary}|weighted"] for r in rc], color=col[c], label=NAMES[c], s=26)
    ax.set_xscale("log")
    ax.set_xlabel("Generation cost per run, $ (list-price estimate, log scale)")
    ax.set_ylabel("Weighted score")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False)
    fig.tight_layout()
    for ext in ("png", "svg"):
        fig.savefig(out / "figures" / f"cost_vs_score.{ext}", dpi=160)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", required=True)
    a = ap.parse_args()
    analyse(a.phase)


if __name__ == "__main__":
    main()
