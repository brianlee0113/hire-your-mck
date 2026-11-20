import json, sys
sys.path.insert(0, "/Users/brianlee0113/hym-bench-work/_plugin/hire-your-mck-6f05966a12b9/skills/hire-your-mck/scripts")
from renderer import measure, pptx_render as R
G = R.G if hasattr(R, "G") else None
w = G["title_w"]
sp = json.load(open(sys.argv[1]))
for s in sp["slides"]:
    lm = s.get("lead_message")
    if not lm: continue
    t = (lm.get("prefix", "") + " " + lm["text"]).strip()
    n = measure.lines(t, w, "georgia", 25, bold=True)
    print(s["id"], n, len(t.split()), "" if n <= 2 else "<<< " + t)
print("governing thought lines at 16pt?", w)
