"""Builds the Boreal Autonomy board deck. Every figure traces to evidence/briefing-pack.md
and the calculations in model.py (same folder)."""
import re
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION

OUT = sys.argv[1] if len(sys.argv) > 1 else "Boreal_OEM_Exclusivity_Board_Deck.pptx"

def rgb(h): return RGBColor.from_string(h)
NAVY, INK, GRAY, MUTED = "0B2545", "1F2937", "4B5563", "6B7280"
LIGHT, LINE, WHITE = "F3F4F6", "D1D5DB", "FFFFFF"
BLUE, BLUE_T, BLUE_TT = "2A78D6", "B7D3F6", "E3EEFC"
ORANGE, ORANGE_T = "EB6834", "FBD9CA"
RED, AMBER, GREEN = "B42318", "B54708", "1E7B34"
RED_T, AMBER_T, GREEN_T = "FDE4E1", "FDF0D5", "DDF3E2"
FONT = "Calibri"

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]
SECTIONS = ["Value", "Evidence", "Alternatives", "Path forward"]
page = [0]


# ---------- helpers ----------
def _runs(par, text, size, color, bold=False, italic=False):
    """Supports **bold** markup inside text."""
    parts = re.split(r"(\*\*.+?\*\*)", text)
    for p in parts:
        if not p:
            continue
        r = par.add_run()
        b = p.startswith("**") and p.endswith("**")
        r.text = p[2:-2] if b else p
        f = r.font
        f.name, f.size, f.bold, f.italic = FONT, Pt(size), bool(bold or b), bool(italic)
        f.color.rgb = rgb(color)


def text(slide, x, y, w, h, paras, size=12, color=INK, bold=False, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, fill=None, line=None, bullets=False, space=4, italic=False,
         margin=0.05, shape=MSO_SHAPE.RECTANGLE):
    shp = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill:
        shp.fill.solid(); shp.fill.fore_color.rgb = rgb(fill)
    else:
        shp.fill.background()
    if line:
        shp.line.color.rgb = rgb(line); shp.line.width = Pt(0.75)
    else:
        shp.line.fill.background()
    shp.shadow.inherit = False
    tf = shp.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    for side in ("margin_left", "margin_right"):
        setattr(tf, side, Inches(margin + 0.03))
    tf.margin_top = tf.margin_bottom = Inches(margin)
    if isinstance(paras, str):
        paras = [paras]
    for i, p in enumerate(paras):
        par = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        par.alignment = align
        par.space_after = Pt(space)
        t = p
        if bullets and not p.startswith("§"):
            t = "•  " + p
        if t.startswith("§"):
            t = t[1:]
        _runs(par, t, size, color, bold, italic)
    return shp


def rect(slide, x, y, w, h, fill, line=None, shape=MSO_SHAPE.RECTANGLE):
    shp = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.fill.solid(); shp.fill.fore_color.rgb = rgb(fill)
    if line:
        shp.line.color.rgb = rgb(line)
    else:
        shp.line.fill.background()
    shp.shadow.inherit = False
    return shp


def hline(slide, x, y, w, color=LINE, weight=0.75):
    ln = slide.shapes.add_connector(1, Inches(x), Inches(y), Inches(x + w), Inches(y))
    ln.line.color.rgb = rgb(color); ln.line.width = Pt(weight)


def new_slide(title, section=None, source=None):
    s = prs.slides.add_slide(BLANK)
    page[0] += 1
    if section is not None:
        # section tracker
        x = 0.5
        for i, name in enumerate(SECTIONS):
            active = (i + 1) == section
            t = text(s, x, 0.18, 1.9, 0.28, f"{i+1}  {name.upper()}", size=8.5,
                     color=NAVY if active else "9CA3AF", bold=active, margin=0.0)
            if active:
                rect(s, x + 0.03, 0.45, 1.2, 0.04, BLUE)
            x += 1.95
    text(s, 0.5, 0.55, 12.3, 0.95, title, size=21, color=NAVY, bold=True,
         anchor=MSO_ANCHOR.MIDDLE, margin=0.0)
    hline(s, 0.5, 1.52, 12.33, LINE, 1)
    if source:
        text(s, 0.5, 7.03, 11.3, 0.3, "Source: " + source, size=8, color=MUTED, margin=0.0)
    text(s, 12.2, 7.03, 0.63, 0.3, str(page[0]), size=8, color=MUTED, align=PP_ALIGN.RIGHT, margin=0.0)
    return s


def table(slide, x, y, w, rows, col_w, size=10.5, header_fill=NAVY, row_h=0.4,
          fills=None, bold_first_col=False, header_size=None, aligns=None):
    nr, nc = len(rows), len(rows[0])
    shp = slide.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(w), Inches(row_h * nr))
    tbl = shp.table
    # remove built-in style banding
    tblPr = shp._element.graphic.graphicData.tbl.tblPr
    tblPr.set("bandRow", "0"); tblPr.set("firstRow", "0")
    tot = sum(col_w)
    for i, cw in enumerate(col_w):
        tbl.columns[i].width = Inches(w * cw / tot)
    for r in range(nr):
        tbl.rows[r].height = Inches(row_h)
        for c in range(nc):
            cell = tbl.cell(r, c)
            cell.margin_left = cell.margin_right = Inches(0.07)
            cell.margin_top = cell.margin_bottom = Inches(0.04)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            val = rows[r][c]
            f = None
            if r == 0 and header_fill:
                f = header_fill
            elif fills and fills.get((r, c)):
                f = fills[(r, c)]
            elif fills and fills.get((r, None)):
                f = fills[(r, None)]
            cell.fill.solid(); cell.fill.fore_color.rgb = rgb(f or WHITE)
            paras = val if isinstance(val, list) else [val]
            tf = cell.text_frame
            tf.word_wrap = True
            for i, p in enumerate(paras):
                par = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                if aligns:
                    par.alignment = aligns[c]
                is_head = bool(r == 0 and header_fill)
                col = WHITE if (is_head and header_fill == NAVY) else INK
                _runs(par, str(p), header_size or size if is_head else size, col,
                      bold=is_head or (bold_first_col and c == 0))
    return tbl


def tag(slide, x, y, w, label, kind):
    colors = {"fail": (RED_T, RED), "partial": (AMBER_T, AMBER), "hold": (GREEN_T, GREEN),
              "neutral": (LIGHT, GRAY)}
    bg, fg = colors[kind]
    text(slide, x, y, w, 0.3, label, size=9.5, color=fg, bold=True, fill=bg,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, margin=0.02,
         shape=MSO_SHAPE.ROUNDED_RECTANGLE)


def style_chart(chart, size=10):
    chart.font.name = FONT
    chart.font.size = Pt(size)
    chart.font.color.rgb = rgb(GRAY)


def axis_style(ax, visible=True, grid=False, fmt=None):
    ax.visible = visible
    ax.has_major_gridlines = grid
    if grid:
        ax.major_gridlines.format.line.color.rgb = rgb("E5E7EB")
        ax.major_gridlines.format.line.width = Pt(0.5)
    ax.format.line.color.rgb = rgb(LINE)
    ax.tick_labels.font.size = Pt(10)
    ax.tick_labels.font.color.rgb = rgb(GRAY)
    if fmt:
        ax.tick_labels.number_format = fmt
        ax.tick_labels.number_format_is_linked = False


# =====================================================================
# 1. Title
s = prs.slides.add_slide(BLANK); page[0] += 1
rect(s, 0, 0, 13.333, 7.5, NAVY)
rect(s, 0.8, 2.05, 0.08, 2.6, BLUE)
text(s, 1.1, 1.9, 11, 0.4, "BOREAL AUTONOMY  |  BOARD OF DIRECTORS  |  APRIL 2027 DECISION", size=12,
     color="9EC5F4", bold=True, margin=0)
text(s, 1.1, 2.35, 11.2, 1.6, "Don't give exclusivity away before it is earned: sign a nonexclusive OEM pilot "
     "now and make North American exclusivity conditional on certification and audited volumes",
     size=28, color=WHITE, bold=True, margin=0)
text(s, 1.1, 4.1, 11, 0.6, "Decision question: should Boreal grant North American exclusivity to an OEM for its "
     "industrial robot navigation software in 2027?", size=14, color="CDE2FB", margin=0)
text(s, 1.1, 6.5, 11.5, 0.5, "Board pre-read prepared November 2026 from the board briefing pack only (synthetic "
     "benchmark data). All $ figures are undiscounted; no NPV is computed, as the board requested.",
     size=10, color="9CA3AF", margin=0)

# =====================================================================
# 2. Executive summary
s = new_slide("Executive summary: reject exclusivity at signing; pilot nonexclusively and switch exclusivity on "
              "only when certification and audited volumes show it pays",
              source="Board briefing pack §1–7; team analysis (calculations on slides 4–7, 12–13 and appendix)")
text(s, 0.5, 1.65, 12.33, 0.92,
     "**Recommendation:** Decline Option X as drafted. Sign Option N, a 12-month nonexclusive pilot at $350 per robot, "
     "and agree up front the gates under which Option M (limited exclusivity) takes effect: certification passed, "
     "two audited quarters at about 9,000 robots a year, and contract protections signed.",
     size=12.5, color=WHITE, fill=NAVY, anchor=MSO_ANCHOR.MIDDLE, margin=0.12)
rows = [
    ("1  The deal is worth less than it is being presented as",
     "The $2.0M is a **recoupable advance**, not extra revenue: three-year OEM cash is **$8.7M, not $10.7M**. After "
     "$80/robot support, $0.9M/yr engineering, the $0.45M assessment and displaced direct sales, exclusivity is worth "
     "**+$2.2M to +$2.8M at plan** but only **−$0.04M to +$0.55M at 65% volumes**."),
    ("2  The evidence the board requires for irreversible exclusivity does not exist yet",
     "Lab uptime is **98.8% against a 99.5% production bar**. The third-party assessment has not started. OEM volumes are "
     "unaudited, and the 14,000 'booked devices' are a forecast. The growth claim rests on correlation. The draft lacks "
     "audit rights, a royalty floor, release triggers and code escrow."),
    ("3  The phased N→M structure beats every alternative",
     "It earns **$50 more per robot**, keeps the direct channel (**~$1.48M** of gross margin on new ARR in 2028), and "
     "matches X's value even if the OEM ships **24–32% fewer robots**. It holds cash at least **$0.55M above the $2.6M "
     "buffer** in the worst case, and it fails none of the board's conditions."),
    ("4  Gates, signposts and next steps make the decision reversible",
     "Start the $0.45M assessment now; it is on the critical path for every OEM route. Convert to exclusivity only after "
     "certification and audited shipments of at least 2,250 robots a quarter. If the OEM insists on exclusivity at "
     "signing, walk away and fall back to direct sales plus the integration-firm pilot."),
]
y = 2.7
for head, body in rows:
    text(s, 0.5, y, 3.6, 1.0, head, size=12.5, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, margin=0.02)
    text(s, 4.25, y, 8.58, 1.0, body, size=11.5, color=INK, anchor=MSO_ANCHOR.MIDDLE, margin=0.02)
    hline(s, 0.5, y + 1.03, 12.33)
    y += 1.07

# =====================================================================
# 3. Hypothesis test
s = new_slide("Of six conditions that would have to hold for exclusivity at signing to be right, only one partly "
              "holds, so the 'don't sign yet' hypothesis stands",
              source="Board briefing pack §1–6; team analysis")
text(s, 0.5, 1.62, 12.33, 0.64,
     "**Initial hypothesis (stated before testing):** Boreal should not grant exclusivity at signing; a nonexclusive or "
     "milestone deal captures the OEM upside without giving up the direct channel. **Test:** state what must hold for "
     "the opposite answer (Option X) to be right, then check each condition against the pack.",
     size=11, color=INK, fill=LIGHT, anchor=MSO_ANCHOR.MIDDLE, margin=0.1)
hdr = ["", "For exclusivity at signing to be right, it must be true that…", "What the evidence shows", "Verdict"]
data = [
    ["Value", "1. The $2.0M signing payment adds value on top of royalties",
     "It is an advance credited against the first $2.0M of royalties, and the partner can demand an offset. 3-yr cash is $8.7M either way (slide 4)"],
    ["", "2. Exclusivity creates value even in the low case and with realistic channel overlap",
     "+$2.2–2.8M at plan; −$0.04M to +$0.55M at 65% volumes with Sales' 30–70% overlap (slides 5–7)"],
    ["Evidence", "3. The product is production-ready in the OEM's hardware",
     "98.8% lab uptime vs 99.5% required; no loaded-warehouse or collision-heavy test; assessment not started (slide 8)"],
    ["", "4. OEM volumes and the growth story are reliable enough to commit on",
     "Shipments unaudited; '14,000 booked devices' have no purchase orders; competitor evidence is correlational (slide 9)"],
    ["Alternatives", "5. Exclusivity is the only way to win the OEM's volume",
     "The OEM will consider Option N (nonexclusive, $350/robot) and Option M (gated exclusivity) (slides 11–12)"],
    ["Protection", "6. The contract protects Boreal if forecasts or certification miss",
     "No audit right, no royalty floor after the advance, no release triggers, no code escrow (slide 10)"],
]
verdicts = [("Does not hold", "fail"), ("Partly: plan case only", "partial"), ("Does not hold", "fail"),
            ("Does not hold", "fail"), ("Does not hold", "fail"), ("Does not hold", "fail")]
rows_ = [hdr] + [r + ["**" + v[0] + "**"] for r, v in zip(data, verdicts)]
vf = {(i + 1, 3): (AMBER_T if k == "partial" else RED_T) for i, (_, k) in enumerate(verdicts)}
table(s, 0.5, 2.38, 12.33, rows_, [1.15, 4.1, 5.6, 1.6], size=10, row_h=0.58, bold_first_col=True,
      fills=vf, aligns=[PP_ALIGN.LEFT] * 3 + [PP_ALIGN.CENTER])
text(s, 0.5, 6.55, 12.33, 0.45,
     "**Result:** the hypothesis survives, refined. The problem is exclusivity **before evidence**, not exclusivity "
     "itself, so the answer is a gated path to exclusivity rather than a flat 'no'.",
     size=10.5, color=NAVY, margin=0.02)

# =====================================================================
# 4. Advance mechanics
s = new_slide("The $2.0M is an advance on royalties, not extra revenue: three-year OEM cash is $8.7M, not the "
              "$10.7M the 'revenue win' framing implies", section=1,
              source="Board briefing pack §3 (forecast, advance terms); team analysis. $M, undiscounted.")
hdr = ["Case / year", "Robots shipped", "Royalties earned ($300)", "Advance credit applied",
       "Royalty cash received", "Total OEM cash (incl. $2.0M at signing)"]
R = [hdr,
     ["**Plan** 2027", "5,000", "1.50", "−1.50", "0.00", "2.00"],
     ["2028", "10,000", "3.00", "−0.50", "2.50", "2.50"],
     ["2029", "14,000", "4.20", "0.00", "4.20", "4.20"],
     ["**Plan total**", "**29,000**", "**8.70**", "**−2.00**", "**6.70**", "**8.70**"],
     ["**65% stress** 2027", "3,250", "0.98", "−0.98", "0.00", "2.00"],
     ["2028", "6,500", "1.95", "−1.03", "0.93", "0.93"],
     ["2029", "9,100", "2.73", "0.00", "2.73", "2.73"],
     ["**Stress total**", "**18,850**", "**5.66**", "**−2.00**", "**3.66**", "**5.66**"]]
fills = {(4, None): BLUE_TT, (8, None): BLUE_TT}
C = PP_ALIGN.CENTER
table(s, 0.5, 1.75, 8.4, R, [1.6, 1.1, 1.3, 1.3, 1.3, 1.8], size=10.5, row_h=0.47, fills=fills,
      aligns=[PP_ALIGN.LEFT, C, C, C, C, C])
text(s, 0.5, 6.1, 8.4, 0.8,
     "Reading the table: the advance is cash received early, then **netted out of 2028 royalty cash**. Total cash "
     "therefore always equals royalties earned. In the stress case, 2028 royalty cash falls to **$0.93M** because "
     "$1.03M of credit is still being recouped.", size=10.5, color=GRAY, margin=0.02)
text(s, 9.2, 1.75, 3.63, 4.95, [
    "**How the board should describe it**",
    "**Revenue = royalties earned** as qualifying robots ship and payment is collected: **$1.5M in 2027** at plan, "
    "not $3.5M.",
    "The $2.0M is a **minimum-guarantee liability** until it is earned. The partner can demand an offset if "
    "guaranteed performance is missed.",
    "The 'revenue win plus recurring royalties' framing **double-counts $2.0M**, overstating 3-year OEM income by "
    "**23%** ($10.7M vs $8.7M).",
    "**What the advance buys:** timing only. It brings $1.5–2.0M of cash forward into 2027, which Boreal does not "
    "need to stay above its buffer (slide 13)."],
    size=11, color=INK, fill=LIGHT, space=8, margin=0.15)

# =====================================================================
# 5. Waterfall
s = new_slide("After full costs, $3.00M of 2028 plan royalties shrinks to about $0.56M of incremental value, "
              "19% rather than the dashboard's 100%", section=1,
              source="Board briefing pack §3–5; team analysis. Lost direct margin = 50% (midpoint of Sales' 30–70% "
                     "overlap) × $1.8M ARR × 82% gross margin.")
cats = ["2028 royalties\n(10,000 × $300)", "Variable support\n(10,000 × $80)", "OEM-specific\nengineering",
        "OEM contribution", "Displaced direct\ngross margin", "Incremental\nvalue"]
base = [0, 2.20, 1.30, 0, 0.562, 0]
vis = [3.00, 0.80, 0.90, 1.30, 0.738, 0.562]
labels = ["$3.00M", "−$0.80M", "−$0.90M", "$1.30M", "−$0.74M", "$0.56M"]
cols = [BLUE, ORANGE, ORANGE, NAVY, ORANGE, NAVY]
cd = CategoryChartData(); cd.categories = cats
cd.add_series("base", base); cd.add_series("value", vis)
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_STACKED, Inches(0.4), Inches(1.7), Inches(8.3), Inches(5.2), cd)
ch = gf.chart; style_chart(ch); ch.has_legend = False
ch.plots[0].gap_width = 55; ch.plots[0].overlap = 100
sb, sv = ch.series[0], ch.series[1]
sb.format.fill.background(); sb.format.line.fill.background()
for i, p in enumerate(sv.points):
    p.format.fill.solid(); p.format.fill.fore_color.rgb = rgb(cols[i])
    dl = p.data_label; dl.has_text_frame = True; dl.text_frame.text = labels[i]
    dl.position = XL_LABEL_POSITION.INSIDE_END
    for r in dl.text_frame.paragraphs[0].runs:
        r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = rgb(WHITE)
axis_style(ch.value_axis, visible=False, grid=False)
ch.value_axis.maximum_scale = 3.2; ch.value_axis.minimum_scale = 0
axis_style(ch.category_axis)
text(s, 9.0, 1.75, 3.83, 5.1, [
    "**Three views of the same royalty**",
    "**CFO dashboard: 100% margin.** It counts only the $300 royalty.",
    "**Per robot: $220 (73%)** after $80 of support, before any fixed cost.",
    "**Complete incremental view: ~19% at plan.** That is $0.27–0.86M across 30–70% overlap.",
    "**At 65% volumes it turns negative:** $1.95M − $0.52M − $0.90M − $0.74M = **−$0.21M** in 2028.",
    "Exclusivity bars all new direct North American licences, including customers who buy other OEMs' robots. "
    "That forgone margin is a real cost of Option X, not of the OEM channel in general."],
    size=11, color=INK, fill=LIGHT, space=8, margin=0.15)

# =====================================================================
# 6. Sensitivity grid
s = new_slide("Over 2027–29, exclusivity is worth +$2.2–2.8M at plan volumes but only −$0.04M to +$0.55M if the "
              "OEM ships 65% of plan", section=1,
              source="Board briefing pack §3–4, §7; team analysis. Undiscounted; no NPV, per board instruction.")
text(s, 0.5, 1.65, 12.33, 0.42,
     "Option X three-year incremental value, $M = Σ(royalties − $80 × robots − $0.9M engineering) − $0.45M assessment "
     "− overlap × ($1.8M × 82%)", size=11, color=GRAY, margin=0.02)

def shade(v):
    if v >= 2: return BLUE_T
    if v >= 1: return BLUE_TT
    if v >= 0: return LIGHT
    return ORANGE_T

def grid(y, title, vals, note):
    text(s, 0.5, y, 12.33, 0.35, title, size=12, color=NAVY, bold=True, margin=0.02)
    hdr = ["OEM volume case (2027–29 robots)", "0% overlap\n(CEO view)", "30%\n(Sales low)", "50%\n(midpoint)",
           "70%\n(Sales high)", "100%\n(all displaced)"]
    rows_ = [hdr]
    fills = {}
    for r, (lab, vv) in enumerate(vals, start=1):
        rows_.append([lab] + [f"{v:+.2f}".replace("-", "−") for v in vv])
        for c, v in enumerate(vv, start=1):
            fills[(r, c)] = shade(v)
    table(s, 0.5, y + 0.38, 8.6, rows_, [2.6, 1.2, 1.2, 1.2, 1.2, 1.2], size=11.5, row_h=0.5,
          fills=fills, bold_first_col=True, header_size=10.5,
          aligns=[PP_ALIGN.LEFT, C, C, C, C, C])
    text(s, 9.35, y + 0.38, 3.48, 1.5, note, size=10.5, color=INK, margin=0.05)

grid(2.15, "A. Direct cohort counted in 2028 only (pack-grounded floor; favours Option X)",
     [("Plan (29,000)", [3.23, 2.79, 2.49, 2.20, 1.75]), ("65% stress (18,850)", [1.00, 0.55, 0.26, -0.04, -0.48])],
     ["Even on the most favourable reading, the low case leaves **at most $0.55M** of value for three years of "
      "irreversible exclusivity."])
grid(4.35, "B. Sensitivity: the lost 2028 direct customers would also have renewed in 2029 (churn not in pack)",
     [("Plan (29,000)", [3.23, 2.34, 1.75, 1.16, 0.28]), ("65% stress (18,850)", [1.00, 0.11, -0.48, -1.07, -1.96])],
     ["If direct ARR renews, as recurring revenue normally does, the low case **destroys up to $1.1M** at Sales' "
      "70% overlap."])
text(s, 0.5, 6.45, 12.33, 0.5,
     "Shading: dark blue ≥ $2M, light blue $1–2M, grey $0–1M, orange < $0. Costs assume full-year engineering from "
     "2027, which is conservative. If deployments start late in 2027, all OEM options gain equally and the ranking "
     "does not change.", size=9.5, color=MUTED, margin=0.02)

# =====================================================================
# 7. Breakeven
s = new_slide("Exclusivity breaks even only if the OEM ships 6,100–8,800 robots a year; the 65% case "
              "(6,500 in 2028) barely clears the most optimistic end", section=1,
              source="Board briefing pack §3–4; team analysis. Breakeven = ($0.9M + overlap × $1.476M) ÷ ($300 − $80).")
cats = ["Breakeven, 0% overlap", "Breakeven, 30% overlap", "Breakeven, 50% overlap", "Breakeven, 70% overlap",
        "Breakeven, 100% overlap", "OEM 2028: 65% stress", "OEM 2028: partner plan"]
vals = [4091, 6104, 7445, 8787, 10800, 6500, 10000]
cd = CategoryChartData(); cd.categories = cats; cd.add_series("Robots per year", vals)
gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(0.4), Inches(1.7), Inches(8.4), Inches(5.2), cd)
ch = gf.chart; style_chart(ch); ch.has_legend = False
ch.plots[0].gap_width = 45
ch.category_axis.reverse_order = True
axis_style(ch.category_axis)
axis_style(ch.value_axis, grid=True, fmt="#,##0")
ch.value_axis.maximum_scale = 12000; ch.value_axis.minimum_scale = 0
ch.value_axis.major_unit = 2000
ch.value_axis.tick_labels.font.size = Pt(9)
pl = ch.plots[0]; pl.has_data_labels = True
pl.data_labels.number_format = "#,##0"; pl.data_labels.number_format_is_linked = False
pl.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
pl.data_labels.font.size = Pt(10.5); pl.data_labels.font.bold = True
pl.data_labels.font.color.rgb = rgb(INK)
for i, p in enumerate(ch.series[0].points):
    p.format.fill.solid()
    p.format.fill.fore_color.rgb = rgb("9CA3AF" if i < 5 else (ORANGE if i == 5 else BLUE))
text(s, 9.05, 1.75, 3.78, 5.1, [
    "**How to read it**",
    "Grey bars show the annual OEM shipments needed for exclusivity to beat staying nonexclusive. Each robot "
    "contributes **$220**, which must cover **$0.9M** of engineering plus the displaced direct margin.",
    "At Sales' **30–70%** overlap, the hurdle is **6,100–8,800 robots a year**. The plan (10,000) clears it; the "
    "stress case (6,500) clears only the 30% end.",
    "Option M's proposed gate of **5,000 annualised is below every realistic breakeven**. It should rise to about "
    "**9,000** (2,250 per quarter) unless the scope excludes customers on other OEMs' robots.",
    "Under Option N, the OEM programme alone breaks even at **3,333 robots** ($0.9M ÷ $270), and the direct channel "
    "is untouched."],
    size=10.5, color=INK, fill=LIGHT, space=7, margin=0.15)

# =====================================================================
# 8. Readiness
s = new_slide("The software has not yet met the OEM's production bar, and Option X would make exclusivity "
              "binding at signing, about five months before certification at the earliest", section=2,
              source="Board briefing pack §2, §5; team analysis. Downtime hours assume 24/7 operation (8,760 h/yr).")
tiles = [("98.8%", "Lab uptime: 60 robots,\n12 weeks", BLUE), ("99.5%", "OEM production\nacceptance bar", NAVY),
         ("−58%", "Downtime cut still needed\n(105 → 44 h per robot-year)", ORANGE)]
x = 0.5
for big, small, col in tiles:
    rect(s, x, 1.75, 2.55, 1.75, LIGHT)
    rect(s, x, 1.75, 0.07, 1.75, col)
    text(s, x + 0.2, 1.82, 2.3, 0.85, big, size=34, color=NAVY, bold=True, margin=0)
    text(s, x + 0.2, 2.67, 2.3, 0.75, small, size=11, color=GRAY, margin=0)
    x += 2.7
text(s, 8.75, 1.75, 4.08, 2.95, [
    "**Not yet demonstrated**",
    "Safe-stop performance in a **fully loaded warehouse**",
    "**Collision-heavy peak** conditions (not in the trial)",
    "Uptime in the **OEM's production hardware**, not the lab",
    "Third-party security and safety assessment ($0.45M): **not started**",
    "Certification by September 2027 is an **engineering projection**, not a plan with a vendor in place"],
    size=10.5, color=INK, bullets=False, fill=LIGHT, space=5, margin=0.15)
# timeline
text(s, 0.5, 3.85, 8.0, 0.35, "Option X timing against the board's own condition", size=12, color=NAVY,
     bold=True, margin=0)
rect(s, 0.7, 4.95, 7.6, 0.06, LINE)
pts = [(0.7, "Nov 2026", "Today: assessment\nnot started", GRAY),
       (3.1, "Apr 2027", "Board meets; under X,\nexclusivity binds here", ORANGE),
       (5.8, "Sep 2027", "Earliest certification\n(projected)", BLUE),
       (8.1, "Dec 2027", "Plan assumes 5,000\nrobots shipped in 2027", GRAY)]
for px, d, lab, col in pts:
    rect(s, px - 0.11, 4.87, 0.22, 0.22, col, shape=MSO_SHAPE.OVAL)
    text(s, px - 0.9, 4.37, 1.8, 0.4, d, size=11, color=NAVY, bold=True, align=PP_ALIGN.CENTER, margin=0)
    text(s, px - 1.1, 5.18, 2.2, 0.6, lab, size=9.5, color=GRAY, align=PP_ALIGN.CENTER, margin=0)
text(s, 8.75, 4.85, 4.08, 1.95, [
    "**So what**",
    "The board requires documented uptime and safety validation in OEM hardware **before** irreversible "
    "exclusivity. Option X fails that condition by design.",
    "Production deployment cannot start until the assessment is complete, so the 2027 plan of 5,000 robots is at "
    "risk, and with it the advance's offset exposure."],
    size=10.5, color=WHITE, fill=NAVY, space=5, margin=0.15)
text(s, 0.5, 6.0, 8.0, 0.9,
     "The gap is closable but unproven: to reach 99.5%, downtime must fall from 1.2% to 0.5% of hours. Over the "
     "12-week trial that means about 24 → 10 hours per robot, under harsher conditions than the lab.",
     size=10.5, color=GRAY, margin=0.02)

# =====================================================================
# 9. Unverified claims
s = new_slide("The upside case rests on unaudited volumes, an untested 'fully incremental' claim and a "
              "correlational competitor analogy", section=2,
              source="Board briefing pack §2, §4–5; team analysis")
cols3 = [
    ("OEM volumes are a forecast, not a commitment",
     ["Quarterly shipment data are **not independently audited**, and the draft contract has **no audit right**.",
      "The '14,000 booked devices' have **no purchase orders**. Treat them as a 2029 forecast.",
      "The 2027 forecast of 5,000 assumes production shipments in a year when certification lands in September at "
      "the earliest.",
      "The board is unwilling to rely solely on verbal OEM launch forecasts."],
     "Impact: plan → 65% moves 3-yr value by **−$2.2M** (slide 6)"),
    ("Channel overlap is unknown, and it drives the answer",
     ["The CEO says the OEM channel is **0% overlap** (entirely incremental). Sales says **30–70%** of OEM buyers "
      "overlap with its pipeline.",
      "Neither view is backed by **customer-level identifiers**.",
      "Each 10 points of overlap is worth **~$0.15M a year** of displaced direct gross margin ($1.8M × 82% × 10%).",
      "The overlap can be measured during a nonexclusive pilot. It cannot be measured after exclusivity has "
      "closed the direct channel."],
     "Impact: 30% → 70% moves the breakeven from **6,100 to 8,800** robots/yr"),
    ("'Exclusivity caused competitors' growth' is not shown",
     ["Five competitors' exclusive OEM deals **coincided** with faster growth. That is a correlation.",
      "Those firms had **more marketing support, more mature products and higher market share** before they "
      "signed, so any of these could explain the growth.",
      "Boreal has none of these advantages yet: its product is uncertified and its leverage limited.",
      "No causal evidence is available, so we give this argument **zero weight** in the economics."],
     "Impact: no evidence that exclusivity itself adds volume over N"),
]
x = 0.5
for head, bl, foot in cols3:
    rect(s, x, 1.75, 3.95, 0.07, BLUE)
    text(s, x, 1.88, 3.95, 0.65, head, size=13, color=NAVY, bold=True, margin=0.02)
    text(s, x, 2.6, 3.95, 3.4, bl, size=11, color=INK, bullets=True, space=7, margin=0.02)
    text(s, x, 6.1, 3.95, 0.7, foot, size=10.5, color=NAVY, fill=BLUE_TT, anchor=MSO_ANCHOR.MIDDLE, margin=0.1)
    x += 4.19

# =====================================================================
# 10. Contract gaps
s = new_slide("As drafted, the contract leaves Boreal exposed on six terms, and its scope blocks the growing "
              "direct channel", section=2,
              source="Board briefing pack §2, §3, §6 (legal counsel and software team review); team analysis")
R = [["Term", "Draft agreement", "Risk to Boreal", "Required before any exclusivity"],
     ["Audit rights", "No clear right to audit reported shipments", "Royalties and volume gates rest on unaudited OEM reports",
      "Independent, shipment-level audit right; quarterly reports reconciled to invoices"],
     ["Royalty floor", "None once the $2.0M advance is used up", "Direct channel barred with no minimum income",
      "Annual minimum royalty; exclusivity lapses automatically if missed"],
     ["Release triggers", "No automatic release", "Locked in if the model is retired or certification slips",
      "Automatic release on model retirement, certification slip or missed minimums"],
     ["IP protection", "Source code delivered as freely reusable OEM IP", "Loss of Boreal's core asset and future leverage",
      "Source code escrow with narrow release conditions; no IP transfer"],
     ["Scope", "All new North American sales, including customers on other OEMs' robots", "Chief strategic opportunity cost; "
      "~$1.48M/yr of direct margin at risk", "Limit to the OEM's robot series; carve out existing and other-OEM customers"],
     ["Guarantee offset", "Partner can demand an offset if guaranteed performance is missed",
      "The $2.0M can claw back, e.g. if certification delays 2027 shipments", "Define the offset; cap it at the "
      "unearned balance; no offset for OEM-driven shortfalls"]]
fills = {(r, 3): GREEN_T for r in range(1, 7)}
table(s, 0.5, 1.75, 12.33, R, [1.5, 3.3, 3.5, 4.0], size=10.5, row_h=0.66, fills=fills, bold_first_col=True)
text(s, 0.5, 6.5, 12.33, 0.45,
     "Existing direct contracts cannot be terminated for convenience. Any exclusivity must apply only to **future new** "
     "North American robot sales, or Boreal faces unquantified contract claims.", size=10.5, color=NAVY, margin=0.02)

# =====================================================================
# 11. Options matrix
s = new_slide("Of the five routes, the phased N→M structure is the only one that keeps the OEM upside without "
              "an irreversible bet before the evidence exists", section=3,
              source="Board briefing pack §1, §4, §6; team analysis (values from slides 6, 12, 13)")
H = ["", "X: exclusive at signing", "N: 12-month nonexclusive pilot", "M: exclusivity after gates",
     "Direct sales only", "Defer until certified"]
R = [H,
     ["Indicative value, 2027–29",
      "+$2.2–2.8M plan; −$0.04 to +$0.55M at 65%",
      "Up to +$4.7M plan / +$1.9M at 65% if terms hold (upper bound)",
      "X-like upside, taken only once proven", "Keeps ~$1.48M/yr direct margin on 2028 new ARR; no OEM upside",
      "As direct, less the $0.45M assessment"],
     ["Low-case resilience", "Weak: thin margin, offset exposure", "Strong: no guarantee to recoup; $270/robot",
      "Strong: gates screen out the low case", "Strong", "Strong"],
     ["Reversibility", "None: 3 years, binding at signing", "High: 12 months", "High until the gates are met",
      "High", "High"],
     ["Board conditions*", "Fails the validation-first condition", "Meets all", "Meets all", "Meets all", "Meets all"],
     ["Deal risk with OEM", "Lowest: it is the OEM's ask", "Medium: offered by the OEM; price not guaranteed",
      "Medium: termination payment still open", "Forgoes the OEM", "High: OEM may choose another supplier"],
     ["Verdict", "Reject as drafted", "Recommend: phase 1", "Recommend: phase 2", "Fallback", "Fallback if N refused"]]
fills = {}
for r in range(1, 7):
    fills[(r, 2)] = BLUE_TT; fills[(r, 3)] = BLUE_TT
fills[(6, 1)] = RED_T; fills[(6, 2)] = GREEN_T; fills[(6, 3)] = GREEN_T; fills[(6, 4)] = LIGHT; fills[(6, 5)] = LIGHT
fills[(2, 1)] = RED_T; fills[(3, 1)] = RED_T; fills[(4, 1)] = RED_T
table(s, 0.5, 1.72, 12.33, R, [1.7, 2.2, 2.2, 2.1, 2.1, 2.0], size=10, row_h=0.68, fills=fills,
      bold_first_col=True, header_size=10.5)
text(s, 0.5, 6.55, 12.33, 0.45,
     "*Board conditions: validation in OEM hardware before irreversible exclusivity; existing licences protected; "
     "$2.6M liquidity buffer held. The integration firm's 1,200-robot nonexclusive pilot is a complement to N and to "
     "the fallbacks; X would likely bar it, as it covers new customers on other OEMs' robots. Its royalty terms are not in the pack.",
     size=9.5, color=MUTED, margin=0.02)

# =====================================================================
# 12. N vs X chart
s = new_slide("Nonexclusive terms would match exclusivity's value even if the OEM shipped 24–32% fewer robots "
              "without exclusivity", section=3,
              source="Board briefing pack §3–4, §6; team analysis. N assumes its $350 terms and partner volumes "
                     "persist for 3 years, which the OEM has not guaranteed.")
cd = CategoryChartData(); cd.categories = ["Partner plan (29,000 robots)", "65% stress (18,850 robots)"]
cd.add_series("X, 30% overlap", (2.79, 0.55))
cd.add_series("X, 70% overlap", (2.20, -0.04))
cd.add_series("N terms, same volumes", (4.68, 1.94))
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.4), Inches(1.7), Inches(8.2), Inches(5.2), cd)
ch = gf.chart; style_chart(ch)
ch.has_legend = True; ch.legend.position = XL_LEGEND_POSITION.TOP; ch.legend.include_in_layout = False
ch.legend.font.size = Pt(10.5)
pl = ch.plots[0]; pl.gap_width = 70; pl.overlap = -8
for sr, col in zip(ch.series, ["9CA3AF", ORANGE, BLUE]):
    sr.format.fill.solid(); sr.format.fill.fore_color.rgb = rgb(col)
    sr.invert_if_negative = False
pl.has_data_labels = True
pl.data_labels.number_format = '"$"0.00"M";"−$"0.00"M"'; pl.data_labels.number_format_is_linked = False
pl.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
pl.data_labels.font.size = Pt(11); pl.data_labels.font.bold = True; pl.data_labels.font.color.rgb = rgb(INK)
axis_style(ch.value_axis, grid=True, fmt='"$"0"M"')
ch.value_axis.minimum_scale = -1; ch.value_axis.maximum_scale = 5; ch.value_axis.major_unit = 1
axis_style(ch.category_axis)
from pptx.enum.chart import XL_TICK_LABEL_POSITION
ch.category_axis.tick_label_position = XL_TICK_LABEL_POSITION.LOW
text(s, 8.85, 1.75, 3.98, 5.1, [
    "**Why N wins on value per unit of risk**",
    "N pays **$350 vs $300** per robot ($270 vs $220 after support) and **does not displace** the direct channel.",
    "N matches X's three-year value at **22,000 robots** (30% overlap) or **19,800** (70%), against the 29,000 plan: "
    "**24–32% fewer robots**.",
    "In the stress case the cushion is **27–39%**.",
    "**Caveats:** the OEM may ship less without exclusivity, and it will not guarantee final pricing. Some OEM "
    "buyers would also substitute for direct buyers under N. The N bars are an upper bound; the volume cushion is "
    "the robust finding."],
    size=10.5, color=INK, fill=LIGHT, space=7, margin=0.15)

# =====================================================================
# 13. Liquidity
s = new_slide("Every route keeps cash above the $2.6M buffer; the advance's liquidity benefit is temporary and "
              "can be clawed back", section=3,
              source="Board briefing pack §2–3; team analysis. Headroom = $4.9M cash − $2.6M buffer + deal cash flows "
                     "to end-2027. Rest-of-business burn is not in the pack and is assumed to be covered by the buffer.")
cats = ["Direct sales only", "Defer: assessment only", "N: royalties collected in-year",
        "N: worst case, no 2027 royalty cash (lag)", "X: plan, advance in hand",
        "X: certification slips, $2.0M offset"]
vals = [2.30, 1.85, 2.30, 0.55, 2.55, 1.85]
cd = CategoryChartData(); cd.categories = cats; cd.add_series("Headroom above $2.6M buffer, end-2027 ($M)", vals)
gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(0.4), Inches(1.7), Inches(8.2), Inches(5.2), cd)
ch = gf.chart; style_chart(ch); ch.has_legend = False
ch.category_axis.reverse_order = True; ch.plots[0].gap_width = 45
axis_style(ch.category_axis); axis_style(ch.value_axis, grid=True, fmt='"$"0.0"M"')
ch.value_axis.minimum_scale = 0; ch.value_axis.maximum_scale = 3; ch.value_axis.major_unit = 0.5
pl = ch.plots[0]; pl.has_data_labels = True
pl.data_labels.number_format = '"$"0.00"M"'; pl.data_labels.number_format_is_linked = False
pl.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
pl.data_labels.font.size = Pt(11); pl.data_labels.font.bold = True; pl.data_labels.font.color.rgb = rgb(INK)
for i, p in enumerate(ch.series[0].points):
    p.format.fill.solid(); p.format.fill.fore_color.rgb = rgb(ORANGE if i == 3 else BLUE)
text(s, 8.85, 1.75, 3.98, 5.1, [
    "**Start:** $4.9M cash − $2.6M buffer = **$2.3M headroom**.",
    "**OEM routes spend** the $0.45M assessment, $0.9M of engineering and $80/robot of support ($0.40M at 5,000 "
    "robots) before royalty cash arrives.",
    "**N's tightest point is $0.55M**, if reporting lags push all 2027 royalties into 2028. Mitigations: monthly "
    "remittance, engineering phased to shipments, OEM-funded integration work.",
    "**X looks richest ($2.55M)**, but only because the advance is unearned. A certification slip plus an offset "
    "demand takes it back to $1.85M.",
    "**Liquidity does not require the advance.** It is not a reason to sign X."],
    size=10.5, color=INK, fill=LIGHT, space=7, margin=0.15)

# =====================================================================
# 14. Recommendation structure
s = new_slide("Recommendation: sign Option N now and pre-agree three gates that switch on limited exclusivity "
              "(Option M) once certification and audited volumes show it pays", section=4,
              source="Board briefing pack §2, §5–7; team analysis. Gate volume from slide 7 breakeven at 70% overlap "
                     "(8,787 robots/yr).")
phases = [("PHASE 0  |  Now → Apr 2027", "Prepare", [
               "Commission the $0.45M third-party security and safety assessment now",
               "Negotiate the N term sheet with the M gates pre-agreed",
               "Tag customers so OEM/direct overlap can be measured"], LIGHT, NAVY),
          ("PHASE 1  |  Apr 2027 → ~Q1 2028", "Option N: nonexclusive pilot", [
               "12 months, $350 per shipped robot, no advance",
               "Boreal keeps all direct and other-OEM rights",
               "Audit rights and monthly royalty reports from day one",
               "Existing licences untouched"], BLUE_TT, NAVY),
          ("PHASE 2  |  Earliest ~Q2 2028", "Option M: limited exclusivity", [
               "New North American sales of the OEM's robot series only",
               "Up to 3 years, with an annual minimum royalty",
               "Automatic release if minimums are missed, the model is retired or certification lapses",
               "Termination payment ≥ 1 year of displaced direct margin (~$1.5M)"], NAVY, WHITE)]
x = 0.5
for i, (hd, name, bl, fill, fg) in enumerate(phases):
    w = 3.55
    rect(s, x, 1.72, w, 2.55, fill)
    text(s, x + 0.1, 1.78, w - 0.2, 0.3, hd, size=9.5, color=fg if fill == NAVY else BLUE, bold=True, margin=0)
    text(s, x + 0.1, 2.07, w - 0.2, 0.4, name, size=13, color=fg, bold=True, margin=0)
    text(s, x + 0.1, 2.5, w - 0.2, 1.75, bl, size=10, color=fg if fill == NAVY else INK, bullets=True,
         space=3, margin=0)
    x += w + 0.84
    if i < 2:
        arr = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x - 0.74), Inches(2.75), Inches(0.62), Inches(0.5))
        arr.fill.solid(); arr.fill.fore_color.rgb = rgb(LINE); arr.line.fill.background()
text(s, 0.5, 4.4, 12.33, 0.35, "All three gates must be passed before Phase 2. Each is verifiable by the board, "
     "not by OEM assertion.", size=12, color=NAVY, bold=True, margin=0)
gates = [("Gate 1: Certification",
          "≥ 99.5% uptime in OEM production hardware in a fully loaded warehouse, including collision-heavy peaks; "
          "documented safe-stop; third-party assessment passed."),
         ("Gate 2: Verified demand",
          "Two consecutive **audited** quarters of ≥ 2,250 robots (~9,000/yr), at or above breakeven at 70% overlap. "
          "Accept the OEM's 5,000/yr gate only if other-OEM customers are carved out."),
         ("Gate 3: Contract protections",
          "Audit right, post-advance royalty floor, automatic release triggers, source code escrow, existing and "
          "other-OEM customers carved out, defined offset terms.")]
x = 0.5
for hd, body in gates:
    rect(s, x, 4.85, 3.98, 0.07, GREEN)
    text(s, x, 4.97, 3.98, 0.35, hd, size=12, color=GREEN, bold=True, margin=0.02)
    text(s, x, 5.33, 3.98, 1.6, body, size=10.5, color=INK, margin=0.02)
    x += 4.175

# =====================================================================
# 15. Negotiation plan
s = new_slide("Negotiate by trading price, scope and timing for evidence, and walk away from any form of "
              "exclusivity that binds at signing", section=4,
              source="Board briefing pack §1, §4, §6; team analysis")
cols3 = [
    ("Must-haves (walk away without them)", RED, [
        "No exclusivity before Gates 1–3 are met",
        "Existing direct contracts excluded; exclusivity covers future new sales only",
        "Independent shipment audit right",
        "Source code escrow; no transfer of reusable IP",
        "Automatic release on model retirement or certification slip"]),
    ("Tradeables (give to get)", AMBER, [
        "Royalty: concede from $350 toward $300 at conversion in return for a royalty floor",
        "Volume gate: accept 5,000/yr instead of ~9,000 if the scope excludes other-OEM customers",
        "Geography: narrower regions or named verticals first",
        "Term: shorter initial exclusivity (e.g. 2 years) with renewal on performance",
        "An advance at conversion, structured as a capped and clearly defined guarantee"]),
    ("Fallback if the OEM refuses (BATNA)", GREEN, [
        "Continue direct sales: ~$1.8M new ARR in 2028, ~$1.48M gross margin",
        "Take the integration firm's nonexclusive 1,200-robot pilot ($0.22M support budget, no guarantee)",
        "Complete certification anyway; return to the OEM with production evidence",
        "This loses the OEM's upside (+$2.2–2.8M at plan) but avoids the low-case downside"]),
]
x = 0.5
for hd, col, bl in cols3:
    rect(s, x, 1.75, 3.95, 0.07, col)
    text(s, x, 1.88, 3.95, 0.4, hd, size=13, color=col, bold=True, margin=0.02)
    text(s, x, 2.35, 3.95, 3.5, bl, size=11, color=INK, bullets=True, space=7, margin=0.02)
    x += 4.19
text(s, 0.5, 6.0, 12.33, 0.85, [
    "**Leverage reality:** Boreal's leverage is limited, but the OEM has itself put Options N and M on the table, and "
    "Boreal has not yet committed its IP. **Messaging:** announce a 'strategic OEM partnership' now. Report any "
    "advance as a recoupable guarantee, never as revenue."],
    size=11, color=WHITE, fill=NAVY, anchor=MSO_ANCHOR.MIDDLE, margin=0.15)

# =====================================================================
# 16. Signposts
s = new_slide("Four measurable signposts would change the recommendation, and the pilot is designed to "
              "produce all four", section=4,
              source="Board briefing pack §7; team analysis (thresholds from slide 7 breakeven formula)")
R = [["Signpost", "Today", "Move toward exclusivity if…", "Move away from the OEM if…"],
     ["Verified OEM shipments", "Unaudited forecast; no purchase orders",
      "Audited run-rate ≥ ~8,800 robots/yr: exclusivity pays even at 70% overlap",
      "Run-rate < ~3,300/yr (N) or ~4,100/yr (X): royalties do not cover $0.9M engineering"],
     ["Realised direct-channel overlap", "0% (CEO) vs 30–70% (Sales); no customer IDs",
      "Measured ≤ 30%: breakeven falls to ~6,100 robots/yr",
      "Measured ≥ 70%: breakeven ~8,800/yr; insist on carving out other-OEM customers"],
     ["Support cost per device", "$80 estimate",
      "Pilot confirms ≤ $80 and the $0.9M/yr engineering holds",
      "Above ~$107/robot, X loses value even at plan volume with 70% overlap (~$166 at 30%)"],
     ["Audit right", "Absent from draft",
      "Shipment-level independent audit agreed and the first audit reconciles",
      "No satisfactory audit right: no exclusivity at any reported volume"]]
fills = {(r, 2): GREEN_T for r in range(1, 5)}
fills.update({(r, 3): RED_T for r in range(1, 5)})
table(s, 0.5, 1.75, 12.33, R, [2.1, 2.6, 3.8, 3.8], size=11, row_h=0.95, fills=fills, bold_first_col=True)
text(s, 0.5, 6.6, 12.33, 0.4,
     "Support-cost threshold: ($3.0M − $0.9M − overlap × $1.476M) ÷ 10,000 robots = $107 (70%) / $166 (30%) per robot.",
     size=10, color=MUTED, margin=0.02)

# =====================================================================
# 17. Assumptions & risks
s = new_slide("The recommendation holds under the key assumptions; the main risk is that the OEM walks away, "
              "and the fallback limits that downside", section=4,
              source="Board briefing pack §2–7; team analysis")
text(s, 0.5, 1.68, 6.0, 0.35, "Key assumptions (and which way they bias the answer)", size=12, color=NAVY,
     bold=True, margin=0.02)
R = [["Assumption", "Effect"],
     ["$0.9M/yr engineering for all of 2027–29 on every OEM route", "Conservative; equal across X/N/M"],
     ["30–70% overlap applied to the $1.8M direct ARR; 2028 cohort only in the base case",
      "Favours X (floor on the lost margin)"],
     ["82% direct gross margin, before unquantified sales support", "Slightly overstates direct value"],
     ["The $0.45M assessment is needed for any OEM production route", "Neutral across OEM options"],
     ["N's $350 and partner volumes persist beyond 12 months", "Favours N; shown as an upper bound"],
     ["No discounting; headroom counts deal cash only", "Per board; rest-of-business burn not in pack"]]
table(s, 0.5, 2.05, 6.0, R, [3.9, 2.1], size=9.5, row_h=0.6)
text(s, 6.83, 1.68, 6.0, 0.35, "Risks and mitigations", size=12, color=NAVY, bold=True, margin=0.02)
R = [["Risk", "Mitigation"],
     ["The OEM rejects N/M and signs with a competitor (limited leverage)",
      "M is the OEM's own proposal; trade price, scope and term; fallback is direct sales plus the integration pilot"],
     ["Certification slips past September 2027", "Start the assessment now; release triggers; no exclusivity until passed"],
     ["Royalty reporting lag squeezes cash to $0.55M headroom", "Monthly remittance; phase engineering; OEM-funded integration work"],
     ["Support cost or engineering effort exceeds the estimate", "Measure in the pilot; reprice before conversion"],
     ["OEM volumes fall short of plan", "Gate 2 uses audited volumes; royalty floor after conversion"],
     ["Competitor claim proves causal after all", "Gated M still captures exclusivity benefits once proven"]]
table(s, 6.83, 2.05, 6.0, R, [2.9, 3.1], size=9.5, row_h=0.6)

# =====================================================================
# 18. Next steps
s = new_slide("Next steps: start certification now, since it is on the critical path for every OEM route, and "
              "bring the gated N→M term sheet to the April 2027 board", section=4,
              source="Board briefing pack §1, §2, §5; team analysis. Owners are proposed.")
text(s, 0.5, 1.7, 12.33, 0.75, [
    "**Decisions requested from the board:**  (1) Reject Option X as drafted.  (2) Authorise management to negotiate "
    "Option N with the pre-agreed Option M gates and the must-have terms.  (3) Approve the $0.45M assessment now; "
    "this leaves $1.85M of headroom above the buffer."],
    size=11.5, color=WHITE, fill=NAVY, anchor=MSO_ANCHOR.MIDDLE, margin=0.15)
R = [["When", "Action", "Proposed owner", "Output / decision point"],
     ["Nov–Dec 2026", "Engage the third-party security and industrial-safety assessor ($0.45M)", "CTO / Engineering",
      "Signed scope; certification plan to September 2027"],
     ["Dec 2026–Mar 2027", "Add customer-level identifiers to the direct pipeline and OEM reports", "Sales + Finance",
      "Baseline for measuring overlap"],
     ["Jan–Mar 2027", "Negotiate the N term sheet: audit, escrow, release, gates, carve-outs", "Partnerships + Legal",
      "Term sheet for board approval"],
     ["Jan–Mar 2027", "Replace the CFO dashboard with a full incremental-margin view", "CFO",
      "Royalty − $80/robot − $0.9M − displaced direct margin"],
     ["Apr 2027", "Board decision: approve N→M or a fallback", "Board", "Signed pilot, or direct + integration pilot"],
     ["Sep 2027", "Certification in OEM hardware (loaded warehouse, peak conditions)", "Engineering", "Gate 1"],
     ["Q4 2027–Q1 2028", "Two audited quarters of OEM shipments; pilot support-cost readout", "Finance", "Gate 2 evidence"],
     ["~Q2 2028", "Gate review: convert to Option M, extend N or exit", "Board", "Exclusivity decision on evidence"]]
table(s, 0.5, 2.6, 12.33, R, [1.6, 5.0, 1.9, 3.8], size=10.5, row_h=0.47, bold_first_col=True)

# =====================================================================
# 19. Appendix A: full calculation
s = new_slide("Appendix A: Option X year-by-year economics under the plan and 65% stress cases", section=None,
              source="Board briefing pack §3–4; team analysis. $M, undiscounted. Lost direct margin shown at 30% / "
                     "70% overlap, 2028 cohort only.")
R = [["$M", "Plan 2027", "Plan 2028", "Plan 2029", "Plan total", "Stress 2027", "Stress 2028", "Stress 2029",
      "Stress total"],
     ["Robots shipped", "5,000", "10,000", "14,000", "29,000", "3,250", "6,500", "9,100", "18,850"],
     ["Royalties earned ($300)", "1.50", "3.00", "4.20", "8.70", "0.98", "1.95", "2.73", "5.66"],
     ["Variable support ($80)", "−0.40", "−0.80", "−1.12", "−2.32", "−0.26", "−0.52", "−0.73", "−1.51"],
     ["OEM engineering", "−0.90", "−0.90", "−0.90", "−2.70", "−0.90", "−0.90", "−0.90", "−2.70"],
     ["OEM contribution", "0.20", "1.30", "2.18", "3.68", "−0.19", "0.53", "1.10", "1.45"],
     ["Security / safety assessment", "−0.45", "", "", "−0.45", "−0.45", "", "", "−0.45"],
     ["Value before channel effects", "", "", "", "3.23", "", "", "", "1.00"],
     ["Lost direct GM, 30% / 70%", "", "−0.44 / −1.03", "", "−0.44 / −1.03", "", "−0.44 / −1.03", "",
      "−0.44 / −1.03"],
     ["**Exclusivity value, 30% / 70%**", "", "", "", "**2.79 / 2.20**", "", "", "", "**0.55 / −0.04**"],
     ["Memo: cash incl. advance", "2.00", "2.50", "4.20", "8.70", "2.00", "0.93", "2.73", "5.66"]]
fills = {(9, None): BLUE_TT, (5, None): LIGHT}
table(s, 0.5, 1.75, 12.33, R, [2.6, 1.1, 1.3, 1.1, 1.4, 1.1, 1.3, 1.1, 1.4], size=10.5, row_h=0.44,
      fills=fills, bold_first_col=True, aligns=[PP_ALIGN.LEFT] + [C] * 8)
text(s, 0.5, 6.7, 12.33, 0.3, "Direct gross margin at risk = $1.8M new 2028 ARR × 82% = $1.476M; × 30% = $0.44M; "
     "× 70% = $1.03M. Totals may differ by ±0.01 due to rounding.", size=9.5, color=MUTED, margin=0.02)

# =====================================================================
# 20. Appendix B: formulas & data gaps
s = new_slide("Appendix B: formulas, data sources and the gaps the pilot should close", section=None,
              source="Board briefing pack §1–7; team analysis")
text(s, 0.5, 1.7, 6.1, 5.2, [
    "**Formulas used**",
    "Royalty cash (X) = royalties earned − advance credit still unrecouped (first $2.0M of royalties)",
    "OEM contribution = robots × (royalty − $80) − $0.9M engineering per year",
    "Exclusivity value = Σ contribution − $0.45M assessment − overlap × $1.8M × 82%",
    "Breakeven robots/yr = ($0.9M + overlap × $1.476M) ÷ ($300 − $80)",
    "N parity volume = (X value + $2.7M + $0.45M) ÷ ($350 − $80)",
    "Headroom = $4.9M − $2.6M + deal cash flows to end-2027",
    "Downtime cut = 1 − (0.5% ÷ 1.2%) = 58%"],
    size=11, color=INK, space=7, margin=0.1, fill=LIGHT)
text(s, 6.83, 1.7, 6.0, 5.2, [
    "**Data gaps and how we handled them**",
    "**Channel overlap:** no customer-level data. We used Sales' 30–70% range, bounded by 0% and 100%.",
    "**Direct churn and later cohorts:** not in the pack. The base case counts the 2028 cohort only; a 2029 "
    "renewal sensitivity is on slide 6.",
    "**Discount rate:** not in the pack. No NPV is computed, per the board.",
    "**OEM enforcement terms and termination payment:** not in the pack. Treated qualitatively.",
    "**Integration-firm royalty:** not in the pack. Treated as a nonexclusive complement, not valued.",
    "**Rest-of-business cash burn:** not in the pack. We assume the $2.6M buffer covers it.",
    "**Pricing under N/M:** the OEM will not guarantee it. Shown as indicative."],
    size=11, color=INK, space=7, margin=0.1, fill=LIGHT)

prs.save(OUT)
print("saved", OUT, "slides:", len(prs.slides))
