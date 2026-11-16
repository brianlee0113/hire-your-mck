"""Build the dashboard's data files from the benchmark results (results/main, results/explore-c2)."""
import csv, json, pathlib, sys
B = pathlib.Path(sys.argv[1])            # benchmark/ directory
OUT = pathlib.Path(__file__).parent
CODE = pathlib.Path(__file__).read_text()
M = json.load(open(B / "results/main/summary.json"))
X = json.load(open(B / "results/explore-c2/summary.json"))
F, S = "claude-fable-5-2", "claude-sonnet-5-5"
NAME = {"A": "Vanilla", "B": "방법론 프롬프트", "C": "스킬 · 딥덱", "C2": "스킬 · full deck"}

def write(name, rows, inputs):
    meta = [{"label": "build_dash_data.py", "value": CODE, "type": "code", "lang": "python"},
            {"label": "Input", "value": ", ".join(inputs)}]
    (OUT / f"{name}.json").write_text(json.dumps({"rows": rows, "meta": meta}, ensure_ascii=False, indent=1))

# 1. pairwise (Fable 5.2, both presentation orders, 15 replicate-matched pairs each)
pw = []
for src, comps, phase in ((M, ("C-A", "C-B", "B-A"), "main"), (X, ("C2-A", "C2-B", "C2-C"), "explore-c2")):
    for comp in comps:
        o = src["pairwise"][F]["by_comparison"][comp]["overall"]
        x, y = comp.split("-")
        c = o["consistent"]
        pw.append({"comparison": comp, "label": f"{NAME[x]} vs {NAME[y]}", "first": x, "second": y,
                   "wins": c["win"], "losses": c["loss"], "ties": c["tie"], "splits": c["split"], "pairs": o["n_pairs"],
                   "score": round(o["score"], 3), "ci_lo": round(o["ci95"][0], 3), "ci_hi": round(o["ci95"][1], 3),
                   "phase": phase, "exploratory": phase != "main"})
write("pairwise", pw, ["results/main/summary.json", "results/explore-c2/summary.json"])

# 2. weighted scores by condition and judge (mean, 95% hierarchical bootstrap)
sc = []
for jm, jl in ((F, "Fable 5.2 (주)"), (S, "Sonnet 5.5 (보조)")):
    for c in ("A", "B", "C"):
        w = M["by_judge"][jm]["by_condition"][c]["weighted"]
        sc.append({"judge": jl, "condition": c, "name": NAME[c], "weighted": round(w["mean"], 3), "ci_lo": round(w["ci95"][0], 3), "ci_hi": round(w["ci95"][1], 3)})
    bc = X["by_judge"][jm]["by_condition"]["C2"]
    sc.append({"judge": jl, "condition": "C2", "name": NAME["C2"], "weighted": round(bc["weighted"], 3), "ci_lo": round(bc["ci95"][0], 3), "ci_hi": round(bc["ci95"][1], 3)})
write("scores", sc, ["results/main/summary.json", "results/explore-c2/summary.json"])

# 3. per-dimension means (Fable 5.2)
DIMS = [("problem_framing", "문제 정의 (15%)"), ("storyline_coherence", "스토리라인 일관성 (25%)"), ("evidence_and_reasoning", "근거와 추론 (25%)"),
        ("strategic_judgment", "전략적 판단 (25%)"), ("clarity_and_concision", "명료성·간결성 (10%)")]
dm = []
for k, label in DIMS:
    r = {"dimension": label}
    for c in ("A", "B", "C"):
        r[c] = round(M["by_judge"][F]["by_condition"][c][k]["mean"], 2)
    r["C2"] = round(X["by_judge"][F]["by_condition"]["C2"][k], 2)
    dm.append(r)
write("dimensions", dm, ["results/main/summary.json", "results/explore-c2/summary.json"])

# 4. one row per document: length, cost, primary-judge weighted score
docs = []
for p in ("results/main/per_doc.csv", "results/explore-c2/per_doc.csv"):
    for r in csv.DictReader(open(B / p)):
        docs.append({"run_id": r["run_id"], "case": r["case"], "condition": r["condition"], "name": NAME[r["condition"]], "rep": int(r["rep"]),
                     "slides": int(r["slides"]), "words": int(r["words"]), "cost_usd": round(float(r["cost_usd"]), 2),
                     "minutes": round(float(r["duration_min"]), 1), "weighted": round(float(r[F + "|weighted"]), 2)})
write("docs", docs, ["results/main/per_doc.csv", "results/explore-c2/per_doc.csv"])
print({k: len(v) for k, v in (("pairwise", pw), ("scores", sc), ("dimensions", dm), ("docs", docs))})
