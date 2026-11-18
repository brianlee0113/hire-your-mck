"""Slide review for the H1 arm (METHODOLOGY.md §15): the source B deck and its two compiled versions, as slides.

Reuses make_slide_review.py (render, review app). Three pairs per case: B vs H1s, B vs H1r, H1s vs H1r. Questions
target usability, which the text judge cannot see: finding the key information, reading, deciding, editing.

  benchmark/.venv/bin/python benchmark/scripts/make_h1_review.py select|render|build|score [--answers FILE]
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
M.OUT = BENCH / "eval" / "dev-h1" / "human-slides"
SEED = 20261118
SOURCES = {"c2-profitability": ("main-c2-B-r3", "dev-h1-c2-H1s-r3", "dev-h1-c2-H1r-r3"),
           "c5-negative-entry": ("main-c5-B-r2", "dev-h1-c5-H1s-r2", "dev-h1-c5-H1r-r2")}
QUESTIONS = [
    ("find", "In which deck is it easier to find the key numbers and conditions behind the recommendation?"),
    ("understand", "Which deck is easier to read and understand?"),
    ("decide", "With which deck could the CEO make the decision faster?"),
    ("edit", "Which needs less editing before it could go out?"),
    ("overall", "Overall, which is the better deck for this decision?"),
]


def run_path(rid):
    phase = "dev-h1" if rid.startswith("dev-h1") else ("explore-c2" if rid.startswith("explore-c2") else "main")
    return BENCH / "runs" / phase / rid


M.run_path = run_path
M.HTML = (M.HTML.replace("'slide-review-v1'", "'slide-review-h1'")  # separate saved answers from the first review
          .replace("../../cases/", "../../../cases/").replace("../../answer_keys/", "../../../answer_keys/")
          .replace("<title>Slide review</title>", "<title>Slide review · H1</title>").replace("<b>Slide review</b>", "<b>Slide review · H1</b>"))


def select(_):
    rng = random.Random(SEED)
    letters = string.ascii_uppercase.replace("I", "").replace("O", "")
    decks, key, ids = [], {}, set()
    for case, rids in SOURCES.items():
        for rid, cond in zip(rids, ("B", "H1s", "H1r")):
            ext = json.loads((run_path(rid) / "extract" / "deck.json").read_text())
            while True:
                did = "T" + "".join(rng.choice(letters) for _ in range(3))
                if did not in ids:
                    ids.add(did)
                    break
            decks.append({"deck_id": did, "case": case, "n_slides": ext["n_slides"]})
            key[did] = {"run_id": rid, "condition": cond, "source": ext["source"], "format": ext["format"]}
    pairs = []
    for case in SOURCES:
        dc = {key[d["deck_id"]]["condition"]: d["deck_id"] for d in decks if d["case"] == case}
        for a, b in (("B", "H1s"), ("B", "H1r"), ("H1s", "H1r")):
            left, right = (dc[a], dc[b]) if rng.random() < 0.5 else (dc[b], dc[a])
            pairs.append({"case": case, "left": left, "right": right})
    rng.shuffle(pairs)
    for i, p in enumerate(pairs, 1):
        p["pair_id"] = f"P{i}"
    manifest = {"rule": "The two B decks of the first slide review (c2 r3, c5 r2) and their compiled versions; every pair within a case; sides and order random (seed %d)." % SEED,
                "seed": SEED, "cases": list(SOURCES), "questions": [{"id": q, "text": t} for q, t in QUESTIONS], "decks": decks, "pairs": pairs}
    M.OUT.mkdir(parents=True, exist_ok=True)
    (M.OUT / "manifest.json").write_text(json.dumps(manifest, indent=1))
    (M.OUT / "key.json").write_text(json.dumps(key, indent=1))
    print(f"{len(decks)} decks, {len(pairs)} pairs -> {M.OUT}")


def score(a):
    manifest = json.loads((M.OUT / "manifest.json").read_text())
    key = json.loads((M.OUT / "key.json").read_text())
    ans = json.loads(pathlib.Path(a.answers).read_text())["answers"]
    L = ["# H1 slide review (author, not blind)", "", "| Pair | Case | Comparison | " + " | ".join(q for q, _ in QUESTIONS) + " | Strength |",
         "|---|---|---|" + "---|" * (len(QUESTIONS) + 1)]
    notes = []
    for p in sorted(manifest["pairs"], key=lambda p: (p["case"], p["pair_id"])):
        r = ans.get(p["pair_id"], {})
        side = {"X": key[p["left"]]["condition"], "Y": key[p["right"]]["condition"]}
        name = lambda v: side.get(v, "same" if v == "same" else "—")  # noqa: E731
        L.append(f"| {p['pair_id']} | {p['case']} | {side['X']} vs {side['Y']} | " + " | ".join(name(r.get(q)) for q, _ in QUESTIONS) + f" | {r.get('strength', '—')} |")
        notes += [f"**{p['pair_id']} ({p['case']}, X = {side['X']}, Y = {side['Y']})**", f"- Reason: {r.get('reason', '—')}",
                  f"- Missing from {side['X']}: {r.get('missing_x', '—')}", f"- Missing from {side['Y']}: {r.get('missing_y', '—')}", ""]
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
