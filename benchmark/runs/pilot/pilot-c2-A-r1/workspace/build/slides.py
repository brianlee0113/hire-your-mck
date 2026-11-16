import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
from charts import *

D = Deck()
SRC = "Source: Harlow Fresh Markets briefing pack (FY2023–FY2025). Fiscal years end in January. "

# ------------------------------------------------------------------ 1. Title
s = D.new()
s.rect(0, 0, SW, SH, fill="FFFFFF")
s.rect(0, 0, 0.28, SH, fill=BLUE)
s.text(1.0, 1.0, 8, 0.3, "HARLOW FRESH MARKETS  |  BOARD OF DIRECTORS, FEBRUARY 2027", size=12, color=BLUE, bold=True)
s.text(1.0, 1.9, 11, 1.8, "Getting Harlow’s operating margin back to 3%", size=40, bold=True, spacing=0.95)
s.text(1.0, 3.55, 11, 1.0, "Where the margin went, what to do about it, and which actions to take first",
       size=20, color=SEC)
s.line(1.0, 4.75, 6.0, 4.75, color=RULE)
s.text(1.0, 4.95, 9, 0.9, ["Margin plan for discussion and decision",
                          "Presented by Dana Whitfield, Chief Executive Officer"], size=14, color=INK, after=4)
s.text(1.0, 6.6, 11.5, 0.5,
       "Based solely on the company briefing pack (FY2023–FY2025 actuals, tests and surveys). The pack’s data are "
       "fictional, produced for a reasoning benchmark.",
       size=9.5, color=MUTED)

# ------------------------------------------------------------------ 2. Executive summary
s = D.new()
s.header("Executive summary",
         "Harlow can return to a 3.0% margin by FY2028 by reversing what caused the decline, not by cutting store hours")
rows = [
    ("The problem", "Operating margin fell from 3.4% to 1.0% in two years. Operating income fell from $47.9M to "
                    "$15.3M while sales grew 6%."),
    ("The cause", "Heavier promotions (−0.70 pts), e-commerce fulfillment (−0.84) and higher shrink (−0.50) explain "
                  "2.0 of the 2.4-point fall. Store labor explains 0.3: wages rose 9.4%, but hours per $ of sales fell 6%."),
    ("The draft plan falls short", "Cutting store hours 8% saves $14.5M on paper, but the stores with the fewest "
                                   "hours already have the most shrink. The draft plan reaches 1.1–1.8% in FY2028, "
                                   "not 3.0%."),
    ("Recommendation", "Five moves worth ~$30M a year by FY2028: reset promotions, rebalance labor to cut shrink, price "
                       "delivery closer to cost, exit the 9 loss-making stores, grow private label. After the 2027 "
                       "wage rise, operating income reaches ~$42M, a 3.0% margin."),
    ("Act first", "In the next 90 days: roll out the tested delivery fee, drop loss-making promotions, replace the hours "
                  "cut with a rebalance, hold the delivery contract rate, give notice on 6 expiring leases. FY2026 "
                  "operating income: ~$24M against the $20M covenant."),
    ("The risk", "3.0% needs every move to deliver. The moves within management’s control reach ~2.3%. The rest depends "
                 "on vendor talks, a second delivery-price test and a board vote on 3 stores."),
]
yy = 1.78
for lab, body in rows:
    s.text(0.6, yy, 2.15, 0.78, lab, size=12.5, bold=True, color=BLUE, name="es lab")
    s.text(2.8, yy, 6.55, 0.78, body, size=12.5, name="es body " + lab)
    yy += 0.83
    if lab != "The risk":
        s.line(0.6, yy - 0.06, 9.35, yy - 0.06, color=GRID, lw=0.5)
# hero panel
s.rect(9.75, 1.78, 2.98, 4.95, fill=PANEL)
tiles = [("1.0% → 3.0%", "Operating margin, FY2025 actual → FY2028 plan"),
         ("~$24M", "FY2026 operating income outlook vs $20M covenant"),
         ("$7.5M", "One-time cost identified, of the $25M allowed")]
ty = 1.98
for big, small in tiles:
    s.text(9.95, ty, 2.6, 0.55, big, size=26, bold=True, color=DBLUE, name="hero")
    s.text(9.95, ty + 0.6, 2.6, 0.7, small, size=11.5, color=SEC, name="hero sub")
    ty += 1.6
s.footer(SRC + "Plan values are annual run-rates in constant FY2025 terms; see appendix for sizing.")

# ------------------------------------------------------------------ 3. Diagnosis
s = D.new()
s.header("Where the margin went",
         "Promotions, delivery costs and shrink explain 2.0 of the 2.4-point margin decline; wages explain 0.3")
items = [("FY2023 margin", 3.37, "total"), ("Promotional mix", -0.70, "delta"), ("Shrink", -0.50, "delta"),
         ("Private-label mix", 0.18, "delta"), ("E-commerce fulfillment", -0.84, "delta"),
         ("Store labor", -0.30, "delta"), ("Occupancy & energy", -0.20, "delta"), ("FY2025 margin", 1.02, "total")]
fmt = lambda v, k: (f"{v:.2f}%" if k == "total" else f"{v:+.2f}").replace("-", "−")
s.text(0.6, 1.78, 8.2, 0.3, "Operating margin, % of sales, FY2023 → FY2025, by driver", size=12, bold=True)
base, k = waterfall(s, 0.6, 2.4, 8.3, 4.25, items, 3.6, fmt, label_size=10.5, label_h=0.62)
# bracket for gross margin
gx0 = 0.6 + 1 * 8.3 / 8 + 0.1; gx1 = 0.6 + 4 * 8.3 / 8 - 0.1
s.line(gx0, 2.38, gx1, 2.38, color=SEC, lw=0.75)
s.line(gx0, 2.38, gx0, 2.48, color=SEC, lw=0.75); s.line(gx1, 2.38, gx1, 2.48, color=SEC, lw=0.75)
s.text(gx0, 2.14, gx1 - gx0, 0.22, "Gross margin: −1.02 pts", size=10.5, bold=True, color=SEC, align="c")
# right panel
s.rect(9.25, 1.78, 3.48, 4.95, fill=PANEL)
s.text(9.45, 1.92, 3.1, 0.3, "What the numbers show", size=12.5, bold=True, color=INK)
s.text(9.45, 2.32, 3.1, 4.3, [
    {"runs": [("Gross margin fell 1.02 pts, ", True), ("fully explained by mix: promotional share +5.0 pts × a "
              "14-pt margin gap; shrink +0.5 pts; private label +1.5 pts × a 12-pt gain.", False)], "bullet": True},
    {"runs": [("E-commerce fulfillment ", True), ("rose from $5.2M to $18.1M as orders tripled and home delivery rose "
              "from 45% to 58% of orders.", False)], "bullet": True, "before": 6},
    {"runs": [("Store labor ", True), ("rose only 0.3 pts of sales: the hourly wage rose 9.4%, but hours per $1,000 "
              "of sales fell 6.0%.", False)], "bullet": True, "before": 6},
    {"runs": [("At FY2025 sales, ", True), ("the shortfall vs FY2023 margins is $35M: gross margin $15.3M, "
              "e-commerce $12.6M, labor $4.5M, occupancy $3.0M.", False)], "bullet": True, "before": 6},
], size=11.5)
s.footer(SRC + "Tables 1–3. Each driver = change in its share of sales; mix effects use the pack’s margin gaps. "
         "Other SG&A unchanged at 4.7% of sales. Figures may not sum due to rounding.")

# ------------------------------------------------------------------ 4. Labor
s = D.new()
s.header("Store labor",
         "Hours are already 6% leaner and the leanest stores lose the most to shrink, so a further 8% cut would "
         "give back much of its saving")
s.text(0.6, 1.78, 4.6, 0.5, "Shrink, % of sales, FY2025, stores by labor-hour quartile", size=12, bold=True)
columns(s, 0.6, 2.25, 4.6, 3.7, [["Q1", "fewest hours"], "Q2", "Q3", ["Q4", "most hours"]], [3.1, 2.7, 2.4, 2.3],
        [RED, TOTAL, TOTAL, TOTAL], 3.4, lambda v: f"{v:.1f}%", label_h=0.6)
s.text(0.6, 6.05, 4.6, 0.8, "Q1 stores lose 0.8 pts more of sales to shrink than Q4. Going from Q3 to Q4 hours "
       "lowers shrink by only 0.1 pts.", size=11, color=SEC)
# middle: draft plan test table
s.text(5.6, 1.78, 3.6, 0.3, "The draft plan, tested ($M a year)", size=12, bold=True)
table(s, 5.6, 2.2, [2.45, 1.05], [
    ["", "FY2028"],
    ["Saving from 8% fewer hours", "+14.5"],
    ["Shrink given back if the FY2023–25 pattern holds*", "up to −9.4"],
    ["2027 minimum-wage step, net", "−3.4"],
    ["FY2028 operating income", "17.0–26.5"],
    ["FY2028 operating margin", "1.1%–1.8%"],
], [0.36, 0.5, 0.7, 0.5, 0.5, 0.5], size=11, col_align=["l", "r"],
      fills={5: LBLUE})
s.text(5.6, 5.4, 3.5, 1.4, "The target needs ~$45M at today’s sales. The draft plan leaves promotions, delivery "
       "and shrink, 2.0 of the 2.4 points lost, untouched.", size=11, color=SEC)
# right: why
s.rect(9.55, 1.78, 3.18, 4.95, fill=PANEL)
s.text(9.75, 1.92, 2.8, 0.3, "Why hours protect margin", size=12.5, bold=True)
s.text(9.75, 2.32, 2.85, 4.3, [
    {"text": "65% of shrink is labor-sensitive: fresh and produce waste 45%, receiving and admin errors 20%.",
     "bullet": True},
    {"text": "Managers in the leanest stores say produce rotation and receiving checks are skipped on busy days.",
     "bullet": True, "before": 6},
    {"text": "Fresh produce is the top reason to shop at Harlow (58%). Checkout waits and stock-outs are also at risk.",
     "bullet": True, "before": 6},
    {"runs": [("Better: ", True), ("trim hours in the most labor-intensive stores and put half back into produce "
              "and receiving in the leanest ones.", False)], "bullet": True, "before": 6},
], size=11.5)
s.footer("*FY2023–25: hours per $1,000 of sales fell 0.42 while shrink rose 0.5 pts. An 8% cut removes a further 0.53 "
         "hours, implying +0.63 pts of shrink (~$9.4M). This is a correlation, not proof of cause. " + SRC + "Tables 3–4.")

# ------------------------------------------------------------------ 5. Promotions
s = D.new()
s.header("Promotions",
         "Promotions grew from 24% to 29% of sales without holding traffic or price perception, and 38% of events "
         "lose money")
s.text(0.6, 1.78, 3.6, 0.5, "Promotional sales, % of total sales", size=12, bold=True)
columns(s, 0.6, 2.2, 3.4, 3.6, ["FY2023", "FY2024", "FY2025"], [24.0, 26.2, 29.0], [TOTAL, TOTAL, BLUE], 32,
        lambda v: f"{v:.1f}%", label_h=0.4)
s.text(0.6, 5.9, 3.4, 0.9, "Each point of sales moved onto promotion costs 0.14 pts of gross margin (~$2.1M).",
       size=11, color=SEC)
stats = [("38%", "of FY2025 promotional events lost money, even counting the extra units they sold"),
         ("55% → 46%", "share of promotional markdowns funded by vendors, FY2023 → FY2025"),
         ("−4.2% vs +1.1%", "FY2025 comparable sales of stores near a new ValuMart vs all other stores"),
         ("33% → 41%", "customers who say Harlow is “more expensive than other options”")]
sy = 1.85
for big, small in stats:
    s.text(4.4, sy, 3.6, 0.45, big, size=21, bold=True, color=DBLUE, name="stat")
    s.text(4.4, sy + 0.47, 3.5, 0.55, small, size=11, color=SEC, name="stat sub")
    sy += 1.22
s.rect(8.4, 1.78, 4.33, 4.95, fill=PANEL)
s.text(8.6, 1.92, 3.95, 0.3, "What we propose (FY2028 run-rate)", size=12.5, bold=True)
s.text(8.6, 2.32, 3.95, 4.3, [
    {"runs": [("Cut the loss-making events, ", True), ("taking promotional share to 25%: +$4.4M. Assumes a third "
              "of the cut volume is lost and two-thirds sells at full price.", False)], "bullet": True},
    {"runs": [("Make vendor funding a condition of a promotional slot, ", True), ("recovering half the slip "
              "(46% → 51%): +$4.5M. To confirm: assumes the 14-pt gap is after vendor funding.", False)],
     "bullet": True, "before": 6},
    {"runs": [("Keep events that pay back in ValuMart trade areas ", True), ("and track their weekly traffic as "
              "the signal to stop or slow the cuts.", False)], "bullet": True, "before": 6},
    {"runs": [("Upside: ", True), ("returning to FY2023’s 24% adds a further ~$1.1M.", False)], "bullet": True,
     "before": 6},
], size=11.5)
s.footer(SRC + "Table 2 and section 9. The 14-pt gap between promotional and regular-price margin was unchanged "
         "over the period. Deeper promotions coincided with weaker ValuMart-area sales; this does not prove cause.")

# ------------------------------------------------------------------ 6. E-commerce
s = D.new()
s.header("E-commerce",
         "Home delivery loses about $12 an order because 70% of online sales would have happened in-store; "
         "click-and-collect nearly breaks even")
s.text(0.6, 1.78, 7.3, 0.3, "Contribution per order after fulfillment, FY2025, $", size=12, bold=True)
fm = lambda v: (f"{v:+.2f}" if not isinstance(v, tuple) else "").replace("-", "−")
endy, zx, kk = hbars(s, 0.6, 2.3, 7.3, [
    ("Click-and-collect", -1.64, TOTAL),
    ("Home delivery, current fees", -12.34, RED),
    ("Home delivery, fee-test terms", -9.04, RED),
], -16, 2, label_w=2.9, bar_h=0.38, gap=0.25, val_fmt=fm, size=11.5)
s.text(0.6, 4.35, 7.3, 0.3, "How an order’s economics build up", size=12, bold=True)
table(s, 0.6, 4.7, [3.9, 1.7, 1.7], [
    ["$ per order", "Click-and-collect", "Home delivery"],
    ["Contribution from new sales ($96 × 30% new × 20%)", "+5.76", "+5.76"],
    ["Picking", "−7.40", "−7.40"],
    ["Third-party delivery, net of fee ($13.80 − $3.10)", "—", "−10.70"],
    ["Net contribution", "−1.64", "−12.34"],
], [0.34, 0.36, 0.34, 0.36, 0.36], size=10.5, col_align=["l", "r", "r"], fills={4: LBLUE})
s.rect(8.3, 1.78, 4.43, 4.95, fill=PANEL)
s.text(8.5, 1.92, 4.05, 0.3, "The fee test points the way", size=12.5, bold=True)
s.text(8.5, 2.3, 4.05, 1.3, "4 stores, 10 weeks: fee $7.99, free delivery from $100 (was $75). Delivered orders −9%, "
       "click-and-collect +14%, e-commerce sales −2%, average fee $3.10 → $6.40.", size=11)
s.text(8.5, 3.3, 4.05, 3.3, [
    {"runs": [("Roll out the test terms chain-wide now: ", True), ("+$2.8M a year.", False)], "bullet": True},
    {"runs": [("Hold the delivery partner’s rate at the 2026 renewal; ", True), ("its proposed +3% would cost "
              "~$0.3M.", False)], "bullet": True, "before": 5},
    {"runs": [("Test a second step in FY2027 ", True), ("(a paid delivery pass or higher fee, averaging ~$9.50): "
              "about +$2.5M if a further 10% of deliveries switch to click-and-collect.", False)], "bullet": True,
     "before": 5},
    {"runs": [("Delivery stays, ", True), ("so the owners’ commitment holds; it is simply priced closer to "
              "its cost.", False)], "bullet": True, "before": 5},
], size=11)
s.footer(SRC + "Section 7, Table 5. FY2025 e-commerce: $7.7M contribution from new sales vs $18.1M fulfillment, a "
         "net loss of ~$10.4M. Assumes sales moved online from stores earn the same margin either way.")

# ------------------------------------------------------------------ 7. Stores
s = D.new()
s.header("Store portfolio",
         "Exiting the nine stores with negative four-wall EBITDA adds ~$6.6M a year, and six can close at lease "
         "end without a board vote")
table(s, 0.6, 1.85, [3.6, 2.35, 2.35, 1.35], [
    ["$M a year unless stated", "6 stores: lease ends by 2027", "3 stores: longer leases", "All 9"],
    ["Sales", "78.7", "39.3", "118.0"],
    ["Negative four-wall EBITDA removed", "+2.1", "+1.0", "+3.1"],
    ["Contribution on sales that move to nearby stores (25% of sales × 12%)", "+2.4", "+1.2", "+3.5"],
    ["Operating income gain", "+4.4", "+2.2", "+6.6"],
    ["One-time lease-exit cost", "None in pack; other closing costs to be costed", "7.5", "7.5"],
    ["Payback on exit cost", "—", "~3.4 years", "—"],
    ["Who decides", "Management, at lease end", "Board vote required", ""],
], [0.45, 0.42, 0.42, 0.62, 0.45, 0.62, 0.42, 0.45], size=11.5, col_align=["l", "r", "r", "r"], fills={4: LBLUE})
s.rect(10.55, 1.85, 2.18, 3.85, fill=PANEL)
s.text(10.7, 1.97, 1.9, 3.7, [
    {"text": "Sales lost", "bold": True},
    {"text": "75% of the 9 stores’ sales ($88.5M) leaves Harlow; 25% moves to nearby stores, as in past closures."},
    {"text": "Margin effect", "bold": True, "before": 8},
    {"text": "Closing all 9 lifts the margin by ~0.5 pts on its own: less sales, more profit."},
], size=11)
s.rect(0.6, 5.85, 12.13, 0.95, fill=LBLUE)
s.text(0.8, 5.92, 11.8, 0.85, [
    {"runs": [("Recommendation: ", True, DBLUE), ("give notice on the 6 expiring leases now, so their benefit lands "
              "during 2027. Run the other 3 for two quarters on the new promotion and shrink playbook. Bring them to "
              "a board vote in Q2 FY2027 if four-wall EBITDA is still negative.", False)]}], size=12, anchor="m")
s.footer(SRC + "Table 6. Figures for the 6 and the 3 are split pro rata by store count, because store-level data "
         "are not in the pack. Depreciation and allocated overhead are ignored.")

# ------------------------------------------------------------------ 8. Plan bridge
s = D.new()
s.header("The plan",
         "Five moves take operating income from $15M to ~$42M by FY2028, a 3.0% margin on smaller but more "
         "profitable sales")
s.text(0.6, 1.78, 7.6, 0.3, "Operating income, $M, FY2025 actual → FY2028 run-rate", size=12, bold=True)
items = [("FY2025 actual", 15, "total"), ("Reset promotions", 9, "delta"), ("Shrink & labor rebalance", 6, "delta"),
         ("Price delivery nearer cost", 5, "delta"), ("Exit 9 loss-making stores", 7, "delta"),
         ("Grow private label", 3, "delta"), ("2027 wage step, net", -3, "delta"), ("FY2028 plan", 42, "total")]
fmt2 = lambda v, k: (f"{v}" if k == "total" else f"{v:+d}").replace("-", "−")
base, k = waterfall(s, 0.6, 2.2, 7.6, 4.0, items, 48, fmt2, label_size=10, label_h=0.62)
s.text(0.6, 6.25, 1.9, 0.6, "1.0% margin on $1,503M sales", size=10, color=SEC, align="c", bold=True)
s.text(6.3, 6.25, 1.9, 0.6, "3.0% margin on $1,392M sales", size=10, color=DBLUE, align="c", bold=True)
table(s, 8.55, 1.8, [3.25, 0.93], [
    ["Component", "$M"],
    ["Cut loss-making promotions (29% → 25%)", "+4.4"],
    ["Vendor funding back to 51% of markdowns", "+4.5"],
    ["Shrink from 2.6% to 2.3% of sales", "+4.2"],
    ["Labor rebalance between stores, net", "+2.0"],
    ["Delivery at fee-test terms", "+2.8"],
    ["Second delivery price step (to test)", "+2.5"],
    ["Close 6 stores at lease end", "+4.4"],
    ["Exit 3 long-lease stores (board vote)", "+2.2"],
    ["Private label from 18.5% to 20.5% of sales", "+3.3"],
    ["2027 minimum wage +4%, half offset", "−3.4"],
    ["FY2028 operating income", "42.4"],
], [0.34] + [0.38] * 10 + [0.38], size=10.5, col_align=["l", "r"], fills={11: LBLUE})
s.footer("Constant FY2025 prices and volumes; components rounded, so totals may differ. Sales fall by $111M: "
         "store exits −$88.5M, lost promotional volume −$20M, delivery repricing −$2.6M. " + SRC)

# ------------------------------------------------------------------ 9. Confidence
s = D.new()
s.header("How sure we are",
         "Moves within management’s control reach 2.3%; 3.0% also needs better vendor terms, a second delivery "
         "test and a board vote")
s.text(0.6, 1.78, 7.4, 0.3, "FY2028 operating margin by case, %", size=12, bold=True)
fm3 = lambda v: (f"{v[0]:.1f}–{v[1]:.1f}%" if isinstance(v, tuple) else f"{v:.1f}%")
hbars(s, 0.6, 2.6, 7.6, [
    ("Draft plan: 8% hours cut", (1.1, 1.8), RULE),
    ("Downside case", 2.0, TOTAL),
    ("Management-controlled moves", 2.3, BLUE),
    ("Full plan", 3.0, DBLUE),
    ("Full plan + upside", 3.3, DBLUE),
], 0, 3.6, label_w=2.6, bar_h=0.4, gap=0.3, val_fmt=fm3, size=11.5, ref=(3.0, "3.0% target"))
s.text(0.6, 6.2, 7.4, 0.6, "Draft plan range: high end assumes no shrink comes back; low end assumes the FY2023–25 "
       "pattern holds.", size=10.5, color=SEC)
s.rect(8.55, 1.78, 4.18, 4.95, fill=PANEL)
s.text(8.75, 1.92, 3.8, 0.3, "What separates the cases", size=12.5, bold=True)
s.text(8.75, 2.32, 3.8, 4.35, [
    {"runs": [("Management moves → full plan (+0.7 pts): ", True), ("vendor funding +$4.5M, second delivery step +$2.5M, "
              "3 long-lease stores +$2.2M.", False)], "bullet": True},
    {"runs": [("Downside: ", True), ("half the cut promotional volume is lost, none of the wage step is offset, "
              "and none of the three items above delivers.", False)], "bullet": True, "before": 6},
    {"runs": [("Upside (+0.3 pts): ", True), ("promotions back to FY2023’s 24% (+$1.1M) and shrink back to FY2023’s "
              "2.1% (+$2.8M).", False)], "bullet": True, "before": 6},
    {"runs": [("Monthly lead indicators: ", True), ("traffic near ValuMart, shrink by store quartile, delivery vs "
              "click-and-collect mix, vendor funding rate.", False)], "bullet": True, "before": 6},
], size=11.5)
s.footer("Full plan: 3.04%. The full plan has no buffer above 3.0%, which is why the upside levers stay in "
         "reserve. " + SRC)

# ------------------------------------------------------------------ 10. Covenant
s = D.new()
s.header("FY2026 and the lender",
         "The fastest moves lift FY2026 operating income to ~$24M, clearing the $20M covenant by about $4M")
s.text(0.6, 1.78, 6.6, 0.3, "Operating income, $M, FY2025 actual → FY2026 outlook", size=12, bold=True)
items = [("FY2025 actual", 15, "total"), ("Promotions", 3, "delta"), ("Shrink & labor", 3, "delta"),
         ("Delivery repricing", 2, "delta"), ("Private label", 1, "delta"), ("FY2026 outlook", 24, "total")]
waterfall(s, 0.6, 2.2, 6.6, 4.1, items, 27, fmt2, label_size=10.5, label_h=0.55, ref=(20, "Covenant: $20M"))
s.text(0.6, 6.35, 6.6, 0.5, "In-year capture of run-rate: promotional cuts 50%, vendor funding 25%, shrink 40%, "
       "labor rebalance 50%, delivery 75%, private label 25%. No store exits in FY2026.", size=10, color=SEC)
s.rect(7.6, 1.78, 5.13, 4.95, fill=PANEL)
s.text(7.8, 1.92, 4.75, 0.3, "Protecting the covenant", size=12.5, bold=True)
s.text(7.8, 2.32, 4.75, 4.35, [
    {"runs": [("Headroom is thin. ", True), ("The outlook assumes the FY2023–25 slide stops, because its drivers "
              "are what the plan targets. If ValuMart keeps pulling sales down, headroom shrinks.", False)],
     "bullet": True},
    {"runs": [("The draft plan shows $29.8M on paper, ", True), ("but every $1M of shrink that comes back falls "
              "straight off it, and it leaves the causes of the decline in place.", False)],
     "bullet": True, "before": 6},
    {"runs": [("Contingency if month-3 tracking misses by >$1M: ", True), ("deepen the trim in the most "
              "labor-intensive stores, cut promotions to 24% early, and move one-time spend into FY2027.", False)],
     "bullet": True, "before": 6},
    {"runs": [("Brief the lender in February ", True), ("with the plan, the tracking metrics and the "
              "contingency.", False)], "bullet": True, "before": 6},
], size=11.5)
s.footer("Components rounded to whole $M (unrounded total $24.3M). Excludes one-time costs: keeping FY2026 one-time spend "
         "small protects the covenant. " + SRC)

# ------------------------------------------------------------------ 11. Roadmap
s = D.new()
s.header("Sequencing",
         "Start with the moves that need no capital and reach the P&L within a quarter; store exits and tests follow")
W = [2.35, 3.5, 3.05, 1.95, 1.28]
rows = [
    ["Move", "First 90 days (Feb–Apr 2027)", "Rest of FY2027", "FY2028", "Run-rate"],
    ["1  Price delivery nearer cost", "Roll out the $7.99 fee and $100 threshold; hold the partner’s rate",
     "Test a delivery pass or higher fee in a few stores", "Scale the second step if it pays", "+$5.3M"],
    ["2  Reset promotions", "Drop loss-making events from the next calendar; make vendor funding a slot condition",
     "Reset annual vendor terms; promotional share to ~27%", "Promotional share 25%", "+$8.9M"],
    ["3  Rebalance labor, cut shrink", "Cancel the 8% cut; restore produce rotation and receiving checks in the "
     "leanest stores", "Trim the most labor-intensive stores; track shrink by store", "Shrink 2.3% of sales",
     "+$6.2M"],
    ["4  Exit loss-making stores", "Give notice on the 6 expiring leases", "Close the 6; board vote on the other 3 "
     "in Q2", "Exit the 3 if approved ($7.5M)", "+$6.6M"],
    ["5  Grow private label", "Set range plan and category targets", "Launch range extensions", "20.5% of sales",
     "+$3.3M"],
]
table(s, 0.6, 1.8, W, rows, [0.38, 0.76, 0.76, 0.76, 0.76, 0.62], size=11, col_align=["l", "l", "l", "l", "r"],
      bold_first_col=True, fills={(r, 1): LBLUE for r in range(1, 6)})
s.text(0.6, 6.1, 12.1, 0.8, [
    {"runs": [("Why this order: ", True, DBLUE), ("the first-90-day actions are tested (delivery fee) or are "
              "management choices (promotional calendar, scheduling, lease notices). They need no capital, can be "
              "reversed, and are the only moves that can lift FY2026. Store exits and the second delivery step "
              "follow once their evidence is in.", False)]}], size=11.5)
s.footer(SRC + "Run-rates are FY2028, constant FY2025 terms, before the −$3.4M net wage step.")

# ------------------------------------------------------------------ 12. Decisions & constraints
s = D.new()
s.header("Decisions for the board",
         "We ask the board for three decisions today; the plan fits every constraint the board has set")
s.text(0.6, 1.8, 5.3, 0.3, "Decisions requested", size=13, bold=True, color=DBLUE)
decs = [("1", "Endorse the five-move plan and its first-90-day actions, in place of the 8% hours cut and the "
              "e-commerce freeze."),
        ("2", "Agree to vote in Q2 FY2027 on exiting 3 long-lease stores (up to $7.5M), if their four-wall EBITDA "
              "is still negative."),
        ("3", "Accept a delivery service priced nearer its cost: delivery stays, with a $7.99 fee, free delivery "
              "from $100, and a pass or higher fee if the test pays."),
        ("+", "Authorize the CEO and CFO to brief the lender this month.")]
dy = 2.25
for n_, t in decs:
    s.rect(0.6, dy + 0.02, 0.4, 0.4, fill=DBLUE if n_ != "+" else TOTAL, shape="oval")
    s.text(0.6, dy + 0.02, 0.4, 0.4, n_, size=13, bold=True, color=WHITE, align="c", anchor="m")
    s.text(1.15, dy, 4.75, 1.0, t, size=12.5, name="dec")
    dy += 1.12
s.text(6.4, 1.8, 6.3, 0.3, "Constraints check", size=13, bold=True, color=DBLUE)
table(s, 6.4, 2.2, [2.15, 2.65, 1.53], [
    ["Constraint", "Plan", "Status"],
    ["Operating margin ≥3.0% by FY2028", "3.0% (range 2.0–3.3%)", "Met, no buffer"],
    ["Operating income ≥$20M in FY2026", "~$24M outlook", "Met, ~$4M headroom"],
    ["≤$25M one-time cost and capital, FY2026–28", "$7.5M identified; closing, private-label and shrink costs "
     "still to be costed", "Expected to fit: $17.5M left"],
    ["No closing stores with leases beyond 2027 without a board vote", "3 such stores go to a vote", "Met"],
    ["Keep home delivery in some form", "Kept, repriced", "Met"],
], [0.38, 0.72, 0.68, 0.95, 0.85, 0.55], size=11, col_align=["l", "l", "l"],
      fills={(1, 2): "FFF1D6", (2, 2): "FFF1D6", (3, 2): "FFF1D6", (4, 2): "E3F1E3", (5, 2): "E3F1E3"})
s.footer(SRC + "Section 3. Status labels: green = met with margin to spare; amber = met or expected, but thin.")

# ------------------------------------------------------------------ 13. Appendix sizing
s = D.new()
s.header("Appendix A", "How each lever is sized")
W = [2.3, 6.55, 2.3, 0.98]
rows = [
    ["Lever", "Calculation", "Basis", "$M a year"],
    ["Cut loss-making promotions", "4 pts of sales ($60M) leave promotion; ⅔ sells at regular price (+14 pts), "
     "⅓ is lost (−6 pts: 20% contribution less 14 pts)", "Table 2; ⅔ / ⅓ split is our assumption", "+4.4"],
    ["Vendor funding 46% → 51%", "If the 14-pt gap is after funding, gross markdown = 14 ÷ 0.54 = 25.9% of promo "
     "sales; +5 pts × 25.9% × $348M", "Inference: confirm with finance", "+4.5"],
    ["Shrink 2.6% → 2.3%", "0.3 pts × $1,392M; 2.3% = FY2024 level and Q4-store level", "Tables 2, 4", "+4.2"],
    ["Labor rebalance", "Most labor-intensive quartile ≈28% of hours; trim 8% ($4.1M), put half back in the leanest "
     "quartile", "Assumed hours split", "+2.0"],
    ["Delivery at fee-test terms", "Deliveries −9%, click-and-collect +14%, fee $6.40: fulfillment $18.1M → $15.1M, "
     "less $0.15M contribution on 2% lower sales", "Fee test, Table 5", "+2.8"],
    ["Second delivery step", "Average fee $9.50 on 10% fewer deliveries (+$1.5M); $13.80 saved on each switch to "
     "click-and-collect (+$1.0M)", "Illustrative; to be tested", "+2.5"],
    ["Store exits", "Removes −$3.1M four-wall EBITDA; 25% of $118M moves at 12% (+$3.5M); split 6 : 3 by count",
     "Table 6", "+6.6"],
    ["Private label +2 pts", "2 pts × 12-pt margin gain × $1,392M; FY2023–25 pace was +0.75 pts a year",
     "Table 2", "+3.3"],
    ["2027 wage step", "4% × continuing-store labor (~$168M) = −$6.7M; half offset by price and productivity, as "
     "most of the FY2023–25 wage rise was", "Section 10; offset is our assumption", "−3.4"],
]
table(s, 0.6, 1.7, W, rows, [0.34, 0.54, 0.54, 0.4, 0.54, 0.54, 0.54, 0.54, 0.4, 0.54], size=10,
      col_align=["l", "l", "l", "r"], bold_first_col=True)
s.footer("All values in constant FY2025 terms at FY2028 run-rate. FY2028 sales base $1,392M. " + SRC)

# ------------------------------------------------------------------ 14. Appendix notes
s = D.new()
s.header("Appendix B", "Choices we made where the briefing pack is silent")
s.text(0.6, 1.8, 5.9, 5.0, [
    {"text": "Timing", "bold": True, "color": DBLUE, "size": 12.5},
    {"text": "The pack has actuals to FY2025 and treats FY2026 as the first plan year (the capital window, the draft "
             "hours cut and the covenant all start there). We do the same. If FY2026 (ending January 2027) has "
             "already closed when the board meets, replace the covenant outlook with the actual and discuss it "
             "with the lender. The FY2027–28 plan does not change.", "before": 3},
    {"text": "Constant terms", "bold": True, "color": DBLUE, "size": 12.5, "before": 10},
    {"text": "The plan is sized at FY2025 prices and volumes, with no market growth. Routine cost inflation is "
             "assumed to be covered by price. The 2027 minimum-wage step is the only headwind we model "
             "explicitly.", "before": 3},
    {"text": "Cannibalization", "bold": True, "color": DBLUE, "size": 12.5, "before": 10},
    {"text": "The 70% of online sales that would otherwise be made in-store are assumed to earn the same margin "
             "in either channel. The survey (n = 2,300) is self-reported.", "before": 3},
], size=11.5)
s.text(6.9, 1.8, 5.8, 5.0, [
    {"text": "What we have not counted", "bold": True, "color": DBLUE, "size": 12.5},
    {"text": "One-time costs other than the $7.5M lease exits (closures, private-label development, shrink "
             "tools). Finance should cost these within the $17.5M left.", "bullet": True, "before": 3},
    {"text": "Any renegotiated cut in the delivery partner’s rate (each 5% ≈ $0.5M).", "bullet": True, "before": 4},
    {"text": "Theft, 35% of shrink, beyond what better receiving catches.", "bullet": True, "before": 4},
    {"text": "Further ValuMart openings, which would add to the pressure on traffic.", "bullet": True, "before": 4},
    {"text": "What to validate before the plan is locked", "bold": True, "color": DBLUE, "size": 12.5,
     "before": 10},
    {"text": "Whether the 14-pt promotional gap is measured after vendor funding.", "bullet": True, "before": 3},
    {"text": "Labor hours and sales by quartile, and by each of the 9 weak stores.", "bullet": True, "before": 4},
    {"text": "Lease-end dates for the 6 stores, which set when their savings start.", "bullet": True, "before": 4},
], size=11.5)
s.footer(SRC)

if __name__ == "__main__":
    out = sys.argv[1]
    prev = sys.argv[2]
    D.save(out)
    os.makedirs(prev, exist_ok=True)
    render(D, prev)
    print("\n".join(D.issues) or "no fit issues")
