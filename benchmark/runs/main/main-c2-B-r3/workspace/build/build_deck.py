import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from engine import Slide, to_pptx, to_png, WARNINGS, W, H
from components import *

SRC = "Source: Harlow Fresh Markets board briefing pack (synthetic data); team analysis."
slides, notes = [], []


def add(s, note=""):
    slides.append(s); notes.append(note)


# ---------------------------------------------------------------- 1. Title
s = Slide()
s.rect(0, 0, W, H, fill=NAVY)
s.rect(0.7, 2.2, 0.08, 2.2, fill=BLUE)
s.text(0.95, 2.1, 11.5, 1.5, "Reversing Harlow's margin decline: fix gross margin and delivery economics, not headcount",
       size=30, bold=True, color="FFFFFF")
s.text(0.95, 3.7, 11.0, 0.8, "Diagnosis, recommended margin plan and first moves to reach a 3.0% operating margin by FY2028",
       size=16, color="D6E2F0")
s.text(0.95, 5.3, 11.0, 0.9, "Board meeting, February 2027\nPrepared for Dana Whitfield, Chief Executive Officer",
       size=13, color="FFFFFF", space=6)
s.text(0.95, 6.6, 11.5, 0.5, "Based only on the board briefing pack (synthetic benchmark data). All figures $ millions unless stated; fiscal years end in January.",
       size=9, color="AFC3DA")
add(s)

# ---------------------------------------------------------------- 2. Executive summary
s = base("Executive summary: margin fell because of promotions, shrink and home delivery — a margin-first plan, started now, gets back to 3.0%",
         None, SRC, 2)
s.rect(0.5, 1.6, W - 1.0, 0.72, fill=NAVY)
s.text(0.7, 1.6, W - 1.4, 0.72,
       "Fix gross margin and delivery economics, not headcount: seven firm levers lift operating margin from 1.0% to ~2.6% by FY2028, "
       "and a second wave prepared now closes the gap to the 3.0% target.", size=13, bold=True, color="FFFFFF", valign="m")
rows = [
    ("1", "Diagnosis",
     "Promotions, shrink and home delivery drove the decline; wages explain only 13% of the 2.35-point fall",
     "- Gross margin (−1.02 pts: more promotion and shrink) and e-commerce fulfilment (−0.84 pts) explain 79%; productivity offset two-thirds of the wage rise\n"
     "- Fully costed, e-commerce loses ~$10M a year, not the +6.1% margin reported: a home-delivered order loses ~$12, a click-and-collect order ~$2"),
    ("2", "Options",
     "The draft 8% labour cut and e-commerce freeze would leave FY2028 margin near 1.1%, far short of 3.0%",
     "- The cut saves $14.5M on paper, but the leanest stores already run 3.1% shrink vs 2.3%: we expect $4–8M of it back as shrink, before any lost sales"),
    ("3", "Plan",
     "Seven firm levers worth ~$30M (range $17–38M) reach ~2.6%; about half of a ~$10M second wave closes the gap",
     "- Gross margin $16.9M (promotions, vendor funding, private label, shrink) · targeted labour $5.5M · delivery repricing $3.3M · exit 6 lease-expiry stores $4.4M\n"
     "- Wave 2: exit the other 3 loss-making stores (board vote), cost-recovery delivery pricing, vendor funding back to FY2023's 55%"),
    ("4", "First moves",
     "Four no-regret moves in the next 90 days lift FY2026 operating income to ~$25M, ~$5M above the $20M covenant",
     "- Promotion reset with vendor-funding terms · roll-out of the tested delivery pricing · targeted labour rebalancing · notice on 6 lease-expiry stores; one-time cost ~$17M vs $25M cap"),
    ("5", "Risks & asks",
     "Key risks are ValuMart traffic and vendor push-back; we ask for three decisions today",
     "- Endorse the plan in place of the 8% cut · approve delivery repricing · prepare the 3-store vote. If wave 2 falls short, click-and-collect-only reaches ~3.0% but needs the owners' consent"),
]
y = 2.45
for num, sec, head, body in rows:
    s.rect(0.5, y + 0.05, 0.36, 0.36, fill=BLUE, shape="oval")
    s.text(0.5, y + 0.05, 0.36, 0.36, num, size=12, bold=True, color="FFFFFF", align="c", valign="m")
    s.text(0.95, y + 0.07, 1.4, 0.32, sec.upper(), size=9, bold=True, color=BLUE)
    s.text(2.35, y, 10.5, 0.32, head, size=11.5, bold=True, color=NAVY)
    s.text(2.35, y + 0.31, 10.5, 0.55, body, size=9.5, color=INK, space=2)
    y += 0.88
    s.line(0.5, y - 0.04, W - 0.5, y - 0.04, color=RULE, lw=0.5)
add(s)

# ---------------------------------------------------------------- 3. The gap to close
s = base("Reaching 3.0% by FY2028 means adding ~$35M of operating income — more than double FY2025's $15.3M",
         None, SRC + " Target base: 3.0% of pro-forma sales of $1,444M after exiting 6 stores (see p.14).", 3)
subhead(s, 0.5, 1.6, 7.0, "Operating income, $M: FY2025 actual to FY2028 target")
waterfall(s, 0.6, 2.25, 6.8, 4.45,
          [("FY2025 actual", 15.3, "total"), ("2027 minimum-wage step (+4%)", -7.3, "delta"),
           ("Delivery rate rise (+3%)", -0.3, "delta"), ("FY2028 if nothing changes", 7.7, "total"),
           ("Gap to close", 35.6, "delta"), ("FY2028 target (3.0%)", 43.3, "total")],
          vmax=48, dec=1, label_h=0.62, colors={4: "9DB9DC", 5: NAVY})
s.text(0.6, 6.66, 6.8, 0.25, "Operating margin: FY2025 1.02% · FY2028 with no action ~0.5% · target 3.0%", size=9, color=INK2)
subhead(s, 7.9, 1.6, 4.93, "What the plan must satisfy (from the board brief)")
cons = [("Margin", "Operating margin ≥ 3.0% by FY2028"),
        ("Capital", "≤ $25M one-time cost or capital, FY2026–FY2028"),
        ("Lender", "Operating income ≥ $20M in FY2026 (covenant)"),
        ("Stores", "No closure of a store with a lease beyond 2027 without a board vote"),
        ("Delivery", "Keep the delivery service in some form (owners)")]
y = 2.05
for k, v in cons:
    s.text(7.9, y, 1.0, 0.4, k, size=10, bold=True, color=BLUE)
    s.text(8.9, y, 3.93, 0.45, v, size=10, color=INK)
    y += 0.47
callout(s, 7.9, 4.5, 4.93, 2.2, "Baseline assumptions (do-nothing case)",
        "- FY2025 cost ratios and sales scale held constant (no further erosion assumed — optimistic)\n"
        "- 2027 minimum-wage rise applied to the whole $181.9M labour bill (conservative)\n"
        "- Third-party delivery provider's proposed +3% accepted\n"
        "- If FY2024–25 erosion continued, FY2026 would already be below the covenant",
        size=9.5)
add(s)

# ---------------------------------------------------------------- 4. Hypotheses
s = base("We tested a margin-first hypothesis against seven conditions: the diagnosis held, but the first answer was not enough to reach 3.0%",
         None, SRC, 4)
s.rect(0.5, 1.6, W - 1.0, 0.5, fill=PALE)
s.text(0.65, 1.6, W - 1.3, 0.5, "**Starting hypothesis:** the margin loss is a gross-margin and delivery-economics problem, not a wage problem — resetting promotions and repricing delivery, rather than cutting labour, would restore 3.0%.",
       size=10.5, color=INK, valign="m")
hyp = [
    ["#", "What would have to be true", "Test against the evidence", "Verdict"],
    ["1", "The decline is driven mainly by gross margin and e-commerce, not wages", "Margin bridge FY2023–25: gross margin −1.02 pts and e-commerce fulfilment −0.84 pts = 79% of the fall; store labour −0.30 pts = 13% (p.5)", ""],
    ["2", "Extra promotion is not buying profitable traffic", "38% of FY2025 events lost money; the +5-pt rise in promo share costs $10.5M a year and would need ~$53M of new sales to pay back (p.6–7)", ""],
    ["3", "E-commerce loses money once fully costed", "With third-party delivery and 70% cannibalisation: −$10.4M in FY2025; −$12.34 per delivered order, −$1.64 per click-and-collect order (p.9)", ""],
    ["4", "Delivery can be repriced without losing the customer base", "Fee test: delivered orders −9%, click-and-collect +14%, e-commerce sales only −2%; worth ~$2.5M a year — but only a quarter of the loss (p.13)", ""],
    ["5", "Store hours can be cut 8% without raising shrink or hurting service (management view)", "Leanest-labour quartile runs 3.1% shrink vs 2.3% in the richest; shrink rose 0.5 pts as hours per $1,000 of sales fell 6% (p.8)", ""],
    ["6", "Weak stores can be exited within the board's commitments", "6 of the 9 negative-EBITDA stores have leases ending by 2027, so no vote is needed; exit adds ~$4.4M a year (p.14)", ""],
    ["7", "The levers in the starting hypothesis are enough for 3.0% within $25M", "Promotions + delivery give ~$13M; even all seven firm levers give ~$30M → ~2.6%; ~$5M more must come from a second wave (p.15)", ""],
]
yb = table(s, 0.5, 2.2, [0.4, 3.75, 6.5, 1.68], hyp, 0.52, size=9.5, header_h=0.34, aligns=["c", "l", "l", "l"])
vk = ["Supported", "Supported", "Supported", "Partly", "Not supported", "Supported", "Not supported"]
for i, k in enumerate(vk):
    verdict(s, 0.5 + 0.4 + 3.75 + 6.5 + 0.08, 2.2 + 0.34 + i * 0.52 + 0.12, k)
s.rect(0.5, 6.32, W - 1.0, 0.55, fill=PALE_BLUE)
s.rect(0.5, 6.32, 0.06, 0.55, fill=BLUE)
s.text(0.65, 6.32, W - 1.3, 0.55, "**Revised answer:** the diagnosis holds, but promotions and delivery alone are not enough — the plan adds shrink, targeted labour and store exits, and needs a prepared second wave to reach 3.0%.",
       size=10.5, color=INK, valign="m")
add(s)

# ---------------------------------------------------------------- 5. Margin bridge
s = base("Gross margin and e-commerce fulfilment explain ~80% of the 2.35-point margin decline; store labour explains only 13%",
         "Diagnosis", SRC + " Table 1. Change in each line as % of sales, FY2023 to FY2025; figures may not sum due to rounding.", 5)
subhead(s, 0.5, 1.6, 7.2, "Operating margin, % of sales, FY2023 → FY2025")
waterfall(s, 0.6, 2.2, 7.0, 4.5,
          [("FY2023", 3.37, "total"), ("Gross margin", -1.02, "delta"), ("E-commerce fulfilment", -0.84, "delta"),
           ("Store labour", -0.30, "delta"), ("Occupancy & energy", -0.20, "delta"), ("Other SG&A", 0.0, "delta"),
           ("FY2025", 1.02, "total")], vmax=3.8, dec=2, unit="%", label_h=0.55, delta_unit=" pts")
subhead(s, 8.1, 1.6, 4.73, "Each line's contribution to the decline")
rows = [["Line", "pts of sales", "$M*", "Share"],
        ["Gross margin", "−1.02", "−15.3", "43%"],
        ["E-commerce fulfilment", "−0.84", "−12.6", "36%"],
        ["Store labour", "−0.30", "−4.5", "13%"],
        ["Occupancy & energy", "−0.20", "−3.0", "8%"],
        ["Other SG&A", "0.00", "0.0", "0%"],
        ["Total", "−2.35", "−35.4", "100%"]]
table(s, 8.1, 2.05, [1.95, 1.0, 0.85, 0.93], rows, 0.33, size=10, header_h=0.32, aligns=["l", "r", "r", "r"],
      bolds={(5, -1)})
s.text(8.1, 4.4, 4.73, 0.25, "* Change in ratio × FY2025 sales of $1,503M", size=8, color=MUTED)
callout(s, 8.1, 4.75, 4.73, 1.95, "Why the dollar view misleads",
        "- Labour had the largest dollar rise (+$14.3M), but sales grew 5.8%\n"
        "- At FY2023's 11.8% ratio, FY2025 labour would have cost $177.4M — so only $4.5M is excess\n"
        "- E-commerce fulfilment more than tripled: $5.2M → $18.1M", size=9.5)
add(s)

# ---------------------------------------------------------------- 6. Gross margin decomposition
s = base("The 1.0-point gross-margin loss is fully explained by more promotion and more shrink; private label offset less than a fifth of it",
         "Diagnosis", SRC + " Tables 1–2. Mix effects use the stated margin gaps (promo −14 pts; private label +12 pts), unchanged over the period.", 6)
subhead(s, 0.5, 1.6, 6.4, "Gross margin, % of sales, FY2023 → FY2025 (axis starts at 24%)")
waterfall(s, 0.6, 2.2, 6.2, 4.5,
          [("FY2023", 26.04, "total"), ("More promotional sales", -0.70, "delta"), ("Higher shrink", -0.50, "delta"),
           ("More private label", 0.18, "delta"), ("FY2025", 25.02, "total")], vmax=26.4, vmin=24.0, dec=2, unit="%", label_h=0.55, delta_unit=" pts")
subhead(s, 7.3, 1.6, 5.53, "How each driver is calculated")
rows = [["Driver", "Calculation", "pts", "$M"],
        ["Promotion mix", "Promo share 24.0% → 29.0% (+5.0 pts) × −14 pts margin gap", "−0.70", "−10.5"],
        ["Shrink", "2.1% → 2.6% of sales (+0.5 pts)", "−0.50", "−7.5"],
        ["Private label", "Share 17.0% → 18.5% (+1.5 pts) × +12 pts margin gap", "+0.18", "+2.7"],
        ["Total explained", "", "−1.02", "−15.3"],
        ["Actual change", "26.04% → 25.02%", "−1.02", "−15.3"]]
table(s, 7.3, 2.05, [1.35, 2.95, 0.6, 0.63], rows, [0.55, 0.42, 0.55, 0.36, 0.36], size=9.5, header_h=0.32,
      aligns=["l", "l", "r", "r"], bolds={(3, -1), (4, -1)})
callout(s, 7.3, 4.85, 5.53, 1.85, "Harlow is also funding more of each promotion itself",
        "- Vendor funding covered 55% of markdowns in FY2023 but only 46% in FY2025\n"
        "- Shrink is now 2.6% of sales ($39.1M): produce waste 45%, theft 35%, admin and receiving errors 20%",
        size=9.5)
add(s)

# ---------------------------------------------------------------- 7. Promotions
s = base("Deeper promotion has not paid for itself: 38% of events lose money, and the extra promo share would need ~$53M of new sales to break even",
         "Diagnosis", SRC + " §5, §9–10. Contribution of 20¢ per new sales dollar is finance's estimate (§7) and flatters promotional sales.", 7)
colw = 3.95
xs = [0.5, 0.5 + colw + 0.24, 0.5 + 2 * (colw + 0.24)]
subhead(s, xs[0], 1.6, colw, "The promotion economics")
stat(s, xs[0], 2.05, colw, "38%", "of FY2025 promotional events lost money even after counting the extra units they sold")
stat(s, xs[0], 3.3, colw, "55% → 46%", "share of markdowns funded by vendors, FY2023 → FY2025")
stat(s, xs[0], 4.55, colw, "~$53M", "of new sales needed (at 20¢ contribution) to repay the $10.5M a year that +5 pts of promo share costs (0.70 pts × $1,503M ÷ 0.20)")
subhead(s, xs[1], 1.6, colw, "Testing the claim that “promotions work”")
s.text(xs[1], 2.05, colw, 3.0,
       "~ Category team: the deepest-promo stores grew comps **+1.8%** vs **+0.2%** for the rest.\n"
       "- **Benefit:** +1.6 pts of sales × 20¢ = **0.32 pts** of sales in contribution\n"
       "- **Cost:** every extra point of promo share costs **0.14 pts** of sales in margin\n"
       "- **Break-even:** those stores can carry at most 0.32 ÷ 0.14 = **2.3 pts** more promo share\n"
       "- The chain added **5 pts**; at that depth the comp gain repays less than half its cost (0.32 vs 0.70 pts)\n"
       "- And it is correlation: stores were not chosen at random",
       size=10, color=INK, bullet=True, space=5)
subhead(s, xs[2], 1.6, colw, "What this means against ValuMart")
s.text(xs[2], 2.05, colw, 3.0,
       "- ValuMart has opened 11 stores in Harlow trade areas; nearby Harlow stores ran comps of **−4.2%** vs **+1.1%**\n"
       "- Despite more promotion, “more expensive” perception rose from **33% to 41%**\n"
       "- Customers choose Harlow for **fresh produce (58%)** and **convenience (44%)**, not price\n"
       "- Broad promotional depth is an expensive and weak defence; private label (+12 pts margin) and fresh are better ones",
       size=10, color=INK, bullet=True, space=5)
s.rect(0.5, 5.85, W - 1.0, 0.85, fill=PALE_BLUE)
s.rect(0.5, 5.85, 0.06, 0.85, fill=BLUE)
s.text(0.65, 5.85, W - 1.3, 0.85,
       "**Implication:** cut the loss-making events chain-wide, require vendor funding as a condition of each event, keep targeted depth only "
       "in ValuMart-exposed stores while their traffic is measured, and move the value message to private label. Open question: how much "
       "promotion is truly needed to hold traffic — so the reset is staged and tracked.", size=10, color=INK, valign="m")
add(s)

# ---------------------------------------------------------------- 8. Labour
s = base("Productivity absorbed two-thirds of the 9.4% wage rise — and the hours already taken out are showing up as shrink",
         "Diagnosis", SRC + " Tables 3–4. Labour % = hours per $1,000 × hourly wage; computed values (11.79%, 12.13%) differ from Table 3 only by rounding.", 8)
subhead(s, 0.5, 1.6, 6.0, "Store labour, % of sales, FY2023 → FY2025 (axis starts at 10%)")
waterfall(s, 0.6, 2.2, 5.8, 3.4,
          [("FY2023", 11.79, "total"), ("Wage +9.4% ($16.80 → $18.38)", 1.11, "delta"),
           ("Hours per $1,000 −6.0% (7.02 → 6.60)", -0.77, "delta"), ("FY2025", 12.13, "total")],
          vmax=13.3, vmin=10.0, dec=2, unit="%", label_h=0.62, colors={1: ORANGE, 2: BLUE}, delta_unit=" pts")
s.text(0.6, 5.65, 5.8, 0.5, "Wage inflation alone would have added 1.11 pts; productivity took back 0.77 pts. Total hours fell slightly (9.97M → 9.92M) while sales rose 5.8%.",
       size=9.5, color=INK2)
subhead(s, 6.9, 1.6, 5.93, "Shrink by store labour intensity, FY2025, % of sales")
# simple bar chart
qs = [("Q1\nfewest hours", 3.1), ("Q2", 2.7), ("Q3", 2.4), ("Q4\nmost hours", 2.3)]
cx0, cy0, ch, cw = 7.0, 2.25, 3.0, 4.55
vmaxq = 3.5
slot = cw / 4
for i, (lab, v) in enumerate(qs):
    bh = ch * v / vmaxq
    bx = cx0 + i * slot + slot * 0.2
    s.rect(bx, cy0 + ch - bh, slot * 0.6, bh, fill=ORANGE if i == 0 else SLATE)
    s.text(bx, cy0 + ch - bh + 0.05, slot * 0.6, 0.26, f"{v:.1f}%", size=10.5, bold=True, color="FFFFFF", align="c")
    s.text(cx0 + i * slot, cy0 + ch + 0.05, slot, 0.45, lab, size=9, color=INK2, align="c")
ya = cy0 + ch - ch * 2.6 / vmaxq
s.line(cx0, ya, cx0 + cw, ya, color=MUTED, lw=1, dash=True)
s.text(cx0 + cw + 0.08, ya - 0.2, 1.2, 0.4, "Chain average 2.6%", size=8.5, color=INK2)
s.line(cx0, cy0 + ch, cx0 + cw, cy0 + ch, color=MUTED)
s.text(6.9, 5.75, 5.93, 0.45, "Q1→Q2: 0.4 pts less shrink. Q3→Q4: only 0.1 pt. Extra hours matter most where hours are thinnest.",
       size=9.5, bold=True, color=INK)
s.rect(0.5, 6.2, W - 1.0, 0.65, fill=PALE_BLUE)
s.rect(0.5, 6.2, 0.06, 0.65, fill=BLUE)
s.text(0.65, 6.2, W - 1.3, 0.65,
       "**Implication:** rebalance hours instead of cutting them across the board. Managers in the leanest stores say produce rotation and receiving checks are skipped on busy days; "
       "waste and receiving errors are 65% of shrink, so these hours protect margin.", size=10, color=INK, valign="m")
add(s)

# ---------------------------------------------------------------- 9. E-commerce
s = base("Fully costed, e-commerce loses ~$10M a year — almost all of it in home delivery, which loses ~$12 on every order",
         "Diagnosis", SRC + " Tables 1, 5; §7, §10. Incremental contribution = $96 basket × 30% new to Harlow (survey) × 20¢ (finance). Costs reconcile to Table 1 (appendix p.22).", 9)
subhead(s, 0.5, 1.6, 6.1, "Economics per order, FY2025, $")
rows = [["$ per order", "Click-and-collect", "Home delivery"],
        ["Incremental contribution", "+5.76", "+5.76"],
        ["Picking", "−7.40", "−7.40"],
        ["Third-party delivery", "—", "−13.80"],
        ["Delivery fee collected", "—", "+3.10"],
        ["Net per order", "−1.64", "−12.34"],
        ["Orders, FY2025 (thousands)", "559", "772"],
        ["Annual result, $M", "−0.9", "−9.5"]]
table(s, 0.5, 2.05, [2.5, 1.8, 1.8], rows, 0.37, size=10.5, header_h=0.36, aligns=["l", "r", "r"],
      bolds={(4, -1), (6, -1)}, colors={(4, 2): RED, (6, 2): RED, (4, 1): RED, (6, 1): RED}, fills={4: PALE, 6: PALE})
s.text(0.5, 5.1, 6.1, 0.85,
       "- **Break-even:** delivery needs **94%** of its sales to be new to Harlow; click-and-collect needs 39% (survey: 30%)\n"
       "- Delivered share of orders rose 45% → 58%, while fees fell from 26% to 22% of delivery cost",
       size=9.5, color=INK, bullet=True, space=3)
subhead(s, 7.0, 1.6, 5.83, "Reconciling the e-commerce team's +6.1%, % of e-commerce sales")
waterfall(s, 7.1, 2.2, 5.6, 3.6,
          [("E-commerce team view", 6.1, "total"), ("Add third-party delivery, net of fees", -6.5, "delta"),
           ("Count only the 30% of sales new to Harlow", -7.8, "delta"), ("Fully costed (finance view)", -8.2, "total")],
          vmax=7.5, vmin=-10.0, dec=1, unit="%", label_h=0.7, colors={0: SLATE, 3: RED}, delta_unit=" pts")
s.text(7.0, 5.85, 5.83, 0.35, "Step 2 switches to finance's incremental method; the two methods are not fully comparable.",
       size=8.5, color=MUTED)
s.rect(0.5, 6.2, W - 1.0, 0.65, fill=PALE_BLUE)
s.rect(0.5, 6.2, 0.06, 0.65, fill=BLUE)
s.text(0.65, 6.2, W - 1.3, 0.65,
       "**Implication:** the problem is subsidised home delivery, not e-commerce as such. Freezing the service locks in the loss; repricing delivery and steering customers to click-and-collect attack it directly.",
       size=10, color=INK, valign="m")
add(s)

# ---------------------------------------------------------------- 10. Management plan
s = base("Management's draft plan would leave FY2028 margin near 1.1%: shrink claws back much of the labour saving, and the freeze locks in the e-commerce loss",
         "Options", SRC + " §4, §6. Shrink effect: +0.25 to +0.50 pts of sales (midpoint shown), moving the average store halfway to fully onto the leanest quartile's 3.1%.", 10)
subhead(s, 0.5, 1.6, 6.9, "Operating income under the draft plan, $M, FY2025 → FY2028")
waterfall(s, 0.6, 2.2, 6.7, 4.45,
          [("FY2025 actual", 15.3, "total"), ("2027 wage step", -7.3, "delta"), ("Delivery rate +3%", -0.3, "delta"),
           ("8% store-hours cut", 14.5, "delta"), ("Added shrink (midpoint)", -5.6, "delta"),
           ("FY2028 draft plan", 16.6, "total")],
          vmax=50, dec=1, label_h=0.55, target=45.1, target_label="3.0% target ≈ $45M", target_pos="left")
s.text(0.6, 6.62, 6.7, 0.28, "FY2028 margin ~1.1% before any sales lost to longer queues or empty shelves (each 1% of sales ≈ −$3.0M).",
       size=9, color=INK2)
subhead(s, 7.8, 1.6, 5.03, "Why the risks are bigger than the plan assumes")
s.text(7.8, 2.05, 5.03, 4.6,
       "- **Shrink:** the leanest-labour stores already run 3.1% shrink vs 2.6% on average; an 8% cut moves every store toward them. +0.25–0.50 pts of shrink = **$3.8–7.5M**\n"
       "- **Fresh and service:** 58% of customers shop Harlow for fresh produce, and managers already skip rotation on busy days; every 1% of sales lost costs ~**$3.0M**\n"
       "- **Freeze:** stops the e-commerce loss growing but keeps the **−$10.4M** a year\n"
       "- **Blind spot:** nothing in the plan addresses promotions — the largest single cause (−$10.5M)\n"
       "- **Covenant:** the cut helps FY2026 on paper, but shrink and service effects arrive with a lag",
       size=10.5, color=INK, bullet=True, space=7)
add(s)

# ---------------------------------------------------------------- 11. Alternatives
s = base("Of three options, only the margin-first plan reaches 3.0% while keeping home delivery and the owners' commitments",
         "Options", SRC + " Option C assumes 40% of home-delivery customers switch to click-and-collect; one-time costs from p.17.", 11)
rows = [["", "A. Management draft", "B. Margin-first plan (recommended)", "C. Margin-first, click-and-collect only"],
        ["What it does", "Cut store hours 8%; freeze e-commerce at current size",
         "Promotion reset, vendor funding, private label, shrink; targeted labour; delivery repricing; exit 6 stores; second wave ready",
         "As B, but close home delivery and keep click-and-collect"],
        ["FY2028 operating margin", "~1.1% ($16.6M)", "~2.6% on firm levers ($37.8M); ~3.4% with the full second wave", "~3.0% on firm levers ($42.9M)"],
        ["One-time cost (cap $25M)", "Small (not specified)", "~$17M", "~$17M"],
        ["FY2026 covenant (≥ $20M)", "Met on paper if the cut lands early", "~$25M: ~$5M headroom", "~$25M"],
        ["Owners' and board commitments", "Kept", "Kept; exiting the 3 other stores needs a board vote", "Breaks “keep delivery” commitment"],
        ["Main risks", "Shrink, service, fresh reputation; promotions untouched",
         "Traffic response to fewer promotions (ValuMart); vendor push-back", "Customer backlash; weaker convenience position (44% shop for it)"],
        ["Verdict", "Reject", "Recommend", "Hold as fallback if second-wave delivery pricing fails"]]
table(s, 0.5, 1.65, [2.3, 3.0, 3.75, 3.28], rows, [0.75, 0.6, 0.45, 0.45, 0.6, 0.65, 0.55], size=10, header_h=0.45,
      bold_first_col=True, fills={6: PALE},
      colors={(6, 1): RED, (6, 2): GREEN, (6, 3): AMBER, (1, 1): RED, (1, 2): GREEN, (4, 3): RED})
s.rect(0.5 + 2.3 + 3.0, 1.65, 3.75, 4.5, fill=None, line=BLUE, lw=2)
s.text(0.5, 6.35, W - 1.0, 0.5, "Also rejected: matching ValuMart with deeper promotions — every extra point of promo share costs ~$2.1M of margin and has not repaired price perception (p.7).",
       size=10, color=INK2)
add(s)

# ---------------------------------------------------------------- 12. Lever table
s = base("Seven firm levers across the four areas where margin leaks are worth ~$30M a year by FY2028 (range $17–38M)",
         "Plan", SRC + " Values at FY2028 run-rate on pro-forma sales of $1,444M; ranges in appendix p.23. Labour bill includes the 2027 wage step.", 12)
rows = [["Area", "Lever", "How it is sized", "Base $M", "Range $M", "Evidence", "Start"],
        ["Gross margin", "1. Promotion reset: drop loss-making events, promo share 29% → 25%", "4 pts × 14 pts × $1,444M = $8.1M, less 25% for lost volume", "6.1", "3.0–7.6", "Strong: event review", "Now"],
        ["", "2. Vendor funding of markdowns 46% → 50%", "Implied markdown 25.9 pts; gap 14.0 → 13.0 pts on $361M of promo sales", "3.7", "1.9–3.7", "Medium: FY2023 level", "Now"],
        ["", "3. Private label share 18.5% → 21%", "2.5 pts × 12 pts × $1,444M", "4.3", "2.6–6.1", "Medium: +0.75 pts/yr trend", "FY2027"],
        ["", "4. Shrink 2.6% → 2.3%, hours reinvested in lean stores", "0.3 pts × $1,444M = $4.3M, less $1.5M of added hours", "2.8", "0.7–4.3", "Medium: quartile pattern", "FY2027"],
        ["Store labour", "5. Targeted rebalancing: −3% hours in high-labour stores", "3% × $174.8M × 1.04 (2027 wage)", "5.5", "3.6–7.3", "Medium: Q3≈Q4 shrink", "Now"],
        ["E-commerce", "6. Roll out tested delivery pricing; renew contract at −5%", "Fee test: $3.0M saved − $0.5M lost sales; contract $0.8M", "3.3", "2.0–4.0", "Strong: 10-week test", "Now"],
        ["Store portfolio", "7. Exit 6 negative-EBITDA stores at lease expiry", "$2.1M losses removed + 25% of $78.7M sales × 12%", "4.4", "3.0–5.0", "Strong: past closures", "Now"],
        ["Total firm levers", "", "", "30.1", "16.8–38.0", "", ""]]
table(s, 0.5, 1.6, [1.3, 3.35, 3.65, 0.75, 0.95, 1.45, 0.88], rows, [0.5] * 7 + [0.38], size=9.5, header_h=0.36,
      aligns=["l", "l", "l", "r", "r", "l", "l"], bolds={(7, -1)}, fills={7: PALE}, colors={(i, 0): BLUE for i in range(7)})
s.text(0.5, 5.95, W - 1.0, 0.9,
       "- **Not levers:** other SG&A held flat at 4.7% of sales throughout (not a cause); occupancy and energy rose 0.2 pts and is partly addressed by the store exits\n"
       "- Levers 1–2 interact: vendor funding is sized on the smaller, post-reset promotion base, so the two are not double-counted",
       size=9.5, color=INK2, bullet=True, space=3)
add(s)

# ---------------------------------------------------------------- 13. Delivery repricing
s = base("Rolling out the tested delivery pricing adds ~$2.5M a year and keeps the service; a cost-recovery step is the next test",
         "Plan", SRC + " Table 5, §7. Fee-test changes applied to the FY2025 base; lost e-commerce sales conservatively treated as lost to Harlow at 20¢ contribution.", 13)
subhead(s, 0.5, 1.6, 7.0, "Fee test ($7.99 fee, $100 free threshold) applied to FY2025")
rows = [["", "FY2025", "Tested pricing", "Change"],
        ["Delivered orders, thousands", "772", "703", "−9%"],
        ["Click-and-collect orders, thousands", "559", "637", "+14%"],
        ["E-commerce sales, $M", "127.8", "125.2", "−2%"],
        ["Fee collected per delivered order", "$3.10", "$6.40", "+$3.30"],
        ["Picking cost, $M", "9.8", "9.9", "+0.1"],
        ["Third-party delivery cost, $M", "10.7", "9.7", "−1.0"],
        ["Delivery fees collected, $M", "−2.4", "−4.5", "−2.1"],
        ["Net fulfilment cost, $M", "18.1", "15.1", "−3.0"],
        ["Contribution lost on lost sales, $M", "", "", "−0.5"],
        ["Net gain, $M a year", "", "", "+2.5"]]
table(s, 0.5, 2.05, [3.1, 1.2, 1.5, 1.2], rows, 0.38, size=10, header_h=0.34, aligns=["l", "r", "r", "r"],
      bolds={(7, -1), (9, -1)}, fills={9: PALE_BLUE})
callout(s, 7.9, 1.6, 4.93, 1.55, "Contract renewal (2026): +$0.8M",
        "- Refuse the proposed +3% (worth $0.3M)\n- Target a 5% reduction on the smaller volume ($0.5M)", size=9.5)
callout(s, 7.9, 3.3, 4.93, 1.75, "Still loss-making after repricing",
        "- Each delivered order still loses ~$9.04 ($5.76 − $7.40 − $13.80 + $6.40)\n"
        "- That is ~$6.4M a year: repricing fixes only a quarter of the e-commerce loss", size=9.5, fill=PALE, bar=ORANGE)
callout(s, 7.9, 5.2, 4.93, 1.6, "Next test (wave 2): ~$3M",
        "- Pilot cost-recovery pricing or a paid delivery membership\n"
        "- Halving the remaining delivery loss is worth ~$3.2M; grow click-and-collect, not subsidised delivery", size=9.5)
add(s)

# ---------------------------------------------------------------- 14. Store exits
s = base("Exiting the six loss-making stores whose leases end by 2027 adds ~$4.4M a year without a board vote; the other three repay their exit cost in ~3.4 years",
         "Plan", SRC + " Table 6. The nine stores' sales and EBITDA are split pro rata (6/9, 3/9) because the pack gives only totals; closure allowance is a team assumption.", 14)
rows = [["$M", "6 stores, leases end by 2027", "3 other stores", "All 9"],
        ["Combined sales", "78.7", "39.3", "118.0"],
        ["Four-wall EBITDA (removed on exit)", "−2.1", "−1.0", "−3.1"],
        ["Sales moving to a nearby Harlow store (25%)", "19.7", "9.8", "29.5"],
        ["Contribution on moved sales (12%)", "+2.4", "+1.2", "+3.5"],
        ["Annual operating-income gain", "+4.4", "+2.2", "+6.6"],
        ["One-time cost", "~3.0 (allowance, $0.5M/store)", "7.5 (lease exit)", "~10.5"],
        ["Payback", "< 1 year", "~3.4 years", "~1.6 years"],
        ["Governance", "No board vote needed", "Board vote required", ""]]
table(s, 0.5, 1.65, [3.4, 2.5, 1.85, 1.25], rows, 0.43, size=10, header_h=0.4, aligns=["l", "r", "r", "r"],
      bolds={(4, -1)}, fills={4: PALE_BLUE})
s.text(0.5, 5.55, 9.0, 1.3,
       "- Gain is likely understated: four-wall EBITDA excludes store depreciation, which also goes on exit\n"
       "- Allocated overheads stay, but four-wall EBITDA already excludes them, so the gain is not overstated\n"
       "- Pro-rata split is the main uncertainty: if the 6 carry less of the loss, the gain could be ~$3M (p.18)",
       size=9.5, color=INK2, bullet=True, space=3)
callout(s, 9.85, 1.65, 2.98, 2.75, "Recommendation",
        "- **Now:** confirm store-level P&Ls, then give notice on the 6 lease-expiry stores\n"
        "- **Next 6 months:** test a fix (range, fresh, labour) in the other 3\n"
        "- **Mid-FY2027:** bring the 3 to a board vote if the fix fails — this is part of wave 2 (+$2.2M)",
        size=9.5)
callout(s, 9.85, 4.55, 2.98, 2.25, "Why not exit all nine now?",
        "- The 3 need a board vote and $7.5M, 44% of the plan's one-time budget\n"
        "- A 3.4-year payback is slower than every other lever; a fix test is cheap",
        size=9.5, fill=PALE, bar=SLATE)
add(s)

# ---------------------------------------------------------------- 15. FY2028 bridge
s = base("The firm levers take operating margin to ~2.6% by FY2028; about half of the second wave closes the gap to 3.0%",
         "Plan", SRC + " Margins on pro-forma sales: $1,503M (FY2025), $1,444M (firm plan, 6 stores exited), $1,415M (full plan, 9 exited). 3.0% target = $42–43M.", 15)
subhead(s, 0.5, 1.6, 8.4, "Operating income, $M, FY2025 → FY2028")
Y = waterfall(s, 0.6, 2.2, 8.2, 4.2,
              [("FY2025 actual", 15.3, "total"), ("Wage step & delivery rate", -7.6, "delta"),
               ("FY2028 if nothing changes", 7.7, "total"), ("Gross-margin levers (1–4)", 16.9, "delta"),
               ("Targeted labour (5)", 5.5, "delta"), ("Delivery repricing (6)", 3.3, "delta"),
               ("Exit 6 stores (7)", 4.4, "delta"), ("Firm plan", 37.8, "total"),
               ("Second wave", 9.9, "delta"), ("Full plan", 47.7, "total")],
              vmax=55, dec=1, label_h=0.6, target=43.3, target_label="3.0% target ≈ $42–43M", target_pos="left",
              colors={7: BLUE, 8: "9DB9DC", 9: NAVY}, val_size=9.5, label_size=8.5)
for i, m in [(0, "1.0%"), (2, "0.5%"), (7, "2.6%"), (9, "3.4%")]:
    s.text(0.6 + i * 0.82, 6.4, 0.82, 0.3, m, size=10, bold=True, color=NAVY, align="c")
s.text(0.6, 6.66, 8.2, 0.25, "Operating margin", size=8, color=MUTED, align="l")
subhead(s, 9.25, 1.6, 3.58, "Second wave: ~$10M, ~$5M needed")
rows = [["Option", "$M"], ["Exit the 3 other loss-making stores (board vote; $7.5M)", "2.2"],
        ["Cost-recovery delivery pricing or membership (pilot first)", "3.0"],
        ["Vendor funding from 50% back to FY2023's 55%", "4.7"], ["Total second wave", "9.9"]]
table(s, 9.25, 2.05, [2.9, 0.68], rows, [0.62, 0.62, 0.62, 0.36], size=9.5, header_h=0.32, aligns=["l", "r"], bolds={(3, -1)})
s.text(9.25, 4.75, 3.58, 1.9,
       "- The gap left by the firm plan is $5–6M, so about half the second wave must deliver\n"
       "- Prepare all three now so the choice can be made at the mid-FY2027 checkpoint",
       size=9.5, color=INK, bullet=True, space=4)
add(s)

# ---------------------------------------------------------------- 16. First moves
s = base("Four no-regret moves in the next 90 days lift FY2026 operating income to ~$25M, about $5M above the $20M covenant",
         "First moves", SRC + " FY2026 in-year phasing (team assumption): promotions 50%, vendor funding 25%, delivery 75%, labour 50%, private label ~25% of run-rate; FY2025 scale.", 16)
subhead(s, 0.5, 1.6, 7.3, "Roadmap")
cols = [("NOW: next 90 days", BLUE,
         "- **1. Promotion reset:** drop the loss-making events from the next calendar, worst first; minimum vendor funding per event\n"
         "- **2. Delivery:** roll out $7.99 fee / $100 threshold; renew the contract at no increase\n"
         "- **3. Labour:** replace the 8% cut with targeted rebalancing (−3% hours in high-labour stores; protect receiving and produce rotation)\n"
         "- **4. Stores:** give notice on the 6 lease-expiry stores"),
        ("FY2027", SLATE,
         "- Private-label push toward 21%\n- Shrink programme to 2.3%; pilot in 10 stores first\n- Fix test, then board vote, on the 3 other stores\n- Pilot cost-recovery delivery pricing\n- Press vendor funding toward 55%"),
        ("FY2028", SLATE,
         "- Full run-rate\n- Mid-FY2027 checkpoint: if run-rate margin is below ~2.4%, trigger the second wave in full and put the fallback (C) to the owners")]
xw = [3.1, 2.15, 1.95]
x = 0.5
for (h, col, body), wdt in zip(cols, xw):
    s.rect(x, 2.05, wdt - 0.08, 0.36, fill=col)
    s.text(x + 0.08, 2.05, wdt - 0.2, 0.36, h, size=10, bold=True, color="FFFFFF", valign="m")
    s.text(x, 2.5, wdt - 0.08, 3.6, body, size=9.5, color=INK, bullet=True, space=5)
    x += wdt
s.rect(0.5, 6.15, 7.12, 0.7, fill=PALE)
s.text(0.6, 6.15, 6.95, 0.7, "**Why these four first:** they pay back within the year, rest on the strongest evidence, need no capital or board vote, and can be reversed if traffic suffers.",
       size=9.5, color=INK, valign="m")
subhead(s, 8.1, 1.6, 4.73, "FY2026 operating income, $M (red line: $20M covenant)")
waterfall(s, 8.2, 2.2, 4.55, 3.95,
          [("FY2025 run-rate", 15.3, "total"), ("Promo reset", 3.2, "delta"), ("Vendor funding", 1.0, "delta"),
           ("Delivery pricing", 1.7, "delta"), ("Labour", 2.7, "delta"), ("Private-label trend", 1.0, "delta"),
           ("FY2026", 24.9, "total")], vmax=30, dec=1, label_h=0.6, target=20.0, target_label=None,
          val_size=9, label_size=8, colors={6: BLUE})
s.text(8.1, 6.2, 4.73, 0.65, "Delivery shown net of the half-year contract rise (−$0.2M). Risk: if about a third of FY2025's $18M erosion recurs, the headroom is gone, so track monthly and brief the lender early.",
       size=8.5, color=INK2)
add(s)

# ---------------------------------------------------------------- 17. Capital
s = base("The plan needs ~$17M of one-time cost — inside the $25M cap with ~$8M of contingency",
         "First moves", SRC + " Only the $7.5M lease-exit cost comes from the pack; other items are team planning allowances for the CFO to validate.", 17)
rows = [["One-time cost item", "$M", "Basis", "Wave"],
        ["Lease exit, 3 other weak stores", "7.5", "Briefing pack (Table 6)", "2"],
        ["Closure costs, 6 lease-expiry stores", "3.0", "Allowance: $0.5M per store", "1"],
        ["Labour scheduling and shrink tools, training", "3.0", "Allowance", "1–2"],
        ["Private-label range development", "2.0", "Allowance", "2"],
        ["Promotion analytics and vendor negotiation", "1.0", "Allowance", "1"],
        ["Delivery pricing changes and pilot", "0.5", "Allowance", "1–2"],
        ["Total plan", "17.0", "", ""],
        ["Cap, FY2026–FY2028", "25.0", "", ""],
        ["Contingency", "8.0", "", ""]]
table(s, 0.5, 1.65, [3.6, 0.8, 2.6, 0.7], rows, 0.42, size=10, header_h=0.38, aligns=["l", "r", "l", "c"],
      bolds={(6, -1), (8, -1)}, fills={6: PALE_BLUE})
# stacked bar
bx, by, bh, bw = 9.3, 1.9, 4.5, 1.1
scale = bh / 27.0
items = [("Lease exit 3 stores", 7.5, "9DB9DC"), ("Closures 6 stores", 3.0, BLUE), ("Tools & training", 3.0, "256ABF"),
         ("Private label", 2.0, "1C5CAB"), ("Promo analytics & delivery", 1.5, "104281")]
yy = by + bh
for nm, v, c in items:
    hgt = v * scale
    s.rect(bx, yy - hgt, bw, hgt - 0.02, fill=c)
    s.text(bx + bw + 0.1, yy - hgt / 2 - 0.13, 2.1, 0.26, f"{nm}  {v:.1f}", size=8.5, color=INK2)
    yy -= hgt
s.text(bx - 0.2, yy - 0.3, bw + 0.4, 0.28, "$17.0M", size=11, bold=True, color=INK, align="c")
ycap = by + bh - 25 * scale
s.line(bx - 0.3, ycap, bx + bw + 0.3, ycap, color=RED, lw=1.25, dash=True)
s.text(bx - 0.3, ycap - 0.28, 2.0, 0.26, "Cap $25M", size=9, bold=True, color=RED)
s.line(bx - 0.3, by + bh, bx + bw + 2.2, by + bh, color=MUTED)
s.text(0.5, 6.0, 8.0, 0.85,
       "- Firm wave alone needs ~$9.5M; the cap holds unless the allowances prove ~80% too low ((25 − 7.5) ÷ 9.5 = 1.84×)\n"
       "- Reinvested shrink hours (~$1.5M a year) are an operating cost and are already netted in lever 4",
       size=9.5, color=INK2, bullet=True, space=3)
add(s)

# ---------------------------------------------------------------- 18. Risks
s = base("The answer is most sensitive to traffic response and vendor funding; each risk has a trigger, and the core diagnosis survives every test",
         "Risks & asks", SRC + " Impacts are changes to FY2028 operating income versus the base plan ($37.8M firm).", 18)
rows = [["Assumption or risk", "Base case", "If wrong", "FY2028 impact", "Early-warning trigger", "Response"],
        ["Traffic response to fewer promotions (ValuMart)", "25% of gross gain lost", "50% lost", "−$2.0M", "Comps in ValuMart trade areas below −4.2%", "Keep depth in exposed stores; lead with private label"],
        ["Vendor funding recovery", "46% → 50%", "Stays at 46%", "−$3.7M", "Funding share in next two promo cycles", "Drop events vendors will not fund"],
        ["Share of e-commerce sales new to Harlow (survey)", "30%", "50%", "Loss shrinks to −$5.3M", "Customer-panel and loyalty data", "None needed: delivery still loses $8.50 per order"],
        ["Shrink responds to reinvested hours", "2.6% → 2.3%", "Only 2.45%", "−$2.1M", "10-store pilot shrink vs control", "Scale only if pilot gains ≥ 0.2 pts"],
        ["2027 wage step", "+4% on full bill", "+6%", "−$3.6M", "Legislation, local market rates", "Scheduling productivity; second wave"],
        ["Loss split across the 9 weak stores", "Pro rata", "The 6 carry less loss", "−$1.4M", "Store-level P&Ls", "Re-rank stores before giving notice"],
        ["FY2026 trading (no FY2026 data in pack)", "Holds at FY2025 run-rate", "Erosion continues", "~$5M slippage uses up covenant headroom", "Monthly operating income vs $20M path", "Brief lender; speed up promotion cuts"]]
table(s, 0.5, 1.6, [2.55, 1.55, 1.45, 1.6, 2.5, 2.68], rows, 0.58, size=9.5, header_h=0.36, bold_first_col=True,
      colors={(i, 3): RED for i in range(7) if i != 2})
s.text(0.5, 6.3, W - 1.0, 0.55,
       "Robustness: under every row, gross margin and delivery remain the main causes and the 8% cut remains inferior; what changes is how much of the second wave is needed.",
       size=10, bold=True, color=NAVY, valign="m")
add(s)

# ---------------------------------------------------------------- 19. Asks
s = base("We ask the board for three decisions today and will report progress against six measures every quarter",
         "Risks & asks", SRC, 19)
subhead(s, 0.5, 1.6, 6.0, "Decisions requested today")
asks = [("1", "Endorse the margin-first plan in place of the 8% across-the-board labour cut",
         "Targets 2.6% on firm levers and 3.0% with the second wave; one-time cost ~$17M within the $25M cap"),
        ("2", "Approve the delivery repricing roll-out and an e-commerce guardrail",
         "$7.99 fee / $100 threshold chain-wide; grow click-and-collect, not subsidised delivery; delivery itself is kept"),
        ("3", "Authorise preparation of the second wave",
         "Fix test and a board vote on the 3 other stores by mid-FY2027 ($7.5M); cost-recovery delivery pilot; vendor terms")]
y = 2.05
for n, h, b in asks:
    s.rect(0.5, y + 0.03, 0.4, 0.4, fill=NAVY, shape="oval")
    s.text(0.5, y + 0.03, 0.4, 0.4, n, size=13, bold=True, color="FFFFFF", align="c", valign="m")
    hd = s.text(1.05, y, 5.45, 0.5, h, size=11, bold=True, color=NAVY)
    nl = len(hd.wrap())
    s.text(1.05, y + 0.06 + nl * 11 * 1.18 / 72, 5.45, 0.6, b, size=9.5, color=INK2)
    y += 1.2
subhead(s, 6.9, 1.6, 5.93, "Next 90 days")
rows = [["Action", "Owner", "By"],
        ["FY2026 covenant forecast; lender briefing", "CFO", "Week 2"],
        ["Next promotion calendar without loss-making events; vendor terms", "Category / merchandising", "Week 4"],
        ["Delivery pricing live chain-wide; contract renewed", "E-commerce", "Week 6"],
        ["Store-by-store labour rebalancing plan (replaces 8% cut)", "COO", "Week 6"],
        ["Store P&L review; notices on 6 lease-expiry stores", "Property / CFO", "Week 8"],
        ["Shrink pilot launched in 10 lean stores", "COO", "Week 12"]]
table(s, 6.9, 2.05, [3.6, 1.5, 0.83], rows, 0.44, size=9.5, header_h=0.34)
subhead(s, 0.5, 5.6, W - 1.0, "Quarterly scorecard: FY2025 → FY2028 target")
kpis = [("Promo share of sales", "29% → 25%"), ("Vendor funding of markdowns", "46% → 50%+"), ("Private-label share", "18.5% → 21%"),
        ("Shrink, % of sales", "2.6% → 2.3%"), ("Loss per delivered order", "$12.34 → < $5"), ("Operating income", "≥ $20M FY2026; 3.0% FY2028")]
kw = (W - 1.0) / 6
for i, (k, v) in enumerate(kpis):
    xk = 0.5 + i * kw
    s.rect(xk + 0.03, 6.03, kw - 0.06, 0.82, fill=PALE)
    s.text(xk + 0.1, 6.06, kw - 0.2, 0.3, k, size=8.5, color=INK2)
    s.text(xk + 0.1, 6.36, kw - 0.2, 0.45, v, size=10.5, bold=True, color=NAVY)
add(s)

# ---------------------------------------------------------------- Appendix divider
s = Slide()
s.rect(0, 0, W, H, fill=NAVY)
s.text(0.95, 2.9, 11, 0.9, "Appendix", size=32, bold=True, color="FFFFFF")
s.text(0.95, 3.8, 11, 1.2, "A1 Margin and gross-margin calculations · A2 E-commerce cost reconstruction · A3 Lever ranges and FY2026 phasing · A4 Data notes and assumptions",
       size=13, color="D6E2F0")
add(s)

# ---------------------------------------------------------------- A1
s = base("A1. Every line of the income statement as a share of sales: the ratio changes sum to the 2.35-point decline",
         None, SRC + " Table 1–3.", 21)
rows = [["% of sales", "FY2023", "FY2024", "FY2025", "Change, pts", "$M at FY2025 sales"],
        ["Sales, $M", "1,420.0", "1,468.0", "1,503.0", "+5.8%", ""],
        ["Gross margin", "26.04%", "25.61%", "25.02%", "−1.02", "−15.3"],
        ["Store labour", "11.80%", "12.00%", "12.10%", "+0.30", "−4.5"],
        ["Occupancy and energy", "5.80%", "5.90%", "6.00%", "+0.20", "−3.0"],
        ["E-commerce fulfilment", "0.37%", "0.74%", "1.20%", "+0.84", "−12.6"],
        ["Other SG&A", "4.70%", "4.70%", "4.70%", "0.00", "0.0"],
        ["Operating margin", "3.37%", "2.27%", "1.02%", "−2.35", "−35.4"]]
table(s, 0.5, 1.65, [2.6, 1.2, 1.2, 1.2, 1.3, 1.7], rows, 0.36, size=10, header_h=0.36, aligns=["l"] + ["r"] * 5, bolds={(6, -1)})
subhead(s, 0.5, 4.75, 5.8, "Gross-margin mix effects")
s.text(0.5, 5.15, 5.8, 1.7,
       "- Promotion: (29.0% − 24.0%) × −14 pts = −0.70 pts\n- Private label: (18.5% − 17.0%) × +12 pts = +0.18 pts\n"
       "- Shrink: −(2.6% − 2.1%) = −0.50 pts\n- Sum −1.02 pts = actual change; residual 0.00", size=10, color=INK, bullet=True, space=3)
subhead(s, 6.9, 4.75, 5.93, "Labour decomposition")
s.text(6.9, 5.15, 5.93, 1.7,
       "- Hours: 7.02 × $1,420M = 9.97M (FY2023); 6.60 × $1,503M = 9.92M (FY2025)\n"
       "- Wage effect at FY2023 hours: 7.02 × ($18.38 − $16.80) ÷ 1,000 = +1.11 pts\n"
       "- Productivity at FY2025 wage: (6.60 − 7.02) × $18.38 ÷ 1,000 = −0.77 pts\n"
       "- Labour at FY2023 productivity would have cost $193.9M", size=10, color=INK, bullet=True, space=3)
add(s)

# ---------------------------------------------------------------- A2
s = base("A2. E-commerce fulfilment cost rebuilds exactly from order data, and the fully costed loss has grown every year",
         None, SRC + " Table 5, §7. Incremental contribution = sales × 30% × 20¢.", 22)
rows = [["$M unless stated", "FY2023", "FY2024", "FY2025", "Formula"],
        ["Orders, thousands", "453", "865", "1,331", "Table 5"],
        ["Delivered orders, thousands", "204", "450", "772", "Orders × delivered share"],
        ["Picking cost", "3.3", "6.3", "9.8", "Orders × picking cost per order"],
        ["Third-party delivery cost", "2.6", "6.0", "10.7", "Delivered × cost per delivered order"],
        ["Delivery fees collected", "−0.7", "−1.4", "−2.4", "Delivered × fee per delivered order"],
        ["Net fulfilment cost (= Table 1)", "5.2", "10.9", "18.1", "Sum; matches income statement"],
        ["E-commerce sales", "42.6", "82.2", "127.8", "Orders × average basket"],
        ["Incremental contribution", "2.6", "4.9", "7.7", "Sales × 30% new × 20¢"],
        ["Fully costed e-commerce result", "−2.6", "−6.0", "−10.4", "Contribution − fulfilment"],
        ["Fee as % of delivery cost", "26%", "24%", "22%", "Fee ÷ cost per delivered order"]]
table(s, 0.5, 1.65, [3.2, 1.2, 1.2, 1.2, 5.53], rows, 0.4, size=10, header_h=0.36, aligns=["l", "r", "r", "r", "l"],
      bolds={(5, -1), (8, -1)}, fills={5: PALE, 8: PALE})
s.text(0.5, 6.25, W - 1.0, 0.6, "E-commerce team's 6.1% × $127.8M = $7.8M; deducting delivery net of fees ($10.7M − $2.4M = $8.3M) gives −$0.5M (−0.4%) even before cannibalisation.",
       size=10, color=INK2)
add(s)

# ---------------------------------------------------------------- A3
s = base("A3. Even the low case adds ~$17M of operating income; the high case reaches ~3.2% on firm levers alone",
         None, SRC + " Low and high cases vary one driver per lever, as shown.", 23)
rows = [["Lever", "Low case driver", "Low", "Base", "High", "High case driver", "FY2026 in-year"],
        ["1. Promotion reset", "Promo share −2 pts", "3.0", "6.1", "7.6", "−5 pts (FY2023 level)", "3.2"],
        ["2. Vendor funding", "To 48%", "1.9", "3.7", "3.7", "50% (55% is wave 2)", "1.0"],
        ["3. Private label", "To 20.0%", "2.6", "4.3", "6.1", "To 22.0%", "1.0"],
        ["4. Shrink (net of hours)", "−0.15 pts", "0.7", "2.8", "4.3", "−0.40 pts", "0.0"],
        ["5. Targeted labour", "−2% hours", "3.6", "5.5", "7.3", "−4% hours", "2.7"],
        ["6. Delivery pricing and contract", "Test result − 20%; no contract gain", "2.0", "3.3", "4.0", "Test +30%; contract −5%", "1.7"],
        ["7. Exit 6 stores", "Less loss in the 6", "3.0", "4.4", "5.0", "More loss in the 6", "0.0"],
        ["Total firm levers", "", "16.8", "30.1", "38.0", "", "9.6"],
        ["FY2028 operating income ($7.7M + levers)", "", "24.5", "37.8", "45.7", "", ""],
        ["FY2028 operating margin (on $1,444M)", "", "1.7%", "2.6%", "3.2%", "", ""]]
table(s, 0.5, 1.65, [3.0, 2.75, 0.85, 0.85, 0.85, 2.6, 1.43], rows, 0.42, size=10, header_h=0.36,
      aligns=["l", "l", "r", "r", "r", "l", "r"], bolds={(7, -1), (8, -1), (9, -1)}, fills={7: PALE, 9: PALE_BLUE})
s.text(0.5, 6.35, W - 1.0, 0.5, "FY2026 in-year values are at FY2025 scale; the delivery figure is net of the half-year contract rise.",
       size=9.5, color=INK2)
add(s)

# ---------------------------------------------------------------- A4
s = base("A4. Data notes and assumptions we made where the briefing pack was silent",
         None, SRC, 24)
s.text(0.5, 1.65, 6.0, 5.2,
       "~ **Choices made without the CEO's input**\n"
       "- **Fiscal timing:** the pack's latest actuals are FY2025 and its constraints (covenant, capital window, labour plan) start in FY2026, so FY2026 is treated as the first plan year. If FY2026 has closed by the board date, its covenant result is a fact to report and the in-year estimates apply to FY2027\n"
       "- **Baseline:** FY2025 ratios at FY2025 sales scale; no further erosion and no growth\n"
       "- **Wage step:** +4% applied to the whole labour bill (conservative)\n"
       "- **Weak stores:** sales and EBITDA split pro rata between the 6 and the 3\n"
       "~ **Claims in the pack we did not rely on**\n"
       "- E-commerce team's +6.1% margin: leaves out third-party delivery and treats every sale as new (p.9)\n"
       "- Category team's “promotions work”: a correlation, and sales growth rather than profit (p.7)\n"
       "- Management's $14.5M labour saving: gross of shrink and service effects (p.10)",
       size=10, color=INK, bullet=True, space=6)
s.text(6.9, 1.65, 5.93, 5.2,
       "~ **Team estimates not in the pack**\n"
       "- One-time cost allowances (p.17), except the $7.5M lease exit\n"
       "- 25% lost-volume allowance on the promotion reset\n"
       "- $1.5M a year of reinvested hours (~78,000 hours, ~1 FTE per lean store)\n"
       "- FY2026 phasing of each lever\n"
       "- 40% of delivery customers switching to click-and-collect under option C\n"
       "~ **Data caveats**\n"
       "- Survey incrementality (30%) is stated intent; delivery is loss-making even at 50%\n"
       "- Shrink-by-quartile is a correlation, hence the pilot\n"
       "- Vendor-funding sizing assumes the 14-pt promo margin gap is net of vendor funding",
       size=10, color=INK, bullet=True, space=6)
add(s)

# ---------------------------------------------------------------- render
out = sys.argv[1]
prev = sys.argv[2]
os.makedirs(prev, exist_ok=True)
imgs = []
for i, sl in enumerate(slides):
    imgs.append(to_png(sl, os.path.join(prev, f"s{i+1:02d}.png"), i + 1))
to_pptx(slides, out, notes)
imgs[0].save(os.path.join(prev, "deck_preview.pdf"), save_all=True, append_images=imgs[1:], resolution=110)
print("slides:", len(slides))
print("\n".join(WARNINGS) if WARNINGS else "no overflow warnings")
