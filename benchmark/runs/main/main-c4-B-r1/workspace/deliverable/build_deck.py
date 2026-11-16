"""Builds Palisade_2027_Pricing_Decision.pptx. All figures trace to evidence/briefing-pack.md;
calculations are reproduced in the appendix slides. Run: python3 build_deck.py"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION
import os

INK = RGBColor(0x0B, 0x0B, 0x0B); INK2 = RGBColor(0x52, 0x51, 0x4E); MUTED = RGBColor(0x8A, 0x89, 0x84)
BLUE = RGBColor(0x2A, 0x78, 0xD6); ORANGE = RGBColor(0xEB, 0x68, 0x34); GREY = RGBColor(0xC9, 0xC8, 0xC2)
NAVY = RGBColor(0x0D, 0x36, 0x6B); PALE = RGBColor(0xEE, 0xF4, 0xFC); RULE = RGBColor(0xDD, 0xDC, 0xD6)
WHITE = RGBColor(0xFF, 0xFF, 0xFF); PALEOR = RGBColor(0xFD, 0xEE, 0xE7)
FONT = "Arial"
W, H = 13.333, 7.5

prs = Presentation(); prs.slide_width = Inches(W); prs.slide_height = Inches(H)
BLANK = prs.slide_layouts[6]
FIT_WARN = []


def _fit_check(text, w, h, size, name):
    # rough Arial estimate: avg glyph 0.5em; line height 1.2em
    cpl = max(1, int(w * 72 / (0.5 * size)))
    lines = 0
    for para in text.split("\n"):
        lines += max(1, -(-len(para) // cpl))
    need = lines * size * 1.22 / 72 + 0.1
    if need > h + 0.02:
        FIT_WARN.append(f"{name}: needs {need:.2f}in, box {h:.2f}in :: {text[:50]}")


def tb(slide, x, y, w, h, text, size=12, bold=False, color=INK, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
       fill=None, line=None, italic=False, name="", margin=0.05):
    """Text box. `text` may be str or list of paragraphs; a paragraph may be a list of (run_text, bold) tuples."""
    shp = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)) if fill is None and line is None else \
        slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is not None or line is not None:
        if fill is None:
            shp.fill.background()
        else:
            shp.fill.solid(); shp.fill.fore_color.rgb = fill
        if line is None:
            shp.line.fill.background()
        else:
            shp.line.color.rgb = line; shp.line.width = Pt(0.75)
        shp.shadow.inherit = False
    tf = shp.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    for side in ("left", "right", "top", "bottom"):
        setattr(tf, f"margin_{side}", Inches(margin))
    paras = text if isinstance(text, list) else [text]
    plain = []
    for i, p in enumerate(paras):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = align
        runs = p if isinstance(p, list) else [(p, bold)]
        ptxt = ""
        for rt, rb in runs:
            r = para.add_run(); r.text = rt; ptxt += rt
            f = r.font; f.name = FONT; f.size = Pt(size); f.bold = rb; f.italic = italic; f.color.rgb = color
        plain.append(ptxt)
    _fit_check("\n".join(plain), w - 2 * margin, h - 2 * margin, size, name or plain[0][:20])
    return shp


def bullets(slide, x, y, w, h, items, size=12, color=INK, gap=4, name=""):
    """items: list of str or (str, level) or list-of-runs. Renders with bullet glyphs."""
    shp = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = shp.text_frame; tf.word_wrap = True
    for side in ("left", "right", "top", "bottom"):
        setattr(tf, f"margin_{side}", Inches(0.05))
    plain = []
    for i, it in enumerate(items):
        lvl = 0
        if isinstance(it, tuple):
            it, lvl = it
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.space_after = Pt(gap)
        runs = it if isinstance(it, list) else [(it, False)]
        glyph = "•  " if lvl == 0 else "–  "
        r = para.add_run(); r.text = ("      " * lvl) + glyph
        r.font.name = FONT; r.font.size = Pt(size); r.font.color.rgb = BLUE if lvl == 0 else MUTED; r.font.bold = True
        ptxt = glyph
        for rt, rb in runs:
            r = para.add_run(); r.text = rt; ptxt += rt
            r.font.name = FONT; r.font.size = Pt(size - (1 if lvl else 0)); r.font.bold = rb; r.font.color.rgb = color
        plain.append(("      " * lvl) + ptxt)
    _fit_check("\n".join(plain), w - 0.1, h - 0.1 - len(items) * gap / 72, size, name or "bullets")
    return shp


def rect(slide, x, y, w, h, fill, line=None):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid(); s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
    s.shadow.inherit = False
    return s


def hline(slide, x, y, w, color=RULE, weight=1.0):
    ln = slide.shapes.add_connector(1, Inches(x), Inches(y), Inches(x + w), Inches(y))
    ln.line.color.rgb = color; ln.line.width = Pt(weight)
    return ln


page = [0]


def new_slide(title, tracker=None, source=None):
    s = prs.slides.add_slide(BLANK)
    page[0] += 1
    if tracker:
        tb(s, 0.5, 0.22, 9, 0.3, tracker.upper(), size=9.5, bold=True, color=BLUE, name="tracker")
    tb(s, 0.5, 0.45, 12.3, 0.95, title, size=20, bold=True, color=INK, anchor=MSO_ANCHOR.TOP, name="TITLE")
    hline(s, 0.5, 1.42, 12.33, color=INK, weight=1.25)
    if source:
        tb(s, 0.5, 6.92, 11.6, 0.5, source, size=8.5, color=MUTED, name="source")
    tb(s, 12.33, 7.05, 0.5, 0.3, str(page[0]), size=9, color=MUTED, align=PP_ALIGN.RIGHT, name="pg")
    return s


def table(slide, x, y, w, h, rows, col_w, size=10.5, header_fill=NAVY, first_bold=True, highlight_row=None,
          row_h=None, align_cols=None):
    nr, nc = len(rows), len(rows[0])
    gt = slide.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(w), Inches(h))
    t = gt.table
    tblPr = gt._element.graphic.graphicData.tbl.tblPr
    # strip default style banding look
    tblPr.set("bandRow", "0"); tblPr.set("firstRow", "1")
    for j, cw in enumerate(col_w):
        t.columns[j].width = Inches(cw)
    for i in range(nr):
        if row_h:
            t.rows[i].height = Inches(row_h[i] if isinstance(row_h, list) else row_h)
        for j in range(nc):
            c = t.cell(i, j); val = rows[i][j]
            c.margin_left = c.margin_right = Inches(0.07); c.margin_top = c.margin_bottom = Inches(0.04)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = c.text_frame; tf.word_wrap = True
            runs = val if isinstance(val, list) else [(str(val), None)]
            p = tf.paragraphs[0]
            if align_cols and j in align_cols:
                p.alignment = align_cols[j]
            for rt, rb in runs:
                r = p.add_run(); r.text = rt
                r.font.name = FONT; r.font.size = Pt(size)
                if i == 0:
                    r.font.bold = True; r.font.color.rgb = WHITE
                else:
                    r.font.bold = (j == 0 and first_bold) if rb is None else rb
                    r.font.color.rgb = INK
            c.fill.solid()
            if i == 0:
                c.fill.fore_color.rgb = header_fill
            elif highlight_row is not None and i == highlight_row:
                c.fill.fore_color.rgb = PALE
            else:
                c.fill.fore_color.rgb = WHITE if i % 2 else RGBColor(0xF6, 0xF6, 0xF4)
    return gt


def style_chart(ch, legend=False, size=10):
    ch.font.name = FONT; ch.font.size = Pt(size); ch.font.color.rgb = INK2
    ch.has_legend = legend
    if legend:
        ch.legend.position = XL_LEGEND_POSITION.TOP; ch.legend.include_in_layout = False
        ch.legend.font.size = Pt(size); ch.legend.font.name = FONT
    va = ch.value_axis
    va.has_major_gridlines = True
    va.major_gridlines.format.line.color.rgb = RGBColor(0xEC, 0xEB, 0xE7)
    va.format.line.fill.background()
    va.tick_labels.font.size = Pt(size - 1); va.tick_labels.font.color.rgb = MUTED
    ca = ch.category_axis
    ca.format.line.color.rgb = GREY
    ca.tick_labels.font.size = Pt(size); ca.tick_labels.font.color.rgb = INK2
    ca.has_major_gridlines = False


def color_series(ser, rgb):
    ser.format.fill.solid(); ser.format.fill.fore_color.rgb = rgb
    ser.format.line.color.rgb = WHITE; ser.format.line.width = Pt(1.5)  # 2px surface gap


def label_series(ser, fmt, size=10, pos=XL_LABEL_POSITION.OUTSIDE_END, color=INK, bold=False):
    ser.data_labels.show_value = True
    ser.data_labels.number_format = fmt; ser.data_labels.number_format_is_linked = False
    ser.data_labels.font.size = Pt(size); ser.data_labels.font.name = FONT
    ser.data_labels.font.color.rgb = color; ser.data_labels.font.bold = bold
    try:
        ser.data_labels.position = pos
    except Exception:
        pass


def waterfall(slide, x, y, w, h, cats, steps, kinds, fmt='0.0', size=10, ymax=None, label_fmt=None, ymin=0):
    """kinds: 'total' | 'up' | 'down'. steps are magnitudes (positive). Segments too small to hold a label get
    their label placed just above the bar (on an invisible pad series) instead of overflowing the mark."""
    base, vis_tot, vis_up, vis_dn = [], [], [], []
    run = 0.0
    for v, k in zip(steps, kinds):
        if k == "total":
            base.append(0); vis_tot.append(v); vis_up.append(0); vis_dn.append(0); run = v
        elif k == "up":
            base.append(run); vis_tot.append(0); vis_up.append(v); vis_dn.append(0); run += v
        else:
            run -= v; base.append(run); vis_tot.append(0); vis_up.append(0); vis_dn.append(v)
    rng = (ymax or max(vis_tot) * 1.1) - ymin
    small = [k != "total" and v < 0.09 * rng for v, k in zip(steps, kinds)]
    pad = [0.06 * rng if sm else 0 for sm in small]
    cd = CategoryChartData(); cd.categories = cats
    cd.add_series("base", base); cd.add_series("Total", vis_tot); cd.add_series("Increase", vis_up)
    cd.add_series("Decrease", vis_dn); cd.add_series("lbl", pad)
    gf = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_STACKED, Inches(x), Inches(y), Inches(w), Inches(h), cd)
    ch = gf.chart; style_chart(ch, size=size)
    plot = ch.plots[0]; plot.gap_width = 45; plot.overlap = 100
    s0, s1, s2, s3, s4 = plot.series
    for inv in (s0, s4):
        inv.format.fill.background(); inv.format.line.fill.background()
    color_series(s1, NAVY); color_series(s2, BLUE); color_series(s3, ORANGE)
    fmtv = (label_fmt or "{:.1f}")
    for ser, vals in ((s1, vis_tot), (s2, vis_up), (s3, vis_dn)):
        for i, v in enumerate(vals):
            if not v:
                continue
            sign = "" if ser is s1 else ("+" if ser is s2 else "\u2013")
            target = s4 if small[i] else ser
            dl = target.points[i].data_label; dl.has_text_frame = True
            dl.text_frame.text = sign + fmtv.format(v)
            r = dl.text_frame.paragraphs[0].runs[0]
            r.font.size = Pt(size); r.font.bold = True; r.font.name = FONT
            if small[i]:
                r.font.color.rgb = INK; dl.position = XL_LABEL_POSITION.INSIDE_BASE
            elif ser is s1:
                r.font.color.rgb = WHITE; dl.position = XL_LABEL_POSITION.INSIDE_END
            else:
                r.font.color.rgb = WHITE; dl.position = XL_LABEL_POSITION.CENTER
    va = ch.value_axis
    va.minimum_scale = ymin
    if ymax:
        va.maximum_scale = ymax
    va.tick_labels.number_format = fmt; va.tick_labels.number_format_is_linked = False
    return ch


# =====================================================================================
# 1. Title
s = prs.slides.add_slide(BLANK); page[0] += 1
rect(s, 0, 0, W, H, NAVY)
tb(s, 0.8, 1.6, 11.5, 0.5, "PALISADE DOCS  |  2027 PRICING DECISION", size=13, bold=True, color=RGBColor(0x9E, 0xC5, 0xF4))
tb(s, 0.8, 2.2, 11.8, 1.9, "Raise prices in 2027 where customers are sticky, not where churn is rising",
   size=36, bold=True, color=WHITE, name="title-main")
tb(s, 0.8, 4.25, 11.5, 0.9, "Recommendation to CEO Ravi Menon and the leadership team for the December 2026 decision "
   "on the 2027 pricing plan", size=16, color=RGBColor(0xDD, 0xE8, 0xF8))
tb(s, 0.8, 6.4, 11.8, 0.6, "Prepared November 2026. Source: Palisade briefing pack, the only evidence used. All company "
   "data in the pack is synthetic benchmark data. $ figures are ARR unless stated otherwise.", size=10,
   color=RGBColor(0x9E, 0xC5, 0xF4))

# =====================================================================================
# 2. Executive summary
s = new_slide("Raise prices in 2027 in mid-market and enterprise only; hold SMB until a test supports it, and treat "
              "churn as a promotion-cohort problem",
              tracker="Executive summary",
              source="ARR = annual recurring revenue; NRR = net revenue retention; MM = mid-market. Base and stress cases "
                     "use different price-response assumptions (slide 10, appendix A1).")
rect(s, 0.5, 1.6, 12.33, 0.95, PALE)
tb(s, 0.65, 1.64, 12.05, 0.88,
   [[("Recommendation: ", True), ("from January 2027, raise mid-market and enterprise prices +10% at renewal (7% where "
     "enterprise contracts cap increases). Hold SMB list prices and test +8% in H1. This adds ", False),
     ("~$3.5M ARR ($2.4M stress case)", True), (", keeps NRR at ~113%, and leaves ~$1.5M of new-customer ARR "
     "needed to reach the +15% target, against $4.9M with no increase.", False)]],
   size=12.5, anchor=MSO_ANCHOR.MIDDLE, name="gov")
cols = [
    ("1", "Rising churn comes from the 2025 promotion cohort; the core base has not become more price-sensitive",
     ["Non-promotion SMB churn: 2.0% → 2.1% a month. Mid-market and enterprise are ~flat.",
      "The 2,100 promotion customers churn at ~4.9% a month. They explain ~1.0pp of the 1.1pp SMB rise.",
      "Price as the exit reason: 18% of non-promotion churners (19% last year) vs 52% of promotion churners.",
      "Onboarding helps (~$0.4M) but cannot halve SMB churn as Customer Success expects."]),
    ("2", "Pricing power sits in mid-market and enterprise (76% of ARR); SMB is exposed to Inkwell",
     ["MM/Ent: NRR 112–118%, churn ≤0.8% a month; customers stay for integrations and the audit trail.",
      "A +10% MM list test showed no significant effect on conversion (23.1% vs 23.6%).",
      "SMB: Inkwell is $9 against our $15, and SMB win rate where Inkwell competed fell from 51% to 38%.",
      "A +12% SMB increase is worth ~$1.25M at the 2023 price response, and ~$0 if sensitivity has doubled."]),
    ("3", "The CFO's 12% plan is worth ~$5.3M, not $10.3M; the segmented plan trades ~$1.8M of upside for less risk",
     ["Only 2027 renewals can be repriced, and caps apply: $10.3M falls to $7.6M before any churn reaction.",
      "After churn reaction: $5.3M base case, $2.7M stress case. Most of the gap is SMB.",
      "Segmented plan: $3.5M base, $2.4M stress, with no SMB downside and within the tested price level.",
      "The SMB test can add $0.3–0.7M from July if it passes the breakeven rules."]),
]
for i, (num, head, pts) in enumerate(cols):
    x = 0.5 + i * 4.18
    tb(s, x, 2.72, 0.42, 0.42, num, size=15, bold=True, color=WHITE, fill=BLUE, align=PP_ALIGN.CENTER,
       anchor=MSO_ANCHOR.MIDDLE)
    tb(s, x + 0.5, 2.66, 3.5, 1.05, head, size=12.5, bold=True, color=NAVY, name=f"es-head{i}")
    hline(s, x, 3.78, 3.97, color=RULE)
    bullets(s, x, 3.86, 3.97, 3.05, pts, size=11, gap=5, name=f"es-b{i}")

# =====================================================================================
# 3. Hypothesis and tests
s = new_slide("We began with ‘raise, but by segment’. The evidence confirmed segmenting, but cut the size, ruled "
              "out an SMB rise and downgraded onboarding",
              tracker="Approach: hypothesis and tests",
              source="Source: briefing pack sections 5–9; calculations on slides 4–12 and appendix.")
tb(s, 0.5, 1.52, 12.33, 0.6, [[("Initial hypothesis: ", True),
   ("raise ~12% in mid-market and enterprise, plus a smaller (5–8%) SMB rise once onboarding has brought SMB "
    "churn down. For that to hold, five things had to be true:", False)]], size=12, name="hyp")
rows = [["What would have to be true", "What the evidence shows", "Verdict", "Effect on the answer"],
        ["1. Rising churn sits in an identifiable group and is not price-driven in the core base",
         "Non-promotion SMB churn 2.0% → 2.1%; the promotion cohort is ~4.9%. Price as exit reason in the core "
         "base: 19% → 18%", "Holds", "Rising churn does not rule out a price rise outside the cohort"],
        ["2. Mid-market and enterprise accept an increase without material churn",
         "NRR 112–118%, low churn, sticky integrations. +10% tested with no significant effect; 12% untested; "
         "MM churn 0.6% → 0.8%", "Holds at 10%", "Size at the tested +10%, not 12%"],
        ["3. SMB can absorb an increase in 2027",
         "Core base looks stable, but Inkwell is $9 vs $15, win rate 51% → 38%, and the upside is ~$1.25M at the 2023 response",
         "Not shown", "Hold SMB list prices; run a test with a breakeven go/no-go rule"],
        ["4. The increase matters for the 15% growth target",
         "$3.5M, not $10.3M, but it cuts the new-customer ARR needed from $4.9M to $1.5M",
         "Holds (smaller)", "Worth doing; do not plan on $10.3M"],
        ["5. Onboarding can cut SMB churn quickly (‘halve it in two quarters’)",
         "Halving needs 1.55%, below the non-promotion level of 2.1%. The activation gap explains only ~0.8pp of the "
         "cohort's ~2.8pp excess churn", "Fails", "Fund it as a ~$0.4M lever, not as the churn cure"]]
gt = table(s, 0.5, 2.15, 12.33, 4.64, rows, [3.2, 4.85, 1.35, 2.93], size=10.5,
           row_h=[0.4, 0.86, 0.86, 0.86, 0.8, 0.86])
for i, v in enumerate(["Holds", "Holds at 10%", "Not shown", "Holds (smaller)", "Fails"], start=1):
    c = gt.table.cell(i, 2); r = c.text_frame.paragraphs[0].runs[0]; r.font.bold = True
    r.font.color.rgb = BLUE if v.startswith("Holds") else ORANGE

# =====================================================================================
# 4. Churn decomposition
s = new_slide("Without the 2025 promotion cohort, SMB churn barely moved (2.0% → 2.1% a month); the cohort "
              "accounts for almost all of the rise", tracker="1 │ Churn diagnosis",
              source="Source: briefing pack Table 1 and section 6. *Promotion-cohort rate derived: (5,900 × 3.1% "
                     "– 3,800 × 2.1%) ÷ 2,100. No H1 2025 value: the cohort joined Feb–Aug 2025. Uses mid-2026 counts; approximate.")
cd = CategoryChartData()
cd.categories = ["SMB, non-promotion", "SMB, promotion cohort*", "SMB, all", "Mid-market", "Enterprise"]
cd.add_series("H1 2025", (2.0, None, 2.0, 0.6, 0.2))
cd.add_series("H1 2026", (2.1, 4.9, 3.1, 0.8, 0.2))
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.5), Inches(1.75), Inches(7.6), Inches(5.0), cd)
ch = gf.chart; style_chart(ch, legend=True, size=11)
ch.plots[0].gap_width = 70; ch.plots[0].overlap = -6
color_series(ch.plots[0].series[0], GREY); color_series(ch.plots[0].series[1], BLUE)
for ser in ch.plots[0].series:
    label_series(ser, '0.0"%"', size=11)
ch.value_axis.maximum_scale = 6; ch.value_axis.minimum_scale = 0
ch.value_axis.tick_labels.number_format = '0"%"'; ch.value_axis.tick_labels.number_format_is_linked = False
tb(s, 0.55, 1.5, 7.5, 0.3, "Monthly logo churn by group, %", size=11, bold=True, color=INK2)
# right panel: the arithmetic
rect(s, 8.45, 1.6, 4.38, 5.2, RGBColor(0xF6, 0xF6, 0xF4))
tb(s, 8.6, 1.68, 4.1, 0.35, "The arithmetic, SMB in H1 2026", size=12, bold=True, color=NAVY)
calc = [["All SMB:  5,900 × 3.1%", "183 churners / mo"],
        ["Non-promotion:  3,800 × 2.1%", "80 churners / mo"],
        ["Promotion cohort:  183 – 80", "103 churners / mo"],
        ["Cohort rate:  103 ÷ 2,100", "≈ 4.9% / mo"]]
yy = 2.1
for a, b in calc:
    tb(s, 8.6, yy, 2.65, 0.34, a, size=11, color=INK, name="calc-a")
    tb(s, 10.95, yy, 1.8, 0.34, b, size=11, bold=True, color=INK, align=PP_ALIGN.RIGHT, name="calc-b")
    yy += 0.36
hline(s, 8.6, 3.6, 4.1)
bullets(s, 8.55, 3.7, 4.2, 3.05, [
    [("The cohort is 36% of SMB customers but ~56% of SMB churners", True)],
    "Of the 1.1pp SMB rise, ~1.0pp is the cohort's mix effect and ~0.1pp is the core base",
    "Cross-check: exit-survey shares (52% / 18% / 34% citing price) imply the cohort is ~47% of churners. "
    "The same direction, so the conclusion holds",
    "Mid-market rose 0.6% → 0.8%: small in absolute terms but unexplained. Diagnose before January notices"],
    size=10.5, gap=4, name="s4-b")

# =====================================================================================
# 5. Price complaints
s = new_slide("Price complaints rose only among promotion customers, who left as their 50% discount ended; the core "
              "SMB base cites price as before", tracker="1 │ Churn diagnosis",
              source="Source: briefing pack Table 2 and section 6. Share of churned customers who answered the exit "
                     "survey and gave ‘price / found a cheaper option’ as the main reason.")
cd = CategoryChartData()
cd.categories = ["All SMB churners\nH1 2025", "All SMB churners\nH1 2026", "Non-promotion\nchurners H1 2026",
                 "Promotion-cohort\nchurners H1 2026"]
cd.add_series("Share citing price", (19, 34, 18, 52))
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.5), Inches(1.8), Inches(7.4), Inches(4.95), cd)
ch = gf.chart; style_chart(ch, size=11); ch.plots[0].gap_width = 80
ser = ch.plots[0].series[0]; color_series(ser, GREY)
for i in (1, 3):
    p = ser.points[i]; p.format.fill.solid(); p.format.fill.fore_color.rgb = BLUE if i == 1 else ORANGE
label_series(ser, '0"%"', size=12, bold=True)
ch.value_axis.maximum_scale = 60; ch.value_axis.minimum_scale = 0
ch.value_axis.tick_labels.number_format = '0"%"'; ch.value_axis.tick_labels.number_format_is_linked = False
tb(s, 0.55, 1.52, 7.3, 0.3, "Churners citing price as main exit reason, %", size=11, bold=True, color=INK2)
rect(s, 8.25, 1.6, 4.58, 5.2, RGBColor(0xF6, 0xF6, 0xF4))
tb(s, 8.4, 1.68, 4.3, 0.35, "What sets the promotion cohort apart", size=12, bold=True, color=NAVY)
bullets(s, 8.35, 2.1, 4.4, 4.65, [
    [("A 100% price step. ", True), ("They paid half price for six months, then full price. Most who left did so "
     "within two months of the discount ending.", False)],
    [("Weaker activation. ", True), ("41% sent ≥5 documents in month one, against 72% of other cohorts.", False)],
    [("Smaller accounts. ", True), ("$2,095 ARR each, against $4,368 for other SMB customers ($4.4M ÷ 2,100 "
     "vs $16.6M ÷ 3,800).", False)],
    [("So the CFO and CEO are each half right. ", True), ("The core base is not churning on price. But the cohort "
     "shows that a sharp price step drives churn among customers who were never activated.", False)]],
    size=11, gap=7, name="s5-b")

# =====================================================================================
# 6. Activation vs onboarding claim
s = new_slide("Better onboarding can recover part of the promotion cohort, but it cannot halve SMB churn as "
              "Customer Success expects", tracker="1 │ Churn diagnosis",
              source="Source: briefing pack sections 6, 8, 9, 10. Model: churn among activated customers = a, among "
                     "non-activated = 3a; non-promotion mix 72/28 at 2.1% gives a = 1.35%. Cohort mix 41/59 gives 2.9%.")
ch = waterfall(s, 0.5, 1.85, 6.9, 4.9,
               ["Non-promotion\nSMB rate", "Activation gap\n(41% vs 72%)", "Discount-end shock\nand other",
                "Promotion\ncohort rate"],
               [2.1, 0.83, 1.97, 4.9], ["total", "up", "up", "total"], fmt='0"%"', size=11, ymax=6,
               label_fmt="{:.1f}%")
tb(s, 0.55, 1.52, 6.8, 0.3, "Promotion-cohort monthly churn, decomposed, %", size=11, bold=True, color=INK2)
rect(s, 7.7, 1.6, 5.13, 2.45, PALEOR)
tb(s, 7.85, 1.68, 4.85, 0.35, "The ‘halve SMB churn’ claim does not hold", size=12, bold=True, color=NAVY)
bullets(s, 7.8, 2.06, 4.95, 1.98, [
    "Halving takes SMB from 3.1% to 1.55%, below the 2.1% non-promotion level and below every SMB rate in the pack "
    "since 2023 (1.8–3.1%)",
    "Best case, with the cohort behaving like everyone else: 2.1%, a 32% cut, not 50%",
    "Activation explains only ~0.8pp of the cohort's 2.8pp excess churn"], size=10.5, gap=3, name="s6-a")
rect(s, 7.7, 4.2, 5.13, 2.6, PALE)
tb(s, 7.85, 4.28, 4.85, 0.35, "What onboarding is realistically worth", size=12, bold=True, color=NAVY)
bullets(s, 7.8, 4.66, 4.95, 2.12, [
    "Lifting cohort activation from 41% to 72% removes ~0.83pp of monthly churn: 2,100 × 0.83% × 12 "
    "≈ 210 customers a year × $2,095 ≈ $0.4M ARR",
    "Worth funding. It also protects every future SMB cohort (customers below 5 documents churn ~3× as often)",
    "Do not count it toward 2027 churn targets until H1 results are in"], size=10.5, gap=3, name="s6-b")

# =====================================================================================
# 7. Metric definition
s = new_slide("Revenue-weighted churn is only ~1.2% a month, and the board's ‘1.4% → 2.3%’ cannot be "
              "reproduced; churn reporting needs a defined measure", tracker="1 │ Churn diagnosis",
              source="Source: briefing pack Table 1 and section 10. Weighted averages of segment monthly logo churn, "
                     "using mid-2026 customer counts and ARR as weights.")
rows = [["Measure", "H1 2025", "H1 2026", "Change", "How calculated"],
        ["Board dashboard (undefined)", "1.4%", "2.3%", "+0.9pp", "Not reproducible from segment data"],
        ["Customer-weighted, all customers", "1.7%", "2.6%", "+0.9pp", "Σ(customers × churn) ÷ 7,400"],
        ["Customer-weighted, excluding promotion cohort", "1.6%", "1.7%", "+0.1pp",
         "Non-promotion SMB 3,800 at 2.0% / 2.1%, plus MM and Ent ÷ 5,300"],
        ["ARR-weighted, all customers", "0.8%", "1.2%", "+0.4pp", "Σ(ARR × churn) ÷ $86.0M"]]
table(s, 0.5, 1.75, 12.33, 2.6, rows, [3.9, 1.2, 1.2, 1.2, 4.83], size=11.5, row_h=0.52,
      align_cols={1: PP_ALIGN.CENTER, 2: PP_ALIGN.CENTER, 3: PP_ALIGN.CENTER}, highlight_row=3)
bullets(s, 0.5, 4.6, 12.3, 2.2, [
    [("Logo churn overstates revenue risk. ", True), ("SMB is 80% of customers but 24% of ARR. The segments holding "
     "76% of ARR have NRR above 110%; company NRR is 109.3% (ARR-weighted 94% / 112% / 118%).", False)],
    [("The headline mixes a one-off cohort into the trend. ", True), ("Without the promotion cohort, company churn moved "
     "0.1pp, not 0.9pp.", False)],
    [("Proposed standard for board reporting: ", True), ("monthly logo and ARR churn by segment, with acquisition "
     "cohorts (including promotions) shown separately.", False)]], size=12, gap=8, name="s7-b")

# =====================================================================================
# 8. MM/Ent pricing power
s = new_slide("Mid-market and enterprise, 76% of ARR, show strong signs of pricing power, with two caveats to "
              "manage", tracker="2 │ Where pricing power is",
              source="Source: briefing pack Table 1, sections 7–9. ARR per customer = segment ARR ÷ customers.")
rows = [["Signal", "Mid-market (51–1,000 staff)", "Enterprise (>1,000 staff)", "Read-across"],
        ["ARR / customers", "$41.0M / 1,350 ($30k each)", "$24.0M / 150 ($160k each)", "76% of company ARR"],
        ["Monthly logo churn, H1 25 → H1 26", "0.6% → 0.8%", "0.2% → 0.2%",
         "Low; MM drift needs a diagnosis"],
        ["Net revenue retention (TTM)", "112%", "118%", "Customers are expanding, not leaving"],
        ["Price test", "+10% list for new sign-ups: 23.1% vs 23.6% conversion (not significant)", "None",
         "+10% is the evidence-backed level"],
        ["Competitive exposure", "Inkwell not seen in deals >200 seats", "Inkwell not seen", "Exposure only at the "
         "small end of MM"],
        ["Why customers stay", "Integrations and audit trail (advisory board)", "Same", "Value is not about price"],
        ["2027 repricing scope", "85% of ARR renews in 2027", "40% renews; 60% of ARR capped at 7%/yr",
         "Limits the in-year ARR effect"]]
table(s, 0.5, 1.65, 12.33, 4.2, rows, [2.75, 3.65, 3.0, 2.93], size=10.5, row_h=0.5)
rect(s, 0.5, 6.0, 12.33, 0.85, PALEOR)
tb(s, 0.65, 6.04, 12.05, 0.78, [[("Caveats: ", True),
   ("(1) the test measured new sign-ups, not renewals. Existing customers have switching costs, so they are probably "
    "less sensitive, but this is unproven; the stress case assumes SMB-level sensitivity. (2) The MM churn rise "
    "(0.6% → 0.8%) is unexplained and must be diagnosed before renewal notices go out.", False)]],
   size=11, anchor=MSO_ANCHOR.MIDDLE, name="s8-cav")

# =====================================================================================
# 9. SMB exposure
s = new_slide("In SMB, Inkwell has opened a large price gap and cut our win rate; a 12% rise would widen it for "
              "~$1.25M of upside, or ~$0 if sensitivity has doubled", tracker="2 │ Where pricing power is",
              source="Source: briefing pack sections 7–8. 2023 response: +0.5pp for 6 months + 0.1pp for 6 months "
                     "= 3.6% extra customers lost in year one for +8%, i.e. 0.45pp per 1% of price.")
cd = CategoryChartData()
cd.categories = ["Inkwell Starter", "Palisade SMB", "Inkwell Pro", "Palisade Business"]
cd.add_series("Today", (9, 15, 24, 29))
cd.add_series("Palisade after +12%", (None, 16.8, None, 32.48))
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.5), Inches(1.8), Inches(6.4), Inches(4.95), cd)
ch = gf.chart; style_chart(ch, legend=True, size=11); ch.plots[0].gap_width = 60; ch.plots[0].overlap = -6
s0, s1 = ch.plots[0].series; color_series(s0, BLUE); color_series(s1, ORANGE)
for i in (0, 2):
    p = s0.points[i]; p.format.fill.solid(); p.format.fill.fore_color.rgb = GREY
label_series(s0, '"$"0', size=11); label_series(s1, '"$"0.00', size=11)
ch.value_axis.minimum_scale = 0; ch.value_axis.maximum_scale = 36
ch.value_axis.tick_labels.number_format = '"$"0'; ch.value_axis.tick_labels.number_format_is_linked = False
tb(s, 0.55, 1.52, 6.3, 0.3, "List price, $ per user per month (Inkwell in grey)", size=11, bold=True, color=INK2)
rect(s, 7.2, 1.6, 5.63, 5.2, RGBColor(0xF6, 0xF6, 0xF4))
stats = [("51% → 38%", "SMB win rate where Inkwell competed, H1 2025 → H1 2026"),
         ("+67% → +87%", "Our SMB premium over Inkwell Starter today vs after +12%"),
         ("$1.25M", "What a +12% SMB increase adds at the 2023 price response: $21.0M × (1.12 × 0.946 – 1)"),
         ("~$0", "Same increase if Inkwell has doubled price sensitivity: $21.0M × (1.12 × 0.892 – 1)"),
         ("~290", "Lost new SMB wins that would erase the $1.25M ($1.25M ÷ $4,368). SMB already loses ~2,200 "
                  "customers a year to churn")]
yy = 1.72
for big, small in stats:
    tb(s, 7.32, yy, 2.0, 0.8, big, size=17, bold=True, color=NAVY, anchor=MSO_ANCHOR.MIDDLE, name="stat-big")
    tb(s, 9.35, yy, 3.4, 0.8, small, size=10.5, color=INK, anchor=MSO_ANCHOR.MIDDLE, name="stat-small")
    yy += 0.86
tb(s, 7.32, 6.05, 5.4, 0.7, "Breakeven: a +12% rise pays only if extra churn stays below 10.7% of the base (1.12 "
   "× (1 – c) = 1), about 2× the 2023 response, before counting any lost new customers.",
   size=10, color=INK2, italic=True, name="s9-be")

# =====================================================================================
# 10. CFO walk
s = new_slide("The CFO's ‘$10.3M’ is worth ~$5.3M of ARR (base) and ~$2.7M (stress): many contracts cannot be "
              "repriced in 2027 and some customers will leave",
              tracker="3 │ Sizing the options",
              source="Base: SMB 2023 response (0.45pp extra loss per 1%); MM response from the 2024 test (2.1% relative "
                     "loss per 10%); enterprise none. Stress: SMB 2× 2023, MM at the SMB 2023 rate, enterprise "
                     "at the MM test rate. Caps assumed pro rata across renewing enterprise ARR. Totals may not add due to rounding.")
ch = waterfall(s, 0.5, 1.8, 8.4, 5.0,
               ["CFO claim\n12% × $86.0M", "MM ARR not\nrenewing (15%)", "Ent ARR not\nrenewing (60%)",
                "Ent 7% caps", "Repriceable\nin 2027", "SMB churn\nreaction", "MM churn\nreaction", "Base case",
                "Extra loss\nin stress", "Stress case"],
               [10.32, 0.74, 1.73, 0.29, 7.57, 1.27, 0.99, 5.30, 2.59, 2.72],
               ["total", "down", "down", "down", "total", "down", "down", "total", "down", "total"],
               fmt='"$"0"M"', size=10, ymax=11, label_fmt="{:.1f}")
tb(s, 0.55, 1.52, 8.3, 0.3, "ARR added by a 12% increase on every plan, $M (exit-2027 run rate)", size=11, bold=True,
   color=INK2)
rect(s, 9.15, 1.6, 3.68, 5.2, RGBColor(0xF6, 0xF6, 0xF4))
tb(s, 9.3, 1.68, 3.4, 0.35, "How the base case breaks down", size=12, bold=True, color=NAVY)
rows = [["Segment", "Gross", "Base", "Stress"], ["SMB", "2.52", "1.25", "–0.02"], ["Mid-market", "4.18", "3.19", "2.07"],
        ["Enterprise", "0.86", "0.86", "0.66"], ["Total", "7.57", "5.30", "2.72"]]
table(s, 9.3, 2.1, 3.4, 2.2, rows, [1.25, 0.7, 0.7, 0.75], size=10.5, row_h=0.42,
      align_cols={1: PP_ALIGN.RIGHT, 2: PP_ALIGN.RIGHT, 3: PP_ALIGN.RIGHT})
bullets(s, 9.25, 4.5, 3.5, 2.3, [
    "Net = renewing ARR × [(1 + price) × (1 – extra loss) – 1]",
    "SMB carries 24% of gross but most of the uncertainty: $1.25M to ~$0",
    "In-year 2027 revenue is roughly half of these figures, because renewals are spread across the year"],
    size=10, gap=4, name="s10-b")

# =====================================================================================
# 11. Options
s = new_slide("A segmented +10% gives up ~$1.8M of base-case ARR against the CFO plan, but removes the SMB "
              "downside and stays within the tested price level", tracker="3 │ Sizing the options",
              source="$M ARR added by end-2027 versus no change. New-customer ARR needed = $98.9M target – $94.0M "
                     "existing base at today's NRR – price uplift. Assumptions on slide 14, model in appendix A1.")
rows = [["Option", "SMB", "Mid-market", "Enterprise", "ARR added:\nbase / stress", "NRR\n(base)",
         "New-customer ARR needed for +15%", "Main trade-off"],
        ["A. No increase", "–", "–", "–", "0 / 0", "109%", "$4.9M",
         "No churn risk, but leaves proven MM/Ent pricing power unused"],
        ["B. CFO: +12% on every plan", "+12%", "+12%", "+12% (7% capped)", "5.3 / 2.7", "115%", "$0 / $2.2M",
         "Most upside, but the SMB part ranges from $1.25M to ~$0, widens the Inkwell gap and hits the fragile cohort"],
        [[("C. Recommended: segmented", True)], "Hold; test +8%", "+10%", "+10% (7% capped)", "3.5 / 2.4", "113%",
         "$1.5M / $2.6M", "Gives up $1.8M base vs B; tested price level; no SMB downside. SMB test can add $0.3–0.7M"],
        ["D. Segmented at 12%", "Hold", "+12%", "+12% (7% capped)", "4.1 / 2.7", "114%", "$0.9M / $2.2M",
         "+$0.6M vs C, but 12% has never been tested and MM churn is drifting up"]]
gt = table(s, 0.5, 1.65, 12.33, 4.3, rows, [2.0, 1.15, 1.0, 1.35, 1.2, 0.8, 1.6, 3.23], size=10,
           row_h=[0.6, 0.75, 1.0, 1.0, 0.85], highlight_row=3,
           align_cols={1: PP_ALIGN.CENTER, 2: PP_ALIGN.CENTER, 3: PP_ALIGN.CENTER, 4: PP_ALIGN.CENTER,
                       5: PP_ALIGN.CENTER, 6: PP_ALIGN.CENTER})
rect(s, 0.5, 6.05, 12.33, 0.85, PALE)
tb(s, 0.65, 6.07, 12.05, 0.8, [[("Why C over B and D: ", True),
   ("the extra ARR in B comes from the segment where churn is rising, a competitor is winning on price, and our "
    "own data cannot size the response. D's extra $0.6M rests on an untested price point. C meets the NRR objective in "
    "both cases and needs only $1.5–2.6M of new-customer ARR. Leadership could choose D for >200-seat accounts, where Inkwell is absent.", False)]],
   size=11, anchor=MSO_ANCHOR.MIDDLE, name="s11-why")

# =====================================================================================
# 12. Bridge to target
s = new_slide("With the recommended plan, reaching +15% ARR needs ~$1.5M of new-customer ARR, against $4.9M with no "
              "increase, and NRR stays well above 100%", tracker="3 │ Sizing the options",
              source="Existing-base growth assumes 2027 segment NRR equals trailing-12-month NRR (SMB 94%, MM 112%, "
                     "Ent 118%). New-customer bookings are not in the briefing pack and must be checked against the "
                     "2027 sales plan.")
ch = waterfall(s, 0.5, 1.8, 7.8, 5.0,
               ["ARR today", "Existing base\nat today's NRR", "Price: MM/Ent\n+10%", "New customers\nneeded",
                "2027 target\n(+15%)"],
               [86.0, 7.98, 3.46, 1.46, 98.9], ["total", "up", "up", "up", "total"], fmt='"$"0"M"', size=11,
               ymax=105, label_fmt="{:.1f}", ymin=70)
tb(s, 0.55, 1.52, 7.7, 0.3, "2027 ARR bridge, recommended plan, base case, $M (axis starts at $70M)", size=11, bold=True,
   color=INK2)
rect(s, 8.6, 1.6, 4.23, 5.2, RGBColor(0xF6, 0xF6, 0xF4))
tb(s, 8.75, 1.68, 3.95, 0.35, "Against the two objectives", size=12, bold=True, color=NAVY)
rows = [["", "Base", "Stress"], ["Price uplift", "$3.5M", "$2.4M"], ["Existing-base NRR", "113%", "112%"],
        ["New-customer ARR needed", "$1.5M", "$2.6M"], ["SMB NRR (unchanged)", "94%", "94%"]]
table(s, 8.75, 2.1, 3.95, 2.15, rows, [2.15, 0.9, 0.9], size=10.5, row_h=0.42,
      align_cols={1: PP_ALIGN.RIGHT, 2: PP_ALIGN.RIGHT})
bullets(s, 8.7, 4.4, 4.05, 2.4, [
    "NRR > 100% holds in every option and case; the binding objective is ARR growth",
    "Each 1pp shortfall in baseline NRR adds ~$0.86M to the new-customer need",
    "SMB NRR stays below 100%; fixing it is a retention and activation job, not a pricing one"],
    size=10.5, gap=4, name="s12-b")

# =====================================================================================
# 13. How: the plan
s = new_slide("Four moves, sequenced so that the 2027 SMB pricing decision is made on evidence by July",
              tracker="4 │ How to do it",
              source="Breakeven rules: +8% price is revenue-neutral if conversion falls 7.4% (1 – 1/1.08) and if "
                     "extra churn among existing customers reaches 7.4% of the base (~2× the 2023 response).")
rows = [["Move", "What exactly", "When", "Lead", "Success measure / decision rule"],
        ["1. Raise MM and Ent prices +10% at renewal",
         "+10% at each 2027 renewal (85% of MM ARR, 40% of Ent ARR). 7% where contracts cap it. Account teams may go to "
         "+5% for accounts actively evaluating a competitor; exceptions logged",
         "Notices from Jan 2027", "CRO / CS",
         "≥$2.4M ARR added by Dec 2027; MM churn ≤ 0.8%/mo; NRR ≥ 112%"],
        ["2. Hold SMB list prices; test +8%",
         "Randomised +8% test on new self-serve sign-ups (Q1–Q2). Track conversion and Inkwell win rate. "
         "Promotion cohort exempt from any 2027 increase",
         "Test Feb–May; decide June", "CPO / Growth",
         "Go to +8% for SMB from July if conversion falls < 7% relative and win rate holds. "
         "Worth $0.3–0.7M"],
        ["3. Activate the promotion cohort and new SMB customers",
         "Targeted onboarding for ~1,240 non-activated cohort customers (59% of 2,100); ≥5 documents in month one "
         "as the standard target for every SMB sign-up",
         "Start Jan; review Q2", "CS",
         "Cohort activation 41% → 72%; cohort churn 4.9% → ~4.1%/mo (≈ $0.4M ARR)"],
        ["4. Fix churn measurement", "Board reporting: logo and ARR churn by segment, with cohorts (incl. promotions) "
         "shown separately; define the dashboard measure",
         "Jan board pack", "CFO",
         "One agreed definition; promotion effects visible, not blended in"]]
table(s, 0.5, 1.65, 12.33, 5.2, rows, [2.35, 4.1, 1.45, 1.05, 3.38], size=10.5,
      row_h=[0.42, 1.2, 1.25, 1.2, 1.0])

# =====================================================================================
# 14. Risks
s = new_slide("The recommendation holds under the main risks, and Palisade's own data can narrow the largest "
              "uncertainties before December", tracker="5 │ Risks and assumptions",
              source="Sensitivities computed with the appendix A1 model.")
rows = [["Assumption or risk", "What we assumed", "If wrong", "Mitigation / what to check"],
        ["MM renewals react like new sign-ups", "2.1% extra ARR loss per +10% (from 2024 test)",
         "At SMB-like sensitivity, uplift falls $3.5M → $2.4M; NRR still 112%; new-customer need rises to $2.6M",
         "Analyse 2023/24 renewal outcomes; CS-led renewal calls"],
        ["2027 NRR equals trailing NRR (109.3%)", "SMB 94%, MM 112%, Ent 118% repeat",
         "Each 1pp lower = $0.86M more new-customer ARR needed",
         "Pull H2 2026 NRR; it may improve as the cohort shock fades"],
        ["New-customer ARR of ≥$1.5–2.6M", "Not in the pack", "If bookings fall short, +15% is missed in "
         "any option except B's base case", "Reconcile with the 2027 sales plan before sign-off"],
        ["Promotion cohort churn persists at ~4.9%/mo", "Built into SMB NRR of 94%",
         "Upside if it is fading: most leavers went within 2 months of discount end", "Pull Jul–Oct 2026 cohort churn now"],
        ["Inkwell moves above 200 seats", "Not seen in larger deals", "MM uplift and NRR at risk",
         "Track competitor presence in MM renewals monthly"],
        ["Price response is linear; caps apply pro rata", "Scaled from +8% / +10% evidence",
         "Above-tested prices may react non-linearly; if all renewing Ent ARR is capped, –$0.1M",
         "Stay at the tested +10%; confirm cap schedule by contract"]]
table(s, 0.5, 1.65, 12.33, 5.2, rows, [2.75, 2.75, 3.6, 3.23], size=10.5,
      row_h=[0.42, 0.8, 0.8, 0.8, 0.8, 0.7, 0.8])

# =====================================================================================
# 15. Decisions & next steps
s = new_slide("Four decisions for the December leadership meeting, and three data checks to run first",
              tracker="Decisions requested", source="Owners are suggestions for leadership to confirm.")
tb(s, 0.5, 1.6, 7.2, 0.35, "Decisions requested", size=13, bold=True, color=NAVY)
decs = [("1", "Approve +10% at renewal for mid-market and enterprise from January 2027 (7% where contracts cap it)."),
        ("2", "Reject the uniform 12%. Hold SMB list prices and approve the +8% sign-up test with the July go/no-go "
              "rule."),
        ("3", "Fund targeted onboarding for the promotion cohort and new SMB customers. Plan on ~$0.4M of value, "
              "not a halving of churn."),
        ("4", "Adopt a defined churn measure (segment × cohort, logo and ARR) for board reporting from "
              "January.")]
yy = 2.05
for n, t in decs:
    tb(s, 0.5, yy, 0.42, 0.42, n, size=14, bold=True, color=WHITE, fill=BLUE, align=PP_ALIGN.CENTER,
       anchor=MSO_ANCHOR.MIDDLE)
    tb(s, 1.05, yy - 0.04, 6.6, 0.95, t, size=12, color=INK, name="dec")
    yy += 1.05
rect(s, 8.0, 1.6, 4.83, 5.2, RGBColor(0xF6, 0xF6, 0xF4))
tb(s, 8.15, 1.68, 4.55, 0.35, "Before the meeting (2–3 weeks)", size=13, bold=True, color=NAVY)
bullets(s, 8.1, 2.15, 4.65, 4.6, [
    [("Promotion cohort, Jul–Oct 2026: ", True), ("is churn fading now the discount has ended? This tells us "
     "whether the 2026 spike is one-off.", False)],
    [("Mid-market churn drivers: ", True), ("why did churn rise from 0.6% to 0.8%? Is it concentrated in "
     "≤200-seat accounts where Inkwell competes?", False)],
    [("2027 new-business plan: ", True), ("confirm that ≥$1.5M (base) to $2.6M (stress) of new-customer ARR "
     "is realistic, given the lower SMB win rate.", False)]],
    size=11.5, gap=10, name="s15-b")

# =====================================================================================
# A1. Model
s = new_slide("Appendix A1: the pricing model, segment by segment", tracker="Appendix",
              source="Inputs: briefing pack Table 1 and section 8. Net = renewing ARR × [(1 + p)(1 – e·p) "
                     "– 1], where e = extra share of ARR lost per 1 point of price. All $M ARR.")
rows = [["Segment", "ARR", "Renews in 2027", "Repriceable ARR", "Price (B / C)", "e base", "e stress",
         "B base / stress", "C base / stress"],
        ["SMB", "21.0", "100%", "21.0", "12% / 0%", "0.45pp (2023)", "0.90pp (2×)", "1.25 / –0.02", "0 / 0"],
        ["Mid-market", "41.0", "85%", "34.85", "12% / 10%", "0.21pp (2024 test)", "0.45pp", "3.19 / 2.07",
         "2.67 / 1.76"],
        ["Enterprise capped (60%)", "24.0", "40%", "5.76", "7% / 7%", "0", "0.21pp", "0.40 / 0.31", "0.40 / 0.31"],
        ["Enterprise uncapped (40%)", "", "", "3.84", "12% / 10%", "0", "0.21pp", "0.46 / 0.35", "0.38 / 0.29"],
        [[("Total", True)], "86.0", "", "65.45", "", "", "", [("5.30 / 2.72", True)], [("3.46 / 2.37", True)]]]
table(s, 0.5, 1.65, 12.33, 3.2, rows, [2.25, 0.7, 1.15, 1.35, 1.25, 1.5, 1.25, 1.45, 1.43], size=10.5, row_h=0.5,
      align_cols={i: PP_ALIGN.CENTER for i in range(1, 9)})
bullets(s, 0.5, 5.05, 12.3, 1.85, [
    "2023 SMB response: +8% raised churn 1.8% → 2.3% for 6 months, then 1.9%: (0.5 × 6 + 0.1 × 6) ÷ 8 "
    "= 0.45pp of customers lost per 1% of price in year one",
    "2024 MM test: conversion 23.1% vs 23.6% = 2.1% relative drop for +10%, i.e. 0.21pp per 1%, used as a proxy for "
    "renewal loss",
    "Existing base at today's NRR: 21.0 × 0.94 + 41.0 × 1.12 + 24.0 × 1.18 = $94.0M; target 86.0 × "
    "1.15 = $98.9M; gap $4.9M before pricing",
    "SMB H2 test upside: $16.6M non-promotion ARR × [(1.08 × (1 – 3.6%)) – 1] = $0.68M if all repriced "
    "by year-end, $0.34M if half"], size=10.5, gap=3, name="a1-b")

# =====================================================================================
# A2. Churn math
s = new_slide("Appendix A2: churn decomposition and activation model", tracker="Appendix",
              source="Inputs: briefing pack Table 1, Table 2, sections 6 and 9. Mid-2026 customer counts used "
                     "throughout; H1 averages are approximate.")
rows = [["Step", "Calculation", "Result"],
        ["SMB churners per month, H1 2026", "5,900 × 3.1%", "182.9"],
        ["Non-promotion churners", "3,800 × 2.1%", "79.8"],
        ["Promotion-cohort churners and rate", "182.9 – 79.8 = 103.1; ÷ 2,100", "4.9% / month"],
        ["Contribution to SMB rise (1.1pp)", "Core: 3,800/5,900 × 0.1pp; cohort: 2,100/5,900 × (4.9 – 2.0)",
         "0.06pp / 1.04pp"],
        ["Survey cross-check", "52%·s + 18%·(1 – s) = 34% → s", "47% of churners (vs 56%)"],
        ["Activated / non-activated churn", "0.72a + 0.28 × 3a = 2.1% → a", "1.35% / 4.04%"],
        ["Cohort churn explained by activation", "0.41a + 0.59 × 3a", "2.93% (vs 4.9% actual)"],
        ["Onboarding value", "2,100 × 0.83pp × 12 × $2,095", "~210 customers, ~$0.44M"],
        ["Board metric reconciliation", "Customer-weighted 1.7% → 2.6%; ARR-weighted 0.8% → 1.2%",
         "Neither matches 1.4% → 2.3%"]]
table(s, 0.5, 1.65, 12.33, 5.1, rows, [3.6, 5.6, 3.13], size=11, row_h=0.5,
      align_cols={2: PP_ALIGN.RIGHT})

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Palisade_2027_Pricing_Decision.pptx")
prs.save(out)
print("saved", out, "slides:", len(prs.slides))
for w in FIT_WARN:
    print("FIT?", w)
