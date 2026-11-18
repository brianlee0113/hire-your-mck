"""Data points for the Harlow margin deck. Pack facts (s1), analysis assumptions (s2), derived (s3)."""
import ast, operator, re

DP = {}      # id -> data point
ORDER = []

def _eval(expr):
    e = expr.replace("−", "-").replace("×", "*").replace("÷", "/")
    ids = sorted(DP, key=len, reverse=True)
    env = {}
    for k, i in enumerate(ids):
        e2 = re.sub(rf"(?<![\w.]){re.escape(i)}(?![\w-])", f"_v{k}", e)
        if e2 != e:
            env[f"_v{k}"] = (DP[i]["value"], i); e = e2
    used = []
    ops = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}
    def ev(n):
        if isinstance(n, ast.Expression): return ev(n.body)
        if isinstance(n, ast.BinOp): return ops[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub): return -ev(n.operand)
        if isinstance(n, ast.Constant): return n.value
        if isinstance(n, ast.Name):
            v, i = env[n.id]; used.append(i); return v
        raise ValueError(expr)
    return ev(ast.parse(e, mode="eval")), list(dict.fromkeys(used))

def _add(d):
    assert d["id"] not in DP, d["id"]
    DP[d["id"]] = d; ORDER.append(d["id"])
    return d["id"]

def pk(id, label, value, unit, excerpt, locator, period=None, **kw):
    d = {"id": id, "slide_id": kw.pop("slide", "3"), "label": label, "value": value, "unit": unit,
         "source_id": "s1", "excerpt": excerpt, "locator": locator}
    if period: d["period"] = period
    d.update(kw)
    return _add(d)

def an(id, label, value, unit, excerpt, locator, est=False, assumptions=None, **kw):
    """A number the analysis states (assumption, target or estimate) that is not in the pack."""
    d = {"id": id, "slide_id": kw.pop("slide", "3"), "label": label, "value": value, "unit": unit,
         "source_id": "s2", "excerpt": excerpt, "locator": locator}
    if est:
        d["estimate"] = True
        d["calc"] = kw.pop("calc", repr(value))
        d["assumptions"] = assumptions or ["Team assumption stated in the source analysis (" + locator + "); not in the briefing pack"]
    d.update(kw)
    return _add(d)

def _tol(v):
    return max(0.011, abs(v) * 0.01)

def dv(id, label, unit, calc, show=None, formula=None, est=False, assumptions=None, vh=None, **kw):
    exact, used = _eval(calc)
    if show is not None:
        if abs(show - exact) <= _tol(show) * 0.98:
            val = show
        else:
            print(f"note: {id} show {show} outside tolerance of {exact:.4f}; stored exact")
            val = round(exact, 6 if unit == "%" else 4)
    else:
        val = round(exact, 6 if unit == "%" else 4)
    d = {"id": id, "slide_id": kw.pop("slide", "3"), "label": label, "value": val, "unit": unit,
         "source_id": "s3", "derived_from": used, "formula": formula or calc, "calc": calc}
    if vh is not None:
        d["value_high"] = vh
    if est:
        d["estimate"] = True
    if assumptions:
        d["assumptions"] = assumptions
    d.update(kw)
    return _add(d)

T1 = "Table 1 (income statement)"
# ---------------------------------------------------------------- pack: Table 1
for row, key, vals in [("Sales", "sales", (1420.0, 1468.0, 1503.0)), ("Gross profit", "gp", (369.8, 376.0, 376.1)),
                       ("Store labor", "lab", (167.6, 176.2, 181.9)), ("Occupancy and energy", "occ", (82.4, 86.6, 90.2)),
                       ("E-commerce fulfillment (picking + delivery, net of delivery fees)", "ecf", (5.2, 10.9, 18.1)),
                       ("Other SG&A", "sga", (66.7, 69.0, 70.6)), ("Operating income", "oi", (47.9, 33.4, 15.3))]:
    for fy, v in zip(("23", "24", "25"), vals):
        pk(f"{key}{fy}", f"{row.split(' (')[0]}, FY20{fy}", v, "$M", f'Table 1, "{row}": FY20{fy} = "{v:,.1f}"', T1, f"FY20{fy}")
for fy, v in zip(("23", "24", "25"), (0.0337, 0.0227, 0.0102)):
    pk(f"om{fy}", f"Operating margin, FY20{fy}", v, "%", f'Table 1, "Operating margin": FY20{fy} = "{v*100:.2f}%"', T1, f"FY20{fy}")
# Table 2
for row, key, vals in [("Promotional sales, share of sales", "promo", (0.24, 0.262, 0.29)),
                       ("Private-label sales, share of sales", "pl", (0.17, 0.177, 0.185)),
                       ("Shrink, % of sales", "shr", (0.021, 0.023, 0.026))]:
    for fy, v in zip(("23", "24", "25"), vals):
        pk(f"{key}{fy}", f"{row}, FY20{fy}", v, "%", f'Table 2, "{row}": FY20{fy} = "{v*100:.1f}%"', "Table 2 (gross-margin drivers)", f"FY20{fy}")
pk("promo_gap", "Gross-margin gap of promotional vs. regular-price sales", 14, "pp",
   "Promotional sales earn 14 percentage points less gross margin than regular-price sales (unchanged over the period).", "§5, Table 2 notes")
pk("pl_gap", "Gross-margin premium of private label vs. national brands", 12, "pp",
   "Private-label sales earn 12 percentage points more gross margin than national brands (unchanged).", "§5, Table 2 notes")
pk("vf23", "Vendor funding of promotional markdowns, FY2023", 0.55, "%",
   "Vendor funding covered 55% of promotional markdowns in FY2023 and 46% in FY2025.", "§5, Table 2 notes", "FY2023")
pk("vf25", "Vendor funding of promotional markdowns, FY2025", 0.46, "%",
   "Vendor funding covered 55% of promotional markdowns in FY2023 and 46% in FY2025.", "§5, Table 2 notes", "FY2025")
pk("ev_loss", "Share of FY2025 promotional events that lost money", 0.38, "%",
   "A post-event review of FY2025 promotions found that 38% of events lost money after counting the extra units they sold.", "§5, Table 2 notes", "FY2025")
# Table 3-4
pk("wage23", "Average hourly wage incl. benefits, FY2023", 16.80, "$", 'Table 3, "Average hourly wage incl. benefits": FY2023 = "$16.80"', "Table 3 (store labor)", "FY2023")
pk("wage25", "Average hourly wage incl. benefits, FY2025", 18.38, "$", 'Table 3, "Average hourly wage incl. benefits": FY2025 = "$18.38"', "Table 3 (store labor)", "FY2025")
pk("hrs23", "Labor hours per $1,000 of sales, FY2023", 7.02, "hours", 'Table 3, "Labor hours per $1,000 of sales": FY2023 = "7.02"', "Table 3 (store labor)", "FY2023")
pk("hrs25", "Labor hours per $1,000 of sales, FY2025", 6.60, "hours", 'Table 3, "Labor hours per $1,000 of sales": FY2025 = "6.60"', "Table 3 (store labor)", "FY2025")
pk("labp23", "Store labor, % of sales, FY2023", 0.118, "%", 'Table 3, "Store labor, % of sales": FY2023 = "11.8%"', "Table 3 (store labor)", "FY2023")
pk("labp25", "Store labor, % of sales, FY2025", 0.121, "%", 'Table 3, "Store labor, % of sales": FY2025 = "12.1%"', "Table 3 (store labor)", "FY2025")
for q, v in zip(("q1", "q2", "q3", "q4"), (0.031, 0.027, 0.024, 0.023)):
    pk(q, f"Shrink, % of sales, labor-intensity quartile {q.upper()}, FY2025", v, "%",
       f'Table 4, "{q.upper()}": Shrink = "{v*100:.1f}%"', "Table 4 (shrink by labor intensity)", "FY2025")
for k, lab, v in (("waste", "fresh and produce waste", 0.45), ("theft", "theft", 0.35), ("admin", "administrative and receiving errors", 0.20)):
    pk(k, f"Share of FY2025 shrink: {lab}", v, "%",
       "Shrink composition FY2025: fresh and produce waste 45%, theft 35%, administrative and receiving errors 20%.", "§6", "FY2025")
# Table 5
for row, key, vals, unit in [("E-commerce share of sales", "ecs", (0.03, 0.056, 0.085), "%"),
                             ("Orders, thousands", "ord", (453, 865, 1331), "k"),
                             ("Average basket", "bask", (94, 95, 96), "$"),
                             ("Share of orders delivered to the home (rest: click-and-collect)", "dsh", (0.45, 0.52, 0.58), "%"),
                             ("Picking cost per order (all orders)", "pick", (7.20, 7.30, 7.40), "$"),
                             ("Third-party delivery cost per delivered order", "dc", (12.90, 13.40, 13.80), "$"),
                             ("Average delivery fee collected per delivered order", "fee", (3.40, 3.20, 3.10), "$")]:
    for fy, v in zip(("23", "24", "25"), vals):
        shown = f"{v*100:.1f}%".replace(".0%", "%") if unit == "%" else (f"${v:.2f}" if key in ("pick", "dc", "fee") else (f"${v}" if unit == "$" else f"{v:,}"))
        pk(f"{key}{fy}", f"{row}, FY20{fy}", v, unit, f'Table 5, "{row}": FY20{fy} = "{shown}"', "Table 5 (e-commerce)", f"FY20{fy}")
pk("cannib", "Share of online purchases customers would otherwise have bought in a Harlow store", 0.70, "%",
   "Survey of 2,300 e-commerce customers (FY2025): 70% of what they buy online they say they would otherwise have bought in a Harlow store.", "§7")
pk("n_ecsurvey", "E-commerce customer survey sample", 2300, "respondents", "Survey of 2,300 e-commerce customers (FY2025)", "§7")
pk("contrib_c", "Contribution per dollar of sales new to Harlow, before e-commerce fulfillment", 20, "cents",
   "a dollar of sales that is genuinely new to Harlow adds about 20 cents of contribution (gross margin less variable store costs), before e-commerce fulfillment", "§7")
pk("k1000", "Sales denominator of the labor-hours ratio", 1000, "$", 'Table 3, "Labor hours per $1,000 of sales"', "Table 3 (store labor)")
pk("ft_fee", "Fee test: delivery fee", 7.99, "$", "delivery fee raised to $7.99 and the free-delivery threshold to $100", "§7, fee test")
pk("ft_thr", "Fee test: free-delivery threshold", 100, "$", "delivery fee raised to $7.99 and the free-delivery threshold to $100", "§7, fee test")
pk("fee_now", "Current delivery fee below the threshold", 4.99, "$", "Delivery is free above $75 (a $4.99 fee below).", "§7")
pk("thr_now", "Current free-delivery threshold", 75, "$", "Delivery is free above $75 (a $4.99 fee below).", "§7")
FT = "Delivered orders fell 9%, click-and-collect orders rose 14%, total e-commerce sales fell 2%, and the average fee collected per delivered order rose to $6.40."
pk("ft_del", "Fee test: change in delivered orders", -0.09, "%", FT, "§7, fee test")
pk("ft_cnc", "Fee test: change in click-and-collect orders", 0.14, "%", FT, "§7, fee test")
pk("ft_sales", "Fee test: change in total e-commerce sales", -0.02, "%", FT, "§7, fee test")
pk("ft_feecol", "Fee test: average fee collected per delivered order", 6.40, "$", FT, "§7, fee test")
pk("ft_stores", "Fee test: stores in the test", 4, "stores", "Fee test (4 stores, 10 weeks, late FY2025)", "§7, fee test")
pk("ft_weeks", "Fee test: length", 10, "weeks", "Fee test (4 stores, 10 weeks, late FY2025)", "§7, fee test")
# Table 6
T6 = "Table 6 (nine weakest stores)"
pk("weak_n", "Stores with negative four-wall EBITDA", 9, "stores", 'Table 6, "Stores with negative four-wall EBITDA" = "9 of 58"', T6, "FY2025")
pk("stores", "Harlow stores", 58, "stores", "a family-controlled grocery chain with 58 stores in Ohio and Indiana", "§1")
pk("weak_sales", "Combined sales of the nine weakest stores", 118.0, "$M", 'Table 6, "Their combined sales" = "$118.0M"', T6, "FY2025")
pk("weak_ebitda", "Combined four-wall EBITDA of the nine weakest stores", -3.1, "$M", 'Table 6, "Their combined four-wall EBITDA" = "−$3.1M"', T6, "FY2025")
pk("lease6", "Weak stores with leases expiring by end of 2027", 6, "stores", 'Table 6, "Leases expiring by end of 2027" = "6 of the 9"', T6)
pk("exit3_cost", "Estimated lease-exit cost for the other 3 weak stores (one-time)", 7.5, "$M", 'Table 6, "Estimated lease-exit cost for the other 3" = "$7.5M (one-time)"', T6)
pk("move", "Share of a closed store's sales that moves to a nearby Harlow store", 0.25, "%", 'Table 6, "Share of their sales expected to move to a nearby Harlow store if closed (past closures)" = "25%"', T6)
pk("move_c", "Contribution on sales moved to a receiving store", 0.12, "%", 'Table 6, "Contribution on sales moved to a receiving store" = "12%"', T6)
# §9-11
VM = "A discount grocer, ValuMart, has opened 11 stores in Harlow trade areas since 2023. Harlow stores within three miles of a new ValuMart had comparable sales of −4.2% in FY2025, against +1.1% for other Harlow stores."
pk("vm_n", "ValuMart stores opened in Harlow trade areas since 2023", 11, "stores", VM, "§9")
pk("vm_comp", "Comparable sales of Harlow stores within three miles of a new ValuMart, FY2025", -0.042, "%", VM, "§9", "FY2025")
pk("oth_comp", "Comparable sales of other Harlow stores, FY2025", 0.011, "%", VM, "§9", "FY2025")
SV = 'Customer survey (n = 3,100): 41% say Harlow is "more expensive than other options" (FY2023: 33%); top reasons to shop Harlow are fresh produce (58%) and convenience (44%).'
pk("exp25", "Customers who say Harlow is more expensive than other options, latest survey", 0.41, "%", SV, "§9")
pk("exp23", "Customers who say Harlow is more expensive than other options, FY2023", 0.33, "%", SV, "§9", "FY2023")
pk("fresh", "Customers citing fresh produce as a top reason to shop Harlow", 0.58, "%", SV, "§9")
pk("conv", "Customers citing convenience as a top reason to shop Harlow", 0.44, "%", SV, "§9")
pk("n_survey", "Customer survey sample", 3100, "respondents", SV, "§9")
pk("ec_claim", "E-commerce team's reported contribution margin, FY2025", 0.061, "%",
   'E-commerce team update: "E-commerce is profitable: a contribution margin of 6.1% of e-commerce sales in FY2025."', "§10")
CT = 'Category team: "Stores with the deepest promotions in FY2025 grew comparable sales 1.8%, against 0.2% for the rest. Promotions work."'
pk("deep_comp", "Comparable sales growth of the deepest-promotion stores, FY2025", 0.018, "%", CT, "§10")
pk("rest_comp", "Comparable sales growth of the other stores, FY2025", 0.002, "%", CT, "§10")
pk("rate_rise", "Third-party delivery rate rise proposed for the 2026 renewal", 0.03, "%",
   "Whether third-party delivery rates can be renegotiated (contract renews in 2026; the provider proposed a 3% rise).", "§11")
pk("wage27", "State minimum-wage rise in 2027", 0.04, "%", "Wage rates: the state minimum wage rises again in 2027 (+4%).", "§11")
pk("tgt", "Operating-margin target, FY2028", 0.03, "%", "Target: operating margin back to at least 3.0% by FY2028.", "§3", "FY2028")
pk("cap", "Cap on one-time cost or capital, FY2026–FY2028", 25, "$M", "Capital: at most $25M of one-time cost or capital for the plan over FY2026–FY2028.", "§3")
pk("cov", "Lender covenant: minimum operating income, FY2026", 20, "$M", "a covenant requires operating income of at least $20M in FY2026", "§3", "FY2026")
pk("cut", "Management's draft cut in scheduled store labor hours", 0.08, "%", "cut scheduled store labor hours by 8% in FY2026", "§4", "FY2026")
pk("cut_save", "Management's estimated saving from the 8% hours cut", 14.5, "$M", "they estimate about $14.5M a year of savings", "§4")

# ---------------------------------------------------------------- analysis assumptions and targets (s2)
an("promo_tgt", "Plan target: promotional share of sales", 0.25, "%", "1. Promotion reset: drop loss-making events, promo share 29% → 25%", "source deck p.12", True)
an("lostvol", "Allowance for volume lost when promotions are cut", 0.25, "%", "4 pts × 14 pts × $1,444M = $8.1M, less 25% for lost volume", "source deck p.12", True,
   ["Team estimate stated in the source analysis (p.12, A4: '25% lost-volume allowance on the promotion reset'); not in the briefing pack"])
an("vf_tgt", "Plan target: vendor funding of markdowns", 0.50, "%", "2. Vendor funding of markdowns 46% → 50%", "source deck p.12", True)
an("pl_tgt", "Plan target: private-label share of sales", 0.21, "%", "3. Private label share 18.5% → 21%", "source deck p.12", True)
an("shr_tgt", "Plan target: shrink, % of sales", 0.023, "%", "4. Shrink 2.6% → 2.3%, hours reinvested in lean stores", "source deck p.12", True)
an("hrs_cost", "Cost of hours reinvested in lean stores, a year", 1.5, "$M", "0.3 pts × $1,444M = $4.3M, less $1.5M of added hours", "source deck p.12", True)
an("hrs_cut", "Targeted cut in store hours (high-labor stores), share of the labor bill", 0.03, "%", "5. Targeted rebalancing: −3% hours in high-labour stores", "source deck p.12", True)
an("cut5", "Target reduction in the third-party delivery rate at renewal", 0.05, "%", "Target a 5% reduction on the smaller volume ($0.5M)", "source deck p.13", True)
an("share6", "Share of the nine weak stores' sales and EBITDA carried by the six lease-expiry stores", 0.6667, "%",
   "The nine stores' sales and EBITDA are split pro rata (6/9, 3/9) because the pack gives only totals", "source deck p.14", True,
   ["The pack gives only totals for the nine stores; the analysis splits them pro rata by store count (6/9 and 3/9)"], calc="6 / 9")
an("clo_per", "Closure-cost allowance per lease-expiry store (one-time)", 0.5, "$M", "~3.0 (allowance, $0.5M/store)", "source deck p.14", True)
an("sh_pp_hi", "Added shrink from the 8% hours cut, high case", 50, "bps", "Shrink effect: +0.25 to +0.50 pts of sales (midpoint shown)", "source deck p.10", True)
an("sh_pp", "Added shrink from the 8% hours cut", 25, "bps", "Shrink effect: +0.25 to +0.50 pts of sales (midpoint shown)", "source deck p.10", True,
   ["Moves the average store halfway (+0.25 pp) to fully (+0.50 pp) onto the leanest quartile's 3.1% shrink (source deck p.10)"])
DP["sh_pp"]["value_high"] = 50
an("ph_promo", "FY2026 in-year phasing of the promotion reset", 0.5, "%", "FY2026 in-year phasing (team assumption): promotions 50%, vendor funding 25%, delivery 75%, labour 50%, private label ~25% of run-rate", "source deck p.16", True)
an("ph_vf", "FY2026 in-year phasing of vendor funding", 0.25, "%", "FY2026 in-year phasing (team assumption): promotions 50%, vendor funding 25%, delivery 75%, labour 50%, private label ~25% of run-rate", "source deck p.16", True)
an("ph_del", "FY2026 in-year phasing of delivery pricing", 0.75, "%", "FY2026 in-year phasing (team assumption): promotions 50%, vendor funding 25%, delivery 75%, labour 50%, private label ~25% of run-rate", "source deck p.16", True)
an("ph_lab", "FY2026 in-year phasing of targeted labor", 0.5, "%", "FY2026 in-year phasing (team assumption): promotions 50%, vendor funding 25%, delivery 75%, labour 50%, private label ~25% of run-rate", "source deck p.16", True)
an("pl26", "FY2026 in-year gain from the private-label push", 1.0, "$M", 'p.16 chart "Private-label trend" = "+1.0"; A3 "3. Private label", FY2026 in-year = "1.0"', "source deck p.16, p.23", True,
   ["Source deck: about 25% of the lever's run-rate in FY2026; the analysis shows +$1.0M (25% of the $4.5M FY2025-scale run-rate would be about $1.1M)"])
an("w_del", "Second wave: cost-recovery delivery pricing or membership", 3.0, "$M", "Cost-recovery delivery pricing or membership (pilot first) - 3.0", "source deck p.15", True,
   ["Source deck p.13: 'Next test (wave 2): ~$3M'; halving the remaining ~$6.4M delivery loss is worth ~$3.2M, which the analysis rounds to ~$3M"])
an("l7_lo", "Exit of 6 stores, low case (the 6 carry less of the loss)", 3.0, "$M", "7. Exit 6 stores - Less loss in the 6 - 3.0 - 4.4 - 5.0 - More loss in the 6", "source deck p.23", True)
an("l7_hi", "Exit of 6 stores, high case (the 6 carry more of the loss)", 5.0, "$M", "7. Exit 6 stores - Less loss in the 6 - 3.0 - 4.4 - 5.0 - More loss in the 6", "source deck p.23", True)
for k, lab, v in (("al_tools", "Labor scheduling and shrink tools, training", 3.0), ("al_pl", "Private-label range development", 2.0),
                  ("al_promo", "Promotion analytics and vendor negotiation", 1.0), ("al_del", "Delivery pricing changes and pilot", 0.5)):
    an(k, f"One-time cost allowance: {lab}", v, "$M", f'p.17 table, "{lab}" = "{v}" (Allowance)', "source deck p.17", True,
       ["Team planning allowance in the source analysis, for the CFO to validate; only the $7.5M lease-exit cost comes from the pack"])
an("optC", "Option C (margin-first, click-and-collect only): FY2028 operating income on firm levers", 42.9, "$M",
   "~3.0% on firm levers ($42.9M)", "source deck p.11")
an("switch40", "Option C: share of home-delivery customers who switch to click-and-collect", 0.40, "%",
   "Option C assumes 40% of home-delivery customers switch to click-and-collect", "source deck p.11", True)
an("chk", "Mid-FY2027 checkpoint: run-rate operating margin that triggers the second wave", 0.024, "%",
   "Mid-FY2027 checkpoint: if run-rate margin is below ~2.4%, trigger the second wave in full and put the fallback (C) to the owners", "source deck p.16")
an("pilot_n", "Stores in the shrink pilot", 10, "stores", "Shrink programme to 2.3%; pilot in 10 stores first", "source deck p.16")
an("pilot_gate", "Shrink pilot gain needed before scaling", 0.2, "pp", "Scale only if pilot gains ≥ 0.2 pts", "source deck p.18")
an("del_tgt", "Scorecard target: loss per delivered order, FY2028", 5, "$", "Loss per delivered order - $12.34 → < $5", "source deck p.19")
an("days90", "First-moves window", 90, "days", "Four no-regret moves in the next 90 days", "source deck p.16")
an("traffic50", "Sensitivity: share of the promotion reset's gross gain lost to traffic", 0.5, "%", "Traffic response to fewer promotions (ValuMart) - 25% of gross gain lost - 50% lost - −$2.0M", "source deck p.18")
an("new50", "Sensitivity: share of e-commerce sales new to Harlow", 0.5, "%", "Share of e-commerce sales new to Harlow (survey) - 30% - 50% - Loss shrinks to −$5.3M", "source deck p.18")
an("shr_alt", "Sensitivity: shrink reached with reinvested hours", 0.0245, "%", "Shrink responds to reinvested hours - 2.6% → 2.3% - Only 2.45% - −$2.1M", "source deck p.18")
an("wage_alt", "Sensitivity: 2027 wage step", 0.06, "%", "2027 wage step - +4% on full bill - +6% - −$3.6M", "source deck p.18")
for k, lab, v, ex in (("p1_lo", "Promotion reset, low case: cut in promo share", 2, "Promo share −2 pts"), ("p1_hi", "Promotion reset, high case: cut in promo share", 5, "−5 pts (FY2023 level)"),
                      ("vf_lo", "Vendor funding, low case", 0.48, "To 48%"), ("pl_lo", "Private label, low case", 0.20, "To 20.0%"), ("pl_hi", "Private label, high case", 0.22, "To 22.0%"),
                      ("sh_lo", "Shrink cut, low case", 0.15, "−0.15 pts"), ("sh_hi", "Shrink cut, high case", 0.40, "−0.40 pts"),
                      ("hc_lo", "Targeted hours cut, low case", 0.02, "−2% hours"), ("hc_hi", "Targeted hours cut, high case", 0.04, "−4% hours"),
                      ("ft_lo", "Delivery pricing, low case: test result less", 0.20, "Test result − 20%; no contract gain"), ("ft_hi", "Delivery pricing, high case: test result plus", 0.30, "Test +30%; contract −5%")):
    an(k, lab, v, "%" if v < 1 else "pp", f"A3: {ex}", "source deck p.23", True)
