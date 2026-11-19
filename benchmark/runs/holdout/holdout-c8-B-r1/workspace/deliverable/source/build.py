import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION, XL_TICK_LABEL_POSITION, XL_TICK_MARK, XL_MARKER_STYLE

OUT = sys.argv[1]
PREV = sys.argv[2]

D = Deck()
SECTIONS = ["1  Economics", "2  Constraints", "3  Recommended path"]

# ------------------------------------------------------------------ model
E, C0, W0 = 200_000, 160_000, 140_000
E28, C28 = E * 1.10, C0 * 1.06
def cost(ev, cv, o, credit=False):
    cw = cv * 9 + W0 * 10 + 3.0e6
    return {"SQ": ev * 8 + cw + 1.3e6, "K": ev * 8 + cw + 1.0e6, "C": ev * 13 + cw + 0.2e6,
            "X": ev * 11 + cw + (0 if credit else 0.85e6)}[o] / 1e6
c27 = {o: cost(E, C0, o) for o in "SQ K C X".split()}
c28 = {o: cost(E28, C28, o) for o in "SQ K C X".split()}
one = {"SQ": 0, "K": 0.15, "C": 0.75, "X": 0.75}
def net(er): return (E * er + C0 * .94 + W0 * .95) / (E + C0 + W0)
assert abs(c27["K"] - 8.44) < 1e-9 and abs(c27["C"] - 8.64) < 1e-9 and abs(c27["X"] - 8.89) < 1e-9

# ------------------------------------------------------------------ frame helpers
def frame(s, sec, title, source):
    # tracker
    if sec is not None:
        x = 0.5
        for i, name in enumerate(SECTIONS):
            on = (i == sec)
            s.text(x, 0.22, 2.0, 0.26, name.upper(), size=8.5, bold=on, color=NAVY if on else MUTED, inset=0.0)
            if on:
                s.rect(x, 0.47, 1.6, 0.035, fill=BLUE)
            x += 2.1
    elif sec is None:
        pass
    s.text(0.5, 0.58, 12.33, 0.92, title, size=20, bold=True, color=INK, inset=0.0, anchor="t")
    s.hline(0.5, 1.55, 12.33, color=AXIS)
    if source:
        s.text(0.5, 7.02, 11.6, 0.36, source, size=8, color=MUTED, inset=0.0)
    s.text(12.33, 7.02, 0.5, 0.3, str(s.n), size=8.5, color=MUTED, align="r", inset=0.0)

def frame_appx(s, title, source):
    s.text(0.5, 0.22, 3, 0.26, "APPENDIX", size=8.5, bold=True, color=NAVY, inset=0.0)
    s.rect(0.5, 0.47, 0.9, 0.035, fill=BLUE)
    s.text(0.5, 0.58, 12.33, 0.92, title, size=20, bold=True, color=INK, inset=0.0)
    s.hline(0.5, 1.55, 12.33, color=AXIS)
    s.text(0.5, 7.02, 11.6, 0.36, source, size=8, color=MUTED, inset=0.0)
    s.text(12.33, 7.02, 0.5, 0.3, str(s.n), size=8.5, color=MUTED, align="r", inset=0.0)

SRC = "Source: Northline Home briefing pack (synthetic case data), sections "

PILL = {"PASS": (GOOD, WHITE), "FAIL": (CRIT, WHITE), "UNPROVEN": (WARN, INK), "PARTLY": (WARN, INK),
        "HOLDS": (GOOD, WHITE), "REFINED": (WARN, INK), "AT RISK": (WARN, INK), "REJECT": (CRIT, WHITE)}
def pill(s, x, y, label, w=0.95, h=0.26):
    f, t = PILL[label]
    s.text(x, y, w, h, label, size=8.5, bold=True, color=t, fill=f, align="c", anchor="m", inset=0.02,
           shape=MSO_SHAPE.ROUNDED_RECTANGLE)

def table(s, x, y, widths, rows, heights, header_fill=NAVY, size=10, head_size=10, zebra=False,
          bold_first_col=True, aligns=None, row_fills=None, line_color=GRID):
    """rows[0] = header. cell may be str or list of paragraph items."""
    cy = y
    for ri, row in enumerate(rows):
        h = heights[ri]
        cx = x
        for ci, cell in enumerate(row):
            w = widths[ci]
            al = aligns[ci] if aligns else "l"
            if ri == 0:
                s.text(cx, cy, w, h, cell, size=head_size, bold=True, color=WHITE if header_fill else INK,
                       fill=header_fill, align=al, anchor="m", inset=0.07)
            else:
                fill = None
                if row_fills and row_fills.get(ri): fill = row_fills[ri]
                elif zebra and ri % 2 == 0: fill = PALE
                s.text(cx, cy, w, h, cell, size=size, bold=(bold_first_col and ci == 0), color=INK,
                       fill=fill, align=al, anchor="m", inset=0.07)
            cx += w
        cy += h
        if ri > 0:
            s.hline(x, cy, sum(widths), color=line_color, lw=0.5)
    return cy

# ------------------------------------------------------------------ chart helpers
def base_chart(s, kind, x, y, w, h, cats, series, label, num_fmt='0.0', legend=False):
    cd = CategoryChartData(number_format=num_fmt)
    cd.categories = cats
    for name, vals in series:
        cd.add_series(name, [round(v, 4) for v in vals])
    gf = s.s.shapes.add_chart(kind, Inches(x), Inches(y), Inches(w), Inches(h), cd)
    s.chart_placeholder(x, y, w, h, label)
    ch = gf.chart
    ch.font.size = Pt(10); ch.font.name = FONT; ch.font.color.rgb = rgb(INK2)
    ch.has_legend = legend
    if legend:
        ch.legend.position = XL_LEGEND_POSITION.TOP; ch.legend.include_in_layout = False
        ch.legend.font.size = Pt(10)
    va, ca = ch.value_axis, ch.category_axis
    va.has_major_gridlines = True
    va.major_gridlines.format.line.color.rgb = rgb(GRID); va.major_gridlines.format.line.width = Pt(0.5)
    va.format.line.fill.background()
    va.major_tick_mark = XL_TICK_MARK.NONE; ca.major_tick_mark = XL_TICK_MARK.NONE
    ca.format.line.color.rgb = rgb(AXIS)
    va.tick_labels.font.size = Pt(9.5); va.tick_labels.font.color.rgb = rgb(MUTED)
    ca.tick_labels.font.size = Pt(10); ca.tick_labels.font.color.rgb = rgb(INK2)
    va.tick_labels.number_format = num_fmt; va.tick_labels.number_format_is_linked = False
    return ch

def color_series(ser, color):
    ser.format.fill.solid(); ser.format.fill.fore_color.rgb = rgb(color)
    ser.format.line.fill.background()

def color_point(ser, i, color):
    pt = ser.points[i]
    pt.format.fill.solid(); pt.format.fill.fore_color.rgb = rgb(color)
    pt.format.line.fill.background()

def label_point(ser, i, txt, pos=XL_LABEL_POSITION.OUTSIDE_END, size=10, bold=True, color=INK):
    dl = ser.points[i].data_label
    dl.has_text_frame = True
    dl.text_frame.text = txt
    r = dl.text_frame.paragraphs[0].runs[0]
    r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = rgb(color); r.font.name = FONT
    if pos is not None:
        dl.position = pos

def drop_legend_entry(ch, idx):
    leg = ch.legend._element
    pos = leg.find(qn("c:legendPos"))
    le = leg.makeelement(qn("c:legendEntry"), {})
    i = le.makeelement(qn("c:idx"), {"val": str(idx)}); le.append(i)
    d = le.makeelement(qn("c:delete"), {"val": "1"}); le.append(d)
    pos.addnext(le)

def hide_series(ser):
    ser.format.fill.background(); ser.format.line.fill.background()

# ================================================================== 1 TITLE
s = D.new()
s.rect(0, 0, SW, SH, fill=NAVY)
s.rect(0.7, 2.2, 0.09, 2.6, fill=BLUE)
s.text(1.0, 1.4, 11, 0.4, "NORTHLINE HOME  |  CEO AND BOARD DECISION PAPER", size=11, bold=True, color="B7D3F6", inset=0)
s.text(1.0, 2.15, 11.2, 1.6, "East regional distribution center: close in 2027, or retain and optimize?",
       size=34, bold=True, color=WHITE, inset=0)
s.text(1.0, 3.85, 11.2, 1.0, "Recommendation: retain and optimize East through its 2029 lease end, and use 2027–28 "
       "to test the cross-dock alternative before the lease decision", size=16, color="DCE8F8", inset=0)
s.text(1.0, 6.3, 11, 0.6, ["Board meeting pre-read  |  November 2026",
                           "Based only on the board briefing pack (synthetic case data). All figures are in US$, at 2027 volumes unless stated."],
       size=10, color="B7D3F6", inset=0)

# ================================================================== 2 EXEC SUMMARY
s = D.new()
frame(s, None, "Executive summary: retain and optimize East through its 2029 lease end. Neither closure "
      "option both saves money and meets the board's 2027 constraints", SRC + "2–7; Northline analysis.")
s.text(0.5, 1.7, 12.33, 0.95,
       [{"runs": [("Governing thought: ", True, NAVY),
                  ("Keep East in 2027 and optimize it (Option K: saves $0.30M a year for $0.15M one-time), and run a capped cross-dock "
                   "test. Closing East saves at most $0.10M a year, not the $1.3M claimed, and fails or cannot yet prove the SLA, "
                   "capacity and evidence tests. The 2029 lease end is the real decision point.", False, INK)]}],
       size=12.5, fill=PALEBLUE, anchor="m", inset=0.12)
rows = [
    ("1", "Closing East does not pay once routing and handling are counted", "Slides 6–8",
     ["The CFO's $1.3M is East's gross fixed cost. Serving 200k Eastern orders from Central adds $1.0M of transport (200k × $5) "
      "and $0.2M of damage: a net $0.10M a year, zero at 2028 volume, before the $0.75M exit fee",
      "The cross-dock costs $0.15M a year more than today: $3 extra per order ($0.60M) outweighs the $0.45M fixed-cost reduction",
      "Optimized retention (K) is the cheapest design in the base case: $8.44M in 2027, $0.20–0.45M a year below either closure"]),
    ("2", "Closure also breaks, or cannot yet prove, the board's binding constraints", "Slides 9–12",
     ["Close to Central: 90.3% network two-day rate vs the 92% contract; Central at 100% of capacity in 2027 and 108% in 2028; "
      "the $1.1M retrofit it needs is unbudgeted and would take one-time spend to $1.85M vs $0.9M authorized",
      "Cross-dock: 93.9% on paper, but from a 6-week, non-holiday pilot with no all-ZIP definition and no promotion guarantee",
      "Retain and optimize: 95.1% network rate, Central at 47% in 2028, $0.15M one-time"]),
    ("3", "Optimize now, test the cross-dock, and decide the 2029 lease at a Q3 2028 gate", "Slides 13–16",
     ["Approve Option K and a capped cross-dock test (≤$0.25M) through holiday 2027 and spring 2028, measured on all ZIP codes",
      "Waiting avoids the $0.75M early-exit fee and settles whether the $0.85M minimum is extra or credited; that point swings "
      "the cross-dock's cost by $0.85M a year",
      "Drop close-to-Central: its $5-per-order penalty makes it no cheaper than today at 2028 volume, even if Central were expanded"]),
]
y = 2.85
for num, head, ref, buls in rows:
    s.text(0.5, y, 0.45, 0.45, num, size=16, bold=True, color=WHITE, fill=BLUE, align="c", anchor="m", inset=0,
           shape=MSO_SHAPE.OVAL)
    s.text(1.1, y - 0.03, 3.5, 0.95, head, size=13, bold=True, color=NAVY, inset=0.02)
    s.text(1.1, y + 0.92, 3.4, 0.3, ref, size=9, color=MUTED, inset=0.02)
    s.text(4.75, y - 0.05, 8.08, 1.33, [{"text": b, "bullet": True, "sb": 0 if i == 0 else 3} for i, b in enumerate(buls)],
           size=10.5, color=INK, inset=0.02)
    y += 1.4
    if num != "3":
        s.hline(0.5, y - 0.1, 12.33, color=GRID)

# ================================================================== 3 DECISION FRAME
s = D.new()
frame(s, None, "We tested four network designs and a deferral path against the board's four tests plus reversibility, "
      "using all-in cost and the contracted all-ZIP service KPI", SRC + "2, 3, 6.")
s.text(0.5, 1.72, 6.3, 0.3, "OPTIONS EVALUATED", size=10, bold=True, color=NAVY, inset=0)
opts = [["", "Option", "What it means"],
        ["SQ", "Status quo", "Keep all three sites as they are today. This is the reference case"],
        ["K", "Retain and optimize", "Renegotiate East staffing shifts and add a transfer buffer for low-volume SKUs. Saves $0.30M a year for $0.15M upfront (facility audit)"],
        ["C", "Close East, serve from Central", "End the East lease in 2027 ($0.75M) and ship all 200k Eastern orders from Central at $13 each"],
        ["X", "Close East, use a cross-dock", "End the East lease and sign a two-year deal with a third-party Eastern cross-dock: $11 per order plus a $0.85M annual minimum"],
        ["D", "Defer (middle path)", "Run K now, test the cross-dock through holiday peak, and decide at the 2029 lease end"]]
table(s, 0.5, 2.05, [0.45, 1.75, 4.1], opts, [0.34, 0.6, 0.78, 0.6, 0.78, 0.6], size=9.5, head_size=9.5)
s.text(7.2, 1.72, 5.6, 0.3, "FIVE TESTS: FOUR SET BY THE BOARD, PLUS REVERSIBILITY", size=10, bold=True, color=NAVY, inset=0)
tests = [["Test", "Pass standard"],
         ["1  Economics", "Lowest all-in annual cost: transport, facility fixed cost and damage, plus one-time cost. Not the CFO's carrier-only cost per shipment"],
         ["2  Service", "At least 92% of all orders delivered within two days, network-wide, on all ZIP codes (the contracted KPI, not the ex-rural dashboard)"],
         ["3  Capacity", "Central at or below its 360k certified practical capacity in 2027 and under 2028 growth (+10% East, +6% Central)"],
         ["4  Funding and lease", "No more than $0.9M of one-time change cost in 2027; East early exit $0.75M; West lease fixed to 2030"],
         ["5  Risk", "Decision-grade evidence and reversibility (rebuilding East-type capacity takes nine months)"]]
table(s, 7.2, 2.05, [1.65, 3.98], tests, [0.34, 0.74, 0.74, 0.6, 0.6, 0.6], size=9.5, head_size=9.5)
s.text(0.5, 6.2, 12.33, 0.62,
       [{"runs": [("Burden of proof: ", True, NAVY),
                  ("closing East is hard to reverse (nine months plus customer migrations) and must pass all five tests on today's "
                   "evidence. Where the evidence is incomplete, we say so and treat it as a risk, not a pass.", False, INK)]}],
       size=10.5, fill=PALE, anchor="m", inset=0.12)

# ================================================================== 4 HYPOTHESIS
s = D.new()
frame(s, None, "Our working hypothesis, the CEO's 'keep East open in 2027', held up under testing, but it needed "
      "three refinements", SRC + "2–7; Northline analysis.")
s.text(0.5, 1.72, 8.0, 0.3, "WHAT WOULD HAVE TO BE TRUE FOR 'KEEP EAST' TO BE RIGHT, AND WHAT WE FOUND", size=10, bold=True, color=NAVY, inset=0)
hy = [["Condition", "What the evidence shows", "Verdict"],
      ["a  Closing saves little once all costs are counted", "Close to Central nets $0.10M a year (vs $1.3M claimed) and $0 at 2028 volume; the cross-dock costs $0.15M a year more than today (slides 6–8)", ""],
      ["b  Closing puts the 92% SLA at risk", "Close to Central: 90.3% (fail). Cross-dock: 93.9% on paper, from non-peak pilot data (slides 9–10)", ""],
      ["c  Central cannot absorb Eastern demand", "True for close to Central: 108% of capacity in 2028. Not relevant to the cross-dock, which does not use Central (slide 11)", ""],
      ["d  Keeping East fits the lease and budget", "Lease runs to 2029 with no fee; K needs $0.15M of the $0.9M authorized (slide 12)", ""],
      ["e  Keeping East is the cheapest way to meet the SLA", "Yes: even unoptimized, East ($8.74M) beats the only SLA-compliant closure option ($8.89M). K is cheaper still at $8.44M (slide 7)", ""]]
hh = [0.34, 0.74, 0.74, 0.74, 0.62, 0.74]
table(s, 0.5, 2.05, [2.45, 4.6, 1.0], hy, hh, size=9.5, head_size=9.5)
verd = ["HOLDS", "PARTLY", "PARTLY", "HOLDS", "HOLDS"]
yy = 2.05 + hh[0]
for i, v in enumerate(verd):
    pill(s, 7.6, yy + (hh[i + 1] - 0.26) / 2, v, w=0.85)
    yy += hh[i + 1]
s.text(8.85, 1.72, 3.98, 1.25,
       [{"text": "INITIAL HYPOTHESIS (CEO'S VIEW)", "bold": True, "color": MUTED, "size": 9},
        {"text": "Keep East open in 2027, because Central has too little spare capacity for demand growth.", "sb": 4, "size": 11.5}],
       fill=PALE, inset=0.14)
s.text(8.85, 3.08, 3.98, 3.75,
       [{"text": "REFINED ANSWER", "bold": True, "color": "B7D3F6", "size": 9},
        {"runs": [("1  Retain and optimize, not just retain. ", True, WHITE), ("Option K beats the status quo by $0.30M a year at low risk.", False, WHITE)], "sb": 6, "size": 10.5},
        {"runs": [("2  Capacity only rules out close-to-Central. ", True, WHITE), ("The cross-dock fails on cost ($0.45M a year above K in the base case) and on unproven peak service.", False, WHITE)], "sb": 8, "size": 10.5},
        {"runs": [("3  Keep East through 2029, not permanently. ", True, WHITE), ("The early-exit fee falls away at lease end. Test the cross-dock now and decide at a Q3 2028 gate.", False, WHITE)], "sb": 8, "size": 10.5}],
       fill=NAVY, inset=0.16)

# ================================================================== 5 CLAIMS
s = D.new()
frame(s, None, "Five claims in the board pre-read overstate the case for one side or the other and should not "
      "anchor the decision", SRC + "3, 5. Corrected figures: Northline analysis.")
cl = [["Claim as circulated", "Source", "What it leaves out", "Evidence-based figure"],
      ["“Closing East saves $1.3M a year”", "CFO slide", "Counts East's fixed cost only. Leaves out the higher Central-to-East transport (+$5 × 200k), $0.2M extra damage and the $0.75M exit fee", "$0.10M a year before the $0.75M exit fee (–$0.65M in 2027); $0 at 2028 volume"],
      ["Cost per shipment as the cost KPI", "CFO dashboard", "Carrier invoice ÷ orders; excludes warehouse rent, returns and replacements, so it is a transport KPI only", "Use all-in cost: $8.44–8.89M a year by option"],
      ["“East delivers 98% in two days”", "Finance report", "Excludes rural deliveries; the contract KPI counts every ZIP code", "96% all-ZIP"],
      ["“East causes 8 pts higher renewal”", "Marketing", "Correlation only. East serves more high-volume accounts with dedicated sales teams, and this is not controlled for", "Not usable as causal evidence; retention response to service is unknown"],
      ["“Close in June 2027 and absorb at Central with today's staffing”", "Cost consultant", "Puts Central at its full 360k practical load before any demand spike; 2028 growth takes it past capacity", "100% of capacity in 2027; 108% in 2028"]]
table(s, 0.5, 1.75, [3.0, 1.45, 4.9, 2.98], cl, [0.36, 0.86, 0.78, 0.6, 0.86, 0.86], size=10, head_size=10, zebra=True)
s.text(0.5, 6.25, 12.33, 0.6,
       [{"runs": [("Implication: ", True, NAVY),
                  ("these corrections cut both ways. They remove most of the closure saving (CFO, consultant) and also the "
                   "inflated service and loyalty case for keeping East (Finance, Marketing). The decision rests on the corrected figures.", False, INK)]}],
       size=10.5, fill=PALEBLUE, anchor="m", inset=0.12)

# ================================================================== 6 WATERFALL
s = D.new()
frame(s, 0, "After routing and damage costs, the CFO's $1.3M closure saving shrinks to $0.10M a year, and "
      "to zero at 2028 volume", SRC + "3–5. Transport rates exclude facility cost, damage and exit charge. 2028: Eastern volume +10% to 220k.")
s.text(0.5, 1.72, 7.9, 0.3, "Option C (close East, serve from Central): annual saving vs status quo, $M", size=11, bold=True, color=INK, inset=0)
cats = ["East fixed cost removed", "Higher transport (200k × $5)", "Transshipment damage", "Net saving 2027",
        "Extra orders in 2028 (20k × $5)", "Net saving 2028"]
base = [0, 0.30, 0.10, 0, 0.0, 0]
vals = [1.30, 1.00, 0.20, 0.10, 0.10, 0.0]
cap = [0.16] * 6
ch = base_chart(s, XL_CHART_TYPE.COLUMN_STACKED, 0.4, 2.0, 8.1, 4.85, cats, [("base", base), ("value", vals), ("cap", cap)],
                "waterfall", num_fmt='"$"0.0"M"')
plot = ch.plots[0]; plot.gap_width = 55; plot.overlap = 100
hide_series(plot.series[0]); hide_series(plot.series[2])
sv = plot.series[1]
colors = [GRAY, CRIT, CRIT, ORANGE, CRIT, ORANGE]
labels = ["+$1.30M", "–$1.00M", "–$0.20M", "$0.10M", "–$0.10M", "$0.00M"]
for i, c in enumerate(colors):
    color_point(sv, i, c)
    label_point(plot.series[2], i, labels[i], pos=XL_LABEL_POSITION.INSIDE_BASE, color=INK)
ch.value_axis.minimum_scale = 0; ch.value_axis.maximum_scale = 1.6; ch.value_axis.major_unit = 0.2
# right panel
s.text(8.8, 1.72, 4.03, 2.2,
       [{"text": "THE ARITHMETIC", "bold": True, "color": NAVY, "size": 9.5},
        {"runs": [("Fixed cost removed: ", True, INK), ("East site $1.30M a year", False, INK)], "sb": 5},
        {"runs": [("Transport: ", True, INK), ("200k orders × ($13 − $8) = $1.00M a year", False, INK)], "sb": 4},
        {"runs": [("Damage: ", True, INK), ("+$0.20M a year for transshipped goods", False, INK)], "sb": 4},
        {"runs": [("Net 2027: ", True, INK), ("1.30 − 1.00 − 0.20 = $0.10M", False, INK)], "sb": 4},
        {"runs": [("Break-even volume: ", True, INK), ("$1.10M ÷ $5 = 220k Eastern orders, exactly the 2028 forecast", False, INK)], "sb": 4}],
       size=10, fill=PALE, inset=0.14)
s.text(8.8, 4.07, 4.03, 2.78,
       [{"text": "NOT YET INCLUDED: ALL MAKE IT WORSE", "bold": True, "color": NAVY, "size": 9.5},
        {"text": "$0.75M exit fee: 7.5-year payback at $0.10M a year, for a lease that ends in 2029 anyway", "bullet": True, "sb": 5},
        {"text": "Carrier surcharge needed to lift Eastern service above 84% (not priced)", "bullet": True, "sb": 3},
        {"text": "$1.1M Central retrofit needed once 2028 growth arrives (slide 11)", "bullet": True, "sb": 3},
        {"text": "Compared with Option K, close-to-Central is $0.20M a year more expensive even before these items", "bullet": True, "sb": 3}],
       size=10, line=AXIS, inset=0.14)

# ================================================================== 7 ALL-IN COST
s = D.new()
frame(s, 0, "On an all-in basis, retaining and optimizing East (Option K) is the cheapest design in both 2027 "
      "and 2028 under the base reading of the cross-dock quote", SRC + "3, 4, 6. *K's $0.30M audit saving is shown against facility cost. C excludes the unpriced carrier "
      "surcharge and the $1.1M retrofit. 2028 assumes +10% East, +6% Central, West flat.")
s.text(0.5, 1.72, 6.9, 0.3, "All-in annual cost build-up, $M", size=11, bold=True, color=INK, inset=0)
f2 = lambda v: f"{v:.2f}"
ct = [["$M", "SQ  Status quo", "K  Retain + optimize", "C  Close to Central", "X  Cross-dock"],
      ["Eastern-order transport", "1.60  (200k × $8)", "1.60", "2.60  (× $13)", "2.20  (× $11)"],
      ["Central and West transport", "2.84", "2.84", "2.84", "2.84"],
      ["Facility fixed cost", "4.30", "4.00*", "3.00", "3.85  (incl. 0.85 min.)"],
      ["Extra damage and handling", "–", "–", "0.20", "in quote"],
      ["All-in cost, 2027", f2(c27["SQ"]), f2(c27["K"]), f2(c27["C"]), f2(c27["X"])],
      ["All-in cost, 2028", f2(c28["SQ"]), f2(c28["K"]), f2(c28["C"]), f2(c28["X"])],
      ["One-time cost, 2027", "0.00", "0.15", "0.75", "0.75"],
      ["Two-year total, 2027–28", f2(c27["SQ"] + c28["SQ"]), f2(c27["K"] + c28["K"] + .15), f2(c27["C"] + c28["C"] + .75), f2(c27["X"] + c28["X"] + .75)]]
table(s, 0.5, 2.05, [2.0, 1.3, 1.25, 1.25, 1.35], ct, [0.5, 0.46, 0.4, 0.46, 0.4, 0.42, 0.42, 0.4, 0.42], size=9.5, head_size=9,
      aligns=["l", "r", "r", "r", "r"], row_fills={5: PALEBLUE, 6: PALEBLUE, 8: PALEBLUE})
s.rect(0.5 + 2.0 + 1.3, 2.05, 1.25, 3.88, line=BLUE, lw=1.75)
s.text(7.9, 1.72, 4.93, 0.3, "Annual all-in cost above Option K, $M", size=11, bold=True, color=INK, inset=0)
ch = base_chart(s, XL_CHART_TYPE.COLUMN_CLUSTERED, 7.8, 2.0, 5.05, 3.95,
                ["SQ  Status quo", "C  Close to Central", "X  Cross-dock"],
                [("2027", [c27[o] - c27["K"] for o in ("SQ", "C", "X")]), ("2028", [c28[o] - c28["K"] for o in ("SQ", "C", "X")])],
                "delta vs K", num_fmt='"$"0.00"M"', legend=True)
plot = ch.plots[0]; plot.gap_width = 70; plot.overlap = -8
color_series(plot.series[0], "86B6EF"); color_series(plot.series[1], "1C5CAB")
for si, ser in enumerate(plot.series):
    vv = [c27, c28][si]
    for i, o in enumerate(("SQ", "C", "X")):
        label_point(ser, i, f"+{vv[o] - vv['K']:.2f}", size=9.5)
ch.value_axis.minimum_scale = 0; ch.value_axis.maximum_scale = 0.6; ch.value_axis.major_unit = 0.1
s.text(0.5, 6.12, 12.33, 0.72,
       [{"runs": [("So what: ", True, NAVY),
                  ("K is $0.45M cheaper than the status quo over 2027–28 after its $0.15M setup cost. Both closure options cost more "
                   "than K every year, and the gap widens as Eastern volume grows, because each extra Eastern order costs $3–5 more to serve.", False, INK)]}],
       size=10.5, fill=PALEBLUE, anchor="m", inset=0.12)

# ================================================================== 8 BREAK-EVEN
s = D.new()
frame(s, 0, "Closing East would beat optimized retention only if Eastern volume fell below 160k orders, against "
      "200k in 2027 and 220k forecast for 2028", SRC + "3, 4, 6. Lines show the annual all-in saving vs Option K; "
      "one-time costs excluded. Assumes rates and fixed costs do not change with volume.")
s.text(0.5, 1.72, 7.9, 0.3, "Annual saving of each closure option vs Option K, by Eastern volume, $M", size=11, bold=True, color=INK, inset=0)
vols = [100, 120, 140, 160, 180, 200, 220, 240]
cdat = [0.8 - 5 * v / 1000 for v in vols]
xdat = [0.15 - 3 * v / 1000 for v in vols]
ch = base_chart(s, XL_CHART_TYPE.LINE_MARKERS, 0.4, 2.0, 8.1, 4.85, [f"{v}k" for v in vols],
                [("C  Close to Central", cdat), ("X  Cross-dock", xdat)], "breakeven lines", num_fmt='"$"0.0"M"', legend=True)
ch.category_axis.tick_label_position = XL_TICK_LABEL_POSITION.LOW
ch.value_axis.minimum_scale = -0.8; ch.value_axis.maximum_scale = 0.4; ch.value_axis.major_unit = 0.2
ch.value_axis.format.line.fill.background()
ch.category_axis.format.line.color.rgb = rgb(INK2)
for ser, col in zip(ch.plots[0].series, (ORANGE, AQUA)):
    ser.format.line.color.rgb = rgb(col); ser.format.line.width = Pt(2.25); ser.smooth = False
    ser.marker.style = XL_MARKER_STYLE.CIRCLE; ser.marker.size = 7
    ser.marker.format.fill.solid(); ser.marker.format.fill.fore_color.rgb = rgb(col)
    ser.marker.format.line.color.rgb = rgb(WHITE)
cs, xs = ch.plots[0].series
label_point(cs, 3, "Break-even 160k", pos=XL_LABEL_POSITION.ABOVE, size=9.5)
label_point(cs, 5, "–$0.20M", pos=XL_LABEL_POSITION.BELOW, size=9.5)
label_point(cs, 6, "–$0.30M", pos=XL_LABEL_POSITION.BELOW, size=9.5)
label_point(xs, 5, "–$0.45M", pos=XL_LABEL_POSITION.BELOW, size=9.5)
label_point(xs, 6, "–$0.51M", pos=XL_LABEL_POSITION.BELOW, size=9.5)
s.text(8.8, 1.72, 4.03, 2.6,
       [{"text": "HOW THE LINES ARE BUILT", "bold": True, "color": NAVY, "size": 9.5},
        {"text": "Saving vs K = fixed cost avoided − added cost − (rate gap × Eastern orders V)", "sb": 5},
        {"runs": [("C: ", True, INK), ("($1.30M − $0.30M − $0.20M) − $5 × V  → zero at V = 160k", False, INK)], "sb": 5},
        {"runs": [("X: ", True, INK), ("($1.30M − $0.30M − $0.85M) − $3 × V  → zero at V = 50k", False, INK)], "sb": 4},
        {"text": "($0.30M = K's saving, lost if East closes)", "sb": 4, "color": INK2, "size": 9.5}],
       size=10, fill=PALE, inset=0.14)
bt = [["Break-even Eastern orders", "vs K", "vs status quo"],
      ["C  Close to Central", "160k", "220k"],
      ["X  Cross-dock", "50k", "150k"]]
table(s, 8.8, 4.48, [1.93, 0.95, 1.15], bt, [0.36, 0.36, 0.36], size=10, head_size=9.5, aligns=["l", "r", "r"])
s.text(8.8, 5.68, 4.03, 1.17,
       "A lower-growth case does not rescue closure: 2027 Eastern volume is already 200k. Volume would have to fall 20% "
       "(close to Central) or 75% (cross-dock) for closure to beat K.", size=10, color=INK, fill=PALEBLUE, inset=0.12, anchor="m")

# ================================================================== 9 SLA
s = D.new()
frame(s, 1, "Moving Eastern orders to Central would breach the contracted 92% two-day SLA; the cross-dock clears "
      "it on paper by 1.9 points", SRC + "2, 4. Assumes Central (94%) and West (95%) keep their current two-day rates. "
      "East's 96% is all-ZIP; the basis of the 84% (modeled) and the 93% (pilot) is not stated.")
s.text(0.5, 1.72, 7.9, 0.3, "Network-wide two-day delivery rate vs the 92% contract floor, 2027, points", size=11, bold=True, color=INK, inset=0)
ch = base_chart(s, XL_CHART_TYPE.BAR_CLUSTERED, 0.4, 2.0, 8.1, 3.3,
                ["K / SQ  Retain East (East 96%)", "X  Cross-dock (East 93% pilot)", "C  Close to Central (East 84%)"],
                [("Margin vs 92% floor", [round((net(.96) - .92) * 100, 2), round((net(.93) - .92) * 100, 2), round((net(.84) - .92) * 100, 2)])],
                "sla margin", num_fmt='+0.0;–0.0;0')
plot = ch.plots[0]; plot.gap_width = 60
ser = plot.series[0]
for i, col in enumerate((BLUE, AQUA, ORANGE)):
    color_point(ser, i, col)
label_point(ser, 0, "95.1% (+3.1)", size=10)
label_point(ser, 1, "93.9% (+1.9, unproven)", size=10)
label_point(ser, 2, "90.3% (–1.7, breach)", size=10)
ch.category_axis.reverse_order = True
ch.category_axis.tick_label_position = XL_TICK_LABEL_POSITION.LOW
ch.value_axis.minimum_scale = -6; ch.value_axis.maximum_scale = 7; ch.value_axis.major_unit = 1
ch.value_axis.tick_labels.font.size = Pt(9)
s.text(0.5, 5.45, 8.0, 1.4,
       [{"text": "Network rate = (200k × Eastern rate + 160k × 94% + 140k × 95%) ÷ 500k", "bold": True, "color": NAVY},
        {"text": "C: (168.0k + 150.4k + 133.0k) ÷ 500k = 90.3%. It needs 460k on-time orders but delivers 451k, so about 8,600 orders "
                 "a year fall short, triggering retailer penalty clauses", "sb": 5},
        {"text": "The 84% can be lifted only with a carrier surcharge that the $13 rate does not include. Any surcharge widens C's existing $0.20M-a-year cost gap to K", "sb": 4}],
       size=10, fill=PALE, inset=0.14)
s.text(8.8, 1.72, 4.03, 5.13,
       [{"text": "THE THRESHOLD THAT MATTERS", "bold": True, "color": NAVY, "size": 9.5},
        {"text": "88.3%", "bold": True, "size": 30, "color": NAVY, "sb": 6},
        {"text": "Minimum Eastern all-ZIP two-day rate that keeps the network at 92%: (460.0k − 283.4k) ÷ 200k", "sb": 2},
        {"text": "Close to Central (84%) is 4.3 pts short", "bullet": True, "sb": 10},
        {"text": "The cross-dock pilot (93%) has 4.7 pts of headroom, but on non-peak data with an unstated measurement basis (slide 10)", "bullet": True, "sb": 3},
        {"text": "Retaining East (96%) has 7.7 pts of headroom", "bullet": True, "sb": 3},
        {"text": "We ignore Finance's 98% (excludes rural ZIPs) and the online dashboard measure. Neither is the contract KPI.", "sb": 10, "color": INK2, "size": 9.5}],
       size=10.5, line=AXIS, inset=0.16)

# ================================================================== 10 CROSS-DOCK EVIDENCE
s = D.new()
frame(s, 1, "The cross-dock's 93% comes from a short, non-peak pilot. It needs a holiday-peak, all-ZIP test "
      "before the board relies on it", SRC + "4, 6, 7. *The 2-pt gap mirrors East's ex-rural (98%) vs all-ZIP (96%) "
      "difference and is illustrative only. Test thresholds are proposed by Northline analysis.")
tiles = [("6%", "of annual Eastern volume tested", "12,000 orders vs 200k a year"),
         ("6 wks", "pilot length, no holiday weeks", "Peak weeks carry the most service risk"),
         ("?", "measurement basis", "The quote does not say whether the 93% covers all ZIP codes"),
         ("None", "service guarantee for the national spring promotion", "The operator has not committed to promotion volumes")]
x = 0.5
for big, lab, sub in tiles:
    s.text(x, 1.75, 2.93, 1.75,
           [{"text": big, "size": 28, "bold": True, "color": NAVY},
            {"text": lab, "size": 11, "bold": True, "sb": 2},
            {"text": sub, "size": 9.5, "color": INK2, "sb": 4}], fill=PALE, inset=0.16)
    x += 3.13
s.text(0.5, 3.72, 6.0, 0.3, "HOW MUCH HEADROOM THE PILOT REALLY GIVES", size=10, bold=True, color=NAVY, inset=0)
hd = [["Eastern rate scenario", "East rate", "Network", "East headroom vs 88.3%"],
      ["Pilot as reported", "93.0%", "93.9%", "+4.7 pts"],
      ["If the pilot excluded rural ZIPs (–2 pts)*", "91.0%", "93.1%", "+2.7 pts"],
      ["Break-even for the 92% contract", "88.3%", "92.0%", "0"]]
table(s, 0.5, 4.05, [2.75, 0.85, 0.85, 1.55], hd, [0.46, 0.4, 0.5, 0.4], size=10, head_size=9.5, aligns=["l", "r", "r", "r"])
s.text(0.5, 5.9, 6.0, 0.95,
       "A full-year rate is a weighted average. If peak weeks run well below the pilot, the remaining headroom of "
       "roughly 3–5 points can disappear, and the two-year contract minimum would already be signed.",
       size=10, color=INK, fill=PALEBLUE, inset=0.12, anchor="m")
s.text(6.9, 3.72, 5.93, 3.13,
       [{"text": "WHAT A DECISION-GRADE TEST MUST SHOW (PROPOSED GATE CRITERIA)", "bold": True, "color": NAVY, "size": 9.5},
        {"runs": [("Coverage: ", True, INK), ("holiday peak 2027 and the spring 2028 promotion, including rural ZIPs", False, INK)], "bullet": True, "sb": 6},
        {"runs": [("Service: ", True, INK), ("at least 92% all-ZIP over the full test period and at least 90% in peak weeks, keeping the network at or above 93.5%", False, INK)], "bullet": True, "sb": 4},
        {"runs": [("Contract: ", True, INK), ("SLA defined on all ZIP codes, a termination-for-cause clause (the provider will accept this), and clarity on whether the $0.85M minimum is extra or credited", False, INK)], "bullet": True, "sb": 4},
        {"runs": [("Cost: ", True, INK), ("measured damage and handling rate on transshipped goods", False, INK)], "bullet": True, "sb": 4}],
       size=10.5, line=AXIS, inset=0.16)

# ================================================================== 11 CAPACITY
s = D.new()
frame(s, 1, "Central would run at 100% of capacity from day one under close-to-Central and at 108% in 2028. "
      "Even a lower-growth case does not fit", SRC + "2, 4, 5. *Lower-growth case (half the forecast: East +5%, "
      "Central +3%) is illustrative; the pack asks for one to be discussed but does not size it.")
s.text(0.5, 1.72, 7.9, 0.3, "Central hub annual shipments vs 360k certified practical capacity, thousands", size=11, bold=True, color=INK, inset=0)
loads = [360.0, 374.8, 389.6, 169.6]
within = [min(v, 360) for v in loads]; over = [max(v - 360, 0) for v in loads]
ch = base_chart(s, XL_CHART_TYPE.COLUMN_STACKED, 0.4, 2.0, 8.1, 4.85,
                ["C, 2027", "C, 2028 lower growth*", "C, 2028 forecast", "K or X, 2028 forecast"],
                [("Within 360k capacity", within), ("Above certified capacity", over), ("cap", [45] * 4)],
                "capacity", num_fmt='0"k"', legend=True)
plot = ch.plots[0]; plot.gap_width = 70; plot.overlap = 100
color_series(plot.series[0], "6DA7EC"); color_series(plot.series[1], CRIT); hide_series(plot.series[2])
color_point(plot.series[0], 3, BLUE)
drop_legend_entry(ch, 2)
for i, t in enumerate(("360k (100%)", "375k (104%)", "390k (108%)", "170k (47%)")):
    label_point(plot.series[2], i, t, pos=XL_LABEL_POSITION.INSIDE_BASE, color=INK)
ch.value_axis.minimum_scale = 0; ch.value_axis.maximum_scale = 450; ch.value_axis.major_unit = 50
s.text(8.8, 1.72, 4.03, 2.2,
       [{"text": "WHY CAPACITY RULES OUT OPTION C", "bold": True, "color": NAVY, "size": 9.5},
        {"text": "2027: 160k Central + 200k Eastern = 360k, with zero headroom for the national promotion or peaks", "bullet": True, "sb": 5},
        {"text": "2028: 169.6k + 220k = 389.6k, which is 29.6k orders over capacity", "bullet": True, "sb": 3},
        {"text": "Any positive growth breaches capacity; only zero growth fits, and then exactly at 100%", "bullet": True, "sb": 3}],
       size=10.5, fill=PALE, inset=0.14)
s.text(8.8, 4.07, 4.03, 2.78,
       [{"text": "THE FIX DOES NOT FIT THE PLAN", "bold": True, "color": NAVY, "size": 9.5},
        {"text": "Operations: absorbing East at Central with today's staffing (the consultant's June 2027 plan) puts Central at full practical load before any demand spike", "bullet": True, "sb": 5},
        {"text": "Expansion needs a two-quarter permit and a $1.1M retrofit that is not in the 2027 budget", "bullet": True, "sb": 3},
        {"text": "Capacity is not a reason to reject the cross-dock or K, because neither adds load to Central (47% in 2028)", "bullet": True, "sb": 3}],
       size=10.5, line=AXIS, inset=0.14)

# ================================================================== 12 BUDGET & LEASE
s = D.new()
frame(s, 1, "Retention and the deferral path fit easily within the $0.9M one-time authority; close-to-Central fits "
      "only if the $1.1M Central retrofit it needs is left unfunded", SRC + "2, 4, 6. *The cross-dock test cap of $0.25M is a Northline "
      "assumption, pending a provider quote.")
s.text(0.5, 1.72, 6.3, 0.3, "One-time network change cost, $M (board authority: $0.9M)", size=11, bold=True, color=INK, inset=0)
ch = base_chart(s, XL_CHART_TYPE.BAR_CLUSTERED, 0.4, 2.0, 6.4, 3.6,
                ["K  Retain + optimize", "D  K + cross-dock test", "X  Cross-dock", "C  Close to Central incl. retrofit"],
                [("One-time cost", [0.15, 0.40, 0.75, 1.85])], "one-time", num_fmt='"$"0.0"M"')
plot = ch.plots[0]; plot.gap_width = 55
ser = plot.series[0]
for i, col in enumerate((BLUE, BLUE, AQUA, ORANGE)):
    color_point(ser, i, col)
for i, t in enumerate(("$0.15M  (within)", "$0.40M*  (within)", "$0.75M  (within, $0.15M spare)", "$1.85M  (over)")):
    label_point(ser, i, t, size=10)
ch.category_axis.reverse_order = True
ch.value_axis.minimum_scale = 0; ch.value_axis.maximum_scale = 3.0; ch.value_axis.major_unit = 0.5
s.text(0.5, 5.75, 6.3, 1.1,
       [{"text": "Option C's $1.85M = $0.75M East exit and transfer + $1.1M Central retrofit. Without the retrofit, C leaves only "
                 "$0.15M of authority for customer migration; with it, C is over budget, and a two-quarter permit means the "
                 "retrofit could not be ready for a June 2027 closure.", "size": 10}], fill=PALE, inset=0.12, anchor="m")
s.text(7.2, 1.72, 5.63, 0.3, "LEASE POSITION BY OPTION", size=10, bold=True, color=NAVY, inset=0)
lt = [["Site", "Lease facts", "Implication"],
      ["East", "Exit in 2027 costs a one-time $0.75M; otherwise the lease expires in 2029", "Waiting to 2029 avoids the early-termination fee; this is the natural point to decide"],
      ["West", "Cannot be changed before 2030", "Outside this decision; West stays as-is"],
      ["Central", "Fixed cost unchanged in every option; any expansion needs a permit and a $1.1M retrofit", "No cost saving from adding load; expansion has to be budgeted for 2028 or later"],
      ["Cross-dock", "Two-year minimum at $0.85M a year; open to a termination-for-cause clause if the SLA is all-ZIP", "Signing in 2027 locks in about $1.7M of minimums before peak service is proven"]]
table(s, 7.2, 2.05, [1.0, 2.33, 2.3], lt, [0.36, 0.95, 0.62, 0.95, 0.95], size=9.5, head_size=9.5)
s.text(7.2, 6.05, 5.63, 0.8, "The board's rule that service cannot be degraded to win a freight discount also limits any "
       "attempt to close C's cost gap through cheaper, slower carriers.", size=10, color=INK, fill=PALEBLUE, inset=0.12, anchor="m")

# ================================================================== 13 SCORECARD
s = D.new()
frame(s, 2, "Only optimized retention (K, alone or with the test in D) passes all five tests. The cross-dock fails on "
      "cost and is unproven on service; close-to-Central fails four tests", SRC + "2–7; Northline analysis (slides 6–12).")
hdr = ["Option", "1  Economics", "2  Service (92% all-ZIP)", "3  Central capacity", "4  Funding and lease", "5  Risk and reversibility"]
sc = [
    ("SQ  Status quo", [("FAIL", "$0.30M a year dearer than K"), ("PASS", "95.1%"), ("PASS", "47% in 2028"), ("PASS", "$0"), ("PASS", "No change")]),
    ("K  Retain + optimize", [("PASS", "Cheapest: $8.44M (2027)"), ("PASS", "95.1%; watch shift changes"), ("PASS", "47% in 2028"), ("PASS", "$0.15M of $0.9M"), ("PASS", "Fully reversible")]),
    ("D  K + test, decide in 2028", [("PASS", "K's cost; ≤$0.25M buys the option"), ("PASS", "95.1%"), ("PASS", "47% in 2028"), ("PASS", "$0.40M of $0.9M"), ("PASS", "Generates the missing evidence")]),
    ("X  Close, use cross-dock", [("FAIL", "+$0.45M a year vs K (base case)"), ("UNPROVEN", "93.9% from non-peak pilot"), ("PASS", "Central unaffected"), ("PASS", "$0.75M; $0.15M spare"), ("FAIL", "Two-year minimum; nine months to reverse")]),
    ("C  Close, serve from Central", [("FAIL", "+$0.20M a year vs K; $0 saving vs SQ by 2028"), ("FAIL", "90.3%"), ("FAIL", "100% in 2027, 108% in 2028"), ("PARTLY", "$0.75M fits; $1.1M retrofit unbudgeted"), ("FAIL", "Nine months to reverse")]),
]
x0, y0 = 0.5, 1.75
cw = [2.33, 2.0, 2.0, 2.0, 2.0, 2.0]
s.text(x0, y0, cw[0], 0.42, hdr[0], size=10, bold=True, color=WHITE, fill=NAVY, anchor="m", inset=0.08)
cx = x0 + cw[0]
for i in range(1, 6):
    s.text(cx, y0, cw[i], 0.42, hdr[i], size=9.5, bold=True, color=WHITE, fill=NAVY, anchor="m", align="c", inset=0.05)
    cx += cw[i]
ry = y0 + 0.42
RH = 0.8
for ri, (name, cells) in enumerate(sc):
    fill = PALEBLUE if ri in (1, 2) else None
    if fill: s.rect(x0, ry, sum(cw), RH, fill=fill)
    s.text(x0, ry, cw[0], RH, name, size=10.5, bold=True, color=INK, anchor="m", inset=0.08)
    cx = x0 + cw[0]
    for i, (st, txt) in enumerate(cells):
        pill(s, cx + (cw[i + 1] - 0.95) / 2, ry + 0.09, st)
        s.text(cx + 0.05, ry + 0.38, cw[i + 1] - 0.1, 0.46, txt, size=9, color=INK2, align="c", inset=0.02)
        cx += cw[i + 1]
    ry += RH
    s.hline(x0, ry, sum(cw), color=GRID, lw=0.5)
s.text(0.5, 6.28, 12.33, 0.58,
       [{"runs": [("Read-across: ", True, NAVY),
                  ("K and D pass on today's evidence. D adds a cheap option on the cross-dock for the 2029 lease decision, so it is the "
                   "recommended path. 'Unproven' counts as a fail until a peak test is complete.", False, INK)]}],
       size=10.5, fill=PALE, anchor="m", inset=0.09)

# ================================================================== 14 VALUE OF DEFERRAL
s = D.new()
frame(s, 2, "Deferring the decision to the 2029 lease end costs little and answers the one contract question "
      "that could make the cross-dock worthwhile", SRC + "3, 6, 7. Reading B is a sensitivity, not the base case: the pack lists "
      "the $0.85M under fixed facility cost. *The ≤$0.25M test cost is an assumption.")
s.text(0.5, 1.72, 12.33, 0.3, "The cross-dock quote can be read two ways, and the answer swings its economics by $0.85M a year",
       size=11, bold=True, color=INK, inset=0)
rd = [["Cross-dock vs K, $M a year", "2027", "2028", "Implication"],
      ["Reading A (base case): $0.85M minimum is a fixed fee on top of $11 per order", "+0.45 cost", "+0.51 cost", "Never worth closing East at forecast volumes"],
      ["Reading B (sensitivity): $0.85M is a spend floor, credited against the $11-per-order charges", "–0.40 saving", "–0.34 saving", "Could be worth it if peak all-ZIP service is proven"]]
table(s, 0.5, 2.05, [5.2, 1.35, 1.35, 4.43], rd, [0.38, 0.62, 0.62], size=10, head_size=9.5, aligns=["l", "r", "r", "l"])
s.text(0.5, 3.85, 6.0, 0.3, "WHY WAITING BEATS CLOSING NOW, EVEN UNDER READING B", size=10, bold=True, color=NAVY, inset=0)
s.text(0.5, 4.15, 6.0, 2.7,
       [{"runs": [("Closing in 2027 gains little: ", True, INK), ("under Reading B the 2027–28 gain over K is $0.40M + $0.34M − $0.75M exit + $0.15M of K setup avoided = $0.14M over two years", False, INK)], "bullet": True},
        {"runs": [("Waiting avoids the early-exit fee: ", True, INK), ("the lease ends in 2029, so the $0.75M termination charge falls away (any transfer costs within it may remain)", False, INK)], "bullet": True, "sb": 5},
        {"runs": [("The downside is lopsided: ", True, INK), ("each point of Eastern service below 88.3% adds 2,000 late orders a year and pushes the network below the 92% contract floor, with penalties and nine months to reverse", False, INK)], "bullet": True, "sb": 5}],
       size=10.5, fill=PALE, inset=0.14)
s.text(6.85, 3.85, 5.98, 0.3, "WHAT THE DEFERRAL PATH COSTS AND BUYS", size=10, bold=True, color=NAVY, inset=0)
dv = [["", "Value"],
      ["K saving locked in now", "$0.30M a year"],
      ["Test cost (capped)*", "≤$0.25M one-time"],
      ["Early-exit fee avoided by waiting to 2029", "Up to $0.75M"],
      ["Cross-dock minimums not committed before proof", "About $1.7M over two years"],
      ["Decision date", "Q3 2028 board gate"]]
table(s, 6.85, 4.15, [3.75, 2.23], dv, [0.34, 0.38, 0.38, 0.38, 0.42, 0.38], size=10, head_size=9.5, aligns=["l", "r"])
s.text(6.85, 6.5, 5.98, 0.36, "Close-to-Central is dropped, not deferred: it loses to K at any volume above 160k.",
       size=10, bold=True, color=NAVY, inset=0.0, anchor="m")

# ================================================================== 15 ROADMAP
s = D.new()
frame(s, 2, "Execute in three steps: optimize East now, test the cross-dock through peak and promotion, and "
      "take the 2029 lease decision at a Q3 2028 gate", SRC + "6, 7. Timing assumes the 2029 lease expiry leaves at least "
      "six months after the gate; confirm the exact expiry date. The gate thresholds are proposals.")
phases = [("Q1–Q2 2027", "1  Optimize East (Option K)",
           ["Approve $0.15M for systems changes",
            "Renegotiate East staffing shifts; set up the low-volume SKU transfer buffer",
            "Guardrail: East all-ZIP two-day rate at or above 95%, tracked weekly",
            "Confirm East can handle 220k orders in 2028"]),
          ("Q2 2027 – Q2 2028", "2  Test the cross-dock",
           ["Negotiate a test contract: all-ZIP SLA, termination for cause, how the minimum is treated",
            "Route a sample of Eastern orders, including rural ZIPs, through holiday 2027 and spring 2028",
            "Measure the all-ZIP rate, peak weeks, damage and cost per order"]),
          ("Q3 2028", "3  Board gate: 2029 lease",
           ["Close East at lease end only if all four gate criteria are met",
            "Otherwise renew East and keep optimizing",
            "Either way, transition before the 2029 expiry"])]
x = 0.5
for i, (when, head, items) in enumerate(phases):
    w = 3.95
    s.text(x, 1.75, w, 0.38, when, size=10, bold=True, color=WHITE, fill=NAVY if i < 2 else BLUE, anchor="m", inset=0.08,
           shape=MSO_SHAPE.PENTAGON if i < 2 else None)
    s.text(x, 2.22, w - 0.15, 0.38, head, size=12, bold=True, color=NAVY, inset=0.02)
    s.text(x, 2.62, w - 0.15, 1.95, [{"text": t, "bullet": True, "sb": 0 if j == 0 else 3} for j, t in enumerate(items)],
           size=10, color=INK, inset=0.02)
    x += 4.19
s.hline(0.5, 4.62, 12.33, color=AXIS)
s.text(0.5, 4.72, 6.6, 0.3, "Q3 2028 GATE: CLOSE EAST AT LEASE END ONLY IF ALL FOUR HOLD", size=10, bold=True, color=NAVY, inset=0)
gt = [["Gate criterion", "Threshold"],
      ["Cross-dock service", "≥92% all-ZIP over the test; ≥90% in peak weeks"],
      ["Network SLA (modeled)", "≥93.5%, keeping a 1.5-pt buffer"],
      ["Cross-dock cost", "At least $0.2M a year below K at forecast volume"],
      ["Contract", "All-ZIP SLA, termination for cause, budget fit"]]
table(s, 0.5, 5.02, [2.3, 4.3], gt, [0.34, 0.37, 0.37, 0.37, 0.37], size=10, head_size=9.5)
s.text(7.45, 4.72, 5.38, 2.13,
       [{"text": "DECISIONS REQUESTED FROM THE BOARD TODAY", "bold": True, "color": "B7D3F6", "size": 9.5},
        {"text": "1  Keep East open in 2027; do not serve the East region from Central", "color": WHITE, "sb": 6, "bold": True},
        {"text": "2  Approve Option K ($0.15M one-time)", "color": WHITE, "sb": 4, "bold": True},
        {"text": "3  Authorize a cross-dock test of up to $0.25M with an all-ZIP SLA and no two-year minimum (subject to provider agreement)", "color": WHITE, "sb": 4, "bold": True},
        {"text": "4  Schedule the 2029 lease gate for Q3 2028", "color": WHITE, "sb": 4, "bold": True}],
       size=10.5, fill=NAVY, inset=0.16)

# ================================================================== 16 RISKS
s = D.new()
frame(s, 2, "The recommendation holds under the main uncertainties. Each one has a monitoring trigger and a "
      "planned response", SRC + "4, 5, 7; Northline analysis.")
rk = [["Risk or uncertainty", "Effect on the recommendation", "Mitigation or trigger"],
      ["K's $0.30M saving does not materialize (audit estimate)", "Still the right call: the status quo ($8.74M) beats the cross-dock ($8.89M), and close-to-Central fails the SLA and capacity tests regardless", "Track savings quarterly; stop the shift changes if service suffers"],
      ["Shift renegotiation hurts East service", "Headroom is 7.7 pts on the Eastern rate (96% vs 88.3%)", "Weekly all-ZIP tracking; act if East drops below 95%"],
      ["Growth falls short (marketplace promotion not contracted)", "Closure still loses: 2027 volume is already 200k, above every break-even except C vs status quo (220k)", "Rerun break-evens at the Q3 2028 gate with actual volumes"],
      ["Growth beats forecast", "East site capacity is not stated in the pack; 220k is assumed to fit", "Confirm East capacity in the Q1 2027 audit"],
      ["Customer retention response to service is unknown", "Not used: the 92% contract floor binds regardless; Marketing's 8-pt claim is confounded", "Run a controlled renewal analysis (by account size and sales coverage)"],
      ["Cross-dock peak performance, damage rate and contract terms are unknown", "These are exactly what the test resolves; no commitment before the gate", "Gate criteria on slide 15"],
      ["Central permit timing is unknown", "Matters only for close-to-Central, which is dropped", "None needed now"]]
table(s, 0.5, 1.75, [3.4, 5.0, 3.93], rk, [0.36, 0.66, 0.5, 0.66, 0.5, 0.66, 0.62, 0.42], size=9.5, head_size=9.5, zebra=True)

# ================================================================== 17 APPX COST MODEL
s = D.new()
frame_appx(s, "Cost model detail: every option is built from the same rates, volumes and fixed costs in the briefing pack",
           SRC + "3, 4, 6. Totals may not add due to rounding. 2028 = East 220k, Central 169.6k, West 140k.")
am = [["Line item ($M)", "Basis", "SQ 2027", "K 2027", "C 2027", "X 2027", "SQ 2028", "K 2028", "C 2028", "X 2028"],
      ["East-region transport", "SQ/K $8, C $13, X $11 per order", "1.60", "1.60", "2.60", "2.20", "1.76", "1.76", "2.86", "2.42"],
      ["Central transport", "Central orders × $9", "1.44", "1.44", "1.44", "1.44", "1.53", "1.53", "1.53", "1.53"],
      ["West transport", "140k × $10", "1.40", "1.40", "1.40", "1.40", "1.40", "1.40", "1.40", "1.40"],
      ["East fixed", "$1.30M; K –$0.30M", "1.30", "1.00", "–", "–", "1.30", "1.00", "–", "–"],
      ["Central + West fixed", "$1.80M + $1.20M", "3.00", "3.00", "3.00", "3.00", "3.00", "3.00", "3.00", "3.00"],
      ["Cross-dock minimum", "$0.85M a year (Reading A)", "–", "–", "–", "0.85", "–", "–", "–", "0.85"],
      ["Extra damage", "C: $0.20M (held flat)", "–", "–", "0.20", "–", "–", "–", "0.20", "–"],
      ["All-in annual cost", "", f2(c27["SQ"]), f2(c27["K"]), f2(c27["C"]), f2(c27["X"]), f2(c28["SQ"]), f2(c28["K"]), f2(c28["C"]), f2(c28["X"])],
      ["One-time (2027)", "Systems $0.15M; exit $0.75M", "–", "0.15", "0.75", "0.75", "", "", "", ""],
      ["Memo: X under Reading B", "Minimum credited against charges", "", "", "", f2(cost(E, C0, 'X', True)), "", "", "", f2(cost(E28, C28, 'X', True))]]
table(s, 0.5, 1.75, [2.1, 2.75, 0.935, 0.935, 0.935, 0.935, 0.935, 0.935, 0.935, 0.935], am,
      [0.4] + [0.4] * 7 + [0.42, 0.4, 0.4], size=9.5, head_size=9, aligns=["l", "l"] + ["r"] * 8, row_fills={8: PALEBLUE})
s.text(0.5, 6.25, 12.33, 0.6, "Not modeled because the pack gives no figure: the carrier surcharge for C, the $1.1M retrofit "
       "(timing), returns and replacements, customer penalties, and any change in Central's 94% service under full load.",
       size=9.5, color=INK2, fill=PALE, inset=0.12, anchor="m")

# ================================================================== 18 APPX ASSUMPTIONS / CHOICES
s = D.new()
frame_appx(s, "Analyst choices made without client input. Each is stated so the board can challenge it",
           SRC + "2–7. These choices were made because the pack is silent or ambiguous; none changes the recommendation except where noted.")
ch_rows = [["Topic", "Choice made", "Why, and sensitivity"],
           ["Cross-dock $0.85M minimum", "Treated as a fixed fee on top of $11 per order (Reading A)", "Listed under fixed facility cost. Under Reading B the cross-dock would be $0.34–0.40M a year cheaper than K, but still unproven on service: this is why we test, not close"],
           ["Where K's $0.30M lands", "Reduction of East facility and operating cost", "Placement does not affect totals"],
           ["Damage under C in 2028", "Held at $0.20M (not scaled to volume)", "Scaling would make C worse by $0.02M"],
           ["Central and West service", "Stay at 94% and 95% in every option", "Generous to C: Central at 100% load would probably slip"],
           ["Cross-dock test cost", "Capped at $0.25M; no two-year minimum", "No test quote in the pack (only a two-year minimum); needs provider agreement"],
           ["Lower-growth case", "Half the forecast (East +5%, Central +3%)", "Pack asks for one but does not size it; capacity fails at any growth above zero"],
           ["Gate timing", "Q3 2028, before the 2029 lease expiry", "Expiry month not given; allows six or more months to transition"],
           ["Deck format", "16:9 PowerPoint with native, editable charts", "Board pre-read and presentation use"]]
table(s, 0.5, 1.75, [2.4, 4.2, 5.73], ch_rows, [0.36, 0.62, 0.42, 0.42, 0.42, 0.42, 0.5, 0.42, 0.42], size=9.5, head_size=9.5, zebra=True)

D.save(OUT)
D.previews(PREV)
print("\n".join(D.warnings) if D.warnings else "no overflow warnings")
