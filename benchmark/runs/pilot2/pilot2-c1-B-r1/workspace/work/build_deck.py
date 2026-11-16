"""Builds deliverable/Onsoo_US_entry_board_deck.pptx from work/model_out.json (run model.py first)."""
import json, os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION, XL_MARKER_STYLE, XL_TICK_LABEL_POSITION
from pptx.enum.dml import MSO_LINE
from pptx.oxml.ns import qn
from lxml import etree

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
M = json.load(open(os.path.join(HERE, "model_out.json")))
C = {k: v["rows"] for k, v in M["cases"].items()}
S = {k: v["summary"] for k, v in M["cases"].items()}
J = M["japan"]["rows"]

def rgb(h): return RGBColor.from_string(h.lstrip("#"))
NAVY, INK, INK2, MUTED, RULE = "#14213d", "#1f1f1f", "#52514e", "#8a8984", "#d9d8d3"
BLUE, ORANGE, AQUA, GRAY, LGRAY = "#2a78d6", "#eb6834", "#1baf7a", "#a3a29c", "#e6e5e0"
RED = "#e34948"
TINT_G, TINT_A, TINT_R, TINT_B = "#e3f4e3", "#fdf1d6", "#fbe3e3", "#eaf1fb"
FONT = "Calibri"
YEARS = [2027, 2028, 2029, 2030]

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]
SECTIONS = ["1  Enter in 2027", "2  Lead with Amazon", "3  Launch with conditions"]
page = [0]


def _run(p, text, size=12, bold=False, color=INK, italic=False):
    r = p.add_run(); r.text = text
    f = r.font; f.size = Pt(size); f.bold = bold; f.italic = italic; f.name = FONT; f.color.rgb = rgb(color)
    return r


def _bullet(p, level=0, char="•"):
    pPr = p._p.get_or_add_pPr()
    mar = 0.18 + 0.2 * level
    pPr.set("marL", str(int(Inches(mar)))); pPr.set("indent", str(-int(Inches(0.16))))
    for tag in ("a:buNone", "a:buChar", "a:buAutoNum"):
        for e in pPr.findall(qn(tag)): pPr.remove(e)
    bu = etree.SubElement(pPr, qn("a:buChar")); bu.set("char", char)


def text(slide, x, y, w, h, paras, anchor=MSO_ANCHOR.TOP, margin=0.05, fill=None, line=None):
    """paras: list of dicts or strings. dict keys: runs=[(text, opts)], size, bold, color, bullet, level, align, space."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if fill:
        tb.fill.solid(); tb.fill.fore_color.rgb = rgb(fill)
    if line:
        tb.line.color.rgb = rgb(line); tb.line.width = Pt(0.75)
    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    for side in ("left", "right", "top", "bottom"):
        setattr(tf, f"margin_{side}", Inches(margin if side in ("top", "bottom") else margin + 0.03))
    first = True
    for para in paras:
        if isinstance(para, str): para = dict(runs=[(para, {})])
        p = tf.paragraphs[0] if first else tf.add_paragraph(); first = False
        size = para.get("size", 12)
        for t, o in para["runs"]:
            _run(p, t, o.get("size", size), o.get("bold", para.get("bold", False)), o.get("color", para.get("color", INK)),
                 o.get("italic", False))
        if para.get("bullet"): _bullet(p, para.get("level", 0), para.get("char", "•"))
        p.alignment = para.get("align", PP_ALIGN.LEFT)
        p.space_after = Pt(para.get("space", 4))
        p.line_spacing = para.get("ls", 1.0)
    return tb


def P(s, size=12, bold=False, color=INK, bullet=False, level=0, space=4, align=PP_ALIGN.LEFT):
    """Parse **bold** markup into runs."""
    runs, parts = [], s.split("**")
    for i, part in enumerate(parts):
        if part: runs.append((part, {"bold": (i % 2 == 1) or bold}))
    return dict(runs=runs, size=size, color=color, bullet=bullet, level=level, space=space, align=align)


def rect(slide, x, y, w, h, fill, line=None, shape=MSO_SHAPE.RECTANGLE):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid(); s.fill.fore_color.rgb = rgb(fill)
    if line: s.line.color.rgb = rgb(line); s.line.width = Pt(0.75)
    else: s.line.fill.background()
    s.shadow.inherit = False
    return s


def new_slide(title, section=None, source=None):
    s = prs.slides.add_slide(BLANK); page[0] += 1
    if section is not None:
        x = 0.5
        for i, name in enumerate(SECTIONS):
            on = i == section
            text(s, x, 0.12, 2.3, 0.28, [P(name, 9, bold=on, color=NAVY if on else MUTED)], margin=0)
            if on: rect(s, x + 0.03, 0.38, 1.9, 0.03, BLUE)
            x += 2.35
    text(s, 0.5, 0.45, 12.3, 0.95, [P(title, 20, bold=True, color=NAVY)], anchor=MSO_ANCHOR.MIDDLE, margin=0)
    rect(s, 0.5, 1.42, 12.33, 0.015, RULE)
    if source:
        text(s, 0.5, 6.98, 11.3, 0.4, [P(source, 8.5, color=MUTED)], margin=0, anchor=MSO_ANCHOR.BOTTOM)
    text(s, 12.2, 7.05, 0.65, 0.3, [P(str(page[0]), 9, color=MUTED, align=PP_ALIGN.RIGHT)], margin=0)
    return s


def callout(slide, x, y, w, h, paras, accent=BLUE, fill=TINT_B):
    rect(slide, x, y, w, h, fill)
    rect(slide, x, y, 0.06, h, accent)
    return text(slide, x + 0.12, y, w - 0.15, h, paras, anchor=MSO_ANCHOR.MIDDLE, margin=0.06)


def table(slide, data, x, y, w, col_w, row_h=0.32, size=10.5, header_fill=NAVY, fills=None, bold_first_col=False,
          aligns=None, header_size=None, header=True):
    rows, cols = len(data), len(data[0])
    gt = slide.shapes.add_table(rows, cols, Inches(x), Inches(y), Inches(w), Inches(row_h * rows))
    tbl = gt.table
    tblPr = tbl._tbl.tblPr
    style = tblPr.find(qn("a:tableStyleId"))
    if style is None: style = etree.SubElement(tblPr, qn("a:tableStyleId"))
    style.text = "{5940675A-B579-460E-94D1-54222C63F5DA}"  # No style, table grid -> we restyle
    for j, cw in enumerate(col_w): tbl.columns[j].width = Inches(cw)
    for i in range(rows):
        tbl.rows[i].height = Inches(row_h)
        for j in range(cols):
            cell = tbl.cell(i, j); val = data[i][j]
            cell.margin_left = cell.margin_right = Inches(0.06); cell.margin_top = cell.margin_bottom = Inches(0.03)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = cell.text_frame; tf.word_wrap = True
            p = tf.paragraphs[0]
            is_h = i == 0 and header
            parts = str(val).split("**")
            for k, part in enumerate(parts):
                if part:
                    _run(p, part, (header_size or size) if is_h else size,
                         bold=is_h or (k % 2 == 1) or (bold_first_col and j == 0),
                         color="#ffffff" if is_h and header_fill == NAVY else (NAVY if is_h else INK))
            if aligns: p.alignment = aligns[j]
            f = header_fill if is_h else (fills[i][j] if fills and fills[i][j] else ("#ffffff"))
            cell.fill.solid(); cell.fill.fore_color.rgb = rgb(f)
            # borders: thin bottom rule only
            tcPr = cell._tc.get_or_add_tcPr()
            for idx, (tag, show) in enumerate((("a:lnL", False), ("a:lnR", False), ("a:lnT", False), ("a:lnB", True))):
                ln = etree.Element(qn(tag)); tcPr.insert(idx, ln)  # lines must precede the fill in tcPr
                ln.set("w", str(int(Pt(0.75))) if show else "0")
                if show:
                    sf = etree.SubElement(ln, qn("a:solidFill")); c = etree.SubElement(sf, qn("a:srgbClr")); c.set("val", RULE.lstrip("#"))
                else:
                    etree.SubElement(ln, qn("a:noFill"))
    return tbl


def set_inner(ch, x, y, w, h):
    """Fix the inner plot area (fractions of the chart frame) so overlay reference lines land exactly."""
    plotArea = ch._chartSpace.chart.plotArea
    old = plotArea.find(qn("c:layout"))
    if old is not None: plotArea.remove(old)
    lay = etree.Element(qn("c:layout")); plotArea.insert(0, lay)
    ml = etree.SubElement(lay, qn("c:manualLayout"))
    for tag, val in (("c:layoutTarget", "inner"), ("c:xMode", "edge"), ("c:yMode", "edge"),
                     ("c:x", x), ("c:y", y), ("c:w", w), ("c:h", h)):
        e = etree.SubElement(ml, qn(tag)); e.set("val", str(val))


def hline(slide, fx, fy, fw, fh, inner, vmin, vmax, v, color, label=None, label_side="left", above=True):
    """Horizontal reference line at value v on a column chart with inner layout `inner`=(x,y,w,h)."""
    ix, iy, iw, ih = inner
    top, bot = fy + iy * fh, fy + (iy + ih) * fh
    yy = bot - (bot - top) * (v - vmin) / (vmax - vmin)
    x0, x1 = fx + ix * fw, fx + (ix + iw) * fw
    ln = slide.shapes.add_connector(1, Inches(x0), Inches(yy), Inches(x1), Inches(yy))
    ln.line.color.rgb = rgb(color); ln.line.width = Pt(1.5); ln.line.dash_style = MSO_LINE.DASH
    if label:
        lx = x0 + 0.05 if label_side == "left" else x1 - 3.05
        text(slide, lx, yy - 0.25 if above else yy + 0.02, 3.0, 0.24,
             [P(label, 9, bold=True, align=PP_ALIGN.LEFT if label_side == "left" else PP_ALIGN.RIGHT)], margin=0)
    return yy


def style_chart(ch, legend=True, size=10, legend_pos=XL_LEGEND_POSITION.BOTTOM):
    ch.font.size = Pt(size); ch.font.name = FONT; ch.font.color.rgb = rgb(INK2)
    ch.has_legend = legend
    if legend:
        ch.legend.position = legend_pos; ch.legend.include_in_layout = False
        ch.legend.font.size = Pt(size); ch.legend.font.name = FONT
    try:
        va = ch.value_axis
        va.has_major_gridlines = True
        va.major_gridlines.format.line.color.rgb = rgb("#ebeae6"); va.major_gridlines.format.line.width = Pt(0.5)
        va.format.line.fill.background()
        va.tick_labels.font.size = Pt(size - 0.5); va.tick_labels.font.color.rgb = rgb(INK2)
        ca = ch.category_axis
        ca.format.line.color.rgb = rgb(GRAY); ca.format.line.width = Pt(0.75)
        ca.tick_labels.font.size = Pt(size); ca.tick_labels.font.color.rgb = rgb(INK2)
        ca.has_major_gridlines = False
    except Exception:
        pass


def color_series_line(ser, color, width=2.25, dash=None, marker=True):
    ser.format.line.color.rgb = rgb(color); ser.format.line.width = Pt(width)
    ser.smooth = False
    if dash: ser.format.line.dash_style = dash
    if marker:
        ser.marker.style = XL_MARKER_STYLE.CIRCLE; ser.marker.size = 7
        ser.marker.format.fill.solid(); ser.marker.format.fill.fore_color.rgb = rgb(color)
        ser.marker.format.line.color.rgb = rgb("#ffffff"); ser.marker.format.line.width = Pt(1.5)
    else:
        ser.marker.style = XL_MARKER_STYLE.NONE


def point_label(pt, txt, pos=XL_LABEL_POSITION.RIGHT, size=10, bold=True, color=INK):
    dl = pt.data_label; dl.has_text_frame = True
    dl.text_frame.text = txt
    for p in dl.text_frame.paragraphs:
        for r in p.runs:
            r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = rgb(color); r.font.name = FONT
    dl.position = pos


def fmt_m(v, plus=True, d=1):
    s = f"{abs(v):.{d}f}"
    sign = "–" if v < 0 else ("+" if plus and v > 0 else "")
    return f"{sign}${s}M"

PASS, FAIL, PART = "✓", "✗", "◐"

# =====================================================================================
# 1. Title
s = prs.slides.add_slide(BLANK); page[0] += 1
rect(s, 0, 0, 13.333, 7.5, NAVY)
rect(s, 0.8, 2.15, 0.08, 2.2, BLUE)
text(s, 1.05, 1.95, 11, 1.0, [P("Onsoo Botanicals · US market entry", 34, bold=True, color="#ffffff")], margin=0)
text(s, 1.05, 2.95, 11, 1.4, [P("Should Onsoo enter the US market in 2027, and if so, by which route?", 20, color="#dfe6f2"),
                              P("Recommendation: yes, with an Amazon-led launch run as a gated build", 20, bold=True, color="#ffffff")], margin=0)
text(s, 1.05, 5.3, 11, 1.0, [P("Discussion document for CEO Park Ji-won and the Board · for decision at the March 2027 board meeting", 13, color="#dfe6f2"),
                             P("Prepared November 2026 using only the planning team's briefing pack (synthetic benchmark data; all figures fictional)", 11, color="#aab6cc")], margin=0)

# =====================================================================================
# 2. Executive summary
a, a32, b, jj = S["A_plan"], S["A_bench32"], S["B_plan"], M["japan"]["summary"]
s = new_slide("Onsoo should enter the US in 2027 with an Amazon-led launch: it is the only route that fits the board's financial rules, but it needs gates because payback depends on ad cost",
              source="Source: Onsoo briefing pack (Tables 1–9, survey Sept 2026); team analysis. Cash figures are pre-tax, cumulative US cash flow 2027–2030 incl. inventory.")
blocks = [
    ("1", "Enter the US in 2027, rather than scale up Japan",
     ["US K-beauty skincare is **$3.6B, growing 17% a year** (category: 5%), and **41% of it sells on Amazon**.",
      "The pilot shows demand: **64,800 units in six months at 4.5 stars**, a $4.0M annualised run-rate, and 29% repeat (benchmark 31%).",
      "Amazon-led gives **$26.4M of US revenue in 2030 vs $7.0M** of extra revenue from the Japan scale-up, with peak cash of only $1.9–3.2M."]),
    ("2", "Lead with Amazon, not a 600-door specialty-retail launch",
     ["Amazon-led passes all three financial tests: **peak cash –$1.9M** (cap $18M), **payback in 2030**, group margin never below 9.5%.",
      "Retail-led **fails all three on its own numbers**: peak cash –$20.8M, no payback by 2030, group margin 4.5% in 2027.",
      "Its key inputs do not hold: at Onsoo's 4% awareness, newcomers sell a **median 2.6 units/door/week** (plan: 4.5; delisting below 4.0), and the 1.3× halo rests on a correlation."]),
    ("3", "Launch with conditions, because three parts of the CEO's plan need changing",
     ["Payback holds only if **ACoS ≤ 28.6%**. At the 32% benchmark for brands this size, cash is still **–$2.3M at end-2030**, so set a 28% ACoS ceiling and hold a gate in March 2028.",
      "Retail from 2029 at the planned cost would break payback and the margin floor. Enter retail **after payback and above 20% awareness** (not 15%).",
      "**No modeled route reaches $40M by 2030** inside the cash cap and payback rule. Keep the rules and move the $40M date to about 2032."]),
]
y = 1.62
for num, head, bullets in blocks:
    rect(s, 0.5, y, 0.5, 0.5, NAVY, shape=MSO_SHAPE.OVAL)
    text(s, 0.5, y, 0.5, 0.5, [P(num, 16, bold=True, color="#ffffff", align=PP_ALIGN.CENTER)], anchor=MSO_ANCHOR.MIDDLE, margin=0)
    text(s, 1.15, y - 0.04, 11.6, 0.4, [P(head, 14.5, bold=True, color=NAVY)], margin=0)
    text(s, 1.15, y + 0.33, 11.6, 1.15, [P(t, 11.5, bullet=True, space=2) for t in bullets], margin=0)
    y += 1.53
callout(s, 0.5, 6.25, 12.33, 0.62, [P("**Decision for March 2027:** approve the Amazon-led launch with a $4M cash envelope, a 28% ACoS ceiling and a gate in March 2028; defer specialty retail; move the $40M ambition to about 2032.", 11.5)])

# =====================================================================================
# 3. Hypothesis test
s = new_slide("We tested the CEO's starting hypothesis against seven conditions: the Amazon-first route holds, but payback, retail timing and the $40M date need changing",
              source="Starting hypothesis (CEO): \"Launch in the US in 2027 through Amazon, then add specialty beauty retail from 2029 once Amazon sales pass $10M and aided awareness passes 15%.\"")
hdr = ["", "What would have to be true", "What the evidence says", "Verdict"]
rows = [
    ["Market", "US K-beauty skincare is large, growing and bought mainly on Amazon",
     "$3.6B in 2025, +17%/yr; Amazon 41% of sales; 61% of K-beauty buyers buy there most often", f"{PASS} Holds"],
    ["Product", "Onsoo's products win with US Amazon shoppers",
     "4.5 stars from 2,140 reviews; units +89% Jan→Jun; repeat 29% vs 31% benchmark; 6% complain of Korean-only labels", f"{PASS} Holds, after a label fix"],
    ["Use of 2027", "The US is a better use of the single 2027 launch slot than Japan",
     "2030 revenue $26.4M (US) vs $7.0M (Japan); both inside the constraints on plan; Japan grows 1.5%/yr", f"{PASS} Holds"],
    ["Route", "Starting on Amazon beats starting in 600 specialty doors",
     "Retail-led breaks the cash cap, payback and margin floor; 4.5 units/door/week is unsupported at 4% awareness", f"{PASS} Holds"],
    ["Economics", "Amazon-led meets the cash cap, payback and margin floor",
     "Cap and margin hold in every case tested; payback only if ACoS ≤ 28.6% (benchmark at this scale 32%)", f"{PART} Partly: payback at risk"],
    ["Retail timing", "Retail from 2029 at $10M sales and 15% awareness works",
     "At 10–20% awareness the median is 3.5 units/door/week (< 4.0 delisting bar); 2029 retail takes cash to –$11.8M", f"{FAIL} Does not hold"],
    ["Ambition", "The route gets Onsoo to $40M of US revenue by 2030",
     "Amazon-led reaches $26.4M; only retail-led gets close ($37.6M), and it breaks the cash cap", f"{FAIL} Does not hold"],
]
vf = {PASS: TINT_G, PART: TINT_A, FAIL: TINT_R}
fills = [[None] * 4] + [[None, None, None, vf[r[3][0]]] for r in rows]
table(s, [hdr] + rows, 0.5, 1.6, 12.33, [1.35, 3.6, 5.28, 2.1], row_h=0.56, size=10.5, fills=fills, bold_first_col=True)
callout(s, 0.5, 6.18, 12.33, 0.68, [P("**Revised answer:** enter via Amazon in 2027, run against a 28% ACoS ceiling with a gate in March 2028; add specialty retail only after payback and above 20% awareness; move the $40M ambition to about 2032.", 12)])

# =====================================================================================
# 4. Market
s = new_slide("US K-beauty skincare is a $3.6B segment growing 17% a year, over three times the category's rate, and 41% of it is bought on Amazon",
              section=0, source="Source: briefing pack Table 1 (US facial skincare sales), Table 2 (K-beauty channel shares 2025), customer survey Sept 2026 (n=1,200 US women 18–44). CAGR = (2025/2021)^(1/4) – 1.")
cd = CategoryChartData(); cd.categories = ["2021", "2022", "2023", "2024", "2025"]
kb = [1.9, 2.3, 2.7, 3.1, 3.6]; tot = [20.1, 21.3, 22.6, 23.5, 24.5]
cd.add_series("K-beauty brands", kb); cd.add_series("Other facial skincare", [round(t - k, 1) for t, k in zip(tot, kb)])
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_STACKED, Inches(0.5), Inches(1.95), Inches(5.6), Inches(4.0), cd); ch = gf.chart
style_chart(ch); ch.plots[0].gap_width = 70; ch.plots[0].overlap = 100
ch.series[0].format.fill.solid(); ch.series[0].format.fill.fore_color.rgb = rgb(BLUE)
ch.series[1].format.fill.solid(); ch.series[1].format.fill.fore_color.rgb = rgb(LGRAY)
ch.value_axis.maximum_scale = 28; ch.value_axis.tick_labels.number_format = '"$"0"B"'; ch.value_axis.tick_labels.number_format_is_linked = False
for i, k in enumerate(kb):
    point_label(ch.series[0].points[i], f"${k}B", XL_LABEL_POSITION.INSIDE_END, 9.5, color="#ffffff")
for i, t in enumerate(tot):
    point_label(ch.series[1].points[i], f"${t}B", XL_LABEL_POSITION.INSIDE_END, 9.5, bold=False, color=INK2)
text(s, 0.5, 1.55, 5.6, 0.4, [P("US facial skincare sales, $B: K-beauty share rose from 9.5% to 14.7%", 11.5, bold=True, color=NAVY)], margin=0)
mk = M["market"]
text(s, 0.6, 5.95, 5.5, 0.5, [P(f"CAGR 2021–25: K-beauty **+{mk['kb_cagr']*100:.0f}%** · all facial skincare +{mk['total_cagr']*100:.0f}% · non-K-beauty +{mk['nonkb_cagr']*100:.1f}%", 10.5, color=INK2)], margin=0)
# channel bars
cd2 = CategoryChartData(); ch_names = ["Amazon", "Specialty beauty", "Mass retail", "Brand DTC", "Other"]; ch_vals = [0.41, 0.27, 0.14, 0.12, 0.06]
cd2.categories = list(reversed(ch_names)); cd2.add_series("Share of 2025 K-beauty skincare sales", list(reversed(ch_vals)))
gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(6.5), Inches(1.95), Inches(3.4), Inches(3.0), cd2); ch = gf.chart
style_chart(ch, legend=False); ch.plots[0].gap_width = 55
ch.value_axis.visible = False; ch.value_axis.has_major_gridlines = False; ch.value_axis.maximum_scale = 0.5
ser = ch.series[0]
for i in range(5):
    pt = ser.points[i]; pt.format.fill.solid(); pt.format.fill.fore_color.rgb = rgb(BLUE if i == 4 else GRAY)
    point_label(pt, f"{list(reversed(ch_vals))[i]*100:.0f}%", XL_LABEL_POSITION.OUTSIDE_END, 10, bold=(i == 4))
text(s, 6.5, 1.55, 3.5, 0.4, [P("Where K-beauty skincare was bought, 2025", 11.5, bold=True, color=NAVY)], margin=0)
text(s, 10.15, 1.55, 2.7, 4.6, [
    P("What K-beauty buyers told us", 11.5, bold=True, color=NAVY, space=6),
    P("**61%** buy K-beauty on Amazon most often; **22%** at specialty retail", 11, bullet=True, space=6),
    P("**38%** discovered their last new brand on TikTok; **17%** in a store", 11, bullet=True, space=6),
    P("**52%** cite \"price compared with US brands\" as a reason to try K-beauty", 11, bullet=True, space=6),
    P("Amazon K-beauty skincare ≈ 41% × $3.6B = **$1.48B**; Option A's 2030 revenue is 1.8% of that", 11, bullet=True, space=6)], margin=0)
callout(s, 6.5, 5.1, 6.33, 0.95, [P("**Use $3.6B, not $5.2B.** The trade-press figure of \"$5.2B US K-beauty\" includes makeup and hair care. It overstates Onsoo's addressable market by about 45%.", 10.5)], accent=GRAY, fill="#f3f2ee")
callout(s, 0.5, 6.35, 12.33, 0.55, [P("**So what:** the market is big enough, growing fast, and Amazon-centric. That favours an Amazon-led entry.", 11.5)])

# =====================================================================================
# 5. Pilot
pl = M["pilot"]
s = new_slide("The Amazon pilot shows real demand: monthly sales nearly doubled in six months at 4.5 stars, and repeat purchase is close to the US benchmark",
              section=0, source="Source: briefing pack §6 (pilot Jan–Jun 2026, three SKUs, cross-border seller). Run-rate = June units × 12 × $24. Growth needed = constant monthly growth from June 2026 that delivers 300k units in calendar 2027 with today's SKUs.")
cd = CategoryChartData(); cd.categories = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
units = [7400, 8600, 10100, 11800, 12900, 14000]; cd.add_series("Pilot units sold per month", units)
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.5), Inches(1.95), Inches(6.2), Inches(3.55), cd); ch = gf.chart
style_chart(ch, legend=False); ch.plots[0].gap_width = 60
ch.series[0].format.fill.solid(); ch.series[0].format.fill.fore_color.rgb = rgb(BLUE)
ch.value_axis.tick_labels.number_format = '#,##0'; ch.value_axis.tick_labels.number_format_is_linked = False; ch.value_axis.maximum_scale = 16000
mom = [None] + pl["mom"]
for i, u in enumerate(units):
    point_label(ch.series[0].points[i], f"{u:,}" + (f"\n+{mom[i]*100:.0f}%" if mom[i] else ""), XL_LABEL_POSITION.OUTSIDE_END, 9.5, bold=False)
text(s, 0.5, 1.55, 6.2, 0.4, [P("Pilot units per month, 2026 (labels: units and month-on-month growth)", 11.5, bold=True, color=NAVY)], margin=0)
text(s, 0.6, 5.55, 6.1, 0.7, [P("Growth slowed from 16–17% a month (Feb–Apr) to 8–9% (May–Jun). The average was 13.6% a month.", 10.5, color=INK2)], margin=0)
tiles = [("64,800", "units sold Jan–Jun", "$1.56M of sales at $24.00"),
         ("$4.0M", "annualised run-rate", "June: 14,000 units × 12 × $24"),
         ("4.5 / 5", "stars, from 2,140 reviews", "Top complaint: Korean-only labels (6% of reviews)"),
         ("29%", "90-day repeat", "Benchmark 31% (first-year US brands); Korea 48%"),
         ("28%", "ACoS in the pilot", "On a small budget; the plan assumes 25%")]
tx, ty = 7.0, 1.6
for i, (big, lab, sub) in enumerate(tiles):
    xx = tx + (i % 2) * 2.95; yy = ty + (i // 2) * 1.25
    rect(s, xx, yy, 2.8, 1.12, "#f5f7fb")
    text(s, xx + 0.1, yy + 0.03, 2.6, 0.5, [P(big, 22, bold=True, color=NAVY)], margin=0)
    text(s, xx + 0.1, yy + 0.5, 2.65, 0.6, [P(lab, 10.5, bold=True), P(sub, 9.5, color=INK2)], margin=0)
text(s, 9.95, 4.1, 2.8, 1.12, [P("**2027 plan needs 300k units** = 1.8× the June run-rate (168k). From today's 3 SKUs alone that takes ~4.6% monthly growth through 2027. The four new SKUs add headroom.", 10, color=INK)], margin=0.04, fill="#f5f7fb")
callout(s, 0.5, 6.3, 12.33, 0.6, [P("**So what:** product-market fit is good enough to scale. Two watch-points: fix the US labels before scaling, and bring repeat from 29% up to the 31% benchmark as the range grows.", 11.5)])

# =====================================================================================
# 6. US vs Japan
s = new_slide("An Amazon-led US launch is a better use of the single 2027 launch slot than the Japan scale-up: about four times the 2030 revenue for a small, capped downside",
              section=0, source="Source: briefing pack Tables 5–7, group context; team model. Japan: incremental figures as given (no working-capital data provided). Stall case: Amazon flat at 200k units ($4.8M) a year at 32% ACoS.")
hdr = ["Metric (US cash = cumulative, pre-tax, incl. inventory)", "A · Amazon-led\nplan (25% ACoS)", "A · Amazon-led\nbenchmark (32% ACoS)", "J · Japan scale-up"]
J30 = J[-1]
rows = [
    ["Revenue in 2030", "$26.4M", "$26.4M", "$7.0M (incremental)"],
    ["Peak cumulative cash need, 2027–30", fmt_m(a["peak"]), fmt_m(a32["peak"]), fmt_m(jj["peak"], d=2)],
    ["Cumulative cash at end-2030", fmt_m(a["cum2030"]), fmt_m(a32["cum2030"]), fmt_m(jj["cum2030"])],
    ["Cash flow in 2030 (run-rate)", fmt_m(a["cf2030"]), fmt_m(a32["cf2030"]), fmt_m(J30["cf"])],
    ["Lowest group operating margin, 2027–30", f"{a['min_group_margin']*100:.1f}%", f"{a32['min_group_margin']*100:.1f}%", f"{jj['min_group_margin']*100:.1f}%"],
    ["Board tests met (cap / payback / margin)", f"{PASS} / {PASS} / {PASS}", f"{PASS} / {FAIL} / {PASS}", f"{PASS} / {PASS} / {PASS}"],
    ["Market growth; Onsoo's position", "+17%/yr K-beauty; new market", "+17%/yr K-beauty; new market", "+1.5%/yr; already 3.1% share"],
    ["Worst case tested", "Sales stall: –$7.1M by 2030, or about –$3M if stopped at the March 2028 gate", "", "Small; not modeled in the pack"],
]
tb = table(s, [hdr] + rows, 0.5, 1.6, 8.3, [2.9, 1.8, 1.8, 1.8], row_h=0.5, size=10.5, bold_first_col=True,
           aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER],
           fills=[[None]*4] + [[None, TINT_B, None, None]]*8)
tb.cell(8, 1).merge(tb.cell(8, 2))
text(s, 9.1, 1.6, 3.75, 4.5, [
    P("Why the US wins the 2027 slot", 12.5, bold=True, color=NAVY, space=6),
    P("**Scale:** the US adds about 4× the revenue Japan does by 2030, and is still growing 29% a year in 2030.", 11, bullet=True, space=6),
    P("**Bounded downside:** even the worst US case tested (–$7.1M) uses under 40% of the $18M cap.", 11, bullet=True, space=6),
    P("**Timing:** the pilot has momentum and 2,140 reviews. Waiting a year cedes a market growing 17% a year.", 11, bullet=True, space=6),
    P("The trade-off", 12.5, bold=True, color=NAVY, space=6),
    P("Japan is the safer bet for 2030 cash (+$1.8M vs –$2.3M at benchmark ACoS). We give that up for the only option that moves the US ambition forward.", 11, bullet=True, space=6),
    P("The bandwidth limit covers 2027 only, so we recommend looking at the Japan scale-up again for 2028.", 11, bullet=True, space=6)], margin=0)
callout(s, 0.5, 6.3, 12.33, 0.6, [P("**So what:** use 2027 for the US. Japan's extra cash does not make up for losing a year in a market growing 17% a year, and the US downside is small.", 11.5)])

# =====================================================================================
# 7. Unit economics
u = M["unit"]
s = new_slide("Per unit, retail earns more than Amazon ($7.55 vs $4.73), but the retail route adds $7.5M a year of fixed cost that its unit margin cannot cover",
              section=1, source="Source: briefing pack Table 4 (Rice Ferment Barrier Cream, applied to all SKUs as the planning team does), Table 6. Contribution before fixed costs; duty at 15% of ex-factory cost.")
hdr = ["Per unit, US$", "Amazon", "Specialty retail"]
rows = [["Price Onsoo receives", "24.00", "14.00 (50% of $28 shelf)"],
        ["Amazon referral fee (15%)", "–3.60", "—"], ["Amazon FBA fee", "–5.10", "—"],
        ["Ex-factory product cost", "–3.50", "–3.50"], ["Freight to US warehouse / retailer DC", "–0.55", "–0.75"],
        ["Import duty (15% of ex-factory)", "–0.53", "–0.53"], ["Co-op marketing (8%) + returns (4%) of wholesale", "—", "–1.68"],
        ["**Contribution before advertising**", "**10.73**", "**7.55**"],
        ["Advertising at 25% ACoS (plan) / 32% (benchmark)", "–6.00 / –7.68", "in fixed budget"],
        ["**Contribution per unit**", f"**{u['amazon_25']+1e-9:.2f} / {u['amazon_32']+1e-9:.2f}**", f"**{u['retail']+1e-9:.2f}**"]]
table(s, [hdr] + rows, 0.5, 1.6, 6.9, [3.6, 1.5, 1.8], row_h=0.38, size=10.5,
      aligns=[PP_ALIGN.LEFT, PP_ALIGN.RIGHT, PP_ALIGN.RIGHT], fills=[[None]*3] + [[None]*3]*7 + [[LGRAY]*3, [None]*3, [TINT_B]*3])
text(s, 7.75, 1.6, 5.1, 4.6, [
    P("Retail's own break-even, at the planned cost base", 12.5, bold=True, color=NAVY, space=6),
    P("Retail-only fixed cost: $6.0M national marketing + $1.5M field team = **$7.5M a year**.", 11, bullet=True, space=4),
    P(f"Units needed = $7.5M ÷ $7.545 = **994k a year**. Across 600 doors that is ÷ (600 × 52) = **{M['retail_breakeven_upw_600']:.0f} units/door/week**.", 11, bullet=True, space=4),
    P(f"The plan assumes 4.5; the evidence for Onsoo suggests 2.6. At 4.5, retail would need **≈{M['retail_breakeven_doors_45']:,.0f} doors** to cover its costs.", 11, bullet=True, space=4),
    P(f"At 4.5 units/door/week, 600 doors sell 140k units: **$2.0M** of wholesale revenue against **$7.5M** of fixed cost.", 11, bullet=True, space=10),
    P("Amazon's sensitivity is advertising", 12.5, bold=True, color=NAVY, space=6),
    P("Each ACoS point costs $0.24 a unit, or ≈ $0.67M over the 2.81M units planned for 2027–30.", 11, bullet=True, space=4),
    P(f"Unit break-even ACoS is {u['amazon_breakeven_acos']*100:.1f}%, but covering fixed costs by 2030 needs ≤ {M['payback_breakeven_acos']*100:.1f}% (see section 3).", 11, bullet=True, space=4)], margin=0)
callout(s, 0.5, 6.3, 12.33, 0.6, [P("**So what:** retail only makes sense if it lifts Amazon sales enough to pay for itself. That rests on the halo assumption tested on page 10.", 11.5)])

# =====================================================================================
# 8. Cumulative cash: three options
s = new_slide("Only the Amazon-led route passes all three of the board's financial tests; retail-led fails all three even on the planning team's own assumptions",
              section=1, source="Source: team model on briefing-pack inputs (Tables 4–7; planning-team volumes, 25% ACoS, 4.5 units/door/week, 1.3× halo). Cash = contribution – fixed – one-time – change in inventory (4 months of landed cost); pre-tax.")
cd = CategoryChartData(); cd.categories = ["2027", "2028", "2029", "2030"]
cd.add_series("A · Amazon-led", [r["cum"] for r in C["A_plan"]])
cd.add_series("B · Retail-led", [r["cum"] for r in C["B_plan"]])
cd.add_series("J · Japan scale-up", [r["cum"] for r in J])
cd.add_series("Board cap: –$18M peak cash", [-18] * 4)
gf = s.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, Inches(0.5), Inches(1.95), Inches(6.9), Inches(4.25), cd); ch = gf.chart
style_chart(ch)
for ser, col in zip(ch.series, [BLUE, ORANGE, AQUA, GRAY]):
    color_series_line(ser, col, dash=MSO_LINE.DASH if col == GRAY else None, marker=col != GRAY, width=1.5 if col == GRAY else 2.25)
ch.value_axis.minimum_scale = -24; ch.value_axis.maximum_scale = 4; ch.value_axis.major_unit = 4
ch.value_axis.tick_labels.number_format = '"$"0"M";"–$"0"M"'; ch.value_axis.tick_labels.number_format_is_linked = False
ch.category_axis.tick_label_position = XL_TICK_LABEL_POSITION.LOW
point_label(ch.series[0].points[3], fmt_m(a["cum2030"]), XL_LABEL_POSITION.ABOVE, 10, color=INK)
point_label(ch.series[1].points[3], fmt_m(b["cum2030"]), XL_LABEL_POSITION.BELOW, 10, color=INK)
point_label(ch.series[2].points[3], fmt_m(jj["cum2030"]), XL_LABEL_POSITION.BELOW, 10, color=INK)
text(s, 0.5, 1.55, 6.9, 0.4, [P("Cumulative cash flow by option, $M (planning-team assumptions)", 11.5, bold=True, color=NAVY)], margin=0)
hdr = ["Board test", "A · Amazon", "B · Retail", "J · Japan"]
rows = [["Peak cash ≤ $18M", f"{PASS} {fmt_m(a['peak'])}", f"{FAIL} {fmt_m(b['peak'])}", f"{PASS} {fmt_m(jj['peak'], d=2)}"],
        ["Payback by end-2030", f"{PASS} 2030 ({fmt_m(a['cum2030'])})", f"{FAIL} Not by 2030", f"{PASS} 2029"],
        ["Group margin ≥ 8% every year", f"{PASS} low {a['min_group_margin']*100:.1f}%", f"{FAIL} {b['min_group_margin']*100:.1f}% in 2027", f"{PASS} low {jj['min_group_margin']*100:.1f}%"],
        ["Ambition: 2030 revenue vs $40M", "$26.4M", "$37.6M", "No US; +$7.0M Japan"]]
fl = [[None]*4,
      [None, TINT_G, TINT_R, TINT_G], [None, TINT_G, TINT_R, TINT_G], [None, TINT_G, TINT_R, TINT_G], [None, None, None, None]]
table(s, [hdr] + rows, 7.7, 1.6, 5.13, [1.55, 1.2, 1.18, 1.2], row_h=0.62, size=10, fills=fl, bold_first_col=True)
text(s, 7.7, 4.85, 5.13, 1.35, [
    P(f"Group margin under B, 2027: ($140M × 11% – $8.66M US loss) ÷ ($140M + $11.33M) = **{C['B_plan'][0]['group_margin']*100:.1f}%**. It stays below 8% until 2030 (6.6%, 7.5%, then 8.2%).", 10.5, space=4),
    P("B's cash is still falling in 2030 (–$1.9M that year), so it has no route to payback on the planning team's own inputs.", 10.5)], margin=0)
callout(s, 0.5, 6.3, 12.33, 0.6, [P("**So what:** retail-led is out on the board's own rules before we even question its inputs. Amazon-led passes, but with little room on payback.", 11.5)])

# =====================================================================================
# 9. Retail velocity evidence
s = new_slide("Retail-led's 4.5 units/door/week comes from successful brands; at Onsoo's 4% awareness, newcomers sell a median 2.6, and most fall below the delisting bar",
              section=1, source="Source: briefing pack Table 8 (retail analytics firm, 2025, 46 newcomer brands; IQR = interquartile range), Table 9, survey Sept 2026. Evidence-adjusted B = 2.6 units/door/week, no halo, otherwise as planned.")
cd = CategoryChartData(); cd.categories = ["Below 10%\n(Onsoo today: 4%)\nIQR 1.9–3.4", "10–20%\n(CEO's 15% gate)\nIQR 2.8–4.3", "Above 20%\n\nIQR 3.9–5.5"]
cd.add_series("Median units per door per week, first year", [2.6, 3.5, 4.6])
FX, FY, FW, FH = 0.5, 1.95, 6.6, 4.25; INNER = (0.09, 0.06, 0.88, 0.7)
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(FX), Inches(FY), Inches(FW), Inches(FH), cd); ch = gf.chart
style_chart(ch, legend=False); ch.plots[0].gap_width = 80; set_inner(ch, *INNER)
ch.value_axis.minimum_scale = 0; ch.value_axis.maximum_scale = 6; ch.value_axis.major_unit = 1
for i, v in enumerate([2.6, 3.5, 4.6]):
    pt = ch.series[0].points[i]; pt.format.fill.solid(); pt.format.fill.fore_color.rgb = rgb(BLUE if i == 0 else GRAY)
    point_label(pt, f"{v}", XL_LABEL_POSITION.INSIDE_END, 11, color="#ffffff")
text(s, 0.5, 1.55, 6.6, 0.4, [P("Median first-year units/door/week, by awareness among category buyers", 11.5, bold=True, color=NAVY)], margin=0)
hline(s, FX, FY, FW, FH, INNER, 0, 6, 4.5, ORANGE, "Option B assumes 4.5", "left", above=True)
hline(s, FX, FY, FW, FH, INNER, 0, 6, 4.0, RED, "Delisting bar: below 4.0 at the 12-month review", "left", above=False)
text(s, 7.45, 1.6, 5.4, 4.6, [
    P("Why 4.5 is not a credible base case for Onsoo", 12.5, bold=True, color=NAVY, space=6),
    P("Onsoo's aided awareness is **4% of category buyers** (9% among K-beauty buyers), so it falls in the below-10% band.", 11, bullet=True, space=4),
    P("In that band **even the top quartile (3.4) is below the 4.0 bar**. More than 75% of comparable newcomers would be removed at the 12-month review.", 11, bullet=True, space=4),
    P("The 4.5 comes from the retailer's deck on **successful** newcomers, which is survivorship bias. It matches the above-20% band (4.6), five times Onsoo's awareness.", 11, bullet=True, space=4),
    P("**Mooncrest** (retail-first, 450 doors, 2023) was removed from shelves in 2025 after an estimated **$21M** US loss.", 11, bullet=True, space=4),
    P(f"With 2.6 units/door/week and no halo, retail-led's cumulative cash reaches **{fmt_m(S['B_evidence']['cum2030'])}** by 2030.", 11, bullet=True, space=4)], margin=0)
callout(s, 0.5, 6.3, 12.33, 0.6, [P("**So what:** on the evidence, a 2027 national retail launch would probably be delisted in 2028, repeating Mooncrest's loss.", 11.5)])

# =====================================================================================
# 10. Halo
hl = M["halo_needed"]
s = new_slide("The 1.3× Amazon \"halo\" behind retail-led rests on a correlation; to pay for retail's costs the halo would need to be 2.1–3.4× from 2028",
              section=1, source="Source: board member memo (r = 0.71 across 30 K-beauty brands), Table 9, survey Sept 2026. Halo needed = 1 + (retail fixed cost $7.5M – retail contribution) ÷ Option-A Amazon contribution at 25% ACoS; one-time costs excluded.")
cd = CategoryChartData(); cd.categories = ["2027", "2028", "2029", "2030"]
cd.add_series("Amazon multiple needed to cover retail costs", [hl[str(y)] for y in YEARS] if isinstance(list(hl.keys())[0], str) else [hl[y] for y in YEARS])
FX, FY, FW, FH = 7.2, 1.95, 5.6, 3.9; INNER = (0.11, 0.06, 0.86, 0.8)
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(FX), Inches(FY), Inches(FW), Inches(FH), cd); ch = gf.chart
style_chart(ch, legend=False); ch.plots[0].gap_width = 80; set_inner(ch, *INNER)
ch.value_axis.minimum_scale = 0; ch.value_axis.maximum_scale = 6; ch.value_axis.major_unit = 1
ch.value_axis.tick_labels.number_format = '0"×"'; ch.value_axis.tick_labels.number_format_is_linked = False
for i, y in enumerate(YEARS):
    v = hl[str(y)]; pt = ch.series[0].points[i]; pt.format.fill.solid(); pt.format.fill.fore_color.rgb = rgb(GRAY)
    point_label(pt, f"{v:.1f}×", XL_LABEL_POSITION.OUTSIDE_END, 10.5)
text(s, 7.2, 1.55, 5.6, 0.4, [P("Amazon multiple needed for retail to cover its own costs", 11.5, bold=True, color=NAVY)], margin=0)
hline(s, FX, FY, FW, FH, INNER, 0, 6, 1.3, ORANGE)
text(s, 7.2, 5.88, 5.6, 0.35, [P("Dashed orange line = the 1.3× halo assumed in Option B (a 30% uplift)", 10, color=INK2)], margin=0)
text(s, 0.5, 1.6, 6.4, 4.6, [
    P("Why a 0.71 correlation does not show that retail drives Amazon", 12.5, bold=True, color=NAVY, space=6),
    P("**Reverse causation:** retailers sign brands that already sell. Saebom reached ~$30M on Amazon first and **then** added 300 doors in 2025.", 11, bullet=True, space=5),
    P("**Common cause:** older, bigger, better-funded brands have both more doors and more Amazon sales.", 11, bullet=True, space=5),
    P("**Survivorship:** the sample is 30 brands sold in the US today. Failures such as Mooncrest are probably not in it.", 11, bullet=True, space=5),
    P("**Size of effect:** r = 0.71 means r² ≈ 0.50 shared variance. It says nothing about direction or about how big a 1.3× uplift would be.", 11, bullet=True, space=5),
    P("**Customer evidence points the other way:** only 17% of K-beauty buyers found their last new brand in a store (38% on TikTok), and 22% buy at specialty retail most often.", 11, bullet=True, space=5)], margin=0)
callout(s, 0.5, 6.3, 12.33, 0.6, [P("**So what:** the halo may exist, but it is unproven. To pay for retail it would have to lift Amazon sales by 110–240%, not 30%. Measure it before paying $7.5M a year for it.", 11.5)])

# =====================================================================================
# 11. Payback vs ACoS
sens = M["acos_sens"]; acos_keys = ["0.25", "0.26", "0.28", "0.30", "0.32", "0.35", "0.38"]
s = new_slide(f"Payback by 2030 is the binding constraint: Amazon-led pays back only if ACoS stays at or below {M['payback_breakeven_acos']*100:.1f}%, while the benchmark for brands this size is 32%",
              section=2, source="Source: team model; briefing pack §6 (pilot ACoS 28%), §11 (agency benchmark: median 32%, range 26–38% for brands scaling $5M→$20M on Amazon US). Volumes as planned unless stated.")
cd = CategoryChartData(); cd.categories = ["25%\nplan", "26%\nlow end", "28%\npilot", "30%", "32%\nmedian", "35%", "38%\nhigh end"]
cd.add_series("Cumulative US cash at end-2030", [sens[k]["cum2030"] for k in acos_keys])
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.5), Inches(1.95), Inches(6.5), Inches(4.25), cd); ch = gf.chart
style_chart(ch, legend=False); ch.plots[0].gap_width = 60
ch.value_axis.minimum_scale = -8; ch.value_axis.maximum_scale = 4; ch.value_axis.major_unit = 2
ch.value_axis.tick_labels.number_format = '"$"0"M";"–$"0"M"'; ch.value_axis.tick_labels.number_format_is_linked = False
ch.category_axis.tick_label_position = XL_TICK_LABEL_POSITION.LOW
for i, k in enumerate(acos_keys):
    v = sens[k]["cum2030"]; pt = ch.series[0].points[i]; pt.format.fill.solid(); pt.format.fill.fore_color.rgb = rgb(BLUE if v >= 0 else RED)
    point_label(pt, fmt_m(v), XL_LABEL_POSITION.OUTSIDE_END, 10, bold=False)
ch.plots[0].series[0].invert_if_negative = False
text(s, 0.5, 1.55, 6.5, 0.4, [P("Option A cumulative cash at end-2030 by ACoS (blue = pays back, red = does not)", 11.5, bold=True, color=NAVY)], margin=0)
# heat table
grid = M["grid"]; vols = ["0.70", "0.85", "1.00", "1.15"]; ac = ["0.25", "0.28", "0.30", "0.32", "0.35"]
def heat(v):
    def mix(c1, c2, t):
        c1, c2 = [int(c1[i:i+2], 16) for i in (1, 3, 5)], [int(c2[i:i+2], 16) for i in (1, 3, 5)]
        return "#" + "".join(f"{int(a_ + (b_ - a_) * t):02x}" for a_, b_ in zip(c1, c2))
    return mix("#f0efec", "#86b6ef", min(1, v / 4.2) * 0.9) if v >= 0 else mix("#f0efec", "#f19c9b", min(1, -v / 5.8) * 0.95)
hdr = ["Volume vs plan ↓ / ACoS →"] + [f"{float(k)*100:.0f}%" for k in ac]
rows = [[f"{float(v)*100:.0f}%" + (" (plan)" if v == "1.00" else "")] + [fmt_m(grid[v][k]) for k in ac] for v in vols]
fl = [[None]*6] + [[None] + [heat(grid[v][k]) for k in ac] for v in vols]
text(s, 7.35, 1.55, 5.5, 0.4, [P("Cumulative cash at end-2030, $M: ACoS × volume", 11.5, bold=True, color=NAVY)], margin=0)
table(s, [hdr] + rows, 7.35, 1.95, 5.48, [1.68, 0.76, 0.76, 0.76, 0.76, 0.76], row_h=0.4, size=10,
      aligns=[PP_ALIGN.LEFT] + [PP_ALIGN.CENTER]*5, fills=fl, bold_first_col=True)
text(s, 7.35, 4.05, 5.48, 2.2, [
    P("The plan assumes ACoS falls to 25% as the brand matures. The agency data says it **rises** as brands bid on broader keywords, to a median of 32% between $5M and $20M a year, which is exactly A's path ($7.2M → $26.4M).", 10.5, bullet=True, space=4),
    P("At the pilot's 28%, volume must reach **≥ 96% of plan** to pay back. At 25%, ≥ 79%.", 10.5, bullet=True, space=4),
    P("The cash cap is never the issue: peak cash stays between –$1.9M and –$6.4M across 25–38% ACoS.", 10.5, bullet=True, space=4)], margin=0)
callout(s, 0.5, 6.3, 12.33, 0.6, [P("**So what:** treat ACoS as the key operating metric. Cap blended ACoS at 28%, and **give up growth rather than buy volume above the ceiling**. Re-forecast at 32% before launch.", 11.5)])

# =====================================================================================
# 12. Downside bounded
scen = [("Plan (25% ACoS)", "A_plan"), ("Pilot ACoS (28%)", "A_pilot28"), ("Tariff rises to 25%", "A_plan_tariff25"),
        ("Benchmark ACoS (32%)", "A_bench32"), ("32% ACoS + 25% tariff", "A_bench32_tariff25"),
        ("ACoS at top of range (38%)", None), ("Sales stall at $4.8M/yr, 32% ACoS", "A_stall"), ("B · Retail-led plan (comparison)", "B_plan")]
vals, pb, gm = [], [], []
for lab, key in scen:
    sm = S[key] if key else sens["0.38"]
    vals.append(sm["peak"]); pb.append(sm["payback_ok"]); gm.append(sm["min_group_margin"])
s = new_slide("The downside is bounded: even if sales stall or tariffs rise, Amazon-led needs at most $7.1M of peak cash, well under the $18M cap, and group margin stays above the 8% floor",
              section=2, source="Source: team model. Tariff stress applies 25% duty to all years (decision expected mid-2027, so conservative). Stall = Gaon Lab/Yeoreum-type outcome (<$5M US revenue). FX: 10% weaker won cuts ex-factory + duty by ≈$0.40 a unit.")
cd = CategoryChartData(); cd.categories = list(reversed([l for l, _ in scen])); cd.add_series("Peak cumulative cash need", list(reversed([-v for v in vals])))
FX, FY, FW, FH = 0.5, 1.95, 7.3, 4.25; INNER = (0.37, 0.03, 0.55, 0.86)
gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(FX), Inches(FY), Inches(FW), Inches(FH), cd); ch = gf.chart
style_chart(ch, legend=False); ch.plots[0].gap_width = 45; set_inner(ch, *INNER)
ch.value_axis.minimum_scale = 0; ch.value_axis.maximum_scale = 24; ch.value_axis.major_unit = 6
ch.value_axis.tick_labels.number_format = '"$"0"M"'; ch.value_axis.tick_labels.number_format_is_linked = False
n = len(scen)
for i in range(n):
    oi = n - 1 - i; pt = ch.series[0].points[i]; pt.format.fill.solid()
    pt.format.fill.fore_color.rgb = rgb(ORANGE if scen[oi][1] == "B_plan" else BLUE)
    point_label(pt, f"${-vals[oi]:.1f}M", XL_LABEL_POSITION.OUTSIDE_END, 10, bold=False)
text(s, 0.5, 1.55, 7.3, 0.4, [P("Peak US cash need by scenario, $M (blue = Amazon-led; orange = retail-led for comparison)", 11.5, bold=True, color=NAVY)], margin=0)
ix, iy, iw, ih = INNER
xc = FX + (ix + iw * 18 / 24) * FW
ln = s.shapes.add_connector(1, Inches(xc), Inches(FY + iy * FH), Inches(xc), Inches(FY + (iy + ih) * FH)); ln.line.color.rgb = rgb(RED); ln.line.width = Pt(1.5); ln.line.dash_style = MSO_LINE.DASH
text(s, xc + 0.06, FY + iy * FH + 0.02, 1.3, 0.25, [P("$18M cap", 9, bold=True)], margin=0)
hdr = ["Scenario", "Payback by 2030", "Lowest group margin"]
rows = [[l, (f"{PASS} Yes" if p else f"{FAIL} No"), f"{g*100:.1f}%"] for (l, _), p, g in zip(scen, pb, gm)]
fl = [[None]*3] + [[None, TINT_G if p else TINT_R, TINT_G if g >= 0.08 else TINT_R] for p, g in zip(pb, gm)]
table(s, [hdr] + rows, 8.1, 1.6, 4.73, [2.45, 1.18, 1.1], row_h=0.4, size=9.5, fills=fl, aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER])
text(s, 8.1, 5.3, 4.73, 0.95, [
    P("If sales stall and we stop at the March 2028 gate, the loss is about **$3M** (2027: –$2.6M, plus one quarter of 2028). A 10% weaker won (≈ –$0.40 a unit) would roughly offset the tariff rise (+$0.35 a unit).", 10.5)], margin=0)
callout(s, 0.5, 6.3, 12.33, 0.6, [P("**So what:** the cash cap and margin floor are safe in every Amazon-led case. The real risk is payback. A gate can limit the cost of a stall to about $3M.", 11.5)])

# =====================================================================================
# 13. Retail timing
ar = C["A_then_retail2029"]
s = new_slide("Specialty retail should follow payback, not come before it: 600 doors in 2029 would break payback and the margin floor, and a 15% awareness gate is too low",
              section=2, source="Source: team model (A plan + 600 doors from 2029 at B's cost base: $7.5M/yr fixed, $0.5M launch fee, $1,100/door, 4.6 units/door/week = above-20% awareness median); Table 8.")
cd = CategoryChartData(); cd.categories = ["2027", "2028", "2029", "2030"]
cd.add_series("A · Amazon-led only", [r["cum"] for r in C["A_plan"]])
cd.add_series("A + 600 retail doors from 2029 (CEO's phase 2)", [r["cum"] for r in ar])
gf = s.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, Inches(0.5), Inches(1.95), Inches(6.3), Inches(4.25), cd); ch = gf.chart
style_chart(ch); color_series_line(ch.series[0], BLUE); color_series_line(ch.series[1], ORANGE)
ch.value_axis.minimum_scale = -14; ch.value_axis.maximum_scale = 4; ch.value_axis.major_unit = 2
ch.value_axis.tick_labels.number_format = '"$"0"M";"–$"0"M"'; ch.value_axis.tick_labels.number_format_is_linked = False
ch.category_axis.tick_label_position = XL_TICK_LABEL_POSITION.LOW
point_label(ch.series[0].points[3], fmt_m(a["cum2030"]), XL_LABEL_POSITION.ABOVE, 10)
point_label(ch.series[1].points[3], fmt_m(ar[-1]["cum"]), XL_LABEL_POSITION.BELOW, 10)
point_label(ch.series[1].points[2], f"Group margin {ar[2]['group_margin']*100:.1f}%", XL_LABEL_POSITION.BELOW, 9.5, bold=False)
text(s, 0.5, 1.55, 6.3, 0.4, [P("Cumulative US cash, $M", 11.5, bold=True, color=NAVY)], margin=0)
hdr = ["Gate for entering retail", "CEO's proposal", "Recommended", "Why"]
rows = [["Timing", "From 2029", "Decide in 2030 for 2031", "2029 entry: –$11.8M at 2030, margin 6.3%"],
        ["Aided awareness (category buyers)", "> 15%", "> 20%", "10–20%: median 3.5 < 4.0 bar; >20%: median 4.6"],
        ["Amazon sales", "> $10M", "> $10M (kept)", "Reached in 2028 on plan; not binding"],
        ["US cash", "—", "Cumulative ≥ 0 (payback met)", "Board's payback rule"],
        ["Cost base", "National, $7.5M/yr", "Scaled to doors", "Needs 32 units/door/week at 600 doors"]]
table(s, [hdr] + rows, 7.1, 1.6, 5.73, [1.45, 1.0, 1.35, 1.93], row_h=0.6, size=9.5, bold_first_col=True,
      fills=[[None]*4] + [[None, None, TINT_B, None]]*5)
text(s, 7.1, 5.3, 5.73, 0.95, [P("Raising awareness from 4% to 20% (5×) is the main brand-building job for 2027–30. TikTok (38% of discovery) is the main lever, so weight the $0.7M off-Amazon budget towards it. Re-run the awareness survey every year.", 10.5)], margin=0)
callout(s, 0.5, 6.3, 12.33, 0.6, [P("**So what:** keep retail in the plan but make it the next step after payback, triggered by >20% awareness rather than by the calendar.", 11.5)])

# =====================================================================================
# 14. Ambition
s = new_slide("No modeled route reaches $40M by 2030 within the $18M cap and 2030 payback; we recommend keeping the financial rules and moving the $40M date to about 2032",
              section=2, source="Source: team model. US revenue = Onsoo's receipts (Amazon at $24; retail at $14 wholesale). Post-2030 path is illustrative: assumes ~25% a year growth after 2030 (A grew 29% in 2030); not in the planning data.")
opts = [("A · Amazon-led", S["A_plan"], BLUE), ("A + retail 2029", S["A_then_retail2029"], GRAY), ("B · plan inputs", S["B_plan"], ORANGE), ("B · evidence inputs", S["B_evidence"], ORANGE)]
cd = CategoryChartData(); cd.categories = [o[0] for o in opts]; cd.add_series("US revenue in 2030", [o[1]["rev2030"] for o in opts])
FX, FY, FW, FH = 0.5, 1.95, 6.6, 3.35; INNER = (0.1, 0.07, 0.87, 0.72)
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(FX), Inches(FY), Inches(FW), Inches(FH), cd); ch = gf.chart
style_chart(ch, legend=False); ch.plots[0].gap_width = 70; set_inner(ch, *INNER)
ch.value_axis.minimum_scale = 0; ch.value_axis.maximum_scale = 48; ch.value_axis.major_unit = 10
ch.value_axis.tick_labels.number_format = '"$"0"M"'; ch.value_axis.tick_labels.number_format_is_linked = False
for i, (lab, sm, col) in enumerate(opts):
    pt = ch.series[0].points[i]; pt.format.fill.solid(); pt.format.fill.fore_color.rgb = rgb(col)
    point_label(pt, f"${sm['rev2030']:.1f}M", XL_LABEL_POSITION.INSIDE_END, 10.5, color="#ffffff")
hline(s, FX, FY, FW, FH, INNER, 0, 48, 40, NAVY, "Ambition: $40M in 2030", "left", above=True)
text(s, 0.5, 1.55, 6.6, 0.4, [P("US revenue in 2030 by route, $M, and the board tests each route meets", 11.5, bold=True, color=NAVY)], margin=0)
tests = [[f"{PASS if sm['cap_ok'] else FAIL} cap · {PASS if sm['payback_ok'] else FAIL} payback\n{PASS if sm['margin_ok'] else FAIL} margin floor" for _, sm, _ in opts]]
ix, iy, iw, ih = INNER
tb = table(s, tests, FX + ix * FW, 5.32, iw * FW, [iw * FW / 4] * 4, row_h=0.5, size=9.5, header=False,
           aligns=[PP_ALIGN.CENTER]*4, fills=[[TINT_G if sm['cap_ok'] and sm['payback_ok'] and sm['margin_ok'] else TINT_R for _, sm, _ in opts]])
hdr = ["Path", "2030", "2031", "2032"]
rows = [["A, continuing at ~25%/yr (illustrative)", "$26.4M", "$33.0M", "$41.3M"], ["+ retail from 2031 if gates are met", "—", "upside", "upside"]]
text(s, 7.45, 1.55, 5.4, 0.4, [P("Board options for the ambition", 12.5, bold=True, color=NAVY)], margin=0)
text(s, 7.45, 1.95, 5.4, 2.4, [
    P("**Recommended: keep the rules, move the date.** Read \"on the way to $40M\" as $25M+ in 2030 with a credible path to $40M around 2032.", 11, bullet=True, space=6),
    P("**Not recommended: keep 2030, relax the rules.** Only retail-led gets near $40M, and it needs a cap above $20.8M on optimistic inputs (–$26.4M on evidence inputs), no payback by 2030, and margins below 8% for three years.", 11, bullet=True, space=6)], margin=0)
text(s, 7.45, 3.75, 5.38, 0.3, [P("Illustrative path for Option A after 2030", 11, bold=True, color=NAVY)], margin=0)
table(s, [hdr] + rows, 7.45, 4.08, 5.38, [2.68, 0.9, 0.9, 0.9], row_h=0.36, size=10, aligns=[PP_ALIGN.LEFT] + [PP_ALIGN.CENTER]*3)
callout(s, 0.5, 6.3, 12.33, 0.6, [P("**So what:** the $40M-by-2030 ambition cannot be met together with the board's $18M cap and 2030 payback rule. The board should formally choose which one gives way. We recommend the date.", 11.5)])

# =====================================================================================
# 15. Phased plan
s = new_slide("We recommend a three-phase plan in which each phase is unlocked by measured results rather than by the calendar",
              section=2, source="Gate thresholds derived from the team model: payback needs ≥96% of planned volume at 28% ACoS (≥79% at 25%); 70% of plan ≈ the stall zone of peers below $5M; 20% awareness from Table 8.")
phases = [
    ("Phase 1 · Launch", "Apr–Dec 2027", ["Set up the US entity, MoCRA registration and US-compliant labels (removes the Korean-only label complaint)",
                                           "Move the listings from the cross-border seller to Onsoo's own Amazon operation",
                                           "Add four SKUs (seven in total); weight the $0.7M off-Amazon budget to TikTok and social",
                                           "Run at a blended ACoS ceiling of 28%; cash envelope $4M (covers the –$3.9M stress case)"]),
    ("Phase 2 · Scale on Amazon", "2028–2030", ["Scale towards ~1.1M units ($26M) only while ACoS ≤ 28%",
                                                 "Build aided awareness from 4% towards 20%; survey every year",
                                                 "Lift 90-day repeat from 29% to ≥ 31% through the wider range",
                                                 "Look again at the Japan scale-up for 2028 (bandwidth now free)"]),
    ("Phase 3 · Add retail", "Decide 2030 → launch 2031", ["Only when awareness > 20% and US cash has paid back",
                                                          "Start with a door-scaled cost base, not the $7.5M national model",
                                                          "Measure the Amazon halo directly before scaling doors",
                                                          "Path to $40M around 2032"])]
x = 0.5
for i, (h, when, items) in enumerate(phases):
    rect(s, x, 1.6, 3.0, 0.62, NAVY if i == 0 else ("#2f4a7a" if i == 1 else "#5b6f94"))
    text(s, x, 1.6, 3.0, 0.62, [P(h, 12.5, bold=True, color="#ffffff", space=0), P(when, 10, color="#dfe6f2")], anchor=MSO_ANCHOR.MIDDLE, margin=0.08)
    text(s, x, 2.3, 3.0, 2.6, [P(t, 10.5, bullet=True, space=4) for t in items], margin=0.04, fill="#f5f7fb")
    x += 3.12
gx = 9.9
rect(s, gx, 1.6, 2.93, 0.62, BLUE)
text(s, gx, 1.6, 2.93, 0.62, [P("Gate 1 · March 2028 board", 12.5, bold=True, color="#ffffff", space=0), P("on full-year 2027 results", 10, color="#eaf1fb")], anchor=MSO_ANCHOR.MIDDLE, margin=0.08)
rows = [[f"{PASS} Green: scale", "ACoS ≤ 28% and units ≥ 96% of plan (re-forecast pays back by 2030); repeat ≥ 31%"],
        ["◐ Amber: hold", "Anything between green and red: hold ad spend at the ceiling, slow SKU additions, re-forecast in 6 months"],
        [f"{FAIL} Red: stop", "ACoS > 32% or units < 70% of plan (stall zone): move to a maintenance model or exit; cash at risk about $3M"]]
table(s, rows, gx, 2.3, 2.93, [0.85, 2.08], row_h=0.86, size=9.5, header=False, bold_first_col=True,
      fills=[[TINT_G, None], [TINT_A, None], [TINT_R, None]])
hdr = ["KPI tracked monthly", "Today", "Gate / target"]
rows = [["Blended ACoS", "28% (pilot)", "≤ 28% ceiling"], ["Amazon units vs plan", "168k/yr run-rate", "300k in 2027 → 1.1M in 2030"],
        ["90-day repeat", "29%", "≥ 31% by Gate 1"], ["Aided awareness, category buyers", "4%", "> 20% before retail"],
        ["Cumulative US cash", "—", "≥ –$4M envelope; ≥ 0 by 2030"]]
table(s, [hdr] + rows, 0.5, 5.0, 9.24, [3.2, 2.4, 3.64], row_h=0.3, size=9.5, bold_first_col=True)

# =====================================================================================
# 16. Risks
s = new_slide("Six risks could derail the plan; ad cost at scale is the largest, and each risk has an early warning sign and an agreed response",
              section=2, source="Source: briefing pack §13 (uncertainties), §6, §11; team model. Impacts are on Option A cumulative cash at end-2030 vs the plan case (+$2.4M) unless stated.")
hdr = ["Risk", "Evidence", "Quantified impact", "Early warning sign", "Response"]
rows = [["**Ad cost at scale**", "Pilot 28% on a small budget; benchmark 32% (26–38%)", "–$0.67M per ACoS point; 32% → –$2.3M (no payback)", "Monthly blended ACoS", "28% ceiling; slower growth over paid volume"],
        ["**Demand stall**", "2 of 3 Amazon-first peers stayed below $5M", "–$7.1M by 2030 if continued; about –$3M if stopped at Gate 1", "Units vs plan; growth after SKU launches", "Gate 1 red rule; maintenance model or exit"],
        ["**Tariff 15% → 25%**", "US review; decision mid-2027", "+$0.35/unit; –$1.1M; break-even ACoS 28.6% → 26.9%", "US decision, mid-2027", "Re-forecast; FX offset; review price (limited: 52% buy partly on price)"],
        ["**Low repeat**", "29% vs 31% benchmark; 48% in Korea", "Lower lifetime value means more reliance on ads", "90-day repeat by cohort", "Range build-out, US labels, regimen bundles"],
        ["**FX (KRW/USD)**", "Product costs in won", "10% weaker won = +$0.40/unit (upside); stronger won is the mirror risk", "Monthly KRW/USD", "Budget at today's rate; group treasury policy"],
        ["**Launch execution**", "Korean-only labels in 6% of reviews; first US entity", "Reviews and conversion; MoCRA compliance", "Review complaints; registration milestones", "Labels and MoCRA fixed before scale-up; $0.8M setup budget"]]
table(s, [hdr] + rows, 0.5, 1.6, 12.33, [1.55, 2.75, 2.95, 2.25, 2.83], row_h=0.66, size=10)
callout(s, 0.5, 6.3, 12.33, 0.6, [P("**So what:** most risks hit the payback date, not the cash cap or margin floor. Monitor them monthly and decide on them at Gate 1.", 11.5)])

# =====================================================================================
# 17. Decisions
s = new_slide("We ask the board to approve five decisions at the March 2027 meeting",
              source="Interpretation choices made without being able to ask are listed on page 18.")
decs = [("Approve US entry in 2027 through the Amazon-led route (Option A)", "Setup $0.8M; fixed costs $2.1M a year; cash envelope $4M against the $18M cap"),
        ("Adopt the ACoS ceiling and Gate 1", "Blended ACoS ≤ 28%; review at the March 2028 board under the green/amber/red rules"),
        ("Do not launch national specialty retail in 2027", "Revisit in 2030 for 2031, once awareness is above 20% and US cash has paid back"),
        ("Move the ambition to $25M+ US revenue in 2030 and $40M around 2032", "Keep the cash cap, payback rule and margin floor unchanged"),
        ("Look again at the Japan scale-up for 2028", "Japan becomes the next major launch once 2027 bandwidth is freed")]
y = 1.65
for i, (h, d) in enumerate(decs):
    rect(s, 0.5, y, 0.55, 0.55, NAVY, shape=MSO_SHAPE.OVAL)
    text(s, 0.5, y, 0.55, 0.55, [P(str(i + 1), 16, bold=True, color="#ffffff", align=PP_ALIGN.CENTER)], anchor=MSO_ANCHOR.MIDDLE, margin=0)
    text(s, 1.25, y - 0.03, 11.5, 0.7, [P(h, 14, bold=True, color=NAVY, space=1), P(d, 11.5, color=INK2)], margin=0)
    y += 0.86
callout(s, 0.5, 6.1, 12.33, 0.75, [P("**Before launch:** re-forecast Option A at 32% ACoS and a 25% tariff, confirm the label and MoCRA work plan, and plan the hand-over from the cross-border seller.", 11.5)])

# =====================================================================================
# Appendix
s = new_slide("Appendix: interpretation choices and key modeling assumptions",
              source="All inputs come from the briefing pack; no outside data used. Figures are synthetic benchmark data.")
left = [
    P("Choices made where we would have asked", 12.5, bold=True, color=NAVY, space=6),
    P("**\"$40M by 2030\"** is read as a 2030 revenue target and treated as an ambition. The cash cap, payback and margin floor are treated as hard constraints.", 10.5, bullet=True, space=4),
    P("**US revenue** = what Onsoo receives: $24 on Amazon and $14 wholesale for retail, not shelf value.", 10.5, bullet=True, space=4),
    P("**Retail volumes** run for the full year from 2027, as the planning team implies; no ramp-up.", 10.5, bullet=True, space=4),
    P("**Tariff stress** applies 25% duty to all four years (conservative, since the decision is mid-2027).", 10.5, bullet=True, space=4),
    P("**Listings move** from the cross-border seller to Onsoo's own operation inside the $0.8M setup cost.", 10.5, bullet=True, space=4),
    P("**Stall case** = Amazon flat at 200k units ($4.8M) a year, consistent with peers below $5M.", 10.5, bullet=True, space=4),
    P("**Cash envelope $4M** is our proposal, covering the worst non-stall stress case (–$3.9M).", 10.5, bullet=True, space=4)]
right = [
    P("Modeling conventions", 12.5, bold=True, color=NAVY, space=6),
    P("Pre-tax US cash flow; constant FX (KRW 1,380/$); no terminal value.", 10.5, bullet=True, space=4),
    P("Cash = units × unit contribution – fixed costs – one-time costs – change in inventory.", 10.5, bullet=True, space=4),
    P("Inventory = 4 months of landed cost (ex-factory + freight + duty): $4.575 a unit on Amazon, $4.775 in retail.", 10.5, bullet=True, space=4),
    P("Door fixtures ($1,100 per new door) expensed in the year the door opens.", 10.5, bullet=True, space=4),
    P("Group margin = (ex-US plan revenue × 11% + US operating result) ÷ (ex-US revenue + US revenue). Inventory is excluded from the margin.", 10.5, bullet=True, space=4),
    P("Hero-SKU unit economics applied to all SKUs, as the planning team does.", 10.5, bullet=True, space=4),
    P("Japan (Option J): incremental revenue × 30% – $0.8M fixed – $1.0M one-time; no working-capital data provided.", 10.5, bullet=True, space=4),
    P("Peak cash = the most negative cumulative cash position, 2027–30.", 10.5, bullet=True, space=4)]
text(s, 0.5, 1.6, 6.0, 5.2, left, margin=0)
text(s, 6.85, 1.6, 6.0, 5.2, right, margin=0)


def model_table_slide(title, cases_, source):
    s = new_slide(title, source=source)
    y = 1.55
    for lab, rows_ in cases_:
        text(s, 0.5, y, 12.3, 0.3, [P(lab, 11.5, bold=True, color=NAVY)], margin=0)
        hdr = ["$M", "Revenue", "Contribution", "Fixed", "One-time", "Operating result", "Δ Inventory", "Cash flow", "Cumulative cash", "Group margin"]
        def n(v, neg=False):
            v = -v if neg else v
            if abs(v) < 0.005: return "—"
            return ("–" if v < 0 else "") + f"{abs(v):.2f}"
        data = [hdr] + [[str(r["year"]), n(r["rev"]), n(r.get("cm", r["rev"] * 0.3)), n(r.get("fixed", 0.8), True),
                         n(r.get("one_time", 1.0 if r["year"] == 2027 else 0), True), n(r["op"]), n(r.get("dwc", 0), True),
                         n(r["cf"]), f"**{n(r['cum'])}**", f"{r['group_margin']*100:.1f}%"] for r in rows_]
        table(s, data, 0.5, y + 0.3, 12.33, [0.9] + [1.27] * 9, row_h=0.25, size=9.5, header_fill=LGRAY,
              aligns=[PP_ALIGN.LEFT] + [PP_ALIGN.RIGHT] * 9)
        y += 0.3 + 0.25 * 5 + 0.2
    return s

model_table_slide("Appendix: Option A (Amazon-led) pays back in 2030 at the plan's 25% ACoS but not at the 32% benchmark",
                  [("Option A · plan inputs: 300k → 1.1M units; 25% ACoS ($4.725 a unit); fixed $2.1M a year; setup $0.8M", C["A_plan"]),
                   ("Option A · benchmark ACoS 32% ($3.045 a unit), otherwise as planned", C["A_bench32"]),
                   ("Option A · stall case: 200k units a year at 32% ACoS", C["A_stall"])],
                  "Source: team model on briefing-pack inputs. Fixed = compliance $0.5M + US team $0.9M + off-Amazon marketing $0.7M.")
model_table_slide("Appendix: Option B (retail-led) loses money in every year on both plan and evidence inputs",
                  [("Option B · plan inputs: 600/600/800/1,000 doors × 4.5 units/door/week; Amazon = A × 1.3; 25% ACoS", C["B_plan"]),
                   ("Option B · evidence inputs: 2.6 units/door/week (below-10% awareness median), no halo", C["B_evidence"]),
                   ("A + CEO's phase 2: 600 doors from 2029 at B's cost base, 4.6 units/door/week", C["A_then_retail2029"])],
                  "Source: team model. B fixed = $2.1M + national retail marketing $6.0M + field team $1.5M; one-time 2027 = setup $0.8M + launch fee $0.5M + fixtures 600 × $1,100.")
s = model_table_slide("Appendix: Option J (Japan scale-up) is low-risk and pays back in 2029, but adds only $7M of revenue by 2030",
                      [("Option J · incremental revenue × 30% contribution; $0.8M fixed a year; $1.0M one-time in 2027", J)],
                      "Source: briefing pack Table 7 and group context (ex-US revenue $140M/$146M/$152M/$158M at 11.0% operating margin).")
text(s, 0.5, 3.55, 12.3, 3.1, [
    P("Key calculations used in the deck", 12.5, bold=True, color=NAVY, space=6),
    P("K-beauty CAGR 2021–25 = (3.6 ÷ 1.9)^(1/4) – 1 = 17.3%; all facial skincare (24.5 ÷ 20.1)^(1/4) – 1 = 5.1%; share 9.5% → 14.7%.", 10.5, bullet=True, space=3),
    P("Amazon contribution = 24.00 – 3.60 referral – 5.10 FBA – 3.50 product – 0.55 freight – 0.525 duty = $10.725 before ads; – 25% × $24 = $4.725.", 10.5, bullet=True, space=3),
    P("Retail contribution = 14.00 – 3.50 – 0.75 – 0.525 – 1.12 co-op – 0.56 returns = $7.545; break-even at 600 doors = 7.5M ÷ 7.545 ÷ 31,200 = 31.9 units/door/week.", 10.5, bullet=True, space=3),
    P("Break-even ACoS for 2030 payback: cumulative contribution must cover $9.2M of fixed and setup costs plus $1.68M of end-2030 inventory over 2.81M units → $3.87 a unit → ACoS ≤ 28.6%.", 10.5, bullet=True, space=3),
    P("Tariff at 25%: duty $0.875 vs $0.525 → +$0.35 a unit × 2.81M = –$0.98M, plus –$0.13M of extra inventory = –$1.1M.", 10.5, bullet=True, space=3),
    P("Pilot run-rate: 14,000 × 12 = 168k units = $4.03M; 2027 plan of 300k = 1.79× that.", 10.5, bullet=True, space=3)], margin=0)

out = os.path.join(ROOT, "deliverable", "Onsoo_US_entry_board_deck.pptx")
prs.save(out)
print("saved", out, page[0], "slides")
