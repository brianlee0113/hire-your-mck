"""Build the Pelican Packaging IC deck. All figures trace to evidence/briefing-pack.md (see calc.py)."""
import math, sys
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.dml import MSO_LINE_DASH_STYLE

OUT = sys.argv[1] if len(sys.argv) > 1 else "deck.pptx"

NAVY = RGBColor(0x0B, 0x25, 0x45)
INK = RGBColor(0x1F, 0x1F, 0x1E)
GRAY = RGBColor(0x52, 0x51, 0x4E)
MUTED = RGBColor(0x8A, 0x89, 0x84)
RULE = RGBColor(0xD9, 0xD8, 0xD3)
PANEL = RGBColor(0xF3, 0xF3, 0xF1)
BLUE = RGBColor(0x2A, 0x78, 0xD6)
BLUE_L = RGBColor(0xB7, 0xD3, 0xF6)
ORANGE = RGBColor(0xEB, 0x68, 0x34)
AQUA = RGBColor(0x1B, 0xAF, 0x7A)
GOOD = RGBColor(0x00, 0x83, 0x00)
WARN = RGBColor(0xB8, 0x7A, 0x00)
BAD = RGBColor(0xC8, 0x2E, 0x2D)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
FONT = "Arial"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
WARNINGS = []
slide_no = [0]


# ---------- text fit estimator (Arial avg glyph ~0.5em) ----------
def est_lines(text, size, width_in):
    cpl = max(1, int(width_in * 72 / (size * 0.5)))
    n = 0
    for para in text.split("\n"):
        words, line, cnt = para.split(" "), 0, 1
        for w in words:
            if line + len(w) + (1 if line else 0) > cpl:
                cnt += 1
                line = len(w)
            else:
                line += len(w) + (1 if line else 0)
        n += cnt
    return n


def check_fit(label, paras, w, h, inset=0.1):
    tot = 0
    for p in paras:
        tot += est_lines(p["t"], p["size"], w - 2 * inset - (0.2 if p.get("bullet") else 0)) * p["size"] * 1.18 / 72
        tot += p.get("space", 0) / 72
    if tot > h - 2 * 0.05 + 0.02:
        WARNINGS.append(f"slide {slide_no[0]}: '{label[:40]}' needs {tot:.2f}in > box {h:.2f}in")


def P(t, size=12, bold=False, color=INK, bullet=False, space=0, align=None, italic=False):
    return dict(t=t, size=size, bold=bold, color=color, bullet=bullet, space=space, align=align, italic=italic)


def text(slide, x, y, w, h, paras, anchor=MSO_ANCHOR.TOP, fill=None, line=None, inset=0.1, check=True):
    if isinstance(paras, str):
        paras = [P(paras)]
    shp = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)) if fill is None and line is None \
        else slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is not None or line is not None:
        shp.shadow.inherit = False
        if fill is not None:
            shp.fill.solid(); shp.fill.fore_color.rgb = fill
        else:
            shp.fill.background()
        if line is not None:
            shp.line.color.rgb = line; shp.line.width = Pt(0.75)
        else:
            shp.line.fill.background()
    tf = shp.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(inset)
    tf.margin_top = tf.margin_bottom = Inches(0.05)
    for i, p in enumerate(paras):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        run = para.add_run()
        run.text = ("•  " if p["bullet"] else "") + p["t"]
        f = run.font
        f.name = FONT; f.size = Pt(p["size"]); f.bold = p["bold"]; f.italic = p["italic"]; f.color.rgb = p["color"]
        if p["space"]:
            para.space_before = Pt(p["space"])
        para.alignment = p["align"] if p["align"] is not None else PP_ALIGN.LEFT
    if check:
        check_fit(paras[0]["t"], paras, w, h, inset)
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


def hline(slide, x1, y, x2, color=RULE, width=0.75, dash=None):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y), Inches(x2), Inches(y))
    c.line.color.rgb = color; c.line.width = Pt(width)
    if dash:
        c.line.dash_style = dash
    return c


def vline(slide, x, y1, y2, color=RULE, width=0.75):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x), Inches(y1), Inches(x), Inches(y2))
    c.line.color.rgb = color; c.line.width = Pt(width)
    return c


def new_slide(title, section=None, source=None):
    slide_no[0] += 1
    s = prs.slides.add_slide(BLANK)
    if section:
        text(s, 0.5, 0.22, 9, 0.3, [P(section.upper(), 9, True, BLUE)], check=False)
    text(s, 0.5, 0.45, 12.3, 0.95, [P(title, 21, True, NAVY)], anchor=MSO_ANCHOR.TOP)
    hline(s, 0.6, 1.42, 12.83, NAVY, 1.0)
    if source:
        text(s, 0.5, 6.95, 11.0, 0.4, [P(source, 8.5, color=MUTED)], check=True)
    text(s, 12.2, 7.0, 0.7, 0.3, [P(str(slide_no[0]), 9, color=MUTED, align=PP_ALIGN.RIGHT)], check=False)
    return s


def table(slide, x, y, col_w, rows, header_size=10.5, body_size=10.5, row_h=None, header_fill=NAVY,
          first_col_bold=True, fills=None, label="table", max_h=None):
    """rows[0] is header. cells may be str or (str, RGBColor) for colored bold text."""
    nrows, ncols = len(rows), len(col_w)
    heights = []
    for r_i, row in enumerate(rows):
        size = header_size if r_i == 0 else body_size
        hmax = 0
        for c_i, cell in enumerate(row):
            t = cell[0] if isinstance(cell, tuple) else cell
            lines = est_lines(t, size, col_w[c_i] - 0.16)
            hmax = max(hmax, lines * size * 1.2 / 72 + 0.12)
        heights.append(max(hmax, row_h or 0))
    total = sum(heights)
    if max_h and total > max_h:
        WARNINGS.append(f"slide {slide_no[0]}: table '{label}' est {total:.2f}in > {max_h:.2f}in")
    shp = slide.shapes.add_table(nrows, ncols, Inches(x), Inches(y), Inches(sum(col_w)), Inches(total))
    tbl = shp.table
    tblPr = shp._element.graphic.graphicData.tbl
    # remove default style banding look
    tbl.first_row = True; tbl.horz_banding = False
    for i, w in enumerate(col_w):
        tbl.columns[i].width = Inches(w)
    for r_i, row in enumerate(rows):
        tbl.rows[r_i].height = Inches(heights[r_i])
        for c_i, cell in enumerate(row):
            c = tbl.cell(r_i, c_i)
            t, col, bold = (cell[0], cell[1], True) if isinstance(cell, tuple) else (cell, None, False)
            c.margin_left = c.margin_right = Inches(0.08)
            c.margin_top = c.margin_bottom = Inches(0.04)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = c.text_frame; tf.word_wrap = True
            para = tf.paragraphs[0]
            run = para.add_run(); run.text = t
            f = run.font; f.name = FONT
            if r_i == 0:
                f.size = Pt(header_size); f.bold = True; f.color.rgb = WHITE
                c.fill.solid(); c.fill.fore_color.rgb = header_fill
            else:
                f.size = Pt(body_size)
                f.bold = bold or (first_col_bold and c_i == 0)
                f.color.rgb = col if col is not None else INK
                c.fill.solid()
                c.fill.fore_color.rgb = (fills[r_i] if fills and fills.get(r_i) else (WHITE if r_i % 2 else PANEL))
    return heights


def bar_chart(slide, x, y, w, h, cats, series, ymax, refs=(), fmt="{:.1f}", label_size=10, legend=True,
              unit_note=None, gap=0.35, gutter=0.0, cat_h=0.3):
    """Shape-drawn grouped column chart. series: list of (name, values, color). refs: (value,label,color)."""
    if unit_note:
        text(slide, x, y, w, 0.28, [P(unit_note, 10, True, GRAY)], check=False)
        y, h = y + 0.3, h - 0.3
    left_pad, bottom_pad, top_pad = 0.15, cat_h + 0.1, 0.35 if legend and len(series) > 1 else 0.1
    px, py, pw, ph = x + left_pad, y + top_pad, w - left_pad - 0.1 - gutter, h - top_pad - bottom_pad
    base = py + ph
    hline(slide, px, base, px + pw, MUTED, 1)
    ncat, ns = len(cats), len(series)
    slot = pw / ncat
    group_w = slot * (1 - gap)
    bw = group_w / ns
    for ci, cat in enumerate(cats):
        gx = px + ci * slot + (slot - group_w) / 2
        for si, (name, vals, colr) in enumerate(series):
            v = vals[ci]
            bh = ph * v / ymax
            bx = gx + si * bw
            if v > 0:
                rect(slide, bx + 0.02, base - bh, bw - 0.04, bh, colr)
            lbl = fmt.format(v) if v else ""
            if bh >= 0.45:
                text(slide, bx - 0.15, base - bh + 0.04, bw + 0.3, 0.26,
                     [P(lbl, label_size, True, WHITE if colr != BLUE_L else INK, align=PP_ALIGN.CENTER)],
                     check=False, inset=0.0)
            else:
                text(slide, bx - 0.15, base - bh - 0.27, bw + 0.3, 0.26,
                     [P(lbl, label_size, True, INK, align=PP_ALIGN.CENTER)], check=False, inset=0.0)
        text(slide, px + ci * slot, base + 0.04, slot, cat_h,
             [P(c_, 10.5 if k == 0 else 9.5, k > 0, GRAY, align=PP_ALIGN.CENTER) for k, c_ in enumerate(cat.split("\n"))],
             check=False)
    for v, lbl, colr in refs:
        ry = base - ph * v / ymax
        hline(slide, px, ry, px + pw, colr, 1.5, MSO_LINE_DASH_STYLE.DASH)
        if gutter:
            text(slide, px + pw + 0.05, ry - 0.14, gutter + 0.1, 0.28, [P(lbl, 9.5, True, colr)], check=False,
                 inset=0.02, anchor=MSO_ANCHOR.MIDDLE)
        else:
            text(slide, px, ry - 0.27, 3.2, 0.26, [P(lbl, 9.5, True, colr)], check=False, inset=0.02)
    if legend and len(series) > 1:
        lx = px
        for name, vals, colr in series:
            rect(slide, lx, y + 0.08, 0.16, 0.16, colr)
            text(slide, lx + 0.18, y + 0.01, 2.6, 0.3, [P(name, 9.5, False, GRAY)], check=False, inset=0.03)
            lx += 0.3 + len(name) * 0.075


def pill(slide, x, y, w, label, color, h=0.28, size=9.5):
    s = rect(slide, x, y, w, h, color, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    tf = s.text_frame; tf.margin_left = tf.margin_right = Inches(0.03)
    tf.margin_top = tf.margin_bottom = Inches(0)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    r = tf.paragraphs[0].add_run(); r.text = label
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    r.font.name = FONT; r.font.size = Pt(size); r.font.bold = True; r.font.color.rgb = WHITE
    return s


def takeaway(slide, y, msg, h=0.5):
    rect(slide, 0.6, y, 0.07, h, BLUE)
    text(slide, 0.75, y, 12.0, h, [P(msg, 12, True, NAVY)], anchor=MSO_ANCHOR.MIDDLE)


SRC = "Source: Briefing pack (synthetic benchmark data); team analysis. "

# =====================================================================
# 1. Title
slide_no[0] += 1
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, 13.333, 7.5, NAVY)
rect(s, 0.8, 2.15, 0.1, 2.0, ORANGE)
text(s, 1.1, 2.0, 11, 1.4, [P("Pelican Packaging: reserve, build or bridge?", 36, True, WHITE)], check=False)
text(s, 1.1, 3.05, 11, 1.2, [P("Recommendation on the second molding-line installation slot, the full line order "
                                "and temporary overflow capacity", 17, False, RGBColor(0xCD, 0xE2, 0xFB))],
     check=False)
text(s, 1.1, 5.3, 11, 1.0, [P("Investment Committee pre-read  |  for decision at the January 2027 IC", 13, True, WHITE),
                            P("Prepared November 2026  |  Built only from the IC briefing pack (synthetic "
                              "benchmark data); no external research", 11, False,
                              RGBColor(0xCD, 0xE2, 0xFB), space=4)], check=False)

# =====================================================================
# 2. Executive summary
s = new_slide("Reserve the slot as a capped $0.6M option, bridge 2028 with the contract molder, and order the "
              "line only once signed demand and funding clear set triggers",
              "Executive summary", SRC + "Cash figures exclude 2027-30 operating cash flow, which the pack does not give.")
blocks = [
    ("1", "The gap is real and starts in 2028, but its size hinges on unsigned demand",
     ["Measured on accepted units, the line is 92% utilized in 2027, not 83%; overflow starts in 2028 (0.6M units)",
      "At forecast, overflow reaches 3.5M units by 2030. At signed minimums it is only 0.9M; 2.6M of 2030 volume is unsigned",
      "The 98% fill rate is measured monthly; two misses let a customer rebid its whole allocation"]),
    ("2", "Ordering now breaks the cash covenant; doing nothing breaks the fill-rate standard",
     ["A full order leaves $4.0M of cash against the $7.0M floor ($3.0M short), and no borrowing facility exists",
      "Doing nothing leaves 0.6M units unserved at the 2028 peak and 3.5M by 2030",
      "The molder covers 2028-29 for $0.07-0.27M a year, but at forecast it falls 1.0M units short in 2030 and cannot make the specialty product"]),
    ("3", "The slot is a capped option worth buying, provided the order date can move",
     ["Cash stays $1.2M above the floor; the most we can lose is the $0.6M deposit",
      "It pays for itself only by protecting customer allocations. On incremental margin alone it does not",
      "As offered, the slot expects an order by June 2027, but funding is only plausible in 2028. Agree a later order date before paying"]),
    ("4", "Three hard triggers turn the reservation into a full order",
     ["Demand: signed 2029 or 2030 minimums of 10.5M units or more (today 9.4M / 9.8M), or a simulated fill-rate breach in 2+ months",
      "Funding: at least $3.5M committed, so cash after the $4.2M payment stays at $7.5M or more",
      "Readiness: supplier dates and the specialty validation plan confirmed. Target decision Q1 2028, last possible date Q3 2028"]),
]
for i, (num, head, buls) in enumerate(blocks):
    yy = 1.62 + i * 1.32
    rect(s, 0.6, yy, 0.45, 1.18, NAVY)
    text(s, 0.6, yy, 0.45, 1.18, [P(num, 20, True, WHITE, align=PP_ALIGN.CENTER)], anchor=MSO_ANCHOR.MIDDLE,
         check=False)
    text(s, 1.15, yy, 3.6, 1.18, [P(head, 13, True, NAVY)], anchor=MSO_ANCHOR.MIDDLE)
    text(s, 4.85, yy, 8.0, 1.18, [P(b, 10.5, False, INK, bullet=True, space=2) for b in buls],
         anchor=MSO_ANCHOR.MIDDLE)
    if i < 3:
        hline(s, 1.15, yy + 1.25, 12.83, RULE)

# =====================================================================
# 3. Hypothesis test
s = new_slide("The starting hypothesis (reserve now, gate the order) survives the tests, but only with a funding "
              "plan and a flexible order date", "How we tested the answer",
              SRC + "Starting hypothesis = Operations Director's proposal: reserve the slot, release the machine "
                    "only after signed orders and a liquidity review.")
G, A, R, Q = ("Holds", GOOD), ("Partly", WARN), ("Not yet", BAD), ("Unverified", WARN)
rows = [["What would have to be true", "Evidence from the briefing pack", "Verdict"],
        ["H1  A full order now does not fit within the covenant", "$11.0M - $2.2M committed R&D - $4.8M = $4.0M, vs a $7.0M floor (-$3.0M)", G],
        ["H2  2028 overflow can be served without the new line", "0.6M units of overflow vs the molder's 2.5M ceiling; 5 months' notice needed; specialty volume not yet in 2028", G],
        ["H3  Demand beyond the molder's reach is credible within the line's lead time", "At forecast, 2030 overflow is 3.5M (1.0M over the ceiling). At signed minimums it is 0.9M. Two programs slipped a quarter last year", A],
        ["H4  The slot is affordable and its downside is capped", "$8.8M - $0.6M = $8.2M, still $1.2M above the floor; the most we can lose is the forfeited $0.6M", G],
        ["H5  The $4.2M balance can be funded when the order must be placed", "No committed facility. The prepayment / signed-volume loan is uncontracted and the CFO sees it in 2028", R],
        ["H6  The slot secures timing we could not get without it", "The slot reserves an installation crew, not capacity. The pack gives no lead time without a slot; its timeline assumes an order by June 2027", Q]]
hts = table(s, 0.6, 1.62, [4.2, 6.5, 1.5], [r[:2] + [""] for r in rows], body_size=11, header_size=11,
            row_h=0.6, label="hyp", max_h=4.5)
yy = 1.62 + hts[0]
for r_i in range(1, len(rows)):
    lab, col = rows[r_i][2]
    pill(s, 11.42, yy + hts[r_i] / 2 - 0.15, 1.25, lab, col, h=0.3, size=10)
    yy += hts[r_i]
takeaway(s, 6.25, "Revision: same direction, tighter conditions. H5 becomes a release trigger; H6 must be "
                  "settled with the supplier before the March deposit.", 0.55)

# =====================================================================
# 4. Practical capacity
s = new_slide("Measured on accepted units, the line is already 92% utilized in 2027 and overflows from 2028; "
              "the '17% free capacity' view divides by nameplate output", "1  The need",
              SRC + "Practical accepted capacity of 9.0M units is net of maintenance, validated changeovers and quality holds; "
                    "nameplate is 10.0M.")
bar_chart(s, 0.6, 1.6, 6.9, 4.6, ["2027", "2028", "2029", "2030"],
          [("Forecast good units (M)", [8.3, 9.6, 11.2, 12.4], BLUE)], 13.5,
          refs=[(10.0, "Nameplate 10.0M", MUTED), (9.0, "Practical 9.0M", ORANGE)],
          legend=False, unit_note="Forecast good units vs capacity, millions", gutter=1.35)
rows = [["Utilization", "2027", "2028", "2029", "2030"],
        ["Ops KPI: forecast / nameplate 10.0M", "83%", "96%", "112%", "124%"],
        [("Accepted units / practical 9.0M", NAVY), ("92%", NAVY), ("107%", NAVY), ("124%", NAVY), ("138%", NAVY)],
        ["Free practical capacity (M units)", "0.7", "-0.6", "-2.2", "-3.4"]]
table(s, 7.75, 1.7, [2.35, 0.7, 0.7, 0.7, 0.7], rows, body_size=10, header_size=10, label="util")
text(s, 7.75, 3.55, 5.1, 2.7, [
    P("Why the Ops KPI misleads", 12, True, NAVY),
    P("It divides units started by nameplate hours and reports quality rejects separately, so it overstates "
      "headroom", 10.5, bullet=True, space=4),
    P("Real 2027 slack is 0.7M units (7.8%), not 1.7M (17%)", 10.5, bullet=True, space=3),
    P("Specialty runs scrap 4 points more than the standard mix, and the forecast has no allowance for it: about "
      "0.09-0.10M units of capacity lost a year from 2029", 10.5, bullet=True, space=3),
    P("Calculation: 20% x 11.2M = 2.24M specialty units x 4% = 0.09M (2030: 2.48M x 4% = 0.10M)", 9.5,
      color=GRAY, space=5, italic=True)])
takeaway(s, 6.32, "The plant has no real buffer for 2028 peaks: whatever the decision, the bridge has to be in "
                  "place before the 2028 peak.", 0.5)

# =====================================================================
# 5. Scenarios of overflow
s = new_slide("The size of the gap depends on unsigned demand: at forecast, overflow reaches 3.5M units by 2030; "
              "at signed minimums it is only 0.9M", "1  The need",
              SRC + "Overflow = demand above 9.0M practical capacity plus the specialty scrap allowance (20% of 2029-30 units "
                    "x 4%). Slip case = forecast delayed one year (assumption).")
bar_chart(s, 0.6, 1.6, 7.6, 4.65, ["2027", "2028", "2029", "2030"],
          [("Forecast", [0, 0.6, 2.3, 3.5], BLUE), ("Forecast slips one year", [0, 0, 0.7, 2.3], BLUE_L),
           ("Signed minimums only", [0, 0, 0.5, 0.9], ORANGE)], 4.0,
          refs=[(2.5, "Molder ceiling 2.5M", BAD)], label_size=9.5, gutter=1.45,
          unit_note="Overflow above internal capacity, millions of accepted units")
text(s, 8.45, 1.65, 4.4, 4.6, [
    P("What drives the range", 12, True, NAVY),
    P("Unsigned volume: of the 12.4M units forecast for 2030, 2.6M (21%) sit above signed minimums and are "
      "nonbinding", 10.5, bullet=True, space=4),
    P("Timing: two key design programs slipped a quarter last year; a one-year slip pushes the molder "
      "ceiling breach from 2030 to 2031", 10.5, bullet=True, space=3),
    P("Mix: specialty volume adds roughly 0.1M units of overflow a year through extra scrap", 10.5,
      bullet=True, space=3),
    P("Implication", 12, True, NAVY, space=10),
    P("Only the forecast case needs a second line before 2031. Committing $4.8M before customers sign is a bet "
      "on the top bar.", 10.5, space=3)])
takeaway(s, 6.32, "The new line is needed only if unsigned demand arrives on time, so signed volume should "
                  "trigger the order.", 0.5)

# =====================================================================
# 6. Monthly fill rate
s = new_slide("Annual totals understate the risk: the 98% standard is measured monthly, and with the molder "
              "maxed out, 2029 runs at 98% of monthly supply", "1  The need",
              SRC + "Monthly rates = annual capacity / 12 (even-flow simplification). Contribution proxy uses the pack's "
                    "$0.45/unit for serving rather than refusing demand.")
cols = [("What the standard requires", [
            "A 98% fill rate every month, for every medical-device customer",
            "Missing it twice gives the customer the right to rebid its whole supplier allocation, not just the "
            "units missed"]),
        ("Why annual capacity is not enough", [
            "Internal practical rate is ~0.75M units a month; the molder adds at most ~0.21M a month",
            "Several customer launches inside one six-week window can exceed the monthly rate even when the year "
            "fits (plant supervisor)",
            "The molder has not committed holiday-period capacity"]),
        ("What is at stake", [
            "Base business of 9.0M units x $0.45 = ~$4.0M of annual contribution exposed to a rebid (proxy)",
            "Losing a quarter of it costs ~$1.0M a year, more than the $0.45M lost on the 2030 forecast shortfall itself",
            "A monthly simulation or an inventory buffer is needed to confirm compliance"])]
for i, (head, buls) in enumerate(cols):
    xx = 0.6 + i * 4.12
    rect(s, xx, 1.65, 3.95, 0.5, NAVY)
    text(s, xx, 1.65, 3.95, 0.5, [P(head, 12.5, True, WHITE)], anchor=MSO_ANCHOR.MIDDLE)
    text(s, xx, 2.2, 3.95, 2.05, [P(b, 11, bullet=True, space=5) for b in buls], fill=PANEL)
rows = [["Average month, forecast (M units)", "2028", "2029", "2030"],
        ["Demand: annual forecast / 12", "0.80", "0.93", "1.03"],
        ["Max supply: internal (after scrap) + molder (2.5M / 12)", "0.75 + 0.21 = 0.96", "0.74 + 0.21 = 0.95",
         "0.74 + 0.21 = 0.95"],
        [("Demand as % of max monthly supply", NAVY), ("83%", GOOD), ("98%", WARN), ("109%", BAD)],
        ["How far a peak month can exceed the average", "~20%", ("~2%", WARN), ("None: short every month", BAD)]]
table(s, 0.6, 4.4, [4.6, 2.5, 2.5, 2.6], rows, body_size=11, header_size=11, label="monthly")
takeaway(s, 6.25, "In 2029 even the molder bridge leaves only ~2% monthly headroom: a launch cluster could "
                  "trigger the two misses that open a rebid.", 0.55)

# =====================================================================
# 7. Cash
s = new_slide("Ordering the full line now would leave $4.0M of cash, $3.0M below the covenant floor, and "
              "the growth evidence offered for it does not show cause and effect", "2  The options",
              SRC + "Cash after 2027 commitments = $11.0M unrestricted - $2.2M approved validation/R&D - path commitment. "
                    "Operating cash flow excluded (not in pack).")
bar_chart(s, 0.6, 1.6, 6.6, 4.65, ["Do nothing", "Molder only", "Reserve slot", "Order line now"],
          [("Cash", [8.8, 8.8, 8.2, 4.0], BLUE)], 10.0, refs=[(7.0, "Floor $7.0M", BAD)],
          fmt="${:.1f}M", legend=False, unit_note="Cash after 2027 commitments, $M", gutter=1.0)
rows = [["Cash test, 2027 ($M)", "Order now", "Reserve slot"],
        ["Unrestricted cash", "11.0", "11.0"],
        ["Approved validation / R&D", "-2.2", "-2.2"],
        ["Path commitment", "-4.8", "-0.6"],
        [("Cash after commitments", NAVY), ("4.0", BAD), ("8.2", GOOD)],
        ["Headroom vs $7.0M floor", ("-3.0", BAD), ("+1.2", GOOD)]]
table(s, 7.5, 1.65, [2.45, 1.4, 1.45], rows, body_size=10.5, label="cash")
text(s, 7.5, 4.15, 5.35, 2.1, [
    P("The Sales VP's '23% faster growth' claim", 12, True, NAVY),
    P("It compares companies at one point in time: the early builders also held more advance purchase "
      "commitments and sold into faster-growing therapeutic segments", 10.5, bullet=True, space=3),
    P("It cannot show that building capacity caused the growth, and the board will not accept 'demand is "
      "growing' as a reason to breach the floor", 10.5, bullet=True, space=3)])
takeaway(s, 6.32, "With no facility, ordering in 2027 needs at least $3.0M of new funding. 'Order now' is "
                  "ruled out on cash.", 0.5)

# =====================================================================
# 8. Options scorecard
s = new_slide("Only 'reserve the slot + molder bridge' passes every hard constraint while keeping "
              "2030 capacity available", "2  The options",
              SRC + "Costs are 2027-30 incremental cash at forecast demand: capex, $0.55M/yr fixed cost from commissioning, "
                    "molder premium $0.12/unit, lost contribution $0.45/unit. They exclude operating cash flow and value after 2030.")
rows = [["Path", "2027 covenant", "2028 service (0.6M overflow)", "2030 service at forecast (3.5M)",
         "Specialty product", "2027-30 cost at forecast", "Reversibility"],
        ["Order line now", ("Fails: $4.0M", BAD), "Line from ~Jan 2028", ("Covered", GOOD), "In-house",
         "$6.45M = 4.8 + 3 x 0.55", ("$4.8M sunk", BAD)],
        [("Reserve slot + molder bridge (recommended)", NAVY), ("Passes: $8.2M", GOOD), ("Molder, $0.07M", GOOD),
         ("Covered if triggers met by Q3 2028", GOOD), "In-house priority",
         "$5.8M if ordered Q1 2028; $0.6M + premium if not", ("Max loss $0.6M", GOOD)],
        ["Molder only", ("Passes: $8.8M", GOOD), ("Molder, $0.07M", GOOD), ("1.0M units short", BAD),
         ("Molder not validated", WARN), "$0.65M premium + $0.45M lost (2030) + rebid risk", ("Fully flexible", GOOD)],
        ["Do nothing", ("Passes: $8.8M", GOOD), ("0.6M unserved", BAD), ("3.5M unserved", BAD), "n/a",
         "$2.9M lost contribution + rebid risk", "n/a"]]
hts = table(s, 0.6, 1.62, [2.0, 1.45, 1.75, 1.95, 1.5, 2.15, 1.43], rows, body_size=11, header_size=10.5,
            row_h=0.62, fills={2: RGBColor(0xE6, 0xF0, 0xFB)}, label="score", max_h=4.4)
text(s, 0.6, 1.62 + sum(hts) + 0.2, 12.2, 1.15, [
    P("How the recommended path's $5.8M builds up: $4.8M line (deposit credited, not double-counted) + $0.07M "
      "molder premium in 2028 + $0.14M for H1 2029 + $0.83M fixed cost for mid-2029 to 2030. That is $0.6M less than "
      "ordering now, because fixed costs start about 18 months later.", 11, color=GRAY),
    P("Molder only is cheapest to 2029 but cannot meet forecast 2030 demand. Do nothing fails in the first peak.",
      11, color=GRAY, space=4)])
takeaway(s, 6.25, "Choosing 'reserve + bridge' over 'order now' costs nothing in capacity; it removes the "
                  "covenant breach and a $4.8M bet on unsigned demand.", 0.55)

# =====================================================================
# 9. Molder
s = new_slide("The contract molder is a cheap bridge through 2029, but at forecast it runs out in 2030 and it "
              "cannot make the specialty product", "2  The options",
              SRC + "Premium of $0.12/accepted unit excludes first-article validation for the specialty product. "
                    "2029 at 92% of the ceiling leaves 0.2M units of annual slack.")
bar_chart(s, 0.6, 1.6, 6.2, 4.65, ["2028\n24% of ceiling", "2029\n92% of ceiling", "2030\n140%: 1.0M short"],
          [("Forecast overflow", [0.6, 2.3, 3.5], BLUE)], 4.0, refs=[(2.5, "Ceiling 2.5M", BAD)],
          fmt="{:.1f}M", legend=False, unit_note="Forecast overflow (incl. specialty scrap), millions of units",
          gutter=1.05, cat_h=0.5)
rows = [["Molder economics", "2028", "2029", "2030"],
        ["Units sent to molder (M)", "0.6", "2.29", "2.5 (cap)"],
        ["Premium @ $0.12 ($M)", "0.07", "0.27", "0.30"],
        ["Unserved units (M)", "0", "0", ("1.0", BAD)],
        ["Lost contribution @ $0.45 ($M)", "0", "0", ("0.45", BAD)]]
table(s, 7.05, 1.65, [2.6, 0.9, 0.9, 1.4], rows, body_size=10.5, label="molder")
text(s, 7.05, 3.55, 5.8, 2.7, [
    P("Limits beyond the ceiling", 12, True, NAVY),
    P("Specialty (20% of 2029 units, 2.24M) is not validated at the molder, so it must run in-house and "
      "takes the internal slack", 10.5, bullet=True, space=3),
    P("Five months' notice; holiday-period capacity not yet committed", 10.5, bullet=True, space=3),
    P("Still worth using: serving through the molder keeps $0.33 of the $0.45 unit contribution, against $0 "
      "for a refused order", 10.5, bullet=True, space=3)])
takeaway(s, 6.32, "Use the molder to bridge 2028-29. It is not a substitute for the line if forecast 2030 "
                  "demand arrives.", 0.5)

# =====================================================================
# 10. Line economics
s = new_slide("The new line is insurance for customer allocations, not a margin play: it beats the molder on "
              "running cost only above 4.6M overflow units a year", "2  The options",
              SRC + "No salvage value, useful life or discount rate is given, so the comparison is on annual "
                    "running economics only. $0.45 and $0.12 are not compared as if they were alternative price quotes.")
rect(s, 0.6, 1.65, 3.9, 4.45, PANEL)
text(s, 0.75, 1.75, 3.6, 0.4, [P("Break-even overflow volume", 12, True, NAVY)])
text(s, 0.75, 2.2, 3.6, 1.0, [P("4.6M", 44, True, BLUE)])
text(s, 0.75, 3.25, 3.6, 2.75, [
    P("units a year = $0.55M line fixed cost / $0.12 molder premium per unit", 11.5, color=GRAY),
    P("Forecast overflow peaks at 3.5M (2030), so within the molder's 2.5M ceiling, buying is cheaper "
      "than running a second line, even before the $4.8M capex", 11.5, space=10),
    P("The line saves $0.12 per unit inside the ceiling, but $0.45 per unit beyond it", 11.5, True, NAVY, space=10)])
rows = [["2030 at forecast ($M/yr)", "New line", "Molder only"],
        ["Units served internally / via molder", "3.5M / 0", "0 / 2.5M"],
        ["Contribution on overflow", "3.5 x 0.45 = 1.58", "2.5 x 0.33 = 0.83"],
        ["Line fixed cost", "-0.55", "0"],
        [("Net, before $4.8M capex", NAVY), ("1.03", NAVY), ("0.83", NAVY)],
        ["Units left unserved", "0", ("1.0M (rebid trigger)", BAD)]]
table(s, 4.8, 1.65, [3.5, 2.2, 2.35], rows, body_size=11, row_h=0.4, label="line econ")
text(s, 4.8, 4.3, 8.05, 1.85, [
    P("So the line earns only ~$0.20M a year more than the molder in 2030. The $4.8M is justified by "
      "what it protects:", 11, True, NAVY),
    P("Fill-rate compliance in peak months, which protects ~$4.0M a year of base contribution from rebids", 10.5,
      bullet=True, space=3),
    P("In-house capacity for the specialty product the molder cannot make", 10.5, bullet=True, space=2),
    P("Growth after 2030: each 1M units above the molder ceiling adds $0.45M a year to the line's advantage",
      10.5, bullet=True, space=2)])
takeaway(s, 6.25, "Because the case rests on protecting allocations, the order trigger should be signed customer "
                  "volume, not forecast margin.", 0.55)

# =====================================================================
# 11. Slot as an option
s = new_slide("The slot is a capped option: it risks at most $0.6M, keeps $1.2M above the cash floor and pays "
              "off only if it heads off an allocation rebid", "3  The slot decision",
              SRC + "Break-even probability = $0.6M at risk / loss avoided for one year of late capacity. Rebid shares are "
                    "illustrative, applied to the 9.0M-unit base x $0.45 proxy.")
rows = [["Outcome", "What happens to the $0.6M", "Net cost of the slot"],
        ["Line ordered (triggers met)", "Credited toward the $4.8M", ("$0", GOOD)],
        ["Line not ordered", "Forfeited", ("$0.6M", BAD)],
        ["Scale check (signed-minimum case)", "Equals ~5.5 years of the 2030 molder premium ($0.11M)", "$0.6M"]]
table(s, 0.6, 1.65, [2.5, 2.7, 1.2], rows, body_size=11, row_h=0.45, label="payoff")
text(s, 0.6, 3.85, 6.4, 2.3, [
    P("Cash test with the deposit paid", 12, True, NAVY),
    P("$8.8M - $0.6M = $8.2M, still $1.2M above the floor. The deposit uses a third of the $1.8M headroom, "
      "leaving room for 2028-29 molder premiums ($0.35M)", 11.5, bullet=True, space=3),
    P("The deposit does not fund the line: the $4.2M balance still needs at least $3.0M of new money", 11.5,
      bullet=True, space=3)])
rows = [["Loss avoided if 2030 capacity is late by one year", "$M", "Break-even probability"],
        ["Shortfall only: 1.0M units x $0.45", "0.45", ("133%: not justified", BAD)],
        ["+ rebid loses 25% of base allocation", "1.46", ("41%", WARN)],
        ["+ rebid loses 50% of base allocation", "2.48", ("24%", GOOD)]]
table(s, 7.3, 1.65, [3.0, 0.75, 1.8], rows, body_size=11, row_h=0.5, label="BE")
text(s, 7.3, 3.85, 5.55, 2.3, [
    P("How to read it", 12, True, NAVY),
    P("On lost units alone, the deposit would not be worth paying", 11.5, bullet=True, space=3),
    P("It is worth paying if there is roughly a 1-in-4 to 2-in-5 chance that the slot is what keeps a "
      "customer's allocation. Today's 2.6M of unsigned 2030 volume and the 2028 overflow make that plausible", 11.5,
      bullet=True, space=3),
    P("That chance is only real if the slot buys timing we could not otherwise get (H6)", 11.5, bullet=True, space=3)])
takeaway(s, 6.25, "Recommendation: pay the deposit as insurance, on condition that its order date can be "
                  "deferred. Without that, the insurance lapses before funding arrives.", 0.55)

# =====================================================================
# 12. What makes the slot a bad option
s = new_slide("Reserving the slot becomes a bad option under five conditions; the two most likely can be "
              "tested before the March deposit", "3  The slot decision",
              SRC + "The pack gives no slot expiry or deferral terms; the June 2027 order date comes from the stated "
                    "'if ordered by June 2027, machine expected mid-2028'.")
rows = [["Condition that destroys the slot's value", "Why it hurts", "Test or mitigation", "When"],
        ["1  The order must be placed by June 2027, while funding is only plausible in 2028",
         "We would have to forfeit $0.6M or breach the covenant", "Negotiate an order date of Q1 2028 or later (install H1 2029); otherwise decline", ("Before Mar 2027", NAVY)],
        ["2  The slot buys nothing scarce: a 12-month lead time is available without it",
         "Paying $0.6M for timing we would get anyway", "Get written lead time and crew availability without a slot", ("Before Mar 2027", NAVY)],
        ["3  Demand stays near signed minimums",
         "Overflow of 0.9M or less through 2030; molder covers it for $0.11M a year or less", "Track signed volume quarterly; kill at the go/no-go gate", "Gate 2"],
        ["4  Programs slip a year",
         "The line arrives a year early and carries $0.55M a year of fixed cost before it is needed", "Use the deferral right; molder covers 2030 at 92% of its ceiling", "Gate 2"],
        ["5  Cash headroom erodes in 2027",
         "The deposit uses $0.6M of $1.8M headroom; pre-build stock and validation compete for the rest", "13-week cash forecast; cap pre-build working capital", "Monthly"]]
table(s, 0.6, 1.62, [3.6, 3.3, 3.75, 1.55], rows, body_size=11, header_size=11, row_h=0.7,
      label="bad option", max_h=4.5)
takeaway(s, 6.25, "If the supplier will not move the order date to Q1 2028 or later, decline the slot and plan on "
                  "the molder plus a 2028 order at standard lead time, once that lead time is confirmed.", 0.55)

# =====================================================================
# 13. Near-term overflow plan
s = new_slide("Cover 2028 in three layers: the contract molder booked by June 2027, a 2027 safety stock, and "
              "specialty kept in-house", "4  The plan and gates",
              SRC + "The pack says the 2028 peak starts before mid-2028; we assume around Q2 2028, so the latest molder notice "
                    "is about November 2027. Unit cost for pre-build not given.")
cols = [("A. External capacity: contract molder", [
            "Book 0.6M units for 2028 (24% of the ceiling), about $0.07M of premium",
            "Formal notice is 5 months, but sign by 30 June 2027 to lock in holiday-period capacity",
            "Hold an option on up to 2.3M units for 2029 (~$0.27M)",
            "Get a quote and timeline for specialty first-article validation as a hedge"]),
        ("B. Internal buffer: 2027 safety stock", [
            "2027 has 0.7M units of practical slack (9.0M - 8.3M), more than the 2028 overflow",
            "Pre-build standard containers ahead of the 2028 peak to absorb launch clustering",
            "Depends on shelf-life and customer lot rules; cap the working capital so cash headroom holds"]),
        ("C. Internal mix: protect what only we can make", [
            "Schedule specialty first on the own line; the molder is not validated for it",
            "Add a 4-point specialty scrap allowance to the plan (~0.1M units a year)",
            "Run a monthly fill-rate simulation (launch windows, holidays, scrap) by Q2 2027"])]
for i, (head, buls) in enumerate(cols):
    xx = 0.6 + i * 4.12
    rect(s, xx, 1.65, 3.95, 0.55, NAVY)
    text(s, xx, 1.65, 3.95, 0.55, [P(head, 12, True, WHITE)], anchor=MSO_ANCHOR.MIDDLE)
    text(s, xx, 2.25, 3.95, 2.35, [P(b, 11, bullet=True, space=5) for b in buls], fill=PANEL)
rows = [["2028 coverage check (M units)", "Available", "Planned use", "Cost"],
        ["Contract molder", "2.5", "0.6 (24%)", "$0.07M premium"],
        ["2027 safety stock from practical slack", "up to 0.7", "Peak-month buffer", "Working capital (unit cost not in pack)"],
        [("Total cover vs 0.6M forecast overflow", NAVY), ("3.2", NAVY), ("~5x the overflow", GOOD), "Fixed capex: $0"]]
table(s, 0.6, 4.75, [4.2, 1.6, 2.6, 3.8], rows, body_size=11, header_size=11, label="cover2028")
takeaway(s, 6.25, "Only a January 2027 order, which breaches the covenant, gets the line in before the 2028 peak; "
                  "any compliant order arrives after it, so 2028 needs this bridge.", 0.55)

# =====================================================================
# 14. Triggers
s = new_slide("Release the $4.2M balance only when all three triggers are met: demand, funding and readiness",
              "4  The plan and gates",
              SRC + "10.5M threshold and $0.5M buffer are our proposals. Internal capacity after specialty scrap ~8.9M + molder 2.5M "
                    "= ~11.4M of demand coverable without the line.")
cols = [("Demand", "Signed 2029 or 2030 minimums of 10.5M units or more (today 9.4M / 9.8M), including take-or-pay or prepaid volume",
         ["OR: the monthly simulation shows 2+ months below 98% with the molder at its contracted capacity",
          "Why 10.5M: signed overflow (~1.6M) would already use two-thirds of the molder ceiling, and fewer than half of "
          "the remaining 1.9M unsigned forecast units would exhaust it"]),
        ("Funding", "At least $3.5M of committed funding, so cash after the $4.2M payment is $7.5M or more",
         ["Arithmetic: $8.2M - $4.2M = $4.0M; plus $3.5M = $7.5M, i.e. the $7.0M floor plus a $0.5M buffer",
          "Sources: customer prepayment, or a supplemental loan backed by a signed-volume guarantee; pricing to be "
          "negotiated"]),
        ("Readiness", "Supplier confirms installation within 12 months of order at a fixed price; specialty validation plan in place",
         ["Plan allows +2 months for specialty validation",
          "Molder bridge contracted through commissioning",
          "Construction inflation re-quoted"])]
for i, (head, main, buls) in enumerate(cols):
    xx = 0.6 + i * 4.12
    rect(s, xx, 1.65, 3.95, 0.5, NAVY)
    text(s, xx, 1.65, 3.95, 0.5, [P(head, 13, True, WHITE)], anchor=MSO_ANCHOR.MIDDLE)
    text(s, xx, 2.2, 3.95, 1.25, [P(main, 11.5, True, NAVY)], fill=RGBColor(0xE6, 0xF0, 0xFB),
         anchor=MSO_ANCHOR.MIDDLE)
    text(s, xx, 3.5, 3.95, 2.2, [P(b, 11.5, bullet=True, space=6) for b in buls], fill=PANEL)
text(s, 0.6, 5.8, 12.2, 0.4, [P("Not triggers: 'demand is growing', nonbinding forecasts, peer growth "
                                "statistics, or a wish to announce capacity publicly.", 10.5, True, BAD)])
takeaway(s, 6.25, "One customer contract can meet two triggers at once: a signed-volume guarantee raises "
                  "committed demand and secures the loan.", 0.55)

# =====================================================================
# 15. Gate timeline
s = new_slide("Four decision gates separate the provisional reservation from the full investment",
              "4  The plan and gates",
              SRC + "Line timing: 12 months from order + up to 2 months extra specialty validation. Order by Q3 2028 to be "
                    "producing before the 2030 peak.")
gates = [("Gate 0", "Jan 2027 IC", ["Owner: CEO / IC", "Approve the $0.6M deposit, conditional on supplier terms",
                                    "Start the molder RFQ and funding workstream", "No full order, no public announcement"]),
         ("Gate 0b", "Feb-Mar 2027", ["Owner: Procurement / Ops", "Supplier confirms an order date of Q1 2028 or later and the lead time in writing",
                                     "Pay the deposit in March, or decline if terms fail"]),
         ("Gate 1", "By Jun 2027", ["Owner: Operations", "Molder signed for 2028, including the holiday period",
                                    "Monthly simulation complete", "Early order only if all 3 triggers are met"]),
         ("Gate 2", "Q1 2028 (target)", ["Owner: IC (CFO case)", "Go/no-go on the $4.2M balance",
                                         "Go: line producing by about mid-2029 and relieves the 2029 peak",
                                         "No-go: book 2029 molder volume"]),
         ("Gate 3", "Q3 2028 (last date)", ["Owner: IC", "Last order date for a line producing before 2030",
                                         "No-go: forfeit $0.6M, extend the molder, re-gate for 2031"])]
w = 2.38
for i, (g, when, buls) in enumerate(gates):
    xx = 0.6 + i * (w + 0.08)
    col = NAVY if i in (0, 3) else BLUE
    shp = rect(s, xx, 1.75, w, 0.85, col, shape=MSO_SHAPE.CHEVRON if i else MSO_SHAPE.PENTAGON)
    text(s, xx + 0.25, 1.75, w - 0.5, 0.85, [P(g, 13, True, WHITE, align=PP_ALIGN.CENTER),
                                             P(when, 10.5, False, WHITE, align=PP_ALIGN.CENTER)],
         anchor=MSO_ANCHOR.MIDDLE)
    text(s, xx, 2.75, w, 2.2, [P(buls[0], 11, True, BLUE)] + [P(b, 11, bullet=True, space=6) for b in buls[1:]],
         fill=PANEL)
arr = {2: "If ordered here: line producing ~mid-2028, after the 2028 peak starts",
       3: "If ordered here: producing ~Q1-Q2 2029 (+2 months validation)",
       4: "If ordered here: producing ~Q3-Q4 2029, just before 2030"}
for i, msg in arr.items():
    xx = 0.6 + i * (w + 0.08)
    text(s, xx, 5.0, w, 0.62, [P(msg, 10, True, NAVY)], fill=RGBColor(0xE6, 0xF0, 0xFB), anchor=MSO_ANCHOR.MIDDLE)
text(s, 0.6, 5.0, 2 * w + 0.08, 0.62, [P("Line timing = 12-month lead time + commissioning; the specialty product may "
                                         "need 2 more months of validation", 10, False, GRAY)], anchor=MSO_ANCHOR.MIDDLE)
rect(s, 0.6, 5.7, 12.25, 0.4, RGBColor(0xE6, 0xF0, 0xFB))
text(s, 0.6, 5.7, 12.25, 0.4, [P("Provisional (Gates 0-1): $0.6M at risk, cash at or above $8.2M   |   Full investment "
                                 "(Gates 2-3): $4.2M, only with at least $3.5M committed funding", 10.5, True, NAVY,
                                 align=PP_ALIGN.CENTER)], anchor=MSO_ANCHOR.MIDDLE)
takeaway(s, 6.25, "Each gate has a date, a proposed owner and a default: if a trigger is missed, the default is "
                  "the cheaper, reversible path.", 0.55)

# =====================================================================
# 16. Downside cases
s = new_slide("If customer orders fall short, the plan degrades gracefully: in the weak-demand cases the worst "
              "outcome is a $0.6M forfeited deposit, never a covenant breach", "4  The plan and gates",
              SRC + "Cash lows exclude operating cash flow. Funded case assumes $3.5M committed at Gate 2. Premiums at $0.12/unit; "
                    "lost contribution at $0.45/unit.")
rows = [["Case (2028 / 2029 / 2030 overflow, M units)", "Molder alone enough?", "Gate outcome", "Incremental cost 2027-30",
         "Lowest cash vs $7.0M floor"],
        ["Forecast, funded (0.6 / 2.3 / 3.5)", ("No: 1.0M short in 2030", BAD), "Triggers met: order Q1 2028",
         "~$5.8M incl. line", ("$7.5M (+0.5)", GOOD)],
        ["One-year slip (0 / 0.7 / 2.3)", ("Yes: 92% of ceiling in 2030", GOOD), "Defer the slot; re-gate for 2031",
         "$0.36M premium (+$0.6M if no deferral)", ("~$7.8M (+0.8)", GOOD)],
        ["Signed minimums only (0 / 0.5 / 0.9)", ("Yes: 36% of ceiling or less", GOOD), "Kill at Gate 2; forfeit deposit",
         "$0.6M + $0.16M premium", ("~$8.0M (+1.0)", GOOD)],
        ["Forecast demand, no funding (0.6 / 2.3 / 3.5)", ("No: 1.0M short in 2030", BAD),
         "No order (the floor holds); molder to cap, safety stock, ration", "$0.6M + $0.65M premium + $0.45M lost + rebid risk",
         ("~$7.6M (+0.6)", WARN)]]
hts = table(s, 0.6, 1.62, [3.1, 2.1, 2.7, 2.35, 1.95], rows, body_size=11, header_size=10.5, row_h=0.65,
            label="cases", max_h=4.0)
text(s, 0.6, 1.62 + sum(hts) + 0.2, 12.2, 1.4, [
    P("The case to watch is the last one: demand arrives but funding does not. The board's rule (no breach of the "
      "floor) then means accepting 2030 rebid risk. The mitigation is to make customer co-funding (prepayment "
      "or a volume guarantee) the price of guaranteed capacity, starting in 2027 negotiations.", 11.5, color=INK),
    P("Calculation, signed case: $8.8M - $0.6M deposit - $0.16M premiums = ~$8.0M. Slip: $8.8M - $0.6M - $0.36M = "
      "~$7.8M. No-funding: $8.8M - $0.6M - $0.65M = ~$7.6M.", 9.5, color=GRAY, italic=True, space=4)])
takeaway(s, 6.25, "The cash floor holds in every case. Weak demand costs at most $0.6M; the unfunded "
                  "forecast case is a customer-retention risk, not a cash risk.", 0.55)

# =====================================================================
# 17. Risks & uncertainties
s = new_slide("The answer is most sensitive to unsigned demand timing, funding and the slot's terms; each is "
              "covered by a gate or a test before the deposit", "4  The plan and gates",
              SRC + "Items marked 'not in pack' are open data gaps, not estimates.")
rows = [["Uncertainty", "Effect on the answer", "How the plan handles it"],
        ["Demand above signed minimums (2.6M units in 2030) and program slips", "Decides whether the line is needed before 2031",
         "Demand trigger on signed volume; quarterly tracking; Gate 3 last date"],
        ["Funding: prepayment / guarantee not contracted; debt pricing not negotiated", "Without it, no order can be placed",
         "Funding trigger of $3.5M or more; CFO term sheet by Gate 2"],
        ["Slot terms: order date, deferral, lead time without a slot (not in pack)", "Decides whether the deposit buys anything",
         "Condition precedent before the March payment"],
        ["Monthly peaks, launch clustering, molder holiday capacity uncommitted", "Fill-rate misses even when annual capacity fits",
         "Monthly simulation; 2027 safety stock; holiday capacity in the molder contract"],
        ["Specialty: +2 months' validation; 4-point scrap allowance missing from forecast", "Line later and capacity ~0.1M units lower",
         "Allowance built in; 14-month line timeline; molder validation quote"],
        ["Construction inflation; no salvage value; 2027-30 operating cash flow (not in pack)", "Capex and cash tests could move",
         "Fixed-price re-quote at Gate 2; 13-week cash forecast"]]
table(s, 0.6, 1.62, [4.4, 3.5, 4.3], rows, body_size=11, header_size=11, row_h=0.62, label="risks", max_h=4.55)
takeaway(s, 6.25, "No single uncertainty overturns the recommendation; together they explain why the "
                  "$4.2M must wait for evidence.", 0.55)

# =====================================================================
# 18. Decisions requested
s = new_slide("We ask the committee for four decisions in January, none of which commits the $4.2M balance",
              "Decisions requested",
              SRC)
decs = [("1", "Approve the $0.6M slot deposit for March 2027, on one condition",
         "Written supplier terms allowing an order date of Q1 2028 or later and confirming the lead time. If refused, decline the slot."),
        ("2", "Decline the full line order and any public capacity announcement now",
         "Instead, let Sales use the reserved slot and molder plan privately to turn nonbinding forecasts into signed minimums or prepayments."),
        ("3", "Authorize the 2028 overflow plan",
         "Contract molder for 0.6M units, signed by June 2027 with holiday capacity; capped 2027 safety stock; specialty validation quote."),
        ("4", "Adopt the three release triggers and the gate calendar",
         "Demand of 10.5M units or more signed, or a simulated breach; at least $3.5M committed funding; readiness confirmed. Target Q1 2028, last date Q3 2028.")]
for i, (n, head, body) in enumerate(decs):
    yy = 1.65 + i * 1.08
    rect(s, 0.6, yy, 0.5, 0.92, NAVY)
    text(s, 0.6, yy, 0.5, 0.92, [P(n, 18, True, WHITE, align=PP_ALIGN.CENTER)], anchor=MSO_ANCHOR.MIDDLE,
         check=False)
    text(s, 1.2, yy, 7.0, 0.92, [P(head, 12.5, True, NAVY), P(body, 11, color=INK, space=2)],
         anchor=MSO_ANCHOR.MIDDLE)
rows = [["Next step", "Owner", "By"],
        ["Supplier terms (order date, lead time, price)", "Procurement / Ops", "Feb 2027"],
        ["Molder RFQ incl. holiday capacity", "Operations", "Jun 2027"],
        ["Monthly fill-rate simulation", "Operations", "Q2 2027"],
        ["Funding term sheet (at least $3.5M)", "CFO", "Q4 2027"],
        ["Signed-volume / prepayment talks", "VP Sales", "Ongoing"],
        ["13-week cash forecast vs floor", "Finance", "Monthly"]]
table(s, 8.45, 1.65, [2.3, 1.3, 0.8], rows, body_size=10.5, header_size=10.5, row_h=0.55, label="next")
takeaway(s, 6.25, "Owners are proposed (management to confirm). Total cash committed by these decisions: $0.6M, "
                 "leaving $8.2M against the $7.0M floor.", 0.55)

# =====================================================================
# 19. Appendix calculations
s = new_slide("Appendix A: every figure in the deck traces to briefing-pack inputs through these calculations",
              "Appendix", SRC + "Reproducible in deliverable/supporting/calc.py.")
rows = [["Item", "Calculation", "Result"],
        ["Cash available above commitments", "$11.0M - $2.2M approved validation/R&D", "$8.8M (headroom $1.8M)"],
        ["Order line now", "$8.8M - $4.8M", "$4.0M; -$3.0M vs floor"],
        ["Reserve slot, then order", "$8.8M - $0.6M = $8.2M; - $4.2M balance = $4.0M (deposit not double-counted)", "Needs $3.0M or more new funding"],
        ["Practical utilization", "8.3 / 9.6 / 11.2 / 12.4 divided by 9.0M", "92% / 107% / 124% / 138%"],
        ["Specialty scrap allowance", "20% x 11.2M x 4% (2029); 20% x 12.4M x 4% (2030); assumed 0 in 2028", "0.09M / 0.10M units"],
        ["Forecast overflow", "Demand - 9.0M + scrap allowance", "0.6 / 2.29 / 3.50M (2028-30)"],
        ["Molder premium", "$0.12 x 0.6M; x 2.29M; x 2.5M (cap)", "$0.07M / $0.27M / $0.30M"],
        ["Line vs molder break-even", "$0.55M / $0.12", "4.6M units a year"],
        ["2030 line vs molder", "3.5 x 0.45 - 0.55 = 1.03 vs 2.5 x (0.45 - 0.12) = 0.83", "Line +$0.20M a year before capex"],
        ["Recommended path, 2027-30 cost", "4.8 + 0.07 + 0.14 (H1 2029 premium) + 0.55 x 1.5 years", "~$5.8M (vs $6.45M order-now)"],
        ["Slot break-even probability", "$0.6M / (0.45 + share x 9.0M x 0.45)", "133% / 41% / 24%"]]
table(s, 0.6, 1.6, [3.0, 6.1, 3.1], rows, body_size=10.5, header_size=10.5, row_h=0.4, label="appx", max_h=5.25)

# =====================================================================
# 20. Assumptions log
s = new_slide("Appendix B: judgment calls made where the pack was silent; each is flagged so the committee can "
              "challenge it", "Appendix", SRC + "These choices were made without access to management; the committee should confirm or replace them.")
rows = [["Gap in the pack", "Choice made", "Effect if wrong"],
        ["2027-30 operating cash flow", "Excluded; cash tests use commitments against $8.8M", "Positive cash flow would ease the funding trigger"],
        ["Slot expiry and deferral terms", "Assume an order by June 2027 unless renegotiated; made a condition of the deposit", "If deferral is already allowed, the case for the slot gets stronger"],
        ["Specialty share in 2028 and 2030", "0% in 2028; 20% in 2030 (same as 2029)", "+/-0.1M units of overflow"],
        ["Timing of the 2028 peak", "About Q2 2028 (pack: before mid-2028)", "Earlier peak brings the molder notice date forward"],
        ["Contribution at risk from a rebid", "$0.45/unit on the 9.0M base; 25% / 50% illustrative losses", "Changes break-even, not direction"],
        ["Demand trigger and cash buffer", "10.5M signed units; $0.5M above the floor", "Policy choices; the committee may tighten or relax them"],
        ["Downside cases", "Slip = forecast delayed one year; weak case = signed minimums", "Other paths fall between these"]]
table(s, 0.6, 1.6, [3.0, 5.0, 4.2], rows, body_size=11, header_size=11, row_h=0.55, label="assump", max_h=5.2)

prs.save(OUT)
print("saved", OUT, "slides", len(prs.slides))
for w_ in WARNINGS:
    print("WARN", w_)
