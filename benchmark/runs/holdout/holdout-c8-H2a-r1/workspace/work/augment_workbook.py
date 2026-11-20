"""Add the numbers a slide shows as text (table cells, bullets, footnotes) to that page's sheet in the
sources workbook. The renderer lists only numbers drawn from data_ref points; slides whose money values
must keep two decimals carry them as text, so their data points are appended here with the same columns
and grades. Usage: python augment_workbook.py spec.json workbook.xlsx"""
import json, re, sys
sys.path.insert(0, "/Users/brianlee0113/hym-bench-work/_plugin/hire-your-mck-6f05966a12b9/skills/hire-your-mck/scripts")
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Border, Side
from renderer.pptx_render import Spec
from renderer.grade import grade, key_refs
from renderer.xlsx_render import _checks, COLS

TEXT_REFS = {
    "3": "k_save k_up exitfee e27 rC rX xmin sla cap g_e g_c auth",
    "4": "c_net27 cfo c_net28 x_net net_C net_X util28 k_up auth all_SQ27 all_X27 all_K27 k_save gap27_X",
    "5": "cfo dmg exitfee e27 c_net27 c_net27_x c_net28 all_K27 all_X27 fin98 s_keep mkt cap util27 util28",
    "6": "exitfee payback retro s_C gap27_C e28 d_e be_c_sq",
    "7": "k_vs_sq2 k_up tw_SQ tw_K tw_C tw_X k_save retro",
    "8": "be_c_sq be_x_k be_x_sq x_net fall_c fall_x e27 e28 k_save dmg xmin fe",
    "9": "h_C short_C h_X h_K need on_cw s_c s_w fin98 sla s_C s_X s_keep",
    "10": "pilot_n e27",
    "10b": "peak90 net_gate xmin sla thr",
    "11": "c28 e28 over28 retro lg_over g_e_lo g_c_lo",
    "12": "exitfee retro xmin mins ot_Cf spare testcap",
    "13": "gap27_SQ all_K27 net_K utilK28 k_up auth ot_D testcap gap27_X net_X exitfee spare gap27_C net_C util27 util28 retro c_net28",
    "14": "xmin b27 b28 xb27 xb28 all_K27 all_K28 rX swing",
    "14b": "k_save testcap exitfee mins b27 b28 k_up b_gain thr late_pp sla be_c_k",
    "15": "k_up guard95 e28 peak90 net_gate buffer costgate testcap",
    "16": "k_save all_SQ27 all_X27 h_K s_keep thr guard95 e27 be_c_sq e28 sla mkt",
    "17": ("tE_SQ tE_C tE_X tC tW fe fe_K fix_C xmin dmg all_SQ27 all_K27 all_C27 all_X27 tE_SQ28 tE_C28 tE_X28 tC28 "
           "all_SQ28 all_K28 all_C28 all_X28 k_up exitfee xb27 xb28 re rC rX rc rw w27 fc fw e28 c28 k_save retro s_c"),
    "18": "xmin rX b27 b28 k_save dmg dmg28 s_c s_w testcap g_e_lo g_c_lo",
}

spec_path, wb_path = sys.argv[1], sys.argv[2]
raw = json.load(open(spec_path))
spec = Spec(raw)
key = key_refs(raw)
src = {s["id"]: s for s in raw["sources"]}
pages = {sl["id"]: i for i, sl in enumerate(raw["slides"], start=1)}


def shown_forms(d):
    v = d["value"]
    vals = [v * 100] if d["unit"] in ("%",) else [v]
    if d["unit"] == "orders" or d["unit"] == "k":
        vals += [v, v * 1000]
    out = set()
    for x in vals:
        for x2 in (x, abs(x)):
            for dec in (0, 1, 2):
                out.add(f"{x2:,.{dec}f}"); out.add(f"{x2:.{dec}f}")
    return out


def slide_text(sl):
    return json.dumps({k: sl.get(k) for k in ("lead_message", "body", "layout", "footnotes", "so_what", "unit_line", "basis", "callout")},
                      ensure_ascii=False)


wb = load_workbook(wb_path)
thin = Border(bottom=Side(style="thin", color="D5DBDF"))
problems = []
for sid, ids in TEXT_REFS.items():
    sl = next(s for s in raw["slides"] if s["id"] == sid)
    text = slide_text(sl)
    sheet = f"p{pages[sid]} (slide {sid})"[:31]
    ws = wb[sheet]
    have = {(ws.cell(row=r, column=1).value, ws.cell(row=r, column=2).value) for r in range(5, ws.max_row + 1)}
    added = 0
    for i in ids.split():
        d = spec.dp[i]
        if not any(re.search(rf"(?<![\d.]){re.escape(f)}(?![\d])", text) for f in shown_forms(d)):
            problems.append(f"{sid}: {i} = {d['value']} not found in the slide text")
        if (d["label"], d["value"]) in have:
            continue
        s = src.get(d["source_id"], {})
        calc = ""
        if d.get("formula") or d.get("derived_from"):
            calc = (d.get("formula") or "") + (f"  (from {', '.join(d['derived_from'])})" if d.get("derived_from") else "")
            if d.get("calc"):
                calc += "  → live formula on the Calculations sheet"
        g, why = grade(spec, i, key)
        ws.append([d.get("label"), d.get("value"), d.get("unit"), d.get("period"), s.get("name"), s.get("kind"), s.get("tier"), g,
                   s.get("url"), d.get("excerpt"), d.get("locator"), s.get("accessed"), "text on the slide (table, bullet or footnote)",
                   calc, _checks(spec, d, why)])
        r = ws.max_row
        if d.get("unit") == "%":
            ws.cell(row=r, column=2).number_format = "0.0%"
        for col in range(1, len(COLS) + 1):
            ws.cell(row=r, column=col).alignment = Alignment(vertical="top", wrap_text=True)
            ws.cell(row=r, column=col).border = thin
        have.add((d["label"], d["value"])); added += 1
    idx = wb["Index"]
    for r in range(2, idx.max_row + 1):
        if idx.cell(row=r, column=6).value == sheet:
            idx.cell(row=r, column=4).value = ws.max_row - 4
    print(f"{sheet}: +{added} rows")
wb.save(wb_path)
print("\n".join(problems) or "every listed number appears in its slide's text")
