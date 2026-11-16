"""Independent check: every user-provided excerpt is in the briefing pack, and its value appears in it."""
import json, re, sys
pack = open(sys.argv[2]).read()
flat = re.sub(r"\*\*", "", pack)
flat = re.sub(r"\s+", " ", flat)
spec = json.load(open(sys.argv[1]))
bad = 0
for d in spec["data_points"]:
    if d["source_id"] != "s1": continue
    ex = d["excerpt"]
    m = re.match(r'Table (\d)[^;]*?(?:row "([^"]+)")?; column (.+?) = "([^"]+)"$', ex)
    if m:
        row, val = m.group(2), m.group(4)
        lines = [l for l in pack.splitlines() if (row is None or l.startswith("| " + row + " |"))]
        if row is None:  # Table 1: header + value row
            ok = val in pack
        else:
            ok = any(val.replace("−", "−") in l for l in lines)
        where = "table"
    else:
        ok = re.sub(r"\s+", " ", ex) in flat
        where = "text"
    if not ok:
        bad += 1; print("NOT FOUND", d["id"], where, ex[:90])
print("checked", sum(1 for d in spec["data_points"] if d["source_id"] == "s1"), "excerpts;", bad, "not found")
