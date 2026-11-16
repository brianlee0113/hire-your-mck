"""Pick representative comparisons by fixed rules (no hand-picking) and write results/<phase>/examples.md.

Rules, on the primary judge's weighted score, per case and replicate (rep-matched trio A, B, C):
  margin = C − max(A, B)
  · "Hire Your McK best"      the trio with the largest margin
  · "about the same"          the trio with the margin closest to 0
  · "Hire Your McK worst"     the trio with the smallest margin
  · "substantive error (C)"   the C document with the most numerical errors + contradictions (primary judge)
  · "substantive error (baseline)" the same for A/B, for balance
Each example shows the governing thought, recommendation and slide count for each document, and the judge's
rationales, quoted verbatim.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import BENCH, CONFIG  # noqa: E402

W = {"problem_framing": 0.15, "storyline_coherence": 0.25, "evidence_and_reasoning": 0.25, "strategic_judgment": 0.25,
     "clarity_and_concision": 0.10}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", default="main")
    a = ap.parse_args()
    jm = CONFIG["judges"]["primary"]["model"]
    key = json.loads((BENCH / "eval" / a.phase / "blinding_key.json").read_text())
    docs = {}
    for bid, rid in key.items():
        jp = BENCH / "eval" / a.phase / "auto" / jm / f"{bid}.json"
        if not jp.exists():
            continue
        o = json.loads(jp.read_text())["output"]
        m = json.loads((BENCH / "runs" / a.phase / rid / "meta.json").read_text())
        n = json.loads((BENCH / "runs" / a.phase / rid / "normalized.json").read_text()).get("normalized") or {}
        e = json.loads((BENCH / "runs" / a.phase / rid / "e2e.json").read_text())
        docs[rid] = {"bid": bid, "case": m["case"], "cond": m["condition"], "rep": m["rep"], "o": o, "n": n, "e": e,
                     "w": sum(W[k] * o["scores"][k]["score"] for k in W)}
    trios = {}
    for rid, d in docs.items():
        trios.setdefault((d["case"], d["rep"]), {})[d["cond"]] = d
    trios = {k: v for k, v in trios.items() if len(v) == 3}
    margin = {k: v["C"]["w"] - max(v["A"]["w"], v["B"]["w"]) for k, v in trios.items()}
    picks = [("Hire Your McK scored best relative to the baselines", max(margin, key=margin.get)),
             ("About the same", min(margin, key=lambda k: abs(margin[k]))),
             ("Hire Your McK scored worst relative to the baselines", min(margin, key=margin.get))]
    L = [f"# Representative examples · phase `{a.phase}`", "",
         "Chosen by fixed rules (see `scripts/examples.py`), not by hand. Quotes are verbatim from the decks and from the "
         f"primary judge (`{jm}`). Weighted scores are on 1–5.", ""]

    def doc_block(d):
        o = d["o"]
        out = [f"**{CONFIG['conditions'][d['cond']]['name']}** ({d['e']['slides']} slides, {d['e']['words']:,} words) — weighted {d['w']:.2f} "
               f"(framing {o['scores']['problem_framing']['score']}, coherence {o['scores']['storyline_coherence']['score']}, "
               f"evidence {o['scores']['evidence_and_reasoning']['score']}, judgment {o['scores']['strategic_judgment']['score']}, "
               f"clarity {o['scores']['clarity_and_concision']['score']})", "",
               f"> Governing thought: {d['n'].get('governing_thought') or '(none stated)'}", ">",
               f"> Recommendation: {(d['n'].get('recommendation') or '(none)')[:600]}", "",
               f"Judge on coherence: \"{o['scores']['storyline_coherence']['rationale']}\"", "",
               f"Judge on clarity: \"{o['scores']['clarity_and_concision']['rationale']}\"", ""]
        return out

    for title, k in picks:
        t = trios[k]
        L += [f"## {title}: {k[0]}, replicate {k[1]} (C − best baseline = {margin[k]:+.2f})", ""]
        for c in ("A", "B", "C"):
            L += doc_block(t[c])
    for title, pool in (("Substantive reasoning errors in a Hire Your McK deck", [d for d in docs.values() if d["cond"] == "C"]),
                        ("Substantive reasoning errors in a baseline deck", [d for d in docs.values() if d["cond"] != "C"])):
        d = max(pool, key=lambda d: (len(d["o"]["numerical_errors"]) + len(d["o"]["logical_contradictions"]), -d["w"]))
        L += [f"## {title}: {d['case']}, {CONFIG['conditions'][d['cond']]['name']}, replicate {d['rep']}", ""]
        L += [f"Weighted {d['w']:.2f}; {len(d['o']['numerical_errors'])} numerical errors, {len(d['o']['logical_contradictions'])} contradictions, "
              f"{len(d['o']['unsupported_claims'])} unsupported claims (primary judge).", ""]
        for x in d["o"]["numerical_errors"]:
            L.append(f"- Numerical error: \"{x['quote']}\" — judge: {x['correct']}")
        for x in d["o"]["logical_contradictions"]:
            L.append(f"- Contradiction: \"{x['quote_a']}\" vs \"{x['quote_b']}\" — judge: {x['why']}")
        L.append("")
    out = BENCH / "results" / a.phase / "examples.md"
    out.write_text("\n".join(L))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
