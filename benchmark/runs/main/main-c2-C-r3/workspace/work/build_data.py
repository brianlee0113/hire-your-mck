"""Data points for the Harlow margin deck. Every input comes from the briefing pack (s1);
every calculation is a derived point (s0) whose value is computed from its calc."""
import re

DP = {}          # id -> data point
ORDER = []


def _ev(calc):
    e = calc
    for i in sorted(DP, key=len, reverse=True):
        e = re.sub(rf"(?<![\w.]){re.escape(i)}(?![\w-])", f"({DP[i]['value']!r})", e)
    return eval(e, {"__builtins__": {}})


def P(id, label, value, unit, period, excerpt, locator, **kw):
    d = {"id": id, "slide_id": None, "label": label, "value": value, "unit": unit, "period": period,
         "source_id": "s1", "excerpt": excerpt, "locator": locator}
    d.update(kw)
    DP[id] = d
    ORDER.append(id)


def D(id, label, unit, calc, formula, period="FY2025", estimate=False, assumptions=None, rnd=None, **kw):
    v = _ev(calc)
    if rnd is not None:
        v = round(v, rnd)
    refs = [i for i in sorted(DP, key=len, reverse=True)]
    used = []
    tmp = calc
    for i in refs:
        if re.search(rf"(?<![\w.]){re.escape(i)}(?![\w-])", tmp):
            used.append(i)
            tmp = re.sub(rf"(?<![\w.]){re.escape(i)}(?![\w-])", "_", tmp)
    d = {"id": id, "slide_id": None, "label": label, "value": v, "unit": unit, "period": period,
         "source_id": "s0", "derived_from": used, "formula": formula, "calc": calc}
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions or []
    d.update(kw)
    DP[id] = d
    ORDER.append(id)


T1 = "Table 1. Income statement, $ millions"
# ---------------------------------------------------------------- Table 1
rows = {
    "sales": ("Sales", "| Sales | 1,420.0 | 1,468.0 | 1,503.0 |", (1420.0, 1468.0, 1503.0)),
    "gp": ("Gross profit", "| Gross profit | 369.8 | 376.0 | 376.1 |", (369.8, 376.0, 376.1)),
    "lab": ("Store labor", "| Store labor | 167.6 | 176.2 | 181.9 |", (167.6, 176.2, 181.9)),
    "occ": ("Occupancy and energy", "| Occupancy and energy | 82.4 | 86.6 | 90.2 |", (82.4, 86.6, 90.2)),
    "ecf": ("E-commerce fulfillment (picking + delivery, net of delivery fees)",
            "| E-commerce fulfillment (picking + delivery, net of delivery fees) | 5.2 | 10.9 | 18.1 |", (5.2, 10.9, 18.1)),
    "oth": ("Other SG&A", "| Other SG&A | 66.7 | 69.0 | 70.6 |", (66.7, 69.0, 70.6)),
    "oi": ("Operating income", "| **Operating income** | **47.9** | **33.4** | **15.3** |", (47.9, 33.4, 15.3)),
}
for k, (lab, ex, vals) in rows.items():
    for y, v in zip(("23", "24", "25"), vals):
        P(f"{k}{y}", f"Harlow {lab}, FY20{y}", v, "$M", f"FY20{y}", ex, f"{T1}, row '{lab}', column FY20{y}")
for y, v in zip(("23", "24", "25"), (0.0337, 0.0227, 0.0102)):
    P(f"om{y}", f"Harlow operating margin, FY20{y}", v, "%", f"FY20{y}", "| Operating margin | 3.37% | 2.27% | 1.02% |",
      f"{T1}, row 'Operating margin', column FY20{y}")

T2 = "Table 2. Gross-margin drivers"
for k, lab, ex, vals in (
        ("promo", "Promotional sales, share of sales", "| Promotional sales, share of sales | 24.0% | 26.2% | 29.0% |", (0.24, 0.262, 0.29)),
        ("pl", "Private-label sales, share of sales", "| Private-label sales, share of sales | 17.0% | 17.7% | 18.5% |", (0.17, 0.177, 0.185)),
        ("shr", "Shrink, % of sales", "| Shrink, % of sales | 2.1% | 2.3% | 2.6% |", (0.021, 0.023, 0.026))):
    for y, v in zip(("23", "24", "25"), vals):
        P(f"{k}{y}", f"{lab}, FY20{y}", v, "%", f"FY20{y}", ex, f"{T2}, row '{lab}', column FY20{y}")
P("promogap", "Gross-margin gap of promotional against regular-price sales", 14, "pp", "FY2023–25",
  "Promotional sales earn 14 percentage points less gross margin than regular-price sales (unchanged over the period).", "Section 5, note under Table 2")
P("plgap", "Gross-margin premium of private label over national brands", 12, "pp", "FY2023–25",
  "Private-label sales earn 12 percentage points more gross margin than national brands (unchanged).", "Section 5, note under Table 2")
P("vf23", "Share of promotional markdowns covered by vendor funding, FY2023", 0.55, "%", "FY2023",
  "Vendor funding covered 55% of promotional markdowns in FY2023 and 46% in FY2025.", "Section 5, note under Table 2")
P("vf25", "Share of promotional markdowns covered by vendor funding, FY2025", 0.46, "%", "FY2025",
  "Vendor funding covered 55% of promotional markdowns in FY2023 and 46% in FY2025.", "Section 5, note under Table 2")
P("lossev", "Share of FY2025 promotional events that lost money after counting extra units", 0.38, "%", "FY2025",
  "A post-event review of FY2025 promotions found that 38% of events lost money after counting the extra units they sold.", "Section 5, note under Table 2")

T3 = "Table 3. Store labor"
P("wage23", "Average hourly wage incl. benefits, FY2023", 16.80, "$", "FY2023", "| Average hourly wage incl. benefits | $16.80 | $18.38 |", f"{T3}, column FY2023")
P("wage25", "Average hourly wage incl. benefits, FY2025", 18.38, "$", "FY2025", "| Average hourly wage incl. benefits | $16.80 | $18.38 |", f"{T3}, column FY2025")
P("hrs23", "Labor hours per $1,000 of sales, FY2023", 7.02, "hours", "FY2023", "| Labor hours per $1,000 of sales | 7.02 | 6.60 |", f"{T3}, column FY2023")
P("hrs25", "Labor hours per $1,000 of sales, FY2025", 6.60, "hours", "FY2025", "| Labor hours per $1,000 of sales | 7.02 | 6.60 |", f"{T3}, column FY2025")
P("labpct23", "Store labor, % of sales, FY2023", 0.118, "%", "FY2023", "| Store labor, % of sales | 11.8% | 12.1% |", f"{T3}, column FY2023")
P("labpct25", "Store labor, % of sales, FY2025", 0.121, "%", "FY2025", "| Store labor, % of sales | 11.8% | 12.1% |", f"{T3}, column FY2025")
P("per1000", "Sales unit for labor hours", 1000, "$", "FY2023–25", "| Labor hours per $1,000 of sales | 7.02 | 6.60 |", f"{T3}, row label", used_in="text")

T4 = "Table 4. Shrink by store labor intensity, FY2025"
for k, lab, v in (("q1", "Q1 (fewest labor hours per $ sales)", 0.031), ("q2", "Q2", 0.027), ("q3", "Q3", 0.024), ("q4", "Q4 (most)", 0.023)):
    P(k, f"Shrink, % of sales, stores in quartile {lab}", v, "%", "FY2025", f"| {lab} | {v * 100:.1f}% |", f"{T4}, row {lab}")
P("waste", "Fresh and produce waste, share of shrink", 0.45, "%", "FY2025",
  "Shrink composition FY2025: fresh and produce waste 45%, theft 35%, administrative and receiving errors 20%.", "Section 6, under Table 4")
P("theft", "Theft, share of shrink", 0.35, "%", "FY2025",
  "Shrink composition FY2025: fresh and produce waste 45%, theft 35%, administrative and receiving errors 20%.", "Section 6, under Table 4")
P("admin", "Administrative and receiving errors, share of shrink", 0.20, "%", "FY2025",
  "Shrink composition FY2025: fresh and produce waste 45%, theft 35%, administrative and receiving errors 20%.", "Section 6, under Table 4")

MG = "Section 4. Management's current view"
P("mgcut", "Cut in scheduled store labor hours in the draft plan", 0.08, "%", "FY2026",
  "cut scheduled store labor hours by 8% in FY2026 (they estimate about $14.5M a year of savings)", MG)
P("mgsave", "Management's estimate of the saving from the 8% hours cut", 14.5, "$M", "a year",
  "cut scheduled store labor hours by 8% in FY2026 (they estimate about $14.5M a year of savings)", MG)

T5 = "Table 5. E-commerce operating data"
for k, lab, ex, vals, unit in (
        ("ecsh", "E-commerce share of sales", "| E-commerce share of sales | 3.0% | 5.6% | 8.5% |", (0.03, 0.056, 0.085), "%"),
        ("ord", "Orders, thousands", "| Orders, thousands | 453 | 865 | 1,331 |", (453, 865, 1331), "k"),
        ("bask", "Average basket", "| Average basket | $94 | $95 | $96 |", (94, 95, 96), "$"),
        ("del", "Share of orders delivered to the home", "| Share of orders delivered to the home (rest: click-and-collect) | 45% | 52% | 58% |", (0.45, 0.52, 0.58), "%"),
        ("pick", "Picking cost per order (all orders)", "| Picking cost per order (all orders) | $7.20 | $7.30 | $7.40 |", (7.20, 7.30, 7.40), "$"),
        ("dcost", "Third-party delivery cost per delivered order", "| Third-party delivery cost per delivered order | $12.90 | $13.40 | $13.80 |", (12.90, 13.40, 13.80), "$"),
        ("fee", "Average delivery fee collected per delivered order", "| Average delivery fee collected per delivered order | $3.40 | $3.20 | $3.10 |", (3.40, 3.20, 3.10), "$")):
    for y, v in zip(("23", "24", "25"), vals):
        P(f"{k}{y}", f"{lab}, FY20{y}", v, unit, f"FY20{y}", ex, f"{T5}, row '{lab}', column FY20{y}")
E7 = "Section 7, notes under Table 5"
P("freeth", "Basket above which delivery is free", 75, "$", "FY2025", "Delivery is free above $75 (a $4.99 fee below). Click-and-collect is free.", E7)
P("smallfee", "Delivery fee below the free-delivery threshold", 4.99, "$", "FY2025", "Delivery is free above $75 (a $4.99 fee below). Click-and-collect is free.", E7)
P("ecn", "E-commerce customers surveyed", 2300, "customers", "FY2025",
  "Survey of 2,300 e-commerce customers (FY2025): 70% of what they buy online they say they would otherwise have bought in a Harlow store.", E7)
P("cannib", "Share of online purchases customers say they would otherwise have bought in a Harlow store", 0.70, "%", "FY2025",
  "Survey of 2,300 e-commerce customers (FY2025): 70% of what they buy online they say they would otherwise have bought in a Harlow store.", E7)
P("newc", "Contribution per dollar of sales new to Harlow, before e-commerce fulfillment", 0.20, "%", "FY2025",
  "Finance estimates that a dollar of sales that is genuinely new to Harlow adds about 20 cents of contribution (gross margin less variable store costs), before e-commerce fulfillment.", E7)
FT = "Section 7, fee test"
P("teststores", "Stores in the fee test", 4, "stores", "late FY2025", "**Fee test** (4 stores, 10 weeks, late FY2025)", FT)
P("testweeks", "Length of the fee test", 10, "weeks", "late FY2025", "**Fee test** (4 stores, 10 weeks, late FY2025)", FT)
P("testfee", "Delivery fee in the test", 7.99, "$", "late FY2025", "delivery fee raised to $7.99 and the free-delivery threshold to $100.", FT)
P("testthr", "Free-delivery threshold in the test", 100, "$", "late FY2025", "delivery fee raised to $7.99 and the free-delivery threshold to $100.", FT)
P("tdel", "Change in delivered orders in the fee test", -0.09, "%", "late FY2025",
  "Delivered orders fell 9%, click-and-collect orders rose 14%, total e-commerce sales fell 2%", FT)
P("tcc", "Change in click-and-collect orders in the fee test", 0.14, "%", "late FY2025",
  "Delivered orders fell 9%, click-and-collect orders rose 14%, total e-commerce sales fell 2%", FT)
P("tsales", "Change in total e-commerce sales in the fee test", -0.02, "%", "late FY2025",
  "Delivered orders fell 9%, click-and-collect orders rose 14%, total e-commerce sales fell 2%", FT)
P("tfee", "Average fee collected per delivered order in the fee test", 6.40, "$", "late FY2025",
  "the average fee collected per delivered order rose to $6.40.", FT)

T6 = "Table 6. The nine weakest stores, FY2025"
P("stores", "Harlow stores", 58, "stores", "FY2025", "| Stores with negative four-wall EBITDA | 9 of 58 |", T6)
P("neg", "Stores with negative four-wall EBITDA", 9, "stores", "FY2025", "| Stores with negative four-wall EBITDA | 9 of 58 |", T6)
P("negsales", "Combined sales of the nine stores", 118.0, "$M", "FY2025", "| Their combined sales | $118.0M |", T6)
P("negebitda", "Combined four-wall EBITDA of the nine stores", -3.1, "$M", "FY2025", "| Their combined four-wall EBITDA | −$3.1M |", T6)
P("lease6", "Stores of the nine with leases expiring by end of 2027", 6, "stores", "FY2025", "| Leases expiring by end of 2027 | 6 of the 9 |", T6)
P("exitcost", "Estimated one-time lease-exit cost for the other three stores", 7.5, "$M", "one-time",
  "| Estimated lease-exit cost for the other 3 | $7.5M (one-time) |", T6)
P("transfer", "Share of a closed store's sales that moves to a nearby Harlow store (past closures)", 0.25, "%", "past closures",
  "| Share of their sales expected to move to a nearby Harlow store if closed (past closures) | 25% |", T6)
P("transc", "Contribution on sales moved to a receiving store", 0.12, "%", "past closures",
  "| Contribution on sales moved to a receiving store | 12% |", T6)

C9 = "Section 9. Customers and competitors"
P("vm", "ValuMart stores opened in Harlow trade areas since 2023", 11, "stores", "2023–FY2025",
  "A discount grocer, ValuMart, has opened 11 stores in Harlow trade areas since 2023.", C9)
P("compnear", "Comparable sales, Harlow stores within three miles of a new ValuMart", -0.042, "%", "FY2025",
  "Harlow stores within three miles of a new ValuMart had comparable sales of −4.2% in FY2025, against +1.1% for other Harlow stores.", C9)
P("compother", "Comparable sales, other Harlow stores", 0.011, "%", "FY2025",
  "Harlow stores within three miles of a new ValuMart had comparable sales of −4.2% in FY2025, against +1.1% for other Harlow stores.", C9)
P("survn", "Customers in the price-perception survey", 3100, "customers", "FY2025", "Customer survey (n = 3,100)", C9)
P("exp25", "Customers who say Harlow is more expensive than other options, FY2025", 0.41, "%", "FY2025",
  "Customer survey (n = 3,100): 41% say Harlow is \"more expensive than other options\" (FY2023: 33%)", C9 + ", current (FY2025) reading")
P("exp23", "Customers who say Harlow is more expensive than other options, FY2023", 0.33, "%", "FY2023",
  "Customer survey (n = 3,100): 41% say Harlow is \"more expensive than other options\" (FY2023: 33%)", C9)
P("fresh", "Customers naming fresh produce as a top reason to shop Harlow", 0.58, "%", "FY2025",
  "top reasons to shop Harlow are fresh produce (58%) and convenience (44%).", C9)
P("conv", "Customers naming convenience as a top reason to shop Harlow", 0.44, "%", "FY2025",
  "top reasons to shop Harlow are fresh produce (58%) and convenience (44%).", C9)
O10 = "Section 10. Other material circulated to the board"
P("ecteam", "E-commerce team's reported contribution margin on e-commerce sales", 0.061, "%", "FY2025",
  "\"E-commerce is profitable: a contribution margin of 6.1% of e-commerce sales in FY2025.\"", O10)
P("deepcomp", "Comparable sales growth, stores with the deepest promotions", 0.018, "%", "FY2025",
  "\"Stores with the deepest promotions in FY2025 grew comparable sales 1.8%, against 0.2% for the rest. Promotions work.\"", O10)
P("restcomp", "Comparable sales growth, other stores", 0.002, "%", "FY2025",
  "\"Stores with the deepest promotions in FY2025 grew comparable sales 1.8%, against 0.2% for the rest. Promotions work.\"", O10)
OB = "Section 3. Objectives and constraints"
P("target", "Operating margin target for FY2028", 0.03, "%", "FY2028", "**Target:** operating margin back to at least 3.0% by FY2028.", OB)
P("capcap", "Maximum one-time cost or capital for the plan", 25, "$M", "FY2026–FY2028",
  "**Capital:** at most $25M of one-time cost or capital for the plan over FY2026–FY2028.", OB)
P("cov", "Lender covenant: minimum operating income in FY2026", 20, "$M", "FY2026",
  "a covenant requires operating income of at least $20M in FY2026.", OB)
U11 = "Section 11. Uncertainties"
P("dcrise", "Rate rise proposed by the third-party delivery provider", 0.03, "%", "2026 renewal",
  "Whether third-party delivery rates can be renegotiated (contract renews in 2026; the provider proposed a 3% rise).", U11)
P("minw", "State minimum-wage rise in 2027", 0.04, "%", "2027", "Wage rates: the state minimum wage rises again in 2027 (+4%).", U11)

# ================================================================ derived: diagnosis
D("salesg", "Sales growth, FY2023–25", "%", "sales25 / sales23 - 1", "1,503.0 ÷ 1,420.0 − 1", "FY2023–25", rnd=2)
D("oidrop", "Change in operating income, FY2023–25", "%", "oi25 / oi23 - 1", "15.3 ÷ 47.9 − 1", "FY2023–25", rnd=2)
D("dompp", "Fall in operating margin, FY2023–25", "pp", "(om23 - om25) * 100", "(3.37% − 1.02%) × 100", "FY2023–25")
D("b_promo", "Operating-margin effect of the rise in promotional share", "%", "(promo23 - promo25) * promogap / 100",
  "−(29.0% − 24.0%) × 14 pp", "FY2023–25")
D("b_shr", "Operating-margin effect of the rise in shrink", "%", "shr23 - shr25", "−(2.6% − 2.1%)", "FY2023–25")
D("b_pl", "Operating-margin effect of the rise in private-label share", "%", "(pl25 - pl23) * plgap / 100",
  "(18.5% − 17.0%) × 12 pp", "FY2023–25")
D("b_lab", "Operating-margin effect of store labor as a share of sales", "%", "lab23 / sales23 - lab25 / sales25",
  "167.6 ÷ 1,420.0 − 181.9 ÷ 1,503.0", "FY2023–25")
D("b_occ", "Operating-margin effect of occupancy and energy as a share of sales", "%", "occ23 / sales23 - occ25 / sales25",
  "82.4 ÷ 1,420.0 − 90.2 ÷ 1,503.0", "FY2023–25")
D("b_ecf", "Operating-margin effect of e-commerce fulfillment as a share of sales", "%", "ecf23 / sales23 - ecf25 / sales25",
  "5.2 ÷ 1,420.0 − 18.1 ÷ 1,503.0", "FY2023–25")
D("b_oth", "Operating-margin effect of other SG&A as a share of sales", "%", "oth23 / sales23 - oth25 / sales25",
  "66.7 ÷ 1,420.0 − 70.6 ÷ 1,503.0", "FY2023–25")
D("big3share", "Share of the margin decline from promotion mix, shrink and e-commerce fulfillment", "%",
  "(b_promo + b_shr + b_ecf) / (om25 - om23)", "(0.70 + 0.50 + 0.84) ÷ 2.35", "FY2023–25", rnd=2)
D("labshare", "Share of the margin decline from store labor", "%", "b_lab / (om25 - om23)", "0.30 ÷ 2.35", "FY2023–25", rnd=2)
D("gm23", "Gross margin, FY2023", "%", "gp23 / sales23", "369.8 ÷ 1,420.0", "FY2023")
D("gm25", "Gross margin, FY2025", "%", "gp25 / sales25", "376.1 ÷ 1,503.0", "FY2025")
D("dgmpp", "Fall in gross margin, FY2023–25", "pp", "(gp23 / sales23 - gp25 / sales25) * 100", "(26.04% − 25.02%) × 100", "FY2023–25")
D("gmpromoshare", "Share of the gross-margin decline from the rise in promotional share", "%",
  "b_promo / (gp25 / sales25 - gp23 / sales23)", "0.70 ÷ 1.02", "FY2023–25", rnd=2)
D("tgtoi25", "Operating income at a 3.0% margin on FY2025 sales", "$M", "target * sales25", "3.0% × 1,503.0", "FY2025 base")
D("gap", "Operating income to add to reach a 3.0% margin, at FY2025 sales", "$M", "target * sales25 - oi25",
  "3.0% × 1,503.0 − 15.3", "FY2028 target")
D("covneed", "Operating income to add in FY2026 to meet the covenant", "$M", "cov - oi25", "20 − 15.3", "FY2026")

# ================================================================ labor and shrink
D("wagerise", "Rise in average hourly wage incl. benefits, FY2023–25", "%", "wage25 / wage23 - 1", "18.38 ÷ 16.80 − 1", "FY2023–25", rnd=3)
D("hrschg", "Change in labor hours per $1,000 of sales, FY2023–25", "%", "hrs25 / hrs23 - 1", "6.60 ÷ 7.02 − 1", "FY2023–25", rnd=2)
D("labpp", "Rise in store labor as a share of sales, FY2023–25", "pp", "(labpct25 - labpct23) * 100", "(12.1% − 11.8%) × 100", "FY2023–25")
D("labsaved", "Store labor cost avoided in FY2025 by fewer hours per $1,000 of sales", "$M", "lab25 * hrs23 / hrs25 - lab25",
  "181.9 × 7.02 ÷ 6.60 − 181.9", "FY2025")
D("shrup", "Rise in shrink, FY2023–25", "pp", "(shr25 - shr23) * 100", "(2.6% − 2.1%) × 100", "FY2023–25")
D("hrsdrop", "Fall in labor hours per $1,000 of sales, FY2023–25", "%", "(hrs23 - hrs25) / hrs23", "(7.02 − 6.60) ÷ 7.02", "FY2023–25")
A_GB = ["All of the 0.5 percentage-point shrink rise in FY2023–25 came from fewer hours per $1,000 of sales (an upper bound: theft is 35% of shrink)",
        "Shrink rises in proportion to the hours cut, as it did in FY2023–25",
        "Sales held at FY2025 level; lost sales from longer waits or stock-outs are not counted, which would cut the net saving further"]
D("gb", "Higher shrink that the 8% hours cut would cause", "$M", "mgcut / hrsdrop * shrup / 100 * sales25",
  "8% ÷ 5.98% × 0.5 pp × $1,503.0M", "a year", True, A_GB)
D("mgnet", "Net saving of the 8% hours cut after higher shrink", "$M", "mgsave - gb", "14.5 − 10.0", "a year", True, A_GB)
D("giveshare", "Share of the hours-cut saving given back in shrink", "%", "gb / mgsave", "10.0 ÷ 14.5", "a year", True, A_GB)
D("mgplan", "Operating income under the draft plan, before the 2027 wage rise", "$M", "oi25 + mgnet", "15.3 + 4.5", "FY2026", True,
  A_GB + ["E-commerce frozen at its FY2025 loss; nothing else changes from FY2025"])
D("q1q4", "Extra shrink in the least-staffed quartile relative to the best-staffed", "%", "q1 / q4 - 1", "3.1% ÷ 2.3% − 1", "FY2025", rnd=2)
D("q34", "Shrink difference between quartile 3 and quartile 4 stores", "pp", "(q3 - q4) * 100", "(2.4% − 2.3%) × 100", "FY2025")
D("q14pp", "Shrink difference between quartile 1 and quartile 4 stores", "pp", "(q1 - q4) * 100", "(3.1% − 2.3%) × 100", "FY2025")
D("nontr", "Share of the nine stores' sales that would not move to another Harlow store", "%", "1 - transfer", "1 − 25%", "past closures")
D("saleslost", "Harlow sales lost by exiting the nine stores", "$M", "negsales * (1 - transfer)", "118.0 × (1 − 25%)", "a year")
A_S28 = ["FY2025 sales and prices held flat to FY2028; no market growth or inflation counted on either sales or costs",
         "The nine loss-making stores are exited and 25% of their sales move to nearby Harlow stores, as in past closures"]
D("sales28", "FY2028 sales at FY2025 prices, after the nine store exits", "$M", "sales25 - negsales * (1 - transfer)",
  "1,503.0 − 118.0 × 75%", "FY2028", True, A_S28)
D("shrgap", "Fleet shrink above the best-staffed quartile's rate", "pp", "(shr25 - q4) * 100", "(2.6% − 2.3%) × 100", "FY2025")
A_SH = ["Fleet shrink falls to the 2.3% of sales the best-staffed quartile already runs, still above FY2023's 2.1%",
        "Hours move from Q4 stores to Q1 and Q2 stores for busy-day rotation and receiving; total hours and labor cost stay flat",
        "Applied to FY2028 sales at FY2025 prices of $1,414.5M (after the nine store exits)"]
D("shrfix", "Operating income from bringing fleet shrink to 2.3% of sales", "$M", "shrgap / 100 * sales28",
  "0.3 pp × $1,414.5M", "FY2028 run-rate", True, A_SH + A_S28)
D("elim", "Four-wall EBITDA loss removed by exiting the nine stores", "$M", "0 - negebitda", "−(−3.1)", "a year")
A_CL = ["25% of the nine stores' sales move to a nearby Harlow store, as in past closures, at 12% contribution",
        "Allocated overheads are not saved and depreciation savings are not counted, both of which make the estimate conservative",
        "The split between the six and the three stores follows the store count, as the pack gives only combined figures"]
D("transfc", "Contribution on sales that move to nearby Harlow stores", "$M", "negsales * transfer * transc",
  "118.0 × 25% × 12%", "a year", True, A_CL)
D("closeall", "Operating income added by exiting the nine loss-making stores", "$M", "0 - negebitda + negsales * transfer * transc",
  "3.1 + 118.0 × 25% × 12%", "FY2028 run-rate", True, A_CL)
D("close6", "Operating income added by exiting the six stores whose leases end by 2027", "$M", "closeall * lease6 / neg",
  "6.6 × 6 ÷ 9", "FY2028 run-rate", True, A_CL)
D("close3", "Operating income added by exiting the other three stores", "$M", "closeall * (neg - lease6) / neg",
  "6.6 × 3 ÷ 9", "FY2028 run-rate", True, A_CL)
D("n3st", "Loss-making stores with leases running beyond 2027", "stores", "neg - lease6", "9 − 6", "FY2025")
D("payback3", "Payback on the exit cost of the three stores", "years", "exitcost / close3", "7.5 ÷ 2.2", "one-time", True, A_CL)

# ================================================================ promotions and private label
D("promocut", "Cut in promotional share to return to the FY2023 mix", "pp", "(promo25 - promo23) * 100", "(29.0% − 24.0%) × 100", "FY2025–28")
D("promoevshare", "Share of FY2025 promotional sales removed by returning to the FY2023 mix", "%", "(promo25 - promo23) / promo25",
  "5.0 pp ÷ 29.0%", "FY2025", rnd=2)
A_PR = ["Promotional share falls from 29% to FY2023's 24% of sales, about a sixth of promotional sales, against the 38% of events that lost money",
        "Sales that leave promotion sell at regular price, earning 14 percentage points more margin; dropped events lost money, so their lost units are not counted",
        "Promotional depth is kept in ValuMart trade areas; cuts fall on the other stores",
        "Applied to FY2028 sales at FY2025 prices of $1,414.5M; vendor funding stays at 46% of markdowns"]
D("promofix", "Operating income from returning promotions to the FY2023 mix", "$M", "promocut * promogap / 10000 * sales28",
  "5 pp × 14 pp × $1,414.5M", "FY2028 run-rate", True, A_PR + A_S28)
D("vfdrop", "Change in vendor funding of promotional markdowns, FY2023–25", "pp", "(vf25 - vf23) * 100", "(46% − 55%) × 100", "FY2023–25")
D("expup", "Rise in customers who say Harlow is more expensive, FY2023–25", "pp", "(exp25 - exp23) * 100", "(41% − 33%) × 100", "FY2023–25")
D("compgap", "Comparable-sales gap of stores near ValuMart against other stores", "pp", "(compnear - compother) * 100",
  "(−4.2% − 1.1%) × 100", "FY2025")
D("plpace", "Private-label share gain per year, FY2023–25", "pp", "(pl25 - pl23) / 2 * 100", "(18.5% − 17.0%) ÷ 2 years", "FY2023–25")
A_PL = ["Private-label share keeps its FY2023–25 pace of 0.75 percentage points a year for three more years, to about 20.8% of sales",
        "The 12 percentage-point margin premium over national brands holds",
        "Applied to FY2028 sales at FY2025 prices of $1,414.5M"]
D("pl28", "Private-label share of sales in FY2028 at the FY2023–25 pace", "%", "pl25 + (pl25 - pl23) / 2 * 3",
  "18.5% + 0.75 pp × 3 years", "FY2028", True, A_PL)
D("plup", "Private-label share gain FY2025–28 at the FY2023–25 pace", "pp", "(pl25 - pl23) / 2 * 3 * 100",
  "0.75 pp × 3 years", "FY2025–28", True, A_PL)
D("plfix", "Operating income from private label keeping its pace", "$M", "(pl25 - pl23) / 2 * 3 * 100 * plgap / 10000 * sales28",
  "2.25 pp × 12 pp × $1,414.5M", "FY2028 run-rate", True, A_PL + A_S28)

# ================================================================ e-commerce
D("ecsales25", "E-commerce sales, FY2025", "$M", "ord25 * bask25 / 1000", "1,331k orders × $96", "FY2025")
D("ecfx", "Growth in e-commerce fulfillment cost, FY2023–25", "x", "ecf25 / ecf23", "18.1 ÷ 5.2", "FY2023–25")
D("ordx", "Growth in e-commerce orders, FY2023–25", "x", "ord25 / ord23", "1,331 ÷ 453", "FY2023–25")
for y in ("23", "24", "25"):
    D(f"delord{y}", f"Delivered orders, FY20{y}", "k", f"ord{y} * del{y}", f"orders × delivered share", f"FY20{y}")
    D(f"pickc{y}", f"Picking cost, FY20{y}", "$M", f"ord{y} * pick{y} / 1000", "orders × picking cost per order", f"FY20{y}")
    D(f"delc{y}", f"Third-party delivery cost, FY20{y}", "$M", f"ord{y} * del{y} * dcost{y} / 1000", "delivered orders × cost per delivery", f"FY20{y}")
    D(f"feec{y}", f"Delivery fees collected, FY20{y}", "$M", f"ord{y} * del{y} * fee{y} / 1000", "delivered orders × fee per delivery", f"FY20{y}")
    D(f"fulfc{y}", f"Net fulfillment cost rebuilt from operating data, FY20{y}", "$M",
      f"ord{y} * pick{y} / 1000 + ord{y} * del{y} * (dcost{y} - fee{y}) / 1000", "picking + delivery − fees", f"FY20{y}")
D("ccord25", "Click-and-collect orders, FY2025", "k", "ord25 * (1 - del25)", "1,331k × 42%", "FY2025")
D("newshare", "Share of e-commerce sales new to Harlow", "%", "1 - cannib", "1 − 70%", "FY2025")
D("cpo", "Contribution from new sales per e-commerce order", "$", "bask25 * (1 - cannib) * newc", "$96 × 30% × 20%", "FY2025")
D("netdel", "Result per home delivery after crediting new sales", "$", "bask25 * (1 - cannib) * newc - pick25 - dcost25 + fee25",
  "5.76 − 7.40 − 13.80 + 3.10", "FY2025")
D("netcc", "Result per click-and-collect order after crediting new sales", "$", "bask25 * (1 - cannib) * newc - pick25",
  "5.76 − 7.40", "FY2025")
D("netdel2", "Result per home delivery at the tested fee", "$", "bask25 * (1 - cannib) * newc - pick25 - dcost25 + tfee",
  "5.76 − 7.40 − 13.80 + 6.40", "late FY2025")
D("shiftgain", "Gain from moving one order from home delivery to click-and-collect", "$", "dcost25 - fee25", "13.80 − 3.10", "FY2025")
A_EC = ["Only 30% of e-commerce sales are new to Harlow: 70% of what customers buy online they say they would otherwise buy in a Harlow store (survey, n = 2,300)",
        "A new dollar earns 20 cents of contribution before fulfillment (finance estimate); moved sales earn what they would have earned in store",
        "Fulfillment of $18.1M includes third-party delivery net of fees, which the team's 6.1% figure leaves out"]
D("ecnew", "E-commerce sales new to Harlow", "$M", "ord25 * bask25 / 1000 * (1 - cannib)", "127.8 × 30%", "FY2025")
D("ecnet", "Operating income effect of e-commerce, counted in full", "$M", "ord25 * bask25 / 1000 * (1 - cannib) * newc - ecf25",
  "127.8 × 30% × 20% − 18.1", "FY2025", True, A_EC)
D("teamclaim", "E-commerce contribution as the e-commerce team reports it", "$M", "ecteam * ord25 * bask25 / 1000", "6.1% × 127.8", "FY2025")
D("bkeven", "Break-even share of new sales for e-commerce", "%",
  "ecf25 / (ord25 * bask25 / 1000 * newc)", "18.1 ÷ (127.8 × 20%)", "FY2025", rnd=2)
A_FT = ["The 4-store, 10-week test response holds in all 58 stores: 9% fewer deliveries, 14% more collections, 2% less e-commerce sales, $6.40 fee",
        "Picking ($7.40) and third-party delivery ($13.80) cost per order stay at FY2025 levels",
        "Lost sales lose 20 cents of contribution only on the 30% that is new to Harlow"]
D("fulf2", "Net fulfillment cost after rolling out the tested fees", "$M",
  "ord25 * (del25 * (1 + tdel) + (1 - del25) * (1 + tcc)) * pick25 / 1000 + ord25 * del25 * (1 + tdel) * (dcost25 - tfee) / 1000",
  "orders after test × $7.40 + deliveries after test × ($13.80 − $6.40)", "FY2028 run-rate", True, A_FT)
D("lostc", "Contribution lost on e-commerce sales that go after the fee rise", "$M",
  "0 - tsales * ord25 * bask25 / 1000 * (1 - cannib) * newc", "2% × 127.8 × 30% × 20%", "FY2028 run-rate", True, A_FT)
D("feegain", "Operating income from rolling out the tested delivery fees", "$M", "ecf25 - fulf2 - lostc",
  "18.1 − 15.1 − 0.15", "FY2028 run-rate", True, A_FT)
D("feex", "Fee collected per delivery in the test relative to FY2025", "x", "tfee / fee25", "6.40 ÷ 3.10", "late FY2025")
D("dcrisk", "Cost of accepting the proposed 3% delivery rate rise", "$M", "ord25 * del25 * dcost25 / 1000 * dcrise",
  "10.7 × 3%", "a year", True, ["Applied to FY2025 delivered orders and cost per delivery"])

# ================================================================ plan
A_PLAN = ["Each move is sized in its section (2c, 2d, 3b, 3c, 4b) at FY2025 prices", "The moves do not overlap: promotions, private label and shrink act on different parts of gross margin"] + A_S28
D("levtot", "Operating income added by the five moves", "$M", "promofix + plfix + shrfix + feegain + closeall",
  "9.9 + 3.8 + 4.2 + 2.8 + 6.6", "FY2028 run-rate", True, A_PLAN)
D("oi28", "FY2028 operating income with the five moves, at FY2025 prices", "$M", "oi25 + promofix + plfix + shrfix + feegain + closeall", "15.3 + 27.4", "FY2028", True, A_PLAN)
D("om28", "FY2028 operating margin with the five moves, at FY2025 prices", "%", "(oi25 + promofix + plfix + shrfix + feegain + closeall) / sales28", "42.7 ÷ 1,414.5", "FY2028", True, A_PLAN)
A_W = ["The 2027 minimum-wage rise of 4% reaches every hourly wage, an upper bound since many staff earn above the minimum",
       "No price increase recovers it"]
D("wagehw", "Upper bound of the cost of the 2027 minimum-wage rise", "$M", "minw * lab25", "4% × 181.9", "a year", True, A_W)
D("omw", "FY2028 operating margin if the 2027 wage rise reaches every wage", "%", "(oi25 + levtot - wagehw) / sales28",
  "(42.7 − 7.3) ÷ 1,414.5", "FY2028", True, A_PLAN + A_W)
A_R = ["Shrink falls to FY2023's 2.1% of sales rather than 2.3%", "Best-staffed (Q4) stores cut hours by 8% once shrink holds; they carry a quarter of store labor"]
D("resshr", "Operating income from shrink falling to 2.1% instead of 2.3%", "$M", "(q4 - shr23) * sales28", "0.2 pp × 1,414.5", "FY2028 run-rate", True, A_R + A_S28)
D("resq4", "Operating income from an 8% hours cut in the best-staffed quartile", "$M", "mgcut * lab25 / 4", "8% × 181.9 ÷ 4", "FY2028 run-rate", True, A_R)
D("res", "Operating income from the two reserve moves", "$M", "resshr + resq4", "2.8 + 3.6", "FY2028 run-rate", True, A_R)
D("rescov", "Share of the wage-rise upper bound the reserves cover", "%", "res / wagehw", "6.5 ÷ 7.3", "FY2028", True, A_R + A_W, rnd=2)
D("omwr", "FY2028 operating margin with the wage rise and both reserves", "%", "(oi25 + levtot - wagehw + res) / sales28",
  "(42.7 − 7.3 + 6.5) ÷ 1,414.5", "FY2028", True, A_PLAN + A_W + A_R)
D("wave1", "Run-rate operating income of the three first-wave moves", "$M", "promofix + feegain + shrfix", "9.9 + 2.8 + 4.2",
  "run-rate", True, ["Promotions reset, tested delivery fees and hours rebalancing, at full run-rate"] + A_S28)
D("covx", "First-wave run-rate as a multiple of the FY2026 covenant need", "x", "wave1 / covneed", "17.0 ÷ 4.7", "FY2026", True,
  ["Promotions reset, tested delivery fees and hours rebalancing, at full run-rate"])
D("capshare", "Share of the $25M plan budget used by the known exit cost", "%", "exitcost / capcap", "7.5 ÷ 25", "FY2026–28")
D("caphead", "Plan budget left after the known exit cost", "$M", "capcap - exitcost", "25 − 7.5", "FY2026–28")

D("plgain", "Private-label share gain, FY2023–25", "pp", "(pl25 - pl23) * 100", "(18.5% − 17.0%) × 100", "FY2023–25")
D("promopp", "Gross-margin effect of the promotion mix, in percentage points", "pp", "(promo25 - promo23) * promogap / 100", "5 pp × 14 pp", "FY2023–25")
D("wasteadmin", "Share of shrink from produce waste and receiving errors", "%", "waste + admin", "45% + 20%", "FY2025")
