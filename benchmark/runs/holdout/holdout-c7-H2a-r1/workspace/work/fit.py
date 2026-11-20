import sys, json
sys.path.insert(0, "/Users/brianlee0113/hym-bench-work/_plugin/hire-your-mck-6f05966a12b9/skills/hire-your-mck/scripts")
from renderer.pptx_render import _est_h, S, G
from renderer import measure
spec = json.load(open(sys.argv[1]))
m = G["margin"]; W = G["slide_w"] - 2*m
gt = spec["storyline"]["governing_thought"]
gsize = S["header"] + 2
while gsize > 13 and _est_h(gt, W - 0.5, gsize, 1.0, bold=True, title=True) > 0.95: gsize -= 0.5
gh = _est_h(gt, W - 0.5, gsize, 1.0, bold=True, title=True) + 0.2
y = 108/96 + gh + 0.22
avail = G["content_bottom"] - y
tw = W - 0.58 - 1.2
f = 12/14
hs, bs = round((S["header"]+2)*f*2)/2, round(S["body"]*f*2)/2
tot = 0
for it in spec["storyline"]["exec_summary"]:
    h = _est_h(it["text"], tw, hs, 1.15, bold=True); tot += h + 0.2
    print(it["id"], "item lines", measure.lines(it["text"], tw, "arial", hs, True))
    for sp in it["sub_points"]:
        h2 = _est_h(sp["text"], tw - 0.2, bs, 1.15); tot += h2
        print("   sub lines", measure.lines(sp["text"], tw - 0.2, "arial", bs), sp["text"][:50])
print("gt size", gsize, "avail", round(avail,2), "need at 12pt", round(tot,2))
for s in spec["slides"]:
    if s.get("so_what"):
        if s.get("so_what_style") == "line":
            n = measure.lines(s["so_what"], G["slide_w"] - 2*m - 0.22 - 0.2, "georgia", S["sowhat"] + 2, True)
        else:
            n = measure.lines(s["so_what"], G["slide_w"] - 2*m - 0.23 - 0.2, "georgia", S["sowhat"], True)
        print("so_what", s["id"], s.get("so_what_style","bar"), n, len(s["so_what"]))
    for fn in s.get("footnotes", []):
        n = measure.lines(fn, G["slide_w"] - 2*m - 0.3, "arial", S.get("source", 9))
        if n > 1: print("footnote 2 lines", s["id"], fn[:50])
