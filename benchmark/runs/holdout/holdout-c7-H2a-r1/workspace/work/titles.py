import sys, json
sys.path.insert(0, "/Users/brianlee0113/hym-bench-work/_plugin/hire-your-mck-6f05966a12b9/skills/hire-your-mck/scripts")
from renderer import measure, tokens
G = tokens.GRID
w = G["title_w"] - float(__import__("os").environ.get("INSET","0.2"))
spec = json.load(open(sys.argv[1]))
extra = sys.argv[2:]
for s in spec["slides"]:
    lm = s.get("lead_message")
    if lm:
        t = ((lm.get("prefix") or "") + " " + lm["text"]).strip()
        n = measure.lines(t, w, "georgia", 25, True)
        print(s["id"], n, len(t.split()), t[:60])
for t in extra:
    print("?", measure.lines(t, w, "georgia", 25, True), len(t.split()), t)
