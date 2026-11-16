import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from decklib import *

OUT = sys.argv[1]
PREV = sys.argv[2]
os.makedirs(PREV, exist_ok=True)
D = Deck()
TOTAL_SLIDES = 21
SRC = "Source: Harlow Fresh Markets briefing pack (synthetic data); team analysis."


def header(section, title):
    D.slide()
    if section:
        D.text(0.5, 0.28, 9, 0.3, Para(section.upper(), size=9.5, bold=True, color=BLUE), margin=0)
    D.text(0.5, 0.55, 12.3, 0.95, Para(title, size=20, bold=True, color=INK), margin=0)
    D.line(0.5, 1.52, 12.83, 1.52, color=INK, lw=0.75)


def footer(src=SRC):
    D.line(0.5, 6.98, 12.83, 6.98, color=RULE, lw=0.5)
    D.text(0.5, 7.02, 11.3, 0.4, Para(src, size=8, color=MUTED), margin=0)
    D.text(11.9, 7.02, 0.93, 0.3, Para(str(D.n), size=8, color=MUTED, align="r"), margin=0)


def P(t, **k):
    k.setdefault("size", 12)
    return Para(t, **k)


def B(t, **k):
    k.setdefault("size", 12); k.setdefault("bullet", True); k.setdefault("space_before", 4)
    return Para(t, **k)


def table(x, y, colw, rows, rowh=0.36, size=10.5, header=True, hl=None, bold_last=False, aligns=None,
          hfill=None, valign="m", rowhs=None):
    hl = hl or {}
    cy = y
    for ri, row in enumerate(rows):
        rh = rowhs[ri] if rowhs else rowh
        is_h = header and ri == 0
        fill = hl.get(ri)
        if is_h and hfill:
            fill = hfill
        if fill:
            D.rect(x, cy, sum(colw), rh, fill=fill)
        cx = x
        for ci, cell in enumerate(row):
            al = (aligns[ci] if aligns else ("l" if ci == 0 else "c"))
            if isinstance(cell, Para):
                p = cell
            else:
                b = is_h or (bold_last and ri == len(rows) - 1)
                p = Para(str(cell), size=size if not is_h else size - 0.5, bold=b,
                         color=(INK2 if is_h else INK), align=al)
            D.text(cx, cy, colw[ci], rh, p, valign=valign, margin=0.05)
            cx += colw[ci]
        cy += rh
        D.line(x, cy, x + sum(colw), cy, color=(INK if is_h else RULE), lw=(0.75 if is_h else 0.5))
    return cy


def waterfall(x, y, w, h, items, fmt=lambda v: f"{v:+.1f}", tfmt=lambda v: f"{v:.1f}", lab=10, catsize=9.5,
              catlines=3, ymin=None, ymax=None, barfrac=0.6, connectors=True):
    """items: (label, value, kind[, color]) kind in total|delta|abs"""
    lv, bars, run = [], [], 0
    for it in items:
        lbl, v, kind = it[:3]
        col = it[3] if len(it) > 3 else None
        if kind == "total":
            lo, hi = sorted((0, v)); run = v
            col = col or INK2
            txt = tfmt(v).replace("-", "−")
        else:
            lo, hi = sorted((run, run + v)); run += v
            col = col or (BLUE if v >= 0 else RED)
            txt = fmt(v).replace("-", "−")
        bars.append((lbl, lo, hi, col, txt, v, kind)); lv += [lo, hi]
    vmin = min(0, min(lv)) if ymin is None else ymin
    vmax = max(lv) if ymax is None else ymax
    cat_h = 0.17 * catlines + 0.1
    top, bot = y + 0.32, y + h - cat_h - (0.3 if vmin < 0 else 0)
    sc = (bot - top) / (vmax - vmin)
    Y = lambda v: bot - (max(v, vmin) - vmin) * sc
    n = len(bars); slot = w / n; bw = slot * barfrac
    D.line(x, Y(max(0, vmin)), x + w, Y(max(0, vmin)), color=GRAY, lw=0.75)
    prev = None
    for i, (lbl, lo, hi, col, txt, v, kind) in enumerate(bars):
        bx = x + i * slot + (slot - bw) / 2
        D.rect(bx, Y(hi), bw, max(Y(lo) - Y(hi), 0.012), fill=col)
        up = (kind == "total" and v >= 0) or (kind != "total" and v >= 0)
        if up:
            D.text(bx - 0.25, Y(hi) - 0.27, bw + 0.5, 0.26, Para(txt, size=lab, bold=True, color=INK, align="c"), margin=0, valign="b")
        else:
            D.text(bx - 0.25, Y(lo) + 0.02, bw + 0.5, 0.26, Para(txt, size=lab, bold=True, color=INK, align="c"), margin=0)
        if prev is not None and connectors:
            D.line(prev[0], Y(prev[1]), bx, Y(prev[1]), color=GRAY, lw=0.5)
        endlvl = v if kind == "total" else (hi if v >= 0 else lo)
        prev = (bx + bw, endlvl)
        D.text(x + i * slot + 0.02, y + h - cat_h + 0.02, slot - 0.04, cat_h, [Para(t, size=catsize, color=INK2, align="c") for t in lbl.split("\n")], margin=0)
    return Y


def numbered(x, y, n, size=0.34, fill=BLUE):
    D.text(x, y, size, size, Para(str(n), size=11, bold=True, color="FFFFFF", align="c"), fill=fill, valign="m", margin=0)


# =========================================================== 1 Title
D.slide()
D.rect(0, 0, 13.333, 7.5, fill="FFFFFF")
D.rect(0.5, 2.2, 0.09, 2.2, fill=BLUE)
D.text(0.8, 2.1, 11.5, 1.5, [P("Restoring Harlow's operating margin", size=32, bold=True),
                             P("Fix gross margin and delivery economics first; rebalance labor rather than cut it", size=18, color=INK2, space_before=8)])
D.text(0.8, 3.75, 11, 0.8, [P("Board of Directors meeting · February 2027", size=13, color=INK2),
                            P("Prepared for Dana Whitfield, Chief Executive Officer", size=13, color=INK2, space_before=2)])
D.text(0.8, 6.55, 11.8, 0.5, P("Based solely on the company briefing pack. All company data in the pack are synthetic (generated for a reasoning benchmark). $ in millions unless stated; fiscal years end in January.",
                               size=9, color=MUTED), margin=0)

# =========================================================== 2 Executive summary
header("Executive summary", "Fix promotions, shrink and delivery pricing, rebalance labor and exit loss-making stores: margin returns to ~2.9–3.1% by FY2028. The 8% labor cut should not go ahead.")
rows = [
    ("Diagnosis", "Gross margin and e-commerce delivery explain ~80% of the 2.4-point margin decline. Wages explain 13%.",
     ["More promotions (24%→29% of sales) and higher shrink (2.1%→2.6%) fully explain the gross-margin loss. 38% of FY2025 promotion events lost money.",
      "E-commerce loses ~$10M a year once third-party delivery and cannibalisation are counted. The team reports a 6.1% profit."]),
    ("Plan", "Eight actions add ~$29M of operating income. After the 2027 wage step, FY2028 operating income is ~$41M (2.9%).",
     ["Gross margin +$16.3M (promotions, vendor funding, private label, shrink). Labor rebalance +$3.6M. Delivery pricing +$2.5M. Exiting nine stores +$6.6M.",
      "Taking shrink back to FY2023's 2.1% closes the gap to the 3.0% target (3.1%). One-time cost is ~$20M, inside the $25M cap."]),
    ("First moves", "Four fast, low-cost moves start this quarter. Within ~6 months they lift run-rate operating income to ~$26M, above the $20M covenant.",
     ["Roll out the tested delivery fee. Drop loss-making promotions. Rebalance labor hours instead of cutting 8%. Give notice on the six leases that expire.",
      "The 8% cut saves $14.5M on paper. If shrink responds as it did in FY2023–25, ~$10M of that comes back as shrink, and fresh produce (the top reason to shop at Harlow) suffers."]),
    ("Risks", "Even in the low case, FY2028 operating income is ~$27M (2.0%). ValuMart's response and vendor funding are the largest uncertainties.",
     ["Stage gates in Q2 and Q4 FY2027. Contingency levers if we fall behind: shrink stretch, delivery contract re-tender, a further targeted hours trim.",
      "Board decisions: approve the plan and budget, withdraw the blanket cut, vote on three store exits, and confirm 'delivery in some form' with the owners."]),
]
y0 = 1.72
for i, (tag, head, subs) in enumerate(rows):
    yy = y0 + i * 1.3
    numbered(0.5, yy + 0.02, i + 1)
    D.text(0.95, yy - 0.02, 1.45, 0.4, P(tag, size=12, bold=True, color=BLUE), margin=0.03)
    D.text(2.45, yy - 0.04, 10.4, 0.5, P(head, size=12, bold=True), margin=0.03)
    D.text(2.45, yy + 0.5, 10.4, 0.72, [B(s, size=10.5, color=INK2, space_before=1) for s in subs], margin=0.03)
    if i < 3:
        D.line(0.5, yy + 1.22, 12.83, yy + 1.22, color=RULE, lw=0.5)
footer()

# =========================================================== 3 Hypothesis
header("Approach", "We started from the hypothesis that commercial fixes alone would be enough. They reach only ~2.1%, so labor rebalancing and store exits are also needed.")
D.text(0.5, 1.68, 6.05, 0.82, [P("Initial answer", size=10, bold=True, color=BLUE),
                               P("The decline is commercial, not wage-driven. Fix promotions and e-commerce pricing; avoid labor cuts and store closures.", size=11)],
       fill=PANEL, margin=0.1)
D.text(6.78, 1.68, 6.05, 0.82, [P("Revised answer", size=10, bold=True, color=BLUE),
                                P("Commercial fixes lead, but labor must be rebalanced and the nine loss-making stores exited to reach ~2.9–3.1%.", size=11)],
       fill=BLUE_L, margin=0.1)
rows = [["What would have to be true", "Test against the evidence", "Result", "Verdict"],
        ["1. Wages are not the main cause", "Store labor's share of the 2.36-pt margin decline", "0.30 pt = 13% of the decline", P("Holds", size=10.5, bold=True, color=GREEN, align="c")],
        ["2. The gross-margin loss is controllable (mix and shrink, not cost of goods)", "Promotion, private-label and shrink effects vs. the −1.02-pt fall", "−0.70 −0.50 +0.18 = −1.02 pt: fully explained", P("Holds", size=10.5, bold=True, color=GREEN, align="c")],
        ["3. E-commerce destroys value and pricing can fix it", "True incremental contribution; 4-store fee test", "−$10.4M a year; tested pricing recovers $2.5M, leaving −$7.6M", P("Partly: contain, don't grow", size=10.5, bold=True, color=AMBER, align="c")],
        ["4. Store hours cannot be cut safely", "Shrink by store labor-intensity quartile", "Q1 3.1% vs Q4 2.3%, but Q3 ≈ Q4 (2.4% vs 2.3%)", P("Partly: no blanket cut; a targeted trim is safe", size=10.5, bold=True, color=AMBER, align="c")],
        ["5. Commercial + e-commerce levers alone reach 3.0%", "Sized levers less the 2027 wage step", "~$31M operating income = ~2.1%", P("Fails: add labor rebalance and store exits", size=10.5, bold=True, color=RED, align="c")]]
table(0.5, 2.7, [3.6, 3.3, 3.3, 2.13], rows, rowh=0.68, size=10.5, rowhs=[0.36] + [0.7] * 5, aligns=["l", "l", "l", "c"])
footer("Source: briefing pack Tables 1–5; team analysis. Verdict on hypothesis 5 uses the plan sizing on pages 8–12 without labor and store actions.")

# =========================================================== 4 Margin bridge
header("1 · Diagnosis", "Operating margin fell 2.4 points in two years. Gross margin and e-commerce fulfillment drove ~80% of the fall; store labor drove 13%.")
waterfall(0.5, 1.75, 8.1, 4.95, [
    ("FY2023 operating margin", 3.37, "total"),
    ("Gross margin", -1.02, "delta"),
    ("E-commerce fulfillment", -0.84, "delta"),
    ("Store labor", -0.30, "delta"),
    ("Occupancy & energy", -0.20, "delta"),
    ("Other SG&A", 0.00, "delta", GRAY),
    ("FY2025 operating margin", 1.02, "total")],
    fmt=lambda v: f"{v:+.2f} pt" if v else "0.00 pt", tfmt=lambda v: f"{v:.2f}%", lab=11, catlines=2)
D.text(0.5, 1.62, 8, 0.3, P("Operating margin bridge, FY2023→FY2025, % of sales", size=10, bold=True, color=INK2), margin=0)
rows = [["Driver", "pt", "$M, FY25 sales", "Share"],
        ["Gross margin", "−1.02", "−15.3", "43%"],
        ["E-com fulfillment", "−0.84", "−12.6", "36%"],
        ["Store labor", "−0.30", "−4.5", "13%"],
        ["Occupancy & energy", "−0.20", "−3.0", "8%"],
        ["Other SG&A", "0.00", "0.0", "0%"],
        ["Total", "−2.36", "−35.4", "100%"]]
table(8.95, 1.75, [1.45, 0.75, 1.15, 0.53], rows, rowh=0.3, size=9.5, bold_last=True)
D.text(8.95, 4.0, 3.88, 2.15, [P("What this means", size=10.5, bold=True, color=BLUE),
                              B("Sales grew $83M (+5.8%), yet operating income fell $32.6M, from $47.9M to $15.3M.", size=10),
                              B("Management's diagnosis (wages) covers only 13% of the fall. A plan built around labor cannot reach 3.0%.", size=10),
                              B("The two big drivers are commercial choices: promotional intensity and how delivery is priced.", size=10)],
       fill=PANEL, margin=0.1)
footer("Source: briefing pack Table 1. Each line's effect = change in its ratio to sales. The $M column applies each ratio change to FY2025 sales of $1,503M, so it totals more than the $32.6M fall in operating income, which is net of sales growth.")

# =========================================================== 5 Labor & shrink
header("1 · Diagnosis", "Wages rose 9.4%, but fewer hours per $ of sales absorbed most of it. The thinner staffing now shows up as shrink.")
rows = [["Store labor", "FY2023", "FY2025", "Change"],
        ["Avg hourly wage incl. benefits", "$16.80", "$18.38", "+9.4%"],
        ["Labor hours per $1,000 of sales", "7.02", "6.60", "−6.0%"],
        ["Labor cost per $1,000 of sales", "$117.9", "$121.3", "+2.9%"],
        ["Store labor, % of sales", "11.8%", "12.1%", "+0.3 pt"]]
table(0.5, 1.75, [2.75, 0.95, 0.95, 0.95], rows, rowh=0.34, size=10.5)
D.text(0.5, 3.6, 5.6, 1.6, [P("Decomposition of the labor-ratio change, % of sales", size=10, bold=True, color=INK2),
                            B("Wage effect at FY2023 hours: 7.02 × ($18.38 − $16.80) ÷ 1,000 = +1.11 pt (≈ $16.7M)", size=10),
                            B("Hours effect: (6.60 − 7.02) × $18.38 ÷ 1,000 = −0.77 pt (≈ −$11.6M)", size=10),
                            B("Net ≈ +0.34 pt, which matches the reported +0.3 pt within rounding (≈ $4.5M)", size=10)], margin=0.02)
D.text(0.5, 5.35, 5.6, 1.05, [P("So what", size=10.5, bold=True, color=BLUE),
                              P("Shrink rose 0.5 pt (≈ $7.5M), more than the $4.5M net rise in labor cost. Further across-the-board cuts would repeat the trade that is already hurting margin.", size=10.5)],
       fill=PANEL, margin=0.1)
D.text(6.6, 1.62, 6.2, 0.3, P("Shrink by store labor intensity, FY2025, % of sales", size=10, bold=True, color=INK2), margin=0)
waterfall(6.6, 1.85, 6.2, 3.35, [("Q1\nfewest hours", 3.1, "total", RED), ("Q2", 2.7, "total", GRAY), ("Q3", 2.4, "total", GRAY), ("Q4\nmost hours", 2.3, "total", GRAY)],
          tfmt=lambda v: f"{v:.1f}%", lab=11, catlines=2, ymax=3.3, barfrac=0.5, connectors=False)
D.text(6.6, 5.25, 6.23, 1.55, [B("The lowest-labor quartile runs 0.8 pt more shrink than the highest. Its managers say produce rotation and receiving checks are skipped on busy days.", size=10, space_before=0),
                               B("Q3 and Q4 differ by only 0.1 pt, so hours in the most labor-intensive stores can be trimmed with little shrink risk.", size=10),
                               B("Mix of shrink: produce and fresh waste 45%, theft 35%, admin and receiving errors 20%.", size=10)], margin=0.04)
footer("Source: briefing pack Tables 3–4 and store-manager comments. Quartiles rank stores by labor hours per $1,000 of sales. The quartile view is a correlation; it is consistent with, but does not prove, that low hours cause shrink.")

# =========================================================== 6 Gross margin
header("1 · Diagnosis", "Heavier promotions and rising shrink fully explain the gross-margin loss. The extra promotions did not make customers see Harlow as better value.")
D.text(0.5, 1.62, 5.8, 0.3, P("Gross-margin bridge FY2023→FY2025, % of sales", size=10, bold=True, color=INK2), margin=0)
waterfall(0.5, 1.8, 5.9, 4.0, [("FY2023 gross margin", 26.04, "total"), ("Promotion mix\n+5.0 pt × −14 pt", -0.70, "delta"),
                               ("Shrink\n2.1%→2.6%", -0.50, "delta"), ("Private label\n+1.5 pt × +12 pt", 0.18, "delta"),
                               ("FY2025 gross margin", 25.02, "total")],
          fmt=lambda v: f"{v:+.2f} pt", tfmt=lambda v: f"{v:.2f}%", lab=10.5, catlines=3, ymin=24.4, ymax=26.3)
D.text(0.5, 5.85, 5.9, 0.95, P("The axis starts at 24.4%. The three drivers sum to −1.02 pt, exactly the reported fall. The promotion and private-label margin gaps did not change, so those two effects are purely about mix.", size=9.5, color=INK2), margin=0.02)
D.text(6.75, 1.7, 6.08, 5.1, [
    P("Promotions are not paying back", size=12, bold=True, color=BLUE),
    B("38% of FY2025 promotion events lost money even after counting the extra units they sold.", size=10.5),
    B("Vendor funding fell from 55% to 46% of promotional markdowns, so Harlow pays for more of each event.", size=10.5),
    B("Price perception got worse: 41% of shoppers now call Harlow 'more expensive', up from 33%.", size=10.5),
    B("The category team says deep-promotion stores grew comps 1.8% vs 0.2%. But 1.6 pt of extra sales at 20¢ contribution is worth 0.32% of sales. It pays only if those stores carry less than 2.3 pt of extra promotion share (0.32 ÷ 0.14). Comps are not profit, and the comparison is not controlled for location.", size=10.5),
    P("Shrink and private label", size=12, bold=True, color=BLUE, space_before=10),
    B("Shrink is $39M a year (2.6% of sales). Every 0.1 pt is worth ~$1.5M.", size=10.5),
    B("Private label is the one positive: each extra point of share adds ~$1.8M of gross profit.", size=10.5)], margin=0.02)
footer("Source: briefing pack Table 2, §5 notes, §9 customer survey (n = 3,100), §10 category-team claim; team analysis.")

# =========================================================== 7 E-commerce
header("1 · Diagnosis", "Counting third-party delivery and cannibalised store sales, e-commerce loses ~$10M a year. Each home delivery loses ~$12.")
D.text(0.5, 1.62, 7.4, 0.3, P("True annual contribution of e-commerce, FY2025, $M", size=10, bold=True, color=INK2), margin=0)
waterfall(0.5, 1.8, 7.4, 4.25, [("Contribution on new-to-Harlow sales\n30% × $127.8M × 20¢", 7.67, "total", BLUE),
                                ("Picking\n1,331k orders × $7.40", -9.85, "delta"),
                                ("3rd-party delivery\n772k × $13.80", -10.65, "delta"),
                                ("Delivery fees\n772k × $3.10", 2.39, "delta"),
                                ("True e-commerce contribution", -10.44, "total", RED)],
          fmt=lambda v: f"{v:+.1f}", tfmt=lambda v: f"{v:+.1f}", lab=11, catlines=3)
rows = [["Per order, FY2025", "Collect", "Delivered"],
        ["Contribution ($96 × 30% new × 20¢)", "$5.76", "$5.76"],
        ["Picking", "−$7.40", "−$7.40"],
        ["Delivery net of fee ($13.80 − $3.10)", "–", "−$10.70"],
        ["Contribution per order", "−$1.64", "−$12.34"]]
table(8.2, 1.8, [2.75, 0.9, 0.98], rows, rowh=0.36, size=10, bold_last=True)
D.text(8.2, 3.75, 4.63, 2.6, [P("Why the team's '6.1% profit' is wrong", size=10.5, bold=True, color=BLUE),
                               B("It leaves out third-party delivery, which costs $8.3M net of fees and is booked in 'E-commerce fulfillment'.", size=10),
                               B("It counts every online sale as new to Harlow. Customers say 70% would otherwise have been bought in a Harlow store.", size=10),
                               B("Net fulfillment cost rose from $5.2M to $18.1M as orders tripled and home delivery's share rose from 45% to 58%. Growth made the loss bigger.", size=10)],
       fill=PANEL, margin=0.1)
footer("Source: briefing pack Table 5, §7 customer survey (n = 2,300) and finance contribution estimate, §10 e-commerce update. The picking, delivery and fee lines reconcile to the $18.1M fulfillment line in Table 1.")

# =========================================================== 8 Plan overview
header("2 · The plan", "Eight actions add ~$29M a year. After the 2027 wage step, FY2028 operating income reaches ~$41M (2.9%). A shrink stretch closes the gap to 3.0%.")
D.text(0.5, 1.62, 9, 0.3, P("Operating income bridge, FY2025 → FY2028 base case, $M (FY2025 prices)", size=10, bold=True, color=INK2), margin=0)
Y = waterfall(0.5, 1.8, 9.2, 4.7, [("FY2025", 15.3, "total"), ("Promotions", 5.1, "delta"), ("Vendor funding", 3.6, "delta"),
                                   ("Private label", 3.4, "delta"), ("Shrink", 4.2, "delta"), ("Labor rebalance", 3.6, "delta"),
                                   ("Delivery pricing", 2.5, "delta"), ("Exit 6 stores at lease end", 4.4, "delta"), ("Exit 3 stores (board vote)", 2.2, "delta"),
                                   ("2027 wage step", -3.6, "delta"), ("FY2028 base", 40.7, "total", BLUE_D)],
              lab=10, catsize=9, catlines=3, ymax=46)
D.line(0.5, Y(41.9), 0.5 + 10 * 9.2 / 11, Y(41.9), color=INK, lw=0.75, dash=True)
D.text(0.55, Y(41.9) - 0.27, 3.6, 0.25, P("3.0% target = $41.9M on FY2028 sales of ~$1,398M", size=9, color=INK), margin=0)
# brackets for groups
for (a, b, lbl) in [(1, 4, "Gross margin +16.3"), (5, 5, "Labor +3.6"), (6, 6, "E-com +2.5"), (7, 8, "Stores +6.6")]:
    slot = 9.2 / 11
    D.line(0.5 + a * slot + 0.06, 6.62, 0.5 + (b + 1) * slot - 0.06, 6.62, color=BLUE, lw=1.25)
    D.text(0.5 + a * slot, 6.64, (b - a + 1) * slot, 0.28, P(lbl, size=9, bold=True, color=BLUE, align="c"), margin=0)
D.text(9.95, 1.8, 2.88, 3.35, [P("Reading the bridge", size=10.5, bold=True, color=BLUE),
                               B("Every action maps to one P&L line: gross margin, store labor, e-commerce fulfillment, or store portfolio (four-wall). Other SG&A has stayed flat at 4.7% of sales, so the plan has no lever there.", size=9.5),
                               B("Base case = 2.9% (40.7 ÷ 1,398). Stretch: shrink back to FY2023's 2.1% adds $2.8M → $43.5M = 3.1%.", size=9.5),
                               B("Store exits lower sales by $88.5M (the 75% not transferred), which lifts the margin ratio.", size=9.5),
                               B("Wage step: +4% minimum wage = $7.3M; we assume half is recovered in pricing.", size=9.5)],
       fill=PANEL, margin=0.1)
footer("Source: team analysis on briefing pack data; calculations on pages 9–12 and in the appendix. Constant FY2025 prices; no real like-for-like growth assumed.")

# =========================================================== 9 Commercial levers
header("2 · The plan", "Four gross-margin actions add ~$16M. The largest is dropping the promotion events that already lose money.")
rows = [["Action", "FY2025", "FY2028 goal", "Calculation", "$M / yr"],
        ["Promotions: cut the loss-making events first; promotion share back toward FY2023", "29.0% of sales", "25.0%",
         "4 pt × 14 pt margin gap × $1,412M = $7.9M; less 1% volume loss ($14.1M × 20¢ = $2.8M)", "+5.1"],
        ["Vendor funding: make funding a condition of promotion slots", "46% of markdowns", "50%",
         "Markdowns ≈ 14 pt ÷ (1 − 46%) = 25.9% of promoted sales; 25% × $1,398M × 25.9% = $90.6M × 4 pt", "+3.6"],
        ["Private label: extend range in fresh and staples", "18.5% of sales", "20.5%",
         "2 pt × 12 pt margin gap × $1,398M; trend was +0.75 pt a year in FY2023–25", "+3.4"],
        ["Shrink: produce rotation, receiving checks, loss prevention", "2.6% of sales", "2.3%",
         "0.3 pt × $1,398M; Q3–Q4 stores already run 2.3–2.4%. Stretch 2.1% (FY2023) adds +$2.8M", "+4.2"],
        ["Total gross-margin actions", "", "", "", "+16.3"]]
table(0.5, 1.75, [3.4, 1.35, 1.1, 5.43, 1.05], rows, rowh=0.72, size=10.5, rowhs=[0.36, 0.78, 0.78, 0.72, 0.78, 0.38], bold_last=True,
      aligns=["l", "c", "c", "l", "c"], hl={5: PANEL})
D.text(0.5, 5.75, 6.05, 1.1, [P("Trade-off: traffic vs margin", size=10.5, bold=True, color=BLUE),
                              P("Cutting promotions risks traffic in the stores that compete with ValuMart (comps −4.2% there). Mitigation: cut the loss-making events first, and if needed reinvest up to $2M in everyday prices on key items in those stores.", size=10)],
       fill=PANEL, margin=0.1)
D.text(6.78, 5.75, 6.05, 1.1, [P("Least certain number", size=10.5, bold=True, color=BLUE),
                               P("The vendor-funding value depends on how markdowns are recorded, and the pack does not say. We read the 14-pt gap as net of funding. Each point of funding is ~$0.9M; full recovery to 55% would be ~$8M.", size=10)],
       fill=PANEL, margin=0.1)
footer("Sales bases: $1,412M = FY2025 sales after store exits and the e-commerce fee effect; $1,398M also deducts the 1% promotion volume loss. Source: briefing pack Table 2, §5; team analysis.")

# =========================================================== 10 E-commerce fix
header("2 · The plan", "Rolling out the tested delivery pricing saves ~$2.5M a year and keeps home delivery. The service still loses money, so growth stays frozen.")
rows = [["Fee test applied to FY2025 volumes", "Today", "Tested pricing", "Change"],
        ["Delivery fee / free-delivery threshold", "$4.99 / $75", "$7.99 / $100", ""],
        ["Home-delivered orders (k)", "772", "703", "−9%"],
        ["Click-and-collect orders (k)", "559", "637", "+14%"],
        ["E-commerce sales ($M)", "127.8", "125.2", "−2%"],
        ["Picking cost ($M)", "9.9", "9.9", "0.0"],
        ["Third-party delivery cost ($M)", "10.7", "9.7", "−1.0"],
        ["Less: delivery fees ($M; $3.10 → $6.40 per order)", "−2.4", "−4.5", "−2.1"],
        ["Net fulfillment cost ($M)", "18.1", "15.1", "−3.0"],
        ["Contribution lost on 2% lower sales ($M)", "", "", "+0.2 to +0.5"],
        ["Net gain ($M a year; plan uses $2.5M)", "", "", "+2.5 to +2.8"]]
table(0.5, 1.75, [3.85, 1.05, 1.15, 1.15], rows, rowh=0.36, size=10, hl={8: PANEL, 10: BLUE_L}, bold_last=True)
D.text(7.95, 1.75, 4.88, 4.0, [
    P("Also act on", size=10.5, bold=True, color=BLUE),
    B("Delivery contract (renews in 2026). The provider wants +3%, which costs $0.3M. Re-tender instead: each 5% off the rate is worth ~$0.5M.", size=10),
    B("Keep growth frozen until both order types make money. Click-and-collect breaks even at 38.5% new-to-Harlow sales (we have 30%), or at a picking cost of $5.76.", size=10),
    P("Options considered", size=10.5, bold=True, color=BLUE, space_before=8),
    B("Grow e-commerce as it is: rejected. Every extra delivered order loses ~$12.", size=10),
    B("Exit home delivery: it still loses ~$9 per order after repricing (~$6M a year), but this breaks the owners' commitment. Kept only as a fallback to discuss with the owners.", size=10),
    B("Further pricing steps (subscription, minimum basket): to be tested; not in the base case.", size=10),
    P("Caveat: the test ran in 4 stores for 10 weeks. Roll out in waves and stop if e-commerce sales fall more than 5%.", size=9.5, color=INK2, space_before=8)],
    fill=PANEL, margin=0.1)
footer("Source: briefing pack Table 5 and §7 fee test; team analysis. Lost contribution: 2% × $127.8M at 30% incrementality (low) or 100% (high), × 20¢.")

# =========================================================== 11 Labor
header("2 · The plan", "A targeted labor rebalance nets ~$3.6M with little risk. The 8% blanket cut could give back most of its $14.5M through shrink and lost sales.")
rows = [["$M a year", "Management draft: cut 8% of hours in every store", "Recommended: targeted rebalance"],
        ["Gross saving", "+14.5 (8% × $181.9M)", "+5.5 (~5% of hours in the most labor-intensive half of stores ≈ 3% of chain hours)"],
        ["Reinvestment", "–", "−1.8 (1% of chain hours put back into produce rotation and receiving in the lowest-labor stores)"],
        ["Shrink effect", "Up to −10.0 if shrink responds as in FY2023–25 (−6% hours ↔ +0.5 pt) → +0.67 pt", "Neutral to positive: Q3 and Q4 stores differ by 0.1 pt of shrink"],
        ["Sales at risk", "Each 1% of sales lost = −3.0 (checkout waits, out-of-stocks)", "Low: fresh and receiving hours are protected"],
        ["Net", "+1.5 to +14.5, central ~+4.5 before any sales loss", "+3.6"]]
table(0.5, 1.75, [1.6, 5.0, 5.73], rows, rowhs=[0.4, 0.55, 0.55, 0.62, 0.55, 0.45], size=10.5, bold_last=True,
      aligns=["l", "l", "l"], hl={5: PANEL})
D.text(0.5, 5.05, 4.0, 1.3, [P("Why it matters to customers", size=10.5, bold=True, color=BLUE),
                             P("The top reasons to shop at Harlow are fresh produce (58%) and convenience (44%). Both depend on store labor. Cutting them while ValuMart competes on price leaves Harlow with neither advantage.", size=10)],
       fill=PANEL, margin=0.1)
D.text(4.67, 5.05, 4.0, 1.3, [P("How the rebalance works", size=10.5, bold=True, color=BLUE),
                              P("Trim hours in Q3–Q4 stores toward the Q3 level and protect task standards for receiving checks and produce rotation. Track shrink, waits and out-of-stocks weekly, and reverse in any store where shrink rises more than 0.2 pt.", size=10)],
       fill=PANEL, margin=0.1)
D.text(8.83, 5.05, 4.0, 1.3, [P("Wage outlook", size=10.5, bold=True, color=BLUE),
                              P("The 2027 minimum-wage rise (+4%) adds ~$7.3M. The plan assumes half is recovered in prices (−$3.6M net). If none is recovered, the contingency is a further 1% targeted hours trim (+$1.8M).", size=10)],
       fill=PANEL, margin=0.1)
footer("Source: briefing pack §4, Tables 1, 3, 4, §9 survey; team analysis. The shrink response is an analogy from FY2023–25 and is illustrative; the per-quartile hours split is not in the pack.")

# =========================================================== 12 Stores
header("2 · The plan", "Exiting the nine stores with negative four-wall EBITDA adds ~$6.6M a year. Six can close when their leases expire, with no lease-exit cost.")
rows = [["Pro-rata by store count", "6 stores: leases end by 2027", "3 stores: leases run beyond 2027", "All 9"],
        ["Sales ($M)", "78.7", "39.3", "118.0"],
        ["Four-wall EBITDA removed ($M)", "+2.1", "+1.0", "+3.1"],
        ["Sales moving to nearby Harlow stores (25%)", "19.7", "9.8", "29.5"],
        ["Contribution on moved sales (12%)", "+2.4", "+1.2", "+3.5"],
        ["Annual operating-income gain ($M)", "+4.4", "+2.2", "+6.6"],
        ["One-time cost ($M): lease exit + closure", "0 + 2.4", "7.5 + 1.2", "11.1"],
        ["Payback", "~0.5 years", "~3.9 years", "~1.7 years"],
        ["Governance", "Management decision", "Board vote required", ""]]
table(0.5, 1.75, [3.9, 2.35, 2.55, 1.2], rows, rowh=0.4, size=10.5, hl={5: PANEL})
D.text(10.75, 1.75, 2.08, 1.85, [P("Recommendation", size=10.5, bold=True, color=BLUE),
                                P("Do not renew the six expiring leases. Run a store-by-store review of the other three and bring them to a board vote in Q2 FY2027.", size=10)],
       fill=BLUE_L, margin=0.1)
D.text(0.5, 5.5, 12.33, 1.35, [P("Trade-offs and caveats", size=10.5, bold=True, color=BLUE),
                               B("The base case includes all nine exits. Without the three that need a board vote, FY2028 margin is ~2.7% (operating income $38.5M on $1,427M of sales), and $8.7M of one-time cost is avoided.", size=10),
                               B("The pack gives totals only. The real split between the six and the three may differ, so the store review must confirm each case. Overhead allocations are not in four-wall EBITDA, so no stranded overhead is double-counted.", size=10)],
       margin=0.02)
footer("Source: briefing pack Table 6 and §3 commitments; team analysis. Non-lease closure costs (severance, fixtures, inventory) are not in the pack; $0.4M per store is a planning assumption.")

# =========================================================== 13 Alternatives
header("2 · The plan", "Of the options assessed, only the recommended plan gets close to 3.0% within the capital cap and the owners' commitments.")
rows = [["Option", "FY2028 operating income", "Operating margin", "One-time cost", "Fit with constraints", "Main risk"],
        ["A. Management draft: 8% hours cut, freeze e-commerce", "$13–26M", "0.9–1.7%", "~$0M", "Fits, but misses the 3.0% target", "Shrink and service; treats a minor cause"],
        [P("B. Recommended: all eight actions", size=10.5, bold=True), P("$40.7M (stretch $43.5M)", size=10.5, bold=True, align="c"), P("2.9% (3.1%)", size=10.5, bold=True, align="c"), P("~$20M", size=10.5, bold=True, align="c"), P("Within $25M; board vote on 3 stores", size=10.5, bold=True, align="c"), P("Traffic response to fewer promotions; vendor funding", size=10.5, bold=True, align="c")],
        ["C. B without the three board-vote store exits", "$38.5M", "2.7%", "~$11M", "No board vote needed", "Misses 3.0% unless stretch levers deliver"],
        ["D. B plus exit home delivery", "~$45–47M", "~3.3%", "~$20M", "Breaks the owners' delivery commitment", "Customer backlash; loses convenience"],
        ["E. Grow e-commerce as is", "Lower than B", "< 2.9%", "–", "Fits", "Each delivered order loses ~$12"]]
table(0.5, 1.75, [3.0, 1.85, 1.45, 1.3, 2.35, 2.38], rows, rowhs=[0.5, 0.72, 0.72, 0.62, 0.62, 0.55], size=10.5, hl={2: BLUE_L})
D.text(0.5, 5.65, 12.33, 1.2, [P("How the figures are built", size=10.5, bold=True, color=BLUE),
                               B("A: $15.3M + $14.5M − $3.6M wage step = $26.2M at best. With the FY2023–25 shrink response (−$10M) and 1% lost sales (−$3M), it is $13.2M.", size=10),
                               B("D: adds the ~$6.4M that repriced home delivery still loses (703k orders × $9.04), less some contribution from customers who switch to other channels or leave.", size=10)],
       margin=0.02)
footer("Source: team analysis on briefing pack data. All options include the 2027 wage step at half recovery (−$3.6M).")

# =========================================================== 14 Prioritisation
header("3 · What to do first", "Start with four moves that are proven, cheap and quick. Slower, larger levers follow once they are under way.")
rows = [["Action", "$M / yr FY2028", "One-time $M", "Time to impact", "Evidence strength", "Wave"],
        ["1. Roll out tested delivery pricing; re-tender delivery contract", "+2.5", "0.5", "1–3 months", "High: in-market test", P("1 · now", size=10, bold=True, color=BLUE, align="c")],
        ["2. Drop loss-making promotion events (share 29%→25%)", "+5.1", "1.0", "3–6 months", "High: post-event review", P("1 · now", size=10, bold=True, color=BLUE, align="c")],
        ["3. Rebalance labor hours, with fresh and receiving standards", "+3.6", "1.5", "3–6 months", "Medium: shrink-by-quartile data", P("1 · now", size=10, bold=True, color=BLUE, align="c")],
        ["4. Give notice on the six expiring leases", "+4.4", "2.4", "At lease end (by end-2027)", "High: four-wall P&L", P("1 · decide now", size=10, bold=True, color=BLUE, align="c")],
        ["5. Recover vendor funding (46%→50%)", "+3.6", "incl. in 2", "6–12 months (annual terms)", "Low–medium: sizing indicative", "2 · FY2027"],
        ["6. Shrink program to 2.3% (stretch 2.1%)", "+4.2", "4.0", "6–18 months", "Medium: Q3–Q4 stores already there", "2 · FY2027"],
        ["7. Extend the private-label range (18.5%→20.5%)", "+3.4", "2.0", "12–24 months", "Medium: existing trend", "2 · FY2027–28"],
        ["8. Exit three stores with leases beyond 2027", "+2.2", "8.7", "FY2028", "Medium: totals only", "3 · after board vote"]]
table(0.5, 1.75, [4.25, 1.25, 1.05, 2.1, 2.45, 1.23], rows, rowh=0.42, size=10, hl={1: PANEL, 2: PANEL, 3: PANEL, 4: PANEL})
D.text(0.5, 5.65, 12.33, 0.9, [P("Ranking logic", size=10.5, bold=True, color=BLUE),
                               P("Wave 1 holds the actions with the highest value per dollar and per month of delay, backed by Harlow's own test or review data, and they are reversible. Action 4 brings no savings until the leases end, but the decision cannot wait: missing a notice date locks in a loss-making store. Wave 1 also protects the lender case, because it delivers the run-rate on the next page.", size=10)],
       fill=PANEL, margin=0.1)
footer("Source: team analysis. Action 1 includes the contract re-tender; 'incl. in 2' means the vendor-funding work shares the promotion-analytics budget.")

# =========================================================== 15 Roadmap
header("3 · What to do first", "Wave 1 lifts run-rate operating income to ~$26M within six months, clear of the $20M covenant. Two stage gates keep the plan honest.")
qx0, qw = 3.6, 1.15
quarters = ["Q1 FY27", "Q2", "Q3", "Q4", "Q1 FY28", "Q2", "Q3", "Q4"]
D.text(0.5, 1.68, 3.0, 0.3, P("Feb 2027 – Jan 2029", size=9.5, color=INK2), margin=0)
for i, q in enumerate(quarters):
    D.text(qx0 + i * qw, 1.68, qw, 0.3, P(q, size=9.5, bold=True, color=INK2, align="c"), margin=0)
D.line(0.5, 2.0, qx0 + 8 * qw, 2.0, color=INK, lw=0.75)
bars = [("Delivery pricing rollout and contract re-tender", 0, 1.5, BLUE),
        ("Promotion calendar reset", 0, 2, BLUE),
        ("Labor rebalance and task standards", 0, 2, BLUE),
        ("Lease notices → six exits by end-2027", 0, 4, BLUE),
        ("Vendor-funding renegotiation", 1, 4, BLUE_L),
        ("Shrink program (tools, loss prevention)", 1, 6, BLUE_L),
        ("Private-label range extension", 1, 8, BLUE_L),
        ("Three-store review → vote → exits", 0.5, 5, GRAY)]
for i, (lbl, a, b, col) in enumerate(bars):
    yy = 2.1 + i * 0.4
    D.text(0.5, yy, 3.05, 0.34, P(lbl, size=9.5), valign="m", margin=0)
    D.rect(qx0 + a * qw + 0.03, yy + 0.07, (b - a) * qw - 0.06, 0.22, fill=col)
for gx, lbl in [(2, "Gate 1"), (4, "Gate 2")]:
    D.line(qx0 + gx * qw, 2.0, qx0 + gx * qw, 5.35, color=INK, lw=1)
    D.text(qx0 + gx * qw - 0.6, 5.33, 1.2, 0.25, P(lbl, size=9, bold=True, align="c"), margin=0)
D.text(0.5, 5.33, 3.0, 0.25, P("Wave 1 dark · Wave 2 light · Wave 3 gray", size=8.5, color=MUTED), margin=0)
tiles = [("$15.3M", "FY2025 actual", "1.0% margin"),
         ("~$26M", "Run-rate after Wave 1 (≈6 months)", "Delivery 2.5 + promotions 3.0 + labor 3.6 + shrink basics 1.4"),
         ("~$28M", "FY2027 (net of wage step)", "≈1.9%; partial-year effects"),
         ("$40.7M", "FY2028 base", "2.9%; stretch 3.1%")]
for i, (v, l1, l2) in enumerate(tiles):
    xx = 0.5 + i * 3.1
    D.text(xx, 5.72, 2.95, 1.15, [P(v, size=20, bold=True, color=BLUE_D), P(l1, size=10, bold=True), P(l2, size=9, color=INK2)],
           fill=PANEL, margin=0.08)
footer("Gate 1 (end Q2 FY27): run-rate ≥ $25M, shrink not rising in rebalanced stores. Gate 2 (end Q4 FY27): FY27 ≈ $28M; vendor terms signed; if more than $3M behind, release contingency (page 18). FY2027 phasing assumes 80% of promotions, 50% of vendor funding and shrink, 40% of private label.")

# =========================================================== 16 Capital
header("3 · What to do first", "The plan needs ~$20M of one-time spend, leaving ~$5M of headroom under the $25M cap. Over 40% of it is the optional three-store exit.")
items = [("Lease exits, three stores (board vote)", 7.5, "Pack"), ("Shrink program: tools, receiving controls, loss prevention", 4.0, "Assumption"),
         ("Store closure costs, nine stores × $0.4M", 3.6, "Assumption"), ("Private-label range development", 2.0, "Assumption"),
         ("Labor scheduling and task-standard training", 1.5, "Assumption"), ("Promotion analytics and vendor negotiation", 1.0, "Assumption"),
         ("Delivery repricing: systems and customer communication", 0.5, "Assumption")]
D.text(0.5, 1.65, 8, 0.3, P("One-time cost or capital, FY2026–FY2028, $M", size=10, bold=True, color=INK2), margin=0)
lx, bx0, sc = 0.5, 5.0, 0.42
for i, (lbl, v, src) in enumerate(items):
    yy = 2.0 + i * 0.5
    D.text(lx, yy, 4.4, 0.4, P(lbl, size=10), valign="m", margin=0)
    D.rect(bx0, yy + 0.08, v * sc, 0.26, fill=BLUE if src == "Pack" else GRAY)
    D.text(bx0 + v * sc + 0.08, yy, 1.6, 0.4, [P([(f"{v:.1f}", True, INK), (f"  {src.lower()}", False, MUTED)], size=10)], valign="m", margin=0)
yy = 2.0 + 7 * 0.5 + 0.1
D.line(0.5, yy, 8.9, yy, color=INK, lw=0.75)
D.text(0.5, yy + 0.05, 4.4, 0.4, P("Total", size=11, bold=True), valign="m", margin=0)
D.text(bx0, yy + 0.05, 3, 0.4, P("$20.1M of $25.0M cap → $4.9M headroom", size=11, bold=True), valign="m", margin=0)
D.text(9.3, 1.75, 3.53, 3.6, [P("Notes", size=10.5, bold=True, color=BLUE),
                              B("Only the $7.5M lease-exit cost comes from the pack. The other lines are planning allowances to be confirmed in business cases before Gate 1.", size=10),
                              B("Without the three-store exit, spend falls to ~$11.4M and FY2028 margin to ~2.7%.", size=10),
                              B("Wave 1 needs only ~$5.4M (delivery 0.5, promotions 1.0, labor 1.5, six-store closure 2.4). The large spend comes after the gates.", size=10),
                              B("Payback: about 0.7 years for the plan overall; 3.9 years for the three-store exit.", size=10)],
       fill=PANEL, margin=0.1)
footer("Source: briefing pack §3 and Table 6; team planning assumptions. Payback = one-time cost ÷ annual operating-income gain ($20.1M ÷ $29.0M ≈ 0.7 years).")

# =========================================================== 17 Scenarios
header("4 · Risks and decisions", "FY2028 margin ranges from 2.0% to 3.8%. Even in the low case operating income is ~$27M, well above the $20M level the lender requires.")
rows = [["$M a year, FY2028", "Low", "Base", "High", "What moves the range"],
        ["Promotions", "3.5", "5.1", "8.0", "Traffic loss when events are cut"],
        ["Vendor funding", "0.0", "3.6", "5.0", "Vendors refuse vs recover toward 55%"],
        ["Private label", "2.5", "3.4", "4.2", "Share gain of 1.5–2.5 pt"],
        ["Shrink", "2.8", "4.2", "5.6", "Shrink reaches 2.4% / 2.3% / 2.2%"],
        ["Labor rebalance", "1.8", "3.6", "4.5", "Size of the safe trim in Q3–Q4 stores"],
        ["Delivery pricing", "2.2", "2.5", "3.3", "Churn after rollout; contract re-tender outcome"],
        ["Store exits (nine)", "6.6", "6.6", "6.6", "Board vote; sales transfer of 25%"],
        ["2027 wage step", "−7.3", "−3.6", "0.0", "None, half or all recovered in prices"],
        ["FY2028 operating income", "27.4", "40.7", "52.5", ""],
        ["FY2028 operating margin", "2.0%", "2.9%", "3.8%", "on ~$1,398M of sales"]]
table(0.5, 1.75, [2.6, 0.85, 0.85, 0.85, 3.6], rows, rowh=0.38, size=10.5, hl={9: PANEL, 10: PANEL}, aligns=["l", "c", "c", "c", "l"])
D.text(9.55, 1.75, 3.28, 4.25, [P("Sensitivities ($M a year)", size=10.5, bold=True, color=BLUE),
                               B("1 pt of promotion share: ±2.0", size=10),
                               B("1 pt of vendor funding: ±0.9", size=10),
                               B("0.1 pt of shrink: ±1.4", size=10),
                               B("1% of store hours: ±1.8", size=10),
                               B("1% of sales lost at 20¢: −2.8", size=10),
                               B("5% on the delivery rate: ±0.5", size=10),
                               P("Not modelled (upside)", size=10.5, bold=True, color=BLUE, space_before=8),
                               B("Real like-for-like growth: each 1% adds ~$2.8M at 20¢ contribution.", size=10),
                               B("Fixed-cost leverage on occupancy and other SG&A.", size=10)],
       fill=PANEL, margin=0.1)
footer("Source: team analysis. Store exits are held constant because four-wall losses are known; the 25% transfer is the main uncertainty ($3.5M of the $6.6M).")

# =========================================================== 18 Risks
header("4 · Risks and decisions", "Each major risk has an early signal and a pre-agreed response. If the plan falls behind, the contingency levers are worth ~$5M.")
rows = [["Risk", "Early signal (tracked monthly)", "Response"],
        ["ValuMart takes traffic as promotions are cut", "Comps and basket count in stores within 3 miles of ValuMart vs the rest", "Cut loss-making events first; up to $2M for everyday prices on key items in those stores"],
        ["Vendors do not restore funding", "Funding as % of markdowns, by supplier", "Tie promotion slots to funding; move events to suppliers that fund"],
        ["Delivery customers leave faster than in the test", "Weekly delivered orders; e-commerce sales vs −2%", "Roll out in waves; pause if e-commerce sales fall more than 5%"],
        ["Labor rebalance hurts shrink or service", "Shrink by quartile, checkout waits, out-of-stocks", "Protect fresh and receiving hours; reverse in any store where shrink rises more than 0.2 pt"],
        ["Closed stores transfer less than 25% of sales", "Sales in the receiving stores", "Retain customers (loyalty offers, click-and-collect from the receiving store)"],
        ["Wage step not recovered in prices", "Store labor % of sales", "Contingency tranche (below)"]]
table(0.5, 1.75, [3.3, 4.1, 4.93], rows, rowh=0.5, size=10, aligns=["l", "l", "l"])
D.text(0.5, 5.4, 12.33, 1.0, [P("Contingency, released at Gate 2 if the plan is more than $3M behind", size=10.5, bold=True, color=BLUE),
                               P("Shrink stretch to 2.1% (+$2.8M) · a further 1% targeted hours trim in Q4 stores (+$1.8M) · delivery contract re-tender beyond flat (+$0.5M per 5%) · the next delivery-pricing test. Together ~$5M: enough to cover either vendor funding failing entirely (−$3.6M) or the wage step going wholly unrecovered (−$3.6M), but not both.", size=10.5)],
       fill=PANEL, margin=0.1)
footer("Source: briefing pack §11 uncertainties; team analysis.")

# =========================================================== 19 Decisions
header("4 · Risks and decisions", "We ask the board for six decisions today, so that Wave 1 can start this quarter.")
dec = [("Approve the margin plan", "Target ≥ 3.0% in FY2028: base 2.9%, stretch 3.1%. Gates at the end of Q2 and Q4 FY2027."),
       ("Withdraw the 8% blanket labor cut", "Replace it with the targeted rebalance (net +$3.6M) and fresh and receiving task standards."),
       ("Approve up to $20.1M of one-time spend", "Within the $25M cap; released by gate. Wave 1 needs ~$5.4M."),
       ("Authorize non-renewal of the six expiring leases", "Decide now so that notice dates are met; exits by end-2027 (+$4.4M a year)."),
       ("Vote on the three-store exit in Q2 FY2027", "After a store-by-store review; $8.7M one-time cost, +$2.2M a year."),
       ("Confirm the delivery commitment with the owners and brief the lender", "'Delivery in some form' means repriced home delivery plus free click-and-collect. Show the lender the ~$26M Wave 1 run-rate.")]
for i, (h, t) in enumerate(dec):
    col, row = i % 2, i // 2
    xx, yy = 0.5 + col * 6.25, 1.8 + row * 1.6
    numbered(xx, yy + 0.05, i + 1)
    D.text(xx + 0.5, yy, 5.55, 1.45, [P(h, size=14, bold=True), P(t, size=12, color=INK2, space_before=4)], margin=0.03)
footer()

# =========================================================== 20 Appendix assumptions
header("Appendix", "Assumptions and choices made where the pack was silent")
rows = [["Topic", "Choice made", "Effect if wrong"],
        ["Timing", "FY2025 = Feb 2025–Jan 2026, so FY2026 closes as the board meets. The pack has no FY2026 results, so FY2025 is used as the run-rate. If FY2026 misses the $20M covenant, use this plan to open the waiver discussion.", "Covenant test may already be fixed; first moves are unchanged"],
        ["Prices and growth", "Constant FY2025 prices; no real like-for-like growth", "Growth would add ~$2.8M per 1%"],
        ["2027 wage step", "+4% on $181.9M = $7.3M; half recovered in prices", "±$3.6M (low and high cases)"],
        ["Vendor funding", "The 14-pt promotion gap is net of funding; markdowns ≈ 25.9% of promoted sales", "Value could be lower; held at $0 in the low case"],
        ["Promotion volume", "Cutting 4 pt of promotion share loses 1% of total sales at 20¢", "Each further 1% lost = −$2.8M"],
        ["Nine weak stores", "Totals split pro rata by store count; closure cost $0.4M per store", "The store review confirms each case"],
        ["One-time costs", "All except the $7.5M lease exits are planning allowances", "Headroom under the cap is $4.9M"],
        ["E-commerce", "30% incrementality (survey of stated intent); 20¢ contribution (finance); fee-test response holds chain-wide", "Higher incrementality makes e-commerce less negative"],
        ["Labor and shrink", "FY2023–25 hours-to-shrink link is used as an illustration only", "Blanket-cut downside could be smaller or larger"]]
table(0.5, 1.7, [1.9, 6.6, 3.83], rows, rowhs=[0.34, 0.75, 0.38, 0.38, 0.5, 0.38, 0.38, 0.38, 0.5, 0.38], size=9.5, aligns=["l", "l", "l"])
footer("Prepared without the chance to ask clarifying questions: each choice above is the recommended option and is flagged for management to confirm.")

# =========================================================== 21 Appendix calc log
header("Appendix", "Calculation log for the key figures")
L1 = [P("Diagnosis", size=10.5, bold=True, color=BLUE),
      B("Ratio changes FY23→FY25: GM 26.04%→25.02%; labor 11.80%→12.10%; occupancy 5.80%→6.00%; e-com 0.37%→1.20%; SG&A 4.70%→4.70%", size=9),
      B("GM drivers: promo (29.0 − 24.0) × −14 pt = −0.70; PL (18.5 − 17.0) × +12 pt = +0.18; shrink −0.50", size=9),
      B("E-com FY25: delivered orders 1,331k × 58% = 772k; picking 1,331k × $7.40 = $9.85M; delivery 772k × $13.80 = $10.65M; fees 772k × $3.10 = $2.39M; net $18.11M (Table 1: $18.1M)", size=9),
      B("Incremental contribution: $127.8M × 30% × 20¢ = $7.67M; true contribution −$10.44M. Team claim 6.1% × $127.8M = $7.8M", size=9),
      P("E-commerce pricing", size=10.5, bold=True, color=BLUE, space_before=6),
      B("Delivered 772k × 0.91 = 703k; C&C 559k × 1.14 = 637k; picking 1,340k × $7.40 = $9.91M; delivery 703k × $13.80 = $9.69M; fees 703k × $6.40 = $4.50M; net $15.11M → −$3.00M", size=9),
      B("Lost sales 2% × $127.8M = $2.56M × 20¢ × (30% to 100%) = $0.15–0.51M → net $2.5–2.8M", size=9),
      P("Labor", size=10.5, bold=True, color=BLUE, space_before=6),
      B("8% × $181.9M = $14.55M; shrink analog 0.5 pt ÷ 6% × 8% = 0.67 pt × $1,503M = $10.0M", size=9),
      B("Rebalance: 3% × $181.9M = $5.46M less 1% = $1.82M → $3.64M. Wage step 4% × $181.9M = $7.28M × 50% = $3.64M", size=9)]
L2 = [P("Gross-margin levers", size=10.5, bold=True, color=BLUE),
      B("Sales after exits and e-com: $1,503M − $88.5M − $2.6M = $1,411.9M; after 1% promo volume loss: $1,397.8M", size=9),
      B("Promotions: 4% × 14% × $1,411.9M = $7.91M − $14.1M × 20% = $2.82M → $5.08M", size=9),
      B("Vendor funding: 14% ÷ 54% = 25.9%; 25% × $1,397.8M × 25.9% = $90.6M × 4% = $3.62M", size=9),
      B("Private label: 2% × 12% × $1,397.8M = $3.35M. Shrink: 0.3% × $1,397.8M = $4.19M; stretch +0.2% = $2.80M", size=9),
      P("Stores (pro rata)", size=10.5, bold=True, color=BLUE, space_before=6),
      B("6 stores: sales $78.7M; EBITDA −$2.07M; transfer 25% × $78.7M × 12% = $2.36M → $4.43M", size=9),
      B("3 stores: $39.3M; −$1.03M; $1.18M → $2.21M; one-time $7.5M + $1.2M = $8.7M → payback 3.9 years", size=9),
      P("Totals", size=10.5, bold=True, color=BLUE, space_before=6),
      B("Levers 5.08 + 3.62 + 3.35 + 4.19 + 3.64 + 2.51 + 4.43 + 2.21 = $29.0M; FY2028 = 15.3 + 29.0 − 3.6 = $40.7M ÷ $1,397.8M = 2.91%", size=9),
      B("Hypothesis 5 test (no labor or store actions): sales $1,485M; operating income $31.4M = 2.1%", size=9),
      B("Wave 1 run-rate: 15.3 + 2.5 + 60% × 5.1 + 3.6 + ⅓ × 4.2 = $25.9M", size=9)]
D.text(0.5, 1.68, 6.05, 5.2, L1, margin=0.02)
D.text(6.78, 1.68, 6.05, 5.2, L2, margin=0.02)
footer()

assert D.n == TOTAL_SLIDES, D.n
D.save(OUT, PREV)
print("\n".join(D.warnings) or "no warnings")
