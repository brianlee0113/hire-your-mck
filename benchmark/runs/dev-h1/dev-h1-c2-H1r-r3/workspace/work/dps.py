"""Data points for the Harlow margin deck. P = briefing pack (s1), A = finished analysis (s2), D = derived (s3)."""
import re

DPS = {}
ORDER = []


def _add(d):
    assert d["id"] not in DPS, d["id"]
    DPS[d["id"]] = d
    ORDER.append(d["id"])
    return d["id"]


def P(id, label, value, unit, period, excerpt, locator, **kw):
    """Number read from the briefing pack."""
    return _add(dict(id=id, label=label, value=value, unit=unit, period=period, source_id="s1",
                     excerpt=excerpt, locator=locator, **kw))


def A(id, label, value, unit, excerpt, locator, assumption, period="FY2026–FY2028 plan"):
    """An assumption or estimate stated in the finished analysis (team assumption, not in the pack)."""
    return _add(dict(id=id, label=label, value=value, unit=unit, period=period, source_id="s2", excerpt=excerpt,
                     locator=locator, estimate=True, calc=repr(value), assumptions=[assumption]))


def _ev(calc):
    e = calc
    for i in sorted(DPS, key=len, reverse=True):
        e = re.sub(rf"(?<![\w.]){re.escape(i)}(?![\w-])", f"DPS['{i}']['value']", e)
    return eval(e)


def D(id, label, unit, calc, formula, period="FY2025", **kw):
    ids = [i for i in sorted(DPS, key=len, reverse=True) if re.search(rf"(?<![\w.]){re.escape(i)}(?![\w-])", calc)]
    v = _ev(calc)
    d = dict(id=id, label=label, value=round(v, 6), unit=unit, period=period, source_id="s3",
             derived_from=sorted(set(ids), key=lambda x: ORDER.index(x)), formula=formula, calc=calc, **kw)
    return _add(d)


T1 = "Briefing pack §5, Table 1 (income statement)"
T2 = "Briefing pack §5, Table 2 (gross-margin drivers)"
T3 = "Briefing pack §6, Table 3 (store labor)"
T5 = "Briefing pack §7, Table 5 (e-commerce operating data)"
T6 = "Briefing pack §8, Table 6 (nine weakest stores)"

# ---------------- briefing pack: income statement
for yr, s, gp, lab, occ, ecf, sga, oi in [("FY2023", "1,420.0", "369.8", "167.6", "82.4", "5.2", "66.7", "47.9"),
                                          ("FY2024", "1,468.0", "376.0", "176.2", "86.6", "10.9", "69.0", "33.4"),
                                          ("FY2025", "1,503.0", "376.1", "181.9", "90.2", "18.1", "70.6", "15.3")]:
    y = yr[-2:]
    P(f"sales{y}", f"Sales, {yr}", float(s.replace(",", "")), "$M", yr, f'"Sales" row, column {yr} = "{s}"', T1)
    P(f"gp{y}", f"Gross profit, {yr}", float(gp), "$M", yr, f'"Gross profit" row, column {yr} = "{gp}"', T1)
    P(f"lab{y}", f"Store labor cost, {yr}", float(lab), "$M", yr, f'"Store labor" row, column {yr} = "{lab}"', T1)
    P(f"occ{y}", f"Occupancy and energy cost, {yr}", float(occ), "$M", yr, f'"Occupancy and energy" row, column {yr} = "{occ}"', T1)
    P(f"ecf{y}", f"E-commerce fulfillment cost, net of delivery fees, {yr}", float(ecf), "$M", yr,
      f'"E-commerce fulfillment (picking + delivery, net of delivery fees)" row, column {yr} = "{ecf}"', T1)
    P(f"sga{y}", f"Other SG&A, {yr}", float(sga), "$M", yr, f'"Other SG&A" row, column {yr} = "{sga}"', T1)
    P(f"oi{y}", f"Operating income, {yr}", float(oi), "$M", yr, f'"Operating income" row, column {yr} = "{oi}"', T1)
P("om23", "Operating margin, FY2023", 0.0337, "%", "FY2023", '"Operating margin" row, column FY2023 = "3.37%"', T1)
P("om24", "Operating margin, FY2024", 0.0227, "%", "FY2024", '"Operating margin" row, column FY2024 = "2.27%"', T1)
P("om25", "Operating margin, FY2025", 0.0102, "%", "FY2025", '"Operating margin" row, column FY2025 = "1.02%"', T1)

# ---------------- gross-margin drivers
P("promo23", "Promotional sales, share of sales, FY2023", 0.24, "%", "FY2023", '"Promotional sales, share of sales" row, column FY2023 = "24.0%"', T2)
P("promo25", "Promotional sales, share of sales, FY2025", 0.29, "%", "FY2025", '"Promotional sales, share of sales" row, column FY2025 = "29.0%"', T2)
P("pl23", "Private-label sales, share of sales, FY2023", 0.17, "%", "FY2023", '"Private-label sales, share of sales" row, column FY2023 = "17.0%"', T2)
P("pl25", "Private-label sales, share of sales, FY2025", 0.185, "%", "FY2025", '"Private-label sales, share of sales" row, column FY2025 = "18.5%"', T2)
P("shr23", "Shrink, % of sales, FY2023", 0.021, "%", "FY2023", '"Shrink, % of sales" row, column FY2023 = "2.1%"', T2)
P("shr25", "Shrink, % of sales, FY2025", 0.026, "%", "FY2025", '"Shrink, % of sales" row, column FY2025 = "2.6%"', T2)
P("promogap", "Gross-margin gap of promotional against regular-price sales", 14, "pp", "FY2023–FY2025",
  "Promotional sales earn 14 percentage points less gross margin than regular-price sales (unchanged over the period).", "Briefing pack §5, note under Table 2")
P("plgap", "Gross-margin premium of private label over national brands", 12, "pp", "FY2023–FY2025",
  "Private-label sales earn 12 percentage points more gross margin than national brands (unchanged).", "Briefing pack §5, note under Table 2")
P("vf23", "Share of promotional markdowns funded by vendors, FY2023", 0.55, "%", "FY2023",
  "Vendor funding covered 55% of promotional markdowns in FY2023 and 46% in FY2025.", "Briefing pack §5, note under Table 2")
P("vf25", "Share of promotional markdowns funded by vendors, FY2025", 0.46, "%", "FY2025",
  "Vendor funding covered 55% of promotional markdowns in FY2023 and 46% in FY2025.", "Briefing pack §5, note under Table 2")
P("loss38", "Share of FY2025 promotional events that lost money after counting extra units", 0.38, "%", "FY2025",
  "A post-event review of FY2025 promotions found that 38% of events lost money after counting the extra units they sold.", "Briefing pack §5, note under Table 2")

# ---------------- labor and shrink
P("wage23", "Average hourly wage incl. benefits, FY2023", 16.80, "$", "FY2023", '"Average hourly wage incl. benefits" row, column FY2023 = "$16.80"', T3)
P("wage25", "Average hourly wage incl. benefits, FY2025", 18.38, "$", "FY2025", '"Average hourly wage incl. benefits" row, column FY2025 = "$18.38"', T3)
P("hrs23", "Labor hours per $1,000 of sales, FY2023", 7.02, "hours", "FY2023", '"Labor hours per $1,000 of sales" row, column FY2023 = "7.02"', T3)
P("hrs25", "Labor hours per $1,000 of sales, FY2025", 6.60, "hours", "FY2025", '"Labor hours per $1,000 of sales" row, column FY2025 = "6.60"', T3)
P("labpct23", "Store labor, % of sales, FY2023", 0.118, "%", "FY2023", '"Store labor, % of sales" row, column FY2023 = "11.8%"', T3)
for q, v, lab in [("q1", 0.031, "Q1 (fewest labor hours per $ sales)"), ("q2", 0.027, "Q2"), ("q3", 0.024, "Q3"), ("q4", 0.023, "Q4 (most)")]:
    P(q, f"Shrink, % of sales, stores in labor-intensity quartile {q.upper()}", v, "%", "FY2025", f'"{lab}" row, "Shrink, % of sales" = "{v*100:.1f}%"',
      "Briefing pack §6, Table 4 (shrink by store labor intensity)")
P("waste", "Fresh and produce waste, share of shrink", 0.45, "%", "FY2025",
  "Shrink composition FY2025: fresh and produce waste 45%, theft 35%, administrative and receiving errors 20%.", "Briefing pack §6")
P("theft", "Theft, share of shrink", 0.35, "%", "FY2025",
  "Shrink composition FY2025: fresh and produce waste 45%, theft 35%, administrative and receiving errors 20%.", "Briefing pack §6")
P("admin", "Administrative and receiving errors, share of shrink", 0.20, "%", "FY2025",
  "Shrink composition FY2025: fresh and produce waste 45%, theft 35%, administrative and receiving errors 20%.", "Briefing pack §6")

# ---------------- e-commerce
for yr, o, b, dsh, pk, dc, fe in [("FY2023", "453", "94", "45", "7.20", "12.90", "3.40"), ("FY2024", "865", "95", "52", "7.30", "13.40", "3.20"),
                                  ("FY2025", "1,331", "96", "58", "7.40", "13.80", "3.10")]:
    y = yr[-2:]
    P(f"ord{y}", f"E-commerce orders, {yr}", float(o.replace(",", "")), "thousand orders", yr, f'"Orders, thousands" row, column {yr} = "{o}"', T5)
    P(f"bask{y}", f"Average e-commerce basket, {yr}", float(b), "$", yr, f'"Average basket" row, column {yr} = "${b}"', T5)
    P(f"dsh{y}", f"Share of e-commerce orders delivered to the home, {yr}", int(dsh) / 100, "%", yr,
      f'"Share of orders delivered to the home (rest: click-and-collect)" row, column {yr} = "{dsh}%"', T5)
    P(f"pick{y}", f"Picking cost per order, {yr}", float(pk), "$", yr, f'"Picking cost per order (all orders)" row, column {yr} = "${pk}"', T5)
    P(f"dc{y}", f"Third-party delivery cost per delivered order, {yr}", float(dc), "$", yr,
      f'"Third-party delivery cost per delivered order" row, column {yr} = "${dc}"', T5)
    P(f"fee{y}", f"Average delivery fee collected per delivered order, {yr}", float(fe), "$", yr,
      f'"Average delivery fee collected per delivered order" row, column {yr} = "${fe}"', T5)
P("ecsh25", "E-commerce share of sales, FY2025", 0.085, "%", "FY2025", '"E-commerce share of sales" row, column FY2025 = "8.5%"', T5)
P("surv70", "Share of online purchases customers say they would otherwise have bought in a Harlow store", 0.70, "%", "FY2025",
  "Survey of 2,300 e-commerce customers (FY2025): 70% of what they buy online they say they would otherwise have bought in a Harlow store.", "Briefing pack §7")
P("contrib20", "Contribution per dollar of sales new to Harlow, before e-commerce fulfillment", 20, "cents", "FY2025",
  "Finance estimates that a dollar of sales that is genuinely new to Harlow adds about 20 cents of contribution (gross margin less variable store costs), before e-commerce fulfillment.", "Briefing pack §7")
FT = ("Fee test (4 stores, 10 weeks, late FY2025): delivery fee raised to $7.99 and the free-delivery threshold to $100. Delivered orders fell 9%, "
      "click-and-collect orders rose 14%, total e-commerce sales fell 2%, and the average fee collected per delivered order rose to $6.40.")
P("ft_fee", "Delivery fee in the fee test", 7.99, "$", "late FY2025", FT, "Briefing pack §7, fee test")
P("ft_thr", "Free-delivery threshold in the fee test", 100, "$", "late FY2025", FT, "Briefing pack §7, fee test")
P("ft_del", "Change in delivered orders in the fee test", -0.09, "%", "late FY2025", FT, "Briefing pack §7, fee test")
P("ft_cc", "Change in click-and-collect orders in the fee test", 0.14, "%", "late FY2025", FT, "Briefing pack §7, fee test")
P("ft_sales", "Change in total e-commerce sales in the fee test", -0.02, "%", "late FY2025", FT, "Briefing pack §7, fee test")
P("ft_fpo", "Average fee collected per delivered order in the fee test", 6.40, "$", "late FY2025", FT, "Briefing pack §7, fee test")
P("ecm", "E-commerce contribution margin reported by the e-commerce team", 0.061, "%", "FY2025",
  "E-commerce team update: \"E-commerce is profitable: a contribution margin of 6.1% of e-commerce sales in FY2025.\"", "Briefing pack §10")

# ---------------- stores, customers, constraints
P("s9sales", "Combined sales of the nine stores with negative four-wall EBITDA", 118.0, "$M", "FY2025", '"Their combined sales" = "$118.0M"', T6)
P("s9ebitda", "Combined four-wall EBITDA of the nine weakest stores", -3.1, "$M", "FY2025", '"Their combined four-wall EBITDA" = "−$3.1M"', T6)
P("ls3", "One-time lease-exit cost for the three weak stores with leases beyond 2027", 7.5, "$M", "one-time", '"Estimated lease-exit cost for the other 3" = "$7.5M (one-time)"', T6)
P("mov25", "Share of a closed store's sales that moves to a nearby Harlow store", 0.25, "%", "past closures",
  '"Share of their sales expected to move to a nearby Harlow store if closed (past closures)" = "25%"', T6)
P("mov12", "Contribution on sales moved to a receiving store", 0.12, "%", "past closures", '"Contribution on sales moved to a receiving store" = "12%"', T6)
P("vm11", "ValuMart stores opened in Harlow trade areas since 2023", 11, "stores", "2023–FY2025",
  "A discount grocer, ValuMart, has opened 11 stores in Harlow trade areas since 2023.", "Briefing pack §9")
VMX = "Harlow stores within three miles of a new ValuMart had comparable sales of −4.2% in FY2025, against +1.1% for other Harlow stores."
P("vmc", "Comparable sales, Harlow stores within three miles of a new ValuMart", -0.042, "%", "FY2025", VMX, "Briefing pack §9")
P("vmo", "Comparable sales, other Harlow stores", 0.011, "%", "FY2025", VMX, "Briefing pack §9")
CSX = ("Customer survey (n = 3,100): 41% say Harlow is \"more expensive than other options\" (FY2023: 33%); top reasons to shop Harlow are "
       "fresh produce (58%) and convenience (44%).")
P("exp41", "Customers who say Harlow is more expensive than other options, latest survey", 0.41, "%", "latest survey", CSX, "Briefing pack §9")
P("exp33", "Customers who say Harlow is more expensive than other options, FY2023", 0.33, "%", "FY2023", CSX, "Briefing pack §9")
P("fresh58", "Customers naming fresh produce as a top reason to shop Harlow", 0.58, "%", "latest survey", CSX, "Briefing pack §9")
P("conv44", "Customers naming convenience as a top reason to shop Harlow", 0.44, "%", "latest survey", CSX, "Briefing pack §9")
PCX = "Category team: \"Stores with the deepest promotions in FY2025 grew comparable sales 1.8%, against 0.2% for the rest. Promotions work.\""
P("pcd", "Comparable sales growth, deepest-promotion stores", 0.018, "%", "FY2025", PCX, "Briefing pack §10")
P("pcr", "Comparable sales growth, other stores", 0.002, "%", "FY2025", PCX, "Briefing pack §10")
P("tgtm", "Operating margin target, FY2028", 0.03, "%", "FY2028", "Target: operating margin back to at least 3.0% by FY2028.", "Briefing pack §3")
P("cap", "Cap on one-time cost or capital for the plan, FY2026–FY2028", 25, "$M", "FY2026–FY2028",
  "Capital: at most $25M of one-time cost or capital for the plan over FY2026–FY2028.", "Briefing pack §3")
P("cov", "Lender covenant: minimum operating income in FY2026", 20, "$M", "FY2026",
  "a covenant requires operating income of at least $20M in FY2026.", "Briefing pack §3")
MGX = ("Their draft plan: cut scheduled store labor hours by 8% in FY2026 (they estimate about $14.5M a year of savings) and freeze the "
       "e-commerce service at its current size.")
P("cut8", "Management's draft cut in scheduled store labor hours", 0.08, "%", "FY2026", MGX, "Briefing pack §4")
P("cut145", "Management's estimate of savings from the 8% hours cut", 14.5, "$M", "a year", MGX, "Briefing pack §4")
P("minw", "2027 state minimum-wage rise", 0.04, "%", "2027", "Wage rates: the state minimum wage rises again in 2027 (+4%).", "Briefing pack §11")
P("drise", "Rate rise proposed by the third-party delivery provider", 0.03, "%", "2026 renewal",
  "Whether third-party delivery rates can be renegotiated (contract renews in 2026; the provider proposed a 3% rise).", "Briefing pack §11")

# ---------------- analysis: assumptions and estimates it states (team assumptions, not in the pack)
SL = "Analysis deck"
A("lostvol", "Lost-volume allowance on the promotion reset", 0.25, "%", "4 pts × 14 pts × $1,444M = $8.1M, less 25% for lost volume", f"{SL} p.12, lever 1",
  "Team assumption: a quarter of the gross promotion-reset gain is lost to lower volume")
A("promotgt", "Target promotional share of sales after the reset", 0.25, "%", "1. Promotion reset: drop loss-making events, promo share 29% → 25%", f"{SL} p.12, lever 1",
  "Plan target set in the analysis: promotional share back to 25% of sales by FY2028")
A("vftgt", "Target vendor funding of markdowns (firm lever)", 0.50, "%", "2. Vendor funding of markdowns 46% → 50%", f"{SL} p.12, lever 2",
  "Plan target set in the analysis; FY2023's 55% is the second-wave target")
A("pltgt", "Target private-label share of sales", 0.21, "%", "3. Private label share 18.5% → 21%", f"{SL} p.12, lever 3",
  "Plan target set in the analysis, roughly the +0.75 percentage points a year trend continued")
A("shrtgt", "Target shrink, % of sales", 0.023, "%", "4. Shrink 2.6% → 2.3%, hours reinvested in lean stores", f"{SL} p.12, lever 4",
  "Plan target: the chain reaches the shrink of the best-staffed quartile (2.3%)")
A("reinv", "Cost of hours reinvested in lean stores for shrink", 1.5, "$M", "$1.5M a year of reinvested hours (~78,000 hours, ~1 FTE per lean store)", f"{SL} p.24",
  "Team estimate of the added hours needed to restore produce rotation and receiving checks")
A("hrs78", "Hours reinvested in lean stores a year", 78000, "hours", "$1.5M a year of reinvested hours (~78,000 hours, ~1 FTE per lean store)", f"{SL} p.24",
  "Team estimate, about one full-time employee per lean store")
A("labcut", "Targeted cut in chain store-labor hours, taken in high-labor stores", 0.03, "%", "5. Targeted rebalancing: −3% hours in high-labour stores", f"{SL} p.12, lever 5",
  "Plan choice in the analysis; sized as 3% of the chain's pro-forma labor bill")
A("dconcut", "Targeted reduction in third-party delivery rates at renewal", 0.05, "%", "Target a 5% reduction on the smaller volume ($0.5M)", f"{SL} p.13",
  "Negotiating target set in the analysis for the 2026 contract renewal")
A("closps", "Closure-cost allowance per lease-expiry store", 0.5, "$M", "~3.0 (allowance, $0.5M/store)", f"{SL} p.14",
  "Team planning allowance for closing a store at lease expiry, for the CFO to validate")
A("ot_tools", "One-time cost: labor scheduling and shrink tools, training", 3.0, "$M", "Labour scheduling and shrink tools, training · 3.0 · Allowance", f"{SL} p.17",
  "Team planning allowance for the CFO to validate", "one-time")
A("ot_pl", "One-time cost: private-label range development", 2.0, "$M", "Private-label range development · 2.0 · Allowance", f"{SL} p.17",
  "Team planning allowance for the CFO to validate", "one-time")
A("ot_promo", "One-time cost: promotion analytics and vendor negotiation", 1.0, "$M", "Promotion analytics and vendor negotiation · 1.0 · Allowance", f"{SL} p.17",
  "Team planning allowance for the CFO to validate", "one-time")
A("ot_del", "One-time cost: delivery pricing changes and pilot", 0.5, "$M", "Delivery pricing changes and pilot · 0.5 · Allowance", f"{SL} p.17",
  "Team planning allowance for the CFO to validate", "one-time")
PH = "FY2026 in-year phasing (team assumption): promotions 50%, vendor funding 25%, delivery 75%, labour 50%, private label ~25% of run-rate; FY2025 scale."
A("ph_promo", "Share of the promotion-reset run-rate reached in FY2026", 0.5, "%", PH, f"{SL} p.16 source note", "Team phasing assumption", "FY2026")
A("ph_vf", "Share of the vendor-funding run-rate reached in FY2026", 0.25, "%", PH, f"{SL} p.16 source note", "Team phasing assumption", "FY2026")
A("ph_del", "Share of the delivery-pricing run-rate reached in FY2026", 0.75, "%", PH, f"{SL} p.16 source note", "Team phasing assumption", "FY2026")
A("ph_lab", "Share of the labor-rebalancing run-rate reached in FY2026", 0.5, "%", PH, f"{SL} p.16 source note", "Team phasing assumption", "FY2026")
A("pl26", "Private-label gain in FY2026", 1.0, "$M", "Private-label trend · +1.0 (FY2026 bridge); 3. Private label · FY2026 in-year 1.0", f"{SL} p.16 chart, p.23",
  "Analysis value for 'private label ~25% of run-rate'; 25% of the $4.3M run-rate would be $1.1M, so the analysis's $1.0M is kept as stated", "FY2026")
A("optC", "FY2028 operating income, option C (margin-first, click-and-collect only)", 42.9, "$M", "~3.0% on firm levers ($42.9M)", f"{SL} p.11",
  "Analysis estimate; assumes 40% of home-delivery customers switch to click-and-collect. Not rebuilt from the pack", "FY2028")
A("sw40", "Share of home-delivery customers switching to click-and-collect under option C", 0.40, "%",
  "Option C assumes 40% of home-delivery customers switch to click-and-collect", f"{SL} p.11 source note", "Team assumption for option C")
A("w2del", "Second-wave gain from cost-recovery delivery pricing or membership", 3.0, "$M", "Cost-recovery delivery pricing or membership (pilot first) · 3.0", f"{SL} p.15",
  "Analysis estimate, set a little below the $3.2M that halving the remaining delivery loss would give", "FY2028")
A("lo7", "Store-exit gain, low case (the six stores carry less of the loss)", 3.0, "$M", "7. Exit 6 stores · Less loss in the 6 · 3.0 · 4.4 · 5.0 · More loss in the 6", f"{SL} p.23",
  "Analysis low case for the pro-rata split of the nine stores' losses; the split is not in the pack", "FY2028")
A("hi7", "Store-exit gain, high case (the six stores carry more of the loss)", 5.0, "$M", "7. Exit 6 stores · Less loss in the 6 · 3.0 · 4.4 · 5.0 · More loss in the 6", f"{SL} p.23",
  "Analysis high case for the pro-rata split of the nine stores' losses; the split is not in the pack", "FY2028")
A("gate24", "Mid-FY2027 checkpoint: run-rate operating margin that triggers the full second wave", 0.024, "%",
  "Mid-FY2027 checkpoint: if run-rate margin is below ~2.4%, trigger the second wave in full and put the fallback (C) to the owners", f"{SL} p.16",
  "Decision gate set in the analysis", "mid-FY2027")
A("lpo5", "Target loss per delivered order, FY2028", 5, "$", "Loss per delivered order · $12.34 → < $5", f"{SL} p.19 scorecard", "Scorecard target set in the analysis", "FY2028")
A("pilot02", "Shrink-pilot gain needed before scaling", 0.2, "pp", "Scale only if pilot gains ≥ 0.2 pts", f"{SL} p.18", "Decision gate set in the analysis", "FY2027")
LH = f"{SL} p.23 (low and high case drivers)"
A("lo_pr", "Promotion reset, low case: cut in promo share", 2, "pp", "Promo share −2 pts", LH, "Low case driver set in the analysis")
A("hi_pr", "Promotion reset, high case: cut in promo share", 5, "pp", "−5 pts (FY2023 level)", LH, "High case driver set in the analysis")
A("lo_vf", "Vendor funding, low case", 0.48, "%", "To 48%", LH, "Low case driver set in the analysis")
A("lo_pl", "Private-label share, low case", 0.20, "%", "To 20.0%", LH, "Low case driver set in the analysis")
A("hi_pl", "Private-label share, high case", 0.22, "%", "To 22.0%", LH, "High case driver set in the analysis")
A("lo_sh", "Shrink reduction, low case", 0.15, "pp", "−0.15 pts", LH, "Low case driver set in the analysis")
A("hi_sh", "Shrink reduction, high case", 0.40, "pp", "−0.40 pts", LH, "High case driver set in the analysis")
A("lo_lab", "Targeted labor cut, low case", 0.02, "%", "−2% hours", LH, "Low case driver set in the analysis")
A("hi_lab", "Targeted labor cut, high case", 0.04, "%", "−4% hours", LH, "High case driver set in the analysis")
A("lo_del", "Delivery pricing, low case: test result less 20%", 0.8, "x", "Test result − 20%; no contract gain", LH, "Low case driver set in the analysis")
A("hi_del", "Delivery pricing, high case: test result plus 30%", 1.3, "x", "Test +30%; contract −5%", LH, "High case driver set in the analysis")
SH = f"{SL} p.18 (sensitivity table)"
A("s_traf50", "Share of the gross promotion gain lost to lower traffic, downside case", 0.5, "%", "25% of gross gain lost · 50% lost", SH, "Downside case set in the analysis")
A("s_new50", "Share of e-commerce sales new to Harlow, upside case", 0.5, "%", "30% · 50% · Loss shrinks to −$5.3M", SH, "Upside case set in the analysis")
A("s_shr245", "Shrink reached, downside case", 0.0245, "%", "2.6% → 2.3% · Only 2.45%", SH, "Downside case set in the analysis")
A("s_w6", "2027 wage step, downside case", 0.06, "%", "+4% on full bill · +6%", SH, "Downside case set in the analysis")
A("third", "Share of FY2025's operating-income erosion that would use up the FY2026 headroom", 0.33, "%",
  "Risk: if about a third of FY2025's $18M erosion recurs, the headroom is gone", f"{SL} p.16", "Analysis risk threshold ('about a third')", "FY2026")

D("contrib", "Contribution per dollar of sales new to Harlow, as a fraction", "$", "contrib20 / 100", "20 cents ÷ 100")
# ---------------- derived: ratios and the margin bridge
D("gm23r", "Gross margin, % of sales, FY2023", "%", "gp23 / sales23", "Gross profit ÷ sales", "FY2023")
D("gm24r", "Gross margin, % of sales, FY2024", "%", "gp24 / sales24", "Gross profit ÷ sales", "FY2024")
D("gm25r", "Gross margin, % of sales, FY2025", "%", "gp25 / sales25", "Gross profit ÷ sales", "FY2025")
for k, nm in [("lab", "Store labor"), ("occ", "Occupancy and energy"), ("ecf", "E-commerce fulfillment"), ("sga", "Other SG&A")]:
    for y in ("23", "24", "25"):
        D(f"{k}{y}r", f"{nm}, % of sales, FY20{y}", "%", f"{k}{y} / sales{y}", f"{nm} ÷ sales", f"FY20{y}")
D("dgm", "Change in gross margin, FY2023 to FY2025", "%", "gm25r - gm23r", "Gross margin % FY2025 − FY2023", "FY2023–FY2025")
D("dec", "Effect of e-commerce fulfillment on operating margin, FY2023 to FY2025", "%", "ecf23r - ecf25r", "−(change in fulfillment cost % of sales)", "FY2023–FY2025")
D("dlab", "Effect of store labor on operating margin, FY2023 to FY2025", "%", "lab23r - lab25r", "−(change in labor % of sales)", "FY2023–FY2025")
D("docc", "Effect of occupancy and energy on operating margin, FY2023 to FY2025", "%", "occ23r - occ25r", "−(change in occupancy % of sales)", "FY2023–FY2025")
D("dsga", "Effect of other SG&A on operating margin, FY2023 to FY2025", "%", "sga23r - sga25r", "−(change in other SG&A % of sales)", "FY2023–FY2025")
D("dom", "Change in operating margin, FY2023 to FY2025", "%", "om25 - om23", "1.02% − 3.37%", "FY2023–FY2025")
D("sh_gmec", "Share of the margin decline from gross margin and e-commerce fulfillment", "%", "(dgm + dec) / dom", "(−1.02 − 0.84) ÷ −2.35", "FY2023–FY2025")
D("sh_gm", "Share of the margin decline from gross margin", "%", "dgm / dom", "−1.02 ÷ −2.35", "FY2023–FY2025")
D("sh_ec", "Share of the margin decline from e-commerce fulfillment", "%", "dec / dom", "−0.84 ÷ −2.35", "FY2023–FY2025")
D("sh_lab", "Share of the margin decline from store labor", "%", "dlab / dom", "−0.30 ÷ −2.35", "FY2023–FY2025")
D("sh_occ", "Share of the margin decline from occupancy and energy", "%", "docc / dom", "−0.20 ÷ −2.35", "FY2023–FY2025")
for k in ("dgm", "dec", "dlab", "docc", "dsga", "dom"):
    D(f"{k}_d", f"{DPS[k]['label']}, $M at FY2025 sales", "$M", f"{k} * sales25", "Change in ratio × FY2025 sales of $1,503M", "FY2023–FY2025")
for k in ("dgm", "dec", "dlab", "docc", "dsga", "dom"):
    D(f"{k}_b", f"{DPS[k]['label']}, basis points", "bps", f"{k} * 10000", "Change in ratio × 10,000", "FY2023–FY2025")
D("salesg", "Sales growth, FY2023 to FY2025", "%", "sales25 / sales23 - 1", "1,503 ÷ 1,420 − 1", "FY2023–FY2025")
D("labrise", "Increase in store labor cost, FY2023 to FY2025", "$M", "lab25 - lab23", "181.9 − 167.6", "FY2023–FY2025")
D("lab_at23", "FY2025 labor cost at FY2023's 11.8% of sales", "$M", "labpct23 * sales25", "11.8% × $1,503M")
D("labex", "Store labor above FY2023's ratio, FY2025", "$M", "lab25 - lab_at23", "181.9 − 177.4")

# gross margin mix effects
D("mpromo", "Gross-margin effect of more promotional sales, FY2023 to FY2025", "%", "(promo23 - promo25) * promogap / 100",
  "(24.0% − 29.0%) × 14 percentage points", "FY2023–FY2025")
D("mshr", "Gross-margin effect of higher shrink, FY2023 to FY2025", "%", "shr23 - shr25", "−(2.6% − 2.1%)", "FY2023–FY2025")
D("mpl", "Gross-margin effect of more private label, FY2023 to FY2025", "%", "(pl25 - pl23) * plgap / 100", "(18.5% − 17.0%) × 12 percentage points", "FY2023–FY2025")
D("mpromo_d", "Annual cost of the added promotional share at FY2025 sales", "$M", "0 - mpromo * sales25", "0.70% × $1,503M")
D("mshr_d", "Annual cost of the higher shrink at FY2025 sales", "$M", "0 - mshr * sales25", "0.50% × $1,503M")
D("mpl_d", "Annual gain from the higher private-label share at FY2025 sales", "$M", "mpl * sales25", "0.18% × $1,503M")
D("plof", "Private-label gain as a share of the net gross-margin loss", "%", "mpl / (0 - dgm)", "0.18 ÷ 1.02", "FY2023–FY2025")
D("shr_d", "Shrink cost, FY2025", "$M", "shr25 * sales25", "2.6% × $1,503M")
D("promo_add", "Rise in promotional share of sales, FY2023 to FY2025", "pp", "(promo25 - promo23) * 100", "29.0% − 24.0%", "FY2023–FY2025")
D("be53", "New sales needed a year to repay the added promotional share", "$M", "mpromo_d / contrib", "$10.5M ÷ 20 cents of contribution per new sales dollar")
D("pc_gap", "Comparable-sales gain of the deepest-promotion stores over the rest", "pp", "(pcd - pcr) * 100", "1.8% − 0.2%")
D("pc_ben", "Contribution of that comparable-sales gain, % of sales", "pp", "pc_gap * contrib", "1.6 percentage points × 20 cents")
D("pc_cost", "Gross-margin cost of one more percentage point of promotional share", "pp", "promogap / 100", "1 percentage point × 14 percentage points")
D("pc_max", "Most extra promotional share the comparable-sales gain can pay for", "pp", "pc_ben / pc_cost", "0.32 ÷ 0.14")
D("pc_rep", "Share of the margin cost of the added promotion repaid by the comparable-sales gain", "%", "pc_ben / promo_add / pc_cost", "0.32 ÷ (5 × 0.14)")
D("pp1", "Margin cost of one more percentage point of promotional share, FY2025 scale", "$M", "pc_cost / 100 * sales25", "0.14% × $1,503M")

# labor decomposition
D("wrise", "Rise in average hourly wage incl. benefits, FY2023 to FY2025", "%", "wage25 / wage23 - 1", "18.38 ÷ 16.80 − 1", "FY2023–FY2025")
D("hchg", "Change in labor hours per $1,000 of sales, FY2023 to FY2025", "%", "hrs25 / hrs23 - 1", "6.60 ÷ 7.02 − 1", "FY2023–FY2025")
D("lp23c", "Store labor, % of sales, FY2023 (hours × wage)", "%", "hrs23 * wage23 / 1000", "7.02 × $16.80 ÷ 1,000", "FY2023")
D("lp25c", "Store labor, % of sales, FY2025 (hours × wage)", "%", "hrs25 * wage25 / 1000", "6.60 × $18.38 ÷ 1,000", "FY2025")
D("weff", "Wage effect on labor % of sales at FY2023 hours", "%", "hrs23 * (wage25 - wage23) / 1000", "7.02 × ($18.38 − $16.80) ÷ 1,000", "FY2023–FY2025")
D("peff", "Productivity effect on labor % of sales at FY2025 wage", "%", "(hrs25 - hrs23) * wage25 / 1000", "(6.60 − 7.02) × $18.38 ÷ 1,000", "FY2023–FY2025")
D("psh", "Share of the wage effect offset by productivity", "%", "(0 - peff) / weff", "0.77 ÷ 1.11", "FY2023–FY2025")
D("thr23", "Total store labor hours, FY2023", "million hours", "hrs23 * sales23 / 1000", "7.02 × $1,420M ÷ 1,000", "FY2023")
D("thr25", "Total store labor hours, FY2025", "million hours", "hrs25 * sales25 / 1000", "6.60 × $1,503M ÷ 1,000", "FY2025")
D("lab_p23", "FY2025 labor cost at FY2023 hours per $1,000 of sales", "$M", "hrs23 * sales25 * wage25 / 1000", "7.02 × $1,503M × $18.38 ÷ 1,000")
D("q12", "Shrink gap between quartiles Q1 and Q2", "pp", "(q1 - q2) * 100", "3.1% − 2.7%")
D("q34", "Shrink gap between quartiles Q3 and Q4", "pp", "(q3 - q4) * 100", "2.4% − 2.3%")
D("wa65", "Waste and receiving errors, share of shrink", "%", "waste + admin", "45% + 20%")

# e-commerce economics
D("newsh", "Share of e-commerce sales new to Harlow", "%", "1 - surv70", "100% − 70% (survey)")
D("del25", "Home-delivered orders, FY2025", "thousand orders", "ord25 * dsh25", "1,331 × 58%")
D("del24", "Home-delivered orders, FY2024", "thousand orders", "ord24 * dsh24", "865 × 52%", "FY2024")
D("del23", "Home-delivered orders, FY2023", "thousand orders", "ord23 * dsh23", "453 × 45%", "FY2023")
D("cc25", "Click-and-collect orders, FY2025", "thousand orders", "ord25 - del25", "1,331 − 772")
for y in ("23", "24", "25"):
    D(f"pk{y}t", f"Picking cost, FY20{y}", "$M", f"ord{y} * pick{y} / 1000", "Orders × picking cost per order", f"FY20{y}")
    D(f"dc{y}t", f"Third-party delivery cost, FY20{y}", "$M", f"del{y} * dc{y} / 1000", "Delivered orders × cost per delivered order", f"FY20{y}")
    D(f"fe{y}t", f"Delivery fees collected, FY20{y}", "$M", f"del{y} * fee{y} / 1000", "Delivered orders × fee per delivered order", f"FY20{y}")
    D(f"nf{y}", f"Net e-commerce fulfillment cost rebuilt from order data, FY20{y}", "$M", f"pk{y}t + dc{y}t - fe{y}t", "Picking + delivery − fees", f"FY20{y}")
    D(f"ecs{y}", f"E-commerce sales, FY20{y}", "$M", f"ord{y} * bask{y} / 1000", "Orders × average basket", f"FY20{y}")
    D(f"inc{y}", f"Contribution from e-commerce sales new to Harlow, FY20{y}", "$M", f"ecs{y} * newsh * contrib", "Sales × 30% new × 20 cents", f"FY20{y}")
    D(f"ecr{y}", f"Fully costed e-commerce result, FY20{y}", "$M", f"inc{y} - ecf{y}", "Contribution − net fulfillment cost (Table 1)", f"FY20{y}")
    D(f"fcov{y}", f"Delivery fee as a share of delivery cost per delivered order, FY20{y}", "%", f"fee{y} / dc{y}", "Fee ÷ cost per delivered order", f"FY20{y}")
D("inc_o", "Contribution per order from sales new to Harlow", "$", "bask25 * newsh * contrib", "$96 basket × 30% new × 20 cents")
D("pickn", "Picking cost per order (as a cost)", "$", "0 - pick25", "−$7.40")
D("dcn", "Third-party delivery cost per delivered order (as a cost)", "$", "0 - dc25", "−$13.80")
D("npo_cc", "Net result per click-and-collect order", "$", "inc_o - pick25", "$5.76 − $7.40")
D("npo_del", "Net result per home-delivered order", "$", "inc_o - pick25 - dc25 + fee25", "$5.76 − $7.40 − $13.80 + $3.10")
D("res_cc", "Annual result, click-and-collect", "$M", "cc25 * npo_cc / 1000", "559 thousand × −$1.64")
D("res_del", "Annual result, home delivery", "$M", "del25 * npo_del / 1000", "772 thousand × −$12.34")
D("be_del", "Share of sales that must be new to Harlow for home delivery to break even", "%", "(pick25 + dc25 - fee25) / (bask25 * contrib)",
  "($7.40 + $13.80 − $3.10) ÷ ($96 × 20 cents)")
D("be_cc", "Share of sales that must be new to Harlow for click-and-collect to break even", "%", "pick25 / (bask25 * contrib)", "$7.40 ÷ ($96 × 20 cents)")
D("ecres", "Fully costed e-commerce result, FY2025", "$M", "(cc25 * npo_cc + del25 * npo_del) / 1000", "559k × −$1.64 + 772k × −$12.34 (equals $127.8M × 30% × 20 cents − $18.1M)")
D("ecloss", "Fully costed e-commerce loss, FY2025", "$M", "0 - (cc25 * npo_cc + del25 * npo_del) / 1000", "−(559k × −$1.64 + 772k × −$12.34)")
D("delnet", "Third-party delivery cost net of fees, FY2025", "$M", "dc25t - fe25t", "$10.7M − $2.4M")
D("rc1", "Margin effect of adding third-party delivery net of fees", "%", "(0 - delnet) / ecs25", "−$8.3M ÷ $127.8M")
D("ecfc", "Fully costed e-commerce margin, % of e-commerce sales", "%", "ecres / ecs25", "−$10.4M ÷ $127.8M")
D("rc2", "Margin effect of counting only sales new to Harlow (finance method)", "%", "ecfc - ecm - rc1", "−8.2% − 6.1% + 6.5%")
D("ecm_d", "E-commerce team's contribution, FY2025", "$M", "ecm * ecs25", "6.1% × $127.8M")
D("ecm_dl", "E-commerce team's contribution after net delivery cost", "$M", "ecm_d - delnet", "$7.8M − $8.3M")
D("ecm_dlr", "E-commerce team's margin after net delivery cost", "%", "ecm_dl / ecs25", "−$0.5M ÷ $127.8M")

# ---------------- plan baseline
D("s6sales", "Combined sales of the six stores with leases ending by 2027", "$M", "s9sales * 6 / 9", "$118.0M × 6/9 (pro rata)")
D("s3sales", "Combined sales of the three other weak stores", "$M", "s9sales * 3 / 9", "$118.0M × 3/9 (pro rata)")
D("e6", "Four-wall EBITDA of the six stores", "$M", "s9ebitda * 6 / 9", "−$3.1M × 6/9 (pro rata)")
D("e3", "Four-wall EBITDA of the three other stores", "$M", "s9ebitda * 3 / 9", "−$3.1M × 3/9 (pro rata)")
D("mv6", "Sales moving to nearby Harlow stores if the six close", "$M", "s6sales * mov25", "$78.7M × 25%")
D("mv3", "Sales moving to nearby Harlow stores if the three close", "$M", "s3sales * mov25", "$39.3M × 25%")
D("mv9", "Sales moving to nearby Harlow stores if all nine close", "$M", "s9sales * mov25", "$118.0M × 25%")
D("ct6", "Contribution on sales moved from the six", "$M", "mv6 * mov12", "$19.7M × 12%")
D("ct3", "Contribution on sales moved from the three", "$M", "mv3 * mov12", "$9.8M × 12%")
D("ct9", "Contribution on sales moved from all nine", "$M", "mv9 * mov12", "$29.5M × 12%")
D("pfs", "Pro-forma sales after exiting the six lease-expiry stores", "$M", "sales25 - s6sales + mv6", "$1,503M − $78.7M + $19.7M", "FY2028 (FY2025 scale)")
D("pfs9", "Pro-forma sales after exiting all nine weak stores", "$M", "pfs - s3sales + mv3", "$1,444M − $39.3M + $9.8M", "FY2028 (FY2025 scale)")
D("wage27", "Cost of the 2027 minimum-wage step on the full labor bill", "$M", "0 - minw * lab25", "−4% × $181.9M", "FY2028",
  assumptions=["The +4% applies to the whole FY2025 labor bill of $181.9M (conservative)"])
D("dlv27", "Cost of the proposed 3% third-party delivery rate rise", "$M", "0 - drise * dc25t", "−3% × $10.7M", "FY2028",
  assumptions=["The provider's proposed +3% is accepted in the do-nothing case"])
D("cost27", "Wage step and delivery rate rise combined", "$M", "wage27 + dlv27", "−$7.3M − $0.3M", "FY2028")
D("oi28na", "FY2028 operating income with no action", "$M", "oi25 + wage27 + dlv27", "$15.3M − $7.3M − $0.3M", "FY2028",
  assumptions=["FY2025 cost ratios and sales scale held constant: no further erosion (optimistic)"])
D("om28na", "FY2028 operating margin with no action", "%", "(oi25 + wage27 + dlv27) / sales25", "$7.7M ÷ $1,503M", "FY2028")
D("tgt28", "Operating income at the 3.0% target on pro-forma sales", "$M", "tgtm * pfs", "3.0% × $1,444M", "FY2028")
D("gap", "Operating income to add to reach the 3.0% target by FY2028", "$M", "tgt28 - oi28na", "$43.3M − $7.7M", "FY2028")
D("tgt9", "Operating income at the 3.0% target after exiting all nine stores", "$M", "tgtm * pfs9", "3.0% × $1,415M", "FY2028")

# management draft plan
D("shr_hi", "Added shrink if every store moves fully onto the leanest quartile", "pp", "(q1 - shr25) * 100", "3.1% − 2.6%", "FY2028")
D("shr_lo", "Added shrink if every store moves halfway onto the leanest quartile", "pp", "shr_hi / 2", "0.50 ÷ 2", "FY2028")
D("shrrng", "Cost of added shrink under the 8% cut", "$M", "shr_lo / 100 * sales25", "0.25% to 0.50% × $1,503M", "FY2028",
  value_high=None)
DPS["shrrng"]["value_high"] = round(DPS["shr_hi"]["value"] / 100 * 1503.0, 6)
D("shrmid", "Cost of added shrink under the 8% cut, midpoint", "$M", "0 - (shr_lo + shr_hi) / 2 / 100 * sales25", "−0.375% × $1,503M", "FY2028")
D("oidraft", "FY2028 operating income under management's draft plan", "$M", "oi28na + cut145 + shrmid", "$7.7M + $14.5M − $5.6M", "FY2028")
D("omdraft", "FY2028 operating margin under management's draft plan", "%", "oidraft / sales25", "$16.6M ÷ $1,503M", "FY2028")
D("tgtd", "Operating income at the 3.0% target on unchanged sales", "$M", "tgtm * sales25", "3.0% × $1,503M", "FY2028")
D("lost1", "Contribution lost per 1% of sales lost", "$M", "0.01 * sales25 * contrib", "1% × $1,503M × 20 cents")

# ---------------- firm levers (FY2028 run-rate on pro-forma sales)
D("mkd", "Implied gross promotional markdown before vendor funding", "pp", "promogap / (1 - vf25)", "14 ÷ (1 − 46%)")
D("gapvf", "Net promotional margin gap with vendor funding at 50%", "pp", "mkd * (1 - vftgt)", "25.9 × (1 − 50%)", "FY2028")
D("ppost", "Promotional sales after the reset, pro-forma", "$M", "promotgt * pfs", "25% × $1,444M", "FY2028")
D("lev1g", "Promotion reset, gross of lost volume", "$M", "(promo25 - promotgt) * promogap / 100 * pfs", "4 pp × 14 pp × $1,444M", "FY2028")
D("lev1", "Lever 1: promotion reset", "$M", "lev1g * (1 - lostvol)", "$8.1M × (1 − 25%)", "FY2028")
D("lev2", "Lever 2: vendor funding of markdowns from 46% to 50%", "$M", "mkd / 100 * (vftgt - vf25) * ppost", "25.9 pp × 4% × $361M", "FY2028")
D("lev3", "Lever 3: private-label share from 18.5% to 21%", "$M", "(pltgt - pl25) * plgap / 100 * pfs", "2.5 pp × 12 pp × $1,444M", "FY2028")
D("lev4", "Lever 4: shrink from 2.6% to 2.3%, net of reinvested hours", "$M", "(shr25 - shrtgt) * pfs - reinv", "0.3% × $1,444M − $1.5M", "FY2028")
D("labpf", "Store labor bill, pro-forma after exiting six stores", "$M", "lab25 * pfs / sales25", "$181.9M × $1,444M ÷ $1,503M", "FY2028")
D("wf27", "2027 wage factor", "x", "1 + minw", "1 + 4%", "FY2028")
D("lev5", "Lever 5: targeted labor rebalancing", "$M", "labcut * labpf * wf27", "3% × $174.8M × 1.04", "FY2028")
# delivery pricing (fee test on FY2025 base)
D("del_t", "Home-delivered orders at tested pricing", "thousand orders", "del25 * (1 + ft_del)", "772 × (1 − 9%)")
D("cc_t", "Click-and-collect orders at tested pricing", "thousand orders", "cc25 * (1 + ft_cc)", "559 × (1 + 14%)")
D("ecs_t", "E-commerce sales at tested pricing", "$M", "ecs25 * (1 + ft_sales)", "$127.8M × (1 − 2%)")
D("pk_t", "Picking cost at tested pricing", "$M", "(del_t + cc_t) * pick25 / 1000", "(703 + 637) × $7.40")
D("dc_t", "Third-party delivery cost at tested pricing", "$M", "del_t * dc25 / 1000", "703 × $13.80")
D("fe_t", "Delivery fees collected at tested pricing", "$M", "del_t * ft_fpo / 1000", "703 × $6.40")
D("nf_t", "Net fulfillment cost at tested pricing", "$M", "pk_t + dc_t - fe_t", "Picking + delivery − fees")
D("ch_fpo", "Change in fee collected per delivered order", "$", "ft_fpo - fee25", "$6.40 − $3.10")
D("ch_pk", "Change in picking cost", "$M", "pk_t - pk25t", "Tested − FY2025")
D("ch_dc", "Change in third-party delivery cost", "$M", "dc_t - dc25t", "Tested − FY2025")
D("ch_fe", "Change in delivery fees collected", "$M", "fe_t - fe25t", "Tested − FY2025")
D("ch_nf", "Change in net fulfillment cost", "$M", "nf_t - nf25", "Tested − FY2025")
D("lostc", "Contribution lost on the 2% of e-commerce sales lost", "$M", "(0 - ft_sales) * ecs25 * contrib", "2% × $127.8M × 20 cents")
D("dnet", "Net gain from rolling out the tested delivery pricing", "$M", "nf25 - nf_t - lostc", "$3.0M saved − $0.5M lost contribution", "FY2028")
D("dref", "Value of refusing the proposed 3% delivery rate rise", "$M", "drise * dc_t", "3% × $9.7M", "FY2028")
D("dred", "Value of a 5% delivery rate reduction on the smaller volume", "$M", "dconcut * dc_t", "5% × $9.7M", "FY2028")
D("dcon", "Gain from the 2026 delivery contract renewal", "$M", "(drise + dconcut) * dc_t", "(3% + 5%) × $9.7M", "FY2028")
D("lev6", "Lever 6: tested delivery pricing and contract renewal", "$M", "dnet + dcon", "$2.5M + $0.8M", "FY2028")
D("npo_t", "Net result per home-delivered order at tested pricing", "$", "inc_o - pick25 - dc25 + ft_fpo", "$5.76 − $7.40 − $13.80 + $6.40", "FY2028")
D("dleft", "Remaining annual loss on home-delivered orders at tested pricing", "$M", "del_t * npo_t / 1000", "703 thousand × −$9.04", "FY2028")
D("dfix", "Share of the e-commerce loss fixed by the tested pricing", "%", "dnet / (0 - ecres)", "$2.5M ÷ $10.4M", "FY2028")
D("dhalf", "Value of halving the remaining delivery loss", "$M", "(0 - dleft) / 2", "$6.4M ÷ 2", "FY2028")
# stores
D("g6", "Lever 7: annual operating-income gain from exiting the six stores", "$M", "0 - e6 + ct6", "$2.1M losses removed + $2.4M moved contribution", "FY2028")
D("g3", "Annual operating-income gain from exiting the three other stores", "$M", "0 - e3 + ct3", "$1.0M + $1.2M", "FY2028")
D("g9", "Annual operating-income gain from exiting all nine stores", "$M", "0 - s9ebitda + ct9", "$3.1M + $3.5M", "FY2028")
D("clos6", "Closure costs for the six lease-expiry stores", "$M", "closps * 6", "6 × $0.5M allowance", "one-time")
D("ot9", "One-time cost of exiting all nine stores", "$M", "clos6 + ls3", "$3.0M + $7.5M", "one-time")
D("pb6", "Payback on exiting the six stores", "years", "clos6 / g6", "$3.0M ÷ $4.4M", "FY2028")
D("pb3", "Payback on exiting the three other stores", "years", "ls3 / g3", "$7.5M ÷ $2.2M", "FY2028")
D("pb9", "Payback on exiting all nine stores", "years", "ot9 / g9", "$10.5M ÷ $6.6M", "FY2028")
D("lev7", "Lever 7: exit six negative-EBITDA stores at lease expiry", "$M", "g6", "= gain from exiting the six", "FY2028")
# totals
D("gm4", "Gross-margin levers 1–4", "$M", "lev1 + lev2 + lev3 + lev4", "Levers 1 + 2 + 3 + 4", "FY2028")
D("levtot", "Seven firm levers, FY2028 run-rate", "$M", "lev1 + lev2 + lev3 + lev4 + lev5 + lev6 + lev7", "Sum of levers 1–7", "FY2028")
D("pd13", "Promotion, vendor funding and delivery levers (the starting hypothesis)", "$M", "lev1 + lev2 + lev6", "Levers 1 + 2 + 6", "FY2028")
D("oifirm", "FY2028 operating income on the firm levers", "$M", "oi28na + levtot", "$7.7M + $30.1M", "FY2028")
D("omfirm", "FY2028 operating margin on the firm levers", "%", "oifirm / pfs", "$37.8M ÷ $1,444M", "FY2028")
D("gapfirm", "Gap left to the 3.0% target by the firm levers", "$M", "tgt28 - oifirm", "$43.3M − $37.8M", "FY2028")
D("w2vf", "Second wave: vendor funding from 50% back to FY2023's 55%", "$M", "mkd / 100 * (vf23 - vftgt) * ppost", "25.9 pp × 5% × $361M", "FY2028")
D("w2tot", "Second wave, all three options", "$M", "g3 + w2del + w2vf", "$2.2M + $3.0M + $4.7M", "FY2028")
D("w2need", "Share of the second wave needed to reach 3.0%", "%", "gapfirm / w2tot", "$5.5M ÷ $9.9M", "FY2028")
D("oifull", "FY2028 operating income with the full second wave", "$M", "oifirm + w2tot", "$37.8M + $9.9M", "FY2028")
D("omfull", "FY2028 operating margin with the full second wave", "%", "oifull / pfs9", "$47.7M ÷ $1,415M", "FY2028")
D("omC", "FY2028 operating margin, option C", "%", "optC / pfs", "$42.9M ÷ $1,444M", "FY2028")
# ranges
D("lo1", "Lever 1, low case", "$M", "lo_pr / 100 * promogap / 100 * pfs * (1 - lostvol)", "2 pp × 14 pp × $1,444M × 75%", "FY2028")
D("hi1", "Lever 1, high case", "$M", "hi_pr / 100 * promogap / 100 * pfs * (1 - lostvol)", "5 pp × 14 pp × $1,444M × 75%", "FY2028")
D("lo2", "Lever 2, low case", "$M", "mkd / 100 * (lo_vf - vf25) * ppost", "25.9 pp × 2% × $361M", "FY2028")
D("lo3", "Lever 3, low case", "$M", "(lo_pl - pl25) * plgap / 100 * pfs", "1.5 pp × 12 pp × $1,444M", "FY2028")
D("hi3", "Lever 3, high case", "$M", "(hi_pl - pl25) * plgap / 100 * pfs", "3.5 pp × 12 pp × $1,444M", "FY2028")
D("lo4", "Lever 4, low case", "$M", "lo_sh / 100 * pfs - reinv", "0.15% × $1,444M − $1.5M", "FY2028")
D("hi4", "Lever 4, high case", "$M", "hi_sh / 100 * pfs - reinv", "0.40% × $1,444M − $1.5M", "FY2028")
D("lo5", "Lever 5, low case", "$M", "lo_lab * labpf * wf27", "2% × $174.8M × 1.04", "FY2028")
D("hi5", "Lever 5, high case", "$M", "hi_lab * labpf * wf27", "4% × $174.8M × 1.04", "FY2028")
D("lo6", "Lever 6, low case", "$M", "dnet * lo_del", "$2.5M × 0.8, no contract gain", "FY2028")
D("hi6", "Lever 6, high case", "$M", "dnet * hi_del + dcon", "$2.5M × 1.3 + $0.8M", "FY2028")
D("levlo", "Seven firm levers, low case", "$M", "lo1 + lo2 + lo3 + lo4 + lo5 + lo6 + lo7", "Sum of low cases", "FY2028")
D("levhi", "Seven firm levers, high case", "$M", "hi1 + lev2 + hi3 + hi4 + hi5 + hi6 + hi7", "Sum of high cases (lever 2 high = base)", "FY2028")
D("oilo", "FY2028 operating income on the firm levers, low case", "$M", "oi28na + levlo", "$7.7M + $16.8M", "FY2028")
D("oihi", "FY2028 operating income on the firm levers, high case", "$M", "oi28na + levhi", "$7.7M + $37.9M", "FY2028")
D("omlo", "FY2028 operating margin, low case", "%", "oilo / pfs", "$24.5M ÷ $1,444M", "FY2028")
D("omhi", "FY2028 operating margin, high case", "%", "oihi / pfs", "$45.6M ÷ $1,444M", "FY2028")
for i, (lo, hi, base) in enumerate([("lo1", "hi1", "lev1"), ("lo2", "lev2", "lev2"), ("lo3", "hi3", "lev3"), ("lo4", "hi4", "lev4"),
                                    ("lo5", "hi5", "lev5"), ("lo6", "hi6", "lev6"), ("lo7", "hi7", "lev7"), ("levlo", "levhi", "levtot")], 1):
    rid = f"rng{i}" if i < 8 else "rngtot"
    D(rid, f"Range, {DPS[base]['label']}", "$M", lo, f"Low {lo} to high {hi}", "FY2028")
    DPS[rid]["value_high"] = DPS[hi]["value"]
    DPS[rid]["derived_from"] = [lo, hi]

# one-time cost
D("otot", "One-time cost of the full plan", "$M", "ls3 + clos6 + ot_tools + ot_pl + ot_promo + ot_del", "7.5 + 3.0 + 3.0 + 2.0 + 1.0 + 0.5", "FY2026–FY2028")
D("cont", "Contingency left under the $25M cap", "$M", "cap - otot", "$25M − $17M", "FY2026–FY2028")
D("otfirm", "One-time cost of the firm wave (all but the three-store lease exit)", "$M", "otot - ls3", "$17.0M − $7.5M", "FY2026–FY2028")
D("hr184", "Times the firm-wave allowances the cap can absorb with the lease exit in", "x", "(cap - ls3) / otfirm", "($25M − $7.5M) ÷ $9.5M", "FY2026–FY2028")
D("sh75", "Three-store lease exit as a share of the plan's one-time cost", "%", "ls3 / otot", "$7.5M ÷ $17.0M", "FY2026–FY2028")

# FY2026
D("promo26", "FY2026 gain from the promotion reset", "$M", "ph_promo * (promo25 - promotgt) * promogap / 100 * sales25 * (1 - lostvol)", "50% × 4 pp × 14 pp × $1,503M × 75%", "FY2026")
D("vf26", "FY2026 gain from vendor funding", "$M", "ph_vf * mkd / 100 * (vftgt - vf25) * promotgt * sales25", "25% × 25.9 pp × 4% × 25% × $1,503M", "FY2026")
D("dhy", "Half-year cost of the delivery contract rise", "$M", "0.5 * drise * dc25t", "½ × 3% × $10.7M", "FY2026")
D("del26", "FY2026 gain from delivery pricing, net of the half-year contract rise", "$M", "ph_del * dnet - dhy", "75% × $2.5M − $0.2M", "FY2026")
D("lab26", "FY2026 gain from labor rebalancing", "$M", "ph_lab * labcut * lab25", "50% × 3% × $181.9M", "FY2026")
D("tot26", "FY2026 gain from the first moves", "$M", "promo26 + vf26 + del26 + lab26 + pl26", "Sum", "FY2026")
D("oi26", "FY2026 operating income with the first moves", "$M", "oi25 + tot26", "$15.3M + $9.6M", "FY2026")
D("head26", "FY2026 headroom over the $20M covenant", "$M", "oi26 - cov", "$24.9M − $20M", "FY2026")
D("eros", "Operating-income erosion, FY2024 to FY2025", "$M", "oi24 - oi25", "$33.4M − $15.3M", "FY2024–FY2025")
D("eros3", "A third of FY2025's operating-income erosion", "$M", "third * eros", "⅓ × $18.1M", "FY2026")

# sensitivities (change to FY2028 operating income against the base plan)
D("s_traf", "Sensitivity: half rather than a quarter of the promotion gain lost to traffic", "$M", "0 - (s_traf50 - lostvol) * lev1g", "−25% × $8.1M", "FY2028")
D("s_vf", "Sensitivity: vendor funding stays at 46%", "$M", "0 - lev2", "−$3.7M", "FY2028")
D("s_newl", "E-commerce result if half its sales are new to Harlow", "$M", "ecs25 * s_new50 * contrib - ecf25", "$127.8M × 50% × 20 cents − $18.1M")
D("s_newd", "Result per delivered order if half of sales are new to Harlow", "$", "bask25 * s_new50 * contrib - pick25 - dc25 + fee25", "$9.60 − $7.40 − $13.80 + $3.10")
D("s_shr", "Sensitivity: shrink reaches only 2.45%", "$M", "0 - (s_shr245 - shrtgt) * pfs", "−0.15% × $1,444M", "FY2028")
D("s_w", "Sensitivity: 2027 wage step of 6% rather than 4%", "$M", "0 - (s_w6 - minw) * lab25", "−2% × $181.9M", "FY2028")
D("s_sto", "Sensitivity: the six stores carry less of the loss", "$M", "lo7 - lev7", "$3.0M − $4.4M", "FY2028")
D("wrise9", "Hourly wage rise cited by management", "%", "wrise", "= 9.4%", "FY2023–FY2025")
del DPS["wrise9"]; ORDER.remove("wrise9")
