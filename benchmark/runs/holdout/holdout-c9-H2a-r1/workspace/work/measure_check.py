import sys, json
sys.path.insert(0, "/Users/brianlee0113/hym-bench-work/_plugin/hire-your-mck-6f05966a12b9/skills/hire-your-mck/scripts")
from renderer import measure
spec = json.load(open(sys.argv[1]))
for s in spec["slides"]:
    sw = s.get("so_what")
    if sw:
        line = s.get("so_what_style") == "line"
        w = 12.13 - (0.22 if line else 0.46)
        n = measure.lines(sw, w, "Georgia", 17 if line else 15, True)
        print(s["id"], "so_what lines", n, len(sw), "" if n == 1 else "  <-- " + sw[:60])
print("--- titles (25pt Georgia bold, 11.25in, max 2 lines)")
for s in spec["slides"]:
    lm = s.get("lead_message")
    if lm:
        n = measure.lines(lm["text"], 11.25, "Georgia", 25, True)
        if n > 2: print(s["id"], "title lines", n, lm["text"][:60])
print("--- exec sub-points (14pt Arial, 10.0in, 1 line)")
for it in spec["storyline"]["exec_summary"]:
    for sp in it["sub_points"]:
        n = measure.lines(sp["text"], 10.0, "Arial", 14, False)
        if n > 1: print(it["id"], n, len(sp["text"]), sp["text"][:70])
print("--- footnotes (9pt Arial, 12.0in, 1 line)")
for s in spec["slides"]:
    for f in s.get("footnotes", []):
        n = measure.lines(f, 11.9, "Arial", 9, False)
        if n > 1: print(s["id"], n, len(f), f[:70])
