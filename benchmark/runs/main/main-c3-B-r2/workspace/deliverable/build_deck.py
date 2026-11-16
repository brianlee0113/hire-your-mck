"""Builds the Dispatch Copilot recommendation deck from the briefing pack figures.

All numbers are computed in calc() from evidence/briefing-pack.md inputs so every figure
shown on a slide is traceable. Run: python3 build_deck.py  -> Dispatch_Copilot_Recommendation.pptx
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_TICK_LABEL_POSITION, XL_TICK_MARK
from pptx.oxml.ns import qn
import os, json
from lxml import etree

# ----------------------------------------------------------------------------- palette
INK = RGBColor(0x0B, 0x0B, 0x0B)
INK2 = RGBColor(0x52, 0x51, 0x4E)
MUTED = RGBColor(0x8A, 0x89, 0x84)
NAVY = RGBColor(0x10, 0x42, 0x81)
BLUE = RGBColor(0x2A, 0x78, 0xD6)
LIGHTBLUE = RGBColor(0xCD, 0xE2, 0xFB)
GREY = RGBColor(0xB4, 0xB3, 0xAE)
LIGHTGREY = RGBColor(0xEF, 0xEE, 0xEA)
RULE = RGBColor(0xD9, 0xD8, 0xD3)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
RED = RGBColor(0xC6, 0x2F, 0x2E)
AMBER = RGBColor(0xB9, 0x7A, 0x00)
GREEN = RGBColor(0x00, 0x7A, 0x00)
ORANGE = RGBColor(0xEB, 0x68, 0x34)
FONT = "Arial"

# ----------------------------------------------------------------------------- numbers
def calc():
    c = {}
    acc, seats, core = 9800, 6.2, 79
    c["arr"] = acc * seats * core * 12
    cogs = c["arr"] * 0.22
    acct_arr = seats * core * 12
    c["acct_arr"] = acct_arr
    c["cpo"] = 0.46 * acc * 149 * 12
    plat = 0.6e6
    def addon(p):
        n = acc * p; rev = n * 149 * 12; inf = n * 6800 * 0.009 * 12
        return dict(n=n, rev=rev, inf=inf, gp=rev - inf - plat, fgm=(rev - inf - plat) / rev,
                    cogm=1 - (cogs + inf + plat) / (c["arr"] + rev), nrr=rev / c["arr"] * 100)
    def pro(p, inf_seat):
        n = acc * p; rev = n * seats * 12 * 12; inf = n * seats * inf_seat * 12
        return dict(n=n, rev=rev, inf=inf, gp=rev - inf - plat, fgm=(rev - inf - plat) / rev,
                    cogm=1 - (cogs + inf + plat) / (c["arr"] + rev), nrr=rev / c["arr"] * 100)
    c["add14"], c["add7"] = addon(0.14), addon(0.07)
    c["seat_inf"] = 3600 / 8.1 * 0.009            # $4.00 per seat per month
    c["pro33"], c["pro14"] = pro(0.33, c["seat_inf"]), pro(0.14, c["seat_inf"])
    c["pro_heavy"] = pro(0.33, 6800 * 0.009 / seats)  # every upgrader uses like paywall buyers, no cap
    c["pro_cap"] = pro(0.33, 600 * 0.009)            # every seat at the 600-request allowance
    inf_free = acc * seats * c["seat_inf"] * 12
    c["free_cost"] = inf_free + plat
    c["free_cogm"] = 1 - (cogs + inf_free + plat) / c["arr"]
    opp = 2600 * 0.6
    c["opp"] = opp
    c["lost_wins"] = opp * 0.07
    c["comp_arr"] = c["lost_wins"] * acct_arr
    lost = opp * 0.63
    c["vp_deals"] = lost / 3
    c["vp_rate"] = (opp * 0.37 + lost / 3) / opp
    churn = acc * 0.14
    c["churn_accts"] = churn
    c["churn_arr"] = churn * acct_arr
    c["mob_arr"] = churn * 0.27 * acct_arr
    c["ai_arr"] = churn * 0.06 * acct_arr
    c["mob_half_100"] = c["mob_arr"] * 0.5
    c["mob_half_50"] = c["mob_arr"] * 0.25
    c["cop_half_ceiling"] = (c["comp_arr"] + c["ai_arr"]) * 0.5
    c["cop_half_half"] = (c["comp_arr"] + c["ai_arr"]) * 0.25
    c["be_ceiling"] = c["cop_half_ceiling"] / c["mob_half_100"]
    c["be_half"] = c["cop_half_half"] / c["mob_half_100"]
    c["eng"] = 14 * 210000 * 0.5
    c["nrr_mob50"] = c["mob_arr"] * 0.5 / c["arr"] * 100
    c["pro_alone_share"] = 0.04 * c["arr"] / (seats * 144) / acc
    c["pro_with_mob_share"] = (0.04 * c["arr"] - c["mob_arr"] * 0.5) / (seats * 144) / acc
    c["defer_gp"] = 0.5 * c["pro33"]["gp"]
    c["defer_gp_low"] = 0.5 * c["pro14"]["gp"]
    return c

C = calc()
def m(x, d=1):
    return f"${x/1e6:.{d}f}M"

# ----------------------------------------------------------------------------- deck helpers
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
TEXTBOXES = []  # for the fit checker
SECTIONS = ["1  Is it worth launching?", "2  Packaging and price", "3  Timing", "4  Risks and next steps"]


def tb(slide, x, y, w, h, paras, size=12, color=INK, bold=False, align=PP_ALIGN.LEFT,
       anchor=MSO_ANCHOR.TOP, fill=None, line=None, margin=0.05, spacing=1.0, check=True):
    """paras: str | list of (str | list of runs | dict). A run is (text, {bold,color,size,italic})."""
    shp = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)) if fill is None and line is None \
        else slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is not None or line is not None:
        shp.shadow.inherit = False
        if fill is None:
            shp.fill.background()
        else:
            shp.fill.solid(); shp.fill.fore_color.rgb = fill
        if line is None:
            shp.line.fill.background()
        else:
            shp.line.color.rgb = line; shp.line.width = Pt(0.75)
    tf = shp.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    tf.vertical_anchor = anchor
    for side in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, side, Inches(margin))
    if isinstance(paras, str):
        paras = [paras]
    rec = []
    for i, p in enumerate(paras):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = align
        para.line_spacing = spacing
        opts = {}
        if isinstance(p, dict):
            opts = p; p = p["runs"]
        if isinstance(p, str):
            p = [(p, {})]
        bullet = opts.get("bullet", False)
        if opts.get("space_before") is not None:
            para.space_before = Pt(opts["space_before"])
        if bullet:
            pPr = para._p.get_or_add_pPr()
            lvl = opts.get("level", 0)
            ind = 0.18 + 0.2 * lvl
            pPr.set("marL", str(int(Inches(ind)))); pPr.set("indent", str(int(-Inches(0.16))))
            bu = etree.SubElement(pPr, qn("a:buChar")); bu.set("char", "•" if lvl == 0 else "–")
        text_all = ""
        for run_text, ro in p:
            r = para.add_run(); r.text = run_text
            f = r.font; f.name = FONT
            f.size = Pt(ro.get("size", opts.get("size", size)))
            f.bold = ro.get("bold", opts.get("bold", bold))
            f.italic = ro.get("italic", False)
            f.color.rgb = ro.get("color", opts.get("color", color))
            text_all += run_text
        rec.append((text_all, opts.get("size", size), bool(opts.get("bold", bold)), bullet,
                    opts.get("level", 0), opts.get("space_before") or 0))
    if check:
        TEXTBOXES.append(dict(slide=len(prs.slides), x=x, w=w, h=h, margin=margin, paras=rec, spacing=spacing))
    return shp


def rect(slide, x, y, w, h, fill, line=None, shape=MSO_SHAPE.RECTANGLE):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    s.shadow.inherit = False
    s.fill.solid(); s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line; s.line.width = Pt(0.75)
    return s


def hline(slide, x, y, w, color=RULE, weight=1.0, dash=False):
    ln = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x), Inches(y), Inches(x + w), Inches(y))
    ln.line.color.rgb = color; ln.line.width = Pt(weight)
    if dash:
        ln.line.dash_style = 4
    return ln


def vline(slide, x, y, h, color=RULE, weight=1.0, dash=False):
    ln = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x), Inches(y), Inches(x), Inches(y + h))
    ln.line.color.rgb = color; ln.line.width = Pt(weight)
    if dash:
        ln.line.dash_style = 4
    return ln


def new_slide(title, section=None, source=None):
    s = prs.slides.add_slide(BLANK)
    if section is not None:
        # section tracker
        x = 0.5
        for i, name in enumerate(SECTIONS):
            active = (i == section)
            tb(s, x, 0.18, 3.0, 0.28, [[(name, {"bold": active, "color": NAVY if active else MUTED})]], size=9, check=False)
            x += 3.08
        hline(s, 0.5, 0.46, 12.33, RULE, 0.75)
    tb(s, 0.5, 0.52, 12.33, 0.95, [title], size=21, bold=True, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
    hline(s, 0.5, 1.5, 12.33, NAVY, 1.5)
    page = len(prs.slides)
    if source:
        tb(s, 0.5, 6.9, 11.5, 0.46, [source], size=8, color=MUTED, anchor=MSO_ANCHOR.BOTTOM)
    tb(s, 12.2, 6.98, 0.63, 0.36, [str(page)], size=9, color=MUTED, align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.BOTTOM, check=False)
    return s


def style_chart_common(chart, legend=False):
    chart.has_legend = legend
    chart.font.name = FONT
    chart.font.size = Pt(10)
    chart.font.color.rgb = INK2
    # transparent chart area
    cs = chart._chartSpace
    spPr = cs.find(qn("c:spPr"))
    if spPr is None:
        spPr = etree.SubElement(cs, qn("c:spPr"))
    for child in list(spPr):
        spPr.remove(child)
    etree.SubElement(spPr, qn("a:noFill"))
    ln = etree.SubElement(spPr, qn("a:ln")); etree.SubElement(ln, qn("a:noFill"))


def bar_chart(slide, x, y, w, h, cats, vals, colors, fmt='0', horizontal=True, label_fmt=None,
              vmax=None, vmin=None, gap=60, label_size=11, cat_size=10, labels=None):
    cd = CategoryChartData()
    cd.categories = cats
    cd.add_series("s", vals)
    ctype = XL_CHART_TYPE.BAR_CLUSTERED if horizontal else XL_CHART_TYPE.COLUMN_CLUSTERED
    gf = slide.shapes.add_chart(ctype, Inches(x), Inches(y), Inches(w), Inches(h), cd)
    ch = gf.chart
    style_chart_common(ch)
    plot = ch.plots[0]
    plot.gap_width = gap
    plot.vary_by_categories = False
    ser = plot.series[0]
    ser.invert_if_negative = False
    for i, col in enumerate(colors):
        pt = ser.points[i]
        pt.format.fill.solid(); pt.format.fill.fore_color.rgb = col
        pt.format.line.fill.background()
    plot.has_data_labels = True
    dl = plot.data_labels
    dl.number_format = label_fmt or fmt
    dl.number_format_is_linked = False
    dl.position = XL_LABEL_POSITION.OUTSIDE_END
    dl.font.size = Pt(label_size); dl.font.bold = True; dl.font.color.rgb = INK
    if labels:
        for i, t in enumerate(labels):
            if t is None:
                continue
            tf = ser.points[i].data_label.text_frame
            tf.text = t
            for p in tf.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(label_size); r.font.bold = True; r.font.color.rgb = INK; r.font.name = FONT
            ser.points[i].data_label.position = XL_LABEL_POSITION.OUTSIDE_END
    va = ch.value_axis
    va.visible = False
    va.has_major_gridlines = False
    if vmax is not None:
        va.maximum_scale = vmax
    va.minimum_scale = vmin if vmin is not None else 0
    ca = ch.category_axis
    ca.tick_labels.font.size = Pt(cat_size)
    ca.tick_labels.font.color.rgb = INK
    ca.format.line.color.rgb = GREY
    ca.major_tick_mark = XL_TICK_MARK.NONE
    if horizontal:
        ca.reverse_order = True
    ca.tick_label_position = XL_TICK_LABEL_POSITION.LOW
    return ch


def table(slide, x, y, w, h, data, col_w, header_fill=NAVY, size=10, row_h=None, bold_first_col=True,
          fills=None, colors=None, header_size=None, aligns=None):
    rows, cols = len(data), len(data[0])
    gt = slide.shapes.add_table(rows, cols, Inches(x), Inches(y), Inches(w), Inches(h))
    t = gt.table
    tblPr = t._tbl.tblPr
    # strip default style banding
    tblPr.set("bandRow", "0"); tblPr.set("firstRow", "0")
    for j, cw in enumerate(col_w):
        t.columns[j].width = Inches(cw)
    for i in range(rows):
        if row_h:
            t.rows[i].height = Inches(row_h[i] if isinstance(row_h, list) else row_h)
        for j in range(cols):
            cell = t.cell(i, j)
            val = data[i][j]
            cell.margin_left = cell.margin_right = Inches(0.06)
            cell.margin_top = cell.margin_bottom = Inches(0.03)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = cell.text_frame; tf.word_wrap = True
            runs = val if isinstance(val, list) else [(val, {})]
            p = tf.paragraphs[0]
            if aligns:
                p.alignment = aligns[j]
            for txt, ro in runs:
                r = p.add_run(); r.text = txt
                r.font.name = FONT
                r.font.size = Pt(ro.get("size", header_size or size if i == 0 else size))
                r.font.bold = ro.get("bold", i == 0 or (bold_first_col and j == 0))
                default_col = WHITE if i == 0 else INK
                if colors and colors.get((i, j)):
                    default_col = colors[(i, j)]
                r.font.color.rgb = ro.get("color", default_col)
            cell.fill.solid()
            if i == 0:
                cell.fill.fore_color.rgb = header_fill
            elif fills and fills.get((i, j)) is not None:
                cell.fill.fore_color.rgb = fills[(i, j)]
            else:
                cell.fill.fore_color.rgb = WHITE if i % 2 else LIGHTGREY
    return t


def callout(slide, x, y, w, h, head, body, size=11, fill=LIGHTBLUE, head_color=NAVY):
    paras = [{"runs": [(head, {"bold": True, "color": head_color})], "size": size + 1}]
    for b in body:
        if isinstance(b, dict):
            paras.append(b)
        else:
            paras.append({"runs": [(b, {})], "size": size, "space_before": 4})
    return tb(slide, x, y, w, h, paras, size=size, fill=fill, margin=0.12)


def bullets(slide, x, y, w, h, items, size=12, head=None, head_size=None):
    paras = []
    if head:
        paras.append({"runs": [(head, {"bold": True, "color": NAVY})], "size": head_size or size + 1})
    for it in items:
        lvl = 0
        if isinstance(it, tuple) and isinstance(it[0], int):
            lvl, it = it
        runs = it if isinstance(it, list) else [(it, {})]
        paras.append({"runs": runs, "bullet": True, "level": lvl, "size": size - (1 if lvl else 0),
                      "space_before": 5 if lvl == 0 else 2})
    return tb(slide, x, y, w, h, paras, size=size)


def B(t):
    return (t, {"bold": True})


def N(t):
    return (t, {})


# ============================================================================= SLIDES
# 1 Title -----------------------------------------------------------------------
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, 13.333, 7.5, NAVY)
rect(s, 0.6, 2.05, 0.08, 2.6, BLUE)
tb(s, 0.85, 1.2, 11, 0.5, ["Brightwork  |  Executive team, January 2027 planning"], size=14, color=LIGHTBLUE)
tb(s, 0.85, 1.95, 11.6, 1.9, ["Dispatch Copilot: launch it in a Pro tier in Q4 2027, after the mobile app, rather than as a $149 add-on in Q2"],
   size=32, bold=True, color=WHITE)
tb(s, 0.85, 3.95, 11, 0.8, ["Recommendation on launch timing, packaging and price for CEO Maya Okafor and the executive team"],
   size=16, color=LIGHTBLUE)
tb(s, 0.85, 6.3, 11.8, 0.7, ["Prepared November 2026 using only the internal briefing pack. All company, competitor and market figures are synthetic benchmark data. "
                              "Figures are annual and in US$ unless stated."], size=10, color=LIGHTBLUE)

# 2 Executive summary ------------------------------------------------------------
s = new_slide("Executive summary: launch Copilot in Q4 2027 inside a new Pro tier at +$12 per seat, and keep the mobile rewrite on schedule",
              source="Source: Brightwork briefing pack (Nov 2026); team analysis. Calculations on the slides that follow and in the appendix.")
tb(s, 0.5, 1.65, 12.33, 0.78,
   [[B("Answer: "), N("Yes, launch Dispatch Copilot, but in Q4 2027 rather than Q2, and inside a new Pro plan at $91 per seat ($12 above Core) "
                      "with a pooled usage allowance. Plan on $1.2–2.9M of new ARR, not $8M. Copilot and the mobile fix are both needed to lift NRR to 105%.")]],
   size=13, fill=LIGHTBLUE, margin=0.12, anchor=MSO_ANCHOR.MIDDLE)
rows = [
    ("1", "Copilot is worth launching, but the prize is $1.2–2.9M of new ARR, not $8M",
     ["Only 14% of beta volunteers paid $149 when asked (17 of 120). The 46% survey figure comes from the 6% of admins who replied, and they run larger accounts",
      f"AI can explain at most the 7-point fall in win rate against Routewise: ~110 deals and {m(C['comp_arr'])} of new ARR a year, not a third of all losses"]),
    ("2", "Package it in Pro at +$12 per seat with 600 requests per seat, not as a $149 add-on",
     [f"Pro brings in as much ARR ({m(C['pro33']['rev'])} at the 33% uptake of the 2023 tier, vs {m(C['add14']['rev'])} for the add-on). Its cost grows with seats, and it matches Routewise's 'AI included in Pro'",
      f"With the allowance, company gross margin stays at {C['pro_cap']['cogm']*100:.1f}% or more in the worst usage case. Bundling Copilot free into Core would cut it to {C['free_cogm']*100:.1f}%"]),
    ("3", "Launch in Q4 2027: fixing the mobile app comes first",
     [f"Mobile reliability causes 27% of churn and AI features 6%. Two quarters of mobile delay put {m(C['mob_half_50'])}–{m(C['mob_half_100'])} of ARR at risk. Two quarters of Copilot delay put at most {m(C['cop_half_ceiling'])} at risk",
      f"Reaching 105% NRR takes both: the mobile fix adds about +{C['nrr_mob50']:.1f} pts and Copilot Pro adds +2.1 to +5.0 pts"]),
]
y = 2.6
for num, head, subs in rows:
    rect(s, 0.5, y + 0.05, 0.42, 0.42, NAVY, shape=MSO_SHAPE.OVAL)
    tb(s, 0.5, y + 0.05, 0.42, 0.42, [num], size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, check=False)
    tb(s, 1.05, y, 4.0, 1.18, [head], size=13, bold=True, color=NAVY)
    bullets(s, 5.15, y - 0.02, 7.68, 1.2, subs, size=11)
    hline(s, 1.05, y + 1.24, 11.78, RULE, 0.75)
    y += 1.32
tb(s, 0.5, 6.58, 12.33, 0.42,
   [[B("Decisions for January: "), N("approve the sequence and the Pro design; run a paid early-access test in H1 2027; bring the launch forward to Q2 only if one of the triggers on slide 16 fires.")]],
   size=11, color=INK, fill=LIGHTGREY, margin=0.08, anchor=MSO_ANCHOR.MIDDLE)

# 3 Hypothesis test ---------------------------------------------------------------
s = new_slide("We tested the CPO's plan against five conditions. Demand and timing failed, so the answer changed",
              source="Source: Briefing pack §4–§8, §10; team analysis.")
tb(s, 0.5, 1.62, 12.33, 0.45, [[B("Starting hypothesis (CPO): "), N("launch in Q2 2027 as a paid add-on at $149 per account per month, worth about $8M of ARR in year 1.")]],
   size=12, fill=LIGHTGREY, margin=0.1, anchor=MSO_ANCHOR.MIDDLE)
X, H, P = ("Not supported", {"bold": True, "color": RED}), ("Partly", {"bold": True, "color": AMBER}), ("Holds", {"bold": True, "color": GREEN})
data = [
    ["What would have to be true", "Evidence", "Verdict", "Implication"],
    ["Demand: about 46% of accounts will pay $149 a month",
     "Paywall test: 17 of 120 beta volunteers (14%) bought. The survey had a 6% response rate, and respondents average 9.4 seats against 6.2 for the base",
     [X], f"The add-on is worth {m(C['add14']['rev'])} of ARR at most, not {m(C['cpo'])}"],
    ["Economics: the price covers inference and company GM stays ≥75%",
     f"The add-on's own margin is {C['add14']['fgm']*100:.0f}% and company GM {C['add14']['cogm']*100:.1f}%. The top 10% of accounts cost $131 a month to serve against a $149 price",
     [("Holds, but thin", {"bold": True, "color": AMBER})], "Price per seat and cap usage"],
    ["Competition: AI is why we lose to Routewise",
     "Win rate fell 7 points while Routewise was offering 20% off. 31% of loss notes 'mention' AI. AI is the main reason for only 6% of churn",
     [H], f"At most {m(C['comp_arr'])} of new ARR a year is at stake"],
    ["Opportunity cost: a two-quarter mobile delay costs less than a two-quarter Copilot delay",
     f"Mobile drives 27% of churn. A two-quarter delay puts {m(C['mob_half_50'])}–{m(C['mob_half_100'])} of ARR at risk, against ≤{m(C['cop_half_ceiling'])} for Copilot",
     [X], "Protect mobile and launch Copilot in Q4 2027"],
    ["Proven value: beta gains will hold across the customer base",
     "Beta: +11% jobs per dispatcher-hour vs +2% for matched accounts, and 97% vs 93% renewal. But the accounts volunteered and are larger (8.1 seats)",
     [("Unproven", {"bold": True, "color": AMBER})], "Leave retention upside out of the case and test it"],
]
table(s, 0.5, 2.2, 12.33, 3.9, data, [2.9, 5.0, 1.55, 2.88], size=10.5, row_h=[0.4, 0.7, 0.7, 0.7, 0.7, 0.7])
tb(s, 0.5, 6.25, 12.33, 0.62, [[B("Revised answer: "), N("launch in Q4 2027, after the mobile rewrite, inside a per-seat Pro tier with a usage allowance. Size the case at $1.2–2.9M, not $8M.")]],
   size=12, fill=LIGHTBLUE, margin=0.1, anchor=MSO_ANCHOR.MIDDLE)

# 4 Demand ---------------------------------------------------------------------
s = new_slide("Survey intent overstates demand: what customers actually paid points to at most $2.5M of add-on ARR, not $8M",
              section=0, source="Source: Briefing pack §4, §6, §10 (survey method note), §5. ARR = accounts × $149 × 12. The 7% case is our illustrative haircut for the fact that beta accounts volunteered.")
tb(s, 0.5, 1.7, 6.6, 0.4, ["Year-1 add-on ARR at $149 a month, by adoption source ($M)"], size=12, bold=True)
bar_chart(s, 0.5, 2.1, 6.6, 3.0,
          ["Survey: 46% 'likely' (CPO)", "Paywall test: 14% bought", "Paywall halved for non-volunteers: 7%"],
          [C["cpo"] / 1e6, C["add14"]["rev"] / 1e6, C["add7"]["rev"] / 1e6], [GREY, NAVY, BLUE], label_fmt='"$"0.0"M"', vmax=9.5, cat_size=11)
tb(s, 0.5, 5.2, 6.6, 1.6, [
    {"runs": [B("How the numbers are built")], "size": 11},
    {"runs": [N("Survey: 9,800 × 46% = 4,508 accounts × $1,788 a year = $8.1M")], "size": 10.5, "space_before": 3},
    {"runs": [N("Paywall: 9,800 × 14% = 1,372 accounts × $1,788 a year = $2.5M")], "size": 10.5, "space_before": 2},
    {"runs": [N("Non-volunteer case: 9,800 × 7% = 686 accounts × $1,788 a year = $1.2M")], "size": 10.5, "space_before": 2},
], size=10.5, fill=LIGHTGREY, margin=0.1)
bullets(s, 7.5, 1.7, 5.33, 5.1, [
    [B("Few people answered, and they were not typical. "), N("Only 610 of 9,800 admins (6%) replied. They average 9.4 seats against 6.2 for the base, so the sample leans to large, engaged accounts")],
    [B("Saying 'likely' is not buying. "), N("When the 120 beta accounts were actually asked to pay $149, 17 did (14%), less than a third of the survey's 46%")],
    [B("14% is a ceiling, not a base case. "), N("Beta accounts volunteered and are larger (8.1 seats) and more active than the base, so the base will convert at a lower rate")],
    [B("Buyers are heavy users. "), N("Those who paid averaged 6,800 requests a month, almost twice the beta mean of 3,600. That raises the cost of serving them (slide 8)")],
    [B("So what: "), N("plan on $1.2–2.5M from a $149 add-on and test conversion on a random sample of accounts that did not volunteer")],
], size=12, head="Why the 46% does not translate into revenue")

# 5 Competition ------------------------------------------------------------------
s = new_slide("Against Routewise, Copilot can win back at most ~110 deals a year (about $0.6M of ARR), not a third of our losses",
              section=0, source="Source: Briefing pack §7, §10 (VP Sales memo), §11. New account = 6.2 seats × $79 × 12 = $5,878 ARR. Pre-AI win rate assumed to be the Q1–Q2 2026 rate.")
tb(s, 0.5, 1.7, 6.3, 0.4, ["Brightwork win rate in deals where Routewise competes (%)"], size=12, bold=True)
bar_chart(s, 0.5, 2.1, 6.3, 3.0, ["Q1–Q2 2026 (before Routewise AI)", "Q3 2026 (AI launch + 20% promo)", "Implied by VP Sales claim"],
          [44, 37, C["vp_rate"] * 100], [NAVY, BLUE, GREY], label_fmt='0"%"', vmax=68, cat_size=11)
tb(s, 0.5, 5.2, 6.3, 1.6, [
    {"runs": [B("How the numbers are built")], "size": 11},
    {"runs": [N("2,600 opportunities × 60% = 1,560 Routewise deals a year")], "size": 10.5, "space_before": 3},
    {"runs": [N(f"7-pt drop × 1,560 = {C['lost_wins']:.0f} deals × $5,878 = {m(C['comp_arr'], 2)} of new ARR a year")], "size": 10.5, "space_before": 2},
    {"runs": [N(f"VP claim: 1/3 × {1560*0.63:.0f} losses = {C['vp_deals']:.0f} deals → {C['vp_rate']*100:.0f}% win rate")], "size": 10.5, "space_before": 2},
], size=10.5, fill=LIGHTGREY, margin=0.1)
bullets(s, 7.2, 1.7, 5.63, 5.1, [
    [B("The VP Sales claim fails a basic check. "), N(f"Winning back a third of our losses would lift the win rate to {C['vp_rate']*100:.0f}%, 14 points higher than before Routewise had any AI")],
    [B("Mentioning AI is not the same as losing on AI. "), N("31% of Q3 loss notes mention AI, but a note can mention it without AI deciding the deal")],
    [B("Price is a competing explanation. "), N("Routewise offered 20% off the first year in the same quarter it launched AI, and price already causes 22% of our churn")],
    [B(f"So {m(C['comp_arr'])} a year is the most Copilot can be worth here, "), N("and it counts as new-customer growth, not NRR")],
    [B("A test is available by January. "), N("Q4 2026 win rates come after the promo ended. If they stay at or below 37%, AI is the likely cause, and that would make launching sooner more urgent")],
], size=12, head="Why the competitive upside is real but limited")

# 6 Beta evidence -----------------------------------------------------------------
s = new_slide("The beta shows Copilot helps engaged accounts, but it cannot yet prove the gains will hold across the customer base",
              section=0, source="Source: Briefing pack §5 Tables 1–2, §11. Difference = beta minus matched non-beta accounts.")
data = [
    ["Measure", "Beta accounts", "Matched non-beta", "Difference", "How much to trust it"],
    ["Jobs scheduled per dispatcher-hour vs prior 12 weeks", "+11%", "+2%", "+9 pts", "Medium. Has a comparison group, but the accounts volunteered"],
    ["90-day renewal rate", "97%", "93%", "+4 pts", "Low. Engaged volunteers would likely renew anyway"],
    ["Dispatcher hours saved per week", "4.1", "—", "n/a", "Low. Self-reported, with no control group"],
]
table(s, 0.5, 1.75, 7.6, 2.5, data, [2.4, 1.05, 1.15, 0.95, 2.05], size=10.5, row_h=[0.45, 0.68, 0.68, 0.68],
      aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.LEFT])
tb(s, 0.5, 4.45, 7.6, 0.4, ["AI requests per account per month in the beta: usage is concentrated"], size=12, bold=True)
bar_chart(s, 0.5, 4.8, 7.6, 2.05, ["Median account", "Mean account", "Mean of top 10% of accounts"], [1900, 3600, 14500],
          [GREY, BLUE, NAVY], label_fmt='#,##0', vmax=17500, cat_size=10.5, gap=45)
bullets(s, 8.5, 1.75, 4.33, 5.1, [
    [B("The signal is positive. "), N("Productivity rose 9 points more than in matched accounts, and beta accounts renewed more often")],
    [B("Selection bias limits it. "), N("The accounts volunteered and are larger (8.1 vs 6.2 seats) and more active, so the effect will probably shrink across the base")],
    [B("A few accounts drive the value. "), N("The top 10% of accounts made 58% of all requests. The mean is almost twice the median")],
    [B("So what: "), N("we leave retention gains out of the business case. Early access for a random sample of Core accounts will measure them on typical customers")],
], size=12, head="What we can and cannot conclude")

# 7 Options ---------------------------------------------------------------------
s = new_slide("A Pro tier at +$12 per seat beats both a $149 add-on and a free bundle on margin, cost control and fit against Routewise",
              section=1, source="Source: Briefing pack §1, §5, §6, §7; team analysis. Inference $0.009 per request (fixed through Dec 2027). Platform $0.6M a year counted as cost of revenue. Pro usage = beta mean 444 requests per seat per month ($4.00). Company GM base: $57.6M ARR at 78%.")
g, r_, a_ = {"color": GREEN, "bold": True}, {"color": RED, "bold": True}, {"color": AMBER, "bold": True}
data = [
    ["", "A. Paid add-on: $149 per account per month", "B. Pro tier: +$12 per seat per month (recommended)", "C. Include in Core at no charge"],
    ["How it is priced", "Flat price per account", "Per seat, with 600 requests per seat a month pooled across the account", "No extra price"],
    ["Adoption evidence", "14% (paywall test, volunteers) is the ceiling. 7% for non-volunteers", "33% (2023 higher-tier precedent) as the base case. 14% as the low case", "All accounts get it"],
    ["New ARR", f"{m(C['add14']['rev'])} at the ceiling, {m(C['add7']['rev'])} at 7%", f"{m(C['pro33']['rev'])} base, {m(C['pro14']['rev'])} low", "$0"],
    ["Inference + platform cost", f"{m(C['add14']['inf']+6e5)} (buyers use 6,800 requests a month)", f"{m(C['pro33']['inf']+6e5)} base, at most {m(C['pro_cap']['inf']+6e5)} under the allowance", f"{m(C['free_cost'])} with no revenue to cover it"],
    ["Margin on the feature itself", f"{C['add14']['fgm']*100:.0f}%", f"{C['pro33']['fgm']*100:.0f}% base, at least {C['pro_cap']['fgm']*100:.0f}% under the allowance", "Negative"],
    ["Company gross margin (floor 75%)", [(f"{C['add14']['cogm']*100:.1f}%", g)], [(f"{C['pro33']['cogm']*100:.1f}% base, at least {C['pro_cap']['cogm']*100:.1f}%", g)], [(f"{C['free_cogm']*100:.1f}%, below the floor", r_)]],
    ["NRR uplift", f"+{C['add7']['nrr']:.1f} to +{C['add14']['nrr']:.1f} pts", f"+{C['pro14']['nrr']:.1f} to +{C['pro33']['nrr']:.1f} pts", "None directly"],
    ["Fit against Routewise (AI included in Pro)", [("Weak: 'AI costs extra' in head-to-head deals", a_)], [("Parity: 'AI included in Pro'", g)], [("Strong, but we cannot afford it", a_)]],
    ["Cost risk", [("Heavy users cost nearly the full price to serve", r_)], [("Revenue grows with seats and the allowance limits cost", g)], [("Cost has no ceiling", r_)]],
    ["Verdict", [("Reject", r_)], [("Recommend", g)], [("Reject: breaches the 75% margin floor", r_)]],
]
fills = {(i, 2): RGBColor(0xE6, 0xF0, 0xFC) for i in range(1, len(data))}
table(s, 0.5, 1.68, 12.33, 5.2, data, [2.45, 3.1, 3.9, 2.88], size=10, row_h=[0.5] + [0.47] * 10, fills=fills)

# 8 Unit economics ------------------------------------------------------------------
s = new_slide("A flat $149 price attracts heavy users: serving the top 10% of accounts would use up 88% of the price in inference alone",
              section=1, source="Source: Briefing pack §5 Table 2, §6. Inference cost = requests per month × $0.009. Per-seat figure = 3,600 requests ÷ 8.1 beta seats = 444 requests per seat.")
tb(s, 0.5, 1.7, 7.3, 0.4, ["Inference cost per account per month vs the $149 add-on price ($)"], size=12, bold=True)
cats = ["Median beta account (1,900 req)", "Mean beta account (3,600 req)", "Paywall buyers (6,800 req)", "Top 10% of accounts (14,500 req)", "Add-on price"]
vals = [1900 * .009, 3600 * .009, 6800 * .009, 14500 * .009, 149]
bar_chart(s, 0.5, 2.1, 7.3, 3.4, cats, vals, [GREY, GREY, BLUE, NAVY, ORANGE], label_fmt='"$"0', vmax=175, cat_size=10.5, gap=45)
tb(s, 0.5, 5.6, 7.3, 1.25, [
    {"runs": [B("Margin left after inference at $149")], "size": 11},
    {"runs": [N("Paywall buyer: ($149 − $61) ÷ $149 = 59%.   Top 10%: ($149 − $131) ÷ $149 = 12%")], "size": 10.5, "space_before": 3},
    {"runs": [N("Break-even: $149 ÷ $0.009 = 16,556 requests a month. Any account above that loses money")], "size": 10.5, "space_before": 2},
], size=10.5, fill=LIGHTGREY, margin=0.1)
bullets(s, 8.2, 1.7, 4.63, 5.1, [
    [B("A flat price selects for heavy use. "), N("The accounts that paid used almost twice the beta mean, because they get the most from a fixed fee")],
    [B("Pricing per seat follows usage. "), N("Usage grows with dispatcher seats: $4.00 of inference per seat against a $12 price leaves 67% before platform cost")],
    [B("Smaller accounts pay less. "), N("A typical 6.2-seat account pays $74 a month for Pro instead of $149. That matters when price causes 22% of churn")],
    [B("So what: "), N("charge per seat and set an allowance, so that one heavy account cannot turn the feature unprofitable")],
], size=12, head="Why per-seat pricing is the better structure")

# 9 Margin guardrail ----------------------------------------------------------------
s = new_slide("A pooled allowance of 600 requests per seat keeps company gross margin above 75% even if only heavy users upgrade",
              section=1, source="Source: Briefing pack §1, §3, §5, §6; team analysis. Pro scenarios assume 33% adoption (3,234 accounts × 6.2 seats). Stress case: every upgrader uses 6,800 requests a month. Capped case: every seat uses its full 600 requests.")
tb(s, 0.5, 1.7, 7.6, 0.4, ["Company gross margin above (+) or below (−) the 75% floor, percentage points"], size=12, bold=True)
scen = [("Today (no Copilot)", 0.78), ("Pro, usage at the beta average", C["pro33"]["cogm"]),
        ("Pro, stress case with an allowance", C["pro_cap"]["cogm"]), ("Pro, stress case with no allowance", C["pro_heavy"]["cogm"]),
        ("Copilot free in Core", C["free_cogm"])]
vals = [(v - 0.75) * 100 for _, v in scen]
labels = [f"{v:+.1f} pts ({g_*100:.1f}%)" for v, (_, g_) in zip(vals, scen)]
bar_chart(s, 0.5, 2.1, 7.6, 3.5, [n for n, _ in scen], vals, [GREY, BLUE, NAVY, RED, RED], vmax=4.5, vmin=-5.5, cat_size=10.5,
          labels=labels, gap=45)
tb(s, 0.5, 5.7, 7.6, 1.15, [
    {"runs": [B("Worked example, stress case with no allowance")], "size": 11},
    {"runs": [N("Inference: 3,234 accounts × 6,800 requests × $0.009 × 12 = $2.4M. Adding $0.6M of platform cost gives $3.0M of extra cost against $2.9M of Pro ARR")], "size": 10.5, "space_before": 3},
    {"runs": [N("Company GM = 1 − ($12.7M + $3.0M) ÷ ($57.6M + $2.9M) = 74.1%")], "size": 10.5, "space_before": 2},
], size=10.5, fill=LIGHTGREY, margin=0.1)
bullets(s, 8.5, 1.7, 4.33, 5.1, [
    [B("Without an allowance, Pro could breach the floor. "), N("If upgraders behave like the paywall buyers, company GM falls to 74.1%")],
    [B("600 requests per seat caps the downside. "), N(f"That is $5.40 of inference against $12, so company GM stays at {C['pro_cap']['cogm']*100:.1f}% or more whatever the usage mix")],
    [B("Typical users never hit it. "), N("The beta average is 444 requests per seat, and the median account used about 235 per seat")],
    [B("Margin improves after 2027. "), N("Our $0.009 rate is fixed through December 2027, and the provider's list prices fell 35% last year. Re-price at renewal")],
], size=12, head="Why the allowance matters")

# 10 Package design -------------------------------------------------------------------
s = new_slide("The recommended package adds Copilot to a new Pro plan at $91 per seat and leaves the $79 Core plan unchanged",
              section=1, source="Source: Briefing pack §1, §5, §6, §8; team analysis. The allowance and the overage pack price are our proposals for early access to test. Hours saved are self-reported by beta volunteers.")
cards = [
    ("Price", ["$91 per seat per month (Core $79 + $12)", "Core keeps its price: price causes 22% of churn, so no one is forced to upgrade", "Typical account: 6.2 seats × $12 = $74 a month extra"]),
    ("What is included", ["All three Copilot features: schedule proposals, quote drafts from technician notes, call summaries", "Positioned as 'AI included in Pro', the same as Routewise"]),
    ("Usage guardrail", ["600 AI requests per seat per month, pooled across the account (1.35× the beta average)", "Top-up packs at $20 per 1,000 requests (55% margin at $0.009)", "Admins see a usage meter, and nothing stops working without warning"]),
    ("Migration", ["The 17 accounts paying $149 move to Pro. Most will pay less, which builds goodwill", "Other beta accounts are offered early access to Pro at the Pro price"]),
]
x = 0.5
for head, items in cards:
    rect(s, x, 1.75, 2.95, 0.5, NAVY)
    tb(s, x, 1.75, 2.95, 0.5, [head], size=13, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE, margin=0.12)
    rect(s, x, 2.25, 2.95, 2.75, LIGHTGREY)
    bullets(s, x + 0.05, 2.3, 2.85, 2.65, items, size=12)
    x += 3.127
callout(s, 0.5, 5.2, 12.33, 1.6, "Value check: Pro pays for itself many times over at the hours the beta reported",
        ["Beta dispatchers reported saving 4.1 hours a week, about 17.8 hours a month per account. A 6.2-seat account pays $74 a month, "
         "so it breaks even at $4.20 per hour saved. Even if the real saving is a quarter of what was reported, the break-even is about $17 per hour. "
         "The $149 add-on would need $8.40 per hour at the reported saving."], size=11)

# 11 Customer problem ------------------------------------------------------------------
s = new_slide("Customers' biggest problem is the mobile app, not AI: it causes 4.5× as much churn and gets twice as many first-choice votes",
              section=2, source="Source: Briefing pack §1, §8 Table 3 (n = 1,190 churned accounts, 2026 to date) and 2026 customer survey. Annual churn = 9,800 × 14% = 1,372 accounts; ARR assumes churned accounts are average size (6.2 seats).")
tb(s, 0.5, 1.7, 6.4, 0.4, ["Main reason given by churned accounts, 2026 (% of accounts)"], size=12, bold=True)
reasons = ["Mobile app reliability", "Price", "Missing integrations", "Out of business / sold", "Switched for AI features", "Other"]
share = [27, 22, 15, 14, 6, 16]
bar_chart(s, 0.5, 2.1, 6.4, 3.4, reasons, share, [NAVY, GREY, GREY, GREY, BLUE, GREY], label_fmt='0"%"', vmax=32, cat_size=11, gap=40)
tb(s, 7.2, 1.7, 5.63, 0.4, ["Feature ranked first, 2026 customer survey (%)"], size=12, bold=True)
bar_chart(s, 7.2, 2.1, 5.63, 1.6, ["Reliable technician mobile app", "AI scheduling"], [38, 19], [NAVY, BLUE], label_fmt='0"%"', vmax=46, cat_size=11, gap=40)
data = [
    ["Churn driver", "Accounts per year", "ARR lost per year"],
    ["All reasons (14%)", f"{C['churn_accts']:,.0f}", m(C["churn_arr"])],
    ["Mobile app reliability (27%)", f"{C['churn_accts']*.27:,.0f}", m(C["mob_arr"])],
    ["Switched for AI features (6%)", f"{C['churn_accts']*.06:,.0f}", m(C["ai_arr"])],
]
table(s, 7.2, 3.95, 5.63, 1.55, data, [2.83, 1.4, 1.4], size=10.5, row_h=0.38, aligns=[PP_ALIGN.LEFT, PP_ALIGN.RIGHT, PP_ALIGN.RIGHT])
callout(s, 0.5, 5.7, 12.33, 1.15, "So what: the mobile app is where churn is lost, and churn is where NRR is lost",
        [f"Mobile-driven churn costs about {m(C['mob_arr'])} of ARR a year, 4.5 times the {m(C['ai_arr'])} lost to AI features. That is why the Head of Customer Success is right to guard the rewrite."], size=11)

# 12 Cost of delay ------------------------------------------------------------------
s = new_slide("A two-quarter delay to the mobile rewrite puts up to twice as much ARR at risk as a two-quarter delay to Copilot",
              section=2, source="Source: Briefing pack §3, §7, §8, §9; team analysis. Six months = 0.5 × annual figure. 'Half credit' assumes the Routewise promo explains half of the win-rate drop and Copilot prevents half of AI churn. Engineering cost: 14 × $210k × 0.5 yr = $1.47M in either order.")
tb(s, 0.5, 1.7, 7.4, 0.4, ["ARR permanently lost during a two-quarter delay ($M)"], size=12, bold=True)
cats = ["Delay mobile: rewrite fixes all mobile churn", "Delay mobile: rewrite fixes half", "Delay Copilot: full credit for win rate + AI churn", "Delay Copilot: half credit (promo effect)"]
vals = [C["mob_half_100"] / 1e6, C["mob_half_50"] / 1e6, C["cop_half_ceiling"] / 1e6, C["cop_half_half"] / 1e6]
bar_chart(s, 0.5, 2.1, 7.4, 3.0, cats, vals, [NAVY, NAVY, BLUE, BLUE], label_fmt='"$"0.00"M"', vmax=1.35, cat_size=10.5, gap=45)
tb(s, 0.5, 5.2, 7.4, 1.65, [
    {"runs": [B("How the numbers are built")], "size": 11},
    {"runs": [N(f"Mobile: 1,372 churned × 27% × $5,878 = {m(C['mob_arr'],2)} a year → × 0.5 yr = {m(C['mob_half_100'],2)} (× 50% fixed = {m(C['mob_half_50'],2)})")], "size": 10.5, "space_before": 3},
    {"runs": [N(f"Copilot: ({m(C['comp_arr'],2)} win-rate gap + {m(C['ai_arr'],2)} AI churn) × 0.5 yr = {m(C['cop_half_ceiling'],2)}; half credit = {m(C['cop_half_half'],2)}")], "size": 10.5, "space_before": 2},
    {"runs": [N(f"Break-even: mobile-first wins if the rewrite fixes more than {C['be_ceiling']*100:.0f}% (full credit) or {C['be_half']*100:.0f}% (half credit) of mobile churn")], "size": 10.5, "space_before": 2},
], size=10.5, fill=LIGHTGREY, margin=0.1)
bullets(s, 8.3, 1.7, 4.53, 5.15, [
    [B("Losses to churn are permanent. "), N("An account that leaves while we wait for the mobile app does not come back when it ships")],
    [B("Copilot revenue is mostly postponed, not lost. "), N(f"Accounts that would take Pro in Q2 can take it in Q4. Six months of deferral costs {m(C['defer_gp_low'])}–{m(C['defer_gp'])} of gross profit")],
    [B("The threshold is not demanding. "), N(f"The rewrite only has to fix {C['be_half']*100:.0f}–{C['be_ceiling']*100:.0f}% of the churn caused by the app's reliability")],
    [B("The engineering cost is the same in either order. "), N("$1.47M. Only the sequence changes")],
    [B("So what: "), N("do the mobile rewrite first, unless the January data shows AI is costing us deals (slide 16)")],
], size=12, head="Why mobile goes first")

# 13 NRR bridge ---------------------------------------------------------------------
s = new_slide("Hitting 105% NRR by 2028 is safest with both levers: Copilot alone needs 26% of accounts on Pro, but with the mobile fix 14% is enough",
              section=2, source="Source: Briefing pack §1, §3, §6, §8; team analysis. 1 NRR point = $0.58M of ARR. Mobile lever = rewrite halves mobile-driven churn (illustrative). Pro lever = adoption × 6.2 seats × $144 a year. New-customer wins do not count in NRR.")
tb(s, 0.5, 1.7, 7.6, 0.4, ["NRR bridge, %: today to the 2028 target (low adoption case)"], size=12, bold=True)
# waterfall via stacked columns
cd = CategoryChartData()
cats = ["NRR today", "Mobile fix halves mobile churn", "Copilot Pro at 14% adoption", "2028 NRR"]
cd.categories = cats
base = [0, 101, 101 + C["nrr_mob50"], 0]
val = [101, C["nrr_mob50"], C["pro14"]["nrr"], 101 + C["nrr_mob50"] + C["pro14"]["nrr"]]
cd.add_series("base", base)
cd.add_series("value", val)
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_STACKED, Inches(0.5), Inches(2.1), Inches(7.6), Inches(3.6), cd)
ch = gf.chart
style_chart_common(ch)
plot = ch.plots[0]; plot.gap_width = 55; plot.overlap = 100
sb, sv = plot.series
sb.format.fill.background(); sb.format.line.fill.background()
for i, col in enumerate([GREY, NAVY, BLUE, NAVY]):
    pt = sv.points[i]; pt.format.fill.solid(); pt.format.fill.fore_color.rgb = col; pt.format.line.fill.background()
lbls = ["101%", f"+{C['nrr_mob50']:.1f}", f"+{C['pro14']['nrr']:.1f}", f"{val[3]:.1f}%"]
for i, t in enumerate(lbls):
    dl = sv.points[i].data_label
    dl.has_text_frame = True
    dl.text_frame.text = t
    dl.position = XL_LABEL_POSITION.INSIDE_END
    for p in dl.text_frame.paragraphs:
        for r in p.runs:
            r.font.size = Pt(12); r.font.bold = True; r.font.color.rgb = WHITE; r.font.name = FONT
va = ch.value_axis; va.minimum_scale = 98; va.maximum_scale = 106; va.visible = True
va.has_major_gridlines = True; va.major_gridlines.format.line.color.rgb = RULE
va.tick_labels.font.size = Pt(9); va.format.line.fill.background(); va.major_unit = 1
ca = ch.category_axis; ca.tick_labels.font.size = Pt(10.5); ca.tick_labels.font.color.rgb = INK
ca.format.line.color.rgb = GREY; ca.major_tick_mark = XL_TICK_MARK.NONE
tb(s, 0.5, 5.75, 7.6, 0.5, ["Axis starts at 98% so the steps are visible. The bars show changes in points, not absolute size."], size=9, color=MUTED)
data = [
    ["Lever (on $57.6M base)", "Low case", "Base case"],
    ["Mobile fix (halves mobile churn)", f"+{C['nrr_mob50']:.1f} pts", f"+{C['nrr_mob50']:.1f} pts"],
    ["Copilot Pro (14% / 33% adoption)", f"+{C['pro14']['nrr']:.1f} pts", f"+{C['pro33']['nrr']:.1f} pts"],
    ["2028 NRR", f"{101+C['nrr_mob50']+C['pro14']['nrr']:.1f}%", f"{101+C['nrr_mob50']+C['pro33']['nrr']:.1f}%"],
]
table(s, 8.5, 1.75, 4.33, 1.7, data, [2.33, 1.0, 1.0], size=10.5, row_h=0.42, aligns=[PP_ALIGN.LEFT, PP_ALIGN.RIGHT, PP_ALIGN.RIGHT])
bullets(s, 8.5, 3.6, 4.33, 3.25, [
    [B("Copilot alone "), N(f"would need {C['pro_alone_share']*100:.0f}% of accounts on Pro to close the 4-point gap ($2.3M)")],
    [B("With the mobile fix, "), N(f"Copilot needs only {C['pro_with_mob_share']*100:.0f}% adoption, the same rate we saw in the paywall test")],
    [B("Mobile alone "), N("would have to remove all of the churn it causes (+3.8 pts) to come close")],
    [B("So what: "), N("the sequence matters less than delivering both by 2028. The order on slide 12 just loses the least ARR along the way")],
], size=11.5)

# 14 Roadmap -------------------------------------------------------------------------
s = new_slide("The roadmap keeps mobile on track in H1, uses that time to test Pro pricing, and launches Copilot in Q4 2027",
              section=2, source="Source: Briefing pack §3, §5, §6, §11; team analysis. Assumes the 14 engineers are free to start Copilot in Q3 2027 (CTO to confirm). Early-access inference ≈ 490 accounts × 3,600 req × $0.009 × 12 ≈ $0.19M a year.")
qx0, qw = 3.6, 1.5
quarters = ["Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027", "H1 2028", "H2 2028"]
for i, q in enumerate(quarters):
    rect(s, qx0 + i * qw + 0.02, 1.72, qw - 0.04, 0.38, NAVY if i < 4 else BLUE)
    tb(s, qx0 + i * qw, 1.72, qw, 0.38, [q], size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, check=False)
# gates
gates = [(0.15, "Gate 1 · Jan 2027", "Read Q4 2026 win rate vs Routewise (after the promo)"),
         (1.95, "Gate 2 · end Q2 2027", "Early-access adoption and requests per seat confirm the $12 price and the 600 allowance"),
         (3.95, "2028", "NRR target of 105%. Re-price on new inference terms")]
y_g = 5.65
for pos, head, body in gates:
    gx = qx0 + pos * qw
    s_ = rect(s, gx - 0.09, y_g - 0.27, 0.18, 0.18, ORANGE, shape=MSO_SHAPE.DIAMOND)
    vline(s, gx, 2.15, y_g - 2.45, ORANGE, 1.0, dash=True)
    tb(s, gx - 0.1, y_g - 0.08, 2.55, 1.15, [{"runs": [B(head)], "size": 10.5}, {"runs": [N(body)], "size": 10, "space_before": 2}], size=10)
lanes = [
    ("Mobile app rewrite", [(0, 2, NAVY, "Full team, no diversion")]),
    ("Copilot early access (existing beta)", [(0, 3, BLUE, "240 beta + ~250 random Core accounts at the Pro price")]),
    ("Copilot launch build (14 engineers)", [(2, 2, NAVY, "Hardening, scale, allowance metering")]),
    ("Pro tier on sale", [(3, 1, ORANGE, "General availability"), (4, 2, LIGHTBLUE, "Ramp toward 14–33% adoption")]),
    ("Inference contract", [(3, 1, GREY, "Renegotiate (fixed to Dec 2027)")]),
]
y = 2.25
for name, bars in lanes:
    tb(s, 0.5, y, 3.0, 0.55, [name], size=11, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    for start, length, col, label in bars:
        rect(s, qx0 + start * qw + 0.04, y + 0.06, length * qw - 0.08, 0.43, col)
        tb(s, qx0 + start * qw + 0.04, y + 0.06, length * qw - 0.08, 0.43, [label], size=9.5, bold=True,
           color=INK if col in (LIGHTBLUE, GREY) else WHITE, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER, margin=0.04)
    hline(s, 0.5, y + 0.6, 12.33, RULE, 0.5)
    y += 0.66
tb(s, 0.5, y_g - 0.08, 3.0, 1.15, [{"runs": [B("Decision gates")], "size": 11, "color": NAVY},
                                    {"runs": [N("Each gate can bring the launch forward or change the price (slide 16)")], "size": 10, "space_before": 2}], size=10)

# 15 Risks -----------------------------------------------------------------------
s = new_slide("Waiting carries risks, but each one can be watched and has a specific mitigation",
              section=3, source="Source: Briefing pack §5–§8, §11; team analysis.")
data = [
    ["Risk", "Why it matters", "Mitigation", "What we watch"],
    ["Routewise pulls further ahead in 2027", f"Up to {m(C['comp_arr'])} of new ARR a year if AI is what is driving the win-rate drop",
     "Sales can say 'AI included in Pro, early access now'. Gate 1 brings the launch forward if the drop is AI-driven", "Win rate in Routewise deals each quarter"],
    ["Pro adoption comes in below 14%", "NRR falls short of 105%, and the feature only covers its platform cost",
     "Early access on a random Core sample tests demand before launch. Adjust the price or bundle at Gate 2", "Early-access conversion and price feedback"],
    ["Heavy usage erodes margin", "Without a cap, company GM could fall to 74.1%",
     "600-request pooled allowance and top-up packs. Usage meter for admins", "Requests per seat; GM by month"],
    ["Productivity gains do not hold for typical accounts", "The case for Pro's value and its retention upside both weaken",
     "Measure on non-volunteers in early access. Retention upside is already left out of the case", "Jobs per dispatcher-hour vs control accounts"],
    ["The mobile rewrite under-delivers or slips", "The main reason for choosing this order disappears",
     "CS and Product set a churn-reduction target. Track reliability incidents", "Crash and failure rates; churn coded as mobile"],
    ["Inference prices change after 2027", "Upside if they fall (list prices are down 35% a year); risk if the contract is re-priced upward",
     "Renegotiate in Q4 2027. Keep the allowance until terms are known", "Provider list prices"],
]
table(s, 0.5, 1.7, 12.33, 5.15, data, [2.6, 3.3, 3.85, 2.58], size=10.5, row_h=[0.42] + [0.78] * 6)

# 16 Assumptions & triggers ----------------------------------------------------------
s = new_slide("Five assumptions carry the recommendation, and each comes with a test and a trigger that would change the plan",
              section=3, source="Source: Briefing pack; team analysis. Thresholds are taken from the calculations on slides 9, 12 and 13.")
data = [
    ["Assumption", "Evidence today", "How we test it, and when", "Trigger → change"],
    ["The win-rate drop is partly Routewise's price promo, not only AI", "The 20% promo ran in the same quarter (Q3 2026)",
     "Win rate in Routewise deals in Q4 2026, after the promo. January planning", [("Stays ≤37% → bring Copilot forward to Q2 2027 (Pro design unchanged)", {"bold": True})]],
    ["The rewrite removes at least 26–52% of mobile-driven churn", "Mobile causes 27% of churn and is the top request for 38%",
     "CS and Product estimate from churn interviews, by type of failure. January", [("Below 26% → launch Copilot first", {"bold": True})]],
    ["Doing mobile first moves Copilot back only two quarters", "Inferred from the staffing note (14 of 60 engineers)",
     "CTO resourcing plan. January", [("If 14 engineers can come from outside mobile → launch in Q2 with no trade-off. If Copilot would slip past Q1 2028 → revisit", {"bold": True})]],
    ["14–33% of accounts take Pro", "2023 tier precedent: 33%. Paywall test: 14%",
     "Conversion in early access on a random Core sample. Gate 2 (end Q2)", [("Below 14% → rethink the price before general availability", {"bold": True})]],
    ["Usage averages about 444 requests per seat", "Beta mean, from volunteers with concentrated usage",
     "Early-access telemetry. Gate 2", [("Above 600 → lower the allowance or raise the price", {"bold": True})]],
]
table(s, 0.5, 1.7, 12.33, 5.15, data, [3.0, 2.85, 3.0, 3.48], size=10.5, row_h=[0.42] + [0.946] * 5)

# 17 Next steps ---------------------------------------------------------------------
s = new_slide("Next steps: three decisions at January planning and four actions before Gate 2",
              section=3, source="Source: team analysis.")
callout(s, 0.5, 1.75, 5.9, 5.1, "Decisions requested from the executive team",
        [{"runs": [B("1.  Sequence. "), N("Keep the mobile rewrite fully staffed in H1 2027 and launch Copilot in Q4 2027, unless a trigger on slide 16 fires")], "size": 12, "space_before": 10},
         {"runs": [B("2.  Packaging and price. "), N("Approve a Pro plan at $91 per seat that includes Copilot with 600 pooled requests per seat. Core stays at $79. Retire the $149 add-on")], "size": 12, "space_before": 10},
         {"runs": [B("3.  Targets. "), N(f"Reset the Copilot business case to $1.2–2.9M of ARR. Set the NRR plan as the mobile fix plus Pro adoption of at least 14%")], "size": 12, "space_before": 10}],
        size=12)
data = [
    ["Action", "Owner", "By"],
    ["Pull Q4 2026 win rates in Routewise deals and read Gate 1", "VP Sales", "Jan 2027"],
    ["Confirm the 14 engineers can start Copilot in Q3 2027, or come from outside mobile", "CTO", "Jan 2027"],
    ["Estimate how much mobile-driven churn the rewrite removes", "Head of CS + CPO", "Feb 2027"],
    ["Launch paid early access: beta accounts plus ~250 randomly chosen Core accounts", "CPO", "Mar 2027"],
]
tb(s, 6.8, 1.75, 6.03, 0.4, ["Actions before Gate 2 (end Q2 2027)"], size=13, bold=True, color=NAVY)
table(s, 6.8, 2.2, 6.03, 3.3, data, [3.73, 1.3, 1.0], size=11, row_h=[0.42, 0.72, 0.72, 0.72, 0.72])
tb(s, 6.8, 5.7, 6.03, 1.15, [[B("Owners are our suggestions, "), N("based on the roles named in the briefing pack. The CEO should confirm them at January planning.")]],
   size=10.5, color=INK2, fill=LIGHTGREY, margin=0.1)

# A1 Calculations ----------------------------------------------------------------------
s = new_slide("Appendix A: every headline figure comes from briefing-pack inputs using the calculations below",
              source="Source: Briefing pack §1–§9. 'Team analysis' assumptions are listed in Appendix B.")
data = [
    ["Figure", "Calculation", "Result"],
    ["Current ARR", "9,800 accounts × 6.2 seats × $79 × 12", m(C["arr"])],
    ["CPO add-on claim", "9,800 × 46% × $149 × 12", m(C["cpo"])],
    ["Add-on ARR (paywall)", "9,800 × 14% × $149 × 12", m(C["add14"]["rev"], 2)],
    ["Add-on cost", "1,372 × 6,800 req × $0.009 × 12 + $0.6M platform", m(C["add14"]["inf"] + 6e5, 2)],
    ["Pro ARR (base / low)", "9,800 × 33% (or 14%) × 6.2 seats × $12 × 12", f"{m(C['pro33']['rev'],2)} / {m(C['pro14']['rev'],2)}"],
    ["Pro cost (base)", "3,234 × 6.2 seats × $4.00 × 12 + $0.6M", m(C["pro33"]["inf"] + 6e5, 2)],
    ["Company GM, Pro base", "1 − ($12.67M + $1.56M) ÷ ($57.6M + $2.89M)", f"{C['pro33']['cogm']*100:.1f}%"],
    ["Free-in-Core cost and GM", "9,800 × 6.2 × $4.00 × 12 + $0.6M; 1 − ($12.67M + $3.52M) ÷ $57.6M", f"{m(C['free_cost'],2)}; {C['free_cogm']*100:.1f}%"],
    ["Routewise win-rate gap", "2,600 × 60% × 7 pts × $5,878", m(C["comp_arr"], 2)],
    ["Mobile / AI churn ARR", "9,800 × 14% × 27% (6%) × $5,878", f"{m(C['mob_arr'],2)} / {m(C['ai_arr'],2)}"],
    ["Copilot engineering", "14 engineers × $210k × 0.5 year", m(C["eng"], 2)],
    ["Payback on engineering (Pro)", "$1.47M ÷ annual Pro gross profit after inference and platform", f"{C['eng']/C['pro33']['gp']:.1f} yrs base; {C['eng']/C['pro14']['gp']:.1f} yrs low"],
]
table(s, 0.5, 1.68, 12.33, 5.2, data, [2.9, 6.83, 2.6], size=10.5, row_h=[0.4] + [0.4] * 12, aligns=[PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.RIGHT])

# A2 Assumptions & judgement calls ------------------------------------------------------
s = new_slide("Appendix B: the judgement calls we made where the briefing pack was silent",
              source="Source: team analysis. These were made without the chance to consult the executive team. Each can be changed and the figures recomputed in build_deck.py.")
data = [
    ["Topic", "Choice we made", "Why", "Effect if wrong"],
    ["Platform cost ($0.6M)", "Counted as cost of revenue", "It covers running, evaluating and supporting the live feature", "If treated as opex, feature margins rise by about 20 pts"],
    ["Size of churned accounts", "Average of 6.2 seats", "No size data by churn reason", "If churned accounts are smaller, mobile ARR at risk is overstated"],
    ["Mobile rewrite effect", "Shown at 50% and 100% of mobile churn, plus a break-even", "No estimate in the pack", "The break-even (26–52%) is the number to challenge"],
    ["Pro usage per seat", "Beta mean: 3,600 ÷ 8.1 = 444 requests", "Only usage data available", "Volunteers likely use more, so this is a conservative cost"],
    ["Pro adoption", "33% base (2023 precedent), 14% low (paywall)", "Two independent reference points", "Tested in early access before launch"],
    ["Allowance and top-up price", "600 requests per seat; $20 per 1,000", "Covers the average with headroom and keeps GM ≥75%", "Tuned at Gate 2 on real usage"],
    ["Order of work", "Swapping the order moves Copilot back exactly two quarters", "The pack gives only the delay to mobile (two quarters). We assume the reverse is the same", "If Copilot slips further, revisit (slide 16)"],
]
table(s, 0.5, 1.68, 12.33, 5.2, data, [2.3, 3.3, 3.43, 3.3], size=10.5, row_h=[0.42] + [0.68] * 7)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Dispatch_Copilot_Recommendation.pptx")
prs.save(out)
with open(os.path.join(os.environ.get("TMPDIR", "/tmp"), "bw_textboxes.json"), "w") as f:
    json.dump(TEXTBOXES, f)
print("saved", out, len(prs.slides), "slides")
