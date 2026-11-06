"""Aggregate archetype tagging data with recency weighting.

Usage: python aggregate.py <sources.md> <tag.jsonl>... [--half-life 5] [--ref-year 2025]

Each tagged page gets weight = 0.5 ** ((ref_year - deck_year) / half_life).
Deck years come from the "Year" column of the sources table (first 4-digit number).
Prints weighted vs unweighted stats and a by-era breakdown so drift is visible.
"""
import argparse, json, re, collections as C, statistics as S

ap = argparse.ArgumentParser()
ap.add_argument("sources")
ap.add_argument("tags", nargs="+")
ap.add_argument("--half-life", type=float, default=5.0)
ap.add_argument("--ref-year", type=int, default=2025)
a = ap.parse_args()

# deck number -> year, from markdown table rows like "| 12 | title | host | 2008 | ..."
years = {}
for line in open(a.sources, encoding="utf-8"):
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) > 4 and cells[0].isdigit():
        m = re.search(r"(19|20)\d{2}", cells[3])
        if m:
            years[int(cells[0])] = int(m.group(0))

rows = []
for f in a.tags:
    for l in open(f, encoding="utf-8"):
        if l.strip():
            rows.append(json.loads(l))
for r in rows:
    y = years.get(r.get("deck"))
    r["_year"] = y
    r["_w"] = 0.5 ** ((a.ref_year - y) / a.half_life) if y else 0.0
missing = sorted({r.get("deck") for r in rows if r["_year"] is None})

def era(y):
    return "≤2009" if y <= 2009 else ("2010–17" if y <= 2017 else "2018+")

content = [r for r in rows if r.get("message_type") != "navigation" and r["_year"]]

def share(rs, pred, w=True):
    tot = sum(r["_w"] if w else 1 for r in rs)
    return 100 * sum((r["_w"] if w else 1) for r in rs if pred(r)) / tot if tot else 0

print(f"pages={len(rows)} content={len(content)} decks_with_year={len(years)} missing_year_decks={missing}")
print(f"half-life={a.half_life}y ref={a.ref_year}\n")

print("ERA        decks pages  so-what%  median_words  source%  unit%  sidebar%  sticker%")
for e in ["≤2009", "2010–17", "2018+"]:
    rs = [r for r in content if era(r["_year"]) == e]
    if not rs: continue
    sw = [r for r in rs if r.get("title_is_sowhat_sentence")]
    words = [r["title_words"] for r in sw if isinstance(r.get("title_words"), int)]
    has = lambda s: (lambda r: s in (r.get("slots") or []))
    side = lambda r: "takeaway-sidebar" in (r.get("slots") or []) or "chart-plus-takeaway-sidebar" in ([r.get("archetype")] + (r.get("secondary") or []))
    print(f"{e:9s} {len({r['deck'] for r in rs}):5d} {len(rs):5d}  {share(rs, lambda r: r.get('title_is_sowhat_sentence'), False):7.0f}  "
          f"{S.median(words) if words else 0:12.1f}  {share(rs, has('source-line'), False):6.0f}  {share(rs, has('unit-line'), False):5.0f}  "
          f"{share(rs, side, False):7.0f}  {share(rs, has('sticker'), False):7.0f}")

print("\nARCHETYPE (primary, content pages)   unweighted%   weighted%   delta")
cu = C.Counter(r["archetype"] for r in content)
cw = C.defaultdict(float)
for r in content: cw[r["archetype"]] += r["_w"]
tw = sum(cw.values())
for k, _ in sorted(cw.items(), key=lambda x: -x[1])[:28]:
    u = 100 * cu[k] / len(content); w = 100 * cw[k] / tw
    print(f"{k:36s} {u:8.1f}    {w:8.1f}   {w-u:+5.1f}")

print("\nHEADLINE RULES  unweighted vs weighted")
sw_u = share(content, lambda r: r.get("title_is_sowhat_sentence"), False)
sw_w = share(content, lambda r: r.get("title_is_sowhat_sentence"))
print(f"so-what titles: {sw_u:.0f}% → {sw_w:.0f}%")
for s in ["source-line", "unit-line", "tracker", "section-tag", "sticker", "footnote", "legend"]:
    print(f"{s:14s}: {share(content, lambda r: s in (r.get('slots') or []), False):.0f}% → {share(content, lambda r: s in (r.get('slots') or [])):.0f}%")
