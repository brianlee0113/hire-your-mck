"""Build the Parcelbird board deck. Numbers come from model.py (re-computed here for traceability)."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from PIL import ImageFont
import sys

# ---------------------------------------------------------------- palette
NAVY = RGBColor(0x0B, 0x25, 0x45)
INK = RGBColor(0x0B, 0x0B, 0x0B)
INK2 = RGBColor(0x52, 0x51, 0x4E)
MUTED = RGBColor(0x8A, 0x89, 0x85)
RULE = RGBColor(0xD9, 0xD7, 0xD2)
PANEL = RGBColor(0xF3, 0xF2, 0xEF)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLUE = RGBColor(0x2A, 0x78, 0xD6)      # positive / primary series
ORANGE = RGBColor(0xEB, 0x68, 0x34)    # negative (diverging warm pole)
AQUA = RGBColor(0x1B, 0xAF, 0x7A)
GREY = RGBColor(0x9E, 0x9C, 0x95)      # totals / context
LIGHTBLUE = RGBColor(0xCD, 0xE2, 0xFB)
OK = RGBColor(0x00, 0x83, 0x00)        # status good
BAD = RGBColor(0xC6, 0x2F, 0x2E)       # status critical (darkened for text contrast)
WARN = RGBColor(0xB0, 0x78, 0x00)      # status warning (darkened for text contrast)

FONT = "Arial"
FONT_FILES = {False: "/Library/Fonts/Arial.ttf", True: "/System/Library/Fonts/Supplemental/Arial Bold.ttf"}
import os
for k, p in list(FONT_FILES.items()):
    if not os.path.exists(p):
        alt = p.replace("/Library/Fonts/", "/System/Library/Fonts/Supplemental/")
        FONT_FILES[k] = alt

_fonts = {}
def font(bold, size):
    key = (bold, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(FONT_FILES[bold], int(size * 20))
    return _fonts[key]

def text_width_pt(s, size, bold=False):
    return font(bold, size).getlength(s) / 20.0

def wrap_lines(s, size, bold, width_pt):
    lines = 0
    for para in s.split("\n"):
        words = para.split(" ")
        cur = ""
        n = 1
        for w in words:
            t = (cur + " " + w) if cur else w
            if text_width_pt(t, size, bold) <= width_pt:
                cur = t
            else:
                n += 1
                cur = w
        lines += n
    return lines

CHECKS = []  # (slide_no, label, needed_pt, available_pt)

# ---------------------------------------------------------------- base helpers
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
SW = 13.333
LM = 0.55
CW = SW - 2 * LM

def I(x):
    return Inches(x)

def rect(slide, x, y, w, h, fill=None, line=None, shape=MSO_SHAPE.RECTANGLE, lw=0.75):
    s = slide.shapes.add_shape(shape, I(x), I(y), I(w), I(h))
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid(); s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line; s.line.width = Pt(lw)
    s.shadow.inherit = False
    if s.has_text_frame:
        s.text_frame.text = ""
    return s

def line(slide, x1, y1, x2, y2, color=RULE, w=0.75):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, I(x1), I(y1), I(x2), I(y2))
    c.line.color.rgb = color; c.line.width = Pt(w)
    return c

def text(slide, x, y, w, h, paras, size=12, color=INK, bold=False, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, inset=0.04, spacing=4, check=True, label=None, line_spacing=1.15):
    """paras: str or list of items; item = str or dict(t=..., b=bool, c=color, s=size, bullet=bool, runs=[(t,bold,color)])."""
    tb = slide.shapes.add_textbox(I(x), I(y), I(w), I(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    tf.margin_left = tf.margin_right = I(inset)
    tf.margin_top = tf.margin_bottom = I(0.02)
    tf.vertical_anchor = anchor
    if isinstance(paras, str):
        paras = [paras]
    exp = []
    for p in paras:
        if isinstance(p, str) and "\n" in p:
            for k, part in enumerate(p.split("\n")):
                exp.append(dict(t=part, sb=(0 if k else None)))
        else:
            exp.append(p)
    paras = [({kk: vv for kk, vv in q.items() if vv is not None} if isinstance(q, dict) else q) for q in exp]
    need = 0.0
    for i, p in enumerate(paras):
        if isinstance(p, str):
            p = dict(t=p)
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = p.get("align", align)
        para.line_spacing = line_spacing
        sz = p.get("s", size)
        if i > 0:
            para.space_before = Pt(p.get("sb", spacing))
        runs = p.get("runs") or [(p["t"], p.get("b", bold), p.get("c", color))]
        bullet = p.get("bullet", False)
        prefix_w = 0
        if bullet:
            runs = [("•  ", False, p.get("bc", MUTED))] + list(runs)
        full = ""
        for (t, b, c) in runs:
            r = para.add_run(); r.text = t
            r.font.name = FONT; r.font.size = Pt(sz); r.font.bold = b; r.font.color.rgb = c
            full += t
        anyb = any(b for (_, b, _) in runs if _ .strip()) if False else all(b for (t, b, c) in runs if t.strip())
        avail_w = (w - 2 * inset) * 72
        n = wrap_lines(full, sz, anyb, avail_w - (0 if not bullet else 0))
        need += n * sz * 1.2 * line_spacing / 1.15 + (p.get("sb", spacing) if i > 0 else 0)
    if check:
        CHECKS.append((len(prs.slides), label or (paras[0] if isinstance(paras[0], str) else paras[0].get("t", str(paras[0].get("runs", ""))))[:50], need, (h - 0.04) * 72))
    return tb

PAGE = {"n": 0}

def new_slide(title, tracker=None, source=None):
    s = prs.slides.add_slide(BLANK)
    PAGE["n"] += 1
    if tracker:
        text(s, LM, 0.28, 9, 0.28, tracker.upper(), size=9.5, color=BLUE, bold=True, check=False)
    text(s, LM, 0.52, CW, 0.95, title, size=21, color=NAVY, bold=True, anchor=MSO_ANCHOR.TOP,
         label="TITLE", line_spacing=1.0)
    line(s, LM, 1.55, SW - LM, 1.55, color=NAVY, w=1.0)
    if source:
        text(s, LM, 6.98, CW - 0.8, 0.36, "Source: " + source, size=8.5, color=MUTED, label="SOURCE")
    text(s, SW - LM - 0.6, 6.98, 0.6, 0.3, str(PAGE["n"]), size=9, color=MUTED, align=PP_ALIGN.RIGHT, check=False)
    return s

def table(slide, x, y, col_w, row_h, rows, header_fill=NAVY, size=10.5, header_size=10,
          first_col_bold=True, fills=None, colors=None, bolds=None, aligns=None, label="table", vcenter=True):
    """rows: list of lists of str. fills/colors/bolds: dict (r,c)->value."""
    nrows, ncols = len(rows), len(col_w)
    if isinstance(row_h, (int, float)):
        row_h = [row_h] * nrows
    shp = slide.shapes.add_table(nrows, ncols, I(x), I(y), I(sum(col_w)), I(sum(row_h)))
    tbl = shp.table
    # disable built-in style banding
    tblPr = shp._element.graphic.graphicData.tbl.tblPr
    tblPr.set("firstRow", "0"); tblPr.set("bandRow", "0")
    for c, w in enumerate(col_w):
        tbl.columns[c].width = I(w)
    for r, h in enumerate(row_h):
        tbl.rows[r].height = I(h)
    fills = fills or {}; colors = colors or {}; bolds = bolds or {}; aligns = aligns or {}
    for r in range(nrows):
        for c in range(ncols):
            cell = tbl.cell(r, c)
            val = rows[r][c]
            cell.margin_left = cell.margin_right = I(0.07)
            cell.margin_top = cell.margin_bottom = I(0.03)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE if vcenter else MSO_ANCHOR.TOP
            tf = cell.text_frame; tf.word_wrap = True
            hdr = (r == 0 and header_fill is not None)
            sz = header_size if hdr else size
            b = bolds.get((r, c), hdr or (c == 0 and first_col_bold))
            col = WHITE if hdr else colors.get((r, c), INK)
            lines_ = val.split("\n")
            for li, ln in enumerate(lines_):
                p = tf.paragraphs[0] if li == 0 else tf.add_paragraph()
                p.alignment = aligns.get((r, c), aligns.get(c, PP_ALIGN.LEFT))
                run = p.add_run(); run.text = ln
                run.font.name = FONT; run.font.size = Pt(sz); run.font.bold = b; run.font.color.rgb = col
            f = fills.get((r, c), header_fill if hdr else (WHITE))
            cell.fill.solid(); cell.fill.fore_color.rgb = f
            n = wrap_lines(val, sz, b, (col_w[c] - 0.14) * 72)
            CHECKS.append((len(prs.slides), f"{label} r{r}c{c}:{val[:25]}", n * sz * 1.2 + 4, row_h[r] * 72))
    return tbl

def status(slide, x, y, w, kind, label=None):
    col = {"ok": OK, "bad": BAD, "warn": WARN}[kind]
    rect(slide, x + 0.02, y + 0.08, 0.15, 0.15, fill=col, shape=MSO_SHAPE.OVAL)
    text(slide, x + 0.24, y, w - 0.24, 0.3, label, size=11, bold=True, color=col, check=False)

# ================================================================= numbers (from model.py)
# Benchmark median per-order
WF_MED = [("Gross margin on goods\n27% × $34 AOV", 9.18), ("Delivery fee\n(net)", 1.99),
          ("Promotions\n6% of AOV", -2.04), ("Picking &\npacking", -3.10),
          ("Rider\n$17.75 ÷ 2.4/hr", -7.40), ("Payment &\npackaging", -1.30),
          ("Contribution\nper order", "T"), ("Site fixed cost\n$1.15M ÷ 328,500", -3.50),
          ("Site-level result\nper order", "T")]

# ================================================================= SLIDE 1: title
s = prs.slides.add_slide(BLANK); PAGE["n"] += 1
rect(s, 0, 0, SW, 7.5, fill=NAVY)
rect(s, LM, 2.35, 0.08, 1.9, fill=BLUE)
text(s, LM + 0.3, 2.25, 11.5, 1.5, "Parcelbird Now: should Parcelbird launch its own quick-commerce grocery delivery service in 2027?",
     size=32, color=WHITE, bold=True, line_spacing=1.0, label="cover title")
text(s, LM + 0.3, 3.85, 11, 0.5, "Board discussion document  ·  Decision meeting, January 2027", size=16, color=LIGHTBLUE)
text(s, LM + 0.3, 6.35, 12, 0.7, ["Built solely from the board briefing pack (synthetic benchmark data; all company, competitor and market figures are fictional). All figures in US$.",
                                  "Calculations are shown on each page and in the appendix."], size=10, color=LIGHTBLUE, spacing=2)

# ================================================================= SLIDE 2: executive summary
s = new_slide("Parcelbird should not launch Parcelbird Now in 2027; it should fund the software business to profitability and keep quick commerce as a gated option",
              tracker="Executive summary",
              source="Board briefing pack (Tables 1–3, sections 7–10); Parcelbird analysis. Detailed calculations on pages 4–12 and in the appendix.")
rect(s, LM, 1.75, CW, 0.95, fill=PANEL)
rect(s, LM, 1.75, 0.07, 0.95, fill=NAVY)
text(s, LM + 0.2, 1.8, CW - 0.3, 0.88,
     [dict(runs=[("Answer: no. ", True, NAVY),
                 ("Quick commerce is a growing market without a profit pool. Launching would lose money on every order at every level of performance anyone has observed, "
                  "breach the board's 12-month runway rule within the first year, and turn the grocers who buy our software into competitors. "
                  "The software business can reach cash break-even inside current cash.", False, INK)])],
     size=12.5, anchor=MSO_ANCHOR.MIDDLE, label="exec answer")
cols = [
    ("1", "Launching would lose money", "pages 4–9", [
        "Market GMV grows ~42% a year ($1.8B → $5.1B, 2022–25), but both scaled incumbents lose $1.90–$3.40 per order; QuickBasket closed 4 of 11 cities",
        "At benchmark-median inputs an order loses $2.67 before site costs and $6.17 after",
        "The plan's +$2.02 per order needs all four levers above the best site ever observed; our own pop-up lost ~$12.60 per order",
        "Pop-up customers do not repay their $38 acquisition cost at benchmark economics"]),
    ("2", "We cannot afford it", "page 10", [
        "The plan needs $9.5M of our $12.0M cash to month 18; no new round is expected",
        "It breaks the ≥12-month runway rule by month ~1 (if on top of today's $0.4M/month burn) or ~11 (most favourable reading)",
        "At benchmark economics nine mature sites would lose ~$18M a year, 1.5× our total cash"]),
    ("3", "Software is the better use of the cash", "pages 11–12", [
        "Indicative model: cash break-even in ~26 months at today's 60% growth, cash never below $5.4M",
        "Still works at 40% growth (break-even ~month 36); below ~30% costs must be cut",
        "9 late-stage deals = $0.86M ARR; pipeline grocers want their own fast delivery from stores, so we sell them the tools rather than compete"]),
]
cw3 = (CW - 0.4) / 3
for i, (num, head, pg, bullets) in enumerate(cols):
    x = LM + i * (cw3 + 0.2)
    rect(s, x, 2.9, 0.42, 0.42, fill=BLUE, shape=MSO_SHAPE.OVAL)
    text(s, x, 2.9, 0.42, 0.42, num, size=14, color=WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, check=False)
    text(s, x + 0.52, 2.84, cw3 - 0.52, 0.62, [dict(t=head, b=True, c=NAVY)], size=13.5, anchor=MSO_ANCHOR.MIDDLE, label="exec col head")
    line(s, x, 3.5, x + cw3, 3.5, color=RULE)
    text(s, x, 3.58, cw3, 2.7, [dict(t=b, bullet=True) for b in bullets] + [dict(t="→ " + pg, c=BLUE, s=10)], size=11, spacing=7, label="exec bullets")
rect(s, LM, 6.32, CW, 0.52, fill=None, line=NAVY, lw=1)
text(s, LM + 0.15, 6.34, CW - 0.3, 0.48,
     [dict(runs=[("Decisions requested:  ", True, NAVY),
                 ("(1) decline the Parcelbird Now launch and its $5.4M capex;  (2) approve ~$0.8M a year for 2 engineers and 2 sales hires;  "
                  "(3) adopt the quarterly re-entry triggers on page 13.", False, INK)])], size=11, anchor=MSO_ANCHOR.MIDDLE, label="decisions")

# ================================================================= SLIDE 3: hypothesis test
s = new_slide("We began with the founders' hypothesis and tested the five things that would have to be true for it to hold; only market growth survives",
              tracker="Approach: hypothesis test",
              source="Board briefing pack; Parcelbird analysis. Verdict: green = holds, red = fails on the evidence in the briefing pack.")
text(s, LM, 1.7, CW, 0.4, [dict(runs=[("Initial hypothesis (founders' view): ", True, NAVY),
                                       ("\"Launch Parcelbird Now in three cities; with density, contribution per order turns positive by month 18.\"", False, INK)])],
     size=12, label="hyp")
rows = [["", "What would have to be true", "What the evidence shows", "Verdict", "Page"],
        ["Market", "Demand is growing fast", "US quick-commerce GMV grew 41.5% a year, 2022–25 ($1.8B → $5.1B); every year was +38% or more", "", "4"],
        ["Unit economics", "Orders make money at performance we can achieve", "−$2.67 per order before site costs at benchmark median; positive only if AOV, promotions, rider productivity and density all beat the best site observed", "", "5–7"],
        ["Customers", "Customers stay and order enough to repay their acquisition cost", "22% still ordering in month 3, at 3.1 orders a month; $173 of acquisition cost per retained customer is never repaid at benchmark economics", "", "9"],
        ["Capital", "It can be funded from current cash with ≥12 months runway at all times", "$9.5M of $12.0M needed to month 18; runway rule broken by month ~1–11; no new round expected", "", "10"],
        ["Right to win", "Our software know-how gives an operating edge, and operating does not hurt the core business", "Our pop-up ran below the benchmark median on every lever; pipeline grocers who want their own fast delivery would become competitors", "", "8, 11"]]
cwid = [1.55, 2.95, 5.6, 1.35, 0.78]
table(s, LM, 2.2, cwid, [0.36] + [0.68] * 5, rows, size=10.5, label="hyp table",
      aligns={4: PP_ALIGN.CENTER})
verdicts = [("ok", "Holds"), ("bad", "Fails"), ("bad", "Fails"), ("bad", "Fails"), ("bad", "Fails")]
for i, (k, l) in enumerate(verdicts):
    y = 2.2 + 0.36 + i * 0.68 + 0.19
    status(s, LM + sum(cwid[:3]) + 0.08, y, 1.3, k, l)
rect(s, LM, 6.2, CW, 0.62, fill=PANEL)
text(s, LM + 0.15, 6.22, CW - 0.3, 0.58, [dict(runs=[("Revised answer: ", True, NAVY),
     ("do not launch. Growth alone does not make the case — the incumbents prove a growing market can still lose money on every order. "
      "We then tested the alternatives (pages 11–12): focusing on software is the only option that meets the board's constraints.", False, INK)])],
     size=11.5, anchor=MSO_ANCHOR.MIDDLE, label="revised")

# ================================================================= SLIDE 4: market
s = new_slide("Quick-commerce demand is growing ~42% a year, but the scaled incumbents lose money on every order and one is already retreating",
              tracker="1  It would lose money  ·  Market",
              source="Board briefing pack, Tables 1–2 and section 5. Growth rates, CAGR and EBITDA margins are Parcelbird calculations.")
# column chart
text(s, LM, 1.75, 6.0, 0.3, "US quick-commerce grocery GMV, $ billions", size=12, bold=True, color=INK)
vals = [("2022", 1.8), ("2023", 2.6), ("2024", 3.6), ("2025", 5.1)]
cx, cy0, ch = LM + 0.3, 5.9, 3.2   # baseline y, chart height for max 6
scale = ch / 6.0
bw, gap = 0.85, 0.55
for i, (yr, v) in enumerate(vals):
    x = cx + i * (bw + gap)
    hgt = v * scale
    rect(s, x, cy0 - hgt, bw, hgt, fill=BLUE)
    text(s, x - 0.2, cy0 - hgt - 0.32, bw + 0.4, 0.28, f"${v:.1f}B", size=11, bold=True, align=PP_ALIGN.CENTER, check=False)
    text(s, x - 0.2, cy0 + 0.05, bw + 0.4, 0.28, yr, size=10.5, color=INK2, align=PP_ALIGN.CENTER, check=False)
    if i > 0:
        g = v / vals[i - 1][1] - 1
        xm = x - gap / 2 - 0.35
        text(s, xm, 2.15, 0.7, 0.26, f"+{g:.0%}", size=10, color=INK2, align=PP_ALIGN.CENTER, check=False)
line(s, cx - 0.1, cy0, cx + 4 * bw + 3 * gap + 0.1, cy0, color=MUTED, w=0.75)
text(s, LM, 2.15, 1.2, 0.26, "Year-on-year:", size=9, color=MUTED, check=False)
rect(s, LM + 0.3, 2.75, 1.9, 0.58, fill=PANEL)
text(s, LM + 0.3, 2.75, 1.9, 0.58, [dict(t="CAGR 2022–25", s=9, c=INK2), dict(t="41.5% a year", b=True, s=13, c=NAVY, sb=0)],
     align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, label="cagr")
text(s, LM, 6.3, 6.0, 0.5, "(5.1 ÷ 1.8)^(1/3) − 1 = 41.5%. The founders' \"over 40% a year\" is confirmed.", size=9.5, color=INK2, label="cagr calc")
# right: incumbents
RX = 7.1
text(s, RX, 1.75, 5.7, 0.3, "Incumbent operators, 2025", size=12, bold=True)
rows = [["Operator", "Revenue", "EBITDA", "EBITDA margin", "Contribution per order"],
        ["Zipcart (national)", "$1,200M", "−$310M", "−26%", "−$1.90"],
        ["QuickBasket (regional)", "$210M", "−$96M", "−46%", "−$3.40"]]
table(s, RX, 2.12, [1.75, 0.9, 0.85, 0.95, 1.23], [0.5, 0.42, 0.42], rows, size=10.5, header_size=9.5, label="incumbents",
      aligns={1: PP_ALIGN.RIGHT, 2: PP_ALIGN.RIGHT, 3: PP_ALIGN.RIGHT, 4: PP_ALIGN.RIGHT},
      colors={(1, 2): BAD, (2, 2): BAD, (1, 3): BAD, (2, 3): BAD, (1, 4): BAD, (2, 4): BAD})
text(s, RX, 3.65, 5.68, 2.6, [
    dict(t="What this tells the board", b=True, c=NAVY, s=12),
    dict(t="Scale has not fixed the economics: a national operator with $1.2B of revenue still loses $1.90 on each order before any overhead.", bullet=True),
    dict(t="The regional model is worse and shrinking: QuickBasket closed 4 of its 11 cities (36%) in 2025.", bullet=True),
    dict(t="\"Nobody owns the Midwest\" is more plausibly a sign of poor economics in mid-size cities than of an open prize.", bullet=True),
    dict(t="Growth is therefore necessary but not sufficient; the question is whether Parcelbird can earn money per order (next pages).", bullet=True)],
    size=11, spacing=6, label="market so-what")

# ================================================================= SLIDE 5: waterfall
s = new_slide("At benchmark-median performance each order loses $2.67 before site costs and $6.17 after; riders alone consume 22% of the basket",
              tracker="1  It would lose money  ·  Unit economics",
              source="Board briefing pack, Table 3 (median of 14 Parcelbird-software sites, 2025). Contribution = per-order revenue less variable costs, before site fixed costs. Parcelbird analysis.")
text(s, LM, 1.72, 8.2, 0.3, "Per-order economics at benchmark-median inputs, $ per order", size=12, bold=True)
# geometry
x0, y_top, y_bot = LM + 0.1, 2.35, 5.75
vmax, vmin = 12.0, -7.0
def Y(v):
    return y_top + (vmax - v) / (vmax - vmin) * (y_bot - y_top)
n = len(WF_MED); bw = 0.62; step = 0.9
run = 0.0
line(s, x0 - 0.05, Y(0), x0 + n * step, Y(0), color=MUTED, w=0.75)
text(s, x0 - 0.5, Y(0) - 0.13, 0.45, 0.26, "$0", size=9, color=MUTED, align=PP_ALIGN.RIGHT, check=False)
prev_end = None
for i, (lab, v) in enumerate(WF_MED):
    x = x0 + i * step + (step - bw) / 2
    if v == "T":
        lo, hi = min(0, run), max(0, run); col = NAVY; val = run
    else:
        start = run; run = round(run + v, 2)
        lo, hi = min(start, run), max(start, run); col = BLUE if v > 0 else ORANGE; val = v
    rect(s, x, Y(hi), bw, max(Y(lo) - Y(hi), 0.01), fill=col)
    lbl = (f"+{val:.2f}" if val > 0 else f"−{abs(val):.2f}")
    ty = Y(hi) - 0.27 if (v == "T" and val >= 0) or (v != "T" and v > 0) else Y(lo) + 0.02
    text(s, x - 0.2, ty, bw + 0.4, 0.25, lbl, size=10.5, bold=True, align=PP_ALIGN.CENTER,
         color=(BAD if (v == "T" and val < 0) else INK), check=False)
    if i < n - 1:
        line(s, x + bw, Y(run), x + step, Y(run), color=MUTED, w=0.5)
    text(s, x0 + i * step - 0.02, 5.95, step + 0.04, 0.55, lab, size=8.5, color=INK2, align=PP_ALIGN.CENTER, label="wf label")
# legend
lx = LM + 0.1
for j, (c, l) in enumerate([(BLUE, "Adds to profit"), (ORANGE, "Cost"), (NAVY, "Subtotal / result")]):
    rect(s, lx + j * 1.6, 6.62, 0.16, 0.16, fill=c)
    text(s, lx + j * 1.6 + 0.2, 6.56, 1.35, 0.28, l, size=9, color=INK2, check=False)
# right panel
RX = 8.85
rect(s, RX, 1.75, SW - LM - RX, 5.05, fill=PANEL)
text(s, RX + 0.15, 1.85, SW - LM - RX - 0.3, 4.9, [
    dict(t="The benchmark is consistent with what incumbents report", b=True, c=NAVY, s=11.5),
    dict(t="−$2.67 sits between Zipcart (−$1.90) and QuickBasket (−$3.40).", bullet=True, sb=3),
    dict(t="Rider cost is the biggest lever", b=True, c=NAVY, s=11.5, sb=10),
    dict(t="$17.75 ÷ 2.4 orders = $7.40 per order, 22% of a $34 basket — more than the $6.03 left after goods margin, fee, promotions and picking.", bullet=True, sb=3),
    dict(t="What it would take to break even", b=True, c=NAVY, s=11.5, sb=10),
    dict(t="Contribution only: AOV of $46.70 (best site: $42) or 3.75 orders per rider-hour (best: 3.0).", bullet=True, sb=3),
    dict(t="Contribution and site costs at 900 orders/day: AOV of $63.", bullet=True, sb=3),
    dict(t="Calc: break-even AOV = (−1.99 + 3.10 + 1.30 + 7.40) ÷ (27% − 6%) = $46.70; adding $3.50 of site cost gives $63.36.", s=9, c=INK2, sb=8)],
    size=10.5, label="wf right")

# ================================================================= SLIDE 6: scenarios
s = new_slide("The plan turns positive only by beating the best site ever observed on all four levers at once; no site has combined even the best two",
              tracker="1  It would lose money  ·  The founders' plan",
              source="Board briefing pack, Table 3 and section 7. Benchmark ranges: 1.9–3.0 orders per rider-hour, 400–1,400 orders per site per day. Best AOV and best density come from different sites. Parcelbird analysis.")
rows = [["Lever", "Columbus pop-up", "Benchmark median", "Best observed", "Founders' plan", "Plan vs best observed"],
        ["Average order value", "$31", "$34", "$42", "$45", "+7%, above any site"],
        ["Promotions, % of AOV", "12%", "6%", "6%", "2%", "One-third of every site"],
        ["Orders per rider-hour", "2.1", "2.4", "3.0", "3.5", "+17%, above benchmark range"],
        ["Orders per site per day", "280", "900", "1,400", "1,800", "+29%, above benchmark range"],
        ["Contribution per order", "−$6.21", "−$2.67", "+$0.49", "+$3.77", ""],
        ["Site fixed cost per order", "−$6.36", "−$3.50", "−$2.25", "−$1.75", ""],
        ["Site-level result per order", "−$12.57", "−$6.17", "−$1.76", "+$2.02", "Only positive column"]]
cwid = [2.25, 1.25, 1.35, 1.25, 1.3, 2.25]
fills = {(r, 4): RGBColor(0xE8, 0xF1, 0xFC) for r in range(1, 8)}
for c in range(6):
    fills[(7, c)] = fills.get((7, c), PANEL) if c != 4 else RGBColor(0xE8, 0xF1, 0xFC)
colors = {}
for r in (5, 6, 7):
    for c in (1, 2, 3, 4):
        colors[(r, c)] = BAD if rows[r][c].startswith("−") else OK
bolds = {(7, c): True for c in range(6)}
table(s, LM, 1.8, cwid, [0.5] + [0.43] * 7, rows, size=10.5, header_size=9.5, label="scen table", fills=fills, colors=colors, bolds=bolds,
      aligns={1: PP_ALIGN.CENTER, 2: PP_ALIGN.CENTER, 3: PP_ALIGN.CENTER, 4: PP_ALIGN.CENTER})
line(s, LM, 1.8 + 0.5 + 4 * 0.43, LM + sum(cwid), 1.8 + 0.5 + 4 * 0.43, color=NAVY, w=1.25)
RX = LM + sum(cwid) + 0.3
rect(s, RX, 1.8, SW - LM - RX, 3.51, fill=PANEL)
text(s, RX + 0.12, 1.88, SW - LM - RX - 0.24, 3.4, [
    dict(t="Reading the table", b=True, c=NAVY, s=11.5),
    dict(t="The \"best observed\" column is itself hypothetical: it pairs the best AOV and best density from different sites. It still loses $1.76 per order.", bullet=True),
    dict(t="The plan assumes performance outside the observed range on rider productivity and density, and promotions at one-third of any site's level.", bullet=True),
    dict(t="The month-18 profit claim rests on these inputs, not on evidence of them.", bullet=True)],
    size=10.5, spacing=6, label="scen right")
text(s, LM, 5.45, CW, 1.4, [
    dict(t="How each column is calculated ($ per order, benchmark median shown)", b=True, c=NAVY, s=11),
    dict(t="Contribution = AOV × 27% goods margin + $1.99 delivery fee − AOV × promotions % − $3.10 picking − $17.75 ÷ orders per rider-hour − $1.30 payment & packaging", bullet=True, sb=3),
    dict(t="Median: 9.18 + 1.99 − 2.04 − 3.10 − 7.40 − 1.30 = −$2.67.   Site fixed cost per order = $1.15M ÷ (900 × 365) = $3.50  →  site-level result −$6.17", bullet=True, sb=3),
    dict(t="Plan: 12.15 + 1.99 − 0.90 − 3.10 − 5.07 − 1.30 = +$3.77;  $1.15M ÷ (1,800 × 365) = $1.75  →  +$2.02.   Pop-up uses its own $0.65M annualised fixed cost.", bullet=True, sb=3)],
    size=10, label="scen calc")

# ================================================================= SLIDE 7: sensitivity
s = new_slide("Resetting a single lever, either basket size or rider productivity, to the benchmark median wipes out the plan's site-level profit",
              tracker="1  It would lose money  ·  Sensitivity",
              source="Board briefing pack, Table 3 and section 11. Rider-pay uplifts are illustrative: the pack gives no figure for the proposed minimum pay standards. Parcelbird analysis.")
text(s, LM, 1.72, 8.0, 0.3, "Site-level result per order under the founders' plan, changing one assumption at a time, $", size=12, bold=True)
items = [("Founders' plan as modelled", 2.02, "ref"),
         ("Density at median (900 orders/day)", 0.27, ""),
         ("Promotions at median (6% of AOV)", 0.22, ""),
         ("Rider productivity at median (2.4/hr)", -0.31, ""),
         ("AOV at median ($34)", -0.73, ""),
         ("Rider cost +10% (minimum pay rules)", 1.51, "pay"),
         ("Rider cost +20% (minimum pay rules)", 1.00, "pay"),
         ("All levers capped at best observed, promotions kept at 2%", -0.08, "combo"),
         ("All levers at benchmark median", -6.17, "combo")]
lab_w = 3.6; zx = LM + lab_w + 3.0   # zero x
unit = 0.55  # inches per $
y = 2.2; rh = 0.44
line(s, zx, y - 0.05, zx, y + rh * len(items) + 0.55, color=MUTED, w=0.75)
text(s, zx - 0.3, y - 0.3, 0.6, 0.25, "$0", size=9, color=MUTED, align=PP_ALIGN.CENTER, check=False)
for i, (lab, v, kind) in enumerate(items):
    yy = y + i * rh + (0.25 if i >= 5 else 0) + (0.25 if i >= 7 else 0)
    text(s, LM, yy, lab_w, rh, lab, size=10, color=INK, anchor=MSO_ANCHOR.MIDDLE, bold=(kind == "ref"), label="sens lab")
    col = NAVY if kind == "ref" else (BLUE if v >= 0 else ORANGE)
    w = abs(v) * unit
    bx = zx if v >= 0 else zx - w
    rect(s, bx, yy + 0.1, max(w, 0.02), rh - 0.2, fill=col)
    lbl = f"+{v:.2f}" if v >= 0 else f"−{abs(v):.2f}"
    if v >= 0:
        text(s, bx + w + 0.05, yy, 0.8, rh, lbl, size=10, bold=True, anchor=MSO_ANCHOR.MIDDLE, check=False)
    else:
        text(s, bx - 0.85, yy, 0.8, rh, lbl, size=10, bold=True, color=BAD, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.RIGHT, check=False)
# group labels
text(s, LM, y + 5 * rh + 0.01, 4, 0.24, "Labour-rule risk", size=8.5, color=MUTED, bold=True, check=False)
text(s, LM, y + 7 * rh + 0.26, 4, 0.24, "Combinations", size=8.5, color=MUTED, bold=True, check=False)
text(s, LM, y + 0 * rh - 0.22, 4, 0.24, "Single levers", size=8.5, color=MUTED, bold=True, check=False)
RX = 9.35
rect(s, RX, 1.75, SW - LM - RX, 5.05, fill=PANEL)
text(s, RX + 0.15, 1.85, SW - LM - RX - 0.3, 4.9, [
    dict(t="The margin of safety is thin", b=True, c=NAVY, s=11.5),
    dict(t="+$2.02 is 4% of a $45 basket. Moving AOV from $45 to $34 removes $2.75 per order; moving riders from 3.5 to 2.4 per hour removes $2.33.", bullet=True, sb=3),
    dict(t="Being as good as the best site is not enough", b=True, c=NAVY, s=11.5, sb=10),
    dict(t="Even with the plan's 2% promotions, capping AOV, rider productivity and density at the best observed values leaves −$0.08.", bullet=True, sb=3),
    dict(t="Labour rules hit the biggest cost line", b=True, c=NAVY, s=11.5, sb=10),
    dict(t="Two of three cities are weighing minimum pay. Each +$1 an hour costs $0.29 per order at 3.5 orders/hr and $0.42 at the 2.4 median.", bullet=True, sb=3)],
    size=10.5, label="sens right")

# ================================================================= SLIDE 8: pop-up
s = new_slide("Our own Columbus pop-up performed below the benchmark median on every lever and lost about $12.60 on each order",
              tracker="1  It would lose money  ·  Columbus pop-up test",
              source="Board briefing pack, section 7 and Table 3. Week-1 and week-6 volumes derived assuming steady 18% weekly growth summing to 11,800 orders. Parcelbird analysis.")
rows = [["Six-week pop-up, autumn 2026", "Pop-up", "Benchmark median", "Gap to median"],
        ["Average order value", "$31", "$34", "−9%"],
        ["Promotions, % of AOV", "12%", "6%", "2× the median"],
        ["Orders per rider-hour", "2.1", "2.4", "−13%"],
        ["Orders per site per day (average)", "280", "900", "−69%"],
        ["Contribution per order", "−$6.21", "−$2.67", "−$3.54"],
        ["Site-level result per order", "−$12.57", "−$6.17", "−$6.40"]]
table(s, LM, 1.8, [2.95, 1.2, 1.5, 1.55], [0.45] + [0.45] * 6, rows, size=10.5, header_size=9.5, label="popup table",
      aligns={1: PP_ALIGN.CENTER, 2: PP_ALIGN.CENTER, 3: PP_ALIGN.CENTER},
      colors={(5, 1): BAD, (5, 2): BAD, (6, 1): BAD, (6, 2): BAD, (5, 3): BAD, (6, 3): BAD},
      bolds={(6, c): True for c in range(4)}, fills={(6, c): PANEL for c in range(4)})
# stat tiles under table
tiles = [("≈ $148k", "estimated six-week loss\n11,800 orders × −$12.57"), ("≈ 410 / day", "week-6 exit run-rate,\nstill 45% of the median"), ("12%", "of AOV spent on promotions\nto drive 18% weekly growth")]
tw = (7.2 - 0.3) / 3
for i, (big, small) in enumerate(tiles):
    x = LM + i * (tw + 0.15)
    rect(s, x, 5.15, tw, 1.3, fill=PANEL)
    text(s, x + 0.1, 5.25, tw - 0.2, 0.5, big, size=20, bold=True, color=NAVY, check=False)
    text(s, x + 0.1, 5.78, tw - 0.2, 0.62, small, size=9.5, color=INK2, label="tile")
RX = 8.1
text(s, RX, 1.78, SW - LM - RX, 5.0, [
    dict(t="What the test does and does not show", b=True, c=NAVY, s=12),
    dict(t="Fair caveat: a temporary six-week site is early on the density curve, and orders were still growing 18% a week (≈180 a day in week 1 to ≈410 in week 6).", bullet=True),
    dict(t="But volume only spreads fixed cost. The −$6.21 lost before site costs comes from a small basket, heavy promotions and slow riders, which density alone does not cure.", bullet=True),
    dict(t="Growth was bought: promotions at 12% of AOV and first-order credits. Without them the 18% weekly growth cannot be assumed to persist.", bullet=True),
    dict(t="Implication for the right-to-win test", b=True, c=NAVY, s=12, sb=12),
    dict(t="Running other grocers' dark stores did not translate into running our own better: the pop-up underperformed the 14 customer sites our software already serves.", bullet=True)],
    size=10.5, spacing=6, label="popup right")

# ================================================================= SLIDE 9: customers
s = new_slide("Pop-up customers churn fast and order less than weekly, so their $38 acquisition cost is never repaid at benchmark economics",
              tracker="1  It would lose money  ·  Customers",
              source="Board briefing pack, sections 6–8. Payback ignores orders by churned customers in months 1–2 and any churn after month 3; the two partly offset. Parcelbird analysis.")
tiles = [("$38", "customer acquisition cost\n(paid social, first-order credits)"),
         ("22%", "of customers still ordering\nin month three"),
         ("3.1", "orders a month per\nretained customer (< weekly)"),
         ("$173", "acquisition cost per retained\ncustomer ($38 ÷ 22%)")]
tw = (CW - 0.45) / 4
for i, (big, small) in enumerate(tiles):
    x = LM + i * (tw + 0.15)
    rect(s, x, 1.78, tw, 1.25, fill=PANEL)
    text(s, x + 0.12, 1.83, tw - 0.24, 0.5, big, size=22, bold=True, color=NAVY if i < 3 else BAD, check=False)
    text(s, x + 0.12, 2.4, tw - 0.24, 0.6, small, size=10, color=INK2, label="cust tile")
text(s, LM, 3.25, 7.3, 0.3, "Months for a retained customer to repay $173 of acquisition cost", size=12, bold=True)
rows = [["Scenario", "Contribution per order", "Per retained customer per month (× 3.1)", "Months to repay $173"],
        ["Founders' plan", "+$3.77", "+$11.68", "≈ 15"],
        ["Best observed", "+$0.49", "+$1.53", "≈ 113"],
        ["Benchmark median", "−$2.67", "−$8.26", "Never"],
        ["Columbus pop-up", "−$6.21", "−$19.26", "Never"]]
table(s, LM, 3.62, [2.0, 1.6, 2.2, 1.5], [0.55, 0.42, 0.42, 0.42, 0.42], rows, size=10.5, header_size=9.5, label="payback",
      aligns={1: PP_ALIGN.CENTER, 2: PP_ALIGN.CENTER, 3: PP_ALIGN.CENTER},
      colors={(3, 1): BAD, (3, 2): BAD, (3, 3): BAD, (4, 1): BAD, (4, 2): BAD, (4, 3): BAD})
text(s, LM, 6.0, 7.3, 0.8, "Calc: plan $3.77 × 3.1 orders = $11.68 a month; $173 ÷ $11.68 ≈ 15 months after month 3, i.e. ≈ 18 months from acquisition, even on the founders' inputs.",
     size=9.5, color=INK2, label="payback calc")
RX = 8.3
rect(s, RX, 3.25, SW - LM - RX, 3.0, fill=PANEL)
text(s, RX + 0.15, 3.33, SW - LM - RX - 0.3, 2.85, [
    dict(t="Stated intent overstates real use", b=True, c=NAVY, s=12),
    dict(t="Survey: 44% of 1,500 Columbus residents aged 25–39 said they would use 15-minute delivery \"at least weekly\".", bullet=True),
    dict(t="Behaviour: 22% of acquired customers were still ordering in month three, at 3.1 orders a month, below once a week (4.3).", bullet=True),
    dict(t="The bases differ, but the direction is clear: the group still ordering is half the survey's 44%, and even it orders less than weekly. The survey also sampled only 25–39-year-olds, likely the keenest users.", bullet=True)],
    size=10.5, spacing=6, label="survey")

# ================================================================= SLIDE 10: capital
s = new_slide("Even on the founders' own numbers the launch breaks the 12-month runway rule within a year; at benchmark economics it would exhaust our cash",
              tracker="2  We cannot afford it  ·  Capital and runway",
              source="Board briefing pack, sections 1, 3 and 9. Runway = cash ÷ current monthly burn; the plan's $9.5M is spread evenly over 18 months because phasing was not provided. Parcelbird analysis.")
text(s, LM, 1.72, 6.6, 0.3, "Runway under the founders' $9.5M plan, two readings of the pack", size=12, bold=True)
rows = [["", "A: $9.5M on top of today's software burn", "B: $9.5M is the whole company's need (most favourable)"],
        ["Monthly burn", "$0.40M + $9.5M ÷ 18 = $0.93M", "$9.5M ÷ 18 = $0.53M"],
        ["Cash needed to keep 12 months of runway", "12 × $0.93M = $11.1M", "12 × $0.53M = $6.3M"],
        ["Runway rule breached", "Month ~1\n($12.0M − $11.1M) ÷ $0.93M", "Month ~11\n($12.0M − $6.3M) ÷ $0.53M"],
        ["Cash at month 18", "−$4.7M: cash runs out in month ~13", "$2.5M: ~6 months of runway left"]]
table(s, LM, 2.1, [1.9, 2.4, 2.4], [0.62, 0.5, 0.55, 0.65, 0.6], rows, size=10, header_size=9.5, label="runway",
      colors={(3, 1): BAD, (3, 2): BAD, (4, 1): BAD, (4, 2): BAD}, bolds={(3, 1): True, (3, 2): True})
text(s, LM, 5.2, 6.7, 1.6, [
    dict(t="Either way the plan fails the board's two constraints", b=True, c=NAVY, s=11.5),
    dict(t="The rule is \"at least 12 months of runway at all times\"; both readings break it before month 18.", bullet=True),
    dict(t="The lead investor calls a new round for a delivery operator \"unlikely in this market\", so there is no backstop if ramp-up is slower.", bullet=True)],
    size=10.5, spacing=5, label="runway so-what")
# right: bars annual site P&L nine sites
RX = 7.55
text(s, RX, 1.72, SW - LM - RX, 0.55, "Annual site-level profit of nine mature sites, $M, vs. $12.0M cash in the bank", size=12, bold=True, label="bars head")
bars = [("Founders' plan", 11.9, ""), ("Best observed", -8.1, "0.7× our cash"), ("Benchmark median", -18.2, "1.5× our cash")]
unit = 0.085; zx = RX + 1.65 + 18.2 * unit + 0.05; y = 2.45
line(s, zx, y - 0.05, zx, y + 3 * 0.72 + 0.05, color=MUTED, w=0.75)
text(s, zx - 0.3, y + 3 * 0.72 + 0.07, 0.6, 0.25, "$0", size=9, color=MUTED, align=PP_ALIGN.CENTER, check=False)
for i, (lab, v, note) in enumerate(bars):
    yy = y + i * 0.72
    w = abs(v) * unit
    bx = zx if v >= 0 else zx - w
    text(s, RX, yy + 0.1, 1.6, 0.48, lab, size=10, anchor=MSO_ANCHOR.MIDDLE, check=False)
    rect(s, bx, yy + 0.12, w, 0.44, fill=BLUE if v >= 0 else ORANGE)
    lbl = (f"+${v:.1f}M" if v >= 0 else f"−${abs(v):.1f}M")
    if v >= 0:
        text(s, bx + w + 0.05, yy + 0.1, 1.0, 0.48, lbl, size=10.5, bold=True, anchor=MSO_ANCHOR.MIDDLE, check=False)
    else:
        text(s, bx + 0.02, yy + 0.1, w - 0.04, 0.48, lbl, size=10.5, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE, check=False)
        text(s, zx + 0.08, yy + 0.1, 1.4, 0.48, note, size=10, color=BAD, bold=True, anchor=MSO_ANCHOR.MIDDLE, check=False)
rect(s, RX, 5.2, SW - LM - RX, 1.6, fill=PANEL)
text(s, RX + 0.15, 5.27, SW - LM - RX - 0.3, 1.5, [
    dict(t="The $9.5M budget only holds if the plan's economics hold", b=True, c=NAVY, s=11),
    dict(t="9 sites × site-level result × orders a year. Median: 9 × −$6.17 × 328,500 = −$18.2M a year, 1.5× our cash, on top of $5.4M capex.", bullet=True, sb=3),
    dict(t="Best observed: 9 × −$1.76 × 511,000 = −$8.1M. Plan: 9 × +$2.02 × 657,000 = +$11.9M.", bullet=True, sb=3)],
    size=10, label="bars so-what")

# ================================================================= SLIDE 11: options
s = new_slide("Of three options, only focusing on the software business keeps 12 months of runway and a path to profit within current cash",
              tracker="3  Software is the better use of the cash  ·  Options",
              source="Board briefing pack; Parcelbird analysis. Option B assumes one permanent site at benchmark-median economics for 12 months ($1.15M fixed cost, $0.6M capex), run alongside option C's software plan.")
hdr = ["Criterion", "A. Launch Parcelbird Now as planned\n9 dark stores, 3 cities", "B. One permanent pilot site\nColumbus, 12 months, plus software plan", "C. Focus on software\nincl. store-based fast-delivery tools for grocers"]
rows = [hdr,
        ["Path to profit within current cash", "Only if all four levers beat the best site observed", "Pilot loses ≈$2.0M a year at median; delays software break-even", "Yes: cash break-even ≈ month 26 (60% growth), ≈ month 36 (40%)"],
        ["Lowest runway (rule: ≥ 12 months)", "Breached by month ~1 to ~11", "≈ 10 months at 60% growth: breached", "≈ 24 months at 60% growth; ≈ 18 at 40%"],
        ["Cash at risk", "$9.5M budget; up to $18M a year of losses at median", "≈ $2.6M ($0.6M capex + ≈$2.0M loss)", "≈ $0.8M a year for four hires"],
        ["Fit with grocer customers", "Competes with them", "Signals intent to compete", "Serves their wish to launch fast delivery from existing stores"],
        ["What we learn", "Expensive proof of the plan's inputs", "Repeats the pop-up; we already see 14 sites' data", "Keeps watching 14+ customer sites at no cost"],
        ["Assessment", "Not recommended", "Not recommended", "Recommended"]]
cwid = [2.3, 3.3, 3.3, 3.33]
fills = {(r, 3): RGBColor(0xE8, 0xF1, 0xFC) for r in range(1, 7)}
fills[(0, 3)] = BLUE
colors = {(2, 1): BAD, (2, 2): BAD, (6, 1): BAD, (6, 2): BAD, (6, 3): OK}
bolds = {(6, 1): True, (6, 2): True, (6, 3): True}
table(s, LM, 1.8, cwid, [0.62, 0.62, 0.55, 0.62, 0.55, 0.55, 0.42], rows, size=10.5, header_size=10, label="options",
      fills=fills, colors=colors, bolds=bolds)
text(s, LM, 5.85, CW, 0.95, [
    dict(t="Why not a smaller test?  ", b=True, c=NAVY, s=11),
    dict(t="A single permanent site answers the wrong question: density is the uncertainty least able to rescue the economics (page 7), and the pop-up plus 14 customer sites already show where the levers sit. "
           "At ≈$2.6M it would take the lowest runway to ≈10 months even if software grows at 60%.", sb=2)],
    size=10.5, label="options note")

# ================================================================= SLIDE 12: software path
s = new_slide("The software business can reach cash break-even in about 26 months within current cash, and still does if growth slows to 40%",
              tracker="3  Software is the better use of the cash  ·  Path to profitability",
              source="Board briefing pack, sections 1 and 10. Indicative model, Parcelbird analysis: costs fixed at today's level (implied by $4.1M ARR and $0.4M monthly burn) plus $0.8M a year of hires; revenue = ARR; 81% gross margin.")
text(s, LM, 1.72, 7.4, 0.3, "Projected cash balance, software-only plan, $M by month", size=12, bold=True)
import math
def sw(growth, months=48):
    arr = 4.1; opex = 4.1 + 4.8 - 4.1 * 0.19 + 0.8; c = 12.0; pts = [(0, 12.0)]
    mg = (1 + growth) ** (1 / 12)
    for m in range(1, months + 1):
        arr *= mg; c -= (opex - 0.81 * arr) / 12; pts.append((m, c))
    return pts
gx0, gx1, gy0, gy1 = LM + 0.55, LM + 6.9, 2.25, 6.0   # plot box
ymax = 18.0
def PX(m): return gx0 + m / 48 * (gx1 - gx0)
def PY(v): return gy1 - max(v, 0) / ymax * (gy1 - gy0)
for v in (0, 6, 12, 18):
    line(s, gx0, PY(v), gx1, PY(v), color=RULE if v else MUTED, w=0.5 if v else 0.75)
    text(s, gx0 - 0.55, PY(v) - 0.13, 0.5, 0.26, f"{v}", size=9, color=MUTED, align=PP_ALIGN.RIGHT, check=False)
for m in (0, 12, 24, 36, 48):
    text(s, PX(m) - 0.3, gy1 + 0.05, 0.6, 0.25, f"{m}", size=9, color=MUTED, align=PP_ALIGN.CENTER, check=False)
text(s, gx1 - 1.2, gy1 + 0.27, 1.2, 0.25, "Month", size=9, color=MUTED, align=PP_ALIGN.RIGHT, check=False)
series = [(0.60, BLUE, "60% growth (today's rate)"), (0.40, ORANGE, "40% growth"), (0.30, AQUA, "30% growth (stress)")]
for g, col, lab in series:
    pts = sw(g)
    fb = s.shapes.build_freeform(I(PX(pts[0][0])), I(PY(pts[0][1])), scale=1.0)
    fb.add_line_segments([(I(PX(m)), I(PY(v))) for m, v in pts[1:]], close=False)
    shp = fb.convert_to_shape()
    shp.fill.background(); shp.line.color.rgb = col; shp.line.width = Pt(2.25)
    end = pts[-1][1]
    text(s, gx1 + 0.05, PY(end) - 0.14, 1.3, 0.28, f"${end:.1f}M", size=9.5, bold=True, check=False)
# break-even markers (trough)
for g, m_be, col in [(0.60, 26, BLUE), (0.40, 36, ORANGE)]:
    v = dict(sw(g))[m_be]
    rect(s, PX(m_be) - 0.06, PY(v) - 0.06, 0.12, 0.12, fill=col, line=WHITE, shape=MSO_SHAPE.OVAL, lw=1.5)
    text(s, PX(m_be) - 0.9, PY(v) - 0.5, 1.8, 0.42, [dict(t=f"break-even month {m_be}", sb=0), dict(t=f"low point ${v:.1f}M", sb=0)], size=8.5, color=INK2, align=PP_ALIGN.CENTER, check=False)
# legend
for j, (g, col, lab) in enumerate(series):
    lx = gx0 + j * 2.15
    line(s, lx, 6.62, lx + 0.3, 6.62, color=col, w=2.25)
    text(s, lx + 0.35, 6.5, 1.85, 0.26, lab, size=9, color=INK2, check=False)
RX = 8.35
rect(s, RX, 1.75, SW - LM - RX, 5.05, fill=PANEL)
text(s, RX + 0.15, 1.83, SW - LM - RX - 0.3, 4.95, [
    dict(t="Break-even needs ≈ $11.0M ARR", b=True, c=NAVY, s=11.5),
    dict(t="Costs ≈ $8.9M a year ÷ 81% gross margin. At 60% growth: 4.1 × 1.6^t = 11.0 → t ≈ 2.1 years.", bullet=True, sb=3),
    dict(t="Growth already in sight", b=True, c=NAVY, s=11.5, sb=9),
    dict(t="9 late-stage deals × $96k = $0.86M ARR, 35% of the $2.46M needed for another 60% year; the full pipeline of 37 is $3.55M.", bullet=True, sb=3),
    dict(t="A product move, not an operator move", b=True, c=NAVY, s=11.5, sb=9),
    dict(t="Pipeline grocers want fast delivery from existing stores; serving them avoids the $1.15M a year dark-store cost.", bullet=True, sb=3),
    dict(t="Where it breaks", b=True, c=NAVY, s=11.5, sb=9),
    dict(t="At 30% growth the runway rule is breached around month 23 unless costs are cut; this sets the guardrail on page 13.", bullet=True, sb=3)],
    size=10.5, label="sw right")

# ================================================================= SLIDE 13: recommendation
s = new_slide("We ask the board to decline the launch, fund four software hires, and revisit quick commerce only when measurable triggers are met",
              tracker="Recommendation and next steps",
              source="Parcelbird analysis. Trigger thresholds derived from pages 5–12.")
blocks = [
    ("Decide today (January 2027)", [
        "Do not launch Parcelbird Now in 2027; commit no dark-store capex.",
        "Approve ≈$0.8M a year for 2 engineers and 2 sales hires.",
        "Adopt a cash guardrail: ≥12 months runway reviewed monthly, with a cost plan ready if trailing growth falls below 40%."]),
    ("Next 90 days", [
        "Close the 9 late-stage deals ($0.86M ARR).",
        "Scope store-based fast-delivery tools (picking, batching, rider dispatch) with pipeline grocers that want to launch.",
        "Turn the pop-up's lessons (promotions, rider productivity) into product features for customers.",
        "Build a quarterly benchmark from the 14+ customer sites to track the triggers."]),
    ("Revisit quick commerce only if all hold", [
        "A customer site sustains positive site-level profit for two quarters (today the best combination is −$1.76 per order).",
        "Rider minimum-pay rules in the target cities are settled and costed.",
        "The software business is cash-flow positive, or committed funding keeps ≥12 months runway after the launch budget."]),
]
bw3 = (CW - 0.4) / 3
for i, (head, items_) in enumerate(blocks):
    x = LM + i * (bw3 + 0.2)
    rect(s, x, 1.8, bw3, 0.55, fill=NAVY if i < 2 else BLUE)
    text(s, x + 0.12, 1.8, bw3 - 0.24, 0.55, head, size=13, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE, label="rec head")
    rect(s, x, 2.35, bw3, 3.3, fill=PANEL)
    text(s, x + 0.15, 2.5, bw3 - 0.3, 3.1, [dict(t=f"{k+1}.  {t}") for k, t in enumerate(items_)], size=11.5, spacing=10, label="rec items")
rect(s, LM, 5.85, CW, 0.95, fill=None, line=NAVY, lw=1)
text(s, LM + 0.15, 5.88, CW - 0.3, 0.9, [dict(runs=[("Why this is low-regret:  ", True, NAVY),
     ("declining now keeps the $12.0M, the grocer relationships and the data. Our software already sees the economics of 14+ fast-delivery sites every quarter, "
      "so we will know if and when the triggers are met without funding the experiment ourselves; a dark store can still be opened later for about $0.6M of capex.", False, INK)])],
     size=11, anchor=MSO_ANCHOR.MIDDLE, label="low regret")

# ================================================================= SLIDE 14: risks
s = new_slide("The recommendation's main risks are slower software growth and ceding the Midwest; both are smaller and more manageable than the launch's downside",
              tracker="Risks, assumptions and uncertainties",
              source="Board briefing pack, sections 4, 10 and 11; Parcelbird analysis.")
rows = [["Risk or uncertainty", "Why it matters", "Size, where known", "Mitigation"],
        ["Software growth slows", "Break-even and the runway low point depend on growth", "Break-even ≈ m26 at 60%, ≈ m36 at 40%; rule breached ≈ m23 at 30%", "Monthly tracking; pre-agreed cost plan below 40% growth"],
        ["A rival captures the Midwest while we wait", "The founders' case is first-mover advantage", "Incumbents lose $1.90–$3.40 per order; QuickBasket is retreating", "Be in the market as supplier to grocers' own fast delivery; triggers allow re-entry"],
        ["Our unit-economic inputs are wrong", "Benchmarks are 14 sites; mid-size Midwest density is unproven", "Even best-observed inputs lose $1.76 per order", "Re-run the model each quarter on customer-site data"],
        ["Rider minimum-pay rules", "Rider cost is the largest per-order cost", "+$1 an hour = $0.42 per order at median productivity", "Sell batching and dispatch efficiency as product value to grocers"],
        ["Founder focus and morale", "The founders' proposal is declined", "Not quantifiable", "Channel ambition into the fast-delivery product line"]]
table(s, LM, 1.8, [2.45, 3.05, 3.4, 3.33], [0.4] + [0.6] * 5, rows, size=10.5, header_size=10, label="risks")
rect(s, LM, 5.45, CW, 1.38, fill=PANEL)
text(s, LM + 0.15, 5.5, CW - 0.3, 1.3, [
    dict(t="Key assumptions behind the numbers", b=True, c=NAVY, s=11),
    dict(t="Benchmark medians from 14 customer sites represent what a new Parcelbird site would achieve; the delivery fee is already net of payment cost.", bullet=True, sb=3),
    dict(t="The plan's $9.5M is spread evenly over 18 months; runway is measured as cash ÷ current monthly burn.", bullet=True, sb=3),
    dict(t="Software costs stay at today's implied level (≈$8.1M a year excluding cost of goods) plus $0.8M of hires; ARR converts to revenue at 81% gross margin.", bullet=True, sb=3)],
    size=10, label="assumptions")

# ================================================================= APPENDIX 1
s = new_slide("Appendix 1: per-order economics by scenario; only the founders' plan inputs produce a profit, and the pop-up is the weakest case",
              tracker="Appendix",
              source="Board briefing pack, Table 3 and section 7; Parcelbird analysis. Totals may differ by $0.01 because of rounding.")
rows = [["$ per order", "Formula", "Columbus pop-up", "Benchmark median", "Best observed", "Founders' plan"],
        ["Gross margin on goods", "AOV × 27%", "+8.37", "+9.18", "+11.34", "+12.15"],
        ["Delivery fee, net", "Given", "+1.99", "+1.99", "+1.99", "+1.99"],
        ["Promotions", "AOV × promo %", "−3.72", "−2.04", "−2.52", "−0.90"],
        ["Picking and packing", "Given", "−3.10", "−3.10", "−3.10", "−3.10"],
        ["Rider cost", "$17.75 ÷ orders per rider-hour", "−8.45", "−7.40", "−5.92", "−5.07"],
        ["Payment processing and packaging", "Given", "−1.30", "−1.30", "−1.30", "−1.30"],
        ["Contribution per order", "Sum of the above", "−6.21", "−2.67", "+0.49", "+3.77"],
        ["Site fixed cost per order", "Annual fixed cost ÷ (orders/day × 365)", "−6.36", "−3.50", "−2.25", "−1.75"],
        ["Site-level result per order", "Contribution − fixed cost", "−12.57", "−6.17", "−1.76", "+2.02"],
        ["Site-level result per site per year", "× orders per year", "−$1.28M", "−$2.03M", "−$0.90M", "+$1.33M"],
        ["Break-even orders per site per day", "Fixed cost ÷ (contribution × 365)", "Never", "Never", "6,390", "836"]]
colors = {}
for r in range(1, 12):
    for c in range(2, 6):
        if rows[r][c].startswith("−") or rows[r][c] == "Never":
            colors[(r, c)] = BAD
bolds = {(r, c): True for r in (7, 9) for c in range(6)}
fills = {(r, c): PANEL for r in (7, 9) for c in range(6)}
table(s, LM, 1.78, [2.75, 3.13, 1.55, 1.6, 1.6, 1.6], [0.4] + [0.38] * 11, rows, size=10, header_size=9.5, label="app1",
      colors=colors, bolds=bolds, fills=fills, aligns={2: PP_ALIGN.RIGHT, 3: PP_ALIGN.RIGHT, 4: PP_ALIGN.RIGHT, 5: PP_ALIGN.RIGHT})
text(s, LM, 6.4, CW, 0.5, "Inputs: AOV $31 / $34 / $42 / $45; promotions 12% / 6% / 6% / 2%; orders per rider-hour 2.1 / 2.4 / 3.0 / 3.5; orders per day 280 / 900 / 1,400 / 1,800; fixed cost $0.65M (pop-up, annualised) / $1.15M.",
     size=9.5, color=INK2, label="app1 note")

# ================================================================= APPENDIX 2
s = new_slide("Appendix 2: the runway, pop-up and software-path figures rest on simple calculations from the pack's numbers",
              tracker="Appendix",
              source="Board briefing pack, sections 1, 7, 8, 9 and 10; Parcelbird analysis.")
blocks = [
    ("Runway under the plan (page 10)", [
        "Reading A: burn = $0.40M + $9.5M ÷ 18 = $0.928M a month. 12-month floor = $11.1M, reached after (12.0 − 11.1) ÷ 0.928 ≈ 0.9 months. Cash = 0 after 12.0 ÷ 0.928 ≈ 12.9 months.",
        "Reading B: burn = $0.528M a month. Floor = $6.3M, reached after (12.0 − 6.3) ÷ 0.528 ≈ 10.7 months. Month 18 cash = $2.5M = 6.2 months at the $0.4M software burn."]),
    ("Pop-up ramp (page 8)", [
        "Six weeks at 18% weekly growth summing to 11,800: week 1 = 11,800 × 0.18 ÷ (1.18^6 − 1) ≈ 1,250 orders (≈180 a day); week 6 = 1,250 × 1.18^5 ≈ 2,860 (≈410 a day).",
        "Loss ≈ 11,800 × −$12.57 ≈ −$148k (annualised fixed cost applied per order)."]),
    ("Software path (pages 11–12)", [
        "Today's total costs ≈ $4.1M revenue + $4.8M annual burn = $8.9M, of which cost of goods 19% × $4.1M = $0.78M and operating costs $8.12M; plus $0.8M hires = $8.92M.",
        "Monthly ARR growth = (1 + annual growth)^(1/12); monthly burn = ($8.92M − 81% × ARR) ÷ 12. Break-even ARR = 8.92 ÷ 0.81 = $11.0M.",
        "Results: 60% → break-even month 26, low point $5.4M, minimum runway ≈24 months; 40% → month 36, $2.7M, ≈18 months; 30% → rule breached ≈ month 23.",
        "Option B adds $0.6M capex at month 0 and $2.03M of site loss over months 1–12: minimum runway ≈10 months at 60% growth."])]
y = 1.78
heights = [1.05, 0.9, 1.7]
for (head, items_), h in zip(blocks, heights):
    text(s, LM, y, CW, h, [dict(t=head, b=True, c=NAVY, s=11.5)] + [dict(t=t, bullet=True, sb=3) for t in items_], size=10, label="app2")
    y += h + 0.2

# ================================================================= APPENDIX 3
s = new_slide("Appendix 3: where the briefing pack was ambiguous we made explicit choices, favouring the launch case where in doubt",
              tracker="Appendix",
              source="Prepared without access to the briefing team; these choices are open for the board to challenge.")
rows = [["Topic", "Ambiguity", "Choice made", "Effect on the answer"],
        ["Contribution definition", "Founders' \"contribution profit\" is not defined", "Per-order revenue less variable costs, before site fixed costs; consistent with incumbents' figures", "None: the conclusion holds at either level"],
        ["$9.5M cash need", "Unclear whether it includes the software business's $0.4M monthly burn", "Show both readings (A additive, B all-in)", "Both breach the runway rule"],
        ["Best observed column", "Best AOV and best density came from different sites", "Treated as an upper bound, not an achievable case", "Favours the launch"],
        ["Pop-up fixed cost", "Temporary site cost $0.65M vs $1.15M permanent", "Used the pop-up's own figure for the pop-up column", "Favours the launch"],
        ["Rider minimum pay", "No figure for the proposed standards", "Illustrative +10% / +20% and per-$1 sensitivities", "Downside only"],
        ["Customer payback", "Orders in months 1–2 and later churn unknown", "Retained customers only, no further churn", "Roughly neutral"],
        ["Software cost base", "Opex not given", "Derived from ARR and burn; held flat apart from $0.8M of hires", "Indicative; flagged on page 12"]]
table(s, LM, 1.78, [2.1, 3.3, 3.9, 2.93], [0.4] + [0.6] * 7, rows, size=10, header_size=9.5, label="app3")

# ----------------------------------------------------------------- save + checks
out = sys.argv[1]
prs.save(out)
bad = [(n, l, round(a, 1), round(b, 1)) for (n, l, a, b) in CHECKS if a > b + 0.5]
print("saved", out, "slides", len(prs.slides))
print("OVERFLOW candidates:", len(bad))
for b in bad:
    print("  ", b)
