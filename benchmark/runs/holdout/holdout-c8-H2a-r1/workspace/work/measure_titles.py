import json, sys
sys.path.insert(0, "/Users/brianlee0113/hym-bench-work/_plugin/hire-your-mck-6f05966a12b9/skills/hire-your-mck/scripts")
from renderer import measure
from renderer.pptx_render import G, S
sp = json.load(open(sys.argv[1]))
fam_t, fam_b = "Georgia", "Arial"
for s in sp["slides"]:
    lm = s.get("lead_message")
    if not lm: continue
    t = (lm.get("prefix", "") + " " + lm["text"]).strip()
    n = measure.lines(t, G["title_w"], fam_t, S["title"], bold=True)
    sw = s.get("so_what")
    m = measure.lines(sw, G["slide_w"] - 2 * G["margin"] - 0.6, fam_b, S["body"], bold=True) if sw else 0
    print(s["id"], "title", n, "lines", len(t), "ch | so_what", m)
for s in sp["slides"]:
    for f in s.get("footnotes", []):
        n = measure.lines(f, G["slide_w"] - 2 * G["margin"], fam_b, S["source"])
        if n > 1: print("FOOTNOTE", s["id"], n, f[:60])
