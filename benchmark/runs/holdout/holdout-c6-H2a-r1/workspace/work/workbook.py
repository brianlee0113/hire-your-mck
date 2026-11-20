"""Re-write the source workbook so each slide's sheet also lists the numbers shown in its table and text cells."""
import json, os, sys
sys.path.insert(0, "/Users/brianlee0113/hym-bench-work/_plugin/hire-your-mck-6f05966a12b9/skills/hire-your-mck/scripts")
sys.path.insert(0, os.path.dirname(__file__))
from renderer import xlsx_render, tokens
from textrefs import TEXT_REFS
spec = json.load(open(sys.argv[1])); out = sys.argv[2]
ids = {s["id"] for s in spec["slides"]}; dps = {d["id"] for d in spec["data_points"]}
bad = [(k, r) for k, v in TEXT_REFS.items() for r in v if r not in dps or k not in ids]
assert not bad, bad
by_body = {id(s.get("body")): s["id"] for s in spec["slides"] if s.get("body") is not None}
orig = xlsx_render.collect_refs
def collect(o):
    refs = list(orig(o))
    sid = by_body.get(id(o.get("b"))) if isinstance(o, dict) and "b" in o else None
    for r in TEXT_REFS.get(sid, []):
        if r not in refs:
            refs.append(r)
    return refs
xlsx_render.collect_refs = collect
primary = tokens.resolve(spec["meta"].get("theme", "navy"))["primary"]
xlsx_render.render(spec, out, primary)
print("wrote", out, "primary", primary)
