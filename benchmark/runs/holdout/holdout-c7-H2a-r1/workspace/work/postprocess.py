"""After render.py: (1) add the numbers written in slide text to each page sheet of the sources workbook,
(2) give every content slide whose numbers sit in text a Source line, styled like the renderer's own."""
import copy, json, os, sys
sys.path.insert(0, "/Users/brianlee0113/hym-bench-work/_plugin/hire-your-mck-6f05966a12b9/skills/hire-your-mck/scripts")
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Border, Side, PatternFill
from pptx import Presentation
from renderer.pptx_render import Spec, collect_refs
from renderer.grade import grade, key_refs
from renderer.xlsx_render import COLS, GRADE_FILL, _checks

HERE = os.path.dirname(os.path.abspath(__file__))
base = os.path.join(HERE, "..", "deliverable", "atlas-routesprout")
raw = json.load(open(base + ".json"))
spec = Spec(raw)
text_refs = json.load(open(os.path.join(HERE, "text_refs.json")))
pages = {sl["id"]: i for i, sl in enumerate(raw["slides"], start=1)}
slides = {sl["id"]: sl for sl in raw["slides"]}
key = key_refs(raw)

def expand(ids):
    out = []
    for r in ids:
        if r in spec.dp and r not in out:
            out.append(r)
            for sub in spec.dp[r].get("derived_from", []):
                if sub in spec.dp and sub not in out:
                    out.append(sub)
    return out

# 1 · workbook
wb = load_workbook(base + "-sources.xlsx")
thin = Border(bottom=Side(style="thin", color="D5DBDF"))
idx = wb["Index"]
for sid, ids in text_refs.items():
    sl = slides[sid]
    sheet = f"p{pages[sid]} (slide {sid})"[:31]
    ws = wb[sheet]
    have = expand(collect_refs({"b": sl.get("body"), "l": sl.get("layout"), "m": sl.get("lead_message")}))
    add = [r for r in expand(ids) if r not in have]
    for r in add:
        d = spec.dp[r]; s = spec.src.get(d.get("source_id"), {})
        calc = ""
        if d.get("formula") or d.get("derived_from"):
            calc = (d.get("formula") or "") + (f"  (from {', '.join(d['derived_from'])})" if d.get("derived_from") else "")
        g, why = grade(spec, r, key)
        ws.append([d.get("label"), d.get("value"), d.get("unit"), d.get("period"), s.get("name"), s.get("kind"), s.get("tier"), g,
                   s.get("url"), d.get("excerpt"), d.get("locator"), s.get("accessed"), "slide text (table cell, bullet or bar)", calc, _checks(spec, d, why)])
        row = ws.max_row
        if d.get("unit") == "%":
            ws.cell(row=row, column=2).number_format = "0.0%"
        for col in range(1, len(COLS) + 1):
            ws.cell(row=row, column=col).alignment = Alignment(vertical="top", wrap_text=True)
            ws.cell(row=row, column=col).border = thin
        if GRADE_FILL[g]:
            ws.cell(row=row, column=COLS.index("Grade") + 1).fill = PatternFill("solid", fgColor=GRADE_FILL[g])
    for row in idx.iter_rows(min_row=2):
        if row[5].value == sheet:
            row[3].value = len(have) + len(add)
wb.save(base + "-sources.xlsx")

# 2 · source lines
def names_for(ids):
    names, derived = [], False
    for r in ids:
        d = spec.dp.get(r); s = spec.src.get(d.get("source_id"), {})
        if s.get("kind") == "derived":
            derived = True
            continue
        if s.get("name") not in names:
            names.append(s.get("name"))
    for r in ids:
        if spec.src.get(spec.dp[r].get("source_id"), {}).get("kind") == "derived":
            for sub in expand([r]):
                s = spec.src.get(spec.dp[sub].get("source_id"), {})
                if s.get("kind") != "derived" and s.get("name") not in names:
                    names.append(s.get("name"))
    if derived:
        names.append("team analysis")
    return names

prs = Presentation(base + ".pptx")
template = None
for sl in prs.slides:
    for sh in sl.shapes:
        if sh.has_text_frame and sh.text_frame.text.startswith("Source"):
            template = sh; break
    if template: break
added = []
for sid, ids in text_refs.items():
    s_ = prs.slides[pages[sid] - 1]
    if any(sh.has_text_frame and sh.text_frame.text.startswith("Source") for sh in s_.shapes):
        continue
    names = names_for(expand(ids))
    text = ("Sources: " if len(names) > 1 else "Source: ") + "; ".join(names)
    el = copy.deepcopy(template._element)
    s_.shapes._spTree.append(el)
    new = s_.shapes[-1]
    runs = [r for p in new.text_frame.paragraphs for r in p.runs]
    runs[0].text = text
    for r in runs[1:]:
        r.text = ""
    added.append(pages[sid])
prs.save(base + ".pptx")
print("source lines added on pages", added)
