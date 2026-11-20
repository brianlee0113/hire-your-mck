import json, sys
sys.path.insert(0, "/Users/brianlee0113/hym-bench-work/_plugin/hire-your-mck-6f05966a12b9/skills/hire-your-mck/scripts")
from renderer import pptx_render as R
G, S, est = R.G, R.S, R._est_h
sp = json.load(open(sys.argv[1]))
st = sp["storyline"]; ex = st["exec_summary"]
m = G["margin"]; W = G["slide_w"] - 2 * m
gt = st["governing_thought"]; gsize = S["header"] + 2
while gsize > 13 and est(gt, W - 0.5, gsize, 1.0, bold=True, title=True) > 0.95: gsize -= 0.5
gh = est(gt, W - 0.5, gsize, 1.0, bold=True, title=True) + 0.2
y = 108 / 96 + gh + 0.22
tw = W - 0.58 - 1.2
def need(item, f):
    hs, bs = round((S["header"] + 2) * f * 2) / 2, round(S["body"] * f * 2) / 2
    return est(item["text"], tw, hs, 1.15, bold=True) + sum(est(p["text"], tw - 0.2, bs, 1.15) for p in item.get("sub_points", [])) + 0.2
avail = G["content_bottom"] - y
f = 1.3
while f > 0.72 and sum(need(it, f) for it in ex) > avail: f -= 0.02
print("gt size", gsize, "avail", round(avail, 2), "f", round(f, 2), "body pt", round(S["body"] * f, 1), "fits", sum(need(it, f) for it in ex) <= avail + 0.02)
for it in ex:
    print(" item", it["id"], round(est(it["text"], tw, S["header"] + 2, 1.15, bold=True) / (S["header"] + 2) / 1.15 * 72, 1), "lines")
    for p in it.get("sub_points", []):
        print("   ", round(est(p["text"], tw - 0.2, S["body"], 1.15) / S["body"] / 1.15 * 72, 1), p["text"][:60])
