import sys, json
sys.path.insert(0, "/Users/brianlee0113/hym-bench-work/_plugin/hire-your-mck-6f05966a12b9/skills/hire-your-mck/scripts")
from renderer.pptx_render import _lines, S, G, body_box, BASIS_H
spec = json.load(open(sys.argv[1]))
for s in spec["slides"]:
    b = s.get("body") or {}
    if b.get("kind") != "table" or (sys.argv[2:] and s["id"] not in sys.argv[2:]): continue
    x, y, w, h = body_box(s)
    if s.get("unit_line") is None: pass
    cols = list(b["columns"]); rows = b["rows"]
    co = s.get("callout")
    verdict = bool(co) or any(r.get("note") for r in rows)
    if verdict: cols.append("v")
    ncols = len(cols) + 1; first = w * 0.19
    widths = [first] + [0]*(ncols-1)
    if verdict:
        widths[-1] = w*0.27; mid = (w - first - widths[-1]) / max(1, ncols-2)
        for j in range(1, ncols-1): widths[j] = mid
    else:
        for j in range(1, ncols): widths[j] = (w-first)/(ncols-1)
    for size in (14, 13, 12, 11):
        hh = max(_lines(c, widths[j], size, True) for j, c in enumerate(cols, 1)) * size*1.2/72 + 0.16
        tot = hh; worst = []
        for r in rows:
            texts = [c.get("text", "$9.9M") for c in r["cells"]]
            if verdict: texts.append(co["header"] + "\n" + co.get("detail", "") if co and co["target"] == r["label"] else r.get("note", ""))
            ls = [_lines(r["label"], widths[0], size+1, True)] + [_lines(t, widths[j], size) for j, t in enumerate(texts, 1) if t]
            tot += max(ls) * size*1.2/72 + 0.18
            worst.append(max(ls))
        if tot <= h: break
    print(s["id"], "fits at", size if tot <= h else "<11", "need", round(tot,2), "have", round(h,2), "lines/row", worst)
