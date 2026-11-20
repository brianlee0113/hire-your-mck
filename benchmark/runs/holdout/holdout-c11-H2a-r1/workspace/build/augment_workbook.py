"""Post-render step: list on each page sheet the numbers a slide shows as text (table cells, bullets,
footnotes), not only those drawn as data points. Keeps the renderer's columns and grading.

usage: python build/augment_workbook.py build/boreal-exclusivity.json deliverable/boreal-exclusivity-sources.xlsx
"""
import json, sys
sys.path.insert(0, "/Users/brianlee0113/hym-bench-work/_plugin/hire-your-mck-6f05966a12b9/skills/hire-your-mck/scripts")
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Border, Side
from renderer.pptx_render import Spec, collect_refs
from renderer.grade import grade, key_refs
from renderer.xlsx_render import COLS, _checks

TEXT_REFS = {
    "3": "adv pl_cash pl_v70 pl_v30 st_v70 st_v30 st ov30 ov70 uptime bar booked nroy",
    "4": "st r27 r28 r29 pl_roy rem28 cash28 pl_rcash pl_cash st27r st28r st29r st_roy rem28s cash28s st_rcash st_cash adv zero overst rev27x fwd roy",
    "5": "st dash cu cshare contr28 inc30 inc70 st28r sup28s inc50s lost50 arr gm ov50 ov30 ov70 roy sup f28",
    "6": "ov0 ov30 ov50 ov70 ov100 sup eng assess arr gm st pl_rob st_rob plB70 stB70",
    "7": "ov0 ov30 ov50 ov70 ov100 st cu eng be_rng f28 st28 mgate gate_y gate_q beN nunit dgm roy sup",
    "8": "hr_lab hr_bar tr_lab tr_bar lab_dt bar_dt hrs trial_n weeks assess f27",
    "9": "st booked f27 ov0 ov30 ov70 step10 ov10 arr gm vol_swing be_rng",
    "10": "adv dgm",
    "11": "st pl_v70 pl_v30 st_v70 st_v30 pl_N st_N nunit nmonths dgm assess buffer integ",
    "12": "st_rob ov30 ov70 st nroy roy nunit cu cush_s par30 par70 pl_rob eng3 assess",
    "13": "cash hd0 assess eng sup sup27 f27 hd_Nlag hd_X hd_Xslip buffer",
    "14": "ov70 assess nroy nmonths bar gate_q gate_y mgate dgm be70",
    "15": "nroy roy mgate gate_y arr dgm integ integ_sup pl_v70 pl_v30",
    "16": "be_rng beN_r be0_r eng ov0 ov30 ov70 sup thr70 thr30 r28 dgm f28",
    "17": "eng assess ov30 ov70 arr gm nroy nmonths hd_Nlag",
    "18": "assess sup eng hd_def",
    "A": ("roy sup ov30 ov70 st f27 f28 f29 pl_rob st27 st28 st29 st_rob r27 r28 r29 pl_roy st27r st28r st29r st_roy sup27 sup28 sup29 pl_sup "
          "sup27s sup28s sup29s st_sup eng eng3 contr27 contr28 contr29 pl_contr contr27s contr28s contr29s st_contr assess "
          "pl_v0 st_v0 lost30 lost70 pl_v30 pl_v70 st_v30 st_v70 adv cash28 cash28s pl_cash st_cash dgm arr gm"),
    "B": "adv sup eng assess arr gm dgm roy nroy cash buffer cut bar_dt lab_dt ov0 ov100 ov30 ov70",
}

spec_d = json.load(open(sys.argv[1]))
spec = Spec(spec_d)
key = key_refs(spec_d)
wb = load_workbook(sys.argv[2])
pages = {sl["id"]: i for i, sl in enumerate(spec_d["slides"], start=1)}
thin = Border(bottom=Side(style="thin", color="D5DBDF"))
idx = wb["Index"]
added_total = 0
for sl in spec_d["slides"]:
    sid = sl["id"]
    if sid not in TEXT_REFS:
        continue
    sheet = f"p{pages[sid]} (slide {sid})"[:31]
    ws = wb[sheet]
    shown = []
    for r in collect_refs({"b": sl.get("body"), "l": sl.get("layout"), "m": sl.get("lead_message")}):
        if r in spec.dp and r not in shown:
            shown.append(r)
            shown += [x for x in spec.dp[r].get("derived_from", []) if x in spec.dp and x not in shown]
    want = []
    for r in TEXT_REFS[sid].split():
        assert r in spec.dp, (sid, r)
        if r not in shown and r not in want:
            want.append(r)
    for r in want:
        d = spec.dp[r]
        s = spec.src.get(d.get("source_id"), {})
        calc = ""
        if d.get("formula") or d.get("derived_from"):
            calc = (d.get("formula") or "") + (f"  (from {', '.join(d['derived_from'])})" if d.get("derived_from") else "")
            if d.get("calc"):
                calc += "  → live formula on the Calculations sheet"
        g, why = grade(spec, r, key)
        ws.append([d.get("label"), d.get("value"), d.get("unit"), d.get("period"), s.get("name"), s.get("kind"),
                   s.get("tier"), g, s.get("url"), d.get("excerpt"), d.get("locator"), s.get("accessed"),
                   "written in the slide text (table cell, bullet or footnote)", calc, _checks(spec, d, why)])
        row = ws.max_row
        if d.get("unit") == "%":
            ws.cell(row=row, column=2).number_format = "0.0%"
        for col in range(1, len(COLS) + 1):
            ws.cell(row=row, column=col).alignment = Alignment(vertical="top", wrap_text=True)
            ws.cell(row=row, column=col).border = thin
    for row in idx.iter_rows(min_row=2):
        if row[5].value == sheet:
            row[3].value = (row[3].value or 0) + len(want)
    added_total += len(want)
wb.save(sys.argv[2])
print(f"added {added_total} text-shown numbers to page sheets")
