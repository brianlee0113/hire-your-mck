b=open('build.py').read()
anchor='dps = []\nfor i in ORDER:'
add='''# display rounding: keep a rounded value only if every calc in the deck still verifies (check.py tolerance)
def _evs(calc, vals):
    e = calc
    for i in sorted(vals, key=len, reverse=True):
        e = re.sub(rf"(?<![\\w.]){re.escape(i)}(?![\\w-])", f"vals['{i}']", e)
    return eval(e)
vals = {i: DPS[i]["value"] for i in ORDER}
def ok_all(ids):
    for j in ids:
        d = DPS[j]
        if d.get("calc"):
            got = _evs(d["calc"], vals)
            if abs(got - vals[j]) > max(0.011, abs(vals[j]) * 0.01):
                return False
    return True
SHARES = {"sh_gmec": 2, "sh_gm": 2, "sh_ec": 2, "sh_lab": 2, "sh_occ": 2}
DEC = {"$M": 1, "years": 1, "thousand orders": 0, "%": 3, "$": 2, "pp": 2, "x": 2, "bps": 0, "million hours": 2}
for i in ORDER:
    d = DPS[i]
    if d.get("source_id") != "s3":
        continue
    nd = SHARES.get(i, DEC.get(d["unit"]))
    if nd is None:
        continue
    old = vals[i]; new = round(old, nd)
    if new == old:
        continue
    vals[i] = new
    users = [i] + [j for j in ORDER if i in DPS[j].get("derived_from", [])]
    if not ok_all(users):
        vals[i] = old
for i in ORDER:
    DPS[i]["value"] = vals[i]

'''
assert b.count(anchor)==1
b=b.replace(anchor, add+anchor)
open('build.py','w').write(b)
s=open('slides.py').read()
s=s.replace('row("Payback", ["@pb6", "@pb3", "@pb9"]),','row("Payback, years", ["@pb6", "@pb3", "@pb9"]),')
open('slides.py','w').write(s)
