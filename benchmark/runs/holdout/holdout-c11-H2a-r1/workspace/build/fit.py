import sys
sys.path.insert(0, "/Users/brianlee0113/hym-bench-work/_plugin/hire-your-mck-6f05966a12b9/skills/hire-your-mck/scripts")
from renderer import pptx_render as R
G, S = R.G, R.S
W = G["slide_w"] - 2 * G["margin"]
def title_lines(t): return R.measure.para_height(R._md_runs(t, S["title"], True, True), G["title_w"], 0.95) / (S["title"] * 0.95 / 72)
def sw_lines(t): return R.measure.para_height(R._md_runs(t, S["sowhat"], True, True), W - 0.46 - 0.2, 1.0) / (S["sowhat"] / 72)
def gt_h(t): return R._est_h(t, W - 0.5, S["header"] + 2, 1.0, bold=True, title=True)
def exec_need(items, f=1.0):
    tw = W - 0.58 - 1.2
    hs, bs = round((S["header"] + 2) * f * 2) / 2, round(S["body"] * f * 2) / 2
    return sum(R._est_h(i[0], tw, hs, 1.15, bold=True) + sum(R._est_h(s, tw - 0.2, bs, 1.15) for s in i[1]) + 0.2 for i in items)
if __name__ == "__main__":
    for line in sys.stdin:
        kind, _, txt = line.rstrip("\n").partition("|")
        if kind == "t": print(f"{title_lines(txt):.2f}  {len(txt.split())}w  {txt}")
        if kind == "s": print(f"{sw_lines(txt):.2f}  {txt}")
