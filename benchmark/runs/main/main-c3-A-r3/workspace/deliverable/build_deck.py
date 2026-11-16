"""Builds Brightwork_Dispatch_Copilot_Launch_Decision.pptx from figures in evidence/briefing-pack.md.
All derived numbers are computed in calc() below so the deck and the appendix stay consistent."""
import sys
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_TICK_LABEL_POSITION
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from PIL import ImageFont

OUT = sys.argv[1] if len(sys.argv) > 1 else "Brightwork_Dispatch_Copilot_Launch_Decision.pptx"

# ---------- palette (dataviz reference palette, light mode) ----------
INK = RGBColor(0x0B, 0x0B, 0x0B)
INK2 = RGBColor(0x52, 0x51, 0x4E)
MUTED = RGBColor(0x89, 0x87, 0x81)
GRID = RGBColor(0xE1, 0xE0, 0xD9)
AXIS = RGBColor(0xC3, 0xC2, 0xB7)
BLUE = RGBColor(0x2A, 0x78, 0xD6)
ORANGE = RGBColor(0xEB, 0x68, 0x34)
GRAYBAR = RGBColor(0xC3, 0xC2, 0xB7)
CRIT = RGBColor(0xD0, 0x3B, 0x3B)
GOODTXT = RGBColor(0x00, 0x63, 0x00)
NAVY = RGBColor(0x10, 0x42, 0x81)
PALE = RGBColor(0xF3, 0xF2, 0xEE)
PALEBLUE = RGBColor(0xE8, 0xF1, 0xFC)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
FONT = "Arial"

# ---------- numbers (all from the briefing pack, derivations explicit) ----------
ACC, SEATS, CORE, COST = 9800, 6.2, 79, 0.009
ARR = ACC * SEATS * CORE * 12                    # $57.6M
COGS = ARR * 0.22                                # 78% GM
PLAT = 0.6e6
ENG = 14 * 0.5 * 210_000                         # $1.47M one-off
CPO_ARR = 0.46 * ACC * 149 * 12                  # $8.1M
ADDON14 = 0.14 * ACC * 149 * 12                  # $2.45M
PERSEAT_COST = 3600 / 8.1 * COST                 # $4.00 / seat / month at beta mean
ALLOW = 600                                      # requests / seat / month (proposed)
CAP_COST = ALLOW * COST                          # $5.40


def pro(a, capped=False, heavy=False):
    n = ACC * a
    s = n * SEATS
    rev = s * 12 * 12
    if heavy:
        inf = n * 6800 * COST * 12
    elif capped:
        inf = s * CAP_COST * 12
    else:
        inf = s * PERSEAT_COST * 12
    gm = (ARR + rev - COGS - inf - PLAT) / (ARR + rev)
    return dict(n=n, rev=rev, inf=inf, contrib=rev - inf - PLAT, gm=gm, nrr=rev / ARR * 100)


def addon(a):
    n = ACC * a
    rev = n * 149 * 12
    inf = n * 6800 * COST * 12
    gm = (ARR + rev - COGS - inf - PLAT) / (ARR + rev)
    return dict(n=n, rev=rev, inf=inf, contrib=rev - inf - PLAT, gm=gm, nrr=rev / ARR * 100)


NEWACC = SEATS * CORE * 12                       # $5,878
RW_DEALS = 2600 * 0.6                            # 1,560
DROP_DEALS = RW_DEALS * 0.07                     # 109
DROP_ARR = DROP_DEALS * NEWACC                   # $0.64M
VPS_DEALS = RW_DEALS * 0.63 / 3                  # 328
VPS_ARR = VPS_DEALS * NEWACC                     # $1.93M
CHURN_ARR = ARR * 0.14                           # $8.1M / yr (logo churn applied to ARR)
MOBILE_CHURN = CHURN_ARR * 0.27                  # $2.18M
AI_CHURN = CHURN_ARR * 0.06                      # $0.48M
MOBILE_FIX_PTS = 0.5 * MOBILE_CHURN / ARR * 100  # +1.9 pts if rewrite halves mobile churn

P14, P23, P33 = pro(0.14), pro(0.23), pro(0.33)
A07, A14 = addon(0.07), addon(0.14)


def m(x, d=1):
    return f"${x/1e6:.{d}f}M"


# ---------- layout helpers ----------
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
L, R = Inches(0.6), Inches(13.333 - 0.6)
CW = R - L
_fonts = {}
WARN = []


def _font(size, bold):
    key = (size, bold)
    if key not in _fonts:
        path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf"
        _fonts[key] = ImageFont.truetype(path, int(size * 10))
    return _fonts[key]


def est_lines(text, size, bold, width_in):
    """Estimate wrapped line count of text at size (pt) in box width (in)."""
    f = _font(size, bold)
    max_px = (width_in - 0.2) * 72 * 10  # inner margins ~0.1in each side
    lines = 0
    for para in text.split("\n"):
        words, cur = para.split(" "), ""
        n = 1
        for w in words:
            t = (cur + " " + w).strip()
            if f.getlength(t) > max_px and cur:
                n += 1
                cur = w
            else:
                cur = t
        lines += n
    return lines


def textbox(slide, x, y, w, h, paras, size=14, color=INK, bold=False, align=PP_ALIGN.LEFT,
            anchor=MSO_ANCHOR.TOP, spacing=1.0, space_after=4, check=True, fill=None, line=None):
    """paras: list of str or list of (runs) where runs = [(text, {bold,color,size})]."""
    if fill is not None:
        shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
        shp.fill.solid(); shp.fill.fore_color.rgb = fill
        if line is None:
            shp.line.fill.background()
        else:
            shp.line.color.rgb = line; shp.line.width = Pt(0.75)
        shp.shadow.inherit = False
        tb = shp
    else:
        tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(0.1)
    tf.margin_top = tf.margin_bottom = Inches(0.05)
    total_h = 0
    for i, p in enumerate(paras):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = align
        para.line_spacing = spacing
        para.space_after = Pt(space_after)
        runs = p if isinstance(p, list) else [(p, {})]
        plain = "".join(r[0] for r in runs)
        psize = max([r[1].get("size", size) for r in runs])
        pbold = all(r[1].get("bold", bold) for r in runs)
        for txt, st in runs:
            r = para.add_run()
            r.text = txt
            r.font.name = FONT
            r.font.size = Pt(st.get("size", size))
            r.font.bold = st.get("bold", bold)
            r.font.color.rgb = st.get("color", color)
        nl = est_lines(plain, psize, pbold, w / 914400)
        total_h += nl * psize * 1.2 * spacing + space_after
    if check and total_h / 72 > (h / 914400) - 0.1 + 0.02:
        WARN.append(f"slide {len(prs.slides)}: text may overflow ({total_h/72:.2f}in > {h/914400:.2f}in): {plain[:60]}")
    return tb


def rect(slide, x, y, w, h, color, line=None):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    s.fill.solid(); s.fill.fore_color.rgb = color
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
    s.shadow.inherit = False
    return s


def hline(slide, x1, y, x2, color=AXIS, width=1.0, dash=False):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x1, y, x2, y)
    c.line.color.rgb = color
    c.line.width = Pt(width)
    if dash:
        from pptx.enum.dml import MSO_LINE
        c.line.dash_style = MSO_LINE.DASH
    return c


def vline(slide, x, y1, y2, color=AXIS, width=1.0, dash=False):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x, y1, x, y2)
    c.line.color.rgb = color
    c.line.width = Pt(width)
    if dash:
        from pptx.enum.dml import MSO_LINE
        c.line.dash_style = MSO_LINE.DASH
    return c


def new_slide(title, kicker=None, source=None, number=True):
    s = prs.slides.add_slide(BLANK)
    if kicker:
        textbox(s, L, Inches(0.35), CW, Inches(0.35), [kicker.upper()], size=11, color=BLUE, bold=True)
    textbox(s, L, Inches(0.62), CW, Inches(1.05), [title], size=24, bold=True, color=INK, spacing=0.95,
            anchor=MSO_ANCHOR.TOP)
    hline(s, L, Inches(1.72), R, color=GRID, width=0.75)
    if source:
        textbox(s, L, Inches(6.88), Inches(10.8), Inches(0.45), [source], size=9, color=MUTED, check=True)
    if number:
        textbox(s, Inches(12.0), Inches(6.95), Inches(0.75), Inches(0.3), [str(len(prs.slides))], size=9,
                color=MUTED, align=PP_ALIGN.RIGHT)
    return s


def bar_chart(slide, x, y, w, h, cats, vals, colors, horizontal=True, fmt='0', maxv=None, minv=None,
              label_size=12, cat_size=12, gap=60, show_val_axis=False):
    cd = CategoryChartData()
    cd.categories = cats
    cd.add_series("s", vals)
    ct = XL_CHART_TYPE.BAR_CLUSTERED if horizontal else XL_CHART_TYPE.COLUMN_CLUSTERED
    gf = slide.shapes.add_chart(ct, x, y, w, h, cd)
    ch = gf.chart
    ch.has_legend = False
    ch.font.name = FONT
    ch.font.size = Pt(cat_size)
    ch.font.color.rgb = INK2
    plot = ch.plots[0]
    plot.gap_width = gap
    plot.vary_by_categories = False
    plot.has_data_labels = True
    dl = plot.data_labels
    dl.number_format = fmt
    dl.number_format_is_linked = False
    dl.position = XL_LABEL_POSITION.OUTSIDE_END
    dl.font.size = Pt(label_size)
    dl.font.bold = True
    dl.font.color.rgb = INK
    ser = plot.series[0]
    for i, c in enumerate(colors):
        pt = ser.points[i]
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = c
        pt.format.line.fill.background()
    va = ch.value_axis
    va.has_major_gridlines = False
    va.visible = show_val_axis
    if maxv is not None:
        va.maximum_scale = maxv
    va.minimum_scale = minv if minv is not None else 0
    va.tick_label_position = XL_TICK_LABEL_POSITION.NONE if not show_val_axis else XL_TICK_LABEL_POSITION.LOW
    ca = ch.category_axis
    ca.format.line.color.rgb = AXIS
    ca.has_major_gridlines = False
    ca.tick_labels.font.size = Pt(cat_size)
    ca.tick_labels.font.color.rgb = INK2
    from pptx.enum.chart import XL_TICK_MARK
    ca.major_tick_mark = XL_TICK_MARK.NONE
    if horizontal:
        ca.reverse_order = True
    return ch


def table(slide, x, y, w, h, rows, col_w, size=12, header_fill=NAVY, first_col_bold=True, row_h=None,
          highlight_col=None):
    nr, nc = len(rows), len(rows[0])
    gt = slide.shapes.add_table(nr, nc, x, y, w, h)
    t = gt.table
    tblPr = gt._element.graphic.graphicData.tbl.tblPr
    # remove default style banding look
    tblPr.set("bandRow", "0"); tblPr.set("firstRow", "0")
    for j, cw in enumerate(col_w):
        t.columns[j].width = Inches(cw)
    for i, row in enumerate(rows):
        if row_h:
            t.rows[i].height = Inches(row_h[i] if isinstance(row_h, list) else row_h)
        for j, val in enumerate(row):
            cell = t.cell(i, j)
            cell.margin_left = cell.margin_right = Inches(0.08)
            cell.margin_top = cell.margin_bottom = Inches(0.04)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            runs = val if isinstance(val, list) else [(str(val), {})]
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            for txt, st in runs:
                r = p.add_run(); r.text = txt
                r.font.name = FONT
                r.font.size = Pt(st.get("size", size))
                hdr = i == 0
                r.font.bold = st.get("bold", hdr or (first_col_bold and j == 0))
                r.font.color.rgb = st.get("color", WHITE if hdr else INK)
            cell.fill.solid()
            if i == 0:
                cell.fill.fore_color.rgb = header_fill
            elif highlight_col is not None and j == highlight_col:
                cell.fill.fore_color.rgb = PALEBLUE
            else:
                cell.fill.fore_color.rgb = WHITE if i % 2 else PALE
    return t


G = [("✓ ", {"color": GOODTXT, "bold": True})]
X = [("✗ ", {"color": CRIT, "bold": True})]

# =====================================================================
# 1. Title
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, prs.slide_width, prs.slide_height, NAVY)
textbox(s, Inches(0.9), Inches(2.0), Inches(11.5), Inches(0.4), ["BRIGHTWORK  |  JANUARY 2027 PLANNING"], size=13,
        color=RGBColor(0x9E, 0xC5, 0xF4), bold=True)
textbox(s, Inches(0.9), Inches(2.5), Inches(11.5), Inches(1.9),
        ["Dispatch Copilot: launch in Q2 2027 inside a new Pro tier, not as a $149 add-on"],
        size=38, bold=True, color=WHITE, spacing=0.95)
textbox(s, Inches(0.9), Inches(4.45), Inches(11.5), Inches(0.9),
        ["Recommendation on the launch decision, packaging and pricing for the CEO and executive team"],
        size=18, color=RGBColor(0xCD, 0xE2, 0xFB))
textbox(s, Inches(0.9), Inches(6.3), Inches(11.5), Inches(0.6),
        ["Based only on the internal briefing pack (synthetic benchmark data). All figures in $ ARR unless stated."],
        size=11, color=RGBColor(0x9E, 0xC5, 0xF4))

# =====================================================================
# 2. Executive summary
s = new_slide("Launch Copilot in Q2 2027 inside a Pro tier at +$12 per seat, with a usage allowance, and "
              "make the mobile rewrite the next commitment", kicker="Executive summary",
              source="Source: Brightwork briefing pack (beta results, paywall test, survey, win/loss and churn data). "
                     "Calculations in appendix A1.")
rows = [
    ("Launch?", [("Yes, in Q2 2027. ", {"bold": True}),
                 (f"Routewise has bundled AI scheduling since Sept 2026, and our win rate against them fell from 44% to 37%. "
                  f"Holding back costs up to ~{m(DROP_ARR + AI_CHURN)} ARR a year in lost deals and AI churn. "
                  "The price is a two-quarter delay to the mobile rewrite, which is a real cost (slide 8).", {})]),
    ("Packaging", [("Include Copilot in a new Pro plan; no standalone add-on. ", {"bold": True}),
                   ("This matches how Routewise sells AI. It also ties price to account size: a 3-seat shop pays $36 a month, "
                    "not $149. And it avoids an add-on that mostly attracts the heaviest users.", {})]),
    ("Price", [("Pro = Core + $12 per seat per month ($91), with 600 AI requests per seat per month pooled; overage $20 per 1,000. ", {"bold": True}),
               ("The allowance keeps company gross margin at or above 75% even if every Pro account uses Copilot heavily.", {})]),
    ("Value", [(f"{m(P14['rev'])}–{m(P33['rev'])} expansion ARR in year one (14–33% of accounts move to Pro). That adds "
                f"+2.1 to +5.0 NRR points. ", {"bold": True}),
               (f"The CPO's $8M is not supported: only 14% of beta accounts bought at $149, against the 46% "
                "who said they would in the survey.", {})]),
    ("NRR 105%", [("Copilot alone is unlikely to get there; Copilot plus the mobile rewrite does, even in the low case. ", {"bold": True}),
                  ("Mobile reliability drives 27% of churn, against 6% for AI. The 14 engineers go back to mobile as soon as Copilot launches.", {})]),
    ("Guardrails", [("Review at end of Q3 2027: ", {"bold": True}),
                    ("≥8% of accounts on Pro, inference cost ≤$5.40 per Pro seat, win rate against Routewise recovering, "
                     "productivity gains holding outside the volunteer accounts, and the mobile rewrite restarted. Renegotiate the inference contract before Dec 2027.", {})]),
]
y = Inches(1.92)
for i, (lab, runs) in enumerate(rows):
    hh = Inches(0.78)
    rect(s, L, y + Inches(0.06), Inches(0.06), hh - Inches(0.16), BLUE)
    textbox(s, L + Inches(0.15), y, Inches(1.75), hh, [lab], size=14, bold=True, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
    textbox(s, L + Inches(1.95), y, CW - Inches(1.95), hh, [runs], size=12.5, anchor=MSO_ANCHOR.MIDDLE, space_after=0)
    y += Inches(0.8)

# =====================================================================
# 3. Competitive pressure
s = new_slide("Competitive pressure is real but smaller than the sales memo implies: at most ~$0.6M a year "
              "of new-customer ARR is at stake, not $1.9M", kicker="Why act now",
              source="Source: briefing pack §7, §10–11. 2,600 qualified opportunities a year × 60% with Routewise = 1,560 deals; "
                     "new account = 6.2 seats × $79 × 12 = $5,878 ARR. The VP Sales figure assumes a third of the 63% of "
                     "Routewise deals we lose are recoverable.")
textbox(s, L, Inches(1.9), Inches(5.6), Inches(0.4), ["Win rate in deals where Routewise competed"], size=13, bold=True, color=INK2)
ch = bar_chart(s, L, Inches(2.25), Inches(5.6), Inches(2.6), ["Q1–Q2 2026", "Q3 2026"], [0.44, 0.37],
               [GRAYBAR, BLUE], horizontal=False, fmt='0%', maxv=0.55, label_size=16, cat_size=13, gap=90)
textbox(s, L, Inches(4.95), Inches(5.6), Inches(1.8), [
    [("−7 points ≈ 109 deals ≈ ", {}), (m(DROP_ARR, 2) + " new ARR a year.", {"bold": True})],
    "This is the most AI could explain. Routewise also offered 20% off the first year in Q3 2026, so some or most of "
    "the drop may be price.",
], size=12.5, color=INK)
xr = L + Inches(6.3)
textbox(s, xr, Inches(1.9), Inches(6.0), Inches(0.4), ["New-customer ARR a year attributed to AI"], size=13, bold=True, color=INK2)
bar_chart(s, xr, Inches(2.25), Inches(6.0), Inches(1.9),
          ["VP Sales memo claim", "Max. explained by win-rate drop"], [VPS_ARR / 1e6, DROP_ARR / 1e6],
          [GRAYBAR, BLUE], fmt='"$"0.0"M"', maxv=2.4, label_size=15, cat_size=12, gap=50)
textbox(s, xr, Inches(4.3), Inches(6.0), Inches(2.4), [
    [("Why the memo overstates: ", {"bold": True}),
     ("31% of loss notes mention AI. That means AI came up, not that it decided the deal, and the memo treats it as recoverable.", {})],
    [("Retention is exposed too: ", {"bold": True}),
     (f"6% of churned accounts left for AI features, ≈ {m(AI_CHURN, 2)} ARR a year, and this will likely grow as Routewise sells its AI.", {})],
    [("Implication: ", {"bold": True}),
     ("launch to stay in contention, but the business case has to rest on expansion revenue from existing customers.", {})],
], size=12.5, space_after=6)

# =====================================================================
# 4. $8M forecast
s = new_slide("The $8M first-year forecast relies on stated intent from a skewed survey. Actual buying in the "
              "paywall test points to $2.5M at most for a $149 add-on", kicker="Testing the CPO proposal",
              source="Source: briefing pack §6, §10. ARR = adopting share × 9,800 accounts × $149 × 12. "
                     "Survey: 610 of 9,800 admins replied (6%), averaging 9.4 seats vs 6.2 for the base. "
                     "Paywall: 17 of 120 beta accounts bought after the free period.")
textbox(s, L, Inches(1.9), Inches(7.0), Inches(0.4), ["Share of accounts buying Copilot at $149/account/month, and implied ARR"],
        size=13, bold=True, color=INK2)
bar_chart(s, L, Inches(2.3), Inches(7.0), Inches(2.4),
          [f"Survey: “likely to buy” → {m(CPO_ARR)} ARR", f"Paywall test: bought → ≤ {m(ADDON14)} ARR"],
          [0.46, 0.14], [GRAYBAR, BLUE], fmt='0%', maxv=0.58, label_size=16, cat_size=13, gap=45)
textbox(s, L, Inches(4.9), Inches(7.0), Inches(1.9), [
    [("Even 14% is likely a ceiling. ", {"bold": True}),
     ("The test ran on beta volunteers, who are larger (8.1 seats) and more active than the base and had already used "
      "the product for 8 weeks. If base adoption is half the test rate, ARR is about " + m(A07['rev']) + ".", {})],
], size=12.5)
xr = L + Inches(7.5)
rect(s, xr, Inches(1.95), Inches(4.65), Inches(4.75), PALE)
textbox(s, xr + Inches(0.15), Inches(2.05), Inches(4.35), Inches(0.4), ["Why the survey overstates demand"], size=14, bold=True, color=NAVY)
textbox(s, xr + Inches(0.15), Inches(2.5), Inches(4.35), Inches(4.1), [
    [("Self-selected: ", {"bold": True}), ("only 6% of admins replied, and they skew to larger accounts (9.4 vs 6.2 seats).", {})],
    [("Intent, not purchase: ", {"bold": True}), ("“likely” or “very likely” counts soft yeses.", {})],
    [("Behaviour beats stated intent: ", {"bold": True}), ("when asked to pay, 86% of beta accounts said no.", {})],
    [("The beta's other results are also from volunteers: ", {"bold": True}),
     ("renewal of 97% vs 93% and +11% productivity show correlation, not proof that Copilot causes them.", {})],
], size=12.5, space_after=9)

# =====================================================================
# 5. Add-on margin / adverse selection
s = new_slide("A flat $149 add-on attracts the heaviest users: paywall buyers cost $61 a month in inference, and "
              "the top tenth cost $131, leaving almost no margin", kicker="Packaging: unit economics",
              source="Source: briefing pack §5–6. Inference cost = requests per month × $0.009 (contract fixed to Dec 2027). "
                     "Gross margin = ($149 − inference) / $149, before the $0.6M a year of platform, evaluation and support cost.")
textbox(s, L, Inches(1.9), Inches(7.4), Inches(0.4), ["Gross margin on a $149 add-on, by account usage (requests per month)"],
        size=13, bold=True, color=INK2)
cats = ["Median beta account (1,900)", "Mean beta account (3,600)", "Paywall buyers (6,800)", "Top 10% of beta (14,500)"]
margins = [(149 - u * COST) / 149 for u in (1900, 3600, 6800, 14500)]
ch = bar_chart(s, L, Inches(2.3), Inches(7.4), Inches(3.5), cats, margins, [GRAYBAR, GRAYBAR, BLUE, BLUE],
               fmt='0%', maxv=1.0, label_size=14, cat_size=12, gap=45)
# 75% reference line: plot area approx; place an annotation instead of precise line
textbox(s, L, Inches(5.85), Inches(7.4), Inches(0.9), [
    [("Company floor is 75% gross margin. ", {"bold": True}),
     ("The accounts most likely to buy sit well below it. Revenue per account is fixed, while cost rises with use.", {})]],
    size=12.5)
xr = L + Inches(7.9)
rect(s, xr, Inches(1.95), Inches(4.15), Inches(4.75), PALE)
textbox(s, xr + Inches(0.15), Inches(2.05), Inches(3.85), Inches(0.4), ["What this means"], size=14, bold=True, color=NAVY)
textbox(s, xr + Inches(0.15), Inches(2.5), Inches(3.85), Inches(4.1), [
    [("Usage is concentrated: ", {"bold": True}), ("the top 10% of beta accounts made 58% of all AI requests.", {})],
    [("Buyers self-select: ", {"bold": True}), ("paywall buyers made 6,800 requests a month, nearly 2× the beta mean and 3.6× the median.", {})],
    [("Flat price, variable cost: ", {"bold": True}), ("one price for 3 seats or 50 seats overcharges small shops and undercharges heavy users.", {})],
    [("Fix: ", {"bold": True}), ("price per seat and cap included usage, so revenue grows with account size and cost has a ceiling.", {})],
], size=12.5, space_after=9)

# =====================================================================
# 6. Pro tier design + margin
s = new_slide("With a 600-request allowance, a per-seat Pro tier keeps gross margin above 75% in every case; "
              "uncapped heavy use would breach it", kicker="Packaging: margin guardrail",
              source="Source: briefing pack §1, §5–6; appendix A1. Company GM = (ARR + Pro uplift − current COGS − inference − $0.6M platform) "
                     "/ (ARR + uplift). Scenario: 33% of accounts on Pro (2023 tier precedent) at 6.2 seats. "
                     "Beta mean = 3,600 requests ÷ 8.1 seats ≈ 444 per seat.")
textbox(s, L, Inches(1.9), Inches(7.0), Inches(0.4), ["Company gross margin, 33% of accounts on Pro"], size=13, bold=True, color=INK2)
gm_rows = [["Scenario", "Inference per Pro seat", "Company GM", "vs 75% floor"],
           ["Today (Core only)", "—", "78.0%", G + [("Above", {})]],
           ["Pro, beta-mean usage (444 requests per seat)", "$4.00", f"{P33['gm']*100:.1f}%", G + [("Above", {})]],
           ["Pro, every seat uses the full allowance (600)", "$5.40", f"{pro(0.33, capped=True)['gm']*100:.1f}%", G + [("Above", {})]],
           ["Pro, uncapped, every account at paywall-buyer usage (6,800 per account)", "$9.87", f"{pro(0.33, heavy=True)['gm']*100:.1f}%", X + [("Breach", {"bold": True, "color": CRIT})]]]
table(s, L, Inches(2.3), Inches(7.0), Inches(3.2), gm_rows, [3.5, 1.3, 1.1, 1.1], size=12, row_h=[0.45, 0.6, 0.7, 0.7, 0.75])
textbox(s, L, Inches(5.7), Inches(7.0), Inches(1.1), [
    [("Floor: 75%. ", {"bold": True}),
     ("The allowance limits the worst case to $5.40 of inference per $12 seat uplift (55% margin on the uplift). "
      "Without it, heavy users push the company to 74.1%.", {})]], size=12.5)
xr = L + Inches(7.5)
rect(s, xr, Inches(1.95), Inches(4.65), Inches(4.75), PALEBLUE)
textbox(s, xr + Inches(0.15), Inches(2.05), Inches(4.35), Inches(0.4), ["Proposed Pro plan"], size=14, bold=True, color=NAVY)
textbox(s, xr + Inches(0.15), Inches(2.5), Inches(4.35), Inches(4.1), [
    [("Price: ", {"bold": True}), ("$91 per seat per month (Core $79 + $12).", {})],
    [("Includes: ", {"bold": True}), ("Dispatch Copilot (schedule proposals, quote drafts, call summaries).", {})],
    [("Allowance: ", {"bold": True}), ("600 requests per seat per month, pooled across the account. A 6.2-seat account gets 3,720; "
                                          "the median beta account used 1,900.", {})],
    [("Overage: ", {"bold": True}), ("$20 per 1,000 extra requests (55% margin at $0.009).", {})],
    [("Unit cost at beta-mean usage: ", {"bold": True}), ("$4.00 per seat per month, 67% margin on the uplift.", {})],
    [("Core: ", {"bold": True}), ("unchanged at $79; no Copilot.", {})],
], size=12, space_after=7)

# =====================================================================
# 7. Options compared
s = new_slide("The Pro tier has the most upside, the best fit against Routewise and a capped margin risk; "
              "the $149 add-on earns no more", kicker="Options compared",
              source="Source: briefing pack; appendix A1. Year-one run-rate ARR; contribution = ARR − inference − $0.6M platform, "
                     "before the $1.47M one-off engineering cost. Add-on range: half to all of the 14% paywall rate. "
                     "Pro range: 14% (paywall rate) to 33% (2023 tier precedent).")
G = [("✓ ", {"color": GOODTXT, "bold": True})]
X = [("✗ ", {"color": CRIT, "bold": True})]
rows = [
    ["", "A. Hold: mobile first, no Copilot", "B. $149 add-on (CPO proposal)", "C. Pro tier, +$12/seat, with allowance (recommended)"],
    ["Expansion ARR, year one", "$0", f"{m(A07['rev'])}–{m(A14['rev'])} (not $8.1M)", f"{m(P14['rev'])}–{m(P33['rev'])}"],
    ["NRR uplift", "0 pts (mobile helps later)", f"+{A07['nrr']:.1f} to +{A14['nrr']:.1f} pts", f"+{P14['nrr']:.1f} to +{P33['nrr']:.1f} pts"],
    ["Contribution after inference and platform", "$0", f"{m(A07['contrib'])}–{m(A14['contrib'])}", f"{m(P14['contrib'])}–{m(P33['contrib'])}"],
    ["Gross-margin risk", G + [("None", {})], X + [("Unbounded: heavy users buy; top 10% leave 12% margin", {})],
     G + [("Bounded: ≥55% on uplift at the allowance", {})]],
    ["Fit against Routewise (AI in Pro)", X + [("Keeps losing AI-led deals and AI churn", {})],
     X + [("AI costs extra; we look pricier", {})], G + [("Like-for-like packaging", {})]],
    ["Fit for small shops (3–50 techs)", "n/a", X + [("$149 is 63% on top of a 3-seat bill", {})],
     G + [("Scales: 3 seats pay $36 a month", {})]],
    ["Mobile rewrite", G + [("On time", {})], X + [("Delayed 2 quarters", {})], X + [("Delayed 2 quarters", {})]],
]
table(s, L, Inches(1.95), CW, Inches(4.7), rows, [2.75, 2.9, 3.3, 3.183], size=12,
      row_h=[0.5] + [0.6] * 7, highlight_col=3)

# =====================================================================
# 8. Mobile trade-off
s = new_slide("The real cost of launching is a two-quarter delay to the mobile rewrite, and mobile reliability is "
              "customers' biggest complaint", kicker="The trade-off",
              source="Source: briefing pack §3, §8 (n = 1,190 churned accounts in 2026; 2026 customer survey). Churned ARR ≈ 14% × $57.6M = $8.1M a year. "
                     "Delay costs are illustrative: the briefing pack does not say how much churn the rewrite would remove; we assume half.")
textbox(s, L, Inches(1.9), Inches(6.4), Inches(0.4), ["Main reason for churn, 2026 (share of churned accounts)"], size=13, bold=True, color=INK2)
cats = ["Mobile app reliability", "Price", "Missing integrations", "Out of business / sold", "Switched for AI features", "Other"]
vals = [0.27, 0.22, 0.15, 0.14, 0.06, 0.16]
bar_chart(s, L, Inches(2.3), Inches(6.4), Inches(3.4), cats, vals, [BLUE, GRAYBAR, GRAYBAR, GRAYBAR, ORANGE, GRAYBAR],
          fmt='0%', maxv=0.33, label_size=13, cat_size=12, gap=40)
textbox(s, L, Inches(5.8), Inches(6.4), Inches(1.0), [
    [("Top feature request: ", {"bold": True}), ("a reliable technician app is ranked first by 38% of customers, against 19% for AI scheduling.", {})]],
    size=12.5)
xr = L + Inches(6.9)
textbox(s, xr, Inches(1.9), Inches(5.2), Inches(0.4), ["What a two-quarter delay costs either way"], size=13, bold=True, color=INK2)
rows = [
    ["", "ARR at risk"],
    [[("Delay mobile", {"bold": True}), (" (launch Copilot)", {"bold": False})],
     [("≈ $0.5M lost for good ", {"bold": True}), ("if the rewrite halves mobile churn ($1.1M if it ends it)", {})]],
    [[("Delay Copilot", {"bold": True}), (" (mobile first)", {"bold": False})],
     [("Up to ≈ $0.6M lost for good ", {"bold": True}), ("(new deals $0.3M + AI churn $0.25M), and $1.2–2.9M of Pro expansion pushed back", {})]],
]
table(s, xr, Inches(2.3), Inches(5.2), Inches(2.3), rows, [1.7, 3.5], size=12, row_h=[0.4, 0.95, 0.95])
textbox(s, xr, Inches(4.75), Inches(5.2), Inches(2.0), [
    [("A close call on the numbers. ", {"bold": True}),
     ("We favour launching because Routewise is already selling AI and expansion is the only lever with a fast NRR effect. ", {}),
     ("The condition: ", {"bold": True}),
     ("the mobile rewrite restarts as soon as Copilot launches and is not delayed again.", {})]],
    size=12.5)

# =====================================================================
# 9. NRR bridge
s = new_slide("Reaching 105% NRR by 2028 needs both levers: in the low case, the Pro tier and the mobile rewrite "
              "together only just get there", kicker="Objective check",
              source="Source: briefing pack §1, §3, §6, §8; appendix A1. Simplified NRR effect = expansion ARR or retained ARR ÷ $57.6M base. "
                     "Mobile effect assumes the rewrite halves mobile-driven churn (illustrative). AI-churn defence (up to +0.8 pts) is not counted.")
textbox(s, L, Inches(1.9), Inches(7.6), Inches(0.4), ["Net revenue retention bridge, low case (%)"], size=13, bold=True, color=INK2)
# waterfall via stacked columns
cd = CategoryChartData()
cats = ["Today", "Pro tier (14% adopt)", "Mobile rewrite", "Both levers"]
base = [0, 101.0, 101.0 + P14["nrr"], 0]
inc = [101.0, P14["nrr"], MOBILE_FIX_PTS, 101.0 + P14["nrr"] + MOBILE_FIX_PTS]
cd.categories = cats
cd.add_series("base", [b - 98 if b else 0 for b in base])
cd.add_series("value", [v - 98 if i in (0, 3) else v for i, v in enumerate(inc)])
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_STACKED, L, Inches(2.3), Inches(7.6), Inches(3.6), cd)
ch = gf.chart
ch.has_legend = False
ch.font.name = FONT; ch.font.size = Pt(12); ch.font.color.rgb = INK2
plot = ch.plots[0]; plot.gap_width = 55; plot.overlap = 100
sb, sv = plot.series
sb.format.fill.background(); sb.format.line.fill.background()
colors = [GRAYBAR, BLUE, BLUE, NAVY]
for i, c in enumerate(colors):
    p = sv.points[i]; p.format.fill.solid(); p.format.fill.fore_color.rgb = c; p.format.line.fill.background()
va = ch.value_axis; va.visible = False; va.has_major_gridlines = False; va.minimum_scale = 0; va.maximum_scale = 8.5
ca = ch.category_axis; ca.format.line.color.rgb = AXIS; ca.tick_labels.font.size = Pt(12)
from pptx.enum.chart import XL_TICK_MARK
ca.major_tick_mark = XL_TICK_MARK.NONE
labels = ["101.0%", f"+{P14['nrr']:.1f}", f"+{MOBILE_FIX_PTS:.1f}", f"{101 + P14['nrr'] + MOBILE_FIX_PTS:.1f}%"]
for i, lab in enumerate(labels):
    dlab = sv.points[i].data_label
    dlab.position = XL_LABEL_POSITION.INSIDE_END
    tf = dlab.text_frame
    tf.text = lab
    r = tf.paragraphs[0].runs[0]
    r.font.size = Pt(14); r.font.bold = True; r.font.name = FONT
    r.font.color.rgb = INK if i == 0 else WHITE
textbox(s, L, Inches(5.95), Inches(7.6), Inches(0.8), ["Axis starts at 98% to show the increments; the bars are not to zero."],
        size=10, color=MUTED)
xr = L + Inches(8.0)
rect(s, xr, Inches(1.95), Inches(4.15), Inches(4.75), PALE)
textbox(s, xr + Inches(0.15), Inches(2.05), Inches(3.85), Inches(0.4), ["Each lever on its own"], size=14, bold=True, color=NAVY)
rows = [["Path", "NRR"],
        ["Pro tier only, low (14%)", f"{101 + P14['nrr']:.1f}%"],
        ["Pro tier only, mid (23%)", f"{101 + P23['nrr']:.1f}%"],
        ["Pro tier only, high (33%)", f"{101 + P33['nrr']:.1f}%"],
        ["Mobile rewrite only", f"{101 + MOBILE_FIX_PTS:.1f}%"],
        [[("Pro (low) + mobile", {"bold": True})], [(f"{101 + P14['nrr'] + MOBILE_FIX_PTS:.1f}%", {"bold": True})]]]
table(s, xr + Inches(0.15), Inches(2.5), Inches(3.85), Inches(2.6), rows, [2.75, 1.1], size=12, row_h=0.42)
textbox(s, xr + Inches(0.15), Inches(5.2), Inches(3.85), Inches(1.45), [
    "Only the high adoption case reaches 105% without the mobile fix. That is why the mobile rewrite must not slip a second time."],
    size=12)

# =====================================================================
# 10. Economics of recommendation
s = new_slide("The Pro tier pays back the $1.47M build in about two years in the mid case. The low case is thin, "
              "so the Q3 review decides whether to keep investing", kicker="Economics of the recommendation",
              source="Source: briefing pack; appendix A1. Assumes adopters average 6.2 seats (conservative: beta and survey accounts "
                     "were larger) and use 444 requests per seat (beta mean). Excludes new-customer and churn-defence upside. "
                     "Payback = $1.47M ÷ annual contribution.")
hdr = ["Year-one run-rate", "Low: 14% on Pro", "Mid: 23% on Pro", "High: 33% on Pro"]
def row(lab, f, bold=False):
    return [[(lab, {"bold": True})]] + [[(f(p), {"bold": bold})] for p in (P14, P23, P33)]
rows = [hdr,
        row("Accounts on Pro", lambda p: f"{p['n']:,.0f}"),
        row("Expansion ARR (+$12 × 6.2 seats × 12)", lambda p: m(p['rev'], 2)),
        row("Inference cost ($4.00 per seat per month)", lambda p: "−" + m(p['inf'], 2)),
        row("Platform, evaluation, support", lambda p: "−$0.60M"),
        row("Contribution", lambda p: m(p['contrib'], 2), bold=True),
        row("Payback on $1.47M engineering", lambda p: f"{ENG / p['contrib']:.1f} years", bold=True),
        row("NRR uplift", lambda p: f"+{p['nrr']:.1f} pts"),
        row("Company gross margin", lambda p: f"{p['gm']*100:.1f}%")]
table(s, L, Inches(1.95), Inches(8.2), Inches(4.5), rows, [3.4, 1.6, 1.6, 1.6], size=12.5, row_h=0.5, highlight_col=2)
xr = L + Inches(8.6)
rect(s, xr, Inches(1.95), Inches(3.55), Inches(4.75), PALE)
textbox(s, xr + Inches(0.15), Inches(2.05), Inches(3.3), Inches(0.4), ["Upside not counted"], size=14, bold=True, color=NAVY)
textbox(s, xr + Inches(0.15), Inches(2.5), Inches(3.3), Inches(4.1), [
    [("New customers: ", {"bold": True}), (f"up to {m(DROP_ARR, 2)} a year if AI caused the win-rate drop. Pro deals are worth $6,770 vs $5,878 on Core.", {})],
    [("AI churn: ", {"bold": True}), (f"up to {m(AI_CHURN, 2)} a year defended.", {})],
    [("Inference prices: ", {"bold": True}), ("list prices fell 35% in 12 months, and our contract is fixed only until Dec 2027.", {})],
    [("Overage revenue ", {"bold": True}), ("from accounts above the allowance.", {})],
], size=12, space_after=8)

# =====================================================================
# 11. Launch plan
s = new_slide("Launch plan: build in Q1–Q2, launch Pro in Q2, review at end of Q3, and return the 14 engineers "
              "to mobile right after launch", kicker="How we would run it",
              source="Note: the timing of the build and the mobile restart assumes the two quarters of Copilot work are Q1–Q2 2027. "
                     "Beta accounts move to Pro or Core when the free period ends.")
phases = [
    ("Q1 2027", "Build and harden", ["14 engineers on Copilot", "Meter usage and enforce allowances", "Pro plan in billing; sales enablement",
                                     "Measure productivity in non-volunteer pilot accounts"]),
    ("Q2 2027", "Launch Pro", ["Pro at $91/seat with 600 requests per seat", "Lead with Pro in every deal against Routewise",
                               "Offer Pro to the 240 beta accounts", "Mobile rewrite plan locked for Q3 restart"]),
    ("Q3 2027", "Review gate", ["14 engineers return to the mobile rewrite", "Check the five go/adjust criteria (next slide)",
                                "Reprice or rescope if adoption is below the bar"]),
    ("Q4 2027", "Renegotiate", ["Renegotiate inference before the Dec 2027 contract end",
                                         "Revisit the allowance and price with real usage data", "Mobile rewrite continues"]),
]
x = L; w = (CW - Inches(0.45)) / 4
for i, (q, name, items) in enumerate(phases):
    xi = L + i * (w + Inches(0.15))
    rect(s, xi, Inches(2.0), w, Inches(0.5), NAVY if i != 2 else BLUE)
    textbox(s, xi, Inches(2.0), w, Inches(0.5), [[(q + "  ", {"bold": True}), (name, {})]], size=14, color=WHITE,
            anchor=MSO_ANCHOR.MIDDLE)
    rect(s, xi, Inches(2.5), w, Inches(3.0), PALE)
    textbox(s, xi + Inches(0.05), Inches(2.6), w - Inches(0.1), Inches(2.85), ["• " + t for t in items], size=12.5, space_after=8)
rect(s, L, Inches(5.7), CW, Inches(1.0), PALEBLUE)
textbox(s, L + Inches(0.15), Inches(5.72), CW - Inches(0.3), Inches(0.95), [
    [("Packaging rules: ", {"bold": True}),
     ("one price per seat across the whole account (no mixing Pro and Core seats); Copilot is not sold on Core; "
      "allowance pooled per account with in-product usage alerts at 80%; overage $20 per 1,000 requests, billed monthly.", {})]],
    size=12.5, anchor=MSO_ANCHOR.MIDDLE)

# =====================================================================
# 12. Gates and uncertainties
s = new_slide("Five checks at the end of Q3 2027 test the biggest unknowns. Missing them triggers a "
              "reprice or rescope, not more investment", kicker="Guardrails",
              source="Source: briefing pack §5–7, §11. Thresholds are proposals: 8% within two quarters is on pace for the 14% low case; "
                     "41% is half the lost win rate recovered; $5.40 is the allowance cost.")
rows = [
    ["Unknown in the briefing pack", "What we measure", "Bar at end of Q3 2027", "If missed"],
    ["Will non-volunteers adopt and pay?", "Share of accounts on Pro", "≥ 8% of accounts", "Test lower uplift ($8–10) or a trial-to-Pro path"],
    ["Does productivity hold beyond volunteers?", "Jobs per dispatcher-hour, Pro accounts vs matched Core", "≥ +5% (beta: +11% vs +2%)",
     "Rescope to the highest-value feature (scheduling)"],
    ["Is AI the cause of lost deals, or Routewise's discount?", "Win rate where Routewise competes, after its Q3 2026 promotion",
     "≥ 41% (half of the 7-pt drop recovered)", "Revisit the pricing response, not the AI roadmap"],
    ["How heavy is real usage, and how fast do costs fall?", "Inference cost per Pro seat; provider quotes for 2028",
     "≤ $5.40 per seat per month", "Lower the allowance or raise overage before renewal"],
    ["Does mobile stay on track?", "Mobile rewrite restart date; mobile-driven churn", "Restarted in Q3 2027", "Escalate to CEO; no further Copilot scope"],
]
table(s, L, Inches(1.95), CW, Inches(4.7), rows, [3.3, 3.3, 2.6, 2.933], size=12, row_h=[0.45] + [0.85] * 5)

# =====================================================================
# 13. Decisions
s = new_slide("Decisions requested from the executive team today", kicker="Next steps",
              source="Choices made in preparing this deck without input from the team are listed in appendix A3.")
decs = [
    ("1", "Approve the Q2 2027 launch of Dispatch Copilot", "14 engineers for Q1–Q2 2027, $1.47M fully loaded; mobile rewrite delayed two quarters."),
    ("2", "Approve Pro packaging instead of the $149 add-on", "Pro = $91 per seat per month with Copilot included; Core unchanged at $79; no standalone add-on."),
    ("3", "Approve the usage allowance and overage", "600 requests per seat per month pooled; $20 per 1,000 above that; keeps gross margin ≥ 75%."),
    ("4", "Commit the mobile rewrite as the next priority", "Engineers return in Q3 2027, owned by CPO with Customer Success. No second delay."),
    ("5", "Adopt the Q3 2027 review and its five checks", "CFO to own; also mandate renegotiating the inference contract before Dec 2027."),
    ("6", "Reset the first-year Copilot target", f"Plan on {m(P14['rev'])}–{m(P33['rev'])} expansion ARR (mid {m(P23['rev'])}), not $8M."),
]
y = Inches(1.95)
for n, head, body in decs:
    circ = s.shapes.add_shape(MSO_SHAPE.OVAL, L, y + Inches(0.08), Inches(0.5), Inches(0.5))
    circ.fill.solid(); circ.fill.fore_color.rgb = BLUE; circ.line.fill.background(); circ.shadow.inherit = False
    circ.text_frame.text = n
    p = circ.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    p.runs[0].font.size = Pt(16); p.runs[0].font.bold = True; p.runs[0].font.color.rgb = WHITE; p.runs[0].font.name = FONT
    textbox(s, L + Inches(0.7), y, Inches(5.0), Inches(0.66), [head], size=14, bold=True, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
    textbox(s, L + Inches(5.8), y, CW - Inches(5.8), Inches(0.66), [body], size=12.5, anchor=MSO_ANCHOR.MIDDLE)
    hline(s, L, y + Inches(0.74), R, color=GRID, width=0.5)
    y += Inches(0.8)

# =====================================================================
# Appendix divider-lite: A1 calculations
s = new_slide("A1. Calculations and assumptions behind the figures in this deck", kicker="Appendix",
              source="Source: Brightwork briefing pack (synthetic benchmark data). Rounded figures; computed in deliverable/build_deck.py.")
rows = [
    ["Figure", "Calculation", "Result"],
    ["Current ARR", "9,800 accounts × 6.2 seats × $79 × 12", m(ARR)],
    ["CPO forecast", "46% × 9,800 × $149 × 12", m(CPO_ARR)],
    ["Add-on at paywall rate", "14% × 9,800 × $149 × 12 (half rate: 7%)", f"{m(ADDON14, 2)} ({m(A07['rev'], 2)})"],
    ["Add-on inference per buyer", "6,800 requests × $0.009 × 12", "$734 a year"],
    ["Pro expansion ARR", "share × 9,800 × 6.2 seats × $12 × 12 (14% / 23% / 33%)", f"{m(P14['rev'],2)} / {m(P23['rev'],2)} / {m(P33['rev'],2)}"],
    ["Pro inference per seat", "3,600 requests ÷ 8.1 seats × $0.009; allowance 600 × $0.009", "$4.00; cap $5.40"],
    ["Engineering cost", "14 engineers × 0.5 year × $210,000", m(ENG, 2)],
    ["Win-rate drop in ARR", "1,560 Routewise deals × 7 pts × $5,878", m(DROP_ARR, 2)],
    ["VP Sales claim", "1,560 × 63% lost × ⅓ × $5,878", m(VPS_ARR, 2)],
    ["Churn by reason", "14% × $57.6M = $8.1M; × 27% mobile / 6% AI", f"{m(MOBILE_CHURN, 2)} / {m(AI_CHURN, 2)}"],
    ["Mobile fix NRR effect", "50% of mobile churn retained ÷ $57.6M (illustrative)", f"+{MOBILE_FIX_PTS:.1f} pts"],
    ["Company gross margin", "(ARR + uplift − 22% × ARR − inference − $0.6M) ÷ (ARR + uplift)", "see slides 6, 10"],
]
table(s, L, Inches(1.9), CW, Inches(4.85), rows, [2.8, 6.833, 2.5], size=11.5, row_h=[0.38] + [0.37] * 12)

# A2 evidence quality
s = new_slide("A2. How much weight each piece of evidence can bear", kicker="Appendix",
              source="Source: briefing pack §5–8, §10–11.")
rows = [
    ["Evidence", "What it shows", "Limitation", "How we used it"],
    ["Survey: 46% likely to buy", "Stated interest at $149", "6% response; larger accounts; intent only", "Not used for sizing"],
    ["Paywall test: 14% bought", "Real purchase at $149", "Beta volunteers; 120 accounts; 4 weeks", "Ceiling for the add-on; low case for Pro"],
    ["2023 tier launch: 33% moved", "Base appetite for an upper tier", "Different tier, different year", "High case for Pro"],
    ["Beta productivity +11% vs +2%", "Copilot may raise throughput", "Volunteers; partly self-reported", "Checked at the Q3 review"],
    ["Beta renewal 97% vs 93%", "Correlation with retention", "Selection bias; 90 days only", "Not counted in the value case"],
    ["Win rate 44% → 37%", "Competitive pressure", "Coincides with Routewise's 20% discount", "Upper bound only ($0.64M)"],
    ["31% of loss notes mention AI", "AI comes up in lost deals", "Mention, not the deciding reason", "Not used for sizing"],
    ["Churn reasons (n = 1,190)", "Mobile 27%, AI 6%", "Main reason only; self-reported", "Mobile priority; AI churn upside"],
]
table(s, L, Inches(1.9), CW, Inches(4.85), rows, [3.0, 2.9, 3.3, 2.933], size=11.5, row_h=[0.4] + [0.55] * 8)

# A3 choices made
s = new_slide("A3. Choices made without input from the team, so they can be challenged", kicker="Appendix",
              source="These are analyst choices, not findings from the briefing pack. Each can be changed without altering the core recommendation, "
                     "except the mobile efficacy assumption, which affects how close the sequencing call is.")
items = [
    ("Pro price kept at +$12 per seat", "This is the option in the briefing pack. It costs a 6.2-seat account $74 a month, about half of $149."),
    ("Allowance of 600 requests per seat; overage $20 per 1,000", "Set above beta-mean usage (444 per seat) to cap the worst case at $5.40 per seat. Revisit with launch data."),
    ("Adoption range 14%–33%; mid 23%", "Bounded by the paywall rate and the 2023 tier precedent. The mid case is a simple midpoint, not a forecast."),
    ("Adopters average 6.2 seats", "Conservative: beta and survey accounts were larger, which would raise ARR per adopter."),
    ("$0.6M platform cost treated as cost of revenue", "Conservative for the gross-margin test. Engineering build cost is treated as a one-off."),
    ("Mobile rewrite halves mobile-driven churn", "Illustrative only; the briefing pack gives no efficacy estimate. At 100%, the case for mobile first gets stronger."),
    ("Build runs Q1–Q2 2027; engineers return in Q3", "Inferred from a Q2 launch and the 'two quarters' of work in the briefing pack."),
    ("Simplified NRR arithmetic", "Expansion or retained ARR ÷ starting ARR; ignores timing within the year and interactions between levers."),
]
y = Inches(1.95)
for head, body in items:
    textbox(s, L, y, Inches(4.6), Inches(0.58), [head], size=12.5, bold=True, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
    textbox(s, L + Inches(4.7), y, CW - Inches(4.7), Inches(0.58), [body], size=12, anchor=MSO_ANCHOR.MIDDLE)
    hline(s, L, y + Inches(0.6), R, color=GRID, width=0.5)
    y += Inches(0.6)

prs.save(OUT)
for w_ in WARN:
    print("WARN", w_)
print("saved", OUT, len(prs.slides), "slides")
