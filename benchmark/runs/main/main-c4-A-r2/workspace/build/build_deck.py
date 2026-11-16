"""Build the Palisade Docs 2027 pricing deck (python-pptx, native editable charts)."""
import re
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from lxml import etree

OUT = "deliverable/Palisade_2027_Pricing_Decision.pptx"

# ---- palette (dataviz reference palette; blue/orange validated, grey = de-emphasis) ----
NAVY = RGBColor(0x0D, 0x36, 0x6B)
BLUE = RGBColor(0x2A, 0x78, 0xD6)
ORANGE = RGBColor(0xEB, 0x68, 0x34)
GREY = RGBColor(0xB5, 0xB4, 0xAB)
INK = RGBColor(0x0B, 0x0B, 0x0B)
INK2 = RGBColor(0x52, 0x51, 0x4E)
MUTED = RGBColor(0x89, 0x87, 0x81)
HAIR = RGBColor(0xE1, 0xE0, 0xD9)
PALE = RGBColor(0xF3, 0xF2, 0xEE)
PALEBLUE = RGBColor(0xE8, 0xF1, 0xFC)
PALEORANGE = RGBColor(0xFD, 0xEE, 0xE7)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GREEN = RGBColor(0x00, 0x63, 0x00)
FONT = "Arial"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
page = {"n": 0}


# ------------------------------------------------------------------ helpers
def _runs(p, text, size, color, bold=False, italic=False):
    """Add runs to paragraph p, honouring **bold** markup."""
    parts = re.split(r"(\*\*[^*]+\*\*)", text)
    for part in parts:
        if not part:
            continue
        b = bold
        if part.startswith("**") and part.endswith("**"):
            part, b = part[2:-2], True
        r = p.add_run()
        r.text = part
        f = r.font
        f.name, f.size, f.bold, f.italic = FONT, Pt(size), b, italic
        f.color.rgb = color


def _bullet(p, level=0, char="•"):
    pPr = p._p.get_or_add_pPr()
    indent = 0.18 + 0.22 * level
    pPr.set("marL", str(int(Inches(indent))))
    pPr.set("indent", str(int(-Inches(0.18))))
    for tag in ("a:buNone", "a:buChar", "a:buAutoNum"):
        for el in pPr.findall(qn(tag)):
            pPr.remove(el)
    buf = etree.SubElement(pPr, qn("a:buFont"))
    buf.set("typeface", FONT)
    bu = etree.SubElement(pPr, qn("a:buChar"))
    bu.set("char", char)


def text(slide, x, y, w, h, paras, size=14, color=INK, anchor=MSO_ANCHOR.TOP,
         align=PP_ALIGN.LEFT, space_after=6, margin=0.05):
    """paras: list of str or dict(t=, size=, color=, bold=, bullet=level, align=, after=)."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    for side in ("left", "right", "top", "bottom"):
        setattr(tf, f"margin_{side}", Inches(margin))
    first = True
    for item in paras:
        if isinstance(item, str):
            item = {"t": item}
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = item.get("align", align)
        p.space_after = Pt(item.get("after", space_after))
        if "bullet" in item:
            _bullet(p, item["bullet"])
        _runs(p, item["t"], item.get("size", size), item.get("color", color),
              bold=item.get("bold", False), italic=item.get("italic", False))
    return tb


def rect(slide, x, y, w, h, fill=PALE, line=None, shape=MSO_SHAPE.RECTANGLE):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(0.75)
    s.shadow.inherit = False
    s.text_frame.margin_left = s.text_frame.margin_right = Inches(0.1)
    return s


def hline(slide, x, y, w, color=HAIR, weight=0.75):
    ln = slide.shapes.add_connector(1, Inches(x), Inches(y), Inches(x + w), Inches(y))
    ln.line.color.rgb = color
    ln.line.width = Pt(weight)
    return ln


def new_slide(title, kicker=None, source=None, notes=None):
    s = prs.slides.add_slide(BLANK)
    page["n"] += 1
    if kicker:
        text(s, 0.5, 0.22, 12.3, 0.35, [{"t": kicker.upper(), "size": 10, "color": BLUE, "bold": True, "after": 0}])
    text(s, 0.5, 0.52, 12.3, 0.95, [{"t": title, "size": 24, "color": NAVY, "bold": True, "after": 0}],
         anchor=MSO_ANCHOR.TOP)
    hline(s, 0.5, 1.45, 12.33, HAIR, 1)
    if source:
        text(s, 0.5, 6.98, 11.3, 0.4, [{"t": source, "size": 8.5, "color": MUTED, "after": 0}], anchor=MSO_ANCHOR.BOTTOM)
    text(s, 12.2, 6.98, 0.63, 0.4, [{"t": str(page["n"]), "size": 9, "color": MUTED, "align": PP_ALIGN.RIGHT}],
         anchor=MSO_ANCHOR.BOTTOM)
    if notes:
        s.notes_slide.notes_text_frame.text = notes
    return s


def _font(tf_or_font, size, color=INK2, bold=False):
    f = tf_or_font
    f.name, f.size, f.bold = FONT, Pt(size), bold
    f.color.rgb = color


def bar_chart(slide, x, y, w, h, categories, series, colors=None, point_colors=None,
              horizontal=False, fmt='0.0"%"', label_size=12, cat_size=11, legend=False,
              gap=60, overlap=0, max_val=None, stacked=False, hide_series=(), label_series=None):
    """series: list of (name, values). colors: per-series RGB. point_colors: {series_idx: [rgb,...]}"""
    cd = CategoryChartData()
    cd.categories = categories
    for name, vals in series:
        cd.add_series(name, vals)
    if stacked:
        ct = XL_CHART_TYPE.BAR_STACKED if horizontal else XL_CHART_TYPE.COLUMN_STACKED
    else:
        ct = XL_CHART_TYPE.BAR_CLUSTERED if horizontal else XL_CHART_TYPE.COLUMN_CLUSTERED
    gf = slide.shapes.add_chart(ct, Inches(x), Inches(y), Inches(w), Inches(h), cd)
    ch = gf.chart
    ch.font.name = FONT
    ch.font.size = Pt(cat_size)
    plot = ch.plots[0]
    plot.gap_width = gap
    plot.overlap = 100 if stacked else overlap
    va = ch.value_axis
    va.visible = False
    va.has_major_gridlines = False
    va.has_minor_gridlines = False
    if max_val is not None:
        va.maximum_scale = max_val
    va.minimum_scale = 0
    ca = ch.category_axis
    ca.has_major_gridlines = False
    ca.format.line.color.rgb = RGBColor(0xC3, 0xC2, 0xB7)
    _font(ca.tick_labels.font, cat_size, INK2)
    ca.major_tick_mark = 2  # none
    from pptx.enum.chart import XL_TICK_MARK
    ca.major_tick_mark = XL_TICK_MARK.NONE
    if horizontal:
        ca.reverse_order = True
        # with reversed category order the value axis would jump to top; keep it hidden anyway
    for i, s in enumerate(plot.series):
        s.invert_if_negative = False
        if i in hide_series:
            s.format.fill.background()
            s.format.line.fill.background()
            continue
        s.format.fill.solid()
        s.format.fill.fore_color.rgb = (colors[i] if colors else BLUE)
        s.format.line.color.rgb = WHITE
        s.format.line.width = Pt(1.5)
        if point_colors and i in point_colors:
            for j, c in enumerate(point_colors[i]):
                pt = s.points[j]
                pt.format.fill.solid()
                pt.format.fill.fore_color.rgb = c
                pt.format.line.color.rgb = WHITE
                pt.format.line.width = Pt(1.5)
        if label_series is None or i in label_series:
            s.data_labels.show_value = True
            s.data_labels.number_format = fmt
            s.data_labels.number_format_is_linked = False
            _font(s.data_labels.font, label_size, INK, True)
            if not stacked:
                s.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
    ch.has_legend = legend
    if legend:
        ch.legend.position = XL_LEGEND_POSITION.TOP
        ch.legend.include_in_layout = False
        _font(ch.legend.font, 11, INK2)
    return ch


def _manual_layout(chart, x, y, w, h):
    plotArea = chart._chartSpace.chart.plotArea
    layout = plotArea.find(qn("c:layout"))
    if layout is None:
        layout = etree.SubElement(plotArea, qn("c:layout"))
        plotArea.remove(layout)
        plotArea.insert(0, layout)
    for el in list(layout):
        layout.remove(el)
    ml = etree.SubElement(layout, qn("c:manualLayout"))
    for tag, val in (("layoutTarget", "inner"), ("xMode", "edge"), ("yMode", "edge"),
                     ("x", x), ("y", y), ("w", w), ("h", h)):
        e = etree.SubElement(ml, qn("c:" + tag))
        e.set("val", str(val))


def waterfall(slide, x, y, w, h, steps, fmt="{:.1f}", label_size=11, cat_size=10, max_val=None, min_val=0.0):
    """steps: list of (label, value, kind) kind in {'total','up','down'}. Labels drawn as text boxes above bars."""
    cats, base, up, down, tot, tops, labels, gap = [], [], [], [], [], [], [], []
    run = 0.0
    for label, v, kind in steps:
        cats.append(label)
        if kind == "total":
            run = v
            base.append(0); tot.append(v); up.append(None); down.append(None); gap.append(None)
            tops.append(v); labels.append(fmt.format(v))
        elif kind in ("up", "gap"):
            base.append(run); tot.append(None); down.append(None)
            up.append(v if kind == "up" else None); gap.append(v if kind == "gap" else None); run += v
            tops.append(run); labels.append("+" + fmt.format(v))
            continue
        else:
            base.append(run - v); down.append(v); tot.append(None); up.append(None); gap.append(None)
            tops.append(run); labels.append("\u2212" + fmt.format(v)); run -= v
    cd = CategoryChartData()
    cd.categories = cats
    cd.add_series("base", base)
    cd.add_series("Total", tot)
    cd.add_series("Increase", up)
    cd.add_series("Decrease", down)
    cd.add_series("Gap", gap)
    gf = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_STACKED, Inches(x), Inches(y), Inches(w), Inches(h), cd)
    ch = gf.chart
    ch.font.name = FONT
    plot = ch.plots[0]
    plot.gap_width = 45
    plot.overlap = 100
    va = ch.value_axis
    va.visible = False
    va.has_major_gridlines = False
    va.maximum_scale = max_val
    va.minimum_scale = min_val
    ca = ch.category_axis
    from pptx.enum.chart import XL_TICK_MARK
    ca.major_tick_mark = XL_TICK_MARK.NONE
    ca.format.line.color.rgb = RGBColor(0xC3, 0xC2, 0xB7)
    _font(ca.tick_labels.font, cat_size, INK2)
    colors = [None, NAVY, BLUE, ORANGE, GREY]
    for i, s in enumerate(plot.series):
        if i == 0:
            s.format.fill.background()
            s.format.line.fill.background()
            continue
        s.format.fill.solid()
        s.format.fill.fore_color.rgb = colors[i]
        s.format.line.color.rgb = WHITE
        s.format.line.width = Pt(1.5)
    ch.has_legend = False
    LX, LY, LW, LH = 0.01, 0.07, 0.98, 0.75
    _manual_layout(ch, LX, LY, LW, LH)
    n = len(steps)
    for i, (top, lab) in enumerate(zip(tops, labels)):
        frac = (top - min_val) / (max_val - min_val)
        ty = y + h * (LY + LH * (1 - frac)) - 0.34
        cx = x + w * (LX + LW * (i + 0.5) / n)
        bw = w * LW / n
        text(slide, cx - bw / 2, ty, bw, 0.32, [{"t": lab, "size": label_size, "bold": True, "color": INK,
                                                 "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.BOTTOM, margin=0)
    return ch, steps


def table(slide, x, y, w, h, data, col_w=None, header_fill=NAVY, size=11, row_h=None,
          first_col_bold=True, fills=None, bold_cells=(), colors=None, align_center_from=1):
    rows, cols = len(data), len(data[0])
    gf = slide.shapes.add_table(rows, cols, Inches(x), Inches(y), Inches(w), Inches(h))
    tbl = gf.table
    # strip default style banding
    tblPr = gf._element.graphic.graphicData.tbl.tblPr
    tblPr.set("firstRow", "0"); tblPr.set("bandRow", "0")
    if col_w:
        for i, cw in enumerate(col_w):
            tbl.columns[i].width = Inches(cw)
    if row_h:
        for i, rh in enumerate(row_h):
            tbl.rows[i].height = Inches(rh)
    for r in range(rows):
        for c in range(cols):
            cell = tbl.cell(r, c)
            cell.margin_left = cell.margin_right = Inches(0.08)
            cell.margin_top = cell.margin_bottom = Inches(0.04)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            if r == 0:
                cell.fill.fore_color.rgb = header_fill
            elif fills and (r, c) in fills:
                cell.fill.fore_color.rgb = fills[(r, c)]
            else:
                cell.fill.fore_color.rgb = WHITE if r % 2 else PALE
            tf = cell.text_frame
            tf.word_wrap = True
            val = data[r][c]
            lines = val.split("\n") if isinstance(val, str) else [str(val)]
            for k, line in enumerate(lines):
                p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
                p.alignment = PP_ALIGN.LEFT if c < align_center_from else PP_ALIGN.CENTER
                col = WHITE if r == 0 else (colors.get((r, c), INK) if colors else INK)
                b = (r == 0) or (c == 0 and first_col_bold) or ((r, c) in bold_cells)
                _runs(p, line, size, col, bold=b)
    return tbl


def callout(slide, x, y, w, h, title, body, fill=PALEBLUE, accent=BLUE, size=12):
    rect(slide, x, y, w, h, fill)
    rect(slide, x, y, 0.07, h, accent)
    paras = []
    if title:
        paras.append({"t": title, "size": size + 1, "bold": True, "color": NAVY, "after": 4})
    for b in body:
        if isinstance(b, dict):
            paras.append(b)
        else:
            paras.append({"t": b, "size": size, "color": INK, "after": 4})
    text(slide, x + 0.18, y + 0.1, w - 0.3, h - 0.2, paras)


def stat(slide, x, y, w, big, label, color=NAVY, big_size=30, label_size=11):
    text(slide, x, y, w, 0.6, [{"t": big, "size": big_size, "bold": True, "color": color, "after": 0}])
    text(slide, x, y + 0.62, w, 0.75, [{"t": label, "size": label_size, "color": INK2, "after": 0}])


SRC = "Source: Palisade Docs briefing pack, Nov 2026 (synthetic benchmark data)"

# =================================================================== 1. Title
s = prs.slides.add_slide(BLANK)
page["n"] += 1
rect(s, 0, 0, 13.333, 7.5, NAVY)
rect(s, 0.8, 2.15, 0.09, 2.2, ORANGE)
text(s, 1.1, 1.2, 11, 0.4, [{"t": "PALISADE DOCS  ·  2027 PRICING PLAN", "size": 13, "bold": True,
                              "color": RGBColor(0x9E, 0xC5, 0xF4)}])
text(s, 1.1, 2.05, 11.3, 1.9, [{"t": "Raise prices in 2027 where we have pricing power — "
                                     "and fix SMB before we reprice it",
                                "size": 36, "bold": True, "color": WHITE}])
text(s, 1.1, 4.0, 11, 0.5, [{"t": "Should Palisade raise prices while customer churn is rising, and if so, how?",
                             "size": 17, "color": RGBColor(0xCD, 0xE2, 0xFB)}])
text(s, 1.1, 5.55, 11, 0.9, [
    {"t": "For: Ravi Menon (CEO) and the leadership team  ·  Decision meeting, December 2026", "size": 13,
     "color": WHITE, "after": 4},
    {"t": "Prepared November 2026 from the internal briefing pack only (synthetic benchmark data; no external research)",
     "size": 11, "color": RGBColor(0x9E, 0xC5, 0xF4)}])

# =================================================================== 2. Exec summary
s = new_slide("Yes, raise prices in 2027 — but by segment: mid-market and enterprise from January, "
              "SMB only after a test",
              kicker="Executive summary", source=SRC + ". All ARR effects are end-2027 run-rate; see appendix for method.",
              notes="The one-page answer. Everything after this slide is the support.")
rows = [
    ("Churn is rising in one place",
     "SMB monthly logo churn rose 2.0% → 3.1%; mid-market 0.6% → 0.8%; enterprise flat at 0.2%. Within SMB, "
     "the 2025 50%-off promotion cohort explains **~90% of the increase**. Other SMB customers: 2.0% → 2.1%."),
    ("Price matters — but not where the CFO plan applies it hardest",
     "Core SMB churners cite price no more than in 2025 (18% vs 19%). But promo churners do (52%) after their "
     "discount ended, and Inkwell’s $9 Starter has cut our contested SMB win rate from **51% to 38%**."),
    ("$10.3M is a headline, not a 2027 number",
     "12% × all ARR ignores renewal timing and enterprise caps: only **$7.6M** is capturable in 2027, and an SMB "
     "churn response cuts that to **~$5.0–6.3M**, losing ~320–640 SMB customers."),
    ("Recommendation",
     "**Mid-market +10%** at renewal ($3.5M) · **Enterprise to contract terms** — 7% where capped, 10% otherwise "
     "($0.8M) · **Hold SMB list prices** in H1, run a controlled renewal test and an activation programme. "
     "= **$4.3M**, up to **~$5.1M** if the April/July checkpoints pass."),
    ("What it delivers",
     "If segments repeat trailing NRR, ARR reaches **~$98.3M (+14.2%)**; the 15% goal ($98.9M) needs ≥$0.7M "
     "new-logo ARR or the checkpoint upside. NRR stays ~114%, far above the 100% floor."),
]
yy = 1.68
for i, (h, b) in enumerate(rows):
    fill = PALEBLUE if i == 3 else (PALE if i % 2 == 0 else WHITE)
    hh = 0.98
    rect(s, 0.5, yy, 12.33, hh, fill)
    if i == 3:
        rect(s, 0.5, yy, 0.07, hh, BLUE)
    text(s, 0.7, yy, 3.3, hh, [{"t": h, "size": 13.5, "bold": True, "color": NAVY}], anchor=MSO_ANCHOR.MIDDLE)
    text(s, 4.1, yy, 8.6, hh, [{"t": b, "size": 12.5}], anchor=MSO_ANCHOR.MIDDLE)
    yy += hh + 0.06

# =================================================================== 3. What the plan must achieve
s = new_slide("The plan must add $12.9M of ARR with NRR above 100% — and only $65M of today’s $86M "
              "can be repriced in 2027",
              kicker="Decision criteria", source=SRC + " — sections 3, 5 and 8.",
              notes="Price changes apply at renewal. All SMB ARR renews in 2027, 85% of mid-market, 40% of "
                    "enterprise. 60% of enterprise ARR is capped at 7% a year; we assume the cap is spread "
                    "evenly across renewing and non-renewing enterprise contracts.")
stat(s, 0.5, 1.75, 3.6, "$98.9M", "2027 ARR goal: +15% (+$12.9M) on today’s $86.0M")
stat(s, 0.5, 3.05, 3.6, "> 100%", "Net revenue retention guardrail; today ~109% ARR-weighted "
                                   "(SMB 94%, mid-market 112%, enterprise 118%)")
stat(s, 0.5, 4.45, 3.6, "$65.4M", "ARR that renews — and so can be repriced — in 2027 (76% of total)")
text(s, 0.5, 5.75, 3.6, 1.1, [{"t": "Enterprise: 60% of ARR is under contracts that cap annual increases at 7%.",
                               "size": 11, "color": INK2}])
text(s, 4.6, 1.65, 8.2, 0.4, [{"t": "ARR by segment and whether it renews in 2027, $M", "size": 13, "bold": True,
                               "color": INK}])
ch = bar_chart(s, 4.5, 2.0, 8.3, 4.1, ["SMB", "Mid-market", "Enterprise"],
               [("Renews in 2027 — can be repriced", (21.0, 34.9, 9.6)),
                ("Does not renew in 2027", (0, 6.1, 14.4))],
               colors=[BLUE, GREY], stacked=True, fmt='0.0;;;', legend=True, gap=70, cat_size=12, label_size=12)
ch.plots[0].series[1].data_labels.font.color.rgb = INK
ch.plots[0].series[0].data_labels.font.color.rgb = WHITE
text(s, 4.6, 6.15, 8.2, 0.7, [{"t": "Renewal share: SMB 100% · mid-market 85% · enterprise 40%. "
                                    "Customers: SMB 5,900 · mid-market 1,350 · enterprise 150.",
                               "size": 11, "color": INK2}])

# =================================================================== 4. Churn by segment
s = new_slide("Churn rose in SMB; mid-market edged up and enterprise is flat",
              kicker="Where churn is rising", source=SRC + " — Table 1 (monthly logo churn, H1 2025 vs H1 2026).",
              notes="The board dashboard figure 1.4% → 2.3% is not defined and cannot be reproduced from Table 1: "
                    "customer-weighted churn is 1.7% → 2.6% and ARR-weighted 0.8% → 1.2% (using mid-2026 "
                    "counts). We use segment figures throughout and recommend finance define the board metric.")
text(s, 0.6, 1.65, 7.6, 0.4, [{"t": "Monthly logo churn by segment, %", "size": 13, "bold": True}])
ch = bar_chart(s, 0.5, 2.0, 7.7, 4.6, ["SMB", "Mid-market", "Enterprise"],
               [("H1 2025", (2.0, 0.6, 0.2)), ("H1 2026", (3.1, 0.8, 0.2))],
               colors=[GREY, BLUE], fmt='0.0"%"', legend=True, gap=80, overlap=-10, max_val=3.6, cat_size=12)
callout(s, 8.6, 1.75, 4.2, 2.4, "The rise is an SMB story",
        ["SMB is **80% of customers but 24% of ARR** ($21.0M).",
         "Mid-market and enterprise ($65M, 76% of ARR) still grow from their base: NRR **112% and 118%**.",
         "SMB NRR is **94%** — the only segment below 100%."])
callout(s, 8.6, 4.35, 4.2, 2.25, "Do not use the board’s “1.4% → 2.3%”",
        ["It is undefined and does not match Table 1 on either weighting (customer-weighted 1.7% → 2.6%; "
         "ARR-weighted 0.8% → 1.2%). **Action:** report churn by segment and cohort."],
        fill=PALEORANGE, accent=ORANGE)

# =================================================================== 5. Promo cohort
s = new_slide("Inside SMB, the 2025 promotion cohort explains ~90% of the churn increase",
              kicker="Why SMB churn rose",
              source=SRC + " — section 6. Promo-cohort churn is implied: (5,900 × 3.1% − 3,800 × 2.1%) ÷ 2,100, "
                           "using mid-2026 counts, so it is approximate.",
              notes="The promotion (Feb–Aug 2025) gave 50% off for six months. 2,100 promo customers remain "
                    "($4.4M ARR at full price). If they churned like other SMB customers, SMB churn would be 2.1% "
                    "instead of 3.1%: 1.0 of the 1.1-point rise.")
text(s, 0.6, 1.65, 7.6, 0.4, [{"t": "SMB monthly logo churn, %", "size": 13, "bold": True}])
bar_chart(s, 0.5, 2.0, 7.7, 4.6,
          ["Other SMB\nH1 2025", "Other SMB\nH1 2026", "All SMB\nH1 2026", "Promo cohort\nH1 2026 (implied)"],
          [("Monthly churn", (2.0, 2.1, 3.1, 4.9))], point_colors={0: [GREY, BLUE, BLUE, ORANGE]},
          fmt='0.0"%"', gap=55, max_val=5.6, cat_size=11.5)
stat(s, 8.6, 1.75, 4.2, "36% vs 56%", "Promo cohort’s share of SMB customers (2,100 of 5,900) vs. its share of "
                                     "SMB customers leaving each month (~103 of ~183)", color=ORANGE, big_size=28)
stat(s, 8.6, 3.2, 4.2, "41% vs 72%", "Share sending ≥5 documents in month one: promo cohort vs. other cohorts. "
                                     "Low-activation customers churn ~3× as often.", color=NAVY, big_size=28)
callout(s, 8.6, 4.75, 4.2, 1.6, "The worst is probably behind us",
        ["Discounts ended Aug 2025–Feb 2026 and most promo leavers left within two months. "
         "The cohort is only **$4.4M of ARR** — 5% of the total."], size=11.5)

# =================================================================== 6. Price reasons
s = new_slide("Price complaints rose only among promotion churners; core SMB looks no more "
              "price-sensitive than in 2025",
              kicker="Is it an onboarding problem or a price problem?",
              source=SRC + " — Table 2 (exit-survey respondents citing “price / found a cheaper option”) and "
                           "section 9. Decomposition is our estimate; see appendix.",
              notes="Rough decomposition: if activated customers churn at rate a and low-activation customers at 3a, "
                    "the 72%/28% mix of other SMB at 2.1% implies a ≈ 1.35%. With the promo cohort's 41%/59% mix that "
                    "predicts ~2.9%, against ~4.9% implied. So activation explains about 0.8 of the 2.8-point gap; the "
                    "rest coincides with the discount ending. Directional only.")
text(s, 0.6, 1.65, 7.6, 0.4, [{"t": "Churners citing price as main reason, % of survey respondents", "size": 13,
                               "bold": True}])
bar_chart(s, 0.5, 2.0, 7.7, 4.6,
          ["All SMB\nH1 2025", "All SMB\nH1 2026", "Other SMB\nH1 2026", "Promo cohort\nH1 2026"],
          [("Cite price", (19, 34, 18, 52))], point_colors={0: [GREY, GREY, BLUE, ORANGE]},
          fmt='0"%"', gap=55, max_val=60, cat_size=11.5)
callout(s, 8.6, 1.75, 4.2, 1.6, "The 34% is a mix, not a trend",
        ["It averages promo churners (52%) and other SMB churners (18%, flat vs. 19% in 2025)."], size=11.5)
callout(s, 8.6, 3.5, 4.2, 3.1, "Both sides are partly right",
        ["**CFO:** the core base is not leaving over price — yet.",
         "**CEO:** price does drive exits where customers face a jump; promo customers saw +100% when the "
         "discount ended.",
         "**Customer Success:** low activation explains only ~0.8 of the ~2.8-point gap; onboarding alone "
         "will not close it."], size=11.5)

# =================================================================== 7. Inkwell
s = new_slide("But Inkwell has made SMB price-sensitive at the point of sale: our contested win rate fell "
              "from 51% to 38%",
              kicker="Competitive exposure", source=SRC + " — section 7.",
              notes="A list-price rise also applies to new sign-ups. A 12% rise takes the SMB plan from $15 to $16.80 "
                    "against Inkwell Starter at $9. Inkwell has not been seen in mid-market or enterprise deals over "
                    "200 seats; we do not know how much of mid-market is 51–200 seats.")
text(s, 0.6, 1.65, 5.2, 0.4, [{"t": "SMB win rate where Inkwell was considered", "size": 13, "bold": True}])
bar_chart(s, 0.5, 2.0, 5.3, 4.5, ["H1 2025", "H1 2026"], [("Win rate", (51, 38))],
          point_colors={0: [GREY, ORANGE]}, fmt='0"%"', gap=70, max_val=60, cat_size=12)
text(s, 6.3, 1.65, 6.5, 0.4, [{"t": "List price, $ per user per month", "size": 13, "bold": True}])
bar_chart(s, 6.2, 2.0, 6.6, 3.0,
          ["Inkwell Starter (Oct 2025)", "Palisade SMB", "Palisade SMB at +12%", "Inkwell Pro", "Palisade Business"],
          [("Price", (9, 15, 16.8, 24, 29))], horizontal=True,
          point_colors={0: [ORANGE, BLUE, GREY, ORANGE, BLUE]}, fmt='"$"0.00', gap=40, max_val=34, cat_size=11)
callout(s, 6.3, 5.15, 6.5, 1.45, "Implication",
        ["Raising SMB list price widens a $6 gap to $7.80 while we already lose 62% of contested deals. "
         "Mid-market and enterprise are not exposed: Inkwell has not appeared in deals above 200 seats."],
        fill=PALEORANGE, accent=ORANGE, size=11.5)

# =================================================================== 8. Segment matrix
s = new_slide("Pricing power sits in mid-market and enterprise, not in SMB",
              kicker="Segment assessment", source=SRC + " — sections 5–9.",
              notes="Colour shading: blue = supports a price rise, orange = argues against.")
data = [
    ["Evidence", "SMB", "Mid-market", "Enterprise"],
    ["Churn trend (monthly)", "2.0% → 3.1%\n(core 2.0% → 2.1%)", "0.6% → 0.8%", "0.2% → 0.2%"],
    ["Net revenue retention", "94%", "112%", "118%"],
    ["Competitor exposure", "Inkwell $9; win rate 51% → 38%", "Not seen above 200 seats", "Not seen"],
    ["Price-response evidence", "2023 +8%: churn 1.8% → 2.3% for six months, then 1.9% — before Inkwell",
     "2024 +10% on new sign-ups: conversion 23.1% vs 23.6% (not significant)", "No test; contracts set terms"],
    ["What keeps customers", "Nothing cited; activation weak (41% in promo cohort)", "Integrations, audit trail (advisory board)", "Integrations, audit trail (advisory board)"],
    ["Repriceable ARR in 2027", "$21.0M (100%)", "$34.9M (85%)", "$9.6M (40%); 60% capped at 7%"],
    ["Verdict", "Hold list price; test first", "Raise +10% at renewal", "Raise to contract terms"],
]
B, O = PALEBLUE, PALEORANGE
fills = {(1, 1): O, (1, 2): B, (1, 3): B, (2, 1): O, (2, 2): B, (2, 3): B, (3, 1): O, (3, 2): B, (3, 3): B,
         (4, 1): O, (4, 2): B, (5, 1): O, (5, 2): B, (5, 3): B,
         (7, 1): O, (7, 2): B, (7, 3): B}
table(s, 0.5, 1.7, 12.33, 5.1, data, col_w=[2.6, 3.4, 3.3, 3.03], size=11.5,
      row_h=[0.45, 0.65, 0.5, 0.6, 0.95, 0.55, 0.6, 0.55], fills=fills,
      bold_cells={(7, 1), (7, 2), (7, 3)})

# =================================================================== 9. CFO waterfall
s = new_slide("The CFO’s $10.3M shrinks to ~$5–6M once renewal timing, contract caps and SMB churn are counted",
              kicker="Testing the CFO plan: +12% on every plan at renewal",
              source=SRC + ". SMB churn response scales the 2023 +8% pattern linearly to 12% (+3.6 pts of customers "
                           "lost in year one × 1.5); stress case doubles it. Run-rate ARR at end-2027.",
              notes="Arithmetic: headline 12% × $86.0M = $10.3M. Mid-market non-renewing 15% × $41.0M × 12% = $0.74M. "
                    "Enterprise non-renewing 60% × $24.0M × 12% = $1.73M. Cap: $5.76M capped renewing ARR × 5 pts = "
                    "$0.29M. Capturable $7.57M. SMB response: 5.4% of SMB ARR at new price ($23.5M) = $1.27M; "
                    "stress 10.8% = $2.54M.")
steps = [("Headline\n(12% × $86.0M)", 10.32, "total"),
         ("Mid-market ARR\nnot renewing", 0.74, "down"),
         ("Enterprise ARR\nnot renewing", 1.73, "down"),
         ("Enterprise\n7% caps", 0.29, "down"),
         ("Capturable\nin 2027", 7.57, "total"),
         ("SMB churn\n(2023 pattern)", 1.27, "down"),
         ("Net, 2023\npattern", 6.30, "total"),
         ("Extra SMB churn\nif response 2×", 1.27, "down"),
         ("Net, stress\ncase", 5.03, "total")]
waterfall(s, 0.5, 1.7, 8.6, 5.15, steps, fmt="${:.1f}M", max_val=11, cat_size=10, label_size=11)
callout(s, 9.4, 1.75, 3.45, 2.35, "Not in the $10.3M",
        ["Only 40% of enterprise and 85% of mid-market ARR renew in 2027.",
         "SMB losses: **~320–640 customers**, many likely to Inkwell."], size=12.5)
callout(s, 9.4, 4.25, 3.45, 2.6, "Also unpriced",
        ["A list rise hits new SMB sign-ups, where we lose 62% of contested deals.",
         "Mid-market +12% is above the only tested level (+10%)."], fill=PALEORANGE, accent=ORANGE, size=12.5)

# =================================================================== 10. Break-even
s = new_slide("Mid-market can absorb +10%; an SMB rise is a coin-flip that could net close to zero",
              kicker="Risk-reward by segment",
              source=SRC + ". Break-even share of repriced ARR lost = p ÷ (1 + p). SMB scenarios as on the previous "
                           "slide. Mid-market annual churn ≈ 1 − (1 − 0.8%)^12 ≈ 9%.",
              notes="For a price rise p, the rise loses money only if more than p/(1+p) of the repriced ARR leaves "
                    "because of it: 9.1% at +10%, 10.7% at +12%.")
text(s, 0.6, 1.65, 6.4, 0.4, [{"t": "SMB +12%: net 2027 ARR gain, $M", "size": 13, "bold": True}])
bar_chart(s, 0.5, 2.0, 6.3, 3.6, ["Gross uplift", "Net, 2023\nchurn pattern", "Net, response\n2× 2023"],
          [("Net ARR", (2.52, 1.25, 0.02))], point_colors={0: [GREY, BLUE, ORANGE]}, fmt='"$"0.0"M"',
          gap=60, max_val=3.0, cat_size=11.5)
text(s, 0.6, 5.7, 6.2, 1.1, [
    {"t": "Extra SMB customers lost: **~320** (2023 pattern) to **~640** (2×). Break-even is 10.7% of SMB ARR "
          "lost — the stress case (10.8%) sits on it. We cannot yet tell which case applies: that is uncertainty #1 "
          "in the pack.", "size": 11.5, "color": INK2}])
rect(s, 7.3, 1.75, 5.55, 4.95, PALEBLUE)
rect(s, 7.3, 1.75, 0.07, 4.95, BLUE)
text(s, 7.55, 1.85, 5.2, 0.4, [{"t": "Mid-market +10%", "size": 14, "bold": True, "color": NAVY}])
stat(s, 7.55, 2.3, 5.1, "$3.5M", "Run-rate uplift: 10% × $34.9M renewing ARR", big_size=28)
stat(s, 7.55, 3.55, 5.1, "9.1%", "Share of repriced ARR that would have to leave before the rise loses money "
                                  "— roughly **doubling** today’s ~9% annual logo churn", big_size=28)
text(s, 7.55, 4.95, 5.15, 1.7, [
    {"t": "Why we expect far less:", "size": 11.5, "bold": True, "after": 3},
    {"t": "2024 +10% test: no significant conversion effect", "size": 11.5, "bullet": 0, "after": 2},
    {"t": "NRR 112%; integrations and audit trail keep customers", "size": 11.5, "bullet": 0, "after": 2},
    {"t": "No Inkwell presence above 200 seats", "size": 11.5, "bullet": 0, "after": 2}])

# =================================================================== 11. Options
s = new_slide("The segmented plan gives up to $2M of paper ARR to avoid an unmeasured bet on SMB",
              kicker="Options compared",
              source=SRC + ". End-2027 ARR assumes each segment repeats its trailing-12-month NRR (+$8.0M on the base) "
                           "plus price effects; new-logo ARR is excluded because the pack has no forecast.",
              notes="Option B ranges include the checkpoint upside: mid-market H2 renewals stepped to 12% (+$0.35M) "
                    "and SMB +8% on H2 renewals if the test passes (~+$0.5M net).")
data = [
    ["", "A. CFO plan\n+12% on every plan", "B. Segmented (recommended)\nMM +10%, Ent to terms, SMB hold + test",
     "C. Hold all prices"],
    ["2027 price uplift (run-rate)", "$5.0–6.3M", "$4.3M (up to $5.1M via checkpoints)", "$0"],
    ["End-2027 ARR, before new logos", "$99.0–100.3M", "$98.3M (up to $99.1M)", "$94.0M"],
    ["Growth vs. 15% goal", "+15.1% to +16.6%", "+14.2%; needs ≥$0.7M new-logo ARR\n(or checkpoint upside)",
     "+9.3%; needs $4.9M new-logo ARR"],
    ["Overall NRR", "~115–117%", "~114%", "~109%"],
    ["Extra SMB customers lost", "~320–640", "Test group only", "None"],
    ["Main risk", "SMB churn response unknown; feeds Inkwell; MM priced above tested level",
     "Relies on new-logo ARR or checkpoint upside to clear 15%", "Misses growth goal; leaves MM/Ent value unused"],
]
fills = {(r, 2): PALEBLUE for r in range(1, 7)}
table(s, 0.5, 1.7, 12.33, 4.9, data, col_w=[2.9, 3.0, 3.6, 2.83], size=11.5,
      row_h=[0.75, 0.55, 0.55, 0.8, 0.5, 0.5, 0.95], fills=fills, bold_cells={(0, 2)} | {(r, 2) for r in (1, 2, 3)})
text(s, 0.5, 6.38, 12.33, 0.55, [{"t": "Why B over A: A’s extra ARR is mostly the SMB rise, worth $0–1.3M net with "
                                      "downside, in the one segment where we lack evidence. B can recover most of it by "
                                      "July once the test shows whether the risk is real.", "size": 11.5, "bold": True,
                                 "color": NAVY}])

# =================================================================== 12. Growth bridge
s = new_slide("The recommended plan gets ARR to ~$98.3M; closing the last $0.7M to the 15% goal needs "
              "new-logo ARR or the checkpoint upside",
              kicker="2027 ARR bridge, recommended plan ($M)",
              source=SRC + ". Base movement = segment ARR × (trailing NRR − 1): SMB 94%, mid-market 112%, enterprise 118%. "
                           "Assumes trailing NRR repeats; each 1 pt of overall NRR ≈ $0.9M.",
              notes="This is a planning bridge, not a forecast. The pack contains no new-business pipeline, so "
                    "new-logo ARR is shown as the residual needed to reach $98.9M.")
steps = [("2026 ARR", 86.0, "total"),
         ("SMB at\n94% NRR", 1.26, "down"),
         ("Mid-market\nat 112% NRR", 4.92, "up"),
         ("Enterprise\nat 118% NRR", 4.32, "up"),
         ("Mid-market\n+10%", 3.49, "up"),
         ("Enterprise\nto terms", 0.79, "up"),
         ("Plan before\nnew logos", 98.26, "total"),
         ("Needed: new logos\nor checkpoints", 0.65, "gap"),
         ("2027 goal\n(+15%)", 98.9, "total")]
ch, _ = waterfall(s, 0.5, 1.7, 9.0, 5.15, steps, fmt="{:.1f}", min_val=80, max_val=100, cat_size=10, label_size=11)
callout(s, 9.8, 1.75, 3.05, 2.4, "SMB pricing is not needed to reach the goal",
        ["Mid-market and enterprise expansion plus their price rises do most of the work.",
         "SMB is the only segment shrinking on its own (−$1.3M at 94% NRR)."], size=12.5)
callout(s, 9.8, 4.3, 3.05, 2.55, "Checkpoint upside ≈ $0.85M",
        ["Mid-market H2 renewals at 12%: ~$0.35M.", "SMB +8% on H2 renewals if test passes: ~$0.5M net.",
         "Grey bar = the residual the pack cannot fill: it has no new-logo forecast."], size=12.5)

# =================================================================== 13. SMB plan
s = new_slide("In SMB, fix activation and measure price sensitivity before repricing",
              kicker="The SMB plan for H1 2027", source=SRC + " — sections 6, 8, 10 and 11.",
              notes="The Customer Success claim to halve SMB churn within two quarters is not supported by the pack. "
                    "Halving 3.1% gives 1.55%, lower than any SMB level in the pack (2023 settled at 1.9%; core SMB "
                    "is 2.1%). If the promo cohort behaved exactly like other SMB customers, SMB churn would be 2.1%, "
                    "a one-third cut. Treat onboarding as upside, not plan.")
measures = ["**Watch:** core SMB churn (2.1%) and Inkwell-contested win rate (38%) do not worsen",
            "**Watch:** share of new customers sending ≥5 documents in month one (72% today; 41% for promo)",
            "**Decides:** whether SMB can take +8% on H2 renewals (July checkpoint)"]
cols = [
    ("1  Hold list prices", BLUE,
     ["Keep SMB $15 and Business $29 through H1 2027.",
      "Exclude the promo cohort from any 2027 rise — they cite price at 52% and just took a +100% step.",
      "Revisit in July with test results."]),
    ("2  Activation programme", BLUE,
     ["Target customers sending <5 documents in month one (59% of the promo cohort).",
      "Goal: bring promo-cohort churn (~4.9%) toward core SMB (2.1%).",
      "Ceiling: SMB churn 3.1% → ~2.1%, a **one-third** cut — not the “halve in two quarters” claimed (1.55%, "
      "below any SMB level on record)."]),
    ("3  Controlled renewal-price test", BLUE,
     ["Randomly assign part of non-promo SMB renewals to +8% (the 2023 level we can benchmark); the rest stay at "
      "current price.",
      "Measure 90-day churn and price-citing exits vs. control.",
      "Also track Inkwell-contested win rate on new sign-ups."]),
]
x0 = 0.5
for (title_, col, items), meas in zip(cols, measures):
    rect(s, x0, 1.75, 3.95, 0.55, col)
    text(s, x0 + 0.1, 1.75, 3.8, 0.55, [{"t": title_, "size": 14, "bold": True, "color": WHITE}],
         anchor=MSO_ANCHOR.MIDDLE)
    rect(s, x0, 2.3, 3.95, 3.55, PALE)
    text(s, x0 + 0.12, 2.42, 3.72, 2.5, [{"t": t, "size": 12.5, "bullet": 0, "after": 8} for t in items])
    hline(s, x0 + 0.12, 4.95, 3.7, GREY, 0.75)
    text(s, x0 + 0.12, 5.0, 3.72, 0.85, [{"t": meas, "size": 11.5, "color": INK2}])
    x0 += 4.19
callout(s, 0.5, 6.0, 12.33, 0.85, None,
        [{"t": "**Do not bank onboarding savings in the 2027 plan.** Count them only once the activation rate of new "
               "cohorts moves.", "size": 12.5, "color": NAVY}])

# =================================================================== 14. Roadmap & gates
s = new_slide("Roll out in waves, with two checkpoints that decide whether to go further",
              kicker="Implementation and decision gates",
              source="Checkpoint thresholds are proposals for leadership to confirm; they sit well inside the break-even "
                     "points (mid-market ~1.6%/month, SMB 10.7% of ARR).",
              notes="Mid-market pause trigger of 1.2%/month is half-way between today's 0.8% and the level that would "
                    "roughly erase the gain (~1.6%). Renewal notice periods are not in the pack; adjust the January "
                    "start if contracts require longer notice.")
phases = [("Dec 2026", "Decide",
           ["Approve segmented plan", "Finance defines the board churn metric and the new-logo forecast"]),
          ("Jan–Mar 2027", "Launch",
           ["Mid-market +10% and enterprise to terms on renewals", "SMB test and activation programme start"]),
          ("April 2027", "Checkpoint 1: mid-market",
           ["Repriced renewals churn ≤1.0%/mo → step H2 renewals to 12%",
            "1.0–1.2%/mo → stay at 10%", "Above 1.2%/mo → pause and review"]),
          ("July 2027", "Checkpoint 2: SMB",
           ["Test churn within 2023 pattern (≤ +0.5 pt, fading in 6 months) → +8% on H2 non-promo renewals",
            "Otherwise hold; rethink SMB packaging for 2028"]),
          ("Dec 2027", "Review", ["Set 2028 pricing with a full year of renewal data"])]
xw = 12.33 / 5
hline(s, 0.5, 2.35, 12.33, NAVY, 2)
for i, (when, what, items) in enumerate(phases):
    x = 0.5 + i * xw
    is_gate = what.startswith("Checkpoint")
    dot = rect(s, x + 0.05, 2.22, 0.26, 0.26, ORANGE if is_gate else NAVY, shape=MSO_SHAPE.OVAL)
    text(s, x, 1.65, xw - 0.1, 0.45, [{"t": when, "size": 13, "bold": True, "color": NAVY}])
    rect(s, x, 2.7, xw - 0.12, 2.75, PALEORANGE if is_gate else PALE)
    text(s, x + 0.1, 2.8, xw - 0.32, 2.6,
         [{"t": what, "size": 13, "bold": True, "color": ORANGE if is_gate else NAVY, "after": 8}] +
         [{"t": t, "size": 11.5, "bullet": 0, "after": 6} for t in items])

callout(s, 0.5, 5.65, 12.33, 1.2, "Tracked monthly from January (one dashboard for the leadership team)",
        ["Mid-market churn: repriced vs. not-yet-repriced renewals  ·  SMB test vs. control churn and price-citing exits  ·  "
         "Promo-cohort activation and churn  ·  Inkwell-contested SMB win rate  ·  NRR by segment"], size=12)

# =================================================================== 15. Risks
s = new_slide("The main risks are measurable early, and each has a pre-agreed response",
              kicker="Risks and what would change the recommendation", source=SRC + " — section 11 and our analysis.")
data = [
    ["Risk", "Why it matters", "Early signal", "Response"],
    ["Existing mid-market reacts worse at renewal than new sign-ups did",
     "The 2024 test covered new sign-ups only (uncertainty #3)", "Monthly churn of repriced renewals",
     "Pause at >1.2%/mo; break-even ~1.6%"],
    ["Trailing NRR does not repeat", "Each 1 pt of overall NRR ≈ $0.9M of ARR", "Quarterly NRR by segment",
     "Pull forward the SMB decision; push new-logo plan"],
    ["Promo cohort churns regardless (uncertainty #2)", "Up to $4.4M ARR; drags SMB NRR",
     "Activation rate and churn of the cohort", "Stop spend on it; focus activation on new cohorts"],
    ["Core SMB more price-sensitive since Inkwell (uncertainty #1)", "Decides whether SMB can ever be repriced",
     "Test vs. control churn; contested win rate", "Hold SMB price; review packaging vs. $9 Starter"],
    ["Inkwell moves upmarket", "Mid-market 51–200 seats may be exposed", "Inkwell in deals above 50 seats",
     "Segment mid-market increases by seat band"],
    ["Enterprise negotiates below caps", "$0.8M is a ceiling, not a forecast", "Renewal outcomes vs. 7%/10% asks",
     "Trade price for term length or scope"],
]
table(s, 0.5, 1.7, 12.33, 5.1, data, col_w=[3.3, 3.2, 2.8, 3.03], size=11,
      row_h=[0.45, 0.8, 0.7, 0.75, 0.8, 0.7, 0.7], align_center_from=99)

# =================================================================== 16. Decisions
s = new_slide("Six decisions for the December leadership meeting",
              kicker="Decisions requested", source=SRC + ".")
decisions = [
    ("1", "Mid-market: +10% list price at renewal from January 2027", "+$3.5M run-rate"),
    ("2", "Enterprise: raise at renewal to contract terms — 7% where capped, 10% otherwise", "+$0.8M (ceiling)"),
    ("3", "SMB: hold list prices in H1 2027; exclude the promo cohort from any 2027 rise; approve the +8% renewal test",
     "Avoids ~320–640 extra losses"),
    ("4", "Fund the SMB activation programme — without booking churn savings in the plan", "Upside, not plan"),
    ("5", "Finance: define the board churn metric and provide a 2027 new-logo ARR forecast", "Closes the $0.7M gap"),
    ("6", "Confirm the April (mid-market) and July (SMB) checkpoints and their thresholds", "Up to +$0.85M"),
]
yy = 1.75
for n, d, v in decisions:
    rect(s, 0.5, yy, 0.6, 0.68, NAVY)
    text(s, 0.5, yy, 0.6, 0.68, [{"t": n, "size": 20, "bold": True, "color": WHITE, "align": PP_ALIGN.CENTER}],
         anchor=MSO_ANCHOR.MIDDLE)
    rect(s, 1.15, yy, 11.68, 0.68, PALE)
    text(s, 1.3, yy, 8.6, 0.68, [{"t": d, "size": 13.5}], anchor=MSO_ANCHOR.MIDDLE)
    text(s, 9.9, yy, 2.8, 0.68, [{"t": v, "size": 13, "bold": True, "color": BLUE, "align": PP_ALIGN.RIGHT}],
         anchor=MSO_ANCHOR.MIDDLE)
    yy += 0.8

# =================================================================== A1. Assumptions & calculations
s = new_slide("Appendix A — How the numbers were built",
              kicker="Appendix", source=SRC + ". All figures are derived from the pack; no external data was used.")
data = [
    ["Figure", "Calculation", "Key assumption"],
    ["CFO capturable $7.6M", "SMB 21.0×12% + MM 41.0×85%×12% + Ent 24.0×40%×(60%×7% + 40%×12%)",
     "Price caps spread evenly across renewing and non-renewing enterprise ARR"],
    ["SMB churn response", "2023 +8%: +0.5 pt for 6 months, +0.1 pt after → +3.6 pts of customers in year one; "
                           "×1.5 for 12% = 5.4%; stress ×2 = 10.8%", "Response scales linearly with price; "
                                                                      "stress multiple is illustrative"],
    ["Promo-cohort churn ~4.9%", "(5,900×3.1% − 3,800×2.1%) ÷ 2,100", "Mid-2026 counts stand for H1 averages"],
    ["Activation explains ~0.8 of 2.8 pts", "Other SMB: 72%×a + 28%×3a = 2.1% → a ≈ 1.35%; promo mix 41%/59% → ~2.9% "
                                            "predicted vs. ~4.9% implied", "The “3×” ratio holds for all SMB; directional only"],
    ["Recommended $4.3M", "MM 41.0×85%×10% = 3.49; Ent 24.0×40%×(60%×7% + 40%×10%) = 0.79",
     "10% = the only tested level; enterprise figures are a ceiling"],
    ["Checkpoint upside ~$0.85M", "MM: 50% of renewing ARR in H2 × 2 pts = 0.35; SMB: 50% × 21.0 × 8% = 0.84 "
                                  "less 2023-style churn (3 pts × $11.3M = 0.34) = ~0.50", "Renewals spread evenly over the year"],
    ["ARR bridge", "Segment ARR × (trailing NRR − 1) = +$8.0M; plus price effects", "Trailing NRR repeats in 2027; "
                                                                                  "price rises add to it"],
    ["Break-even", "Lost share = p ÷ (1 + p): 9.1% at +10%, 10.7% at +12%", "Departures are a share of repriced ARR"],
]
table(s, 0.5, 1.65, 12.33, 5.2, data, col_w=[2.7, 5.8, 3.83], size=10.5,
      row_h=[0.38, 0.6, 0.62, 0.42, 0.62, 0.6, 0.62, 0.45, 0.45], align_center_from=99)

# =================================================================== A2. Gaps & choices
s = new_slide("Appendix B — Data gaps and judgement calls made in preparing this deck",
              kicker="Appendix", source=SRC + ".")
text(s, 0.5, 1.7, 6.0, 0.4, [{"t": "Not in the pack — would sharpen the decision", "size": 14, "bold": True,
                              "color": NAVY}])
text(s, 0.5, 2.15, 6.0, 4.7, [{"t": t, "size": 12, "bullet": 0, "after": 7} for t in [
    "2027 new-logo ARR forecast (the bridge treats it as a residual).",
    "Renewal dates by month, and notice periods for mid-market and enterprise contracts.",
    "Mid-market seat-size mix, especially the 51–200 seat band where Inkwell could appear.",
    "SMB split between monthly and annual plans.",
    "Exit-survey response rates: the survey mix implies promo churners are ~47% of respondents vs. ~56% of "
    "estimated churners — consistent, but not exact.",
    "Definition of the board dashboard churn measure (1.4% → 2.3%).",
    "Evidence behind the claim that onboarding will halve SMB churn in two quarters.",
]])
text(s, 6.9, 1.7, 5.9, 0.4, [{"t": "Judgement calls (no one was available to ask)", "size": 14, "bold": True,
                              "color": NAVY}])
text(s, 6.9, 2.15, 5.9, 4.7, [{"t": t, "size": 12, "bullet": 0, "after": 7} for t in [
    "ARR effects shown as end-2027 run-rate (the growth goal is an ARR goal); in-year revenue is lower because "
    "renewals fall through the year.",
    "Mid-market set at +10% — the tested level — rather than the CFO’s 12%, with a step-up gate.",
    "Uncapped enterprise contracts set at 10% for consistency with mid-market.",
    "SMB test set at +8% so results compare with the 2023 increase.",
    "Board dashboard churn figure set aside because it cannot be reconciled with Table 1.",
    "Checkpoint thresholds proposed by us, set well inside break-even.",
]])

prs.save(OUT)
print("saved", OUT, "slides:", len(prs.slides))
