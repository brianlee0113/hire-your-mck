import json, sys
sys.path.insert(0, "/Users/brianlee0113/hym-bench-work/_plugin/hire-your-mck-caf6e9634e77/skills/hire-your-mck/scripts")
from renderer import pptx_render as R
G, S = R.G, R.S
spec = json.load(open("/Users/brianlee0113/hym-bench-work/ws/dev-h1-c2-H1r-r3/work/harlow-margin-plan.json"))
one = R._est_h("X", G["title_w"], S["title"], 1.0, bold=True, title=True)
for s in spec["slides"]:
    lm = s.get("lead_message")
    if not lm: continue
    t = (lm.get("prefix", "") + " " + lm["text"]).strip()
    h = R._est_h(t, G["title_w"], S["title"], 1.0, bold=True, title=True)
    n = round(h / one)
    if n > 2: print(s["id"], n, len(t), t)
