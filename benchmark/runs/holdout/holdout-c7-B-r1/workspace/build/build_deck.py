"""Build the Atlas FieldOps / RouteSprout board deck (python-pptx, native charts)."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.chart.data import CategoryChartData, XyChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION, XL_TICK_LABEL_POSITION
import sys

OUT = sys.argv[1]

# ---------- palette ----------
NAVY = RGBColor(0x1F, 0x2A, 0x44)
INK = RGBColor(0x0B, 0x0B, 0x0B)
INK2 = RGBColor(0x52, 0x51, 0x4E)
MUTED = RGBColor(0x8A, 0x89, 0x84)
RULE = RGBColor(0xD9, 0xD8, 0xD3)
PANEL = RGBColor(0xF3, 0xF2, 0xEE)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLUE = RGBColor(0x2A, 0x78, 0xD6)
BLUE_LT = RGBColor(0xCD, 0xE2, 0xFB)
ORANGE = RGBColor(0xEB, 0x68, 0x34)
AQUA = RGBColor(0x1B, 0xAF, 0x7A)
RED = RGBColor(0xE3, 0x49, 0x48)
GOOD = RGBColor(0x0C, 0xA3, 0x0C)
WARN = RGBColor(0xFA, 0xB2, 0x19)
CRIT = RGBColor(0xD0, 0x3B, 0x3B)
FONT = "Arial"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
SW = 13.333
LM = 0.55
CW = SW - 2 * LM

page = {"n": 0}
fit_warnings = []


def est_lines(text, width_in, pt):
    chars_per_line = max(1, int(width_in * 72 / (pt * 0.52)))
    lines = 0
    for para in text.split("\n"):
        lines += max(1, -(-len(para) // chars_per_line))
    return lines


def check_fit(label, text, w, h, pt, spacing=1.2):
    need = est_lines(text, w - 0.2, pt) * pt * spacing / 72 + 0.1
    if need > h:
        fit_warnings.append(f"p{page['n']} {label}: need {need:.2f}in have {h:.2f}in :: {text[:50]}")


def tb(slide, x, y, w, h, paras, size=12, color=INK, bold=False, align=PP_ALIGN.LEFT,
       anchor=MSO_ANCHOR.TOP, fill=None, line=None, margin=0.08, spacing=1.1, label="tb"):
    """paras: str or list of items. item = str | (str, dict) | list of runs [(text, dict)]."""
    shp = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)) if fill is None and line is None \
        else slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is not None or line is not None:
        if fill is not None:
            shp.fill.solid(); shp.fill.fore_color.rgb = fill
        else:
            shp.fill.background()
        if line is not None:
            shp.line.color.rgb = line; shp.line.width = Pt(0.75)
        else:
            shp.line.fill.background()
        shp.shadow.inherit = False
    tf = shp.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    tf.vertical_anchor = anchor
    for side in ("left", "right", "top", "bottom"):
        setattr(tf, f"margin_{side}", Inches(margin))
    if isinstance(paras, str):
        paras = [paras]
    alltext = []
    first = True
    for item in paras:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = align
        p.line_spacing = spacing
        opts = {}
        if isinstance(item, tuple):
            item, opts = item
        runs = item if isinstance(item, list) else [(item, {})]
        bullet = opts.get("bullet", False)
        if bullet:
            runs = [("•  ", {})] + list(runs)
        if opts.get("space_before"):
            p.space_before = Pt(opts["space_before"])
        if opts.get("space_after") is not None:
            p.space_after = Pt(opts["space_after"])
        ptxt = ""
        for text, ro in runs:
            r = p.add_run()
            r.text = text
            ptxt += text
            f = r.font
            f.name = FONT
            f.size = Pt(ro.get("size", opts.get("size", size)))
            f.bold = ro.get("bold", opts.get("bold", bold))
            f.italic = ro.get("italic", False)
            f.color.rgb = ro.get("color", opts.get("color", color))
        alltext.append(ptxt)
    check_fit(label, "\n".join(alltext), w, h, size, spacing * 1.12)
    return shp


def rect(slide, x, y, w, h, fill, line=None, shape=MSO_SHAPE.RECTANGLE):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid(); s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line; s.line.width = Pt(0.75)
    s.shadow.inherit = False
    return s


def hline(slide, x, y, w, color=RULE, weight=1.0):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x), Inches(y), Inches(x + w), Inches(y))
    c.line.color.rgb = color; c.line.width = Pt(weight)
    return c


def vline(slide, x, y, h, color=RULE, weight=1.0, dash=False):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x), Inches(y), Inches(x), Inches(y + h))
    c.line.color.rgb = color; c.line.width = Pt(weight)
    if dash:
        from pptx.enum.dml import MSO_LINE_DASH_STYLE
        c.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    return c


def new_slide(title, tracker, source=None):
    page["n"] += 1
    s = prs.slides.add_slide(BLANK)
    tb(s, LM, 0.22, CW, 0.3, tracker.upper(), size=10, color=BLUE, bold=True, label="tracker")
    tb(s, LM, 0.48, CW, 0.95, title, size=21, color=NAVY, bold=True, anchor=MSO_ANCHOR.TOP,
       spacing=1.0, label="title")
    hline(s, LM, 1.45, CW, color=NAVY, weight=1.25)
    src = "Source: Atlas FieldOps briefing pack (synthetic benchmark data); team analysis."
    if source:
        src = "Source: " + source
    tb(s, LM, 7.0, CW - 0.8, 0.35, src, size=8.5, color=MUTED, label="source")
    tb(s, SW - LM - 0.6, 7.0, 0.6, 0.35, str(page["n"]), size=9, color=MUTED, align=PP_ALIGN.RIGHT,
       label="pg")
    return s


def table(slide, x, y, w, h, data, col_w=None, font=10.5, header_fill=NAVY, header_color=WHITE,
          row_h=None, bold_first_col=True, zebra=True, cell_fills=None, cell_colors=None,
          cell_bold=None, align_cols=None, label="table"):
    rows, cols = len(data), len(data[0])
    gt = slide.shapes.add_table(rows, cols, Inches(x), Inches(y), Inches(w), Inches(h))
    t = gt.table
    tblPr = gt._element.graphic.graphicData.tbl.tblPr
    # remove default style banding look
    tblPr.set("bandRow", "0"); tblPr.set("firstRow", "0")
    if col_w:
        for i, cw in enumerate(col_w):
            t.columns[i].width = Inches(cw)
    for r in range(rows):
        if row_h:
            t.rows[r].height = Inches(row_h[r] if isinstance(row_h, list) else row_h)
        for c in range(cols):
            cell = t.cell(r, c)
            val = data[r][c]
            cell.margin_left = cell.margin_right = Inches(0.07)
            cell.margin_top = cell.margin_bottom = Inches(0.04)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = cell.text_frame
            tf.word_wrap = True
            lines = val.split("\n") if isinstance(val, str) else [val]
            for li, ln in enumerate(lines):
                p = tf.paragraphs[0] if li == 0 else tf.add_paragraph()
                p.line_spacing = 1.0
                r_ = p.add_run(); r_.text = ln
                f = r_.font; f.name = FONT; f.size = Pt(font)
                if r == 0:
                    f.bold = True; f.color.rgb = header_color
                else:
                    f.color.rgb = INK
                    f.bold = (c == 0 and bold_first_col)
                    if cell_bold and (r, c) in cell_bold:
                        f.bold = True
                    if cell_colors and (r, c) in cell_colors:
                        f.color.rgb = cell_colors[(r, c)]
                if align_cols and c in align_cols:
                    p.alignment = align_cols[c]
            cell.fill.solid()
            if r == 0:
                cell.fill.fore_color.rgb = header_fill
            elif cell_fills and (r, c) in cell_fills:
                cell.fill.fore_color.rgb = cell_fills[(r, c)]
            elif zebra and r % 2 == 0:
                cell.fill.fore_color.rgb = PANEL
            else:
                cell.fill.fore_color.rgb = WHITE
    # fit estimate per row
    if col_w:
        total = 0
        for r in range(rows):
            mx = 0
            for c in range(cols):
                txt = data[r][c]
                need = est_lines(txt, col_w[c] - 0.16, font) * font * 1.18 / 72 + 0.09
                mx = max(mx, need)
            total += mx
        if total > h + 0.05:
            fit_warnings.append(f"p{page['n']} {label}: table needs ~{total:.2f}in, given {h:.2f}in")
    return t


def style_chart_common(chart, legend=True, legend_pos=XL_LEGEND_POSITION.TOP, size=10):
    chart.font.name = FONT
    chart.font.size = Pt(size)
    chart.font.color.rgb = INK2
    chart.has_legend = legend
    if legend:
        chart.legend.position = legend_pos
        chart.legend.include_in_layout = False
        chart.legend.font.size = Pt(size)


def style_axis(ax, numfmt=None, gridlines=False, visible=True, size=10):
    ax.has_major_gridlines = gridlines
    if gridlines:
        ax.major_gridlines.format.line.color.rgb = RULE
        ax.major_gridlines.format.line.width = Pt(0.5)
    ax.format.line.color.rgb = RULE
    ax.tick_labels.font.size = Pt(size)
    ax.tick_labels.font.color.rgb = INK2
    if numfmt:
        ax.tick_labels.number_format = numfmt
        ax.tick_labels.number_format_is_linked = False
    ax.visible = visible


def status_chip(slide, x, y, status):
    col = {"PASS": GOOD, "WATCH": WARN, "FAIL": CRIT, "UNPROVEN": WARN}[status]
    icon = {"PASS": "✔ ", "WATCH": "! ", "FAIL": "✖ ", "UNPROVEN": "? "}[status]
    rect(slide, x, y + 0.04, 0.12, 0.22, col)
    tb(slide, x + 0.14, y, 1.2, 0.3, icon + status.title(), size=10, bold=True, color=INK, margin=0.02,
       label="chip")


# =====================================================================
# 1. Title
# =====================================================================
page["n"] += 1
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, SW, 7.5, NAVY)
rect(s, LM, 2.35, 0.08, 1.9, BLUE)
tb(s, LM + 0.3, 1.2, 11, 0.4, "ATLAS FIELDOPS · BOARD OF DIRECTORS · MARCH 2027 MEETING", size=12,
   color=BLUE_LT, bold=True)
tb(s, LM + 0.3, 2.25, 11.5, 1.4, "Routing strategy: partner with RouteSprout now, and buy only on conditional terms",
   size=34, color=WHITE, bold=True, spacing=1.0)
tb(s, LM + 0.3, 3.65, 11.5, 0.7,
   "Should Atlas buy RouteSprout in 2027, and on what terms, rather than build or partner?",
   size=17, color=BLUE_LT)
tb(s, LM + 0.3, 5.6, 11.5, 0.9,
   ["Board pre-read · prepared November 2026",
    "All figures are from the briefing pack (synthetic benchmark data) or are labelled team assumptions. "
    "$ in millions unless stated."],
   size=11, color=RGBColor(0xC3, 0xC2, 0xB7))

# =====================================================================
# 2. Executive summary
# =====================================================================
s = new_slide("Do not buy RouteSprout on the proposed terms in 2027. Partner now, and keep a conditional "
              "option to buy later at no more than $8.5M upfront", "Executive summary")
rect(s, LM, 1.62, CW, 0.95, PANEL)
rect(s, LM, 1.62, 0.07, 0.95, BLUE)
tb(s, LM + 0.18, 1.64, CW - 0.25, 0.92,
   [[("Recommendation: ", {"bold": True, "color": NAVY}),
     ("Reject the $18.0M all-cash deal (Path A) and the staged deal as structured (Path B). Sign a two-year "
      "RouteSprout routing partnership ($1.2M minimum, live summer 2027) that includes a right of first refusal and a "
      "pre-agreed conditional purchase option. Exercise it at a Q1 2028 gate only if six evidence thresholds are met.",
      {})]], size=12.5, anchor=MSO_ANCHOR.MIDDLE, label="gov")
points = [
    ("1  Cash", "Neither acquisition path stays inside the cash limits.",
     "Path A needs $22.0M against a $15.0M ceiling. Path B fits at signing ($14.5M), but 18 months of operating "
     "drag takes cash to $7.2–8.2M, below the $9.0M floor. Nothing in the plan funds the $7.0M earnout due in 2029."),
    ("2  Value", "The value case is overstated, and payback takes more than 15 years.",
     "$18.0M is 3.75x recognised ARR, not the sellers' 2.5x of bookings. The $2.4M cross-sell is ARR, not EBITDA. "
     "After margin, support and RouteSprout's losses it adds about $0.1M a year, and loses $1.2M a year in the low case."),
    ("3  Risk", "Customer and execution risk is high and not priced in.",
     "Logo churn rose from 12% to 21%, and 58% of ARR sits in 41 accounts. The sellers assume 100% renewal. 30% of "
     "the integration is unscoped, and the synergy evidence is correlation only."),
    ("4  Options", "Only the partnership passes all four board criteria in 2027.",
     "At most $1.2M is at risk, it is live this summer, and no customers have to migrate. It earns more than ownership "
     "at any routing ARR below about $3.5M. Building is affordable but ships no earlier than late 2028."),
    ("5  Terms", "Buying stays possible, but only on conditional terms.",
     "At most $8.5M upfront (about 1.8x verified ARR) and up to $9.5M more if earned, paid only while cash stays "
     "above the floor. Integrate through the API first, and keep RouteSprout's interface until its large accounts renew."),
]
y = 2.75
for tag, head, body in points:
    tb(s, LM, y, 1.25, 0.78, tag, size=12, bold=True, color=BLUE, label="tag")
    tb(s, LM + 1.3, y, 3.6, 0.78, head, size=12, bold=True, color=NAVY, label="head")
    tb(s, LM + 5.0, y, CW - 5.0, 0.78, body, size=10.5, color=INK, label="body")
    hline(s, LM, y + 0.8, CW)
    y += 0.84

# =====================================================================
# 3. Hypothesis test
# =====================================================================
s = new_slide("Our starting hypothesis was to buy RouteSprout in 2027 on staged terms. It fails four of the five "
              "tests it has to pass, and the fifth is unproven", "Approach: hypothesis-driven")
tb(s, LM, 1.57, CW, 0.58,
   [[("Initial hypothesis: ", {"bold": True, "color": NAVY}),
     ("Atlas should buy RouteSprout in 2027, using the staged structure (Path B, $11.0M upfront) to fit the $15.0M cash "
      "ceiling, because it is the fastest way to own routing.", {})]], size=12, label="hyp")
data = [
    ["What would have to be true", "What the evidence shows", "Verdict", "See"],
    ["1. Affordable: cash stays at or above the $9.0M floor through 2028, and the earnout can be funded",
     "Path B leaves $0.5M headroom at signing and falls to $7.2–8.2M by end-2028. The $7.0M earnout has no "
     "funding source.", "", "p.4–5"],
    ["2. Fairly priced: the price rests on verified recurring revenue",
     "3.75x recognised ARR, not 2.5x. Bookings include multi-year contract value and pilots. No quality-of-earnings "
     "(QoE) review has been done.", "", "p.6"],
    ["3. Pays back: positive incremental contribution within a reasonable horizon",
     "Run-rate contribution is +$0.07M (base) or −$1.21M (low) while integration support runs. Payback takes "
     "more than 15 years.", "", "p.7–8"],
    ["4. Protects customers: RouteSprout and Atlas renewals and 99.7% uptime survive integration",
     "Churn rose from 12% to 21%. The case assumes 100% renewal. Replacing the interface before renewals "
     "risks churn. No cohort data exists.", "", "p.9–10"],
    ["5. Beats the alternatives on cash, payback, continuity and execution",
     "The partnership earns more below about $3.5M of routing ARR and risks at most $1.2M. "
     "Building is slower but cheaper.", "", "p.11–13"],
]
table(s, LM, 2.2, CW, 3.85, data, col_w=[4.1, 5.6, 1.3, 1.233], font=10.5,
      row_h=[0.38] + [0.69] * 5, align_cols={3: PP_ALIGN.CENTER}, label="hyp table")
verdicts = ["FAIL", "FAIL", "FAIL", "UNPROVEN", "FAIL"]
yy = 2.2 + 0.38
for v in verdicts:
    status_chip(s, LM + 4.1 + 5.6 + 0.08, yy + 0.2, v)
    yy += 0.69
rect(s, LM, 6.2, CW, 0.65, PANEL)
tb(s, LM + 0.15, 6.2, CW - 0.3, 0.65,
   [[("Revised answer: ", {"bold": True, "color": NAVY}),
     ("partner now to meet the customer need within the cash limits. Turn the acquisition into an option that is "
      "exercised only if diligence and partnership data clear defined thresholds (p.14–16).", {})]],
   size=12, anchor=MSO_ANCHOR.MIDDLE, label="revised")

# =====================================================================
# 4. Cash headroom chart
# =====================================================================
s = new_slide("Neither acquisition path keeps cash above the $9.0M board floor once 18 months of operating "
              "losses are counted", "1 · Cash")
tb(s, LM, 1.58, 6.6, 0.5, "Lowest cash balance through end-2028 compared with the $9.0M floor, $M "
   "(0 = at the floor; below 0 = breach)", size=11, bold=True, color=NAVY, label="ct")
cd = CategoryChartData()
cd.categories = ["D · Internal build", "C · Partnership", "B · Staged acquisition", "A · Full cash acquisition"]
cd.add_series("Base case (cross-sell $2.4M)", (11.6, 13.8, -0.8, -8.3))
cd.add_series("Low case (cross-sell $0.8M)", (11.6, 13.8, -1.8, -9.3))
gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(LM), Inches(2.05), Inches(6.6), Inches(4.3), cd)
ch = gf.chart
style_chart_common(ch, legend=True)
plot = ch.plots[0]
plot.gap_width = 60; plot.overlap = -10
for ser, col in zip(plot.series, (BLUE, ORANGE)):
    ser.format.fill.solid(); ser.format.fill.fore_color.rgb = col
    ser.invert_if_negative = False
plot.has_data_labels = True
dl = plot.data_labels
dl.number_format = '+0.0;"−"0.0'; dl.number_format_is_linked = False
dl.position = XL_LABEL_POSITION.OUTSIDE_END
dl.font.size = Pt(10); dl.font.color.rgb = INK
style_axis(ch.category_axis, size=10)
ch.category_axis.tick_label_position = XL_TICK_LABEL_POSITION.LOW
style_axis(ch.value_axis, numfmt='0;"−"0', gridlines=True, size=9)
ch.value_axis.minimum_scale = -12; ch.value_axis.maximum_scale = 16
tb(s, LM, 6.38, 6.6, 0.55, "C assumes zero partner revenue (worst case). D assumes the full $3.4M is spent before "
   "launch. A and B include RouteSprout losses and integration-era support from a July 2027 close.",
   size=9, color=INK2, label="note")
# Right: cash bridge table
tb(s, 7.45, 1.58, 5.33, 0.4, "How Path B falls below the floor, $M", size=11, bold=True, color=NAVY)
data = [
    ["Cash item (Jul 2027 – Dec 2028)", "Base", "Low"],
    ["Unrestricted cash today", "24.0", "24.0"],
    ["Upfront price", "−11.0", "−11.0"],
    ["Integration (Path B estimate)", "−3.5", "−3.5"],
    ["Cash at close (floor + 0.5)", "9.5", "9.5"],
    ["RouteSprout EBITDA (−1.0/yr × 1.5)", "−1.5", "−1.5"],
    ["Integration-era support (−0.85/yr × 1.5)", "−1.3", "−1.3"],
    ["Cross-sell gross profit (linear ramp, 80%)", "+1.4", "+0.5"],
    ["Lowest cash, end-2028", "8.2", "7.2"],
    ["Headroom vs $9.0M floor", "−0.8", "−1.8"],
]
r_ = PP_ALIGN.RIGHT
table(s, 7.45, 2.0, 5.33, 3.9, data, col_w=[3.53, 0.9, 0.9], font=10.5, row_h=0.39,
      align_cols={1: r_, 2: r_}, cell_bold={(4, 1), (4, 2), (8, 1), (8, 2), (9, 1), (9, 2), (4, 0), (8, 0), (9, 0)},
      cell_colors={(9, 1): CRIT, (9, 2): CRIT}, bold_first_col=False, label="bridge")
tb(s, 7.45, 6.0, 5.33, 0.9,
   "Path A is worse at every step: $18.0M + $4.0M = $22.0M leaves $2.0M before any operating losses. "
   "The $15.0M limit on initial spend ($24.0M − $9.0M) rules it out on its own.",
   size=10, color=INK, label="patha")

# =====================================================================
# 5. Path B stress tests
# =====================================================================
s = new_slide("Path B's $0.5M margin is also exposed to three cash calls the deal case does not price: unscoped "
              "integration work, the integration cap and the $7.0M earnout", "1 · Cash")
data = [
    ["Stress", "Evidence in the pack", "Effect on Atlas cash and limits"],
    ["Operating losses before synergies",
     "RouteSprout EBITDA is −$1.0M/yr. Integration-era support costs $0.85M/yr. Cross-sell is unsigned and ramps "
     "over time.",
     "−$1.3M to −$2.3M over 18 months. This alone breaches the $9.0M floor (p.4)."],
    ["Unscoped integration work",
     "30% of the integration work is not yet scoped. The six-month plan assumes zero change-management delay.",
     "Every $1 of overrun is $1 below the floor. Path B's $3.5M estimate leaves $0.5M under the $4.0M cap."],
    ["The $4.0M integration cap",
     "The cap explicitly covers \"systems migration and customer support\". The pack calls the $0.85M/yr "
     "integration-era support \"another\" cost, so it may count.",
     "If it counts: A = $4.0M + $1.3M = $5.3M and B = $3.5M + $1.3M = $4.8M. Both breach the cap. If it does not, it hits cash instead."],
    ["The $7.0M earnout due in 2029",
     "Payable after 2028 if growth and renewal tests pass. The CFO notes an earnout \"does not eliminate future cash "
     "strain\".",
     "Cash is already below the floor at end-2028. Base-case run-rate contribution of $0.92M/yr would need about 7.6 "
     "years to fund it."],
    ["Uptime service credits",
     "Large customers need 99.7% uptime. A missed quarter triggers service credits and renewal risk that the "
     "sellers leave out.",
     "Not quantified in the pack. The risk only runs one way, and a full record migration makes it larger."],
]
table(s, LM, 1.65, CW, 4.75, data, col_w=[2.5, 4.9, 4.833], font=10.5, row_h=[0.38] + [0.87] * 5,
      label="stress")
rect(s, LM, 6.45, CW, 0.45, PANEL)
tb(s, LM + 0.15, 6.43, CW - 0.3, 0.5,
   [[("So what: ", {"bold": True, "color": NAVY}),
     ("the problem is not just the headline price. Any acquisition must leave room for 18 months of losses, a "
      "contingency on unscoped work, and an earnout that does not have to be paid in cash.", {})]],
   size=10.5, anchor=MSO_ANCHOR.MIDDLE, label="sowhat5")

# =====================================================================
# 6. Valuation multiple
# =====================================================================
s = new_slide("On recognised ARR the $18.0M price is 3.75x revenue, 50% higher than the sellers' 2.5x, and "
              "even the $4.8M ARR figure has not been verified", "2 · Value and payback")
tb(s, LM, 1.58, 6.0, 0.4, "Price ÷ revenue measure, multiple (x)", size=11, bold=True, color=NAVY)
cd = CategoryChartData()
cd.categories = ["Sellers' framing\n$18.0M ÷ $7.2M bookings", "Atlas finance\n$18.0M ÷ $4.8M ARR",
                 "Path B upfront only\n$11.0M ÷ $4.8M ARR"]
cd.add_series("Multiple", (2.5, 3.75, 2.29))
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(LM), Inches(2.0), Inches(6.0), Inches(4.3), cd)
ch = gf.chart
style_chart_common(ch, legend=False)
plot = ch.plots[0]; plot.gap_width = 90
ser = plot.series[0]
ser.format.fill.solid(); ser.format.fill.fore_color.rgb = BLUE
for idx, col in ((0, MUTED), (1, BLUE), (2, BLUE_LT)):
    pt = ser.points[idx]
    pt.format.fill.solid(); pt.format.fill.fore_color.rgb = col
plot.has_data_labels = True
plot.data_labels.number_format = '0.0#"x"'; plot.data_labels.number_format_is_linked = False
plot.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
plot.data_labels.font.size = Pt(12); plot.data_labels.font.bold = True
style_axis(ch.category_axis, size=10)
style_axis(ch.value_axis, numfmt='0.0"x"', gridlines=True, size=9)
ch.value_axis.minimum_scale = 0; ch.value_axis.maximum_scale = 4.5
tb(s, LM, 6.35, 6.0, 0.55, "Path B's total, including the full earnout, is also $18.0M, which is 3.75x ARR. "
   "The structure moves when the money is paid, not how much is paid.", size=9.5, color=INK2, label="n6")
tb(s, 6.95, 1.58, 5.83, 0.4, "Why $7.2M of bookings is the wrong denominator", size=11, bold=True, color=NAVY)
tb(s, 6.95, 2.0, 5.83, 4.9, [
    ([("It is not recurring revenue. ", {"bold": True}),
      ("The audit notes say the $7.2M includes multi-year contract value and one-time pilots. It is not a current "
       "recurring revenue rate.", {})], {"bullet": True, "space_after": 8}),
    ([("Pilots are counted as if they renew. ", {"bold": True}),
      ("The sellers make no adjustment for one-year pilots that will not renew, so bookings overstate both value and "
       "retention-adjusted revenue.", {})], {"bullet": True, "space_after": 8}),
    ([("Atlas policy is to value on recognised ARR. ", {"bold": True}),
      ("Corporate finance values recurring revenue on ARR ($4.8M), which gives 3.75x.", {})],
     {"bullet": True, "space_after": 8}),
    ([("Even $4.8M is unverified. ", {"bold": True}),
      ("There is no QoE review and no independently verified ARR schedule. The 42% growth figure stops "
       "before the last quarter.", {})], {"bullet": True, "space_after": 8}),
    ([("There are no earnings to support the price. ", {"bold": True}),
      ("EBITDA is −$1.0M, including founder salaries, so the price relies entirely on revenue quality and "
       "on synergies.", {})], {"bullet": True, "space_after": 8}),
], size=11, label="why6")

# =====================================================================
# 7. Contribution bridge
# =====================================================================
s = new_slide("The $2.4M cross-sell is ARR, not EBITDA. After margin, support and RouteSprout's losses it adds "
              "about $0.1M a year, and loses $1.2M a year in the low case", "2 · Value and payback")
tb(s, LM, 1.58, 5.6, 0.4, "Annual run-rate incremental contribution to Atlas, $M", size=11, bold=True, color=NAVY)
cd = CategoryChartData()
cd.categories = ["Sellers' pitch\n($2.4M as EBITDA)", "Evidence-based\nbase case", "Evidence-based\nlow case"]
cd.add_series("Contribution", (2.40, 0.07, -1.21))
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(LM), Inches(2.0), Inches(5.6), Inches(4.4), cd)
ch = gf.chart
style_chart_common(ch, legend=False)
plot = ch.plots[0]; plot.gap_width = 90
ser = plot.series[0]; ser.invert_if_negative = False
for idx, col in ((0, MUTED), (1, BLUE), (2, RED)):
    pt = ser.points[idx]; pt.format.fill.solid(); pt.format.fill.fore_color.rgb = col
plot.has_data_labels = True
plot.data_labels.number_format = '+0.00;"−"0.00'; plot.data_labels.number_format_is_linked = False
plot.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
plot.data_labels.font.size = Pt(12); plot.data_labels.font.bold = True
style_axis(ch.category_axis, size=10)
ch.category_axis.tick_label_position = XL_TICK_LABEL_POSITION.LOW
style_axis(ch.value_axis, numfmt='0.0;"−"0.0', gridlines=True, size=9)
ch.value_axis.minimum_scale = -2.0; ch.value_axis.maximum_scale = 3.0
tb(s, 6.45, 1.58, 6.33, 0.4, "Bridge from cross-sell ARR to contribution, $M per year", size=11, bold=True, color=NAVY)
data = [
    ["Step", "Base", "Low", "Basis"],
    ["Cross-sell ARR by end-2028", "2.40", "0.80", "Sales VP / finance"],
    ["× 80% incremental gross margin", "1.92", "0.64", "Pack, §5"],
    ["− Integration-era support", "−0.85", "−0.85", "Pack, §5"],
    ["= Cross-sell contribution", "1.07", "−0.21", ""],
    ["+ RouteSprout standalone EBITDA", "−1.00", "−1.00", "FY2026, held flat"],
    ["= Contribution in integration era", "0.07", "−1.21", "Chart"],
    ["Memo: after support ends", "0.92", "−0.36", "Assumption"],
]
table(s, 6.45, 2.0, 6.33, 3.25, data, col_w=[2.85, 0.8, 0.8, 1.88], font=10.5, row_h=0.4,
      align_cols={1: r_, 2: r_}, cell_bold={(4, 1), (4, 2), (6, 1), (6, 2), (4, 0), (6, 0)},
      cell_colors={(6, 2): CRIT, (4, 2): CRIT}, bold_first_col=False, label="bridge7")
tb(s, 6.45, 5.35, 6.33, 1.55, [
    ([("Still optimistic: ", {"bold": True}),
      ("it ignores the sellers' assumption of 100% renewal. At 21% logo churn, about $1.0M of RouteSprout's $4.8M ARR is "
       "at risk each year (logo churn used as a proxy for revenue churn).", {})], {"bullet": True, "space_after": 4}),
    ([("No cost savings are assumed, ", {"bold": True}),
      ("as the pack instructs, and the low case is the one finance considers plausible if churn persists.", {})],
     {"bullet": True}),
], size=10.5, label="still7")

# =====================================================================
# 8. Payback table
# =====================================================================
s = new_slide("Buying takes more than 15 years to pay back, and never does in the low case. Building takes "
              "about 5 years, and partnering risks at most $1.2M", "2 · Value and payback")
data = [
    ["Path", "Cash committed, $M", "Annual run-rate contribution, $M\nbase / low",
     "Simple payback (undiscounted)\nbase / low", "Comment"],
    ["A · Full cash acquisition", "22.0", "+0.92 / −0.36\n(+0.07 / −1.21 during integration)",
     "≈24 years / never", "22.0 ÷ 0.92. RouteSprout's losses absorb most of the cross-sell gross profit."],
    ["B · Staged acquisition", "14.5 upfront\n+ 7.0 earnout", "+0.92 / −0.36\n(same business)",
     "≈16 years (23 with earnout) / never", "Staging lowers upfront cash, not the total. The earnout is paid only "
     "in the base case."],
    ["C · Partnership", "1.2 (two-year minimum)", "+0.46 / −0.25\n(after the $0.6M/yr minimum)",
     "≈1.1 years / not within the 2-year term", "Breaks even at $1.36M of routing ARR. The worst-case loss is $1.2M; in the "
     "low case it is about $0.5M over two years."],
    ["D · Internal build", "3.4 through 2028\n+ 0.4/yr operations", "+0.64 from 2029\n(low case not given)",
     "≈5.3 years after launch", "1.3 × 80% − 0.4 = 0.64. Assumes an on-time launch. It also displaces the compliance "
     "upgrade, at an unestimated cost."],
]
table(s, LM, 1.65, CW, 4.2, data, col_w=[2.2, 1.9, 2.75, 2.35, 3.033], font=10.5,
      row_h=[0.6, 0.9, 0.9, 0.9, 0.9], label="payback")
rect(s, LM, 6.0, CW, 0.88, PANEL)
tb(s, LM + 0.15, 6.0, CW - 0.3, 0.88, [
    [("How to read this: ", {"bold": True, "color": NAVY}),
     ("payback = cash committed ÷ annual contribution after that path's running costs. It is deliberately simple. The board asked us "
      "not to build a precise DCF from inputs we do not have. For C, cross-sell ARR uses the same $0.8–2.4M range "
      "at 80% margin and Atlas's 55% share. Because the partner offering is limited, the low end is more likely.", {})]],
   size=10.5, anchor=MSO_ANCHOR.MIDDLE, label="read8")

# =====================================================================
# 9. Customer base
# =====================================================================
s = new_slide("RouteSprout's customers are churning faster and its revenue is concentrated, yet the "
              "sellers' case assumes every account renews", "3 · Customer continuity and execution")
tb(s, LM, 1.58, 3.7, 0.4, "Annual customer logo churn, %", size=11, bold=True, color=NAVY)
cd = CategoryChartData()
cd.categories = ["FY2024", "FY2026", "Sellers' case"]
cd.add_series("Churn", (0.12, 0.21, 0.0))
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(LM), Inches(2.0), Inches(3.7), Inches(3.7), cd)
ch = gf.chart; style_chart_common(ch, legend=False)
plot = ch.plots[0]; plot.gap_width = 80
ser = plot.series[0]
for idx, col in ((0, BLUE_LT), (1, BLUE), (2, MUTED)):
    pt = ser.points[idx]; pt.format.fill.solid(); pt.format.fill.fore_color.rgb = col
plot.has_data_labels = True
plot.data_labels.number_format = '0%'; plot.data_labels.number_format_is_linked = False
plot.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
plot.data_labels.font.size = Pt(12); plot.data_labels.font.bold = True
style_axis(ch.category_axis, size=10)
style_axis(ch.value_axis, numfmt='0%', gridlines=True, size=9)
ch.value_axis.minimum_scale = 0; ch.value_axis.maximum_scale = 0.25
tb(s, LM, 5.75, 3.7, 0.6, "The sellers' case assumes 100% renewal of all 310 accounts, which is 0% churn.",
   size=9.5, color=INK2, label="n9a")

tb(s, 4.55, 1.58, 4.0, 0.4, "FY2026 ARR by account group, $M", size=11, bold=True, color=NAVY)
cd = CategoryChartData()
cd.categories = ["41 large accounts", "269 other accounts"]
cd.add_series("ARR", (2.78, 2.02))
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(4.55), Inches(2.0), Inches(4.0), Inches(3.7), cd)
ch = gf.chart; style_chart_common(ch, legend=False)
plot = ch.plots[0]; plot.gap_width = 80
ser = plot.series[0]; ser.format.fill.solid(); ser.format.fill.fore_color.rgb = BLUE
plot.has_data_labels = True
plot.data_labels.number_format = '0.00'; plot.data_labels.number_format_is_linked = False
plot.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
plot.data_labels.font.size = Pt(12); plot.data_labels.font.bold = True
style_axis(ch.category_axis, size=10)
style_axis(ch.value_axis, numfmt='0.0', gridlines=True, size=9)
ch.value_axis.minimum_scale = 0; ch.value_axis.maximum_scale = 3.5
tb(s, 4.55, 5.75, 4.0, 0.6, "58% vs 42% of $4.8M ARR. That is about $68K per large account against about $7.5K per "
   "other account.", size=9.5, color=INK2, label="n9b")

tb(s, 8.85, 1.58, 3.93, 0.4, "Implications", size=11, bold=True, color=NAVY)
tb(s, 8.85, 2.0, 3.93, 4.9, [
    ([("Churn is rising: ", {"bold": True}), ("21% of logos, against 12% two years earlier. About $1.0M of ARR is at risk each year.", {})],
     {"bullet": True, "space_after": 6}),
    ([("Concentration magnifies the risk: ", {"bold": True}),
      ("losing a handful of the 41 large accounts would wipe out a year of cross-sell.", {})], {"bullet": True, "space_after": 6}),
    ([("People drive renewals, not features: ", {"bold": True}),
      ("customer success interviews found account managers drive renewal decisions, so RouteSprout's account managers "
       "matter as much as its code.", {})], {"bullet": True, "space_after": 6}),
    ([("Interface timing matters: ", {"bold": True}),
      ("the product VP warns that replacing RouteSprout's interface before large customers renew could add churn.", {})],
     {"bullet": True, "space_after": 6}),
    ([("No cohort data: ", {"bold": True}),
      ("we cannot yet tell whether churn sits in small or large accounts. That is the first diligence item.", {})],
     {"bullet": True}),
], size=10.5, label="impl9")

# =====================================================================
# 10. Evidence quality
# =====================================================================
s = new_slide("The synergy, retention and integration claims rest on correlations and untested plans, "
              "not on evidence of cause", "3 · Customer continuity and execution")
data = [
    ["Claim in the deal case", "What the evidence actually shows", "How we treat it"],
    ["\"Customers who use routing renew at 95%, so routing causes retention\"",
     "Routing users are mostly larger, multi-branch firms with dedicated customer success teams. Smaller non-users "
     "renew at 78%. The feature effect is not isolated.",
     "We credit no retention uplift to Atlas's core base, and we keep RouteSprout's account managers."],
    ["\"Integration works when the product is under one general manager\"",
     "The cited companies were on average twice as large, with lower churn. The link between integration spend and "
     "cross-sell is a correlation with no causal identification.",
     "Not transferable. We do not underwrite the $2.4M cross-sell. Earnouts carry that risk instead."],
    ["\"Six months and $4.0M to integrate\"",
     "30% of the work is unscoped and the plan assumes zero change-management delay. API plus single sign-on (SSO) "
     "is simpler than migrating records and support.",
     "Integrate through the API first. Scope 100% of the work and price the contingency before signing."],
    ["\"2.5x recurring revenue\" and $7.2M of \"annual recurring new sales\"",
     "The $7.2M includes multi-year contract value and one-time pilots. It is unsuitable for valuation or for "
     "projecting retention.",
     "Value on QoE-verified recognised ARR only."],
    ["Key people stay (implicit)",
     "A substantial part of the value depends on keeping key engineers for at least two years. No agreements "
     "are in place.",
     "Signed 24-month retention agreements become a condition of the deal."],
]
table(s, LM, 1.65, CW, 5.2, data, col_w=[3.0, 5.2, 4.033], font=10.5, row_h=[0.38] + [0.96] * 5,
      label="claims")

# =====================================================================
# 11. Scorecard
# =====================================================================
s = new_slide("Against the board's four criteria, only the partnership passes in 2027. The build is the "
              "fallback, not the first move", "4 · Alternatives")
cols = ["A · Full cash\nacquisition", "B · Staged\nacquisition", "C · Commercial\npartnership", "D · Internal\nbuild"]
rows = [
    ("Cash vs $9.0M floor",
     [("FAIL", "$22.0M out. Cash is at $2.0M before losses."),
      ("FAIL", "$14.5M at signing, then $7.2–8.2M by end-2028."),
      ("PASS", "At most $1.2M. Cash stays at $22.8M or more."),
      ("PASS", "$3.4M. Cash stays at $20.6M or more.")]),
    ("Payback",
     [("FAIL", "About 24 years in the base case, never in the low case."),
      ("FAIL", "About 16 years (23 with the earnout), never in the low case."),
      ("WATCH", "Breaks even at $1.36M of routing ARR. Loss capped at $1.2M."),
      ("WATCH", "About 5.3 years after a late-2028 launch.")]),
    ("Customer continuity",
     [("FAIL", "Full migration before renewals, with churn at 21%."),
      ("WATCH", "Same migration risk. The earnout ties sellers to renewals."),
      ("PASS", "No migration. Prospects are served from summer 2027."),
      ("WATCH", "Nothing to offer prospects until late 2028.")]),
    ("Execution capacity",
     [("FAIL", "30% unscoped, zero-delay plan, key engineers at risk."),
      ("FAIL", "Same integration load on a thinner budget."),
      ("WATCH", "Depends on the partner's viability. Roadmap has to be shared."),
      ("FAIL", "At least 18 months. Displaces the compliance upgrade.")]),
    ("Strategic fit (tie-break)",
     [("PASS", "Owns routing and RouteSprout's team."),
      ("PASS", "Owns routing once integrated."),
      ("WATCH", "No ownership, but first refusal keeps the option."),
      ("PASS", "Atlas owns the IP, but it arrives late.")]),
]
x0, y0 = LM, 1.62
lw, cwid, hh, rh = 2.05, (CW - 2.05) / 4, 0.5, 0.87
rect(s, x0, y0, CW, hh, NAVY)
tb(s, x0, y0, lw, hh, "Criterion", size=11, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
for i, cname in enumerate(cols):
    fillc = BLUE if i == 2 else NAVY
    rect(s, x0 + lw + i * cwid, y0, cwid, hh, fillc)
    tb(s, x0 + lw + i * cwid, y0, cwid, hh, cname, size=11, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE,
       align=PP_ALIGN.CENTER, spacing=1.0, label="colhead")
for r, (crit, cells) in enumerate(rows):
    yy = y0 + hh + r * rh
    if r % 2 == 1:
        rect(s, x0, yy, CW, rh, PANEL)
    tb(s, x0, yy, lw, rh, crit, size=11, bold=True, color=NAVY, anchor=MSO_ANCHOR.MIDDLE, label="crit")
    for i, (st, txt) in enumerate(cells):
        cx = x0 + lw + i * cwid
        status_chip(s, cx + 0.1, yy + 0.06, st)
        tb(s, cx + 0.1, yy + 0.34, cwid - 0.2, rh - 0.35, txt, size=9.5, color=INK, label="cell")
    hline(s, x0, yy + rh, CW)
# highlight partnership column
hl = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x0 + lw + 2 * cwid), Inches(y0),
                        Inches(cwid), Inches(hh + 5 * rh))
hl.fill.background(); hl.line.color.rgb = BLUE; hl.line.width = Pt(2.25); hl.shadow.inherit = False
tb(s, LM, 6.52, CW, 0.45, "Ratings: ✔ Pass = meets the board limit with margin; ! Watch = meets it with a risk to manage; "
   "✖ Fail = breaches a hard limit or has no credible path. Only one routing strategy can run in 2027.",
   size=9, color=INK2, label="legend11")

# =====================================================================
# 12. Partner vs acquire contribution lines
# =====================================================================
s = new_slide("The partnership earns more than ownership at any routing ARR below about $3.5M, well above the "
              "Sales VP's unsigned $2.4M base case", "4 · Alternatives")
tb(s, LM, 1.58, 7.9, 0.4, "Annual run-rate contribution to Atlas by routing ARR sold, $M (before acquisition capital)",
   size=11, bold=True, color=NAVY)
xs = [i * 0.25 for i in range(17)]
cd = XyChartData()
s1 = cd.add_series("Partnership (55% of gross profit, less $0.6M/yr minimum)")
for x in xs:
    s1.add_data_point(x, round(0.44 * x - 0.6, 3))
s2 = cd.add_series("Acquisition, integration era (less $1.0M losses and $0.85M support)")
for x in xs:
    s2.add_data_point(x, round(0.8 * x - 1.85, 3))
s3 = cd.add_series("Acquisition, after integration support ends")
for x in xs:
    s3.add_data_point(x, round(0.8 * x - 1.0, 3))
gf = s.shapes.add_chart(XL_CHART_TYPE.XY_SCATTER_LINES_NO_MARKERS, Inches(LM), Inches(2.0), Inches(7.9),
                        Inches(4.55), cd)
ch = gf.chart
style_chart_common(ch, legend=True, legend_pos=XL_LEGEND_POSITION.BOTTOM, size=9.5)
for ser, col, w in zip(ch.plots[0].series, (BLUE, ORANGE, AQUA), (2.5, 2.25, 2.25)):
    ser.format.line.color.rgb = col; ser.format.line.width = Pt(w)
    ser.smooth = False
    ser.marker.style = None
from pptx.enum.chart import XL_MARKER_STYLE
for ser in ch.plots[0].series:
    ser.marker.style = XL_MARKER_STYLE.NONE
va, ca = ch.value_axis, ch.category_axis
style_axis(va, numfmt='0.0;"−"0.0', gridlines=True, size=9)
style_axis(ca, numfmt='0.0', gridlines=False, size=9)
va.minimum_scale = -2.0; va.maximum_scale = 2.5; va.major_unit = 0.5
ca.minimum_scale = 0; ca.maximum_scale = 4.0; ca.major_unit = 0.5
ca.tick_label_position = XL_TICK_LABEL_POSITION.LOW
ca.has_title = True; ca.axis_title.text_frame.text = "Routing ARR sold to customers, $M"
ca.axis_title.text_frame.paragraphs[0].runs[0].font.size = Pt(9.5)
ca.axis_title.text_frame.paragraphs[0].runs[0].font.bold = False
# annotate the low / base cases with labels above plot (text, not lines, to avoid misplacement)
tb(s, 8.65, 1.58, 4.13, 0.4, "Reading the crossover", size=11, bold=True, color=NAVY)
data = [
    ["Routing ARR", "Partner", "Acquire*", "Better"],
    ["$0.8M (low)", "−0.25", "−1.21", "Partner"],
    ["$2.4M (base)", "+0.46", "+0.07", "Partner"],
    ["$3.47M", "+0.93", "+0.93", "Equal"],
]
table(s, 8.65, 2.0, 4.13, 1.6, data, col_w=[1.33, 0.9, 0.95, 0.95], font=10.5, row_h=0.4,
      align_cols={1: r_, 2: r_}, label="xover")
tb(s, 8.65, 3.62, 4.13, 0.45, "* Integration era: 0.8 × ARR − 1.85. Partner: 0.44 × ARR − 0.6.", size=9,
   color=INK2, label="fn12")
tb(s, 8.65, 4.12, 4.13, 2.8, [
    ([("Ownership wins only at scale: ", {"bold": True}),
      ("0.36 × ARR = 1.25 gives $3.47M. Once support ends and the partner minimum lapses, the crossover is still "
       "$2.78M (0.8x − 1.0 = 0.44x).", {})], {"bullet": True, "space_after": 5}),
    ([("Capital is excluded: ", {"bold": True}),
      ("the chart ignores the $14.5–22.0M paid to acquire. Including it widens the partnership's lead.", {})],
     {"bullet": True, "space_after": 5}),
    ([("Assumption: ", {"bold": True}),
      ("partner-sold routing earns the same 80% gross margin, and the $1.2M minimum is a fixed cost that cannot "
       "be recouped.", {})], {"bullet": True}),
], size=10.5, label="xs12")

# =====================================================================
# 13. Timeline / build
# =====================================================================
s = new_slide("Building is affordable but cannot ship before late 2028, so it misses the renewal cycles the "
              "partnership can serve from summer 2027", "4 · Alternatives")
quarters = ["Q1\n2027", "Q2", "Q3", "Q4", "Q1\n2028", "Q2", "Q3", "Q4", "Q1\n2029", "Q2"]
gx, gy, labw = LM, 1.75, 1.7
qw = (8.3 - labw) / 10
for i, q in enumerate(quarters):
    tb(s, gx + labw + i * qw, gy, qw, 0.45, q, size=9, color=INK2, align=PP_ALIGN.CENTER, spacing=0.95,
       margin=0.01, label="q")
hline(s, gx, gy + 0.5, 8.3)
lanes = [
    ("C · Partnership", [(1, 1, RULE, "Contract"), (2, 8, BLUE, "Live summer 2027, two-year term to mid-2029")]),
    ("A/B · Acquisition", [(1, 1, RULE, "Diligence"), (2, 2, ORANGE, "Integrate (6 mo plan)"),
                           (4, 2, RGBColor(0xF7, 0xC3, 0xAE), "Delay risk")]),
    ("D · Internal build", [(1, 6, RULE, "Build ≥ 18 months"), (7, 1, AQUA, "Launch"),
                            (8, 2, RGBColor(0xBF, 0xE9, 0xD9), "Ramp to $1.3M ARR")]),
]
for li, (name, bars) in enumerate(lanes):
    ly = gy + 0.7 + li * 0.95
    tb(s, gx, ly, labw, 0.55, name, size=11, bold=True, color=NAVY, anchor=MSO_ANCHOR.MIDDLE, label="lane")
    for (start, dur, col, txt) in bars:
        rect(s, gx + labw + start * qw + 0.02, ly + 0.08, dur * qw - 0.04, 0.42, col)
        tb(s, gx + labw + start * qw + 0.02, ly + 0.08, dur * qw - 0.04, 0.42, txt, size=8.5 if dur == 1 else 9,
           color=INK if col in (RULE,) or txt in ("Delay risk", "Ramp to $1.3M ARR") else WHITE,
           anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER, margin=0.02, label="bar")
mx = gx + labw + 0.0 * qw
vline(s, gx + labw + 0.33 * qw, gy + 0.5, 2.95, color=NAVY, weight=1.25, dash=True)
tb(s, gx + labw + 0.33 * qw - 0.6, gy + 3.45, 1.4, 0.3, "Board, Mar 2027", size=9, color=NAVY, bold=True,
   align=PP_ALIGN.CENTER)
vline(s, gx + labw + 4.5 * qw, gy + 0.5, 2.95, color=BLUE, weight=1.25, dash=True)
tb(s, gx + labw + 4.5 * qw - 0.8, gy + 3.45, 1.6, 0.3, "Gate, Q1 2028", size=9, color=BLUE, bold=True,
   align=PP_ALIGN.CENTER)
tb(s, LM, 5.65, 8.3, 1.25, [
    ([("Timing assumptions: ", {"bold": True}),
      ("acquisition closes after a roughly 3-month diligence. The build starts after the March 2027 board and takes "
       "at least 18 months, so launch comes no earlier than Q4 2028. Atlas can run only one major routing strategy "
       "in 2027.", {})], {}),
], size=10, color=INK2, label="timing13")
tb(s, 9.15, 1.58, 3.63, 0.4, "The build case in numbers", size=11, bold=True, color=NAVY)
tb(s, 9.15, 2.0, 3.63, 4.9, [
    ([("$3.4M ", {"bold": True}), ("through 2028, plus $0.4M a year in operations after launch.", {})],
     {"bullet": True, "space_after": 5}),
    ([("$0.64M a year ", {"bold": True}), ("in contribution if $1.3M ARR arrives (1.3 × 80% − 0.4). "
                                    "Payback is about 5.3 years after launch.", {})], {"bullet": True, "space_after": 5}),
    ([("The ARR timing is doubtful: ", {"bold": True}),
      ("the pack calls it \"2028 ARR\", but a late-2028 launch makes that unlikely. We treat it as a 2029 "
       "run-rate.", {})], {"bullet": True, "space_after": 5}),
    ([("Hidden cost: ", {"bold": True}),
      ("it displaces a planned compliance upgrade. The customer cost of that delay has not been estimated.", {})],
     {"bullet": True, "space_after": 5}),
    ([("Role: ", {"bold": True}),
      ("the fallback if the partnership underperforms and the buy terms fail at the 2028 gate.", {})],
     {"bullet": True}),
], size=10.5, label="build13")

# =====================================================================
# 14. Partnership terms
# =====================================================================
s = new_slide("Sign the partnership on terms that cap cost, protect uptime and stop a competitor from "
              "capturing RouteSprout", "5 · Terms")
left = [
    ("Scope and price (as offered)", "Non-exclusive routing API with a $1.2M two-year minimum. Gross profit splits 55% to "
     "Atlas and 45% to RouteSprout."),
    ("Ask: credit the minimum", "Count minimum payments against RouteSprout's 45% share. This cuts the "
     "$1.36M break-even and the $1.2M maximum loss."),
    ("Service level", "At least 99.7% quarterly uptime, with service credits passed back to Atlas to match the "
     "credits Atlas owes its large customers."),
    ("Segment exclusivity (ask)", "Exclusivity in utilities and repair contractors, Atlas's core segments. "
     "Negotiate for it, but do not make it a condition."),
]
right = [
    ("Change of control", "Right of first refusal on any sale of RouteSprout, plus a right to terminate if a "
     "competitor buys it. The founders want to sell, so this is the key protection."),
    ("Pre-agreed purchase option", "Attach the conditional term sheet (p.15), exercisable at the Q1 2028 gate. "
     "Partnership fees paid are credited against the price."),
    ("Information rights", "Customer-level churn cohorts, the ARR schedule and pipeline data. These double as "
     "diligence evidence."),
    ("Continuity and roadmap", "Source-code escrow and data portability in case RouteSprout fails "
     "(EBITDA −$1.0M). Share only interface-level roadmap, through a clean team."),
]
for col_i, items in enumerate((left, right)):
    cx = LM + col_i * (CW / 2 + 0.1)
    w = CW / 2 - 0.1
    tb(s, cx, 1.6, w, 0.35, ("Commercial terms" if col_i == 0 else "Protection terms"), size=12, bold=True,
       color=BLUE)
    yy = 2.0
    for head, body in items:
        rect(s, cx, yy, 0.06, 1.0, BLUE if col_i == 0 else NAVY)
        tb(s, cx + 0.15, yy - 0.02, w - 0.15, 0.32, head, size=11.5, bold=True, color=NAVY, label="h14")
        tb(s, cx + 0.15, yy + 0.3, w - 0.15, 0.72, body, size=10.5, color=INK, label="b14")
        yy += 1.13
rect(s, LM, 6.55, CW, 0.38, PANEL)
tb(s, LM + 0.15, 6.55, CW - 0.3, 0.38,
   [[("Walk-away: ", {"bold": True, "color": NAVY}),
     ("if RouteSprout refuses first-refusal or change-of-control protection, the roadmap risk outweighs the "
      "speed benefit. Reopen the build decision.", {})]], size=10, anchor=MSO_ANCHOR.MIDDLE, label="walk14")

# =====================================================================
# 15. Conditional acquisition term sheet
# =====================================================================
s = new_slide("If the evidence clears, buy on conditional terms: at most $8.5M upfront, up to $9.5M more if "
              "earned, and no payment that takes cash below the floor", "5 · Terms")
tb(s, LM, 1.58, 4.6, 0.4, "Deriving the upfront ceiling, $M", size=11, bold=True, color=NAVY)
data = [
    ["Item", "$M"],
    ["Cash above the $9.0M floor", "15.0"],
    ["− Integration, at the $4.0M cap\n(30% unscoped, so assume it is all used)", "−4.0"],
    ["− 18-month operating drag, low case\n(losses + support − cross-sell gross profit)", "−2.3"],
    ["= Maximum affordable upfront", "8.7"],
    ["Recommended ceiling (≈1.8x $4.8M ARR)", "8.5"],
]
table(s, LM, 2.0, 4.6, 3.1, data, col_w=[3.8, 0.8], font=10.5, row_h=[0.38, 0.42, 0.62, 0.62, 0.48, 0.48],
      align_cols={1: r_}, cell_bold={(4, 0), (4, 1), (5, 0), (5, 1)}, cell_fills={(5, 0): BLUE_LT, (5, 1): BLUE_LT},
      bold_first_col=False, label="ceiling")
tb(s, LM, 5.2, 4.6, 1.7, [
    ([("The ceiling drops $1-for-$1 ", {"bold": True}),
      ("for any partnership fees not credited at close, and for any audited integration budget above the cap.", {})],
     {"bullet": True, "space_after": 4}),
    ([("The $0.2M buffer is thin. ", {"bold": True}),
      ("If diligence shows churn concentrated in large accounts, do not raise the upfront to compensate.", {})],
     {"bullet": True}),
], size=10, label="notes15")
data = [
    ["Term", "Proposed structure"],
    ["Upfront cash", "At most $8.5M, priced on QoE-verified recognised ARR excluding pilots. Reduce by about 1.8x any ARR shortfall."],
    ["Earnout", "Up to $9.5M, so the total stays within the sellers' $18.0M headline. Measured over 2028–29: top-41 ARR "
                "retained, logo churn at or below 12%, signed cross-sell ARR in bands from $1.4M to $2.4M, and 99.7% uptime."],
    ["Payment protection", "Pay the earnout only while cash stays above $9.0M plus a buffer. Defer any excess, or settle "
                           "it in Atlas equity if shareholders approve."],
    ["Integration", "API plus single sign-on first. No interface replacement or record migration before large-account "
                    "renewals. Fully scoped budget of no more than $4.0M, including support."],
    ["People", "24-month retention agreements for key engineers and account managers, signed before close."],
    ["Walk-away", "If the sellers demand more than $8.5M upfront or all cash, keep the partnership and do not buy."],
]
table(s, 5.45, 1.6, 7.33, 5.3, data, col_w=[1.6, 5.73], font=10.5,
      row_h=[0.36, 0.72, 1.05, 0.8, 0.85, 0.62, 0.62], label="terms")

# =====================================================================
# 16. What changes the recommendation
# =====================================================================
s = new_slide("Six pieces of missing information would change the recommendation, and each has a threshold "
              "set in advance", "5 · Terms")
data = [
    ["Information", "Today", "Threshold to proceed with buying", "If it is not met"],
    ["1. QoE-verified ARR", "$4.8M, unverified. Bookings include pilots.",
     "Recognised ARR of at least $4.8M, excluding pilots", "Cut the price about 1.8x per $1 of shortfall, or walk away"],
    ["2. Customer-level churn cohort", "21% logo churn, no cohort data",
     "Churn falling toward 12% (FY2024), and stable top-41 accounts", "Stay with the partnership. Do not buy."],
    ["3. Signed routing demand", "$0 signed. $2.4M is the Sales VP's view.",
     "At least $1.36M run-rate shows demand. About $2.3M is needed to cover RouteSprout's losses.",
     "Below $1.36M, reconsider routing altogether, including the build"],
    ["4. RouteSprout standalone EBITDA", "−$1.0M a year",
     "At breakeven, ownership needs only about $1.06M of cross-sell (0.85 ÷ 0.8)", "Keep the earnout weighted to results"],
    ["5. Audited integration budget", "30% unscoped, zero-delay plan",
     "Fully scoped at no more than $4.0M, including support and contingency", "Do not buy"],
    ["6. Key people and seller terms", "No retention agreements. $18.0M all cash.",
     "24-month agreements signed, and sellers accept at most $8.5M upfront", "Keep the partnership. Revisit the build in 2028."],
]
table(s, LM, 1.65, CW, 4.75, data, col_w=[2.55, 2.85, 3.9, 2.933], font=10.5,
      row_h=[0.38, 0.7, 0.7, 0.85, 0.7, 0.7, 0.7], label="triggers")
rect(s, LM, 6.48, CW, 0.42, PANEL)
tb(s, LM + 0.15, 6.48, CW - 0.3, 0.42,
   [[("Early trigger: ", {"bold": True, "color": NAVY}),
     ("if a competing buyer emerges, use the right of first refusal on the pre-agreed terms, but only if items 1, 2 "
      "and 5 have already cleared.", {})]], size=10.5, anchor=MSO_ANCHOR.MIDDLE, label="early16")

# =====================================================================
# 17. Roadmap & board asks
# =====================================================================
s = new_slide("In March 2027 the board should approve the partnership, fund diligence and set the walk-away "
              "terms. The decision to buy follows at a Q1 2028 gate", "Next steps")
tb(s, LM, 1.6, 5.9, 0.35, "Decisions requested in March 2027", size=12, bold=True, color=BLUE)
asks = [
    "Decline the $18.0M all-cash proposal (Path A) and the staged deal as structured (Path B).",
    "Approve the two-year RouteSprout partnership (at most $1.2M minimum) with the protections on p.14.",
    "Approve preliminary diligence: QoE, customer cohorts, integration scoping and key-person review. The CFO will "
    "size the budget, which the pack does not give.",
    "Mandate negotiation of the conditional term sheet: at most $8.5M upfront and up to $9.5M earned, "
    "with a set walk-away.",
    "Defer the internal build, and revisit it at the gate if the partnership underperforms.",
]
yy = 2.05
for i, a in enumerate(asks, 1):
    rect(s, LM, yy + 0.03, 0.36, 0.36, NAVY, shape=MSO_SHAPE.OVAL)
    tb(s, LM, yy + 0.03, 0.36, 0.36, str(i), size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER,
       anchor=MSO_ANCHOR.MIDDLE, margin=0.0)
    tb(s, LM + 0.5, yy, 5.4, 0.85, a, size=11, color=INK, label="ask")
    yy += 0.9
tb(s, 6.85, 1.6, 5.93, 0.35, "Sequence after approval", size=12, bold=True, color=BLUE)
steps = [
    ("Apr–Jun 2027", "Sign the partnership. Run diligence in parallel and negotiate the conditional term sheet."),
    ("Summer 2027", "Routing goes live with the enterprise prospects that asked for it. Start tracking attach and ARR."),
    ("Q3–Q4 2027", "QoE and cohort results arrive. Watch the RouteSprout renewal outcomes for its 41 large accounts."),
    ("Q1 2028 gate", "Buy if all six thresholds are met (p.16). Otherwise continue the partnership, or start the build "
                     "if demand is proven but the partner falls short."),
    ("Any time", "If a competing bid emerges, apply the early trigger (p.16)."),
]
yy = 2.05
for when, what in steps:
    rect(s, 6.85, yy, 1.55, 0.72, PANEL)
    tb(s, 6.85, yy, 1.55, 0.72, when, size=10.5, bold=True, color=NAVY, anchor=MSO_ANCHOR.MIDDLE,
       align=PP_ALIGN.CENTER, label="when")
    tb(s, 8.5, yy, 4.28, 0.78, what, size=10.5, color=INK, anchor=MSO_ANCHOR.MIDDLE, label="what")
    yy += 0.88
tb(s, LM, 6.55, CW, 0.4, "Interpretation: partnering with RouteSprout in 2027 and buying it in 2028 counts as one routing "
   "strategy (the same product), so the plan respects the one-strategy rule.", size=9.5, color=INK2,
   label="interp")

# =====================================================================
# 18. Risks
# =====================================================================
s = new_slide("The recommendation carries five main risks. Each has a mitigation, and the cash downside "
              "is capped at $1.2M", "Risks")
data = [
    ["Risk", "Why it matters", "Mitigation", "Residual exposure"],
    ["RouteSprout is sold to a competitor during the partnership",
     "The founders want to sell. Atlas will have shared roadmap details.",
     "Right of first refusal, termination on change of control, interface-only roadmap through a clean team",
     "Medium. Atlas would lose its routing supplier, and the build becomes the fallback."],
    ["The partner offering is too limited for enterprise prospects",
     "The partner offer is \"limited\". Prospects may want deep integration.",
     "Pilot with the requesting prospects in summer 2027. Measure attach before the gate.",
     "Medium. Prospects may wait for the 2028 decision."],
    ["Routing ARR stays below the $1.36M break-even",
     "The $1.2M minimum is a fixed cost.",
     "Ask for the minimum to be credited against the 45% share. Weight the gate to signed ARR.",
     "Low. At most $1.2M; about $0.5M net in the low case."],
    ["RouteSprout fails financially",
     "EBITDA is −$1.0M and churn is 21%. Its cash position is unknown.",
     "Source-code escrow, data portability and uptime service credits. Our minimum also funds the partner.",
     "Medium. Service disruption, so we need an SLA tied to 99.7%."],
    ["The sellers reject the conditional terms",
     "The founders asked for $18.0M in cash.",
     "Walk away. The partnership meets the customer need without ownership.",
     "Low. We give up the option of owning routing, not the capability."],
]
table(s, LM, 1.65, CW, 5.2, data, col_w=[2.6, 3.0, 3.6, 3.033], font=10.5,
      row_h=[0.38] + [0.96] * 5, label="risks")

# =====================================================================
# 19. Appendix: assumptions register
# =====================================================================
s = new_slide("Appendix: the analysis separates pack evidence from team assumptions, and each assumption "
              "is conservative or is tested on the slide that uses it", "Appendix · Assumptions register")
data = [
    ["Item", "Type", "Value used", "Why / sensitivity"],
    ["Acquisition close timing", "Assumption", "July 2027, so 18 months to end-2028",
     "After a March board and about 3 months of diligence. A later close shifts the timing but not the conclusion."],
    ["RouteSprout EBITDA", "Assumption", "Held at −$1.0M/yr", "42% growth and 21% churn pull in opposite directions. "
     "Breakeven would lower the cross-sell needed to about $1.06M (p.16)."],
    ["Cross-sell ramp", "Assumption", "Linear from 0 to target by end-2028", "Average ARR over the period is half the target."],
    ["Integration-era support", "Evidence + assumption", "$0.85M/yr for 18 months, then ends",
     "Amount from the pack. Duration assumed. Shown as cost to cash or to the $4.0M cap (p.5)."],
    ["Partner economics", "Assumption", "Same ARR range at 80% gross margin. $1.2M minimum is fixed.",
     "Conservative. Crediting the minimum would improve the partnership case."],
    ["Atlas core operations", "Evidence", "About cash-break-even", "No offset from, or drain on, core cash."],
    ["Cost synergies / retention uplift", "Evidence + choice", "None", "The pack says not to assume savings. "
     "The routing-retention link is confounded."],
    ["ARR at risk from churn", "Assumption", "21% × $4.8M ≈ $1.0M/yr", "Logo churn used as a proxy for revenue churn. Not in the base numbers."],
    ["One routing strategy", "Interpretation", "Partnering, then buying RouteSprout, counts as one",
     "If the board disagrees, the 2028 gate becomes a choice between partnership and build only."],
]
table(s, LM, 1.65, CW, 5.25, data, col_w=[2.45, 1.55, 3.3, 4.933], font=10,
      row_h=[0.36] + [0.54] * 9, label="assump")

# =====================================================================
# 20. Appendix: calculation detail
# =====================================================================
s = new_slide("Appendix: every figure in the deck can be traced to pack inputs through simple arithmetic",
              "Appendix · Calculations")
data = [
    ["Metric", "Calculation", "Result"],
    ["Initial cash ceiling", "$24.0M cash − $9.0M floor", "$15.0M"],
    ["Path A / B cash out at close", "18.0 + 4.0  /  11.0 + 3.5", "$22.0M / $14.5M"],
    ["Operating drag, 18 months", "−1.0×1.5 − 0.85×1.5 + (ARR/2)×1.5×0.8 → base ARR 2.4 / low 0.8", "−$1.3M / −$2.3M"],
    ["Path B lowest cash", "24.0 − 14.5 − 1.3 (base)  /  − 2.3 (low)", "$8.2M / $7.2M"],
    ["Valuation multiples", "18.0 ÷ 7.2  /  18.0 ÷ 4.8  /  11.0 ÷ 4.8", "2.5x / 3.75x / 2.3x"],
    ["Acquisition run-rate contribution", "0.8 × ARR − 0.85 − 1.0 (integration era); 0.8 × ARR − 1.0 (after)",
     "+0.07 / −1.21; +0.92 / −0.36"],
    ["Partnership contribution and break-even", "0.8 × 0.55 × ARR − 0.6; break-even 0.6 ÷ 0.44", "+0.46 / −0.25; $1.36M"],
    ["Partner vs acquire crossover", "0.44x − 0.6 = 0.8x − 1.85 → x = 1.25 ÷ 0.36", "$3.47M ARR"],
    ["Build contribution and payback", "1.3 × 0.8 − 0.4; 3.4 ÷ 0.64", "$0.64M/yr; ≈5.3 years"],
    ["Earnout funding period", "7.0 ÷ 0.92 base-case run-rate contribution", "≈7.6 years"],
    ["Upfront ceiling", "15.0 − 4.0 − 2.3", "$8.7M → $8.5M"],
    ["Concentration", "58% × 4.8 ÷ 41  /  42% × 4.8 ÷ 269", "≈$68K / ≈$7.5K per account"],
]
table(s, LM, 1.65, CW, 5.25, data, col_w=[3.1, 6.2, 2.933], font=10,
      row_h=[0.36] + [0.405] * 12, label="calcs")

prs.save(OUT)
print("saved", OUT, "slides:", len(prs.slides))
print("\n".join(fit_warnings) if fit_warnings else "no fit warnings")
