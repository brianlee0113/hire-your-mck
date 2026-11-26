"""Storyline spec -> sources.xlsx (one sheet per slide, A-07).

Every number on a slide is one row. Placeholders and open data requirements
are listed too, so the reader sees what is still missing.
"""
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

import re

from .grade import GRADES, grade, key_refs
from .pptx_render import Spec, collect_refs, fmt, has_placeholder

COLS = ["Data point", "Value", "Unit", "Period", "Source", "Source type", "Tier", "Grade", "URL", "Excerpt",
        "Locator", "Accessed", "Used in", "How it was calculated", "Checks"]
WIDTHS = [34, 12, 8, 12, 40, 13, 6, 7, 36, 44, 18, 12, 22, 34, 40]
GRADE_FILL = {"A": "E3F1E6", "B": None, "C": "FBE3E1", "E": "EEF3FB"}
URL_COL = COLS.index("URL") + 1


def _style_header(ws, row, color):
    for col in range(1, len(COLS) + 1):
        c = ws.cell(row=row, column=col)
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor=color)
        c.alignment = Alignment(vertical="center", wrap_text=True)


def render(spec_dict, out_path, primary="0B1F33"):
    spec = Spec(spec_dict)
    primary = primary.lstrip("#")
    wb = Workbook()
    idx = wb.active
    idx.title = "Index"
    idx.append(["Page", "Title", "Status", "Numbers with a source", "Numbers still missing", "Sheet"])
    for col in range(1, 7):
        c = idx.cell(row=1, column=col)
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor=primary)
    for w, col in zip([8, 70, 11, 22, 22, 12], "ABCDEF"):
        idx.column_dimensions[col].width = w
    thin = Border(bottom=Side(style="thin", color="D5DBDF"))
    missing_fill = PatternFill("solid", fgColor="FFF4D6")

    pages = {sl["id"]: i for i, sl in enumerate(spec_dict["slides"], start=1)}
    calc_rows = _calculations(wb, spec, primary)
    key = key_refs(spec_dict)
    for sl in spec_dict["slides"]:
        if sl["role"] not in ("content", "backup"):
            continue
        refs = []
        for r in collect_refs({"b": sl.get("body"), "l": sl.get("layout"), "m": sl.get("lead_message")}):
            if r in spec.dp and r not in refs:
                refs.append(r)
                for sub in spec.dp[r].get("derived_from", []):
                    if sub in spec.dp and sub not in refs:
                        refs.append(sub)
        open_reqs = [r for r in sl.get("data_requirements", []) if r.get("status") in ("needed", "not_found")]
        n_ph = _count_placeholders(sl.get("body")) + _count_placeholders(sl.get("layout"))
        sheet = f"p{pages[sl['id']]} (slide {sl['id']})"[:31]  # page number as on the slide
        ws = wb.create_sheet(sheet)
        title = (spec.prefix(sl) + " " + (sl.get("lead_message") or {}).get("text", "")).strip()
        ws["A1"] = title
        ws["A1"].font = Font(bold=True, size=13)
        ws["A2"] = f"Status: {sl['status']} · archetype: {sl.get('archetype', '')}"
        ws["A2"].font = Font(color="6A7682")
        ws.append([])
        ws.append(COLS)
        _style_header(ws, 4, primary)
        for i, w in enumerate(WIDTHS, start=1):
            ws.column_dimensions[get_column_letter(i)].width = w
        for r in refs:
            d = spec.dp[r]
            s = spec.src.get(d.get("source_id"), {})
            calc = ""
            if d.get("formula") or d.get("derived_from"):
                calc = (d.get("formula") or "") + (f"  (from {', '.join(d['derived_from'])})" if d.get("derived_from") else "")
            if r in calc_rows:
                calc += f"  → live formula: Calculations!C{calc_rows[r]}"
            g, why = grade(spec, r, key)
            ws.append([
                d.get("label"), d.get("value"), d.get("unit"), d.get("period"), s.get("name"), s.get("kind"),
                s.get("tier"), g, s.get("url"), d.get("excerpt"), d.get("locator"), s.get("accessed"), d.get("used_in"), calc,
                _checks(spec, d, why),
            ])
            row = ws.max_row
            v = ws.cell(row=row, column=2)
            if d.get("unit") == "%":
                v.number_format = "0.0%"
            if s.get("url"):
                ws.cell(row=row, column=URL_COL).hyperlink = s["url"]
            for col in range(1, len(COLS) + 1):
                ws.cell(row=row, column=col).alignment = Alignment(vertical="top", wrap_text=True)
                ws.cell(row=row, column=col).border = thin
            if GRADE_FILL[g]:
                ws.cell(row=row, column=COLS.index("Grade") + 1).fill = PatternFill("solid", fgColor=GRADE_FILL[g])
        for req in open_reqs:
            ws.append([req["description"], "MISSING", req.get("unit"), req.get("period"),
                       "; ".join(req.get("candidate_sources", [])), "needed", None, None, None,
                       req.get("recommended_exhibit"), None, None, "placeholder", None, None])
            for col in range(1, len(COLS) + 1):
                c = ws.cell(row=ws.max_row, column=col)
                c.fill = missing_fill
                c.alignment = Alignment(vertical="top", wrap_text=True)
        if n_ph and not open_reqs:
            ws.append([f"{n_ph} value(s) shown as “?” on the slide", "MISSING", None, None, None, "needed"])
            for col in range(1, len(COLS) + 1):
                ws.cell(row=ws.max_row, column=col).fill = missing_fill
        ws.freeze_panes = "A5"
        idx.append([pages[sl["id"]], title, sl["status"], len(refs), n_ph + len(open_reqs), sheet])
        idx.cell(row=idx.max_row, column=6).hyperlink = f"#'{sheet}'!A1"

    idx.append([])
    idx.append([None, "Grade: how far each number has been checked (column Grade on every page sheet)"])
    idx.cell(row=idx.max_row, column=2).font = Font(bold=True)
    for g, text in GRADES.items():
        idx.append([g, text])
        if GRADE_FILL[g]:
            idx.cell(row=idx.max_row, column=1).fill = PatternFill("solid", fgColor=GRADE_FILL[g])

    if "Calculations" in wb.sheetnames:  # after the page sheets, before Sources
        calc_ws = wb["Calculations"]
        wb._sheets.remove(calc_ws)
        wb._sheets.append(calc_ws)
    src = wb.create_sheet("Sources")
    src.append(["Id", "Name", "Type", "Tier", "Publisher", "URL", "Published", "Accessed", "Primary source (T3)", "Why still current"])
    for col in range(1, 11):
        c = src.cell(row=1, column=col)
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor=primary)
    for s in spec_dict.get("sources", []):
        src.append([s["id"], s.get("name"), s.get("kind"), s.get("tier"), s.get("publisher"), s.get("url"), s.get("published"),
                    s.get("accessed"), s.get("cites"), s.get("recency_ok")])
    for w, col in zip([6, 60, 14, 6, 30, 40, 11, 11, 30, 30], "ABCDEFGHIJ"):
        src.column_dimensions[col].width = w
    wb.save(out_path)
    return {"path": out_path, "sheets": len(wb.sheetnames)}


def _checks(spec, d, why):
    """What was done to check the number: re-fetch result and second sources."""
    parts = [why]
    v = d.get("verified") or {}
    if v.get("result"):
        parts.append(f"re-check {v['result'].replace('_', ' ')}" + (f" {v['at']}" if v.get("at") else "") +
                     (f" by {v['by']}" if v.get("by") else "") + (f": {v['note']}" if v.get("note") else ""))
    for c in d.get("corroboration", []):
        name = spec.src.get(c.get("source_id"), {}).get("name", c.get("source_id"))
        val = f" = {c['value']:g}" if isinstance(c.get("value"), (int, float)) else ""
        parts.append(f"second source: {name}{val}" + (f" ({c['note']})" if c.get("note") else ""))
    return "\n".join(p for p in parts if p)


def _count_placeholders(obj):
    if isinstance(obj, dict):
        return (1 if obj.get("placeholder") is True else 0) + sum(_count_placeholders(v) for v in obj.values())
    if isinstance(obj, list):
        return sum(_count_placeholders(v) for v in obj)
    return 0


OPS = {"−": "-", "×": "*", "÷": "/"}


def excel_formula(calc, cell_of):
    """'(us1 - pl1) * 100' -> '=(C5-C4)*100'. Ids are matched whole, longest first."""
    f = calc
    for a, b in OPS.items():
        f = f.replace(a, b)
    for i in sorted(cell_of, key=len, reverse=True):
        f = re.sub(rf"(?<![\w.]){re.escape(i)}(?![\w-])", cell_of[i], f)
    return "=" + f.replace(" ", "")


def _calculations(wb, spec, primary):
    """Every estimate and derived number with its inputs, assumptions and a live Excel formula (B-08)."""
    derived = [d for d in spec.dp.values() if d.get("calc")]
    if not derived:
        return {}
    need, order = set(), []
    def visit(i):
        if i in need or i not in spec.dp:
            return
        need.add(i)
        for sub in spec.dp[i].get("derived_from", []):
            visit(sub)
        order.append(i)  # inputs before the numbers built from them
    for d in derived:
        visit(d["id"])
    ws = wb.create_sheet("Calculations")
    ws["A1"] = "How every estimate is built: change an input (blue) and the numbers below it update"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = "Inputs come from the sources listed; estimates are team calculations. Assumptions are listed next to each estimate."
    ws["A2"].font = Font(color="6A7682")
    heads = ["Id", "Data point", "Value", "Unit", "Period", "Type", "Formula", "Assumptions", "Source"]
    ws.append([]); ws.append(heads)
    for col in range(1, len(heads) + 1):
        c = ws.cell(row=4, column=col)
        c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor=primary)
        c.alignment = Alignment(vertical="center", wrap_text=True)
    for w, col in zip([10, 46, 12, 8, 14, 11, 40, 52, 34], "ABCDEFGHI"):
        ws.column_dimensions[col].width = w
    rows = {i: 5 + k for k, i in enumerate(order)}
    cell_of = {i: f"C{r}" for i, r in rows.items()}
    for i in order:
        d = spec.dp[i]
        src = spec.src.get(d.get("source_id"), {})
        kind = "estimate" if d.get("estimate") else ("calculated" if d.get("calc") else "input")
        value = excel_formula(d["calc"], cell_of) if d.get("calc") else d.get("value")
        ws.append([i, d.get("label"), value, d.get("unit"), d.get("period"), kind, d.get("formula"),
                   "\n".join("• " + a for a in d.get("assumptions", [])), src.get("name")])
        r = ws.max_row
        v = ws.cell(row=r, column=3)
        v.number_format = "0.0%" if d.get("unit") == "%" else "#,##0.0#"
        if kind == "input":
            v.font = Font(color="1F4FD1")  # inputs in blue, formulas in black
        if kind == "estimate":
            for col in range(1, len(heads) + 1):
                ws.cell(row=r, column=col).fill = PatternFill("solid", fgColor="EEF3FB")
        for col in range(1, len(heads) + 1):
            ws.cell(row=r, column=col).alignment = Alignment(vertical="top", wrap_text=True)
    ws.freeze_panes = "A5"
    return rows
