import json, sys
sys.path.insert(0, "/private/tmp/claude-501/-Users-brianlee0113-Developer-slides-like-a-consultant/ecc57932-fbce-495b-95b7-2715fee2e303/scratchpad/hymwork/_plugin/hire-your-mck-132dffb7fdfd/skills/hire-your-mck/scripts")
from renderer.pptx_render import _est_h, S, G
spec = json.load(open(sys.argv[1]))
m = G["margin"]; W = G["slide_w"] - 2 * m; tw = W - 0.58 - 1.2
gt = spec["storyline"]["governing_thought"]
gsize = S["header"] + 2
while gsize > 13 and _est_h(gt, W - 0.5, gsize, 1.0, bold=True, title=True) > 0.95: gsize -= 0.5
gh = _est_h(gt, W - 0.5, gsize, 1.0, bold=True, title=True) + 0.2
y = 108 / 96 + gh + 0.22; avail = G["content_bottom"] - y
print(f"GT size {gsize}, height {gh:.2f}; avail {avail:.2f}")
f = 1.0
hs, bs = S["header"] + 2, S["body"]
tot = 0
for it in spec["storyline"]["exec_summary"]:
    h = _est_h(it["text"], tw, hs, 1.15, bold=True); line = hs * 1.15 / 72
    print(f"item {it['id']}: head {h / line:.1f} lines")
    tot += h + 0.2
    for sp in it["sub_points"]:
        hh = _est_h(sp["text"], tw - 0.2, bs, 1.15); tot += hh
        print(f"   sub {hh / (bs * 1.15 / 72):.1f} lines: {sp['text'][:60]}")
print(f"need at 14pt: {tot:.2f} vs avail {avail:.2f}")
def need(item, f):
    hs, bs = round((S["header"] + 2) * f * 2) / 2, round(S["body"] * f * 2) / 2
    h = _est_h(item["text"], tw, hs, 1.15, bold=True)
    h += sum(_est_h(sp["text"], tw - 0.2, bs, 1.15) for sp in item.get("sub_points", []))
    return h + 0.2
f = 1.3
ex = spec["storyline"]["exec_summary"]
while f > 0.72 and sum(need(it, f) for it in ex) > avail: f -= 0.02
print(f"renderer scale f={f:.2f} -> body {S['body'] * f:.1f} pt (need >= 11.95)")
