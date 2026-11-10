"""Validate a Storyline spec: JSON Schema + cross-reference QA rules from docs/principles.md.

Usage: python check.py <spec.json> [--schema docs/spec/storyline.schema.json]
Exit code 1 if any rule fails. Warnings do not fail.
"""
import argparse, json, re, sys, pathlib

ap = argparse.ArgumentParser()
ap.add_argument("spec")
_here = pathlib.Path(__file__).resolve().parent
_candidates = [_here / "storyline.schema.json"] + [p / "docs/spec/storyline.schema.json" for p in _here.parents]
ap.add_argument("--schema", default=str(next((c for c in _candidates if c.exists()), _candidates[0])),
                help="defaults to storyline.schema.json next to this script (skill build) or docs/spec/ in the repo")
a = ap.parse_args()
spec = json.load(open(a.spec))
results = []
def out(rule, status, detail, slide=None):
    results.append((rule, status, slide, detail))

# 1. schema
try:
    import jsonschema
    v = jsonschema.Draft202012Validator(json.load(open(a.schema)))
    errs = sorted(v.iter_errors(spec), key=lambda e: list(e.path))
    for e in errs:
        out("schema", "fail", f"{'/'.join(map(str, e.path))}: {e.message[:160]}")
    if not errs:
        out("schema", "pass", "valid")
except ImportError:
    out("schema", "warn", "jsonschema not installed; schema not checked")

slides = {s["id"]: s for s in spec["slides"]}
dps = {d["id"]: d for d in spec.get("data_points", [])}
srcs = {s["id"]: s for s in spec.get("sources", [])}
content = [s for s in spec["slides"] if s["role"] == "content"]

def points(o):
    """Yield every point object inside a body/layout."""
    if isinstance(o, dict):
        if "data_ref" in o or "placeholder" in o:
            if set(o) <= {"data_ref", "placeholder", "label"}:
                yield o
        for v in o.values():
            yield from points(v)
    elif isinstance(o, list):
        for v in o:
            yield from points(v)

def collect_labels(o):
    """Headers, labels, ids and codes of body elements (callout targets)."""
    out = []
    if isinstance(o, dict):
        for k in ("header", "label", "id", "code"):
            if isinstance(o.get(k), str):
                out.append(o[k])
        for v in o.values():
            out += collect_labels(v)
    elif isinstance(o, list):
        for v in o:
            out += collect_labels(v)
    return out


def collect_data_refs(o):
    if isinstance(o, dict):
        return ([o["data_ref"]] if "data_ref" in o else []) + [r for v in o.values() for r in collect_data_refs(v)]
    if isinstance(o, list):
        return [r for v in o for r in collect_data_refs(v)]
    return []


SKIP_KEYS = {"id", "kind", "chart_type", "style", "status", "role", "archetype", "message_type", "variant",
             "data_ref", "data_refs", "section_id", "backup_of", "parent_id", "sort", "value_format", "table_type",
             "focus_quadrant", "rationale", "data_requirements", "sticker", "shape", "prefix", "rating", "x", "y", "size"}


def slide_chars(slide):
    """Approximate characters a reader sees on the slide (A-12). Each shown value counts 5."""
    total = 0
    def walk(o, key=None):
        nonlocal total
        if key in SKIP_KEYS:
            if key == "data_ref":
                total += 5
            return
        if isinstance(o, str):
            total += len(o)
        elif isinstance(o, dict):
            if o.get("placeholder") is True:
                total += 1
            for k, v in o.items():
                walk(v, k)
        elif isinstance(o, list):
            for v in o:
                walk(v, key)
    walk({k: v for k, v in slide.items() if k not in ("data_requirements", "rationale")})
    return total


def count_elements(body):
    k = body.get("kind")
    return {"framework": lambda: len(body["items"]), "process": lambda: len(body["steps"]),
            "levers": lambda: len(body["items"]), "panels": lambda: len(body["panels"]),
            "kpi": lambda: len(body["items"]), "text": lambda: len(body.get("columns") or body.get("bullets") or body.get("quotes") or []),
            # waterfall: start and end bars are totals, the steps in between are the elements
            "chart": lambda: len(body["categories"]) - 2 if body.get("chart_type") == "waterfall" else len(body["categories"]),
            "tree": lambda: len(body["root"].get("children", []))}.get(k, lambda: None)()

# 1b. ids must be unique within each list
for key in ("slides", "data_points", "sources", "sections"):
    seen = set()
    for item in spec.get(key, []):
        if item["id"] in seen:
            out("ids", "fail", f"duplicate id '{item['id']}' in {key}")
        seen.add(item["id"])

def device(s):
    """Which conclusion device a slide uses (A-12): sidebar, callout, bar, line or none."""
    if (s.get("layout") or {}).get("variant") == "takeaway_sidebar":
        return "sidebar"
    if s.get("callout"):
        return "callout"
    if s.get("so_what"):
        return s.get("so_what_style", "bar")
    return "none"

# 1c. navigation slides: section dividers and agenda trackers point at real sections
sec_ids = {sc["id"] for sc in spec.get("sections", [])}
for s in spec["slides"]:
    if s["role"] == "section_divider" and s.get("section_id") not in sec_ids:
        out("S3", "fail", f"section divider needs an existing section_id (got {s.get('section_id')})", s["id"])
    if s["role"] == "agenda_tracker":
        if s.get("section_id") and s["section_id"] not in sec_ids:
            out("S3", "fail", f"agenda tracker section_id {s['section_id']} does not exist", s["id"])
        if not sec_ids:
            out("S3", "warn", "agenda tracker in a deck without sections", s["id"])
nav = [s for s in spec["slides"] if s["role"] in ("section_divider", "agenda_tracker")]
n_content = sum(1 for s in spec["slides"] if s["role"] == "content")
if nav and n_content < 10:
    out("S3", "warn", f"navigation slides in a deck with {n_content} content slides; under 10, the exec summary is the contents")
if {s["role"] for s in nav} == {"section_divider", "agenda_tracker"}:
    out("S3", "warn", "section dividers and agenda trackers mixed; use one navigation style for the whole deck")

# 2. B-04: exec summary <-> content slides
es = spec["storyline"]["exec_summary"]
covered = {}
for item in es:
    sup = item.get("supports", [])
    if not sup:
        out("B-04", "fail", f"exec item {item['id']} has no supporting slide")
    for sid in sup:
        if sid not in slides:
            out("B-04", "fail", f"exec item {item['id']} points to missing slide {sid}")
        covered.setdefault(sid, []).append(item["id"])
for s in content:
    c = covered.get(s["id"], [])
    if len(c) != 1:
        out("B-04", "fail", f"content slide is listed under {len(c)} exec items (want exactly 1)", s["id"])
if spec["mode"] == "single_slide" and len(content) != 1:
    out("mode", "fail", f"single_slide mode needs exactly 1 content slide, has {len(content)}")

for s in spec["slides"]:
    sid = s["id"]
    if s["role"] not in ("content", "backup"):
        continue
    lm = s["lead_message"]; body = s.get("body"); pts = list(points(body)) + list(points(s.get("layout")))
    # A-03 title length
    words = len(lm["text"].split())
    if words > 25: out("A-03", "fail", f"title has {words} words (max 25)", sid)
    elif words > 21: out("A-03", "warn", f"title has {words} words (90% of observed titles ≤20)", sid)
    if lm["text"].rstrip().endswith("."): out("D8", "warn", "title ends with a period", sid)
    # A-01 numbers in title appear on slide
    nums = re.findall(r"[$~]?\d[\d,.]*\s?(?:%|x|M|B|K|pp|p\.p\.)?", lm["text"])
    nums = [n for n in nums if not re.fullmatch(r"(19|20)\d\d(s)?", n.strip().rstrip(",.;:"))]  # years are not claims
    declared = lm.get("numbers", [])
    if nums and not declared:
        out("A-01", "warn", f"title numbers {nums} not declared in lead_message.numbers", sid)
    for n in declared:
        ref = n.get("data_ref")
        if s["status"] in ("filled", "qa_passed") and not ref:
            out("A-01", "fail", f"title number '{n['text']}' has no data_ref", sid)
        elif ref and not any(p.get("data_ref") == ref for p in pts):
            out("A-01", "fail", f"title number '{n['text']}' ({ref}) is not shown in the body/sidebar", sid)
    # A-02 highlights
    if body and body.get("kind") == "chart":
        hl_t = set(lm.get("highlights", [])); hl_c = set(body.get("highlight", []))
        if hl_t != hl_c: out("A-02", "fail", f"title highlights {sorted(hl_t)} ≠ chart highlight {sorted(hl_c)}", sid)
        if body.get("chart_type") == "scatter" and len(body["series"]) not in (2, 3):
            out("schema+", "fail", f"scatter needs series x, y and optionally size; has {len(body['series'])} series", sid)
        if body.get("quadrant_labels") and body.get("reference_lines") == "none":
            out("schema+", "warn", "quadrant_labels need the average lines (reference_lines 'mean')", sid)
        for ser in body["series"]:
            if len(ser["points"]) != len(body["categories"]):
                out("schema+", "fail", f"series '{ser['name']}' has {len(ser['points'])} points for {len(body['categories'])} categories", sid)
    # ghost slides may carry a skeleton body, but every value must still be a placeholder
    if s.get("status") == "ghost" and body and collect_data_refs(body):
        out("status", "fail", "ghost slide body has data_refs; a ghost shows placeholders only (use drafted)", sid)
    # B-05 no repeated information: side elements must not reuse numbers the body already shows
    if body and s.get("status") != "ghost":
        body_refs = set(collect_data_refs(body))
        side = {"sidebar": (s.get("layout") or {}).get("sidebar") or {}, "callout": s.get("callout") or {}}
        for where, obj in side.items():
            dup = sorted(set(collect_data_refs(obj)) & body_refs)
            if dup:
                out("B-05", "fail", f"{where} repeats numbers the body already shows ({', '.join(dup)}); show a new insight or data point", sid)
            # B-06: other numbers must be computed from the body (shares, gaps, changes), not a new topic
            for r in sorted(set(collect_data_refs(obj)) - body_refs):
                dpd = dps.get(r) or {}
                if not (set(dpd.get("derived_from", [])) & body_refs):
                    out("B-06", "warn", f"{where} number {r} ('{dpd.get('label', '')[:40]}') is not computed from the exhibit; does it explain the chart or start a new topic?", sid)
    # A-12 density
    if s.get("status") != "ghost" and s.get("archetype") != "statement" and body:
        n_chars = slide_chars(s)
        low = 300 if body.get("kind") in ("chart", "panels", "tree", "matrix") else 450  # exhibits carry the message
        if n_chars < low: out("A-12", "warn", f"slide text is ~{n_chars} chars; references run 670–1,110 (target 600–1,100, charts ≥300)", sid)
        elif n_chars > 1300: out("A-12", "warn", f"slide text is ~{n_chars} chars; above 1,300 reads as crowded", sid)
        for it in body.get("columns", []) + body.get("items", []) + body.get("steps", []):
            if isinstance(it, dict) and "header" in it and len(it.get("detail", [])) < 3:
                out("A-12", "warn", f"'{it['header'][:30]}' has {len(it.get('detail', []))} bullets (want 3–5)", sid); break
        lay = s.get("layout") or {}
        if body.get("kind") == "chart" and lay.get("variant") != "takeaway_sidebar" and n_chars < 450:
            out("A-12", "warn", "a lone chart with a one-line conclusion reads as unfinished; add a takeaway sidebar (bullets, rows) or use panels", sid)
        sb = lay.get("sidebar") or {}
        if lay.get("variant") == "takeaway_sidebar":
            sb_chars = sum(len(x) for x in [sb.get("header", ""), sb.get("caption", "")] + sb.get("bullets", []) + [r["header"] + r["detail"] for r in sb.get("reasons", [])])
            if sb_chars < 160 and not sb.get("rows"):
                out("A-12", "warn", f"takeaway sidebar has ~{sb_chars} chars and no rows; it will look empty below the first line", sid)
        if s.get("callout") and body.get("kind") == "table":
            missing = [r["label"] for r in body["rows"] if r["label"] != s["callout"]["target"] and not r.get("note") and not r.get("benchmark")]
            if missing:
                out("A-12", "warn", f"table callout: rows without a note leave the verdict column empty ({', '.join(missing)})", sid)
        if body.get("kind") == "kpi" and any(not it.get("drivers") for it in body["items"]):
            out("A-12", "warn", "KPI items without drivers (2–4 lines on what drives each number)", sid)
    # A-02 statement emphasis must be words of the title
    if body and body.get("kind") == "text" and body.get("style") == "statement":
        for e in (body.get("statement") or {}).get("emphasis", []):
            if e.lower() not in lm.get("text", "").lower():
                out("A-02", "fail", f"statement emphasis '{e}' is not in the lead message", sid)
        if s.get("archetype") != "statement":
            out("schema+", "warn", "text style 'statement' used outside archetype 'statement'", sid)
    # quote-interview: every quote traces to its interview notes or survey (A-07)
    if body and body.get("kind") == "text" and body.get("style") == "quotes":
        for q in body.get("quotes", []):
            if q.get("placeholder"):
                continue
            if s.get("status") == "ghost":
                out("A-07", "warn", f"ghost slide shows a quote from '{q['speaker'][:30]}' as if it were real; mark it "
                    "placeholder: true unless it is verbatim from the user's material", sid)
            if not q.get("source_id"):
                out("A-07", "warn", f"quote from '{q['speaker'][:30]}' has no source_id (interview notes, survey)", sid)
            elif q["source_id"] not in srcs:
                out("A-07", "fail", f"quote cites unknown source {q['source_id']}", sid)
    # heatmap: low_is_better must name real columns; shading needs numbers
    if body and body.get("kind") == "table" and body.get("table_type") == "heatmap":
        for col in body.get("low_is_better", []):
            if col not in body["columns"]:
                out("schema+", "fail", f"low_is_better names '{col}', which is not a column", sid)
        if not any(cell.get("point") for r in body["rows"] for cell in r["cells"]):
            out("schema+", "fail", "heatmap has no numeric cells to shade", sid)
    # A-04 count word
    cw = lm.get("count_word")
    if cw and body:
        n = count_elements(body)
        named = len(body.get("highlight", [])) if body.get("kind") == "chart" else 0  # "four stores" may be the highlighted ones
        if n is not None and n != cw and named != cw: out("A-04", "fail", f"title says {cw}, body has {n} elements", sid)
    # A-05 two clauses
    if lm.get("clauses") == 2 and body and body.get("kind") != "panels" and s.get("layout", {}).get("variant") != "split_2":
        out("A-05", "warn", "two-clause title but not split_2 / panels", sid)
    # A-06 unit line on chart slides
    panels_ok = body and body.get("kind") == "panels" and all(pn.get("unit_line") for pn in body["panels"])
    if body and body.get("kind") in ("chart", "panels") and not s.get("unit_line") and not panels_ok:
        out("A-06", "fail", "chart slide without unit_line", sid)
    # A-07 / D5: every point resolves to a data point with a source
    has_ph = False
    for p in pts:
        if p.get("placeholder"):
            has_ph = True; continue
        d = dps.get(p["data_ref"])
        if not d: out("A-07", "fail", f"data_ref {p['data_ref']} not in data_points", sid); continue
        if d["source_id"] not in srcs: out("A-07", "fail", f"{d['id']} cites unknown source {d['source_id']}", sid)
        if srcs.get(d["source_id"], {}).get("kind") == "derived" and not d.get("derived_from"):
            out("A-07", "fail", f"{d['id']} is derived but lists no inputs", sid)
    quote_ph = body and body.get("kind") == "text" and body.get("style") == "quotes" and \
        any(q.get("placeholder") for q in body.get("quotes", []))
    has_ph = has_ph or bool(quote_ph)
    # L3 sticker
    if has_ph and s.get("sticker") != "ILLUSTRATIVE — DATA NEEDED":
        out("L3", "fail", "slide has placeholders but no 'ILLUSTRATIVE — DATA NEEDED' sticker", sid)
    if has_ph and s["status"] in ("filled", "qa_passed"):
        out("status", "fail", f"status {s['status']} but slide still has placeholders", sid)
    # backup
    if s["role"] == "backup" and s.get("backup_of") not in slides:
        out("S4", "fail", f"backup_of {s.get('backup_of')} does not exist", sid)

for d in dps.values():
    if d["slide_id"] not in slides: out("A-07", "fail", f"data point {d['id']} on unknown slide {d['slide_id']}")
    for x in d.get("derived_from", []):
        if x not in dps: out("A-07", "fail", f"{d['id']} derived from unknown {x}")

# A-12 variety: no single conclusion device dominates, and no three in a row
body_slides = [s for s in content if s.get("status") != "ghost" and s.get("archetype") != "statement"]
if len(body_slides) >= 4:
    from collections import Counter
    # the takeaway sidebar is the default for chart slides (A-11), so it is not counted
    cnt = Counter(device(s) for s in body_slides if device(s) not in ("none", "sidebar"))
    for dev, n in cnt.items():
        if n / len(body_slides) > 0.4:
            out("A-12", "warn", f"'{dev}' closes {n} of {len(body_slides)} content slides; mix devices (bar, line, callout, sidebar, none)")
    run = 1
    for a, b in zip(body_slides, body_slides[1:]):
        run = run + 1 if device(a) == device(b) and device(a) not in ("none", "sidebar") else 1
        if run == 3:
            out("A-12", "warn", f"'{device(b)}' used on three slides in a row", b["id"])
for s in content:
    co = s.get("callout")
    if co and s.get("body"):
        labels = [str(x) for x in collect_labels(s["body"])]
        if co["target"] not in labels:
            out("A-12", "fail", f"callout target '{co['target']}' matches no element on the slide", s["id"])
# D5: numbers written into text (bullets, captions, so_what, unit lines...) need a data point too
def _shown_values():
    vals = set()
    for d in dps.values():
        for v in (d.get("value"), d.get("value_high")):
            if isinstance(v, (int, float)):
                for x in (v, v * 100 if d.get("unit") == "%" else v, abs(v), abs(v) * 100 if d.get("unit") == "%" else abs(v)):
                    vals.add(round(x, 1)); vals.add(round(x)); vals.add(round(x, 2))
    return vals
_vals = _shown_values()
_NUM = re.compile(r"(?<![\w.])[$~]?(\d[\d,]*\.?\d*)\s?(%|x|pp|M|B|K)?")
TEXT_KEYS = {"text", "caption", "so_what", "unit_line", "header", "detail", "bullets", "note", "relation", "drivers",
             "footer", "support", "situation", "approach", "sub", "label"}
def _texts(o, key=None):
    if isinstance(o, str):
        if key in TEXT_KEYS:
            yield o
    elif isinstance(o, dict):
        for k, v in o.items():
            if k not in ("data_requirements", "rationale", "lead_message"):
                yield from _texts(v, k)
    elif isinstance(o, list):
        for v in o:
            yield from _texts(v, key)
for s in content:
    seen = set()
    for txt in _texts(s):
        txt = re.sub(r"(19|20)\d\d\s?[–-]\s?\d{2,4}", "", txt)  # year ranges like 2021–25
        for m in _NUM.finditer(txt):
            raw = m.group(1).replace(",", "")
            if not raw or re.fullmatch(r"(19|20)\d\d", raw) or (not m.group(2) and float(raw) < 10 and "." not in raw):
                continue  # years and small counting words ("3 levers") are fine
            try:
                v = float(raw)
            except ValueError:
                continue
            if round(v, 1) not in _vals and round(v) not in _vals and raw not in seen:
                seen.add(raw)
                out("D5", "warn", f"number '{m.group(0).strip()}' in text has no data point; add one (or remove the number): \"{txt[:50]}\"", s["id"])
# B-08: estimates show how they were built. calc must recompute the value; estimates need assumptions
import ast, operator
_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}
def _eval(expr):
    e = expr.replace("−", "-").replace("×", "*").replace("÷", "/")
    ids = sorted(dps, key=len, reverse=True)
    env = {}
    for k, i in enumerate(ids):
        e2 = re.sub(rf"(?<![\w.]){re.escape(i)}(?![\w-])", f"_v{k}", e)
        if e2 != e:
            env[f"_v{k}"] = dps[i]["value"]; e = e2
    def ev(n):
        if isinstance(n, ast.Expression): return ev(n.body)
        if isinstance(n, ast.BinOp) and type(n.op) in _OPS: return _OPS[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub): return -ev(n.operand)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)): return n.value
        if isinstance(n, ast.Name) and n.id in env: return env[n.id]
        raise ValueError(f"unknown term '{ast.unparse(n)}' (data point ids and + - * / only; spaces around '-')")
    return ev(ast.parse(e, mode="eval"))
for d in dps.values():
    if d.get("calc"):
        try:
            got = _eval(d["calc"])
            if abs(got - d["value"]) > max(0.011, abs(d["value"]) * 0.01):
                out("B-08", "fail", f"{d['id']}: calc '{d['calc']}' gives {got:.4g}, value is {d['value']}")
        except Exception as ex:
            out("B-08", "fail", f"{d['id']}: calc cannot be evaluated: {ex}")
    if d.get("estimate"):
        if not d.get("calc"): out("B-08", "fail", f"{d['id']} is an estimate without calc (needed for the live Excel formula)")
        if not d.get("assumptions"): out("B-08", "fail", f"{d['id']} is an estimate without assumptions")
    elif (srcs.get(d.get("source_id"), {}).get("kind") == "derived" and re.search(r"project|forecast|estimat|uplift|potential|would", d.get("label", ""), re.I)
          and not re.fullmatch(r"[\w.\s+-]+", d.get("calc") or "*")):  # a plain sum of sourced numbers is not our estimate
        out("B-08", "warn", f"{d['id']} ('{d['label'][:40]}') reads like an estimate; set estimate: true, calc and assumptions")
    elif srcs.get(d.get("source_id"), {}).get("kind") == "derived" and not d.get("calc"):
        out("B-08", "warn", f"{d['id']} is derived but has no calc; the Calculations sheet cannot show a live formula")
def _basis_refs(slide):
    """Refs whose basis is on the slide: basis strip, equation body, or a row/element carrying 'basis'."""
    refs = set(collect_data_refs(slide.get("basis") or {}))
    if (slide.get("body") or {}).get("kind") == "equation":
        refs |= set(collect_data_refs(slide["body"]))
    def walk(o):
        if isinstance(o, dict):
            if o.get("basis") and isinstance(o.get("basis"), str):
                refs.update(collect_data_refs(o))
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(slide)
    return refs
for s in content:
    if s.get("status") == "ghost":
        continue
    shown = set(collect_data_refs({k: s.get(k) for k in ("body", "layout", "lead_message", "callout")}))
    est = {r for r in shown if (dps.get(r) or {}).get("estimate")}
    covered = _basis_refs(s)
    # the basis also covers sibling estimates built from the same inputs (e.g. every bar of one projection)
    blocks = covered | {i for r in covered for i in (dps.get(r) or {}).get("derived_from", [])}
    missing = {r for r in est - covered if not (set(dps[r].get("derived_from", [])) <= blocks)}
    if missing:
        out("B-08", "fail", f"estimate(s) {', '.join(sorted(missing))} shown without their basis; add slide.basis (number cards), an equation body, or a row 'basis', or move the derivation to its own slide (B-03)", s["id"])
    # B-05: a plain sum, difference or remainder of body numbers is the same information again
    body_refs = set(collect_data_refs(s.get("body") or {}))
    for where, obj in (("sidebar", (s.get("layout") or {}).get("sidebar") or {}), ("callout", s.get("callout") or {})):
        for r in set(collect_data_refs(obj)) - body_refs:
            d = dps.get(r) or {}
            f = (d.get("calc") or d.get("formula") or "")
            if d.get("derived_from") and set(d["derived_from"]) <= body_refs and not re.search(r"[*×/÷]", f.split("=")[0]):
                out("B-05", "warn", f"{where} number {r} is a plain sum/difference/remainder of numbers the chart shows ({f[:40]}); replace with expected impact, a driver or a quote", s["id"])
    # B-10: lever numbers need column headers and a line saying what each number measures
    b = s.get("body") or {}
    if b.get("kind") == "levers" and any(it.get("point") for it in b["items"]):
        if not b.get("headers"): out("B-10", "fail", "lever numbers without column headers (body.headers)", s["id"])
        units = {(dps.get(it["point"].get("data_ref")) or {}).get("unit") for it in b["items"] if it.get("point")}
        if len(units) > 1 and any(it.get("point") and not it.get("metric") for it in b["items"]):
            out("B-10", "fail", "lever numbers in different units without 'metric' (what each number measures)", s["id"])
# Units (style.md): percentage differences are 'percentage points' in sentences and 'pp' in labels, never bare 'points'
def _all_text(o, path=""):
    if isinstance(o, str): yield path, o
    elif isinstance(o, dict):
        for k, v in o.items():
            if k not in ("data_requirements", "rationale", "excerpt", "inputs", "formula", "calc", "data_ref", "id"):
                yield from _all_text(v, f"{path}/{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o): yield from _all_text(v, f"{path}/{i}")
for path, txt in _all_text({k: v for k, v in spec.items() if k not in ("inputs", "sources")}):
    if re.search(r"\d\s?(?:-\s?)?points?\b", txt):
        out("units", "fail", f"'points' after a number at {path}: write 'percentage points' in sentences, 'pp' in labels: \"{txt[:60]}\"")
    sentence = re.search(r"/(lead_message/text|governing_thought|exec_summary/\d+/text|sub_points/\d+/text|bullets/\d+|so_what|key_takeaways/\d+)$", path)
    if sentence and re.search(r"\d\s?pp\b", txt):
        out("units", "warn", f"sentence uses 'pp'; spell out 'percentage points' in sentences (pp is for labels): \"{txt[:60]}\"")
    if sentence and re.search(r"\d(?:\.\d+)?x\b", txt):
        out("units", "warn", f"sentence uses 'Nx'; write 'N times' (x is for labels and pills): \"{txt[:60]}\"")
    if sentence and re.search(r"\bvs\.?\s", txt):
        out("units", "warn", f"sentence uses 'vs.'; write 'compared with': \"{txt[:60]}\"")
# A-12 (F3): sidebar value rows (label + number + bar) on at most a third of content slides, never two in a row
row_slides = [s for s in content if s.get("status") != "ghost"]
has_rows = [bool(((s.get("layout") or {}).get("sidebar") or {}).get("rows")) for s in row_slides]
if row_slides and sum(has_rows) > len(row_slides) / 3:
    out("A-12", "warn", f"sidebar value rows on {sum(has_rows)} of {len(row_slides)} content slides (max a third); use interpretation bullets or a big number instead")
for a_, b_, s_ in zip(has_rows, has_rows[1:], row_slides[1:]):
    if a_ and b_:
        out("A-12", "warn", "sidebar value rows on two slides in a row", s_["id"])
# B-12 (F5): a full deck does not leave "?" values
if spec["mode"] == "deck_detailed":
    n_ph = sum(1 for s in content for p in list(points(s.get("body"))) + list(points(s.get("layout"))) if p.get("placeholder"))
    n_ph += sum(1 for s in content for q in ((s.get("body") or {}).get("quotes") or []) if q.get("placeholder"))
    if n_ph:
        out("B-12", "warn", f"full deck still has {n_ph} '?' value(s): ask the user (multiple choice, with a recommended value and its basis) or estimate it from sourced inputs (B-08) before rendering")
# B-05 deck level: key takeaways that restate the exec summary
def _words(t): return set(re.findall(r"[a-z0-9%$.]+", t.lower())) - {"the", "a", "an", "and", "of", "to", "in", "our", "is", "by", "for", "with", "at"}
for kt in spec["storyline"].get("key_takeaways", []):
    for it in spec["storyline"]["exec_summary"]:
        a_, b_ = _words(kt), _words(it["text"])
        if a_ and len(a_ & b_) / len(a_) > 0.5:
            out("B-05", "warn", f"key takeaway repeats exec item {it['id']}; drop it and keep next steps only: \"{kt[:50]}\"")
if any(s["role"] == "end_page" for s in spec["slides"]) and not spec["storyline"].get("next_steps"):
    out("A-12", "warn", "end page has no storyline.next_steps; the right half will be empty")
# ---- V-01: the value appears in its excerpt -------------------------------------------------
_SCALE_WORDS = {"thousand": 1e3, "k": 1e3, "million": 1e6, "mn": 1e6, "mm": 1e6, "m": 1e6,
                "billion": 1e9, "bn": 1e9, "b": 1e9, "trillion": 1e12, "tn": 1e12, "t": 1e12}
_UNIT_SCALE = {"$K": 1e3, "$M": 1e6, "$B": 1e9, "$T": 1e12, "k": 1e3, "M": 1e6, "B": 1e9}
_NUM = re.compile(r"(?<![\w.])(\d{1,3}(?:,\d{3})+|\d+)(\.\d+)?(?:\s?(thousand|million|billion|trillion|mn|mm|bn|tn|[kKmMbBtT])(?![A-Za-z]))?")


def excerpt_numbers(text):
    """(raw, absolute) for every figure in the text; absolute applies a scale word ("1.2 billion")."""
    out = []
    for m in _NUM.finditer(text or ""):
        raw = float(m.group(1).replace(",", "") + (m.group(2) or ""))
        sc = _SCALE_WORDS.get((m.group(3) or "").lower(), 1)
        out.append((raw, raw * sc))
    return out


def _tol(x):
    """Half a unit of the last shown digit of x, so 1.2 matches 1.23 and 40 matches 40.4."""
    s = f"{abs(x):.6f}".rstrip("0").rstrip(".")
    dec = len(s.split(".")[1]) if "." in s else 0
    return 0.5 * 10 ** -dec + 1e-9


def value_in_excerpt(value, unit, text):
    """True / False, or None when the text has no figure to compare."""
    if value == 0 and re.search(r"\b(no|none|zero|nil|not any)\b", text or "", re.I):
        return True
    nums = excerpt_numbers(text)
    if not nums:
        return None
    v = abs(value)
    shown = [v] + ([v * 100] if unit in ("%", "pp") else [])
    absolute = v * _UNIT_SCALE.get(unit, 1)
    for raw, ab in nums:
        if any(abs(raw - c) <= _tol(c) for c in shown):
            return True
        if abs(ab - absolute) <= _tol(v) * _UNIT_SCALE.get(unit, 1):
            return True
    return False


_CUR = {"$": r"\$|USD|dollar", "€": r"€|EUR|euro", "£": r"£|GBP|pound", "¥": r"¥|JPY|yen|CNY|yuan", "₩": r"₩|KRW|won"}


def foreign_currency(unit, text):
    """The excerpt states money in another currency than the data point's unit ($M against '€4.2 billion')."""
    if not unit.startswith("$") or re.search(_CUR["$"], text or ""):
        return None
    for sym, pat in _CUR.items():
        if sym != "$" and re.search(pat, text or ""):
            return sym
    return None


# ---- V · source verification ------------------------------------------------------------------
import datetime
_this_year = datetime.date.today().year
lead_refs = set()  # numbers the reader takes away: titles and the executive summary
for s in content:
    lead_refs |= set(collect_data_refs((s.get("lead_message") or {})))
lead_refs |= set(collect_data_refs(spec["storyline"].get("exec_summary", [])))
no_trace = {}
for d in dps.values():
    src = srcs.get(d.get("source_id"), {})
    kind = src.get("kind")
    if kind == "derived" or d.get("estimate"):
        continue
    vals = [d["value"]] + ([d["value_high"]] if "value_high" in d else [])
    text = d.get("excerpt")
    if not text and kind == "user_provided":
        inp = next((i for i in spec.get("inputs", []) if i.get("id") == src.get("input_id")), {})
        if inp.get("kind") == "qa_answer":
            continue  # a value the user picked at a checkpoint is its own source
        text = inp.get("content") if isinstance(inp.get("content"), str) else None
        if not text and not d.get("locator"):
            no_trace.setdefault(src.get("id"), []).append(d["id"]); continue
    if not text:
        if kind == "web":
            out("V-01", "fail", f"{d['id']} ('{d['label'][:40]}') is from the web but has no excerpt; copy the sentence or table cell the value comes from", d["slide_id"])
        continue
    for v in vals:
        ok = value_in_excerpt(v, d.get("unit", ""), text)
        if ok is False:
            shown_v = f"{v * 100:g}%" if d.get("unit") == "%" else f"{v:g} {d.get('unit', '')}".strip()
            out("V-01", "fail", f"{d['id']} = {shown_v} is not in its excerpt: \"{text[:70]}\". Fix the value, quote the right passage, or make it a derived number with calc", d["slide_id"])
        elif ok is None and d.get("excerpt"):
            out("V-01", "warn", f"{d['id']}: excerpt has no figure to check {v:g} against: \"{text[:60]}\"", d["slide_id"])
    cur = foreign_currency(d.get("unit", ""), d.get("excerpt") or "")
    if cur:
        out("V-02", "fail", f"{d['id']} is in {d['unit']} but its excerpt is in {cur}; convert it as a derived number (calc, rate and date in assumptions)", d["slide_id"])
    years = set(re.findall(r"(?:19|20)\d\d", d.get("period") or ""))
    context = " ".join(str(x or "") for x in (d.get("excerpt"), d.get("locator")))  # not the source's own date: a 2026 report often holds 2025 data
    if years and d.get("excerpt") and re.search(r"(?:19|20)\d\d", context) and not years & set(re.findall(r"(?:19|20)\d\d", context)):
        out("V-02", "warn", f"{d['id']}: period {d['period']} does not appear in its excerpt or locator, which name other years; check the value is for that period", d["slide_id"])
for sid_, ids in no_trace.items():
    out("V-01", "warn", f"{len(ids)} data point(s) from {sid_} have neither excerpt nor locator ({', '.join(ids[:4])}{'…' if len(ids) > 4 else ''}); add the sheet, row or page they come from")
uses = {}
for d in dps.values():
    uses.setdefault(d.get("source_id"), []).append(d["id"])
for s in srcs.values():
    if s.get("kind") != "web":
        continue
    tier = s.get("tier")
    used = uses.get(s["id"], [])
    if not tier:
        out("V-03", "fail", f"web source {s['id']} ('{s['name'][:40]}') has no tier (T1 primary · T2 research or industry body · T3 reporting on another source · T4 not citable)")
    elif tier == "T4" and used:
        out("V-03", "fail", f"{s['id']} is T4 (blog, vendor marketing, aggregator); find the primary source for {', '.join(used[:4])}")
    elif tier == "T3":
        if not s.get("cites"):
            out("V-03", "warn", f"{s['id']} is T3: trace it to the primary source and cite that, or name it in 'cites'")
        key = sorted(set(used) & lead_refs)
        if key:
            out("V-03", "warn", f"title or exec summary number(s) {', '.join(key)} rest on T3 source {s['id']}; confirm them in a T1/T2 source")
    pub = re.match(r"(19|20)\d\d", str(s.get("published") or ""))
    if not pub:
        out("V-04", "warn", f"web source {s['id']} has no 'published' date")
    elif _this_year - int(pub.group(0)) >= 4 and not s.get("recency_ok"):
        out("V-04", "warn", f"{s['id']} was published in {pub.group(0)}; look for a newer edition, or say why it still holds in 'recency_ok'")
fails = [r for r in results if r[1] == "fail"]; warns = [r for r in results if r[1] == "warn"]
for rule, st, sid, det in results:
    if st != "pass" or rule == "schema":
        print(f"[{st.upper():4s}] {rule:7s} {('slide ' + sid) if sid else '':10s} {det}")
ghost = sum(1 for s in content if s["status"] == "ghost")
print(f"\n{len(content)} content slides ({ghost} ghost) · {len(dps)} data points · {len(srcs)} sources · {len(fails)} fail · {len(warns)} warn")
sys.exit(1 if fails else 0)
