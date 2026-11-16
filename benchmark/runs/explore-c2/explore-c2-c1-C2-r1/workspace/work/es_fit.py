import sys, json
S_DIR = sys.argv[2]
sys.path.insert(0, S_DIR + "/scripts")
from renderer.pptx_render import _est_h, S, G
spec = json.load(open(sys.argv[1]))
m = G["margin"]; W = G["slide_w"] - 2 * m
gt = spec["storyline"]["governing_thought"]
y = 108 / 96
gsize = S["header"] + 2
while gsize > 13 and _est_h(gt, W - 0.5, gsize, 1.0, bold=True, title=True) > 0.95: gsize -= 0.5
gh = _est_h(gt, W - 0.5, gsize, 1.0, bold=True, title=True) + 0.2
y += gh + 0.22
tw = W - 0.58 - 1.2
avail = G["content_bottom"] - y
print("gt size", gsize, "gt h", round(gh, 2), "avail", round(avail, 2))
for f in (1.0, 0.86):
    hs, bs = round((S["header"] + 2) * f * 2) / 2, round(S["body"] * f * 2) / 2
    tot = 0
    for it in spec["storyline"]["exec_summary"]:
        h = _est_h(it["text"], tw, hs, 1.15, bold=True); hh = [round(_est_h(sp["text"], tw - 0.2, bs, 1.15), 2) for sp in it["sub_points"]]
        tot += h + sum(hh) + 0.2
        print(f, it["id"], round(h, 2), hh)
    print("total", round(tot, 2))
