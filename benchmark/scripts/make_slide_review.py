"""Slide-based human review (exploratory direction check, not part of the pre-registered design).

The pre-registered human package (make_human_eval.py) shows normalised text with formatting removed. This one shows
the decks as rendered slides, because the open question after the main and C2 results is whether a human reading
the actual deck agrees with the automated pairwise judge.

Steps
  select   seeded choice of 2 cases and one replicate per case; conditions B, C and C2; writes manifest + key
  render   PowerPoint (AppleScript) -> PDF -> JPEG per slide; a PDF deliverable is rasterised directly
  build    writes index.html (pairwise review app; autosaves to localStorage, exports JSON)
  score    unblinds an exported JSON and compares it with the Fable 5.2 pairwise verdicts on the same pairs

Run with the benchmark venv:  benchmark/.venv/bin/python benchmark/scripts/make_slide_review.py <step> [...]
"""
import argparse
import json
import random
import shutil
import string
import subprocess
import sys
import time
from pathlib import Path

BENCH = Path(__file__).resolve().parents[1]
OUT = BENCH / "eval" / "human-slides"
SEED = 20261116
CASES = ["c1-market-entry", "c2-profitability", "c3-ai-assistant", "c4-pricing-churn", "c5-negative-entry"]
CONDS = ["B", "C", "C2"]
PPT_DATA = Path.home() / "Library/Containers/com.microsoft.Powerpoint/Data"
IMG_WIDTH = 1600

QUESTIONS = [
    ("send", "If one of these had to go to the CEO tonight, which would you send?"),
    ("decide", "With which deck could the CEO make the decision faster?"),
    ("complete", "Which gives the CEO more of what they need to decide: options compared, sensitivities, downside case, decision gates?"),
    ("edit", "Which needs less editing before it could go out?"),
    ("overall", "Overall, which is the better deck for this decision?"),
]


def run_id(case, cond, rep):
    phase = "explore-c2" if cond == "C2" else "main"
    return f"{phase}-{case.split('-')[0]}-{cond}-r{rep}"


def select(_):
    rng = random.Random(SEED)
    cases = sorted(rng.sample(CASES, 2))
    reps = {c: rng.choice([1, 2, 3]) for c in cases}
    letters = string.ascii_uppercase.replace("I", "").replace("O", "")
    ids = set()
    decks, key = [], {}
    for case in cases:
        for cond in CONDS:
            while True:
                did = "S" + "".join(rng.choice(letters) for _ in range(3))
                if did not in ids:
                    ids.add(did)
                    break
            rid = run_id(case, cond, reps[case])
            ext = json.loads((run_path(rid) / "extract" / "deck.json").read_text())
            decks.append({"deck_id": did, "case": case, "n_slides": ext["n_slides"]})
            key[did] = {"run_id": rid, "condition": cond, "source": ext["source"], "format": ext["format"]}
    pairs = []
    for case in cases:
        dc = {key[d["deck_id"]]["condition"]: d["deck_id"] for d in decks if d["case"] == case}
        for a, b in (("B", "C"), ("B", "C2"), ("C", "C2")):
            left, right = (dc[a], dc[b]) if rng.random() < 0.5 else (dc[b], dc[a])
            pairs.append({"case": case, "left": left, "right": right})
    rng.shuffle(pairs)
    for i, p in enumerate(pairs, 1):
        p["pair_id"] = f"P{i}"
    manifest = {
        "created": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "rule": f"random.Random({SEED}): sample 2 of the 5 cases, then one replicate per case; conditions B, C, C2 at "
                "that replicate (replicate-matched, as in the automated pairwise judging). Deck ids, left/right side "
                "and pair order are random from the same generator.",
        "seed": SEED, "cases": cases, "replicates": reps,
        "questions": [{"id": q, "text": t} for q, t in QUESTIONS],
        "decks": decks, "pairs": pairs,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=1))
    (OUT / "key.json").write_text(json.dumps(key, indent=1))
    print(f"cases {cases}, replicates {reps}; {len(decks)} decks, {len(pairs)} pairs -> {OUT}")


def run_path(rid):
    phase = "explore-c2" if rid.startswith("explore-c2") else "main"
    return BENCH / "runs" / phase / rid


def osa(script, timeout=180):
    r = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=timeout)
    if r.returncode:
        raise RuntimeError(r.stderr.strip())
    return r.stdout.strip()


def pptx_to_pdf(src, stem):
    """Export by presentation name (not 'active presentation') so another open deck is never exported instead."""
    PPT_DATA.mkdir(parents=True, exist_ok=True)
    tmp = PPT_DATA / f"{stem}.pptx"
    pdf = PPT_DATA / f"{stem}.pdf"
    shutil.copy2(src, tmp)
    pdf.unlink(missing_ok=True)
    osa(f'''tell application "Microsoft PowerPoint"
    open POSIX file "{tmp}"
    delay 4
    save presentation "{tmp.name}" in POSIX file "{pdf}" as save as PDF
    close presentation "{tmp.name}" saving no
end tell''', timeout=300)
    for _ in range(30):
        if pdf.exists() and pdf.stat().st_size > 0:
            break
        time.sleep(1)
    tmp.unlink(missing_ok=True)
    if not pdf.exists():
        raise RuntimeError(f"PowerPoint did not write {pdf}")
    return pdf


def rasterise(pdf, dest):
    import pymupdf
    dest.mkdir(parents=True, exist_ok=True)
    for old in dest.glob("*.jpg"):
        old.unlink()
    doc = pymupdf.open(pdf)
    names = []
    for i, page in enumerate(doc, 1):
        zoom = IMG_WIDTH / page.rect.width
        pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom))
        name = f"s{i:02d}.jpg"
        pix.save(dest / name, jpg_quality=82)
        names.append(name)
    return names


def render(_):
    manifest = json.loads((OUT / "manifest.json").read_text())
    key = json.loads((OUT / "key.json").read_text())
    for d in manifest["decks"]:
        k = key[d["deck_id"]]
        src = run_path(k["run_id"]) / "workspace" / "deliverable" / k["source"]
        if not src.exists():
            sys.exit(f"missing deliverable {src}")
        stem = f"hr_{d['deck_id']}"
        print(f"{d['deck_id']}: {k['format']} ...", flush=True)
        pdf = src if k["format"] == "pdf" else pptx_to_pdf(src, stem)
        d["images"] = rasterise(pdf, OUT / "img" / d["deck_id"])
        if pdf.parent == PPT_DATA:
            pdf.unlink(missing_ok=True)
        if len(d["images"]) != d["n_slides"]:
            print(f"  warning: {len(d['images'])} pages rendered, extraction counted {d['n_slides']} slides")
        print(f"  {len(d['images'])} slides")
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=1))


HTML = r"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Slide review</title>
<style>
:root{--ink:#14202b;--mute:#5d6b78;--line:#d9dfe5;--bg:#f5f7f9;--acc:#2450c8}
*{box-sizing:border-box}body{margin:0;font:14px/1.45 -apple-system,system-ui,sans-serif;color:var(--ink);background:var(--bg)}
header{position:sticky;top:0;z-index:5;background:#fff;border-bottom:1px solid var(--line);padding:8px 14px;display:flex;gap:12px;align-items:center;flex-wrap:wrap}
header b{font-size:15px}header .sp{flex:1}button{font:inherit;padding:5px 11px;border:1px solid var(--line);background:#fff;border-radius:6px;cursor:pointer}
button.primary{background:var(--acc);color:#fff;border-color:var(--acc)}.mute{color:var(--mute)}
main{display:grid;grid-template-columns:1fr 1fr 360px;gap:10px;padding:10px;height:calc(100vh - 50px)}
.deck{background:#fff;border:1px solid var(--line);border-radius:8px;overflow-y:auto;padding:8px}
.deck h2{position:sticky;top:-8px;background:#fff;margin:-8px -8px 8px;padding:8px;border-bottom:1px solid var(--line);font-size:15px}
.deck img{width:100%;display:block;margin:0 0 8px;border:1px solid var(--line);cursor:zoom-in}
.form{background:#fff;border:1px solid var(--line);border-radius:8px;overflow-y:auto;padding:12px}
.q{margin:0 0 14px}.q p{margin:0 0 5px;font-weight:600}.opts{display:flex;gap:6px}.opts label{flex:1;border:1px solid var(--line);border-radius:6px;padding:5px;text-align:center;cursor:pointer}
.opts input{display:none}.opts input:checked+span{font-weight:700;color:var(--acc)}.opts label:has(input:checked){border-color:var(--acc);background:#eef2fd}
textarea{width:100%;min-height:54px;font:inherit;border:1px solid var(--line);border-radius:6px;padding:6px}
#zoom{display:none;position:fixed;inset:0;background:rgba(10,15,20,.88);z-index:9;align-items:center;justify-content:center;cursor:zoom-out}#zoom img{max-width:96vw;max-height:96vh}
.done{color:#1b7f3b}
</style></head><body>
<header><b>Slide review</b><span id="pos" class="mute"></span><span id="case" class="mute"></span>
<a id="pack" target="_blank">briefing pack</a><a id="keyl" target="_blank" class="mute">answer key</a>
<span class="sp"></span><span id="prog" class="mute"></span>
<button id="prev">← Prev</button><button id="next">Next →</button><button id="exp" class="primary">Export JSON</button></header>
<main><section class="deck" id="L"></section><section class="deck" id="R"></section><section class="form" id="F"></section></main>
<div id="zoom"><img></div>
<script>
const M = __MANIFEST__;
const QS = M.questions;
const ST = 'slide-review-v1';
let S = JSON.parse(localStorage.getItem(ST) || '{"answers":{}}'), i = 0, t0 = Date.now();
const deck = id => M.decks.find(d => d.deck_id === id);
const $ = s => document.querySelector(s);
function save(){localStorage.setItem(ST, JSON.stringify(S))}
function tick(){const p = M.pairs[i]; const a = S.answers[p.pair_id] = S.answers[p.pair_id] || {}; a.seconds = (a.seconds || 0) + Math.round((Date.now() - t0) / 1000); t0 = Date.now(); save()}
function complete(p){const a = S.answers[p.pair_id] || {}; return QS.every(q => a[q.id]) && a.strength}
function col(el, id, side){const d = deck(id); el.innerHTML = `<h2>Deck ${side} <span class="mute">· ${d.images.length} slides</span></h2>` +
  d.images.map(n => `<img loading="lazy" src="img/${id}/${n}">`).join('')}
function opt(name, val, label, cur){return `<label><input type="radio" name="${name}" value="${val}" ${cur === val ? 'checked' : ''}><span>${label}</span></label>`}
function render(){
  const p = M.pairs[i], a = S.answers[p.pair_id] || {};
  $('#pos').textContent = `Pair ${i + 1} of ${M.pairs.length}`;
  $('#case').textContent = p.case;
  $('#pack').href = `../../cases/${p.case}/packet.md`; $('#keyl').href = `../../answer_keys/${p.case}.md`;
  $('#prog').innerHTML = M.pairs.map(q => complete(q) ? '<span class="done">●</span>' : '○').join(' ');
  col($('#L'), p.left, 'X'); col($('#R'), p.right, 'Y');
  $('#L').scrollTop = 0; $('#R').scrollTop = 0;
  let h = QS.map(q => `<div class="q"><p>${q.text}</p><div class="opts">${opt(q.id, 'X', 'X', a[q.id])}${opt(q.id, 'same', 'About the same', a[q.id])}${opt(q.id, 'Y', 'Y', a[q.id])}</div></div>`).join('');
  h += `<div class="q"><p>How strong is your overall preference?</p><div class="opts">${['slight', 'clear', 'strong'].map(v => opt('strength', v, v, a.strength)).join('')}</div></div>`;
  h += `<div class="q"><p>What important option, risk or evidence is missing from X?</p><textarea data-k="missing_x">${a.missing_x || ''}</textarea></div>`;
  h += `<div class="q"><p>…and from Y?</p><textarea data-k="missing_y">${a.missing_y || ''}</textarea></div>`;
  h += `<div class="q"><p>Main reason for your overall choice</p><textarea data-k="reason">${a.reason || ''}</textarea></div>`;
  h += `<div class="q"><p>Did you recognise which system made either deck?</p><div class="opts">${opt('recognised', 'no', 'No', a.recognised)}${opt('recognised', 'one', 'One of them', a.recognised)}${opt('recognised', 'both', 'Both', a.recognised)}</div></div>`;
  $('#F').innerHTML = h;
  $('#F').querySelectorAll('input').forEach(el => el.onchange = () => {tick(); S.answers[p.pair_id][el.name] = el.value; save(); $('#prog').innerHTML = M.pairs.map(q => complete(q) ? '<span class="done">●</span>' : '○').join(' ')});
  $('#F').querySelectorAll('textarea').forEach(el => el.oninput = () => {const x = S.answers[p.pair_id] = S.answers[p.pair_id] || {}; x[el.dataset.k] = el.value; save()});
}
$('#prev').onclick = () => {tick(); i = Math.max(0, i - 1); render()};
$('#next').onclick = () => {tick(); i = Math.min(M.pairs.length - 1, i + 1); render()};
document.addEventListener('click', e => {if (e.target.matches('.deck img')) {$('#zoom img').src = e.target.src; $('#zoom').style.display = 'flex'}});
$('#zoom').onclick = () => $('#zoom').style.display = 'none';
document.addEventListener('keydown', e => {if (e.key === 'Escape') $('#zoom').style.display = 'none'});
$('#exp').onclick = () => {tick(); const blob = new Blob([JSON.stringify({manifest_created: M.created, exported: new Date().toISOString(), answers: S.answers}, null, 1)], {type: 'application/json'});
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'slide-review-answers.json'; a.click()};
render();
</script></body></html>
"""


def build(_):
    manifest = json.loads((OUT / "manifest.json").read_text())
    if not all(d.get("images") for d in manifest["decks"]):
        sys.exit("render first")
    (OUT / "index.html").write_text(HTML.replace("__MANIFEST__", json.dumps(manifest)))
    print(f"wrote {OUT / 'index.html'}")


def judge_verdicts(rid_x, rid_y):
    """Fable 5.2 pairwise verdicts for two runs, in both presentation orders."""
    keys = {}
    for ph in ("main", "explore-c2"):
        keys.update({v: (k, ph) for k, v in json.loads((BENCH / "eval" / ph / "blinding_key.json").read_text()).items()})
    bx, by = keys[rid_x][0], keys[rid_y][0]
    out = []
    for ph in ("main", "explore-c2"):
        for a, b in ((bx, by), (by, bx)):
            f = BENCH / "eval" / ph / "pairwise" / "claude-fable-5-2" / f"{a}__{b}.json"
            if f.exists():
                o = json.loads(f.read_text())["output"]
                out.append({q: (None if o[q]["winner"] == "tie" else (rid_x if (o[q]["winner"] == "X") == (a == bx) else rid_y))
                            for q in ("overall", "judgment", "evidence", "coherence")})
    return out


def score(a):
    manifest = json.loads((OUT / "manifest.json").read_text())
    key = json.loads((OUT / "key.json").read_text())
    ans = json.loads(Path(a.answers).read_text())["answers"]
    rows, agree = [], {"overall": [0, 0]}
    lines = ["# Slide review: human vs automated pairwise judge", "",
             f"Selection: {manifest['rule']} Cases {manifest['cases']}, replicates {manifest['replicates']}.", "",
             "Exploratory, one reviewer (the skill's author, not blind to its style). Read as a direction check only.", "",
             "| Pair | Case | Comparison | Human overall | Strength | Send | Decide | Complete | Edit less | Judge overall (both orders) | Agree |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for p in sorted(manifest["pairs"], key=lambda p: (p["case"], p["pair_id"])):
        r = ans.get(p["pair_id"], {})
        side = {"X": key[p["left"]], "Y": key[p["right"]]}
        name = lambda v: "same" if v == "same" else (side[v]["condition"] if v in side else "—")
        conds = sorted([side["X"]["condition"], side["Y"]["condition"]], key=CONDS.index)
        jv = judge_verdicts(side["X"]["run_id"], side["Y"]["run_id"])
        cond_of = {side["X"]["run_id"]: side["X"]["condition"], side["Y"]["run_id"]: side["Y"]["condition"]}
        jw = [cond_of.get(v["overall"], "tie") for v in jv]
        human = name(r.get("overall"))
        ag = "—"
        if jw and human in conds and len(set(jw)) == 1:
            ag = "yes" if jw[0] == human else "no"
            agree["overall"][0] += ag == "yes"
            agree["overall"][1] += 1
        lines.append(f"| {p['pair_id']} | {p['case']} | {conds[0]} vs {conds[1]} | {human} | {r.get('strength', '—')} | "
                     + " | ".join(name(r.get(q)) for q in ("send", "decide", "complete", "edit"))
                     + f" | {', '.join(jw) or 'n/a'} | {ag} |")
        rows.append({"pair": p["pair_id"], "case": p["case"], "conditions": conds, "human": r, "judge_overall": jw,
                     "x": side["X"], "y": side["Y"]})
    n_ok, n = agree["overall"]
    lines += ["", f"Overall agreement with the judge where both judge orders agree: {n_ok} of {n}.", "", "## Notes", ""]
    for r in rows:
        h = r["human"]
        cx, cy = r["x"]["condition"], r["y"]["condition"]
        lines += [f"**{r['pair']} ({r['case']}, X = {cx}, Y = {cy})** · {h.get('seconds', 0) // 60} min",
                  f"- Reason: {h.get('reason', '').strip() or '—'}",
                  f"- Missing from {cx}: {h.get('missing_x', '').strip() or '—'}",
                  f"- Missing from {cy}: {h.get('missing_y', '').strip() or '—'}",
                  f"- Recognised: {h.get('recognised', '—')}", ""]
    (OUT / "results.md").write_text("\n".join(lines))
    (OUT / "results.json").write_text(json.dumps(rows, indent=1))
    print("\n".join(lines[:len(manifest['pairs']) + 8]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["select", "render", "build", "score"])
    ap.add_argument("--answers", help="exported JSON (score)")
    a = ap.parse_args()
    {"select": select, "render": render, "build": build, "score": score}[a.step](a)


if __name__ == "__main__":
    main()
