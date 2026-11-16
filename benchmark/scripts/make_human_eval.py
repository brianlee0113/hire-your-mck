"""Build the human-review package: a self-contained HTML scoring app and CSV forms, one random order per reviewer.

Usage: python benchmark/scripts/make_human_eval.py --phase main [--reviewers 3]
Writes eval/<phase>/human/index.html        open in a browser; scores stay in the browser and export as JSON
       eval/<phase>/human/forms/R<n>.csv   the same items as a spreadsheet, in that reviewer's order
       eval/<phase>/human/INSTRUCTIONS.md

Import finished scores with:  python benchmark/scripts/make_human_eval.py --phase main --import FILE ...
(JSON exported from the app, or a filled CSV). They are stored in eval/<phase>/human/scores/<reviewer>.json.
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import pathlib
import random
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import BENCH, CONFIG  # noqa: E402

DIMS = ["problem_framing", "storyline_coherence", "evidence_and_reasoning", "strategic_judgment", "clarity_and_concision"]
COUNTS = ["unsupported_claims", "numerical_errors", "logical_contradictions", "missed_critical_evidence"]
CATS = {"recommendation_defensible": ["yes", "partial", "no"], "hypothesis_handling_appropriate": ["yes", "partial", "no"],
        "key_tradeoffs_identified": ["all", "some", "none"]}

INSTRUCTIONS = """# Human review instructions

You will score anonymised strategy documents. Each answers a business decision from a synthetic briefing pack.
You see the pack, the evaluator's answer key, and the document (a normalised storyline followed by the full slide
text). Formatting has been removed on purpose: score the reasoning, not the look or the length.

1. Enter your reviewer id (R1, R2, R3 …). The app shows the documents in an order that is random for you.
2. Read the briefing pack once per case; it is the same for every document of that case.
3. Score the five dimensions 1–5 using the anchors (shown in the app; full text in `prompts/eval/rubric.md`).
4. Count unsupported claims, numerical errors, material contradictions and missed critical evidence items.
5. Judge whether the recommendation is defensible against the key's criteria (not against its preferred answer)
   and whether the initial hypothesis in the pack was handled appropriately.
6. Work independently: do not discuss documents with other reviewers until everyone has exported their scores.
7. Export your scores (button at the top) and send the JSON file to the study owner.

Do not try to guess which system produced a document. If you think you recognise one, note it in the comment field.
Budget about 20–30 minutes per document; long documents may take longer.
"""


def items(phase):
    out = []
    bdir = BENCH / "eval" / phase / "blinded"
    for p in sorted(bdir.glob("*.json")):
        info = json.loads(p.read_text())
        out.append({"id": info["blind_id"], "case": info["case"], "words": info["words"],
                    "doc": (bdir / f"{info['blind_id']}.md").read_text()})
    return out


def build(phase, n_reviewers):
    out = BENCH / "eval" / phase / "human"
    (out / "forms").mkdir(parents=True, exist_ok=True)
    its = items(phase)
    cases = sorted({i["case"] for i in its})
    packets = {c: (BENCH / "cases" / c / "packet.md").read_text() for c in cases}
    keys = {c: (BENCH / "answer_keys" / f"{c}.md").read_text() for c in cases}
    rubric = (BENCH / "prompts" / "eval" / "rubric.md").read_text()
    orders = {}
    for r in range(1, n_reviewers + 1):
        ids = [i["id"] for i in its]
        random.Random(CONFIG["seeds"]["human_order"] * 100 + r).shuffle(ids)
        orders[f"R{r}"] = ids
        with open(out / "forms" / f"R{r}.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["reviewer", "order", "blind_id", "case"] + DIMS + COUNTS + list(CATS) + ["comment"])
            case_of = {i["id"]: i["case"] for i in its}
            for k, bid in enumerate(ids, 1):
                w.writerow([f"R{r}", k, bid, case_of[bid]] + [""] * (len(DIMS) + len(COUNTS) + len(CATS) + 1))
    data = {"items": its, "packets": packets, "keys": keys, "rubric": rubric, "orders": orders, "dims": DIMS,
            "counts": COUNTS, "cats": CATS, "phase": phase}
    page = TEMPLATE.replace("/*DATA*/", json.dumps(data).replace("</", "<\\/"))
    (out / "index.html").write_text(page)
    (out / "INSTRUCTIONS.md").write_text(INSTRUCTIONS)
    print(f"{len(its)} items, {n_reviewers} reviewer orders → {out}")


def import_scores(phase, files):
    dst = BENCH / "eval" / phase / "human" / "scores"
    dst.mkdir(parents=True, exist_ok=True)
    for f in files:
        f = pathlib.Path(f)
        if f.suffix == ".json":
            d = json.loads(f.read_text())
            reviewer, rows = d["reviewer"], d["scores"]
        else:
            rows, reviewer = {}, None
            for r in csv.DictReader(open(f)):
                reviewer = r["reviewer"]
                if not r.get(DIMS[0]):
                    continue
                rows[r["blind_id"]] = {k: (int(r[k]) if k in DIMS + COUNTS and r[k] != "" else r[k]) for k in DIMS + COUNTS + list(CATS) + ["comment"]}
        (dst / f"{reviewer}.json").write_text(json.dumps({"reviewer": reviewer, "scores": rows}, indent=1))
        print(f"imported {len(rows)} scores from {reviewer}")


TEMPLATE = r"""<!doctype html><html><head><meta charset="utf-8"><title>Blind review · strategy documents</title>
<style>
body{font:15px/1.5 -apple-system,Segoe UI,Arial,sans-serif;margin:0;color:#1b2430;background:#f6f7f9}
header{position:sticky;top:0;background:#0b1f33;color:#fff;padding:10px 18px;display:flex;gap:14px;align-items:center;z-index:5}
header input,header select,header button{font:inherit;padding:4px 8px}
main{display:grid;grid-template-columns:1fr 420px;gap:18px;padding:18px;max-width:1500px;margin:auto}
.doc,.form{background:#fff;border:1px solid #d9dee5;border-radius:6px;padding:16px 20px}
.doc pre{white-space:pre-wrap;font:13.5px/1.5 ui-monospace,Menlo,monospace}
.form{position:sticky;top:64px;align-self:start;max-height:calc(100vh - 90px);overflow:auto}
details{margin:8px 0}summary{cursor:pointer;font-weight:600}
.dim{margin:10px 0}.dim label{margin-right:10px}.muted{color:#5b6775;font-size:13px}
.saved{color:#2e7d32;font-weight:600}
</style></head><body>
<header><b>Blind review</b>
Reviewer <input id="rev" size="4" placeholder="R1">
<button id="prev">◀</button><span id="pos"></span><button id="next">▶</button>
<span id="bid"></span><span id="status"></span>
<button id="export" style="margin-left:auto">Export my scores (JSON)</button></header>
<main><section class="doc">
<details><summary>Briefing pack (same for every document of this case)</summary><pre id="packet"></pre></details>
<details><summary>Evaluator's answer key</summary><pre id="key"></pre></details>
<details><summary>Rubric and anchors</summary><pre id="rubric"></pre></details>
<h3>Document</h3><pre id="doc"></pre></section>
<section class="form" id="form"></section></main>
<script>
const D=/*DATA*/;
let rev=localStorage.getItem('rev')||'', idx=0;
const $=s=>document.querySelector(s);
function order(){return D.orders[rev]||D.items.map(i=>i.id)}
function store(){return JSON.parse(localStorage.getItem('scores-'+rev)||'{}')}
function save(s){localStorage.setItem('scores-'+rev,JSON.stringify(s))}
function render(){
  $('#rev').value=rev; const ids=order(); const id=ids[idx]; const it=D.items.find(i=>i.id==id);
  $('#pos').textContent=(idx+1)+' / '+ids.length; $('#bid').textContent=id+' · '+it.case+' · '+it.words+' words';
  $('#packet').textContent=D.packets[it.case]; $('#key').textContent=D.keys[it.case]; $('#rubric').textContent=D.rubric; $('#doc').textContent=it.doc;
  const s=store()[id]||{}; let h='<h3>Scores for '+id+'</h3><p class="muted">1 = poor · 3 = adequate · 5 = excellent (anchors in the rubric)</p>';
  for(const d of D.dims){h+='<div class="dim"><b>'+d.replace(/_/g,' ')+'</b><br>';for(let v=1;v<=5;v++)h+='<label><input type="radio" name="'+d+'" value="'+v+'"'+(s[d]==v?' checked':'')+'> '+v+'</label>';h+='</div>'}
  for(const c of D.counts)h+='<div class="dim"><b>'+c.replace(/_/g,' ')+'</b> <input type="number" min="0" name="'+c+'" value="'+(s[c]??'')+'" style="width:5em"></div>';
  for(const [c,opts] of Object.entries(D.cats)){h+='<div class="dim"><b>'+c.replace(/_/g,' ')+'</b><br>';for(const o of opts)h+='<label><input type="radio" name="'+c+'" value="'+o+'"'+(s[c]==o?' checked':'')+'> '+o+'</label>';h+='</div>'}
  h+='<div class="dim"><b>comment</b><br><textarea name="comment" rows="5" style="width:100%">'+(s.comment||'')+'</textarea></div><button id="save">Save</button> <span id="ok"></span>';
  $('#form').innerHTML=h; $('#save').onclick=()=>{const all=store();const r={};
    for(const d of D.dims){const e=document.querySelector('input[name='+d+']:checked');if(e)r[d]=+e.value}
    for(const c of D.counts){const e=document.querySelector('input[name='+c+']');if(e.value!=='')r[c]=+e.value}
    for(const c of Object.keys(D.cats)){const e=document.querySelector('input[name='+c+']:checked');if(e)r[c]=e.value}
    r.comment=document.querySelector('textarea[name=comment]').value; r.saved_at=new Date().toISOString();
    all[id]=r; save(all); $('#ok').innerHTML='<span class="saved">saved</span>'; status()};
  status(); window.scrollTo(0,0)}
function status(){const n=Object.keys(store()).length;$('#status').textContent=n+' scored'}
$('#rev').onchange=e=>{rev=e.target.value.trim();localStorage.setItem('rev',rev);idx=0;render()};
$('#prev').onclick=()=>{idx=Math.max(0,idx-1);render()};
$('#next').onclick=()=>{idx=Math.min(order().length-1,idx+1);render()};
$('#export').onclick=()=>{const b=new Blob([JSON.stringify({reviewer:rev,phase:D.phase,scores:store()},null,1)],{type:'application/json'});
  const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='human-scores-'+rev+'.json';a.click()};
render();
</script></body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", default="main")
    ap.add_argument("--reviewers", type=int, default=3)
    ap.add_argument("--import", dest="imp", nargs="*")
    a = ap.parse_args()
    if a.imp:
        import_scores(a.phase, a.imp)
    else:
        build(a.phase, a.reviewers)


if __name__ == "__main__":
    main()
