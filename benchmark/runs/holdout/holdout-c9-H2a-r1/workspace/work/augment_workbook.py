"""Add the numbers written in each slide's text and table cells to that slide's sheet in the sources workbook.

The renderer lists only numbers drawn as points; table-heavy slides carry most numbers as text. This script
(1) checks, per slide, that every figure in the slide's text matches a data point listed in MENTIONS, and
(2) appends those data points to the slide's sheet with the same columns, source, grade and formula.
"""
import json, re, sys
from pathlib import Path
SK = "/Users/brianlee0113/hym-bench-work/_plugin/hire-your-mck-6f05966a12b9/skills/hire-your-mck/scripts"
sys.path.insert(0, SK)
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from renderer.pptx_render import Spec, collect_refs
from renderer import xlsx_render as X

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "deliverable" / "pelican-capacity.json"
XLSX = ROOT / "deliverable" / "pelican-capacity-sources.xlsx"

M = {
 "3": "cash rd capex cash_order floor gap_order ov28 mold_cap mold_lead ov30 ov30_short sov30 cash_avail dep cash_slot head_slot balance",
 "4": "slack27 slack_share np_slack ops_free ops_util scrap scr29 scr30 nameplate practical f2027",
 "5": "unsigned30 unsigned_share f2030 capex scr30 ov30 sov30 mold_cap practical spec_share scrap",
 "6": "dem28 dem29 dem30 int28 int29 int30 mold_m sup28 sup29 sup30 peak28 peak29 fill base_contrib practical contrib rebid_s25 rebid25_loss short30_loss mold_cap",
 "7": "floor gap_order new_money cash rd dep cash_order growth23",
 "8": "cash_order cash_slot cash_avail p28 cost_order capex fixed cost_rec dep mold_only_prem short30_loss ov30_short nothing_lost ov28 ov30 p29h fix15 save_rec fix_delay prem contrib",
 "9": "sh28 sh29 sh30 slack29 ov30_short spec_share sp29 mold_lead keep_unit contrib ov28 ov29 prem mold_cap",
 "10": "be ov30 mold_cap base_contrib adv ov30_short short30_loss fixed prem capex contrib keep_unit line_contrib line_net mold_net",
 "11": "short30_loss loss25 loss50 be_sh be25 be50 rebid_s25 rebid_s50 cash_slot head_slot dep_share headroom balance new_money sig_prem30 dep_years prem_2829 practical contrib capex dep floor ov30_short",
 "12": "dep lead sov30 sig_prem30 fixed sh29 headroom cash13",
 "13": "ov28 sh28 p28 slack27 scr29 mold_lead ov29 p29 f2027 practical scrap cover_total cover_mult mold_cap",
 "14": "thr s2029 s2030 balance fund_need cash_target fill thr_ov unsigned_rem cash_slot floor buffer lead val_extra int_after coverable mold_cap cash_slot_order",
 "15": "dep cash_slot balance fund_need lead val_extra",
 "16": "ov28 ov29 ov30 slip29 slip30 sov29 sov30 ov30_short sh29 sig_share30 cost_rec cash_target buffer slip_prem dep low_slip hd_slip sig_prem low_signed hd_signed mold_only_prem short30_loss low_nofund hd_nofund floor cash_avail fund_need prem contrib",
 "17": "unsigned30 fund_need val_extra scrap line14 cash13 balance",
 "18": "dep balance ov28 p28 thr fund_need cash_slot floor",
 "19": "cash rd cash_avail headroom capex cash_order gap_order dep cash_slot balance cash_slot_order new_money f2028 f2029 f2030 f2027 practical up27 up28 up29 up30 spec_share scrap scr29 scr30 ov28 ov29 ov30",
 "19b": "p28 p29 p30 prem ov28 ov29 mold_cap be fixed line_net mold_net adv cost_rec cost_order p29h fix15 be_sh be25 be50 contrib keep_unit ov30 dep practical",
 "20": "cash_avail practical contrib rebid_s25 rebid_s50 spec28 spec30 thr buffer scr30",
}
M = {k: v.split() for k, v in M.items()}

spec_d = json.loads(SPEC.read_text())
spec = Spec(spec_d)
dps = {d["id"]: d for d in spec_d["data_points"]}

TEXT_KEYS = {"text", "caption", "so_what", "unit_line", "header", "detail", "bullets", "note", "relation", "drivers",
             "footer", "support", "label", "point_caption", "metric", "foundation", "footnotes"}


def texts(o, key=None):
    if isinstance(o, str):
        if key in TEXT_KEYS:
            yield o
    elif isinstance(o, dict):
        for k, v in o.items():
            if k not in ("data_requirements", "rationale"):
                yield from texts(v, k)
    elif isinstance(o, list):
        for v in o:
            yield from texts(v, key)


def shown_vals(d):
    v = d["value"]; out = set()
    for x in (v, abs(v)) + ((v * 100, abs(v) * 100) if d["unit"] in ("%",) else ()):
        out |= {round(x, 2), round(x, 1), round(x)}
    return out


problems = []
for sl in spec_d["slides"]:
    sid = sl["id"]
    if sl["role"] not in ("content", "backup"):
        continue
    ids = set(M.get(sid, [])) | set(collect_refs({"b": sl.get("body"), "l": sl.get("layout"), "m": sl.get("lead_message")}))
    for i in ids:
        assert i in dps, (sid, i)
    allowed = set().union(*[shown_vals(dps[i]) for i in ids]) if ids else set()
    for t in texts(sl):
        t2 = re.sub(r"\b(19|20)\d\d\b", "", t)  # years
        t2 = re.sub(r"\b(Q[1-4]|H[12]|Gate \d|H\d|[1-6] ·)", "", t2)
        for m in re.finditer(r"(?<![\w.])[$~+−-]?(\d[\d,]*\.?\d*)", t2):
            raw = m.group(1).rstrip(".")
            if not raw:
                continue
            v = float(raw.replace(",", ""))
            if v in (1, 2, 3, 4, 5, 6) and "." not in raw:
                continue  # counting words and list numbers
            if round(v, 2) not in allowed and round(v, 1) not in allowed and round(v) not in allowed:
                problems.append((sid, raw, t[:70]))
for p in problems:
    print("UNMATCHED", p)

wb = openpyxl.load_workbook(XLSX)
pages = {sl["id"]: i for i, sl in enumerate(spec_d["slides"], start=1)}
key = X.key_refs(spec_d)
calc_rows = {}
if "Calculations" in wb.sheetnames:
    for row in wb["Calculations"].iter_rows(min_row=1):
        for c in row:
            pass
idx = wb["Index"]
idx_rows = {r[0].value: r for r in idx.iter_rows(min_row=2) if r[0].value is not None}
for sl in spec_d["slides"]:
    sid = sl["id"]
    if sid not in M:
        continue
    sheet = f"p{pages[sid]} (slide {sid})"[:31]
    ws = wb[sheet]
    listed = {ws.cell(row=r, column=1).value for r in range(5, ws.max_row + 1)}
    extra = [i for i in M[sid] if dps[i]["label"] not in listed]
    if not extra:
        continue
    ws.append([])
    ws.append(["Numbers written in this slide's text and table cells"])
    ws.cell(row=ws.max_row, column=1).font = Font(bold=True)
    for i in extra:
        d = dps[i]; s = spec.src.get(d.get("source_id"), {})
        calc = (d.get("formula") or "") + (f"  (from {', '.join(d['derived_from'])})" if d.get("derived_from") else "")
        g, why = X.grade(spec, i, key)
        ws.append([d.get("label"), d.get("value"), d.get("unit"), d.get("period"), s.get("name"), s.get("kind"), s.get("tier"), g,
                   s.get("url"), d.get("excerpt"), d.get("locator"), s.get("accessed"), "text or table cell on this slide", calc,
                   X._checks(spec, d, why)])
        r = ws.max_row
        if d.get("unit") == "%":
            ws.cell(row=r, column=2).number_format = "0.0%"
        for col in range(1, len(X.COLS) + 1):
            ws.cell(row=r, column=col).alignment = Alignment(vertical="top", wrap_text=True)
        if X.GRADE_FILL.get(g):
            ws.cell(row=r, column=X.COLS.index("Grade") + 1).fill = PatternFill("solid", fgColor=X.GRADE_FILL[g])
    row = idx_rows.get(pages[sid])
    if row is not None:
        row[3].value = (row[3].value or 0) + len(extra)
wb.save(XLSX)
print("workbook updated;", len(problems), "unmatched figures")
