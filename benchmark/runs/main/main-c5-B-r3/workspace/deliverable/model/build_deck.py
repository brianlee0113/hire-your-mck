"""Builds deliverable/Parcelbird_Now_board_deck.pptx from parcelbird_model.py.
Run from this folder: PYTHONPATH=. python3 build_deck.py"""
import math, os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_TICK_LABEL_POSITION
from pptx.oxml.ns import qn
from lxml import etree
import parcelbird_model as M

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Parcelbird_Now_board_deck.pptx")

# ---------- palette (dataviz reference palette, light mode) ----------
def C(h): return RGBColor.from_string(h.lstrip("#"))
INK, INK2, MUTED = C("0b0b0b"), C("52514e"), C("898781")
GRID, AXIS, SURF, PLANE = C("e1e0d9"), C("c3c2b7"), C("fcfcfb"), C("f4f3ef")
BLUE, ORANGE, AQUA, YELLOW = C("2a78d6"), C("eb6834"), C("1baf7a"), C("eda100")
NEG = C("e34948")          # diverging negative pole (red)
POS = C("2a78d6")          # diverging positive pole (blue)
TOTAL = C("52514e")
GOOD, WARN, CRIT = C("0ca30c"), C("fab219"), C("d03b3b")
WHITE = C("ffffff")
BLUE_T = C("eaf2fc")       # light tint for callouts
RED_T = C("fbe9e8")
FONT = "Arial"

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]
SW = 13.333

# ---------- helpers ----------
def tb(slide, x, y, w, h, paras, size=12, color=INK, bold=False, align=PP_ALIGN.LEFT,
       anchor=MSO_ANCHOR.TOP, fill=None, line=None, margin=0.04, spacing=None):
    """paras: str | list of items; item = str | dict(text|runs, size, bold, color, bullet, level, align, space_before)"""
    shp = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is not None:
        shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is not None:
        shp.line.color.rgb = line; shp.line.width = Pt(0.75)
    tf = shp.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(margin + (0.06 if fill is not None else 0))
    tf.margin_top = tf.margin_bottom = Inches(0.03 + (0.04 if fill is not None else 0))
    tf.vertical_anchor = anchor
    if isinstance(paras, str): paras = [paras]
    for i, p in enumerate(paras):
        if isinstance(p, str): p = dict(text=p)
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = p.get("align", align)
        if spacing: para.line_spacing = spacing
        sb = p.get("space_before", 3 if i else 0)
        para.space_before = Pt(sb)
        runs = p.get("runs") or [dict(text=p.get("text", ""))]
        for r in runs:
            run = para.add_run(); run.text = r["text"]
            f = run.font; f.name = FONT
            f.size = Pt(r.get("size", p.get("size", size)))
            f.bold = r.get("bold", p.get("bold", bold))
            f.italic = r.get("italic", False)
            f.color.rgb = r.get("color", p.get("color", color))
        if p.get("bullet"):
            lvl = p.get("level", 0)
            pPr = para._p.get_or_add_pPr()
            ind = 0.17 + 0.2 * lvl
            pPr.set("marL", str(int(Inches(ind)))); pPr.set("indent", str(int(-Inches(0.17))))
            for tag in ("a:buNone", "a:buChar", "a:buAutoNum"):
                for e in pPr.findall(qn(tag)): pPr.remove(e)
            buf = etree.SubElement(pPr, qn("a:buFont")); buf.set("typeface", "Arial")
            bu = etree.SubElement(pPr, qn("a:buChar")); bu.set("char", "–" if lvl else "•")
    return shp

def rect(slide, x, y, w, h, fill, line=None, shape=MSO_SHAPE.RECTANGLE):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid(); s.fill.fore_color.rgb = fill
    if line is None: s.line.fill.background()
    else: s.line.color.rgb = line; s.line.width = Pt(0.75)
    s.shadow.inherit = False
    return s

def hline(slide, x1, y1, x2, y2, color=AXIS, width=0.75):
    l = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    l.line.color.rgb = color; l.line.width = Pt(width)
    return l

page_no = [0]
def new_slide(title, section=None, source=None):
    s = prs.slides.add_slide(BLANK)
    page_no[0] += 1
    if section:
        tb(s, 0.5, 0.28, 9, 0.28, section.upper(), size=9, color=BLUE, bold=True)
    tb(s, 0.5, 0.52, 12.3, 0.95, title, size=20, bold=True, color=INK, anchor=MSO_ANCHOR.TOP, spacing=0.95)
    hline(s, 0.5, 1.5, SW - 0.5, 1.5, color=GRID, width=0.75)
    if source:
        tb(s, 0.5, 6.98, 11.3, 0.36, source, size=8, color=MUTED)
    tb(s, SW - 1.1, 7.02, 0.6, 0.3, str(page_no[0]), size=8, color=MUTED, align=PP_ALIGN.RIGHT)
    return s

def table(slide, x, y, w, h, data, col_w=None, size=10, header_fill=INK2, zebra=True,
          bold_first_col=False, fills=None, fonts=None, aligns=None, row_h=None):
    rows, cols = len(data), len(data[0])
    gt = slide.shapes.add_table(rows, cols, Inches(x), Inches(y), Inches(w), Inches(h))
    t = gt.table
    tblPr = t._tbl.tblPr
    for a in ("bandRow", "firstRow"): tblPr.set(a, "0")
    sid = tblPr.find(qn("a:tableStyleId"))
    if sid is not None: sid.text = "{5940675A-B579-460E-94D1-54222C63F5DA}"  # No style, table grid
    if col_w:
        for i, cw in enumerate(col_w): t.columns[i].width = Inches(cw)
    for r in range(rows):
        if row_h: t.rows[r].height = Inches(row_h if not isinstance(row_h, list) else row_h[r])
        for c in range(cols):
            cell = t.cell(r, c)
            val = data[r][c]
            cell.margin_left = cell.margin_right = Inches(0.07)
            cell.margin_top = cell.margin_bottom = Inches(0.03)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = cell.text_frame; tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = ""
            run = p.add_run(); run.text = str(val)
            f = run.font; f.name = FONT; f.size = Pt(size)
            if r == 0:
                f.bold = True; f.color.rgb = WHITE
                cell.fill.solid(); cell.fill.fore_color.rgb = header_fill
            else:
                f.color.rgb = INK
                f.bold = bold_first_col and c == 0
                cell.fill.solid()
                cell.fill.fore_color.rgb = PLANE if (zebra and r % 2 == 0) else WHITE
            if fills and (r, c) in fills:
                cell.fill.solid(); cell.fill.fore_color.rgb = fills[(r, c)]
            if fonts and (r, c) in fonts:
                for k, v in fonts[(r, c)].items(): setattr(f, k, v) if k != "color" else setattr(f.color, "rgb", v)
            p.alignment = PP_ALIGN.LEFT if c == 0 else PP_ALIGN.CENTER
            if aligns and c in aligns: p.alignment = aligns[c]
            # thin borders
            tcPr = cell._tc.get_or_add_tcPr()
            for i_e, edge in enumerate(("a:lnL", "a:lnR", "a:lnT", "a:lnB")):  # schema order: borders before fill
                ln = etree.Element(qn(edge)); ln.set("w", str(int(Pt(0.5))))
                sf = etree.SubElement(ln, qn("a:solidFill")); clr = etree.SubElement(sf, qn("a:srgbClr")); clr.set("val", "E1E0D9")
                tcPr.insert(i_e, ln)
    return t

def fmt_money(v, dp=2):
    return ("−" if v < 0 else "+") + f"${abs(v):.{dp}f}"

def bar_chart(slide, x, y, w, h, items, vmin, vmax, label_fmt=fmt_money, bar_frac=0.56, cat_size=10,
              val_size=11, zero_line=True, cat_h=0.55):
    """Shape-drawn bars from zero. items: (label, value, color, bold_label)."""
    plot_h = h - cat_h
    scale = plot_h / (vmax - vmin)
    y0 = y + vmax * scale
    n = len(items); slot = w / n; bw = slot * bar_frac
    for i, (lab, v, col, *rest) in enumerate(items):
        bx = x + i * slot + (slot - bw) / 2
        top = y0 - max(v, 0) * scale; hh = abs(v) * scale
        rect(slide, bx, top, bw, max(hh, 0.01), col)
        if v >= 0: tb(slide, bx - 0.3, top - 0.3, bw + 0.6, 0.28, label_fmt(v), size=val_size, bold=True, align=PP_ALIGN.CENTER)
        else: tb(slide, bx - 0.3, top + hh + 0.02, bw + 0.6, 0.28, label_fmt(v), size=val_size, bold=True, align=PP_ALIGN.CENTER)
        tb(slide, x + i * slot, y + plot_h + 0.06 + (0 if vmin >= 0 else 0), slot, cat_h, lab, size=cat_size, color=INK2,
           align=PP_ALIGN.CENTER, bold=bool(rest and rest[0]))
    if zero_line: hline(slide, x, y0, x + w, y0, color=AXIS, width=1)
    return y0, scale

def waterfall(slide, x, y, w, h, steps, vmin, vmax, cat_h=0.6, cat_size=9.5, val_size=10.5, bar_frac=0.62):
    """steps: (label, value, kind) kind in {'delta','total'}; totals drawn from zero."""
    plot_h = h - cat_h
    scale = plot_h / (vmax - vmin)
    yv = lambda v: y + (vmax - v) * scale
    n = len(steps); slot = w / n; bw = slot * bar_frac
    run = 0.0; prev_end = None
    for i, (lab, v, kind) in enumerate(steps):
        bx = x + i * slot + (slot - bw) / 2
        if kind == "total":
            a, b = 0.0, v; run = v; col = TOTAL
        else:
            a, b = run, run + v; run = b; col = POS if v >= 0 else NEG
        top, bot = yv(max(a, b)), yv(min(a, b))
        rect(slide, bx, top, bw, max(bot - top, 0.012), col)
        if prev_end is not None:
            hline(slide, prev_end[0], yv(prev_end[1]), bx, yv(prev_end[1]), color=AXIS, width=0.5)
        prev_end = (bx + bw, run)
        lab_v = fmt_money(v)
        if kind == "total" or v >= 0:
            ly = top - 0.27 if (kind != "total" or v >= 0) else bot + 0.02
        else:
            ly = bot + 0.02
        tb(slide, bx - 0.35, ly, bw + 0.7, 0.26, lab_v, size=val_size, bold=True, align=PP_ALIGN.CENTER)
        tb(slide, x + i * slot - 0.02, y + plot_h + 0.08, slot + 0.04, cat_h, lab, size=cat_size, color=INK2,
           align=PP_ALIGN.CENTER, bold=(kind == "total"))
    hline(slide, x, yv(0), x + w, yv(0), color=INK2, width=1)
    return yv

def line_chart(slide, x, y, w, h, cats, series, colors, y_min=None, y_max=None, y_title=None, major=None,
               legend=True, number_format='0', widths=None):
    cd = CategoryChartData(); cd.categories = cats
    for name, vals in series: cd.add_series(name, vals)
    gf = slide.shapes.add_chart(XL_CHART_TYPE.LINE, Inches(x), Inches(y), Inches(w), Inches(h), cd)
    ch = gf.chart
    ch.font.name = FONT; ch.font.size = Pt(10); ch.font.color.rgb = INK2
    ch.has_legend = legend
    if legend:
        ch.legend.position = XL_LEGEND_POSITION.TOP; ch.legend.include_in_layout = False
        ch.legend.font.size = Pt(10)
    va = ch.value_axis
    if y_min is not None: va.minimum_scale = y_min
    if y_max is not None: va.maximum_scale = y_max
    if major: va.major_unit = major
    va.has_major_gridlines = True
    va.major_gridlines.format.line.color.rgb = GRID; va.major_gridlines.format.line.width = Pt(0.5)
    va.format.line.fill.background()
    va.tick_labels.number_format = number_format; va.tick_labels.number_format_is_linked = False
    va.tick_labels.font.size = Pt(9); va.tick_labels.font.color.rgb = MUTED
    ca = ch.category_axis
    ca.format.line.color.rgb = AXIS
    ca.tick_labels.font.size = Pt(9); ca.tick_labels.font.color.rgb = MUTED
    ca.tick_label_position = XL_TICK_LABEL_POSITION.LOW
    ca.has_major_gridlines = False
    if y_title:
        va.has_title = True; va.axis_title.text_frame.text = y_title
        r = va.axis_title.text_frame.paragraphs[0].runs[0]; r.font.size = Pt(9); r.font.color.rgb = MUTED; r.font.bold = False
    plot = ch.plots[0]
    for i, s in enumerate(plot.series):
        s.smooth = False
        s.format.line.color.rgb = colors[i]
        s.format.line.width = Pt(widths[i] if widths else 2.25)
        s.marker.style = None
        from pptx.enum.chart import XL_MARKER_STYLE
        s.marker.style = XL_MARKER_STYLE.NONE
    return ch

def status_chip(slide, x, y, kind, w=1.25):
    col, txt, ink = {"fail": (CRIT, "×  Not met", WHITE), "part": (WARN, "½  Partly met", INK),
                     "pass": (GOOD, "✓  Met", WHITE)}[kind]
    s = rect(slide, x, y, w, 0.32, col, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    tf = s.text_frame; tf.margin_left = tf.margin_right = Inches(0.04)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = txt; r.font.size = Pt(10); r.font.bold = True; r.font.color.rgb = ink; r.font.name = FONT
    return s

def callout(slide, x, y, w, h, head, body, fill=BLUE_T, bar=BLUE, size=11):
    rect(slide, x, y, w, h, fill)
    rect(slide, x, y, 0.06, h, bar)
    paras = []
    if head: paras.append(dict(text=head, bold=True, size=size + 1))
    for b in body:
        if isinstance(b, dict): paras.append(b)
        else: paras.append(dict(text=b, size=size, bullet=True, space_before=4))
    tb(slide, x + 0.14, y + 0.08, w - 0.24, h - 0.14, paras, size=size)

SRC = "Source: Parcelbird briefing pack (synthetic benchmark data); team analysis. "

# ---------- precomputed numbers ----------
SC = {k: M.contribution(*v[:4], fixed=v[4]) for k, v in M.SCENARIOS.items()}
POP, MED, BEST, PLAN = (SC[k] for k in M.SCENARIOS)
sw_base = M.simulate(0.60, months=48)
sw_45 = M.simulate(0.45, months=48)
sw_30 = M.simulate(0.30, months=48)
sw_opex = M.simulate(0.60, opex_growth=0.10, months=48)
launch_inc = M.simulate(hires=0, extra=M.LAUNCH_INCREMENTAL, months=24)

# =====================================================================
# 1. Title
s = prs.slides.add_slide(BLANK); page_no[0] += 1
rect(s, 0, 0, SW, 7.5, C("0d366b"))
rect(s, 0.8, 2.2, 0.08, 2.3, BLUE)
tb(s, 1.05, 2.1, 11, 0.5, "PARCELBIRD  |  BOARD MEETING, JANUARY 2027", size=12, color=C("9ec5f4"), bold=True)
tb(s, 1.05, 2.6, 11.2, 1.3, "Should Parcelbird launch its own quick-commerce grocery delivery service in 2027?",
   size=32, bold=True, color=WHITE, spacing=0.95)
tb(s, 1.05, 3.95, 11, 0.9, "Recommendation: do not launch Parcelbird Now in 2027. Put the money into the software business "
   "and sell fast delivery to grocers instead.", size=16, color=C("cde2fb"))
tb(s, 1.05, 6.6, 11.5, 0.5, "Decision paper for the board (two founders, two investors). All figures are from the briefing pack, "
   "which contains synthetic benchmark data; calculations are shown on each slide and in the appendix.", size=10, color=C("86b6ef"))

# =====================================================================
# 2. Executive summary
s = new_slide("Executive summary: do not launch Parcelbird Now in 2027. Scale the software business, which reaches "
              "profitability within current cash, and sell fast delivery to grocers", section="Executive summary")
rect(s, 0.5, 1.68, 12.33, 0.62, C("0d366b"))
tb(s, 0.65, 1.7, 12.1, 0.58, [dict(runs=[dict(text="Answer: No. ", bold=True, color=C("9ec5f4")),
   dict(text="As an operator, Parcelbird would lose money on every order at any level of performance observed so far, and the plan "
        "would break the board's cash rules within a year. The software business has a funded path to profit and still "
        "captures the growth in quick commerce.", color=WHITE)])], size=12, anchor=MSO_ANCHOR.MIDDLE)
rows = [
 ("A", "The economics fail: the market grows but makes no profit, and a Parcelbird order would lose money",
  ["The market grew 41% a year to $5.1B (2022–25), but both incumbents lose money on each order; QuickBasket closed 4 of its 11 cities",
   "At the median of Parcelbird's 14 customer sites, an order loses $6.17 after site costs. The best composite still loses $1.76, and the pop-up lost $12.57",
   "The plan's +$2.02 needs every driver to beat the best site ever observed. At the standard 6% promotions it falls to +$0.22",
   "With $38 CAC and 22% of customers left at month 3, acquisition cost is never earned back at benchmark economics"]),
 ("B", "Parcelbird cannot afford to find out: every dark-store option breaks the 12-month runway floor",
  ["If the $9.5M plan runs on top of today's software burn, runway falls below 12 months in month 2 and cash runs out in month 15",
   "At benchmark economics, nine stores need about $37M in their first full year (operating loss, CAC, capex) against $12M of cash, and no new round is expected",
   "Even a one-store pilot (about $3.8M) keeps runway below 12 months from month 5 to month 18"]),
 ("C", "Scaling the software business is the better route into the same market",
  ["The pipeline holds $3.55M of ARR, 1.4× what 60% growth needs in 2027. The $0.8M/yr of hires pay back with about 11 contracts",
   "Base case: cash break-even in about month 26, cash never below $5.4M, runway never below 24 months. Holds at 45% growth",
   "Pipeline grocers want fast delivery from their own stores. Selling that capability gives Parcelbird the growth and leaves the operating risk with grocers"]),
]
y = 2.45
hts = [1.55, 1.25, 1.3]
for (tag, head, bul), hh in zip(rows, hts):
    rect(s, 0.5, y, 0.42, hh - 0.1, BLUE)
    tb(s, 0.5, y, 0.42, hh - 0.1, tag, size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    tb(s, 1.0, y, 3.55, hh - 0.1, head, size=12, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    tb(s, 4.65, y - 0.02, 8.2, hh - 0.06, [dict(text=b, bullet=True, space_before=2) for b in bul], size=10.5,
       anchor=MSO_ANCHOR.MIDDLE)
    hline(s, 1.0, y + hh - 0.05, SW - 0.5, y + hh - 0.05, color=GRID)
    y += hh
tb(s, 0.5, 6.56, 12.3, 0.45, [dict(runs=[dict(text="Decisions requested: ", bold=True),
   dict(text="(1) do not launch in 2027; (2) approve $0.8M/yr for 2 engineers and 2 sales hires, focused on a store-based fast-delivery module; "
             "(3) set objective triggers for reopening the question (slide 18).")])], size=10.5, color=INK)
tb(s, 0.5, 7.05, 11, 0.3, SRC, size=8, color=MUTED)

# =====================================================================
# 3. Hypothesis and scorecard
s = new_slide("We started from the founders' case for launching and listed five things that would have to be true. "
              "The evidence fails four of them and only partly supports the first", section="Approach: hypothesis-driven test",
              source=SRC + "Conditions 1–3 are tested in section A, condition 4 in section B and condition 5 in section C.")
tb(s, 0.5, 1.6, 12.3, 0.55, [dict(runs=[dict(text="Starting hypothesis (the founders' view): ", bold=True),
   dict(text="“Launch Parcelbird Now: a 15-minute dark-store service in Columbus, Indianapolis and Kansas City, reaching positive contribution per order by month 18.”")])],
   size=11.5, color=INK)
data = [["#", "What would have to be true", "What the evidence shows", "Verdict", "Section"],
        ["1", "The market is large, growing and leaves profit for a new entrant",
         "Growing 41%/yr, but Zipcart (−$1.90/order) and QuickBasket (−$3.40/order) both lose money; QuickBasket shut 4 of 11 cities", "", "A"],
        ["2", "A Parcelbird order is profitable at performance it can realistically achieve",
         "−$6.17 per order at the benchmark median, −$1.76 at the best composite. Positive only if all four plan inputs beat the best site", "", "A"],
        ["3", "Customers stay and repay their acquisition cost",
         "22% still ordering at month 3; $38 CAC never repaid at benchmark economics; pop-up demand was promotion-led (12% of AOV)", "", "A"],
        ["4", "It can be funded from $12.0M while keeping ≥12 months of runway",
         "Floor breached in month 2 (month 11 even if the $9.5M is all-in); cash runs out in month 15; no new round expected", "", "B"],
        ["5", "It is the best use of the cash available",
         "Software path reaches break-even in about month 26, with runway never below 24 months, and sells into the same q-commerce trend", "", "C"]]
t = table(s, 0.5, 2.2, 12.33, 4.4, data, col_w=[0.4, 3.6, 5.7, 1.6, 1.03], size=10.5, row_h=[0.4] + [0.8] * 5, aligns={1: PP_ALIGN.LEFT, 2: PP_ALIGN.LEFT})
for i, k in enumerate(["part", "fail", "fail", "fail", "fail"]):
    status_chip(s, 0.5 + 0.4 + 3.6 + 5.7 + 0.17, 2.2 + 0.4 + i * 0.8 + 0.24, k, w=1.26)
tb(s, 0.5, 6.62, 12.3, 0.35, [dict(runs=[dict(text="Revised answer: ", bold=True, color=CRIT),
   dict(text="do not launch in 2027. The hypothesis fails on economics (A) and affordability (B), and a better alternative exists (C).")])], size=11.5)

# =====================================================================
# 4. Market
s = new_slide("Quick commerce grows about 41% a year, yet its two incumbents lost $406M in 2025. The growth has not "
              "created a profit pool", section="A  |  Economics: market",
              source=SRC + "CAGR = (5.1 / 1.8)^(1/3) − 1 = 41.5%. Combined EBITDA −$406M on $1,410M revenue = −29% margin.")
tb(s, 0.5, 1.65, 6, 0.3, "US quick-commerce grocery GMV, $B", size=11, bold=True, color=INK2)
gmv = [(2022, 1.8), (2023, 2.6), (2024, 3.6), (2025, 5.1)]
bar_chart(s, 0.7, 2.3, 5.4, 3.9, [(str(yv), v, BLUE) for yv, v in gmv], 0, 5.6,
          label_fmt=lambda v: f"${v:.1f}B", bar_frac=0.5, cat_h=0.4)
for i, g in enumerate(["+44%", "+38%", "+42%"]):
    tb(s, 0.7 + (i + 1) * 1.35 - 0.4, 1.98, 0.8, 0.26, g, size=10, color=GOOD if False else C("006300"), bold=True, align=PP_ALIGN.CENTER)
tb(s, 0.7, 6.45, 5.4, 0.3, "Year-on-year growth shown between the bars", size=9, color=MUTED, align=PP_ALIGN.CENTER)
tb(s, 6.8, 1.65, 6, 0.3, "Incumbent operators, 2025", size=11, bold=True, color=INK2)
data = [["Operator", "Revenue", "EBITDA", "EBITDA margin", "Contribution / order"],
        ["Zipcart (national)", "$1,200M", "−$310M", "−26%", "−$1.90"],
        ["QuickBasket (regional)", "$210M", "−$96M", "−46%", "−$3.40"]]
table(s, 6.8, 2.05, 6.03, 1.2, data, col_w=[1.8, 0.95, 0.95, 1.08, 1.25], size=10.5, row_h=0.4,
      fonts={(1, 2): dict(color=NEG, bold=True), (2, 2): dict(color=NEG, bold=True), (1, 4): dict(color=NEG, bold=True), (2, 4): dict(color=NEG, bold=True)})
callout(s, 6.8, 3.5, 6.03, 2.75, "So what for Parcelbird",
        ["“Growing over 40% a year” holds: the 2022–25 CAGR is 41.5%, though 2024 grew only 38%",
         "“Nobody owns the Midwest” is more likely a warning than a gap. The regional player most like Parcelbird closed 36% of its cities in 2025",
         "Market growth does not test the decision. The test is whether one order can make money (next slides)",
         "Parcelbird's median order-level result (−$2.67, next slide) sits between the two incumbents, which supports using the benchmarks"],
        size=10.5)

# =====================================================================
# 5. Waterfall at median
_, ol, fx, site = MED
L = MED[0]
s = new_slide("At the median performance of Parcelbird's 14 customer sites, each order loses $2.67 before site costs "
              "and $6.17 after them", section="A  |  Economics: unit economics",
              source=SRC + "Benchmark median inputs: AOV $34, 27% goods margin, 6% promotions, 2.4 orders per rider-hour at $17.75/h, "
              "900 orders/site/day, $1.15M site fixed cost/yr (÷ 328,500 orders = $3.50/order).")
tb(s, 0.5, 1.65, 8.3, 0.3, "Contribution per order at benchmark-median inputs, $", size=11, bold=True, color=INK2)
steps = [("Goods margin\n27% × $34", L["Goods margin"], "delta"), ("Delivery fee\n(net)", L["Delivery fee"], "delta"),
         ("Promotions\n6% × $34", L["Promotions"], "delta"), ("Picking &\npacking", L["Picking & packing"], "delta"),
         ("Rider\n$17.75 ÷ 2.4", L["Rider cost"], "delta"), ("Payment &\npackaging", L["Payment & packaging"], "delta"),
         ("Order-level\ncontribution", ol, "total"), ("Site fixed cost\n$1.15M ÷ 328.5k", fx, "delta"),
         ("Site-level\ncontribution", site, "total")]
waterfall(s, 0.6, 2.15, 8.2, 4.55, steps, -7.2, 12.5, cat_h=0.62)
callout(s, 9.15, 1.75, 3.68, 4.95, "Reading the waterfall",
        ["Goods margin on a $34 basket is $9.18. Riders alone cost $7.40 of that, so the basket is too small to carry a 15-minute delivery",
         "Before any store cost, the variable costs already exceed the margin by $2.67",
         "Spreading the $1.15M dark-store cost over 900 orders a day adds another $3.50",
         "At this rate one store loses $2.0M a year (−$6.17 × 900 × 365)",
         "Decision metric: site-level contribution, because Parcelbird would own the store costs"], size=10.5)

# =====================================================================
# 6. Scenarios + inputs table
s = new_slide("Only the founders' plan makes money per order, and it needs all four drivers to beat the best "
              "site Parcelbird has observed at the same time", section="A  |  Economics: unit economics",
              source=SRC + "Best observed is a composite: the best AOV and the best density come from different sites, and no site achieved both. "
              "Benchmark ranges: 1.9–3.0 orders per rider-hour; 400–1,400 orders/site/day.")
tb(s, 0.5, 1.65, 5.6, 0.3, "Site-level contribution per order, $", size=11, bold=True, color=INK2)
items = [("Columbus pop-up\n(actual)", POP[3], NEG), ("Benchmark\nmedian", MED[3], NEG),
         ("Best observed\n(composite)", BEST[3], NEG), ("Founders'\nplan", PLAN[3], POS, True)]
bar_chart(s, 0.6, 2.2, 5.4, 4.0, items, -14, 3.5, cat_h=0.6, bar_frac=0.5)
tb(s, 0.6, 6.35, 5.4, 0.5, f"Order-level (before site cost): pop-up {fmt_money(POP[1])}, median {fmt_money(MED[1])}, "
   f"best {fmt_money(BEST[1])}, plan {fmt_money(PLAN[1])}", size=9.5, color=INK2, align=PP_ALIGN.CENTER)
tb(s, 6.5, 1.65, 6.3, 0.3, "Plan inputs compared with what has been observed", size=11, bold=True, color=INK2)
data = [["Driver", "Benchmark median", "Best observed", "Pop-up", "Founders' plan", "Plan vs best"],
        ["Average order value", "$34", "$42", "$31", "$45", "+7%"],
        ["Promotions, % of AOV", "6%", "6%", "12%", "2%", "⅓ of any site"],
        ["Orders per rider-hour", "2.4", "3.0 (top of range)", "2.1", "3.5", "+17%"],
        ["Orders per site per day", "900", "1,400 (top of range)", "280", "1,800", "+29%"],
        ["Site-level contribution", fmt_money(MED[3]), fmt_money(BEST[3]), fmt_money(POP[3]), fmt_money(PLAN[3]), ""]]
fills = {(r, 4): BLUE_T for r in range(1, 6)}
fills.update({(r, 5): RED_T for r in range(1, 5)})
table(s, 6.5, 2.05, 6.33, 2.75, data, col_w=[1.75, 0.95, 1.13, 0.7, 0.85, 0.95], size=10, row_h=[0.5] + [0.45] * 5, fills=fills,
      fonts={(5, c): dict(bold=True) for c in range(6)})
callout(s, 6.5, 5.0, 6.33, 1.85, "What would have to be true for the plan",
        ["The plan needs a basket 32% larger than the median, promotions at a third of what every site spends, riders 46% more productive and twice the density, all at once",
         "Even with every other plan input, standard 6% promotions cut the plan to +$0.22 per order"], size=10.5)

# =====================================================================
# 7. Bridge plan -> median
c0 = PLAN[3]
c1 = M.contribution(34, 3.5, 1800, 0.02)[3]
c2 = M.contribution(34, 3.5, 1800, 0.06)[3]
c3 = M.contribution(34, 2.4, 1800, 0.06)[3]
c4 = M.contribution(34, 2.4, 900, 0.06)[3]
s = new_slide("Four optimistic assumptions make up the $8.19 gap between the plan and benchmark reality, and "
              "basket size and rider productivity together account for $5.07 of it", section="A  |  Economics: unit economics",
              source=SRC + "Each step changes one input from plan to benchmark median, holding the previous changes. Step size depends on order "
              "(e.g. promotions are worth $1.80 at a $45 basket but $1.36 at $34).")
tb(s, 0.5, 1.65, 8, 0.3, "Site-level contribution per order: founders' plan to benchmark median, $", size=11, bold=True, color=INK2)
steps = [("Founders'\nplan", c0, "total"), ("AOV\n$45 → $34", c1 - c0, "delta"), ("Promotions\n2% → 6%", c2 - c1, "delta"),
         ("Rider output\n3.5 → 2.4/h", c3 - c2, "delta"), ("Density\n1,800 → 900/day", c4 - c3, "delta"),
         ("Benchmark\nmedian", c4, "total")]
waterfall(s, 0.6, 2.15, 7.9, 4.5, steps, -7, 3.2, cat_h=0.62, bar_frac=0.55)
callout(s, 8.9, 1.75, 3.93, 4.95, "Implications",
        ["Basket size is the largest gap (−$2.75). The pop-up's AOV was $31, so baskets are moving away from $45, not towards it",
         "Rider productivity (−$2.32) is the cost line most exposed to the minimum-pay rules under discussion in two of the three cities",
         "Density (−$1.75) depends on demand that the pop-up has not yet shown (280/day, about 410/day at exit)",
         "Closing the gap would need all four to improve together. No site has even combined the best AOV with the best density"], size=10.5)

# =====================================================================
# 8. Heatmap break-even
s = new_slide("Even at the best density any site has reached, no combination of observed basket size and "
              "rider productivity breaks even with standard promotions", section="A  |  Economics: break-even test",
              source=SRC + "Grid holds 1,400 orders/site/day (top of benchmark range) and 6% promotions. Break-even AOV solves "
              "AOV × (27% − 6%) = $2.41 + rider cost + site fixed cost per order.")
tb(s, 0.5, 1.65, 7.4, 0.3, "Site-level contribution per order at 1,400 orders/day and 6% promotions, $", size=11, bold=True, color=INK2)
aovs = [31, 34, 38, 42, 45]; rs = [2.1, 2.4, 3.0, 3.5]
grid = [["AOV  \\  orders per rider-hour"] + [f"{r}" + (" (pop-up)" if r == 2.1 else " (median)" if r == 2.4 else " (best)" if r == 3.0 else " (plan)") for r in rs]]
fills = {}; fonts = {}
reds = ["fbe9e8", "f6c9c7", "f0a3a1", "ea7b79", "e34948"]
for i, a in enumerate(aovs):
    lab = f"${a}" + (" (pop-up)" if a == 31 else " (median)" if a == 34 else " (best)" if a == 42 else " (plan)" if a == 45 else "")
    row = [lab]
    for j, r in enumerate(rs):
        v = M.contribution(a, r, 1400, 0.06)[3]
        row.append(fmt_money(v))
        k = min(4, int(abs(v) // 1.4))
        fills[(i + 1, j + 1)] = C(reds[k])
        fonts[(i + 1, j + 1)] = dict(color=WHITE if k >= 3 else INK, bold=True)
    grid.append(row)
table(s, 0.5, 2.05, 7.4, 3.3, grid, col_w=[1.9, 1.375, 1.375, 1.375, 1.375], size=11, row_h=[0.5] + [0.56] * 5,
      fills=fills, fonts=fonts, zebra=False)
tb(s, 0.5, 5.45, 7.4, 0.5, "Shading: darker red = larger loss per order. Every cell is negative. At 1,800/day (above any site) only the "
   "plan's own AOV and rider productivity turn positive: +$0.22.", size=9.5, color=INK2)
data = [["Break-even needed (site level)", "Value", "Observed max"],
        ["AOV at median density & riders", "$63", "$42"],
        ["AOV at best density & riders", "$50", "$42"],
        ["AOV at plan density & riders, 6% promos", "$44", "$42"],
        ["Orders per rider-hour at median AOV & density", "14.4", "3.0"]]
table(s, 8.3, 2.05, 4.53, 2.5, data, col_w=[2.73, 0.8, 1.0], size=10, row_h=0.5,
      fonts={(r, 1): dict(bold=True, color=NEG) for r in range(1, 5)})
callout(s, 8.3, 4.75, 4.53, 2.05, "So what",
        ["Break-even needs a basket well above anything seen, or density and productivity above the top of the benchmark range",
         "The economics depend on the format itself (small basket, paid rider, dedicated store). Better execution alone will not fix them"], size=10.5)

# =====================================================================
# 9. Pop-up vs median
s = new_slide("Parcelbird's own pop-up trailed its customers' median on all four drivers, so the evidence does not yet "
              "support “we run them better than anyone”", section="A  |  Economics: operating capability",
              source=SRC + "Pop-up: six weeks, one temporary site, autumn 2026, 11,800 orders. Exit run-rate is derived from 18%/week growth: "
              "week 1 ≈ 1,250 orders, week 6 ≈ 2,860 orders (≈ 410/day).")
panels = [("Average order value, $", [("Pop-up", 31), ("Median", 34), ("Plan", 45)], lambda v: f"${v:.0f}", 50, "Higher is better"),
          ("Promotions, % of AOV", [("Pop-up", 12), ("Median", 6), ("Plan", 2)], lambda v: f"{v:.0f}%", 14, "Lower is better"),
          ("Orders per rider-hour", [("Pop-up", 2.1), ("Median", 2.4), ("Plan", 3.5)], lambda v: f"{v:.1f}", 4, "Higher is better"),
          ("Orders per site per day", [("Pop-up", 280), ("Median", 900), ("Plan", 1800)], lambda v: f"{v:,.0f}", 2000, "Higher is better")]
cols = [BLUE, AXIS, INK2]
pw = 2.9
tb(s, 0.5, 1.62, 8, 0.3, [dict(runs=[dict(text="■ ", color=BLUE), dict(text="Columbus pop-up   "), dict(text="■ ", color=AXIS),
   dict(text="Benchmark median (14 customer sites)   "), dict(text="■ ", color=INK2), dict(text="Founders' plan")])], size=10, color=INK2)
for i, (ttl, vals, f, vmax, note) in enumerate(panels):
    x0 = 0.5 + i * (pw + 0.24)
    tb(s, x0, 1.95, pw, 0.3, ttl, size=11, bold=True)
    tb(s, x0, 2.22, pw, 0.25, note, size=9, color=MUTED)
    bar_chart(s, x0 + 0.1, 2.85, pw - 0.2, 2.35, [(l, v, cols[k]) for k, (l, v) in enumerate(vals)], 0, vmax,
              label_fmt=f, bar_frac=0.55, cat_h=0.35, val_size=11, cat_size=9.5)
callout(s, 0.5, 5.4, 6.05, 1.5, "What the pop-up shows",
        ["Order-level loss of $6.21 and site-level loss of $12.57 per order; about $0.15M lost over six weeks",
         "The 12% promotions and first-order credits bought much of the 18%/week order growth"], size=10.5)
callout(s, 6.78, 5.4, 6.05, 1.5, "Fair caveats", ["Six weeks at a temporary site is an early read, and volume was still rising (about 410/day at exit)",
         "Still, exit volume was below the 900/day median, and the plan assumes 1,800/day"],
        fill=PLANE, bar=MUTED, size=10.5)

# =====================================================================
# 10. Zipcart
z_base = MED[3]
z_fee = 3.99
z_promo = 34 * 0.05
z_vol = M.contribution(34, 2.4, 900 * 0.86, 0.01, fee=1.99 + 3.99)[3] - M.contribution(34, 2.4, 900, 0.01, fee=1.99 + 3.99)[3]
z_end = M.contribution(34, 2.4, 900 * 0.86, 0.01, fee=1.99 + 3.99)[3]
s = new_slide("Zipcart's one profitable city shows what break-even costs: a $3.99 fee and almost no promotions, which cost "
              "14% of volume. The same moves would still leave Parcelbird at −$1.05", section="A  |  Economics: the founders' proof point",
              source=SRC + "Applying Zipcart's levers to Parcelbird's median assumes the fee does not lower AOV and volume falls 14%, spreading "
              "the $1.15M site cost over 774 orders/day ($4.07/order).")
tb(s, 0.5, 1.65, 4.6, 0.3, "What happened in Zipcart's densest city, Q4 2025", size=11, bold=True, color=INK2)
data = [["", "Zipcart, densest city"], ["Contribution per order after changes", "+$0.40"],
        ["New service fee on every order", "+$3.99"], ["Promotions", "cut to 1% of order value"],
        ["Order volume afterwards", "−14%"], ["Implied contribution without the new fee (if fully retained)", "≈ −$3.59"],
        ["Zipcart national contribution per order", "−$1.90"]]
table(s, 0.5, 2.05, 4.6, 3.3, data, col_w=[2.9, 1.7], size=10.5, row_h=0.47,
      fonts={(1, 1): dict(bold=True), (4, 1): dict(bold=True, color=NEG), (5, 1): dict(bold=True, color=NEG)})
tb(s, 0.5, 5.45, 4.6, 1.3, [dict(text="The founders read this as “it can be done”. The shareholder letter says it was done by "
   "charging customers more and losing customers, and only in Zipcart's densest city. Nationally it still loses $1.90 per order.", size=10.5)])
tb(s, 5.5, 1.65, 7.3, 0.3, "Zipcart's levers applied to Parcelbird's benchmark median, site-level $ per order", size=11, bold=True, color=INK2)
steps = [("Benchmark\nmedian", z_base, "total"), ("+$3.99\nservice fee", z_fee, "delta"), ("Promotions\n6% → 1%", z_promo, "delta"),
         ("Volume −14%\n(fixed cost/order)", z_vol, "delta"), ("With Zipcart's\nlevers", z_end, "total")]
waterfall(s, 5.6, 2.15, 7.2, 3.9, steps, -7, 2.0, cat_h=0.62, bar_frac=0.55)
callout(s, 5.5, 6.15, 7.33, 0.75, None, [dict(text="Even if Parcelbird copies Zipcart's moves, its stores stay loss-making. Order-level contribution "
        "would turn positive (+$3.02), but the dark-store fixed cost would not be covered.", size=10.5)], size=10.5)

# =====================================================================
# 11. Customers
s = new_slide("Pop-up demand was largely bought: 22% of customers still ordered at month 3, and the $38 acquisition cost is "
              "never repaid at benchmark economics", section="A  |  Economics: customers",
              source=SRC + "CAC to fill a site = orders/day × 30 ÷ 3.1 orders/month ÷ 22% month-3 retention × $38. Assumes survivors stay "
              "and no organic acquisition (both generous). Payback ignores orders in months 1–2.")
tiles = [("44%", "of surveyed 25–39-year-olds said they would use it at least weekly (stated intent)"),
         ("22%", "of pop-up customers still ordering in month 3 (revealed behaviour)"),
         ("$38", "customer acquisition cost (paid social and first-order credits)"),
         ("12%", "of AOV spent on promotions in the pop-up, twice the benchmark")]
for i, (big, small) in enumerate(tiles):
    x0 = 0.5 + i * 3.13
    rect(s, x0, 1.7, 2.95, 1.35, PLANE)
    tb(s, x0 + 0.15, 1.74, 2.7, 0.6, big, size=28, bold=True, color=BLUE if i != 1 else NEG)
    tb(s, x0 + 0.15, 2.36, 2.7, 0.68, small, size=10, color=INK2)
tb(s, 0.5, 3.25, 6.0, 0.3, "Months to repay $38 CAC per acquired customer", size=11, bold=True, color=INK2)
data = [["Scenario", "Order-level / order", "Monthly per acquired customer", "Payback"],
        ["Benchmark median", fmt_money(MED[1]), fmt_money(MED[1] * 0.22 * 3.1), "Never"],
        ["Best observed", fmt_money(BEST[1]), fmt_money(BEST[1] * 0.22 * 3.1), "≈ 113 months"],
        ["Founders' plan", fmt_money(PLAN[1]), fmt_money(PLAN[1] * 0.22 * 3.1), "≈ 15 months"]]
table(s, 0.5, 3.6, 6.0, 1.8, data, col_w=[1.6, 1.3, 1.85, 1.25], size=10.5, row_h=0.45,
      fonts={(1, 3): dict(bold=True, color=NEG), (2, 3): dict(bold=True, color=NEG), (3, 3): dict(bold=True)})
tb(s, 0.5, 5.45, 6.0, 0.6, "Monthly per acquired customer = 22% × 3.1 orders × order-level contribution. At site level the plan's payback "
   "stretches to about 28 months.", size=9.5, color=INK2)
tb(s, 6.85, 3.25, 6.0, 0.3, "Acquisition spend needed to fill nine stores, $M", size=11, bold=True, color=INK2)
items = [("Benchmark\n900/day", 13.5, ORANGE), ("Best observed\n1,400/day", 21.1, ORANGE), ("Founders' plan\n1,800/day", 27.1, ORANGE),
         ("Total plan\nbudget", 9.5, AXIS, True)]
bar_chart(s, 7.0, 3.85, 5.8, 2.55, items, 0, 30, label_fmt=lambda v: f"${v:.1f}M", bar_frac=0.5, cat_h=0.55)
tb(s, 6.85, 6.45, 6.0, 0.5, "At plan density each store needs about 79,000 acquired customers (≈ $3.0M of CAC). The $9.5M plan covers "
   "capex, marketing and losses together.", size=9.5, color=INK2)

# =====================================================================
# 12. Runway
cats = [str(t) for t in range(0, 25)]
def capr(v): return max(0, min(36, v))
sw_r = [None] + [capr(r["runway"]) for r in sw_base[:24]]
sw_r[0] = 30
li_r = [30] + [capr(r["runway"]) if r["cash"] > 0 else 0 for r in launch_inc[:24]]
burnB = 9.5 / 18
ai_r = [12 / 0.4] + [capr((12 - burnB * t) / burnB) if t <= 18 else None for t in range(1, 25)]
floor = [12] * 25
s = new_slide("The $9.5M plan breaks the 12-month runway floor within its first year under either reading of the "
              "budget. If it adds to today's burn, cash runs out in month 15", section="B  |  Affordability: runway",
              source=SRC + "Runway = cash ÷ that month's net burn, capped at 36 on the chart. Start: $12.0M, January 2027. $9.5M is spread evenly over 18 months. "
              "Software path: 60% ARR growth, 81% GM, implied opex $8.1M/yr plus $0.8M hires.")
ch = line_chart(s, 0.5, 1.7, 8.3, 5.2, cats, [("Scale software (recommended)", sw_r), ("Launch: $9.5M on top of software burn", li_r),
                ("Launch: $9.5M treated as all-in", ai_r), ("12-month runway floor", floor)],
                [BLUE, ORANGE, AQUA, INK2], y_min=0, y_max=36, major=6, y_title="Months of runway", widths=[2.5, 2.5, 2.5, 1.25])
tb(s, 3.9, 6.62, 2, 0.28, "Months from January 2027", size=9, color=MUTED, align=PP_ALIGN.CENTER)
data = [["Path", "Floor breached", "Cash at month 18"],
        ["Scale software", "Never (min 24 mo.)", f"${sw_base[17]['cash']:.1f}M"],
        ["Launch, $9.5M on top", "Month 2", "−$2.3M (out in month 15)"],
        ["Launch, $9.5M all-in", "Month 11", "$2.5M"]]
table(s, 9.1, 1.75, 3.73, 1.9, data, col_w=[1.35, 1.15, 1.23], size=9.5, row_h=[0.4, 0.5, 0.5, 0.5],
      fonts={(2, 1): dict(bold=True, color=NEG), (3, 1): dict(bold=True, color=NEG), (1, 1): dict(bold=True)})
callout(s, 9.1, 3.85, 3.73, 3.0, "Why both readings fail",
        ["The pack does not say whether the $9.5M includes the software burn. We assume it does not (base case) and test the generous reading too",
         "Without the launch, the software business already uses about $6.6M of cash before break-even",
         "The plan is costed on the founders' inputs; at benchmark inputs the loss is larger (next slide)"], size=10)

# =====================================================================
# 13. Downside: benchmark economics + pilot
s = new_slide("At benchmark economics the nine stores would need about $37M in their first full year. Even a one-store pilot "
              "keeps runway below the floor for over a year", section="B  |  Affordability: downside and smaller bets",
              source=SRC + "Operating loss = −$6.17 × 900 orders × 365 days × 9 stores. CAC = $1.50M per store × 9. Pilot: $0.6M capex, $1.15M fixed, "
              "average 600 orders/day at −$2.67 order-level, $1.5M CAC to reach 900/day.")
tb(s, 0.5, 1.65, 6.2, 0.3, "Cash needed vs. available, $M", size=11, bold=True, color=INK2)
# stacked bar via shapes
x0, ybase, sc = 1.0, 6.2, 4.2 / 40
def stack(xc, parts, lab):
    yb = ybase
    for v, col, name in parts:
        hgt = v * sc; rect(s, xc, yb - hgt, 1.3, hgt - 0.02, col)
        if hgt > 0.3: tb(s, xc, yb - hgt, 1.3, hgt, f"{name}\n${v:.1f}M", size=9 if hgt < 0.6 else 9.5, margin=0, color=WHITE if col != AXIS else INK,
                         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, bold=True)
        yb -= hgt
    tot = sum(p[0] for p in parts)
    tb(s, xc - 0.3, yb - 0.3, 1.9, 0.28, f"${tot:.1f}M", size=11.5, bold=True, align=PP_ALIGN.CENTER)
    tb(s, xc - 0.3, ybase + 0.05, 1.9, 0.5, lab, size=9.5, color=INK2, align=PP_ALIGN.CENTER)
stack(0.8, [(12.0, BLUE, "Cash")], "Cash in the bank")
stack(2.6, [(5.4, INK2, "Capex"), (4.1, MUTED, "Marketing & losses")], "Founders' plan\n(to month 18)")
stack(4.4, [(5.4, INK2, "Capex"), (13.5, ORANGE, "CAC"), (18.2, NEG, "Operating loss")], "Benchmark economics\n(first full year)")
hline(s, 0.6, ybase, 6.0, ybase, color=AXIS, width=1)
tb(s, 0.5, 6.62, 6.2, 0.35, "Founders' plan split: $5.4M capex stated; marketing and losses are the $4.1M remainder.", size=9, color=MUTED)
tb(s, 7.1, 1.65, 5.7, 0.3, "Smaller operator bets break the floor or teach nothing new", size=11, bold=True, color=INK2)
data = [["Option", "Cash cost", "Runway floor", "What it would teach"],
        ["One permanent dark store, 12 months", "≈ $3.8M", "Below 12 mo. from month 5 to 18 (low 6.3)",
         "Little new: 14 customer sites and the pop-up already show the economics"],
        ["Second pop-up", "≈ $0.15M per 6 weeks", "Within floor", "Repeats a test already run, still at a loss"]]
table(s, 7.1, 2.05, 5.73, 2.0, data, col_w=[1.55, 1.0, 1.5, 1.68], size=9.5, row_h=[0.4, 0.95, 0.65],
      fonts={(1, 2): dict(bold=True, color=NEG)})
callout(s, 7.1, 4.3, 5.73, 2.6, "Other risks that make it worse",
        ["Rider minimum-pay rules (two of three cities): each +$1/hour costs $0.42 per order at 2.4 orders/hour, about $1.2M a year across nine stores",
         "No new funding round is expected for a delivery operator, so any shortfall has to come out of the software business",
         "Operating would compete with grocers who are customers or prospects, which puts the $96k-a-year contracts at risk"], size=10)

# =====================================================================
# 14. Software pipeline
s = new_slide("The software business already has a funded path to growth: its pipeline is worth 1.4× the ARR that 60% "
              "growth needs in 2027, and the proposed hires pay back with about 11 contracts", section="C  |  Alternative: software",
              source=SRC + "Pipeline ARR = grocers × $96k ACV. 2027 need = $4.1M × 60%. Hire payback = $0.8M ÷ ($96k × 81% gross margin) = 10.3 contracts per year. "
              "Assumes no churn and no expansion revenue.")
tb(s, 0.5, 1.65, 6.4, 0.3, "Software ARR available vs. needed in 2027, $M", size=11, bold=True, color=INK2)
items = [("Late-stage\npipeline (9)", 0.864, BLUE), ("Total pipeline\n(37 grocers)", 3.552, BLUE),
         ("New ARR for 60%\ngrowth in 2027", 2.46, AXIS, True), ("New ARR for 45%\ngrowth", 1.845, AXIS)]
bar_chart(s, 0.6, 2.25, 6.2, 3.95, items, 0, 4.0, label_fmt=lambda v: f"${v:.2f}M", bar_frac=0.5, cat_h=0.6)
tb(s, 0.6, 6.4, 6.2, 0.5, "60% growth needs about 26 new contracts in 2027. The 9 late-stage deals cover a third of that, so 17 must come "
   "from the 28 earlier-stage grocers or new leads.", size=9.5, color=INK2)
data = [["Metric", "Software business", "Parcelbird Now (median)"],
        ["Gross margin", "81%", "27% on goods; order loses money"],
        ["Unit of growth", "$96k contract, ≈ $78k gross profit/yr", "Order at −$6.17"],
        ["Capital per unit", "Hiring; no capex", "$0.6M capex + $1.5M CAC per store"],
        ["Who bears operating risk", "The grocer", "Parcelbird"]]
table(s, 7.2, 2.05, 5.63, 2.4, data, col_w=[1.45, 2.09, 2.09], size=10, row_h=0.48, bold_first_col=True)
callout(s, 7.2, 4.65, 5.63, 2.25, "Captures q-commerce growth without the operator's losses",
        ["Several pipeline grocers want fast delivery from their existing stores. A store-based module fits Parcelbird's picking and rider-dispatch software",
         "Store-based delivery uses stores the grocer already pays for, avoiding the $3.50/order dark-store cost (not quantified in the pack)",
         "Parcelbird keeps learning from more sites without putting its own capital at risk"], size=10)

# =====================================================================
# 15. Software cash path
cats = [str(t) for t in range(0, 43)]
ser = [("60% growth (base)", [12.0] + [r["cash"] for r in sw_base[:42]]), ("45% growth", [12.0] + [r["cash"] for r in sw_45[:42]]),
       ("30% growth (stress)", [12.0] + [r["cash"] for r in sw_30[:42]])]
s = new_slide("Scaling software reaches cash break-even in about month 26 and stays above the runway floor at 45% "
              "growth. Only a fall to about 30% would need cost action", section="C  |  Alternative: software cash path",
              source=SRC + "Implied opex = $4.1M × 81% + $4.8M burn = $8.1M/yr, held flat in real terms, plus $0.8M hires. Revenue = ARR ÷ 12, compounding monthly. "
              "Starts at $12.0M in January 2027 (two months of burn before then would lower every path by about $0.8M).")
line_chart(s, 0.5, 1.7, 7.9, 5.2, cats, ser, [BLUE, ORANGE, AQUA], y_min=0, y_max=12, major=2, y_title="Cash balance, $M",
           number_format='"$"0"M"')
tb(s, 3.6, 6.62, 2.2, 0.28, "Months from January 2027", size=9, color=MUTED, align=PP_ALIGN.CENTER)
def sm(rows):
    S = M.summary(rows); return S
rows_t = [("60% growth (base)", sw_base), ("45% growth", sw_45), ("60%, opex +10%/yr", sw_opex), ("30% growth (stress)", M.simulate(0.30, months=60))]
data = [["Scenario", "Break-even", "Lowest cash", "Floor"]]
for name, rr in rows_t:
    S = M.summary(rr)
    data.append([name, f"Month {S['breakeven_month']}" if S["breakeven_month"] else "—",
                 f"${S['min_cash']:.1f}M" if S["min_cash"] > 0 else "Runs out",
                 "Held" if not S["floor_breach_month"] else f"Breached m{S['floor_breach_month']}"])
table(s, 8.7, 1.75, 4.13, 2.4, data, col_w=[1.55, 0.9, 0.85, 0.83], size=9.5, row_h=0.48,
      fonts={(4, 3): dict(bold=True, color=NEG), (4, 2): dict(bold=True, color=NEG)})
callout(s, 8.7, 4.35, 4.13, 2.55, "Reading the stress case",
        ["At 30% growth, runway falls below 12 months around month 23 and cash runs out near month 46",
         "The board can see this early: if ARR growth runs below about 45% by mid-2027, cut opex to hold the floor",
         "Even in the stress case Parcelbird keeps 23 months to act, compared with 2 months in the launch case"], size=10)

# =====================================================================
# 16. Options comparison
s = new_slide("Of the four options, only scaling software with a store-based delivery module meets both board constraints "
              "and still captures quick-commerce growth", section="Options and trade-offs",
              source=SRC + "Options are mutually exclusive levels of operating exposure, from full operator to none. A hybrid (license software and run stores) "
              "is covered by A/B, because the store losses are the same.")
hdr = ["Criterion", "A. Launch as planned\n(9 dark stores, 3 cities)", "B. Single-store pilot\n(Columbus, 12 months)",
       "C. Scale software + store-\nbased delivery module", "D. Status quo\n(no hires, no launch)"]
data = [hdr,
        ["Path to profit within current cash", "No: −$6.17/order at median; +$2.02 only on plan inputs", "No: about −$3.8M; no path to profit at one store",
         "Yes: break-even in about month 26 (base)", "Likely, but slower if the pipeline is not converted"],
        ["Keeps ≥12 months of runway", "No: breached in month 2 (month 11 if all-in)", "No: below floor from month 5 to 18", "Yes: min 24 months (base), 20 at 45% growth", "Yes"],
        ["Exposure to q-commerce growth", "Direct, but at a loss on every order", "Small", "Indirect: grocers' fast-delivery demand", "Limited to current customers"],
        ["Downside if wrong", "Company-ending: cash out in month 15", "Uses about a third of cash for little new learning",
         "Slower growth; cut opex if growth is under 45%", "Pipeline left to competitors"],
        ["Reversibility", "Low: leases, capex, brand", "Medium", "High: can still operate later", "High"],
        ["Overall", "Reject", "Reject", "Recommend", "Fallback"]]
fills = {}; fonts = {}
for r in range(1, 6):
    fills[(r, 1)] = RED_T; fills[(r, 2)] = RED_T if r in (1, 2) else WHITE; fills[(r, 3)] = BLUE_T
for c, (txt, col) in enumerate([("Reject", CRIT), ("Reject", CRIT), ("Recommend", GOOD), ("Fallback", WARN)], start=1):
    fills[(6, c)] = col; fonts[(6, c)] = dict(bold=True, color=WHITE if col != WARN else INK)
table(s, 0.5, 1.7, 12.33, 5.15, data, col_w=[2.13, 2.6, 2.5, 2.6, 2.5], size=10, row_h=[0.62, 0.8, 0.75, 0.7, 0.8, 0.6, 0.42],
      fills=fills, fonts=fonts, bold_first_col=True, zebra=False, aligns={c: PP_ALIGN.LEFT for c in range(1, 5)})

# =====================================================================
# 17. Risks & assumptions
s = new_slide("The recommendation rests on a few explicit assumptions. The one that matters most is software growth "
              "holding above about 45%", section="Key assumptions, risks and uncertainties",
              source=SRC + "Sensitivity figures come from the calculation model in deliverable/model/parcelbird_model.py.")
data = [["Assumption / uncertainty", "Our treatment", "If wrong, does the answer change?", "Monitor / mitigate"],
        ["Benchmark sites represent what Parcelbird Now would achieve", "14 customer sites + pop-up; pop-up was worse",
         "Only if Parcelbird beat the best site on all four drivers at once", "Reopen trigger: a site that is positive at site level (slide 18)"],
        ["Density in mid-size Midwest cities", "Median 900/day; pop-up 280 (≈410 at exit)", "No: break-even fails even at 1,400/day", "Track customer-site density"],
        ["AOV can rise without losing the convenience use case", "Range $31–$45 tested", "No: break-even AOV is $44–$63 with 6% promotions", "Covered by the site-level reopen trigger"],
        ["Rider labor rules (2 of 3 cities)", "Not in base case", "Reinforces it: −$0.42/order per +$1/hour", "Reopen trigger: rules final in target cities"],
        ["$9.5M excludes software burn", "Base case; all-in reading also tested", "No: floor breached in month 11 even if all-in", "Ask founders to confirm budget scope"],
        ["Software ARR grows 60% with $0.8M hires", "Tested at 45% and 30%; opex +10%/yr", "No, but at 30% cost action is needed by about month 20",
         "Quarterly ARR review; pre-agreed opex cuts"],
        ["Store-based module demand", "Qualitative (\"several grocers\")", "No: upside only, not needed for break-even", "Validate with 9 late-stage grocers in Q1"],
        ["Founder motivation and focus", "Not modelled", "Execution risk to software plan", "Give founders a q-commerce product to lead (option C)"]]
table(s, 0.5, 1.7, 12.33, 5.15, data, col_w=[3.0, 2.85, 3.3, 3.18], size=9.5, row_h=[0.4] + [0.59] * 8, bold_first_col=True, aligns={c: PP_ALIGN.LEFT for c in range(4)})

# =====================================================================
# 18. Decisions & next steps
s = new_slide("We ask the board to make three decisions in January and to set measurable triggers for "
              "reopening the operator question", section="Recommendation and next steps",
              source=SRC + "Trigger thresholds are set from the break-even analysis on slides 6–8 and the cash analysis on slides 12 and 15.")
tb(s, 0.5, 1.65, 6.1, 0.3, "Decisions for January 2027", size=12, bold=True, color=INK2)
decs = [("1", "Do not launch Parcelbird Now in 2027", "No dark-store leases, capex or launch marketing, and no further pop-ups."),
        ("2", "Fund software scaling: $0.8M a year", "2 engineers and 2 sales hires; target ≥11 new contracts per year to pay back the hires."),
        ("3", "Build a store-based fast-delivery module", "Build with 2–3 design-partner grocers from the late-stage pipeline; price as an add-on to the $96k contract.")]
y = 2.05
for n, h, b in decs:
    rect(s, 0.5, y, 0.45, 0.95, BLUE)
    tb(s, 0.5, y, 0.45, 0.95, n, size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    tb(s, 1.05, y, 5.55, 0.95, [dict(text=h, bold=True, size=12), dict(text=b, size=10.5, color=INK2)], anchor=MSO_ANCHOR.MIDDLE)
    y += 1.08
tb(s, 0.5, 5.35, 6.1, 0.3, "First 90 days", size=12, bold=True, color=INK2)
tb(s, 0.5, 5.65, 6.1, 1.3, [dict(text=t, bullet=True, size=10.5) for t in [
    "Weeks 1–4: hire plan approved; first design-partner grocer signed for the module",
    "Weeks 4–8: close as many of the 9 late-stage deals as possible (≈ $0.86M ARR)",
    "Week 12: board review of ARR growth, burn and runway against the base case"]])
tb(s, 7.0, 1.65, 5.8, 0.3, "Reopen the operator question only if all of these hold", size=12, bold=True, color=INK2)
data = [["Trigger", "Threshold", "Today"],
        ["A real site is positive at site level for 2 straight quarters, with promotions ≥ 5% and no extra fee", "≥ $0 / order", "Best composite −$1.76"],
        ["Software business is self-funding", "Burn ≤ 0 for a quarter", "Burn $0.4M / month"],
        ["Cash after a launch still gives ≥ 12 months of runway", "Fully funded plan", "Not met"],
        ["Rider pay rules in the target cities are known", "Rules final", "Under consideration"]]
table(s, 7.0, 2.05, 5.83, 3.45, data, col_w=[3.13, 1.35, 1.35], size=10, row_h=[0.4, 0.95, 0.7, 0.7, 0.7], aligns={0: PP_ALIGN.LEFT})
callout(s, 7.0, 5.7, 5.83, 1.2, None, [dict(text="On the base case the software business reaches break-even in early 2029. Parcelbird could then "
        "revisit operating from a position of strength, with benchmark data from many more customer sites.", size=10.5)])

# =====================================================================
# Appendix 1: unit economics detail
s = new_slide("Appendix 1. Unit economics calculations for all four scenarios",
              section="Appendix", source=SRC + "Delivery fee is net of its own payment cost, as stated in Table 3. Pop-up uses its own $650k annualised fixed cost.")
names = ["Pop-up (actual)", "Benchmark median", "Best observed (composite)", "Founders' plan"]
ins = list(M.SCENARIOS.values())
rows_ = [["Line ($ per order unless stated)", "Formula"] + names,
         ["Inputs: AOV / promo % / orders per rider-h / orders per day", "—"] + [f"${a} / {p*100:.0f}% / {r} / {n:,}" for a, r, n, p, f in ins]]
keys = [("Goods margin", "AOV × 27%"), ("Delivery fee", "Table 3, net"), ("Promotions", "−AOV × promo %"),
        ("Picking & packing", "Table 3"), ("Rider cost", "−$17.75 ÷ orders per rider-h"), ("Payment & packaging", "Table 3")]
for k, f in keys:
    rows_.append([k, f] + [fmt_money(SC[n][0][k]) for n in M.SCENARIOS])
rows_.append(["Order-level contribution", "Sum of the above"] + [fmt_money(SC[n][1]) for n in M.SCENARIOS])
rows_.append(["Site fixed cost per order", "−Fixed ÷ (orders/day × 365)"] + [fmt_money(SC[n][2]) for n in M.SCENARIOS])
rows_.append(["Site-level contribution", "Order-level + fixed"] + [fmt_money(SC[n][3]) for n in M.SCENARIOS])
rows_.append(["Annual result per site, $M", "Site-level × orders/day × 365"] +
             [f"{SC[n][3]*v[2]*365/1e6:+.2f}" for n, v in M.SCENARIOS.items()])
fonts = {(r, c): dict(bold=True) for r in (8, 10) for c in range(6)}
table(s, 0.5, 1.7, 12.33, 5.15, rows_, col_w=[3.1, 2.43, 1.7, 1.7, 1.7, 1.7], size=10, row_h=[0.45] + [0.425] * 11, fonts=fonts,
      bold_first_col=False)

# =====================================================================
# Appendix 2: cash model
s = new_slide("Appendix 2. Cash and runway model: method and assumptions", section="Appendix", source=SRC)
tb(s, 0.5, 1.7, 6.0, 5.2, [dict(text="Method", bold=True, size=12)] + [dict(text=t, bullet=True, size=10.5, space_before=5) for t in [
    "Monthly model from January 2027, starting at the $12.0M stated in the pack",
    "Software ARR compounds monthly at the annual growth rate; revenue = ARR ÷ 12; gross margin 81%",
    "Implied opex: $4.1M × 81% = $3.32M gross profit + $4.8M annual burn = $8.12M/yr, held flat in real terms (stress case: +10%/yr)",
    "Hires add $0.8M/yr (option C). Status quo (D) has no hires and assumes slower pipeline conversion",
    "Runway = cash ÷ that month's net burn. The board rule is ≥12 months at all times",
    "Launch (base reading): $9.5M spread evenly over 18 months on top of software burn, no hires",
    "Launch (all-in reading): $9.5M covers all company spending for 18 months",
    "Pilot: one store, $0.6M capex in month 1, $1.15M fixed, 600 orders/day average at −$2.67, $1.5M CAC over 12 months"]])
data = [["Output", "Value"], ["Months to break-even, 60% / 45% / 30% growth", "26 / 32 / 46"],
        ["Lowest cash, 60% / 45% growth", "$5.4M / $3.6M"], ["Lowest runway, 60% / 45% growth", "24 / 20 months"],
        ["Launch on top: floor breach / cash-out", "Month 2 / month 15"], ["Launch all-in: floor breach / cash at m18", "Month 11 / $2.5M"],
        ["Pilot: months below floor", "5 to 18 (low 6.3 months)"],
        ["CAC to fill 9 stores at 900 / 1,400 / 1,800 per day", "$13.5M / $21.1M / $27.1M"],
        ["Benchmark nine-store annual operating loss", "$18.2M"]]
table(s, 6.9, 1.75, 5.93, 4.3, data, col_w=[3.83, 2.1], size=10, row_h=0.47)

# =====================================================================
# Appendix 3: judgement calls
s = new_slide("Appendix 3. Where the briefing pack was ambiguous, we chose the reading that is most favourable to launching "
              "or most standard, and tested the alternative", section="Appendix", source=SRC)
data = [["Question we would have asked", "Choice made", "Effect on the answer"],
        ["Does “contribution per order” in the founders' model include dark-store fixed costs?", "Show both levels; decide on site level because Parcelbird would own the stores",
         "None: the median is negative at both levels (−$2.67 / −$6.17)"],
        ["Does the $9.5M include the existing software burn?", "Base: no (incremental). Also tested all-in", "None: floor breached in month 2 or month 11"],
        ["How to treat the best observed site, given best AOV and best density came from different sites?", "Combine them into a composite (generous to launch)",
         "None: still −$1.76 per order"],
        ["How to read the 44% survey result?", "Stated intent from 25–39s only; use pop-up retention (22%) as revealed behaviour", "Weakens the demand case"],
        ["What does the software business need to grow 60%?", "Assume the $0.8M hires sustain 60%; stress at 45% and 30%", "Recommendation holds; cost action needed only near 30%"],
        ["Cash at January 2027", "$12.0M as stated (Nov–Dec 2026 burn ignored)", "All paths about $0.8M lower; ranking unchanged"]]
table(s, 0.5, 1.7, 12.33, 5.1, data, col_w=[4.1, 4.4, 3.83], size=10, row_h=[0.4] + [0.78] * 6, bold_first_col=True, aligns={c: PP_ALIGN.LEFT for c in range(3)})

prs.save(OUT)
print("saved", os.path.abspath(OUT), "slides:", len(prs.slides))
