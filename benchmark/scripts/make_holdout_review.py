"""Author's slide review for the holdout (METHODOLOGY.md §16): B, E1 and H2a decks as rendered slides, blind to condition.

Done before any automated verdict for the holdout is seen. Reuses make_slide_review.py (render, review app). Three
pairs per case (B vs H2a, E1 vs H2a, E1 vs B), 6 cases, 18 pairs. Questions are the H1 usability questions.
Output lives outside eval/holdout so the review page never links to judge files.

  benchmark/.venv/bin/python benchmark/scripts/make_holdout_review.py select|render|build|score [--answers FILE]
"""
import argparse
import json
import pathlib
import random
import string
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import make_slide_review as M  # noqa: E402

BENCH = M.BENCH
M.OUT = BENCH / "eval" / "holdout-slides"
SEED = 20261121
CASES = ["c6-make-buy", "c7-m-and-a", "c8-distribution-network", "c9-capacity-timing", "c10-portfolio-exit", "c11-oem-licensing"]
CONDS = ["B", "E1", "H2a"]
QUESTIONS = [
    ("find", "In which deck is it easier to find the key numbers and conditions behind the recommendation?"),
    ("understand", "Which deck is easier to read and understand?"),
    ("decide", "With which deck could the CEO make the decision faster?"),
    ("edit", "Which needs less editing before it could go out?"),
    ("overall", "Overall, which is the better deck for this decision?"),
]


def run_path(rid):
    return BENCH / "runs" / "holdout" / rid


def rid(case, cond):
    return f"holdout-{case.split('-')[0]}-{cond}-r1"


M.run_path = run_path
M.HTML = (M.HTML.replace("'slide-review-v1'", "'slide-review-holdout'")
          .replace("<title>Slide review</title>", "<title>Slide review · holdout</title>")
          .replace("<b>Slide review</b>", "<b>Slide review · holdout</b>"))


def select(_):
    rng = random.Random(SEED)
    letters = string.ascii_uppercase.replace("I", "").replace("O", "")
    decks, key, ids = [], {}, set()
    for case in CASES:
        for cond in CONDS:
            r = rid(case, cond)
            ext = json.loads((run_path(r) / "extract" / "deck.json").read_text())
            while True:
                did = "K" + "".join(rng.choice(letters) for _ in range(3))
                if did not in ids:
                    ids.add(did)
                    break
            decks.append({"deck_id": did, "case": case, "n_slides": ext["n_slides"]})
            key[did] = {"run_id": r, "condition": cond, "source": ext["source"], "format": ext["format"]}
    rng.shuffle(decks)  # deck order in the manifest says nothing about condition
    pairs = []
    for case in CASES:
        dc = {key[d["deck_id"]]["condition"]: d["deck_id"] for d in decks if d["case"] == case}
        for a, b in (("B", "H2a"), ("E1", "H2a"), ("E1", "B")):
            left, right = (dc[a], dc[b]) if rng.random() < 0.5 else (dc[b], dc[a])
            pairs.append({"case": case, "left": left, "right": right})
    rng.shuffle(pairs)
    for i, p in enumerate(pairs, 1):
        p["pair_id"] = f"P{i}"
    manifest = {"rule": "All 18 holdout decks (6 cases x B, E1, H2a, replicate 1); every pair within a case; deck ids, sides and pair order random (seed %d)." % SEED,
                "seed": SEED, "cases": CASES, "questions": [{"id": q, "text": t} for q, t in QUESTIONS], "decks": decks, "pairs": pairs}
    M.OUT.mkdir(parents=True, exist_ok=True)
    (M.OUT / "manifest.json").write_text(json.dumps(manifest, indent=1))
    (M.OUT / "key.json").write_text(json.dumps(key, indent=1))
    print(f"{len(decks)} decks, {len(pairs)} pairs -> {M.OUT}")


def score(a):
    manifest = json.loads((M.OUT / "manifest.json").read_text())
    key = json.loads((M.OUT / "key.json").read_text())
    ans = json.loads(pathlib.Path(a.answers).read_text())["answers"]
    L = ["# Holdout slide review (author, blind to condition)", "", manifest["rule"], "",
         "| Pair | Case | Comparison | " + " | ".join(q for q, _ in QUESTIONS) + " | Strength | Recognised |",
         "|---|---|---|" + "---|" * (len(QUESTIONS) + 2)]
    notes = []
    for p in sorted(manifest["pairs"], key=lambda p: (CASES.index(p["case"]), p["pair_id"])):
        r = ans.get(p["pair_id"], {})
        side = {"X": key[p["left"]]["condition"], "Y": key[p["right"]]["condition"]}
        name = lambda v: side.get(v, "same" if v == "same" else "—")  # noqa: E731
        L.append(f"| {p['pair_id']} | {p['case']} | {side['X']} vs {side['Y']} | " + " | ".join(name(r.get(q)) for q, _ in QUESTIONS)
                 + f" | {r.get('strength', '—')} | {r.get('recognised', '—')} |")
        notes += [f"**{p['pair_id']} ({p['case']}, X = {side['X']}, Y = {side['Y']})** · {r.get('seconds', 0) // 60} min",
                  f"- Reason: {r.get('reason', '—')}", f"- Missing from {side['X']}: {r.get('missing_x', '—')}",
                  f"- Missing from {side['Y']}: {r.get('missing_y', '—')}", ""]
    (M.OUT / "results.md").write_text("\n".join(L + ["", "## Notes", ""] + notes))
    print("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["select", "render", "build", "score"])
    ap.add_argument("--answers")
    a = ap.parse_args()
    {"select": select, "render": M.render, "build": M.build, "score": score}[a.step](a)


if __name__ == "__main__":
    main()
