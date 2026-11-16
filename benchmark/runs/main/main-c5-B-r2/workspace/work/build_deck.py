"""Build the Parcelbird board deck. Run from project root: python3 work/build_deck.py"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from model import R, SCEN

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION, XL_TICK_LABEL_POSITION

# ---------- design tokens ----------
INK = RGBColor(0x0B, 0x0B, 0x0B)
INK2 = RGBColor(0x52, 0x51, 0x4E)
MUTED = RGBColor(0x89, 0x87, 0x81)
GRID = RGBColor(0xE1, 0xE0, 0xD9)
AXIS = RGBColor(0xC3, 0xC2, 0xB7)
PANEL = RGBColor(0xF3, 0xF2, 0xEE)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLUE = RGBColor(0x2A, 0x78, 0xD6)
NAVY = RGBColor(0x10, 0x42, 0x81)
ORANGE = RGBColor(0xEB, 0x68, 0x34)
AQUA = RGBColor(0x1B, 0xAF, 0x7A)
RED = RGBColor(0xD0, 0x3B, 0x3B)       # status: critical
GREEN = RGBColor(0x00, 0x63, 0x00)     # success text
LIGHTBLUE = RGBColor(0xCD, 0xE2, 0xFB)
FONT = "Calibri"

SECTIONS = ["Market", "Economics", "Funding", "Alternative"]
SRC = "Source: Parcelbird briefing pack (synthetic benchmark data); team analysis"

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]
W = 13.333
LM = 0.6            # left margin
CW = W - 2 * LM     # content width
FIT_WARN = []


def est_lines(text, width_in, size_pt):
    cpl = max(1, int(width_in * 72 / (size_pt * 0.50)))  # Calibri avg glyph ~0.5em
    lines = 0
    for para in text.split("\n"):
        words, cur, n = para.split(" "), 0, 1
        for w_ in words:
            L = len(w_) + (1 if cur else 0)
            if cur + L > cpl:
                n += 1; cur = len(w_)
            else:
                cur += L
        lines += n
    return lines


def tb(slide, x, y, w, h, paras, size=12, color=INK, bold=False, align=PP_ALIGN.LEFT,
       anchor=MSO_ANCHOR.TOP, spacing=1.0, space_after=0, name=None, check=True):
    """paras: str | list of str | list of list-of-runs; run = (text, {bold,color,size,italic})"""
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.04)
    tf.margin_top = tf.margin_bottom = Inches(0.02)
    tf.vertical_anchor = anchor
    if isinstance(paras, str):
        paras = [paras]
    total_h, plain = 0, []
    for i, p in enumerate(paras):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = align
        para.line_spacing = spacing
        para.space_after = Pt(space_after)
        runs = [(p, {})] if isinstance(p, str) else p
        txt = "".join(r[0] for r in runs)
        psize = max([r[1].get("size", size) for r in runs])
        total_h += est_lines(txt, w - 0.08, psize) * psize * 1.2 * spacing / 72 + space_after / 72
        for t, st in runs:
            r = para.add_run()
            r.text = t
            f = r.font
            f.name = FONT
            f.size = Pt(st.get("size", size))
            f.bold = st.get("bold", bold)
            f.italic = st.get("italic", False)
            f.color.rgb = st.get("color", color)
        plain.append(txt)
    if check and total_h > h + 0.05:
        FIT_WARN.append(f"slide {len(prs.slides)}: '{plain[0][:50]}' est {total_h:.2f}in > box {h:.2f}in")
    return box


def rect(slide, x, y, w, h, fill=PANEL, line=None, shape=MSO_SHAPE.RECTANGLE):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid(); s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line; s.line.width = Pt(0.75)
    s.shadow.inherit = False
    return s


def hline(slide, x, y, w, color=AXIS, weight=0.75):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x), Inches(y), Inches(x + w), Inches(y))
    c.line.color.rgb = color; c.line.width = Pt(weight)
    return c


def new_slide(title, section=None, source=SRC, title_size=22):
    s = prs.slides.add_slide(BLANK)
    # section tracker
    if section is not None:
        x = W - LM - 4 * 1.05
        for i, name in enumerate(SECTIONS):
            on = (i == section)
            tb(s, x + i * 1.05, 0.22, 1.05, 0.25, [[(f"{i+1} {name}", {"bold": on, "color": BLUE if on else MUTED})]],
               size=9, align=PP_ALIGN.CENTER, check=False)
            if on:
                rect(s, x + i * 1.05 + 0.1, 0.47, 0.85, 0.03, fill=BLUE)
    tb(s, LM, 0.55, CW, 0.95, title, size=title_size, bold=True, color=INK, anchor=MSO_ANCHOR.BOTTOM)
    hline(s, LM, 1.55, CW, color=INK, weight=1)
    # footer
    if source:
        tb(s, LM, 7.05, CW - 0.6, 0.3, source, size=8, color=MUTED, check=False)
    tb(s, W - LM - 0.5, 7.05, 0.5, 0.3, str(len(prs.slides)), size=8, color=MUTED, align=PP_ALIGN.RIGHT, check=False)
    return s


def table(slide, x, y, w, data, col_w, row_h=0.36, size=11, header_fill=NAVY, first_col_bold=True,
          fills=None, colors=None, bolds=None, aligns=None, header_size=None):
    rows, cols = len(data), len(data[0])
    gt = slide.shapes.add_table(rows, cols, Inches(x), Inches(y), Inches(w), Inches(row_h * rows))
    t = gt.table
    tblPr = gt._element.graphic.graphicData.tbl.tblPr
    # remove banding/style
    tblPr.set("bandRow", "0"); tblPr.set("firstRow", "0")
    for j, cw in enumerate(col_w):
        t.columns[j].width = Inches(cw)
    for i in range(rows):
        t.rows[i].height = Inches(row_h)
        for j in range(cols):
            c = t.cell(i, j)
            c.margin_left = c.margin_right = Inches(0.06)
            c.margin_top = c.margin_bottom = Inches(0.03)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            val = data[i][j]
            runs = [(val, {})] if isinstance(val, str) else val
            tf = c.text_frame; tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = (aligns[j] if aligns else (PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER))
            for txt, st in runs:
                r = p.add_run(); r.text = txt
                f = r.font; f.name = FONT
                f.size = Pt(st.get("size", (header_size or size) if i == 0 else size))
                if i == 0:
                    f.bold = True; f.color.rgb = WHITE
                else:
                    b = st.get("bold", (j == 0 and first_col_bold) or (bolds and bolds.get((i, j))))
                    f.bold = bool(b)
                    f.color.rgb = st.get("color", (colors or {}).get((i, j), INK))
            c.fill.solid()
            if i == 0:
                c.fill.fore_color.rgb = header_fill
            else:
                c.fill.fore_color.rgb = (fills or {}).get((i, j), (fills or {}).get((i, None), WHITE if i % 2 else RGBColor(0xF7, 0xF7, 0xF5)))
            # estimate fit
            ln = est_lines("".join(r_[0] for r_ in runs), col_w[j] - 0.12, size)
            if ln * size * 1.2 / 72 > row_h + 0.02:
                FIT_WARN.append(f"slide {len(prs.slides)} table cell ({i},{j}) '{''.join(r_[0] for r_ in runs)[:40]}' needs {ln} lines")
    return gt


def style_chart(chart, size=10, legend=True, legend_pos=XL_LEGEND_POSITION.TOP):
    chart.font.name = FONT
    chart.font.size = Pt(size)
    chart.font.color.rgb = INK2
    chart.has_legend = legend
    if legend:
        chart.legend.position = legend_pos
        chart.legend.include_in_layout = False
        chart.legend.font.size = Pt(size)


def axis_style(ax, fmt=None, grid=True, visible=True, size=10):
    ax.format.line.color.rgb = AXIS
    ax.tick_labels.font.size = Pt(size)
    ax.tick_labels.font.color.rgb = INK2
    if fmt:
        ax.tick_labels.number_format = fmt
        ax.tick_labels.number_format_is_linked = False
    try:
        ax.has_major_gridlines = grid
        if grid:
            ax.major_gridlines.format.line.color.rgb = GRID
            ax.major_gridlines.format.line.width = Pt(0.5)
    except Exception:
        pass
    ax.visible = visible


def waterfall(slide, x, y, w, h, steps, fmt="{:+.2f}", total_fmt="{:.2f}", ymin=None, ymax=None,
              label_size=10, cat_size=10, prefix="$"):
    """steps: list of (label, value, kind) kind in {'total','delta'}; totals are absolute levels."""
    cats, inv_pos, vis_pos, inv_neg, vis_neg, kinds, labels = [], [], [], [], [], [], []
    level = 0.0
    for lab, val, kind in steps:
        if kind == "total":
            lo, hi = min(0, val), max(0, val); level = val
            labels.append(("-" if val < 0 else "") + prefix + total_fmt.format(abs(val)))
        else:
            lo, hi = sorted([level, level + val]); level += val
            labels.append(("+" if val >= 0 else "−") + prefix + total_fmt.format(abs(val)))
        ip = vp = ineg = vneg = 0.0
        if lo >= 0:
            ip, vp = lo, hi - lo
        elif hi <= 0:
            ineg, vneg = hi, lo - hi
        else:
            vp, vneg = hi, lo
        cats.append(lab); inv_pos.append(ip); vis_pos.append(vp); inv_neg.append(ineg); vis_neg.append(vneg)
        kinds.append((kind, val))
    cd = CategoryChartData()
    cd.categories = cats
    cd.add_series("b+", inv_pos); cd.add_series("v+", vis_pos)
    cd.add_series("b-", inv_neg); cd.add_series("v-", vis_neg)
    gf = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_STACKED, Inches(x), Inches(y), Inches(w), Inches(h), cd)
    ch = gf.chart
    style_chart(ch, legend=False)
    plot = ch.plots[0]; plot.gap_width = 45; plot.overlap = 100
    va = ch.value_axis
    axis_style(va, fmt='"$"0;"−$"0', grid=True)
    if ymin is not None: va.minimum_scale = ymin
    if ymax is not None: va.maximum_scale = ymax
    ca = ch.category_axis
    axis_style(ca, grid=False, size=cat_size)
    ca.tick_label_position = XL_TICK_LABEL_POSITION.LOW
    ca.format.line.color.rgb = AXIS
    for si, ser in enumerate(plot.series):
        ser.invert_if_negative = False
        if si in (0, 2):
            ser.format.fill.background(); ser.format.line.fill.background()
        else:
            for pi, (kind, val) in enumerate(kinds):
                pt = ser.points[pi]
                pt.format.fill.solid()
                if kind == "total":
                    pt.format.fill.fore_color.rgb = NAVY if val >= 0 else RED
                else:
                    pt.format.fill.fore_color.rgb = BLUE if val >= 0 else ORANGE
                pt.format.line.fill.background()
    # labels: put on the visible segment that ends at the bar's outer edge
    for pi, (kind, val) in enumerate(kinds):
        top_is_pos = vis_pos[pi] != 0 and (vis_neg[pi] == 0 or (kind == "delta" and val > 0) or (kind == "total" and val > 0))
        ser = plot.series[1] if top_is_pos else plot.series[3]
        dl = ser.points[pi].data_label
        dl.has_text_frame = True
        dl.text_frame.text = labels[pi]
        dl.position = XL_LABEL_POSITION.INSIDE_END if False else XL_LABEL_POSITION.CENTER
        r = dl.text_frame.paragraphs[0].runs[0]
        r.font.size = Pt(label_size); r.font.bold = True
        r.font.color.rgb = WHITE if not (kind == "delta" and abs(val) < 0.9) else INK
        r.font.name = FONT
    return ch



from pptx.oxml.ns import qn
from lxml import etree
from pptx.enum.chart import XL_MARKER_STYLE


def set_skip(chart, n):
    """Insert tickLblSkip/tickMarkSkip in schema order (before noMultiLvlLbl/extLst)."""
    ca = chart.category_axis._element
    anchor = ca.find(qn("c:noMultiLvlLbl"))
    if anchor is None:
        anchor = ca.find(qn("c:extLst"))
    for tag in ("c:tickLblSkip", "c:tickMarkSkip"):
        el = etree.Element(qn(tag)); el.set("val", str(n))
        if anchor is not None:
            anchor.addprevious(el)
        else:
            ca.append(el)

# =====================================================================
U = R["unit"]
med, best, fp, pop = U["Benchmark median"], U["Best observed"], U["Founders' plan"], U["Pop-up test"]
money = lambda v: ("−" if v < 0 else "+") + f"${abs(v):.2f}"
mm = lambda v: ("−" if v < 0 else "+") + f"${abs(v)/1e6:.1f}M"
OPT = R["options"]
A_neg = next(r["m"] for r in OPT["A_60"]["rows"] if r["cash"] < 0)

# ---------- 1. Title ----------
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, W, 7.5, fill=NAVY)
rect(s, LM, 2.35, 0.08, 2.0, fill=BLUE)
tb(s, LM + 0.3, 2.2, 11.5, 1.4, "Should Parcelbird launch its own quick-commerce grocery delivery service in 2027?",
   size=34, bold=True, color=WHITE)
tb(s, LM + 0.3, 3.65, 11.5, 0.8, "Assessment of the Parcelbird Now proposal and recommendation to the board",
   size=18, color=LIGHTBLUE)
tb(s, LM + 0.3, 5.6, 11.5, 0.9, ["Board meeting, January 2027", "Prepared from the board briefing pack only (synthetic benchmark data); no external research"],
   size=12, color=LIGHTBLUE)

# ---------- 2. Executive summary ----------
s = new_slide("Recommendation: do not launch Parcelbird Now in 2027; invest in the software business, "
              "which can reach profitability within current cash")
rows = [
    ("1", "Market", "The market is growing fast, but no operator makes money in it",
     f"US quick-commerce GMV grew {R['market_cagr']*100:.0f}% a year, 2022–25. Both incumbents lose money on every order "
     f"(EBITDA margins −{abs(R['ebitda_margin']['Zipcart'])*100:.0f}% and −{abs(R['ebitda_margin']['QuickBasket'])*100:.0f}%); QuickBasket closed 4 of its 11 cities."),
    ("2", "Economics", "A Parcelbird dark store would lose money on every order, and customers don't stay long enough to repay their acquisition cost",
     f"Loss of {money(med['site_level'])[1:]} per order at benchmark median, and {money(best['site_level'])[1:]} with best-observed inputs on every driver. "
     f"Only the founders' plan ({money(fp['site_level'])}) is profitable, and it beats the best site ever observed on all four drivers. "
     f"Our pop-up lost ${abs(pop['site_level']):.2f} per order; 22% of its customers were still ordering in month 3."),
    ("3", "Funding", "Even on the founders' own numbers, the launch breaks the investors' cash constraints",
     f"The launch needs $9.5M; only ${R['spendable_headroom']:.1f}M can be spent while keeping 12 months of runway. "
     f"Adding today's core burn, cash runs out in month {A_neg}. At benchmark economics, 9 stores would lose ${abs(R['network9']['Benchmark median'])/1e6:.0f}M a year."),
    ("4", "Alternative", "The software business is a better use of the same cash",
     f"It breaks even in about month {R['sw'][0.6]['breakeven_month']} at today's 60% growth "
     f"(month {R['sw'][0.4]['breakeven_month']} at 40%) and never drops below 12 months of runway, provided growth stays at {R['sw_min_growth']}% or more. "
     "Selling store-based fast delivery to pipeline grocers gives Parcelbird a share of the market's growth."),
]
y0 = 1.8
for i, (n, sec, head, ev) in enumerate(rows):
    y = y0 + i * 1.08
    rect(s, LM, y, 0.42, 0.95, fill=BLUE)
    tb(s, LM, y, 0.42, 0.95, n, size=18, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    tb(s, LM + 0.55, y, 1.25, 0.95, sec, size=12, bold=True, color=BLUE, anchor=MSO_ANCHOR.MIDDLE)
    tb(s, LM + 1.8, y, 3.9, 0.95, head, size=13, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    tb(s, LM + 5.85, y, CW - 5.85, 0.95, ev, size=11, color=INK2, anchor=MSO_ANCHOR.MIDDLE)
    if i < 3:
        hline(s, LM + 0.55, y + 1.03, CW - 0.55, color=GRID)
rect(s, LM, 6.15, CW, 0.8, fill=PANEL)
tb(s, LM + 0.15, 6.18, CW - 0.3, 0.75,
   [[("Decisions for the board: ", {"bold": True, "color": NAVY}),
     ("(1) decline the 2027 launch and do not extend the pop-up; (2) approve the $0.8M a year of software hires, "
      "phased against signed contracts; (3) build a store-based fast-delivery offer for the grocers in the pipeline; "
      "(4) adopt explicit re-entry triggers, tracked through our customers' sites, before quick commerce is reconsidered.", {})]],
   size=11.5, anchor=MSO_ANCHOR.MIDDLE)

# ---------- 3. Hypothesis test ----------
s = new_slide("We started from the founders' answer, \"launch\", and tested the six conditions it needs; "
              "the evidence supports none of them")
tb(s, LM, 1.7, CW, 0.35, [[("Initial hypothesis tested: ", {"bold": True}),
   ("“Parcelbird should launch Parcelbird Now: 9 dark stores in 3 cities, contribution-positive per order by month 18.”", {"italic": True})]],
   size=12, color=INK2)
X = [("× Not met", RED), ("× Not met", RED), ("× Not shown", RED), ("× Not met", RED), ("× Not met", RED), ("× Not met", RED)]
data = [["Section", "What would have to be true", "What the evidence shows", "Verdict"],
        ["1 Market", "1. The market has a profit pool, not just growth",
         f"GMV +{R['market_cagr']*100:.0f}% a year, but contribution per order is −$1.90 (Zipcart) and −$3.40 (QuickBasket); QuickBasket shut 36% of its cities", X[0]],
        ["2 Economics", "2. A dark store makes money per order at achievable inputs",
         f"{money(med['site_level'])} per order at benchmark median; {money(best['site_level'])} even with every best-observed input combined", X[1]],
        ["", "3. Parcelbird runs stores better than the benchmark",
         "The pop-up was below the median on all four drivers (AOV, promotions, rider productivity, density)", X[2]],
        ["", "4. Customers stay long enough to repay acquisition cost",
         "$38 CAC; 22% still ordering in month 3; CAC is never repaid at benchmark or pop-up economics", X[3]],
        ["3 Funding", "5. The plan fits current cash with 12 months of runway",
         f"$9.5M needed vs ${R['spendable_headroom']:.1f}M spendable above the runway floor; no new funding expected", X[4]],
        ["4 Alternative", "6. It beats the best other use of the cash",
         f"The software business can reach break-even within current cash if growth stays at {R['sw_min_growth']}% or more", X[5]]]
for i in range(1, 7):
    lab, col = data[i][3]
    data[i][3] = [(lab, {"bold": True, "color": col})]
table(s, LM, 2.2, CW, data, [1.45, 3.6, 5.9, 1.18], row_h=0.58, size=11.5, aligns=[PP_ALIGN.LEFT]*3 + [PP_ALIGN.CENTER])
rect(s, LM, 6.4, CW, 0.55, fill=PANEL)
tb(s, LM + 0.15, 6.42, CW - 0.3, 0.5,
   [[("So what: ", {"bold": True, "color": NAVY}),
     ("the hypothesis fails on every condition, so we reverse it. The rest of the deck sets out the evidence in the order of the table.", {})]],
   size=12, anchor=MSO_ANCHOR.MIDDLE)

# ---------- 4. Market ----------
s = new_slide(f"Quick commerce is growing {R['market_cagr']*100:.0f}% a year, but both incumbents lose money "
              "on every order and one is already retreating", section=0)
tb(s, LM, 1.75, 5.6, 0.3, "US quick-commerce grocery GMV, $ billions", size=12, bold=True)
cd = CategoryChartData()
yoy = R["market_yoy"]
cd.categories = ["2022", f"2023\n+{yoy[2023]*100:.0f}%", f"2024\n+{yoy[2024]*100:.0f}%", f"2025\n+{yoy[2025]*100:.0f}%"]
cd.add_series("GMV", [1.8, 2.6, 3.6, 5.1])
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(LM), Inches(2.05), Inches(5.6), Inches(4.0), cd)
ch = gf.chart; style_chart(ch, legend=False)
ch.plots[0].gap_width = 70
ser = ch.plots[0].series[0]; ser.format.fill.solid(); ser.format.fill.fore_color.rgb = BLUE
ch.plots[0].has_data_labels = True
dls = ch.plots[0].data_labels; dls.number_format = '"$"0.0"B"'; dls.number_format_is_linked = False
dls.position = XL_LABEL_POSITION.OUTSIDE_END; dls.font.size = Pt(11); dls.font.bold = True; dls.font.color.rgb = INK
axis_style(ch.value_axis, fmt='0', grid=True); ch.value_axis.maximum_scale = 6; ch.value_axis.visible = False
ch.value_axis.has_major_gridlines = False
axis_style(ch.category_axis, grid=False, size=11)
tb(s, LM, 6.1, 5.6, 0.5, f"Year-on-year growth shown under each year; CAGR 2022–25 = (5.1 / 1.8)^(1/3) − 1 = {R['market_cagr']*100:.1f}%",
   size=9.5, color=INK2)

xr = LM + 6.1
tb(s, xr, 1.75, CW - 6.1, 0.3, "Incumbent operators, 2025", size=12, bold=True)
em = R["ebitda_margin"]
data = [["", "Zipcart (national)", "QuickBasket (regional)"],
        ["Revenue", "$1,200M", "$210M"],
        ["EBITDA", "−$310M", "−$96M"],
        ["EBITDA margin", f"−{abs(em['Zipcart'])*100:.0f}%", f"−{abs(em['QuickBasket'])*100:.0f}%"],
        ["Contribution per order", "−$1.90", "−$3.40"],
        ["Footprint signal", "Positive in only its densest city, and only after a fee rise (p. 10)", "Closed 4 of 11 cities (36%) in 2025"]]
cols = {(i, j): RED for i in (2, 3, 4) for j in (1, 2)}
table(s, xr, 2.1, CW - 6.1, data, [1.75, 2.3, 2.08], row_h=0.48, size=11, colors=cols)
data_h = 6 * 0.48
rect(s, xr, 2.1 + data_h + 0.3, CW - 6.1, 1.3, fill=PANEL)
tb(s, xr + 0.15, 2.1 + data_h + 0.35, CW - 6.4, 1.2,
   [[("So what: ", {"bold": True, "color": NAVY}),
     ("the market's growth is real, but none of it has become profit. \"Nobody owns the Midwest\" may simply mean "
      "nobody has made it pay. Growth does not justify entry on its own; the per-order economics have to.", {})]],
   size=12, anchor=MSO_ANCHOR.MIDDLE)

# ---------- 5. Median waterfall ----------
s = new_slide(f"At benchmark-median inputs a Parcelbird store would lose ${abs(med['site_level']):.2f} per order; "
              f"${abs(med['variable']):.2f} of that is lost before any site cost, so more volume cannot fix it", section=1)
tb(s, LM, 1.75, 8.0, 0.3, "Contribution per order at benchmark median (14 customer sites, 2025), $", size=12, bold=True)
L = med["lines"]
steps = [("Goods margin\n(27% × $34)", L["Goods margin (27% of AOV)"], "delta"),
         ("Delivery fee", L["Delivery fee (net)"], "delta"),
         ("Promotions\n(6% × $34)", L["Promotions"], "delta"),
         ("Picking &\npacking", L["Picking & packing"], "delta"),
         ("Rider\n($17.75 ÷ 2.4)", L["Rider cost"], "delta"),
         ("Payment &\npackaging", L["Payment & packaging"], "delta"),
         ("Before site\nfixed cost", med["variable"], "total"),
         ("Site fixed cost\n($1.15M ÷ 328.5k)", med["site_fixed"], "delta"),
         ("After site\nfixed cost", med["site_level"], "total")]
waterfall(s, LM, 2.05, 8.1, 4.75, steps, ymin=-8, ymax=12, cat_size=9)
xr = LM + 8.35
rect(s, xr, 1.8, CW - 8.35, 5.0, fill=PANEL)
tb(s, xr + 0.15, 1.9, CW - 8.65, 4.85, [
    [("How to read it", {"bold": True, "color": NAVY})],
    "Each order brings in $11.17 (goods margin plus delivery fee) and costs $13.84 in promotions, picking, riders and payment before the store's rent and staff are counted.",
    [("Why volume can't fix it", {"bold": True, "color": NAVY})],
    f"Higher density spreads the ${abs(med['site_fixed']):.2f} of site cost over more orders, but each extra order still loses ${abs(med['variable']):.2f}. "
    "The model only turns positive if AOV or rider productivity rise sharply.",
    [("Biggest cost line", {"bold": True, "color": NAVY})],
    f"Riders: ${abs(L['Rider cost']):.2f} per order, 81% of the goods margin. Two of our three cities are considering minimum pay standards for delivery workers.",
], size=11.5, space_after=6)

# ---------- 6. Scenarios ----------
s = new_slide("Only the founders' plan makes money; even the best-observed result on every driver at once "
              f"loses ${abs(best['site_level']):.2f} per order", section=1)
tb(s, LM, 1.75, 7.4, 0.3, "Contribution per order by input scenario, $", size=12, bold=True)
order = ["Pop-up test", "Benchmark median", "Best observed", "Founders' plan"]
cd = CategoryChartData()
cd.categories = ["Columbus pop-up\n(actual)", "Benchmark\nmedian", "Best observed\n(all drivers)", "Founders'\nplan"]
cd.add_series("Before site fixed cost", [U[k]["variable"] for k in order])
cd.add_series("After site fixed cost", [U[k]["site_level"] for k in order])
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(LM), Inches(2.05), Inches(7.4), Inches(3.55), cd)
ch = gf.chart; style_chart(ch, legend=True)
ch.plots[0].gap_width = 60; ch.plots[0].overlap = -5
for ser, col in zip(ch.plots[0].series, [BLUE, ORANGE]):
    ser.format.fill.solid(); ser.format.fill.fore_color.rgb = col; ser.invert_if_negative = False
ch.plots[0].has_data_labels = True
dls = ch.plots[0].data_labels; dls.number_format = '"+$"0.00;"−$"0.00'; dls.number_format_is_linked = False
dls.position = XL_LABEL_POSITION.OUTSIDE_END; dls.font.size = Pt(10); dls.font.bold = True; dls.font.color.rgb = INK
axis_style(ch.value_axis, fmt='"$"0;"−$"0', grid=True); ch.value_axis.minimum_scale = -15; ch.value_axis.maximum_scale = 5
axis_style(ch.category_axis, grid=False, size=10)
ch.category_axis.tick_label_position = XL_TICK_LABEL_POSITION.LOW
# inputs + annual table beneath
n9 = R["network9"]
data = [["", "Pop-up", "Median", "Best obs.", "Plan"],
        ["AOV / promotions", "$31 / 12%", "$34 / 6%", "$42 / 6%", "$45 / 2%"],
        ["Orders per rider-hour", "2.1", "2.4", "3.0", "3.5"],
        ["Orders per site per day", "280", "900", "1,400", "1,800"],
        ["Profit per store per year", mm(pop["annual_site"]), mm(med["annual_site"]), mm(best["annual_site"]), mm(fp["annual_site"])],
        ]
cols = {(4, 1): RED, (4, 2): RED, (4, 3): RED, (4, 4): GREEN}
table(s, LM, 5.68, 7.4, data, [2.2, 1.3, 1.3, 1.3, 1.3], row_h=0.27, size=10, colors=cols)
xr = LM + 7.7
rect(s, xr, 1.8, CW - 7.7, 5.0, fill=PANEL)
tb(s, xr + 0.15, 1.9, CW - 8.0, 4.85, [
    [("No site has achieved the best-observed case", {"bold": True, "color": NAVY})],
    "The best AOV ($42) and the best density (1,400 orders/day) come from different sites. Combining them is already optimistic, and it still loses money.",
    [("Nine stores at network scale", {"bold": True, "color": NAVY})],
    f"Median: {mm(n9['Benchmark median'])} a year. Best observed: {mm(n9['Best observed'])} a year. Founders' plan: {mm(n9['Founders\' plan'])} a year. "
    "Only the plan's inputs give a profitable network.",
    [("Break-even AOV", {"bold": True, "color": NAVY})],
    f"With other inputs held, the median store needs an AOV of ${R['breakeven_aov']['Benchmark median']:.0f} and the best-observed store ${R['breakeven_aov']['Best observed']:.0f}. "
    "The median is $34 and the best ever observed is $42.",
    [("Definition", {"bold": True, "color": NAVY})],
    "\"Before site fixed cost\" covers the variable costs of each order. \"After\" also spreads each store's $1.15M a year of rent, staff and utilities (pop-up: $0.65M) across its orders. "
    "Both figures exclude HQ overhead, capex and marketing.",
], size=11, space_after=5)

# ---------- 7. Founders' plan stretch ----------
s = new_slide("The founders' plan needs results beyond the best site ever observed on all four drivers; "
              "if AOV or rider productivity only reaches the median, the plan loses money again", section=1)
tb(s, LM, 1.75, 7.0, 0.3, "Founders' plan inputs against what has been observed", size=12, bold=True)
data = [["Driver", "Observed range", "Median", "Best", "Plan", "Plan vs best"],
        ["Average order value", "n/a", "$34", "$42", "$45", [("+7%", {"bold": True, "color": RED})]],
        ["Promotions, % of AOV", "Pop-up: 12%", "6%", "6%", "2%", [("−4 pts", {"bold": True, "color": RED})]],
        ["Orders per rider-hour", "1.9–3.0", "2.4", "3.0", "3.5", [("+17% above range", {"bold": True, "color": RED})]],
        ["Orders per site per day", "400–1,400", "900", "1,400", "1,800", [("+29% above range", {"bold": True, "color": RED})]]]
table(s, LM, 2.1, 7.0, data, [2.0, 1.25, 0.8, 0.75, 0.75, 1.45], row_h=0.5, size=11)
rect(s, LM, 4.8, 7.0, 1.75, fill=PANEL)
tb(s, LM + 0.15, 4.88, 6.7, 1.65, [
    [("Sanity check on scale", {"bold": True, "color": NAVY})],
    f"9 stores × 1,800 orders × $45 × 365 days = ${R['plan_gmv']:.0f}M a year of sales in three mid-size cities. "
    "That is more than QuickBasket's total 2025 revenue ($210M) across all its cities, and about 5% of the entire 2025 US market ($5.1B).",
    "(This compares our GMV with their reported revenue, which we take to be roughly equivalent for an operator that sells the goods itself.)",
], size=11, space_after=4)
xr = LM + 7.4
tb(s, xr, 1.75, CW - 7.4, 0.3, "Plan profit per order if one driver is at the median, $", size=12, bold=True)
fr = R["founders_revert_one"]
labels = ["Plan as proposed"] + list(fr.keys())
vals = [fp["site_level"]] + list(fr.values())
cd = CategoryChartData()
cd.categories = ["Plan as proposed", "AOV $45 → $34", "Riders 3.5 → 2.4 /hr", "Orders/day 1,800 → 900", "Promotions 2% → 6%"]
cd.add_series("Contribution per order", vals)
gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(xr), Inches(2.1), Inches(CW - 7.4), Inches(3.4), cd)
ch = gf.chart; style_chart(ch, legend=False)
ch.plots[0].gap_width = 60
ser = ch.plots[0].series[0]; ser.invert_if_negative = False
for i, v in enumerate(vals):
    pt = ser.points[i]; pt.format.fill.solid()
    pt.format.fill.fore_color.rgb = NAVY if i == 0 else (ORANGE if v < 0 else BLUE)
ch.plots[0].has_data_labels = True
dls = ch.plots[0].data_labels; dls.number_format = '"+$"0.00;"−$"0.00'; dls.number_format_is_linked = False
dls.position = XL_LABEL_POSITION.OUTSIDE_END; dls.font.size = Pt(10.5); dls.font.bold = True; dls.font.color.rgb = INK
axis_style(ch.value_axis, fmt='"$"0.0;"−$"0.0', grid=True); ch.value_axis.minimum_scale = -1.5; ch.value_axis.maximum_scale = 3
axis_style(ch.category_axis, grid=False, size=10)
ch.category_axis.tick_label_position = XL_TICK_LABEL_POSITION.LOW
ch.category_axis.reverse_order = True
tb(s, xr, 5.6, CW - 7.4, 1.2,
   "The plan is most exposed to AOV and rider productivity, the two drivers it stretches furthest. "
   "Falling short on density or promotions alone still leaves a thin positive margin of about $0.2–0.3 per order, "
   "but nothing for HQ overhead or marketing.",
   size=11, color=INK2)

# ---------- 8. Pop-up ----------
s = new_slide("Our own Columbus pop-up came in below the benchmark median on every driver, so there is "
              "no evidence yet that we run stores better than others", section=1)
data = [["Driver", "Columbus pop-up (6 weeks)", "Benchmark median", "Founders' plan", "Pop-up vs median"],
        ["Average order value", "$31", "$34", "$45", "−9%"],
        ["Promotions, % of AOV", "12%", "6%", "2%", "2× higher"],
        ["Orders per rider-hour", "2.1", "2.4", "3.5", "−13%"],
        ["Orders per site per day", "280", "900", "1,800", "−69%"],
        ["Contribution before site cost", money(pop["variable"]), money(med["variable"]), money(fp["variable"]), ""],
        ["Contribution after site cost", money(pop["site_level"]), money(med["site_level"]), money(fp["site_level"]), ""]]
cols = {(i, 4): RED for i in range(1, 5)}
cols.update({(5, 1): RED, (5, 2): RED, (6, 1): RED, (6, 2): RED, (5, 3): GREEN, (6, 3): GREEN})
bolds = {(6, 1): True, (6, 2): True, (6, 3): True}
table(s, LM, 1.85, 7.7, data, [2.5, 1.55, 1.3, 1.15, 1.2], row_h=0.5, size=11, colors=cols, bolds=bolds)
tb(s, LM, 5.5, 7.7, 0.9, f"Pop-up site cost: $650,000 a year ÷ (280 × 365 orders) = ${abs(pop['site_fixed']):.2f} per order. "
   f"Rider cost: $17.75 ÷ 2.1 = ${abs(pop['lines']['Rider cost']):.2f} per order.", size=10, color=INK2)
xr = LM + 8.0
rect(s, xr, 1.85, CW - 8.0, 4.95, fill=PANEL)
tb(s, xr + 0.15, 1.95, CW - 8.3, 4.8, [
    [("The founders' case for a capability edge", {"bold": True, "color": NAVY})],
    "\"Our software already runs other people's dark stores, so we know how to run them better than anyone.\" The pop-up is the only test of this, and it did worse than the median of the stores our software runs.",
    [("Fair caveat: it was early", {"bold": True, "color": NAVY})],
    f"Six weeks on a temporary site. Orders grew 18% a week, from roughly {R['popup_week1_per_day']:.0f} a day in week 1 to roughly {R['popup_week6_per_day']:.0f} in week 6 (our estimate from the compounding). "
    "But that growth came with 12% promotions and $38 of acquisition cost per customer.",
    [("Implication", {"bold": True, "color": NAVY})],
    "Even if density reached the median, the store would still lose $6.17 per order (p. 5). Ramp-up alone does not close the gap.",
], size=11, space_after=5)

# ---------- 9. Customers ----------
s = new_slide("Customers don't stay long enough to repay their $38 acquisition cost: 44% say they would order weekly, "
              "but only 22% of pop-up customers were still ordering in month 3", section=1)
# left: intent vs behaviour
tb(s, LM, 1.75, 4.6, 0.3, "Stated intent vs. observed behaviour", size=12, bold=True)
for i, (big, lab) in enumerate([("44%", "of 1,500 surveyed Columbus residents aged 25–39 said they would use 15-minute delivery “at least weekly” (stated intent, one age group only)"),
                                ("22%", "of pop-up customers were still ordering in month 3, at 3.1 orders a month (observed behaviour)"),
                                (f"{R['orders_per_acq_cust_month']:.2f}", "orders a month per acquired customer by month 3 (22% × 3.1)")]):
    y = 2.15 + i * 1.5
    tb(s, LM, y, 1.5, 1.2, big, size=34, bold=True, color=NAVY if i < 2 else BLUE, anchor=MSO_ANCHOR.MIDDLE)
    tb(s, LM + 1.55, y, 3.05, 1.2, lab, size=11, color=INK2, anchor=MSO_ANCHOR.MIDDLE)
xr = LM + 5.0
tb(s, xr, 1.75, CW - 5.0, 0.3, "Months to repay $38 of acquisition cost, by unit-economics scenario", size=12, bold=True)
cac_o, cac_m = R["cac_payback_orders"], R["cac_payback_months"]
data = [["Scenario", "Contribution per order\n(before site cost)", "Orders to repay $38", "Months to repay*"],
        ["Columbus pop-up", money(pop["variable"]), "Never", [("Never", {"bold": True, "color": RED})]],
        ["Benchmark median", money(med["variable"]), "Never", [("Never", {"bold": True, "color": RED})]],
        ["Best observed", money(best["variable"]), f"{cac_o['Best observed']:.0f}", [(f"{cac_m['Best observed']:.0f} (~9 years)", {"bold": True, "color": RED})]],
        ["Founders' plan", money(fp["variable"]), f"{cac_o['Founders\' plan']:.0f}", [(f"{cac_m['Founders\' plan']:.0f}", {"bold": True})]]]
table(s, xr, 2.1, CW - 5.0, data, [1.9, 1.85, 1.55, 1.83], row_h=0.55, size=11.5, header_size=10.5)
tb(s, xr, 4.95, CW - 5.0, 0.55, "* Months = ($38 ÷ contribution per order) ÷ 0.68 orders per acquired customer per month. "
   "This is generous: it assumes no churn after month 3 and uses contribution before any site cost.", size=9.5, color=INK2)
rect(s, xr, 5.6, CW - 5.0, 1.2, fill=PANEL)
tb(s, xr + 0.15, 5.65, CW - 5.3, 1.1,
   [[("So what: ", {"bold": True, "color": NAVY}),
     ("buying growth with promotions and paid social does not create value at these economics. At the median, every "
      "customer acquired adds to the losses. Even under the founders' plan, payback takes more than a year.", {})]],
   size=11.5, anchor=MSO_ANCHOR.MIDDLE)

# ---------- 10. Zipcart ----------
zm = R["zipcart_on_median"]
s = new_slide("Zipcart's one profitable city needed a $3.99 fee and near-zero promotions, and it lost 14% of its volume; "
              f"the same moves on our median store still lose ${abs(zm['site_level']):.2f} per order", section=1)
tb(s, LM, 1.75, 7.6, 0.3, "Applying Zipcart's Q4 2025 moves to the benchmark-median store, contribution after site cost, $/order", size=12, bold=True)
fixed_delta = zm["site_fixed"] - med["site_fixed"]
steps = [("Benchmark\nmedian", med["site_level"], "total"),
         ("+$3.99 service\nfee", 3.99, "delta"),
         ("Promotions\n6% → 1%", 0.05 * 34, "delta"),
         ("Volume −14%:\nsite cost per order", fixed_delta, "delta"),
         ("With Zipcart\nmoves", zm["site_level"], "total")]
waterfall(s, LM, 2.05, 7.6, 4.7, steps, ymin=-8, ymax=2, cat_size=10)
xr = LM + 7.9
rect(s, xr, 1.8, CW - 7.9, 5.0, fill=PANEL)
tb(s, xr + 0.15, 1.9, CW - 8.2, 4.85, [
    [("What the investor update leaves out", {"bold": True, "color": NAVY})],
    "\"Zipcart turned contribution-positive (+$0.40 per order)\" was true only for its densest city, after a new $3.99 fee on every order and a cut in promotions to 1%. Volume in that city then fell 14%.",
    [("What it would take for us", {"bold": True, "color": NAVY})],
    f"With those moves, a median store before site cost earns {money(zm['variable'])} per order. To cover $1.15M of site cost it needs about "
    f"{R['zipcart_breakeven_opd']:,.0f} orders a day after the fee rise: 16% above today's median, 3.7× the pop-up, "
    "and with no loss of rider productivity at the lower volume.",
    [("Read-across", {"bold": True, "color": NAVY})],
    "A profitable route may exist, but only at top-quartile density with premium pricing. This is not where a new entrant starts, and nothing in our data shows it yet.",
], size=11, space_after=5)

# ---------- 11. Funding ----------
s = new_slide("Even on the founders' own numbers, the launch breaks the 12-month runway rule, and with today's "
              f"core burn added it runs out of cash by month {A_neg}", section=2)
tb(s, LM, 1.75, 6.6, 0.3, "Cash available for Parcelbird Now vs. founders' requirement, $M", size=12, bold=True)
steps = [("Cash in\nbank", 12.0, "total"),
         ("12-month\nrunway floor\n(12 × $0.4M)", -R["runway_floor_today"], "delta"),
         ("Spendable", R["spendable_headroom"], "total"),
         ("Founders' cash\nneed to\nmonth 18", -9.5, "delta"),
         ("Shortfall", R["spendable_headroom"] - 9.5, "total")]
waterfall(s, LM, 2.05, 6.6, 4.3, steps, ymin=-4, ymax=14, cat_size=10, total_fmt="{:.1f}", prefix="$")
tb(s, LM, 6.4, 6.6, 0.55, "The floor rises once stores are operating, because a higher burn needs a larger reserve to cover 12 months. "
   "The $7.2M of headroom is therefore a ceiling.", size=10, color=INK2)
xr = LM + 6.9
facts = [
    ("If the $9.5M is in addition to today's $0.4M a month of core burn",
     f"With software ARR still growing 60% a year, cash falls below 12 months of runway in month {OPT['A_60']['breach']} and below zero in month {A_neg} (model, p. 14)."),
    ("Even if the $9.5M covered all company spending",
     f"$12.0M − $9.5M = $2.5M left at month 18: about 6 months of runway at today's burn, against the 12 required."),
    ("If benchmark economics apply rather than the plan's",
     f"A mature 9-store network loses about ${abs(R['network9']['Benchmark median'])/1e6:.0f}M a year (${abs(R['network9']['Benchmark median'])/12e6:.1f}M a month), "
     "more than our total cash every year. The lead investor calls a new round for a delivery operator \"unlikely\"."),
]
for i, (h, b) in enumerate(facts):
    y = 1.8 + i * 1.68
    rect(s, xr, y, 0.07, 1.5, fill=RED)
    tb(s, xr + 0.2, y, CW - 7.1, 1.5, [[(h, {"bold": True, "color": INK})], b], size=11.5, space_after=3)

# ---------- 12. Options ----------
s = new_slide("Of the three options, only software-first meets both investor constraints and keeps a "
              "foothold in fast delivery", section=3)
G, Rd, Am = GREEN, RED, RGBColor(0x9A, 0x5B, 0x00)
data = [["Criterion", "A. Launch Parcelbird Now\n(9 dark stores, 3 cities)", "B. One permanent pilot store\n(Columbus)", "C. Software-first + store-based\nfast delivery for grocers (recommended)"],
        ["Per-order economics", [(f"No: {money(med['site_level'])} median; positive only on plan inputs", {"color": Rd})],
         [(f"No: {money(med['site_level'])} median; {money(pop['site_level'])} pop-up actual", {"color": Rd})],
         [("Yes: 81% gross margin on $96k contracts", {"color": G})]],
        ["Cash need", [("No: $9.5M to month 18 (plan)", {"color": Rd})], [("Partly: $0.6M capex + ~$2.0M a year loss", {"color": Am})], [("Yes: $0.8M a year of hires, phased", {"color": G})]],
        ["12-month runway rule", [(f"No: Breached in month {OPT['A_60']['breach']}; cash out in month {A_neg}", {"color": Rd})],
         [(f"No: Breached in month {OPT['B_60']['breach']}", {"color": Rd})], [(f"Yes: Never below {OPT['C_60']['rows'] and min(r['runway'] for r in OPT['C_60']['rows']):.0f} months at 60% growth", {"color": G})]],
        ["Path to profit within current cash", [("No: Only if every driver beats the best observed", {"color": Rd})],
         [("No: None: a single store cannot reach scale", {"color": Rd})], [(f"Yes: Break-even in month {R['sw'][0.6]['breakeven_month']} (60%) or {R['sw'][0.4]['breakeven_month']} (40%)", {"color": G})]],
        ["Strategic fit", [("No: Competes with the grocers we sell to; distracts the team", {"color": Rd})],
         [("Partly: Little new learning: pop-up and 14-site data already exist", {"color": Am})],
         [("Yes: Meets demand already in the pipeline", {"color": G})]],
        ["Main risk", "Unit economics never close; cash runs out", "Losses with no route to scale", f"ARR growth falls below {R['sw_min_growth']}% a year"]]
fills = {(i, 3): RGBColor(0xEA, 0xF2, 0xFC) for i in range(1, 7)}
table(s, LM, 1.8, CW, data, [2.3, 3.3, 3.2, 3.33], row_h=0.66, size=11, fills=fills, header_size=11, aligns=[PP_ALIGN.LEFT]*4)
tb(s, LM, 6.5, CW, 0.45, "Runway and break-even figures come from the monthly cash model (p. 13–14) and assume software ARR grows 60% a year unless stated.",
   size=9.5, color=INK2)

# ---------- 13. Cash trajectories ----------
s = new_slide(f"Cash under each option: A runs out in month {A_neg}, B drifts to near zero, and C bottoms out at "
              f"${OPT['C_60']['trough']:.1f}M before the business turns cash-positive", section=3)
tb(s, LM, 1.75, 8.2, 0.3, "Projected cash balance, $M, months from launch decision (software ARR +60% a year in all three)", size=12, bold=True)
cd = CategoryChartData()
cd.categories = [str(m) for m in range(0, 37)]
for key, name in [("C_60", "C. Software-first"), ("A_60", "A. Launch Parcelbird Now (founders' plan)"), ("B_60", "B. One pilot store")]:
    cd.add_series(name, [12.0] + [round(r["cash"], 2) for r in OPT[key]["rows"]])
gf = s.shapes.add_chart(XL_CHART_TYPE.LINE, Inches(LM), Inches(2.05), Inches(8.2), Inches(4.75), cd)
ch = gf.chart; style_chart(ch, legend=True)
for ser, col in zip(ch.plots[0].series, [BLUE, ORANGE, AQUA]):
    ser.format.line.color.rgb = col; ser.format.line.width = Pt(2.25); ser.smooth = False
    ser.marker.style = None
    from pptx.enum.chart import XL_MARKER_STYLE
    ser.marker.style = XL_MARKER_STYLE.NONE
axis_style(ch.value_axis, fmt='"$"0"M";"−$"0"M"', grid=True); ch.value_axis.minimum_scale = -4; ch.value_axis.maximum_scale = 14
ch.value_axis.major_unit = 2
axis_style(ch.category_axis, grid=False, size=9)
ch.category_axis.tick_label_position = XL_TICK_LABEL_POSITION.LOW
from pptx.oxml.ns import qn
# show every 6th month label
set_skip(ch, 6)
xr = LM + 8.5
data = [["Option", "Runway < 12 mo.", "Lowest cash"],
        ["A. Launch", f"Month {OPT['A_60']['breach']}", f"−${abs(OPT['A_60']['trough']):.1f}M"],
        ["B. Pilot", f"Month {OPT['B_60']['breach']}", f"${OPT['B_60']['trough']:.1f}M"],
        ["C. Software-first", "Never", f"${OPT['C_60']['trough']:.1f}M"]]
table(s, xr, 2.05, CW - 8.5, data, [1.4, 1.2, 1.03], row_h=0.42, size=10.5,
      colors={(1, 1): RED, (1, 2): RED, (2, 1): RED, (3, 1): GREEN}, header_size=10)
tb(s, xr, 3.9, CW - 8.5, 2.9, [
    [("Model assumptions", {"bold": True, "color": NAVY})],
    "Today's burn ($0.4M a month) = software opex − gross profit. Opex is held flat apart from the $0.8M hires (in B and C, not in A).",
    "A: $5.4M capex at one store a month (months 1–9), plus the plan's other $4.1M spread evenly over months 1–18 and nothing after. This is the founders' best case.",
    "B: $0.6M capex, then the median store's −$2.0M a year.",
    "Runway = cash ÷ recurring monthly burn.",
], size=9.5, color=INK2, space_after=3)

# ---------- 14. Software-first path ----------
sw = R["sw"]; mg = R["sw_min_growth"]
s = new_slide(f"Software-first stays within current cash and the runway rule as long as ARR keeps growing at least "
              f"{mg}% a year, just over half today's 60%", section=3)
tb(s, LM, 1.75, 7.6, 0.3, "Software-first projected cash balance, $M, by annual ARR growth rate", size=12, bold=True)
cd = CategoryChartData()
cd.categories = [str(m) for m in range(0, 49)]
from model import sw_path
paths = [(0.60, "60% (today's rate)"), (0.40, "40%"), (mg / 100, f"{mg}% (minimum that keeps 12-month runway)")]
for gr, name in paths:
    p = sw_path(gr, 48)
    cd.add_series(name, [12.0] + [round(r["cash"], 2) for r in p["rows"]])
gf = s.shapes.add_chart(XL_CHART_TYPE.LINE, Inches(LM), Inches(2.05), Inches(7.6), Inches(4.75), cd)
ch = gf.chart; style_chart(ch, legend=True)
for ser, col in zip(ch.plots[0].series, [BLUE, ORANGE, AQUA]):
    ser.format.line.color.rgb = col; ser.format.line.width = Pt(2.25); ser.smooth = False
    ser.marker.style = XL_MARKER_STYLE.NONE
axis_style(ch.value_axis, fmt='"$"0"M"', grid=True); ch.value_axis.minimum_scale = 0; ch.value_axis.maximum_scale = 18
ch.value_axis.major_unit = 2
axis_style(ch.category_axis, grid=False, size=9)
set_skip(ch, 6)
xr = LM + 7.9
mp = R["sw_min_growth_path"]
data = [["ARR growth", "Break-even", "Lowest cash", "Min. runway"],
        ["60%", f"Month {sw[0.6]['breakeven_month']}", f"${sw[0.6]['trough']:.1f}M", f"{sw[0.6]['min_runway']:.0f} mo."],
        ["40%", f"Month {sw[0.4]['breakeven_month']}", f"${sw[0.4]['trough']:.1f}M", f"{sw[0.4]['min_runway']:.0f} mo."],
        [f"{mg}%", f"Month {mp['breakeven_month']}", f"${mp['trough']:.1f}M", f"{mp['min_runway']:.0f} mo."],
        ["25%", "Not by month 48", "Runs out", "Breached"]]
table(s, xr, 2.05, CW - 7.9, data, [0.95, 1.25, 1.0, 1.03], row_h=0.38, size=10.5, header_size=10,
      colors={(4, 1): RED, (4, 2): RED, (4, 3): RED})
tb(s, xr, 4.05, CW - 7.9, 2.8, [
    [("Break-even ARR ", {"bold": True, "color": NAVY}), (f"= opex ÷ 81% = ${R['sw_opex']:.1f}M ÷ 0.81 = ${R['sw_breakeven_arr']:.1f}M, against $4.1M today.", {})],
    [("The pipeline supports the hires: ", {"bold": True, "color": NAVY}),
     (f"the 9 late-stage grocers are worth ${R['late_stage_arr']:.2f}M of ARR; all 37 are worth ${R['pipeline_arr']:.2f}M. "
      f"The $0.8M of hires pays for itself with {R['contracts_to_fund_hires']:.0f} contracts ({R['pipeline_winrate_to_fund_hires']*100:.0f}% of the pipeline).", {})],
    [("What has to be true: ", {"bold": True, "color": NAVY}),
     (f"{mg}% growth means about {R['contracts_for_growth'][mg/100]:.0f} net new contracts in year 1, and 60% means about {R['contracts_for_growth'][0.6]:.0f}. "
      "Costs must also stay flat apart from the hires. The pack does not give churn or win rates, so phase the hires against signed contracts.", {})],
], size=10.5, color=INK2, space_after=5)

# ---------- 15. Risks ----------
s = new_slide("The recommendation survives the main uncertainties: most of them would make a launch worse, "
              "and the risks to software-first can be managed")
data = [["Risk or uncertainty", "Evidence and size", "Effect on the recommendation", "Mitigation or monitoring"],
        ["Rider minimum-pay rules (2 of 3 cities)", f"+20% rider cost = +${R['rider_plus20']['Benchmark median']:.2f}/order at median, +${R['rider_plus20']['Founders\' plan']:.2f} on the plan",
         [("Strengthens \"don't launch\"", {"color": GREEN, "bold": True})], "None needed for C; track the rules for any future re-entry"],
        ["Density in mid-size Midwest cities", "Pop-up 280/day vs median 900; range 400–1,400",
         [("Strengthens \"don't launch\"", {"color": GREEN, "bold": True})], "Trigger 1 (p. 16) tracks density across customer sites"],
        ["Raising AOV could erode the convenience use case", "The plan needs $45 vs $42 best and $31 pop-up",
         [("Strengthens \"don't launch\"", {"color": GREEN, "bold": True})], "Trigger 2 (p. 16)"],
        ["A competitor claims the Midwest first", "Incumbents are retreating (QuickBasket −4 cities) and lose money per order",
         [("Low: first-mover status has not created profit", {"color": INK2, "bold": True})], "Re-entry later can use our software data"],
        ["Software growth slows below the minimum", f"Below {mg}% a year, C breaches the runway rule; 25% runs out of cash",
         [("Main risk to C", {"color": RED, "bold": True})], "Phase hires against signed contracts; review cost base quarterly"],
        ["Software cost base grows faster than assumed", "The model holds opex flat apart from the $0.8M of hires",
         [("Delays C's break-even", {"color": RED, "bold": True})], "Board-approved opex envelope; monthly runway reporting"],
        ["Grocers' own fast delivery competes with our customers", "Several pipeline grocers want store-based fast delivery",
         [("Upside for C", {"color": GREEN, "bold": True})], "Package store-based fast delivery as a product"]]
table(s, LM, 1.8, CW, data, [3.0, 3.55, 2.75, 2.83], row_h=0.6, size=10.5, header_size=11, aligns=[PP_ALIGN.LEFT]*4)

# ---------- 16. Triggers ----------
s = new_slide("What would change our mind: reconsider an operator model only when our customers' sites "
              "show that the economics work and the funding exists")
tb(s, LM, 1.75, CW, 0.4, "Proposed re-entry triggers, reviewed quarterly from the data our software already collects across the 14 customer sites (no extra cost)",
   size=12, color=INK2)
trig = [("1", "Site-level profit is proven",
         "At least one customer site shows positive contribution after site cost for two consecutive quarters.",
         f"Today: none. Best-observed inputs give {money(best['site_level'])}."),
        ("2", "The profit drivers are seen at one site at the same time",
         "AOV ≥ $42 and ≥ 3.0 orders per rider-hour at ≥ 1,050 orders a day, or a service fee that does the same job without losing more than 15% of volume.",
         f"Today: no site has both. Break-even with Zipcart's moves needs about {R['zipcart_breakeven_opd']:,.0f} orders a day."),
        ("3", "Customers stay",
         "Month-3 retention high enough to repay $38 of acquisition cost within 12 months at actual contribution.",
         "Today: 22% at 3.1 orders a month, so payback never happens at the median."),
        ("4", "Funding is ring-fenced",
         "Dedicated capital that leaves the core business with 12 months of runway at all times.",
         "Today: a new round is \"unlikely\"; headroom is $7.2M against a $9.5M plan.")]
for i, (n, h, b, now) in enumerate(trig):
    x = LM + i * (CW / 4)
    w_ = CW / 4 - 0.2
    rect(s, x, 2.3, w_, 4.5, fill=PANEL)
    rect(s, x, 2.3, w_, 0.07, fill=BLUE)
    tb(s, x + 0.15, 2.45, 0.6, 0.6, n, size=26, bold=True, color=BLUE)
    tb(s, x + 0.15, 3.05, w_ - 0.3, 0.75, h, size=13, bold=True)
    tb(s, x + 0.15, 3.8, w_ - 0.3, 1.6, b, size=11)
    hline(s, x + 0.15, 5.5, w_ - 0.3, color=AXIS)
    tb(s, x + 0.15, 5.6, w_ - 0.3, 1.15, now, size=10.5, color=INK2)

# ---------- 17. Decisions & next steps ----------
s = new_slide("We ask the board to make four decisions in January 2027 and review progress in 90 days")
data = [["#", "Decision", "Detail", "Owner", "By"],
        ["1", "Decline the 2027 launch of Parcelbird Now", "Do not commit capex to dark stores and do not extend the pop-up (annualised loss about $1.3M). Keep the pop-up data and cohort learning.", "Board", "Jan 2027"],
        ["2", "Approve the software scale-up", "2 engineers and 2 sales hires ($0.8M a year), released in two tranches tied to signed late-stage contracts (9 grocers, $0.86M ARR)", "CEO", "Q1 2027"],
        ["3", "Build a store-based fast-delivery offer", "Package picking and rider dispatch for grocers who want fast delivery from existing stores; test it with late-stage pipeline accounts", "CTO / Sales", "Q2 2027"],
        ["4", "Adopt re-entry triggers and runway reporting", "Quarterly dashboard of the 4 triggers from customer-site data, plus monthly runway against the 12-month rule", "CFO", "Q1 2027"]]
table(s, LM, 1.8, CW, data, [0.4, 3.2, 6.2, 1.25, 1.08], row_h=0.78, size=11,
      aligns=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER], first_col_bold=True,
      bolds={(i, 1): True for i in range(1, 5)})
rect(s, LM, 5.95, CW, 0.95, fill=PANEL)
tb(s, LM + 0.15, 5.98, CW - 0.3, 0.9,
   [[("90-day checkpoint (April 2027): ", {"bold": True, "color": NAVY}),
     ("late-stage conversions against the 9 grocers, pilot interest in store-based fast delivery, actual ARR growth against the "
      f"{mg}% minimum, and the first trigger dashboard. If growth is tracking below {mg}%, hold the second tranche of hires.", {})]],
   size=11.5, anchor=MSO_ANCHOR.MIDDLE)

# ---------- Appendix A1: unit economics ----------
s = new_slide("Appendix A1: per-order unit economics by scenario, with calculations", source=SRC)
order = ["Pop-up test", "Benchmark median", "Best observed", "Founders' plan"]
lines = ["Goods margin (27% of AOV)", "Delivery fee (net)", "Promotions", "Picking & packing", "Rider cost", "Payment & packaging"]
calc = {"Goods margin (27% of AOV)": "AOV × 27%", "Delivery fee (net)": "$1.99, net of payment cost",
        "Promotions": "AOV × promo %", "Picking & packing": "$3.10 per order", "Rider cost": "$17.75 ÷ orders per rider-hour",
        "Payment & packaging": "$1.30 per order"}
data = [["Line item ($ per order)", "Calculation", "Pop-up", "Median", "Best obs.", "Plan"]]
for ln in lines:
    data.append([ln, calc[ln]] + [money(U[k]["lines"][ln]) for k in order])
data.append(["Contribution before site fixed cost", "Sum of the above"] + [money(U[k]["variable"]) for k in order])
data.append(["Site fixed cost per order", "Annual fixed ÷ (orders/day × 365)"] + [money(U[k]["site_fixed"]) for k in order])
data.append(["Contribution after site fixed cost", ""] + [money(U[k]["site_level"]) for k in order])
data.append(["Per store per year", "× orders/day × 365"] + [mm(U[k]["annual_site"]) for k in order])
data.append(["Break-even AOV (other inputs held)", "Solve contribution after site cost = 0"] + [f"${R['breakeven_aov'][k]:.0f}" for k in order])
bolds = {(7, j): True for j in range(6)}; bolds.update({(9, j): True for j in range(6)})
table(s, LM, 1.75, CW, data, [3.4, 3.53, 1.3, 1.3, 1.3, 1.3], row_h=0.38, size=10.5, bolds=bolds, aligns=[PP_ALIGN.LEFT, PP_ALIGN.LEFT] + [PP_ALIGN.RIGHT]*4)
tb(s, LM, 6.4, CW, 0.55, "Inputs: Table 3 and section 7 of the briefing pack. Pop-up site fixed cost is $650k a year; all others are $1.15M. "
   "Promotions are treated as a cost on AOV and goods margin as 27% of AOV before promotions. HQ overhead, capex and marketing are excluded.",
   size=9.5, color=INK2)

# ---------- Appendix A2: assumptions & judgement calls ----------
s = new_slide("Appendix A2: judgement calls made where the briefing pack is ambiguous", source=SRC)
data = [["Topic", "Ambiguity", "Choice made and why", "Does it change the answer?"],
        ["\"Contribution per order\"", "The founders and incumbents don't define it", "We show it both before and after site fixed cost", "No: the median is negative on both"],
        ["Founders' $9.5M", "Unclear whether it includes the core $0.4M a month of burn", "We show both readings: on top of core burn (cash out in month 13) and all-in ($2.5M left at month 18)", "No: both breach the 12-month rule"],
        ["Runway definition", "\"12 months of runway at all times\"", "Cash ÷ recurring monthly burn; one-off capex excluded from the burn (lenient)", "No"],
        ["Software cost base", "The pack gives burn, not opex", "Opex = 81% × ARR + burn; held flat apart from the $0.8M hires", "Optimistic for C; hence the 34% minimum and phased hires"],
        ["Pilot option (B)", "Not in the pack", "One permanent store at median economics, $0.6M capex", "No"],
        ["GMV vs revenue", "Operators' revenue is roughly their GMV", "Used only for the scale sanity check (p. 7)", "No"],
        ["Pop-up ramp", "Only the average and weekly growth are given", "Assumed constant 18% weekly compounding over 6 weeks", "No"]]
table(s, LM, 1.75, CW, data, [2.1, 3.3, 4.43, 2.3], row_h=0.6, size=10.5, aligns=[PP_ALIGN.LEFT]*4)

prs.save("deliverable/Parcelbird_Now_board_deck.pptx")
print("saved; slides:", len(prs.slides))
print("\n".join(FIT_WARN) if FIT_WARN else "no fit warnings")
