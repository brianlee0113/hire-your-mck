import json, sys
sys.path.insert(0, "/Users/brianlee0113/hym-bench-work/_plugin/hire-your-mck-6f05966a12b9/skills/hire-your-mck/scripts")
from renderer import pptx_render as R
G, S = R.G, R.S
spec = json.load(open(sys.argv[1]))
tf = "Georgia"
def lines(text, w, size, bold=False, title=False):
    return R._est_h(text, w, size, 1.0, bold=bold, title=title) / (size / 72)
for s in spec["slides"]:
    lm = s.get("lead_message")
    if lm:
        n = lines(lm["text"], G["title_w"], S["title"], bold=True, title=True)
        flag = " <-- 3 lines" if n > 2.3 else ""
        print(f"{s['id']:>4} title {n:.1f}{flag}")
    if s.get("so_what"):
        W = G["slide_w"] - 2 * G["margin"]
        n = lines(s["so_what"], W - 0.6, S["body"] + 1, bold=True)
        print(f"{s['id']:>4} so_what {n:.1f} {'<--' if n > 1.15 else ''}")
W = G["slide_w"] - 2 * G["margin"]
tw = W - 0.58 - 1.2
gt = spec["storyline"]["governing_thought"]
print("GT lines at", S["header"] + 2, lines(gt, W - 0.5, S["header"] + 2, bold=True, title=True))
for it in spec["storyline"]["exec_summary"]:
    print("item", it["id"], round(lines(it["text"], tw, S["header"] + 2, bold=True), 2))
    for sp in it["sub_points"]:
        n = lines(sp["text"], tw - 0.2, S["body"])
        print("   sub", round(n, 2), "<--" if n > 1.15 else "", sp["text"][:60])
print("S", S, "G", {k: G[k] for k in ("slide_w", "margin", "title_w", "content_top", "content_bottom", "sidebar_w")})
