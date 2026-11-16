import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from engine import Slide, Text, Rect, Line, W, H, render_png, render_pptx
from components import *

SRC = "Source: Harlow Fresh Markets briefing pack (synthetic benchmark data)"
slides = []


def new(kicker, title, source=SRC):
    s = base_slide(kicker, title, source, page=len(slides) + 1)
    slides.append(s)
    return s


# ------------------------------------------------------------------ 1. Title
s = Slide(); slides.append(s)
s.add(Rect(0, 0, W, H, fill=NAVY))
s.add(Rect(L, 2.35, 0.12, 2.2, fill=BLUE))
s.add(Text(L + 0.35, 2.25, 11.5, 1.1, "Reversing the margin decline", size=40, bold=True, color="#ffffff"))
s.add(Text(L + 0.35, 3.3, 11.5, 1.2,
           "A plan to take Harlow Fresh Markets' operating margin from 1.0% back to 3.0% by FY2028, and what to do first",
           size=20, color="#cde2fb"))
s.add(Text(L + 0.35, 5.3, 11.5, 0.9, ["Board of Directors meeting, February 2027",
                                      "Presented by Dana Whitfield, Chief Executive Officer"],
           size=14, color="#ffffff"))
s.add(Text(L + 0.35, 6.75, 12, 0.4, "All figures in $ millions unless stated. Fiscal years end in January. "
           "Based only on the board briefing pack (synthetic benchmark data).", size=9, color="#9ec5f4"))

# ------------------------------------------------------------------ 2. Executive summary
s = new("Executive summary",
        "Margin is falling because of promotions, shrink and e-commerce delivery, not wages; fixing those first gets Harlow to ~3% by FY2028")
col_y, col_h = 1.75, 4.95
cols = [
    ("What happened", [
        {"t": "Operating margin fell from **3.4% to 1.0%** in two years (FY2023–FY2025); operating income fell from $47.9M to $15.3M while sales grew 6%.", "bullet": True},
        {"t": "**About 80%** of the fall is gross margin (deeper promotions, more shrink) and e-commerce fulfilment. Store labor explains **13%**: wages rose 9.4%, but 6% fewer hours per sales dollar offset most of it.", "bullet": True, "before": 6},
        {"t": "E-commerce **loses ~$10M a year** once third-party delivery and sales taken from our own stores are counted.", "bullet": True, "before": 6},
    ]),
    ("What we recommend", [
        {"t": "Replace the 8% across-the-board labor cut with **six actions**: cut loss-making promotions, restore fresh and receiving routines to cut shrink, reprice delivery, grow private label, exit the nine loss-making stores, and target labor savings where hours are heaviest.", "bullet": True},
        {"t": "Result: **~$39M operating income (2.8%)** in FY2028 on cautious assumptions; **$5.5M of named stretch levers** take it to 3.1%. Management's draft plan reaches ~1.5%.", "bullet": True, "before": 6},
        {"t": "**Start with promotions, delivery pricing and shrink**: fast, low-capital, partly tested. They should lift FY2026 to ~$24–28M, above the $20M covenant.", "bullet": True, "before": 6},
    ]),
    ("Decisions needed today", [
        {"t": "Approve the plan in place of the draft labor-cut plan, and launch wave 1 now.", "bullet": True},
        {"t": "Approve in principle the exit of the three loss-making stores whose leases run beyond 2027 ($7.5M one-time); store-by-store cases come to the next board meeting.", "bullet": True, "before": 6},
        {"t": "Keep home delivery, but repriced, with delivered-order growth on hold until each order covers its cost.", "bullet": True, "before": 6},
    ]),
]
cw3 = (CW - 0.4) / 3
for i, (hd, ps) in enumerate(cols):
    x = L + i * (cw3 + 0.2)
    fill = PANEL if i < 2 else "#e8f1fc"
    s.add(Rect(x, col_y, cw3, col_h, fill=fill))
    s.add(Rect(x, col_y, cw3, 0.06, fill=BLUE if i == 2 else NAVY))
    s.add(Text(x + 0.18, col_y + 0.2, cw3 - 0.36, 0.35, hd, size=13, bold=True, color=NAVY))
    s.add(Text(x + 0.18, col_y + 0.62, cw3 - 0.36, col_h - 0.75, ps, size=11.5))

# ------------------------------------------------------------------ 3. Margin bridge FY2023 -> FY2025
s = new("Diagnosis: where the margin went",
        "Operating margin fell 2.4 points in two years; gross margin and e-commerce explain about 80% of the fall, store labor about 13%",
        SRC + ", Table 1. Change in each line as a % of sales, FY2023 to FY2025; $ effect valued at FY2025 sales of $1,503M. "
              "Sales growth at the FY2023 margin added ~$2.8M. Points may not sum exactly because of rounding.")
steps = [
    {"label": "FY2023 margin", "v": 3.37, "kind": "total", "vlabel": "3.37%"},
    {"label": "Gross margin rate", "v": -1.02, "kind": "delta", "sub": "26.0% → 25.0% of sales\n−$15.3M"},
    {"label": "E-commerce fulfilment", "v": -0.84, "kind": "delta", "sub": "0.4% → 1.2% of sales\n−$12.6M"},
    {"label": "Store labor", "v": -0.30, "kind": "delta", "sub": "11.8% → 12.1%\n−$4.5M"},
    {"label": "Occupancy & energy", "v": -0.20, "kind": "delta", "sub": "5.8% → 6.0%\n−$3.0M"},
    {"label": "Other SG&A", "v": 0.0, "kind": "delta", "color": "#9a9893", "sub": "4.7% → 4.7%\n$0.0M", "vlabel": "0.00"},
    {"label": "FY2025 margin", "v": 1.02, "kind": "total", "vlabel": "1.02%"},
]
# sub labels contain newlines -> split into paragraphs
for st in steps:
    if st.get("sub") and "\n" in st["sub"]:
        pass
s.add(Text(L, 1.68, 8.2, 0.3, "Operating margin, % of sales, FY2023 → FY2025 (points of sales)", size=11, bold=True, color=INK2))


def waterfall_multisub(s, x, y, w, h, steps, vmin, vmax, **kw):
    # expand multi-line sublabels into separate paragraphs via a custom label pass
    st2 = []
    subs = []
    for st in steps:
        st = dict(st)
        subs.append(st.pop("sub", None))
        st2.append(st)
    Y = waterfall(s, x, y, w, h, st2, vmin, vmax, **kw)
    n = len(steps); slot = w / n
    label_h = kw.get("label_h", 0.62)
    bottom = y + h - label_h
    for i, sub in enumerate(subs):
        if sub:
            s.add(Text(x + slot * i + 0.02, bottom + 0.42, slot - 0.04, label_h - 0.42,
                       [{"t": ln} for ln in sub.split("\n")], size=9, color=INK2, align="c"))
    return Y


waterfall_multisub(s, L, 2.0, 8.2, 4.75, steps, 0, 3.8, dec=2, label_h=1.0, label_size=10, value_size=11)
panel(s, L + 8.55, 1.75, CW - 8.55, 4.95, "What the bridge shows", [
    {"t": "**Gross margin and e-commerce** together took 1.86 of the 2.36 points lost. Both are commercial and operating choices we control.", "bullet": True},
    {"t": "**E-commerce fulfilment** nearly tripled as a share of sales: orders rose from 453k to 1.33M and home delivery's share of orders rose from 45% to 58%.", "bullet": True, "before": 6},
    {"t": "**Store labor** rose only 0.3 points of sales despite 9.4% wage inflation (page 5). It is a real pressure, but not the main one.", "bullet": True, "before": 6},
    {"t": "Other SG&A held steady at 4.7% of sales.", "bullet": True, "before": 6},
], size=11)

# ------------------------------------------------------------------ 4. Gross margin
s = new("Diagnosis: gross margin",
        "Deeper promotions and higher shrink cut gross margin by 1.2 points; private-label growth won back only 0.2",
        SRC + ", Tables 1–2 and sections 5 and 9. Effect = change in share of sales × margin gap (promotions −14 pts, private label +12 pts); "
              "shrink effect = change in shrink % of sales. $ at FY2025 sales.")
s.add(Text(L, 1.68, 6.9, 0.3, "Gross margin change FY2023 → FY2025, points of sales ($M)", size=11, bold=True, color=INK2))
hbars(s, L, 2.15, 6.9, [
    ("More promotional sales", -0.70, "24.0% → 29.0% of sales", None, "−0.70 (−$10.5M)"),
    ("Higher shrink", -0.50, "2.1% → 2.6% of sales", None, "−0.50 (−$7.5M)"),
    ("More private label", 0.18, "17.0% → 18.5% of sales", None, "+0.18 (+$2.7M)"),
    ("Net change in gross margin", -1.02, "26.0% → 25.0% of sales", TOTAL, "−1.02 (−$15.3M)"),
], vmin=-1.6, vmax=0.75, label_w=2.55, row_h=0.95, value_w=1.55, dec=2, label_size=11)
s.add(Text(L, 6.05, 6.9, 0.7, "The three drivers in the pack add up exactly to the 1.02-point fall, so nothing material is missing from this explanation.",
           size=10.5, color=INK2))
panel(s, L + 7.25, 1.75, CW - 7.25, 4.95, "Promotions are not paying for themselves", [
    {"t": "**38% of FY2025 promotional events lost money**, even after counting the extra units they sold.", "bullet": True},
    {"t": "Vendors now fund less of each markdown: **46%** in FY2025, down from 55% in FY2023.", "bullet": True, "before": 5},
    {"t": "Deeper promotions did not fix price perception: **41%** of customers now call Harlow \"more expensive\" (33% in FY2023). Their top reasons to shop with us are fresh produce (58%) and convenience (44%).", "bullet": True, "before": 5},
    {"t": "The category team's evidence (deep-promotion stores: comparable sales +1.8% vs +0.2%) measures sales, not profit. Each extra point of promotional share costs 0.14% of sales in margin, so it needs ~0.7% more sales at 20% contribution just to break even.", "bullet": True, "before": 5},
], size=11)

# ------------------------------------------------------------------ 5. Labor
s = new("Diagnosis: store labor",
        "Wages rose 9%, but productivity absorbed most of it; cutting hours further risks more shrink, which is already highest in the leanest stores",
        SRC + ", Tables 3–4 and section 6. Labor % of sales = wage × hours per $1,000 of sales. Quartiles rank stores by labor hours per $1,000 of sales. "
              "The shrink pattern is a correlation across stores, not proof of cause.")
s.add(Text(L, 1.68, 5.6, 0.3, "Store labor as % of sales: what changed, FY2023 → FY2025", size=11, bold=True, color=INK2))
hbars(s, L, 2.1, 5.6, [
    ("Wage rate +9.4%", 1.1, "$16.80 → $18.38 per hour", ORANGE, "+1.1 pts"),
    ("Hours per $1,000 of sales −6.0%", -0.8, "7.02 → 6.60 hours", BLUE, "−0.8 pts"),
    ("Net change in labor % of sales", 0.3, "11.8% → 12.1% (−$4.5M)", TOTAL, "+0.3 pts"),
], vmin=-1.2, vmax=1.5, label_w=2.45, row_h=0.8, value_w=0.8, dec=1, label_size=11)
# shrink by quartile column chart
cx0, cy0, cwid, chh = L + 6.2, 2.1, 5.8, 2.2
s.add(Text(L + 6.2, 1.68, 6.0, 0.3, "Shrink, % of sales, FY2025, by store labor quartile (chain average 2.6%)", size=11, bold=True, color=INK2))
qs = [("Q1\nfewest hours", 3.1), ("Q2", 2.7), ("Q3", 2.4), ("Q4\nmost hours", 2.3)]
vmax = 3.5
base_y = cy0 + chh
s.add(Line(cx0, base_y, cx0 + cwid, base_y, color=MUTED))
slotw = cwid / 4
for i, (lab, v) in enumerate(qs):
    bx = cx0 + i * slotw + slotw * 0.22
    bh = v / vmax * (chh - 0.3)
    s.add(Rect(bx, base_y - bh, slotw * 0.56, bh, fill=ORANGE if i == 0 else "#e8a184" if i == 1 else "#c9c7c1"))
    s.add(Text(bx - 0.2, base_y - bh - 0.3, slotw * 0.56 + 0.4, 0.28, f"{v:.1f}%", size=11, bold=True, align="c", valign="b"))
    s.add(Text(cx0 + i * slotw, base_y + 0.05, slotw, 0.5, [{"t": t} for t in lab.split("\n")], size=10, align="c", color=INK))
s.add(Rect(L, 5.05, CW, 1.67, fill="#fdf1eb"))
s.add(Rect(L, 5.05, 0.07, 1.67, fill=ORANGE))
s.add(Text(L + 0.25, 5.12, CW - 0.4, 0.3, "Implication for management's 8% hour cut (~$14.5M a year)", size=12, bold=True, color=NAVY))
s.add(Text(L + 0.25, 5.45, CW - 0.4, 1.25, [
    {"t": "It would take the chain to ~6.1 hours per $1,000 of sales. The last 6% reduction came with shrink rising 0.5 points (~$7.5M a year), and managers in the leanest stores say produce rotation and receiving checks are skipped on busy days. Each 0.1 point of shrink costs ~$1.5M, so the cut could give back half its savings, before any effect on checkout waits or stock-outs.", "bullet": True},
    {"t": "**Better: target hours where labor is heaviest and shrink lowest (Q3–Q4), and protect fresh and receiving tasks in the leanest stores.**", "bullet": True, "before": 4},
], size=11))

# ------------------------------------------------------------------ 6. E-commerce economics
s = new("Diagnosis: e-commerce",
        "E-commerce loses about $10M a year once delivery costs and sales taken from our stores are counted, not the 6.1% profit reported",
        SRC + ", Table 5 and sections 7 and 10. New contribution = $96 basket × 30% genuinely new sales (survey: 70% would otherwise be bought in a Harlow store) × $0.20 "
              "contribution per new $. FY2025: 1,331k orders, 58% delivered.")
s.add(Text(L, 1.68, 7.3, 0.3, "Contribution per order, FY2025 ($)", size=11, bold=True, color=INK2))
hdr = ["", "Click-and-collect", "Home delivery"]
rows = [
    ["New contribution per order", {"t": "+5.76"}, {"t": "+5.76"}],
    ["Picking", {"t": "−7.40"}, {"t": "−7.40"}],
    ["Third-party delivery", {"t": "–", "color": MUTED}, {"t": "−13.80"}],
    ["Delivery fee collected", {"t": "–", "color": MUTED}, {"t": "+3.10"}],
    [{"t": "Net per order", "bold": True}, {"t": "−1.64", "bold": True}, {"t": "−12.34", "bold": True, "color": RED}],
    [{"t": "Orders, FY2025", "bold": False, "color": INK2}, {"t": "559k", "color": INK2}, {"t": "772k", "color": INK2}],
    [{"t": "Annual result", "bold": True}, {"t": "−$0.9M", "bold": True}, {"t": "−$9.5M", "bold": True, "color": RED}],
]
end_y = table(s, L, 1.95, [3.1, 2.1, 2.1], rows, header=hdr, row_h=0.45, size=11.5, col_align=["l", "r", "r"],
              bold_first=False, fills=[None, None, None, None, "#f4f3f0", None, "#f4f3f0"])
s.add(Rect(L, end_y + 0.15, 7.3, 0.62, fill=NAVY))
s.add(Text(L + 0.15, end_y + 0.15, 7.0, 0.62, "Total e-commerce: −$10.4M a year, versus +$7.8M (6.1% of $127.8M sales) in the e-commerce team's update",
           size=12, bold=True, color="#ffffff", valign="m"))
panel(s, L + 7.65, 1.75, CW - 7.65, 4.95, "Why the reported 6.1% margin is wrong", [
    {"t": "**It leaves out third-party delivery**, which finance books separately: $10.7M of cost less $2.4M of fees, a net $8.3M in FY2025.", "bullet": True},
    {"t": "**It counts every online sale as new.** Customers say 70% of what they buy online they would otherwise have bought in a Harlow store, where we already earn that margin.", "bullet": True, "before": 6},
    {"t": "**The conclusion holds even if the survey is wrong:** at today's costs e-commerce breaks even only if more than 70% of its sales are new to Harlow.", "bullet": True, "before": 6},
    {"t": "**Click-and-collect is close to break-even; home delivery is the problem.** Delivery is free above $75 and the average basket is $96, so most delivered orders pay no fee.", "bullet": True, "before": 6},
], size=11)

# ------------------------------------------------------------------ 7. E-commerce fix
s = new("Options: e-commerce",
        "The tested delivery pricing saves ~$2.5M a year and keeps 98% of e-commerce sales; the 2026 contract renewal is the next lever",
        SRC + ", Table 5 and section 7. Fee test: 4 stores, 10 weeks, late FY2025; results applied to FY2025 volumes. Lost contribution assumes all lost e-commerce sales "
              "leave Harlow at 20% contribution (cautious).")
s.add(Text(L, 1.68, 3.6, 0.3, "Fee test: $7.99 fee, free above $100", size=11, bold=True, color=INK2))
kp = [("−9%", "delivered orders"), ("+14%", "click-and-collect orders"), ("−2%", "total e-commerce sales"),
      ("$3.10 → $6.40", "fee collected per delivered order")]
for i, (big, small) in enumerate(kp):
    yy = 2.08 + i * 1.12
    s.add(Rect(L, yy, 3.6, 1.0, fill=PANEL))
    s.add(Text(L + 0.15, yy + 0.08, 3.3, 0.5, big, size=20, bold=True, color=NAVY))
    s.add(Text(L + 0.15, yy + 0.58, 3.3, 0.35, small, size=11, color=INK2))
s.add(Text(L + 3.95, 1.68, 4.1, 0.3, "Annual effect of chain-wide rollout ($M)", size=11, bold=True, color=INK2))
waterfall(s, L + 3.95, 2.0, 4.1, 4.4, [
    {"label": "Fulfilment cost today", "v": 18.1, "kind": "total"},
    {"label": "Lower net delivery cost", "v": -3.0, "kind": "delta", "vlabel": "−3.0", "color": BLUE},
    {"label": "Fulfilment cost after", "v": 15.1, "kind": "total"},
], 0, 20, dec=1, label_h=0.62, bar_frac=0.55)
s.add(Text(L + 3.75, 6.38, 4.5, 0.48, "Saving $3.0M less ≤$0.5M contribution on lost sales = **~$2.5M a year net**",
           size=10.5, color=INK, align="c"))
panel(s, L + 8.4, 1.75, CW - 8.4, 4.95, "What we will do", [
    {"t": "**Roll out the tested pricing chain-wide now.** No capital needed; most lost delivery orders switch to click-and-collect.", "bullet": True},
    {"t": "**Use the 2026 contract renewal.** The provider's proposed 3% rise would cost ~$0.3M a year; each $1 off the rate per delivered order is worth ~$0.7M.", "bullet": True, "before": 6},
    {"t": "**Keep delivery, but stop it growing at a loss.** Even after the fee change a delivered order loses ~$9, so we hold delivered volume flat, steer customers to click-and-collect, and test the next fee step.", "bullet": True, "before": 6},
    {"t": "This keeps the owners' commitment to delivery; the draft plan's freeze alone would leave the ~$10M loss in place.", "bullet": True, "before": 6},
], size=11)

# ------------------------------------------------------------------ 8. Stores
s = new("Options: store portfolio",
        "Exiting the nine loss-making stores adds ~$6.6M a year; six can close as their leases expire, without a board vote",
        SRC + ", Table 6. Split between the 6 and 3 stores assumes losses and sales are spread evenly (the pack gives only combined figures). "
              "Closure costs other than lease exits are not in the pack.")
s.add(Text(L, 1.68, 6.2, 0.3, "Annual operating income effect of exiting all nine stores ($M)", size=11, bold=True, color=INK2))
waterfall(s, L, 2.0, 6.2, 4.3, [
    {"label": "Stop four-wall losses", "v": 3.1, "kind": "delta", "sub": "nine stores, −$3.1M EBITDA"},
    {"label": "Keep sales that move", "v": 3.5, "kind": "delta", "sub": "25% of $118M at 12%"},
    {"label": "Total gain", "v": 6.6, "kind": "total", "color": BLUE, "sub": "chain sales fall ~$88M"},
], 0, 7.5, dec=1, label_h=0.75, bar_frac=0.5)
rows = [
    ["6 stores, leases end by 2027", "~$4.4M", "None", "–", "CEO decision"],
    ["3 stores, leases run longer", "~$2.2M", "$7.5M", "~3.4 years", "Board vote"],
]
s.add(Text(L + 6.6, 1.68, CW - 6.6, 0.3, "Two groups, two routes", size=11, bold=True, color=INK2))
table(s, L + 6.6, 1.9, [1.75, 1.0, 1.05, 0.9, 0.93], rows,
      header=["Group", "Annual gain", "One-time cost", "Payback", "Approval"], row_h=0.62, size=10.5,
      col_align=["l", "r", "r", "r", "r"])
panel(s, L + 6.6, 3.85, CW - 6.6, 2.85, "How we will approach it", [
    {"t": "Use each lease expiry to **renegotiate rent first**; close only if four-wall EBITDA stays negative.", "bullet": True},
    {"t": "Ask the board to **approve in principle** the three longer-lease exits now, with a store-by-store case at the next meeting.", "bullet": True, "before": 5},
    {"t": "Exits land across FY2027–FY2028 as leases end, so the full run-rate may come only in FY2029.", "bullet": True, "before": 5},
], size=11)

# ------------------------------------------------------------------ 9. Management plan vs recommended
s = new("Options: comparing the plans",
        "The draft labor-led plan reaches only ~1.5% margin by FY2028 because it leaves the largest causes of the decline untouched",
        SRC + ". Management plan: 8% fewer hours ($14.5M), e-commerce frozen, all 58 stores kept (FY2025 sales base). Both plans absorb the 2027 minimum-wage rise "
              "(+4%, assumed to apply to all store labor). Recommended plan detail on page 10.")
s.add(Text(L, 1.68, 5.3, 0.3, "FY2028 operating margin, % of sales", size=11, bold=True, color=INK2))
bars = [("FY2025\nactual", 1.02, TOTAL, "1.0%"), ("Draft plan\n(labor cut)", 1.50, "#c9c7c1", "1.5%"),
        ("Recommended\nplan", 2.76, BLUE, "2.8%"), ("With stretch\nlevers", 3.15, BLUE_LT, "3.1%")]
bx0, by0, bwid, bhh = L + 0.1, 2.05, 5.2, 3.75
base_y = by0 + bhh
vmax = 3.6
s.add(Line(bx0, base_y, bx0 + bwid, base_y, color=MUTED))
sl = bwid / len(bars)
for i, (lab, v, col, vt) in enumerate(bars):
    x = bx0 + i * sl + sl * 0.2
    hh = v / vmax * bhh
    s.add(Rect(x, base_y - hh, sl * 0.6, hh, fill=col))
    s.add(Text(x - 0.2, base_y - hh - 0.32, sl * 0.6 + 0.4, 0.3, vt, size=12, bold=True, align="c", valign="b"))
    s.add(Text(bx0 + i * sl, base_y + 0.06, sl, 0.55, [{"t": t} for t in lab.split("\n")], size=10, align="c"))
ty = base_y - 3.0 / vmax * bhh
s.add(Line(bx0, ty, bx0 + bwid, ty, color=GREEN, lw=1.25, dash=True))
s.add(Text(bx0, ty - 0.3, 2.4, 0.26, "Board target 3.0%", size=9.5, bold=True, color=GREEN))
s.add(Text(L, 6.45, 5.4, 0.4, "Draft plan range: 2.0% if the wage rise is ignored; ~1.0% if shrink rises as it did after the last hour cuts.",
           size=9.5, color=INK2))
hdr = ["Cause (FY2023–25 effect)", "Draft plan", "Recommended plan"]
rows = [
    ["Promotions (−0.70 pts)", {"t": "Not addressed", "color": RED}, "Cut loss-making events; promo share 29% → 25%"],
    ["Shrink (−0.50 pts)", {"t": "Likely worse with fewer hours", "color": RED}, "Restore produce rotation and receiving checks; 2.6% → 2.3%"],
    ["E-commerce (−0.84 pts)", {"t": "Frozen; ~$10M loss stays", "color": RED}, "Reprice delivery, renegotiate contract, steer to collect"],
    ["Store labor (−0.30 pts)", "8% fewer hours in every store", "8% fewer hours in the most labor-heavy half only"],
    ["Loss-making stores", {"t": "Not addressed", "color": RED}, "Exit 9 stores, 6 at lease expiry"],
]
table(s, L + 5.75, 1.75, [2.05, 2.05, 2.6], rows, header=hdr, row_h=0.78, size=10.5, col_align=["l", "l", "l"])
s.add(Text(L + 5.75, 6.25, 6.7, 0.5, "Private-label growth (18.5% → 20% of sales) is a further lever in the recommended plan only.",
           size=10, color=INK2))

# ------------------------------------------------------------------ 10. FY2028 bridge
s = new("The plan",
        "The plan rebuilds operating income to ~$39M (2.8%) by FY2028; $5.5M of named stretch levers would take it past 3.0%",
        "Rate levers valued on a FY2028 sales base of $1,415M (FY2025 sales less the nine stores, plus recaptured sales; no market growth assumed). Labor: 8% fewer hours in the "
        "most labor-heavy half of stores (~4% of chain hours). Wage rise: +4% on all store labor (cautious). Stretch: promotions to 24% (+$2.0M), shrink to 2.1% (+$2.8M), "
        "$1 lower delivery rate (+$0.7M). Vendor-funding recovery not counted.")
s.add(Text(L, 1.68, 9, 0.3, "Operating income bridge, FY2025 actual → FY2028 plan ($M)", size=11, bold=True, color=INK2))
steps = [
    {"label": "FY2025 actual", "v": 15.3, "kind": "total", "sub": "1.0%"},
    {"label": "Promotions", "v": 7.9, "kind": "delta", "sub": "29% → 25% share"},
    {"label": "Private label", "v": 2.5, "kind": "delta", "sub": "18.5% → 20%"},
    {"label": "Shrink", "v": 4.2, "kind": "delta", "sub": "2.6% → 2.3%"},
    {"label": "Delivery pricing", "v": 2.5, "kind": "delta", "sub": "tested fee"},
    {"label": "Store exits", "v": 6.6, "kind": "delta", "sub": "9 stores"},
    {"label": "Targeted labor", "v": 6.8, "kind": "delta", "sub": "~4% of hours"},
    {"label": "2027 wage rise", "v": -6.8, "kind": "delta", "sub": "+4% min. wage"},
    {"label": "FY2028 plan", "v": 39.0, "kind": "total", "color": NAVY, "sub": "2.8%"},
    {"label": "Stretch levers", "v": 5.5, "kind": "stretch", "sub": "named, not yet banked"},
    {"label": "With stretch", "v": 44.5, "kind": "total", "color": BLUE, "sub": "3.1%"},
]
waterfall(s, L, 1.95, CW, 4.85, steps, 0, 50, dec=1, label_h=0.75, bar_frac=0.6, label_size=10, value_size=11,
          target=42.4, target_label="3.0% target = $42.4M")

# ------------------------------------------------------------------ 11. Prioritisation
s = new("Sequencing: what to do first",
        "Start with three fast, low-capital moves: they deliver about half of the plan's gross gains and protect the FY2026 covenant",
        SRC + ". FY2028 run-rate impact. Confidence reflects the strength of evidence in the pack. One-time costs other than the $7.5M lease exits are not in the pack and need a CFO estimate.")
hdr = ["Action", "FY2028 impact", "Time to impact", "Evidence and confidence", "One-time cost", "Approval"]
W1, W2, W3 = "#e8f1fc", "#f4f3f0", "#ffffff"
rows = [
    [{"t": "WAVE 1  Start now", "color": BLUE, "size": 10}, "", "", "", "", ""],
    ["Cut loss-making promotions (share 29% → 25%), holding price where ValuMart competes", "+$7.9M", "3–6 months", "Medium: 38% of events lose money; traffic risk near ValuMart", "Minimal", "CEO"],
    ["Roll out tested delivery pricing; renegotiate the delivery contract", "+$2.5M", "1–3 months", "High: 10-week test in 4 stores", "None", "CEO"],
    ["Restore produce rotation and receiving checks in the leanest stores", "+$4.2M", "3–9 months", "Medium: shrink 3.1% vs 2.3% across labor quartiles", "Small", "CEO"],
    [{"t": "WAVE 2  From mid-FY2026", "color": BLUE, "size": 10}, "", "", "", "", ""],
    ["Cut hours 8% in the most labor-heavy half of stores; protect fresh and receiving", "+$6.8M", "6–12 months", "Medium: watch shrink and checkout waits", "None", "CEO"],
    ["Grow private label from 18.5% to 20% of sales", "+$2.5M", "12–24 months", "Medium: +12 pts margin; continues the trend", "Small", "CEO"],
    [{"t": "WAVE 3  As leases end, FY2027–FY2028", "color": BLUE, "size": 10}, "", "", "", "", ""],
    ["Exit six loss-making stores at lease expiry", "+$4.4M", "FY2027–28", "High: based on past closures", "Not in pack", "CEO"],
    ["Exit three loss-making stores with longer leases", "+$2.2M", "FY2027–28", "High: based on past closures", "$7.5M", "Board vote"],
]
rh = [0.32, 0.56, 0.5, 0.5, 0.32, 0.5, 0.5, 0.32, 0.45, 0.45]
fills = [None, W1, W1, W1, None, None, None, None, None, None]
table(s, L, 1.62, [4.4, 1.2, 1.3, 3.25, 1.0, 1.08], rows, header=hdr, row_h=0.5, size=10, head_size=10,
      col_align=["l", "r", "l", "l", "l", "l"], row_heights=rh, fills=fills)
s.add(Text(L, 6.48, CW, 0.35, "Wave 1 = $14.6M of the $30.5M gross gains (48%). The 2027 wage rise (−$6.8M) offsets the labor lever.",
           size=10.5, bold=True, color=NAVY))

# ------------------------------------------------------------------ 12. Roadmap and covenant
s = new("Sequencing: roadmap and covenant",
        "Wave 1 should lift FY2026 operating income to ~$24–28M, above the $20M covenant; identified one-time costs are $7.5M of the $25M budget",
        SRC + ". FY2026 in-year estimates assume: half the promotion reset (2 pts), 9 months of delivery pricing, a 0.15-pt shrink reduction, half a year of targeted labor "
              "savings and +0.5 pt private label, valued at FY2025 sales, with the underlying business holding at FY2025 levels.")
gx, gy = L, 1.75
lab_w = 3.3
per = ["FY26 H1", "FY26 H2", "FY27 H1", "FY27 H2", "FY28 H1", "FY28 H2"]
pw = (7.6 - lab_w) / len(per)
for j, p in enumerate(per):
    s.add(Text(gx + lab_w + j * pw, gy, pw, 0.3, p, size=9.5, bold=True, color=INK2, align="c"))
s.add(Line(gx, gy + 0.34, gx + 7.6, gy + 0.34, color=INK2, lw=1))
grows = [
    ("Wave 1", None, None, None),
    ("Promotion reset (outside ValuMart areas first)", 0, 3, BLUE),
    ("Delivery pricing and contract", 0, 1, BLUE),
    ("Fresh and receiving routines (shrink)", 0, 2, BLUE),
    ("Wave 2", None, None, None),
    ("Targeted labor scheduling", 1, 3, "#5598e7"),
    ("Private-label growth", 1, 6, "#5598e7"),
    ("Wave 3", None, None, None),
    ("Six store exits at lease expiry", 2, 6, "#86b6ef"),
    ("Three longer-lease exits (board vote)", 2, 5, "#86b6ef"),
]
yy = gy + 0.42
for lab, a, b, col in grows:
    if a is None:
        s.add(Text(gx, yy, lab_w, 0.28, lab.upper(), size=9, bold=True, color=BLUE))
        yy += 0.3
        continue
    s.add(Text(gx, yy, lab_w - 0.1, 0.38, lab, size=10, valign="m"))
    s.add(Rect(gx + lab_w + a * pw + 0.04, yy + 0.09, (b - a) * pw - 0.08, 0.2, fill=col))
    yy += 0.4
for j in range(len(per) + 1):
    s.add(Line(gx + lab_w + j * pw, gy + 0.34, gx + lab_w + j * pw, yy, color="#ebeae6", lw=0.5))
# milestones
s.add(Text(gx + lab_w + 2 * pw - 0.95, yy + 0.05, 1.9, 0.5, ["▲ FY2026 covenant test", "operating income ≥ $20M"], size=9, color=INK2, align="c"))
s.add(Text(gx + 7.6 - 1.6, yy + 0.05, 1.6, 0.5, ["FY2028 target ▲", "margin ≥ 3.0%"], size=9, color=INK2, align="r"))
# covenant box
bx = L + 8.0
bw_ = CW - 8.0
s.add(Rect(bx, 1.75, bw_, 2.75, fill=PANEL))
s.add(Text(bx + 0.15, 1.85, bw_ - 0.3, 0.3, "FY2026 operating income outlook ($M)", size=12, bold=True, color=NAVY))
crow = [
    ["FY2025 actual", "15.3"],
    ["Wave 1 in-year", "+8.4"],
    [{"t": "After wave 1", "bold": True}, {"t": "23.7", "bold": True}],
    ["Wave 2 starts in-year", "+4.3"],
    [{"t": "After waves 1 and 2", "bold": True}, {"t": "28.0", "bold": True}],
    [{"t": "Lender covenant", "color": GREEN, "bold": True}, {"t": "≥ 20.0", "color": GREEN, "bold": True}],
]
table(s, bx + 0.15, 2.2, [bw_ - 1.3, 1.0], crow, row_h=0.36, size=10.5, col_align=["l", "r"], bold_first=False)
s.add(Rect(bx, 4.65, bw_, 2.05, fill=PANEL))
s.add(Text(bx + 0.15, 4.75, bw_ - 0.3, 0.3, "Capital and one-time cost", size=12, bold=True, color=NAVY))
s.add(Text(bx + 0.15, 5.1, bw_ - 0.3, 1.55, [
    {"t": "Identified: $7.5M for the three lease exits.", "bullet": True},
    {"t": "Not yet costed: closing the six other stores, shrink controls, private-label development. The CFO will cost these before the next board meeting.", "bullet": True, "before": 4},
    {"t": "Headroom under the $25M cap: $17.5M.", "bullet": True, "before": 4},
], size=10.5))

# ------------------------------------------------------------------ 13. Risks
s = new("Risks",
        "Five risks could knock the plan off course; each has an early warning sign and an agreed response",
        SRC + ", sections 9 and 11.")
hdr = ["Risk", "Early warning sign we will track", "Agreed response"]
rows = [
    ["Cutting promotions loses traffic to ValuMart (11 stores opened in our trade areas since 2023)",
     "Weekly traffic and comparable sales in stores within three miles of a ValuMart (already −4.2% in FY2025)",
     "Cut first outside ValuMart areas; where traffic falls, put part of the saving into private label and everyday prices"],
    ["Fewer hours raise shrink or hurt service",
     "Shrink % by store; checkout waits; stock-outs",
     "Protect fresh and receiving hours; pause cuts in any store whose shrink rises 0.2 pts"],
    ["Delivery customers leave after repricing",
     "E-commerce sales against the test's −2%; switching to click-and-collect",
     "Adjust fee and threshold; the test showed most delivery customers switch rather than leave"],
    ["Costs rise further: delivery contract (+3% proposed), minimum wage (+4% in 2027)",
     "Contract terms at renewal; wage settlements",
     "Plan already absorbs the full wage rise; rebid delivery if the provider will not hold rates"],
    ["E-commerce cannibalisation estimate rests on a survey",
     "Basket and store-visit data for online customers",
     "Low exposure: e-commerce loses money unless over 70% of its sales are new"],
]
table(s, L, 1.7, [4.0, 4.0, 4.23], rows, header=hdr, row_h=0.88, size=10.5, col_align=["l", "l", "l"])

# ------------------------------------------------------------------ 14. Decisions
s = new("Decisions requested",
        "We ask the board for four decisions today, and will report progress against four measures every quarter",
        None)
dec = [
    ("1", "Approve the margin plan in place of the draft labor-cut plan",
     "Identified levers reach ~$39M (2.8%) by FY2028; reaching the 3.0% target needs at least $3.4M of the $5.5M named stretch levers, which we will pursue in parallel."),
    ("2", "Launch wave 1 now",
     "Promotion reset, chain-wide delivery pricing and contract renegotiation, fresh and receiving routines. No significant capital."),
    ("3", "Approve in principle the exit of three stores with leases beyond 2027",
     "$7.5M one-time cost, ~$2.2M a year, ~3.4-year payback. Store-by-store cases at the next board meeting for the formal vote."),
    ("4", "Keep home delivery, repriced",
     "Honours the owners' commitment; delivered-order growth paused until each order covers its cost."),
]
for i, (n, hd, body) in enumerate(dec):
    yy = 1.75 + i * 1.02
    s.add(Rect(L, yy, 0.6, 0.6, fill=NAVY, shape="oval"))
    s.add(Text(L, yy, 0.6, 0.6, n, size=16, bold=True, color="#ffffff", align="c", valign="m"))
    s.add(Text(L + 0.8, yy - 0.04, 7.0, 0.36, hd, size=13, bold=True, color=NAVY))
    s.add(Text(L + 0.8, yy + 0.32, 7.0, 0.62, body, size=11, color=INK))
panel(s, L + 8.2, 1.75, CW - 8.2, 4.9, "Quarterly measures and next steps", [
    {"t": "**Promotional share of sales**: 29% → 25%", "bullet": True},
    {"t": "**Shrink, % of sales**: 2.6% → 2.3%, by store", "bullet": True, "before": 4},
    {"t": "**Net cost per delivered order**: $10.70 → ~$7.40", "bullet": True, "before": 4},
    {"t": "**Labor hours per $1,000 of sales**, by quartile", "bullet": True, "before": 4},
    {"t": "Next steps", "bold": True, "color": NAVY, "before": 14},
    {"t": "Brief the lender on the FY2026 outlook and plan.", "bullet": True, "before": 4},
    {"t": "CFO to cost the remaining one-time items.", "bullet": True, "before": 4},
    {"t": "Bring store-by-store exit cases and the delivery contract outcome to the next board meeting.", "bullet": True, "before": 4},
], size=11)

# ------------------------------------------------------------------ 15. Appendix: calculations
s = new("Appendix A: how the numbers were built",
        "Key calculations and assumptions behind the plan",
        SRC + ". All lever values are run-rate annual effects on operating income.")
hdr = ["Item", "Calculation", "Result"]
rows = [
    ["Gross margin bridge", "Promo share +5.0 pts × −14 pts; private label +1.5 pts × +12 pts; shrink +0.5 pts", "−0.70 / +0.18 / −0.50 = −1.02 pts"],
    ["Labor rate effects", "Wage $16.80 → $18.38 (+9.4%) at 7.02 hrs; hours 7.02 → 6.60 (−6.0%) at the new wage", "+1.1 / −0.8 pts"],
    ["E-commerce FY2025", "1,331k orders × $7.40 picking + 772k delivered × ($13.80 − $3.10); new contribution $127.8M × 30% × 20%", "$18.1M cost vs $7.7M → −$10.4M"],
    ["Delivery pricing", "Delivered −9%, collect +14%, fee $6.40 → cost $15.1M; minus ≤$0.5M on the 2% of sales lost", "+$3.0M − $0.5M = +$2.5M"],
    ["Store exits", "$3.1M losses removed + 25% × $118M × 12%; split 6/9 and 3/9", "$6.6M ($4.4M + $2.2M)"],
    ["FY2028 sales base", "$1,503M − $118M + $29.5M recaptured", "$1,415M"],
    ["Promotions / private label / shrink", "−4 pts × 14 pts; +1.5 pts × 12 pts; −0.3 pts; each on $1,415M", "+$7.9M / +$2.5M / +$4.2M"],
    ["Labor and wage rise", "Store labor scaled to $171M; 4% of hours saved; +4% wage on all store labor", "+$6.8M / −$6.8M"],
    ["Draft plan FY2028", "$15.3M + $14.5M − $7.3M wage rise, on $1,503M sales", "$22.5M, 1.5%"],
]
table(s, L, 1.62, [2.6, 6.8, 2.83], rows, header=hdr, row_h=0.5, size=10, col_align=["l", "l", "l"])

# ------------------------------------------------------------------ 16. Appendix: caveats
s = new("Appendix B: data limits and choices made",
        "Where the pack is thin, we chose cautious assumptions; these are the ones that matter most",
        SRC + ".")
panel(s, L, 1.75, (CW - 0.25) / 2, 4.95, "Limits of the evidence", [
    {"t": "**Shrink and labor:** the quartile pattern is a correlation across stores, not proof that fewer hours cause shrink.", "bullet": True},
    {"t": "**Cannibalisation:** the 70% figure is what customers say in a survey (n = 2,300). The conclusion holds unless over 70% of online sales are new.", "bullet": True, "before": 6},
    {"t": "**Fee test:** 4 stores over 10 weeks; chain-wide response may differ.", "bullet": True, "before": 6},
    {"t": "**Promotions:** the valuation assumes promotional sales move to regular price rather than disappear; we stop at 4 of the ~11 points of share in money-losing events.", "bullet": True, "before": 6},
    {"t": "**Stores:** only combined figures for the nine stores are available; the 6/3 split is pro rata.", "bullet": True, "before": 6},
], size=10.5)
panel(s, L + (CW - 0.25) / 2 + 0.25, 1.75, (CW - 0.25) / 2, 4.95, "Choices made", [
    {"t": "**No market growth** in the FY2028 sales base; margin gains come only from the actions.", "bullet": True},
    {"t": "**Full wage pass-through:** the 2027 rise is applied to all store labor, though not every employee is on the minimum wage. Partial pass-through would be upside.", "bullet": True, "before": 6},
    {"t": "**Vendor funding** recovery (46% back towards 55%) is not counted.", "bullet": True, "before": 6},
    {"t": "**Timing:** the pack treats FY2026 as the first plan year. If FY2026 is largely booked by the time of the meeting, the covenant view on page 12 should be replaced with the actual result before it goes to the lender.", "bullet": True, "before": 6},
], size=10.5)

# ------------------------------------------------------------------ output
if __name__ == "__main__":
    out_dir = sys.argv[1]
    prev_dir = sys.argv[2]
    os.makedirs(prev_dir, exist_ok=True)
    allw = []
    for i, sl in enumerate(slides, 1):
        w = render_png(sl, os.path.join(prev_dir, f"s{i:02d}.png"))
        for x in w:
            allw.append(f"slide {i}: {x}")
    print("\n".join(allw) or "no overflow warnings")
    render_pptx(slides, os.path.join(out_dir, "Harlow_margin_plan_board_Feb2027.pptx"))
    print("saved", len(slides), "slides")
