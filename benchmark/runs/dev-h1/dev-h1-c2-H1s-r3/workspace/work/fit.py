import json, sys
sys.path.insert(0, "/Users/brianlee0113/hym-bench-work/_plugin/hire-your-mck-caf6e9634e77/skills/hire-your-mck/scripts")
from renderer import pptx_render as R
spec = json.load(open("harlow-margin-plan.json"))
G, S = R.G, R.S
W = G["slide_w"] - 2 * G["margin"]
gt = spec["storyline"]["governing_thought"]
gsize = S["header"] + 2
while gsize > 13 and R._est_h(gt, W - 0.5, gsize, 1.0, bold=True, title=True) > 0.95: gsize -= 0.5
gh = R._est_h(gt, W - 0.5, gsize, 1.0, bold=True, title=True) + 0.2
y = 108/96 + gh + 0.22
avail = G["content_bottom"] - y
tw = W - 0.58 - 1.2
def need(item, f):
    hs, bs = round((S["header"] + 2) * f * 2) / 2, round(S["body"] * f * 2) / 2
    h = R._est_h(item["text"], tw, hs, 1.15, bold=True)
    h += sum(R._est_h(sp["text"], tw - 0.2, bs, 1.15) for sp in item.get("sub_points", []))
    return h + 0.2
f = 1.3
ex = spec["storyline"]["exec_summary"]
while f > 0.72 and sum(need(it, f) for it in ex) > avail: f -= 0.02
print("gt size", gsize, "gh", round(gh,2), "f", round(f,2), "body pt", round(S["body"]*f,1))
for it in ex:
    print(it["id"], round(R._est_h(it["text"], tw, round((S["header"]+2)*1.0*2)/2, 1.15, bold=True),2), [round(R._est_h(sp["text"], tw-0.2, S["body"], 1.15),2) for sp in it["sub_points"]])
# titles: lines at title size
for sl in spec["slides"]:
    lm = sl.get("lead_message")
    if not lm: continue
    t = (lm.get("prefix","") + " " + lm["text"]).strip()
    h = R._est_h(t, G["title_w"], S["title"], 0.95, bold=True, title=True)
    if h > G["title_h"]: print("TITLE too tall", sl["id"], round(h,2), G["title_h"], len(t))
print("avail", round(avail,2), "tw", round(tw,2))
for s_ in ["Promotions, shrink and home delivery drove the decline; wages explain only 13% of the fall",
           "x"*60, "Gross margin and e-commerce explain 79%; productivity offset two-thirds of the wage rise"]:
    print(len(s_), round(R._est_h(s_, tw, 16, 1.15, bold=True),2), round(R._est_h(s_, tw, 14, 1.15, bold=True),2), round(R._est_h(s_, tw-0.2, 14, 1.15),2), round(R._est_h(s_, tw-0.2, 12, 1.15),2))
print("--- at f=0.86")
tot=0
for it in ex:
    h=R._est_h(it["text"], tw, 14, 1.15, bold=True); subs=[R._est_h(sp["text"], tw-0.2, 12, 1.15) for sp in it["sub_points"]]
    tot+=h+sum(subs)+0.2
    print(it["id"], round(h,2), [round(x,2) for x in subs], len(it["text"]), [len(sp["text"]) for sp in it["sub_points"]])
print("total", round(tot,2), "avail", round(avail,2))
