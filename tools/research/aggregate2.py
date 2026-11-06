"""Aggregate round-1 + round-2 tagging with recency weighting, style rules from recent decks only.

Usage: python aggregate2.py --r1-sources SRC.md --r1 r1/*.jsonl --r2 r2/group-*.jsonl --style r2/group-N-style.jsonl
       [--exclude-style r2-090,...] [--half-life 5] [--ref-year 2025] [--json out.json]
"""
import argparse, json, re, glob, collections as C, statistics as S

ap = argparse.ArgumentParser()
ap.add_argument("--r1-sources"); ap.add_argument("--r1", nargs="*", default=[]); ap.add_argument("--r2", nargs="*", default=[])
ap.add_argument("--style", nargs="*", default=[]); ap.add_argument("--exclude-style", default="")
ap.add_argument("--exclude-words", default=""); ap.add_argument("--half-life", type=float, default=5.0)
ap.add_argument("--ref-year", type=int, default=2025); ap.add_argument("--json")
ap.add_argument("--host-map"); ap.add_argument("--host-cap", type=float, default=3.0)
a = ap.parse_args()
EXS = set(x for x in a.exclude_style.split(",") if x); EXW = set(x for x in a.exclude_words.split(",") if x)

years = {}
for line in open(a.r1_sources, encoding="utf-8"):
    c = [x.strip() for x in line.strip().strip("|").split("|")]
    if len(c) > 4 and c[0].isdigit():
        m = re.search(r"(19|20)\d{2}", c[3])
        if m: years[int(c[0])] = int(m.group(0))

rows = []
for f in a.r1:
    for l in open(f, encoding="utf-8"):
        if l.strip():
            r = json.loads(l); r["_deck"] = f"r1-{r['deck']}"; r["_year"] = years.get(r["deck"]); rows.append(r)
for f in a.r2:
    for l in open(f, encoding="utf-8"):
        if l.strip():
            try: r = json.loads(l)
            except json.JSONDecodeError: continue
            r["_deck"] = str(r.get("deck")); y = r.get("year")
            r["_year"] = int(y) if isinstance(y, (int, float)) or (isinstance(y, str) and y.isdigit()) else None
            rows.append(r)
style_rows = []
for f in a.style:
    for l in open(f, encoding="utf-8"):
        if l.strip():
            r = json.loads(l); r["_deck"] = f"r1-{r['r1_deck']}"; r["_year"] = r.get("year"); style_rows.append(r)

rows = [r for r in rows if r["_year"]]
HOST = json.load(open(a.host_map)) if a.host_map else {}
host_decks = C.Counter(HOST.get(d, d) for d in {r["_deck"] for r in rows + style_rows})
def host_factor(deck):
    n = host_decks[HOST.get(deck, deck)]
    return min(1.0, a.host_cap / n) if n else 1.0  # a host with many decks counts as at most host_cap decks
for r in rows + style_rows:
    r["_w"] = 0.5 ** (max(0, a.ref_year - r["_year"]) / a.half_life) * host_factor(r["_deck"])

NAV = {"cover", "agenda-contents", "section-divider", "backup-divider", "end-page"}
content = [r for r in rows if r.get("message_type") != "navigation" and r.get("archetype") not in NAV]
def W(rs): return sum(r["_w"] for r in rs)
def wshare(rs, pred): t = W(rs); return 100 * sum(r["_w"] for r in rs if pred(r)) / t if t else 0
def ushare(rs, pred): return 100 * sum(1 for r in rs if pred(r)) / len(rs) if rs else 0
def era(y): return "≤2009" if y <= 2009 else "2010–17" if y <= 2017 else "2018–21" if y <= 2021 else "2022+"

out = {"decks": len({r["_deck"] for r in rows}), "pages": len(rows), "content": len(content)}
print(f"decks={out['decks']} pages={len(rows)} content={len(content)} half-life={a.half_life}")
print("by era (decks/pages):", dict(C.Counter(era(r["_year"]) for r in rows)), dict(C.Counter(era(y) for y in {r['_deck']: r['_year'] for r in rows}.values())))

# --- title rules by era
sow = lambda r: bool(r.get("title_is_sowhat_sentence"))
print("\nERA      pages  so-what%  med_words  2-lines-or-less%  source%  unit%  sidebar%")
eras = {}
for e in ["≤2009", "2010–17", "2018–21", "2022+"]:
    rs = [r for r in content if era(r["_year"]) == e]
    if not rs: continue
    sw = [r for r in rs if sow(r) and r["_deck"] not in EXW]
    wd = [r["title_words"] for r in sw if isinstance(r.get("title_words"), int)]
    ln = [r["title_lines"] for r in sw if isinstance(r.get("title_lines"), int)]
    side = lambda r: "takeaway-sidebar" in (r.get("slots") or []) or "chart-plus-takeaway-sidebar" in [r.get("archetype")] + (r.get("secondary") or [])
    has = lambda s: (lambda r: s in (r.get("slots") or []))
    eras[e] = dict(pages=len(rs), sowhat=ushare(rs, sow), words=S.median(wd) if wd else None,
                   le2=ushare(sw, lambda r: isinstance(r.get("title_lines"), int) and r["title_lines"] <= 2),
                   source=ushare(rs, has("source-line")), unit=ushare(rs, has("unit-line")), sidebar=ushare(rs, side))
    d = eras[e]; print(f"{e:8s} {d['pages']:5d}  {d['sowhat']:7.0f}  {d['words'] or 0:9.1f}  {d['le2']:15.0f}  {d['source']:6.0f}  {d['unit']:5.0f}  {d['sidebar']:7.0f}")
out["eras"] = eras

sw_all = [r for r in content if sow(r) and r["_deck"] not in EXW]
wd = sorted(r["title_words"] for r in sw_all if isinstance(r.get("title_words"), int))
out["weighted"] = dict(sowhat=wshare(content, sow), median_words=S.median(wd), p90_words=wd[int(.9 * len(wd))],
                       le2=wshare(sw_all, lambda r: isinstance(r.get("title_lines"), int) and r["title_lines"] <= 2),
                       source=wshare(content, lambda r: "source-line" in (r.get("slots") or [])),
                       unit=wshare(content, lambda r: "unit-line" in (r.get("slots") or [])),
                       sidebar=wshare(content, lambda r: "takeaway-sidebar" in (r.get("slots") or []) or "chart-plus-takeaway-sidebar" in [r.get("archetype")] + (r.get("secondary") or [])))
print("\nWEIGHTED:", {k: round(v, 1) for k, v in out["weighted"].items()})

# --- archetypes (sidebar treated as layout modifier, not archetype)
def norm(a_):
    return {"comparison-table-text": "comparison-table", "harvey-ball-rating-table": "harvey-ball-table", "process-flow-value-chain": "process-flow",
            "timeline-roadmap-gantt": "timeline-roadmap", "issue-driver-tree": "issue-tree", "stacked-100-or-marimekko": "stacked-100"}.get(a_, a_)
arch = [r for r in content if r.get("archetype") != "chart-plus-takeaway-sidebar"]
cw = C.defaultdict(float); cu = C.Counter(); dk = C.defaultdict(set)
for r in arch:
    k = norm(r.get("archetype", "?")); cw[k] += r["_w"]; cu[k] += 1; dk[k].add(r["_deck"])
tw = sum(cw.values()); ranked = sorted(cw.items(), key=lambda x: -x[1])
print("\nARCHETYPE                      n   decks  unweighted%  weighted%")
out["archetypes"] = []
for k, v in ranked[:45]:
    row = dict(id=k, n=cu[k], decks=len(dk[k]), u=100 * cu[k] / len(arch), w=100 * v / tw); out["archetypes"].append(row)
    print(f"{k:30s} {cu[k]:4d}  {len(dk[k]):5d}  {row['u']:10.1f}  {row['w']:9.1f}")

# --- message type routing
mt = C.defaultdict(C.Counter)
for r in arch: mt[r.get("message_type")][norm(r.get("archetype"))] += r["_w"]
out["routing"] = {m: [(k, round(100 * v / sum(c.values()), 1)) for k, v in c.most_common(5)] for m, c in mt.items()}
print("\nMESSAGE TYPE → top archetypes (weighted %)")
for m, c in sorted(mt.items(), key=lambda x: -sum(x[1].values())):
    print(f"  {m:12s} {round(100*sum(c.values())/tw):3d}% :", ", ".join(f"{k} {100*v/sum(c.values()):.0f}%" for k, v in c.most_common(5)))

# --- visual style from 2020+ standard-template decks
st = [r for r in rows + style_rows if r.get("style") and r["_year"] >= 2020 and r["_deck"] not in EXS]
print(f"\nSTYLE 2020+ (decks={len({r['_deck'] for r in st})}, pages={len(st)}, excluded={sorted(EXS)})")
out["style"] = {}
for f in ["title_font", "title_case", "title_weight", "title_end_period", "title_color", "palette", "chart_style", "gridlines", "density", "tracker_style", "sticker_style", "whitespace"]:
    c = C.Counter()
    for r in st:
        if r["style"].get(f) is not None: c[str(r["style"].get(f))] += r["_w"]
    tot = sum(c.values()); out["style"][f] = [(k, round(100 * v / tot)) for k, v in c.most_common(4)]
    print(f"  {f:16s}", ", ".join(f"{k} {100*v/tot:.0f}%" for k, v in c.most_common(4)))
late = [r for r in st if r["_year"] >= 2025]
if late:
    print(f"\nSTYLE 2025–26 only (decks={len({r['_deck'] for r in late})}, pages={len(late)})")
    out["style_2025"] = {}
    for f in ["title_font", "title_weight", "title_end_period", "title_color", "palette", "tracker_style", "density"]:
        c = C.Counter()
        for r in late:
            if r["style"].get(f) is not None: c[str(r["style"].get(f))] += r["_w"]
        tot = sum(c.values())
        out["style_2025"][f] = [(k, round(100 * v / tot)) for k, v in c.most_common(3)]
        print(f"  {f:16s}", ", ".join(f"{k} {100*v/tot:.0f}%" for k, v in c.most_common(3)))

# --- NEW candidates across groups
nc = C.Counter(); nd = C.defaultdict(set)
for r in rows:
    for k in [r.get("archetype")] + (r.get("secondary") or []):
        if isinstance(k, str) and k.startswith("NEW:"): nc[k] += 1; nd[k].add(r["_deck"])
out["new"] = [(k, v, len(nd[k])) for k, v in nc.most_common(25)]
print("\nNEW candidates (n, decks):", ", ".join(f"{k[4:]} {v}/{len(nd[k])}" for k, v in nc.most_common(25)))
if a.json: json.dump(out, open(a.json, "w"), ensure_ascii=False, indent=1)
